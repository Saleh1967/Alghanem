import Slge.Bridge

/-!
# الإملاء: الخاناتُ تُكتب رسمًا ثمّ تُقرأ، فتعود بعينها — لكلّ سلسلة

النظيرُ البايثونيّ: `slge.orthography.to_rasm` (الكاتب) و`to_atoms` (القارئ). وقواعدُ
الكاتب الخمسُ كما في الشيفرة:

1. **التنوين:** نونٌ ساكنةٌ **في الخاتمة** بعد خانةٍ متحرّكةٍ تُكتب تنوينًا على سابقتها.
2. **المدّة:** همزةٌ مفتوحةٌ بعدها ألفٌ ساكنة تُكتبان «آ».
3. **الهمزة:** تُكتب بكرسيّها وحركتها: أَ إِ أُ ءْ.
4. **حرفُ المدّ:** واوٌ ساكنةٌ بعد ضمّة، وياءٌ ساكنةٌ بعد كسرة، بلا علامة.
5. وما سوى ذلك: الحرفُ وعلامتُه.

والقارئُ يعكسها بلا سياق: الحرفُ العاري ساكن، والتنوينُ حركةٌ ونونٌ ساكنة، والمدّةُ
همزةٌ مفتوحةٌ وألفٌ ساكنة.

## ما يُبرهَن

`read_write`: لكلّ سلسلةِ خاناتٍ `w` ولأيّ سابقٍ: ‎read (write prev w) = some w‎.
فالكتابةُ متباينة (`write_injective`)، ولا تضيع خانةٌ في الرسم.

والرسمُ هنا **رموزٌ مجرّدة** (`G`) لا يونيكود: الحرفُ والعلامةُ والتنوينُ وكرسيُّ الهمزة والمدّة.
ومطابقةُ هذه الرموز بمحارف اليونيكود التي يكتبها البايثون يفحصها
`tests/test_conformance.py::test_rasm_matches_lean` على كلّ سلسلةٍ بطول ‎≤ 2‎.

## ما لا يُبرهَن

أنّ هذه القواعدَ هي الإملاءُ العربيّ. هي القواعدُ المعلنةُ في الشيفرة، والبرهانُ عن
اتّساقها (الكتابةُ تُقرأ) لا عن صوابها.
-/

namespace Slge.Rasm

/-- رموزُ الرسم المجرّدة. -/
inductive G where
  | letter (l : Fin 29)
  | mark (h : Fin 4)
  | tanwin (v : Fin 4)
  | hamza (h : Fin 4)
  | hamzaTanwin (v : Fin 4)
  | madda
  deriving DecidableEq, Repr

/-- مواضعُ الحروف في أبجديّة SLGE: ء ٠، ا ١، ن ٢٥، و ٢٧، ي ٢٨. -/
def hamzaIdx : Fin 29 := 0
def alifIdx : Fin 29 := 1
def nunIdx : Fin 29 := 25
def wawIdx : Fin 29 := 27
def yaIdx : Fin 29 := 28

/-- الحالات: فتح ٠، كسر ١، ضم ٢، سكون ٣. -/
def sukun : Fin 4 := 3

def nunSukun : SCell := ⟨nunIdx, sukun⟩
def alifSukun : SCell := ⟨alifIdx, sukun⟩
def hamzaFatha : SCell := ⟨hamzaIdx, 0⟩

/-- أيكتب حرفُ المدّ عاريًا؟ واوٌ ساكنةٌ بعد ضمّ، أو ياءٌ ساكنةٌ بعد كسر. -/
def bareMadd (prev : Option (Fin 4)) (c : SCell) : Bool :=
  c.state = sukun && ((c.carrier = wawIdx && prev = some 2) || (c.carrier = yaIdx && prev = some 1))

/-- رسمُ خانةٍ واحدةٍ في غير التنوين والمدّة. -/
def single (prev : Option (Fin 4)) (c : SCell) : List G :=
  if c.carrier = hamzaIdx then [.hamza c.state]
  else if bareMadd prev c then [.letter c.carrier]
  else [.letter c.carrier, .mark c.state]

/-- رسمُ خانةٍ متحرّكةٍ تليها نونُ التنوين. -/
def withTanwin (c : SCell) : List G :=
  if c.carrier = hamzaIdx then [.hamzaTanwin c.state] else [.letter c.carrier, .tanwin c.state]

/-- الكاتب. `prev` حالةُ الخانة السابقة إن وُجدت. -/
def write : Option (Fin 4) → List SCell → List G
  | _, [] => []
  | prev, [c] => single prev c
  | prev, c :: a :: rest =>
    if c = hamzaFatha && a = alifSukun then
      .madda :: write (some sukun) rest
    else if c.state != sukun && a = nunSukun && rest = [] then
      withTanwin c
    else
      single prev c ++ write (some c.state) (a :: rest)

/-- القارئ: بلا سياق. -/
def read : List G → Option (List SCell)
  | [] => some []
  | .madda :: gs => (read gs).map fun w => hamzaFatha :: alifSukun :: w
  | .hamza h :: gs => (read gs).map fun w => ⟨hamzaIdx, h⟩ :: w
  | .hamzaTanwin v :: gs => (read gs).map fun w => ⟨hamzaIdx, v⟩ :: nunSukun :: w
  | .letter l :: .mark h :: gs => (read gs).map fun w => ⟨l, h⟩ :: w
  | .letter l :: .tanwin v :: gs => (read gs).map fun w => ⟨l, v⟩ :: nunSukun :: w
  | .letter l :: gs => (read gs).map fun w => ⟨l, sukun⟩ :: w
  | .mark _ :: _ => none
  | .tanwin _ :: _ => none

/-- لا يبدأ رسمٌ بعلامةٍ ولا بتنوين؛ فالحرفُ العاري لا يلتبس بما بعده. -/
def headOK : List G → Prop
  | .mark _ :: _ => False
  | .tanwin _ :: _ => False
  | _ => True

theorem headOK_single (prev : Option (Fin 4)) (c : SCell) (gs : List G) :
    headOK (single prev c ++ gs) := by
  unfold single
  split <;> (try split) <;> simp [headOK]

theorem headOK_withTanwin (c : SCell) : headOK (withTanwin c) := by
  unfold withTanwin; split <;> simp [headOK]

theorem headOK_write : ∀ (prev : Option (Fin 4)) (w : List SCell), headOK (write prev w)
  | _, [] => by simp [write, headOK]
  | prev, [c] => by
    rw [write, show single prev c = single prev c ++ [] from (List.append_nil _).symm]
    exact headOK_single prev c []
  | prev, c :: a :: rest => by
    rw [write]
    split
    · simp [headOK]
    · split
      · exact headOK_withTanwin c
      · exact headOK_single prev c _

theorem read_single_append (prev : Option (Fin 4)) (c : SCell) (gs : List G) (hg : headOK gs) :
    read (single prev c ++ gs) = (read gs).map fun w => c :: w := by
  unfold single
  by_cases hh : c.carrier = hamzaIdx
  · simp only [hh, ↓reduceIte, List.cons_append, List.nil_append, read]
    cases c; simp_all
  · by_cases hb : bareMadd prev c = true
    · simp only [hh, hb, ↓reduceIte, List.cons_append, List.nil_append]
      have hs : c.state = sukun := by
        unfold bareMadd at hb; simp at hb; exact hb.1
      cases gs with
      | nil => cases c; simp_all [read, sukun]
      | cons g gs' =>
        cases g <;> cases c <;> simp_all [read, sukun, headOK]
    · simp only [hh, hb, Bool.false_eq_true, ↓reduceIte, List.cons_append, List.nil_append, read]

theorem read_withTanwin (c : SCell) : read (withTanwin c) = some [c, nunSukun] := by
  unfold withTanwin
  by_cases hh : c.carrier = hamzaIdx
  · simp only [hh, ↓reduceIte, read]; cases c; simp_all
  · simp only [hh, ↓reduceIte, read]; cases c; rfl

/-- **ما كُتب يُقرأ بعينه**، لكلّ سلسلةٍ ولأيّ سابق. -/
theorem read_write : ∀ (prev : Option (Fin 4)) (w : List SCell), read (write prev w) = some w
  | _, [] => by simp [write, read]
  | prev, [c] => by
    rw [write, show single prev c = single prev c ++ [] from (List.append_nil _).symm,
      read_single_append prev c [] (by simp [headOK])]
    rfl
  | prev, c :: a :: rest => by
    rw [write]
    split
    · rename_i h
      simp only [Bool.and_eq_true, decide_eq_true_eq] at h
      obtain ⟨hc, ha⟩ := h
      subst hc; subst ha
      simp [read, read_write (some sukun) rest]
    · split
      · rename_i h
        simp only [Bool.and_eq_true, bne_iff_ne, ne_eq, decide_eq_true_eq] at h
        obtain ⟨⟨-, ha⟩, hr⟩ := h
        subst ha; subst hr
        exact read_withTanwin c
      · rw [read_single_append prev c _ (headOK_write _ _), read_write (some c.state) (a :: rest)]
        rfl

theorem write_injective (prev : Option (Fin 4)) {w w' : List SCell}
    (h : write prev w = write prev w') : w = w' := by
  have := read_write prev w
  rw [h, read_write] at this
  exact (Option.some.inj this).symm

end Slge.Rasm
