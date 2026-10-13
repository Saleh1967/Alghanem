import Slge.MayaatirTable

/-!
# المعقوليّة: حكمٌ ثلاثيٌّ على الحجّة، وبطاقةُ مادّة الحوار، وطيُّ المرفوض (ADR ٤٩)

المراحلُ الثانية والثالثة والرابعة من خطّة المالك («نفّذ المراحل الأربعة»)، على معايير `MayaatirTable`
المختومة بأسطرها. الحجّةُ هنا **بنيةٌ لا نصّ**: الدعوى، ونوعُها (وجودُ الشيء أو حقيقتُه وصفتُه — U8)،
وشاهدُ الواقع (موضعٌ في المودَع المختوم، أو مادّةُ حوارٍ ببطاقة)، والواقعُ المعروض والمحكومُ عليه (U1)،
وموضوعُ البحث وموضوعاتُ المقدّمات (U6)، وسلسلةُ المعلومات السابقة بما تقوم عليه (U2، U4)، والخبرُ ونطاقُه (U5).

**الحكمُ ثلاثيّ** (دستورُ الوكيل، المادّة ١٣؛ لا ثنائيّ كما في الخطّة الواردة):

* `maqool d`: لا بابَ رفضٍ ينفتح والشاهدُ واقعٌ مختوم؛ ودرجتُه من U8 — **قطعيّة** إن كانت الدعوى عن وجود
  الشيء، و**ظنّيّة** إن كانت عن حقيقته أو صفته («تبقى فكراً صائباً حتى يتبين خطؤها»).
* `ghayr b`: بابُ رفضٍ مسمًّى من بنية الحجّة، مرسًى في معيارٍ من الجدول (`anchor`، `every_bab_anchored`).
* `laHukm r`: لا بابَ ينفتح ولا شاهدَ واقعٍ مختوم — «مجرّدُ معلومات» (U3) **لا رفض**: الغيابُ ليس امتناعًا.

المبرهَن:

* لا «معقول» بلا شاهدٍ مختوم (`maqool_has_sealed_witness`)، ولا تُرسي مادّةُ الحوار حكمًا (`card_never_anchors`).
* **الرفضُ لا يأتي من الغياب**: بابُ الرفض لا يتغيّر بتغيير الشاهد أيًّا كان (`ghayr_indep_shahid`)، فما لا شاهدَ له
  إمّا مرفوضٌ ببنيته أو «لا حكم» (`no_witness_not_maqool`).
* الدرجةُ من نوع الدعوى (`daraja_of_kind`)، والآفاتُ الثلاث لا تنفتح إلّا في الخبر (`u5_only_khabar`)،
  والدعوى مقدّمةً لنفسها دورٌ (`self_premise_dawar`)، والرأيُ في السلسلة بابُه (`ray_door`).
* **بطاقةُ الحوار**: لا مادّةَ بلا بطاقةٍ تامّة (مصدر، بصمةٌ من 64 حرفًا ستّ عشريًّا، نوعُ شهادة، حدُّ استعمال)
  (`no_card_no_entry`، `admit_needs_valid`)، والمقبولُ معلومةٌ سابقةٌ لا رأيٌ ولا مرساة (`admitted_is_sabiqa`).
* **الطيّ في «ز»**: كلُّ حجّةٍ في واحدٍ من ثلاثة — المعقول، والمؤجَّل، و«ز» ببابه — لا تضيع ولا تزيد
  (`archive_length`، `archive_mem`)، وكلُّ صفٍّ في «ز» يحمل بابَ رفضه بعينه (`zur_carries_door`).

ما ليس هنا: قراءةُ حجّةٍ من نصّ (البنيةُ مدخلُ المالك أو قارئٍ لم يُكتب)؛ وبابُ «مصادرة المطلوب» كما عرّفته الخطّة
(«قفزٌ من درجة k إلى k+1») ليس بابًا نبهانيًّا — والدعوى مقدّمةً لنفسها هي الدورُ (U4).
-/

namespace Slge.Maqool

/-- نوعُ الدعوى (U8): وجودُ الشيء، أو الحكمُ على حقيقته أو صفته. -/
inductive Kind where
  | wujud
  | haqiqa
  deriving DecidableEq, Repr

/-- درجةُ المعقول (U8). -/
inductive Daraja where
  | qati
  | zanni
  deriving DecidableEq, Repr

/-- الشاهد: موضعٌ في المودَع المختوم، أو مادّةُ حوارٍ ببطاقة (معلومةٌ سابقة، لا مرساة). -/
inductive Shahid where
  | makhtum (id : Nat)
  | bitaqa (id : Nat)
  deriving DecidableEq, Repr

/-- معلومةٌ سابقةٌ في السلسلة: رقمُها، أهي رأيٌ سابقٌ لا معلومة (U2)، وما تقوم عليه. -/
structure Sabiqa where
  id : Nat
  ray : Bool
  deps : List Nat
  deriving DecidableEq, Repr

/-- الحجّةُ بنيةً. -/
structure Hujja where
  claim : Nat
  kind : Kind
  shahid : Option Shahid
  presented : Nat
  judgedOn : Nat
  mawdu : Nat
  premTopics : List Nat
  sabiqa : List Sabiqa
  khabar : Bool
  withCircumstances : Bool
  covered : List Nat
  witnessed : List Nat
  shumuli : Bool
  deriving DecidableEq, Repr

/-- أبوابُ الرفض. -/
inductive Bab where
  | dawar
  | rayMutanakkir
  | tahrifWaqi
  | khurujMawdu
  | tajrid
  | taamim
  | qiyasShumuli
  | khata
  deriving DecidableEq, Repr

/-- أسبابُ «لا حكم». -/
inductive Sabab where
  | bilaShahid
  | shahidBitaqa
  deriving DecidableEq, Repr

/-- الحكمُ الثلاثيّ. -/
inductive Hukm where
  | maqool (d : Daraja)
  | ghayr (b : Bab)
  | laHukm (r : Sabab)
  deriving DecidableEq, Repr

/-- مرساةُ كلّ باب: مفتاحُ معياره في الجدول المختوم. -/
def anchor : Bab → String
  | .dawar => "U4"
  | .rayMutanakkir => "U2"
  | .tahrifWaqi => "U1"
  | .khurujMawdu => "U6"
  | .tajrid => "U5"
  | .taamim => "U5"
  | .qiyasShumuli => "U5"
  | .khata => "U8"

def Sabab.anchor : Sabab → String
  | .bilaShahid => "U3"
  | .shahidBitaqa => "U3"

def allBab : List Bab :=
  [.dawar, .rayMutanakkir, .tahrifWaqi, .khurujMawdu, .tajrid, .taamim, .qiyasShumuli, .khata]

theorem every_bab_anchored : ∀ b ∈ allBab, anchor b ∈ MayaatirTable.keys := by decide

theorem every_sabab_anchored :
    ∀ r ∈ [Sabab.bilaShahid, .shahidBitaqa], r.anchor ∈ MayaatirTable.keys := by decide

/-! ## الدور (U4): الدعوى وسلسلتُها رسمٌ، والدورُ حلقةٌ فيه. -/

/-- الجيران: الدعوى `c` تقوم على كلّ معلوماتها السابقة `ss`، والمعلومةُ على ما تقوم عليه. -/
def succ (c : Nat) (ss : List Sabiqa) (v : Nat) : List Nat :=
  (if v == c then ss.map (·.id) else []) ++ (ss.filter (·.id == v)).flatMap (·.deps)

/-- ما يُبلَغ في خطوةٍ فأكثر، بوقودٍ يكفي عددَ العُقد. -/
def reach (c : Nat) (ss : List Sabiqa) : Nat → List Nat → List Nat
  | 0, xs => xs
  | n + 1, xs => reach c ss n (xs ++ xs.flatMap (succ c ss))

def nodes (c : Nat) (ss : List Sabiqa) : List Nat := c :: ss.map (·.id)

/-- الدور: عقدةٌ تبلغ نفسَها. -/
def cyc (c : Nat) (ss : List Sabiqa) : Bool :=
  (nodes c ss).any fun v => (reach c ss (nodes c ss).length (succ c ss v)).contains v

def cyclic (h : Hujja) : Bool := cyc h.claim h.sabiqa

theorem reach_mono (c : Nat) (ss : List Sabiqa) :
    ∀ (n : Nat) (xs : List Nat) (v : Nat), v ∈ xs → v ∈ reach c ss n xs
  | 0, _, _, hv => hv
  | n + 1, _, v, hv => reach_mono c ss n _ v (List.mem_append_left _ hv)

theorem reach_step (c : Nat) (ss : List Sabiqa) :
    ∀ (n : Nat) (xs : List Nat) (u v : Nat), u ∈ xs → v ∈ succ c ss u → 0 < n → v ∈ reach c ss n xs
  | 0, _, _, _, _, _, h0 => absurd h0 (Nat.lt_irrefl 0)
  | n + 1, _, u, v, hu, hv, _ =>
    reach_mono c ss n _ v (List.mem_append_right _ (List.mem_flatMap.2 ⟨u, hu, hv⟩))

/-- **الدعوى مقدّمةً لنفسها دور**: إن قامت معلومةٌ في السلسلة على الدعوى نفسِها. -/
theorem self_premise_dawar (h : Hujja) (s : Sabiqa) (hs : s ∈ h.sabiqa) (hc : h.claim ∈ s.deps) :
    cyclic h = true := by
  unfold cyclic cyc
  rw [List.any_eq_true]
  refine ⟨h.claim, List.mem_cons_self .., ?_⟩
  have h1 : s.id ∈ succ h.claim h.sabiqa h.claim := by
    unfold succ; simp only [beq_self_eq_true, ↓reduceIte]
    exact List.mem_append_left _ (List.mem_map.2 ⟨s, hs, rfl⟩)
  have h2 : h.claim ∈ succ h.claim h.sabiqa s.id :=
    List.mem_append_right _ (List.mem_flatMap.2 ⟨s, List.mem_filter.2 ⟨hs, by simp⟩, hc⟩)
  have : 0 < (nodes h.claim h.sabiqa).length := by simp [nodes]
  exact List.contains_iff_mem.2 (reach_step _ _ _ _ s.id h.claim h1 h2 this)

/-! ## الأبواب بترتيبها، ثمّ الشاهد. -/

/-- أوّلُ بابٍ ينفتح من بنية الحجّة وحدَها — لا يقرأ الشاهد. -/
def door (h : Hujja) : Option Bab :=
  if cyclic h then some .dawar
  else if h.sabiqa.any (·.ray) then some .rayMutanakkir
  else if h.presented != h.judgedOn then some .tahrifWaqi
  else if h.premTopics.any (· != h.mawdu) then some .khurujMawdu
  else if h.khabar && !h.withCircumstances then some .tajrid
  else if h.khabar && h.covered.any (fun e => !h.witnessed.contains e) then some .taamim
  else if h.khabar && h.shumuli then some .qiyasShumuli
  else none

def darajaOf : Kind → Daraja
  | .wujud => .qati
  | .haqiqa => .zanni

/-- ما بعد الأبواب: الشاهدُ يقرّر المعقولَ أو «لا حكم». -/
def tailHukm (k : Kind) : Option Shahid → Hukm
  | some (.makhtum _) => .maqool (darajaOf k)
  | some (.bitaqa _) => .laHukm .shahidBitaqa
  | none => .laHukm .bilaShahid

/-- الحكمُ الثلاثيّ: البابُ أوّلًا، ثمّ الشاهد. -/
def judge (h : Hujja) : Hukm :=
  match door h with
  | some b => .ghayr b
  | none => tailHukm h.kind h.shahid

theorem tail_not_ghayr (k : Kind) (s : Option Shahid) (b : Bab) : tailHukm k s ≠ .ghayr b := by
  cases s with
  | none => simp [tailHukm]
  | some x => cases x <;> simp [tailHukm]

theorem door_indep_shahid (h : Hujja) (s : Option Shahid) : door { h with shahid := s } = door h := by
  rfl

theorem judge_ghayr_iff (h : Hujja) (b : Bab) : judge h = .ghayr b ↔ door h = some b := by
  unfold judge
  cases hd : door h with
  | some c => simp
  | none => simp [tail_not_ghayr]

/-- **الرفضُ لا يأتي من الغياب**: بابُ الرفض واحدٌ أيًّا كان الشاهد. -/
theorem ghayr_indep_shahid (h : Hujja) (s : Option Shahid) (b : Bab) :
    judge { h with shahid := s } = .ghayr b ↔ judge h = .ghayr b := by
  rw [judge_ghayr_iff, judge_ghayr_iff, door_indep_shahid]

theorem tail_maqool (k : Kind) (s : Option Shahid) (d : Daraja) (ht : tailHukm k s = .maqool d) :
    (∃ i, s = some (.makhtum i)) ∧ d = darajaOf k := by
  cases s with
  | none => simp [tailHukm] at ht
  | some x => cases x with
    | makhtum i => simp [tailHukm] at ht; exact ⟨⟨i, rfl⟩, ht.symm⟩
    | bitaqa _ => simp [tailHukm] at ht

theorem judge_maqool (h : Hujja) (d : Daraja) (hj : judge h = .maqool d) :
    door h = none ∧ (∃ i, h.shahid = some (.makhtum i)) ∧ d = darajaOf h.kind := by
  unfold judge at hj
  cases hd : door h with
  | some b => rw [hd] at hj; simp at hj
  | none => rw [hd] at hj; exact ⟨rfl, tail_maqool _ _ _ hj⟩

/-- لا «معقول» بلا شاهدٍ مختوم. -/
theorem maqool_has_sealed_witness (h : Hujja) (d : Daraja) (hj : judge h = .maqool d) :
    ∃ i, h.shahid = some (.makhtum i) := (judge_maqool h d hj).2.1

theorem no_witness_not_maqool (h : Hujja) (hn : h.shahid = none) (d : Daraja) : judge h ≠ .maqool d := by
  intro hj; obtain ⟨i, hi⟩ := maqool_has_sealed_witness h d hj; simp [hn] at hi

/-- مادّةُ الحوار لا تُرسي حكمًا. -/
theorem card_never_anchors (h : Hujja) (n : Nat) (hc : h.shahid = some (.bitaqa n)) (d : Daraja) :
    judge h ≠ .maqool d := by
  intro hj; obtain ⟨i, hi⟩ := maqool_has_sealed_witness h d hj; simp [hc] at hi

/-- الدرجةُ من نوع الدعوى (U8). -/
theorem daraja_of_kind (h : Hujja) (d : Daraja) (hj : judge h = .maqool d) :
    (d = .qati ↔ h.kind = .wujud) := by
  rw [(judge_maqool h d hj).2.2]
  cases h.kind <;> simp [darajaOf]

/-- الآفاتُ الثلاث في الخبر وحدَه (U5: «آفة فهم الوقائع والحوادث، أي آفة معرفة الأخبار»). -/
theorem u5_only_khabar (h : Hujja) (hk : h.khabar = false) :
    door h ≠ some .tajrid ∧ door h ≠ some .taamim ∧ door h ≠ some .qiyasShumuli := by
  unfold door
  simp only [hk, Bool.false_and, Bool.false_eq_true, ite_false]
  refine ⟨?_, ?_, ?_⟩ <;> (repeat' split) <;> simp

/-- الرأيُ السابقُ في السلسلة بابُه، ما لم يكن دور. -/
theorem ray_door (h : Hujja) (hc : cyclic h = false) (s : Sabiqa) (hs : s ∈ h.sabiqa) (hr : s.ray = true) :
    judge h = .ghayr .rayMutanakkir := by
  have : h.sabiqa.any (·.ray) = true := List.any_eq_true.2 ⟨s, hs, hr⟩
  simp [judge, door, hc, this]

theorem dawar_door (h : Hujja) (hc : cyclic h = true) : judge h = .ghayr .dawar := by
  simp [judge, door, hc]

/-- ثلاثيٌّ تامّ: لكلّ حجّةٍ واحدٌ من الثلاثة. -/
theorem ternary (h : Hujja) :
    (∃ d, judge h = .maqool d) ∨ (∃ b, judge h = .ghayr b) ∨ (∃ r, judge h = .laHukm r) := by
  cases hj : judge h with
  | maqool d => exact Or.inl ⟨d, rfl⟩
  | ghayr b => exact Or.inr (Or.inl ⟨b, rfl⟩)
  | laHukm r => exact Or.inr (Or.inr ⟨r, rfl⟩)

/-! ## بطاقةُ مادّة الحوار (المرحلة الثالثة). -/

/-- نوعُ شهادة المادّة (نظريّة الشهادة §5 في الخطّة): انتقاءٌ أو قرينةٌ معجميّة. -/
inductive Naw where
  | intiqa
  | qarina
  deriving DecidableEq, Repr

structure Bitaqa where
  masdar : String
  sha256 : String
  naw : Naw
  hadd : String
  deriving DecidableEq, Repr

def hexDigit (c : Char) : Bool := ('0' ≤ c && c ≤ '9') || ('a' ≤ c && c ≤ 'f')

/-- بطاقةٌ تامّة: مصدرٌ غيرُ فارغ، وبصمةٌ من 64 حرفًا ستّ عشريًّا صغيرًا، وحدُّ استعمالٍ غيرُ فارغ. -/
def Bitaqa.valid (c : Bitaqa) : Bool :=
  !c.masdar.isEmpty && c.sha256.length == 64 && c.sha256.toList.all hexDigit && !c.hadd.isEmpty

/-- قبولُ المادّة: لا مادّةَ بلا بطاقةٍ تامّة؛ والمقبولُ معلومةٌ سابقةٌ بلا سوالف — لا رأيٌ ولا مرساة. -/
def admit (c : Option Bitaqa) (id : Nat) : Option Sabiqa :=
  match c with
  | some b => if b.valid then some ⟨id, false, []⟩ else none
  | none => none

theorem no_card_no_entry (id : Nat) : admit none id = none := rfl

theorem admit_needs_valid (c : Bitaqa) (id : Nat) (s : Sabiqa) (h : admit (some c) id = some s) :
    c.valid = true := by
  unfold admit at h; split at h <;> simp_all

theorem admitted_is_sabiqa (c : Option Bitaqa) (id : Nat) (s : Sabiqa) (h : admit c id = some s) :
    s.id = id ∧ s.ray = false ∧ s.deps = [] := by
  unfold admit at h; split at h
  · split at h <;> simp_all; subst h; simp
  · simp at h

/-! ## الطيّ في «ز» (المرحلة الرابعة): المرفوضُ بقيّةٌ مفسَّرة لا عدم. -/

structure Archive where
  maqool : List Hujja
  muajjal : List Hujja
  zur : List (Hujja × Bab)

def isMaqool (h : Hujja) : Bool := match judge h with | .maqool _ => true | _ => false
def isLaHukm (h : Hujja) : Bool := match judge h with | .laHukm _ => true | _ => false

def zurOf (hs : List Hujja) : List (Hujja × Bab) :=
  hs.filterMap fun h => match judge h with | .ghayr b => some (h, b) | _ => none

def archive (hs : List Hujja) : Archive :=
  ⟨hs.filter isMaqool, hs.filter isLaHukm, zurOf hs⟩

theorem zur_carries_door (hs : List Hujja) (p : Hujja × Bab) (hp : p ∈ (archive hs).zur) :
    p.1 ∈ hs ∧ judge p.1 = .ghayr p.2 := by
  simp only [archive, zurOf, List.mem_filterMap] at hp
  obtain ⟨h, hh, he⟩ := hp
  revert he; cases hj : judge h <;> simp
  intro e; subst e; exact ⟨hh, hj⟩

theorem zur_length (hs : List Hujja) :
    (zurOf hs).length = hs.countP fun h => match judge h with | .ghayr _ => true | _ => false := by
  induction hs with
  | nil => rfl
  | cons h t ih =>
    simp only [zurOf, List.filterMap_cons, List.countP_cons] at ih ⊢
    cases judge h <;> simp [ih]

/-- **لا تضيع حجّةٌ ولا تزيد**: أعدادُ الثلاثة مجموعُها عددُ الحجج. -/
theorem archive_length (hs : List Hujja) :
    (archive hs).maqool.length + (archive hs).muajjal.length + (archive hs).zur.length = hs.length := by
  simp only [archive, ← List.countP_eq_length_filter, zur_length]
  induction hs with
  | nil => rfl
  | cons h t ih =>
    simp only [List.countP_cons, List.length_cons]
    cases hj : judge h <;> simp [isMaqool, isLaHukm, hj] <;> omega

/-- **وكلُّ حجّةٍ في واحدٍ منها**: الردُّ من الثلاثة. -/
theorem archive_mem (hs : List Hujja) (h : Hujja) :
    h ∈ hs ↔ h ∈ (archive hs).maqool ∨ h ∈ (archive hs).muajjal ∨ h ∈ (archive hs).zur.map (·.1) := by
  simp only [archive, zurOf, List.mem_filter, List.mem_map, List.mem_filterMap]
  constructor
  · intro hh
    cases hj : judge h with
    | maqool d => exact Or.inl ⟨hh, by simp [isMaqool, hj]⟩
    | laHukm r => exact Or.inr (Or.inl ⟨hh, by simp [isLaHukm, hj]⟩)
    | ghayr b => exact Or.inr (Or.inr ⟨(h, b), ⟨h, hh, by simp [hj]⟩, rfl⟩)
  · rintro (⟨hh, _⟩ | ⟨hh, _⟩ | ⟨p, ⟨x, hx, he⟩, rfl⟩)
    · exact hh
    · exact hh
    · revert he; cases judge x <;> simp
      intro e; subst e; exact hx

/-! ## شواهدُ الحكم: حججٌ معلومةُ الحكم سلفًا (بوّابةُ المرحلة الثانية في الخطّة: عشرٌ فأكثر). -/

/-- حجّةٌ سليمة: دعوى عن وجود شيء، بشاهدٍ مختوم، على الواقع المعروض نفسِه، في موضوعها، بمعلومةٍ لا رأي. -/
def base : Hujja :=
  { claim := 1, kind := .wujud, shahid := some (.makhtum 32), presented := 7, judgedOn := 7, mawdu := 5,
    premTopics := [5], sabiqa := [⟨2, false, []⟩], khabar := false, withCircumstances := true,
    covered := [], witnessed := [], shumuli := false }

def cases : List (String × Hujja) := [
  ("c01_wujud_sound", base),
  ("c02_haqiqa_sound", { base with kind := .haqiqa }),
  ("c03_self_premise", { base with sabiqa := [⟨2, false, [1]⟩] }),
  ("c04_cycle_two", { base with sabiqa := [⟨2, false, [3]⟩, ⟨3, false, [2]⟩] }),
  ("c05_ray", { base with sabiqa := [⟨2, true, []⟩] }),
  ("c06_ad_hominem", { base with premTopics := [5, 9] }),
  ("c07_straw_man", { base with judgedOn := 8 }),
  ("c08_tajrid", { base with khabar := true, withCircumstances := false }),
  ("c09_taamim", { base with khabar := true, covered := [10, 11], witnessed := [10] }),
  ("c10_shumuli", { base with khabar := true, shumuli := true }),
  ("c11_u5_outside_khabar",
    { base with withCircumstances := false, covered := [10, 11], witnessed := [10], shumuli := true }),
  ("c12_no_witness", { base with shahid := none }),
  ("c13_card_witness", { base with shahid := some (.bitaqa 4) }),
  ("c14_cycle_no_witness", { base with shahid := none, sabiqa := [⟨2, false, [1]⟩] }),
  ("c15_khabar_sound", { base with khabar := true, covered := [10], witnessed := [10] }),
  ("c16_cycle_three", { base with sabiqa := [⟨2, false, [3]⟩, ⟨3, false, [4]⟩, ⟨4, false, [2]⟩] }),
  ("c17_chain_no_cycle", { base with sabiqa := [⟨2, false, [3]⟩, ⟨3, false, [4]⟩, ⟨4, false, []⟩] })
]

/-- أحكامُها كما تحسبها النواة. -/
theorem cases_verdicts : cases.map (judge ·.2) = [
    .maqool .qati, .maqool .zanni, .ghayr .dawar, .ghayr .dawar, .ghayr .rayMutanakkir,
    .ghayr .khurujMawdu, .ghayr .tahrifWaqi, .ghayr .tajrid, .ghayr .taamim, .ghayr .qiyasShumuli,
    .maqool .qati, .laHukm .bilaShahid, .laHukm .shahidBitaqa, .ghayr .dawar, .maqool .qati,
    .ghayr .dawar, .maqool .qati] := by decide

/-- وطيُّها: المعقولُ والمؤجَّلُ و«ز» تُعدّ ولا تُفترض، ومجموعُها عددُ الحجج. -/
theorem cases_archive :
    ((archive (cases.map (·.2))).maqool.length, (archive (cases.map (·.2))).muajjal.length,
      (archive (cases.map (·.2))).zur.length) = (5, 2, 10) := by decide

def tag : Hukm → String
  | .maqool .qati => "maqool,qati"
  | .maqool .zanni => "maqool,zanni"
  | .ghayr b => "ghayr," ++ (match b with
      | .dawar => "dawar" | .rayMutanakkir => "ray_mutanakkir" | .tahrifWaqi => "tahrif_waqi"
      | .khurujMawdu => "khuruj_mawdu" | .tajrid => "tajrid" | .taamim => "taamim"
      | .qiyasShumuli => "qiyas_shumuli" | .khata => "khata")
  | .laHukm .bilaShahid => "la_hukm,bila_shahid"
  | .laHukm .shahidBitaqa => "la_hukm,shahid_bitaqa"

/-- صفوفُ الجدول المصدَّر: (الاسم، الحكم، القيمة، المرساة). -/
def rows : List String :=
  cases.map fun (n, h) =>
    let j := judge h
    n ++ "," ++ tag j ++ "," ++
      (match j with | .maqool _ => "U8" | .ghayr b => anchor b | .laHukm r => r.anchor)

/-! ## الجولات (دَينُ D-RATING في الخطّة، على U8): «تبقى فكراً صائباً حتى يتبين خطؤها».

الحكمُ لا يُرفع إلّا بشاهدٍ مختومٍ جديد، ولا يُخفض إلّا بخطأٍ تبيّن؛ والدرجةُ من نوع الدعوى لا من عدد الجولات —
فالظنّيُّ لا يصير قطعيًّا بكثرة الشواهد (`zanni_never_qati`)، و«لا حكم» لا يصير معقولًا بلا شاهد (`rise_needs_witness`)،
والمعقولُ لا يسقط بلا خطأٍ تبيّن (`fall_needs_khata`)، وما تبيّن خطؤه لا يعود (`khata_sticks`). -/

/-- جولة: شاهدٌ مختومٌ جديد إن وُجد، وهل تبيّن فيها الخطأ. -/
structure Jawla where
  shahid : Option Nat
  khata : Bool
  deriving DecidableEq, Repr

/-- الحالُ عبر الجولات: الحجّةُ وهل تبيّن خطؤها. -/
structure HalJ where
  hujja : Hujja
  khata : Bool
  deriving DecidableEq, Repr

def stepJ (s : HalJ) (j : Jawla) : HalJ :=
  ⟨match j.shahid with
    | some i => { s.hujja with shahid := some (.makhtum i) }
    | none => s.hujja, s.khata || j.khata⟩

def runJ (s : HalJ) (js : List Jawla) : HalJ := js.foldl stepJ s

/-- الحكمُ على الحال: ما تبيّن خطؤه بابُه `khata` (U8)، وإلّا حكمُ الحجّة. -/
def judgeJ (s : HalJ) : Hukm := if s.khata then .ghayr .khata else judge s.hujja

theorem stepJ_kind (s : HalJ) (j : Jawla) : (stepJ s j).hujja.kind = s.hujja.kind := by
  unfold stepJ; cases j.shahid <;> rfl

theorem stepJ_door (s : HalJ) (j : Jawla) : door (stepJ s j).hujja = door s.hujja := by
  unfold stepJ; cases j.shahid with
  | none => rfl
  | some i => exact door_indep_shahid s.hujja _

theorem runJ_kind : ∀ (s : HalJ) (js : List Jawla), (runJ s js).hujja.kind = s.hujja.kind
  | _, [] => rfl
  | s, j :: js => (runJ_kind (stepJ s j) js).trans (stepJ_kind s j)

theorem runJ_door : ∀ (s : HalJ) (js : List Jawla), door (runJ s js).hujja = door s.hujja
  | _, [] => rfl
  | s, j :: js => (runJ_door (stepJ s j) js).trans (stepJ_door s j)

/-- ما تبيّن خطؤه لا يعود. -/
theorem khata_sticks : ∀ (s : HalJ) (js : List Jawla), s.khata = true → (runJ s js).khata = true
  | _, [], h => h
  | s, j :: js, h => khata_sticks (stepJ s j) js (by simp [stepJ, h])

theorem judgeJ_maqool (s : HalJ) (d : Daraja) (h : judgeJ s = .maqool d) :
    s.khata = false ∧ judge s.hujja = .maqool d := by
  unfold judgeJ at h; cases hk : s.khata <;> simp_all

/-- **الظنّيُّ لا يصير قطعيًّا بالجولات**: الدرجةُ من نوع الدعوى، والنوعُ ثابت. -/
theorem zanni_never_qati (s : HalJ) (js : List Jawla) (h : judgeJ s = .maqool .zanni) :
    judgeJ (runJ s js) ≠ .maqool .qati := by
  intro h'
  have h1 := (judge_maqool _ _ (judgeJ_maqool s _ h).2).2.2
  have h2 := (judge_maqool _ _ (judgeJ_maqool _ _ h').2).2.2
  rw [runJ_kind] at h2
  rw [← h2] at h1
  exact Daraja.noConfusion h1

theorem runJ_no_witness : ∀ (s : HalJ) (js : List Jawla), (∀ j ∈ js, j.shahid = none) →
    (runJ s js).hujja = s.hujja
  | _, [], _ => rfl
  | s, j :: js, h => by
    have hj : j.shahid = none := h j (List.mem_cons_self ..)
    have : (stepJ s j).hujja = s.hujja := by simp [stepJ, hj]
    rw [← this]; exact runJ_no_witness _ js (fun x hx => h x (List.mem_cons_of_mem _ hx))

/-- **«لا حكم» لا يصير معقولًا بلا شاهدٍ جديد.** -/
theorem rise_needs_witness (s : HalJ) (js : List Jawla) (r : Sabab) (d : Daraja)
    (h : judge s.hujja = .laHukm r) (hn : ∀ j ∈ js, j.shahid = none) : judgeJ (runJ s js) ≠ .maqool d := by
  intro h'
  have := (judgeJ_maqool _ _ h').2
  rw [runJ_no_witness s js hn, h] at this
  exact Hukm.noConfusion this

theorem runJ_sealed : ∀ (s : HalJ) (js : List Jawla), (∃ i, s.hujja.shahid = some (.makhtum i)) →
    ∃ i, (runJ s js).hujja.shahid = some (.makhtum i)
  | _, [], h => h
  | s, j :: js, h => by
    apply runJ_sealed (stepJ s j) js
    unfold stepJ; cases j.shahid with
    | none => exact h
    | some i => exact ⟨i, rfl⟩

theorem runJ_khata_false : ∀ (s : HalJ) (js : List Jawla), s.khata = false → (∀ j ∈ js, j.khata = false) →
    (runJ s js).khata = false
  | _, [], h, _ => h
  | s, j :: js, h, hj => by
    apply runJ_khata_false (stepJ s j) js _ (fun x hx => hj x (List.mem_cons_of_mem _ hx))
    simp [stepJ, h, hj j (List.mem_cons_self ..)]

/-- **المعقولُ لا يسقط بلا خطأٍ تبيّن**: ولا يتغيّر درجةً. -/
theorem fall_needs_khata (s : HalJ) (js : List Jawla) (d : Daraja) (h : judgeJ s = .maqool d)
    (hn : ∀ j ∈ js, j.khata = false) : judgeJ (runJ s js) = .maqool d := by
  obtain ⟨hk, hj⟩ := judgeJ_maqool s d h
  obtain ⟨hd, hs, hdk⟩ := judge_maqool _ _ hj
  obtain ⟨i, hi⟩ := runJ_sealed s js hs
  unfold judgeJ judge
  rw [runJ_khata_false s js hk hn, runJ_door, hd]
  simp only [Bool.false_eq_true, ↓reduceIte, hi, tailHukm, runJ_kind, hdk]

/-- شواهدُ الجولات: (الحالُ الأولى، الجولات) معلومةُ الحكم سلفًا. -/
def jawlatCases : List (String × HalJ × List Jawla) := [
  ("j1_zanni_many_witnesses", ⟨{ base with kind := .haqiqa }, false⟩, [⟨some 38, false⟩, ⟨some 241, false⟩]),
  ("j2_lahukm_then_witness", ⟨{ base with shahid := none }, false⟩, [⟨some 32, false⟩]),
  ("j3_lahukm_no_witness", ⟨{ base with shahid := none }, false⟩, [⟨none, false⟩, ⟨none, false⟩]),
  ("j4_maqool_then_khata", ⟨base, false⟩, [⟨none, true⟩]),
  ("j5_khata_then_witness", ⟨base, false⟩, [⟨none, true⟩, ⟨some 71, false⟩]),
  ("j6_door_survives_witness", ⟨{ base with sabiqa := [⟨2, true, []⟩] }, false⟩, [⟨some 37, false⟩])
]

theorem jawlat_verdicts : jawlatCases.map (fun c => judgeJ (runJ c.2.1 c.2.2)) = [
    .maqool .zanni, .maqool .qati, .laHukm .bilaShahid, .ghayr .khata, .ghayr .khata,
    .ghayr .rayMutanakkir] := by decide

end Slge.Maqool
