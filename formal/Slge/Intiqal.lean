import Slge.IntiqalTable

/-!
# سجلُّ الانتقالات: الأسماءُ في Lean، والفحصُ في الحارس

`IntiqalTable.registry` مولَّدٌ من `slge.intiqal.REGISTRY` بعد أن فحص الحارسُ (`tools/gen_intiqal_index.py`)
أنّ كلَّ دالّةِ انتقالٍ عامّة في الشجرة مسجَّلة، وأنّ كلَّ مبرهنةٍ مذكورة مدقَّقةٌ في `Audit.lean`. هنا ما يصحّ
برهانُه على الأسماء: لا صفّان لدالّةٍ واحدة (`registry_nodup`)، ولا صفٌّ ذو مبرهنةٍ بنوع «دَين» ولا صفٌّ
بلا مبرهنةٍ بنوعٍ غيرِ «دَين» (`kind_matches_theorem`)، والعددُ بأنواعه (`counts`). الإغلاقُ نفسُه ليس هنا:
هو في كلّ مبرهنةٍ باسمها حيث تعيش؛ وهذا السجلُّ **مفحوصٌ** بالأداة لا مبرهَنٌ على الدوالّ.
-/

namespace Slge.Intiqal

open Slge.IntiqalTable (registry)

def keys : List (String × String) := registry.map fun r => (r.1, r.2.1)

theorem registry_nodup : keys.Nodup := by decide

/-- النوعُ 2 (دَين) ⇔ لا مبرهنة. -/
theorem kind_matches_theorem :
    registry.all (fun r => (r.2.2.2 == 2) == (r.2.2.1 == "")) = true := by decide

def countKind (k : Nat) : Nat := (registry.filter (·.2.2.2 == k)).length

theorem counts : countKind 0 + countKind 1 + countKind 2 = registry.length := by decide

end Slge.Intiqal
