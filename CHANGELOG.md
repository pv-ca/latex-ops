# Changelog

## 0.1.1 — 2026-10-15

- Add public plugin and marketplace manifests for Claude Code and Codex, using the same skill directory as the standalone installation.
- Expand the English and Brazilian Portuguese READMEs with installation by agent, first use, updates, compatibility, troubleshooting and repository structure.
- Focus the examples and public documentation on academic use, with a problem set and research proposal.
- Fix assessment table placeholders and use amsthm directly in lecture notes to avoid the thmtools sibling-counter conflict with the June 2026 LaTeX kernel.
- Declare makeindex for the ABNT template and install a PDF renderer in Linux CI.
- Fail the gallery check when rendering fails or an expected image is missing; include driver output when compilation fails.
- Add regression checks for gallery failures and consistent plugin metadata and skill paths.

## 0.1.0 — 2026-10-15

- Design system: 33 functional templates (academic, teaching, professional, legal, editorial, technical) and 9 visual presets, each a compilable `.tex` reference.
- Academic templates: Research Article, Conference Paper, Lecture Notes, Problem Set, Lab Report, Literature Review, Research Proposal, Statistical Report, ABNT academic work (abnTeX2), Response to Reviewers.
- References for mathematics, statistics and integrations (Python, R, Julia, Quarto, Pandoc, TikZ, Overleaf).
- Four filled examples in `examples/` with rendered pages in `docs/showcase/`.
- `SKILL.md` workflow: classify the request, choose template and preset, compile, render and inspect pages, fix, reduce.
- Rules for academic papers and theses (venue kits, citations, figures, page limits, anonymity) and for Beamer slides.
- Build repair procedure: root document, first real error, minimal change, evidence report.
- Scripts (Python 3.8+, standard library, Windows/macOS/Linux): `check_env.py` (toolchain report and package installation on request), `build.py` (compile and summarize the log), `preview.py` (PDF pages to PNG).
- CI compiles every template and example on Linux and Windows with only the declared packages.
