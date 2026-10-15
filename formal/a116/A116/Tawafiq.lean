import A116.Alif
import A116.Count

/-!
# توافيقُ الخانات: عددُ المرخَّص من كلّ سلاسل الشبكة بطولٍ معلوم (ADR ٦٣)

السؤال: «كم تركيبًا من خانات الـ116 يُرخَّص؟» — جوابُه هنا **على الخانات بأعيانها** لا على أصناف
المقاطع (ذلك في `Exhaust.table_length` و`ExhaustPause.pauseTable_length`) ولا على الأوزان
(`PauseCount.pause_count_fib`).

* `seqs n`: كلُّ سلاسل الشبكة المرخَّصة (`Alif.licensable`، 113) بطول n؛ عددُها ‎113^n‎ (`seqs_length`).
* `wasl n` و`waqf n`: ما يقبله `Hadd.strictB` و`Hadd.strictPauseB` منها.
* الطولُ الأوّل: **84** = 28 حاملًا × 3 حركات (`wasl_one`، `one_is_cv`) — الألفُ ليست حاملَ ابتداء
  والساكنُ لا يُبتدأ به؛ فالنموذجُ الثنائيّ (`Count.U 1 = 87`) يزيد بالألف المتحرّكة الثلاث بالضبط
  (`binary_adds_vowelled_alif`).
* الطولُ الثاني: **9,492** = 84 × 84 (CV.CV) + 84 × 29 (CV ثمّ مُغلِقٌ أو مدّ) (`wasl_two`،
  `two_structure`)؛ والوقفُ كذلك (`waqf_two`)؛ لا ‎29 × 4 × 29 = 3,364‎ الذي يعدّ الألفَ حاملَ ابتداء
  والسكونَ حركة.
* **ثغرةٌ مسمّاة** `ALIF_CLOSER_NOT_REFUSED`: الألفُ الساكنة بعد ضمّةٍ أو كسرة صنفُها `c` في `Hadd.kindOne`
  (لأنّ مدَّها الفتحةُ وحدَها) فتُرخَّص مُغلِقًا — كُاْ (`alif_closer_licensed`)، و56 سلسلةً من الطول الثاني
  (`alif_closers_two`)، وكَاْاْ وقفًا (`kaa_aa_pause`) — والألفُ «لا بد لها من حرف قبلها مفتوح» (الكتاب
  س17941) ولا تكون مُغلِقًا أبدًا. الثغرةُ تزيد ولا تنقص: لا كلمةَ من المدوّنة تُرفض بها؛ وسدُّها تغييرٌ
  في `kindOne` يمسّ جداولَ Lean المودَعة كلَّها، فهو ADR بعد قفل الدالّ لا تعديلٌ صامت.

الطولُ الثالث وما بعده يطبعه Lean المترجَم جدولًا (`lake exe a116-table tawafiq`) ويطابقه
`tests/test_tawafiq.py` بمرآة البوّابة؛ وعددُه لكلّ طولٍ **غيرُ مبرهَن** بعدُ (`TAWAFIQ_CLOSED_FORM_NOT_PROVEN`):
النموذجُ الثنائيّ له شكلٌ مغلق لكلّ طول (`Count.U_succ_succ`)، والثلاثيُّ على الخانات ينتظر آلةَ انتقالٍ
بحالة (حركةُ ما قبل، حاملُ المُغلِق المنتظَر) على نسق `Fold`.
-/

namespace A116.Tawafiq

open A116 A116.Ladder A116.Hadd

/-- كلُّ سلاسل الشبكة المرخَّصة بطول n. -/
def seqs : Nat → List (List Cell)
  | 0 => [[]]
  | n + 1 => Alif.licensable.flatMap fun c => (seqs n).map (c :: ·)

theorem length_flatMap_cons {α : Type} (l : List α) (m : List (List α)) :
    (l.flatMap fun c => m.map (c :: ·)).length = l.length * m.length := by
  induction l with
  | nil => simp
  | cons c l ih =>
    simp only [List.flatMap_cons, List.length_append, List.length_map, ih, List.length_cons]
    rw [Nat.succ_mul, Nat.add_comm]

theorem seqs_length : ∀ n, (seqs n).length = 113 ^ n
  | 0 => rfl
  | n + 1 => by
    rw [seqs, length_flatMap_cons, seqs_length n, Alif.licensable_length, Nat.pow_succ, Nat.mul_comm]

/-- المرخَّصُ وصلًا من الطول n. -/
def wasl (n : Nat) : Nat := ((seqs n).filter strictB).length

/-- المرخَّصُ وقفًا من الطول n. -/
def waqf (n : Nat) : Nat := ((seqs n).filter strictPauseB).length

/-- ما آخرُه ألفٌ ساكنة صنفُها `c` (مُغلِق) وهو مرخَّصٌ وصلًا. -/
def alifClosers (n : Nat) : Nat :=
  ((seqs n).filter fun w =>
    strictB w && w.getLast? == some (atom 'ا' .sukun) && (kindOf w).getLast? == some .c).length

set_option maxRecDepth 100000

theorem wasl_one : wasl 1 = 84 := by decide +kernel

theorem waqf_one : waqf 1 = 84 := by decide +kernel

/-- الطولُ الأوّل كلُّه CV: 28 حاملًا (بلا ألف) × 3 حركات. -/
theorem one_is_cv : wasl 1 = (carrierCount - 1) * 3 := by rw [wasl_one]; rfl

/-- النموذجُ الثنائيّ على الـ116 يزيد على الثلاثيّ بالألف المتحرّكة الثلاث بالضبط. -/
theorem binary_adds_vowelled_alif : U 1 = wasl 1 + Alif.alifVowelled.length := by
  rw [U_one, wasl_one]; rfl

theorem wasl_two : wasl 2 = 9492 := by decide +kernel

theorem waqf_two : waqf 2 = 9492 := by decide +kernel

/-- الطولُ الثاني: CV ثمّ CV، أو CV ثمّ ساكنٌ (مُغلِقٌ أو مدّ) من الـ29. -/
theorem two_structure : wasl 2 = 84 * 84 + 84 * 29 := by rw [wasl_two]

/-- ‎29 × 4 × 29‎ ليس عددَ المرخَّص من الطول الثاني ولا من أيّ طول: إنّه أكبرُ من الأوّل وأصغرُ من الثاني. -/
theorem not_3364 : wasl 1 < 29 * 4 * 29 ∧ 29 * 4 * 29 < wasl 2 := by
  rw [wasl_one, wasl_two]; decide

/-- `ALIF_CLOSER_NOT_REFUSED`: كُاْ مرخَّصٌ وصلًا والألفُ فيه مُغلِق. -/
theorem alif_closer_licensed :
    strictB [atom 'ك' .damma, atom 'ا' .sukun] = true ∧
    kindOf [atom 'ك' .damma, atom 'ا' .sukun] = [.cv, .c] := by decide +kernel

/-- بعد الفتحة الألفُ مدٌّ لا مُغلِق. -/
theorem alif_after_fatha_is_madd : kindOf [atom 'ك' .fatha, atom 'ا' .sukun] = [.cv, .v] := by decide +kernel

/-- 56 سلسلةً من الطول الثاني ألفُها مُغلِق: 28 حاملًا × (ضمّة، كسرة). -/
theorem alif_closers_two : alifClosers 2 = 56 := by decide +kernel

/-- كَاْاْ: مدٌّ ثمّ ألفٌ مُغلِقةٌ عارضةً وقفًا — تُرخَّص بالثغرة نفسِها. -/
theorem kaa_aa_pause :
    strictPauseB [atom 'ك' .fatha, atom 'ا' .sukun, atom 'ا' .sukun] = true ∧
    strictB [atom 'ك' .fatha, atom 'ا' .sukun, atom 'ا' .sukun] = false := by decide +kernel

end A116.Tawafiq
