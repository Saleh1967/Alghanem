import Slge.Categories

/-! أبوابُ السوابق الحرفيّة عند سيبويه: لكلّ بابٍ سطرُه وشاهدُه حواملَ بالرسم، وصورةٌ من مودَع
المصحف يقرؤها `Sawabiq.sawabiq` بالباب نفسه — مولَّدٌ من المختوم
`tests/data/openiti-sibawayh-kitab.txt.gz`
(SHA-256 `a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625`) ومن `corpus-certificates.json.gz`
بـ`tools/deposit_sawabiq.py`؛ لا يُحرَّر باليد. الصفُّ: (رقمُ الباب في `Kind.idx`، سطرُ الباب،
شاهدُ الباب حواملَ، صورةُ المصحف خاناتٍ، سوابقُها، أموصولةٌ). -/

namespace Slge.SawabiqTable

open Slge.Categories (c)

def table : List (Nat × Nat × List Nat × List SCell × List SCell × Bool) := [
  (0, 18330, [2, 11, 28, 8], [c 2 1, c 10 0, c 2 3, c 2 1], [c 2 1], false),
  (1, 18330, [23, 22], [c 23 1, c 10 0, c 2 3, c 2 1], [c 23 1], false),
  (2, 8686, [23, 28, 20, 18, 23], [c 23 1, c 28 2, c 25 3, c 20 1, c 21 3], [c 23 1], false),
  (2, 17564, [20, 23, 28, 25, 17, 10], [c 20 0, c 23 3, c 28 0, c 25 3, c 17 2, c 10 3], [c 20 0], true),
  (3, 8658, [23, 3, 20, 18, 23], [c 23 1, c 28 0, c 6 3, c 22 2, c 24 0], [c 23 1], false),
  (4, 17502, [1, 23, 10, 5, 23], [c 0 0, c 23 3, c 6 0, c 24 3, c 8 2], [], false),
  (4, 17502, [2, 9, 23], [c 2 1, c 23 3, c 6 0, c 21 3, c 21 1], [c 2 1], true),
  (5, 17502, [1, 15, 10, 2], [c 0 2, c 12 3, c 22 2, c 25 3], [], false),
  (5, 17502, [1, 15, 10, 2], [c 27 0, c 12 3, c 3 0, c 19 3, c 20 1, c 10 3], [c 27 0], true),
  (6, 17564, [1, 2, 25], [c 0 1, c 2 3, c 25 0], [], false),
  (6, 17564, [1, 12, 24], [c 2 1, c 12 3, c 24 1], [c 2 1], true)
]

theorem table_length : table.length = 11 := by rfl

end Slge.SawabiqTable
