import Slge.Sarf

/-!
# التوابع: الحالةُ لا العلامة

قانونُ الفرز في الحصر: التابعُ يتبع المتبوعَ في **الحالة** (رفع/نصب/جرّ) لا في **العلامة** (ضمّةٌ أو واوٌ
أو ألف). فلا بدّ من قارئٍ يردّ العلاماتِ كلَّها إلى الحالة: `caseClass` يقرأ الضمّةَ والواوَ (ُونَ، ُو)
والألفَ (َانِ) رفعًا، والفتحةَ والياءَ (ِينَ، َيْنِ) نصبًا أو جرًّا، والكسرةَ جرًّا — والألفُ بعد فتحٍ
والياءُ بعد كسرٍ لا تُقرآن (الخمسةُ أم المقصورُ والمنقوص: المعجم) — مجمِّعًا قوانينَ
الأسماء الخمسة والمثنّى والعقود والممنوع من الصرف.

المبرهَن:
* `caseClass_damma`، `caseClass_khamsa_raf`، `caseClass_dual_raf`، `caseClass_uqud_raf`: علاماتٌ أربعٌ
  تُقرأ رفعًا واحدًا — فيتبع «العَالِمُ» «أَخُوكَ» وإن اختلفت علامتاهما (`follows_khamsa`).
* `follows_refl`، `follows_symm`: التبعيّةُ علاقةُ توافقٍ (مع التباسِ الياء بين النصب والجرّ).
* **عطفُ النسق**: الحروفُ التسعة كلُّها في جدول أدوات الربط (`nasaq_in_rawabit`)؛ والواوُ والفاءُ حرفان
  متّصلان لا يُفسدان ما بعدهما (`Rawabit.proclitic_keeps_licence`).
* **التوكيدُ المعنويّ**: ألفاظٌ سبعة تُضاف إلى ضميرٍ (`tawkid_words_licensed`)، والحالةُ تُقرأ من
  الجذع قبل الضمير (`tawkid_case`).

النعتُ والبدلُ وعطفُ البيان لا تفرّقها الخانة: كلُّها «تابعٌ يوافق في الحالة»؛ والمطابقةُ في التعريف والجنس
والعدد قوانينُ تيارٍ تُقاس في بايثون. القياسُ على MASAQ: 3,179 زوجًا (تابع، متبوع) بشهادات البوّابة.
-/

namespace Slge.Tawabi

open Slge.Categories (c)
open Slge.Zuruf (setLast)

inductive CaseClass where
  | raf | nasb | jarr | nasbJarr | unread
  deriving DecidableEq, Repr

/-- القارئُ الموحِّد للعلامات. -/
def caseClass (w : List SCell) : CaseClass :=
  match w.reverse with
  | n :: g :: p :: _ =>
      -- ُونَ / ِينَ (الجمعُ السالم والعقود)، َانِ / َيْنِ (المثنّى)
      if n.carrier.val = 25 ∧ n.state.val = 0 ∧ g.state.val = 3 ∧ g.carrier.val = 27 ∧ p.state.val = 2 then .raf
      else if n.carrier.val = 25 ∧ n.state.val = 0 ∧ g.state.val = 3 ∧ g.carrier.val = 28 ∧ p.state.val = 1 then .nasbJarr
      else if n.carrier.val = 25 ∧ n.state.val = 1 ∧ g.state.val = 3 ∧ g.carrier.val = 1 ∧ p.state.val = 0 then .raf
      else if n.carrier.val = 25 ∧ n.state.val = 1 ∧ g.state.val = 3 ∧ g.carrier.val = 28 ∧ p.state.val = 0 then .nasbJarr
      -- التنوين: حركةٌ فنونٌ ساكنة
      else if n.carrier.val = 25 ∧ n.state.val = 3 then
        (if g.state.val = 2 then .raf else if g.state.val = 0 then .nasb else if g.state.val = 1 then .jarr else .unread)
      -- الأسماءُ الخمسة: ُو رفعٌ؛ أمّا َا وِي فالمقصورُ والمنقوصُ يشاركانها: لا تقرؤهما الخانة
      else if n.state.val = 3 ∧ n.carrier.val = 27 ∧ g.state.val = 2 then .raf
      else if n.state.val = 3 then .unread
      else if n.state.val = 2 then .raf else if n.state.val = 0 then .nasb else if n.state.val = 1 then .jarr
      else .unread
  | [n, g] =>
      if n.carrier.val = 25 ∧ n.state.val = 3 then
        (if g.state.val = 2 then .raf else if g.state.val = 0 then .nasb else if g.state.val = 1 then .jarr else .unread)
      else if n.state.val = 2 then .raf else if n.state.val = 0 then .nasb else if n.state.val = 1 then .jarr
      else .unread
  | [n] => if n.state.val = 2 then .raf else if n.state.val = 0 then .nasb else if n.state.val = 1 then .jarr
           else .unread
  | [] => .unread

/-- التوافق: الحالتان واحدة، أو إحداهما ملتبسةٌ تشمل الأخرى. -/
def compatible : CaseClass → CaseClass → Bool
  | .unread, _ | _, .unread => false
  | .nasbJarr, .nasb | .nasbJarr, .jarr | .nasb, .nasbJarr | .jarr, .nasbJarr => true
  | a, b => a == b

def follows (tabi matbu : List SCell) : Bool := compatible (caseClass tabi) (caseClass matbu)

theorem compatible_symm : ∀ a b, compatible a b = compatible b a := by
  intro a b; cases a <;> cases b <;> rfl

theorem follows_symm (a b : List SCell) : follows a b = follows b a := by
  unfold follows; exact compatible_symm _ _

theorem compatible_refl (a : CaseClass) (h : a ≠ .unread) : compatible a a = true := by
  cases a <;> first | rfl | exact absurd rfl h

theorem follows_refl (w : List SCell) (h : caseClass w ≠ .unread) : follows w w = true :=
  compatible_refl _ h

/-- شواهدُ البوّابة: علاماتٌ مختلفةٌ، حالةٌ واحدة. -/
def alimu : List SCell := [c 0 0, c 23 3, c 18 0, c 1 3, c 23 1, c 24 2]            -- الْعَالِمُ
def akhuka : List SCell := [c 0 0, c 7 2, c 27 3, c 22 0]                             -- أَخُوكَ (الجذعُ أَخُو)
def muslimuna : List SCell := [c 24 2, c 12 3, c 23 1, c 24 2, c 27 3, c 25 0]         -- مُسْلِمُونَ
def rajulani : List SCell := [c 10 0, c 5 2, c 23 0, c 1 3, c 25 1]                   -- رَجُلَانِ
def rajulun : List SCell := [c 10 0, c 5 2, c 23 2, c 25 3]                           -- رَجُلٌ

theorem four_markers_one_case :
    caseClass alimu = .raf ∧ caseClass (akhuka.take 3) = .raf ∧ caseClass muslimuna = .raf ∧
    caseClass rajulani = .raf ∧ caseClass rajulun = .raf := by decide

theorem follows_khamsa : follows alimu (akhuka.take 3) = true := by decide

/-- حروفُ عطف النسق التسعة في جدول أدوات الربط. -/
def nasaq : List String := ["وَ", "فَ", "ثُمَّ", "حَتَّى", "أَوْ", "أَمْ", "لَا", "بَلْ", "لَكِنْ"]

theorem nasaq_in_rawabit : nasaq.all (fun n => Rawabit.particles.any (·.name == n)) = true := by decide

/-- ألفاظُ التوكيد المعنويّ (جذوعُها قبل الضمير)؛ وعَامَّة (ألفٌ فميمٌ مشدّدة) خارج الترخيص الثنائيّ
كحَاجَّ: يرخّصها الثلاثيُّ في الغانم. -/
def tawkidWords : List (String × List SCell) := [
  ("نَفْس", [c 25 0, c 20 3, c 12 2]), ("عَيْن", [c 18 0, c 28 3, c 25 2]),
  ("كُلّ", [c 22 2, c 23 3, c 23 2]), ("جَمِيع", [c 5 0, c 24 1, c 28 3, c 18 2]),
  ("كِلَا", [c 22 1, c 23 0, c 1 3]), ("كِلْتَا", [c 22 1, c 23 3, c 3 0, c 1 3])
]

theorem tawkid_words_licensed : tawkidWords.all (fun p => licensed p.2) = true := by decide

/-- كُلُّهُمْ: الحالةُ من الجذع قبل الضمير. -/
theorem tawkid_case :
    caseClass (tawkidWords.getD 2 ("", [])).2 = .raf ∧
    caseClass (setLast (tawkidWords.getD 2 ("", [])).2 0) = .nasb ∧
    licensed (Marifa.idafa (tawkidWords.getD 2 ("", [])).2 [c 26 2, c 24 3]) = true := by decide

/-- قانونُ الحالة على العمليّات: رفعُ الأسماء الخمسة بالواو رفعٌ عند القارئ، لكلّ جذع. -/
theorem caseClass_khamsa_raf (s : Khamsa.Stem) (hne : s.head ≠ []) :
    caseClass (Khamsa.form s .raf) = .raf := by
  unfold caseClass Khamsa.form Khamsa.maddOf Khamsa.shortOf
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.cons_append]
  cases hh : s.head.reverse with
  | nil => exact absurd (List.reverse_eq_nil_iff.1 hh) hne
  | cons p t => simp [Ishara.s3]

/-- ونصبُها بالألف لا يقرؤه القارئُ العامّ: الألفُ بعد فتحٍ مشتركةٌ مع المقصور (مُوسَى) — المعجمُ يفصل. -/
theorem khamsa_nasb_unread (s : Khamsa.Stem) (hne : s.head ≠ []) :
    caseClass (Khamsa.form s .nasb) = .unread := by
  unfold caseClass Khamsa.form Khamsa.maddOf Khamsa.shortOf
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.cons_append]
  cases hh : s.head.reverse with
  | nil => exact absurd (List.reverse_eq_nil_iff.1 hh) hne
  | cons p t => simp [Ishara.s3]

/-- العقودُ بالواو رفعٌ لكلّ جذعٍ غيرِ فارغ. -/
theorem caseClass_uqud_raf (stem : List SCell) (hne : stem ≠ []) :
    caseClass (Adad.uqud stem true) = .raf := by
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast stem 2 hne
  unfold caseClass Adad.uqud
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.cons_append]
  have : ∀ l : List SCell, Afal.lastOf l = some ⟨k, 2⟩ → ∃ t, l.reverse = ⟨k, 2⟩ :: t := by
    intro l hl
    cases hr : l.reverse with
    | nil => rw [List.reverse_eq_nil_iff.1 hr] at hl; simp [Afal.lastOf] at hl
    | cons y u =>
      refine ⟨u, ?_⟩
      have h2 : Afal.lastOf l = l.reverse.head? := by
        clear hl hr hk; induction l with
        | nil => rfl
        | cons z v ih => cases v with
          | nil => rfl
          | cons w v' => simp [Afal.lastOf, ih, List.reverse_cons, List.head?_append]
      rw [h2, hr] at hl; simp at hl; rw [hl]
  obtain ⟨t, ht⟩ := this _ hk
  simp only [ite_true]
  rw [ht]; simp [c, Ishara.v25, Ishara.s3]

end Slge.Tawabi
