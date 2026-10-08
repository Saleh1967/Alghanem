import Slge.Maqayis
import Slge.Adawat
import Slge.HasmTable

/-!
# حسمُ الجذع — قسمةٌ واحدة بقرينتين

ما يسأله المرجعُ عن الكلمة قسمتُها (سوابق، أل، جذع، لواحق) لا قالبُها: القراءاتُ المتّفقةُ قسمةً قسمةٌ واحدة
(`segments`، صحيحةٌ وتامّةٌ: `mem_segments`). وإن تعدّدت القسماتُ حُسم بينها بالدرجة — الجوارُ (الأداةُ قبلها
توافق قراءةً من القسمة) ثمّ المعجمُ (جذرٌ مشهود في المقاييس) ثمّ تكرارُ الجذر في المودَع (`HasmTable`) — عددًا
واحدًا مرتَّبًا ترتيبًا معجميًّا (`score`؛ التكرارُ تحت الحدّ `freq_lt_bound` فلا يطغى على ما فوقه:
`score_order`). الحسمُ **الأعلى الوحيد** (`best`): ما يُختار من القسمات (`best_mem`)، لا يقلّ عن كلّ قسمة
(`best_max`)، ويعلو كلَّ قسمةٍ غيرِه (`best_strict`)؛ والتعادلُ لا يُحسم (`best_none_of_tie`). القراءاتُ لا
تُحذف: `hasm` يختار قسمةً من قسمات القراءات نفسها (`hasm_mem`) ولا يمسّها.
-/

namespace Slge.Hasm

open Slge.Categories (c)

/-- القسمة: (السوابق، أل، الجذع، اللاحقة). -/
abbrev Seg := List (List SCell) × Jidh.Al × List SCell × List SCell

def segOf (rd : Jidh.Reading) : Seg := (rd.pre, rd.al, rd.stem, rd.suf)

/-- القسماتُ المتمايزة بترتيب أوّل ظهورها. -/
def segments : List Jidh.Reading → List Seg
  | [] => []
  | rd :: rs => segOf rd :: (segments rs).filter (· ≠ segOf rd)

theorem mem_segments (rs : List Jidh.Reading) (s : Seg) :
    s ∈ segments rs ↔ ∃ rd ∈ rs, segOf rd = s := by
  induction rs with
  | nil => simp [segments]
  | cons rd rs ih =>
    simp only [segments, List.mem_cons, List.mem_filter, ih, decide_eq_true_eq]
    constructor
    · rintro (h | ⟨⟨r, hr, hs⟩, _⟩)
      · exact ⟨rd, Or.inl rfl, h.symm⟩
      · exact ⟨r, Or.inr hr, hs⟩
    · rintro ⟨r, hr | hr, hs⟩
      · exact Or.inl (hr ▸ hs.symm)
      · by_cases h : s = segOf rd
        · exact Or.inl h
        · exact Or.inr ⟨⟨r, hr, hs⟩, h⟩

theorem segments_nodup : ∀ rs : List Jidh.Reading, (segments rs).Nodup
  | [] => List.nodup_nil
  | rd :: rs => by
    simp only [segments]
    refine List.nodup_cons.2 ⟨?_, (segments_nodup rs).filter _⟩
    intro h
    have := (List.mem_filter.1 h).2
    simp at this

/-- قراءاتُ القسمة. -/
def group (s : Seg) (rs : List Jidh.Reading) : List Jidh.Reading := rs.filter (fun rd => segOf rd == s)

/-- رمزُ الجذر كما في جدول التكرار. -/
def code (r : Wazn.Root) : Nat := r 0 * 900 + r 1 * 30 + r 2

/-- تكرارُ الجذر في المودَع (0 إن لم يُشهد). -/
def freqOf (r : Wazn.Root) : Nat := ((HasmTable.table.find? (·.1 == code r)).map (·.2)).getD 0

theorem freqOf_lt_bound (r : Wazn.Root) : freqOf r < HasmTable.bound := by
  unfold freqOf
  cases h : HasmTable.table.find? (·.1 == code r) with
  | none => simp [HasmTable.bound]
  | some p =>
    have hp := List.mem_of_find?_eq_some h
    have := List.all_eq_true.1 HasmTable.freq_lt_bound p hp
    simpa using this

/-- أكبرُ تكرارٍ لجذرٍ من جذور القراءات. -/
def freqMax (g : List Jidh.Reading) : Nat :=
  g.foldl (fun acc rd => (Maqayis.Reading.roots rd).foldl (fun m' r => max m' (freqOf r)) acc) 0

theorem foldl_max_lt {β : Type} (f : β → Nat) (b : Nat) (hb : ∀ x, f x < b) :
    ∀ (l : List β) (m : Nat), m < b → l.foldl (fun m' x => max m' (f x)) m < b
  | [], _, hm => hm
  | x :: l, _, hm => foldl_max_lt f b hb l _ (Nat.max_lt.2 ⟨hm, hb x⟩)

theorem freqMax_aux : ∀ (g : List Jidh.Reading) (m : Nat), m < HasmTable.bound →
    g.foldl (fun acc rd => (Maqayis.Reading.roots rd).foldl (fun m' r => max m' (freqOf r)) acc) m
      < HasmTable.bound
  | [], _, hm => hm
  | _ :: g, m, hm =>
    freqMax_aux g _ (foldl_max_lt freqOf HasmTable.bound freqOf_lt_bound _ m hm)

theorem freqMax_lt_bound (g : List Jidh.Reading) : freqMax g < HasmTable.bound :=
  freqMax_aux g 0 (by decide)

/-- الجوارُ: الأداةُ قبل الكلمة توافق قراءةً من القسمة. -/
def neighbour (a : Option Adawat.Adat) (g : List Jidh.Reading) : Bool :=
  match a with
  | some a => g.any (Adawat.fits a)
  | none => false

/-- المعجم: قراءةٌ من القسمة مشهودة. -/
def lexical (g : List Jidh.Reading) : Bool := g.any Maqayis.attested

/-- الدرجة: الجوارُ ثمّ المعجمُ ثمّ التكرار، عددًا واحدًا. -/
def score (a : Option Adawat.Adat) (g : List Jidh.Reading) : Nat :=
  ((if neighbour a g then 2 else 0) + (if lexical g then 1 else 0)) * HasmTable.bound + freqMax g

/-- الأعلى الوحيد، وإلّا لا شيء. -/
def best {α : Type} [DecidableEq α] (s : α → Nat) (xs : List α) : Option α :=
  match xs.filter (fun x => xs.all (fun y => s y ≤ s x)) with
  | [x] => some x
  | _ => none

theorem best_eq {α : Type} [DecidableEq α] (s : α → Nat) (xs : List α) (x : α)
    (h : best s xs = some x) : xs.filter (fun x => xs.all (fun y => s y ≤ s x)) = [x] := by
  unfold best at h
  split at h
  · simp_all
  · exact absurd h (by simp)

theorem best_mem {α : Type} [DecidableEq α] {s : α → Nat} {xs : List α} {x : α}
    (h : best s xs = some x) : x ∈ xs := by
  have := best_eq s xs x h
  have hx : x ∈ xs.filter (fun x => xs.all (fun y => s y ≤ s x)) := by simp [this]
  exact (List.mem_filter.1 hx).1

theorem best_max {α : Type} [DecidableEq α] {s : α → Nat} {xs : List α} {x : α}
    (h : best s xs = some x) : ∀ y ∈ xs, s y ≤ s x := by
  have := best_eq s xs x h
  have hx : x ∈ xs.filter (fun x => xs.all (fun y => s y ≤ s x)) := by simp [this]
  have := (List.mem_filter.1 hx).2
  simpa [List.all_eq_true] using this

theorem best_strict {α : Type} [DecidableEq α] {s : α → Nat} {xs : List α} {x : α}
    (h : best s xs = some x) : ∀ y ∈ xs, y ≠ x → s y < s x := by
  intro y hy hne
  have hmax := best_max h
  rcases Nat.lt_or_ge (s y) (s x) with hlt | hge
  · exact hlt
  · exfalso
    have hyx : s y = s x := Nat.le_antisymm (hmax y hy) hge
    have hyf : y ∈ xs.filter (fun x => xs.all (fun y => s y ≤ s x)) := by
      refine List.mem_filter.2 ⟨hy, ?_⟩
      simp only [List.all_eq_true, decide_eq_true_eq]
      intro z hz
      exact hyx ▸ hmax z hz
    rw [best_eq s xs x h] at hyf
    exact hne (List.mem_singleton.1 hyf)

theorem best_single {α : Type} [DecidableEq α] (s : α → Nat) (x : α) : best s [x] = some x := by
  simp [best]

/-- تعادلٌ على القمّة بين مختلفَين: لا حسم. -/
theorem best_none_of_tie {α : Type} [DecidableEq α] {s : α → Nat} {xs : List α} {x y : α}
    (hx : x ∈ xs) (hy : y ∈ xs) (hne : x ≠ y) (heq : s x = s y) (hmax : ∀ z ∈ xs, s z ≤ s x) :
    best s xs = none := by
  cases h : best s xs with
  | none => rfl
  | some z =>
    exfalso
    have hs := best_strict h
    have hzmax := best_max h
    by_cases hxz : x = z
    · subst hxz
      exact Nat.lt_irrefl _ (heq ▸ hs y hy (Ne.symm hne))
    · have h1 := hs x hx hxz
      have h2 := hmax z (best_mem h)
      exact Nat.lt_irrefl _ (Nat.lt_of_lt_of_le h1 h2)

/-- الحسم: قسمةٌ واحدة كما هي، أو الأعلى الوحيدة بالدرجة، أو لا شيء. -/
def hasm (a : Option Adawat.Adat) (rs : List Jidh.Reading) : Option Seg :=
  match segments rs with
  | [] => none
  | [s] => some s
  | ss => best (fun s => score a (group s rs)) ss

/-- ما يُحسم قسمةُ قراءةٍ من القراءات نفسها. -/
theorem hasm_mem {a : Option Adawat.Adat} {rs : List Jidh.Reading} {s : Seg}
    (h : hasm a rs = some s) : ∃ rd ∈ rs, segOf rd = s := by
  rw [← mem_segments]
  unfold hasm at h
  revert h
  cases hs : segments rs with
  | nil => intro h; simp at h
  | cons s0 rest =>
    cases rest with
    | nil => intro h; simp_all
    | cons s1 rest' => intro h; exact best_mem h

/-- قسمةٌ واحدة تُحسم بلا قرينة. -/
theorem hasm_unique (a : Option Adawat.Adat) (rs : List Jidh.Reading) (s : Seg)
    (h : segments rs = [s]) : hasm a rs = some s := by
  simp [hasm, h]

/-- الجوارُ يعلو المعجمَ والتكرار، والمعجمُ يعلو التكرار: الدرجةُ مرتَّبةٌ ترتيبًا معجميًّا. -/
theorem score_order (a : Option Adawat.Adat) (g g' : List Jidh.Reading)
    (hn : neighbour a g = true) (hn' : neighbour a g' = false) :
    score a g' < score a g := by
  unfold score
  rw [hn, hn']
  have h1 := freqMax_lt_bound g'
  by_cases hl : lexical g = true <;> by_cases hl' : lexical g' = true <;> simp [hl, hl'] <;> omega

/-! ## شواهد على المودَع (بـ`decide`) -/

def min_ : List SCell := [c 24 1, c 25 3]                         -- مِنْ
def kataba : List SCell := [c 22 0, c 3 0, c 2 0]                -- كَتَبَ
def ilayka : List SCell := [c 0 1, c 23 0, c 28 3, c 22 0]        -- إِلَيْكَ

/-- مِنْ: قراءتان على قالبين وقسمةٌ واحدة — تُحسم بلا قرينة. -/
theorem witness_min :
    (Jidh.jidh min_).length = 2 ∧ segments (Jidh.jidh min_) = [([], .none, min_, [])] ∧
    hasm none (Jidh.jidh min_) = some ([], .none, min_, []) := by decide +kernel

/-- كَتَبَ: قسمتان (كَ سابقةً + تَبَ، أو كَتَبَ) — تُحسم بالمعجم والتكرار إلى كَتَبَ. -/
theorem witness_kataba :
    (segments (Jidh.jidh kataba)).length = 2 ∧
    hasm none (Jidh.jidh kataba) = some ([], .none, kataba, []) := by decide +kernel

/-- إِلَيْكَ: قسمتان (الكافُ لاحقةً أو من الجذع) — تُحسم إلى إِلَيْ + كَ. -/
theorem witness_ilayka :
    (segments (Jidh.jidh ilayka)).length = 2 ∧
    hasm none (Jidh.jidh ilayka) = some ([], .none, [c 0 1, c 23 0, c 28 3], [c 22 0]) := by
  decide +kernel

end Slge.Hasm
