"""package_lint: bad input fails cleanly, and the owner's package rule (thumbnail, chapters, sources) is enforced."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "package_lint.py"
spec = importlib.util.spec_from_file_location("package_lint", SCRIPT)
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


def good():
    return {"titles": ["You Read It. Can You Explain It?", "Rereading Feels Like Learning"],
            "thumbnails": [{"title_index": 0, "text": "BLANK PAGE", "focal": "empty speech bubble"}],
            "description": "Explaining beats rereading for spotting gaps.\n0:00 Test\n0:41 Why\n10:00 How\n\n"
                           "Sources:\nhttps://example.org/a\nhttps://example.org/b",
            "chapters": [["00:00", "Test"], ["00:41", "Why"], ["10:00", "How"]], "tags": ["study"],
            "sources": ["https://example.org/a", "https://example.org/b"]}


class PackageLintTests(unittest.TestCase):
    def run_lint(self, text):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "p.json"
            p.write_text(text if isinstance(text, str) else json.dumps(text), encoding="utf-8")
            log = io.StringIO()
            with contextlib.redirect_stdout(log):
                code = lint.main([str(p), "--duration", "700"])
            return code, log.getvalue()

    def test_good_package_passes(self):
        code, log = self.run_lint(good())
        self.assertEqual(code, 0, log)

    def test_each_defect_fails_without_traceback(self):
        def variant(**changes):
            pkg = good(); pkg.update(changes); return pkg
        desc = good()["description"]
        cases = {
            "malformed json": "{not json",
            "top-level list": [],
            "non-dict thumbnail": variant(thumbnails=["BLANK PAGE"]),
            "non-string thumbnail text": variant(thumbnails=[{"text": 5, "focal": "x"}]),
            "non-string tag": variant(tags=["ok", 7]),
            "non-string source": variant(sources=[None]),
            "whitespace description": variant(description="   \n  "),
            "one of two sources listed": variant(description=desc.replace("https://example.org/b", "")),
            "0:00 only inside 10:00": variant(description=desc.replace("0:00 Test\n", "Intro at 10:00 Test\n")),
            "eleven titles": variant(titles=[f"Title number {i}" for i in range(11)]),
            "no thumbnails": variant(thumbnails=[]),
            "no chapters": variant(chapters=[]),
        }
        for name, pkg in cases.items():
            with self.subTest(name):
                code, log = self.run_lint(pkg)
                self.assertEqual(code, 1, log)
                self.assertIn("FAIL", log)


if __name__ == "__main__":
    unittest.main()
