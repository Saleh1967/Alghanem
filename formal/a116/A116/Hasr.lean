/-!
# الحصرُ عند المجهول المسمّى: حدّا العدّ مبرهَنان (ADR ٣٧)

قياسُ نسبةٍ على مرجعٍ محجوب قد يتوقّف على معاملٍ لا يشهده المرجع (تعديةُ فعلٍ لم يُعلَّم، تشكيلُ مثالٍ ملتبس).
لا يُخمَّن المعامل: يُحصر العدُّ بين حدّين يصحّان **لكلّ** قيمةٍ له، وهما محقَّقان بقيمتين بعينهما فلا حدَّ أضيق.

* `hasr`: لكلّ عنصرٍ إصابتان ممكنتان `a` و`b` (بحسب قيمة المعامل)، ولكلّ اختيارٍ `c`، عددُ الإصابات بين عدّ
  `a && b` وعدّ `a || b`.
* `hasr_tight_low`/`hasr_tight_high`: الحدّان يُبلَغان باختيارين مسمّيين.
* `countP_mono`: الإصابةُ مطّردةٌ في المتوقَّع — قاعدةٌ أوسعُ لا تُنقص الإصابة؛ فقواعدُ أمثلةٍ بين استخراجٍ صارمٍ
  وآخرَ مُرخًى تحصر الإصابةَ بين عدّيهما.
* `hasr_mono`: الحصران معًا — معاملٌ مجهولٌ وقاعدةٌ بين حدّين — حصرٌ واحد.

لا شيء هنا على اللغة: خواصُّ عدٍّ على قوائم، تُطبَّق في `tools/gen_lane.py` (`sensitivity`).
-/

namespace A116.Hasr

variable {α : Type}

/-- **الحصر**: لكلّ اختيارٍ للمعامل، عددُ الإصابات بين عدّ «كلاهما» وعدّ «أحدهما». -/
theorem hasr (a b c : α → Bool) (L : List α) :
    L.countP (fun x => a x && b x) ≤ L.countP (fun x => if c x then a x else b x) ∧
      L.countP (fun x => if c x then a x else b x) ≤ L.countP (fun x => a x || b x) := by
  induction L with
  | nil => simp
  | cons x L ih =>
    simp only [List.countP_cons]
    cases ha : a x <;> cases hb : b x <;> cases hc : c x <;> simp <;> omega

/-- الحدُّ الأدنى يُبلَغ: يُختار من الإصابتين أضعفُهما. -/
theorem hasr_tight_low (a b : α → Bool) (L : List α) :
    L.countP (fun x => if !a x then a x else b x) = L.countP (fun x => a x && b x) := by
  congr 1
  funext x
  cases a x <;> cases b x <;> rfl

/-- والأعلى يُبلَغ: يُختار أقواهما. -/
theorem hasr_tight_high (a b : α → Bool) (L : List α) :
    L.countP (fun x => if a x then a x else b x) = L.countP (fun x => a x || b x) := by
  congr 1
  funext x
  cases a x <;> cases b x <;> rfl

/-- **الاطّراد**: ما أصاب بالقاعدة الأضيق أصاب بالأوسع. -/
theorem countP_mono (p q : α → Bool) (h : ∀ x, p x = true → q x = true) (L : List α) :
    L.countP p ≤ L.countP q := by
  induction L with
  | nil => simp
  | cons x L ih =>
    simp only [List.countP_cons]
    cases hp : p x
    · cases q x <;> simp <;> omega
    · simp [h x hp]; omega

/-- **الحصران معًا**: معاملٌ مجهول (`c`) وقاعدةٌ بين صارمةٍ (`a₀`، `b₀`) ومُرخاةٍ (`a₁`، `b₁`). -/
theorem hasr_mono (a₀ b₀ a₁ b₁ c : α → Bool) (ha : ∀ x, a₀ x = true → a₁ x = true)
    (hb : ∀ x, b₀ x = true → b₁ x = true) (L : List α) :
    L.countP (fun x => a₀ x && b₀ x) ≤ L.countP (fun x => if c x then a₀ x else b₀ x) ∧
      L.countP (fun x => if c x then a₀ x else b₀ x) ≤ L.countP (fun x => if c x then a₁ x else b₁ x) ∧
      L.countP (fun x => if c x then a₁ x else b₁ x) ≤ L.countP (fun x => a₁ x || b₁ x) := by
  refine ⟨(hasr a₀ b₀ c L).1, countP_mono _ _ ?_ L, (hasr a₁ b₁ c L).2⟩
  intro x hx
  cases hc : c x
  · simp only [hc] at hx ⊢; exact hb x hx
  · simp only [hc] at hx ⊢; exact ha x hx

end A116.Hasr
