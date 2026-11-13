"""The owner-supplied voice is the channel narrator when available; the synthetic voice is only a fallback."""
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import narrate

OWNER = {"name": narrate.OWNER_NARRATOR_NAME, "id": "owner-1", "sample_count": 1}
SYNTH = {"name": narrate.CHANNEL_NARRATOR_NAME, "id": "synth-1", "sample_count": 1}


class ChannelNarrator(unittest.TestCase):
    def test_owner_profile_wins(self):
        self.assertEqual(narrate.pick_channel_profile([SYNTH, OWNER], False), ("owner-1", "owner"))

    def test_owner_reference_without_profile_is_created(self):
        self.assertEqual(narrate.pick_channel_profile([SYNTH], True), (None, "owner"))

    def test_synthetic_fallback(self):
        self.assertEqual(narrate.pick_channel_profile([SYNTH], False), ("synth-1", "synthetic"))
        self.assertEqual(narrate.pick_channel_profile([], False), (None, "synthetic"))

    def test_profile_without_samples_is_ignored(self):
        self.assertEqual(narrate.pick_channel_profile([dict(OWNER, sample_count=0)], False), (None, "synthetic"))

    def test_owner_reference_is_not_tracked_in_git(self):
        self.assertIn("voice/local/", (Path(__file__).resolve().parents[4] / ".gitignore").read_text())


if __name__ == "__main__":
    unittest.main()
