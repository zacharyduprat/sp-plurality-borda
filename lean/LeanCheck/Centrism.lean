import Mathlib.Tactic

/-! Core inequalities for the SP-Borda centrism lemma. -/

theorem centrism_A
    (x1 x2 x3 x4 : Int)
    (h2 : 0 ≤ x2) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4)
    (h  : 2 * x1 + x3 > x1 + x2 + 2 * x3 + 2 * x4) :
    x1 > x3 + x4 ∧ x1 > x2 := by
  constructor
  · linarith
  · linarith

theorem centrism_C
    (x1 x2 x3 x4 : Int)
    (h1 : 0 ≤ x1) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4)
    (h  : 2 * x2 + x4 > x1 + x2 + 2 * x3 + 2 * x4) :
    x2 > x1 ∧ x2 > x3 + x4 := by
  constructor
  · linarith
  · linarith