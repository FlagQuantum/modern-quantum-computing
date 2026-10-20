#!/usr/bin/env python3
"""Generate curriculum views from stable records; --check reports stale outputs."""
import argparse
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]

def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", text).strip().lower())

def render():
    data = json.loads((ROOT / "book/curriculum.json").read_text())
    parts = data["parts"]
    chapters = [c for p in parts for c in p["chapters"]]
    numbers = [c["number"] for c in chapters]
    assert numbers == list(range(1, len(chapters) + 1)), "Nonconsecutive chapter numbers"
    ids = [c["id"] for c in chapters] + [s["id"] for c in chapters for s in c["sections"]]
    assert len(ids) == len(set(ids)), "Duplicate stable ID"
    assert all(all(n in numbers and n < c["number"] for n in c["requires"]) for c in chapters), "Invalid prerequisite graph"
    section_links = {s["id"]: (f"{c['number']}.{i}", f"section-plans/{p['path']}.md#{s['id']}")
                     for p in parts for c in p["chapters"] for i, s in enumerate(c["sections"], 1)}
    count = len(section_links)
    links = {c["number"]: f"section-plans/{p['path']}.md#{c['id']}" for p in parts for c in p["chapters"]}
    summary = f"{len(parts)} parts, {len(chapters)} chapters and {count} numbered sections"
    overview = [
        "# Detailed chapter and section plan\n\n",
        f"**Revision: {data['revision']}.** {summary}. **Writing Baseline 1.0 adopted; section acceptance pending.**\n\n",
        "Each section has a learning/derivation target and an implementation/evidence target. These are authoring specifications, not completed sections or validated APIs. See the [curriculum audit](curriculum-audit.md), [reader-continuity standard](reader-continuity.md), and [full book plan](book-plan.md).\n\n",
        "## How to read the specification\n\n",
        "- Section numbers are display labels; stable chapter/section anchors preserve references when numbering changes.\n",
        "- A learning target states what the reader can explain or derive; a central result needs assumptions and a proof or an explicit advanced-proof roadmap.\n",
        "- An evidence target defines an independently checked calculation, experiment, counterexample or resource analysis. Numerical agreement does not prove a general theorem.\n",
        "- Each chapter has unnumbered closing material: recap, conceptual checks, substantial derivation/proof and transfer problems, programming/debugging laboratories, selected answers, source locators and review records.\n",
        "- Exact section prerequisites are authoritative; chapter-level entry guidance does not require completing whole chapters. Read local bridges before use. Core/advanced labels apply within specialized chapters too.\n",
        "- [Framework gaps](implementation-roadmap.md) do not remove a theoretical topic. Unsupported examples stay explicitly pending.\n",
        "- The [writing baseline](writing-baseline.md) fixes scope, depth, volumes and production order. Future drafts use local start checks; proof/software/reader review remains required for acceptance.\n\n",
        "[Full editorial review](architecture-review.md) · [All-section ledger](section-review.md) · [Checked learning paths](learning-paths.md)\n\n## Parts and chapters\n\n",
    ]
    contents = [
        "# Contents and chapter status\n\n",
        f"**Revision: {data['revision']}.** {summary} and six appendices. **Writing Baseline 1.0 adopted; chapter acceptance pending.** See the [editorial charter](editorial-charter.md), [curriculum audit](curriculum-audit.md) and [full plan](book-plan.md).\n\n",
        "The [numbered section specification](section-plan.md) gives learning, derivation and evidence targets. Only three starter chapters exist, with intended homes in **6, 23 and 49**; they require expansion. The PDF sample keeps independent numbering.\n\n",
    ]
    book = [(ROOT / "book/curriculum-introduction.md").read_text().rstrip() + "\n"]
    outputs = {}
    starters = {6: ("Measurement starter", "measurement"), 23: ("Gradients starter", "gradients"), 49: ("Hydrogen VQE starter", "vqe")}
    for p in parts:
        pnum = p["number"]
        heading = f"Part {pnum}. {p['title']}"
        overview += [f"### {heading}\n\n| Chapter | Sections | Detailed plan |\n|---|---|---|\n"]
        contents += [f"## {heading}\n\n| Chapter | Title | Reading level | Status |\n|---|---|---|---|\n"]
        book += [f"\n## {heading}\n"]
        detailed = [
            f"# {heading}\n\n",
            f"**Detailed plan · {data['revision']} · Scope fixed by Writing Baseline 1.0; prose and independent acceptance pending.** [All sections](../section-plan.md) · [Full plan](../book-plan.md) · [Reader continuity](../reader-continuity.md)\n\n",
            "Each section specifies its argument and independent evidence. Framework implementation, mathematical review and reader review have separate status. Closing materials follow the [section-plan guide](../section-plan.md#how-to-read-the-specification).\n",
        ]
        for c in p["chapters"]:
            n = c["number"]
            total = len(c["sections"])
            link = links[n]
            overview += [f"| {n} | {n}.1–{n}.{total} | [{c['title']}]({link}) |\n"]
            status = f"[{starters[n][0]}](chapters/{starters[n][1]}.md)" if n in starters else "Planned"
            contents += [f"| {n} | [{c['title']}]({link}) | {c['level']} | {status} |\n"]
            book += [f'\n<span id="{c["id"]}"></span>\n']
            if c.get("legacy_number") and c["legacy_number"] != n:
                old_book_anchor = slug(f"Chapter {c['legacy_number']}: {c['title']}")
                book += [f'<span id="{old_book_anchor}"></span>\n']
            book += [
                f"\n### Chapter {n}: {c['title']}\n\n",
                f"**Reading level:** {c['level']}. **Entry guidance:** {c['prerequisites']}\n\n",
                f"**Numbered section specification:** [Sections {n}.1–{n}.{total}]({link}).\n\n",
                f"**Planned sections:** {c['summary']}\n\n",
                f"**Mathematical outcome:** {c['outcome']}\n\n",
                f"**Experiment and independent verification:** {c['verification']}\n",
            ]
            detailed += [f'\n<span id="{c["id"]}"></span>\n']
            old = c.get("legacy_number")
            if old and old != n:
                detailed += [f'<span id="chapter-{old}"></span>\n']
            detailed += [
                f"\n## Chapter {n}\n\n**{c['title']}**\n\n",
                f"**Reading level:** {c['level']}. **Entry guidance:** {c['prerequisites']}\n",
            ]
            if n == 7:
                detailed += ["\n**Bridge:** derive no-signalling through marginal probabilities first; revisit the density-operator argument after Chapter 8.\n"]
            if n == 16:
                detailed += ["\n**Bridge:** Chapter 16 uses phase-free estimation; the QPE-based derivation is 17.8, after phase estimation.\n"]
            if n == 34:
                detailed += ["\n**Branch design:** use selected common bridges and choose a platform. Basic compilation can instead start with a supplied target contract; microscopic platform physics is a separate branch.\n"]
            if n == 50:
                detailed += ["\n**Claim/model acceptance gate:** Fowler et al. v2, Section VII A/Fig. 5 anchors syndrome ambiguity. The finite memory benchmark is a declared extension; exact model choices still need acceptance, and no threshold reproduction is promised.\n"]
            for j, s in enumerate(c["sections"], 1):
                current = slug(f"{n}.{j} {s['title']}")
                detailed += [f'\n<span id="{s["id"]}"></span>\n']
                aliases = set(s.get("aliases", []))
                if s.get("legacy_anchor"):
                    aliases.add(s["legacy_anchor"])
                for alias in sorted(aliases - {current, s["id"]}):
                    detailed += [f'<span id="{alias}"></span>\n']
                prereqs = ", ".join(f"[{section_links[x][0]}](../{section_links[x][1]})" for x in s["requires"]) or "Entry knowledge / local bridge"
                detailed += [
                    f"\n### {n}.{j} {s['title']}\n\n",
                    f"**Result/proof/source specification:** [Scholarly plan](../proof-plans/{p['path']}.md#{s['id']}).\n\n",
                    f"**Section level:** {s['reading_level']}. **Required earlier sections:** {prereqs}.\n\n",
                    f"**Learning and derivation target:** {s['theory']}\n\n",
                    f"**Implementation and evidence target:** {s['evidence']}\n",
                ]
        overview.append("\n")
        contents.append("\n")
        outputs[f"docs/section-plans/{p['path']}.md"] = "".join(detailed)
    overview += [
        "## Integration and review\n\n",
        f"The complete plan contains **{len(chapters)} chapters and {count} numbered sections**. A higher count does not establish coverage, depth or readability. The [architecture-review gates](curriculum-audit.md) require coverage, dependency, workload and reader review before sustained drafting.\n\n",
        "Existing starters supply material to 6, 23 and 49 at their scheduled homes. Writing Baseline 1.0 fixes the production queue; subsequent drafts follow its section-local start checks. Provider access and framework availability are tracked separately from theory.\n",
    ]
    notes = (ROOT / "book/curriculum-notes.md").read_text()
    outputs["docs/book-plan.md"] = re.sub(r"\n{3,}", "\n\n", "".join(book) + "\n\n" + notes).rstrip() + "\n"
    outputs["docs/section-plan.md"] = "".join(overview)
    appendix = notes.split("## Dependencies and course routes")[0]
    outputs["docs/contents.md"] = ("".join(contents) + appendix).rstrip() + "\n"
    return outputs

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = render()
    stale = [name for name, text in outputs.items() if not (ROOT / name).exists() or (ROOT / name).read_text() != text]
    if args.check:
        if stale:
            raise SystemExit("Stale curriculum views: " + ", ".join(stale))
        print("Curriculum records, prerequisites, stable IDs and generated views agree.")
    else:
        for name, text in outputs.items():
            (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / name).write_text(text)
        print(f"Generated {len(outputs)} curriculum views.")

if __name__ == "__main__":
    main()
