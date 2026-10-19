"""قياسُ ضرورةِ البنية الصرفية: هل يميّز مجالٌ صوريٌّ قائمٌ أطرافَ التصادم؟

هذه وحدةُ **القياس** وحدها. هدفُ التمييز ومخروطُ المجالات مُجمَّدان قبلها في
`morphological_necessity_probe`، ولا يُقرأ هنا إلا ما جُمِّد هناك: لا يُزاد زوجٌ،
ولا يُنقَص مجالٌ، ولا يُعادُ ترتيب.

`MeasurementReadsAFrozenTarget`: تُستورَد الأزواجُ والمخروطُ استيرادًا من وحدة
التجميد، وتُتحقَّق بصمتُهما عند الاستيراد. فقياسٌ يختار هدفَه أثناءه ليس قياسًا.

`ApplicationIsAttemptedNotAsserted`: لا يُكتَب في هذه الوحدة أنّ مجالًا «لا مدخل
له»؛ بل يُنادى المجالُ فعلًا بقارئه المُصرَّح على الشكل السطحيّ، وتُسجَّل رسالةُ
ردِّه بنصّها كما نطق بها هو. فالردُّ المرصودُ حجّة، والردُّ المُخبَرُ عنه دعوى.

`RefusalIsNotFailureToDiscriminate`: مجالٌ ردَّ المدخلَ لأنّ الشكل السطحيّ ليس
من مفرداته **لم يفشل في التمييز**؛ إنّما تعذّر عليه القياس. الخلطُ بين الغياب
والتعذّر هو البابُ الوحيد الذي تُصنَع منه «ضرورةٌ» زائفة، فسُدَّ بمفردةٍ مستقلّة
(`لا_مدخل_للشكل_السطحي`) لا تُجمَع أبدًا مع (`يسوي_الطرفين`).

`CoverageBeforeJudgement`: لا تُشتَقّ منزلةُ زوجٍ إلا بعد تغطيةٍ تامّةٍ لمخروط
المجالات الأربعة، بلا تكرارٍ ولا مجالٍ أجنبيّ. فحكمٌ على ثلاثةِ مجالاتٍ من أربعة
حكمٌ على غير ما أُعلِن.

`ExhaustiveMeasurementIsTheOnlyGateToTheNegative`: لا تُقال
(`لا_يميزه_مجال_قائم_بعد_قياس_تام`) إلا إذا طُبِّق كلُّ مجالٍ فعلًا وسوّى
الطرفين. فإن تعذّر مجالٌ واحد، فالمنزلة (`غير_محسوم_لتعذّر_القياس`) لا غير.

`MeasuredNegativeIsNotAConstitutionalNecessity`: أقصى ما تبلغه هذه الوحدة
نفيٌ مقيس. أمّا أنّ ذلك يوجب فتحَ مجالٍ صوريٍّ جديدٍ للجذر والمصدر، فحكمٌ
دستوريٌّ لا تملكه طبقةُ `arabic/`، ولا يخرج من هذا الملفّ، ولا يُشتَقّ آليًّا
من مُخرَجه. `docs/CONSTITUTION.md` تُثبت الضرورة بتصادمِ إسقاطٍ نسبةً إلى هدفِ
تمييزٍ مُعلَن، وتنفي صراحةً الأدنويّةَ الدلاليّة.

`ThisIsRegistrationNotAuthority`: لا ولادةَ هنا، ولا تجميدَ حكمٍ، ولا بوّابة.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .kulli_juzi_formal import (
    canonical_sub_outcome,
    canonical_sub_partition,
    canonical_universality,
)
from .lafz_madlul_relation_formal import (
    canonical_intended_meaning,
    canonical_relation_answer,
    canonical_relation_count,
)
from .madlul_alone_formal import (
    canonical_signified_composition,
    canonical_signified_kind,
    canonical_signified_usage_state,
)
from .morphological_necessity_probe import (
    DISCRIMINATION_TARGET_DIGEST,
    FROZEN_DISCRIMINATION_TARGET,
    PRE_REGISTERED_EXPECTATION,
    DiscriminationPair,
    WeakerDomainReference,
    discrimination_target_digest,
    read_weaker_domain_cone,
)
from .pipeline_stations import ARABIC_PACKAGE_RELATIVE_PATH
from .word_class_formal import canonical_answer

MEASUREMENT_READS_A_FROZEN_TARGET_NOTE: Final[str] = (
    "تُستورَد الأزواجُ والمخروطُ من وحدة التجميد وتُتحقَّق بصمتُهما عند الاستيراد؛ "
    "فقياسٌ يختار هدفَه أثناءه ليس قياسًا."
)

APPLICATION_IS_ATTEMPTED_NOT_ASSERTED_NOTE: Final[str] = (
    "لا يُكتَب هنا أنّ مجالًا لا مدخل له؛ بل يُنادى بقارئه المُصرَّح فعلًا على الشكل "
    "السطحيّ وتُسجَّل رسالةُ ردِّه بنصّها. فالردُّ المرصودُ حجّة، والمُخبَرُ عنه دعوى."
)

REFUSAL_IS_NOT_FAILURE_TO_DISCRIMINATE_NOTE: Final[str] = (
    "مجالٌ ردَّ المدخلَ لأنّ الشكل السطحيّ ليس من مفرداته لم يفشل في التمييز، بل تعذّر "
    "عليه القياس؛ والخلطُ بين الغياب والتعذّر هو البابُ الذي تُصنَع منه ضرورةٌ زائفة."
)

COVERAGE_BEFORE_JUDGEMENT_NOTE: Final[str] = (
    "لا تُشتَقّ منزلةُ زوجٍ إلا بعد تغطيةٍ تامّةٍ للمخروط بلا تكرارٍ ولا مجالٍ أجنبيّ؛ "
    "فحكمٌ على ثلاثةِ مجالاتٍ من أربعة حكمٌ على غير ما أُعلِن."
)

EXHAUSTIVE_MEASUREMENT_IS_THE_ONLY_GATE_TO_THE_NEGATIVE_NOTE: Final[str] = (
    "لا يُقال (لا_يميزه_مجال_قائم_بعد_قياس_تام) إلا إذا طُبِّق كلُّ مجالٍ فعلًا وسوّى "
    "الطرفين؛ فإن تعذّر مجالٌ واحد فالمنزلة (غير_محسوم_لتعذّر_القياس) لا غير."
)

MEASURED_NEGATIVE_IS_NOT_A_CONSTITUTIONAL_NECESSITY_NOTE: Final[str] = (
    "أقصى ما تبلغه هذه الوحدة نفيٌ مقيس؛ أمّا إيجابُ فتحِ مجالٍ صوريٍّ للجذر والمصدر "
    "فحكمٌ دستوريٌّ لا تملكه طبقةُ arabic/ ولا يُشتَقّ آليًّا من مُخرَج هذا الملفّ."
)

SURFACE_FORM_IS_NOT_A_LEXEME_NOTE: Final[str] = (
    "القوارئُ المُصرَّحة في المجالات الأربعة تُحوِّل **مفرداتِ جوابٍ مُعلَنة** إلى أعضاء "
    "تعداد، لا تُحلِّل ألفاظَ اللغة؛ فمناداتُها على شكلٍ سطحيٍّ قياسٌ لحدِّ المجال نفسه."
)

READERS_ARE_THE_DOMAINS_OWN_DOORS_NOTE: Final[str] = (
    "لم يُصطَنَع للمجالات مدخلٌ جديد لأجل هذا القياس؛ بل نوديت قوارئُها القائمة كما هي، "
    "إذ اصطناعُ مدخلٍ يقيس ما بنيناه نحن لا ما في الشجرة."
)

NAMED_RESIDUALS: Final[dict[str, str]] = {
    "MEASUREMENT_READS_A_FROZEN_TARGET": MEASUREMENT_READS_A_FROZEN_TARGET_NOTE,
    "APPLICATION_IS_ATTEMPTED_NOT_ASSERTED": APPLICATION_IS_ATTEMPTED_NOT_ASSERTED_NOTE,
    "REFUSAL_IS_NOT_FAILURE_TO_DISCRIMINATE": (
        REFUSAL_IS_NOT_FAILURE_TO_DISCRIMINATE_NOTE
    ),
    "COVERAGE_BEFORE_JUDGEMENT": COVERAGE_BEFORE_JUDGEMENT_NOTE,
    "EXHAUSTIVE_MEASUREMENT_IS_THE_ONLY_GATE_TO_THE_NEGATIVE": (
        EXHAUSTIVE_MEASUREMENT_IS_THE_ONLY_GATE_TO_THE_NEGATIVE_NOTE
    ),
    "MEASURED_NEGATIVE_IS_NOT_A_CONSTITUTIONAL_NECESSITY": (
        MEASURED_NEGATIVE_IS_NOT_A_CONSTITUTIONAL_NECESSITY_NOTE
    ),
    "SURFACE_FORM_IS_NOT_A_LEXEME": SURFACE_FORM_IS_NOT_A_LEXEME_NOTE,
    "READERS_ARE_THE_DOMAINS_OWN_DOORS": READERS_ARE_THE_DOMAINS_OWN_DOORS_NOTE,
}


class MorphologicalNecessityMeasurementError(ValueError):
    """خطأُ قياسِ ضرورةِ البنية الصرفية."""


class DomainApplication(Enum):
    """حصيلةُ تطبيقِ مجالٍ واحدٍ على زوجٍ واحد: ثلاثُ حالاتٍ لا رابع لها."""

    DISTINGUISHES = "يميز_الطرفين"
    EQUATES = "يسوي_الطرفين"
    NO_ENTRY_FOR_SURFACE_FORM = "لا_مدخل_للشكل_السطحي"


if len(DomainApplication) != 3:  # pragma: no cover - guard
    raise RuntimeError("حصيلةُ التطبيق ثلاثُ حالاتٍ بالضبط؛ وتوسيعُها يخلط التعذّرَ بالتسوية")


class PairStanding(Enum):
    """منزلةُ زوجٍ بعد تطبيق المخروط كلِّه: ثلاثُ منازلَ لا رابع لها."""

    DISTINGUISHED_BY_STANDING_DOMAIN = "يميزه_مجال_قائم"
    UNDISTINGUISHED_AFTER_EXHAUSTIVE_MEASUREMENT = "لا_يميزه_مجال_قائم_بعد_قياس_تام"
    UNRESOLVED_MEASUREMENT_IMPOSSIBLE = "غير_محسوم_لتعذّر_القياس"


if len(PairStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError("منازلُ الزوج ثلاثٌ بالضبط؛ ورابعةٌ تُدخِل حكمًا لم يُقَس")


_DomainReader = Callable[[str], Enum]

_READERS_BY_MODULE: Final[dict[str, tuple[tuple[str, _DomainReader], ...]]] = {
    ARABIC_PACKAGE_RELATIVE_PATH + "/word_class_formal.py": (
        ("canonical_answer", canonical_answer),
    ),
    ARABIC_PACKAGE_RELATIVE_PATH + "/kulli_juzi_formal.py": (
        ("canonical_universality", canonical_universality),
        ("canonical_sub_partition", canonical_sub_partition),
        ("canonical_sub_outcome", canonical_sub_outcome),
    ),
    ARABIC_PACKAGE_RELATIVE_PATH + "/lafz_madlul_relation_formal.py": (
        ("canonical_relation_count", canonical_relation_count),
        ("canonical_relation_answer", canonical_relation_answer),
        ("canonical_intended_meaning", canonical_intended_meaning),
    ),
    ARABIC_PACKAGE_RELATIVE_PATH + "/madlul_alone_formal.py": (
        ("canonical_signified_kind", canonical_signified_kind),
        ("canonical_signified_composition", canonical_signified_composition),
        ("canonical_signified_usage_state", canonical_signified_usage_state),
    ),
}


@dataclass(frozen=True)
class ReaderAttempt:
    """محاولةٌ واحدةٌ مرصودة: قارئٌ نودي على شكلٍ سطحيّ، فقبِل أو ردّ بنصّه."""

    reader_name: str
    surface: str
    accepted: bool
    accepted_member: str | None
    refusal_message: str | None

    def __post_init__(self) -> None:
        if not self.reader_name.strip() or not self.surface.strip():
            raise MorphologicalNecessityMeasurementError(
                "اسمُ القارئ والشكلُ السطحيّ نصّان غير فارغين."
            )
        if self.accepted and self.accepted_member is None:
            raise MorphologicalNecessityMeasurementError(
                "قبولٌ بلا عضوٍ مُسمّى ليس قبولًا مرصودًا."
            )
        if not self.accepted and not (self.refusal_message or "").strip():
            raise MorphologicalNecessityMeasurementError(
                "ردٌّ بلا رسالةِ المجال نفسه دعوى لا رصد."
            )
        if self.accepted and self.refusal_message is not None:
            raise MorphologicalNecessityMeasurementError("لا تجتمع رسالةُ ردٍّ مع قبول.")


@dataclass(frozen=True)
class DomainApplicationRow:
    """سطرُ (زوج × مجال): محاولاتُه المرصودة، وحصيلتُه مُشتقّةً منها لا مكتوبة."""

    pair: DiscriminationPair
    module_relative_path: str
    attempts: tuple[ReaderAttempt, ...]

    def __post_init__(self) -> None:
        if not self.attempts:
            raise MorphologicalNecessityMeasurementError(
                "سطرٌ بلا محاولةٍ واحدةٍ مرصودة ليس قياسًا."
            )

    @property
    def accepting_readers(self) -> tuple[str, ...]:
        """القوارئُ التي قبِلت الطرفين معًا؛ وهي وحدها التي يصحّ بها تمييز."""

        names: list[str] = []
        for reader_name, _ in _READERS_BY_MODULE[self.module_relative_path]:
            for_reader = [a for a in self.attempts if a.reader_name == reader_name]
            if len(for_reader) == 2 and all(a.accepted for a in for_reader):
                names.append(reader_name)
        return tuple(names)

    @property
    def application(self) -> DomainApplication:
        """حصيلةُ التطبيق مُشتقّةً من المحاولات المرصودة وحدها."""

        for reader_name in self.accepting_readers:
            members = {
                attempt.accepted_member
                for attempt in self.attempts
                if attempt.reader_name == reader_name
            }
            if len(members) == 2:
                return DomainApplication.DISTINGUISHES
        if self.accepting_readers:
            return DomainApplication.EQUATES
        return DomainApplication.NO_ENTRY_FOR_SURFACE_FORM

    @property
    def refusal_messages(self) -> tuple[str, ...]:
        """رسائلُ ردِّ المجال بنصّها كما نطق بها هو، لا كما لخّصناها."""

        return tuple(
            attempt.refusal_message
            for attempt in self.attempts
            if attempt.refusal_message is not None
        )


def apply_domain_to_pair(
    pair: DiscriminationPair, reference: WeakerDomainReference
) -> DomainApplicationRow:
    """طبِّق مجالًا قائمًا على زوجٍ مُجمَّدٍ فعلًا، وسجِّل ما وقع لا ما يُتوقَّع."""

    readers = _READERS_BY_MODULE.get(reference.module_relative_path)
    if readers is None:
        raise MorphologicalNecessityMeasurementError(
            f"لا قارئَ مُصرَّحًا مُسجَّلًا للمجال {reference.module_relative_path}؛ "
            "ولا يُصطَنَع له مدخلٌ لأجل هذا القياس."
        )
    attempts: list[ReaderAttempt] = []
    for reader_name, reader in readers:
        for surface in (pair.surface_a, pair.surface_b):
            try:
                member = reader(surface)
            except ValueError as refusal:
                attempts.append(
                    ReaderAttempt(
                        reader_name=reader_name,
                        surface=surface,
                        accepted=False,
                        accepted_member=None,
                        refusal_message=str(refusal),
                    )
                )
            else:
                attempts.append(
                    ReaderAttempt(
                        reader_name=reader_name,
                        surface=surface,
                        accepted=True,
                        accepted_member=member.value,
                        refusal_message=None,
                    )
                )
    return DomainApplicationRow(
        pair=pair,
        module_relative_path=reference.module_relative_path,
        attempts=tuple(attempts),
    )


@dataclass(frozen=True)
class PairMeasurement:
    """قياسُ زوجٍ واحدٍ عبر المخروط كلِّه؛ منزلتُه مُشتقّةٌ لا مكتوبة."""

    pair: DiscriminationPair
    rows: tuple[DomainApplicationRow, ...]
    covered_cone: tuple[str, ...]

    def __post_init__(self) -> None:
        measured = tuple(row.module_relative_path for row in self.rows)
        if len(set(measured)) != len(measured):
            raise MorphologicalNecessityMeasurementError(
                "تكرارُ مجالٍ في القياس يُضاعِف شاهدًا واحدًا."
            )
        if set(measured) != set(self.covered_cone):
            raise MorphologicalNecessityMeasurementError(
                "تغطيةُ المخروط ليست تامّة: "
                f"المقيسة {sorted(measured)} والمُعلَنة {sorted(self.covered_cone)}؛ "
                + COVERAGE_BEFORE_JUDGEMENT_NOTE
            )

    @property
    def standing(self) -> PairStanding:
        """منزلةُ الزوج بالأسبقية المُعلَنة: تمييزٌ ثمّ تعذّرٌ ثمّ نفيٌ مقيس."""

        applications = tuple(row.application for row in self.rows)
        if DomainApplication.DISTINGUISHES in applications:
            return PairStanding.DISTINGUISHED_BY_STANDING_DOMAIN
        if DomainApplication.NO_ENTRY_FOR_SURFACE_FORM in applications:
            return PairStanding.UNRESOLVED_MEASUREMENT_IMPOSSIBLE
        return PairStanding.UNDISTINGUISHED_AFTER_EXHAUSTIVE_MEASUREMENT

    @property
    def blocking_domains(self) -> tuple[str, ...]:
        """المجالاتُ التي تعذّر عليها القياس، مُسمّاةً لا مطويّة في مُخرَجٍ واحد."""

        return tuple(
            row.module_relative_path
            for row in self.rows
            if row.application is DomainApplication.NO_ENTRY_FOR_SURFACE_FORM
        )


@dataclass(frozen=True)
class NecessityProbeReport:
    """تقريرُ القياس كلِّه: كلُّ سطرٍ ظاهرٌ، ولا حُكمَ دستوريًّا في حقلٍ منه."""

    measurements: tuple[PairMeasurement, ...]
    target_digest: str
    pre_registered_expectation: str

    def __post_init__(self) -> None:
        if self.target_digest != DISCRIMINATION_TARGET_DIGEST:
            raise MorphologicalNecessityMeasurementError(
                "بصمةُ الهدف في التقرير تخالف المُجمَّدة؛ فالقياسُ جرى على غير ما جُمِّد."
            )
        if len(self.measurements) != len(FROZEN_DISCRIMINATION_TARGET):
            raise MorphologicalNecessityMeasurementError(
                "التقريرُ لا يغطّي الأزواجَ المُجمَّدة كلَّها."
            )

    @property
    def standing_by_pair(self) -> tuple[tuple[str, PairStanding], ...]:
        """منزلةُ كلِّ زوجٍ على حدة، لا مُخرَجٌ واحدٌ يبتلع التفصيل."""

        return tuple(
            (f"{m.pair.surface_a}/{m.pair.surface_b}", m.standing)
            for m in self.measurements
        )

    @property
    def matches_pre_registered_expectation(self) -> bool:
        """أطابقت النتيجةُ الفعليّةُ التوقّعَ المُسجَّل قبل القياس؟"""

        return all(
            measurement.standing is PairStanding.UNRESOLVED_MEASUREMENT_IMPOSSIBLE
            for measurement in self.measurements
        )


def run_necessity_probe() -> NecessityProbeReport:
    """أجرِ القياسَ فعلًا على الأزواج المُجمَّدة عبر المخروط المقروء من الشجرة."""

    cone = read_weaker_domain_cone()
    covered = tuple(reference.module_relative_path for reference in cone)
    measurements = tuple(
        PairMeasurement(
            pair=pair,
            rows=tuple(apply_domain_to_pair(pair, reference) for reference in cone),
            covered_cone=covered,
        )
        for pair in FROZEN_DISCRIMINATION_TARGET
    )
    return NecessityProbeReport(
        measurements=measurements,
        target_digest=discrimination_target_digest(),
        pre_registered_expectation=PRE_REGISTERED_EXPECTATION,
    )


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "necessity",
    "necessary",
    "verdict",
    "birth",
    "ضرورة",
    "حكم",
    "ولادة",
)


def _assert_no_necessity_field() -> None:
    """احرسْ خلوَّ وحدة القياس من حقلِ ضرورةٍ أو حكمٍ دستوريّ؛ فذلك ليس لها."""

    for declaring_type in (
        ReaderAttempt,
        DomainApplicationRow,
        PairMeasurement,
        NecessityProbeReport,
    ):
        for field in fields(declaring_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise RuntimeError(
                        f"{declaring_type.__name__}.{field.name} حقلٌ ممنوع: "
                        + MEASURED_NEGATIVE_IS_NOT_A_CONSTITUTIONAL_NECESSITY_NOTE
                    )


def _assert_measured_target_is_the_frozen_one() -> None:
    """احرسْ أنّ المقيسَ هو المُجمَّدُ عينُه، لا هدفًا أُعيدت صياغتُه هنا."""

    if discrimination_target_digest() != DISCRIMINATION_TARGET_DIGEST:
        raise RuntimeError(  # pragma: no cover - guard
            "هدفُ التمييز تغيّر؛ ولا يُقاس على هدفٍ غير الذي جُمِّد. "
            + MEASUREMENT_READS_A_FROZEN_TARGET_NOTE
        )
    if set(_READERS_BY_MODULE) != {
        reference.module_relative_path for reference in read_weaker_domain_cone()
    }:
        raise RuntimeError(  # pragma: no cover - guard
            "القوارئُ المُسجَّلة لا تطابق مخروطَ المجالات المُجمَّد. "
            + COVERAGE_BEFORE_JUDGEMENT_NOTE
        )


_assert_no_necessity_field()
_assert_measured_target_is_the_frozen_one()
