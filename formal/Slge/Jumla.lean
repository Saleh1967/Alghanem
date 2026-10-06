import Slge.Huruf

/-!
# الجملةُ الاسميّة: طرفان مرفوعان، ورتبةٌ تُقرأ من الخانة، ومطابقةٌ عمليّات، ورابطٌ يُقرأ

* **د٤ الخانة**: المبتدأُ والخبرُ طرفان، والرفعُ عمليّةٌ واحدةٌ عليهما (`nominal`: `Nawasikh.raf` على كلٍّ)،
  تُقرأ رفعًا لكلّ جذع (`nominal_reads_raf`) وتحفظ الترخيص (`nominal_licensed`). صورُ المبتدأ الثلاث
  يقرؤها `mubtadaKind`: الضميرُ المنفصل من جدوله (`pronoun_is_damir`)، والاسمُ الظاهر من رفعه
  (`raf_is_ism`)؛ والمصدرُ المؤوّل تيارٌ (أَنْ + فعل) لا كلمةٌ — خارج القارئ باسمه. وصورُ الخبر الثلاث
  يقرؤها `khabarKind`: شبهُ الجملة من صدره (حرفُ جرٍّ من `Majrurat.harfs` أو ظرفٌ من `Zuruf`/`Zaman`)،
  والجملةُ الفعليّةُ من قالب الفعل (`isVerb`)، والمفردُ من رفعه.
* **د٨ الحدّ — الرتبة**: التقديمُ عمليّةٌ على الزوج (`swap`؛ `swap_swap`)، والرتبةُ دالّةٌ في الخانات لا في
  الموضع (`order`؛ `order_swap`): لامُ الابتداء تمسك المبتدأ (`order_lam` لكلّ مبتدأ وخبر)، وصدارةُ
  الاستفهام تقدّم الخبر، والنكرةُ مع شبه الجملة تقدّمه، والضميرُ العائدُ مع شبه الجملة تقدّمه، والخبرُ
  الفعليُّ يؤخّر، وتساوي الرتبة في المفرد يؤخّر، وما سواه جواز. والموضعُ المخالفُ للرتبة يُرفض
  (`admissible`؛ `lam_refuses_khabar_first`). الحصرُ بإلّا/إنّما تيارٌ (كلمتان) — خارج القارئ باسمه.
* **د١٦ — المطابقة**: التأنيثُ والتثنيةُ والجمعان عمليّاتٌ على الخبر (`taNith`، `dual`، `jamM`، `jamF`)
  تحفظ الترخيص (`ops_licensed`)، ويقرؤها الجنسُ والعددُ من اللاحقة بعد إسقاطها (`gender`، `number`:
  `gender_taNith`، `number_ops`)؛ والمطابقةُ تساوي القراءتين، فتطبيقُ العمليّة الواحدة على الطرفين
  يُطابق (`agree_ops`). استثناءُ جمع غير العاقل (الْجِبَالُ شَاهِقَةٌ) يقرؤه القالبُ احتمالًا
  (`brokenPlural`) والعقلُ معجم. والرابطُ في الخبر الجملة: ضميرٌ متّصل من جدول `Damair`، أو اسمُ إشارةٍ
  من جدول `Ishara`، أو إعادةُ اللفظ (المساواة)؛ والعمومُ معنًى (`rabit`؛ `rabit_repeat` لكلّ مبتدأ).
* **حذفُ الخبر**: لَوْلَا ولَعَمْرُكَ مودَعتان بشهادة البوّابة (`lawla_witness`)؛ والتقديرُ (كونٌ عامّ) معلَن.
* **التلاؤمُ الأنطولوجيّ** (رَجُلٌ طَوِيلٌ لا حَجَرٌ طَوِيلٌ) معجمٌ ودلالة: لا تقرؤه الخانة — باسمه.
القياسُ على MASAQ (أزواجُ المبتدأ والخبر بشهادات البوّابة) في بايثون.
-/

namespace Slge.Jumla

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-- الجملةُ الاسميّة: مبتدأٌ وخبرٌ، وعلمُ التقديم (الخبرُ أوّلًا). -/
structure Jumla where
  mubtada : List SCell
  khabar : List SCell
  khabarFirst : Bool := false
  deriving DecidableEq, Repr

/-! ## د٤ الخانة: الرفعُ عمليّةٌ واحدةٌ على الطرفين -/

def nominal (m k : List SCell) : Jumla := ⟨Nawasikh.raf m, Nawasikh.raf k, false⟩

theorem nominal_reads_raf (m k : List SCell) (hm : m ≠ []) (hk : k ≠ []) :
    Tawabi.caseClass (nominal m k).mubtada = .raf ∧ Tawabi.caseClass (nominal m k).khabar = .raf := by
  obtain ⟨i, a, hi⟩ := Nawasikh.setLast_eq_append m 2 hm
  obtain ⟨j, b, hj⟩ := Nawasikh.setLast_eq_append k 2 hk
  constructor
  · show Tawabi.caseClass (Nawasikh.raf m) = .raf
    unfold Nawasikh.raf; rw [hi]; exact Nawasikh.caseClass_of_last_damm i a
  · show Tawabi.caseClass (Nawasikh.raf k) = .raf
    unfold Nawasikh.raf; rw [hj]; exact Nawasikh.caseClass_of_last_damm j b

theorem nominal_licensed (m k : List SCell) (hm : licensed m = true) (hk : licensed k = true)
    (hm' : ∀ x, Afal.lastOf m = some x → x.state.val ≠ 3)
    (hk' : ∀ x, Afal.lastOf k = some x → x.state.val ≠ 3) :
    licensed (nominal m k).mubtada = true ∧ licensed (nominal m k).khabar = true :=
  ⟨Nawasikh.raf_licensed m hm hm', Nawasikh.raf_licensed k hk hk'⟩

/-- صورُ المبتدأ: ضميرٌ منفصل، اسمٌ ظاهرٌ مرفوع، اسمٌ ظاهرٌ مبنيٌّ من جداوله (الإشارة، الموصول،
الاستفهام)، وما سواه لا يُقرأ (المصدرُ المؤوّل تيار). -/
inductive MubtadaKind where
  | damir | ism | mabni | unread
  deriving DecidableEq, Repr

def mabniIsm (w : List SCell) : Bool :=
  Ishara.forms.any (fun p => p.2 == w) || Marifa.mawsul.any (fun p => p.2 == w) ||
    Istifham.forms.any (fun p => p.2 == w)

def mubtadaKind (w : List SCell) : MubtadaKind :=
  if Categories.pronouns.contains w then .damir
  else if mabniIsm w then .mabni
  else if Tawabi.caseClass w = .raf then .ism else .unread

theorem pronoun_is_damir : Categories.pronouns.all (fun p => mubtadaKind p == .damir) = true := by decide

/-- الاسمُ الظاهرُ المرفوع يُقرأ مبتدأً: ضميرًا أو مبنيًّا إن صادف جدولًا، وإلّا فاسمًا من رفعه. -/
theorem raf_is_ism (w : List SCell) (hne : w ≠ []) : mubtadaKind (Nawasikh.raf w) ≠ .unread := by
  obtain ⟨i, a, hi⟩ := Nawasikh.setLast_eq_append w 2 hne
  unfold mubtadaKind
  have h := Nawasikh.caseClass_of_last_damm i a
  unfold Nawasikh.raf; rw [hi, h]
  split <;> (try split) <;> simp

/-- صورُ الخبر: مفردٌ مرفوع، شبهُ جملة (صدرُها حرفُ جرٍّ أو ظرف)، جملةٌ فعليّة (قالبُ فعل). -/
inductive KhabarKind where
  | mufrad | shibhJumla | jumla | unread
  deriving DecidableEq, Repr

/-- الجارُّ قبل الضمير المتّصل: صورتُه في الوصل (لَ، إِلَيْ، عَلَيْ، لَدَيْ) أو صورتُه نفسُها. -/
def jarrBeforePronoun : List (List SCell) :=
  [[c 23 0], [c 0 1, c 23 0, c 28 3], [c 18 0, c 23 0, c 28 3], [c 23 0, c 8 0, c 28 3]] ++
    Majrurat.harfs.map (·.2)

/-- المتّصلةُ من جدول `Damair` وصورُ الهاء بالكسر بعد الياء والكسرة (هِ هِمْ هِمَا هِنَّ: بوّابة). -/
def aidSuffixes : List (List SCell) :=
  Damair.nasbSuffixes.map (·.2) ++ [[c 26 1], [c 26 1, c 24 3], [c 26 1, c 24 0, c 1 3], [c 26 1, c 25 3, c 25 0]]

def jarrPronoun (w : List SCell) : Bool :=
  aidSuffixes.any (fun p => jarrBeforePronoun.any (fun h => w == h ++ p))

/-- شبهُ الجملة من صدرها: حرفُ جرٍّ من خانتين فأكثر، أو متّصلٌ (بِ لِ كَ وَ تَ) تليه أل، أو جارٌّ وضميرٌ متّصل، أو ظرفٌ من جداوله.
المتّصلُ على نكرةٍ (بِزَيْدٍ) لا تفرّقه الخانةُ من حرفِ الأصل (كَرِيم) — باسمه. -/
def shibhJumla (w : List SCell) : Bool :=
  Majrurat.harfs.any (fun p => p.2.length ≥ 2 && p.2.isPrefixOf w) ||
    (Majrurat.harfs.take 5).any (fun p => p.2.isPrefixOf w && Marifa.hasAl (w.drop 1)) ||
    jarrPronoun w || Zuruf.forms.any (· == w) || Zaman.forms.any (· == w)

/-- قوالبُ الفعل في `Wazn.awzan`: المجرّدُ ومضارعُه وأمرُه (0–10)، والمزيدُ ومضارعُه (11–28). -/
def verbTemplates : List Nat := List.range 29

def isVerb (w : List SCell) : Bool := verbTemplates.any (fun k => Sarf.onTemplate (Sarf.templ k) w)

def khabarKind (w : List SCell) : KhabarKind :=
  if shibhJumla w then .shibhJumla
  else if isVerb w then .jumla
  else if Tawabi.caseClass w = .raf then .mufrad else .unread

/-- شواهد: نُورٌ مفرد، فِي الدَّارِ شبهُ جملة، دَرَسَ جملةٌ فعليّة، هُوَ ضمير، الْعِلْمُ اسم. -/
theorem kinds_witnesses :
    khabarKind [c 25 2, c 27 3, c 10 2, c 25 3] = .mufrad ∧
    khabarKind [c 20 1, c 28 3, c 0 0, c 8 3, c 8 0, c 1 3, c 10 1] = .shibhJumla ∧
    khabarKind [c 8 0, c 10 0, c 12 0] = .jumla ∧
    mubtadaKind [c 26 2, c 27 0] = .damir ∧
    mubtadaKind [c 0 0, c 23 3, c 18 1, c 23 3, c 24 2] = .ism ∧
    mubtadaKind Ishara.dha = .mabni ∧
    shibhJumla [c 2 1, c 0 0, c 23 3, c 2 0, c 28 3, c 3 1] = true ∧        -- بِالْبَيْتِ
    shibhJumla [c 23 0, c 26 2, c 24 3] = true ∧                             -- لَهُمْ (بوّابة)
    shibhJumla [c 0 1, c 23 0, c 28 3, c 26 1] = true ∧                      -- إِلَيْهِ (بوّابة)
    shibhJumla [c 22 0, c 10 1, c 28 3, c 24 2] = false := by decide         -- كَرِيمُ: لا تُقرأ شبهَ جملة

/-! ## د٨ الحدّ — الرتبة -/

inductive Rutba where
  | khabarFirst | mubtadaFirst | free
  deriving DecidableEq, Repr

theorem v23 : ((23 : Fin 29).val = 23) := rfl

def swap (j : Jumla) : Jumla := ⟨j.mubtada, j.khabar, !j.khabarFirst⟩

theorem swap_swap (j : Jumla) : swap (swap j) = j := by
  cases j; simp [swap]

def lam (w : List SCell) : List SCell := c 23 0 :: w

def startsLam : List SCell → Bool
  | x :: _ => x.carrier.val == 23 && x.state.val == 0
  | [] => false

theorem lam_licensed (w : List SCell) (hw : licensed w = true) : licensed (lam w) = true :=
  Rawabit.proclitic_keeps_licence _ 0 (by decide) w hw

/-- النكرةُ من الخانة: تنوينٌ بلا أل. -/
def nakira (w : List SCell) : Bool := Nida.hasTanwin w && !Marifa.hasAl w

def istifham (w : List SCell) : Bool := Istifham.forms.any (fun p => p.2 == w)

/-- الضميرُ العائدُ: متّصلٌ من جدول `Damair` في آخر المبتدأ. -/
def hasAidPronoun (w : List SCell) : Bool :=
  aidSuffixes.any (fun p => p.isSuffixOf w && p.length < w.length)

/-- الرتبةُ دالّةٌ في الخانات (لا في الموضع): كما في الحصر، 4 + 4 + الجواز. -/
def order (j : Jumla) : Rutba :=
  if startsLam j.mubtada then .mubtadaFirst                                   -- لامُ الابتداء
  else if istifham j.khabar then .khabarFirst                                  -- الصدارة
  else if nakira j.mubtada && shibhJumla j.khabar then .khabarFirst           -- النكرةُ المبهمة
  else if hasAidPronoun j.mubtada && shibhJumla j.khabar then .khabarFirst    -- الضميرُ العائد
  else if khabarKind j.khabar = .jumla then .mubtadaFirst                     -- الخبرُ الفعليّ
  else if khabarKind j.khabar ≠ .shibhJumla && nakira j.mubtada = nakira j.khabar then .mubtadaFirst
  else .free                                                                  -- الجواز

theorem order_swap (j : Jumla) : order (swap j) = order j := by
  cases j; rfl

/-- لامُ الابتداء تمسك المبتدأ في المقدمة لكلّ مبتدأ وخبر. -/
theorem order_lam (m k : List SCell) (b : Bool) : order ⟨lam m, k, b⟩ = .mubtadaFirst := by
  simp [order, lam, startsLam, c, v23]

/-- الموضعُ المقبول: ما وافق الرتبة؛ والجوازُ يقبل الوجهين. -/
def admissible (j : Jumla) : Bool :=
  match order j with
  | .khabarFirst => j.khabarFirst
  | .mubtadaFirst => !j.khabarFirst
  | .free => true

theorem lam_refuses_khabar_first (m k : List SCell) : admissible ⟨lam m, k, true⟩ = false := by
  simp [admissible, order_lam]

def rajul : List SCell := [c 10 0, c 5 2, c 23 2, c 25 3]                        -- رَجُلٌ
def fidDar : List SCell := [c 20 1, c 28 3, c 0 0, c 8 3, c 8 0, c 1 3, c 10 1]   -- فِي الدَّارِ
def ayna : List SCell := [c 0 0, c 28 3, c 25 0]                                  -- أَيْنَ (بوّابة)
def almafarr : List SCell := [c 0 0, c 23 3, c 24 0, c 20 0, c 10 3, c 10 2]      -- الْمَفَرُّ (بوّابة)
def zayd : List SCell := [c 11 0, c 28 3, c 8 2, c 25 3]                          -- زَيْدٌ
def qaim : List SCell := [c 21 0, c 1 3, c 0 1, c 24 2, c 25 3]                   -- قَائِمٌ
def darasa : List SCell := [c 8 0, c 10 0, c 12 0]                                -- دَرَسَ
def akhi : List SCell := [c 0 0, c 7 1, c 28 3]                                   -- أَخِي
def rafiqi : List SCell := [c 10 0, c 20 1, c 28 3, c 21 1, c 28 3]               -- رَفِيقِي
def tullabuha : List SCell := [c 16 2, c 23 3, c 23 0, c 1 3, c 2 2, c 26 0, c 1 3] -- طُلَّابُهَا
def fiMadrasa : List SCell := [c 20 1, c 28 3, c 0 0, c 23 3, c 24 0, c 8 3, c 10 0, c 12 0, c 3 1]
def salama : List SCell := [c 0 0, c 12 3, c 12 0, c 23 0, c 1 3, c 24 0, c 3 2]  -- السَّلَامَةُ
def fiTaanni : List SCell := [c 20 1, c 28 3, c 0 0, c 3 3, c 3 0, c 0 0, c 25 3, c 25 1, c 28 3]

/-- الثمانيةُ والجواز كما في الحصر: التقديمُ الحتميُّ (النكرة، الصدارة، العائد)، وتقديمُ المبتدأ
(الخبرُ الفعليّ، التساوي، لامُ الابتداء)، والجوازُ (المعرفةُ مع شبه الجملة). -/
theorem order_witnesses :
    order ⟨rajul, fidDar, true⟩ = .khabarFirst ∧
    order ⟨almafarr, ayna, true⟩ = .khabarFirst ∧
    order ⟨tullabuha, fiMadrasa, true⟩ = .khabarFirst ∧
    order ⟨zayd, darasa, false⟩ = .mubtadaFirst ∧
    order ⟨akhi, rafiqi, false⟩ = .mubtadaFirst ∧
    order ⟨lam zayd, qaim, false⟩ = .mubtadaFirst ∧
    order ⟨salama, fiTaanni, false⟩ = .free ∧
    admissible ⟨rajul, fidDar, false⟩ = false ∧ admissible ⟨salama, fiTaanni, true⟩ = true := by
  decide

/-! ## د١٦ — المطابقة: عمليّاتٌ على الخبر، وقراءةٌ من اللاحقة -/

inductive Gender where
  | masc | fem
  deriving DecidableEq, Repr

inductive Number where
  | single | dual | plural
  deriving DecidableEq, Repr

def taNith (w : List SCell) : List SCell := setLast w 0 ++ [c 3 2]            -- ـَةُ
def dual (w : List SCell) : List SCell := setLast w 0 ++ [c 1 3, c 25 1]      -- ـَانِ
def jamM (w : List SCell) : List SCell := setLast w 2 ++ [c 27 3, c 25 0]     -- ـُونَ
def jamF (w : List SCell) : List SCell := setLast w 0 ++ [c 1 3, c 3 2]       -- ـَاتُ

/-- العددُ من اللاحقة: َانِ/َيْنِ مثنًّى، ُونَ/ِينَ وَات جمعٌ، وما سواه مفرد (جمعُ التكسير قالبٌ: `brokenPlural`). -/
def number (w : List SCell) : Number :=
  match w.reverse with
  | n :: g :: p :: _ =>
      if n.carrier.val = 25 ∧ n.state.val = 1 ∧ g.state.val = 3 ∧ (g.carrier.val = 1 ∨ g.carrier.val = 28)
          ∧ p.state.val = 0 then .dual
      else if n.carrier.val = 25 ∧ n.state.val = 0 ∧ g.state.val = 3 ∧ (g.carrier.val = 27 ∨ g.carrier.val = 28)
          then .plural
      else if n.carrier.val = 3 ∧ g = c 1 3 ∧ p.state.val = 0 then .plural
      else if n.carrier.val = 25 ∧ n.state.val = 3 ∧ g.carrier.val = 3 ∧ p = c 1 3 then .plural
      else .single
  | _ => .single

/-- الجذعُ قبل اللاحقة (لقراءة الجنس تحتها). -/
def core (w : List SCell) : List SCell :=
  match number w with
  | .single => w
  | .dual => w.take (w.length - 2)
  | .plural => w.take (w.length - 2)

def endsWithAt (w : List SCell) : Bool :=
  match w.reverse with
  | n :: g :: _ => n.carrier.val == 3 && g == c 1 3
  | _ => false

/-- الجنس: جمعُ المؤنّث السالم (ـَات)، أو تاءُ التأنيث بعد فتحٍ في آخر الجذع (تحت التثنية والجمع). -/
def gender (w : List SCell) : Gender :=
  if number w = .plural ∧ endsWithAt w then .fem
  else match (core w).reverse with
    | t :: v :: _ => if t.carrier.val = 3 ∧ v.state.val = 0 then .fem else .masc
    | _ => .masc

/-- الجذعُ بلا أل (خانتا الهمزة واللام/الشمسيّة). -/
def bare (w : List SCell) : List SCell := if Marifa.hasAl w then w.drop 2 else w

/-- جمعُ التكسير احتمالًا: على قالبٍ من قوالب الجموع (83–100 ومنتهى الجموع). -/
def brokenPlural (w : List SCell) : Bool :=
  ((List.range 18).map (· + 83) ++ Sarf.muntaha).any
    (fun k => Sarf.onTemplate (Sarf.templ k) (setLast (bare w) 2))

def agree (m k : List SCell) : Bool := gender m == gender k && number m == number k

/-- استثناءُ الحصر: جمعُ غير العاقل مع مفردٍ مؤنّث أو جمعٍ مؤنّثٍ سالم — يقرؤه القالبُ احتمالًا والعقلُ معجم. -/
def agreeLoose (m k : List SCell) : Bool :=
  agree m k || (brokenPlural m && gender k == .fem && (number k == .single || number k == .plural))

theorem v3 : ((3 : Fin 29).val = 3) := rfl
theorem v25 : ((25 : Fin 29).val = 25) := rfl
theorem v27 : ((27 : Fin 29).val = 27) := rfl
theorem s3 : ((3 : Fin 4).val = 3) := rfl

theorem number_taNith (w : List SCell) (hne : w ≠ []) : number (taNith w) = .single := by
  obtain ⟨i, a, hi⟩ := Nawasikh.setLast_eq_append w 0 hne
  unfold taNith; rw [hi]
  simp only [number, List.append_assoc, List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.singleton_append]
  generalize i.reverse = r
  cases r <;> simp [c, v3]

theorem gender_taNith (w : List SCell) (hne : w ≠ []) : gender (taNith w) = .fem := by
  have hn := number_taNith w hne
  obtain ⟨i, a, hi⟩ := Nawasikh.setLast_eq_append w 0 hne
  unfold gender core; rw [hn]
  unfold taNith; rw [hi]
  simp [List.reverse_append, c, v3]

theorem number_ops (w : List SCell) (hne : w ≠ []) :
    number (dual w) = .dual ∧ number (jamM w) = .plural ∧ number (jamF w) = .plural := by
  obtain ⟨i, a, hi⟩ := Nawasikh.setLast_eq_append w 0 hne
  obtain ⟨j, b, hj⟩ := Nawasikh.setLast_eq_append w 2 hne
  unfold dual jamM jamF; rw [hi, hj]
  simp [number, List.reverse_append, c, v3, v25, v27, s3]

theorem gender_jamF (w : List SCell) (hne : w ≠ []) : gender (jamF w) = .fem := by
  have hn := (number_ops w hne).2.2
  obtain ⟨i, a, hi⟩ := Nawasikh.setLast_eq_append w 0 hne
  unfold gender; rw [hn]
  unfold jamF; rw [hi]
  simp [endsWithAt, List.reverse_append, c, v3]

/-- العمليّةُ الواحدةُ على الطرفين تُطابق: الجنسُ والعددُ يُقرآن من اللاحقة نفسِها (التأنيثُ وجمعُه
مطابقةٌ تامّة؛ والتثنيةُ وجمعُ المذكّر يساويان العدد، والجنسُ تحتهما من الجذع). -/
theorem agree_ops (m k : List SCell) (hm : m ≠ []) (hk : k ≠ []) :
    agree (taNith m) (taNith k) = true ∧ agree (jamF m) (jamF k) = true ∧
    number (dual m) = number (dual k) ∧ number (jamM m) = number (jamM k) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp [agree, gender_taNith m hm, gender_taNith k hk, number_taNith m hm, number_taNith k hk]
  · simp [agree, gender_jamF m hm, gender_jamF k hk, (number_ops m hm).2.2, (number_ops k hk).2.2]
  · rw [(number_ops m hm).1, (number_ops k hk).1]
  · rw [(number_ops m hm).2.1, (number_ops k hk).2.1]

theorem suffix_licensed (w suffix : List SCell) (st : Fin 4) (hst : st.val ≠ 3) (hw : licensed w = true)
    (hne : w ≠ []) (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) (hs : noAdj suffix = true) :
    licensed (setLast w st ++ suffix) = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w st hne
  have h1 : licensed (setLast w st) = true := by rw [Zuruf.setLast_licensed w st hst hlast]; exact hw
  refine Damair.attach_licensed _ _ h1 hs (by rw [hi]; simp) ?_
  intro x y hx _
  rw [hi] at hx; simp at hx; subst hx; simp [SCell.isSukun, hst]

/-- العمليّاتُ الأربع تحفظ الترخيص. -/
theorem ops_licensed (w : List SCell) (hw : licensed w = true) (hne : w ≠ [])
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) :
    licensed (taNith w) = true ∧ licensed (dual w) = true ∧ licensed (jamM w) = true ∧
    licensed (jamF w) = true :=
  ⟨suffix_licensed w _ 0 (by decide) hw hne hlast (by decide),
   suffix_licensed w _ 0 (by decide) hw hne hlast (by decide),
   suffix_licensed w _ 2 (by decide) hw hne hlast (by decide),
   suffix_licensed w _ 0 (by decide) hw hne hlast (by decide)⟩

def talib : List SCell := [c 16 0, c 1 3, c 23 1, c 2 2]            -- طَالِبُ
def mujtahid : List SCell := [c 24 2, c 5 3, c 3 0, c 26 1, c 8 2]  -- مُجْتَهِدُ
def jibal : List SCell := [c 0 0, c 23 3, c 5 1, c 2 0, c 1 3, c 23 2]  -- الْجِبَالُ
def shahiqa : List SCell := [c 13 0, c 1 3, c 26 1, c 21 0, c 3 2]  -- شَاهِقَةُ

/-- الطَّالِبُ مُجْتَهِدٌ / الطَّالِبَةُ مُجْتَهِدَةٌ / الطَّالِبَانِ مُجْتَهِدَانِ / الطُّلَّابُ مُجْتَهِدُونَ؛
والْجِبَالُ شَاهِقَةٌ بالاستثناء (فِعَال من قوالب الجمع) لا بالمطابقة. -/
theorem agree_witnesses :
    agree talib mujtahid = true ∧ agree (taNith talib) (taNith mujtahid) = true ∧
    agree (dual talib) (dual mujtahid) = true ∧ agree (jamM talib) (jamM mujtahid) = true ∧
    agree talib (taNith mujtahid) = false ∧
    agree jibal shahiqa = false ∧ agreeLoose jibal shahiqa = true ∧
    gender (dual (taNith talib)) = .fem := by decide

/-! ## الرابطُ في الخبر الجملة -/

inductive Rabit where
  | damir | ishara | repeat | unread
  deriving DecidableEq, Repr

/-- ضمائرُ الربط: المتّصلةُ للنصب والجرّ، والمتّصلةُ للرفع (`Damair.rafSuffixes`)، ولواحقُ المضارع
(ُونَ ِينَ َانِ). -/
def rabitSuffixes : List (List SCell) :=
  aidSuffixes ++ Damair.rafSuffixes.map (·.2) ++ [[c 27 3, c 25 0], [c 28 3, c 25 0], [c 1 3, c 25 1]]

/-- الرابطُ بين المبتدأ وكلمةٍ من جملة الخبر: ضميرٌ متّصلٌ بها، أو هي اسمُ إشارة، أو هي المبتدأُ بلفظه. -/
def rabit (m w : List SCell) : Rabit :=
  if w == m then .repeat
  else if Ishara.forms.any (fun p => p.2 == w) then .ishara
  else if rabitSuffixes.any (fun p => p.isSuffixOf w && p.length < w.length) then .damir else .unread

theorem rabit_repeat (m : List SCell) : rabit m m = .repeat := by simp [rabit]

def haqqa : List SCell := [c 0 0, c 23 3, c 6 0, c 1 3, c 21 3, c 21 0, c 3 2]  -- الْحَاقَّةُ (بوّابة)
def abuhu : List SCell := [c 0 0, c 2 2, c 27 3, c 26 2]                       -- أَبُوهُ

/-- الْحَاقَّةُ مَا الْحَاقَّةُ (إعادةُ اللفظ)، زَيْدٌ أَبُوهُ مُسَافِرٌ (الضمير)، ذَٰلِكَ خَيْرٌ (الإشارة). -/
theorem rabit_witnesses :
    rabit haqqa haqqa = .repeat ∧ rabit zayd abuhu = .damir ∧
    rabit zayd (((Ishara.forms.find? (·.1 == "ذَلِكَ")).map (·.2)).getD []) = .ishara ∧
    rabit zayd darasa = .unread := by decide

/-! ## حذفُ الخبر -/

def lawla : List SCell := [c 23 0, c 27 3, c 23 0, c 1 3]              -- لَوْلَا (بوّابة)
def laAmruka : List SCell := [c 23 0, c 18 0, c 24 3, c 10 2, c 22 0]  -- لَعَمْرُكَ (بوّابة)

/-- لَوْلَا وَلَعَمْرُكَ مرخَّصتان؛ وما بعدهما مبتدأٌ خبرُه محذوفٌ — التقديرُ معلَن. -/
theorem lawla_witness : licensed lawla = true ∧ licensed laAmruka = true ∧
    startsLam laAmruka = true := by decide

end Slge.Jumla
