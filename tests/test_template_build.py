"""Regression checks for the compile-and-render CI gate."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_templates


class Gallery(unittest.TestCase):
    def test_render_failure_fails_the_gate(self):
        self.check_gallery(1, False, 1)

    def test_missing_image_fails_even_when_renderer_reports_success(self):
        self.check_gallery(0, False, 1)

    def test_successful_render_produces_named_gallery_image(self):
        self.check_gallery(0, True, 0)

    def check_gallery(self, render_code, write_image, expected):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tex = root / "source" / "sample.tex"
            tex.parent.mkdir()
            tex.write_text(r"\documentclass{article}", encoding="utf-8")

            def compile_pdf(copy, *args):
                copy.with_suffix(".pdf").write_bytes(b"test PDF")
                return 0, copy.with_suffix(".log")

            def render(argv):
                if write_image:
                    (root / "gallery" / "sample-p1.png").write_bytes(b"test PNG")
                return render_code

            with patch.object(build_templates, "templates", return_value=[tex]), \
                 patch.object(build_templates.build, "build", side_effect=compile_pdf), \
                 patch.object(build_templates.preview, "main", side_effect=render), \
                 contextlib.redirect_stdout(io.StringIO()):
                result = build_templates.main(["--workdir", str(root / "build"),
                                               "--gallery", str(root / "gallery")])
            self.assertEqual(result, expected)
            if expected == 0:
                self.assertTrue((root / "gallery" / "source-sample.png").is_file())
