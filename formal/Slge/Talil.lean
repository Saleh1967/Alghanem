import Slge.Nisab

/-!
# التعليلُ والسببيّة: العلّةُ فضلةٌ لا تُرفَع، وصورتاها كلمةٌ واحدة، والسببيّةُ الاشتقاقيّةُ ترتيبٌ صارم

* **المفعولُ لأجله** (د٨): مصدرٌ منصوبٌ (`mafulLiAjlih` = `Nawasikh.nasb`) يُقرأ نصبًا لكلّ جذع
  (`liajlih_reads_nasb`)؛ وفرزُه عن المطلق بالجذر لا بالمعنى (`Filiyya.sortFadla`: حَذَرَ بعد دَرَسَ لأجله،
  ودَرْسَ بعده مطلق — `fadla_witnesses`). ما بقي من شرطه (القلبيّةُ، اتّحادُ الفاعل والزمان) معنًى — معلَن.
* **صورتا التعليل**: نصبُ المصدر أو جرُّه بالحرف كلمةٌ بعينها: الحوامِلُ وما قبل الآخر واحدةٌ والطولُ واحد
  (`two_forms_same_word`)؛ الفرقُ خانةُ الآخر وحدَها.
* **أدواتُ التعليل** جدولٌ حاصرٌ على الخانات (`tools`): لِ وبِ ومِنْ أَجْلِ جرٌّ، ولِأَنَّ عملُ إِنَّ بعينه
  (`li_anna_eq_inna`)، وكَيْ ولِ نصبُ المضارع. كلُّها مرخَّصةٌ (`tools_licensed`) ومن جدول أدوات الربط
  (`tools_in_rawabit`). و**ليس فيها ما يرفع العلّة**: الجرُّ جرٌّ والنصبُ نصبٌ واسمُ لِأَنَّ نصبٌ
  (`talil_never_raf`) — العلّةُ فضلةٌ أبدًا.
* **السببيّةُ الاشتقاقيّة** (د١٦): المصدرُ علّةُ المشتقّ عند البصريّين — فالعلّيّةُ على الـ125 هي السلفيّةُ في
  الشبكة (`derives a b`: `b` سلفُ `a` في `Nisab.chain`)، وهي ترتيبٌ جزئيٌّ **صارم**: لا شيءَ علّةُ نفسه
  (`derives_irrefl`)، وعلّةُ العلّة علّة (`derives_trans`)، ولا دورَ (`derives_asymm`) — الثلاثةُ من
  ثلاثة جداول مقرَّرة بـ`decide` على 125 و125×125 (لا نوعٌ مُعرَّفٌ باليد). والبعدُ عن الجذر يتناقص على كلّ
  سببٍ (`derives_dist`) فلا لانهاية.
* **التنازع** (د٨): فعلان على معمولٍ واحد — إعمالُ الثاني لقربه (البصريّون): المتنازَعُ فيه معمولُ الأقرب
  ولا يمسّه الأوّلُ (`nearer_works`: الخانةُ مستقلّةٌ عن الفعل الأوّل)، والأوّلُ يُعمَل في ضميره متّصلًا
  (`first_takes_pronoun`) حافظًا للترخيص (`Damair.attach_licensed`). إعمالُ الأوّل (الكوفيّون) معلَن.
* **التقديمُ الحتميّ**: المفعولُ المتّصلُ يتقدّم على الفاعل الظاهر (`Filiyya.attached_object_first`)؛
  والمفعولُ لأجله حرٌّ في الموضع: نصبُه في التقديم والتأخير واحد (`fronting_keeps_nasb`).
* القارئُ `talil` يقرأ التعليلَ بين كلمتين من خانتيهما: لِأَنَّ، أو مصدرٌ بغير جذر الفعل منصوبًا (لأجله)،
  أو لِ/بِ على مصدرٍ مجرور (تعليلٌ بالحرف — احتمالٌ، فاللامُ تُفيد غيرَ التعليل)، وما سواه لا يُقرأ.
القياسُ على MASAQ في بايثون. الحصرُ المُرسَل أحال على ملفّ `causality_operators_proofs.lean` لم يُرفَق،
ومصفوفةُ أحداثه (`taliim`، `ilm`…) مكتوبةٌ باليد لا على خانة، وفحصُ إجهاده يعدّ «صحيحًا» ما بناه (100%
بالبناء) — لم يُدخَل منه شيء؛ ودخل معناه على الخانات: السببيّةُ ترتيبٌ صارمٌ على الأوزان، والأدواتُ عمليّاتٌ.
-/

namespace Slge.Talil

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## المفعولُ لأجله -/

def mafulLiAjlih (w : List SCell) : List SCell := Nawasikh.nasb w

theorem liajlih_reads_nasb (w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25) :
    Tawabi.caseClass (mafulLiAjlih w) = .nasb := Nawasikh.caseClass_nasb w hne hk

def hadhar : List SCell := [c 6 0, c 9 0, c 10 0]       -- حَذَرَ (شاهدُ MASAQ)
def dars : List SCell := [c 8 0, c 10 3, c 12 0]        -- دَرْسَ

/-- حَذَرَ بعد دَرَسَ مفعولٌ لأجله (مصدرٌ بغير جذر الفعل)، ودَرْسَ بعده مطلقٌ (بجذره). -/
theorem fadla_witnesses :
    Filiyya.sortFadla hadhar Jumla.darasa = .liajlih ∧ Filiyya.sortFadla dars Jumla.darasa = .mutlaqF := by
  decide

/-! ## صورتا التعليل -/

/-- النصبُ مصدرًا والجرُّ بالحرف كلمةٌ بعينها: ما قبل الآخر واحدٌ والطولُ واحد. -/
theorem two_forms_same_word (w : List SCell) :
    Afal.initOf (mafulLiAjlih w) = Afal.initOf (Majrurat.jarr w) ∧
    (mafulLiAjlih w).length = (Majrurat.jarr w).length := by
  refine ⟨?_, ?_⟩
  · show Afal.initOf (setLast w 0) = Afal.initOf (setLast w 1)
    rw [Filiyya.initOf_setLast, Filiyya.initOf_setLast]
  · show (setLast w 0).length = (setLast w 1).length
    rw [Filiyya.length_setLast, Filiyya.length_setLast]

/-! ## أدواتُ التعليل -/

inductive Amal where
  | jarrIsm | innaAmal | nasbFil
  deriving DecidableEq, Repr

def li : List SCell := [c 23 1]
def bi : List SCell := [c 2 1]
def min : List SCell := [c 24 1, c 25 3]
def ajl : List SCell := [c 0 0, c 5 3, c 23 2]           -- أَجْلُ
def anna : List SCell := [c 0 0, c 25 3, c 25 0]         -- أَنَّ
def kay : List SCell := [c 22 0, c 28 3]                 -- كَيْ

/-- مِنْ أَجْلِ: مِنْ ثمّ أَجْل مجرورًا به ومضافًا إلى ما بعده. -/
def minAjli : List SCell := min ++ Majrurat.jarr ajl
/-- لِأَنَّ: اللامُ الجارّةُ على أَنَّ. -/
def liAnna : List SCell := li ++ anna

def tools : List (String × List SCell × Amal) := [
  ("لِ", li, .jarrIsm), ("بِ", bi, .jarrIsm), ("مِنْ أَجْلِ", minAjli, .jarrIsm),
  ("لِأَنَّ", liAnna, .innaAmal), ("كَيْ", kay, .nasbFil), ("لِ (كي)", li, .nasbFil)
]

theorem tools_licensed : tools.all (fun t => licensed t.2.1) = true := by decide
theorem tools_count : tools.length = 6 := by decide

/-- المفردةُ منها في جدول أدوات الربط بعملها: لِ وبِ ومِنْ جرًّا، وكَيْ نصبًا؛ والمركَّبةُ (مِنْ أَجْلِ، لِأَنَّ)
تركيبُ مفردتين. -/
theorem tools_in_rawabit :
    (["لِ", "بِ", "مِنْ"].all fun n => Rawabit.particles.any fun p => p.name == n && p.amal == .jarr) = true ∧
    (Rawabit.particles.any fun p => p.name == "كَيْ" && p.amal == .nasb) = true ∧
    minAjli = min ++ Majrurat.jarr ajl ∧ liAnna = li ++ anna := ⟨by decide, by decide, rfl, rfl⟩

/-- عملُ الأداة على الخانة: جرُّ الاسم، أو عملُ إِنَّ (نصبُ الاسم ورفعُ الخبر)، أو نصبُ المضارع. -/
def apply (a : Amal) (w : List SCell) : List SCell :=
  match a with
  | .jarrIsm => Majrurat.jarr w
  | .innaAmal => Nawasikh.inna.1 w
  | .nasbFil => Nawasikh.nasb w

theorem li_anna_eq_inna : apply .innaAmal = Nawasikh.inna.1 ∧ Nawasikh.inna = (Nawasikh.nasb, Nawasikh.raf) :=
  ⟨rfl, rfl⟩

/-- ليس في أدوات التعليل ما يرفع معمولَها: الجرُّ جرٌّ، واسمُ لِأَنَّ نصبٌ، والمضارعُ نصبٌ — العلّةُ فضلة. -/
theorem talil_never_raf (w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25 ∧ x.carrier.val ≠ 3) :
    ∀ a, Tawabi.caseClass (apply a w) ≠ .raf := by
  intro a
  cases a with
  | jarrIsm => simp [apply, Majrurat.caseClass_jarr w hne hk]
  | innaAmal => simp [apply, Nawasikh.inna, Nawasikh.caseClass_nasb w hne (fun x hx => (hk x hx).1)]
  | nasbFil => simp [apply, Nawasikh.caseClass_nasb w hne (fun x hx => (hk x hx).1)]

/-- مِنْ أَجْلِ: أَجْلِ مجرورٌ، والمضافُ إليه بعدَه مجرور. -/
theorem min_ajli_jarr (w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25 ∧ x.carrier.val ≠ 3) :
    Tawabi.caseClass (Majrurat.jarr ajl) = .jarr ∧ Tawabi.caseClass (Majrurat.jarr w) = .jarr ∧
    licensed minAjli = true :=
  ⟨by decide, Majrurat.caseClass_jarr w hne hk, by decide⟩

/-! ## السببيّةُ الاشتقاقيّة: ترتيبٌ جزئيٌّ صارم على الـ125 -/

/-- `b` علّةُ `a`: سلفٌ له في شبكة البصريّين (المصدرُ أصلُ المشتقّ). -/
def derives (a b : Nat) : Bool := (Nisab.chain a Nisab.F).tail.contains b

set_option maxRecDepth 4096 in
theorem derives_irrefl_all : ((List.range Wazn.N).all fun a => !derives a a) = true := by decide

set_option maxRecDepth 100000 in
/-- البعدُ عن الجذر يتناقص على كلّ سبب. -/
theorem derives_dist_all :
    ((List.range Wazn.N).all fun a => (List.range Wazn.N).all fun b =>
      !derives a b || decide (Nisab.dist b Nisab.F < Nisab.dist a Nisab.F)) = true := by
  decide

set_option maxRecDepth 100000 in
/-- أسلافُ السلف أسلاف. -/
theorem derives_trans_all :
    ((List.range Wazn.N).all fun a => (List.range Wazn.N).all fun b =>
      !derives a b || (Nisab.chain b Nisab.F).tail.all fun d => derives a d) = true := by
  decide

theorem derives_irrefl (a : Nat) (ha : a < Wazn.N) : derives a a = false := by
  have h := List.all_eq_true.1 derives_irrefl_all a (List.mem_range.2 ha)
  simpa using h

theorem derives_dist (a b : Nat) (ha : a < Wazn.N) (hb : b < Wazn.N) (h : derives a b = true) :
    Nisab.dist b Nisab.F < Nisab.dist a Nisab.F := by
  have h1 := List.all_eq_true.1 (List.all_eq_true.1 derives_dist_all a (List.mem_range.2 ha)) b
    (List.mem_range.2 hb)
  simpa [h] using h1

theorem derives_trans (a b d : Nat) (ha : a < Wazn.N) (hb : b < Wazn.N)
    (h₁ : derives a b = true) (h₂ : derives b d = true) : derives a d = true := by
  have h1 := List.all_eq_true.1 (List.all_eq_true.1 derives_trans_all a (List.mem_range.2 ha)) b
    (List.mem_range.2 hb)
  simp only [h₁, Bool.not_true, Bool.false_or] at h1
  exact List.all_eq_true.1 h1 d (List.mem_of_elem_eq_true h₂)

theorem derives_asymm (a b : Nat) (ha : a < Wazn.N) (hb : b < Wazn.N) (h : derives a b = true) :
    derives b a = false := by
  cases hba : derives b a with
  | false => rfl
  | true =>
    have h1 := derives_dist a b ha hb h
    have h2 := derives_dist b a hb ha hba
    exact absurd (Nat.lt_trans h1 h2) (Nat.lt_irrefl _)

/-- الجذرُ (فَعْلٌ، 29) علّةُ كلّ وزنٍ سواه، ولا علّةَ له. -/
theorem root_causes_all :
    ((List.range Wazn.N).all fun a => (a == Shabaka.root) || derives a Shabaka.root) = true ∧
    ((List.range Wazn.N).all fun b => !derives Shabaka.root b) = true := by
  refine ⟨?_, ?_⟩ <;> decide

/-! ## التنازع -/

/-- فعلان على معمولٍ واحد: الأوّلُ بضميره متّصلًا، والثاني يعمل في المتنازَع فيه نصبًا. -/
def tanazu (v₁ v₂ w p : List SCell) : List SCell × List SCell × List SCell :=
  (Damair.attach v₁ p, v₂, Nawasikh.nasb w)

/-- المتنازَعُ فيه معمولُ الأقرب: خانتُه لا تتغيّر بتغيّر الفعل الأوّل. -/
theorem nearer_works (v₁ v₁' v₂ w p : List SCell) :
    (tanazu v₁ v₂ w p).2.2 = Nawasikh.nasb w ∧ (tanazu v₁ v₂ w p).2.2 = (tanazu v₁' v₂ w p).2.2 ∧
    (tanazu v₁ v₂ w p).2.1 = v₂ := ⟨rfl, rfl, rfl⟩

/-- الأوّلُ يأخذ ضميرَه متّصلًا، حافظًا للترخيص بشرط الاتّصال. -/
theorem first_takes_pronoun (v₁ v₂ w p : List SCell) (hh : licensed v₁ = true)
    (hs : noAdj p = true) (hne : v₁ ≠ [])
    (hj : ∀ x y, v₁.getLast? = some x → p.head? = some y → (x.isSukun && y.isSukun) = false) :
    (tanazu v₁ v₂ w p).1 = v₁ ++ p ∧ licensed (tanazu v₁ v₂ w p).1 = true :=
  ⟨rfl, Damair.attach_licensed v₁ p hh hs hne hj⟩

def alimtu : List SCell := [c 18 0, c 23 1, c 24 3, c 3 2]        -- عَلِمْتُ
def amiltu : List SCell := [c 18 0, c 24 1, c 23 3, c 3 2]        -- عَمِلْتُ
def hu : List SCell := [c 26 2]                                   -- ـهُ
def alkhayr : List SCell := [c 0 0, c 23 3, c 7 0, c 28 3, c 10 2] -- الْخَيْرُ

/-- عَلِمْتُهُ وَعَمِلْتُ الْخَيْرَ: الأوّلُ بضميره، والثاني ناصبٌ. -/
theorem tanazu_witness :
    (tanazu alimtu amiltu alkhayr hu).1 = [c 18 0, c 23 1, c 24 3, c 3 2, c 26 2] ∧
    licensed (tanazu alimtu amiltu alkhayr hu).1 = true ∧
    Tawabi.caseClass (tanazu alimtu amiltu alkhayr hu).2.2 = .nasb := by decide

/-! ## التقديم -/

/-- المفعولُ لأجله حرٌّ في الموضع: نصبُه قبل الفعل وبعده واحد. -/
theorem fronting_keeps_nasb (v w : List SCell) (hne : w ≠ [])
    (hk : ∀ x, Afal.lastOf w = some x → x.carrier.val ≠ 25) :
    ([mafulLiAjlih w, v].head? = some (mafulLiAjlih w)) ∧ ([v, mafulLiAjlih w].getLast? = some (mafulLiAjlih w)) ∧
    Tawabi.caseClass (mafulLiAjlih w) = .nasb := ⟨rfl, rfl, liajlih_reads_nasb w hne hk⟩

/-! ## القارئ -/

inductive Talil where
  | liAnna | liajlih | biHarf | unread
  deriving DecidableEq, Repr

/-- التعليلُ من الخانتين: لِأَنَّ بعينها؛ مصدرٌ منصوبٌ بلا «ال» بغير جذر الفعل قبله ⇒ لأجله (المعرَّفُ بأل
مفعولٌ به: أَكَلَ الدَّرْسَ)؛ لِ/بِ على مصدرٍ مجرور ⇒
تعليلٌ بالحرف (احتمالٌ: اللامُ والباءُ تُفيدان غيرَه — باسمه)؛ وما سواه لا يُقرأ. -/
def talil (prev w : List SCell) : Talil :=
  if w == liAnna then .liAnna
  else if Tawabi.caseClass w == .nasb && !Marifa.hasAl w && Filiyya.sortFadla w prev == .liajlih then .liajlih
  else if (w.take 1 == li || w.take 1 == bi) && (Filiyya.masdarRoot (w.drop 1)).isSome &&
      Tawabi.caseClass w == .jarr then .biHarf
  else .unread

def darb : List SCell := [c 15 0, c 10 3, c 2 1]                  -- ضَرْبِ
def hikma : List SCell := [c 6 1, c 22 3, c 24 0, c 3 1]          -- حِكْمَةِ

/-- دَرَسَ حَذَرَ لأجله؛ دَرَسَ دَرْسَ لا يُقرأ تعليلًا (مطلق)؛ بِضَرْبِ ولِحِكْمَةِ تعليلٌ بالحرف؛ لِأَنَّ بعينها؛
أَكَلَ الدَّرْسَ مفعولٌ به لا علّة. -/
theorem talil_witnesses :
    talil Jumla.darasa hadhar = .liajlih ∧ talil Jumla.darasa dars = .unread ∧
    talil Jumla.darasa (bi ++ darb) = .biHarf ∧ talil Jumla.darasa (li ++ hikma) = .biHarf ∧
    talil Jumla.darasa liAnna = .liAnna ∧ talil Jumla.darasa Jumla.zayd = .unread ∧
    talil Filiyya.akala Filiyya.addars = .unread := by decide

end Slge.Talil
