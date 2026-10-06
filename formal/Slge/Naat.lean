import Slge.Jiha

/-!
# النعتُ الحقيقيّ: مطابقةٌ في أربعة من الخانات، والحملُ واحدٌ والفرقُ التعريف، والجملةُ بعد النكرة نعت

* **المتّجهُ الرباعيّ من الخانة** (د٤): الإعرابُ (`Tawabi.caseClass`)، والتعريفُ (نفيُ `Jumla.nakira`)،
  والجنسُ والعددُ (`Jumla.gender`، `Jumla.number`) — أربعةٌ تُقرأ من الخانات لا تُكتب باليد (`vec`).
* **النعتُ الحقيقيّ** مطابقةٌ في الأربعة (`naatOk`): انعكاسيٌّ على المقروء (`naatOk_refl`) وتناظريّ
  (`naatOk_symm`)؛ ومنه: الإعرابُ تبعٌ (`naatOk_case`)، والتعريفُ واحد (`naatOk_definite`)، والجنسُ
  والعددُ موافقان (`naatOk_agree`). **المخالفُ إعرابًا ممنوع**: مرفوعٌ لا يُنعَت بمنصوب لكلّ جذعين
  (`non_matching_case_blocked`)، و**المخالفُ تعريفًا ممنوع** (`non_matching_definite_blocked`).
* **الحملُ واحدٌ والفرقُ التعريف** (د٨): النعتُ والخبرُ على معرفةٍ مرفوعةٍ يتّفقان إعرابًا وجنسًا وعددًا ويفترقان
  في التعريف وحده: الرَّجُلُ الطَّوِيلُ نعتٌ والرَّجُلُ طَوِيلٌ خبر (`hamlKind`؛ `khabar_not_naat`:
  نكرةٌ بعد معرفةٍ ليست نعتًا لكلّ جذعين). وعامًّا: النكرةُ المرفوعةُ المنوَّنةُ على نكرةٍ مثلِها مطابقةٌ في
  الإعراب والتعريف لكلّ جذعين (`nakira_pair_two_coordinates`).
* **الجملةُ بعد النكرة نعتٌ وبعد المعرفة حال** (`jumlaMahall`): الحالُ تشترط صاحبًا معرفةً
  (`hal_requires_marifa`: لكلّ كلمة)، والجملةُ بعد النكرة المنوَّنة نعتٌ لكلّ جذع (`naat_after_nakira`).
* العمليّةُ `naat m k`: الجذعُ `k` على إعراب المنعوت وتعريفه (رفعٌ/نصبٌ/جرٌّ، ثمّ أل أو تنوين) — شواهدُ
  على الأربعة (`naat_witnesses`)؛ وعمومُ الجنس والعدد بعمليّاتهما في `Jumla.agree_ops`.
القياسُ على MASAQ (1,388 زوجَ نعتٍ بشهادات البوّابة) في بايثون. الحصرُ المُرسَل: متّجهاتُه (`NounVector`)
مكتوبةٌ باليد لا تُقرأ من كلمة، وفحصُ إجهاده يفحص ما بناه (`is_valid` ثمّ `assert` على المساواة نفسِها) —
لم يُدخَل منه شيء؛ ودخل معناه على الخانات: الأربعةُ مقروءةٌ، والمنعُ مبرهَنٌ لكلّ جذع.
-/

namespace Slge.Naat

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## المتّجه الرباعيّ -/

structure Vec where
  cc : Tawabi.CaseClass
  definite : Bool
  gender : Jumla.Gender
  number : Jumla.Number
  deriving DecidableEq, Repr

/-- الجنسُ والعددُ يُقرآن تحت التنوين. -/
def core (w : List SCell) : List SCell := Marifa.dropTanwin w

def vec (w : List SCell) : Vec :=
  ⟨Tawabi.caseClass w, !Jumla.nakira w, Jumla.gender (core w), Jumla.number (core w)⟩

/-- النعتُ الحقيقيّ: تبعٌ في الإعراب، وتعريفٌ واحد، وجنسٌ وعددٌ موافقان (تحت التنوين). -/
def naatOk (m n : List SCell) : Bool :=
  Tawabi.follows n m && (Jumla.nakira m == Jumla.nakira n) && Jumla.agree (core m) (core n)

theorem naatOk_refl (w : List SCell) (h : Tawabi.caseClass w ≠ .unread) : naatOk w w = true := by
  simp [naatOk, Tawabi.follows_refl w h, Jumla.agree]

theorem naatOk_symm (m n : List SCell) : naatOk m n = naatOk n m := by
  simp only [naatOk, Tawabi.follows_symm n m, Jumla.agree]
  cases Jumla.nakira m <;> cases Jumla.nakira n <;>
    cases hg : Jumla.gender (core m) <;> cases hg' : Jumla.gender (core n) <;>
    cases hn : Jumla.number (core m) <;> cases hn' : Jumla.number (core n) <;> rfl

theorem naatOk_case (m n : List SCell) (h : naatOk m n = true) : Tawabi.follows n m = true := by
  simp only [naatOk, Bool.and_eq_true] at h; exact h.1.1

theorem naatOk_definite (m n : List SCell) (h : naatOk m n = true) : Jumla.nakira m = Jumla.nakira n := by
  simp only [naatOk, Bool.and_eq_true, beq_iff_eq] at h; exact h.1.2

theorem naatOk_agree (m n : List SCell) (h : naatOk m n = true) : Jumla.agree (core m) (core n) = true := by
  simp only [naatOk, Bool.and_eq_true] at h; exact h.2

/-- مرفوعٌ لا يُنعَت بمنصوب، ولا منصوبٌ بمجرور، لكلّ جذعين. -/
theorem non_matching_case_blocked (m n : List SCell)
    (h : Tawabi.caseClass m = .raf ∧ Tawabi.caseClass n = .nasb ∨
         Tawabi.caseClass m = .nasb ∧ Tawabi.caseClass n = .jarr ∨
         Tawabi.caseClass m = .raf ∧ Tawabi.caseClass n = .jarr) : naatOk m n = false := by
  apply Bool.eq_false_iff.2
  intro hn
  have hf := naatOk_case m n hn
  unfold Tawabi.follows at hf
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ <;> rw [h1, h2] at hf <;> exact absurd hf (by decide)

/-- معرفةٌ لا تُنعَت بنكرة ولا نكرةٌ بمعرفة، لكلّ جذعين. -/
theorem non_matching_definite_blocked (m n : List SCell) (h : Jumla.nakira m ≠ Jumla.nakira n) :
    naatOk m n = false := by
  apply Bool.eq_false_iff.2
  intro hn
  exact h (naatOk_definite m n hn)

/-! ## الحملُ واحد: النعتُ والخبر -/

inductive Haml where
  | naat | khabar | unread
  deriving DecidableEq, Repr

/-- الحملُ على المعرفة المرفوعة: مطابقٌ في الأربعة ⇒ نعت؛ مرفوعٌ موافقٌ جنسًا وعددًا نكرةٌ بعد معرفةٍ ⇒ خبر. -/
def hamlKind (m n : List SCell) : Haml :=
  if naatOk m n then .naat
  else if Tawabi.caseClass m == .raf && Tawabi.caseClass n == .raf && Jumla.agree (core m) (core n) &&
      !Jumla.nakira m && Jumla.nakira n then .khabar
  else .unread

theorem khabar_not_naat (m n : List SCell) (h : hamlKind m n = .khabar) : naatOk m n = false := by
  unfold hamlKind at h
  cases hk : naatOk m n with
  | false => rfl
  | true => simp [hk] at h

/-- أل لا تُستحدَث بتغيير الآخر والتنوين: لكلّ جذعٍ بلا أل. -/
theorem hasAl_setLast_tanwin (w : List SCell) (st : Fin 4) (hst : st.val ≠ 3) (hne : w ≠ [])
    (h0 : Marifa.hasAl w = false) : Marifa.hasAl (setLast w st ++ [c 25 3]) = false := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w st hne
  have h1 : Marifa.hasAl (i ++ [⟨k, st⟩]) = false := hi ▸ Nawasikh.hasAl_setLast w st hst h0
  rw [hi]
  match i with
  | [] =>
    simp [Marifa.hasAl, c]
    intro _ _ h; exact absurd h (by decide)
  | [a] => simp [Marifa.hasAl, hst]
  | a :: l :: r =>
    cases r with
    | nil => simpa [Marifa.hasAl] using h1
    | cons x t => simpa [Marifa.hasAl] using h1

/-- لكلّ جذعين: المنوَّنُ المرفوعُ بلا أل على مثله مطابقٌ في الإعراب والتعريف. -/
theorem nakira_pair_two_coordinates (m k : List SCell) (hm : m ≠ []) (hk : k ≠ [])
    (ham : Marifa.hasAl m = false) (hak : Marifa.hasAl k = false) :
    Tawabi.follows (Nawasikh.tanwin (Nawasikh.raf k)) (Nawasikh.tanwin (Nawasikh.raf m)) = true ∧
    Jumla.nakira (Nawasikh.tanwin (Nawasikh.raf m)) = true ∧
    Jumla.nakira (Nawasikh.tanwin (Nawasikh.raf k)) = true := by
  have hal : ∀ w, w ≠ [] → Marifa.hasAl w = false → Marifa.hasAl (Nawasikh.tanwin (Nawasikh.raf w)) = false :=
    fun w hw hw0 => hasAl_setLast_tanwin w 2 (by decide) hw hw0
  have ht : ∀ w, w ≠ [] → Nida.hasTanwin (Nawasikh.tanwin (Nawasikh.raf w)) = true := by
    intro w hw
    obtain ⟨i, kk, hi⟩ := Nawasikh.setLast_eq_append w 2 hw
    unfold Nawasikh.tanwin Nawasikh.raf; rw [hi]; unfold Nida.hasTanwin
    simp only [List.append_assoc, List.reverse_append, List.reverse_cons, List.reverse_nil,
      List.nil_append, List.cons_append]
    simp [c, Ishara.v25, Ishara.s3]
  refine ⟨?_, ?_, ?_⟩
  · unfold Tawabi.follows
    rw [Nawasikh.caseClass_raf_tanwin k hk, Nawasikh.caseClass_raf_tanwin m hm]; rfl
  · simp [Jumla.nakira, ht m hm, hal m hm ham]
  · simp [Jumla.nakira, ht k hk, hal k hk hak]

/-! ## الجملةُ بعد الاسم -/

inductive Mahall where
  | naat | hal | unread
  deriving DecidableEq, Repr

/-- الجملُ بعد النكرات صفات، وبعد المعارف المقروءةِ الإعراب أحوال؛ وبعد الفعل والضمير لا تُقرأ. -/
def jumlaMahall (prev : List SCell) : Mahall :=
  if Jumla.isVerb prev || Categories.pronouns.contains prev then .unread
  else if Jumla.nakira prev then .naat
  else if Tawabi.caseClass prev != .unread then .hal
  else .unread

/-- الحالُ تشترط صاحبًا معرفة: ما قُرئ حالًا فصاحبُه ليس نكرة — لكلّ كلمة. -/
theorem hal_requires_marifa (prev : List SCell) (h : jumlaMahall prev = .hal) : Jumla.nakira prev = false := by
  unfold jumlaMahall at h
  split at h
  · exact absurd h (by decide)
  · split at h
    · exact absurd h (by decide)
    · rename_i h2
      exact Bool.eq_false_iff.2 h2

/-- بعد النكرة المنوَّنة المنصوبة نعتٌ لكلّ جذعٍ لا تشابه صورتُه فعلًا (اِفْعَنْ أمرُ فَعَنَ بالخانة). -/
theorem naat_after_nakira (w : List SCell) (hne : w ≠ []) (hal : Marifa.hasAl w = false)
    (hv : Jumla.isVerb (Mansubat.nakiraMansuba w) = false) :
    jumlaMahall (Mansubat.nakiraMansuba w) = .naat := by
  have ht := Mansubat.nakira_has_tanwin w hne
  have h2 : Marifa.hasAl (Mansubat.nakiraMansuba w) = false :=
    hasAl_setLast_tanwin w 0 (by decide) hne hal
  have hp : Mansubat.nakiraMansuba w ∉ Categories.pronouns := by
    intro hm
    have hall := List.all_eq_true.1
      (by decide : Categories.pronouns.all (fun p => !Nida.hasTanwin p) = true) _ hm
    rw [ht] at hall; simp at hall
  simp [jumlaMahall, Jumla.nakira, ht, h2, hv, hp]

/-! ## العمليّة والشواهد -/

/-- النعتُ عمليّة: الجذعُ على إعراب المنعوت (رفع/نصب/جرّ) ثمّ على تعريفه (أل أو تنوين). -/
def naat (m k : List SCell) : List SCell :=
  let k' := match Tawabi.caseClass m with
    | .raf => Nawasikh.raf k
    | .nasb => Nawasikh.nasb k
    | .jarr => Majrurat.jarr k
    | _ => k
  if Marifa.hasAl m then Marifa.al k' else if Jumla.nakira m then Nawasikh.tanwin k' else k'

def rajul : List SCell := [c 10 0, c 5 2, c 23 2]                     -- رَجُلُ
def tawil : List SCell := [c 16 0, c 27 1, c 28 3, c 23 2]            -- طَوِيلُ
def alrajul : List SCell := Marifa.al rajul                           -- الرَّجُلُ
def rajulun : List SCell := Nawasikh.tanwin rajul                     -- رَجُلٌ
def rajulan : List SCell := Nawasikh.tanwin (Nawasikh.nasb rajul)     -- رَجُلًا
def alrajuli : List SCell := Marifa.al (Majrurat.jarr rajul)          -- الرَّجُلِ
def madrasa : List SCell := Jumla.taNith [c 24 0, c 8 3, c 10 0, c 12 0]   -- مَدْرَسَةُ
def kabira : List SCell := Jumla.taNith [c 22 0, c 2 1, c 28 3, c 10 0]    -- كَبِيرَةُ

/-- الرَّجُلُ الطَّوِيلُ، رَجُلٌ طَوِيلٌ، رَجُلًا طَوِيلًا، الرَّجُلِ الطَّوِيلِ، مَدْرَسَةٌ كَبِيرَةٌ: مطابقةٌ في الأربعة؛
رَجُلٌ طَوِيلًا (إعراب)، رَجُلٌ الطَّوِيلُ (تعريف)، رَجُلٌ كَبِيرَةٌ (جنس)، رَجُلَانِ طَوِيلٌ (عدد) لا؛
الرَّجُلُ طَوِيلٌ خبرٌ لا نعت؛ وبعد رَجُلًا الجملةُ نعتٌ وبعد الرَّجُلَ حال. -/
theorem naat_witnesses :
    naatOk alrajul (naat alrajul tawil) = true ∧ naatOk rajulun (naat rajulun tawil) = true ∧
    naatOk rajulan (naat rajulan tawil) = true ∧ naatOk alrajuli (naat alrajuli tawil) = true ∧
    naatOk (Nawasikh.tanwin madrasa) (naat (Nawasikh.tanwin madrasa) kabira) = true ∧
    naatOk rajulun (Nawasikh.tanwin (Nawasikh.nasb tawil)) = false ∧
    naatOk rajulun (Marifa.al tawil) = false ∧
    naatOk rajulun (Nawasikh.tanwin kabira) = false ∧
    naatOk (Jumla.dual rajul) (Nawasikh.tanwin tawil) = false ∧
    hamlKind alrajul (Nawasikh.tanwin tawil) = .khabar ∧ hamlKind alrajul (naat alrajul tawil) = .naat ∧
    jumlaMahall rajulan = .naat ∧ jumlaMahall (Nawasikh.nasb alrajul) = .hal ∧
    jumlaMahall Jumla.darasa = .unread ∧ jumlaMahall [c 26 2, c 27 0] = .unread := by decide

end Slge.Naat
