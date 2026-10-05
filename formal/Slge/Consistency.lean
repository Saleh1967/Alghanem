import Slge.Bridge

/-!
# اتّساقُ العددين: عددُ الشهادة وعددُ الطيّ شيءٌ واحدٌ بوجهين

للكلمة عددان: **عددُ الطيّ** `slgeFold` (كثيفٌ: ‎n < U(k)‎، مبرهَنٌ تقابلًا على المرخَّصات بطول ‎k‎)،
و**عددُ الذرّات** `A116.Numbering.atomNumber` (ترقيمٌ بأساس 116 لكلّ سلسلة، وهو ما تحمله شهادةُ
بوّابة الغانم). ولا يجوز أن يختلفا في الحكم: كلٌّ منهما يحدّد الكلمةَ، فيحدّد الآخر.

* `atomNumber_determines_fold`: تساوي عددَي الذرّات ⟹ تساوي عددَي الطيّ.
* `fold_determines_atomNumber`: تساوي عددَي الطيّ (بطولٍ واحد، مرخَّصتين) ⟹ تساوي عددَي الذرّات.
* `numbers_agree`: فالعددان متكافئان على المرخَّصات بطولٍ واحد.
-/

namespace Slge.Consistency

open A116 A116.Numbering

/-- عددُ الذرّات لكلمة SLGE بعد الجسر. -/
def atomNumberS (w : List SCell) : Nat := atomNumber (w.map toCell)

theorem atomNumberS_injective {w w' : List SCell} (h : atomNumberS w = atomNumberS w') :
    w = w' :=
  map_toCell_injective (atomNumber_injective h)

theorem atomNumber_determines_fold {w w' : List SCell} (h : atomNumberS w = atomNumberS w') :
    slgeFold w = slgeFold w' := by
  rw [atomNumberS_injective h]

theorem fold_determines_atomNumber {w w' : List SCell} (hw : licensed w = true)
    (hw' : licensed w' = true) (hlen : w.length = w'.length) (h : slgeFold w = slgeFold w') :
    atomNumberS w = atomNumberS w' := by
  rw [slgeFold_injective hw hw' hlen h]

/-- **العددان متكافئان** على مرخَّصتين بطولٍ واحد. -/
theorem numbers_agree {w w' : List SCell} (hw : licensed w = true) (hw' : licensed w' = true)
    (hlen : w.length = w'.length) :
    slgeFold w = slgeFold w' ↔ atomNumberS w = atomNumberS w' :=
  ⟨fold_determines_atomNumber hw hw' hlen, atomNumber_determines_fold⟩

end Slge.Consistency
