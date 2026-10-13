import Slge.Jidh
import Slge.Zaman
import Slge.Istifham
import Slge.Marifa
import Slge.Khamsa

/-!
# الموزِّع — المبنيّاتُ تُقرأ من جدولها قبل القوالب

الحروفُ والضمائرُ وأسماءُ الإشارة والاستفهام والموصولُ والظروفُ المودَعة لا قالبَ لها؛ الجدولُ `table` جمعُها من
جداولها القائمة (`Rawabit.particles` غيرَ المتّصلة، `Categories.pronouns`، `Damair.nasbDetached`، `Ishara.forms`،
`Istifham.forms`، `Marifa.mawsul`، `Zuruf.forms` و`constants`، `Zaman.forms` و`constants`)، وكلُّها مرخَّصة (`table_licensed`). القراءةُ: سوابقُ من
`Jidh.proclitics` (حتى اثنتين) + مبنيٌّ من الجدول + لاحقةُ ضميرٍ من `Filiyya.objectSuffixes` أو لا لاحقة؛ والتعديلاتُ المسمّاة:
مع اللاحقة الألفُ المقصورة ياءً (`alifToYa`) ولامُ الجرّ مفتوحة (`lamFatha`)، وبدونها آخرُ الساكن مكسورًا أو
مفتوحًا لالتقاء الساكنين (`junction`)؛ والحروفُ المتّصلة حواملُ لا تُقرأ إلّا بلاحقة (`hosts`). المبرهَن: كلُّ قراءةٍ تُردّ إلى الكلمة
بعينها (`tawzi_restores`)، ومبنيُّها من الجدول أو حاملٌ (`tawzi_core_mem`)، والحاملُ لا يُقرأ إلّا بلاحقة (`tawzi_host_suf`)، ولا لاحقةَ إلّا من جدولها (`tawzi_suf_mem`)؛
وشواهدُ على المودَع بـ`decide`.
-/

namespace Slge.Tawzi

open Slge.Categories (c)

/-- أفعالٌ في جدول أدوات الربط (`Rawabit.particles`، بابُ الشكّ والترجيح) لها قالبٌ تتصرّف عليه: ليست مبنيّةً
مغلقة، فتُترك لقارئ القوالب (`VERB_NOT_MABNI`). -/
def verbs : List String := ["ظَنَّ", "حَسِبَ"]

/-- موصولٌ لا سندَ له في الكتاب المختوم: ذُو الطائيّة؛ وذُو فيه اسمٌ من الخمسة («ذو مال» س12422، س12981) —
`DHU_TAI_UNSOURCED`. -/
def unsourced : List String := ["ذُو"]

/-- المبنيّاتُ المودَعة بصورها. -/
def table : List (List SCell) :=
  (Rawabit.particles.filter (fun p => !p.proclitic && !verbs.contains p.name)).map (·.cells) ++
    Categories.pronouns ++ Damair.nasbDetached ++ Ishara.forms.map (·.2) ++ Istifham.forms.map (·.2) ++
    (Marifa.mawsul.filter (fun p => !unsourced.contains p.1)).map (·.2) ++ Zuruf.forms ++ Zuruf.constants.map (·.2) ++ Zaman.forms ++
    Zaman.constants.map (·.2.1)

theorem table_licensed : table.all licensed = true := by decide +kernel

/-- حاملا الضمير من الحروف المتّصلة: باءُ الجرّ ولامُه وحدَهما (`HOST_BI_LI`). الكافُ «لو أضفتَ إلى الياء الكافَ التي
تجرّ بها لقلت ما أنت كي … ولكن العرب قلّما تكلّموا بذا» (الكتاب س8128–8130)، والتاءُ «لا تدخل إلّا في واحد» (س14027)،
والواوُ والفاءُ والسينُ والهمزةُ ولامُ التوكيد لا تعمل في الضمير. -/
def hosts : List (List SCell) := [[c 2 1], [c 23 1]]

theorem hosts_proclitic :
    hosts.all (fun h => (Rawabit.particles.filter (·.proclitic)).any (·.cells == h)) = true := by decide

/-- أَيُّ أَيَّ أَيِّ: معربٌ يُضاف إلى الضمير — «أيُّهم كان أخاك»، «أيُّهم تَرَ يأتِك» (الكتاب س532، س871؛
`AYY_WITH_SUFFIX`). -/
def ayyForms : List (List SCell) := [Istifham.ayy 2, Istifham.ayy 0, Istifham.ayy 1]

/-- ما يحمل لاحقةَ الضمير من المبنيّات القائمة بنفسها (`SUFFIX_HOSTS`): الجارُّ والناسخُ من الحروف، والظروف. -/
def sufTable : List (List SCell) :=
  (Rawabit.particles.filter (fun p => !p.proclitic && (p.amal == .jarr || p.amal == .nasbIsm))).map (·.cells) ++
    ayyForms ++
    Zuruf.forms ++ Zuruf.constants.map (·.2) ++ Zaman.forms

theorem sufTable_sub : sufTable.all table.contains = true := by decide +kernel

/-- مَا ومَنْ تتّصلان بالحرف قبلهما (فِيمَا، مِمَّا، عَمَّنْ، إِنَّمَا، كَأَنَّمَا). -/
def maMan : List (List SCell) := [[c 24 0, c 1 3], [c 24 0, c 25 3]]

/-- الوصلُ بمَا/مَنْ: النونُ الساكنة آخرَ الحرف ميمٌ مدغمةٌ في ميمهما (`NUN_MIM_IDGHAM`؛ «وتدغم النون مع الميم لأن
صوتهما واحد» الكتاب س21468)؛ وإلّا ضمٌّ بعينه. -/
def joinMa (a b : List SCell) : List SCell :=
  match a.reverse with
  | x :: rest => if x == c 25 3 then (c 24 3 :: rest).reverse ++ b else a ++ b
  | [] => b

/-- لَا تتّصل بالحرف قبلها والنونُ الساكنة آخرَه لامٌ مدغمة: «النونُ قد تُدغم مع اللام حتى تُبدل مكانها لام»
(الكتاب س8095؛ `NUN_LAM_IDGHAM`). -/
def joinLa (a : List SCell) : List SCell := a.dropLast ++ [c 23 3, c 23 0, c 1 3]

/-- ما يتّصل بلَا (`LA_COMPOUND`): أَنْ + لَا ← أَلَّا، إِنْ + لَا ← إِلَّا. -/
def laHeads : List String := ["أَنْ", "إِنْ"]

/-- المركَّباتُ المغلقة: كلُّ جارٍّ أو ناسخٍ من الحروف القائمة بنفسها موصولًا بمَا أو مَنْ (`MA_COMPOUND`)، وأَنْ
وإِنْ موصولتين بلَا. -/
def compounds : List (List SCell) :=
  ((Rawabit.particles.filter (fun p => !p.proclitic && (p.amal == .jarr || p.amal == .nasbIsm))).map
    (·.cells)).flatMap (fun a => maMan.map (joinMa a)) ++
  ((Rawabit.particles.filter (fun p => laHeads.contains p.name)).map (·.cells)).map joinLa

theorem compounds_licensed : compounds.all licensed = true := by decide +kernel

/-- الألفُ المقصورة آخرَ المبنيّ (بعد فتحة) ياءً ساكنة قبل اللاحقة؛ وإلّا كما هو. -/
def alifToYa (core : List SCell) : List SCell :=
  match core.reverse with
  | a :: p :: rest => if a == c 1 3 && p.state.val == 0 then (c 28 3 :: p :: rest).reverse else core
  | _ => core

/-- لامُ الجرّ مفتوحةً قبل الضمير (لَهُ)؛ وإلّا كما هو. -/
def lamFatha (core : List SCell) : List SCell := if core == [c 23 1] then [c 23 0] else core

/-- ياءُ الإضافة (المتكلّم) مفتوحةً أو ساكنة. -/
def yaSufs : List (List SCell) := [[c 28 0], [c 28 3]]

/-- آخرُ المبنيّ المتحرّكُ مكسورًا قبل ياء الإضافة (`KASR_BEFORE_YA`؛ «ليس من حرفٍ تلحقه ياءُ الإضافة إلّا كان متحرّكًا
مكسورًا» الكتاب س8106: إِنِّي، لَعَلِّي)؛ والساكنُ كما هو (مِنْ ← مِنِّي بنون الوقاية من الجدول). -/
def kasrLast (core : List SCell) : List SCell :=
  match core.reverse with
  | a :: rest => if a.state.val == 0 || a.state.val == 2 then (⟨a.carrier, ⟨1, by decide⟩⟩ :: rest).reverse
      else core
  | [] => core

/-- آخرُ المبنيّ الساكن — غيرَ حرف المدّ — مكسورًا أو مفتوحًا لالتقاء الساكنين (عَنِ، مِنَ) بلا لاحقة. -/
def isMadd (a : SCell) (before : Option SCell) : Bool :=
  a.carrier.val == 1 || (a.carrier.val == 27 && (before.map (·.state.val == 2)).getD false) ||
    (a.carrier.val == 28 && (before.map (·.state.val == 1)).getD false)

def junction (core : List SCell) : List (List SCell) :=
  match core.reverse with
  | a :: rest => if a.state.val == 3 && !isMadd a rest.head? then
      [(⟨a.carrier, ⟨1, by decide⟩⟩ :: rest).reverse, (⟨a.carrier, ⟨0, by decide⟩⟩ :: rest).reverse]
    else []
  | [] => []

/-- ميمُ الجمع الساكنة مضمومةً لالتقاء الساكنين (`JUNCTION_DAMMA`؛ «من أسكن هذه الميمات في الوصل لا يكسرها إذا كانت
بعدها ألفُ وصل ولكن يضمّها» الكتاب س18109–18110: هُمُ، أَنْتُمُ). -/
def mimDamma (core : List SCell) : List (List SCell) :=
  match core.reverse with
  | a :: rest => if a == c 24 3 then [(c 24 2 :: rest).reverse] else []
  | [] => []

/-- لاحقةُ الضمير بميم الجمع موصولةً: الميمُ مضمومةً أو مكسورةً لالتقاء الساكنين (`SUF_MIM_WASL`؛ «وعليهمُ المال
… ومن قال عليهمِ … كسر» الكتاب س18117–18124). -/
def mimWasl : List (List SCell) :=
  Filiyya.objectSuffixes.flatMap fun s =>
    match s.reverse with
    | a :: rest => if a == c 24 3 then [(c 24 2 :: rest).reverse, (c 24 1 :: rest).reverse] else []
    | [] => []

/-- كافُ الخطاب آخرَ المبنيّ (ذَلِكَ، تِلْكَ، أُولَئِكَ) تتبع المخاطَبَ بصور لاحقة الكاف (`KAF_KHITAB`: ذَلِكُمْ، تِلْكُمَا،
كَذَلِكِ). -/
def kafKhitab (core : List SCell) : List (List SCell) :=
  match core.reverse with
  | a :: rest => if a == c 22 0 then
      ((Filiyya.objectSuffixes ++ mimWasl).filter (fun s => s.head?.map (·.carrier.val == 22) == some true)).map
        fun k => rest.reverse ++ k
    else []
  | [] => []

/-- همزةُ الوصل في أوّل الموصول (ءَلْ) تسقط بعد سابقة (`WASL_DROP`؛ «إذا كان قبلها كلامٌ حُذفت»: وَلِلَّذِينَ). -/
def dropWasl (core : List SCell) : List (List SCell) :=
  match core with
  | a :: b :: rest => if a == c 0 0 && b == c 23 3 then [b :: rest] else []
  | _ => []

/-- نونُ «نَا» بعد النون المشدّدة تُحذف إحداهما: إِنَّنَا ← إِنَّا (`NUN_NA_IDGHAM`؛ «يستثقلون التضعيفَ … فحذفوا» في
إِنِّي وكَأَنِّي ولَكِنِّي، الكتاب س8091–8093، وقياسُ نَا عليها معلَن). -/
def nunNa (core suf : List SCell) : List (List SCell) :=
  if suf == [c 25 0, c 1 3] && core.reverse.take 2 == [c 25 0, c 25 3] then [core.dropLast] else []

/-- صورُ المبنيّ الجائزة في الكلمة: بلاحقةٍ (كما هو، ألفُه ياءً، لامُه مفتوحة، وآخرُه مكسورًا قبل ياء الإضافة) وبدونها
(كما هو، آخرُه لالتقاء الساكنين، كافُ خطابه بصورها، وهمزةُ وصله ساقطةً بعد سابقة)؛ ونونُ نَا بعد المشدّدة محذوفة. -/
def variants (hasPre : Bool) (core suf : List SCell) : List (List SCell) :=
  if suf.isEmpty then
    core :: junction core ++ mimDamma core ++ kafKhitab core ++
      (if hasPre && !compounds.contains core then dropWasl core else [])
  else [core, alifToYa core, lamFatha core] ++ (if yaSufs.contains suf then [kasrLast core] else []) ++
    nunNa core suf

/-- المبنيّاتُ الجائزة مع لاحقةٍ أو بدونها: بلا لاحقةٍ الجدولُ والمركَّبات، وباللاحقة حاملُها وحدَه. -/
def cores (suf : List SCell) : List (List SCell) :=
  if suf.isEmpty then table ++ compounds else sufTable ++ hosts

/-- قراءةُ مبنيّ: السوابقُ، صورتُه في الجدول، صورتُه في الكلمة، اللاحقة. -/
structure Mabni where
  pre : List (List SCell)
  core : List SCell
  surface : List SCell
  suf : List SCell
  deriving DecidableEq, Repr

/-- الردُّ: السوابقُ ثمّ الصورةُ ثمّ اللاحقة. -/
def restore (m : Mabni) : List SCell := m.pre.flatten ++ m.surface ++ m.suf

def pres : List (List (List SCell)) :=
  [[]] ++ Jidh.proclitics.map ([·]) ++ (Jidh.proclitics.flatMap fun p => Jidh.proclitics.map fun q => [p, q])

/-- اللواحق: ضمائرُ النصب والجرّ المتّصلة، وياءُ الإضافة ساكنة، وميمُ الجمع موصولة. -/
def sufs : List (List SCell) := [] :: Filiyya.objectSuffixes ++ [[c 28 3]] ++ mimWasl

/-- الصورةُ: ما بين السوابق واللاحقة. -/
def surfaceOf (w : List SCell) (pre : List (List SCell)) (suf : List SCell) : List SCell :=
  (w.drop pre.flatten.length).take (w.length - pre.flatten.length - suf.length)

/-- الجارُّ المتّصلُ المحض (بِ كَ تَ). -/
def jarrPre : List (List SCell) := [[c 2 1], [c 22 0], [c 3 0]]

/-- الجارُّ والحامل: «والجرُّ إنما يكون في كلّ اسمٍ مضافٍ إليه» (الكتاب س4192)، فلا يليان جارًّا متّصلًا محضًا
(`JARR_NEEDS_ISM`). -/
def jarrCores : List (List SCell) := (Rawabit.particles.filter (·.amal == .jarr)).map (·.cells) ++ hosts

/-- القيودُ المسمّاة على القراءة: صورةُ اسمٍ من الخمسة لا تُقطع حروفًا (`KHAMSA_WHOLE_FIRST`)؛ ولا جارَّ بعد جارٍّ
متّصلٍ محض (`JARR_NEEDS_ISM`)؛ ولا هاءَ ضميرٍ بعد أيّ (يا أيُّها: «جاءوا بيا أيها ليصلوا…» س5503–5505،
`AYYUHA_VOCATIVE`). -/
def allowed (w : List SCell) (pre : List (List SCell)) (core suf : List SCell) : Bool :=
  !((pre != [] || suf != []) && Khamsa.forms.contains w) &&
  !((pre.getLast?.map jarrPre.contains).getD false && jarrCores.contains core) &&
  !(ayyForms.contains core && suf == [c 26 0, c 1 3])

/-- هل تقرأ (السوابقُ، المبنيُّ، اللاحقةُ) الكلمةَ؟ -/
def ok (w : List SCell) (pre : List (List SCell)) (core suf : List SCell) : Bool :=
  pre.flatten ++ surfaceOf w pre suf ++ suf == w && surfaceOf w pre suf != [] &&
    (variants (!pre.isEmpty) core suf).contains (surfaceOf w pre suf) && allowed w pre core suf

def readAt (w : List SCell) (pre : List (List SCell)) (core suf : List SCell) : Option Mabni :=
  if ok w pre core suf then some ⟨pre, core, surfaceOf w pre suf, suf⟩ else none

/-- قراءاتُ الكلمة مبنيًّا. -/
def tawzi (w : List SCell) : List Mabni :=
  (pres.filter (fun pre => pre.flatten.isPrefixOf w)).flatMap fun pre =>
    (sufs.filter (fun suf => suf.isSuffixOf w)).flatMap fun suf =>
      (cores suf).filterMap fun core => readAt w pre core suf

theorem ok_restore {w : List SCell} {pre : List (List SCell)} {core suf : List SCell}
    (h : ok w pre core suf = true) : pre.flatten ++ surfaceOf w pre suf ++ suf = w := by
  unfold ok at h
  simp only [Bool.and_eq_true, beq_iff_eq] at h
  exact h.1.1.1

theorem readAt_some {w : List SCell} {pre : List (List SCell)} {core suf : List SCell} {m : Mabni}
    (h : readAt w pre core suf = some m) :
    restore m = w ∧ m.pre = pre ∧ m.core = core ∧ m.suf = suf := by
  unfold readAt at h
  split at h
  · rename_i hc
    cases h
    exact ⟨ok_restore hc, rfl, rfl, rfl⟩
  · exact absurd h (by simp)

theorem tawzi_spec {w : List SCell} {m : Mabni} (h : m ∈ tawzi w) :
    restore m = w ∧ m.pre ∈ pres ∧ m.core ∈ cores m.suf ∧ m.suf ∈ sufs := by
  unfold tawzi at h
  obtain ⟨pre, hpre, h⟩ := List.mem_flatMap.1 h
  obtain ⟨suf, hsuf, h⟩ := List.mem_flatMap.1 h
  obtain ⟨core, hcore, h⟩ := List.mem_filterMap.1 h
  obtain ⟨hr, hp, hc, hs⟩ := readAt_some h
  exact ⟨hr, hp ▸ (List.mem_filter.1 hpre).1, hs ▸ hc ▸ hcore, hs ▸ (List.mem_filter.1 hsuf).1⟩

/-- كلُّ قراءةٍ تُردّ إلى الكلمة بعينها. -/
theorem tawzi_restores {w : List SCell} {m : Mabni} (h : m ∈ tawzi w) : restore m = w :=
  (tawzi_spec h).1

theorem sufTable_mem {x : List SCell} (hx : x ∈ sufTable) : x ∈ table := by
  have := List.all_eq_true.1 sufTable_sub x hx
  simpa using this

theorem cores_sub (suf : List SCell) : ∀ x ∈ cores suf, x ∈ table ++ compounds ++ hosts := by
  intro x hx
  unfold cores at hx
  split at hx
  · exact List.mem_append_left _ hx
  · rcases List.mem_append.1 hx with h | h
    · exact List.mem_append_left _ (List.mem_append_left _ (sufTable_mem h))
    · exact List.mem_append_right _ h

/-- مبنيُّ القراءة من الجدول أو من المركَّبات أو من الحوامل. -/
theorem tawzi_core_mem {w : List SCell} {m : Mabni} (h : m ∈ tawzi w) :
    m.core ∈ table ++ compounds ++ hosts :=
  cores_sub _ _ (tawzi_spec h).2.2.1

/-- الحاملُ لا يُقرأ وحدَه: ما ليس في الجدول ولا في المركَّبات لا يُقرأ إلّا بلاحقة. -/
theorem tawzi_host_suf {w : List SCell} {m : Mabni} (h : m ∈ tawzi w) (hc : m.core ∉ table ++ compounds) :
    m.suf ≠ [] := by
  intro hs
  have := (tawzi_spec h).2.2.1
  rw [hs] at this
  exact hc this

/-- اللاحقةُ لا يحملها إلّا حاملُها (`SUFFIX_HOSTS`، `HOST_BI_LI`): الجارُّ أو الناسخُ أو الظرف، أو باءُ الجرّ ولامُه —
فلا «وَ» حاملًا في وَهُمْ ولا «إِنْ» في إِنِّي. -/
theorem tawzi_suf_host {w : List SCell} {m : Mabni} (h : m ∈ tawzi w) (hs : m.suf ≠ []) :
    m.core ∈ sufTable ++ hosts := by
  have := (tawzi_spec h).2.2.1
  unfold cores at this
  split at this
  · rename_i he
    exact absurd (List.isEmpty_iff.1 he) hs
  · exact this

/-- لا لاحقةَ إلّا من جدول الضمائر المتّصلة (أو لا لاحقة). -/
theorem tawzi_suf_mem {w : List SCell} {m : Mabni} (h : m ∈ tawzi w) : m.suf ∈ sufs :=
  (tawzi_spec h).2.2.2

/-! ## شواهد على المودَع -/

def alayhim : List SCell := [c 18 0, c 23 0, c 28 3, c 26 1, c 24 3]      -- عَلَيْهِمْ
def ala : List SCell := [c 18 0, c 23 0, c 1 3]                            -- عَلَى
def lahum : List SCell := [c 23 0, c 26 2, c 24 3]                         -- لَهُمْ
def mina : List SCell := [c 24 1, c 25 0]                                  -- مِنَ
def bihi : List SCell := [c 2 1, c 26 1]                                   -- بِهِ
def waidha : List SCell := [c 27 0, c 0 1, c 9 0, c 1 3]                    -- وَإِذَا
def kataba : List SCell := [c 22 0, c 3 0, c 2 0]                           -- كَتَبَ

/-- عَلَيْهِمْ = عَلَى (ألفُه ياءً) + هِمْ. -/
theorem witness_alayhim :
    (tawzi alayhim).any (fun m => m.pre == [] && m.core == ala && m.suf == [c 26 1, c 24 3]) = true := by
  decide +kernel

/-- لَهُمْ = لَ + هُمْ (ضميرًا منفصلًا بعد سابقة) أو لِ (مفتوحةً) + هُمْ (حاملٌ بلاحقة). -/
theorem witness_lahum :
    (tawzi lahum).any (fun m => m.pre == [[c 23 0]] && m.core == [c 26 2, c 24 3] && m.suf == []) = true ∧
    (tawzi lahum).any (fun m => m.pre == [] && m.core == [c 23 1] && m.suf == [c 26 2, c 24 3]) = true := by
  decide +kernel

/-- وَإِذَا = وَ + إِذَا؛ مِنَ = مِنْ لالتقاء الساكنين؛ بِهِ = الحاملُ بِ + هِ. -/
theorem witness_particles :
    (tawzi waidha).any (fun m => m.pre == [[c 27 0]] && m.suf == []) = true ∧
    (tawzi mina).any (fun m => m.core == [c 24 1, c 25 3] && m.surface == mina) = true ∧
    (tawzi bihi).any (fun m => m.core == [c 2 1] && m.suf == [c 26 1]) = true := by
  decide +kernel

/-- كَتَبَ ليس مبنيًّا، وبِ وحدَها حاملٌ لا يُقرأ. -/
theorem witness_none : tawzi kataba = [] ∧ tawzi [c 2 1] = [] := by decide +kernel

/-! ## الإغلاق: شواهدُ القواعد المسمّاة (ADR ٥٣) -/

def lahumu : List SCell := [c 23 0, c 26 2, c 24 2]                        -- لَهُمُ
def li : List SCell := [c 23 1, c 28 3]                                    -- لِيْ
def walladhina : List SCell := [c 27 0, c 23 3, c 23 0, c 9 1, c 28 3, c 25 0]  -- وَلْلَذِيْنَ
def fima : List SCell := [c 20 1, c 28 3, c 24 0, c 1 3]                   -- فِيمَا
def mimma : List SCell := [c 24 1, c 24 3, c 24 0, c 1 3]                  -- مِمَّا
def dhalikum : List SCell := [c 9 0, c 23 1, c 22 2, c 24 3]               -- ذَلِكُمْ
def inni : List SCell := [c 0 1, c 25 3, c 25 1, c 28 3]                   -- إِنِّي
def wahum : List SCell := [c 27 0, c 26 2, c 24 3]                         -- وَهُمْ
def humu : List SCell := [c 26 2, c 24 2]                                  -- هُمُ

/-- لَهُمُ = لِ + هُمُ (ميمُ الجمع موصولة)؛ لِيْ = لِ + ياءُ الإضافة ساكنة؛ هُمُ = هُمْ مضمومَ الميم. -/
theorem witness_mim_ya :
    (tawzi lahumu).any (fun m => m.core == [c 23 1] && m.suf == [c 26 2, c 24 2]) = true ∧
    (tawzi li).any (fun m => m.core == [c 23 1] && m.suf == [c 28 3]) = true ∧
    (tawzi humu).any (fun m => m.core == [c 26 2, c 24 3] && m.suf == []) = true := by
  decide +kernel

/-- وَلِلَّذِينَ بلا همزة الوصل بعد الواو؛ فِيمَا ومِمَّا مركَّبان (مِنْ + مَا بإدغام النون في الميم)؛ ذَلِكُمْ بكاف
الخطاب؛ إِنِّي = إِنَّ مكسورةً قبل ياء الإضافة. -/
theorem witness_closure :
    (tawzi walladhina).any (fun m => m.pre == [[c 27 0]] && m.surface == walladhina.drop 1) = true ∧
    (tawzi fima).any (fun m => m.core == fima && m.suf == []) = true ∧
    (tawzi mimma).any (fun m => m.core == mimma && m.pre == []) = true ∧
    (tawzi dhalikum).any (fun m => m.core == [c 9 0, c 23 1, c 22 0] && m.suf == []) = true ∧
    (tawzi inni).all (fun m => m.core == [c 0 1, c 25 3, c 25 0] && m.suf == [c 28 3]) = true ∧
    (tawzi inni).length = 1 := by
  decide +kernel

/-- الواوُ ليست حاملًا: وَهُمْ = وَ + هُمْ ضميرًا منفصلًا، ولا قراءةَ فيها بلاحقة. -/
theorem witness_wa_not_host :
    (tawzi wahum).all (fun m => m.suf == []) = true ∧ (tawzi wahum).length > 0 := by
  decide +kernel

/-! ## سدادُ الديون (ADR ٥٤) -/

def inna : List SCell := [c 0 1, c 25 3, c 25 0, c 1 3]                    -- إِنَّا
def alla : List SCell := [c 0 0, c 23 3, c 23 0, c 1 3]                    -- أَلَّا
def ayyuhum : List SCell := [c 0 0, c 28 3, c 28 2, c 26 2, c 24 3]        -- أَيُّهُمْ
def ayyuha : List SCell := [c 0 0, c 28 3, c 28 2, c 26 0, c 1 3]          -- أَيُّهَا
def akalahu : List SCell := [c 0 0, c 22 0, c 23 0, c 26 2]                -- أَكَلَهُ
def abi : List SCell := [c 0 0, c 2 1, c 28 3]                             -- أَبِي
def dhu : List SCell := [c 9 2, c 27 3]                                    -- ذُو

/-- إِنَّا = إِنَّ + نَا بحذف إحدى النونات؛ أَلَّا = أَنْ + لَا بإدغام النون في اللام؛ أَيُّهُمْ = أَيُّ + هُمْ — كلٌّ
قراءةٌ واحدة. -/
theorem witness_debts_read :
    (tawzi inna).map (fun m => (m.core, m.suf)) = [([c 0 1, c 25 3, c 25 0], [c 25 0, c 1 3])] ∧
    (tawzi alla).map (fun m => (m.pre, m.core)) = [([], alla)] ∧
    (tawzi ayyuhum).map (fun m => (m.core, m.suf)) = [(Istifham.ayy 2, [c 26 2, c 24 3])] := by
  decide +kernel

/-- ولا تُقرأ: يا أَيُّهَا (هاءُ التنبيه)، أَكَلَهُ (لا جارَّ بعد الكاف)، أَبِي (اسمٌ من الخمسة)، ذُو (لا سندَ لموصوله). -/
theorem witness_debts_refused :
    tawzi ayyuha = [] ∧ tawzi akalahu = [] ∧ tawzi abi = [] ∧ tawzi dhu = [] := by
  decide +kernel

end Slge.Tawzi
