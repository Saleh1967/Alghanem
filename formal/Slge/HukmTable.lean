/-! الحكمُ على مودَع المصحف — مولَّدٌ بـ`tools/gen_hukm_index.py`؛ لا يُحرَّر باليد.
الأعدادُ صورًا: بلا جذرٍ (لا حكم)، وذاتُ الحكم ومنها ما فيه مفهومٌ بشاهد وما كلُّه معلومة؛
والمرجعُ المحجوب: حجمُه وما مُلئ منه (ولا رقمَ قبل الملء). -/

namespace Slge.HukmTable

def forms : Nat := 18179
def laHukm : Nat := 4725
def ahkam : Nat := 13454
def anyMafhum : Nat := 6160
def bothMalumah : Nat := 7294
def singleRoot : Nat := 11898
def multiRoot : Nat := 1556
def referenceSize : Nat := 300
def referenceFilled : Nat := 0

/-- القسمةُ تامّة: لا حكم + ذاتُ الحكم = الصور؛ وذاتُ الحكم مفهومٌ بشاهد أو معلومةٌ كلُّه؛
وبجذرٍ أو بجذور؛ والمملوءُ من المرجع لا يتجاوز حجمَه. -/
theorem partition :
    laHukm + ahkam = forms ∧ anyMafhum + bothMalumah = ahkam ∧
      singleRoot + multiRoot = ahkam ∧ referenceFilled ≤ referenceSize := by decide

end Slge.HukmTable
