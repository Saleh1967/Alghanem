import Slge.Jidh
import Slge.MaqayisTable

/-!
# القرينةُ المعجميّة: عضويّةُ الجذر في مقاييس اللغة دالّةٌ على الخانات، والترتيبُ لا يُسقط قراءة

الجذعُ يعيد قراءاتٍ متعدّدة (قَالَ: قول/قيل؛ كَذَّبُوا: فَعَّلَ+وا أو كَ+الذَّبُو) والتعدّدُ يُقرأ كما هو؛ والقرينةُ
التي تفصله **عضويّةُ الجذر** في جدولٍ مختوم (مقاييسُ اللغة لابن فارس، 4,561 جذرًا ثلاثيًّا حواملَ، `MaqayisTable`).
المبرهَن:

* `member_sound`: العضويّةُ دالّةٌ على الخانات: `member r = true ↔ ∃ n ∈ table, matchesRoot n r` — لا بحثَ خارج الجدول.
* `matchesL_weak`: العينُ أو اللامُ المعتلّةُ في الطبعة (ا/ى) تطابق الواوَ أو الياءَ لا غير — شرطُ الطبعة معلَنٌ وأثرُه مبرهَن.
* `mem_rank`، `length_rank`: الترتيبُ بالقرينة (المشهودُ أوّلًا) لا يُسقط قراءةً ولا يزيدها — لكلّ قائمة قراءات.
* `attested_of_member`: قراءةٌ أصلُها على قالبٍ سليم بجذرٍ مشهودٍ قراءةٌ مشهودة.

ما ليس هنا: الدلالةُ (محاورُ المعاني في المقاييس لم تُودَع)؛ وأيُّ جذرٍ مشهودٍ فعلًا في هذه الكلمة — الجدولُ يفصل ما
لم يُشهَد ولا يختار بين مشهودَين (قول/قيل كلاهما في المقاييس).
-/

namespace Slge.Maqayis

open Slge.Categories (c)

/-- عينٌ أو لامٌ معتلّة في الطبعة (ا/ى): واوٌ أو ياء. -/
def WEAK : Nat := 29

/-- رمزُ الجدول ← حوامله الثلاثة (29 = معتلّة). -/
def decode (n : Nat) : Nat × Nat × Nat := (n / 900, n / 30 % 30, n % 30)

/-- حاملُ الجدول يطابق حاملَ الجذر: بعينه، أو معتلّةٌ تطابق و/ي. -/
def matchesL (t k : Nat) : Bool := if t = WEAK then (k == 27 || k == 28) else t == k

def matchesRoot (n : Nat) (r : Wazn.Root) : Bool :=
  let (a, b, d) := decode n
  matchesL a (r 0).val && matchesL b (r 1).val && matchesL d (r 2).val

/-- العضويّةُ: جذرٌ من الخانات في جدول المقاييس. -/
def member (r : Wazn.Root) : Bool := table.any (matchesRoot · r)

/-- العضويّةُ دالّةٌ على الخانات: شاهدُها رمزٌ في الجدول يطابق الجذر. -/
theorem member_sound (r : Wazn.Root) : member r = true ↔ ∃ n ∈ table, matchesRoot n r = true :=
  List.any_eq_true

/-- المعتلّةُ تطابق الواوَ أو الياءَ لا غير. -/
theorem matchesL_weak (k : Nat) : matchesL WEAK k = true ↔ k = 27 ∨ k = 28 := by
  simp [matchesL]

/-- غيرُ المعتلّة تطابق حاملَها بعينه. -/
theorem matchesL_exact (t k : Nat) (h : t ≠ WEAK) : matchesL t k = true ↔ t = k := by
  simp [matchesL, h]

/-! ## القراءةُ وجذورها -/

def rootOfTemplate (k : Nat) (u : List SCell) : Option Wazn.Root :=
  match Wazn.rootOf (Sarf.templ k) u 0, Wazn.rootOf (Sarf.templ k) u 1, Wazn.rootOf (Sarf.templ k) u 2 with
  | some a, some b, some d => some (fun i => if i = 0 then a else if i = 1 then b else d)
  | _, _, _ => none

/-- جذورُ القراءة: جذرُ **صورة** أصلها (`Jidh.stemForm`: بلا تنوينٍ أو بصدر المضارع، كما قُرئت) على كلّ
قالبٍ من قوالبها — فالتنوينُ خانةٌ زائدة على القالب. -/
def Reading.roots (rd : Jidh.Reading) : List Wazn.Root :=
  rd.templates.filterMap (rootOfTemplate · (Jidh.stemForm rd.asl))

/-- قراءةٌ مشهودة: أحدُ جذورها في المقاييس. -/
def attested (rd : Jidh.Reading) : Bool := (Reading.roots rd).any member

/-- الترتيبُ بالقرينة: المشهودُ أوّلًا ثمّ الباقي، بترتيبه. -/
def rank (rs : List Jidh.Reading) : List Jidh.Reading := rs.filter attested ++ rs.filter (fun rd => !attested rd)

/-- الترتيبُ لا يُسقط قراءةً ولا يزيدها. -/
theorem mem_rank (rs : List Jidh.Reading) (rd : Jidh.Reading) : rd ∈ rank rs ↔ rd ∈ rs := by
  simp only [rank, List.mem_append, List.mem_filter, Bool.not_eq_true']
  constructor
  · rintro (⟨h, _⟩ | ⟨h, _⟩) <;> exact h
  · intro h
    cases ha : attested rd
    · exact Or.inr ⟨h, rfl⟩
    · exact Or.inl ⟨h, rfl⟩

theorem length_rank : ∀ rs : List Jidh.Reading, (rank rs).length = rs.length
  | [] => rfl
  | rd :: rs => by
    have ih := length_rank rs
    simp only [rank, List.length_append] at ih ⊢
    cases ha : attested rd <;> simp [ha] <;> omega

/-- قراءةٌ صورةُ أصلها ملءُ قالبٍ سليم `k` من قوالبها بجذرٍ مشهود قراءةٌ مشهودة. -/
theorem attested_of_member (rd : Jidh.Reading) (k : Nat) (hk : k ∈ rd.templates) (r : Wazn.Root)
    (hwf : Wazn.WF (Sarf.templ k)) (hasl : Jidh.stemForm rd.asl = Wazn.fill (Sarf.templ k) r)
    (hm : member r = true) :
    attested rd = true := by
  unfold attested
  rw [List.any_eq_true]
  refine ⟨r, ?_, hm⟩
  unfold Reading.roots
  rw [List.mem_filterMap]
  refine ⟨k, hk, ?_⟩
  unfold rootOfTemplate
  rw [hasl, Wazn.rootOf_fill _ hwf r 0, Wazn.rootOf_fill _ hwf r 1, Wazn.rootOf_fill _ hwf r 2]
  simp only [Option.some.injEq]
  funext i
  match i with
  | 0 => rfl
  | 1 => rfl
  | 2 => rfl

/-! ## الشواهد بالحساب -/

def qwl : Wazn.Root := fun i => if i = 0 then 21 else if i = 1 then 27 else 23   -- قول
def qyl : Wazn.Root := fun i => if i = 0 then 21 else if i = 1 then 28 else 23   -- قيل
def ktb : Wazn.Root := fun i => if i = 0 then 22 else if i = 1 then 3 else 2     -- كتب
def dhbw : Wazn.Root := fun i => if i = 0 then 9 else if i = 1 then 2 else 27    -- ذبو
def rmy : Wazn.Root := fun i => if i = 0 then 10 else if i = 1 then 24 else 28   -- رمي (رمى في الطبعة)
def rmw : Wazn.Root := fun i => if i = 0 then 10 else if i = 1 then 24 else 27   -- رمو: المعتلّةُ تطابقه أيضًا

set_option maxRecDepth 100000 in
/-- قول وقيل وكتب مشهودة؛ ذبو ليست؛ ورمى في الطبعة يطابق رمي ورمو معًا (المعتلّةُ مجهولةُ العين). -/
theorem member_witnesses :
    member qwl = true ∧ member qyl = true ∧ member ktb = true ∧ member dhbw = false ∧
    member rmy = true ∧ member rmw = true := by decide +kernel

set_option maxRecDepth 100000 in
/-- كَذَّبُوا: القراءةُ على فَعَّلَ بجذر كذب مشهودة، وقراءةُ كَ + الذَّبُو ليست — فالقرينةُ تفصلهما. -/
theorem rank_kadhdhabu :
    (rank (Jidh.jidh Jidh.kadhdhabu)).map (fun rd => (attested rd, rd.al, rd.templates)) =
      [(true, .none, [12]), (false, .silent, [2]), (false, .silent, [0, 36]), (false, .silent, [0, 36]),
       (false, .silent, [2]), (false, .silent, [2])] := by decide +kernel

set_option maxRecDepth 100000 in
/-- قَالَ: الأصلان قول وقيل كلاهما مشهود — القرينةُ المعجميّة لا تفصلهما، وهذا يُقال باسمه. -/
theorem rank_qala : (rank (Jidh.jidh Ilal.qala)).map attested = [true, true] := by decide +kernel

set_option maxRecDepth 100000 in
/-- فَرِيقٌ: التنوينُ خانةٌ زائدة على القالب؛ الجذرُ من صورة الجذع بلا تنوين (فَعِيل، فرق مشهود) لا من الجذع
كما هو — وقراءةُ فَ+رِيق على فِعْل (121) مشهودةٌ أيضًا (ريق): القرينةُ هنا لا تفصل، وهذا يُقال باسمه. -/
theorem rank_fariqun :
    (rank (Jidh.jidh Jidh.fariqun)).map (fun rd => (attested rd, rd.templates)) =
      [(true, [53]), (true, [121])] := by decide +kernel

end Slge.Maqayis
