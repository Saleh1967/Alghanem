import Slge.CoverageTable

/-!
# التغطية: ما يشهد عليه المودَعُ من الشبكة والجداول والمقاييس والمخصّص — بشاهدٍ مسمًّى أو «معلومة»

الفهرسُ `COVERAGE_INDEX.md` يقيس على مودَعَي شهادات المصحف ثلاثةَ محاور: الخاناتُ، وصفوفُ الجداول المودَعة
(الموزِّع، الأعلام، السوابق)، وجذورُ المقاييس ومن فوقها عقدُ المخصّص. هنا تعريفُ **الشاهد** لكلّ محورٍ
وخواصُّه المبرهَنة؛ والعدُّ في الجدول المولَّد (`CoverageTable`) من المودَع لا من هنا.

* **الشبكة**: الكتابُ لسيبويه (JK006989، مختومٌ هنا) «لأن الألف لا تكون أبدا إلا ساكنة» (س18101) — فمن
  الـ116 ثلاثٌ لا تُرخَّص: (ا،فتح) (ا،ضم) (ا،كسر) (`alifVowelled`)، والمرخَّصُ **113** (`licensable`،
  `licensable_length`) قسمةً تامّةً (`cells_partition`). ومرآتُها في الغانم `A116.Alif.licensable` بجدولها
  المودَع. والمبرهَن على المودَع: **المشهودُ في المصحف هو المرخَّصُ من الشبكة بعينه** (`attested_eq_licensable`).
* **شاهدُ الجذر** (المقاييس): صورةٌ من المودَع يقرؤها الجذعُ على ذلك الجذر — **قاطعٌ** إن لم يقرأها على غيره
  (`qati_iff`: الجذورُ كلُّها `r` وليست خالية)، و**محتملٌ** إن قرأها على غيره أيضًا؛ ولا
  شاهدَ إلّا والجذرُ من جذور الصورة (`witness_some_iff_mem`)، والقاطعُ محتملٌ (`qati_mem`).
* **شاهدُ العقدة** (المخصّص): جذرٌ من جذور عنوانها له شاهدٌ قاطع (`nodeGrade`؛ `node_mafhum_has_witness`:
  لا «مفهوم» بلا شاهدٍ هو جذرٌ في العنوان وفي القواطع؛ `nodeGrade_total`: مفهومٌ أو معلومة، لا رفض).
* **شاهدُ الصفّ** (جداول المبنيّات والأعلام والسوابق): صورةٌ من المودَع يقرؤها قارئُ الجدول على ذلك الصفّ؛
  الدرجةُ بعدد الشواهد (`rowGrade`؛ `row_mafhum_pos`)، والصفُّ بلا شاهدٍ يبقى في جدوله «معلومة» لا يُحذف
  (المادّة ١٥: الغيابُ ليس امتناعًا).

وعلى الجدول المولَّد: المشهودُ لا يتجاوز المودَع في كلّ محور (`axes_attested_le_total`)، وقسمةُ الجذور
(قاطع/محتمل فقط/بلا شاهد) وقسمةُ العقد تامّتان (`roots_partition`، `nodes_partition`).
-/

namespace Slge.Coverage

open Slge
open Slge.Categories (c)

/-! ## الشبكة -/

/-- الألفُ (الحاملُ ١ في SLGE) بالحركات الثلاث: خاناتٌ في الشبكة لا في الكلام. -/
def alifVowelled : List SCell := [c 1 0, c 1 1, c 1 2]

/-- المرخَّصُ من الشبكة: كلُّ خانةٍ ليست ألفًا متحرّكة. -/
def licensable : List SCell := scells.filter fun x => !(alifVowelled.contains x)

theorem alifVowelled_length : alifVowelled.length = 3 := by rfl

theorem licensable_length : licensable.length = 113 := by decide

theorem licensable_nodup : licensable.Nodup := by decide

/-- الشبكةُ قسمةٌ تامّة: المرخَّصُ والألفُ المتحرّكة بلا تداخل، ومجموعُهما الـ116. -/
theorem cells_partition :
    licensable.length + alifVowelled.length = scells.length ∧
    licensable.all (fun x => !(alifVowelled.contains x)) = true := by decide

theorem vowelled_alif_not_licensable : alifVowelled.all (fun x => !(licensable.contains x)) = true := by
  decide

theorem alif_sukun_licensable : licensable.contains (c 1 3) = true := by decide

/-- **المشهودُ في مودَع المصحف هو المرخَّصُ من الشبكة بعينه**: لا خانةَ مرخَّصةً بلا شاهد، ولا ألفَ متحرّكةً
في المصحف. -/
theorem attested_eq_licensable : CoverageTable.attestedCells = licensable := by decide

/-! ## شاهدُ الجذر -/

/-- قاطعٌ: الصورةُ لا تُقرأ إلّا على هذا الجذر؛ محتملٌ: تُقرأ عليه وعلى غيره. -/
inductive Witness where
  | qati
  | muhtamal
  deriving DecidableEq, Repr

/-- شاهدُ الجذر `r` من صورةٍ جذورُ قراءاتها `roots`: قاطعٌ إن كانت كلُّها `r` (وليست خالية)، محتملٌ إن كان
`r` فيها مع غيره، وإلّا لا شاهد. -/
def witnessOf (roots : List Nat) (r : Nat) : Option Witness :=
  if roots ≠ [] ∧ roots.all (· == r) then some .qati
  else if roots.contains r then some .muhtamal else none

theorem qati_iff (roots : List Nat) (r : Nat) :
    witnessOf roots r = some .qati ↔ roots ≠ [] ∧ roots.all (· == r) = true := by
  unfold witnessOf
  constructor
  · intro h
    by_cases h1 : roots ≠ [] ∧ roots.all (· == r) = true
    · exact h1
    · simp only [h1, ↓reduceIte] at h
      split at h <;> simp_all
  · intro h; simp [h]

theorem witness_some_iff_mem (roots : List Nat) (r : Nat) :
    (witnessOf roots r).isSome = true ↔ r ∈ roots := by
  unfold witnessOf
  by_cases h1 : roots ≠ [] ∧ roots.all (· == r) = true
  · rw [ite_eq_left h1]
    obtain ⟨hne, hall⟩ := h1
    obtain ⟨x, hx⟩ := List.exists_mem_of_ne_nil roots hne
    have := List.all_eq_true.mp hall x hx
    simp only [beq_iff_eq] at this
    exact ⟨fun _ => this ▸ hx, fun _ => rfl⟩
  · rw [ite_eq_right h1]
    by_cases h2 : roots.contains r
    · simp [List.contains_iff_mem.mp h2]
    · simp only [h2, ↓reduceIte, Option.isSome_none, Bool.false_eq_true, false_iff]
      exact fun hm => h2 (List.contains_iff_mem.mpr hm)

/-- القاطعُ محتمل: الجذرُ من جذور الصورة. -/
theorem qati_mem (roots : List Nat) (r : Nat) (h : witnessOf roots r = some .qati) : r ∈ roots := by
  obtain ⟨hne, hall⟩ := (qati_iff roots r).mp h
  obtain ⟨x, hx⟩ := List.exists_mem_of_ne_nil roots hne
  have := List.all_eq_true.mp hall x hx
  simp only [beq_iff_eq] at this
  exact this ▸ hx

/-- لا قاطعَ لجذرين من صورةٍ واحدة. -/
theorem qati_unique (roots : List Nat) (r s : Nat) (hr : witnessOf roots r = some .qati)
    (hs : witnessOf roots s = some .qati) : r = s := by
  obtain ⟨hne, hr'⟩ := (qati_iff roots r).mp hr
  obtain ⟨_, hs'⟩ := (qati_iff roots s).mp hs
  obtain ⟨x, hx⟩ := List.exists_mem_of_ne_nil roots hne
  have h1 := List.all_eq_true.mp hr' x hx
  have h2 := List.all_eq_true.mp hs' x hx
  simp only [beq_iff_eq] at h1 h2
  omega

/-! ## الدرجة -/

/-- مرتبتا الحكم (المادّة ١٥): مفهومٌ بشاهدٍ مسمًّى أو معلومةٌ بلا شاهد. -/
inductive Grade where
  | malumah
  | mafhum (witness : Nat)
  deriving DecidableEq, Repr

/-- درجةُ الصفّ بعدد شواهده من المودَع. -/
def rowGrade (n : Nat) : Grade := if 0 < n then .mafhum n else .malumah

theorem row_mafhum_pos (n w : Nat) (h : rowGrade n = .mafhum w) : 0 < n ∧ w = n := by
  unfold rowGrade at h
  split at h
  · cases h; exact ⟨‹_›, rfl⟩
  · cases h

theorem row_malumah_iff (n : Nat) : rowGrade n = .malumah ↔ n = 0 := by
  unfold rowGrade; split <;> simp_all <;> omega

/-- درجةُ العقدة: أوّلُ جذرٍ في عنوانها له شاهدٌ قاطعٌ في المودَع (`qati` قائمةُ القواطع). -/
def nodeGrade (title qati : List Nat) : Grade :=
  match title.find? (qati.contains ·) with
  | some r => .mafhum r
  | none => .malumah

/-- لا «مفهوم» بلا شاهد: الشاهدُ جذرٌ في العنوان وله شاهدٌ قاطع. -/
theorem node_mafhum_has_witness (title qati : List Nat) (w : Nat) (h : nodeGrade title qati = .mafhum w) :
    w ∈ title ∧ w ∈ qati := by
  unfold nodeGrade at h
  split at h
  · rename_i r hr
    have hw : w = r := by cases h; rfl
    subst hw
    exact ⟨List.mem_of_find?_eq_some hr, List.contains_iff_mem.mp (List.find?_some hr)⟩
  · cases h

theorem nodeGrade_total (title qati : List Nat) :
    nodeGrade title qati = .malumah ∨ ∃ w, nodeGrade title qati = .mafhum w := by
  cases h : nodeGrade title qati with
  | malumah => exact Or.inl rfl
  | mafhum w => exact Or.inr ⟨w, rfl⟩

/-- عقدةٌ بلا جذورٍ في عنوانها معلومةٌ أبدًا. -/
theorem nodeGrade_nil (qati : List Nat) : nodeGrade [] qati = .malumah := by rfl

/-! ## على الجدول المولَّد -/

theorem axes_attested_le_total : CoverageTable.axes.all (fun a => a.2.2 ≤ a.2.1) = true := by decide

theorem roots_partition :
    CoverageTable.rootsQati + CoverageTable.rootsMuhtamalOnly + CoverageTable.rootsNone =
      CoverageTable.rootsTotal := by decide

theorem nodes_partition :
    CoverageTable.nodesQati + CoverageTable.nodesMuhtamalOnly + CoverageTable.nodesNone +
      CoverageTable.nodesNoRoots = CoverageTable.nodesTotal := by decide

end Slge.Coverage
