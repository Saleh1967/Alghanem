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

/-- سلسلةُ إعلالٍ نصًّا: رقمُ القاعدة في `Rule.all` وموضعُها. -/
def chain (ch : Slge.Ilal.Chain) : String :=
  "+".intercalate (ch.map fun x => s!"{Slge.Ilal.Rule.all.idxOf x.1}:{x.2}")

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
      IO.println s!"{e.1},{e.2.1},{e.2.2.length},{Shabaka.reaches e.1 Wazn.N}"
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
  | ["sarf"] =>
    for w in Sarf.witnesses do
      let h := match w.2.2 with
        | .muntahaJumu => "muntahaJumu" | .maqsura => "maqsura" | .mamduda => "mamduda"
        | .sifa => "sifa" | .alifNun => "alifNun" | .unread => "unread"
      IO.println s!"{w.1},{"-".intercalate (w.2.1.map fun c => toString c.index)},{h}"
  | ["tawabi"] =>
    for (n, w) in [("alimu", Tawabi.alimu), ("akhu", Tawabi.akhuka.take 3), ("muslimuna", Tawabi.muslimuna),
                   ("rajulani", Tawabi.rajulani), ("rajulun", Tawabi.rajulun)] do
      let h := match Tawabi.caseClass w with
        | .raf => "raf" | .nasb => "nasb" | .jarr => "jarr" | .nasbJarr => "nasbJarr" | .unread => "unread"
      IO.println s!"{n},{"-".intercalate (w.map fun c => toString c.index)},{h}"
  | ["nawasikh"] =>
    -- المودَعات الأربع بخاناتها، وصورُ الكفّ الستّ، وشاهدا كان/إنّ
    for (bab, l) in [("kana", Nawasikh.kanaSisters), ("kada", Nawasikh.kadaSisters),
                     ("inna", Nawasikh.innaSisters), ("zanna", Nawasikh.zannaSisters)] do
      for p in l do
        IO.println s!"{bab},{p.1},{"-".intercalate (p.2.map fun c => toString c.index)}"
    for p in Nawasikh.innaSisters do
      IO.println s!"kaffa,{p.1},{"-".intercalate ((Nawasikh.kaffa p.2).map fun c => toString c.index)}"
    IO.println s!"kana_khabar,غَفُورًا,{"-".intercalate ((Nawasikh.tanwin (Nawasikh.kana.2 Nawasikh.ghafur)).map fun c => toString c.index)}"
    IO.println s!"inna_khabar,غَفُورٌ,{"-".intercalate ((Nawasikh.tanwin (Nawasikh.inna.2 Nawasikh.ghafur)).map fun c => toString c.index)}"
  | ["jazm"] =>
    let mk := fun (m : Jazm.Marker) => match m with
      | .sukun => "sukun" | .dropNun => "dropNun" | .unread => "unread"
    for (bab, l) in [("one", Jazm.jazimOne), ("jazim", Jazm.shartJazim), ("ghayr", Jazm.shartGhayr)] do
      for p in l do
        IO.println s!"{bab},{p.1},{"-".intercalate (p.2.map fun c => toString c.index)}"
    for (n, w) in Jazm.witnesses do
      IO.println s!"marker,{n},{"-".intercalate (w.map fun c => toString c.index)},{mk (Jazm.marker w)}"
  | ["mansubat"] =>
    for (n, w) in [("dahik", Mansubat.dahik), ("rakid", Mansubat.rakid), ("nafs", Mansubat.nafs),
                   ("shayb", Mansubat.shayb), ("sukara", Mansubat.sukara)] do
      IO.println s!"derived,{n},{"-".intercalate (w.map fun c => toString c.index)},{Mansubat.derived w}"
    for (n, w) in [("shayb", Mansubat.nakiraMansuba Mansubat.shayb),
                   ("ras", (Mansubat.tahwil Mansubat.shayb Mansubat.rasStem).1),
                   ("original", Mansubat.original Mansubat.shayb Mansubat.rasStem),
                   ("ghayr_raf", Mansubat.ghayrOf Nawasikh.raf [Slge.Categories.c 10 0, Slge.Categories.c 5 2, Slge.Categories.c 23 2])] do
      IO.println s!"op,{n},{"-".intercalate (w.map fun c => toString c.index)}"
    for (n, w) in [("illa", Mansubat.illa), ("ghayr", Mansubat.ghayr), ("siwa", Mansubat.siwa),
                   ("khala", Mansubat.khala), ("ada", Mansubat.ada), ("hasha", Mansubat.hasha)] do
      IO.println s!"tool,{n},{"-".intercalate (w.map fun c => toString c.index)}"
  | ["majrurat"] =>
    for p in Majrurat.harfs do
      IO.println s!"harf,{p.1},{"-".intercalate (p.2.map fun c => toString c.index)}"
    let rajul := [Slge.Categories.c 10 0, Slge.Categories.c 5 2, Slge.Categories.c 23 2]
    for (n, w) in [("jarr_nakira", Nawasikh.tanwin (Majrurat.jarr rajul)), ("dual", Majrurat.dual rajul),
                   ("mudaf_uqud", Majrurat.mudafUqud [Slge.Categories.c 24 2, Slge.Categories.c 26 0,
                      Slge.Categories.c 25 3, Slge.Categories.c 8 1, Slge.Categories.c 12 2] true),
                   ("mudaf_dual", Majrurat.mudafDual rajul)] do
      IO.println s!"op,{n},{"-".intercalate (w.map fun c => toString c.index)}"
  | ["wasl"] =>
    let kn := fun (k : Wasl.Kind) => match k with
      | .wasl => "wasl" | .qat => "qat" | .qatRadical => "qatRadical" | .unread => "unread"
    for p in Wasl.tenNouns do
      IO.println s!"ten,{p.1},{"-".intercalate (p.2.map fun c => toString c.index)},{kn (Wasl.kind p.2)}"
    for (n, w) in [("iqra", [Slge.Categories.c 0 1, Slge.Categories.c 21 3, Slge.Categories.c 10 0, Slge.Categories.c 0 3]),
                   ("intalaqa", Wasl.intalaqa), ("intilaq", Wasl.intilaq), ("akrama", Wasl.akrama),
                   ("ikram", Wasl.ikram), ("akhadha", [Slge.Categories.c 0 0, Slge.Categories.c 7 0, Slge.Categories.c 9 0]),
                   ("illa", Mansubat.illa)] do
      IO.println s!"kind,{n},{"-".intercalate (w.map fun c => toString c.index)},{kn (Wasl.kind w)}"
    IO.println s!"templates,wasl,{"-".intercalate (Wasl.waslTemplates.map toString)}"
    IO.println s!"templates,qat,{"-".intercalate (Wasl.qatTemplates.map toString)}"
  | ["ism"] =>
    for w in Ism.witnesses do
      IO.println s!"thulathi,{w.1},{"-".intercalate (w.2.1.map fun c => toString c.index)},{w.2.2.1}-{w.2.2.2}"
    for p in Ism.rubai ++ Ism.khumasi do
      IO.println s!"shape,{p.1},{"-".intercalate (p.2.map fun c => toString c.index)},{"-".intercalate ((Ism.shape p.2).map toString)}"
    for (n, w) in [("rujayl", Ism.saghir3 10 5 23 2), ("durayhim", Ism.saghir4 8 10 26 24 2),
                   ("usayfir", Ism.saghir5 18 14 20 10 2),
                   ("misri", Ism.nisba [Slge.Categories.c 24 1, Slge.Categories.c 14 3, Slge.Categories.c 10 0] 2),
                   ("makki", Ism.nisba (Ism.prepare .dropTa [Slge.Categories.c 24 0, Slge.Categories.c 22 3, Slge.Categories.c 22 0, Slge.Categories.c 3 2]) 2),
                   ("asawi", Ism.nisba (Ism.prepare .maqsur3 [Slge.Categories.c 18 0, Slge.Categories.c 14 0, Slge.Categories.c 1 3]) 2),
                   ("amawi", Ism.nisba (Ism.prepare .manqus3 [Slge.Categories.c 18 0, Slge.Categories.c 24 1, Slge.Categories.c 28 3]) 2)] do
      IO.println s!"op,{n},{"-".intercalate (w.map fun c => toString c.index)}"
  | ["fil"] =>
    for p in Fil.abwab do
      IO.println s!"bab,{p.1}-{p.2}"
    for k in Fil.mazid do
      IO.println s!"mazid,{k},{Fil.added (Sarf.templ k)}"
    let r1 : Wazn.Root := fun i => if i = 0 then 14 else if i = 1 then 2 else 10
    let r2 : Wazn.Root := fun i => if i = 0 then 11 else if i = 1 then 26 else 10
    let r3 : Wazn.Root := fun i => if i = 0 then 27 else if i = 1 then 14 else 23
    let r4 : Wazn.Root := fun i => if i = 0 then 0 else if i = 1 then 7 else 9
    for (p, a) in Fil.mazidPres.zip Fil.mazidAmr do
      IO.println s!"amr,{p},{a},{Fil.amrOf (Sarf.templ p) == Sarf.templ a}"
    for (n, w) in [("istabara", Fil.ibdal (Fil.iftaal r1)), ("izdahara", Fil.ibdal (Fil.iftaal r2)),
                   ("ittasala", Fil.ibdal (Fil.iftaal r3)), ("ittakhadha", Fil.ibdal (Fil.iftaal r4)),
                   ("radda", Fil.idgham [Slge.Categories.c 10 0, Slge.Categories.c 8 0, Slge.Categories.c 8 0]),
                   ("qala", Fil.qalb [Slge.Categories.c 21 0, Slge.Categories.c 27 0, Slge.Categories.c 23 0]),
                   ("qulu", Fil.naql [Slge.Categories.c 21 3, Slge.Categories.c 27 2, Slge.Categories.c 23 2])] do
      IO.println s!"op,{n},{"-".intercalate (w.map fun c => toString c.index)}"
    for p in Fil.rubai do
      IO.println s!"rubai,{p.1},{"-".intercalate (p.2.map fun c => toString c.index)}"
  | ["huruf"] =>
    let cl := fun (k : Huruf.Class) => match k with | .ism => "ism" | .fil => "fil" | .mushtarak => "mushtarak"
    let am := fun (a : Huruf.Amal) => match a with
      | .jarr => "jarr" | .nasbIsm => "nasbIsm" | .nida => "nida" | .maiyya => "maiyya" | .nasbFil => "nasbFil"
      | .jazm => "jazm" | .jazm2 => "jazm2" | .tabi => "tabi" | .none => "none"
    for x in Huruf.table do
      IO.println s!"{cl x.cls},{x.name},{"-".intercalate (x.cells.map fun c => toString c.index)},{am x.amal}"
  | ["jumla"] =>
    -- الشواهدُ: الرتبةُ المقروءة والقبول، والجنسُ والعددُ بعد العمليّات، والرابط.
    let ru := fun (r : Jumla.Rutba) => match r with
      | .khabarFirst => "khabarFirst" | .mubtadaFirst => "mubtadaFirst" | .free => "free"
    let kk := fun (k : Jumla.KhabarKind) => match k with
      | .mufrad => "mufrad" | .shibhJumla => "shibhJumla" | .jumla => "jumla" | .unread => "unread"
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    for (n, j) in [("rajul-fidDar", (⟨Jumla.rajul, Jumla.fidDar, true⟩ : Jumla.Jumla)),
                   ("almafarr-ayna", ⟨Jumla.almafarr, Jumla.ayna, true⟩),
                   ("tullabuha-fiMadrasa", ⟨Jumla.tullabuha, Jumla.fiMadrasa, true⟩),
                   ("zayd-darasa", ⟨Jumla.zayd, Jumla.darasa, false⟩),
                   ("akhi-rafiqi", ⟨Jumla.akhi, Jumla.rafiqi, false⟩),
                   ("lazayd-qaim", ⟨Jumla.lam Jumla.zayd, Jumla.qaim, false⟩),
                   ("salama-fiTaanni", ⟨Jumla.salama, Jumla.fiTaanni, false⟩)] do
      IO.println s!"order,{n},{key j.mubtada},{key j.khabar},{ru (Jumla.order j)},{Jumla.admissible j},{kk (Jumla.khabarKind j.khabar)}"
    let g := fun (w : List SCell) => match Jumla.gender w with | .masc => "masc" | .fem => "fem"
    let nn := fun (w : List SCell) => match Jumla.number w with
      | .single => "single" | .dual => "dual" | .plural => "plural"
    for (n, w) in [("talib", Jumla.talib), ("taNith", Jumla.taNith Jumla.talib), ("dual", Jumla.dual Jumla.talib),
                   ("jamM", Jumla.jamM Jumla.talib), ("jamF", Jumla.jamF Jumla.talib),
                   ("dualTaNith", Jumla.dual (Jumla.taNith Jumla.talib)), ("jibal", Jumla.jibal),
                   ("shahiqa", Jumla.shahiqa)] do
      IO.println s!"agree,{n},{key w},{g w},{nn w},{Jumla.brokenPlural w}"
  | ["filiyya"] =>
    -- الشواهدُ: رتبةُ الثلاثيّ وقبولُه، والمجهولُ، والنائبُ، والفرزُ.
    let ru := fun (r : Filiyya.Rutba) => match r with
      | .failFirst => "failFirst" | .mafulFirst => "mafulFirst" | .mafulBeforeFil => "mafulBeforeFil"
      | .free => "free"
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    for (n, j) in [("katabtu", (⟨Filiyya.katabtu, [], Filiyya.addars, .FSO⟩ : Filiyya.Filiyya)),
                   ("musa-isa", ⟨Filiyya.daraba, Filiyya.musa, Filiyya.isa, .FSO⟩),
                   ("sahibuha", ⟨Filiyya.sakana, Filiyya.sahibuha, Filiyya.addar, .FOS⟩),
                   ("akramani", ⟨Filiyya.akramani, Filiyya.abuka, [], .FOS⟩),
                   ("ayya", ⟨Filiyya.qabalta, [], Filiyya.ayya, .OFS⟩),
                   ("akala", ⟨Filiyya.akala, Filiyya.zaydun, Filiyya.tuffahatan, .FSO⟩)] do
      IO.println s!"order,{n},{key j.fil},{key j.fail},{key j.maful},{ru (Filiyya.order j)},{Filiyya.admissible j}"
    let nk := fun (k : Filiyya.NaibKind) => match k with
      | .maful => "maful" | .majrur => "majrur" | .zarf => "zarf" | .masdar => "masdar"
    let fd := fun (k : Filiyya.Fadla) => match k with
      | .liajlih => "liajlih" | .mutlaqF => "mutlaq" | .hal => "hal" | .unread => "unread"
    for (n, w) in [("kataba", Filiyya.majhul [Slge.Categories.c 22 0, Slge.Categories.c 3 0, Slge.Categories.c 2 0]),
                   ("yaktubu", Filiyya.majhulPres [Slge.Categories.c 28 0, Slge.Categories.c 22 3, Slge.Categories.c 3 2, Slge.Categories.c 2 2])] do
      IO.println s!"majhul,{n},{key w}"
    for w in [Filiyya.naib [Slge.Categories.c 0 0, Slge.Categories.c 10 3, Slge.Categories.c 10 0, Slge.Categories.c 5 2, Slge.Categories.c 23 0],
              [Slge.Categories.c 28 0, Slge.Categories.c 27 3, Slge.Categories.c 24 2],
              [Slge.Categories.c 20 0, Slge.Categories.c 26 3, Slge.Categories.c 24 2, Slge.Categories.c 25 3]] do
      IO.println s!"naib,{key w},{nk (Filiyya.naibKind w)}"
    for (w, v) in [([Slge.Categories.c 10 0, Slge.Categories.c 20 3, Slge.Categories.c 2 0, Slge.Categories.c 3 0, Slge.Categories.c 25 3], Filiyya.qumtu),
              ([Slge.Categories.c 10 0, Slge.Categories.c 1 3, Slge.Categories.c 18 1, Slge.Categories.c 2 0, Slge.Categories.c 25 3], Filiyya.qumtu),
              ([Slge.Categories.c 15 0, Slge.Categories.c 10 3, Slge.Categories.c 2 0, Slge.Categories.c 25 3], Filiyya.darabtu)] do
      IO.println s!"fadla,{key w},{key v},{fd (Filiyya.sortFadla w v)}"
  | ["shibh"] =>
    -- الشواهدُ: الصورتان، والزائدُ، والمرتكزُ، والمحلُّ، والكونُ المحذوف.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let kk := fun (k : Shibh.Kind) => match k with
      | .jarrMajrur => "jarrMajrur" | .zarf => "zarf" | .none => "none"
    let an := fun (a : Shibh.Anchor) => match a with
      | .verb => "verb" | .derived => "derived" | .kawn => "kawn"
    let mh := fun (m : Shibh.Mahall) => match m with
      | .khabar => "khabar" | .naat => "naat" | .hal => "hal" | .sila => "sila" | .unread => "unread"
    for w in [Shibh.fiDar, [Slge.Categories.c 23 0, Slge.Categories.c 26 2, Slge.Categories.c 24 3],
              Shibh.masaan, Shibh.zarf Shibh.masjid, Jumla.zayd] do
      IO.println s!"kind,{key w},{kk (Shibh.kind w)}"
    IO.println s!"zaid,{key (Nawasikh.raf (Majrurat.jarr (Marifa.dropTanwin Shibh.ahad)))},{key (Nawasikh.raf (Marifa.dropTanwin Shibh.ahad))}"
    for w in [Shibh.jalasa, Jumla.qaim, Shibh.ilm] do
      IO.println s!"anchor,{key w},{an (Shibh.anchor w)}"
    for w in [Shibh.ilm, Shibh.tair, Shibh.usfur,
              [Slge.Categories.c 0 0, Slge.Categories.c 23 3, Slge.Categories.c 23 0, Slge.Categories.c 9 1, Slge.Categories.c 28 3]] do
      IO.println s!"mahall,{key w},{mh (Shibh.mahall w)}"
    for m in [Shibh.Mahall.khabar, .naat, .hal, .sila] do
      IO.println s!"kawn,{mh m},{key (Shibh.kawn m)}"
  | ["nisab"] =>
    -- التضمينُ على الأوزان: لكلّ وزنٍ سلسلةُ أسلافه وبعدُه عن الجذر؛ والنسبةُ المقروءةُ على الشواهد.
    for k in List.range Wazn.N do
      IO.println s!"chain,{k},{"-".intercalate ((Nisab.chain k Nisab.F).map toString)},{Nisab.dist k Nisab.F}"
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let nn := fun (n : Nisab.Nisba) => match n with
      | .isnad => "isnad" | .taqyid => "taqyid" | .unread => "unread"
    for (a, b) in [(Nisab.ilm, Nisab.nur), (Filiyya.akala, Jumla.zayd), (Jumla.rajul, Nisab.karim),
                   (Jumla.zayd, Nisab.rakiban), (Nisab.kitabu, Nisab.zaydin), (Nisab.ilm, Jumla.darasa),
                   (Nisab.ilm, Jumla.fidDar), (Jumla.darasa, Jumla.darasa)] do
      IO.println s!"nisba,{key a},{key b},{nn (Nisab.nisba a b)}"
  | ["talil"] =>
    -- السببيّةُ الاشتقاقيّة: لكلّ وزنٍ أسلافُه (عللُه)؛ وأدواتُ التعليل بخاناتها وعملها؛ والتعليلُ المقروء على الشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    for a in List.range Wazn.N do
      for b in List.range Wazn.N do
        if Talil.derives a b then IO.println s!"derives,{a},{b},{Nisab.dist b Nisab.F}"
    let an := fun (a : Talil.Amal) => match a with
      | .jarrIsm => "jarr" | .innaAmal => "inna" | .nasbFil => "nasbFil"
    for (n, cs, a) in Talil.tools do
      IO.println s!"tool,{n},{key cs},{an a}"
    let tn := fun (t : Talil.Talil) => match t with
      | .liAnna => "liAnna" | .liajlih => "liajlih" | .biHarf => "biHarf" | .unread => "unread"
    for (a, b) in [(Jumla.darasa, Talil.hadhar), (Jumla.darasa, Talil.dars), (Jumla.darasa, Talil.bi ++ Talil.darb),
                   (Jumla.darasa, Talil.li ++ Talil.hikma), (Jumla.darasa, Talil.liAnna), (Jumla.darasa, Jumla.zayd),
                   (Filiyya.akala, Filiyya.addars)] do
      IO.println s!"talil,{key a},{key b},{tn (Talil.talil a b)}"
    let t := Talil.tanazu Talil.alimtu Talil.amiltu Talil.alkhayr Talil.hu
    IO.println s!"tanazu,{key t.1},{key t.2.1},{key t.2.2}"
  | ["maqam"] =>
    -- الشخصُ من الخانات لكلّ قالبِ مضارعٍ بصدوره الأربعة على الميزان؛ والشواهدُ: الشخصُ والظهورُ والتوكيد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let sn := fun (s : Option Maqam.Shakhs) => match s with
      | some .mutakallim => "mutakallim" | some .mukhatab => "mukhatab" | some .ghaib => "ghaib"
      | some .mukhatabOrGhaiba => "ta" | none => "none"
    for k in Maqam.presentTemplates do
      for p in [(0 : Fin 29), 25, 3, 28] do
        let v := Maqam.withPrefix p (Wazn.mizan (Sarf.templ k))
        IO.println s!"present,{k},{p},{key v},{sn (Maqam.shakhs v)}"
    for v in [Maqam.adrusu, Maqam.nadrusu, Maqam.tadrusu, Maqam.yadrusu, Maqam.darasat, Maqam.udrus,
              Filiyya.qumtu, Filiyya.darabtu, Jumla.darasa, Jumla.zayd] do
      IO.println s!"shakhs,{key v},{sn (Maqam.shakhs v)}"
    let zn := fun (z : Maqam.Zuhur) => match z with
      | .zahir => "zahir" | .mustatir => "mustatir" | .muttasil => "muttasil"
    for (v, n) in [(Jumla.darasa, some Jumla.zayd), (Maqam.adrusu, some Jumla.zayd),
                   (Jumla.darasa, some Filiyya.addars), (Filiyya.darabtu, none)] do
      IO.println s!"zuhur,{key v},{match n with | some w => key w | none => ""},{zn (Maqam.zuhur v n)}"
    for (v, d) in [(Filiyya.darabtu, Maqam.ana), (Maqam.adrusu, Maqam.ana), (Jumla.darasa, Maqam.huwa),
                   (Maqam.tadrusu, Maqam.anta), (Maqam.tadrusu, Maqam.hiya), (Filiyya.darabtu, Maqam.anta),
                   (Maqam.adrusu, Maqam.huwa), (Jumla.darasa, Jumla.zayd)] do
      IO.println s!"tawkid,{key v},{key d},{Maqam.tawkid v d}"
  | ["jiha"] =>
    -- الصيغةُ من الحالات لكلّ قالبٍ على الميزان (الماضي، الأمر، المضارعُ بصدوره)؛ والجهةُ على الشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let gn := fun (s : Option Jiha.Sigha) => match s with
      | some .madi => "madi" | some .mudari => "mudari" | some .amr => "amr" | none => "none"
    for k in Jiha.pastTemplates ++ Jiha.amrTemplates do
      IO.println s!"sigha,{k},{key (Wazn.mizan (Sarf.templ k))},{gn (Jiha.sigha (Wazn.mizan (Sarf.templ k)))}"
    for k in Jiha.presentTemplates do
      for p in [(0 : Fin 29), 25, 3, 28] do
        let v := Maqam.withPrefix p (Wazn.mizan (Sarf.templ k))
        IO.println s!"sigha,{k},{key v},{gn (Jiha.sigha v)}"
    let jn := fun (j : Jiha.Jiha) => match j with
      | .madi => "madi" | .mudari => "mudari" | .mustaqbal => "mustaqbal" | .madiManfi => "madiManfi"
      | .mustaqbalManfi => "mustaqbalManfi" | .madiMustamirr => "madiMustamirr" | .amr => "amr"
      | .unread => "unread"
    for (a, b) in [([], Jiha.kataba), ([], Jiha.yaktubu), ([], Jiha.sa ++ Jiha.yaktubu), (Jiha.sawfa, Jiha.yaktubu),
                   (Jiha.lam, Jazm.sukun Jiha.yaktubu), (Jiha.lan, Nawasikh.nasb Jiha.yaktubu),
                   (Jiha.kana, Jiha.yaktubu), ([], Jiha.uktub), ([], Jiha.sa ++ Jiha.kataba),
                   (Jiha.sawfa, Jiha.kataba), ([], Jumla.zayd)] do
      IO.println s!"jiha,{key a},{key b},{jn (Jiha.jiha a b)}"
  | ["naat"] =>
    -- المتّجهُ الرباعيّ والنعتُ والحملُ والمحلُّ على الشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let cn := fun (x : Tawabi.CaseClass) => match x with
      | .raf => "raf" | .nasb => "nasb" | .jarr => "jarr" | .nasbJarr => "nasbJarr" | .unread => "unread"
    let gn := fun (g : Jumla.Gender) => match g with | .masc => "masc" | .fem => "fem"
    let nn := fun (n : Jumla.Number) => match n with | .single => "single" | .dual => "dual" | .plural => "plural"
    let hn := fun (h : Naat.Haml) => match h with | .naat => "naat" | .khabar => "khabar" | .unread => "unread"
    let mn := fun (m : Naat.Mahall) => match m with | .naat => "naat" | .hal => "hal" | .unread => "unread"
    let ws := [Naat.alrajul, Naat.rajulun, Naat.rajulan, Naat.alrajuli, Nawasikh.tanwin Naat.madrasa,
               Nawasikh.tanwin Naat.kabira, Jumla.dual Naat.rajul, Nawasikh.tanwin Naat.tawil,
               Nawasikh.tanwin (Nawasikh.nasb Naat.tawil), Marifa.al Naat.tawil, Nawasikh.nasb Naat.alrajul,
               Jumla.darasa]
    for w in ws do
      let v := Naat.vec w
      IO.println s!"vec,{key w},{cn v.cc},{v.definite},{gn v.gender},{nn v.number}"
    for (m, k) in [(Naat.alrajul, Naat.tawil), (Naat.rajulun, Naat.tawil), (Naat.rajulan, Naat.tawil),
                   (Naat.alrajuli, Naat.tawil), (Nawasikh.tanwin Naat.madrasa, Naat.kabira)] do
      IO.println s!"naat,{key m},{key k},{key (Naat.naat m k)},{Naat.naatOk m (Naat.naat m k)}"
    for (m, n) in [(Naat.rajulun, Nawasikh.tanwin (Nawasikh.nasb Naat.tawil)), (Naat.rajulun, Marifa.al Naat.tawil),
                   (Naat.rajulun, Nawasikh.tanwin Naat.kabira), (Jumla.dual Naat.rajul, Nawasikh.tanwin Naat.tawil),
                   (Naat.alrajul, Nawasikh.tanwin Naat.tawil)] do
      IO.println s!"haml,{key m},{key n},{Naat.naatOk m n},{hn (Naat.hamlKind m n)}"
    for w in [Naat.rajulan, Nawasikh.nasb Naat.alrajul, Jumla.darasa, Naat.alrajul] do
      IO.println s!"mahall,{key w},{mn (Naat.jumlaMahall w)}"
  | ["uslub"] =>
    -- الأسلوبُ على الشواهد، ولَا على كلّ قالبِ مضارعٍ بصدوره مجزومًا ومرفوعًا (على الميزان)، والأدوات.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let un := fun (u : Uslub.Uslub) => match u with
      | .khabar => "khabar" | .amr => "amr" | .nahy => "nahy" | .istifham => "istifham" | .nida => "nida"
      | .tamanni => "tamanni" | .tarajji => "tarajji" | .taajjub => "taajjub" | .madhDhamm => "madhDhamm"
      | .unread => "unread"
    for (n, cs, u) in Uslub.tools do
      IO.println s!"tool,{n},{key cs},{un u}"
    for k in Jiha.presentTemplates do
      for p in [(0 : Fin 29), 25, 3, 28] do
        let v := Maqam.withPrefix p (Wazn.mizan (Sarf.templ k))
        IO.println s!"la,{key (Jazm.sukun v)},{un (Uslub.uslub Uslub.la (Jazm.sukun v) none)}"
        IO.println s!"la,{key v},{un (Uslub.uslub Uslub.la v none)}"
    let nasbRajul := Nawasikh.tanwin (Nawasikh.nasb Naat.rajul)
    for (a, b, n) in [([], Jiha.uktub, none), (Uslub.la, Jazm.sukun Uslub.taktub, none), (Uslub.la, Uslub.taktub, none),
                      (Uslub.hal, Uslub.taktub, none), (Uslub.ya, Naat.rajul, none), (Uslub.layta, Jumla.zayd, none),
                      (Uslub.laalla, Jumla.zayd, none), (Uslub.ma, Uslub.akrama, some nasbRajul),
                      (Uslub.ma, Uslub.akrama, some Jumla.zayd), ([], Uslub.nima, none), ([], Jiha.kataba, none),
                      ([], Naat.alrajul, none), ([], Uslub.la, none)] do
      let u := Uslub.uslub a b n
      IO.println s!"uslub,{key a},{key b},{match n with | some w => key w | none => ""},{un u},{Uslub.truthApt u}"
  | ["talab"] =>
    -- صورُ الطلب على الشواهد، ولامُ الأمر على كلّ قالبِ مضارعٍ بصدوره على الميزان، وأسماءُ الفعل.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let sn := fun (s : Option Talab.Sura) => match s with
      | some .sigha => "sigha" | some .lam => "lam" | some .masdar => "masdar" | some .ismFil => "ismFil"
      | none => "none"
    for (n, cs) in Talab.ismFil do
      IO.println s!"ismFil,{n},{key cs},{sn (Talab.talab [] cs)}"
    for k in Jiha.presentTemplates do
      for p in [(0 : Fin 29), 25, 3, 28] do
        let v := Maqam.withPrefix p (Wazn.mizan (Sarf.templ k))
        IO.println s!"lam,{key (Talab.lamAmr v)},{sn (Talab.talab [] (Talab.lamAmr v))}"
        IO.println s!"lamWaw,{key (Talab.lamAmrAfterWaw v)},{sn (Talab.talab Talab.waw (Talab.lamAmrAfterWaw v))}"
    for (a, b) in [([], Jiha.uktub), ([], Talab.lamAmr Jiha.yaktubu), (Talab.waw, Talab.lamAmrAfterWaw Jiha.yaktubu),
                   (Talab.fa, Talab.lamAmrAfterWaw Jiha.yaktubu), ([], Talab.masdarAmr Talab.darb), ([], Talab.sah),
                   ([], Jiha.yaktubu), ([], Jiha.kataba), ([], Talab.lamAmrAfterWaw Jiha.yaktubu),
                   (Jiha.kataba, Talab.masdarAmr Talab.darb)] do
      IO.println s!"talab,{key a},{key b},{sn (Talab.talab a b)}"
  | ["kulli"] =>
    -- الجهةُ الوجوديّة على الميزان لكلّ قالبٍ من الـ121، وعلى الجزئيّات المجدوَلة، وعلى الشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let kn := fun (k : Kulli.Kind) => match k with
      | .juzi => "juzi" | .aradi => "aradi" | .hadath => "hadath" | .fil => "fil" | .jamid => "jamid"
      | .unread => "unread"
    for k in List.range Wazn.N do
      IO.println s!"mizan,{k},{key (Wazn.mizan (Sarf.templ k))},{kn (Kulli.kulli (Wazn.mizan (Sarf.templ k)))}"
    for w in Categories.pronouns ++ Ishara.forms.map (·.2) ++ Marifa.mawsul.map (·.2) do
      IO.println s!"table,{key w},{kn (Kulli.kulli w)}"
    for w in [Kulli.katib, Kulli.kitaba, Nawasikh.tanwin Talab.darb, Jiha.kataba, Jiha.yaktubu, Jiha.uktub,
              Kulli.rajulun, Naat.alrajul, Uslub.la, Kulli.hadha] do
      IO.println s!"kulli,{key w},{kn (Kulli.kulli w)}"
  | ["wad"] =>
    -- الوضعُ على الميزان لكلّ قالبٍ من الـ121 (معانيه وصورُه وقراءتُه)، وأزواجُ الالتقاء، والمتطابقات، والشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let kn := fun (k : Wad.Kind) => match k with
      | .majdul => "majdul" | .mufrad => "mufrad" | .wadMushtarak => "wadMushtarak"
      | .suraMushtarak => "suraMushtarak" | .unread => "unread"
    let ks := fun (l : List Nat) => "+".intercalate (l.map toString)
    for k in List.range Wazn.N do
      let m := Wazn.mizan (Sarf.templ k)
      IO.println s!"mizan,{k},{key m},{ks (Wad.senses m)},{ks (Wad.classes m)},{kn (Wad.wad m)}"
    for (k, q) in Wad.collisionPairs do
      IO.println s!"pair,{k},{q}"
    for (k, q) in Wad.duplicates do
      IO.println s!"dup,{k},{q}"
    for w in [Wad.intishar, Wad.manha, Wad.kitab, Wad.hilal, Wad.ayn, Wad.qamar, Wad.amana, Kulli.katib,
              Jiha.yaktubu, Maqam.huwa, Kulli.hadha, Uslub.la] do
      IO.println s!"wad,{key w},{ks (Wad.senses (Marifa.dropTanwin w))},{kn (Wad.wad w)}"
  | ["tabayun"] =>
    -- عزلةُ القالب وعددُ موادّ الميزان لكلّ قالبٍ من الـ121، وعلاقاتُ الشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let rn := fun (k : Tabayun.Rel) => match k with
      | .munfarid => "munfarid" | .mushtarak => "mushtarak" | .ittihad => "ittihad"
      | .mutabayin => "mutabayin" | .mutadakhil => "mutadakhil" | .unread => "unread"
    for k in List.range Wazn.N do
      let m := Wazn.mizan (Sarf.templ k)
      IO.println s!"mizan,{k},{key m},{Tabayun.isolated k},{(Tabayun.mawadd m).length}"
    for (a, b) in [(Tabayun.darbun, Tabayun.qatl), (Tabayun.qatl, Tabayun.darbun), (Tabayun.darbun, Tabayun.dirab),
                   (Wad.intishar, Tabayun.nashr), (Tabayun.nashr, Wad.intishar), (Wad.kitab, Wad.kitab),
                   (Wad.intishar, Wad.intishar), (Uslub.la, Tabayun.darbun), (Wad.manha, Tabayun.nashr)] do
      IO.println s!"rel,{key a},{key b},{rn (Tabayun.rel a b)}"
  | ["madd"] =>
    -- الأصنافُ الثلاثة والترخيصُ الثلاثيّ والثنائيّ على الميزان لكلّ قالب، ومدودُ الميزان وصلًا ووقفًا، والشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let kk := fun (k : A116.Stages.K) => match k with | .cv => "cv" | .v => "v" | .c => "c"
    let mn := fun (k : Madd.Kind) => match k with
      | .tabii => "tabii" | .muttasil => "muttasil" | .munfasil => "munfasil" | .lazimThaqil => "lazimThaqil"
      | .lazimKhafif => "lazimKhafif" | .arid => "arid" | .lin => "lin" | .silaSughra => "silaSughra"
      | .silaKubra => "silaKubra" | .silent => "silent"
    let hits := fun (l : List (Nat × Madd.Kind)) => "+".intercalate (l.map fun (i, k) => s!"{i}:{mn k}")
    for k in List.range Wazn.N do
      let m := Wazn.mizan (Sarf.templ k)
      IO.println s!"mizan,{k},{key m},{"".intercalate ((Madd.kinds m).map kk)},{Madd.continueLicensed m},{Madd.pauseLicensed m},{A116.Ternary.binOK (Madd.kinds m)},{hits (Madd.madd m [] false)},{hits (Madd.madd m [] true)}"
    for (w, n, p) in [(Madd.qalu, ([] : List SCell), false), (Madd.assama, [], false), (Madd.addallin, [], false),
                      (Madd.alan, [], false), (Madd.alamin, [], true), (Madd.alamin, [], false),
                      (Madd.khawf, [], true), (Madd.khawf, [], false), (Madd.innahu, Madd.kana, false),
                      (Madd.innahu, Madd.illa, false), (Madd.bima, Madd.unzila, false), (Madd.bima, Madd.kana, false),
                      (Madd.amanu, [], false), (Madd.ulaika, [], false), (Madd.addallin, [], true)] do
      IO.println s!"madd,{key w},{key n},{p},{hits (Madd.madd w n p)},{A116.Ternary.binOK (Madd.kinds w)},{Madd.hasVC (Madd.kinds w)}"
  | ["jidh"] =>
    -- تسويةُ الآخر على الميزان لكلّ قالبٍ وكلّ حالة، وقراءاتُ الشواهد (السوابق، أل، الجذع، اللاحقة، القوالب).
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let al := fun (a : Jidh.Al) => match a with | .none => "0" | .full => "1" | .silent => "2"
    let ks := fun (l : List Nat) => "+".intercalate (l.map toString)
    for k in List.range Wazn.N do
      let m := Wazn.mizan (Sarf.templ k)
      let hits := (List.range 4).map fun st => Jidh.onTemplateMod (Sarf.templ k) (Zuruf.setLast m ⟨st % 4, by omega⟩)
      IO.println s!"mizan,{k},{key m},{(Jidh.lastState (Sarf.templ k)).val},{"".intercalate (hits.map fun b => if b then "1" else "0")},{ks (Jidh.stemSenses (Zuruf.setLast m 1))}"
    for w in [Jidh.walard, Jidh.alard, Jidh.washshams, Jidh.rabbi, Jidh.kadhdhabu, Jidh.tajalu, Jidh.bikitabihim,
              Jidh.wajada, Uslub.la, Madd.qalu] do
      let rs := Jidh.jidh w
      IO.println s!"jidh,{key w},{rs.length}"
      for r in rs do
        IO.println s!"reading,{key w},{key r.pre.flatten},{al r.al},{key r.stem},{key r.suf},{ks r.templates},{key r.restore},{key r.asl},{chain r.ilal}"
  | ["ilal"] =>
    -- الصعودُ والنزولُ لكلّ قاعدةٍ وموضعٍ على كلمات الشواهد، والنزولُ حتى خطوتين بسلاسله.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let words := [Ilal.qawala, Ilal.qala, Ilal.qawal, Ilal.qul, Ilal.yaqwulu, Ilal.yaqulu, Ilal.daawa, Ilal.daa,
                  Ilal.yawidu, Ilal.yaidu, Ilal.aamana, Ilal.amana, Ilal.miwzan, Ilal.mizan, Ilal.istabara0,
                  Ilal.istabara, Jidh.kuntum, Jidh.kana, Jidh.daaw, Jidh.jaa, Jidh.kadhdhabu,
                  [Categories.c 24 2, Categories.c 28 3, Categories.c 21 1, Categories.c 25 2], [Categories.c 0 1, Categories.c 11 3, Categories.c 8 0, Categories.c 1 3, Categories.c 8 0], [Categories.c 0 1, Categories.c 27 3, Categories.c 3 0, Categories.c 14 0, Categories.c 23 0]]
    for w in words do
      for (ρ, j) in Ilal.Rule.all.zip (List.range Ilal.Rule.all.length) do
        for i in List.range w.length do
          let a := match Ilal.apply ρ w i with | some v => key v | none => "-"
          IO.println s!"apply,{j},{key w},{i},{a}"
          IO.println s!"undo,{j},{key w},{i},{"|".intercalate ((Ilal.undo ρ w i).map key)}"
          match Ilal.apply ρ w i with
          | some v =>
            let rc := Ilal.record ρ w i
            IO.println s!"record,{j},{key w},{i},{rc.start},{rc.insertedLength},{key rc.removed},{key (A116.Recovery.restoreEdit v rc)}"
          | none => pure ()
      for x in Ilal.descend w w.length do
        IO.println s!"descend,{key w},{chain x.1},{key x.2}"
  | ["maqayis"] =>
    -- الجدولُ المودَع مفكوكًا، والعضويّةُ على شبكةٍ من الجذور وعلى الشواهد، وترتيبُ قراءات الشواهد بالقرينة.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let ks := fun (l : List Nat) => "+".intercalate (l.map toString)
    let fin := fun (n : Nat) => (⟨n % 29, Nat.mod_lt _ (by decide)⟩ : Fin 29)
    let root := fun (a b d : Nat) => (fun i => if i = 0 then fin a else if i = 1 then fin b else fin d : Wazn.Root)
    IO.println s!"size,{Maqayis.table.length}"
    for n in Maqayis.table do
      let (a, b, d) := Maqayis.decode n
      IO.println s!"code,{n},{a},{b},{d}"
    -- شبكةٌ: كلُّ جذرٍ (a, b, d) بخطوة 7 على الحوامل الـ29 — 5×5×5 = 125 جذرًا، وبعضُها في الجدول وبعضُها لا
    for a in [0, 7, 14, 21, 28] do
      for b in [0, 7, 14, 21, 28] do
        for d in [0, 7, 14, 21, 28] do
          IO.println s!"member,{a},{b},{d},{Maqayis.member (root a b d)}"
    for (a, b, d) in [(21, 27, 23), (21, 28, 23), (22, 3, 2), (9, 2, 27), (10, 24, 28), (10, 24, 27), (22, 9, 2),
                      (8, 18, 27), (8, 18, 28), (5, 28, 0), (22, 27, 25), (22, 28, 25)] do
      IO.println s!"member,{a},{b},{d},{Maqayis.member (root a b d)}"
    for w in [Jidh.kadhdhabu, Ilal.qala, Jidh.kuntum, Jidh.kana, Jidh.daaw, Jidh.jaa, Jidh.wajada, Jidh.walard,
              Jidh.bikitabihim, Madd.qalu, Jidh.fariqun, Jidh.tajalu] do
      let rs := Maqayis.rank (Jidh.jidh w)
      IO.println s!"rank,{key w},{rs.length}"
      for r in rs do
        let roots := (Maqayis.Reading.roots r).map fun ρ => s!"{(ρ 0).val}.{(ρ 1).val}.{(ρ 2).val}"
        IO.println s!"reading,{key w},{Maqayis.attested r},{key r.asl},{ks r.templates},{"+".intercalate roots}"
  | ["abniya"] =>
    -- هيكلُ كلّ قالب وعضويّتُه في أبنية سيبويه، وتمايزُ كلّ زوجين، والأزواجُ المسمّاة.
    IO.println s!"size,{Abniya.abniya.length}"
    for k in List.range Wazn.N do
      IO.println s!"skel,{k},{"-".intercalate ((Abniya.skeletonOf (Sarf.templ k)).map toString)},{Abniya.inAbniya (Sarf.templ k)}"
    for k in List.range Wazn.N do
      for q in List.range Wazn.N do
        if k < q then
          IO.println s!"sep,{k},{q},{Abniya.separated (Sarf.templ k) (Sarf.templ q)}"
    for p in Abniya.ambiguous do
      IO.println s!"amb,{p.1},{p.2}"
  | ["adawat"] =>
    -- لكلّ أداة: الصورةُ، الرتبةُ، الأصنافُ، العملُ على شاهدين (اسمٌ وفعلٌ معربان)، ونوعُ العلاقة؛ والترتيبُ على الشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let cat := fun (k : Adawat.Cat) => match k with | .ism => "ism" | .fil => "fil" | .jumla => "jumla" | .ay => "ay"
    let kitabu := [Categories.c 22 1, Categories.c 3 0, Categories.c 1 3, Categories.c 2 2]
    for (a, k) in Adawat.table.zip (List.range Adawat.table.length) do
      IO.println s!"adat,{k},{key a.harf.cells},{a.arity},{"+".intercalate (a.args.map cat)},{repr a.rel},{key (Adawat.apply a kitabu)},{key (Adawat.apply a Adawat.yaktubu)}"
    for (w, p) in [(Jidh.fariqun, Adawat.inna), (Jidh.fariqun, Adawat.lam), (Jidh.wajada, Adawat.lam), (Jidh.kadhdhabu, Adawat.inna),
                   (Madd.qalu, Adawat.lam), (Jidh.walard, [Categories.c 20 1, Categories.c 28 3])] do
      match Adawat.ofCells p with
      | some a =>
        let rs := Adawat.rank a (Maqayis.rank (Jidh.jidh w))
        IO.println s!"rank,{key w},{key p},{rs.length},{"+".intercalate (rs.map fun rd => (if Adawat.fits a rd then "1" else "0") ++ "." ++ (cat (Adawat.catOf rd)))}"
      | none => IO.println s!"rank,{key w},{key p},none,"
  | ["wujud"] =>
    -- جهةُ كلّ قالب، وقراءةُ الكليّ لميزانه، وأبوه في الشبكة؛ وجهةُ قراءات الشواهد.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let on := fun (o : Wujud.Ont) => match o with
      | .fil => "fil" | .masdar => "masdar" | .wasf => "wasf" | .zarfAla => "zarfAla" | .jam => "jam" | .ism => "ism"
    let kn := fun (k : Kulli.Kind) => match k with
      | .juzi => "juzi" | .aradi => "aradi" | .hadath => "hadath" | .fil => "fil" | .jamid => "jamid" | .unread => "unread"
    for k in List.range Wazn.N do
      let p := match Shabaka.parentOf k with | some p => toString p | none => "-"
      IO.println s!"ont,{k},{on (Wujud.ontOf k)},{kn (Kulli.kulli (Wazn.mizan (Sarf.templ k)))},{p}"
    for w in [Jidh.fariqun, Jidh.kadhdhabu, Ilal.qala, Jidh.wajada, Jidh.bikitabihim, Madd.qalu, Jidh.walard] do
      IO.println s!"reading,{key w},{"+".intercalate ((Jidh.jidh w).map fun rd => on (Wujud.ontOfReading rd))}"
  | ["maani"] =>
    -- معاني كلّ حرفٍ بترتيب المصدر، والترتيبُ بالقرينتين على شواهد؛ وظرفيّةُ صورٍ من الجدولين.
    let key := fun (w : List SCell) => "-".intercalate (w.map fun c => toString c.index)
    let sn := fun (s : Maani.Sense) => ((repr s).pretty.splitOn ".").getLastD ""
    for p in Maani.table do
      IO.println s!"senses,{p.1},{"+".intercalate (p.2.map sn)}"
    for h in [5, 9, 0, 1, 6] do
      for q in [({} : Maani.Clue), {nafyBefore := true}, {zarfAfter := true}, {nafyBefore := true, zarfAfter := true}] do
        IO.println s!"rank,{h},{q.nafyBefore},{q.zarfAfter},{"+".intercalate ((Maani.rank q (Maani.sensesOf h)).map sn)}"
    for w in [Zuruf.jarr (Zuruf.stems.getD 0 ("", [])).2, Zuruf.jarr (Zaman.stems.getD 0 ("", [])).2, Jidh.fariqun, Shibh.ilm] do
      IO.println s!"zarf,{key w},{Maani.isZarf w}"
  | ["mukhassas"] =>
    -- الشجرةُ (معرّف، مستوى، أب، كتاب، جذور) والقابليّاتُ الموروثة لكلّ كتاب، والحكمُ على شواهد.
    for n in Mukhassas.nodes do
      IO.println s!"node,{n.1},{n.2.1},{n.2.2.1},{n.2.2.2.1},{"+".intercalate (n.2.2.2.2.map toString)}"
    for n in Mukhassas.nodes do
      if n.2.1 == 1 then
        IO.println s!"under,{n.1},{"+".intercalate ((Mukhassas.capsUnder n.1).map toString)}"
    for (b, r) in [(163, 22018), (1, 22018), (979, 4829), (617, 22018), (664, 4829)] do
      let g := match Mukhassas.judgeIn b r with | .mafhum w => s!"mafhum:{w}" | .malumah => "malumah"
      IO.println s!"judge,{b},{r},{g}"
  | ["rank"] =>
    for g1 in [Rank.Grade.zanni, .qati] do
      for s1 in [1, 2, 3] do
        for g2 in [Rank.Grade.zanni, .qati] do
          for s2 in [1, 2, 3] do
            for (x, y) in [(false, false), (true, false), (false, true)] do
              let v := Rank.weighS ⟨g1, s1⟩ ⟨g2, s2⟩ x y
              IO.println s!"{gradeName g1},{s1},{x},{gradeName g2},{s2},{y},{verdictName v}"
  | _ => IO.eprintln "usage: slge-table bridge|counts|folds|ghazali|rank|rasm"
