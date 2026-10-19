"""تجميدُ نصّ «فرضية الانتقال المرخّص الفركتالي» حرفيًّا قبل أيّ تشغيل.

هذه الوحدةُ **لا تختبر شيئًا**. وظيفتها الوحيدة أن تُثبّت النصّ المطلوب
اختبارُه بصيغته الواردة — بعربيّته وبترميزه الرياضي كما كُتب، لا بإعادة صياغةٍ
نثريّةٍ له — وأن تُغلق مفردةَ الأحكام المسموحة، وأن تُسمّي الحقولَ التي يجوز
أن تدخل في معيار المطابقة والحقولَ التي لا يجوز. فمن جمّد النصَّ بعد رؤية
نتيجته لم يُجمّد شيئًا:

    FrozenAfterReadout != Frozen

**والترميزُ جزءٌ من النصّ لا زينةٌ عليه** (`NotationIsPartOfTheFrozenText`):
`\\mathcal K` و`S_{n\\to m}\\circ \\mathcal K_n \\cong \\mathcal K_m\\circ
S_{n\\to m}` و`\\boxed{...}` محفوظةٌ بحروفها في `HYPOTHESIS_TEXT`، وحارسٌ عند
الاستيراد يسقط الوحدةَ إن سقط واحدٌ من مواضعها المُسمّاة. ولذلك بُصِم النصُّ
ببصمةٍ **مُشتقّة لا مكتوبة**: أيُّ حرفٍ يتغيّر فيه لاحقًا يغيّر البصمة، وكلُّ
قراءةٍ تحمل بصمتَها فتُعرَف على أيِّ نصٍّ جرت.

**والأحكامُ أربعةٌ مغلقة** كما نصّ عليها النصُّ نفسه: `SUPPORTED` و`REFUTED`
و`UNDERPOWERED` و`WEAKER_MODEL_RECONSTRUCTS`. وليس في المفردة عضوٌ خامس، ولا
يوجد في هذه الوحدة — ولا يجوز أن يوجد في وحدةٍ تقرأ منها — رمزٌ اسمُه
`FRACTAL_LAW_PROVED` (`FractalLawProvedIsNotAnOutput`). وحارسُ الاستيراد يفحص
ذلك بالاسم لا بالنيّة.

**ومعيارُ المطابقة محصورٌ بستّة حقول** هي: الحامل، والبوّابة، وحفظ الهوية،
والأثر، والبقية، والإغلاق. وستّةٌ أخرى ممنوعةٌ من الدخول فيه صراحةً — التواتر،
والإنتروبيا، و`α`، وعددُ الحالات، والشكلُ السطحيّ، والمقدار — لأن النصَّ لا
يشترط حفظها، فإدخالُها في المعيار يُحوّل الفرضيةَ إلى دعوى تشابُهِ مقاديرَ لم
تُدَّعَ (`StructureMatchIsFieldRestricted`). ومن سمّى حقلًا خارج الستّة رُدَّ
عند النداء، لا نُبِّه بتحذير.

حدودُ الوحدة، مُسجَّلةً لا معتذَرًا عنها لاحقًا:

* لا بوّابةَ هنا، ولا قراءة، ولا حكم، ولا حالة اختبارٍ واحدة. تجميدُ النصّ لا
  يُقرِّبه من الصدق خطوةً واحدة: `FrozenHypothesis != SupportedHypothesis`.
* لا نوعَ في `kernel/` يقرأ هذه الوحدة، ولا `Freeze`، ولا `E0`، ولا ولادة.
* المفرداتُ المُغلقة هنا مفرداتُ **النصّ المطلوب اختبارُه**، ولا تُنسَب إلى
  مصدرٍ لغويٍّ ولا تُقرأ دعوى صحّةٍ عن العربية.
"""

from __future__ import annotations

from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "COMPARED_FIELDS",
    "EXCLUDED_FIELDS",
    "FORBIDDEN_VERDICT_NAME",
    "FRACTAL_LAW_PROVED_IS_NOT_AN_OUTPUT_NOTE",
    "FROZEN_AFTER_READOUT_IS_NOT_FROZEN_NOTE",
    "HYPOTHESIS_DIGEST",
    "HYPOTHESIS_TEXT",
    "HYPOTHESIS_TEXT_IS_VERBATIM_NOTE",
    "NOTATION_IS_PART_OF_THE_FROZEN_TEXT_NOTE",
    "REQUIRED_NOTATION_SITES",
    "STRUCTURE_MATCH_IS_FIELD_RESTRICTED_NOTE",
    "FractalTransitionHypothesisError",
    "FractalVerdict",
    "hypothesis_digest",
    "require_compared_field",
]


class FractalTransitionHypothesisError(ValueError):
    """رُفض مدخلٌ خارج النصّ المُجمَّد؛ ولا يُحمَل على أقرب حقلٍ مسموح."""


HYPOTHESIS_TEXT: Final[str] = r"""Fractal Licensed Transition Hypothesis

لتكن الطبقات اللغوية المرخّصة:

[
L_0,L_1,\ldots,L_n
]

مثل:

[
\text{حرف}\rightarrow
\text{مقطع}\rightarrow
\text{قالب/وزن}\rightarrow
\text{كلمة}\rightarrow
\text{تركيب}\rightarrow
\text{جملة}.
]

لا يُفترض أن القيم الإحصائية، أو عدد الحالات، أو الإنتروبيا، أو التوزيعات تتكرر بين الطبقات.

الادعاء الوحيد المراد اختباره هو:

[
\boxed{
\exists \mathcal K
;\text{بحيث تعمل بنية انتقال واحدة عبر أكثر من مقياس لغوي}
}
]

حيث:

[
\mathcal K=
(
C,G,O,I,E,R,T,Cl
)
]

وتمثل:

[
C=\text{Carrier}
]

[
G=\text{Gate}
]

[
O=\text{Operation}
]

[
I=\text{Identity Preservation}
]

[
E=\text{Evidence}
]

[
R=\text{Residual}
]

[
T=\text{Trace}
]

[
Cl=\text{Closure}.
]

ويكون الانتقال في كل طبقة:

[
x_n
\xrightarrow{\mathcal K_n}
x_{n+1}.
]

تتحقق الفراكتالية البنيوية فقط إذا وُجد تحويل تغيير مقياس

[
S_{n\to m}
]

بحيث تكون بنية الانتقال محافظة، أي:

[
\boxed{
S_{n\to m}\circ \mathcal K_n
\cong
\mathcal K_m\circ S_{n\to m}
}
]

بالنسبة إلى الحقول المحددة مسبقًا فقط:

[
{
\text{Carrier},
\text{Gate},
\text{Identity},
\text{Trace},
\text{Residual},
\text{Closure}
}
]

ولا يُشترط حفظ:

[
{
\text{frequency},
H,
\alpha,
\text{number of states},
\text{surface form},
\text{magnitude}
}
]

شرط الاختبار

يجب قبل تشغيل البيانات تحديد:

1. الطبقات التي ستُقارن.
2. الحامل في كل طبقة.
3. البوابة في كل طبقة.
4. معنى حفظ الهوية في كل طبقة.
5. تعريف البقية.
6. تعريف الإغلاق.
7. تحويل تغيير المقياس S.
8. معيار المطابقة بين البنيتين.
9. النموذج الأضعف المنافس.
10. شروط PASS / FAIL / UNDERPOWERED.

شرط النجاح

لا تنجح الفرضية لمجرد ظهور تشابه.

بل يجب أن يثبت:

[
\operatorname{StructureMatch}
(\mathcal K_n,\mathcal K_m)

«»

\operatorname{BestWeakerReconstruction}
]

على طبقتين على الأقل لم تُستخدما في صياغة الفرضية، ثم تُعاد النتيجة على طبقة ثالثة مستقلة.

شرط التفنيد

تُفنّد الفرضية إذا حدث واحد من الآتي:

[
\neg\text{IdentityPreservation}
]

أو

[
\neg\text{GateCorrespondence}
]

أو

[
\neg\text{ResidualCorrespondence}
]

أو

[
\neg\text{ClosureCorrespondence}
]

أو استطاع نموذج أضعف غير فراكتالي إعادة بناء النتائج:

[
\exists W:
\operatorname{Reconstruct}W
\ge
\operatorname{Reconstruct}{\mathcal K}.
]

قانون عدم القفز

لا يجوز أن يُعد التشابه بين طبقتين شاهدًا إذا استُخرجت بنية المقارنة بعد رؤية نتائج الطبقتين.

[
\boxed{
\text{PostHocSimilarity}
\neq
\text{FractalEvidence}
}
]

ولا يكون الشاهد مقبولًا إلا إذا كانت خريطة المطابقة ومعايير الفشل مسجلة قبل تشغيل الطبقة المختبرة.

الحكم الممكن

المخرجات الوحيدة المسموحة:

[
\texttt{SUPPORTED}
]

أو

[
\texttt{REFUTED}
]

أو

[
\texttt{UNDERPOWERED}
]

أو

[
\texttt{WEAKER_MODEL_RECONSTRUCTS}.
]

ولا يجوز للنظام إخراج:

[
\texttt{FRACTAL_LAW_PROVED}
]

من تجربة واحدة أو مدونة واحدة.

الادعاء المركزي

[
\boxed{
\text{الفراكتالية — إن وُجدت — تقع في قانون الانتقال والحفظ والإغلاق،
لا في تكرار الأشكال أو المقادير.}
}
]"""  # noqa: E501


REQUIRED_NOTATION_SITES: Final[tuple[str, ...]] = (
    r"\mathcal K=",
    r"C,G,O,I,E,R,T,Cl",
    r"x_n",
    r"\xrightarrow{\mathcal K_n}",
    r"S_{n\to m}",
    r"S_{n\to m}\circ \mathcal K_n",
    r"\cong",
    r"\mathcal K_m\circ S_{n\to m}",
    r"\boxed{",
    r"\neg\text{IdentityPreservation}",
    r"\neg\text{GateCorrespondence}",
    r"\neg\text{ResidualCorrespondence}",
    r"\neg\text{ClosureCorrespondence}",
    r"\operatorname{StructureMatch}",
    r"\operatorname{BestWeakerReconstruction}",
    r"\exists W:",
    r"\text{PostHocSimilarity}",
    r"\neq",
    r"\text{FractalEvidence}",
)


class FractalVerdict(Enum):
    """الأحكام الأربعة المسموحة بنصّ الفرضية؛ لا خامسَ لها ولا حكمَ وسيط."""

    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    UNDERPOWERED = "UNDERPOWERED"
    WEAKER_MODEL_RECONSTRUCTS = "WEAKER_MODEL_RECONSTRUCTS"


FORBIDDEN_VERDICT_NAME: Final[str] = "FRACTAL_LAW_PROVED"

COMPARED_FIELDS: Final[tuple[str, ...]] = (
    "Carrier",
    "Gate",
    "Identity",
    "Trace",
    "Residual",
    "Closure",
)

EXCLUDED_FIELDS: Final[tuple[str, ...]] = (
    "frequency",
    "H",
    "alpha",
    "number_of_states",
    "surface_form",
    "magnitude",
)

HYPOTHESIS_TEXT_IS_VERBATIM_NOTE: Final[str] = (
    "HypothesisTextIsVerbatim: النصُّ محفوظٌ بصيغته الواردة، ولم يُترجَم ولم "
    "يُعَد صوغُه نثرًا؛ والبصمةُ مُشتقّةٌ منه لا مكتوبةٌ بجانبه"
)

NOTATION_IS_PART_OF_THE_FROZEN_TEXT_NOTE: Final[str] = (
    "NotationIsPartOfTheFrozenText: مواضعُ الترميز الرياضي المُسمّاة في "
    "`REQUIRED_NOTATION_SITES` مفحوصةٌ عند الاستيراد؛ فسقوطُ موضعٍ منها يُسقط "
    "الوحدةَ ولا يمرّ بوصفه تنسيقًا"
)

FROZEN_AFTER_READOUT_IS_NOT_FROZEN_NOTE: Final[str] = (
    "FrozenAfterReadoutIsNotFrozen: تجميدُ نصٍّ بعد رؤية نتيجته ليس تجميدًا؛ "
    "وشاهدُ الترتيب في هذا المستودع أن هذه الوحدةَ ووحدةَ التسجيل تُودَعان قبل "
    "وجود أيّ وحدةِ قراءةٍ تقرأ منهما"
)

STRUCTURE_MATCH_IS_FIELD_RESTRICTED_NOTE: Final[str] = (
    "StructureMatchIsFieldRestricted: معيارُ المطابقة محصورٌ بالحقول الستّة "
    "المُسمّاة؛ ومن أدخل تواترًا أو إنتروبيا أو عددَ حالاتٍ أو مقدارًا فقد "
    "اختبر دعوى تشابُهِ مقاديرَ لم تدّعِها الفرضية"
)

FRACTAL_LAW_PROVED_IS_NOT_AN_OUTPUT_NOTE: Final[str] = (
    "FractalLawProvedIsNotAnOutput: لا مخرجَ بهذا الاسم من تجربةٍ واحدةٍ ولا "
    "من مدوّنةٍ واحدة؛ والمنعُ مفحوصٌ بالاسم عند الاستيراد لا موكولٌ إلى النيّة"
)

HYPOTHESIS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    HYPOTHESIS_TEXT_IS_VERBATIM_NOTE,
    NOTATION_IS_PART_OF_THE_FROZEN_TEXT_NOTE,
    FROZEN_AFTER_READOUT_IS_NOT_FROZEN_NOTE,
    STRUCTURE_MATCH_IS_FIELD_RESTRICTED_NOTE,
    FRACTAL_LAW_PROVED_IS_NOT_AN_OUTPUT_NOTE,
)


def hypothesis_digest(text: str = HYPOTHESIS_TEXT) -> str:
    """بصمةُ نصّ الفرضية، مُشتقّةً عند النداء لا منقولةً من ثابتٍ مكتوب."""

    return canonical_digest(
        canonical_bytes(
            {
                "canonicalization_version": "fractal-transition-hypothesis-v1",
                "hypothesis_text": text,
                "compared_fields": list(COMPARED_FIELDS),
                "excluded_fields": list(EXCLUDED_FIELDS),
                "verdicts": [member.value for member in FractalVerdict],
            }
        )
    )


HYPOTHESIS_DIGEST: Final[str] = hypothesis_digest()


def require_compared_field(name: str) -> str:
    """اقبل اسمَ حقلٍ داخلًا في معيار المطابقة، أو رُدَّه باسم سببه."""

    if not isinstance(name, str) or not name.strip():
        raise FractalTransitionHypothesisError("اسمُ الحقل نصٌّ غيرُ فارغ")
    if name in EXCLUDED_FIELDS:
        raise FractalTransitionHypothesisError(
            f"الحقل «{name}» مُستثنًى بنصّ الفرضية من شرط الحفظ، فلا يدخل في "
            f"معيار المطابقة: {STRUCTURE_MATCH_IS_FIELD_RESTRICTED_NOTE}"
        )
    if name not in COMPARED_FIELDS:
        raise FractalTransitionHypothesisError(
            f"الحقل «{name}» ليس واحدًا من الحقول الستّة المُقارَنة؛ وتوسيعُ "
            "المعيار بعد تجميده توسيعٌ للفرضية لا اختبارٌ لها"
        )
    return name


def _refuse_a_text_that_lost_its_notation() -> None:
    for site in REQUIRED_NOTATION_SITES:
        if site not in HYPOTHESIS_TEXT:
            raise FractalTransitionHypothesisError(
                f"سقط من النصّ المُجمَّد موضعُ ترميزٍ مُسمًّى: {site!r}؛ "
                f"{NOTATION_IS_PART_OF_THE_FROZEN_TEXT_NOTE}"
            )


def _refuse_a_fifth_verdict() -> None:
    if len(FractalVerdict) != 4:
        raise FractalTransitionHypothesisError(
            "الأحكامُ أربعةٌ مغلقة بنصّ الفرضية، ولا يُفتَح لها عضوٌ خامس"
        )
    names = {member.name for member in FractalVerdict}
    if names != {
        "SUPPORTED",
        "REFUTED",
        "UNDERPOWERED",
        "WEAKER_MODEL_RECONSTRUCTS",
    }:
        raise FractalTransitionHypothesisError("أسماءُ الأحكام هي المنصوصةُ بعينها")
    if FORBIDDEN_VERDICT_NAME in names:
        raise FractalTransitionHypothesisError(FRACTAL_LAW_PROVED_IS_NOT_AN_OUTPUT_NOTE)
    if FORBIDDEN_VERDICT_NAME in set(globals()) - {"FORBIDDEN_VERDICT_NAME"}:
        raise FractalTransitionHypothesisError(FRACTAL_LAW_PROVED_IS_NOT_AN_OUTPUT_NOTE)


def _refuse_a_field_vocabulary_that_overlaps() -> None:
    if len(COMPARED_FIELDS) != 6 or len(set(COMPARED_FIELDS)) != 6:
        raise FractalTransitionHypothesisError("الحقولُ المُقارَنةُ ستٌّ بلا تكرار")
    if len(EXCLUDED_FIELDS) != 6 or len(set(EXCLUDED_FIELDS)) != 6:
        raise FractalTransitionHypothesisError("الحقولُ المُستثناةُ ستٌّ بلا تكرار")
    if set(COMPARED_FIELDS) & set(EXCLUDED_FIELDS):
        raise FractalTransitionHypothesisError(
            "حقلٌ واحدٌ مُقارَنٌ ومُستثنًى معًا يجعل المعيارَ يقرأ الشيءَ ونقيضَه"
        )
    if len(HYPOTHESIS_DIGEST) != 64:
        raise FractalTransitionHypothesisError("بصمةُ النصّ سلسلةٌ ستّينيّةٌ رباعية")


_refuse_a_text_that_lost_its_notation()
_refuse_a_fifth_verdict()
_refuse_a_field_vocabulary_that_overlaps()
