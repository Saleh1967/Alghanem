import Slge.Zuruf

/-!
# ظروفُ الزمان: التصرُّفُ عددُ الحالات، والبناءُ حالةٌ واحدة

**المتصرِّف** (يَوْم، شَهْر، لَيْل…) اسمٌ تجري عليه عمليّاتُ الظرف الثلاث (`Zuruf.mudaf/jarr/qat`)
وعمليّتا التنوين (`rafTanwin`، `nasbTanwin`): خمسُ صورٍ مرخَّصةٌ متباينة لكلّ جذع (`forms_nodup`)،
و**الخانةُ تفرّق** بين الضمّ المنوَّن (مرفوعٌ متصرّف: مبتدأٌ أو خبر) والضمّ العاري (مقطوعٌ عن الإضافة)
(`tanwin_vs_qat`، `hukm_rafTanwin`). والظرفيّةُ نفسُها (معنى «في») **ليست خانة**: الفتحُ يقرأ النصبَ
ولا يفرّق ظرفًا من مفعولٍ به — دَينٌ على النظم.

**المبنيُّ** (إِذْ، إِذَا، أَمْسِ، الْآنَ، مُذْ، مُنْذُ، قَطُّ، عَوْضُ) صورةٌ واحدةٌ بحالةٍ أخيرةٍ ثابتة
(`constants_states`) — فالتصرُّفُ عددُ الحالات في الخانة الأخيرة: ≥ 2 للمتصرّف، 1 للمبنيّ.
وأَمْسِ بأل العهديّة يصير معربًا: الْأَمْسُ = ال ++ (أَمْس بالضمّ) (`al_amsu`).

والمشتركةُ (قَبْل، بَعْد، بَيْن، عِنْد) في `Zuruf`؛ زمانٌ أم مكانٌ من المضاف إليه لا من الخانة.
-/

namespace Slge.Zaman

open Slge.Categories (c)
open Slge.Zuruf (setLast mudaf jarr qat)

/-- التنوين: حركةٌ فنونٌ ساكنة. -/
def rafTanwin (w : List SCell) : List SCell := setLast w 2 ++ [c 25 3]
def nasbTanwin (w : List SCell) : List SCell := setLast w 0 ++ [c 25 3]

theorem tanwin_vs_qat (w : List SCell) : rafTanwin w ≠ qat w := by
  intro h
  have := congrArg List.length h
  simp [rafTanwin, qat] at this

/-- قارئٌ يفرّق المنوَّنَ من المقطوع. -/
inductive Hukm where
  | marfu | mansub | majrur | maqtu | unread
  deriving DecidableEq, Repr

def hukm (w : List SCell) : Hukm :=
  match Afal.lastOf w with
  | some n =>
      if n.carrier.val = 25 ∧ n.state.val = 3 then
        (match Afal.lastOf (Afal.initOf w) with
         | some v => if v.state.val = 2 then .marfu else if v.state.val = 0 then .mansub
                     else if v.state.val = 1 then .majrur else .unread
         | none => .unread)
      else if n.state.val = 2 then .maqtu else if n.state.val = 0 then .mansub
      else if n.state.val = 1 then .majrur else .unread
  | none => .unread

theorem lastOf_append_singleton : ∀ (l : List SCell) (a : SCell), Afal.lastOf (l ++ [a]) = some a
  | [], _ => rfl
  | [_], _ => rfl
  | _ :: y :: t, a => by
    show Afal.lastOf (_ :: (y :: t ++ [a])) = some a
    simp only [List.cons_append, Afal.lastOf]; exact lastOf_append_singleton (y :: t) a

theorem initOf_append_singleton : ∀ (l : List SCell) (a : SCell), Afal.initOf (l ++ [a]) = l
  | [], _ => rfl
  | [_], _ => rfl
  | x :: y :: t, a => by
    show Afal.initOf (x :: (y :: t ++ [a])) = x :: y :: t
    simp only [List.cons_append, Afal.initOf]
    have := initOf_append_singleton (y :: t) a
    simp only [List.cons_append] at this
    rw [this]

theorem hukm_rafTanwin (w : List SCell) (hne : w ≠ []) : hukm (rafTanwin w) = .marfu := by
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast w 2 hne
  unfold hukm rafTanwin
  rw [lastOf_append_singleton, initOf_append_singleton, hk]
  simp [c, Ishara.v25, Ishara.s3]

theorem hukm_nasbTanwin (w : List SCell) (hne : w ≠ []) : hukm (nasbTanwin w) = .mansub := by
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast w 0 hne
  unfold hukm nasbTanwin
  rw [lastOf_append_singleton, initOf_append_singleton, hk]
  simp [c, Ishara.v25, Ishara.s3]

/-- الجذوعُ المتصرّفة الثمانية. -/
def stems : List (String × List SCell) := [
  ("يَوْم", [c 28 0, c 27 3, c 24 0]), ("شَهْر", [c 13 0, c 26 3, c 10 0]),
  ("سَنَة", [c 12 0, c 25 0, c 3 0]), ("عَام", [c 18 0, c 1 3, c 24 0]),
  ("لَيْل", [c 23 0, c 28 3, c 23 0]), ("نَهَار", [c 25 0, c 26 0, c 1 3, c 10 0]),
  ("صَبَاح", [c 14 0, c 2 0, c 1 3, c 6 0]), ("مَسَاء", [c 24 0, c 12 0, c 1 3, c 0 0])
]

/-- خمسُ صورٍ لكلّ جذع: مضاف، مجرور، مقطوع، مرفوعٌ منوَّن، منصوبٌ منوَّن. -/
def forms : List (List SCell) :=
  stems.flatMap fun p => [mudaf p.2, jarr p.2, qat p.2, rafTanwin p.2, nasbTanwin p.2]

theorem forms_count : forms.length = 40 := by rfl
theorem forms_licensed : forms.all licensed = true := by decide
theorem forms_nodup : forms.Nodup := by decide

theorem forms_hukm : stems.all (fun p => hukm (mudaf p.2) == .mansub && hukm (jarr p.2) == .majrur &&
    hukm (qat p.2) == .maqtu && hukm (rafTanwin p.2) == .marfu &&
    hukm (nasbTanwin p.2) == .mansub) = true := by decide

/-- المبنيّةُ الثمانية بحالاتها الأخيرة المعلَنة. -/
def constants : List (String × List SCell × Fin 4) := [
  ("إِذْ", [c 0 1, c 9 3], 3), ("إِذَا", [c 0 1, c 9 0, c 1 3], 3),
  ("أَمْسِ", [c 0 0, c 24 3, c 12 1], 1), ("الْآنَ", [c 0 0, c 23 3, c 0 0, c 1 3, c 25 0], 0),
  ("مُذْ", [c 24 2, c 9 3], 3), ("مُنْذُ", [c 24 2, c 25 3, c 9 2], 2),
  ("قَطُّ", [c 21 0, c 16 3, c 16 2], 2), ("عَوْضُ", [c 18 0, c 27 3, c 15 2], 2)
]

theorem constants_licensed : constants.all (fun p => licensed p.2.1) = true := by decide

theorem constants_states :
    constants.all (fun p => (Afal.lastOf p.2.1).map SCell.state == some p.2.2) = true := by decide

/-- أَمْسِ بأل العهديّة: معربٌ. -/
def amsStem : List SCell := [c 0 0, c 24 3, c 12 1]
theorem al_amsu : [c 0 0, c 23 3] ++ setLast amsStem 2 = [c 0 0, c 23 3, c 0 0, c 24 3, c 12 2] := by
  decide

end Slge.Zaman
