#!/usr/bin/env python3
"""Compile a LaTeX document and print a short report of errors and warnings.

Uses latexmk when it runs; otherwise runs the engine, biber or bibtex, and reruns
until references settle. Shell escape stays off unless --shell-escape is given.
Python 3.8+, standard library only; Windows, macOS and Linux.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ENGINES = {"lualatex": "-lualatex", "xelatex": "-xelatex", "pdflatex": "-pdf"}
RERUN = re.compile(r"Rerun to get|Label\(s\) may have changed|Please rerun|Please \(re\)run Biber")


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
        "undefined_cites": sorted(set(re.findall(r"Citation `([^']+)'", text))),
        "overfull_over_1pt": sum(1 for x in overfull if x > 1.0),
        "worst_overfull_pt": max(overfull, default=0.0),
        "missing_glyphs": sorted(set(re.findall(r"Missing character: There is no (\S+)", text))),
        "needs_rerun": bool(RERUN.search(text)),
    }


def run(cmd, cwd, timeout):
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                              errors="replace", timeout=timeout)
        return proc.returncode
    except subprocess.TimeoutExpired:
        print("timeout after %ss: %s" % (timeout, " ".join(cmd)))
        return 124


def latexmk_usable():
    exe = shutil.which("latexmk")
    if not exe:
        return None
    try:
        ok = subprocess.run([exe, "-v"], capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        ok = False
    return exe if ok else None  # under MiKTeX latexmk fails without Perl


def build(tex, engine, outdir, shell_escape, timeout, use_latexmk=True):
    tex = Path(tex).resolve()
    cwd = tex.parent
    out = Path(outdir).resolve() if outdir else cwd
    out.mkdir(parents=True, exist_ok=True)
    flags = ["-interaction=nonstopmode", "-halt-on-error", "-file-line-error"]
    flags.append("-shell-escape" if shell_escape else "-no-shell-escape")

    latexmk = latexmk_usable() if use_latexmk else None
    if latexmk:
        code = run([latexmk, ENGINES[engine], "-outdir=" + str(out)] + flags + [tex.name], cwd, timeout)
    else:
        exe = shutil.which(engine)
        if not exe:
            print("%s not found; run scripts/check_env.py" % engine)
            return 127, None
        cmd = [exe] + flags + ["-output-directory=" + str(out), tex.name]
        code = run(cmd, cwd, timeout)
        stem = out / tex.stem
        if code == 0 and stem.with_suffix(".bcf").exists() and shutil.which("biber"):
            run([shutil.which("biber"), "--input-directory", str(out), tex.stem], out, timeout)
        elif code == 0 and "\\bibdata" in _read(stem.with_suffix(".aux")) and shutil.which("bibtex"):
            run([shutil.which("bibtex"), tex.stem], out, timeout)
        for _ in range(4):
            if code != 0:
                break
            code = run(cmd, cwd, timeout)
            if not RERUN.search(_read(stem.with_suffix(".log"))):
                break
    return code, out / (tex.stem + ".log")


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
    args = ap.parse_args(argv)

    tex = Path(args.tex)
    if not tex.is_file():
        print("not found: %s" % tex)
        return 2
    engine = args.engine or choose_engine(_read(tex))
    code, log = build(tex, engine, args.outdir, args.shell_escape, args.timeout, not args.no_latexmk)
    if log is None:
        return code
    report = parse_log(_read(log))
    pdf = log.with_suffix(".pdf")
    print("engine: %s | result: %s" % (engine, "OK" if code == 0 and pdf.exists() else "FAILED (exit %s)" % code))
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
