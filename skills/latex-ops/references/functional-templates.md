# LaTeX Functional Template Library

Purpose: Functional document architectures for latex-ops.

This file defines **what a document must do**. Visual language belongs in `references/visual-presets.md`. The canonical operating behavior remains in `SKILL.md`.

Template references below name files in `assets/templates/functional/`, relative to the skill root.

## Selection rule

Choose the functional template from the reader's task and document purpose. Then choose a visual preset separately. Mandatory institutional, publisher, legal, accessibility, or venue rules override project defaults.

Do not force every possible section into a document. Use only structures supported by the user's content and request. Never invent facts merely because a template contains a field for them.

## Education

### Workbook / Worksheet
Purpose: material learners actively complete, write on, review, and reuse.
Typical structure: concise context/model -> example -> controlled practice -> guided practice -> production/review when justified.
Core components: Exercise, Example, Remember, Language Note, Word Bank, Speaking, Writing, Challenge, Review, Answer Area.
Defaults: sober editorial language suited to the learners' age; sufficient handwriting space; predictable numbering; avoid revealing answers through layout.
Default visual preset: Swiss Minimal. Long/course-book-like material: Kao Textbook.
Reference: `assets/templates/functional/01_workbook.tex`.

### Assessment Report
Purpose: communicate evidence, performance, corrections, interpretation, priorities, and next steps.
Keep observed evidence, interpretation, and recommendation distinct. Never invent scores, CEFR levels, strengths, weaknesses, diagnoses, or learner quotes.
Default visual preset: Modern Report; quieter alternative: Swiss Minimal.
Reference: `02_assessment_report.tex`.

### Course Plan
Purpose: turn curriculum intentions into a navigable sequence of objectives, content, practice, review, and progression.
Use semantic week/module structures. Do not create false timing, outcome, or assessment precision when not supplied.
Default visual preset: Swiss Minimal; formal institutional alternative: Modern Report.
Reference: `03_course_plan.tex`.

### Book / Guide
Purpose: sustained reading and navigation across substantial material.
Possible architecture: front matter -> orientation -> parts/chapters -> recurring semantic components -> references/appendices -> back matter.
Default visual preset: Classic Editorial; educational/modular alternative: Kao Textbook; margin-intensive alternative: Tufte Editorial.
Reference: `04_book_guide.tex`.

## Professional and business

### Professional CV
Purpose: present experience, education, skills, selected achievements, publications, or projects with high scanning efficiency.
Modes: `CV Minimal` for ATS/standard professional use; `CV Editorial` for human-reviewed portfolios and senior/creative contexts.
Prioritize chronology, role/org/date alignment, factual economy, and machine-readable text. Avoid decorative rating bars, unexplained icons, and visual elements that replace explicit skill descriptions.
Implementation: custom/KOMA for maximal control; `moderncv` may be used when its structure is useful and accessibility constraints permit.
Default visual preset: Swiss Minimal.
Reference: `05_professional_cv.tex`.

### Formal Letter
Purpose: formal, institutional, recommendation, cover, request, or business correspondence.
Architecture: sender/recipient metadata -> date/subject -> salutation -> body -> closing/signature -> enclosures/copies when needed.
Prefer `scrlttr2` when its letter-specific layout controls are useful. Preserve jurisdictional/institutional conventions if supplied.
Default visual preset: Swiss Minimal.
Reference: `06_formal_letter.tex`.

### Executive Brief
Purpose: compress a decision-relevant issue into 1-3 pages for fast executive reading.
Typical structure: issue/opportunity -> key facts/findings -> implications -> recommendation -> immediate next step when supported.
Optimize for scanning, not report completeness. Keep evidence and recommendation distinct.
Default visual preset: Swiss Minimal or Modern Report.
Reference: `09_executive_brief.tex`.

### Professional Memo
Purpose: concise internal analysis or decision communication.
Typical metadata: To / From / Date / Subject. Typical body: Summary -> Background -> Analysis -> Recommendation.
Use prose-first structure with small metadata hierarchy. Avoid turning a memo into a dashboard.
Default visual preset: Swiss Minimal.
Reference: `10_professional_memo.tex`.

### Proposal
Purpose: explain a proposed project/service/research effort and make scope, deliverables, method, timing, assumptions, and decision path legible.
Possible structure: executive summary -> problem/opportunity -> scope -> deliverables -> approach -> timeline -> budget/investment -> assumptions/terms -> next step.
Use only fields justified by the request. Never invent prices, dates, legal terms, or commitments.
Default visual preset: Modern Report with Swiss Minimal restraint.
Reference: `11_proposal.tex`.

### Invoice & Quote
Purpose: present billable items, quantities, prices, taxes/discounts, totals, payment terms, and parties clearly.
Calculations must be deterministic and auditable. Use `siunitx`/explicit arithmetic or application-side calculation; do not trust prose inference for financial totals.
`invoice2` may be considered for its calculation features, but it is an older package and should not be a mandatory dependency.
Default visual preset: Swiss Minimal.
Reference: `12_invoice_quote.tex`.

### Meeting Minutes / Agenda
Purpose: capture agenda items, discussion, decisions, action items, owners, and deadlines; or prepare the same structure before a meeting.
Keep decision, action, owner, and due date fields semantically distinct. The `minutes` package may be consulted, but a compact custom architecture is preferred unless its specialized task/decision features are needed.
Default visual preset: Swiss Minimal.
Reference: `14_meeting_minutes.tex`.

## Academic and research

### Classic Thesis
Purpose: long academic work where classical book typography and sustained reading are appropriate and institutional rules allow design freedom.
Use strong front/main/back matter, chapter architecture, bibliography, appendices, page parity, and durable typographic proportions.
`classicthesis` is a reference/optional implementation, not a rule; institutional thesis classes override it.
Default visual preset: Classic Editorial.
Reference: `07_classic_thesis.tex`.

### Technical Thesis / Dissertation
Purpose: engineering/science/technical theses with equations, figures, nomenclature, algorithms, tables, appendices, and reproducible navigation.
Prioritize technical hierarchy, semantic numbering, cross-references, consistent notation, and venue/institutional compliance over decorative chapter styling.
Default visual preset: Minimal Research or Swiss Minimal.
Reference: `08_technical_thesis.tex`.

### Research Article
Purpose: journal-style paper when no venue class is imposed (preprints, working papers, essays submitted without a template).
Structure: title stating the finding, abstract with the main number, keywords, introduction with the contribution stated plainly, related work, method, results, discussion with limitations, conclusion, data/code availability.
Rules: see *Academic papers and theses* in `references/design-rules.md`; math conventions in `references/math.md`.
Default visual preset: Minimal Research.
Reference: `23_research_article.tex`.

### Conference Paper
Purpose: page-limited two-column paper, often anonymous for review.
Real submissions use the venue's official kit (IEEEtran, acmart, llncs, the year's `.sty`); this reference shows the density, float placement and review/camera-ready switch.
Reference: `24_conference_paper.tex`.

### Lecture Notes
Purpose: course notes built from definitions, examples, theorems, proofs, remarks and exercises.
Number environments by section with one shared counter so references stay stable; concrete example before the general statement.
Default visual preset: Kao Textbook or Swiss Minimal.
Reference: `25_lecture_notes.tex`.

### Problem Set / Homework
Purpose: numbered problems with points and answer space; one source compiles the student version or the solutions version (`\solutionstrue`).
Never write solutions that were not supplied or derived and checked.
Reference: `26_problem_set.tex`.

### Lab Report
Purpose: aim, apparatus, procedure as performed, data with units and uncertainty, analysis, conclusion.
Every quantity with unit and uncertainty (`siunitx`); plots read the measured data file.
Reference: `27_lab_report.tex`.

### Literature Review
Purpose: themed synthesis of real, checked sources with a comparison table (`longtable` when it spans pages).
Synthesise across sources instead of summarising them one by one; state search scope and inclusion criteria.
Reference: `28_literature_review.tex`.

### Research Proposal / Grant
Purpose: aims, significance, methods, timeline (`pgfgantt`), budget, risks, impact.
Funders' templates and page limits override this structure. Never invent budget figures, dates or preliminary results.
Reference: `29_research_proposal.tex`.

### Statistical Report
Purpose: descriptive and inferential results from the user's data, with tables aligned on the decimal point and plots read from CSV (`pgfplotstable`).
Numbers come from the analysis software or the data file, never from mental arithmetic. See `references/statistics.md`.
Default visual preset: Modern Report.
Reference: `30_statistical_report.tex`.

### ABNT Academic Work (Brazil)
Purpose: TCC, monografia, dissertação or tese under ABNT NBR 14724, with the `abntex2` class and `abntex2cite` author-date citations.
The class produces cover, title page, abstracts in Portuguese and English, table of contents and the textual/post-textual order. The institution's own manual overrides; keep document text in Portuguese.
Reference: `31_abnt_academic.tex`.

### Response to Reviewers
Purpose: point-by-point reply to journal reviewers: each comment quoted, answered, and tied to the exact change (section, page, line).
Never claim a change that was not made in the manuscript.
Reference: `32_response_to_reviewers.tex`.

## Legal and administrative

### Contract / Legal Document
Purpose: formal contracts, terms, statutes, policies, or other clause-driven legal material.
Architecture: metadata/parties when supplied -> definitions -> numbered clauses/subclauses -> schedules/annexes -> signatures when required.
Preserve supplied legal text exactly unless legal editing was requested. Never invent legal obligations, governing law, parties, dates, or signatures.
The current `contract` package may be used when its semantic legal structures materially help; custom clause environments are acceptable when portability is more important.
Default visual preset: Legal Minimal.
Reference: `13_contract_legal.tex`.

### Form
Purpose: printed or PDF-oriented data collection, checklist, interview, administrative, or evaluation forms.
Optimize label clarity, field size, grouping, completion accuracy, and print reliability. Distinguish static printable fields from interactive PDF forms; do not assume interactivity unless requested.
Default visual preset: Swiss Minimal.
Reference: `22_form.tex`.

## Editorial and visual communication

### Magazine Editorial
Purpose: multi-column editorial publication, newsletter, zine, feature article, catalog-like editorial, or visually rich report.
Use grid, columns, opening hierarchy, pull quotes, captions, image rhythm, and controlled section variation. `flowfram` is a current option when arbitrary flowing frames are genuinely needed; otherwise simpler columns/grids are preferred.
Default visual preset: Magazine Editorial.
Reference: `15_magazine_editorial.tex`.

### Brochure / Flyer
Purpose: compact promotional/informational handout, including tri-fold material.
Prioritize panel logic, fold order, headline hierarchy, contact/action information, and physical print behavior. The `leaflet` class is useful when true two-fold imposition is required, but its accessibility compatibility must be checked.
Default visual preset: Swiss Minimal or Magazine Editorial.
Reference: `16_brochure_flyer.tex`.

### Poster
Purpose: large-format scientific or editorial communication at viewing distance.
Modes:
- Scientific Poster: research question -> method -> results -> interpretation; charts/tables/figures dominate.
- Editorial Poster: one visual hierarchy with strong spatial grouping and minimal text.
Do not shrink body text to fit. Prefer fewer, larger information units.
Possible implementation: custom large-page grid; `flowfram`; `beamerposter` only when its Beamer-based workflow is advantageous and accessibility constraints permit.
Default visual preset: Swiss Minimal or Magazine Editorial.
References: `17a_poster_scientific.tex`, `17b_poster_editorial.tex`.

### Portfolio / Case Study
Purpose: present projects and evidence as a coherent narrative rather than a gallery of decoration.
Typical architecture: project/context -> problem -> constraints -> process -> solution -> evidence/outcome -> reflection when appropriate.
Use images and diagrams as evidence. Keep captions, roles, dates, and outcomes explicit.
Default visual preset: Swiss Minimal with Magazine Editorial traits when appropriate.
Reference: `18_portfolio_case_study.tex`.

## Technical and operational

### Technical Manual
Purpose: durable documentation for systems, software, equipment, protocols, or procedures.
Optimize retrieval, consistency, cross-reference, warnings, notes, code/configuration, diagrams, troubleshooting, and revision lifecycle.
Use semantic components such as Procedure, Warning, Caution, Note, Command, Configuration, Troubleshooting, Reference.
Default visual preset: Swiss Minimal; long-form alternative: Classic Editorial.
Reference: `19_technical_manual.tex`.

### SOP / Procedure
Purpose: controlled operational procedure with explicit scope, prerequisites, ordered actions, verification, exceptions, ownership, versioning, and revision history.
Typical metadata: SOP ID, version, owner, approval/status, effective date when supplied.
Keep procedure steps imperative and testable. Separate verification from execution steps.
Default visual preset: Swiss Minimal or Modern Report.
Reference: `20_sop_procedure.tex`.

### One-Page Reference
Purpose: cheatsheet, command reference, formula sheet, quick-start, process reference, or compact summary optimized for retrieval rather than linear reading.
Use one-, two-, or three-column grid according to content density. Prefer short semantic blocks and lookup-friendly labels. Never compress below comfortable reading size merely to remain on one page.
Default visual preset: Swiss Minimal.
Reference: `21_one_page_reference.tex`.

## Existing special modes

- Interview / individual evaluation: use Form when completion is primary; Assessment Report when evaluation/interpretation is primary.
- Academic paper without venue restrictions: Minimal Research visual preset using a conventional paper architecture.
- Presentation: Minimal Beamer.
- TikZ diagram: treat as information design; establish semantic relationships and hierarchy before drawing.
- Reference sheet: use One-Page Reference.

## Default routing summary

- teaching exercise -> Workbook + Swiss Minimal
- student diagnosis -> Assessment Report + Modern Report
- curriculum -> Course Plan + Swiss Minimal
- long guide -> Book/Guide + Classic Editorial or Kao Textbook
- CV -> Professional CV + Swiss Minimal
- letter -> Formal Letter + Swiss Minimal
- thesis -> Technical Thesis unless classical typography is clearly desired and rules permit Classic Thesis
- executive summary/decision note -> Executive Brief + Swiss Minimal
- memo -> Professional Memo + Swiss Minimal
- proposal -> Proposal + Modern Report
- invoice/quote -> Invoice & Quote + Swiss Minimal
- contract -> Contract/Legal + Legal Minimal
- meeting record -> Meeting Minutes + Swiss Minimal
- magazine/newsletter -> Magazine Editorial + Magazine Editorial
- brochure -> Brochure/Flyer + Swiss Minimal
- poster -> Poster + Swiss Minimal or Magazine Editorial
- portfolio -> Portfolio/Case Study + Swiss Minimal
- manual -> Technical Manual + Swiss Minimal
- SOP -> SOP/Procedure + Swiss Minimal
- cheatsheet -> One-Page Reference + Swiss Minimal
- form -> Form + Swiss Minimal
- paper without venue rules -> Research Article + Minimal Research
- paper for a named venue -> the venue's official kit; Conference Paper only as structure
- course notes -> Lecture Notes + Kao Textbook or Swiss Minimal
- homework / exam with solutions -> Problem Set + Swiss Minimal
- lab write-up -> Lab Report + Swiss Minimal
- literature review -> Literature Review + Minimal Research
- grant or research proposal -> Research Proposal + Classic Editorial or Swiss Minimal
- data analysis write-up -> Statistical Report + Modern Report
- Brazilian TCC, dissertação, tese -> ABNT Academic Work (abntex2)
- journal revision -> Response to Reviewers
