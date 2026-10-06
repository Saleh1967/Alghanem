import Slge.Bridge

/-!
# الوزن: الميزانُ الصرفيُّ قالبًا على الخانات

الوزنُ قالبٌ `Template`: رموزٌ كلٌّ منها زائدٌ بخانته (`lit`) أو أصلٌ بموضعه وحالته (`slot`).
وملؤه بأصلٍ ثلاثيّ `fill` يعطي الكلمةَ خاناتٍ. المبرهَن:

* `rootOf_fill`: الأصلُ يُستردّ من الصيغة بالقالب (أوّلُ ظهورٍ لكلّ موضع)، لكلّ قالبٍ سليم
  (`WF`: المواضعُ الثلاثةُ كلُّها حاضرة) ولكلّ أصل.
* `states_fill`: حالاتُ الصيغة هي حالاتُ القالب، لا تتوقّف على الأصل.
* `licensed_fill_indep`: **الترخيصُ لا يتوقّف على الأصل** — فالوزنُ يُرخَّص مرّةً لكلّ الأصول.
* `awzan_wf`، `awzan_licensed`: الأوزانُ المودَعة (113) سليمةٌ ومرخَّصةٌ بميزانها، فمرخَّصةٌ
  لكلّ أصلٍ بـ`licensed_fill_indep`.

وهو الشقُّ الصوريُّ من `A116.Ishtiqaq` معادًا على خانات SLGE بحالاتها؛ ما ليس هنا: الإعلال،
والرباعيّ، والدلالة.
-/

namespace Slge.Wazn

/-- رمزُ القالب. -/
inductive Sym where
  | lit : SCell → Sym
  | slot : Fin 3 → Fin 4 → Sym
  deriving DecidableEq, Repr

abbrev Template := List Sym
abbrev Root := Fin 3 → Fin 29

def fillSym (r : Root) : Sym → SCell
  | .lit c => c
  | .slot i s => ⟨r i, s⟩

/-- ملءُ القالب. -/
def fill (t : Template) (r : Root) : List SCell := t.map (fillSym r)

/-- حالةُ الرمز. -/
def stateOf : Sym → Fin 4
  | .lit c => c.state
  | .slot _ s => s

/-- مواضعُ الأصل في القالب بترتيبها. -/
def slots : Template → List (Fin 3)
  | [] => []
  | .lit _ :: t => slots t
  | .slot i _ :: t => i :: slots t

/-- القالبُ السليم: المواضعُ الثلاثةُ حاضرة. -/
def WF (t : Template) : Prop := (0 : Fin 3) ∈ slots t ∧ (1 : Fin 3) ∈ slots t ∧ (2 : Fin 3) ∈ slots t

instance (t : Template) : Decidable (WF t) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))

/-- الاستخراج: أزواجُ (موضع، حامل) من الصيغة بالقالب. -/
def extract : Template → List SCell → List (Fin 3 × Fin 29)
  | [], _ => []
  | _, [] => []
  | .lit _ :: t, _ :: w => extract t w
  | .slot i _ :: t, c :: w => (i, c.carrier) :: extract t w

/-- أوّلُ ظهور. -/
def lookup (i : Fin 3) : List (Fin 3 × Fin 29) → Option (Fin 29)
  | [] => none
  | (j, c) :: l => if i = j then some c else lookup i l

/-- الأصلُ من الصيغة بالقالب. -/
def rootOf (t : Template) (w : List SCell) (i : Fin 3) : Option (Fin 29) := lookup i (extract t w)

theorem extract_fill (t : Template) (r : Root) :
    extract t (fill t r) = (slots t).map (fun i => (i, r i)) := by
  induction t with
  | nil => rfl
  | cons s t ih =>
    cases s with
    | lit c => simpa [fill, fillSym, extract, slots] using ih
    | slot i st => simpa [fill, fillSym, extract, slots] using ih

theorem lookup_map (r : Root) (i : Fin 3) : ∀ l : List (Fin 3), i ∈ l →
    lookup i (l.map (fun j => (j, r j))) = some (r i)
  | [], h => absurd h (List.not_mem_nil)
  | j :: l, h => by
    simp only [List.map, lookup]
    by_cases hij : i = j
    · subst hij; simp
    · simp [hij]
      exact lookup_map r i l (by
        rcases List.mem_cons.1 h with h1 | h1
        · exact absurd h1 hij
        · exact h1)

/-- الأصلُ يُستردّ من الصيغة، لكلّ قالبٍ سليمٍ ولكلّ أصل. -/
theorem rootOf_fill (t : Template) (h : WF t) (r : Root) :
    ∀ i, rootOf t (fill t r) i = some (r i) := by
  intro i
  unfold rootOf
  rw [extract_fill]
  apply lookup_map
  match i with
  | 0 => exact h.1
  | 1 => exact h.2.1
  | 2 => exact h.2.2

/-- حالاتُ الصيغة حالاتُ القالب. -/
theorem states_fill (t : Template) (r : Root) :
    (fill t r).map SCell.state = t.map stateOf := by
  induction t with
  | nil => rfl
  | cons s t ih =>
    cases s <;> simp [fill, fillSym, stateOf] at ih ⊢ <;> exact ih

/-! ## الترخيصُ دالّةٌ في الحالات وحدَها -/

def noAdjS : List (Fin 4) → Bool
  | a :: b :: t => !(a.val == 3 && b.val == 3) && noAdjS (b :: t)
  | _ => true

def licensedS : List (Fin 4) → Bool
  | [] => true
  | s :: t => !(s.val == 3) && noAdjS (s :: t)

theorem noAdj_states : ∀ w : List SCell, noAdj w = noAdjS (w.map SCell.state)
  | [] => rfl
  | [_] => rfl
  | a :: b :: t => by
    simp only [noAdj, noAdjS, List.map, SCell.isSukun]
    rw [noAdj_states (b :: t)]; rfl

theorem licensed_states (w : List SCell) : licensed w = licensedS (w.map SCell.state) := by
  cases w with
  | nil => rfl
  | cons c t =>
    simp only [licensed, licensedS, List.map, SCell.isSukun]
    rw [noAdj_states (c :: t)]; rfl

/-- **الترخيصُ لا يتوقّف على الأصل.** -/
theorem licensed_fill_indep (t : Template) (r r' : Root) :
    licensed (fill t r) = licensed (fill t r') := by
  rw [licensed_states, licensed_states, states_fill, states_fill]

/-- الميزان: الأصلُ (ف، ع، ل) = (20، 18، 23). -/
def falRoot : Root := fun i => if i = 0 then ⟨20, by decide⟩ else if i = 1 then ⟨18, by decide⟩
  else ⟨23, by decide⟩

def mizan (t : Template) : List SCell := fill t falRoot

/-- مرخَّصٌ بميزانه ⇒ مرخَّصٌ بكلّ أصل. -/
theorem licensed_of_mizan (t : Template) (h : licensed (mizan t) = true) (r : Root) :
    licensed (fill t r) = true := by
  rw [licensed_fill_indep t r falRoot]; exact h

/-! ## الأوزانُ المودَعة -/

def r (i s : Nat) (hi : i < 3 := by decide) (hs : s < 4 := by decide) : Sym := .slot ⟨i, hi⟩ ⟨s, hs⟩
def l (k s : Nat) (hk : k < 29 := by decide) (hs : s < 4 := by decide) : Sym := .lit ⟨⟨k, hk⟩, ⟨s, hs⟩⟩

/-- 113 وزنًا بترتيب `slge.wazn.AWZAN` (مولَّدةٌ منه؛ تُطابَق بجدول `wazn.csv`). -/
def awzan : List Template := [
  [r 0 0, r 1 0, r 2 0],  -- فَعَلَ
  [r 0 0, r 1 1, r 2 0],  -- فَعِلَ
  [r 0 0, r 1 2, r 2 0],  -- فَعُلَ
  [r 0 2, r 1 1, r 2 0],  -- فُعِلَ
  [l 28 0, r 0 3, r 1 0, r 2 2],  -- يَفْعَلُ
  [l 28 0, r 0 3, r 1 1, r 2 2],  -- يَفْعِلُ
  [l 28 0, r 0 3, r 1 2, r 2 2],  -- يَفْعُلُ
  [l 28 2, r 0 3, r 1 0, r 2 2],  -- يُفْعَلُ
  [l 0 1, r 0 3, r 1 0, r 2 3],  -- اِفْعَلْ
  [l 0 1, r 0 3, r 1 1, r 2 3],  -- اِفْعِلْ
  [l 0 2, r 0 3, r 1 2, r 2 3],  -- اُفْعُلْ
  [l 0 0, r 0 3, r 1 0, r 2 0],  -- أَفْعَلَ
  [r 0 0, r 1 3, r 1 0, r 2 0],  -- فَعَّلَ
  [r 0 0, l 1 3, r 1 0, r 2 0],  -- فَاعَلَ
  [l 3 0, r 0 0, r 1 3, r 1 0, r 2 0],  -- تَفَعَّلَ
  [l 3 0, r 0 0, l 1 3, r 1 0, r 2 0],  -- تَفَاعَلَ
  [l 0 1, l 25 3, r 0 0, r 1 0, r 2 0],  -- اِنْفَعَلَ
  [l 0 1, r 0 3, l 3 0, r 1 0, r 2 0],  -- اِفْتَعَلَ
  [l 0 1, r 0 3, r 1 0, r 2 3, r 2 0],  -- اِفْعَلَّ
  [l 0 1, l 12 3, l 3 0, r 0 3, r 1 0, r 2 0],  -- اِسْتَفْعَلَ
  [l 28 2, r 0 3, r 1 1, r 2 2],  -- يُفْعِلُ
  [l 28 2, r 0 0, r 1 3, r 1 1, r 2 2],  -- يُفَعِّلُ
  [l 28 2, r 0 0, l 1 3, r 1 1, r 2 2],  -- يُفَاعِلُ
  [l 28 0, l 3 0, r 0 0, r 1 3, r 1 0, r 2 2],  -- يَتَفَعَّلُ
  [l 28 0, l 3 0, r 0 0, l 1 3, r 1 0, r 2 2],  -- يَتَفَاعَلُ
  [l 28 0, l 25 3, r 0 0, r 1 1, r 2 2],  -- يَنْفَعِلُ
  [l 28 0, r 0 3, l 3 0, r 1 1, r 2 2],  -- يَفْتَعِلُ
  [l 28 0, r 0 3, r 1 0, r 2 3, r 2 2],  -- يَفْعَلُّ
  [l 28 0, l 12 3, l 3 0, r 0 3, r 1 1, r 2 2],  -- يَسْتَفْعِلُ
  [r 0 0, r 1 3, r 2 2],  -- فَعْلٌ
  [r 0 2, r 1 2, l 27 3, r 2 2],  -- فُعُولٌ
  [r 0 0, r 1 0, l 1 3, r 2 0, l 3 2],  -- فَعَالَةٌ
  [r 0 2, r 1 2, l 27 3, r 2 0, l 3 2],  -- فُعُولَةٌ
  [r 0 0, r 1 0, r 2 0, l 1 3, l 25 2],  -- فَعَلَانٌ
  [r 0 2, r 1 0, l 1 3, r 2 2],  -- فُعَالٌ
  [r 0 1, r 1 0, l 1 3, r 2 2],  -- فِعَالٌ
  [r 0 0, r 1 0, r 2 2],  -- فَعَلٌ
  [r 0 1, r 1 0, l 1 3, r 2 0, l 3 2],  -- فِعَالَةٌ
  [l 0 1, r 0 3, r 1 0, l 1 3, r 2 2],  -- إِفْعَالٌ
  [l 3 0, r 0 3, r 1 1, l 28 3, r 2 2],  -- تَفْعِيلٌ
  [l 24 2, r 0 0, l 1 3, r 1 0, r 2 0, l 3 2],  -- مُفَاعَلَةٌ
  [r 0 1, r 1 0, l 1 3, r 2 2],  -- فِعَالٌ (مفاعلة)
  [l 3 0, r 0 0, r 1 3, r 1 2, r 2 2],  -- تَفَعُّلٌ
  [l 3 0, r 0 0, l 1 3, r 1 2, r 2 2],  -- تَفَاعُلٌ
  [l 0 1, l 25 3, r 0 1, r 1 0, l 1 3, r 2 2],  -- اِنْفِعَالٌ
  [l 0 1, r 0 3, l 3 1, r 1 0, l 1 3, r 2 2],  -- اِفْتِعَالٌ
  [l 0 1, r 0 3, r 1 1, r 2 0, l 1 3, r 2 2],  -- اِفْعِلَالٌ
  [l 0 1, l 12 3, l 3 1, r 0 3, r 1 0, l 1 3, r 2 2],  -- اِسْتِفْعَالٌ
  [r 0 0, l 1 3, r 1 1, r 2 2],  -- فَاعِلٌ
  [l 24 0, r 0 3, r 1 2, l 27 3, r 2 2],  -- مَفْعُولٌ
  [r 0 0, r 1 3, r 1 0, l 1 3, r 2 2],  -- فَعَّالٌ
  [l 24 1, r 0 3, r 1 0, l 1 3, r 2 2],  -- مِفْعَالٌ
  [r 0 0, r 1 2, l 27 3, r 2 2],  -- فَعُولٌ
  [r 0 0, r 1 1, l 28 3, r 2 2],  -- فَعِيلٌ
  [l 0 0, r 0 3, r 1 0, r 2 2],  -- أَفْعَلُ
  [r 0 0, r 1 3, r 2 0, l 1 3, l 25 2],  -- فَعْلَانُ
  [l 24 0, r 0 3, r 1 0, r 2 2],  -- مَفْعَلٌ
  [l 24 0, r 0 3, r 1 1, r 2 2],  -- مَفْعِلٌ
  [l 24 0, r 0 3, r 1 0, r 2 0, l 3 2],  -- مَفْعَلَةٌ
  [l 24 1, r 0 3, r 1 0, r 2 2],  -- مِفْعَلٌ
  [l 24 1, r 0 3, r 1 0, l 1 3, r 2 2],  -- مِفْعَالٌ (آلة)
  [l 24 1, r 0 3, r 1 0, r 2 0, l 3 2],  -- مِفْعَلَةٌ
  [r 0 0, r 1 3, r 1 0, l 1 3, r 2 0, l 3 2],  -- فَعَّالَةٌ
  [r 0 0, r 1 3, r 2 0, l 3 2],  -- فَعْلَةٌ
  [r 0 1, r 1 3, r 2 0, l 3 2],  -- فِعْلَةٌ
  [r 0 0, r 1 3, r 2 1, l 28 3, l 28 0, l 3 2],  -- فَعْلِيَّةٌ
  [l 24 2, r 0 3, r 1 1, r 2 2],  -- مُفْعِلٌ
  [l 24 2, r 0 3, r 1 0, r 2 2],  -- مُفْعَلٌ
  [l 24 2, r 0 0, r 1 3, r 1 1, r 2 2],  -- مُفَعِّلٌ
  [l 24 2, r 0 0, r 1 3, r 1 0, r 2 2],  -- مُفَعَّلٌ
  [l 24 2, r 0 0, l 1 3, r 1 1, r 2 2],  -- مُفَاعِلٌ
  [l 24 2, r 0 0, l 1 3, r 1 0, r 2 2],  -- مُفَاعَلٌ
  [l 24 2, l 3 0, r 0 0, r 1 3, r 1 1, r 2 2],  -- مُتَفَعِّلٌ
  [l 24 2, l 3 0, r 0 0, l 1 3, r 1 1, r 2 2],  -- مُتَفَاعِلٌ
  [l 24 2, l 25 3, r 0 0, r 1 1, r 2 2],  -- مُنْفَعِلٌ
  [l 24 2, r 0 3, l 3 0, r 1 1, r 2 2],  -- مُفْتَعِلٌ
  [l 24 2, r 0 3, l 3 0, r 1 0, r 2 2],  -- مُفْتَعَلٌ
  [l 24 2, l 12 3, l 3 0, r 0 3, r 1 1, r 2 2],  -- مُسْتَفْعِلٌ
  [l 24 2, l 12 3, l 3 0, r 0 3, r 1 0, r 2 2],  -- مُسْتَفْعَلٌ
  [r 0 0, l 1 3, r 1 1, r 2 0, l 3 2],  -- فَاعِلَةٌ
  [r 0 0, r 1 3, r 2 0, l 1 3, l 0 2],  -- فَعْلَاءُ
  [r 0 0, r 1 3, r 2 0, l 1 3],  -- فَعْلَى
  [r 0 2, r 1 3, r 2 0, l 1 3],  -- فُعْلَى
  [l 0 0, r 0 3, r 1 2, r 2 2],  -- أَفْعُلٌ
  [l 0 0, r 0 3, r 1 0, l 1 3, r 2 2],  -- أَفْعَالٌ
  [l 0 0, r 0 3, r 1 1, r 2 0, l 3 2],  -- أَفْعِلَةٌ
  [r 0 1, r 1 3, r 2 0, l 3 2],  -- فِعْلَةٌ (جمع)
  [r 0 2, r 1 3, r 2 2],  -- فُعْلٌ
  [r 0 2, r 1 2, r 2 2],  -- فُعُلٌ
  [r 0 2, r 1 0, r 2 2],  -- فُعَلٌ
  [r 0 1, r 1 0, r 2 2],  -- فِعَلٌ
  [r 0 0, r 1 0, r 2 0, l 3 2],  -- فَعَلَةٌ
  [r 0 2, r 1 0, r 2 0, l 3 2],  -- فُعَلَةٌ
  [r 0 1, r 1 0, l 1 3, r 2 2],  -- فِعَالٌ (جمع)
  [r 0 2, r 1 2, l 27 3, r 2 2],  -- فُعُولٌ (جمع)
  [r 0 2, r 1 3, r 1 0, l 1 3, r 2 2],  -- فُعَّالٌ
  [r 0 2, r 1 3, r 1 0, r 2 2],  -- فُعَّلٌ
  [r 0 1, r 1 3, r 2 0, l 1 3, l 25 2],  -- فِعْلَانٌ
  [r 0 2, r 1 3, r 2 0, l 1 3, l 25 2],  -- فُعْلَانٌ
  [r 0 2, r 1 0, r 2 0, l 1 3, l 0 2],  -- فُعَلَاءُ
  [l 0 0, r 0 3, r 1 1, r 2 0, l 1 3, l 0 2],  -- أَفْعِلَاءُ
  [l 24 0, r 0 0, l 1 3, r 1 1, r 2 2],  -- مَفَاعِلُ
  [l 24 0, r 0 0, l 1 3, r 1 1, l 28 3, r 2 2],  -- مَفَاعِيلُ
  [r 0 0, l 27 0, l 1 3, r 1 1, r 2 2],  -- فَوَاعِلُ
  [r 0 0, r 1 0, l 1 3, l 0 1, r 2 2],  -- فَعَائِلُ
  [l 0 0, r 0 0, l 1 3, r 1 1, r 2 2],  -- أَفَاعِلُ
  [l 0 0, r 0 0, l 1 3, r 1 1, l 28 3, r 2 2],  -- أَفَاعِيلُ
  [l 3 0, r 0 0, l 1 3, r 1 1, l 28 3, r 2 2],  -- تَفَاعِيلُ
  [r 0 0, r 1 0, l 1 3, r 2 1, l 28 3],  -- فَعَالِي
  [r 0 0, r 1 0, l 1 3, r 2 0, l 1 3],  -- فَعَالَى
  [r 0 2, r 1 0, l 1 3, r 2 0, l 1 3],  -- فُعَالَى
  [r 0 0, l 28 0, l 1 3, r 1 1, r 2 2],  -- فَيَاعِلُ
  [r 0 0, r 1 0, l 1 3, r 1 1, l 28 3, r 2 2]  -- فَعَاعِيلُ
]

theorem awzan_count : awzan.length = 113 := by rfl

theorem awzan_wf : ∀ t ∈ awzan, WF t := by decide

theorem awzan_mizan_licensed : ∀ t ∈ awzan, licensed (mizan t) = true := by decide

/-- كلُّ وزنٍ مودَعٍ مرخَّصٌ لكلّ أصلٍ ثلاثيّ. -/
theorem awzan_licensed (t : Template) (ht : t ∈ awzan) (r : Root) : licensed (fill t r) = true :=
  licensed_of_mizan t (awzan_mizan_licensed t ht) r

/-- وكلُّ وزنٍ مودَعٍ يردّ الأصل. -/
theorem awzan_root (t : Template) (ht : t ∈ awzan) (r : Root) :
    ∀ i, rootOf t (fill t r) i = some (r i) := rootOf_fill t (awzan_wf t ht) r

end Slge.Wazn
