# ADR ١١٧ — دمجُ `main` في فرع العمل ثمّ دمجُ الفرع في `main` (أمرُ المالك 2026-10-19 23:41)

**الحال:** مقبول. لا يمسّ `gate/` ولا Lean.

## السبب

قال المالك: «ادمج في الغانم». و`main` فيه ثلاثةُ إيداعاتٍ ليست في `claude/official-gate` (‏`6cc0f67`، `aa64e54`، ودمجُ PR #215
`0c83835`، 2026-10-14)، والفرعُ فيه 188 إيداعًا ليست في `main`؛ وأساسُهما المشترك `f922938` (دمجُ PR #213). وكانت نسخةُ الجلسة
ضحلةً فظهر التاريخان بلا أصلٍ مشترك («refusing to merge unrelated histories»)، فأُعمقت (`git fetch --unshallow`) قبل الدمج.

## التعارضُ وحلُّه

PR #215 أضاف أربعة ملفّاتٍ في `src/` و`tests/`، والفرعُ نقل `src/` و`tests/` القديمة إلى `suspended/` بالقانون الواحد (ADR ١
وما بعده). فوضعتُ الأربعة في `suspended/` حيث اقترح git، لا في الشجرة الحيّة:

* `suspended/src/alghanem/ontology/world_knowledge.py`، `suspended/src/alghanem/arabic/world_knowledge_gap.py`
* `suspended/tests/ontology/test_world_knowledge.py`، `suspended/tests/arabic/test_world_knowledge_gap.py`

وعُدّل `suspended/src/alghanem/arabic/pair_sample_widening.py` و`docs/VISION.md` بدمجٍ آليٍّ بلا تعارض. وولّد
`tools/gen_registry.py` السجلَّ: 1035 ← 1039 وحدةً معلَّقة، بسبب صنفها وشرط عودتها الثلاثيّ.

**تعيينُ البنّاء (م٢٢):** التعليقُ لا الإدخال، لأنّ هذه الوحدات تقرأ النصَّ خارج البوّابة وقد كُتبت قبل القانون الواحد؛ ولا
تعود إلّا بشروط `RE_ADMIT` الثلاثة. والتعليقُ نقلٌ لا حذف: التاريخُ في git.
