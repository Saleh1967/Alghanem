import Slge.Wad

/-!
# المتباين: مادّتان لا تلتقيان — والأصلُ في الوضع التباين

* **المادّة** على الخانات: الجذرُ الذي يستخرجه قالبٌ قارئ (`key`)؛ وموادُّ الكلمة جذورُها بكلّ قالبٍ يقرؤها
  (`mawadd`). الحصرُ السباعيُّ باعتبار الدالّ والمدلول يُقرأ على الخانات بعدد الكلمات وعدد الموادّ:
  **المنفرد** كلمةٌ بمادّةٍ واحدة، **المشترك** كلمةٌ بمادّتين، **متّحدا المادّة** (ترادفُ الصورة) كلمتان
  مادّتُهما واحدة، **المتباينان** كلمتان لا مادّةَ بينهما (`tabayun`)؛ و**المتداخلان** كلمتان تشتركان في
  مادّةٍ وتنفرد إحداهما بأخرى — قسمٌ لا يذكره الحصرُ وتقرؤه الخانة (اِنْتِشَارٌ/نَشْرٌ: `rel_witnesses`)،
  فالسبعةُ ليست حاصرةً على الخانات — باسمه.
* **التباينُ متماثلٌ غيرُ انعكاسيّ**: `tabayun_symm` لكلّ كلمتين، و`shareMadda_self` (كلُّ ذي مادّةٍ يشارك
  نفسَه) فلا كلمةَ تباين نفسَها (`tabayun_irrefl`).
* **الأصلُ في الوضع التباين**: على القالب المعزول (الذي لا يلتقي بغيره — 77 من الـ121 `isolated_count`)،
  جذران مختلفان لا ألفَ فيهما يعطيان كلمتين متباينتين، وهما على قالبٍ واحد: التباينُ في المادّة لا
  يلغي الجنسَ الجامع (الصورة) — `tabayun_of_isolated` لكلّ قالبٍ معزول ولكلّ جذرين. وعلى غير
  المعزول (اِنْتِشَارٌ) يقع التداخل — باسمه.
* **الترادفُ التامُّ مستحيلٌ على الخانات**: الملءُ دالّة، فلا يُعطي القالبُ والجذرُ كلمتين (`fill_functional`
  — بديهيّ)، ولا يبقى من الترادف إلّا ترادفُ الصورة (مادّةٌ واحدةٌ بقالبين).
ما ليس في الخانة — باسمه: المنقولُ والحقيقةُ والمجاز (نقلٌ بالاشتهار، لا خانةَ له)، والتضادُّ (السوادُ والبياض
متباينان بالخانة كأيّ جذرين، والضدّيّةُ معنًى)، وفَعَالٌ (سَوَادٌ/بَيَاضٌ) ليست في المعجم المودَع. القياسُ على
MASAQ في بايثون: العلاقةُ بين كلّ كلمتين متجاورتين في الآية. الحصرُ المُرسَل: أنواعُه مكتوبةٌ باليد
(`SpeechRelation`، `Meaning`، `Divergent` ببانيَين) وبرهاناه `cases r <;> simp` على عدٍّ مكتوبٍ باليد —
لم يُدخَل منه شيء؛ ودخل معناه على الخانات.
-/

namespace Slge.Tabayun

open Slge.Categories (c)

/-! ## المادّة -/

abbrev Key := Option (Fin 29) × Option (Fin 29) × Option (Fin 29)

/-- مادّةُ الكلمة بقالبٍ: جذرُها المستخرَج. -/
def key (q : Nat) (w : List SCell) : Key :=
  (Wazn.rootOf (Sarf.templ q) w 0, Wazn.rootOf (Sarf.templ q) w 1, Wazn.rootOf (Sarf.templ q) w 2)

/-- موادُّ الكلمة: جذورُها بكلّ قالبٍ يقرؤها. -/
def mawadd (w : List SCell) : List Key := (Wad.senses w).map fun q => key q w

def shareMadda (a b : List SCell) : Bool := (mawadd a).any fun m => (mawadd b).contains m

/-- متباينان: كلمتان مختلفتان ذواتا مادّةٍ لا مادّةَ بينهما. -/
def tabayun (a b : List SCell) : Bool :=
  a != b && mawadd a != [] && mawadd b != [] && !shareMadda a b

theorem shareMadda_iff (a b : List SCell) :
    shareMadda a b = true ↔ ∃ m, m ∈ mawadd a ∧ m ∈ mawadd b := by
  simp [shareMadda, List.any_eq_true]

/-- التباينُ متماثل: «كلُّ واحدٍ مباينُ الآخر» — لكلّ كلمتين. -/
theorem shareMadda_symm (a b : List SCell) : shareMadda a b = shareMadda b a := by
  rw [Bool.eq_iff_iff, shareMadda_iff, shareMadda_iff]
  constructor
  · rintro ⟨m, h1, h2⟩; exact ⟨m, h2, h1⟩
  · rintro ⟨m, h1, h2⟩; exact ⟨m, h2, h1⟩

theorem tabayun_symm (a b : List SCell) : tabayun a b = tabayun b a := by
  unfold tabayun
  rw [shareMadda_symm]
  cases h1 : (a != b)
  · have hab : a = b := by simpa [bne_iff_ne] using h1
    subst hab; simp
  · have : (b != a) = true := by
      simp only [bne_iff_ne, ne_eq] at h1 ⊢; exact fun h => h1 h.symm
    simp [this, Bool.and_comm]

/-- كلُّ ذي مادّةٍ يشارك نفسَه. -/
theorem shareMadda_self (w : List SCell) (h : mawadd w ≠ []) : shareMadda w w = true := by
  rw [shareMadda_iff]
  cases hm : mawadd w with
  | nil => exact absurd hm h
  | cons m _ => exact ⟨m, by simp⟩

/-- لا كلمةَ تباين نفسَها. -/
theorem tabayun_irrefl (w : List SCell) : tabayun w w = false := by simp [tabayun]

/-! ## الأصلُ في الوضع التباين: على القالب المعزول -/

/-- القالبُ المعزول: لا يلتقي بقالبٍ غيرِ مطابقٍ له. -/
def isolated (k : Nat) : Bool :=
  (List.range 121).all fun q => !Wad.mayCollide (Sarf.templ k) (Sarf.templ q) || Sarf.templ q == Sarf.templ k

set_option maxRecDepth 100000 in
/-- 77 قالبًا معزولًا من الـ121؛ وغيرُ المعزول 44 هي أطرافُ أزواج الالتقاء المختلفة. -/
theorem isolated_count : ((List.range 121).filter isolated).length = 77 := by decide

theorem templ_wf : ∀ q, q < 121 → Wazn.WF (Sarf.templ q) := by decide

/-- على القالب المعزول، كلُّ قالبٍ يقرأ ملأَه (بجذرٍ لا ألفَ فيه) مطابقٌ له، فمادّتُه جذرُه وحدَه. -/
theorem mawadd_fill_isolated (k : Nat) (hk : k < 121) (hiso : isolated k = true) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) :
    ∀ m ∈ mawadd (Wazn.fill (Sarf.templ k) r), m = (some (r 0), some (r 1), some (r 2)) := by
  intro m hm
  unfold mawadd at hm
  rw [List.mem_map] at hm
  obtain ⟨q, hq, rfl⟩ := hm
  unfold Wad.senses at hq
  rw [List.mem_filter] at hq
  obtain ⟨hq121, hqr⟩ := hq
  have hq121' := List.mem_range.1 hq121
  unfold Maqam.onTemplateRoot at hqr
  simp only [Bool.and_eq_true] at hqr
  obtain ⟨hon, hna⟩ := hqr
  obtain ⟨r2, hr2⟩ := (Kulli.universal_in_particulars _ (templ_wf q hq121') _).1 hon
  have hr2na : ∀ i, (r2 i).val ≠ 1 := by
    intro i
    have h := List.all_eq_true.1 hna i (by
      match i with
      | 0 => simp | 1 => simp | 2 => simp)
    rw [← hr2, Wazn.rootOf_fill _ (templ_wf q hq121') r2 i] at h
    simpa [bne_iff_ne] using h
  have hmc := Wad.mayCollide_sound _ _ r r2 hr hr2na hr2.symm
  have hiso' := List.all_eq_true.1 hiso q hq121
  rw [hmc] at hiso'
  simp only [Bool.not_true, Bool.false_or, beq_iff_eq] at hiso'
  unfold key
  rw [hiso', Wazn.rootOf_fill _ (templ_wf k hk) r 0, Wazn.rootOf_fill _ (templ_wf k hk) r 1,
    Wazn.rootOf_fill _ (templ_wf k hk) r 2]

/-- الأصلُ في الوضع التباين: على القالب المعزول، جذران مختلفان لا ألفَ فيهما يعطيان كلمتين متباينتين
على قالبٍ واحد (التباينُ في المادّة لا يلغي الجنسَ الجامع) — لكلّ قالبٍ معزول ولكلّ جذرين. -/
theorem tabayun_of_isolated (k : Nat) (hk : k < 121) (hiso : isolated k = true) (r r' : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) (hr' : ∀ i, (r' i).val ≠ 1) (hne : r ≠ r') :
    tabayun (Wazn.fill (Sarf.templ k) r) (Wazn.fill (Sarf.templ k) r') = true ∧
    Sarf.onTemplate (Sarf.templ k) (Wazn.fill (Sarf.templ k) r) = true ∧
    Sarf.onTemplate (Sarf.templ k) (Wazn.fill (Sarf.templ k) r') = true := by
  have hwf := templ_wf k hk
  refine ⟨?_, Sarf.onTemplate_fill _ hwf r, Sarf.onTemplate_fill _ hwf r'⟩
  have hne' : Wazn.fill (Sarf.templ k) r ≠ Wazn.fill (Sarf.templ k) r' :=
    fun h => hne (Wad.wad_injective _ hwf r r' h)
  have hsense := Wad.sense_of_fill k hk hwf r hr
  have hsense' := Wad.sense_of_fill k hk hwf r' hr'
  have hm : mawadd (Wazn.fill (Sarf.templ k) r) ≠ [] := by
    intro h; unfold mawadd at h; rw [List.map_eq_nil_iff] at h; rw [h] at hsense; simp at hsense
  have hm' : mawadd (Wazn.fill (Sarf.templ k) r') ≠ [] := by
    intro h; unfold mawadd at h; rw [List.map_eq_nil_iff] at h; rw [h] at hsense'; simp at hsense'
  have hshare : shareMadda (Wazn.fill (Sarf.templ k) r) (Wazn.fill (Sarf.templ k) r') = false := by
    apply Bool.eq_false_iff.2
    intro h
    obtain ⟨m, h1, h2⟩ := (shareMadda_iff _ _).1 h
    have e1 := mawadd_fill_isolated k hk hiso r hr m h1
    have e2 := mawadd_fill_isolated k hk hiso r' hr' m h2
    rw [e1] at e2
    simp only [Prod.mk.injEq, Option.some.injEq] at e2
    apply hne
    funext i
    match i with
    | 0 => exact e2.1
    | 1 => exact e2.2.1
    | 2 => exact e2.2.2
  unfold tabayun
  simp [hne', hm, hm', hshare]

/-- الترادفُ التامُّ مستحيلٌ على الخانات: الملءُ دالّة — بديهيّ. -/
theorem fill_functional (t : Wazn.Template) (r : Wazn.Root) (w1 w2 : List SCell)
    (h1 : Wazn.fill t r = w1) (h2 : Wazn.fill t r = w2) : w1 = w2 := h1 ▸ h2

/-! ## القارئ: الحصرُ السباعيُّ على الخانات وقسمُه الثامن -/

inductive Rel where
  | munfarid | mushtarak | ittihad | mutabayin | mutadakhil | unread
  deriving DecidableEq, Repr

/-- موادُّ الكلمة بلا تكرار. -/
def mawaddSet (w : List SCell) : List Key := (mawadd w).eraseDups

/-- علاقةُ كلمتين بعد ردّ التنوين: كلمةٌ واحدة (منفردٌ بمادّة، مشتركٌ بمادّتين)، أو كلمتان (متّحدتا
المادّة، متباينتان، متداخلتان)، أو لا يُقرأ. -/
def rel (a b : List SCell) : Rel :=
  let a := Marifa.dropTanwin a
  let b := Marifa.dropTanwin b
  let ma := mawaddSet a
  let mb := mawaddSet b
  if ma.isEmpty || mb.isEmpty then .unread
  else if a == b then (if ma.length == 1 then .munfarid else .mushtarak)
  else if !shareMadda a b then .mutabayin
  else if (ma.all mb.contains) && (mb.all ma.contains) then .ittihad
  else .mutadakhil

def qatl : List SCell := [c 21 0, c 3 3, c 23 2, c 25 3]                      -- قَتْلٌ
def nashr : List SCell := [c 25 0, c 13 3, c 10 2, c 25 3]                    -- نَشْرٌ
def dirab : List SCell := [c 15 1, c 10 0, c 1 3, c 2 2, c 25 3]              -- ضِرَابٌ
def darbun : List SCell := Nawasikh.tanwin Talab.darb                         -- ضَرْبٌ

/-- ضَرْبٌ/قَتْلٌ متباينان على قالبٍ واحد؛ ضَرْبٌ/ضِرَابٌ متّحدا المادّة (ترادفُ صورة)؛ اِنْتِشَارٌ/نَشْرٌ
متداخلان (ن‑ش‑ر مشتركة، وت‑ش‑ر تنفرد بها الأولى) — القسمُ الثامن؛ كِتَابٌ منفردٌ بمادّته وإن اشترك وضعُه؛
اِنْتِشَارٌ مشترك؛ ولَا لا تُقرأ. والتباينُ متماثل. -/
theorem rel_witnesses :
    rel darbun qatl = .mutabayin ∧ rel qatl darbun = .mutabayin ∧ rel darbun dirab = .ittihad ∧
    rel Wad.intishar nashr = .mutadakhil ∧ rel Wad.kitab Wad.kitab = .munfarid ∧
    rel Wad.intishar Wad.intishar = .mushtarak ∧ rel Uslub.la darbun = .unread ∧
    Sarf.onTemplate (Sarf.templ 29) (Marifa.dropTanwin darbun) = true ∧
    Sarf.onTemplate (Sarf.templ 29) (Marifa.dropTanwin qatl) = true := by decide

/-- المتداخلُ ليس في الحصر السباعيّ: كلمتان بأكثر من مادّةٍ لا متباينتان ولا متّحدتا المادّة — فالتكثّرُ في
الطرفين لا يلزم منه التباين على الخانات. -/
theorem seven_not_exhaustive :
    rel Wad.intishar nashr ≠ .mutabayin ∧ rel Wad.intishar nashr ≠ .ittihad ∧
    Wad.intishar ≠ nashr ∧ (mawaddSet (Marifa.dropTanwin Wad.intishar) ++
      mawaddSet (Marifa.dropTanwin nashr)).eraseDups.length = 2 := by decide

end Slge.Tabayun
