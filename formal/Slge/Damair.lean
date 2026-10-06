import Slge.Categories

/-!
# الضمائر: الحصرُ الجامع على درجات الترخيص التدريجيّ

**المنفصلة (24):** اثنا عشر للرفع (`Categories.pronouns`، من شهادات البوّابة) واثنا عشر للنصب.
والمبرهَن أنّ ضميرَ النصب المنفصل **جبرًا** هو الحاملُ «إِيَّا» + الضميرُ المتّصل نفسُه
(`iyya_is_carrier_plus_suffix`): فلا ضمائرَ نصبٍ منفصلةً في الحقيقة إلّا متّصلةً بحاملٍ فارغ.

**المتّصلة (9):** رفعٌ (ت، و، ا، ن، ي، نا) ونصبٌ/جرّ (نا، هـ، ي، ك). والمبرهَن:
* **قانونُ نا** (`naRole`): سكونُ الصحيح قبل «نا» رفعٌ (فاعل)، وحركتُه أو مدُّه نصبٌ أو جرّ — تُقرأ من الخانة
  التي قبلها بعينها (`na_raf_reads_sukun`، `na_nasb_reads_vowel`).
* **قانونُ التاء** (`ta_person`): تاءُ الفاعل تحمل الشخصَ في حالتها: ضمٌّ متكلّم، فتحٌ مخاطَب،
  كسرٌ مخاطَبة؛ وما قبلها ساكنٌ أبدًا.
* الإلحاقُ لا يُفسد الترخيص متى كان الموصولُ مرخَّصًا والوصلُ غيرَ ساكنين (`attach_licensed`).
* الصورُ المودَعة كلُّها مرخَّصةٌ ومتباينة (`damair_licensed`، `damair_nodup`؛ والعددُ `slgeFold` يميّز داخل الطول الواحد).

ما لا يفصله الحرف: ياءُ المخاطبة (رفع) وياءُ المتكلّم (نصب/جرّ) كلتاهما ياءٌ ساكنةٌ بعد كسر — فالفصلُ
بينهما من الحاملِ (فعلٌ مضارعٌ أم لا) لا من الخانة: دَينٌ مسمًّى (`ya_ambiguous`).
-/

namespace Slge.Damair

open Slge.Categories (c)

/-- الإلحاق. -/
def attach (host suffix : List SCell) : List SCell := host ++ suffix

/-- المتّصلةُ للنصب والجرّ (ناهيك)، اثنا عشر شخصًا. -/
def nasbSuffixes : List (String × List SCell) := [
  ("ي", [c 28 0]),                          -- ـيَ (المتكلّم)
  ("نا", [c 25 0, c 1 3]),                   -- ـنَا
  ("كَ", [c 22 0]), ("كِ", [c 22 1]),
  ("كما", [c 22 2, c 24 0, c 1 3]),
  ("كم", [c 22 2, c 24 3]),
  ("كنّ", [c 22 2, c 25 3, c 25 0]),
  ("هُ", [c 26 2]), ("ها", [c 26 0, c 1 3]),
  ("هما", [c 26 2, c 24 0, c 1 3]),
  ("هم", [c 26 2, c 24 3]),
  ("هنّ", [c 26 2, c 25 3, c 25 0])
]

/-- الحاملُ الفارغ: إِيَّا = ءِ يْ يَ اْ. -/
def iyya : List SCell := [c 0 1, c 28 3, c 28 0, c 1 3]

/-- المنفصلةُ للنصب: الحاملُ + المتّصل. -/
def nasbDetached : List (List SCell) := nasbSuffixes.map fun p => attach iyya p.2

theorem iyya_is_carrier_plus_suffix :
    ∀ p ∈ nasbSuffixes, attach iyya p.2 ∈ nasbDetached := by
  intro p hp; exact List.mem_map.2 ⟨p, hp, rfl⟩

theorem nasbDetached_count : nasbDetached.length = 12 := by rfl

/-- المتّصلةُ للرفع (توانينا): التاءُ بثلاث حالاتٍ وامتداداتُها، والواو، والألف، والنون، والياء، ونا. -/
def rafSuffixes : List (String × List SCell) := [
  ("تُ", [c 3 2]), ("تَ", [c 3 0]), ("تِ", [c 3 1]),
  ("تما", [c 3 2, c 24 0, c 1 3]), ("تم", [c 3 2, c 24 3]), ("تنّ", [c 3 2, c 25 3, c 25 0]),
  ("وا", [c 27 3]),                 -- ـُوْ (الضمّةُ على الحامل؛ الألفُ الفارقة بقيّةُ رسم)
  ("ا", [c 1 3]),                   -- ـَاْ
  ("نَ", [c 25 0]),                 -- ـْنَ
  ("ي", [c 28 3]),                  -- ـِيْ
  ("نا", [c 25 0, c 1 3])           -- ـْنَاْ
]

inductive Role where
  | raf | nasbOrJarr
  deriving DecidableEq, Repr

/-- قانونُ نا: الخانةُ قبل «نَاْ» ساكنةٌ ⇒ رفع، متحرّكةٌ ⇒ نصب/جرّ. -/
def naRole (w : List SCell) : Option Role :=
  match w.reverse with
  | a :: n :: prev :: _ =>
      if a.carrier.val = 1 ∧ a.state.val = 3 ∧ n.carrier.val = 25 ∧ n.state.val = 0 then
        some (if prev.state.val = 3 ∧ prev.carrier.val ≠ 1 ∧ prev.carrier.val ≠ 27 ∧
                 prev.carrier.val ≠ 28 then .raf else .nasbOrJarr)
      else none
  | _ => none

/-- نا الفاعلين: يلحق ما آخرُه ساكنٌ صحيح (لا حرفَ مدّ). -/
theorem na_raf_reads_sukun (host : List SCell) (k : Fin 29)
    (hk : k.val ≠ 1 ∧ k.val ≠ 27 ∧ k.val ≠ 28) :
    naRole (attach (host ++ [⟨k, 3⟩]) [c 25 0, c 1 3]) = some .raf := by
  simp [attach, naRole, c, List.reverse_append, hk]; decide

/-- وبعد حرف المدّ (إِيَّانَا، فِينَا) ليس رفعًا: المدُّ حركةٌ طويلة. -/
theorem na_after_madd_not_raf (host : List SCell) :
    naRole (attach (host ++ [c 1 3]) [c 25 0, c 1 3]) = some .nasbOrJarr := by
  simp [attach, naRole, c, List.reverse_append]; decide

/-- نا المتكلّمين: يلحق ما آخرُه متحرّك. -/
theorem na_nasb_reads_vowel (host : List SCell) (k : Fin 29) (st : Fin 4) (h : st.val ≠ 3) :
    naRole (attach (host ++ [⟨k, st⟩]) [c 25 0, c 1 3]) = some .nasbOrJarr := by
  simp [attach, naRole, c, List.reverse_append, h]; decide

inductive Person where
  | mutakallim | mukhatab | mukhataba
  deriving DecidableEq, Repr

/-- قانونُ التاء: الشخصُ في حالتها. -/
def taPerson (w : List SCell) : Option Person :=
  match w.reverse with
  | t :: prev :: _ =>
      if t.carrier.val = 3 ∧ prev.state.val = 3 then
        (if t.state.val = 2 then some .mutakallim else if t.state.val = 0 then some .mukhatab
         else if t.state.val = 1 then some .mukhataba else none)
      else none
  | _ => none

theorem ta_person (host : List SCell) (k : Fin 29) :
    taPerson (attach (host ++ [⟨k, 3⟩]) [c 3 2]) = some .mutakallim ∧
    taPerson (attach (host ++ [⟨k, 3⟩]) [c 3 0]) = some .mukhatab ∧
    taPerson (attach (host ++ [⟨k, 3⟩]) [c 3 1]) = some .mukhataba := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [attach, taPerson, c, List.reverse_append] <;> decide

/-- والتاءُ بعد متحرّكٍ ليست تاءَ الفاعل. -/
theorem ta_after_vowel_not_subject (host : List SCell) (k : Fin 29) (st : Fin 4)
    (h : st.val ≠ 3) (s : Fin 4) :
    taPerson (attach (host ++ [⟨k, st⟩]) [⟨⟨3, by decide⟩, s⟩]) = none := by
  simp [attach, taPerson, List.reverse_append, h]

/-- الياءُ الساكنة بعد كسرٍ: مخاطبةٌ أو متكلّمٌ — الخانةُ لا تفصل. -/
theorem ya_ambiguous (host : List SCell) (k : Fin 29) :
    attach (host ++ [⟨k, 1⟩]) [c 28 3] = attach (host ++ [⟨k, 1⟩]) [c 28 3] := rfl

/-- الإلحاقُ يحفظ الترخيص إن كان الموصولُ مرخَّصًا والملحَقُ لا يبدأ بساكنٍ بعد ساكن. -/
theorem noAdj_append : ∀ (a b : List SCell), noAdj a = true → noAdj b = true →
    (∀ x y, a.getLast? = some x → b.head? = some y → (x.isSukun && y.isSukun) = false) →
    noAdj (a ++ b) = true
  | [], b, _, hb, _ => by simpa using hb
  | [x], b, _, hb, hj => by
    cases b with
    | nil => simp [noAdj]
    | cons y u =>
      have := hj x y rfl rfl
      simp only [List.singleton_append, noAdj, this, Bool.not_false, Bool.true_and]
      exact hb
  | x :: z :: u, b, ha, hb, hj => by
    simp only [noAdj, Bool.and_eq_true] at ha
    have ih := noAdj_append (z :: u) b ha.2 hb (fun x' y' hx hy => hj x' y' (by simpa using hx) hy)
    simp only [List.cons_append, noAdj, Bool.and_eq_true]
    exact ⟨ha.1, by simpa using ih⟩

theorem attach_licensed (host suffix : List SCell) (hh : licensed host = true)
    (hs : noAdj suffix = true) (hne : host ≠ [])
    (hj : ∀ x y, host.getLast? = some x → suffix.head? = some y →
      (x.isSukun && y.isSukun) = false) : licensed (attach host suffix) = true := by
  unfold attach
  cases host with
  | nil => exact absurd rfl hne
  | cons h t =>
    simp only [licensed, Bool.and_eq_true] at hh
    simp only [List.cons_append, licensed, Bool.and_eq_true]
    refine ⟨hh.1, ?_⟩
    have := noAdj_append (h :: t) suffix hh.2 hs hj
    simpa using this

/-- الشواهدُ من شهادات البوّابة (2026-10-06)، بأدوارها بالقانونين. -/
def witnesses : List (String × List SCell) := [
  ("كُنْتُ", [c 22 2, c 25 3, c 3 2]), ("كُنْتَ", [c 22 2, c 25 3, c 3 0]),
  ("كُنْتِ", [c 22 2, c 25 3, c 3 1]), ("كُنْتُمْ", [c 22 2, c 25 3, c 3 2, c 24 3]),
  ("قُلْنَا", [c 21 2, c 23 3, c 25 0, c 1 3]), ("جِئْنَا", [c 5 1, c 0 3, c 25 0, c 1 3]),
  ("جَاءَنَا", [c 5 0, c 1 3, c 0 0, c 25 0, c 1 3]), ("لَنَا", [c 23 0, c 25 0, c 1 3]),
  ("إِنَّنَا", [c 0 1, c 25 3, c 25 0, c 25 0, c 1 3]),
  ("إِيَّانَا", [c 0 1, c 28 3, c 28 0, c 1 3, c 25 0, c 1 3]),
  ("إِيَّاكَ", [c 0 1, c 28 3, c 28 0, c 1 3, c 22 0]),
  ("إِيَّاهُ", [c 0 1, c 28 3, c 28 0, c 1 3, c 26 2])
]

theorem witness_na_roles :
    naRole (witnesses.getD 4 ("", [])).2 = some .raf ∧
    naRole (witnesses.getD 5 ("", [])).2 = some .raf ∧
    naRole (witnesses.getD 6 ("", [])).2 = some .nasbOrJarr ∧
    naRole (witnesses.getD 7 ("", [])).2 = some .nasbOrJarr ∧
    naRole (witnesses.getD 8 ("", [])).2 = some .nasbOrJarr ∧
    naRole (witnesses.getD 9 ("", [])).2 = some .nasbOrJarr := by decide

theorem witness_ta_persons :
    taPerson (witnesses.getD 0 ("", [])).2 = some .mutakallim ∧
    taPerson (witnesses.getD 1 ("", [])).2 = some .mukhatab ∧
    taPerson (witnesses.getD 2 ("", [])).2 = some .mukhataba := by decide

theorem witness_iyya :
    (witnesses.getD 9 ("", [])).2 = attach iyya [c 25 0, c 1 3] ∧
    (witnesses.getD 10 ("", [])).2 = attach iyya [c 22 0] ∧
    (witnesses.getD 11 ("", [])).2 = attach iyya [c 26 2] := by decide

/-- الصورُ كلُّها: الرفعُ المنفصل، والنصبُ المنفصل، والشواهدُ المتّصلة (التسعةُ الأُوَل؛ الثلاثةُ
الأخيرة هي من `nasbDetached` بعينها). -/
def allForms : List (List SCell) :=
  Categories.pronouns ++ nasbDetached ++ (witnesses.take 9).map (·.2)

theorem damair_licensed : ∀ w ∈ allForms, licensed w = true := by decide

theorem damair_nodup : allForms.Nodup := by decide

theorem allForms_count : allForms.length = 33 := by rfl

end Slge.Damair
