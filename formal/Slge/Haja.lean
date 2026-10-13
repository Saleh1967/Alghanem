import Slge.HajaTable
import Slge.Bawwabat

/-!
# توقيعُ الحاجة: ما يحتاجه كلُّ بابٍ من المغلق ليتمّ، وقسمةُ المفرد عند النبهانيّ بمعيار الحاجة (ADR ٥٦)

النبهانيّ يقسم المفرد **بالحاجة**: «إن كان لا يستقلّ بمعناه فهو الحرف… لا يفهم معناه… إلا باعتبار لفظٍ آخر» (ج3 500)،
و«إن كان يستقلّ بمعناه، أي يفهم معناه من غير حاجةٍ للفظٍ آخر» فعلٌ أو اسم (403)، والجزئيُّ «إن لم يستقلّ، بأن كان
يفتقر إلى شيءٍ يفسّره، فهو المضمر» (407). فالحاجةُ هنا **قيدٌ مكتوب**: لكلّ بابٍ قائمةُ حاجاتٍ (`Haja`)، كلُّ حاجةٍ
جهتُها (قبل، بعد، أيٌّ) وما يقضيها (اسم، فعل، جزءُ كلام) وهل يُشترط الاتّصال، ومفتاحُها في `HajaTable` (عباراتُها
في سطرٍ واحدٍ من ج3 أو الكتاب المختومَين). والصدارة (`sadr`) من الكتاب: «الفعل ليس في الجزاء بصلةٍ لما قبله كما أنه
في حروف الاستفهام ليس صلةً لما قبله» (س9213).

## ما يُبرهَن

* **المرساة**: كلُّ حاجةٍ مفتاحُها في الجدول المرسى (`needs_anchored`).
* **معيارُ النبهانيّ**: كلُّ بابٍ حرفيٍّ له حاجة (`harf_has_need`)، والمستقلُّ لا حاجةَ له (`mustaqill_none`)، والمضمرُ
  حاجتُه مفسِّر (`damir_mufassir`)؛ والتخصيصُ المتّصل (الاستثناء والشرط) متّصلُ الحاجات كلِّها ولا اتّصالَ مفروضٌ في غيرهما — النصُّ لا يذكره (`muttasil_takhsis`، `ittisal_only_takhsis`)؛
  والصدارةُ للشرط والاستفهام وحدَهما (`sadr_exactly`).
* **الجدولُ الموحَّد**: كلُّ حرفٍ من `Huruf.table` (68) في بابٍ حرفيٍّ إلّا اثنين بأسمائهما بلا سند — واوُ المعيّة
  الاسميّة ولاتَ (`huruf_have_needs`، `ghayr_musnad`)؛ والصنفُ في الجدول (المختصّةُ بالأسماء/بالأفعال، بناءٌ
  مستقلٌّ سابق) يوافق حاجةَ بابها: المختصّةُ بالأسماء تحتاج اسمًا بعدها، والمختصّةُ بالأفعال فعلًا بعدها، إلّا
  مسمّاةً (`class_agrees`). والخاناتُ الواحدةُ في أبوابٍ عدّة (لَا في أربعة: `la_four`) — الخانةُ لا تحسم الباب.
* **قسمةُ المفرد** (`mufradOf`): حرفٌ إن كان بابُه حرفيًّا، ومضمرٌ إن لم يستقلّ وليس حرفًا، وإلّا فعلٌ إن دلّ بهيئته،
  واسمٌ؛ قسمةٌ تامّةٌ مانعة (`mufrad_partition`) ولا حرفَ إلّا ذو حاجة (`mufrad_harf_needs`).

والمبرهَنُ خواصُّ هذا القيد المنقول على الجداول، لا اللغة.
-/

namespace Slge.Haja

open Slge.Categories (c)

inductive Jiha where
  | qabl | bad | ayy
  deriving DecidableEq, Repr

inductive Mahjuj where
  | ism | fil | juz
  deriving DecidableEq, Repr

structure Haja where
  jiha : Jiha
  ma : Mahjuj
  ittisal : Bool
  key : String
  deriving DecidableEq, Repr

inductive Bab where
  | mustaqill | jarr | mushabbaha | atf | istithna | shart | nafy | amilFil | tanbih | jawab | rad
  | istifham | nida | damir | mawsul | ghayrMusnad
  deriving DecidableEq, Repr

def Bab.all : List Bab :=
  [.mustaqill, .jarr, .mushabbaha, .atf, .istithna, .shart, .nafy, .amilFil, .tanbih, .jawab, .rad,
   .istifham, .nida, .damir, .mawsul, .ghayrMusnad]

/-- ما يحتاجه البابُ ليتمّ. -/
def needs : Bab → List Haja
  | .mustaqill => []
  | .jarr => [⟨.bad, .ism, false, "H_IDAFA"⟩, ⟨.ayy, .fil, false, "H_IDAFA"⟩]
  | .mushabbaha => [⟨.bad, .ism, false, "H_MUSHABBAHA"⟩, ⟨.bad, .juz, false, "H_MUSHABBAHA"⟩]
  | .atf => [⟨.qabl, .juz, false, "H_ATF"⟩, ⟨.bad, .juz, false, "H_ATF"⟩]
  | .istithna => [⟨.qabl, .juz, true, "H_ISTITHNA"⟩, ⟨.bad, .ism, true, "H_ISTITHNA"⟩]
  | .shart => [⟨.bad, .juz, true, "H_SHART"⟩, ⟨.ayy, .juz, true, "H_SHART"⟩]
  | .nafy => [⟨.bad, .juz, false, "H_NAFY"⟩]
  | .amilFil => [⟨.bad, .fil, false, "H_ISTIQBAL"⟩]
  | .tanbih => [⟨.bad, .juz, false, "H_TANBIH"⟩]
  | .jawab => [⟨.qabl, .juz, false, "H_JAWAB"⟩]
  | .rad => [⟨.qabl, .juz, false, "H_RAD"⟩]
  | .istifham => [⟨.bad, .juz, false, "H_SADARA"⟩]
  | .nida => [⟨.bad, .ism, false, "H_NIDA"⟩]
  | .damir => [⟨.ayy, .ism, false, "H_DAMIR"⟩]
  | .mawsul => [⟨.bad, .juz, false, "H_MAWSUL"⟩]
  | .ghayrMusnad => []

/-- الصدارة: لا يتّصل ما بعده بما قبله (س9213). -/
def sadr : Bab → Bool
  | .shart | .istifham => true
  | _ => false

/-- البابُ حرفيٌّ: أعضاؤه حروفٌ لا تستقلّ (ج3 500). -/
def Bab.harf : Bab → Bool
  | .jarr | .mushabbaha | .atf | .istithna | .shart | .nafy | .amilFil | .tanbih | .jawab | .rad
  | .istifham | .nida => true
  | _ => false

theorem needs_anchored :
    Bab.all.all (fun b => (needs b).all (fun h => HajaTable.keys.contains h.key)) = true ∧
    HajaTable.keys.contains "H_SADARA" = true ∧ HajaTable.keys.contains "H_HARF" = true ∧
    HajaTable.keys.contains "H_MUSTAQILL" = true := by decide

theorem harf_has_need : Bab.all.all (fun b => !b.harf || !(needs b).isEmpty) = true := by decide

theorem mustaqill_none : needs .mustaqill = [] := rfl

theorem damir_mufassir : needs .damir = [⟨.ayy, .ism, false, "H_DAMIR"⟩] := rfl

theorem muttasil_takhsis :
    [Bab.istithna, .shart].all (fun b => (needs b).all (·.ittisal)) = true := by decide

/-- الاتّصالُ شرطٌ منصوصٌ في الاستثناء والشرط وحدَهما (ج3 711، 714)؛ ولا يُفرض على غيرهما. -/
theorem ittisal_only_takhsis :
    Bab.all.filter (fun b => (needs b).any (·.ittisal)) = [.istithna, .shart] := by decide

theorem sadr_exactly : Bab.all.filter sadr = [.shart, .istifham] := by decide

/-- بابُ كلّ مدخلٍ من `Huruf.table` بترتيبه (68). -/
def babs : List Bab :=
  [.jarr, .jarr, .jarr, .jarr, .jarr, .jarr, .jarr, .jarr, .jarr, .jarr, .jarr, .jarr, .jarr,
   .istithna, .istithna, .istithna, .jarr,
   .mushabbaha, .mushabbaha, .mushabbaha, .mushabbaha, .mushabbaha, .mushabbaha,
   .nida, .nida, .nida, .nida, .nida, .nida,
   .mushabbaha, .ghayrMusnad,
   .amilFil, .amilFil, .amilFil, .amilFil, .amilFil, .amilFil, .amilFil, .amilFil,
   .amilFil, .amilFil, .amilFil, .amilFil,
   .shart, .shart,
   .amilFil, .amilFil, .rad, .amilFil,
   .atf, .atf, .atf, .atf, .atf, .atf, .atf, .atf, .atf,
   .istifham, .istifham, .nafy, .nafy, .amilFil, .amilFil, .nafy, .ghayrMusnad, .tanbih, .tanbih]

def babOf (i : Nat) : Bab := babs.getD i .ghayrMusnad

theorem babs_length : babs.length = Huruf.table.length := by decide

/-- كلُّ حرفٍ في بابٍ حرفيٍّ إلّا اثنين بلا سندٍ في المرسى: واوُ المعيّة الاسميّة (30) ولاتَ (65). -/
theorem huruf_have_needs :
    (List.range Huruf.table.length).filter (fun i => !(babOf i).harf) = [30, 65] := by decide

theorem ghayr_musnad : babOf 30 = .ghayrMusnad ∧ babOf 65 = .ghayrMusnad := by decide

def needsIsmAfter (b : Bab) : Bool := (needs b).any (fun h => h.jiha == .bad && h.ma == .ism)
def needsFilAfter (b : Bab) : Bool := (needs b).any (fun h => h.jiha == .bad && h.ma == .fil)

/-- الصنفُ في الجدول الموحَّد يوافق حاجةَ الباب: المختصّةُ بالأسماء تحتاج اسمًا بعدها إلّا واوَ المعيّة (30)،
والمختصّةُ بالأفعال فعلًا بعدها إلّا أداتَي الجزاء (43، 44: حاجتُهما جزءُ كلام) وكلّا (47: ردع). -/
theorem class_agrees :
    (List.range Huruf.table.length).filter (fun i =>
      match Huruf.table[i]? with
      | some h => (h.cls == .ism && !needsIsmAfter (babOf i)) || (h.cls == .fil && !needsFilAfter (babOf i))
      | none => false) = [30, 43, 44, 47] := by decide

/-- لَا خاناتٌ واحدة في أربعة أبواب: المشبّهة (النافية للجنس)، والعامل في الفعل (الناهية)، والعطف، والنفي. -/
theorem la_four :
    ((List.range Huruf.table.length).filter (fun i =>
      match Huruf.table[i]? with
      | some h => h.cells == [c 23 0, c 1 3]
      | none => false)).map babOf = [.mushabbaha, .amilFil, .atf, .nafy] := by decide

/-- أدواتُ الربط خارج الجدول الموحَّد ببابها حيث يسمّيها المرسى بلفظها: (الصورة، الاسمُ في النصّ، الباب، المفتاح).
وما سواها من أدوات الربط (لَيْسَ، إِنَّمَا، مَتَى، أَيُّ، كُلَّمَا…) بلا باب: لا يسمّيها مرسى الحاجة. -/
def particles : List (String × String × Bab × String) :=
  [("إِلَّا", "إلا", .istithna, "H_ISTITHNA"), ("غَيْرُ", "غير", .istithna, "H_ISTITHNA"),
   ("إِذَا", "إذا", .shart, "H_SHART"), ("مَنْ", "من", .shart, "H_SHART"),
   ("مَهْمَا", "مهما", .shart, "H_SHART"), ("حَيْثُمَا", "حيثما", .shart, "H_SHART"),
   ("أَيْنَمَا", "أينما", .shart, "H_SHART"), ("لَوْ", "لو", .shart, "H_LAW"),
   ("نَعَمْ", "نعم", .jawab, "H_JAWAB_HURUF"), ("بَلَى", "بلى", .jawab, "H_JAWAB_HURUF"),
   ("أَجَلْ", "أجل", .jawab, "H_JAWAB_HURUF")]

theorem particles_anchored :
    particles.all (fun p => HajaTable.keys.contains p.2.2.2 && p.2.2.1.harf) = true := by decide

/-! ## قسمةُ المفرد عند النبهانيّ (ج3 403–407) -/

inductive Mufrad where
  | harf | mudmar | fil | ism
  deriving DecidableEq, Repr

/-- حرفٌ إن كان البابُ حرفيًّا؛ وإلّا مضمرٌ إن احتاج (لا يستقلّ)؛ وإلّا فعلٌ إن دلّ بهيئته؛ وإلّا اسم. -/
def mufradOf (b : Bab) (hayaa : Bool) : Mufrad :=
  if b.harf then .harf
  else if !(needs b).isEmpty then .mudmar
  else if hayaa then .fil
  else .ism

theorem mufrad_partition (b : Bab) (hayaa : Bool) :
    (mufradOf b hayaa = .harf ↔ b.harf = true) ∧
    (mufradOf b hayaa = .mudmar ↔ b.harf = false ∧ (needs b).isEmpty = false) ∧
    (mufradOf b hayaa = .fil ↔ b.harf = false ∧ (needs b).isEmpty = true ∧ hayaa = true) := by
  unfold mufradOf
  cases hb : b.harf <;> cases he : (needs b).isEmpty <;> cases hayaa <;> simp

theorem mufrad_harf_needs (b : Bab) (hayaa : Bool) (h : mufradOf b hayaa = .harf) :
    (needs b).isEmpty = false := by
  have hb := ((mufrad_partition b hayaa).1).1 h
  have := harf_has_need
  revert hb
  cases b <;> simp_all [needs, Bab.harf]

theorem mufrad_witnesses :
    mufradOf .jarr false = .harf ∧ mufradOf .damir false = .mudmar ∧
    mufradOf .mawsul false = .mudmar ∧ mufradOf .mustaqill true = .fil ∧
    mufradOf .mustaqill false = .ism := by decide

end Slge.Haja
