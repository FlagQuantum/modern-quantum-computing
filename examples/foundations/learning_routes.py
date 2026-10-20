#!/usr/bin/env python3
"""Resolve planned reading routes; this is not a learner-completion test.

Run from a complete repository checkout. Python 3.12, standard library only.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def expand(spec):
    if "-" not in spec:
        return [spec]
    start, last = spec.split("-")
    chapter, first = map(int, start.split("."))
    return [f"{chapter}.{i}" for i in range(first, int(last) + 1)]


def closure(targets, sections):
    """Include every direct and indirect prerequisite, including targets."""
    included = set(targets)
    while True:
        enlarged = included | {
            prior for section_id in included
            for prior in sections[section_id]["requires"]
        }
        if enlarged == included:
            return included
        included = enlarged


def check_order(study, known, sections):
    """Return the first unmet prerequisite, or None; known means assumed studied."""
    seen = set(known)
    for section_id in study:
        missing = set(sections[section_id]["requires"]) - seen
        if missing:
            return section_id, sorted(missing)
        seen.add(section_id)
    return None


def resolve_routes(data):
    sections = {}
    by_ref = {}
    for part in data["parts"]:
        for chapter in part["chapters"]:
            for number, section in enumerate(chapter["sections"], 1):
                section_id = section["id"]
                assert section_id not in sections
                sections[section_id] = section
                by_ref[f"{chapter['number']}.{number}"] = section_id
    order = {section_id: i for i, section_id in enumerate(sections)}
    routes = {}
    for route in data["learning_routes"]:
        known = set()
        for parent in route["assumes"]:
            known |= routes[parent]["complete"]
        targets = {by_ref[ref] for spec in route["targets"] for ref in expand(spec)}
        complete = closure(targets | known, sections)
        study = sorted(complete - known, key=order.get)
        assert check_order(study, known, sections) is None
        assert targets <= known | set(study)
        routes[route["id"]] = dict(known=known, study=study, complete=complete)
    return sections, by_ref, routes


def main():
    data = json.loads((ROOT / "book/curriculum.json").read_text())
    sections, by_ref, routes = resolve_routes(data)
    # Independent hand-sized reference: C needs B, and B needs A.
    tiny = {"A": {"requires": []}, "B": {"requires": ["A"]},
            "C": {"requires": ["B"]}}
    assert closure({"C"}, tiny) == {"A", "B", "C"}
    assert check_order(["B", "C"], set(), tiny) == ("B", ["A"])
    assert check_order(["B", "C"], {"A"}, tiny) is None
    assert len(sections) == 435 and len(routes) == 19
    print("Planning graph only; neither learner completion nor prose acceptance is certified.")
    for name in ("algorithms", "hybrid-learning", "compiler-core"):
        route = routes[name]
        print(f"{name}: {len(route['known'])} assumed sections; "
              f"{len(route['study'])} new sections; prerequisite order checked.")
    # A deliberately broken real route: skip 1.1 before attempting 1.4.
    missing = check_order([by_ref["1.4"]], set(), sections)
    assert missing == (by_ref["1.4"], [by_ref["1.1"]])
    print("Broken entry detected: 1.4 requires 1.1.")
    compiler = set(routes["compiler-core"]["study"])
    unrelated = {section["id"] for part in data["parts"]
                 for chapter in part["chapters"]
                 if chapter["number"] in {17, 34, 35, 36, 37, 38, 39, 40}
                 for section in chapter["sections"]}
    assert not compiler & unrelated
    print("Compiler core does not import QFT or microscopic platform chapters.")
    print("Tiny-chain reference, all 19 routes, and missing-entry checks passed.")


if __name__ == "__main__":
    main()
