import Slge.Huruf
import Slge.Maqayis

/-!
# الأدواتُ علاقاتٍ تشغيليّة: صورةٌ، رتبةٌ، أصنافُ معمولات، عملٌ دالّةً، ونوعُ علاقةٍ معلَن

كلُّ أداةٍ من جدول الحروف الموحَّد (`Huruf.table`، 68) تُحمَل على بنيةٍ واحدة (`Adat`): صورتُها خاناتٍ، **رتبتُها**
(عددُ معمولاتها)، **أصنافُ معمولاتها** (اسم/فعل/جملة/أيّ)، **عملُها** دالّةً على خانة آخر معمولها (`apply`)، و**نوعُ
علاقتها** (`Rel`: تعدية، توكيد، نفي، شرط، جمع، ترتيب، تخيير…) — والنوعُ **معلَنٌ** من كتب حروف المعاني لا مبرهَن:
الخاناتُ لا تحمل معنى، فما يُبرهَن هنا هو ما على الصورة:

* `apply_licensed`: عملُ الأداة على معمولٍ مرخَّصٍ معربٍ يعيد مرخَّصًا — الجرُّ والنصبان بتغيير حالةٍ (لكلّ كلمة)،
  والجزمُ بتسكين الآخر إلّا بعد مدٍّ (`Jazm.hollow_forced`: حذفُ العين ملزَم، وهو شأنُ `Jazm` لا هذه البنية).
* `args_arity`: أصنافُ المعمولات بعدد الرتبة، لكلّ مدخل.
* **التركيبُ بعينه**: كَأَنَّ = كَ ++ أَنَّ، أَلَا = أَ ++ لَا، أَمَا = أَ ++ مَا، لِكَيْ = لِ ++ كَيْ وكَيْلَا = كَيْ ++ لَا
  بعملِ كَيْ، وإِنَّمَا = إِنَّ ++ مَا **بلا عمل** (الكفّ: `Nawasikh.kaffa`).
* **الترتيبُ لا الحذف**: الأداةُ تقدّم قراءاتِ جارتها التي صنفُها صنفُ معمولها الأوّل (`rank`) ولا تُسقط قراءةً
  ولا تزيدها (`mem_rank`، `length_rank`) — القياسُ على MASAQ في `tools/gen_adawat_index.py`.

ما ليس هنا: جداولُ صدقٍ للأدوات؛ «و» ليست ∧ و«أو» ليست ∨ و«إنْ» ليست الاستلزام — نوعُ العلاقة وسمٌ يُقاس في
المرحلة د مع التفسير المختوم.
-/

namespace Slge.Adawat

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-- صنفُ المعمول. -/
inductive Cat where
  | ism | fil | jumla | ay
  deriving DecidableEq, Repr

/-- نوعُ العلاقة — معلَنٌ من كتب حروف المعاني؛ لا يُشتقّ من الخانات. -/
inductive Rel where
  | taadiya   -- حروفُ الجرّ: تعديةٌ وظرفيّة
  | istithna  -- خلا، عدا، حاشا
  | taqlil    -- رُبَّ
  | tawkid    -- إنّ، أنّ
  | tashbih   -- كأنّ
  | istidrak  -- لكنّ، لكن
  | tamanni   -- ليت
  | tarajji   -- لعلّ
  | nida
  | nafy      -- لا، ما، لم، لمّا، لن، إنْ النافية، لات، لا النافية للجنس
  | maiyya    -- واو المعيّة
  | masdariyya -- أنْ، كي، لام كي، حتّى الناصبة، فاء السببيّة، واو المعيّة الناصبة
  | jaza      -- إذن
  | amr       -- لام الأمر
  | nahy      -- لا الناهية
  | shart     -- إنْ، إذما
  | tanfis    -- س، سوف
  | rad       -- كلّا
  | tahqiq    -- قد
  | jam       -- و: مطلقُ الجمع
  | tartibTaqib   -- ف
  | tartibTarakhi -- ثمّ
  | ghaya     -- حتّى العاطفة
  | takhyir   -- أو، أم
  | idrab     -- بل
  | istifham  -- أ، هل
  | istiftah  -- ألا، أما
  deriving DecidableEq, Repr

structure Adat where
  harf : Huruf.Harf
  arity : Nat
  args : List Cat
  rel : Rel

/-- الأعمدةُ المعلَنة بترتيب `Huruf.table`: (الرتبة، الأصناف، النوع). -/
def declared : List (Nat × List Cat × Rel) := [
  (1, [.ism], .taadiya), (1, [.ism], .taadiya), (1, [.ism], .taadiya), (1, [.ism], .taadiya),
  (1, [.ism], .taadiya), (1, [.ism], .taadiya), (1, [.ism], .taadiya), (1, [.ism], .taadiya),
  (1, [.ism], .taadiya), (1, [.ism], .taadiya), (1, [.ism], .taadiya), (1, [.ism], .taadiya),
  (1, [.ism], .taadiya),
  (1, [.ism], .istithna), (1, [.ism], .istithna), (1, [.ism], .istithna),
  (1, [.ism], .taqlil),
  (2, [.ism, .ay], .tawkid), (2, [.ism, .ay], .tawkid), (2, [.ism, .ay], .tashbih),
  (2, [.ism, .ay], .istidrak), (2, [.ism, .ay], .tamanni), (2, [.ism, .ay], .tarajji),
  (1, [.ism], .nida), (1, [.ism], .nida), (1, [.ism], .nida), (1, [.ism], .nida), (1, [.ism], .nida),
  (1, [.ism], .nida),
  (2, [.ism, .ay], .nafy),
  (1, [.ism], .maiyya),
  (1, [.fil], .masdariyya), (1, [.fil], .nafy), (1, [.fil], .masdariyya), (1, [.fil], .jaza),
  (1, [.fil], .masdariyya), (1, [.fil], .masdariyya), (1, [.fil], .masdariyya), (1, [.fil], .masdariyya),
  (1, [.fil], .nafy), (1, [.fil], .nafy), (1, [.fil], .amr), (1, [.fil], .nahy),
  (2, [.fil, .fil], .shart), (2, [.fil, .fil], .shart),
  (1, [.fil], .tanfis), (1, [.fil], .tanfis), (1, [.jumla], .rad), (1, [.fil], .tahqiq),
  (2, [.ay, .ay], .jam), (2, [.ay, .ay], .tartibTaqib), (2, [.ay, .ay], .tartibTarakhi),
  (2, [.ay, .ay], .ghaya), (2, [.ay, .ay], .takhyir), (2, [.ay, .ay], .takhyir), (2, [.ay, .ay], .nafy),
  (2, [.ay, .ay], .idrab), (2, [.ay, .ay], .istidrak),
  (1, [.jumla], .istifham), (1, [.jumla], .istifham), (1, [.jumla], .nafy), (1, [.jumla], .nafy),
  (1, [.fil], .nafy), (1, [.fil], .nafy), (1, [.jumla], .nafy), (1, [.jumla], .nafy),
  (1, [.jumla], .istiftah), (1, [.jumla], .istiftah)
]

def table : List Adat :=
  (Huruf.table.zip declared).map fun p => ⟨p.1, p.2.1, p.2.2.1, p.2.2.2⟩

theorem table_length : table.length = 68 ∧ declared.length = Huruf.table.length := by decide

/-- أصنافُ المعمولات بعدد الرتبة، لكلّ مدخل. -/
theorem args_arity : table.all (fun a => a.args.length == a.arity) = true := by decide

/-- العاملُ في الاسم معمولُه الأوّل اسم، وفي الفعل فعل؛ والعاطفُ ثنائيُّ الرتبة؛ والمشبّهةُ بالفعل ثنائيّة
(اسمٌ وخبر). -/
theorem args_of_amal :
    table.all (fun a => match a.harf.amal with
      | .jarr | .nasbIsm | .nida | .maiyya => a.args.head? == some .ism
      | .nasbFil | .jazm | .jazm2 => a.args.head? == some .fil
      | .tabi => a.arity == 2
      | .none => true) = true := by decide

/-! ## العملُ دالّةً على خانة آخر المعمول -/

/-- العمل: الجرُّ كسرٌ، نصبُ الاسم ونصبُ المضارع فتحٌ، الجزمُ سكونٌ؛ وما لا عملَ له يعيد معمولَه بعينه. -/
def apply (a : Adat) (w : List SCell) : List SCell :=
  match a.harf.amal with
  | .jarr => Majrurat.jarr w
  | .nasbIsm => Nawasikh.nasb w
  | .nasbFil => setLast w 0
  | .jazm | .jazm2 => Jazm.sukun w
  | _ => w

/-- عملُ الأداة ذاتِ الحركة على معمولٍ مرخَّصٍ معربٍ (آخرُه متحرّك) يعيد مرخَّصًا — لكلّ أداةٍ وكلمة. -/
theorem apply_licensed (a : Adat) (w : List SCell) (hw : licensed w = true)
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) (hj : a.harf.amal ≠ .jazm ∧ a.harf.amal ≠ .jazm2) :
    licensed (apply a w) = true := by
  unfold apply
  split
  · unfold Majrurat.jarr; rw [Zuruf.setLast_licensed w 1 (by decide) hlast]; exact hw
  · unfold Nawasikh.nasb; rw [Zuruf.setLast_licensed w 0 (by decide) hlast]; exact hw
  · rw [Zuruf.setLast_licensed w 0 (by decide) hlast]; exact hw
  · rename_i h; exact absurd h hj.1
  · rename_i h; exact absurd h hj.2
  · exact hw

/-- الجزمُ: تسكينُ الآخر مرخَّصٌ ما لم يسبقه ساكنٌ (مدّ) — وإلّا فحذفُ العين ملزَم (`Jazm.hollow_forced`). -/
theorem apply_jazm_licensed (a : Adat) (i : List SCell) (x : SCell) (hi : licensed i = true) (hne : i ≠ [])
    (hlast : ∀ y, i.getLast? = some y → y.isSukun = false) (hj : a.harf.amal = .jazm ∨ a.harf.amal = .jazm2) :
    licensed (apply a (i ++ [x])) = true := by
  unfold apply
  have key : Jazm.sukun (i ++ [x]) = i ++ [⟨x.carrier, 3⟩] := Shibh.setLast_append_singleton i x 3
  rcases hj with h | h <;> simp only [h] <;> rw [key] <;> exact Jazm.sukun_licensed i x.carrier hi hne hlast

/-! ## التركيبُ بعينه والكفّ -/

def at_ (k : Nat) : List SCell := (Huruf.table.getD k ⟨"", [], .ism, .none⟩).cells
def rw_ (n : String) : List SCell := ((Rawabit.particles.find? (·.name == n)).map (·.cells)).getD []
def rwAmal (n : String) : Rawabit.Amal := ((Rawabit.particles.find? (·.name == n)).map (·.amal)).getD .none

/-- كَأَنَّ = كَ ++ أَنَّ؛ أَلَا = أَ ++ لَا؛ أَمَا = أَ ++ مَا؛ لِكَيْ = لِ ++ كَيْ وكَيْلَا = كَيْ ++ لَا بعملِ كَيْ (النصب)؛
وإِنَّمَا = إِنَّ ++ مَا بلا عمل (الكفّ). -/
theorem compositions :
    at_ 19 = at_ 2 ++ at_ 18 ∧ at_ 66 = at_ 58 ++ at_ 61 ∧ at_ 67 = at_ 58 ++ at_ 60 ∧
    rw_ "لِكَيْ" = at_ 1 ++ at_ 33 ∧ rw_ "كَيْلَا" = at_ 33 ++ at_ 61 ∧
    rwAmal "لِكَيْ" = .nasb ∧ rwAmal "كَيْلَا" = .nasb ∧
    rw_ "إِنَّمَا" = Nawasikh.kaffa (at_ 17) ∧ rwAmal "إِنَّمَا" = .none := by decide

/-! ## الترتيبُ لا الحذف -/

/-- صنفُ القراءة من قوالبها: فعلٌ إن كان قالبٌ من قوالبها قالبَ فعل (الماضي والمضارع والأمر)، وإلّا اسم. -/
def catOf (rd : Jidh.Reading) : Cat :=
  if rd.templates.any (fun k => Jumla.verbTemplates.contains k || Filiyya.amrTemplates.contains k) then .fil
  else .ism

/-- القراءةُ توافق الأداة: صنفُها صنفُ معمولها الأوّل، أو المعمولُ أيُّ شيء. -/
def fits (a : Adat) (rd : Jidh.Reading) : Bool :=
  match a.args.head? with
  | some .ay | some .jumla | none => true
  | some k => catOf rd == k

def rank (a : Adat) (rs : List Jidh.Reading) : List Jidh.Reading :=
  rs.filter (fits a) ++ rs.filter (fun rd => !fits a rd)

theorem mem_rank (a : Adat) (rs : List Jidh.Reading) (rd : Jidh.Reading) : rd ∈ rank a rs ↔ rd ∈ rs := by
  simp only [rank, List.mem_append, List.mem_filter, Bool.not_eq_true']
  constructor
  · rintro (⟨h, _⟩ | ⟨h, _⟩) <;> exact h
  · intro h
    cases hf : fits a rd
    · exact Or.inr ⟨h, rfl⟩
    · exact Or.inl ⟨h, rfl⟩

theorem length_rank (a : Adat) : ∀ rs : List Jidh.Reading, (rank a rs).length = rs.length
  | [] => rfl
  | rd :: rs => by
    have ih := length_rank a rs
    simp only [rank, List.length_append] at ih ⊢
    cases hf : fits a rd <;> simp [hf] <;> omega

/-- الأداةُ المجاورة من صورتها: أوّلُ مدخلٍ صورتُه الكلمة. -/
def ofCells (w : List SCell) : Option Adat := table.find? (·.harf.cells == w)

/-! ## الشواهد بالحساب -/

def lam : List SCell := [c 23 0, c 24 3]                -- لَمْ
def inna : List SCell := [c 0 1, c 25 3, c 25 0]         -- إِنَّ
def yaktubu : List SCell := [c 28 0, c 22 3, c 3 2, c 2 2] -- يَكْتُبُ

set_option maxRecDepth 100000 in
/-- لَمْ تجزم يَكْتُبُ (سكونُ الآخر، مرخَّص)؛ إِنَّ تنصب كِتَابٌ؛ وبعد لَمْ تتقدّم قراءةُ الفعل لِوَجَدَ (وَجَدَ لا وَ+جَدَ)،
وبعد إِنَّ تتقدّم قراءةُ الاسم لِفَرِيقٌ، ولا قراءةَ تسقط. -/
theorem witnesses :
    (ofCells lam).map (fun a => apply a yaktubu) = some [c 28 0, c 22 3, c 3 2, c 2 3] ∧
    (ofCells lam).map (fun a => licensed (apply a yaktubu)) = some true ∧
    (ofCells inna).map (fun a => apply a [c 22 1, c 3 0, c 1 3, c 2 2]) = some [c 22 1, c 3 0, c 1 3, c 2 0] ∧
    (ofCells lam).map (fun a => (rank a (Jidh.jidh Jidh.wajada)).map (fun rd => (fits a rd, rd.pre.length))) =
      some [(true, 0)] ∧
    (ofCells inna).map (fun a => (rank a (Jidh.jidh Jidh.fariqun)).map (fun rd => (fits a rd, rd.templates))) =
      some [(true, [53]), (true, [121])] ∧
    (ofCells inna).map (fun a => (rank a (Jidh.jidh Jidh.fariqun)).length) = some 2 := by decide +kernel

end Slge.Adawat
