#!/usr/bin/env python3
"""Render PDF pages to PNG so the agent can look at the result.

Tries pdftoppm (poppler), then mutool (MuPDF), then Ghostscript (gs, gswin64c, or
rungs from TeX Live). With none of them it exits 1: read the PDF directly instead.
Python 3.8+, standard library only; Windows, macOS and Linux.
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_pages(spec):
    """'1,3-4' -> [1, 3, 4]."""
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            if int(a) > int(b):
                raise ValueError("page ranges must be ascending")
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
    ap.add_argument("--timeout", type=int, default=60, help="seconds per page (default 60)")
    args = ap.parse_args(argv)
    if args.timeout <= 0 or args.dpi <= 0:
        ap.error("--timeout and --dpi must be positive")
    try:
        pages = parse_pages(args.pages)
    except ValueError as exc:
        ap.error(str(exc))

    pdf = Path(args.pdf).resolve()
    if not pdf.is_file():
        print("not found: %s" % pdf)
        return 2
    renderer, exe = find_renderer()
    if not renderer:
        print("no PDF renderer (pdftoppm, mutool or Ghostscript) found; read the PDF directly")
        return 1
    outdir = Path(args.outdir).resolve() if args.outdir else pdf.parent
    outdir.mkdir(parents=True, exist_ok=True)
    failed = 0
    for page in pages:
        png = outdir / ("%s-p%d.png" % (pdf.stem, page))
        # Render in a private staging directory. A successful return without a
        # new image cannot accidentally approve last run's PNG.
        with tempfile.TemporaryDirectory(prefix=".latex-ops-preview-", dir=str(outdir)) as directory:
            staged = Path(directory) / png.name
            try:
                proc = subprocess.run(commands(renderer, exe, pdf, page, args.dpi, staged),
                                      capture_output=True, text=True, errors="replace",
                                      timeout=args.timeout)
                if proc.returncode == 0 and staged.is_file():
                    staged.replace(png)
                    print(png)
                    continue
                detail = (proc.stderr or proc.stdout or "no fresh PNG produced").strip()[:200]
            except subprocess.TimeoutExpired:
                detail = "timeout after %ss" % args.timeout
            except OSError as exc:
                detail = str(exc)
            failed += 1
            print("page %d failed (%s): %s" % (page, renderer, detail))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
