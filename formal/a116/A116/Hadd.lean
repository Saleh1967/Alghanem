import A116.Ternary
import A116.Ladder

/-!
# التقاءُ الساكنين على حدّه: قافيةُ المدّ (CVVC) لا تُرخَّص وصلًا إلّا والمُغلِقُ أوّلُ مثلين

## الدَّينُ الذي تسدّه هذه الوحدة

`Ternary.ContinueLicensed` يقرأ الأصنافَ `cv | v | c` وحدَها، فـ«حَاجَّ» (`حَ اْ جْ جَ`) و«قَالْتُ»
(`قَ اْ لْ تُ`) عنده سلسلةٌ واحدة `cv v c cv`، فيقبلهما معًا؛ والثنائيُّ (`Admissible`) يرفضهما معًا.
والقيدُ الذي يفرّق بينهما يقرأ **هويّةَ الحامل**: المُغلِقُ بعد المدّ يساوي حاملُه حاملَ الخانة التي
بعده (تضعيف)، أي «التقاءُ الساكنين على حدّه». وكان هذا دَينًا مسمًّى في `tests/test_ilal.py` و
`tests/test_residue.py`.

## ما يُعرَّف هنا

* `kindOf`: إسقاطُ الخانات على أصنافها (`cv` متحرّك؛ `v` حرفُ مدٍّ ساكنٌ بعد حركته المجانسة: ا بعد
  فتحة، و بعد ضمّة، ي بعد كسرة؛ وإلّا `c`). كان في `gate.licence.kind_of` «معلنًا لا مبرهنًا»؛ وهو
  هنا تعريفٌ في Lean يطابقه البايثون بجدولٍ مولَّد (`lake exe a116-table hadd`).
  **تنبيه:** «ساكن» في الخانة معناه موضعيٌّ — «موضعٌ لا تتبعه حركةٌ قصيرة» — لا «عدمُ الحركة نطقًا»؛
  فحرفُ المدّ خانةٌ ساكنةٌ موضعًا وجزءٌ ثانٍ من حركةٍ طويلةٍ نطقًا، ودورُه `v` هو ما يفرّقه.
* `geminateB`: كلُّ `v` يليه `c` فالـ`c` يليه خانةٌ بحامله نفسه.
* `isFarq`: **مدُّ الفرق** (آلْآنَ): همزةٌ مفتوحةٌ ثمّ ألفُ مدٍّ ثمّ لامٌ ساكنة في أوّل الكلمة — الاستثناءُ
  الوحيد المشهود في المدوّنة المختومة؛ معلنٌ من اصطلاح القرّاء، وموضعُ نصّه في مصدرٍ مسمًّى لم يُتحقَّق
  في هذه الوحدة (`MADD_AL_FARQ_SOURCE_LOCUS_UNVERIFIED`).
* `strictB`: `continueB (kindOf w) && haddB w`.

## المبرهنات

* `strictB_continue`: كلُّ مرخَّصٍ بالقيد مرخَّصٌ ثلاثيًّا (القيدُ تضييقٌ لا توسيع).
* `geminateB_vc_carrier`: **لكلّ** موضعٍ في **أيّ** سلسلةٍ مقبولة: إن تلا `v` صنفُ `c` فحاملُ الـ`c`
  هو حاملُ ما بعده.
* `strict_cvvc_is_geminate`: الشيءُ نفسُه على الخانات: كلُّ كلمةٍ مرخَّصةٍ بالقيد (غيرِ مدّ الفرق)
  كلُّ قافيةِ مدٍّ فيها مدغمة.
* `geminateB_vc_final`: `v` ثمّ `c` في الآخر لا يُقبل وصلًا.
* `hadd_debt_closed`: «قَالْتُ» مرخَّصةٌ ثلاثيًّا ومرفوضةٌ بالقيد — الدَّينُ المسمّى مسدود.
* `hajja_strict`، `dallina_strict`، `qultu_strict`، `alaana_strict`: الشواهدُ الموجبة.
* `farq_needs_its_hamza`: الطفرةُ المرفوضة — الصورةُ نفسُها بغير همزة الاستفهام في أوّلها مرفوضة؛
  فالاستثناءُ لا يتّسع لكلّ مدٍّ قبل لام.
* `kindOf_hajja`: إسقاطُ خانات «حَاجَّ» هو `Ternary.hajja` بعينه.
* **الحدّ بين كلمتين** (`strictJoinB`): الاستثناءُ داخلَ الكلمة الواحدة وحدَها. `straddle_rejected` (مدٌّ آخرَ
  الأولى ومُغلِقٌ أوّلَ الثانية مرفوضٌ لكلّ طول)، `strictJoinB_strict`، `strictJoinB_nil`، والعيبُ المسدود
  `ya_shafiina_straddles` (يَا + الشَّافِعِينَ: يقبله `strictB` موصولًا ويرفضه `strictJoinB`)، وشاهدا القبول
  `quli_dallina_join` و`quli_lhamdu_join`.

ولا يُبرهَن هنا أنّ هذا القيدَ هو قانونُ العربيّة: Lean يُبرهن خواصَّ التعريف على الخانات؛ ومطابقتُه
للمرويّ مقيسةٌ على المدوّنة المختومة (`tests/test_hadd.py`).
-/

namespace A116.Hadd

open A116 A116.Stages A116.Ladder

/-- الحركةُ المجانسة لحرف المدّ، إن كان حاملُه حرفَ مدّ. -/
def maddVowel (k : Fin carrierCount) : Option Haraka :=
  if k = carrierOf 'ا' then some .fatha
  else if k = carrierOf 'و' then some .damma
  else if k = carrierOf 'ي' then some .kasra
  else none

/-- صنفُ الخانة بحسب حالة ما قبلها. -/
def kindOne (prev : Option Haraka) (x : Cell) : K :=
  if x.haraka ≠ .sukun then .cv
  else
    match prev, maddVowel x.carrier with
    | some a, some b => if a = b then .v else .c
    | _, _ => .c

def kindGo : Option Haraka → List Cell → List K
  | _, [] => []
  | p, x :: t => kindOne p x :: kindGo (some x.haraka) t

/-- إسقاطُ الخانات على الأصناف الثلاثة (مرآتُه `gate.licence.kind_of`). -/
def kindOf (w : List Cell) : List K := kindGo none w

theorem kindGo_length : ∀ (p : Option Haraka) (w : List Cell), (kindGo p w).length = w.length
  | _, [] => rfl
  | p, x :: t => by simp [kindGo, kindGo_length _ t]

/-- شرطُ الموضع الواحد: إن كان `v` وتلاه `c` فالـ`c` يليه حاملُه نفسُه. -/
def stepOK : K × Cell → List (K × Cell) → Bool
  | (.v, _), (.c, x) :: (_, y) :: _ => x.carrier == y.carrier
  | (.v, _), [(.c, _)] => false
  | _, _ => true

/-- كلُّ `v` يليه `c`: المُغلِقُ أوّلُ مثلين (يليه حاملُه نفسُه). -/
def geminateB : List (K × Cell) → Bool
  | [] => true
  | a :: tl => stepOK a tl && geminateB tl

/-- مدُّ الفرق: ءَ اْ لْ في أوّل الكلمة. -/
def isFarq : List Cell → Bool
  | h :: a :: l :: _ => h == atom 'ء' .fatha && a == atom 'ا' .sukun && l.carrier == carrierOf 'ل'
  | _ => false

def haddB (w : List Cell) : Bool :=
  let p := (kindOf w).zip w
  if isFarq w then geminateB (p.drop 2) else geminateB p

/-- الترخيصُ الثلاثيّ وصلًا مع قيد الحدّ. -/
def strictB (w : List Cell) : Bool := Ternary.continueB (kindOf w) && haddB w

/-! ## المبرهنات العامّة -/

theorem strictB_continue {w : List Cell} (h : strictB w = true) :
    Ternary.ContinueLicensed (kindOf w) := by
  simp only [strictB, Bool.and_eq_true] at h
  exact (Ternary.continueB_iff _).1 h.1

theorem geminateB_cons_true {a : K × Cell} {tl : List (K × Cell)}
    (h : geminateB (a :: tl) = true) : geminateB tl = true := by
  simp only [geminateB, Bool.and_eq_true] at h
  exact h.2

/-- **الحدّ لكلّ موضع:** في كلّ سلسلةٍ مقبولة، `v` ثمّ `c` ثمّ خانة ⇒ حاملُ الـ`c` حاملُ ما بعده. -/
theorem geminateB_vc_carrier :
    ∀ (p q : List (K × Cell)) (a x y : Cell) (k : K),
      geminateB (p ++ (.v, a) :: (.c, x) :: (k, y) :: q) = true → x.carrier = y.carrier
  | [], q, a, x, y, k, h => by
    simp only [List.nil_append, geminateB, Bool.and_eq_true] at h
    simpa [stepOK] using h.1
  | b :: p, q, a, x, y, k, h =>
    geminateB_vc_carrier p q a x y k (geminateB_cons_true (by simpa using h))

/-- `v` ثمّ `c` في آخر السلسلة: لا مثلَ بعد المُغلِق، فلا قبول. -/
theorem geminateB_vc_final :
    ∀ (p : List (K × Cell)) (a x : Cell), geminateB (p ++ [(.v, a), (.c, x)]) = false
  | [], a, x => by simp [geminateB, stepOK]
  | b :: p, a, x => by
    have ih := geminateB_vc_final p a x
    cases h : geminateB (b :: p ++ [(.v, a), (.c, x)]) with
    | false => rfl
    | true => exact absurd (geminateB_cons_true (by simpa using h)) (by simp [ih])

/-- **على الخانات:** في كلّ كلمةٍ مرخَّصةٍ بالقيد ليست مدَّ فرق، كلُّ مدٍّ يليه مُغلِقٌ فالمُغلِقُ أوّلُ مثلين،
بأيّ طولٍ وفي أيّ موضع. -/
theorem strict_cvvc_is_geminate {w : List Cell} (h : strictB w = true) (hf : isFarq w = false)
    {p q : List (K × Cell)} {a x y : Cell} {k : K}
    (hz : (kindOf w).zip w = p ++ (.v, a) :: (.c, x) :: (k, y) :: q) : x.carrier = y.carrier := by
  simp only [strictB, haddB, hf, Bool.and_eq_true] at h
  rw [hz] at h
  exact geminateB_vc_carrier p q a x y k (by simpa using h.2)

/-! ## الشواهد (بالحساب على خاناتٍ مسمّاة) -/

theorem cited_letters_are_carriers :
    ['ح', 'ا', 'ج', 'ق', 'ل', 'ت', 'ض', 'ب', 'ء', 'ن', 'و', 'ي'].all
      (Field112.carriers29.contains ·) = true := by
  decide

open Haraka in
/-- حَاجَّ: `حَ اْ جْ جَ`. -/
def hajjaCells : List Cell := [atom 'ح' fatha, atom 'ا' sukun, atom 'ج' sukun, atom 'ج' fatha]
open Haraka in
/-- قَالْتُ (الأصلُ المعلّ): `قَ اْ لْ تُ`. -/
def qaaltu : List Cell := [atom 'ق' fatha, atom 'ا' sukun, atom 'ل' sukun, atom 'ت' damma]
open Haraka in
/-- قُلْتُ: `قُ لْ تُ`. -/
def qultu : List Cell := [atom 'ق' damma, atom 'ل' sukun, atom 'ت' damma]
open Haraka in
/-- ضَالِّينَ: `ضَ اْ لْ لِ يْ نَ` (مدٌّ قبل مضعَّف، ثمّ مدٌّ قبل متحرّك). -/
def dallina : List Cell :=
  [atom 'ض' fatha, atom 'ا' sukun, atom 'ل' sukun, atom 'ل' kasra, atom 'ي' sukun, atom 'ن' fatha]
open Haraka in
/-- آلْآنَ: `ءَ اْ لْ ءَ اْ نَ`. -/
def alaana : List Cell :=
  [atom 'ء' fatha, atom 'ا' sukun, atom 'ل' sukun, atom 'ء' fatha, atom 'ا' sukun, atom 'ن' fatha]
open Haraka in
/-- الطفرة: آلْآنَ بغير همزة الاستفهام (`بَ اْ لْ ءَ اْ نَ`). -/
def baalaana : List Cell :=
  [atom 'ب' fatha, atom 'ا' sukun, atom 'ل' sukun, atom 'ء' fatha, atom 'ا' sukun, atom 'ن' fatha]

theorem kindOf_hajja : kindOf hajjaCells = Ternary.hajja := by decide

/-- `continueB` على وصل مقاطع: `parse` معرَّفٌ بالاستقراء المؤسَّس فلا تحسبه النواةُ مباشرةً، فيُمرّ
بمبرهنة `Stages.parse_flat`. -/
theorem continueB_flat (ss : List Syl) :
    Ternary.continueB (flat .none ss) = ss.all fun s => !Ternary.pauseOnly s := by
  simp [Ternary.continueB, parse_flat]

/-- **الدَّينُ المسمّى مسدود:** قَالْتُ مقبولةٌ ثلاثيًّا (CVVC + CV) ومرفوضةٌ بقيد الحدّ. -/
theorem hadd_debt_closed :
    Ternary.continueB (kindOf qaaltu) = true ∧ strictB qaaltu = false := by
  have hk : kindOf qaaltu = flat .none [.CVVC, .CV] := by decide
  simp only [strictB, hk, continueB_flat]
  decide

theorem hajja_strict : strictB hajjaCells = true := by
  have hk : kindOf hajjaCells = flat .none [.CVVC, .CV] := by decide
  simp only [strictB, hk, continueB_flat]
  decide

theorem dallina_strict : strictB dallina = true := by
  have hk : kindOf dallina = flat .none [.CVVC, .CVV, .CV] := by decide
  simp only [strictB, hk, continueB_flat]
  decide

theorem qultu_strict : strictB qultu = true := by
  have hk : kindOf qultu = flat .none [.CVC, .CV] := by decide
  simp only [strictB, hk, continueB_flat]
  decide

theorem alaana_strict : strictB alaana = true := by
  have hk : kindOf alaana = flat .none [.CVVC, .CVV, .CV] := by decide
  simp only [strictB, hk, continueB_flat]
  decide

/-- الاستثناءُ لا يتّسع: بلا همزة الاستفهام في الأوّل تُرفض الصورةُ نفسُها. -/
theorem farq_needs_its_hamza :
    Ternary.continueB (kindOf baalaana) = true ∧ strictB baalaana = false := by
  have hk : kindOf baalaana = flat .none [.CVVC, .CVV, .CV] := by decide
  simp only [strictB, hk, continueB_flat]
  decide

/-! ## الحدُّ بين كلمتين: الاستثناءُ داخلَ الكلمة الواحدة وحدَها

شرطُ باب «دابّة» عند المؤلّف أن يكون المدُّ والمدغمُ «من كلمةٍ واحدة». فإن كان المدُّ آخرَ الأولى
والمدغمُ أوّلَ الثانية (يَا + الشَّافِعِينَ ← `يَ اْ | شْ شَ …`) فالمدُّ يُقصَّر نطقًا، والقافيةُ ليست
على حدّها. `strictB` على السلسلة الموصولة لا يرى الحدّ فيقبلها؛ و`strictJoinB` يرفض كلَّ `v` يليه
`c` إن وقع الحدُّ بين المدّ وما بعد المُغلِق. -/

/-- قافيةُ مدٍّ يقطعها الحدّ: `v | c` أو `v c | x`، حيث `b` طولُ الكلمة الأولى. -/
def straddles (l r : List Cell) : Bool :=
  let k := kindOf (l ++ r)
  let b := l.length
  (decide (1 ≤ b) && k[b - 1]? == some .v && k[b]? == some .c) ||
    (decide (2 ≤ b) && k[b - 2]? == some .v && k[b - 1]? == some .c)

/-- الوصلُ مرخَّصٌ بقيد الحدّ: مرخَّصٌ موصولًا، ولا قافيةَ مدٍّ يقطعها الحدّ. -/
def strictJoinB (l r : List Cell) : Bool := strictB (l ++ r) && !straddles l r

theorem strictJoinB_strict {l r : List Cell} (h : strictJoinB l r = true) : strictB (l ++ r) = true := by
  simp only [strictJoinB, Bool.and_eq_true] at h
  exact h.1

/-- بلا كلمةٍ أولى لا حدَّ: القيدُ هو `strictB` بعينه. -/
theorem strictJoinB_nil (r : List Cell) : strictJoinB [] r = strictB r := by
  simp [strictJoinB, straddles]

/-- **الحدُّ لكلّ طول:** مدٌّ آخرَ الأولى يليه مُغلِقٌ أوّلَ الثانية — مرفوضٌ مهما كان بعده. -/
theorem straddle_rejected (l r : List Cell) (hb : 1 ≤ l.length)
    (hv : (kindOf (l ++ r))[l.length - 1]? = some .v) (hc : (kindOf (l ++ r))[l.length]? = some .c) :
    strictJoinB l r = false := by
  simp [strictJoinB, straddles, hb, hv, hc]

theorem cited_join_letters_are_carriers :
    ['ش', 'ف', 'ع', 'ح', 'م', 'د'].all (Field112.carriers29.contains ·) = true := by
  decide

open Haraka in
/-- «يَا» كما تحملها الشهادة: `يَ اْ`. -/
def ya : List Cell := [atom 'ي' fatha, atom 'ا' sukun]
open Haraka in
/-- «الشَّافِعِينَ» موصولةً: سقطت همزةُ الوصل ولامُ الشمسيّة بقيّةٌ (`شْ شَ اْ فِ عِ يْ نَ`). -/
def shshafiina : List Cell :=
  [atom 'ش' sukun, atom 'ش' fatha, atom 'ا' sukun, atom 'ف' kasra, atom 'ع' kasra, atom 'ي' sukun,
    atom 'ن' fatha]
open Haraka in
/-- «قُلِ»: `قُ لِ`. -/
def quli : List Cell := [atom 'ق' damma, atom 'ل' kasra]
open Haraka in
/-- «الْحَمْدُ» موصولةً: `لْ حَ مْ دُ`. -/
def lhamdu : List Cell := [atom 'ل' sukun, atom 'ح' fatha, atom 'م' sukun, atom 'د' damma]

/-- **العيبُ مسمًّى ومسدود:** `strictB` على الموصول يقبل «يَا + الشَّافِعِينَ»، و`strictJoinB` يرفضه. -/
theorem ya_shafiina_straddles :
    strictB (ya ++ shshafiina) = true ∧ strictJoinB ya shshafiina = false := by
  have hk : kindOf (ya ++ shshafiina) = flat .none [.CVVC, .CVV, .CV, .CVV, .CV] := by decide
  refine ⟨?_, ?_⟩
  · simp only [strictB, hk, continueB_flat]; decide
  · simp only [strictJoinB, strictB, hk, continueB_flat]; decide

/-- المدُّ والمدغمُ في الكلمة الثانية وحدَها (قُلِ + ضَالِّينَ): مقبول. -/
theorem quli_dallina_join : strictJoinB quli dallina = true := by
  have hk : kindOf (quli ++ dallina) = flat .none [.CV, .CV, .CVVC, .CVV, .CV] := by decide
  simp only [strictJoinB, strictB, hk, continueB_flat]; decide

/-- الوصلُ بعد متحرّك (قُلِ + الْحَمْدُ): مقبول. -/
theorem quli_lhamdu_join : strictJoinB quli lhamdu = true := by
  have hk : kindOf (quli ++ lhamdu) = flat .none [.CV, .CVC, .CVC, .CV] := by decide
  simp only [strictJoinB, strictB, hk, continueB_flat]; decide

end A116.Hadd
