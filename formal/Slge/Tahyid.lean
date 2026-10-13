/-!
# التحييد: الصورةُ القانونيّة للنصّ المستخرَج من حاويته (ADR ٥٩)

النصُّ المختوم بابٌ على حاوية: كلُّ فقرةٍ من `document.xml` نصوصُها موصولة، والفقراتُ بسطر، بلا تطبيع. والبابان
القائمان (SLGE وhamil) على حاويةٍ واحدة (ج3) يختلفان بقواعدَ مسمّاة: الجداولُ وصناديقُ النصّ، والجدولة، والمسافاتُ في
الطرفين، والأسطرُ الفارغة. فهويّةُ النصّ **صفٌّ تكافؤيّ** ممثّلُه الصورةُ القانونيّة (`canon`): تُحذف الأسطرُ المستثناةُ
بالبنية (علامةٌ يحملها السطرُ من الباب، لا من محتواه)، ثمّ تُحذف الجدولة، ثمّ تُقصّ المسافاتُ من الطرفين، ثمّ يُحذف
الفارغ.

## ما يُبرهَن

* **الحذفُ والتعديل** (`dropL`، `mapL`): الحذفُ مستقرّ (`dropL_idem`)، والحذفان يتبادلان دائمًا (`dropL_comm`)،
  والحذفُ بعد التعديل حذفٌ بالمحمول المركَّب قبله (`drop_after_map`)، فيتبادلان إذا لم يغيّر التعديلُ حكمَ المحمول
  (`comm_of_invariant`)؛ والتعديلُ المستقرُّ لا يتغيّر بتكراره (`mapL_idem`).
* **والترتيبُ يغيّر الناتجَ في العموم** (`order_matters`): سطرٌ آخرُه مسافةٌ ثمّ جدولة — فالقولُ «القواعدُ مستقلّةٌ
  فترتيبُها لا يغيّر» خاطئٌ بإطلاقه، والترتيبُ هنا معلنٌ ثابت، وأزواجُ الالتقاء تُعدّ على النصّ (`tools/deposit_tahyid.py`).
* **الشكلُ لا يُمسّ** (`marks_preserved`): كلُّ حرفٍ غيرِ المسافة والجدولة عددُه في الصورة القانونيّة عددُه في الأسطر
  غيرِ المستثناة — فالتحييدُ لا يحذف علامةَ شكلٍ ولا حرفًا.
* **القصُّ مستقرّ في طرفه** (`dropWhile_idem`)، وشاهدٌ محسوب على نصٍّ صغير (`witness`).

المبرهَنُ خواصُّ هذه الدوالّ على الأسطر؛ وأنّ البابَ يعيد المختومَ بايتًا بايتًا وأنّ الصورتين القانونيّتين لاستخراجَي ج3
واحدة — فحصٌ بالأداة على المودَع، لا برهان.
-/

namespace Slge.Tahyid

abbrev Line := List Char
abbrev Text := List Line

/-- حذفُ الأسطر التي يصدق عليها محمول. -/
def dropL (P : Line → Bool) (t : Text) : Text := t.filter (fun l => !P l)

/-- تعديلُ كلّ سطر. -/
def mapL (f : Line → Line) (t : Text) : Text := t.map f

theorem dropL_idem (P : Line → Bool) (t : Text) : dropL P (dropL P t) = dropL P t := by
  simp [dropL, List.filter_filter]

theorem dropL_comm (P Q : Line → Bool) (t : Text) : dropL P (dropL Q t) = dropL Q (dropL P t) := by
  simp only [dropL, List.filter_filter]
  congr 1; funext l; cases P l <;> cases Q l <;> rfl

theorem mapL_idem (f : Line → Line) (hf : ∀ l, f (f l) = f l) (t : Text) :
    mapL f (mapL f t) = mapL f t := by
  simp [mapL, List.map_map, Function.comp_def, hf]

theorem drop_after_map (P : Line → Bool) (f : Line → Line) (t : Text) :
    dropL P (mapL f t) = mapL f (dropL (fun l => P (f l)) t) := by
  simp [dropL, mapL, List.filter_map, Function.comp_def]

theorem comm_of_invariant (P : Line → Bool) (f : Line → Line) (h : ∀ l, P (f l) = P l) (t : Text) :
    dropL P (mapL f t) = mapL f (dropL P t) := by
  rw [drop_after_map]; congr 1; simp [dropL, h]

/-- حذفُ الجدولة. -/
def delTab (l : Line) : Line := l.filter (· != '\t')

/-- قصُّ المسافات من الطرفين. -/
def stripSp (l : Line) : Line :=
  ((l.dropWhile (· == ' ')).reverse.dropWhile (· == ' ')).reverse

theorem order_matters : stripSp (delTab ['a', ' ', '\t']) ≠ delTab (stripSp ['a', ' ', '\t']) := by
  decide

theorem dropWhile_idem (p : Char → Bool) : ∀ l : Line, (l.dropWhile p).dropWhile p = l.dropWhile p
  | [] => rfl
  | x :: xs => by
    by_cases h : p x = true
    · simp [h, dropWhile_idem p xs]
    · simp [h]

theorem count_dropWhile_sp (c : Char) (hc : c ≠ ' ') :
    ∀ l : Line, (l.dropWhile (· == ' ')).count c = l.count c
  | [] => rfl
  | x :: xs => by
    by_cases h : x = ' '
    · subst h
      simp only [List.dropWhile_cons, beq_self_eq_true, ↓reduceIte]
      rw [count_dropWhile_sp c hc xs, List.count_cons]
      simp [Ne.symm hc]
    · have : (x == ' ') = false := by simpa using h
      simp [this]

theorem count_stripSp (c : Char) (hc : c ≠ ' ') (l : Line) : (stripSp l).count c = l.count c := by
  simp only [stripSp, List.count_reverse]
  rw [count_dropWhile_sp c hc, List.count_reverse, count_dropWhile_sp c hc]

theorem count_delTab (c : Char) (hc : c ≠ '\t') : ∀ l : Line, (delTab l).count c = l.count c
  | [] => rfl
  | x :: xs => by
    have ih := count_delTab c hc xs
    simp only [delTab] at ih ⊢
    by_cases h : x = '\t'
    · subst h
      simp only [List.filter_cons, bne_self_eq_false, Bool.false_eq_true, ↓reduceIte, ih,
        List.count_cons]
      simp [Ne.symm hc]
    · have hx : (x != '\t') = true := by simpa using h
      simp only [List.filter_cons, hx, ↓reduceIte, List.count_cons, ih]

/-- الصورةُ القانونيّة: السطرُ يحمل علامةَ الاستثناء البنيويّ من الباب. -/
def clean (l : Line) : Line := stripSp (delTab l)

def canon (t : List (Bool × Line)) : Text :=
  dropL List.isEmpty (mapL clean ((t.filter (fun p => !p.1)).map (·.2)))

theorem count_clean (c : Char) (h1 : c ≠ ' ') (h2 : c ≠ '\t') (l : Line) :
    (clean l).count c = l.count c := by
  simp only [clean]; rw [count_stripSp c h1, count_delTab c h2]

theorem count_flatten_dropEmpty (c : Char) : ∀ t : Text,
    ((dropL List.isEmpty t).flatten).count c = t.flatten.count c
  | [] => rfl
  | l :: ls => by
    have ih := count_flatten_dropEmpty c ls
    simp only [dropL] at ih
    cases l with
    | nil =>
      simp only [dropL, List.filter_cons, List.isEmpty_nil, Bool.not_true, Bool.false_eq_true,
        ↓reduceIte, List.flatten_cons, List.nil_append]
      exact ih
    | cons x xs =>
      simp only [dropL, List.filter_cons, List.isEmpty_cons, Bool.not_false, ↓reduceIte,
        List.flatten_cons, List.count_append]
      rw [ih]

theorem count_flatten_map_clean (c : Char) (h1 : c ≠ ' ') (h2 : c ≠ '\t') : ∀ t : Text,
    ((mapL clean t).flatten).count c = t.flatten.count c
  | [] => rfl
  | l :: ls => by
    have ih := count_flatten_map_clean c h1 h2 ls
    simp only [mapL] at ih ⊢
    simp [List.flatten_cons, List.count_append, ih, count_clean c h1 h2]

/-- الشكلُ والحروفُ لا تُمسّ: كلُّ حرفٍ غيرِ المسافة والجدولة عددُه في الصورة القانونيّة عددُه في غير المستثنى. -/
theorem marks_preserved (c : Char) (h1 : c ≠ ' ') (h2 : c ≠ '\t') (t : List (Bool × Line)) :
    (canon t).flatten.count c = (((t.filter (fun p => !p.1)).map (·.2)).flatten).count c := by
  simp only [canon]
  rw [count_flatten_dropEmpty, count_flatten_map_clean c h1 h2]

theorem witness :
    canon [(false, [' ', 'a', '\t', 'b', ' ']), (false, [' ', '\t']), (true, ['x']), (false, ['c'])] =
      [['a', 'b'], ['c']] := by decide

end Slge.Tahyid
