import Slge.Nawasikh

/-!
# الجزمُ والشرط: ثلاثُ علاماتٍ ثلاثُ عمليّات، والأداةُ تُعدّ ولا تُقرأ

الحصرُ يعدّ الأدواتِ (4 + 12 + 7) ويحصر العلاماتِ في ثلاث. على الخانات العلاماتُ عمليّاتٌ:
* **السكون** (`sukun`): سكونُ الآخر؛ مرخَّصٌ إذا لم يكن ما قبله ساكنًا (`sukun_licensed`)، و**غيرُ مرخَّصٍ
  إذا كان ما قبله مدًّا** (`hollow_forced`) — فحذفُ عين الأجوف (يَقُولُ ← يَقُلْ) ملزَمٌ لا اختيار،
  كما في `A116.Ilal`.
* **حذفُ حرف العلّة** (`dropWeak`): إسقاطُ المدّ الأخير؛ يحفظ الترخيص (`dropWeak_licensed`)، ويترك
  حركةَ الأصل في الآخر (`dropWeak_last`) — **فلا يُقرأ الجزمُ من الخانة بعده** بل بالمقارنة بالأصل.
* **حذفُ النون** (`Afal.form _ _ _ .jazm`): صورةُ الجزم هي صورةُ النصب بعينها (`Afal.nasb_eq_jazm`) —
  الأداةُ تفصل لا الخانة.

القارئُ `marker` يردّ الصورةَ إلى: سكونٌ، حذفُ نون، أو لا يقرؤه (المعتلّ). والأدواتُ **تُعدّ** في جداول
(`jazimOne`، `shartJazim`، `shartGhayr`) مرخَّصةً، ومنها ما خانتُه خانةُ غيره باسمه: لَا الناهيةُ = لَا
النافية، لَمَّا الجازمةُ = لَمَّا الحينيّة، ومَنْ ومَا وأَيّ وأَيْنَ ومَتَى وأَيَّانَ وأَنَّى = الاستفهام
(`shared_*`)؛ ولامُ الأمر حرفٌ متّصل (`amr_licensed`). والجزمُ بفعلين، والفاءُ الرابطة، والامتناعُ: تيار.
الشواهدُ بشهادات البوّابة (لَمْ يَلِدْ، لِيُنْفِقْ، لَا تُبْطِلُوا، يَعْمَلْ…)؛ القياسُ على MASAQ في بايثون.
-/

namespace Slge.Jazm

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## العمليّاتُ الثلاث -/

/-- السكونُ الظاهر. -/
def sukun (w : List SCell) : List SCell := setLast w 3

/-- حذفُ حرف العلّة: إسقاطُ الآخر. -/
def dropWeak (w : List SCell) : List SCell := Afal.initOf w

/-- الآخرُ مدٌّ من جنس ما قبله؟ (ألفٌ بعد فتح، واوٌ بعد ضمّ، ياءٌ بعد كسر) -/
def weakFinal (w : List SCell) : Bool :=
  match w.reverse with
  | m :: v :: _ => m.state.val == 3 && Khamsa.shortOfMadd m.carrier == some v.state
  | _ => false

theorem noAdj_append_two_sukun : ∀ (l : List SCell) (a b : SCell), a.isSukun = true →
    b.isSukun = true → noAdj (l ++ [a, b]) = false
  | [], a, b, ha, hb => by simp [noAdj, ha, hb]
  | [x], a, b, ha, hb => by simp [noAdj, ha, hb]
  | x :: y :: t, a, b, ha, hb => by
    simp only [List.cons_append, noAdj, Bool.and_eq_false_iff]
    exact Or.inr (noAdj_append_two_sukun (y :: t) a b ha hb)

/-- السكونُ بعد متحرّكٍ مرخَّص. -/
theorem sukun_licensed (i : List SCell) (k : Fin 29) (hi : licensed i = true) (hne : i ≠ [])
    (hlast : ∀ x, i.getLast? = some x → x.isSukun = false) : licensed (i ++ [⟨k, 3⟩]) = true :=
  Damair.attach_licensed i [⟨k, 3⟩] hi rfl hne
    (fun x y hx hy => by
      simp only [List.head?_cons, Option.some.injEq] at hy
      rw [← hy, hlast x hx]; rfl)

/-- السكونُ بعد مدٍّ غيرُ مرخَّص: حذفُ عين الأجوف ملزَم. -/
theorem hollow_forced (i : List SCell) (m k : SCell) (hm : m.isSukun = true) :
    licensed (i ++ [m, ⟨k.carrier, 3⟩]) = false := by
  cases i with
  | nil =>
    have h3 : m.state.val = 3 := by simpa [SCell.isSukun] using hm
    simp [licensed, noAdj, SCell.isSukun, h3]
  | cons x t =>
    simp only [List.cons_append, licensed, Bool.and_eq_false_iff]
    exact Or.inr (noAdj_append_two_sukun (x :: t) m ⟨k.carrier, 3⟩ hm rfl)

theorem dropWeak_licensed (w : List SCell) (h : licensed w = true) :
    licensed (dropWeak w) = true := Marifa.licensed_initOf w h

/-- بعد الحذف يبقى الآخرُ بحركة الأصل — لا سكونَ يُقرأ. -/
theorem dropWeak_last (i : List SCell) (x m : SCell) :
    Afal.lastOf (dropWeak (i ++ [x, m])) = some x := by
  unfold dropWeak
  have : i ++ [x, m] = (i ++ [x]) ++ [m] := by simp
  rw [this, Zaman.initOf_append_singleton, Zaman.lastOf_append_singleton]

/-- شواهدُ البوّابة: يَدْعُو/يَسْعَى/يَقْضِي ← يَدْعُ/يَسْعَ/يَقْضِ؛ ويَقُولُ ← يَقُلْ ملزَمًا. -/
def yadu : List SCell := [c 28 0, c 8 3, c 18 2, c 27 3]
def yasa : List SCell := [c 28 0, c 12 3, c 18 0, c 1 3]
def yaqdi : List SCell := [c 28 0, c 21 3, c 15 1, c 28 3]
def yaqulu : List SCell := [c 28 0, c 21 2, c 27 3, c 23 2]
def yaqul : List SCell := [c 28 0, c 21 2, c 23 3]

theorem weak_witnesses :
    (weakFinal yadu && weakFinal yasa && weakFinal yaqdi && !weakFinal yaqulu) = true ∧
    dropWeak yadu = [c 28 0, c 8 3, c 18 2] ∧ dropWeak yasa = [c 28 0, c 12 3, c 18 0] ∧
    dropWeak yaqdi = [c 28 0, c 21 3, c 15 1] := by decide

theorem yaqulu_sukun_unlicensed : licensed (sukun yaqulu) = false := by decide
theorem yaqul_licensed : licensed yaqul = true := by decide

/-- واوُ الجماعة المجزومة وواوُ المعتلّ المرفوع: خانةٌ واحدة (الألفُ الفارقةُ بقيّةُ رسم تفصلهما). -/
def yadu_jamaa : List SCell := [c 28 0, c 8 3, c 18 2, c 27 3]  -- يَدْعُوا
theorem waw_shared : yadu = yadu_jamaa := rfl

/-! ## القارئ -/

inductive Marker where
  | sukun | dropNun | unread
  deriving DecidableEq, Repr

/-- النونُ أوّلًا (الصورةُ الخمسيّةُ آخرُها مدٌّ ساكن)، ثمّ السكون؛ وما سواهما لا يُقرأ. -/
def marker (w : List SCell) : Marker :=
  if Afal.pronounOf w != none && Afal.moodOf w != .raf then .dropNun
  else match Afal.lastOf w with
    | some x => if x.state.val = 3 then .sukun else .unread
    | none => .unread

theorem marker_afal_jazm (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) :
    marker (Afal.form pr s p .jazm) = .dropNun := by
  unfold marker
  rw [Afal.pronounOf_form, ← Afal.nasb_eq_jazm, Afal.moodOf_nasb]; rfl

/-- الجزمُ والنصبُ في الخمسة صورةٌ واحدة: الأداةُ تفصل. -/
theorem afal_jazm_eq_nasb (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) :
    marker (Afal.form pr s p .nasb) = marker (Afal.form pr s p .jazm) := by
  rw [Afal.nasb_eq_jazm]

/-- شواهدُ القارئ بشهادات البوّابة. -/
def witnesses : List (String × List SCell) := [
  ("yalid", [c 28 0, c 23 1, c 8 3]), ("yamal", [c 28 0, c 18 3, c 24 0, c 23 3]),
  ("tubtilu", [c 3 2, c 2 3, c 16 1, c 23 2, c 27 3]), ("takunu", [c 3 0, c 22 2, c 27 3, c 25 2, c 27 3]),
  ("yadu", dropWeak yadu), ("yasa", dropWeak yasa), ("yaqul", yaqul), ("yujza", [c 28 2, c 5 3, c 11 0])
]

theorem marker_witnesses :
    marker [c 28 0, c 23 1, c 8 3] = .sukun ∧                       -- يَلِدْ
    marker [c 28 0, c 18 3, c 24 0, c 23 3] = .sukun ∧               -- يَعْمَلْ
    marker [c 3 2, c 2 3, c 16 1, c 23 2, c 27 3] = .dropNun ∧        -- تُبْطِلُوا
    marker [c 3 0, c 22 2, c 27 3, c 25 2, c 27 3] = .dropNun ∧       -- تَكُونُوا
    marker (dropWeak yadu) = .unread ∧ marker (dropWeak yasa) = .unread ∧
    marker [c 28 2, c 5 3, c 11 0] = .unread := by decide             -- يُجْزَ

/-! ## الأدواتُ تُعدّ -/

/-- تجزم فعلًا واحدًا (4): لَمْ، لَمَّا، لامُ الأمر (حرفٌ متّصلٌ مكسور)، لَا الناهية. -/
def jazimOne : List (String × List SCell) := [
  ("لَمْ", [c 23 0, c 24 3]), ("لَمَّا", [c 23 0, c 24 3, c 24 0, c 1 3]),
  ("لِ", [c 23 1]), ("لَا", [c 23 0, c 1 3])
]

/-- أدواتُ الشرط الجازمة (12): حرفان وعشرةُ أسماء. -/
def shartJazim : List (String × List SCell) := [
  ("إِنْ", [c 0 1, c 25 3]), ("إِذْمَا", [c 0 1, c 9 3, c 24 0, c 1 3]),
  ("مَنْ", Istifham.man), ("مَا", Istifham.ma), ("مَهْمَا", [c 24 0, c 26 3, c 24 0, c 1 3]),
  ("مَتَى", [c 24 0, c 3 0, c 1 3]), ("أَيَّانَ", [c 0 0, c 28 3, c 28 0, c 1 3, c 25 0]),
  ("أَيْنَ", [c 0 0, c 28 3, c 25 0]), ("أَنَّى", [c 0 0, c 25 3, c 25 0, c 1 3]),
  ("حَيْثُمَا", [c 6 0, c 28 3, c 4 2, c 24 0, c 1 3]),
  ("كَيْفَمَا", [c 22 0, c 28 3, c 20 0, c 24 0, c 1 3]), ("أَيُّ", Istifham.ayy 2)
]

/-- أدواتُ الشرط غيرُ الجازمة (7): أربعةُ ظروفٍ وثلاثةُ حروف. -/
def shartGhayr : List (String × List SCell) := [
  ("إِذَا", [c 0 1, c 9 0, c 1 3]), ("كُلَّمَا", [c 22 2, c 23 3, c 23 0, c 24 0, c 1 3]),
  ("لَمَّا", [c 23 0, c 24 3, c 24 0, c 1 3]), ("حِينَ", [c 6 1, c 28 3, c 25 0]),
  ("لَوْ", [c 23 0, c 27 3]), ("لَوْلَا", [c 23 0, c 27 3, c 23 0, c 1 3]),
  ("لَوْمَا", [c 23 0, c 27 3, c 24 0, c 1 3])
]

theorem tools_licensed :
    (jazimOne ++ shartJazim ++ shartGhayr).all (fun p => licensed p.2) = true := by decide
theorem counts : jazimOne.length = 4 ∧ shartJazim.length = 12 ∧ shartGhayr.length = 7 := by decide

/-- لامُ الأمر حرفٌ متّصلٌ مكسورٌ لا يُفسد ما بعده؛ شاهدُ البوّابة لِيُنْفِقْ. -/
def amr (w : List SCell) : List SCell := ⟨⟨23, by decide⟩, 1⟩ :: w

theorem amr_licensed (w : List SCell) (hw : licensed w = true) : licensed (amr w) = true :=
  Rawabit.proclitic_keeps_licence _ 1 (by decide) w hw

theorem yunfiq_witness :
    amr [c 28 2, c 25 3, c 20 1, c 21 3] = [c 23 1, c 28 2, c 25 3, c 20 1, c 21 3] ∧
    marker [c 28 2, c 25 3, c 20 1, c 21 3] = .sukun := by decide

/-! ## الخانةُ الواحدةُ باسمها -/

/-- لَا الناهيةُ ولَا النافية، ولَمَّا الجازمةُ والحينيّة: خانةٌ واحدة — الحكمُ من الفعل بعدها. -/
theorem shared_la_lamma :
    Rawabit.particles.any (fun p => p.name == "لَا" && p.cells == (jazimOne.getD 3 ("", [])).2) = true ∧
    (jazimOne.getD 1 ("", [])).2 = (shartGhayr.getD 2 ("", [])).2 := by decide

/-- سبعةٌ من أسماء الشرط خاناتُها خاناتُ الاستفهام. -/
theorem shared_istifham :
    ["مَنْ", "مَا", "مَتَى", "أَيَّانَ", "أَيْنَ", "أَنَّى", "أَيُّ"].all
      (fun n => (shartJazim.lookup n) == (Istifham.forms.lookup n)) = true := by decide

/-- أَيّ وحدَها معربة: ثلاثُ صورٍ بثلاث حركات. -/
theorem ayy_declines : Istifham.ayy 2 ≠ Istifham.ayy 0 ∧ Istifham.ayy 0 ≠ Istifham.ayy 1 := by decide

/-- جدولُ أدوات الربط: الجوازمُ كلُّها فيه بعملها (لَمْ لَمَّا وأدواتُ الشرط الجازمة الاثنتا عشرة)، وغيرُ
الجازمة السبعُ بلا عمل — سُدِّد الدَينُ: لا أداةَ خارج الجدول. -/
theorem rawabit_jazm :
    (["لَمْ", "لَمَّا"] ++ shartJazim.map (·.1)).all
      (fun n => Rawabit.particles.any (fun p => p.name == n && p.amal == .jazm)) = true ∧
    (shartGhayr.filter (·.1 != "لَمَّا")).all
      (fun q => Rawabit.particles.any (fun p => p.name == q.1 && p.amal == .none)) = true ∧
    Rawabit.particles.any (fun p => p.name == "لَمَّا" && p.amal == .jazm) = true ∧   -- الحينيّةُ خانةُ الجازمة
    ["لِ", "لَا"].all (fun n => Rawabit.particles.any (·.name == n)) = true := by decide

/-- الجزمُ بفعلين: حكمُ كلٍّ منهما حكمُ الواحد. -/
theorem two_verbs (pr₁ pr₂ : Afal.Prefix) (s₁ s₂ : Afal.Stem) (p₁ p₂ : Afal.Pronoun) :
    Rawabit.govern .jazm (Afal.form pr₁ s₁ p₁ .jazm) = true ∧
    Rawabit.govern .jazm (Afal.form pr₂ s₂ p₂ .jazm) = true :=
  ⟨Rawabit.govern_jazm_afal _ _ _, Rawabit.govern_jazm_afal _ _ _⟩

end Slge.Jazm
