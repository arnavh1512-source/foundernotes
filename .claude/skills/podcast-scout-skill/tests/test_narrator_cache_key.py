"""The owner-narrator cache key is stable (matches takes stamped with the alias); the synthetic fallback never matches."""
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import narrate


class NarratorCacheKey(unittest.TestCase):
    def test_owner_key_is_the_alias(self):
        self.assertEqual(narrate.narrator_cache_key("owner"), narrate.CHANNEL_NARRATOR)

    def test_synthetic_key_differs_from_owner(self):
        self.assertNotEqual(narrate.narrator_cache_key("synthetic"), narrate.narrator_cache_key("owner"))
        self.assertNotEqual(narrate.narrator_cache_key(None), narrate.narrator_cache_key("owner"))


if __name__ == "__main__":
    unittest.main()
