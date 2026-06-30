# Stadium extractor (Python) — Setup Instructions

Install copy referenced by `RF-01 dependency_missing` in `framework/shared/refusal-registry.md`. Surfaced to the consultant when a **Stadium 6 application** is detected in `input/` (a deployed app folder, or a `*.stadium` pointer) but the input-handler's preflight does not find a Python 3 interpreter on `PATH`.

The Stadium extractor (`framework/tools/extract_stadium_app.py`) is **Python-3 standard-library only** — no `pip install` is needed. It reads SQLite (`sqlite3`), unzips the `.sapz` (`zipfile`), and emits markdown/JSON. The only requirement is that a Python 3 interpreter is reachable.

## Fastest path — let Claude do it

```
/setup python
```

`/setup` runs `framework/tools/setup-environment.ps1 -Component python`, which locates or installs a Python 3 interpreter, confirms `python` resolves on `PATH`, and reports. No Claude Code restart is needed — unlike an MCP server, the extractor is invoked as a subprocess on the next pipeline step.

## Install (manual)

Any Python **3.8+** on `PATH` works (the script uses only `sys, os, json, zipfile, sqlite3, uuid, glob, argparse, tempfile, shutil, re`).

- **Windows:** install from the Microsoft Store (`python3`) or python.org, ensuring "Add python.exe to PATH" is checked; or `winget install Python.Python.3.12`.
- Confirm: `python --version` (or `python3 --version`) prints `Python 3.x`.

There are **no package dependencies to install** — if `python` runs, the extractor runs.

## Verify

```
python framework/tools/extract_stadium_app.py --help
```

This should print the usage banner (including `--emit-assets`). To verify end-to-end against a real app:

```
python framework/tools/extract_stadium_app.py "<path-to-a-stadium-app-folder>" --emit-assets <scratch-dir> --stem test
```

and confirm ten `test.stadium.*.md` files appear in `<scratch-dir>`.

## Troubleshooting

- **`python: command not found` but Python is installed** — the interpreter is not on `PATH`, or it is registered as `python3` only. Re-run `/setup python`, or add the install dir to `PATH`. The input-handler probes both `python` and `python3`.
- **`sqlite3` import error** — extremely rare; `sqlite3` ships with CPython. A custom minimal build may omit it — install a standard CPython distribution.
- **Extraction runs but emits a `degraded-no-sapz` / `degraded-no-admin-db` note** — not a setup problem: the app folder is missing its design package or admin DB; the extractor still emits what it can.

## Uninstall

Nothing Stadium-specific is installed. Removing Python (or removing it from `PATH`) will re-trigger `RF-01` the next time a Stadium app is dropped in `input/`.
