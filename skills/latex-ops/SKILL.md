---
name: latex-ops
description: Write, format, fix and compile academic and professional LaTeX that looks professionally typeset, then inspect the PDF and report page coverage. Use for research articles, conference papers, theses and dissertations (including Brazilian ABNT work with abnTeX2), literature reviews, research proposals, lab and statistical reports, lecture notes, problem sets, posters, Beamer talks and responses to reviewers; for mathematical and statistical writing (equations, proofs, algorithms, regression tables, data plots); and for formatting a paper to a journal, conference or university template. Also covers professional documents from its templates (CV, letter, report, memo, proposal, invoice, contract, minutes, manual, SOP, form), turning notes, Markdown or Word drafts into a designed PDF, fixing LaTeX that does not compile, setting up TeX on Windows, macOS or Linux, and accessible PDF. Use it whenever .tex, LaTeX, Beamer, TikZ or pgfplots is involved, even if the user never says "LaTeX".
license: MIT
compatibility: Needs a TeX distribution with LuaLaTeX (TeX Live or TinyTeX recommended; MiKTeX works) and Python 3.8+ for the helper scripts. Works on Windows, macOS and Linux.
metadata:
  version: "0.1.2"
---

# latex-ops

Make LaTeX documents that read as published, not exported: faithful to the supplied content, technically sound, and designed for the reader. Design comes from typography, proportion, hierarchy, spacing and consistency, informed by Dieter Rams' restraint and contemporary editorial practice, not from ornament.

## Priorities

When requirements conflict, resolve them in this order:

1. Explicit user requirements and mandatory institutional, journal, publisher, accessibility or venue rules.
2. Factual accuracy and preservation of the supplied meaning.
3. Compilation correctness and dependency compatibility.
4. Reader comprehension, navigation and accessibility.
5. Maintainable, semantic source.
6. Editorial and visual refinement.
7. Novelty.

## Match the action to the request

- **Question or troubleshooting:** answer directly; a minimal example only when it helps. Do not turn a LaTeX question into a document project.
- **Critique or diagnosis:** read the material first; separate technical defects, reader-experience defects, maintainability problems and optional refinements. Do not rewrite unless asked.
- **Fix:** follow "Fixing a build" below; smallest change that works, no unrelated refactors.
- **Revision or redesign:** read the existing source before claiming anything; keep sound and mandatory decisions; change what was asked or what coherence requires.
- **New document:** choose a functional template and a visual preset (below) and produce a complete document.
- **Conversion:** decide which kind is wanted. *Faithful* keeps structure and wording. *Editorial* (the default for instructional, professional and long-form material) keeps content and meaning but improves hierarchy, tables, exercises, spacing and page behaviour. *Redesign* reconsiders the architecture. Never change answer keys, results, quotations or factual claims to improve the design.
- **Code only:** return only the LaTeX; put indispensable dependency notes in comments.
- **Slides:** Beamer only when slides are requested.

Ask a question only when a missing fact would make the result wrong or change its architecture; otherwise choose sensibly and say what you chose. Ask before anything destructive, costly, externally visible, or that installs software.

## Ground everything in what was supplied

The user's text, files, data, citations, images, templates and institutional rules are the evidence. Do not invent facts, numbers, scores, proficiency levels, quotations, citations, bibliography entries, authors, dates, prices, legal terms, image files, fonts, venue rules, or compilation and validation results. Keep three records distinct: source comments for working notes (invisible in the PDF), visible draft markers where content is missing, and a pending-content list in the delivery report. For example:

```latex
% Working note: request the author affiliation.
\textbf{[CONTENT: author affiliation not supplied]}
```

Escape LaTeX special characters in marker text. A draft with visible markers is a legitimate deliverable when labelled as a draft; do not call it submission-ready. Never remove a marker by inventing the missing information.

Illustrative content only when asked for, and visibly marked as such. Deterministic calculation outranks prose for totals and statistics. For version-sensitive package, compiler, accessibility or venue behaviour, check current official documentation when you can, and say so when you could not.

## Design: two coordinates

Every designed document has a **functional template** (what the reader must do with it and how information is organized) and a **visual preset** (how it looks). Function outranks style; mandatory venue or institutional rules outrank both.

1. Read `references/functional-templates.md` and pick the template.
2. Read `references/visual-presets.md` and pick the preset.
3. Open only the matching files in `assets/templates/functional/` and `assets/templates/presets/` (a second preset only for a requested hybrid).
4. Adapt them to the real content, medium, fonts, venue and toolchain. They are design evidence, not boilerplate: copy into the user's document, never edit the bundled files.

Templates. Academic: Research Article, Conference Paper, Classic Thesis, Technical Thesis, ABNT Academic Work (Brazil), Literature Review, Research Proposal, Lab Report, Statistical Report, Response to Reviewers, Poster (scientific or editorial). Teaching: Lecture Notes, Problem Set, Course Plan, Assessment Report, Book/Guide. Professional: Professional CV, Formal Letter, Executive Brief, Professional Memo, Proposal, Invoice & Quote, Contract/Legal, Meeting Minutes/Agenda, Technical Manual, SOP/Procedure, One-Page Reference, Form, Magazine Editorial, Brochure/Flyer, Portfolio/Case Study.

Presets: Swiss Minimal, Tufte Editorial, Kao Textbook, Classic Editorial, Minimal Research, Modern Report, Minimal Beamer, Magazine Editorial, Legal Minimal.

Usual pairs: paper without venue rules → Research Article + Minimal Research; paper for a named venue → the venue's official kit; thesis → Technical or Classic Thesis, or ABNT Academic Work in Brazil; course notes → Lecture Notes + Kao Textbook; homework or exam → Problem Set; data analysis → Statistical Report + Modern Report; student report → Assessment Report + Modern Report; CV or letter → Swiss Minimal; proposal → Proposal + Modern Report; contract → Contract/Legal + Legal Minimal; newsletter → Magazine Editorial; manual, SOP, reference card or form → matching template + Swiss Minimal; talk → Minimal Beamer. Choose without asking when one option is clearly better.

Before writing a preamble or styling components, read the relevant section of `references/design-rules.md` (typography and layout, classes and packages, components, accessibility, source architecture). For a paper, thesis, or formatting for a journal, conference or university, read its *Academic papers and theses* section first: the venue's official kit overrides every preset. For slides, read *Presentations*.

For mathematics (equations, theorems, notation, matrices, algorithms, plots, units) read `references/math.md`; for data analysis, statistical reporting and data plots read `references/statistics.md`; when content comes from Python, R, Julia, Quarto, Pandoc or Overleaf, or for TikZ diagram systems, read `references/integrations.md`.

## Tools

Scripts live in `scripts/` next to this file; run them with `python3` (`python` or `py` on Windows). They use only the standard library.

| Script | Use |
| --- | --- |
| `check_env.py` | First LaTeX task on a machine, or when a build fails for a reason outside the document. Reports distribution, engines, latexmk, renderer and missing packages. `--install` shows the install command; `--install --yes` runs it, only after the user agrees |
| `build.py FILE.tex` | Compile (latexmk when it works, else the engine plus Biber/BibTeX and makeindex when required, until references settle). Backend failures, missing required backends and exhausted reruns fail the build. Shell escape and latexmk rc loading are off by default. Prints errors with file and line, undefined references and citations, missing glyphs, overfull boxes |
| `preview.py FILE.pdf --pages 1,3-4` | Render pages to PNG to look at them; `--timeout 60` limits each page. Rendering failures name the tool. If no renderer is available, inspect the PDF directly when possible and report the limitation |

`build.py --trust-project-config` enables latexmk's normal rc search, including system, user and project files. These files execute Perl independently of `--shell-escape`; review the applicable configuration and use the option only within the task's authorization. Diagnostic probes always use `-norc`, even for trusted builds. `--shell-escape` separately lets the TeX document run programs: enable it only for reviewed features authorized by the user. Neither switch provides a sandbox.

A successful build must produce a fresh PDF; a failed build may leave an earlier PDF in place. Previews are staged and promoted only after a new image is produced; image existence never proves visual inspection. These existing build/preview commands intentionally update their outputs on success.

If the tools are unavailable (no shell, no TeX), do static review and say plainly that nothing was compiled. Read `references/platforms.md` for Windows, MiKTeX, Linux-packaged TeX Live, Overleaf and font problems, and `references/technical.md` for engines, specialized classes and tagged PDF.

## Workflow for substantial work

1. **Inspect:** read the sources, assets and constraints together.
2. **Specify:** reader, template, preset, medium and page size, engine, fonts, the recurring components; only the criteria the task needs.
3. **Implement:** the complete result with the smallest coherent set of classes, packages and macros. One self-contained `.tex` unless a multi-file project helps or was requested.
4. **Compile:** `build.py`.
5. **Look:** read the report, then render and inspect all pages of short documents. For long documents, choose a sample covering chapter transitions, dense tables, equations, figures, bibliography and final pages. Record the exact pages inspected, the total page count and the remaining coverage. Check hierarchy, stranded headings, near-empty pages, floats, cramped or overflowing tables, clipped text and missing glyphs. Sampling does not establish whole-document inspection.
6. **Correct** what matters and rebuild when the change can affect the output.
7. **Reduce:** remove packages, decoration and macros that no longer solve a real problem.

Never claim compilation, rendering, visual inspection, or PDF/UA, PDF/A or WCAG conformance unless that check actually ran.

## Fixing a build

1. Find the root document (build configuration, `latexmkrc`, magic comments, the file with `\documentclass`); do not assume `main.tex`. Read any build configuration before executing it. Reproduce with `build.py` by default; use the project's own command or trusted rc route only when its code execution is reviewed and authorized, and keep the original error text.
2. Fix the first real error: later ones are usually consequences. Common causes: wrong engine (`fontspec` or `unicode-math` under pdfLaTeX), package or font not installed (`check_env.py`), unbalanced environment or brace, undefined command, Unicode character the font lacks, a file path that does not exist, the wrong bibliography step (check biblatex's `backend=` before running biber; projects with `\bibliography{}` use BibTeX).
3. Change as little as possible. Do not alter equation meaning, table cells, citation and label keys, bibliography records, file paths, comments or verbatim/code blocks, and never edit official `.cls`, `.sty` or `.bst` files. Never make an error disappear by deleting or commenting out content.
4. Rebuild until stable; exhausting the repeat limit is a build failure. Keep build failures separate from documentary warnings: undefined references or citations need correction before submission; overfull boxes need contextual review. A draft may retain explicit pending content without being called finished.
5. Report the files changed and why, the command and engine used, the result, where the log and PDF are, the exact pages inspected and any uninspected coverage, and the pending content and decisions for the author.

## Output

- New document or full redesign: a 2–3 sentence design brief (reader, template, preset, medium, structural logic), the LaTeX file, and at most five design decisions, dependencies or places to edit.
- Revision: a short evidence-based diagnosis, the complete revised file (or a patch if asked), at most five material changes.
- Always state what was compiled, rendered and inspected separately, with page coverage and pending content. Label draft deliveries explicitly.

## Final check

Before returning substantial work, confirm once: the request was classified correctly; supplied content survived; mandatory constraints beat aesthetics; template and preset fit the reading task; typography, spacing and components form one system; every package earns its place; missing information is marked, not invented; validation claims match what ran; the output matches the requested mode.
