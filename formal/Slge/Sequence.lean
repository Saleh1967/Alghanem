import Slge.Bridge

/-!
# التسلسل: النصُّ تيارُ شهاداتٍ ذاتيُّ الحدّ، يُفكّ بلا لبس

الكلمةُ المرخَّصةُ بطول ‎k‎ لها عددٌ ‎n < U(k)‎ (`slgeFold`)، ويُسترجَع منه بعينها
(`slgeUnfold_slgeFold`). فالنصُّ تيارُ أزواجٍ ‎(k, n)‎، ولا فاصلَ بين الكلمات ولا حاملَ سابعَ
عشرَ بعد المئة: **الحدُّ في الترميز نفسِه**.

* طولُ الكلمة يُكتب أُحاديًّا: ‎k‎ آحادٍ ثمّ صفر (`lenBits`).
* عددُها يُكتب بعرضٍ ثابتٍ يُحسَب من ‎U(k)‎: ‎width k = log₂ U(k) + 1‎ خانةً (`natToBits`)؛
  و‎U(k) < 2^(width k)‎ (`U_lt_two_pow_width`) فكلُّ ‎n‎ يتّسع.
* التيار: ‎encode ws = ws.flatMap encodeWord‎.

## ما يُبرهَن

1. `bitsToNat_natToBits`: قراءةُ العدد بعرضه تعيده، لكلّ ‎n < 2^w‎.
2. `slgeUnfold_slgeFold`: فكُّ طيِّ المرخَّصة يعيدها بعينها.
3. `decodeWord_encodeWord`: قراءةُ كلمةٍ مرمَّزةٍ من رأس أيّ تيارٍ تعيدها **وما بعدها بعينه** —
   وهذا هو ذاتيّةُ الحدّ: الكلمةُ تعرف أين تنتهي.
4. `encodeWord_prefix_free`: لا ترميزُ كلمةٍ بادئةٌ لترميز كلمةٍ أخرى — فالتفكيكُ وحيد.
5. `decode_encode`: فكُّ تيارِ كلماتٍ مرخَّصةٍ يعيدها كلَّها بترتيبها.

والكلفةُ بالبتّ معلَنةٌ لا مخفيّة: ‎cost k = (k + 1) + width k‎ (`cost`)، تُطبع في الجدول.
-/

namespace Slge.Sequence

open A116 A116.Fold

/-! ## الفكّ يعيد الطيّ -/

theorem cellUnfold_cellFold {w : List Cell} (h : Admissible w) :
    cellUnfold w.length (cellFold w) = w := by
  unfold cellUnfold cellFold
  have hv := (admissible_iff_valid w).1 h
  have := unfold_fold (f := 87) (b := 29) (w.map code) false hv
  rw [List.length_map] at this
  rw [this, List.map_map]
  conv => lhs; arg 1; ext c; simp [Function.comp_def, decode_code]
  exact List.map_id w

/-- **الاسترجاع:** `slgeUnfold` بعد `slgeFold` هو الكلمةُ بعينها. -/
theorem slgeUnfold_slgeFold {w : List SCell} (h : licensed w = true) :
    slgeUnfold w.length (slgeFold w) = w := by
  unfold slgeUnfold slgeFold
  have hadm := (licensed_iff w).1 h
  have := cellUnfold_cellFold hadm
  rw [List.length_map] at this
  rw [this, List.map_map]
  conv => lhs; arg 1; ext c; simp [Function.comp_def]
  exact List.map_id w

/-! ## البتّات -/

/-- عددٌ بعرضٍ ثابت، الخانةُ الدنيا أوّلًا. -/
def natToBits : Nat → Nat → List Bool
  | 0, _ => []
  | w + 1, n => (n % 2 == 1) :: natToBits w (n / 2)

def bitsToNat : List Bool → Nat
  | [] => 0
  | b :: bs => (if b then 1 else 0) + 2 * bitsToNat bs

@[simp] theorem natToBits_length (w n : Nat) : (natToBits w n).length = w := by
  induction w generalizing n with
  | zero => rfl
  | succ w ih => simp [natToBits, ih]

theorem bitsToNat_natToBits : ∀ (w n : Nat), n < 2 ^ w → bitsToNat (natToBits w n) = n
  | 0, n, h => by simp [natToBits, bitsToNat]; omega
  | w + 1, n, h => by
    have hlt : n / 2 < 2 ^ w := by
      rw [Nat.pow_succ] at h; omega
    simp only [natToBits, bitsToNat, bitsToNat_natToBits w (n / 2) hlt]
    have := Nat.mod_two_eq_zero_or_one n
    rcases this with h0 | h1
    · simp [h0]; omega
    · simp [h1]; omega

/-! ## العرض والكلفة -/

/-- عرضُ عدد الكلمة بطول ‎k‎: ‎log₂ U(k) + 1‎. -/
def width (k : Nat) : Nat := (U k).log2 + 1

theorem U_lt_two_pow_width (k : Nat) : U k < 2 ^ width k := Nat.lt_log2_self

/-- كلفةُ كلمةٍ بطول ‎k‎ بالبتّ: الطولُ أُحاديًّا ثمّ العدد. -/
def cost (k : Nat) : Nat := (k + 1) + width k

/-! ## ترميزُ الكلمة والتيار -/

/-- الطولُ أُحاديًّا: ‎k‎ آحادٍ ثمّ صفر. -/
def lenBits (k : Nat) : List Bool := List.replicate k true ++ [false]

def encodeWord (w : List SCell) : List Bool :=
  lenBits w.length ++ natToBits (width w.length) (slgeFold w)

def encode (ws : List (List SCell)) : List Bool := ws.flatMap encodeWord

/-- قراءةُ الطول: عدُّ الآحاد حتى أوّل صفر. -/
def readLen : List Bool → Option (Nat × List Bool)
  | [] => none
  | false :: rest => some (0, rest)
  | true :: rest => (readLen rest).map fun (k, r) => (k + 1, r)

theorem readLen_lenBits (k : Nat) (rest : List Bool) :
    readLen (lenBits k ++ rest) = some (k, rest) := by
  induction k with
  | zero => rfl
  | succ k ih => simp [lenBits, List.replicate_succ, readLen] at ih ⊢; simp [ih]

/-- قراءةُ كلمةٍ من رأس التيار: الطول، ثمّ ‎width‎ خانةً، ثمّ الفكّ. -/
def decodeWord (bits : List Bool) : Option (List SCell × List Bool) :=
  match readLen bits with
  | none => none
  | some (k, rest) =>
    if _h : width k ≤ rest.length then
      some (slgeUnfold k (bitsToNat (rest.take (width k))), rest.drop (width k))
    else none

/-- **ذاتيّةُ الحدّ:** كلمةٌ مرخَّصةٌ مرمَّزةٌ في رأس أيّ تيارٍ تُقرأ بعينها ويبقى ما بعدها بعينه. -/
theorem decodeWord_encodeWord {w : List SCell} (h : licensed w = true) (rest : List Bool) :
    decodeWord (encodeWord w ++ rest) = some (w, rest) := by
  unfold decodeWord encodeWord
  rw [List.append_assoc, readLen_lenBits]
  simp only
  have hlen : (natToBits (width w.length) (slgeFold w) ++ rest).length ≥ width w.length := by
    simp
  simp only [hlen, dite_true]
  have hfold : slgeFold w < 2 ^ width w.length :=
    Nat.lt_trans (slgeFold_lt h) (U_lt_two_pow_width _)
  rw [List.take_append_of_le_length (by simp), List.take_of_length_le (by simp),
    bitsToNat_natToBits _ _ hfold, slgeUnfold_slgeFold h,
    List.drop_append_of_le_length (by simp), List.drop_of_length_le (by simp)]
  rfl

/-- **التفكيكُ وحيد:** إن تساوى ترميزا كلمتين مرخَّصتين مع ذيليهما فالكلمتان واحدةٌ والذيلان واحد. -/
theorem encodeWord_prefix_free {w w' : List SCell} (hw : licensed w = true)
    (hw' : licensed w' = true) {r r' : List Bool}
    (h : encodeWord w ++ r = encodeWord w' ++ r') : w = w' ∧ r = r' := by
  have h1 := decodeWord_encodeWord hw r
  have h2 := decodeWord_encodeWord hw' r'
  rw [h] at h1
  rw [h1] at h2
  simp at h2
  exact ⟨h2.1, h2.2⟩

/-- فكُّ التيار كلِّه، بوقودٍ هو عددُ الكلمات على الأكثر (كلُّ كلمةٍ تستهلك بتًّا على الأقلّ). -/
def decodeN : Nat → List Bool → List (List SCell)
  | 0, _ => []
  | _, [] => []
  | fuel + 1, bits =>
    match decodeWord bits with
    | none => []
    | some (w, rest) => w :: decodeN fuel rest

/-- **التيار يعود كلُّه:** فكُّ ترميزِ كلماتٍ مرخَّصةٍ يعيدها بترتيبها. -/
theorem decode_encode : ∀ (ws : List (List SCell)), (∀ w ∈ ws, licensed w = true) →
    decodeN ws.length (encode ws) = ws
  | [], _ => by simp [encode, decodeN]
  | w :: ws, hall => by
    have hw := hall w (by simp)
    have hrest : ∀ v ∈ ws, licensed v = true := fun v hv => hall v (by simp [hv])
    simp only [encode, List.flatMap_cons, List.length_cons]
    have hne : encodeWord w ++ ws.flatMap encodeWord ≠ [] := by
      simp [encodeWord, lenBits]
    cases hcons : encodeWord w ++ ws.flatMap encodeWord with
    | nil => exact absurd hcons hne
    | cons b bs =>
      rw [← hcons]
      simp only [decodeN]
      rw [decodeWord_encodeWord hw]
      simp only
      exact congrArg _ (decode_encode ws hrest)

end Slge.Sequence
