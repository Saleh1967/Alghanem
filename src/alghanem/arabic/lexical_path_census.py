"""مسحُ «طريق النقل المعجميّ» في بطاقات الشجرة: جوابُ متغيّرٍ مرصودٍ لا فتحُ باب.

سُجِّلت جبهةٌ مفتوحةٌ في `qayd_marker_preregistration` بمتغيّرٍ واحدٍ بعينه:
«أهو طريقٌ ثالثٌ يُقرأ في نفسه أم تابعٌ لطريق نقل القيد؟»، ومُنِع العملُ فيها
حتى تُغلَق تجربةُ «سائمة الغنم» بنتيجةٍ واحدةٍ كاملة. وقد أُغلِقت في
`level_two_source_texts` بنتيجةٍ سالبةٍ تامّة، فارتفع المانعُ التسلسليُّ
(`NoRicherStructureBeforeLowerOpenResidualClosure`) وصار فتحُ هذه الجبهة مأذونًا.

**والجبهةُ تُفتَح بجواب متغيّرها لا بتوسيع مفردة**: لم يُزَد عضوٌ في
`LexicalCitationStructure`، ولم يُمسَّ `qayd_marker_preregistration` بحرف — فمن
أجاب سؤالًا بتحرير موضعِ تسجيلِه أزال السؤالَ ولم يُجِبه.

**والجوابُ يُشتَقّ من البطاقات نفسها**: تُقرأ بطاقاتُ `examples/` من الشجرة عند
النداء، ويُجمَع منها ما يُصرِّح بمفتاح `طريق_النقل_المعجمي` المستورَد من
`lexical_transmission`، ويُقابَل بمفتاح `نسبة_التركيب` المستورَد من
`level_two_manat` — **استيرادًا لا نسخًا**، فمفتاحٌ مكتوبٌ مرّتين يُغيَّر في موضعٍ
ويبقى في الآخر.

**والحاسمُ نقيضةٌ واحدةٌ لا أكثريّة** (`OneCounterInstanceDecidesADependencyClaim`):
دعوى التبعيّة تقول إنّ الطريق المعجميّ لا يُعلَن إلا حيث يُعلَن طريقُ نقل القيد،
وهي دعوى كلّيّة يُبطلها مثالٌ مضادٌّ واحد. فالاشتقاقُ هنا يقع على **وجود** بطاقةٍ
تُعلن الطريقَ المعجميَّ بلا نسبةِ تركيب، لا على نسبة البطاقات؛ ولو كانت النسبةُ
خمسةً إلى واحدٍ أو واحدًا إلى خمسة لما تغيّر المُشتَقّ. ومن جعل العددَ حجّةً
جعل الجوابَ رهنًا بما يُضاف غدًا من بطاقات.

**والإعلانُ ليس سلوكًا** (`DeclaringAPathIsNotWalkingIt`): أربعٌ من الستّ تُصرِّح
بالمفتاح بتعدادِ إسناداتٍ **خالٍ**. فالمُشتَقُّ هنا أنّ الطريق يُعلَن مستقلًّا عن
طريق القيد، لا أنّه مسلوكٌ فيها؛ وقوّةُ ما فيها من إسنادٍ تُقرأ من
`lexical_transmission` وعتبتِه `LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS`، ولا تُقرأ
من هذا المسح بحال. ولذلك لا يُخرِج هذا المسحُ بنيةَ استشهادٍ ولا درجةَ نقلٍ ولا
يمسّ اشتقاقهما.

**واتّحادُ الشكل ليس اتّحادَ الحكم** (`SchemaIdentityIsNotSemanticIndependence`):
البطاقاتُ الستُّ تتّفق في مفاتيحها الثلاثة (`المصدر`/`المادة`/`الإسنادات`)، وهذا
شاهدٌ على أنّ الحقلَ ذو صورةٍ واحدةٍ حيثما وقع، لا برهانٌ على أنّ ما يُقرأ منه
مستقلٌّ في المعنى. ويُسجَّل الشاهدُ بحدّه.

**وستُّ بطاقاتٍ في هذه الشجرة ليست دعوى في البطاقات عمومًا**
(`ThisTreeIsNotTheWorld`، على نصّ `ExhaustedSourceIsNotAnExhaustedWorld`): مسحٌ
تامٌّ على `examples/` تامٌّ عليها وحدها.

**وهذه الوحدة تسجيلٌ لا سلطة**: لا ولادة، ولا حكمَ ولادة، ولا تجميد، ولا `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Any, Final

from .level_two_manat import CARD_COMPOSITION_RELATION_KEY
from .lexical_transmission import CARD_LEXICAL_PATH_KEY
from .pipeline_stations import repository_root_path

__all__ = [
    "CARDS_RELATIVE_PATH",
    "DECLARING_A_PATH_IS_NOT_WALKING_IT_NOTE",
    "LEXICAL_PATH_CENSUS_IS_NOT_A_GATE_NOTE",
    "NAMED_RESIDUALS",
    "ONE_COUNTER_INSTANCE_DECIDES_NOTE",
    "SCHEMA_IDENTITY_IS_NOT_SEMANTIC_INDEPENDENCE_NOTE",
    "THIS_TREE_IS_NOT_THE_WORLD_NOTE",
    "CardLexicalPathReading",
    "LexicalPathCensus",
    "LexicalPathCensusError",
    "LexicalPathStanding",
    "QaydCoOccurrence",
    "derive_lexical_path_standing",
    "read_lexical_path_census",
]


class LexicalPathCensusError(ValueError):
    """رفضٌ صريحٌ في مسح الطريق المعجميّ؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


CARDS_RELATIVE_PATH: Final[str] = "examples"


class QaydCoOccurrence(Enum):
    """أتُعلِن البطاقةُ مع طريقها المعجميِّ نسبةَ تركيبٍ أم لا؟ ثنائيةٌ مغلقة."""

    مع_نسبة_تركيب = "مع_نسبة_تركيب"
    بلا_نسبة_تركيب = "بلا_نسبة_تركيب"


class LexicalPathStanding(Enum):
    """جوابُ المتغيّر المرصود؛ ثلاثيةٌ مغلقة، وثالثتُها ليست ترجيحًا.

    و`غير_محسوم` عضوٌ مقصود: شجرةٌ لا تُعلن فيها بطاقةٌ واحدةٌ طريقًا معجميًّا لا
    تُنتج جوابًا في أيّ من الطرفين، وقراءةُ خلوّها تبعيّةً قراءةُ عدمِ الشاهد
    شاهدًا على العدم.
    """

    يقرأ_في_نفسه = "يقرأ_في_نفسه"
    تابع_لطريق_نقل_القيد = "تابع_لطريق_نقل_القيد"
    غير_محسوم = "غير_محسوم"


for _vocabulary, _size, _reason in (
    (
        QaydCoOccurrence,
        2,
        "a card either declares a composition relation or it does not",
    ),
    (LexicalPathStanding, 3, "an empty tree answers neither side of the variable"),
):
    if len(_vocabulary) != _size:  # pragma: no cover - guard
        raise RuntimeError(_reason)


ONE_COUNTER_INSTANCE_DECIDES_NOTE: Final[str] = (
    "OneCounterInstanceDecidesADependencyClaim: دعوى التبعيّة كلّيّةٌ — «لا "
    "يُعلَن الطريقُ المعجميُّ إلا مع طريق نقل القيد» — ويُبطلها مثالٌ مضادٌّ "
    "واحد. فالاشتقاقُ على وجود النقيضة لا على نسبتها، ولو انقلبت النسبةُ لما "
    "تغيّر المُشتَقّ؛ ومن احتجّ بالعدد جعل الجوابَ رهنًا بما يُضاف غدًا"
)

DECLARING_A_PATH_IS_NOT_WALKING_IT_NOTE: Final[str] = (
    "DeclaringAPathIsNotWalkingIt: إعلانُ المفتاح بتعدادِ إسناداتٍ خالٍ يُثبت "
    "أنّ الحقلَ مُعلَنٌ لا أنّ الطريقَ مسلوك؛ فالمُشتَقُّ هنا استقلالُ الإعلان "
    "عن طريق القيد، وقوّةُ الإسناد تُقرأ في `lexical_transmission` وعتبتِه لا "
    "في هذا المسح"
)

SCHEMA_IDENTITY_IS_NOT_SEMANTIC_INDEPENDENCE_NOTE: Final[str] = (
    "SchemaIdentityIsNotSemanticIndependence: اتّفاقُ البطاقات في مفاتيحها "
    "شاهدٌ على وحدة الصورة حيثما وقع الحقل، لا برهانٌ على استقلال ما يُقرأ منه "
    "في المعنى؛ فيُسجَّل الشاهدُ بحدّه ولا يُحمَّل ما ليس فيه"
)

THIS_TREE_IS_NOT_THE_WORLD_NOTE: Final[str] = (
    "ThisTreeIsNotTheWorld: المسحُ تامٌّ على بطاقات `examples/` في هذه الشجرة، "
    "وتمامُه عليها ليس تمامًا على البطاقات عمومًا ولا على ما يُكتَب منها بعدُ؛ "
    "وهو عينُ حدِّ `ExhaustedSourceIsNotAnExhaustedWorld` مطبَّقًا على شجرةٍ "
    "بدل كتاب"
)

LEXICAL_PATH_CENSUS_IS_NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا تُصدر هذه الوحدة ولادةً ولا حكمَ ولادة ولا تجميدًا ولا "
    "`E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه"
)


NAMED_RESIDUALS: Final[dict[str, str]] = {
    "DECLARING_A_PATH_IS_NOT_WALKING_IT": DECLARING_A_PATH_IS_NOT_WALKING_IT_NOTE,
    "SCHEMA_IDENTITY_IS_NOT_SEMANTIC_INDEPENDENCE": (
        SCHEMA_IDENTITY_IS_NOT_SEMANTIC_INDEPENDENCE_NOTE
    ),
    "THIS_TREE_IS_NOT_THE_WORLD": THIS_TREE_IS_NOT_THE_WORLD_NOTE,
    "CO_OCCURRENCE_IS_NOT_THE_ONLY_SHAPE_OF_DEPENDENCE": (
        "التبعيّةُ المفحوصةُ هنا تبعيّةُ **إعلان**: أيُعلَن هذا الحقلُ إلا مع "
        "ذاك؟ وقد تكون تبعيّةٌ أخرى في جهة المحتوى — أن يُقرأ المعجميُّ لأجل "
        "القيد وإن أُعلِن وحده — ولا يفحصها هذا المسح ولا ينفيها، فإبطالُ "
        "صورةٍ من التبعيّة ليس إبطالًا لكلّ صورها"
    ),
    "CARD_CORPUS_IS_NOT_FROZEN_BY_THIS_MODULE": (
        "لا تُجمَّد هنا قائمةُ بطاقاتٍ ولا تُكتَب أسماؤها في جدول: تُقرأ الشجرةُ "
        "عند كلّ نداء، فيصدق المسحُ مع الشجرة ويكذب معها ولا ينفصل عنها — على "
        "منوال `COVERAGE_IS_READ_FROM_THE_TREE_NOTE`. ولازمُه أنّ هذا المُخرَج "
        "ليس شهادةً مُجمَّدةً يُحتَجّ بها بعد تغيُّر البطاقات"
    ),
    "NO_CITATION_STRUCTURE_IS_DERIVED_HERE": (
        "لا يُخرِج هذا المسحُ `LexicalCitationStructure` ولا درجةَ نقلٍ ولا "
        "يمسّ اشتقاقهما، ولم يُزَد عضوٌ في مفردةٍ قائمة؛ فجوابُ متغيّرٍ مرصودٍ "
        "شيءٌ وبناءُ أداةِ حكمٍ على الطريق شيءٌ آخر لم يقع"
    ),
}


@dataclass(frozen=True, slots=True)
class CardLexicalPathReading:
    """قراءةُ بطاقةٍ واحدةٍ تُعلن الطريقَ المعجميّ؛ ولا حقلَ حكمٍ فيها."""

    card_relative_path: str
    declared_keys: tuple[str, ...]
    attributions_declared: tuple[str, ...]
    qayd_co_occurrence: QaydCoOccurrence

    def __post_init__(self) -> None:
        if not self.card_relative_path.strip():
            raise LexicalPathCensusError("موضعُ البطاقة مُسمًّى لا فارغ.")
        if not isinstance(self.qayd_co_occurrence, QaydCoOccurrence):
            raise LexicalPathCensusError("اقترانُ نسبة التركيب عضوٌ في مفردته.")
        for name in self.declared_keys:
            if not isinstance(name, str) or not name.strip():
                raise LexicalPathCensusError("مفاتيحُ الحقل أسماءٌ غيرُ فارغة.")

    @property
    def path_is_declared_empty(self) -> bool:
        """أمُعلَنٌ الطريقُ بتعدادِ إسناداتٍ خالٍ؟ مُشتَقٌّ من التعداد نفسه."""

        return not self.attributions_declared


def derive_lexical_path_standing(
    readings: tuple[CardLexicalPathReading, ...],
) -> LexicalPathStanding:
    """اشتقّ جوابَ المتغيّر من وجود نقيضةٍ واحدة، لا من نسبةٍ ولا من عدد.

    فبطاقةٌ واحدةٌ تُعلن الطريقَ المعجميَّ بلا نسبةِ تركيبٍ تُبطل دعوى التبعيّة
    في الإعلان؛ وإن لم توجد بطاقةٌ تُعلنه أصلًا فالمتغيّرُ `غير_محسوم` ولا
    يُحمَل خلوُّ الشجرة على أحد الطرفين.
    """

    if not isinstance(readings, tuple):
        raise LexicalPathCensusError("المسحُ يقع على تعدادٍ مُجمَّد.")
    for reading in readings:
        if not isinstance(reading, CardLexicalPathReading):
            raise LexicalPathCensusError("كلُّ عنصرٍ قراءةُ بطاقةٍ مُصاغة.")
    if not readings:
        return LexicalPathStanding.غير_محسوم
    for reading in readings:
        if reading.qayd_co_occurrence is QaydCoOccurrence.بلا_نسبة_تركيب:
            return LexicalPathStanding.يقرأ_في_نفسه
    return LexicalPathStanding.تابع_لطريق_نقل_القيد


@dataclass(frozen=True, slots=True)
class LexicalPathCensus:
    """مسحُ البطاقات المُعلِنة للطريق المعجميّ؛ والجوابُ مُشتَقٌّ لا مكتوب."""

    readings: tuple[CardLexicalPathReading, ...]

    def __post_init__(self) -> None:
        seen: list[str] = []
        for reading in self.readings:
            if not isinstance(reading, CardLexicalPathReading):
                raise LexicalPathCensusError("كلُّ عنصرٍ قراءةُ بطاقةٍ مُصاغة.")
            if reading.card_relative_path in seen:
                raise LexicalPathCensusError(
                    f"بطاقةٌ مكرّرة في المسح: {reading.card_relative_path}."
                )
            seen.append(reading.card_relative_path)

    @property
    def standing(self) -> LexicalPathStanding:
        """جوابُ المتغيّر، مُشتقًّا من القراءات لا مكتوبًا في حقل."""

        return derive_lexical_path_standing(self.readings)

    @property
    def counter_instances(self) -> tuple[str, ...]:
        """البطاقاتُ المُبطِلة لدعوى التبعيّة، مُسمّاةً لا معدودةً فقط."""

        return tuple(
            reading.card_relative_path
            for reading in self.readings
            if reading.qayd_co_occurrence is QaydCoOccurrence.بلا_نسبة_تركيب
        )

    @property
    def declared_but_empty(self) -> tuple[str, ...]:
        """البطاقاتُ المُعلِنةُ للطريق بتعدادٍ خالٍ؛ إعلانٌ لا سلوك."""

        return tuple(
            reading.card_relative_path
            for reading in self.readings
            if reading.path_is_declared_empty
        )

    @property
    def declared_key_shapes(self) -> tuple[tuple[str, ...], ...]:
        """صورُ المفاتيح المُعلَنة، بلا تكرار؛ وحدتُها شاهدُ صورةٍ لا حكم."""

        shapes: list[tuple[str, ...]] = []
        for reading in self.readings:
            if reading.declared_keys not in shapes:
                shapes.append(reading.declared_keys)
        return tuple(shapes)


def _lexical_path_value(node: Any) -> Any:
    """اعثر على قيمة المفتاح المعجميِّ في أيّ عمقٍ من البطاقة، أو `None`."""

    if isinstance(node, dict):
        if CARD_LEXICAL_PATH_KEY in node:
            return node[CARD_LEXICAL_PATH_KEY]
        for value in node.values():
            found = _lexical_path_value(value)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _lexical_path_value(value)
            if found is not None:
                return found
    return None


def _declares_composition_relation(node: Any) -> bool:
    if isinstance(node, dict):
        if CARD_COMPOSITION_RELATION_KEY in node:
            return True
        return any(_declares_composition_relation(v) for v in node.values())
    if isinstance(node, list):
        return any(_declares_composition_relation(v) for v in node)
    return False


def read_lexical_path_census(root: Path | None = None) -> LexicalPathCensus:
    """امسح بطاقاتِ الشجرة، مُشتقًّا كلَّ قراءةٍ من البطاقة نفسها عند النداء."""

    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise LexicalPathCensusError("جذرُ المستودع مسار.")
    cards_root = base / CARDS_RELATIVE_PATH
    if not cards_root.is_dir():
        raise LexicalPathCensusError(
            f"موضعُ البطاقات غير موجودٍ عند {cards_root}: شجرةٌ غائبةٌ تُقرأ «لا "
            "بطاقات» وهو ادّعاءٌ لم تُقرأ الشجرة لأجله."
        )
    readings: list[CardLexicalPathReading] = []
    for path in sorted(cards_root.rglob("*.yaml")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:  # pragma: no cover - guard
            raise LexicalPathCensusError(
                f"{path.name}: بطاقةٌ لم تُقرأ، ولا تُتخطّى صامتةً — بطاقةٌ "
                f"متعذّرةُ القراءة تُنقِص المسحَ وهو يُقرأ تامًّا: {error}"
            ) from error
        if not isinstance(document, dict):
            raise LexicalPathCensusError(
                f"{path.name}: البطاقةُ كائنٌ بمفاتيح، ولا يُتخطّى ما ليس كذلك صامتًا."
            )
        declared = _lexical_path_value(document)
        if declared is None:
            continue
        if not isinstance(declared, dict):
            raise LexicalPathCensusError(
                f"{path.name}: {CARD_LEXICAL_PATH_KEY} كائنٌ لا نصّ."
            )
        attributions = declared.get("الإسنادات", [])
        if not isinstance(attributions, list):
            raise LexicalPathCensusError(f"{path.name}: الإسنادات تعدادٌ لا نصّ.")
        readings.append(
            CardLexicalPathReading(
                card_relative_path=path.relative_to(base).as_posix(),
                declared_keys=tuple(sorted(declared)),
                attributions_declared=tuple(
                    str(item.get("السلطة", "")) if isinstance(item, dict) else str(item)
                    for item in attributions
                ),
                qayd_co_occurrence=(
                    QaydCoOccurrence.مع_نسبة_تركيب
                    if _declares_composition_relation(document)
                    else QaydCoOccurrence.بلا_نسبة_تركيب
                ),
            )
        )
    return LexicalPathCensus(readings=tuple(readings))


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "standing",
    "answer",
    "result",
    "verdict",
    "count",
    "total",
    "birth",
    "freeze",
)


def _assert_no_written_answer_field() -> None:
    """احرسْ خلوَّ القراءة والمسح من حقلِ جوابٍ مكتوب.

    الجوابُ يُشتَقّ من القراءات؛ فحقلٌ يحمله يُخالَف به المُشتَقُّ عند اختلافهما.
    """

    for declaring_type in (CardLexicalPathReading, LexicalPathCensus):
        for field in fields(declaring_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise RuntimeError(
                        f"{declaring_type.__name__}.{field.name} حقلٌ ممنوع: "
                        "الجوابُ مُشتَقٌّ لا مكتوب."
                    )


_assert_no_written_answer_field()
