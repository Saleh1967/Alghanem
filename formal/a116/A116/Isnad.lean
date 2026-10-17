/-!
# الحقيقة والمجاز في الاقتران: الحدث (المصدر) بذاتٍ من جنسٍ له خواصّ

**الدعوى (من المالك، 2026-10-17):** “الكلام والنطق والفهم مصدر، وهو إذا اقترن بالإنسان
حقيقة، سواء اقتران مصدرٍ أو مشتقّاتِ أسماءٍ أو مشتقّاتِ أفعال؛ ولكن إذا اقترن مصدرُ
الكلام والنطق والفهم مع الحجر أو الكلب أو القمر فهذا اقترانٌ يجعل الحقيقةَ ممتنعة،
لأنّ خواصّ الحجر وخواصّ الكلب وخواصّ القمر تجعل الحقيقة ممتنعة، ولذلك تُحمل على المجاز”.

**السند:**
* الشخصية ج٣ (sha256 ‎`360f7653…d5bd`‎، ترقيم pandoc):
  - [822] «لأن كلاً من الفعل والمشتق تابع لأصله وهو المصدر في كونه حقيقة أو مجازاً» —
    وهو سندُ أنّ الحكم لا يتغيّر بالصيغة (§٣).
  - [792] «أشاب الصغير… كرّ الغداة»: الإسناد «لغير من قام بهما» مجاز.
  - [794] العلاقة «لا بد أن تكون من أنواع العلاقة التي استعملتها العرب».
* «التفكير» (sha256 ‎`e917d9a0…492c`‎، ترقيم الفقرات بعد التحويل UTF-8):
  - [15] «والعقل هو من خواص الإنسان».
  - [27] «فدماغ الإنسان فيه خاصية الربط … ولكن الحيوان لا توجد لديه خاصية الربط».
  - [30] «فإن العقل غير موجود إلا عند الإنسان».
* سيبويه، الكتاب ج١ ص٢٦: «حَمَلتُ الجبلَ» مستقيمٌ **كذب** لا مجاز — فالامتناعُ وحده
  لا يُنتج مجازًا (§٢، `mumtani_without_rukhsa_is_not_majaz`).

**البناء:** طبقةُ حكمٍ فوق الوضع (المادّة ١٠). خواصُّ الأجناس وشروطُ الأحداث «معلوماتٌ
سابقة» مودَعة [725]، ثلاثيّةُ القيمة: ثابتة / منتفية بشاهد / غير مودَعة؛ و“غير مودَعة”
ليست امتناعًا (المادّة ١٦). والحكمُ ثلاثيُّ المُنشئات (المادّة ١٣): حقيقة / مجازٌ برخصة
مسمّاة / لا حكم بسببٍ مسمّى.

**ما ليس هنا:** لا يُبرهَن أنّ الحجر لا يتكلّم؛ ذلك سطرٌ في المودَع منسوبٌ إلى نصّه.
المبرهَن: ما يلزم عن أيّ مودَعٍ كذلك، والشاهدُ في §٤ مبرهنٌ على الشاهد.
-/

namespace A116.Isnad

/-- حالُ خاصّةٍ لجنسٍ في المودَع: ثابتة، أو منتفية بشاهد، أو غير مودَعة. -/
inductive Hal where
  | thabit
  | muntafin
  | ghayrMudaa
  deriving DecidableEq, Repr

/-- صيغةُ الاقتران: مصدر، أو اسمٌ مشتق، أو فعل. -/
inductive Sigha where
  | masdar
  | ismMushtaqq
  | fil
  deriving DecidableEq, Repr

/-- سببُ «لا حكم»: خاصّةٌ مشروطةٌ غيرُ مودَعة، أو امتناعٌ بلا علاقةٍ مسمّاة. -/
inductive Sabab where
  | khassaGhayrMudaa
  | mumtaniBilaAlaqa
  deriving DecidableEq, Repr

/-- الحكم ثلاثيّ المُنشئات (المادّة ١٣). -/
inductive Hukm (R : Type) where
  | haqiqa
  | majaz (rukhsa : R)
  | laHukm (sabab : Sabab)
  deriving DecidableEq, Repr

/-- مودَعُ المعلومات السابقة للاقتران.
* `shart h`: الخواصّ التي يشترطها الحدثُ `h` في الذات (قائمةٌ منتهية).
* `hal j k`: حالُ الخاصّة `k` في الجنس `j`.
* `rukhsa h j`: علاقةُ مجازٍ مسمّاة من أنواع العرب [794] لاقتران `h` بـ`j`، إن أُودعت. -/
structure Mudaa (H J K R : Type) where
  shart : H → List K
  hal : J → K → Hal
  rukhsa : H → J → Option R

variable {H J K R : Type}

/-- الحدثُ قابلٌ للذات: كلُّ خاصّةٍ يشترطها ثابتةٌ في جنسها. -/
def Qabil (D : Mudaa H J K R) (h : H) (j : J) : Prop :=
  ∀ k ∈ D.shart h, D.hal j k = .thabit

/-- الامتناعُ بشاهد: خاصّةٌ مشروطةٌ منتفيةٌ في الجنس انتفاءً مودَعًا. -/
def Mumtani (D : Mudaa H J K R) (h : H) (j : J) : Prop :=
  ∃ k ∈ D.shart h, D.hal j k = .muntafin

/-- الحكمُ على الأصل: الحدث مع الجنس، قبل أيّ صيغة. -/
def hukmAsl (D : Mudaa H J K R) (h : H) (j : J) : Hukm R :=
  match (D.shart h).any (fun k => D.hal j k == .muntafin), D.rukhsa h j,
      (D.shart h).all (fun k => D.hal j k == .thabit) with
  | true, some r, _ => .majaz r
  | true, none, _ => .laHukm .mumtaniBilaAlaqa
  | false, _, true => .haqiqa
  | false, _, false => .laHukm .khassaGhayrMudaa

/-- الحكمُ على الاقتران بصيغةٍ ما: تابعٌ لأصله [822]. -/
def hukm (D : Mudaa H J K R) (_s : Sigha) (h : H) (j : J) : Hukm R :=
  hukmAsl D h j

variable (D : Mudaa H J K R)

theorem any_muntafin_iff (h : H) (j : J) :
    (D.shart h).any (fun k => D.hal j k == .muntafin) = true ↔ Mumtani D h j := by
  simp [Mumtani, List.any_eq_true]

theorem all_thabit_iff (h : H) (j : J) :
    (D.shart h).all (fun k => D.hal j k == .thabit) = true ↔ Qabil D h j := by
  simp [Qabil, List.all_eq_true]

/-- القابليّةُ والامتناعُ لا يجتمعان. -/
theorem qabil_not_mumtani {h : H} {j : J} (hq : Qabil D h j) : ¬ Mumtani D h j := by
  intro ⟨k, hk, hkm⟩
  rw [hq k hk] at hkm
  cases hkm

/-- جدولُ الحالات الأربع، بلغة القابليّة والامتناع. -/
theorem hukm_cases (s : Sigha) (h : H) (j : J) :
    (Mumtani D h j → ∀ r, D.rukhsa h j = some r → hukm D s h j = .majaz r) ∧
    (Mumtani D h j → D.rukhsa h j = none → hukm D s h j = .laHukm .mumtaniBilaAlaqa) ∧
    (¬ Mumtani D h j → Qabil D h j → hukm D s h j = .haqiqa) ∧
    (¬ Mumtani D h j → ¬ Qabil D h j → hukm D s h j = .laHukm .khassaGhayrMudaa) := by
  have hA := any_muntafin_iff D h j
  have hB := all_thabit_iff D h j
  unfold hukm hukmAsl
  refine ⟨fun hm r hr => ?_, fun hm hr => ?_, fun hn hq => ?_, fun hn hq => ?_⟩
  · rw [hA.2 hm, hr]
  · rw [hA.2 hm, hr]
  · have e1 : (D.shart h).any (fun k => D.hal j k == .muntafin) = false := by
      cases e : (D.shart h).any (fun k => D.hal j k == .muntafin)
      · rfl
      · exact absurd (hA.1 e) hn
    rw [e1, hB.2 hq]
  · have e1 : (D.shart h).any (fun k => D.hal j k == .muntafin) = false := by
      cases e : (D.shart h).any (fun k => D.hal j k == .muntafin)
      · rfl
      · exact absurd (hA.1 e) hn
    have e2 : (D.shart h).all (fun k => D.hal j k == .thabit) = false := by
      cases e : (D.shart h).all (fun k => D.hal j k == .thabit)
      · rfl
      · exact absurd (hB.1 e) hq
    rw [e1, e2]

/-! ## §١ الحقيقة: القابليّةُ وحدها -/

/-- **الحقيقة ⟺ القابليّة.** يكون الاقترانُ حقيقةً إذا وفقط إذا ثبتت في جنس الذات كلُّ
خاصّةٍ يشترطها الحدث. -/
theorem haqiqa_iff_qabil (s : Sigha) (h : H) (j : J) :
    hukm D s h j = .haqiqa ↔ Qabil D h j := by
  obtain ⟨c1, c2, c3, c4⟩ := hukm_cases D s h j
  constructor
  · intro e
    by_cases hm : Mumtani D h j
    · cases hr : D.rukhsa h j with
      | none => rw [c2 hm hr] at e; cases e
      | some r => rw [c1 hm r hr] at e; cases e
    · by_cases hq : Qabil D h j
      · exact hq
      · rw [c4 hm hq] at e; cases e
  · intro hq
    exact c3 (qabil_not_mumtani D hq) hq

/-- **الامتناع يُسقط الحقيقة:** خاصّةٌ مشروطةٌ منتفيةٌ بشاهد ⟹ ليس حقيقة. -/
theorem mumtani_not_haqiqa {s : Sigha} {h : H} {j : J} (hm : Mumtani D h j) :
    hukm D s h j ≠ .haqiqa :=
  fun e => qabil_not_mumtani D ((haqiqa_iff_qabil D s h j).1 e) hm

/-! ## §٢ المجاز: امتناعٌ بشاهد **و**رخصةٌ مسمّاة -/

/-- **لا مجاز إلا بامتناعٍ ورخصة.** -/
theorem majaz_iff {s : Sigha} {h : H} {j : J} {r : R} :
    hukm D s h j = .majaz r ↔ Mumtani D h j ∧ D.rukhsa h j = some r := by
  obtain ⟨c1, c2, c3, c4⟩ := hukm_cases D s h j
  constructor
  · intro e
    by_cases hm : Mumtani D h j
    · cases hr : D.rukhsa h j with
      | none => rw [c2 hm hr] at e; cases e
      | some r' => rw [c1 hm r' hr] at e; cases e; exact ⟨hm, rfl⟩
    · by_cases hq : Qabil D h j
      · rw [c3 hm hq] at e; cases e
      · rw [c4 hm hq] at e; cases e
  · intro ⟨hm, hr⟩
    exact c1 hm r hr

/-- **الامتناعُ بلا رخصة ليس مجازًا** («حملتُ الجبل» مستقيمٌ كذب عند سيبويه):
حكمُه «لا حكم» بسببه المسمّى. -/
theorem mumtani_without_rukhsa_is_not_majaz {s : Sigha} {h : H} {j : J}
    (hm : Mumtani D h j) (hr : D.rukhsa h j = none) :
    hukm D s h j = .laHukm .mumtaniBilaAlaqa :=
  (hukm_cases D s h j).2.1 hm hr

/-- **الغيابُ ليس امتناعًا** (المادّة ١٦): إن لم تنتفِ خاصّةٌ بشاهد ولم تثبت كلُّها، فلا
حقيقة ولا مجاز، بل «لا حكم» لخاصّةٍ غير مودَعة. -/
theorem absence_is_not_mumtani {s : Sigha} {h : H} {j : J}
    (hn : ¬ Mumtani D h j) (hq : ¬ Qabil D h j) :
    hukm D s h j = .laHukm .khassaGhayrMudaa :=
  (hukm_cases D s h j).2.2.2 hn hq

/-- الحقيقة والمجاز لا يجتمعان على اقترانٍ واحد. -/
theorem haqiqa_majaz_exclusive {s : Sigha} {h : H} {j : J} {r : R}
    (e : hukm D s h j = .majaz r) : ¬ Qabil D h j :=
  fun hq => qabil_not_mumtani D hq ((majaz_iff D).1 e).1

/-! ## §٣ الصيغة لا تغيّر الحكم [822] -/

/-- **المصدرُ والاسمُ المشتقّ والفعلُ سواءٌ في الحكم:** «الفعل والمشتق تابع لأصله وهو
المصدر في كونه حقيقة أو مجازاً» [822]. -/
theorem hukm_independent_of_sigha (s₁ s₂ : Sigha) (h : H) (j : J) :
    hukm D s₁ h j = hukm D s₂ h j := rfl

/-! ## §٤ التحسين: إيداعُ ما لم يُودَع لا يقلب حكمًا قائمًا -/

/-- `D'` يُحسّن `D`: الشروطُ والرخصُ نفسُها، وكلُّ خاصّةٍ مودَعةٍ في `D` باقيةٌ في `D'`
على حالها؛ ولا يتغيّر إلا ما كان “غير مودَع”. -/
def Refines (D D' : Mudaa H J K R) : Prop :=
  D'.shart = D.shart ∧ D'.rukhsa = D.rukhsa ∧
  ∀ j k, D.hal j k ≠ .ghayrMudaa → D'.hal j k = D.hal j k

/-- **حكمٌ قائمٌ (حقيقة أو مجاز) ثابتٌ تحت كلّ تحسينٍ للمودَع.** فزيادةُ المعلومات السابقة
لا تنقض حقيقةً ولا مجازًا، وإنما تحسم ما كان «لا حكم» لغياب الشاهد. -/
theorem refines_preserves_decided {D D' : Mudaa H J K R} (hr : Refines D D')
    {s : Sigha} {h : H} {j : J}
    (hd : hukm D s h j = .haqiqa ∨ ∃ r, hukm D s h j = .majaz r) :
    hukm D' s h j = hukm D s h j := by
  obtain ⟨hs, hrk, hh⟩ := hr
  rcases hd with e | ⟨r, e⟩
  · have hq := (haqiqa_iff_qabil D s h j).1 e
    have hq' : Qabil D' h j := by
      intro k hk
      rw [hs] at hk
      rw [hh j k (by rw [hq k hk]; exact fun x => by cases x), hq k hk]
    rw [e]; exact (haqiqa_iff_qabil D' s h j).2 hq'
  · obtain ⟨⟨k, hk, hkm⟩, hrj⟩ := (majaz_iff D).1 e
    have hm' : Mumtani D' h j :=
      ⟨k, by rw [hs]; exact hk, by rw [hh j k (by rw [hkm]; exact fun x => by cases x), hkm]⟩
    rw [e]; exact (majaz_iff D').2 ⟨hm', by rw [hrk]; exact hrj⟩

/-! ## §٥ الشاهد: الكلام والنطق والفهم مع الإنسان والحجر والكلب والقمر

المودَع هنا منسوبٌ سطرًا سطرًا إلى نصّه؛ ومبرهناتُه “مبرهنةٌ على الشاهد”.
* الخاصّة الوحيدة المشروطة: **العقل/خاصّية الربط**؛ وشرطُها للفهم والنطق من «التفكير»
  [15] [27]؛ وشرطُها **للكلام** ترميزٌ معلَن منّي (الكلام «تعبيرٌ عمّا في الذهن»، ج٣
  [721])، لا نصٌّ في الشرط.
* ثبوتُها للإنسان [15] [27]، وانتفاؤها عن الحيوان (الكلب) [27]، وعن غير الإنسان كلِّه
  (الحجر، القمر) [30] «العقل غير موجود إلا عند الإنسان».
* الرخصة: لا علاقةَ مودَعة في هذا الشاهد؛ فإن أُودعت (مثلًا تشبيهٌ في “القمر يُكلّمني”)
  صار الحكمُ مجازًا بها، وهو موضعُ الإيداع لا الاستنتاج. -/

inductive Hadath where
  | kalam | nutq | fahm
  deriving DecidableEq, Repr

inductive Jins where
  | insan | hajar | kalb | qamar
  deriving DecidableEq, Repr

inductive Khassa where
  | aql
  deriving DecidableEq, Repr

/-- علاقةُ مجازٍ مسمّاة (من أنواع ج٣ [796]–[816])؛ والمشابهةُ مثالٌ [800]. -/
inductive Alaqa where
  | mushabaha
  deriving DecidableEq, Repr

def witHal : Jins → Khassa → Hal
  | .insan, .aql => .thabit
  | .hajar, .aql => .muntafin
  | .kalb, .aql => .muntafin
  | .qamar, .aql => .muntafin

/-- الشاهدُ بلا رخصةٍ مودَعة. -/
def wit : Mudaa Hadath Jins Khassa Alaqa where
  shart _ := [.aql]
  hal := witHal
  rukhsa _ _ := none

/-- الكلامُ والنطقُ والفهمُ مع الإنسان حقيقةٌ، بأيّ صيغة. -/
theorem wit_insan_haqiqa : ∀ (s : Sigha) (h : Hadath), hukm wit s h .insan = .haqiqa := by
  intro s h; cases s <;> cases h <;> decide

/-- ومع الحجر والكلب والقمر ممتنعةٌ الحقيقة، بأيّ صيغة. -/
theorem wit_not_haqiqa :
    ∀ (s : Sigha) (h : Hadath) (j : Jins), j ≠ .insan → hukm wit s h j ≠ .haqiqa := by
  intro s h j hj
  cases j <;> first | exact absurd rfl hj | (cases s <;> cases h <;> decide)

/-- وبلا رخصةٍ مودَعة ليست مجازًا بعد: «لا حكم» لامتناعٍ بلا علاقة. -/
theorem wit_no_rukhsa :
    hukm wit .fil .kalam .hajar = .laHukm .mumtaniBilaAlaqa := by decide

/-- فإن أُودعت رخصةُ المشابهة لاقتران الكلام بالقمر صار مجازًا بها، ولم يتغيّر غيرُه. -/
def witQamar : Mudaa Hadath Jins Khassa Alaqa :=
  { wit with rukhsa := fun h j => if h = .kalam ∧ j = .qamar then some .mushabaha else none }

theorem wit_qamar_majaz :
    hukm witQamar .ismMushtaqq .kalam .qamar = .majaz .mushabaha ∧
    hukm witQamar .fil .kalam .hajar = .laHukm .mumtaniBilaAlaqa ∧
    hukm witQamar .masdar .fahm .insan = .haqiqa := by decide

end A116.Isnad
