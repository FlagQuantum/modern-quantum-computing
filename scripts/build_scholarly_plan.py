#!/usr/bin/env python3
"""Validate and generate all-section result/proof/source and volume plans."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from build_source_evidence import build as build_evidence

ROOT = Path(__file__).resolve().parents[1]

def build():
    curriculum=json.loads((ROOT/'book/curriculum.json').read_text())
    plan=json.loads((ROOT/'book/proof-plan.json').read_text())
    sources=json.loads((ROOT/'book/proof-sources.json').read_text())
    allocation=json.loads((ROOT/'book/volumes.json').read_text())
    chapters={c['number']:c for p in curriculum['parts'] for c in p['chapters']}
    sections={s['id']:dict(s,ref=f"{c['number']}.{i}",chapter=c['number'],
              link=f"section-plans/{p['path']}.md#{s['id']}")
              for p in curriculum['parts'] for c in p['chapters'] for i,s in enumerate(c['sections'],1)}
    records={x['section_id']:x for x in plan['sections']}
    assert len(records)==len(plan['sections'])==len(sections), 'Duplicate/missing section proof record'
    assert set(records)==set(sections), 'Proof-plan coverage differs from curriculum'
    levels=plan['depth_levels'];works=sources['works'];locators=sources['locators']
    for key,loc in locators.items():
        assert loc['work'] in works and loc['locator'].strip(), key
        assert loc['proof_review']=='pending', 'Locator check must not imply proof approval'
        if loc['pages']:
            a,b=loc['pages'];assert 0<a<=b,key
            if loc['page_unit'].startswith('PDF'):assert b<=works[loc['work']]['pdf_pages'],key
        if loc['work']!='ED':assert re.fullmatch('[0-9a-f]{64}',works[loc['work']]['sha256']),key
    for id,row in records.items():
        assert row['depth'] in levels,id
        assert all(row[k].strip() for k in ('result','assumptions','proof_plan','source_review')),id
        assert row['source_locators'] and all(k in locators for k in row['source_locators']),id
        if 'Z2018:status' in row['source_locators']:assert 'ZR2021:notice' in row['source_locators'], id
        if 'L2026:comment' in row['source_locators']:assert 'MR2026:reply' in row['source_locators'], id
        assert row['mathematical_review']=='pending', 'Planning does not certify proofs'
        if row['depth']=='R':
            assert row['local_bridge_requirements'].strip() and row['deferred_proof_ingredients'].strip(), id
        if row['depth'] in {'F','M','R'}:
            assert any(locators[k]['work']!='ED' for k in row['source_locators']),id
    volumes=allocation['volumes'];owner={};volume_order={v['id']:i for i,v in enumerate(volumes)}
    for v in volumes:
        assert v['chapters'] and len(v['chapters'])==len(set(v['chapters']))
        for n in v['chapters']:
            assert n in chapters and n not in owner, 'Missing/duplicate volume chapter'
            owner[n]=v['id']
    assert set(owner)==set(chapters),'Incomplete volume allocation'
    position={s['id']:(volume_order[v['id']],j,i)
              for v in volumes for j,n in enumerate(v['chapters'])
              for i,s in enumerate(chapters[n]['sections'])}
    for id,s in sections.items():
        for dep in s['requires']:
            assert dep in sections and position[dep]<position[id],f'Later-volume/section prerequisite: {s["ref"]}'
    def slink(id,prefix=''):
        s=sections[id];return f"[{s['ref']}]({prefix}{s['link']})"
    def anchor(key):return 'source-'+re.sub('[^a-z0-9]+','-',key.lower()).strip('-')
    outputs={};counts=Counter(x['depth'] for x in records.values())
    intro=[
        '# Core results, proof depth, and exact source plan\n\n',
        f"**{len(chapters)} chapters / {len(sections)} sections · {plan['revision']} · planning only.** No new textbook body is written by this specification. ",
        'Every section has a result or explicit non-theorem role, assumptions, proof obligation and version-specific source locators. ',
        'A source locator identifies where to read; it does not certify that its proof has been independently checked or that a FlagQuantum API implements it.\n\n',
        '[Volume proposal](volume-plan.md) · [Exact source catalogue](references/proof-sources.md) · [Prerequisites](section-review.md) · [Acceptance gates](curriculum-audit.md)\n\n',
        '## Proof-depth contract\n\n| Code | Planned depth | Sections | Acceptance requirement |\n|---|---|---|---|\n',
    ]
    for k,v in levels.items():intro.append(f"| {k} | {v['name']} | {counts[k]} | {v['requirement']} |\n")
    intro += [
        '\n**Global convention:** '+plan['global_assumptions']+'\n\n',
        '“Complete proof” is relative to explicitly stated imported earlier results. For example, the Holevo proof can use the previously stated data-processing theorem; it must disclose that dependence. ',
        'Definitions, physical postulates and experiment protocols are not relabeled as theorems. For R sections, exact quantifiers/constants and the selected theorem revision must be transcribed and reviewed before drafting; the plan is not the theorem statement itself.\n\n',
        '## All-section specifications\n\n| Part | Detailed proof/source plan |\n|---|---|\n',
    ]
    for p in curriculum['parts']:
        intro.append(f"| {p['number']} | [{p['title']}](proof-plans/{p['path']}.md) |\n")
        doc=[f"# Result and proof plan: {p['title']}\n\n",
             '[Depth definitions](../proof-plan.md#proof-depth-contract) · [Source catalogue](../references/proof-sources.md) · [Volume plan](../volume-plan.md)\n\n',
             'Authoring specifications only. No result/proof/API is certified by this plan. F/M/R have different scope; imported results are the exact prerequisite sections linked below.\n']
        for c in p['chapters']:
            doc.append(f"\n## Chapter {c['number']}: {c['title']}\n")
            for i,s in enumerate(c['sections'],1):
                row=records[s['id']];ref=f"{c['number']}.{i}"
                doc += [f'\n<span id="{s["id"]}"></span>\n\n### {ref} {s["title"]}\n\n',
                        f"**Core result / role:** {row['result']}.\n\n",
                        f"**Assumptions and scope:** {row['assumptions']}.\n\n",
                        f"**Proof depth:** {row['depth']} — {levels[row['depth']]['name']}. **Proof obligation:** {row['proof_plan']}.\n\n",
                        '**Imported earlier results:** '+(', '.join(slink(x,'../') for x in s['requires']) or 'Entry knowledge / locally supplied bridge')+'.\n\n',
                        '**Exact source targets:** '+ '; '.join(f"[{k}](../references/proof-sources.md#{anchor(k)}): {locators[k]['locator']}" for k in row['source_locators'])+'.\n\n',
                        f"**Independent evidence target:** {s['evidence']}\n\n",
                        f"**Planning budget:** {s['page_budget'][0]}–{s['page_budget'][1]} pages. **Review status:** {row['source_review']}; mathematical and implementation review remain separate.\n",
                ]
                if row.get('local_bridge_requirements'):
                    doc += [f"\n**Local mathematical bridge to supply:** {row['local_bridge_requirements']}.\n"]
                if row['depth']=='R':
                    doc += [f"\n**Explicitly deferred proof ingredients:** {row['deferred_proof_ingredients']}.\n"]
        outputs[f"docs/proof-plans/{p['path']}.md"]=''.join(doc)
    intro += [
        '\n## Outstanding source acceptance items\n\n',
        '- 49.2: [H2-01–09](references/h2-provenance.md) now pins the integral-to-model chain and independent 324-coefficient audit. Original author integral files were not recovered; mathematical/reader acceptance remains open.\n',
        '- 40.7: [TOPO-01–09](references/topological-experiments.md) now selects dated primary sources and pairs critique/reply and retraction records. The [full public argument audit](references/topological-dispute-review.md) now compares nine disputes. Exact final-journal-reply text matching, raw/corrected data analysis and specialist interpretation remain open.\n',
        '- Chapter 50 now selects Fowler et al. v2, Section VII A/Fig. 5 for syndrome ambiguity. The finite memory experiment is a declared textbook extension; Fig. 4 threshold results are outside the reproduction claim. Exact patch/round/decoder choices still require acceptance.\n',
        '- All proof plans require mathematical/source review, source-specific counterexamples and calibrated problem/example budgets before baseline freeze. Locator checks and planned full proofs do not satisfy those gates.\n',
    ]
    outputs['docs/proof-plan.md']=''.join(intro)
    catalogue=[
        '# Exact sources for the result and proof plan\n\n',
        f"**{len(works)} works / {len(locators)} locators · checked/assigned {sources['revision']}.** ",
        'The catalogue records the actual manuscript/edition, citation metadata, section or page target, and the SHA-256 of the locally accessed source artifact (PDF, publisher HTML or basis JSON). ',
        'The files and extracted source passages are not distributed. Public availability does not confer redistribution permission. ',
        'Historical reviews support stated models, not current performance rankings. An arXiv v1 can have a different title/author order from its journal publication.\n\n',
        '[Section plans](../proof-plan.md) · [Download BibTeX](proof-plan.bib)\n\n',
        '## Locator and review semantics\n\n',
        'NC uses section starts checked in the supplied 10th Anniversary contents; page numbers are printed pages. Watrous and Boyd use the accessed manuscripts’ printed pages. ',
        'Other numeric intervals use **1-based PDF pages**, including title/front matter. A section or named theorem disambiguates the target; an interval can include only the relevant portion of a section. ',
        'Contents/heading/targeted-text locator checks are not line-by-line proof verification. Mathematical review is pending for every planned result. Original editorial entries provide methodology only, not external theorem authority.\n\n',
    ]
    bib=[]
    for k,w in works.items():
        catalogue += [f'\n<span id="work-{k.lower()}"></span>\n\n## {k}: {w["title"]}\n\n',
                      f"{w['authors']} ({w['year']}). **Accessed version:** {w['revision']}. [Source]({w['url']}).\n\n"]
        if w['note']:catalogue.append(w['note']+'.\n\n')
        if w.get('sha256'):catalogue.append('**Accessed source SHA-256 ('+w.get('media_type','application/pdf')+'):** '+w['sha256']+'.\n\n')
        for key,l in locators.items():
            if l['work']!=k:continue
            page_text=(str(l['pages'][0]) if l['pages'][0]==l['pages'][1] else f"{l['pages'][0]}–{l['pages'][1]}") if l['pages'] else ''
            pages=f"; {l['page_unit']} {page_text}" if l['pages'] else ''
            catalogue += [f'<span id="{anchor(key)}"></span>\n\n',f"- **{key}:** [{l['locator']}]({l['url']}){pages}. Locator status: {l['status']}; proof review pending.\n\n"]
        # Only the checked family-name metadata is exported; initials are not invented.
        family_names=re.split(r', | and ', w['authors'].replace(' et al.', ' and others'))
        bib_author=' and '.join('{'+name+'}' if ' ' in name else name for name in family_names)
        safe=lambda x:x.replace('{','').replace('}','')
        bib.append('@misc{plan_'+k.lower()+',\n  author = {'+bib_author+'},\n  title = {'+safe(w['title'])+'},\n  year = {'+str(w['year'])+'},\n  url = {'+w['url']+'},\n  note = {'+safe(w['authors']+'; accessed version: '+w['revision']+'; '+w['note'])+'}\n}\n')
    outputs['docs/references/proof-sources.md']=''.join(catalogue)
    outputs['docs/references/proof-plan.bib']='\n'.join(bib)
    volume=[
        '# A dependency-compatible seven-volume proposal\n\n',
        '**Editorial recommendation · '+allocation['revision']+' · packaging not frozen.** '+allocation['policy']+'\n\n',
        'The proof-depth pass changes the earlier uniform budgets. Foundations and information together would reach an estimated 738 pages with closing/front material; splitting them keeps distinct entry and advanced-information courses usable. ',
        'Seven subject volumes avoid compressing proofs to fit an arbitrary chapter/page count. These are planned ranges, not rendered pages or promised release dates.\n\n',
        '| Volume | Title | Global chapters | Sections | Planned pages including 24–40 pages of volume front/back matter |\n|---|---|---|---|---|\n',
    ]
    totals=[0,0]
    for v in volumes:
        ss=[s for n in v['chapters'] for s in chapters[n]['sections']]
        budget=[sum(s['page_budget'][i] for s in ss)+v['front_back_budget'][i] for i in (0,1)]
        totals=[a+b for a,b in zip(totals,budget)]
        volume.append(f"| [{v['id']}](#volume-{v['id'].lower()}) | {v['title']} | {', '.join(map(str,v['chapters']))} | {len(ss)} | {budget[0]}–{budget[1]} |\n")
    volume += [f'\nSeries total: **{totals[0]}–{totals[1]} planned pages**, including the stated per-volume front/back allocation, but excluding substantial shared appendices/solutions. ',
               'Central full proofs have extra space; ordinary F/M sections receive 3–6 pages, advanced theorem roadmaps 4–8, and 23 substantial arguments 6–10. These ranges require reader and typesetting calibration.\n\n',
               '## Reading continuity and shared material\n\n',
               'Global Chapter 14 closes Volume I so basic computational models are available without first completing advanced information theory. Global Chapter 48 is placed in Volume IV before the two capstones need its methods. ',
               'The H2 capstone (49) closes Volume IV; memory (50) closes Volume V. Its exact tiny reference uses dense/error enumeration, so it does not require the later tableau implementation (45). ',
               'Existing global numbers/URLs/IDs remain stable. Print running heads and the series contents identify both the volume and global chapter. Avoid an additional independent numbering scheme for concepts.\n\n',
               'No section requires a later volume under the current graph and this internal chapter ordering. This is structural consistency, not completed learner validation. ',
               'Readers need the **specified sections**, not all preceding volumes. Use the [19 checked routes](learning-paths.md) for courses; fixed kernels, basic compilation and physical branches retain their lighter entry contracts.\n\n']
    for v in volumes:
        imports=sorted({dep for n in v['chapters'] for s in chapters[n]['sections'] for dep in s['requires'] if owner[sections[dep]['chapter']]!=v['id']},key=lambda id:tuple(map(int,sections[id]['ref'].split('.'))))
        volume += [f'\n<span id="volume-{v["id"].lower()}"></span>\n\n## Volume {v["id"]}: {v["title"]}\n\n',v['role']+'\n\n',
                   f"**Cross-volume imports:** {len(imports)} distinct direct prerequisite sections across the full volume, including optional advanced branches. This is not one course's mandatory reading list.\n\n"]
        groups={}
        for id in imports:groups.setdefault(sections[id]['chapter'],[]).append(id)
        for n,ids in groups.items():volume.append(f"- **Chapter {n}:** "+', '.join(slink(id) for id in ids)+'.\n')
        if not imports:volume.append('No earlier-volume section imports.\n')
    volume += [
        '\n## Alternatives and publishing sequence\n\n',
        'One/three large books would create long mixed courses and oversized manuscripts. Five/six books reduce bindings but either merge distinct specialization routes or leave the opening volume especially long. ',
        'Seven is the present editorial recommendation, with related volumes also distributable as a series bundle and one searchable website. Reassess against actual typesetting and reader workload before freezing; do not trade away central proof obligations to preserve a chosen volume count.\n\n',
        'After the architecture gate, build coherent accepted routes incrementally. Start with Volume I’s opening route; develop one complete algorithm route and a gradient-to-H2 route next. ',
        'Advanced information, fault tolerance, platforms and systems follow their required specialist review. This is an eventual publication architecture, not authorization to draft seven volumes now.\n\n',
        'Shared appendices A–F, glossary, symbol index and bibliography use one canonical source and stable links; print includes locally required bridges and sufficient notation. ',
        'Core exercises/selected solutions and independent references remain accessible offline. Runtime/provider instructions stay versioned companions. Exact theorem/source acceptance, reader testing and final page/problem budgets still precede baseline freeze.\n',
    ]
    outputs['docs/volume-plan.md']=''.join(volume)
    outputs.update(build_evidence(ROOT,sources,{x['ref']:x['link'] for x in sections.values()}))
    return outputs,dict(sections=len(sections),works=len(works),locators=len(locators),volumes=len(volumes),depth_counts=dict(counts),series_pages=totals)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs,stats=build();stale=[p for p,t in outputs.items() if not (ROOT/p).exists() or (ROOT/p).read_text()!=t]
    if args.check:
        if stale:raise SystemExit('Stale scholarly-plan views: '+', '.join(stale))
    else:
        for p,t in outputs.items():(ROOT/p).parent.mkdir(parents=True,exist_ok=True);(ROOT/p).write_text(t)
    print(json.dumps(stats))
if __name__=='__main__':main()
