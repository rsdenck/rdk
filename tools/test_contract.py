import re
import sys
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from validate import SEMVER, load_json

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F]")
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py"}


class ContractTest(unittest.TestCase):
    def setUp(self):
        self.errors = []
        self.version = (ROOT / "VERSION").read_text().strip()

    def json_file(self, path):
        return load_json(ROOT / path, self.errors)

    def test_version_is_semver(self):
        self.assertRegex(self.version, SEMVER)

    def test_schema_index_matches_files(self):
        index = self.json_file("schema/index.json")
        self.assertEqual(index["version"], self.version)
        self.assertEqual(index["major"], int(self.version.split(".", 1)[0]))
        files = {path.name for path in (ROOT / "schema").glob("*.json") if path.name != "index.json"}
        indexed = {row["file"] for row in index["schemas"]}
        self.assertEqual(files, indexed)
        for row in index["schemas"]:
            self.assertIn(f"/v{index['major']}/", row["id"])

    def test_version_history_latest_entry(self):
        history = yaml.safe_load((ROOT / "registry/version-history.yaml").read_text())
        self.assertEqual(history["protocol"], "rdk")
        self.assertEqual(history["versions"][0]["version"], self.version)
        self.assertEqual(history["versions"][0]["status"], "active")

    def test_catalogs_are_unique(self):
        operations = yaml.safe_load((ROOT / "registry/operations.yaml").read_text())
        codes = yaml.safe_load((ROOT / "registry/error-codes.yaml").read_text())
        operation_keys = [(row["id"], row["version"]) for row in operations["operations"]]
        code_values = [row["code"] for row in codes["codes"]]
        self.assertEqual(len(operation_keys), len(set(operation_keys)))
        self.assertEqual(len(code_values), len(set(code_values)))

    def test_valid_examples_pass_schemas(self):
        envelope = self.json_file("schema/rdk-envelope.schema.json")
        for path in sorted((ROOT / "examples").glob("*.json")):
            with self.subTest(example=path.name):
                data = self.json_file(path.relative_to(ROOT))
                schema = self.json_file(f"schema/{data['type']}.schema.json")
                self.assertFalse(list(Draft202012Validator(schema).iter_errors(data)))
                self.assertFalse(list(Draft202012Validator(envelope).iter_errors(data)))
                self.assertEqual(data["spec_version"], self.version)

    def test_invalid_examples_are_rejected(self):
        envelope = self.json_file("schema/rdk-envelope.schema.json")
        paths = sorted((ROOT / "examples/invalid").glob("*.json"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(example=path.name):
                data = self.json_file(path.relative_to(ROOT))
                schema = self.json_file(f"schema/{data['type']}.schema.json")
                rejected = data.get("spec_version") != self.version
                rejected = rejected or bool(list(Draft202012Validator(schema).iter_errors(data)))
                rejected = rejected or bool(list(Draft202012Validator(envelope).iter_errors(data)))
                self.assertTrue(rejected)

    def test_no_emoji_or_em_dash(self):
        paths = []
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if ".git" in path.parts:
                continue
            if path.suffix in TEXT_SUFFIXES or path.name in {"VERSION", "Makefile", "CODEOWNERS"}:
                paths.append(path)
        self.assertTrue(paths)
        for path in paths:
            text = path.read_text()
            with self.subTest(file=path.relative_to(ROOT)):
                self.assertNotIn("\u2014", text)
                self.assertIsNone(EMOJI.search(text))


if __name__ == "__main__":
    unittest.main(verbosity=2)
