# Lean verification

Lean formalization of the linear-arithmetic core of the SP-Borda reduction.

It verifies:

- the Plurality and Borda score definitions;
- the SP-Borda centrism lemma;
- the side-candidate implications;
- the four forbidden disagreement chambers;
- the conclusion that any Plurality-Borda disagreement must have Borda winner `B`;
- the shifted integer chamber for the `(Plurality = A, Borda = B)` event;
- the `A ↔ C` score symmetry.

It does **not** formalize Ehrhart/generating-function enumeration results; those are checked by the Python and LattE scripts.
