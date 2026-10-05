/-!
# رتبةُ الجواب — يقينٌ وظنٌّ وراجحٌ ومرجوحٌ ومردودٌ وتعادل

المصادر (نصوصها في `src/slge/rank.py` بمواضعها):

* الغزالي، «محكّ النظر»، مراتب الإدراك: اليقينُ قطعٌ لا يجوز معه الغلط، والظنُّ سكونُ
  نفسٍ مع الشعور بالنقيض «وله درجات … لا تحصى»، يقوى بانضمام شاهدٍ ثانٍ وثالث؛ و«كانت
  النتيجة الحاصلة يقينية ضرورية بحسب ذوق المقدمات».
* النبهاني، «التفكير»: «إذا تعارض القطعي والظني يؤخذ القطعي ويرد الظني».
* النبهاني، «الشخصية» ج٣ ¶1060–1065: التعادلُ لا يقع بين قطعيّين ولا بين قطعيٍّ وظنّيّ،
  «والترجيح يختص بالأدلة الظنية».

## ما يُبرهَن

1. `pathGrade_qati_iff`: الطريقُ قطعيٌّ **إذا وفقط إذا** كان كلُّ ما فيه قطعيًّا — فلا
   ترقيةَ لنتيجةٍ فوق أضعف مقدّماتها (`no_promotion`).
2. `weigh_swap`: الوزنُ متناظر: ما هو راجحٌ من جهةٍ مرجوحٌ من الأخرى، واليقينُ يقابله المردود.
3. `qati_never_loses`: القطعيُّ لا يكون مردودًا ولا مرجوحًا أبدًا.
4. `mardud_iff`: لا يُردّ إلّا ظنّيٌّ عارضه قطعيّ.
5. `tanaqud_iff`: تعارضُ قطعيّين ليس ترجيحًا بل تناقضٌ في الرصيد.
6. `taadul_iff`: التعادلُ ظنّيّان متساويا الشواهد، لا غير.
7. `specific_wins`، `general_is_makhsus`: إذا كان أحدُ المتعارضين أخصَّ عُمل بالخاصّ أيًّا كان
   ثبوتُه، والعامُّ **مخصوصٌ لا مردود** — ج٣ ¶1065: «فإن كان المقطوع به عاماً والمظنون خاصاً
   عمل بالمظنون … فحينئذ يرجح الخاص على العام، ويعمل به جمعاً بين الدليلين».
-/

namespace Slge.Rank

/-- ثبوتُ مقدّمةٍ أو دلالةُ خطوة. -/
inductive Grade where
  | zanni
  | qati
  deriving DecidableEq, Repr

/-- الأدنى من اثنين. -/
def Grade.meet : Grade → Grade → Grade
  | .qati, .qati => .qati
  | _, _ => .zanni

/-- رتبةُ الطريق: أدنى ما فيه. -/
def pathGrade : List Grade → Grade
  | [] => .qati
  | g :: gs => g.meet (pathGrade gs)

theorem pathGrade_qati_iff : ∀ gs : List Grade, pathGrade gs = .qati ↔ ∀ g ∈ gs, g = .qati
  | [] => by simp [pathGrade]
  | g :: gs => by
    rw [List.forall_mem_cons, ← pathGrade_qati_iff gs]
    cases g <;> cases h : pathGrade gs <;> simp [pathGrade, Grade.meet, h]

/-- **لا ترقية:** ظنّيٌّ واحدٌ في الطريق يجعله ظنّيًّا. -/
theorem no_promotion (gs : List Grade) (h : Grade.zanni ∈ gs) : pathGrade gs = .zanni := by
  cases hp : pathGrade gs with
  | zanni => rfl
  | qati => exact absurd ((pathGrade_qati_iff gs).1 hp _ h) (by decide)

/-- جانبٌ من التعارض: رتبتُه، وعددُ شواهده المستقلّة. -/
structure Side where
  grade : Grade
  strength : Nat
  deriving DecidableEq, Repr

/-- الحكم. -/
inductive Verdict where
  | yaqin
  | zann
  | rajih
  | marjuh
  | mardud
  | taadul
  | tanaqud
  | makhsus
  deriving DecidableEq, Repr

/-- بلا معارض. -/
def alone : Grade → Verdict
  | .qati => .yaqin
  | .zanni => .zann

/-- حكمُ الجانب الأوّل إذا عارضه الثاني. -/
def weigh (a b : Side) : Verdict :=
  match a.grade, b.grade with
  | .qati, .qati => .tanaqud
  | .qati, .zanni => .yaqin
  | .zanni, .qati => .mardud
  | .zanni, .zanni =>
    if b.strength < a.strength then .rajih
    else if a.strength < b.strength then .marjuh
    else .taadul

/-- الحكمُ من الجهة الأخرى. -/
def opposite : Verdict → Verdict
  | .yaqin => .mardud
  | .mardud => .yaqin
  | .rajih => .marjuh
  | .marjuh => .rajih
  | v => v

/-- الوزنُ مع الخصوص: الأخصُّ يُعمل به، والعامُّ مخصوص؛ وإلّا فالوزنُ بالثبوت والشواهد. -/
def weighS (a b : Side) (aSpecific bSpecific : Bool) : Verdict :=
  match aSpecific, bSpecific with
  | true, false => alone a.grade
  | false, true => .makhsus
  | _, _ => weigh a b

theorem weigh_swap (a b : Side) : weigh b a = opposite (weigh a b) := by
  cases a with
  | mk ga sa =>
    cases b with
    | mk gb sb =>
      cases ga <;> cases gb <;> simp only [weigh, opposite]
      by_cases h1 : sb < sa
      · have : ¬ sa < sb := by omega
        simp [h1, this]
      · by_cases h2 : sa < sb
        · simp [h1, h2]
        · simp [h1, h2]

theorem qati_never_loses (a b : Side) (h : a.grade = .qati) :
    weigh a b ≠ .mardud ∧ weigh a b ≠ .marjuh := by
  cases a with
  | mk ga sa =>
    cases b with
    | mk gb sb =>
      simp only at h
      subst h
      cases gb <;> simp [weigh]

theorem mardud_iff (a b : Side) : weigh a b = .mardud ↔ a.grade = .zanni ∧ b.grade = .qati := by
  cases a with
  | mk ga sa =>
    cases b with
    | mk gb sb =>
      cases ga <;> cases gb <;> simp only [weigh] <;> (try split) <;> (try split) <;> simp_all

theorem tanaqud_iff (a b : Side) : weigh a b = .tanaqud ↔ a.grade = .qati ∧ b.grade = .qati := by
  cases a with
  | mk ga sa =>
    cases b with
    | mk gb sb =>
      cases ga <;> cases gb <;> simp only [weigh] <;> (try split) <;> (try split) <;> simp_all

theorem taadul_iff (a b : Side) :
    weigh a b = .taadul ↔ a.grade = .zanni ∧ b.grade = .zanni ∧ a.strength = b.strength := by
  cases a with
  | mk ga sa =>
    cases b with
    | mk gb sb =>
      cases ga <;> cases gb <;> simp only [weigh]
      all_goals first
        | (simp; done)
        | (by_cases h1 : sb < sa
           · simp [h1]; omega
           · by_cases h2 : sa < sb
             · simp [h1, h2]; omega
             · simp [h1, h2]; omega)

theorem specific_wins (a b : Side) : weighS a b true false = alone a.grade := rfl

theorem general_is_makhsus (a b : Side) :
    weighS a b false true = .makhsus ∧ weighS a b false true ≠ .mardud := by
  simp [weighS]

/-- **الخصوصُ مقدَّمٌ على الثبوت:** عامٌّ قطعيٌّ يعارضه خاصٌّ ظنّيٌّ فيُعمل بالظنّيّ. -/
theorem qati_general_yields_to_zanni_specific (s t : Nat) :
    weighS ⟨.zanni, s⟩ ⟨.qati, t⟩ true false = .zann := rfl

/-- وبلا خصوصٍ يرجع الوزنُ إلى `weigh` بعينه. -/
theorem same_scope_is_weigh (a b : Side) (x : Bool) : weighS a b x x = weigh a b := by
  cases x <;> rfl

end Slge.Rank
