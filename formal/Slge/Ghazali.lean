/-!
# صورُ الشرطيّ المتّصل عند الغزالي — جدولٌ من أربع خاناتٍ ثنائيّة

في «معيار العلم» و«محكّ النظر»: إذا كان المقدَّمُ أخصَّ من التالي («إن كان إنسانًا
فهو حيوان») أنتج **عينُ المقدَّم** عينَ التالي، و**نقيضُ التالي** نقيضَ المقدَّم،
ولم ينتج نقيضُ المقدَّم ولا عينُ التالي («إذ ربما يكون فرسًا»). وإذا كانا متساويين
(«إن كانت الشمسُ طالعةً فالنهارُ موجود») أنتجت الصورُ الأربع.

وهنا تُبرهَن هذه الدعوى **بالبتات**: الشرطيّةُ قيدٌ على زوجٍ ثنائيٍّ ‎(أ، ب)‎،
والصورةُ منتجةٌ إذا صدقت نتيجتُها في كلّ نموذجٍ من النماذج الأربعة يصدق فيه القيدُ
والمقدّمةُ الصغرى. فجدولُ الغزالي **نتيجةٌ** لا مُدخَل (`ghazali_table`)، وعقمُ
الصورتين **مشهودٌ بنموذجين** (`barren_witnessed`).

النظيرُ البايثونيّ: `slge.knowledge.PRODUCTIVE`، تطابقه `tests/test_conformance.py`.
-/

namespace Slge.Ghazali

/-- درجةُ اللزوم: المقدَّمُ أخصُّ من التالي، أو مساوٍ له. -/
inductive Degree where
  | akhass
  | musawi
  deriving DecidableEq, Repr

/-- الصورُ الأربع. -/
inductive Form where
  | aynMuqaddam
  | naqidTali
  | naqidMuqaddam
  | aynTali
  deriving DecidableEq, Repr

/-- القيد: الأخصُّ لزومٌ ‎(أ ⇒ ب)‎، والمساوي تلازمٌ ‎(أ ⇔ ب)‎. -/
def holds : Degree → Bool → Bool → Bool
  | .akhass, a, b => !a || b
  | .musawi, a, b => a == b

/-- المقدّمةُ الصغرى (ما يُعطى). -/
def premise : Form → Bool → Bool → Bool
  | .aynMuqaddam, a, _ => a
  | .naqidTali, _, b => !b
  | .naqidMuqaddam, a, _ => !a
  | .aynTali, _, b => b

/-- النتيجةُ المطلوبة. -/
def conclusion : Form → Bool → Bool → Bool
  | .aynMuqaddam, _, b => b
  | .naqidTali, a, _ => !a
  | .naqidMuqaddam, _, b => !b
  | .aynTali, a, _ => a

/-- النماذجُ الأربعة. -/
def models : List (Bool × Bool) := [(false, false), (false, true), (true, false), (true, true)]

/-- منتجةٌ: النتيجةُ صادقةٌ في كلّ نموذجٍ يصدق فيه القيدُ والمقدّمة. -/
def productive (d : Degree) (f : Form) : Bool :=
  models.all fun (a, b) => !(holds d a b && premise f a b) || conclusion f a b

/-- الجدولُ كما نصّه الغزالي. -/
def stated : Degree → Form → Bool
  | .akhass, .aynMuqaddam => true
  | .akhass, .naqidTali => true
  | .akhass, _ => false
  | .musawi, _ => true

/-- **الجدولُ نتيجة:** المنتِجُ بالبتات هو المنتِجُ عند الغزالي، خانةً خانة. -/
theorem ghazali_table (d : Degree) (f : Form) : productive d f = stated d f := by
  cases d <;> cases f <;> decide

/-- النماذجُ التي يصدق فيها القيدُ والمقدّمة. -/
def admitted (d : Degree) (f : Form) : List (Bool × Bool) :=
  models.filter fun (a, b) => holds d a b && premise f a b

/-- **العقمُ مشهود:** في الصورتين العقيمتين من الأخصّ نموذجان مقبولان تختلف فيهما
النتيجة؛ فلا يلزم إثباتٌ ولا نفي («ربما يكون فرسًا»، وربما يكون حجرًا). -/
theorem barren_witnessed :
    (admitted .akhass .naqidMuqaddam).map (fun (a, b) => conclusion .naqidMuqaddam a b)
        = [true, false] ∧
      (admitted .akhass .aynTali).map (fun (a, b) => conclusion .aynTali a b)
        = [false, true] := by
  decide

/-- **الموافقةُ سلسلة:** الأخصُّ متعدٍّ، فـ«أفّ ⇒ أذى ⇒ محرَّم» تنتج «أفّ ⇒ محرَّم». -/
theorem akhass_chain (a b c : Bool) :
    holds .akhass a b = true → holds .akhass b c = true → holds .akhass a c = true := by
  cases a <;> cases b <;> cases c <;> decide

/-- **الرافعُ إلى المساواة يُنتج:** إذا قام دليلٌ على أنّ العلّةَ واحدة (الأخصُّ صار
مساويًا) أنتج نقيضُ المقدَّم، وهو مفهومُ المخالفة. -/
theorem licence_makes_mafhum : productive .musawi .naqidMuqaddam = true := by decide

end Slge.Ghazali
