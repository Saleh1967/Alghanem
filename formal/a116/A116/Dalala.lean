import A116.Ishtiqaq

/-!
# الدلالاتُ الثلاث بين الجنس والصفة والوزن — الشخصيّة ج٣، «أبحاث اللغة»

**المصدر:** “الشخصية الاسلامية الجزء الثالث ورد (2).docx” في جذر هذا المستودع،
‏sha256 ‎`360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd`‎.
وأرقامُ الفقرات بين معقوفين هي ترقيمُ `pandoc -t plain --wrap=none` لهذا الملفّ
(سطرٌ لكلّ فقرة)؛ فـ[737] «تقسيم اللفظ باعتبار الدال وحده»، وهو الترقيمُ الذي
تحيل إليه وثائقُ المشروع.

**النطاق (المادّة ١٧):** كلُّ مبرهنةٍ في §١–§٣ هي على **كلّ** جدولِ وضعٍ مودَع
`T` وكلّ إيداعِ صيغٍ `S`، لا على اللغة. واللغةُ تُعرَف بالنقل لا بالعقل [729]؛
فـLean يبرهن ما يلزم عن الجدول، لا صحّةَ الجدول. وأجزاءُ الماهيّة واللوازمُ
«معلوماتٌ سابقة» [725] تُودَع بنوعها، لا تُستنتج هنا. و§٤ شاهدٌ واحدٌ منقولٌ من
أمثلة النصّ نفسه، فمبرهناتُه “مبرهنةٌ على الشاهد” لا “لكلّ”.

**ما ليس في النصّ ولا يُنسَب إليه:** لا ترد في مباحث اللغة (719–1106) ألفاظُ
“الفصل” ولا “العرض العامّ” ولا “الكلّيات”؛ و“الخاصّة” لا ترد إلا في [886]، في
سياق «الحقيقة العرفية الخاصة»، لا اسمًا لكلّيٍّ منطقيّ. فلا تُبنى هنا الكلّياتُ الخمس. و“الخواصّ” عند النبهاني
في هذا الجزء هي [725]: «حقائق الأشياء وخواصّها، أي … المعلومات التي يستعملها للحكم
على الأشياء» — فهي من جنس المعلومات السابقة، ومكانُها جدولُ الإيداع لا الوضع.

## ما يُبنى

* §١ الدلالات الثلاث [737]: المطابقةُ على تمام المسمّى، والتضمّنُ على جزئه،
  والالتزامُ على اللازم **الذهنيّ** لا الخارجيّ وحدَه، و«السببُ هو إطلاقُ اللفظ».
* §٢ الجنسُ والصفة [747] [818]: اسمُ الجنس يدلّ على ذاتٍ غير معيّنة «من غير
  اعتبار وصف»، والمشتقُّ يدلّ على «ذي صفةٍ معيّنة». والصفةُ نفسُها اسمُ جنس
  («السواد» من أمثلة الجنس في [747]، و«الأسود» من أمثلة المشتق).
* §٣ الوزن [741] [926] [895] [868]: الفعلُ يدلّ «بهيئته» على الزمان، و«الفعلُ
  عبارةٌ عن المصدر والزمان»، والاشتقاقُ «أن تصوغ من المصدر فعلًا أو اسم فاعل أو
  اسم مفعول». ومنها: الصفةُ التي يدلّ عليها المشتقُّ بالتضمّن هي الجنسُ الذي
  يدلّ عليه مصدرُه بالمطابقة، والصورةُ وحدها لا تعيّن التضمّن.
-/

namespace A116.Dalala

open A116.Ishtiqaq

/-! ## §١ المسمّى وأجزاؤه ولوازمه -/

/-- مسمّى الاسم الكلّيّ [747]: جنسٌ (ذاتٌ غير معيّنة) أو ذو صفةٍ معيّنة.
والصفةُ مُعرَّفةٌ بجنسها: «الأسود» ذو «السواد»، و«السواد» اسمُ جنس. -/
inductive Musamma (G : Type) where
  | jins : G → Musamma G
  | dhuSifa : G → Musamma G
  deriving DecidableEq, Repr

/-- ما يُقرأ جزءًا أو لازمًا: الذاتُ غيرُ المعيّنة، أو صفةٌ بجنسها، أو ذرّةٌ من
ذرّات المعلومات السابقة (كالحيوان والناطق في [737]). -/
inductive Mana (G A : Type) where
  | dhat : Mana G A
  | sifa : G → Mana G A
  | atom : A → Mana G A
  deriving DecidableEq, Repr

/-- جدولُ وضعٍ مودَع. `wad` من النقل [729] (`none` = لا قيدَ في المودَع، وهو
غيابٌ لا امتناع). والثلاثةُ الباقيةُ معلوماتٌ سابقةٌ مودَعة [725]. -/
structure Table (W G A : Type) where
  wad : W → Option (Musamma G)
  /-- أجزاءُ ماهيّة الجنس: الإنسانُ ↦ الحيوان، الناطق [737]. -/
  juzMahiya : G → A → Prop
  /-- ذرّاتٌ تُودَع جزءًا لذي الصفة؛ تُترك للإيداع ولا يُحكم فيها هنا. -/
  juzDhuSifa : G → A → Prop
  /-- اللازمُ الذهنيّ: «الذي ينتقل الذهنُ إليه عند سماع اللفظ» [737]. -/
  lazimDhihni : Musamma G → Mana G A → Prop
  /-- اللازمُ الخارجيّ؛ يُودَع ليُبرهَن أنّه وحده لا يُنتج دلالة. -/
  lazimKhariji : Musamma G → Mana G A → Prop

variable {W G A : Type}

/-- أجزاءُ المسمّى. اسمُ الجنس لا جزءَ صفةٍ فيه: «من غير اعتبار وصفٍ من
الأوصاف» [818]؛ ولا تُعدّ الذاتُ جزءًا منه لأنّها تمامُه [747]. وذو الصفة جزآه
الذاتُ والصفةُ المعيّنة [747]. -/
def Juz (T : Table W G A) : Musamma G → Mana G A → Prop
  | .jins g, .atom a => T.juzMahiya g a
  | .jins _, .dhat => False
  | .jins _, .sifa _ => False
  | .dhuSifa _, .dhat => True
  | .dhuSifa g, .sifa g' => g' = g
  | .dhuSifa g, .atom a => T.juzDhuSifa g a

/-- المطابقة: «دلالة اللفظ على تمام مسمّاه» [737]. -/
def Mutabaqa (T : Table W G A) (w : W) (c : Musamma G) : Prop :=
  T.wad w = some c

/-- التضمّن: «دلالة اللفظ على جزء المسمّى» [737]. -/
def Tadammun (T : Table W G A) (w : W) (m : Mana G A) : Prop :=
  ∃ c, T.wad w = some c ∧ Juz T c m

/-- الالتزام: دلالةُ اللفظ على لازمٍ **ذهنيّ** لمسمّاه [737]، خارجٍ عن أجزائه
(«في ضمن الموضوع له» مقابلَ «لازمًا للموضوع له»؛ والفصلُ بينهما هنا ترميزٌ
معلَن، وسندُه حصرُ المنطوق والمفهوم في [1032]). -/
def Iltizam (T : Table W G A) (w : W) (m : Mana G A) : Prop :=
  ∃ c, T.wad w = some c ∧ T.lazimDhihni c m ∧ ¬ Juz T c m

variable (T : Table W G A)

/-- «السببُ هو إطلاقُ اللفظ» [737]: لا تضمّنَ بلا وضعٍ للفظ. -/
theorem tadammun_needs_mutabaqa {w : W} {m : Mana G A} :
    Tadammun T w m → ∃ c, Mutabaqa T w c :=
  fun ⟨c, h, _⟩ => ⟨c, h⟩

/-- ولا التزامَ بلا وضعٍ للفظ: اللزومُ «شرطٌ وليس بموجِب» [737]. -/
theorem iltizam_needs_mutabaqa {w : W} {m : Mana G A} :
    Iltizam T w m → ∃ c, Mutabaqa T w c :=
  fun ⟨c, h, _, _⟩ => ⟨c, h⟩

/-- لفظٌ لا قيدَ له في الوضع لا يدلّ بتضمّنٍ ولا التزام. وهذا غيابُ دلالةٍ في
المودَع، لا حكمٌ بالامتناع في اللغة (المادّة ١٦). -/
theorem no_wad_no_dalala {w : W} (h : T.wad w = none) (m : Mana G A) :
    ¬ Tadammun T w m ∧ ¬ Iltizam T w m := by
  refine ⟨fun ⟨c, hc, _⟩ => ?_, fun ⟨c, hc, _, _⟩ => ?_⟩
  · rw [h] at hc; cases hc
  · rw [h] at hc; cases hc

/-- «ولا يأتي ذلك في اللازم الخارجيّ فقط» [737]: لازمٌ خارجيٌّ ليس ذهنيًّا لا
يُنتج التزامًا، ولو ثبت لزومُه في الخارج. -/
theorem khariji_alone_no_iltizam {w : W} {c : Musamma G} {m : Mana G A}
    (hw : T.wad w = some c) (_hk : T.lazimKhariji c m)
    (hd : ¬ T.lazimDhihni c m) : ¬ Iltizam T w m := by
  intro ⟨c', hc', hl, _⟩
  rw [hw] at hc'
  cases hc'
  exact hd hl

/-- التضمّنُ والالتزامُ لا يجتمعان على معنًى واحدٍ للفظٍ واحد: الأوّلُ منطوقٌ
والثاني مفهوم، «ولا يوجد غير ذلك» [1032]. -/
theorem tadammun_iltizam_disjoint {w : W} {m : Mana G A} :
    Tadammun T w m → Iltizam T w m → False := by
  intro ⟨c₁, h₁, hj⟩ ⟨c₂, h₂, _, hn⟩
  rw [h₁] at h₂
  cases h₂
  exact hn hj

/-! ## §٢ الجنسُ والصفة -/

/-- الجنسُ والمشتقّ قسمان للكلّيّ لا يجتمعان في لفظٍ واحد [747]. -/
theorem jins_not_mushtaqq {w : W} {g g' : G} :
    Mutabaqa T w (.jins g) → ¬ Mutabaqa T w (.dhuSifa g') := by
  intro h₁ h₂
  unfold Mutabaqa at h₁ h₂
  rw [h₁] at h₂
  cases h₂

/-- اسمُ الجنس لا يدلّ بالتضمّن على صفة: «من غير اعتبار وصفٍ من الأوصاف» [818]. -/
theorem jins_no_sifa_part {w : W} {g : G} (h : Mutabaqa T w (.jins g)) (s : G) :
    ¬ Tadammun T w (.sifa s) := by
  intro ⟨c, hc, hj⟩
  unfold Mutabaqa at h
  rw [h] at hc
  cases hc
  exact hj

/-- المشتقّ يدلّ بالتضمّن على صفته وعلى ذاتٍ غير معيّنة: «على ذي صفةٍ
معيّنة» [747]. -/
theorem mushtaqq_tadammun {w : W} {g : G} (h : Mutabaqa T w (.dhuSifa g)) :
    Tadammun T w (.sifa g) ∧ Tadammun T w .dhat :=
  ⟨⟨_, h, rfl⟩, ⟨_, h, trivial⟩⟩

/-- والصفةُ «معيّنة» [747]: لا يدلّ المشتقّ بالتضمّن على صفةٍ غيرِ صفته. -/
theorem mushtaqq_sifa_unique {w : W} {g g' : G} (h : Mutabaqa T w (.dhuSifa g)) :
    Tadammun T w (.sifa g') → g' = g := by
  intro ⟨c, hc, hj⟩
  unfold Mutabaqa at h
  rw [h] at hc
  cases hc
  exact hj

/-! ## §٣ الوزن -/

/-- الأزمنةُ الثلاثة [741]: «الماضي، أو الحال، أو المستقبل». -/
inductive Zaman where
  | madi
  | hal
  | mustaqbal
  deriving DecidableEq, Repr

/-- أدوارُ الصفة في المشتقّ [868]: اسمُ الفاعل واسمُ المفعول. -/
inductive Dawr where
  | faail
  | mafuul
  deriving DecidableEq, Repr

/-- ما تدلّ عليه **الهيئة** (الوزن): زمانٌ في الفعل [741]، أو لا زيادةَ على
الحدث في المصدر، أو دورٌ في المشتقّ [868]. -/
inductive Hayaa where
  | zaman : Zaman → Hayaa
  | masdar : Hayaa
  | mushtaqq : Dawr → Hayaa
  deriving DecidableEq, Repr

/-- إيداعُ الصيغ: ما تدلّ عليه هيئةُ كلّ قالب، وما يدلّ عليه كلُّ أصلٍ من حدثٍ
هو مصدرُه، مُعرَّفًا بجنسه («والحدثُ هو المصدر» [926]). -/
structure Sigha (G : Type) where
  hayaa : Template Char → Option Hayaa
  madda : Root Char → Option G

/-- جزآ الصيغة: ما من الهيئة، وما من الحدث. -/
inductive Part (G : Type) where
  | hayaa : Hayaa → Part G
  | hadath : G → Part G
  deriving DecidableEq, Repr

/-- التضمّنُ في الصيغة المحلَّلة بقالبٍ وأصل. -/
def TadS (S : Sigha G) (t : Template Char) (r : Root Char) : Part G → Prop
  | .hayaa h => S.hayaa t = some h ∧ ∃ g, S.madda r = some g
  | .hadath g => S.madda r = some g ∧ ∃ h, S.hayaa t = some h

/-- الفعل: ما دلّ **بهيئته** على أحد الأزمنة [741]. -/
def IsFil (S : Sigha G) (t : Template Char) : Prop :=
  ∃ z, S.hayaa t = some (.zaman z)

variable (S : Sigha G)

/-- ما تدلّ عليه الهيئةُ لا يتغيّر بتغيّر الأصل: هو للوزن لا للمادّة [741]. -/
theorem hayaa_part_uniform {t : Template Char} {r₁ r₂ : Root Char} {h : Hayaa}
    (h₁ : TadS S t r₁ (.hayaa h)) (h₂ : ∃ g, S.madda r₂ = some g) :
    TadS S t r₂ (.hayaa h) :=
  ⟨h₁.1, h₂⟩

/-- وما يدلّ عليه الحدثُ لا يتغيّر بتغيّر الوزن: هو المصدرُ المصوغُ منه [868]. -/
theorem hadath_part_uniform {t₁ t₂ : Template Char} {r : Root Char} {g : G}
    (h₁ : TadS S t₁ r (.hadath g)) (h₂ : ∃ h, S.hayaa t₂ = some h) :
    TadS S t₂ r (.hadath g) :=
  ⟨h₁.1, h₂⟩

/-- «الفعلُ عبارةٌ عن المصدر والزمان» [895]: أجزاءُ الفعل المحلَّل هذان لا غير. -/
theorem fil_parts {t : Template Char} {r : Root Char} {z : Zaman} {g : G}
    (ht : S.hayaa t = some (.zaman z)) (hr : S.madda r = some g) :
    (∀ g', TadS S t r (.hadath g') ↔ g' = g) ∧
    (∀ h, TadS S t r (.hayaa h) ↔ h = .zaman z) := by
  constructor
  · intro g'
    constructor
    · intro ⟨e, _⟩
      rw [hr] at e
      exact (Option.some.inj e).symm
    · intro e
      subst e
      exact ⟨hr, _, ht⟩
  · intro h
    constructor
    · intro ⟨e, _⟩
      rw [ht] at e
      exact (Option.some.inj e).symm
    · intro e
      subst e
      exact ⟨ht, _, hr⟩

/-- الزمانُ بالمادّة لا يجعل الكلمةَ فعلًا («أمس»، «الصبوح»): ما لم تدلّ
**الهيئةُ** على زمان فليس فعلًا، أيًّا كان الأصل [741]. -/
theorem not_fil_unless_hayaa {t : Template Char}
    (h : ∀ z, S.hayaa t ≠ some (.zaman z)) : ¬ IsFil S t :=
  fun ⟨z, hz⟩ => h z hz

/-- المسمّى الاسميّ للصيغة المحلَّلة: المصدرُ اسمُ جنسٍ لحدثه، والمشتقُّ ذو صفةٍ
هي ذلك الحدث [747] [868]، والفعلُ ليس اسمًا. -/
def ismOf (t : Template Char) (r : Root Char) : Option (Musamma G) :=
  match S.hayaa t, S.madda r with
  | some .masdar, some g => some (.jins g)
  | some (.mushtaqq _), some g => some (.dhuSifa g)
  | _, _ => none

/-- اتّساقُ جدول الوضع مع الاشتقاق: ما وُضع للصورة `fill t r` هو مسمّاها الاسميّ. -/
def Compositional (T : Table (List Char) G A) : Prop :=
  ∀ t r, T.wad (fill t r) = ismOf S t r

/-- **صفةُ المشتقّ هي جنسُ مصدره.** في كلّ جدولٍ متّسقٍ مع الاشتقاق: مصدرُ الأصل
يدلّ بالمطابقة على الجنس `g` ولا يدلّ على صفة، وكلُّ مشتقٍّ من الأصل نفسه يدلّ
بالتضمّن على `g` صفةً، ولا على صفةٍ غيرها [747] [818] [868]. -/
theorem sifa_of_mushtaqq_is_jins_of_masdar
    (T : Table (List Char) G A) (hc : Compositional S T)
    {tm td : Template Char} {r : Root Char} {g : G} {d : Dawr}
    (hm : S.hayaa tm = some .masdar) (hd : S.hayaa td = some (.mushtaqq d))
    (hr : S.madda r = some g) :
    Mutabaqa T (fill tm r) (.jins g) ∧
    (∀ s, ¬ Tadammun T (fill tm r) (.sifa s)) ∧
    Tadammun T (fill td r) (.sifa g) ∧
    (∀ g', Tadammun T (fill td r) (.sifa g') → g' = g) := by
  have em : Mutabaqa T (fill tm r) (.jins g) := by
    unfold Mutabaqa; rw [hc, ismOf, hm, hr]
  have ed : Mutabaqa T (fill td r) (.dhuSifa g) := by
    unfold Mutabaqa; rw [hc, ismOf, hd, hr]
  exact ⟨em, jins_no_sifa_part T em, (mushtaqq_tadammun T ed).1,
    fun _ => mushtaqq_sifa_unique T ed⟩

/-- جدولٌ مفهرَسٌ بالصورة متّسقٌ مع الاشتقاق يُلزِم كلَّ تحليلين لصورةٍ واحدة أن
يتّفقا في المسمّى. -/
theorem compositional_collision (T : Table (List Char) G A) (hc : Compositional S T)
    {t₁ t₂ : Template Char} {r₁ r₂ : Root Char} (e : fill t₁ r₁ = fill t₂ r₂) :
    ismOf S t₁ r₁ = ismOf S t₂ r₂ := by
  rw [← hc, ← hc, e]

/-- **الصورةُ وحدها لا تعيّن التضمّن.** “انْتَبَرَ” صورةٌ واحدةٌ لانفعل من (ت ب ر)
ولافتعل من (ن ب ر) (`form_alone_does_not_determine_root`)؛ فإن اختلف حدثا
الأصلين في الإيداع دلّ التحليلُ الأوّل بالتضمّن على حدثٍ لا يدلّ عليه الثاني.
فالدلالةُ على الحدث دالّةٌ في (الوزن، الأصل) لا في الصورة. -/
theorem surface_alone_does_not_determine_tadammun
    {h₁ h₂ : Hayaa} {g₁ g₂ : G}
    (ht₁ : S.hayaa t_past_VII = some h₁) (ht₂ : S.hayaa t_past_VIII = some h₂)
    (hr₁ : S.madda rootTBR = some g₁) (hr₂ : S.madda rootNBR = some g₂)
    (hne : g₁ ≠ g₂) :
    fill t_past_VII rootTBR = fill t_past_VIII rootNBR ∧
    TadS S t_past_VII rootTBR (.hadath g₁) ∧
    TadS S t_past_VIII rootNBR (.hadath g₂) ∧
    ¬ TadS S t_past_VIII rootNBR (.hadath g₁) := by
  refine ⟨form_alone_does_not_determine_root.1, ⟨hr₁, _, ht₁⟩, ⟨hr₂, _, ht₂⟩, ?_⟩
  intro ⟨e, _⟩
  rw [hr₂] at e
  exact hne (Option.some.inj e).symm

/-! ## §٤ الشاهد: أمثلةُ النصّ نفسِه [737] [747] [822]

كلُّ مدخلٍ هنا مثالٌ في الفقرة المذكورة بلفظه، لا غير. ومبرهناتُ هذا القسم
“مبرهنةٌ على الشاهد”. -/

/-- أجناسُ الشاهد: الإنسان، الفرس، السواد [747]؛ الأسد، السرير، العمى [737]؛
الضرب [822]. -/
inductive WG where
  | insan | faras | sawad | asad | sarir | ama | darb
  deriving DecidableEq, Repr

/-- ذرّاتُ الشاهد [737]: الحيوان، الناطق، الشجاعة، الارتفاع، البصر. -/
inductive WA where
  | hayawan | natiq | shajaa | irtifa | basar
  deriving DecidableEq, Repr

/-- ألفاظُ الشاهد [737] [747]. -/
inductive WW where
  | alInsan | alFaras | asSawad | alAswad | alAsad | asSarir | alAma
  deriving DecidableEq, Repr

def witWad : WW → Option (Musamma WG)
  | .alInsan => some (.jins .insan)
  | .alFaras => some (.jins .faras)
  | .asSawad => some (.jins .sawad)
  | .alAswad => some (.dhuSifa .sawad)
  | .alAsad => some (.jins .asad)
  | .asSarir => some (.jins .sarir)
  | .alAma => some (.jins .ama)

def witDhihni : Musamma WG → Mana WG WA → Bool
  | .jins .asad, .atom .shajaa => true
  | .jins .sarir, .atom .irtifa => true
  | .jins .ama, .atom .basar => true
  | _, _ => false

def witKhariji : Musamma WG → Mana WG WA → Bool
  | .jins .sarir, .atom .irtifa => true
  | _, _ => false

def witMahiya : WG → WA → Bool
  | .insan, .hayawan => true
  | .insan, .natiq => true
  | _, _ => false

/-- جدولُ الشاهد. -/
def wit : Table WW WG WA where
  wad := witWad
  juzMahiya := fun g a => witMahiya g a = true
  juzDhuSifa := fun _ _ => False
  lazimDhihni := fun c m => witDhihni c m = true
  lazimKhariji := fun c m => witKhariji c m = true

/-- «كدلالة الإنسان على الحيوان الناطق»، و«على الحيوان فقط، أو على الناطق
فقط» [737]. -/
theorem wit_insan :
    Mutabaqa wit .alInsan (.jins .insan) ∧
    Tadammun wit .alInsan (.atom .hayawan) ∧
    Tadammun wit .alInsan (.atom .natiq) :=
  ⟨rfl, ⟨_, rfl, rfl⟩, ⟨_, rfl, rfl⟩⟩

/-- «كدلالة الأسد على الشجاعة» [737]. -/
theorem wit_asad : Iltizam wit .alAsad (.atom .shajaa) :=
  ⟨_, rfl, rfl, fun h => by cases h⟩

/-- «كالسرير والارتفاع» لازمٌ ذهنيٌّ وخارجيّ، و«كالعمى والبصر» ذهنيٌّ غيرُ
خارجيّ؛ وكلاهما التزام [737]. -/
theorem wit_sarir_ama :
    (Iltizam wit .asSarir (.atom .irtifa) ∧ wit.lazimKhariji (.jins .sarir) (.atom .irtifa)) ∧
    (Iltizam wit .alAma (.atom .basar) ∧ ¬ wit.lazimKhariji (.jins .ama) (.atom .basar)) :=
  ⟨⟨⟨_, rfl, rfl, fun h => by cases h⟩, rfl⟩,
   ⟨⟨_, rfl, rfl, fun h => by cases h⟩, fun h => by cases h⟩⟩

/-- «السواد» جنسٌ و«الأسود» مشتقّ [747]: الأسودُ يدلّ بالتضمّن على السواد صفةً،
والسوادُ لا يدلّ على صفة. -/
theorem wit_sawad_aswad :
    Mutabaqa wit .asSawad (.jins .sawad) ∧
    (∀ s, ¬ Tadammun wit .asSawad (.sifa s)) ∧
    Tadammun wit .alAswad (.sifa .sawad) ∧
    Tadammun wit .alAswad .dhat :=
  ⟨rfl, jins_no_sifa_part wit rfl, (mushtaqq_tadammun wit (w := .alAswad) rfl).1,
    (mushtaqq_tadammun wit (w := .alAswad) rfl).2⟩

/-- قالبُ اسم الفاعل `1َا2ِ3` وقالبُ المصدر `1َ2ْ3`، والأصلُ (ض ر ب) [822]. -/
def t_faail : Template Char := [.slot 0, .lit 'َ', .lit 'ا', .slot 1, .lit 'ِ', .slot 2]
def t_masdar_fal : Template Char := [.slot 0, .lit 'َ', .slot 1, .lit 'ْ', .slot 2]
def rootDRB : Root Char := root3 'ض' 'ر' 'ب'

/-- «ضارب» و«الضرب» في [822] صورتان لأصلٍ واحد على قالبين سليمين. -/
theorem wit_drb_forms :
    WF t_faail ∧ WF t_masdar_fal ∧
    fill t_faail rootDRB = "ضَارِب".toList ∧
    fill t_masdar_fal rootDRB = "ضَرْب".toList := by
  decide

/-- إيداعُ صيغ الشاهد: قالبُ الفاعل دورُ فاعل، وقالبُ المصدر مصدر، والأصلُ
(ض ر ب) حدثُه الضرب. -/
def witSigha : Sigha WG where
  hayaa t := if t = t_faail then some (.mushtaqq .faail)
    else if t = t_masdar_fal then some .masdar else none
  madda r := if r 0 = 'ض' ∧ r 1 = 'ر' ∧ r 2 = 'ب' then some .darb else none

/-- «ضارب» يدلّ بالتضمّن على الضرب حدثًا وعلى الفاعليّة هيئةً، و«ضَرْب» يدلّ على
الحدث نفسِه بهيئةٍ لا زيادةَ فيها [822] [868]. -/
theorem wit_drb_parts :
    TadS witSigha t_faail rootDRB (.hadath .darb) ∧
    TadS witSigha t_faail rootDRB (.hayaa (.mushtaqq .faail)) ∧
    TadS witSigha t_masdar_fal rootDRB (.hadath .darb) ∧
    ismOf witSigha t_faail rootDRB = some (.dhuSifa .darb) ∧
    ismOf witSigha t_masdar_fal rootDRB = some (.jins .darb) := by
  refine ⟨⟨?_, .mushtaqq .faail, ?_⟩, ⟨?_, .darb, ?_⟩, ⟨?_, .masdar, ?_⟩, ?_, ?_⟩ <;> decide

end A116.Dalala
