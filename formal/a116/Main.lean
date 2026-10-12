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
* `hadd`: لكلّ سلسلةِ خاناتٍ بطول ‎1 … 4‎ من ستّة حواملَ (ء ا و ي ل ج) × أربع حالات
  (‎24 + 24² + 24³ + 24⁴ = 346,200‎ سطرًا): الذرّاتُ نصًّا، ثمّ `Hadd.kindOf` و`continueB` و
  `Hadd.strictB`، ليُطابَق بـ`gate.licence.kind_of` و`strict_licensed` سطرًا سطرًا.
* `hadd-join`: لكلّ زوجٍ (أولى بطول ‎1 … 3‎، ثانيةٌ بطول ‎1 … 2‎) من ثلاثة حواملَ (ا ل ج) × أربع
  حالات (‎1,884 × 156 = 293,904‎ سطرًا): الذرّاتُ، ثمّ `Hadd.strictB` على الموصول و`Hadd.strictJoinB`،
  ليُطابَق بـ`gate.licence.strict_joined` سطرًا سطرًا.
* `syllables`: لكلّ سلسلةِ أنواعٍ بطول ‎1 … 11‎ (265,719 سلسلة) تقطيعُها بـ`Stages.parse`
  أو `none`، ثمّ `binOK` و`continueB` و`pauseB` من `Ternary`، ليُطابَق ذلك كلُّه
  بـ`mabni_stages.syllabify` و`ternary_licence` سلسلةً سلسلة.
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
  | .CVVCC => "CVVCC"

def render (k : List K) : String :=
  let key := "-".intercalate (k.map kName)
  let lic := s!"{Ternary.binOK k},{Ternary.continueB k},{Ternary.pauseB k}"
  match parse k with
  | some (l, ss) => s!"{key},{"-".intercalate (leadName l ++ ss.map sylName)},{lic}"
  | none => s!"{key},none,{lic}"

end SyllableTable

namespace HaddTable

open Stages

def mark : Haraka → Char
  | .fatha => '\u064E'
  | .damma => '\u064F'
  | .kasra => '\u0650'
  | .sukun => '\u0652'

def alphabet : List Cell :=
  ['ء', 'ا', 'و', 'ي', 'ل', 'ج'].flatMap fun ch => Haraka.all.map fun h => Ladder.atom ch h

def allW : Nat → List (List Cell)
  | 0 => [[]]
  | n + 1 => (allW n).flatMap fun w => alphabet.map fun c => w ++ [c]

def render (w : List Cell) : String :=
  let atoms := " ".intercalate (w.map fun c => String.ofList [Field112.carrierChar c.carrier, mark c.haraka])
  let k := Hadd.kindOf w
  s!"{atoms},{"-".intercalate (k.map SyllableTable.kName)},{Ternary.continueB k},{Hadd.strictB w},{Hadd.strictPauseB w}"

def joinAlphabet : List Cell :=
  ['ا', 'ل', 'ج'].flatMap fun ch => Haraka.all.map fun h => Ladder.atom ch h

def allJ : Nat → List (List Cell)
  | 0 => [[]]
  | n + 1 => (allJ n).flatMap fun w => joinAlphabet.map fun c => w ++ [c]

def atomsOf (w : List Cell) : String :=
  " ".intercalate (w.map fun c => String.ofList [Field112.carrierChar c.carrier, mark c.haraka])

def iltiqaAlphabet : List Cell :=
  ['ء', 'ا', 'و', 'ي', 'ن', 'ل'].flatMap fun ch => Haraka.all.map fun h => Ladder.atom ch h

def allI : Nat → List (List Cell)
  | 0 => [[]]
  | n + 1 => (allI n).flatMap fun w => iltiqaAlphabet.map fun c => w ++ [c]

def repairName : Option Iltiqa.Repair → String
  | none => "-"
  | some .farqAlifDropped => "FARQ_ALIF_DROPPED"
  | some .maddDropped => "MADD_DROPPED"
  | some .sakinKasra => "SAKIN_KASRA"

/-- التقاءُ الساكنين على الحدّ: الزوج، الوجه، الأولى بعد الإصلاح، الوصلُ قبلُ وبعدُ، والوقفُ بعدُ. -/
def renderIltiqa (l r : List Cell) : String :=
  let p := Iltiqa.repair l r
  s!"{atomsOf l}|{atomsOf r},{repairName p.2},{atomsOf p.1},{Hadd.strictJoinB l r},{Iltiqa.strictJoinRepairedB l r},{Iltiqa.strictJoinPauseRepairedB l r}"

def renderJoin (l r : List Cell) : String :=
  s!"{atomsOf l}|{atomsOf r},{Hadd.strictB (l ++ r)},{Hadd.strictJoinB l r},{Hadd.strictJoinPauseB l r}"

end HaddTable

namespace MizanTable

open A116.Mizan (hi ki)

/-- جدولُ الآلة كاملًا: الخانات، والأحوال، والانتقالُ وصلًا ووقفًا على المجال كلِّه. -/
def rows : List String :=
  (A116.cells.map fun c =>
      s!"cell,{String.ofList [Field112.carrierChar c.carrier, HaddTable.mark c.haraka]},{ki (HarfBridge.unproj c)}") ++
  (Harf.Hal.all.map fun s =>
      s!"state,{hi s},{Harf.qabilWasl s},{Harf.qabilWaqf s},{hi (Harf.hadd s)}") ++
  (Harf.Hal.all.flatMap fun s => Harf.Khana.all.map fun x =>
      s!"wasl,{hi s},{ki x},{hi (Harf.wasl s x)}") ++
  (Harf.Hal.all.flatMap fun s => Harf.Khana.all.map fun x =>
      s!"waqf,{hi s},{ki x},{hi (Harf.waqf s x)}")

def esc (c : Char) : String :=
  let h := String.ofList (Nat.toDigits 16 c.toNat)
  "'\\u" ++ String.ofList (List.replicate (4 - h.length) '0') ++ h ++ "'"

def harakaName : Haraka → String
  | .fatha => ".fatha" | .damma => ".damma" | .kasra => ".kasra" | .sukun => ".sukun"

def commas (l : List String) : List String := (l.dropLast.map (· ++ ",")) ++ l.getLast?.toList

def natRow (xs : List Nat) : String := "[" ++ ", ".intercalate (xs.map toString) ++ "]"

/-- الجدولُ نفسُه مصدرَ Lean: يولَّد هنا ثمّ تفحصه النواةُ في `A116.MizanKernel` فلا يُوثَق بهذا الطابع. -/
def leanFile : List String :=
  ["import A116.Cells", "",
   "/-! مولَّدٌ بـ`lake exe a116-table mizan-lean`؛ لا يُحرَّر باليد. النواةُ تفحصه في `A116.MizanKernel` (ADR ٤٤). -/",
   "", "set_option maxRecDepth 100000", "", "namespace A116.MizanData", "",
   "def cellT : List (Char × A116.Haraka × Nat) := ["] ++
  commas (A116.cells.map fun c =>
      s!"  ({esc (Field112.carrierChar c.carrier)}, {harakaName c.haraka}, {ki (HarfBridge.unproj c)})") ++
  ["]", "",
   "def stateT : List (Bool × Bool × Nat) := ["] ++
  ((Harf.Hal.all.map fun s =>
      s!"  ({Harf.qabilWasl s}, {Harf.qabilWaqf s}, {hi (Harf.hadd s)})") |> fun l =>
        commas l) ++
  ["]", "",
   "def waslT : List (List Nat) := ["] ++
  ((Harf.Hal.all.map fun s => "  " ++ natRow (Harf.Khana.all.map fun x => hi (Harf.wasl s x))) |> fun l =>
        commas l) ++
  ["]", "",
   "def waqfT : List (List Nat) := ["] ++
  ((Harf.Hal.all.map fun s => "  " ++ natRow (Harf.Khana.all.map fun x => hi (Harf.waqf s x))) |> fun l =>
        commas l) ++
  ["]", "", "end A116.MizanData"]

end MizanTable

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
    for n in List.range 11 do
      for k in SyllableTable.allK (n + 1) do
        IO.println (SyllableTable.render k)
  | ["hadd"] =>
    for n in List.range 4 do
      for w in HaddTable.allW (n + 1) do
        IO.println (HaddTable.render w)
  | ["mizan-lean"] =>
    for r in MizanTable.leanFile do IO.println r
  | ["mizan"] =>
    for r in MizanTable.rows do IO.println r
  | ["hadd-join"] =>
    for m in List.range 3 do
      for l in HaddTable.allJ (m + 1) do
        for n in List.range 2 do
          for r in HaddTable.allJ (n + 1) do
            IO.println (HaddTable.renderJoin l r)
  | ["iltiqa"] =>
    for m in List.range 2 do
      for l in HaddTable.allI (m + 1) do
        for n in List.range 2 do
          for r in HaddTable.allI (n + 1) do
            IO.println (HaddTable.renderIltiqa l r)
  | ["licensable"] =>
    -- المرخَّصُ من الشبكة: 113 خانةً (الألفُ المتحرّكة الثلاثُ خارجَه) — ذرّةٌ في كلّ سطر.
    for c in Alif.licensable do
      IO.println (HaddTable.atomsOf [c])
  | ["roles"] =>
    -- الأدوارُ المرخَّصة (`NizamHadd.licensed_roles_n`، ADR ٢٥): الذرّة، الصنف، عددُ الخانة، عددُ الدور n.
    let nm : Stages.K → String
      | .cv => "cv" | .v => "v" | .c => "c"
    for c in Alif.licensable do
      for k in Exhaust.rolesOf c do
        IO.println s!"{HaddTable.atomsOf [c]},{nm k},{Numbering.bridgeIndex c},{NizamHadd.roleN (k, c)}"
  | ["hamza"] =>
    -- جدولُ الكرسيّ لكلّ سياق: pos,own,prev,prevLong,prevYa,nextWaw,seat
    for p in [Hamza.Pos.initial, .medial, .final] do
      for own in [Haraka.fatha, .damma, .kasra, .sukun] do
        for prev in [Haraka.fatha, .damma, .kasra, .sukun] do
          for pl in [false, true] do
            for py in [false, true] do
              for nw in [false, true] do
                let s := Hamza.seatOf ⟨p, own, prev, pl, py, nw⟩
                IO.println s!"{repr p},{repr own},{repr prev},{pl},{py},{nw},{repr s}"
  | ["degrees"] =>
    -- جداولُ الدرجات وصلًا (`Exhaust.table`): الدرجة d = 1 … 4، والعدد n، ومقاطعُ الصفّ — 255 سطرًا.
    for k in List.range 4 do
      for n in List.range (3 * 4 ^ k) do
        let ss := Exhaust.decodeW k n
        IO.println s!"{k + 1},{n},{"-".intercalate (ss.map SyllableTable.sylName)}"
  | ["wazn"] =>
    -- الأوزانُ الثلاثيّة على الخانات (`Wazn.thulathi`) ابتداءً وصلًا بحالة الأصل الأخير الصرفيّة: رقمُ القالب،
    -- ثمّ الذرّاتُ والأصولُ أرقامًا (1 2 3) بحالاتها، ثمّ المقاطعُ وصلًا ووقفًا على الجذر الصحيح ك ت ب.
    let mark : Haraka → String
      | .fatha => "َ" | .damma => "ُ" | .kasra => "ِ" | .sukun => "ْ"
    let nm : Stages.Syl → String
      | .CV => "CV" | .CVV => "CVV" | .CVC => "CVC" | .CVVC => "CVVC" | .CVCC => "CVCC"
      | .CVVCC => "CVVCC"
    let sy := fun (w : List Cell) =>
      match Wazn.syllables w with
      | some ss => "-".intercalate (ss.map nm)
      | none => "none"
    for (i, W) in (List.range Wazn.thulathi.length).zip Wazn.thulathi do
      let pre := if W.wasl then [s!"ء{mark (Wazn.waslH W Wazn.ktb)}"] else []
      let body := W.body.map fun
        | .lit c => s!"{Field112.carrierChar c.carrier}{mark c.haraka}"
        | .slot j h => s!"{j.val + 1}{mark h}"
      let last := s!"{W.last.val + 1}{mark (Wazn.lastH i)}"
      let cont := Wazn.realize W Wazn.ktb .start .continue (Wazn.lastH i)
      let paus := Wazn.realize W Wazn.ktb .start .pause (Wazn.lastH i)
      IO.println s!"{i},{" ".intercalate (pre ++ body ++ [last])},{sy cont},{sy paus}"
  | ["wazn-body"] =>
    -- جسمُ كلّ وزنٍ ثلاثيّ رموزًا (`Wazn.thulathi`): رقمُه، أله همزةُ وصل، رقمُ الأصل الأخير، ثمّ الرموز:
    -- خانةٌ زائدة حرفًا وحالةً، أو أصلٌ رقمًا (1 2 3) وحالة.
    let mark : Haraka → String
      | .fatha => "َ" | .damma => "ُ" | .kasra => "ِ" | .sukun => "ْ"
    for (i, W) in (List.range Wazn.thulathi.length).zip Wazn.thulathi do
      let toks := W.body.map fun
        | .lit c => s!"{Field112.carrierChar c.carrier}{mark c.haraka}"
        | .slot j h => s!"{j.val + 1}{mark h}"
      IO.println s!"{i},{W.wasl},{W.last.val + 1},{" ".intercalate toks}"
  | ["neutral"] =>
    -- التقييمُ بالمحايد (`Neutral.realizeN`) على الجذور المرجعيّة والأوزان كلِّها، ابتداءً وصلًا وابتداءً وقفًا.
    let mark : Haraka → String
      | .fatha => "َ" | .damma => "ُ" | .kasra => "ِ" | .sukun => "ْ"
    let atoms := fun (w : List Cell) =>
      " ".intercalate (w.map fun c => s!"{Field112.carrierChar c.carrier}{mark c.haraka}")
    let names := ["قول", "سير", "دعو", "رمي", "وعد", "ءمن", "سءل", "قرء", "مدد", "هوي", "حيي"]
    for (nm, r) in names.zip Neutral.refRoots do
      for (i, W) in (List.range Wazn.thulathi.length).zip Wazn.thulathi do
        let c := Neutral.realizeN W r .start .continue (Wazn.lastH i)
        let p := Neutral.realizeN W r .start .pause (Wazn.lastH i)
        IO.println s!"{nm},{i},{atoms c},{atoms p}"
  | ["tasrif"] =>
    -- التصريفُ على الخانات (`Tasrif`، ADR ٢٦) على جذورٍ شواهد: الجذر، الصيغة، الباب، حركةُ العين،
    -- حرفُ المضارعة، الإعراب، ثمّ الذرّات. الصيغُ: madi (الماضي 3MS)، mudari، amr، amr-pause، khudh.
    let mark : Haraka → String
      | .fatha => "َ" | .damma => "ُ" | .kasra => "ِ" | .sukun => "ْ"
    let hn : Haraka → String
      | .fatha => "a" | .damma => "u" | .kasra => "i" | .sukun => "0"
    let atoms := fun (w : List Cell) =>
      " ".intercalate (w.map fun c => s!"{Field112.carrierChar c.carrier}{mark c.haraka}")
    let roots := ["قوم", "قول", "نوم", "خوف", "كون", "وقي", "وعي", "وعد", "وصل", "ولد", "نمو", "دعو",
      "خشي", "رضي", "نهي", "هدي", "مشي", "ءخذ", "ءمر", "عطو", "مدد"]
    for nm in roots do
      match nm.toList with
      | [a, b, c] =>
        let r := Tasrif.r3 a b c
        let s := Tasrif.sifa r
        let row := fun (k bab v p m : String) (t : List (Wazn.CSym 3)) =>
          IO.println s!"{nm},{k},{bab},{v},{p},{m},{atoms (Wazn.fillC t r)}"
        for a' in Tasrif.harakat3 do
          row "madi" "I" (hn a') "-" "-" (Tasrif.madi s a' .fatha)
        for v in Tasrif.harakat3 do
          for p in Tasrif.prefixes do
            for m in Tasrif.moods do
              row "mudari" "I" (hn v) p.toString (hn m) (Tasrif.mudari s .mujarrad p v m)
          row "amr" "I" (hn v) "-" "-" (Tasrif.amr s .mujarrad v)
          row "amr-pause" "I" (hn v) "-" "-" (Tasrif.amrPause s .mujarrad v)
          row "khudh" "I" (hn v) "-" "-" (Tasrif.amrKhudh s v)
        for p in Tasrif.prefixes do
          for m in Tasrif.moods do
            row "mudari" "IV" "i" p.toString (hn m) (Tasrif.mudari s .afala p .kasra m)
        row "amr" "IV" "i" "-" "-" (Tasrif.amr s .afala .kasra)
      | _ => pure ()
  | ["rubai"] =>
    -- أوزانُ الرباعيّ (`Rubai`، ADR ٢٨) على جذورٍ شواهد: اسمُ الوزن، الجذر، الذرّاتُ ابتداءً وصلًا ووقفًا؛
    -- ثمّ عددُ شاهد الدلالة المختوم (`Rubai.maqayisCount`).
    let mark : Haraka → String
      | .fatha => "َ" | .damma => "ُ" | .kasra => "ِ" | .sukun => "ْ"
    let atoms := fun (w : List Cell) =>
      " ".intercalate (w.map fun c => s!"{Field112.carrierChar c.carrier}{mark c.haraka}")
    let roots := ["حصحص", "عسعس", "دمدم", "وسوس", "بعثر", "زحزح", "زلزل", "دحرج", "مضمض", "دهده", "طمءن",
      "شمءز", "قشعر"]
    for B in Rubai.abniya do
      for nm in roots do
        match nm.toList with
        | [a, b, c, d] =>
          let r := Rubai.r4 a b c d
          IO.println s!"{B.name},{nm},{atoms (Wazn.realize B.w r .start .continue B.h)},{atoms (Wazn.realize B.w r .start .pause B.h)}"
        | _ => pure ()
    IO.println s!"maqayis,{Rubai.maqayisCount}"
  | ["maqayis"] =>
    -- جذورُ «مقاييس اللغة» الثلاثيّة صفوفًا من جدول الدرجة (`Maqayis.roots`، ADR ٣٥): الأصولُ حروفًا بترتيب العدد n.
    for r in Maqayis.roots do
      IO.println (String.ofList (r.map fun d => Field112.carrierChar (RootGrade.toCarrier d)))
  | ["degrees-pause"] =>
    -- جداولُ الدرجات وقفًا (`ExhaustPause.pauseTable`، ADR ١٨): الدرجة d = 1 … 4، والعدد n، ومقاطعُ الصفّ — 510 سطرًا.
    for k in List.range 4 do
      for n in List.range (6 * 4 ^ k) do
        let ss := ExhaustPause.decodeP k n
        IO.println s!"{k + 1},{n},{"-".intercalate (ss.map SyllableTable.sylName)}"
  | ["ledger"] =>
    -- الأوزانُ في جداول درجاتها (`Ledger.waznRows`، ADR ١٩): رقمُ القالب، الدرجة، العدد n.
    for (i, d, n) in Ledger.waznRows do
      IO.println s!"{i},{d},{n}"
  | ["need"] =>
    -- قانونُ الحاجة المتبادلة (`Hajah.NeedLaw`) على كلّ سلسلةِ أدوارٍ بطول 1 … 8 (9,840 سطرًا): السلسلة، والقانون،
    -- وحالةُ الوراثة بعدها (ذيلُ المقطع المفتوح، أو none).
    let st := fun (s : Option (Option (List Stages.K))) => match s with
      | some (some t) => "[" ++ "-".intercalate (t.map SyllableTable.kName) ++ "]"
      | some none => "none"
      | none => "refused"
    for n in List.range 8 do
      for k in SyllableTable.allK (n + 1) do
        IO.println s!"{"-".intercalate (k.map SyllableTable.kName)},{decide (Hajah.NeedLaw k)},{st (Hajah.needState none k)}"
  | ["nizam"] =>
    -- نظامُ الجوار الثلاثيّ (`Nizam.ternary`، ADR ٢٣): لكلّ زوجٍ (قبل، بعد) من أصناف الذرّة إذنُه وصلًا ووقفًا.
    let nm : Stages.K → String
      | .cv => "cv" | .v => "v" | .c => "c"
    for a in [Stages.K.cv, .v, .c] do
      for b in [Stages.K.cv, .v, .c] do
        IO.println s!"{nm a},{nm b},{Nizam.waslK a b},{Nizam.waqfK a b}"
  | ["amr"] =>
    -- المضارعُ والأمر (`Mudari`، ADR ٢٤) على الجذور المرجعيّة × الأوزان التسعة × الأبواب: رقمُ الجذر، الوزن، الباب،
    -- المضارعُ رفعًا بالياء، والمجزومُ بالتاء، والأمر — ذرّاتٍ، وأأقام قانونُ الابتداء همزةَ وصل.
    let mark : Haraka → String
      | .fatha => "َ" | .damma => "ُ" | .kasra => "ِ" | .sukun => "ْ"
    let atoms := fun (w : List Cell) =>
      " ".intercalate (w.map fun c => s!"{Field112.carrierChar c.carrier}{mark c.haraka}")
    let fname : Mudari.Form → String
      | .I => "I" | .II => "II" | .III => "III" | .IV => "IV" | .V => "V" | .VI => "VI"
      | .VII => "VII" | .VIII => "VIII" | .X => "X"
    for (r, i) in Mudari.refRoots.zip (List.range Mudari.refRoots.length) do
      for f in Mudari.Form.all do
        for b in Mudari.babs r f do
          IO.println s!"{i},{fname f},{mark b},{atoms (Mudari.mudari r f b 'ي' .damma)},{atoms (Mudari.mudari r f b 'ت' .sukun)},{atoms (Mudari.amr r f b)},{Mudari.amrWasl r f b}"
  | ["utf8"] =>
    -- أبجديّةُ الرسم: الحروفُ ‎U+0621–U+064A‎، العلاماتُ ‎U+064B–U+0652‎، ألفُ الوصل ‎U+0671‎، والمسافة.
    for c in (List.range 0x2B).map (· + 0x621) ++ (List.range 8).map (· + 0x64B) ++ [0x671, 0x20] do
      IO.println s!"{c},{" ".intercalate ((Unicode.utf8Encode c).map toString)}"
  | ["pairs"] =>
    for u in List.range 64 do
      for r in List.range 64 do
        IO.println s!"{u},{r},{Numbering.pair u r}"
  | _ =>
    for q in State.all do
      for c in cells do
        IO.println s!"{q.pyName},{c.carrier.val},{c.haraka.index},{(step q c).pyName}"
