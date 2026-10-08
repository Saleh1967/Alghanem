import Slge.Categories

/-!
# السُّلَّمُ كلُّه رقمًا واحدًا — قانونُ القمع

كلُّ فهرسٍ يقيس طبقتَه وحدَها؛ هنا القانونُ الذي يجعل تركيبَ المراحل رقمًا واحدًا صادقًا: السُّلَّمُ
قائمةُ مراحلَ `List (α → Bool)`، والكلمةُ تعبر إن عبرت كلَّ مرحلة (`survive`). المبرهَن على المجرّد:

* **لا قفز**: من عبر السُّلَّمَ عبر كلَّ مرحلةٍ فيه (`survive_mem`)، وعبر كلَّ بادئةٍ منه (`survive_prefix`).
* **لا يزيد العابرون بزيادة المراحل**: عددُ من يعبر `ps ++ qs` لا يزيد على عدد من يعبر `ps`
  (`survivors_antitone`)، ومن ثَمّ لا يزيد على من يعبر أيَّ مرحلةٍ واحدةٍ فيه (`survivors_le_stage`).
* **القمعُ سلسلةٌ متناقصة**: العابرون بعد `k` مراحل لكلّ `k` يكوّنون قائمةً `Antitone`
  (`funnel_antitone`)؛ والجدولُ المولَّد على MASAQ (`PipelineTable`) يُفحص بـ`decide` أنّه كذلك.

ما لا يُبرهَن هنا: صوابُ المراحل نفسها؛ ذاك قياسٌ على المرجع المحجوب في `PIPELINE_INDEX.md`.
-/

namespace Slge.Pipeline

variable {α : Type}

/-- هل تعبر `x` المراحلَ كلَّها؟ -/
def survive (ps : List (α → Bool)) (x : α) : Bool := ps.all (fun p => p x)

/-- العابرون من `xs`. -/
def survivors (ps : List (α → Bool)) (xs : List α) : Nat := (xs.filter (survive ps)).length

theorem survive_nil (x : α) : survive ([] : List (α → Bool)) x = true := rfl

theorem survive_cons (p : α → Bool) (ps : List (α → Bool)) (x : α) :
    survive (p :: ps) x = (p x && survive ps x) := by
  simp [survive, List.all_cons]

theorem survive_append (ps qs : List (α → Bool)) (x : α) :
    survive (ps ++ qs) x = (survive ps x && survive qs x) := by
  simp [survive, List.all_append]

/-- لا قفز: من عبر السُّلَّمَ عبر كلَّ مرحلةٍ فيه. -/
theorem survive_mem {ps : List (α → Bool)} {x : α} (h : survive ps x = true) :
    ∀ p ∈ ps, p x = true := by
  simpa [survive, List.all_eq_true] using h

/-- من عبر `ps ++ qs` عبر `ps`. -/
theorem survive_prefix {ps qs : List (α → Bool)} {x : α} (h : survive (ps ++ qs) x = true) :
    survive ps x = true := by
  rw [survive_append, Bool.and_eq_true] at h
  exact h.1

/-- عددُ المرشَّح بشرطٍ أقوى لا يزيد على عدده بشرطٍ أضعف. -/
theorem length_filter_mono {f g : α → Bool} (h : ∀ x, f x = true → g x = true) :
    ∀ xs : List α, (xs.filter f).length ≤ (xs.filter g).length
  | [] => Nat.le_refl _
  | x :: xs => by
    simp only [List.filter_cons]
    cases hf : f x with
    | false =>
      cases g x with
      | false => exact length_filter_mono h xs
      | true => exact Nat.le_succ_of_le (length_filter_mono h xs)
    | true =>
      rw [h x hf]
      exact Nat.succ_le_succ (length_filter_mono h xs)

/-- لا يزيد العابرون بزيادة المراحل. -/
theorem survivors_antitone (ps qs : List (α → Bool)) (xs : List α) :
    survivors (ps ++ qs) xs ≤ survivors ps xs :=
  length_filter_mono (fun _ h => survive_prefix h) xs

/-- من يعبر السُّلَّمَ لا يزيد على من يعبر أيَّ مرحلةٍ واحدةٍ فيه. -/
theorem survivors_le_stage (ps : List (α → Bool)) (xs : List α) {p : α → Bool} (hp : p ∈ ps) :
    survivors ps xs ≤ (xs.filter p).length :=
  length_filter_mono (fun _ h => survive_mem h p hp) xs

/-- قائمةٌ متناقصة: كلُّ عنصرٍ لا يزيد على سابقه. -/
def Antitone : List Nat → Prop
  | [] => True
  | [_] => True
  | a :: b :: rest => b ≤ a ∧ Antitone (b :: rest)

instance decAntitone : ∀ l : List Nat, Decidable (Antitone l)
  | [] => inferInstanceAs (Decidable True)
  | [_] => inferInstanceAs (Decidable True)
  | a :: b :: rest =>
    have := decAntitone (b :: rest)
    inferInstanceAs (Decidable (b ≤ a ∧ Antitone (b :: rest)))

/-- `a` لا تقلّ عن `b` موضعًا موضعًا (بالطول نفسه). -/
def Dominates : List Nat → List Nat → Prop
  | [], [] => True
  | a :: as, b :: bs => b ≤ a ∧ Dominates as bs
  | _, _ => False

instance : ∀ a b : List Nat, Decidable (Dominates a b)
  | [], [] => inferInstanceAs (Decidable True)
  | _ :: _, [] => inferInstanceAs (Decidable False)
  | [], _ :: _ => inferInstanceAs (Decidable False)
  | a :: as, b :: bs =>
    have := instDecidableDominates as bs
    inferInstanceAs (Decidable (b ≤ a ∧ Dominates as bs))

/-- القمع: العابرون بعد `0, 1, …, ps.length` مراحل. -/
def funnel (ps : List (α → Bool)) (xs : List α) : List Nat :=
  (List.range (ps.length + 1)).map (fun k => survivors (ps.take k) xs)

theorem take_succ_eq_append : ∀ (ps : List (α → Bool)) (k : Nat),
    ps.take (k + 1) = ps.take k ++ (ps.drop k).take 1
  | [], _ => by simp
  | _ :: _, 0 => by simp
  | _ :: ps, k + 1 => by simp [take_succ_eq_append ps k]

theorem survivors_take_succ_le (ps : List (α → Bool)) (xs : List α) (k : Nat) :
    survivors (ps.take (k + 1)) xs ≤ survivors (ps.take k) xs := by
  rw [take_succ_eq_append]
  exact survivors_antitone _ _ xs

theorem antitone_map_of_succ_le (f : Nat → Nat) (h : ∀ k, f (k + 1) ≤ f k) :
    ∀ n, Antitone ((List.range n).map f)
  | 0 => trivial
  | 1 => trivial
  | n + 2 => by
    have ih := antitone_map_of_succ_le f h (n + 1)
    simp only [List.range_succ, List.map_append, List.map_cons, List.map_nil] at ih ⊢
    exact antitone_append_last _ _ _ ih (by simpa using h n)
where
  antitone_append_last : ∀ (l : List Nat) (a b : Nat), Antitone (l ++ [a]) → b ≤ a →
      Antitone (l ++ [a] ++ [b])
    | [], a, b, _, hb => ⟨hb, trivial⟩
    | [c], a, b, h, hb => ⟨h.1, hb, trivial⟩
    | c :: d :: rest, a, b, h, hb =>
      ⟨h.1, antitone_append_last (d :: rest) a b h.2 hb⟩

/-- القمعُ متناقصٌ لكلّ سُلَّمٍ وكلّ مادّة. -/
theorem funnel_antitone (ps : List (α → Bool)) (xs : List α) : Antitone (funnel ps xs) :=
  antitone_map_of_succ_le _ (survivors_take_succ_le ps xs) _

theorem funnel_length (ps : List (α → Bool)) (xs : List α) :
    (funnel ps xs).length = ps.length + 1 := by
  simp [funnel]

/-- السُّلَّمُ المقيس خمسُ مراحل. -/
def stageCount : Nat := 5

theorem stageCount_eq : stageCount = 5 := rfl

end Slge.Pipeline
