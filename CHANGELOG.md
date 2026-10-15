# Changelog

## 0.1.0 — unreleased

- Design system: 31 functional templates (academic, teaching, professional, legal, editorial, technical) and 9 visual presets, each a compilable `.tex` reference.
- Academic templates: Research Article, Conference Paper, Lecture Notes, Problem Set, Lab Report, Literature Review, Research Proposal, Statistical Report, ABNT academic work (abnTeX2), Response to Reviewers.
- References for mathematics, statistics and integrations (Python, R, Julia, Quarto, Pandoc, TikZ, Overleaf).
- Four filled examples in `examples/` with rendered pages in `docs/showcase/`.
- `SKILL.md` workflow: classify the request, choose template and preset, compile, render and inspect pages, fix, reduce.
- Rules for academic papers and theses (venue kits, citations, figures, page limits, anonymity) and for Beamer slides.
- Build repair procedure: root document, first real error, minimal change, evidence report.
- Scripts (Python 3.8+, standard library, Windows/macOS/Linux): `check_env.py` (toolchain report and package installation on request), `build.py` (compile and summarize the log), `preview.py` (PDF pages to PNG).
- CI compiles every template and example on Linux and Windows with only the declared packages.
