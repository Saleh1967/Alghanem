import A116.FractalTarkib

/-! مولَّدٌ بـ`tools/gen_fractal_tarkib.py` (ADR ٨٠)؛ لا يُحرَّر باليد. عدُّ الأزواج على المصحف قطعةً قطعة، كلُّ قطعةٍ تفحصها النواة، ثمّ تُوصل بالطيّ (`List.foldl_append`). -/

set_option maxRecDepth 200000

namespace A116.FractalTarkib

def accs : List (List Nat) := [
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [2460, 843, 2668, 1542, 20, 387, 2288, 1038, 680],
  [5055, 1639, 5490, 3265, 33, 781, 4537, 2313, 1403],
  [7235, 2451, 7640, 4765, 63, 1159, 6370, 3304, 1967],
  [9471, 3113, 9912, 6109, 77, 1494, 8318, 4263, 2549],
  [11209, 3691, 11634, 7141, 93, 1817, 9936, 4964, 2994],
  [12933, 4127, 12997, 8068, 119, 2154, 11135, 5736, 3345],
  [14443, 4541, 14442, 8928, 130, 2389, 12458, 6377, 3717],
  [15771, 4878, 15554, 9673, 141, 2610, 13521, 6930, 3987],
  [17577, 5538, 17404, 10823, 162, 2969, 15235, 7731, 4440],
  [18712, 5861, 18473, 11497, 177, 3124, 16304, 8199, 4764],
  [20410, 6425, 20008, 12403, 192, 3404, 17817, 8782, 5150],
  [21833, 6843, 21198, 13222, 195, 3585, 18926, 9335, 5446],
  [23182, 7199, 22294, 13910, 201, 3707, 20008, 9765, 5782],
  [24195, 7455, 23056, 14478, 212, 3880, 20789, 10226, 6038],
  [24695, 7620, 23326, 14732, 218, 3940, 21225, 10415, 6167],
  [25020, 7697, 23484, 14893, 221, 3989, 21460, 10571, 6271]]

theorem qitaa0 : ayat0.foldl cntPairs (accs.getD 0 []) = accs.getD 1 [] := by
  decide +kernel

theorem qitaa1 : ayat1.foldl cntPairs (accs.getD 1 []) = accs.getD 2 [] := by
  decide +kernel

theorem qitaa2 : ayat2.foldl cntPairs (accs.getD 2 []) = accs.getD 3 [] := by
  decide +kernel

theorem qitaa3 : ayat3.foldl cntPairs (accs.getD 3 []) = accs.getD 4 [] := by
  decide +kernel

theorem qitaa4 : ayat4.foldl cntPairs (accs.getD 4 []) = accs.getD 5 [] := by
  decide +kernel

theorem qitaa5 : ayat5.foldl cntPairs (accs.getD 5 []) = accs.getD 6 [] := by
  decide +kernel

theorem qitaa6 : ayat6.foldl cntPairs (accs.getD 6 []) = accs.getD 7 [] := by
  decide +kernel

theorem qitaa7 : ayat7.foldl cntPairs (accs.getD 7 []) = accs.getD 8 [] := by
  decide +kernel

theorem qitaa8 : ayat8.foldl cntPairs (accs.getD 8 []) = accs.getD 9 [] := by
  decide +kernel

theorem qitaa9 : ayat9.foldl cntPairs (accs.getD 9 []) = accs.getD 10 [] := by
  decide +kernel

theorem qitaa10 : ayat10.foldl cntPairs (accs.getD 10 []) = accs.getD 11 [] := by
  decide +kernel

theorem qitaa11 : ayat11.foldl cntPairs (accs.getD 11 []) = accs.getD 12 [] := by
  decide +kernel

theorem qitaa12 : ayat12.foldl cntPairs (accs.getD 12 []) = accs.getD 13 [] := by
  decide +kernel

theorem qitaa13 : ayat13.foldl cntPairs (accs.getD 13 []) = accs.getD 14 [] := by
  decide +kernel

theorem qitaa14 : ayat14.foldl cntPairs (accs.getD 14 []) = accs.getD 15 [] := by
  decide +kernel

theorem qitaa15 : ayat15.foldl cntPairs (accs.getD 15 []) = accs.getD 16 [] := by
  decide +kernel

/-- **الأنواعُ التسعة كلُّها واقعةٌ بأعدادها** برمز ‎3a + b‎ (0 اسم، 1 فعل، 2 حرف). -/
theorem azwaj_mushaf :
    ayat.foldl cntPairs [0, 0, 0, 0, 0, 0, 0, 0, 0] = [25020, 7697, 23484, 14893, 221, 3989, 21460, 10571, 6271] := by
  rw [show [0, 0, 0, 0, 0, 0, 0, 0, 0] = accs.getD 0 [] from rfl]
  simp only [ayat, List.foldl_append, qitaa0, qitaa1, qitaa2, qitaa3, qitaa4, qitaa5, qitaa6, qitaa7, qitaa8, qitaa9, qitaa10, qitaa11, qitaa12, qitaa13, qitaa14, qitaa15]
  rfl

end A116.FractalTarkib
