import Slge.BawwabatTable
import Slge.Maani

/-!
# بوّاباتُ المعنى: الزمنُ والعطفُ والعمومُ والتخصيصُ جبرًا منقولًا من ج3 (ADR ٥٥)

الحرفُ «ما دلّ على معنى في غيره» (ج3 499)؛ ومعناه هنا **عمليّةٌ على معنى غيره**: على زمن الفعل، أو على صدق
جزأي العطف، أو على مجال الحكم. كلُّ عمليّةٍ بمفتاحها في `BawwabatTable` (عباراتُها في سطرٍ واحدٍ من ج3 المختوم،
`tools/deposit_bawwabat.py`)، والمعنى المكتوب هنا **قراءةُ تلك العبارات لا غيرُها**؛ والمبرهَن خواصُّ هذا الجبر
المنقول (لا اللغة: المادّة ١٧ من دستور الوكيل). الوضعُ «من حيث هو»: لا لافظَ ولا سامعَ ولا عالَم.

## ١. الزمن (`Z_HAYAA`، `Z_FIL`، `N_*`، `T_*`)

الأوقاتُ أربعة لا ثلاثة، لأنّ النصَّ يسمّي رابعًا: «الماضي القريب من الحال» («ما» 527، «قد» 539). والزمنُ مجموعةُ أوقات
(`Azmina`). الهيئةُ تعطي: الماضي ⟼ {ماضٍ، قريب}، والمضارعُ ⟼ {حال، مستقبل} («الحاضر والمستقبل في اللفظ واحد» —
**اشتراكٌ في الدالّ بنصّه**: `mudari_two_points`)؛ والأمرُ «ما نُزع منه حرفُ المضارعة» ولا يسمّي النصُّ زمنَه
(`zamanOf .amr = none`، دَينٌ مسمًّى `AMR_TIME_UNSOURCED`). والأداةُ عمليّةٌ على الهيئة (`apply`):
* **تخليص** (`takhlis`): الناتجُ داخلَ زمن الهيئة — السينُ وسوفَ وأنْ وإنِ الشرطيّةُ ولا ولن على المضارع ⟼ {مستقبل}
  (`istiqbal_group`، «حروف الاستقبال» 539)، وما على المضارع ⟼ {حال} وعلى الماضي ⟼ {قريب}، وقد على الماضي ⟼ {قريب}.
* **قلب** (`qalb`): الناتجُ خارجَ زمن الهيئة كلّه — لم ولمّا على المضارع ⟼ الماضي («لقلب المضارع إلى الماضي»)،
  وإنِ النافيةُ على الماضي ⟼ {حال} (شاهدُ النصّ «إِنْ كَانَتْ» ماضٍ).
المبرهَن: كلُّ عمليّةٍ معرَّفةٍ تخليصٌ أو قلبٌ ولا ثالث (`takhlis_xor_qalb`)، والقلبُ ثلاثةُ أزواجٍ بأعيانها
(`qalb_exactly`)؛ والأزمنةُ التي تبلغها الهيئاتُ والأدواتُ خمسٌ لا سادسَ لها (`reach_exhausted` — الاستنفاد)؛
وكلُّ تخليصٍ يحسم اشتراكَ المضارع إلى وقتٍ واحد (`takhlis_resolves_mudari`)؛ والجدولُ موافقٌ لمعاني `Maani` المستخرجة
استقلالًا (`agrees_with_maani`).

## ٢. العطف (`A_*`)

الواقعةُ صدقُ الجزأين ووقتاهما (`Waqia`). الواو «لمطلق الجمع لا تفيد ترتيبًا ولا معيّة» ⟼ ∧؛ الفاءُ ترتيبٌ وتعقيب
⟼ ∧ والثاني عقبَ الأوّل؛ ثمّ ترتيبٌ وتراخٍ ⟼ ∧ وبينهما فاصل؛ حتّى ترتيب ⟼ ∧ والثاني بعد الأوّل (والجزئيّةُ لا تُكتب
هنا: `HATTA_JUZ_NOT_MODELED`)؛ أو وأم «تعليقُ الحكم بأحد المذكورين» ⟼ ∨، وأم لا تقع إلّا في الاستفهام؛ ولا وبل
ولكن «المعطوفُ مخالفٌ للمعطوف عليه في حكمه» ⟼ ⊕. المبرهَن لكلّ واقعة (لا على شاهد): الواوُ تبادليّة
(`waw_comm`) والفاءُ ليست (`fa_not_comm`)؛ الترتيبُ تعقيبٌ أو تراخٍ لا ثالث (`tartib_split`) والاثنان لا يجتمعان
(`fa_thumma_disjoint`)؛ كلُّ مرتَّبٍ جمعٌ (`tartib_imp_waw`)؛ الجمعُ يستلزم الأحد (`waw_imp_aw`)؛ والمخالفةُ
تُصدِق جزءًا واحدًا بعينه (`mukhalafa_exactly_one`)؛ ونفيُ الجمع أحدُ النفيين (`nafy_waw`).

## ٣. التخصيصُ المتّصل ومفهومُ الشرط (`K_*`)

الحكمُ العامّ مجالٌ (`α → Bool`)؛ والتخصيصُ «يخرج» منه: الاستثناءُ ما بعد «إلّا»، والشرطُ «ما لولاه لبقي»،
والصفةُ «ما عداها»، والغايةُ «ما بعدها» (على المرتَّب). المبرهَن لكلّ مجالٍ ولكلّ حكم: كلُّ تخصيصٍ داخلَ العامّ
(`istithna_sub`، `shart_sub`، `sifa_sub`، `ghaya_sub`) — يُخرج ولا يُدخل؛ والتخصيصاتُ تتبادل (`sifa_shart_comm`،
`istithna_comm`) ولا يتغيّر المخصَّص بتكراره (`istithna_idem`)؛ والشرطُ ومفهومُه قسمةٌ تامّةٌ للعامّ
(`shart_mafhum_partition`، `shart_mafhum_disjoint`)؛ والغايةُ تُخرج حدَّها نفسَه (`ghaya_excludes_bound`) وتتّسع
باتّساعه (`ghaya_mono`).

## ٤. العموم (`U_*`)

صيغُ العموم بأنفسها بمجالها (كلُّ شيء، العاقل، غيرُ العاقل، المكان، الزمان) وشرطِها في دورها: أيٌّ ومَن عامّتان
شرطيّتين أو استفهاميّتين لا موصولتين (`ayy_man_need_role`)، وما عامّةٌ إلّا موصوفةً أو تعجّبيّة وموصولتُها عامّة
بشاهد النصّ «اشتر ما رأيت» (`ma_mawsula_umum`). والنكرةُ في سياق النفي تعمّ: نفيُ الوجود عمومُ النفي على كلّ مجالٍ
منتهٍ (`nakira_nafy_umum`).
-/

namespace Slge.Bawwabat

/-! ## ١. الزمن -/

/-- الأوقاتُ الأربعة: ماضٍ، ماضٍ قريبٌ من الحال، حال، مستقبل. مجموعةُ الأوقات أربعةُ أعلام. -/
structure Azmina where
  madi : Bool
  qarib : Bool
  hal : Bool
  mustaqbal : Bool
  deriving DecidableEq, Repr

def Azmina.inter (a b : Azmina) : Azmina :=
  ⟨a.madi && b.madi, a.qarib && b.qarib, a.hal && b.hal, a.mustaqbal && b.mustaqbal⟩

def Azmina.sub (a b : Azmina) : Bool :=
  (!a.madi || b.madi) && (!a.qarib || b.qarib) && (!a.hal || b.hal) && (!a.mustaqbal || b.mustaqbal)

def Azmina.disj (a b : Azmina) : Bool := a.inter b == ⟨false, false, false, false⟩

def Azmina.size (a : Azmina) : Nat :=
  a.madi.toNat + a.qarib.toNat + a.hal.toNat + a.mustaqbal.toNat

def past : Azmina := ⟨true, true, false, false⟩
def halMustaqbal : Azmina := ⟨false, false, true, true⟩
def mustaqbal : Azmina := ⟨false, false, false, true⟩
def hal : Azmina := ⟨false, false, true, false⟩
def qarib : Azmina := ⟨false, true, false, false⟩

/-- هيئةُ الفعل. -/
inductive Hayaa where
  | madi | mudari | amr
  deriving DecidableEq, Repr

def Hayaa.all : List Hayaa := [.madi, .mudari, .amr]

/-- زمنُ الهيئة (`Z_HAYAA`، `Z_FIL`)؛ الأمرُ لا يسمّي النصُّ زمنَه: `AMR_TIME_UNSOURCED`. -/
def zamanOf : Hayaa → Option Azmina
  | .madi => some past
  | .mudari => some halMustaqbal
  | .amr => none

/-- أدواتُ الزمن والنفي من ج3 (527–531، 539). -/
inductive Adat where
  | sin | sawfa | an | inShart | la | lan | lam | lamma | ma | inNafy | qad
  deriving DecidableEq, Repr

def Adat.all : List Adat := [.sin, .sawfa, .an, .inShart, .la, .lan, .lam, .lamma, .ma, .inNafy, .qad]

/-- مفتاحُ كلّ أداةٍ في `BawwabatTable`. -/
def Adat.key : Adat → String
  | .sin | .sawfa => "Z_FIL"
  | .an | .inShart => "T_ISTIQBAL"
  | .la => "N_LA" | .lan => "N_LAN" | .lam | .lamma => "N_LAM"
  | .ma => "N_MA" | .inNafy => "N_IN" | .qad => "T_QAD"

/-- فهرسُ الأداة في `Huruf.table`. -/
def Adat.harf : Adat → Nat
  | .sin => 45 | .sawfa => 46 | .an => 31 | .inShart => 43 | .la => 61 | .lan => 63
  | .lam => 62 | .lamma => 40 | .ma => 60 | .inNafy => 64 | .qad => 48

def Adat.nafy : Adat → Bool
  | .la | .lan | .lam | .lamma | .ma | .inNafy => true
  | _ => false

/-- الأداةُ على الهيئة؛ `none` = لا يذكر النصُّ دخولَها عليها. -/
def apply : Adat → Hayaa → Option Azmina
  | .sin, .mudari | .sawfa, .mudari | .an, .mudari | .inShart, .mudari => some mustaqbal
  | .la, .mudari | .lan, .mudari => some mustaqbal
  | .lam, .mudari | .lamma, .mudari => some past
  | .ma, .mudari => some hal
  | .ma, .madi => some qarib
  | .inNafy, .mudari | .inNafy, .madi => some hal
  | .qad, .madi => some qarib
  | _, _ => none

/-- تخليص: الناتجُ داخلَ زمن الهيئة. -/
def takhlis (a : Adat) (h : Hayaa) : Bool :=
  match apply a h, zamanOf h with
  | some z, some t => z.sub t
  | _, _ => false

/-- قلب: الناتجُ خارجَ زمن الهيئة كلّه. -/
def qalb (a : Adat) (h : Hayaa) : Bool :=
  match apply a h, zamanOf h with
  | some z, some t => z.disj t
  | _, _ => false

def pairs : List (Adat × Hayaa) := Adat.all.flatMap fun a => Hayaa.all.map fun h => (a, h)

/-- كلُّ عمليّةٍ معرَّفةٍ تخليصٌ أو قلبٌ ولا ثالث، ولا تجتمعان. -/
theorem takhlis_xor_qalb :
    pairs.all (fun p => (apply p.1 p.2).isNone || (takhlis p.1 p.2 != qalb p.1 p.2)) = true := by
  decide

/-- القلبُ ثلاثةُ أزواجٍ بأعيانها. -/
theorem qalb_exactly :
    pairs.filter (fun p => qalb p.1 p.2) = [(.lam, .mudari), (.lamma, .mudari), (.inNafy, .madi)] := by
  decide

/-- لا أداةَ على الأمر في النصّ. -/
theorem none_on_amr : Adat.all.all (fun a => (apply a .amr).isNone) = true := by decide

/-- ما على الماضي ثلاث: ما، وإنِ النافية، وقد؛ وسائرُها على المضارع وحده. -/
theorem on_madi :
    Adat.all.filter (fun a => (apply a .madi).isSome) = [.ma, .inNafy, .qad] := by decide

theorem on_mudari :
    Adat.all.filter (fun a => (apply a .mudari).isSome) =
      [.sin, .sawfa, .an, .inShart, .la, .lan, .lam, .lamma, .ma, .inNafy] := by decide

/-- حروفُ الاستقبال الخمسة (539) على المضارع مستقبلٌ؛ ولا ولن من باب النفي موافقتان. -/
theorem istiqbal_group :
    [Adat.sin, .sawfa, .an, .la, .inShart, .lan].all (fun a => apply a .mudari == some mustaqbal) = true := by
  decide

/-- المضارعُ وقتان («الحاضر والمستقبل في اللفظ واحد»)، والماضي وقتان. -/
theorem mudari_two_points : (halMustaqbal).size = 2 ∧ past.size = 2 := by decide

/-- كلُّ تخليصٍ على المضارع يحسمه إلى وقتٍ واحد. -/
theorem takhlis_resolves_mudari :
    Adat.all.all (fun a => !takhlis a .mudari ||
      (match apply a .mudari with | some z => z.size == 1 | none => false)) = true := by decide

/-- الأزمنةُ المبلوغة: أزمنةُ الهيئات ونواتجُ الأدوات. -/
def reach : List Azmina :=
  ((Hayaa.all.filterMap zamanOf) ++ pairs.filterMap (fun p => apply p.1 p.2)).eraseDups

/-- الاستنفاد: خمسةُ أزمنةٍ لا سادسَ لها. -/
theorem reach_exhausted : reach = [past, halMustaqbal, mustaqbal, qarib, hal] := by decide

/-- النفيُ ستّ أدوات (527–531). -/
theorem nafy_six : Adat.all.filter Adat.nafy = [.la, .lan, .lam, .lamma, .ma, .inNafy] := by decide

/-- مفاتيحُ الأدوات في الجدول المرسى. -/
theorem adat_anchored : Adat.all.all (fun a => BawwabatTable.keys.contains a.key) = true := by decide

/-- الأداةُ في جدول الحروف الموحَّد. -/
theorem adat_in_huruf : Adat.all.all (fun a => a.harf < Huruf.table.length) = true := by decide

/-- موافقةُ معاني `Maani` (استخراجٌ مستقلٌّ بالمطابقة من المبحث نفسه): نفيُ الحال ⟼ {حال}، نفيُ المستقبل
وتأكيدُه ⟼ {مستقبل}، وقلبُ المضارع ⟼ قلب. -/
theorem agrees_with_maani :
    Maani.sensesOf (Adat.harf .ma) = [.nafyHal] ∧ apply .ma .mudari = some hal ∧
    Maani.sensesOf (Adat.harf .inNafy) = [.nafyHal] ∧ apply .inNafy .mudari = some hal ∧
    (Maani.sensesOf (Adat.harf .la)).head? = some .nafyMustaqbal ∧ apply .la .mudari = some mustaqbal ∧
    Maani.sensesOf (Adat.harf .lan) = [.takidMustaqbal] ∧ apply .lan .mudari = some mustaqbal ∧
    Maani.sensesOf (Adat.harf .lam) = [.qalbMadi] ∧ qalb .lam .mudari = true ∧
    Maani.sensesOf (Adat.harf .lamma) = [.qalbMadi] ∧ qalb .lamma .mudari = true := by decide

/-! ## ٢. العطف -/

/-- واقعةُ العطف: صدقُ المعطوف عليه والمعطوف، ووقتاهما. -/
structure Waqia where
  a : Bool
  b : Bool
  ta : Nat
  tb : Nat
  deriving DecidableEq, Repr

inductive Atf where
  | waw | fa | thumma | hatta | aw | am | la | bal | lakin
  deriving DecidableEq, Repr

def Atf.all : List Atf := [.waw, .fa, .thumma, .hatta, .aw, .am, .la, .bal, .lakin]

def Atf.key : Atf → String
  | .waw => "A_WAW" | .fa => "A_FA" | .thumma => "A_THUMMA" | .hatta => "A_HATTA"
  | .aw => "A_AW" | .am => "A_AM" | .la | .bal | .lakin => "A_MUKHALAFA"

/-- فهرسُ حرف العطف في `Huruf.table` (49–57). -/
def Atf.harf : Atf → Nat
  | .waw => 49 | .fa => 50 | .thumma => 51 | .hatta => 52 | .aw => 53 | .am => 54
  | .la => 55 | .bal => 56 | .lakin => 57

/-- صدقُ العطف على الواقعة. -/
def sidq : Atf → Waqia → Bool
  | .waw, w => w.a && w.b
  | .fa, w => w.a && w.b && w.tb == w.ta + 1
  | .thumma, w => w.a && w.b && decide (w.ta + 1 < w.tb)
  | .hatta, w => w.a && w.b && decide (w.ta < w.tb)
  | .aw, w => w.a || w.b
  | .am, w => w.a || w.b
  | .la, w | .bal, w | .lakin, w => w.a != w.b

/-- الأسلوبُ الذي يقع فيه الحرف (`A_AW`، `A_AM`). -/
inductive Siyaq where
  | khabar | amr | istifham
  deriving DecidableEq, Repr

def Atf.siyaq : Atf → List Siyaq
  | .am => [.istifham]
  | _ => [.khabar, .amr, .istifham]

def Waqia.swap (w : Waqia) : Waqia := ⟨w.b, w.a, w.tb, w.ta⟩

theorem waw_comm (w : Waqia) : sidq .waw w.swap = sidq .waw w := by
  simp [sidq, Waqia.swap, Bool.and_comm]

theorem fa_not_comm : ∃ w, sidq .fa w = true ∧ sidq .fa w.swap = false :=
  ⟨⟨true, true, 0, 1⟩, by decide, by decide⟩

theorem lt_split (ta tb : Nat) : decide (ta < tb) = ((tb == ta + 1) || decide (ta + 1 < tb)) := by
  rw [Bool.eq_iff_iff]
  simp only [decide_eq_true_eq, Bool.or_eq_true, beq_iff_eq]
  constructor <;> intro h <;> omega

theorem tartib_split (w : Waqia) : sidq .hatta w = (sidq .fa w || sidq .thumma w) := by
  obtain ⟨a, b, ta, tb⟩ := w
  cases a <;> cases b <;> simp only [sidq, Bool.true_and, Bool.false_and, Bool.false_or, Bool.and_self]
  exact lt_split ta tb

theorem fa_thumma_disjoint (w : Waqia) : (sidq .fa w && sidq .thumma w) = false := by
  obtain ⟨a, b, ta, tb⟩ := w
  cases a <;> cases b <;> simp only [sidq, Bool.true_and, Bool.false_and, Bool.and_false]
  rw [Bool.eq_false_iff]
  simp only [ne_eq, Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq]
  omega

theorem tartib_imp_waw (t : Atf) (ht : t = .fa ∨ t = .thumma ∨ t = .hatta) (w : Waqia)
    (h : sidq t w = true) : sidq .waw w = true := by
  rcases ht with rfl | rfl | rfl <;> simp_all [sidq]

theorem waw_imp_aw (w : Waqia) (h : sidq .waw w = true) : sidq .aw w = true := by
  simp_all [sidq]

theorem mukhalafa_exactly_one (t : Atf) (ht : t = .la ∨ t = .bal ∨ t = .lakin) (w : Waqia)
    (h : sidq t w = true) : (w.a = true ∧ w.b = false) ∨ (w.a = false ∧ w.b = true) := by
  rcases ht with rfl | rfl | rfl <;> cases ha : w.a <;> cases hb : w.b <;> simp_all [sidq]

/-- نفيُ الجمع أحدُ النفيين. -/
theorem nafy_waw (w : Waqia) : (!sidq .waw w) = sidq .aw ⟨!w.a, !w.b, w.ta, w.tb⟩ := by
  obtain ⟨a, b, ta, tb⟩ := w
  cases a <;> cases b <;> rfl

theorem am_istifham_only : Atf.siyaq .am = [.istifham] ∧ Atf.siyaq .aw = [.khabar, .amr, .istifham] := by
  decide

theorem atf_anchored : Atf.all.all (fun t => BawwabatTable.keys.contains t.key) = true := by decide

/-- موافقةُ `Maani`: الواو مطلقُ الجمع، والفاء وثمّ وحتّى الترتيب، وأو وأم التعليقُ بأحد، ولا وبل ولكن المخالفة. -/
theorem atf_agrees_with_maani :
    Maani.sensesOf (Atf.harf .waw) = [.mutlaqJam] ∧ Maani.sensesOf (Atf.harf .fa) = [.tartibTaqib] ∧
    Maani.sensesOf (Atf.harf .thumma) = [.tartibTarakhi] ∧
    (Maani.sensesOf (Atf.harf .hatta)).head? = some .tartib ∧
    (Maani.sensesOf (Atf.harf .aw)).head? = some .taliqBiAhad ∧
    Maani.sensesOf (Atf.harf .am) = [.taliqBiAhad] ∧
    [Atf.la, .bal, .lakin].all (fun t => Maani.sensesOf t.harf == [.mukhalafa]) = true := by decide

/-! ## ٣. التخصيصُ المتّصل ومفهومُ الشرط -/

section Takhsis
variable {α : Type}

/-- الاستثناء: إخراجُ ما بعد «إلّا» ممّا قبلها. -/
def istithna (amm m : α → Bool) (x : α) : Bool := amm x && !m x
/-- الشرط: يُخرج ما لولاه لبقي. -/
def shart (amm c : α → Bool) (x : α) : Bool := amm x && c x
/-- مفهومُ الشرط: نفيُ الحكم عند عدمه — مجالُ الحكم المنفيّ. -/
def mafhumShart (amm c : α → Bool) (x : α) : Bool := amm x && !c x
/-- الصفة: تُخرج ما عداها. -/
def sifa (amm s : α → Bool) (x : α) : Bool := amm x && s x

theorem istithna_sub (amm m : α → Bool) (x : α) (h : istithna amm m x = true) : amm x = true := by
  simp_all [istithna]
theorem shart_sub (amm c : α → Bool) (x : α) (h : shart amm c x = true) : amm x = true := by
  simp_all [shart]
theorem sifa_sub (amm s : α → Bool) (x : α) (h : sifa amm s x = true) : amm x = true := by
  simp_all [sifa]

theorem istithna_removes (amm m : α → Bool) (x : α) (h : m x = true) : istithna amm m x = false := by
  simp [istithna, h]

theorem sifa_shart_comm (amm s c : α → Bool) : sifa (shart amm c) s = shart (sifa amm s) c := by
  funext x; simp only [sifa, shart]; cases amm x <;> cases s x <;> cases c x <;> rfl

theorem istithna_comm (amm m n : α → Bool) : istithna (istithna amm m) n = istithna (istithna amm n) m := by
  funext x; simp only [istithna]; cases amm x <;> cases m x <;> cases n x <;> rfl

theorem istithna_idem (amm m : α → Bool) : istithna (istithna amm m) m = istithna amm m := by
  funext x; simp only [istithna]; cases amm x <;> cases m x <;> rfl

theorem shart_mafhum_partition (amm c : α → Bool) (x : α) :
    (shart amm c x || mafhumShart amm c x) = amm x := by
  simp only [shart, mafhumShart]; cases amm x <;> cases c x <;> rfl

theorem shart_mafhum_disjoint (amm c : α → Bool) (x : α) :
    (shart amm c x && mafhumShart amm c x) = false := by
  simp only [shart, mafhumShart]; cases amm x <;> cases c x <;> rfl

/-- النكرةُ في سياق النفي: نفيُ وجود ما يصدق عليه الحكم عمومُ النفي على المجال. -/
theorem nakira_nafy_umum (p : α → Bool) (dom : List α) : (!dom.any p) = dom.all (fun x => !p x) := by
  induction dom with
  | nil => rfl
  | cons y ys ih => simp [List.any_cons, List.all_cons, ← ih]

end Takhsis

/-- الغاية على المرتَّب: تُخرج ما بعدها — والحدُّ نفسُه بعدها («فحكم الليل الذي بعد إلى مخالف لما قبلها»). -/
def ghaya (amm : Nat → Bool) (g x : Nat) : Bool := amm x && decide (x < g)

theorem ghaya_sub (amm : Nat → Bool) (g x : Nat) (h : ghaya amm g x = true) : amm x = true := by
  simp_all [ghaya]

theorem ghaya_excludes_bound (amm : Nat → Bool) (g : Nat) : ghaya amm g g = false := by
  simp [ghaya]

theorem ghaya_mono (amm : Nat → Bool) (g g' x : Nat) (hg : g ≤ g') (h : ghaya amm g x = true) :
    ghaya amm g' x = true := by
  simp only [ghaya, Bool.and_eq_true, decide_eq_true_eq] at h ⊢
  exact ⟨h.1, by omega⟩

/-! ## ٤. العموم -/

/-- مجالُ العموم. -/
inductive Majal where
  | kull | aqil | ghayrAqil | amkina | zaman
  deriving DecidableEq, Repr

/-- دورُ الصيغة في جملتها. -/
inductive Dawr where
  | shart | istifham | mawsul | mawsuf | hal | munada | taajjub
  deriving DecidableEq, Repr

def Dawr.all : List Dawr := [.shart, .istifham, .mawsul, .mawsuf, .hal, .munada, .taajjub]

/-- صيغُ العموم بأنفسها (687) بأسمائها في النصّ. -/
def siyagh : List String := ["أي", "كل", "جميع", "الذين", "اللاتي", "من", "ما", "أين", "حيث", "متى"]

/-- العمومُ بالصيغة والدور (`U_SIYAGH`): أيٌّ ومَن بشرط الشرط أو الاستفهام؛ وما إلّا موصوفةً أو تعجّبيّة. -/
def umum (s : String) (d : Dawr) : Option Majal :=
  if s == "أي" then (if d == .shart || d == .istifham then some .kull else none)
  else if s == "من" then (if d == .shart || d == .istifham then some .aqil else none)
  else if s == "ما" then (if d == .mawsuf || d == .taajjub then none else some .ghayrAqil)
  else if s == "أين" || s == "حيث" then some .amkina
  else if s == "متى" then some .zaman
  else if siyagh.contains s then some .kull
  else none

theorem ayy_man_need_role :
    ["أي", "من"].all (fun s => Dawr.all.all fun d =>
      (umum s d).isSome == (d == .shart || d == .istifham)) = true := by decide

/-- «اشتر ما رأيت»: ما الموصولةُ عامّةٌ في غير العاقل؛ و«ما أحسن زيدًا» لا تعمّ. -/
theorem ma_mawsula_umum : umum "ما" .mawsul = some .ghayrAqil ∧ umum "ما" .taajjub = none := by decide

theorem umum_witnesses :
    umum "كل" .mawsul = some .kull ∧ umum "متى" .shart = some .zaman ∧
    umum "حيث" .shart = some .amkina ∧ umum "أي" .munada = none ∧ umum "رجل" .shart = none := by decide

theorem takhsis_anchored :
    ["K_MUTTASIL", "K_ISTITHNA", "K_SHART", "K_MAFHUM_SHART", "K_SIFA", "K_GHAYA", "U_SIYAGH",
      "U_NAFY", "Z_HAYAA"].all BawwabatTable.keys.contains = true := by decide

end Slge.Bawwabat
