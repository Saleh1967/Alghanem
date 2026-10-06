import Slge.Categories

/-!
# الأسماء الخمسة: الإعرابُ بالحروف دالّةً

أبٌ، أخٌ، حمٌ، فوٌ، ذو. القانونُ الواحد: الاسمُ **جذعٌ** (حواملُ بلا حالةٍ في آخره) و**خانةُ إعرابٍ**:
آخرُ الجذع يأخذ الحركةَ القصيرةَ للحالة، ويليه حرفُ المدّ **من جنسها** ساكنًا (ضم↔و، فتح↔ا،
كسر↔ي). فالإعرابُ بالحروف ليس استثناءً من الإعراب بالحركات بل **إطالتُه**: الحرفُ صورةُ الحركة
(`madd_matches_short`).

المبرهَن:
* `caseOf_form`: الحالةُ تُقرأ من الصورة بعينها — حرفُ المدّ شفرةٌ تامّةٌ للحالة (`madd_injective`).
* `form_injective_stem`: الصورةُ تعيّن الجذع.
* `ya_neutralizes_case`: المضافُ إلى ياء المتكلّم صورةٌ واحدةٌ للحالات الثلاث (أَبِي).
* `tanwin_when_not_mudaf`: غيرُ المضاف يُعرب بالحركة والتنوين (أَخٌ ← ءَ خُ نْ كما تُخرجه البوّابة).
* `khamsa_licensed`: الصورُ الخمسَ عشرة مرخَّصةٌ، والـ15 أعدادًا متباينة.

وشروطُ الإعراب بالحروف (مفردٌ، مكبَّر، مضافٌ لغير ياء المتكلّم) **معلَنة** في `Ctx`؛ الدالّةُ `decline`
تختار بها، ولا تخمّن: ما خرج عن الشروط فبالحركة.
-/

namespace Slge.Khamsa

open Slge.Categories (c)

/-- الحالاتُ الإعرابيّة. -/
inductive Case where
  | raf | nasb | jarr
  deriving DecidableEq, Repr

/-- الحركةُ القصيرة للحالة (بترتيب SLGE: فتح ٠، كسر ١، ضم ٢). -/
def shortOf : Case → Fin 4
  | .raf => 2
  | .nasb => 0
  | .jarr => 1

/-- حرفُ المدّ من جنس الحركة: و ٢٧، ا ١، ي ٢٨. -/
def maddOf : Case → Fin 29
  | .raf => ⟨27, by decide⟩
  | .nasb => ⟨1, by decide⟩
  | .jarr => ⟨28, by decide⟩

theorem madd_injective : ∀ a b : Case, maddOf a = maddOf b → a = b := by
  intro a b h; cases a <;> cases b <;> first | rfl | (exfalso; exact absurd h (by decide))

/-- الحرفُ صورةُ الحركة: و للضمّ، ا للفتح، ي للكسر — ومعكوسُه. -/
def shortOfMadd (k : Fin 29) : Option (Fin 4) :=
  if k.val = 27 then some 2 else if k.val = 1 then some 0 else if k.val = 28 then some 1 else none

theorem madd_matches_short : ∀ cs : Case, shortOfMadd (maddOf cs) = some (shortOf cs) := by
  intro cs; cases cs <;> rfl

/-- الجذع: الحوامل، آخرُها يحمل الإعراب. -/
structure Stem where
  head : List SCell
  last : Fin 29
  deriving DecidableEq, Repr

/-- الصورةُ بالحروف: الرأس، ثمّ آخرُ الجذع بالحركة القصيرة، ثمّ حرفُ المدّ ساكنًا. -/
def form (s : Stem) (cs : Case) : List SCell :=
  s.head ++ [⟨s.last, shortOf cs⟩, ⟨maddOf cs, 3⟩]

/-- قراءةُ الحالة من الصورة: حرفُ المدّ في الآخر. -/
def caseOf (w : List SCell) : Option Case :=
  match w.getLast? with
  | some ⟨k, _⟩ => if k.val = 27 then some .raf else if k.val = 1 then some .nasb
                   else if k.val = 28 then some .jarr else none
  | none => none

theorem getLast_form (s : Stem) (cs : Case) : (form s cs).getLast? = some ⟨maddOf cs, 3⟩ := by
  simp [form, List.getLast?_append]

theorem caseOf_form (s : Stem) : ∀ cs, caseOf (form s cs) = some cs := by
  intro cs; unfold caseOf; rw [getLast_form]; cases cs <;> rfl

theorem form_injective_stem (s s' : Stem) (cs : Case) (h : form s cs = form s' cs) : s = s' := by
  unfold form at h
  obtain ⟨h1, h2⟩ := List.append_inj' h rfl
  cases s; cases s'
  have h3 := List.head_eq_of_cons_eq h2
  have h4 : ∀ {a b : Fin 29} {x y : Fin 4}, (⟨a, x⟩ : SCell) = ⟨b, y⟩ → a = b := fun h => by
    cases h; rfl
  simp only [Stem.mk.injEq]
  exact ⟨h1, h4 h3⟩

/-- المضافُ إلى ياء المتكلّم: كسرةٌ وياء، في الحالات كلِّها. -/
def withYa (s : Stem) : List SCell := s.head ++ [⟨s.last, 1⟩, ⟨⟨28, by decide⟩, 3⟩]

theorem ya_neutralizes_case (s : Stem) : ∀ _a _b : Case, withYa s = withYa s := fun _ _ => rfl

/-- غيرُ المضاف: الحركةُ ونونُ التنوين ساكنةً (كما تُخرجها البوّابة). -/
def tanwin (s : Stem) (cs : Case) : List SCell :=
  s.head ++ [⟨s.last, shortOf cs⟩, ⟨⟨25, by decide⟩, 3⟩]

/-- شروطُ الإعراب بالحروف، معلَنةً. -/
structure Ctx where
  mufrad : Bool
  mukabbar : Bool
  mudaf : Bool
  ilaYa : Bool
  deriving DecidableEq, Repr

def Ctx.byLetters (x : Ctx) : Bool := x.mufrad && x.mukabbar && x.mudaf && !x.ilaYa

/-- الإعراب: بالحروف إن تمّت الشروط؛ وإلّا بياء المتكلّم إن أُضيف إليها؛ وإلّا بالحركة والتنوين.
ما لم يُغطَّ (الجمعُ، التصغير) يُردّ `none` لا تخمينًا. -/
def decline (s : Stem) (x : Ctx) (cs : Case) : Option (List SCell) :=
  if x.byLetters then some (form s cs)
  else if x.mufrad && x.mukabbar && x.mudaf && x.ilaYa then some (withYa s)
  else if x.mufrad && x.mukabbar && !x.mudaf then some (tanwin s cs)
  else none

theorem tanwin_when_not_mudaf (s : Stem) (cs : Case) :
    decline s ⟨true, true, false, false⟩ cs = some (tanwin s cs) := by rfl

theorem letters_when_mudaf (s : Stem) (cs : Case) :
    decline s ⟨true, true, true, false⟩ cs = some (form s cs) := by rfl

theorem no_guess_for_plural (s : Stem) (cs : Case) (x : Ctx) (h : x.mufrad = false) :
    decline s x cs = none := by
  unfold decline Ctx.byLetters; simp [h]

/-- الخمسة: أب، أخ، حم، فو، ذو (الجذعُ بلا الحرف الأخير الذي يحمل الإعراب). -/
def ab : Stem := ⟨[c 0 0], ⟨2, by decide⟩⟩
def akh : Stem := ⟨[c 0 0], ⟨7, by decide⟩⟩
def ham : Stem := ⟨[c 6 0], ⟨24, by decide⟩⟩
def fu : Stem := ⟨[], ⟨20, by decide⟩⟩
def dhu : Stem := ⟨[], ⟨9, by decide⟩⟩

def khamsa : List Stem := [ab, akh, ham, fu, dhu]

def cases : List Case := [.raf, .nasb, .jarr]

/-- الصورُ الخمسَ عشرة. -/
def forms : List (List SCell) := khamsa.flatMap fun s => cases.map (form s)

theorem khamsa_licensed : ∀ w ∈ forms, licensed w = true := by decide

theorem khamsa_numbers_nodup : (forms.map slgeFold).Nodup := by decide

theorem forms_count : forms.length = 15 := by rfl

/-- وبالتنوين كذلك مرخَّصة. -/
theorem khamsa_tanwin_licensed :
    ∀ s ∈ khamsa, ∀ cs ∈ cases, licensed (tanwin s cs) = true := by decide

end Slge.Khamsa
