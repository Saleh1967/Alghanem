/-
  ExhaustionGate.lean — بوابة الاستنفاد: الصياغة الصحيحة وفحص نسخة المستند
  Lean 4 core (v4.15.0)، بلا Mathlib، بلا sorry، بلا axiom.

  الباب أ: ثلاث مبرهنات تفحص صيغ Lean الواردة في المستند (بإعادة بناء تواقيعها).
  الباب ب: بوابة الاستنفاد بصيغة غير فارغة: الترخيص وراثةٌ من جدولٍ مسمّى.
  الباب ج: الطيّ والاسترجاع (التقشير) بصيغة غير فارغة: لا فقدَ ولا بقيّة.
-/

namespace Ghanem

/-! ## الباب أ — فحص صيغ المستند -/

/-- جدول بخانات 116، كما في المستند: كل خانة ترخيصٌ أو فراغ. -/
structure DegreeTable where
  slots : Fin 116 → Option Nat

def DegreeTable.Complete (t : DegreeTable) : Prop :=
  ∀ i : Fin 116, (t.slots i).isSome = true

/-- الجدول الفارغ: لا خانة فيه مرخَّصة. -/
def emptyTable : DegreeTable := ⟨fun _ => none⟩

theorem emptyTable_incomplete : ¬ emptyTable.Complete := by
  intro h
  have := h ⟨0, by decide⟩
  simp [emptyTable] at this

/-- أ-١: توقيع `exhaustion_gate` في المستند يجعل `t` حرًّا غير مقيَّد بالدرجة.
    فكلُّ مسنَدٍ ترخيصيٍّ يحقّق ذلك التوقيع لا ساكنَ له: الترخيص يصير مستحيلًا. -/
theorem doc_gate_signature_vacuous (Licensed : Nat → Prop)
    (gate : ∀ {k : Nat} {t : DegreeTable}, Licensed (k + 1) → t.Complete) :
    ∀ k, ¬ Licensed (k + 1) :=
  fun _ hl => emptyTable_incomplete (gate (t := emptyTable) hl)

/-- أ-٢: صيغة `residue_recycled` (∃ i, origin z = i) صادقةٌ لأيّ دالّة كانت،
    فلا تحمل خبرًا عن الزوائد. -/
theorem doc_residue_statement_trivial {α : Type} (origin : α → Fin 116) (z : α) :
    ∃ i : Fin 116, origin z = i :=
  ⟨origin z, rfl⟩

/-- أ-٣: صيغة `peeling_terminates` (∃ root wazn, peelStar w = (root, wazn))
    صادقةٌ لأيّ دالّة نوعُ قيمتها زوج، فلا تشهد بانتهاءٍ ولا بصحّة. -/
theorem doc_peeling_statement_trivial {W : Type} (peelStar : W → Nat × Nat) (w : W) :
    ∃ root wazn : Nat, peelStar w = (root, wazn) :=
  ⟨(peelStar w).1, (peelStar w).2, rfl⟩

/-! ## الباب ب — بوابة الاستنفاد بصيغة غير فارغة -/

/-- جدول درجة: قائمة خانات، كل خانة ترخيصٌ (some) أو فراغ (none). -/
abbrev Table := List (Option Nat)

def Complete (t : Table) : Prop := ∀ x ∈ t, x.isSome = true

instance (t : Table) : Decidable (Complete t) := by
  unfold Complete; exact inferInstance

/-- سُلَّم: جدولٌ مسمّى لكل درجة. -/
structure Ladder where
  table : Nat → Table

/-- الترخيص بالدرجة k: كلّ جدولٍ تحتها تامّ. -/
def LicensedAt (L : Ladder) (k : Nat) : Prop := ∀ j, j < k → Complete (L.table j)

/-- ب-١: بوابة الاستنفاد — الترخيص بالدرجة k+1 يشهد بتمام جدول الدرجة k بعينه. -/
theorem gate {L : Ladder} {k : Nat} (h : LicensedAt L (k + 1)) :
    Complete (L.table k) :=
  h k (Nat.lt_succ_self k)

/-- ب-٢: المانع — جدولٌ ناقص في الدرجة k ⇒ لا ترخيص بالدرجة k+1. -/
theorem gate_blocks {L : Ladder} {k : Nat} (hnc : ¬ Complete (L.table k)) :
    ¬ LicensedAt L (k + 1) :=
  fun h => hnc (gate h)

/-- ب-٣: لا قفز — الترخيص بدرجةٍ يتضمّن الترخيص بكل ما تحتها. -/
theorem no_jump {L : Ladder} {k m : Nat} (hkm : m ≤ k) (h : LicensedAt L k) :
    LicensedAt L m :=
  fun j hj => h j (Nat.lt_of_lt_of_le hj hkm)

/-- ب-٤: الترخيص وراثةٌ بالضبط: الدرجة k+1 = الدرجة k + تمام جدولها. -/
theorem licensed_succ_iff {L : Ladder} {k : Nat} :
    LicensedAt L (k + 1) ↔ LicensedAt L k ∧ Complete (L.table k) := by
  constructor
  · intro h
    exact ⟨no_jump (Nat.le_succ k) h, gate h⟩
  · intro ⟨hk, hc⟩ j hj
    rcases Nat.lt_succ_iff_lt_or_eq.mp hj with hlt | heq
    · exact hk j hlt
    · exact heq ▸ hc

/-- ب-٥: الدرجة ٠ مرخَّصة دائمًا (لا شيء تحتها). -/
theorem licensed_zero (L : Ladder) : LicensedAt L 0 :=
  fun _ hj => absurd hj (Nat.not_lt_zero _)

/-- شاهد: جدول 116 خانة، فيه خانة واحدة فارغة — ناقص (يُحسب بالآلة). -/
def table116_oneGap : Table := List.replicate 115 (some 1) ++ [none]

theorem table116_oneGap_len : table116_oneGap.length = 116 := by decide
theorem table116_oneGap_incomplete : ¬ Complete table116_oneGap := by decide

/-- شاهد: الجدول نفسه بعد ملء الخانة — تامّ. -/
def table116_full : Table := List.replicate 116 (some 1)
theorem table116_full_complete : Complete table116_full := by decide

theorem oneGap_blocks_degree1 :
    ¬ LicensedAt ⟨fun _ => table116_oneGap⟩ 1 :=
  gate_blocks table116_oneGap_incomplete

/-! ## الباب ج — الطيّ والاسترجاع (التقشير) بصيغة غير فارغة -/

/-- قطعة الكلمة: أصلٌ أو زائد (والوسم معطى، لا مستنبط). -/
inductive Seg
  | asl  (c : Nat)
  | zaid (c : Nat)
  deriving DecidableEq, Repr

abbrev Word := List Seg

def Seg.isZaid : Seg → Bool
  | .asl _ => false
  | .zaid _ => true

/-- الطيّ: الكلمة ⇒ (القناع، الأصول، الزوائد). -/
def mask  : Word → List Bool := List.map Seg.isZaid
def asls  : Word → List Nat
  | [] => []
  | .asl c :: w => c :: asls w
  | .zaid _ :: w => asls w
def zaids : Word → List Nat
  | [] => []
  | .asl _ :: w => zaids w
  | .zaid c :: w => c :: zaids w

/-- الاسترجاع: إعادة النسج بالقناع. -/
def rebuild : List Bool → List Nat → List Nat → Word
  | [], _, _ => []
  | true :: m, a, z :: zs => .zaid z :: rebuild m a zs
  | false :: m, c :: cs, z => .asl c :: rebuild m cs z
  | _, _, _ => []

/-- ج-١: الطيّ ثم الاسترجاع يعيد الكلمة نفسها — لا ضائع. -/
theorem rebuild_fold (w : Word) : rebuild (mask w) (asls w) (zaids w) = w := by
  induction w with
  | nil => rfl
  | cons s w ih =>
    cases s with
    | asl c => simp [mask, asls, zaids, Seg.isZaid, rebuild] at *; exact ih
    | zaid c => simp [mask, asls, zaids, Seg.isZaid, rebuild] at *; exact ih

/-- ج-٢: الحفظ — عدد الأصول + عدد الزوائد = طول الكلمة. -/
theorem fold_conserves (w : Word) : (asls w).length + (zaids w).length = w.length := by
  induction w with
  | nil => rfl
  | cons s w ih =>
    cases s <;> simp [asls, zaids] <;> omega

/-- التقشير التامّ: حذف كل زائد. -/
def peelAll : Word → Word := List.filter (fun s => !s.isZaid)

/-- ج-٣: ما بعد التقشير التامّ لا زائد فيه (لا بقيّة). -/
theorem peelAll_clean (w : Word) : ∀ s ∈ peelAll w, s.isZaid = false := by
  intro s hs
  simp [peelAll, List.mem_filter] at hs
  exact hs.2

/-- ج-٤: التقشير التامّ يُبقي الأصول بترتيبها، بلا زيادة ولا نقص. -/
theorem peelAll_eq_asls (w : Word) : peelAll w = (asls w).map Seg.asl := by
  induction w with
  | nil => rfl
  | cons s w ih =>
    cases s <;> simp [peelAll, asls, Seg.isZaid, List.filter] at * <;> exact ih

end Ghanem

#print axioms Ghanem.doc_gate_signature_vacuous
#print axioms Ghanem.licensed_succ_iff
#print axioms Ghanem.table116_oneGap_incomplete
#print axioms Ghanem.rebuild_fold
#print axioms Ghanem.fold_conserves
#print axioms Ghanem.peelAll_eq_asls
