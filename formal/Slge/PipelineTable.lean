import Slge.Pipeline

/-! قمعُ السُّلَّم على MASAQ: العابرون قبل المراحل وبعد كلٍّ منها — مولَّدٌ بـ
`tools/gen_pipeline_index.py` من `masaq-shibh.json.gz` و`corpus-certificates.json.gz`؛
لا يُحرَّر باليد. الصارمُ: قسمةٌ واحدة محسومة (Hasm)؛ المرتَّبُ: الأولى بعد الترتيب ذهبيّة. -/

namespace Slge.PipelineTable

/-- 40731 كلمةً؛ العابرون بعد 0..5 مراحل (الصارم). -/
def strict : List Nat := [40731, 40731, 32592, 11596, 6563, 2070]

/-- العابرون بعد 0..5 مراحل (المرتَّب). -/
def ranked : List Nat := [40731, 40731, 32683, 11423, 6502, 2023]

/-- القمعان سلسلتان متناقصتان على خمس مراحل. -/
theorem funnels : Pipeline.Antitone strict ∧ Pipeline.Antitone ranked ∧
    strict.length = 6 ∧ ranked.length = 6 := by decide

end Slge.PipelineTable
