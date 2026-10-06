import Slge.Afal

/-!
# أدواتُ الربط: فهرسةٌ على درجات الترخيص الجبريّ التدريجيّ

الأداةُ تُفهرَس بأعلى درجةٍ يبلغها البرهانُ فيها:
* **الخانة**: خاناتُها مرخَّصة (`particles_licensed`).
* **الحدّ**: الحرفُ الواحد المتحرّك (و، ف، ل، ب، ك، س) يتّصل بما بعده ولا يُفسد ترخيصَه
  (`proclitic_keeps_licence`، لكلّ كلمةٍ مرخَّصة).
* **العمل**: أثرُها في آخر ما بعدها دالّةٌ على الخانة الأخيرة (`govern`)؛ وعلى الأفعال الخمسة
  حذفُ النون جزمًا ونصبًا (`govern_jazm_afal`، `govern_nasb_afal`).
* **المعنى**: بابُها من الجدول المُرسَل — معلَنٌ في بايثون، لا هنا.
-/

namespace Slge.Rawabit

open Slge.Categories (c)

inductive Amal where
  | none | jazm | nasb | jarr | nasbIsm
  deriving DecidableEq, Repr

structure Particle where
  name : String
  cells : List SCell
  amal : Amal
  proclitic : Bool
  deriving Repr

/-- آخرُ الكلمة. -/
def lastState (w : List SCell) : Option (Fin 4) := (Afal.lastOf w).map SCell.state

/-- أيَحمل آخرُ الكلمة أثرَ العمل؟ -/
def govern (a : Amal) (w : List SCell) : Bool :=
  match a, lastState w with
  | .none, _ => true
  | _, Option.none => false
  | .jazm, some st => st.val == 3 || (Afal.pronounOf w != none && Afal.moodOf w != .raf)
  | .nasb, some st => st.val == 0 || (Afal.pronounOf w != none && Afal.moodOf w != .raf)
  | .jarr, some st => st.val == 1
  | .nasbIsm, some st => st.val == 0

/-- الجزمُ على الأفعال الخمسة: حذفُ النون. -/
theorem govern_jazm_afal (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) :
    govern .jazm (Afal.form pr s p .jazm) = true := by
  unfold govern lastState
  rw [← Afal.nasb_eq_jazm, Afal.moodOf_nasb, Afal.pronounOf_form]
  rw [Afal.form_nasb, Afal.lastOf_cons_append]; cases p <;> rfl

theorem govern_nasb_afal (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) :
    govern .nasb (Afal.form pr s p .nasb) = true := by
  unfold govern lastState
  rw [Afal.moodOf_nasb, Afal.pronounOf_form]
  rw [Afal.form_nasb, Afal.lastOf_cons_append]; cases p <;> rfl

/-- والرفعُ لا يحمل أثرَ الجزم: النونُ باقية. -/
theorem raf_not_governed_jazm (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) :
    govern .jazm (Afal.form pr s p .raf) = false := by
  unfold govern lastState
  rw [Afal.moodOf_raf, Afal.pronounOf_form, Afal.form_raf, Afal.lastOf_cons_append]; cases p <;> rfl

/-- الحرفُ المتحرّك المتّصل لا يُفسد ترخيصَ ما بعده. -/
theorem proclitic_keeps_licence (k : Fin 29) (st : Fin 4) (hst : st.val ≠ 3) (w : List SCell)
    (hw : licensed w = true) : licensed (⟨k, st⟩ :: w) = true := by
  cases w with
  | nil => simp [licensed, SCell.isSukun, noAdj, hst]
  | cons x t =>
    simp only [licensed, SCell.isSukun, noAdj] at hw ⊢
    simp only [Bool.and_eq_true, Bool.not_eq_eq_eq_not, Bool.not_true] at hw
    simp [hst, hw.2, hw.1]

/-- الأدواتُ المودَعة (90)، خاناتُها كما تُخرجها البوّابة. -/
def particles : List Particle := [
  ⟨"وَ", [c 27 0], .none, true⟩,
  ⟨"فَ", [c 20 0], .none, true⟩,
  ⟨"ثُمَّ", [c 4 2, c 24 3, c 24 0], .none, false⟩,
  ⟨"أَوْ", [c 0 0, c 27 3], .none, false⟩,
  ⟨"أَمْ", [c 0 0, c 24 3], .none, false⟩,
  ⟨"بَلْ", [c 2 0, c 23 3], .none, false⟩,
  ⟨"لَكِنْ", [c 23 0, c 22 1, c 25 3], .none, false⟩,
  ⟨"حَتَّى", [c 6 0, c 3 3, c 3 0, c 1 3], .jarr, false⟩,
  ⟨"قَدْ", [c 21 0, c 8 3], .none, false⟩,
  ⟨"لَمَّا", [c 23 0, c 24 3, c 24 0, c 1 3], .jazm, false⟩,
  ⟨"لَمْ", [c 23 0, c 24 3], .jazm, false⟩,
  ⟨"لَا", [c 23 0, c 1 3], .none, false⟩,
  ⟨"لَنْ", [c 23 0, c 25 3], .nasb, false⟩,
  ⟨"لَيْسَ", [c 23 0, c 28 3, c 12 0], .none, false⟩,
  ⟨"إِنَّمَا", [c 0 1, c 25 3, c 25 0, c 24 0, c 1 3], .none, false⟩,
  ⟨"أَيْ", [c 0 0, c 28 3], .none, false⟩,
  ⟨"حَيْثُ", [c 6 0, c 28 3, c 4 2], .none, false⟩,
  ⟨"عِنْدَ", [c 18 1, c 25 3, c 8 0], .jarr, false⟩,
  ⟨"فَوْقَ", [c 20 0, c 27 3, c 21 0], .jarr, false⟩,
  ⟨"تَحْتَ", [c 3 0, c 6 3, c 3 0], .jarr, false⟩,
  ⟨"أَمَامَ", [c 0 0, c 24 0, c 1 3, c 24 0], .jarr, false⟩,
  ⟨"خَلْفَ", [c 7 0, c 23 3, c 20 0], .jarr, false⟩,
  ⟨"هُنَا", [c 26 2, c 25 0, c 1 3], .none, false⟩,
  ⟨"هُنَالِكَ", [c 26 2, c 25 0, c 1 3, c 23 1, c 22 0], .none, false⟩,
  ⟨"بَيْنَمَا", [c 2 0, c 28 3, c 25 0, c 24 0, c 1 3], .none, false⟩,
  ⟨"نَعَمْ", [c 25 0, c 18 0, c 24 3], .none, false⟩,
  ⟨"أَجَلْ", [c 0 0, c 5 0, c 23 3], .none, false⟩,
  ⟨"بَلَى", [c 2 0, c 23 0, c 1 3], .none, false⟩,
  ⟨"كَلَّا", [c 22 0, c 23 3, c 23 0, c 1 3], .none, false⟩,
  ⟨"إِلَّا", [c 0 1, c 23 3, c 23 0, c 1 3], .none, false⟩,
  ⟨"غَيْرُ", [c 19 0, c 28 3, c 10 2], .jarr, false⟩,
  ⟨"لَكِنَّ", [c 23 0, c 22 1, c 25 3, c 25 0], .nasbIsm, false⟩,
  ⟨"أَمَّا", [c 0 0, c 24 3, c 24 0, c 1 3], .none, false⟩,
  ⟨"لَعَلَّ", [c 23 0, c 18 0, c 23 3, c 23 0], .nasbIsm, false⟩,
  ⟨"رُبَّمَا", [c 10 2, c 2 3, c 2 0, c 24 0, c 1 3], .none, false⟩,
  ⟨"ظَنَّ", [c 17 0, c 25 3, c 25 0], .none, false⟩,
  ⟨"حَسِبَ", [c 6 0, c 12 1, c 2 0], .none, false⟩,
  ⟨"لِ", [c 23 1], .jarr, true⟩,
  ⟨"إِذْ", [c 0 1, c 9 3], .none, false⟩,
  ⟨"إِذًا", [c 0 1, c 9 0, c 25 3], .none, false⟩,
  ⟨"كَيْ", [c 22 0, c 28 3], .nasb, false⟩,
  ⟨"لِكَيْ", [c 23 1, c 22 0, c 28 3], .nasb, false⟩,
  ⟨"لِئَلَّا", [c 23 1, c 0 0, c 23 3, c 23 0, c 1 3], .nasb, false⟩,
  ⟨"كَيْلَا", [c 22 0, c 28 3, c 23 0, c 1 3], .nasb, false⟩,
  ⟨"إِنَّ", [c 0 1, c 25 3, c 25 0], .nasbIsm, false⟩,
  ⟨"أَنَّ", [c 0 0, c 25 3, c 25 0], .nasbIsm, false⟩,
  ⟨"سَ", [c 12 0], .none, true⟩,
  ⟨"سَوْفَ", [c 12 0, c 27 3, c 20 0], .none, false⟩,
  ⟨"إِنْ", [c 0 1, c 25 3], .jazm, false⟩,
  ⟨"مَنْ", [c 24 0, c 25 3], .jazm, false⟩,
  ⟨"مَا", [c 24 0, c 1 3], .jazm, false⟩,
  ⟨"مَهْمَا", [c 24 0, c 26 3, c 24 0, c 1 3], .jazm, false⟩,
  ⟨"مَتَى", [c 24 0, c 3 0, c 1 3], .jazm, false⟩,
  ⟨"أَيْنَ", [c 0 0, c 28 3, c 25 0], .jazm, false⟩,
  ⟨"أَيْنَمَا", [c 0 0, c 28 3, c 25 0, c 24 0, c 1 3], .jazm, false⟩,
  ⟨"أَنَّى", [c 0 0, c 25 3, c 25 0, c 1 3], .jazm, false⟩,
  ⟨"حَيْثُمَا", [c 6 0, c 28 3, c 4 2, c 24 0, c 1 3], .jazm, false⟩,
  ⟨"كَيْفَمَا", [c 22 0, c 28 3, c 20 0, c 24 0, c 1 3], .jazm, false⟩,
  ⟨"أَيُّ", [c 0 0, c 28 3, c 28 2], .jazm, false⟩,
  ⟨"إِذَا", [c 0 1, c 9 0, c 1 3], .none, false⟩,
  ⟨"لَوْ", [c 23 0, c 27 3], .none, false⟩,
  ⟨"كُلَّمَا", [c 22 2, c 23 3, c 23 0, c 24 0, c 1 3], .none, false⟩,
  ⟨"لَوْلَا", [c 23 0, c 27 3, c 23 0, c 1 3], .none, false⟩,
  ⟨"إِمَّا", [c 0 1, c 24 3, c 24 0, c 1 3], .none, false⟩,
  ⟨"بِ", [c 2 1], .jarr, true⟩,
  ⟨"كَ", [c 22 0], .jarr, true⟩,
  ⟨"مِنْ", [c 24 1, c 25 3], .jarr, false⟩,
  ⟨"عَنْ", [c 18 0, c 25 3], .jarr, false⟩,
  ⟨"إِلَى", [c 0 1, c 23 0, c 1 3], .jarr, false⟩,
  ⟨"عَلَى", [c 18 0, c 23 0, c 1 3], .jarr, false⟩,
  -- سدادُ دَينٍ مسمًّى (2026-10-06): حروفُ حصر الأدوات التي كانت خارج الجدول
  ⟨"أَنْ", [c 0 0, c 25 3], .nasb, false⟩,
  ⟨"إِذَنْ", [c 0 1, c 9 0, c 25 3], .nasb, false⟩,
  ⟨"إِذْمَا", [c 0 1, c 9 3, c 24 0, c 1 3], .jazm, false⟩,
  ⟨"أَيَّانَ", [c 0 0, c 28 3, c 28 0, c 1 3, c 25 0], .jazm, false⟩,
  ⟨"حِينَ", [c 6 1, c 28 3, c 25 0], .none, false⟩,
  ⟨"لَوْمَا", [c 23 0, c 27 3, c 24 0, c 1 3], .none, false⟩,
  ⟨"كَأَنَّ", [c 22 0, c 0 0, c 25 3, c 25 0], .nasbIsm, false⟩,
  ⟨"لَيْتَ", [c 23 0, c 28 3, c 3 0], .nasbIsm, false⟩,
  ⟨"مُذْ", [c 24 2, c 9 3], .jarr, false⟩,
  ⟨"مُنْذُ", [c 24 2, c 25 3, c 9 2], .jarr, false⟩,
  ⟨"رُبَّ", [c 10 2, c 2 3, c 2 0], .jarr, false⟩,
  ⟨"خَلَا", [c 7 0, c 23 0, c 1 3], .jarr, false⟩,
  ⟨"عَدَا", [c 18 0, c 8 0, c 1 3], .jarr, false⟩,
  ⟨"حَاشَا", [c 6 0, c 1 3, c 13 0, c 1 3], .jarr, false⟩,
  ⟨"تَ", [c 3 0], .jarr, true⟩,
  ⟨"أَلَا", [c 0 0, c 23 0, c 1 3], .none, false⟩,
  ⟨"أَمَا", [c 0 0, c 24 0, c 1 3], .none, false⟩,
  ⟨"لَاتَ", [c 23 0, c 1 3, c 3 0], .none, false⟩,
  ⟨"هَلْ", [c 26 0, c 23 3], .none, false⟩,
  ⟨"فِي", [c 20 1, c 28 3], .jarr, false⟩
]

theorem particles_count : particles.length = 90 := by rfl

theorem particles_licensed : particles.all (fun p => licensed p.cells) = true := by decide

/-- كلُّ حرفٍ متّصلٍ خانةٌ واحدةٌ متحرّكة. -/
theorem proclitics_one_vowelled_cell :
    particles.all (fun p => !p.proclitic || (p.cells.length == 1 &&
      (p.cells.headD ⟨0, 0⟩).state.val != 3)) = true := by decide

end Slge.Rawabit
