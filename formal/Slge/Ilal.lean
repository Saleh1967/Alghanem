import Slge.Categories
import Slge.Wazn
import Slge.Madd
import A116.Ilal

/-!
# الإعلالُ والإبدال: جبرٌ مغلقٌ صعودًا ونزولًا — هندسةٌ عكسيّةٌ لـ`A116.Ilal` على خانات SLGE

في الغانم القواعدُ الاثنتا عشرة **تعديلاتٌ موضعيّةٌ على الخانات** لها سجلٌّ يردّ الأصلَ (`edit_roundtrip`)،
وإغلاقُها على الترخيص مبرهَنٌ بأدواتٍ عامّة (قلبُ متحرّكٍ ساكنًا بين متحرّكين، نقلٌ، حذفُ ساكنٍ بعد متحرّك،
إبدالُ حامل، وساكنان لا ترخيص). هنا تُقلب الهندسة: القاعدةُ **صعودٌ** `up` من الأصل إلى الصورة في نافذةٍ من
الموضع `i`، و**نزولٌ** `down` من الصورة إلى الأصول التي يصعد كلٌّ منها إلى الصورة بعينها؛ والمبرهَن:

* `down_sound` / `undo_sound`: كلُّ أصلٍ ينزل إليه القارئُ يصعد إلى الصورة بعينها (النزولُ عكسُ الصعود).
* `down_complete` / `undo_complete`: كلُّ أصلٍ يصعد إلى الصورة ينزل إليه القارئ (لا أصلَ يفوت).
* الإغلاقُ على الترخيص عبر الجسر إلى أدوات `A116.Ilal` بعينها: `qalbAyn_closed`
  (`vowelled_to_sukun_between_vowelled`)، `naql_closed` (`swap_sukun_vowel`)، `hadhfWaw_closed`
  (`delete_sukun_after_vowelled`)، `ibdal_closed` (`admissible_replace_carrier`؛ هنا بـ`licensed_states`)،
  `hadhfAyn_forced` (`two_sukun_not_admissible`: الأصلُ غيرُ مرخَّصٍ فالحذفُ واجب)؛ و`qalbLam_closed`،
  `hadhfLam_closed` بخطوات النموذج نفسه (`step_vowelled`…).
* `descend_ascends`: كلُّ ما ينزل إليه القارئُ (حتى خطوتين) يصعد بسلسلته إلى الصورة بعينها؛
  `descend_complete`: ما صعد بخطوةٍ ينزل.

ما ليس هنا — باسمه: شروطُ الانطباق اللغويّة (أيُّ جذرٍ أجوف) معلَنةٌ لا مبرهَنة، كما في الغانم؛ والإدغامُ
الرسميُّ بعد `faTa` (اتَّصَلَ) بقيّةُ رسمٍ لا إعلال. والنافذةُ تبدأ بالخانة **قبل** موضع التعديل.
-/

namespace Slge.Ilal

open Slge.Categories (c)

/-- متحرّك؟ -/
def vow (x : SCell) : Bool := x.state.val != 3
/-- واوٌ أو ياء؟ -/
def wy (x : SCell) : Bool := x.carrier.val == 27 || x.carrier.val == 28
/-- حرفُ إطباق؟ (ص ض ط ظ) -/
def itbaq (x : SCell) : Bool := x.carrier.val == 14 || x.carrier.val == 15 || x.carrier.val == 16 || x.carrier.val == 17
/-- د ذ ز؟ -/
def dzz (x : SCell) : Bool := x.carrier.val == 8 || x.carrier.val == 9 || x.carrier.val == 11
/-- حرفُ مضارعة؟ (ء ن ت ي) -/
def mudari (x : SCell) : Bool := x.carrier.val == 0 || x.carrier.val == 25 || x.carrier.val == 3 || x.carrier.val == 28
/-- ألفٌ ساكنة. -/
def alif : SCell := c 1 3
/-- واوٌ ساكنة (واوُ الجماعة). -/
def gw : SCell := c 27 3

/-- القواعدُ الاثنتا عشرة (حذفُ العين بوجهيه: ضمُّ الفاء أو كسرُها). -/
inductive Rule where
  | qalbAyn | hadhfAynU | hadhfAynI | naql | qalbLam | hadhfLam | hadhfWaw
  | hamzaMadd | taTta | taDal | faTa | wawYa | yaWaw
  deriving DecidableEq, Repr

def Rule.all : List Rule :=
  [.qalbAyn, .hadhfAynU, .hadhfAynI, .naql, .qalbLam, .hadhfLam, .hadhfWaw,
   .hamzaMadd, .taTta, .taDal, .faTa, .wawYa, .yaWaw]

theorem Rule.mem_all (ρ : Rule) : ρ ∈ Rule.all := by cases ρ <;> decide

/-! ## الصعود: الأصلُ ← الصورة في نافذةٍ -/

/-- النافذةُ تبدأ بالخانة التي قبل موضع التعديل؛ `none` إن لم ينطبق الشرط. -/
def up : Rule → List SCell → Option (List SCell)
  | .qalbAyn, p :: y :: z :: r =>  -- قَوَلَ ← قَالَ (وقَوَلْتُ ← قَالْتُ، ثمّ الحذفُ ملزَم)
    if p.state.val == 0 && wy y && y.state.val == 0 then some (p :: alif :: z :: r) else none
  | .hadhfAynU, p :: y :: t :: r =>  -- قَالْتُ ← قُلْتُ
    if p.state.val == 0 && y == alif && !vow t then some (⟨p.carrier, 2⟩ :: t :: r) else none
  | .hadhfAynI, p :: y :: t :: r =>  -- بَاعْتُ ← بِعْتُ
    if p.state.val == 0 && y == alif && !vow t then some (⟨p.carrier, 1⟩ :: t :: r) else none
  | .naql, p :: x :: y :: z :: r =>  -- يَقْوُلُ ← يَقُولُ
    if vow p && !vow x && wy y && vow y && vow z then
      some (p :: ⟨x.carrier, y.state⟩ :: ⟨y.carrier, 3⟩ :: z :: r) else none
  | .qalbLam, [p, y] =>  -- دَعَوَ ← دَعَا
    if p.state.val == 0 && wy y && y.state.val == 0 then some [p, alif] else none
  | .hadhfLam, p :: y :: g :: r =>  -- دَعَوُوْ ← دَعَوْ: اللامُ مضمومةٌ قبل واو الجماعة
    if vow p && wy y && y.state.val == 2 && g == gw then some (p :: g :: r) else none
  | .hadhfWaw, p :: y :: z :: r =>  -- يَوْعِدُ ← يَعِدُ: بعد حرف المضارعة (ء ن ت ي)
    if mudari p && vow p && y == gw && vow z then some (p :: z :: r) else none
  | .hamzaMadd, p :: y :: r =>  -- ءَءْمَنَ ← ءَامَنَ
    if p == c 0 0 && y == c 0 3 then some (p :: alif :: r) else none
  | .taTta, p :: y :: r =>  -- اصْتَبَرَ ← اصْطَبَرَ
    if itbaq p && !vow p && y.carrier.val == 3 then some (p :: ⟨16, y.state⟩ :: r) else none
  | .taDal, p :: y :: r =>  -- ازْتَادَ ← ازْدَادَ
    if dzz p && !vow p && y.carrier.val == 3 then some (p :: ⟨8, y.state⟩ :: r) else none
  | .faTa, y :: t :: r =>  -- اوْتَصَلَ ← اتْتَصَلَ
    if wy y && !vow y && t.carrier.val == 3 then some (c 3 3 :: t :: r) else none
  | .wawYa, p :: y :: r =>  -- مِوْزَان ← مِيزَان
    if p.state.val == 1 && y == gw then some (p :: c 28 3 :: r) else none
  | .yaWaw, p :: y :: r =>  -- مُيْقِن ← مُوقِن
    if p.state.val == 2 && y == c 28 3 then some (p :: gw :: r) else none
  | _, _ => none

/-- تطبيقُ القاعدة في الموضع `i` من الكلمة. -/
def apply (ρ : Rule) (w : List SCell) (i : Nat) : Option (List SCell) :=
  (up ρ (w.drop i)).map (w.take i ++ ·)

/-! ## النزول: الصورةُ ← الأصولُ التي تصعد إليها بعينها -/

/-- الحرفان و/ي مضمومين (لامُ الناقص قبل واو الجماعة مضمومةٌ ثمّ تُحذف). -/
def wyDamma : List SCell := [c 27 2, c 28 2]

def down : Rule → List SCell → List (List SCell)
  | .qalbAyn, p :: y :: z :: r =>
    if p.state.val == 0 && y == alif then [p :: c 27 0 :: z :: r, p :: c 28 0 :: z :: r] else []
  | .hadhfAynU, f :: t :: r =>
    if f.state.val == 2 && !vow t then [⟨f.carrier, 0⟩ :: alif :: t :: r] else []
  | .hadhfAynI, f :: t :: r =>
    if f.state.val == 1 && !vow t then [⟨f.carrier, 0⟩ :: alif :: t :: r] else []
  | .naql, p :: x :: y :: z :: r =>
    if vow p && vow x && wy y && !vow y && vow z then [p :: ⟨x.carrier, 3⟩ :: ⟨y.carrier, x.state⟩ :: z :: r]
    else []
  | .qalbLam, [p, y] => if p.state.val == 0 && y == alif then [[p, c 27 0], [p, c 28 0]] else []
  | .hadhfLam, p :: g :: r => if vow p && g == gw then wyDamma.map fun y => p :: y :: g :: r else []
  | .hadhfWaw, p :: z :: r => if mudari p && vow p && vow z then [p :: gw :: z :: r] else []
  | .hamzaMadd, p :: y :: r => if p == c 0 0 && y == alif then [p :: c 0 3 :: r] else []
  | .taTta, p :: y :: r => if itbaq p && !vow p && y.carrier.val == 16 then [p :: ⟨3, y.state⟩ :: r] else []
  | .taDal, p :: y :: r => if dzz p && !vow p && y.carrier.val == 8 then [p :: ⟨3, y.state⟩ :: r] else []
  | .faTa, y :: t :: r => if y == c 3 3 && t.carrier.val == 3 then [c 27 3 :: t :: r, c 28 3 :: t :: r] else []
  | .wawYa, p :: y :: r => if p.state.val == 1 && y == c 28 3 then [p :: gw :: r] else []
  | .yaWaw, p :: y :: r => if p.state.val == 2 && y == gw then [p :: c 28 3 :: r] else []
  | _, _ => []

/-- الأصولُ في الموضع `i`. -/
def undo (ρ : Rule) (w : List SCell) (i : Nat) : List (List SCell) :=
  (down ρ (w.drop i)).map (w.take i ++ ·)

/-! ## النزولُ عكسُ الصعود بعينه، ولا أصلَ يفوت -/

theorem fin4_cases (s : Fin 4) : s.val = 0 ∨ s.val = 1 ∨ s.val = 2 ∨ s.val = 3 := by omega

theorem ext_val {x y : SCell} (h1 : x.carrier.val = y.carrier.val) (h2 : x.state.val = y.state.val) :
    x = y := by
  cases x; cases y; simp only [SCell.mk.injEq]; exact ⟨Fin.ext h1, Fin.ext h2⟩

/-- خانتان بقيمتَي حامليهما وحالتيهما. -/
macro "cellext" : tactic => `(tactic| (apply ext_val <;> (try simp_all) <;> (try decide)))

theorem wy_fatha (y : SCell) (h1 : y.carrier.val = 27 ∨ y.carrier.val = 28) (h2 : y.state.val = 0) :
    y = c 27 0 ∨ y = c 28 0 := by
  rcases h1 with h | h
  · left; cellext
  · right; cellext

theorem wy_sukun (y : SCell) (h1 : y.carrier.val = 27 ∨ y.carrier.val = 28) (h2 : y.state.val = 3) :
    y = c 27 3 ∨ y = c 28 3 := by
  rcases h1 with h | h
  · left; cellext
  · right; cellext

theorem wy_damma (y : SCell) (h1 : y.carrier.val = 27 ∨ y.carrier.val = 28) (h2 : y.state.val = 2) :
    y ∈ wyDamma := by
  simp only [wyDamma, List.mem_cons, List.not_mem_nil, or_false]
  rcases h1 with h | h
  · left; cellext
  · right; cellext

theorem scell_eq (x : SCell) (k s : Nat) (hk : k < 29) (hs : s < 4)
    (h1 : x.carrier.val = k) (h2 : x.state.val = s) : x = c k s hk hs := by
  cases x with
  | mk a b => simp only [c]; congr 1 <;> exact Fin.ext (by assumption)

/-- كلُّ أصلٍ ينزل إليه القارئُ يصعد إلى الصورة بعينها. -/
theorem down_sound (ρ : Rule) (v : List SCell) : ∀ u ∈ down ρ v, up ρ u = some v := by
  intro u hu
  cases ρ <;> rcases v with _ | ⟨p, _ | ⟨y, _ | ⟨z, _ | ⟨t, r⟩⟩⟩⟩ <;>
    simp only [down, List.not_mem_nil] at hu <;>
    (split at hu <;> simp only [List.mem_cons, or_false, wyDamma,
        List.map_cons, List.map_nil, List.mem_nil_iff] at hu) <;>
    rename_i hc <;> simp only [Bool.and_eq_true, beq_iff_eq, Bool.not_eq_true'] at hc <;>
    (rcases hu with rfl | rfl <;> simp_all [up, vow, wy, alif, gw, c, itbaq, dzz, mudari] <;>
      (first | decide | omega | cellext | (refine ⟨by decide, ?_⟩; cellext) | skip))

/-- كلُّ أصلٍ يصعد إلى الصورة ينزل إليه القارئ: لا أصلَ يفوت. -/
theorem down_complete (ρ : Rule) (u v : List SCell) (h : up ρ u = some v) : u ∈ down ρ v := by
  cases ρ <;> rcases u with _ | ⟨p, _ | ⟨y, _ | ⟨z, _ | ⟨t, r⟩⟩⟩⟩ <;>
    simp only [up, reduceCtorEq] at h <;>
    (split at h <;> simp only [Option.some.injEq, reduceCtorEq] at h) <;>
    rename_i hc <;>
    simp only [Bool.and_eq_true, beq_iff_eq, Bool.not_eq_true', wy, vow, itbaq, dzz, mudari,
      Bool.or_eq_true, bne_iff_ne, ne_eq] at hc <;>
    subst h <;> simp only [down] <;> split <;> rename_i hd <;>
    simp only [Bool.and_eq_true, beq_iff_eq, Bool.not_eq_true', wy, vow, itbaq, dzz, mudari,
      Bool.or_eq_true, bne_iff_ne, ne_eq, List.mem_cons, List.cons.injEq, true_and, and_true, List.not_mem_nil,
      or_false] at hd ⊢ <;>
    first
      | (simp_all (config := {decide := true}); done)
      | cellext
      | exact wy_fatha _ (by simp_all) (by simp_all)
      | exact wy_sukun _ (by simp_all) (by simp_all)
      | exact List.mem_map_of_mem (wy_damma _ (by simp_all) (by simp_all))
      | (constructor <;> first | cellext | (simp_all (config := {decide := true}); done))

theorem up_nil (ρ : Rule) : up ρ [] = none := by cases ρ <;> rfl
theorem down_nil (ρ : Rule) : down ρ [] = [] := by cases ρ <;> rfl

/-- الصورةُ خانتان فأكثر. -/
theorem up_length (ρ : Rule) (u v : List SCell) (h : up ρ u = some v) : 2 ≤ v.length := by
  cases ρ <;> rcases u with _ | ⟨p, _ | ⟨y, _ | ⟨z, _ | ⟨t, r⟩⟩⟩⟩ <;>
    simp only [up, reduceCtorEq] at h <;>
    (split at h <;> simp only [Option.some.injEq, reduceCtorEq] at h) <;> subst h <;> simp

theorem take_length_of_drop_ne_nil {w : List SCell} {i : Nat} (h : w.drop i ≠ []) :
    (w.take i).length = i := by
  have : i < w.length := by
    rcases Nat.lt_or_ge i w.length with hl | hl
    · exact hl
    · exact absurd (List.drop_eq_nil_of_le hl) h
  rw [List.length_take]; omega

/-- النزولُ عكسُ الصعود بعينه في الكلمة كلِّها. -/
theorem undo_sound (ρ : Rule) (w : List SCell) (i : Nat) :
    ∀ u ∈ undo ρ w i, apply ρ u i = some w := by
  intro u hu
  simp only [undo, List.mem_map] at hu
  obtain ⟨d, hd, rfl⟩ := hu
  have hne : w.drop i ≠ [] := by
    intro h; rw [h, down_nil] at hd; exact List.not_mem_nil hd
  have hlen := take_length_of_drop_ne_nil hne
  simp only [apply, List.drop_left' hlen, List.take_left' hlen, down_sound ρ _ d hd, Option.map_some,
    List.take_append_drop]

/-- لا أصلَ يفوت في الكلمة كلِّها. -/
theorem undo_complete (ρ : Rule) (u w : List SCell) (i : Nat) (h : apply ρ u i = some w) :
    u ∈ undo ρ w i := by
  simp only [apply, Option.map_eq_some_iff] at h
  obtain ⟨v, hv, rfl⟩ := h
  have hne : u.drop i ≠ [] := by
    intro h; rw [h, up_nil] at hv; exact absurd hv (by simp)
  have hlen := take_length_of_drop_ne_nil hne
  simp only [undo, List.drop_left' hlen, List.take_left' hlen, List.mem_map]
  exact ⟨u.drop i, down_complete ρ _ v hv, List.take_append_drop i u⟩

/-! ## الإغلاقُ على الترخيص — عبر الجسر إلى أدوات `A116.Ilal` بعينها -/

section Closure
open A116 A116.State A116.Junction A116.Ilal

theorem licensed_eq_of_adm {w w' : List SCell}
    (h : Admissible (w.map toCell) ↔ Admissible (w'.map toCell)) : licensed w = licensed w' :=
  Bool.eq_iff_iff.2 (by rw [licensed_iff, licensed_iff]; exact h)

theorem isSukun_of_vow {x : SCell} (h : vow x = true) : x.isSukun = false := by
  simpa [vow, SCell.isSukun] using h

theorem isSukun_of_not_vow {x : SCell} (h : vow x = false) : x.isSukun = true := by
  simpa [vow, SCell.isSukun] using h

theorem toCell_alif : toCell alif = ⟨carrierToA116 1, .sukun⟩ := rfl
theorem toCell_gw : toCell gw = ⟨carrierToA116 27, .sukun⟩ := rfl
theorem toCell_sukun (k : Fin 29) : toCell ⟨k, 3⟩ = ⟨carrierToA116 k, .sukun⟩ := rfl
theorem toCell_mk (x y : SCell) : toCell ⟨x.carrier, y.state⟩ = ⟨(toCell x).carrier, (toCell y).haraka⟩ := rfl

/-- 1. قلبُ العين ألفًا (قَوَلَ ← قَالَ) يحفظ الترخيص — `vowelled_to_sukun_between_vowelled` بعينها. -/
theorem qalbAyn_closed (l r : List SCell) (p y z : SCell) (hp : vow p = true) (hz : vow z = true) :
    licensed (l ++ [p, y, z] ++ r) = licensed (l ++ [p, alif, z] ++ r) := by
  apply licensed_eq_of_adm
  simp only [List.map_append, List.map_cons, List.map_nil, toCell_alif]
  exact vowelled_to_sukun_between_vowelled _ _ _ _ _ _ (by simp [isSukun_of_vow hp])
    (by simp [isSukun_of_vow hz])

/-- 4. قلبُ اللام ألفًا في الآخر (دَعَوَ ← دَعَا) يحفظ الترخيص: بعد متحرّكٍ لا يسقط آخرٌ أيًّا كان. -/
theorem run_two (q : State) (x y : Cell) (hx : x.isSukun = false) :
    run q [x, y] ≠ fellOut ↔ q ≠ fellOut := by
  cases q with
  | fellOut => simp [run, step]
  | awaiting => rw [run2, step_vowelled awaiting (by decide) x hx]; cases hy : y.isSukun <;> simp [step, hy]
  | afterSeed => rw [run2, step_vowelled afterSeed (by decide) x hx]; cases hy : y.isSukun <;> simp [step, hy]

theorem qalbLam_closed (l : List SCell) (p y : SCell) (hp : vow p = true) :
    licensed (l ++ [p, y]) = licensed (l ++ [p, alif]) := by
  apply licensed_eq_of_adm
  simp only [List.map_append, List.map_cons, List.map_nil]
  rw [← run_ne_fellOut_iff, ← run_ne_fellOut_iff, run_append, run_append,
    run_two _ _ _ (by simp [isSukun_of_vow hp]), run_two _ _ _ (by simp [isSukun_of_vow hp])]

/-- 3. النقلُ (يَقْوُلُ ← يَقُولُ) يحفظ الترخيص — `swap_sukun_vowel` بعينها، والساكنُ قبلها متحرّكٌ. -/
theorem naql_closed (l r : List SCell) (p x y z : SCell) (hp : vow p = true) (hx : vow x = false)
    (hy : vow y = true) (hz : vow z = true) :
    licensed (l ++ [p, x, y, z] ++ r) =
      licensed (l ++ [p, ⟨x.carrier, y.state⟩, ⟨y.carrier, 3⟩, z] ++ r) := by
  apply licensed_eq_of_adm
  simp only [List.map_append, List.map_cons, List.map_nil, toCell_mk, toCell_sukun]
  have e1 : l.map toCell ++ [toCell p, toCell x, toCell y, toCell z] ++ r.map toCell =
      (l.map toCell ++ [toCell p]) ++ [toCell x, toCell y, toCell z] ++ r.map toCell := by simp
  have e2 : l.map toCell ++ [toCell p, ⟨(toCell x).carrier, (toCell y).haraka⟩,
      ⟨carrierToA116 y.carrier, Haraka.sukun⟩, toCell z] ++ r.map toCell =
      (l.map toCell ++ [toCell p]) ++ [⟨(toCell x).carrier, (toCell y).haraka⟩,
      ⟨(toCell y).carrier, Haraka.sukun⟩, toCell z] ++ r.map toCell := by simp [toCell]
  rw [e1, e2]
  by_cases hq : run awaiting (l.map toCell) = fellOut
  · constructor <;> intro h <;> rw [← run_ne_fellOut_iff] at h <;>
      simp only [run_append, hq, run_fellOut, ne_eq, not_true_eq_false] at h
  · exact swap_sukun_vowel _ _ _ _ _
      (by rw [run_append]; exact step_vowelled _ hq _ (by simp [isSukun_of_vow hp]))
      (by simp [isSukun_of_not_vow hx]) (by simp [isSukun_of_vow hy]) (by simp [isSukun_of_vow hz])

/-- 6. حذفُ واو المثال (يَوْعِدُ ← يَعِدُ) يحفظ الترخيص — `delete_sukun_after_vowelled` بعينها. -/
theorem hadhfWaw_closed (l r : List SCell) (p z : SCell) (hp : vow p = true) (hz : vow z = true) :
    licensed (l ++ [p, gw, z] ++ r) = licensed (l ++ [p, z] ++ r) := by
  apply licensed_eq_of_adm
  simp only [List.map_append, List.map_cons, List.map_nil]
  exact delete_sukun_after_vowelled _ _ _ _ _ (by simp [isSukun_of_vow hp]) (by simp [isSukun_of_vow hz])

/-- 5. حذفُ لام الناقص المتحرّكة قبل واو الجماعة (دَعَوُوْ ← دَعَوْ) يحفظ الترخيص: متحرّكٌ بعد متحرّكٍ لا
يغيّر الحالة. -/
theorem run_vowelled_vowelled (q : State) (x y : Cell) (hx : x.isSukun = false) (hy : y.isSukun = false) :
    run q [x, y] = run q [x] := by
  cases q with
  | fellOut => simp [run, step]
  | awaiting => simp [run, step, hx, hy]
  | afterSeed => simp [run, step, hx, hy]

theorem hadhfLam_closed (l r : List SCell) (p y g : SCell) (hp : vow p = true) (hy : vow y = true) :
    licensed (l ++ [p, y, g] ++ r) = licensed (l ++ [p, g] ++ r) := by
  apply licensed_eq_of_adm
  simp only [List.map_append, List.map_cons, List.map_nil]
  rw [← run_ne_fellOut_iff, ← run_ne_fellOut_iff]
  have e1 : l.map toCell ++ [toCell p, toCell y, toCell g] ++ r.map toCell =
      l.map toCell ++ [toCell p, toCell y] ++ ([toCell g] ++ r.map toCell) := by simp
  have e2 : l.map toCell ++ [toCell p, toCell g] ++ r.map toCell =
      l.map toCell ++ [toCell p] ++ ([toCell g] ++ r.map toCell) := by simp
  rw [e1, e2]
  simp only [run_append]
  rw [run_vowelled_vowelled _ _ _ (by simp [isSukun_of_vow hp]) (by simp [isSukun_of_vow hy])]

/-- 7–12. الإبدالُ (حاملٌ بحامل، الحالةُ باقية) يحفظ الترخيص — `admissible_replace_carrier`؛ هنا لأنّ
الترخيصَ دالّةٌ في الحالات وحدَها (`licensed_states`). -/
theorem ibdal_closed (l r : List SCell) (x : SCell) (k : Fin 29) :
    licensed (l ++ [⟨k, x.state⟩] ++ r) = licensed (l ++ [x] ++ r) := by
  rw [Wazn.licensed_states, Wazn.licensed_states]; simp

/-- 2. **الإلزام**: أصلُ حذف العين (فاءٌ ثمّ ألفٌ ساكنةٌ ثمّ ساكن) غيرُ مرخَّصٍ أصلًا، فالحذفُ واجب —
`two_sukun_not_admissible` بعينها. -/
theorem hadhfAyn_forced (l r : List SCell) (p t : SCell) (ht : vow t = false) :
    licensed (l ++ [p, alif, t] ++ r) = false := by
  have h := two_sukun_not_admissible (l.map toCell ++ [toCell p]) (r.map toCell) (toCell alif) (toCell t)
    (by rfl) (by simp [isSukun_of_not_vow ht])
  have e : (l ++ [p, alif, t] ++ r).map toCell =
      l.map toCell ++ [toCell p] ++ [toCell alif, toCell t] ++ r.map toCell := by simp
  cases hl : licensed (l ++ [p, alif, t] ++ r)
  · rfl
  · exact absurd ((licensed_iff _).1 hl) (e ▸ h)

end Closure

/-! ## القارئ: النزولُ حتى خطوتين، وكلُّ ما ينزل إليه يصعد بسلسلته إلى الصورة بعينها -/

/-- سلسلةُ صعود: قواعدُ بمواضعها تُطبَّق بالترتيب من الأصل إلى الصورة. -/
abbrev Chain := List (Rule × Nat)

def ascend : Chain → List SCell → Option (List SCell)
  | [], u => some u
  | (ρ, i) :: ch, u => (apply ρ u i).bind (ascend ch)

/-- مواضعُ النافذة في جذعٍ طولُه `n`: حذفُ واو المثال في صدر الجذع وحدَه (بعد حرف المضارعة)، وحذفُ لام
الناقص في آخره وحدَه (قبل واو الجماعة اللاحقة)، وسائرُ القواعد في أيّ موضعٍ من الجذع — شرطٌ معلَن. -/
def positions : Rule → Nat → List Nat
  | .hadhfWaw, _ => [0]
  | .hadhfLam, n => [n - 1]
  | _, n => List.range n

/-- النزولُ خطوةً: كلُّ (قاعدة، موضع، أصل) يصعد إلى الكلمة. -/
def step1 (w : List SCell) (n : Nat) : List (Rule × Nat × List SCell) :=
  Rule.all.flatMap fun ρ => (positions ρ n).flatMap fun i => (undo ρ w i).map fun u => (ρ, i, u)

/-- النزولُ حتى خطوتين: (سلسلةُ الصعود، الأصل)؛ `n` طولُ الجذع في الكلمة. -/
def descend (w : List SCell) (n : Nat) : List (Chain × List SCell) :=
  (step1 w n).flatMap fun x =>
    ([(x.1, x.2.1)], x.2.2) :: (step1 x.2.2 n).map fun y => ([(y.1, y.2.1), (x.1, x.2.1)], y.2.2)

theorem step1_sound (w : List SCell) (n : Nat) : ∀ x ∈ step1 w n, apply x.1 x.2.2 x.2.1 = some w := by
  intro x hx
  simp only [step1, List.mem_flatMap, List.mem_map] at hx
  obtain ⟨ρ, _, i, _, u, hu, rfl⟩ := hx
  exact undo_sound ρ w i u hu

/-- كلُّ ما ينزل إليه القارئُ يصعد بسلسلته إلى الكلمة بعينها — لكلّ كلمة. -/
theorem descend_ascends (w : List SCell) (n : Nat) : ∀ x ∈ descend w n, ascend x.1 x.2 = some w := by
  intro x hx
  simp only [descend, List.mem_flatMap, List.mem_cons, List.mem_map] at hx
  obtain ⟨y, hy, rfl | ⟨z, hz, rfl⟩⟩ := hx
  · simp [ascend, step1_sound w n y hy]
  · simp [ascend, step1_sound _ n z hz, step1_sound w n y hy]

/-- ما صعد بخطوةٍ في موضعٍ من مواضعه ينزل: لكلّ قاعدةٍ وموضعٍ وأصل. -/
theorem step1_complete (ρ : Rule) (u w : List SCell) (i n : Nat) (hi : i ∈ positions ρ n)
    (h : apply ρ u i = some w) : (ρ, i, u) ∈ step1 w n := by
  simp only [step1, List.mem_flatMap, List.mem_map]
  exact ⟨ρ, Rule.mem_all ρ, i, hi, u, undo_complete ρ u w i h, rfl⟩

theorem descend_complete (ρ : Rule) (u w : List SCell) (i n : Nat) (hi : i ∈ positions ρ n)
    (h : apply ρ u i = some w) : ([(ρ, i)], u) ∈ descend w n := by
  simp only [descend, List.mem_flatMap, List.mem_cons]
  exact ⟨(ρ, i, u), step1_complete ρ u w i n hi h, Or.inl rfl⟩

/-! ## الردُّ بسجلّ الغانم بعينه (roundtrip)

في الغانم كلُّ قاعدةٍ تعديلٌ له سجلٌّ `EditRecord` (البداية، طولُ المدرَج، المحذوف) يردّه `restoreEdit` بعينه
(`edit_roundtrip`). هنا `record ρ u i` سجلُّ تطبيق القاعدة، و`apply_roundtrip`: ردُّ الصورة بالسجلّ هو الأصلُ بعينه —
لكلّ قاعدةٍ وأصلٍ وموضع، وهو مثولُ `edit_roundtrip` نفسِه؛ و`apply_roundtrip_a116`: الشيءُ نفسُه على خانات
الغانم عبر الجسر، فسجلُّ SLGE هو سجلُّ الغانم. -/

section Roundtrip
open A116.Recovery

/-- سجلُّ التعديل: البداية، طولُ المدرَج، المحذوفُ من الأصل. -/
def record (ρ : Rule) (u : List SCell) (i : Nat) : EditRecord SCell :=
  match ρ, u.drop i with
  | .qalbAyn, _ :: y :: _ => ⟨i + 1, 1, [y]⟩
  | .hadhfAynU, p :: y :: _ => ⟨i, 1, [p, y]⟩
  | .hadhfAynI, p :: y :: _ => ⟨i, 1, [p, y]⟩
  | .naql, _ :: x :: y :: _ => ⟨i + 1, 2, [x, y]⟩
  | .qalbLam, _ :: y :: _ => ⟨i + 1, 1, [y]⟩
  | .hadhfLam, _ :: y :: _ => ⟨i + 1, 0, [y]⟩
  | .hadhfWaw, _ :: y :: _ => ⟨i + 1, 0, [y]⟩
  | .faTa, y :: _ => ⟨i, 1, [y]⟩
  | _, _ :: y :: _ => ⟨i + 1, 1, [y]⟩
  | _, _ => ⟨i, 0, []⟩

theorem roundtrip_of (L ins R rem : List SCell) (s : Nat) (hs : L.length = s) :
    restoreEdit (L ++ ins ++ R) ⟨s, ins.length, rem⟩ = L ++ rem ++ R := by
  subst hs; rw [List.append_assoc]; exact edit_roundtrip L rem ins R

theorem roundtrip_cons (A pre ins R rem : List SCell) (s : Nat) (hs : (A ++ pre).length = s) :
    restoreEdit (A ++ (pre ++ (ins ++ R))) ⟨s, ins.length, rem⟩ = A ++ (pre ++ (rem ++ R)) := by
  have := roundtrip_of (A ++ pre) ins R rem s hs
  simpa only [List.append_assoc] using this

/-- الردُّ بالسجلّ هو الأصلُ بعينه — لكلّ قاعدةٍ وأصلٍ وموضع (مثولُ `edit_roundtrip`). -/
theorem apply_roundtrip (ρ : Rule) (u w : List SCell) (i : Nat) (h : apply ρ u i = some w) :
    restoreEdit w (record ρ u i) = u := by
  have hne : u.drop i ≠ [] := by
    intro hn; simp only [apply, hn, up_nil, Option.map_none] at h; exact absurd h (by simp)
  have hlen := take_length_of_drop_ne_nil hne
  have hu : u = u.take i ++ u.drop i := (List.take_append_drop i u).symm
  simp only [apply, Option.map_eq_some_iff] at h
  obtain ⟨v, hv, rfl⟩ := h
  generalize hd : u.drop i = d at hv hu hne
  conv => rhs; rw [hu]
  cases ρ <;> rcases d with _ | ⟨p, _ | ⟨y, _ | ⟨z, _ | ⟨t, r⟩⟩⟩⟩ <;>
    simp only [up, reduceCtorEq] at hv <;>
    (split at hv <;> simp only [Option.some.injEq, reduceCtorEq] at hv) <;> subst hv <;>
    simp only [record, hd] <;>
    first
      | exact roundtrip_cons (u.take i) [p] [alif] _ [y] (i + 1) (by simp [hlen])
      | exact roundtrip_cons (u.take i) [] [⟨p.carrier, 2⟩] _ [p, y] i (by simp [hlen])
      | exact roundtrip_cons (u.take i) [] [⟨p.carrier, 1⟩] _ [p, y] i (by simp [hlen])
      | exact roundtrip_cons (u.take i) [p] [⟨y.carrier, z.state⟩, ⟨z.carrier, 3⟩] _ [y, z] (i + 1)
          (by simp [hlen])
      | exact roundtrip_cons (u.take i) [p] [] _ [y] (i + 1) (by simp [hlen])
      | exact roundtrip_cons (u.take i) [] [c 3 3] _ [p] i (by simp [hlen])
      | exact roundtrip_cons (u.take i) [p] [⟨16, y.state⟩] _ [y] (i + 1) (by simp [hlen])
      | exact roundtrip_cons (u.take i) [p] [⟨8, y.state⟩] _ [y] (i + 1) (by simp [hlen])
      | exact roundtrip_cons (u.take i) [p] [c 28 3] _ [y] (i + 1) (by simp [hlen])
      | exact roundtrip_cons (u.take i) [p] [gw] _ [y] (i + 1) (by simp [hlen])

theorem restoreEdit_map (out : List SCell) (r : EditRecord SCell) :
    restoreEdit (out.map toCell) ⟨r.start, r.insertedLength, r.removed.map toCell⟩ =
      (restoreEdit out r).map toCell := by
  simp [restoreEdit, List.map_append, List.map_take, List.map_drop]

/-- الردُّ على خانات الغانم بسجلّ SLGE بعينه: سجلُّ SLGE هو سجلُّ الغانم عبر الجسر. -/
theorem apply_roundtrip_a116 (ρ : Rule) (u w : List SCell) (i : Nat) (h : apply ρ u i = some w) :
    restoreEdit (w.map toCell)
      ⟨(record ρ u i).start, (record ρ u i).insertedLength, (record ρ u i).removed.map toCell⟩ =
      u.map toCell := by
  rw [restoreEdit_map, apply_roundtrip ρ u w i h]

end Roundtrip

/-! ## الإبدالُ والترخيصُ المتدرّج: إبدالُ حاملٍ غيرِ حرف مدٍّ بمثله لا يغيّر الأصنافَ الثلاثة -/

section Ternary

theorem kindsAux_state (y y' : SCell) (h : y.state = y'.state) (r : List SCell) :
    Madd.kindsAux (some y) r = Madd.kindsAux (some y') r := by
  cases r with
  | nil => rfl
  | cons z t => simp only [Madd.kindsAux, Madd.kindOf, Madd.isMaddAfter, h]; rfl

/-- ليس حرفَ مدّ (ا و ي). -/
def notMadd (k : Fin 29) : Prop := k.val ≠ 1 ∧ k.val ≠ 27 ∧ k.val ≠ 28

theorem kindOf_carrier (p : Option SCell) (x : SCell) (k : Fin 29) (hk : notMadd k)
    (hx : notMadd x.carrier) : Madd.kindOf p ⟨k, x.state⟩ = Madd.kindOf p x := by
  unfold Madd.kindOf
  cases p with
  | none => rfl
  | some q =>
    simp only [Madd.isMaddAfter]
    have h1 : (k.val == 1) = false := by simp [hk.1]
    have h2 : (k.val == 27) = false := by simp [hk.2.1]
    have h3 : (k.val == 28) = false := by simp [hk.2.2]
    have h4 : (x.carrier.val == 1) = false := by simp [hx.1]
    have h5 : (x.carrier.val == 27) = false := by simp [hx.2.1]
    have h6 : (x.carrier.val == 28) = false := by simp [hx.2.2]
    simp only [h1, h2, h3, h4, h5, h6, Bool.false_and, Bool.or_self]

theorem ibdal_kinds (l r : List SCell) (x : SCell) (k : Fin 29) (hk : notMadd k) (hx : notMadd x.carrier) :
    ∀ p, Madd.kindsAux p (l ++ [⟨k, x.state⟩] ++ r) = Madd.kindsAux p (l ++ [x] ++ r) := by
  induction l with
  | nil =>
    intro p
    simp only [List.nil_append, List.cons_append, List.nil_append, Madd.kindsAux]
    rw [kindOf_carrier p x k hk hx, kindsAux_state ⟨k, x.state⟩ x rfl r]
  | cons a l ih =>
    intro p
    simp only [List.cons_append, Madd.kindsAux]
    rw [ih (some a)]

/-- تاءُ الافتعال طاءً أو دالًا وفاؤُه تاءً: الترخيصُ الثلاثيُّ (وصلًا ووقفًا) لا يتغيّر، كما لا يتغيّر الثنائيّ. -/
theorem ibdal_ternary (l r : List SCell) (x : SCell) (k : Fin 29) (hk : notMadd k) (hx : notMadd x.carrier) :
    Madd.continueLicensed (l ++ [⟨k, x.state⟩] ++ r) = Madd.continueLicensed (l ++ [x] ++ r) ∧
    Madd.pauseLicensed (l ++ [⟨k, x.state⟩] ++ r) = Madd.pauseLicensed (l ++ [x] ++ r) := by
  unfold Madd.continueLicensed Madd.pauseLicensed Madd.kinds
  rw [ibdal_kinds l r x k hk hx none]
  exact ⟨rfl, rfl⟩

end Ternary

/-! ## الشواهد بالحساب (خانات SLGE: ء٠ ا١ … ق٢١ ل٢٣ م٢٤ ن٢٥ و٢٧ ي٢٨) -/

def qala : List SCell := [c 21 0, c 1 3, c 23 0]                       -- قَالَ
def qawala : List SCell := [c 21 0, c 27 0, c 23 0]                    -- قَوَلَ
def qul : List SCell := [c 21 2, c 23 3]                                -- قُلْ
def qawal : List SCell := [c 21 0, c 27 0, c 23 3]                     -- قَوَلْ
def yaqulu : List SCell := [c 28 0, c 21 2, c 27 3, c 23 2]            -- يَقُولُ
def yaqwulu : List SCell := [c 28 0, c 21 3, c 27 2, c 23 2]           -- يَقْوُلُ
def daa : List SCell := [c 8 0, c 18 0, c 1 3]                          -- دَعَا
def daawa : List SCell := [c 8 0, c 18 0, c 27 0]                       -- دَعَوَ
def yaidu : List SCell := [c 28 0, c 18 1, c 8 2]                       -- يَعِدُ
def yawidu : List SCell := [c 28 0, c 27 3, c 18 1, c 8 2]              -- يَوْعِدُ
def amana : List SCell := [c 0 0, c 1 3, c 24 0, c 25 0]                -- ءَامَنَ
def aamana : List SCell := [c 0 0, c 0 3, c 24 0, c 25 0]               -- ءَءْمَنَ
def mizan : List SCell := [c 24 1, c 28 3, c 11 0, c 1 3, c 25 2]       -- مِيزَان
def miwzan : List SCell := [c 24 1, c 27 3, c 11 0, c 1 3, c 25 2]      -- مِوْزَان
def istabara : List SCell := [c 0 1, c 14 3, c 16 0, c 2 0, c 10 0]     -- إِصْطَبَرَ
def istabara0 : List SCell := [c 0 1, c 14 3, c 3 0, c 2 0, c 10 0]     -- إِصْتَبَرَ

/-- الصعودُ بعينه على الشواهد (قُلْ بخطوتين: قلبٌ ثمّ حذفٌ ملزَم). -/
theorem up_witnesses :
    apply .qalbAyn qawala 0 = some qala ∧ ascend [(.qalbAyn, 0), (.hadhfAynU, 0)] qawal = some qul ∧
    apply .naql yaqwulu 0 = some yaqulu ∧ apply .qalbLam daawa 1 = some daa ∧
    apply .hadhfWaw yawidu 0 = some yaidu ∧ apply .hamzaMadd aamana 0 = some amana ∧
    apply .wawYa miwzan 0 = some mizan ∧ apply .taTta istabara0 1 = some istabara := by decide

/-- النزولُ يجد الأصولَ بسلاسلها. -/
theorem down_qala : ([(.qalbAyn, 0)], qawala) ∈ descend qala 3 := by decide
theorem down_qul : ([(.qalbAyn, 0), (.hadhfAynU, 0)], qawal) ∈ descend qul 2 := by decide
theorem down_yaqulu : ([(.naql, 0)], yaqwulu) ∈ descend yaqulu 4 := by decide
theorem down_daa : ([(.qalbLam, 1)], daawa) ∈ descend daa 3 := by decide
theorem down_yaidu : ([(.hadhfWaw, 0)], yawidu) ∈ descend yaidu 3 := by decide
theorem down_amana : ([(.hamzaMadd, 0)], aamana) ∈ descend amana 4 := by decide
theorem down_mizan : ([(.wawYa, 0)], miwzan) ∈ descend mizan 5 := by decide
theorem down_istabara : ([(.taTta, 1)], istabara0) ∈ descend istabara 5 := by decide

/-- الإغلاقُ والإلزامُ على الشواهد: قَوَلَ وقَالَ مرخَّصان، وقَالْ (أصلُ قُلْ) غيرُ مرخَّص وقُلْ مرخَّص. -/
theorem closure_witnesses :
    licensed qawala = true ∧ licensed qala = true ∧ licensed [c 21 0, c 1 3, c 23 3] = false ∧
    licensed qul = true ∧ licensed yaqwulu = true ∧ licensed yaqulu = true := by decide


/-- الردُّ بالسجلّ على الشواهد (بعينها بالحساب). -/
theorem roundtrip_witnesses :
    A116.Recovery.restoreEdit qala (record .qalbAyn qawala 0) = qawala ∧
    A116.Recovery.restoreEdit yaqulu (record .naql yaqwulu 0) = yaqwulu ∧
    A116.Recovery.restoreEdit yaidu (record .hadhfWaw yawidu 0) = yawidu ∧
    A116.Recovery.restoreEdit istabara (record .taTta istabara0 1) = istabara0 := by decide

end Slge.Ilal
