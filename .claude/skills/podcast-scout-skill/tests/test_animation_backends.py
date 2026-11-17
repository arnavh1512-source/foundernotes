import importlib.util
from pathlib import Path
import tempfile
import unittest
SCRIPT = Path(__file__).resolve().parents[1] / "scripts/animation_backends.py"
spec = importlib.util.spec_from_file_location("animation_backends", SCRIPT)
backend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend)

class BackendTests(unittest.TestCase):
    def test_every_requested_tool_is_routed_without_claiming_installation(self):
        self.assertEqual(set(backend.catalog()), {"painted-character-motion","remotion","synfig","friction","theatre","opentoonz","freemocap","effekseer","openvdb","natron"})
        self.assertEqual(backend.catalog()["opentoonz"]["status"], "optional-external")

    def test_import_requires_real_media_path_and_rights(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scene.mp4").write_bytes(b"test fixture only")
            recipe = {"backend":"opentoonz","picture":"scene.mp4","picture_provenance":{"rights_verified":True,"creator":"artist","source":"original project","license":"original","export_method":"manual export"}}
            self.assertEqual(backend.validate_import(recipe,root), root / "scene.mp4")
            recipe["picture"] = "../escape.mp4"
            with self.assertRaises(ValueError):
                backend.validate_import(recipe,root)
            recipe["picture"] = "scene.mp4"
            recipe["picture_provenance"]["rights_verified"] = False
            with self.assertRaises(ValueError):
                backend.validate_import(recipe,root)

if __name__ == "__main__":
    unittest.main()

