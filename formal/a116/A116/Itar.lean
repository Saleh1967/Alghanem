import A116.Tarkib
import A116.AjnasMukhassas
import A116.ExhaustPause
import A116.Imla

/-!
# الأطرُ الثلاثة على القانون العامّ: الدالّ، والمدلول، والدالُّ والمدلولُ معًا (ADR ١٠٤)

أمرُ المالك (2026-10-18): «ممكن تنسخ فكرته الى الغانم ولا تعمل في mashru ابدا ممكن تنسخ من طريقته وتكتب مثلها من
جديد بناء جديد». الفكرةُ من تصميم «Itar3» في مستودعٍ آخر قُرئ ولم يُمسّ. والبناءُ هنا جديدٌ على وحدات الغانم وحدها.

## ما يُبنى

١. **إطارُ الدالّ** (`dal`): السطرُ كلماتٌ بخاناتها، وحكمُه في المواضع الثلاثة بقيد الحدّ نفسِه:
   * الابتداءُ: لا ابتداءَ بساكن (`Boundary.initialSukun`).
   * الوصلُ: `NizamLine.strictLineB`.
   * الوقفُ: `NizamLine.strictLinePauseB`.
   والوصلُ يستلزم الوقف، والوقفُ يستلزم الابتداء (`dal_silsila`)، كما في الكلمة (`ExhaustPause.awa_chain`).
٢. **إطارُ المدلول** (`madlul`): المسندُ إليه جنسٌ، والمسندُ ربطُ صيغته واستعمالُه. والحكمُ ثلاثيٌّ بعينه:
   `HukmMuwahhad.hukm` (حقيقة، مجاز، لا حكم) على شجرةٍ وقابليّةٍ موروثة.
٣. **الإطارُ الجامع** (`hukm3`): التركيبُ بأقسامه ومدلولُه. ونتيجتُه ترخيصٌ وحكم:
   * الترخيصُ من الدالّ وحدَه في موضعه، ولا يغيّره المدلول (`tarkhis_dal_wahdahu`).
   * الحكمُ لا يقوم إلّا على مرخَّص (`hukm_yastalzim_tarkhis`).
   * وما لا إسنادَ فيه خارجَ حدّ الطبقة: «لا حكم» (`kharij_hadd`). مثالُه «فِي الدَّارِ»: مرخَّصٌ دالًّا ولا قضيّة.
   * وما فيه إسنادٌ حكمُه حكمُ المدلول بعينه (`hukm_madlul`)، و«لا حكم» فيه لا يُسقط الترخيص.
٤. **الإسنادُ محسوبًا** (`isnadB`): دالّةٌ تقرّر `Tarkib.Isnad` (`isnadB_iff`).

## ما ليس هنا

* جنسُ المسند إليه وصيغةُ المسند معاملان مُعطَيان (`ITAR_MADLUL_FIELDS_ARE_INPUT`). فلا دالّةَ هنا تقرأ الجنسَ من خانات
  الكلمة.
* والإسنادُ متجاورٌ وحدَه. فـ«الْوَلَدُ ذَهَبَ» (فاعلُها مستتر) خارجَ الحدّ هنا (`MUSTATIR_NOT_SEGMENTED`).
* والإطارُ ليس مدخلًا في `gate.enter` (`ITAR_NOT_IN_GATE`).
-/

namespace A116.Itar

open A116 A116.Tarkib A116.NizamLine
open A116.ExhaustPause (AWA)
open A116.Majaz (Istimal)

/-! ## ١. إطارُ الدالّ -/

/-- حكمُ الدالّ على السطر في موضعه. -/
def dal : AWA → List (List Cell) → Bool
  | .ibtida, ws => !Boundary.initialSukun ws.flatten
  | .wasl, ws => strictLineB ws
  | .waqf, ws => strictLinePauseB ws

/-- **السلسلةُ في السطر**: الوصلُ يستلزم الوقف، والوقفُ يستلزم الابتداء. -/
theorem dal_silsila {ws : List (List Cell)} (h : dal .wasl ws = true) :
    dal .waqf ws = true ∧ dal .ibtida ws = true := by
  simp only [dal, strictLineB, strictLinePauseB, Bool.and_eq_true] at h ⊢
  have hp : Hadd.strictPauseB ws.flatten = true := Hadd.strictB_pause h.1
  refine ⟨⟨hp, h.2⟩, ?_⟩
  have := ExhaustPause.awa_waqf_ibtida (w := ws.flatten) (by simpa [ExhaustPause.awa] using hp)
  simpa [ExhaustPause.awa] using this

/-- **سطرٌ من كلمةٍ واحدة** حكمُه وصلًا حكمُ الكلمة بقيد الحدّ. -/
theorem dal_kalima (w : List Cell) : dal .wasl [w] = strictLineB [w] := rfl

/-! ## ٢. الإسنادُ محسوبًا -/

/-- الإسنادُ بين متجاورين قرارًا. -/
def isnadPair (a b : Kalima) : Bool :=
  (a.qism == .ism && b.qism == .ism) || (a.qism == .fil && b.qism == .ism)

/-- في التركيب إسنادٌ بين متجاورين. -/
def isnadB : Tarkib → Bool
  | a :: b :: rest => isnadPair a b || isnadB (b :: rest)
  | _ => false

theorem isnadPair_iff (a b : Kalima) : isnadPair a b = true ↔ ismiyya a b ∨ filiyya a b := by
  cases ha : a.qism <;> cases hb : b.qism <;> simp [isnadPair, ismiyya, filiyya, ha, hb]

/-- **الإسنادُ المحسوب هو الإسنادُ بعينه** (`Tarkib.Isnad`). -/
theorem isnadB_iff : ∀ t : Tarkib, isnadB t = true ↔ Isnad t
  | [] => by simp [isnadB]; intro h; cases h
  | [w] => by
    simp [isnadB]; intro h
    cases h with
    | there _ _ h' => cases h'
  | a :: b :: rest => by
    simp only [isnadB, Bool.or_eq_true, isnadPair_iff, isnadB_iff (b :: rest)]
    constructor
    · rintro (h | h)
      · exact Isnad.here a b rest h
      · exact Isnad.there a _ h
    · intro h
      cases h with
      | here _ _ _ h => exact Or.inl h
      | there _ _ h => exact Or.inr h

/-! ## ٣. إطارُ المدلول -/

/-- مدلولُ الجملة: جنسُ المسند إليه، وربطُ صيغة المسند، واستعمالُه. -/
structure Madlul where
  jins : String
  sigha : Majaz.Hukm
  istimal : Istimal

/-- حكمُ المدلول: الحكمُ الموحَّد على شجرةٍ وقابليّةٍ موروثة. -/
def madlul (abb : HukmMuwahhad.Shajara) (n : Nat) (q : String → Option Bool) (m : Madlul) : Majaz.Hukm :=
  HukmMuwahhad.hukm abb n q m.sigha m.istimal m.jins

/-! ## ٤. الإطارُ الجامع -/

/-- الجملة: تركيبٌ بأقسامه ومدلولُه. -/
structure Jumla where
  tarkib : Tarkib
  madlul : Madlul

/-- النتيجة: ترخيصُ الدالّ في موضعه، وحكمُ المدلول إن قام. -/
structure Natija where
  tarkhis : Bool
  hukm : Option Majaz.Hukm
  deriving DecidableEq, Repr

/-- حدُّ الطبقة: في التركيب إسناد. -/
def fiHadd (j : Jumla) : Bool := isnadB j.tarkib

/-- الحكمُ الجامع: الدالُّ يرخّص، ثمّ حدُّ الطبقة، ثمّ المدلول. -/
def hukm3 (abb : HukmMuwahhad.Shajara) (n : Nat) (q : String → Option Bool) (p : AWA) (j : Jumla) : Natija :=
  let t := dal p (j.tarkib.map Kalima.cells)
  { tarkhis := t
    hukm := if !t then none else if fiHadd j then some (madlul abb n q j.madlul) else some .laHukm }

/-- **الترخيصُ من الدالّ وحدَه**: لا يغيّره المدلولُ ولا الشجرةُ ولا القابليّة. -/
theorem tarkhis_dal_wahdahu (abb abb' : HukmMuwahhad.Shajara) (n n' : Nat) (q q' : String → Option Bool)
    (p : AWA) (j : Jumla) (m : Madlul) :
    (hukm3 abb n q p j).tarkhis = (hukm3 abb' n' q' p ⟨j.tarkib, m⟩).tarkhis := rfl

/-- **لا حكمَ بلا ترخيص**. -/
theorem hukm_yastalzim_tarkhis (abb : HukmMuwahhad.Shajara) (n : Nat) (q : String → Option Bool) (p : AWA)
    (j : Jumla) (h : Majaz.Hukm) (hh : (hukm3 abb n q p j).hukm = some h) :
    (hukm3 abb n q p j).tarkhis = true := by
  simp only [hukm3] at hh ⊢
  cases ht : dal p (j.tarkib.map Kalima.cells) <;> simp_all

/-- **خارجَ حدّ الطبقة «لا حكم»**: مرخَّصٌ بلا إسنادٍ ليس قضيّة. -/
theorem kharij_hadd (abb : HukmMuwahhad.Shajara) (n : Nat) (q : String → Option Bool) (p : AWA) (j : Jumla)
    (ht : dal p (j.tarkib.map Kalima.cells) = true) (hf : fiHadd j = false) :
    hukm3 abb n q p j = ⟨true, some .laHukm⟩ := by
  simp [hukm3, ht, hf]

/-- **داخلَ الحدّ حكمُ المدلول بعينه**، والترخيصُ قائمٌ ولو كان الحكمُ «لا حكم». -/
theorem hukm_madlul (abb : HukmMuwahhad.Shajara) (n : Nat) (q : String → Option Bool) (p : AWA) (j : Jumla)
    (ht : dal p (j.tarkib.map Kalima.cells) = true) (hf : fiHadd j = true) :
    hukm3 abb n q p j = ⟨true, some (madlul abb n q j.madlul)⟩ := by
  simp [hukm3, ht, hf]

/-- **الوصلُ يرث إلى الوقف والابتداء** في الإطار الجامع: ما يُحكم عليه موصولًا يُحكم عليه بالحكم نفسِه موقوفًا ومبتدأً. -/
theorem hukm3_silsila (abb : HukmMuwahhad.Shajara) (n : Nat) (q : String → Option Bool) (j : Jumla)
    (h : (hukm3 abb n q .wasl j).tarkhis = true) :
    hukm3 abb n q .waqf j = hukm3 abb n q .wasl j ∧ hukm3 abb n q .ibtida j = hukm3 abb n q .wasl j := by
  simp only [hukm3] at h
  obtain ⟨h1, h2⟩ := dal_silsila h
  simp [hukm3, h, h1, h2]

/-- **القسمُ لا يمسّ الترخيص**، ويمسّ الحدَّ وحدَه: إعادةُ وسم الأقسام لا تغيّر ترخيصَ الدالّ. -/
theorem tarkhis_ama_an_qism (abb : HukmMuwahhad.Shajara) (n : Nat) (q : String → Option Bool) (p : AWA)
    (f : Qism → Qism) (j : Jumla) :
    (hukm3 abb n q p ⟨relabel f j.tarkib, j.madlul⟩).tarkhis = (hukm3 abb n q p j).tarkhis := by
  simp [hukm3, relabel, List.map_map, Function.comp_def]

/-! ## ٥. الشواهد

الكلماتُ صورٌ قانونيّة (كلُّ خانةٍ حرفٌ ثمّ علامته، `Imla.parse`). وفي الوصل تسقط همزةُ الوصل فـ«الْوَلَدُ» بعد كلمةٍ
«لْوَلَدُ». والجنسُ معاملٌ مُعطى من شجرة المخصَّص (`AjnasMukhassas`). -/

/-- الكلمةُ من صورتها القانونيّة. -/
def k (s : String) : List Cell := (Imla.parse (s.toList.map Char.toNat)).getD []

def nataqa : Kalima := ⟨k "نَطَقَ", .fil⟩
def nabaha : Kalima := ⟨k "نَبَحَ", .fil⟩
def walad : Kalima := ⟨k "لْوَلَدُ", .ism⟩
def kalb : Kalima := ⟨k "لْكَلْبُ", .ism⟩
def fi : Kalima := ⟨k "فِيْ", .harf⟩
def dar : Kalima := ⟨k "دَاْرِ", .ism⟩

/-- المدلول: «الإنسان» فاعلًا لفعلٍ معلوم، و«الكلب» مفعولًا (يُخاطَب)، والاستعمالُ بالتشبيه. -/
def mInsan : Madlul := ⟨"الإنسان", Khawass.sighaLink .filMaloom .faail, HukmMuwahhad.tashbih⟩
def mKalbKhitab : Madlul := ⟨"الكلب", Khawass.sighaLink .ismMafool .mafool, HukmMuwahhad.tashbih⟩
def mGhul : Madlul := ⟨"الغول", .haqiqa, HukmMuwahhad.tashbih⟩

def h3 := hukm3 AjnasMukhassas.abb 1 AjnasMukhassas.qKitab

/-- **الشواهد** (`decide`):
* الكلماتُ تُقرأ من صورها (لا فارغ).
* «نَطَقَ الْوَلَدُ» والجنسُ الإنسان: مرخَّصٌ وصلًا، وحقيقة.
* «نَبَحَ الْكَلْبُ» وقد جُعل الكلبُ مخاطَبًا: مرخَّص، ومجازٌ بالتشبيه.
* والجنسُ «الغول» لا صفَّ له: مرخَّص، و«لا حكم» — والترخيصُ لم يسقط.
* «فِي الدَّارِ»: مرخَّصٌ، وخارجَ الحدّ «لا حكم».
* «نْطَقَ» ابتداءً بساكن: مرفوضٌ دالًّا، ولا حكم يُطلب. -/
theorem shawahid :
    (k "نَطَقَ" ≠ [] ∧ k "لْوَلَدُ" ≠ [] ∧ k "فِيْ" ≠ [] ∧ k "دَاْرِ" ≠ []) ∧
    h3 .wasl ⟨[nataqa, walad], mInsan⟩ = ⟨true, some .haqiqa⟩ ∧
    h3 .wasl ⟨[nabaha, kalb], mKalbKhitab⟩ = ⟨true, some .majaz⟩ ∧
    h3 .wasl ⟨[nataqa, walad], mGhul⟩ = ⟨true, some .laHukm⟩ ∧
    h3 .wasl ⟨[fi, dar], mInsan⟩ = ⟨true, some .laHukm⟩ ∧
    h3 .ibtida ⟨[⟨k "نْطَقَ", .fil⟩, walad], mInsan⟩ = ⟨false, none⟩ := by
  decide +kernel

end A116.Itar
