import Mathlib.Tactic
import LeanCheck.Centrism

/-! Score definitions and structural reduction to Borda winner B. -/

/-- Plurality score of side candidate A. -/
def PA (x1 : Int) : Int := x1

/-- Plurality score of center candidate B. -/
def PB (x3 x4 : Int) : Int := x3 + x4

/-- Plurality score of side candidate C. -/
def PC (x2 : Int) : Int := x2

/-- Borda score of side candidate A. -/
def BA (x1 x3 : Int) : Int := 2 * x1 + x3

/-- Borda score of center candidate B. -/
def BB (x1 x2 x3 x4 : Int) : Int := x1 + x2 + 2 * x3 + 2 * x4

/-- Borda score of side candidate C. -/
def BC (x2 x4 : Int) : Int := 2 * x2 + x4

/-- A is the strict plurality winner. -/
def pluralityWinnerA (x1 x2 x3 x4 : Int) : Prop :=
  PA x1 > PB x3 x4 ∧ PA x1 > PC x2

/-- B is the strict plurality winner. -/
def pluralityWinnerB (x1 x2 x3 x4 : Int) : Prop :=
  PB x3 x4 > PA x1 ∧ PB x3 x4 > PC x2

/-- C is the strict plurality winner. -/
def pluralityWinnerC (x1 x2 x3 x4 : Int) : Prop :=
  PC x2 > PA x1 ∧ PC x2 > PB x3 x4

/-- A is the strict Borda winner. -/
def bordaWinnerA (x1 x2 x3 x4 : Int) : Prop :=
  BA x1 x3 > BB x1 x2 x3 x4 ∧ BA x1 x3 > BC x2 x4

/-- B is the strict Borda winner. -/
def bordaWinnerB (x1 x2 x3 x4 : Int) : Prop :=
  BB x1 x2 x3 x4 > BA x1 x3 ∧ BB x1 x2 x3 x4 > BC x2 x4

/-- C is the strict Borda winner. -/
def bordaWinnerC (x1 x2 x3 x4 : Int) : Prop :=
  BC x2 x4 > BA x1 x3 ∧ BC x2 x4 > BB x1 x2 x3 x4

theorem bordaA_implies_pluralityA
    (x1 x2 x3 x4 : Int)
    (_h1 : 0 ≤ x1) (h2 : 0 ≤ x2) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4)
    (hB : bordaWinnerA x1 x2 x3 x4) :
    pluralityWinnerA x1 x2 x3 x4 := by
  unfold bordaWinnerA BA BB BC at hB
  unfold pluralityWinnerA PA PB PC
  exact centrism_A x1 x2 x3 x4 h2 h3 h4 hB.1

theorem bordaC_implies_pluralityC
    (x1 x2 x3 x4 : Int)
    (h1 : 0 ≤ x1) (_h2 : 0 ≤ x2) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4)
    (hB : bordaWinnerC x1 x2 x3 x4) :
    pluralityWinnerC x1 x2 x3 x4 := by
  unfold bordaWinnerC BA BB BC at hB
  unfold pluralityWinnerC PA PB PC
  exact centrism_C x1 x2 x3 x4 h1 h3 h4 hB.2

theorem forbidden_PB_BA
    (x1 x2 x3 x4 : Int)
    (h1 : 0 ≤ x1) (h2 : 0 ≤ x2) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4) :
    ¬ (pluralityWinnerB x1 x2 x3 x4 ∧ bordaWinnerA x1 x2 x3 x4) := by
  rintro ⟨hP, hB⟩
  unfold pluralityWinnerB PA PB PC at hP
  unfold bordaWinnerA BA BB BC at hB
  linarith [hP.1, hP.2, hB.1, hB.2, h1, h2, h3, h4]

theorem forbidden_PC_BA
    (x1 x2 x3 x4 : Int)
    (h1 : 0 ≤ x1) (h2 : 0 ≤ x2) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4) :
    ¬ (pluralityWinnerC x1 x2 x3 x4 ∧ bordaWinnerA x1 x2 x3 x4) := by
  rintro ⟨hP, hB⟩
  unfold pluralityWinnerC PA PB PC at hP
  unfold bordaWinnerA BA BB BC at hB
  linarith [hP.1, hP.2, hB.1, hB.2, h1, h2, h3, h4]

theorem forbidden_PA_BC
    (x1 x2 x3 x4 : Int)
    (h1 : 0 ≤ x1) (h2 : 0 ≤ x2) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4) :
    ¬ (pluralityWinnerA x1 x2 x3 x4 ∧ bordaWinnerC x1 x2 x3 x4) := by
  rintro ⟨hP, hB⟩
  unfold pluralityWinnerA PA PB PC at hP
  unfold bordaWinnerC BA BB BC at hB
  linarith [hP.1, hP.2, hB.1, hB.2, h1, h2, h3, h4]

theorem forbidden_PB_BC
    (x1 x2 x3 x4 : Int)
    (h1 : 0 ≤ x1) (h2 : 0 ≤ x2) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4) :
    ¬ (pluralityWinnerB x1 x2 x3 x4 ∧ bordaWinnerC x1 x2 x3 x4) := by
  rintro ⟨hP, hB⟩
  unfold pluralityWinnerB PA PB PC at hP
  unfold bordaWinnerC BA BB BC at hB
  linarith [hP.1, hP.2, hB.1, hB.2, h1, h2, h3, h4]

/-- Disagreement cases. -/
def disagreement (x1 x2 x3 x4 : Int) : Prop :=
  (pluralityWinnerA x1 x2 x3 x4 ∧ bordaWinnerB x1 x2 x3 x4) ∨
  (pluralityWinnerA x1 x2 x3 x4 ∧ bordaWinnerC x1 x2 x3 x4) ∨
  (pluralityWinnerB x1 x2 x3 x4 ∧ bordaWinnerA x1 x2 x3 x4) ∨
  (pluralityWinnerB x1 x2 x3 x4 ∧ bordaWinnerC x1 x2 x3 x4) ∨
  (pluralityWinnerC x1 x2 x3 x4 ∧ bordaWinnerA x1 x2 x3 x4) ∨
  (pluralityWinnerC x1 x2 x3 x4 ∧ bordaWinnerB x1 x2 x3 x4)

/-- Under nonnegativity, disagreement implies Borda winner B. -/
theorem disagreement_implies_bordaB
    (x1 x2 x3 x4 : Int)
    (h1 : 0 ≤ x1) (h2 : 0 ≤ x2) (h3 : 0 ≤ x3) (h4 : 0 ≤ x4)
    (hd : disagreement x1 x2 x3 x4) :
    bordaWinnerB x1 x2 x3 x4 := by
  unfold disagreement at hd
  rcases hd with hAB | hAC | hBA | hBC | hCA | hCB
  · exact hAB.2
  · exfalso
    exact forbidden_PA_BC x1 x2 x3 x4 h1 h2 h3 h4 hAC
  · exfalso
    exact forbidden_PB_BA x1 x2 x3 x4 h1 h2 h3 h4 hBA
  · exfalso
    exact forbidden_PB_BC x1 x2 x3 x4 h1 h2 h3 h4 hBC
  · exfalso
    exact forbidden_PC_BA x1 x2 x3 x4 h1 h2 h3 h4 hCA
  · exact hCB.2