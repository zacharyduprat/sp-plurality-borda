# sp-plurality-borda

Computational verification and Lean 4 formalization for the paper

> Z. Duprat, *A Period-Six Quasi-Polynomial for Plurality–Borda Disagreement on the Single-Peaked Domain* (May 2026).

The repository counts anonymous single-peaked profiles on three candidates on which Plurality and Borda elect distinct unique winners, on the axis `A < B < C`. The main object is the period-6 cubic quasi-polynomial

```text
D^{SP}_{Plur,Borda}(n)
```

obtained from a closed-form rational generating function, an explicit quasi-polynomial, and an asymptotic disagreement frequency of `2/9` under the single-peaked impartial-anonymous-culture measure.

## Mathematical object

Use four single-peaked ranking types:

```text
x1 = A > B > C
x2 = C > B > A
x3 = B > A > C
x4 = B > C > A
```

with `x1 + x2 + x3 + x4 = n`.

Plurality scores:

```text
P_A = x1
P_B = x3 + x4
P_C = x2
```

Borda scores:

```text
B_A = 2*x1 + x3
B_B = x1 + x2 + 2*x3 + 2*x4
B_C = 2*x2 + x4
```

By the **SP–Borda centrism lemma**, the only nonempty disagreement chambers are

```text
(Plurality = A, Borda = B)
(Plurality = C, Borda = B)
```

and these have equal counts by the involution `(x1, x2, x3, x4) -> (x2, x1, x4, x3)`. Therefore

```text
D^{SP}(n) = 2 * D_{(A,B)}(n).
```

## Headline result

For the open chamber `(Plurality = A, Borda = B)` with the strict score inequalities, the strict generating function is

```text
F_{AB}(t) = (t^4 + t^5 + t^6 + 2*t^7 - t^10)
            / ((1 - t)^4 * (1 + t)^2 * (1 + t + t^2)^2).
```

Partial-fraction decomposition yields, for every `n >= 1`,

```text
D^{SP}(n) = n^3 / 27 + n^2 / 36 + c_1(n mod 6) * n + c_0(n mod 6),
```

a degree-3 quasi-polynomial of period exactly 6, and the asymptotic disagreement frequency under SP-IAC is

```text
lim_{n -> infinity} D^{SP}(n) / C(n + 3, 3) = 2 / 9.
```

The first 21 values are

```text
0, 0, 0, 0, 2, 2, 6, 12, 14, 26, 34, 46, 60, 82, 94, 126, 148, 180, 212, 258, 288.
```

## Repository structure

| Path | Purpose |
|---|---|
| `code/disagreement.py` | Brute-force enumeration of `D_{(A,B)}(n)` and `D^{SP}(n)` |
| `code/chamber_vertices.py` | Six vertices of the closed chamber polytope `P`; denominators in `{2,3}` |
| `code/arrangement_vertices.py` | Inside-out denominator check: vertices of every `Q_S = P ∩ ⋂_{H in S} H` for `S ⊆ {H1,H2,H3,H4}`; lcm of all vertex denominators is `6` |
| `code/derive_strict_gf.py` | Derives `F_{AB}(t)` from the first 24 brute-force values; verifies the recurrence through `n = 42` |
| `code/verify_quasipoly.py` | Exact verification of the period-6 coefficient table |
| `code/verify_closed.py` | Cross-checks LattE closed Ehrhart coefficients against brute force |
| `code/latte_verify_final.py` | Open-chamber strict-count verification at widely spaced `n` up to `1000` |
| `code/verify_lemma.py` | LattE confirmation of the SP–Borda centrism lemma (forbidden-chamber emptiness, `n` up to 300) |
| `code/parse_latte.py` | Parses LattE's Maple-style rational generating function output |
| `latte/chamber_AB.latte` | LattE polytope file for the closed chamber `(Plur=A, Borda=B)` |
| `latte/chamber_AB.latte.rat` | LattE's unsimplified Ehrhart rational generating function |
| `output/` | PASS-output logs from the verification scripts |
| `lean/` | Lean 4 project formalizing the structural reduction |

## Lean 4 formalization

The Lean development under `lean/` formalizes the structural, linear-arithmetic core of the reduction. Entry point is `LeanCheck.lean`, with modules `Basic.lean`, `Centrism.lean`, `Reduction.lean`, `Chamber.lean`, and `Symmetry.lean`. The project builds with `lake build` against Mathlib and contains no occurrence of `sorry` or `admit`. Each proof is discharged by `linarith`, `omega`, `ring`, or definitional unfolding.

Formalized statements:

- score definitions for Plurality and Borda in coordinates `(x1, x2, x3, x4)`;
- the SP–Borda centrism lemma (`centrism_A`, `centrism_C`);
- the side-candidate implications `bordaA_implies_pluralityA` and `bordaC_implies_pluralityC`;
- the four forbidden disagreement chambers (`forbidden_PB_BA`, `forbidden_PC_BA`, `forbidden_PA_BC`, `forbidden_PB_BC`);
- `disagreement_implies_bordaB`;
- the shifted-integer chamber description `eventAB_iff_chamber_shifted`;
- the `A ↔ C` score symmetry under `σ : (x1, x2, x3, x4) ↦ (x2, x1, x4, x3)`, and `sigma_involutive`.

**Not** formalized in Lean: the finite-set cardinality identity `D^{SP}(n) = 2 * D_{(A,B)}(n)` (the involution `σ` is verified at the level of scores, not as an explicit `Finset` bijection between counted sets); the inside-out Ehrhart period bound and the arrangement-vertex computation; the generating-function derivation; the period-6 cubic quasi-polynomial; and the asymptotic `2/9`. Those remain at the level of the paper's mathematical arguments and the Python/LattE verification.

## Reproduction

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install LattE Integrale on Ubuntu:

```bash
sudo apt-get install latte-int
```

Run the verification scripts from the repository root:

```bash
python3 code/disagreement.py             # brute-force enumeration
python3 code/chamber_vertices.py         # six vertices of P, denominators in {2,3}
python3 code/arrangement_vertices.py     # inside-out denominator check, lcm = 6
python3 code/derive_strict_gf.py         # derive F_{AB}(t), verify recurrence to n = 42
python3 code/verify_quasipoly.py         # period-6 coefficient table
python3 code/verify_closed.py            # closed Ehrhart vs brute force, n = 0..25
python3 code/parse_latte.py              # parse closed-chamber rational GF
python3 code/latte_verify_final.py       # open strict count, n up to 1000
python3 code/verify_lemma.py             # forbidden-chamber emptiness, n up to 300
```

Each script prints `PASS` on success.

For the Lean development:

```bash
cd lean
lake build
```

## Closed-chamber generating function

For the closed chamber `(Plur = A, Borda = B)`, the LattE rational generating function is

```text
E^{<=}_{(A,B)}(t) = (t^4 + t^3 + t^2 + 1)
                  / (t^10 - 2*t^8 - 2*t^7 + t^6 + 4*t^5 + t^4 - 2*t^3 - 2*t^2 + 1).
```

Its Taylor coefficients reproduce the brute-force closed count exactly through `n = 25`.

## Encoding strict inequalities for LattE

LattE only accepts weak inequalities. The integer identity

```text
a > b   <=>   a >= b + 1
```

is used to encode the four strict score inequalities defining the open chamber. `code/latte_verify_final.py` generates a fresh LattE input file for each tested value of `n`.

## Structural lemma

If Borda elects `A` uniquely on the single-peaked domain, then Plurality also elects `A`. Symmetrically, if Borda elects `C` uniquely, then Plurality also elects `C`. Consequently, whenever Plurality and Borda disagree on this domain, Borda elects the centrist candidate `B`. The four forbidden chambers have integer-point count `0` at all tested values.

## Citation

If you use this code, please cite:

```bibtex
@unpublished{duprat2026sp,
  author = {Duprat, Zachary},
  title  = {A Period-Six Quasi-Polynomial for Plurality--Borda Disagreement on the Single-Peaked Domain},
  year   = {2026},
  note   = {Manuscript},
}
```
