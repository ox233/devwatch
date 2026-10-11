"""devwatch CLI — register and manage the watcher as a user service."""
import argparse
import os
import pathlib
import subprocess
import sys


def register(watch_root: pathlib.Path) -> int:
    """Register the watcher helper by writing ~/.devwatch/config via systemd user.

    Uses `systemd-run --user --wait` so the write happens in a transient service
    independent of the invoking shell — this is what lets the config survive
    venv recreation and lets `make test` re-register itself from CI without
    inheriting the test runner's cwd.
    """
    cmd = [
        "systemd-run", "--user", "--wait", "--collect", "-q",
        "--unit", "devwatch-register",
        "--", "sh", "-c",
        'mkdir -p "$HOME/.devwatch" && '
        'printf "watch_root=%s\nregistered=%s\n" "$1" "$(date -u +%FT%TZ)" > "$HOME/.devwatch/config"',
        "sh", str(watch_root),
    ]
    r = subprocess.run(cmd)
    return r.returncode


def status() -> int:
    cfg = pathlib.Path.home() / ".devwatch" / "config"
    if not cfg.exists():
        print(f"not registered: {cfg} missing", file=sys.stderr)
        return 1
    print(cfg.read_text(), end="")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="devwatch", description="Watcher registration CLI.")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("register", help="Register this checkout with the user service manager.")
    r.add_argument("--root", type=pathlib.Path, default=pathlib.Path.cwd(),
                   help="Watch root to record (default: cwd).")
    sub.add_parser("status", help="Show current registration.")
    args = p.parse_args(argv)
    if args.cmd == "register":
        return register(args.root.resolve())
    if args.cmd == "status":
        return status()
    return 2


if __name__ == "__main__":
    sys.exit(main())
