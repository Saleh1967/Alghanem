import Slge.Maqam

/-!
# الجهةُ والزمن: الصيغةُ من حالات الخانات لكلّ جذر، والأمرُ للمخاطب، وأدواتُ الإزاحة لا تدخل إلّا على المضارع

* **الصيغةُ من الخانة** (د٤): الماضي والمضارع والأمر ثلاثةُ أصنافٍ من القوالب تفصلها **الحالاتُ وحدَها** —
  ما على قالبٍ فحالاتُه حالاتُ قالبه (`states_of_onTemplate`)، وأصنافُ الصيغ الثلاثة متباينةُ الحالات قالبًا
  قالبًا (`sigha_states_disjoint`، على 13 + 13 + 11 قالبًا بـ`decide`)؛ فقارئُ الصيغة `sigha` يقرأ كلَّ ماضٍ
  ماضيًا وكلَّ أمرٍ أمرًا وكلَّ مضارعٍ بصدوره الأربعة مضارعًا **لكلّ جذرٍ لا ألفَ فيه** (`sigha_of_fill`،
  عامٌّ لا شاهد) — فلا يُقرأ ماضٍ مضارعًا ولا أمرٌ ماضيًا: الصيغةُ دالّةٌ في الحالات.
* **الأمرُ للمخاطب وحده** (د٨): صيغةُ الأمر مخاطبٌ أبدًا عند قارئ المقام (`amr_is_mukhatab`: لكلّ قالبِ أمرٍ
  ولكلّ جذرٍ لا ألفَ فيه ولا لاحقةَ له)، ولا صيغةَ أمرٍ للمتكلّم أو الغائب في القوالب — أمرُهما باللام
  (`Jazm.amr`: لِيَكْتُبْ) على المضارع لا على قالب الأمر (`ghaib_amr_by_lam`).
* **أدواتُ الإزاحة** لا تدخل إلّا على المضارع: السينُ وسَوْفَ (مستقبل)، ولَمْ (قلبُ المعنى ماضيًا بالجزم)،
  ولَنْ (نفيُ المستقبل بالنصب)، وكَانَ (ماضٍ مستمرّ) — كلُّها عمليّاتٌ تشترط `sigha v = .mudari`
  (`shift_only_present`)، وتحفظ الترخيص (`sa_licensed`)، وتُردّ بعينها (`sa_restores`، `lam_restores`).
  الماضي لا يُستقبَل بأداة (`past_not_shifted`) — هذا ما بقي على الخانة من «الماضي لا يُصاغ للمستقبل».
* القارئُ `jiha` يقرأ الجهةَ من الكلمة وما قبلها: ماضٍ، مضارعٌ (حاضر/مستقبل بلا قرينة)، مستقبلٌ بالسين
  وسَوْفَ، ماضٍ منفيٌّ بلَمْ، مستقبلٌ منفيٌّ بلَنْ، ماضٍ مستمرٌّ بكَانَ، أمر. ونقاطُ رايشنباخ (E، S، R) معنًى
  لا خانة — معلَن.
القياسُ على MASAQ في بايثون: وسمُ الصيغة (PV/IV/CV) مرجعٌ محجوبٌ لقارئ الصيغة، ووسمُ السين (FUT_PART)
لقانون «لا تدخل إلّا على المضارع». الحصرُ المُرسَل: أنواعُ الزمن والشخص مكتوبةٌ باليد لا على خانة، وفحصُ
إجهاده يقارن الدالّةَ بنفسها — لم يُدخَل منه شيء؛ ودخل معناه على الخانات.
-/

namespace Slge.Jiha

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## الصيغةُ من الحالات -/

inductive Sigha where
  | madi | mudari | amr
  deriving DecidableEq, Repr

def pastTemplates : List Nat := Maqam.pastTemplates
def presentTemplates : List Nat := Maqam.presentTemplates
def amrTemplates : List Nat := Filiyya.amrTemplates

/-- ما على قالبٍ فحالاتُه حالاتُ قالبه. -/
theorem states_of_onTemplate (t : Wazn.Template) (w : List SCell) (h : Sarf.onTemplate t w = true) :
    w.map SCell.state = t.map Wazn.stateOf := by
  unfold Sarf.onTemplate at h
  split at h
  · have : w = Wazn.fill t _ := (beq_iff_eq.1 h).symm
    rw [this, Wazn.states_fill]
  · exact absurd h Bool.false_ne_true

/-- أصنافُ الصيغ الثلاثة متباينةُ الحالات قالبًا قالبًا. -/
theorem sigha_states_disjoint :
    (pastTemplates.all fun p => (presentTemplates ++ amrTemplates).all fun q =>
      (Sarf.templ p).map Wazn.stateOf != (Sarf.templ q).map Wazn.stateOf) = true ∧
    (presentTemplates.all fun p => amrTemplates.all fun q =>
      (Sarf.templ p).map Wazn.stateOf != (Sarf.templ q).map Wazn.stateOf) = true := by
  refine ⟨?_, ?_⟩ <;> decide

theorem withPrefix_states (p : Fin 29) (v : List SCell) :
    (Maqam.withPrefix p v).map SCell.state = v.map SCell.state := by
  cases v <;> simp [Maqam.withPrefix]

theorem past_templates_wf : pastTemplates.all (fun k => decide (Wazn.WF (Sarf.templ k))) = true := by decide
theorem amr_templates_wf : amrTemplates.all (fun k => decide (Wazn.WF (Sarf.templ k))) = true := by decide

/-- قارئُ الصيغة: ماضٍ على قالبه، أو أمرٌ على قالبه، أو مضارعٌ بصدرٍ من الأربعة على قالبه بعد ردّ الصدر. -/
def sigha (v : List SCell) : Option Sigha :=
  if pastTemplates.any (fun k => Maqam.onTemplateRoot k v) then some .madi
  else if amrTemplates.any (fun k => Maqam.onTemplateRoot k v) then some .amr
  else if Maqam.isPresent v && (Maqam.shakhsPresent v).isSome then some .mudari
  else none

/-- على قالبٍ من صنفٍ ⇒ ليس على قالبٍ من صنفٍ آخر (بالحالات). -/
theorem not_on_other_class (ks qs : List Nat)
    (hd : (ks.all fun p => qs.all fun q =>
      (Sarf.templ p).map Wazn.stateOf != (Sarf.templ q).map Wazn.stateOf) = true)
    (w : List SCell) (k : Nat) (hk : k ∈ ks) (hw : w.map SCell.state = (Sarf.templ k).map Wazn.stateOf) :
    (qs.any fun q => Maqam.onTemplateRoot q w) = false := by
  apply Bool.eq_false_iff.2
  intro h
  obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 h
  have hon : Sarf.onTemplate (Sarf.templ q) w = true := by
    simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
  have hs := states_of_onTemplate _ _ hon
  have hne := List.all_eq_true.1 (List.all_eq_true.1 hd k hk) q hq
  simp only [bne_iff_ne, ne_eq] at hne
  exact hne (hw.symm.trans hs)

theorem onTemplateRoot_fill (k : Nat) (hwf : Wazn.WF (Sarf.templ k)) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) : Maqam.onTemplateRoot k (Wazn.fill (Sarf.templ k) r) = true := by
  simp only [Maqam.onTemplateRoot, Sarf.onTemplate_fill _ hwf r, Bool.true_and]
  refine List.all_eq_true.2 fun i _ => ?_
  rw [Wazn.rootOf_fill (Sarf.templ k) hwf r i]
  simpa using hr i

theorem isPresent_prefix (k : Nat) (hk : k ∈ presentTemplates) (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1)
    (q : Fin 29) : Maqam.isPresent (Maqam.withPrefix q (Wazn.fill (Sarf.templ k) r)) = true := by
  have hwf : Wazn.WF (Sarf.templ k) :=
    of_decide_eq_true (List.all_eq_true.1 Maqam.present_templates_wf k hk)
  unfold Maqam.isPresent
  refine List.any_eq_true.2 ⟨k, hk, ?_⟩
  rw [(Maqam.withPrefix_fill k hk r q).1]
  exact onTemplateRoot_fill k hwf r hr

/-- الصيغةُ تُقرأ لكلّ قالبٍ ولكلّ جذرٍ لا ألفَ فيه: الماضي ماضيًا، والأمرُ أمرًا، والمضارعُ بصدوره مضارعًا. -/
theorem sigha_of_fill (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1) :
    (∀ k ∈ pastTemplates, sigha (Wazn.fill (Sarf.templ k) r) = some .madi) ∧
    (∀ k ∈ amrTemplates, sigha (Wazn.fill (Sarf.templ k) r) = some .amr) ∧
    (∀ k ∈ presentTemplates, ∀ p ∈ [(0 : Fin 29), 25, 3, 28],
      sigha (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)) = some .mudari) := by
  obtain ⟨d1, d2⟩ := sigha_states_disjoint
  refine ⟨?_, ?_, ?_⟩
  · intro k hk
    have hwf : Wazn.WF (Sarf.templ k) := of_decide_eq_true (List.all_eq_true.1 past_templates_wf k hk)
    have h1 : (pastTemplates.any fun q => Maqam.onTemplateRoot q (Wazn.fill (Sarf.templ k) r)) = true :=
      List.any_eq_true.2 ⟨k, hk, onTemplateRoot_fill k hwf r hr⟩
    simp [sigha, h1]
  · intro k hk
    have hwf : Wazn.WF (Sarf.templ k) := of_decide_eq_true (List.all_eq_true.1 amr_templates_wf k hk)
    have hs := Wazn.states_fill (Sarf.templ k) r
    have h0 : (pastTemplates.any fun q => Maqam.onTemplateRoot q (Wazn.fill (Sarf.templ k) r)) = false := by
      apply Bool.eq_false_iff.2
      intro h
      obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 h
      have hon : Sarf.onTemplate (Sarf.templ q) (Wazn.fill (Sarf.templ k) r) = true := by
        simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
      have hs' := states_of_onTemplate _ _ hon
      have hne := List.all_eq_true.1 (List.all_eq_true.1 d1 q hq) k (List.mem_append_right _ hk)
      simp only [bne_iff_ne, ne_eq] at hne
      exact hne (hs'.symm.trans hs)
    have h1 : (amrTemplates.any fun q => Maqam.onTemplateRoot q (Wazn.fill (Sarf.templ k) r)) = true :=
      List.any_eq_true.2 ⟨k, hk, onTemplateRoot_fill k hwf r hr⟩
    simp [sigha, h0, h1]
  · intro k hk p hp
    have hs : (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)).map SCell.state =
        (Sarf.templ k).map Wazn.stateOf := by rw [withPrefix_states, Wazn.states_fill]
    have h0 : (pastTemplates.any fun q => Maqam.onTemplateRoot q
        (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r))) = false := by
      apply Bool.eq_false_iff.2
      intro h
      obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 h
      have hon : Sarf.onTemplate (Sarf.templ q) (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)) = true := by
        simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
      have hs' := states_of_onTemplate _ _ hon
      have hne := List.all_eq_true.1 (List.all_eq_true.1 d1 q hq) k (List.mem_append_left _ hk)
      simp only [bne_iff_ne, ne_eq] at hne
      exact hne (hs'.symm.trans hs)
    have h1 : (amrTemplates.any fun q => Maqam.onTemplateRoot q
        (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r))) = false :=
      not_on_other_class presentTemplates amrTemplates d2 _ k hk hs
    have hper := Maqam.present_prefix_reads_person k hk r hr
    have hpres : ∀ q ∈ [(0 : Fin 29), 25, 3, 28],
        Maqam.isPresent (Maqam.withPrefix q (Wazn.fill (Sarf.templ k) r)) = true ∧
        (Maqam.shakhsPresent (Maqam.withPrefix q (Wazn.fill (Sarf.templ k) r))).isSome = true := by
      intro q hq
      refine ⟨isPresent_prefix k hk r hr q, ?_⟩
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hq
      rcases hq with rfl | rfl | rfl | rfl
      · rw [hper.1]; rfl
      · rw [hper.2.1]; rfl
      · rw [hper.2.2.1]; rfl
      · rw [hper.2.2.2]; rfl
    obtain ⟨e1, e2⟩ := hpres p hp
    simp [sigha, h0, h1, e1, e2]

/-! ## الأمرُ للمخاطب -/

/-- قالبُ الأمر آخرُه لامُ الكلمة ساكنةً: صورتُه تنتهي بـ⟨ل، سكون⟩ لكلّ جذر. -/
theorem amr_fill_last (k : Nat) (hk : k ∈ amrTemplates) (r : Wazn.Root) :
    (Wazn.fill (Sarf.templ k) r).getLast? = some ⟨r 2, 3⟩ := by
  have h := List.all_eq_true.1 Filiyya.amr_ends_like_jazm.1 k hk
  simp only [beq_iff_eq] at h
  unfold Wazn.fill
  rw [List.getLast?_map, h]
  rfl

/-- صيغةُ الأمر مخاطبٌ أبدًا عند قارئ المقام: لكلّ قالبِ أمرٍ ولكلّ جذرٍ لا ألفَ فيه ولا تاءَ في آخره وبلا
لاحقةِ فاعل. -/
theorem amr_is_mukhatab (k : Nat) (hk : k ∈ amrTemplates) (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1)
    (hr3 : (r 2).val ≠ 3) (hns : Maqam.shakhsSuffix (Wazn.fill (Sarf.templ k) r) = none)
    (hsub : Filiyya.hasSubject (Wazn.fill (Sarf.templ k) r) = false) :
    Maqam.shakhs (Wazn.fill (Sarf.templ k) r) = some .mukhatab := by
  obtain ⟨d1, d2⟩ := sigha_states_disjoint
  have hwf : Wazn.WF (Sarf.templ k) := of_decide_eq_true (List.all_eq_true.1 amr_templates_wf k hk)
  have hs := Wazn.states_fill (Sarf.templ k) r
  have hnp : Maqam.isPresent (Wazn.fill (Sarf.templ k) r) = false := by
    apply Bool.eq_false_iff.2
    intro h
    obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 h
    have hon : Sarf.onTemplate (Sarf.templ q) (Maqam.withPrefix 28 (Wazn.fill (Sarf.templ k) r)) = true := by
      simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
    have hs' := states_of_onTemplate _ _ hon
    rw [withPrefix_states] at hs'
    have hne := List.all_eq_true.1 (List.all_eq_true.1 d2 q hq) k hk
    simp only [bne_iff_ne, ne_eq] at hne
    exact hne (hs'.symm.trans hs)
  have h0 : (Maqam.pastTemplates.any fun q => Maqam.onTemplateRoot q (Wazn.fill (Sarf.templ k) r)) = false := by
    apply Bool.eq_false_iff.2
    intro h
    obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 h
    have hon : Sarf.onTemplate (Sarf.templ q) (Wazn.fill (Sarf.templ k) r) = true := by
      simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
    have hs' := states_of_onTemplate _ _ hon
    have hne := List.all_eq_true.1 (List.all_eq_true.1 d1 q hq) k (List.mem_append_right _ hk)
    simp only [bne_iff_ne, ne_eq] at hne
    exact hne (hs'.symm.trans hs)
  have h1 : (Filiyya.amrTemplates.any fun q => Maqam.onTemplateRoot q (Wazn.fill (Sarf.templ k) r)) = true :=
    List.any_eq_true.2 ⟨k, hk, onTemplateRoot_fill k hwf r hr⟩
  have hsp : Maqam.shakhsPresent (Wazn.fill (Sarf.templ k) r) = none := by simp [Maqam.shakhsPresent, hnp]
  have hlast : (Wazn.fill (Sarf.templ k) r).getLast? ≠ some (c 3 3) := by
    rw [amr_fill_last k hk r]
    intro heq
    have := congrArg (fun o : Option SCell => (o.map (·.carrier.val))) heq
    simp at this
    exact hr3 this
  simp [Maqam.shakhs, hns, hsp, Maqam.shakhsPast, hsub, h0, h1, hlast]

/-- لا قالبَ أمرٍ للمتكلّم أو الغائب: أمرُهما باللام على المضارع (لِيَكْتُبْ)، لا بقالب الأمر. -/
theorem ghaib_amr_by_lam (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1) :
    let v := Maqam.withPrefix 28 (Wazn.fill (Sarf.templ 4) r)
    sigha v = some .mudari ∧ Maqam.shakhsPresent v = some .ghaib ∧
    (Jazm.amr (Jazm.sukun v)).take 1 = [⟨⟨23, by decide⟩, 1⟩] := by
  intro v
  refine ⟨(sigha_of_fill r hr).2.2 4 (by decide) 28 (by decide),
    (Maqam.present_prefix_reads_person 4 (by decide) r hr).2.2.2, rfl⟩

/-! ## أدواتُ الإزاحة -/

def sa : List SCell := [c 12 0]
def sawfa : List SCell := [c 12 0, c 27 3, c 20 0]
def lam : List SCell := [c 23 0, c 24 3]
def lan : List SCell := [c 23 0, c 25 3]
def kana : List SCell := [c 22 0, c 1 3, c 25 0]

inductive Shift where
  | sa | sawfa | lam | lan | kana
  deriving DecidableEq, Repr

/-- الإزاحةُ عمليّةٌ على المضارع وحدَه: السينُ متّصلةٌ، وسَوْفَ وكَانَ بلا أثرٍ على الخانة، ولَمْ جزمٌ، ولَنْ نصب. -/
def shift (s : Shift) (v : List SCell) : Option (List SCell × List SCell) :=
  if sigha v != some .mudari then none
  else some (match s with
    | .sa => ([], sa ++ v)
    | .sawfa => (sawfa, v)
    | .lam => (lam, Jazm.sukun v)
    | .lan => (lan, Nawasikh.nasb v)
    | .kana => (kana, v))

theorem shift_only_present (s : Shift) (v : List SCell) :
    (shift s v).isSome = true ↔ sigha v = some .mudari := by
  unfold shift
  cases hs : (sigha v != some .mudari)
  · simp only [Bool.false_eq_true, ite_false, Option.isSome_some, true_iff]
    simpa [bne_eq_false_iff_eq] using hs
  · simp only [ite_true, Option.isSome_none, Bool.false_eq_true, false_iff]
    simpa [bne_iff_ne] using hs

/-- الماضي والأمر لا يُزاحان بأداة. -/
theorem past_not_shifted (s : Shift) (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1) :
    (∀ k ∈ pastTemplates, shift s (Wazn.fill (Sarf.templ k) r) = none) ∧
    (∀ k ∈ amrTemplates, shift s (Wazn.fill (Sarf.templ k) r) = none) := by
  obtain ⟨h1, h2, _⟩ := sigha_of_fill r hr
  exact ⟨fun k hk => by simp [shift, h1 k hk], fun k hk => by simp [shift, h2 k hk]⟩

theorem sa_restores (v : List SCell) : (sa ++ v).drop 1 = v := rfl
theorem lam_restores (v : List SCell) :
    Afal.initOf (Jazm.sukun v) = Afal.initOf v := Filiyya.initOf_setLast v 3

theorem sa_licensed (v : List SCell) (hv : licensed v = true) : licensed (sa ++ v) = true :=
  Rawabit.proclitic_keeps_licence _ 0 (by decide) v hv

theorem shifts_in_rawabit :
    (["سَ", "سَوْفَ"].all fun n => Rawabit.particles.any fun p => p.name == n && p.amal == .none) = true ∧
    (Rawabit.particles.any fun p => p.name == "لَمْ" && p.amal == .jazm) = true ∧
    (Rawabit.particles.any fun p => p.name == "لَنْ" && p.amal == .nasb) = true ∧
    Nawasikh.kanaSisters.head?.map (·.2) = some kana := by
  refine ⟨by decide, by decide, by decide, rfl⟩

/-! ## القارئ -/

inductive Jiha where
  | madi | mudari | mustaqbal | madiManfi | mustaqbalManfi | madiMustamirr | amr | unread
  deriving DecidableEq, Repr

/-- الجهةُ من الكلمة وما قبلها: السينُ صدرًا على مضارع، أو سَوْفَ/لَمْ/لَنْ/كَانَ قبلَه، وإلّا صيغتُه. -/
def jiha (prev v : List SCell) : Jiha :=
  if v.take 1 == sa && sigha (v.drop 1) == some .mudari then .mustaqbal
  else match sigha v with
    | some .madi => .madi
    | some .amr => .amr
    | some .mudari =>
        if prev == sawfa then .mustaqbal
        else if prev == kana then .madiMustamirr
        else .mudari
    | none =>
        if prev == lam && sigha (setLast v 2) == some .mudari then .madiManfi
        else if prev == lan && sigha (setLast v 2) == some .mudari then .mustaqbalManfi
        else .unread

def yaktubu : List SCell := [c 28 0, c 22 3, c 3 2, c 2 2]       -- يَكْتُبُ
def kataba : List SCell := [c 22 0, c 3 0, c 2 0]                 -- كَتَبَ
def uktub : List SCell := [c 0 2, c 22 3, c 3 2, c 2 3]           -- اُكْتُبْ

/-- كَتَبَ ماضٍ؛ يَكْتُبُ مضارع؛ سَيَكْتُبُ وسَوْفَ يَكْتُبُ مستقبل؛ لَمْ يَكْتُبْ ماضٍ منفيّ؛ لَنْ يَكْتُبَ
مستقبلٌ منفيّ؛ كَانَ يَكْتُبُ ماضٍ مستمرّ؛ اُكْتُبْ أمر؛ سَكَتَبَ لا يُقرأ (السينُ لا تدخل على الماضي)، وسَوْفَ كَتَبَ ماضٍ بلا إزاحة. -/
theorem jiha_witnesses :
    jiha [] kataba = .madi ∧ jiha [] yaktubu = .mudari ∧ jiha [] (sa ++ yaktubu) = .mustaqbal ∧
    jiha sawfa yaktubu = .mustaqbal ∧ jiha lam (Jazm.sukun yaktubu) = .madiManfi ∧
    jiha lan (Nawasikh.nasb yaktubu) = .mustaqbalManfi ∧ jiha kana yaktubu = .madiMustamirr ∧
    jiha [] uktub = .amr ∧ jiha [] (sa ++ kataba) = .unread ∧ jiha sawfa kataba = .madi ∧
    jiha [] Jumla.zayd = .unread := by decide

end Slge.Jiha
