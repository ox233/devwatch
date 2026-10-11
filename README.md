# devwatch

Small file-watcher library used by internal tooling. Watches a directory and
calls back on changes, with debouncing.

## Development setup

```sh
python3 -m venv .venv && . .venv/bin/activate && pip install -e '.[dev]'
make test
```
