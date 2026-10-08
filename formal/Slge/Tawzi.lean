import Slge.Jidh
import Slge.Zaman
import Slge.Istifham
import Slge.Marifa

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

/-- المبنيّاتُ المودَعة بصورها. -/
def table : List (List SCell) :=
  (Rawabit.particles.filter (fun p => !p.proclitic)).map (·.cells) ++ Categories.pronouns ++
    Damair.nasbDetached ++ Ishara.forms.map (·.2) ++ Istifham.forms.map (·.2) ++
    Marifa.mawsul.map (·.2) ++ Zuruf.forms ++ Zuruf.constants.map (·.2) ++ Zaman.forms ++
    Zaman.constants.map (·.2.1)

theorem table_licensed : table.all licensed = true := by decide +kernel

/-- الحروفُ المتّصلة (بِ لِ كَ وَ…): مبنيٌّ حاملٌ لضميرٍ فقط (بِهِ، لَكُمْ). -/
def hosts : List (List SCell) := (Rawabit.particles.filter (·.proclitic)).map (·.cells)

/-- الألفُ المقصورة آخرَ المبنيّ (بعد فتحة) ياءً ساكنة قبل اللاحقة؛ وإلّا كما هو. -/
def alifToYa (core : List SCell) : List SCell :=
  match core.reverse with
  | a :: p :: rest => if a == c 1 3 && p.state.val == 0 then (c 28 3 :: p :: rest).reverse else core
  | _ => core

/-- لامُ الجرّ مفتوحةً قبل الضمير (لَهُ)؛ وإلّا كما هو. -/
def lamFatha (core : List SCell) : List SCell := if core == [c 23 1] then [c 23 0] else core

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

/-- صورُ المبنيّ الجائزة في الكلمة: بلاحقةٍ (كما هو، ألفُه ياءً، لامُه مفتوحة) وبدونها (كما هو، آخرُه
لالتقاء الساكنين). -/
def variants (core suf : List SCell) : List (List SCell) :=
  if suf.isEmpty then core :: junction core else [core, alifToYa core, lamFatha core]

/-- المبنيّاتُ الجائزة مع لاحقةٍ أو بدونها: الحاملُ لا يُقرأ وحدَه. -/
def cores (suf : List SCell) : List (List SCell) := if suf.isEmpty then table else table ++ hosts

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

def sufs : List (List SCell) := [] :: Filiyya.objectSuffixes

/-- الصورةُ: ما بين السوابق واللاحقة. -/
def surfaceOf (w : List SCell) (pre : List (List SCell)) (suf : List SCell) : List SCell :=
  (w.drop pre.flatten.length).take (w.length - pre.flatten.length - suf.length)

/-- هل تقرأ (السوابقُ، المبنيُّ، اللاحقةُ) الكلمةَ؟ -/
def ok (w : List SCell) (pre : List (List SCell)) (core suf : List SCell) : Bool :=
  pre.flatten ++ surfaceOf w pre suf ++ suf == w && surfaceOf w pre suf != [] &&
    (variants core suf).contains (surfaceOf w pre suf)

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
  exact h.1.1

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

theorem cores_sub (suf : List SCell) : ∀ x ∈ cores suf, x ∈ table ++ hosts := by
  intro x hx
  unfold cores at hx
  split at hx
  · exact List.mem_append_left _ hx
  · exact hx

/-- مبنيُّ القراءة من الجدول أو من الحوامل. -/
theorem tawzi_core_mem {w : List SCell} {m : Mabni} (h : m ∈ tawzi w) : m.core ∈ table ++ hosts :=
  cores_sub _ _ (tawzi_spec h).2.2.1

/-- الحاملُ لا يُقرأ وحدَه: ما ليس في الجدول لا يُقرأ إلّا بلاحقة. -/
theorem tawzi_host_suf {w : List SCell} {m : Mabni} (h : m ∈ tawzi w) (hc : m.core ∉ table) :
    m.suf ≠ [] := by
  intro hs
  have := (tawzi_spec h).2.2.1
  rw [hs] at this
  exact hc this

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

end Slge.Tawzi
