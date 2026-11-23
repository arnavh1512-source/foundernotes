#!/usr/bin/env python3
"""Spend gate shared by the MuAPI stages: the default run only prints the plan; --generate submits."""
import argparse
import os

DEFAULT_MAX_JOBS = 20


def add_flags(ap):
    ap.add_argument("--generate", action="store_true",
                    help="really submit the paid MuAPI jobs (default: print the plan, no network)")
    ap.add_argument("--max-jobs", type=int, default=DEFAULT_MAX_JOBS,
                    help=f"refuse to start when the plan has more jobs than this (default {DEFAULT_MAX_JOBS})")
    return ap


def parser(description, demo="demo"):
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("project_dir", nargs="?",
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", demo))
    return add_flags(ap)


def approve(jobs, generate, max_jobs=DEFAULT_MAX_JOBS):
    """jobs: [(key, model, output)]. Prints the plan; True only when a real run may start."""
    print(f"plan: {len(jobs)} paid MuAPI job(s)")
    for key, model, out in jobs:
        print(f"  [{key}] {model} -> {out}")
    over = len(jobs) > max_jobs
    if over and generate:
        raise SystemExit(f"plan has {len(jobs)} jobs, more than --max-jobs {max_jobs}; refusing to start.")
    if not generate:
        if over:
            print(f"note: {len(jobs)} jobs is more than --max-jobs {max_jobs}; raise it to run them all.")
        print("dry run: nothing sent. Add --generate to submit (spends MuAPI credit).")
        return False
    return True
