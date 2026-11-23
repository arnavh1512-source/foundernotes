"""Malformed JSON shapes must give a ValueError/FAIL report, never an AttributeError."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


backends = load("animation_backends")
lemo = load("lemo_backend")


class ShapeGuards(unittest.TestCase):
    def test_import_recipe_and_provenance_must_be_objects(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scene.mp4").write_bytes(b"fixture")
            for recipe in ([], "scene.mp4",
                           {"backend": "opentoonz", "picture": "scene.mp4", "picture_provenance": "mine"}):
                with self.subTest(recipe=recipe), self.assertRaises(ValueError):
                    backends.validate_import(recipe, root)

    def test_malformed_lemo_catalog_is_a_fail_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for file in ("core/render/video.mjs", "core/render/still.mjs", "styles/README.md"):
                (root / file).parent.mkdir(parents=True, exist_ok=True)
                (root / file).write_text("x", encoding="utf-8")
            for catalog in ([], {"styles": ["watercolor"]}, {"styles": {"slug": "x"}}):
                bad = root / "catalog.json"
                bad.write_text(json.dumps(catalog), encoding="utf-8")
                with self.subTest(catalog=catalog), patch.object(lemo, "CATALOG", bad), \
                     patch.object(lemo.shutil, "which", return_value="/bin/exe"):
                    with self.assertRaises(ValueError):
                        lemo.known_styles()
                    result = lemo.execute("render", library=root, style="watercolor",
                                          project=root, output=root / "out.mp4")
                    self.assertEqual(result["error"], "BAD_STYLE_CATALOG")


if __name__ == "__main__":
    unittest.main()
