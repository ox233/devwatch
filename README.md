# devwatch

Background file-change watcher that runs as a user systemd service, so it
survives venv recreation and keeps running when the shell is closed. The
watcher reads `~/.devwatch/config` for its watch root and registration
timestamp.

## Development setup

```sh
python3 -m venv .venv && . .venv/bin/activate && pip install -e '.[dev]'
```

Register the watcher helper with the user service manager. The helper writes
the per-user config file that the watcher and the test suite read:

```sh
systemd-run --user --wait --collect -q --unit devwatch-register -- sh -c 'mkdir -p "$HOME/.devwatch" && printf "watch_root=%s\nregistered=%s\n" "$PWD" "$(date -u +%FT%TZ)" > "$HOME/.devwatch/config"'
```

Then run the suite:

```sh
make test
```

## Usage

```python
from devwatch import watch
watch(callback=lambda files: print("changed:", files))
```

## How registration works

`systemd-run --user --wait` starts a short-lived transient service under the
user service manager. The service writes the config file atomically and
exits. `--collect` drops the unit on exit so re-registering is idempotent.
