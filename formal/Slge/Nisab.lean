import Slge.Shibh

/-!
# النِّسَبُ الثلاث: الإسنادُ عمليّةٌ واحدة، والتقييدُ لا يُنشئ رفعًا، والتضمينُ ترتيبٌ جزئيٌّ على الخانات

* **الإسناديّة** (د٤): المسندُ إليه مرفوعٌ بعمليّةٍ واحدةٍ في الجملتين — مبتدأُ الاسميّة (`Jumla.nominal`) وفاعلُ
  الفعليّة (`Filiyya.fail`) هما `Nawasikh.raf` بعينه (`isnad_one_operation`)، فيُقرأ رفعًا لكلّ جذع
  (`isnad_reads_raf`)؛ والمسندُ: خبرٌ مرفوعٌ أو فعلٌ على قالبه أو شبهُ جملة بكونٍ محذوف (`Jumla.khabarKind`).
* **التقييديّة** (د٨): كلُّ مقيِّدٍ عمليّةٌ مبرهَنةٌ في بابها، ولا يُنشئ رفعًا بنفسه: الحالُ والتمييزُ والمفعولُ
  نصبٌ لكلّ جذع (`taqyid_nasb`)، والإضافةُ والجارُّ جرٌّ لكلّ اسم (`taqyid_jarr`)، والنعتُ يأخذ حالةَ متبوعه
  (`Tawabi.follows`؛ `naat_follows`) — فالرفعُ في التقييد تبعٌ لا أصل (`taqyid_raf_only_by_following`).
* **التضمينيّة** (د١٦): الصورةُ تتضمّن جذرَها — حوامِلُ الجذر الثلاثة جزءٌ مرتَّبٌ (`List.Sublist`) من حوامل الصورة
  لكلّ قالبٍ مودَعٍ ولكلّ جذر (`form_contains_root`). والتضمينُ على الخانات هو الجزئيّةُ المرتَّبة: انعكاسيٌّ
  ومتعدٍّ ومتضادُّ التباين (`contains_refl`، `contains_trans`، `contains_antisymm`) — ترتيبٌ جزئيٌّ مبرهَنٌ
  من نواة Lean لا من نوعٍ مُعرَّفٍ باليد. و**الفصلُ**: الجذرُ الواحد (الجنس) تشقّه القوالبُ أنواعًا متباينة —
  125 صورةً للميزان متباينةٌ كلُّها (`species_distinct`)، فما اختلف قالبُه اختلفت صورتُه.
* القارئُ `nisba` يقرأ النسبةَ بين كلمتين من خانتيهما: إسنادٌ (مسندٌ إليه مرفوعٌ أو ضميرٌ أو فعلٌ، ومسند)،
  تقييدٌ (نصبٌ منوَّنٌ، أو جرٌّ، أو تبعيّةٌ في الحالة)، وما سواه لا يُقرأ؛ والتضمينُ بين كلمتين معنًى (الإنسانُ
  حيوان) لا خانة — باسمه.
القياسُ على MASAQ (أزواجُ الإسناد والتقييد بشهادات البوّابة) في بايثون.
الحصرُ المُرسَل أحال على ملفّ `differentiation_and_verbal_matrix.lean` لم يُرفَق؛ وفحصُ إجهاده في بايثون
يعدّ «صحيحًا» ما بناه صحيحًا بالتعريف (100% بالبناء) — لم يُدخَل منه شيء.
-/

namespace Slge.Nisab

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## الإسناديّة -/

theorem isnad_one_operation (m k : List SCell) :
    (Jumla.nominal m k).mubtada = Nawasikh.raf m ∧ Filiyya.fail m = Nawasikh.raf m ∧
    Filiyya.naib m = Nawasikh.raf m := ⟨rfl, rfl, rfl⟩

theorem isnad_reads_raf (m : List SCell) (hne : m ≠ []) :
    Tawabi.caseClass (Jumla.nominal m []).mubtada = .raf ∧ Tawabi.caseClass (Filiyya.fail m) = .raf :=
  ⟨(Jumla.nominal_reads_raf m [c 0 0] hne (by simp)).1, Filiyya.fail_reads_raf m hne⟩

/-! ## التقييديّة -/

/-- الحالُ والتمييزُ والمفعولُ نصبٌ لكلّ جذع. -/
theorem taqyid_nasb (w : List SCell) (hne : w ≠ []) :
    Tawabi.caseClass (Mansubat.hal w) = .nasb ∧ Tawabi.caseClass (Mansubat.tamyiz w) = .nasb ∧
    Tawabi.caseClass (Filiyya.maful w) = .nasb :=
  ⟨Mansubat.nakira_reads_nasb w hne, Mansubat.nakira_reads_nasb w hne, Filiyya.maful_reads_nasb w hne⟩

/-- المضافُ إليه والمجرورُ بالحرف جرٌّ لكلّ اسم. -/
theorem taqyid_jarr (h w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25 ∧ x.carrier.val ≠ 3) :
    Tawabi.caseClass (Majrurat.jarr w) = .jarr ∧
    Tawabi.caseClass ((Shibh.jarrMajrur h w).drop h.length) = .jarr := by
  have := Shibh.jarr_majrur_reads_jarr h w hne hk
  exact ⟨this.2, by rw [this.1]; exact this.2⟩

/-- النعتُ يأخذ حالةَ متبوعه: التبعيّةُ تناظريّةٌ وانعكاسيّةٌ على المقروء. -/
theorem naat_follows (a b : List SCell) (ha : Tawabi.caseClass a ≠ .unread) :
    Tawabi.follows a b = Tawabi.follows b a ∧ Tawabi.follows a a = true :=
  ⟨Tawabi.follows_symm a b, Tawabi.follows_refl a ha⟩

/-- الرفعُ في التقييد تبعٌ لا أصل: ما نُصب أو جُرَّ لا يُقرأ رفعًا، والتابعُ المرفوع إنّما رُفع بمتبوعه. -/
theorem taqyid_raf_only_by_following (w b : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25 ∧ x.carrier.val ≠ 3) :
    Tawabi.caseClass (Mansubat.hal w) ≠ .raf ∧ Tawabi.caseClass (Majrurat.jarr w) ≠ .raf ∧
    (Tawabi.follows (Nawasikh.raf w) b = true → Tawabi.caseClass b = .raf) := by
  refine ⟨by rw [(taqyid_nasb w hne).1]; decide, by rw [(taqyid_jarr [] w hne hk).1]; decide, ?_⟩
  intro hf
  unfold Tawabi.follows at hf
  rw [Nawasikh.caseClass_raf w hne] at hf
  cases hb : Tawabi.caseClass b <;> simp [hb, Tawabi.compatible] at hf ⊢

/-! ## التضمينيّة -/

/-- التضمينُ على الخانات: الجزئيّةُ المرتَّبة (`List.Sublist`). -/
def Contains (big small : List SCell) : Prop := List.Sublist small big

theorem contains_refl (w : List SCell) : Contains w w := List.Sublist.refl w
theorem contains_trans {a b d : List SCell} (h₁ : Contains a b) (h₂ : Contains b d) : Contains a d :=
  List.Sublist.trans h₂ h₁
theorem contains_antisymm {a b : List SCell} (h₁ : Contains a b) (h₂ : Contains b a) : a = b :=
  (List.Sublist.eq_of_length h₁ (Nat.le_antisymm h₁.length_le h₂.length_le)).symm

/-- حواملُ الجذر الثلاثة بترتيبها جزءٌ من حوامل الصورة لكلّ قالبٍ مودَع ولكلّ جذر. -/
def rootCarriers (r : Wazn.Root) : List (Fin 29) := [r 0, r 1, r 2]

theorem slots_ordered : Wazn.awzan.all (fun t => ([0, 1, 2] : List (Fin 3)).isSublist (Wazn.slots t)) = true := by
  decide

theorem map_carrier_fill (t : Wazn.Template) (r : Wazn.Root) :
    List.Sublist ((Wazn.slots t).map r) ((Wazn.fill t r).map SCell.carrier) := by
  induction t with
  | nil => exact List.Sublist.refl _
  | cons s t ih =>
    cases s with
    | lit x => exact List.Sublist.cons _ ih
    | slot i st => exact List.Sublist.cons_cons _ ih

theorem form_contains_root (t : Wazn.Template) (ht : t ∈ Wazn.awzan) (r : Wazn.Root) :
    List.Sublist (rootCarriers r) ((Wazn.fill t r).map SCell.carrier) := by
  have h1 : ([0, 1, 2] : List (Fin 3)).isSublist (Wazn.slots t) = true :=
    List.all_eq_true.1 slots_ordered t ht
  have h2 : List.Sublist ([0, 1, 2] : List (Fin 3)) (Wazn.slots t) := List.isSublist_iff_sublist.1 h1
  have h3 : List.Sublist (([0, 1, 2] : List (Fin 3)).map r) ((Wazn.slots t).map r) := h2.map r
  exact List.Sublist.trans h3 (map_carrier_fill t r)

/-- التضمينُ على الأوزان: سلسلةُ أسلاف الوزن في شبكة البصريّين حتى الجذر، بوقودٍ يكفي الشجرةَ كلَّها. -/
def F : Nat := Wazn.N

def chain (k : Nat) : Nat → List Nat
  | 0 => [k]
  | n + 1 => if k == Shabaka.root then [k] else match Shabaka.parentOf k with
      | some p => k :: chain p n
      | none => [k]

/-- البعدُ عن الجذر: طولُ السلسلة ناقصَ واحد. -/
def dist (k : Nat) (fuel : Nat) : Nat := (chain k fuel).length - 1

set_option maxRecDepth 4096 in
/-- كلُّ سلسلةٍ تنتهي بالجذر (`network_rooted` بصورةٍ أخرى)، والجذرُ بعدُه صفر. -/
theorem chains_end_at_root :
    ((List.range Wazn.N).all fun k => (chain k F).getLast? == some Shabaka.root) = true ∧ dist 29 F = 0 := by
  decide

set_option maxRecDepth 100000 in
/-- الفصل: الجنسُ الواحد (الميزان) تشقّه القوالبُ أنواعًا: ما اختلف قالبُه اختلفت صورتُه (الميزانُ يفصل
القوالبَ)؛ والصورةُ الواحدةُ المودَعةُ بمعنيين (فِعَال مصدرًا وجمعًا) قالبٌ واحدٌ — الفصلُ هناك معنًى. -/
theorem species_distinct :
    (Wazn.awzan.all fun t₁ => Wazn.awzan.all fun t₂ => (Wazn.mizan t₁ == Wazn.mizan t₂) == (t₁ == t₂)) = true := by
  decide

/-! ## القارئ -/

inductive Nisba where
  | isnad | taqyid | unread
  deriving DecidableEq, Repr

/-- المسندُ إليه: مرفوعٌ، أو ضميرٌ منفصل، أو مبنيٌّ من جداوله، أو فعلٌ (إسنادُ الفاعل). -/
def musnadIlayh (w : List SCell) : Bool :=
  Jumla.mubtadaKind w != .unread || (Filiyya.verbRoot w).isSome || Filiyya.hasSubject w

/-- النسبةُ بين كلمتين من خانتيهما: الثاني فعلٌ أو شبهُ جملةٍ بعد مسندٍ إليه ⇒ إسناد؛ منصوبٌ أو مجرور
⇒ تقييد؛ مرفوعٌ بعد نكرةٍ مرفوعةٍ وهو نكرة ⇒ تقييدٌ (نعتٌ بالتبعيّة)، وبعد مسندٍ إليه ⇒ إسناد؛ وما سواه لا
يُقرأ. العلمُ المنوَّن (زَيْدٌ) نكرةٌ بالخانة — باسمه. -/
def nisba (prev w : List SCell) : Nisba :=
  if Jumla.isVerb w || Jumla.shibhJumla w then
    (if Jumla.mubtadaKind prev != .unread then .isnad else .unread)   -- مبتدأٌ خبرُه جملةٌ أو شبهُها
  else if Jumla.mabniIsm w || Categories.pronouns.contains w then      -- الموصولُ والإشارةُ والضميرُ فاعلًا أو خبرًا
    (if (Filiyya.verbRoot prev).isSome || Filiyya.hasSubject prev || Jumla.mubtadaKind prev != .unread
      then .isnad else .unread)
  else match Tawabi.caseClass w with
    | .nasb => .taqyid                                                  -- النصبُ فضلةٌ: تقييدٌ أبدًا
    | .jarr => .taqyid
    | .nasbJarr => .taqyid
    | .raf =>
        if Jumla.nakira prev && Jumla.nakira w && Tawabi.caseClass prev = .raf then .taqyid
        else if musnadIlayh prev then .isnad else .unread
    | .unread => .unread

def ilm : List SCell := Shibh.ilm                                        -- الْعِلْمُ
def nur : List SCell := [c 25 2, c 27 3, c 10 2, c 25 3]                 -- نُورٌ
def karim : List SCell := [c 22 0, c 10 1, c 28 3, c 24 2, c 25 3]        -- كَرِيمٌ
def rakiban : List SCell := [c 10 0, c 1 3, c 22 1, c 2 0, c 25 3]        -- رَاكِبًا
def kitabu : List SCell := [c 22 1, c 3 0, c 1 3, c 2 2]                  -- كِتَابُ
def zaydin : List SCell := [c 11 0, c 28 3, c 8 1, c 25 3]                -- زَيْدٍ

/-- الْعِلْمُ نُورٌ وأَكَلَ زَيْدٌ وهُوَ قَائِمٌ إسناد؛ رَجُلٌ كَرِيمٌ تقييدٌ بالتبعيّة؛ رَاكِبًا وكِتَابُ زَيْدٍ تقييد؛
الْعِلْمُ دَرَسَ والْعِلْمُ فِي الدَّارِ إسناد؛ فعلٌ بعد فعلٍ لا يُقرأ. -/
theorem nisba_witnesses :
    nisba ilm nur = .isnad ∧ nisba Filiyya.akala Jumla.zayd = .isnad ∧
    nisba [c 26 2, c 27 0] Jumla.qaim = .isnad ∧
    nisba Jumla.rajul karim = .taqyid ∧ nisba Jumla.zayd rakiban = .taqyid ∧
    nisba kitabu zaydin = .taqyid ∧
    nisba ilm Jumla.darasa = .isnad ∧ nisba ilm Jumla.fidDar = .isnad ∧
    nisba Jumla.darasa Jumla.darasa = .unread := by decide

end Slge.Nisab
