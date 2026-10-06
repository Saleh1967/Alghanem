import Slge.Nida

/-!
# ظروفُ المكان: الإضافةُ والقطعُ والجرُّ في الخانة الأخيرة

الظرفُ المعربُ **جذعٌ** وخانةُ إعرابٍ في آخره تقرأ ثلاثةَ أحوال (`hukm`):
* **فتحٌ** ⇒ منصوبٌ على الظرفيّة مضافًا (فَوْقَ الأرضِ)؛
* **كسرٌ** ⇒ مجرورٌ بالجارّ مضافًا (مِن فَوْقِ)، أو مضافٌ إلى ياء المتكلّم (عِنْدِي)؛
* **ضمٌّ** ⇒ **مقطوعٌ عن الإضافة** مبنيًّا على الضمّ (مِن قَبْلُ وَمِن بَعْدُ).

والقطعُ **عمليّةٌ** على الخانة الأخيرة (`qat`: الفتحُ يصير ضمًّا) تحفظ الترخيص (`setLast_licensed`)،
والحكمُ يقرؤها (`hukm_qat`، `hukm_mudaf`، `hukm_jarr`). والمبنيّاتُ ثوابتُ صورةٍ واحدة: حَيْثُ
(ضمٌّ لازم: مقطوعٌ أبدًا)، لَدُنْ، لَدَى، ثَمَّ، هُنَا (`constants_single`). والمختصُّ (المسجد، البيت)
ليس ظرفًا: قيدٌ معجميٌّ لا خانة.

القياسُ على MASAQ (1,493 ظرفًا بشهادات البوّابة) في بايثون: الضمُّ ⇒ غيرُ مضاف 82/82 (وحَيْثُ
ثابت)، الفتحُ ⇒ مضاف 752/756، الكسرُ ⇒ بعد جارٍّ أو ياءِ المتكلّم 568/584.
-/

namespace Slge.Zuruf

open Slge.Categories (c)

inductive Hukm where
  | mansubMudaf | majrur | maqtu | mabni | unread
  deriving DecidableEq, Repr

def hukm (w : List SCell) : Hukm :=
  match Afal.lastOf w with
  | some x => if x.state.val = 0 then .mansubMudaf else if x.state.val = 1 then .majrur
              else if x.state.val = 2 then .maqtu else .unread
  | none => .unread

/-- تغييرُ حالة الخانة الأخيرة. -/
def setLast : List SCell → Fin 4 → List SCell
  | [], _ => []
  | [x], st => [⟨x.carrier, st⟩]
  | x :: y :: t, st => x :: setLast (y :: t) st

/-- القطعُ عن الإضافة: ضمٌّ في الآخر. -/
def qat (w : List SCell) : List SCell := setLast w 2
def jarr (w : List SCell) : List SCell := setLast w 1
def mudaf (w : List SCell) : List SCell := setLast w 0

theorem lastOf_setLast : ∀ (w : List SCell) (st : Fin 4), w ≠ [] →
    ∃ k, Afal.lastOf (setLast w st) = some ⟨k, st⟩
  | [], _, h => absurd rfl h
  | [x], st, _ => ⟨x.carrier, rfl⟩
  | x :: y :: t, st, _ => by
    show ∃ k, Afal.lastOf (x :: setLast (y :: t) st) = some ⟨k, st⟩
    obtain ⟨k, hk⟩ := lastOf_setLast (y :: t) st (by simp)
    refine ⟨k, ?_⟩
    cases h : setLast (y :: t) st with
    | nil => rw [h] at hk; exact absurd hk (by simp [Afal.lastOf])
    | cons z u => rw [h] at hk; simpa [Afal.lastOf] using hk

theorem hukm_qat (w : List SCell) (hne : w ≠ []) : hukm (qat w) = .maqtu := by
  obtain ⟨k, hk⟩ := lastOf_setLast w 2 hne
  unfold hukm qat; rw [hk]; rfl

theorem hukm_mudaf (w : List SCell) (hne : w ≠ []) : hukm (mudaf w) = .mansubMudaf := by
  obtain ⟨k, hk⟩ := lastOf_setLast w 0 hne
  unfold hukm mudaf; rw [hk]; rfl

theorem hukm_jarr (w : List SCell) (hne : w ≠ []) : hukm (jarr w) = .majrur := by
  obtain ⟨k, hk⟩ := lastOf_setLast w 1 hne
  unfold hukm jarr; rw [hk]; rfl

/-- حالاتُ السكون لا تتغيّر بتبديل حركةٍ بحركة، فالترخيصُ محفوظ. -/
theorem map_isSukun_setLast : ∀ (w : List SCell) (st : Fin 4), st.val ≠ 3 →
    (∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) →
    (setLast w st).map SCell.isSukun = w.map SCell.isSukun
  | [], _, _, _ => rfl
  | [x], st, hst, hlast => by
    have h1 := hlast x rfl
    have e1 : (st.val == 3) = false := by simpa using hst
    have e2 : (x.state.val == 3) = false := by simpa using h1
    simp [setLast, SCell.isSukun, e1, e2]
  | x :: y :: t, st, hst, hlast => by
    show (x :: setLast (y :: t) st).map SCell.isSukun = (x :: y :: t).map SCell.isSukun
    rw [List.map_cons, List.map_cons,
      map_isSukun_setLast (y :: t) st hst (fun z hz => hlast z (by simpa [Afal.lastOf] using hz))]

theorem licensed_of_map_isSukun (v w : List SCell) (h : v.map SCell.isSukun = w.map SCell.isSukun) :
    licensed v = licensed w := by
  have hn : ∀ (a b : List SCell), a.map SCell.isSukun = b.map SCell.isSukun → noAdj a = noAdj b := by
    intro a
    induction a with
    | nil => intro b hb; cases b <;> simp_all [noAdj]
    | cons x t ih =>
      intro b hb
      cases b with
      | nil => simp at hb
      | cons y u =>
        simp only [List.map_cons, List.cons.injEq] at hb
        cases t with
        | nil => cases u with
          | nil => rfl
          | cons _ _ => simp at hb
        | cons z t' => cases u with
          | nil => simp at hb
          | cons w' u' =>
            simp only [List.map_cons, List.cons.injEq] at hb
            simp only [noAdj, hb.1, hb.2.1]
            rw [ih (w' :: u') (by simp [hb.2.1, hb.2.2])]
  cases v with
  | nil => cases w with
    | nil => rfl
    | cons _ _ => simp at h
  | cons x t => cases w with
    | nil => simp at h
    | cons y u =>
      simp only [List.map_cons, List.cons.injEq] at h
      simp only [licensed, h.1]
      rw [hn (x :: t) (y :: u) (by simp [h.1, h.2])]

theorem setLast_licensed (w : List SCell) (st : Fin 4) (hst : st.val ≠ 3)
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) :
    licensed (setLast w st) = licensed w :=
  licensed_of_map_isSukun _ _ (map_isSukun_setLast w st hst hlast)

/-- الجذوعُ المعربة (الحرفُ الأخير بلا حالة تُثبَّت بالعمليّة). -/
def stems : List (String × List SCell) := [
  ("فَوْق", [c 20 0, c 27 3, c 21 0]), ("تَحْت", [c 3 0, c 6 3, c 3 0]),
  ("خَلْف", [c 7 0, c 23 3, c 20 0]), ("وَرَاء", [c 27 0, c 10 0, c 1 3, c 0 0]),
  ("أَمَام", [c 0 0, c 24 0, c 1 3, c 24 0]), ("يَمِين", [c 28 0, c 24 1, c 28 3, c 25 0]),
  ("شِمَال", [c 13 1, c 24 0, c 1 3, c 23 0]), ("يَسَار", [c 28 0, c 12 0, c 1 3, c 10 0]),
  ("بَيْن", [c 2 0, c 28 3, c 25 0]), ("حَوْل", [c 6 0, c 27 3, c 23 0]),
  ("تِلْقَاء", [c 3 1, c 23 3, c 21 0, c 1 3, c 0 0]), ("تِجَاه", [c 3 1, c 5 0, c 1 3, c 26 0]),
  ("نَحْو", [c 25 0, c 6 3, c 27 0]), ("قَبْل", [c 21 0, c 2 3, c 23 0]),
  ("بَعْد", [c 2 0, c 18 3, c 8 0]), ("عِنْد", [c 18 1, c 25 3, c 8 0]), ("دُون", [c 8 2, c 27 3, c 25 0])
]

/-- الصورُ الثلاث لكلّ جذع. -/
def forms : List (List SCell) :=
  stems.flatMap fun p => [mudaf p.2, jarr p.2, qat p.2]

theorem forms_licensed : forms.all licensed = true := by decide
theorem forms_count : forms.length = 51 := by rfl

theorem forms_hukm : stems.all (fun p => hukm (mudaf p.2) == .mansubMudaf &&
    hukm (jarr p.2) == .majrur && hukm (qat p.2) == .maqtu) = true := by decide

/-- الثوابتُ المبنيّة: صورةٌ واحدة. -/
def constants : List (String × List SCell) := [
  ("حَيْثُ", [c 6 0, c 28 3, c 4 2]), ("لَدُنْ", [c 23 0, c 8 2, c 25 3]),
  ("لَدَى", [c 23 0, c 8 0, c 1 3]), ("ثَمَّ", Ishara.thamma), ("هُنَا", Ishara.huna)
]

theorem constants_single : constants.all (fun p => licensed p.2) = true := by decide

/-- حَيْثُ مقطوعةٌ أبدًا: حكمُها الضمّ. -/
theorem haythu_always_cut : hukm (constants.getD 0 ("", [])).2 = .maqtu := by decide

end Slge.Zuruf
