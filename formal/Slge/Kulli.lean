import Slge.Talab

/-!
# الكليُّ والجزئيّ: القالبُ كليٌّ وجودُه في أفراده، والجزئيُّ من جدولٍ لا من قالب، والمصدرُ مجرّدٌ من الزمن

* **الكليُّ في الخارج وجودُه في أفراده** (د٤): القالبُ (الماهيةُ) لا يوجد في الخانات إلّا مملوءًا بجذر — ما على
  قالبٍ فهو `fill t r` لجذرٍ ما، وكلُّ `fill t r` على قالبه (`universal_in_particulars`: لكلّ قالبٍ حسنِ
  التكوين ولكلّ كلمة). المعجمُ المودَع (`Wazn.awzan`) قوالبُ لا أفراد.
* **الجزئيُّ من جدولٍ لا من قالب**: الضمائرُ وأسماءُ الإشارة والموصولُ ليست على قالبٍ من الـ121 إلّا أربعًا
  تشابه قالبًا بالخانة (نَحْنُ، أَيُّ، ذَلِكَ، ثَمَّتَ — `particulars_off_templates`)، والقارئُ يقدّم الجدولَ على
  القالب فيقرأها كلَّها جزئيًّا (`juzi_by_table`) — الجزئيُّ يُحفَظ لا يُشتَقّ.
* **الكليُّ العرضيُّ والماهويُّ لا يشتركان في قالب**: قوالبُ الوصف (المشتقّ: `Mansubat.derivedTemplates`)
  وقوالبُ المصدر (`Filiyya.masdarTemplates`) متباينةٌ (`aradi_hadath_disjoint`).
* **المصدرُ مجرّدٌ من الزمن** (د٨): لكلّ قالبِ مصدرٍ ولكلّ جذرٍ لا ألفَ فيه لا يُقرأ ماضيًا ولا مضارعًا ولا أمرًا
  (`masdar_no_sigha`؛ وفَعْلَةُ بشرط ألّا تكون فاؤها صدرَ مضارع)، فلا تدخله أدواتُ الإزاحة (`masdar_not_shifted`) — والفعلُ مهيّأٌ بالزمن لكلّ قالبٍ
  (`Jiha.sigha_of_fill`).
* القارئُ `kulli` يقرأ الجهةَ الوجوديّة من الخانة: جزئيٌّ (ضميرٌ/إشارةٌ/موصول)، كليٌّ عرضيٌّ (مشتقٌّ على قالب
  الوصف)، حدثٌ مجرّد (مصدر)، حدثٌ مهيّأ (فعل)، كليٌّ ماهويّ (اسمٌ على غير ذلك)؛ والعلمُ جزئيٌّ بالمعجم لا
  بالخانة — باسمه.
القياسُ على MASAQ في بايثون: وسومُ الأصناف (PRON/DEM_PRON/REL_PRON، NOUN_ACTIVE_PART/ADJ، GERUND،
IV/PV/CV، NOUN_CONCRETE/NOUN_ABSTRACT، NOUN_PROP) مرجعٌ محجوبٌ للقارئ. الحصرُ المُرسَل: أنواعُه مكتوبةٌ
باليد (`Genus`، `OntologicalStatus`) وبرهاناه `use t` وفحصُه `assert x in [True, False]` — لم يُدخَل منه شيء؛
ودخل معناه على الخانات.
-/

namespace Slge.Kulli

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## الكليُّ في أفراده -/

/-- ما على قالبٍ فهو القالبُ مملوءًا بجذر، وكلُّ ملءٍ على قالبه. -/
theorem universal_in_particulars (t : Wazn.Template) (ht : Wazn.WF t) (w : List SCell) :
    Sarf.onTemplate t w = true ↔ ∃ r : Wazn.Root, Wazn.fill t r = w := by
  constructor
  · intro h
    unfold Sarf.onTemplate at h
    split at h
    · exact ⟨_, beq_iff_eq.1 h⟩
    · exact absurd h Bool.false_ne_true
  · rintro ⟨r, rfl⟩
    exact Sarf.onTemplate_fill t ht r

/-- الجزئيّاتُ المجدوَلة (الضمائرُ والإشارةُ والموصول) ليست على قالبٍ من الـ121 — إلّا أربعًا تشابه قالبًا
بالخانة (نَحْنُ وأَيُّ على فَعْلٌ، ذَلِكَ على فَعِلَ، ثَمَّتَ على فَعَّلَ): الخانةُ لا تفصلها فيفصلها الجدول. -/
theorem particulars_off_templates :
    (((Categories.pronouns ++ Ishara.forms.map (·.2) ++ Marifa.mawsul.map (·.2)).filter fun w =>
      (List.range 121).any fun k => Sarf.onTemplate (Sarf.templ k) w).length = 4) := by
  decide

/-! ## القارئ -/

inductive Kind where
  | juzi | aradi | hadath | fil | jamid | unread
  deriving DecidableEq, Repr

/-- الجهةُ الوجوديّة من الخانة: جزئيٌّ مجدوَل، أو حدثٌ مهيّأ (فعلٌ بصيغته — قبل القوالب الاسميّة، فكَتَبَ يشابه
فَعَلًا مصدرًا بعد ردّ آخره، وأَكْتَبَ يشابه أَفْعَلَ التفضيل)، أو كليٌّ عرضيٌّ (مشتقّ)، أو حدثٌ مجرّد (مصدر)، أو
كليٌّ ماهويّ (اسمٌ مقروءُ الإعراب على غير ذلك)؛ وما سواه لا يُقرأ. -/
def kulli (w : List SCell) : Kind :=
  if Categories.pronouns.contains w || Jumla.mabniIsm w then .juzi
  else if (Jiha.sigha w).isSome || Uslub.presentAnyMood w then .fil
  else if Mansubat.derived (Marifa.dropTanwin w) then .aradi
  else if Filiyya.isMasdar w then .hadath
  else if Tawabi.caseClass w != .unread then .jamid
  else .unread

/-- القارئُ يقدّم الجدولَ على القالب: كلُّ مجدوَلٍ جزئيّ. -/
theorem juzi_by_table :
    ((Categories.pronouns ++ Ishara.forms.map (·.2) ++ Marifa.mawsul.map (·.2)).all fun w =>
      kulli w == .juzi) = true := by decide

/-- قوالبُ الوصف وقوالبُ المصدر متباينة: العرضيُّ والحدثُ لا يشتركان في قالب. -/
theorem aradi_hadath_disjoint :
    (Mansubat.derivedTemplates.all fun k => !Filiyya.masdarTemplates.contains k) = true := by decide

/-! ## المصدرُ مجرّدٌ من الزمن -/

def masdarTemplates : List Nat := Filiyya.masdarTemplates

theorem masdar_templates_wf : masdarTemplates.all (fun k => decide (Wazn.WF (Sarf.templ k))) = true := by
  decide

/-- حالاتُ قوالب المصدر غيرُ حالات قوالب الماضي والأمر كلِّها؛ وغيرُ حالات المضارع إلّا المصدرَ الميميّ
(مَفْعَل، مَفْعِل) الذي صدرُه ميمٌ لا صدرَ مضارعٍ فيه، وفَعْلَة التي صدرُها فاءُ الكلمة (نَصْرَةٌ تشابه
نَفْعَلُ بالخانة إن كانت فاؤها صدرَ مضارع — باسمها). -/
theorem masdar_states_disjoint :
    (masdarTemplates.all fun k => (Jiha.pastTemplates ++ Jiha.amrTemplates).all fun q =>
      (Sarf.templ k).map Wazn.stateOf != (Sarf.templ q).map Wazn.stateOf) = true ∧
    ((masdarTemplates.filter fun k => k != 56 && k != 57 && k != 63).all fun k =>
      Jiha.presentTemplates.all fun q =>
        (Sarf.templ k).map Wazn.stateOf != (Sarf.templ q).map Wazn.stateOf) = true ∧
    ([56, 57].all fun k => match (Sarf.templ k).head? with
      | some (.lit x) => x.carrier.val == 24 | _ => false) = true ∧
    (Sarf.templ 63).head? = some (.slot 0 0) := by
  refine ⟨by decide, by decide, by decide, by decide⟩

/-- المصدرُ لا يُقرأ ماضيًا ولا مضارعًا ولا أمرًا: لكلّ قالبِ مصدرٍ ولكلّ جذرٍ لا ألفَ فيه — وفَعْلَةُ بشرط ألّا
تكون فاؤها صدرَ مضارع (همزةً أو نونًا أو تاءً أو ياءً). -/
theorem masdar_no_sigha (k : Nat) (hk : k ∈ masdarTemplates) (r : Wazn.Root) (_hr : ∀ i, (r i).val ≠ 1)
    (h63 : k = 63 → (r 0).val ≠ 0 ∧ (r 0).val ≠ 25 ∧ (r 0).val ≠ 3 ∧ (r 0).val ≠ 28) :
    Jiha.sigha (Wazn.fill (Sarf.templ k) r) = none := by
  obtain ⟨d1, d2, d3, d4⟩ := masdar_states_disjoint
  have hs := Wazn.states_fill (Sarf.templ k) r
  have hnot : ∀ (qs : List Nat), (qs.all fun q =>
      (Sarf.templ k).map Wazn.stateOf != (Sarf.templ q).map Wazn.stateOf) = true →
      (qs.any fun q => Maqam.onTemplateRoot q (Wazn.fill (Sarf.templ k) r)) = false := by
    intro qs hqs
    apply Bool.eq_false_iff.2
    intro h
    obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 h
    have hon : Sarf.onTemplate (Sarf.templ q) (Wazn.fill (Sarf.templ k) r) = true := by
      simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
    have hs' := Jiha.states_of_onTemplate _ _ hon
    have hne := List.all_eq_true.1 hqs q hq
    simp only [bne_iff_ne, ne_eq] at hne
    exact hne (hs.symm.trans hs')
  have hall := List.all_eq_true.1 d1 k hk
  have hpast : (Jiha.pastTemplates.any fun q => Maqam.onTemplateRoot q (Wazn.fill (Sarf.templ k) r)) = false :=
    hnot _ (List.all_eq_true.2 fun q hq => List.all_eq_true.1 hall q (List.mem_append_left _ hq))
  have hamr : (Jiha.amrTemplates.any fun q => Maqam.onTemplateRoot q (Wazn.fill (Sarf.templ k) r)) = false :=
    hnot _ (List.all_eq_true.2 fun q hq => List.all_eq_true.1 hall q (List.mem_append_right _ hq))
  have hsp : Maqam.shakhsPresent (Wazn.fill (Sarf.templ k) r) = none := by
    by_cases h56 : k = 56 ∨ k = 57
    · -- المصدرُ الميميّ: صدرُه ميم
      have hh := List.all_eq_true.1 d3 k (by rcases h56 with rfl | rfl <;> decide)
      have hhead : (Wazn.fill (Sarf.templ k) r).head?.map (·.carrier.val) = some 24 := by
        cases ht : Sarf.templ k with
        | nil => rw [ht] at hh; simp at hh
        | cons x rest =>
          rw [ht] at hh
          cases x with
          | slot _ _ => simp at hh
          | lit y =>
            simp only [List.head?_cons, beq_iff_eq] at hh
            simp [Wazn.fill, Wazn.fillSym, hh]
      unfold Maqam.shakhsPresent
      split
      · rw [hhead]; rfl
      · rfl
    · by_cases h63' : k = 63
      · -- فَعْلَة: صدرُها فاءُ الكلمة، وليست صدرَ مضارعٍ بالشرط
        obtain ⟨n0, n25, n3, n28⟩ := h63 h63'
        subst h63'
        have hhead : (Wazn.fill (Sarf.templ 63) r).head?.map (·.carrier.val) = some (r 0).val := by
          cases ht : Sarf.templ 63 with
          | nil => rw [ht] at d4; simp at d4
          | cons x rest =>
            rw [ht] at d4
            simp only [List.head?_cons, Option.some.injEq] at d4
            subst d4
            simp [Wazn.fill, Wazn.fillSym]
        unfold Maqam.shakhsPresent
        split
        · rw [hhead]
          generalize hv : (r 0).val = v at n0 n25 n3 n28
          match v with
          | 0 => exact absurd rfl n0
          | 3 => exact absurd rfl n3
          | 25 => exact absurd rfl n25
          | 28 => exact absurd rfl n28
          | 1 | 2 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22
          | 23 | 24 | 26 | 27 | n + 29 => rfl
        · rfl
      · have hk' : k ∈ masdarTemplates.filter fun k => k != 56 && k != 57 && k != 63 := by
          rw [List.mem_filter]
          refine ⟨hk, ?_⟩
          simp only [Bool.and_eq_true, bne_iff_ne, ne_eq]
          exact ⟨⟨fun h => h56 (Or.inl h), fun h => h56 (Or.inr h)⟩, h63'⟩
        have hpres := List.all_eq_true.1 d2 k hk'
        have hnp : Maqam.isPresent (Wazn.fill (Sarf.templ k) r) = false := by
          apply Bool.eq_false_iff.2
          intro h
          obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 h
          have hon : Sarf.onTemplate (Sarf.templ q) (Maqam.withPrefix 28 (Wazn.fill (Sarf.templ k) r)) = true := by
            simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
          have hs' := Jiha.states_of_onTemplate _ _ hon
          rw [Jiha.withPrefix_states] at hs'
          have hne := List.all_eq_true.1 hpres q hq
          simp only [bne_iff_ne, ne_eq] at hne
          exact hne (hs.symm.trans hs')
        simp [Maqam.shakhsPresent, hnp]
  simp [Jiha.sigha, hpast, hamr, hsp]

/-- المصدرُ لا تدخله أدواتُ الإزاحة: لا سينَ ولا لَمْ ولا لَنْ ولا كَانَ على حدثٍ مجرّد. -/
theorem masdar_not_shifted (s : Jiha.Shift) (k : Nat) (hk : k ∈ masdarTemplates) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1)
    (h63 : k = 63 → (r 0).val ≠ 0 ∧ (r 0).val ≠ 25 ∧ (r 0).val ≠ 3 ∧ (r 0).val ≠ 28) :
    Jiha.shift s (Wazn.fill (Sarf.templ k) r) = none := by
  simp [Jiha.shift, masdar_no_sigha k hk r hr h63]

def katib : List SCell := [c 22 0, c 1 3, c 3 1, c 2 2, c 25 3]      -- كَاتِبٌ
def kitaba : List SCell := [c 22 1, c 3 0, c 1 3, c 2 0, c 3 2, c 25 3]  -- كِتَابَةٌ
def rajulun : List SCell := Naat.rajulun                               -- رَجُلٌ
def hadha : List SCell := [c 26 0, c 9 0, c 1 3]                       -- هَذَا

/-- هُوَ وهَذَا جزئيّان؛ كَاتِبٌ عرضيّ؛ كِتَابَةٌ وضَرْبٌ حدثٌ مجرّد؛ كَتَبَ ويَكْتُبُ واُكْتُبْ حدثٌ مهيّأ؛
رَجُلٌ والرَّجُلُ ماهويّ؛ ولَا لا تُقرأ. -/
theorem kulli_witnesses :
    kulli Maqam.huwa = .juzi ∧ kulli hadha = .juzi ∧ kulli katib = .aradi ∧ kulli kitaba = .hadath ∧
    kulli (Nawasikh.tanwin Talab.darb) = .hadath ∧ kulli Jiha.kataba = .fil ∧ kulli Jiha.yaktubu = .fil ∧
    kulli Jiha.uktub = .fil ∧ kulli rajulun = .jamid ∧ kulli Naat.alrajul = .jamid ∧
    kulli Uslub.la = .unread := by decide

end Slge.Kulli
