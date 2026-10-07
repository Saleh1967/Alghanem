import Slge.Bridge

/-! الجهةُ الوجوديّة لكلّ قالبٍ من بابه المودَع: مولَّدٌ من `slge.wazn.AWZAN` بـ`tools/deposit_wujud.py`؛
لا يُحرَّر باليد. الأصنافُ ستّة: فعل، مصدر، وصفٌ مشتقّ، اسمٌ مشتقٌّ غيرُ وصفٍ (زمانٌ ومكانٌ وآلة)، صيغةُ جمع،
اسمٌ (مصدرٌ أو جامد لا تفصله الخانة). -/

namespace Slge.Wujud

inductive Ont where
  | fil | masdar | wasf | zarfAla | jam | ism
  deriving DecidableEq, Repr

/-- 125 قالبًا بترتيب `Wazn.awzan`. -/
def table : List Ont := [
  .fil, .fil, .fil, .fil, .fil, .fil, .fil, .fil, .fil, .fil,
  .fil, .fil, .fil, .fil, .fil, .fil, .fil, .fil, .fil, .fil,
  .fil, .fil, .fil, .fil, .fil, .fil, .fil, .fil, .fil, .masdar,
  .masdar, .masdar, .masdar, .masdar, .masdar, .masdar, .masdar, .masdar, .masdar, .masdar,
  .masdar, .masdar, .masdar, .masdar, .masdar, .masdar, .masdar, .masdar, .wasf, .wasf,
  .wasf, .wasf, .wasf, .wasf, .wasf, .wasf, .zarfAla, .zarfAla, .zarfAla, .zarfAla,
  .zarfAla, .zarfAla, .zarfAla, .masdar, .masdar, .masdar, .wasf, .wasf, .wasf, .wasf,
  .wasf, .wasf, .wasf, .wasf, .wasf, .wasf, .wasf, .wasf, .wasf, .wasf,
  .wasf, .wasf, .wasf, .jam, .jam, .jam, .jam, .jam, .jam, .jam,
  .jam, .jam, .jam, .jam, .jam, .jam, .jam, .jam, .jam, .jam,
  .jam, .jam, .jam, .jam, .jam, .jam, .jam, .jam, .jam, .jam,
  .jam, .jam, .jam, .fil, .fil, .fil, .fil, .fil, .fil, .fil,
  .fil, .ism, .ism, .ism, .ism
]

theorem table_length : table.length = 125 := by rfl

end Slge.Wujud
