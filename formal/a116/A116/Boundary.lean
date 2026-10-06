import A116.Pause

/-!
# قانونُ الحدّ: الابتداءُ والوصلُ والوقف

الكلمةُ المرخَّصةُ (`Admissible`) نموذجُ **وصل**؛ وللحدّين قانونان من سيبويه:
**«لا يُبتدأ بساكن، ولا يُوقف على متحرّك»**. وهذه الوحدةُ تجعلهما مبرهناتٍ على الخانات، وتضيف
الوصلَ بين كلمتين وهمزةَ الوصل.

## السياق
`Entry = start | joined` و`Exit = continue | pause` — عينُ ما تحمله `gate.contextual.Context`.

## ما يُبرهَن

* `no_start_with_sukun`: المرخَّصُ لا يبدأ بساكن (الابتداء) — من تعريف `Admissible`.
* `pause_ends_with_sukun`: الوقفُ يُسكِّن الآخر، ووقفُ المرخَّص مرخَّصٌ وقفًا (`Pause.pause_admissible`).
* `join_iff`: وصلُ كلمتين مرخَّصتين مرخَّصٌ **إذا وفقط إذا** كان حدُّهما جائزًا: إن انتهت الأولى بساكنٍ
  فالثانية مرخَّصةٌ كما هي، وإن انتهت بمتحرّكٍ فيكفي ألّا يتجاور ساكنان في الثانية (`Junction.admissible_append`).
* `wasl_dropped_needs_moving_left`: همزةُ الوصل تسقط في الوصل، فتصير الكلمةُ مبدوءةً بساكن (لْحَمْدُ)،
  فلا تُرخَّص إلّا موصولةً بكلمةٍ **تنتهي بمتحرّك** — وهذا هو قانونُ همزة الوصل.
* `pause_then_join_is_not_join`: الوقفُ ثمّ الوصلُ ليس وصلًا: ما وُقف عليه بساكنٍ ثمّ وُصل بكلمةٍ تبدأ
  بساكن (بعد سقوط الوصل) غيرُ مرخَّص — فالقارئُ إمّا يقف وإمّا يصل.

ولا يُبرهَن هنا أنّ `gate.contextual.project` ينفّذ هذه المشغّلات بعينها؛ ذلك ما تفحصه المطابقة.
-/

namespace A116.Boundary

open A116 A116.Junction A116.Pause

inductive Entry where | start | joined deriving DecidableEq, Repr
inductive Exit where | continue | pause deriving DecidableEq, Repr

/-- **الابتداء:** المرخَّصُ لا يبدأ بساكن. -/
theorem no_start_with_sukun {c : Cell} {w : List Cell} (h : Admissible (c :: w)) :
    c.isSukun = false := by
  obtain ⟨hhead, _⟩ := h
  simpa [HeadNotSukun] using hhead

/-- **الوقف:** مشغّلُ الوقف يُسكِّن الآخر، والناتجُ مرخَّصٌ وقفًا. -/
theorem pause_ends_with_sukun (v : List Cell) (c : Cell) (hv : v ≠ []) (h : Admissible (v ++ [c])) :
    (pause (v ++ [c])).getLast? = some ⟨c.carrier, .sukun⟩ ∧ PauseAdmissible (pause (v ++ [c])) := by
  refine ⟨?_, pause_admissible v c hv h⟩
  rw [pause_snoc]; simp

/-- **الوصل:** وصلُ ‎a‎ (المنتهية بـ‎c‎) بـ‎b‎ مرخَّصٌ ⇔ حدُّهما جائز. -/
theorem join_iff (a : List Cell) (c : Cell) (b : List Cell) (ha : Admissible (a ++ [c])) :
    Admissible ((a ++ [c]) ++ b) ↔ (if c.isSukun then Admissible b else NoAdjacentSukun b) :=
  admissible_append a c b ha

/-- إسقاطُ همزة الوصل: الخانةُ الأولى تسقط في الوصل. -/
def dropWasl : List Cell → List Cell
  | [] => []
  | _ :: t => t

/-- **همزةُ الوصل:** إن سقطت وبقيت الكلمةُ مبدوءةً بساكنٍ (لْحَمْدُ) فلا ترخيصَ لها إلّا موصولةً بما
ينتهي بمتحرّك. -/
theorem wasl_dropped_needs_moving_left (a : List Cell) (c : Cell) (h : Cell) (t : List Cell)
    (ha : Admissible (a ++ [c])) (hs : h.isSukun = true) (ht : NoAdjacentSukun (h :: t)) :
    Admissible ((a ++ [c]) ++ dropWasl (⟨h.carrier, .fatha⟩ :: h :: t)) ↔ c.isSukun = false := by
  simp only [dropWasl]
  rw [join_iff a c (h :: t) ha]
  constructor
  · intro hj
    cases hc : c.isSukun
    · rfl
    · rw [hc] at hj; simp only [↓reduceIte] at hj
      have := no_start_with_sukun hj; simp_all
  · intro hc; simp [hc, ht]

/-- **الوقفُ ثمّ الوصلُ ليس وصلًا:** ما وُقف عليه (ساكنُ الآخر) لا يُوصل بما سقطت وصلُه. -/
theorem pause_then_join_is_not_join (v : List Cell) (c : Cell) (h : Cell) (t : List Cell)
    (hs : h.isSukun = true) :
    ¬ Admissible (pause (v ++ [c]) ++ (h :: t)) := by
  rw [pause_snoc]
  intro hj
  have hpre : Admissible (v ++ [⟨c.carrier, .sukun⟩]) := admissible_prefix hj
  rw [join_iff v _ (h :: t) hpre] at hj
  simp only [Cell.isSukun, Haraka.isSukun, ↓reduceIte] at hj
  have := no_start_with_sukun hj
  simp_all

end A116.Boundary
