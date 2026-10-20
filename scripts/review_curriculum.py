#!/usr/bin/env python3
"""Validate exact prerequisites and generate the editorial audit/learning paths."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def expand(spec):
    """Expand 17.1-3 to numbered section references."""
    if "-" not in spec:
        return [spec]
    start, end = spec.split("-")
    chapter, first = map(int, start.split("."))
    return [f"{chapter}.{i}" for i in range(first, int(end) + 1)]

def build():
    data = json.loads((ROOT / "book/curriculum.json").read_text())
    chapters = [c for p in data["parts"] for c in p["chapters"]]
    byid = {}
    byref = {}
    for p in data["parts"]:
        for c in p["chapters"]:
            for i, s in enumerate(c["sections"], 1):
                ref = f"{c['number']}.{i}"
                item = dict(s, ref=ref, chapter=c["number"],
                            link=f"section-plans/{p['path']}.md#{s['id']}")
                assert s["id"] not in byid, "Duplicate stable section ID"
                byid[s["id"]] = item
                byref[ref] = item
    order = {id: i for i, id in enumerate(byid)}
    for id, s in byid.items():
        assert "requires" in s and "planning_review" in s, f"Missing review fields: {s['ref']}"
        assert len(s["requires"]) == len(set(s["requires"])), f"Repeated prerequisite: {s['ref']}"
        for prerequisite in s["requires"]:
            assert prerequisite in byid, f"Unknown prerequisite: {s['ref']}"
            assert order[prerequisite] < order[id], f"Non-earlier prerequisite: {s['ref']} -> {byid[prerequisite]['ref']}"
        assert s["reading_level"] in {"core", "advanced"}
        assert len(s["page_budget"]) == 2 and 0 < s["page_budget"][0] <= s["page_budget"][1]
    def closure(ids):
        result = set()
        def visit(id):
            if id in result:
                return
            for previous in byid[id]["requires"]:
                visit(previous)
            result.add(id)
        for id in ids:
            visit(id)
        return result
    def ids_from_specs(specs):
        return {byref[ref]["id"] for spec in specs for ref in expand(spec)}
    routes = {}
    for route in data["learning_routes"]:
        assert route["id"] not in routes
        known = set()
        for parent in route["assumes"]:
            assert parent in routes, f"Unknown/forward assumed route: {parent}"
            known |= routes[parent]["complete"]
        targets = ids_from_specs(route["targets"])
        complete = closure(targets | known)
        route = dict(route, targets_ids=targets, known=known, complete=complete,
                     study=sorted(complete-known, key=order.get))
        # Reconstruct the declared path: no section may use unseen prerequisites.
        seen = set(known)
        for id in route["study"]:
            assert set(byid[id]["requires"]) <= seen, f"Invalid route {route['id']}: {byid[id]['ref']}"
            seen.add(id)
        assert targets <= seen
        routes[route["id"]] = route
    # Guard the pedagogical repairs, rather than just testing a DAG's syntax.
    assert not any(byid[id]["chapter"] == 17 for id in closure(ids_from_specs(["16.1-8"])))
    assert not any(byid[id]["chapter"] in {17,18,19,20,21,34,35,36,37,38,39,40}
                   for id in routes["compiler-core"]["study"])
    assert not any(byid[id]["chapter"] in {23,24,25,26}
                   for id in routes["fixed-kernels"]["study"])
    assert not any(byid[id]["chapter"] in {32,33} for id in routes["logical-memory"]["study"])
    assert not any(byid[id]["ref"] in {"25.7","25.9","25.10","25.11"}
                   for id in routes["h2-research"]["study"])
    assert not any(byid[id]["chapter"] == 46 for id in closure(ids_from_specs(["47.1-5"])))
    audit = json.loads((ROOT / "book/architecture-review.json").read_text())
    assert audit["reviewed_chapter_count"] == len(chapters)
    assert audit["reviewed_section_count"] == len(byid)
    assert {row["chapter"] for row in audit["chapters"]} == {c["number"] for c in chapters}
    assert len(audit["chapters"]) == len(chapters) and len(audit["sections"]) == len(byid)
    assert {row["section_id"] for row in audit["sections"]} == set(byid)
    for row in audit["sections"]:
        assert row["chapter"] == byid[row["section_id"]]["chapter"], "Wrong ledger chapter"
        assert row["disposition"].strip(), "Empty section disposition"
    assert {row["chapter"]: row["decision"] for row in audit["chapters"]} == {
        c["number"]: c["architecture_review"] for c in chapters}, "Chapter review records disagree"
    def link(id):
        s = byid[id]
        return f"[{s['ref']}]({s['link']})"
    report = [
        "# Systematic editorial architecture review\n\n",
        f"**Review date: {audit['date']}. Scope: all {len(chapters)} chapters and {len(byid)} sections.** ",
        "This is a completed editorial architecture pass, not external specialist, mathematical-proof, API or reader validation. ",
        "**New textbook body drafting is paused until the architecture baseline gate is satisfied.**\n\n",
        "[Findings and scope decisions](curriculum-audit.md) · [Exact section ledger](section-review.md) · [Checked learning paths](learning-paths.md)\n\n",
        "## Findings and dispositions\n\n| ID | Finding | Repair or explicit disposition |\n|---|---|---|\n",
    ]
    for f in audit["findings"]:
        report.append(f"| {f['id']} | {f['finding']} | {f['disposition']} |\n")
    report += [
        "\n## Every-chapter review and provisional workload\n\n",
        "Ranges are editorial planning estimates for explanatory text, examples and exercises; they are not measured reading time or completed page counts. They use per-section budgets and exclude appendices/front matter. Advanced modules can be omitted from an introductory route.\n\n",
        "| Chapter | Sections | Planned pages | Specific architecture decision |\n|---|---|---|---|\n",
    ]
    total_min = total_max = 0
    for c in chapters:
        low = sum(s["page_budget"][0] for s in c["sections"])
        high = sum(s["page_budget"][1] for s in c["sections"])
        total_min += low
        total_max += high
        report.append(f"| {c['number']} | {len(c['sections'])} | {low}–{high} | {c['architecture_review']} |\n")
    report += [
        f"\nThe whole reference architecture budgets **{total_min}–{total_max} pages before appendices/front matter**. ",
        "This does not fit a single introductory course. Use the route-specific selections; assess coordinated volume packaging before freezing publication scope.\n\n",
        "## What has and has not passed\n\n",
        f"- Editorial coverage/ownership pass: all {len(chapters)} chapters and {len(byid)} sections recorded.\n",
        f"- Exact prerequisite graph: {sum(len(s['requires']) for s in byid.values())} direct edges, each earlier than its use; no cycles or unresolved section references.\n",
        f"- Learning paths: {len(routes)} explicit routes reconstructed from prerequisites and checked for missing entry knowledge.\n",
        "- Specialist validation, exact theorem/source acceptance, complete cross-layer programs and target-reader testing remain pending.\n",
        "- A [seven-volume allocation](volume-plan.md) and [all-section proof/source plan](proof-plan.md) are proposed; final packaging and a tagged architecture freeze remain pending; no new body chapters are authorized by this audit alone.\n",
    ]
    ledger = [
        "# Section-by-section architecture ledger\n\n",
        f"**{len(byid)} section records, editorial review only.** Each row links to the argument/evidence targets and lists its curated direct prerequisites. ",
        "A retained row has been assessed for role and dependency, not certified as mathematically proved or implemented. Advanced branches may require extra earlier sections without blocking a core route.\n\n",
    ]
    dispositions = {s["section_id"]:s["disposition"] for s in audit["sections"]}
    for p in data["parts"]:
        ledger += [f"## Part {p['number']}. {p['title']}\n\n| Section | Level | Direct prerequisites | Editorial disposition |\n|---|---|---|---|\n"]
        for c in p["chapters"]:
            for s in c["sections"]:
                id = s["id"];prereqs=", ".join(link(x) for x in s["requires"]) or "Entry / local bridge"
                ledger.append(f"| {link(id)} {s['title']} | {s['reading_level']} | {prereqs} | {dispositions[id]} |\n")
        ledger.append("\n")
    pathdoc = [
        "# Learning paths with checked prerequisites\n\n",
        "These are planned section sequences, not validated syllabi. Each path states its assumed earlier route(s), selects targets and includes the exact transitive prerequisites needed. ",
        "Lists are printed in prerequisite-safe order. Unselected advanced sections are not silently required.\n\n",
        "“Planned pages” is the per-section editorial range for the new reading only, not an empirical time estimate. Large routes are multi-stage/advanced sequences rather than a promise of one semester.\n\n",
        "| Route | New sections | Added prerequisite sections | Planned pages | Assumed route(s) |\n|---|---|---|---|---|\n",
    ]
    path_summary = {}
    for id, route in routes.items():
        new = route["study"];added = set(new)-route["targets_ids"]
        low=sum(byid[x]["page_budget"][0] for x in new);high=sum(byid[x]["page_budget"][1] for x in new)
        path_summary[id] = dict(new_sections=len(new), added_prerequisites=len(added), planned_pages=[low,high])
        pathdoc.append(f"| [{route['title']}](#{id}) | {len(new)} | {len(added)} | {low}–{high} | {', '.join(route['assumes']) or 'Basic Python/entry arithmetic'} |\n")
    for id, route in routes.items():
        pathdoc += [f'\n<span id="{id}"></span>\n\n## {route["title"]}\n\n',
                    f"**Entry:** {', '.join(route['assumes']) or 'Basic Python/entry arithmetic'}. **Scope:** {route['scope']}\n\n"]
        bychapter = {}
        for section_id in route["study"]:
            bychapter.setdefault(byid[section_id]["chapter"], []).append(section_id)
        for n, ids in bychapter.items():
            pathdoc.append(f"- **Chapter {n}:** " + ", ".join(link(x) for x in ids) + ".\n")
        pathdoc += ["\n**Completion check:** reconstruct a selected derivation, implement its independent small reference, diagnose a changed case and explain the cost/error assumptions. Reader validation of these paths remains pending.\n"]
    stats=dict(chapters=len(chapters), sections=len(byid),
               direct_prerequisite_edges=sum(len(s["requires"]) for s in byid.values()),
               routes=path_summary, manuscript_page_budget=[total_min,total_max])
    return {
        "docs/architecture-review.md":"".join(report),
        "docs/section-review.md":"".join(ledger),
        "docs/learning-paths.md":"".join(pathdoc),
    }, stats

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    outputs,stats=build()
    stale=[name for name,text in outputs.items() if not (ROOT/name).exists() or (ROOT/name).read_text()!=text]
    if args.check:
        if stale:raise SystemExit("Stale review views: "+", ".join(stale))
    else:
        for name,text in outputs.items():(ROOT/name).write_text(text)
    print(f"Reviewed {stats['chapters']} chapters / {stats['sections']} sections / {stats['direct_prerequisite_edges']} direct edges / {len(stats['routes'])} routes; generated views agree.")
if __name__=="__main__":main()
