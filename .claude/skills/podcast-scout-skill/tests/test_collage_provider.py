"""run_jobs must not buy the same job twice just because it is slow."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "collage-director" / "scripts"))
import provider  # noqa: E402


class FakeProvider:
    def __init__(self, statuses):
        self.statuses = iter(statuses)

    def get_status(self, job_id):
        return {"status": next(self.statuses), "output": "https://example.invalid/out.mp4", "error": "boom"}


class RunJobsTests(unittest.TestCase):
    def run_one(self, statuses):
        submitted = []
        specs = {"shot1": lambda: submitted.append(1) or f"job{len(submitted)}"}
        done = provider.run_jobs(FakeProvider(statuses), specs, poll_s=0, stall_s=0, max_retries=2, deadline_s=30)
        return submitted, done

    def test_slow_job_is_submitted_once(self):
        submitted, done = self.run_one(["pending"] * 5 + ["completed"])
        self.assertEqual(len(submitted), 1)
        self.assertEqual(done["shot1"], "https://example.invalid/out.mp4")

    def test_failed_job_is_retried(self):
        submitted, done = self.run_one(["failed", "completed"])
        self.assertEqual(len(submitted), 2)
        self.assertTrue(done["shot1"])


if __name__ == "__main__":
    unittest.main()
