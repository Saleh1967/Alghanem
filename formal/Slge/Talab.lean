import Slge.Uslub

/-!
# الطلب: صورُ الأمر الأربع من الخانة، والأمرُ ليس نهيًا على الخانة، والإلزامُ ليس في الخانة

* **صورُ الأمر الأربع** (د٤): الصيغةُ (قالبُ الأمر)، ولامُ الأمر على المضارع المجزوم (لِيَكْتُبْ؛ وبعد الواو
  والفاء تسكن: وَلْيَكْتُبْ)، والمصدرُ النائب (ضَرْبًا)، واسمُ الفعل من جدوله الحاصر (صَهْ، مَهْ، هَلُمَّ…) —
  يقرؤها `talab` من الخانات (`four_forms_witnesses`).
* **الصيغةُ للمخاطب واللامُ لكلّ شخص**: لامُ الأمر على المضارع تصل الغائبَ والمتكلّم لكلّ قالبِ مضارعٍ ولكلّ
  جذر (`lam_reaches_every_person`)، وتجزم: آخرُها ساكنٌ أبدًا (`lam_amr_jazm`) وتحفظ الترخيص
  (`lam_amr_licensed`).
* **الأمرُ بالشيء ليس نهيًا عن ضدّه على الخانة** (د٨): لَا قبل صيغة الأمر لا تقلبها نهيًا لكلّ قالبٍ ولكلّ جذر
  (`la_before_amr_stays_amr`)، والنهيُ لا يُقرأ إلّا بلَا قبل مضارع (`nahy_requires_la`)، فلا تحويلَ بين
  الأمر والنهي إلّا بعمليّتين: إدخالُ لَا وتغييرُ القالب (`amr_never_reads_nahy`). الضدُّ معنًى — معلَن.
* **الإلزامُ ليس في الخانة**: صيغةُ الأمر من جذرٍ واحدة لا تحمل وجوبًا ولا ندبًا ولا إباحة — فالجزمُ والإلزامُ من
  القرائن، لا من اللفظ المجرّد: معلَن لا مبرهَن (بديهيّةٌ لا تُسمّى برهانًا).
القياسُ على MASAQ في بايثون: فعلُ الأمر، واسمُ فعل الأمر، ولامُ الأمر (71 موضعًا: علامةُ الجزم). الحصرُ
المُرسَل في هذه الرسالة عمومٌ وخصوصٌ بأنواعٍ مكتوبةٍ باليد وإجهادٌ يقارن الدالّةَ بنفسها — لم يُدخَل منه شيء؛
والمطلوبُ (الطلب) دخل على الخانات.
-/

namespace Slge.Talab

open Slge.Categories (c)
open Slge.Zuruf (setLast)

inductive Sura where
  | sigha | lam | masdar | ismFil
  deriving DecidableEq, Repr

/-- أسماءُ فعل الأمر: جدولٌ حاصرٌ مبنيّ. -/
def ismFil : List (String × List SCell) := [
  ("صَهْ", [c 14 0, c 26 3]), ("مَهْ", [c 24 0, c 26 3]),
  ("هَلُمَّ", [c 26 0, c 23 2, c 24 3, c 24 0]), ("حَيَّ", [c 6 0, c 28 3, c 28 0]),
  ("آمِينَ", [c 0 0, c 1 3, c 24 1, c 28 3, c 25 0]), ("إِيهِ", [c 0 1, c 28 3, c 26 1]),
  ("هَيَّا", [c 26 0, c 28 3, c 28 0, c 1 3]), ("هَاتِ", [c 26 0, c 1 3, c 3 1])
]

theorem ismFil_licensed : ismFil.all (fun p => licensed p.2) = true := by decide
theorem ismFil_count : ismFil.length = 8 := by decide

/-- لامُ الأمر على المضارع المجزوم. -/
def lamAmr (v : List SCell) : List SCell := Jazm.amr (Jazm.sukun v)
/-- وبعد الواو والفاء تسكن اللام: وَلْيَكْتُبْ. -/
def lamAmrAfterWaw (v : List SCell) : List SCell := c 23 3 :: Jazm.sukun v
/-- المصدرُ النائبُ عن فعل الأمر: منصوبٌ منوَّن. -/
def masdarAmr (w : List SCell) : List SCell := Nawasikh.tanwin (Nawasikh.nasb w)

def waw : List SCell := [c 27 0]
def fa : List SCell := [c 20 0]

/-- صورةُ الطلب من الخانة: صيغةٌ، أو لامٌ (مكسورةً، أو ساكنةً بعد الواو والفاء) على مضارعٍ آخرُه ساكن، أو
اسمُ فعل، أو مصدرٌ منصوبٌ منوَّنٌ في الصدر (بلا فعلٍ قبله — وإلّا فمفعولٌ مطلق). -/
def talab (prev w : List SCell) : Option Sura :=
  if Jiha.sigha w == some .amr then some .sigha
  else if (w.take 1 == [c 23 1] || (w.take 1 == [c 23 3] && (prev == waw || prev == fa))) &&
      Uslub.presentAnyMood (w.drop 1) && (w.getLast?.map (·.state.val) == some 3) then some .lam
  else if ismFil.any (·.2 == w) then some .ismFil
  else if prev == [] && Filiyya.isMasdar w && Tawabi.caseClass w == .nasb && Nida.hasTanwin w then
    some .masdar
  else none

def darb : List SCell := [c 15 0, c 10 3, c 2 2]                  -- ضَرْبُ
def sah : List SCell := [c 14 0, c 26 3]                           -- صَهْ

/-- اُكْتُبْ صيغة؛ لِيَكْتُبْ ووَلْيَكْتُبْ لام؛ ضَرْبًا في الصدر مصدر؛ صَهْ اسمُ فعل؛ يَكْتُبُ وكَتَبَ لا طلب؛ ولامٌ
ساكنةٌ بلا واوٍ قبلها لا تُقرأ. -/
theorem four_forms_witnesses :
    talab [] Jiha.uktub = some .sigha ∧ talab [] (lamAmr Jiha.yaktubu) = some .lam ∧
    talab waw (lamAmrAfterWaw Jiha.yaktubu) = some .lam ∧ talab fa (lamAmrAfterWaw Jiha.yaktubu) = some .lam ∧
    talab [] (masdarAmr darb) = some .masdar ∧ talab [] sah = some .ismFil ∧
    talab [] Jiha.yaktubu = none ∧ talab [] Jiha.kataba = none ∧
    talab [] (lamAmrAfterWaw Jiha.yaktubu) = none ∧ talab Jiha.kataba (masdarAmr darb) = none := by
  decide

/-! ## اللامُ تصل كلَّ شخصٍ وتجزم -/

/-- لامُ الأمر على المضارع بصدوره: الغائبُ والمتكلّمُ (ونون المتكلّمين) لكلّ قالبٍ ولكلّ جذرٍ لا ألفَ فيه. -/
theorem lam_reaches_every_person (k : Nat) (hk : k ∈ Jiha.presentTemplates) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) :
    Maqam.shakhsPresent (Maqam.withPrefix 28 (Wazn.fill (Sarf.templ k) r)) = some .ghaib ∧
    Maqam.shakhsPresent (Maqam.withPrefix 0 (Wazn.fill (Sarf.templ k) r)) = some .mutakallim ∧
    Maqam.shakhsPresent (Maqam.withPrefix 25 (Wazn.fill (Sarf.templ k) r)) = some .mutakallim ∧
    (∀ p ∈ [(0 : Fin 29), 25, 3, 28], talab [] (lamAmr (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r))) =
      some .lam) := by
  have hper := Maqam.present_prefix_reads_person k hk r hr
  refine ⟨hper.2.2.2, hper.1, hper.2.1, ?_⟩
  intro p hp
  have hs := (Jiha.sigha_of_fill r hr).2.2 k hk p hp
  have hlast := Uslub.present_fill_last k hk r p
  have hnp := Uslub.sukun_present_not_past k hk r p
  generalize hvv : Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r) = v at hs hlast hnp ⊢
  have hid : setLast v 2 = v := Uslub.setLast_id v 2 (fun x hx => by rw [hlast] at hx; cases hx; rfl)
  have hne : v ≠ [] := by intro h; rw [h] at hlast; simp at hlast
  have hpm : Uslub.presentAnyMood (Jazm.sukun v) = true := by
    simp [Uslub.presentAnyMood, Jazm.sukun, Shibh.setLast_setLast, hid, hs]
  have hl : (Jazm.sukun v).getLast?.map (·.state.val) = some 3 := by
    obtain ⟨i, kk, hi⟩ := Nawasikh.setLast_eq_append v 3 hne
    unfold Jazm.sukun; rw [hi, List.getLast?_concat]; rfl
  have hnotamr : (Jiha.sigha (lamAmr v) == some .amr) = false := by
    -- لِيَفْعَلْ ليس على قالبِ أمرٍ ولا ماضٍ: صدرُه لامٌ مكسورةٌ وطولُه فوق قوالب الأمر الثلاثيّ
    apply Bool.eq_false_iff.2
    intro h
    have hsa : Jiha.sigha (lamAmr v) = some .amr := by simpa using h
    unfold Jiha.sigha at hsa
    split at hsa
    · simp at hsa
    · split at hsa
      · rename_i _ hamr
        obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 hamr
        have hon : Sarf.onTemplate (Sarf.templ q) (lamAmr v) = true := by
          simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
        have hst := Jiha.states_of_onTemplate _ _ hon
        have hv : v.map SCell.state = (Sarf.templ k).map Wazn.stateOf := by
          rw [← hvv, Jiha.withPrefix_states, Wazn.states_fill]
        have hlam : (lamAmr v).map SCell.state = 1 :: Uslub.setLastSt ((Sarf.templ k).map Wazn.stateOf) 3 := by
          unfold lamAmr Jazm.amr Jazm.sukun
          simp only [List.map_cons]
          rw [Uslub.map_state_setLast, hv]
        rw [hlam] at hst
        have := List.all_eq_true.1 (List.all_eq_true.1 (by decide : Jiha.presentTemplates.all fun k =>
          Jiha.amrTemplates.all fun q =>
            (1 :: Uslub.setLastSt ((Sarf.templ k).map Wazn.stateOf) 3) != (Sarf.templ q).map Wazn.stateOf) k hk) q hq
        simp only [bne_iff_ne, ne_eq] at this
        exact this hst
      · simp at hsa
  have hl1 : (lamAmr v).take 1 == [c 23 1] := by rfl
  have hdrop : (lamAmr v).drop 1 = Jazm.sukun v := rfl
  have hl2 : (lamAmr v).getLast?.map (·.state.val) = some 3 := by
    unfold lamAmr Jazm.amr
    obtain ⟨i, kk, hi⟩ := Nawasikh.setLast_eq_append v 3 hne
    unfold Jazm.sukun; rw [hi]
    show (((⟨⟨23, by decide⟩, 1⟩ : SCell) :: i) ++ [(⟨kk, 3⟩ : SCell)]).getLast?.map (·.state.val) = some 3
    rw [List.getLast?_concat]; rfl
  simp [talab, hnotamr, hl1, hdrop, hpm, hl2]

/-- لامُ الأمر تجزم: آخرُ الفعل ساكنٌ أبدًا لكلّ مضارع. -/
theorem lam_amr_jazm (v : List SCell) (hne : v ≠ []) :
    (lamAmr v).getLast?.map (·.state.val) = some 3 ∧ (lamAmrAfterWaw v).getLast?.map (·.state.val) = some 3 := by
  obtain ⟨i, kk, hi⟩ := Nawasikh.setLast_eq_append v 3 hne
  constructor
  · unfold lamAmr Jazm.amr Jazm.sukun; rw [hi]
    show (((⟨⟨23, by decide⟩, 1⟩ : SCell) :: i) ++ [(⟨kk, 3⟩ : SCell)]).getLast?.map (·.state.val) = some 3
    rw [List.getLast?_concat]; rfl
  · unfold lamAmrAfterWaw Jazm.sukun; rw [hi]
    show ((c 23 3 :: i) ++ [(⟨kk, 3⟩ : SCell)]).getLast?.map (·.state.val) = some 3
    rw [List.getLast?_concat]; rfl

/-- لامُ الأمر تحفظ الترخيص: المضارعُ المرخَّصُ ما قبل آخره متحرّكٌ يُجزَم فيُرخَّص وتدخله اللام. -/
theorem lam_amr_licensed (v : List SCell) (hne : v ≠ [])
    (hpen : ∀ x, (Afal.initOf v).getLast? = some x → x.isSukun = false) (hi : licensed (Afal.initOf v) = true)
    (hine : Afal.initOf v ≠ []) :
    licensed (lamAmr v) = true := by
  unfold lamAmr
  apply Jazm.amr_licensed
  obtain ⟨i, kk, hik⟩ := Nawasikh.setLast_eq_append v 3 hne
  have hii : i = Afal.initOf v := by
    have := congrArg Afal.initOf hik
    rw [Filiyya.initOf_setLast, Zaman.initOf_append_singleton] at this
    exact this.symm
  unfold Jazm.sukun; rw [hik, hii]
  exact Jazm.sukun_licensed _ kk hi hine hpen

/-! ## الأمرُ ليس نهيًا على الخانة -/

/-- لَا قبل صيغة الأمر لا تقلبها نهيًا: لكلّ قالبِ أمرٍ ولكلّ جذرٍ لا ألفَ فيه. -/
theorem la_before_amr_stays_amr (k : Nat) (hk : k ∈ Jiha.amrTemplates) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) (next : Option (List SCell)) :
    Uslub.uslub Uslub.la (Wazn.fill (Sarf.templ k) r) next = .amr :=
  (Uslub.amr_is_insha k hk r hr Uslub.la next).1

/-- النهيُ لا يُقرأ إلّا بلَا قبل مضارع. -/
theorem nahy_requires_la (prev w : List SCell) (next : Option (List SCell))
    (h : Uslub.uslub prev w next = .nahy) : prev = Uslub.la ∧ Uslub.presentAnyMood w = true := by
  refine ⟨?_, Uslub.nahy_only_present prev w next h⟩
  unfold Uslub.uslub at h
  split at h
  · exact absurd h (by decide)
  · split at h
    · rename_i hc
      simp only [Bool.and_eq_true, beq_iff_eq] at hc
      exact hc.1
    · exfalso
      repeat' split at h
      all_goals first | exact absurd h (by decide) | (simp at h)

/-- صيغةُ الأمر لا تُقرأ نهيًا مهما كان ما قبلها وما بعدها: التحويلُ عمليّتان (لَا وتغييرُ القالب). -/
theorem amr_never_reads_nahy (k : Nat) (hk : k ∈ Jiha.amrTemplates) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) (prev : List SCell) (next : Option (List SCell)) :
    Uslub.uslub prev (Wazn.fill (Sarf.templ k) r) next ≠ .nahy := by
  rw [(Uslub.amr_is_insha k hk r hr prev next).1]; decide

/-! الإلزامُ (وجوبٌ/ندبٌ/إباحة) ليس في الخانة: صيغةُ الأمر من الجذر الواحد قائمةُ خاناتٍ واحدة لكلّ حكم، فلا
دالّةَ من الخانة تفصل الأحكام — الجزمُ والإلزامُ من القرائن (معلَن؛ لا برهانَ على بديهيّة). -/

end Slge.Talab
