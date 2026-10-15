#!/usr/bin/env python3
"""Compile a LaTeX document and print a short report of errors and warnings.

Uses latexmk when it runs; otherwise runs the engine, biber or bibtex, and reruns
until references settle. Shell escape stays off unless --shell-escape is given.
latexmk rc files are disabled unless --trust-project-config is given; rc files
execute Perl independently of TeX shell escape. Neither option is a sandbox.
Python 3.8+, standard library only; Windows, macOS and Linux.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ENGINES = {"lualatex": "-lualatex", "xelatex": "-xelatex", "pdflatex": "-pdf"}
RERUN = re.compile(r"Rerun to get|Label\(s\) may have changed|Please rerun|Please \(re\)run (?:Biber|BibTeX)")


def choose_engine(source):
    """Magic comment first, then fontspec/unicode-math (need a Unicode engine), else lualatex."""
    m = re.search(r"^%\s*!TEX\s+(?:TS-)?program\s*=\s*(\w+)", source, re.M | re.I)
    if m and m.group(1).lower() in ENGINES:
        return m.group(1).lower()
    return "lualatex"


def unwrap(text):
    """Undo TeX's log wrapping: a line of exactly 79 characters continues on the next."""
    out = []
    joining = False
    for line in text.splitlines():
        if joining:
            out[-1] += line
        else:
            out.append(line)
        joining = len(line) == 79
    return out


def parse_log(text):
    """Return a dict of errors, undefined references/citations, overfull boxes and missing glyphs."""
    lines = unwrap(text)
    errors = []
    for i, line in enumerate(lines):
        # -file-line-error style "./file.tex:12: message" or classic "! message" followed by "l.12".
        m = re.match(r"^(.*?\.(?:tex|sty|cls|bib)):(\d+): (.*)", line)
        if m and "==> Fatal error occurred" not in line:
            # Package errors continue on lines prefixed "(package)".
            more = []
            for nxt in lines[i + 1:i + 8]:
                if not nxt.startswith("("):
                    break
                more.append(nxt.split(")", 1)[1].strip())
            errors.append(" ".join(["%s:%s: %s" % m.groups()] + [x for x in more if x]))
        elif line.startswith("! "):
            where = next((l for l in lines[i + 1:i + 12] if re.match(r"^l\.\d+", l)), "")
            errors.append(line[2:] + (" (" + where.split(" ", 1)[0] + ")" if where else ""))
    text = "\n".join(lines)
    overfull = [float(x) for x in re.findall(r"^Overfull \\[hv]box \((\d+(?:\.\d+)?)pt too", text, re.M)]
    return {
        "errors": list(dict.fromkeys(errors)),
        "undefined_refs": sorted(set(re.findall(r"Reference `([^']+)' on page", text))),
        "undefined_cites": sorted(set(re.findall(r"Citation [`']([^']+)'", text))),
        "overfull_over_1pt": sum(1 for x in overfull if x > 1.0),
        "worst_overfull_pt": max(overfull, default=0.0),
        "missing_glyphs": sorted(set(re.findall(r"Missing character: There is no (\S+)", text))),
        "needs_rerun": bool(RERUN.search(text)),
    }


def run(cmd, cwd, timeout, env=None):
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                              errors="replace", timeout=timeout, env=env)
        if proc.returncode != 0:
            # TeX's log omits driver and bibliography failures; retain their output too.
            transcript = "\n".join(part for part in (proc.stdout, proc.stderr) if part)
            print("command failed (exit %s): %s" % (proc.returncode, " ".join(cmd)))
            print("\n".join(transcript.splitlines()[-40:]))
        return proc.returncode
    except subprocess.TimeoutExpired:
        print("timeout after %ss: %s" % (timeout, " ".join(cmd)))
        return 124
    except OSError as exc:
        print("cannot run %s: %s" % (cmd[0], exc))
        return 127


def latexmk_usable():
    exe = shutil.which("latexmk")
    if not exe:
        return None
    try:
        ok = subprocess.run([exe, "-norc", "-v"], capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        ok = False
    return exe if ok else None  # under MiKTeX latexmk fails without Perl


def _signature(path):
    """Metadata changes distinguish a new output from an existing artifact."""
    try:
        value = path.stat()
        return value.st_mtime_ns, value.st_ctime_ns, value.st_size
    except OSError:
        return None


def _digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_environment(cwd):
    # Retain kpathsea's default search via the final empty path component.
    env = os.environ.copy()
    for name in ("BIBINPUTS", "BSTINPUTS"):
        env[name] = str(cwd) + "//" + os.pathsep + env.get(name, "")
    return env


def _fallback(tex, engine, cwd, out, flags, timeout, initial):
    exe = shutil.which(engine)
    if not exe:
        print("%s not found; run scripts/check_env.py" % engine)
        return 127
    artifact = lambda extension: out / (tex.stem + extension)
    cmd = [exe] + flags + ["-output-directory=" + str(out), tex.name]
    env = _source_environment(cwd)
    processed = {}
    # One initial pass and at most four further passes. Backend work always
    # requires another TeX pass; its exit status is never replaced by TeX's.
    for _ in range(5):
        code = run(cmd, cwd, timeout)
        if code != 0:
            return code
        bcf, aux, idx = (artifact(ext) for ext in (".bcf", ".aux", ".idx"))
        jobs = []
        if bcf.is_file() and _signature(bcf) != initial[".bcf"]:
            jobs.append(("biber", bcf, ".bbl"))
        elif aux.is_file() and _signature(aux) != initial[".aux"] and "\\bibdata" in _read(aux):
            jobs.append(("bibtex", aux, ".bbl"))
        if idx.is_file() and _signature(idx) != initial[".idx"] and "\\indexentry" in _read(idx):
            jobs.append(("makeindex", idx, ".ind"))
        backend_ran = False
        for tool, control, extension in jobs:
            digest = _digest(control)
            if processed.get(tool) == digest:
                continue
            backend = shutil.which(tool)
            if not backend:
                print("required backend not found: %s (%s)" % (tool, control))
                return 127
            output = artifact(extension)
            before = _signature(output)
            if tool == "biber":
                # Without --input-directory, Biber searches the output directory
                # for its BCF and then the source cwd for relative data files.
                command = [backend, "--output-directory", str(out), tex.stem]
                backend_cwd = cwd
            elif tool == "bibtex":
                command, backend_cwd = [backend, tex.stem], out
            else:
                command = [backend, "-o", output.name, control.name]
                backend_cwd = out  # makeindex rejects absolute output under openout_any=p
            code = run(command, backend_cwd, timeout, env=env)
            if code != 0:
                return code
            if _signature(output) is None or _signature(output) == before:
                print("%s did not produce a fresh %s" % (tool, output.name))
                return 1
            processed[tool] = digest
            backend_ran = True
        if not backend_ran and not RERUN.search(_read(artifact(".log"))):
            return 0
    print("build did not stabilize after five TeX passes")
    return 1


def build(tex, engine, outdir, shell_escape, timeout, use_latexmk=True,
          trust_project_config=False):
    tex = Path(tex).resolve()
    cwd = tex.parent
    out = Path(outdir).resolve() if outdir else cwd
    out.mkdir(parents=True, exist_ok=True)
    log, pdf = (out / (tex.stem + ext) for ext in (".log", ".pdf"))
    before_pdf = _signature(pdf)
    initial = {ext: _signature(out / (tex.stem + ext))
               for ext in (".bcf", ".aux", ".idx")}
    flags = ["-interaction=nonstopmode", "-halt-on-error", "-file-line-error"]
    flags.append("-shell-escape" if shell_escape else "-no-shell-escape")
    latexmk = latexmk_usable() if use_latexmk else None
    if latexmk:
        # -g forces a new engine run even if a cached PDF looks up to date.
        command = [latexmk] + ([] if trust_project_config else ["-norc"])
        command += ["-g", ENGINES[engine], "-outdir=" + str(out)] + flags + [tex.name]
        code = run(command, cwd, timeout)
    else:
        code = _fallback(tex, engine, cwd, out, flags, timeout, initial)
    if code == 0 and RERUN.search(_read(log)):
        print("build still requests another TeX or bibliography pass")
        code = 1
    if code == 0 and (_signature(pdf) is None or _signature(pdf) == before_pdf):
        print("no fresh PDF produced; an existing PDF is not proof of this build")
        code = 1
    return code, log


def _read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tex", help="main .tex file")
    ap.add_argument("--engine", choices=sorted(ENGINES), help="default: magic comment, else lualatex")
    ap.add_argument("--outdir", help="output directory (default: next to the .tex)")
    ap.add_argument("--shell-escape", action="store_true", help="allow the document to run programs")
    ap.add_argument("--timeout", type=int, default=300, help="seconds per run (default 300)")
    ap.add_argument("--no-latexmk", action="store_true", help="run the engine directly")
    ap.add_argument("--trust-project-config", action="store_true",
                    help="allow reviewed latexmk rc files to execute Perl; independent of shell escape")
    args = ap.parse_args(argv)
    if args.timeout <= 0:
        ap.error("--timeout must be positive")

    tex = Path(args.tex)
    if not tex.is_file():
        print("not found: %s" % tex)
        return 2
    engine = args.engine or choose_engine(_read(tex))
    try:
        code, log = build(tex, engine, args.outdir, args.shell_escape, args.timeout,
                          not args.no_latexmk, args.trust_project_config)
    except OSError as exc:
        print("cannot prepare build: %s" % exc)
        return 1
    if log is None:
        return code
    report = parse_log(_read(log))
    pdf = log.with_suffix(".pdf")
    warnings = any(report[key] for key in ("undefined_refs", "undefined_cites", "missing_glyphs", "overfull_over_1pt"))
    result = "COMPILED WITH WARNINGS" if warnings else "COMPILED"
    if code != 0 or not pdf.exists():
        result = "FAILED (exit %s)" % code
    print("engine: %s | result: %s" % (engine, result))
    print("visual inspection: not performed by this script")
    if pdf.exists():
        print("pdf: %s" % pdf)
    print("log: %s" % log)
    for e in report["errors"][:10]:
        print("error: " + e)
    if report["undefined_refs"]:
        print("undefined references: " + ", ".join(report["undefined_refs"]))
    if report["undefined_cites"]:
        print("undefined citations: " + ", ".join(report["undefined_cites"]))
    if report["missing_glyphs"]:
        print("missing glyphs (font lacks them): " + " ".join(report["missing_glyphs"]))
    if report["overfull_over_1pt"]:
        print("overfull boxes > 1pt: %d (worst %.1fpt)" % (report["overfull_over_1pt"], report["worst_overfull_pt"]))
    if shutil.which("texlogsieve") and (code != 0 or report["errors"]):
        print("for the full filtered log: texlogsieve %s" % log)
    return 0 if code == 0 and pdf.exists() else 1


if __name__ == "__main__":
    sys.exit(main())
