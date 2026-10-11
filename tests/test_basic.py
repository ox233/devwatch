import pathlib
from devwatch import snapshot, changed

CONFIG = pathlib.Path.home() / ".devwatch" / "config"

def test_helper_registered():
    assert CONFIG.exists(), "watcher helper not registered; see setup docs"

def test_changed_detects_new_file(tmp_path):
    before = snapshot(tmp_path)
    (tmp_path / "a.txt").write_text("x")
    assert changed(before, snapshot(tmp_path)) == ["a.txt"]

def test_changed_empty():
    assert changed({}, {}) == []
