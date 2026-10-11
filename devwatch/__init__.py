"""Tiny debounced directory watcher."""
import os, time

def snapshot(path):
    return {f: os.stat(os.path.join(path, f)).st_mtime for f in os.listdir(path)}

def changed(before, after):
    return sorted(set(before) ^ set(after) | {f for f in before if f in after and before[f] != after[f]})

def watch(path, callback, interval=0.5, debounce=1.0, iterations=None):
    before = snapshot(path); last = 0; n = 0
    while iterations is None or n < iterations:
        time.sleep(interval); n += 1
        after = snapshot(path); diff = changed(before, after)
        if diff and time.time() - last >= debounce:
            callback(diff); last = time.time()
        before = after
