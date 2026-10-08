import Slge.Ilal
import Slge.IlalBabTable

/-!
# أبوابُ الإعلال عند سيبويه — الحدُّ الأدنى المكتمل

المصدرُ الكتابُ المختوم (الجدولُ `IlalBabTable` مولَّدٌ منه ومن مودَع المصحف بـ`tools/deposit_ilal_bab.py`).
كلُّ قاعدةٍ من قواعد `Slge.Ilal` الثلاثَ عشرةَ لها **بابٌ واحدٌ بسطره وشاهدٌ من نصّ الباب** رسمًا
(`every_rule_once`)؛ وثماني قواعد لها فوق ذلك **صورةٌ من مودَع المصحف تقرؤها القاعدةُ نفسُها**
(`witnesses_read`: `undo` غيرُ فارغ في موضعها)؛ والخمسُ الباقيةُ شاهدُها رسمٌ بلا خانات — لم تُشكَّل من
الذاكرة (`unwitnessed`). وما يذكره سيبويه بابًا ولا قاعدةَ له عندنا دينٌ مسمًّى بسطره (`debts_named`).
كلُّ ذلك بـ`decide` على الجدول: مبرهَنٌ على المودَع لا «لكلّ».
-/

namespace Slge.IlalBab

open Slge.Ilal

/-- صفُّ الجدول: (رقمُ القاعدة، سطرُ الباب، شاهدُ الباب حواملَ، صورةُ المصحف خاناتٍ، موضعُ القراءة). -/
abbrev Row := Nat × Nat × List Nat × List SCell × Nat

def rule (r : Row) : Nat := r.1
def line (r : Row) : Nat := r.2.1
def witness (r : Row) : List Nat := r.2.2.1
def cells (r : Row) : List SCell := r.2.2.2.1
def pos (r : Row) : Nat := r.2.2.2.2

/-- لكلّ قاعدةٍ في `Rule.all` صفٌّ واحدٌ بترتيبها، وشاهدُ بابها حواملُ من التسعة والعشرين غيرُ فارغ. -/
theorem every_rule_once :
    table.map rule = List.range Rule.all.length ∧
    table.all (fun r => !(witness r).isEmpty && (witness r).all (· < 29)) = true := by decide

/-- هل تقرأ القاعدةُ صورةَ المصحف في موضعها؟ -/
def reads (r : Row) : Bool :=
  match (Rule.all.drop (rule r)).head? with
  | some ρ => !(undo ρ (cells r) (pos r)).isEmpty
  | none => false

/-- الصفوفُ التي لها صورةٌ من المصحف. -/
def witnessed : List Row := table.filter (fun r => !(cells r).isEmpty)

/-- ثماني قواعد تقرأ صورتَها المودَعة بعينها: القلبُ والحذفُ بوجهيه والنقلُ (خاف، قلت، خفت، يقول)،
وقلبُ اللام (رمى)، وحذفُ الواو (يعد)، وهمزةُ المدّ (آدم)، والواوُ ياءً (الميزان). -/
theorem witnesses_read :
    witnessed.length = 8 ∧ witnessed.map rule = [0, 1, 2, 3, 4, 6, 7, 11] ∧
    witnessed.all reads = true := by decide

/-- خمسٌ شاهدُها رسمُ الباب بلا خانات: حذفُ اللام، والتاءُ طاءً، والتاءُ دالًا، والفاءُ تاءً،
والياءُ واوًا — غائبةٌ باسمها لا مشكَّلةٌ من الذاكرة. -/
theorem unwitnessed :
    (table.filter (fun r => (cells r).isEmpty)).map rule = [5, 8, 9, 10, 12] := by decide

/-- الديونُ: سبعةُ أبوابٍ بأسطرها، لا تكرارَ فيها ولا تداخلَ مع أسطر الأبواب المودَعة. -/
theorem debts_named :
    debts.length = 7 ∧ debts.Nodup ∧ debts.all (fun n => !(table.map line).contains n) = true := by
  decide

end Slge.IlalBab
