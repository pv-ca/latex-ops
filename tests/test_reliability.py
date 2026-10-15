"""Regression tests for build results, configuration trust and fresh previews."""
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills' / 'latex-ops' / 'scripts'))
import build
import check_env
import preview


class BuildFlow(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.tex = self.source / 'paper.v1.tex'
        self.tex.write_text(r'\documentclass{article}', encoding='utf-8')
        self.out = self.root / 'output'
        self.out.mkdir()
        self.backend = None
        self.backend_code = 0
        self.index = False
        self.unstable = False
        self.write_pdf = True
        self.calls = []
        self.missing = set()
        self.addCleanup(patch.stopall)
        patch.object(build, 'latexmk_usable', return_value=None).start()
        patch.object(build.shutil, 'which', side_effect=lambda name: None if name in self.missing else '/mock/' + name).start()
        patch.object(build, 'run', side_effect=self.execute).start()

    def artifact(self, extension):
        return self.out / (self.tex.stem + extension)

    def execute(self, command, cwd, timeout, env=None):
        program = Path(command[0]).name
        self.calls.append((program, command, Path(cwd), env))
        if program in ('lualatex', 'latexmk'):
            if self.write_pdf:
                pdf = self.artifact('.pdf')
                before = pdf.stat().st_mtime_ns if pdf.exists() else 0
                pdf.write_bytes(b'new PDF')
                if before:
                    os.utime(str(pdf), ns=(before + 1000000000, before + 1000000000))
            self.artifact('.log').write_text('Rerun to get cross-references right.' if self.unstable else 'Output written', encoding='utf-8')
            if self.backend == 'biber':
                self.artifact('.bcf').write_text('control', encoding='utf-8')
            self.artifact('.aux').write_text(r'\bibdata{refs}' if self.backend == 'bibtex' else '', encoding='utf-8')
            if self.index:
                self.artifact('.idx').write_text(r'\indexentry{term}{1}', encoding='utf-8')
            return 0
        if program in ('biber', 'bibtex'):
            if self.backend_code == 0:
                self.artifact('.bbl').write_text('bibliography', encoding='utf-8')
            return self.backend_code
        if program == 'makeindex':
            if self.backend_code == 0:
                self.artifact('.ind').write_text('index', encoding='utf-8')
            return self.backend_code
        raise AssertionError(command)

    def compile(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return build.build(self.tex, 'lualatex', self.out, False, 5, **kwargs)

    def test_biber_failure_is_not_success(self):
        self.backend, self.backend_code = 'biber', 2
        self.assertNotEqual(self.compile()[0], 0)

    def test_bibtex_failure_is_not_success(self):
        self.backend, self.backend_code = 'bibtex', 2
        self.assertNotEqual(self.compile()[0], 0)

    def test_missing_biber_is_a_failure(self):
        self.backend = 'biber'
        self.missing.add('biber')
        self.assertNotEqual(self.compile()[0], 0)

    def test_missing_bibtex_is_a_failure(self):
        self.backend = 'bibtex'
        self.missing.add('bibtex')
        self.assertNotEqual(self.compile()[0], 0)

    def test_biber_uses_complete_job_name_and_source_search_path(self):
        self.backend = 'biber'
        self.assertEqual(self.compile()[0], 0)
        calls = [c for c in self.calls if c[0] == 'biber']
        self.assertEqual(len(calls), 1)
        self.assertIn(self.tex.stem, calls[0][1])
        self.assertIn(str(self.source), calls[0][3]['BIBINPUTS'])

    def test_bibtex_uses_complete_job_name_and_source_search_path(self):
        self.backend = 'bibtex'
        self.assertEqual(self.compile()[0], 0)
        calls = [c for c in self.calls if c[0] == 'bibtex']
        self.assertEqual(len(calls), 1)
        self.assertIn(self.tex.stem, calls[0][1])
        self.assertIn(str(self.source), calls[0][3]['BIBINPUTS'])
        self.assertIn(str(self.source), calls[0][3]['BSTINPUTS'])

    def test_nonempty_index_runs_makeindex(self):
        self.index = True
        self.assertEqual(self.compile()[0], 0)
        call = next(c for c in self.calls if c[0] == 'makeindex')
        self.assertEqual(call[2], self.out)
        self.assertEqual(call[1][1:], ['-o', 'paper.v1.ind', 'paper.v1.idx'])
        self.assertTrue(self.artifact('.ind').exists())

    def test_makeindex_failure_is_not_success(self):
        self.index, self.backend_code = True, 2
        self.assertNotEqual(self.compile()[0], 0)

    def test_missing_makeindex_is_a_failure(self):
        self.index = True
        self.missing.add('makeindex')
        self.assertNotEqual(self.compile()[0], 0)

    def test_unsettled_references_are_a_failure(self):
        self.unstable = True
        self.assertNotEqual(self.compile()[0], 0)

    def test_preexisting_pdf_cannot_prove_new_build_success(self):
        self.artifact('.pdf').write_bytes(b'old PDF')
        self.write_pdf = False
        self.assertNotEqual(self.compile()[0], 0)
        self.assertEqual(self.artifact('.pdf').read_bytes(), b'old PDF')

    def test_current_pdf_is_required(self):
        self.write_pdf = False
        self.assertNotEqual(self.compile()[0], 0)

    def test_stale_backend_control_is_ignored(self):
        self.artifact('.bcf').write_text('old biblatex project', encoding='utf-8')
        self.assertEqual(self.compile()[0], 0)
        self.assertFalse(any(c[0] == 'biber' for c in self.calls))

    def test_latexmk_disables_rc_by_default(self):
        build.latexmk_usable.return_value = '/mock/latexmk'
        self.assertEqual(self.compile()[0], 0)
        self.assertIn('-norc', self.calls[0][1])

    def test_latexmk_trust_must_be_explicit(self):
        build.latexmk_usable.return_value = '/mock/latexmk'
        self.assertEqual(self.compile(trust_project_config=True)[0], 0)
        self.assertNotIn('-norc', self.calls[0][1])

    def test_latexmk_rebuilds_instead_of_reusing_pdf(self):
        build.latexmk_usable.return_value = '/mock/latexmk'
        self.artifact('.pdf').write_bytes(b'old PDF')
        self.assertEqual(self.compile()[0], 0)
        self.assertIn('-g', self.calls[0][1])


class Probes(unittest.TestCase):
    def test_build_probe_does_not_read_rc(self):
        with patch.object(build.shutil, 'which', return_value='/mock/latexmk'), patch.object(build.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as execute:
            self.assertIsNotNone(build.latexmk_usable())
        self.assertIn('-norc', execute.call_args[0][0])

    def test_environment_probe_does_not_read_rc(self):
        with patch.object(check_env, 'run', return_value=(0, 'version')) as execute:
            self.assertTrue(check_env.latexmk_works({'latexmk': '/mock/latexmk'}))
        self.assertIn('-norc', execute.call_args[0][0])

    def test_biblatex_bibtex_repeat_request_is_reported(self):
        self.assertTrue(build.parse_log('Please (re)run BibTeX on the file:')['needs_rerun'])

    def test_biblatex_citation_warning_is_reported(self):
        self.assertEqual(build.parse_log("LaTeX Warning: Citation 'missing' on page 1 undefined.")['undefined_cites'], ['missing'])


class Preview(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.pdf = self.root / 'paper.v1.pdf'
        self.pdf.write_bytes(b'PDF')
        self.png = self.root / 'paper.v1-p1.png'

    def render(self, execute, *options):
        with patch.object(preview, 'find_renderer', return_value=('pdftoppm', '/mock/pdftoppm')), patch.object(preview.subprocess, 'run', side_effect=execute), contextlib.redirect_stdout(io.StringIO()):
            return preview.main([str(self.pdf)] + list(options))

    def test_stale_png_does_not_prove_success(self):
        self.png.write_bytes(b'old PNG')
        self.assertEqual(self.render(lambda *a, **kw: subprocess.CompletedProcess([], 0, '', '')), 1)
        self.assertEqual(self.png.read_bytes(), b'old PNG')

    def test_failure_preserves_previous_preview(self):
        self.png.write_bytes(b'old PNG')
        self.assertEqual(self.render(lambda *a, **kw: subprocess.CompletedProcess([], 1, '', 'failed')), 1)
        self.assertEqual(self.png.read_bytes(), b'old PNG')

    def test_timeout_is_reported(self):
        def execute(command, **kwargs):
            raise subprocess.TimeoutExpired(command, kwargs['timeout'])
        self.assertEqual(self.render(execute, '--timeout', '1'), 1)

    def test_missing_renderer_executable_is_reported(self):
        def execute(*a, **kw):
            raise FileNotFoundError('renderer disappeared')
        self.assertEqual(self.render(execute), 1)

    def test_successful_render_is_promoted(self):
        def execute(command, **kwargs):
            Path(command[-1] + '.png').write_bytes(b'new PNG')
            return subprocess.CompletedProcess(command, 0, '', '')
        self.assertEqual(self.render(execute), 0)
        self.assertEqual(self.png.read_bytes(), b'new PNG')

    def test_pdftoppm_keeps_dotted_output_name(self):
        command = preview.commands('pdftoppm', 'pdftoppm', self.pdf, 1, 60, self.png)
        self.assertEqual(command[-1], str(self.root / 'paper.v1-p1'))
