import Slge

/-!
مخرجاتٌ لمطابقة Lean بالبايثون في CI (`tests/test_conformance.py`):

* `bridge`: لكلّ خانةٍ من خانات SLGE الـ116 بترتيبها: ‎حامل،حالة،رمز الـ116‎.
* `counts`: ‎n,count(n)‎ لـ‎n = 0 … 12‎ من `Slge.count` المبرهَن أنه ‎U(n)‎.
* `folds`: لكلّ مرخَّصةٍ بطول ‎≤ 2‎: رموزُ SLGE (‎4·حامل + حالة‎) مفصولةً بـ`-` ثمّ طيُّها.
* `ghazali`: ‎درجة,صورة,منتجة‎ للخانات الثماني.
* `rasm`: لكلّ سلسلةِ خاناتٍ بطول ‎≤ 2‎ (‎13,573‎): رموزُ SLGE ثمّ رموزُ الرسم التي يكتبها `Rasm.write none`.
* `rank`: ‎رتبة١,شواهد١,خاص١,رتبة٢,شواهد٢,خاص٢,الحكم‎ لكلّ رتبتين وشواهد ‎1…3‎ وخصوصٍ (‎108‎ أسطر).
-/

open Slge

def words : Nat → List (List SCell)
  | 0 => [[]]
  | n + 1 => (words n).flatMap fun w => scells.map fun c => w ++ [c]

def degreeName : Ghazali.Degree → String
  | .akhass => "akhass"
  | .musawi => "musawi"

def formName : Ghazali.Form → String
  | .aynMuqaddam => "ayn_muqaddam"
  | .naqidTali => "naqid_tali"
  | .naqidMuqaddam => "naqid_muqaddam"
  | .aynTali => "ayn_tali"

def glyphName : Rasm.G → String
  | .letter l => s!"L{l.val}"
  | .mark h => s!"M{h.val}"
  | .tanwin v => s!"T{v.val}"
  | .hamza h => s!"H{h.val}"
  | .hamzaTanwin v => s!"HT{v.val}"
  | .madda => "MADDA"

def gradeName : Rank.Grade → String
  | .zanni => "zanni"
  | .qati => "qati"

def verdictName : Rank.Verdict → String
  | .yaqin => "yaqin"
  | .zann => "zann"
  | .rajih => "rajih"
  | .marjuh => "marjuh"
  | .mardud => "mardud"
  | .taadul => "taadul"
  | .tanaqud => "tanaqud"
  | .makhsus => "makhsus"

def main (args : List String) : IO Unit := do
  match args with
  | ["bridge"] =>
    for c in scells do
      IO.println s!"{c.carrier.val},{c.state.val},{A116.code (toCell c)}"
  | ["counts"] =>
    for n in List.range 13 do
      IO.println s!"{n},{count n}"
  | ["folds"] =>
    for n in List.range 3 do
      for w in words n do
        if licensed w then
          let key := "-".intercalate (w.map fun c => toString c.index)
          IO.println s!"{key},{slgeFold w}"
  | ["ghazali"] =>
    for d in [Ghazali.Degree.akhass, .musawi] do
      for f in [Ghazali.Form.aynMuqaddam, .naqidTali, .naqidMuqaddam, .aynTali] do
        IO.println s!"{degreeName d},{formName f},{Ghazali.productive d f}"
  | ["rasm"] =>
    for n in List.range 3 do
      for w in words n do
        let key := "-".intercalate (w.map fun c => toString c.index)
        let gl := " ".intercalate ((Rasm.write none w).map glyphName)
        IO.println s!"{key},{gl}"
  | ["rank"] =>
    for g1 in [Rank.Grade.zanni, .qati] do
      for s1 in [1, 2, 3] do
        for g2 in [Rank.Grade.zanni, .qati] do
          for s2 in [1, 2, 3] do
            for (x, y) in [(false, false), (true, false), (false, true)] do
              let v := Rank.weighS ⟨g1, s1⟩ ⟨g2, s2⟩ x y
              IO.println s!"{gradeName g1},{s1},{x},{gradeName g2},{s2},{y},{verdictName v}"
  | _ => IO.eprintln "usage: slge-table bridge|counts|folds|ghazali|rank|rasm"
