import Slge.Bridge
import Slge.Nabhani

/-!
# شهادةُ SLGE: الدالُّ خاناتٍ، ومسارُ القراءة، ونوعُ المدلول — ببصمةٍ مميِّزة

خرجُ SLGE شهادةٌ ثانية فوق شهادة الغانم: **الخاناتُ** (الدالُّ وحده، تُردّ ذرّاتٍ بعينها عبر الجسر)،
**المسارُ** (لكلّ بوّابةٍ قارئة عددُ قراءاتها أو المختارة — أعدادٌ لا نصّ)، و**نوعُ المدلول** على تقسيم
النبهانيّ الخماسيّ (`Nabhani.Madlul`) اختياريًّا: `none` = لم يُحكم بعد — فالسُّلَّمُ يقرأ الدالَّ من حيث هو،
والمدلولُ يُسنَد في طبقة الحكم بشاهد (المادّتان ١٠ و١٥).

**البصمة** عددٌ واحد: اقترانُ كانتور (`A116.Numbering.pair`) لعدد الذرّات (`atomNumber`، مميِّزٌ لكلّ
قائمة خانات بلا شرط ترخيص) مع ترميز المسار (`encList`، مميِّز) ونوع المدلول (`encMadlul`، مميِّز). المبرهَن:
* `fingerprint_injective`: شهادتان ببصمةٍ واحدة هما واحدة — فلا خرجان مختلفان ببصمةٍ واحدة في أيّ مستودع.
* `restore`: خاناتُ الشهادة تعود ذرّاتِ الغانم بعينها وتُقرأ منها (`restore_cells`).
* `withMadlul_changes_fingerprint`: إسنادُ نوع المدلول يغيّر البصمة — فالحكمُ لا يُخفى في بصمة الدالّ.
-/

namespace Slge.Shahada

open A116.Numbering (pair pair_injective atomNumber atomNumber_injective)

/-- ترميزُ قائمة أعداد عددًا واحدًا، مميِّز. -/
def encList : List Nat → Nat
  | [] => 0
  | x :: xs => pair x (encList xs) + 1

theorem encList_injective : ∀ {a b : List Nat}, encList a = encList b → a = b
  | [], [], _ => rfl
  | [], _ :: _, h => by simp [encList] at h
  | _ :: _, [], h => by simp [encList] at h
  | x :: xs, y :: ys, h => by
    simp only [encList, Nat.add_right_cancel_iff] at h
    obtain ⟨h1, h2⟩ := pair_injective h
    rw [h1, encList_injective h2]

/-- نوعُ المدلول عددًا: 0 لم يُحكم، ثمّ الخمسةُ بترتيب النبهانيّ. -/
def encMadlul : Option Nabhani.Madlul → Nat
  | none => 0
  | some .mana => 1 | some .mufradMustamal => 2 | some .mufradMuhmal => 3
  | some .murakkabMustamal => 4 | some .muhmalMurakkab => 5

theorem encMadlul_injective : ∀ {a b : Option Nabhani.Madlul}, encMadlul a = encMadlul b → a = b := by
  intro a b h
  rcases a with _ | x <;> rcases b with _ | y
  · rfl
  · cases y <;> simp [encMadlul] at h
  · cases x <;> simp [encMadlul] at h
  · cases x <;> cases y <;> simp [encMadlul] at h ⊢

structure Shahada where
  cells : List SCell
  path : List Nat
  madlul : Option Nabhani.Madlul
  deriving DecidableEq, Repr

/-- ذرّاتُ الغانم من خانات الشهادة (عبر الجسر). -/
def atoms (s : Shahada) : List A116.Cell := s.cells.map toCell

def fingerprint (s : Shahada) : Nat :=
  pair (atomNumber (atoms s)) (pair (encList s.path) (encMadlul s.madlul))

theorem fingerprint_injective {s t : Shahada} (h : fingerprint s = fingerprint t) : s = t := by
  unfold fingerprint at h
  obtain ⟨h1, h2⟩ := pair_injective h
  obtain ⟨h3, h4⟩ := pair_injective h2
  have hc : s.cells = t.cells := map_toCell_injective (atomNumber_injective h1)
  have hp := encList_injective h3
  have hm := encMadlul_injective h4
  cases s; cases t; simp_all

/-- الردُّ: الذرّاتُ تعود خاناتِ الشهادة بعينها (على خانات SLGE المودَعة). -/
theorem map_ofCell_toCell : ∀ (l : List SCell), (∀ c ∈ l, c ∈ scells) →
    (l.map toCell).map ofCell = l
  | [], _ => rfl
  | c :: t, h => by
    simp only [List.map_cons, List.cons.injEq]
    exact ⟨ofCell_toCell_on c (h c (List.mem_cons_self ..)),
           map_ofCell_toCell t (fun x hx => h x (List.mem_cons_of_mem _ hx))⟩

theorem restore_cells (s : Shahada) (h : ∀ c ∈ s.cells, c ∈ scells) :
    (atoms s).map ofCell = s.cells := map_ofCell_toCell s.cells h

/-- إسنادُ نوع المدلول في طبقة الحكم. -/
def withMadlul (s : Shahada) (m : Nabhani.Madlul) : Shahada := { s with madlul := some m }

theorem withMadlul_changes_fingerprint (s : Shahada) (m : Nabhani.Madlul) (h : s.madlul ≠ some m) :
    fingerprint (withMadlul s m) ≠ fingerprint s := by
  intro heq
  have := fingerprint_injective heq
  have hm : (withMadlul s m).madlul = s.madlul := by rw [this]
  simp [withMadlul] at hm
  exact h hm.symm

/-! ## الصورُ المغلقة للحساب: الاقترانُ بصيغته المغلقة (`pair_closed`) وعددُ الذرّات بصيغته
(`atomNumber_closed`) — مساويان للتعريفين، وبهما يُحسب التصدير على أعدادٍ كبيرة. -/

def pairC (u r : Nat) : Nat := (u + r) * (u + r + 1) / 2 + r

theorem pairC_eq (u r : Nat) : pairC u r = pair u r := (A116.Numbering.pair_closed u r).symm

def encListC : List Nat → Nat
  | [] => 0
  | x :: xs => pairC x (encListC xs) + 1

theorem encListC_eq : ∀ l : List Nat, encListC l = encList l
  | [] => rfl
  | x :: xs => by simp only [encListC, encList, pairC_eq, encListC_eq xs]

def atomNumberC (w : List A116.Cell) : Nat :=
  A116.Numbering.geo 116 w.length + A116.Numbering.digits 116 (w.map A116.Numbering.bridgeIndex)

theorem atomNumberC_eq (w : List A116.Cell) : atomNumberC w = atomNumber w :=
  (A116.Numbering.atomNumber_closed w).symm

def fingerprintC (s : Shahada) : Nat :=
  pairC (atomNumberC (atoms s)) (pairC (encListC s.path) (encMadlul s.madlul))

theorem fingerprintC_eq (s : Shahada) : fingerprintC s = fingerprint s := by
  simp only [fingerprintC, fingerprint, pairC_eq, encListC_eq, atomNumberC_eq]

/-! ## شواهد -/

def kataba : Shahada := ⟨[Categories.c 22 0, Categories.c 3 0, Categories.c 2 0], [0, 0, 2, 1, 1, 1, 1], none⟩

theorem witness_distinct :
    fingerprint kataba ≠ fingerprint (withMadlul kataba .mana) ∧
    fingerprint kataba ≠ fingerprint { kataba with path := [0, 0, 1, 1, 1, 1, 1] } := by
  constructor
  · exact (withMadlul_changes_fingerprint kataba .mana (by simp [kataba])).symm
  · intro h; have := fingerprint_injective h; simp [kataba] at this

end Slge.Shahada
