# LaTeX Technical Reference

Last verified: 2026-08-12
Purpose: Version-sensitive technical baseline for latex-ops. This is a reference, not a second operating prompt.

## 1. Freshness rule

LaTeX releases, tagged-PDF support, package compatibility, and publisher requirements change. Verify current official documentation when exact current behavior matters, especially for accessibility, package compatibility, engine behavior, or venue templates.

## 2. Engines and fonts

For new custom documents, LuaLaTeX is a strong default when Unicode, OpenType, multilingual work, or the current tagged-PDF workflow matters. Do not override a venue or toolchain that requires another engine.

`fontspec` is for XeLaTeX and LuaLaTeX and provides access to OpenType/AAT fonts. Current CTAN baseline reviewed: fontspec 2.9g (2025-09-29).

Use `microtype` when its refinements are compatible and useful. Current baseline reviewed: microtype 3.2d (2026-03-01). Character protrusion is supported by LuaTeX; font expansion is available with LuaTeX.

Do not make an undeclared system font a portability requirement. For reusable templates, either use TeX-distributed fonts or declare/fallback the system-font dependency explicitly.

## 3. Classes

KOMA-Script is an appropriate option when integrated typographic/page-layout control materially improves an article/report/book. Current CTAN baseline reviewed: 3.49.2 (2026-02-02).

`memoir` is an appropriate option for long-form publication when its integrated page styles, chapter styles, and layout controls provide a concrete advantage. Current CTAN baseline reviewed: 3.8.4b (2025-11-04).

Neither should be used merely because it is more sophisticated than a standard class.

## 4. Tables and hyperlinks

`booktabs` remains a strong baseline for publication-quality tabular structure and supports `longtable` integration. Favor whitespace, semantic alignment, and restrained horizontal rules over dense vertical grids.

`hyperref` remains the standard hyperlink/navigation layer but package/class/tagging compatibility should be checked in accessibility-sensitive workflows. Current CTAN baseline reviewed: 7.01r (2026-06-17).

## 5. Accessible PDF — current 2026 workflow

The LaTeX Tagged PDF Project documents accessible-PDF generation for LaTeX2e 2026-06-01 and 2025-11-01. For new documents, LuaLaTeX is the preferred engine in the official usage guidance.

Use a current LaTeX release when possible. Accessible-PDF support is actively developed and older releases may lack current syntax or package support.

The current basic workflow uses `\DocumentMetadata{...}` before `\documentclass`, with keys for language, PDF standard, tagging, and tagging setup. For PDF/UA-2 work, configure the requested standard and tagging explicitly rather than relying on legacy prototype/testphase instructions.

The LaTeX core can produce PDF/UA-2-conforming documents, but contributed class/package support is still an important compatibility concern. Check the current tagging-status documentation for packages used by the document.

For mathematics, use the current supported MathML/tagging workflow. For figures and graphics, supply appropriate alternative text or artifact classification. For tables, provide meaningful header structure when required.

Compilation success is not accessibility conformance. Validate with an appropriate current validator and inspect logical structure. The LaTeX Project currently points to tools including veraPDF for standards validation and its own structure-inspection tooling.

## 6. Sources reviewed

Primary/current sources:
- LaTeX Tagged PDF documentation: https://latex3.github.io/tagging-project/documentation/
- Accessible-PDF usage instructions: https://latex3.github.io/tagging-project/documentation/usage-instructions
- KOMA-Script: https://ctan.org/pkg/koma-script
- memoir: https://ctan.org/pkg/memoir
- fontspec: https://ctan.org/pkg/fontspec
- microtype: https://ctan.org/pkg/microtype
- booktabs: https://ctan.org/pkg/booktabs
- hyperref: https://ctan.org/pkg/hyperref

Use official package documentation rather than this summary when exact syntax or compatibility matters.

## 7. Specialized document classes/packages

The following packages are **optional implementation tools**, not mandatory project dependencies. Prefer custom, portable implementations when the specialized package adds little value.

- `moderncv` — CV class. CTAN baseline reviewed: 2.6.1 (2026-06-24). Useful when its CV semantics/layout help. CTAN currently marks it tagged-PDF incompatible, so do not choose it blindly for accessibility-sensitive work.
- `scrlttr2` — KOMA-Script letter class. Baseline reviewed: 3.49 / KOMA-Script 3.49.2 (2026-02-02). Useful for letter-specific layout variables and correspondence conventions. CTAN currently marks it tagged-PDF incompatible.
- `classicthesis` — thesis package. Baseline reviewed: 4.8 (2025-02-02). Treat it as an optional implementation/reference when institutional rules permit; do not let it override a mandatory thesis class.
- `contract` — legal-document package. Baseline reviewed: 0.92 (2026-04-23). It is the current successor to the former KOMA-Script `scrjura` package and supports custom legal environments, including Anglo-American specifications. Use when semantic clause machinery is beneficial.
- `flowfram` — arbitrary flowing frames for magazines, posters, brochures, and nonstandard page layouts. Baseline reviewed: 2.3 (2026-06-19). Use only when a conventional grid/multicolumn implementation is insufficient.
- `leaflet` — two-fold flyer/leaflet class. Baseline reviewed: 2.1c (2024-03-12). Useful for physical imposition of a folded sheet. CTAN currently marks it tagged-PDF incompatible.
- `minutes` — meeting-minutes package. Baseline reviewed: 1.8f. It supports tasks, open-task lists, attachments, decisions, and votes. Its last listed package announcement is older; prefer a compact custom system unless those specialized features are required.
- `invoice2` — invoice package with VAT/totals. Baseline reviewed: 2018-01-15. Because it is older, prefer explicit/custom calculations or application-side deterministic arithmetic unless its feature set clearly fits the task.
- `beamerposter` — Beamer-based large-format poster extension. Baseline reviewed: 1.13 (2018). CTAN currently marks tagged PDF unsupported. Prefer a custom large-page grid or `flowfram` for new work unless Beamer integration is a concrete advantage.

## 8. Specialized implementation decision rule

When a functional template maps to a specialized class/package:

1. Check whether the package solves a real structural requirement rather than only providing a pre-styled appearance.
2. Check current maintenance status and engine/class compatibility.
3. Check accessibility/tagging compatibility when accessible PDF is required.
4. Prefer the skill's bundled `.tex` reference when a simple custom implementation is sufficient.
5. Preserve mandatory institutional, legal, or publisher classes even when a project preset would otherwise be preferable.

## 9. Additional sources

- moderncv: https://ctan.org/pkg/moderncv
- scrlttr2 / KOMA-Script: https://ctan.org/pkg/scrlttr2 and https://ctan.org/pkg/koma-script
- ClassicThesis: https://ctan.org/pkg/classicthesis
- contract: https://ctan.org/pkg/contract
- flowfram: https://ctan.org/pkg/flowfram
- leaflet: https://ctan.org/pkg/leaflet
- minutes: https://ctan.org/pkg/minutes
- invoice2: https://ctan.org/pkg/invoice2
- beamerposter: https://ctan.org/pkg/beamerposter
