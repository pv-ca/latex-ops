# Integrations: Python, R, Julia, Quarto, Pandoc, TikZ, Overleaf

Read when the document's content comes from another tool or must live inside another workflow.

## Principle

The analysis tool computes; LaTeX typesets. Generated tables and figures are files the document includes and a script regenerates, so a change in the data never requires editing the `.tex` by hand.

```text
project/
├── main.tex
├── tables/   model.tex, descriptives.tex   (generated)
├── figures/  fig1.pdf                      (generated)
├── data/     raw.csv
└── analysis/ make_outputs.py or .R         (regenerates tables/ and figures/)
```

## Python

- Tables: `df.style.format(precision=2).hide(axis="index").to_latex("tables/desc.tex", hrules=True, siunitx=True)` (pandas Styler; needs `booktabs` and `siunitx` in the preamble). Regression tables: `pyfixest`'s `etable`, `stargazer`, or statsmodels summaries converted with care.
- Figures: `matplotlib` saving PDF with the document's fonts and sizes. Set the figure width to the column or text width in inches and the font size to the document's caption size, so nothing is scaled. The `pgf` backend (`matplotlib.use("pgf")` with `pgf.texsystem = "lualatex"`) typesets labels with LaTeX itself.
- Avoid `tikzplotlib`: unmaintained and broken with current matplotlib. If editable pgfplots code is wanted, export the data to CSV and write the pgfplots axis instead.
- Calculations inside the document: PythonTeX (`pythontex` package) runs Python during the build. It needs `--shell-escape` and an extra build step; use only when the user wants computation in the `.tex`, and say it executes code.

## R

- Sweave/knitr: `.Rnw` files mix R chunks and LaTeX; `knitr::knit("paper.Rnw")` produces the `.tex`. R Markdown and Quarto (below) are the more common route today.
- Tables: `modelsummary(models, output = "latex")`, `fixest::etable(..., tex = TRUE)`, `kableExtra::kbl(df, format = "latex", booktabs = TRUE)`, `xtable`.
- Figures: `ggsave("figures/fig1.pdf", width = 3.3, height = 2.4, device = cairo_pdf)` with a theme whose base size matches the document; `tikzDevice` when labels must be typeset by LaTeX.

## Julia

- `PGFPlotsX.jl` writes pgfplots code or PDFs directly; `Latexify.jl` turns expressions and tables into LaTeX.

## Quarto and R Markdown

- They build PDF through LaTeX. Keep the user's `.qmd`/`.Rmd` as the source and customise the LaTeX side through YAML: `format: pdf` with `documentclass`, `include-in-header` (preamble additions), `pdf-engine: lualatex`, or a full custom template (`template:`).
- Apply this skill's presets by moving their preamble into the header include, not by converting the project to plain `.tex` unless asked.

## Pandoc

- First step for converting Markdown, DOCX, HTML or ODT to LaTeX: `pandoc input.docx -s -o draft.tex` (add `--extract-media=media` for images).
- Pandoc's output is a starting point: rebuild structure (template, preset), fix tables and math environments, then design. For documents that stay in Markdown, a custom Pandoc LaTeX template carries the preset.

## TikZ and pgfplots as drawing frameworks

- Load only the TikZ libraries the figure uses (`arrows.meta`, `positioning`, `calc`, `shapes.geometric`, `decorations.pathreplacing`).
- Define styles once (`\tikzset{box/.style={draw, rounded corners, inner sep=4pt}}`) and use them across figures for a consistent visual language.
- Position with `positioning` (`right=of a`) and computed coordinates rather than absolute numbers copied from trial and error.
- Diagrams with many nodes: `graphs`/`graphdrawing` (LuaLaTeX), `forest` for trees, `tikz-cd` for commutative diagrams, `circuitikz` for circuits, `pgfgantt` for schedules.
- Large or numerous figures slow compilation: externalise (`\usetikzlibrary{external}` and `\tikzexternalize`, which needs `--shell-escape`) or build each figure once as a standalone PDF (`\documentclass{standalone}`).

## Overleaf

- A project downloaded from Overleaf builds locally with `latexmk`; read `latexmkrc` and check the main document in Overleaf project settings. Local `build.py` ignores rc files unless `--trust-project-config` is explicitly authorized; that configuration executes Perl, independently of shell escape.
- On Overleaf the compiler (pdfLaTeX, XeLaTeX, LuaLaTeX) and the TeX Live year are chosen in project settings; a `% !TEX program = lualatex` magic comment is a reminder, not a setting there.
- Fonts: Overleaf ships the TeX Live fonts used by the bundled templates; system fonts are unavailable unless uploaded to the project.
- When preparing a project for Overleaf, keep it self-contained (all images, `.bib`, class and style files in the project) and check whether required external commands are supported by that environment before using them. A local build does not establish that the project was tested on Overleaf.

## Editors and build files

- `latexmkrc` in the project root can share engine and options with collaborators who explicitly trust and load it: `$pdf_mode = 4;` (LuaLaTeX), `$bibtex_use = 2;`.
- VS Code (LaTeX Workshop), TeXstudio and TeXworks read the `% !TEX program` magic comment.
