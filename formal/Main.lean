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
  | ["sequence"] =>
    -- لكلّ مرخَّصةٍ بطول ‎≤ 2‎: مفتاحُها، بتّاتُ `encodeWord` (0/1)، وكلفةُ الطول؛ وسطرٌ ختاميّ
    -- يرمّز تيارًا من ثلاث كلماتٍ ويفكّه ليُطابَق فكُّه بايثونًا.
    for k in List.range 3 do
      IO.println s!"width,{k},{Sequence.width k},{Sequence.cost k}"
    for n in List.range 3 do
      for w in words n do
        if licensed w then
          let key := "-".intercalate (w.map fun c => toString c.index)
          let bits := String.ofList ((Sequence.encodeWord w).map fun b => if b then '1' else '0')
          IO.println s!"{key},{bits}"
  | ["categories"] =>
    for w in Categories.pronouns do
      let key := "-".intercalate (w.map fun c => toString c.index)
      IO.println s!"pronoun,{key},{slgeFold w}"
  | ["wazn"] =>
    -- لكلّ وزنٍ مودَع: رقمُه، وميزانُه خاناتٍ (رموزُ SLGE)، وهل يردّ الأصلَ (ف، ع، ل).
    let mut n := 0
    for t in Wazn.awzan do
      let m := Wazn.mizan t
      let key := "-".intercalate (m.map fun c => toString c.index)
      let back := ([0, 1, 2] : List (Fin 3)).map fun i => match Wazn.rootOf t m i with
        | some c => toString c.val | none => "none"
      IO.println s!"{n},{key},{licensed m},{"-".intercalate back}"
      n := n + 1
  | ["shabaka"] =>
    -- حوافُّ شبكة البصريّين: الابن، الأب، عددُ العمليّات، وهل يبلغ الجذر.
    for e in Shabaka.edges do
      IO.println s!"{e.1},{e.2.1},{e.2.2.length},{Shabaka.reaches e.1 113}"
  | ["khamsa"] =>
    for w in Khamsa.forms do
      let key := "-".intercalate (w.map fun c => toString c.index)
      IO.println s!"{key},{slgeFold w}"
  | ["afal"] =>
    for w in Afal.forms do
      let key := "-".intercalate (w.map fun c => toString c.index)
      IO.println s!"{key},{licensed w}"
  | ["rawabit"] =>
    for p in Rawabit.particles do
      let key := "-".intercalate (p.cells.map fun c => toString c.index)
      let a := match p.amal with
        | .none => "none" | .jazm => "jazm" | .nasb => "nasb" | .jarr => "jarr" | .nasbIsm => "nasbIsm"
      IO.println s!"{p.name},{key},{a},{p.proclitic},{licensed p.cells}"
  | ["damair"] =>
    for w in Damair.allForms do
      IO.println ("-".intercalate (w.map fun c => toString c.index))
  | ["ishara"] =>
    for p in Ishara.forms do
      IO.println s!"{p.1},{"-".intercalate (p.2.map fun c => toString c.index)}"
  | ["istifham"] =>
    for p in Istifham.forms do
      IO.println s!"{p.1},{"-".intercalate (p.2.map fun c => toString c.index)}"
  | ["nida"] =>
    for p in Nida.particles do
      IO.println s!"particle,{p.1},{"-".intercalate (p.2.map fun c => toString c.index)}"
    for w in Nida.witnesses do
      let h := match w.2.2 with
        | .mabniDamm => "mabniDamm" | .mabniAlif => "mabniAlif" | .mabniWaw => "mabniWaw"
        | .mansub => "mansub" | .nakiraGhayrMaqsuda => "nakira" | .mudafIlaYa => "mudafIlaYa"
        | .unread => "unread"
      IO.println s!"witness,{w.1},{"-".intercalate (w.2.1.map fun c => toString c.index)},{h}"
  | ["zuruf"] =>
    for w in Zuruf.forms do
      IO.println ("-".intercalate (w.map fun c => toString c.index))
  | ["zaman"] =>
    for w in Zaman.forms do
      IO.println s!"form,{"-".intercalate (w.map fun c => toString c.index)}"
    for p in Zaman.constants do
      IO.println s!"constant,{p.1},{"-".intercalate (p.2.1.map fun c => toString c.index)},{p.2.2}"
  | ["adad"] =>
    for w in Adad.forms do
      IO.println ("-".intercalate (w.map fun c => toString c.index))
  | ["marifa"] =>
    for p in Marifa.mawsul do
      IO.println s!"{p.1},{"-".intercalate (p.2.map fun c => toString c.index)}"
  | ["rank"] =>
    for g1 in [Rank.Grade.zanni, .qati] do
      for s1 in [1, 2, 3] do
        for g2 in [Rank.Grade.zanni, .qati] do
          for s2 in [1, 2, 3] do
            for (x, y) in [(false, false), (true, false), (false, true)] do
              let v := Rank.weighS ⟨g1, s1⟩ ⟨g2, s2⟩ x y
              IO.println s!"{gradeName g1},{s1},{x},{gradeName g2},{s2},{y},{verdictName v}"
  | _ => IO.eprintln "usage: slge-table bridge|counts|folds|ghazali|rank|rasm"
