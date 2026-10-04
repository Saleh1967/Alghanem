import A116

/-!
مخرجاتٌ لمطابقة Lean بالبايثون في CI:

* بلا وسيط: جدولُ الانتقال كاملًا (‎3 × 116 = 348‎ سطرًا)
  `state,carrier_index,haraka_index,next_state` بأسماء `SyllableState`.
* `counts`: ‎U(n)‎ لـ‎n = 0 … 6‎، أي عددُ السلاسل التي يقبلها النموذج، كما حسبه
  Lean من التعريف الذي بُرهِن عليه التقابل (`A116.U`).
-/

open A116

def main (args : List String) : IO Unit := do
  match args with
  | ["counts"] =>
    for n in List.range 7 do
      IO.println s!"{n},{U n}"
  | _ =>
    for q in State.all do
      for c in cells do
        IO.println s!"{q.pyName},{c.carrier.val},{c.haraka.index},{(step q c).pyName}"
