#!/usr/bin/env python3
"""Validate the planning overlay and render its curriculum-to-skill catalog.

This checks coverage and references, not agent behavior or scientific acceptance.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]


def render():
    plan=json.loads((ROOT/'book/agent-skills-plan.json').read_text())
    curriculum=json.loads((ROOT/'book/curriculum.json').read_text())
    baseline=json.loads((ROOT/'book/writing-baseline.json').read_text())
    progress=json.loads((ROOT/'book/writing-progress.json').read_text())['sections']
    assert plan['curriculum_baseline']==baseline['id']
    assert plan['curriculum_scope_sha256']==baseline['scope_sha256']
    assert plan['status']=='prototype-pilot' and plan['released_skills']==0
    for path in plan['entry_points'].values():assert (ROOT/path).is_file(),path
    chapters={c['number']:(p,c) for p in curriculum['parts'] for c in p['chapters']}
    section_map={s['id']:(p,c,i,s) for p in curriculum['parts'] for c in p['chapters'] for i,s in enumerate(c['sections'],1)}
    assert len(chapters)==50 and len(section_map)==435
    skills={s['id']:s for s in plan['skills']}
    assert len(skills)==len(plan['skills'])
    levels={l['id']:l for l in plan['levels']}
    assert list(levels)==[f'L{i}' for i in range(6)]
    owners={}
    for skill in skills.values():
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',skill['id']) and len(skill['id'])<64
        assert skill['level'] in levels and skill['independent_acceptance']=='pending'
        if skill['id']=='compare-quantum-states-and-operators':
            assert skill['status']=='independent-agent-tested prototype'
            assert skill['behavioral_evaluation']=='blind agent retest: 11/11; author helper regression: 45/45'
            assert (ROOT/skill['prototype_package']).is_file()
            report=json.loads((ROOT/skill['evaluation_report']).read_text())
            assert report['passed']==45 and report['independent_agent_forward_test']=='not run'
            assert report['independent_acceptance']=='pending'
            assert report['counts']=={'normal':11,'boundary':7,'error':21,'transfer-regression':6}
            assert all(c['passed'] for c in report['cases']) and len(report['cases'])==45
            blind=json.loads((ROOT/skill['blind_evaluation_report']).read_text())
            assert blind['current_version']==skill['package_version']=='0.1.1'
            assert blind['fresh_retest_tasks']==blind['fresh_retest_passed']==11
            assert blind['initial_nonconforming_helper_calls']==14
            assert blind['scientific_acceptance']=='pending' and blind['released_skills']==0
        elif skill['id']=='reproduce-qubit-interference':
            assert skill['status']=='independent-agent-tested prototype'
            assert skill['behavioral_evaluation']=='blind agent tasks: 12/12; author cases: 35/35'
            assert (ROOT/skill['prototype_package']).is_file()
            author=json.loads((ROOT/skill['evaluation_report']).read_text())
            blind=json.loads((ROOT/skill['blind_evaluation_report']).read_text())
            assert author['version']==blind['version']==skill['package_version']=='0.1.0'
            assert author['passed']==35 and author['actual_flagquantum_circuits']==167
            assert all(c['passed'] for c in author['cases']) and len(author['cases'])==35
            assert blind['new_tasks']==blind['passed_tasks']==12 and blind['agents']==3
            assert blind['actual_flagquantum_circuits']==18 and blind['scientific_acceptance']=='pending'
        elif skill['id']=='translate-unitary-evolution':
            assert skill['status']=='independent-agent-tested prototype'
            assert skill['behavioral_evaluation']=='blind agent tasks: 12/12; author cases: 53/53'
            assert (ROOT/skill['prototype_package']).is_file()
            author=json.loads((ROOT/skill['evaluation_report']).read_text())
            blind=json.loads((ROOT/skill['blind_evaluation_report']).read_text())
            assert author['version']==blind['version']==skill['package_version']=='0.1.0'
            assert author['passed']==53 and author['actual_flagquantum_circuits']==258
            assert all(c['passed'] for c in author['cases']) and len(author['cases'])==53
            assert blind['new_tasks']==blind['passed_tasks']==12 and blind['agents']==3
            assert blind['actual_flagquantum_circuits']==56 and blind['scientific_acceptance']=='pending'
        elif skill['id']=='translate-complex-linear-algebra':
            assert skill['status']=='independent-agent-tested prototype'
            assert skill['behavioral_evaluation']=='fresh blind retest: 9/9; author cases: 57/57'
            assert (ROOT/skill['prototype_package']).is_file()
            author=json.loads((ROOT/skill['evaluation_report']).read_text())
            blind=json.loads((ROOT/skill['blind_evaluation_report']).read_text())
            assert author['version']==blind['version']==skill['package_version']=='0.1.1'
            assert author['passed']==57 and author['actual_flagquantum_circuits']==0
            assert all(c['passed'] for c in author['cases']) and len(author['cases'])==57
            assert blind['new_tasks']==blind['passed_tasks']==9 and blind['agents']==3
            assert blind['algebra_quantum_circuits']==0 and blind['routed_flagquantum_circuits']==0
            assert blind['scientific_acceptance']=='pending'
        else:
            assert skill['status']=='planned' and skill['behavioral_evaluation']=='not run'
        assert len(skill['primary_section_ids'])==len(set(skill['primary_section_ids']))
        for sid in skill['primary_section_ids']:
            assert sid in section_map and sid not in owners,(sid,'invalid or duplicate owner')
            owners[sid]=skill['id']
        for sid in skill['support_section_ids']:assert sid in section_map,sid
        for dep in skill['requires_skills']:
            assert dep in skills and dep!=skill['id']
            assert int(skills[dep]['level'][1:])<=int(skill['level'][1:]),dep
        for path in skill['candidate_evidence']:assert (ROOT/path).is_file(),path
    assert set(owners)==set(section_map),'Missing primary section assignment'
    seen,stack=set(),set()
    def visit(ident):
        assert ident not in stack,('Skill dependency cycle',ident)
        if ident in seen:return
        stack.add(ident)
        for dep in skills[ident]['requires_skills']:visit(dep)
        stack.remove(ident);seen.add(ident)
    for ident in skills:visit(ident)
    mapping={m['chapter']:m for m in plan['chapter_map']}
    assert len(mapping)==len(plan['chapter_map'])==50
    for number,(_,ch) in chapters.items():
        m=mapping[number]
        assert m['chapter_id']==ch['id']
        assert m['section_ids']==[s['id'] for s in ch['sections']]
        assert m['primary_skill_ids']==sorted({owners[s['id']] for s in ch['sections']})
    def source(sid):
        part,ch,i,_=section_map[sid]
        return f"[{ch['number']}.{i}](section-plans/{part['path']}.md#{sid})"
    states=Counter(progress.get(sid,{}).get('state','not_started') for sid in section_map)
    lines=['# Agent skills: capability levels and chapter map','',
           f'**Plan 0.1 · October 21, 2026 · first prototype pilot.** Generated from `book/agent-skills-plan.json`. This catalog contains {len(skills)} proposed task skills; four have independent-agent-tested prototypes: state/operator comparison 0.1.1, single-qubit interference 0.1.0, phase-tracked unitary evolution 0.1.0 and complex linear algebra 0.1.1. Their separate evidence records retain failures, author execution and blind-task outcomes. Scientific acceptance remains pending. Zero skills are released. It does not assert existing FlagQuantum support for planned topics.','',
           '[Dual-entry design](dual-entry.md) · [Skill contract](skill-contract.md) · [Paper verification and acceptance](paper-reproduction-standard.md)','',
           '## Capability levels','',
           'Levels describe increasing task composition and evaluation scope. They do not replace the textbook P/F/M/R/V proof-depth codes, its prerequisite graph, or evidence-based competence in a domain. An L5 router does not certify every L2 workflow.','',
           '| Level | Capability | Required evidence |','|---|---|---|']
    for level in levels.values():lines.append(f"| {level['id']}: {level['title']} | {level['capability']} | {level['exit_evidence']} |")
    lines+=['','## Complete chapter-to-skill mapping','',
            f"All **50 chapters and 435 sections** have one primary task-family assignment in the JSON catalog. Current source states: {states['draft']} drafts, {states['not_started']} not started, {states['accepted']} accepted. A draft with checked examples is useful prototype evidence, not a released skill.",'',
            'The primary owner is an editorial responsibility, not exclusive use or a claim that every section already implements the task. Support references and selected domain workflows create many-to-many reuse. Source links below lead to stable planning anchors; a planned section must not be presented as completed prose.','',
            '| Chapter and canonical section range | Primary task skill(s) | Source drafts / sections |','|---|---|---|']
    for number,(part,ch) in chapters.items():
        refs=f"{number}.1–{number}.{len(ch['sections'])}"
        linked=f"[{number}. {ch['title']}](section-plans/{part['path']}.md#{ch['id']})"
        ids=mapping[number]['primary_skill_ids']
        labels='; '.join(f"[{ident}](#{ident})" for ident in ids)
        drafted=sum(progress.get(s['id'],{}).get('state')=='draft' for s in ch['sections'])
        lines.append(f"| {linked} ({refs}) | {labels} | {drafted} / {len(ch['sections'])} |")
    lines+=['','## Task catalog and dependency contracts','',
            'Each proposed package must expose a bounded task/profile before implementation. Broad domain entries may be split into narrower packages after pilot evidence; this does not alter textbook chapters. Load the specific profile and mathematical references needed for a run rather than all domain material.','',
            'The declared skill graph is acyclic. A run must additionally name its selected domain profiles, direct and transitive textbook prerequisites, and concrete versions. L3–L5 orchestration may select relevant L2 skills; it must not treat an unlisted domain requirement as satisfied.','']
    for skill in skills.values():
        lines +=[f"### {skill['id']}",'',f"**{skill['level']} · {skill['status']} · {skill['behavioral_evaluation']} · independent acceptance pending.**",'',skill['task'],'',f"**Deliverable:** {skill['deliverable']}"]
        if skill['id']=='compare-quantum-states-and-operators':
            lines += ['', '[Prototype usage](comparison-skill-prototype.md) · [Independent blind evaluation and runtime repair](comparison-skill-blind-evaluation.md).']
        elif skill['id']=='reproduce-qubit-interference':
            lines += ['', '[Interference prototype, formula-to-code contract and independent blind evaluation](interference-skill-prototype.md).']
        elif skill['id']=='translate-unitary-evolution':
            lines += ['', '[Unitary evolution prototype, units, phase contract and independent blind evaluation](unitary-evolution-skill-prototype.md).']
        elif skill['id']=='translate-complex-linear-algebra':
            lines += ['', '[Complex linear algebra prototype, numerical contracts and independent blind evaluation](complex-algebra-skill-prototype.md).']
        deps=', '.join(f"[{dep}](#{dep})" for dep in skill['requires_skills']) or 'None at catalog level; this does not waive source prerequisites.'
        lines +=['',f'**Required task skills:** {deps}']
        grouped={}
        for sid in skill['primary_section_ids']:
            _,ch,idx,_=section_map[sid];grouped.setdefault(ch['number'],[]).append((sid,idx))
        parts=[]
        for number,items in grouped.items():
            if len(items)==len(chapters[number][1]['sections']):
                part,ch=chapters[number];parts.append(f"[Chapter {number}, all sections](section-plans/{part['path']}.md#{ch['id']})")
            else:parts.extend(source(sid) for sid,_ in items)
        lines+=['','**Primary sources:** '+('; '.join(parts) if parts else 'Cross-cutting orchestration; no primary section ownership. See support references and the selected run profile.')]
        if skill['support_section_ids']:lines+=['','**Support sources:** '+', '.join(source(sid) for sid in skill['support_section_ids'])]
        if skill['candidate_evidence']:
            refs='; '.join(f"[{Path(path).name}](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/{path})" for path in skill['candidate_evidence'])
            lines+=['','**Existing candidate evidence:** '+refs+'. These artifacts are not a skill evaluation, an acceptance decision or a whole-paper reproduction claim.']
        lines+=['']
    lines+=['## Implementation order after this planning pass','',
            '1. Preserve the [state/operator blind evaluation](comparison-skill-blind-evaluation.md): 0.1.1 passed 11 fresh tasks after a runtime-contract repair. Gather separate scientific acceptance and reader evidence; published cases are now regression fixtures.',
            '2. Preserve the [interference prototype evidence](interference-skill-prototype.md): 35 author cases and 12 new blind-agent tasks passed, including units, analyzer signs, chronology, claim rejection and selection between two runnable skills. Scientific acceptance remains separate.',
            '3. Preserve the [phase-tracked unitary evolution evidence](unitary-evolution-skill-prototype.md): 53 author cases and 12 blind tasks passed, covering units, generator validation, Euler endpoints, controlled phase repair and selection among three skills. Scientific acceptance remains pending.',
            '4. Preserve the [complex linear algebra evidence](complex-algebra-skill-prototype.md): 57 author cases and nine fresh blind retest tasks passed after a tail-metadata underflow repair. Preserve the initial 12-task evidence and original failure; classical and routed FlagQuantum executions are recorded separately. Scientific acceptance remains pending.',
            '5. Establish per-claim evidence bundling and a fresh-workspace rerun. Extend the existing molecular case only after the integral-to-model provenance and the chosen paper targets are explicitly contracted.',
            '6. Add L2 workflows as their source obligations and genuine APIs are authored and verified. Evaluate L4 on a registered multi-claim case, then L5 on held-out papers with separately reported domain coverage.', '',
            'This order concerns future skill prototypes. It does not reorder the frozen 16 textbook writing batches, start a new chapter, or label a prototype accepted. The first four bounded prototypes are independent-agent-tested; no paper run or new textbook section is performed by this update.','']
    return '\n'.join(lines),len(skills)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    content,count=render();out=ROOT/'docs/agent-skills.md'
    if args.check:
        assert out.exists() and out.read_text()==content,'Regenerate docs/agent-skills.md'
    else:out.write_text(content)
    print(f'Validated {count} catalog skills / 6 levels / 50 chapters / 435 section assignments; no released skills.')

if __name__=='__main__':main()
