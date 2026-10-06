import Slge.Tawabi

/-!
# النواسخ: أربعةُ أبوابٍ عمليّتان

الحصرُ أربعةُ أبوابٍ (كان، كاد، إنّ، ظنّ)؛ وعلى الخانات **عمليّتان لا غير**: `raf` (ضمٌّ في الآخر)
و`nasb` (فتحٌ في الآخر). فكان = (رفع، نصب)، وإنّ **عكسُها** (`inna_eq_swap_kana`)، وكاد عملُ كان
بعينه (`kada_eq_kana`)، وظنّ نصبان (`zanna_both_nasb`)، ولا النافيةُ للجنس عملُ إنّ (`laJins_eq_inna`).

المبرهَن على العمليّتين:
* الترخيص: `raf_licensed`، `nasb_licensed` (الحركةُ لا تُدخل ساكنًا).
* القراءة (د١٦): `caseClass_raf` — ما رُفع يُقرأ رفعًا لكلّ جذعٍ غيرِ فارغ؛ `caseClass_nasb` — ما نُصب يُقرأ
  نصبًا إن لم يكن آخرُه نونًا (ُونَ/ِينَ قانونُهما قانونُ العقود: `uqud_nasb_compatible`)؛ `caseClass_nasb_tanwin`
  للنكرة؛ `caseClass_al_raf` للمعرَّف.
* التنوينُ عمليّةٌ ثالثةٌ منفصلة: الحركةُ وحدَها لا تنوينَ معها (`raf_no_tanwin`، `nasb_no_tanwin`) —
  ومنه اسمُ لا النافية للجنس: فتحٌ بلا تنوين ولا أداة (`laJins_ism_no_tanwin`).
* **الكفّ**: `kaffa` تُلحق «مَا» (`kaffa_licensed`)؛ والصورُ الستّ المودَعةُ هي العمليّةُ على الستّة
  (`kaffa_forms`)؛ وجدولُ أدوات الربط يسجّل إِنَّ ناصبةً للاسم وإِنَّمَا بلا عمل (`innama_kaffa_in_rawabit`).
* **خبرُ كاد مضارع**: صورةٌ من `Afal.form` مرفوعة (`kada_khabar_raf`)، وبأَنْ منصوبة (`an_khabar_nasb`).

الجامدُ والمتصرّف، والتمامُ، وشرطُ النفي قبل زال وأخواتها، والتعليقُ والإلغاء: قوانينُ تيارٍ ومعجمٍ لا خانة.
الشواهدُ الموسومةُ `gate` بشهادات البوّابة؛ والباقي مودَعٌ على طريقتها. القياسُ على MASAQ في بايثون.
-/

namespace Slge.Nawasikh

open Slge.Categories (c)
open Slge.Zuruf (setLast)
open Slge.Tawabi (caseClass CaseClass)

/-! ## العمليّتان -/

def raf (w : List SCell) : List SCell := setLast w 2
def nasb (w : List SCell) : List SCell := setLast w 0
/-- التنوين: نونٌ ساكنةٌ بعد الحركة — عمليّةٌ منفصلة. -/
def tanwin (w : List SCell) : List SCell := w ++ [c 25 3]

/-- عملُ الناسخ: (ما يصنعه بالاسم، ما يصنعه بالخبر). -/
abbrev Amal := (List SCell → List SCell) × (List SCell → List SCell)

def kana : Amal := (raf, nasb)
def kada : Amal := (raf, nasb)
def inna : Amal := (nasb, raf)
def laJins : Amal := (nasb, raf)
def zanna : Amal := (nasb, nasb)

theorem inna_eq_swap_kana : inna = Prod.swap kana := rfl
theorem kada_eq_kana : kada = kana := rfl
theorem laJins_eq_inna : laJins = inna := rfl
theorem zanna_both_nasb : zanna.1 = zanna.2 ∧ zanna.2 = kana.2 := ⟨rfl, rfl⟩

/-! ## الترخيص -/

theorem raf_licensed (w : List SCell) (hw : licensed w = true)
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) : licensed (raf w) = true := by
  unfold raf; rw [Zuruf.setLast_licensed w 2 (by decide) hlast]; exact hw

theorem nasb_licensed (w : List SCell) (hw : licensed w = true)
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) : licensed (nasb w) = true := by
  unfold nasb; rw [Zuruf.setLast_licensed w 0 (by decide) hlast]; exact hw

/-! ## القراءة من الخانة الأخيرة -/

/-- تغييرُ الآخر تفكيكٌ: ما قبلَ الآخر ثمّ الآخرُ بحالته الجديدة. -/
theorem setLast_eq_append : ∀ (w : List SCell) (st : Fin 4), w ≠ [] →
    ∃ (i : List SCell) (k : Fin 29), setLast w st = i ++ [⟨k, st⟩]
  | [], _, h => absurd rfl h
  | [x], st, _ => ⟨[], x.carrier, rfl⟩
  | x :: y :: t, st, _ => by
    obtain ⟨i, k, hi⟩ := setLast_eq_append (y :: t) st (by simp)
    exact ⟨x :: i, k, by show x :: setLast (y :: t) st = _; rw [hi]; rfl⟩

/-- ما آخرُه مضمومٌ يُقرأ رفعًا، كائنًا ما كان ما قبله. -/
theorem caseClass_of_last_damm (i : List SCell) (k : Fin 29) : caseClass (i ++ [⟨k, 2⟩]) = .raf := by
  unfold caseClass
  rw [List.reverse_append, List.reverse_singleton, List.singleton_append]
  cases i.reverse with
  | nil => simp
  | cons g u => cases u with
    | nil => simp
    | cons p v => simp

theorem caseClass_raf (w : List SCell) (hne : w ≠ []) : caseClass (raf w) = .raf := by
  obtain ⟨i, k, hi⟩ := setLast_eq_append w 2 hne
  unfold raf; rw [hi]; exact caseClass_of_last_damm i k

theorem lastOf_setLast_carrier : ∀ (w : List SCell) (st : Fin 4) (x : SCell),
    Afal.lastOf w = some x → Afal.lastOf (setLast w st) = some ⟨x.carrier, st⟩
  | [], _, _, h => by simp [Afal.lastOf] at h
  | [y], st, x, h => by
    simp only [Afal.lastOf, Option.some.injEq] at h; subst h; rfl
  | y :: z :: u, st, x, h => by
    have ih := lastOf_setLast_carrier (z :: u) st x h
    show Afal.lastOf (y :: setLast (z :: u) st) = _
    cases hs : setLast (z :: u) st with
    | nil => rw [hs] at ih; simp [Afal.lastOf] at ih
    | cons a b => rw [hs] at ih; simpa [Afal.lastOf] using ih

theorem exists_lastOf : ∀ (w : List SCell), w ≠ [] → ∃ x, Afal.lastOf w = some x
  | [], h => absurd rfl h
  | [y], _ => ⟨y, rfl⟩
  | _ :: z :: u, _ => exists_lastOf (z :: u) (by simp)

theorem caseClass_nasb (w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25) : caseClass (nasb w) = .nasb := by
  obtain ⟨i, k, hi⟩ := setLast_eq_append w 0 hne
  obtain ⟨x, hx⟩ := exists_lastOf w hne
  have h1 : Afal.lastOf (setLast w 0) = some ⟨k, 0⟩ := by
    rw [hi]
    cases i with
    | nil => rfl
    | cons y t => exact Afal.lastOf_cons_append y t ⟨k, 0⟩ []
  have h2 := lastOf_setLast_carrier w 0 x hx
  rw [h1] at h2
  have hk' : k.val ≠ 25 := by
    have : k = x.carrier := by
      have := congrArg (fun o => (o.map SCell.carrier)) h2
      simpa using this
    rw [this]; exact hk x hx
  unfold nasb; rw [hi]; unfold caseClass
  rw [List.reverse_append, List.reverse_singleton, List.singleton_append]
  cases i.reverse with
  | nil => simp
  | cons g u => cases u with
    | nil => simp [hk']
    | cons p v => simp [hk']

/-- النكرةُ المنصوبة: فتحٌ فتنوين — تُقرأ نصبًا لكلّ جذع. -/
theorem caseClass_nasb_tanwin (w : List SCell) (hne : w ≠ []) :
    caseClass (tanwin (nasb w)) = .nasb := by
  obtain ⟨i, k, hi⟩ := setLast_eq_append w 0 hne
  unfold tanwin nasb; rw [hi]; unfold caseClass
  simp only [List.append_assoc, List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.cons_append]
  cases i.reverse with
  | nil => simp [c, Ishara.v25, Ishara.s3]
  | cons g u => simp [c, Ishara.v25, Ishara.s3]

theorem caseClass_raf_tanwin (w : List SCell) (hne : w ≠ []) :
    caseClass (tanwin (raf w)) = .raf := by
  obtain ⟨i, k, hi⟩ := setLast_eq_append w 2 hne
  unfold tanwin raf; rw [hi]; unfold caseClass
  simp only [List.append_assoc, List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.cons_append]
  cases i.reverse with
  | nil => simp [c, Ishara.v25, Ishara.s3]
  | cons g u => simp [c, Ishara.v25, Ishara.s3]

/-- المعرَّفُ بأل مرفوعًا يُقرأ رفعًا: الأداةُ في الصدر لا تمسّ الآخر. -/
theorem caseClass_al_raf (w : List SCell) (hne : w ≠ []) :
    caseClass (Marifa.al (raf w)) = .raf := by
  obtain ⟨i, k, hi⟩ := setLast_eq_append w 2 hne
  unfold raf; rw [hi]; unfold Marifa.al Marifa.shamsi
  cases i with
  | nil =>
    show caseClass (if _ then _ else _) = _
    split
    · exact caseClass_of_last_damm [c 0 0, ⟨k, (c 23 3).state⟩] k
    · exact caseClass_of_last_damm [c 0 0, c 23 3] k
  | cons y t =>
    show caseClass (if _ then _ else _) = _
    split
    · exact caseClass_of_last_damm (c 0 0 :: ⟨y.carrier, (c 23 3).state⟩ :: y :: t) k
    · exact caseClass_of_last_damm (c 0 0 :: c 23 3 :: y :: t) k

/-- ما آخرُه كسرٌ فياءٌ ساكنةٌ فنونٌ مفتوحة: نصبٌ أو جرّ. -/
theorem caseClass_of_last_yin (i : List SCell) (k : Fin 29) :
    caseClass (i ++ [⟨k, 1⟩, ⟨⟨28, by decide⟩, 3⟩, c 25 0]) = .nasbJarr := by
  unfold caseClass
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.cons_append]
  simp [c, Ishara.v25, Ishara.s3]

/-- ُونَ/ِينَ: خبرُ كان جمعًا سالمًا يوافق النصبَ (قانونُ العقود). -/
theorem uqud_nasb_compatible (stem : List SCell) (hne : stem ≠ []) :
    Tawabi.compatible (caseClass (Adad.uqud stem false)) .nasb = true := by
  obtain ⟨i, k, hi⟩ := setLast_eq_append stem 1 hne
  unfold Adad.uqud; simp only [Bool.false_eq_true, ite_false]; rw [hi, List.append_assoc]
  exact (congrArg (fun x => Tawabi.compatible x .nasb) (caseClass_of_last_yin i k)).trans rfl

/-! ## الحركةُ بلا تنوين -/

theorem no_tanwin_setLast (w : List SCell) (st : Fin 4) (hst : st.val ≠ 3) (hne : w ≠ []) :
    Nida.hasTanwin (setLast w st) = false := by
  obtain ⟨i, k, hi⟩ := setLast_eq_append w st hne
  rw [hi]; unfold Nida.hasTanwin
  rw [List.reverse_append, List.reverse_singleton, List.singleton_append]
  cases i.reverse with
  | nil => rfl
  | cons g u => simp [hst]

theorem raf_no_tanwin (w : List SCell) (hne : w ≠ []) : Nida.hasTanwin (raf w) = false :=
  no_tanwin_setLast w 2 (by decide) hne

theorem nasb_no_tanwin (w : List SCell) (hne : w ≠ []) : Nida.hasTanwin (nasb w) = false :=
  no_tanwin_setLast w 0 (by decide) hne

/-- الحركةُ في الآخر لا تُدخل الأداةَ في الصدر. -/
theorem hasAl_setLast (w : List SCell) (st : Fin 4) (hst : st.val ≠ 3)
    (hal : Marifa.hasAl w = false) : Marifa.hasAl (setLast w st) = false := by
  match w with
  | [] => rfl
  | [_] => rfl
  | [a, l] => simp [Marifa.hasAl, setLast, hst]
  | [a, l, x] => simpa [Marifa.hasAl, setLast] using hal
  | a :: l :: x :: y :: v =>
    show Marifa.hasAl (a :: l :: x :: setLast (y :: v) st) = false
    cases hs : setLast (y :: v) st with
    | nil => simpa [Marifa.hasAl] using hal
    | cons z u => simpa [Marifa.hasAl] using hal

/-- اسمُ لا النافية للجنس: فتحٌ بلا تنوينٍ ولا أداة (نكرةٌ)؛ والفتحُ يُقرأ نصبًا. -/
theorem laJins_ism_no_tanwin (w : List SCell) (hne : w ≠ []) (hal : Marifa.hasAl w = false)
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25) :
    Nida.hasTanwin (laJins.1 w) = false ∧ caseClass (laJins.1 w) = .nasb ∧
      Marifa.hasAl (laJins.1 w) = false :=
  ⟨nasb_no_tanwin w hne, caseClass_nasb w hne hk, hasAl_setLast w 0 (by decide) hal⟩

/-! ## المودَعات -/

/-- كان وأخواتها (13): الثمانيةُ بلا شرط، ثمّ الأربعةُ بشرط النفي (زَالَ، بَرِحَ، فَتِئَ، انْفَكَّ)، ثمّ دَامَ
بشرط «ما» المصدريّة — الشرطان قانونُ تيار. -/
def kanaSisters : List (String × List SCell) := [
  ("كَانَ", [c 22 0, c 1 3, c 25 0]), ("أَصْبَحَ", [c 0 0, c 14 3, c 2 0, c 6 0]),
  ("أَضْحَى", [c 0 0, c 15 3, c 6 0, c 1 3]), ("ظَلَّ", [c 17 0, c 23 3, c 23 0]),
  ("أَمْسَى", [c 0 0, c 24 3, c 12 0, c 1 3]), ("بَاتَ", [c 2 0, c 1 3, c 3 0]),
  ("صَارَ", [c 14 0, c 1 3, c 10 0]), ("لَيْسَ", [c 23 0, c 28 3, c 12 0]),
  ("زَالَ", [c 11 0, c 1 3, c 23 0]), ("بَرِحَ", [c 2 0, c 10 1, c 6 0]),
  ("فَتِئَ", [c 20 0, c 3 1, c 0 0]), ("انْفَكَّ", [c 0 1, c 25 3, c 20 0, c 22 3, c 22 0]),
  ("دَامَ", [c 8 0, c 1 3, c 24 0])
]

/-- كاد وأخواتها (11): المقاربة، الرجاء، الشروع. -/
def kadaSisters : List (String × List SCell) := [
  ("كَادَ", [c 22 0, c 1 3, c 8 0]), ("كَرَبَ", [c 22 0, c 10 0, c 2 0]),
  ("أَوْشَكَ", [c 0 0, c 27 3, c 13 0, c 22 0]), ("عَسَى", [c 18 0, c 12 0, c 1 3]),
  ("حَرَى", [c 6 0, c 10 0, c 1 3]), ("اخْلَوْلَقَ", [c 0 1, c 7 3, c 23 0, c 27 3, c 23 0, c 21 0]),
  ("أَنْشَأَ", [c 0 0, c 25 3, c 13 0, c 0 0]), ("طَفِقَ", [c 16 0, c 20 1, c 21 0]),
  ("جَعَلَ", [c 5 0, c 18 0, c 23 0]), ("هَبَّ", [c 26 0, c 2 3, c 2 0]),
  ("أَخَذَ", [c 0 0, c 7 0, c 9 0]), ("بَدَأَ", [c 2 0, c 8 0, c 0 0])
]

/-- إنّ وأخواتها (6) ولا النافيةُ للجنس ملحقةٌ بها. -/
def innaSisters : List (String × List SCell) := [
  ("إِنَّ", [c 0 1, c 25 3, c 25 0]), ("أَنَّ", [c 0 0, c 25 3, c 25 0]),
  ("كَأَنَّ", [c 22 0, c 0 0, c 25 3, c 25 0]), ("لَكِنَّ", [c 23 0, c 22 1, c 25 3, c 25 0]),
  ("لَيْتَ", [c 23 0, c 28 3, c 3 0]), ("لَعَلَّ", [c 23 0, c 18 0, c 23 3, c 23 0])
]

def la : List SCell := [c 23 0, c 1 3]

/-- ظنّ وأخواتها (16): الرجحان، اليقين، التحويل. -/
def zannaSisters : List (String × List SCell) := [
  ("ظَنَّ", [c 17 0, c 25 3, c 25 0]), ("حَسِبَ", [c 6 0, c 12 1, c 2 0]),
  ("خَالَ", [c 7 0, c 1 3, c 23 0]), ("زَعَمَ", [c 11 0, c 18 0, c 24 0]),
  ("جَعَلَ", [c 5 0, c 18 0, c 23 0]), ("رَأَى", [c 10 0, c 0 0, c 1 3]),
  ("عَلِمَ", [c 18 0, c 23 1, c 24 0]), ("وَجَدَ", [c 27 0, c 5 0, c 8 0]),
  ("دَرَى", [c 8 0, c 10 0, c 1 3]), ("أَلْفَى", [c 0 0, c 23 3, c 20 0, c 1 3]),
  ("صَيَّرَ", [c 14 0, c 28 3, c 28 0, c 10 0]), ("اتَّخَذَ", [c 0 1, c 3 3, c 3 0, c 7 0, c 9 0]),
  ("تَرَكَ", [c 3 0, c 10 0, c 22 0]), ("رَدَّ", [c 10 0, c 8 3, c 8 0]),
  ("وَهَبَ", [c 27 0, c 26 0, c 2 0])
]

theorem kana_licensed : kanaSisters.all (fun p => licensed p.2) = true := by decide
theorem kada_licensed : kadaSisters.all (fun p => licensed p.2) = true := by decide
theorem inna_licensed : (innaSisters.all (fun p => licensed p.2) && licensed la) = true := by decide
theorem zanna_licensed : zannaSisters.all (fun p => licensed p.2) = true := by decide

theorem counts : kanaSisters.length = 13 ∧ kadaSisters.length = 12 ∧ innaSisters.length = 6 ∧
    zannaSisters.length = 15 := by decide

/-- جَعَلَ في بابين: الخانةُ واحدةٌ والمعنى (الشروع/التحويل) يفصل. -/
theorem jaala_shared : (kadaSisters.map (·.2)).contains [c 5 0, c 18 0, c 23 0] = true ∧
    (zannaSisters.map (·.2)).contains [c 5 0, c 18 0, c 23 0] = true := by decide

/-- أربعةٌ من الستّة في جدول أدوات الربط بعملها `nasbIsm`؛ وكَأَنَّ ولَيْتَ ليستا فيه. -/
theorem inna_in_rawabit :
    ["إِنَّ", "أَنَّ", "لَكِنَّ", "لَعَلَّ"].all
      (fun n => Rawabit.particles.any (fun p => p.name == n && p.amal == .nasbIsm)) = true := by decide

/-- لَيْسَ ولَا ومَا في جدول أدوات الربط بلا عملٍ مسجَّل: عملُها عملُ كان قانونُ تيار. -/
theorem laysa_la_ma_in_rawabit :
    ["لَيْسَ", "لَا", "مَا"].all (fun n => Rawabit.particles.any (·.name == n)) = true := by decide

/-! ## الكفّ -/

/-- «مَا» الزائدةُ تُلحق بالحرف فتكفّه. -/
def kaffa (w : List SCell) : List SCell := w ++ [c 24 0, c 1 3]

theorem kaffa_licensed (w : List SCell) (hw : licensed w = true) (hne : w ≠ [])
    (hlast : ∀ x, w.getLast? = some x → x.isSukun = false) : licensed (kaffa w) = true := by
  unfold kaffa
  exact Damair.attach_licensed w [c 24 0, c 1 3] hw (by decide) hne
    (fun x y hx hy => by
      simp only [List.head?_cons, Option.some.injEq] at hy
      rw [← hy, hlast x hx]; rfl)

/-- الصورُ الستّ: إِنَّمَا، أَنَّمَا، كَأَنَّمَا، لَكِنَّمَا، لَيْتَمَا، لَعَلَّمَا. -/
def kaffaForms : List (List SCell) := [
  [c 0 1, c 25 3, c 25 0, c 24 0, c 1 3], [c 0 0, c 25 3, c 25 0, c 24 0, c 1 3],
  [c 22 0, c 0 0, c 25 3, c 25 0, c 24 0, c 1 3], [c 23 0, c 22 1, c 25 3, c 25 0, c 24 0, c 1 3],
  [c 23 0, c 28 3, c 3 0, c 24 0, c 1 3], [c 23 0, c 18 0, c 23 3, c 23 0, c 24 0, c 1 3]
]

theorem kaffa_forms : innaSisters.map (fun p => kaffa p.2) = kaffaForms := by decide
theorem kaffa_forms_licensed : kaffaForms.all licensed = true := by decide

/-- جدولُ أدوات الربط: إِنَّ تنصب الاسم، وإِنَّمَا بلا عمل — الكفُّ مسجَّلٌ في الجدول. -/
theorem innama_kaffa_in_rawabit :
    Rawabit.particles.any (fun p => p.name == "إِنَّ" && p.amal == .nasbIsm) = true ∧
    Rawabit.particles.any (fun p => p.name == "إِنَّمَا" && p.amal == .none) = true := by decide

/-- لَيْتَمَا يجوز فيها الإعمال: الكفُّ قرارُ تيارٍ لا خانة (الخانةُ واحدة). -/
theorem laytama_cells : kaffa (innaSisters.getD 4 ("", [])).2 = kaffaForms.getD 4 [] := rfl

/-! ## خبرُ كاد مضارع -/

/-- خبرُ كاد وأخواتها: مضارعٌ مرفوع (صورةٌ من الأفعال الخمسة). -/
def kadaKhabar (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) : List SCell :=
  Afal.form pr s p .raf

theorem kada_khabar_raf (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) :
    Afal.moodOf (kadaKhabar pr s p) = .raf := Afal.moodOf_raf pr s p

/-- أَنْ المصدريّة (شاهدُ بوّابة)؛ ليست في جدول أدوات الربط — دَينٌ مسمًّى؛ وخبرُ عَسَى بها منصوب. -/
def an : List SCell := [c 0 0, c 25 3]

theorem an_licensed : licensed an = true := by decide
theorem an_not_in_rawabit : Rawabit.particles.any (·.name == "أَنْ") = false := by decide

theorem an_khabar_nasb (pr : Afal.Prefix) (s : Afal.Stem) (p : Afal.Pronoun) :
    Afal.moodOf (Afal.form pr s p .nasb) = .nasb := Afal.moodOf_nasb pr s p

/-! ## شواهدُ البوّابة -/

/-- كَانَ اللَّهُ غَفُورًا: رفعُ الاسم، نصبُ الخبر مع تنوين؛ إِنَّ اللَّهَ غَفُورٌ: العكس. -/
def ghafur : List SCell := [c 19 0, c 20 2, c 27 3, c 10 0]

theorem kana_inna_witness :
    caseClass (tanwin (kana.2 ghafur)) = .nasb ∧ caseClass (tanwin (inna.2 ghafur)) = .raf ∧
    tanwin (kana.2 ghafur) = [c 19 0, c 20 2, c 27 3, c 10 0, c 25 3] ∧
    tanwin (inna.2 ghafur) = [c 19 0, c 20 2, c 27 3, c 10 2, c 25 3] := by decide

/-- لَا رَيْبَ: فتحٌ بلا تنوين ولا أداة. -/
def rayb : List SCell := [c 10 0, c 28 3, c 2 0]

theorem la_rayb_witness :
    laJins.1 rayb = rayb ∧ Nida.hasTanwin (laJins.1 rayb) = false ∧
    caseClass (laJins.1 rayb) = .nasb := by decide

end Slge.Nawasikh
