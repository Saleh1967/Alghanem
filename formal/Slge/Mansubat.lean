import Slge.Jazm

/-!
# بقيّةُ المنصوبات: الحالُ والتمييزُ عمليّةٌ واحدة، والاستثناءُ ثلاثُ حالاتٍ ثلاثُ عمليّات

على الخانات **الحالُ المفردةُ والتمييزُ عمليّةٌ واحدة**: نكرةٌ منصوبة = فتحٌ فتنوين
(`nakiraMansuba = tanwin ∘ nasb`؛ `tamyiz_eq_hal`). تُقرأ نصبًا لكلّ جذع (`nakira_reads_nasb`)
وتحمل التنوينَ (`nakira_has_tanwin`) وتحفظ الترخيص (`nakira_licensed`). **قانونُ الفرز** (مشتقٌّ/جامد)
يقرؤه **القالب**: ضَاحِك ورَاكِض على فَاعِل، ونَفْس وشَيْب على فَعْل (`sorting_by_template`) — والمعنى
(الهيئةُ/رفعُ الإبهام) معلَن. تمييزُ العدد 11–99 بالقانون نفسِه (`Adad.tamyizState`:
`adad_tamyiz_is_nakira`). والمحوَّلُ عن فاعلٍ عمليّاتٌ: اشْتَعَلَ شَيْبُ الرَّأْسِ ⇄ اشْتَعَلَ الرَّأْسُ شَيْبًا
(`tahwil`، شاهدٌ بالبوّابة).

**الاستثناء** ثلاثُ حالات = ثلاثُ عمليّاتٍ على المستثنى:
* تامٌّ مثبت: `nasb` (مع التنوين للنكرة) — `tamm_muthbat_reads_nasb`.
* تامٌّ منفيّ: `nasb` أو **البدل** — والبدلُ تبعيّةٌ في الحالة: `badal_follows` (من `Tawabi.caseClass_raf`).
* ناقصٌ منفيّ (مفرَّغ): العمليّةُ عمليّةُ الموقع — إِلَّا بلا أثرٍ على الخانة (`mufarragh_eq_role`).
غَيْر وسِوَى: ما بعدهما مضافٌ إليه مجرور (`ghayr_idafa_jarr`)، وهما تأخذان حكمَ ما بعد إِلَّا
(`ghayr_takes_hukm`). خَلَا/عَدَا/حَاشَا: جرٌّ أو نصب؛ وبـ«مَا» نصبٌ: عمليّتان مودَعتان. الأدواتُ مرخَّصة.

النفيُ والتمامُ والموقعُ والرابطُ في الحال الجملة: تيار. القياسُ على MASAQ في بايثون.
-/

namespace Slge.Mansubat

open Slge.Categories (c)
open Slge.Zuruf (setLast)
open Slge.Nawasikh (raf nasb tanwin)
open Slge.Tawabi (caseClass)

/-! ## الحالُ والتمييز: عمليّةٌ واحدة -/

/-- النكرةُ المنصوبة: فتحٌ فتنوين. -/
def nakiraMansuba (w : List SCell) : List SCell := tanwin (nasb w)

def hal : List SCell → List SCell := nakiraMansuba
def tamyiz : List SCell → List SCell := nakiraMansuba

theorem tamyiz_eq_hal : tamyiz = hal := rfl

theorem nakira_reads_nasb (w : List SCell) (hne : w ≠ []) : caseClass (nakiraMansuba w) = .nasb :=
  Nawasikh.caseClass_nasb_tanwin w hne

theorem nakira_has_tanwin (w : List SCell) (hne : w ≠ []) :
    Nida.hasTanwin (nakiraMansuba w) = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 0 hne
  unfold nakiraMansuba tanwin nasb; rw [hi]; unfold Nida.hasTanwin
  simp only [List.append_assoc, List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.cons_append]
  simp [c, Ishara.v25, Ishara.s3]

theorem nakira_licensed (w : List SCell) (hw : licensed w = true) (hne : w ≠ [])
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) :
    licensed (nakiraMansuba w) = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 0 hne
  have h1 : licensed (nasb w) = true := Nawasikh.nasb_licensed w hw hlast
  unfold nakiraMansuba tanwin
  rw [show nasb w = i ++ [⟨k, 0⟩] from hi] at h1 ⊢
  exact Jazm.sukun_licensed _ _ h1 (by simp)
    (fun x hx => by simp at hx; subst hx; rfl)

/-! ## قانونُ الفرز: القالبُ يقرأ المشتقَّ من الجامد -/

/-- قوالبُ الوصف المشتقّ في `Wazn.awzan`: فَاعِل، مَفْعُول، فَعَّال، مِفْعَال، فَعُول، فَعِيل، أَفْعَل، فَعْلَان،
ومُفْعِل … مُسْتَفْعَل، وفَاعِلَة، ومؤنّثاتُ الصفة (فَعْلَاء، فَعْلَى، فُعْلَى) وجمعُ فَعِيل (فُعَلَاء). -/
def derivedTemplates : List Nat :=
  [48, 49, 50, 51, 52, 53, 54, 55, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 99]

/-- مشتقٌّ على الخانة: على قالبٍ من قوالب الوصف (بالضمّ في الآخر كما أُودعت). -/
def derivedBare (w : List SCell) : Bool :=
  derivedTemplates.any (fun k => Sarf.onTemplate (Sarf.templ k) (setLast w 2))

/-- ما بعد الجذع يُسقَط قبل القراءة (دَينٌ سُدِّد): ـَات، ـِين/ـُون، ـَيْن، ـِي (الجمعُ المضاف)، ـَة. -/
def stripSuffix (w : List SCell) : List SCell :=
  let n := w.length
  let at_ (i : Nat) : SCell := w.getD i (c 0 0)
  if n ≥ 4 ∧ at_ (n - 2) = c 1 3 ∧ (at_ (n - 1)).carrier.val = 3 ∧ (at_ (n - 3)).state.val = 0 then
    w.take (n - 2)                                                                    -- ـَات
  else if n ≥ 4 ∧ (at_ (n - 2) = c 28 3 ∨ at_ (n - 2) = c 27 3) ∧ (at_ (n - 1)).carrier.val = 25 then
    w.take (n - 2)                                                                    -- ـِين ـُون ـَيْن
  else if n ≥ 4 ∧ at_ (n - 1) = c 28 3 ∧ (at_ (n - 2)).state.val = 1 then
    w.take (n - 1)                                                                    -- ـِي (مضاف)
  else if n ≥ 3 ∧ (at_ (n - 1)).carrier.val = 3 ∧ (at_ (n - 2)).state.val = 0 then
    w.take (n - 1)                                                                    -- ـَة
  else w

/-- فكُّ الإدغام: أوّلُ ساكنٍ يليه حرفُه نفسُه يُحرَّك بالحالة `s` (صَافّ ← صَافِف). -/
def fakk (s : Fin 4) : List SCell → List SCell
  | x :: y :: t => if x.carrier = y.carrier ∧ x.state.val = 3 ∧ y.state.val ≠ 3 then ⟨x.carrier, s⟩ :: y :: t
      else x :: fakk s (y :: t)
  | w => w

/-- القارئُ التامّ: الجذعُ بعينه، أو بعد إسقاط اللاحقة، أو بعد فكّ الإدغام (بالحالات الثلاث) ثمّ الإسقاط. -/
def derived (w : List SCell) : Bool :=
  derivedBare w || derivedBare (stripSuffix w) ||
    ([0, 1, 2] : List (Fin 4)).any (fun s => derivedBare (fakk s w) || derivedBare (stripSuffix (fakk s w)))

theorem derived_of_bare (w : List SCell) (h : derivedBare w = true) : derived w = true := by
  simp [derived, h]

/-- شواهدُ البوّابة: صَافَّاتٍ (فكٌّ فإسقاط)، مُبْصِرَةً (ـَة)، خَالِدِينَ (ـِين)، بَيْضَاءَ (فَعْلَاء)،
حُنَفَاءَ (فُعَلَاء)، ظَالِمِي (ـِي)؛ ونَفْسٌ وشَيْبٌ وكِتَابٌ لا تُقرأ بعد الإسقاط أيضًا. -/
theorem derived_witnesses :
    derived [c 14 0, c 1 3, c 20 3, c 20 0, c 1 3, c 3 1] = true ∧
    derived [c 24 2, c 2 3, c 14 1, c 10 0, c 3 0] = true ∧
    derived [c 7 0, c 1 3, c 23 1, c 8 1, c 28 3, c 25 0] = true ∧
    derived [c 2 0, c 28 3, c 15 0, c 1 3, c 0 0] = true ∧
    derived [c 6 2, c 25 0, c 20 0, c 1 3, c 0 0] = true ∧
    derived [c 17 0, c 1 3, c 23 1, c 24 1, c 28 3] = true ∧
    derivedBare [c 14 0, c 1 3, c 20 3, c 20 0, c 1 3, c 3 1] = false ∧
    derived [c 25 0, c 20 3, c 12 2] = false ∧ derived [c 13 0, c 28 3, c 2 2] = false ∧
    derived [c 22 1, c 3 0, c 1 3, c 2 2] = false := by decide

def faail : Wazn.Template := Sarf.templ 48
def fal : Wazn.Template := Sarf.templ 29

def dahik : List SCell := [c 15 0, c 1 3, c 6 1, c 22 2]   -- ضَاحِكُ (شاهدُ بوّابة)
def rakid : List SCell := [c 10 0, c 1 3, c 22 1, c 15 2]  -- رَاكِضُ
def nafs : List SCell := [c 25 0, c 20 3, c 12 2]           -- نَفْسُ (شاهدُ بوّابة)
def shayb : List SCell := [c 13 0, c 28 3, c 2 2]           -- شَيْبُ (شاهدُ بوّابة)

theorem sorting_by_template :
    Sarf.onTemplate faail dahik = true ∧ Sarf.onTemplate faail rakid = true ∧
    Sarf.onTemplate fal nafs = true ∧ Sarf.onTemplate fal shayb = true ∧
    derived dahik = true ∧ derived rakid = true ∧ derived nafs = false ∧ derived shayb = false ∧
    derived [c 24 2, c 20 3, c 12 1, c 8 2] = true := by decide                      -- مُفْسِدُ

theorem derived_templates_wf : derivedTemplates.all (fun k => decide (Wazn.WF (Sarf.templ k))) = true := by
  decide

/-- تمييزُ العدد 11–99: الحالةُ نفسُها (فتحٌ منوَّنٌ مفرد). -/
theorem adad_tamyiz_is_nakira : ∀ n, 11 ≤ n → n ≤ 99 → Adad.tamyizState n = (0, true, false) := by
  intro n h1 h2; unfold Adad.tamyizState
  have : ¬(3 ≤ n ∧ n ≤ 10) := fun h => by omega
  simp [this, h1, h2]

/-- المحوَّلُ عن فاعل: اشْتَعَلَ شَيْبُ الرَّأْسِ ⇄ اشْتَعَلَ الرَّأْسُ شَيْبًا — عمليّاتٌ لا معنى. -/
def rasStem : List SCell := [c 10 0, c 0 3, c 12 2]  -- رَأْسُ

def original (s r : List SCell) : List SCell := Marifa.idafa (raf s) (Marifa.al (Zuruf.jarr r))
def tahwil (s r : List SCell) : List SCell × List SCell := (Marifa.al (raf r), nakiraMansuba s)

theorem tahwil_witness :
    (tahwil shayb rasStem).1 = [c 0 0, c 10 3, c 10 0, c 0 3, c 12 2] ∧        -- الرَّأْسُ
    (tahwil shayb rasStem).2 = [c 13 0, c 28 3, c 2 0, c 25 3] ∧                -- شَيْبًا
    licensed (original shayb rasStem) = true ∧ licensed (tahwil shayb rasStem).1 = true ∧
    licensed (tahwil shayb rasStem).2 = true := by decide

/-! ## الاستثناء: ثلاثُ حالاتٍ ثلاثُ عمليّات -/

inductive Istithna where
  | tammMuthbat | tammManfi | naqisManfi
  deriving DecidableEq, Repr

/-- عمليّةُ المستثنى: نصبٌ في التامّ المثبت؛ نصبٌ أو بدلٌ في التامّ المنفيّ؛ وعمليّةُ الموقع في المفرَّغ. -/
def mustathna (k : Istithna) (role : List SCell → List SCell) (badal : Bool) :
    List SCell → List SCell :=
  match k with
  | .tammMuthbat => nakiraMansuba
  | .tammManfi => if badal then role else nakiraMansuba
  | .naqisManfi => role

theorem tamm_muthbat_reads_nasb (role) (b : Bool) (w : List SCell) (hne : w ≠ []) :
    caseClass (mustathna .tammMuthbat role b w) = .nasb := nakira_reads_nasb w hne

/-- البدلُ تبعيّةٌ في الحالة: مرفوعٌ بعد مرفوع (المستثنى منه فاعلٌ). -/
theorem badal_follows (x y : List SCell) (hx : x ≠ []) (hy : y ≠ []) :
    Tawabi.follows (mustathna .tammManfi raf true x) (raf y) = true := by
  unfold Tawabi.follows mustathna; simp only [ite_true]
  rw [Nawasikh.caseClass_raf x hx, Nawasikh.caseClass_raf y hy]; rfl

/-- المفرَّغ: إِلَّا بلا أثرٍ على الخانة؛ العمليّةُ عمليّةُ الموقع. -/
theorem mufarragh_eq_role (role) (b : Bool) : mustathna .naqisManfi role b = role := rfl

/-- الأدوات: حرفٌ، واسمان، وثلاثةٌ أفعالٌ أو حروف. -/
def illa : List SCell := [c 0 1, c 23 3, c 23 0, c 1 3]
def ghayr : List SCell := [c 19 0, c 28 3, c 10 2]          -- غَيْرُ (شاهدُ بوّابة؛ الحكمُ عمليّة)
def siwa : List SCell := [c 12 1, c 27 0, c 1 3]           -- سِوَى
def khala : List SCell := [c 7 0, c 23 0, c 1 3]
def ada : List SCell := [c 18 0, c 8 0, c 1 3]
def hasha : List SCell := [c 6 0, c 1 3, c 13 0, c 1 3]

theorem tools_licensed :
    [illa, ghayr, siwa, khala, ada, hasha].all licensed = true := by decide

theorem illa_ghayr_in_rawabit :
    Rawabit.particles.any (fun p => p.name == "إِلَّا" && p.amal == .none) = true ∧
    Rawabit.particles.any (fun p => p.name == "غَيْرُ" && p.amal == .jarr) = true := by decide

/-- غَيْر مضافةٌ: ما بعدها مجرور، وهي تأخذ حكمَ ما بعد إِلَّا. -/
def ghayrOf (hukm : List SCell → List SCell) (w : List SCell) : List SCell :=
  Marifa.idafa (hukm ghayr) (Zuruf.jarr w)

theorem ghayr_idafa_jarr (hukm) (w : List SCell) (hne : w ≠ []) :
    ∃ k, Afal.lastOf (ghayrOf hukm w) = some ⟨k, 1⟩ := by
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast w 1 hne
  refine ⟨k, ?_⟩
  unfold ghayrOf Marifa.idafa
  obtain ⟨i, k', hi⟩ := Nawasikh.setLast_eq_append w 1 hne
  show Afal.lastOf (Marifa.dropTanwin (hukm ghayr) ++ setLast w 1) = _
  rw [hi, ← List.append_assoc, Zaman.lastOf_append_singleton]
  rw [hi, Zaman.lastOf_append_singleton] at hk
  exact hk

theorem ghayr_takes_hukm :
    caseClass (ghayrOf raf [c 10 0, c 5 2, c 23 2]) ≠ .raf ∧      -- الحكمُ في غَيْر لا في المضاف إليه
    caseClass (raf ghayr) = .raf ∧ caseClass (nasb ghayr) = .nasb := by decide

/-- خَلَا/عَدَا/حَاشَا: ما بعدها مجرورٌ أو منصوب؛ وبـ«مَا» منصوبٌ حتمًا. -/
def afterKhala (ma : Bool) (w : List SCell) : List SCell := if ma then nasb w else Zuruf.jarr w

theorem ma_khala_nasb (w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25) :
    caseClass (afterKhala true w) = .nasb := Nawasikh.caseClass_nasb w hne hk

/-- شواهدُ البوّابة: سُجَّدًا (حال)، شَيْبًا وعُيُونًا وكَوْكَبًا (تمييز) = العمليّةُ على الجذع. -/
theorem witnesses :
    nakiraMansuba [c 12 2, c 5 3, c 5 0, c 8 2] = [c 12 2, c 5 3, c 5 0, c 8 0, c 25 3] ∧
    nakiraMansuba shayb = [c 13 0, c 28 3, c 2 0, c 25 3] ∧
    nakiraMansuba [c 18 2, c 28 2, c 27 3, c 25 2] = [c 18 2, c 28 2, c 27 3, c 25 0, c 25 3] ∧
    nakiraMansuba [c 22 0, c 27 3, c 22 0, c 2 2] = [c 22 0, c 27 3, c 22 0, c 2 0, c 25 3] := by
  decide

/-- سُكَارَى حالٌ ممنوعةٌ من الصرف مقصورة: لا تنوينَ، والحركةُ مقدَّرةٌ لا تقرؤها الخانة. -/
def sukara : List SCell := [c 12 2, c 22 0, c 1 3, c 10 0, c 1 3]

theorem sukara_hal : Nida.hasTanwin sukara = false ∧ caseClass sukara = .unread ∧
    Sarf.illa sukara = .maqsura := by decide

end Slge.Mansubat
