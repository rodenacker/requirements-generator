#!/usr/bin/env python3
r"""test_extract_stadium.py -- Phase-2c regression harness for the Stadium extractor.

Formalizes the golden fixture Phase 1 seeded. Two tiers of test:

  * Corpus-INDEPENDENT (always run). Validate the checked-in ExecutionPath JSON goldens
    (__fixtures__/execpath-*.json) encode the source-model shapes the extractor depends on,
    and lock the decoded Operator/Join enum table, the GUID `bytes_le` normalization rule,
    and the fabricate-nothing fallbacks. These are the ONLY proof that survives the
    out-of-repo corpus being absent -- so they never skip.

  * Corpus-DEPENDENT (skipped cleanly when the corpus is absent). Re-derive the MemberAdmin
    golden live via _probe_execpath.py -- confirming the checked-in golden still matches the
    corpus, not just itself -- and smoke-run the extractor over a 4-app subset, asserting the
    enriched Tier-1 sub-sections (Phases 0/1) are actually emitted. An optional golden-asset
    `.md` snapshot diff runs when snapshots exist under __fixtures__/golden-assets/<App>/; a
    diff is reported as a REVIEW PROMPT, never an auto-fail (per the plan).

The corpus lives OUTSIDE the repo (default: C:\Stadium 6 Web Apps). Override with the
STADIUM_CORPUS environment variable. Apps are discovered by their administration.db
Applications.Name so no GUID folder names need be hard-coded.

USAGE
    python -m unittest framework/tools/test_extract_stadium.py         # run the suite
    python framework/tools/test_extract_stadium.py                     # same (unittest.main)
    python framework/tools/test_extract_stadium.py --update-goldens    # (corpus only) seed/refresh
                                                                       #   the .md snapshot goldens
"""

import os
import sys
import json
import glob
import sqlite3
import tempfile
import shutil
import subprocess
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "__fixtures__")
GOLDEN_ASSETS = os.path.join(FIXTURES, "golden-assets")
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))          # framework/tools -> repo root
KB_DIR = os.path.join(HERE, "..", "assets", "stadium")      # framework/assets/stadium
PROBE = os.path.join(HERE, "_probe_execpath.py")

CORPUS_ROOT = os.environ.get("STADIUM_CORPUS", r"C:\Stadium 6 Web Apps")

# The 4-app golden subset (plan 2c): configured RBAC + linear / branches + dialogs /
# wizard + validation gate / null case. Matched case-insensitively against Applications.Name.
SUBSET = ["MemberAdmin", "PaymentsApp", "RMB_Onboarding", "ResourceCenter"]

# Sub-section headers each enriched Tier-1 asset MUST emit after Phases 0/1. These are
# rendered unconditionally by emit_assets() (present even when the section body is a
# "_No ..._" placeholder), so they are stable across every app -- the right thing to
# assert for a smoke test that must not be app-specific.
ENRICHED_MARKERS = {
    "business-rules": [
        "## Tier-A — event logic",                              # 1c trigger-grouped flows
        "## Tier-A — notification points",                      # 0a
        "## Tier-A — validation",                               # 0f
        "## Tier-A — edge / empty / error / loading state signals",  # 1d
    ],
    "access-control": [
        "## Tier-B — actor candidates",                         # 0d
        "## Tier-B — actor / persona scaffold",                 # 0h
    ],
    "surfaces": [
        "## View / task / feature inventory",                   # 0b
        "## Action affordances → candidate tasks",              # 0e
    ],
    "navigation": [
        "## Tier-A — navigation reachability",                  # 0c
        "## Tier-B — candidate cross-surface journeys",         # 1e
    ],
}

TIER1_CATEGORIES = ["overview", "data-model", "data-sources", "business-rules",
                    "access-control", "surfaces", "navigation", "glossary",
                    "design-signals", "modules"]


# --------------------------------------------------------------------------- corpus discovery
def discover_corpus_apps():
    """Map {app-name-lower: folder-path} by reading each app's administration.db Applications.Name.
    Returns {} when the corpus root is absent (so every corpus-dependent test skips cleanly)."""
    if not os.path.isdir(CORPUS_ROOT):
        return {}
    found = {}
    for entry in sorted(os.listdir(CORPUS_ROOT)):
        folder = os.path.join(CORPUS_ROOT, entry)
        admin = os.path.join(folder, "administration.db")
        if not (os.path.isdir(folder) and os.path.isfile(admin)):
            continue
        name = None
        try:
            con = sqlite3.connect(f"file:{admin}?mode=ro", uri=True)
            row = con.execute("SELECT Name FROM Applications LIMIT 1").fetchone()
            con.close()
            if row and row[0]:
                name = str(row[0]).strip()
        except Exception:
            name = None
        # Fall back to the folder basename if the name is unreadable (still discoverable by GUID).
        found[(name or entry).lower()] = folder
    return found


_CORPUS_APPS = discover_corpus_apps()
_HAS_CORPUS = bool(_CORPUS_APPS)
_SKIP_CORPUS_MSG = (f"Stadium corpus absent (looked in {CORPUS_ROOT!r}; set STADIUM_CORPUS to "
                    f"point at it). Corpus-independent golden checks still ran.")


def _resolve_subset():
    """Return [(name, folder)] for the subset apps present in the discovered corpus."""
    out = []
    for want in SUBSET:
        folder = _CORPUS_APPS.get(want.lower())
        if folder:
            out.append((want, folder))
    return out


def _run_extractor(app_folder, out_dir, stem):
    """Run extract_stadium_app.py --emit-assets over one app. Returns (returncode, stdout, stderr)."""
    cmd = [sys.executable, os.path.join(HERE, "extract_stadium_app.py"), app_folder,
           "--emit-assets", out_dir, "--stem", stem,
           "--kb", KB_DIR, "--model-out", os.path.join(out_dir, "model.json")]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


# =========================================================================== corpus-INDEPENDENT
class TestExecPathGoldens(unittest.TestCase):
    """The in-repo JSON goldens are the corpus-independent proof of the source-model shapes.
    These assertions must hold regardless of whether the corpus is present."""

    def _load(self, basename):
        path = os.path.join(FIXTURES, basename)
        self.assertTrue(os.path.isfile(path), f"missing golden fixture: {path}")
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def test_memberadmin_linear_10_actions(self):
        """MemberAdmin MemberUpdate.Load -> Script->ExecutionPath->Actions = 10 ordered root
        actions, no branches (the 1a acceptance oracle)."""
        g = self._load("execpath-memberadmin-memberupdate-load.json")
        self.assertEqual(g["script"]["name"], "MemberUpdate.Load")
        self.assertEqual(g["action_count"], 10)
        self.assertEqual(len(g["actions"]), 10)
        self.assertEqual(len(g["action_sequence"]), 10)
        # every action resolved (no dangling GUID) and carries a type in execution order
        for i, a in enumerate(g["actions"]):
            self.assertNotIn("_missing", a, f"action {i} unresolved")
            self.assertEqual(a.get("type"), g["action_sequence"][i])
        # linear: no Decision node at the root
        self.assertNotIn("Decision", g["action_sequence"])
        self.assertIsNone(g.get("decision_sample"))

    def test_rmb_onboarding_branch_and_else(self):
        """RMB_Onboarding btnNext.Click proves the branch shape AND that the validation-fail
        Notification lives INSIDE the else branch (the flat DFS scrambled it after the navigate)."""
        g = self._load("execpath-rmb-onboarding-btnnext-click.json")
        self.assertEqual(g["script"]["name"], "btnNext.Click")
        # root = CallScript(Validate) then a Decision
        self.assertEqual(g["action_sequence"], ["CallScript", "Decision"])
        decision = g["actions"][1]
        self.assertTrue(decision.get("decision") or decision.get("type") == "Decision")
        self.assertTrue(decision.get("ShowElse"), "ShowElse must be True to carry an else branch")
        branches = decision["branches"]
        self.assertGreaterEqual(len(branches), 2)

        ifs = [b for b in branches if (b.get("kind") == "if" or b.get("type") == "IfPath")]
        elses = [b for b in branches if b.get("type") == "ExecutionPath" or b.get("kind") == "else"]
        self.assertTrue(ifs, "expected an IfPath branch with conditions")
        self.assertTrue(elses, "expected a trailing else ExecutionPath branch")

        # the if-branch carries a resolved condition (Valid == true)
        cond = ifs[0]["conditions"][0]
        self.assertEqual(cond["Value1"], "Valid")
        self.assertEqual(cond["Operator"], 0)          # 0 == equality (see enum table)
        self.assertEqual(cond["Value2"], "true")

        # THE key regression: a Notification lives inside the else branch, not after the navigate
        else_types = [a.get("type") for a in elses[-1]["actions"]]
        self.assertIn("Notification", else_types,
                      "validation-fail Notification must sit INSIDE the else branch")

    def test_golden_condition_operators_match_enum_table(self):
        """Every Operator int in the goldens must map through the documented enum table
        (sapz-spec.md). Guards against the table silently drifting from the fixtures."""
        sys.path.insert(0, HERE)
        from extract_stadium_app import op_symbol

        def _walk(node):
            for b in node.get("branches", []) or []:
                for c in b.get("conditions", []) or []:
                    op = c.get("Operator")
                    if op is not None:
                        self.assertFalse(op_symbol(op).startswith("op"),
                                         f"Operator {op} present in a golden but unmapped in the enum table")
                for a in b.get("actions", []) or []:
                    _walk(a)
        for basename in ("execpath-memberadmin-memberupdate-load.json",
                         "execpath-rmb-onboarding-btnnext-click.json"):
            g = self._load(basename)
            for a in g.get("actions", []):
                _walk(a)
            if g.get("decision_sample"):
                _walk(g["decision_sample"])


class TestDecodedEnumsAndGuidRule(unittest.TestCase):
    """Lock the two facts the Phase-2b docs now assert: the decoded Operator/Join table and the
    GUID bytes_le normalization rule. If either changes, the docs (sapz-spec.md) must change too."""

    def setUp(self):
        sys.path.insert(0, HERE)

    def test_operator_enum_table(self):
        from extract_stadium_app import DECISION_OP_SYMBOLS, op_symbol
        self.assertEqual(DECISION_OP_SYMBOLS,
                         {0: "==", 1: "!=", 2: "<", 3: "<=", 4: ">", 5: ">="})
        self.assertEqual(op_symbol(0), "==")
        self.assertEqual(op_symbol(5), ">=")

    def test_join_enum_table(self):
        from extract_stadium_app import DECISION_JOIN_SYMBOLS, join_word
        self.assertEqual(DECISION_JOIN_SYMBOLS, {0: "AND", 1: "OR"})
        self.assertEqual(join_word(0), "AND")
        self.assertEqual(join_word(1), "OR")

    def test_unmapped_codes_fabricate_nothing(self):
        """An unmapped enum degrades to op<N>/join<N> -- never a wrong symbol (fabricate-nothing)."""
        from extract_stadium_app import op_symbol, join_word
        self.assertEqual(op_symbol(99), "op99")
        self.assertEqual(join_word(7), "join7")
        self.assertEqual(op_symbol(None), "opNone")

    def test_norm_guid_string_and_blob_agree(self):
        """A .NET bytes_le blob and its string form must canonicalize to the SAME lowercase-hyphen
        GUID -- the 'gotcha' the reference-walk depends on."""
        import uuid
        from extract_stadium_app import norm_guid
        u = uuid.UUID("785d3104-7f1a-4d0d-9689-566e0c21295b")
        self.assertEqual(norm_guid(str(u)), str(u))
        self.assertEqual(norm_guid(u.bytes_le), str(u))
        self.assertEqual(norm_guid(u.bytes_le), norm_guid(str(u).upper()))
        self.assertIsNone(norm_guid(None))


class TestControlPropSurfacing(unittest.TestCase):
    """Cluster A #1/#2/#3 — corpus-independent proof that the widened control props render
    correctly: the validation projection, field-behaviour constraints, DataGrid column resolution,
    and the fabricate-nothing fallbacks. Grounded in checked-in MemberAdmin fixtures + synthetic
    edge cases, so these run even when the corpus is absent."""

    def setUp(self):
        sys.path.insert(0, HERE)

    def _load(self, basename):
        path = os.path.join(FIXTURES, basename)
        self.assertTrue(os.path.isfile(path), f"missing fixture: {path}")
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # ---- #1: rule-intent classifier
    def test_rule_intent_classification(self):
        from extract_stadium_app import _rule_intent
        self.assertEqual(_rule_intent('/^\\S+@\\S+\\.\\S+$/.test({0})'), "email")
        self.assertEqual(_rule_intent('/^[+-]?[0-9]\\d*$/.test({0})'), "numeric")
        self.assertEqual(_rule_intent("dayjs({0}) < dayjs().add(-18,'year')"), "date")
        self.assertEqual(_rule_intent('/^[\\w!@#$%^&*]{8,16}$/.test({0})'), "length")
        self.assertEqual(_rule_intent(""), "pattern")     # fabricate-nothing: no rule -> generic
        self.assertEqual(_rule_intent(None), "pattern")

    # ---- #1: validation projection (target/type/rule/message, empty-message + required-only)
    def test_validation_rows(self):
        from extract_stadium_app import _control_validation_rows
        controls = self._load("control-props-memberadmin.json")["controls"]
        rich, req = _control_validation_rows(controls)
        blob = "\n".join(rich)
        self.assertIn("`EmailTextBox` · required+email", blob)
        self.assertIn("`PasswordTextBox` · required+length", blob)
        self.assertIn("`DOBDatePicker` · required+date", blob)
        self.assertIn('`FirstNameTextBox` · required · "Please add a value"', blob)
        # .NET composite-format braces un-escaped for display
        self.assertIn("{1,3}", blob)
        self.assertNotIn("{{1,3}}", blob)
        # intent label is Tier-B advisory on the format rules
        self.assertIn("`[AI-SUGGESTED: email]`", blob)
        # required-only + EMPTY ErrorText -> compact list, never a bare "" message
        self.assertIn("EmptyMsgField", req)
        self.assertNotIn("EmptyMsgField", blob)
        self.assertNotIn(' · "" ', blob)
        self.assertNotIn(' · ""', blob)
        # constraint-only controls (no required / rule / message) are NOT validation rows
        self.assertNotIn("NotesTextBox", blob)
        self.assertNotIn("IdTypeDd", blob)
        self.assertNotIn("NotesTextBox", " ".join(req))

    # ---- #1: field-behaviour constraints (help / editability / multi-line / enums)
    def test_control_constraints(self):
        from extract_stadium_app import _control_constraints
        by = {c["name"]: c["key_props"] for c in self._load("control-props-memberadmin.json")["controls"]}
        self.assertIn('hint: "Select a date"', _control_constraints(by["DOBDatePicker"]))
        city = _control_constraints(by["CityDropDown"])
        self.assertIn('hint: "Select a city"', city)
        self.assertIn("dynamic choices (bound)", city)     # OptionsField binding, Options null
        notes = _control_constraints(by["NotesTextBox"])
        self.assertIn("multi-line (5 rows)", notes)
        self.assertIn("read-only", notes)
        self.assertIn('hint: "Free text"', notes)
        idt = _control_constraints(by["IdTypeDd"])          # static inline Options -> verbatim enum
        self.assertTrue(any(a.startswith("choices:") and '"ID"' in a and '"Passport"' in a for a in idt),
                        f"expected verbatim enum choices, got {idt}")
        # presence != data: Hint null + VisibleLines "1" -> no constraint annotations
        self.assertEqual(_control_constraints(by["FirstNameTextBox"]), [])

    # ---- #2: ColumnType enum decode + fabricate-nothing fallback
    def test_decode_column_type(self):
        from extract_stadium_app import _decode_column_type
        self.assertEqual(_decode_column_type(0), "data")
        self.assertEqual(_decode_column_type(1), "action")
        self.assertEqual(_decode_column_type("1"), "action")
        self.assertEqual(_decode_column_type(99), "type99")     # unknown int round-trips, never guessed
        self.assertIsNone(_decode_column_type(None))
        self.assertIsNone(_decode_column_type("x"))

    # ---- #2: Columns GUID resolution (order, hidden, action, unresolved fallback)
    def test_resolve_columns_synthetic(self):
        from extract_stadium_app import _resolve_columns
        f = self._load("datagrid-columns-memberadmin.json")["synthetic"]
        cols = _resolve_columns(f["props"], f["registry"])
        self.assertEqual(len(cols), 4)
        self.assertEqual(cols[0]["kind"], "action")
        self.assertTrue(cols[0]["has_action"])
        self.assertTrue(cols[0]["visible"])
        self.assertEqual(cols[1]["kind"], "data")
        self.assertFalse(cols[1]["visible"])               # ID column hidden
        self.assertEqual(cols[2]["kind"], "data")
        self.assertTrue(cols[2]["visible"])
        self.assertEqual(cols[3].get("unresolved"), "col-missing")   # never fabricated

    # ---- #2: the one-line render matches the MemberAdmin golden verbatim
    def test_columns_line_golden(self):
        from extract_stadium_app import _columns_line
        f = self._load("datagrid-columns-memberadmin.json")
        self.assertEqual(_columns_line(f["resolved_golden"]), f["expected_columns_line"])


# =========================================================================== corpus-DEPENDENT
@unittest.skipUnless(_HAS_CORPUS, _SKIP_CORPUS_MSG)
class TestProbeReproducesGolden(unittest.TestCase):
    """Re-derive the MemberAdmin golden straight off the live .sapz via the independent probe --
    confirms the checked-in golden still matches the corpus, not merely itself."""

    def test_probe_exit_zero_on_memberadmin(self):
        folder = _CORPUS_APPS.get("memberadmin")
        if not folder:
            self.skipTest("MemberAdmin not found in the corpus")
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "regen.json")
            p = subprocess.run([sys.executable, PROBE, "--app", folder, "--out", out],
                               capture_output=True, text=True)
            # The probe exits non-zero unless MemberUpdate.Load reproduces exactly 10 ordered actions.
            self.assertEqual(p.returncode, 0, f"probe failed:\n{p.stdout}\n{p.stderr}")
            with open(out, encoding="utf-8") as f:
                regen = json.load(f)
            self.assertEqual(regen["action_count"], 10)


@unittest.skipUnless(_HAS_CORPUS, _SKIP_CORPUS_MSG)
class TestExtractorSmokeOverSubset(unittest.TestCase):
    """Run the real extractor over the 4-app subset; assert it exits 0, writes all ten Tier-1
    assets non-empty, and emits every enriched Phase-0/1 sub-section header."""

    def test_subset_extracts_with_enriched_sections(self):
        subset = _resolve_subset()
        if not subset:
            self.skipTest(f"none of {SUBSET} found in the corpus")
        for name, folder in subset:
            with self.subTest(app=name), tempfile.TemporaryDirectory() as tmp:
                rc, out, err = _run_extractor(folder, tmp, name)
                self.assertEqual(rc, 0, f"[{name}] extractor exited {rc}\n{out}\n{err}")
                for cat in TIER1_CATEGORIES:
                    path = os.path.join(tmp, f"{name}.stadium.{cat}.md")
                    self.assertTrue(os.path.isfile(path), f"[{name}] missing Tier-1 asset {cat}")
                    self.assertGreater(os.path.getsize(path), 0, f"[{name}] empty asset {cat}")
                for cat, markers in ENRICHED_MARKERS.items():
                    with open(os.path.join(tmp, f"{name}.stadium.{cat}.md"), encoding="utf-8") as fh:
                        text = fh.read()
                    for marker in markers:
                        self.assertIn(marker, text, f"[{name}] {cat}.md missing enriched section: {marker!r}")

    def test_tier_a_headings_carry_no_ai_suggested(self):
        """Tiering contract: a line directly under a '## Tier-A' heading must not itself be an
        [AI-SUGGESTED] assertion. (Tier-A blocks may still reference gap prompts on their own
        marked lines, so we only flag a heading whose own text carries the marker.)"""
        subset = _resolve_subset()
        if not subset:
            self.skipTest(f"none of {SUBSET} found in the corpus")
        name, folder = subset[0]
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = _run_extractor(folder, tmp, name)
            self.assertEqual(rc, 0, f"[{name}] extractor exited {rc}\n{err}")
            for cat in ("business-rules", "access-control", "surfaces", "navigation"):
                with open(os.path.join(tmp, f"{name}.stadium.{cat}.md"), encoding="utf-8") as fh:
                    for line in fh:
                        if line.startswith("## Tier-A"):
                            self.assertNotIn("[AI-SUGGESTED", line,
                                             f"[{name}] {cat}: a Tier-A heading carries [AI-SUGGESTED]: {line!r}")

    def test_clusterA_validation_and_columns_rendered(self):
        """Live-render check on MemberAdmin (the golden: email/password/DOB rules + a DataGrid):
        the validation section carries per-control rows (never a bare "" message) and the surfaces
        asset carries at least one resolved DataGrid column line."""
        folder = _CORPUS_APPS.get("memberadmin")
        if not folder:
            self.skipTest("MemberAdmin not found in the corpus")
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = _run_extractor(folder, tmp, "MemberAdmin")
            self.assertEqual(rc, 0, f"extractor exited {rc}\n{err}")
            with open(os.path.join(tmp, "MemberAdmin.stadium.business-rules.md"), encoding="utf-8") as fh:
                br = fh.read()
            with open(os.path.join(tmp, "MemberAdmin.stadium.surfaces.md"), encoding="utf-8") as fh:
                sf = fh.read()
            self.assertRegex(br, r"## Tier-A — validation\n[\s\S]*?\n- `[^`]+` · ")   # a per-control row
            self.assertIn("required+email", br)
            self.assertNotIn(' · ""', br)                                              # never a bare empty msg
            self.assertIn("columns (in order):", sf)                                   # #2 resolved columns


@unittest.skipUnless(_HAS_CORPUS, _SKIP_CORPUS_MSG)
class TestUntouchedAssetsByteIdentical(unittest.TestCase):
    """Cluster A touches only `business-rules`, `surfaces`, and `overview`. Assert every OTHER
    Tier-1 asset is byte-identical to its checked-in golden snapshot — a HARD fail on drift (unlike
    the review-only snapshot diff). Skips cleanly until goldens are seeded (--update-goldens)."""

    UNTOUCHED = [c for c in TIER1_CATEGORIES if c not in ("business-rules", "surfaces", "overview")]

    def test_untouched_assets_match_golden(self):
        if not os.path.isdir(GOLDEN_ASSETS):
            self.skipTest("no golden-asset snapshots checked in yet (run --update-goldens)")
        checked = 0
        for name, folder in _resolve_subset():
            snap_dir = os.path.join(GOLDEN_ASSETS, name)
            if not os.path.isdir(snap_dir):
                continue
            with tempfile.TemporaryDirectory() as tmp:
                rc, out, err = _run_extractor(folder, tmp, name)
                self.assertEqual(rc, 0, f"[{name}] extractor exited {rc}\n{err}")
                for cat in self.UNTOUCHED:
                    snap = os.path.join(snap_dir, f"{name}.stadium.{cat}.md")
                    fresh = os.path.join(tmp, f"{name}.stadium.{cat}.md")
                    if not os.path.isfile(snap):
                        continue
                    with open(snap, encoding="utf-8") as fa, open(fresh, encoding="utf-8") as fb:
                        self.assertEqual(fa.read(), fb.read(),
                                         f"[{name}] untouched asset {cat}.md drifted from its golden")
                    checked += 1
        if not checked:
            self.skipTest("no untouched-asset goldens to compare (seed with --update-goldens)")


@unittest.skipUnless(_HAS_CORPUS, _SKIP_CORPUS_MSG)
class TestGoldenAssetSnapshots(unittest.TestCase):
    """Diff freshly-emitted assets against checked-in `.md` snapshots. A diff is a REVIEW PROMPT
    (printed, non-fatal) -- never an auto-fail -- per the plan. Skips when no snapshot is present;
    seed snapshots with `python test_extract_stadium.py --update-goldens`."""

    def test_snapshot_diff_is_review_only(self):
        if not os.path.isdir(GOLDEN_ASSETS):
            self.skipTest("no golden-asset snapshots checked in yet "
                          "(run --update-goldens with the corpus present to seed them)")
        any_snapshot = False
        for name, folder in _resolve_subset():
            snap_dir = os.path.join(GOLDEN_ASSETS, name)
            if not os.path.isdir(snap_dir):
                continue
            any_snapshot = True
            with tempfile.TemporaryDirectory() as tmp:
                rc, out, err = _run_extractor(folder, tmp, name)
                self.assertEqual(rc, 0, f"[{name}] extractor exited {rc}\n{err}")
                for snap in sorted(glob.glob(os.path.join(snap_dir, "*.md"))):
                    fresh = os.path.join(tmp, os.path.basename(snap))
                    if not os.path.isfile(fresh):
                        print(f"REVIEW [{name}]: golden {os.path.basename(snap)} has no emitted counterpart")
                        continue
                    with open(snap, encoding="utf-8") as fa:
                        a = fa.read().splitlines()
                    with open(fresh, encoding="utf-8") as fb:
                        b = fb.read().splitlines()
                    if a != b:
                        import difflib
                        diff = list(difflib.unified_diff(a, b, fromfile=f"golden/{os.path.basename(snap)}",
                                                         tofile=f"emitted/{os.path.basename(snap)}", lineterm=""))
                        print(f"REVIEW [{name}] {os.path.basename(snap)} drifted "
                              f"({sum(1 for d in diff if d and d[0] in '+-' and d[:2] not in ('+++', '---'))} changed lines):")
                        print("\n".join(diff[:60]))
                        if len(diff) > 60:
                            print(f"  ... (+{len(diff) - 60} more diff lines)")
        if not any_snapshot:
            self.skipTest("no per-app snapshot directories under golden-assets/ for the discovered subset")


# --------------------------------------------------------------------------- snapshot seeding
def update_goldens():
    """Regenerate the .md snapshot goldens for the subset apps found in the corpus. Corpus-only
    maintenance helper (the snapshots are a local regression aid, not a CI gate)."""
    if not _HAS_CORPUS:
        print(_SKIP_CORPUS_MSG, file=sys.stderr)
        return 3
    subset = _resolve_subset()
    if not subset:
        print(f"none of {SUBSET} found in {CORPUS_ROOT!r}", file=sys.stderr)
        return 3
    os.makedirs(GOLDEN_ASSETS, exist_ok=True)
    for name, folder in subset:
        snap_dir = os.path.join(GOLDEN_ASSETS, name)
        os.makedirs(snap_dir, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = _run_extractor(folder, tmp, name)
            if rc != 0:
                print(f"[{name}] extractor exited {rc} -- skipping\n{err}", file=sys.stderr)
                continue
            for cat in TIER1_CATEGORIES:
                src = os.path.join(tmp, f"{name}.stadium.{cat}.md")
                if os.path.isfile(src):
                    shutil.copy2(src, os.path.join(snap_dir, f"{name}.stadium.{cat}.md"))
            print(f"[{name}] seeded {len(TIER1_CATEGORIES)} asset goldens -> {snap_dir}")
    print("NOTE: review the seeded goldens before committing (they encode the current, "
          "assumed-correct, emitter output).")
    return 0


if __name__ == "__main__":
    if "--update-goldens" in sys.argv:
        sys.argv.remove("--update-goldens")
        sys.exit(update_goldens())
    unittest.main()
