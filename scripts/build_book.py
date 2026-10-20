#!/usr/bin/env python3
"""Build web metadata, a standalone LaTeX source bundle, and an optional PDF.

Requires Pandoc 3.12.1 and Tectonic 0.17.0 for the validated print build.
The chapter Markdown and the example Python files remain canonical.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "book/metadata.json").read_text())
OUT = ROOT / "output/pdf"
WORK = ROOT / "build/pdf"
STEM = "modern-quantum-computing"


def run(*args, **kwargs):
    return subprocess.run(args, check=True, text=True, **kwargs)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def tex(value):
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
                    "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}"}
    return "".join(replacements.get(c, c) for c in value)


def web_metadata():
    # Only this metadata block is generated; the surrounding introduction is prose.
    path = ROOT / "docs/index.md"
    text = path.read_text()
    block = ("<!-- book-metadata:start -->\n"
             f"**{META['author']}**\n\n{META['team']}\n\n{META['institution']}\n\n"
             f"{META['location']}\n\n**Version {META['version']} · {META['date']} · Draft**\n"
             "<!-- book-metadata:end -->")
    pattern = r"<!-- book-metadata:start -->.*?<!-- book-metadata:end -->"
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, lambda _: block, text, flags=re.S)
    else:
        text = text.replace("## Who this book is for", block + "\n\n## Who this book is for")
    path.write_text(text)


def chapter(path):
    text = path.read_text()
    # Preserve repository destinations when the source Markdown is rendered in PDF.
    def link(match):
        label, target = match.groups()
        if "://" in target or target.startswith("#"):
            return match.group(0)
        location, _, anchor = target.partition("#")
        relative = (path.parent / location).resolve().relative_to(ROOT)
        internal = {
            "docs/conventions.md": "notation-and-implementation-conventions",
            "docs/chapters/measurement.md": "measurement-and-expectation-values",
            "docs/chapters/gradients.md": "parameterized-circuits-and-gradients",
            "docs/chapters/vqe.md": "molecular-hydrogen-vqe-from-a-paper-to-code",
        }
        if relative.as_posix() in internal and not anchor:
            return f"[{label}](#{internal[relative.as_posix()]})"
        destination = f"{META['repository']}/blob/{git('rev-parse', 'HEAD')}/{relative.as_posix()}"
        if anchor:
            destination += "#" + anchor
        return f"[{label}]({destination})"
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    return text.replace("→", "to").replace("·", " / ")


def listing(relative):
    path = ROOT / relative
    return f"\n## `{relative}`\n\n```python\n{path.read_text().rstrip()}\n```\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--web-metadata", action="store_true", help="update the web author/version block")
    parser.add_argument("--tex-only", action="store_true", help="generate sources without running TeX")
    args = parser.parse_args()
    if args.web_metadata:
        web_metadata()
        return
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    commit = git("rev-parse", "HEAD")
    dirty = bool(git("status", "--porcelain", "--untracked-files=no"))
    # All transformed prose and listings are generated, never edited by hand.
    front = f"""# About this draft {{.unnumbered}}

This is a three-chapter sample of an open English textbook. It is not a complete course or an arXiv submission. The three sample chapters are drawn from different parts of the proposed curriculum.

The learning sequence is formula, derivation, FlagQuantum implementation, independent verification, and exercises. Numerical checks supplement mathematical arguments; they do not prove a general identity.

Author: **{META['author']}**. Affiliation: {META['team']}, {META['institution']}, {META['location']}.

Version: **{META['version']}**, dated {META['date']}. Source revision: `{commit}`. Tracked source changes at build time: `{str(dirty).lower()}`.

## Abstract

This sample connects quantum-computing formulas to executable and independently checked programs. A rotated qubit introduces probabilities and expectation values; a parameterized circuit illustrates analytic, automatic and parameter-shift differentiation; a two-qubit molecular hydrogen model demonstrates source-version selection, wire-order translation, variational energies and numerical verification. Examples target FlagQuantum {META['flagquantum_version']} using the PyTorch CPU backend and complex128 statevectors. The hydrogen case is an ideal calculation using rounded, corrected paper coefficients, not a reproduction of a physical hardware experiment.

## Reproduction environment

The examples were checked with Python 3.12.14, FlagQuantum 0.3.1, PyTorch 2.13.0, NumPy 2.5.4 and Matplotlib 3.11.2 on macOS ARM64 CPU. A separate Linux CI runs the example suite. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-examples.txt
python examples/measurement.py
python examples/gradients.py
python examples/omalley2016/verify_h2_vqe.py
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. No accelerator or physical hardware configuration is required for these examples.

## Sources, assistance and licensing

Original prose is CC BY 4.0; repository-authored code is MIT. Linked third-party works retain their own rights. The primary hydrogen calculation follows O'Malley et al. [@omalley_2016]; analytic quantum gradients are discussed by Schuld et al. [@schuld_gradients_2019]. General companion references appear in the bibliography and repository reading guide.

This draft was prepared with generative-AI assistance for prose, code and publication tooling. The named author is responsible for reviewing the mathematical claims, source attribution and executable results before scholarly submission. Automated checks and visual inspection are recorded with the release artifacts; they are not a claim of independent peer review.

Repository: <{META['repository']}>.

"""
    conventions = chapter(ROOT / "docs/conventions.md").replace("# Notation and implementation conventions", "# Notation and implementation conventions {.unnumbered}", 1)
    pieces = [front, conventions]
    for name, example in [("measurement", "examples/measurement.py"),
                          ("gradients", "examples/gradients.py"), ("vqe", None)]:
        text = chapter(ROOT / f"docs/chapters/{name}.md")
        text = re.sub(r"(?m)^## [1-9]\. ", "## ", text)
        if name == "measurement":
            text += "\nThe displayed rotation matrix is Equation~\\eqref{eq:print-1}.\n"
        if name == "gradients":
            text += "\nThe single-rotation shift rule is Equation~\\eqref{eq:print-2}.\n"
            text += "\nThe parameter-shift reading is cited as [@schuld_gradients_2019].\n"
        if name == "vqe":
            text += "\nEquations~\\eqref{eq:print-3} and~\\eqref{eq:print-4} define the Hamiltonian and ansatz; Equations~\\eqref{eq:print-5}--\\eqref{eq:print-7} give the energy, shift rule and analytic reference minimum.\n"
            text += "\nThe paper and corrected data source are cited as [@omalley_2016].\n"
        if example:
            text += "\n## Complete executable example\n" + listing(example)
        pieces.append(text)
    pieces.append("\\appendix\n\n# Hydrogen implementation and verification\n\nSave these two files in the same directory. The model embeds all 54 corrected table rows. Run `python verify_h2_vqe.py` after installing the pinned example requirements. The repository contains the additional scan, optimizer and sampling programs.\n")
    pieces += [listing("examples/omalley2016/h2_vqe_model.py"),
               listing("examples/omalley2016/verify_h2_vqe.py")]
    pieces.append("# References {#refs}\n")
    manuscript = WORK / "manuscript.md"
    manuscript.write_text("\n\n".join(pieces))
    cover = WORK / "cover.tex"
    cover.write_text(r"\begin{titlepage}\thispagestyle{empty}\centering" + "\n" +
        r"\vspace*{1.3cm}{\color{bookteal}\large OPEN TEXTBOOK / SAMPLE EDITION\par}\vspace{1.5cm}" + "\n" +
        r"{\color{booknavy}\Huge\bfseries Modern Quantum Computing\par}\vspace{0.6cm}" + "\n" +
        r"{\LARGE A Formula-to-Code Approach\par}\vspace{1cm}" + "\n" +
        r"{\large " + tex(META["subtitle"]) + r"\par}\vspace{1.6cm}" + "\n" +
        r"{\Large\bfseries " + tex(META["author"]) + r"\par}\vspace{0.4cm}" + "\n" +
        r"{\large " + tex(META["team"]) + r"\par " + tex(META["institution"]) + r"\par " + tex(META["location"]) + r"\par}" + "\n" +
        r"\vfill{\large Version " + tex(META["version"]) + r"\quad Draft\par}" + "\n" +
        tex(META["date"]) + r"\par\vspace{0.5cm}{\small Three starter chapters / FlagQuantum " + tex(META["flagquantum_version"]) + r"\par}\end{titlepage}\pagenumbering{arabic}" + "\n")
    output_tex = OUT / "book.tex"
    run("pandoc", str(manuscript), "--from=markdown", "--to=latex", "--standalone",
        "--top-level-division=chapter", "--number-sections", "--toc", "--listings", "--citeproc",
        "--metadata=nocite:@*", f"--metadata=author:{META['author']}",
        "--variable=documentclass:book", "--variable=classoption:oneside,openany",
        "--variable=fontsize:11pt", "--variable=papersize:a4", "--variable=geometry:margin=25mm",
        f"--include-in-header={ROOT / 'book/preamble.tex'}", f"--include-before-body={cover}",
        f"--lua-filter={ROOT / 'book/pdf.lua'}",
        f"--bibliography={ROOT / 'docs/references/references.bib'}", "--output", str(output_tex))
    # Start text after the contents on a clean page without suppressing chapter numbering.
    source = output_tex.read_text()
    source = source.replace(r"\hypersetup{", r"\hypersetup{pdftitle={" + tex(META["title"]) + "},", 1)
    output_tex.write_text(source)
    shutil.copy(ROOT / "docs/references/references.bib", OUT / "references.bib")
    instructions = OUT / "README.txt"
    instructions.write_text("Standalone source generated from the canonical Markdown and Python examples.\n"
        "Compile book.tex with Tectonic 0.17.0 or a compatible XeLaTeX toolchain.\n"
        "References and code listings are already embedded in book.tex.\n"
        f"Version: {META['version']}\nSource revision: {commit}\n"
        f"Tracked modifications at build time: {dirty}\n"
        "This is a sample draft, not a completed textbook or a submitted arXiv work.\n")
    if not args.tex_only:
        compiler = os.environ.get("TECTONIC", "tectonic")
        run(compiler, "--keep-logs", "--keep-intermediates", "--outdir", str(OUT), str(output_tex))
        shutil.copyfile(OUT / "book.pdf", OUT / f"{STEM}.pdf")
    files = [output_tex, OUT / "references.bib", instructions]
    if not args.tex_only:
        files.append(OUT / f"{STEM}.pdf")
    manifest = dict(META, source_commit=commit, tracked_modifications=dirty,
                    pandoc=subprocess.check_output(["pandoc", "--version"], text=True).splitlines()[0],
                    files={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with tarfile.open(OUT / f"{STEM}-source.tar.gz", "w:gz") as bundle:
        for p in [output_tex, OUT / "references.bib", instructions, OUT / "manifest.json"]:
            bundle.add(p, arcname=p.name)
    print(f"Built source bundle{' and PDF' if not args.tex_only else ''} under {OUT}")


if __name__ == "__main__":
    main()
