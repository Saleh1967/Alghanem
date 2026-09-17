"""القراءةُ بعد الختم: توقيعُ كلّ طبقةٍ على الصور المُجمَّدة، ثمّ حكمٌ مُشتَقّ.

هذه الوحدةُ تأتي **بعد** `fractal_transition_hypothesis` و
`fractal_transition_preregistration`، ولا تُضيف إليهما حقلًا ولا تُوسّع لهما
مفردة. وظيفتها أن تقرأ ما سُجِّل، ثمّ تشتقّ حكمًا من مفردة الأحكام الأربعة
المغلقة، ثمّ تتوقّف. والبوّابةُ **لا تقبل حكمًا من مُستدعيها**
(`CallerDoesNotOwnFractalVerdict`): لا تقرأ منه حالةً ولا سببًا ولا نتيجةَ
مطابقة، وإنّما تقرأ التسجيلَ المختوم والصورَ ثمّ تشتقّ.

**والختمُ يُفحَص لا يُصدَّق**: `seal_preregistration` تُعيد اشتقاق بصمتَي النصّ
والتسجيل عند الختم، والبوّابةُ تُعيد اشتقاقهما مرّةً أخرى عند القراءة؛ فتغيّرُ
حرفٍ واحدٍ في النصّ أو في بندٍ من البنود العشرة يُسقِط القراءةَ ولا يمرّ
تصحيحًا صامتًا. وهذا موضعُ `PostHocSimilarity != FractalEvidence` في الشيفرة لا
في النثر.

**والنقلُ هو الدعوى نفسها**: `S` هنا ليس دالّةً تُخترَع في هذه الوحدة، بل هو
عينُ ما سُجِّل: يُقرأ محمولُ الحقل في الطبقة الأدنى على الصورة، ويُتوقَّع أن
يقرأ الحقلُ نفسُه في الطبقة الأعلى على الصورة نفسها المحمولَ نفسَه. فإصابةُ
البنية `Reconstruct_K` عددُ المواضع التي صدق فيها هذا التوقّع، وإصابةُ النموذج
الأضعف `Reconstruct_W` عددُ المواضع التي صدق فيها مخرجُه الثابت. و
`Reconstruct_W >= Reconstruct_K` يُخرِج `WEAKER_MODEL_RECONSTRUCTS` قبل أيّ
قراءةٍ أخرى، لأن النصَّ يجعله سببَ تفنيدٍ مستقلًّا لا حاشيةً على النتيجة.

**وحقلٌ لا يستطيع أن يقرأ كذبًا لا يُسحَب من الحساب ولا يُرجَّح**: يُعَدّ كما
هو، ويُسمّى في `non_discriminating_fields` بعد القراءة. فحذفُه بعد رؤية النتيجة
تحسينُ معيارٍ بعد نتيجته، وترجيحُه اختراعُ وزنٍ لم يُسجَّل.

**وهذه القراءةُ تقف تحت معايرة `G0.FLT-0`**: التسجيلُ الذي تقرأ منه ثبت
انحرافُ نصّه المُبصَّم عن النصّ الوارد في موضعٍ يقرّر شرطَ النجاح، فحكمُها —
أيًّا كان — لا يُنسَب إلى الفرضية المطلوبة. وموضعُ هذا الاشتقاق
`fractal_transition_calibration`، وهي الجهةُ الوحيدةُ التي تُقرأ منها هذه
النتيجةُ منسوبةً إلى منزلتها.

**ولا ولادةَ هنا ولا تجميد**: `FractalReadout != Birth`، ولا `Freeze`، ولا
`E0`، ولا وحدةَ في `kernel/` تقرأ هذه المخرجات. والحكمُ — أيًّا كان — حكمٌ على
**هذه الصور الخمس بهاتين الوحدتين**، لا على العربية.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .fractal_transition_hypothesis import (
    COMPARED_FIELDS,
    HYPOTHESIS_DIGEST,
    HYPOTHESIS_TEXT,
    FractalVerdict,
    hypothesis_digest,
)
from .fractal_transition_preregistration import (
    DECLARED_PAIRS,
    FROZEN_CASES,
    MATCH_CRITERION,
    LayerStanding,
    PairDeclaration,
    layer_named,
    preregistration_digest,
)
from .p_extractor import read_surface
from .syllabifier import expand_slots, syllabify_reading
from .syllable_preregistration import PREREGISTRATION_DIGEST as SYLLABLE_DIGEST
from .syllable_preregistration import SyllableTemplate
from .word_structure_dictionary import analyze_word
from .word_structure_dictionary_preregistration import DictionaryLayer

__all__ = [
    "CALLER_DOES_NOT_OWN_FRACTAL_VERDICT_NOTE",
    "FIELD_EXTRACTORS",
    "A_READOUT_IS_NOT_A_BIRTH_NOTE",
    "FieldReading",
    "FractalTransitionReadoutError",
    "FractalTransitionReadoutGate",
    "HypothesisReadout",
    "PairReadout",
    "PairReadingStatus",
    "SealedPreregistration",
    "StructureSignature",
    "read_signature",
    "seal_preregistration",
]


class FractalTransitionReadoutError(ValueError):
    """رُفضت قراءةٌ ببصمةٍ غيرِ المختومة، أو بولايةٍ بلا مُستخرِجٍ مُسجَّل."""


_SEAL_TOKEN: Final[object] = object()


class PairReadingStatus(Enum):
    """قراءةُ زوجٍ واحد؛ و`MATCH_HOLDS` ليست حكمًا على الفرضية بل على زوج."""

    MATCH_HOLDS = "تطابقُ_البنية_قائمٌ_على_هذا_الزوج"
    REFUTED = "REFUTED"
    WEAKER_MODEL_RECONSTRUCTS = "WEAKER_MODEL_RECONSTRUCTS"
    UNDERPOWERED = "UNDERPOWERED"


@dataclass(frozen=True, slots=True)
class FieldReading:
    """محمولُ حقلٍ واحدٍ على صورةٍ واحدة، ومعه سببُه مُسمًّى لا مُستنتَجًا."""

    field: str
    holds: bool
    named_reason: str

    def __post_init__(self) -> None:
        if self.field not in COMPARED_FIELDS:
            raise FractalTransitionReadoutError(
                f"الحقل «{self.field}» خارج الحقول الستّة المُقارَنة"
            )
        if not isinstance(self.holds, bool):
            raise FractalTransitionReadoutError("محمولُ الحقل صوابٌ أو خطأ، لا ثالثَ له")
        if not isinstance(self.named_reason, str) or not self.named_reason.strip():
            raise FractalTransitionReadoutError("سببُ المحمول نصٌّ غير فارغ")


@dataclass(frozen=True, slots=True)
class StructureSignature:
    """توقيعُ الانتقال في ولايةٍ واحدةٍ على صورةٍ واحدة: ستّةُ محمولاتٍ لا غير."""

    jurisdiction: str
    surface: str
    readings: tuple[FieldReading, ...]

    def __post_init__(self) -> None:
        declared = tuple(reading.field for reading in self.readings)
        if declared != COMPARED_FIELDS:
            raise FractalTransitionReadoutError(
                "التوقيعُ يحمل الحقولَ الستّةَ بعينها وبترتيبها المُجمَّد"
            )

    def holds(self, field: str) -> bool:
        """محمولُ حقلٍ بعينه؛ وغيرُ المُقارَن يُرَدّ ولا يُقرأ أقربَ حقل."""

        for reading in self.readings:
            if reading.field == field:
                return reading.holds
        raise FractalTransitionReadoutError(f"الحقل «{field}» ليس في التوقيع")

    def reason(self, field: str) -> str:
        """سببُ محمولِ حقلٍ بعينه كما قُرِئ، لا كما يُفسَّر بعد النتيجة."""

        for reading in self.readings:
            if reading.field == field:
                return reading.named_reason
        raise FractalTransitionReadoutError(f"الحقل «{field}» ليس في التوقيع")


def _syllable_signature(surface: str) -> StructureSignature:
    reading = read_surface(surface)
    slots, expansion_failure = expand_slots(reading)
    word = syllabify_reading(reading)
    expanded_positions = tuple(slot.letter_index for slot in slots)
    segmented_positions = tuple(
        slot.letter_index for syllable in word.syllables for slot in syllable.slots
    )
    positions_are_inside_the_reading = all(
        0 <= position < len(reading.letters) for position in segmented_positions
    )
    identity_holds = (
        expansion_failure is None
        and bool(word.syllables)
        and segmented_positions == expanded_positions
        and positions_are_inside_the_reading
    )
    templates_are_closed = all(
        isinstance(syllable.template, SyllableTemplate) for syllable in word.syllables
    )
    refusals_are_named = all(item.reason.strip() for item in word.wazn_unresolved)
    return StructureSignature(
        jurisdiction="syllable-segmentation",
        surface=surface,
        readings=(
            FieldReading(
                field="Carrier",
                holds=bool(word.syllables),
                named_reason=(
                    f"عددُ المقاطع الخارجة: {len(word.syllables)}؛ والحاملُ قائمٌ "
                    "إن خرج مقطعٌ واحدٌ فأكثر"
                ),
            ),
            FieldReading(
                field="Gate",
                holds=word.is_resolved,
                named_reason=(
                    "مرّت الصورةُ في القوالب الستّة"
                    if word.is_resolved
                    else "وقف التقطيعُ عند: "
                    + "؛ ".join(item.reason for item in word.wazn_unresolved)
                ),
            ),
            FieldReading(
                field="Identity",
                holds=identity_holds,
                named_reason=(
                    f"مواضعُ الشرائح بعد التوسيع {expanded_positions} ومواضعُها "
                    f"بعد التقطيع {segmented_positions}"
                ),
            ),
            FieldReading(
                field="Trace",
                holds=word.preregistration_digest == SYLLABLE_DIGEST,
                named_reason=(
                    "القراءةُ تحمل بصمةَ تجميد المقاطع القائمة: "
                    f"{word.preregistration_digest[:12]}"
                ),
            ),
            FieldReading(
                field="Residual",
                holds=not word.wazn_unresolved,
                named_reason=(
                    "لا بقيّةَ في هذا الورود"
                    if not word.wazn_unresolved
                    else f"بقيّةٌ مُسمّاةٌ عددُها {len(word.wazn_unresolved)}"
                ),
            ),
            FieldReading(
                field="Closure",
                holds=templates_are_closed and refusals_are_named,
                named_reason=(
                    "كلُّ قالبٍ خارجٍ عضوٌ في الستّة، وكلُّ تعذّرٍ مُسمًّى بسببه"
                    if templates_are_closed and refusals_are_named
                    else "خرج قالبٌ خارج الستّة أو تعذّرٌ بلا سببٍ مُسمّى"
                ),
            ),
        ),
    )


def _word_signature(surface: str) -> StructureSignature:
    dictionary = analyze_word(surface)
    positions = sorted(
        [letter.position for letter in dictionary.letters]
        + [segment.position for segment in dictionary.unread]
    )
    closure_holds = positions == list(range(len(positions)))
    standings_are_readable = all(
        dictionary.standing_of(layer) is not None for layer in DictionaryLayer
    )
    return StructureSignature(
        jurisdiction="word-structure-dictionary",
        surface=surface,
        readings=(
            FieldReading(
                field="Carrier",
                holds=bool(dictionary.letters),
                named_reason=(f"عددُ الحروف المقروءة حالتُها: {len(dictionary.letters)}"),
            ),
            FieldReading(
                field="Gate",
                holds=not dictionary.unread,
                named_reason=(
                    "كلُّ وحدةٍ وقعت في الحوامل المُعلَنة"
                    if not dictionary.unread
                    else "وقع خارج الحوامل المُعلَنة: "
                    + "، ".join(
                        f"{segment.codepoint} في الموضع {segment.position}"
                        for segment in dictionary.unread
                    )
                ),
            ),
            FieldReading(
                field="Identity",
                holds=dictionary.surface_round_trips,
                named_reason=(
                    "الصورةُ تُعاد من قراءتها كما دخلت"
                    if dictionary.surface_round_trips
                    else "الصورةُ لا تُعاد من قراءتها كما دخلت"
                ),
            ),
            FieldReading(
                field="Trace",
                holds=standings_are_readable,
                named_reason=(
                    "منزلةُ كلّ طبقةٍ مُعلَنةٍ مقروءةٌ من القراءة نفسها: "
                    f"{len(dictionary.measured_layers)} مقيسةٌ و"
                    f"{len(dictionary.withheld)} محجوبة"
                ),
            ),
            FieldReading(
                field="Residual",
                holds=not dictionary.unread,
                named_reason=(
                    "لا بقيّةَ في هذا الورود"
                    if not dictionary.unread
                    else f"بقيّةٌ مُسمّاةٌ بمواضعها عددُها {len(dictionary.unread)}"
                ),
            ),
            FieldReading(
                field="Closure",
                holds=closure_holds,
                named_reason=(
                    f"مواضعُ الصورة {len(positions)} موزّعةٌ بين حرفٍ مقروءٍ "
                    "ومُمرَّرٍ مُسمًّى بلا موضعٍ ساقطٍ ولا مُكرَّر"
                    if closure_holds
                    else "موضعٌ سقط بين الحقلين أو تكرّر فيهما"
                ),
            ),
        ),
    )


FIELD_EXTRACTORS: Final[dict[str, Callable[[str], StructureSignature]]] = {
    "syllable-segmentation": _syllable_signature,
    "word-structure-dictionary": _word_signature,
}


def read_signature(jurisdiction: str, surface: str) -> StructureSignature:
    """اقرأ توقيعَ ولايةٍ مُرمَّزةٍ على صورة؛ وغيرُ المُرمَّزة تُرَدّ باسم سببها."""

    layer = layer_named(jurisdiction)
    if layer.standing is not LayerStanding.CODED_AND_MEASURABLE:
        raise FractalTransitionReadoutError(
            f"الولاية «{jurisdiction}» منزلتُها {layer.standing.value}: "
            f"{layer.why_this_standing}"
        )
    extractor = FIELD_EXTRACTORS.get(jurisdiction)
    if extractor is None:
        raise FractalTransitionReadoutError(
            f"لا مُستخرِجَ مُسجَّلًا للولاية «{jurisdiction}»؛ وإعلانُ منزلةٍ "
            "مُرمَّزةٍ بلا مُستخرِجٍ دعوى قياسٍ بلا قياس"
        )
    return extractor(surface)


@dataclass(frozen=True, slots=True)
class SealedPreregistration:
    """تسجيلٌ مختومٌ ببصمتيه؛ لا تُبنى إلّا من `seal_preregistration`."""

    hypothesis_digest: str
    preregistration_digest: str
    _token: object

    def __post_init__(self) -> None:
        if self._token is not _SEAL_TOKEN:
            raise FractalTransitionReadoutError(
                "الختمُ يصدر عن `seal_preregistration` وحدها؛ وختمٌ يُبنى باليد "
                "ليس ختمًا"
            )


def seal_preregistration() -> SealedPreregistration:
    """اختم التسجيلَ ببصمتيه المُشتقّتين حالًا، لا بثابتين منقولين."""

    return SealedPreregistration(
        hypothesis_digest=hypothesis_digest(),
        preregistration_digest=preregistration_digest(),
        _token=_SEAL_TOKEN,
    )


@dataclass(frozen=True, slots=True)
class PairReadout:
    """قراءةُ زوجٍ واحدٍ بعد الختم: حالتُه، وتناظرُ حقوله، وعدُّ الإصابات."""

    pair_id: str
    status: PairReadingStatus
    reason: str
    field_correspondence: tuple[tuple[str, bool], ...]
    disagreements: tuple[tuple[str, str], ...]
    non_discriminating_fields: tuple[str, ...]
    reconstruct_structure: int
    reconstruct_weaker_model: int
    comparisons: int
    is_holdout_pair: bool


@dataclass(frozen=True, slots=True)
class HypothesisReadout:
    """حكمُ الفرضية مُشتقًّا من قراءات الأزواج، بمفردةٍ رباعيّةٍ مغلقة."""

    verdict: FractalVerdict
    reason: str
    pairs: tuple[PairReadout, ...]
    hypothesis_digest: str
    preregistration_digest: str


def _is_holdout(pair: PairDeclaration) -> bool:
    lower = layer_named(pair.lower_jurisdiction)
    upper = layer_named(pair.upper_jurisdiction)
    return not lower.is_named_in_the_frozen_ladder and (
        not upper.is_named_in_the_frozen_ladder
    )


class FractalTransitionReadoutGate:
    """البوّابةُ الوحيدةُ التي تُصدر حكمًا؛ ولا تقبل من مُستدعيها حكمًا ولا سببًا."""

    @staticmethod
    def read_pair(sealed: SealedPreregistration, pair_id: str) -> PairReadout:
        """اقرأ زوجًا مُعلَنًا بعد فحص الختم؛ والزوجُ غيرُ المُعلَن يُرَدّ."""

        FractalTransitionReadoutGate._require_intact_seal(sealed)
        pair = next((item for item in DECLARED_PAIRS if item.pair_id == pair_id), None)
        if pair is None:
            raise FractalTransitionReadoutError(
                f"الزوج «{pair_id}» غيرُ مُعلَنٍ قبل التشغيل، فلا يُقرأ بعده"
            )
        lower = layer_named(pair.lower_jurisdiction)
        upper = layer_named(pair.upper_jurisdiction)
        holdout = _is_holdout(pair)
        unmeasurable = tuple(
            layer.jurisdiction
            for layer in (lower, upper)
            if layer.standing is not LayerStanding.CODED_AND_MEASURABLE
        )
        if unmeasurable:
            return PairReadout(
                pair_id=pair.pair_id,
                status=PairReadingStatus.UNDERPOWERED,
                reason=(
                    "ولايةٌ بلا حاملٍ مُرمَّزٍ يُقرأ لكلّ ورود: "
                    + "، ".join(unmeasurable)
                    + f"؛ وشرطُ القصور المُسجَّل: {pair.underpowered_condition}"
                ),
                field_correspondence=(),
                disagreements=(),
                non_discriminating_fields=(),
                reconstruct_structure=0,
                reconstruct_weaker_model=0,
                comparisons=0,
                is_holdout_pair=holdout,
            )

        correspondence: list[tuple[str, bool]] = []
        disagreements: list[tuple[str, str]] = []
        non_discriminating: list[str] = []
        structure_hits = 0
        weaker_hits = 0
        comparisons = 0
        for field in MATCH_CRITERION.compared_fields:
            field_holds_everywhere = True
            observed_upper: list[bool] = []
            for case in FROZEN_CASES:
                lower_signature = read_signature(lower.jurisdiction, case.surface)
                upper_signature = read_signature(upper.jurisdiction, case.surface)
                transported = lower_signature.holds(field)
                actual = upper_signature.holds(field)
                observed_upper.append(actual)
                comparisons += 1
                if transported == actual:
                    structure_hits += 1
                else:
                    field_holds_everywhere = False
                    disagreements.append(
                        (
                            field,
                            f"«{case.surface}»: الأدنى {transported} "
                            f"({lower_signature.reason(field)}) — الأعلى {actual} "
                            f"({upper_signature.reason(field)})",
                        )
                    )
                if actual is True:
                    weaker_hits += 1
            correspondence.append((field, field_holds_everywhere))
            if all(observed_upper):
                non_discriminating.append(field)

        if weaker_hits >= structure_hits:
            status = PairReadingStatus.WEAKER_MODEL_RECONSTRUCTS
            reason = (
                f"النموذجُ الأضعفُ الثابت أصاب {weaker_hits} من {comparisons}، "
                f"والبنيةُ بالنقل أصابت {structure_hits}؛ و"
                "`Reconstruct_W ≥ Reconstruct_K` سببُ تفنيدٍ مستقلٌّ بنصّ الفرضية"
            )
        else:
            failed = tuple(
                field
                for field, holds in correspondence
                if not holds and field in MATCH_CRITERION.refuting_fields
            )
            if failed:
                status = PairReadingStatus.REFUTED
                reason = (
                    "اختلّ تناظرُ حقلٍ مُفنِّدٍ فأكثر: "
                    + "، ".join(failed)
                    + f"؛ وشرطُ الفشل المُسجَّل: {pair.fail_condition}"
                )
            else:
                status = PairReadingStatus.MATCH_HOLDS
                reason = (
                    f"تناظرت الحقولُ المُفنِّدةُ الأربعةُ على {len(FROZEN_CASES)} "
                    f"صورٍ، وأصابت البنيةُ {structure_hits} من {comparisons} "
                    f"مقابلَ {weaker_hits} للنموذج الأضعف"
                )
        return PairReadout(
            pair_id=pair.pair_id,
            status=status,
            reason=reason,
            field_correspondence=tuple(correspondence),
            disagreements=tuple(disagreements),
            non_discriminating_fields=tuple(non_discriminating),
            reconstruct_structure=structure_hits,
            reconstruct_weaker_model=weaker_hits,
            comparisons=comparisons,
            is_holdout_pair=holdout,
        )

    @staticmethod
    def read_hypothesis(sealed: SealedPreregistration) -> HypothesisReadout:
        """اقرأ الأزواجَ المُعلَنةَ كلَّها، ثمّ اشتقّ حكمًا من المفردة الرباعية."""

        FractalTransitionReadoutGate._require_intact_seal(sealed)
        readouts = tuple(
            FractalTransitionReadoutGate.read_pair(sealed, pair.pair_id)
            for pair in DECLARED_PAIRS
        )
        reconstructing = tuple(
            item
            for item in readouts
            if item.status is PairReadingStatus.WEAKER_MODEL_RECONSTRUCTS
        )
        if reconstructing:
            return HypothesisReadout(
                verdict=FractalVerdict.WEAKER_MODEL_RECONSTRUCTS,
                reason=(
                    "أعاد نموذجٌ أضعفُ غيرُ فركتاليٍّ بناءَ النتائج على: "
                    + "، ".join(item.pair_id for item in reconstructing)
                ),
                pairs=readouts,
                hypothesis_digest=sealed.hypothesis_digest,
                preregistration_digest=sealed.preregistration_digest,
            )
        refuted = tuple(
            item for item in readouts if item.status is PairReadingStatus.REFUTED
        )
        if refuted:
            return HypothesisReadout(
                verdict=FractalVerdict.REFUTED,
                reason=(
                    "اختلّ تناظرُ حقلٍ مُفنِّدٍ على: "
                    + "، ".join(item.pair_id for item in refuted)
                ),
                pairs=readouts,
                hypothesis_digest=sealed.hypothesis_digest,
                preregistration_digest=sealed.preregistration_digest,
            )
        holdout_matches = tuple(
            item
            for item in readouts
            if item.status is PairReadingStatus.MATCH_HOLDS and item.is_holdout_pair
        )
        if len(holdout_matches) >= 3:
            return HypothesisReadout(
                verdict=FractalVerdict.SUPPORTED,
                reason=(
                    "تطابقت البنيةُ على زوجين لم يُسمَّيا في نصّ الصياغة، "
                    "وأُعيدت النتيجةُ على زوجٍ ثالثٍ مستقلّ"
                ),
                pairs=readouts,
                hypothesis_digest=sealed.hypothesis_digest,
                preregistration_digest=sealed.preregistration_digest,
            )
        return HypothesisReadout(
            verdict=FractalVerdict.UNDERPOWERED,
            reason=(
                f"بلغت أزواجُ التطابقِ خارجَ سلّم الصياغة {len(holdout_matches)}، "
                "وشرطُ النجاح يطلب طبقتين لم تُستخدما في الصياغة ثمّ إعادةً على "
                "ثالثةٍ مستقلّة؛ وكلُّ طبقةٍ مُعلَنةٍ هنا مذكورةٌ في نصّ الفرضية"
            ),
            pairs=readouts,
            hypothesis_digest=sealed.hypothesis_digest,
            preregistration_digest=sealed.preregistration_digest,
        )

    @staticmethod
    def _require_intact_seal(sealed: SealedPreregistration) -> None:
        if not isinstance(sealed, SealedPreregistration):
            raise FractalTransitionReadoutError("القراءةُ تجري على ختمٍ مُصدَرٍ لا على سواه")
        if sealed.hypothesis_digest != hypothesis_digest():
            raise FractalTransitionReadoutError(
                "نصُّ الفرضية تغيّر بعد ختمه؛ والقراءةُ عليه قراءةٌ على نصٍّ آخر"
            )
        if sealed.preregistration_digest != preregistration_digest():
            raise FractalTransitionReadoutError(
                "تغيّر بندٌ من البنود العشرة بعد ختمه؛ وتعديلُ المعيار بعد "
                "التشغيل هو عينُ ما يمنعه قانونُ عدم القفز"
            )
        if sealed.hypothesis_digest != HYPOTHESIS_DIGEST:
            raise FractalTransitionReadoutError("بصمةُ النصّ المختومة تخالف القائمة")


CALLER_DOES_NOT_OWN_FRACTAL_VERDICT_NOTE: Final[str] = (
    "CallerDoesNotOwnFractalVerdict: البوّابةُ لا تقرأ من مُستدعيها حالةً ولا "
    "سببًا ولا نتيجةَ مطابقة؛ وكلُّ ما تُصدره مُشتَقٌّ من التسجيل المختوم "
    "والصور المُجمَّدة"
)

A_READOUT_IS_NOT_A_BIRTH_NOTE: Final[str] = (
    "AReadoutIsNotABirth: هذه قراءةٌ على خمس صورٍ بوحدتين في هذا المستودع؛ "
    "ليست ولادةً، ولا تجميدًا، ولا حكمًا على العربية، ولا `E0`"
)

A_NON_DISCRIMINATING_FIELD_IS_COUNTED_NOT_DROPPED_NOTE: Final[str] = (
    "ANonDiscriminatingFieldIsCountedNotDropped: الحقلُ الذي قرأ محمولًا صادقًا "
    "على كلّ صورةٍ في الطبقة الأعلى يُسمّى في القراءة ويُعَدّ للطرفين معًا؛ "
    "وحذفُه بعد النتيجة تحسينُ معيارٍ بعد نتيجته"
)

READOUT_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    CALLER_DOES_NOT_OWN_FRACTAL_VERDICT_NOTE,
    A_READOUT_IS_NOT_A_BIRTH_NOTE,
    A_NON_DISCRIMINATING_FIELD_IS_COUNTED_NOT_DROPPED_NOTE,
)


def _refuse_an_extractor_without_a_declaration() -> None:
    for jurisdiction in FIELD_EXTRACTORS:
        layer = layer_named(jurisdiction)
        if layer.standing is not LayerStanding.CODED_AND_MEASURABLE:
            raise FractalTransitionReadoutError(
                f"مُستخرِجٌ لولايةٍ غيرِ مُعلَنةٍ مُرمَّزة: {jurisdiction}"
            )
    if HYPOTHESIS_TEXT.strip() == "":
        raise FractalTransitionReadoutError("لا قراءةَ على نصٍّ خالٍ")


_refuse_an_extractor_without_a_declaration()
