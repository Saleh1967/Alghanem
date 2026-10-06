import Slge.Bridge

/-!
# المنح: لا اسمَ قبل قبضته

قانونُ الجسر كما وصل في `tarkib/bridge.py`: ‎grants = Λ(observables, witness, check)‎. هناك
كان `check` **سلسلةَ نصٍّ** و`check_verdict` حقلًا يُملأ باليد («PASS»)، فيقبل المنحُ ما كُتب
فيه. وهنا الفحصُ **دالّةٌ** على الخانات، والمنحُ **برهانٌ** بأنّها أعادت `true`؛ فلا يُصاغ
منحٌ بلا فحصٍ جرى، لا بالقول ولا بالتزوير (`grant_iff_check`).

والسُّلَّمُ سلسلةُ جسورٍ كلُّ درجةٍ تشترط ما تحتها (`Ladder`)، فمنحُ الدرجة ‎n+1‎ يستلزم منحَ
‎n‎ (`ladder_implies_lower`)، ومنحُ أيّ درجةٍ يستلزم الدرجةَ الأولى (`ladder_implies_base`).
والدرجةُ الأولى المودَعة واحدة: **المرسوم** — فحصُها الترخيصُ نفسُه (`licensed`)، فلا يُمنح
«مرسوم» إلّا لمرخَّصٍ (`mursam_sound`). ما فوقها معلَنٌ لا مبرهَن.
-/

namespace Slge.Grant

/-- الجسر: اسمُه، ما يمنحه، وفحصُه دالّةً لا نصًّا. -/
structure Bridge (α : Type) where
  name : String
  grants : String
  check : α → Bool

/-- المنحُ برهانُ فحصٍ جرى؛ لا حقلَ فيه يُملأ. -/
def Granted {α : Type} (b : Bridge α) (x : α) : Prop := b.check x = true

theorem grant_iff_check {α : Type} (b : Bridge α) (x : α) :
    Granted b x ↔ b.check x = true := Iff.rfl

/-- ما رفضه الفحصُ لا يُمنح، مهما قيل. -/
theorem no_grant_of_refused {α : Type} (b : Bridge α) (x : α) (h : b.check x = false) :
    ¬ Granted b x := by
  intro hg; unfold Granted at hg; rw [h] at hg; exact Bool.false_ne_true hg

/-- السُّلَّم: الدرجةُ ‎n+1‎ تمنح إذا مُنحت ‎n‎ وجاز فحصُها هي. -/
def Ladder {α : Type} (rungs : List (Bridge α)) (x : α) : Nat → Prop
  | 0 => match rungs.head? with
         | some b => Granted b x
         | none => False
  | n + 1 => Ladder rungs x n ∧ (match rungs[n+1]? with
                                 | some b => Granted b x
                                 | none => False)

theorem ladder_implies_lower {α : Type} (rungs : List (Bridge α)) (x : α) (n : Nat)
    (h : Ladder rungs x (n + 1)) : Ladder rungs x n := h.1

theorem ladder_implies_base {α : Type} (rungs : List (Bridge α)) (x : α) :
    ∀ n, Ladder rungs x n → Ladder rungs x 0
  | 0, h => h
  | n + 1, h => ladder_implies_base rungs x n h.1

/-- لا درجةَ فوق سُلَّمٍ فارغ. -/
theorem empty_ladder_grants_nothing {α : Type} (x : α) (n : Nat) :
    ¬ Ladder ([] : List (Bridge α)) x n := by
  induction n with
  | zero => simp [Ladder]
  | succ n ih => intro h; exact ih h.1

/-- الدرجةُ الأولى المودَعة: المرسوم؛ فحصُه الترخيص. -/
def mursam : Bridge (List SCell) := ⟨"b-mursam", "مرسوم", licensed⟩

/-- لا يُمنح «مرسوم» إلّا لمرخَّص — وهو بالجسر `Admissible` في الـ116. -/
theorem mursam_sound (w : List SCell) (h : Granted mursam w) :
    A116.Admissible (w.map toCell) := (licensed_iff w).1 h

/-- شاهدُ رفض: ساكنٌ في الصدر لا يُمنح. -/
theorem mursam_refuses_initial_sukun (c : Fin 29) (rest : List SCell) :
    ¬ Granted mursam (⟨c, 3⟩ :: rest) := by
  apply no_grant_of_refused
  show licensed (⟨c, 3⟩ :: rest) = false
  have h3 : SCell.isSukun ⟨c, 3⟩ = true := by rfl
  simp [licensed, h3]

end Slge.Grant
