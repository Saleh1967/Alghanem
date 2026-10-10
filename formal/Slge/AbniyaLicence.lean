import Slge.AbniyaLicenceTable
import Slge.AbniyaTable
import Slge.Madd

/-!
# أبنيةُ سيبويه على الترخيص الثلاثيّ: لكلّ هيكلٍ شاهدٌ مرخَّصٌ وصلًا ووقفًا، وهمزةُ الوصل هي الفارق (ADR ٣٦)

الهيكلُ في المودَع (`Abniya.abniya`، 158) حواملُ بلا حركات؛ و`AbniyaLicenceTable.witnesses` لكلّ هيكلٍ تشكيلٌ
مولَّدٌ (أوّلُ مرخَّصٍ بترتيب الحالات — سقفٌ لا تشكيلُ سيبويه). المبرهَن **على الشواهد** (`decide`):

* `witnesses_cover`: الشواهدُ للهياكل الـ158 بعينها وبترتيبها.
* `witnesses_match`: حواملُ كلّ شاهدٍ هي هيكلُه، إلّا الألفَ الأولى فهمزةٌ (همزةُ الوصل ابتداءً).
* `witnesses_licensed`: كلُّ شاهدٍ مرخَّصٌ وصلًا ووقفًا (`Madd.continueLicensed`، `pauseLicensed`).
* `witnesses_alif_sukun`: لا ألفَ متحرّكةً في شاهد (الألفُ لا تكون إلّا ساكنة).
* `wasl_is_the_difference`: في هياكل همزة الوصل (13)، الشاهدُ نفسُه بألفٍ ساكنةٍ أوّلًا كما رُسمت لا يُرخَّص —
  فالقاعدةُ (لا ابتداءَ بساكن، والهمزةُ تُجتلب) هي ما يُدخل هذه الأبنية، لا الهيكل.

وعددُ التشكيلات المرخَّصة لكلّ هيكلٍ محسوبٌ على المودَع في `ABNIYA_LICENCE_INDEX.md`؛ ومنه أنّ هياكلَ همزة الوصل
بلا القاعدة لا يُرخَّص لها تشكيلٌ أصلًا (فحصٌ شاملٌ لتشكيلاتها كلِّها في `test_abniya_licence.py`).
-/

namespace Slge.AbniyaLicence

open Slge.AbniyaLicenceTable (witnesses)
open Slge.Categories (c)

/-- الهيكلُ بهمزة الوصل ابتداءً: الألفُ الأولى (1) همزةٌ (0). -/
def waslize : List Nat → List Nat
  | 1 :: t => 0 :: t
  | s => s

/-- الشاهدُ بألفٍ ساكنةٍ أوّلًا كما رُسم الهيكل. -/
def asWritten : List SCell → List SCell
  | _ :: t => c 1 3 :: t
  | [] => []

def isWasl (s : List Nat) : Bool := s.head? == some 1

set_option maxRecDepth 100000 in
theorem witnesses_cover : witnesses.map (·.1) = Abniya.abniya := by decide

set_option maxRecDepth 100000 in
theorem witnesses_match :
    witnesses.all (fun p => p.2.map (fun x => x.carrier.val) == waslize p.1) = true := by decide

set_option maxRecDepth 100000 in
theorem witnesses_licensed :
    witnesses.all (fun p => Madd.continueLicensed p.2 && Madd.pauseLicensed p.2) = true := by
  decide +kernel

set_option maxRecDepth 100000 in
theorem witnesses_alif_sukun :
    witnesses.all (fun p => p.2.all (fun x => x.carrier.val != 1 || x.state.val == 3)) = true := by
  decide

set_option maxRecDepth 100000 in
theorem wasl_is_the_difference :
    (witnesses.filter (fun p => isWasl p.1)).length = 13 ∧
      (witnesses.filter (fun p => isWasl p.1)).all
        (fun p => !Madd.continueLicensed (asWritten p.2) && !Madd.pauseLicensed (asWritten p.2))
        = true := by
  decide +kernel

end Slge.AbniyaLicence
