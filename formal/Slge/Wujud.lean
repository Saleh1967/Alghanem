import Slge.WujudTable
import Slge.Kulli
import Slge.Talil
import Slge.Maqayis

/-!
# الجهةُ الوجوديّة للقوالب: المصدرُ والمشتقُّ والجامدُ تقسيمًا مغلقًا على الـ125

كلُّ قالبٍ على صنفٍ واحدٍ من ستّة (`Ont`، من بابه المودَع — معلَن): فعلٌ، مصدرٌ، وصفٌ مشتقّ، اسمٌ مشتقٌّ غيرُ وصف
(زمانٌ ومكانٌ وآلة)، صيغةُ جمع، واسمٌ (مصدرٌ أو جامدٌ لا تفصله الخانة: الجمودُ قيدٌ معجميٌّ لا وزن). المبرهَن على الجدول:

* **المطابقةُ مع القوائم القائمة**: الفعلُ هو الماضي والمضارعُ والأمر بقوائمها (`fil_eq`)، والمصدرُ قوالبُ `Kulli.masdarTemplates`
  بعينها (`masdar_eq`)، والوصفُ داخل قوالب الوصف في `Mansubat` ولا يفضل منها إلّا فُعَلَاءُ جمعًا (`wasf_derived`).
* **الإغلاقُ المنطقيّ**: كلُّ فعلٍ له صيغةٌ على ميزانه ولا صيغةَ لمصدرٍ (`fil_sigha_mizan`، `masdar_no_sigha_mizan`؛ ولكلّ
  الجذور: `Jiha.sigha_of_fill`، `Kulli.masdar_no_sigha`)؛ وكلُّ وصفٍ مشتقٌّ على ميزانه (`wasf_derived_mizan`).
* **الإغلاقُ الأنطولوجيّ**: أصلُ الشبكة مصدرٌ (`root_masdar`)، وكلُّ قالبٍ ينحدر منه (`Talil.root_causes_all`)، ولا شيءَ ينحدر
  من اسمٍ ولا من صيغة جمع (`ism_jam_leaves`): الاسمُ والجمعُ طرفان لا أصلان — هذا معنى «الجامدُ لا يُشتقّ منه».
* **المطابقةُ مع القارئ**: `Kulli.kulli` يقرأ على الميزان الجهةَ المودَعة في 111 من 125، والمخالفُ 14 بأرقامها
  (`kulli_agreement`): اشتراكٌ في الصورة (أَفْعَلُ/أَفْعُلُ مضارعُ المتكلّم؛ فِعْلَة جمعًا وهيئة؛ فِعَال وفُعُول جمعًا ومصدرًا؛
  مُفَاعَلَة ومِفْعَال وفَعَّالَة بصورة المشتقّ؛ فُعَلَاء) أو ما لا يقرؤه (المقصور). والزمانُ والمكانُ والآلةُ يقرؤها الكليُّ
  «جامدًا» لأنّه لا صنفَ له لها — باسمه.
* **القراءة**: جهةُ القراءة من قوالبها (`ontOfReading`)، والقراءاتُ تُرتَّب بجهةٍ مطلوبة ولا تسقط (`mem_rank`، `length_rank`).
-/

namespace Slge.Wujud

open Slge.Categories (c)

def ontOf (k : Nat) : Ont := table.getD k .ism

theorem table_length_N : table.length = Wazn.N := by rfl

def ofClass (o : Ont) : List Nat := (List.range Wazn.N).filter (fun k => ontOf k == o)

set_option maxRecDepth 100000 in
theorem class_counts :
    (ofClass .fil).length = 37 ∧ (ofClass .masdar).length = 22 ∧ (ofClass .wasf).length = 25 ∧
    (ofClass .zarfAla).length = 7 ∧ (ofClass .jam).length = 30 ∧ (ofClass .ism).length = 4 := by decide

/-! ## المطابقةُ مع القوائم القائمة -/

set_option maxRecDepth 100000 in
theorem fil_eq :
    (ofClass .fil).all (fun k => (Jiha.pastTemplates ++ Jiha.presentTemplates ++ Jiha.amrTemplates).contains k) ∧
    (Jiha.pastTemplates ++ Jiha.presentTemplates ++ Jiha.amrTemplates).all (fun k => ontOf k == .fil) := by decide

set_option maxRecDepth 100000 in
theorem masdar_eq :
    (ofClass .masdar).all (fun k => Kulli.masdarTemplates.contains k) ∧
    Kulli.masdarTemplates.all (fun k => ontOf k == .masdar) := by decide

set_option maxRecDepth 100000 in
/-- الوصفُ داخل قوالب الوصف، ولا يفضل منها إلّا فُعَلَاءُ (99): جمعُ فَعِيل صيغةُ جمعٍ لا وصف. -/
theorem wasf_derived :
    (ofClass .wasf).all (fun k => Mansubat.derivedTemplates.contains k) = true ∧
    Mansubat.derivedTemplates.filter (fun k => ontOf k != .wasf) = [99] := by decide

/-! ## الإغلاقُ المنطقيّ على الميزان -/

set_option maxRecDepth 100000 in
/-- كلُّ فعلٍ له صيغةٌ على ميزانه (ماضٍ أو مضارعٌ أو أمر)؛ ولكلّ الجذور: `Jiha.sigha_of_fill`. -/
theorem fil_sigha_mizan : (ofClass .fil).all (fun k => (Jiha.sigha (Wazn.mizan (Sarf.templ k))).isSome) = true := by
  decide

set_option maxRecDepth 100000 in
/-- لا صيغةَ لمصدرٍ على ميزانه؛ ولكلّ الجذور: `Kulli.masdar_no_sigha`. -/
theorem masdar_no_sigha_mizan :
    (ofClass .masdar).all (fun k => (Jiha.sigha (Wazn.mizan (Sarf.templ k))).isNone) = true := by decide

set_option maxRecDepth 100000 in
/-- كلُّ وصفٍ مشتقٌّ على ميزانه (بالضمّ في آخره كما أُودع) — إلّا المقصورَين فَعْلَى وفُعْلَى (81، 82) فلا ضمَّ في
آخرهما ولا يقرؤهما `derivedBare`: باسمهما. -/
theorem wasf_derived_mizan :
    (ofClass .wasf).filter (fun k => !Mansubat.derivedBare (Wazn.mizan (Sarf.templ k))) = [81, 82] := by decide

/-! ## الإغلاقُ الأنطولوجيّ على الشبكة -/

theorem root_masdar : ontOf Shabaka.root = .masdar := by decide

set_option maxRecDepth 100000 in
/-- لا قالبَ ينحدر من اسمٍ ولا من صيغة جمع: الاسمُ والجمعُ طرفان في الشبكة لا أصلان. -/
theorem ism_jam_leaves :
    ((List.range Wazn.N).filter (fun k => ontOf k == .ism || ontOf k == .jam)).all (fun k =>
      (List.range Wazn.N).all (fun q => !Talil.derives q k)) = true := by decide

set_option maxRecDepth 100000 in
/-- كلُّ وصفٍ وكلُّ زمانٍ ومكانٍ وآلةٍ أبوه في الشبكة فعلٌ أو مشتقٌّ (ولا يكون اسمًا ولا جمعًا)، وبالتعدّي يبلغ
المصدرَ الأصل (`Talil.root_causes_all`). -/
theorem mushtaqq_from_fil_or_mushtaqq :
    ((List.range Wazn.N).filter (fun k => ontOf k == .wasf || ontOf k == .zarfAla)).all (fun k =>
      match Shabaka.parentOf k with
      | some p => ontOf p == .fil || ontOf p == .wasf || ontOf p == .zarfAla
      | none => false) = true := by decide

/-! ## المطابقةُ مع القارئ -/

/-- جهةُ القارئ التي تقابل الصنفَ المودَع. -/
def kindOf : Ont → Kulli.Kind
  | .fil => .fil | .masdar => .hadath | .wasf => .aradi | .zarfAla => .jamid | .jam => .jamid | .ism => .jamid

set_option maxRecDepth 100000 in
/-- الكليُّ يقرأ الجهةَ المودَعة على الميزان إلّا 14 قالبًا بأرقامها. -/
theorem kulli_agreement :
    (List.range Wazn.N).filter (fun k => Kulli.kulli (Wazn.mizan (Sarf.templ k)) != kindOf (ontOf k)) =
      [40, 54, 60, 62, 81, 82, 83, 86, 93, 94, 99, 108, 109, 110] := by decide

/-! ## القراءة -/

/-- جهةُ القراءة: الفعلُ إن كان فيها قالبُ فعل، وإلّا جهةُ قالبها الأوّل. -/
def ontOfReading (rd : Jidh.Reading) : Ont :=
  if rd.templates.any (fun k => ontOf k == .fil) then .fil
  else match rd.templates.head? with
    | some k => ontOf k
    | none => .ism

def rank (o : Ont) (rs : List Jidh.Reading) : List Jidh.Reading :=
  rs.filter (fun rd => ontOfReading rd == o) ++ rs.filter (fun rd => ontOfReading rd != o)

theorem mem_rank (o : Ont) (rs : List Jidh.Reading) (rd : Jidh.Reading) : rd ∈ rank o rs ↔ rd ∈ rs := by
  simp only [rank, List.mem_append, List.mem_filter, bne_iff_ne, ne_eq, beq_iff_eq]
  constructor
  · rintro (⟨h, _⟩ | ⟨h, _⟩) <;> exact h
  · intro h
    by_cases hf : ontOfReading rd = o
    · exact Or.inl ⟨h, by simpa using hf⟩
    · exact Or.inr ⟨h, by simpa using hf⟩

theorem length_rank (o : Ont) : ∀ rs : List Jidh.Reading, (rank o rs).length = rs.length
  | [] => rfl
  | rd :: rs => by
    have ih := length_rank o rs
    simp only [rank, List.length_append] at ih ⊢
    by_cases hf : ontOfReading rd = o <;> simp [hf] <;> omega

set_option maxRecDepth 100000 in
/-- فَرِيقٌ: اسمٌ (فَعِيل وصفٌ، وفِعْل اسم)؛ كَذَّبُو: فعلٌ؛ قَالَ: فعل. -/
theorem witnesses :
    (Jidh.jidh Jidh.fariqun).map ontOfReading = [.wasf, .ism] ∧
    (Jidh.jidh Jidh.kadhdhabu).map ontOfReading = [.fil, .fil, .fil, .fil, .fil, .fil] ∧
    (Jidh.jidh Ilal.qala).map ontOfReading = [.fil, .fil] := by decide +kernel

end Slge.Wujud
