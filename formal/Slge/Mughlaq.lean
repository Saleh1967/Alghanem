import Slge.Tawzi
import Slge.Maani

/-!
# الصنفُ المغلق: وسمٌ يفصل المبنيّات عن الاسم والفعل (ADR ٥٣، طلبُ المالك 2026-10-13)

الأدواتُ وحروفُ المعاني والضمائرُ وأسماءُ الإشارة والاستفهام والموصولُ — منفصلةً ومتّصلةً ومتّصلًا بعضُها ببعض
(مِنْهُمْ، لَكُمْ، وَمِنْ، وَمِنْكُمْ، فِيمَا) — **صنفٌ مغلق**: يقرؤها الموزِّع (`Tawzi.tawzi`) من جداولها المودَعة
بقواعد مسمّاة لا من قالب. والوسمُ ثلاثيّ: **مغلق** إن قرأه الموزِّعُ بنواةٍ ليست ظرفًا، و**ظرف** إن لم يقرأه إلّا ظرفًا
(فالظرفُ اسمٌ مبنيٌّ أو متصرِّف يقرؤه الجدول ولا يُعدّ أداةً)، و**مفتوح** إن لم يقرأه الموزِّعُ — فيُترك للاسم والفعل.

المبرهَن:
* **القسمةُ تامّةٌ مانعة**: كلُّ كلمةٍ بوسمٍ واحد (`qism` دالّة)، والمفتوحُ هو ما لا يقرؤه الموزِّعُ بعينه
  (`maftuh_iff`)، والمغلقُ ما له قراءةٌ نواتُها غيرُ ظرف (`mughlaq_iff`)، وقراءةُ المغلق تُردّ إلى الكلمة بعينها
  (`closed_restores`).
* **إغلاقُ التعريف والمعنى**: لكلّ نواةٍ مغلقة يقرؤها الموزِّعُ — من الجدول أو المركَّبات أو الحاملَين — مصدرُ معنًى
  مسمًّى (`closed_has_src`): معانيها من مبحث الحرف المختوم (`Maani`)، أو عملُها من جدول الحروف الموحَّد، أو بابُها في
  أدوات الربط، أو بابُها ضميرًا أو إشارةً أو استفهامًا أو موصولًا، أو تركيبُها من حرفٍ ومَا/مَنْ.
* **الشواهد**: لَهُمُ ووَهُمْ ومِنْكُمْ وفِيمَا مغلقة، وعِنْدَهُ ظرف، وكَتَبَ مفتوح.
-/

namespace Slge.Mughlaq

open Slge.Categories (c)

/-- الوسمُ الثلاثيّ. -/
inductive Qism where
  | mughlaq | zarf | maftuh
  deriving DecidableEq, Repr

/-- صورُ الظروف المودَعة (`Zuruf`، `Zaman`). -/
def zarfCells : List (List SCell) :=
  Zuruf.forms ++ Zuruf.constants.map (·.2) ++ Zaman.forms ++ Zaman.constants.map (·.2.1)

/-- نواةٌ مغلقة: ما ليس ظرفًا من نوى الموزِّع. -/
def closedCore (core : List SCell) : Bool := !zarfCells.contains core

/-- قراءاتُ الموزِّع المغلقة. -/
def closed (w : List SCell) : List Tawzi.Mabni := (Tawzi.tawzi w).filter (closedCore ·.core)

/-- الوسم. -/
def qism (w : List SCell) : Qism :=
  if !(closed w).isEmpty then .mughlaq else if !(Tawzi.tawzi w).isEmpty then .zarf else .maftuh

theorem maftuh_iff (w : List SCell) : qism w = .maftuh ↔ Tawzi.tawzi w = [] := by
  unfold qism closed
  constructor
  · intro h
    by_cases h1 : (List.filter (fun x => closedCore x.core) (Tawzi.tawzi w)).isEmpty = true
    · by_cases h2 : (Tawzi.tawzi w).isEmpty = true
      · exact List.isEmpty_iff.1 h2
      · simp [h1, h2] at h
    · simp [h1] at h
  · intro h
    simp [h]

theorem mughlaq_iff (w : List SCell) :
    qism w = .mughlaq ↔ ∃ m ∈ Tawzi.tawzi w, closedCore m.core = true := by
  unfold qism closed
  constructor
  · intro h
    by_cases h1 : (List.filter (fun x => closedCore x.core) (Tawzi.tawzi w)).isEmpty = true
    · by_cases h2 : (Tawzi.tawzi w).isEmpty = true <;> simp [h1, h2] at h
    · obtain ⟨m, hm⟩ := List.exists_mem_of_ne_nil _ (fun e => h1 (List.isEmpty_iff.2 e))
      obtain ⟨hm, hc⟩ := List.mem_filter.1 hm
      exact ⟨m, hm, hc⟩
  · rintro ⟨m, hm, hc⟩
    have : (List.filter (fun x => closedCore x.core) (Tawzi.tawzi w)) ≠ [] :=
      List.ne_nil_of_mem (List.mem_filter.2 ⟨hm, hc⟩)
    simp [this]

/-- قراءةُ المغلق تُردّ إلى الكلمة بعينها. -/
theorem closed_restores {w : List SCell} {m : Tawzi.Mabni} (h : m ∈ closed w) : Tawzi.restore m = w :=
  Tawzi.tawzi_restores (List.mem_filter.1 h).1

/-! ## إغلاقُ المعنى -/

/-- مصدرُ معنى النواة المغلقة. -/
inductive Src where
  | nabhani             -- معانيها من مبحث الحرف المختوم (`Maani.sensesOf` لأحد مداخلها)
  | amal                -- عملُها من جدول الحروف الموحَّد (`Huruf.table`) ولا معنى لها في المصدر
  | rawabit             -- بابُها في أدوات الربط (`Rawabit.particles`، معلن)
  | damir               -- ضميرٌ منفصل (`Categories.pronouns`، `Damair.nasbDetached`)
  | ishara | istifham | mawsul
  | tarkib              -- حرفٌ جارٌّ أو ناسخٌ ومَا/مَنْ (`Tawzi.compounds`)
  deriving DecidableEq, Repr

/-- فهارسُ مداخل النواة في جدول الحروف الموحَّد (للصورة الواحدة مداخلُ: الواوُ جارّةً وعاطفة). -/
def hurufIdxs (core : List SCell) : List Nat :=
  (List.range Huruf.table.length).filter fun i => (Huruf.table[i]?.map (·.cells)) == some core

/-- المصدرُ بأوّل ما يوجد بترتيبٍ ثابت: حروفُ المعاني (بمعانيها إن ذكرها المصدرُ لأحد مداخلها، وإلّا بعملها)، ثمّ
أدواتُ الربط، ثمّ الضمائر، ثمّ الإشارة، ثمّ الاستفهام، ثمّ الموصول، ثمّ التركيب. -/
def src (core : List SCell) : Option Src :=
  if hurufIdxs core != [] then
    if (hurufIdxs core).any (fun i => Maani.sensesOf i != []) then some .nabhani else some .amal
  else
    if Rawabit.particles.any (·.cells == core) then some .rawabit
    else if (Categories.pronouns ++ Damair.nasbDetached).contains core then some .damir
    else if Ishara.forms.any (·.2 == core) then some .ishara
    else if Istifham.forms.any (·.2 == core) then some .istifham
    else if Marifa.mawsul.any (·.2 == core) then some .mawsul
    else if Tawzi.compounds.contains core then some .tarkib
    else none

/-- كلُّ نواةٍ مغلقةٍ يقرؤها الموزِّع لها مصدرُ معنًى مسمًّى. -/
theorem closed_has_src :
    (Tawzi.table ++ Tawzi.compounds ++ Tawzi.hosts).all (fun k => !closedCore k || (src k).isSome) = true := by
  decide +kernel

/-- فكلُّ قراءةٍ مغلقةٍ لنواتها مصدرُ معنى. -/
theorem closed_reading_has_src {w : List SCell} {m : Tawzi.Mabni} (h : m ∈ closed w) :
    (src m.core).isSome = true := by
  obtain ⟨hm, hc⟩ := List.mem_filter.1 h
  have := List.all_eq_true.1 closed_has_src m.core (Tawzi.tawzi_core_mem hm)
  simpa [hc] using this

/-! ## شواهد -/

def minkum : List SCell := [c 24 1, c 25 3, c 22 2, c 24 3]                -- مِنْكُمْ
def wamin : List SCell := [c 27 0, c 24 1, c 25 3]                         -- وَمِنْ
def indahu : List SCell := [c 18 1, c 25 3, c 8 0, c 26 2]                 -- عِنْدَهُ

theorem witness_qism :
    qism Tawzi.lahumu = .mughlaq ∧ qism Tawzi.wahum = .mughlaq ∧ qism minkum = .mughlaq ∧
    qism wamin = .mughlaq ∧ qism Tawzi.fima = .mughlaq ∧ qism Tawzi.walladhina = .mughlaq ∧
    qism indahu = .zarf ∧ qism Tawzi.kataba = .maftuh := by
  decide +kernel

/-! ## حدُّ الخطأ (ADR ٥٤): الوسمُ دالّةٌ في الخانات -/

theorem countP_ne_true (ls : List Bool) : ls.countP (fun x => x != true) = ls.count false := by
  have : (fun x : Bool => x != true) = (fun x => x == false) := by funext x; cases x <;> rfl
  rw [this, List.count]

theorem countP_ne_false (ls : List Bool) : ls.countP (fun x => x != false) = ls.count true := by
  have : (fun x : Bool => x != false) = (fun x => x == true) := by funext x; cases x <;> rfl
  rw [this, List.count]

/-- صورةٌ واحدة بوسمٍ واحد `b`، ومواضعُها بأصنافها عند مرجعٍ ما `ls` (صوابٌ = مغلق): لا ينزل خطؤها عن أقلّ
الصنفين. فما تساوت خاناتُه واختلف صنفُه عند المرجع حدٌّ أدنى للخطأ لا تفصله دالّةٌ في الخانات. -/
theorem const_errors_ge_min (ls : List Bool) (b : Bool) :
    min (ls.count true) (ls.count false) ≤ ls.countP (fun x => x != b) := by
  cases b
  · rw [countP_ne_false]; exact Nat.min_le_left _ _
  · rw [countP_ne_true]; exact Nat.min_le_right _ _

/-- والحدُّ يُبلَغ: الوسمُ بالأكثر خطؤه الأقلُّ بعينه. -/
theorem const_errors_majority (ls : List Bool) :
    ls.countP (fun x => x != decide (ls.count false ≤ ls.count true)) =
      min (ls.count true) (ls.count false) := by
  by_cases h : ls.count false ≤ ls.count true
  · simp only [h, decide_true, countP_ne_true]; omega
  · simp only [h, decide_false, countP_ne_false]; omega

end Slge.Mughlaq
