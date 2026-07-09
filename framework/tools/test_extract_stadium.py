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

# The emitted assets are UTF-8 and (since Cluster C) carry non-cp1252 glyphs (→ ⚠ · —). The review-diff
# printer below writes them to the console, so force UTF-8 stdout/stderr — otherwise a Windows cp1252
# console raises UnicodeEncodeError inside a REVIEW print (which must never be fatal).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    except Exception:
        pass

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
        "## User tasks (per view)",                             # 0e superseded → pointer to the tasks asset
    ],
    "tasks": [
        "## Task inventory",                                    # per-view user-task rows
        "## Views with no derivable user task",                 # completeness declaration
        "## Coverage",                                          # coverage stat
    ],
    "navigation": [
        "## Tier-A — navigation reachability",                  # 0c
        "## Tier-B — candidate cross-surface journeys",         # 1e
    ],
}

TIER1_CATEGORIES = ["overview", "data-model", "data-sources", "business-rules",
                    "access-control", "surfaces", "tasks", "navigation", "glossary",
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


class TestClusterBSettingRedaction(unittest.TestCase):
    """Cluster B #4-B — corpus-independent proof that `_redact_setting` classifies every Setting-row
    shape and that no secret VALUE ever survives (the `IsSecret` flag is unreliable, so it is never
    trusted). Uses synthetic values only — real Setting rows carry live secrets and are never committed."""

    def setUp(self):
        sys.path.insert(0, HERE)

    def test_classification(self):
        from extract_stadium_app import _redact_setting
        cases = [
            ("ApiCosmoCrmKey", "sk-live-DEADBEEF1234", "credential"),      # secret-shaped NAME
            ("Stadium_api_key", "0123456789abcdef0123456789abcdef", "credential"),
            ("DBConnection", "Server=DB01;Database=App;User ID=sa;Password=hunter2;", "connection"),
            ("SmartStream_InternalAPI_URL", "https://internal.example.co/api?token=SECRET#f", "endpoint"),
            ("MenuItems", r"C:\DigiataRepos\App\menu.json", "path"),
            ("DepartmentID", "2", "scalar"),
        ]
        for name, value, kind in cases:
            k, _ = _redact_setting(name, value)
            self.assertEqual(k, kind, f"{name!r} -> {k!r}, expected {kind!r}")

    def test_no_secret_value_survives(self):
        from extract_stadium_app import _redact_setting
        # secret-shaped name -> presence only, value never emitted
        k, v = _redact_setting("ApiCosmoCrmKey", "sk-live-DEADBEEF1234")
        self.assertEqual((k, v), ("credential", "<redacted>"))
        self.assertNotIn("DEADBEEF", v)
        # connection string -> password redacted, host kept visible
        _, v = _redact_setting("DBConnection", "Server=DB01;Database=App;User ID=sa;Password=hunter2;")
        self.assertNotIn("hunter2", v)
        self.assertIn("DB01", v)
        # URL -> query/token + fragment dropped, scheme+host+path kept
        _, v = _redact_setting("SmartStream_InternalAPI_URL", "https://internal.example.co/api?token=SECRET#f")
        self.assertNotIn("SECRET", v)
        self.assertNotIn("token", v)
        self.assertTrue(v.startswith("https://internal.example.co/api"))
        # fabricate-nothing / never-raise on odd input
        self.assertEqual(_redact_setting(None, None), ("scalar", ""))


class TestClusterBModuleDetection(unittest.TestCase):
    """Cluster B #5 — corpus-independent proof of the 3-signal union: comment-URL primary, then
    function-name recovery, then CSS footprint; presence-only behaviours; no un-whitelisted / no
    bare-mention emission; debug-noise resilience. Builds a synthetic app dir — needs no corpus."""

    def setUp(self):
        sys.path.insert(0, HERE)

    def _make_app(self, tmp, gs_text, css_files):
        srcdir = os.path.join(tmp, "ClientApp", "src")
        os.makedirs(srcdir, exist_ok=True)
        with open(os.path.join(srcdir, "global-scripts.js"), "w", encoding="utf-8") as f:
            f.write(gs_text)
        cssdir = os.path.join(tmp, "wwwroot", "Content", "EmbeddedFiles", "CSS")
        os.makedirs(cssdir, exist_ok=True)
        for c in css_files:
            with open(os.path.join(cssdir, c), "w", encoding="utf-8") as f:
                f.write("/* css */")

    def test_three_signal_union_and_behaviours(self):
        from extract_stadium_app import read_modules, FN_MODULE_MAP, CSS_MODULE_MAP
        gs = (
            "const scriptInstanceId = topLevelLogGroup; // consoleLogGroupHelper VITE_APP_DEBUG breadcrumb\n"
            "// https://github.com/stadium-software/conditional-datagrid-styling\n"
            "export const EditableRow = async (DataGridClass) => { logDebugInfo('EditableRow'); };\n"
            "  ConstructSearchPhrase: async(x) => {},\n"
            "function ParseColumnHeading(h) { return h; }\n"
            "const WorkflowSteps = async (ContainerClass, Steps) => {};\n"
            "  RoleSpecificStartPages: async(RolePages) => {},\n"
            "function AddTextBoxComponentValidation() {}   // FN_EXCLUDE helper — must never map\n"
            "// a bare mention of 'Accordion' in a comment must not count as a module\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            self._make_app(tmp, gs, ["tabs.css", "tabs-variables.css"])
            mods = read_modules(tmp, KB_DIR)
        by = {m["module"]: m["detection_source"] for m in mods["detected"]}
        self.assertEqual(by.get("conditional-datagrid-styling"), "url")   # comment-URL primary
        self.assertEqual(by.get("datagrid-inline-row-edit"), "fn")        # EditableRow, no URL
        self.assertEqual(by.get("filter-grid"), "fn")                     # ConstructSearchPhrase
        self.assertEqual(by.get("dynamic-datagrid"), "fn")                # ParseColumnHeading
        self.assertEqual(by.get("workflow-steps"), "fn")
        self.assertEqual(by.get("tabs"), "css")                           # CSS footprint
        # behaviours (presence-only): multi-step workflow + role→landing
        self.assertTrue(any("multi-step" in b for b in mods["behaviours"]))
        self.assertTrue(any("role" in b.lower() for b in mods["behaviours"]))
        # RoleSpecificStartPages is a behaviour, NOT a catalogued module
        self.assertNotIn("role-specific-startpage", by)
        # bare comment mention does not create a module; FN_EXCLUDE helper never maps
        self.assertNotIn("accordion", by)
        # no un-whitelisted emission: every fn/css slug is a real map value
        allowed = set(FN_MODULE_MAP.values()) | set(CSS_MODULE_MAP.values())
        for m in mods["detected"]:
            if m["detection_source"] in ("fn", "css"):
                self.assertIn(m["module"], allowed)

    def test_comment_url_wins_over_fn_and_css(self):
        from extract_stadium_app import read_modules
        gs = ("// https://github.com/stadium-software/datagrid-inline-row-edit\n"
              "const EditableRow = async () => {};\n")     # same slug via URL + fn
        with tempfile.TemporaryDirectory() as tmp:
            self._make_app(tmp, gs, ["datagrid-inline-edit.css"])   # ...and via CSS
            mods = read_modules(tmp, KB_DIR)
        by = {m["module"]: m["detection_source"] for m in mods["detected"]}
        self.assertEqual(by.get("datagrid-inline-row-edit"), "url")   # precedence: url > fn > css


class TestClusterCRenderedClientApp(unittest.TestCase):
    """Cluster C #6/#7/#8 — corpus-independent proof of the rendered `ClientApp/src` parsers. Pure
    helpers (_peel / stem / endpoint / divergence) are tested directly; the three readers run against a
    committed fixture tree copied into a temp app dir. Fixtures are PII-/secret-free (field names, page
    titles, column labels), so real-shaped snippets are safe to commit."""

    RENDERED_FIXTURE = os.path.join(FIXTURES, "rendered-clientapp")

    def setUp(self):
        sys.path.insert(0, HERE)

    def _make_app(self):
        """Copy the fixture ClientApp/src tree (router/types/views) into a temp app dir; returns the dir."""
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        dst = os.path.join(tmp, "ClientApp", "src")
        shutil.copytree(self.RENDERED_FIXTURE, dst)
        return tmp

    # ---- #8: _peel (every wrapper shape + fabricate-nothing fallback)
    def test_peel(self):
        from extract_stadium_app import _peel
        self.assertEqual(_peel("errorHandling.invoke(() => ('Edit'))"), "Edit")
        self.assertEqual(_peel("errorHandling.invoke(() => (typeResolver.toString('Account Name')))"), "Account Name")
        self.assertIs(_peel("errorHandling.invoke(() => (typeResolver.toBoolean(true)))"), True)
        self.assertIs(_peel("errorHandling.invoke(() => (false))"), False)
        self.assertEqual(_peel("'bare'"), "bare")
        self.assertIsNone(_peel("null"))
        self.assertIsNone(_peel("someUnknownFn(x)"))          # unrecognised → None, never fabricated
        self.assertIsNone(_peel(None))

    # ---- #6: variant-stem + authority (collapse, non-collapse, envelope/list exclusion)
    def test_rendered_entity_stem(self):
        from extract_stadium_app import _rendered_entity_stem
        self.assertEqual(_rendered_entity_stem("UserRead"), ("User", "display"))
        self.assertEqual(_rendered_entity_stem("UserWrite"), ("User", "editable"))
        self.assertEqual(_rendered_entity_stem("CustomerBasicRead"), ("Customer", "display"))   # Basic binds to Read
        self.assertEqual(_rendered_entity_stem("CustomerStatusRead"), ("CustomerStatus", "display"))  # Status stays
        self.assertEqual(_rendered_entity_stem("Role"), ("Role", "display"))                    # bare shape
        self.assertEqual(_rendered_entity_stem("MeetingCancel"), ("Meeting", "action"))
        self.assertEqual(_rendered_entity_stem("UserReadList"), (None, None))                   # list wrapper excluded
        self.assertEqual(_rendered_entity_stem("GeneralError"), (None, None))                   # envelope excluded
        self.assertEqual(_rendered_entity_stem("CustomerValidation"), (None, None))             # validation DTO excluded

    # ---- #8: endpoint decode (_46→. _95→_ ; connector/function split)
    def test_decode_endpoint(self):
        from extract_stadium_app import _decode_endpoint
        ep = _decode_endpoint("Sample", "SampleDataGrid_46Edit_46Click_46SampleUsersAPI_95UserGetById")
        self.assertEqual(ep["control"], "SampleDataGrid")
        self.assertEqual(ep["connector"], "SampleUsersAPI")
        self.assertEqual(ep["function"], "UserGetById")
        self.assertEqual(ep["decoded"], "SampleDataGrid.Edit.Click.SampleUsersAPI_UserGetById")

    # ---- #8: divergence-aware join (only surfaces deployed-vs-design mismatches)
    def test_column_divergences(self):
        from extract_stadium_app import _column_divergences
        sapz = [{"name": "AccountName", "header_text": "Account Name", "visible": True, "has_action": False},
                {"name": "BizUnit", "header_text": {"$type": "Expression"}, "visible": False, "has_action": False}]
        rendered = [{"name": "AccountName", "label": "Account Name", "visible": True, "clickable": False},
                    {"name": "BizUnit", "label": "Business Unit", "visible": False, "clickable": False},
                    {"name": "Extra", "label": "Extra Col", "visible": True, "clickable": False}]
        notes = "\n".join(_column_divergences(sapz, rendered))
        self.assertNotIn("AccountName", notes)                # identical → no note (no redundant echo)
        self.assertIn("header resolves to \"Business Unit\"", notes)   # Expression header resolved by rendered view
        self.assertIn("rendered-only column `Extra`", notes)

    # ---- #7: page-routes.js reader (redirect skip, BOM, title/component)
    def test_read_page_routes(self):
        from extract_stadium_app import read_page_routes
        routes = read_page_routes(self._make_app())
        names = [r["component"] for r in routes]
        self.assertEqual(names, ["Members", "MemberAdd", "MemberUpdate"])   # redirect-only entry skipped
        by = {r["component"]: r for r in routes}
        self.assertEqual(by["MemberAdd"]["title"], "Member Add")
        self.assertEqual(by["Members"]["path"], "/Members")                 # BOM tolerated (utf-8-sig)

    # ---- #6: types.js reader (union, relations, non-collapse, envelope/list/scaffolding exclusion)
    def test_read_client_types(self):
        from extract_stadium_app import read_client_types, _norm_entity
        types = read_client_types(self._make_app())
        by_norm = {}
        for t in types:
            by_norm.setdefault(t["norm"], []).append(t)
        stems = {t["entity"] for t in types}
        self.assertIn("User", stems)
        self.assertIn("Role", stems)
        self.assertIn("Customer", stems)
        self.assertIn("CustomerStatus", stems)                # distinct from Customer (Status stays)
        # envelopes / list wrapper / bare scaffolding excluded
        for excluded in ("GeneralError", "ValidationResult", "CustomerValidation", "UserReadList", "Filter"):
            self.assertNotIn(excluded, stems, f"{excluded} must not be a rendered entity")
        # UserRead + UserWrite variants both present (they collapse later in reconcile)
        user_variants = {t["variant"] for t in types if t["entity"] == "User"}
        self.assertEqual(user_variants, {"Read", "Write"})
        # nested relation Roles → Role resolved through the Array wrapper
        rel = next((t["relations"] for t in types if t["entity"] == "User" and t["variant"] == "Read"), {})
        self.assertEqual(rel.get("Roles"), "Role")
        # Id is read-only (Read only); Email editable (in Write)
        read_user = next(t for t in types if t["entity"] == "User" and t["variant"] == "Read")
        self.assertEqual({f["name"] for f in read_user["fields"]}, {"Id", "Email", "FirstName", "Roles"})

    # ---- #6: reconcile collapses the variants into one authoritative entity
    def test_reconcile_collapses_variants(self):
        from extract_stadium_app import read_client_types, reconcile_entities
        model = {"rendered_types": read_client_types(self._make_app())}
        entities, _ = reconcile_entities(model)
        by_disp = {e["display"]: e for e in entities.values()}
        self.assertIn("User", by_disp)
        fields = {f["name"]: f for f in by_disp["User"]["fields"]}
        self.assertEqual(set(fields), {"Id", "Email", "FirstName", "Roles"})       # UserRead ∪ UserWrite
        self.assertEqual(fields["Id"]["authority"], ["display"])                    # Read-only (Id only in Read)
        self.assertIn("editable", fields["Email"]["authority"])                     # in Write
        self.assertEqual(by_disp["User"]["rel"].get("Roles"), "Role")
        # envelope classes never become entities from the rendered path
        for k in entities:
            self.assertNotIn(k, {_norm for _norm in ("generalerror", "validationresult")})

    # ---- #8: view reader (peel labels, visible/clickable, endpoint decode)
    def test_read_view_columns(self):
        from extract_stadium_app import read_view_columns
        vc = read_view_columns(self._make_app())
        self.assertIn("Sample", vc)
        grid = vc["Sample"]["grids"]["SampleDataGrid"]
        by = {c["name"]: c for c in grid}
        self.assertEqual(by["Edit"]["label"], "Edit")
        self.assertTrue(by["Edit"]["clickable"])              # hasClickEvent: true (plain bool)
        self.assertFalse(by["Id"]["visible"])                 # visible: (false) peeled → hidden
        self.assertEqual(by["AccountName"]["label"], "Account Name")   # typeResolver.toString peeled
        self.assertTrue(by["AccountName"]["visible"])         # visible: (true) peeled
        self.assertFalse(by["AccountName"]["clickable"])      # hasClickEvent: false
        eps = {(e["control"], e["connector"], e["function"]) for e in vc["Sample"]["endpoints"]}
        self.assertIn(("SampleDataGrid", "SampleUsersAPI", "UserGetById"), eps)
        self.assertIn(("SaveButton", "SampleCustomersAPI", "CustomerUpdate"), eps)

    # ---- #8: the upgraded _columns_line shows the field-name binding + resolves Expression headers by name
    def test_columns_line_fieldname_binding(self):
        from extract_stadium_app import _columns_line
        cols = [{"name": "AccountName", "header_text": "Account Name", "visible": True, "kind": "data", "has_action": False},
                {"name": "Id", "header_text": "Id", "visible": False, "kind": "data", "has_action": False},
                {"name": "BizUnit", "header_text": {"$type": "Expression"}, "visible": False, "kind": "data"}]
        line = _columns_line(cols)
        self.assertIn('`AccountName` "Account Name"', line)    # field-name binding shown when it differs
        self.assertIn('"Id"(hidden)', line)                    # equal name/label → just the label
        self.assertIn('`BizUnit`(hidden)', line)               # Expression header → by name, never a raw blob
        self.assertNotIn("$type", line)


class TestDeriveViewTasks(unittest.TestCase):
    """Corpus-INDEPENDENT proof of the deterministic per-view USER TASK derivation
    (`_derive_view_tasks` + helpers). Feeds a synthetic MemberAdmin-shaped `views` list so the
    algorithm's contract is locked without the out-of-repo corpus. Covers: multi-source
    triangulation, within-view dedup on the canonical CRUD verb (NOT the update+delete cluster),
    the SELECT supporting-reads suppression, closed-set entity binding (never invent / never bind to
    the connector name), and the ≥1-task-per-view completeness guarantee."""

    def setUp(self):
        sys.path.insert(0, HERE)

    @staticmethod
    def _views():
        from extract_stadium_app import _norm_entity
        ent_by_norm = {_norm_entity("Members"): {"display": "Members", "norm": _norm_entity("Members")},
                       _norm_entity("Cities"):  {"display": "Cities",  "norm": _norm_entity("Cities")}}
        cols = [{"header_text": "Edit", "kind": "action"}, {"header_text": "Delete", "kind": "action"},
                {"header_text": "ID", "name": "ID", "kind": "data"},
                {"header_text": "First Name", "name": "FirstName", "kind": "data"}]
        views = [
            {"name": "Members", "title": "Members", "kind": "entity-maintenance",
             "roles": ["User", "Viewer", "AllAccess"], "screen_entity": "Members",
             "endpoints": [{"control": "MembersDataGrid", "connector": "Members", "function": "MemberDelete"},
                           {"control": "MembersDGLoad", "connector": "Members", "function": "MembersSelect"}],
             "grids": [{"name": "MembersDataGrid", "searchable": True, "columns": cols}],
             "affordances": [("MemberAddButton", "Add Member", "add", ["MemberAddButton.Click"])]},
            {"name": "MemberAdd", "title": "Member Add", "kind": "create", "roles": ["AllAccess"],
             "screen_entity": None,
             "endpoints": [{"control": "SaveButton", "connector": "Members", "function": "MemberInsert"},
                           {"control": "MemberAdd", "connector": "Members", "function": "CitiesSelect"}],
             "grids": [], "affordances": []},
            {"name": "MemberUpdate", "title": "Member Update", "kind": "entity-maintenance",
             "roles": ["AllAccess"], "screen_entity": None,
             "endpoints": [{"control": "SaveButton", "connector": "Members", "function": "MemberUpdate"},
                           {"control": "MemberUpdate", "connector": "Members", "function": "MemberSelect"},
                           {"control": "MemberUpdate", "connector": "Members", "function": "CitiesSelect"}],
             "grids": [], "affordances": []},
            {"name": "Login", "title": "Login", "kind": "landing", "roles": [],
             "screen_entity": None, "endpoints": [], "grids": [], "affordances": []},
        ]
        return views, ent_by_norm

    def _by_view(self):
        from extract_stadium_app import _derive_view_tasks
        views, ent_by_norm = self._views()
        return {vt["name"]: vt for vt in _derive_view_tasks(views, ent_by_norm)}

    def test_members_view_yields_four_distinct_crud_tasks(self):
        m = self._by_view()["Members"]
        got = {(t["verb"], t["entity"]): t for t in m["tasks"]}
        # update + delete stay SEPARATE (dedup is on the CRUD verb, not the update+delete cluster)
        self.assertEqual({k[0] for k in got}, {"SELECT", "INSERT", "UPDATE", "DELETE"})
        for (verb, ent) in got:
            self.assertEqual(ent, "Members")
        # browse triangulated (grid + wired SELECT) -> high; delete (endpoint + action col) -> high
        self.assertEqual(got[("SELECT", "Members")]["conf"], "high")
        self.assertEqual(got[("DELETE", "Members")]["conf"], "high")
        self.assertEqual(got[("INSERT", "Members")]["name"], "Add Member")   # app's own affordance wording kept
        self.assertEqual(got[("UPDATE", "Members")]["name"], "Update Members")  # single-word "Edit" -> synth
        # the browse task carries BOTH its grid and its corroborating endpoint as evidence
        self.assertTrue(any("MembersDataGrid" in e for e in got[("SELECT", "Members")]["ev"]))
        self.assertTrue(any("MembersSelect" in e for e in got[("SELECT", "Members")]["ev"]))

    def test_write_endpoint_synthesizes_name_and_binds_entity_from_stem(self):
        # A wired WRITE is a high-confidence task; its name is synthesized <Verb> <Entity> (NOT the
        # page title — that would collapse every write on a multi-write page to one name), and the
        # entity is bound from the function stem (MemberInsert -> Members).
        v = self._by_view()
        add = v["MemberAdd"]["tasks"]
        self.assertEqual(len(add), 1)
        self.assertEqual((add[0]["verb"], add[0]["entity"], add[0]["name"], add[0]["conf"]),
                         ("INSERT", "Members", "Add Members", "high"))
        upd = v["MemberUpdate"]["tasks"]
        self.assertEqual([(t["verb"], t["entity"], t["name"]) for t in upd],
                         [("UPDATE", "Members", "Update Members")])

    def test_select_lookups_are_supporting_reads_not_tasks(self):
        v = self._by_view()
        # CitiesSelect (dropdown) and MemberSelect (form pre-fill) never become "Browse Cities/Member"
        for name in ("MemberAdd", "MemberUpdate"):
            for t in v[name]["tasks"]:
                self.assertNotEqual(t["verb"], "SELECT", f"{name}: a lookup SELECT leaked as a task")
        self.assertTrue(any("CitiesSelect" in s for s in v["MemberAdd"]["supporting_reads"]))
        self.assertTrue(any("MemberSelect" in s for s in v["MemberUpdate"]["supporting_reads"]))

    def test_completeness_guarantee_and_no_fabricated_entity(self):
        from extract_stadium_app import _derive_view_tasks
        v = self._by_view()
        # every non-chrome view has >=1 task; the chrome/landing view is explicitly declared, not dropped
        self.assertTrue(v["Members"]["tasks"] and v["MemberAdd"]["tasks"] and v["MemberUpdate"]["tasks"])
        self.assertEqual(v["Login"]["tasks"], [])
        self.assertIn("landing", v["Login"]["notask"])
        # closed-set discipline: an op whose stem is not a reconciled entity binds no entity (never invents)
        views, ent_by_norm = self._views()
        orphan = [{"name": "Widgets", "title": "Widgets", "kind": "entity-maintenance", "roles": [],
                   "screen_entity": None, "grids": [], "affordances": [],
                   "endpoints": [{"control": "b", "connector": "X", "function": "GadgetInsert"}]}]
        got = _derive_view_tasks(orphan, ent_by_norm)[0]["tasks"]
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["verb"], "INSERT")
        self.assertIsNone(got[0]["entity"])          # "Gadget" not in the closed set -> blank, not invented

    def test_endpoint_verb_entity_uses_stem_not_connector(self):
        from extract_stadium_app import _endpoint_verb_entity, _norm_entity
        ebn = {_norm_entity("Cities"): {"display": "Cities", "norm": _norm_entity("Cities")},
               _norm_entity("Members"): {"display": "Members", "norm": _norm_entity("Members")}}
        # CitiesSelect must resolve to Cities via the function stem, NOT to its "Members" connector
        self.assertEqual(_endpoint_verb_entity("CitiesSelect", ebn), ("SELECT", "Cities"))
        self.assertEqual(_endpoint_verb_entity("MemberInsert", ebn), ("INSERT", "Members"))
        self.assertEqual(_endpoint_verb_entity("Frobnicate", ebn), (None, None))   # no CRUD keyword


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
    """Run the real extractor over the 4-app subset; assert it exits 0, writes all eleven Tier-1
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
class TestClusterBLiveRender(unittest.TestCase):
    """Cluster B live-render checks over the subset: every detected module line carries a
    `[detected via: …]` source tag; the `.sapz Setting` integration block renders where Setting
    rows exist (RMB/Payments); and no unredacted password ever reaches the data-sources asset."""

    def test_modules_tagged_and_settings_rendered(self):
        subset = _resolve_subset()
        if not subset:
            self.skipTest(f"none of {SUBSET} found in the corpus")
        saw_settings = False
        for name, folder in subset:
            with self.subTest(app=name), tempfile.TemporaryDirectory() as tmp:
                rc, out, err = _run_extractor(folder, tmp, name)
                self.assertEqual(rc, 0, f"[{name}] extractor exited {rc}\n{err}")
                with open(os.path.join(tmp, f"{name}.stadium.modules.md"), encoding="utf-8") as fh:
                    for line in fh:
                        if line.startswith("- **") and "github.com/stadium-software" in line:
                            self.assertIn("[detected via:", line,
                                          f"[{name}] module line missing detection_source: {line!r}")
                with open(os.path.join(tmp, f"{name}.stadium.data-sources.md"), encoding="utf-8") as fh:
                    ds = fh.read()
                if "## Tier-A — app settings / integration" in ds:
                    saw_settings = True
                    seg = ds.split("## Tier-A — app settings / integration", 1)[1]
                    # large/markup Setting values (e.g. RMB's MenuItems HTML) collapse to a presence
                    # note — never dumped raw into the integration block.
                    self.assertNotIn("<div", seg, f"[{name}] raw UI markup leaked into the Setting block")
        self.assertTrue(saw_settings,
                        "expected >=1 subset app to render the .sapz Setting integration block")

    def test_no_unredacted_password_in_data_sources(self):
        """Secret-leak guard (belt-and-braces over read-time redaction): every connection-string
        `Password=<value>` in the data-sources asset — connector strings AND Setting `connection`
        rows — must be `<redacted>`. Matches only the no-space `Key=Value;` connection-string form
        (`sanitize_conn` emits `Password=<redacted>`), so SQL `WHERE Password = @p` and `@`-params
        are not mistaken for leaks."""
        import re
        subset = _resolve_subset()
        if not subset:
            self.skipTest(f"none of {SUBSET} found in the corpus")
        for name, folder in subset:
            with self.subTest(app=name), tempfile.TemporaryDirectory() as tmp:
                rc, out, err = _run_extractor(folder, tmp, name)
                self.assertEqual(rc, 0, f"[{name}] extractor exited {rc}\n{err}")
                with open(os.path.join(tmp, f"{name}.stadium.data-sources.md"), encoding="utf-8") as fh:
                    ds = fh.read()
                for m in re.finditer(r"(?i)(?:password|pwd)=([^\s;`]+)", ds):   # connection-string form only
                    val = m.group(1)
                    if val.startswith("@"):                 # SQL parameter placeholder, not a value
                        continue
                    self.assertTrue(val.lower().startswith("<redacted>"),
                                    f"[{name}] unredacted connection-string password in data-sources: {m.group(0)!r}")


@unittest.skipUnless(_HAS_CORPUS, _SKIP_CORPUS_MSG)
class TestUntouchedAssetsByteIdentical(unittest.TestCase):
    """Cluster A touched `business-rules`, `surfaces`, `overview`; Cluster B additionally touches
    `data-sources` (the Setting integration block) and `modules` (detection_source + behaviours);
    Cluster C additionally touches `navigation` (#7 route reachability) and `data-model` (#6 rendered
    types.js §7 fields). Assert every OTHER Tier-1 asset is byte-identical to its checked-in golden
    snapshot — a HARD fail on drift. Skips cleanly until goldens are seeded (--update-goldens).
    The `tasks` enrichment additionally touches `surfaces` (0e → pointer) and adds the new `tasks`
    asset + the `overview` index row. UNTOUCHED stays {access-control, glossary, design-signals}."""

    UNTOUCHED = [c for c in TIER1_CATEGORIES if c not in
                 ("business-rules", "surfaces", "overview",      # Cluster A
                  "data-sources", "modules",                     # Cluster B
                  "navigation", "data-model",                    # Cluster C (#7, #6)
                  "tasks")]                                      # per-view user-task inventory (new asset)

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


@unittest.skipUnless(_HAS_CORPUS, _SKIP_CORPUS_MSG)
class TestClusterCLiveOverSubset(unittest.TestCase):
    """Cluster C — live-render checks over the subset: the empty-`types.js` no-op (the critical safety
    assertion — rendered parsing must never corrupt a pure-SQL app's data model), and the positive #6/#7/#8
    signal on the web-service subset app (PaymentsApp)."""

    def _emit(self, name):
        subset = dict((n.lower(), f) for n, f in _resolve_subset())
        folder = subset.get(name.lower())
        if not folder:
            self.skipTest(f"{name} not in the discovered corpus")
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        rc, out, err = _run_extractor(folder, tmp, name)
        self.assertEqual(rc, 0, f"[{name}] extractor exited {rc}\n{err}")
        return tmp

    def test_empty_types_js_is_a_data_model_noop(self):
        """MemberAdmin + ResourceCenter have an empty `types.js` → #6 must contribute NOTHING: no
        `[from rendered types]` locator and no rendered-authority tag anywhere in the data model. This is
        the fabricate-nothing / never-corrupt-a-pure-SQL-app guarantee (byte-identity is additionally
        locked by TestUntouchedAssetsByteIdentical's golden comparison once goldens are seeded)."""
        for name in ("MemberAdmin", "ResourceCenter"):
            with self.subTest(app=name):
                tmp = self._emit(name)
                dm = open(os.path.join(tmp, f"{name}.stadium.data-model.md"), encoding="utf-8").read()
                self.assertNotIn("from rendered types", dm)
                self.assertNotIn("· editable", dm)
                self.assertNotIn("· read-only", dm)

    def test_paymentsapp_rendered_types_and_endpoints(self):
        """PaymentsApp (1366-line types.js, 23 views) exercises #6 + #8 end-to-end: rendered §7 fields with
        authority, the field-name column binding, endpoint source-UI references, and route reachability."""
        tmp = self._emit("PaymentsApp")
        dm = open(os.path.join(tmp, "PaymentsApp.stadium.data-model.md"), encoding="utf-8").read()
        sf = open(os.path.join(tmp, "PaymentsApp.stadium.surfaces.md"), encoding="utf-8").read()
        nav = open(os.path.join(tmp, "PaymentsApp.stadium.navigation.md"), encoding="utf-8").read()
        self.assertIn("from rendered types", dm)                      # #6 rendered §7 fields present
        self.assertIn("editable", dm)                                 # per-field authority rendered
        self.assertRegex(sf, r"`[A-Za-z]+` \"[A-Za-z ]+\"")           # #2/#8 field-name binding in a column line
        self.assertIn("source-UI reference", sf)                      # #8 endpoint block
        self.assertIn("PaymentsApi", sf)                              # decoded connector name
        self.assertIn("Route-declared?", sf)                          # #7 inventory column
        self.assertIn("reachable via a declared client route", nav)   # #7 reachability reclassification

    def test_no_envelope_entities_across_subset(self):
        """DA#4 — no transport/response envelope class becomes a §7 entity on ANY subset app (from any
        source), and every rendered field carries the `[from rendered types]` locator."""
        import re as _re
        for name, _ in _resolve_subset():
            with self.subTest(app=name):
                tmp = self._emit(name)
                dm = open(os.path.join(tmp, f"{name}.stadium.data-model.md"), encoding="utf-8").read()
                for env in ("GeneralError", "GeneralResponse", "ResponseId", "ResponseMessage",
                            "ValidationResult", "DefaultResponse", "CustomerValidation"):
                    self.assertFalse(_re.search(rf"(?m)^### {env}\b", dm),
                                     f"[{name}] envelope class {env} leaked into §7 entities")


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
