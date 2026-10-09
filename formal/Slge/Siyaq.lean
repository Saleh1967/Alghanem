import Slge.Sawabiq

/-!
# السياق: الكلمةُ في حدّها — إسقاطٌ وردّ

مودَعُ الغانم الثاني (`context-certificates.json.gz`) يحمل كلَّ موقعٍ من المصحف **بسياقه**: ابتداءً أو
وصلًا، استمرارًا أو وقفًا. والكلمةُ من حيث هي (مودَعُ الابتداء) تُسقَط إلى صورتها في الحدّ بعمليّتين:
* **الوقف** على أربعة أوجهٍ كما طبعتها البوّابة على المصحف (`Waqf`): تسكينُ الآخر؛ تنوينُ النصب ألفًا
  (سَبِيلًا ← سَبِيلَا)؛ حذفُ تنوين الرفع والجرّ مع التسكين (أَحَدٌ ← أَحَدْ)؛ تاءُ التأنيث هاءً ساكنة
  (وَاحِدَةٌ ← وَاحِدَهْ). أيُّ وجهٍ هو؟ قراءةٌ لا تُرى في الخانات وحدَها، فتُؤخذ معاملًا.
* **الوصل**: تسقط همزةُ الوصل (إن كان أوّلُها همزةَ وصل — قراءةٌ تُؤخذ معاملًا `wasl`): الذيل.

والردُّ `restore` يعكسهما مرشَّحاتٍ: ما أوّلُه ساكنٌ في الوصل يُرفع بهمزةٍ على قاعدة `Sawabiq.lift`
(مفتوحةٌ لأل، ومضمومةٌ إن كان الثالثُ مضمومًا وإلّا مكسورة) أو يبقى؛ وفي الوقف كلُّ ما يُسقَط إلى الصورة
بوجهٍ من الأربعة. فالوقفُ يُخفي الإعرابَ والتنوين ولا يُستعادان منه إلّا بقرينة.

المبرهَن: كلُّ مرشَّحٍ يُسقَط إلى الصورة بعينها (`project_restore`: الردُّ مغلقٌ على الإسقاط)؛ والصورةُ
نفسُها مرشَّحة (`self_mem_restore`)؛ وبلا وصلٍ ولا وقف تُردّ إلى نفسها وحدَها (`restore_plain`)؛ والعددُ
محدود (`restore_length_le`: ≤ 26). وما **لا** يُبرهَن هنا: أنّ حركةَ الهمزة المردودة هي حركةُ الأصل — ذلك
قياسُ `Sawabiq.lift` على مودَع الابتداء، رقمُه في `SIYAQ_INDEX.md`.
-/

namespace Slge.Siyaq

open Slge.Categories (c)

/-- الحدُّ: وصلٌ (أم ابتداء)، ووقفٌ (أم استمرار). -/
structure Hadd where
  joined : Bool
  pause : Bool
  deriving DecidableEq, Repr

/-- أوجهُ الوقف الأربعة كما طبعتها البوّابة. -/
inductive Waqf | sukun | alif | hadhf | ha
  deriving DecidableEq, Repr

def Waqf.all : List Waqf := [.sukun, .alif, .hadhf, .ha]

def headSukun : List SCell → Bool
  | x :: _ => x.state.val == 3
  | [] => false

def lastSukun (w : List SCell) : Bool :=
  match Afal.lastOf w with
  | some x => x.state.val == 3
  | none => false

/-- التنوين خانةً: نونٌ ساكنة. -/
def tanwin : SCell := c 25 3
def alifSakina : SCell := c 1 3
def haSakina : SCell := c 26 3

def endsWith (w : List SCell) (x : SCell) : Bool := w.getLast? == some x

/-- الوقفُ بوجهه. -/
def waqf : Waqf → List SCell → List SCell
  | .sukun, w => Zuruf.setLast w 3
  | .alif, w => w.dropLast ++ [alifSakina]
  | .hadhf, w => Zuruf.setLast w.dropLast 3
  | .ha, w => (if endsWith w tanwin then w.dropLast else w).dropLast ++ [haSakina]

/-- إسقاطُ الكلمة من حيث هي إلى صورتها في الحدّ: الوقفُ بوجهه ثمّ الوصلُ يُسقط همزةَ الوصل. -/
def project (h : Hadd) (wasl : Bool) (k : Waqf) (w : List SCell) : List SCell :=
  let p := if h.pause then waqf k w else w
  if h.joined && wasl then p.tail else p

/-- مرشَّحاتُ الوقف: ما يُسقَط إلى الصورة بوجهٍ من الأربعة. -/
def waqfCandidates (x : List SCell) : List (List SCell) :=
  [Zuruf.setLast x 0, Zuruf.setLast x 1, Zuruf.setLast x 2, Zuruf.setLast x 3]
  ++ (if endsWith x alifSakina then [x.dropLast ++ [tanwin]] else [])
  ++ [Zuruf.setLast x 1 ++ [tanwin], Zuruf.setLast x 2 ++ [tanwin]]
  ++ (if endsWith x haSakina then
        [x.dropLast ++ [c 3 0], x.dropLast ++ [c 3 1], x.dropLast ++ [c 3 2],
         x.dropLast ++ [c 3 0, tanwin], x.dropLast ++ [c 3 1, tanwin], x.dropLast ++ [c 3 2, tanwin]]
      else [])

/-- مرشَّحاتُ الأوّل: في الوصل ما أوّلُه ساكنٌ يُرفع بهمزةٍ أو يبقى. -/
def heads (h : Hadd) (x : List SCell) : List (List SCell) :=
  if h.joined && headSukun x then [Sawabiq.lift x, x] else [x]

/-- ردُّ الصورة في الحدّ إلى مرشَّحات الكلمة من حيث هي. -/
def restore (h : Hadd) (x : List SCell) : List (List SCell) :=
  if h.pause then (heads h x).flatMap waqfCandidates else heads h x

/-! ## أدواتُ البرهان -/

theorem setLast_of_lastSukun : ∀ (w : List SCell), lastSukun w = true → Zuruf.setLast w 3 = w
  | [], h => by simp [lastSukun, Afal.lastOf] at h
  | ⟨k, st⟩ :: [], h => by
    simp only [lastSukun, Afal.lastOf, beq_iff_eq] at h
    simp only [Zuruf.setLast, List.cons.injEq, and_true, SCell.mk.injEq, true_and]
    exact (Fin.ext h).symm
  | x :: y :: t, h => by
    have ih := setLast_of_lastSukun (y :: t) (by simpa [lastSukun, Afal.lastOf] using h)
    simp [Zuruf.setLast, ih]

theorem lift_tail (x : List SCell) : (Sawabiq.lift x).tail = x := by
  unfold Sawabiq.lift; split <;> rfl

theorem lastSukun_cons (a : SCell) (x : List SCell) (hx : x ≠ []) :
    lastSukun (a :: x) = lastSukun x := by
  cases x with
  | nil => exact absurd rfl hx
  | cons y t => simp [lastSukun, Afal.lastOf]

theorem lastSukun_lift (x : List SCell) (hx : x ≠ []) :
    lastSukun (Sawabiq.lift x) = lastSukun x := by
  unfold Sawabiq.lift; split <;> exact lastSukun_cons _ x hx

theorem dropLast_append_of_getLast? : ∀ {l : List SCell} {a : SCell},
    l.getLast? = some a → l.dropLast ++ [a] = l
  | [], _, h => by simp at h
  | [x], a, h => by simp at h; simp [h]
  | x :: y :: t, a, h => by
    have ih := dropLast_append_of_getLast? (l := y :: t) (a := a) (by simpa using h)
    simpa [List.dropLast] using ih

theorem endsWith_restore {x : List SCell} {a : SCell} (h : endsWith x a = true) :
    x.dropLast ++ [a] = x :=
  dropLast_append_of_getLast? (by simpa [endsWith] using h)

theorem endsWith_append (l : List SCell) (a b : SCell) : endsWith (l ++ [a]) b = (a == b) := by
  simp [endsWith]

theorem endsWith_append₂ (l : List SCell) (a b d : SCell) :
    endsWith (l ++ [a, b]) d = (b == d) := by
  simp [endsWith]

/-- كلُّ مرشَّح وقفٍ يُسقَط إلى الصورة بوجهٍ من الأربعة. -/
theorem waqf_candidates_sound {x : List SCell} (hx : lastSukun x = true) :
    ∀ w ∈ waqfCandidates x, ∃ k, waqf k w = x := by
  intro w hw
  have hsx := setLast_of_lastSukun x hx
  simp only [waqfCandidates, List.append_assoc, List.mem_append, List.mem_cons,
    List.not_mem_nil, or_false] at hw
  rcases hw with (rfl | rfl | rfl | rfl) | hw | (rfl | rfl) | hw
  · exact ⟨.sukun, by simp [waqf, Shibh.setLast_setLast, hsx]⟩
  · exact ⟨.sukun, by simp [waqf, Shibh.setLast_setLast, hsx]⟩
  · exact ⟨.sukun, by simp [waqf, Shibh.setLast_setLast, hsx]⟩
  · exact ⟨.sukun, by simp [waqf, hsx]⟩
  · split at hw <;> rename_i ha
    · simp only [List.mem_cons, List.not_mem_nil, or_false] at hw
      subst hw
      exact ⟨.alif, by simp [waqf, endsWith_restore ha]⟩
    · simp at hw
  · exact ⟨.hadhf, by simp [waqf, Shibh.setLast_setLast, hsx]⟩
  · exact ⟨.hadhf, by simp [waqf, Shibh.setLast_setLast, hsx]⟩
  · split at hw <;> rename_i hh
    · simp only [List.mem_cons, List.not_mem_nil, or_false] at hw
      rcases hw with rfl | rfl | rfl | rfl | rfl | rfl
      all_goals exact ⟨.ha, by
        simp [waqf, endsWith_append, endsWith_append₂, endsWith_restore hh, tanwin, c]⟩
    · simp at hw

theorem mem_heads {h : Hadd} {u x : List SCell} (hu : u ∈ heads h x) :
    ∃ b, (h.joined && b) = true ∧ u = Sawabiq.lift x ∨ b = false ∧ u = x := by
  unfold heads at hu
  split at hu <;> rename_i hc
  · simp only [List.mem_cons, List.not_mem_nil, or_false] at hu
    rcases hu with rfl | rfl
    · exact ⟨true, Or.inl ⟨by simp_all, rfl⟩⟩
    · exact ⟨false, Or.inr ⟨rfl, rfl⟩⟩
  · simp only [List.mem_cons, List.not_mem_nil, or_false] at hu
    exact ⟨false, Or.inr ⟨rfl, hu⟩⟩

theorem project_pause (h : Hadd) (b : Bool) (k : Waqf) (w : List SCell) (hp : h.pause = true) :
    project h b k w = (if h.joined && b then (waqf k w).tail else waqf k w) := by
  simp [project, hp]

theorem project_continue (h : Hadd) (b : Bool) (k : Waqf) (w : List SCell) (hp : h.pause = false) :
    project h b k w = (if h.joined && b then w.tail else w) := by
  simp [project, hp]

theorem lastSukun_ne_nil {x : List SCell} (hx : lastSukun x = true) : x ≠ [] := by
  intro h; subst h; simp [lastSukun, Afal.lastOf] at hx

/-- الردُّ مغلقٌ على الإسقاط: كلُّ مرشَّحٍ يعود إلى الصورة بعينها (بمعاملَي الوصل والوقف المناسبين). -/
theorem project_restore (h : Hadd) (x : List SCell) (hx : h.pause = true → lastSukun x = true) :
    ∀ w ∈ restore h x, ∃ b k, project h b k w = x := by
  intro w hw
  unfold restore at hw
  cases hp : h.pause
  · rw [hp] at hw
    simp only [Bool.false_eq_true, ite_false] at hw
    obtain ⟨b, hb⟩ := mem_heads hw
    refine ⟨b, .sukun, ?_⟩
    rw [project_continue h b .sukun w hp]
    rcases hb with ⟨hjb, rfl⟩ | ⟨rfl, rfl⟩
    · rw [hjb]; simp [lift_tail]
    · simp
  · rw [hp] at hw
    simp only [ite_true, List.mem_flatMap] at hw
    obtain ⟨u, hu, hwu⟩ := hw
    obtain ⟨b, hb⟩ := mem_heads hu
    rcases hb with ⟨hjb, rfl⟩ | ⟨rfl, rfl⟩
    · -- `u = lift x`: آخرُه آخرُ `x` ساكنٌ، فمرشَّحاتُ وقفه تعود إليه، وذيلُه `x`.
      have hl : lastSukun (Sawabiq.lift x) = true := by
        rw [lastSukun_lift x (lastSukun_ne_nil (hx hp))]; exact hx hp
      obtain ⟨k, hk⟩ := waqf_candidates_sound hl w hwu
      exact ⟨b, k, by rw [project_pause h b k w hp, hjb]; simp [hk, lift_tail]⟩
    · obtain ⟨k, hk⟩ := waqf_candidates_sound (hx hp) w hwu
      exact ⟨false, k, by rw [project_pause h false k w hp]; simp [hk]⟩

theorem self_mem_heads (h : Hadd) (x : List SCell) : x ∈ heads h x := by
  unfold heads; split <;> simp

/-- الصورةُ نفسُها مرشَّحة (آخرُها ساكنٌ وقفًا). -/
theorem self_mem_restore (h : Hadd) (x : List SCell) (hx : h.pause = true → lastSukun x = true) :
    x ∈ restore h x := by
  unfold restore
  cases hp : h.pause
  · simp only [Bool.false_eq_true, ite_false]; exact self_mem_heads h x
  · simp only [ite_true, List.mem_flatMap]
    exact ⟨x, self_mem_heads h x, by
      simp only [waqfCandidates, List.append_assoc, List.mem_append, List.mem_cons,
        setLast_of_lastSukun x (hx hp)]; simp⟩

/-- بلا وصلٍ ولا وقف: الصورةُ هي الكلمة. -/
theorem restore_plain (x : List SCell) : restore ⟨false, false⟩ x = [x] := rfl

theorem heads_length_le (h : Hadd) (x : List SCell) : (heads h x).length ≤ 2 := by
  unfold heads; split <;> simp

theorem waqfCandidates_length_le (x : List SCell) : (waqfCandidates x).length ≤ 13 := by
  unfold waqfCandidates; split <;> split <;> simp

/-- عددُ المرشَّحات: اثنان في الوصل، وثلاثةَ عشرَ لكلٍّ في الوقف. -/
theorem restore_length_le (h : Hadd) (x : List SCell) : (restore h x).length ≤ 26 := by
  unfold restore
  split
  · unfold heads
    split
    · simp only [List.flatMap_cons, List.flatMap_nil, List.append_nil, List.length_append]
      have := waqfCandidates_length_le (Sawabiq.lift x)
      have := waqfCandidates_length_le x
      omega
    · simp only [List.flatMap_cons, List.flatMap_nil, List.append_nil]
      exact Nat.le_trans (waqfCandidates_length_le x) (by decide)
  · exact Nat.le_trans (heads_length_le h x) (by decide)

/-! ## شواهد -/

/-- لِلَّهِ بعد بِسْمِ: الصورةُ في الوصل `لْلَهِ`؛ المردودُ `ءَلْلَهِ` (أل) أو هي. -/
def lillahiJoined : List SCell := [c 23 3, c 23 0, c 26 1]

/-- سَبِيلًا وقفًا: `سَبِيلَا` — التنوينُ ألفًا؛ والردُّ يحوي سَبِيلًا بعينه. -/
def sabilanPaused : List SCell := [c 12 0, c 2 1, c 28 3, c 23 0, c 1 3]
def sabilan : List SCell := [c 12 0, c 2 1, c 28 3, c 23 0, c 25 3]

/-- وَاحِدَةٌ وقفًا: `وَاحِدَهْ` — التاءُ هاءً والتنوينُ ساقط. -/
def wahidahPaused : List SCell := [c 27 0, c 1 3, c 6 1, c 8 0, c 26 3]
def wahidatun : List SCell := [c 27 0, c 1 3, c 6 1, c 8 0, c 3 2, c 25 3]

theorem witness_joined :
    restore ⟨true, false⟩ lillahiJoined = [c 0 0 :: lillahiJoined, lillahiJoined] := by decide

theorem witness_paused :
    sabilan ∈ restore ⟨true, true⟩ sabilanPaused ∧ waqf .alif sabilan = sabilanPaused ∧
    wahidatun ∈ restore ⟨true, true⟩ wahidahPaused ∧ waqf .ha wahidatun = wahidahPaused ∧
    (restore ⟨true, true⟩ wahidahPaused).length = 12 := by decide

end Slge.Siyaq
