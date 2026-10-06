import Slge.Jumla

/-!
# الجملةُ الفعليّة: نواةٌ (فعلٌ وفاعل) تُقرأ من الخانة، ورتبةٌ ثلاثيّةٌ من الخانات، ونيابةٌ عمليّتان، ومفاعيلُ نصبٌ

* **د٤ الخانة — الفعل**: ثلاثُ حالات. الماضي مبنيٌّ وآخرُه يقرؤه ما اتّصل به (فتحٌ بلا لاحقة، سكونٌ قبل التاء
  ونَا، ضمٌّ قبل الواو: `pastEnding` على `Damair.rafSuffixes`؛ `past_endings`)؛ والمضارعُ معربٌ بعلاماتٍ ثلاثٍ
  عمليّاتٍ ثلاثٍ مبرهَنةٍ في `Jazm` و`Afal` (الضمّةُ وثبوتُ النون، الفتحةُ وحذفُ النون، السكونُ وحذفُ النون
  وحذفُ العلّة)؛ والأمرُ مبنيٌّ على ما يُجزم به مضارعُه: آخرُ `Fil.amrOf` ساكنٌ كآخر `Jazm.sukun` لكلّ
  القوالب المودَعة (`amr_ends_like_jazm`).
* **الفاعل**: مرفوعٌ بعمليّةٍ واحدة (`fail`؛ يُقرأ رفعًا لكلّ جذع `fail_reads_raf`)؛ صورُه الثلاث: ظاهرٌ
  من رفعه، بارزٌ متّصلٌ من جدول `Damair.rafSuffixes` (`attached_subject` لكلّ فعل)، ومستترٌ لا خانةَ له؛
  والمصدرُ المؤوّل تيار.
* **د٨ الحدّ — رتبُ التباديل (ف × س₁ × س₂)**: الرتبةُ دالّةٌ في الخانات لا في الموضع (`order`، `order_swap`):
  الفاعلُ متّصلٌ بالفعل ⇒ الفاعلُ أوّلًا (`attached_subject_first` لكلّ فعل ومفعول)، خفاءُ العلامة في الطرفين
  ⇒ الفاعلُ أوّلًا، الضميرُ العائدُ في الفاعل ⇒ المفعولُ أوّلًا، المفعولُ متّصلٌ بالفعل ⇒ المفعولُ أوّلًا
  (`attached_object_first`)، المفعولُ اسمُ صدارة ⇒ قبل الفعل؛ وما سواه جواز. الحصرُ بإلّا تيار.
* **د١٦ — النيابة**: المبنيُّ للمجهول عمليّتان على الحالات (ضمُّ الأوّل وكسرُ ما قبل الآخر: `majhul`؛ قَالَبُه
  فُعِلَ من فَعَلَ بعينه `majhul_fill`؛ والمضارعُ ضمٌّ ففتح `majhulPres`)؛ ونائبُ الفاعل بالرفع نفسِه
  (`naib_eq_fail`)؛ والنائبُ الأربعة يقرؤها صدرُ الكلمة وجدولُها (`naibKind`)، وترتيبُها معلَن.
* **المفاعيلُ الأربعة**: نصبٌ وتنوين (`maful`). المفعولُ فيه من جداول `Zuruf`/`Zaman` (`zarf_reads_nasb`)،
  والمختصُّ (المسجد) خارج الجدول فلا يُنصب — معجم. المفعولُ لأجله مصدرٌ على قالبه (`isMasdar`) لا مشتقٌّ
  (`sorting_masdar_hal`: رَغْبَةً مصدرٌ، رَاغِبًا حال). المفعولُ معه واوٌ متّصلةٌ ونصب (`maiyya`؛ يحفظ
  الترخيص `maiyya_licensed`)؛ وفعلُ المشاركة على تَفَاعَلَ عطفٌ (`tafaala_is_ataf`)؛ وما سواه معجم. المفعولُ
  المطلق مصدرُ الفعل بجذره بعينه (`mutlaq_shares_root` لكلّ جذر).
القياسُ على MASAQ (أفعالُ المصحف وفاعلُها ومفاعيلُها بشهادات البوّابة) في بايثون.
-/

namespace Slge.Filiyya

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## د٤ الخانة — الفعل -/

inductive PastEnding where
  | fath | sukun | damm | unread
  deriving DecidableEq, Repr

/-- آخرُ الماضي قبل اللاحقة: فتحٌ بلا لاحقة، سكونٌ قبل التاء ونَا ونون النسوة، ضمٌّ قبل واو الجماعة. -/
def pastEnding (stem : List SCell) (suffix : List SCell) : PastEnding :=
  match suffix with
  | [] => .fath
  | [⟨⟨27, _⟩, ⟨3, _⟩⟩] => .damm
  | ⟨⟨3, _⟩, _⟩ :: _ => .sukun
  | [⟨⟨25, _⟩, ⟨0, _⟩⟩, ⟨⟨1, _⟩, ⟨3, _⟩⟩] => .sukun
  | [⟨⟨25, _⟩, ⟨0, _⟩⟩] => .sukun
  | [⟨⟨1, _⟩, ⟨3, _⟩⟩] => .fath
  | _ => if stem.isEmpty then .unread else .unread

/-- الماضي بلاحقته: الآخرُ بالحالة التي تقرؤها اللاحقة، ثمّ اللاحقة. -/
def past (stem suffix : List SCell) : List SCell :=
  let st : Fin 4 := match pastEnding stem suffix with
    | .fath => 0 | .sukun => 3 | .damm => 2 | .unread => 0
  setLast stem st ++ suffix

theorem past_endings :
    (Damair.rafSuffixes.map (fun p => pastEnding [c 22 0, c 3 0, c 2 0] p.2)) =
      [.sukun, .sukun, .sukun, .sukun, .sukun, .sukun, .damm, .fath, .sukun, .unread, .sukun] ∧
    past [c 22 0, c 3 0, c 2 0] [] = [c 22 0, c 3 0, c 2 0] ∧                 -- كَتَبَ
    past [c 22 0, c 3 0, c 2 0] [c 3 2] = [c 22 0, c 3 0, c 2 3, c 3 2] ∧      -- كَتَبْتُ
    past [c 22 0, c 3 0, c 2 0] [c 27 3] = [c 22 0, c 3 0, c 2 2, c 27 3] ∧    -- كَتَبُوا
    past [c 22 0, c 3 0, c 2 0] [c 25 0, c 1 3] = [c 22 0, c 3 0, c 2 3, c 25 0, c 1 3] := by decide

theorem length_setLast : ∀ (w : List SCell) (st : Fin 4), (setLast w st).length = w.length
  | [], _ => rfl
  | [_], _ => rfl
  | _ :: y :: t, st => by
    show (_ :: setLast (y :: t) st).length = _
    simp [length_setLast (y :: t) st]

theorem initOf_setLast : ∀ (w : List SCell) (st : Fin 4), Afal.initOf (setLast w st) = Afal.initOf w
  | [], _ => rfl
  | [_], _ => rfl
  | x :: y :: t, st => by
    show Afal.initOf (x :: setLast (y :: t) st) = Afal.initOf (x :: y :: t)
    obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append (y :: t) st (by simp)
    have ih := initOf_setLast (y :: t) st
    rw [hi] at ih ⊢
    cases i with
    | nil => simp [Afal.initOf] at ih ⊢; exact ih
    | cons z r => simp only [List.cons_append, Afal.initOf] at ih ⊢; rw [ih]

/-- الماضي بلاحقةٍ مرخَّصٌ لكلّ جذعٍ سالمٍ مرخَّص (خانتان فأكثر، آخرُه متحرّكٌ وما قبله متحرّك): واوُ الجماعة
بعد ضمّ، والتاءُ ونَا بعد سكون. -/
theorem past_licensed (stem : List SCell) (hw : licensed stem = true) (hlen : 2 ≤ stem.length)
    (hlast : ∀ x, Afal.lastOf stem = some x → x.state.val ≠ 3)
    (hpen : ∀ x, (Afal.initOf stem).getLast? = some x → x.isSukun = false) :
    licensed (past stem [c 27 3]) = true ∧ licensed (past stem [c 3 2]) = true ∧
    licensed (past stem [c 25 0, c 1 3]) = true := by
  have hne : stem ≠ [] := by intro h; subst h; simp at hlen
  refine ⟨Jumla.suffix_licensed stem _ 2 (by decide) hw hne hlast (by decide), ?_, ?_⟩
  all_goals
    obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append stem 3 hne
    have hi' : i = Afal.initOf stem := by
      have := initOf_setLast stem 3
      rw [hi, Zaman.initOf_append_singleton] at this; exact this
    have hil : licensed i = true := by rw [hi']; exact Marifa.licensed_initOf stem hw
    have hine : i ≠ [] := by
      intro h; rw [h] at hi
      have := congrArg List.length hi; rw [length_setLast] at this; simp at this; omega
    have hhost : licensed (i ++ [⟨k, 3⟩]) = true :=
      Jazm.sukun_licensed i k hil hine (by rw [hi']; exact hpen)
    show licensed (setLast stem 3 ++ _) = true
    rw [hi]
    refine Damair.attach_licensed _ _ hhost (by decide) (by simp) ?_
    intro x y hx hy
    simp at hy; subst hy; simp [SCell.isSukun, c]

/-- الأمرُ مبنيٌّ على ما يُجزم به مضارعُه: آخرُه ساكنٌ لكلّ قوالب الأمر المودَعة، كآخر `Jazm.sukun`. -/
def amrTemplates : List Nat := [8, 9, 10] ++ Fil.mazidAmr

theorem amr_ends_like_jazm :
    amrTemplates.all (fun k => (Sarf.templ k).getLast? == some (.slot 2 3)) = true ∧
    (Fil.mazidPres.zip Fil.mazidAmr).all (fun p =>
      (Fil.amrOf (Sarf.templ p.1)).getLast? == (Jazm.sukun (Wazn.mizan (Sarf.templ p.1))).getLast?.map
        (fun x => Wazn.Sym.slot 2 x.state)) = true := by decide

/-! ## الفاعل -/

def fail (w : List SCell) : List SCell := Nawasikh.raf w

theorem fail_reads_raf (w : List SCell) (hne : w ≠ []) : Tawabi.caseClass (fail w) = .raf := by
  obtain ⟨i, a, hi⟩ := Nawasikh.setLast_eq_append w 2 hne
  unfold fail Nawasikh.raf; rw [hi]; exact Nawasikh.caseClass_of_last_damm i a

/-- الفاعلُ البارزُ المتّصل: لاحقةٌ من جدول `Damair.rafSuffixes` بحالة ما قبلها (سكونٌ قبل التاء ونَا ونون
النسوة، ضمٌّ قبل واو الجماعة، فتحٌ قبل ألف الاثنين، كسرٌ قبل ياء المخاطبة)، ولواحقُ المضارع ُونَ ِينَ َانِ. -/
def subjectSuffixes : List (List SCell × Fin 4) :=
  [([c 3 2], 3), ([c 3 0], 3), ([c 3 1], 3), ([c 3 2, c 24 0, c 1 3], 3), ([c 3 2, c 24 3], 3),
   ([c 3 2, c 25 3, c 25 0], 3), ([c 27 3], 2), ([c 1 3], 0), ([c 25 0], 3), ([c 28 3], 1),
   ([c 25 0, c 1 3], 3), ([c 27 3, c 25 0], 2), ([c 28 3, c 25 0], 1), ([c 1 3, c 25 1], 0)]

theorem subjectSuffixes_from_table :
    (subjectSuffixes.take 11).map (·.1) = Damair.rafSuffixes.map (·.2) := by decide

def endsWithState (v : List SCell) (p : List SCell) (st : Fin 4) : Bool :=
  p.isSuffixOf v && p.length < v.length &&
    ((v.take (v.length - p.length)).getLast?.map (·.state) == some st)

/-- ياءُ المتكلّم بنون الوقاية (ـنِي) مفعولٌ لا مخاطبة. -/
def hasSubject (v : List SCell) : Bool :=
  subjectSuffixes.any (fun p => endsWithState v p.1 p.2) && !([c 25 1, c 28 3].isSuffixOf v)

theorem isSuffixOf_append (l p : List SCell) : p.isSuffixOf (l ++ p) = true := by
  simp [List.isSuffixOf_iff_suffix]

theorem endsWithState_append (l p : List SCell) (st : Fin 4) (hl : l ≠ []) :
    endsWithState (l ++ p) p st = (l.getLast?.map (·.state) == some st) := by
  unfold endsWithState
  have h1 : p.isSuffixOf (l ++ p) = true := List.isSuffixOf_iff_suffix.2 (List.suffix_append l p)
  have h2 : (l ++ p).length - p.length = l.length := by simp
  have h3 : p.length < (l ++ p).length := by
    simp only [List.length_append]; exact Nat.lt_add_of_pos_left (List.length_pos_iff.2 hl)
  rw [h1, h2, List.take_left]; simp [List.length_pos_iff.2 hl]

/-- كلُّ فعلٍ لحقته لاحقةٌ من الجدول بحالتها يُقرأ فاعلُه بارزًا (ما لم تكن ـنِي). -/
theorem attached_subject (v : List SCell) (hne : v ≠ []) (p : List SCell × Fin 4)
    (hp : p ∈ subjectSuffixes) (hni : ([c 25 1, c 28 3].isSuffixOf (setLast v p.2 ++ p.1)) = false) :
    hasSubject (setLast v p.2 ++ p.1) = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append v p.2 hne
  have hsl : setLast v p.2 ≠ [] := by rw [hi]; simp
  unfold hasSubject
  rw [hni]
  simp only [Bool.not_false, Bool.and_true, List.any_eq_true]
  refine ⟨p, hp, ?_⟩
  rw [endsWithState_append _ _ _ hsl, hi]
  simp [List.getLast?_append]

/-- المفعولُ المتّصل: لاحقةٌ من جدول النصب (مع صورِ الهاء المكسورة) أو ـنِي، بعد متحرّك. -/
def objectSuffixes : List (List SCell) := [c 25 1, c 28 3] :: Jumla.aidSuffixes

def hasObject (v : List SCell) : Bool :=
  objectSuffixes.any (fun p => p.isSuffixOf v && p.length < v.length &&
    ((v.take (v.length - p.length)).getLast?.map (·.isSukun) == some false))

theorem attached_object (v : List SCell) (hne : v ≠ [])
    (hlast : ∀ x, v.getLast? = some x → x.isSukun = false) :
    objectSuffixes.all (fun p => hasObject (v ++ p)) = true := by
  simp only [List.all_eq_true]
  intro p hp
  unfold hasObject
  simp only [List.any_eq_true]
  refine ⟨p, hp, ?_⟩
  obtain ⟨x, hx⟩ : ∃ x, v.getLast? = some x := by
    cases h : v.getLast? with
    | none => exact absurd (List.getLast?_eq_none_iff.1 h) hne
    | some x => exact ⟨x, rfl⟩
  simp [isSuffixOf_append, List.take_left', hx, hlast x hx, (by cases v <;> simp_all : 0 < v.length)]

/-! ## د٨ الحدّ — رتبُ التباديل -/

/-- الجملةُ الفعليّة: الفعلُ (بما اتّصل به)، والفاعلُ الظاهر، والمفعولُ الظاهر، وموضعُهما. -/
inductive Pos where
  | FSO | FOS | OFS
  deriving DecidableEq, Repr

structure Filiyya where
  fil : List SCell
  fail : List SCell
  maful : List SCell
  pos : Pos := .FSO
  deriving DecidableEq, Repr

inductive Rutba where
  | failFirst | mafulFirst | mafulBeforeFil | free
  deriving DecidableEq, Repr

/-- خفاءُ العلامة: الطرفان لا تقرأ الخانةُ حالتَهما (مُوسَى، عِيسَى). -/
def hidden (w : List SCell) : Bool := Tawabi.caseClass w == .unread

/-- الرتبةُ من الخانات: (أ) الفاعلُ متّصلٌ أو العلامةُ خفيّةٌ في الطرفين ⇒ الفاعلُ أوّلًا؛ (ب) الضميرُ العائدُ
في الفاعل أو المفعولُ متّصلٌ ⇒ المفعولُ أوّلًا؛ (ج) المفعولُ اسمُ صدارة ⇒ قبل الفعل؛ وما سواه جواز. -/
def order (j : Filiyya) : Rutba :=
  if Jumla.istifham j.maful then .mafulBeforeFil
  else if hasSubject j.fil ∧ ¬hasObject j.fil then .failFirst
  else if hasObject j.fil ∧ ¬hasSubject j.fil then .mafulFirst
  else if Jumla.hasAidPronoun j.fail then .mafulFirst
  else if hidden j.fail ∧ hidden j.maful then .failFirst
  else .free

def swap (j : Filiyya) : Filiyya :=
  ⟨j.fil, j.fail, j.maful, match j.pos with | .FSO => .FOS | .FOS => .FSO | .OFS => .OFS⟩

theorem order_swap (j : Filiyya) : order (swap j) = order j := by cases j; rfl

def admissible (j : Filiyya) : Bool :=
  match order j, j.pos with
  | .failFirst, .FSO => true
  | .mafulFirst, .FOS => true
  | .mafulBeforeFil, .OFS => true
  | .free, _ => true
  | _, _ => false

/-- الفاعلُ المتّصلُ بالفعل (بلا مفعولٍ متّصل) يقدّم الفاعلَ لكلّ فعلٍ ومفعولٍ غيرِ ذي صدارة. -/
theorem attached_subject_first (v : List SCell) (hv : v ≠ []) (p : List SCell × Fin 4)
    (hp : p ∈ subjectSuffixes) (hni : ([c 25 1, c 28 3].isSuffixOf (setLast v p.2 ++ p.1)) = false)
    (hno : hasObject (setLast v p.2 ++ p.1) = false) (m : List SCell) (hm : Jumla.istifham m = false)
    (f : List SCell) : order ⟨setLast v p.2 ++ p.1, f, m, .FSO⟩ = .failFirst := by
  have hs := attached_subject v hv p hp hni
  simp [order, hm, hs, hno]

/-- المفعولُ المتّصلُ بالفعل (بلا فاعلٍ متّصل) يقدّم المفعولَ لكلّ فعلٍ وفاعلٍ ومفعولٍ غيرِ ذي صدارة. -/
theorem attached_object_first (v p : List SCell) (hv : v ≠ [])
    (hlast : ∀ x, v.getLast? = some x → x.isSukun = false) (hp : p ∈ objectSuffixes)
    (hns : hasSubject (v ++ p) = false) (f m : List SCell) (hm : Jumla.istifham m = false) :
    order ⟨v ++ p, f, m, .FOS⟩ = .mafulFirst := by
  have ho : hasObject (v ++ p) = true := List.all_eq_true.1 (attached_object v hv hlast) p hp
  simp [order, hm, hns, ho]

def katabtu : List SCell := [c 22 0, c 3 0, c 2 3, c 3 2]            -- كَتَبْتُ
def addars : List SCell := [c 0 0, c 8 3, c 8 0, c 10 3, c 12 0]       -- الدَّرْسَ
def musa : List SCell := [c 24 2, c 27 3, c 12 0, c 1 3]               -- مُوسَى (بوّابة)
def isa : List SCell := [c 18 1, c 28 3, c 12 0, c 1 3]                -- عِيسَى (بوّابة)
def daraba : List SCell := [c 15 0, c 10 0, c 2 0]                     -- ضَرَبَ
def sakana : List SCell := [c 12 0, c 22 0, c 25 0]                    -- سَكَنَ
def addar : List SCell := [c 0 0, c 8 3, c 8 0, c 1 3, c 10 0]         -- الدَّارَ
def sahibuha : List SCell := [c 14 0, c 1 3, c 6 1, c 2 2, c 26 0, c 1 3]  -- صَاحِبُهَا
def akramani : List SCell := [c 0 0, c 22 3, c 10 0, c 24 0, c 25 1, c 28 3]  -- أَكْرَمَنِي
def abuka : List SCell := [c 0 0, c 2 2, c 27 3, c 22 0]               -- أَبُوكَ
def qabalta : List SCell := [c 21 0, c 1 3, c 2 0, c 23 3, c 3 0]      -- قَابَلْتَ
def ayya : List SCell := Istifham.ayy 0                                -- أَيَّ
def akala : List SCell := [c 0 0, c 22 0, c 23 0]                      -- أَكَلَ
def zaydun : List SCell := Jumla.zayd                                  -- زَيْدٌ
def tuffahatan : List SCell := [c 3 2, c 20 3, c 20 0, c 1 3, c 6 0, c 3 0, c 25 3]  -- تُفَّاحَةً

/-- الخمسةُ والجواز كما في الحصر: كَتَبْتُ الدَّرْسَ، ضَرَبَ مُوسَى عِيسَى، سَكَنَ الدَّارَ صَاحِبُهَا،
أَكْرَمَنِي أَبُوكَ، أَيَّ رَجُلٍ قَابَلْتَ، أَكَلَ زَيْدٌ تُفَّاحَةً (جواز). -/
theorem order_witnesses :
    order ⟨katabtu, [], addars, .FSO⟩ = .failFirst ∧
    order ⟨daraba, musa, isa, .FSO⟩ = .failFirst ∧
    order ⟨sakana, sahibuha, addar, .FOS⟩ = .mafulFirst ∧
    order ⟨akramani, abuka, [], .FOS⟩ = .mafulFirst ∧
    order ⟨qabalta, [], ayya, .OFS⟩ = .mafulBeforeFil ∧
    order ⟨akala, zaydun, tuffahatan, .FSO⟩ = .free ∧
    admissible ⟨daraba, musa, isa, .FOS⟩ = false ∧ admissible ⟨akala, zaydun, tuffahatan, .FOS⟩ = true ∧
    admissible ⟨sakana, sahibuha, addar, .FSO⟩ = false := by decide

/-! ## د١٦ — النيابة -/

/-- المبنيُّ للمجهول من الماضي: ضمُّ الأوّل وكسرُ ما قبل الآخر (عمليّتا حالة لا حرف). -/
def majhul : List SCell → List SCell
  | x :: rest =>
      ⟨x.carrier, 2⟩ :: (match rest.reverse with
        | l :: m :: t => (l :: ⟨m.carrier, 1⟩ :: t).reverse
        | r => r.reverse)
  | [] => []

/-- والمضارعُ: ضمُّ الأوّل وفتحُ ما قبل الآخر. -/
def majhulPres : List SCell → List SCell
  | x :: rest =>
      ⟨x.carrier, 2⟩ :: (match rest.reverse with
        | l :: m :: t => (l :: ⟨m.carrier, 0⟩ :: t).reverse
        | r => r.reverse)
  | [] => []

/-- فَعَلَ ← فُعِلَ ويَفْعَلُ ← يُفْعَلُ لكلّ جذر: قالبا الشبكة بعينهما. -/
theorem majhul_fill (r : Wazn.Root) :
    majhul (Wazn.fill (Sarf.templ 0) r) = Wazn.fill (Sarf.templ 3) r ∧
    majhulPres (Wazn.fill (Sarf.templ 4) r) = Wazn.fill (Sarf.templ 7) r := by
  constructor <;> simp [Wazn.fill, Sarf.templ, Wazn.awzan, Wazn.fillSym, majhul, majhulPres, Wazn.r,
    Wazn.l, List.reverse_cons]

/-- المجهولُ لا يغيّر نمطَ السكون في الماضي السالم (ما قبل الآخر متحرّكٌ أصلًا) فيحفظ الترخيص. -/
theorem majhul_witnesses :
    majhul [c 22 0, c 3 0, c 2 0] = [c 22 2, c 3 1, c 2 0] ∧                     -- كُتِبَ
    majhulPres [c 28 0, c 22 3, c 3 2, c 2 2] = [c 28 2, c 22 3, c 3 0, c 2 2] ∧   -- يُكْتَبُ
    licensed (majhul [c 22 0, c 3 0, c 2 0]) = true ∧
    licensed (majhulPres [c 28 0, c 22 3, c 3 2, c 2 2]) = true := by decide

/-- نائبُ الفاعل بالرفع نفسِه. -/
def naib (w : List SCell) : List SCell := Nawasikh.raf w
theorem naib_eq_fail : naib = fail := rfl

inductive NaibKind where
  | maful | majrur | zarf | masdar
  deriving DecidableEq, Repr

/-- قوالبُ المصدر في `Wazn.awzan`: 29–47، وفَعْلَة/فِعْلَة/فَعْلِيَّة (المرّةُ والهيئةُ والصناعيُّ مصادر). -/
def masdarTemplates : List Nat := (List.range 19).map (· + 29) ++ [63, 64, 65]

def isMasdar (w : List SCell) : Bool :=
  masdarTemplates.any (fun k =>
    Sarf.onTemplate (Sarf.templ k) (setLast (Marifa.dropTanwin (Jumla.bare w)) 2))

def isZarf (w : List SCell) : Bool :=
  Zuruf.forms.any (· == setLast w 0) || Zaman.forms.any (· == w) || Zaman.forms.any (· == setLast w 0)

/-- النائبُ من صدر الكلمة وجدولها: مجرورٌ (شبهُ جملة)، ظرفٌ، مصدرٌ، وإلّا فالمفعولُ به؛ والترتيبُ معلَن. -/
def naibKind (w : List SCell) : NaibKind :=
  if isZarf w then .zarf
  else if Jumla.shibhJumla w then .majrur
  else if isMasdar w then .masdar
  else .maful

/-- ضُرِبَ الرَّجُلُ، نُظِرَ فِي الْأَمْرِ، صِيمَ يَوْمُ الخميس (بالإضافة)، فُهِمَ فَهْمٌ؛ وكُتِبَ الدَّرْسُ يقرؤه
القالبُ مصدرًا (فَعْل) — الخانةُ لا تفرّق اسمَ المصدر من المصدر: معجم. -/
theorem naib_witnesses :
    naibKind (naib [c 0 0, c 10 3, c 10 0, c 5 2, c 23 0]) = .maful ∧
    naibKind (naib [c 0 0, c 8 3, c 8 0, c 10 3, c 12 0]) = .masdar ∧
    naibKind [c 20 1, c 28 3, c 0 0, c 23 3, c 0 0, c 24 3, c 10 1] = .majrur ∧
    naibKind [c 28 0, c 27 3, c 24 2] = .zarf ∧
    naibKind [c 20 0, c 26 3, c 24 2, c 25 3] = .masdar := by decide

/-! ## المفاعيلُ الأربعة -/

/-- المفعولُ: نصبٌ فتنوين (عمليّتا `Nawasikh`). -/
def maful (w : List SCell) : List SCell := Nawasikh.tanwin (Nawasikh.nasb w)

theorem maful_reads_nasb (w : List SCell) (hne : w ≠ []) : Tawabi.caseClass (maful w) = .nasb := by
  obtain ⟨i, a, hi⟩ := Nawasikh.setLast_eq_append w 0 hne
  unfold maful Nawasikh.tanwin Nawasikh.nasb; rw [hi]
  cases i using List.rec with
  | nil => rfl
  | cons x t _ =>
    simp only [Tawabi.caseClass, List.append_assoc, List.reverse_append,
      List.reverse_cons, List.reverse_nil, List.nil_append, List.cons_append]
    cases t.reverse <;> simp [c, Jumla.v25, Jumla.s3]

/-- المفعولُ فيه: ظرفٌ من الجدول منصوبٌ (`Zuruf.mudaf`/`Zaman.nasbTanwin`) يُقرأ نصبًا؛ والمختصُّ خارج الجدول. -/
theorem zarf_reads_nasb :
    Zuruf.stems.all (fun p => Zuruf.hukm (Zuruf.mudaf p.2) == .mansubMudaf) = true ∧
    Zaman.stems.all (fun p => Zaman.hukm (Zaman.nasbTanwin p.2) == .mansub) = true ∧
    isZarf [c 20 0, c 27 3, c 21 0] = true ∧ isZarf [c 0 0, c 23 3, c 24 0, c 12 3, c 5 1, c 8 0] = false := by
  decide

/-- جذرُ الكلمة على أوّل قالبٍ يقبلها من قائمة. -/
def rootOn (ks : List Nat) (w : List SCell) : Option Wazn.Root :=
  (ks.find? (fun k => Sarf.onTemplate (Sarf.templ k) w)).bind fun k =>
    match Wazn.rootOf (Sarf.templ k) w 0, Wazn.rootOf (Sarf.templ k) w 1, Wazn.rootOf (Sarf.templ k) w 2 with
    | some a, some b, some d => some (fun i => if i = 0 then a else if i = 1 then b else d)
    | _, _, _ => none

/-- جذرُ الفعل: بعينه، أو بعد إسقاط لاحقةٍ من جدولي الفاعل والمفعول وردِّ آخره فتحًا أو ضمًّا. -/
def verbRoot (v : List SCell) : Option Wazn.Root :=
  let strip := (subjectSuffixes.map (·.1) ++ objectSuffixes).filterMap fun p =>
    if p.isSuffixOf v && p.length < v.length then some (v.take (v.length - p.length)) else none
  let cands := v :: strip.flatMap fun b => [setLast b 0, setLast b 2]
  (cands.filterMap (rootOn Jumla.verbTemplates)).head?
def masdarRoot (w : List SCell) : Option Wazn.Root :=
  rootOn masdarTemplates (setLast (Marifa.dropTanwin (Jumla.bare w)) 2)

/-- قانونُ الفرز: مشتقٌّ على قالب الوصف ⇒ حال؛ مصدرٌ بجذر الفعل ⇒ مفعولٌ مطلق؛ مصدرٌ بغيره ⇒ مفعولٌ لأجله. -/
inductive Fadla where
  | liajlih | mutlaqF | hal | unread
  deriving DecidableEq, Repr

def sortFadla (w : List SCell) (v : List SCell) : Fadla :=
  if Mansubat.derived (Marifa.dropTanwin w) then .hal
  else match masdarRoot w, verbRoot v with
    | some r, some rv => if r 0 == rv 0 && r 1 == rv 1 && r 2 == rv 2 then .mutlaqF else .liajlih
    | some _, none => .liajlih
    | none, _ => .unread

def qumtu : List SCell := [c 21 2, c 24 3, c 3 2]                      -- قُمْتُ
def darabtu : List SCell := [c 15 0, c 10 0, c 2 3, c 3 2]              -- ضَرَبْتُ

/-- قُمْتُ إِجْلَالًا ودَرَسْتُ رَغْبَةً لأجلِه؛ ضَرَبْتُ ضَرْبًا مطلقٌ (الجذرُ واحد)؛ قُمْتُ رَاغِبًا حال. -/
theorem sorting_masdar_hal :
    sortFadla [c 10 0, c 20 3, c 2 0, c 3 0, c 25 3] [c 8 0, c 10 0, c 12 3, c 3 2] = .liajlih ∧
    sortFadla [c 0 1, c 5 3, c 23 0, c 1 3, c 23 0, c 25 3] qumtu = .liajlih ∧
    sortFadla [c 15 0, c 10 3, c 2 0, c 25 3] darabtu = .mutlaqF ∧
    sortFadla [c 10 0, c 1 3, c 18 1, c 2 0, c 25 3] qumtu = .hal ∧
    sortFadla [c 24 2, c 5 3, c 3 0, c 26 1, c 8 0, c 25 3] qumtu = .hal := by decide

/-- المفعولُ معه: واوٌ متّصلةٌ فنصب. -/
def maiyya (w : List SCell) : List SCell := c 27 0 :: Nawasikh.nasb w

theorem maiyya_licensed (w : List SCell) (hw : licensed w = true)
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) : licensed (maiyya w) = true :=
  Rawabit.proclitic_keeps_licence _ 0 (by decide) _ (Nawasikh.nasb_licensed w hw hlast)

/-- الواوُ خانةٌ واحدةٌ للعطف والمعيّة (`Huruf.shared_cells`): الفرزُ من الفعل — المشاركةُ على تَفَاعَلَ
(القالبُ 15) عطفٌ؛ وما سواه معجم. -/
def tafaala (v : List SCell) : Bool := Sarf.onTemplate (Sarf.templ 15) v

theorem tafaala_is_ataf :
    tafaala [c 3 0, c 7 0, c 1 3, c 14 0, c 24 0] = true ∧        -- تَخَاصَمَ
    tafaala [c 12 0, c 1 3, c 10 0] = false ∧                      -- سَارَ
    maiyya [c 0 0, c 25 3, c 25 0, c 26 3, c 10 2] = [c 27 0, c 0 0, c 25 3, c 25 0, c 26 3, c 10 0] := by
  decide  -- سِرْتُ وَالنَّهْرَ

/-- المفعولُ المطلق: مصدرُ الفعل بجذره بعينه، منصوبًا منوَّنًا؛ الجذرُ يُستردّ منه لكلّ جذر. -/
def mutlaq (k : Nat) (r : Wazn.Root) : List SCell := maful (Wazn.fill (Sarf.templ k) r)

theorem mutlaq_shares_root (r : Wazn.Root) :
    (∀ i, Wazn.rootOf (Sarf.templ 29) (Wazn.fill (Sarf.templ 29) r) i = some (r i)) ∧
    mutlaq 29 (fun i => if i = 0 then 15 else if i = 1 then 10 else 2) =
      [c 15 0, c 10 3, c 2 0, c 25 3] := by                                   -- ضَرْبًا
  exact ⟨Wazn.rootOf_fill _ (by decide) r, by decide⟩

end Slge.Filiyya
