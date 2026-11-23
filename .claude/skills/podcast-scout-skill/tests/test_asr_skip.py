"""Without faster-whisper the ASR check is skipped cleanly and leaves no report behind."""
import sys, tempfile, unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import narrate


class AsrSkip(unittest.TestCase):
    def test_missing_whisper_skips_and_removes_stale_report(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(sys.modules, {"faster_whisper": None}):
            out = Path(d); (out / "asr.json").write_text("[]")
            self.assertIsNone(narrate.asr_check(out, [], "base.en"))
            self.assertFalse((out / "asr.json").exists())


if __name__ == "__main__":
    unittest.main()
