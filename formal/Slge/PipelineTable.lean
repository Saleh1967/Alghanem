import Slge.Pipeline

/-! قمعُ السُّلَّم على MASAQ: العابرون قبل المراحل وبعد كلٍّ منها — مولَّدٌ بـ
`tools/gen_pipeline_index.py` من `masaq-shibh.json.gz` و`corpus-certificates.json.gz`؛
لا يُحرَّر باليد. الصارمُ: قراءةُ جذعٍ واحدة لا غير؛ المرتَّبُ: الأولى بعد الترتيب ذهبيّة. -/

namespace Slge.PipelineTable

/-- 40731 كلمةً؛ العابرون بعد 0..5 مراحل (الصارم). -/
def strict : List Nat := [40731, 40731, 15583, 7549, 4990, 1763]

/-- العابرون بعد 0..5 مراحل (المرتَّب). -/
def ranked : List Nat := [40731, 40731, 26124, 10845, 5609, 1943]

/-- القمعان سلسلتان متناقصتان على خمس مراحل، والمرتَّبُ لا يقلّ عن الصارم مرحلةً مرحلة. -/
theorem funnels : Pipeline.Antitone strict ∧ Pipeline.Antitone ranked ∧
    strict.length = 6 ∧ ranked.length = 6 ∧ Pipeline.Dominates ranked strict := by decide

end Slge.PipelineTable
