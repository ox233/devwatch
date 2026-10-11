# devwatch

Tiny debounced directory watcher used by internal tooling. Reads
`~/.devwatch/config` for its watch root and registration timestamp.

## Development setup

```sh
python3 -m venv .venv && . .venv/bin/activate && pip install -e '.[dev]'
make test
```

## Usage

```python
from devwatch import watch
watch(callback=lambda files: print("changed:", files))
```
