# latex-ops roadmap

Approved on 2026-10-15. The current delivery is **0.1.2 only**, based on v0.1.1 (`330053a`). Versions 0.2.0–0.6.0 are saved for later work, not authorized as concurrent release stages. Complete and review one stage before starting the next. This document preserves the approved scope; unchecked items are not shipped capabilities.

## Architecture and release rules

- Keep one skill with `SKILL.md` as a selective router; move details into thematic references.
- Keep central utilities in Python using the standard library. Declare external tools as optional, feature-specific integrations.
- Explicit arguments override project preferences. Mandatory institutional/publication rules override presets.
- Skill instructions and normative documentation stay in English; maintain the Brazilian Portuguese README.
- Preserve the personal `skills/latex`, official `.cls`/`.sty`/`.bst` files and published releases.
- Do not write under the retired workspace prefix, run new agent evals without specific approval, install components or alter personal agent profiles implicitly, publish to Overleaf or submit documents automatically.
- A failure blocks that stage's release; it does not require implementing later stages early.

## 0.1.2 — Corrective foundation (current release)

Implementation contract: [0.1.2 corrective release](development/0.1.2.md).

- Propagate failed/missing bibliography backends, preserve dotted names and separate output directories, process nonempty indexes, fail unsettled builds and reject stale artifacts as success evidence.
- Disable rc loading in latexmk probes/default builds; allow reviewed configuration through explicit trust. Distinguish Perl configuration from shell escape.
- Bound renderer execution and identify failed tools.
- Separate invisible working comments, visible draft markers and delivery pending-content lists; accept clearly labelled drafts.
- Require exact visual inspection coverage; correct Overleaf compiler guidance and metadata versions; identify historical evaluation results.
- Integrate approved transparent light/dark logos in both README headers, keeping tagline, badges, named language links, navigation and showcase.

Acceptance: backend errors cannot finish as success; dotted names work; diagnostics do not load rc; unsettled builds and existing artifacts cannot receive false approval.

## 0.2.0 — Delivery verification and reproducibility (deferred)

- [ ] Add a delivery verifier for compilation errors, undefined references/citations, missing glyphs, overfull boxes, rerun requests and pending-content markers.
- [ ] Add strict mode that prevents technical approval with blocking findings. Keep overfull boxes as contextual review warnings, without arbitrary size-based rejection.
- [ ] Separate automatic findings from agent-declared visual inspection.
- [ ] Add optional `latex-ops.json`: main document, engine, language, preset, bibliography, intended TeX version and institutional rules. Preferences never grant code-execution authorization.
- [ ] Separate task dependencies from the complete template catalog's dependencies.
- [ ] Record build receipts with commands, available versions, input files/hashes, executed stages and results.
- [ ] Distinguish bibliography key integrity, bibliographic identity, source consultation and claim support. Automate key integrity only; require identified evidence for other levels.
- [ ] Test installation, native discovery, relative resources and invocation in disposable Claude Code/Codex environments, plus standalone installation with the `skills` CLI. No live profile changes.
- [ ] Add macOS build CI and a separate Windows MiKTeX battery. Match platform claims to executed checks.

Acceptance: reports distinguish compilation, pending content and inspection; working articles are not blocked by unrelated template dependencies; platform claims have actual evidence.

## 0.3.0 — Portability, Overleaf and submission (deferred)

- [ ] Package projects for coauthors, Overleaf and submission, collecting required sources, images, bibliography and local dependencies.
- [ ] Exclude personal files, caches and unrelated material; detect external references and missing dependencies before claiming a package is self-contained.
- [ ] Generate main-document, engine, intended TeX-version and extra-step instructions.
- [ ] Extract and rebuild in another directory without the original tree.
- [ ] Add a dedicated Overleaf reference: import/export, fonts, bibliography, settings, logs, clean recompilation and timeout diagnosis. Distinguish local validation from an actual Overleaf test.
- [ ] Offer pregenerated PDFs for costly figures while preserving regeneration sources.
- [ ] Tie submission checklists to the official kit, year, modality and stage: anonymity, limits, figures, bibliography, metadata and required declarations.
- [ ] Compare migration content: sections, values, equations, units, citations, captions and appendices.
- [ ] Link reviewer responses to real changes; recheck locations against the final PDF.

Acceptance: extracted packages rebuild independently; requirements are pass/fail/unverified with evidence; local builds are not described as Overleaf tests.

## 0.4.0 — Revisions and long documents (deferred)

- [ ] Compare two files or project trees, producing file inventories and source differences.
- [ ] Highlight changes to numbers, units, equations, tables and citation keys for agent review; textual comparisons do not prove semantic equivalence.
- [ ] Offer a marked-change PDF using an optional appropriate integration; preserve both originals.
- [ ] Add a long-document example with separate chapters, glossary, acronyms, symbols, index and cross-references.
- [ ] Record intentional changes and review pending items.
- [ ] Define digital-reading checks: links, bookmarks, navigation and structure.
- [ ] Define print checks: duplex, binding margins, intentional blank pages and grayscale legibility.
- [ ] Keep accessibility validation separate from visual inspection; record tool, result and limits when conformance is requested.

Acceptance: material changes are locatable; reports identify what needs human judgment; generating a PDF alone proves neither preservation, full inspection nor conformance.

## 0.5.0 — Software and hardware documentation (deferred)

- [ ] Organize technical documentation guidance into tutorial, task guide, reference and explanation.
- [ ] Expand manual, procedure and quick-reference templates.
- [ ] Add complete software and equipment manuals with clearly identified illustrative content.
- [ ] Software: installation, first use, configuration, update, removal, CLI/API, errors, architecture and compatibility.
- [ ] Hardware: model/revision, interfaces, pinout, dimensions, power, operating conditions, assembly, maintenance and troubleshooting.
- [ ] Bind information to the relevant release/commit, firmware or physical revision. Never invent parameters, specifications or test results.
- [ ] Include code directly from example source files and record commands actually tested.
- [ ] Add component, flow, circuit and protocol-field diagrams. Require TikZ, CircuiTikZ and `bytefield` only where used.
- [ ] Integrate Sphinx and Doxygen LaTeX/PDF generation while preserving regeneration sources.

Acceptance: examples match documented versions; code excerpts have identified sources; Sphinx/Doxygen outputs regenerate; hardware manuals separate supplied specifications from performed checks.

## 0.6.0 — Executable data and specialized integrations (deferred)

- [ ] Add small Python, R and Julia examples with included input data, reproducible transformations, tables and figures consumed by documents.
- [ ] Add minimal Quarto/R Markdown and Pandoc examples, preserving their formats as the source of truth.
- [ ] Automatically check values, precision, units and consistency across text, tables and plots.
- [ ] Record stages/examples actually executed, versions and results.
- [ ] Keep integration dependencies outside the mandatory core, with separate instructions and checks.
- [ ] Update the showcase from versioned example outputs.

Acceptance: each integration regenerates its outputs from included data; values reconcile; an unavailable integration does not block other features.

## Planned public interfaces

Existing commands remain supported. Only the trust flag and renderer timeout belong to 0.1.2; other additions follow their stage.

| Interface | Contract |
| --- | --- |
| `build.py --json` | Structured execution result, stages, artifacts and repeat requirement |
| `build.py --trust-project-config` | Allow reviewed configuration covered by task authorization |
| `check_env.py --project MAIN.tex` | Project-specific diagnosis; retain full-catalog mode |
| `verify.py MAIN.tex --json [--strict]` | Consolidate findings and technical checks |
| `package.py MAIN.tex --target overleaf\|submission\|collaboration --output PROJECT.zip` | Prepare project package and destination instructions |
| `compare.py OLD NEW --output DIR` | Produce source/project difference report |

- JSON reports use `schema_version` and separate execution, findings and visual inspection.
- Exit 0: requested operation succeeded; 1: operation failed or strict verification rejected; 2: invalid input/configuration.
- Unsettled compilation fails. Drafts may compile with explicit documentary pending items.
- PNG existence never establishes visual inspection.
- New operations never silently overwrite originals or existing results. Packaging/comparison never execute discovered project content.

## Required test matrix and release gates

- [ ] latexmk/fallback; BibTeX/Biber absent, failing and working.
- [ ] Spaced/dotted names, separate output directories, indexes and unsettled references/auxiliaries.
- [ ] Old PDF/PNG, missing/failing/timed-out renderer.
- [ ] Rc-free diagnostics and explicitly trusted configuration when required.
- [ ] Visible pending content, undefined citations and partial inspection coverage.
- [ ] Chapters, images and bibliography; extracted package independent of origin.
- [ ] Value/equation/citation changes identified for review.
- [ ] Disposable installation, native invocation, relative resources and no duplicate copies.
- [ ] Technical/data example regeneration and numerical checks.

Before each release: run the checks applicable to that stage; retain existing template/example builds; compile/render affected examples and inspect their pages; review English/pt-BR docs; synchronize versions; update changelog and progress. Publish only the revision that passed applicable checks. Record missing optional tests as not executed. Keep old eval results tied to their assessed version; do not rerun without approval.
