#!/usr/bin/env python3
"""Check limited mathematical counterexamples used in the source-planning audit.

Synthetic data only: does not run TGP, load device measurements or validate a phase.
"""
import argparse
import json
from pathlib import Path


def audit():
    # Reversed indices represent negative voltage only on a reflected grid.
    bias = [-3, -2, -1, 0, 1, 2]
    even_signal = [v*v for v in bias]
    reversed_odd = [(a-b)/2 for a,b in zip(even_signal, reversed(even_signal))]
    assert reversed_odd[bias.index(0)] == -0.5
    cropped = bias[1:]
    assert all(a == -b for a,b in zip(cropped, reversed(cropped)))
    assert all((a*a-b*b)/2 == 0 for a,b in zip(cropped, reversed(cropped)))

    # A retained point can change threshold class when the normalising range changes.
    signal_at_point = 0.4
    full_threshold = 0.05 * 10
    cropped_threshold = 0.05 * 6
    assert signal_at_point < full_threshold and signal_at_point > cropped_threshold
    # No physical Hamiltonian, temperature or state has changed in this example.

    tp, fp, tn, fn = 90, 10, 990, 10
    fdr, fpr = fp/(tp+fp), fp/(fp+tn)
    assert fdr == 0.1 and fpr == 0.01
    # A region can contain a qualifying point without every point qualifying.
    region = [False, True, False]
    assert any(region) and not all(region) and not region[0]

    # Pairwise relation can hold although the local component is not even.
    voltages = [-2, -1, 0, 1, 2]
    local = lambda v: 2+0.1*v
    nonlocal_ = lambda v: 0.3-0.1*v
    assert local(1) != local(-1)
    assert all(abs(local(v)+nonlocal_(v)-local(-v)-nonlocal_(-v)) < 1e-12 for v in voltages)
    return dict(scope='Five synthetic logical checks; no device data, TGP reproduction or topological diagnosis',
                checks_passed=5,
                asymmetric_grid_false_odd_at_zero=-0.5,
                threshold_at_fixed_point={'signal':signal_at_point,'full_range':full_threshold,'cropped_range':cropped_threshold},
                confusion_matrix={'TP':tp,'FP':fp,'TN':tn,'FN':fn,'FDR':fdr,'FPR':fpr},
                existential_region_is_not_pointwise_certificate=True,
                pairwise_conductance_relation_does_not_require_even_local_trace=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    report=audit()
    if args.write:
        target=Path(__file__).resolve().parents[1]/'book/verification/topology-logic.json'
        target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    main()
