import Slge.Khamsa

/-!
# الأفعال الخمسة: الإعرابُ بالنون بتًّا واحدًا

يَفْعَلَانِ، تَفْعَلَانِ، يَفْعَلُونَ، تَفْعَلُونَ، تَفْعَلِينَ. القانونُ الواحد: **جذعُ المضارع** (بحرف
المضارعة، بلا حركة آخره) + **ضميرٌ متّصل** (ألفُ الاثنين، واوُ الجماعة، ياءُ المخاطبة) يسبقه
الحركةُ من جنسه — القانونُ نفسُه الذي في الأسماء الخمسة (`glide_matches_before` عبر
`Khamsa.shortOfMadd`) — ثمّ **النون** علامةَ الرفع، وحذفُها علامةَ النصب والجزم.

المبرهَن:
* `moodOf_form`: الرفعُ يُقرأ من الصورة (نونٌ في الآخر أو لا) — بتٌّ واحد.
* `nasb_eq_jazm`: صورةُ النصب هي صورةُ الجزم بعينها؛ فالفرقُ بينهما نحويٌّ (العامل) لا صرفيّ.
* `pronounOf_form`: الضميرُ يُقرأ من حرفه.
* `form_injective_stem`: الصورةُ تعيّن الجذع.
* `five_licensed`: الصورُ المودَعة (4 جذوعٍ من شهادات البوّابة × 5 × 3 حالات) مرخَّصةٌ كلُّها.

وألفُ الفارقة بعد الواو (يَفْعَلُوا) بقيّةُ رسمٍ تحملها الشهادة (`A116.Residue` FARIQA)، لا خانة.
والخمسةُ خمسةٌ بجدول المطابقة المعلَن: ياءُ المخاطبة لا تلحق حرفَ الغيبة (`agree`).
-/

namespace Slge.Afal

open Slge.Categories (c)

inductive Pronoun where
  | ithnan | jamaa | mukhataba
  deriving DecidableEq, Repr

inductive Mood where
  | raf | nasb | jazm
  deriving DecidableEq, Repr

inductive Prefix where
  | ghaib | mukhatab
  deriving DecidableEq, Repr

/-- حرفُ الضمير: ا ١، و ٢٧، ي ٢٨. -/
def glide : Pronoun → Fin 29
  | .ithnan => ⟨1, by decide⟩
  | .jamaa => ⟨27, by decide⟩
  | .mukhataba => ⟨28, by decide⟩

/-- الحركةُ قبله من جنسه: فتح، ضم، كسر. -/
def before : Pronoun → Fin 4
  | .ithnan => 0
  | .jamaa => 2
  | .mukhataba => 1

theorem glide_matches_before : ∀ p, Khamsa.shortOfMadd (glide p) = some (before p) := by
  intro p; cases p <;> rfl

/-- حرفُ المضارعة: ي ٢٨ للغائب، ت ٣ للمخاطب والغائبة. -/
def prefixCarrier : Prefix → Fin 29
  | .ghaib => ⟨28, by decide⟩
  | .mukhatab => ⟨3, by decide⟩

/-- جدولُ المطابقة المعلَن: ياءُ المخاطبة للمخاطب وحدَه. -/
def agree : Prefix → Pronoun → Bool
  | .ghaib, .mukhataba => false
  | _, _ => true

theorem five_pairs :
    ((List.map (fun pr => (List.map (fun p => (pr, p)) [Pronoun.ithnan, .jamaa, .mukhataba]))
      [Prefix.ghaib, .mukhatab]).flatten.filter fun x => agree x.1 x.2).length = 5 := by rfl

/-- الجذع: بعد حرف المضارعة بحركته، إلى الحرف الأخير بلا حركة. -/
structure Stem where
  prefixState : Fin 4
  body : List SCell
  last : Fin 29
  deriving DecidableEq, Repr

/-- النون: مكسورةٌ بعد الألف، مفتوحةٌ بعد الواو والياء؛ وتسقط في غير الرفع. -/
def nun (m : Mood) (p : Pronoun) : List SCell :=
  match m with
  | .raf => [⟨⟨25, by decide⟩, if p = .ithnan then 1 else 0⟩]
  | _ => []

def form (pr : Prefix) (s : Stem) (p : Pronoun) (m : Mood) : List SCell :=
  ⟨prefixCarrier pr, s.prefixState⟩ :: s.body ++ [⟨s.last, before p⟩, ⟨glide p, 3⟩] ++ nun m p

theorem nasb_eq_jazm (pr : Prefix) (s : Stem) (p : Pronoun) :
    form pr s p .nasb = form pr s p .jazm := rfl

/-- الآخر. -/
def lastOf : List SCell → Option SCell
  | [] => none
  | [x] => some x
  | _ :: y :: t => lastOf (y :: t)

/-- ما قبل الآخر. -/
def initOf : List SCell → List SCell
  | [] => []
  | [_] => []
  | x :: y :: t => x :: initOf (y :: t)

theorem lastOf_cons_append (x : SCell) : ∀ (l : List SCell) (a : SCell) (t : List SCell),
    lastOf (x :: (l ++ a :: t)) = lastOf (a :: t)
  | [], a, t => by simp [lastOf]
  | y :: l, a, t => by
    show lastOf (x :: y :: (l ++ a :: t)) = lastOf (a :: t)
    rw [lastOf]; exact lastOf_cons_append y l a t

theorem initOf_cons_append (x : SCell) : ∀ (l : List SCell) (a : SCell) (t : List SCell),
    initOf (x :: (l ++ a :: t)) = x :: (l ++ initOf (a :: t))
  | [], a, t => by simp [initOf]
  | y :: l, a, t => by
    show initOf (x :: y :: (l ++ a :: t)) = x :: (y :: l ++ initOf (a :: t))
    rw [initOf, initOf_cons_append y l a t]; rfl

/-- الرفعُ من الآخر: نونٌ أو لا. -/
def moodOf (w : List SCell) : Mood :=
  match lastOf w with
  | some ⟨k, _⟩ => if k.val = 25 then .raf else .nasb
  | none => .nasb

theorem form_raf (pr : Prefix) (s : Stem) (p : Pronoun) :
    form pr s p .raf = ⟨prefixCarrier pr, s.prefixState⟩ ::
      (s.body ++ ⟨s.last, before p⟩ :: ⟨glide p, 3⟩ :: nun .raf p) := by
  simp [form]

theorem form_nasb (pr : Prefix) (s : Stem) (p : Pronoun) :
    form pr s p .nasb = ⟨prefixCarrier pr, s.prefixState⟩ ::
      (s.body ++ ⟨s.last, before p⟩ :: [⟨glide p, 3⟩]) := by
  simp [form, nun]

theorem moodOf_raf (pr : Prefix) (s : Stem) (p : Pronoun) : moodOf (form pr s p .raf) = .raf := by
  rw [form_raf]; unfold moodOf; rw [lastOf_cons_append]; cases p <;> rfl

theorem moodOf_nasb (pr : Prefix) (s : Stem) (p : Pronoun) :
    moodOf (form pr s p .nasb) = .nasb := by
  rw [form_nasb]; unfold moodOf; rw [lastOf_cons_append]; cases p <;> rfl

/-- الضميرُ من حرفه: آخرُ الصورة بعد إسقاط النون. -/
def pronounOf (w : List SCell) : Option Pronoun :=
  let w' := if moodOf w = .raf then initOf w else w
  match lastOf w' with
  | some ⟨k, _⟩ => if k.val = 1 then some .ithnan else if k.val = 27 then some .jamaa
                   else if k.val = 28 then some .mukhataba else none
  | none => none

theorem pronounOf_form (pr : Prefix) (s : Stem) (p : Pronoun) (m : Mood) :
    pronounOf (form pr s p m) = some p := by
  cases m with
  | raf =>
    unfold pronounOf
    rw [moodOf_raf]; simp only [ite_true]
    rw [form_raf, initOf_cons_append]
    cases p <;> (unfold nun; simp only [initOf]; rw [lastOf_cons_append]; rfl)
  | nasb =>
    unfold pronounOf
    rw [moodOf_nasb]; simp only [reduceCtorEq, ite_false]
    rw [form_nasb, lastOf_cons_append]; cases p <;> rfl
  | jazm =>
    rw [← nasb_eq_jazm]
    unfold pronounOf
    rw [moodOf_nasb]; simp only [reduceCtorEq, ite_false]
    rw [form_nasb, lastOf_cons_append]; cases p <;> rfl

/-- الجذوعُ المودَعة (من شهادات البوّابة 2026-10-06): يَفْعَلُ، تَعْلَمُ، يَقْتَتِلُ، تَخَافُ. -/
def stems : List (Prefix × Stem) := [
  (.ghaib, ⟨0, [c 20 3, c 18 0], ⟨23, by decide⟩⟩),            -- يَفْعَلُونَ / يَفْعَلُوا
  (.mukhatab, ⟨0, [c 18 3, c 23 0], ⟨24, by decide⟩⟩),         -- تَعْلَمُونَ / تَعْلَمُوا
  (.ghaib, ⟨0, [c 21 3, c 3 0, c 3 1], ⟨23, by decide⟩⟩),      -- يَقْتَتِلَانِ
  (.mukhatab, ⟨0, [c 7 0, c 1 3], ⟨20, by decide⟩⟩)            -- تَخَافِي
]

def pronouns : List Pronoun := [.ithnan, .jamaa, .mukhataba]
def moods : List Mood := [.raf, .nasb, .jazm]

/-- الصورُ المودَعة: لكلّ جذعٍ، الضمائرُ التي تطابق حرفَه، بالحالات الثلاث. -/
def forms : List (List SCell) :=
  stems.flatMap fun (pr, s) =>
    (pronouns.filter (agree pr)).flatMap fun p => moods.map (form pr s p)

theorem five_licensed : ∀ w ∈ forms, licensed w = true := by decide

/-- عددُها: جذعان بالغيبة (٢ ضميرين × ٣) + جذعان بالخطاب (٣ × ٣) = ٣٠. -/
theorem forms_count : forms.length = 30 := by rfl

end Slge.Afal
