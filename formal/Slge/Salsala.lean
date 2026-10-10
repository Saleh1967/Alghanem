import Slge.SalsalaTable

/-!
# السلسلة: أركانُ المدلول الكونيّ على سلالم النبهانيّ الثلاثة (ADR ٣١)

جدولُ المالك العشرون أُعيد ترتيبُه على ثلاثة سلالم، وكلُّ ركنٍ **مربوطٌ بسطره** من المختومَين (ج3، «التفكير») في
`SalsalaTable` — أو معلَنٌ بقرار المالك باسمه (`declared`) لا من الذاكرة:

* **(أ) المعلوماتُ السابقة** (`ladder = 0`): الجذرُ الأركانُ الأربعة (واقع، إحساس، ذهن، معلومات سابقة — ج3 393،
  التفكير 24)؛ ثمّ الوجودُ والحقائقُ **يقينًا** (التفكير 65، 123)، والكنهُ والأجناسُ والصفاتُ والخواصُّ والقابليّاتُ
  والحدثُ والزمانُ والمكانُ والعددُ **ظنًّا** («نتيجة ظنية عن كنه الشيء وصفته»).
* **(ب) الوضعُ والنسب** (`ladder = 1`): التسميةُ (الوضع، فرعُ التصوّر، تُعرف بالأخذ عنهم)، ثمّ النسبُ الثلاث
  إسنادٌ وتقييدٌ وإضافة — لا «تضمينيّة» — والفاعليّةُ والمفعوليّةُ نسبتان، والإفادةُ شرطُ عدم الهذيان (ج3 393، 414).
* **(ج) الحكم: علاقاتُ المجاز** (`ladder = 2`): العلاقةُ والسببيّةُ (أربعة) والمسببيّة (ج3 432–434) — من طبقة
  الحكم لا من الواقع.

المبرهَن هنا بناءُ الجدول لا اللغة: السلالمُ ثلاثةٌ تغطّي الأركان (`ladders_cover`)؛ اليقينُ للوجود والحقائق
وحدَهما (`certain_iff`)، وما في السلّمين (ب) و(ج) بلا مرتبة حكمٍ (`wad_hukm_ungraded`)؛ لا ركنَ اسمُه التضمين
(`no_tadmin`)، والنسبُ الثلاث بأسمائها بعد الوضع (`nisab_three`)؛ كلُّ سالفٍ أسبقُ من ركنه فلا دور
(`salaf_earlier`)؛ وكلُّ ركنٍ مرسًى بسطرٍ أو معلَنٌ باسمه ولا ثالث (`anchored_or_declared`)؛ والجذرُ الأركانُ
الأربعة (`root_is_arkan`).
-/

namespace Slge.Salsala

open SalsalaTable

/-- الركنُ برقمه. -/
def rukn (i : Nat) : Option Rukn := rows.find? (·.id == i)

def certain (r : Rukn) : Bool := r.grade == 0

/-- السلالمُ ثلاثةٌ لا رابع. -/
theorem ladders_cover : rows.all (·.ladder < 3) = true := by decide

/-- اليقينُ للوجود (1) والحقائق (2) وحدَهما — «قطعية عن وجود الشيء… ظنية عن كنهه وصفته». -/
theorem certain_iff : rows.all (fun r => (r.grade == 0) == (r.id == 1 || r.id == 2)) = true := by
  decide

/-- الوضعُ والنسبُ والمجازُ ليست أحكامًا على واقعٍ فلا مرتبةَ لها. -/
theorem wad_hukm_ungraded : rows.all (fun r => r.ladder == 0 || r.grade == 2) = true := by decide

/-- لا ركنَ اسمُه «التضمين»: النسبُ إسناديّةٌ وتقييديّةٌ وإضافيّة. -/
theorem no_tadmin : rows.all (fun r => r.name != "التضمين" && r.name != "التضمينية") = true := by
  decide

/-- النسبُ الثلاث بأسمائها وبترتيب النصّ، كلُّها بعد الوضع (12). -/
theorem nisab_three :
    (rows.filter (fun r => r.id == 13 || r.id == 14 || r.id == 15)).map (·.name)
      = ["الإسناد", "التقييد", "الإضافة"] ∧
    (rows.filter (fun r => r.id == 13 || r.id == 14 || r.id == 15)).all (·.salaf.contains 12)
      = true := by decide

/-- كلُّ سالفٍ أسبقُ من ركنه: لا دور. -/
theorem salaf_earlier : rows.all (fun r => r.salaf.all (· < r.id)) = true := by decide

/-- كلُّ ركنٍ إمّا مرسًى بسطرٍ من المختوم وإمّا معلَنٌ باسمه، ولا ثالث. -/
theorem anchored_or_declared :
    rows.all (fun r => (r.anchors.isEmpty) == declared.contains r.id) = true := by decide

/-- الجذرُ الأركانُ الأربعة، بلا سالف. -/
theorem root_is_arkan :
    (rukn 0).map (·.name) = some "الأركان الأربعة" ∧ (rukn 0).map (·.salaf) = some [] := by decide

/-- الأركانُ 22: اثنا عشر في المعلومات السابقة، سبعةٌ في الوضع والنسب، ثلاثةٌ في المجاز. -/
theorem ladder_counts :
    (rows.filter (·.ladder == 0)).length = 12 ∧ (rows.filter (·.ladder == 1)).length = 7 ∧
    (rows.filter (·.ladder == 2)).length = 3 := by decide

end Slge.Salsala
