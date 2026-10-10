import Slge.AjnasTable
import Slge.SalsalaTable
import Slge.Mukhassas
import Slge.Shahada

/-!
# الحكم: من جذور الشهادة إلى ركنٍ من السلسلة بمرتبته وشاهده، أو «لا حكم» (ADR ٣٤)

أوّلُ دالّةِ حكمٍ تستهلك جدولَ السلسلة (`SalsalaTable`) ومودَعَ المعلومات السابقة (`AjnasTable`: الأجناسُ
والقابليّاتُ من المخصّص بشاهدها). المدخلُ جذورُ قراءات الشهادة (أعدادٌ من جدول المقاييس، كما يقرؤها الجذعُ)؛
والمخرجُ لكلّ جذرٍ حكمان على ركنَين من السلّم الأوّل (المعلومات السابقة): **الأجناسُ والأنواع** (الركن 4:
الجذرُ اسمُ كتابٍ في المخصّص — شاهدُه الكتاب) و**القابليّات** (الركن 7، وكان معلَنًا بلا مرساةٍ في النبهانيّ:
الجذرُ في عنوان عقدةٍ تحت كتاب — شاهدُه تلك العقدة)؛ كلٌّ «مفهومٌ» بشاهدٍ من المودَع أو «معلومةٌ» بلا شاهد
(المادّتان ١٣ و١٦)؛ وإن لم يكن للشهادة جذرٌ فـ**لا حكم** باسمه. المرتبةُ من جدول السلسلة نفسِه (`gradeOf`).

المبرهَن:
* **لا حكمَ إلّا بلا جذر** (`hukm_none_iff`)، و**لا يُسقط ولا يزيد**: لكلّ جذرٍ حكمُه وبعدد الجذور
  (`hukm_length`، `hukm_mem`)؛ والترتيبُ مفهومًا أوّلًا لا يحذف (`mem_rank`، `length_rank`).
* **لا «مفهوم» بلا شاهد** من المودَع: شاهدُ الجنس كتابٌ في `genera` جذورُ عنوانه تحمل الجذر
  (`jins_mafhum_has_witness`)، وشاهدُ القابليّة عقدةٌ مسجَّلةٌ في جدول القابليّات (`qabiliyya_mafhum_has_witness`)
  — وهي عقدةٌ في **شجرة المخصّص** تحت ذلك الكتاب، من مستوًى ثانٍ فأعلى، يحمل عنوانُها الجذر
  (`caps_are_tree_nodes`، `qabiliyya_witness_in_tree`).
* **الحكمُ تامّ**: مفهومٌ أو معلومة، لا رفض (`judge_total`)، والركنان في عمود النبهانيّ بمرتبة الظنّ
  (`ranks_in_spine`)، والحكمُ لا يمسّ الشهادة (`shahada_untouched`: بصمتُها كما هي — المادّة ١٣).
* **شاهدٌ من الواقع المودَع للركن المعلَن**: «مشي» جنسٌ تحت «أبواب المشي» (163)، و«ولد» قابليّةٌ لكتاب
  خلق الإنسان بعقدة باب الحمل والولادة (2) (`witnesses`).
-/

namespace Slge.Hukm

open Slge.AjnasTable (genera Genus)

/-- ركنا السلسلة اللذان يحكم عليهما هذا الحكم. -/
def JINS : Nat := 4
def QABILIYYA : Nat := 7

/-- مرتبةُ الركن من جدول السلسلة نفسِه (2 = بلا مرتبة إن لم يوجد). -/
def gradeOf (rukn : Nat) : Nat :=
  match SalsalaTable.rows.find? (·.id == rukn) with
  | some r => r.grade
  | none => 2

/-- حكمٌ على ركن: مفهومٌ بشاهدٍ من المودَع، أو معلومةٌ بلا شاهد. -/
inductive Judgement where
  | malumah (rukn : Nat)
  | mafhum (rukn witness : Nat)
  deriving DecidableEq, Repr

def Judgement.rukn : Judgement → Nat
  | .malumah k => k
  | .mafhum k _ => k

def Judgement.isMafhum : Judgement → Bool
  | .malumah _ => false
  | .mafhum _ _ => true

/-- الجنس: أوّلُ كتابٍ جذورُ عنوانه تحمل الجذر. -/
def judgeJins (r : Nat) : Judgement :=
  match genera.find? (fun g => g.roots.contains r) with
  | some g => .mafhum JINS g.book
  | none => .malumah JINS

/-- القابليّة: أوّلُ عقدةٍ شاهدةٍ في جدول القابليّات تحمل الجذر. -/
def judgeQabiliyya (r : Nat) : Judgement :=
  match genera.findSome? (fun g => (g.caps.find? (·.1 == r)).map (·.2)) with
  | some w => .mafhum QABILIYYA w
  | none => .malumah QABILIYYA

/-- حكمُ الجذر الواحد: (الجذر، حكمُ الجنس، حكمُ القابليّة). -/
abbrev Row := Nat × Judgement × Judgement

def judgeRoot (r : Nat) : Row := (r, judgeJins r, judgeQabiliyya r)

/-- الحكمُ على جذور الشهادة: لا حكمَ بلا جذر، وإلّا لكلّ جذرٍ حكمُه. -/
def hukm (roots : List Nat) : Option (List Row) :=
  if roots.isEmpty then none else some (roots.map judgeRoot)

/-- الترتيب: ما فيه مفهومٌ أوّلًا، ولا شيءَ يُحذف. -/
def hasMafhum (x : Row) : Bool := x.2.1.isMafhum || x.2.2.isMafhum

def rank (l : List Row) : List Row := l.filter hasMafhum ++ l.filter (fun x => !hasMafhum x)

/-- الحكمُ لا يمسّ الشهادة: يُلحق بها ولا يغيّرها. -/
def withHukm (s : Shahada.Shahada) (roots : List Nat) : Shahada.Shahada × Option (List Row) :=
  (s, hukm roots)

/-! ## لا حكمَ إلّا بلا جذر؛ ولا إسقاطَ ولا زيادة -/

theorem hukm_none_iff (roots : List Nat) : hukm roots = none ↔ roots = [] := by
  unfold hukm
  cases roots <;> simp

theorem hukm_length (roots : List Nat) (l : List Row) (h : hukm roots = some l) :
    l.length = roots.length := by
  unfold hukm at h
  split at h
  · cases h
  · cases h; simp

theorem hukm_mem (roots : List Nat) (l : List Row) (h : hukm roots = some l) (r : Nat) :
    r ∈ roots ↔ (r, judgeJins r, judgeQabiliyya r) ∈ l := by
  unfold hukm at h
  split at h
  · cases h
  · cases h
    constructor
    · intro hr; exact List.mem_map.mpr ⟨r, hr, rfl⟩
    · intro hm
      obtain ⟨x, hx, hxe⟩ := List.mem_map.mp hm
      have : x = r := by simp [judgeRoot] at hxe; exact hxe.1.symm ▸ rfl
      exact this ▸ hx

theorem mem_rank (l : List Row) (x : Row) : x ∈ rank l ↔ x ∈ l := by
  simp only [rank, List.mem_append, List.mem_filter, Bool.not_eq_true']
  constructor
  · rintro (⟨h, _⟩ | ⟨h, _⟩) <;> exact h
  · intro h
    cases ha : hasMafhum x
    · exact Or.inr ⟨h, rfl⟩
    · exact Or.inl ⟨h, rfl⟩

theorem length_rank : ∀ l : List Row, (rank l).length = l.length
  | [] => rfl
  | x :: l => by
    have ih := length_rank l
    simp only [rank, List.length_append] at ih ⊢
    cases ha : hasMafhum x <;> simp [ha] <;> omega

/-! ## لا «مفهوم» بلا شاهدٍ من المودَع -/

theorem jins_mafhum_has_witness (r k w : Nat) (h : judgeJins r = .mafhum k w) :
    k = JINS ∧ ∃ g ∈ genera, g.book = w ∧ g.roots.contains r = true := by
  unfold judgeJins at h
  split at h
  · rename_i g hg
    have hw : w = g.book := by cases h; rfl
    have hk : k = JINS := by cases h; rfl
    subst hw
    refine ⟨hk, g, List.mem_of_find?_eq_some hg, rfl, ?_⟩
    have := List.find?_some hg
    simpa using this
  · cases h

theorem qabiliyya_mafhum_has_witness (r k w : Nat) (h : judgeQabiliyya r = .mafhum k w) :
    k = QABILIYYA ∧ ∃ g ∈ genera, (r, w) ∈ g.caps := by
  unfold judgeQabiliyya at h
  split at h
  · rename_i w' hw'
    have hw : w = w' := by cases h; rfl
    have hk : k = QABILIYYA := by cases h; rfl
    subst hw
    obtain ⟨g, hg, hsome⟩ := List.exists_of_findSome?_eq_some hw'
    refine ⟨hk, g, hg, ?_⟩
    simp only [Option.map_eq_some_iff] at hsome
    obtain ⟨p, hp, hpw⟩ := hsome
    have hpr := List.find?_some hp
    have hmem := List.mem_of_find?_eq_some hp
    simp only [beq_iff_eq] at hpr
    have : p = (r, w) := by
      obtain ⟨a, b⟩ := p
      simp only at hpr hpw
      subst hpr hpw; rfl
    exact this ▸ hmem
  · cases h

set_option maxRecDepth 100000 in
/-- القابليّاتُ المودَعة عقدٌ من شجرة المخصّص: كلُّ (جذر، شاهد) في جنسٍ كتابُه `b` عقدةٌ تحت `b` من مستوًى
ثانٍ فأعلى، يحمل عنوانُها الجذر. -/
theorem caps_are_tree_nodes :
    genera.all (fun g => g.caps.all (fun p =>
      p.2 < 1600 && Mukhassas.bookOf p.2 == g.book && 2 ≤ Mukhassas.levelOf p.2 &&
        (Mukhassas.rootsOf p.2).contains p.1)) = true := by
  decide +kernel

/-- شاهدُ القابليّة عقدةٌ في الشجرة بعينها، في الكتاب الشاهد، تحمل الجذر. -/
theorem qabiliyya_witness_in_tree (r k w : Nat) (h : judgeQabiliyya r = .mafhum k w) :
    w < 1600 ∧ 2 ≤ Mukhassas.levelOf w ∧ (Mukhassas.rootsOf w).contains r = true ∧
      ∃ g ∈ genera, Mukhassas.bookOf w = g.book := by
  obtain ⟨_, g, hg, hc⟩ := qabiliyya_mafhum_has_witness r k w h
  have hall := List.all_eq_true.mp caps_are_tree_nodes g hg
  have hp := List.all_eq_true.mp hall (r, w) hc
  simp only [Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at hp
  exact ⟨hp.1.1.1, hp.1.2, hp.2, g, hg, hp.1.1.2⟩

set_option maxRecDepth 100000 in
/-- الأجناسُ المودَعة كتبُ الشجرة: كلُّ جنسٍ عقدةٌ من المستوى الأوّل جذورُها جذورُ عنوانه. -/
theorem genera_are_books :
    genera.all (fun g => g.book < 1600 && Mukhassas.levelOf g.book == 1 &&
      Mukhassas.rootsOf g.book == g.roots) = true := by
  decide +kernel

/-! ## الحكمُ تامٌّ ولا يمسّ الشهادة -/

theorem judge_total (j : Judgement) : (∃ k, j = .malumah k) ∨ ∃ k w, j = .mafhum k w := by
  cases j with
  | malumah k => exact Or.inl ⟨k, rfl⟩
  | mafhum k w => exact Or.inr ⟨k, w, rfl⟩

theorem judgeRoot_ranks (r : Nat) :
    (judgeRoot r).2.1.rukn = JINS ∧ (judgeRoot r).2.2.rukn = QABILIYYA := by
  simp only [judgeRoot, judgeJins, judgeQabiliyya]
  constructor <;> split <;> rfl

/-- الركنان في عمود النبهانيّ (السلّم الأوّل) بمرتبة الظنّ (التفكير 65). -/
theorem ranks_in_spine :
    gradeOf JINS = 1 ∧ gradeOf QABILIYYA = 1 ∧
      (SalsalaTable.rows.filter (fun x => x.id == JINS || x.id == QABILIYYA)).all (·.ladder == 0)
        = true := by
  decide

theorem shahada_untouched (s : Shahada.Shahada) (roots : List Nat) :
    (withHukm s roots).1 = s ∧ Shahada.fingerprint (withHukm s roots).1 = Shahada.fingerprint s :=
  ⟨rfl, rfl⟩

/-! ## شواهد من المودَع -/

set_option maxRecDepth 100000 in
/-- «مشي» (22018) جنسٌ بشاهد الكتاب 163، و«ولد» (24998) قابليّةٌ لكتاب خلق الإنسان بشاهد العقدة 2 — فالركنُ
المعلَن (القابليّات) له شاهدٌ من الواقع المودَع لا من نصّ. -/
theorem witnesses :
    judgeJins 22018 = .mafhum JINS 163 ∧ judgeQabiliyya 24998 = .mafhum QABILIYYA 2 ∧
      judgeJins 24998 = .malumah JINS ∧ hukm [] = none ∧
      (hukm [22018, 24998]).map List.length = some 2 := by
  decide +kernel

end Slge.Hukm
