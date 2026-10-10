import Slge.Nabhani

/-! وسمُ الأجناس بقسمة النبهانيّ «باعتبار المدلول وحده» (ج3 409) — مولَّدٌ
بـ`tools/deposit_madlul.py` من إطار المالك `tests/data/owner-ajnas-madlul.json`؛
لا يُحرَّر باليد. `signed = false` = لم يُوقَّع:
كلُّ الوسوم `none`. الصفُّ: (الكتاب، القسم أو `none` — لم يُوقَّع أو «ليس جنسًا»). -/

namespace Slge.MadlulTable

def signed : Bool := false

def tags : List (Nat × Option Nabhani.Madlul) := [
  (0, none),
  (1, none),
  (119, none),
  (163, none),
  (195, none),
  (239, none),
  (275, none),
  (413, none),
  (419, none),
  (546, none),
  (547, none),
  (584, none),
  (589, none),
  (617, none),
  (664, none),
  (722, none),
  (755, none),
  (979, none),
  (1410, none),
  (1419, none),
  (1442, none),
  (1476, none),
  (1544, none),
  (1550, none),
  (1551, none),
  (1552, none),
  (1553, none),
  (1554, none),
  (1555, none),
  (1556, none),
  (1557, none),
  (1558, none),
  (1559, none),
  (1560, none),
  (1561, none),
  (1562, none),
  (1563, none),
  (1564, none),
  (1565, none),
  (1566, none),
  (1567, none),
  (1568, none),
  (1569, none),
  (1570, none),
  (1571, none),
  (1572, none),
  (1573, none),
  (1574, none),
  (1575, none),
  (1576, none),
  (1577, none),
  (1578, none),
  (1579, none),
  (1580, none),
  (1581, none),
  (1582, none),
  (1583, none),
  (1584, none),
  (1585, none),
  (1586, none),
  (1587, none),
  (1588, none),
  (1589, none),
  (1590, none),
  (1591, none),
  (1592, none),
  (1593, none),
  (1594, none),
  (1595, none),
  (1596, none),
  (1597, none),
  (1598, none),
  (1599, none)
]

theorem tags_length : tags.length = 73 := by rfl

/-- لا وسمَ قبل التوقيع. -/
theorem unsigned_none : signed = false → tags.all (·.2.isNone) = true := by decide

end Slge.MadlulTable
