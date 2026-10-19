"""محوِّلٌ اصطناعيٌّ: أربعُ حالاتٍ مفحوصةٍ باليد، بلا مدوَّنةٍ ولا ملفّ.

المحوّلُ عميلُ الطبقة لا جزؤها: الاتّجاه `adapter → core` ولا عكس، فالقلبُ لا
يستورد من هنا شيئًا. وترتيبُ المحوّلات مُصرَّحٌ به ومقصود:

```
SyntheticAdapter → MASAQAdapter → QuranAdapter
```

والاصطناعيُّ أوّلٌ لأنّ حالاته مفحوصةٌ باليد، فإن سقط اختبارٌ عليها كان الخللُ
في الطبقة قطعًا لا في المدوَّنة؛ وهذا تمييزٌ لا يتيسّر إن بدأنا بمدوَّنةٍ
ضخمةٍ يختلط فيها خطأُ القراءة بخطأ البناء. والمحوّلان الآخران **مؤجَّلان** ولا
يُبنى منهما شيءٌ في هذه المرحلة.

الحالاتُ الأربع مختارةٌ لتغطية أجناسٍ متمايزة: جامدٌ، ومشتقٌّ، ومعرَّب، وحرف.
ولا يحمل المحوّلُ حكمًا على أيٍّ منها: `SyntheticCaseIsNotAttestedUsage`،
فالحالةُ مُدخَلُ فحصٍ مُصرَّحٌ باصطناعه لا شاهدُ استعمالٍ منقول.

تسجيلٌ لا سلطة.
"""

from __future__ import annotations

from typing import Final

from .lexical_evidence_layer import SurfaceOccurrence

__all__ = [
    "ADAPTER_ORDER",
    "SYNTHETIC_CASE_IS_NOT_ATTESTED_USAGE_NOTE",
    "SYNTHETIC_SOURCE_ID",
    "synthetic_occurrences",
]

SYNTHETIC_SOURCE_ID: Final[str] = "synthetic:lex0:v1"

ADAPTER_ORDER: Final[tuple[str, ...]] = (
    "SyntheticAdapter",
    "MASAQAdapter",
    "QuranAdapter",
)

SYNTHETIC_CASE_IS_NOT_ATTESTED_USAGE_NOTE: Final[str] = (
    "SyntheticCaseIsNotAttestedUsage: الحالةُ الاصطناعيّةُ مُدخَلُ فحصٍ مُصرَّحٌ "
    "باصطناعه، ولا تُنقَل شاهدَ استعمالٍ ولا تدخل إحصاءَ تغطية؛ فمصدرُها "
    "مُعرَّفٌ باسمه لئلّا يختلط بمدوَّنة"
)

_CASES: Final[tuple[tuple[str, str, str], ...]] = (
    ("جامد", "حجر", "1"),
    ("مشتق", "كاتب", "2"),
    ("معرب", "سندس", "3"),
    ("حرف", "على", "4"),
)


def synthetic_occurrences() -> tuple[SurfaceOccurrence, ...]:
    """ابنِ الوقوعاتِ الأربعةَ بترتيبها المُصرَّح، ولا تقرأ ملفًّا."""

    return tuple(
        SurfaceOccurrence(
            source_id=SYNTHETIC_SOURCE_ID,
            occurrence_id=f"{genus}:{occurrence_id}",
            raw_form=raw_form,
            source_position=occurrence_id,
            local_position=index,
        )
        for index, (genus, raw_form, occurrence_id) in enumerate(_CASES)
    )
