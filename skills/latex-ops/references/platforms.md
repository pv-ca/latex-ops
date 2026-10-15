# Platforms and TeX distributions

Read when `scripts/check_env.py` reports a problem, when a build fails for a reason outside the document (missing package, font, program), or when the user works on Windows, with MiKTeX, or on Overleaf.

## Distributions

| Distribution | Package manager | Notes |
| --- | --- | --- |
| TeX Live (upstream installer, any OS) | `tlmgr install <pkg>` | Recommended. Includes Perl on Windows, `latexmk`, `texlogsieve` and the template fonts (`inter`, `libertinus-fonts`, `lm`) |
| TinyTeX | `tlmgr install <pkg>` | Small TeX Live; installs per user, no administrator rights. Best choice when nothing is installed |
| TeX Live from a Linux distribution (apt, dnf, pacman, zypper) | the system package manager | `tlmgr` is absent or disabled; use the system command `check_env.py --install` prints. Fedora maps files directly: `dnf install 'tex(scrartcl.cls)'` |
| MiKTeX (mostly Windows) | `miktex packages install <pkg>` or the MiKTeX Console | Installs missing `.sty`/`.cls` on the fly when that option is on, but **not** fonts requested by name through `fontspec`: install `inter`, `libertinus-fonts` and `lm` before using the templates. `latexmk` needs a separate Perl (Strawberry Perl) |
| Overleaf | the project menu | The compiler (pdfLaTeX, XeLaTeX, LuaLaTeX) and TeX Live year are chosen in project settings; a `latexmkrc` in the project is honoured. Nothing can be installed |

Installing software changes the user's machine: show the command from `check_env.py --install` and run it with `--yes` only after the user agrees.

## Windows

- Run the scripts with `python` or `py` (the `python3` name often does not exist).
- In LaTeX sources use forward slashes in paths (`\includegraphics{img/fig.pdf}`); avoid spaces and non-ASCII characters in file names the document loads.
- The first LuaLaTeX run after installing fonts builds the font cache and can take minutes; it is not a hang.
- Ghostscript ships hidden inside TeX Live for Windows; `rungs` reaches it, and `scripts/preview.py` tries it after `pdftoppm` and `mutool`.
- Antivirus software sometimes locks the PDF being rewritten; if a rebuild fails with a permission error, close the PDF viewer and retry.

## Engines

- LuaLaTeX: default for new documents (Unicode, OpenType fonts, tagged PDF). Slower than pdfLaTeX.
- XeLaTeX: Unicode and system fonts; use when a class or venue asks for it.
- pdfLaTeX: required by many journal and conference classes; no `fontspec` or `unicode-math`.
- A magic comment on the first lines selects the engine for `build.py`: `% !TEX program = xelatex`. Editor support varies. On Overleaf, select the compiler explicitly in project settings; the comment is only a reminder. See [Overleaf compiler settings](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler).

## Fonts

The templates use Inter, Libertinus and Latin Modern, all distributed with TeX. If one is missing and cannot be installed, replace it in the preamble with a font that is present (for example `Latin Modern Sans` for Inter) and say so; do not leave a document that only compiles on one machine.
