"""`Σ_AR`: ترتيبُ منزلةِ `G0.FLT-1.Q` بإزاء النواة اللغويّة، لا نسخُه ولا منافستُه.

النتيجةُ الأولى لنصّ القياس **قد قُرِئت**، ولذلك بابُ `SupersessionRecord`
مُغلَقٌ بحكم شرطه المنصوص: الاستبدالُ مُرخَّصٌ ما لم تُقرَأ نتيجةٌ من النصّ
المُستبدَل. وليس هذا الموضعُ استبدالًا أصلًا:

    Representation(x)     = (Carrier, State)   ← كيف يوجد الكيانُ في النظام؟
    LinguisticFunction(x) = RelationalRole(x)  ← ماذا يفعل بوصفه لغة؟

فالسؤالان مختلفان، ولا تناقضَ مُبرهَنًا بينهما؛ والسجلُّ المُودَع هنا **يُرتّب
منزلةً** ولا يُفنّد نتيجةً، ونصُّ القياس يبقى بلفظه وبصمته وقراءته المُسجَّلة.

**والبصمةُ مُشتَقّةٌ لا منقولة**: تُؤخَذ من `flt1_qiyas_law` في موضعها، فلا
نسختان لبصمةٍ واحدةٍ تنحرفان.

**وهذا الموضعُ هو الجهةُ الوحيدة التي تجمع المستويين**: `linguistic/` لا تستورد
من `arabic/` بحال، و`arabic/` تستورد منها؛ فجمعُ النواة بنصّ القياس يقع هنا
وحدَه، حفظًا للاتّجاه `metaalgebra → linguistic → arabic`.

تسجيلٌ لا سلطة: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا تستورد هذه
الوحدةُ من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from typing import Final

from alghanem.linguistic.relativization import (
    ContradictionStanding,
    HigherOrderRelativizationRecord,
    RelativizedStatementRef,
)

from .flt1_qiyas_law import FLT1_QIYAS_TEXT_DIGEST

__all__ = [
    "FLT1_QIYAS_RELATIVIZATION",
    "FLT1_QIYAS_STATEMENT_REF",
    "READ_RESULT_CLOSES_THE_SUPERSESSION_DOOR_NOTE",
]

READ_RESULT_CLOSES_THE_SUPERSESSION_DOOR_NOTE: Final[str] = (
    "ReadResultClosesTheSupersessionDoor: `SupersessionIsNotEditing` يُرخِّص "
    "الاستبدالَ ما لم تُقرَأ نتيجةٌ من النصّ المُستبدَل، وقد قُرِئت نتيجةُ "
    "`G0.FLT-1.Q`؛ فلا استبدالَ هنا، ولا منافسةَ بلا تناقضٍ مُبرهَن"
)

FLT1_QIYAS_STATEMENT_REF: Final[RelativizedStatementRef] = RelativizedStatementRef(
    statement_id="G0.FLT-1.Q",
    module_path="src/alghanem/arabic/flt1_qiyas_law.py",
    text_digest=FLT1_QIYAS_TEXT_DIGEST,
)

FLT1_QIYAS_RELATIVIZATION: Final[HigherOrderRelativizationRecord] = (
    HigherOrderRelativizationRecord(
        record_id="G0.NSB-0.relativization-of-FLT1Q",
        relativized=FLT1_QIYAS_STATEMENT_REF,
        representation_question="كيف يوجد الكيانُ في النظام؟ — حاملٌ وحالة",
        relational_question="ماذا يفعل الكيانُ بوصفه لغة؟ — دورٌ في نسبة",
        contradiction_standing=ContradictionStanding.NO_CONTRADICTION_DEMONSTRATED,
        what_would_make_it_competing=(
            "تناقضٌ مُبرهَنٌ مُبيَّنُ الموضع بين نتيجةِ نصّ القياس ودعوى النسبة؛ "
            "وعند ذلك يُطلَب سجلٌّ من جنسٍ آخر لا تُصدِره هذه الوحدةُ ولا يُقرَأ "
            "هذا السجلُّ بديلًا عنه"
        ),
    )
)
"""سجلُّ ترتيبِ المنزلة؛ مثيلٌ واحدٌ مبنيٌّ على بصمةٍ مُشتَقّةٍ لا منقولة."""
