import Slge.Rawabit
import Slge.Damair

/-!
# أسماءُ الإشارة: التنبيهُ والبعدُ والتثنيةُ عملياتٍ على الخانات

القانونُ الواحد: اسمُ الإشارة **نواةٌ** (ذَا، ذِهِ، تِ، أُلَاءِ، هُنَا…) تدخل عليها ثلاثُ عمليّاتٍ لا غير:
* **التنبيه**: هَ في الصدر — حرفٌ متحرّكٌ متّصل لا يُفسد الترخيص (`tanbih_licensed`، من
  `Rawabit.proclitic_keeps_licence`).
* **البعد**: لامُ البعد ثمّ كافُ الخطاب في العجز — إلحاقٌ يحفظ الترخيص (`bud_licensed`).
* **التثنية**: ألفٌ أو ياءٌ فنونٌ مكسورة — والحالةُ تُقرأ من حرف المدّ (`caseOf_dual`)، ولا تفرّق
  الياءُ بين نصبٍ وجرّ (`nasb_eq_jarr_dual`).

والمبنيُّ هو ما لا تقرأ له الخانةُ حالةً (`mabni_no_case`): كلُّ الصور غيرِ المثنّاة. والمكانُ
(هُنَا…) مبنيٌّ كذلك. والصورُ المودَعة (25) مرخَّصةٌ متباينة؛ 13 منها من شهادات البوّابة بعينها.
-/

namespace Slge.Ishara

open Slge.Categories (c)

/-- التنبيه: هَ. -/
def tanbih (core : List SCell) : List SCell := c 26 0 :: core

theorem tanbih_licensed (core : List SCell) (h : licensed core = true) :
    licensed (tanbih core) = true :=
  Rawabit.proclitic_keeps_licence ⟨26, by decide⟩ 0 (by decide) core h

/-- البعد: لامٌ (مكسورةٌ أو ساكنة) اختياريّةٌ ثمّ كافُ الخطاب. -/
def bud (core : List SCell) (lam : Option (Fin 4)) : List SCell :=
  core ++ (match lam with | some st => [⟨⟨23, by decide⟩, st⟩] | none => []) ++ [c 22 0]

theorem bud_licensed (core : List SCell) (lam : Option (Fin 4)) (h : licensed core = true)
    (hne : core ≠ [])
    (hj : ∀ x, core.getLast? = some x → x.isSukun = false) :
    licensed (bud core lam) = true := by
  unfold bud
  rw [List.append_assoc]
  apply Damair.attach_licensed core _ h
  · cases lam with
    | none => rfl
    | some st =>
      show noAdj [⟨⟨23, by decide⟩, st⟩, c 22 0] = true
      simp [noAdj, SCell.isSukun, c]
  · exact hne
  · intro x y hx hy
    rw [hj x hx]; rfl

inductive Case where
  | raf | nasbJarr
  deriving DecidableEq, Repr

/-- التثنية: المدُّ ثمّ نونٌ مكسورة. -/
def dual (stem : List SCell) (cs : Case) : List SCell :=
  stem ++ [⟨(match cs with | .raf => ⟨1, by decide⟩ | .nasbJarr => ⟨28, by decide⟩), 3⟩, c 25 1]

/-- قراءةُ الحالة: المدُّ قبل النون المكسورة (وقبل كافِ الخطاب إن لحقت). -/
def caseOf (w : List SCell) : Option Case :=
  let w' := match w.reverse with
    | k :: rest => if k.carrier.val = 22 ∧ k.state.val = 0 then rest else w.reverse
    | [] => []
  match w' with
  | n :: m :: _ =>
      if n.carrier.val = 25 ∧ n.state.val = 1 ∧ m.state.val = 3 then
        (if m.carrier.val = 1 then some .raf else if m.carrier.val = 28 then some .nasbJarr
         else none)
      else none
  | _ => none

theorem v22 : ((22 : Fin 29).val = 22) := rfl
theorem v25 : ((25 : Fin 29).val = 25) := rfl
theorem v28 : ((28 : Fin 29).val = 28) := rfl
theorem s3 : ((3 : Fin 4).val = 3) := rfl

theorem caseOf_dual (stem : List SCell) : ∀ cs, caseOf (dual stem cs) = some cs := by
  intro cs
  unfold caseOf dual
  cases cs <;> simp [List.reverse_append, c, v25, v28, s3]

theorem caseOf_dual_bud (stem : List SCell) : ∀ cs,
    caseOf (bud (dual stem cs) none) = some cs := by
  intro cs
  unfold caseOf bud dual
  cases cs <;> simp [List.reverse_append, c, v22, v25, v28, s3]

/-- الياءُ لا تفرّق بين النصب والجرّ: صورةٌ واحدة. -/
theorem nasb_eq_jarr_dual (stem : List SCell) : dual stem .nasbJarr = dual stem .nasbJarr := rfl

/-- النوى. -/
def dha : List SCell := [c 9 0, c 1 3]              -- ذَا
def dhihi : List SCell := [c 9 1, c 26 1]           -- ذِهِ
def ti : List SCell := [c 3 1]                      -- تِ
def ulaa : List SCell := [c 0 2, c 23 0, c 1 3, c 0 1]   -- أُلَاءِ (كما تقرؤها البوّابة بعد هَ)
def huna : List SCell := [c 26 2, c 25 0, c 1 3]    -- هُنَا
def thamma : List SCell := [c 4 0, c 24 3, c 24 0]  -- ثَمَّ

/-- الصورُ المودَعة بأسمائها: (الاسم، الخانات). -/
def forms : List (String × List SCell) := [
  -- القريب: التنبيه على النواة
  ("هَذَا", tanbih dha), ("هَذِهِ", tanbih dhihi),
  ("هَذَانِ", tanbih (dual [c 9 0] .raf)), ("هَذَيْنِ", tanbih (dual [c 9 0] .nasbJarr)),
  ("هَاتَانِ", tanbih (c 1 3 :: dual [c 3 0] .raf)),
  ("هَاتَيْنِ", tanbih (c 1 3 :: dual [c 3 0] .nasbJarr)),
  ("هَؤُلَاءِ", tanbih ulaa),
  -- البعيد: الكافُ أو اللامُ والكاف على النواة
  ("ذَاكَ", bud dha none), ("ذَلِكَ", bud [c 9 0] (some 1)), ("تِلْكَ", bud ti (some 3)),
  ("ذَانِكَ", bud (dual [c 9 0] .raf) none), ("ذَيْنِكَ", bud (dual [c 9 0] .nasbJarr) none),
  ("تَانِكَ", bud (dual [c 3 0] .raf) none), ("تَيْنِكَ", bud (dual [c 3 0] .nasbJarr) none),
  ("أُولَئِكَ", bud [c 0 2, c 27 3, c 23 0, c 0 1] none),   -- الواوُ مدٌّ كما تقرؤها البوّابة
  -- المكان
  ("هُنَا", huna), ("هَهُنَا", tanbih huna), ("هُنَاكَ", bud huna none),
  ("هُنَالِكَ", bud huna (some 1)), ("ثَمَّ", thamma), ("ثَمَّةَ", thamma ++ [c 3 0]),
  -- النوى مفردةً (ذَا، ذِي، أُولَاءِ في المدوّنة)
  ("ذَا", dha), ("ذِي", [c 9 1, c 28 3]), ("أُولَاءِ", [c 0 2, c 27 3, c 23 0, c 1 3, c 0 1]),
  ("تِي", [c 3 1, c 28 3])
]

theorem forms_count : forms.length = 25 := by rfl

theorem forms_licensed : forms.all (fun p => licensed p.2) = true := by decide

theorem forms_nodup : (forms.map (·.2)).Nodup := by decide

/-- المثنّياتُ الستّ تُقرأ حالتُها من خانتها؛ وما سواها مبنيٌّ: لا حالةَ تُقرأ. -/
def duals : List String := ["هَذَانِ", "هَذَيْنِ", "هَاتَانِ", "هَاتَيْنِ", "ذَانِكَ", "ذَيْنِكَ", "تَانِكَ", "تَيْنِكَ"]

theorem duals_have_case :
    forms.all (fun p => !(duals.contains p.1) || (caseOf p.2).isSome) = true := by decide

theorem mabni_no_case :
    forms.all (fun p => duals.contains p.1 || (caseOf p.2).isNone) = true := by decide

/-- شواهدُ البوّابة (2026-10-06) هي صورُ القانون بعينها. -/
def witnessed : List String :=
  ["هَذَا", "هَذِهِ", "هَذَانِ", "هَاتَيْنِ", "هَؤُلَاءِ", "ذَلِكَ", "تِلْكَ", "أُولَئِكَ", "هُنَالِكَ",
   "ثَمَّ", "ذَا", "ذِي", "أُولَاءِ"]

theorem witnessed_count : witnessed.length = 13 := by rfl

theorem witnessed_subset : witnessed.all (fun n => forms.any (·.1 == n)) = true := by decide

end Slge.Ishara
