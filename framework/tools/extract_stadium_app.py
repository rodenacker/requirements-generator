#!/usr/bin/env python3
"""
extract_stadium_app.py  --  Deterministic fact extractor for Twenty57 Stadium 6 web apps.

Reverse-engineers a single Stadium application folder into a structured, lossless-ish
"facts bundle" that AI analyst agents reason over. It does NOT interpret intent --
it only reports what is provably present in the source.

Primary source of truth: the `.sapz` deployment package (a ZIP containing a `sqlitedata`
SQLite database -- the Stadium Designer's design-time model). Falls back to / supplements
with administration.db, appsettings.json, package.json and the generated ClientApp.

USAGE
    python extract_stadium_app.py <app_folder> [--out <output_dir>]

OUTPUT (written to <output_dir>, default: ./analysis-output/<WebAppName>/)
    model.json     full structured facts (machine-readable; for agents & prototype generators)
    inventory.md   human-readable digest of the same facts

The script is defensive: every section is wrapped so a partial/odd app still yields a
usable bundle. Anything it cannot determine is recorded under "gaps" rather than guessed.
"""

import sys, os, json, zipfile, sqlite3, uuid, glob, argparse, tempfile, shutil, re
from datetime import datetime, timezone

# --------------------------------------------------------------------------- helpers

def norm_guid(v):
    """Stadium stores GUIDs as either a 16-byte .NET blob (bytes_le) or a string. Normalise both."""
    if v is None:
        return None
    if isinstance(v, (bytes, bytearray)):
        if len(v) == 16:
            try:
                return str(uuid.UUID(bytes_le=bytes(v)))
            except Exception:
                return v.hex()
        return v.hex()
    s = str(v).strip()
    try:
        return str(uuid.UUID(s))
    except Exception:
        return s

# Stadium Decision.Condition int enums, decoded empirically over the 20-app corpus by correlating
# each condition's Operator int against the operator PHRASE Stadium embeds in its auto-generated
# Decision node names (e.g. `DecisionCF...GreaterThanOrEquals0`, `dec...OrBefore`) + literal-value
# samples. Standard comparison ordering. op0/op3/op5 corpus-confirmed; op1/op2/op4 best-guess
# (consultant-approved, 2026-07-02). Any unmapped code degrades to `op<N>` — never a wrong symbol.
DECISION_OP_SYMBOLS = {0: "==", 1: "!=", 2: "<", 3: "<=", 4: ">", 5: ">="}
DECISION_JOIN_SYMBOLS = {0: "AND", 1: "OR"}   # 0 dominant (1495x); 1 = OR (43x)

def op_symbol(v):
    try:
        return DECISION_OP_SYMBOLS.get(int(v), f"op{v}")
    except (TypeError, ValueError):
        return f"op{v}"

def join_word(v):
    try:
        return DECISION_JOIN_SYMBOLS.get(int(v), f"join{v}")
    except (TypeError, ValueError):
        return f"join{v}"

def friendly_type(translation_type):
    """'Twenty57.Stadium.Controls.Label, Twenty57...' -> 'Label'."""
    if not translation_type:
        return None
    head = str(translation_type).split(",")[0].strip()
    return head.split(".")[-1]

def friendly_name(name):
    """Strip the auto-appended 32-hex suffix Stadium adds to layout controls."""
    if not name:
        return name
    return re.sub(r"_[0-9a-f]{32}$", "", str(name))

def parse_props(jsondata):
    """A Stadium JsonData blob is an array of {Name, ValueType, Value} PropertyDataItems.
    Return {Name: value}. Values that are themselves JSON (bindings/expressions) are kept as parsed objects."""
    out = {}
    if not jsondata:
        return out
    try:
        items = json.loads(jsondata)
    except Exception:
        return {"_raw": str(jsondata)[:2000]}
    if not isinstance(items, list):
        return out
    for it in items:
        if not isinstance(it, dict) or "Name" not in it:
            continue
        val = it.get("Value")
        if isinstance(val, str) and val and val[0] in "[{":
            try:
                val = json.loads(val)
            except Exception:
                pass
        out[it["Name"]] = val
    return out

def safe(fn, default=None):
    try:
        return fn()
    except Exception as e:
        return default if default is not None else {"_error": str(e)}

def sanitize_conn(s):
    """Redact passwords in a connection string while keeping shape/host/db visible.
    Accepts a raw string or an already-parsed dict (filesystem connector stores JSON {Path,User,Password})."""
    if not s:
        return s
    if isinstance(s, dict):
        d = dict(s)
        for k in list(d):
            if str(k).lower() in ("password", "pwd"):
                d[k] = "<redacted>" if d[k] else ""
        return json.dumps(d)
    if not isinstance(s, str):
        return str(s)
    s = re.sub(r"(?i)(password|pwd)\s*=\s*[^;]*", r"\1=<redacted>", s)
    try:  # filesystem connector stores JSON {Path,User,Password}
        d = json.loads(s)
        if isinstance(d, dict) and "Password" in d:
            d["Password"] = "<redacted>" if d["Password"] else ""
            return json.dumps(d)
    except Exception:
        pass
    return s

# --- Cluster B #4-B: classify + redact a `.sapz` `Setting` row. The `IsSecret` column is
# UNRELIABLE (0 even on password/API-key rows across the whole corpus), so secret detection is
# driven by the Name pattern, never the flag. Redaction happens at READ time so no secret value
# ever reaches model.json. Returns (kind, redacted_value); never raises, never emits a secret.
_SECRET_NAME_RE = re.compile(r"(?i)(key|secret|password|pwd|token|apikey)")
_CONNSTR_RE = re.compile(r"(?i)(server\s*=|data source\s*=|user id\s*=|password\s*=|\"Password\"\s*:)")
_HTTP_URL_RE = re.compile(r"(?i)^\s*https?://")
_WINPATH_RE = re.compile(r"^\s*([A-Za-z]:\\|\\\\)")

def _redact_setting(name, value):
    nm = name or ""
    sval = value if isinstance(value, str) else ("" if value is None else str(value))
    if _SECRET_NAME_RE.search(nm):                         # secret-shaped NAME -> presence only
        return ("credential", "<redacted>")
    if _CONNSTR_RE.search(sval):                           # connection string -> reuse sanitize_conn
        return ("connection", sanitize_conn(sval))
    if _HTTP_URL_RE.match(sval):                           # URL -> keep scheme+host+path, drop query/#
        return ("endpoint", _redact_pii(sval.strip().split("#", 1)[0].split("?", 1)[0]))
    if _WINPATH_RE.match(sval):                            # filesystem path -> handoff fact (PII-scrubbed)
        return ("path", _redact_pii(sval.strip()))
    return ("scalar", _redact_pii(sval.strip()))           # e.g. DepartmentID

# System.Data.DbType enum -> readable name (Stadium DB connector stores params by this enum)
DBTYPE = {0:"AnsiString",1:"Binary",2:"Byte",3:"Boolean",4:"Currency",5:"Date",6:"DateTime",
          7:"Decimal",8:"Double",9:"Guid",10:"Int16",11:"Int32",12:"Int64",13:"Object",
          14:"SByte",15:"Single",16:"String",17:"Time",18:"UInt16",19:"UInt32",20:"UInt64",
          21:"VarNumeric",22:"AnsiStringFixedLength",23:"StringFixedLength",25:"Xml",
          26:"DateTime2",27:"DateTimeOffset"}

def dbtype_name(v):
    try:
        return DBTYPE.get(int(v), v)
    except Exception:
        return v

def _count_types(controls):
    from collections import Counter
    c = Counter(x.get("type") or "Unknown" for x in controls)
    return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))

def table_names(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return {r[0] for r in cur.fetchall()}

def rows(cur, table, cols="*"):
    try:
        cur.execute(f'SELECT {cols} FROM "{table}"')
        return [dict(r) for r in cur.fetchall()]
    except Exception:
        return []

# --------------------------------------------------------------------------- sapz selection

def select_design_model(app_dir, workdir):
    """Extract the most recent .sapz deployment package; return path to its sqlitedata + metadata."""
    updates_dir = os.path.join(app_dir, "App_Data", "Updates")
    sapz = glob.glob(os.path.join(updates_dir, "*.sapz"))
    if not sapz:
        return None, {"note": "No .sapz deployment packages found under App_Data/Updates"}

    # Prefer ordering by ApplicationUpdates.DateTime (admin db) when available.
    order = {}
    admin = os.path.join(app_dir, "administration.db")
    if os.path.exists(admin):
        try:
            c = sqlite3.connect(admin); c.row_factory = sqlite3.Row
            # Username (publisher identity) is intentionally NOT read — PII, not needed.
            for r in c.execute("SELECT Id, DateTime, DesignerVersion FROM ApplicationUpdates"):
                order[str(r["Id"]).lower()] = (r["DateTime"], r["DesignerVersion"])
            c.close()
        except Exception:
            pass

    def keyfn(p):
        gid = os.path.splitext(os.path.basename(p))[0].lower()
        if gid in order and order[gid][0]:
            return order[gid][0]
        return datetime.fromtimestamp(os.path.getmtime(p), tz=timezone.utc).isoformat()

    sapz.sort(key=keyfn)
    chosen = sapz[-1]
    dest = os.path.join(workdir, "design")
    os.makedirs(dest, exist_ok=True)
    with zipfile.ZipFile(chosen) as z:
        z.extractall(dest)
    sqlitedata = os.path.join(dest, "sqlitedata")
    meta = {
        "selected_package": os.path.basename(chosen),
        "package_count": len(sapz),
        "all_deployments": [
            {"id": os.path.splitext(os.path.basename(p))[0],
             "datetime": order.get(os.path.splitext(os.path.basename(p))[0].lower(), [None])[0],
             "designer_version": order.get(os.path.splitext(os.path.basename(p))[0].lower(), [None, None])[1] if order.get(os.path.splitext(os.path.basename(p))[0].lower()) else None}
            for p in sapz
        ],
        "embedded_files_dir": os.path.join(dest, "EmbeddedFiles"),
    }
    return (sqlitedata if os.path.exists(sqlitedata) else None), meta

# --------------------------------------------------------------------------- design model

def read_design_model(sqlitedata):
    con = sqlite3.connect(sqlitedata); con.row_factory = sqlite3.Row
    cur = con.cursor()
    tn = table_names(cur)
    model = {}

    # --- registry of every named entity, keyed by normalised GUID, for parent resolution
    registry = {}      # guid -> {kind, name, type, parent}
    children = {}      # parent guid -> [child guid]

    def register(kind, table):
        if table not in tn:
            return []
        out = []
        for r in rows(cur, table):
            d = dict(r)
            gid = norm_guid(d.get("ID"))
            pid = norm_guid(d.get("ParentID"))
            entry = {
                "id": gid, "parent": pid, "kind": kind,
                "name": d.get("Name"),
                "type": friendly_type(d.get("TranslationType")),
                "translation_type": d.get("TranslationType"),
                "props": parse_props(d.get("JsonData")) if "JsonData" in d else {},
                "raw": {k: v for k, v in d.items() if k not in ("JsonData",)},
            }
            if gid:
                registry[gid] = entry
                children.setdefault(pid, []).append(gid)
            out.append(entry)
        return out

    pages_e      = register("page", "Page")
    templates_e  = register("template", "Template")
    controls_e   = register("control", "StadiumControl")
    scripts_e    = register("script", "Script")
    scriptitems_e= register("scriptitem", "ScriptItem")
    connectors_e = register("connector", "Connector")
    connfuncs_e  = register("connectorfunction", "ConnectorFunction")
    params_e     = register("parameter", "Parameter")
    sessvars_e   = register("sessionvariable", "SessionVariable")
    customtypes_e= register("customtype", "CustomType")
    validators_e = register("validator", "Validator")
    # Structural passthrough nodes (grid cells, repeater items, etc.) link controls to their layout parents.
    register("expando", "UniqueItemExpando")
    register("folder", "Folder")
    # Data-model type system — registered so the WebService/StoredProcedure data-model shapers
    # can walk a function's request/response shapes through the same children{} machinery.
    # (These are parented to Parameters/DataResults/CustomTypes, never to Pages, so the existing
    #  control-tree / owner_page / action walkers ignore them.)
    register("dataresult", "DataResult")
    register("structtype", "StructDataType")
    register("listtype",   "ListDataType")
    register("simpletype", "SimpleDataType")
    register("field",      "Field")

    # CustomType id -> name: the name dictionary a WebService Body/ResponseType GuidReference
    # resolves against (e.g. NamedItemID -> "fullmember"). CustomTypes are heavily used and
    # carry names in web-service apps, contrary to the older "usually empty" assumption.
    type_names = {e["id"]: e["name"] for e in customtypes_e if e.get("name")}
    model["type_names"] = type_names

    def struct_field_list(struct_id, depth=0, seen=None):
        """Flatten a StructDataType's Field members -> [{name, path, type, is_data_field, nested}].
        Follows Field->StructDataType (object) and Field->ListDataType->StructDataType (array);
        depth-capped + cycle-safe. Primitive type comes from the field's child SimpleDataType
        (often the weak `Object` for API shapes; names are the reliable part)."""
        seen = seen if seen is not None else set()
        if not struct_id or struct_id in seen or depth > 4:
            return []
        seen.add(struct_id)
        out = []
        for cid in children.get(struct_id, []):
            e = registry.get(cid)
            if not e or e["kind"] != "field":
                continue
            fname = (e.get("raw") or {}).get("Name")
            if not fname:
                continue
            is_df = bool((e.get("raw") or {}).get("IsDataField"))
            ftype, nested_struct, is_list = None, None, False
            for gc in children.get(cid, []):
                ge = registry.get(gc)
                if not ge:
                    continue
                if ge["kind"] == "simpletype":
                    ftype = friendly_type((ge.get("raw") or {}).get("TypeName"))
                elif ge["kind"] == "structtype":
                    nested_struct = gc
                elif ge["kind"] == "listtype":
                    is_list = True
                    for lc in children.get(gc, []):
                        if (registry.get(lc) or {}).get("kind") == "structtype":
                            nested_struct = lc
            disp_type = (ftype + "[]") if (is_list and ftype) else ftype
            out.append({"name": fname, "path": fname, "type": disp_type,
                        "is_data_field": is_df, "nested": bool(nested_struct)})
            if nested_struct:
                for sub in struct_field_list(nested_struct, depth + 1, seen):
                    out.append({"name": sub["name"], "path": f"{fname}.{sub['path']}",
                                "type": sub["type"], "is_data_field": sub["is_data_field"],
                                "nested": sub["nested"]})
        return out

    def _child_struct_of(owner_id):
        """First StructDataType directly under owner_id (a Parameter or DataResult)."""
        for cid in children.get(owner_id, []):
            if (registry.get(cid) or {}).get("kind") == "structtype":
                return cid
        return None

    def _ref_customtype_name(ref):
        """A BodyType/ResponseType GuidReference dict -> the CustomType name it points at."""
        if not isinstance(ref, dict):
            return None
        nid = ref.get("NamedItemID")
        return type_names.get(norm_guid(nid)) if nid else None

    def _resolve_ws_hint(func_id, fprops):
        """WebService function -> {http_method, path, body_name, resp_name, body_fields, resp_fields}.
        NAME from the Body/Response CustomType ref; FIELDS from the function's own bound
        Parameter(Body) / DataResult(ResponseBody) struct."""
        body_fields, resp_fields = [], []
        for cid in children.get(func_id, []):
            e = registry.get(cid)
            if not e:
                continue
            if e["kind"] == "parameter":
                nm = (e.get("name") or "").lower()
                if nm == "body" or (e.get("props") or {}).get("ParameterType") == 4:
                    s = _child_struct_of(cid)
                    if s and not body_fields:
                        body_fields = struct_field_list(s)
            elif e["kind"] == "dataresult" and (e.get("name") or "").lower() == "responsebody":
                s = _child_struct_of(cid)
                if s and not resp_fields:
                    resp_fields = struct_field_list(s)
        return {"http_method": fprops.get("HttpMethod"), "path": fprops.get("Path"),
                "body_name": _ref_customtype_name(fprops.get("BodyType")),
                "resp_name": _ref_customtype_name(fprops.get("ResponseType")),
                "body_fields": body_fields, "resp_fields": resp_fields}

    def _resolve_sp_hint(fprops, params):
        """StoredProcedure function -> {proc_name, params, param_types} (params are the fields)."""
        return {"proc_name": fprops.get("Text") or fprops.get("CommandText") or fprops.get("Query"),
                "params": [p.get("name") for p in params if p.get("name")],
                "param_types": {p.get("name"): (p.get("db_type") or p.get("type"))
                                for p in params if p.get("name")}}

    def owner_page(gid):
        """Walk parents up to a page/template."""
        seen = set()
        cur_id = gid
        while cur_id and cur_id in registry and cur_id not in seen:
            seen.add(cur_id)
            e = registry[cur_id]
            if e["kind"] in ("page", "template"):
                return e["name"], e["kind"]
            cur_id = e["parent"]
        return None, None

    # ----- Application
    app = {}
    if "Application" in tn:
        a = rows(cur, "Application")
        if a:
            d = a[0]
            app = {
                "name": d.get("Name"),
                "designer_version": d.get("DesignerVersion"),
                "file_guid": d.get("FileGuid"),
                "theme": d.get("Theme"),
                "start_page_id": norm_guid(d.get("StartPageId")),
                "session_timeout": d.get("SessionTimeout"),
                "max_file_upload_size": d.get("MaxFileUploadSize"),
                "stylesheet_enabled": bool(d.get("IsStyleSheetEnabled")),
                "stylesheet": d.get("StyleSheet"),
                "head_html": d.get("Head"),
            }
    model["application"] = app

    # ----- Pages (with control tree + load script)
    KEY_PROP_NAMES = ("Text", "Label", "Classes", "Visible", "Placeholder", "Value",
                      "Heading", "Title", "Source", "List", "Url", "NavigateUrl",
                      "HeaderText", "Required", "Enabled", "Columns",
                      # --- field-behaviour props surfaced by Cluster A #1 (render-only; already parsed
                      # into all_props). Widening the allowlist lights up BOTH key_props stores at once
                      # (control_tree :416 + flat all_controls :459). AllowMultiple is deliberately omitted
                      # (0/5029 controls in the corpus — dead prop).
                      "IsValidRule", "ErrorText", "Hint", "ToolTip", "ReadOnly", "IsPassword",
                      "Options", "OptionsField", "VisibleLines", "Rows",
                      "AllowExport", "DisplaySearchBar", "HasSelectableData",
                      "AllowedExtensions", "FilesField")

    def build_tree(parent_id):
        """Build the nested control tree. Non-control containers (grid cells, repeater
        items, folders) are traversed transparently so their controls surface in place."""
        out = []
        for cid in children.get(parent_id, []):
            e = registry.get(cid)
            if not e:
                continue
            if e["kind"] != "control":
                # passthrough: splice the container's control descendants in at this level
                if e["kind"] in ("expando", "folder"):
                    out.extend(build_tree(cid))
                continue
            props = e["props"]
            node = {
                "name": friendly_name(e["name"]),
                "raw_name": e["name"],
                "type": e["type"],
                "id": cid,
                "key_props": {k: props[k] for k in KEY_PROP_NAMES if k in props},
                "all_props": props,
                "children": build_tree(cid),
            }
            if props.get("Columns"):        # Cluster A #2 — resolve DataGrid column GUIDs here (registry
                node["columns"] = _resolve_columns(props, registry)   # is in scope only at build time)
            out.append(node)
        return out

    pages = []
    start_id = app.get("start_page_id")
    for e in pages_e:
        pid = e["id"]
        p = e["raw"]
        pages.append({
            "name": p.get("Name"),
            "title": p.get("Title"),
            "is_start_page": (pid == start_id),
            "load_script_id": norm_guid(p.get("LoadEventHandlerScriptId")),
            "control_tree": build_tree(pid),
        })
    model["pages"] = pages

    templates = []
    for e in templates_e:
        t = e["raw"]
        templates.append({
            "name": t.get("Name"),
            "is_default": bool(t.get("IsDefaultTemplate")),
            "load_script_id": norm_guid(t.get("LoadEventHandlerScriptId")),
            "control_tree": build_tree(e["id"]),
        })
    model["templates"] = templates

    # ----- Flat list of EVERY control (safety net: complete even if tree linkage is imperfect)
    all_controls = []
    for e in controls_e:
        props = e["props"]
        owner, owner_kind = owner_page(e["parent"]) if e["parent"] else (None, None)
        all_controls.append({
            "name": friendly_name(e["name"]),
            "raw_name": e["name"],
            "type": e["type"],
            "owner_page": owner,
            "owner_kind": owner_kind,
            "key_props": {k: props[k] for k in KEY_PROP_NAMES if k in props},
        })
    model["all_controls"] = all_controls
    model["control_type_counts"] = _count_types(all_controls)

    # ----- Connectors with functions, queries, parameters
    connectors = []
    for e in connectors_e:
        cprops = e["props"]
        conn = {
            "name": e["name"],
            "type": e["type"],
            "connection_string": sanitize_conn(cprops.get("ConnectionString")),
            "functions": [],
        }
        for f in connfuncs_e:
            if f["parent"] != e["id"]:
                continue
            fprops = f["props"]
            params = []
            for pr in params_e:
                if pr["parent"] == f["id"]:
                    pprops = pr["props"]
                    params.append({
                        "name": pr["name"],
                        "type": friendly_type(pr["raw"].get("TranslationType")),
                        "db_type": dbtype_name(pprops.get("DbType") if pprops.get("DbType") is not None else pprops.get("Type")),
                        "required": pprops.get("Required"),
                        "props": pprops,
                    })
            ftype = f["type"]
            shape_hint = None
            if ftype == "WebServiceFunction":
                shape_hint = _resolve_ws_hint(f["id"], fprops)
            elif ftype == "StoredProcedure":
                shape_hint = _resolve_sp_hint(fprops, params)
            conn["functions"].append({
                "name": f["name"],
                "type": f["type"],
                "query": fprops.get("Text") or fprops.get("Query") or fprops.get("CommandText"),
                "timeout": fprops.get("Timeout"),
                "parameters": params,
                "shape_hint": shape_hint,
                "other_props": {k: v for k, v in fprops.items() if k not in ("Text", "Query", "CommandText", "Timeout")},
            })
        connectors.append(conn)
    model["connectors"] = connectors

    # ----- Scripts (event handlers) and their action sequence
    def _ref_name(v):
        """Resolve a GuidReference / Expression / scalar to a readable string where possible."""
        if isinstance(v, dict):
            nid = v.get("NamedItemID")
            if nid:
                g = norm_guid(nid)
                if g in registry and registry[g].get("name"):
                    return registry[g]["name"]
                return str(nid)
            if v.get("FormatString") is not None:
                names = []
                for pv in (v.get("PlaceholderValues") or []):
                    if isinstance(pv, dict) and pv.get("NamedItemID"):
                        g = norm_guid(pv.get("NamedItemID"))
                        if g in registry and registry[g].get("name"):
                            names.append(registry[g]["name"])
                if names:
                    return " / ".join(names)
                return str(v.get("FormatString"))
            return None
        if isinstance(v, (str, int, float, bool)):
            s = str(v).strip()
            return s or None
        return None

    def summarise_action(props):
        """Pull the readable, resolved fields out of an action's prop bag (names + message text)."""
        s = {}
        for k, v in (props or {}).items():
            nm = _ref_name(v)
            if nm and not re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", str(nm)):
                s[k] = nm[:300]
        return s

    # ----- 1a/1b: branch-structured action tree via the ExecutionPath reference-walk.
    # The flat `actions` list built by collect_actions (below) is a DFS over the ScriptItem tree —
    # it is APPROXIMATELY right for linear scripts but SCRAMBLES branches (a validation-fail
    # notification prints after the happy-path navigate) and captures NO guard conditions. This adds
    # a parallel `tree` that preserves execution order, branch structure, and predicates. The flat
    # `actions` is kept UNTOUCHED (nav-edge + affordance readers depend on it — Phase-1 back-compat).
    #
    # Shape (proven against golden fixtures, framework/tools/__fixtures__/):
    #   A Script has one child of type ...Scripts.ExecutionPath whose props["Actions"] is the ordered
    #   GUID list of its root actions. A Decision.Decision action carries props["ExecutionPaths"] ->
    #   IfPath nodes (props: Conditions + Actions) plus, when ShowElse, a trailing ExecutionPath node
    #   (the else branch: Actions, no Conditions). A Conditions GUID -> a ...Decision.Condition expando
    #   {Value1, Operator, Value2, Join}. Every GUID is normalised before lookup (norm_guid handles
    #   the string-vs-blob mix). JavaScript actions are opaque (branch resolution cannot see inside).
    TREE_DEPTH_CAP = 12

    def _exec_path_child(parent_id):
        """The root ExecutionPath node directly under a Script."""
        for cid in children.get(norm_guid(parent_id), []):
            e = registry.get(cid)
            tt = ((e or {}).get("translation_type") or "").split(",")[0].strip()
            if e and tt.endswith("ExecutionPath"):
                return e
        return None

    def _render_condition(cond_id):
        """Resolve a Condition expando GUID -> {value1, op, value2, join, text}. 1b."""
        e = registry.get(norm_guid(cond_id))
        if not e:
            return None
        p = e.get("props") or {}
        v1 = _ref_name(p.get("Value1"))
        v2 = _ref_name(p.get("Value2"))
        sym = op_symbol(p.get("Operator"))
        return {"value1": v1, "op": sym, "op_raw": p.get("Operator"),
                "value2": v2, "join": join_word(p.get("Join")), "join_raw": p.get("Join"),
                "text": f"{v1 if v1 is not None else '?'} {sym} {v2 if v2 is not None else '?'}"}

    def _predicate_text(cond_ids):
        """Join an IfPath's conditions into one predicate, using each condition's own Join word
        (the first condition's Join is the leading, unused, connector)."""
        conds = [c for c in (_render_condition(cid) for cid in (cond_ids or [])) if c]
        if not conds:
            return None
        out = conds[0]["text"]
        for c in conds[1:]:
            out += f" {c['join']} {c['text']}"
        return out

    def _walk_action(aid, depth, seen):
        aid = norm_guid(aid)
        e = registry.get(aid)
        if not e:
            return {"action": "?", "missing": True}
        if aid in seen or depth > TREE_DEPTH_CAP:
            return {"action": e.get("type"), "name": e.get("name"), "truncated": True}
        seen.add(aid)
        aprops = {k: v for k, v in (e.get("props") or {}).items() if not str(k).startswith("$")}
        node = {"action": e.get("type"), "name": e.get("name"), "summary": summarise_action(aprops)}
        if e.get("type") == "JavaScript":
            node["opaque"] = True
        if e.get("type") == "Decision":
            node["decision"] = True
            node["show_else"] = bool(aprops.get("ShowElse"))
            branches = []
            for ep_id in (aprops.get("ExecutionPaths") or []):
                ep = registry.get(norm_guid(ep_id))
                if not ep:
                    continue
                epp = ep.get("props") or {}
                is_if = ((ep.get("translation_type") or "").split(",")[0].strip().endswith("IfPath"))
                branches.append({
                    "kind": "if" if is_if else "else",
                    "predicate": _predicate_text(epp.get("Conditions")) if is_if else None,
                    "steps": [_walk_action(a, depth + 1, seen) for a in (epp.get("Actions") or [])],
                })
            node["branches"] = branches
        return node

    def build_action_tree(script_id):
        ep = _exec_path_child(script_id)
        if not ep:
            return []
        seen = set()
        return [_walk_action(a, 0, seen) for a in ((ep.get("props") or {}).get("Actions") or [])]

    scripts = []
    for e in scripts_e:
        sid = e["id"]
        owner, owner_kind = owner_page(e["parent"]) if e["parent"] else (None, None)
        actions = []
        # action ScriptItems are descendants of the script
        def collect_actions(pid):
            for cid in children.get(pid, []):
                ce = registry.get(cid)
                if not ce:
                    continue
                if ce["kind"] == "scriptitem" and ce["translation_type"] and ".Actions." in ce["translation_type"]:
                    aprops = {k: v for k, v in ce["props"].items() if not str(k).startswith("$")}
                    actions.append({"action": ce["type"], "name": ce["name"],
                                    "summary": summarise_action(aprops),
                                    "props": aprops})
                collect_actions(cid)
        collect_actions(sid)
        scripts.append({
            "name": e["name"],
            "is_event_handler": bool(e["raw"].get("IsEventHandlerScript")),
            "owner": owner, "owner_kind": owner_kind,
            "actions": actions,
            "tree": build_action_tree(sid),   # 1a: branch-structured, condition-bearing (additive)
        })
    model["scripts"] = scripts

    # ----- Session variables, custom types, validators
    model["session_variables"] = [{"name": e["name"], "props": e["props"]} for e in sessvars_e]
    model["custom_types"] = [{"name": e["name"], "props": e["props"]} for e in customtypes_e]
    # `summary` resolves any GuidReference / message props via the registry (reused by the 0f
    # validator render in emit_assets, which has no registry access). Additive; `props` retained.
    model["validators"] = [{"name": e["name"], "type": e["type"], "props": e["props"],
                            "summary": summarise_action(e["props"])} for e in validators_e]

    # ----- Styling
    stylerules = []
    if "StyleRule" in tn:
        for r in rows(cur, "StyleRule"):
            css = (r.get("CSS") or "").strip()
            if css:
                stylerules.append({"key": r.get("Key"), "pseudo": r.get("PseudoSelector"), "css": css})
    model["styling"] = {
        "theme": app.get("theme"),
        "app_stylesheet_enabled": app.get("stylesheet_enabled"),
        "app_stylesheet": app.get("stylesheet"),
        "head_html": app.get("head_html"),
        "non_empty_style_rules": stylerules,
        "style_rule_count_total": len(rows(cur, "StyleRule")) if "StyleRule" in tn else 0,
    }

    # ----- Embedded file inventory (names only; content read separately by agents)
    model["embedded_file_items"] = [
        {"name": e.get("Name"), "is_folder": bool(e.get("IsFolder")), "last_modified": e.get("LastModifiedDate")}
        for e in rows(cur, "EmbeddedFileItem")
    ] if "EmbeddedFileItem" in tn else []

    # ----- Data dictionary: StructDataType -> fields -> primitive type (+ IsDataField).
    # This clean central data model is mangled in the deployed source; IsDataField lives only here.
    data_dictionary = []
    if "Field" in tn and "StructDataType" in tn:
        field_type = {}   # field guid -> friendly primitive type (from its SimpleDataType child)
        if "SimpleDataType" in tn:
            for r in rows(cur, "SimpleDataType"):
                fid = norm_guid(r.get("ParentID"))
                if fid:
                    field_type[fid] = friendly_type(r.get("TypeName"))
        structs = {}      # struct guid -> [field dicts]
        for r in rows(cur, "Field"):
            sid = norm_guid(r.get("ParentID"))
            fid = norm_guid(r.get("ID"))
            structs.setdefault(sid, []).append({
                "name": r.get("Name"),
                "type": field_type.get(fid),
                "is_data_field": bool(r.get("IsDataField")),
            })
        for sid, flds in structs.items():
            data_dictionary.append({"struct_id": sid, "field_count": len(flds), "fields": flds})
    model["data_dictionary"] = data_dictionary

    # ----- App settings (.sapz `Setting` table) — Cluster B #4-B. Rows are classified + redacted
    # AT READ TIME (see `_redact_setting`); no secret value reaches model.json. Absent table -> [].
    settings = []
    if "Setting" in tn:
        for r in rows(cur, "Setting"):
            nm = r.get("Name")
            if not nm:
                continue
            kind, val = _redact_setting(nm, r.get("Value"))
            settings.append({"name": nm, "kind": kind, "value": val,
                             "is_secret_flag": bool(r.get("IsSecret"))})
    model["settings"] = settings

    con.close()
    return model

# --------------------------------------------------------------------------- admin db (security)

def read_admin_db(app_dir):
    out = {"roles": [], "page_access": {}, "pages": [], "pagerole_count": 0, "user_count": 0, "admin_count": 0, "connections": [], "deploy_history": [], "audit_log": []}
    admin = os.path.join(app_dir, "administration.db")
    if not os.path.exists(admin):
        return out
    try:
        c = sqlite3.connect(admin); c.row_factory = sqlite3.Row
        # Full Pages table (0b view/task inventory) — IsStartPage added; the WHOLE list is kept
        # (not just PageRole-joined pages), so admin-only surfaces surface too. Defensive: fall
        # back to the old shape if IsStartPage is absent.
        pages, pages_full = {}, []
        try:
            for r in c.execute("SELECT Id,Name,IsStartPage FROM Pages"):
                pages[str(r["Id"])] = r["Name"]
                pages_full.append({"name": r["Name"], "is_start_page": bool(r["IsStartPage"])})
        except Exception:
            for r in c.execute("SELECT Id,Name FROM Pages"):
                pages[str(r["Id"])] = r["Name"]
                pages_full.append({"name": r["Name"], "is_start_page": False})
        out["pages"] = pages_full
        roles = {str(r["Id"]): r["Name"] for r in c.execute("SELECT Id,Name FROM Roles")}
        out["roles"] = sorted(roles.values())
        pr_count = 0
        for r in c.execute("SELECT PageId,RoleId FROM PageRole"):
            pr_count += 1
            pg = pages.get(str(r["PageId"]), str(r["PageId"]))
            out["page_access"].setdefault(pg, []).append(roles.get(str(r["RoleId"]), str(r["RoleId"])))
        out["pagerole_count"] = pr_count  # 0d branch predicate: len(roles) > 1 or pagerole_count > 1
        # Actual user identities (UserName / Name / Email) are intentionally NOT extracted —
        # they are PII and are not needed for requirements. Only aggregate counts are kept;
        # roles + page-level permissions (above) are the actor model the requirements need.
        urows = list(c.execute("SELECT IsAdministrator FROM Users"))
        out["user_count"] = len(urows)
        out["admin_count"] = sum(1 for r in urows if r["IsAdministrator"])
        try:
            arow = c.execute("SELECT Name,FileGuid FROM Applications LIMIT 1").fetchone()
            if arow:
                out["app_name"] = arow["Name"]
                out["file_guid"] = str(arow["FileGuid"])
        except Exception:
            pass
        for r in c.execute("SELECT Name,ConnectionString FROM Connections"):
            out["connections"].append({"name": r["Name"], "connection_string": sanitize_conn(r["ConnectionString"])})
        # Publisher username is a real identity (PII) — not extracted; keep only version + date.
        for r in c.execute("SELECT DesignerVersion,DateTime FROM ApplicationUpdates ORDER BY DateTime"):
            out["deploy_history"].append({"designer_version": r["DesignerVersion"], "datetime": r["DateTime"]})
        try:
            # AuditLogs.ChangedBy / Source can carry user identifiers — keep only the
            # non-identifying shape (when something changed, and of what kind).
            for r in c.execute("SELECT ChangedOn,Type,Action FROM AuditLogs ORDER BY ChangedOn"):
                out["audit_log"].append({"changed_on": r["ChangedOn"], "type": r["Type"], "action": r["Action"]})
        except Exception:
            pass
        c.close()
    except Exception as e:
        out["_error"] = str(e)
    return out

# --------------------------------------------------------------------------- config / stack / front-end assets

def read_config(app_dir):
    cfg = {}
    p = os.path.join(app_dir, "appsettings.json")
    if os.path.exists(p):
        try:
            cfg = json.load(open(p, encoding="utf-8-sig")).get("Config", {})
            if isinstance(cfg.get("OAuth"), dict):
                cfg["OAuth"] = {k: ("<set>" if v else None) for k, v in cfg["OAuth"].items()}
        except Exception as e:
            cfg = {"_error": str(e)}
    return cfg

def read_stack(app_dir):
    stack = {"backend": None, "frontend_deps": {}, "frontend_devdeps": {}, "csproj_packages": []}
    pj = os.path.join(app_dir, "ClientApp", "package.json")
    if os.path.exists(pj):
        try:
            d = json.load(open(pj, encoding="utf-8"))
            stack["frontend_deps"] = d.get("dependencies", {})
            stack["frontend_devdeps"] = d.get("devDependencies", {})
        except Exception:
            pass
    csproj = glob.glob(os.path.join(app_dir, "*.csproj"))
    if csproj:
        try:
            txt = open(csproj[0], encoding="utf-8").read()
            tf = re.search(r"<TargetFramework>([^<]+)</TargetFramework>", txt)
            stack["backend"] = tf.group(1) if tf else None
            stack["csproj_packages"] = re.findall(r'<PackageReference Include="([^"]+)" Version="([^"]+)"', txt)
        except Exception:
            pass
    return stack

def read_frontend_assets(app_dir):
    """Locate styling assets the design-system agent will read in full."""
    base = os.path.join(app_dir, "ClientApp", "src", "assets")
    info = {"themes_dir": None, "available_themes": [], "current_theme": None,
            "fonts": [], "css_files": [], "embedded_files": []}
    themes = os.path.join(base, "themes")
    if os.path.isdir(themes):
        info["themes_dir"] = themes
        info["available_themes"] = sorted([d for d in os.listdir(themes) if os.path.isdir(os.path.join(themes, d))])
        for f in os.listdir(themes):
            if f.endswith(".scss"):
                info["css_files"].append(os.path.join(themes, f))
    fonts = os.path.join(base, "fonts")
    if os.path.isdir(fonts):
        names = set()
        for root, _, files in os.walk(fonts):
            for f in files:
                names.add(re.sub(r"\.(woff2?|ttf|eot|svg)$", "", f, flags=re.I))
        info["fonts"] = sorted(names)
    for f in ("application-custom.scss", "stadium-layout.css", "bootstrap-substitute.css", "fontawesome-all.css"):
        fp = os.path.join(base, f)
        if os.path.exists(fp):
            info["css_files"].append(fp)
    ef = os.path.join(app_dir, "wwwroot", "Content", "EmbeddedFiles")
    if os.path.isdir(ef):
        for root, _, files in os.walk(ef):
            for f in files:
                info["embedded_files"].append(os.path.join(root, f))
    return info

# --------------------------------------------------------------------------- gap detection

def detect_gaps(model, admin, cfg, assets):
    gaps = []
    if not any((p.get("control_tree") for p in model.get("pages", []))):
        gaps.append("One or more pages have no controls in the design model (possible stub or layout-only page).")
    for c in model.get("connectors", []):
        if c.get("type") and "FileSystem" in str(c.get("type", "")) + str(c.get("connection_string", "")):
            gaps.append(f"Connector '{c['name']}' references an external filesystem path; the actual files/content are not in the repo.")
        for f in c.get("functions", []):
            if f.get("query"):
                gaps.append(f"Data schema for connector '{c['name']}' is implied by SQL in '{f['name']}' but the live database schema/constraints are external.")
                break
    # Cluster A #3 — real validation lives in control props, not the (corpus-wide empty) `Validator`
    # table. Only flag the gap when NO validation signal of any kind exists — a bare `not validators`
    # test fired the false blocking gap on every app despite 4–72 validated controls.
    def _has_control_validation():
        for c in model.get("all_controls", []) or []:
            kp = c.get("key_props") or {}
            err = kp.get("ErrorText")
            if kp.get("Required") or kp.get("IsValidRule") or (isinstance(err, str) and err.strip()):
                return True
        return False
    if not model.get("validators") and not _has_control_validation():
        gaps.append("Validation not modelled in the design model (no validators, required-field flags, or control validation rules).")
    if cfg.get("AuthenticationType") == "OAuth":
        gaps.append("OAuth is configured but secrets are redacted; identity-provider details must be supplied.")
    gaps.append("Business intent, target users, and success criteria are not present in source and must come from a stakeholder.")
    gaps.append("Non-functional requirements (performance, scale, availability, accessibility, browser support, compliance) are not in source.")
    gaps.append("Acceptance criteria / test cases are not present in source.")
    # dedupe, keep order
    seen, out = set(), []
    for g in gaps:
        if g not in seen:
            seen.add(g); out.append(g)
    return out

# --------------------------------------------------------------------------- markdown digest

def write_inventory_md(model, admin, cfg, stack, assets, deploy_meta, path):
    app = model.get("application", {})
    L = []
    L.append(f"# Stadium App Inventory — {app.get('name') or cfg.get('WebAppName') or 'Unknown'}\n")
    L.append(f"- **Web App ID:** `{cfg.get('WebAppId', '?')}`")
    L.append(f"- **Designer version:** {app.get('designer_version', '?')}")
    L.append(f"- **Theme:** {app.get('theme', '?')}")
    L.append(f"- **Authentication:** {cfg.get('AuthenticationType', '?')}  |  Session timeout: {cfg.get('SessionStateTimeout', '?')} min")
    L.append(f"- **Backend:** {stack.get('backend')}  |  **Frontend:** Vue (see deps)")
    L.append(f"- **Design model package:** {deploy_meta.get('selected_package')} (of {deploy_meta.get('package_count')} deployments)\n")

    L.append("## Pages")
    for p in model.get("pages", []):
        star = " ⭐ start" if p.get("is_start_page") else ""
        def count(nodes):
            n = len(nodes)
            for x in nodes:
                n += count(x.get("children", []))
            return n
        L.append(f"- **{p['name']}** (title: {p.get('title')}){star} — {count(p.get('control_tree', []))} controls")
    L.append("")

    L.append("## Controls (by page)")
    def render(nodes, depth=1):
        for n in nodes:
            txt = n.get("key_props", {}).get("Text") or n.get("key_props", {}).get("Label") or ""
            txt = f" — \"{txt}\"" if isinstance(txt, str) and txt else ""
            L.append("  " * depth + f"- {n['type']}: `{n['name']}`{txt}")
            render(n.get("children", []), depth + 1)
    for p in model.get("pages", []):
        L.append(f"\n### {p['name']}")
        render(p.get("control_tree", []))
    for t in model.get("templates", []):
        L.append(f"\n### Template: {t['name']}{' (default)' if t.get('is_default') else ''}")
        render(t.get("control_tree", []))
    L.append("")

    L.append("## Connectors & data operations")
    for c in model.get("connectors", []):
        L.append(f"\n### {c['name']} ({c.get('type')})")
        L.append(f"- Connection: `{c.get('connection_string')}`")
        for f in c.get("functions", []):
            L.append(f"- **{f['name']}** ({f.get('type')})")
            if f.get("parameters"):
                L.append("  - params: " + ", ".join(f"{p['name']}:{p.get('db_type') or p.get('type')}" for p in f["parameters"]))
            if f.get("query"):
                q = " ".join(str(f["query"]).split())
                L.append(f"  - query: `{q[:240]}`")
    L.append("")

    L.append("## Event logic (scripts → action sequences)")
    for s in model.get("scripts", []):
        if not s.get("actions"):
            continue
        L.append(f"- **{s['name']}** ({s.get('owner') or 'app'}): " + " → ".join(a["action"] for a in s["actions"]))
    L.append("")

    L.append("## Security")
    L.append(f"- Roles: {', '.join(admin.get('roles', [])) or '—'}")
    for pg, rs in admin.get("page_access", {}).items():
        L.append(f"- `{pg}` → {', '.join(sorted(set(rs)))}")
    L.append(f"- Users: {admin.get('user_count', 0)} (admins: {admin.get('admin_count', 0)})")
    L.append("")

    L.append("## Styling sources (read in full for the design system)")
    L.append(f"- Theme: **{model['styling'].get('theme')}**  |  app stylesheet enabled: {model['styling'].get('app_stylesheet_enabled')}")
    L.append(f"- Non-empty per-control style rules: {len(model['styling'].get('non_empty_style_rules', []))} (of {model['styling'].get('style_rule_count_total')})")
    L.append(f"- Available theme files: {', '.join(assets.get('available_themes', [])) or '—'}")
    L.append(f"- Fonts present: {', '.join(assets.get('fonts', [])) or '—'}")
    L.append(f"- App-level custom stylesheet: {'present' if model['styling'].get('app_stylesheet') else 'none'}")
    L.append(f"- Embedded widget files: {len(assets.get('embedded_files', []))}")
    L.append("")

    L.append("## Detected gaps (not ascertainable from source)")
    for g in model.get("gaps", []):
        L.append(f"- {g}")
    L.append("")

    open(path, "w", encoding="utf-8").write("\n".join(L))

# --------------------------------------------------------------------------- modules / custom JS

# --- Cluster B #5: complementary module-detection maps. The comment-URL scan stays the PRIMARY,
# strongest signal (probe: 53 URL hits vs 42 function hits, 62% overlap); function-name inventory
# + CSS footprint add recovery for URL-stripped / CSS-only modules and are tagged distinctly. The
# authoritative maps live here in code; `module-catalogue.md` mirrors them for maintainers. This is
# a curated POSITIVE whitelist (we only look for known module functions) — so there is no inventory
# step and no false-positive class. Every emitted slug is a real `module-catalogue.md` slug.
FN_MODULE_MAP = {
    "EditableRow": "datagrid-inline-row-edit",
    "ConditionalColumnsStyling": "conditional-datagrid-styling",
    "DataGridFilter": "datagrid-advanced-search",
    "GenerateFilters": "datagrid-advanced-search",
    "ConstructSearchPhrase": "filter-grid",
    "ParseColumnHeading": "dynamic-datagrid",
    "CollapseControl": "collapse-controls",
    "FixHeaders": "full-width-top-bar",
    "WorkflowSteps": "workflow-steps",
    "Spinner": "page-loader",
    "DismissOnClick": "popups",
    "DismissOnEscape": "popups",
    "Popup": "popups",
    "Icons": "icons",
    "Accordion": "accordion",
    "EnvironmentIdentifier": "environment-identifier",
    "ClearUploadFileControl": "utils-clear-upload-file-control",
}
# Framework / validation helper names that appear in nearly every app. The positive whitelist
# above already excludes everything not in it, so these never emit — kept documented so a future
# inventory-based approach can't silently promote a generic helper to a module.
FN_EXCLUDE = frozenset({
    "app", "AddCheckBoxComponentValidation", "AddDropDownComponentValidation",
    "AddTextBoxComponentValidation", "AreInputsValid", "AreValidationsReset", "Callback",
    "CallbackScript", "CheckMultipleComponentsValidation", "ClassName", "CollapseOnClickAway",
    "ColumnHeading", "ColumnTextValues", "Conditions", "DataGridClass", "EventCallback",
    "EventHandler", "FormFields", "globalScripts", "Headings", "install", "options",
    "provide", "ContainerClass",
})
# CSS filename stem (case-insensitive prefix) -> slug, for CSS-only / URL-stripped modules.
# Ambiguous stems (`utils.css`) and pure-theming stems (`theming-variables.css` -> design-signals)
# are deliberately omitted (see module-catalogue.md note on CSS-only theming modules).
CSS_MODULE_MAP = {
    "tabs": "tabs",
    "workflow-steps": "workflow-steps",
    "datagrid-inline-edit": "datagrid-inline-row-edit",
    "datagrid-custom-filters": "datagrid-advanced-search",
    "stadium-repeater-datagrid": "repeater-datagrid-client-side",
    "page-loader": "page-loader",
    "top-bar": "full-width-top-bar",
    "collapsible-control": "collapse-controls",
    "modal": "popups",
    "popup": "popups",
    "accordion": "accordion",
    "environments": "environment-identifier",
    "icons": "icons",
    "progress-bar": "progress-bar",
    "button-bar": "button-bar",
}
# Function -> presence-only behaviour signal (the runtime step list / role->page map are function
# ARGUMENTS — out of scope here; they belong to the behaviour axis). `RoleSpecificStartPages` is a
# pattern, not a catalogued github module, so it is surfaced only as a behaviour, never as a module.
BEHAVIOUR_FNS = {
    "WorkflowSteps": "multi-step (stepper) workflow — a required multi-step interaction",
    "RoleSpecificStartPages": "role-specific start pages — role → landing-page navigation policy",
    "RolePages": "role-specific start pages — role → landing-page navigation policy",
}

def _fn_present(txt, name):
    """True when a module function is DEFINED or CALLED in global-scripts.js text — anchored to
    definition / object-property / call-site contexts, so debug-log noise (which mentions names in
    strings) cannot false-positive. No strip pre-pass needed (probe-confirmed: names survive)."""
    n = re.escape(name)
    return re.search(rf"(?:function\s+{n}\b|\b{n}\s*[:=]|\.{n}\s*\()", txt) is not None

def read_modules(app_dir, kb_dir=None):
    """Detect stadium-software modules from the generated source. Comment-URL is the PRIMARY signal;
    function-name inventory + CSS footprint (Cluster B #5) are complementary, each tagged with its
    `detection_source`. Presence-only module-driven behaviours are surfaced separately."""
    out = {"global_scripts_present": False, "embedded_css": [], "detected": [], "behaviours": []}
    gs = os.path.join(app_dir, "ClientApp", "src", "global-scripts.js")
    url_slugs, fn_slugs, behaviours = set(), set(), []
    txt = ""
    if os.path.exists(gs):
        out["global_scripts_present"] = True
        try:
            txt = open(gs, encoding="utf-8", errors="ignore").read()
        except Exception:
            txt = ""
        for u in re.findall(r"github\.com/stadium-software/([A-Za-z0-9._-]+)", txt):
            url_slugs.add(u.strip().rstrip("/.").lower())
        for fn, slug in FN_MODULE_MAP.items():             # positive whitelist; FN_EXCLUDE is a no-op guard
            if fn not in FN_EXCLUDE and _fn_present(txt, fn):
                fn_slugs.add(slug)
        for fn, behaviour in BEHAVIOUR_FNS.items():
            if _fn_present(txt, fn) and behaviour not in behaviours:
                behaviours.append(behaviour)
    ef = os.path.join(app_dir, "wwwroot", "Content", "EmbeddedFiles", "CSS")
    if os.path.isdir(ef):
        out["embedded_css"] = sorted(f for f in os.listdir(ef) if f.lower().endswith(".css"))
    css_slugs = set()
    for f in out["embedded_css"]:
        stem = f.lower()
        for pref, slug in CSS_MODULE_MAP.items():
            if stem.startswith(pref):
                css_slugs.add(slug)
                break
    gloss = {}
    if kb_dir:
        kbf = os.path.join(kb_dir, "module-catalogue.md")
        if os.path.exists(kbf):
            try:
                for line in open(kbf, encoding="utf-8"):
                    mm = re.match(r"\s*\|\s*`?([A-Za-z0-9._-]+)`?\s*\|\s*(.+?)\s*\|", line)
                    if mm and mm.group(1).strip().lower() not in ("module", "name", "---", ":---"):
                        gloss[mm.group(1).strip().lower()] = mm.group(2).strip()
            except Exception:
                pass
    # union: comment-URL wins, then function-name, then CSS footprint
    sources = {}
    for slug in sorted(url_slugs):
        sources[slug] = "url"
    for slug in sorted(fn_slugs):
        sources.setdefault(slug, "fn")
    for slug in sorted(css_slugs):
        sources.setdefault(slug, "css")
    for slug in sorted(sources):
        out["detected"].append({"module": slug, "repo": f"https://github.com/stadium-software/{slug}",
                                 "gloss": gloss.get(slug), "detection_source": sources[slug]})
    out["behaviours"] = behaviours
    return out

# --------------------------------------------------------------------------- rendered ClientApp/src readers (Cluster C)
# The rendered `ClientApp/src` is GENERATED from the `.sapz`, so every fact mined here is a COMPLEMENT to
# the design model, never a replacement: it is stamped with a `[from rendered ...]` locator and reconciled
# against the `.sapz`, which wins on type conflict. Parsing is regex + bracket-balancing over BOUNDED
# declarative regions (the route array, class bodies, the `columnDefinitions` array) — deliberately NO JS
# AST (Python ships none; a new dep is rejected). This matches the read_modules regex-over-JS precedent:
# the declarative blocks parse clean, so no debug-log strip pre-pass is needed. Every reader clones
# read_frontend_assets/read_modules — path off app_dir, graceful absence — so pure-SQL apps and
# bare-`.sapz` inputs no-op (return an empty result), never raising.

def _read_client_src(app_dir, *relpath):
    """Safe read of a ClientApp/src/** file. Strips a UTF-8 BOM (some routers carry one — CosmoCrm).
    Returns "" when the file is absent (→ SQL apps and bare-`.sapz` inputs no-op, exactly like read_modules)."""
    p = os.path.join(app_dir, "ClientApp", "src", *relpath)
    if not os.path.isfile(p):
        return ""
    try:
        return open(p, encoding="utf-8-sig", errors="ignore").read()
    except Exception:
        return ""

def _balanced_block(text, start_idx, open_ch="[", close_ch="]"):
    """Substring of the first `open_ch..close_ch`-balanced region starting at text[start_idx] (which must
    be `open_ch`). Skips over quoted strings ('...', "...", `...`) so a bracket/brace inside a label can
    never unbalance the scan. Bounds a 1.3 MB view's `columnDefinitions` array / a class body / the route
    array WITHOUT structuring the whole file. Returns the tail from start_idx if unbalanced (truncated)."""
    depth, i, n, quote = 0, start_idx, len(text), None
    while i < n:
        c = text[i]
        if quote:
            if c == "\\":
                i += 2; continue
            if c == quote:
                quote = None
        elif c in "'\"`":
            quote = c
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return text[start_idx:i + 1]
        i += 1
    return text[start_idx:]

def _split_object_literals(block):
    """Given a `[ {…}, {…} ]` block substring, return the top-level `{…}` object substrings (brace-
    balanced, string-aware, ignoring nested braces such as a route's `meta: {…}`). Bounds each column /
    route object for field extraction."""
    objs, depth, s, i, n, quote = [], 0, None, 0, len(block), None
    while i < n:
        c = block[i]
        if quote:
            if c == "\\":
                i += 2; continue
            if c == quote:
                quote = None
        elif c in "'\"`":
            quote = c
        elif c == "{":
            if depth == 0:
                s = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0 and s is not None:
                objs.append(block[s:i + 1]); s = None
        i += 1
    return objs

def read_page_routes(app_dir):
    """Cluster C #7 — parse ClientApp/src/router/page-routes.js into the COMPLETE titled page list. This
    is the definitive page enumeration; the `.sapz` NavigateToPage walk is only a floor (JS-computed nav
    is opaque). Grammar (probed uniform across all 20 corpus apps):

        const pageRoutes = [
          { path: '/', redirect: '/Members' },                                 // redirect → SKIP (no component)
          { path: '/Members', component: Members, meta: { title: 'Members' } },
          ...
        ];

    Parse `page-routes.js` ONLY — router/ also holds routes.js + index.js (framework admin/auth/error
    routes), which are NOT the app payload. Returns [{path, title, component}]; [] when the file is absent."""
    txt = _read_client_src(app_dir, "router", "page-routes.js")
    if not txt:
        return []
    m = re.search(r"(?:const|let|var)\s+pageRoutes\s*=\s*\[", txt)
    if not m:
        return []
    routes = []
    for obj in _split_object_literals(_balanced_block(txt, m.end() - 1, "[", "]")):
        comp = re.search(r"\bcomponent\s*:\s*([A-Za-z_$][\w$]*)", obj)
        if not comp:                                   # redirect-only entry (no component) → skip
            continue
        path = re.search(r"\bpath\s*:\s*['\"]([^'\"]*)['\"]", obj)
        title = re.search(r"\btitle\s*:\s*['\"]([^'\"]*)['\"]", obj)
        routes.append({"path": path.group(1) if path else None,
                       "title": title.group(1) if title else None,
                       "component": comp.group(1)})
    return routes

def _route_page_name(r):
    """Page name for a page-routes.js entry: the component identifier (matches the `.sapz` page name and
    the `.vue` filename), falling back to the last path segment."""
    return r.get("component") or ((r.get("path") or "").strip("/").split("/")[-1] or None)

# Cluster C #6 — rendered types.js grammar. A DOMAIN entity class is `<API>_Types_<Entity><Variant>`; the
# `<API>_` prefix is REQUIRED (bare `Types_*` classes — Types_Filter/Types_Column/Types_WorkflowStep/
# Types_ConditionalColumn — are stadium-module framework scaffolding, never FE↔API domain data, and are
# skipped by the `_Types_`-must-be-present rule). Transport/validation envelopes are denied (never §7
# entities). Fields are `<Name> = undefined;` with NO type and NO nullability (required-ness comes from
# Cluster A #1's `.sapz` control props, not here). Relationships come from a class's `_getFieldTypeName`
# map → a `_..._Type extends Array` wrapper → its `_getItemTypeName()` element type.

# Entity+variant names whose CLASS is a transport/response envelope, not a domain entity (normalized, no `_Types_`).
_RENDERED_ENVELOPE = {"defaultresponse", "generalresponse", "generalerror", "generalresponseid",
                      "responseid", "responsemessage", "validationresult"}

# Trailing variant tokens stripped to reach the entity STEM, with the field-authority each implies.
# `Basic` binds to its Read (CustomerBasicRead → Customer); `Status` does NOT strip (CustomerStatusRead →
# CustomerStatus, a distinct sub-resource) — the probe requires Customer and CustomerStatus stay distinct.
# Matched longest-first (sorted at use). `*List` tokens mark a list-collection wrapper → the class is
# excluded entirely (its only field is a self-collection already implied by the item entity).
_TYPE_VARIANTS = [
    ("BasicRead", "display"), ("AddUpdate", "editable"), ("WriteList", "editable"), ("ReadList", "display"),
    ("Read", "display"), ("Write", "editable"), ("Update", "editable"), ("Post", "editable"),
    ("Put", "editable"), ("Add", "editable"),
    ("Convert", "action"), ("Complete", "action"), ("Cancel", "action"), ("Close", "action"),
    ("List", "display"),
]

def _rendered_entity_stem(ev):
    """Split a rendered `<Entity><Variant>` name (the part after `<API>_Types_`) into (stem, authority).
    Strips the longest trailing variant token. Returns (None, None) when the class is excluded from §7
    entities: a transport/response envelope, a `*Validation` result DTO, or a `*List` collection wrapper
    (self-collection adds nothing the item entity lacks)."""
    low = ev.lower()
    if low in _RENDERED_ENVELOPE or low.endswith("validation"):
        return None, None
    for tok, authority in sorted(_TYPE_VARIANTS, key=lambda t: -len(t[0])):
        if ev.endswith(tok) and len(ev) > len(tok):
            if tok.endswith("List"):                     # list-collection wrapper → excluded
                return None, None
            return ev[:-len(tok)], authority
    return ev, "display"                                 # no recognized variant → bare shape, read-authority default

def read_client_types(app_dir):
    """Cluster C #6 — parse ClientApp/src/types/types.js into FE↔API contract entities. For the ~15/20
    web-service-backed apps this is the ONLY good typing source (the `.sapz` type reconciliation collapses
    — CosmoCrm types 4/247 fields). Empty (1 blank line) for the 5/20 pure-SQL apps → returns []. Returns
    [{api, entity, variant, authority, norm, fields:[{name, authority}], relations:{field: element_entity}}];
    Array wrappers, envelopes, `*Validation` DTOs, `*List` collection wrappers and bare `Types_*`
    scaffolding are all excluded."""
    txt = _read_client_src(app_dir, "types", "types.js")
    if not txt:
        return []
    classes = []                                          # (name, base, body)
    for m in re.finditer(r"export\s+class\s+([A-Za-z0-9_$]+)\s*(?:extends\s+([A-Za-z0-9_.$]+)\s*)?\{", txt):
        classes.append((m.group(1), m.group(2), _balanced_block(txt, m.end() - 1, "{", "}")))
    # 1) `_..._Type extends Array` wrappers → {wrapper_name: element_type_name}
    wrapper_elem = {}
    for name, base, body in classes:
        if base and base.split(".")[-1] == "Array":
            em = re.search(r"_getItemTypeName\s*\([^)]*\)\s*\{[^{}]*return\s+'([^']+)'", body)
            wrapper_elem[name] = em.group(1) if em else None
    # 2) field-bearing domain classes (require the `<API>_Types_` prefix; not `extends Array`)
    out = []
    for name, base, body in classes:
        if (base and base.split(".")[-1] == "Array") or "_Types_" not in name:
            continue
        api, ev = name.split("_Types_", 1)
        if not api or not ev:
            continue
        stem, authority = _rendered_entity_stem(ev)
        if stem is None:
            continue
        fields = [{"name": fm.group(1), "authority": authority}
                  for fm in re.finditer(r"(?m)^\s*([A-Za-z_$][\w$]*)\s*=\s*undefined\s*;", body)]
        relations = {}                                    # field → element entity (nested-type map)
        for cm in re.finditer(r"([A-Za-z_$][\w$]*)\s*:\s*'(_[A-Za-z0-9_$]+)'", body):
            elem = wrapper_elem.get(cm.group(2))
            if not elem or "_Types_" not in elem:
                continue
            estem, _ = _rendered_entity_stem(elem.split("_Types_", 1)[1])
            relations[cm.group(1)] = estem or elem.split("_Types_", 1)[1]
        out.append({"api": api, "entity": stem, "variant": (ev[len(stem):] or None),
                    "authority": authority, "norm": _norm_entity(stem),
                    "fields": fields, "relations": relations})
    return out

def _peel(expr):
    """Cluster C #8 — unwrap a generated columnDefinitions value to its literal. Peels
    errorHandling.invoke(() => (X)) → X, typeResolver.toString('X') → 'X', typeResolver.toBoolean(b) → bool;
    resolves a bare '...'/"..."/true/false/null literal. Returns None on any unrecognised shape (→ caller
    falls back to the field name; never fabricates). Never raises. A naive literal read gets nothing — the
    probe showed EVERY value is wrapped."""
    if expr is None:
        return None
    s = str(expr).strip()
    for _ in range(6):                                    # bounded unwrap (invoke → toString/toBoolean → literal)
        m = re.match(r"errorHandling\.invoke\(\s*\(\)\s*=>\s*\((.*)\)\s*\)$", s, re.S)
        if m:
            s = m.group(1).strip(); continue
        m = re.match(r"typeResolver\.to(?:String|Boolean)\((.*)\)$", s, re.S)
        if m:
            s = m.group(1).strip(); continue
        break
    if s in ("true", "false"):
        return s == "true"
    if s in ("null", "undefined"):
        return None
    m = re.match(r"^'([^']*)'$", s) or re.match(r'^"([^"]*)"$', s)
    return m.group(1) if m else None

def _obj_value(obj, key):
    """Raw value expression for `key:` in an object-literal substring, up to the matching top-level comma
    or the object's own closing brace (paren/bracket/brace/string-aware). None if the key is absent."""
    m = re.search(rf"(?<![A-Za-z0-9_$]){re.escape(key)}\s*:", obj)
    if not m:
        return None
    i, n, depth, quote, start = m.end(), len(obj), 0, None, m.end()
    while i < n:
        c = obj[i]
        if quote:
            if c == "\\":
                i += 2; continue
            if c == quote:
                quote = None
        elif c in "'\"`":
            quote = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            if depth == 0:
                break                                     # the object's own closing brace
            depth -= 1
        elif c == "," and depth == 0:
            break
        i += 1
    return obj[start:i].strip()

def _decode_endpoint(view, tail):
    """Cluster C #8 — decode a generated `api/Documents/Pages/<View>/<tail>` route string. `_46`→`.`,
    `_95`→`_` (ASCII encoding). The decoded tail is `<Control>.<Event>…Click.<Connector>_<Function>`: the
    last dotted segment is `<Connector>_<Function>` (connector/function split on its first `_`; connector
    names carry no `_` in the corpus). Returns {control, connector, function, decoded}."""
    decoded = tail.replace("_46", ".").replace("_95", "_")
    segs = decoded.split(".")
    connector, _, function = segs[-1].partition("_")
    return {"control": segs[0] if segs else None, "connector": connector or None,
            "function": function or None, "decoded": decoded}

def read_view_columns(app_dir):
    """Cluster C #8 — parse rendered domain `views/*.vue` for per-grid column labels/visibility/clickability
    + the page→connector-function endpoints. Only TOP-LEVEL `views/*.vue` (excludes the administration/
    authentication/errors/layout/templates subdirs and StartPage.vue). Each `<Grid>ColumnDefinitions: [`
    is bounded via bracket-balancing (view files reach 1.3 MB — NEVER structure the whole file) and each
    column value `_peel`ed. Returns {view: {grids: {grid_var: [{name,label,visible,clickable}]}, endpoints:[…]}};
    {} when views/ is absent."""
    base = os.path.join(app_dir, "ClientApp", "src", "views")
    if not os.path.isdir(base):
        return {}
    out = {}
    for fn in sorted(os.listdir(base)):
        if not fn.endswith(".vue") or fn == "StartPage.vue":
            continue
        fp = os.path.join(base, fn)
        if not os.path.isfile(fp):                        # skip subdirs (admin/auth/errors/layout/templates)
            continue
        try:
            txt = open(fp, encoding="utf-8-sig", errors="ignore").read()
        except Exception:
            continue
        view = fn[:-4]
        grids = {}
        for m in re.finditer(r"([A-Za-z0-9_$]*)ColumnDefinitions\s*:\s*\[", txt):  # capital C excludes the template binding
            block = _balanced_block(txt, m.end() - 1, "[", "]")
            cols = []
            for obj in _split_object_literals(block):
                name = _peel(_obj_value(obj, "name"))
                if not name:                              # unpeelable name → skip the column (fabricate nothing)
                    continue
                cols.append({"name": name,
                             "label": _peel(_obj_value(obj, "headerText")),
                             "visible": _peel(_obj_value(obj, "visible")),
                             "clickable": bool(_peel(_obj_value(obj, "hasClickEvent")))})
            if cols:
                grids.setdefault(m.group(1), cols)        # first definition wins
        endpoints, seen = [], set()
        for em in re.finditer(r"api/Documents/Pages/([A-Za-z0-9_$]+)/([A-Za-z0-9_$]+)", txt):
            ep = _decode_endpoint(em.group(1), em.group(2))
            if ep["decoded"] in seen:
                continue
            seen.add(ep["decoded"])
            endpoints.append(ep)
        if grids or endpoints:
            out[view] = {"grids": grids, "endpoints": endpoints}
    return out

# --------------------------------------------------------------------------- asset projection (--emit-assets)
# All Tier-1 sharding/projection happens HERE in Python, so the LLM-facing skill never loads the
# full model.json. Each asset is lean markdown with a provenance header and a Tier-A (authoritative,
# [SRC]-quotable) / Tier-B (advisory design signal) split.

def _flat(s):
    return " ".join(str(s if s is not None else "").split())

def _control_text(kp):
    for k in ("Text", "Label", "HeaderText", "Title", "Placeholder"):
        v = kp.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _as_int(v):
    """Best-effort int — control props store numbers as int or numeric string."""
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return None


def _enum_choices(opts):
    """Verbatim inline `Options` -> ordered display labels (text, falling back to value).
    Returns [] for an empty list or a runtime binding (the caller handles `OptionsField` separately)."""
    out = []
    if not isinstance(opts, list):
        return out
    for o in opts:
        if isinstance(o, dict):
            txt = o.get("text")
            lab = txt if isinstance(txt, str) and txt.strip() else o.get("value")
            if lab is not None and str(lab).strip():
                out.append(str(lab).strip())
        elif isinstance(o, (str, int, float)) and str(o).strip():
            out.append(str(o).strip())
    return out


def _control_constraints(kp):
    """Cluster A #1 — ordered, non-empty field-behaviour annotations from a control's `key_props`.
    Every entry is a Tier-A verbatim projection; emitted only when the prop carries real data
    (presence != data — 254 empty strings + 999 nulls observed across the corpus)."""
    kp = kp or {}
    out = []
    hint = kp.get("Hint")
    if isinstance(hint, str) and hint.strip():
        out.append(f'hint: "{_redact_pii(_flat(hint))}"')
    tip = kp.get("ToolTip")
    if isinstance(tip, str) and tip.strip():
        out.append(f'tooltip: "{_redact_pii(_flat(tip))}"')
    if kp.get("ReadOnly"):
        out.append("read-only")
    if kp.get("IsPassword"):
        out.append("password-masked")
    rows = _as_int(kp.get("VisibleLines")) or _as_int(kp.get("Rows"))
    if rows and rows > 1:
        out.append(f"multi-line ({rows} rows)")
    choices = _enum_choices(kp.get("Options"))
    if choices:
        shown = choices[:12]
        more = f" _(+{len(choices) - len(shown)} more)_" if len(choices) > len(shown) else ""
        out.append("choices: " + ", ".join(f'"{c}"' for c in shown) + more)
    elif kp.get("OptionsField"):
        out.append("dynamic choices (bound)")
    exts = kp.get("AllowedExtensions")
    if isinstance(exts, str) and exts.strip():
        out.append(f"accepts: {_flat(exts)}")
    elif isinstance(exts, list) and exts:
        out.append("accepts: " + ", ".join(str(e).strip() for e in exts if str(e).strip()))
    grid = [lbl for flag, lbl in (("AllowExport", "exportable"),
                                  ("DisplaySearchBar", "searchable"),
                                  ("HasSelectableData", "selectable")) if kp.get(flag)]
    if grid:
        out.append("grid: " + " / ".join(grid))
    return out


def _columns_line(cols):
    """Cluster A #2 — render a DataGrid's resolved ordered columns as one Tier-A line. Shows the
    field-name binding + human label: `` `FieldName` "Human Label" `` when they differ (Cluster C makes
    the binding explicit — the wireframe data-prop), `"Label"` when equal, `` `FieldName` `` when the
    HeaderText is a non-literal binding (an unresolved `.sapz` Expression → shown by name, never as a
    raw blob; the rendered view resolves the literal via #8). `(action)` for command columns, `(hidden)`
    for Visible:false. Unresolved column GUIDs surface as `(unresolved)` — never invented."""
    parts = []
    for c in cols or []:
        if c.get("unresolved"):
            parts.append("(unresolved)")
            continue
        name = c.get("name")
        ht = c.get("header_text")
        label = ht.strip() if isinstance(ht, str) and ht.strip() else None   # non-string HeaderText = a binding/Expression
        tags = []
        if c.get("kind") == "action":
            tags.append("action")
        if c.get("visible") is False:
            tags.append("hidden")
        if name and label and label != name:
            disp = f'`{name}` "{label}"'
        elif label:
            disp = f'"{label}"'
        elif name:
            disp = f'`{name}`'
        else:
            disp = "(unnamed)"
        parts.append(disp + (f"({', '.join(tags)})" if tags else ""))
    return "columns (in order): " + ", ".join(parts)

def _column_divergences(sapz_cols, rendered_cols):
    """Cluster C #8 — compare the rendered view's grid columns to the `.sapz` #2 columns (matched by field
    name). The `.sapz` #2 already resolves label/visibility/clickability for ~all columns, so this returns
    ONLY the divergences (deployed rendered source vs the design package — the DA#1 staleness cross-check):
    a resolved Expression header, a label/visibility/clickability mismatch, or a rendered-only column.
    Empty list when they agree (the common case) or there is no rendered grid. Each note is Tier-A."""
    notes, r_by, matched = [], {}, set()
    for rc in rendered_cols or []:
        nm = (rc.get("name") or "").lower()
        if nm:
            r_by.setdefault(nm, rc)
    for sc in sapz_cols or []:
        if sc.get("unresolved"):
            continue
        nm = (sc.get("name") or "").lower()
        rc = r_by.get(nm)
        if not rc:
            continue
        matched.add(nm)
        sh = sc.get("header_text")
        s_label = sh.strip() if isinstance(sh, str) and sh.strip() else None
        rl = rc.get("label")
        if rl and s_label is None:                    # design header was an unresolved binding/Expression
            notes.append(f"`{sc.get('name')}` header resolves to \"{rl}\" (design header is an unresolved binding)")
        elif rl and s_label and rl != s_label:
            notes.append(f"`{sc.get('name')}` label differs — design \"{s_label}\" / deployed \"{rl}\"")
        rv, sv = rc.get("visible"), sc.get("visible")
        if isinstance(rv, bool) and isinstance(sv, bool) and rv != sv:
            notes.append(f"`{sc.get('name')}` visibility differs — design {'visible' if sv else 'hidden'} / "
                         f"deployed {'visible' if rv else 'hidden'}")
        rcl, scl = rc.get("clickable"), sc.get("has_action")
        if isinstance(rcl, bool) and isinstance(scl, bool) and rcl != scl:
            notes.append(f"`{sc.get('name')}` clickability differs — design {'clickable' if scl else 'static'} / "
                         f"deployed {'clickable' if rcl else 'static'}")
    for rc in rendered_cols or []:
        nm = (rc.get("name") or "").lower()
        if nm and nm not in matched:
            lbl = rc.get("label")
            notes.append(f"rendered-only column `{rc.get('name')}`" + (f" \"{lbl}\"" if lbl and lbl != rc.get("name") else ""))
    return notes


_COLUMN_TYPE_ENUM = {0: "data", 1: "action"}

def _decode_column_type(v):
    """Cluster A #2 — DataGrid Column `ColumnType` int enum: 0=data, 1=action. Unknown ints round-trip
    as `type<N>` (fabricate-nothing; widen the map if a broader probe surfaces more values)."""
    i = _as_int(v)
    if i is None:
        return None
    return _COLUMN_TYPE_ENUM.get(i, f"type{i}")


def _resolve_columns(props, registry):
    """Cluster A #2 — resolve a DataGrid control's `Columns` (ordered GUID list) into ordered column
    defs via the design-model registry. Build-time only (the registry is not in the returned model).
    Column GUIDs may be raw strings, bytes_le blobs, or `{ID|NamedItemID: guid}` refs. Unresolved GUIDs
    surface as `{"unresolved": <guid>}` — never fabricated. Columns carry NO DataField (verified 0/841),
    so no data-field binding is emitted; `HeaderText`/`Name` are the Tier-A facts."""
    out = []
    for gid in (props.get("Columns") or []):
        ref = gid.get("ID") or gid.get("NamedItemID") if isinstance(gid, dict) else gid
        nid = norm_guid(ref)
        col = registry.get(nid) if nid else None
        if not col:
            out.append({"unresolved": nid or str(gid)})
            continue
        cp = col.get("props") or {}
        vis = cp.get("Visible")
        out.append({
            "guid": nid,
            "header_text": cp.get("HeaderText"),
            "name": col.get("name") or cp.get("Name"),
            "visible": not (vis is False or str(vis).strip().lower() in ("false", "0")),
            "kind": _decode_column_type(cp.get("ColumnType")),
            "has_action": bool(cp.get("ClickEventHandlerScript")),
        })
    return out

_SQL_DENY = {"dbo", "sys", "master", "tempdb", "model", "msdb", "information_schema", "spt_values"}

def _sql_last(tok):
    """Final identifier of a possibly schema-qualified name (master.dbo.X -> X)."""
    return tok.replace("[", "").replace("]", "").lstrip("@").split(".")[-1]

def _paren_block(s, open_idx):
    """s[open_idx] is '('. Return the text inside up to its matching ')' (paren-balanced)."""
    depth = 0
    for i in range(open_idx, len(s)):
        if s[i] == "(":
            depth += 1
        elif s[i] == ")":
            depth -= 1
            if depth == 0:
                return s[open_idx + 1:i]
    return s[open_idx + 1:]

def _split_top(s):
    """Split on commas that are NOT inside parentheses (so varchar(150) / ISNULL(a,b) stay whole)."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur); cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts

def _sql_shape(query):
    """Best-effort parse: {verb, tables[], primary, columns[]} from a SQL/connector query string.
    Schema prefixes (dbo/master/...), CTE names and system schemas are filtered out; a table
    variable (DECLARE @X TABLE(...)) becomes a synthetic entity when no real table owns the columns."""
    q = _flat(query)
    if not q:
        return None
    verb = None
    for v in ("INSERT", "UPDATE", "DELETE", "MERGE"):
        if re.search(rf"(?i)\b{v}\b", q):
            verb = v; break
    if verb is None and re.search(r"(?i)\bSELECT\b", q):
        verb = "SELECT"
    if verb is None and re.search(r"(?i)\b(EXEC|EXECUTE)\b", q):
        verb = "EXEC"
    ctes = set(n.lower() for n in re.findall(r"(?i)(?:\bWITH\b|,)\s*([A-Za-z_][A-Za-z0-9_]*)\s+AS\s*\(", q))
    raw = re.findall(r"(?i)\b(?:FROM|JOIN|INTO|UPDATE)\s+(@?[A-Za-z_][A-Za-z0-9_.\[\]]*)", q)
    tables = []
    for t in raw:
        last = _sql_last(t)
        if not last or last.lower() in _SQL_DENY or last.lower() in ctes or last.lower() in ("select", "set", "values"):
            continue
        if last not in tables:
            tables.append(last)
    cols = []
    mi = re.search(r"(?i)INSERT\s+INTO[^(]*\(", q)
    md = re.search(r"(?i)DECLARE\s+@(\w+)\s+TABLE\s*\(", q)
    ms = re.search(r"(?i)\bSELECT\b\s+(?:TOP\s+\d+\s+)?(.+?)\s+\bFROM\b", q)
    if mi:
        cols = [p.strip().strip("[]@") for p in _split_top(_paren_block(q, mi.end() - 1)) if p.strip()]
    elif md:
        cols = [p.strip().split()[0].strip("[]") for p in _split_top(_paren_block(q, md.end() - 1)) if p.strip()]
    elif ms and "*" not in ms.group(1):
        for c in _split_top(ms.group(1)):
            c = re.sub(r"(?i)\s+AS\s+\w+\s*$", "", c.strip())
            c = c.split(".")[-1].strip("[]")
            if c and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", c):
                cols.append(c)
    # the "primary" table owns the columns (INSERT INTO / UPDATE / DELETE FROM / first FROM);
    # joined tables are listed in `tables` for CRUD presence but are not attributed columns.
    primary = None
    mp = (re.search(r"(?i)\bINSERT\s+INTO\s+(@?[A-Za-z_][A-Za-z0-9_.\[\]]*)", q) or
          re.search(r"(?i)\bUPDATE\s+(@?[A-Za-z_][A-Za-z0-9_.\[\]]*)", q) or
          re.search(r"(?i)\bDELETE\s+FROM\s+(@?[A-Za-z_][A-Za-z0-9_.\[\]]*)", q) or
          re.search(r"(?i)\bFROM\s+(@?[A-Za-z_][A-Za-z0-9_.\[\]]*)", q))
    if mp:
        cand = _sql_last(mp.group(1))
        if cand and cand.lower() not in _SQL_DENY and cand.lower() not in ctes:
            primary = cand
    if md and not primary:                       # synthetic entity from a table-variable shape
        primary = md.group(1)
    if not primary and tables:
        primary = tables[0]
    # source/locator/col_types added so the SQL shape shares one contract with _sp_shape/_ws_shape.
    # (locator is filled per-function by reconcile_entities; SQL columns get their types there too.)
    return {"verb": verb, "tables": tables, "primary": primary,
            "columns": [c for c in cols if c][:50], "source": "sql", "locator": None, "col_types": {}}

# --------------------------------------------------------------------------- stored-proc / web-service shapers
# Siblings to _sql_shape: they return the SAME {verb, tables, primary, columns} contract (+ source,
# locator, col_types) so the reconciliation layer treats all three evidence classes uniformly.

_HTTP_VERB = {0: "GET", 1: "POST", 2: "PUT", 3: "DELETE", 4: "PATCH"}
_HTTP_CRUD = {0: "SELECT", 1: "INSERT", 2: "UPDATE", 3: "DELETE", 4: "UPDATE"}
_SP_PREFIXES = {"sp", "prc", "usp", "fn", "udf", "proc"}
# Status/transport wrapper FIELDS to drop from SP params + WS payloads (case-insensitive).
# Deliberately narrow: a real column like `ApplicationID` (a multi-tenant FK) is genuine data and
# is NOT dropped — over-filtering fields would lose real SQL/proc columns.
_ENVELOPE_DENY = {"success", "message", "raiseexceptions", "statuscode", "responsebody", "apiresponse"}
# Broader denylist for ENTITY NAMES (incl. the WS path fallback): a transport wrapper is never an entity.
# _RENDERED_ENVELOPE (defined with the Cluster C readers above) adds the rendered types.js envelopes
# (DefaultResponse/GeneralError/ResponseId/ValidationResult/…) so they are denied from EVERY source, not
# just the rendered one — the WS path also names some of them (CosmoCrm ValidationResult).
_ENTITY_DENY = _ENVELOPE_DENY | {"result", "error", "response", "data"} | _RENDERED_ENVELOPE
# CRUD verb keywords matched against a path/proc-name. Order is documentary only — matching uses
# rightmost-position (a name like "createOrUpdate" resolves to its last action, UPDATE).
_VERB_KEYWORDS = [
    ("getlist", "SELECT"), ("getall", "SELECT"), ("list", "SELECT"), ("search", "SELECT"),
    ("select", "SELECT"), ("read", "SELECT"), ("fetch", "SELECT"), ("find", "SELECT"), ("get", "SELECT"),
    ("insert", "INSERT"), ("create", "INSERT"), ("add", "INSERT"), ("new", "INSERT"),
    ("update", "UPDATE"), ("edit", "UPDATE"), ("modify", "UPDATE"), ("save", "UPDATE"), ("set", "UPDATE"),
    ("delete", "DELETE"), ("remove", "DELETE"), ("disable", "DELETE"), ("deactivate", "DELETE"),
]
_VERB_MAP = dict(_VERB_KEYWORDS)
_GUID_RE = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

def _keyword_verb(text):
    """Rightmost CRUD keyword found as a substring of text -> verb (or None)."""
    text = (text or "").lower()
    best_pos, best_verb = -1, None
    for kw, verb in _VERB_KEYWORDS:
        pos = text.rfind(kw)
        if pos > best_pos:
            best_pos, best_verb = pos, verb
    return best_verb

def _entity_from_path(path):
    """Last real path segment -> candidate entity name; strips a leading verb (deletemember->member)."""
    if not path:
        return None
    segs = [s for s in re.split(r"[/\\]", str(path)) if s and not s.startswith("{") and "?" not in s]
    if not segs:
        return None
    seg = segs[-1]
    low = seg.lower()
    for kw, _v in _VERB_KEYWORDS:
        if low.startswith(kw) and len(low) > len(kw):
            return seg[len(kw):]
    return seg

def _ws_shape(hint, fn_name=""):
    """WebService function shape. NAME from Body/Response CustomType ref (else path); verb from
    path/name keyword (else HTTP method — GET is used for semantic deletes in the corpus, so the
    keyword wins). FIELDS from the write body (else the response), envelope-filtered."""
    if not hint:
        return None
    path = hint.get("path") or ""
    method = _HTTP_VERB.get(hint.get("http_method"))
    verb = _keyword_verb(f"{path} {fn_name or ''}") or _HTTP_CRUD.get(hint.get("http_method"))
    is_write = verb in ("INSERT", "UPDATE", "DELETE")
    body_name, resp_name = hint.get("body_name"), hint.get("resp_name")
    name = None
    for cand in ([body_name, resp_name] if is_write else [resp_name, body_name]):
        if cand and cand.lower() not in _ENTITY_DENY and not re.fullmatch(_GUID_RE, cand):
            name = cand
            break
    if not name:
        name = _entity_from_path(path) or _entity_from_path(fn_name)
    if not name or re.fullmatch(_GUID_RE, name) or name.lower() in _ENTITY_DENY:
        return None
    raw_fields = (hint.get("body_fields") if (is_write and hint.get("body_fields"))
                  else (hint.get("resp_fields") or hint.get("body_fields") or []))
    cols, col_types = [], {}
    for fl in raw_fields:
        col = fl.get("path") or fl.get("name")
        if not col or col.split(".")[-1].lower() in _ENVELOPE_DENY:
            continue
        # NB: IsDataField is NOT used as a gate — it is uniformly 0 in deployed .sapz models,
        # so gating on it would drop every field. The envelope denylist is the real guard.
        if col not in cols:
            cols.append(col)
        t = fl.get("type")
        if t and str(t).lower() not in ("object", "system.object"):
            col_types[col] = t
    return {"verb": verb, "tables": [name], "primary": name, "columns": cols[:50],
            "source": "web-service", "locator": f"from web-service: {(method or '?')} {path}".strip(),
            "col_types": col_types}

def _sp_entity_verb(proc_name):
    """`<prefix>_[Stadium_]<Entity>[_<qual>]_<Op>` -> (entity, verb). Rightmost op-keyword wins.
    Empirical Twenty57 convention, NOT a platform guarantee; no match -> (None, None)."""
    base = _sql_last(proc_name or "")
    parts = [p for p in re.split(r"[_\s]+", base) if p]
    while parts and parts[0].lower() in _SP_PREFIXES:
        parts = parts[1:]
    if parts and parts[0].lower() == "stadium":
        parts = parts[1:]
    verb, op_idx = None, None
    for i, seg in enumerate(parts):
        if seg.lower() in _VERB_MAP:
            verb, op_idx = _VERB_MAP[seg.lower()], i
    if verb is None or op_idx in (None, 0):
        return None, None
    entity = "".join(parts[:op_idx])
    return (entity or None), verb

def _sp_shape(hint):
    """StoredProcedure shape: entity+verb from the proc name, fields from parameters (envelope-filtered)."""
    if not hint:
        return None
    entity, verb = _sp_entity_verb(hint.get("proc_name"))
    if not entity or not verb:
        return None  # unclassified -> caller lists it under Tier-B
    cols, col_types = [], {}
    for nm in hint.get("params", []) or []:
        if not nm or nm.lower() in _ENVELOPE_DENY:
            continue
        if nm not in cols:
            cols.append(nm)
        t = (hint.get("param_types") or {}).get(nm)
        if t and str(t).lower() not in ("object", "system.object"):
            col_types[nm] = t
    return {"verb": verb, "tables": [entity], "primary": entity, "columns": cols[:50],
            "source": "stored-procedure", "locator": f"from stored-procedure: {hint.get('proc_name')}",
            "col_types": col_types}

# --------------------------------------------------------------------------- entity reconciliation
# Aggressive union by normalized name: one entity per normalized name, unioning fields from SQL,
# stored-proc and web-service evidence. Every field is real and carries per-source [from ...] locators
# (completeness, not fabrication); noise is kept out by the envelope denylist + weak-type omission.

def _norm_entity(name):
    """Merge KEY for an entity name (NOT the display spelling): strip schema/prefixes, lowercase,
    de-punctuate, naive-singularize. `Members`(table) and `member`(API) collapse; `member`/`fullmember`
    keep distinct stems (union-by-name does not over-collapse DTO variants)."""
    s = _sql_last(str(name or "")).lower()
    s = re.sub(r"^(vw|tbl|tb|cf|prc|sp|usp)_?", "", s)
    s = re.sub(r"^stadium_?", "", s)
    s = re.sub(r"[^a-z0-9]", "", s)
    if s.endswith("ies") and len(s) > 4:
        s = s[:-3] + "y"
    elif s.endswith("ses") and len(s) > 4:
        s = s[:-2]
    elif s.endswith("s") and not s.endswith("ss") and len(s) > 3:
        s = s[:-1]
    return s

def _variant_norm(name):
    """Cluster C #6 — merge key that ALSO strips a trailing rendered-types variant token before norming,
    so a web-service shape keyed on the raw type name (`CustomerRead`, `CustomerWrite`, `BeneficiaryReadList`)
    collapses onto the variant-stripped rendered stem (`Customer`, `Beneficiary`). Case-sensitive PascalCase
    token matching means a SQL table like `Bread` / `Blacklist` never strips — only genuine
    `<Entity><Variant>` names do."""
    s = re.sub(r"^_+", "", str(name or ""))
    if s.endswith("List") and len(s) > 4:              # ReadList/WriteList/List → drop List, keep the stem
        s = s[:-4]
    stem, _ = _rendered_entity_stem(s)
    return _norm_entity(stem or s)

# Normalized transport/scratch names that are never domain entities from ANY source — this also
# catches SQL `DECLARE @result TABLE(...)` scratch table-variables surfaced by _sql_shape.
_ENTITY_DENY_NORM = {_norm_entity(x) for x in _ENTITY_DENY}
_SOURCE_RANK = {"sql": 3, "stored-procedure": 2, "rendered-types": 2, "web-service": 1}  # richer spelling wins the display name
# rendered-types ranks below sql (design-model type/spelling wins on conflict) but above web-service so
# the clean PascalCase API type name (`Beneficiary`) beats an ugly WS-path-derived spelling.

def _blank_entity():
    return {"_disp": None, "sources": set(), "aliases": set(), "ops": set(), "fns": [], "fields": {}}

def reconcile_entities(model):
    """Union entities across all evidence classes. Returns (entities_by_norm, unclassified_procs).
    Sets f["_shape"] on each function. All sets are converted to sorted lists in the result."""
    reconciled = {}
    unclassified = []

    def consider_display(rec, spelling, source):
        rank = _SOURCE_RANK.get(source, 0)
        if rec["_disp"] is None or rank > rec["_disp"][1]:
            rec["_disp"] = (spelling, rank)

    for c in model.get("connectors", []) or []:
        for f in c.get("functions", []) or []:
            ftype = f.get("type") or ""
            if ftype == "WebServiceFunction":
                shape = _ws_shape(f.get("shape_hint"), f.get("name"))
            elif ftype == "StoredProcedure":
                shape = _sp_shape(f.get("shape_hint"))
                if shape is None and f.get("shape_hint", {}).get("proc_name"):
                    unclassified.append(f["shape_hint"]["proc_name"])
            else:
                shape = _sql_shape(f.get("query"))
            f["_shape"] = shape
            if not shape:
                continue
            source = shape.get("source", "sql")
            locator = shape.get("locator") or (f"from connector: {f.get('name')}" if source == "sql" else None)
            sql_ptypes = {}
            if source == "sql":
                sql_ptypes = {p.get("name"): (p.get("db_type") or p.get("type"))
                              for p in f.get("parameters", []) or []}
            # secondary tables get presence (name) only
            for t in shape.get("tables", []) or []:
                k = _norm_entity(t)
                if not k or k in _ENTITY_DENY_NORM:
                    continue
                rec = reconciled.setdefault(k, _blank_entity())
                rec["sources"].add(source)
                rec["aliases"].add(t)
                consider_display(rec, t, source)
            prim = shape.get("primary")
            if not prim:
                continue
            k = _norm_entity(prim)
            if not k or k in _ENTITY_DENY_NORM:
                continue
            rec = reconciled.setdefault(k, _blank_entity())
            rec["sources"].add(source)
            rec["aliases"].add(prim)
            consider_display(rec, prim, source)
            if shape.get("verb"):
                rec["ops"].add(shape["verb"])
            if f.get("name"):
                rec["fns"].append(f["name"])
            for col in shape.get("columns", []) or []:
                col = col if isinstance(col, str) else (col.get("path") or col.get("name"))
                if not col:
                    continue
                fk = re.sub(r"[^a-z0-9.]", "", col.lower())
                if not fk:
                    continue
                fr = rec["fields"].get(fk)
                if fr is None:
                    fr = {"name": col, "path": col, "types": set(), "sources": set(), "ops": set(),
                          "locators": [], "authority": set()}
                    rec["fields"][fk] = fr
                fr["sources"].add(source)
                if shape.get("verb"):
                    fr["ops"].add(shape["verb"])
                if locator and locator not in fr["locators"]:
                    fr["locators"].append(locator)
                t = (shape.get("col_types") or {}).get(col) or sql_ptypes.get(col)
                if t and str(t).lower() not in ("object", "system.object"):
                    fr["types"].add(t)

    # Cluster C #6 — rendered types.js as a new evidence class. Supplies FE↔API field shapes for the
    # web-service apps the `.sapz` type reconciliation missed. types.js carries NO type/nullability (all
    # `= undefined`), so a rendered field NEVER overrides a `.sapz`/SQL type — it only ADDS to the closed
    # set (design-model type still wins on conflict). Each rendered field carries a `[from rendered types]`
    # locator + a per-field authority (Tier-B: display/editable/action, from the class variant). Nested-type
    # relations feed §2.2. Envelopes / `*Validation` / `*List` wrappers are pre-excluded by the reader.
    for rt in model.get("rendered_types", []) or []:
        k = rt.get("norm")
        if not k or k in _ENTITY_DENY_NORM:
            continue
        rec = reconciled.setdefault(k, _blank_entity())
        rec["sources"].add("rendered-types")
        rec["aliases"].add(rt["entity"])
        consider_display(rec, rt["entity"], "rendered-types")
        for fdef in rt.get("fields", []) or []:
            nm = fdef["name"]
            fk = re.sub(r"[^a-z0-9.]", "", nm.lower())
            if not fk:
                continue
            fr = rec["fields"].get(fk)
            if fr is None:
                fr = {"name": nm, "path": nm, "types": set(), "sources": set(), "ops": set(),
                      "locators": [], "authority": set()}
                rec["fields"][fk] = fr
            fr["sources"].add("rendered-types")
            fr.setdefault("authority", set()).add(fdef["authority"])
            if "from rendered types" not in fr["locators"]:
                fr["locators"].append("from rendered types")
        rels = rec.setdefault("rel", {})
        for fld_name, elem_entity in (rt.get("relations") or {}).items():
            if elem_entity:
                rels[fld_name] = elem_entity

    # Cluster C #6 — consolidate variant-siblings. Web-service shapes are keyed on the raw type name
    # (`CustomerRead`/`CustomerWrite`), which plain `_norm_entity` does NOT variant-strip, so they sit
    # beside the rendered `Customer`. Re-group every entity by its variant-stripped stem and fold each
    # group into its cleanest member (the one already at the stem key / rendered / richest). This both
    # de-duplicates the rendered↔WS split and cleans the pre-existing "247 fields / 4 typed" WS sprawl —
    # #6's core purpose. GATED on rendered_types so pure-SQL apps stay byte-identical (no-op).
    if model.get("rendered_types"):
        groups = {}
        for key, rec in reconciled.items():
            disp = rec["_disp"][0] if rec["_disp"] else key
            groups.setdefault(_variant_norm(disp), []).append(key)
        for canon, keys in groups.items():
            if len(keys) < 2 or not any("rendered-types" in reconciled[k]["sources"] for k in keys):
                continue                                  # only fold groups #6 actually contributed to
            def _score(k, canon=canon):
                rec = reconciled[k]
                disp = rec["_disp"][0] if rec["_disp"] else k
                return (_norm_entity(disp) == canon, "rendered-types" in rec["sources"], len(rec["fields"]))
            target = max(keys, key=_score)
            dst = reconciled[target]
            for k in keys:
                if k == target:
                    continue
                src = reconciled.pop(k)
                dst["sources"] |= src["sources"]; dst["aliases"] |= src["aliases"]; dst["ops"] |= src["ops"]
                dst["fns"] = list(dict.fromkeys(dst["fns"] + src["fns"]))
                dst.setdefault("rel", {}).update(src.get("rel", {}))
                for fk, fr in src["fields"].items():
                    ex = dst["fields"].get(fk)
                    if ex is None:
                        dst["fields"][fk] = fr
                        continue
                    ex["types"] |= fr["types"]; ex["sources"] |= fr["sources"]; ex["ops"] |= fr["ops"]
                    ex.setdefault("authority", set())
                    ex["authority"] |= fr.get("authority", set())
                    for loc in fr["locators"]:
                        if loc not in ex["locators"]:
                            ex["locators"].append(loc)

    # fill still-untyped fields from the design-model data dictionary (concrete beats none)
    type_by_field = {}
    for d in model.get("data_dictionary", []) or []:
        for fl in d.get("fields", []) or []:
            nm, ty = fl.get("name"), fl.get("type")
            if nm and ty and str(ty).lower() not in ("object", "system.object"):
                type_by_field.setdefault(re.sub(r"[^a-z0-9.]", "", str(nm).lower()), ty)
    for rec in reconciled.values():
        for fk, fr in rec["fields"].items():
            if not fr["types"] and fk in type_by_field:
                fr["types"].add(type_by_field[fk])

    keys = list(reconciled.keys())
    out = {}
    for k, rec in reconciled.items():
        related = sorted({reconciled[o]["_disp"][0] for o in keys
                          if o != k and len(o) >= 3 and len(k) >= 3 and (o in k or k in o)})
        fields = []
        for fr in rec["fields"].values():
            fields.append({"name": fr["name"], "path": fr["path"],
                           "type": (sorted(fr["types"])[0] if fr["types"] else None),
                           "types": sorted(fr["types"]), "sources": sorted(fr["sources"]),
                           "ops": sorted(fr["ops"]), "locators": fr["locators"],
                           "authority": sorted(fr.get("authority") or [])})
        fields.sort(key=lambda x: x["path"].lower())
        out[k] = {"display": rec["_disp"][0] if rec["_disp"] else k, "norm": k,
                  "sources": sorted(rec["sources"]), "ops": sorted(rec["ops"]),
                  "aliases": sorted(rec["aliases"]), "related": related,
                  "fns": rec["fns"], "fields": fields, "rel": rec.get("rel", {})}
    return out, sorted(set(unclassified))

def _prov_header(model, category, extra=None):
    app = model.get("application", {}) or {}
    dep = model.get("deployment", {}) or {}
    L = ["---",
         f"stadium_asset: {category}",
         f"app: {model.get('_app_name') or app.get('name') or 'Unknown'}",
         f"file_guid: {model.get('_file_guid') or ''}",
         f"designer_version: {app.get('designer_version') or ''}",
         f"selected_package: {dep.get('selected_package') or ''}",
         f"extracted_from: {model.get('_extracted_from') or ''}",
         "provenance: deterministic extraction from the Stadium 6 design model + administration.db",
         "marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals."]
    for k, v in (extra or {}).items():          # category-specific front-matter (e.g. design-signals logo pointer)
        L.append(f"{k}: {v if v is not None else 'null'}")
    L += ["---", ""]
    return "\n".join(L)

# --------------------------------------------------------------------------- Phase-0 behavioural render helpers
# Render-only enrichment (0a–0h): classifiers + joins over data the extractor ALREADY captured
# (control text, script names, action props, admin-db pages). No new source extraction here.
# Everything provably in the source is Tier-A ([SRC]-quotable); every interpretation is Tier-B
# ([AI-SUGGESTED]) and never [SRC]-citable.

# PII guard (CLAUDE.md invariant: never emit an email address). Redacts email addresses from any
# RENDERED text — notification/dialog messages, SetValue values (apps hardcode default sender
# addresses), validator messages — keeping the shape visible. Applied only at .md render; the
# forensic model.json's scripts[].actions stay raw (Phase-1 back-compat requires them untouched,
# and model.json is read by no downstream pipeline).
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
def _redact_pii(s):
    return _EMAIL_RE.sub("<redacted-email>", s) if isinstance(s, str) else s

# 0a — notification severity. Verified corpus mapping: 1 = success, 3 = error; every other code
# (0, 2, …) is the safe "info" default — never assert success/error on an unmapped code.
def _notif_severity(v):
    try:
        n = int(v)
    except (TypeError, ValueError):
        return None
    return {1: "success", 3: "error"}.get(n, "info")

def _notif_message(props):
    """Human message text of a Notification/DisplayMessageBox action, VERBATIM. Reads the raw
    props (NOT the lossy action `summary`, which resolves a message's placeholder to a bare control
    name); prefers a literal string, else the Expression `FormatString` (expression syntax kept)."""
    if not isinstance(props, dict):
        return None
    for key in ("Message", "Title"):
        v = props.get(key)
        if isinstance(v, str) and v.strip():
            return _flat(v)[:300]
        if isinstance(v, dict):
            fs = v.get("FormatString")
            if isinstance(fs, str) and fs.strip():
                return _flat(fs)[:300]
    return None

# 0g — trigger classification. The event token is literally the trailing dotted segment of the
# script name (btnNext.Click, MembersDataGrid.Delete.Click, Members.Load). Fact, not inference.
_USER_EVENTS = {"click": "clicks", "change": "changes", "select": "selects", "input": "enters text in",
                "blur": "leaves", "focus": "focuses", "check": "toggles", "keyup": "types in",
                "keydown": "types in", "dblclick": "double-clicks", "clicked": "clicks"}

def _script_trigger(name):
    """(class, event_token, gesture_verb). class ∈ {user-initiated, automatic-on-open, other …}."""
    parts = (name or "").split(".")
    last = parts[-1].lower() if len(parts) > 1 else ""
    if last == "load":
        return "automatic-on-open", last, None
    if last in _USER_EVENTS:
        return "user-initiated", last, _USER_EVENTS[last]
    if len(parts) <= 1:
        return "other (helper script)", "", None
    return "other (timer / lifecycle)", last, None

# 0e — action-verb taxonomy (corpus-observed + plan set; bounded, OQ4 default). A label carrying
# one of these verbs is a candidate user *task* (Tier-B). Pure UI chrome (nav/pagination/commit/
# list-controls) is exempt, mirroring the wireframe pipeline's UI-only exemption.
_ACTION_VERBS = {"approve", "reject", "submit", "create", "add", "delete", "remove", "assign",
                 "reassign", "export", "download", "upload", "capture", "review", "confirm",
                 "edit", "update", "generate", "accept", "link", "view", "send", "print",
                 "import", "archive", "allocate", "vet", "vetting", "reconcile", "publish"}
_UI_CHROME_LABELS = {"save", "cancel", "close", "back", "next", "previous", "prev", "ok",
                     "save draft", "apply filters", "clear filters", "clear", "search", "filter",
                     "refresh", "first", "last", "home", "<", ">", "«", "»"}
_ACTIONABLE_TYPES = {"Button", "LinkButton", "Hyperlink", "Link", "ImageButton"}

def _label_verb(label):
    """First action verb appearing as a whole word in a control label (else None)."""
    for w in re.findall(r"[A-Za-z]+", (label or "").lower()):
        if w in _ACTION_VERBS:
            return w
    return None

def _is_ui_chrome(label):
    return (label or "").strip().lower() in _UI_CHROME_LABELS

# 0b — page-kind taxonomy from a name suffix (~36% of corpus names carry one; the rest are bare
# entity nouns → per-entity maintenance surfaces). Tier-B [AI-SUGGESTED].
_PAGE_KIND_SUFFIXES = [
    (("dashboard",), "landing"),
    (("view",), "list"),
    (("details", "detail", "edit"), "detail"),
    (("add",), "create"),
    (("setup", "settings", "config"), "configure"),
    (("pool", "queue"), "work-queue"),
    (("reports", "report", "enquiries", "enquiry"), "reporting"),
    (("capture", "upload", "review"), "workflow-step"),
]

def _page_kind(name):
    n = (name or "").lower()
    for suffixes, kind in _PAGE_KIND_SUFFIXES:
        for suf in suffixes:
            if n.endswith(suf):
                return kind
    return "entity-maintenance"

# 0d/0h — task-cluster taxonomy (verb → operational cluster). Distinct clusters imply distinct
# operator roles even under a single RBAC role (the Tier-B leap the actor-candidate reading makes).
_TASK_CLUSTER = {
    "capture": "capture", "upload": "capture", "add": "capture", "create": "capture",
    "submit": "capture", "import": "capture",
    "approve": "approve/decide", "reject": "approve/decide", "review": "approve/decide",
    "assign": "approve/decide", "reassign": "approve/decide", "confirm": "approve/decide",
    "accept": "approve/decide", "allocate": "approve/decide", "vet": "approve/decide",
    "vetting": "approve/decide",
    "export": "reporting", "download": "reporting", "print": "reporting", "generate": "reporting",
    "view": "reporting", "publish": "reporting",
    "edit": "maintain", "update": "maintain", "delete": "maintain", "remove": "maintain",
    "archive": "maintain", "link": "maintain", "reconcile": "maintain", "send": "maintain",
}
# A surface *kind* (0b) also implies an operator even with no verb-labelled button — a
# workflow/queue/reporting screen is a distinguishing actor signal buttons alone miss. Only the
# distinguishing kinds map; baseline CRUD kinds (detail/list/entity-maintenance/configure/landing)
# do not spawn a cluster on their own.
_KIND_CLUSTER = {"workflow-step": "capture", "work-queue": "approve/decide", "reporting": "reporting"}

def _validator_rule(vtype, props):
    """Best-effort validator rule label from friendly type + props; None if unrecognised (the
    caller then falls back to `name (type)` — never fabricate a rule that isn't in the props)."""
    t = (vtype or "").lower()
    props = props or {}
    if "require" in t:
        return "required"
    if "regular" in t or "regex" in t:
        expr = props.get("ValidationExpression") or props.get("Expression") or props.get("Pattern")
        return f"format(regex: {_flat(expr)[:80]})" if isinstance(expr, str) and expr.strip() else "format(regex)"
    if "range" in t:
        lo, hi = props.get("MinimumValue"), props.get("MaximumValue")
        return f"range({lo}..{hi})" if (lo is not None or hi is not None) else "range"
    if "compare" in t:
        return "compare"
    if "email" in t:
        return "format(email)"
    return None

def _rule_intent(fmt):
    """Cluster A #1 — Tier-B advisory classification of an `IsValidRule` FormatString (email /
    numeric / date / length / pattern). The raw expression stays the Tier-A anchor; this only
    labels likely intent, so it is marked `[AI-SUGGESTED]` at render. Never raises."""
    s = _flat(fmt)
    if not s:
        return "pattern"
    if "dayjs(" in s.lower():
        return "date"
    m = re.search(r"/(.*)/[a-z]*\.test", s)          # regex body from `/…/.test({0})`
    body = m.group(1) if m else s
    if "@" in re.sub(r"\[[^\]]*\]", "", body):        # an @ outside any char class => email
        return "email"
    has_digit = ("[0-9]" in body) or ("\\d" in body)
    has_alpha = bool(re.search(r"\[a-zA-Z\]|\[a-z\]|\[A-Z\]|[A-Za-z]{2,}", body))
    if has_digit and not has_alpha:
        return "numeric"
    if re.search(r"\{\d+(,\d*)?\}", body):
        return "length"
    return "pattern"


def _control_validation_rows(all_controls):
    """Cluster A #1/#3 — project control validation props into `(rich_rows, required_only_names)`.
    `rich_rows` are §6.3-shaped lines for controls carrying a rule and/or a verbatim message;
    `required_only_names` are Required controls with neither (collapsed to one compact line by the
    caller). Empty `ErrorText` yields no message — never a bare `""`. FormatString braces are
    un-escaped (.NET composite format); the rule/message are Tier-A, the intent label is Tier-B."""
    rich_rows, req_only = [], []
    for c in all_controls or []:
        kp = c.get("key_props") or {}
        name = c.get("name")
        if not name:
            continue
        required = bool(kp.get("Required"))
        ivr = kp.get("IsValidRule")
        fmt = ivr.get("FormatString") if isinstance(ivr, dict) else (ivr if isinstance(ivr, str) else None)
        fmt = fmt if isinstance(fmt, str) and fmt.strip() else None
        err = kp.get("ErrorText")
        msg = _redact_pii(err.strip()) if isinstance(err, str) and err.strip() else None
        if not (required or fmt or msg):
            continue
        if not fmt and not msg:                       # required-only → compact list, not a row
            if name not in req_only:
                req_only.append(name)
            continue
        norm = _flat(fmt).replace("{{", "{").replace("}}", "}") if fmt else None
        intent = _rule_intent(norm) if norm else None
        types = (["required"] if required else []) + ([intent] if intent else [])
        bits = [f"`{name}`", "+".join(types) if types else "validation"]
        if norm:
            bits.append(norm if len(norm) <= 160 else norm[:160] + "…")
        if msg:
            bits.append(f'"{msg}"')
        marker = f"  `[AI-SUGGESTED: {intent}]`" if intent else ""
        rich_rows.append("- " + " · ".join(bits) + " [from design model]" + marker)
    return rich_rows, req_only

def _role_capability(role):
    """Tier-B capability reading of a role NAME (advisory; the split is a reading, not a grant)."""
    r = (role or "").lower()
    if any(k in r for k in ("view", "read", "report", "audit", "guest")):
        return "read-only (view)"
    if any(k in r for k in ("all", "admin", "full", "manage", "super", "owner", "edit")):
        return "full edit / manage"
    return "standard operator"

# 1c — render an action `tree` (built in read_design_model) as indented markdown. Linear steps as
# bullets; Decisions as `IF <predicate> → […]` / `ELSE → […]` blocks. A shared node budget caps a
# single huge handler with an explicit `(+N more)` note (never a silent truncation — DA#3).
_SUMMARY_KEYS = ("ConnectorFunction", "Target", "Destination", "ScriptToCall", "Message",
                 "Title", "Condition", "Value", "List", "Url")

def _summary_bits(sm):
    return "; ".join(f"{k}={_redact_pii(str(sm[k]))}" for k in _SUMMARY_KEYS if k in (sm or {}))

def _tree_has_decision(nodes):
    for n in nodes or []:
        if n.get("decision"):
            return True
        for b in n.get("branches", []):
            if _tree_has_decision(b.get("steps", [])):
                return True
    return False

def _iter_tree(nodes):
    """Depth-first over every node in an action tree (including inside branches)."""
    for n in nodes or []:
        yield n
        for b in n.get("branches", []):
            yield from _iter_tree(b.get("steps", []))

def _tree_md(nodes, indent, budget):
    """budget is a 1-element list (shared remaining-node counter). Returns markdown lines."""
    out = []
    for n in nodes or []:
        if budget[0] <= 0:
            out.append("  " * indent + "- _(+more steps — full tree in model.json)_")
            return out
        budget[0] -= 1
        if n.get("decision"):
            out.append("  " * indent + "- **Decision**" + (" *(has else)*" if n.get("show_else") else ""))
            for b in n.get("branches", []):
                if b.get("kind") == "else":
                    head = "ELSE"
                elif b.get("predicate"):
                    head = f"IF `{_redact_pii(b['predicate'])}`"
                else:
                    head = "IF *(condition unresolved)*"
                out.append("  " * (indent + 1) + f"- {head} →")
                out += _tree_md(b.get("steps", []), indent + 2, budget)
                if budget[0] <= 0:
                    return out
        else:
            bits = _summary_bits(n.get("summary"))
            tag = "  `[opaque: custom JS]`" if n.get("opaque") else ""
            trunc = "  _(…)_" if n.get("truncated") else ""
            out.append("  " * indent + f"- {n.get('action')}" + (f": {bits}" if bits else "") + tag + trunc)
    return out

# 1d — edge/empty/error/loading state signals. A SetValue targeting one of these UI-state suffixes
# is a loading/visibility toggle; the FACT is Tier-A, the {loading|empty|error|permission} LABEL is
# Tier-B (a `Visible=False` is ambiguous: busy vs empty vs initial-hide).
def _state_label(target, value):
    """Tier-B classification of a state toggle. Never asserted as Tier-A."""
    t = (target or "").lower()
    if any(k in t for k in ("spinner", "loader", "busy", "overlay")):
        return "loading"
    if "visible" in t or "container" in t:
        return "empty/hidden" if str(value).lower() in ("false", "0", "none") else "shown"
    return "state"

# ============================================================================ per-view USER TASKS
# Deterministic per-view user-task derivation (render-only over joins already materialized in
# emit_assets — NO new extraction). Task IDENTITY = the canonical CRUD verb (SELECT/INSERT/UPDATE/
# DELETE) or a raw non-CRUD verb token; NOT `_TASK_CLUSTER` (which maps update+delete → "maintain"
# and would silently collapse Edit + Delete into one row). The task OBJECT is closed-set only (a
# reconciled entity display, or blank) — never invented. The task NAME is Tier-B `[AI-SUGGESTED]`;
# its evidence chain (view, wired op, grid/column, title, roles) is Tier-A. Full contract:
# `framework/assets/stadium/asset-schemas.md` ("tasks").
_VERB_TASK_WORD = {"SELECT": "Browse", "INSERT": "Add", "UPDATE": "Update", "DELETE": "Delete"}
_VERB_SORT = {"SELECT": 0, "INSERT": 1, "UPDATE": 2, "DELETE": 3}      # inventory row order; non-CRUD last
# Page-kind → a fallback CRUD verb, used only when a view yields no op/grid/affordance task (S4).
_KIND_FALLBACK_VERB = {"create": "INSERT", "detail": "SELECT", "list": "SELECT", "reporting": "SELECT",
                       "work-queue": "SELECT", "configure": "UPDATE", "entity-maintenance": "UPDATE",
                       "workflow-step": "INSERT", "landing": None}
# A SELECT endpoint is a genuine *browse* task only on these page-kinds (or when a grid corroborates
# it); every other SELECT is a supporting read (dropdown lookup / form pre-fill), not a task.
_BROWSE_KINDS = {"list", "reporting", "work-queue", "detail"}
_NAME_RANK = {"affordance": 0, "action-col": 1, "title": 2, "synth": 3}   # lower = preferred human wording
_CONF_ORDER = {"low": 0, "medium": 1, "high": 2}

def _canon_verb(text):
    """Canonical task verb from arbitrary text: a CRUD keyword (substring, rightmost-wins) else an
    action-verb label token (approve/export/…). None if neither."""
    return _keyword_verb(text) or _label_verb(text)

def _resolve_entity(token, ent_by_norm):
    """Closed-set ONLY: normalize `token` → the reconciled entity's display spelling, else None.
    Never invents an entity (mirrors the §7 closed-property discipline)."""
    if not token:
        return None
    e = ent_by_norm.get(_norm_entity(token))
    return e.get("display") if e else None

def _endpoint_verb_entity(fn, ent_by_norm):
    """(verb, entity_display) for a camelCase rendered-endpoint function name (`MemberInsert`,
    `CitiesSelect`). verb via `_keyword_verb` (substring); entity by stripping the matched CRUD keyword
    from the stem and resolving the remainder against the closed set. `_sp_entity_verb` does NOT work
    here — it token-splits on `[_\\s]+` and an endpoint name carries no separator. entity may be None
    (unresolved → don't invent). The connector name is deliberately NOT used to bind the entity (in
    MemberAdmin every function sits under one connector `Members`, so it would mislabel `CitiesSelect`)."""
    verb = _keyword_verb(fn)
    if not verb:
        return None, None
    low = (fn or "").lower()
    for kw, v in _VERB_KEYWORDS:
        if v == verb and kw in low:
            ent = _resolve_entity(re.sub(re.escape(kw), "", fn, flags=re.I), ent_by_norm)
            if ent:
                return verb, ent
    return verb, None

def _task_display_name(raw, verb, entity):
    """Tier-B task name. Keep the app's own wording (`raw`) when it is multi-word or is itself the
    entity noun; else synthesize `<Word> <Entity>` from the verb + closed-set entity."""
    if raw:
        raw = raw.strip()
        words = re.findall(r"[A-Za-z0-9]+", raw)
        if len(words) > 1 or (entity and _norm_entity(raw) == _norm_entity(entity)):
            return raw[:1].upper() + raw[1:]
    word = _VERB_TASK_WORD.get(verb) or (verb.capitalize() if verb else "Use")
    return f"{word} {entity}" if entity else f"{word} (object unresolved)"

def _derive_view_tasks(views, ent_by_norm):
    """Per-view user-task derivation. `views` is a list of plain dicts (built by `emit_assets`):
        {name, title, kind, roles[], screen_entity,
         endpoints[{control,connector,function}],
         grids[{name, searchable, columns[{header_text,kind}]}],
         affordances[(control, label, verb, wired[])]}
    Returns a list (in view order) of {name, roles, tasks[], supporting_reads[], notask}. Every view
    yields ≥1 task OR an explicit `notask` reason — never silently absent (no-silent-truncation)."""
    results = []
    for v in views:
        name, kind, title = v["name"], v.get("kind"), v.get("title")
        sent = v.get("screen_entity")
        cand = {}                                   # (verb, norm_entity) -> merged candidate
        supporting = []

        def _add(verb, entity, raw, name_src, conf, ev):
            if not verb:
                return
            key = (verb, _norm_entity(entity) if entity else "")
            c = cand.get(key)
            if c is None:
                cand[key] = {"verb": verb, "entity": entity, "raw": raw,
                             "rank": _NAME_RANK[name_src], "conf": conf, "ev": list(ev)}
                return
            for loc in ev:                          # union evidence
                if loc not in c["ev"]:
                    c["ev"].append(loc)
            if _CONF_ORDER[conf] > _CONF_ORDER[c["conf"]]:   # triangulation upgrades confidence
                c["conf"] = conf
            if _NAME_RANK[name_src] < c["rank"]:    # keep the better human wording
                c["raw"], c["rank"] = raw, _NAME_RANK[name_src]
            if entity and not c["entity"]:
                c["entity"] = entity

        # partition rendered endpoints into writes (tasks) + selects (deferred by the supporting rule)
        writes, selects = [], []
        for ep in v.get("endpoints", []):
            verb, ent = _endpoint_verb_entity(ep.get("function", ""), ent_by_norm)
            if not verb:
                continue
            loc = (f'`{ep.get("control") or "?"}` → '
                   f'`{ep.get("connector") or "?"}.{ep.get("function") or ""}` [from rendered view]')
            (selects if verb == "SELECT" else writes).append((verb, ent, loc))

        # S1 — a wired WRITE is (almost) always a genuine user task. Its name is synthesized from
        # verb+entity (an affordance / action-column label, if the same (verb,entity) also has one,
        # outranks the synth); the page title is deliberately NOT used here — on a multi-write page
        # every write would otherwise collapse to the same title-derived name.
        for verb, ent, loc in writes:
            _add(verb, ent or sent, None, "synth", "high" if ent else "medium", [loc])

        # S3 — grids: a browse task + row-action tasks; corroborate/consume matching SELECTs
        consumed = set()
        for g in v.get("grids", []):
            gent = next((ent for (verb, ent, loc) in selects if ent), None) or sent
            corrob = [loc for (verb, ent, loc) in selects
                      if ent and _norm_entity(ent) == _norm_entity(gent)]
            consumed.update(corrob)
            ev = [f'grid `{g.get("name") or "?"}`'
                  + (" (searchable)" if g.get("searchable") else "") + " [from design model]"] + corrob
            _add("SELECT", gent, None, "synth", "high" if corrob else "medium", ev)
            for col in g.get("columns", []):
                if col.get("kind") != "action":
                    continue
                ht = col.get("header_text")
                cv = _canon_verb(ht) if isinstance(ht, str) else None
                if cv:
                    _add(cv, gent, ht, "action-col", "medium",
                         [f'action column "{ht}" on `{g.get("name") or "?"}` [from design model]'])

        # remaining SELECTs: a browse task only on a list/reporting/detail kind, else a supporting read
        for verb, ent, loc in selects:
            if loc in consumed:
                continue
            if kind in _BROWSE_KINDS:
                _add("SELECT", ent or sent, None, "synth", "medium" if ent else "low", [loc])
            else:
                supporting.append(loc)

        # S2 — verb-labelled affordances (the absorbed 0e signal)
        for control, label, verb, wired in v.get("affordances", []):
            cv = _canon_verb(label) or (verb.upper() if verb else None)
            noun = re.sub(rf"\b{re.escape(verb)}\b", "", label, flags=re.I) if verb else label
            ent = _resolve_entity(noun, ent_by_norm) or sent
            loc = f'affordance `{control}` "{label}" [from design model]'
            if wired:
                loc += f'; wired to `{wired[0]}`'
            _add(cv, ent, label, "affordance", "medium", [loc])

        # S4 — page-kind / title fallback, ONLY if nothing else derived a task
        if not cand:
            fv = _KIND_FALLBACK_VERB.get(kind)
            has_title = bool(title and title != "—")
            if fv and (sent or has_title):
                _add(fv, sent, title, "title", "low",
                     [f"kind `{kind}` `[AI-SUGGESTED]`",
                      (f'title "{title}" [from rendered routes]' if has_title
                       else "no wired op / grid / verb affordance")])

        tasks = [{"verb": c["verb"], "entity": c["entity"], "conf": c["conf"], "ev": c["ev"],
                  "name": _task_display_name(c["raw"], c["verb"], c["entity"])}
                 for c in cand.values()]
        tasks.sort(key=lambda t: (_VERB_SORT.get(t["verb"], 4), t["name"].lower()))
        notask = None
        if not tasks:
            notask = ("authentication / landing surface (no data operation)" if kind == "landing"
                      else "pure layout / container — no wired op, grid, or verb affordance")
        results.append({"name": name, "roles": v.get("roles", []),
                        "tasks": tasks, "supporting_reads": supporting, "notask": notask})
    return results

def emit_assets(model, out_dir, stem, kb_dir=None):
    os.makedirs(out_dir, exist_ok=True)
    written = []
    def W(category, body, extra=None):
        path = os.path.join(out_dir, f"{stem}.stadium.{category}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(_prov_header(model, category, extra))
            f.write(body.rstrip() + "\n")
        written.append(os.path.basename(path))

    app = model.get("application", {}) or {}
    pages = model.get("pages", []) or []
    connectors = model.get("connectors", []) or []
    scripts = model.get("scripts", []) or []
    security = model.get("security", {}) or {}
    appname = model.get("_app_name") or app.get("name") or "the application"

    # ---- reconcile the data model across SQL + stored-proc + web-service evidence (union by name).
    # `entities` is keyed by normalized name; each record carries display/sources/ops + per-field
    # provenance. `unclassified_procs` are stored procs whose name yielded no recognizable entity/op.
    entities, unclassified_procs = reconcile_entities(model)
    ents_sorted = sorted(entities.values(), key=lambda e: (e.get("display") or "").lower())

    # ======================================================================= Phase-0 shared structures
    # Joins over already-captured data, computed once and consumed by 0a–0h below. Script `owner` is
    # frequently None in the corpus, so the reliable surface attribution is: first dotted segment of
    # the script name → a page name, else that control's owner_page.
    all_controls = model.get("all_controls", []) or []
    page_names = {p.get("name") for p in pages if p.get("name")}
    ctrl_by_name = {}
    ctrl_owners = {}              # control name/raw_name → set of owner_pages (collision detection)
    for c in all_controls:
        for k in (c.get("raw_name"), c.get("name")):
            if k:
                ctrl_by_name.setdefault(k, c)
                ctrl_owners.setdefault(k, set()).add(c.get("owner_page"))

    def _script_surface(script_name):
        """Best-effort surface for a script (script `owner` is usually None). First dotted segment →
        a page name, else the owning page of a UNIQUELY-named control. A control name that spans
        several pages (SaveButton, CancelButton …) is ambiguous → None (never assert a wrong surface)."""
        seg = (script_name or "").split(".")[0]
        if seg in page_names:
            return seg
        owners = (ctrl_owners.get(seg) or set()) - {None}
        return next(iter(owners)) if len(owners) == 1 else None

    # control raw_name/name → scripts it fires (event-style names only; the reverse of the join above)
    scripts_by_ctrl = {}
    for s in scripts:
        nm = s.get("name") or ""
        if "." in nm:
            scripts_by_ctrl.setdefault(nm.split(".")[0], []).append(nm)

    # navigation edges + reachable-page set. A NavigateToPage Destination summarises as
    # "<Page> / <Param1> / <Param2>" — the page is the head before the first ' / ' (query params).
    def _nav_page(dest):
        if not dest:
            return None
        return str(dest).split(" / ")[0].strip() or None
    nav_edges = []
    for s in scripts:
        for a in s.get("actions", []):
            if "Navigate" in (a.get("action") or ""):
                dest = (a.get("summary") or {}).get("Destination")
                nav_edges.append((_script_surface(s.get("name")) or s.get("name"), dest))
    nav_dests = {_nav_page(d) for _, d in nav_edges}
    nav_dests.discard(None)

    # page inventory: union of design-model pages + admin-db pages (admin may hold admin-only pages)
    admin_pages = security.get("pages", []) or []
    start_by_name = {}
    for p in pages:
        if p.get("is_start_page") and p.get("name"):
            start_by_name[p["name"]] = True
    for ap in admin_pages:
        if ap.get("is_start_page") and ap.get("name"):
            start_by_name[ap["name"]] = True
    inv_order = [p.get("name") for p in pages if p.get("name")]
    for ap in admin_pages:
        if ap.get("name") and ap["name"] not in inv_order:
            inv_order.append(ap["name"])
    # Cluster C #7 — union the rendered route list (page-routes.js is the definitive page enumeration;
    # the `.sapz` walk is a floor). A route-declared page absent from the design + admin inventory is a
    # real page the `.sapz` nav walk could not reach — surfaced here, closing the orphan-page gap.
    route_by_name = {}
    for r in model.get("page_routes", []) or []:
        nm = _route_page_name(r)
        if nm:
            route_by_name.setdefault(nm, r)
            if nm not in inv_order:
                inv_order.append(nm)
    route_names = set(route_by_name)
    view_columns = model.get("view_columns") or {}      # Cluster C #8 — rendered grid columns + endpoints, keyed by view
    design_names = set(page_names)

    # 0e — per-surface action affordances: actionable controls whose label carries an action verb.
    def _walk_tree(nodes):
        for n in nodes or []:
            yield n
            yield from _walk_tree(n.get("children", []))
    affordances_by_page = {}      # page → [(control_name, label, verb, [wired script names])]
    for p in pages:
        rows_a = []
        for n in _walk_tree(p.get("control_tree", [])):
            if n.get("type") not in _ACTIONABLE_TYPES:
                continue
            label = _control_text(n.get("key_props") or {})
            if not label or _is_ui_chrome(label):
                continue
            verb = _label_verb(label)
            if not verb:
                continue
            wired = scripts_by_ctrl.get(n.get("raw_name")) or scripts_by_ctrl.get(n.get("name")) or []
            rows_a.append((n.get("name"), label, verb, wired))
        if rows_a:
            affordances_by_page[p.get("name")] = rows_a

    # 0a — notification points: raw-prop message text + decoded severity + dialog/toast. Deduped.
    notif_points, _seen_np = [], set()
    for s in scripts:
        for a in s.get("actions", []):
            act = a.get("action") or ""
            if act not in ("Notification", "DisplayMessageBox"):
                continue
            props = a.get("props") or {}
            kind = "dialog" if act == "DisplayMessageBox" else "toast"
            sev = _notif_severity(props.get("NotificationType")) if act == "Notification" else None
            msg = _notif_message(props) or (("⟨" + str((a.get("summary") or {}).get("Message")) + "⟩")
                                            if (a.get("summary") or {}).get("Message") else None)
            msg = _redact_pii(msg)
            surface = _script_surface(s.get("name"))
            key = (surface, s.get("name"), kind, sev, msg)
            if key in _seen_np:
                continue
            _seen_np.add(key)
            notif_points.append(key)

    # ======================================================================= overview
    L = [f"# Stadium app — {appname}\n",
         "## Tier-A — facts\n",
         f"- App name: **{appname}** [from design model]",
         f"- Designer version: {app.get('designer_version') or '—'} [from design model]",
         f"- Authentication: {security.get('authentication_type') or '—'} [from appsettings]",
         f"- Theme: {app.get('theme') or '—'} [from design model]",
         f"- Session timeout: {app.get('session_timeout') or '—'} min [from design model]",
         f"- Counts: {len(pages)} pages, {len(model.get('all_controls', []))} controls, "
         f"{len(connectors)} connectors, {len(scripts)} scripts, {len(security.get('roles', []))} roles [from design model]"]
    dep = model.get("deployment", {}) or {}
    L.append(f"- Deployment package: {dep.get('selected_package') or '—'} (of {dep.get('package_count') or '?'} deployments) [from administration.db]")
    dh = model.get("deploy_history", []) or []
    if dh:
        last = dh[-1]
        L.append(f"- Last published: {last.get('datetime')} (designer {last.get('designer_version')}) [from administration.db]")
    L.append("\n## Tier-B — inferred domain (advisory)")
    dom_hint = ", ".join([e["display"] for e in ents_sorted][:8]) or "—"
    L.append(f"- Candidate domain entities (from data operations): {dom_hint} `[AI-SUGGESTED: domain inference]`")
    L.append("\n## Gaps (not ascertainable from source)")
    for g in model.get("gaps", []) or []:
        L.append(f"- {g} `[AI-SUGGESTED: blocking]`")
    L.append("\n## Asset index")
    for cat in ("data-model", "data-sources", "business-rules", "access-control",
                "surfaces", "tasks", "navigation", "glossary", "design-signals", "modules",
                "task-flows", "quality-signals"):
        L.append(f"- `{stem}.stadium.{cat}.md`")
    W("overview", "\n".join(L))

    # ======================================================================= data-model
    # The rendered-types clause is added ONLY when types.js contributed shapes — so a pure-SQL app
    # (empty types.js) emits the identical intro it did before Cluster C (the #6 no-op guarantee).
    _dm_intro = ("> Entities + fields reconciled across SQL queries/views, stored procedures and web-service "
                 "calls (union by name). Every field carries a `[from …]` locator naming its exact source.")
    if model.get("rendered_types"):
        _dm_intro = ("> Entities + fields reconciled across SQL queries/views, stored procedures, web-service "
                     "calls and the rendered `types.js` FE↔API contract (union by name). Every field carries a "
                     "`[from …]` locator naming its exact source; `[from rendered types]` fields carry a per-field "
                     "authority (editable / read-only / action-input — Tier-B, read from the rendered variant).")
    L = [f"# Data model — {appname}\n", _dm_intro + "\n", "## Tier-A — entities & fields\n"]
    if ents_sorted:
        for e in ents_sorted:
            srcs = ", ".join(e["sources"]) or "—"
            ops = ", ".join(e["ops"]) or "—"
            L.append(f"### {e['display']}  ·  sources: {srcs}  ·  operations: {ops}")
            if e["fields"]:
                for fld in e["fields"]:
                    typ = fld.get("type")
                    loc = fld["locators"][0] if fld["locators"] else f"from connector: {(e['fns'] or ['?'])[0]}"
                    auth = fld.get("authority") or []            # Cluster C #6 — Tier-B field authority
                    atag = (" · editable" if "editable" in auth else
                            " · action-input" if "action" in auth else
                            " · read-only" if "display" in auth else "")
                    line = f"- `{e['display']}.{fld['path']}`" + (f" : {typ}" if typ else "") + atag + f" [{loc}]"
                    if len(fld["locators"]) > 1:
                        line += f"  _(+{len(fld['locators']) - 1} more)_"
                    L.append(line)
            else:
                L.append("- _(fields not modelled for this endpoint)_")
            for fld_name, elem in sorted((e.get("rel") or {}).items()):   # Cluster C #6 — nested-type relations (§2.2)
                L.append(f"  - relation: `{e['display']}.{fld_name}` → `{elem}[]` (nested type) [from rendered types]")
            if e["related"]:
                rel = ", ".join("`" + r + "`" for r in e["related"])
                L.append(f"> related shapes: {rel} (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`")
            L.append("")
    else:
        L.append("_No data operations found in the design model._\n")
    nstructs = len(model.get("data_dictionary", []) or [])
    if nstructs:
        L.append(f"> The design model defines {nstructs} internal data-type instances "
                 "(control/result/parameter bindings); field types above are sourced from them where concrete. "
                 "Full detail is in the forensic model.json.\n")
    # CRUD matrix (across all three evidence classes)
    L.append("## Tier-A — CRUD matrix\n")
    L.append("| Entity | SELECT | INSERT | UPDATE | DELETE | Evidence |")
    L.append("|---|:---:|:---:|:---:|:---:|---|")
    for e in ents_sorted:
        ops = set(e["ops"])
        def _m(v, ops=ops): return "✓" if v in ops else ""
        L.append(f"| {e['display']} | {_m('SELECT')} | {_m('INSERT')} | {_m('UPDATE')} | {_m('DELETE')} "
                 f"| {', '.join(e['sources'])} |")
    # unclassified stored procedures (name yielded no entity/op) — advisory only
    if unclassified_procs:
        L.append("\n## Tier-B — unclassified stored procedures (no recognized entity/op)")
        for pn in unclassified_procs[:40]:
            L.append(f"- `{pn}` `[AI-SUGGESTED]`")
        if len(unclassified_procs) > 40:
            L.append(f"- …and {len(unclassified_procs) - 40} more `[AI-SUGGESTED]`")
    # lifecycle (inferred)
    status_fields = sorted({fld["path"] for e in ents_sorted for fld in e["fields"]
                            if re.search(r"(?i)(status|state|stage|approv|archiv)", fld["path"])})
    if status_fields:
        L.append("\n## Tier-B — entity lifecycle / states (inferred)")
        L.append(f"- Status-like fields suggest stateful entities: {', '.join('`'+s+'`' for s in status_fields)} `[AI-SUGGESTED]`")
    W("data-model", "\n".join(L))

    # ======================================================================= data-sources
    L = [f"# Data sources — {appname}\n",
         "> **Internal data-source contract — handoff-only.** The SQL / stored procedures / API "
         "endpoints below name the client's internal databases and services. Treat as backend-contract "
         "material, not prototype design input (only the payload *field names* in `data-model` are §7 shapes).\n",
         "## Tier-A — connectors & operations\n"]
    if connectors:
        for c in connectors:
            L.append(f"### {c.get('name')} ({c.get('type') or 'connector'})")
            L.append(f"- Connection (redacted): `{_flat(c.get('connection_string'))[:300] or '—'}` [from administration.db / design model]")
            for f in c.get("functions", []):
                params = ", ".join(f"{p['name']}:{p.get('db_type') or p.get('type')}" for p in f.get("parameters", [])) or "none"
                L.append(f"- **{f.get('name')}** ({f.get('type')}) — params: {params} [from connector: {c.get('name')}]")
                q = _flat(f.get("query"))
                hint = f.get("shape_hint") or {}
                if f.get("type") == "WebServiceFunction":
                    method = _HTTP_VERB.get(hint.get("http_method")) or "?"
                    bits = []
                    if hint.get("body_name"):
                        bits.append(f"body: {hint['body_name']}")
                    if hint.get("resp_name"):
                        bits.append(f"response: {hint['resp_name']}")
                    tail = f" — {', '.join(bits)}" if bits else ""
                    L.append(f"  - endpoint: `{method} {hint.get('path') or ''}`{tail}")
                elif f.get("type") == "StoredProcedure" and q:
                    L.append(f"  - proc: `{q}`")
                elif q:
                    L.append("  ```sql\n  " + q[:1200] + "\n  ```")
            L.append("")
    else:
        L.append("_No connectors in the design model._\n")
    # --- app settings / integration signals (Cluster B #4-B) — non-secret `Setting` rows only.
    # Secrets are already reduced to a redacted presence signal at read time (`_redact_setting`).
    settings = model.get("settings") or []
    if settings:
        conn_blob = " ".join((_flat(c.get("connection_string")) or "") for c in (connectors or []))
        integ, creds = [], []
        for s in settings:
            k, nm, v = s.get("kind"), s.get("name"), s.get("value")
            if k == "credential":
                creds.append(nm)
            elif k == "endpoint":
                integ.append(f"- Internal API endpoint: `{_flat(v)[:200]}` [from design model: Setting]")
            elif k == "connection":
                if v and _flat(v) in conn_blob:            # dedupe vs the connector inventory above
                    continue
                integ.append(f"- Data connection configured: `{_flat(v)[:200]}` [from design model: Setting]")
            elif k == "path":
                integ.append(f"- Filesystem path referenced: `{_flat(v)[:200]}` [from design model: Setting]")
            else:                                          # scalar (e.g. DepartmentID)
                disp = _flat(v)
                if len(disp) > 100 or re.search(r"<[A-Za-z/!]", disp):   # UI markup / huge blob -> presence only
                    integ.append(f"- Config value present: `{nm}` (structured/large value, not shown) [from design model: Setting]")
                else:
                    integ.append(f"- Config value: `{nm}` = `{disp}` [from design model: Setting]")
        if integ or creds:
            L.append("## Tier-A — app settings / integration\n")
            L.extend(integ)
            if creds:
                L.append("- Integration credential(s) configured (redacted): "
                         + ", ".join(f"`{c}`" for c in creds) + " [from design model: Setting]")
            L.append("")
    W("data-sources", "\n".join(L))

    # ======================================================================= business-rules
    L = [f"# Business rules & behaviour — {appname}\n",
         "## Tier-A — event logic (scripts → action sequences)\n",
         "> Each script is classified by its **trigger** (0g): *user-initiated* (a control event — "
         "`.Click/.Change/…`), *automatic-on-open* (a page/template `.Load`), or *other* (a helper "
         "invoked via CallScript, or a timer/lifecycle hook). User-initiated scripts are rendered "
         "gesture-first; the *goal* a gesture serves is advisory (Tier-B), the gesture itself is fact.\n"]
    # 1c — group scripts by trigger; render branch-structured flow where the script branches, else the
    # lean flat per-action summary (linear scripts stay close to their Phase-0 rendering). A per-script
    # node budget caps the render of a huge handler with an explicit (+more) note.
    PER_SCRIPT_NODE_CAP = 50

    def _render_script(s, trig_class, event_tok, gesture):
        surface = _script_surface(s.get("name")) or s.get("owner") or "app"
        seq = " → ".join(a["action"] for a in s["actions"])
        L.append(f"#### {s['name']}  [from script, surface: {surface}]")
        L.append(f"- Trigger: **{trig_class}**" + (f"  (`.{event_tok}`)" if event_tok else ""))
        if trig_class == "user-initiated":
            seg = (s.get("name") or "").split(".")[0]
            c = ctrl_by_name.get(seg)
            label = _control_text(c.get("key_props") or {}) if c else None
            tgt = f' "{label}"' if label else (f' `{seg}`' if seg else "")
            L.append(f"- User {gesture or 'activates'}{tgt} → runs the flow below")
        L.append(f"- Sequence: {seq}")
        tree = s.get("tree") or []
        if _tree_has_decision(tree):     # 1c: branch-structured render for scripts with Decisions
            L.append("- Flow (branch-structured):")
            L.extend(_tree_md(tree, 1, [PER_SCRIPT_NODE_CAP]))
        else:                            # linear script: lean per-action summary bullets (back-compat)
            for a in s["actions"]:
                bits = _summary_bits(a.get("summary"))
                is_js = a.get("action") == "JavaScript"
                if not bits and not is_js:
                    continue
                tag = "  `[opaque: custom JS]`" if is_js else ""  # never silently drop opaque JS
                L.append(f"  - {a['action']}" + (f": {bits}" if bits else "") + tag)
        L.append("")

    def _grp_key(tc):
        return tc if tc in ("user-initiated", "automatic-on-open") else "other"
    triaged = [(s, *_script_trigger(s.get("name"))) for s in scripts if s.get("actions")]
    for gkey, gtitle in (("user-initiated", "User-initiated — gesture → outcome"),
                         ("automatic-on-open", "Automatic — on page / template open"),
                         ("other", "Other — helper scripts / timers / lifecycle")):
        grp = [t for t in triaged if _grp_key(t[1]) == gkey]
        if not grp:
            continue
        L.append(f"### {gtitle}\n")
        for s, tc, et, g in grp:
            _render_script(s, tc, et, g)
    # ---- 0a — notification points (verbatim message text + decoded severity + dialog/toast)
    L.append("## Tier-A — notification points\n")
    if notif_points:
        L.append("> Verbatim message text (expressions preserved), severity decoded from "
                 "`NotificationType` (1=success, 3=error, other=info), and dialog (blocking confirm) "
                 "vs toast. These target the **current operator** (not an actor signal — see access-control).\n")
        shown = 0
        for surface, sname, kind, sev, msg in notif_points:
            if shown >= 200:
                L.append(f"- _(+{len(notif_points) - shown} more notification points)_")
                break
            shown += 1
            sevtxt = f" · {sev}" if sev else ""
            msgtxt = f' — "{msg}"' if msg else ""
            L.append(f"- `{sname}` ({surface or 'app'}) · {kind}{sevtxt}{msgtxt} [from design model]")
    else:
        L.append("_No notification or dialog actions in the design model._")
    L.append("")
    # ---- 0f — validation (Cluster A #1): per-control rule + verbatim message + target + required.
    # Real validation lives in control props (the `Validator` table is empty in every corpus app), so
    # project each input control's IsValidRule/ErrorText/Required. Controls carrying a rule or a message
    # get an individual §6.3-shaped row; required-only fields collapse to one compact line. The rule
    # expression + message are Tier-A (verbatim); the intent label is a Tier-B `[AI-SUGGESTED]` reading.
    vals = model.get("validators", []) or []
    L.append("## Tier-A — validation\n")
    VALIDATION_ROW_CAP = 200
    rich_rows, req_only = _control_validation_rows(model.get("all_controls", []))
    # legacy design-model validators (empty across the corpus; retained for forward-compat)
    for v in vals:
        rule = _validator_rule(v.get("type"), v.get("props"))
        summ = v.get("summary") or {}
        msg = next((_redact_pii(summ[k].strip()) for k in ("Message", "ErrorMessage", "ValidationMessage", "Text")
                    if isinstance(summ.get(k), str) and summ[k].strip()), None)
        target = next((summ[k].strip() for k in ("ControlToValidate", "Target", "Control", "ValidatedControl")
                       if isinstance(summ.get(k), str) and summ[k].strip()
                       and not re.fullmatch(_GUID_RE, summ[k].strip())), None)
        if rule is None:
            rich_rows.append(f"- Validator: {v.get('name')} ({v.get('type')}) [from design model]")
        else:
            bits = [b for b in (target, rule, (f'"{msg}"' if msg else None)) if b]
            rich_rows.append("- " + " · ".join(bits) + " [from design model]")
    # dedupe identical rows — the same-named field validated identically on >1 page (e.g. add + edit)
    seen_v = set()
    rich_rows = [r for r in rich_rows if not (r in seen_v or seen_v.add(r))]
    for row in rich_rows[:VALIDATION_ROW_CAP]:
        L.append(row)
    if len(rich_rows) > VALIDATION_ROW_CAP:
        L.append(f"- _(+{len(rich_rows) - VALIDATION_ROW_CAP} more validation rules)_")
    if req_only:
        L.append("- Required inputs (from control `Required` flags): "
                 + ", ".join(f"`{n}`" for n in req_only[:40])
                 + (f" _(+{len(req_only) - 40} more)_" if len(req_only) > 40 else "")
                 + " [from design model]")
    if not rich_rows and not req_only:
        L.append("_No validators, required-field flags, or control validation rules in the design model._")
    # ---- 1d — edge / empty / error / loading states (facts Tier-A; the {loading|empty|error} label
    # is Tier-B — a hidden control is ambiguous). Cross-links 0a (notifications) + 0f (validators).
    _STATE_TGT = re.compile(r"(?i)spinner|loader|overlay|busy|visible|container")
    _EMPTY_NAME = re.compile(r"(?i)\b(empty|null|none|count|exists|any|zero)\b")
    _EMPTY_ZERO = re.compile(r"[=<>!]=?\s*0(\b|$)")
    err_notifs = [(sfc, sn, msg) for (sfc, sn, kind, sev, msg) in notif_points if sev == "error"]
    state_toggles, _seen_st = [], set()
    for s in scripts:
        sfc = _script_surface(s.get("name"))
        for a in s.get("actions", []):
            if a.get("action") != "SetValue":
                continue
            sm = a.get("summary") or {}
            tgt = sm.get("Target")
            if not isinstance(tgt, str) or not _STATE_TGT.search(tgt):
                continue
            val = sm.get("Value")
            key = (sfc, tgt, str(val))
            if key in _seen_st:
                continue
            _seen_st.add(key)
            state_toggles.append((sfc, s.get("name"), tgt, val))
    empty_guards, _seen_eg = [], set()
    for s in scripts:
        sfc = _script_surface(s.get("name"))
        for n in _iter_tree(s.get("tree")):
            if not n.get("decision"):
                continue
            for b in n.get("branches", []):
                p = b.get("predicate")
                if not p or not (_EMPTY_NAME.search(p) or _EMPTY_ZERO.search(p)):
                    continue
                key = (sfc, p)
                if key in _seen_eg:
                    continue
                _seen_eg.add(key)
                empty_guards.append((sfc, s.get("name"), p))
    L.append("\n## Tier-A — edge / empty / error / loading state signals\n")
    if err_notifs or state_toggles or empty_guards:
        L.append("> The toggle / error-type / guard predicate is Tier-A (provably in the model). The "
                 "**state classification** (loading vs empty vs error vs permission) is a Tier-B reading — "
                 "a hidden control is ambiguous (busy vs empty vs initial-hide). See 0a / 0f above.\n")
        for sfc, sn, msg in err_notifs[:80]:
            L.append(f"- **error notification** · `{sn}` ({sfc or 'app'}) — \"{msg}\" [from design model]")
        for sfc, sn, tgt, val in state_toggles[:120]:
            L.append(f"- **visibility/loading toggle** · `{sn}` ({sfc or 'app'}) — `{tgt}` = {val} "
                     f"[from design model] `[AI-SUGGESTED: state={_state_label(tgt, val)}]`")
        for sfc, sn, p in empty_guards[:120]:
            L.append(f"- **empty/edge guard** · `{sn}` ({sfc or 'app'}) — IF `{_redact_pii(p)}` "
                     "[from design model] `[AI-SUGGESTED: empty/count guard]`")
        extra = max(0, len(state_toggles) - 120) + max(0, len(empty_guards) - 120) + max(0, len(err_notifs) - 80)
        if extra:
            L.append(f"- _(+{extra} more state signals — see model.json)_")
    else:
        L.append("_No explicit spinner/visibility toggles, error notifications, or empty/null guards in the design model._")
    W("business-rules", "\n".join(L))

    # ======================================================================= access-control
    roles = security.get("roles", []) or []
    pagerole_rows = security.get("pagerole_count", 0) or 0
    pa = security.get("page_access", {}) or {}
    configured = len(roles) > 1 or pagerole_rows > 1
    L = [f"# Access control & actors — {appname}\n", "## Tier-A — roles & page access\n",
         f"- Authentication: {security.get('authentication_type') or '—'} [from appsettings]",
         f"- Roles: {', '.join(roles) or '—'} [from admin.db: Roles]"]
    if configured:
        # ---- 0d configured branch: real Page×Role matrix + counts + capability-split reading
        L.append(f"- **{len(roles)} role(s), {pagerole_rows} page grant(s) configured** [from admin.db: PageRole]\n")
        L += ["| Page | Roles with access |", "|---|---|"]
        for pg in sorted(pa):
            L.append(f"| {pg} | {', '.join(sorted(set(pa[pg]))) or '—'} |")
        L.append("\n## Tier-B — capability split (advisory)")
        for r in roles:
            L.append(f"- `{r}` → {_role_capability(r)} `[AI-SUGGESTED]`")
    else:
        # ---- 0d default single-operator branch: posture statement + full capability surface
        L.append("")
        L.append("## Tier-A — RBAC posture\n")
        L.append(f"- RBAC is effectively **unconfigured** in the deployed app — {len(roles) or 1} role "
                 f"(`{(roles or ['User'])[0]}`), {pagerole_rows} page grant (the start page), and the "
                 "operator holds the administrator flag (administrators bypass page-role checks). Actor "
                 "differentiation is **not modelled** in the app; persona differentiation must come from "
                 "stakeholder input. [from admin.db]")
        L.append("\n### Full capability surface (single operator)\n")
        L.append("> Every inventory page/task is available to the single operator:")
        for name in inv_order:
            L.append(f"- {name}")
        if not inv_order:
            L.append("- _(no pages found)_")
    # ---- 0d actor candidates (both branches): task-cluster split + external send-recipient signal
    cluster_pages = {}
    for pg, rows_a in affordances_by_page.items():
        for _cn, _lb, verb, _wr in rows_a:
            cl = _TASK_CLUSTER.get(verb)
            if cl:
                cluster_pages.setdefault(cl, set()).add(pg)
    for name in inv_order:                     # page-kind also contributes a cluster (0b → 0d)
        cl = _KIND_CLUSTER.get(_page_kind(name))
        if cl:
            cluster_pages.setdefault(cl, set()).add(name)
    present_clusters = sorted(cluster_pages)
    action_types = {a.get("action") for s in scripts for a in s.get("actions", [])}
    send_signals = sorted({at for at in action_types if at and re.search(r"(?i)mail|smtp|\bsend\b", at)})
    for c in connectors:
        if re.search(r"(?i)mail|smtp", (c.get("type") or "") + " " + (c.get("name") or "")):
            send_signals.append(f"connector:{c.get('name')}")
    L.append("\n## Tier-B — actor candidates (advisory; interpretive review gate)\n")
    if len(present_clusters) > 1:
        L.append("- Distinct task clusters — " + ", ".join(f"`{c}`" for c in present_clusters) +
                 " — suggest more than one operator role even under a single RBAC role (a capture "
                 "operator and an approver need not be the same person). `[AI-SUGGESTED]`")
    elif present_clusters:
        L.append(f"- A single task cluster (`{present_clusters[0]}`) is evident; the affordances imply "
                 "no multi-actor split. `[AI-SUGGESTED]`")
    else:
        L.append("- No action-verb affordances detected, so no task-cluster actor split can be read. `[AI-SUGGESTED]`")
    if send_signals:
        L.append("- External send/email action(s) present (" + ", ".join(f"`{s}`" for s in send_signals) +
                 ") → an external recipient exists (a second actor). The recipient **address is not "
                 "extracted** (PII); only its existence is surfaced. `[AI-SUGGESTED]`")
    L.append("> Toast/dialog notifications target the current operator only and are **not** an actor signal.")
    # ---- 0h grounded actor / persona scaffold (skeleton rendered; ungroundable fields left as gaps)
    notif_by_surface = {}
    for surface, _sn, kind, sev, msg in notif_points:
        notif_by_surface.setdefault(surface, []).append((kind, sev, msg))
    actors = []   # (label, clusters, surfaces)
    if configured:
        for r in roles:
            surfaces = sorted({pg for pg, rs in pa.items() if r in set(rs)})
            cls = sorted({_TASK_CLUSTER.get(v) for pg in surfaces
                          for (_c, _l, v, _w) in affordances_by_page.get(pg, []) if _TASK_CLUSTER.get(v)})
            actors.append((f"Role: {r}", cls, surfaces))
    else:
        letters = "ABCDEFGHIJ"
        for i, cl in enumerate(present_clusters):
            tag = letters[i] if i < len(letters) else str(i + 1)
            actors.append((f"Operator {tag} ({cl})", [cl], sorted(cluster_pages.get(cl, []))))
        if not actors:
            actors.append(("Operator A", [], list(inv_order)))
    L.append("\n## Tier-B — actor / persona scaffold (interpretive review gate)\n")
    L.append("> Grounded skeleton per candidate actor (task-clusters, surfaces, notifications). "
             "Persona fields the `.sapz` cannot ground are left as explicit gap prompts — authoring a "
             "name/goal/motivation here would fabricate. Skeleton rendered, flesh refused. `[AI-SUGGESTED]`\n")
    for label, cls, surfaces in actors:
        L.append(f"### Actor candidate: {label}  `[AI-SUGGESTED: actor candidate]`")
        L.append(f"- Task clusters: {', '.join(cls) or '—'}")
        L.append(f"- Surfaces touched: {', '.join(surfaces) or '—'}")
        nmsgs = [f'"{msg}" ({sev or kind})' for sfc in surfaces
                 for (kind, sev, msg) in notif_by_surface.get(sfc, []) if msg][:6]
        L.append(f"- Notifications sent/received: {'; '.join(nmsgs) if nmsgs else '—'}")
        for gap in ("name", "goal", "motivation", "pain-points", "success-metric"):
            L.append(f"- {gap}: `[AI-SUGGESTED: blocking]`")
        L.append("")
    # ---- user population (counts only; identities are PII and not extracted)
    L.append("## Tier-A — user population (counts only; identities not extracted)\n")
    L.append(f"- {security.get('user_count', 0)} user account(s), of which {security.get('admin_count', 0)} hold the administrator flag. Individual user identities (name / email) are intentionally **not** extracted — PII, and not needed for requirements; the roles + page-access matrix above is the actor model. [from admin.db: Users]")
    W("access-control", "\n".join(L))

    # ======================================================================= surfaces
    L = [f"# Surfaces (screens, controls, layout) — {appname}\n",
         "> Tier-A = which surfaces/controls/data exist (authoritative). "
         "Tier-B = layout & control-choice (advisory; the system holds design authority).\n"]
    # ---- 0b — view / task / feature inventory (union of design-model + administration.db pages)
    L.append("## View / task / feature inventory\n")
    L.append("> Columns Page / Title / Route / Start / Design-surface / Reachable / Route-declared are "
             "**Tier-A** facts (design model + administration.db + rendered `page-routes.js`). **Inferred "
             "kind** is **Tier-B** `[AI-SUGGESTED]` (name-suffix taxonomy; bare nouns → entity-maintenance). "
             "Title + Route come from the rendered router `[from rendered routes]`.\n")
    L.append("| Page | Title | Route | Start? | Design surface? | Reachable via nav? | Route-declared? | Inferred kind |")
    L.append("|---|---|---|:---:|:---:|:---:|:---:|---|")
    for name in inv_order:
        st = "✓" if start_by_name.get(name) else ""
        ds = "✓" if name in design_names else ""
        rc = "✓" if name in nav_dests else ""
        r = route_by_name.get(name) or {}
        title = _flat(r.get("title")) or (next((p.get("title") for p in pages if p.get("name") == name and p.get("title")), None)) or "—"
        route = r.get("path") or "—"
        rd = "✓" if name in route_names else ""
        L.append(f"| {name} | {title} | `{route}` | {st} | {ds} | {rc} | {rd} | {_page_kind(name)} `[AI-SUGGESTED]` |")
    if not inv_order:
        L.append("| _(no pages found)_ | | | | | | | |")
    L.append("")
    start = app.get("start_page_id")
    for p in pages:
        star = " ⭐ start" if p.get("is_start_page") else ""
        roles = ", ".join(p.get("roles", [])) or "—"
        L.append(f"## {p['name']}{star}  ·  title: {p.get('title') or '—'}  ·  roles: {roles}")
        def render(nodes, depth=1):
            for n in nodes:
                kp = n.get("key_props") or {}
                txt = _control_text(kp)
                txt = f' — "{txt}"' if txt else ""
                cons = _control_constraints(kp)          # Cluster A #1 — field behaviour, inline
                cons_txt = ("  ·  " + " · ".join(cons)) if cons else ""
                L.append("  " * depth + f"- {n['type']}: `{n['name']}`{txt}{cons_txt}")
                cols = n.get("columns")                  # Cluster A #2 — resolved DataGrid columns
                if cols:
                    L.append("  " * (depth + 1) + "- " + _columns_line(cols) + " [from design model]")
                    # Cluster C #8 — divergence-aware join: the `.sapz` #2 columns already carry
                    # label/visibility/clickability, so surface ONLY where the DEPLOYED rendered grid
                    # differs (resolved Expression header / mismatch / rendered-only col) — the DA#1
                    # deployed-vs-design staleness cross-check. Matched by (page → grid control name).
                    rgrid = ((view_columns.get(p.get("name")) or {}).get("grids") or {}).get(n.get("name"))
                    for note in _column_divergences(cols, rgrid):
                        L.append("  " * (depth + 2) + f"- ⚠ {note} [from rendered view]")
                render(n.get("children", []), depth + 1)
        render(p.get("control_tree", []))
        # Cluster C #8 — page→connector-function endpoints decoded from the rendered view (§8 existing-tool
        # reference). The `.sapz` renders these weakly; the rendered route strings bind UI action → backend.
        eps = (view_columns.get(p.get("name")) or {}).get("endpoints") or []
        if eps:
            L.append(f"\n### source-UI reference — {p['name']} (from rendered view)")
            L.append("> Backend operations the deployed page invokes (UI control → connector.function), "
                     "decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).")
            shown, seen_cf = 0, set()
            for ep in eps:
                cf = (ep.get("control"), ep.get("connector"), ep.get("function"))
                if cf in seen_cf:
                    continue
                seen_cf.add(cf)
                conn, fn = ep.get("connector") or "?", ep.get("function") or ""
                L.append(f"- `{ep.get('control') or '?'}` → `{conn}{('.' + fn) if fn else ''}`")
                shown += 1
                if shown >= 40:
                    L.append(f"- …and further endpoint bindings (truncated at 40) [from rendered view]")
                    break
        L.append("")
    # ---- 0e superseded: the per-view USER TASK inventory (verb-labelled affordances triangulated with
    # wired ops, grids and page-kinds, with a completeness guarantee) now lives in the `tasks` asset.
    L.append("## User tasks (per view)\n")
    L.append("> The per-view user-task inventory — the verb-labelled action affordances triangulated "
             "with wired backend operations, DataGrids and page-kinds, with a ≥1-task-per-view "
             "completeness guarantee — is emitted as its own asset: see `" + f"{stem}.stadium.tasks.md" + "`.\n")
    # screen<->entity bijection (heuristic)
    L.append("## Tier-A — screen ↔ entity (best-effort)\n")
    L.append("| Page | Likely entity |")
    L.append("|---|---|")
    for p in pages:
        guess = None
        pname = (p["name"] or "").lower()
        for e in ents_sorted:
            d = (e["display"] or "").lower()
            if d and (d in pname or pname in d):
                guess = e["display"]; break
        L.append(f"| {p['name']} | {guess or '—'} |")
    W("surfaces", "\n".join(L))

    # ======================================================================= tasks (per-view user tasks)
    # Deterministic per-view USER TASK inventory. Render-only over joins already materialized above
    # (endpoints, grids, affordances, kinds, roles, reconciled entities) — see `_derive_view_tasks`.
    def _screen_entity(pname):
        low = (pname or "").lower()
        for e in ents_sorted:
            d = (e.get("display") or "").lower()
            if d and (d in low or low in d):
                return e.get("display")
        return None
    ent_by_norm = {}
    for e in ents_sorted:
        ent_by_norm[e.get("norm") or _norm_entity(e.get("display") or "")] = e
    page_by_name = {p.get("name"): p for p in pages if p.get("name")}
    views = []
    for name in inv_order:
        p = page_by_name.get(name)
        r = route_by_name.get(name) or {}
        title = _flat(r.get("title")) or (p.get("title") if p else None) or "—"
        grids = []
        if p:
            for n in _walk_tree(p.get("control_tree", [])):
                if n.get("columns"):
                    grids.append({"name": n.get("name"),
                                  "searchable": bool((n.get("key_props") or {}).get("DisplaySearchBar")),
                                  "columns": n.get("columns") or []})
        roles = (p.get("roles") if p else None) or security.get("page_access", {}).get(name, []) or []
        views.append({"name": name, "title": title, "kind": _page_kind(name), "roles": roles,
                      "screen_entity": _screen_entity(name),
                      "endpoints": (view_columns.get(name) or {}).get("endpoints") or [],
                      "grids": grids,
                      "affordances": affordances_by_page.get(name) or []})
    view_tasks = _derive_view_tasks(views, ent_by_norm)

    L = [f"# User tasks — {appname}\n",
         "> One row per derivable USER TASK per view. Each task's EVIDENCE — the view, the wired "
         "control→op (`[from rendered view]`), the grid / action column (`[from design model]`), the "
         "title (`[from rendered routes]`) — is **Tier-A** (authoritative, `[SRC]`-citable via the inline "
         "locator). The task's verb / name is **Tier-B** `[AI-SUGGESTED]` (interpretation). Entities are "
         "drawn only from the reconciled set (see `data-model`) — never invented. Every view yields ≥1 "
         "row; a view with no derivable task says so explicitly. Confidence: high (wired op + resolved "
         "entity) / medium (labelled affordance, grid action, or op without entity) / low "
         "(page-kind/title fallback).\n",
         "## Task inventory\n",
         "| View | Task `[AI-SUGGESTED]` | Verb | Entity | Conf. | Evidence [from …] |",
         "|---|---|---|---|:--:|---|"]
    covered = 0
    for vt in view_tasks:
        if not vt["tasks"]:
            continue
        covered += 1
        for t in vt["tasks"]:
            L.append(f'| {vt["name"]} | {t["name"]} | {t["verb"]} | {t["entity"] or "—"} | '
                     f'{t["conf"]} | {"; ".join(t["ev"])} |')
    if covered == 0:
        L.append("| _(no views found)_ | | | | | |")
    L.append("")

    notes = []
    for vt in view_tasks:
        bits = []
        if vt["roles"]:
            bits.append("actor roles: " + ", ".join(vt["roles"]) + " [from admin.db: PageRole]")
        if vt["supporting_reads"]:
            bits.append("supporting reads (lookups / pre-fill, not tasks): " + "; ".join(vt["supporting_reads"]))
        if bits:
            notes.append(f"- **{vt['name']}** — " + " · ".join(bits))
    if notes:
        L.append("## Per-view notes\n")
        L += notes
        L.append("")

    notasks = [vt for vt in view_tasks if vt["notask"]]
    L.append("## Views with no derivable user task\n")
    if notasks:
        for vt in notasks:
            L.append(f"- `{vt['name']}` — {vt['notask']}")
    else:
        L.append("- _(none — every view yielded ≥1 task)_")
    L.append("\n## Coverage\n")
    L.append(f"- **{covered} / {len(view_tasks)}** views have ≥1 derived user task; "
             f"{len(notasks)} view(s) with no derivable task (listed above).")
    W("tasks", "\n".join(L))

    # ======================================================================= navigation
    L = [f"# Navigation & app shell — {appname}\n", "## Tier-A — templates (master pages)\n"]
    for t in model.get("templates", []) or []:
        L.append(f"- Template `{t['name']}`{' (default)' if t.get('is_default') else ''} [from design model]")
    L.append("\n## Tier-A — navigation edges (from NavigateToPage actions)\n")
    if nav_edges:
        for src, dst in nav_edges:
            L.append(f"- {src} → {dst or '?'}")
    else:
        L.append("_No explicit page-navigation actions found._")
    # ---- 0c — navigation reachability / orphans
    inv_set = list(dict.fromkeys(inv_order))
    reachable = [n for n in inv_set if n in nav_dests]
    orphans = [n for n in inv_set if n not in nav_dests]
    # Cluster C #7 — a page absent from the captured `.sapz` walk but DECLARED in page-routes.js is
    # reachable via a client route (the router is the definitive enumeration), NOT a true orphan. The
    # JS-computed-nav caveat narrows to pages absent from BOTH signals (should be ~none).
    route_reachable = [n for n in orphans if n in route_names]
    true_orphans = [n for n in orphans if n not in route_names]
    L.append("\n## Tier-A — navigation reachability\n")
    L.append(f"- Coverage: **{len(reachable)} of {len(inv_set)}** inventory pages are reachable via a "
             "captured `NavigateToPage` action. [from design model + administration.db]")
    if route_reachable:
        L.append(f"- Additionally reachable via a declared client route (not on the captured `.sapz` walk): "
                 + ", ".join(f"`{n}`" for n in route_reachable) + " [from rendered routes]")
    if true_orphans:
        starts = [n for n in true_orphans if start_by_name.get(n)]
        note = f" _(includes the start page `{starts[0]}`, the entry point)_" if starts else ""
        L.append("- Orphans (no inbound captured edge AND not route-declared): "
                 + ", ".join(f"`{n}`" for n in true_orphans) + note)
    L.append("\n## Tier-B — reachability caveat (advisory)")
    L.append("- Any remaining unreached page (absent from the captured `.sapz` walk AND from "
             "`page-routes.js`) is typically reached by JS-computed navigation (`jsGETCurrentURl` / "
             "custom JS) or is entry-only, so the captured nav graph is a floor, not the complete "
             "journey map. Route-declared pages above close most of this gap. `[AI-SUGGESTED]`")
    # ---- 1e — candidate cross-surface journeys (Tier-B; joins 0c edges + 0e/0g gesture + 0h actor).
    # Edges/gestures/states are Tier-A facts; the claim that a chain IS one end-to-end task is Tier-B.
    def _page_actor(page):
        cls = {_TASK_CLUSTER.get(v) for (_c, _l, v, _w) in affordances_by_page.get(page, [])}
        kc = _KIND_CLUSTER.get(_page_kind(page))
        if kc:
            cls.add(kc)
        picked = sorted(c for c in cls if c)
        return ", ".join(picked) if picked else _page_kind(page)

    journey_edges = []      # (src_page, dest_page, gesture, label)
    for s in scripts:
        _tc, _ev, gesture = _script_trigger(s.get("name"))
        src = _script_surface(s.get("name"))
        if not src or src not in inv_set:
            continue
        seg = (s.get("name") or "").split(".")[0]
        cobj = ctrl_by_name.get(seg)
        label = _control_text(cobj.get("key_props") or {}) if cobj else None
        for a in s.get("actions", []):
            if "Navigate" not in (a.get("action") or ""):
                continue
            dest = _nav_page((a.get("summary") or {}).get("Destination"))
            if dest and dest != src:
                journey_edges.append((src, dest, gesture, label))
    adj, edge_ann = {}, {}
    for src, dest, gesture, label in journey_edges:
        adj.setdefault(src, set()).add(dest)
        edge_ann.setdefault((src, dest), (gesture, label))
    dests_all = {d for ds in adj.values() for d in ds}
    roots = [p for p in adj if p not in dests_all] or list(adj)
    for st in [n for n in inv_set if start_by_name.get(n)]:
        if st in adj and st not in roots:
            roots.insert(0, st)
    journeys = []

    def _dfs(node, path, seen):
        nxts = [n for n in sorted(adj.get(node, [])) if n not in seen]
        if not nxts or len(path) >= 6:
            if len(path) >= 2:
                journeys.append(list(path))
            return
        for nxt in nxts:
            if len(journeys) >= 40:
                break
            _dfs(nxt, path + [nxt], seen | {nxt})
    for r in roots:
        if len(journeys) >= 40:
            break
        _dfs(r, [r], {r})
    # keep maximal, distinct journeys (drop a path that is a prefix of another)
    journeys.sort(key=len, reverse=True)
    uniq = []
    for p in journeys:
        key = " → ".join(p)
        if any(" → ".join(q).startswith(key) for q in uniq):
            continue
        uniq.append(p)
    L.append("\n## Tier-B — candidate cross-surface journeys (advisory; interpretive review gate)\n")
    L.append("> A journey joins nav edges (0c) with the affordance/gesture that triggers each hop "
             "(0e/0g) and the actor that performs it (0h). The **edges, gestures and page kinds are "
             "Tier-A facts**; the claim that a chain **is one** end-to-end task is a **Tier-B** reading. "
             "JS-computed nav gaps are shown as explicit breaks, never bridged. `[AI-SUGGESTED]`\n")
    if uniq:
        for path in uniq[:12]:
            parts = []
            for i, node in enumerate(path):
                parts.append(f"`{node}` _({_page_actor(node)})_")
                if i < len(path) - 1:
                    g, lbl = edge_ann.get((node, path[i + 1]), (None, None))
                    via = f'{g or "navigates"} "{lbl}"' if lbl else (g or "navigates")
                    parts.append(f" —[{via}]→ ")
            L.append("- " + "".join(parts))
        gap_pages = [n for n in orphans if affordances_by_page.get(n)]
        if gap_pages:
            L.append("- **JS-nav gaps** — interactive pages with no captured inbound edge (reached via "
                     "JS-computed nav): " + ", ".join(f"`{n}`" for n in gap_pages[:20]) + " `[gap: JS-computed nav]`")
    elif affordances_by_page:
        L.append("_No captured cross-surface nav — per-surface mini-flows (no cross-surface link invented):_\n")
        for p in pages:
            rows_a = affordances_by_page.get(p.get("name"))
            if not rows_a:
                continue
            acts = ", ".join(f'{v} ("{lbl}")' for (_c, lbl, v, _w) in rows_a[:8])
            L.append(f"- `{p['name']}` _({_page_actor(p['name'])})_: {acts}")
    else:
        L.append("_No navigation affordances from which to derive journeys._")
    # affordances
    types = model.get("control_type_counts", {}) or {}
    affordances = []
    if types.get("DataGrid"):
        affordances.append("data grids (search/sort/export likely)")
    action_types = {a["action"] for s in scripts for a in s.get("actions", [])}
    if "DownloadFile" in action_types: affordances.append("file download/export")
    if "Notification" in action_types: affordances.append("toast notifications")
    if "DisplayMessageBox" in action_types: affordances.append("confirmation dialogs")
    L.append("\n## Tier-B — affordances (advisory)")
    L.append("- " + ("; ".join(affordances) if affordances else "none detected"))
    W("navigation", "\n".join(L))

    # ======================================================================= glossary
    terms = {}
    for c in model.get("all_controls", []) or []:
        t = _control_text(c.get("key_props") or {})
        if t and 1 < len(t) <= 60:
            terms[t] = terms.get(t, 0) + 1
    for p in pages:
        if p.get("title"):
            terms[p["title"]] = terms.get(p["title"], 0) + 1
    L = [f"# Key terms (from page content) — {appname}\n",
         "## Tier-A — visible terms (verbatim from labels, headings, buttons, titles)\n"]
    for t in sorted(terms):
        L.append(f"- {t}")
    W("glossary", "\n".join(L))

    # ======================================================================= embedded brand assets (copy + logo id)
    # Advisory brand chrome (icons + product logo). Excluded from every input pipeline's manifest
    # by IX-04 in framework/shared/input-exclusions.md; the identified logo is surfaced into
    # prototypes at scaffold time (framework/skills/extract-brand-theme.md) via the design-signals pointer.
    fa = model.get("frontend_assets", {}) or {}
    _IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico")
    emb_dir = os.path.join(out_dir, "embedded")
    copied = []
    for p in (fa.get("embedded_files") or [])[:60]:
        try:
            if (os.path.isfile(p) and os.path.splitext(p)[1].lower() in _IMG_EXT
                    and os.path.getsize(p) <= 2_000_000):
                os.makedirs(emb_dir, exist_ok=True)
                shutil.copy2(p, os.path.join(emb_dir, os.path.basename(p)))
                copied.append(os.path.basename(p))
        except Exception:
            pass
    # Identify the product logo deterministically: basename contains "logo" (case-insensitive);
    # if several match, the largest. No match -> no logo (do not guess from arbitrary icons).
    logo_file = None
    _logo_named = [b for b in copied if "logo" in b.lower()]
    if _logo_named:
        logo_file = max(_logo_named, key=lambda b: os.path.getsize(os.path.join(emb_dir, b)))
    # Favicon: prefer a copied .ico, else reuse the logo.
    _icos = [b for b in copied if b.lower().endswith(".ico")]
    favicon_file = _icos[0] if _icos else logo_file

    # ======================================================================= design-signals
    styling = model.get("styling", {}) or {}
    mods = model.get("modules", {}) or {}
    css = mods.get("embedded_css", [])
    if not css:
        classification = "plain / standard (stock theme, no custom CSS)"
    elif css == ["theming-variables.css"]:
        classification = "built-in theming-kit (theming-variables.css)"
    else:
        classification = "extensively customized (custom component CSS)"
    L = [f"# Design signals (advisory — for /design-system) — {appname}\n",
         "> Entirely Tier-B / advisory. Stock theme folders are identical boilerplate across apps — ignore them.\n",
         "## Signals\n",
         f"- Theme: **{styling.get('theme') or '—'}**",
         f"- Styling classification: **{classification}**",
         f"- Custom embedded CSS: {', '.join(css) or 'none'}",
         f"- App-level custom stylesheet: {'present' if styling.get('app_stylesheet') else 'none'}",
         f"- Fonts present: {', '.join(fa.get('fonts', [])) or '—'}",
         f"- Available (stock) themes: {', '.join(fa.get('available_themes', [])) or '—'} _(boilerplate)_",
         f"- Product logo: {('embedded/' + logo_file) if logo_file else 'none identified'} _(advisory; surfaced into prototypes at scaffold time)_"]
    W("design-signals", "\n".join(L), extra={
        "logo": (f"embedded/{logo_file}" if logo_file else "null"),
        "favicon": (f"embedded/{favicon_file}" if favicon_file else "null"),
    })

    # ======================================================================= modules
    _SRC_LABEL = {"url": "comment-URL", "fn": "function-name", "css": "CSS footprint"}
    L = [f"# Custom JS / modules — {appname}\n", "## Tier-A — detected modules\n"]
    if mods.get("detected"):
        for m in mods["detected"]:
            src = _SRC_LABEL.get(m.get("detection_source"), m.get("detection_source") or "?")
            L.append(f"- **{m['module']}** — {m.get('gloss') or '(no KB gloss)'} — {m['repo']} [detected via: {src}]")
    else:
        L.append("_No stadium-software modules detected (comment-URL, function-name, or CSS footprint)._")
    if mods.get("behaviours"):
        L.append("\n## Tier-A — module-driven behaviours\n")
        for b in mods["behaviours"]:
            L.append(f"- {b} [from global-scripts]")
    L.append(f"\n- global-scripts.js present: {mods.get('global_scripts_present')}")
    L.append(f"- Module CSS footprint: {', '.join(mods.get('embedded_css', [])) or 'none'}")
    L.append("\n## Tier-B — implication (advisory)")
    L.append("- Detected modules indicate behaviour beyond standard CRUD controls (must be captured as required interactions). `[AI-SUGGESTED]`")
    W("modules", "\n".join(L))

    return written

# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Extract a Twenty57 Stadium app into a structured facts bundle.")
    ap.add_argument("app_folder", help="Path to the Stadium application folder")
    ap.add_argument("--out", default=None, help="Output directory (default: ./analysis-output/<WebAppName>/)")
    ap.add_argument("--emit-assets", default=None, help="Emit lean per-category requirement assets into this dir (LLM-facing)")
    ap.add_argument("--stem", default=None, help="Filename stem for emitted assets (default: sanitized app name)")
    ap.add_argument("--kb", default=None, help="Path to the Stadium knowledge-base dir (module glosses, thresholds)")
    ap.add_argument("--model-out", default=None, help="Write the full forensic model.json to this path (asset mode only)")
    args = ap.parse_args()

    app_dir = os.path.abspath(args.app_folder)
    if not os.path.isdir(app_dir):
        print(f"ERROR: not a folder: {app_dir}", file=sys.stderr); sys.exit(2)

    cfg = read_config(app_dir)
    admin = read_admin_db(app_dir)
    stack = read_stack(app_dir)
    assets = read_frontend_assets(app_dir)

    workdir = tempfile.mkdtemp(prefix="stadium-extract-")
    try:
        sqlitedata, deploy_meta = select_design_model(app_dir, workdir)
        if sqlitedata:
            model = read_design_model(sqlitedata)
        else:
            model = {"application": {}, "pages": [], "templates": [], "connectors": [],
                     "scripts": [], "styling": {}, "_note": "No design model (.sapz) available; facts limited to admin db + source."}

        # Merge security from admin db into model + attach page roles
        model["security"] = {
            "authentication_type": cfg.get("AuthenticationType"),
            "roles": admin.get("roles", []),
            "page_access": admin.get("page_access", {}),
            "pages": admin.get("pages", []),
            "pagerole_count": admin.get("pagerole_count", 0),
            "user_count": admin.get("user_count", 0),
            "admin_count": admin.get("admin_count", 0),
        }
        for p in model.get("pages", []):
            p["roles"] = admin.get("page_access", {}).get(p["name"], [])

        model["config"] = cfg
        model["tech_stack"] = stack
        model["frontend_assets"] = {k: v for k, v in assets.items()}
        model["deployment"] = deploy_meta
        model["deploy_history"] = admin.get("deploy_history", [])
        model["audit_log"] = admin.get("audit_log", [])
        model["gaps"] = detect_gaps(model, admin, cfg, assets)
        model["_extracted_from"] = app_dir

        model["_app_name"] = admin.get("app_name") or model.get("application", {}).get("name") or cfg.get("WebAppName")
        model["_file_guid"] = admin.get("file_guid") or os.path.basename(app_dir)
        model["modules"] = read_modules(app_dir, args.kb)
        model["page_routes"] = read_page_routes(app_dir)          # Cluster C #7 — complete titled page list
        model["rendered_types"] = read_client_types(app_dir)       # Cluster C #6 — FE↔API contract shapes
        model["view_columns"] = read_view_columns(app_dir)         # Cluster C #8 — rendered grid labels + endpoints

        name = (model.get("application", {}).get("name") or admin.get("app_name")
                or cfg.get("WebAppName") or os.path.basename(app_dir))

        if args.emit_assets:
            os.makedirs(args.emit_assets, exist_ok=True)
            stem = args.stem or re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_") or "stadium-app"
            written = emit_assets(model, args.emit_assets, stem, args.kb)
            if args.model_out:
                md_dir = os.path.dirname(os.path.abspath(args.model_out))
                os.makedirs(md_dir, exist_ok=True)
                with open(args.model_out, "w", encoding="utf-8") as f:
                    json.dump(model, f, indent=2, ensure_ascii=False, default=str)
            print(f"App: {name}")
            print(f"Assets ({len(written)}) -> {args.emit_assets}")
            for w in written:
                print(f"  - {w}")
            if args.model_out:
                print(f"Model: {args.model_out}")
        else:
            out_dir = args.out or os.path.join(os.getcwd(), "analysis-output", name)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "model.json"), "w", encoding="utf-8") as f:
                json.dump(model, f, indent=2, ensure_ascii=False, default=str)
            write_inventory_md(model, admin, cfg, stack, assets, deploy_meta, os.path.join(out_dir, "inventory.md"))
            print(f"App: {name}")
            print(f"Pages: {len(model.get('pages', []))}  Controls: {sum(1 for _ in iter_controls(model))}  "
                  f"Connectors: {len(model.get('connectors', []))}  Scripts: {len(model.get('scripts', []))}")
            print(f"Roles: {', '.join(model['security']['roles']) or '—'}")
            print(f"Output: {out_dir}")
            print(f"  - model.json")
            print(f"  - inventory.md")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

def iter_controls(model):
    def walk(nodes):
        for n in nodes:
            yield n
            yield from walk(n.get("children", []))
    for p in model.get("pages", []):
        yield from walk(p.get("control_tree", []))
    for t in model.get("templates", []):
        yield from walk(t.get("control_tree", []))

if __name__ == "__main__":
    main()
