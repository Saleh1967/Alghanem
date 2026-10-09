import Slge.Categories

/-! التغطية على مودَعَي المصحف — مولَّدٌ بـ`tools/gen_coverage_index.py`؛ لا يُحرَّر باليد.
`attestedCells` الخاناتُ التي تحملها صورةٌ من المودَعين بترتيب الشبكة؛ `axes` (المحور،
المودَع، المشهود): ١ الشبكة، ٢ الموزِّع، ٣ الأعلام، ٤ السوابق، ٥ جذورُ المقاييس (قاطعًا أو
محتملًا)، ٦ عقدُ المخصّص ذاتُ الجذور (قاطعًا). -/

namespace Slge.CoverageTable

open Slge.Categories (c)

def attestedCells : List SCell := [
  c 0 0, c 0 1, c 0 2, c 0 3, c 1 3, c 2 0,
  c 2 1, c 2 2, c 2 3, c 3 0, c 3 1, c 3 2,
  c 3 3, c 4 0, c 4 1, c 4 2, c 4 3, c 5 0,
  c 5 1, c 5 2, c 5 3, c 6 0, c 6 1, c 6 2,
  c 6 3, c 7 0, c 7 1, c 7 2, c 7 3, c 8 0,
  c 8 1, c 8 2, c 8 3, c 9 0, c 9 1, c 9 2,
  c 9 3, c 10 0, c 10 1, c 10 2, c 10 3, c 11 0,
  c 11 1, c 11 2, c 11 3, c 12 0, c 12 1, c 12 2,
  c 12 3, c 13 0, c 13 1, c 13 2, c 13 3, c 14 0,
  c 14 1, c 14 2, c 14 3, c 15 0, c 15 1, c 15 2,
  c 15 3, c 16 0, c 16 1, c 16 2, c 16 3, c 17 0,
  c 17 1, c 17 2, c 17 3, c 18 0, c 18 1, c 18 2,
  c 18 3, c 19 0, c 19 1, c 19 2, c 19 3, c 20 0,
  c 20 1, c 20 2, c 20 3, c 21 0, c 21 1, c 21 2,
  c 21 3, c 22 0, c 22 1, c 22 2, c 22 3, c 23 0,
  c 23 1, c 23 2, c 23 3, c 24 0, c 24 1, c 24 2,
  c 24 3, c 25 0, c 25 1, c 25 2, c 25 3, c 26 0,
  c 26 1, c 26 2, c 26 3, c 27 0, c 27 1, c 27 2,
  c 27 3, c 28 0, c 28 1, c 28 2, c 28 3
]

def axes : List (Nat × Nat × Nat) := [
  (1, 113, 113),
  (2, 246, 160),
  (3, 57, 57),
  (4, 11, 11),
  (5, 4561, 1895),
  (6, 1080, 972)
]

def rootsTotal : Nat := 4561
def rootsQati : Nat := 1619
def rootsMuhtamalOnly : Nat := 276
def rootsNone : Nat := 2666

def nodesTotal : Nat := 1600
def nodesQati : Nat := 972
def nodesMuhtamalOnly : Nat := 19
def nodesNone : Nat := 89
def nodesNoRoots : Nat := 520

theorem attestedCells_length : attestedCells.length = 113 := by decide

end Slge.CoverageTable
