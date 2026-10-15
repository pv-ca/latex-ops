"""Check that every plugin entrypoint resolves the same shipped skill."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class Packaging(unittest.TestCase):
    def test_compatibility_manifests_share_identity_and_version(self):
        portable = read("plugin.json")
        self.assertEqual(portable["$schema"],
                         "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        for name in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
            manifest = read(name)
            for field in ("name", "version", "license", "repository"):
                self.assertEqual(manifest[field], portable[field], (name, field))
        self.assertNotIn("skills", portable)

    def test_skill_metadata_matches_plugin_version(self):
        text = (ROOT / "skills/latex-ops/SKILL.md").read_text(encoding="utf-8")
        version = re.search(r'^  version: "([^"\n]+)"$', text, re.M)
        self.assertIsNotNone(version)
        self.assertEqual(version.group(1), read("plugin.json")["version"])

    def test_each_host_discovers_only_the_shipped_skill(self):
        expected = ROOT / "skills" / "latex-ops" / "SKILL.md"
        claude = read(".claude-plugin/plugin.json")
        self.assertEqual([ROOT / p / "SKILL.md" for p in claude["skills"]], [expected])
        codex = read(".codex-plugin/plugin.json")
        self.assertEqual(list((ROOT / codex["skills"]).glob("*/SKILL.md")), [expected])
        self.assertTrue(expected.is_file())
        for directory in ("assets", "scripts", "references"):
            self.assertTrue((expected.parent / directory).is_dir())

    def test_marketplace_resolves_the_local_plugin(self):
        marketplace = read(".claude-plugin/marketplace.json")
        self.assertEqual(marketplace["name"], "pvca-latex")
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], read("plugin.json")["name"])
        self.assertEqual((ROOT / entry["source"]).resolve(), ROOT)
