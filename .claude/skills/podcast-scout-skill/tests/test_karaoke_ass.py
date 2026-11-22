"""Karaoke ASS: one cue per word, literal braces, clear error on a malformed words file."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "karaoke_ass.py"
spec = importlib.util.spec_from_file_location("karaoke_ass", SCRIPT)
karaoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(karaoke)


class KaraokeAssTests(unittest.TestCase):
    def run_karaoke(self, folder, words_js):
        srt, words, out = folder / "c.srt", folder / "words.js", folder / "c.ass"
        srt.write_text("1\n00:00:00,000 --> 00:00:01,000\nHello world\n\n"
                       "2\n00:00:01,000 --> 00:00:02,000\nnext {cue}\n", encoding="utf-8")
        words.write_text(words_js, encoding="utf-8")
        log = io.StringIO()
        with contextlib.redirect_stdout(log):
            karaoke.main([str(srt), str(words), "-o", str(out)])
        return log.getvalue(), out.read_text(encoding="utf-8")

    def test_boundary_word_belongs_to_one_cue_and_braces_are_literal(self):
        # "world" ends at 1.1 s: midpoint 0.9 is inside cue 1 but within the old 0.15 s window of cue 2
        words = {"a": [["hello", 0.1, 0.5], ["world", 0.7, 1.1]], "b": [["next", 1.15, 1.5], ["cue", 1.5, 1.9]]}
        with tempfile.TemporaryDirectory() as temp:
            log, ass = self.run_karaoke(Path(temp), "window.WORDS=" + json.dumps(words) + ";\n")
        self.assertIn("2 cues, 2 word-exact, 0 spread", log)
        self.assertIn("\\{cue\\}", ass)
        self.assertNotIn("}{cue}", ass)

    def test_malformed_words_file_is_a_clear_error(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(SystemExit) as caught:
                self.run_karaoke(Path(temp), "window.WORDS = not json at all")
        self.assertIn("is not window.WORDS", str(caught.exception.code))


if __name__ == "__main__":
    unittest.main()
