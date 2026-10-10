import Slge.Wasl
import Slge.Jidh
import Slge.SawabiqTable

/-!
# السوابقُ الحرفيّة: باءُ الجرّ ولامُ الجرّ ولامُ الأمر ولامُ كي وألُ التعريف وهمزةُ الوصل

قارئٌ لطبقة السابقة من حيث هي: الحرفُ الواحد في صدر الكلمة يُقرأ **بعلاقته المرخَّصة بما بعده** لا
بنفسه (الكتابُ لسيبويه، «باب عدة ما يكون عليه الكلم»: «لام الإضافة ومعناها الملك»، «باء الجر إنما هي
للإلزاق»؛ «باب ما يعمل في الأفعال فيجزمها»: «اللام التي في الأمر وذلك قولك ليفعل»؛ «باب الحروف التي
تضمر فيها أن»: «اللام التي في قولك جئتك لتفعل»؛ «باب ما يتقدم أول الحروف وهي زائدة»: ألفُ الوصل في
الأفعال وفي «الحرف الذي تعرف به الأسماء»، «مكسورة أبدا إلا أن يكون الحرف الثالث مضموما»، «إذا كان قبلها
كلام حذفت»؛ «باب كينونتها في الأسماء»: ابن واسم وامرؤ…، و«فعلوا بلام الأمر مع الفاء والواو مثل ذلك:
فلينظر وليضرب»). الجدولُ `SawabiqTable` مولَّدٌ من الكتاب المختوم بأسطره وشواهده.

القراءةُ `Reading`: السوابقُ، البابُ، ما بعد السابقة كما هو (`rest`)، وصورتُه **الأصل** (`under`) بعد ردّ ما
سقط في الوصل: همزةُ الوصل بحركتها (مضمومةٌ إن ضُمّ الثالث وإلّا مكسورة؛ وفي أل مفتوحة)، وكسرةُ لام الأمر
المسكَّنة بعد الواو والفاء. المبرهَن:
* كلُّ قراءةٍ تُردّ إلى الكلمة بعينها (`sawabiq_restores`).
* ما سقطت همزتُه لا يُرخَّص وحدَه (`joined_rest_unlicensed`: لا ابتداءَ بساكن)، وقراءتُه الموصولة هي قراءةُ
  أصله ابتداءً (`joined_is_initial`)؛ ولامُ الأمر المسكَّنة هي المكسورةُ بعينها (`sakin_is_kasra`).
* الحركةُ المردودة للهمزة دالّةٌ في الثالث (`wasl_state_damm_iff`).
* الأبوابُ الستّة في الجدول كلُّها بشاهدٍ من المصحف يقرؤه هذا القارئُ بعينه (`table_read`، `decide +kernel`).
-/

namespace Slge.Sawabiq

open Slge.Categories (c)

inductive Kind where
  | baJarr | lamJarr | lamAmr | lamKay | al | waslFil | waslIsm
  deriving DecidableEq, Repr

def Kind.idx : Kind → Nat
  | .baJarr => 0 | .lamJarr => 1 | .lamAmr => 2 | .lamKay => 3 | .al => 4 | .waslFil => 5
  | .waslIsm => 6

def Kind.ofIdx : Nat → Kind
  | 0 => .baJarr | 1 => .lamJarr | 2 => .lamAmr | 3 => .lamKay | 4 => .al | 5 => .waslFil
  | _ => .waslIsm

theorem idx_ofIdx : ∀ k : Kind, Kind.ofIdx k.idx = k := by intro k; cases k <;> rfl

def ba : SCell := c 2 1
def lamI : SCell := c 23 1
def wa : SCell := c 27 0
def fa : SCell := c 20 0
def hamzaA : SCell := c 0 0

/-- سوابقُ الجذع وتاءُ القسم (كما في `Alam.proclitics`). -/
def proclitics : List SCell := Jidh.proclitics.flatMap id ++ [c 3 0]

def lastState (r : List SCell) : Nat := ((r.getLast?.map (·.state.val)).getD 4)

/-- صدرُ المضارع: ياءٌ أو تاءٌ أو نونٌ أو همزةٌ مفتوحةٌ أو مضمومة، وثلاثُ خاناتٍ فأكثر. -/
def isMudari (r : List SCell) : Bool :=
  match r with
  | x :: _ :: _ :: _ => [28, 3, 25, 0].contains x.carrier.val && (x.state.val == 0 || x.state.val == 2)
  | _ => false

/-- حذفُ النون: آخرُه واوٌ بعد ضمّة أو ياءٌ بعد كسرة أو ألفٌ بعد فتحة. -/
def nunDropped (r : List SCell) : Bool :=
  match r.reverse with
  | y :: x :: _ => y.state.val == 3 &&
      ((y.carrier.val == 27 && x.state.val == 2) || (y.carrier.val == 28 && x.state.val == 1) ||
       (y.carrier.val == 1 && x.state.val == 0))
  | _ => false

/-- الكلمةُ، ثمّ ما بقي بعد قطع ضميرِ نصبٍ متّصل (يُظْهِرَهُ ← يُظْهِرَ). -/
def stems (r : List SCell) : List (List SCell) :=
  r :: Filiyya.objectSuffixes.filterMap (fun q => Jidh.peelSuffix q r)

def jazmShaped (r : List SCell) : Bool :=
  isMudari r && (stems r).any (fun s => !s.isEmpty && lastState s == 3)
def nasbShaped (r : List SCell) : Bool :=
  isMudari r && (stems r).any (fun s => !s.isEmpty && (lastState s == 0 || nunDropped s))
def isJarr (r : List SCell) : Bool :=
  Tawabi.caseClass r == .jarr || Tawabi.caseClass r == .nasbJarr

/-- آخرُه جرٌّ، أو مضافٌ إلى ضميرٍ متّصل وآخرُ مضافه جرّ (رَبِّهِمْ). -/
def jarrShaped (r : List SCell) : Bool :=
  isJarr r || Filiyya.objectSuffixes.any (fun q => match Jidh.peelSuffix q r with
    | some s => isJarr s | none => false)

/-- ما بعد السابقة مبدوءٌ بلامٍ ساكنة أو بشمسيٍّ ساكنٍ يليه مثلُه: أل موصولةً بلا همزة. -/
def alJoined (r : List SCell) : Bool :=
  match r with
  | l :: x :: _ => l.state.val == 3 &&
      (l.carrier.val == 23 || (Marifa.sun.contains l.carrier.val && l.carrier == x.carrier))
  | _ => false

/-- أهيكلُ ما بعد الهمزة هيكلُ اسمٍ موصول؟ حواملُه بادئةً: ابن ٢٬٢٥، اسم ١٢٬٢٤، امرؤ ٢٤٬١٠٬٠، اثنان ٤٬٢٥
(«است» تُركت لالتباسها باستفعل) — مرآةُ `WASL_NOUNS` في بوّابة الغانم (`gate/residue.py`). -/
def waslNoun (r : List SCell) : Bool :=
  match r.map (·.carrier.val) with
  | 2 :: 25 :: _ => true
  | 12 :: 24 :: _ => true
  | 24 :: 10 :: 0 :: _ => true
  | 4 :: 25 :: _ => true
  | _ => false

/-- حركةُ همزة الوصل المردودة: مضمومةٌ إن كان الثالثُ مضمومًا («مكسورة أبدا إلا أن يكون الحرف الثالث
مضموما فتضمها»، س17530) **في غير الأسماء الموصولة** — فهي «مكسورة في الابتداء وإن كان الثالث مضموما
نحو ابنم وامرؤ لأنها ليست ضمة تثبت في هذا البناء» (س17569–17573) — وإلّا مكسورة. `r` ما بعد الهمزة
(أوّلُه الساكن). -/
def waslState (r : List SCell) : Fin 4 :=
  if waslNoun r then 1 else
  match r with
  | _ :: y :: _ => if y.state.val == 2 then 2 else 1
  | _ => 1

theorem wasl_state_damm_iff (x y : SCell) (t : List SCell) :
    waslState (x :: y :: t) = 2 ↔ y.state.val = 2 ∧ waslNoun (x :: y :: t) = false := by
  simp only [waslState]
  split
  · rename_i h; simp [h]
  · rename_i h; simp only [Bool.not_eq_true] at h; split
    · rename_i h2; simp [h, beq_iff_eq.1 h2]
    · rename_i h2; simp only [beq_iff_eq] at h2; simp [h, h2]

/-- الاسمُ الموصول مكسورٌ أبدًا، ولو ضُمّ ثالثُه. -/
theorem wasl_noun_kasra (r : List SCell) (h : waslNoun r = true) : waslState r = 1 := by
  simp [waslState, h]

/-- شاهدان: اِبْنُ (ب ن ضمّ) كسرٌ، واُنْصُرْ (ن ص ضمّ) ضمّ. -/
theorem wasl_noun_witnesses :
    waslState [⟨⟨2, by decide⟩, ⟨3, by decide⟩⟩, ⟨⟨25, by decide⟩, ⟨2, by decide⟩⟩] = 1 ∧
    waslState [⟨⟨25, by decide⟩, ⟨3, by decide⟩⟩, ⟨⟨13, by decide⟩, ⟨2, by decide⟩⟩,
               ⟨⟨10, by decide⟩, ⟨3, by decide⟩⟩] = 2 := by decide

/-- ردُّ ما سقط في الوصل: همزةُ أل مفتوحة، وهمزةُ الوصل بحركتها. -/
def lift (r : List SCell) : List SCell :=
  (if alJoined r then hamzaA else ⟨⟨0, by decide⟩, waslState r⟩) :: r

theorem lift_head (r : List SCell) : ∃ v, (lift r).head? = some ⟨⟨0, by decide⟩, v⟩ := by
  unfold lift; split
  · exact ⟨0, rfl⟩
  · exact ⟨waslState r, rfl⟩

theorem lift_length (r : List SCell) : (lift r).length = r.length + 1 := by
  unfold lift; rfl

/-- همزةُ الوصل في الكلمة ابتداءً: السماعيُّ (العشرة) اسمٌ، وما قُرئ وصلًا من قالبه (بلاحقةٍ أو بدونها)
فعلٌ. -/
def waslKinds (w : List SCell) : List Kind :=
  if Wasl.tenNouns.any (fun p => p.2 == w || p.2 == Zuruf.setLast w 2 || p.2 == Zuruf.setLast w 0)
  then [.waslIsm]
  else if Wasl.kind w == .wasl ||
      Jidh.enclitics.any (fun q => match Jidh.peelSuffix q w with
        | some s => Wasl.kind s == .wasl || Wasl.kind (Zuruf.setLast s 3) == .wasl
        | none => false)
  then [.waslFil] else []  -- بلاحقةٍ: الجذعُ على آخره أو مسكَّنًا (أمرُ الجماعة اُسْجُدُوا)

/-- القراءةُ المباشرة (بلا ردّ): ابتداءً أل أو همزةُ الوصل؛ وبعد الباء الجرّ؛ وبعد اللام الجرُّ والأمرُ وكي. -/
def direct (p : Option SCell) (r : List SCell) : List Kind :=
  match p with
  | none => (if Marifa.hasAl r then [Kind.al] else []) ++ waslKinds r
  | some q =>
    (if q == ba && jarrShaped r then [Kind.baJarr] else []) ++
    (if q == lamI && jarrShaped r then [Kind.lamJarr] else []) ++
    (if q == lamI && jazmShaped r then [Kind.lamAmr] else []) ++
    (if q == lamI && nasbShaped r then [Kind.lamKay] else [])

/-- الموصولُ: بعد سابقةٍ وباقٍ مبدوءٍ بساكن، أصلُه `lift` يُقرأ ابتداءً؛ وهمزةُ أل لا تسقط بعد همزة
الاستفهام («إلا ما ذكرنا من الألف واللام في الاستفهام»). -/
def joinedKinds (p : Option SCell) (r : List SCell) : List Kind :=
  match r with
  | x :: _ => if p.isSome && x.state.val == 3 then
      (direct none (lift r)).filter (fun k => !(k == .al && p == some hamzaA)) else []
  | [] => []

/-- لامُ الأمر المسكَّنة بعد الواو والفاء («فلينظر وليضرب»): أصلُها المكسورة. -/
def sakinKinds (p : Option SCell) (r : List SCell) : List Kind :=
  match r with
  | x :: t => if (p == some wa || p == some fa) && x.carrier.val == 23 && x.state.val == 3 then
      (direct (some lamI) t).filter (· == .lamAmr) else []
  | [] => []

structure Reading where
  pre : List SCell
  kind : Kind
  rest : List SCell
  under : List SCell
  deriving DecidableEq, Repr

def restore (m : Reading) : List SCell := m.pre ++ m.rest

/-- قراءاتُ الكلمة بسابقةٍ بعينها (أو بلا سابقة): المباشرةُ، ثمّ الموصولةُ، ثمّ لامُ الأمر المسكَّنة. -/
def readAt (pre : List SCell) (r : List SCell) : List Reading :=
  (direct pre.getLast? r).map (fun k => ⟨pre, k, r, r⟩) ++
  (joinedKinds pre.getLast? r).map (fun k => ⟨pre, k, r, lift r⟩) ++
  (sakinKinds pre.getLast? r).map (fun k => ⟨pre, k, r, lamI :: r.tail⟩)

def pres : List (List SCell) :=
  [[]] ++ proclitics.map ([·]) ++ (proclitics.flatMap fun p => proclitics.map fun q => [p, q])

def sawabiq (w : List SCell) : List Reading :=
  (pres.filter (fun pre => pre.isPrefixOf w && pre.length < w.length)).flatMap fun pre =>
    readAt pre (w.drop pre.length)

theorem mem_readAt {pre r : List SCell} {m : Reading} :
    m ∈ readAt pre r ↔ m.pre = pre ∧ m.rest = r ∧
      ((m.kind ∈ direct pre.getLast? r ∧ m.under = r) ∨
       (m.kind ∈ joinedKinds pre.getLast? r ∧ m.under = lift r) ∨
       (m.kind ∈ sakinKinds pre.getLast? r ∧ m.under = lamI :: r.tail)) := by
  unfold readAt
  simp only [List.mem_append, List.mem_map]
  constructor
  · rintro ((⟨k, hk, rfl⟩ | ⟨k, hk, rfl⟩) | ⟨k, hk, rfl⟩)
    · exact ⟨rfl, rfl, Or.inl ⟨hk, rfl⟩⟩
    · exact ⟨rfl, rfl, Or.inr (Or.inl ⟨hk, rfl⟩)⟩
    · exact ⟨rfl, rfl, Or.inr (Or.inr ⟨hk, rfl⟩)⟩
  · rintro ⟨h1, h2, (⟨hk, hu⟩ | ⟨hk, hu⟩ | ⟨hk, hu⟩)⟩
    · left; left; exact ⟨m.kind, hk, by cases m; simp_all⟩
    · left; right; exact ⟨m.kind, hk, by cases m; simp_all⟩
    · right; exact ⟨m.kind, hk, by cases m; simp_all⟩

/-- كلُّ قراءةٍ تُردّ إلى الكلمة بعينها. -/
theorem sawabiq_restores {w : List SCell} {m : Reading} (h : m ∈ sawabiq w) : restore m = w := by
  unfold sawabiq at h
  obtain ⟨pre, hpre, hm⟩ := List.mem_flatMap.1 h
  have hp := (List.mem_filter.1 hpre).2
  simp only [Bool.and_eq_true, decide_eq_true_eq] at hp
  obtain ⟨h1, h2, _⟩ := mem_readAt.1 hm
  unfold restore; rw [h1, h2]
  exact List.prefix_iff_eq_append.1 (List.isPrefixOf_iff_prefix.1 hp.1)

theorem joinedKinds_sukun {p : Option SCell} {r : List SCell} {k : Kind}
    (h : k ∈ joinedKinds p r) : ∃ x t, r = x :: t ∧ x.state.val = 3 := by
  unfold joinedKinds at h
  split at h
  · rename_i x t
    split at h
    · rename_i hc; simp only [Bool.and_eq_true, beq_iff_eq] at hc; exact ⟨x, t, rfl, hc.2⟩
    · simp at h
  · simp at h

theorem sakinKinds_sukun {p : Option SCell} {r : List SCell} {k : Kind}
    (h : k ∈ sakinKinds p r) : ∃ x t, r = x :: t ∧ x.state.val = 3 := by
  unfold sakinKinds at h
  split at h
  · rename_i x t
    split at h
    · rename_i hc; simp only [Bool.and_eq_true, beq_iff_eq] at hc; exact ⟨x, t, rfl, hc.2⟩
    · simp at h
  · simp at h

/-- ما سقطت همزتُه (أو كسرةُ لامه) لا يُرخَّص وحدَه: يبدأ بساكن. -/
theorem joined_rest_unlicensed {pre r : List SCell} {m : Reading} (h : m ∈ readAt pre r)
    (hne : m.under ≠ m.rest) : licensed m.rest = false := by
  obtain ⟨_, h2, hc⟩ := mem_readAt.1 h
  have key : ∃ x t, r = x :: t ∧ x.state.val = 3 := by
    rcases hc with ⟨_, hu⟩ | ⟨hk, _⟩ | ⟨hk, _⟩
    · exact absurd (hu.trans h2.symm) hne
    · exact joinedKinds_sukun hk
    · exact sakinKinds_sukun hk
  obtain ⟨x, t, rfl, hx⟩ := key
  rw [h2]
  have : x = ⟨x.carrier, 3⟩ := by cases x; simp only [SCell.mk.injEq, true_and]; exact Fin.ext hx
  rw [this]; exact Wasl.no_initial_sukun _ _

/-- القراءةُ الموصولة قراءةُ الأصل ابتداءً: ما قُرئ بعد سابقةٍ بردّ همزته يُقرأ أصلُه بلا سابقة بالباب
نفسه. -/
theorem joined_is_initial {pre r : List SCell} {m : Reading} (h : m ∈ readAt pre r)
    (hu : m.under = lift r) : ⟨[], m.kind, lift r, lift r⟩ ∈ readAt [] (lift r) := by
  obtain ⟨_, _, hc⟩ := mem_readAt.1 h
  have key : m.kind ∈ direct none (lift r) := by
    rcases hc with ⟨_, hu'⟩ | ⟨hk, _⟩ | ⟨_, hu'⟩
    · have := congrArg List.length (hu'.symm.trans hu); rw [lift_length] at this; omega
    · unfold joinedKinds at hk
      split at hk
      · split at hk
        · exact (List.mem_filter.1 hk).1
        · simp at hk
      · simp at hk
    · obtain ⟨v, hv⟩ := lift_head r
      have := congrArg List.head? (hu'.symm.trans hu)
      rw [hv] at this; simp [lamI, c] at this
  exact mem_readAt.2 ⟨rfl, rfl, Or.inl ⟨key, rfl⟩⟩

/-- لامُ الأمر المسكَّنةُ بعد الواو والفاء هي المكسورةُ بعينها: فَلْيَنْظُرْ تُقرأ كما تُقرأ لِيَنْظُرْ. -/
theorem sakin_is_kasra {pre r : List SCell} {m : Reading} (h : m ∈ readAt pre r)
    (hu : m.under = lamI :: r.tail) (hne : m.under ≠ m.rest) :
    ⟨[lamI], .lamAmr, r.tail, r.tail⟩ ∈ readAt [lamI] r.tail := by
  obtain ⟨_, h2, hc⟩ := mem_readAt.1 h
  have key : Kind.lamAmr ∈ direct (some lamI) r.tail := by
    rcases hc with ⟨_, hu'⟩ | ⟨_, hu'⟩ | ⟨hk, _⟩
    · exact absurd (hu'.trans h2.symm) hne
    · obtain ⟨v, hv⟩ := lift_head r
      have := congrArg List.head? (hu'.symm.trans hu)
      rw [hv] at this; simp [lamI, c] at this
    · unfold sakinKinds at hk
      split at hk
      · split at hk
        · have := List.mem_filter.1 hk
          rw [beq_iff_eq.1 this.2] at this; exact this.1
        · simp at hk
      · simp at hk
  exact mem_readAt.2 ⟨rfl, rfl, Or.inl ⟨key, rfl⟩⟩

/-! ## الجدولُ المولَّد من الكتاب: كلُّ بابٍ بشاهدٍ من المصحف يقرؤه القارئ -/

/-- الصفُّ: (البابُ، سطرُ الكتاب، شاهدُ الكتاب حواملَ، صورةُ المصحف خاناتٍ، سوابقُها، أموصولة). -/
abbrev Row := Nat × Nat × List Nat × List SCell × List SCell × Bool

def rowKind (r : Row) : Kind := Kind.ofIdx r.1
def rowCells (r : Row) : List SCell := r.2.2.2.1
def rowPre (r : Row) : List SCell := r.2.2.2.2.1
def rowJoined (r : Row) : Bool := r.2.2.2.2.2

/-- الشاهدُ يُقرأ بالباب نفسه وبالسوابق نفسها، موصولًا إن كان الصفُّ موصولًا. -/
def reads (r : Row) : Bool :=
  (sawabiq (rowCells r)).any fun m =>
    m.kind == rowKind r && m.pre == rowPre r && ((m.under != m.rest) == rowJoined r)

set_option maxRecDepth 8192 in
theorem table_read : SawabiqTable.table.all reads = true := by decide +kernel

theorem table_kinds :
    (SawabiqTable.table.map (·.1)).eraseDups.length = 7 := by decide

/-! ## شواهد -/

def kataba : List SCell := [c 22 0, c 3 0, c 2 0]                              -- كَتَبَ
def liyawmin : List SCell := [c 23 1, c 28 0, c 27 3, c 24 1, c 25 3]          -- لِيَوْمٍ

set_option maxRecDepth 8192 in
/-- كَتَبَ لا سابقةَ فيها تُقرأ؛ لِيَوْمٍ تتعدّد قراءتُها: لامُ الجرّ ولامُ الأمر (يَوْمِنْ على صورة مجزوم) —
التعدّدُ يُحصى ولا يُحسم هنا. -/
theorem witness_none_and_multiple :
    sawabiq kataba = [] ∧
    (sawabiq liyawmin).map (·.kind) = [.lamJarr, .lamAmr] := by decide +kernel

end Slge.Sawabiq
