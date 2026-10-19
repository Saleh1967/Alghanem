"""اختبارُ الانتقال إلى المقطع: أيُعيّن سلّمُ رفع الالتباس شكلَ المقاطع؟

**السؤالُ مطروحٌ لا مُجابٌ عنه سلفًا**: بلغ سلّمُ رفع الالتباس طبقتَه الرابعة
(العلاقاتُ المقطعيّةُ والصرفيّة)، فهل يكفي ما بلغه لتعيين **شكل المقاطع** في
الكلمة التي وقعت فيها الهمزة؟ هذا سؤالُ انتقالٍ من طبقةٍ إلى ما فوقها، ولا
يُجاب عنه بالإعلان بل بالتشغيل.

**والهدفُ مقيسٌ لا مُعلَن**: شكلُ المقاطع يُستخرَج بتشغيل `syllabify_surface`
على سطح الكلمة المُعلَنة، فهو **قياسُ وحدةٍ أخرى** لا حقلٌ كتبناه بجانب الوقوع
(`THE_TARGET_IS_MEASURED_BY_THE_SYLLABIFIER_NOT_DECLARED`). وهو محجوبٌ عن
السلّم: لا يُسجَّل في حقول القطعة، ولا يُستشهَد به في طبقة.

**والقارئُ أعمى**: تُشغَّل التجربةُ بـ`run_target_recovery_experiment` نفسِها،
فلا يرى القارئُ إلّا قيمةَ السلّم، ويُسأل مرّةً واحدةً لكلّ قيمةٍ متمايزة.

**والنتيجةُ سالبةٌ على هذا المجال، ومقيسةٌ**: قيمةُ السلّم الواحدةُ تدمج كلماتٍ
تختلف أشكالُ مقاطعها، فتُردّ التجربةُ **قبل سؤال القارئ**؛ أي إنّ الانتقال إلى
المقطع **غيرُ حاصلٍ** بما بلغه السلّم
(`THE_LADDER_DOES_NOT_DETERMINE_THE_SYLLABLE_SHAPE`). وهذا تفنيدٌ على مجالٍ
مصمَّم، لا برهانُ استحالةٍ في العربية
(`A_REFUTATION_ON_A_DESIGNED_DOMAIN_IS_NOT_AN_IMPOSSIBILITY_PROOF`).

**ولا تُغلَق ولادةُ المقطع ههنا بحالٍ**: فشلُ الانتقال ليس ولادةً منفيّة، ونجاحُه
لو حصل ما كان ولادةً مُثبَتة (`SYLLABLE_BIRTH_IS_NOT_SETTLED_BY_THIS_RUN`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ، ولا استيرادَ من
`kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .disambiguation_layer_order import (
    DisambiguationLayer,
    LadderReader,
    LayerReading,
    ObservedItem,
    OrderedLadder,
    RecordedField,
    TargetRecoveryReport,
    refuse_syllable_birth_claim,
    run_target_recovery_experiment,
)
from .hamza_contract import (
    HamzaFunction,
    HamzaIdentity,
    HamzaOccurrence,
    HamzaRealization,
    HamzaSeat,
    codec_projection,
)
from .syllabifier import syllabify_surface

__all__ = [
    "A_REFUTATION_ON_A_DESIGNED_DOMAIN_IS_NOT_AN_IMPOSSIBILITY_PROOF_NOTE",
    "SYLLABLE_BIRTH_IS_NOT_SETTLED_BY_THIS_RUN_NOTE",
    "SYLLABLE_TRANSITION_NAMED_RESIDUALS",
    "THE_CARRIER_FIELD",
    "THE_DECLARED_HOSTED_ITEMS",
    "THE_DECLARED_HOSTS",
    "THE_FUNCTION_FIELD",
    "THE_HOSTED_LADDER",
    "THE_IDENTITY_FIELD",
    "THE_LADDER_DOES_NOT_DETERMINE_THE_SYLLABLE_SHAPE_NOTE",
    "THE_REALIZATION_FIELD",
    "THE_SEAT_FIELD",
    "THE_SYLLABLE_SHAPE_TARGET",
    "THE_TARGET_IS_MEASURED_BY_THE_SYLLABIFIER_NOT_DECLARED_NOTE",
    "AN_UNSEGMENTABLE_HOST_IS_A_NAMED_REFUSAL_NOTE",
    "HostedOccurrence",
    "SyllableTransitionError",
    "hosted_item",
    "measured_syllable_shape",
    "refuse_a_syllable_birth_claim_from_this_run",
    "run_syllable_transition_experiment",
    "the_transition_to_the_syllable_is_established",
]


class SyllableTransitionError(ValueError):
    """رفضٌ صريح: كلمةٌ متعذّرُ التقطيع، أو مضيفٌ بلا مصدرٍ مكتوب."""


THE_CARRIER_FIELD: Final[str] = "الحاملُ_المِرمازيّ"
THE_SEAT_FIELD: Final[str] = "الكرسيُّ_المِرمازيّ"
THE_IDENTITY_FIELD: Final[str] = "الهويّةُ_المُعلَنة"
THE_FUNCTION_FIELD: Final[str] = "الوظيفةُ_المُعلَنة"
THE_REALIZATION_FIELD: Final[str] = "التحقّقُ_السياقيّ"
THE_SYLLABLE_SHAPE_TARGET: Final[str] = "شكلُ_المقاطع_المقيس"
"""اسمُ الهدف؛ وهو محجوبٌ عن حقول القطعة وعن استشهاد الطبقات."""

_CODEC_SOURCE: Final[str] = "تشغيلُ المِرماز على سطح الوقوع"
_DECLARED_SOURCE: Final[str] = "إعلانُ الوقوع بمصدره المكتوب في هذه الوحدة"
_MEASURED_SOURCE: Final[str] = "تشغيلُ `syllabify_surface` على سطح الكلمة"


def measured_syllable_shape(surface: str) -> str:
    """شكلُ مقاطع الكلمة، مقيسًا بالمُقطِّع؛ والتعذّرُ رفضٌ مُسمًّى لا قيمةٌ خالية."""

    if not surface.strip():
        raise SyllableTransitionError("كلمةٌ خاليةٌ لا تُقطَّع")
    word = syllabify_surface(surface)
    if not word.is_resolved:
        raise SyllableTransitionError(
            f"تعذّر تقطيعُ «{surface}»؛ ولا يُقاس هدفٌ من تعذّرٍ فيُحسَب فرقًا"
        )
    return "-".join(syllable.template.value for syllable in word.syllables)


@dataclass(frozen=True, slots=True)
class HostedOccurrence:
    """وقوعُ همزةٍ في كلمةٍ مُعلَنة: حقولُه المفصولة، وسطحُ مضيفه."""

    occurrence: HamzaOccurrence
    host_note: str

    def __post_init__(self) -> None:
        if not isinstance(self.occurrence, HamzaOccurrence):
            raise SyllableTransitionError("وقوعٌ خارجَ عقد الهمزة لا يدخل التجربة")
        if not self.host_note.strip():
            raise SyllableTransitionError("مضيفٌ بلا بيانٍ مكتوبٍ لا يُقبَل")

    @property
    def host_surface(self) -> str:
        """سطحُ الكلمة المضيفة، مأخوذًا من الوقوع نفسِه لا مكتوبًا بجانبه."""

        return self.occurrence.surface

    @property
    def measured_shape(self) -> str:
        """هدفُ التجربة، مقيسًا عند كلّ طلبٍ لا محفوظًا مكتوبًا."""

        return measured_syllable_shape(self.host_surface)


def hosted_item(hosted: HostedOccurrence) -> ObservedItem:
    """قطعةٌ للسلّم: حقولُ الوقوع مُسجَّلةً، وشكلُ المقاطع هدفًا محجوبًا عنها."""

    carrier, seat = codec_projection(hosted.occurrence)
    occurrence = hosted.occurrence
    return ObservedItem(
        item_id=f"{occurrence.surface}@{occurrence.index}",
        original_measurement=carrier,
        recorded=(
            RecordedField(THE_CARRIER_FIELD, carrier, _CODEC_SOURCE),
            RecordedField(
                THE_SEAT_FIELD,
                "بلا_كرسيّ" if seat is None else seat,
                _CODEC_SOURCE,
            ),
            RecordedField(
                THE_IDENTITY_FIELD,
                occurrence.identity.value,
                occurrence.declared_source,
            ),
            RecordedField(
                THE_FUNCTION_FIELD,
                occurrence.function.value,
                occurrence.declared_source,
            ),
            RecordedField(
                THE_REALIZATION_FIELD,
                occurrence.realization.value,
                occurrence.declared_source,
            ),
        ),
        target=RecordedField(
            THE_SYLLABLE_SHAPE_TARGET, hosted.measured_shape, _MEASURED_SOURCE
        ),
    )


def _hosted(
    surface: str,
    index: int,
    identity: HamzaIdentity,
    seat: HamzaSeat,
    function: HamzaFunction,
    realization: HamzaRealization,
    context: str,
    host_note: str,
) -> HostedOccurrence:
    return HostedOccurrence(
        occurrence=HamzaOccurrence(
            surface=surface,
            index=index,
            identity=identity,
            seat=seat,
            function=function,
            realization=realization,
            context=context,
            declared_source=_DECLARED_SOURCE,
            content=context,
        ),
        host_note=host_note,
    )


THE_DECLARED_HOSTS: Final[tuple[HostedOccurrence, ...]] = (
    _hosted(
        "أَكَلَ",
        0,
        HamzaIdentity.HAMZA,
        HamzaSeat.ON_ALEF,
        HamzaFunction.QAT,
        HamzaRealization.REALIZED,
        "همزةُ قطعٍ فاءً للكلمة في «أَكَلَ»",
        "فعلٌ ثلاثيٌّ مفتوحُ العين",
    ),
    _hosted(
        "أُمٌّ",
        0,
        HamzaIdentity.HAMZA,
        HamzaSeat.ON_ALEF,
        HamzaFunction.QAT,
        HamzaRealization.REALIZED,
        "همزةُ قطعٍ فاءً للكلمة في «أُمٌّ»",
        "اسمٌ مُشدَّدُ اللام منوَّن",
    ),
    _hosted(
        "سَأَلَ",
        1,
        HamzaIdentity.HAMZA,
        HamzaSeat.ON_ALEF,
        HamzaFunction.QAT,
        HamzaRealization.REALIZED,
        "همزةُ قطعٍ عينًا للكلمة في «سَأَلَ»",
        "فعلٌ ثلاثيٌّ مهموزُ العين",
    ),
    _hosted(
        "رَأْسٌ",
        1,
        HamzaIdentity.HAMZA,
        HamzaSeat.ON_ALEF,
        HamzaFunction.QAT,
        HamzaRealization.REALIZED,
        "همزةُ قطعٍ ساكنةً عينًا للكلمة في «رَأْسٌ»",
        "اسمٌ ساكنُ العين منوَّن",
    ),
    _hosted(
        "سُؤَالٌ",
        1,
        HamzaIdentity.HAMZA,
        HamzaSeat.ON_WAW,
        HamzaFunction.QAT,
        HamzaRealization.REALIZED,
        "همزةُ قطعٍ على الواو في «سُؤَالٌ»",
        "مصدرٌ فيه ألفُ مدٍّ منوَّن",
    ),
    _hosted(
        "بِئْرٌ",
        1,
        HamzaIdentity.HAMZA,
        HamzaSeat.ON_YEH,
        HamzaFunction.QAT,
        HamzaRealization.REALIZED,
        "همزةُ قطعٍ ساكنةً على الياء في «بِئْرٌ»",
        "اسمٌ ساكنُ العين منوَّن",
    ),
    _hosted(
        "مَاءٌ",
        2,
        HamzaIdentity.HAMZA,
        HamzaSeat.BARE,
        HamzaFunction.QAT,
        HamzaRealization.REALIZED,
        "همزةٌ مفردةٌ على السطر لامًا للكلمة في «مَاءٌ»",
        "اسمٌ فيه ألفُ مدٍّ منوَّن",
    ),
    _hosted(
        "آمَنَ",
        0,
        HamzaIdentity.HAMZA,
        HamzaSeat.ON_ALEF_MADDA,
        HamzaFunction.QAT,
        HamzaRealization.LENGTHENED,
        "همزةُ قطعٍ ممدودةٌ على ألف المدّ في «آمَنَ»",
        "فعلٌ مزيدٌ أوّلُه ألفُ مدّ",
    ),
    _hosted(
        "اِبْنٌ",
        0,
        HamzaIdentity.HAMZA,
        HamzaSeat.NO_HAMZA_SEAT,
        HamzaFunction.WASL,
        HamzaRealization.REALIZED_AT_IBTIDA_ONLY,
        "همزةُ وصلٍ منطوقةٌ في الابتداء في «اِبْنٌ»",
        "اسمٌ مبدوءٌ بهمزة وصل",
    ),
    _hosted(
        "اُكْتُبْ",
        0,
        HamzaIdentity.HAMZA,
        HamzaSeat.NO_HAMZA_SEAT,
        HamzaFunction.WASL,
        HamzaRealization.REALIZED_AT_IBTIDA_ONLY,
        "همزةُ وصلٍ منطوقةٌ في الابتداء في «اُكْتُبْ»",
        "فعلُ أمرٍ مبدوءٌ بهمزة وصل",
    ),
)
"""مجالُ التجربة: وقوعاتُ همزةٍ في كلماتٍ مُعلَنةٍ، كلٌّ ببيان مضيفه."""

THE_DECLARED_HOSTED_ITEMS: Final[tuple[ObservedItem, ...]] = tuple(
    hosted_item(hosted) for hosted in THE_DECLARED_HOSTS
)
"""القطعُ بعد بناء حقولها وقياس أهدافها؛ لا عددَ مكتوبٌ بجانبها."""

THE_HOSTED_LADDER: Final[OrderedLadder] = OrderedLadder(
    readings=(
        LayerReading(DisambiguationLayer.CARRIER_IDENTITY, (THE_CARRIER_FIELD,)),
        LayerReading(DisambiguationLayer.RASM_VERSUS_SOUND, (THE_SEAT_FIELD,)),
        LayerReading(
            DisambiguationLayer.LICENSED_FEATURES,
            (THE_IDENTITY_FIELD, THE_FUNCTION_FIELD),
        ),
        LayerReading(
            DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS,
            (THE_REALIZATION_FIELD,),
        ),
    )
)
"""السلّمُ نفسُه بطبقاته الأربع؛ وشكلُ المقاطع خارجَه هدفًا لا رُتبةً فيه."""


def run_syllable_transition_experiment(
    reader: LadderReader,
) -> TargetRecoveryReport:
    """اسأل بالقارئ المُعطى: أيكفي ما بلغه السلّمُ لتعيين شكل المقاطع؟"""

    return run_target_recovery_experiment(
        THE_HOSTED_LADDER, THE_DECLARED_HOSTED_ITEMS, reader
    )


def _never_asked(value: tuple[tuple[str, str], ...]) -> str:
    raise SyllableTransitionError("سُئل القارئُ وقد دُمجت الأهداف؛ والتفنيدُ سابقٌ لسؤاله")


def the_transition_to_the_syllable_is_established() -> bool:
    """أحصل الانتقال؟ يُقاس بالتشغيل على المجال المُعلَن، ولا يُكتَب حكمًا."""

    return run_syllable_transition_experiment(
        _never_asked
    ).the_ladder_determines_the_target


def refuse_a_syllable_birth_claim_from_this_run() -> None:
    """ارفض أن تُقرأ هذه التجربةُ ولادةً للمقطع أو نفيًا لها."""

    refuse_syllable_birth_claim(
        DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS
    )


# --- البواقي المُسمّاة --------------------------------------------------------


AN_UNSEGMENTABLE_HOST_IS_A_NAMED_REFUSAL_NOTE: Final[str] = (
    "AnUnsegmentableHostIsANamedRefusal: كلمةٌ يتعذّر تقطيعُها تُرفَض باسمها في "
    "`measured_syllable_shape` ولا تدخل المجالَ بهدفٍ خالٍ؛ فالتعذّرُ ليس شكلًا "
    "ثالثًا يُحسَب فرقًا بين القطع"
)

A_REFUTATION_ON_A_DESIGNED_DOMAIN_IS_NOT_AN_IMPOSSIBILITY_PROOF_NOTE: Final[str] = (
    "ARefutationOnADesignedDomainIsNotAnImpossibilityProof: الكلماتُ العشرُ "
    "مُعلَنةٌ مختارةٌ ههنا، لا معدودةٌ من مدوّنةٍ مبصومة؛ فالتفنيدُ يُسقِط دعوى "
    "التعيين، ولا يُبرهن أنّ سلّمًا آخرَ بحقولٍ أُخَرَ لا يُعيّن شكلَ المقاطع"
)

SYLLABLE_BIRTH_IS_NOT_SETTLED_BY_THIS_RUN_NOTE: Final[str] = (
    "SyllableBirthIsNotSettledByThisRun: فشلُ الانتقال ليس نفيًا لولادة المقطع، "
    "ونجاحُه لو حصل ما كان إثباتًا لها؛ و`refuse_a_syllable_birth_claim_from_this_run` "
    "ترفض الدعويين معًا من هذه التجربة"
)

THE_LADDER_DOES_NOT_DETERMINE_THE_SYLLABLE_SHAPE_NOTE: Final[str] = (
    "TheLadderDoesNotDetermineTheSyllableShape: قيمةُ السلّم الواحدةُ تدمج "
    "كلماتٍ تختلف أشكالُ مقاطعها المقيسة، فتُردّ التجربةُ قبل سؤال القارئ؛ فما "
    "بلغه السلّمُ إلى طبقته الرابعة لا يُعيّن المقطع، وحاجةُ التعيين إلى قياسٍ "
    "جديدٍ مُسمّاةٌ ولم تُقضَ"
)

THE_TARGET_IS_MEASURED_BY_THE_SYLLABIFIER_NOT_DECLARED_NOTE: Final[str] = (
    "TheTargetIsMeasuredBySyllabifierNotDeclared: شكلُ المقاطع يُستخرَج بتشغيل "
    "`syllabify_surface` على سطح الكلمة عند كلّ طلب، فهو قياسُ وحدةٍ أخرى لا "
    "حقلٌ كُتِب بجانب الوقوع؛ ولو كُتِب لصار الهدفُ إعلانًا يُصدِّق نفسَه"
)

SYLLABLE_TRANSITION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_TARGET_IS_MEASURED_BY_THE_SYLLABIFIER_NOT_DECLARED_NOTE,
    THE_LADDER_DOES_NOT_DETERMINE_THE_SYLLABLE_SHAPE_NOTE,
    A_REFUTATION_ON_A_DESIGNED_DOMAIN_IS_NOT_AN_IMPOSSIBILITY_PROOF_NOTE,
    SYLLABLE_BIRTH_IS_NOT_SETTLED_BY_THIS_RUN_NOTE,
    AN_UNSEGMENTABLE_HOST_IS_A_NAMED_REFUSAL_NOTE,
)
"""البواقي المُسمّاة؛ تُعَدّ في الاختبار ولا يُكتَب عددُها بجانبها."""
