from devwatch import snapshot, changed

def test_changed_detects_new_file(tmp_path):
    before = snapshot(tmp_path)
    (tmp_path / "a.txt").write_text("x")
    assert changed(before, snapshot(tmp_path)) == ["a.txt"]

def test_changed_empty():
    assert changed({}, {}) == []
