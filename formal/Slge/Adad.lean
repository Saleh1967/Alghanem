import Slge.Zaman

/-!
# العدد: المخالفةُ تاءٌ، والتركيبُ فتحٌ، والعقودُ واوٌ وياء

* **المخالفة (3–10)**: صورةُ المذكّر = جذعٌ مفتوحُ الآخر + تاءٌ بحركة الإعراب؛ وصورةُ المؤنّث = الجذعُ
  بحركة الإعراب. فالفرقُ **خانةُ تاءٍ واحدة** (`fem_is_masc_without_ta`)، والقارئُ يستخرج جنسَ
  المعدود من التاء بعد فتحة الجذع (`genderOf`؛ وسِتُّ تاؤها أصلٌ بعد ساكن: `six_ta_is_radical`). و«عشرة» المفردةُ تخالف كأخواتها (`ten_single_opposes`).
* **التركيب (11–19)**: الجزءان مفتوحا الآخر (`compound_both_fatha`)؛ و«عشر» المركّبةُ تطابق المعدود:
  عَشَرَ للمذكّر وعَشْرَةَ للمؤنّث، وشينُها مفتوحةٌ للمذكّر ساكنةٌ للمؤنّث (`shin_law`).
* **اثنا عشر**: الجزءُ الأوّل مثنًّى يُقرأ إعرابُه من مدّه (ا رفعٌ، ي نصبٌ/جرّ) (`twelve_case`).
* **العقود (20–90)**: ملحقةٌ بجمع المذكّر السالم: ُونَ رفعٌ، ِينَ نصبٌ/جرّ (`uqud_case`)، والحركةُ قبل
  المدّ من جنسه (قانونُ الأسماء الخمسة).
* **الحياد**: مِائَة وأَلْف صورةٌ واحدةٌ للجنسين (معلن؛ لا تاءَ تُقرأ).
* **التمييز**: حالةُ المعدود دالّةٌ في مدى العدد (`tamyizState`): 3–10 جمعٌ مجرور، 11–99 مفردٌ منصوبٌ
  منوَّن، 100 و1000 مفردٌ مجرور — ويُقاس في بايثون على MASAQ.

الصورُ المودَعة مرخَّصةٌ ومتباينة (`forms_licensed`، `forms_nodup`).
-/

namespace Slge.Adad

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-- جذوعُ 3–10 بلا حالةٍ أخيرة (الحرفُ الأخير بفتحةٍ مؤقّتة). -/
def stems : List (Nat × List SCell) := [
  (3, [c 4 0, c 23 0, c 1 3, c 4 0]), (4, [c 0 0, c 10 3, c 2 0, c 18 0]),
  (5, [c 7 0, c 24 3, c 12 0]), (6, [c 12 1, c 3 3, c 3 0]),
  (7, [c 12 0, c 2 3, c 18 0]), (8, [c 4 0, c 24 0, c 1 3, c 25 1, c 28 0]),
  (9, [c 3 1, c 12 3, c 18 0]), (10, [c 18 0, c 13 3, c 10 0])
]

/-- صورةُ المذكّر: الجذعُ مفتوحًا + تاءٌ بحركة الإعراب. -/
def masc (stem : List SCell) (cs : Fin 4) : List SCell := setLast stem 0 ++ [⟨⟨3, by decide⟩, cs⟩]

/-- صورةُ المؤنّث: الجذعُ بحركة الإعراب. -/
def fem (stem : List SCell) (cs : Fin 4) : List SCell := setLast stem cs

theorem setLast_setLast : ∀ (w : List SCell) (a b : Fin 4), setLast (setLast w a) b = setLast w b
  | [], _, _ => rfl
  | [_], _, _ => rfl
  | x :: y :: t, a, b => by
    cases t with
    | nil => rfl
    | cons z u =>
      show x :: setLast (y :: setLast (z :: u) a) b = x :: y :: setLast (z :: u) b
      have ih := setLast_setLast (y :: z :: u) a b
      simpa [setLast] using ih

theorem fem_is_masc_without_ta (stem : List SCell) (cs : Fin 4) :
    fem stem cs = setLast (masc stem cs).dropLast cs := by
  simp [fem, masc, setLast_setLast]

/-- جنسُ المعدود من التاء: تاءٌ في الآخر بعد فتحةِ الجذع ⇒ مذكّر، وإلّا مؤنّث (سِتُّ: تاؤها أصلٌ
بعد ساكن). -/
def genderOf (w : List SCell) : Bool :=
  match Afal.lastOf w, Afal.lastOf (Afal.initOf w) with
  | some x, some p => x.carrier.val == 3 && p.state.val == 0
  | _, _ => false

theorem genderOf_masc (stem : List SCell) (cs : Fin 4) (hne : stem ≠ []) :
    genderOf (masc stem cs) = true := by
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast stem 0 hne
  unfold genderOf masc
  rw [Zaman.lastOf_append_singleton, Zaman.initOf_append_singleton, hk]; rfl

/-- صورُ المؤنّث المودَعة كلُّها تُقرأ مؤنّثةً — ومنها سِتُّ بتائها الأصليّة. -/
theorem genderOf_fem_forms :
    stems.all (fun p => !genderOf (fem p.2 2) && !genderOf (fem p.2 0) && !genderOf (fem p.2 1)) =
      true := by decide

/-- عَشَرَ المركّبة للمذكّر، وعَشْرَةَ للمؤنّث: الشينُ مفتوحةٌ أو ساكنة. -/
def tenMasc : List SCell := [c 18 0, c 13 0, c 10 0]
def tenFem : List SCell := [c 18 0, c 13 3, c 10 0, c 3 0]

theorem shin_law : (tenMasc.getD 1 (c 0 0)).state.val = 0 ∧ (tenFem.getD 1 (c 0 0)).state.val = 3 := by
  decide

/-- التركيب: الجزءُ الأوّل مفتوحًا + عَشَر مطابِقةً. -/
def compound (unit : List SCell) (masculine : Bool) : List SCell :=
  setLast unit 0 ++ (if masculine then tenMasc else tenFem)

theorem compound_both_fatha (unit : List SCell) (m : Bool) (hne : unit ≠ []) :
    (∃ k, Afal.lastOf (setLast unit 0) = some ⟨k, 0⟩) ∧
    (Afal.lastOf (compound unit m)).map SCell.state = some 0 := by
  refine ⟨Zuruf.lastOf_setLast unit 0 hne, ?_⟩
  unfold compound
  cases m with
  | true =>
    rw [show setLast unit 0 ++ (if true = true then tenMasc else tenFem) =
      (setLast unit 0 ++ [c 18 0, c 13 0]) ++ [c 10 0] by simp [tenMasc]]
    rw [Zaman.lastOf_append_singleton]; rfl
  | false =>
    rw [show setLast unit 0 ++ (if false = true then tenMasc else tenFem) =
      (setLast unit 0 ++ [c 18 0, c 13 3, c 10 0]) ++ [c 3 0] by simp [tenFem]]
    rw [Zaman.lastOf_append_singleton]; rfl

/-- اثنا عَشَرَ: الجزءُ الأوّل مثنًّى بلا نون؛ إعرابُه من مدّه. -/
def twelve (raf : Bool) (masculine : Bool) : List SCell :=
  (if masculine then [c 0 1, c 4 3, c 25 0] else [c 0 1, c 4 3, c 25 0, c 3 0]) ++
  [⟨if raf then ⟨1, by decide⟩ else ⟨28, by decide⟩, 3⟩] ++ (if masculine then tenMasc else tenFem)

def twelveCase (w : List SCell) : Option Bool :=
  let n := if genderOf w then 4 else 3   -- طولُ عَشْرَةَ أو عَشَرَ
  match (w.take (w.length - n)).reverse with
  | g :: _ => if g.carrier.val = 1 ∧ g.state.val = 3 then some true
              else if g.carrier.val = 28 ∧ g.state.val = 3 then some false else none
  | [] => none

theorem twelve_case : ∀ r m, twelveCase (twelve r m) = some r := by decide

/-- العقود: ُونَ للرفع، ِينَ للنصب والجرّ. -/
def uqud (stem : List SCell) (raf : Bool) : List SCell :=
  setLast stem (if raf then 2 else 1) ++
    [⟨if raf then ⟨27, by decide⟩ else ⟨28, by decide⟩, 3⟩, c 25 0]

def uqudCase (w : List SCell) : Option Bool :=
  match w.reverse with
  | n :: g :: _ =>
      if n.carrier.val = 25 ∧ n.state.val = 0 ∧ g.state.val = 3 then
        (if g.carrier.val = 27 then some true else if g.carrier.val = 28 then some false else none)
      else none
  | _ => none

theorem v27 : ((27 : Fin 29).val = 27) := rfl

theorem uqud_case (stem : List SCell) (r : Bool) : uqudCase (uqud stem r) = some r := by
  unfold uqudCase uqud
  cases r <;> simp [List.reverse_append, c, Ishara.v25, Ishara.v28, Ishara.s3, v27]

/-- حالةُ المعدود دالّةٌ في مدى العدد: (الحالة، منوَّن؟، جمع؟). -/
def tamyizState (n : Nat) : Fin 4 × Bool × Bool :=
  if 3 ≤ n ∧ n ≤ 10 then (1, false, true)
  else if 11 ≤ n ∧ n ≤ 99 then (0, true, false)
  else if n = 100 ∨ n = 1000 then (1, false, false)
  else (0, false, false)

theorem tamyiz_ranges : tamyizState 7 = (1, false, true) ∧ tamyizState 11 = (0, true, false) ∧
    tamyizState 40 = (0, true, false) ∧ tamyizState 100 = (1, false, false) := by decide

/-- الصورُ المودَعة: لكلّ جذعٍ (3–10) مذكّرٌ ومؤنّث بالحالات الثلاث، والعقودُ الثمانية بصورتيها،
واثنا عشر بأربعه. -/
def uqudStems : List (List SCell) := [
  [c 18 1, c 13 3, c 10 0], [c 4 0, c 23 0, c 1 3, c 4 0], [c 0 0, c 10 3, c 2 0, c 18 0],
  [c 7 0, c 24 3, c 12 0], [c 12 1, c 3 3, c 3 0], [c 12 0, c 2 3, c 18 0],
  [c 4 0, c 24 0, c 1 3, c 25 0], [c 3 1, c 12 3, c 18 0]
]

def forms : List (List SCell) :=
  (stems.flatMap fun p => [masc p.2 2, masc p.2 0, masc p.2 1, fem p.2 2, fem p.2 0, fem p.2 1]) ++
  (uqudStems.flatMap fun s => [uqud s true, uqud s false]) ++
  [twelve true true, twelve false true, twelve true false, twelve false false] ++
  (stems.flatMap fun p => if p.1 ≤ 9 then [compound p.2 true, compound p.2 false] else [])

theorem forms_count : forms.length = 82 := by rfl
theorem forms_licensed : forms.all licensed = true := by decide
theorem forms_nodup : forms.Nodup := by decide

theorem ten_single_opposes : genderOf (masc (stems.getD 7 (0, [])).2 2) = true ∧
    genderOf (fem (stems.getD 7 (0, [])).2 2) = false := by decide

theorem six_ta_is_radical : genderOf (fem (stems.getD 3 (0, [])).2 2) = false ∧
    genderOf (masc (stems.getD 3 (0, [])).2 2) = true := by decide

end Slge.Adad
