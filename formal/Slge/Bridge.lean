import A116

/-!
# جسرُ SLGE إلى الـ116 — ترميزان، برهانٌ واحد

SLGE يكتب الخانةَ بترتيبه: الهمزةُ أوّلُ الحوامل (الموضع ٠)، والحالاتُ
«فتح، كسر، ضم، سكون». والـ116 في `A116/Cells.lean` يضع الهمزةَ آخرًا (الموضع ٢٨)،
والحالاتُ «فتحة، ضمّة، كسرة، سكون». فلا تنتقل مبرهنةٌ من هناك إلى هنا إلّا بجسرٍ
مبرهَن. وهذا الملفُّ هو ذلك الجسر.

## المسلّمة المُعلَنة

* **ج١:** الحروفُ الثمانيةُ والعشرون بعد الهمزة في SLGE هي بترتيبها نفسِه الحروفُ
  الثمانيةُ والعشرون الأولى في الـ116. والرقمُ هنا اسمٌ؛ ومطابقةُ الرقم بالحرف
  تفحصها `tests/test_conformance.py` في CI، لا هذا الملفّ.

## ما يُبرهَن هنا

1. `toCell` تقابلٌ بين خانات SLGE الـ116 وخانات الـ116 (`ofCell_toCell`،
   `toCell_ofCell`)، ويحفظ السكون (`toCell_isSukun`).
2. `licensed_iff`: ترخيصُ SLGE (لا يبدأ بساكن، ولا يتجاور ساكنان) هو **بعينه**
   `Admissible` في الـ116 بعد الجسر، لكلّ سلسلةٍ بأيّ طول.
3. `slgeFold_lt`، `slgeFold_injective`، `slgeFold_surjective`: طيُّ SLGE تقابلٌ
   بين المرخَّصات بطول n و‎{0, …, U(n) − 1}‎، فعددُها ‎U(n)‎ بالتقابل لا بالتعداد.
4. `count_eq_U`: عدّادُ SLGE (`count` بحلقته البايثونيّة نفسِها) يساوي ‎U(n)‎ لكلّ n.

فكلُّ مبرهنةٍ في الـ116 عن المقبولات مبرهنةٌ عن مرخَّصات SLGE.
-/

namespace Slge

open A116 A116.Fold

/-- حالاتُ SLGE بترتيبها: فتح ٠، كسر ١، ضم ٢، سكون ٣. -/
def stateToHaraka (s : Fin 4) : Haraka :=
  if s.val = 0 then .fatha else if s.val = 1 then .kasra else if s.val = 2 then .damma
  else .sukun

/-- وعكسُه. -/
def harakaToState : Haraka → Fin 4
  | .fatha => 0
  | .kasra => 1
  | .damma => 2
  | .sukun => 3

/-- الحاملُ: موضعُ الهمزة ٠ في SLGE هو ٢٨ في الـ116، والباقي يتأخّر واحدًا. -/
def carrierToA116 (c : Fin 29) : Fin 29 := ⟨(c.val + 28) % 29, Nat.mod_lt _ (by decide)⟩

def carrierOfA116 (c : Fin 29) : Fin 29 := ⟨(c.val + 1) % 29, Nat.mod_lt _ (by decide)⟩

/-- خانةُ SLGE: رقمُ الحامل بترتيب SLGE ورقمُ الحالة بترتيبه. -/
structure SCell where
  carrier : Fin 29
  state : Fin 4
  deriving DecidableEq, Repr

/-- أهي سكون؟ -/
def SCell.isSukun (c : SCell) : Bool := c.state.val == 3

/-- رمزُ SLGE الأصليّ: ‎4·حامل + حالة‎ (بفجوات؛ ليس طيًّا كثيفًا). -/
def SCell.index (c : SCell) : Nat := 4 * c.carrier.val + c.state.val

/-- الجسر. -/
def toCell (c : SCell) : Cell := ⟨carrierToA116 c.carrier, stateToHaraka c.state⟩

/-- ومعكوسُه. -/
def ofCell (c : Cell) : SCell := ⟨carrierOfA116 c.carrier, harakaToState c.haraka⟩

/-- خاناتُ SLGE مُعدَّدةً بترتيبها: الحاملُ أوّلًا ثمّ الحالة. -/
def scells : List SCell :=
  (List.finRange 29).flatMap fun l => (List.finRange 4).map fun s => ⟨l, s⟩

theorem mem_scells (c : SCell) : c ∈ scells := by
  cases c with
  | mk l s =>
    simp only [scells, List.mem_flatMap, List.mem_map]
    exact ⟨l, List.mem_finRange l, s, List.mem_finRange s, rfl⟩

theorem scells_length : scells.length = 116 := by decide

/-! ## الجسرُ تقابلٌ يحفظ السكون -/

theorem ofCell_toCell_on : ∀ c ∈ scells, ofCell (toCell c) = c := by decide +kernel

theorem toCell_ofCell_on : ∀ c ∈ cells, toCell (ofCell c) = c := by decide +kernel

theorem toCell_isSukun_on : ∀ c ∈ scells, (toCell c).isSukun = c.isSukun := by decide +kernel

@[simp] theorem ofCell_toCell (c : SCell) : ofCell (toCell c) = c :=
  ofCell_toCell_on c (mem_scells c)

@[simp] theorem toCell_ofCell (c : Cell) : toCell (ofCell c) = c :=
  toCell_ofCell_on c (mem_cells c)

@[simp] theorem toCell_isSukun (c : SCell) : (toCell c).isSukun = c.isSukun :=
  toCell_isSukun_on c (mem_scells c)

theorem toCell_injective {a b : SCell} (h : toCell a = toCell b) : a = b := by
  rw [← ofCell_toCell a, ← ofCell_toCell b, h]

theorem map_toCell_injective {w w' : List SCell} (h : w.map toCell = w'.map toCell) :
    w = w' := by
  have := congrArg (List.map ofCell) h
  simpa [List.map_map, Function.comp_def] using this

theorem map_toCell_ofCell (w : List Cell) : (w.map ofCell).map toCell = w := by
  simp [List.map_map, Function.comp_def]

/-! ## الترخيص -/

/-- لا يتجاور ساكنان (كما في `slge.cells.licensed`). -/
def noAdj : List SCell → Bool
  | a :: b :: t => !(a.isSukun && b.isSukun) && noAdj (b :: t)
  | _ => true

/-- الترخيص: لا يبدأ بساكن، ولا يتجاور ساكنان. والسلسلةُ الخاليةُ مرخَّصة (‎U(0) = 1‎). -/
def licensed : List SCell → Bool
  | [] => true
  | c :: t => !c.isSukun && noAdj (c :: t)

theorem noAdj_iff : ∀ w : List SCell, noAdj w = true ↔ NoAdjacentSukun (w.map toCell)
  | [] => by simp [noAdj, NoAdjacentSukun]
  | [_] => by simp [noAdj, NoAdjacentSukun]
  | a :: b :: t => by
    have ih := noAdj_iff (b :: t)
    simp only [List.map_cons] at ih
    simp only [noAdj, List.map_cons, NoAdjacentSukun, toCell_isSukun, Bool.and_eq_true,
      Bool.not_eq_true', ← ih]
    cases a.isSukun <;> cases b.isSukun <;> simp

/-- **الترخيصُ هو القبولُ في الـ116 بعينه**، لكلّ سلسلةٍ بأيّ طول. -/
theorem licensed_iff (w : List SCell) : licensed w = true ↔ Admissible (w.map toCell) := by
  cases w with
  | nil => simp [licensed, Admissible, HeadNotSukun, NoAdjacentSukun]
  | cons c t =>
    have h := noAdj_iff (c :: t)
    simp only [List.map_cons] at h
    simp only [licensed, List.map_cons, Admissible, HeadNotSukun, toCell_isSukun,
      Bool.and_eq_true, Bool.not_eq_true', h]

/-! ## الطيُّ والعدد -/

/-- طيُّ SLGE: طيُّ الـ116 بعد الجسر. -/
def slgeFold (w : List SCell) : Nat := cellFold (w.map toCell)

/-- فكُّه. -/
def slgeUnfold (n k : Nat) : List SCell := (cellUnfold n k).map ofCell

theorem slgeFold_lt {w : List SCell} (h : licensed w = true) : slgeFold w < U w.length := by
  have := cellFold_lt ((licensed_iff w).1 h)
  rwa [List.length_map] at this

/-- **متباين:** مرخَّصتان بطولٍ واحدٍ وطيٍّ واحدٍ هما واحدة. -/
theorem slgeFold_injective {w w' : List SCell} (hw : licensed w = true)
    (hw' : licensed w' = true) (hlen : w.length = w'.length) (h : slgeFold w = slgeFold w') :
    w = w' :=
  map_toCell_injective <|
    cellFold_injective ((licensed_iff w).1 hw) ((licensed_iff w').1 hw') (by simpa using hlen) h

/-- **شامل:** كلُّ عددٍ دون ‎U(n)‎ طيُّ مرخَّصةٍ بطول n، وهي `slgeUnfold n k`. -/
theorem slgeFold_surjective {n k : Nat} (hk : k < U n) :
    ∃ w : List SCell, w.length = n ∧ licensed w = true ∧ slgeFold w = k := by
  obtain ⟨w, hlen, hadm, hfold⟩ := cellFold_surjective hk
  refine ⟨w.map ofCell, by simpa using hlen, ?_, ?_⟩
  · rw [licensed_iff, map_toCell_ofCell]; exact hadm
  · rw [slgeFold, map_toCell_ofCell]; exact hfold

/-- عدّادُ SLGE بحلقته البايثونيّة: ‎(a, b) ← (b, 87b + 2523a)‎ بدءًا من ‎(1, 87)‎. -/
def countPair : Nat → Nat × Nat
  | 0 => (1, 87)
  | n + 1 => ((countPair n).2, 87 * (countPair n).2 + 2523 * (countPair n).1)

def count (n : Nat) : Nat := (countPair n).1

theorem countPair_eq (n : Nat) : countPair n = (U n, U (n + 1)) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [countPair, ih, Prod.mk.injEq, true_and]
    rw [U_succ_succ]

/-- **عدّادُ SLGE هو ‎U(n)‎ لكلّ n.** -/
theorem count_eq_U (n : Nat) : count n = U n := by
  simp [count, countPair_eq]

end Slge
