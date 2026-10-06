import Slge.Talil

/-!
# المقام: الشخصُ يُقرأ من خانات الفعل، والمستترُ لا خانةَ له، والظاهرُ للغائب، والتوكيدُ مطابقةُ شخص

* **الشخصُ من الخانة** (د٤): صدرُ المضارع يقرأ الشخص — همزةٌ أو نونٌ متكلّم، ياءٌ غائب، وتاءٌ مخاطبٌ أو غائبة
  (الخانةُ لا تفصل — باسمه): لكلّ قالبِ مضارعٍ ولكلّ جذر (`present_prefix_reads_person`، عامٌّ لا شاهد).
  ولاحقةُ الماضي تقرؤه من جدول `Filiyya.subjectSuffixes` (`shakhsPast`)، والأمرُ مخاطبٌ أبدًا، والماضي
  بلا لاحقةٍ غائب.
* **المستترُ لا خانةَ له**: الفاعلُ المستترُ غيابُ لاحقةٍ لا حضورُها (`Filiyya.hasSubject = false`) والشخصُ
  مقروءٌ مع ذلك من الصدر أو القالب (`mustatir_has_no_cell`). حكمُه: وجوبًا للحاضر (المتكلّم والمخاطب)،
  وجوازًا للغائب (`hadir_wujub`، `ghaib_jawaz`) — فالغائبُ **يستتر** لكن جوازًا، وما في الحصر المُرسَل من
  «حظر استتار الغائب» خلافُ النحو: هُوَ مستترٌ جوازًا في فَعَلَ ويَفْعَلُ.
* **الظاهرُ للغائب وحدَه** (د٨): الفاعلُ الاسمُ الظاهر لا يقع بعد فعلِ متكلّمٍ أو مخاطب (`zahir_only_ghaib`)؛
  والمتّصلُ لكلّ شخص، والمستترُ لكلّ شخصٍ بحكمه (`valid`).
* **التوكيدُ اللفظيّ**: المنفصلُ بعد المتّصل أو المستتر مطابقةُ شخص (`tawkid`): ضَرَبْتُ أَنَا، أَدْرُسُ أَنَا،
  دَرَسَ هُوَ؛ وضَرَبْتُ أَنْتَ لا (`tawkid_witnesses`). ولكلّ منفصلٍ في الجدول شخصٌ (`detached_all_read`)،
  ولا توكيدَ إلّا بمنفصلٍ من الجدول وفعلٍ قُرئ شخصُه (`tawkid_needs_both`).
* **عودُ الغائب**: الضميرُ العائدُ في الفاعل يفرض تقديمَ المفعول (`Filiyya.order`؛ `aid_forces_maful_first`) —
  الغائبُ يحتاج ما يعود عليه لفظًا ورتبة؛ وما سوى ذلك من المقام (الحضورُ والشهود) معنًى — معلَن.
القياسُ على MASAQ في بايثون: وسومُ السوابق واللواحق التي تحمل الشخص، والفاعلُ الظاهرُ بعد الفعل.
الحصرُ المُرسَل: أنواعُه (`Person`، `SubjectManifestation`) مكتوبةٌ باليد لا على خانة، وفحصُ إجهاده يقارن
الدالّةَ بنفسها (`assert f(x) == f(x)`) — لم يُدخَل منه شيء، ودخل معناه على الخانات مصحَّحًا.
-/

namespace Slge.Maqam

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## الشخص -/

inductive Shakhs where
  | mutakallim | mukhatab | ghaib | mukhatabOrGhaiba   -- الأخير: صدرُ التاء لا يفصل
  deriving DecidableEq, Repr

def presentTemplates : List Nat := [4, 5, 6, 7, 20, 21, 22, 23, 24, 25, 26, 27, 28]

/-- إبدالُ حامل الصدر بحالته. -/
def withPrefix (k : Fin 29) : List SCell → List SCell
  | [] => []
  | x :: t => ⟨k, x.state⟩ :: t

/-- على القالب وأصلُه بلا ألف: الألفُ ليست أصلًا (آمَنَ لا يُقرأ على يَفْعَلُ بأصلٍ أوّلُه ألف). -/
def onTemplateRoot (k : Nat) (u : List SCell) : Bool :=
  Sarf.onTemplate (Sarf.templ k) u &&
    ([0, 1, 2] : List (Fin 3)).all fun i => (Wazn.rootOf (Sarf.templ k) u i).map (·.val) != some 1

/-- مضارعٌ مجرّدٌ من اللواحق: على قالبٍ من قوالبه بعد ردِّ صدره ياءً. -/
def isPresent (v : List SCell) : Bool := presentTemplates.any fun k => onTemplateRoot k (withPrefix 28 v)

/-- قارئُ الصدر: شخصُ المضارع من حامله الأوّل. -/
def shakhsPresent (v : List SCell) : Option Shakhs :=
  if isPresent v then
    match v.head?.map (·.carrier.val) with
    | some 0 => some .mutakallim
    | some 25 => some .mutakallim
    | some 3 => some .mukhatabOrGhaiba
    | some 28 => some .ghaib
    | _ => none
  else none

/-- شخصُ لاحقة الماضي بترتيب الجدول: تُ ونا متكلّم؛ تَ تِ تما تم تنّ وي وين مخاطب؛ وا ا نَ ون ان غائب. -/
def suffixShakhs : List Shakhs :=
  [.mutakallim, .mukhatab, .mukhatab, .mukhatab, .mukhatab, .mukhatab, .ghaib, .ghaib, .ghaib, .mukhatab,
   .mutakallim, .ghaib, .mukhatab, .ghaib]

theorem suffixShakhs_covers : suffixShakhs.length = Filiyya.subjectSuffixes.length := by decide

def pastTemplates : List Nat := [0, 1, 2, 3] ++ Fil.mazid

/-- جذعُ فعلٍ قبل لاحقة: ماضٍ بفتح الآخر، أو أمرٌ بسكونه، أو مضارعٌ بضمّه بعد ردّ الصدر، أو أجوفٌ محذوفُ
العين (قُمْ، بِعْ: حرفان ساكنُ الآخر). -/
def verbStem (b : List SCell) : Bool :=
  (b.length == 2 && b.getLast?.map SCell.isSukun == some true) ||
  pastTemplates.any (fun k => onTemplateRoot k (setLast b 0)) ||
  Filiyya.amrTemplates.any (fun k => onTemplateRoot k (setLast b 3)) ||
  isPresent (setLast b 2)

/-- شخصُ اللاحقة: المضارعُ بلاحقةٍ (تَفْعَلُونَ، يَفْعَلُونَ) صدرُه يفصل؛ وإلّا الجدول. -/
def shakhsSuffix (v : List SCell) : Option Shakhs :=
  match (Filiyya.subjectSuffixes.zip suffixShakhs).find?
      (fun p => Filiyya.endsWithState v p.1.1 p.1.2 && verbStem (v.take (v.length - p.1.1.length))) with
  | some p =>
      let b := v.take (v.length - p.1.1.length)
      if isPresent (setLast b 2) then
        match v.head?.map (·.carrier.val) with
        | some 3 => some .mukhatab
        | some 28 => some .ghaib
        | _ => none
      else some p.2
  | none => none

def shakhsPast (v : List SCell) : Option Shakhs :=
  if Filiyya.hasSubject v then none
  else if pastTemplates.any (fun k => onTemplateRoot k v) then some .ghaib
  else if pastTemplates.any (fun k => onTemplateRoot k (Afal.initOf v)) &&
      v.getLast? == some (c 3 3) then some .ghaib                       -- فَعَلَتْ
  else if Filiyya.amrTemplates.any (fun k => onTemplateRoot k v) then some .mukhatab
  else none

/-- الشخصُ من الخانات: اللاحقةُ على جذعِ فعل، وإلّا الصدرُ، وإلّا الماضي بقالبه والأمرُ مخاطب. -/
def shakhs (v : List SCell) : Option Shakhs := ((shakhsSuffix v).or (shakhsPresent v)).or (shakhsPast v)

set_option maxRecDepth 2048 in
theorem present_heads_ya :
    (presentTemplates.all fun k => match (Sarf.templ k).head? with
      | some (.lit x) => x.carrier.val == 28 | _ => false) = true := by decide

theorem present_templates_wf : presentTemplates.all (fun k => decide (Wazn.WF (Sarf.templ k))) = true := by
  decide

theorem withPrefix_fill (k : Nat) (hk : k ∈ presentTemplates) (r : Wazn.Root) (p : Fin 29) :
    withPrefix 28 (withPrefix p (Wazn.fill (Sarf.templ k) r)) = Wazn.fill (Sarf.templ k) r ∧
    (withPrefix p (Wazn.fill (Sarf.templ k) r)).head?.map (·.carrier.val) = some p.val := by
  have h := List.all_eq_true.1 present_heads_ya k hk
  match ht : Sarf.templ k with
  | [] => simp [ht] at h
  | .slot _ _ :: _ => simp [ht] at h
  | .lit x :: rest =>
    simp only [ht, List.head?_cons, beq_iff_eq] at h
    have hx : (⟨28, x.state⟩ : SCell) = x := by
      cases x with
      | mk ca st =>
        cases ca with
        | mk v hv =>
          simp only at h
          subst h
          rfl
    simp only [Wazn.fill, List.map_cons, Wazn.fillSym, withPrefix, Option.map_some, List.head?_cons]
    refine ⟨by rw [hx], ?_⟩
    first | trivial | rfl

/-- صدرُ المضارع يقرأ الشخصَ لكلّ قالبٍ ولكلّ جذرٍ لا ألفَ فيه: همزةٌ ونونٌ متكلّم، تاءٌ مخاطبٌ أو غائبة، ياءٌ غائب. -/
theorem present_prefix_reads_person (k : Nat) (hk : k ∈ presentTemplates) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) :
    shakhsPresent (withPrefix 0 (Wazn.fill (Sarf.templ k) r)) = some .mutakallim ∧
    shakhsPresent (withPrefix 25 (Wazn.fill (Sarf.templ k) r)) = some .mutakallim ∧
    shakhsPresent (withPrefix 3 (Wazn.fill (Sarf.templ k) r)) = some .mukhatabOrGhaiba ∧
    shakhsPresent (withPrefix 28 (Wazn.fill (Sarf.templ k) r)) = some .ghaib := by
  have hwf : Wazn.WF (Sarf.templ k) := of_decide_eq_true (List.all_eq_true.1 present_templates_wf k hk)
  have hon := Sarf.onTemplate_fill (Sarf.templ k) hwf r
  have key : ∀ p : Fin 29, isPresent (withPrefix p (Wazn.fill (Sarf.templ k) r)) = true := by
    intro p
    obtain ⟨h1, _⟩ := withPrefix_fill k hk r p
    unfold isPresent
    refine List.any_eq_true.2 ⟨k, hk, ?_⟩
    rw [h1]
    simp only [onTemplateRoot, hon, Bool.true_and]
    refine List.all_eq_true.2 fun i _ => ?_
    rw [Wazn.rootOf_fill (Sarf.templ k) hwf r i]
    simpa using hr i
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp only [shakhsPresent, key 0, ite_true, (withPrefix_fill k hk r 0).2]; decide
  · simp only [shakhsPresent, key 25, ite_true, (withPrefix_fill k hk r 25).2]; decide
  · simp only [shakhsPresent, key 3, ite_true, (withPrefix_fill k hk r 3).2]; decide
  · simp only [shakhsPresent, key 28, ite_true, (withPrefix_fill k hk r 28).2]; decide

/-! ## الاستتارُ والظهور -/

inductive Zuhur where
  | zahir | mustatir | muttasil
  deriving DecidableEq, Repr

inductive Hukm where
  | wujub | jawaz
  deriving DecidableEq, Repr

/-- حكمُ الاستتار: وجوبًا للحاضر، جوازًا للغائب؛ وتاءُ المضارع لا تفصل. -/
def hukmIstitar : Shakhs → Option Hukm
  | .mutakallim => some .wujub
  | .mukhatab => some .wujub
  | .ghaib => some .jawaz
  | .mukhatabOrGhaiba => none

theorem hadir_wujub : hukmIstitar .mutakallim = some .wujub ∧ hukmIstitar .mukhatab = some .wujub :=
  ⟨rfl, rfl⟩
theorem ghaib_jawaz : hukmIstitar .ghaib = some .jawaz := rfl

/-- الظهورُ الجائز للشخص: الاسمُ الظاهر للغائب (أو تاءِ الغائبة)، والمتّصلُ والمستترُ لكلّ شخص. -/
def valid (s : Shakhs) : Zuhur → Bool
  | .zahir => s == .ghaib || s == .mukhatabOrGhaiba
  | .muttasil => true
  | .mustatir => true

theorem zahir_only_ghaib (s : Shakhs) :
    valid s .zahir = true ↔ (s = .ghaib ∨ s = .mukhatabOrGhaiba) := by
  cases s <;> simp [valid]

theorem zahir_not_hadir : valid .mutakallim .zahir = false ∧ valid .mukhatab .zahir = false := ⟨rfl, rfl⟩

/-- الظهورُ من الخانات: لاحقةُ فاعلٍ ⇒ متّصل؛ وإلّا فاعلٌ ظاهرٌ بعده أو مستتر (الحدُّ من الكلمة التالية). -/
def zuhur (v : List SCell) (next : Option (List SCell)) : Zuhur :=
  if Filiyya.hasSubject v then .muttasil
  else match next with
    | some n => if Tawabi.caseClass n == .raf then .zahir else .mustatir
    | none => .mustatir

def adrusu : List SCell := [c 0 0, c 8 3, c 10 2, c 12 2]        -- أَدْرُسُ
def nadrusu : List SCell := [c 25 0, c 8 3, c 10 2, c 12 2]      -- نَدْرُسُ
def tadrusu : List SCell := [c 3 0, c 8 3, c 10 2, c 12 2]       -- تَدْرُسُ
def yadrusu : List SCell := [c 28 0, c 8 3, c 10 2, c 12 2]      -- يَدْرُسُ
def darasat : List SCell := [c 8 0, c 10 0, c 12 0, c 3 3]       -- دَرَسَتْ
def udrus : List SCell := [c 0 2, c 8 3, c 10 2, c 12 3]         -- اُدْرُسْ

/-- المستترُ لا خانةَ له: أَدْرُسُ ودَرَسَ ويَدْرُسُ بلا لاحقةِ فاعلٍ، وشخصُها مقروء؛ وضَرَبْتُ لاحقتُه خانة. -/
theorem mustatir_has_no_cell :
    Filiyya.hasSubject adrusu = false ∧ shakhs adrusu = some .mutakallim ∧
    Filiyya.hasSubject Jumla.darasa = false ∧ shakhs Jumla.darasa = some .ghaib ∧
    Filiyya.hasSubject yadrusu = false ∧ shakhs yadrusu = some .ghaib ∧
    Filiyya.hasSubject Filiyya.darabtu = true ∧ shakhs Filiyya.darabtu = some .mutakallim := by decide

/-- الشخصُ على الشواهد: نَدْرُسُ متكلّم، تَدْرُسُ لا تفصل، دَرَسَتْ غائب، اُدْرُسْ مخاطب، قُمْتُ متكلّم، وزَيْدٌ لا يُقرأ. -/
theorem shakhs_witnesses :
    shakhs nadrusu = some .mutakallim ∧ shakhs tadrusu = some .mukhatabOrGhaiba ∧
    shakhs darasat = some .ghaib ∧ shakhs udrus = some .mukhatab ∧ shakhs Filiyya.qumtu = some .mutakallim ∧
    shakhs Jumla.zayd = none := by decide

/-- الظهورُ على الشواهد: دَرَسَ زَيْدٌ ظاهرٌ (غائب: جائز)، أَدْرُسُ زَيْدٌ ظاهرٌ بعد متكلّم (ممنوع)،
دَرَسَ الدَّرْسَ مستتر، ضَرَبْتُ متّصل. -/
theorem zuhur_witnesses :
    zuhur Jumla.darasa (some Jumla.zayd) = .zahir ∧ valid .ghaib .zahir = true ∧
    zuhur adrusu (some Jumla.zayd) = .zahir ∧ valid .mutakallim .zahir = false ∧
    zuhur Jumla.darasa (some Filiyya.addars) = .mustatir ∧ zuhur Filiyya.darabtu none = .muttasil := by
  decide

/-! ## التوكيدُ اللفظيّ -/

/-- شخصُ المنفصل بترتيب جدول `Categories.pronouns`: الأوّلان متكلّم، ثمّ خمسةٌ مخاطب، ثمّ خمسةٌ غائب. -/
def detachedTable : List Shakhs :=
  [.mutakallim, .mutakallim, .mukhatab, .mukhatab, .mukhatab, .mukhatab, .mukhatab,
   .ghaib, .ghaib, .ghaib, .ghaib, .ghaib]

def shakhsDetached (d : List SCell) : Option Shakhs :=
  ((Categories.pronouns.zip detachedTable).find? (·.1 == d)).map (·.2)

theorem detached_all_read : Categories.pronouns.all (fun d => (shakhsDetached d).isSome) = true := by decide

/-- مطابقةُ الشخص: تاءُ المضارع تطابق المخاطبَ والغائب. -/
def same : Shakhs → Shakhs → Bool
  | .mukhatabOrGhaiba, .mukhatab => true
  | .mukhatabOrGhaiba, .ghaib => true
  | a, b => a == b

/-- التوكيدُ اللفظيّ للضمير: منفصلٌ بعد الفعل يطابق شخصَه. -/
def tawkid (v d : List SCell) : Bool :=
  match shakhs v, shakhsDetached d with
  | some a, some b => same a b
  | _, _ => false

theorem detached_mem (d : List SCell) (h : (shakhsDetached d).isSome = true) : d ∈ Categories.pronouns := by
  unfold shakhsDetached at h
  cases hf : (Categories.pronouns.zip detachedTable).find? (·.1 == d) with
  | none => simp [hf] at h
  | some x =>
    have h1 := List.find?_some hf
    have h2 := List.mem_of_find?_eq_some hf
    simp only [beq_iff_eq] at h1
    exact h1 ▸ (List.of_mem_zip h2).1

theorem tawkid_needs_both (v d : List SCell) (h : tawkid v d = true) :
    (shakhs v).isSome ∧ d ∈ Categories.pronouns := by
  unfold tawkid at h
  cases hs : shakhs v with
  | none => simp [hs] at h
  | some a =>
    cases hd : shakhsDetached d with
    | none => simp [hs, hd] at h
    | some b => exact ⟨rfl, detached_mem d (by simp [hd])⟩

def ana : List SCell := [c 0 0, c 25 0, c 1 3]
def anta : List SCell := [c 0 0, c 25 3, c 3 0]
def huwa : List SCell := [c 26 2, c 27 0]
def hiya : List SCell := [c 26 1, c 28 0]

/-- ضَرَبْتُ أَنَا، أَدْرُسُ أَنَا، دَرَسَ هُوَ، تَدْرُسُ أَنْتَ، تَدْرُسُ هِيَ توكيد؛ ضَرَبْتُ أَنْتَ وأَدْرُسُ هُوَ لا. -/
theorem tawkid_witnesses :
    tawkid Filiyya.darabtu ana = true ∧ tawkid adrusu ana = true ∧ tawkid Jumla.darasa huwa = true ∧
    tawkid tadrusu anta = true ∧ tawkid tadrusu hiya = true ∧
    tawkid Filiyya.darabtu anta = false ∧ tawkid adrusu huwa = false ∧
    tawkid Jumla.darasa Jumla.zayd = false := by decide

/-! ## عودُ الغائب -/

/-- الضميرُ العائدُ في الفاعل يفرض تقديمَ المفعول: الغائبُ يحتاج ما يعود عليه لفظًا ورتبة. -/
theorem aid_forces_maful_first (v f m : List SCell) (hm : Jumla.istifham m = false)
    (hs : Filiyya.hasSubject v = false) (ho : Filiyya.hasObject v = false)
    (ha : Jumla.hasAidPronoun f = true) :
    Filiyya.order ⟨v, f, m, .FOS⟩ = .mafulFirst := by
  simp [Filiyya.order, hm, hs, ho, ha]

end Slge.Maqam
