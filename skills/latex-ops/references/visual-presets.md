# LaTeX Design System Library

Purpose: Visual/editorial presets and selection logic for latex-ops.

This file defines **how a document looks and behaves visually**. Functional architecture is defined in `references/functional-templates.md`. The canonical operating behavior remains in `SKILL.md`.

Preset references below name files in `assets/templates/presets/`, relative to the skill root.

## Core rule

A document has two independent coordinates:

1. Functional Template - what the reader must do with the document and how information is organized.
2. Visual Preset - typography, grid, measure, hierarchy, spacing, color, margin behavior, and component language.

Function outranks style. Mandatory venue/institutional rules outrank both.

When a preset is selected, consult only its matching `.tex` reference. Read a second preset only for an explicitly requested hybrid.

## Educational material

For course material (lecture notes, problem sets, course plans), default to sober editorial design: clear progression, readable instructions, sufficient answer space, controlled density, restrained color, functional diagrams/tables, and predictable components. Never invent grades, levels or answer keys.

## Visual presets

### Swiss Minimal
Aliases: Swiss, Minimal, Clean Editorial, Rams.
Character: quiet, precise, rational, restrained. Strong grid, deliberate alignment, useful negative space, few hierarchy levels, neutral palette with at most one principal accent, minimal chrome.
Hierarchy order: position -> space -> size -> weight -> restrained color.
Use broadly for professional, technical, educational, administrative, reference, and general-purpose documents.
Implementation: KOMA-Script when its integrated page/typographic architecture materially helps; otherwise simplest suitable class.
Reference: `assets/templates/presets/01_swiss_minimal.tex`.

### Tufte Editorial
Character: spacious intellectual design built around primary prose plus marginal supporting information.
Use for essays, annotated explainers, lectures, and information-rich narratives where proximity matters.
Use the margin only when it carries real information. Avoid when heavily tabular, venue-controlled, or writing width is critical.
Reference: `02_tufte_editorial.tex`.

### Kao Textbook
Character: contemporary educational publishing with main narrative plus active information margin.
Use for textbooks, long study guides, technical/educational books, richly annotated manuals, and modular learning material.
`kaobook`/`kaohandt` may be used when their margin architecture materially helps; do not import every feature by default.
Reference: `03_kao_textbook.tex`.

### Classic Editorial
Character: durable long-form typography with classical proportions, quiet running matter, duplex-aware layout, serif body when appropriate, and restrained chapter openings.
Use for books, long guides, literary/scholarly work, and classic theses when regulations permit.
Consider `memoir` or KOMA-Script when useful.
Reference: `04_classic_editorial.tex`.

### Minimal Research
Character: compact, sober academic design optimized for uninterrupted reading and scanning.
Use for papers, preprints, technical notes, literature reviews, and technical theses without mandatory venue formatting.
Single column by default; predictable hierarchy; restrained metadata; professional figures/tables; minimal color.
Reference: `05_minimal_research.tex`.

### Modern Report
Character: professional editorial design between an academic report and a restrained corporate publication.
Use for assessments, proposals, executive reports, project reports, and professional/institutional deliverables.
Strong opening hierarchy, efficient scanning, clean tables, quiet semantic callouts, restrained accent.
Reference: `06_modern_report.tex`.

### Minimal Beamer
Character: content-first presentations with little chrome, large type, strong whitespace, simple section frames, and one primary idea per frame.
Use for teaching, academic, technical, and professional talks.
Reference: `07_minimal_beamer.tex`.

### Magazine Editorial
Character: multi-column, image-aware editorial composition with stronger page rhythm than Swiss Minimal while remaining disciplined.
Use for magazines, newsletters, feature reports, catalogs, brochures, portfolios, and editorial posters.
System: column grid; opening spreads/eyebrows; captions; pull quotes used sparingly; deliberate image scale; controlled variation between article openings and body pages.
Use `flowfram` only when arbitrary flowing frames are a real requirement; otherwise prefer simpler multi-column/grid mechanisms.
Reference: `08_magazine_editorial.tex`.

### Legal Minimal
Character: conservative, neutral, highly legible legal/administrative design. Authority comes from structure, not decoration.
Use for contracts, policies, terms, formal declarations, and clause-driven documents.
System: serif or neutral sans body according to convention; clear numbered clauses; restrained metadata; strong cross-reference; no decorative color dependence; signature blocks and annexes treated consistently.
Reference: `09_legal_minimal.tex`.

## Hybrids

A hybrid must have one base preset and a narrowly defined imported trait, for example:
- Swiss Minimal + Tufte-style sidenotes
- Classic Editorial + sans-serif headings
- Kao Textbook, more restrained
- Modern Report + Swiss typography
- Swiss Minimal + Magazine Editorial image rhythm

Do not mechanically mix signature components from multiple presets.

## Selection behavior

If the user names a functional template and preset, use both. If only one is named, infer the other. If neither is named, consult `references/functional-templates.md` and choose without asking when one option is clearly superior.

Natural aliases should resolve automatically. The user does not need to know canonical names.
