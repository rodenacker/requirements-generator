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
                      "HeaderText", "Required", "Enabled", "Columns")

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
            conn["functions"].append({
                "name": f["name"],
                "type": f["type"],
                "query": fprops.get("Text") or fprops.get("Query") or fprops.get("CommandText"),
                "timeout": fprops.get("Timeout"),
                "parameters": params,
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
        })
    model["scripts"] = scripts

    # ----- Session variables, custom types, validators
    model["session_variables"] = [{"name": e["name"], "props": e["props"]} for e in sessvars_e]
    model["custom_types"] = [{"name": e["name"], "props": e["props"]} for e in customtypes_e]
    model["validators"] = [{"name": e["name"], "type": e["type"], "props": e["props"]} for e in validators_e]

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

    con.close()
    return model

# --------------------------------------------------------------------------- admin db (security)

def read_admin_db(app_dir):
    out = {"roles": [], "page_access": {}, "user_count": 0, "admin_count": 0, "connections": [], "deploy_history": [], "audit_log": []}
    admin = os.path.join(app_dir, "administration.db")
    if not os.path.exists(admin):
        return out
    try:
        c = sqlite3.connect(admin); c.row_factory = sqlite3.Row
        pages = {str(r["Id"]): r["Name"] for r in c.execute("SELECT Id,Name FROM Pages")}
        roles = {str(r["Id"]): r["Name"] for r in c.execute("SELECT Id,Name FROM Roles")}
        out["roles"] = sorted(roles.values())
        for r in c.execute("SELECT PageId,RoleId FROM PageRole"):
            pg = pages.get(str(r["PageId"]), str(r["PageId"]))
            out["page_access"].setdefault(pg, []).append(roles.get(str(r["RoleId"]), str(r["RoleId"])))
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
    if not model.get("validators"):
        gaps.append("No validators defined in the design model; intended validation rules & messages (if any) are unknown.")
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

def read_modules(app_dir, kb_dir=None):
    """Detect stadium-software modules / custom vanilla JS from the generated source."""
    out = {"global_scripts_present": False, "embedded_css": [], "detected": []}
    gs = os.path.join(app_dir, "ClientApp", "src", "global-scripts.js")
    names = set()
    if os.path.exists(gs):
        out["global_scripts_present"] = True
        try:
            txt = open(gs, encoding="utf-8", errors="ignore").read()
            for u in re.findall(r"github\.com/stadium-software/([A-Za-z0-9._-]+)", txt):
                names.add(u.strip().rstrip("/.").lower())
        except Exception:
            pass
    ef = os.path.join(app_dir, "wwwroot", "Content", "EmbeddedFiles", "CSS")
    if os.path.isdir(ef):
        out["embedded_css"] = sorted(f for f in os.listdir(ef) if f.lower().endswith(".css"))
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
    for n in sorted(names):
        out["detected"].append({"module": n, "repo": f"https://github.com/stadium-software/{n}", "gloss": gloss.get(n)})
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
    return {"verb": verb, "tables": tables, "primary": primary, "columns": [c for c in cols if c][:50]}

def _prov_header(model, category):
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
         "marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.",
         "---", ""]
    return "\n".join(L)

def emit_assets(model, out_dir, stem, kb_dir=None):
    os.makedirs(out_dir, exist_ok=True)
    written = []
    def W(category, body):
        path = os.path.join(out_dir, f"{stem}.stadium.{category}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(_prov_header(model, category))
            f.write(body.rstrip() + "\n")
        written.append(os.path.basename(path))

    app = model.get("application", {}) or {}
    pages = model.get("pages", []) or []
    connectors = model.get("connectors", []) or []
    scripts = model.get("scripts", []) or []
    security = model.get("security", {}) or {}
    appname = model.get("_app_name") or app.get("name") or "the application"

    # ---- precompute entity / CRUD map from connector SQL (columns attributed to the PRIMARY table only)
    entities = {}   # table -> {columns:[], col_types:{}, ops:set, fns:[]}
    for c in connectors:
        for f in c.get("functions", []):
            shape = _sql_shape(f.get("query"))
            f["_shape"] = shape
            if not shape:
                continue
            for t in shape["tables"]:
                entities.setdefault(t, {"columns": [], "col_types": {}, "ops": set(), "fns": []})
            prim = shape.get("primary")
            if not prim:
                continue
            ent = entities.setdefault(prim, {"columns": [], "col_types": {}, "ops": set(), "fns": []})
            if shape["verb"]:
                ent["ops"].add(shape["verb"])
            ent["fns"].append(f.get("name"))
            ptypes = {p.get("name"): (p.get("db_type") or p.get("type")) for p in f.get("parameters", [])}
            for col in shape["columns"]:
                if col not in ent["columns"]:
                    ent["columns"].append(col)
                if col in ptypes and ptypes[col] and col not in ent["col_types"]:
                    ent["col_types"][col] = ptypes[col]

    # enrich column types from the design-model data dictionary (concrete types beat SQL's String params)
    type_by_field = {}
    for d in model.get("data_dictionary", []) or []:
        for fl in d.get("fields", []):
            nm, ty = fl.get("name"), fl.get("type")
            if nm and ty and ty != "Object" and nm not in type_by_field:
                type_by_field[nm] = ty
    for ent in entities.values():
        for col in ent["columns"]:
            if col in type_by_field:   # design-model type is more accurate than SQL's uniform String params
                ent["col_types"][col] = type_by_field[col]

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
    dom_hint = ", ".join(sorted(entities.keys())[:8]) or "—"
    L.append(f"- Candidate domain entities (from data operations): {dom_hint} `[AI-SUGGESTED: domain inference]`")
    L.append("\n## Gaps (not ascertainable from source)")
    for g in model.get("gaps", []) or []:
        L.append(f"- {g} `[AI-SUGGESTED: blocking]`")
    L.append("\n## Asset index")
    for cat in ("data-model", "data-sources", "business-rules", "access-control",
                "surfaces", "navigation", "glossary", "design-signals", "modules",
                "task-flows", "quality-signals"):
        L.append(f"- `{stem}.stadium.{cat}.md`")
    W("overview", "\n".join(L))

    # ======================================================================= data-model
    L = [f"# Data model — {appname}\n", "## Tier-A — entities & fields\n"]
    if entities:
        for t in sorted(entities):
            ent = entities[t]
            ops = ", ".join(sorted(ent["ops"])) or "—"
            L.append(f"### {t}  ·  operations: {ops}")
            if ent["columns"]:
                fn0 = ent["fns"][0] if ent["fns"] else "?"
                for col in ent["columns"]:
                    typ = ent["col_types"].get(col)
                    L.append(f"- `{t}.{col}`" + (f" : {typ}" if typ else "") + f" [from connector: {fn0}]")
            else:
                L.append("- _(columns not parseable from SQL)_")
            L.append("")
    else:
        L.append("_No SQL-derived entities found._\n")
    nstructs = len(model.get("data_dictionary", []) or [])
    if nstructs:
        L.append(f"> The design model also defines {nstructs} internal data-type instances "
                 "(control/result bindings); the field types above are sourced from them. "
                 "Full detail is in the forensic model.json.\n")
    # CRUD matrix
    L.append("## Tier-A — CRUD matrix\n")
    L.append("| Entity | SELECT | INSERT | UPDATE | DELETE |")
    L.append("|---|:---:|:---:|:---:|:---:|")
    for t in sorted(entities):
        ops = entities[t]["ops"]
        def _m(v): return "✓" if v in ops else ""
        L.append(f"| {t} | {_m('SELECT')} | {_m('INSERT')} | {_m('UPDATE')} | {_m('DELETE')} |")
    # lifecycle (inferred)
    status_fields = sorted({c for ent in entities.values() for c in ent["columns"]
                            if re.search(r"(?i)(status|state|stage|approv|archiv)", c)})
    if status_fields:
        L.append("\n## Tier-B — entity lifecycle / states (inferred)")
        L.append(f"- Status-like fields suggest stateful entities: {', '.join('`'+s+'`' for s in status_fields)} `[AI-SUGGESTED]`")
    W("data-model", "\n".join(L))

    # ======================================================================= data-sources
    L = [f"# Data sources — {appname}\n",
         "> **Internal data-source contract — handoff-only.** The SQL below names the client's "
         "internal databases/tables/columns. Treat as backend-contract material, not prototype design input.\n",
         "## Tier-A — connectors & operations\n"]
    if connectors:
        for c in connectors:
            L.append(f"### {c.get('name')} ({c.get('type') or 'connector'})")
            L.append(f"- Connection (redacted): `{_flat(c.get('connection_string'))[:300] or '—'}` [from administration.db / design model]")
            for f in c.get("functions", []):
                params = ", ".join(f"{p['name']}:{p.get('db_type') or p.get('type')}" for p in f.get("parameters", [])) or "none"
                L.append(f"- **{f.get('name')}** ({f.get('type')}) — params: {params} [from connector: {c.get('name')}]")
                q = _flat(f.get("query"))
                if q:
                    L.append("  ```sql\n  " + q[:1200] + "\n  ```")
            L.append("")
    else:
        L.append("_No connectors in the design model._\n")
    W("data-sources", "\n".join(L))

    # ======================================================================= business-rules
    L = [f"# Business rules & behaviour — {appname}\n", "## Tier-A — event logic (scripts → action sequences)\n"]
    for s in scripts:
        if not s.get("actions"):
            continue
        owner = s.get("owner") or "app"
        seq = " → ".join(a["action"] for a in s["actions"])
        L.append(f"### {s['name']}  [from script, owner: {owner}]")
        L.append(f"- Sequence: {seq}")
        for a in s["actions"]:
            sm = a.get("summary") or {}
            bits = []
            for k in ("ConnectorFunction", "Target", "Destination", "ScriptToCall", "Message", "Title", "Condition", "Value", "List", "Url"):
                if k in sm:
                    bits.append(f"{k}={sm[k]}")
            if bits:
                L.append(f"  - {a['action']}: " + "; ".join(bits))
        L.append("")
    # validation
    vals = model.get("validators", []) or []
    seen_req = []
    for c in model.get("all_controls", []) or []:
        if (c.get("key_props") or {}).get("Required") and c.get("name") and c["name"] not in seen_req:
            seen_req.append(c["name"])
    L.append("## Tier-A — validation\n")
    if vals:
        for v in vals:
            L.append(f"- Validator: {v.get('name')} ({v.get('type')}) [from design model]")
    if seen_req:
        L.append("- Required inputs: " + ", ".join(f"`{n}`" for n in seen_req[:40]) + " [from design model]")
    if not vals and not seen_req:
        L.append("_No explicit validators or required-field flags in the design model._ `[AI-SUGGESTED: blocking]`")
    W("business-rules", "\n".join(L))

    # ======================================================================= access-control
    L = [f"# Access control & actors — {appname}\n", "## Tier-A — roles & page access\n",
         f"- Authentication: {security.get('authentication_type') or '—'} [from appsettings]",
         f"- Roles: {', '.join(security.get('roles', [])) or '—'} [from admin.db: Roles]\n",
         "| Page | Roles with access |", "|---|---|"]
    pa = security.get("page_access", {}) or {}
    for pg in sorted(pa):
        L.append(f"| {pg} | {', '.join(sorted(set(pa[pg]))) or '—'} |")
    L.append("\n## Tier-A — user population (counts only; identities not extracted)\n")
    L.append(f"- {security.get('user_count', 0)} user account(s), of which {security.get('admin_count', 0)} hold the administrator flag. Individual user identities (name / email) are intentionally **not** extracted — PII, and not needed for requirements; the roles + page-access matrix above is the actor model. [from admin.db: Users]")
    W("access-control", "\n".join(L))

    # ======================================================================= surfaces
    L = [f"# Surfaces (screens, controls, layout) — {appname}\n",
         "> Tier-A = which surfaces/controls/data exist (authoritative). "
         "Tier-B = layout & control-choice (advisory; the system holds design authority).\n"]
    start = app.get("start_page_id")
    for p in pages:
        star = " ⭐ start" if p.get("is_start_page") else ""
        roles = ", ".join(p.get("roles", [])) or "—"
        L.append(f"## {p['name']}{star}  ·  title: {p.get('title') or '—'}  ·  roles: {roles}")
        def render(nodes, depth=1):
            for n in nodes:
                txt = _control_text(n.get("key_props") or {})
                txt = f' — "{txt}"' if txt else ""
                L.append("  " * depth + f"- {n['type']}: `{n['name']}`{txt}")
                render(n.get("children", []), depth + 1)
        render(p.get("control_tree", []))
        L.append("")
    # screen<->entity bijection (heuristic)
    L.append("## Tier-A — screen ↔ entity (best-effort)\n")
    L.append("| Page | Likely entity |")
    L.append("|---|---|")
    for p in pages:
        guess = None
        pname = (p["name"] or "").lower()
        for t in entities:
            if t.lower() in pname or pname in t.lower():
                guess = t; break
        L.append(f"| {p['name']} | {guess or '—'} |")
    W("surfaces", "\n".join(L))

    # ======================================================================= navigation
    L = [f"# Navigation & app shell — {appname}\n", "## Tier-A — templates (master pages)\n"]
    for t in model.get("templates", []) or []:
        L.append(f"- Template `{t['name']}`{' (default)' if t.get('is_default') else ''} [from design model]")
    L.append("\n## Tier-A — navigation edges (from NavigateToPage actions)\n")
    edges = []
    for s in scripts:
        for a in s.get("actions", []):
            if "Navigate" in (a.get("action") or ""):
                dest = (a.get("summary") or {}).get("Destination") or "?"
                edges.append((s.get("owner") or s.get("name"), dest))
    for src, dst in edges:
        L.append(f"- {src} → {dst}")
    if not edges:
        L.append("_No explicit page-navigation actions found._")
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

    # ======================================================================= design-signals
    styling = model.get("styling", {}) or {}
    fa = model.get("frontend_assets", {}) or {}
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
         f"- Available (stock) themes: {', '.join(fa.get('available_themes', [])) or '—'} _(boilerplate)_"]
    W("design-signals", "\n".join(L))

    # ======================================================================= modules
    L = [f"# Custom JS / modules — {appname}\n", "## Tier-A — detected modules\n"]
    if mods.get("detected"):
        for m in mods["detected"]:
            L.append(f"- **{m['module']}** — {m.get('gloss') or '(no KB gloss)'} — {m['repo']}")
    else:
        L.append("_No stadium-software module references detected in global-scripts.js._")
    L.append(f"\n- global-scripts.js present: {mods.get('global_scripts_present')}")
    L.append(f"- Module CSS footprint: {', '.join(mods.get('embedded_css', [])) or 'none'}")
    L.append("\n## Tier-B — implication (advisory)")
    L.append("- Detected modules indicate behaviour beyond standard CRUD controls (must be captured as required interactions). `[AI-SUGGESTED]`")
    W("modules", "\n".join(L))

    # ======================================================================= embedded brand assets
    copied = []
    for p in (fa.get("embedded_files") or [])[:60]:
        try:
            if (os.path.isfile(p) and os.path.splitext(p)[1].lower() in
                    (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico")
                    and os.path.getsize(p) <= 2_000_000):
                emb_dir = os.path.join(out_dir, "embedded")
                os.makedirs(emb_dir, exist_ok=True)
                shutil.copy2(p, os.path.join(emb_dir, os.path.basename(p)))
                copied.append(os.path.basename(p))
        except Exception:
            pass

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
