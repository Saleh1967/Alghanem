"""قيدٌ واحدٌ كان موزَّعًا في الشجرة بلا اسمٍ جامع، مجموعًا بشرط أن يُفحَص.

**ما تفعله هذه الوحدة**: تُسمّي قيدًا واحدًا — «لا يُشتَقّ من حاملٍ إلّا ما
يحفظه أو يُرخِّص الجسرُ إليه» — وتُثبِت أنّه **قائمٌ مفحوصٌ الآن** في أربع
وحداتٍ سبقتها، كلٌّ منها يُنفِّذه في مجاله باسمٍ خاصٍّ به. وليست تُنشئ سلطةً
ولا مفردةً ولا سُلَّمًا.

`A_DERIVED_CROSS_MODULE_LAW_IS_NOT_AN_ATTESTED_SOURCE_LAW`: اجتماعُ هذه
السوابق يُجيز استخراجَ قاعدةٍ تشغيليةٍ **داخل هذا المشروع**، ولا يجعلها نصًّا
منقولًا ولا قانونًا منسوبًا إلى النبهاني، ولا يرفع حالَ صفٍّ في
`docs/CONSTITUTION.md`، ولا يُنشئ بوّابة. فالفرقُ بين قاعدةٍ مُشتَقّةٍ من
انتظامٍ في شجرةٍ وبين قاعدةٍ منصوصةٍ في مصدرٍ فرقُ جنسٍ لا فرقُ درجة، وهذه من
الأولى.

`SUPPORT_IS_A_CHECKED_INVARIANT_NOT_AN_IMPORT`: وجودُ الوحدة ليس دليلًا على
تحقُّق المبدأ فيها. فكلُّ موضعِ دعمٍ هنا يحمل **دالّةَ فحصٍ** تُشغَّل فعلًا على
الحارس البنيويّ في موضعه، ولا يُعَدّ مدعومًا إلّا ما اجتاز::

    ModuleExists              != LawSupported
    NamedNoteExists           != LawSupported
    CheckedStructuralGuard     = LawSupported

`THE_FOUR_LAYER_SERIES_IS_AN_ALGHANEM_COMPOSITION`: السلسلةُ الرباعية —
الواقع، فالتصوّر، فاللفظ، فالحامل — **تركيبٌ مقترحٌ في مشروع الغانم**، يستند
إلى نصوصٍ منقولةٍ منسوبةٍ للنبهاني لم تُقابَل بعدُ بمصدرٍ مطبوع، ولا يُنسَب
إليه ترتيبُها في هذه السلسلة. ولذلك لا تُرمَّز السلسلةُ هنا مفردةً ولا تُبنى
عليها دالّةُ قرار.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

from .dalalat_thalath import (
    CHANNEL_DOES_NOT_DETERMINE_DALALA_NOTE,
    DalalaKind,
    channel_of_dalala,
    dalalat_of_channel,
)
from .epistemic_layers import (
    UNICODE_IS_NOT_RECORDED_SOUND_NOTE,
    EpistemicLayerError,
    OntologicalLayer,
    OntologicalLayerClassification,
)
from .maluma_mafhum import (
    EXCLUDED_TARGET_NOTES,
    STRUCTURAL_UNDERSTANDING_IS_NOT_A_CONCEPT_NOTE,
    ContentStanding,
    MalumaMafhumError,
    SemanticTarget,
    UnderstandingRecord,
)
from .wad_naql import (
    DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH_NOTE,
    WadDerivationRefusal,
    WadNaqlError,
    refuse_derivation,
)

__all__ = [
    "A_DERIVED_CROSS_MODULE_LAW_IS_NOT_AN_ATTESTED_SOURCE_LAW_NOTE",
    "A_SIGN_IS_NOT_ITS_REFERENT_AND_NEITHER_IS_IT_UNRELATED_TO_IT_NOTE",
    "A_ZERO_SHOWS_AN_UNBUILT_BRIDGE_NOT_AN_IMPOSSIBLE_ONE_NOTE",
    "CARRIER_AUTHORITY_SUPPORTS",
    "FORMAL_ENCODING_IS_NOT_CONCEPTUAL_MEANING_NOTE",
    "NO_DERIVATION_BEYOND_THE_AUTHORITY_OF_ITS_CARRIER_NOTE",
    "SUPPORT_IS_A_CHECKED_INVARIANT_NOT_AN_IMPORT_NOTE",
    "THE_FOUR_LAYER_SERIES_IS_AN_ALGHANEM_COMPOSITION_NOTE",
    "TRANSITION_AUTHORITY_IS_NOT_A_GATE_NOTE",
    "TRANSITION_AUTHORITY_NAMED_RESIDUALS",
    "CarrierAuthoritySupport",
    "TransitionAuthorityError",
    "supported_positions",
    "unsupported_positions",
]


class TransitionAuthorityError(ValueError):
    """رفضٌ صريحٌ في جمع القيد: موضعُ دعمٍ بلا فحصٍ أو باسمِ قيدٍ غيرِ مُودَع."""


# --- القيدُ نفسُه، وحدودُه ------------------------------------------------------


NO_DERIVATION_BEYOND_THE_AUTHORITY_OF_ITS_CARRIER_NOTE: Final[str] = (
    "NoDerivationBeyondTheAuthorityOfItsCarrier: لا يُشتَقّ من حاملٍ إلّا ما "
    "يحفظه الحاملُ نفسُه أو ما يُرخِّص الجسرُ إليه. فالترميزُ الرقميّ يحفظ "
    "صورةَ اللفظ، والبنيةُ اللفظية تحفظ بعضَ الخصائص والعلاقات اللغوية، "
    "والمدلولُ المفهوميّ يلزمه الوضعُ والسياقُ والمعرفةُ السابقة، والحكمُ على "
    "الواقع يلزمه دليلٌ مستقلٌّ عن مجرّد الدلالة. وكلُّ انتقالٍ يتجاوز سلطةَ "
    "حامله بلا جسرٍ مُرخَّصٍ قفزةٌ طبقية"
)

A_ZERO_SHOWS_AN_UNBUILT_BRIDGE_NOT_AN_IMPOSSIBLE_ONE_NOTE: Final[str] = (
    "AZeroShowsAnUnbuiltBridgeNotAnImpossibleOne: صفرٌ خرج من مُستخرِجٍ بعينه "
    "على مدوَّنةٍ بعينها يُثبِت أنّ **ذلك الجسر** لم يُبنَ ولم يُرخَّص، ولا "
    "يُثبِت امتناعَ بنائه. ورفعُ الحكم من «هذا المُستخرِج أخفق» إلى «هذا "
    "المدخلُ غير كافٍ لهذا المخرج» دعوى على **كلّ مُستخرِجٍ ممكن**، وهي تلزمها "
    "برهانُ عدمِ كفايةٍ لا محاولةٌ فاشلة؛ وهذا حدُّ "
    "`CompleteInductionIsCorpusBounded` مرفوعًا من المدوَّنة إلى فضاء الدوالّ"
)

A_SIGN_IS_NOT_ITS_REFERENT_AND_NEITHER_IS_IT_UNRELATED_TO_IT_NOTE: Final[str] = (
    "ASignIsNotItsReferentAndNeitherIsItUnrelatedToIt: تبدُّلُ العلامة مع بقاء "
    "المرجع يُثبِت أنّ العلامةَ ليست الشيءَ وأنّ تغيُّرَها لا يستلزم تغيُّرَه؛ "
    "ولا يلزم منه انتفاءُ الصلة بينهما. فالمنفيُّ **الانتقالُ المباشر** من "
    "اللفظ إلى الواقع، لا الصلةُ التي تقوم بالمفهوم والوضع والسياق. والأولى "
    "مُحتمِلةٌ للدفاع، والثانية أوسعُ من دليلها"
)

FORMAL_ENCODING_IS_NOT_CONCEPTUAL_MEANING_NOTE: Final[str] = (
    "FormalEncodingIsNotConceptualMeaning: الحدُّ الصحيح أنّ الترميزَ الشكليّ "
    "ليس المدلولَ المفهوميّ، وليس أنّ اللغةَ ليست معنًى. فالأوّل يمنع القفزةَ "
    "من الصورة اللفظية وحدها إلى المفهوم، والثاني يُغلِق الدلالةَ كلَّها "
    "ويُنكِر ما يقوم بالوضع والسياق والمعرفة السابقة"
)

A_DERIVED_CROSS_MODULE_LAW_IS_NOT_AN_ATTESTED_SOURCE_LAW_NOTE: Final[str] = (
    "ADerivedCrossModuleLawIsNotAnAttestedSourceLaw: هذا القيدُ **تركيبُ هذا "
    "المشروع** من قيودٍ قائمةٍ مفحوصةٍ في وحداتٍ سبقته، لا نصٌّ منقولٌ ولا "
    "قانونٌ منسوبٌ إلى النبهاني. فاجتماعُ سوابقَ في شجرةٍ يُجيز قاعدةً "
    "تشغيليةً داخلها، ولا يرفع حالَ صفٍّ في `docs/CONSTITUTION.md`، ولا يُنشئ "
    "بوّابةً، ولا يصير بهذا الاجتماع منصوصًا في مصدر"
)

SUPPORT_IS_A_CHECKED_INVARIANT_NOT_AN_IMPORT_NOTE: Final[str] = (
    "SupportIsACheckedInvariantNotAnImport: وجودُ الوحدة يُثبِت أنّها في "
    "الشجرة، ولا يُثبِت أنّ المبدأ تحقَّق فيها؛ وكذلك وجودُ ثابتٍ مُسمًّى "
    "فيها. فموضعُ الدعم هنا لا يُعَدّ مدعومًا إلّا إذا شُغِّلت دالّةُ فحصه "
    "على الحارس البنيويّ في موضعه فاجتازَته"
)

THE_FOUR_LAYER_SERIES_IS_AN_ALGHANEM_COMPOSITION_NOTE: Final[str] = (
    "TheFourLayerSeriesIsAnAlghanemComposition: السلسلةُ الرباعية — الواقع، "
    "فالتصوّر، فاللفظ، فالحامل — تركيبٌ مقترحٌ في مشروع الغانم، يستند إلى "
    "نصوصٍ منقولةٍ منسوبةٍ للنبهاني لم تُقابَل بعدُ بمصدرٍ مطبوع، ولا يُنسَب "
    "إليه ترتيبُها في هذه السلسلة. فلا يُقال «نظرية النبهاني في الطبقات "
    "الأربع»، ولا تُرمَّز السلسلةُ مفردةً مغلقةً ولا تُبنى عليها دالّةُ قرار"
)

TRANSITION_AUTHORITY_IS_NOT_A_GATE_NOTE: Final[str] = (
    "TransitionAuthorityIsNotAGate: هذه الوحدةُ تجمع قيدًا وتفحص مواضعَ "
    "دعمه، ولا تحكم على انتقالٍ ولا تمنعه ولا ترخّصه؛ فالمنعُ حيث الحارسُ "
    "البنيويّ في موضعه، لا هنا"
)

TRANSITION_AUTHORITY_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "NoDerivationBeyondTheAuthorityOfItsCarrier": (
        NO_DERIVATION_BEYOND_THE_AUTHORITY_OF_ITS_CARRIER_NOTE
    ),
    "AZeroShowsAnUnbuiltBridgeNotAnImpossibleOne": (
        A_ZERO_SHOWS_AN_UNBUILT_BRIDGE_NOT_AN_IMPOSSIBLE_ONE_NOTE
    ),
    "ASignIsNotItsReferentAndNeitherIsItUnrelatedToIt": (
        A_SIGN_IS_NOT_ITS_REFERENT_AND_NEITHER_IS_IT_UNRELATED_TO_IT_NOTE
    ),
    "FormalEncodingIsNotConceptualMeaning": (
        FORMAL_ENCODING_IS_NOT_CONCEPTUAL_MEANING_NOTE
    ),
    "ADerivedCrossModuleLawIsNotAnAttestedSourceLaw": (
        A_DERIVED_CROSS_MODULE_LAW_IS_NOT_AN_ATTESTED_SOURCE_LAW_NOTE
    ),
    "SupportIsACheckedInvariantNotAnImport": (
        SUPPORT_IS_A_CHECKED_INVARIANT_NOT_AN_IMPORT_NOTE
    ),
    "TheFourLayerSeriesIsAnAlghanemComposition": (
        THE_FOUR_LAYER_SERIES_IS_AN_ALGHANEM_COMPOSITION_NOTE
    ),
    "TransitionAuthorityIsNotAGate": TRANSITION_AUTHORITY_IS_NOT_A_GATE_NOTE,
}
"""ما تُسمّيه هذه الوحدة؛ والقيدُ الجامعُ أوّلُها وسائرُها حدودٌ عليه."""


# --- مواضعُ الدعم: قيدٌ مُسمًّى في موضعه، وفحصٌ يُشغَّل عليه ---------------------


@dataclass(frozen=True, slots=True)
class CarrierAuthoritySupport:
    """موضعُ دعمٍ واحد: وحدتُه، واسمُ قيده فيها، ونصُّه، ودالّةُ فحصه.

    ولا يقوم بلا دالّةِ فحص: موضعٌ بلا فحصٍ دعوى استيرادٍ لا دعوى تحقُّق
    (`SUPPORT_IS_A_CHECKED_INVARIANT_NOT_AN_IMPORT_NOTE`).
    """

    law_name: str
    module_name: str
    invariant_name: str
    invariant_text: str
    what_the_guard_refuses: str
    check: Callable[[], bool]

    def __post_init__(self) -> None:
        for value, label in (
            (self.law_name, "اسمُ القيد"),
            (self.module_name, "اسمُ الوحدة"),
            (self.invariant_name, "اسمُ القيد في موضعه"),
            (self.invariant_text, "نصُّ القيد في موضعه"),
            (self.what_the_guard_refuses, "ما يرفضه الحارس"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise TransitionAuthorityError(f"{label} نصٌّ غير فارغ.")
        if self.law_name not in TRANSITION_AUTHORITY_NAMED_RESIDUALS:
            raise TransitionAuthorityError(
                f"موضعُ دعمٍ لقيدٍ غيرِ مُودَعٍ بهذا الاسم: {self.law_name}"
            )
        if not callable(self.check):
            raise TransitionAuthorityError(
                "موضعُ دعمٍ بلا دالّةِ فحصٍ دعوى استيرادٍ لا دعوى تحقُّق."
            )

    def holds(self) -> bool:
        """أشُغِّل الحارسُ البنيويُّ في موضعه الآن فاجتاز الفحص؟"""

        return self.check() is True


def _physical_layer_cannot_be_constructed() -> bool:
    """الطبقةُ الفيزيائية مُعلَنةٌ وممتنعةُ البناء؛ والامتناعُ يُختبَر لا يُوصَف."""

    try:
        OntologicalLayerClassification(
            layer=OntologicalLayer.PHYSICAL_EXISTENCE,
            artifact_kind="نقاط_ترميز",
        )
    except EpistemicLayerError:
        return True
    return False


def _reality_match_is_not_a_semantic_target() -> bool:
    """المطابقةُ للخارج مستبعَدةٌ بالإنشاء: لا سجلَّ يُبنى عليها هدفًا."""

    if SemanticTarget.المطابقة_للخارج not in EXCLUDED_TARGET_NOTES:
        return False
    try:
        UnderstandingRecord(
            content_id="فحص",
            target=SemanticTarget.المطابقة_للخارج,
            structurally_admissible=True,
            sanad=(),
            declared_standing=ContentStanding.معلومة,
        )
    except MalumaMafhumError:
        return True
    return False


def _structural_reading_alone_is_not_a_concept() -> bool:
    """قراءةٌ بنيويةٌ صحيحةٌ بلا سندٍ تبقى معلومةً، وترقيتُها ترتفع بها الحال."""

    reading = UnderstandingRecord(
        content_id="فحص",
        target=SemanticTarget.استرجاع_الوضع,
        structurally_admissible=True,
        sanad=(),
        declared_standing=ContentStanding.معلومة,
    )
    if reading.is_concept:
        return False
    try:
        UnderstandingRecord(
            content_id="فحص",
            target=SemanticTarget.استرجاع_الوضع,
            structurally_admissible=True,
            sanad=(),
            declared_standing=ContentStanding.مفهوم,
        )
    except MalumaMafhumError:
        return True
    return False


def _wad_is_not_derived_from_either_side() -> bool:
    """طريقا الاستنباط مرفوضان بالإنشاء، كلاهما لا أحدُهما."""

    for path in WadDerivationRefusal:
        try:
            refuse_derivation(path)
        except WadNaqlError:
            continue
        return False
    return True


def _the_channel_does_not_determine_the_dalala() -> bool:
    """من الدلالة تُشتَقّ القناة، ولا يُشتَقّ من القناة دلالةٌ بعينها."""

    for kind in DalalaKind:
        channel = channel_of_dalala(kind)
        if kind not in dalalat_of_channel(channel):
            return False
    spoken = channel_of_dalala(DalalaKind.مطابقة)
    return len(dalalat_of_channel(spoken)) > 1


CARRIER_AUTHORITY_SUPPORTS: Final[tuple[CarrierAuthoritySupport, ...]] = (
    CarrierAuthoritySupport(
        law_name="NoDerivationBeyondTheAuthorityOfItsCarrier",
        module_name="alghanem.arabic.epistemic_layers",
        invariant_name="UnicodeIsNotRecordedSound",
        invariant_text=UNICODE_IS_NOT_RECORDED_SOUND_NOTE,
        what_the_guard_refuses=(
            "إصدارَ تصنيفٍ في الطبقة الفيزيائية من قطعةٍ في هذا المستودع: "
            "نقاطُ الترميز لا تحفظ الصوتَ، فلا يُشتَقّ منها ما لا تحفظه"
        ),
        check=_physical_layer_cannot_be_constructed,
    ),
    CarrierAuthoritySupport(
        law_name="NoDerivationBeyondTheAuthorityOfItsCarrier",
        module_name="alghanem.arabic.wad_naql",
        invariant_name="DistributionalTraceIsNotWadPath",
        invariant_text=DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH_NOTE,
        what_the_guard_refuses=(
            "اشتقاقَ الوضع من التحليل التوزيعيّ أو من تحليل المدلول: أثرُ "
            "الوضع غيرُ طريقِ معرفته، والجسرُ إليه النقلُ لا الانتظام"
        ),
        check=_wad_is_not_derived_from_either_side,
    ),
    CarrierAuthoritySupport(
        law_name="ASignIsNotItsReferentAndNeitherIsItUnrelatedToIt",
        module_name="alghanem.arabic.maluma_mafhum",
        invariant_name="المطابقة_للخارج مستبعَدةٌ بنيويًّا لا عمليًّا",
        invariant_text=EXCLUDED_TARGET_NOTES[SemanticTarget.المطابقة_للخارج],
        what_the_guard_refuses=(
            "اتّخاذَ مطابقةِ الخارج هدفًا للدلالة داخل هذا الأنبوب. والمرفوضُ "
            "الانتقالُ المباشر لا الصلة: النصُّ نفسُه يُعلِّل بأنّها تحتاج "
            "دليلًا خارج اللغة، وهذا إثباتُ جسرٍ لازمٍ لا نفيُ صلة"
        ),
        check=_reality_match_is_not_a_semantic_target,
    ),
    CarrierAuthoritySupport(
        law_name="FormalEncodingIsNotConceptualMeaning",
        module_name="alghanem.arabic.maluma_mafhum",
        invariant_name="StructuralUnderstandingIsNotAConcept",
        invariant_text=STRUCTURAL_UNDERSTANDING_IS_NOT_A_CONCEPT_NOTE,
        what_the_guard_refuses=(
            "ترقيةَ فهمٍ بنيويٍّ صحيحٍ إلى مفهومٍ بلا سندٍ ينتهي بحسّ؛ فالبنيةُ "
            "تُعطي معلومةً، والمفهومُ يلزمه جسرٌ آخر"
        ),
        check=_structural_reading_alone_is_not_a_concept,
    ),
    CarrierAuthoritySupport(
        law_name="FormalEncodingIsNotConceptualMeaning",
        module_name="alghanem.arabic.dalalat_thalath",
        invariant_name="ChannelDoesNotDetermineDalala",
        invariant_text=CHANNEL_DOES_NOT_DETERMINE_DALALA_NOTE,
        what_the_guard_refuses=(
            "عكسَ اتّجاه الاشتقاق: القناةُ تُشتَقّ من الدلالة، ولا تُشتَقّ "
            "منها دلالةٌ بعينها، فاشتقاقُ الأضيقِ من الأوسع ترجيحٌ بلا مُرجِّح"
        ),
        check=_the_channel_does_not_determine_the_dalala,
    ),
)
"""خمسةُ مواضعَ سبقت هذه الوحدة، كلٌّ منها يُنفِّذ القيدَ في مجاله باسمه."""


def supported_positions() -> tuple[CarrierAuthoritySupport, ...]:
    """المواضعُ التي شُغِّل حارسُها الآن فاجتاز؛ والباقي لا يُعَدّ دعمًا."""

    return tuple(support for support in CARRIER_AUTHORITY_SUPPORTS if support.holds())


def unsupported_positions() -> tuple[CarrierAuthoritySupport, ...]:
    """المواضعُ التي لم يجتز حارسُها؛ تُخرَج ولا تُطوى في فرقِ عددٍ صامت."""

    return tuple(
        support for support in CARRIER_AUTHORITY_SUPPORTS if not support.holds()
    )


_LAWS_WITH_A_CHECKED_POSITION: Final[frozenset[str]] = frozenset(
    support.law_name for support in CARRIER_AUTHORITY_SUPPORTS
)

if "NoDerivationBeyondTheAuthorityOfItsCarrier" not in _LAWS_WITH_A_CHECKED_POSITION:
    raise RuntimeError("القيدُ الجامعُ بلا موضعِ دعمٍ مفحوصٍ لا يُودَع.")
