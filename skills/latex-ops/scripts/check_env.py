#!/usr/bin/env python3
"""Report the TeX toolchain on this machine and what the latex-ops templates still need.

Reads only. With --install it prints the command that would install the missing
packages; with --install --yes it runs that command (ask the user first).
Python 3.8+, standard library only; Windows, macOS and Linux.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REQUIREMENTS = Path(__file__).resolve().parent.parent / "assets" / "requirements.txt"
TOOLS = ["lualatex", "xelatex", "pdflatex", "latexmk", "perl", "biber", "bibtex",
         "texlogsieve", "kpsewhich", "tlmgr", "miktex", "pdftoppm", "mutool",
         "gs", "gswin64c", "rungs"]
TINYTEX = {
    "Windows": "Download and run https://yihui.org/tinytex/install-bin-windows.bat (no admin needed)",
    "Darwin": 'curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh',
    "Linux": 'wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh',
}


def read_requirements(path=REQUIREMENTS):
    """Return [(package, probe)] from requirements.txt, skipping comments."""
    reqs = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            name, probe = line.split()
            reqs.append((name, probe))
    return reqs


def run(cmd, timeout=60):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return out.returncode, (out.stdout or "") + (out.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)


def detect_distribution(tools):
    """Return (kind, version line). kind: texlive, tinytex, texlive-system, miktex or none."""
    engine = tools.get("lualatex") or tools.get("pdflatex") or tools.get("xelatex")
    if not engine:
        return "none", ""
    _, out = run([engine, "--version"])
    first = out.strip().splitlines()[0] if out.strip() else ""
    if "MiKTeX" in out:
        return "miktex", first
    if "tinytex" in engine.lower():
        return "tinytex", first
    # TeX Live packaged by a Linux distribution: tlmgr is absent or disabled there.
    if platform.system() == "Linux" and engine.startswith("/usr/"):
        return "texlive-system", first
    return "texlive", first


def latexmk_works(tools):
    """latexmk is a Perl script; under MiKTeX it fails without a Perl installation."""
    if not tools.get("latexmk"):
        return False
    code, _ = run([tools["latexmk"], "-norc", "-v"])
    return code == 0


def missing_packages(reqs, tools):
    kpsewhich = tools.get("kpsewhich")
    missing = []
    for name, probe in reqs:
        if probe.startswith("bin:"):
            if not shutil.which(probe[4:]):
                missing.append(name)
        elif not kpsewhich or run([kpsewhich, probe])[0] != 0:
            missing.append(name)
    return missing


def linux_family():
    try:
        text = Path("/etc/os-release").read_text()
    except OSError:
        return ""
    ids = ""
    for line in text.splitlines():
        if line.startswith(("ID=", "ID_LIKE=")):
            ids += " " + line.split("=", 1)[1].strip('"')
    for family in ("fedora", "rhel", "debian", "ubuntu", "arch", "suse"):
        if family in ids.split():
            return family
    return ""


def install_plan(kind, missing, reqs):
    """Return (command list or None, advice text)."""
    if kind == "none":
        names = " ".join(n for n, _ in reqs)
        return None, ("No TeX distribution found. Install TinyTeX:\n  "
                      + TINYTEX.get(platform.system(), TINYTEX["Linux"])
                      + "\nthen run: tlmgr install " + names)
    if not missing:
        return None, "Nothing to install."
    if kind in ("texlive", "tinytex"):
        return ["tlmgr", "install"] + missing, ""
    if kind == "miktex":
        advice = "" if shutil.which("perl") else "latexmk also needs Perl on MiKTeX: install Strawberry Perl."
        return ["miktex", "packages", "install"] + missing, advice
    # texlive-system: the distribution owns TeX; print, never run, the system command.
    family = linux_family()
    probes = dict(reqs)
    if family in ("fedora", "rhel"):
        cmd = "sudo dnf install " + " ".join(
            "'tex(%s)'" % probes[m] if not probes[m].startswith("bin:") else "texlive-" + m
            for m in missing)
    elif family in ("debian", "ubuntu"):
        cmd = ("sudo apt install latexmk texlive-luatex texlive-latex-extra "
               "texlive-fonts-extra texlive-pictures texlive-science texlive-extra-utils")
    elif family == "arch":
        cmd = "sudo pacman -S texlive-luatex texlive-latexextra texlive-fontsextra texlive-pictures texlive-science"
    elif family == "suse":
        cmd = "sudo zypper install " + " ".join("texlive-" + m for m in missing)
    else:
        cmd = "install these TeX Live packages with your package manager: " + " ".join(missing)
    return None, "TeX Live is managed by your Linux distribution; run:\n  " + cmd


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="print a JSON report")
    ap.add_argument("--install", action="store_true", help="show the install command for missing packages")
    ap.add_argument("--yes", action="store_true", help="with --install, run the command")
    ap.add_argument("--list-packages", action="store_true", help="print the required package names and exit")
    args = ap.parse_args(argv)

    reqs = read_requirements()
    if args.list_packages:
        print(" ".join(n for n, _ in reqs))
        return 0

    tools = {t: shutil.which(t) for t in TOOLS}
    kind, version = detect_distribution(tools)
    missing = missing_packages(reqs, tools) if kind != "none" else [n for n, _ in reqs]
    renderer = next((t for t in ("pdftoppm", "mutool", "gswin64c", "gs", "rungs") if tools.get(t)), None)
    report = {
        "os": platform.system(),
        "distribution": kind,
        "version": version,
        "tools": {t: bool(p) for t, p in tools.items()},
        "latexmk_works": latexmk_works(tools),
        "renderer": renderer,
        "missing_packages": missing,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("OS: %s | TeX: %s %s" % (report["os"], kind, version))
        print("engines: " + (", ".join(t for t in ("lualatex", "xelatex", "pdflatex") if tools[t]) or "none"))
        print("latexmk: " + ("works" if report["latexmk_works"] else
                             "missing or not runnable (build.py falls back to running the engine)"))
        print("page renderer: " + (renderer or "none (read the PDF directly to inspect pages)"))
        print("missing packages: " + (", ".join(missing) if missing else "none"))

    if args.install:
        cmd, advice = install_plan(kind, missing, reqs)
        if advice:
            print(advice)
        if cmd:
            print("install command: " + " ".join(cmd))
            if args.yes:
                # Full path, so Windows can start tlmgr.bat / miktex.exe without a shell.
                return subprocess.run([shutil.which(cmd[0]) or cmd[0]] + cmd[1:]).returncode
            print("Re-run with --install --yes to execute it.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
