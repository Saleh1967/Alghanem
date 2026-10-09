import Slge.NabhaniTable

/-!
# تقسيماتُ النبهانيّ أنماطًا: الدالُّ وحده، الدالُّ والمدلول، المدلولُ وحده — والترجيحُ عند التعارض

المصدرُ «أبحاث اللغة» (الشخصيّة الإسلاميّة ج3) مختومًا؛ الجدولُ `NabhaniTable` مولَّدٌ منه بأسطره وعباراته.
هنا الأنماطُ بأسمائها، وكلُّ نمطٍ **مربوطٌ بالنصّ**: قائمةُ أسمائه هي عباراتُ بحثه في الجدول بترتيبها
(`*_from_text`، بـ`decide`) — فلا منشئَ من الذاكرة.

* **الدالُّ وحده** (ف401): الدلالاتُ الثلاث (`Dalala`) والتراكيبُ الثلاثة (`Tarkib`)، والمفردُ اسمٌ وفعلٌ وحرف،
  والمركّبُ ستّةٌ «من أقسام الدالّ وحده» (`Murakkab`).
* **المدلولُ وحده** (ف409): خمسةُ أنواعٍ لما يُشار إليه (`Madlul`)، وفيها `muhmalMurakkab` = **الهذيان**: «موجودٌ
  غيرُ موضوع» — المرخَّصُ بلا حكم.
* **الدالُّ والمدلول** (ف418): سبعة (`DallMadlul`)؛ والنِّسَبُ الثلاث التي وُضع اللفظُ ليفيدها (`Nisba`، ف393).
* **الترجيح** (ف485–496): خمسةُ احتمالاتٍ تخلّ بالفهم (`Ihtimal`) وعشرةُ أوجهٍ بنصّه: التخصيصُ أولى من الكلّ،
  والمجازُ والإضمارُ سيّان، ثمّ النقل، ثمّ الاشتراك — `awla` رتبةٌ (`rank`)، والأوجهُ العشرةُ مبرهنةٌ واحدةً
  (`ten_rules`)، والرتبةُ ترتيبٌ شبهُ تامّ: متعدٍّ (`awla_trans`)، غيرُ انعكاسيّ (`awla_irrefl`)، وكلُّ اثنين إمّا
  أولى أحدُهما أو سيّان (`awla_total`)، ولا سيّان إلّا المجازُ والإضمار (`tie_only_majaz_idmar`).
-/

namespace Slge.Nabhani

inductive Dalala where
  | mutabaqa | tadammun | iltizam
  deriving DecidableEq, Repr

def Dalala.name : Dalala → String
  | .mutabaqa => "دلالة المطابقة" | .tadammun => "دلالة التضمن" | .iltizam => "دلالة الالتزام"

def Dalala.all : List Dalala := [.mutabaqa, .tadammun, .iltizam]

/-- المنطوقُ مطابقةٌ وتضمّن؛ والمفهومُ الالتزام (ف549، 551). -/
def Dalala.mantuq : Dalala → Bool
  | .iltizam => false | _ => true

inductive Tarkib where
  | isnad | mazj | idafa
  deriving DecidableEq, Repr

def Tarkib.name : Tarkib → String
  | .isnad => "تركيب إسناد" | .mazj => "تركيب مزج" | .idafa => "تركيب إضافة"

def Tarkib.all : List Tarkib := [.isnad, .mazj, .idafa]

/-- المركّبُ ستّةٌ بالوضع؛ الطلبُ أوّلًا (استفهامٌ للماهيّة، وتحصيلُها استعلاءً/تساويًا/تذلُّلًا) ثمّ الخبرُ وما
لا يحتمل الصدقَ والكذب. -/
inductive Murakkab where
  | istifham | amr | iltimas | sual | khabar | tanbih
  deriving DecidableEq, Repr

def Murakkab.name : Murakkab → String
  | .istifham => "الاستفهام" | .amr => "الأمر" | .iltimas => "الالتماس" | .sual => "السؤال"
  | .khabar => "الخبر" | .tanbih => "التنبيه"

def Murakkab.all : List Murakkab := [.istifham, .amr, .iltimas, .sual, .khabar, .tanbih]

/-- طلبٌ بالوضع: الأربعةُ الأُوَل. -/
def Murakkab.talab : Murakkab → Bool
  | .khabar => false | .tanbih => false | _ => true

/-- الأمرُ والالتماسُ والسؤالُ صيغةٌ واحدة (طلبُ تحصيل الماهيّة) يفرّقها المقام — على الخانات واحدة. -/
def Murakkab.tahsil : Murakkab → Bool
  | .amr => true | .iltimas => true | .sual => true | _ => false

/-- المدلولُ وحده خمسة: معنًى، أو لفظٌ مفردٌ مستعمل/مهمل، أو لفظٌ مركّبٌ مستعمل/مهمل (الهذيان). -/
inductive Madlul where
  | mana | mufradMustamal | mufradMuhmal | murakkabMustamal | muhmalMurakkab
  deriving DecidableEq, Repr

def Madlul.name : Madlul → String
  | .mana => "مدلول اللفظ معنى" | .mufradMustamal => "لفظاً مفرداً مستعملاً"
  | .mufradMuhmal => "لفظاً مفرداً مهملاً" | .murakkabMustamal => "لفظاً مركباً مستعملاً"
  | .muhmalMurakkab => "لفظاً مركباً مهملاً"

def Madlul.all : List Madlul :=
  [.mana, .mufradMustamal, .mufradMuhmal, .murakkabMustamal, .muhmalMurakkab]

/-- الهذيانُ: مركّبٌ مهمل — «لا يدلّ مجموعُ الكلام من حيث هو على معنًى وإن دلّ كلُّ جزء». -/
def Madlul.hadhayan : Madlul → Bool
  | .muhmalMurakkab => true | _ => false

/-- الدالُّ والمدلولُ سبعة. -/
inductive DallMadlul where
  | munfarid | mutabayin | mutaradif | mushtarak | manqul | haqiqa | majaz
  deriving DecidableEq, Repr

def DallMadlul.name : DallMadlul → String
  | .munfarid => "المنفرد" | .mutabayin => "المتباين" | .mutaradif => "المترادف"
  | .mushtarak => "المشترك" | .manqul => "المنقول" | .haqiqa => "الحقيقة" | .majaz => "المجاز"

def DallMadlul.all : List DallMadlul :=
  [.munfarid, .mutabayin, .mutaradif, .mushtarak, .manqul, .haqiqa, .majaz]

/-- خلافُ الأصل بنصّه: الترادفُ والاشتراكُ والنقلُ والمجاز؛ والأصلُ الحقيقةُ والانفراد. -/
def DallMadlul.khilafAsl : DallMadlul → Bool
  | .mutaradif => true | .mushtarak => true | .manqul => true | .majaz => true | _ => false

/-- النِّسَبُ التي وُضع اللفظُ ليفيدها (ف393): إسناديّة، تقييديّة، إضافيّة — لا «تضمينيّة». -/
inductive Nisba where
  | isnadiyya | taqyidiyya | idafiyya
  deriving DecidableEq, Repr

def Nisba.all : List Nisba := [.isnadiyya, .taqyidiyya, .idafiyya]

/-- الاحتمالاتُ الخمسة التي تخلّ بالفهم. -/
inductive Ihtimal where
  | ishtirak | naql | majaz | idmar | takhsis
  deriving DecidableEq, Repr

def Ihtimal.name : Ihtimal → String
  | .ishtirak => "الاشتراك" | .naql => "النقل" | .majaz => "المجاز" | .idmar => "الإضمار"
  | .takhsis => "التخصيص"

def Ihtimal.all : List Ihtimal := [.ishtirak, .naql, .majaz, .idmar, .takhsis]

/-- الرتبةُ بنصّه: «كلُّ واحدٍ منها مرجوحٌ بالنسبة إلى كلّ ما بعده … إلّا الإضمارَ والمجازَ فهما سيّان». -/
def Ihtimal.rank : Ihtimal → Nat
  | .ishtirak => 0 | .naql => 1 | .majaz => 2 | .idmar => 2 | .takhsis => 3

/-- `a` أولى من `b`. -/
def awla (a b : Ihtimal) : Bool := b.rank < a.rank

/-- الأوجهُ العشرةُ بترتيبها في النصّ (الأوّل … العاشر). -/
theorem ten_rules :
    awla .naql .ishtirak ∧ awla .majaz .ishtirak ∧ awla .idmar .ishtirak ∧
    awla .takhsis .ishtirak ∧ awla .majaz .naql ∧ awla .idmar .naql ∧ awla .takhsis .naql ∧
    (awla .idmar .majaz = false ∧ awla .majaz .idmar = false) ∧
    awla .takhsis .majaz ∧ awla .takhsis .idmar := by decide

theorem awla_trans (a b c : Ihtimal) (h₁ : awla a b = true) (h₂ : awla b c = true) :
    awla a c = true := by
  simp only [awla, decide_eq_true_eq] at *; omega

theorem awla_irrefl (a : Ihtimal) : awla a a = false := by simp [awla]

theorem awla_total (a b : Ihtimal) : awla a b = true ∨ awla b a = true ∨ a.rank = b.rank := by
  simp only [awla, decide_eq_true_eq]; omega

/-- لا سيّان إلّا المجازُ والإضمار. -/
theorem tie_only_majaz_idmar (a b : Ihtimal) (h : a ≠ b) (hr : a.rank = b.rank) :
    (a = .majaz ∧ b = .idmar) ∨ (a = .idmar ∧ b = .majaz) := by
  cases a <;> cases b <;> simp_all [Ihtimal.rank]

/-- التخصيصُ أولى من كلّ ما سواه، والاشتراكُ مرجوحٌ عند كلّ ما سواه. -/
theorem takhsis_top (a : Ihtimal) (h : a ≠ .takhsis) : awla .takhsis a = true := by
  cases a <;> simp_all [awla, Ihtimal.rank]

theorem ishtirak_bottom (a : Ihtimal) (h : a ≠ .ishtirak) : awla a .ishtirak = true := by
  cases a <;> simp_all [awla, Ihtimal.rank]

/-! ## الربطُ بالنصّ: أسماءُ الأنماط هي عباراتُ أبحاثها في الجدول المولَّد -/

theorem dalala_from_text :
    (NabhaniTable.phrases "الدال-وحده").take 3 = Dalala.all.map Dalala.name := by decide

theorem tarkib_from_text :
    (NabhaniTable.phrases "الدال-وحده").drop 4 = Tarkib.all.map Tarkib.name := by decide

theorem murakkab_from_text :
    ((NabhaniTable.phrases "المركب").drop 1).take 6 = Murakkab.all.map Murakkab.name := by decide

theorem madlul_from_text :
    (NabhaniTable.phrases "المدلول-وحده").take 5 = Madlul.all.map Madlul.name := by decide

theorem dallMadlul_from_text :
    (NabhaniTable.phrases "الدال-والمدلول").take 7 = DallMadlul.all.map DallMadlul.name := by
  decide

theorem ihtimal_from_text :
    (NabhaniTable.phrases "الترجيح").take 1 =
      ["الاشتراك، والنقل، والمجاز، والإضمار، والتخصيص"] ∧
    (Ihtimal.all.map Ihtimal.name) = ["الاشتراك", "النقل", "المجاز", "الإضمار", "التخصيص"] := by
  decide

/-- الأوجهُ العشرةُ بألفاظها في النصّ، بترتيب `ten_rules`. -/
theorem ten_rules_from_text :
    (NabhaniTable.phrases "الترجيح").drop 2 =
      ["النقل أولى من الاشتراك", "المجاز أولى من الاشتراك", "الإضمار أولى من الاشتراك",
       "التخصيص أولى من الاشتراك", "المجاز أولى من النقل", "الإضمار أولى من النقل",
       "التخصيص أولى من النقل", "الإضمار مثل المجاز", "التخصيص أولى من المجاز",
       "التخصيص أولى من الإضمار"] := by decide

theorem nisba_from_text :
    (NabhaniTable.phrases "الوضع-والنسب")[2]? =
      some "النسب الإسنادية، أو التقييدية، أو الإضافية" ∧ Nisba.all.length = 3 := by decide

/-- المركّبُ «من أقسام الدالّ وحده» بنصّه — فالخبرُ والإنشاءُ في جبر الدالّ. -/
theorem murakkab_is_dall :
    (NabhaniTable.phrases "المركب")[0]? = some "من أقسام الدال وحده" := by decide

theorem sections_count : NabhaniTable.sections.length = 20 := by decide

end Slge.Nabhani
