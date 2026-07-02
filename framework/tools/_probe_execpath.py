#!/usr/bin/env python3
"""
_probe_execpath.py  --  Phase-1 golden-fixture prerequisite probe (behaviour enrichment).

Independently re-verifies the source-model shapes the Phase-1 reference-walk rewrite depends on,
straight off a real `.sapz`, WITHOUT going through read_design_model() (so it is an independent
oracle, not a circular one). Freezes the resolution as a JSON golden under __fixtures__/ that
becomes the acceptance oracle for 1a and the seed for the Phase-2c harness.

Shapes proven (see plans/stadium-behaviour-enrichment/phase-1-branch-aware-behaviour.md):
  1. A Script row (MemberAdmin `MemberUpdate.Load`) has exactly one child of type
     `...Scripts.ExecutionPath` whose props["Actions"] is the ORDERED GUID list of its root actions.
  2. That list resolves to N action nodes in exact execution order (plan asserts 10).
  3. A Decision.Decision action carries props["ExecutionPaths"] -> IfPath nodes; each IfPath carries
     props["Actions"] (ordered branch steps) + props["Conditions"] (predicate GUID list).
  4. A Conditions GUID resolves to a `...Decision.Condition` expando with {Value1, Operator, Value2, Join}.

USAGE
    python _probe_execpath.py [--app <folder>] [--out <fixture.json>] [--print]
Defaults to MemberAdmin in the out-of-repo corpus and the checked-in golden path.
Exit code 0 iff the ExecutionPath->Actions walk reproduces (>=1 action; plan expects 10).
"""

import sys, os, json, sqlite3, argparse, tempfile, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_stadium_app import norm_guid, parse_props, friendly_type, select_design_model

DEFAULT_APP = r"C:\Stadium 6 Web Apps\785d3104-7f1a-4d0d-9689-566e0c21295b"  # MemberAdmin
DEFAULT_SCRIPT = "MemberUpdate.Load"
DEFAULT_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "__fixtures__", "execpath-memberadmin-memberupdate-load.json")


def build_index(sqlitedata):
    """Independent id-index over EVERY row carrying an ID, keyed by norm_guid. Mirrors what
    read_design_model builds internally, but stands alone so this probe can falsify it."""
    con = sqlite3.connect(sqlitedata); con.row_factory = sqlite3.Row
    cur = con.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    registry, children = {}, {}
    for t in tables:
        cols = {r[1] for r in cur.execute(f"PRAGMA table_info([{t}])")}
        if "ID" not in cols:
            continue
        for r in cur.execute(f"SELECT * FROM [{t}]"):
            d = dict(r)
            gid = norm_guid(d.get("ID"))
            pid = norm_guid(d.get("ParentID")) if "ParentID" in cols else None
            if not gid:
                continue
            registry[gid] = {
                "id": gid, "parent": pid, "table": t,
                "name": d.get("Name"),
                "translation_type": d.get("TranslationType"),
                "type": friendly_type(d.get("TranslationType")),
                "props": parse_props(d.get("JsonData")) if "JsonData" in cols else {},
            }
            children.setdefault(pid, []).append(gid)
    con.close()
    return registry, children


def _norm_list(v):
    """A props Actions/ExecutionPaths/Conditions value -> list of normalised GUID strings."""
    if not isinstance(v, list):
        return []
    return [norm_guid(x) for x in v if x]


def resolve_condition(reg, cond_id):
    e = reg.get(cond_id)
    if not e:
        return {"id": cond_id, "_missing": True}
    p = e["props"]
    def _ref(v):
        if isinstance(v, dict):
            nid = norm_guid(v.get("NamedItemID")) if v.get("NamedItemID") else None
            if nid and nid in reg and reg[nid].get("name"):
                return reg[nid]["name"]
            return v.get("NamedItemID") or v.get("FormatString") or v
        return v
    return {
        "id": cond_id, "type": e["type"],
        "Value1": _ref(p.get("Value1")), "Operator": p.get("Operator"),
        "Value2": _ref(p.get("Value2")), "Join": p.get("Join"),
    }


def resolve_action(reg, children, aid, depth=0, seen=None):
    seen = seen if seen is not None else set()
    e = reg.get(aid)
    if not e:
        return {"id": aid, "_missing": True}
    if aid in seen or depth > 8:
        return {"id": aid, "type": e["type"], "_cycle_or_deep": True}
    seen.add(aid)
    node = {"id": aid, "type": e["type"], "name": e["name"], "table": e["table"]}
    if e["type"] == "Decision":
        node["ShowElse"] = e["props"].get("ShowElse")
        branches = []
        for ep_id in _norm_list(e["props"].get("ExecutionPaths")):
            ep = reg.get(ep_id) or {}
            branches.append({
                "ifpath_id": ep_id, "type": ep.get("type"),
                "conditions": [resolve_condition(reg, c) for c in _norm_list((ep.get("props") or {}).get("Conditions"))],
                "actions": [resolve_action(reg, children, a, depth + 1, seen)
                            for a in _norm_list((ep.get("props") or {}).get("Actions"))],
            })
        node["branches"] = branches
    return node


def find_execution_path(reg, children, script_id):
    for cid in children.get(script_id, []):
        e = reg.get(cid)
        if e and (e["translation_type"] or "").split(",")[0].strip().endswith("ExecutionPath"):
            return cid, e
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=DEFAULT_APP)
    ap.add_argument("--script", default=DEFAULT_SCRIPT)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--print", action="store_true", dest="do_print")
    args = ap.parse_args()

    if not os.path.isdir(args.app):
        print(f"ERROR: corpus app folder not found: {args.app}", file=sys.stderr)
        print("       (the corpus lives outside the repo; pass --app <folder>)", file=sys.stderr)
        sys.exit(3)

    workdir = tempfile.mkdtemp(prefix="stadium-probe-")
    try:
        sqlitedata, meta = select_design_model(args.app, workdir)
        if not sqlitedata:
            print(f"ERROR: no .sapz design model in {args.app}: {meta}", file=sys.stderr)
            sys.exit(3)
        reg, children = build_index(sqlitedata)

        # locate the target script (exact name, else first ending with the same event token)
        target = None
        for gid, e in reg.items():
            if e["table"] == "Script" and (e["name"] or "") == args.script:
                target = (gid, e); break
        if not target:
            for gid, e in reg.items():
                if e["table"] == "Script" and (e["name"] or "").endswith("." + args.script.split(".")[-1]):
                    target = (gid, e); break
        if not target:
            print(f"ERROR: script {args.script!r} not found among {sum(1 for e in reg.values() if e['table']=='Script')} scripts", file=sys.stderr)
            sys.exit(3)

        script_id, script_e = target
        ep_id, ep_e = find_execution_path(reg, children, script_id)
        if not ep_e:
            print(f"ERROR: no ExecutionPath child under script {script_e['name']!r}", file=sys.stderr)
            sys.exit(3)
        action_ids = _norm_list(ep_e["props"].get("Actions"))
        actions = [resolve_action(reg, children, a) for a in action_ids]

        # find one Decision anywhere in the app to prove branch/condition shape
        decision_sample = None
        for gid, e in reg.items():
            if e["type"] == "Decision" and _norm_list(e["props"].get("ExecutionPaths")):
                decision_sample = resolve_action(reg, children, gid)
                # prefer one that actually has resolved conditions
                if any(b.get("conditions") for b in decision_sample.get("branches", [])):
                    break

        golden = {
            "_about": "Phase-1 golden fixture: proves ExecutionPath->Actions ordering + Decision->IfPath->{Conditions,Actions}.",
            "_source_app": os.path.basename(args.app),
            "_source_package": meta.get("selected_package"),
            "script": {"name": script_e["name"], "id": script_id, "execution_path_id": ep_id},
            "action_count": len(actions),
            "action_sequence": [a.get("type") for a in actions],
            "actions": actions,
            "decision_sample": decision_sample,
        }

        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(golden, f, indent=2, ensure_ascii=False, default=str)

        print(f"App:      {os.path.basename(args.app)}  ({meta.get('selected_package')})")
        print(f"Script:   {script_e['name']}  (ExecutionPath child: {'yes' if ep_id else 'no'})")
        print(f"Actions:  {len(actions)} in execution order:")
        for i, a in enumerate(actions, 1):
            print(f"  {i:2}. {a.get('type')}" + (f"  [{a.get('name')}]" if a.get("name") else ""))
        if decision_sample:
            nb = len(decision_sample.get("branches", []))
            nc = sum(len(b.get("conditions", [])) for b in decision_sample.get("branches", []))
            print(f"Decision sample: {nb} branch(es), {nc} condition(s) resolved")
        print(f"Golden -> {args.out}")

        if args.do_print:
            print(json.dumps(golden, indent=2, ensure_ascii=False, default=str))

        if len(actions) < 1:
            print("FAIL: ExecutionPath->Actions resolved to zero actions.", file=sys.stderr)
            sys.exit(1)
        # The plan's asserted oracle is MemberAdmin MemberUpdate.Load -> exactly 10 ordered actions.
        if os.path.basename(args.app) == os.path.basename(DEFAULT_APP) and args.script == DEFAULT_SCRIPT and len(actions) != 10:
            print(f"FAIL: MemberUpdate.Load expected 10 actions (plan oracle), got {len(actions)}.", file=sys.stderr)
            sys.exit(1)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
