"""قراءةُ G0.FLT-1 على قانون القياس: تُشغَّل بعد التجميد، وتُخرِج ما يخرج.

هذه الوحدةُ **لاحقةٌ** لإيداع `flt1_qiyas_law.py` و`flt1_qiyas_preregistration.py`
في تاريخ المستودع، ولا تُعدِّل منهما حرفًا. وهي تختم التسجيلَ ببصمتيه ثمّ
تُعيد اشتقاقهما عند كلّ قراءة؛ فإن انزاحت بصمةٌ رُدَّت القراءةُ ولم تُصحَّح.

**والهدفُ ليس مخرجَ المُرخَّص** (`TheTargetComesFromTheSameReaderAsTheLicensedModel`):
هدفُ إعادة البناء في هذه النسخة مأخوذٌ من المُقطِّع نفسِه الذي يُجسِّد النموذجَ
المُرخَّص. فتفوّقُ المُرخَّص **مضمونٌ بالبناء** ولا يُعَدّ شاهدًا. ولهذا يكون
حكمُ الأدنويّة غيرَ متماثل: تساوي نموذجٍ أضعفَ يُسقِط الدعوى إسقاطًا، وتفوّقُ
المُرخَّص لا يرفعها بل يترك الشرطَ `UNDERPOWERED`. وهذا هو درسُ `G0.FLT-0`
مطبَّقًا على نفسنا.

**وبوّاباتٌ تحليليّةٌ لا تُعَدّ شاهدًا** (`AnalyticGatesCarryNoDiscriminatingWeight`):
`w^\\*` و`\\mu` في هذه النسخة صادقتان بحكم دالّة القوالب نفسِها، لا بحكم
المدوّنة. فتُقرأان ويُسمّى كونُهما تحليليّتين، ولا تُحسَبان إصابةً.

**وفرعٌ من آلة القرار لم يُطلَق ليس مُختبَرًا**
(`AnUnfiredRuleIsAnUntestedRule`): يُعَدّ في المُخرَج أيُّ مخرجٍ مُسجَّلٍ لم
تُطلِقه المدوّنةُ المُجمَّدة، ولا يُعَدّ سكوتُه نجاحًا.

**ولا تُعدَّل الفرضيّةُ بعد النتيجة**: `PostHocSimilarity != FractalEvidence`.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .flt1_preregistration import (
    FLT1_FROZEN_SURFACES,
    WEAKER_REPRESENTATIONS,
)
from .flt1_qiyas_law import FLT1_QIYAS_TEXT_DIGEST, qiyas_text_digest
from .flt1_qiyas_preregistration import (
    DECISION_RULES,
    FLT1_QIYAS_PREREGISTRATION_DIGEST,
    HigherCenterStanding,
    QiyasOutcome,
    flt1_qiyas_preregistration_digest,
)
from .p_extractor import PhoneticRole, read_surface
from .syllabifier import SlotKind, Syllable, expand_slots, syllabify_reading

__all__ = [
    "ANALYTIC_GATES_CARRY_NO_DISCRIMINATING_WEIGHT_NOTE",
    "AN_UNFIRED_RULE_IS_AN_UNTESTED_RULE_NOTE",
    "ANALYTIC_GATE_SYMBOLS",
    "PREVENTER_ROLES",
    "QIYAS_READOUT_NAMED_RESIDUALS",
    "THE_TARGET_COMES_FROM_THE_SAME_READER_NOTE",
    "BranchReading",
    "GateReading",
    "MinimalityReading",
    "MinimalityStanding",
    "QiyasReadoutError",
    "QiyasRun",
    "SealedQiyasPreregistration",
    "SurfaceReading",
    "WeakerModelScore",
    "read_qiyas",
    "seal_qiyas_preregistration",
]


class QiyasReadoutError(ValueError):
    """رفضٌ مُسمّى في قراءة القياس؛ لا تصحيحَ صامتًا ولا تخطّي."""


_SEAL_TOKEN: Final[object] = object()

PREVENTER_ROLES: Final[frozenset[PhoneticRole]] = frozenset(
    {PhoneticRole.ASSIMILATED_SILENT, PhoneticRole.SILENT_DIFFERENTIATING_ALIF}
)

ANALYTIC_GATE_SYMBOLS: Final[tuple[str, ...]] = (r"w^\*", r"\mu")

_ORIGIN_TEMPLATE: Final[str] = "CV"


@dataclass(frozen=True, slots=True)
class SealedQiyasPreregistration:
    """تسجيلٌ مختومٌ ببصمتيه؛ لا يُنشَأ إلّا من `seal_qiyas_preregistration`."""

    law_text_digest: str
    preregistration_digest: str
    _token: object

    def __post_init__(self) -> None:
        if self._token is not _SEAL_TOKEN:
            raise QiyasReadoutError(
                "التسجيلُ المختومُ لا يُبنى مباشرةً؛ فبناؤه بيدٍ يُبطِل الختم"
            )


def seal_qiyas_preregistration() -> SealedQiyasPreregistration:
    """اختم التسجيلَ القائم ببصمتيه المُشتقّتين، لا بقيمتين منقولتين."""

    return SealedQiyasPreregistration(
        law_text_digest=qiyas_text_digest(),
        preregistration_digest=flt1_qiyas_preregistration_digest(),
        _token=_SEAL_TOKEN,
    )


def _require_intact_seal(sealed: SealedQiyasPreregistration) -> None:
    if not isinstance(sealed, SealedQiyasPreregistration):
        raise QiyasReadoutError("القراءةُ تطلب تسجيلًا مختومًا لا كائنًا آخر")
    if sealed.law_text_digest != FLT1_QIYAS_TEXT_DIGEST:
        raise QiyasReadoutError(
            "نصُّ القانون انزاح عن بصمته المُجمَّدة؛ والقراءةُ عليه قراءةٌ لنصٍّ آخر"
        )
    if sealed.preregistration_digest != FLT1_QIYAS_PREREGISTRATION_DIGEST:
        raise QiyasReadoutError(
            "التسجيلُ انزاح عن بصمته المُجمَّدة؛ ولا تُقرأ نتيجةٌ على تسجيلٍ مُبدَّل"
        )
    if qiyas_text_digest() != FLT1_QIYAS_TEXT_DIGEST:
        raise QiyasReadoutError("بصمةُ النصّ المُشتقّةُ الآن تخالف المُجمَّدة")
    if flt1_qiyas_preregistration_digest() != FLT1_QIYAS_PREREGISTRATION_DIGEST:
        raise QiyasReadoutError("بصمةُ التسجيل المُشتقّةُ الآن تخالف المُجمَّدة")


@dataclass(frozen=True, slots=True)
class GateReading:
    """قراءةُ بوّابةٍ واحدةٍ على فرعٍ واحد: أثبتَت أم لا، وبأيّ سببٍ مُسمّى."""

    symbol: str
    holds: bool
    named_reason: str
    is_analytic_in_this_deposit: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.holds, bool):
            raise QiyasReadoutError("ثبوتُ البوّابة قيمةٌ ثنائيّة")
        if not isinstance(self.named_reason, str) or not self.named_reason.strip():
            raise QiyasReadoutError("سببُ قراءة البوّابة نصٌّ غيرُ فارغ")


@dataclass(frozen=True, slots=True)
class BranchReading:
    """فرعٌ مرشَّحٌ واحدٌ — مقطعٌ — بقراءات بوّاباته ومخرج آلة القرار عليه."""

    surface: str
    branch_index: int
    template: str
    gates: tuple[GateReading, ...]
    outcome: QiyasOutcome

    def gate(self, symbol: str) -> GateReading:
        """أعِد قراءةَ بوّابةٍ بعينها؛ وغيرُ المقروءة تُرَدّ لا تُخترَع."""

        for reading in self.gates:
            if reading.symbol == symbol:
                return reading
        raise QiyasReadoutError(f"البوّابة «{symbol}» ليست في قراءة هذا الفرع")


class MinimalityStanding(Enum):
    """منزلةُ شرط الأدنويّة؛ غيرُ متماثلةٍ لأنّ الهدفَ غيرُ مستقلٍّ عن المُرخَّص."""

    DEFEATED_BY_A_TIE = "أسقطَه_تساوي_نموذجٍ_أضعف"
    UNDERPOWERED_BY_TARGET_PROVENANCE = "قاصرٌ_لأنّ_الهدفَ_من_قارئ_المُرخَّص_نفسِه"


@dataclass(frozen=True, slots=True)
class WeakerModelScore:
    """درجةُ نموذجٍ أضعفَ على الهدف نفسِه، ومعها ما أُعطِيه من سعةٍ مقصودة."""

    model_id: str
    hits: int
    attempts: int
    what_generosity_it_was_given: str


@dataclass(frozen=True, slots=True)
class MinimalityReading:
    """قراءةُ الأدنويّة: درجةُ المُرخَّص، ودرجاتُ الأضعف، والمنزلةُ المُشتقّة."""

    licensed_hits: int
    target_size: int
    weaker_scores: tuple[WeakerModelScore, ...]

    @property
    def standing(self) -> MinimalityStanding:
        """المنزلةُ مُشتقّةٌ لا مُخزَّنة؛ والتساوي يُسقِط والتفوّقُ لا يرفع."""

        if any(score.hits >= self.licensed_hits for score in self.weaker_scores):
            return MinimalityStanding.DEFEATED_BY_A_TIE
        return MinimalityStanding.UNDERPOWERED_BY_TARGET_PROVENANCE


@dataclass(frozen=True, slots=True)
class SurfaceReading:
    """قراءةُ صورةٍ مُجمَّدةٍ واحدة: فروعُها، وشروطُ المركز الأعلى عليها."""

    surface: str
    target_templates: tuple[str, ...]
    branches: tuple[BranchReading, ...]
    reconstruction: GateReading
    no_bypass: GateReading
    closure: GateReading
    identity: GateReading


@dataclass(frozen=True, slots=True)
class QiyasRun:
    """تشغيلٌ واحدٌ كاملٌ على الصور المُجمَّدة السبع؛ مخرجاتُه كما خرجت."""

    surfaces: tuple[SurfaceReading, ...]
    minimality: MinimalityReading
    unfired_outcomes: tuple[str, ...]
    analytic_gates: tuple[str, ...]

    def surface_named(self, surface: str) -> SurfaceReading:
        """أعِد قراءةَ صورةٍ بعينها؛ وغيرُ المقروءة تُرَدّ لا تُخترَع."""

        for reading in self.surfaces:
            if reading.surface == surface:
                return reading
        raise QiyasReadoutError(f"الصورة «{surface}» ليست في هذا التشغيل")

    def standing_for(self, surface: str) -> HigherCenterStanding:
        """منزلةُ المركز الأعلى لصورةٍ بعينها، مُشتقّةً من الشروط الأربعة معًا."""

        reading = self.surface_named(surface)
        local = (
            reading.reconstruction.holds
            and reading.no_bypass.holds
            and reading.closure.holds
            and reading.identity.holds
        )
        if not local:
            return HigherCenterStanding.WITHHELD
        if self.minimality.standing is MinimalityStanding.DEFEATED_BY_A_TIE:
            return HigherCenterStanding.WITHHELD
        return HigherCenterStanding.UNDERPOWERED


def _template_of_shape(nucleus_length: int, coda_count: int) -> str:
    return "C" + "V" * nucleus_length + "C" * coda_count


def _shape_of(syllable: Syllable) -> tuple[int, int]:
    nucleus = next(slot for slot in syllable.slots if slot.kind is SlotKind.VOWEL)
    coda = sum(
        1
        for index, slot in enumerate(syllable.slots)
        if slot.kind is SlotKind.CONSONANT and index > syllable.slots.index(nucleus)
    )
    return nucleus.length, coda


def _read_gates(
    syllable: Syllable,
    surface_is_resolved: bool,
    preventer_positions: frozenset[int],
) -> tuple[GateReading, ...]:
    nucleus_length, coda_count = _shape_of(syllable)
    has_onset = syllable.slots[0].kind is SlotKind.CONSONANT
    has_nucleus = any(slot.kind is SlotKind.VOWEL for slot in syllable.slots)
    touched = {slot.letter_index for slot in syllable.slots}
    preventers = sorted(touched & preventer_positions)
    counterfactual = _template_of_shape(
        1 if nucleus_length != 1 else 2, coda_count if coda_count != 0 else 1
    )
    return (
        GateReading(
            symbol="Sh",
            holds=surface_is_resolved,
            named_reason=(
                "قُطِّعت الصورةُ كلُّها بلا تعذّرٍ باقٍ"
                if surface_is_resolved
                else "بقي في الصورة تعذّرٌ مُسمًّى فلا يُقاس عليها"
            ),
        ),
        GateReading(
            symbol="Sb",
            holds=has_onset and has_nucleus,
            named_reason=(
                f"الفرعُ يفتتح بحاملٍ صامتٍ ونواتُه واحدةٌ طولُها {nucleus_length}"
                if has_onset and has_nucleus
                else "الفرعُ بلا حاملٍ مفتتِحٍ أو بلا نواة"
            ),
        ),
        GateReading(
            symbol="Mn",
            holds=not preventers,
            named_reason=(
                "لا دورَ مانعًا في مواضع الفرع"
                if not preventers
                else f"دورٌ مانعٌ في المواضع {tuple(preventers)}"
            ),
        ),
        GateReading(
            symbol=r"w^\*",
            holds=counterfactual != syllable.template.value,
            named_reason=(
                f"التبديلُ المضادُّ يُخرِج «{counterfactual}» بدل "
                f"«{syllable.template.value}»؛ والوصفُ مؤثِّرٌ بحكم دالّة "
                "القوالب نفسِها لا بحكم المدوّنة"
            ),
            is_analytic_in_this_deposit=True,
        ),
        GateReading(
            symbol=r"\mu",
            holds=has_onset and has_nucleus,
            named_reason=(
                "الأصلُ والفرعُ يشتركان في افتتاحٍ واحد: حاملٌ صامتٌ تليه نواةٌ؛ "
                "وهذا صادقٌ في القوالب الستّة كلِّها بحكم بنائها"
            ),
            is_analytic_in_this_deposit=True,
        ),
        GateReading(
            symbol=r"\Delta_q",
            holds=(nucleus_length, coda_count) != (1, 0),
            named_reason=(
                f"شكلُ الفرع (نواةٌ طولُها {nucleus_length}، صوامتُ إغلاقٍ "
                f"عددُها {coda_count}) مقابل شكل الأصل (1، 0)"
            ),
        ),
    )


def _outcome_for(gates: tuple[GateReading, ...], syllable: Syllable) -> QiyasOutcome:
    by_symbol = {reading.symbol: reading for reading in gates}
    if not by_symbol["Sh"].holds:
        return QiyasOutcome.BLOCK
    if not by_symbol["Sb"].holds:
        return QiyasOutcome.DEFER_OR_BLOCK
    if not by_symbol["Mn"].holds:
        return QiyasOutcome.BLOCK
    if not by_symbol[r"w^\*"].holds:
        return QiyasOutcome.NO_EFFECTIVE_DESCRIPTION
    if not by_symbol[r"\mu"].holds:
        return QiyasOutcome.NO_QIYAS
    if not by_symbol[r"\Delta_q"].holds:
        return QiyasOutcome.CONTINUITY_UNDER_ORIGIN
    nucleus_length, coda_count = _shape_of(syllable)
    collapsed = _template_of_shape(1, 0)
    difference_is_effective = (
        collapsed == _ORIGIN_TEMPLATE
        and _template_of_shape(nucleus_length, coda_count) != _ORIGIN_TEMPLATE
    )
    if not difference_is_effective:
        return QiyasOutcome.FORMAL_DIFFERENCE_ONLY
    return QiyasOutcome.INDEPENDENT_BRANCH_CANDIDATE


def _bypass_sequence(states: tuple[str, ...]) -> tuple[str, ...]:
    return tuple("CV" for state in states if not state.startswith("sukun"))


def _best_constant(targets: tuple[str, ...], emissions: int) -> tuple[str, int]:
    if not targets:
        return ("CV", 0)
    best_template = ""
    best_hits = -1
    for candidate in sorted(set(targets)):
        hits = sum(
            1
            for index in range(min(emissions, len(targets)))
            if targets[index] == candidate
        )
        if hits > best_hits:
            best_template, best_hits = candidate, hits
    return (best_template, best_hits)


def _fit_state_map(
    pairs: tuple[tuple[str, str], ...],
) -> dict[str, str]:
    grouped: dict[str, Counter[str]] = {}
    for state, template in pairs:
        grouped.setdefault(state, Counter())[template] += 1
    return {
        state: sorted(counter.items(), key=lambda item: (-item[1], item[0]))[0][0]
        for state, counter in grouped.items()
    }


def read_qiyas(sealed: SealedQiyasPreregistration) -> QiyasRun:
    """اقرأ الصورَ المُجمَّدةَ على قانون القياس، وأخرِج ما يخرج بلا ضبط."""

    _require_intact_seal(sealed)

    readings: list[SurfaceReading] = []
    licensed_hits = 0
    target_size = 0
    carrier_alone_hits = 0
    carrier_alone_attempts = 0
    unordered_hits = 0
    unordered_attempts = 0
    state_pairs: list[tuple[tuple[str, str], ...]] = []
    state_sequences: list[tuple[tuple[str, ...], tuple[str, ...]]] = []

    for frozen in FLT1_FROZEN_SURFACES:
        surface = frozen.surface
        reading = read_surface(surface)
        word = syllabify_reading(reading)
        slots, expansion_failure = expand_slots(reading)
        preventer_positions = frozenset(
            letter.index
            for letter in reading.letters
            if set(letter.roles) & PREVENTER_ROLES
        )
        targets = tuple(syllable.template.value for syllable in word.syllables)
        target_size += len(targets)
        licensed_hits += len(targets)

        branches = tuple(
            BranchReading(
                surface=surface,
                branch_index=index,
                template=syllable.template.value,
                gates=gates,
                outcome=_outcome_for(gates, syllable),
            )
            for index, syllable, gates in (
                (
                    position,
                    syllable,
                    _read_gates(syllable, word.is_resolved, preventer_positions),
                )
                for position, syllable in enumerate(word.syllables)
            )
        )

        entered: list[int] = []
        for syllable in word.syllables:
            for slot in syllable.slots:
                if slot.letter_index not in entered:
                    entered.append(slot.letter_index)
        expected = list(range(len(reading.letters)))
        reconstruction = GateReading(
            symbol="Reconstruction",
            holds=entered == expected,
            named_reason=(
                f"المراكزُ المُستخرَجةُ من المقاطع {tuple(entered)} مقابل "
                f"مواضع الوحدات الداخلة {tuple(expected)}"
            ),
        )

        states = tuple(letter.unit.state.value for letter in reading.letters)
        bypass = _bypass_sequence(states)
        no_bypass = GateReading(
            symbol="NoBypass",
            holds=bypass != targets,
            named_reason=(
                f"مسارُ «لا وصل» يُخرِج {bypass} والهدفُ {targets}"
                + ("؛ فافترقا" if bypass != targets else "؛ فتطابقا والوصلُ زينة")
            ),
        )

        covered = {
            slot.letter_index for syllable in word.syllables for slot in syllable.slots
        }
        closure = GateReading(
            symbol="Closure",
            holds=covered == set(expected),
            named_reason=(
                "كلُّ موضعٍ في الصورة واقعٌ في مقطعٍ وكلُّ قالبٍ من الستّة"
                if covered == set(expected)
                else "مواضعُ خارجةٌ عن المقاطع: "
                f"{tuple(sorted(set(expected) - covered))}"
            ),
        )

        expanded_positions = tuple(slot.letter_index for slot in slots)
        segmented_positions = tuple(
            slot.letter_index for syllable in word.syllables for slot in syllable.slots
        )
        identity = GateReading(
            symbol="I",
            holds=(
                expansion_failure is None and expanded_positions == segmented_positions
            ),
            named_reason=(
                f"مواضعُ التوسيع {expanded_positions} ومواضعُ التقطيع "
                f"{segmented_positions}"
            ),
        )

        readings.append(
            SurfaceReading(
                surface=surface,
                target_templates=targets,
                branches=branches,
                reconstruction=reconstruction,
                no_bypass=no_bypass,
                closure=closure,
                identity=identity,
            )
        )

        carriers = tuple(letter.unit.carrier for letter in reading.letters)
        _, hits = _best_constant(targets, len(carriers))
        carrier_alone_hits += hits
        carrier_alone_attempts += min(len(carriers), len(targets))

        _, unordered = _best_constant(targets, len(targets))
        unordered_hits += unordered
        unordered_attempts += len(targets)

        state_sequences.append((states, targets))
        state_pairs.append(
            tuple(
                (states[index], targets[index])
                for index in range(min(len(states), len(targets)))
            )
        )

    fitted = _fit_state_map(tuple(pair for group in state_pairs for pair in group))
    state_alone_hits = 0
    state_alone_attempts = 0
    for states, targets in state_sequences:
        for index in range(min(len(states), len(targets))):
            state_alone_attempts += 1
            if fitted.get(states[index]) == targets[index]:
                state_alone_hits += 1

    generosity = {
        "carrier-alone": (
            "أُعطِي أفضلَ قالبٍ ثابتٍ لكلّ صورةٍ يُختار بعد رؤية الهدف؛ وهي "
            "سعةٌ في صالحه لا في صالح الدعوى"
        ),
        "state-alone": (
            "أُعطِي أفضلَ تقابلٍ بين الحالة والقالب يُلائَم على المدوّنة "
            "كلِّها بعد رؤية الهدف"
        ),
        "unordered-carrier-state-pair": (
            "أُعطِي عددَ المقاطع وأفضلَ قالبٍ ثابتٍ لكلّ صورة، مع أنّ المجموعةَ "
            "غيرَ المرتَّبة لا تُعطي العددَ من نفسها"
        ),
    }
    scores = tuple(
        WeakerModelScore(
            model_id=model.model_id,
            hits=hits,
            attempts=attempts,
            what_generosity_it_was_given=generosity[model.model_id],
        )
        for model, hits, attempts in (
            (WEAKER_REPRESENTATIONS[0], carrier_alone_hits, carrier_alone_attempts),
            (WEAKER_REPRESENTATIONS[1], state_alone_hits, state_alone_attempts),
            (WEAKER_REPRESENTATIONS[2], unordered_hits, unordered_attempts),
        )
    )

    fired = {branch.outcome for reading in readings for branch in reading.branches}
    unfired = tuple(
        sorted(
            {rule.outcome.value for rule in DECISION_RULES}
            - {outcome.value for outcome in fired}
        )
    )

    return QiyasRun(
        surfaces=tuple(readings),
        minimality=MinimalityReading(
            licensed_hits=licensed_hits,
            target_size=target_size,
            weaker_scores=scores,
        ),
        unfired_outcomes=unfired,
        analytic_gates=ANALYTIC_GATE_SYMBOLS,
    )


THE_TARGET_COMES_FROM_THE_SAME_READER_NOTE: Final[str] = (
    "TheTargetComesFromTheSameReaderAsTheLicensedModel: هدفُ إعادة البناء "
    "مأخوذٌ من المُقطِّع نفسِه؛ فتفوّقُ المُرخَّص مضمونٌ بالبناء ولا يُعَدّ "
    "شاهدًا، وتساوي نموذجٍ أضعفَ يُسقِط الدعوى إسقاطًا"
)

ANALYTIC_GATES_CARRY_NO_DISCRIMINATING_WEIGHT_NOTE: Final[str] = (
    r"AnalyticGatesCarryNoDiscriminatingWeight: `w^\*` و`\mu` صادقتان بحكم "
    "دالّة القوالب لا بحكم المدوّنة؛ فتُقرأان ولا تُحسَبان إصابةً"
)

AN_UNFIRED_RULE_IS_AN_UNTESTED_RULE_NOTE: Final[str] = (
    "AnUnfiredRuleIsAnUntestedRule: مخرجٌ مُسجَّلٌ لم تُطلِقه المدوّنةُ "
    "المُجمَّدة يُعَدّ غيرَ مُختبَر، ولا يُعَدّ سكوتُه نجاحًا"
)

QIYAS_READOUT_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_TARGET_COMES_FROM_THE_SAME_READER_NOTE,
    ANALYTIC_GATES_CARRY_NO_DISCRIMINATING_WEIGHT_NOTE,
    AN_UNFIRED_RULE_IS_AN_UNTESTED_RULE_NOTE,
)


def _refuse_a_readout_on_a_drifted_text() -> None:
    if qiyas_text_digest() != FLT1_QIYAS_TEXT_DIGEST:
        raise QiyasReadoutError("نصُّ القانون انزاح؛ ولا تُبنى قراءةٌ على نصٍّ مُبدَّل")


_refuse_a_readout_on_a_drifted_text()
