import Slge.Adad

/-!
# المعارف: التعريفُ عمليّاتٌ على الخانات، والنكرةُ ما بقي

السبعةُ في الحصر ثلاثةُ أصنافٍ على الخانات:
* **بالذات** (الضمير، الإشارة، الموصول): جداولُ صورٍ مودَعة (`Categories.pronouns`، `Ishara.forms`،
  `mawsul`)؛ والعلمُ معجمٌ لا خانة.
* **بالأداة**: `al` تدخل همزةً مفتوحةً فلامًا ساكنة، ثمّ **الشمسيّة** تُدغم اللامَ في أربعةَ عشرَ
  حرفًا (`shamsi`) كما تُخرجها البوّابة (الرَّحْمَنِ = ءَ رْ رَ…). المبرهَن: الإدغامُ يحفظ الترخيص
  (`shamsi_licensed`، لأنّه لا يغيّر نمطَ السكون)، والتعريفُ بأل يحفظ الترخيص (`al_licensed`)،
  والأداةُ تُقرأ من الصدر (`hasAl_al`).
* **بالتبعية**: الإضافةُ تُسقط التنوينَ ثمّ تُلحق (`idafa`): إسقاطُ التنوين يحفظ الترخيص
  (`dropTanwin_licensed`)، والمضافُ لا تنوينَ له (`idafa_no_tanwin`).

**قانونُ الخانة:** التنوينُ والأداةُ لا يجتمعان، والمضافُ لا يُنوَّن — مقيسٌ على MASAQ في بايثون؛
والاستثناءُ المسمّى **تنوينُ العوض** (يَوْمَئِذٍ، كُلٍّ). أمّا العلمُ فيُنوَّن إن انصرف (مُحَمَّدٌ): فالتنوينُ
ليس علامةَ تنكير.

والقوّةُ (الضمير فالعلم فالإشارة…) ترتيبٌ معلَن لا خانة. والمستترُ بلا خانة.
-/

namespace Slge.Marifa

open Slge.Categories (c)

/-- الحروفُ الشمسيّة. -/
def sun : List Nat := [3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 23, 25]

/-- الإدغامُ الشمسيّ: لامٌ ساكنةٌ قبل شمسيٍّ تصير ذلك الحرفَ ساكنًا. -/
def shamsi : List SCell → List SCell
  | a :: l :: x :: t =>
      if l.carrier.val = 23 ∧ l.state.val = 3 ∧ sun.contains x.carrier.val then
        a :: ⟨x.carrier, l.state⟩ :: x :: t
      else a :: l :: x :: t
  | w => w

theorem shamsi_map_isSukun : ∀ w : List SCell, (shamsi w).map SCell.isSukun = w.map SCell.isSukun
  | a :: l :: x :: t => by
    show (if l.carrier.val = 23 ∧ l.state.val = 3 ∧ sun.contains x.carrier.val then
            a :: ⟨x.carrier, l.state⟩ :: x :: t else a :: l :: x :: t).map SCell.isSukun = _
    split <;> simp [SCell.isSukun]
  | [] => rfl
  | [_] => rfl
  | [_, _] => rfl

theorem shamsi_licensed (w : List SCell) : licensed (shamsi w) = licensed w :=
  Zuruf.licensed_of_map_isSukun _ _ (shamsi_map_isSukun w)

/-- التعريفُ بأل: همزةٌ مفتوحة (ألفُ الوصل بقيّةُ رسم) ولامٌ ساكنة، ثمّ الإدغامُ الشمسيّ. -/
def al (w : List SCell) : List SCell := shamsi (c 0 0 :: c 23 3 :: w)

theorem al_licensed (w : List SCell) (hw : licensed w = true) : licensed (al w) = true := by
  unfold al; rw [shamsi_licensed]
  cases w with
  | nil => rfl
  | cons x t =>
    simp only [licensed, Bool.and_eq_true] at hw
    have h1 : x.state.val ≠ 3 := by
      intro h3
      have : x.isSukun = true := by simp [SCell.isSukun, h3]
      rw [this] at hw; exact absurd hw.1 (by decide)
    show (!(c 0 0).isSukun && noAdj (c 0 0 :: c 23 3 :: x :: t)) = true
    simp [noAdj, SCell.isSukun, c, h1, hw.2]

/-- الأداةُ تُقرأ من الصدر: همزةٌ مفتوحةٌ ثمّ لامٌ ساكنة أو حرفٌ شمسيٌّ ساكنٌ يليه مثلُه. -/
def hasAl (w : List SCell) : Bool :=
  match w with
  | a :: l :: x :: _ =>
      a.carrier.val == 0 && a.state.val == 0 && l.state.val == 3 &&
        (l.carrier.val == 23 || (sun.contains l.carrier.val && l.carrier == x.carrier))
  | [a, l] => a.carrier.val == 0 && a.state.val == 0 && l.carrier.val == 23 && l.state.val == 3
  | _ => false

theorem hasAl_al (w : List SCell) (hne : w ≠ []) : hasAl (al w) = true := by
  unfold al shamsi
  cases w with
  | nil => exact absurd rfl hne
  | cons x t =>
    simp only [c]
    split
    · rename_i h
      have hm : x.carrier.val ∈ sun := List.contains_iff_mem.1 h.2.2
      simp [hasAl, hm]
    · simp [hasAl]

/-- التنوين: حركةٌ فنونٌ ساكنة. -/
def dropTanwin (w : List SCell) : List SCell := if Nida.hasTanwin w then Afal.initOf w else w

theorem licensed_initOf : ∀ w : List SCell, licensed w = true → licensed (Afal.initOf w) = true
  | [], _ => rfl
  | [_], _ => rfl
  | x :: y :: t, h => by
    show licensed (x :: Afal.initOf (y :: t)) = true
    simp only [licensed, Bool.and_eq_true] at h ⊢
    refine ⟨h.1, ?_⟩
    have hn : ∀ (a : SCell) (l : List SCell), noAdj (a :: l) = true → noAdj (a :: Afal.initOf l) = true := by
      intro a l
      induction l generalizing a with
      | nil => intro _; rfl
      | cons b u ih =>
        intro hb
        cases u with
        | nil => rfl
        | cons d v =>
          show noAdj (a :: b :: Afal.initOf (d :: v)) = true
          have hb' : (!(a.isSukun && b.isSukun) && noAdj (b :: d :: v)) = true := hb
          have hp : (!(a.isSukun && b.isSukun)) = true ∧ noAdj (b :: d :: v) = true := by
            simpa only [Bool.and_eq_true] using hb'
          have ih' := ih b hp.2
          cases hi : Afal.initOf (d :: v) with
          | nil => show (!(a.isSukun && b.isSukun) && noAdj [b]) = true; simp [noAdj, hp.1]
          | cons e u =>
            rw [hi] at ih'
            show (!(a.isSukun && b.isSukun) && noAdj (b :: e :: u)) = true
            simp [hp.1, ih']
    exact hn x (y :: t) h.2

theorem dropTanwin_licensed (w : List SCell) (h : licensed w = true) :
    licensed (dropTanwin w) = true := by
  unfold dropTanwin; split
  · exact licensed_initOf w h
  · exact h

/-- الإضافة: إسقاطُ التنوين ثمّ الإلحاقُ بالمضاف إليه (ضميرًا أو كلمةً تاليةً في التيار). -/
def idafa (w suffix : List SCell) : List SCell := dropTanwin w ++ suffix

theorem v24 : ((24 : Fin 29).val = 24) := rfl
theorem v26 : ((26 : Fin 29).val = 26) := rfl

/-- المضافُ إلى ضميرٍ لا تنوينَ له: آخرُه الضميرُ لا النون. -/
theorem idafa_no_tanwin (w : List SCell) (p : List SCell)
    (hp : p ∈ Damair.nasbSuffixes.map (·.2)) : Nida.hasTanwin (idafa w p) = false := by
  unfold idafa
  generalize dropTanwin w = l
  simp only [Damair.nasbSuffixes, List.map, List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    (unfold Nida.hasTanwin; rw [List.reverse_append];
     cases hl : l.reverse <;> simp [c, Ishara.v25, Ishara.s3, Ishara.v22, Ishara.v28, v24, v26])

/-- الأسماءُ الموصولة. -/
def mawsul : List (String × List SCell) := [
  ("الَّذِي", [c 0 0, c 23 3, c 23 0, c 9 1, c 28 3]),
  ("الَّتِي", [c 0 0, c 23 3, c 23 0, c 3 1, c 28 3]),
  ("اللَّذَانِ", [c 0 0, c 23 3, c 23 0, c 9 0, c 1 3, c 25 1]),
  ("اللَّتَانِ", [c 0 0, c 23 3, c 23 0, c 3 0, c 1 3, c 25 1]),
  ("اللَّذَيْنِ", [c 0 0, c 23 3, c 23 0, c 9 0, c 28 3, c 25 1]),
  ("اللَّتَيْنِ", [c 0 0, c 23 3, c 23 0, c 3 0, c 28 3, c 25 1]),
  ("الَّذِينَ", [c 0 0, c 23 3, c 23 0, c 9 1, c 28 3, c 25 0]),
  ("اللَّاتِي", [c 0 0, c 23 3, c 23 0, c 1 3, c 3 1, c 28 3]),
  ("اللَّائِي", [c 0 0, c 23 3, c 23 0, c 1 3, c 0 1, c 28 3]),
  ("اللَّوَاتِي", [c 0 0, c 23 3, c 23 0, c 27 0, c 1 3, c 3 1, c 28 3]),
  ("مَنْ", Istifham.man), ("مَا", Istifham.ma), ("أَيُّ", Istifham.ayy 2), ("ذُو", [c 9 2, c 27 3])
]

theorem mawsul_licensed : mawsul.all (fun p => licensed p.2) = true := by decide
theorem mawsul_nodup : (mawsul.map (·.2)).Nodup := by decide

/-- الموصولُ المبدوءُ بأل تقرأ الأداةَ في صدره. -/
theorem mawsul_al : (mawsul.take 10).all (fun p => hasAl p.2) = true := by decide

/-- مثنّى الموصول يُقرأ إعرابُه كالإشارة: من المدّ قبل النون. -/
theorem mawsul_dual_case :
    Ishara.caseOf (mawsul.getD 2 ("", [])).2 = some .raf ∧
    Ishara.caseOf (mawsul.getD 4 ("", [])).2 = some .nasbJarr := by decide

/-- المعرفةُ على الخانات: ما له صورةٌ في جدولٍ، أو أداةٌ في صدره، أو مضافٌ إلى ضمير. -/
inductive Marifa : List SCell → Prop where
  | pronoun (w) (h : w ∈ Categories.pronouns) : Marifa w
  | ishara (w) (h : w ∈ Ishara.forms.map (·.2)) : Marifa w
  | mawsul (w) (h : w ∈ mawsul.map (·.2)) : Marifa w
  | alWord (w) (h : hasAl w = true) : Marifa w
  | mudafToPronoun (w p) (hp : p ∈ Damair.nasbSuffixes.map (·.2)) : Marifa (idafa w p)

theorem al_is_marifa (w : List SCell) (hne : w ≠ []) : Marifa (al w) :=
  .alWord _ (hasAl_al w hne)

theorem mudaf_is_marifa (w : List SCell) : Marifa (idafa w [c 22 0]) :=
  .mudafToPronoun w [c 22 0] (by decide)

/-- المودَعُ بالذات لا تنوينَ فيه — إلّا مَنْ: نونُها أصلٌ ساكنٌ بعد فتحٍ، فالخانةُ تقرؤها كتنوين
(تشابهٌ مسمًّى). -/
theorem deposited_no_tanwin :
    (Categories.pronouns ++ Ishara.forms.map (·.2) ++ (mawsul.take 10).map (·.2)).all
      (fun w => !Nida.hasTanwin w) = true := by decide

theorem man_looks_like_tanwin : Nida.hasTanwin Istifham.man = true := by decide

end Slge.Marifa
