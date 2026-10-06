import Slge.Filiyya

/-!
# شبهُ الجملة: صورتان على الخانة، وزائدٌ يُردّ بعمليّة، وتعلُّقٌ ومحلٌّ يُقرآن ممّا قبلها

* **د٤ الخانة — صورتان لا ثالثَ لهما**: الجارُّ والمجرور = حرفٌ من جدول `Majrurat.harfs` ثمّ جرٌّ على الخانة
  الأخيرة (`jarrMajrur`؛ يُقرأ جرًّا لكلّ اسم `jarr_majrur_reads_jarr`، ويحفظ الترخيص لكلّ حرفٍ واسم
  `jarr_majrur_licensed`)؛ والظرفُ = اسمٌ من جداول `Zuruf`/`Zaman` منصوبًا (`zarf`؛ `zarf_reads_nasb` في
  `Filiyya`). القارئُ `kind` يفرز الصورتين من الصدر والجدول، وما سواهما ليس شبهَ جملة (`kind_witnesses`).
* **الزائد**: الجرُّ بالحرف الزائد عمليّةٌ على الخانة الأخيرة لا تمسّ المحلّ: ردُّ الزائد رفعٌ يُعيد الاسمَ
  بعينه — `raf (jarr w) = raf w` لكلّ اسم (`zaid_restores`؛ `setLast_setLast`)؛ فما جَاءَ مِنْ أَحَدٍ = ما جَاءَ
  أَحَدٌ على الخانة. والمجرورُ بالزائد خارج شبه الجملة اصطلاحًا — معلَن.
* **قانونُ الحظر**: الظرفُ من الجدول الحاصر (17 ظرفَ مكان + ظروفُ الزمان)؛ وما ليس فيه (المسجدُ، البيتُ)
  لا يُقرأ ظرفًا بالنصب (`masjid_not_zarf`) فيُجرّ بالحرف شبهَ جملةٍ من الصورة الأولى (`fi_masjid`).
* **د٨ الحدّ — التعلّق**: المرتكزُ يُقرأ ممّا قبل شبه الجملة: فعلٌ على قالبه (`Jumla.isVerb`)، أو مشتقٌّ على
  قالب الوصف (`Mansubat.derived`)، وإلّا فالكونُ العامُّ المحذوف (`anchor`). الثلاثةُ حاصرة بالبناء، والشاهدان
  جَلَسَ وقَائِمٌ (`anchor_witnesses`).
* **د١٦ — مصفوفةُ المحلّ**: حين يكون المرتكزُ كونًا محذوفًا، محلُّ شبه الجملة تقرؤه خانةُ ما قبلها: بعد
  الموصول صلةٌ لكلّ الموصولات (`mahall_after_mawsul`)، بعد النكرة المحضة (تنوينٌ) نعتٌ لكلّ جذع
  (`mahall_after_nakira`)، بعد المعرفة بأل منصوبةً حالٌ لكلّ جذع (`mahall_after_al_nasb`)، وبعد المعرفة
  مرفوعةً خبرٌ (`mahall_after_al_raf`). والكونُ المحذوفُ يأخذ حالةَ المحلّ (`kawn`؛ `kawn_reads`): كَائِنٌ في الخبر
  وكَائِنًا في الحال — تقديرُه معلَنٌ وحالتُه مقروءة.
الحصرُ المُرسَل حمل برهانَ Lean لتعريفٍ ثلاثيٍّ للمرتكز وجميعُ فروعه `true`: مبرهنتُه تحصيلُ حاصلٍ على نوعٍ
مُعرَّفٍ باليد لا على الخانة؛ وما هنا يقرأ المرتكزَ والمحلَّ من الخانات بعينها.
القياسُ على MASAQ (الجارُّ والمجرور والظروفُ وجوارُها بشهادات البوّابة) في بايثون.
-/

namespace Slge.Shibh

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## د٤ الخانة — صورتان -/

inductive Kind where
  | jarrMajrur | zarf | none
  deriving DecidableEq, Repr

/-- الجارُّ والمجرور: حرفٌ ثمّ الاسمُ مجرورًا (كسرةٌ على الآخر). -/
def jarrMajrur (h w : List SCell) : List SCell := h ++ Majrurat.jarr w

/-- المجرورُ بعد الحرف بعينه، ويُقرأ جرًّا لكلّ اسمٍ آخرُه ليس نونًا ولا تاء. -/
theorem jarr_majrur_reads_jarr (h w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25 ∧ x.carrier.val ≠ 3) :
    (jarrMajrur h w).drop h.length = Majrurat.jarr w ∧ Tawabi.caseClass (Majrurat.jarr w) = .jarr :=
  ⟨by unfold jarrMajrur; simp, Majrurat.caseClass_jarr w hne hk⟩

/-- الحرفُ ثمّ المجرور مرخَّصٌ لكلّ حرفٍ مرخَّصٍ لا ينتهي بساكنٍ يليه ساكنٌ، ولكلّ اسمٍ مرخَّصٍ آخرُه متحرّك. -/
theorem jarr_majrur_licensed (h w : List SCell) (hh : licensed h = true) (hne : h ≠ [])
    (hw : licensed w = true)
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3)
    (hj : ∀ x y, h.getLast? = some x → (Majrurat.jarr w).head? = some y → (x.isSukun && y.isSukun) = false) :
    licensed (jarrMajrur h w) = true := by
  have hjw : licensed (Majrurat.jarr w) = true := by
    unfold Majrurat.jarr; rw [Zuruf.setLast_licensed w 1 (by decide) hlast]; exact hw
  have hn : noAdj (Majrurat.jarr w) = true := by
    cases hq : Majrurat.jarr w with
    | nil => rfl
    | cons a t => rw [hq] at hjw; simp only [licensed, Bool.and_eq_true] at hjw; exact hjw.2
  exact Damair.attach_licensed h (Majrurat.jarr w) hh hn hne hj

/-- الظرف: اسمٌ من الجدول منصوبًا. -/
def zarf (w : List SCell) : List SCell := Nawasikh.nasb w

/-- القارئ: صدرٌ جارٌّ (من خانتين، أو متّصلٌ تليه أل، أو جارٌّ وضمير) ⇒ جارٌّ ومجرور؛ من جدول الظروف ⇒ ظرف. -/
def kind (w : List SCell) : Kind :=
  if Filiyya.isZarf w then .zarf
  else if Jumla.shibhJumla w then .jarrMajrur
  else .none

def fiDar : List SCell := Jumla.fidDar                                    -- فِي الدَّارِ
def amamaka : List SCell := [c 0 0, c 24 0, c 1 3, c 24 0, c 22 0]         -- أَمَامَكَ
def masaan : List SCell := [c 24 0, c 12 0, c 1 3, c 0 0, c 25 3]          -- مَسَاءً
def masjid : List SCell := [c 24 0, c 12 3, c 5 1, c 8 0]                  -- مَسْجِدَ

theorem kind_witnesses :
    kind fiDar = .jarrMajrur ∧ kind [c 23 0, c 26 2, c 24 3] = .jarrMajrur ∧
    kind (Zuruf.mudaf [c 0 0, c 24 0, c 1 3, c 24 0]) = .zarf ∧ kind [c 20 0, c 27 3, c 21 0] = .zarf ∧
    kind masaan = .zarf ∧ kind Jumla.zayd = .none ∧ kind Jumla.darasa = .none := by decide

/-! ## الزائد: الجرُّ لا يمسّ المحلّ -/

theorem setLast_append_singleton : ∀ (i : List SCell) (x : SCell) (st : Fin 4),
    setLast (i ++ [x]) st = i ++ [⟨x.carrier, st⟩]
  | [], _, _ => rfl
  | [_], _, _ => rfl
  | y :: z :: t, x, st => by
    show y :: setLast (z :: t ++ [x]) st = y :: (z :: t ++ [⟨x.carrier, st⟩])
    rw [setLast_append_singleton (z :: t) x st]

theorem setLast_setLast (w : List SCell) (a b : Fin 4) : setLast (setLast w a) b = setLast w b := by
  cases hw : w with
  | nil => rfl
  | cons x t =>
    have hne : x :: t ≠ [] := by simp
    obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append (x :: t) a hne
    obtain ⟨j, m, hj⟩ := Nawasikh.setLast_eq_append (x :: t) b hne
    have hij : i = j := by
      have h1 := Filiyya.initOf_setLast (x :: t) a
      have h2 := Filiyya.initOf_setLast (x :: t) b
      rw [hi, Zaman.initOf_append_singleton] at h1
      rw [hj, Zaman.initOf_append_singleton] at h2
      rw [h1, h2]
    have hkm : k = m := by
      obtain ⟨y, hy⟩ := Nawasikh.exists_lastOf (x :: t) hne
      have h1 := Nawasikh.lastOf_setLast_carrier (x :: t) a y hy
      have h2 := Nawasikh.lastOf_setLast_carrier (x :: t) b y hy
      rw [hi, Zaman.lastOf_append_singleton] at h1
      rw [hj, Zaman.lastOf_append_singleton] at h2
      simp only [Option.some.injEq, SCell.mk.injEq] at h1 h2
      rw [h1.1, h2.1]
    rw [hi, setLast_append_singleton, hj, hij, hkm]

/-- ردُّ الزائد: رفعُ المجرور بالزائد هو رفعُ الاسم بعينه — مَا جَاءَ مِنْ أَحَدٍ ⇔ مَا جَاءَ أَحَدٌ. -/
theorem zaid_restores (w : List SCell) : Nawasikh.raf (Majrurat.jarr w) = Nawasikh.raf w :=
  setLast_setLast w 1 2

def ahad : List SCell := [c 0 0, c 6 0, c 8 2, c 25 3]                     -- أَحَدٌ

theorem zaid_witness :
    jarrMajrur [c 24 1, c 25 3] (Marifa.dropTanwin ahad) ++ [c 25 3] =
      [c 24 1, c 25 3, c 0 0, c 6 0, c 8 1, c 25 3] ∧                          -- مِنْ أَحَدٍ
    Nawasikh.raf (Majrurat.jarr (Marifa.dropTanwin ahad)) ++ [c 25 3] = ahad := by decide

/-! ## قانونُ الحظر: الجدولُ حاصر -/

/-- المسجدُ ليس في جدول الظروف: نصبُه لا يُقرأ ظرفًا، وجرُّه بالحرف شبهُ جملةٍ من الصورة الأولى. -/
theorem masjid_not_zarf :
    Filiyya.isZarf (zarf masjid) = false ∧ kind (zarf masjid) = .none ∧
    kind (jarrMajrur [c 20 1, c 28 3] (Marifa.al masjid)) = .jarrMajrur ∧
    Zuruf.stems.length = 17 := by decide

/-! ## د٨ الحدّ — التعلّق -/

inductive Anchor where
  | verb | derived | kawn
  deriving DecidableEq, Repr

/-- المرتكزُ ممّا قبل شبه الجملة: فعلٌ على قالبه، أو مشتقٌّ على قالب الوصف، وإلّا فالكونُ العامّ المحذوف. -/
def anchor (prev : List SCell) : Anchor :=
  if Jumla.isVerb prev then .verb
  else if Mansubat.derived (Marifa.dropTanwin prev) then .derived
  else .kawn

def jalasa : List SCell := [c 5 0, c 23 0, c 12 0]                        -- جَلَسَ

/-- جَلَسَ {فِي الحَدِيقَةِ} فعلٌ؛ قَائِمٌ {أَمَامَكَ} مشتقّ؛ الْعِلْمُ {فِي الصُّدُورِ} كونٌ محذوف. -/
theorem anchor_witnesses :
    anchor jalasa = .verb ∧ anchor Jumla.qaim = .derived ∧
    anchor [c 0 0, c 23 3, c 18 1, c 23 3, c 24 2] = .kawn := by decide

/-! ## د١٦ — مصفوفةُ المحلّ -/

inductive Mahall where
  | khabar | naat | hal | sila | unread
  deriving DecidableEq, Repr

/-- المحلُّ من خانة ما قبل شبه الجملة: موصولٌ ⇒ صلة؛ ضميرٌ منفصل ⇒ خبر؛ نكرةٌ (تنوين) ⇒ نعت؛ معرفةٌ مرفوعة ⇒ خبر؛ معرفةٌ
منصوبةٌ أو مجرورة ⇒ حال؛ وما سواه لا يُقرأ. -/
def mahall (prev : List SCell) : Mahall :=
  if Marifa.mawsul.any (fun p => p.2 == prev) then .sila
  else if Categories.pronouns.contains prev then .khabar          -- هُوَ فِي الدَّارِ: الضميرُ مبتدأ
  else if Nida.hasTanwin prev then .naat
  else match Tawabi.caseClass prev with
    | .raf => .khabar
    | .nasb => .hal
    | .jarr => .hal
    | .nasbJarr => .hal
    | .unread => .unread

theorem mahall_after_mawsul : Marifa.mawsul.all (fun p => mahall p.2 == .sila) = true := by decide

theorem hasTanwin_last (l : List SCell) (x : SCell) (hx : x.state.val ≠ 3) :
    Nida.hasTanwin (l ++ [x]) = false := by
  unfold Nida.hasTanwin
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.singleton_append]
  cases l.reverse <;> simp [hx]

/-- بعد النكرة المحضة (خانتان فأكثر) نعتٌ لكلّ جذع: مَنْ وحدَها تشابه نكرةً من خانةٍ منوَّنة. -/
theorem mahall_after_nakira (w : List SCell) (hlen : 2 ≤ w.length) :
    mahall (Mansubat.nakiraMansuba w) = .naat := by
  have hne : w ≠ [] := by intro h; subst h; simp at hlen
  have ht := Mansubat.nakira_has_tanwin w hne
  have hlen' : (Mansubat.nakiraMansuba w).length = w.length + 1 := by
    unfold Mansubat.nakiraMansuba Nawasikh.tanwin Nawasikh.nasb
    simp [Filiyya.length_setLast]
  have hm : Marifa.mawsul.any (fun p => p.2 == Mansubat.nakiraMansuba w) = false := by
    rw [Bool.eq_false_iff]; intro h
    obtain ⟨p, hp, hpe⟩ := List.any_eq_true.1 h
    have hall := List.all_eq_true.1
      (by decide : Marifa.mawsul.all (fun p => !Nida.hasTanwin p.2 || decide (p.2.length ≤ 2)) = true) p hp
    rw [beq_iff_eq.1 hpe, ht, hlen'] at hall
    simp at hall; omega
  have hp : Categories.pronouns.contains (Mansubat.nakiraMansuba w) = false := by
    rw [Bool.eq_false_iff]; intro h
    have hall := List.all_eq_true.1
      (by decide : Categories.pronouns.all (fun p => !Nida.hasTanwin p) = true) _ (List.contains_iff_mem.1 h)
    rw [ht] at hall; simp at hall
  unfold mahall; rw [hm, hp, ht]; rfl

/-- بعد المعرفة بأل مرفوعةً خبرٌ لكلّ جذعٍ (ما لم تصادف صورتُه موصولًا). -/
theorem mahall_after_al_raf (w : List SCell) (hne : w ≠ [])
    (hm : Marifa.mawsul.any (fun p => p.2 == Marifa.al (Nawasikh.raf w)) = false) :
    mahall (Marifa.al (Nawasikh.raf w)) = .khabar := by
  have hp : Categories.pronouns.contains (Marifa.al (Nawasikh.raf w)) = false := by
    rw [Bool.eq_false_iff]; intro h
    have hall := List.all_eq_true.1
      (by decide : Categories.pronouns.all (fun p => !Marifa.hasAl p) = true) _ (List.contains_iff_mem.1 h)
    have hal : Marifa.hasAl (Marifa.al (Nawasikh.raf w)) = true :=
      Marifa.hasAl_al _ (by obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 2 hne; unfold Nawasikh.raf; rw [hi]; simp)
    rw [hal] at hall; simp at hall
  unfold mahall
  rw [hm, hp, Nawasikh.caseClass_al_raf w hne]
  have ht : Nida.hasTanwin (Marifa.al (Nawasikh.raf w)) = false := by
    obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 2 hne
    unfold Nawasikh.raf; rw [hi]; unfold Marifa.al
    cases i with
    | nil =>
      show Nida.hasTanwin (if _ then _ else _) = false
      split
      · exact hasTanwin_last [c 0 0, ⟨⟨k, by omega⟩, 3⟩] ⟨k, 2⟩ (by simp)
      · exact hasTanwin_last [c 0 0, c 23 3] ⟨k, 2⟩ (by simp)
    | cons y t =>
      show Nida.hasTanwin (if _ then _ else _) = false
      split
      · exact hasTanwin_last (c 0 0 :: ⟨y.carrier, 3⟩ :: y :: t) ⟨k, 2⟩ (by simp)
      · exact hasTanwin_last (c 0 0 :: c 23 3 :: y :: t) ⟨k, 2⟩ (by simp)
  rw [ht]; rfl

def usfur : List SCell := [c 0 0, c 23 3, c 18 2, c 14 3, c 20 2, c 27 3, c 10 0]   -- الْعُصْفُورَ
def tair : List SCell := [c 16 0, c 1 3, c 0 1, c 10 0, c 25 3]                    -- طَائِرًا
def ilm : List SCell := [c 0 0, c 23 3, c 18 1, c 23 3, c 24 2]                     -- الْعِلْمُ

/-- الْعِلْمُ {فِي الصُّدُورِ} خبر؛ طَائِرًا {فَوْقَ الغُصْنِ} نعت؛ الْعُصْفُورَ {فَوْقَ} حال؛ الَّذِي {فِي الدَّارِ} صلة. -/
theorem mahall_witnesses :
    mahall ilm = .khabar ∧ mahall tair = .naat ∧ mahall usfur = .hal ∧
    mahall [c 0 0, c 23 3, c 23 0, c 9 1, c 28 3] = .sila := by decide

/-- الكونُ العامُّ المحذوف بحالة المحلّ: كَائِنٌ، كَائِنًا، كَائِنٍ؛ والصلةُ فعلٌ (اسْتَقَرَّ). -/
def kain : List SCell := [c 22 0, c 1 3, c 0 1, c 25 2]                   -- كَائِنُ

def kawn : Mahall → List SCell
  | .khabar => Nawasikh.tanwin (Nawasikh.raf kain)
  | .naat => Nawasikh.tanwin (Nawasikh.nasb kain)
  | .hal => Nawasikh.tanwin (Nawasikh.nasb kain)
  | .sila => [c 0 1, c 12 3, c 3 0, c 21 0, c 10 3, c 10 0]               -- اِسْتَقَرَّ
  | .unread => []

theorem kawn_reads :
    Tawabi.caseClass (kawn .khabar) = .raf ∧ Tawabi.caseClass (kawn .hal) = .nasb ∧
    Jumla.isVerb (kawn .sila) = false ∧ Filiyya.verbRoot (kawn .sila) = none ∧
    ([Mahall.khabar, .naat, .hal, .sila].all (fun m => licensed (kawn m))) = true := by decide

end Slge.Shibh
