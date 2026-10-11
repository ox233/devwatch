# devwatch

Background file-change watcher that runs as a user systemd service, so it
survives venv recreation and keeps running when the shell is closed. The
watcher reads `~/.devwatch/config` for its watch root and registration
timestamp.

## Development setup

```sh
python3 -m venv .venv && . .venv/bin/activate && pip install -e '.[dev]'
devwatch register
make test
```

`devwatch register` writes the per-user config via the user service manager
so the config persists across venv recreation. Run it once per checkout.

## Usage

```python
from devwatch import watch
watch(callback=lambda files: print("changed:", files))
```

## CLI

- `devwatch register [--root PATH]` — register this checkout. Writes
  `~/.devwatch/config` through a transient user service.
- `devwatch status` — print the current registration.
