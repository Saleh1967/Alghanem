import Slge.Majrurat

/-!
# همزتا الوصل والقطع: الوصلُ حدٌّ، والقطعُ خانة، والحصرُ الصرفيُّ تقسيمٌ للقوالب

على الخانات الهمزتان **خانةٌ واحدة** في الابتداء (همزةٌ متحرّكةٌ فساكن: اِنْطِلَاق/إِكْرَام —
`wasl_qat_cells_shared`)؛ الفرقُ في موضعين: **الحدّ** (الوصلُ يسقط في الوصل والقطعُ يبقى) و**بقيّةُ الرسم**
(`WASL`/`WASL_SILENT` في شهادة البوّابة؛ `A116.Boundary`: لا ابتداءَ بساكن، وهمزةُ الوصل تسقط ولا تُقبل
بعد ساكن). المبرهَن هنا على الحدّ:
* لا ابتداءَ بساكن (`no_initial_sukun`)، وهمزةُ الوصل تُرخِّص الساكن (`wasl_licenses`).
* في الوصل تسقط: ما قبلها متحرّكًا يتّصل بالساكن (`wasl_drops`: وَ + نْطَلَقَ)، وما قبلها ساكنًا لا يُرخَّص
  (`wasl_after_sukun`: كسرةُ التقاء الساكنين قانونُ `Context` في الغانم).
* القطعُ يبقى بعد الساكن والمتحرّك (`qat_stays`: وَأَكْرَمَ) — وهذا هو «الاختبارُ الإملائيّ السريع».

والحصرُ الصرفيُّ (أين تقع كلٌّ منهما) **تقسيمٌ لقوالب `Wazn.awzan`** المبدوءة بهمزة: `waslTemplates` (أمرُ
الثلاثيّ، وماضي الخماسيّ والسداسيّ ومصدراهما) و`qatTemplates` (الرباعيُّ ومصدرُه وأَفْعَل والجموع)؛ متباينان
ويغطّيان كلَّ قالبٍ مبدوءٍ بهمزة (`templates_partition`). القارئُ `kind` يقرأ الوصلَ والقطعَ من القالب، والقطعَ
الأصليَّ من الجذر (أَخَذَ، أَرْض: `radicalHamza`)، وما سواه لا يقرؤه؛ ومضارعُ المتكلّم أَكْتُبُ يقرؤه قطعًا من
قالب أَفْعُل (خانةٌ مشتركةٌ مع جمع القلّة، والحكمُ واحد).
الأسماءُ العشرةُ مودَعة (`tenNouns`) وجمعُها قطعٌ على أَفْعَال (`plural_qat`). الحذفُ الإملائيّ (بِسْمِ،
ابن بين علمين، آل، أَسْتَخْرَجْتَ) عمليّاتُ حدٍّ مشهودة (`bism_witness`، `istifham_al_witness`).
-/

namespace Slge.Wasl

open Slge.Categories (c)
open Slge.Wazn (Sym)

/-! ## الحدّ -/

theorem no_initial_sukun (k : Fin 29) (w : List SCell) : licensed (⟨k, 3⟩ :: w) = false := by
  simp [licensed, SCell.isSukun, Ishara.s3]

/-- همزةُ الوصل تُرخِّص الابتداءَ بالساكن. -/
theorem wasl_licenses (v : Fin 4) (hv : v.val ≠ 3) (w : List SCell) (hw : noAdj w = true) :
    licensed (⟨⟨0, by decide⟩, v⟩ :: w) = true := by
  cases w with
  | nil => simp [licensed, SCell.isSukun, noAdj, hv]
  | cons x t => simp [licensed, SCell.isSukun, noAdj, hv, hw]

/-- في الوصل تسقط الهمزةُ ويتّصل الساكنُ بما قبله متحرّكًا. -/
theorem wasl_drops (prev w : List SCell) (hp : licensed prev = true) (hne : prev ≠ [])
    (hw : noAdj w = true) (hlast : ∀ x, prev.getLast? = some x → x.isSukun = false) :
    licensed (prev ++ w) = true :=
  Damair.attach_licensed prev w hp hw hne (fun x _ hx _ => by rw [hlast x hx]; rfl)

/-- وبعد ساكنٍ لا تُقبل: ساكنان — كسرةُ التقاء الساكنين قانونُ الحدّ في الغانم. -/
theorem wasl_after_sukun (prev : List SCell) (m : SCell) (hm : m.isSukun = true)
    (k : Fin 29) (t : List SCell) : licensed (prev ++ [m] ++ ⟨k, 3⟩ :: t) = false := by
  have h3 : m.state.val = 3 := by simpa [SCell.isSukun] using hm
  have key : ∀ l : List SCell, noAdj (l ++ [m] ++ ⟨k, 3⟩ :: t) = false := by
    intro l
    induction l with
    | nil => simp [noAdj, SCell.isSukun, h3, Ishara.s3]
    | cons x u ih =>
      cases u with
      | nil => simp [noAdj, SCell.isSukun, h3, Ishara.s3]
      | cons y v =>
        simp only [List.cons_append, noAdj, Bool.and_eq_false_iff]
        exact Or.inr (by simpa using ih)
  cases prev with
  | nil => simp [licensed, noAdj, SCell.isSukun, h3, Ishara.s3]
  | cons x u =>
    simp only [List.cons_append, List.append_assoc, licensed, Bool.and_eq_false_iff]
    exact Or.inr (by simpa using key (x :: u))

/-- القطعُ يبقى: همزةٌ متحرّكةٌ بعد أيّ آخر. -/
theorem qat_stays (prev w : List SCell) (v : Fin 4) (hv : v.val ≠ 3) (hp : licensed prev = true)
    (hne : prev ≠ []) (hw : licensed (⟨⟨0, by decide⟩, v⟩ :: w) = true) :
    licensed (prev ++ ⟨⟨0, by decide⟩, v⟩ :: w) = true := by
  have hn : noAdj (⟨⟨0, by decide⟩, v⟩ :: w) = true := by
    simp only [licensed, Bool.and_eq_true] at hw; exact hw.2
  exact Damair.attach_licensed prev _ hp hn hne
    (fun x y _ hy => by
      simp only [List.head?_cons, Option.some.injEq] at hy
      rw [← hy]; simp [SCell.isSukun, hv])

/-- الاختبارُ السريع بشهادتي البوّابة: وَانْطَلَقَ (الهمزةُ ساقطة) ووَأَكْرَمَ (باقية). -/
def intalaqa : List SCell := [c 0 1, c 25 3, c 16 0, c 23 0, c 21 0]   -- اِنْطَلَقَ
def akrama : List SCell := [c 0 0, c 22 3, c 10 0, c 24 0]              -- أَكْرَمَ

theorem quick_test :
    [c 27 0] ++ intalaqa.tail = [c 27 0, c 25 3, c 16 0, c 23 0, c 21 0] ∧   -- وَانْطَلَقَ (بوّابة)
    licensed ([c 27 0] ++ intalaqa.tail) = true ∧
    licensed ([c 27 0] ++ akrama) = true ∧
    licensed intalaqa.tail = false ∧ licensed intalaqa = true := by decide

/-- الخانةُ واحدة: اِنْطِلَاق وإِكْرَام همزةٌ مكسورةٌ فساكن. -/
def intilaq : List SCell := [c 0 1, c 25 3, c 16 1, c 23 0, c 1 3, c 21 2]
def ikram : List SCell := [c 0 1, c 22 3, c 10 0, c 1 3, c 24 2]

theorem wasl_qat_cells_shared :
    intilaq.head? = ikram.head? ∧ (intilaq.getD 1 (c 0 0)).state = (ikram.getD 1 (c 0 0)).state := by
  decide

/-! ## الحصرُ الصرفيّ: تقسيمُ القوالب -/

/-- أمرُ الثلاثيّ (8–10)، ماضي الخماسيّ والسداسيّ (16–19)، ومصادرُهما (44–47). -/
def waslTemplates : List Nat := [8, 9, 10, 16, 17, 18, 19, 44, 45, 46, 47]
/-- الرباعيُّ أَفْعَلَ ومصدرُه إِفْعَال، وأَفْعَل، والجموعُ أَفْعُل/أَفْعَال/أَفْعِلَة/أَفْعِلَاء، وأَفَاعِل/أَفَاعِيل. -/
def qatTemplates : List Nat := [11, 38, 54, 83, 84, 85, 100, 105, 106]

def startsHamza : Wazn.Template → Bool
  | .lit x :: _ => x.carrier.val == 0
  | _ => false

/-- القوالبُ المبدوءةُ بهمزة في `awzan` هي بالضبط الوصلُ والقطعُ المودَعان، ولا قالبَ في الصنفين معًا. -/
def hamzaTemplates : List Nat :=
  (List.range Wazn.awzan.length).filter (fun k => startsHamza (Sarf.templ k))

theorem templates_partition :
    (waslTemplates.filter (· ∈ qatTemplates)) = [] ∧
    hamzaTemplates.all (fun k => k ∈ waslTemplates || k ∈ qatTemplates) = true ∧
    (waslTemplates ++ qatTemplates).all (· ∈ hamzaTemplates) = true ∧
    hamzaTemplates.length = waslTemplates.length + qatTemplates.length := by decide

theorem templates_wf :
    (waslTemplates ++ qatTemplates).all (fun k => decide (Wazn.WF (Sarf.templ k))) = true := by decide

/-! ## الأسماءُ العشرة -/

def tenNouns : List (String × List SCell) := [
  ("اِسْم", [c 0 1, c 12 3, c 24 2]), ("اِبْن", [c 0 1, c 2 3, c 25 2]),
  ("اِبْنَة", [c 0 1, c 2 3, c 25 0, c 3 2]), ("اِمْرُؤ", [c 0 1, c 24 3, c 10 2, c 0 2]),
  ("اِمْرَأَة", [c 0 1, c 24 3, c 10 0, c 0 0, c 3 2]), ("اِثْنَان", [c 0 1, c 4 3, c 25 0, c 1 3, c 25 1]),
  ("اِثْنَتَان", [c 0 1, c 4 3, c 25 0, c 3 0, c 1 3, c 25 1]), ("اِبْنُم", [c 0 1, c 2 3, c 25 2, c 24 2]),
  ("اَيْم", [c 0 0, c 28 3, c 24 2]), ("اَيْمُن", [c 0 0, c 28 3, c 24 2, c 25 2])
]

theorem ten_licensed : tenNouns.all (fun p => licensed p.2) = true := by decide
theorem ten_count : tenNouns.length = 10 := by decide

/-- كلُّها همزةٌ متحرّكةٌ فساكن: شكلُ الوصل. -/
theorem ten_shape : tenNouns.all (fun p => match p.2 with
    | h :: s :: _ => h.carrier.val == 0 && h.state.val != 3 && s.state.val == 3
    | _ => false) = true := by decide


inductive Kind where
  | wasl | qat | qatRadical | unread
  deriving DecidableEq, Repr

/-- الألفُ لا تكون أصلًا: قالبٌ يستخرج ألفًا في موضع أصلٍ مردود (إِلَّا على اِفْعَلْ بجذر ل‑ل‑ا). -/
def noAlifRoot (t : Wazn.Template) (w : List SCell) : Bool :=
  !([0, 1, 2] : List (Fin 3)).any (fun i => Wazn.rootOf t w i == some ⟨1, by decide⟩)

/-- على القالب بآخرٍ مفتوحٍ أو مضمومٍ أو كما هو (الفعلُ والاسمُ)، بلا ألفٍ أصلًا. -/
def onT (k : Nat) (w : List SCell) : Bool :=
  let t := Sarf.templ k
  (Sarf.onTemplate t w || Sarf.onTemplate t (Zuruf.setLast w 2) ||
    Sarf.onTemplate t (Zuruf.setLast w 0)) && noAlifRoot t w

/-- الهمزةُ أصلٌ في موضع الفاء: على قالبٍ لا همزةَ في صدره وجذرُه يبدأ بهمزة. -/
def radicalHamza (w : List SCell) : Bool :=
  (List.range Wazn.awzan.length).any (fun k =>
    !startsHamza (Sarf.templ k) && onT k w &&
      (Wazn.rootOf (Sarf.templ k) w 0 == some ⟨0, by decide⟩))

/-- القارئ: وصلٌ أو قطعٌ من القالب، أو قطعٌ أصليٌّ من الجذر، أو لا يُقرأ. -/
def kind (w : List SCell) : Kind :=
  if tenNouns.any (fun p => p.2 == w || p.2 == Zuruf.setLast w 2) then .wasl   -- السماعيّ أوّلًا
  else if waslTemplates.any (fun k => onT k w) then .wasl
  else if qatTemplates.any (fun k => onT k w) then .qat
  else if radicalHamza w then .qatRadical
  else .unread

/-- إِلَّا على اِفْعَلْ بجذر ل‑ل‑ا: القالبُ يقبلها والألفُ الأصلُ تردّها — فلا تُقرأ وصلًا. -/
theorem illa_not_wasl : kind Mansubat.illa = .unread := by decide

/-- شواهد: اِقْرَأْ (بوّابة)، اِنْطَلَقَ، اِسْتَخْرَجَ، اِنْطِلَاق وصلٌ؛ أَكْرَمَ، إِكْرَام، أَبْنَاءَ (بوّابة) قطعٌ؛
أَخَذَ (بوّابة) وأَرْض قطعٌ أصليّ؛ أَكْتُبُ قطعٌ — لكن من قالب أَفْعُل (أَنْفُس) لا من المضارعة: الخانةُ لا تفرّق
مضارعَ المتكلّم من جمع القلّة، والحكمُ (قطع) واحد. -/
theorem kind_witnesses :
    kind [c 0 1, c 21 3, c 10 0, c 0 3] = .wasl ∧ kind intalaqa = .wasl ∧
    kind [c 0 1, c 12 3, c 3 0, c 7 3, c 10 0, c 5 0] = .wasl ∧ kind intilaq = .wasl ∧
    kind akrama = .qat ∧ kind ikram = .qat ∧ kind [c 0 0, c 2 3, c 25 0, c 1 3, c 0 0] = .qat ∧
    kind [c 0 0, c 7 0, c 9 0] = .qatRadical ∧ kind [c 0 0, c 10 3, c 15 2] = .qatRadical ∧
    kind [c 0 0, c 22 3, c 3 2, c 2 2] = .qat := by decide

/-- القالبُ يقرأ الوصلَ من القطع حيث الخانةُ لا تقرؤه: اِنْطِلَاق وإِكْرَام. -/
theorem template_reads_what_cells_cannot : kind intilaq ≠ kind ikram := by decide

/-! ## جمعُ الاسم والابن -/

/-- جمعُهما قطعٌ: أَسْمَاء وأَبْنَاء على أَفْعَال؛ والمفردان وصلٌ بالسماع (الجدول قبل القالب). -/
theorem plural_qat :
    kind [c 0 0, c 12 3, c 24 0, c 1 3, c 0 2] = .qat ∧ kind [c 0 0, c 2 3, c 25 0, c 1 3, c 0 2] = .qat ∧
    kind [c 0 1, c 12 3, c 24 2] = .wasl ∧ kind [c 0 1, c 2 3, c 25 0] = .wasl := by decide

/-! ## الحذفُ الإملائيّ عمليّاتُ حدّ -/

/-- بِسْمِ: الحرفُ المتّصل + الجذعُ بعد إسقاط الهمزة، مجرورًا — بشهادة البوّابة بلا بقيّة. -/
theorem bism_witness :
    [c 2 1] ++ Majrurat.jarr (tenNouns.getD 0 ("", [])).2.tail = [c 2 1, c 12 3, c 24 1] := by decide

/-- همزةُ الاستفهام على أل: آل = ءَ اْ + ما بعد همزة الوصل؛ وعلى فعلٍ بهمزة وصل: تسقط (أَسْتَخْرَجْتَ). -/
def istifhamAl (w : List SCell) : List SCell := c 0 0 :: c 1 3 :: (Marifa.al w).tail
def istifhamVerb (w : List SCell) : List SCell := c 0 0 :: w.tail

theorem istifham_al_witness :
    istifhamAl [c 0 0, c 1 3, c 25 0] = [c 0 0, c 1 3, c 23 3, c 0 0, c 1 3, c 25 0] ∧   -- آلْآنَ (بوّابة)
    licensed (istifhamAl [c 0 0, c 1 3, c 25 0]) = false ∧      -- مدٌّ فساكن: الثلاثيُّ يرخّصها كحَاجَّ
    istifhamVerb [c 0 1, c 12 3, c 3 0, c 7 3, c 10 0, c 5 3, c 3 0] =
      [c 0 0, c 12 3, c 3 0, c 7 3, c 10 0, c 5 3, c 3 0] ∧
    licensed (istifhamVerb [c 0 1, c 12 3, c 3 0, c 7 3, c 10 0, c 5 3, c 3 0]) = true := by decide

theorem istifhamVerb_licensed (w : List SCell) (hw : licensed w = true) :
    licensed (istifhamVerb w) = true := by
  unfold istifhamVerb
  cases w with
  | nil => rfl
  | cons y t =>
    simp only [List.tail_cons]
    simp only [licensed, Bool.and_eq_true] at hw
    cases t with
    | nil => rfl
    | cons z u =>
      simp only [noAdj, Bool.and_eq_true] at hw
      show (!(c 0 0).isSukun && noAdj (c 0 0 :: z :: u)) = true
      have h2 := hw.2.2
      simp [noAdj, c, SCell.isSukun, h2]

end Slge.Wasl
