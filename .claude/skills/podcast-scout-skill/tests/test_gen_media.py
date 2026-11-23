"""gen_media.py: plan by default, validated batch specs, https-only downloads, clean network errors. No network."""
import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("gen_media", SCRIPTS / "gen_media.py")
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)

NO_NETWORK = urllib.error.URLError("network disabled in tests")


class GenMediaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        net =patch("urllib.request.urlopen", side_effect=NO_NETWORK)
        self.urlopen = net.start()
        self.addCleanup(net.stop)

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gm.main(list(argv))
        return code, out.getvalue()

    def batch(self, specs):
        path = self.tmp / "plates.json"
        path.write_text(json.dumps(specs), encoding="utf-8")
        return str(path)

    def test_bare_run_is_plan_only(self):
        code, out = self.main("--batch", self.batch({"sky": {"prompt": "a sky"}}), "--out-dir", str(self.tmp))
        self.assertEqual(code, 0)
        self.assertIn("dry run", out)
        self.urlopen.assert_not_called()  # not even the balance check

    def test_unsafe_batch_entries_rejected_before_any_request(self):
        for specs in ({"../../escape": {"prompt": "x"}},
                      {"ok": {"prompt": "x", "ext": "png/../../x"}},
                      {"ok": {"prompt": "x", "model": "../account/balance"}},
                      {"ok": {"prompt": "x", "model": "flux/./dev"}}):
            with self.assertRaises(SystemExit) as caught, contextlib.redirect_stderr(io.StringIO()):
                gm.main(["--batch", self.batch(specs), "--generate"])
            self.assertEqual(caught.exception.code, 2, specs)
        self.urlopen.assert_not_called()

    def test_over_max_jobs_refuses_before_balance_call(self):
        specs = {f"p{i}": {"prompt": "x"} for i in range(3)}
        with self.assertRaisesRegex(SystemExit, "max-jobs"), contextlib.redirect_stdout(io.StringIO()):
            gm.main(["--batch", self.batch(specs), "--generate", "--max-jobs", "2"])
        self.urlopen.assert_not_called()

    def test_base_must_be_https(self):
        with patch.object(gm, "BASE", "http://api.muapi.ai"), self.assertRaises(SystemExit), \
                contextlib.redirect_stderr(io.StringIO()):
            gm.main(["--prompt", "x", "--out", str(self.tmp / "a.png")])

    def test_network_error_is_a_clean_exit(self):
        with self.assertRaisesRegex(SystemExit, "network disabled"):
            gm.balance("test-key-not-real")

    def test_result_url_must_be_https(self):
        result = {"outputs": ["file:///etc/passwd"], "cost": {"amount_usd": 0.01}}
        with patch.object(gm, "generate", return_value=result), self.assertRaisesRegex(SystemExit, "unsafe"):
            gm.one("a", {"prompt": "x"}, str(self.tmp / "a.png"), "test-key-not-real")
        self.assertFalse((self.tmp / "a.png").exists())


if __name__ == "__main__":
    unittest.main()
