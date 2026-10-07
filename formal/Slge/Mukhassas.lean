import Slge.MukhassasTable
import Slge.Maqayis

/-!
# شجرةُ المخصّص: الأجناسُ والقابليّاتُ معلوماتٍ سابقةً، والحكمُ عليها ثلاثيًّا بشاهد

المخصّصُ مختومٌ «وضعًا» (روايةُ الوضع الأوّل)؛ يُشتقّ منه هنا جدولُ **معلوماتٍ سابقة**: شجرةُ عناوينه كما هي
(`nodes`: معرّف، مستوى، أب، كتاب، وجذورُ العنوان **بالرسم** في جدول المقاييس). المبرهَن:

* **شجرة**: المعرّفاتُ مواضع (`ids_are_positions`)؛ الأبُ أسبقُ من ابنه (`parent_lt`: لا دور) وأدنى مستوًى، وكتابُ
  الابن كتابُ أبيه (`parent_level_lt`)؛ المستوى الأوّل وحدَه بلا أب وكتابُه نفسُه (`level_one_iff_no_parent`)؛ كتابُ
  كلّ عقدةٍ من المستوى الأوّل (`book_is_level_one`)؛ الأعدادُ بالمستوى (`level_counts`). فالكتابُ، بالاستقراء على
  `parent_lt`، ما تبلغه مطاردةُ الأب — الاستقراءُ العامّ غيرُ مكتوبٍ في Lean (الفحصُ الشامل في `test_conformance`).
* **القابليّات**: `caps` العقدُ ذاتُ الجذور (بالتعريف)، و`capsUnder b` اتّحادُ جذور عناوين ما تحت الكتاب `b`
  **بالتعريف** — فكلُّ قابليّةٍ موروثة شهد بها عنوانٌ تحت الكتاب، ولا قابليّةَ بلا عنوان؛ وعددُ العقد المربوطة
  (`caps_length`).
* **الحكم** (المادّتان ١٣ و١٦): `judge n r` مرتبتان — `mafhum w` بشاهدٍ `w` عقدةٌ في كتاب `n` عنوانُها يحمل الجذر
  `r` (`mafhum_has_witness`: لا «مفهوم» بلا شاهد؛ `mafhum_in_capsUnder`)، أو `malumah` (لا شاهد — لا رفضَ ولا
  امتناع: الغيابُ ليس امتناعًا، `judge_total`).
* **شواهد**: جذرُ «مشي» مفهومٌ تحت «أبواب المشي» (163) ومعلومةٌ تحت «كتاب خلق الإنسان» (1) — فالمشيُ عند ابن سيده
  كتابٌ قائمٌ لا بابٌ تحت الإنسان؛ وجذرُ «جري» معلومةٌ تحت «كتاب النخل» (979): النخلةُ لا شاهدَ لجريها.

الربطُ بالرسم (النصُّ غيرُ مشكول) وقاعدةُ ألفاظ الهيكل **معلَنان** في `tools/deposit_mukhassas.py`؛ الشجرةُ منقولةٌ
بلا إعادة تصنيف. هذه أوّلُ وحدةٍ في طبقة «الحكم» فوق سُلَّم الترخيص (المادّة ١٠): لا تدخل السُّلَّم ولا تمسّ شهادة.
-/

namespace Slge.Mukhassas

abbrev Node := Nat × Nat × Int × Nat × List Nat

def node (i : Nat) : Node := nodes.getD i (0, 0, 0, 0, [])
def levelOf (i : Nat) : Nat := (node i).2.1
def parentOf (i : Nat) : Int := (node i).2.2.1
def bookOf (i : Nat) : Nat := (node i).2.2.2.1
def rootsOf (i : Nat) : List Nat := (node i).2.2.2.2

/-- العقدُ ذاتُ الجذور. -/
def caps : List Node := nodes.filter (fun n => !n.2.2.2.2.isEmpty)

/-- القابليّاتُ الموروثة للكتاب `b`: اتّحادُ جذور عناوين ما تحته، بالتعريف. -/
def capsUnder (b : Nat) : List Nat := (nodes.filter (fun n => n.2.2.2.1 == b)).flatMap (·.2.2.2.2)

/-! ## شجرة -/

set_option maxRecDepth 100000 in
theorem ids_are_positions :
    ((List.range nodes.length).zip nodes).all (fun q => q.2.1 == q.1) = true := by decide

set_option maxRecDepth 100000 in
/-- الأبُ أسبقُ من ابنه: لا دورَ في الشجرة. -/
theorem parent_lt : nodes.all (fun n => n.2.2.1 < (n.1 : Int)) = true := by decide

set_option maxRecDepth 100000 in
/-- المستوى الأوّل وحدَه بلا أب، وكتابُه نفسُه. -/
theorem level_one_iff_no_parent :
    nodes.all (fun n => ((n.2.1 == 1) == (n.2.2.1 == -1)) && (n.2.1 != 1 || n.2.2.2.1 == n.1)) = true := by
  decide

set_option maxRecDepth 100000 in
theorem level_counts :
    (nodes.filter (fun n => n.2.1 == 1)).length = 73 ∧ (nodes.filter (fun n => n.2.1 == 2)).length = 337 ∧
    (nodes.filter (fun n => n.2.1 == 3)).length = 1190 := by decide

set_option maxRecDepth 100000 in
theorem caps_length : caps.length = 1080 := by decide

set_option maxRecDepth 100000 in
/-- الأبُ أدنى مستوًى من ابنه (لا يلزم أن يكون أدنى بواحد: المصدرُ يقفز أحيانًا من كتابٍ إلى فصل)،
وكتابُ الابن كتابُ أبيه. -/
theorem parent_level_lt :
    nodes.all (fun n => n.2.2.1 < 0 ||
      (levelOf n.2.2.1.toNat < n.2.1 && bookOf n.2.2.1.toNat == n.2.2.2.1)) = true := by decide +kernel

set_option maxRecDepth 100000 in
theorem book_is_level_one : nodes.all (fun n => levelOf n.2.2.2.1 == 1) = true := by decide +kernel

/-! ## الحكم -/

/-- مرتبتا الحكم على (عقدة، جذر): مفهومٌ بشاهدٍ أو معلومةٌ بلا شاهد (المادّة ١٥؛ «من حيث هي» مرتبةُ الدالّ لا
تُصدر من هنا). -/
inductive Grade where
  | malumah
  | mafhum (witness : Nat)
  deriving DecidableEq, Repr

/-- الحكمُ داخل كتابٍ `b`: أوّلُ عقدةٍ فيه يحمل عنوانُها الجذر. -/
def judgeIn (b r : Nat) : Grade :=
  match nodes.find? (fun n => n.2.2.2.1 == b && n.2.2.2.2.contains r) with
  | some n => .mafhum n.1
  | none => .malumah

def judge (n r : Nat) : Grade := judgeIn (bookOf n) r

/-- لا «مفهوم» بلا شاهد: الشاهدُ عقدةٌ مسجَّلةٌ في الشجرة، في كتاب `n`، يحمل عنوانُها الجذر. -/
theorem mafhum_has_witness (n r w : Nat) (h : judge n r = .mafhum w) :
    ∃ p ∈ nodes, p.1 = w ∧ p.2.2.2.1 = bookOf n ∧ p.2.2.2.2.contains r = true := by
  unfold judge judgeIn at h
  split at h
  · rename_i p hp
    have hw : w = p.1 := by cases h; rfl
    have hpred := List.find?_some hp
    have hmem := List.mem_of_find?_eq_some hp
    subst hw
    simp only [Bool.and_eq_true, beq_iff_eq] at hpred
    exact ⟨p, hmem, rfl, hpred.1, hpred.2⟩
  · cases h

/-- المفهومُ شاهدُه في القابليّات الموروثة لكتابه. -/
theorem mafhum_in_capsUnder (n r w : Nat) (h : judge n r = .mafhum w) : r ∈ capsUnder (bookOf n) := by
  obtain ⟨p, hmem, _, hb, hc⟩ := mafhum_has_witness n r w h
  unfold capsUnder
  simp only [List.mem_flatMap, List.mem_filter, beq_iff_eq]
  exact ⟨p, ⟨hmem, hb⟩, List.contains_iff_mem.mp hc⟩

/-- الحكمُ تامٌّ ولا رفضَ فيه. -/
theorem judge_total (n r : Nat) : judge n r = .malumah ∨ ∃ w, judge n r = .mafhum w := by
  cases h : judge n r with
  | malumah => exact Or.inl rfl
  | mafhum w => exact Or.inr ⟨w, rfl⟩

set_option maxRecDepth 100000 in
/-- مشي (22018) مفهومٌ تحت أبواب المشي (163) ومعلومةٌ تحت كتاب خلق الإنسان (1)؛ جري (4829) معلومةٌ تحت كتاب
النخل (979). -/
theorem witnesses :
    judgeIn 163 22018 = .mafhum 163 ∧ judgeIn 1 22018 = .malumah ∧ judgeIn 979 4829 = .malumah ∧
    bookOf 163 = 163 ∧ bookOf 1 = 1 ∧ bookOf 979 = 979 ∧ levelOf 979 = 1 ∧ levelOf 163 = 1 := by
  decide +kernel

end Slge.Mukhassas
