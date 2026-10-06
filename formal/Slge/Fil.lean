import Slge.Ism
import Slge.Shabaka

/-!
# الفعل: أبوابُه أزواجُ حالات، وزيادتُه طولُ قالب، وإعلالُه وإبدالُه عمليّاتٌ على الخانات

* **الأبوابُ الستّة** أزواجُ (حالةِ عين الماضي، حالةِ عين المضارع) من تسعةٍ ممكنة (`abwab`، `abwab_six`)؛
  قوالبُها سليمةٌ (`bab_wf`)، وصورُها مرخَّصةٌ لكلّ جذر (`bab_licensed`)، وتُقرأ من الخانتين (`bab_read`).
  شرطُ بابِ فَتَحَ–يَفْتَحُ (حلقيّةُ العين أو اللام) يقرؤه `halqi` (`bab3_condition`). الثلاثةُ الساقطةُ
  (كسرٌ–ضمّ، ضمٌّ–فتح، ضمٌّ–كسر) ثقلٌ معلَن.
* **المزيد**: أحرفُ الزيادة = طولُ القالب − 3 (`added`)؛ التسعةُ في `Wazn.awzan` تنقسم كما في الحصر:
  ثلاثةٌ بحرف، خمسةٌ بحرفين، واحدٌ بثلاثة (`mazid_counts`). لا فعلَ خماسيَّ الأصول: جذرُ `Wazn` ثلاثيٌّ
  بالبناء (`Root = Fin 3 → Fin 29`)؛ والرباعيُّ (فَعْلَلَ، تَفَعْلَلَ، اِفْعَلَلَّ) أشكالُ حالاتٍ مودَعة (`rubai_shapes`).
  معاني الصيغ (التعدية، المشاركة، المطاوعة…) معلَنة.
* **الإعلالُ ثلاثُ عمليّات**: القلبُ (`qalb`: و/ي متحرّكةٌ بعد فتحٍ ⇒ ألفٌ ساكنة؛ قَوَلَ ← قَالَ)، والنقلُ
  (`naql`: حركةُ المعتلّ إلى الساكن قبله؛ يَقْوُلُ ← يَقُولُ)، والحذفُ (`Jazm.hollow_forced`: السكونُ بعد
  مدٍّ غيرُ مرخَّصٍ فيُحذف؛ يَقُولُ ← يَقُلْ) — تحفظ الترخيصَ أو تُلزمه (`qalb_licensed`، `naql_licensed`).
  الردُّ مبرهَنٌ في الغانم (`A116.Ilal.*_restore`).
* **الإبدالُ ثلاثُ قواعد** على اِفْتَعَلَ: تاءٌ ⇒ طاءٌ بعد الإطباق، تاءٌ ⇒ دالٌ بعد د/ذ/ز، وفاءٌ واويّةٌ أو
  يائيّةٌ ⇒ تاءٌ تُدغَم (`ibdal`)؛ لا يغيّر نمطَ السكون فيحفظ الترخيص (`ibdal_licensed`)؛ شواهدُ البوّابة
  اصْطَفَى وازْدَادُوا، واِتَّصَلَ مودَع.
النواسخُ في `Nawasikh` (هذا الحصرُ يعدّ كاد أحدَ عشرَ بلا هَبَّ: `kada_eleven`).
القياسُ على MASAQ (أفعالُ المصحف بشهادات البوّابة) في بايثون.
-/

namespace Slge.Fil

open Slge.Categories (c)
open Slge.Wazn (Sym)

/-! ## الأبواب -/

def pastT (ayn : Fin 4) : Wazn.Template := [.slot 0 0, .slot 1 ayn, .slot 2 0]
def presT (ayn : Fin 4) : Wazn.Template := [.lit (c 28 0), .slot 0 3, .slot 1 ayn, .slot 2 2]

/-- (عينُ الماضي، عينُ المضارع): فتحٌ–ضمّ، فتحٌ–كسر، فتحان، كسرٌ–فتح، ضمّان، كسرتان. -/
def abwab : List (Fin 4 × Fin 4) := [(0, 2), (0, 1), (0, 0), (1, 0), (2, 2), (1, 1)]

def nine : List (Fin 4 × Fin 4) :=
  ([0, 1, 2] : List (Fin 4)).flatMap (fun p => ([0, 1, 2] : List (Fin 4)).map (fun q => (p, q)))

theorem abwab_six : abwab.length = 6 ∧ abwab.Nodup ∧ abwab.all (· ∈ nine) = true ∧
    (nine.filter (· ∉ abwab)) = [(1, 2), (2, 0), (2, 1)] := by decide

theorem bab_wf : abwab.all (fun p => decide (Wazn.WF (pastT p.1)) && decide (Wazn.WF (presT p.2))) = true := by
  decide

theorem bab_licensed (r : Wazn.Root) (p q : Fin 4) (hq : q.val ≠ 3) :
    licensed (Wazn.fill (pastT p) r) = true ∧ licensed (Wazn.fill (presT q) r) = true := by
  constructor <;> simp [Wazn.fill, pastT, presT, Wazn.fillSym, licensed, noAdj, SCell.isSukun, c, hq]

/-- القراءة: عينُ الماضي خانتُه الثانية، وعينُ المضارع خانتُه الثالثة. -/
def readBab (past pres : List SCell) : Option (Fin 4 × Fin 4) :=
  match past, pres with
  | [_, a, _], [_, _, b, _] => some (a.state, b.state)
  | _, _ => none

theorem bab_read (r : Wazn.Root) (p q : Fin 4) :
    readBab (Wazn.fill (pastT p) r) (Wazn.fill (presT q) r) = some (p, q) := by
  simp [Wazn.fill, pastT, presT, Wazn.fillSym, readBab]

/-- حروفُ الحلق: ء ه ع ح غ خ. -/
def halqi (k : Fin 29) : Bool := k.val == 0 || k.val == 26 || k.val == 18 || k.val == 6 ||
  k.val == 19 || k.val == 7

/-- شرطُ باب فَتَحَ–يَفْتَحُ: العينُ أو اللامُ حلقيّة. -/
def bab3Condition (r : Wazn.Root) : Bool := halqi (r 1) || halqi (r 2)

/-- شواهدُ البوّابة: ضَرَبَ–يَضْرِبُ، فَتَحَ–يَفْتَحُ (ح حلقيّة)، فَرِحَ–يَفْرَحُ؛ ويَنْصُرُ وحَسِبَ. -/
theorem bab_witnesses :
    readBab [c 15 0, c 10 0, c 2 0] [c 28 0, c 15 3, c 10 1, c 2 2] = some (0, 1) ∧
    readBab [c 20 0, c 3 0, c 6 0] [c 28 0, c 20 3, c 3 0, c 6 2] = some (0, 0) ∧
    readBab [c 20 0, c 10 1, c 6 0] [c 28 0, c 20 3, c 10 0, c 6 2] = some (1, 0) ∧
    bab3Condition (fun i => if i = 0 then 20 else if i = 1 then 3 else 6) = true ∧
    bab3Condition (fun i => if i = 0 then 15 else if i = 1 then 10 else 2) = false := by decide

theorem bab3_condition_witness :
    Wazn.fill (pastT 0) (fun i => if i = 0 then 20 else if i = 1 then 3 else 6) = [c 20 0, c 3 0, c 6 0] := by
  decide

/-! ## المزيد -/

/-- أحرفُ الزيادة = طولُ القالب − 3. -/
def added (t : Wazn.Template) : Nat := t.length - 3

/-- التسعةُ: أَفْعَلَ فَعَّلَ فَاعَلَ | اِنْفَعَلَ اِفْتَعَلَ اِفْعَلَّ تَفَعَّلَ تَفَاعَلَ | اِسْتَفْعَلَ. -/
def mazid : List Nat := [11, 12, 13, 16, 17, 18, 14, 15, 19]

theorem mazid_counts :
    (mazid.map (fun k => added (Sarf.templ k))) = [1, 1, 1, 2, 2, 2, 2, 2, 3] ∧
    mazid.all (fun k => decide (Wazn.WF (Sarf.templ k))) = true ∧
    ([0, 1, 2].map (fun k => added (Sarf.templ k))) = [0, 0, 0] := by decide

/-! ## أمرُ المزيد (دَينٌ سُدِّد) -/

def startsSukun : Wazn.Template → Bool
  | .slot _ s :: _ => s.val == 3
  | .lit x :: _ => x.state.val == 3
  | [] => false

/-- أمرُ المضارع: حذفُ حرف المضارعة وتسكينُ الآخر؛ وما بدأ بساكنٍ سبقته همزةُ وصلٍ مكسورة. -/
def amrOf (pres : Wazn.Template) : Wazn.Template :=
  let body := Shabaka.del 0 (Shabaka.setSt (pres.length - 1) 3 pres)
  if startsSukun body then .lit (c 0 1) :: body else body

def mazidPres : List Nat := [21, 22, 23, 24, 25, 26, 28]
def mazidAmr : List Nat := [114, 115, 116, 117, 118, 119, 120]

/-- أمرُ المزيد من مضارعه بالقاعدة نفسِها التي تُخرج أمرَ المجرّد (`Shabaka.edges` 8–10): سبعةٌ بالقاعدة
وحدَها؛ ويُفْعِلُ بالقاعدة يُعطي اِفْعِلْ (أمرَ المجرّد بعينه) — فهمزةُ القطع المفتوحةُ في أَفْعِلْ هي ما يفرّق
الرباعيَّ من الثلاثيّ: قطعٌ لا وصل (`Wasl.qatTemplates`)، والخانةُ تحمل الفرق. -/
theorem amr_of_pres :
    (mazidPres.zip mazidAmr).all (fun p => amrOf (Sarf.templ p.1) == Sarf.templ p.2) = true ∧
    amrOf (Sarf.templ 20) = Sarf.templ 9 ∧
    Sarf.templ 113 = Shabaka.setSt 0 0 (amrOf (Sarf.templ 20)) ∧
    amrOf (Sarf.templ 4) = Sarf.templ 8 ∧ amrOf (Sarf.templ 5) = Sarf.templ 9 ∧
    (113 ∈ Wasl.qatTemplates) ∧ ([118, 119, 120].all (· ∈ Wasl.waslTemplates)) = true ∧
    (mazidAmr.all (fun k => decide (Wazn.WF (Sarf.templ k)))) = true ∧
    (mazidAmr.map (fun k => added (Sarf.templ k))) = [1, 1, 2, 2, 2, 2, 3] := by decide

/-- أمرُ اِفْعَلَّ بالقاعدة اِفْعَلْلْ: ساكنان، غيرُ مرخَّصٍ ثنائيًّا (كجزمه) — فكُّ الإدغام أو الفتحُ
بقيّةٌ مسمّاة. -/
theorem amr_ifalla_unlicensed : licensed (Wazn.mizan (amrOf (Sarf.templ 27))) = false := by decide

/-- المجرّدُ الرباعيُّ ومزيدُه: أشكالُ حالاتٍ (الجذرُ في `Wazn` ثلاثيٌّ بالبناء). -/
def rubai : List (String × List SCell) := [
  ("دَحْرَجَ", [c 8 0, c 6 3, c 10 0, c 5 0]), ("زَلْزَلَ", [c 11 0, c 23 3, c 11 0, c 23 0]),
  ("تَدَحْرَجَ", [c 3 0, c 8 0, c 6 3, c 10 0, c 5 0]),
  ("اِطْمَأَنَّ", [c 0 1, c 16 3, c 24 0, c 0 0, c 25 3, c 25 0])
]

theorem rubai_shapes :
    rubai.all (fun p => licensed p.2) = true ∧
    Ism.shape (rubai.getD 0 ("", [])).2 = Ism.shape (rubai.getD 1 ("", [])).2 ∧
    (rubai.getD 3 ("", [])).2 = [c 0 1, c 16 3, c 24 0, c 0 0, c 25 3, c 25 0] := by decide

/-- جذرُ `Wazn` ثلاثيٌّ بالبناء: لا خماسيَّ الأصول. -/
theorem root_is_ternary : Wazn.Root = (Fin 3 → Fin 29) := rfl

/-! ## الإعلال: ثلاثُ عمليّات -/

/-- القلب: و/ي متحرّكةٌ بعد فتحٍ ⇒ ألفٌ ساكنة. -/
def qalb : List SCell → List SCell
  | x :: y :: t =>
      if x.state.val = 0 ∧ (y.carrier.val = 27 ∨ y.carrier.val = 28) ∧ y.state.val ≠ 3 then
        x :: c 1 3 :: t
      else x :: y :: t
  | w => w

/-- النقل: حركةُ المعتلّ إلى الساكن قبله. -/
def naql : List SCell → List SCell
  | x :: y :: t =>
      if x.state.val = 3 ∧ (y.carrier.val = 27 ∨ y.carrier.val = 28) ∧ y.state.val ≠ 3 then
        ⟨x.carrier, y.state⟩ :: ⟨y.carrier, 3⟩ :: t
      else x :: y :: t
  | w => w

theorem qalb_witness : qalb [c 21 0, c 27 0, c 23 0] = [c 21 0, c 1 3, c 23 0] := by decide   -- قَوَلَ ← قَالَ

theorem naql_witness :
    naql [c 21 3, c 27 2, c 23 2] = [c 21 2, c 27 3, c 23 2] ∧                               -- قْوُلُ ← قُولُ
    c 28 0 :: naql [c 21 3, c 27 2, c 23 2] = [c 28 0, c 21 2, c 27 3, c 23 2] := by decide   -- يَقُولُ (بوّابة)

/-- القلبُ يحفظ الترخيص إذا كان ما بعد الألف متحرّكًا. -/
theorem qalb_licensed (x y z : SCell) (t : List SCell) (hz : z.isSukun = false)
    (h : licensed (x :: y :: z :: t) = true) : licensed (qalb (x :: y :: z :: t)) = true := by
  have h' := h
  simp only [licensed, noAdj, Bool.and_eq_true] at h'
  have hx : x.isSukun = false := by simpa using h'.1
  have hzt : noAdj (z :: t) = true := h'.2.2.2
  show licensed (if x.state.val = 0 ∧ (y.carrier.val = 27 ∨ y.carrier.val = 28) ∧ y.state.val ≠ 3
      then x :: c 1 3 :: z :: t else x :: y :: z :: t) = true
  have hx' : x.state.val ≠ 3 := by simpa [SCell.isSukun] using hx
  have hz' : z.state.val ≠ 3 := by simpa [SCell.isSukun] using hz
  split
  · simp [licensed, noAdj, hx', hz', hzt, SCell.isSukun, c, Ishara.s3]
  · exact h

/-- النقلُ يحفظ الترخيص بعد حرفٍ متحرّك: المعتلُّ كان متحرّكًا فلا يجتمع ساكنان. -/
theorem naql_licensed (w x y z : SCell) (t : List SCell) (hw : w.isSukun = false)
    (hz : z.isSukun = false) (hn : noAdj (x :: y :: z :: t) = true) :
    licensed (w :: naql (x :: y :: z :: t)) = true := by
  have hn' := hn
  simp only [noAdj, Bool.and_eq_true] at hn'
  have hzt : noAdj (z :: t) = true := hn'.2.2
  show licensed (w :: (if x.state.val = 3 ∧ (y.carrier.val = 27 ∨ y.carrier.val = 28) ∧ y.state.val ≠ 3
      then ⟨x.carrier, y.state⟩ :: ⟨y.carrier, 3⟩ :: z :: t else x :: y :: z :: t)) = true
  have hw' : w.state.val ≠ 3 := by simpa [SCell.isSukun] using hw
  have hz' : z.state.val ≠ 3 := by simpa [SCell.isSukun] using hz
  split
  · rename_i hc
    have hy : y.state.val ≠ 3 := hc.2.2
    simp [licensed, noAdj, hw', hz', hzt, SCell.isSukun, hy, Ishara.s3]
  · simp only [licensed, noAdj, Bool.and_eq_true]
    exact ⟨by simp [hw], by simp [hw], hn'.1, hn'.2.1, hzt⟩

/-- الحذفُ ملزَم: يَقُولُ مجزومًا — السكونُ بعد المدّ غيرُ مرخَّصٍ (`Jazm.hollow_forced`) فيُحذف. -/
theorem hadhf_witness : licensed (Jazm.sukun Jazm.yaqulu) = false ∧ licensed Jazm.yaqul = true :=
  ⟨Jazm.yaqulu_sukun_unlicensed, Jazm.yaqul_licensed⟩

/-! ## الإبدال على اِفْتَعَلَ -/

def itbaq (k : Fin 29) : Bool := k.val == 14 || k.val == 15 || k.val == 16 || k.val == 17
def dhz (k : Fin 29) : Bool := k.val == 8 || k.val == 9 || k.val == 11

/-- اِفْتَعَلَ من الجذر ثمّ الإبدال: تاءُ الافتعال في الخانة الثالثة، والفاءُ في الثانية. -/
def iftaal (r : Wazn.Root) : List SCell := Wazn.fill (Sarf.templ 17) r

def ibdal : List SCell → List SCell
  | h :: f :: t :: rest =>
      if itbaq f.carrier then h :: f :: ⟨⟨16, by decide⟩, t.state⟩ :: rest
      else if dhz f.carrier then h :: f :: ⟨⟨8, by decide⟩, t.state⟩ :: rest
      else if f.carrier.val = 27 ∨ f.carrier.val = 28 ∨ f.carrier.val = 0 then
        h :: ⟨⟨3, by decide⟩, f.state⟩ :: t :: rest
      else h :: f :: t :: rest
  | w => w

theorem ibdal_map_isSukun : ∀ w : List SCell, (ibdal w).map SCell.isSukun = w.map SCell.isSukun
  | h :: f :: t :: rest => by
    simp only [ibdal]
    split <;> (try split) <;> (try split) <;> simp [SCell.isSukun]
  | [] => rfl
  | [_] => rfl
  | [_, _] => rfl

theorem ibdal_licensed (w : List SCell) : licensed (ibdal w) = licensed w :=
  Zuruf.licensed_of_map_isSukun _ _ (ibdal_map_isSukun w)

/-- اِصْطَبَرَ، اِزْدَهَرَ، اِتَّصَلَ، اِتَّخَذَ (الهمزةُ فاءً كالواو والياء — دَينٌ سُدِّد)؛ وبشهادة البوّابة اصْطَفَى
وازْدَادُوا واتَّخَذَ (جذعُها بالقاعدة نفسِها). -/
theorem ibdal_witnesses :
    ibdal (iftaal (fun i => if i = 0 then 0 else if i = 1 then 7 else 9)) =
      [c 0 1, c 3 3, c 3 0, c 7 0, c 9 0] ∧
    ibdal (iftaal (fun i => if i = 0 then 14 else if i = 1 then 2 else 10)) =
      [c 0 1, c 14 3, c 16 0, c 2 0, c 10 0] ∧
    ibdal (iftaal (fun i => if i = 0 then 11 else if i = 1 then 26 else 10)) =
      [c 0 1, c 11 3, c 8 0, c 26 0, c 10 0] ∧
    ibdal (iftaal (fun i => if i = 0 then 27 else if i = 1 then 14 else 23)) =
      [c 0 1, c 3 3, c 3 0, c 14 0, c 23 0] ∧
    (ibdal [c 0 1, c 14 3, c 3 0, c 20 0, c 1 3]) = [c 0 1, c 14 3, c 16 0, c 20 0, c 1 3] ∧
    (ibdal [c 0 1, c 11 3, c 3 0, c 1 3, c 8 2, c 27 3]).take 3 = [c 0 1, c 11 3, c 8 0] := by decide

/-! ## ما بعد القالب: الأجوفُ والمضعَّف يُقرآن بالعمليّة (دَينٌ سُدِّد) -/

/-- الإدغام: عينٌ ولامٌ من حرفٍ واحدٍ متحرّكتان ⇒ العينُ ساكنة (رَدَدَ ← رَدَّ). -/
def idgham : List SCell → List SCell
  | x :: y :: z :: t =>
      if y.carrier = z.carrier ∧ y.state.val ≠ 3 ∧ z.state.val ≠ 3 then x :: ⟨y.carrier, 3⟩ :: z :: t
      else x :: y :: z :: t
  | w => w

/-- الإدغامُ يحفظ الترخيصَ إذا كان الأوّلُ متحرّكًا (ما قبل العين لا يكون ساكنًا في الماضي). -/
theorem idgham_licensed (x y z : SCell) (t : List SCell) (hx : x.isSukun = false)
    (h : licensed (x :: y :: z :: t) = true) : licensed (idgham (x :: y :: z :: t)) = true := by
  have h' := h
  simp only [licensed, noAdj, Bool.and_eq_true] at h'
  have hzt : noAdj (z :: t) = true := h'.2.2.2
  show licensed (if y.carrier = z.carrier ∧ y.state.val ≠ 3 ∧ z.state.val ≠ 3
      then x :: ⟨y.carrier, 3⟩ :: z :: t else x :: y :: z :: t) = true
  have hx' : x.state.val ≠ 3 := by simpa [SCell.isSukun] using hx
  split
  · rename_i hc
    simp [licensed, noAdj, hx', hc.2.2, hzt, SCell.isSukun, Ishara.s3]
  · exact h

/-- الأجوفُ على فَعَلَ بعد القلب: [ف، ا، ل] لكلّ جذرٍ عينُه واوٌ أو ياء. -/
theorem qalb_pastT (r : Wazn.Root) (h : (r 1).val = 27 ∨ (r 1).val = 28) :
    qalb (Wazn.fill (pastT 0) r) = [⟨r 0, 0⟩, c 1 3, ⟨r 2, 0⟩] := by
  simp [Wazn.fill, pastT, Wazn.fillSym, qalb, h]

/-- المضعَّفُ على فَعَلَ بعد الإدغام: [ف، عْ، ع] لكلّ جذرٍ عينُه لامُه. -/
theorem idgham_pastT (r : Wazn.Root) (h : r 1 = r 2) :
    idgham (Wazn.fill (pastT 0) r) = [⟨r 0, 0⟩, ⟨r 1, 3⟩, ⟨r 2, 0⟩] := by
  simp [Wazn.fill, pastT, Wazn.fillSym, idgham, h]

/-- القارئان: الأجوفُ يُقرأ جذرًا بعينٍ مجهولةٍ بين الواو والياء (المعجمُ يفصل)، والمضعَّفُ جذرًا تامًّا. -/
def readHollow : List SCell → Option (Fin 29 × Fin 29)
  | [x, m, z] => if m = c 1 3 ∧ x.state.val = 0 ∧ z.state.val = 0 then some (x.carrier, z.carrier) else none
  | _ => none

def readDoubled : List SCell → Option Wazn.Root
  | [x, y, z] => if y.carrier = z.carrier ∧ y.state.val = 3 ∧ x.state.val = 0 ∧ z.state.val = 0 then
      some (fun i => if i = 0 then x.carrier else y.carrier) else none
  | _ => none

/-- قَالَ وجَاءَ يُقرآن أجوفين (ق‑؟‑ل، ج‑؟‑ء)؛ رَدَّ ومَدَّ مضعَّفين، وما قُرئ يُردّ بالعمليّة بعينه. -/
theorem readers_witnesses :
    readHollow [c 21 0, c 1 3, c 23 0] = some (21, 23) ∧
    readHollow [c 5 0, c 1 3, c 0 0] = some (5, 0) ∧
    (readDoubled [c 10 0, c 8 3, c 8 0]).map (fun r => idgham (Wazn.fill (pastT 0) r)) =
      some [c 10 0, c 8 3, c 8 0] ∧
    readHollow [c 25 0, c 14 0, c 10 0] = none ∧ readDoubled [c 25 0, c 14 0, c 10 0] = none := by
  decide

/-- هذا الحصرُ يعدّ كاد أحدَ عشرَ (بلا هَبَّ): العشرةُ المشتركةُ في `Nawasikh.kadaSisters`. -/
theorem kada_eleven :
    (["كَادَ", "كَرَبَ", "أَوْشَكَ", "عَسَى", "حَرَى", "اخْلَوْلَقَ", "أَنْشَأَ", "طَفِقَ", "جَعَلَ", "أَخَذَ", "بَدَأَ"].all
      (fun n => Nawasikh.kadaSisters.any (·.1 == n))) = true ∧ Nawasikh.kadaSisters.length = 12 := by
  decide

end Slge.Fil
