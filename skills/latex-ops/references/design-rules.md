# Design rules

Detailed rules behind the workflow in `SKILL.md`. Read only the section the task needs: typography and layout for any new or redesigned document; classes and packages before choosing a preamble; accessibility when tagged or accessible PDF is required; academic papers and theses for any paper, thesis or venue formatting; presentations for Beamer.

## Acceptance criteria

Before substantial implementation, derive only criteria relevant to the request. Consider reader/task, language/locale, document template, design preset, required content/hierarchy, medium, page/slide size, duplex/binding/handwriting needs, mandatory class/template/branding, compiler, font/dependency availability, mathematics, bibliography, tables/figures/diagrams/forms/exercises, navigation, accessibility, editable areas, and requested deliverable.

Do not create requirements the task does not need.

## Typography and layout

Choose typography and geometry for the reading conditions rather than from habit.

- Prefer LuaLaTeX for new custom documents when Unicode, OpenType, substantial multilingual work, or current accessible-PDF workflows benefit from it. Use another engine when the class, venue, toolchain, or user requires it.
- Use `fontspec` only with compatible Unicode engines. Use `microtype` when compatible and useful.
- Inter is a preferred sans-serif option for contemporary custom documents when available; it is not mandatory. Do not force it onto venue-controlled or long-form documents where another system is more appropriate.
- For portability-sensitive projects, prefer fonts reliably available in the target TeX environment or provide an explicit fallback/dependency note.
- Use a compatible dedicated mathematical type system for substantial mathematics.
- Configure language and hyphenation explicitly when known.
- Maintain comfortable measure, leading, and body size. Solve density structurally before shrinking text.
- Set geometry deliberately from page size, reading distance, binding/duplex needs, information density, and medium.
- Use one consistent paragraph-separation strategy unless the genre requires otherwise.
- Build hierarchy primarily with position, spacing, scale, and weight; use restrained color/rules only when they solve a structural problem.
- Keep headers, footers, folios, captions, metadata, and secondary labels quieter than primary content.
- Prevent obvious defects such as stranded headings, nearly empty pages, uncontrolled floats, cramped tables, excessive line length, clipping, and undersized text.
- Meaning and hierarchy should survive grayscale reproduction unless the requested medium explicitly permits otherwise.

## Classes and packages

Choose the class from constraints and function.

- Use standard classes when sufficient.
- Consider KOMA-Script or `memoir` when their integrated editorial capabilities provide a concrete advantage.
- Preserve required venue/institutional classes.
- Use Beamer only for presentations.
- Prefer class-native mechanisms before packages that duplicate them.

Use the minimum stable package set required. Common tools may include `fontspec`, `microtype`, `geometry`, `babel`, `graphicx`, `xcolor`, `enumitem`, `booktabs`, `array`, `tabularx`, `longtable`, `siunitx`, `amsmath`, `amssymb`, `unicode-math`, `biblatex`, `csquotes`, `hyperref`, `cleveref`, and `tcolorbox` when justified.

This is a capability list, not a default preamble. Add packages only when their capability is used. Check compatibility with restrictive classes and tagged-PDF workflows.

## Components

Tables: prefer semantic columns, whitespace, alignment, and publication-quality horizontal structure over vertical-rule grids; align numeric data and units consistently; restructure before shrinking; repeat headers in multipage tables when needed.

Figures: use predictable paths; keep sizing, placement, captions, labels, and references consistent; never invent missing assets or credits; distinguish informative graphics from decorative artifacts.

References: use semantic labels and cross-references rather than manually typed numbers.

Lists: use them for genuinely enumerable information and keep indentation/spacing consistent with document density.

Callouts: use a box only for a distinct semantic function such as warning, definition, exercise, answer area, or key result. Prefer spacing, labels, or restrained rules when sufficient.

Mathematics: use semantic math environments and notation; define recurring notation only when repetition justifies abstraction; avoid manual visual hacks that weaken structure.

## Accessibility

Treat accessibility as architecture, not decoration.

For ordinary documents: maintain logical sectioning and reading order, avoid color-only meaning, use semantic headings/lists/tables/captions/references, keep text usable, and provide useful metadata/navigation when supported.

When accessible or standards-conforming PDF is required:
1. Consult current official LaTeX tagging guidance; prefer a current LaTeX release and LuaLaTeX for new documents unless constraints require otherwise.
2. Use the current `\DocumentMetadata`/tagged-PDF workflow rather than obsolete accessibility hacks.
3. Configure language, metadata, tagging, and requested PDF standard appropriately.
4. Provide alternative text or artifact classification for graphics as appropriate.
5. Mark table header structure where required.
6. Preserve semantic mathematics and use the current supported math-accessibility workflow.
7. Check current class/package tagging compatibility before optional package selection.
8. Validate with an appropriate current validator when tools are available and inspect logical structure, not only appearance.

Do not claim PDF/UA, PDF/A, WCAG, or other formal compliance merely because tagging commands are present. Claim conformance only when appropriate validation supports it.

## Source architecture

Treat `.tex` as a maintainable document system.

Organize the preamble coherently around metadata/engine assumptions, language/fonts, geometry, typography, structural styling, content-specific packages, bibliography/references, hyperlinks, and custom semantic definitions.

Use intention-revealing names. Create a macro/environment only when it prevents meaningful repetition, represents a recurring semantic element, centralizes a genuine design value, improves editability, or solves a recurring edge case. Keep one-off styling local.

Use comments for rationale, compatibility constraints, non-obvious implementation details, editable markers, and missing dependencies—not to narrate obvious code.

Prefer one self-contained file unless multi-file architecture provides a concrete advantage or the user requests it. For multi-file projects, provide a clear file tree and complete required files.

## Revising existing files

Inspect an existing file before diagnosing or rewriting it. Identify mandatory conventions and probable origin when relevant.

Preserve sound existing decisions and venue constraints. Fix demonstrated defects. Avoid unrelated refactors. Do not rewrite factual content unless requested. Prefer the smallest coherent change set that achieves the requested improvement.
## Academic papers and theses

The venue decides first. A journal, conference, publisher or university class overrides every preset here; the presets apply only to papers with no imposed format (preprints, working papers, course essays, internal reports), where Minimal Research is the default.

### Before writing

- Identify the target: venue, year, track or article type, and stage (anonymous review, preprint, camera-ready). Formats change every year; a kit from a previous year is not the current kit.
- Use the official author kit (class, style and bibliography-style files) supplied by the user or downloaded from the venue's own page. Never rewrite a `.cls`, `.sty` or `.bst` from memory and never edit the official ones; adapt the document to them.
- Write down the rules that matter before migrating: page or word limit and what it excludes (references, appendices), anonymity, required sections and statements, citation style, figure formats, metadata.

### Structure and prose

- Title, abstract, keywords and section order follow the venue. Without a venue: introduction with the contribution stated plainly, related work, method, results, discussion or limitations, conclusion.
- One idea per paragraph; the first sentence carries it. Define every symbol at first use; keep notation identical across text, equations, figures and tables.
- Number only equations that are referred to. Refer with `\cref`/`\Cref` (or the venue's convention), never with typed numbers.
- Keep the author's claims: do not strengthen, soften or add results while formatting.

### Citations and bibliography

- Every `\cite` must point to a real, checked entry. Do not create bibliography entries from memory; when a source cannot be verified, leave `% [CITATION NEEDED: claim]` and say so.
- Keep citation keys, and keep the difference between textual and parenthetical citation (`\citet` versus `\citep`, `\textcite` versus `\parencite`); do not replace every citation with one command.
- Use the bibliography style and backend the venue or project already uses (BibTeX with a `.bst`, or biblatex with biber); do not switch backends to make a warning disappear.
- Zero undefined citations and references is part of done.

### Figures and tables

- Vector formats (PDF) for plots and diagrams; raster only for photographs and screenshots, at print resolution.
- Fonts in figures should match the document's size and family closely enough to read as one system; no text smaller than the footnote size.
- `subcaption` for side-by-side panels (not the obsolete `subfigure`); `booktabs` tables without vertical rules; numbers aligned on the decimal point with `siunitx`.
- Captions say what the reader should see, not only what is plotted. Colour choices must survive grayscale printing and colour-blind readers: vary marker shape or line style as well as hue.

### Mathematics

Full rules in `references/math.md`; the essentials:

- `amsmath` and `mathtools` for display math; `amsthm` (or `thmtools`) for theorem, lemma, definition and proof environments, numbered consistently.
- Declare recurring operators and delimiters once (`\DeclareMathOperator`, `\DeclarePairedDelimiter`); do not hand-space math.
- One algorithm package per document (`algpseudocode` with `algorithm`, or `algorithm2e`), never both.
- Do not change the meaning of an equation while reformatting it; check indices, signs and constants survive.

### Page limits and anonymity

- Measure the compiled main text against the limit as the venue defines it; total page count proves nothing when references or appendices are excluded.
- To fit a limit, propose content cuts. Do not shrink fonts, margins or spacing, or use negative space: reviewers and desk editors notice, and many venues reject it.
- For anonymous review, use the template's review mode, then inspect the PDF and its metadata: author block, acknowledgments, funding, self-citations written in the first person, URLs, file properties. Searching for names is not proof of anonymity; report what was checked.
- Never submit or upload anything on the user's behalf.

### Reporting a formatting job

Report the venue, year and stage with the source of the rules and the date checked; the changes made; the build result with measured page or word counts; each requirement as **pass**, **fail** or **unverified** with its evidence; and what the authors still have to supply. Successful compilation alone does not mean ready to submit.

## Presentations (Beamer)

- One message per slide; the title states it. Aim for at most about six bullets, two displayed equations, or one figure per slide; split rather than shrink text.
- Prefer separate slides to `\pause`/`\only` overlays unless the talk benefits from progressive reveal and the user wants it; handouts and PDF readers handle plain slides better.
- Define a small semantic colour set (emphasis, positive, negative) as macros, with WCAG AA contrast against the background and safe for colour-blind viewers; never encode meaning in colour alone.
- Motivation before formalism, concrete example before abstraction, a closing slide that repeats the key points; put anticipated questions on backup slides after the conclusion.
- Beamer hides many overflow warnings: render every slide and look for text or graphics crossing the frame or the footline.
- Diagrams drawn with TikZ should compute positions from values (`\pgfmathsetmacro`) rather than hard-coded approximations when they represent data or geometry.
