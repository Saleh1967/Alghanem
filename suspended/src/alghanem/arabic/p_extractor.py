"""قراءةُ P-EXTRACTOR: أدوارٌ تُعلَّق على وحدات المرماز القائم، لا حالاتٌ جديدة.

هذه الوحدةُ تُنفّذ المرورَ الثاني من §٢ في المواصفة المُودَعة، **بالترتيب
المُجمَّد** في `p_extractor_preregistration.PASS_TWO_RULES` ولا تتجاوزه بقاعدة.
وتُطابِق عند الاستيراد أسماءَ القواعد المُنفَّذة بأسماء المُسجَّلة وترتيبَها،
فلا تُطبَّق قاعدةٌ لم تُسجَّل ولا تُهمَل قاعدةٌ سُجِّلت
(`THE_IMPLEMENTED_ORDER_IS_CHECKED_AGAINST_THE_FROZEN_ONE`).

`A_ROLE_IS_NOT_A_STATE`: لا عضوَ يُزاد إلى `CarrierState`؛ الأدوارُ مفردةٌ
مستقلّةٌ مغلقةٌ بخمسةِ أعضاء تُعلَّق على `CarrierStateUnit` كما وردت من
المرماز. والوحداتُ تخرج من هذه القراءة **كما دخلت**، فطريقُ العودة إلى الصورة
هو طريقُ المرماز نفسُه ولم يُحدَث له طريقٌ ثانٍ
(`THE_READING_ADDS_ROLES_AND_TOUCHES_NO_UNIT`). وهذا وحدَه ما يجعل أرضيّةَ
القبول المكتوبةَ قبلُ محفوظةً **بنيويًّا** لا بقياسٍ يُعاد كلَّ مرّة: ما لم
تُمَسّ وحدةٌ لم تنقص نسبةُ الذهاب والإياب ولم تُفسَد كلمةٌ كانت سليمة.

`REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY`: غموضُ «جذرٌ أم مدّ» يخرج في
`PExtractorReading.ambiguities` سجلًّا مستقلًّا، ومتعذّرُ همزة الوصل يخرج في
`PExtractorReading.undecided` موضعًا مُسمًّى. وليس واحدٌ منهما دورًا، ولا
يدخل واحدٌ منهما مفردةَ الأدوار.

`HARAKA_BEARING_IS_A_DERIVED_PREDICATE`: حملُ الحركة الحقيقيّة يُشتَقّ عند
السؤال من الحالة والأدوار بنصّ التعريف المُجمَّد في
`p_extractor_preregistration.HARAKA_BEARING_DEFINITION`، ولا يُخزَّن حقلًا.

`THE_READING_IS_BOUNDED_BY_ONE_SURFACE`: تُقرأ الصورةُ الواحدةُ وحدَها. فما
احتاج إلى ما قبلها أو بعدها من الكلام — كالوقف والوصل وفواتح السور — لا يُقرأ
هنا ولا يُفتَرض، و«آخرُ الكلمة» في هذه الوحدة آخرُ الصورة المُدخَلة لا آخرُ
نطقٍ في سياق.

`THIS_IS_A_READING_NOT_A_BIRTH`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا استيرادَ من `kernel/`، ولا تُرفَع بهذه القراءةِ حواجزُ المخرج/الصفة
ولا حاجزُ «أل».
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import (
    CarrierSeat,
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
    GeminationRole,
)
from .gflk_state_machine_registration import (
    UNRESOLVABLE_PROPOSALS,
    UnresolvableProposal,
)
from .p_extractor_preregistration import (
    PASS_TWO_RULES,
    PREREGISTRATION_DIGEST,
    RuleEmission,
)

__all__ = [
    "AMBIGUOUS_PROPOSAL",
    "SILENCING_ROLES",
    "THE_IMPLEMENTED_ORDER_IS_CHECKED_AGAINST_THE_FROZEN_ONE_NOTE",
    "THE_READING_ADDS_ROLES_AND_TOUCHES_NO_UNIT_NOTE",
    "THIS_IS_A_READING_NOT_A_BIRTH_NOTE",
    "AmbiguityRecord",
    "LetterReading",
    "PExtractorError",
    "PExtractorReading",
    "PhoneticRole",
    "UndecidedSite",
    "read_surface",
    "reading_preserves_the_round_trip",
    "retrieve_surface",
]


class PExtractorError(ValueError):
    """رفضٌ عند الإنشاء: دورٌ مكرَّر، أو قراءةٌ لا تُطابق التسجيلَ القبْليّ."""


class PhoneticRole(Enum):
    """الأدوارُ الخمسةُ التي تُعلَّق على وحدةٍ قائمة. مفردةٌ مغلقةٌ لا سادسَ لها.

    وليست هذه حالاتٍ: الوحدةُ تحمل حالتَها من `CarrierState`، والدورُ وصفُ ما
    تؤدّيه في سياق صورتها. ومن جعل الدورَ حالةً صيّر الوحدةَ الواحدةَ عضوين.
    """

    MADD_EXTENSION = "مدٌّ يمتدّ به صائتٌ سابق"
    TANWEEN_ALIF_CARRIER = "مَقعدُ ألفٍ استهلكه تنوينُ الفتح"
    ASSIMILATED_SILENT = "مُدغَمٌ ساكتٌ في تاليه"
    SILENT_DIFFERENTIATING_ALIF = "ألفٌ فارقةٌ لا تُنطَق"
    SHADDA_PAIR_START = "النصفُ الأوّلُ من زوج تضعيف"


SILENCING_ROLES: Final[frozenset[PhoneticRole]] = frozenset(
    {
        PhoneticRole.ASSIMILATED_SILENT,
        PhoneticRole.MADD_EXTENSION,
        PhoneticRole.SILENT_DIFFERENTIATING_ALIF,
    }
)
"""الأدوارُ التي تمنع قراءةَ الوحدة حاملةَ حركةٍ حقيقيّة، بنصّ التعريف المُجمَّد."""


AMBIGUOUS_PROPOSAL: Final[UnresolvableProposal] = UNRESOLVABLE_PROPOSALS[0]
"""المقترحُ المتعذّرُ، مقروءًا من تسجيله السابق لا مُنشأً هنا من جديد."""


_WEAK_LETTERS: Final[frozenset[str]] = frozenset({"\u0648", "\u064a"})
_ALEF: Final[str] = "\u0627"
_WAW: Final[str] = "\u0648"
_YEH: Final[str] = "\u064a"
_LAM: Final[str] = "\u0644"

_MADD_PARTNERS: Final[dict[str, CarrierState]] = {
    _ALEF: CarrierState.FATHA,
    _WAW: CarrierState.DAMMA,
    _YEH: CarrierState.KASRA,
}

_SHORT_VOWELS: Final[frozenset[CarrierState]] = frozenset(
    {CarrierState.FATHA, CarrierState.DAMMA, CarrierState.KASRA}
)


@dataclass(frozen=True, slots=True)
class LetterReading:
    """وحدةٌ واحدةٌ كما خرجت من المرماز، ومعها أدوارُها في صورتها.

    الوحدةُ منقولةٌ بعينها لا مُعادةَ البناء، فحقلُها `unit` هو ما يُعاد إلى
    المرماز عند الكتابة، ولا طريقَ ثانيًا للعودة إلى الصورة.
    """

    index: int
    unit: CarrierStateUnit
    roles: tuple[PhoneticRole, ...] = ()

    def __post_init__(self) -> None:
        if isinstance(self.index, bool) or not isinstance(self.index, int):
            raise PExtractorError("موضعُ الوحدة عددٌ صحيح")
        if self.index < 0:
            raise PExtractorError("موضعُ الوحدة عددٌ غيرُ سالب")
        if not isinstance(self.unit, CarrierStateUnit):
            raise PExtractorError("الوحدةُ من `CarrierStateUnit` لا من مفردةٍ مُبتكَرة")
        for role in self.roles:
            if not isinstance(role, PhoneticRole):
                raise PExtractorError("الدورُ عضوٌ في مفردته المغلقة")
        if len(set(self.roles)) != len(self.roles):
            raise PExtractorError(
                "دورٌ تكرّر على وحدةٍ واحدة؛ والتكرارُ يُضاعف قراءةً واحدةً " "فتُقرأ شاهدين"
            )

    @property
    def is_haraka_bearing(self) -> bool:
        """أتحمل هذه الوحدةُ حركةً حقيقيّة؟ مُشتَقٌّ عند السؤال لا مُخزَّن."""

        if self.unit.state not in _SHORT_VOWELS:
            return False
        return not any(role in SILENCING_ROLES for role in self.roles)

    def has_role(self, role: PhoneticRole) -> bool:
        """أعُلِّق هذا الدورُ على هذه الوحدة؟"""

        return role in self.roles

    def with_role(self, role: PhoneticRole) -> LetterReading:
        """قراءةٌ جديدةٌ بالدور مضافًا؛ والوحدةُ نفسُها لا تُمَسّ."""

        if role in self.roles:
            return self
        return LetterReading(self.index, self.unit, (*self.roles, role))


@dataclass(frozen=True, slots=True)
class AmbiguityRecord:
    """سجلُّ غموضٍ في حقلٍ منفصل، لا عضوٌ في مفردة الأدوار.

    والمقترحُ مقروءٌ من `gflk_state_machine_registration.UNRESOLVABLE_PROPOSALS`
    لا مُنشأٌ هنا، فسببُ التعذّر وموضعُه المكتوبان قبلُ هما نفسُهما ما يُقرأ
    بعدُ.
    """

    index: int
    proposal: UnresolvableProposal
    madd_index: int
    tanween_index: int

    def __post_init__(self) -> None:
        if not isinstance(self.proposal, UnresolvableProposal):
            raise PExtractorError("المقترحُ المتعذّرُ من نوعه المُسجَّل لا من نصٍّ حرّ")
        for number, label in (
            (self.index, "موضعُ السجلّ"),
            (self.madd_index, "موضعُ المدّ"),
            (self.tanween_index, "موضعُ حامل التنوين"),
        ):
            if isinstance(number, bool) or not isinstance(number, int) or number < 0:
                raise PExtractorError(f"{label} عددٌ صحيحٌ غيرُ سالب")

    @property
    def proposed_name(self) -> str:
        """اسمُ المقترح، مقروءًا من تسجيله لا مكتوبًا هنا."""

        return self.proposal.proposed_name


@dataclass(frozen=True, slots=True)
class UndecidedSite:
    """موضعٌ لا تحسمه العلاماتُ المكتوبة، بقاعدته ومرجع تعذّره."""

    index: int
    rule_name: str
    why_it_is_undecided: str
    tree_reference: str

    def __post_init__(self) -> None:
        if isinstance(self.index, bool) or not isinstance(self.index, int):
            raise PExtractorError("موضعُ التعذّر عددٌ صحيح")
        if self.index < 0:
            raise PExtractorError("موضعُ التعذّر عددٌ غيرُ سالب")
        for value, label in (
            (self.rule_name, "اسمُ القاعدة"),
            (self.why_it_is_undecided, "سببُ التعذّر"),
            (self.tree_reference, "مرجعُ التعذّر في الشجرة"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise PExtractorError(f"{label} نصٌّ غير فارغ")


@dataclass(frozen=True, slots=True)
class PExtractorReading:
    """قراءةُ صورةٍ واحدة: وحداتُها بأدوارها، وغموضُها، ومتعذّرُها.

    الحقولُ الثلاثةُ أجناسٌ مختلفةٌ لا تُجمَع: الدورُ مقروءٌ، والغموضُ
    مرصودٌ غيرُ محسوم، والتعذّرُ ليس شيئًا قِيس فكان لا شيء.
    """

    surface: str
    letters: tuple[LetterReading, ...]
    ambiguities: tuple[AmbiguityRecord, ...] = ()
    undecided: tuple[UndecidedSite, ...] = ()
    preregistration_digest: str = PREREGISTRATION_DIGEST

    def __post_init__(self) -> None:
        if not isinstance(self.surface, str):
            raise PExtractorError("الصورةُ نصّ")
        if tuple(reading.index for reading in self.letters) != tuple(
            range(len(self.letters))
        ):
            raise PExtractorError(
                "مواضعُ الوحدات متّصلةٌ من الصفر؛ وفجوةٌ فيها تُخفي وحدةً قُرِئت"
            )
        if self.preregistration_digest != PREREGISTRATION_DIGEST:
            raise PExtractorError(
                "قراءةٌ ببصمةِ تسجيلٍ غيرِ البصمة القائمة قراءةٌ بترتيبِ قواعدَ " "آخر"
            )

    @property
    def units(self) -> tuple[CarrierStateUnit, ...]:
        """الوحداتُ كما خرجت من المرماز، بلا زيادةٍ ولا نقص."""

        return tuple(reading.unit for reading in self.letters)

    @property
    def haraka_bearing(self) -> tuple[LetterReading, ...]:
        """الوحداتُ الحاملةُ حركةً حقيقيّة، مُشتقّةً لا مُخزَّنة."""

        return tuple(reading for reading in self.letters if reading.is_haraka_bearing)

    def roles_at(self, index: int) -> tuple[PhoneticRole, ...]:
        """أدوارُ الوحدة في موضعٍ بعينه."""

        return self.letters[index].roles


_CODEC: Final[CarrierStateCodec] = CarrierStateCodec()


def _pair_start_after(
    readings: Sequence[LetterReading], index: int
) -> LetterReading | None:
    """النصفُ الأوّلُ من زوج تضعيفٍ يلي هذا الموضعَ مباشرةً، إن وُجد."""

    if index + 1 >= len(readings):
        return None
    following = readings[index + 1]
    if following.unit.gemination is GeminationRole.PAIR_START:
        return following
    return None


def _is_bare(unit: CarrierStateUnit) -> bool:
    """وحدةٌ ساكنةٌ ضمنًا بلا تنوينٍ ولا تضعيف: ما تسمّيه المواصفةُ `PENDING`."""

    return (
        unit.state is CarrierState.SUKUN_IMPLICIT
        and not unit.tanwin
        and unit.gemination is None
    )


def _apply_idgham(readings: list[LetterReading]) -> None:
    for index, reading in enumerate(readings):
        if not _is_bare(reading.unit):
            continue
        pair_start = _pair_start_after(readings, index)
        if pair_start is None or pair_start.unit.carrier == reading.unit.carrier:
            continue
        readings[index] = reading.with_role(PhoneticRole.ASSIMILATED_SILENT)


def _apply_doubled_weak_idgham(readings: list[LetterReading]) -> None:
    for index, reading in enumerate(readings):
        if not _is_bare(reading.unit) or reading.unit.carrier not in _WEAK_LETTERS:
            continue
        pair_start = _pair_start_after(readings, index)
        if pair_start is None or pair_start.unit.carrier != reading.unit.carrier:
            continue
        readings[index] = reading.with_role(PhoneticRole.ASSIMILATED_SILENT)


def _apply_tanween_alif_carrier(readings: list[LetterReading]) -> None:
    for index, reading in enumerate(readings):
        if reading.unit.tanwin_alif_seat:
            readings[index] = reading.with_role(PhoneticRole.TANWEEN_ALIF_CARRIER)
            continue
        if not _is_bare(reading.unit) or reading.unit.carrier != _ALEF:
            continue
        if reading.unit.seat is not None or index == 0:
            continue
        previous = readings[index - 1].unit
        if previous.tanwin and previous.state is CarrierState.FATHA:
            readings[index] = reading.with_role(PhoneticRole.TANWEEN_ALIF_CARRIER)


def _apply_madd_extension(readings: list[LetterReading]) -> None:
    for index, reading in enumerate(readings):
        unit = reading.unit
        if unit.seat is CarrierSeat.MADD:
            readings[index] = reading.with_role(PhoneticRole.MADD_EXTENSION)
            continue
        if unit.seat is not None or not _is_bare(unit):
            continue
        if reading.has_role(PhoneticRole.TANWEEN_ALIF_CARRIER):
            continue
        partner = _MADD_PARTNERS.get(unit.carrier)
        if partner is None or index == 0:
            continue
        previous = readings[index - 1].unit
        if previous.state is partner and not previous.tanwin:
            readings[index] = reading.with_role(PhoneticRole.MADD_EXTENSION)


def _apply_wasl_lam(readings: list[LetterReading]) -> tuple[UndecidedSite, ...]:
    if len(readings) < 2:
        return ()
    first, second = readings[0], readings[1]
    if (
        first.unit.carrier != _ALEF
        or first.unit.seat is not None
        or first.unit.state is not CarrierState.SUKUN_IMPLICIT
        or first.unit.tanwin
    ):
        return ()
    if second.unit.carrier != _LAM:
        return ()
    return (
        UndecidedSite(
            index=0,
            rule_name="WASL_LAM",
            why_it_is_undecided=(
                "الألفُ العاريةُ لا تحمل علامةً تُميّز همزةَ الوصل من غيرها، "
                "وفرعُ الشمسيّة/القمريّة تحتها؛ فالموضعُ يُسمّى ولا يُخمَّن"
            ),
            tree_reference=(
                "ibtida_wasl_waqf_registration."
                "HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS"
            ),
        ),
    )


def _apply_silent_differentiating_alif(readings: list[LetterReading]) -> None:
    if len(readings) < 2:
        return
    index = len(readings) - 1
    reading = readings[index]
    unit = reading.unit
    if unit.carrier != _ALEF or unit.seat is not None or not _is_bare(unit):
        return
    previous = readings[index - 1]
    if previous.unit.carrier != _WAW:
        return
    if not previous.has_role(PhoneticRole.MADD_EXTENSION):
        return
    readings[index] = reading.with_role(PhoneticRole.SILENT_DIFFERENTIATING_ALIF)


def _apply_shadda_pair_start(readings: list[LetterReading]) -> None:
    for index, reading in enumerate(readings):
        if reading.unit.gemination is GeminationRole.PAIR_START:
            readings[index] = reading.with_role(PhoneticRole.SHADDA_PAIR_START)


def _apply_madd_tanween_ambiguity(
    readings: list[LetterReading],
) -> tuple[AmbiguityRecord, ...]:
    records: list[AmbiguityRecord] = []
    for index in range(len(readings) - 1):
        current, following = readings[index], readings[index + 1]
        if not current.has_role(PhoneticRole.MADD_EXTENSION):
            continue
        if not following.has_role(PhoneticRole.TANWEEN_ALIF_CARRIER):
            continue
        records.append(
            AmbiguityRecord(
                index=index,
                proposal=AMBIGUOUS_PROPOSAL,
                madd_index=index,
                tanween_index=index + 1,
            )
        )
    return tuple(records)


_RoleRule = Callable[[list[LetterReading]], None]
_AmbiguityRule = Callable[[list[LetterReading]], tuple[AmbiguityRecord, ...]]
_UndecidedRule = Callable[[list[LetterReading]], tuple[UndecidedSite, ...]]

_ROLE_RULES: Final[dict[str, _RoleRule]] = {
    "IDGHAM": _apply_idgham,
    "DOUBLED_WEAK_IDGHAM": _apply_doubled_weak_idgham,
    "TANWEEN_ALIF_CARRIER": _apply_tanween_alif_carrier,
    "MADD_EXTENSION": _apply_madd_extension,
    "SILENT_DIFFERENTIATING_ALIF": _apply_silent_differentiating_alif,
    "SHADDA_PAIR_START": _apply_shadda_pair_start,
}

_AMBIGUITY_RULES: Final[dict[str, _AmbiguityRule]] = {
    "MADD_TANWEEN_AMBIGUITY": _apply_madd_tanween_ambiguity,
}

_UNDECIDED_RULES: Final[dict[str, _UndecidedRule]] = {
    "WASL_LAM": _apply_wasl_lam,
}


def _refuse_an_unregistered_implementation() -> None:
    """حارسٌ عند الاستيراد: المُنفَّذُ هو المُسجَّلُ بعينه وبترتيبه."""

    implemented: dict[str, RuleEmission] = {}
    for name in _ROLE_RULES:
        implemented[name] = RuleEmission.ROLE_OVER_AN_EXISTING_UNIT
    for name in _AMBIGUITY_RULES:
        implemented[name] = RuleEmission.AMBIGUITY_RECORD
    for name in _UNDECIDED_RULES:
        implemented[name] = RuleEmission.UNDECIDED_SITE
    registered = {rule.name: rule.emission for rule in PASS_TWO_RULES}
    if implemented != registered:
        raise PExtractorError(
            "المُنفَّذُ يخالف المُسجَّلَ في الأسماء أو في أجناس المُخرَجات؛ "
            "وقاعدةٌ تُطبَّق بلا تسجيلٍ قاعدةٌ لا شرطَ قبولٍ مكتوبٌ لها"
        )
    for rule in PASS_TWO_RULES:
        if rule.emission is RuleEmission.ROLE_OVER_AN_EXISTING_UNIT:
            name = rule.emitted_role_name or ""
            if name not in PhoneticRole.__members__:
                raise PExtractorError(
                    f"الدورُ المُسجَّل {name!r} ليس عضوًا في مفردة الأدوار المغلقة"
                )


_refuse_an_unregistered_implementation()


def read_surface(surface: str) -> PExtractorReading:
    """اقرأ صورةً واحدةً: وحداتُها بأدوارها، وغموضُها، ومتعذّرُها.

    الوحداتُ من `CarrierStateCodec.generate` بأعيانها، والقواعدُ تُطبَّق
    بالترتيب المُجمَّد؛ فالقراءةُ دالّةٌ خالصةٌ لا تحتفظ بحالٍ بين ندائين.
    """

    units = _CODEC.generate(surface)
    readings = [LetterReading(index, unit) for index, unit in enumerate(units)]
    ambiguities: list[AmbiguityRecord] = []
    undecided: list[UndecidedSite] = []
    for rule in PASS_TWO_RULES:
        if rule.emission is RuleEmission.ROLE_OVER_AN_EXISTING_UNIT:
            _ROLE_RULES[rule.name](readings)
        elif rule.emission is RuleEmission.AMBIGUITY_RECORD:
            ambiguities.extend(_AMBIGUITY_RULES[rule.name](readings))
        else:
            undecided.extend(_UNDECIDED_RULES[rule.name](readings))
    return PExtractorReading(
        surface=surface,
        letters=tuple(readings),
        ambiguities=tuple(ambiguities),
        undecided=tuple(undecided),
    )


def retrieve_surface(reading: PExtractorReading) -> str:
    """أعِد الصورةَ من وحدات القراءة، بطريق المرماز نفسِه لا بطريقٍ ثانٍ."""

    return _CODEC.retrieve(reading.units)


def reading_preserves_the_round_trip(surface: str) -> bool:
    """أتُعيد القراءةُ ما يُعيده المرمازُ نفسُه على هذه الصورة؟ مُشتَقٌّ لا مقولٌ."""

    reading = read_surface(surface)
    return retrieve_surface(reading) == _CODEC.retrieve(_CODEC.generate(surface))


THE_IMPLEMENTED_ORDER_IS_CHECKED_AGAINST_THE_FROZEN_ONE_NOTE: Final[str] = (
    "TheImplementedOrderIsCheckedAgainstTheFrozenOne: أسماءُ القواعد المُنفَّذة "
    "وأجناسُ مُخرَجاتها تُطابَق عند الاستيراد بالمُسجَّلة قبلُ؛ فلا تُطبَّق "
    "قاعدةٌ بلا شرطِ قبولٍ مكتوب، ولا تُهمَل قاعدةٌ سُجِّل شرطُها"
)

THE_READING_ADDS_ROLES_AND_TOUCHES_NO_UNIT_NOTE: Final[str] = (
    "TheReadingAddsRolesAndTouchesNoUnit: الوحداتُ تخرج كما دخلت، وطريقُ "
    "العودة إلى الصورة طريقُ المرماز نفسُه؛ فأرضيّةُ القبول محفوظةٌ بنيويًّا "
    "لا برقمٍ يُعاد قياسُه بعد كلّ تحرير"
)

THIS_IS_A_READING_NOT_A_BIRTH_NOTE: Final[str] = (
    "قراءةٌ لا ولادة: لا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ من "
    "`kernel/`، ولا تُرفَع بها حواجزُ المخرج/الصفة ولا حاجزُ «أل»"
)
