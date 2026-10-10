import Slge.GhazaliTable

/-!
# مراسي جدول الغزاليّ: الخاناتُ الثماني بسطرها، والموافقُ للنبهانيّ منها (ADR ٣٣)

`Slge.Ghazali.stated` جدولٌ كُتب باليد؛ و`GhazaliTable.rows` مولَّدٌ من المختومات الثلاثة (معيار العلم،
المستصفى، محكّ النظر) كلُّ خانةٍ بسطرها وعبارتها، ومن ج3 و«التفكير» للنبهانيّ. المبرهَنُ هنا بناءُ الجدول لا
اللغة ولا المنطق:

* الخاناتُ الثماني كلُّها مرساةٌ بلا تكرار (`cells_cover`)، وقيمتُها المرساةُ هي ما نصّه الجدولُ اليدويّ
  (`cells_agree`) وهي المنتِجُ بالبتات (`anchored_is_productive`) — فصار الجدولُ المبرهَنُ مربوطًا بسطره.
* خاناتُ المنطق **رأيٌ ثانٍ** بإذن المالك: مرساةٌ عند الغزاليّ ولا مرساةَ لها في النبهانيّ
  (`logic_is_second_opinion`)، ومنهجُه في المنطق مرسًى من العمود وحده (`manhaj_from_spine`).
* القراءتان الأصوليّتان (مفهومُ الموافقة، مفهومُ المخالفة بالشرط) **موافقتان**: مرساتان في المودَعَين معًا،
  وصورتاهما منتِجتان (`usul_agreed_and_productive`).
* مراسي الغزاليّ من مودَعاته الثلاثة ومراسي النبهانيّ من العمود لا غير (`sources_named`).
-/

namespace Slge.GhazaliAnchors

open Slge.Ghazali Slge.GhazaliTable

/-- خاناتُ المنطق (الصنف 0). -/
def cells : List Row := rows.filter (·.kind == 0)

/-- القراءتان الأصوليّتان (الصنف 1). -/
def usul : List Row := rows.filter (·.kind == 1)

/-- منهجُ النبهانيّ في المنطق (الصنف 2). -/
def manhaj : List Row := rows.filter (·.kind == 2)

/-- الخاناتُ الثماني كلُّها، كلٌّ مرّة: (الدرجة، الصورة) بترتيب الجدول. -/
theorem cells_cover :
    cells.map (fun r => (r.degree, r.form)) =
      [(.akhass, .aynMuqaddam), (.akhass, .naqidTali), (.akhass, .naqidMuqaddam), (.akhass, .aynTali),
       (.musawi, .aynMuqaddam), (.musawi, .naqidTali), (.musawi, .naqidMuqaddam), (.musawi, .aynTali)] := by
  decide

/-- القيمةُ المرساةُ بسطرها هي ما نصّه الجدولُ اليدويّ، خانةً خانة. -/
theorem cells_agree : cells.all (fun r => r.stated == stated r.degree r.form) = true := by decide

/-- والقيمةُ المرساةُ هي المنتِجُ بالبتات: فالجدولُ المبرهَن (`ghazali_table`) مربوطٌ بسطره من المختوم. -/
theorem anchored_is_productive :
    cells.all (fun r => r.stated == productive r.degree r.form) = true := by decide

/-- خاناتُ المنطق رأيٌ ثانٍ: مرساةٌ عند الغزاليّ، ولا مرساةَ لها في النبهانيّ. -/
theorem logic_is_second_opinion :
    cells.all (fun r => !r.ghazali.isEmpty && r.nabhani.isEmpty) = true := by decide

/-- منهجُ النبهانيّ في المنطق من العمود وحده. -/
theorem manhaj_from_spine :
    manhaj.length = 1 ∧ manhaj.all (fun r => r.ghazali.isEmpty && !r.nabhani.isEmpty) = true := by
  decide

/-- القراءتان الأصوليّتان موافقتان: مرساتان في المودَعَين معًا، وصورتاهما منتِجتان. -/
theorem usul_agreed_and_productive :
    usul.length = 2 ∧
      usul.all (fun r => !r.ghazali.isEmpty && !r.nabhani.isEmpty && productive r.degree r.form)
        = true := by
  decide

/-- مراسي الغزاليّ من مودَعاته الثلاثة، ومراسي النبهانيّ من ج3 و«التفكير» لا غير. -/
theorem sources_named :
    rows.all (fun r =>
      r.ghazali.all (fun a => a.1 == "المستصفى" || a.1 == "محك النظر" || a.1 == "معيار العلم") &&
      r.nabhani.all (fun a => a.1 == "ج3" || a.1 == "التفكير")) = true := by
  decide

end Slge.GhazaliAnchors
