# Mathematics in LaTeX

Read the section the task needs. Every rule here serves one goal: mathematics that is correct, consistent and readable, written as structure rather than visual hacks.

Contents: 1 Engine and fonts · 2 Display environments · 3 Alignment and line breaking · 4 Notation and macros · 5 Spacing and punctuation · 6 Theorems and proofs · 7 Matrices and arrays · 8 Numbers and units · 9 Algorithms and code · 10 Plots and diagrams · 11 Physics and chemistry · 12 Checking the mathematics · 13 Accessible mathematics · 14 Teaching material · 15 Converting from other formats · 16 Errors and fixes

## 1. Engine and fonts

Choose the pair once and keep it for the whole document.

| Engine | Load | Notes |
| --- | --- | --- |
| pdfLaTeX | `amsmath`, `mathtools`, `amssymb` (or a font package that provides the symbols), text font package | Required by many journal classes. Matching pairs: `newtxtext,newtxmath` (Times-like), `lmodern` (Computer Modern), `libertinus` (pdfLaTeX version), `newpxtext,newpxmath` (Palatino-like). Load `amsthm` **before** `newtxmath`. |
| LuaLaTeX / XeLaTeX | `amsmath`, `mathtools`, then `unicode-math` last among math packages; `\setmathfont{...}` | OpenType math fonts: Latin Modern Math, New Computer Modern Math, STIX Two Math, Libertinus Math, TeX Gyre Pagella/Termes/Schola Math, Fira Math (sans, for slides). Do not load `amssymb`, `bm` or `amsfonts` with `unicode-math`; it provides the symbols and `\symbf`. |

Match the math font to the text font's design (serif with serif; Fira Math with Fira Sans on slides). A sans text with Latin Modern Math is acceptable for slides only when no matching sans math font is available; say so.

## 2. Display environments

| Need | Use |
| --- | --- |
| One numbered equation | `equation` |
| One unnumbered equation | `\[ ... \]` or `equation*`; never `$$ ... $$` |
| Several equations aligned at a relation | `align` / `align*` |
| Several equations centred, not aligned | `gather` |
| One long equation over lines | `multline`, or `split` inside `equation` for one number |
| Piecewise definitions | `cases` (`dcases` from `mathtools` for display-size fractions) |
| An aligned block inside a larger formula | `aligned`, `gathered` |
| Related equations numbered 1a, 1b | `subequations` around them |

Never use `eqnarray`: its spacing around the relation is wrong and it fights with labels.

Number only equations that the text refers to: use `\notag` on the others in `align`, or the starred environment. With many unreferenced equations, `\mathtoolsset{showonlyrefs}` numbers only the referenced ones automatically.

Put `\label` right after the content of the line it names, never on an unnumbered line. Refer with `\eqref{...}` or `\cref{...}`.

## 3. Alignment and line breaking

- Align at the relation symbol: `&=` and `&\le`, with `&` before the symbol.
- Break a long right-hand side before a binary operator (`+`, `-`, `\times`), and indent the continuation with `&\quad + ...` so the reader sees it continues.
- `\MoveEqLeft` (mathtools) starts a long first line further left in multi-step derivations.
- In a chain of equalities, each line should be one justified step; put the justification on the right with `&& \text{(by \eqref{eq:x})}` or below with `\intertext{}` / `\shortintertext{}` (mathtools).
- Inline formulas should not break across lines at awkward points; for long inline math, display it instead.
- Do not shrink a formula with `\small` or `\resizebox` to make it fit; restructure it (define a symbol, split the line, move a factor out).

## 4. Notation and macros

Define notation once, in the preamble, and use the macro everywhere. Changing notation later then means one edit.

```latex
\DeclareMathOperator{\tr}{tr}            % upright operator names with correct spacing
\DeclareMathOperator*{\argmin}{arg\,min} % starred: limits go below in display
\DeclarePairedDelimiter{\abs}{\lvert}{\rvert}
\DeclarePairedDelimiter{\norm}{\lVert}{\rVert}
\DeclarePairedDelimiter{\set}{\{}{\}}
\DeclarePairedDelimiterX{\inner}[2]{\langle}{\rangle}{#1, #2}
\newcommand{\R}{\mathbb{R}}
\newcommand{\dd}{\mathop{}\!\mathrm{d}}  % differential: \int f(x) \dd x
\newcommand{\E}{\mathbb{E}}
```

- Paired delimiters: `\abs{x}` stays normal size, `\abs*{\frac{a}{b}}` grows automatically, `\abs[\big]{x}` fixes the size. Prefer explicit sizes (`\bigl( \bigr)`) to `\left( \right)` when the automatic size is too large.
- Vectors and matrices: pick one convention and say it in the text. Bold upright or italic with `\symbf` (unicode-math) or `\bm` (pdfLaTeX, package `bm`); arrows (`\vec`) suit physics teaching more than research papers.
- Upright for things that are not variables: function names (`\sin`, `\log`, declared operators), the differential d if the field uses it, Euler's e and the imaginary unit i when following ISO 80000-2, units, and multi-letter subscripts that are words (`x_{\mathrm{max}}`, `T_{\text{room}}`).
- Definitions with `\coloneqq` (mathtools), not `:=`, so the colon centres on the axis.
- Functions: `f \colon A \to B`, not `f: A \to B`.
- Sets: `\{\, x \in \R \mid x > 0 \,\}` with `\mid`, not `|`.
- Fractions: `\frac` in display; `\tfrac` or a slash `a/b` inline; never a stacked fraction inside an exponent.
- Ellipses: `\dots` lets amsmath choose; `\cdots` between operators (`a_1 + \cdots + a_n`), `\ldots` in lists (`x_1, \ldots, x_n`).
- Do not use `\bf`, `\it`, `\rm` (obsolete); use `\mathbf`, `\mathit`, `\mathrm` or the semantic macros above.

## 5. Spacing and punctuation

- A display formula is part of the sentence: end it with the comma or full stop the sentence needs, inside the math (`x = 1 .` or with `\,.`).
- Thin space before differentials and between a function and its argument when ambiguous: `\int_0^1 f(x) \, \mathrm{d}x` (built into `\dd` above).
- `\quad` or `\qquad` between a formula and a condition: `a_n \to 0 \quad \text{as } n \to \infty`.
- Words inside math with `\text{...}`, including spaces at the edges (`\text{ for all }`).
- Do not insert manual negative spaces (`\!\!\!`) to fix appearance; the fix is usually a missing macro or the wrong delimiter.

## 6. Theorems and proofs

```latex
\usepackage{amsthm}          % before newtxmath on pdfLaTeX
\theoremstyle{plain}         % italic body: theorem, lemma, proposition, corollary
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}          % shared counter: Theorem 2.1, Lemma 2.2
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}    % upright body: definition, example, exercise
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\theoremstyle{remark}
\newtheorem*{remark}{Remark}
```

- One shared counter numbered within sections keeps references easy to find. `thmtools` (`\declaretheorem`) gives the same with less code and custom styles.
- Load `cleveref` after `hyperref` and the theorem definitions so `\cref{thm:x}` prints "Theorem 2.1".
- Put the end-of-proof mark on the last line when the proof ends with a display: `\qedhere` inside the final equation.
- A proof cites what it uses (`by \cref{lem:bound}`) and states where each assumption enters.
- Optional title: `\begin{theorem}[Banach]`; source of a known result: `\begin{theorem}[{\cite[Thm.~3]{key}}]`.

## 7. Matrices and arrays

- `pmatrix` (parentheses), `bmatrix` (brackets), `vmatrix` (determinant); `bmatrix*[r]` (mathtools) to right-align numbers.
- Inline small matrices: `\bigl(\begin{smallmatrix} a & b \\ c & d \end{smallmatrix}\bigr)`.
- Block or augmented matrices: `\left[\begin{array}{cc|c} ... \end{array}\right]`.
- Large sparse matrices: `\vdots`, `\ddots`, `\cdots` with explicit zeros only where they carry meaning.
- Tables of numbers are tables (`tabular` + `booktabs` + `siunitx`), not matrices.

## 8. Numbers and units (siunitx, version 3)

- `\num{12345.678}` groups digits and uses the configured decimal marker; `\num{1.2e-5}` prints scientific notation.
- `\qty{9.81}{\metre\per\second\squared}`, `\unit{\kilo\gram}`, ranges `\qtyrange{10}{20}{\celsius}`, lists `\qtylist{1;2;3}{\milli\metre}`.
- Uncertainty: `\qty{9.79 +- 0.04}{\metre\per\second\squared}` or `\num{1.234(5)}`; set `separate-uncertainty=true` if the field prefers it.
- Locale: `\sisetup{locale = DE}` or `output-decimal-marker = {,}` for comma-decimal languages (Portuguese, German, French).
- Table columns aligned on the decimal point: `S[table-format=2.3]`; wrap header text in braces.
- Rounding for presentation only (`round-mode=places, round-precision=2`); never round the user's results to a different precision than they reported without saying so.

## 9. Algorithms and code

- Pseudocode: `algorithm` (float and caption) + `algpseudocode` (`\Require`, `\Ensure`, `\State`, `\If`, `\For`, `\While`, `\Return`, `\Comment`), or `algorithm2e`. Never both in one document.
- Number lines (`\begin{algorithmic}[1]`) when the text refers to them.
- Keep pseudocode at the level of the method; real code goes in a listing.
- Source code: `listings` (no external tools) or `minted` (better highlighting; needs Python Pygments and `--shell-escape`, so tell the user). Use a monospaced font that has the glyphs the code needs.

## 10. Plots and diagrams

- Function plots and data plots: `pgfplots` with `\pgfplotsset{compat=1.18}` (or the installed version). `domain` and `samples` control smoothness; `semilogyaxis`/`loglogaxis` for orders of magnitude; `restrict y to domain` to drop poles.
- Plot exact formulas directly (`\addplot {exp(-x)}`) and data from files (`\addplot table[col sep=comma, x=t, y=v]{data.csv}`); never retype data by hand.
- Distinguish series by line style and marker as well as colour, so the plot survives grayscale and colour-blind readers.
- Axis labels name the quantity and unit (`time $t$ / \si{\second}`); the legend must not cover data (`legend pos=outer north east` when in doubt).
- 3D: `\addplot3[surf]` with `view={azimuth}{elevation}`; keep sample counts modest because compilation time grows fast.
- Commutative diagrams: `tikz-cd`. Graphs and trees: TikZ `graphs`/`trees` libraries or `forest`. Geometry figures: compute coordinates (`\pgfmathsetmacro`, `calc` library) instead of eyeballing them.
- Very heavy figures: externalise with the `external` library or produce a PDF once and include it.

## 11. Physics and chemistry

- Bra-ket notation: `braket` package or paired delimiters you define (`\DeclarePairedDelimiterX{\ket}[1]{\lvert}{\rangle}{#1}`).
- The `physics` package redefines common commands and has known spacing problems; prefer small explicit macros unless the user already uses it.
- Chemical formulas and equations: `mhchem` (`\ce{H2O}`, `\ce{A + B -> C}`) or `chemformula`.
- Tensors with staggered indices: `tensor` package or `{}^{a}{}_{b}` with care.

## 12. Checking the mathematics

Typesetting does not verify mathematics, and the reader trusts what looks finished.

- Re-derive or numerically check every result you write or transform: substitute values, check limits and special cases, check dimensions and units, verify a derivative by differentiating back. A quick Python or computer-algebra check is cheap.
- Numbers in tables and plots come from a computation or the user's data, never from estimation. State formulas that generate plotted curves.
- When converting or reformatting, compare symbols, signs, indices and constants line by line with the source; a dropped minus sign is the commonest silent error.
- Do not complete a proof the user left incomplete without saying so, and never present an unchecked derivation as a proof.
- Keep notation consistent across text, equations, figures and tables; list symbols in a nomenclature table for long documents.

## 13. Accessible mathematics

- Use real math markup, never images of equations.
- For tagged PDF: LuaLaTeX, `unicode-math`, a current LaTeX release (2025 or newer), and `\DocumentMetadata{lang=..., pdfstandard=ua-2, tagging=on}` before `\documentclass`. Mathematics then carries MathML (associated files by default; `tagging-setup={math/setup=mathml-SE}` for structure elements).
- Avoid conveying meaning only by colour inside formulas; avoid hand-built symbols made of overlapping glyphs.
- Validate with a PDF/UA checker before claiming conformance (see `references/technical.md`).

## 14. Teaching material

- Exercises: number them, give point values when graded, and leave answer space proportional to the expected work.
- Solutions from the same source with a switch (see the Problem Set template), so the two versions never drift apart.
- Worked examples: one step per line in `align*`, each step with a short reason.
- Use the notation of the course or textbook the students use, even when another is more common.

## 15. Converting from other formats

- MathJax/KaTeX/Markdown: `$...$` and `$$...$$` become `\( \)` and `\[ \]` or the right display environment; MathJax-only macros (`\bold`, `\dfrac` inside inline math overuse) need translating.
- Word (OMML) and Google Docs: export through Pandoc to LaTeX, then rebuild the environments by hand; Pandoc output uses generic `\[ \]` and inconsistent macros.
- Handwritten or image formulas: transcribe, then check every symbol against the source with the user when anything is ambiguous.

## 16. Errors and fixes

| Message | Usual cause | Fix |
| --- | --- | --- |
| `Missing $ inserted` | Math command used in text (`_`, `^`, `\alpha`) or a blank line inside display math | Wrap in math; remove the blank line |
| `Display math should end with $$` | Mixed `$$` and `\[` or unbalanced delimiters | Use `\[ \]` consistently |
| `Extra alignment tab has been changed to \cr` | More `&` than columns in `align` or a matrix | Count `&`: in `align`, pairs of columns per equation |
| `Double subscript` / `Double superscript` | `x_i_j` | Group: `x_{i_j}` or `x_{ij}` |
| `\left` / `\right` missing | Unbalanced, or split across `align` lines | Use `\bigl`/`\bigr`, or `\right.` and `\left.` per line |
| `Command \openbox already defined` | `amsthm` loaded after `newtxmath` | Load `amsthm` first |
| Symbols missing or `Option clash` with `unicode-math` | `amssymb`, `bm` or a pdfLaTeX math font loaded too | Remove them; use `\symbf` and the OpenType math font |
| `Undefined control sequence \mathbb` | pdfLaTeX without `amssymb`/`amsfonts` | Load `amssymb` (not with `unicode-math`) |
| Equation number on a separate line | Equation too wide | Break with `split`/`multline`, define symbols |
| `Missing number, treated as zero` after `\\` | Next line starts with `[` and is read as a spacing argument | Insert `{}` before the bracket |
