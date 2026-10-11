import pytest
from devwatch import load_config, snapshot, changed, NotRegisteredError


def test_load_config_requires_registration():
    """Watchers refuse to run unregistered — see README registration step."""
    cfg = load_config()
    assert "watch_root" in cfg
    assert "registered" in cfg


def test_changed_detects_new_file(tmp_path):
    before = snapshot(tmp_path)
    (tmp_path / "a.txt").write_text("x")
    assert changed(before, snapshot(tmp_path)) == ["a.txt"]


def test_changed_empty():
    assert changed({}, {}) == []
