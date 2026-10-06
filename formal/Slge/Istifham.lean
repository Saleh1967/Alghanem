import Slge.Ishara

/-!
# أسماءُ الاستفهام: المعربُ الواحد، والتركيبُ على الخانات، وحذفُ ألف «ما» بعد الجارّ

المبرهَن:
* **أَيّ المعربُ الوحيد** (`ayy_differs_only_in_state`): صورُه الثلاث تختلف في حالة الخانة الأخيرة
  لا غير، والحالةُ تُقرأ منها (`caseOf_ayy`)؛ وسائرُ الأسماء صورةٌ واحدة (`mabni_single_form`).
* **التركيب**: مَاذَا = مَا ++ ذَا بعينها (`madha_is_ma_dha`)، ومَنْ ذَا وصلُ كلمتين مرخَّص
  (`man_dha_junction`)، وأَمَّنْ = أَمْ ++ مَنْ (`amman_is_am_man`).
* **«ما» بعد الجارّ تحذف ألفَها**: بِمَ، لِمَ، فِيمَ = الجارُّ ++ [مَ] (`ma_after_jarr`)؛ وعَمَّ ومِمَّ
  كذلك ثمّ تُدغَم نونُ الجارّ في الميم (`amma_is_an_ma_idgham`، `mimma_is_min_ma_idgham`) —
  عمليّةُ الإدغام دالّةٌ على الخانات (`idghamNM`).
* الحرفان: الهمزةُ حرفٌ متّصل لا يُفسد الترخيص (`hamza_prefix_licensed`)، وهَلْ كلمة.
* الصورُ المودَعة (22) مرخَّصةٌ متباينة، 21 منها شواهدُ البوّابة بعينها.

**الصدارة** قانونُ تيارٍ لا خانة: يُقاس في بايثون على MASAQ ولا يُبرهَن هنا.
-/

namespace Slge.Istifham

open Slge.Categories (c)

/-- أَيّ: ءَ يْ يَ/يُ/يِ. -/
def ayy (st : Fin 4) : List SCell := [c 0 0, c 28 3, ⟨⟨28, by decide⟩, st⟩]

def caseOf (w : List SCell) : Option (Fin 4) := (w.getLast?).map SCell.state

theorem caseOf_ayy (st : Fin 4) : caseOf (ayy st) = some st := by simp [caseOf, ayy]

theorem ayy_differs_only_in_state (a b : Fin 4) :
    (ayy a).dropLast = (ayy b).dropLast := by simp [ayy]

/-- الإدغام: نونٌ ساكنةٌ قبل ميمٍ تصير ميمًا ساكنة. -/
def idghamNM : List SCell → List SCell
  | x :: m :: t =>
      if x.carrier.val = 25 ∧ x.state.val = 3 ∧ m.carrier.val = 24 then c 24 3 :: m :: t
      else x :: idghamNM (m :: t)
  | w => w

/-- «ما» بعد الجارّ: ميمٌ مفتوحةٌ بلا ألف. -/
def maJarr : List SCell := [c 24 0]

def ma : List SCell := [c 24 0, c 1 3]
def man : List SCell := [c 24 0, c 25 3]
def dha : List SCell := Ishara.dha
def am : List SCell := [c 0 0, c 24 3]
def an : List SCell := [c 18 0, c 25 3]
def min : List SCell := [c 24 1, c 25 3]
def bi : List SCell := [c 2 1]
def li : List SCell := [c 23 1]
def fi : List SCell := [c 20 1, c 28 3]

theorem madha_is_ma_dha : ma ++ dha = [c 24 0, c 1 3, c 9 0, c 1 3] := by rfl

theorem man_dha_junction : licensed (man ++ dha) = true := by decide

theorem amman_is_am_man : am ++ man = [c 0 0, c 24 3, c 24 0, c 25 3] := by rfl

theorem ma_after_jarr :
    bi ++ maJarr = [c 2 1, c 24 0] ∧ li ++ maJarr = [c 23 1, c 24 0] ∧
    fi ++ maJarr = [c 20 1, c 28 3, c 24 0] := by refine ⟨rfl, rfl, rfl⟩

theorem amma_is_an_ma_idgham : idghamNM (an ++ maJarr) = [c 18 0, c 24 3, c 24 0] := by decide

theorem mimma_is_min_ma_idgham : idghamNM (min ++ maJarr) = [c 24 1, c 24 3, c 24 0] := by decide

/-- الإدغامُ لا يغيّر الطول. -/
theorem idghamNM_length : ∀ w : List SCell, (idghamNM w).length = w.length
  | [] => rfl
  | [_] => rfl
  | x :: m :: t => by
    show (if x.carrier.val = 25 ∧ x.state.val = 3 ∧ m.carrier.val = 24 then c 24 3 :: m :: t
          else x :: idghamNM (m :: t)).length = (x :: m :: t).length
    split
    · rfl
    · simp [idghamNM_length (m :: t)]

theorem hamza_prefix_licensed (w : List SCell) (h : licensed w = true) :
    licensed (c 0 0 :: w) = true :=
  Rawabit.proclitic_keeps_licence ⟨0, by decide⟩ 0 (by decide) w h

/-- الصورُ المودَعة بأسمائها. -/
def forms : List (String × List SCell) := [
  ("مَنْ", man), ("مَا", ma), ("مَتَى", [c 24 0, c 3 0, c 1 3]),
  ("أَيَّانَ", [c 0 0, c 28 3, c 28 0, c 1 3, c 25 0]), ("أَيْنَ", [c 0 0, c 28 3, c 25 0]),
  ("كَيْفَ", [c 22 0, c 28 3, c 20 0]), ("كَمْ", [c 22 0, c 24 3]),
  ("أَنَّى", [c 0 0, c 25 3, c 25 0, c 1 3]),
  ("أَيُّ", ayy 2), ("أَيَّ", ayy 0), ("أَيِّ", ayy 1),
  ("مَاذَا", ma ++ dha), ("مَنْ ذَا", man ++ dha), ("أَمَّنْ", am ++ man),
  ("هَلْ", [c 26 0, c 23 3]), ("أَ", [c 0 0]),
  ("بِمَ", bi ++ maJarr), ("لِمَ", li ++ maJarr), ("فِيمَ", fi ++ maJarr),
  ("عَمَّ", idghamNM (an ++ maJarr)), ("مِمَّ", idghamNM (min ++ maJarr)),
  ("لِأَيِّ", li ++ ayy 1)
]

theorem forms_count : forms.length = 22 := by rfl
theorem forms_licensed : forms.all (fun p => licensed p.2) = true := by decide
theorem forms_nodup : (forms.map (·.2)).Nodup := by decide

/-- المبنيّات: صورةٌ واحدةٌ لكلٍّ (لا تظهر عليها حالات). -/
def mabni : List String := ["مَنْ", "مَا", "مَتَى", "أَيَّانَ", "أَيْنَ", "كَيْفَ", "كَمْ", "أَنَّى"]

theorem mabni_single_form : mabni.all (fun n => (forms.filter (·.1 == n)).length == 1) = true := by
  decide

/-- والمعربُ أَيّ له ثلاث. -/
theorem ayy_three_forms :
    (forms.filter (fun p => p.2.dropLast == (ayy 0).dropLast ∧
      (p.2.getLast?.map (·.carrier.val)) == some 28)).length = 3 := by
  decide

end Slge.Istifham
