#!/usr/bin/env python3
"""Render PDF pages to PNG so the agent can look at the result.

Tries pdftoppm (poppler), then mutool (MuPDF), then Ghostscript (gs, gswin64c, or
rungs from TeX Live). With none of them it exits 3: read the PDF directly instead.
Python 3.8+, standard library only; Windows, macOS and Linux.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def parse_pages(spec):
    """'1,3-4' -> [1, 3, 4]."""
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a), int(b) + 1))
        elif part:
            pages.append(int(part))
    if not pages or min(pages) < 1:
        raise ValueError("pages start at 1: %r" % spec)
    return sorted(set(pages))


def commands(renderer, exe, pdf, page, dpi, png):
    if renderer == "pdftoppm":
        return [exe, "-f", str(page), "-l", str(page), "-r", str(dpi), "-png", "-singlefile",
                str(pdf), str(png.with_suffix(""))]
    if renderer == "mutool":
        return [exe, "draw", "-r", str(dpi), "-o", str(png), str(pdf), str(page)]
    return [exe, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r%d" % dpi,
            "-dFirstPage=%d" % page, "-dLastPage=%d" % page, "-sOutputFile=%s" % png, str(pdf)]


def find_renderer():
    for name in ("pdftoppm", "mutool", "gswin64c", "gs", "rungs"):
        exe = shutil.which(name)
        if exe:
            return ("ghostscript" if name in ("gswin64c", "gs", "rungs") else name), exe
    return None, None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf")
    ap.add_argument("--pages", default="1", help="e.g. 1,3-4 (default 1)")
    ap.add_argument("--dpi", type=int, default=80, help="default 80; use 150 for detail")
    ap.add_argument("--outdir", help="default: next to the PDF")
    args = ap.parse_args(argv)

    pdf = Path(args.pdf).resolve()
    if not pdf.is_file():
        print("not found: %s" % pdf)
        return 2
    renderer, exe = find_renderer()
    if not renderer:
        print("no PDF renderer (pdftoppm, mutool or Ghostscript) found; read the PDF directly")
        return 3
    outdir = Path(args.outdir).resolve() if args.outdir else pdf.parent
    outdir.mkdir(parents=True, exist_ok=True)
    failed = 0
    for page in parse_pages(args.pages):
        png = outdir / ("%s-p%d.png" % (pdf.stem, page))
        proc = subprocess.run(commands(renderer, exe, pdf, page, args.dpi, png),
                              capture_output=True, text=True, errors="replace")
        if proc.returncode == 0 and png.exists():
            print(png)
        else:
            failed += 1
            print("page %d failed (%s): %s" % (page, renderer, (proc.stderr or proc.stdout).strip()[:200]))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
