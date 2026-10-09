import Slge.MukhassasTable
import Slge.Maqayis

/-!
# شجرةُ المخصّص: الأجناسُ والقابليّاتُ معلوماتٍ سابقةً، والحكمُ عليها ثلاثيًّا بشاهد

المخصّصُ مختومٌ «وضعًا» (روايةُ الوضع الأوّل)؛ يُشتقّ منه هنا جدولُ **معلوماتٍ سابقة**: شجرةُ عناوينه كما هي
(`nodes`: معرّف، مستوى، أب، كتاب، وجذورُ العنوان **بالرسم** في جدول المقاييس). المبرهَن:

* **شجرة**: المعرّفاتُ مواضع (`ids_are_positions`)؛ الأبُ أسبقُ من ابنه (`parent_lt`: لا دور) وأدنى مستوًى، وكتابُ
  الابن كتابُ أبيه (`parent_level_lt`)؛ المستوى الأوّل وحدَه بلا أب وكتابُه نفسُه (`level_one_iff_no_parent`)؛ كتابُ
  كلّ عقدةٍ من المستوى الأوّل (`book_is_level_one`)؛ الأعدادُ بالمستوى (`level_counts`). فالكتابُ ما تبلغه مطاردةُ الأب — **مكتوبٌ** عامًّا (`chase_eq_book`: استقراءٌ على الوقود فوق خواصّ
  العقد المقرَّرة `nodes_ok`).
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

/-! ## الاستقراءُ العامّ: الكتابُ ما تبلغه مطاردةُ الأب

كان مكتوبًا أعلاه أنّ الاستقراءَ العامّ «غيرُ مكتوبٍ في Lean». هنا يُكتب: خواصُّ العقدة الواحدة بمؤشّرها
تُقرَّر على الجدول (`nodes_ok` — فحصٌ منتهٍ على 1,600 عقدة، كلُّ عقدةٍ في اليد)، ثمّ **الاستقراءُ على الوقود** عامٌّ لا يَعدّ:
مطاردةُ الأب من أيّ عقدةٍ تبلغ كتابَها (`chase_eq_book`)، والوقودُ i يكفي لأنّ الأبَ أسبقُ من ابنه. -/

/-- مطاردةُ الأب بوقود: من `i` صعودًا حتى عقدةٍ بلا أب. -/
def chase : Nat → Nat → Nat
  | 0, i => i
  | fuel + 1, i => if parentOf i < 0 then i else chase fuel (parentOf i).toNat

/-- خواصُّ العقدة الواحدة (وهي في اليد): أبوها أسبقُ منها؛ بلا أبٍ فكتابُها نفسُها، وبأبٍ فكتابُها كتابُ أبيها. -/
def nodeOK (n : Node) : Bool :=
  decide (n.2.2.1 < (n.1 : Int)) &&
    (if n.2.2.1 < 0 then n.2.2.2.1 == n.1 else bookOf n.2.2.1.toNat == n.2.2.2.1)

set_option maxRecDepth 100000 in
theorem nodes_ok : nodes.all nodeOK = true := by decide +kernel

theorem node_mem (i : Nat) (h : i < nodes.length) : node i ∈ nodes := by
  unfold node
  rw [← List.getElem_eq_getD (h := h)]
  exact List.getElem_mem h

/-- المعرّفُ موضعُه، بمؤشّره (من `ids_are_positions`). -/
theorem node_id (i : Nat) (h : i < nodes.length) : (node i).1 = i := by
  have hall := List.all_eq_true.mp ids_are_positions
  have hlen : i < ((List.range nodes.length).zip nodes).length := by
    simp [List.length_zip, h]
  have hmem := List.getElem_mem hlen
  rw [List.getElem_zip, List.getElem_range] at hmem
  have := hall _ hmem
  simp only [beq_iff_eq] at this
  unfold node
  rw [← List.getElem_eq_getD (h := h)]
  exact this

theorem nodeOK_unfold {i : Nat} (h : i < nodes.length) :
    parentOf i < (i : Int) ∧
      (parentOf i < 0 → bookOf i = i) ∧ (¬ parentOf i < 0 → bookOf (parentOf i).toNat = bookOf i) := by
  have hok := List.all_eq_true.mp nodes_ok _ (node_mem i h)
  have hid := node_id i h
  unfold nodeOK at hok
  simp only [Bool.and_eq_true, decide_eq_true_eq] at hok
  unfold parentOf bookOf
  rw [hid] at hok
  refine ⟨hok.1, fun hp => ?_, fun hp => ?_⟩
  · rw [ite_eq_left hp] at hok; exact beq_iff_eq.mp hok.2
  · rw [ite_eq_right hp] at hok; exact beq_iff_eq.mp hok.2

/-- **الاستقراءُ العامّ**: من أيّ عقدةٍ بوقودٍ لا يقلّ عن مؤشّرها تبلغ المطاردةُ كتابَها. -/
theorem chase_eq_book : ∀ (fuel i : Nat), i < 1600 → i ≤ fuel → chase fuel i = bookOf i
  | 0, i, hi, hf => by
    have : i = 0 := Nat.le_zero.mp hf
    subst this
    decide
  | fuel + 1, i, hi, hf => by
    obtain ⟨hlt, hroot, hstep⟩ := nodeOK_unfold (by rw [nodes_length]; exact hi)
    simp only [chase]
    split
    · exact (hroot ‹_›).symm
    · rename_i hp
      have hp' : 0 ≤ parentOf i := Int.not_lt.mp hp
      have hpn : (parentOf i).toNat < i := by
        have := Int.toNat_lt_toNat (by omega : (0 : Int) < i) |>.mpr hlt
        simpa using this
      rw [chase_eq_book fuel (parentOf i).toNat (by omega) (by omega)]
      exact hstep hp

/-- بوقودٍ قدرِ المؤشّر. -/
theorem chase_self (i : Nat) (hi : i < 1600) : chase i i = bookOf i := chase_eq_book i i hi (Nat.le_refl i)

/-- شاهدان: 163 كتابٌ قائم (بلا أب)، و 3 تحت 2 تحت 1. -/
theorem chase_witnesses : chase 163 163 = 163 ∧ chase 3 3 = 1 ∧ chase 2 2 = 1 := by decide +kernel

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
