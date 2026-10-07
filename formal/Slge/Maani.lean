import Slge.MaaniTable
import Slge.Huruf
import Slge.Zuruf
import Slge.Zaman

/-!
# معاني الحروف: تعدّدُ معاني الحرف الواحد مرتَّبًا بالقرينة لا مختارًا

الحرفُ «ما دلّ على معنًى في غيره» (الشخصيّة ج3، مبحث الحرف): معناه دالّةٌ في متعلَّقه، ولحرفٍ واحدٍ معانٍ
(«مِن» لابتداء الغاية والتبعيض وبيان الجنس وزائدة). الجدولُ `Maani.table` منقولٌ من المصدر بترتيب ذكره
(`tools/deposit_maani.py`، مودَعٌ مختوم)، لا يُحرَّر ولا يُختار منه.

المبرهَن هنا على الجدول:
* **الربطُ بالجدول الموحَّد**: كلُّ فهرسٍ فيه فهرسٌ في `Huruf.table` (`indices_in_table`)؛ وحروفُ الجرّ التي لا
  معنى لها في المصدر ثلاثةٌ بأرقامها: خلا وعدا وحاشا، ومدخلُها نثرٌ عن الاستثناء (`jarr_uncovered`).
* **المتعدّد** بأرقامه: تسعةُ أحرف لها معنيان فأكثر (`multi_eq`).
* **الأصلُ أوّلًا**: حيث ذكر المصدرُ معنى غايةٍ أو ظرفيّةٍ لحرفٍ ذكره أوّلَ معانيه (`ghaya_first_in_source`) —
  فقرينةُ الظرف بعد الحرف لا تغيّر ترتيبَ المصدر بل تثبّته.
* **الترتيبُ لا يُسقط معنًى**: `rank` بالقرينتين (ظرفٌ بعد الحرف، نفيٌ قبله) يحفظ العضويّةَ والعدد
  (`mem_rank`، `length_rank`)؛ وبلا قرينةٍ يعيد ترتيبَ المصدر بعينه (`rank_none`).

القرينتان **معلَنتان** لا مبرهنتان: الظرفُ بعد الحرف من جدولَي `Zuruf`/`Zaman` المبرهَنَين ترخيصًا، والنفيُ قبله
يقدّم «زائدة» تعميمًا لشاهد المصدر الوحيد («ما جاءني من أحد») — ويُقاس أثرُهما في `MAANI_INDEX.md`.
-/

namespace Slge.Maani

def sensesOf (h : Nat) : List Sense :=
  match table.find? (fun p => p.1 == h) with
  | some p => p.2
  | none => []

theorem indices_in_table : table.all (fun p => p.1 < Huruf.table.length) = true := by decide

/-- فهارسُ حروف الجرّ في الجدول الموحَّد. -/
def jarrIdx : List Nat :=
  (List.range Huruf.table.length).filter fun i =>
    match Huruf.table[i]? with
    | some h => h.amal == .jarr
    | none => false

set_option maxRecDepth 100000 in
/-- حروفُ الجرّ بلا معنًى في المصدر: خلا (13) وعدا (14) وحاشا (15) — مدخلُها نثرٌ عن الاستثناء. -/
theorem jarr_uncovered : jarrIdx.filter (fun i => sensesOf i == []) = [13, 14, 15] := by decide

/-- الحروفُ ذاتُ المعنيين فأكثر، بأرقامها. -/
def multi : List Nat := (table.filter fun p => p.2.length ≥ 2).map (·.1)

theorem multi_eq : multi = [0, 1, 5, 6, 9, 10, 52, 53, 61] := by decide

/-- معاني الغاية والظرفيّة: ما يقدّمه ظرفُ مكانٍ أو زمانٍ بعد الحرف. -/
def ghaya : Sense → Bool
  | .ibtidaGhaya | .intihaGhaya | .zarfiyya | .ibtidaGhayaZaman => true
  | _ => false

/-- حيث ذكر المصدرُ معنى غايةٍ لحرفٍ ذكره أوّلَ معانيه: الأصلُ أوّلًا. -/
theorem ghaya_first_in_source :
    table.all (fun p => !(p.2.any ghaya) || ghaya (p.2.headD .zaida)) = true := by decide

/-- ظرفُ مكانٍ أو زمانٍ من الجدولَين المبرهَنَين (بصورهما المضافة والمجرورة والمقطوعة). -/
def isZarf (w : List SCell) : Bool := Zuruf.forms.contains w || Zaman.forms.contains w

structure Clue where
  nafyBefore : Bool := false
  zarfAfter : Bool := false
  deriving DecidableEq, Repr

def split (p : Sense → Bool) (ss : List Sense) : List Sense :=
  ss.filter p ++ ss.filter (fun s => !p s)

/-- الترتيبُ بالقرينة: ظرفٌ بعده يقدّم الغاية؛ وإلّا نفيٌ قبله يقدّم «زائدة»؛ وإلّا ترتيبُ المصدر. -/
def rank (q : Clue) (ss : List Sense) : List Sense :=
  if q.zarfAfter then split ghaya ss
  else if q.nafyBefore then split (fun s => s == .zaida) ss
  else ss

theorem mem_split (p : Sense → Bool) (ss : List Sense) (s : Sense) : s ∈ split p ss ↔ s ∈ ss := by
  simp only [split, List.mem_append, List.mem_filter]
  constructor
  · rintro (⟨h, _⟩ | ⟨h, _⟩) <;> exact h
  · intro h
    by_cases hp : p s = true
    · exact Or.inl ⟨h, hp⟩
    · exact Or.inr ⟨h, by simpa using hp⟩

theorem length_split (p : Sense → Bool) : ∀ ss : List Sense, (split p ss).length = ss.length
  | [] => rfl
  | s :: ss => by
    have ih := length_split p ss
    simp only [split, List.length_append] at ih ⊢
    by_cases hp : p s = true <;> simp [hp] <;> omega

theorem mem_rank (q : Clue) (ss : List Sense) (s : Sense) : s ∈ rank q ss ↔ s ∈ ss := by
  unfold rank
  by_cases hz : q.zarfAfter = true <;> by_cases hn : q.nafyBefore = true <;> simp [hz, hn, mem_split]

theorem length_rank (q : Clue) (ss : List Sense) : (rank q ss).length = ss.length := by
  unfold rank
  by_cases hz : q.zarfAfter = true <;> by_cases hn : q.nafyBefore = true <;> simp [hz, hn, length_split]

theorem rank_none (ss : List Sense) : rank {} ss = ss := rfl

/-- شواهد: «مِن» بمعانيه الأربعة بترتيب المصدر؛ النفيُ قبلها يقدّم «زائدة»؛ الظرفُ بعد «في» يثبّت الظرفيّة؛
وخلا بلا معنًى. -/
theorem witnesses :
    sensesOf 5 = [.ibtidaGhaya, .tabid, .bayanJins, .zaida] ∧
    rank {nafyBefore := true} (sensesOf 5) = [.zaida, .ibtidaGhaya, .tabid, .bayanJins] ∧
    rank {zarfAfter := true} (sensesOf 9) = [.zarfiyya, .ala, .tajawwuz] ∧
    rank {nafyBefore := true, zarfAfter := true} (sensesOf 5) = sensesOf 5 ∧
    sensesOf 13 = [] := by decide

end Slge.Maani
