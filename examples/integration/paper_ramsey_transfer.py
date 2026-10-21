#!/usr/bin/env python3
"""Scoped ideal-claim transfer from arXiv:1608.04908v1, not a new skill."""
import argparse
import cmath
import json
import math
from pathlib import Path
from four_skill_interference import run, encode

SOURCE = "https://arxiv.org/pdf/1608.04908v1"
SOURCE_AXIS = [0, 0.23, 0.5, 1, 1.37, 2]


def request(axis, generator=None, seconds=0):
    """Caller-selected full-coordinate convention: g=0, e=1, H2=H Z."""
    return dict(
        profile="constant-qubit-interference",
        generator=dict(matrix=encode(generator or [[0, 0], [0, 0]]), unit="rad/s"),
        time=dict(value=seconds, unit="s"),
        initial_state=encode([1/math.sqrt(2), 1/math.sqrt(2)]),
        basis=["0", "1"],
        phase_scan=dict(values=[math.pi*x for x in axis], unit="radian"),
        analyzer=dict(delta=math.pi, unit="radian"),
        tolerance=dict(coordinate_atol=1e-10, rtol=0),
        phase_context="full-coordinates-with-controlled-witness",
    )


def independent_check(report, phases, scalar_phase=0):
    """Scalar complex arithmetic; no helper/backend exponential as oracle."""
    assert report["status"] == "verified", report
    assert len(report["outputs"]) == len(phases)
    worst = 0.0
    for item, phi in zip(report["outputs"], phases):
        phase = cmath.exp(1j*phi)
        v = [cmath.exp(-1j*scalar_phase)*(1-phase)/2,
             cmath.exp(-1j*scalar_phase)*(1+phase)/2]
        p = [(1-math.cos(phi))/2, (1+math.cos(phi))/2]
        actual = [complex(*z) for z in item["statevector"]]
        staged = [complex(*z) for z in item["staged_statevector"]]
        errors = [abs(a-b) for a,b in zip(actual, v)]
        errors += [abs(a-b) for a,b in zip(staged, v)]
        errors += [abs(a-b) for a,b in zip(item["probabilities"], p)]
        worst = max(worst, *errors)
    assert worst <= 1e-10, worst
    return worst


def execute(output, skills):
    output = Path(output)
    output.mkdir(exist_ok=False, parents=True)
    baseline = run(request(SOURCE_AXIS), output/"source-vacuum", skills)
    baseline_error = independent_check(baseline, [math.pi*x for x in SOURCE_AXIS])
    # Explicit caller extension, not a pulse duration/frequency quoted by the paper.
    seconds = 0.83e-9
    omega = 2*math.pi*125e6
    offset = 0.17/seconds
    extended = run(request([0], [[offset,0],[0,offset-omega]], seconds),
                   output/"caller-extension", skills)
    extension_error = independent_check(extended, [omega*seconds], scalar_phase=0.17)
    result = dict(
        experiment="liu2016-vacuum-ramsey-transfer", source=SOURCE,
        status="verified_in_declared_ideal_scope",
        source_target="vacuum-WPD ideal ground-state probability only",
        basis=["g=0", "e=1"],
        pulse_convention="H1=Ry(pi/2), H2=Ry(pi/2)=H Z; chosen compatible ideal completion, not uniquely reconstructed laboratory pulses",
        source_axis=SOURCE_AXIS,
        probabilities_g=[r["probabilities"][0] for r in baseline["outputs"]],
        caller_extension_probability_g=extended["outputs"][0]["probabilities"][0],
        worst_coordinate_or_probability_error=max(baseline_error,extension_error),
        actual_flagquantum_circuits=baseline["actual_flagquantum_circuits"]+extended["actual_flagquantum_circuits"],
        helper_calls=len(baseline["helper_calls"])+len(extended["helper_calls"]),
        quantum_cavity_simulated=False, hardware_data_compared=False,
        scientific_acceptance="pending", reader_trial="not run", new_skills=0,
    )
    (output/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skills-root", type=Path, default=Path("skills"))
    args = parser.parse_args()
    result = execute(args.output, args.skills_root.resolve())
    print("source p_g:", " ".join(f"{p:.9f}" for p in result["probabilities_g"]))
    print(f"caller extension p_g: {result['caller_extension_probability_g']:.9f}")
    print("actual FlagQuantum circuits:", result["actual_flagquantum_circuits"])
    print("scientific acceptance:", result["scientific_acceptance"])
