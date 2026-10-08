import Slge.Bridge
import Slge.MakharijTable

/-!
# المخارجُ والصفات عند سيبويه — الحدُّ الأدنى المكتمل

المصدرُ «باب عدد الحروف العربية ومخارجها ومهموسها ومجهورها» (الكتابُ المختوم؛ الجدولُ `MakharijTable`
مولَّدٌ منه). الحرفُ عند هذه الطبقة لا يُستورد من الـ116 بل يُثبَت أنّه هو: ترتيبُ سيبويه **تبديلٌ** للحوامل
التسعة والعشرين (`order_is_the_alphabet`)، فالصفةُ تقع على الحامل نفسه الذي تقع عليه الحالةُ في الخانة.

* **المخارج**: المعدودُ في النشرة 15 والمنطوقُ 16، والساقطُ مخرجُ اللام وحدَه — نقصٌ مسمًّى لا مرمَّم
  (`lacuna_is_lam`)؛ ما عدا اللام مغطًّى، والنونُ وحدَها في مخرجين (طرفُ اللسان والخياشيم للخفيفة).
* **الجهرُ والهمس** قسمةٌ تامّة للتسعة والعشرين (`jahr_partition`): 19 + 10 كما نطق النصّ.
* **الشدّةُ والرخاوةُ وما بينهما** قسمةٌ تامّة (`shidda_partition`): 8 شديدة، 13 رخوة، 8 بينَ بين
  (العين، والمنحرف، والغنّة، والمكرّر، واللينتان، والهاوي).
* **الإطباقُ والانفتاح** قسمةٌ تامّة (`itbaq_partition`): 4 + 25.
كلُّ ذلك بـ`decide` على الجدول: مبرهَنٌ على المودَع لا «لكلّ».
-/

namespace Slge.Makharij

/-- الحواملُ كلُّها. -/
def all : List Nat := List.range 29

theorem order_is_the_alphabet : order.length = 29 ∧ order.Nodup ∧ order.all (· < 29) = true := by decide

/-- اتّحادُ المخارج. -/
def covered : List Nat := makharij.flatten

theorem lacuna_is_lam :
    makharij.length = 15 ∧ statedCount = 16 ∧ missing = [23] ∧
    (all.filter (fun k => !covered.contains k)) = missing := by decide

/-- النونُ (25) وحدَها تقع في مخرجين؛ وما سواها في مخرجٍ واحد. -/
theorem nun_twice :
    (all.filter (fun k => (makharij.filter (·.contains k)).length ≥ 2)) = [25] := by decide

def disjoint (a b : List Nat) : Bool := a.all (fun k => !b.contains k)

theorem jahr_partition :
    majhura.length = 19 ∧ mahmusa.length = 10 ∧ disjoint majhura mahmusa = true ∧
    all.all (fun k => majhura.contains k || mahmusa.contains k) = true := by decide

/-- بينَ الشديدة والرخوة: العينُ والمنحرفُ والغنّةُ والمكرّرُ واللينتان والهاوي. -/
def bayn : List Nat := baynBayn ++ munharif ++ ghunna ++ mukarrar ++ layyina ++ hawi

theorem shidda_partition :
    shadida.length = 8 ∧ rikhwa.length = 13 ∧ bayn.length = 8 ∧
    disjoint shadida rikhwa = true ∧ disjoint shadida bayn = true ∧ disjoint rikhwa bayn = true ∧
    all.all (fun k => shadida.contains k || rikhwa.contains k || bayn.contains k) = true := by decide

theorem itbaq_partition :
    mutbaqa.length = 4 ∧ munfatiha.length = 25 ∧ disjoint mutbaqa munfatiha = true ∧
    all.all (fun k => mutbaqa.contains k || munfatiha.contains k) = true := by decide

/-- المطبقةُ الأربعُ من مخارج طرف اللسان وحافته (الصاد والضاد والطاء والظاء)، وكلُّها مجهورةٌ إلّا الصاد. -/
theorem mutbaqa_witness : mutbaqa = [14, 15, 16, 17] ∧
    (mutbaqa.filter majhura.contains) = [15, 16, 17] := by decide

end Slge.Makharij
