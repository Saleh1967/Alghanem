import Slge.Mansubat

/-!
# المجرورات: ثلاثةُ أبوابٍ وثلاثُ علامات — الجرُّ عمليّةٌ واحدة على الخانة، وسببُه في الحدّ

الحصرُ يعدّ الأبوابَ بسبب الجرّ (الحرف، الإضافة، التبعيّة) ويحصر العلاماتِ في ثلاث. على الخانات:
* **الجرُّ عمليّةٌ واحدة** `jarr = setLast · 1` (الكسرةُ الأصل)، وللنكرة `tanwin ∘ jarr`؛ تُقرأ جرًّا لكلّ
  جذعٍ آخرُه غيرُ نون (`caseClass_jarr`)، ومنوَّنةً لكلّ جذع (`caseClass_jarr_tanwin`)، وتحفظ الترخيص
  (`jarr_licensed`)؛ وجدولُ أدوات الربط يحكم عليها بالعمل (`govern_jarr`).
* **الياءُ** علامةٌ فرعيّة: جمعُ المذكّر السالم `Adad.uqud _ false` (`uqud_jarr_compatible`)، والمثنّى
  `dual` (`dual_jarr_compatible`) — كلاهما نصبٌ أو جرّ: الخانةُ لا تفصلهما؛ والأسماءُ الخمسة
  `Khamsa.form _ .jarr` لا يقرؤها القارئُ العامّ (الياءُ بعد كسرٍ مشتركةٌ مع المنقوص: `khamsa_jarr_unread`).
* **الفتحةُ** للممنوع من الصرف: `Sarf.mamnuJarr` تُقرأ نصبًا (`mamnu_jarr_reads_nasb`) — الجرُّ من جدول
  العلل لا من الآخر؛ وبأل أو بالإضافة كسرٌ (`Sarf.al_jarr_kasra`، `Sarf.idafa_jarr_kasra`).

**السببُ في الحدّ**: حروفُ الجرّ مودَعةٌ مرخَّصة (`harfs_licensed`)، والمتّصلةُ منها (بِ لِ كَ وَ تَ) حروفٌ
متحرّكةٌ لا تُفسد ما بعدها (`proclitic_jarr_licensed`)؛ والإضافةُ `Marifa.idafa` تُسقط التنوينَ
(`mudaf_no_tanwin`) وتُسقط نونَ الجمع والمثنّى (`mudaf_drops_nun`)؛ والإضافةُ اللفظيّةُ يقرؤها القالب
(`lafziyya_by_template`: صَانِع على فَاعِل)؛ والتبعيّةُ توافقٌ في الحالة (`tabi_jarr_follows`).
معاني الإضافة (اللام، مِنْ، فِي) والتعريفُ بها وتخصيصُ رُبَّ بالنكرات والتاءِ بلفظ الجلالة: معلَن/تيار.
القياسُ على MASAQ (18,184 مجرورًا ومضافًا بشهادات البوّابة) في بايثون.
-/

namespace Slge.Majrurat

open Slge.Categories (c)
open Slge.Zuruf (setLast)
open Slge.Nawasikh (tanwin)
open Slge.Tawabi (caseClass)

/-! ## العمليّةُ الواحدة -/

def jarr (w : List SCell) : List SCell := setLast w 1

theorem jarr_licensed (w : List SCell) (hw : licensed w = true)
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) : licensed (jarr w) = true := by
  unfold jarr; rw [Zuruf.setLast_licensed w 1 (by decide) hlast]; exact hw

/-- الكسرةُ تُقرأ جرًّا إن لم يكن الآخرُ نونًا (ِينَ قانونُها قانونُ العقود) ولم يكن تاءً بعد ألف
(جمعُ المؤنّث: نصبٌ أو جرّ). -/
theorem caseClass_jarr (w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25 ∧ x.carrier.val ≠ 3) :
    caseClass (jarr w) = .jarr := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 1 hne
  obtain ⟨x, hx⟩ := Nawasikh.exists_lastOf w hne
  have h1 : Afal.lastOf (setLast w 1) = some ⟨k, 1⟩ := by
    rw [hi]; exact Zaman.lastOf_append_singleton i _
  have h2 := Nawasikh.lastOf_setLast_carrier w 1 x hx
  rw [h1] at h2
  have hk' : k.val ≠ 25 ∧ k.val ≠ 3 := by
    have : k = x.carrier := by
      have := congrArg (fun o => (o.map SCell.carrier)) h2
      simpa using this
    rw [this]; exact hk x hx
  unfold jarr; rw [hi]; unfold caseClass
  rw [List.reverse_append, List.reverse_singleton, List.singleton_append]
  cases i.reverse with
  | nil => simp
  | cons g u => cases u with
    | nil => simp [hk'.1, hk'.2]
    | cons p v => simp [hk'.1, hk'.2]

/-- النكرةُ المجرورة: كسرٌ فتنوين — جرٌّ (أو نصبٌ/جرٌّ في جمع المؤنّث) لكلّ جذع. -/
theorem caseClass_jarr_tanwin (w : List SCell) (hne : w ≠ []) :
    Tawabi.compatible (caseClass (tanwin (jarr w))) .jarr = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 1 hne
  unfold tanwin jarr; rw [hi]; unfold caseClass
  simp only [List.append_assoc, List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.cons_append]
  cases i.reverse with
  | nil => simp [c, Ishara.v25, Ishara.s3, Tawabi.compatible]
  | cons g u => simp [c, Ishara.v25, Ishara.s3]; split <;> rfl

theorem govern_jarr (w : List SCell) (hne : w ≠ []) : Rawabit.govern .jarr (jarr w) = true := by
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast w 1 hne
  unfold Rawabit.govern Rawabit.lastState jarr; rw [hk]; rfl

/-! ## الياءُ والفتحة -/

theorem uqud_jarr_compatible (stem : List SCell) (hne : stem ≠ []) :
    Tawabi.compatible (caseClass (Adad.uqud stem false)) .jarr = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append stem 1 hne
  unfold Adad.uqud; simp only [Bool.false_eq_true, ite_false]; rw [hi, List.append_assoc]
  exact (congrArg (fun x => Tawabi.compatible x .jarr) (Nawasikh.caseClass_of_last_yin i k)).trans rfl

/-- المثنّى مجرورًا: فتحٌ فياءٌ ساكنةٌ فنونٌ مكسورة. -/
def dual (w : List SCell) : List SCell := setLast w 0 ++ [⟨⟨28, by decide⟩, 3⟩, c 25 1]

theorem caseClass_of_last_ayn (i : List SCell) (k : Fin 29) :
    caseClass (i ++ [⟨k, 0⟩, ⟨⟨28, by decide⟩, 3⟩, c 25 1]) = .nasbJarr := by
  unfold caseClass
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.cons_append]
  simp [c, Ishara.v25, Ishara.s3]

theorem dual_jarr_compatible (stem : List SCell) (hne : stem ≠ []) :
    Tawabi.compatible (caseClass (dual stem)) .jarr = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append stem 0 hne
  unfold dual; rw [hi, List.append_assoc]
  exact (congrArg (fun x => Tawabi.compatible x .jarr) (caseClass_of_last_ayn i k)).trans rfl

/-- الأسماءُ الخمسة بالياء: الياءُ بعد كسرٍ مشتركةٌ مع المنقوص — المعجمُ يفصل. -/
theorem khamsa_jarr_unread (s : Khamsa.Stem) (hne : s.head ≠ []) :
    caseClass (Khamsa.form s .jarr) = .unread := by
  unfold caseClass Khamsa.form Khamsa.maddOf Khamsa.shortOf
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.cons_append]
  cases hh : s.head.reverse with
  | nil => exact absurd (List.reverse_eq_nil_iff.1 hh) hne
  | cons p t => simp [Ishara.s3]

/-- الممنوعُ من الصرف: فتحٌ يُقرأ نصبًا؛ الجرُّ من جدول العلل. -/
theorem mamnu_jarr_reads_nasb (w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25) :
    caseClass (Sarf.mamnuJarr w) = .nasb := Nawasikh.caseClass_nasb w hne hk

theorem masajid_witness :
    caseClass [c 24 0, c 12 0, c 1 3, c 5 1, c 8 0] = .nasb ∧
    Sarf.illa [c 24 0, c 12 0, c 1 3, c 5 1, c 8 0] = .muntahaJumu ∧
    Marifa.al (jarr [c 24 0, c 12 0, c 1 3, c 5 1, c 8 0]) =
      [c 0 0, c 23 3, c 24 0, c 12 0, c 1 3, c 5 1, c 8 1] := by decide        -- الْمَسَاجِدِ

/-! ## السببُ في الحدّ: الحرف -/

/-- حروفُ الجرّ المودَعة (17 من العشرين المعلَنة)؛ الخمسةُ الأُول متّصلة. -/
def harfs : List (String × List SCell) := [
  ("بِ", [c 2 1]), ("لِ", [c 23 1]), ("كَ", [c 22 0]), ("وَ", [c 27 0]), ("تَ", [c 3 0]),
  ("مِنْ", [c 24 1, c 25 3]), ("إِلَى", [c 0 1, c 23 0, c 1 3]), ("عَنْ", [c 18 0, c 25 3]),
  ("عَلَى", [c 18 0, c 23 0, c 1 3]), ("فِي", [c 20 1, c 28 3]), ("حَتَّى", [c 6 0, c 3 3, c 3 0, c 1 3]),
  ("مُذْ", [c 24 2, c 9 3]), ("مُنْذُ", [c 24 2, c 25 3, c 9 2]), ("خَلَا", Mansubat.khala),
  ("عَدَا", Mansubat.ada), ("حَاشَا", Mansubat.hasha), ("رُبَّ", [c 10 2, c 2 3, c 2 0])
]

theorem harfs_licensed : harfs.all (fun p => licensed p.2) = true := by decide
theorem harfs_count : harfs.length = 17 := by decide

/-- المتّصلةُ الخمسةُ لا تُفسد ما بعدها. -/
theorem proclitic_jarr_licensed (w : List SCell) (hw : licensed w = true) :
    (harfs.take 5).all (fun p => licensed (p.2 ++ w)) = true := by
  simp only [harfs, List.take, List.all_cons, List.all_nil, Bool.and_true, Bool.and_eq_true,
    List.singleton_append]
  exact ⟨Rawabit.proclitic_keeps_licence _ 1 (by decide) w hw,
    Rawabit.proclitic_keeps_licence _ 1 (by decide) w hw,
    Rawabit.proclitic_keeps_licence _ 0 (by decide) w hw,
    Rawabit.proclitic_keeps_licence _ 0 (by decide) w hw,
    Rawabit.proclitic_keeps_licence _ 0 (by decide) w hw⟩

/-- تسعةٌ منها في جدول أدوات الربط جارّةً. -/
theorem harfs_in_rawabit :
    ["بِ", "لِ", "كَ", "مِنْ", "إِلَى", "عَنْ", "عَلَى", "حَتَّى"].all
      (fun n => Rawabit.particles.any (fun p => p.name == n && p.amal == .jarr)) = true := by decide

/-- تَاللَّهِ ووَاللَّهِ: شاهدا بوّابة؛ التاءُ مختصّةٌ بلفظ الجلالة (معلَن). وتَاللَّهِ (مدٌّ قبل لامٍ
مشدّدة: ساكنان) خارج الترخيص الثنائيّ كحَاجَّ — يرخّصها الثلاثيُّ في الغانم؛ ووَاللَّهِ ثنائيّةُ الترخيص. -/
theorem qasam_witness :
    licensed [c 3 0, c 1 3, c 23 3, c 23 0, c 26 1] = false ∧
    licensed [c 27 0, c 23 3, c 23 0, c 26 1] = true := by decide

/-- رُبَّ تجرّ النكرات: النكرةُ المجرورةُ تحمل التنوين لكلّ جذع. -/
theorem rubba_nakira (w : List SCell) (hne : w ≠ []) :
    Nida.hasTanwin (tanwin (jarr w)) = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 1 hne
  unfold tanwin jarr; rw [hi]; unfold Nida.hasTanwin
  simp only [List.append_assoc, List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.cons_append]
  simp [c, Ishara.v25, Ishara.s3]

/-! ## السببُ في الحدّ: الإضافة -/

/-- المضافُ لا تنوينَ له (قانونُ حسم المضاف): إسقاطُ التنوين عمليّةٌ قبل الإلحاق. -/
theorem mudaf_no_tanwin (w : List SCell) (hw : Nida.hasTanwin w = true) :
    Nida.hasTanwin (Marifa.dropTanwin w) = false ∨ Afal.initOf w = [] := by
  unfold Marifa.dropTanwin; rw [hw]; simp only [ite_true]
  by_cases h : Afal.initOf w = []
  · exact Or.inr h
  · left
    -- بعد إسقاط النون يبقى الآخرُ متحرّكًا (حركةُ التنوين) فلا نونَ ساكنةً بعده
    unfold Nida.hasTanwin at hw ⊢
    cases hr : w.reverse with
    | nil => rw [hr] at hw; simp at hw
    | cons n t =>
      cases t with
      | nil => rw [hr] at hw; simp at hw
      | cons v u =>
        rw [hr] at hw
        simp only [Bool.and_eq_true, beq_iff_eq, bne_iff_ne, ne_eq] at hw
        have hw' : w = (v :: u).reverse ++ [n] := by
          have := congrArg List.reverse hr; simpa using this
        rw [hw', Zaman.initOf_append_singleton, List.reverse_reverse]
        cases u with
        | nil => rfl
        | cons p q => simp [hw.2]

/-- المضافُ من الجمع السالم والمثنّى: تسقط النون (`initOf`)، ويبقى المدُّ آخرًا. -/
def mudafUqud (stem : List SCell) (raf : Bool) : List SCell := Afal.initOf (Adad.uqud stem raf)
def mudafDual (stem : List SCell) : List SCell := Afal.initOf (dual stem)

theorem mudaf_drops_nun (stem : List SCell) (r : Bool) :
    mudafUqud stem r = setLast stem (if r then 2 else 1) ++
      [⟨if r then ⟨27, by decide⟩ else ⟨28, by decide⟩, 3⟩] ∧
    mudafDual stem = setLast stem 0 ++ [⟨⟨28, by decide⟩, 3⟩] := by
  constructor
  · unfold mudafUqud Adad.uqud
    rw [show (setLast stem (if r then 2 else 1) ++
        [⟨if r then ⟨27, by decide⟩ else ⟨28, by decide⟩, 3⟩, c 25 0]) =
        (setLast stem (if r then 2 else 1) ++ [⟨if r then ⟨27, by decide⟩ else ⟨28, by decide⟩, 3⟩])
          ++ [c 25 0] by simp]
    exact Zaman.initOf_append_singleton _ _
  · unfold mudafDual dual
    rw [show (setLast stem 0 ++ [⟨⟨28, by decide⟩, 3⟩, c 25 1]) =
        (setLast stem 0 ++ [⟨⟨28, by decide⟩, 3⟩]) ++ [c 25 1] by simp]
    exact Zaman.initOf_append_singleton _ _

/-- مُهَنْدِسُو الشَّرِكَةِ: شاهدُ الحصر عمليّةً. -/
theorem muhandisu_witness :
    mudafUqud [c 24 2, c 26 0, c 25 3, c 8 1, c 12 2] true =
      [c 24 2, c 26 0, c 25 3, c 8 1, c 12 2, c 27 3] := by decide

/-- الإضافةُ اللفظيّة: المضافُ مشتقٌّ على قالبٍ (صَانِعُ الْمَعْرُوفِ)؛ والمعنويّة: المضافُ جامد
(كِتَابُ مُحَمَّدٍ). القالبُ يقرأ الفرق. -/
theorem lafziyya_by_template :
    Mansubat.derived [c 14 0, c 1 3, c 25 1, c 18 2] = true ∧      -- صَانِعُ
    Mansubat.derived [c 22 1, c 3 0, c 1 3, c 2 2] = false ∧        -- كِتَابُ
    licensed (Marifa.idafa [c 22 1, c 3 0, c 1 3, c 2 2]
      (tanwin (jarr [c 24 2, c 6 0, c 24 3, c 24 0, c 8 2]))) = true := by decide  -- كِتَابُ مُحَمَّدٍ

/-- المضافُ إلى معرفةٍ معرفةٌ (الإضافةُ المحضة): المضافُ إلى ضميرٍ في `Marifa`. -/
theorem mudaf_marifa (w : List SCell) : Marifa.Marifa (Marifa.idafa w [c 26 2]) :=
  .mudafToPronoun w [c 26 2] (by decide)

/-! ## السببُ في الحدّ: التبعيّة -/

theorem tabi_jarr_follows (x y : List SCell) (hx : x ≠ []) (hy : y ≠ [])
    (kx : ∀ z, Afal.lastOf x = some z → z.carrier.val ≠ 25 ∧ z.carrier.val ≠ 3)
    (ky : ∀ z, Afal.lastOf y = some z → z.carrier.val ≠ 25 ∧ z.carrier.val ≠ 3) :
    Tawabi.follows (jarr x) (jarr y) = true := by
  unfold Tawabi.follows; rw [caseClass_jarr x hx kx, caseClass_jarr y hy ky]; rfl

/-- المفردُ المختومُ بألفٍ ونونٍ مجرورًا (إِيمَانِ، شَيْطَانِ) والمثنّى المرفوعُ (رَجُلَانِ): خانةٌ واحدة — القارئُ
يقرؤها رفعًا بالقانون العامّ، والفصلُ للمعجم (الألفُ أصلٌ أم علامة). -/
theorem an_kasra_shared :
    caseClass [c 0 1, c 28 3, c 24 0, c 1 3, c 25 1] = .raf ∧                    -- إِيمَانِ
    caseClass [c 10 0, c 5 2, c 23 0, c 1 3, c 25 1] = .raf := by decide          -- رَجُلَانِ

/-- بِرَجُلٍ صَالِحٍ: نكرتان مجرورتان منوَّنتان تتبع إحداهما الأخرى. -/
theorem rajul_salih :
    Tawabi.follows (tanwin (jarr [c 10 0, c 5 2, c 23 2])) (tanwin (jarr [c 14 0, c 1 3, c 23 1, c 6 2])) =
      true := by decide

end Slge.Majrurat
