import Slge.Fil

/-!
# حروفُ المعاني والأدوات: جدولٌ واحدٌ يجمع المودَعات، وعملُها عمليّاتٌ في أبوابها

الحصرُ ثلاثُ مجموعات (المختصّةُ بالأسماء، المختصّةُ بالأفعال، المشتركة)، والقانونُ: الأداةُ أعمُّ من الحرف.
على الخانات:
* **الحرفُ صورةٌ مودَعة**: `table` جدولٌ واحدٌ لـ68 مدخلًا (31، 18، 19: `counts`) خاناتُها خاناتُ أبوابها
  (`Majrurat.harfs`، `Nawasikh.innaSisters`، `Nida.particles`، `Jazm.jazimOne`، `Tawabi.nasaq`…)،
  مرخَّصةٌ كلُّها (`table_licensed`)، لا تنوينَ فيها — وما نونُه أصلٌ ساكنٌ بعد حركةٍ يشابه التنوينَ
  مسمًّى (`no_tanwin`: مِنْ عَنْ أَنْ لَنْ إِذَنْ إِنْ لَكِنْ)، وأَنَّ وحدَها تُقرأ أداةَ تعريفٍ شمسيّة (ءَ نْ نَ) — خانةٌ
  واحدةٌ باسمها؛ والمتّصلةُ (بِ لِ كَ وَ تَ فَ سَ أَ) لا تُفسد ما بعدها
  (`proclitics_keep_licence`).
* **الخانةُ الواحدةُ في أكثرَ من باب**: 68 مدخلًا على 53 صورة — لَا في أربعة، وَ في أربعة، حَتَّى في ثلاثة،
  لِ في ثلاثة، إِنْ وفَ في اثنين (`shared_cells`): العملُ من التيار لا من الخانة.
* **العملُ عمليّةٌ على ما بعد الحرف** بُرهنت في بابها ويحكم عليها جدولُ أدوات الربط (`amal_is_operation`:
  جرٌّ، نصبُ اسم، نصبُ مضارع، جزم)؛ وجدولُ أدوات الربط يشهد لكلّ عاملٍ فيه بعملِه (`rawabit_agrees`؛
  ومَا الشرطيّةُ اسمٌ في هذا الحصر فتُستثنى)؛ والتنفيسُ بلا أثر: سَيَقُولُ شاهدُ بوّابة (`sawfa_witness`).
الاختصاصُ (اسمٌ بعدها أم فعل) والمعنى (ردعٌ، تحقيقٌ، تنبيه…) حدٌّ ومعلَن. القياسُ على MASAQ في بايثون.
-/

namespace Slge.Huruf

open Slge.Categories (c)

inductive Class where
  | ism | fil | mushtarak
  deriving DecidableEq, Repr

inductive Amal where
  | jarr | nasbIsm | nida | maiyya | nasbFil | jazm | jazm2 | tabi | none
  deriving DecidableEq, Repr

structure Harf where
  name : String
  cells : List SCell
  cls : Class
  amal : Amal
  deriving Repr

/-- الجدولُ الموحَّد (68). -/
def table : List Harf := [
  ⟨"بِ", [c 2 1], .ism, .jarr⟩,
  ⟨"لِ", [c 23 1], .ism, .jarr⟩,
  ⟨"كَ", [c 22 0], .ism, .jarr⟩,
  ⟨"وَ", [c 27 0], .ism, .jarr⟩,
  ⟨"تَ", [c 3 0], .ism, .jarr⟩,
  ⟨"مِنْ", [c 24 1, c 25 3], .ism, .jarr⟩,
  ⟨"إِلَى", [c 0 1, c 23 0, c 1 3], .ism, .jarr⟩,
  ⟨"عَنْ", [c 18 0, c 25 3], .ism, .jarr⟩,
  ⟨"عَلَى", [c 18 0, c 23 0, c 1 3], .ism, .jarr⟩,
  ⟨"فِي", [c 20 1, c 28 3], .ism, .jarr⟩,
  ⟨"حَتَّى", [c 6 0, c 3 3, c 3 0, c 1 3], .ism, .jarr⟩,
  ⟨"مُذْ", [c 24 2, c 9 3], .ism, .jarr⟩,
  ⟨"مُنْذُ", [c 24 2, c 25 3, c 9 2], .ism, .jarr⟩,
  ⟨"خَلَا", [c 7 0, c 23 0, c 1 3], .ism, .jarr⟩,
  ⟨"عَدَا", [c 18 0, c 8 0, c 1 3], .ism, .jarr⟩,
  ⟨"حَاشَا", [c 6 0, c 1 3, c 13 0, c 1 3], .ism, .jarr⟩,
  ⟨"رُبَّ", [c 10 2, c 2 3, c 2 0], .ism, .jarr⟩,
  ⟨"إِنَّ", [c 0 1, c 25 3, c 25 0], .ism, .nasbIsm⟩,
  ⟨"أَنَّ", [c 0 0, c 25 3, c 25 0], .ism, .nasbIsm⟩,
  ⟨"كَأَنَّ", [c 22 0, c 0 0, c 25 3, c 25 0], .ism, .nasbIsm⟩,
  ⟨"لَكِنَّ", [c 23 0, c 22 1, c 25 3, c 25 0], .ism, .nasbIsm⟩,
  ⟨"لَيْتَ", [c 23 0, c 28 3, c 3 0], .ism, .nasbIsm⟩,
  ⟨"لَعَلَّ", [c 23 0, c 18 0, c 23 3, c 23 0], .ism, .nasbIsm⟩,
  ⟨"أَ", [c 0 0], .ism, .nida⟩,
  ⟨"أَيْ", [c 0 0, c 28 3], .ism, .nida⟩,
  ⟨"أَيَا", [c 0 0, c 28 0, c 1 3], .ism, .nida⟩,
  ⟨"هَيَا", [c 26 0, c 28 0, c 1 3], .ism, .nida⟩,
  ⟨"يَا", [c 28 0, c 1 3], .ism, .nida⟩,
  ⟨"وَا", [c 27 0, c 1 3], .ism, .nida⟩,
  ⟨"لَا (النافية للجنس)", [c 23 0, c 1 3], .ism, .nasbIsm⟩,
  ⟨"وَ (المعيّة)", [c 27 0], .ism, .maiyya⟩,
  ⟨"أَنْ", [c 0 0, c 25 3], .fil, .nasbFil⟩,
  ⟨"لَنْ", [c 23 0, c 25 3], .fil, .nasbFil⟩,
  ⟨"كَيْ", [c 22 0, c 28 3], .fil, .nasbFil⟩,
  ⟨"إِذَنْ", [c 0 1, c 9 0, c 25 3], .fil, .nasbFil⟩,
  ⟨"لِ (كي/الجحود)", [c 23 1], .fil, .nasbFil⟩,
  ⟨"حَتَّى (النصب)", [c 6 0, c 3 3, c 3 0, c 1 3], .fil, .nasbFil⟩,
  ⟨"فَ (السببيّة)", [c 20 0], .fil, .nasbFil⟩,
  ⟨"وَ (المعيّة)", [c 27 0], .fil, .nasbFil⟩,
  ⟨"لَمْ", [c 23 0, c 24 3], .fil, .jazm⟩,
  ⟨"لَمَّا", [c 23 0, c 24 3, c 24 0, c 1 3], .fil, .jazm⟩,
  ⟨"لِ", [c 23 1], .fil, .jazm⟩,
  ⟨"لَا", [c 23 0, c 1 3], .fil, .jazm⟩,
  ⟨"إِنْ", [c 0 1, c 25 3], .fil, .jazm2⟩,
  ⟨"إِذْمَا", [c 0 1, c 9 3, c 24 0, c 1 3], .fil, .jazm2⟩,
  ⟨"سَ", [c 12 0], .fil, .none⟩,
  ⟨"سَوْفَ", [c 12 0, c 27 3, c 20 0], .fil, .none⟩,
  ⟨"كَلَّا", [c 22 0, c 23 3, c 23 0, c 1 3], .fil, .none⟩,
  ⟨"قَدْ", [c 21 0, c 8 3], .fil, .none⟩,
  ⟨"وَ", [c 27 0], .mushtarak, .tabi⟩,
  ⟨"فَ", [c 20 0], .mushtarak, .tabi⟩,
  ⟨"ثُمَّ", [c 4 2, c 24 3, c 24 0], .mushtarak, .tabi⟩,
  ⟨"حَتَّى", [c 6 0, c 3 3, c 3 0, c 1 3], .mushtarak, .tabi⟩,
  ⟨"أَوْ", [c 0 0, c 27 3], .mushtarak, .tabi⟩,
  ⟨"أَمْ", [c 0 0, c 24 3], .mushtarak, .tabi⟩,
  ⟨"لَا", [c 23 0, c 1 3], .mushtarak, .tabi⟩,
  ⟨"بَلْ", [c 2 0, c 23 3], .mushtarak, .tabi⟩,
  ⟨"لَكِنْ", [c 23 0, c 22 1, c 25 3], .mushtarak, .tabi⟩,
  ⟨"أَ", [c 0 0], .mushtarak, .none⟩,
  ⟨"هَلْ", [c 26 0, c 23 3], .mushtarak, .none⟩,
  ⟨"مَا", [c 24 0, c 1 3], .mushtarak, .none⟩,
  ⟨"لَا", [c 23 0, c 1 3], .mushtarak, .none⟩,
  ⟨"لَمْ", [c 23 0, c 24 3], .mushtarak, .jazm⟩,
  ⟨"لَنْ", [c 23 0, c 25 3], .mushtarak, .nasbFil⟩,
  ⟨"إِنْ (النفي)", [c 0 1, c 25 3], .mushtarak, .none⟩,
  ⟨"لَاتَ", [c 23 0, c 1 3, c 3 0], .mushtarak, .none⟩,
  ⟨"أَلَا", [c 0 0, c 23 0, c 1 3], .mushtarak, .none⟩,
  ⟨"أَمَا", [c 0 0, c 24 0, c 1 3], .mushtarak, .none⟩
]

def ism : List Harf := table.filter (·.cls == .ism)
def fil : List Harf := table.filter (·.cls == .fil)
def mushtarak : List Harf := table.filter (·.cls == .mushtarak)

theorem counts : ism.length = 31 ∧ fil.length = 18 ∧ mushtarak.length = 19 ∧ table.length = 68 := by
  decide

theorem table_licensed : table.all (fun h => licensed h.cells) = true := by decide

/-- لا تنوينَ في حرف؛ وما نونُه أصلٌ ساكنٌ بعد حركةٍ يقرؤه `Nida.hasTanwin` تنوينًا — بالاسم. -/
theorem no_tanwin :
    (table.filter (fun h => Nida.hasTanwin h.cells)).map (·.name) =
      ["مِنْ", "عَنْ", "أَنْ", "لَنْ", "إِذَنْ", "إِنْ", "لَكِنْ", "لَنْ", "إِنْ (النفي)"] ∧
    (table.filter (fun h => Marifa.hasAl h.cells)).map (·.name) = ["أَنَّ"] := by decide

/-- المتّصلةُ (خانةٌ واحدةٌ متحرّكة) لا تُفسد ما بعدها. -/
theorem proclitics_keep_licence (w : List SCell) (hw : licensed w = true) :
    ∀ h ∈ table, h.cells.length = 1 → licensed (h.cells ++ w) = true := by
  intro h hm hl
  have key : table.all (fun h => h.cells.length != 1 ||
      (h.cells.head?.map (fun x => x.state.val != 3)).getD false) = true := by decide
  have hk := List.all_eq_true.1 key h hm
  cases hc : h.cells with
  | nil => simp [hc] at hl
  | cons x t =>
    cases t with
    | nil =>
      rw [hc] at hk
      have hst : x.state.val ≠ 3 := by simpa using hk
      simpa using Rawabit.proclitic_keeps_licence x.carrier x.state hst w hw
    | cons y u => simp [hc] at hl

/-- 68 مدخلًا على 53 صورة؛ لَا ووَ أربعًا، حَتَّى ولِ ثلاثًا، إِنْ وفَ اثنين. -/
theorem shared_cells :
    (table.map (·.cells)).eraseDups.length = 53 ∧
    (table.filter (·.cells == [c 23 0, c 1 3])).length = 4 ∧
    (table.filter (·.cells == [c 27 0])).length = 4 ∧
    (table.filter (·.cells == [c 6 0, c 3 3, c 3 0, c 1 3])).length = 3 ∧
    (table.filter (·.cells == [c 23 1])).length = 3 ∧
    (table.filter (·.cells == [c 0 1, c 25 3])).length = 2 ∧
    (table.filter (·.cells == [c 20 0])).length = 2 := by decide

/-- العملُ عمليّةٌ على ما بعد الحرف: مجرورٌ بعد الجارّ، منصوبُ الاسم بعد المشبّهة، منصوبُ المضارع
بعد الناصب، مجزومٌ بعد الجازم — ويحكم بها جدولُ أدوات الربط. -/
theorem amal_is_operation (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) (w : List SCell)
    (hne : w ≠ []) :
    Rawabit.govern .jarr (Majrurat.jarr w) = true ∧
    Rawabit.govern .nasbIsm (Nawasikh.nasb w) = true ∧
    Rawabit.govern .nasb (Afal.form pr s p .nasb) = true ∧
    Rawabit.govern .jazm (Afal.form pr s p .jazm) = true := by
  refine ⟨Majrurat.govern_jarr w hne, ?_, Rawabit.govern_nasb_afal pr s p,
    Rawabit.govern_jazm_afal pr s p⟩
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast w 0 hne
  unfold Rawabit.govern Rawabit.lastState Nawasikh.nasb; rw [hk]; rfl

def toRawabit : Amal → Rawabit.Amal
  | .jarr => .jarr | .nasbIsm => .nasbIsm | .nasbFil => .nasb | .jazm => .jazm | .jazm2 => .jazm
  | _ => .none

/-- كلُّ عاملٍ في جدول أدوات الربط اسمُه في هذا الجدول له مدخلٌ بعملِه نفسِه — إلّا مَا: شرطيّةً اسمٌ
في هذا الحصر (جزمُها في `Jazm.shartJazim`) ونافيةً حرفٌ بلا عمل. -/
theorem rawabit_agrees :
    (Rawabit.particles.filter (fun p => p.amal != .none && p.name != "مَا" &&
        table.any (·.name == p.name))).all
      (fun p => table.any (fun h => h.name == p.name && toRawabit h.amal == p.amal)) = true ∧
    Rawabit.particles.any (fun p => p.name == "مَا" && p.amal == .jazm) = true ∧
    Jazm.shartJazim.any (·.1 == "مَا") = true := by decide

/-- التنفيسُ بلا أثر: سَيَقُولُ (بوّابة) = سَ + يَقُولُ، وسَوْفَ مودَعة. -/
theorem sawfa_witness :
    [c 12 0] ++ Jazm.yaqulu = [c 12 0, c 28 0, c 21 2, c 27 3, c 23 2] ∧
    licensed ([c 12 0] ++ Jazm.yaqulu) = true ∧
    table.any (fun h => h.name == "سَوْفَ" && h.cells == [c 12 0, c 27 3, c 20 0] && h.amal == .none) =
      true := by decide

end Slge.Huruf
