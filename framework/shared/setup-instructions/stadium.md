# Ingesting a Stadium 6 application

`/ingest-stadium` turns a deployed **Stadium 6 application** into a set of readable markdown files: its data, business rules, pages, user tasks and navigation. `/requirements` and the other input commands then read those files like any other client material. Run it once per app, **before** `/requirements`.

## Contents

- [Before you run the command](#before-you-run-the-command)
- [Run it](#run-it)
- [What you get](#what-you-get)
  - [Extracted facts (11 files)](#extracted-facts-11-files)
  - [Advisory files (AI-suggested)](#advisory-files-ai-suggested)
  - [Other files](#other-files)
- [What to do next](#what-to-do-next)
- [Re-ingesting an updated app](#re-ingesting-an-updated-app)
- [Setup: Python](#setup-python)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)

## Before you run the command

The command asks you nothing on a first run, so all the preparation happens here.

1. **Find the app.** Deployed Stadium 6 apps live under `C:\Stadium 6 Web Apps\`. The folders have GUID names (e.g. `09bd0d7a-f257-4831-a35f-bd5522f981ba`). To tell which app a folder holds, look for the `<AppName>.csproj` file inside it.
2. **Check that the folder is complete.** It should contain all three of these:
   - `administration.db`: users, roles and page permissions.
   - `App_Data/Updates/*.sapz`: the app's design package. This is where most of the data model, business rules and pages come from.
   - `ClientApp/`: the rendered front end.

   If one is missing, the command still runs but produces thinner output. With no `.sapz`, most of the content is lost. With no `administration.db`, roles and permissions are lost.
3. **Copy the entire folder into `documentation/`.** Copy it unchanged, as a direct child: `documentation/<guid>/administration.db`. Do not rename it (the GUID is the app's identity), do not put it inside another folder, and do not copy only part of it. A typical app is a few hundred MB.
4. **Add the rest of the client material** (briefs, decks, screenshots, spreadsheets) to `documentation/` as usual. `/requirements` reads it together with the Stadium output.
5. **Make sure Python 3 is installed.** See [Setup: Python](#setup-python). If it is missing, the command tells you and offers to install it.

> **Can't copy the folder?** If it is very large or in a read-only location, create a one-line text file `documentation/<AppName>.stadium` that contains the absolute path to the app folder. The command treats that pointer like a copied folder.

> **Git:** `documentation/` is not ignored by git, so the copied folder shows up as untracked. `/ingest-stadium` never commits it. Avoid `git add .` / `git add -A` while it is there.

## Run it

```
/ingest-stadium
```

The command finds every Stadium app in `documentation/` and extracts each new one. You are asked a question only when an app was ingested before (see [Re-ingesting an updated app](#re-ingesting-an-updated-app)). Your copied app folder is only read. It is never changed.

## What you get

A new folder per app, `documentation/<AppName>.stadium-assets/`, where `<AppName>` is the app's own name. It contains thirteen files named `<AppName>.stadium.<category>.md`.

### Extracted facts (11 files)

These are read directly from the app. They are factual, and `/requirements` cites them as sources.

| File | What it contains |
|---|---|
| `…stadium.overview.md` | App name, sign-in type, theme, session timeout, technology baseline, a list of gaps to be resolved, and an index of the other files. |
| `…stadium.data-model.md` | The data objects and their fields, which ones are created / read / updated / deleted, and how they relate to each other. |
| `…stadium.data-sources.md` | The databases, stored procedures and web services the app calls, with passwords removed. A backend reference for handoff. It is not used for design. |
| `…stadium.business-rules.md` | The app's scripts as step-by-step logic with their conditions, the messages shown to users, field validation rules, and empty / error / loading states. |
| `…stadium.access-control.md` | Sign-in, roles, which role can open which page, and a skeleton of the candidate user types. Only user counts are extracted, never names or emails. |
| `…stadium.surfaces.md` | Every page with its title and route, its meaningful controls, data-grid columns, and any reports or dashboards. |
| `…stadium.tasks.md` | The user tasks each page supports (e.g. "create a member"), with the evidence for each. |
| `…stadium.navigation.md` | How pages link to each other, pages that cannot be reached, and candidate journeys across pages. |
| `…stadium.glossary.md` | The words the app shows: labels, headings, button texts, titles. |
| `…stadium.design-signals.md` | Theme, colours, fonts and custom CSS. These are styling hints, not requirements. |
| `…stadium.modules.md` | Stadium add-on modules the app uses, the behaviour they imply, and modernisation hints. |

### Advisory files (AI-suggested)

These are written by Claude from the eleven files above. Every line is marked `[AI-SUGGESTED]`. Treat them as hints, not facts.

| File | What it contains |
|---|---|
| `…stadium.task-flows.md` | Suggested end-to-end user flows, with decision points and error paths. |
| `…stadium.quality-signals.md` | Suggested UX priorities (e.g. "efficiency over simplicity" for dense data grids). These feed the design variants of `/wireframe` and `/prototype`. |

### Other files

- `embedded/`: brand images found in the app, such as the logo. `/prototype` can reuse the logo.
- `framework/state/stadium/<guid>/model.json` and `framework/state/.stadium-processed.json` are internal bookkeeping. You can ignore them.

## What to do next

1. **Skim the assets** (optional). Start with `overview.md`, especially its gaps list. You may edit any file, and your edits are kept on later runs.
2. **Run `/requirements`.** It picks up the Stadium files automatically, together with the rest of `documentation/`, and produces `generated-docs/requirements/requirements.md`. That requirements document is the goal. Everything downstream (`/wireframe`, `/prototype`, `/export-application`) builds on it.

The same files also feed `/generate-prd`, `/analyse-inputs` and `/review-inputs` if you run those. Keep the copied app folder in `documentation/`, because you need it to re-ingest.

## Re-ingesting an updated app

Each app is extracted **once**. Later runs skip it, so your hand-edits are never overwritten by accident. To pick up a newer version of the app:

1. Replace the copied folder in `documentation/` with the updated one, keeping the same GUID name.
2. Run `/ingest-stadium` and choose **Re-ingest** when asked.

Re-ingest first saves a git checkpoint. It then **discards** the old assets, including your edits, and extracts them again. Choose **Skip** to keep the existing assets, or **Cancel** to stop.

## Setup: Python

The extractor (`framework/tools/extract_stadium_app.py`) uses only the Python 3 standard library, so there is no `pip install`. It needs just a Python **3.8+** interpreter on `PATH`. If you already installed Python for Office/PDF inputs, you are done.

**Fastest:** run `/setup python`. It locates or installs Python and confirms that `python` resolves on `PATH`. No Claude Code restart is needed.

**Manual (Windows):** install from python.org with "Add python.exe to PATH" checked, or from the Microsoft Store, or run `winget install Python.Python.3.12`. Confirm with `python --version`.

**Verify:**

```
python framework/tools/extract_stadium_app.py --help
```

This prints the usage banner. For an end-to-end check against a real app:

```
python framework/tools/extract_stadium_app.py "<path-to-a-stadium-app-folder>" --emit-assets <scratch-dir> --stem test
```

Eleven `test.stadium.*.md` files should appear in `<scratch-dir>`.

## Troubleshooting

- **"No Stadium application found in `documentation/`"**: the app folder is not a direct child of `documentation/` (e.g. it sits at `documentation/apps/<guid>/`), or it has none of `administration.db`, `App_Data/Updates/*.sapz` or `ClientApp/`.
- **`python: command not found`, but Python is installed**: the interpreter is not on `PATH`, or it is registered only as `python3`. Re-run `/setup python`, or add the install folder to `PATH`. The command tries both `python` and `python3`.
- **`sqlite3` import error**: rare. It happens with a custom minimal Python build. Install a standard CPython distribution.
- **The output mentions `degraded-no-sapz` / `degraded-no-admin-db`**: this is not a setup problem. The copied folder is missing its design package or admin database (see [Before you run the command](#before-you-run-the-command), step 2). Copy the complete folder and re-ingest.

## Uninstall

Nothing Stadium-specific is installed. Removing Python, or removing it from `PATH`, makes the command ask for it again on the next run.

---

*Maintainers: this file is also the setup advice that `RF-01` points to when the Stadium Python probe fails (`framework/shared/refusal-registry.md`, `framework/agents/stadium-ingestor.md`). Keep the Setup: Python section.*
