import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "latex-ops" / "scripts"))
import build  # noqa: E402
import check_env  # noqa: E402
import preview  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def log(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


class Requirements(unittest.TestCase):
    def test_every_line_has_name_and_probe(self):
        reqs = check_env.read_requirements()
        names = [n for n, _ in reqs]
        self.assertGreater(len(reqs), 50)
        self.assertEqual(len(names), len(set(names)))
        for name, probe in reqs:
            self.assertTrue(probe.startswith("bin:") or "." in probe, (name, probe))

    def test_install_plan_per_distribution(self):
        reqs = [("inter", "Inter-Regular.otf"), ("latexmk", "bin:latexmk")]
        cmd, _ = check_env.install_plan("tinytex", ["inter"], reqs)
        self.assertEqual(cmd, ["tlmgr", "install", "inter"])
        cmd, _ = check_env.install_plan("miktex", ["inter"], reqs)
        self.assertEqual(cmd, ["miktex", "packages", "install", "inter"])
        cmd, advice = check_env.install_plan("none", [], reqs)
        self.assertIsNone(cmd)
        self.assertIn("TinyTeX", advice)
        cmd, advice = check_env.install_plan("texlive-system", ["inter"], reqs)
        self.assertIsNone(cmd)  # never runs sudo itself
        self.assertEqual(check_env.install_plan("texlive", [], reqs), (None, "Nothing to install."))


class LogParsing(unittest.TestCase):
    def test_wrapped_package_error_is_joined(self):
        report = build.parse_log(log("bad.log"))
        self.assertEqual(len(report["errors"]), 1)
        self.assertIn("fontspec package requires either XeTeX or LuaTeX", report["errors"][0])
        self.assertIn("lualatex", report["errors"][0])

    def test_unbalanced_environment(self):
        report = build.parse_log(log("env.log"))
        self.assertIn("ended by \\end{document}", report["errors"][0])
        self.assertIn("env.tex:5:", report["errors"][0])

    def test_undefined_reference(self):
        report = build.parse_log(log("ref.log"))
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["undefined_refs"], ["nope"])

    def test_overfull_and_glyphs(self):
        text = ("Overfull \\hbox (12.5pt too wide) in paragraph at lines 3--4\n"
                "Overfull \\hbox (0.3pt too wide) in paragraph at lines 7--8\n"
                "Missing character: There is no ç in font cmr10!\n")
        report = build.parse_log(text)
        self.assertEqual(report["overfull_over_1pt"], 1)
        self.assertEqual(report["worst_overfull_pt"], 12.5)
        self.assertEqual(report["missing_glyphs"], ["ç"])

    def test_unwrap_only_joins_79_char_lines(self):
        self.assertEqual(build.unwrap("a" * 79 + "\nb\nc"), ["a" * 79 + "b", "c"])


class Engine(unittest.TestCase):
    def test_magic_comment(self):
        self.assertEqual(build.choose_engine("% !TEX program = xelatex\n\\documentclass{article}"), "xelatex")
        self.assertEqual(build.choose_engine("% !TEX TS-program = pdflatex\n"), "pdflatex")
        self.assertEqual(build.choose_engine("\\documentclass{article}"), "lualatex")


class Pages(unittest.TestCase):
    def test_parse_pages(self):
        self.assertEqual(preview.parse_pages("1,3-4,3"), [1, 3, 4])
        with self.assertRaises(ValueError):
            preview.parse_pages("0")


if __name__ == "__main__":
    unittest.main()
