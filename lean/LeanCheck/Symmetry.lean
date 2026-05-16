import Mathlib.Tactic
import LeanCheck.Reduction

/-! Score symmetries under the side-swap involution σ. -/

/-- 1st coordinate of the involution `σ`. -/
def sigma1 (_x1 x2 _x3 _x4 : Int) : Int := x2

/-- 2nd coordinate of the involution `σ`. -/
def sigma2 (x1 _x2 _x3 _x4 : Int) : Int := x1

/-- 3rd coordinate of the involution `σ`. -/
def sigma3 (_x1 _x2 _x3 x4 : Int) : Int := x4

/-- 4th coordinate of the involution `σ`. -/
def sigma4 (_x1 _x2 x3 _x4 : Int) : Int := x3

/-- Plurality score of A on `σ`-image equals plurality score of C on the
original tuple. -/
theorem PA_sigma_eq_PC (x1 x2 x3 x4 : Int) :
    PA (sigma1 x1 x2 x3 x4) = PC x2 := rfl

/-- Plurality score of B is invariant under `σ`. -/
theorem PB_sigma_eq_PB (x1 x2 x3 x4 : Int) :
    PB (sigma3 x1 x2 x3 x4) (sigma4 x1 x2 x3 x4) = PB x3 x4 := by
  unfold PB sigma3 sigma4
  ring

/-- Plurality score of C on `σ`-image equals plurality score of A on the
original tuple. -/
theorem PC_sigma_eq_PA (x1 x2 x3 x4 : Int) :
    PC (sigma2 x1 x2 x3 x4) = PA x1 := rfl

/-- Borda score of A on `σ`-image equals Borda score of C on the
original tuple. -/
theorem BA_sigma_eq_BC (x1 x2 x3 x4 : Int) :
    BA (sigma1 x1 x2 x3 x4) (sigma3 x1 x2 x3 x4) = BC x2 x4 := rfl

/-- Borda score of B is invariant under `σ`. -/
theorem BB_sigma_eq_BB (x1 x2 x3 x4 : Int) :
    BB (sigma1 x1 x2 x3 x4) (sigma2 x1 x2 x3 x4)
       (sigma3 x1 x2 x3 x4) (sigma4 x1 x2 x3 x4) = BB x1 x2 x3 x4 := by
  unfold BB sigma1 sigma2 sigma3 sigma4
  ring

/-- Borda score of C on `σ`-image equals Borda score of A on the
original tuple. -/
theorem BC_sigma_eq_BA (x1 x2 x3 x4 : Int) :
    BC (sigma2 x1 x2 x3 x4) (sigma4 x1 x2 x3 x4) = BA x1 x3 := rfl

/-- `σ` is an involution. -/
theorem sigma_involutive (x1 x2 x3 x4 : Int) :
    sigma1 (sigma1 x1 x2 x3 x4) (sigma2 x1 x2 x3 x4)
           (sigma3 x1 x2 x3 x4) (sigma4 x1 x2 x3 x4) = x1 ∧
    sigma2 (sigma1 x1 x2 x3 x4) (sigma2 x1 x2 x3 x4)
           (sigma3 x1 x2 x3 x4) (sigma4 x1 x2 x3 x4) = x2 ∧
    sigma3 (sigma1 x1 x2 x3 x4) (sigma2 x1 x2 x3 x4)
           (sigma3 x1 x2 x3 x4) (sigma4 x1 x2 x3 x4) = x3 ∧
    sigma4 (sigma1 x1 x2 x3 x4) (sigma2 x1 x2 x3 x4)
           (sigma3 x1 x2 x3 x4) (sigma4 x1 x2 x3 x4) = x4 :=
  ⟨rfl, rfl, rfl, rfl⟩