import Slge.Bridge

/-! معاني الحروف كما ذكرها مبحثُ «الحرف» في الشخصيّة الإسلاميّة ج3، بترتيب ذكرها: مولَّدٌ من
`tests/data/nabhani-huruf.json` (بصمةُ المودَع في `tools/deposit_maani.py`؛ بصمةُ المصدر `2d46a0438cc8cf31…`)؛ لا يُحرَّر باليد.
الفهرسُ الأوّل فهرسُ الحرف في `Huruf.table`. -/

namespace Slge.Maani

inductive Sense where
  | ibtidaGhayaZaman | ibtidaGhaya | intihaGhaya | tabid | bayanJins | zaida
  | maa | zarfiyya | ala | tajawwuz | ilsaq | istiana
  | musahaba | minAjl | fi | ikhtisas | taqlil | qasam
  | istila | mubaada | tashbih | mutlaqJam | tartibTaqib | tartibTarakhi
  | juzMinMatuf | tartib | taliqBiAhad | shakk | takhyir | ibaha
  | mukhalafa | nafyHal | nafyMustaqbal | nahy | dua | qalbMadi
  | takidMustaqbal
  deriving DecidableEq, Repr

/-- 29 حرفًا من `Huruf.table` ومعانيه بترتيب المصدر. -/
def table : List (Nat × List Sense) := [
  (0, [.ilsaq, .istiana, .musahaba, .ala, .minAjl, .fi, .zaida]),
  (1, [.ikhtisas, .zaida]),
  (2, [.tashbih]),
  (3, [.qasam]),
  (4, [.qasam]),
  (5, [.ibtidaGhaya, .tabid, .bayanJins, .zaida]),
  (6, [.intihaGhaya, .maa]),
  (7, [.mubaada]),
  (8, [.istila]),
  (9, [.zarfiyya, .ala, .tajawwuz]),
  (10, [.intihaGhaya, .maa]),
  (11, [.ibtidaGhayaZaman]),
  (12, [.ibtidaGhayaZaman]),
  (16, [.taqlil]),
  (40, [.qalbMadi]),
  (49, [.mutlaqJam]),
  (50, [.tartibTaqib]),
  (51, [.tartibTarakhi]),
  (52, [.tartib, .juzMinMatuf]),
  (53, [.taliqBiAhad, .shakk, .takhyir, .ibaha]),
  (54, [.taliqBiAhad]),
  (55, [.mukhalafa]),
  (56, [.mukhalafa]),
  (57, [.mukhalafa]),
  (60, [.nafyHal]),
  (61, [.nafyMustaqbal, .nahy, .dua]),
  (62, [.qalbMadi]),
  (63, [.takidMustaqbal]),
  (64, [.nafyHal])
]

theorem table_length : table.length = 29 := by rfl

end Slge.Maani
