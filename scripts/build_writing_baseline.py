#!/usr/bin/env python3
"""Check the adopted writing scope and render the full dependency-safe work queue."""
import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def scope_payload(curriculum,proof,volumes,baseline):
    records={x['section_id']:x for x in proof['sections']}
    chapters=[]
    for part in curriculum['parts']:
        for chapter in part['chapters']:
            sections=[]
            for section in chapter['sections']:
                record=records[section['id']]
                sections.append({k:section[k] for k in ['id','title','requires','reading_level','page_budget']} | {
                    'depth':record['depth'],'result':record['result'],'assumptions':record['assumptions'],
                    'local_bridge_requirements':record.get('local_bridge_requirements',''),
                    'deferred_proof_ingredients':record.get('deferred_proof_ingredients','')})
            chapters.append(dict(number=chapter['number'],id=chapter['id'],title=chapter['title'],sections=sections))
    return dict(chapters=chapters,routes=curriculum['learning_routes'],depth_levels=proof['depth_levels'],
                volumes=volumes['volumes'],batches=baseline['batches'],appendices=baseline['appendices'])


def digest(payload):
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def build():
    load=lambda name:json.loads((ROOT/name).read_text())
    c=load('book/curriculum.json');p=load('book/proof-plan.json');v=load('book/volumes.json')
    b=load('book/writing-baseline.json');progress=load('book/writing-progress.json');brief=load('book/briefs/ch01.json')
    assert b['status']=='adopted-for-editorial-execution'
    assert digest(scope_payload(c,p,v,b))==b['scope_sha256'], 'Writing scope changed: record an impact assessment and baseline revision before refreshing the scope digest.'
    assert progress['baseline']==brief['baseline']==b['id']
    assert 'No new standalone paper audits' in b['research_policy']
    chapters={ch['number']:ch for part in c['parts'] for ch in part['chapters']}
    sections={s['id']:dict(s,ref=f"{ch['number']}.{i}",chapter=ch['number'],
                         link=f"section-plans/{part['path']}.md#{s['id']}",
                         proof_link=f"proof-plans/{part['path']}.md#{s['id']}")
              for part in c['parts'] for ch in part['chapters'] for i,s in enumerate(ch['sections'],1)}
    byref={s['ref']:id for id,s in sections.items()};records={x['section_id']:x for x in p['sections']}
    assert len(chapters)==50 and len(sections)==435 and len(c['learning_routes'])==19
    assert len(b['batches'])==16 and len({row['id'] for row in b['batches']})==16
    assert set(progress['sections']) <= set(sections)
    for id,row in progress['sections'].items():
        assert row['state'] in b['states'],id
        if row['state']=='accepted':
            assert row['mathematical_review']=='passed' and row['reader_review']=='passed',id
            assert row['implementation_review'] in ['passed','justified-N/A'],id
            assert row.get('review_evidence'),id
    seen=set();queue=[];batches=[]
    def expand(spec):
        start,sep,last=spec.partition('-');chapter,first=map(int,start.split('.'))
        return [byref[f'{chapter}.{i}'] for i in range(first,(int(last) if sep else first)+1)]
    for batch in b['batches']:
        targets=[id for spec in batch['targets'] for id in expand(spec)]
        new=[];previous=set(seen)
        def visit(id):
            if id in seen:return
            for dep in sections[id]['requires']:visit(dep)
            assert set(sections[id]['requires']) <= seen,id
            seen.add(id);new.append(id)
        for id in targets:visit(id)
        imported=[id for id in new if id not in set(targets)]
        for id in new:
            s=sections[id];state=progress['sections'].get(id,{}).get('state','not_started')
            queue.append(dict(sequence=len(queue)+1,batch=batch['id'],section_id=id,ref=s['ref'],title=s['title'],
                              depth=records[id]['depth'],requires=s['requires'],role='inserted prerequisite' if id in imported else 'batch target',state=state,
                              planned_body_path=f"docs/chapters/{chapters[s['chapter']]['id']}.md"))
        batches.append(dict(batch,new=new,imported=imported,already=len(set(targets)&previous)))
    assert len(queue)==len(seen)==len(sections) and seen==set(sections)
    position={row['section_id']:row['sequence'] for row in queue}
    assert all(position[dep]<position[id] for id,s in sections.items() for dep in s['requires'])
    for id,row in progress['sections'].items():
        if row['state']=='accepted':assert all(progress['sections'].get(dep,{}).get('state')=='accepted' for dep in sections[id]['requires']),id
    for row in brief['sections']:
        id=row['section_id'];assert row['requires']==sections[id]['requires'] and row['depth']==records[id]['depth']
        assert row['source_locators']==records[id]['source_locators']
        assert progress['sections'][id]['state'] in ['brief_ready','draft','review','accepted']
    assert [x['section_id'] for x in brief['sections']]==b['first_batch']
    assert [row['ref'] for row in queue[:6]]==[f'1.{i}' for i in range(1,7)]
    def link(id):return f"[{sections[id]['ref']}]({sections[id]['link']})"
    def chapterlink(n):
        s=next(s for s in sections.values() if s['chapter']==n)
        return f"[{n}]({s['link'].split('#')[0]}#{chapters[n]['id']})"
    counts=Counter(row['state'] for row in queue);depth=Counter(row['depth'] for row in queue)
    next_row=next((row for row in queue if row['state']!='accepted'),None)
    next_text=(link(next_row['section_id'])+' '+next_row['title']) if next_row else 'All sections accepted; proceed to route/edition release checks'
    main=['# Executable writing baseline 1.0\n\n',
          f"**{b['revision']} · {b['id']} · adopted for editorial execution.** {b['scope']}\n\n",
          '[Full ordered queue](writing-order.md) · [First-chapter briefs](writing-first-batch.md) · [Result/proof obligations](proof-plan.md) · [Reader routes](learning-paths.md) · [Seven-volume allocation](volume-plan.md)\n\n',
          '## Decision and immediate next work\n\n',b['body_policy']+'\n\n',
          'The previous all-series drafting hold is replaced by this baseline plus the local start and acceptance gates below. External mathematical, software and reader review are still required for acceptance; none is being claimed complete. ',
          'A versioned working structure lets that evidence be collected while coherent drafts are written, rather than requiring evidence from an unwritten book before drafting can start.\n\n',
          f"**Next unfinished section:** {next_text}. The initial writing assignment is 1.1, then 1.2–1.6; all six briefs are prepared. This baseline change itself supplies no new chapter body. ",
          f"Current queue: **{counts.get('brief_ready',0)} brief-ready / {counts.get('draft',0)} drafts / {counts.get('review',0)} in review / {counts.get('accepted',0)} accepted / {counts.get('not_started',0)} not started**. The three previous starters are format pilots and are not counted as accepted sections.\n\n",
          b['research_policy']+'\n\n',
          '## Frozen scope and authoritative records\n\n',
          '| Decision | Baseline |\n|---|---|\n',
          '| Contents and ownership | Nine subject parts, 50 global chapters, 435 stable section IDs; current intentional exclusions and owner/reuse boundaries remain in force. |\n',
          '| Prerequisites | 1,045 exact direct section dependencies and 19 reader routes; use exact sections rather than entire preceding volumes. |\n',
          '| Depth | Every section keeps its existing result, assumptions and P/F/M/R/V obligation; no proof downgrade to make the project shorter. |\n',
          '| Packaging | Seven volumes with the chapter allocation below; global IDs and chapter numbers are preserved. Trim size, typeset pages and release dates remain production decisions. |\n',
          '| Production | 16 ordered batches and one generated 435-section queue; imported prerequisite bridges are exposed before first use. |\n',
          '| Changes | The structural scope digest and tagged Git revision preserve the baseline. Citation refinements and body edits can proceed within frozen learning/proof scope; material changes use a new baseline revision. |\n\n',
          'Canonical records are `book/curriculum.json` (scope/graph/routes), `book/proof-plan.json` (depth/result/assumptions), `book/volumes.json` (allocation), ',
          '`book/writing-baseline.json` (batch/acceptance decisions), and `book/writing-progress.json` (actual work/review state). ',
          'Planning source-locator checks remain distinct from actual manuscript review evidence. The full baseline is recoverable from Git tag `'+b['id']+'`; the book/PDF edition number is separate.\n\n',
          '## Adopted seven-volume plan\n\n| Volume | Title | Global chapters, in reading order | Sections | Planned pages |\n|---|---|---|---|---|\n']
    for vol in v['volumes']:
        ss=[s for n in vol['chapters'] for s in chapters[n]['sections']]
        pages=[sum(s['page_budget'][i] for s in ss)+vol['front_back_budget'][i] for i in [0,1]]
        main.append(f"| {vol['id']} | {vol['title']} | {', '.join(chapterlink(n) for n in vol['chapters'])} | {len(ss)} | {pages[0]}–{pages[1]} |\n")
    main+=['\nPage envelopes include the existing 24–40 pages of front/back material per volume and exclude substantial shared appendices/solutions. ',
           'They are estimates, not rendered lengths. Appendix A–F subjects and a common bibliography, glossary, symbol index and errata remain shared. ',
           'Volume I closes with global Chapter 14; global Chapter 48 precedes capstones in Volume IV; 49 closes IV and 50 closes V. A partial chapter bridge stays at its owning section and is reused later.\n\n',
           '## Writing order and batch exit targets\n\n',
           'This is the production order, not a new reader prerequisite chain. Later batch placement of a platform does not make it a prerequisite for earlier abstract compilation. ',
           '“Exit” below is a target to review, not a claim that the batch is complete.\n\n',
           '| Batch | Planned work | New sections | Inserted prerequisites | Exit target |\n|---|---|---|---|---|\n']
    for batch in batches:
        imported=', '.join(link(id) for id in batch['imported']) or 'None'
        main.append(f"| [{batch['id']}](writing-order.md#{batch['id'].lower()}) | {batch['title']} | {len(batch['new'])} | {imported} | {batch['exit']} |\n")
    main+=['\nBatch B06 explicitly inserts 10.7 (Pauli sums/grouping/shot allocation); B07 inserts 9.1, 9.2, 9.3 and 9.7 (the exact channel/semantics bridges). ',
           'These do not require completing the whole information volume first. Basic executor sections are written in B03 and complete Chapter 44 later in B16. ',
           'Finite logical memory is written in B11; only its resource-interpretation section waits for B12.\n\n',
           '## Fixed section-depth contract\n\n| Code | Sections | Required depth |\n|---|---|---|\n']
    for code,definition in p['depth_levels'].items():main.append(f"| {code} | {depth[code]} | {definition['requirement']} |\n")
    main+=['\nEach queue row links to its exact section specification; its result, assumptions, local bridge and deferred ingredients remain in the [detailed proof plans](proof-plan.md). ',
           'These are minimum obligations, not a request to prove every generalization or to turn a physical postulate into a theorem.\n\n',
           '## Start a section\n\n']
    for i,item in enumerate(b['section_start_checks'],1):main.append(f'{i}. {item}\n')
    main+=['\n## Accept a section and a batch\n\n']
    for i,item in enumerate(b['section_acceptance'],1):main.append(f'{i}. {item}\n')
    main+=['\nA draft may use an explained, convention-consistent earlier draft while both remain in review. Publication requires the route’s prerequisite sections and each released section to be accepted. ',
           'A batch exits drafting when its sections form a continuous working route; it exits acceptance only when the required independent reviews, integrated example, problem answers and web/print checks pass. ',
           'Do not fabricate a reviewer, reader trial or successful run to advance a status.\n\n',
           '## Local risks rather than a global research backlog\n\n| Item | Writing decision |\n|---|---|\n',
           '| Unchecked theorem details | Inspect only the exact theorem required for the current section; resolve a central proof uncertainty before claiming the result. Other batches continue. |\n',
           '| Missing FlagQuantum API | Write the mathematics and independent reference, investigate the actual call and track a confirmed upstream gap. Keep framework execution explicitly pending. |\n',
           '| H2 original author integral files | Use the checked STO-6G reconstruction at published precision and disclose the provenance limit in 49; no renewed search is a baseline prerequisite. |\n',
           '| Contested topological-device interpretation | Retain the existing audit as reference. Use a bounded dated claim or omit the optional disputed example in 40.7; do not resume a standalone paper investigation. |\n',
           '| Specialist/reader workload and print calibration | Collect evidence on the authored section/batch. Do not label an untested draft accepted or require all seven volumes to pass before starting Chapter 1. |\n\n',
           '## Change control\n\n']
    for item in b['change_policy']:main.append('- '+item+'\n')
    main+=['\nUse [the baseline-change record template](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/templates/baseline-change.md) for an intentional revision. ',
           'The initial decision record is [in the repository](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/baseline-changes/v1.0.md). ',
           'Automated checks verify scope/coverage/order; they do not supply scientific or educational sign-off.\n']
    order=['# Full writing queue\n\n',f"**{b['id']} · 435 sections · 16 batches.** [Baseline and acceptance](writing-baseline.md) · [First chapter briefs](writing-first-batch.md).\n\n",
           'Queue order is dependency-safe; an inserted prerequisite is written before its first consumer. A section appears once even when multiple batches target its chapter. ',
           'The state is actual recorded work, not a declaration of mathematical or implementation acceptance. Body paths in the machine queue are planned destinations; the existing three starters are expanded/migrated only when their turn arrives, preserving old public URLs.\n\n']
    for batch in batches:
        order += [f"<span id=\"{batch['id'].lower()}\"></span>\n\n## {batch['id']}: {batch['title']}\n\n",
                  f"**Exit target:** {batch['exit']}\n\n| Order | Section and exact plan | Depth | Direct prerequisites | Role | Work state |\n|---|---|---|---|---|---|\n"]
        for row in queue:
            if row['batch']!=batch['id']:continue
            id=row['section_id'];deps=', '.join(link(x) for x in row['requires']) or 'Entry/local bridge'
            order.append(f"| {row['sequence']} | {link(id)} {row['title']} | [{row['depth']}]({sections[id]['proof_link']}) | {deps} | {row['role']} | {row['state']} |\n")
        order.append('\n')
    first=['# First writing assignment: Chapter 1\n\n',f"**{b['id']} · six briefs prepared; no chapter body or execution claim.** [Writing baseline](writing-baseline.md) · [Full queue](writing-order.md).\n\n",
           'Write 1.1 first, then 1.2–1.6. Chapter 1 is an entry and preview: it must supply its own minimal arithmetic and notation without importing unproved results from later chapters. ',
           'The formal mathematics, state postulates, gates and measurement theory will be developed in their named owning chapters. The preview must say what is being adopted and what will be derived later.\n\n']
    for row in brief['sections']:
        id=row['section_id'];first += [f"## {row['ref']} {row['title']}\n\n",f"**Stable ID:** `{id}`. **Depth:** {row['depth']}. **State:** {progress['sections'][id]['state']}.\n\n"]
        for label,key in [('Concrete question','question'),('Entry knowledge','entry'),('Exit skill','exit'),('Worked-case plan','worked_case'),('Scope/continuity boundary','boundary'),('Formula-to-code plan','code_plan'),('Independent check','independent_check'),('Transfer task','transfer_task')]:first.append(f"**{label}:** {row[key]}\n\n")
        first.append('**Assigned exact sources:** '+', '.join(f"[{k}](references/proof-sources.md#source-{re.sub('[^a-z0-9]+','-',k.lower()).strip('-')})" for k in row['source_locators'])+'. Source assignment is not independent proof review.\n\n')
    output={'docs/writing-baseline.md':''.join(main),'docs/writing-order.md':''.join(order),'docs/writing-first-batch.md':''.join(first),
            'book/writing-queue.json':json.dumps(dict(baseline=b['id'],scope_sha256=b['scope_sha256'],sections=queue),indent=2,ensure_ascii=False)+'\n'}
    return output,dict(baseline=b['id'],chapters=len(chapters),sections=len(queue),batches=len(batches),states=dict(counts),scope_sha256=b['scope_sha256'])


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs,stats=build();stale=[path for path,text in outputs.items() if not (ROOT/path).exists() or (ROOT/path).read_text()!=text]
    if args.check:
        if stale:raise SystemExit('Stale writing baseline views: '+', '.join(stale))
    else:
        for path,text in outputs.items():(ROOT/path).write_text(text)
    print(json.dumps(stats))
if __name__=='__main__':main()
