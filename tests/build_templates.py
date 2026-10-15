#!/usr/bin/env python3
"""Compile every bundled template and example; optionally render page 1 of each into a gallery folder.

Usage: python3 tests/build_templates.py [--gallery docs/gallery] [--workdir DIR]
Exit code 1 if any template fails.
"""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "latex-ops"
sys.path.insert(0, str(SKILL / "scripts"))
import build  # noqa: E402
import preview  # noqa: E402


def templates():
    return sorted((SKILL / "assets" / "templates").glob("*/*.tex")) + sorted((ROOT / "examples").glob("*.tex"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gallery", help="write <kind>-<name>.png here")
    ap.add_argument("--workdir", help="keep build files here (default: a temporary folder)")
    args = ap.parse_args(argv)
    work = Path(args.workdir or tempfile.mkdtemp(prefix="latex-ops-"))
    failures = []
    for tex in templates():
        kind = tex.parent.name
        dest = work / kind
        dest.mkdir(parents=True, exist_ok=True)
        copy = dest / tex.name
        shutil.copy(tex, copy)
        engine = build.choose_engine(copy.read_text(encoding="utf-8"))
        code, log = build.build(copy, engine, None, False, 600)
        pdf = copy.with_suffix(".pdf")
        ok = code == 0 and pdf.exists()
        print("%-4s %s/%s" % ("OK" if ok else "FAIL", kind, tex.name))
        if not ok:
            report = build.parse_log(build._read(log)) if log else {"errors": []}
            failures.append(tex.name)
            for e in report["errors"][:3]:
                print("     " + e)
        elif args.gallery:
            out = Path(args.gallery)
            out.mkdir(parents=True, exist_ok=True)
            preview.main([str(pdf), "--pages", "1", "--dpi", "60", "--outdir", str(out)])
            png = out / (pdf.stem + "-p1.png")
            if png.exists():
                png.replace(out / ("%s-%s.png" % (kind, pdf.stem)))
    print("%d documents, %d failed" % (len(templates()), len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
