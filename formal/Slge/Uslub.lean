import Slge.Naat

/-!
# الأسلوب: الخبرُ وحدَه يحتمل الصدقَ والكذب، والإنشاءُ يُقرأ من الخانة لا يُكتب باليد

* **الأسلوبُ من الخانة** (د٤): الإنشاءُ طلبيٌّ (أمرٌ بصيغته، نهيٌ بلَا والجزم، استفهامٌ بأداته، نداءٌ بأداته،
  تمنٍّ بلَيْتَ، ترجٍّ بلَعَلَّ) وغيرُ طلبيّ (تعجّبٌ بمَا أَفْعَلَ ومنصوب، مدحٌ وذمٌّ بنِعْمَ وبِئْسَ)؛ وما سواه
  من الجمل الاسميّة والفعليّة خبرٌ (`uslub`). أدواتُ الإنشاء جدولٌ حاصرٌ مرخَّصٌ من جدول الربط
  (`tools_licensed`، `tools_in_rawabit`).
* **الصدقُ والكذب** للخبر وحده: `truthApt u = true ↔ u = .khabar` (`truth_iff_khabar`) — الإنشاءُ كلُّه
  محرومٌ منهما بالتعريف، والمبرهَنُ هو **أنّ القراءةَ من الخانة**: الأمرُ إنشاءٌ لكلّ قالبِ أمرٍ ولكلّ جذر
  (`amr_is_insha`)، ولَا تفصل النهيَ (إنشاء) عن النفي (خبر) بخانة آخر الفعل وحدها لكلّ قالبِ مضارعٍ ولكلّ
  جذر — لَا تَكْذِبْ إنشاءٌ ولَا تَكْذِبُ خبرٌ (`la_splits_by_last_state`)، ومَا أَفْعَلَ تعجّبٌ إن نُصب ما
  بعده وخبرٌ (نفيٌ) إن رُفع، لكلّ جذر (`ma_afala_splits_by_next_case`).
* النهيُ لا يقع إلّا على المضارع (`nahy_only_present`)، والتعجّبُ على قالب أَفْعَلَ بعينه.
القياسُ على MASAQ في بايثون: لَا الناهيةُ (حرف جزم) ولَا النافيةُ (حرف غير عامل) مرجعٌ محجوبٌ لقانون الخانة،
وفعلُ الأمر والاستفهام. الحصرُ المُرسَل في هذه الرسالة جملةٌ فعليّةٌ بأجناسٍ مكتوبةٍ باليد (`Genus`) وإجهادٌ
يقارن الدالّةَ بنفسها — لم يُدخَل منه شيء؛ وما طُلب (الخبرُ والإنشاء) دخل على الخانات.
-/

namespace Slge.Uslub

open Slge.Categories (c)
open Slge.Zuruf (setLast)

inductive Uslub where
  | khabar | amr | nahy | istifham | nida | tamanni | tarajji | taajjub | madhDhamm | unread
  deriving DecidableEq, Repr

/-- الصدقُ والكذبُ للخبر وحده. -/
def truthApt : Uslub → Bool
  | .khabar => true
  | _ => false

theorem truth_iff_khabar (u : Uslub) : truthApt u = true ↔ u = .khabar := by
  cases u <;> simp [truthApt]

/-! ## الأدوات -/

def la : List SCell := [c 23 0, c 1 3]                                  -- لَا
def ma : List SCell := [c 24 0, c 1 3]                                  -- مَا
def layta : List SCell := [c 23 0, c 28 3, c 3 0]                       -- لَيْتَ
def laalla : List SCell := [c 23 0, c 18 0, c 23 3, c 23 0]             -- لَعَلَّ
def nima : List SCell := [c 25 1, c 18 3, c 24 0]                       -- نِعْمَ
def bisa : List SCell := [c 2 1, c 0 3, c 12 0]                         -- بِئْسَ
def istifhamTools : List (List SCell) := [[c 0 0], [c 26 0, c 23 3]]    -- أَ، هَلْ

def tools : List (String × List SCell × Uslub) :=
  [("لَا", la, .nahy), ("أَ", [c 0 0], .istifham), ("هَلْ", [c 26 0, c 23 3], .istifham),
   ("لَيْتَ", layta, .tamanni), ("لَعَلَّ", laalla, .tarajji), ("مَا", ma, .taajjub),
   ("نِعْمَ", nima, .madhDhamm), ("بِئْسَ", bisa, .madhDhamm)] ++
  Nida.particles.map fun p => (p.1, p.2, .nida)

theorem tools_licensed : tools.all (fun t => licensed t.2.1) = true := by decide
theorem tools_count : tools.length = 14 := by decide

/-- الأدواتُ الحرفيّة في جدول أدوات الربط بعملها: لَا خانةٌ واحدة (الحكمُ من الفعل بعدها: `Jazm`)، ولَيْتَ
ولَعَلَّ نصبَ الاسم، وهَلْ بلا عمل؛ وأدواتُ النداء جدولُ `Nida`، وأسماءُ الاستفهام جدولُ `Istifham`. -/
theorem tools_in_rawabit :
    (Rawabit.particles.any fun p => p.name == "لَا" && p.cells == la) = true ∧
    Jazm.jazimOne.any (·.2 == la) = true ∧
    (["لَيْتَ", "لَعَلَّ"].all fun n => Rawabit.particles.any fun p => p.name == n && p.amal == .nasbIsm) = true ∧
    (Rawabit.particles.any fun p => p.name == "هَلْ" && p.amal == .none) = true ∧
    Nawasikh.innaSisters.any (·.2 == layta) = true ∧ Nawasikh.innaSisters.any (·.2 == laalla) = true := by
  refine ⟨by decide, by decide, by decide, by decide, by decide⟩

/-! ## القارئ -/

/-- مضارعٌ بأيّ حالةٍ للآخر. -/
def presentAnyMood (w : List SCell) : Bool := Jiha.sigha (setLast w 2) == some .mudari

/-- الأسلوبُ من الكلمة وما قبلها وما بعدها: الأمرُ بصيغته؛ لَا + مضارعٍ آخرُه ساكنٌ نهيٌ ومرفوعٌ نفيٌ (خبر)؛
أداةُ استفهامٍ أو اسمُه قبلَها استفهام؛ أداةُ نداءٍ قبلَها نداء؛ لَيْتَ تمنٍّ ولَعَلَّ ترجٍّ؛ مَا + أَفْعَلَ ومنصوبٌ
بعده تعجّبٌ ومرفوعٌ نفي؛ نِعْمَ وبِئْسَ مدحٌ وذمّ؛ وما سواه من فعلٍ أو مبتدأٍ خبر. -/
def uslub (prev w : List SCell) (next : Option (List SCell)) : Uslub :=
  if Jiha.sigha w == some .amr then .amr
  else if prev == la && presentAnyMood w then
    (if w.getLast?.map (·.state.val) == some 3 then .nahy else .khabar)
  else if prev == ma && Maqam.onTemplateRoot 11 w then
    (match next with
      | some n => if Tawabi.caseClass n == .nasb then .taajjub else .khabar
      | none => .unread)
  else if istifhamTools.contains prev || (Istifham.forms.any (·.2 == prev) && prev != ma) then .istifham
  else if Nida.particles.any (·.2 == prev) then .nida
  else if prev == layta then .tamanni
  else if prev == laalla then .tarajji
  else if w == nima || w == bisa then .madhDhamm
  else if (Jiha.sigha w).isSome || presentAnyMood w || Jumla.mubtadaKind w != .unread then .khabar
  else .unread

theorem setLast_id : ∀ (v : List SCell) (st : Fin 4), (∀ x, v.getLast? = some x → x.state = st) →
    setLast v st = v
  | [], _, _ => rfl
  | [x], st, h => by
    have := h x rfl
    simp [setLast, ← this]
  | x :: y :: t, st, h => by
    simp only [setLast, List.cons.injEq, true_and]
    exact setLast_id (y :: t) st (fun z hz => h z (by simpa using hz))

/-- الأمرُ إنشاءٌ لكلّ قالبِ أمرٍ ولكلّ جذرٍ لا ألفَ فيه، مهما كان ما قبله وما بعده. -/
theorem amr_is_insha (k : Nat) (hk : k ∈ Jiha.amrTemplates) (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1)
    (prev : List SCell) (next : Option (List SCell)) :
    uslub prev (Wazn.fill (Sarf.templ k) r) next = .amr ∧
    truthApt (uslub prev (Wazn.fill (Sarf.templ k) r) next) = false := by
  have h := (Jiha.sigha_of_fill r hr).2.1 k hk
  simp [uslub, h, truthApt]

theorem present_fill_last (k : Nat) (hk : k ∈ Jiha.presentTemplates) (r : Wazn.Root) (p : Fin 29) :
    (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)).getLast? = some ⟨r 2, 2⟩ := by
  have h := List.all_eq_true.1 (by decide : Jiha.presentTemplates.all
    (fun k => (Sarf.templ k).getLast? == some (.slot 2 2))) k hk
  simp only [beq_iff_eq] at h
  have hlen := List.all_eq_true.1 (by decide : Jiha.presentTemplates.all
    (fun k => decide (2 ≤ (Sarf.templ k).length))) k hk
  have hlen' : 2 ≤ (Wazn.fill (Sarf.templ k) r).length := by
    unfold Wazn.fill; rw [List.length_map]; exact of_decide_eq_true hlen
  have hf : (Wazn.fill (Sarf.templ k) r).getLast? = some ⟨r 2, 2⟩ := by
    unfold Wazn.fill; rw [List.getLast?_map, h]; rfl
  match hv : Wazn.fill (Sarf.templ k) r with
  | [] => simp [hv] at hlen'
  | [x] => simp [hv] at hlen'
  | x :: y :: t =>
    rw [hv] at hf
    simp only [Maqam.withPrefix, List.getLast?_cons_cons]
    simpa using hf

/-- حالاتُ القائمة بعد تغيير الآخر. -/
def setLastSt : List (Fin 4) → Fin 4 → List (Fin 4)
  | [], _ => []
  | [_], st => [st]
  | x :: y :: t, st => x :: setLastSt (y :: t) st

theorem map_state_setLast : ∀ (v : List SCell) (st : Fin 4),
    (setLast v st).map SCell.state = setLastSt (v.map SCell.state) st
  | [], _ => rfl
  | [_], _ => rfl
  | x :: y :: t, st => by
    simp only [setLast, List.map_cons, setLastSt]
    exact congrArg _ (map_state_setLast (y :: t) st)

theorem sukun_present_not_past (k : Nat) (hk : k ∈ Jiha.presentTemplates) (r : Wazn.Root) (p : Fin 29) :
    (Jiha.pastTemplates.any fun q =>
      Maqam.onTemplateRoot q (Jazm.sukun (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)))) = false := by
  apply Bool.eq_false_iff.2
  intro hp
  obtain ⟨q, hq, hqw⟩ := List.any_eq_true.1 hp
  have hon : Sarf.onTemplate (Sarf.templ q) (Jazm.sukun (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r))) = true := by
    simp only [Maqam.onTemplateRoot, Bool.and_eq_true] at hqw; exact hqw.1
  have hst := Jiha.states_of_onTemplate _ _ hon
  have hv : (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)).map SCell.state = (Sarf.templ k).map Wazn.stateOf := by
    rw [Jiha.withPrefix_states, Wazn.states_fill]
  have hsk : (Jazm.sukun (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r))).map SCell.state =
      setLastSt ((Sarf.templ k).map Wazn.stateOf) 3 := by
    rw [← hv]; exact map_state_setLast _ 3
  rw [hsk] at hst
  have := List.all_eq_true.1 (List.all_eq_true.1 (by decide : Jiha.presentTemplates.all fun k =>
    Jiha.pastTemplates.all fun q =>
      setLastSt ((Sarf.templ k).map Wazn.stateOf) 3 != (Sarf.templ q).map Wazn.stateOf) k hk) q hq
  simp only [bne_iff_ne, ne_eq] at this
  exact this hst

/-- لَا تفصل النهيَ عن النفي بخانة آخر الفعل: لكلّ قالبِ مضارعٍ وصدرٍ وجذر، المجزومُ إنشاءٌ والمرفوعُ خبر —
بشرط ألّا تشابه الصورةُ المجزومة قالبَ أمرٍ بالخانة (يَلْلِمْ من الجذر ل‑ل‑م يشابه لَلِّمْ: الخانةُ لا تفصل). -/
theorem la_splits_by_last_state (k : Nat) (hk : k ∈ Jiha.presentTemplates) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) (p : Fin 29) (hp : p ∈ [(0 : Fin 29), 25, 3, 28]) (next : Option (List SCell))
    (hna : (Jiha.amrTemplates.any fun q =>
      Maqam.onTemplateRoot q (Jazm.sukun (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)))) = false) :
    uslub la (Jazm.sukun (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r))) next = .nahy ∧
    uslub la (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)) next = .khabar ∧
    truthApt (uslub la (Jazm.sukun (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r))) next) = false ∧
    truthApt (uslub la (Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r)) next) = true := by
  have hs := (Jiha.sigha_of_fill r hr).2.2 k hk p hp
  have hlast := present_fill_last k hk r p
  have hnp := sukun_present_not_past k hk r p
  generalize hvv : Maqam.withPrefix p (Wazn.fill (Sarf.templ k) r) = v at hs hlast hna hnp ⊢
  have hid : setLast v 2 = v := setLast_id v 2 (fun x hx => by rw [hlast] at hx; cases hx; rfl)
  have hne : v ≠ [] := by intro h; rw [h] at hlast; simp at hlast
  have hpm : presentAnyMood v = true := by simp [presentAnyMood, hid, hs]
  have hpm' : presentAnyMood (Jazm.sukun v) = true := by
    simp [presentAnyMood, Jazm.sukun, Shibh.setLast_setLast, hid, hs]
  have hnotamr : (Jiha.sigha v == some .amr) = false := by simp [hs]
  have hnotamr' : (Jiha.sigha (Jazm.sukun v) == some .amr) = false := by
    simp [Jiha.sigha, hna, hnp]
  have hl' : (Jazm.sukun v).getLast?.map (·.state.val) = some 3 := by
    obtain ⟨i, kk, hi⟩ := Nawasikh.setLast_eq_append v 3 hne
    unfold Jazm.sukun; rw [hi, List.getLast?_concat]; rfl
  have hl : v.getLast?.map (·.state.val) = some 2 := by rw [hlast]; rfl
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp [uslub, hnotamr', hpm', hl']
  · simp [uslub, hnotamr, hpm, hl]
  · simp [uslub, hnotamr', hpm', hl', truthApt]
  · simp [uslub, hnotamr, hpm, hl, truthApt]

/-- النهيُ لا يقع إلّا على المضارع: ما قُرئ نهيًا فهو مضارعٌ بحالةٍ ما. -/
theorem nahy_only_present (prev w : List SCell) (next : Option (List SCell))
    (h : uslub prev w next = .nahy) : presentAnyMood w = true := by
  cases hpm : presentAnyMood w with
  | true => rfl
  | false =>
    exfalso
    simp [uslub, hpm] at h
    repeat' split at h
    all_goals first | exact absurd h (by decide) | (simp at h)

/-- مَا أَفْعَلَ: تعجّبٌ إن نُصب ما بعده وخبرٌ (نفيٌ) إن رُفع — لكلّ جذرٍ لا ألفَ فيه، ولكلّ اسمٍ بعده. -/
theorem ma_afala_splits_by_next_case (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1) (n : List SCell)
    (hne : n ≠ []) :
    uslub ma (Wazn.fill (Sarf.templ 11) r) (some (Nawasikh.tanwin (Nawasikh.nasb n))) = .taajjub ∧
    uslub ma (Wazn.fill (Sarf.templ 11) r) (some (Nawasikh.tanwin (Nawasikh.raf n))) = .khabar := by
  have hwf : Wazn.WF (Sarf.templ 11) := by decide
  have hon := Jiha.onTemplateRoot_fill 11 hwf r hr
  have hsig := (Jiha.sigha_of_fill r hr).1 11 (by decide)
  have hnotamr : (Jiha.sigha (Wazn.fill (Sarf.templ 11) r) == some .amr) = false := by simp [hsig]
  have hla : (ma == la) = false := by decide
  refine ⟨?_, ?_⟩
  · simp [uslub, hnotamr, hla, hon, Nawasikh.caseClass_nasb_tanwin n hne]
  · simp [uslub, hnotamr, hla, hon, Nawasikh.caseClass_raf_tanwin n hne]

def taktub : List SCell := [c 3 0, c 22 3, c 3 2, c 2 2]         -- تَكْتُبُ
def akrama : List SCell := [c 0 0, c 22 3, c 10 0, c 24 0]        -- أَكْرَمَ
def hal : List SCell := [c 26 0, c 23 3]
def ya : List SCell := Nida.ya

/-- اُكْتُبْ أمر؛ لَا تَكْتُبْ نهيٌ ولَا تَكْتُبُ خبر؛ هَلْ تَكْتُبُ استفهام؛ يَا رَجُلُ نداء؛ لَيْتَ زَيْدًا تمنٍّ؛
لَعَلَّ زَيْدًا ترجٍّ؛ مَا أَكْرَمَ زَيْدًا تعجّبٌ ومَا أَكْرَمَ زَيْدٌ خبر؛ نِعْمَ مدح؛ كَتَبَ والرَّجُلُ خبر؛ والحرفُ
وحدَه لا يُقرأ. -/
theorem uslub_witnesses :
    uslub [] Jiha.uktub none = .amr ∧ uslub la (Jazm.sukun taktub) none = .nahy ∧
    uslub la taktub none = .khabar ∧ uslub hal taktub none = .istifham ∧
    uslub ya Naat.rajul none = .nida ∧ uslub layta Jumla.zayd none = .tamanni ∧
    uslub laalla Jumla.zayd none = .tarajji ∧
    uslub ma akrama (some (Nawasikh.tanwin (Nawasikh.nasb Naat.rajul))) = .taajjub ∧
    uslub ma akrama (some Jumla.zayd) = .khabar ∧ uslub [] nima none = .madhDhamm ∧
    uslub [] Jiha.kataba none = .khabar ∧ uslub [] Naat.alrajul none = .khabar ∧
    uslub [] la none = .unread ∧
    (truthApt (uslub la taktub none) = true ∧ truthApt (uslub la (Jazm.sukun taktub) none) = false) := by
  decide

end Slge.Uslub
