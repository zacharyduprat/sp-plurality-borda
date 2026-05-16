import Mathlib.Tactic
import LeanCheck.Reduction

/-! Integer chamber formulation for the (Plurality A, Borda B) event. -/

/-- Integer chamber for the disagreement event
`pluralityWinnerA ∧ bordaWinnerB`, written in shifted form: each
strict score inequality `a > b` is replaced by the equivalent
weak inequality `a ≥ b + 1`, valid because we work over `Int`. -/
def chamberAB_shifted (x1 x2 x3 x4 : Int) : Prop :=
  x1 ≥ x3 + x4 + 1 ∧
  x1 ≥ x2 + 1 ∧
  x2 + x3 + 2 * x4 ≥ x1 + 1 ∧
  x1 + 2 * x3 + x4 ≥ x2 + 1

/-- Plurality-A vs plurality-B comparison reduces to `x1 > x3 + x4`. -/
theorem pa_gt_pb_iff (x1 x3 x4 : Int) :
    PA x1 > PB x3 x4 ↔ x1 > x3 + x4 := Iff.rfl

/-- Plurality-A vs plurality-C comparison reduces to `x1 > x2`. -/
theorem pa_gt_pc_iff (x1 x2 : Int) :
    PA x1 > PC x2 ↔ x1 > x2 := Iff.rfl

/-- Borda-B vs Borda-A comparison reduces to `x2 + x3 + 2 x4 > x1`. -/
theorem bb_gt_ba_iff (x1 x2 x3 x4 : Int) :
    BB x1 x2 x3 x4 > BA x1 x3 ↔ x2 + x3 + 2 * x4 > x1 := by
  unfold BB BA
  constructor
  · intro h; linarith
  · intro h; linarith

/-- Borda-B vs Borda-C comparison reduces to `x1 + 2 x3 + x4 > x2`. -/
theorem bb_gt_bc_iff (x1 x2 x3 x4 : Int) :
    BB x1 x2 x3 x4 > BC x2 x4 ↔ x1 + 2 * x3 + x4 > x2 := by
  unfold BB BC
  constructor
  · intro h; linarith
  · intro h; linarith

/-- Over `Int`, strict inequality is the shift of weak inequality by 1. -/
theorem int_gt_iff_ge_add_one (a b : Int) :
    a > b ↔ a ≥ b + 1 := by
  omega

/-- Event and shifted chamber are equivalent over `Int`. -/
theorem eventAB_iff_chamber_shifted (x1 x2 x3 x4 : Int) :
    pluralityWinnerA x1 x2 x3 x4 ∧ bordaWinnerB x1 x2 x3 x4 ↔
      chamberAB_shifted x1 x2 x3 x4 := by
  unfold pluralityWinnerA bordaWinnerB chamberAB_shifted
         PA PB PC BA BB BC
  constructor
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩
    refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith
  · rintro ⟨c1, c2, c3, c4⟩
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith