/-
  FractalBridges.lean — القانون الواحد والجسور: ما يُبرهَن صوريًّا وما لا يُبرهَن
  Lean 4 core (v4.15.0)، بلا Mathlib، بلا sorry، بلا axiom.

  ١. القانون الواحد (ابتداء/وصل/وقف) في كل درجة، على أبجدية الدرجة التي تحتها.
  ٢. الجسر بلا فقد (طيّ/استرجاع) — وانغلاقه بالتركيب: هذا هو «الفراكتال» صوريًّا.
  ٣. حدّ الجسر: كل تصادم (لفظان ← صورة واحدة) يمنع الجسر بلا فقد.
  ٤. الجسر الدلالي: علاقة مرتَّبة لا تحذف مرشَّحًا (يرتّب ولا يحذف).
-/
namespace Ghanem.Fractal

/-! ## ١. القانون الواحد: ابتداء / وصل / وقف -/

/-- قانون درجة: ما يصحّ ابتداءً، وما يصحّ وصلُه بما قبله، وما يصحّ وقفًا. -/
structure Law (α : Type) where
  ibtida : α → Bool
  wasl   : α → α → Bool
  waqf   : α → Bool

/-- سلامة الوصل في سلسلة. -/
def links {α} (L : Law α) : List α → Bool
  | [] => true
  | [_] => true
  | a :: b :: r => L.wasl a b && links L (b :: r)

/-- السلسلة مرخَّصة بالقانون: غير فارغة، تبتدئ وتتصل وتقف على شرطه. -/
def Law.licenses {α} (L : Law α) : List α → Bool
  | [] => false
  | a :: r => L.ibtida a && links L (a :: r) && L.waqf ((a :: r).getLast (by simp))

/-- الترخيص قابل للحسم بالآلة في كل درجة (دالّة بوليانيّة). -/
theorem licenses_decidable {α} (L : Law α) (xs : List α) :
    L.licenses xs = true ∨ L.licenses xs = false := by
  cases L.licenses xs <;> simp

/-- شاهد صغير بأبجدية مجرّدة: ٠ = صامت، ١ = حركة.
    القانون: يُبتدأ بصامت، لا صامتان متتاليان في هذا المثال، ولا يُوقف إلا على حركة. -/
def cvLaw : Law Nat :=
  { ibtida := fun a => a == 0
    wasl   := fun a b => !(a == 0 && b == 0)
    waqf   := fun a => a == 1 }

theorem cv_ok   : cvLaw.licenses [0, 1, 0, 1] = true := by decide
theorem cv_bad1 : cvLaw.licenses [1, 0, 1] = false := by decide      -- ابتداء بحركة
theorem cv_bad2 : cvLaw.licenses [0, 0, 1] = false := by decide      -- وصل ممنوع
theorem cv_bad3 : cvLaw.licenses [0, 1, 0] = false := by decide      -- وقف ممنوع

/-! ## ٢. الجسر بلا فقد، وانغلاقه بالتركيب -/

/-- جسر بين درجتين: صعودٌ جزئيّ (ما لا يُرخَّص يُرفض باسمه = none)
    ونزولٌ تامّ، وقانونه: ما صعد ينزل إلى نفسه (لا ضائع). -/
structure Bridge (α β : Type) where
  up    : α → Option β
  down  : β → α
  sound : ∀ a b, up a = some b → down b = a

/-- تركيب جسرين. -/
def Bridge.comp {α β γ} (f : Bridge α β) (g : Bridge β γ) : Bridge α γ where
  up a := (f.up a).bind g.up
  down c := f.down (g.down c)
  sound a c h := by
    cases hf : f.up a with
    | none => simp [hf] at h
    | some b =>
      simp [hf] at h
      show f.down (g.down c) = a
      rw [g.sound b c h, f.sound a b hf]

/-- الفراكتال صوريًّا: تركيب أيّ عدد من الجسور جسرٌ من النوع نفسه.
    (يُعبَّر عنه بالانغلاق: comp يعطي Bridge، فالسلسلة كلها جسر واحد.) -/
theorem comp_down_up {α β γ} (f : Bridge α β) (g : Bridge β γ) (a : α) (c : γ)
    (h : (f.comp g).up a = some c) : (f.comp g).down c = a :=
  (f.comp g).sound a c h

/-- الجسر الهويّ: الدرجة إلى نفسها. -/
def Bridge.id (α) : Bridge α α := ⟨some, fun a => a, fun _ _ h => by cases h; rfl⟩

/-! ## ٣. حدّ الجسر بلا فقد: التصادم -/

/-- كل جسر بلا فقد متباين على ما يرخّصه: صورتان متساويتان ⇒ أصلان متساويان. -/
theorem up_injective {α β} (f : Bridge α β) {a₁ a₂ : α} {b : β}
    (h₁ : f.up a₁ = some b) (h₂ : f.up a₂ = some b) : a₁ = a₂ := by
  rw [← f.sound a₁ b h₁, ← f.sound a₂ b h₂]

/-- المانع: إذا أخذ «إسقاطٌ» لفظين مختلفين إلى صورة واحدة، فلا جسر بلا فقد
    يكون صعودُه ذلك الإسقاط. (مثاله: حذف الحركات، أو اللفظ ← معنى واحد مع الاشتراك.) -/
theorem no_lossless_of_collision {α β} (p : α → β) {a₁ a₂ : α}
    (hne : a₁ ≠ a₂) (hcol : p a₁ = p a₂) :
    ¬ ∃ f : Bridge α β, ∀ a, f.up a = some (p a) := by
  intro ⟨f, hf⟩
  exact hne (up_injective f (hf a₁) (hcol ▸ hf a₂))

/-- شاهد مجرّد: إسقاط الحركات من (حرف، حركة) يصدم كَتَبَ بكُتُب.
    ك=1 ت=2 ب=3؛ فتحة=10، ضمة=11، سكون=12 — الترميز مكتوب هنا للمثال لا من مودَع. -/
def kataba : List (Nat × Nat) := [(1,10), (2,10), (3,10)]
def kutub  : List (Nat × Nat) := [(1,11), (2,11), (3,12)]
def rasm (w : List (Nat × Nat)) : List Nat := w.map Prod.fst

theorem rasm_collides : kataba ≠ kutub ∧ rasm kataba = rasm kutub := by decide

theorem no_lossless_rasm :
    ¬ ∃ f : Bridge (List (Nat × Nat)) (List Nat), ∀ a, f.up a = some (rasm a) :=
  no_lossless_of_collision rasm rasm_collides.1 rasm_collides.2

/-! ## ٤. الجسر الدلالي: علاقة مرتَّبة لا تحذف -/

/-- إدراج بحسب درجة. -/
def insertBy {β} (score : β → Nat) (x : β) : List β → List β
  | [] => [x]
  | y :: ys => if score y ≤ score x then x :: y :: ys else y :: insertBy score x ys

/-- ترتيب المرشَّحات بحسب درجة (شاهد/قرينة). -/
def rank {β} (score : β → Nat) : List β → List β
  | [] => []
  | x :: xs => insertBy score x (rank score xs)

theorem mem_insertBy {β} (score : β → Nat) (x z : β) (l : List β) :
    z ∈ insertBy score x l ↔ z = x ∨ z ∈ l := by
  induction l with
  | nil => simp [insertBy]
  | cons y ys ih =>
    simp only [insertBy]
    split
    · simp
    · simp [ih]; constructor
      · rintro (h | h | h) <;> simp [h]
      · rintro (h | h | h) <;> simp [h]

/-- يرتّب ولا يحذف: كل مرشَّح قبل الترتيب باقٍ بعده، ولا يُزاد غيره. -/
theorem mem_rank {β} (score : β → Nat) (z : β) (l : List β) :
    z ∈ rank score l ↔ z ∈ l := by
  induction l with
  | nil => simp [rank]
  | cons x xs ih => simp [rank, mem_insertBy, ih]

theorem length_rank {β} (score : β → Nat) (l : List β) :
    (rank score l).length = l.length := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    simp only [rank]
    suffices ∀ m : List β, (insertBy score x m).length = m.length + 1 by
      rw [this, ih]; rfl
    intro m
    induction m with
    | nil => rfl
    | cons y ys ihm => simp only [insertBy]; split <;> simp [ihm]

/-! ## ٥. مراتب المخرج الثلاث (المادة ١٥–١٦) -/

/-- مخرج وحدة الحكم ثلاثيّ: من حيث هي / معلومة / مفهوم (بشاهد). -/
inductive Grade (W : Type)
  | minHaythuHiya
  | maluma
  | mafhum (witness : List W) (nonempty : witness ≠ [])

/-- لا «مفهوم» بلا شاهد: يُبرهَن من نوع المُنشئ نفسه. -/
theorem mafhum_has_witness {W} (g : Grade W) :
    ∀ w h, g = Grade.mafhum w h → w ≠ [] :=
  fun _ h _ => h

end Ghanem.Fractal

#print axioms Ghanem.Fractal.comp_down_up
#print axioms Ghanem.Fractal.no_lossless_rasm
#print axioms Ghanem.Fractal.mem_rank
#print axioms Ghanem.Fractal.length_rank
#print axioms Ghanem.Fractal.cv_bad2
