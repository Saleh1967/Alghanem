import A116

/-!
جدولُ الانتقال كاملًا (‎3 × 116 = 348‎ سطرًا) لمطابقته بالبايثون في CI:
`state,carrier_index,haraka_index,next_state` بأسماء `SyllableState`.
-/

open A116

def main : IO Unit := do
  for q in State.all do
    for c in cells do
      IO.println s!"{q.pyName},{c.carrier.val},{c.haraka.index},{(step q c).pyName}"
