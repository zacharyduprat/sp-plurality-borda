# Paper workspace (`/paper`)

This directory is now the staging area for the write-up that matches the current computational + formal verification state of the repository.

## What is new (current project state to reflect in the paper)

The paper should now describe **three complementary verification layers**:

1. **Exact brute-force counting (small/medium `n`)** via Python enumeration on the anonymous single-peaked domain.
2. **Independent polyhedral counting (large `n`)** via LattE/Barvinok-generated Ehrhart data and strict-chamber checks.
3. **Machine-checked structural lemmas in Lean 4** for the linear-inequality logic behind the centrist-winner reduction.

## Core mathematical setup to include

- Axis: `A < B < C`.
- Single-peaked anonymous profile variables:
  - `x1 = A>B>C`
  - `x2 = C>B>A`
  - `x3 = B>A>C`
  - `x4 = B>C>A`
  - `x1 + x2 + x3 + x4 = n`
- Plurality scores:
  - `P_A = x1`
  - `P_B = x3 + x4`
  - `P_C = x2`
- Borda scores:
  - `B_A = 2x1 + x3`
  - `B_B = x1 + x2 + 2x3 + 2x4`
  - `B_C = 2x2 + x4`

## Structural result to emphasize

The SP-Borda centrism result implies disagreement can only occur in chambers where **Borda picks `B`**:

- `(Plurality = A, Borda = B)`
- `(Plurality = C, Borda = B)`

The `A \leftrightarrow C` symmetry gives equal chamber counts, so the paper should use:

- `D_SP(n) = 2 * D_(A,B)(n)`

and explicitly note that the four side-candidate Borda chambers are empty.

## Computation/verification assets now available

### Python scripts (`/code`)

- `disagreement.py`: brute-force disagreement counts.
- `chamber_vertices.py`: chamber vertex/sanity checks.
- `derive_strict_gf.py`: strict-chamber generating-function derivation support.
- `verify_quasipoly.py`: quasi-polynomial coefficient/value checks.
- `verify_closed.py`: closed Ehrhart coefficient cross-checks against brute force.
- `parse_latte.py`: parser for LattE Maple-style rational output.
- `latte_verify_final.py`: final large-`n` strict-chamber validations.
- `verify_lemma.py`: computational confirmation of forbidden-chamber emptiness.
- `arrangement_vertices.py`: arrangement-level vertex computation support.

### LattE artifacts (`/latte`)

- `chamber_AB.latte`: closed chamber model file.
- `chamber_AB.latte.rat`: rational generating function output.

### Saved outputs (`/output`)

- `arrangement_vertices_output.txt`
- `chamber_vertices_output.txt`
- `derive_strict_gf_output.txt`
- `verify_quasipoly_output.txt`

These files can be cited/reproduced in the methods or appendix sections.

### Lean formalization (`/lean`)

The Lean development formalizes the linear-arithmetic core:

- score definitions,
- centrism and side-candidate implications,
- forbidden chamber reductions,
- shifted integer chamber encoding for `(Plurality=A, Borda=B)`,
- `A \leftrightarrow C` symmetry.

The paper should clearly distinguish this from non-formalized enumerative parts (Ehrhart/quasi-polynomial/asymptotic counting), which remain computationally verified.

## Important current status in `/paper`

- `main.tex` exists but is currently empty.
- `references.bib` exists and should be extended as drafting proceeds.

## Suggested immediate paper outline

1. Problem statement and notation.
2. Single-peaked reduction and score inequalities.
3. Centrism lemma and chamber reduction (`D_SP = 2D_(A,B)`).
4. Polyhedral model of `(A,B)` chamber (closed vs strict).
5. LattE workflow + rational generating function.
6. Quasi-polynomial statement and numerical validation range.
7. Lean formalization scope and trust decomposition.
8. Reproducibility checklist (commands + artifact files).

## Minimal reproducibility command list (from repo root)

```bash
python3 code/chamber_vertices.py
python3 code/derive_strict_gf.py
python3 code/verify_quasipoly.py
python3 code/disagreement.py
python3 code/verify_closed.py
python3 code/parse_latte.py
python3 code/latte_verify_final.py
python3 code/verify_lemma.py
```

If LattE Integrale is missing, install it first (Ubuntu example):

```bash
sudo apt-get install latte-int
```
