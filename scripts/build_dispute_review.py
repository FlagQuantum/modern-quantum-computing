"""Validate and render the version-specific topology-controversy planning audit."""
import json
import re
from verify_topology_logic import audit


def build(root, sources):
    plan=json.loads((root/'book/topology-dispute.json').read_text())
    assert len(plan['versions'])==6 and len(plan['issues'])==9
    assert len({x['id'] for x in plan['issues']})==9
    for group in ['versions','issues']:
        for row in plan[group]:
            assert row['source_locators'] and all(k in sources['locators'] for k in row['source_locators'])
            assert all(str(v).strip() for v in row.values())
    assert {x['id'] for x in plan['issues']}=={f'D{i}' for i in range(1,10)}
    assert 'not retrieved' in plan['versions'][-1]['access']
    assert audit()==json.loads((root/'book/verification/topology-logic.json').read_text())
    def refs(row):
        return ', '.join('['+k+'](proof-sources.md#source-'+re.sub('[^a-z0-9]+','-',k.lower()).strip('-')+')' for k in row['source_locators'])
    out=['# Topological parity-readout controversy: version and argument audit\n\n',
         f"**Checked {plan['revision']} · planning only.** {plan['scope']}\n\n",
         '[Experimental evidence ledger](topological-experiments.md) · [Chapter 40 proof plan](../proof-plans/physical-platforms.md#chapter-40-topological-quantum-computation-and-candidate-physical-realizations) · [Exact sources and hashes](proof-sources.md)\n\n',
         '## Accessed versions and identity boundaries\n\n',
         'The full public comment, early response and later rebuttals have different roles. The accepted manuscript is identified by the university record, title/author and matching journal DOI; ',
         'the [institutional record](https://research-portal.st-andrews.ac.uk/en/publications/on-the-robustness-of-topological-gap-detection-via-transport/) contains an unrelated 2025 DOI in its rights boilerplate, which is not used to identify the comment. ',
         'The standard portal file URL returned an access challenge; the university’s public legacy file endpoint supplied the licensed manuscript without login. No source PDFs or article figures are redistributed here.\n\n']
    for row in plan['versions']:
        out += [f"### {row['id']}: {row['label']}\n\n",
                f"[Public source]({row['url']}) · {refs(row)}.\n\n",
                f"**Access:** {row['access']}.\n\n",f"**Version relation:** {row['relation']}\n\n"]
    out += ['## Issue-by-issue authoring decisions\n\n',
            'The “assessment” entries are bounded editorial reasoning from the accessed sources. They separate acknowledged processing facts, competing physical interpretations and tests still required. ',
            'They do not certify the correctness of either side’s device model. Numbered reviewer positions below are attributed to the **Anonymous Referees** in the public joint review file and its stated review version.\n\n']
    for row in plan['issues']:
        out += [f"### {row['id']}: {row['title']}\n\n", f"**Exact targets:** {refs(row)}.\n\n",
                f"**Comment / challenge:** {row['challenge']}\n\n",f"**Response / qualification:** {row['response']}\n\n",
                f"**Editorial assessment:** {row['assessment']}\n\n",f"**Required before authoring acceptance:** {row['authoring_obligation']}\n\n",
                f"**Status:** {row['status']}.\n\n"]
    out += ['## Frozen data and analysis versions\n\n',
            'A dataset-family DOI and a specific version are different identifiers. Publisher checksums below come from the versioned file listings; they are not claimed as hashes of archives successfully downloaded in this pass.\n\n']
    for row in plan['data_versions']:
        out += [f"- **[{row['role']}]({row['url']}):** {row['version']}; `{row['artifact']}`. Publisher MD5: `{row['publisher_md5']}`. {row['access']}.\n\n"]
    out += ['The older Microsoft response reports changes below 5 microelectronvolts for more than 96% of pixels. ',
            'The later dataset description reports 4.6% of pixels changing classification. These measure different quantities and use different versions; neither percentage certifies small changes to connectivity or selected clusters.\n\n',
            '## Limited independent logic checks\n\n',
            'The [verification tool](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/scripts/verify_topology_logic.py) checks five synthetic counterexamples/invariants with the Python standard library: ',
            'bias-coordinate reflection, range-normalised threshold changes at a fixed point, FDR versus FPR, region-existence versus pointwise certification, and pairwise conductance symmetry versus an even local trace. ',
            'The conductance example checks the algebraic implication only, under the separately imported physical assumptions from Danon Eq. (1)–(8). It is not a fitted device signal.\n\n',
            'Run `python3 scripts/verify_topology_logic.py` from the repository root. ',
            '[Machine-readable results](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/verification/topology-logic.json) record all five checks. ',
            'No device data are loaded and no measured percentage, TGP map, RF fit or topological phase is reproduced.\n\n',
            '## Remaining acceptance gates\n\n']
    for gate in plan['release_gates']:out.append('- '+gate+'\n')
    return {'docs/references/topological-dispute-review.md':''.join(out)}
