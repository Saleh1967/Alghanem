import A116.PauseCount

/-!
# «الغلاف» الثنائيّ والترخيصُ الثلاثيّ: العددُ واحدٌ والأعيانُ لا (ADR ١١)

الغلافُ كما ورد في النقاش (مقترَحٌ خارجيّ، لا مودَع): سلاسلُ على ‎{C، V}‎ بطول 2..12، تبدأ بـC وتنتهي بـC ولا
تتجاور فيها V وV. وقراءتُها على الأصناف الثلاثة: ‎C‎ تليها ‎V‎ متحرّكٌ (`cv`)، و‎C‎ لا تليها ‎V‎ مدٌّ (`v`) أو
ساكنٌ (`c`) — فالغلافُ أعمى عن الفرق بينهما كما الثنائيُّ أعمى عن المدّ (`binary_is_blind_to_madd`).

* `envelope_375`: عددُ الغلاف 375 — وهو مجموعُ المرخَّص وقفًا بالأوزان نفسها (`pause_count_375`)؛
* `envelope_licensed_75`: ومنه **75** فقط لها قراءةٌ مرخَّصةٌ وقفًا، و59 وصلًا (`envelope_licensed_continue_59`).

فالتوافقُ في العدد لا في الأعيان. البرهانُ حسابٌ على تعريف الغلاف المذكور بعينه (`decide +kernel`)،
مبرهنٌ على هذه الأطوال لا لكلّ طول. وهو عن تعريفٍ لا عن اللغة: الغلافُ اقتراحٌ يُقاس، لا معلومةٌ سابقة.
-/

namespace A116.Ternary

open A116.Stages K

/-- كلُّ السلاسل بطول `n` (‎true = C‎، ‎false = V‎). -/
def strs : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 => (strs n).map (true :: ·) ++ (strs n).map (false :: ·)

def noVV : List Bool → Bool
  | false :: false :: _ => false
  | _ :: t => noVV t
  | [] => true

/-- شرطُ الغلاف: يبدأ بـC، وينتهي بـC، ولا ‎VV‎. -/
def envOk (s : List Bool) : Bool := s.head? == some true && s.getLast? == some true && noVV s

def envelope (n : Nat) : List (List Bool) := (strs n).filter envOk

/-- خياراتُ كلّ موضع: ‎CV‎ متحرّك، و‎C‎ وحدَها مدٌّ أو ساكن، و‎V‎ بلا حاملٍ لا قراءةَ لها. -/
def choices : List Bool → List (List K)
  | true :: false :: t => [cv] :: choices t
  | true :: t => [v, c] :: choices t
  | false :: t => [] :: choices t
  | [] => []

def readings : List (List K) → List (List K)
  | [] => [[]]
  | o :: t => o.flatMap fun x => (readings t).map (x :: ·)

def pauseSome (s : List Bool) : Bool := (readings (choices s)).any pauseB
def continueSome (s : List Bool) : Bool := (readings (choices s)).any continueB

def total (f : List Bool → Bool) : Nat :=
  ((List.range 11).map fun i => ((envelope (i + 2)).filter f).length).sum

set_option maxRecDepth 100000 in
theorem envelope_375 : total (fun _ => true) = 375 := by decide +kernel

set_option maxRecDepth 100000 in
theorem envelope_licensed_75 : total pauseSome = 75 := by decide +kernel

set_option maxRecDepth 100000 in
theorem envelope_licensed_continue_59 : total continueSome = 59 := by decide +kernel

end A116.Ternary
