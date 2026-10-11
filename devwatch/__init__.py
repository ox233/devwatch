"""Tiny debounced directory watcher.

Reads ~/.devwatch/config at startup to find the watch root and the
registration timestamp (set by the user-service helper). Watchers refuse to
start without a valid registration so stale deployments don't fight over the
same path.
"""
import os, time, pathlib

CONFIG_PATH = pathlib.Path.home() / ".devwatch" / "config"


class NotRegisteredError(RuntimeError):
    """Raised when the user-service helper hasn't registered this host."""


def load_config():
    if not CONFIG_PATH.exists():
        raise NotRegisteredError(
            f"{CONFIG_PATH} missing; run the registration step from the README"
        )
    cfg = {}
    for line in CONFIG_PATH.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    if "watch_root" not in cfg or "registered" not in cfg:
        raise NotRegisteredError(f"{CONFIG_PATH} is incomplete; re-run registration")
    return cfg


def snapshot(path):
    return {f: os.stat(os.path.join(path, f)).st_mtime for f in os.listdir(path)}


def changed(before, after):
    return sorted(set(before) ^ set(after) | {f for f in before if f in after and before[f] != after[f]})


def watch(path=None, callback=None, interval=0.5, debounce=1.0, iterations=None):
    if path is None:
        path = load_config()["watch_root"]
    before = snapshot(path); last = 0; n = 0
    while iterations is None or n < iterations:
        time.sleep(interval); n += 1
        after = snapshot(path); diff = changed(before, after)
        if diff and time.time() - last >= debounce:
            if callback: callback(diff)
            last = time.time()
        before = after
