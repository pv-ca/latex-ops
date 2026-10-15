"""Opt-in real TeX regression cases. Set LATEX_OPS_INTEGRATION=1 to require them."""
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills' / 'latex-ops' / 'scripts'))
import build
import check_env


@unittest.skipUnless(os.environ.get('LATEX_OPS_INTEGRATION') == '1', 'real TeX checks are opt-in')
class RealBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = ('pdflatex', 'latexmk', 'bibtex', 'biber', 'makeindex', 'kpsewhich')
        missing = [name for name in required if not shutil.which(name)]
        if missing:
            raise AssertionError('required integration tools missing: ' + ', '.join(missing))

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='latex-ops-integration-')
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / 'source files'
        self.source.mkdir()
        self.out = self.root / 'output files'
        self.tex = self.source / 'paper.v1.tex'
        (self.source / 'data').mkdir()
        (self.source / 'data' / 'refs.bib').write_text(
            '@book{example,author={Example Author},title={Fixture Book},year={2020}}', encoding='utf-8')

    def compile(self, text, latexmk=False, trust=False):
        self.tex.write_text(text, encoding='utf-8')
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code, log = build.build(self.tex, 'pdflatex', self.out, False, 90,
                                    use_latexmk=latexmk, trust_project_config=trust)
        self.assertEqual(code, 0, output.getvalue() + '\n' + build._read(log)[-3000:])
        report = build.parse_log(build._read(log))
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['undefined_refs'], [])
        self.assertEqual(report['undefined_cites'], [])
        self.assertFalse(report['needs_rerun'])
        self.assertTrue((self.out / (self.tex.stem + '.pdf')).is_file())

    def bibliography(self, backend, latexmk=False):
        if backend == 'biber':
            preamble = r'\usepackage[backend=biber]{biblatex}\addbibresource{data/refs.bib}'
            tail = r'\printbibliography'
        else:
            preamble = ''
            tail = r'\bibliographystyle{plain}\bibliography{data/refs}'
        self.compile(r'\documentclass{article}' + preamble + r'\begin{document}\cite{example}' + tail + r'\end{document}', latexmk)
        self.assertIn('Fixture Book', (self.out / (self.tex.stem + '.bbl')).read_text(encoding='utf-8'))

    def test_bibtex_fallback_with_separate_output(self):
        self.bibliography('bibtex')

    def test_biber_fallback_with_separate_output(self):
        self.bibliography('biber')

    def test_bibtex_latexmk_with_separate_output(self):
        self.bibliography('bibtex', True)

    def test_biber_latexmk_with_separate_output(self):
        self.bibliography('biber', True)

    def test_index_fallback(self):
        self.compile(r'\documentclass{article}\usepackage{makeidx}\makeindex\begin{document}Term\index{term}\printindex\end{document}')
        self.assertIn('term', (self.out / (self.tex.stem + '.ind')).read_text())

    def test_spaces_and_cross_references(self):
        self.tex = self.source / 'paper draft.v1.tex'
        self.compile(r'\documentclass{article}\begin{document}\section{One}\label{one}See \ref{one}.\end{document}')

    def test_multipart_sources_and_citations(self):
        (self.source / 'chapter.tex').write_text(r'\section{One}\label{one}See \cite{example}.', encoding='utf-8')
        self.compile(r'\documentclass{article}\begin{document}\input{chapter}See \ref{one}.\bibliographystyle{plain}\bibliography{data/refs}\end{document}')

    def test_untrusted_rc_is_not_loaded(self):
        (self.source / '.latexmkrc').write_text('die "CONFIG_CANARY_LOADED";\n', encoding='utf-8')
        self.compile(r'\documentclass{article}\begin{document}Test\end{document}', True)

    def test_trusted_rc_is_explicitly_loaded(self):
        (self.source / '.latexmkrc').write_text('die "CONFIG_CANARY_LOADED";\n', encoding='utf-8')
        self.tex.write_text(r'\documentclass{article}\begin{document}Test\end{document}', encoding='utf-8')
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code, _ = build.build(self.tex, 'pdflatex', self.out, False, 90, trust_project_config=True)
        self.assertNotEqual(code, 0)
        self.assertIn('CONFIG_CANARY_LOADED', output.getvalue())
