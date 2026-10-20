"""Render and validate claim-level authoring evidence (called by scholarly builder)."""
import hashlib
import json
import re


def build(root, sources, section_refs):
    ledger = json.loads((root / 'book/source-evidence.json').read_text())
    report = json.loads((root / 'book/verification/h2-provenance.json').read_text())
    table = root / 'examples/omalley2016/h2-table.csv'
    assert report['input_table_sha256'] == hashlib.sha256(table.read_bytes()).hexdigest()
    assert report['coefficient_count'] == 324 and len(report['rows']) == 54
    assert report['max_coefficient_residual_hartree'] <= report['tolerance_hartree'] == 0.00005
    assert len(ledger['h2']) == 9 and len(ledger['topology']) == 9
    assert len({r['id'] for k in ['h2', 'topology'] for r in ledger[k]}) == 18
    for kind in ['h2', 'topology']:
        for row in ledger[kind]:
            assert row['sections'] and all(ref in section_refs for ref in row['sections'])
            assert row['source_locators'] and all(k in sources['locators'] for k in row['source_locators'])
            assert all(str(v).strip() for v in row.values())
            works = {sources['locators'][k]['work'] for k in row['source_locators']}
            if 'Z2018' in works:
                assert 'ZR2021' in works and 'RETRACTED' in row['status']
    experiment_works = {sources['locators'][k]['work'] for r in ledger['topology'] for k in r['source_locators']}
    assert {'L2026', 'MR2026', 'N2020', 'G2023', 'I2024', 'F2024', 'K2026'} <= experiment_works

    def links(row):
        return ', '.join('['+k+'](proof-sources.md#source-'+re.sub('[^a-z0-9]+', '-', k.lower()).strip('-')+')' for k in row['source_locators'])
    def sections(row):
        return ', '.join(f'[{r}](../{section_refs[r]})' for r in row['sections'])
    header = f"**Checked {ledger['revision']} · authoring specification, not chapter body.** {ledger['scope']}\n\n"
    h = ['# H₂: integral-to-reduced-model provenance plan\n\n', header,
         '[All-section proof plan](../proof-plan.md) · [Topological experiment ledger](topological-experiments.md) · [Exact source catalogue](proof-sources.md)\n\n',
         '## Source chain and acceptance obligations\n\n']
    for row in ledger['h2']:
        h += [f"### {row['id']}: {row['claim']}\n\n",
              f"**Owning sections:** {sections(row)}. **Sources:** {links(row)}.\n\n",
              f"**Checked:** {row['verified']}\n\n", f"**Authoring acceptance:** {row['acceptance']}\n\n"]
    h += ['## Independent numerical audit\n\n',
          'The repository verification tool constructs creation/annihilation matrices and the BK basis permutation independently of the coefficient table. ',
          'It checks all 15 terms of the four-qubit Pauli expansion before projection, the analytic six-integral bridge, absent reduced Pauli coefficients, removed-Z commutators, fixed-N=2 spectrum and coefficient-rounding energy bound. ',
          'It does not execute a new FlagQuantum implementation or claim recovery of original author integral files.\n\n',
          f"- Coverage: {report['coefficient_count']} coefficients at 54 geometries.\n",
          f"- Maximum absolute coefficient residual: {report['max_coefficient_residual_hartree']:.12g} Hartree; tolerance 0.00005 Hartree, half the last printed decimal.\n",
          '- STO-3G counterexample at 0.75 angstrom differs from Table I by more than 0.007 Hartree in an individual coefficient.\n',
          '- Historical Seeley Table III fixture is checked separately at 1.401 bohr, within its six-decimal reporting precision.\n\n',
          '| R (angstrom) | Regenerated total N=2 energy (Hartree) | Rounded-table energy (Hartree) | Maximum coefficient residual (Hartree) |\n|---|---|---|---|\n']
    for row in report['rows']:
        if row['R_angstrom'] in [.75, 1., 2.85]:
            h.append(f"| {row['R_angstrom']:.2f} | {row['exact_two_electron_energy_hartree']:.10f} | {row['rounded_table_energy_hartree']:.10f} | {row['max_coefficient_residual_hartree']:.6g} |\n")
    env=report['environment']
    h += ['\nRecorded environment: '+', '.join(f'{k} {env[k]}' for k in ['python','pyscf','numpy','scipy','h5py'])+'. CPU, macOS ARM64. Linux CI repeats the invariant/tolerance checks; exact floating-point bits are not prescribed.\n\n',
          'Verification tooling and machine-readable records: [script](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/scripts/verify_h2_provenance.py), ',
          '[pinned audit dependencies](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/requirements-provenance.txt), ',
          '[54-row audit report](https://github.com/FlagQuantum/modern-quantum-computing/blob/main/book/verification/h2-provenance.json). ',
          'These optional chemistry dependencies are separate from the FlagQuantum examples environment.\n\n',
          '```bash\npython3 -m venv .venv-provenance\n.venv-provenance/bin/python -m pip install -r requirements-provenance.txt\nOMP_NUM_THREADS=1 .venv-provenance/bin/python scripts/verify_h2_provenance.py\n```\n\n',
          'The command asserts the physical/numerical contracts and prints the coefficient count, maximum residual and tolerance. It leaves the checked-in report unchanged; an intentional new audit can use `--write`.\n\n',
          '## Software-method sources\n\n',
          'Integral notation is checked against the official [PySCF ao2mo documentation](https://pyscf.org/pyscf_api_docs/pyscf.ao2mo.html) and [AO-to-MO guide](https://pyscf.org/contributor/ao2mo_developer.html). ',
          'The [PySCF 2.10.0 source](https://github.com/pyscf/pyscf/tree/v2.10.0) pins the implementation; [BSE STO-family notes](https://www.basissetexchange.org/family_notes/sto/) identify the basis origin. ',
          'The mathematical proof, first-use explanation and reader acceptance gates remain pending.\n']
    t = ['# Topological routes: primary experimental evidence ledger\n\n',header,
         '[Chapter 40 proof plan](../proof-plans/physical-platforms.md#chapter-40-topological-quantum-computation-and-candidate-physical-realizations) · [H₂ provenance plan](h2-provenance.md) · [Exact sources](proof-sources.md)\n\n',
         '## Claim-specific experiments and source status\n\n',
         'The same word “braiding” occurs in different physical and encoded settings. Each entry below specifies which observable and interpretation the selected source can support. ',
         'A proposed theoretical operation, simulated ideal model, experimental signature and demonstrated logical protection have separate acceptance obligations.\n\n']
    for row in ledger['topology']:
        t += [f"### {row['id']}: {row['claim']}\n\n",
              f"**Owning sections:** {sections(row)}. **Sources:** {links(row)}.\n\n",
              f"**Observation / source target:** {row['observation']}\n\n",
              f"**Attributed interpretation:** {row['interpretation']}\n\n",
              f"**Not established by this source:** {row['not_established']}\n\n",
              f"**Data / access scope:** {row['data']}\n\n",
              f"**Status checked {ledger['revision']}:** {row['status']}\n\n"]
    t += ['## Acceptance before drafting and release\n\n']
    for x in ledger['topology_acceptance']:t.append('- '+x+'\n')
    t += ['\nNo experimental data analysis is claimed by this planning pass. Citations and source-status checks do not establish a device’s topological phase or logical error protection. ',
          'Original papers, figures and raw datasets are linked rather than redistributed. The section-level mathematical review remains pending.\n']
    return {'docs/references/h2-provenance.md': ''.join(h), 'docs/references/topological-experiments.md': ''.join(t)}
