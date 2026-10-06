import Slge.Istifham

/-!
# النداء: الأداةُ حرفٌ، والمنادى يُقرأ حكمُه من خانته الأخيرة

**الأدوات** ستٌّ (أَ، أَيْ، أَيَا، هَيَا، يَا، وَا): حروفٌ مرخَّصةٌ متباينة؛ والهمزةُ حرفٌ متّصل
(`Istifham.hamza_prefix_licensed`)، ويَا تنتهي بألفٍ ساكنة فوصلُها بكلّ مرخَّصٍ مرخَّص
(`ya_junction`).

**قانونُ المنادى** على الخانة الأخيرة من جذعه (قبل الضمير المتّصل إن لحق): ضمٌّ بلا تنوين ⇒ **مبنيٌّ
على الضمّ في محلّ نصب** (علمٌ أو نكرةٌ مقصودة)؛ فتحٌ ⇒ **معربٌ منصوب** (مضافٌ أو شبيهٌ به)؛ فتحٌ
بتنوين ⇒ نكرةٌ غيرُ مقصودة؛ كسرٌ ⇒ مضافٌ إلى ياءٍ محذوفة (يَا قَوْمِ). والمثنّى والجمعُ السالم:
مبنيٌّ على الألف أو الواو. والمبرهَن: التنوينُ لا يجامع البناء (`tanwin_never_bina`)، والضمُّ
بلا تنوينٍ بناءٌ أبدًا (`damm_is_bina`)، والقراءةُ دالّة (`hukm`).

**الندبة** (وَا حَسْرَتَاهْ): ألفٌ فهاءُ سكتٍ ساكنتان — غيرُ مرخَّصةٍ ثنائيًّا لكلّ جذع
(`nudba_not_binary_licensed`): صورةُ وقفٍ تُرخَّص بالثلاثيّ في الغانم (`A116.Ternary`)، لا هنا.

القياسُ على MASAQ (489 منادًى بشهادات البوّابة) في بايثون: الضمُّ ⇒ مبنيّ 188/188؛ الفتحُ والكسرُ
⇒ معربٌ مضاف 195/237؛ والمنتهي بألفٍ أو ياء (مُوسَى، بَنِي) لا تقرؤه الخانة: 63.
-/

namespace Slge.Nida

open Slge.Categories (c)

inductive Hukm where
  | mabniDamm | mabniAlif | mabniWaw | mansub | nakiraGhayrMaqsuda | mudafIlaYa | unread
  deriving DecidableEq, Repr

/-- التنوين كما تُخرجه البوّابة: حركةٌ فنونٌ ساكنة في الآخر. -/
def hasTanwin (w : List SCell) : Bool :=
  match w.reverse with
  | n :: v :: _ => n.carrier.val == 25 && n.state.val == 3 && v.state.val != 3
  | _ => false

/-- الحكمُ من الخانة الأخيرة للجذع. -/
def hukm (stem : List SCell) : Hukm :=
  if hasTanwin stem then
    (match stem.reverse with
     | _ :: v :: _ => if v.state.val = 0 then .nakiraGhayrMaqsuda else .unread
     | _ => .unread)
  else match stem.reverse with
    | n :: g :: _ =>
        if n.carrier.val = 25 ∧ n.state.val = 0 ∧ g.carrier.val = 27 ∧ g.state.val = 3 then .mabniWaw
        else if n.carrier.val = 25 ∧ n.state.val = 1 ∧ g.carrier.val = 1 ∧ g.state.val = 3 then .mabniAlif
        else if n.state.val = 2 then .mabniDamm
        else if n.state.val = 0 then .mansub
        else if n.state.val = 1 then .mudafIlaYa
        else .unread
    | [n] => if n.state.val = 2 then .mabniDamm else if n.state.val = 0 then .mansub
             else if n.state.val = 1 then .mudafIlaYa else .unread
    | [] => .unread

def IsBina : Hukm → Bool
  | .mabniDamm | .mabniAlif | .mabniWaw => true
  | _ => false

/-- التنوينُ لا يجامع البناء. -/
theorem tanwin_never_bina (stem : List SCell) (h : hasTanwin stem = true) :
    IsBina (hukm stem) = false := by
  unfold hukm; rw [h]; simp only [ite_true]
  split <;> (try split) <;> rfl

/-- الضمُّ في الآخر بلا تنوينٍ بناءٌ أبدًا (ما لم يكن قبله واوٌ ساكنةٌ فنون: جمعٌ سالم). -/
theorem damm_is_bina (stem : List SCell) (k : Fin 29) (hk : k.val ≠ 25) :
    IsBina (hukm (stem ++ [(⟨k, 2⟩ : SCell)])) = true := by
  have hr : (stem ++ [(⟨k, 2⟩ : SCell)]).reverse = (⟨k, 2⟩ : SCell) :: stem.reverse := by simp
  have ht : hasTanwin (stem ++ [(⟨k, 2⟩ : SCell)]) = false := by
    unfold hasTanwin; rw [hr]
    generalize stem.reverse = r
    cases r with
    | nil => rfl
    | cons y l => simp
  unfold hukm; rw [ht]; simp only [Bool.false_eq_true, ite_false]; rw [hr]
  generalize stem.reverse = r
  cases r with
  | nil => rfl
  | cons y l => simp [hk, IsBina]

/-- يَا: ياءٌ مفتوحةٌ فألفٌ ساكنة؛ وصلُها بكلّ مرخَّصٍ مرخَّص. -/
def ya : List SCell := [c 28 0, c 1 3]

theorem ya_junction (w : List SCell) (hw : licensed w = true) : licensed (ya ++ w) = true := by
  cases w with
  | nil => rfl
  | cons x t =>
    simp only [licensed, Bool.and_eq_true] at hw
    have h1 : x.state.val ≠ 3 := by
      intro h3
      have : x.isSukun = true := by simp [SCell.isSukun, h3]
      rw [this] at hw; exact absurd hw.1 (by decide)
    show (!(c 28 0).isSukun && noAdj (c 28 0 :: c 1 3 :: x :: t)) = true
    simp [noAdj, SCell.isSukun, c, h1, hw.2]

/-- الندبة: ألفٌ فهاءُ سكتٍ ساكنتان — ساكنان متجاوران، فلا ترخيصَ ثنائيًّا. -/
def nudba (stem : List SCell) : List SCell := stem ++ [c 1 3, c 26 3]

theorem noAdj_two_sukun : ∀ l : List SCell, noAdj (l ++ [c 1 3, c 26 3]) = false
  | [] => rfl
  | [x] => by simp [noAdj, c, SCell.isSukun, Ishara.s3]
  | x :: y :: t => by
    simp only [List.cons_append, noAdj, Bool.and_eq_false_iff]
    exact Or.inr (noAdj_two_sukun (y :: t))

theorem nudba_not_binary_licensed (stem : List SCell) : licensed (nudba stem) = false := by
  unfold nudba
  cases stem with
  | nil => rfl
  | cons x t =>
    simp only [List.cons_append, licensed, Bool.and_eq_false_iff]
    exact Or.inr (noAdj_two_sukun (x :: t))

/-- الأدواتُ الستّ. -/
def particles : List (String × List SCell) := [
  ("أَ", [c 0 0]), ("أَيْ", [c 0 0, c 28 3]), ("أَيَا", [c 0 0, c 28 0, c 1 3]),
  ("هَيَا", [c 26 0, c 28 0, c 1 3]), ("يَا", ya), ("وَا", [c 27 0, c 1 3])
]

theorem particles_licensed : particles.all (fun p => licensed p.2) = true := by decide
theorem particles_nodup : (particles.map (·.2)).Nodup := by decide
theorem particles_count : particles.length = 6 := by rfl

/-- شواهدُ من البوّابة بأحكامها المقروءة. -/
def witnesses : List (String × List SCell × Hukm) := [
  ("آدَمُ", [c 0 0, c 1 3, c 8 0, c 24 2], .mabniDamm),
  ("إِبْرَاهِيمُ", [c 0 1, c 2 3, c 10 0, c 1 3, c 26 1, c 28 3, c 24 2], .mabniDamm),
  ("مَعْشَرَ", [c 24 0, c 18 3, c 13 0, c 10 0], .mansub),
  ("قَوْمِ", [c 21 0, c 27 3, c 24 1], .mudafIlaYa),
  ("أَبَتِ", [c 0 0, c 2 0, c 3 1], .mudafIlaYa),
  ("مُوسَى", [c 24 2, c 27 3, c 12 0, c 1 3], .unread)
]

theorem witnesses_hukm : witnesses.all (fun w => hukm w.2.1 == w.2.2) = true := by decide

end Slge.Nida
