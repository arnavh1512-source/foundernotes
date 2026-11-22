#!/usr/bin/env python3
"""
Provider abstraction — pluggable media backend for Vox Director pipeline stages.
Supports 'muapi' as the primary provider (via MuAPI platform) and 'atlas_cloud' as fallback.
"""

import time
from abc import ABC, abstractmethod

import muapi_client


class ProviderError(RuntimeError):
    pass


class Provider(ABC):
    """Abstract provider surface for Vox Director pipeline stages."""
    name = "base"

    @abstractmethod
    def submit_image(self, model, prompt, **params): ...
    @abstractmethod
    def submit_video(self, model, prompt, **params): ...
    @abstractmethod
    def submit_audio(self, model, **params): ...
    @abstractmethod
    def remove_bg(self, model, image_url, **params): ...
    @abstractmethod
    def get_status(self, job_id): ...
    @abstractmethod
    def upload(self, path): ...
    @abstractmethod
    def download(self, url, dest): ...


class MuapiProvider(Provider):
    """Wraps muapi_client — interfaces with api.muapi.ai"""
    name = "muapi"

    def submit_image(self, model, prompt, **params):
        return muapi_client.submit(model, {"prompt": prompt, **params})

    def submit_video(self, model, prompt, **params):
        return muapi_client.submit(model, {"prompt": prompt, **params})

    def submit_audio(self, model, **params):
        return muapi_client.submit(model, params)

    def remove_bg(self, model, image_url, **params):
        return muapi_client.submit(model or "remove-background", {"image_url": image_url, **params})

    def get_status(self, job_id):
        res = None
        try:
            res = muapi_client._get(f"/predictions/{job_id}/result")
        except Exception:
            try:
                res = muapi_client._get(f"/predictions/{job_id}")
            except Exception as e2:
                code = getattr(e2, "code", None)
                if code and 400 <= code < 500 and code != 429:
                    # refused (bad key, unknown job): not "still running". The job may still exist and bill,
                    # so it must not be resubmitted either.
                    return {"status": "failed", "output": None, "error": str(e2), "retry": False}
                return {"status": "pending", "output": None, "error": str(e2)}

        if not res:
            return {"status": "pending", "output": None, "error": None}

        status = (res.get("status") or (res.get("data") or {}).get("status") or "").lower()
        if status in ("completed", "success", "succeeded"):
            url = muapi_client.extract_url(res)
            return {"status": "completed", "output": url, "error": None}
        if status in ("failed", "cancelled"):
            err = res.get("error") or (res.get("data") or {}).get("error") or "Job failed"
            return {"status": "failed", "output": None, "error": str(err)}
        return {"status": "pending", "output": None, "error": None}

    def upload(self, path):
        return muapi_client.upload(path)

    def download(self, url, dest):
        return muapi_client.download(url, dest)


_REGISTRY = {
    "muapi": MuapiProvider,
}


def get_provider(name=None):
    """Return a Provider instance by name (default 'muapi')."""
    name = (name or "muapi").lower()
    if name not in _REGISTRY:
        raise ProviderError(f"Unknown provider '{name}'; available: {list(_REGISTRY)}")
    return _REGISTRY[name]()


def run_jobs(prov, specs, *, poll_s=3, stall_s=90, max_retries=2, deadline_s=900):
    """Submit + poll a batch of jobs, resubmitting only a job the provider reports as failed.

    A job that is still running is never resubmitted: the status carries no progress, so "slow" cannot be told
    from "stalled", and every resubmission is a new paid job. stall_s is accepted for existing callers and unused;
    deadline_s bounds the wait."""
    state = {}
    for key, submit_fn in specs.items():
        try:
            jid = submit_fn()
            state[key] = {
                "submit_fn": submit_fn,
                "id": jid,
                "tries": 1,
                "out": None,
                "error": None,
                "done": False,
            }
            print(f"  [{key}] submitted -> {jid}")
        except Exception as e:
            print(f"  [{key}] submit failed: {e}")
            state[key] = {
                "submit_fn": submit_fn,
                "id": None,
                "tries": 1,
                "out": None,
                "error": str(e),
                "done": True,
            }

    deadline = time.monotonic() + deadline_s
    while time.monotonic() < deadline:
        all_done = True
        for key, s in state.items():
            if s["done"]:
                continue
            all_done = False
            res = prov.get_status(s["id"])
            st = res["status"]
            if st == "completed":
                s["out"] = res["output"]
                s["done"] = True
                print(f"  [{key}] completed -> {s['out']}")
            elif st == "failed":
                reason = res["error"]
                if s["tries"] <= max_retries and res.get("retry", True):
                    print(f"  [{key}] {reason}; retry {s['tries']}/{max_retries}...")
                    try:
                        new_id = s["submit_fn"]()
                        s["id"] = new_id
                        s["tries"] += 1
                        print(f"  [{key}] re-submitted -> {new_id}")
                    except Exception as e:
                        s["error"] = str(e)
                        s["done"] = True
                        print(f"  [{key}] re-submit failed: {e}")
                else:
                    s["error"] = reason
                    s["done"] = True
                    print(f"  [{key}] failed permanently: {reason}")

        if all_done:
            break
        time.sleep(poll_s)

    results = {}
    for key, s in state.items():
        results[key] = s["out"]
        if not s["out"]:
            print(f"  WARNING: [{key}] produced no output (error: {s['error']})")
    return results
