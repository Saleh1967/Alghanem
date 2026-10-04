import A116

/-!
مخرجاتٌ لمطابقة Lean بالبايثون في CI:

* بلا وسيط: جدولُ الانتقال كاملًا (‎3 × 116 = 348‎ سطرًا)
  `state,carrier_index,haraka_index,next_state` بأسماء `SyllableState`.
* `counts`: ‎U(n)‎ لـ‎n = 0 … 6‎، أي عددُ السلاسل التي يقبلها النموذج، كما حسبه
  Lean من التعريف الذي بُرهِن عليه التقابل (`A116.U`).
* `bridge-order`: ‎k,carrier,haraka‎ لـ‎k < 116‎ من `bridgeCell`، ليُطابَق بـ
  `canonical116.bridge.A116` خانةً خانة.
* `numbers`: ‎F‎ (`atomNumber`) لكلّ سلسلةٍ بطول ‎≤ 2‎ بترتيب الجسر (13,573 سطرًا).
* `pairs`: ‎P(u, r)‎ لـ‎u, r < 64‎.
* `syllables`: لكلّ سلسلةِ أنواعٍ بطول ‎1 … 8‎ (9,840 سلسلة) تقطيعُها بـ`Stages.parse`
  أو `none`، ليُطابَق بـ`mabni_stages.syllabify` سلسلةً سلسلة.
-/

open A116

namespace SyllableTable

open Stages

def allK : Nat → List (List K)
  | 0 => [[]]
  | n + 1 => (allK n).flatMap fun p => [p ++ [.cv], p ++ [.v], p ++ [.c]]

def kName : K → String
  | .cv => "CV"
  | .v => "V"
  | .c => "C"

def leadName : Lead → List String
  | .none => []
  | .C => ["C|"]
  | .V => ["V|"]
  | .VC => ["VC|"]

def sylName : Syl → String
  | .CV => "CV"
  | .CVV => "CVV"
  | .CVC => "CVC"
  | .CVVC => "CVVC"
  | .CVCC => "CVCC"

def render (k : List K) : String :=
  let key := "-".intercalate (k.map kName)
  match parse k with
  | some (l, ss) => s!"{key},{"-".intercalate (leadName l ++ ss.map sylName)}"
  | none => s!"{key},none"

end SyllableTable

def main (args : List String) : IO Unit := do
  match args with
  | ["counts"] =>
    for n in List.range 7 do
      IO.println s!"{n},{U n}"
  | ["bridge-order"] =>
    for k in List.range 116 do
      let c := Numbering.bridgeCell k
      IO.println s!"{k},{c.carrier.val},{c.haraka.index}"
  | ["numbers"] =>
    let ix := List.range 116
    IO.println s!",{Numbering.atomNumber []}"
    for i in ix do
      IO.println s!"{i},{Numbering.atomNumber [Numbering.bridgeCell i]}"
    for i in ix do
      for j in ix do
        IO.println
          s!"{i} {j},{Numbering.atomNumber [Numbering.bridgeCell i, Numbering.bridgeCell j]}"
  | ["syllables"] =>
    for n in List.range 8 do
      for k in SyllableTable.allK (n + 1) do
        IO.println (SyllableTable.render k)
  | ["pairs"] =>
    for u in List.range 64 do
      for r in List.range 64 do
        IO.println s!"{u},{r},{Numbering.pair u r}"
  | _ =>
    for q in State.all do
      for c in cells do
        IO.println s!"{q.pyName},{c.carrier.val},{c.haraka.index},{(step q c).pyName}"
