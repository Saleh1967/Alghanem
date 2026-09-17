"""قياسُ فضاء الرصد لكلّ حامل: صفٌّ لكلّ وقوع، وحالةٌ بمحاورها لا بقيمةٍ مسطّحة.

هذه الوحدةُ **قياسٌ لا حكم**: تقرأ سطورَ مدوّنةٍ مُودَعةٍ ببصمتها، وتُخرِج
لكلّ ذرّةٍ (حامل، حالة) صفًّا كاملًا، ثمّ تشتقّ منه لكلّ حاملٍ ليفَه المرصود.
ولا تُصدِر حكمًا، ولا تُرخِّص حالةً، ولا تمنعها.

**والحالةُ تُقرأ بمخطَّطها المُجمَّد لا بمجموعةٍ مسطّحة.** المخطَّطُ مُعلَنٌ في
`carrier_fiber_preregistration` قبل أيّ عدّ، والحالةُ هنا **مُتَّجِهٌ على
المحاور المقيسة**:

    state(atom) = (vowel, nunation, gemination, quiescence)

وقيمةُ الغياب عضوٌ في كلّ محورٍ لا طرحٌ من الحساب. والمحورُ المؤجَّل — المدُّ —
لا يدخل هذا المتَّجِه أصلًا، ويُحفَظ وقوعُه في حقلٍ مُسمًّى على الصفّ لا
يُطرَح (`DEFERRED_AXIS_MARKS_ARE_KEPT_NOT_DROPPED`).

**وما يُصنَع من الترميز يُسمّى قبل أن يُقرأ نتيجة.** اجتماعُ علامتين من محورين
على حاملٍ واحد — الشدّةُ مع الحركة مثلًا — يُشتَقّ صفًّا في
`derive_cross_axis_cooccurrences`، وهو شاهدٌ على أنّ المحورين ليسا قيمتين
متنافيتين في محورٍ واحد. وخرقُ التنافي **داخلَ** المحور الواحد يُحفَظ كذلك في
`axis_exclusivity_violations`، لا يُطرَح ولا يُلخَّص رقمًا
(`AN_EXCLUSIVITY_VIOLATION_IS_A_ROW_NOT_A_CORRECTION`).

**وما يُفنَّد هنا مُقيَّدٌ بنطاقه حرفًا بحرف.** ما تُخرِجه هذه الوحدةُ من شاهدٍ
هو:

    E_observed ≠ C × S_observed-global      (في هذه المدوّنة وهذا الترميز)

ولا شيءَ أوسع. أمّا:

    E_licensed = ⨆_c S_licensed(c)

فما يزال فرضيةً لا يقولها رصدٌ (`OBSERVED_FIBER_IS_NOT_LICENSED_FIBER`)؛
والانتقالُ من التفنيد إلى بنيةٍ ليفيةٍ حقيقيةٍ يحتاج `π: E → C` بليفٍ مرخَّصٍ
لا مرصود، ولا تُنشِئه هذه الوحدة.

**والمدوّنةُ مدخلٌ لا مُثبَتٌ في الكود.** `read_corpus_lines` تأخذ بايتاتِ أيّ
مدوّنةٍ مع بصمتها المنتظَرة وتردُّ ما خالفها؛ والفاتحةُ المُودَعةُ تُشغَّل
بوصفها `CALIBRATION_WITNESS` لا اختبارًا حاسمًا، فلا يمنع غيابُ بايتات مدوّنةٍ
أكبر تشغيلَ الشجرة (`A_CALIBRATION_RUN_IS_NOT_A_DECISIVE_RUN`).

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا
تقرؤها بوّابةٌ في `kernel/`، ولا تستورد طبقةَ البرنامج.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Final, Literal

from ..canonical_content import canonical_digest
from .alif_state_raw_count import (
    AlifStateRawCountTable,
    CarrierAtomRow,
    count_alif_states,
)
from .carrier_fiber_preregistration import (
    CARRIER_FIBER_STATE_SCHEMA,
    StateAxisDeclaration,
    StateSchema,
)
from .fatiha_source_text import (
    FATIHA_LINES,
    FATIHA_SOURCE_ID,
    NORMALIZATION_FORM,
    source_byte_length,
    source_sha256,
)

__all__ = [
    "ABSENT",
    "AN_EXCLUSIVITY_VIOLATION_IS_A_ROW_NOT_A_CORRECTION",
    "A_CALIBRATION_RUN_IS_NOT_A_DECISIVE_RUN",
    "CARRIER_STATE_OBSERVED_FIBER_NAMED_RESIDUALS",
    "OBSERVED_FIBER_IS_NOT_LICENSED_FIBER",
    "OBSERVED_SPACE_IS_NOT_A_GLOBAL_PRODUCT",
    "PRODUCT_REFUTATION_IS_NOT_FIBER_PROOF",
    "AxisExclusivityViolation",
    "Boundary",
    "CorpusDeposit",
    "CrossAxisCooccurrence",
    "ObservedFiber",
    "ObservedFiberTable",
    "ObservedStateFiberError",
    "OccurrenceRow",
    "ProductRefutationWitness",
    "capacity_by_carrier",
    "derive_cross_axis_cooccurrences",
    "read_corpus_lines",
    "read_state_vector",
    "run_observed_fiber_on_the_deposited_fatiha",
    "tabulate_observed_fibers",
]


class ObservedStateFiberError(ValueError):
    """رفضٌ عند الإنشاء: قياسٌ بلا بصمةِ مصدره، أو حالةٌ خارجَ مخطَّطها."""


ABSENT: Final[str] = "ABSENT"
"""قيمةُ الغياب على المحور؛ عضوٌ في كلّ محورٍ لا طرحٌ من الحساب."""


class Boundary(Enum):
    """طرفيّةُ الذرّة في كلمتها، مفردةً مغلقةً مُشتقّةً من موضعها لا مُقدَّرة."""

    WORD_INITIAL = "WORD_INITIAL"
    WORD_MEDIAL = "WORD_MEDIAL"
    WORD_FINAL = "WORD_FINAL"
    WORD_SOLE = "WORD_SOLE"


# --- المدوّنةُ مدخلٌ ببصمتها، لا نصٌّ مُثبَتٌ في الكود ------------------------


@dataclass(frozen=True, slots=True)
class CorpusDeposit:
    """مدوّنةٌ مقروءةٌ: اسمُها، وبصمتُها، وطولُ بايتاتها، وصورةُ تطبيعها.

    ولا قياسَ بلا هذه الأربعة: رقمٌ بلا بصمةِ مصدره رقمٌ لا يُعاد اشتقاقُه.
    """

    source_id: str
    sha256: str
    byte_length: int
    normalization_form: str

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ObservedStateFiberError("مدوّنةٌ بلا اسمِ مصدرٍ لا تُراجَع")
        if len(self.sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.sha256
        ):
            raise ObservedStateFiberError("بصمةُ المدوّنة بصمةٌ قانونيّةٌ بشكلها")
        if self.byte_length <= 0:
            raise ObservedStateFiberError("طولُ بايتات المدوّنة عددٌ موجب")
        if self.normalization_form not in ("NFC", "NFD", "NFKC", "NFKD"):
            raise ObservedStateFiberError("صورةُ التطبيع مُعلَنةٌ من صور يونيكود")


def read_corpus_lines(
    data: bytes,
    *,
    source_id: str,
    expected_sha256: str,
    normalization_form: Literal["NFC", "NFD", "NFKC", "NFKD"] = "NFC",
) -> tuple[CorpusDeposit, tuple[str, ...]]:
    """اقرأ بايتات أيّ مدوّنةٍ سطورًا، وارفضها إن خالفت بصمتَها المنتظَرة.

    وهذه هي الدالّةُ العامّة: لا تعرف الفاتحةَ ولا سواها، وتصلح لأيّ مدوّنةٍ
    تُقدَّم بايتاتُها وبصمتُها؛ وتثبيتُ نصٍّ بعينه شأنُ المدخل عديم الوسائط.
    """

    if type(data) is not bytes:
        raise ObservedStateFiberError("قراءةُ المدوّنة تلزمها بايتاتُها")
    digest = canonical_digest(data)
    if digest != expected_sha256:
        raise ObservedStateFiberError(
            "بايتاتُ المدوّنة تخالف البصمةَ المنتظَرة؛ والقياسُ على بايتاتٍ لم "
            "تُعرَف قياسٌ لا يُعاد اشتقاقُه"
        )
    text = data.decode("utf-8")
    if unicodedata.normalize(normalization_form, text) != text:
        raise ObservedStateFiberError(
            "نصُّ المدوّنة ليس في صورة تطبيعه المُعلَنة، والتطبيعُ الصامتُ يغيّر " "ما يُعَدّ"
        )
    deposit = CorpusDeposit(
        source_id=source_id,
        sha256=digest,
        byte_length=len(data),
        normalization_form=normalization_form,
    )
    return deposit, tuple(text.splitlines())


# --- قراءةُ الحالة بمحاورها --------------------------------------------------


def _axis_value(axis: StateAxisDeclaration, marks: tuple[str, ...]) -> str:
    present = [mark for mark in marks if mark in axis.marks]
    if not present:
        return ABSENT
    return present[0]


def read_state_vector(
    row: CarrierAtomRow, schema: StateSchema = CARRIER_FIBER_STATE_SCHEMA
) -> tuple[tuple[str, str], ...]:
    """اقرأ حالةَ الذرّة متَّجِهًا على المحاور المقيسة، بقيمةِ غيابٍ لا بطرح.

    والترتيبُ ترتيبُ المحاور في المخطَّط المُجمَّد، فلا يتغيّر المتَّجِهُ بتغيّر
    ترتيب العلامات في الرسم.
    """

    if type(row) is not CarrierAtomRow:
        raise ObservedStateFiberError("قراءةُ الحالة تلزمها صفَّ ذرّةٍ من العدّ الخامّ")
    if type(schema) is not StateSchema:
        raise ObservedStateFiberError("قراءةُ الحالة تلزمها مخطَّطًا مُجمَّدًا")
    return tuple(
        (axis.axis_id, _axis_value(axis, row.state_marks))
        for axis in schema.measured_axes
    )


def _deferred_marks(row: CarrierAtomRow, schema: StateSchema) -> tuple[str, ...]:
    deferred = {mark for axis in schema.deferred_axes for mark in axis.marks}
    return tuple(mark for mark in row.state_marks if mark in deferred)


def _unread_marks(row: CarrierAtomRow, schema: StateSchema) -> tuple[str, ...]:
    declared = {mark for axis in schema.axes for mark in axis.marks}
    return tuple(mark for mark in row.state_marks if mark not in declared)


# --- صفُّ الوقوع الواحد ------------------------------------------------------


@dataclass(frozen=True, slots=True)
class OccurrenceRow:
    """وقوعٌ واحد: حاملُه، وحالتُه بمحاورها، وموضعُه، وما لم يُقرأ منه.

    ولا حقلَ حكمٍ على الصفّ: لا «مسموح» ولا «ممنوع»؛ وما لم يدخل المتَّجِهَ
    محفوظٌ في حقلٍ مُسمًّى لا مطروحٌ بصمت.
    """

    line_index: int
    word_index: int
    position_in_word: int
    boundary: Boundary
    word: str
    carrier: str
    state_vector: tuple[tuple[str, str], ...]
    deferred_axis_marks: tuple[str, ...]
    unread_marks: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.position_in_word < 0:
            raise ObservedStateFiberError("موضعُ الذرّة في كلمتها عددٌ غيرُ سالب")
        if not isinstance(self.boundary, Boundary):
            raise ObservedStateFiberError("الطرفيّةُ عضوٌ في مفردتها المغلقة")
        if len(self.carrier) != 1:
            raise ObservedStateFiberError("حاملُ الوقوع رمزٌ واحد")
        if not self.state_vector:
            raise ObservedStateFiberError("متَّجِهُ الحالة لا يكون فارغًا")

    @property
    def stratum(self) -> tuple[int, str]:
        """طبقةُ الضبط: الموضعُ في الكلمة والطرفيّة معًا، لا أحدُهما."""

        return (self.position_in_word, self.boundary.value)


@dataclass(frozen=True, slots=True)
class AxisExclusivityViolation:
    """خرقٌ لدعوى التنافي داخلَ محورٍ واحد؛ صفٌّ يُحفَظ لا تصحيحٌ يُجرى."""

    line_index: int
    word_index: int
    carrier: str
    axis_id: str
    marks: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.marks) < 2:
            raise ObservedStateFiberError("خرقُ التنافي علامتان فأكثرُ من محورٍ واحد")


@dataclass(frozen=True, slots=True)
class CrossAxisCooccurrence:
    """اجتماعُ محورين على حاملٍ واحد: شاهدٌ على أنّهما ليسا قيمتين متنافيتين."""

    first_axis_id: str
    second_axis_id: str
    occurrence_count: int

    def __post_init__(self) -> None:
        if self.first_axis_id == self.second_axis_id:
            raise ObservedStateFiberError("الاجتماعُ بين محورين اثنين لا محورٍ ونفسِه")
        if self.occurrence_count <= 0:
            raise ObservedStateFiberError("صفُّ اجتماعٍ بلا وقوعٍ لا يُكتَب")


# --- ليفُ الحامل المرصود -----------------------------------------------------


@dataclass(frozen=True, slots=True)
class ObservedFiber:
    """ليفُ حاملٍ واحدٍ كما رُصِد: سعتُه، وتركيبُه، وتردّدُه، وطبقاتُه.

    والسعةُ والتركيبُ حقلان اثنان لا حقلٌ واحد، لأنّ حاملين قد يتساويان في
    الأوّل ويختلفان في الثاني، والسعةُ وحدَها تُفقِد البنية.
    """

    carrier: str
    frequency: int
    composition: tuple[tuple[tuple[str, str], ...], ...]
    strata: tuple[tuple[int, str], ...]

    def __post_init__(self) -> None:
        if len(self.carrier) != 1:
            raise ObservedStateFiberError("حاملُ الليف رمزٌ واحد")
        if self.frequency <= 0:
            raise ObservedStateFiberError("ليفٌ بلا وقوعٍ لا يُكتَب")
        if not self.composition:
            raise ObservedStateFiberError("تركيبُ الليف لا يكون فارغًا")
        if len(set(self.composition)) != len(self.composition):
            raise ObservedStateFiberError("تكرّرت حالةٌ في تركيب ليفٍ واحد")

    @property
    def capacity(self) -> int:
        """`Capacity(C) = |S_obs(C)|`، مُشتقًّا من التركيب لا مكتوبًا بجانبه."""

        return len(self.composition)


@dataclass(frozen=True, slots=True)
class ProductRefutationWitness:
    """شاهدُ تفنيدٍ مُقيَّدٌ بنطاقه: حاملان اختلف ليفُهما المرصود في هذه المدوّنة."""

    source_id: str
    source_sha256: str
    first_carrier: str
    second_carrier: str
    first_capacity: int
    second_capacity: int
    compositions_differ: bool
    scope_note: str

    def __post_init__(self) -> None:
        if self.first_carrier == self.second_carrier:
            raise ObservedStateFiberError("شاهدُ التفنيد حاملان مختلفان لا حاملٌ ونفسُه")
        if not self.scope_note.strip():
            raise ObservedStateFiberError("شاهدٌ بلا نطاقٍ مكتوبٍ يُقرأ أوسعَ ممّا قِيس")

    @property
    def refutes_global_product_in_scope(self) -> bool:
        """أيُفنِّد هذا الشاهدُ `C × S_global` في نطاقه؟ مُشتَقٌّ لا مُصرَّحٌ به."""

        return self.compositions_differ


# --- الجدولُ: وقوعاتٌ كاملةٌ، وألياف مُشتقّةٌ منها ----------------------------


@dataclass(frozen=True, slots=True)
class ObservedFiberTable:
    """قياسُ مدوّنةٍ واحدة: مصدرُها ببصمته، ووقوعاتُها كلُّها، وما خرق التنافي."""

    deposit: CorpusDeposit
    schema: StateSchema
    rows: tuple[OccurrenceRow, ...]
    axis_exclusivity_violations: tuple[AxisExclusivityViolation, ...]
    unattached_mark_count: int
    unclassified_codepoints: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.deposit) is not CorpusDeposit:
            raise ObservedStateFiberError("الجدولُ يلزمه مدوّنةً مقروءةً ببصمتها")
        if type(self.schema) is not StateSchema:
            raise ObservedStateFiberError("الجدولُ يلزمه مخطَّطَ الحالة المُجمَّد")
        if self.unattached_mark_count < 0:
            raise ObservedStateFiberError("عددُ العلامات غير المتّصلة غيرُ سالب")

    @property
    def carriers(self) -> tuple[str, ...]:
        """الحواملُ التي وردت، بترتيب أوّل ورودها."""

        return tuple(dict.fromkeys(row.carrier for row in self.rows))

    @property
    def fibers(self) -> tuple[ObservedFiber, ...]:
        """ليفُ كلّ حاملٍ مُشتقًّا من الصفوف، بترتيب أوّل ورود حامله."""

        composition: dict[str, list[tuple[tuple[str, str], ...]]] = {}
        strata: dict[str, list[tuple[int, str]]] = {}
        frequency: dict[str, int] = {}
        for row in self.rows:
            frequency[row.carrier] = frequency.get(row.carrier, 0) + 1
            states = composition.setdefault(row.carrier, [])
            if row.state_vector not in states:
                states.append(row.state_vector)
            carrier_strata = strata.setdefault(row.carrier, [])
            if row.stratum not in carrier_strata:
                carrier_strata.append(row.stratum)
        return tuple(
            ObservedFiber(
                carrier=carrier,
                frequency=frequency[carrier],
                composition=tuple(composition[carrier]),
                strata=tuple(strata[carrier]),
            )
            for carrier in self.carriers
        )

    def fiber_for(self, carrier: str) -> ObservedFiber:
        """ليفُ حاملٍ بعينه؛ وحاملٌ لم يرد يُرَدّ باسمه لا بليفٍ فارغ."""

        for fiber in self.fibers:
            if fiber.carrier == carrier:
                return fiber
        raise ObservedStateFiberError("حاملٌ لم يرد في هذه المدوّنة لا ليفَ له هنا")

    @property
    def global_composition(self) -> tuple[tuple[tuple[str, str], ...], ...]:
        """`S_observed-global`: كلُّ حالةٍ رُصِدت مع أيّ حامل، بترتيب ورودها."""

        seen: list[tuple[tuple[str, str], ...]] = []
        for row in self.rows:
            if row.state_vector not in seen:
                seen.append(row.state_vector)
        return tuple(seen)

    @property
    def observed_support_size(self) -> int:
        """حجمُ الحامل الفعليّ: عددُ أزواج (حامل، حالة) المرصودة."""

        return sum(fiber.capacity for fiber in self.fibers)

    @property
    def global_product_size(self) -> int:
        """حجمُ `C × S_observed-global` لو كان الفضاءُ حاصلًا مسطَّحًا."""

        return len(self.carriers) * len(self.global_composition)

    def derive_product_refutation(self) -> ProductRefutationWitness | None:
        """اشتقّ شاهدَ التفنيد إن وُجد، بنطاقه مكتوبًا لا مطويًّا.

        والغيابُ يُرَدّ `None` صريحًا: مدوّنةٌ لم تُخرِج حاملين مختلفَي الليف
        لا تُفنِّد شيئًا، وقراءةُ الغياب تأييدًا هي عينُ ما تمنعه هذه الشجرة.
        """

        fibers = self.fibers
        for index, first in enumerate(fibers):
            for second in fibers[index + 1 :]:
                if set(first.composition) != set(second.composition):
                    return ProductRefutationWitness(
                        source_id=self.deposit.source_id,
                        source_sha256=self.deposit.sha256,
                        first_carrier=first.carrier,
                        second_carrier=second.carrier,
                        first_capacity=first.capacity,
                        second_capacity=second.capacity,
                        compositions_differ=True,
                        scope_note=OBSERVED_SPACE_IS_NOT_A_GLOBAL_PRODUCT,
                    )
        return None


def _boundary_of(position: int, carrier_count: int) -> Boundary:
    if carrier_count == 1:
        return Boundary.WORD_SOLE
    if position == 0:
        return Boundary.WORD_INITIAL
    if position == carrier_count - 1:
        return Boundary.WORD_FINAL
    return Boundary.WORD_MEDIAL


def _exclusivity_violations(
    row: CarrierAtomRow, schema: StateSchema
) -> tuple[AxisExclusivityViolation, ...]:
    violations: list[AxisExclusivityViolation] = []
    for axis in schema.axes:
        present = tuple(mark for mark in row.state_marks if mark in axis.marks)
        if axis.exclusivity_within_axis_is_claimed and len(set(present)) > 1:
            violations.append(
                AxisExclusivityViolation(
                    line_index=row.line_index,
                    word_index=row.word_index,
                    carrier=row.carrier,
                    axis_id=axis.axis_id,
                    marks=present,
                )
            )
    return tuple(violations)


def tabulate_observed_fibers(
    lines: Iterable[str],
    *,
    deposit: CorpusDeposit,
    schema: StateSchema = CARRIER_FIBER_STATE_SCHEMA,
) -> ObservedFiberTable:
    """اقرأ سطورَ مدوّنةٍ وأخرِج جدولَ وقوعاتها التامَّ بحالاتها على المحاور."""

    if type(deposit) is not CorpusDeposit:
        raise ObservedStateFiberError("القياسُ يلزمه مدوّنةً مقروءةً ببصمتها")
    raw: AlifStateRawCountTable = count_alif_states(lines, source_id=deposit.source_id)
    per_word: dict[tuple[int, int], int] = {}
    for atom in raw.rows:
        key = (atom.line_index, atom.word_index)
        per_word[key] = per_word.get(key, 0) + 1
    seen_in_word: dict[tuple[int, int], int] = {}
    rows: list[OccurrenceRow] = []
    violations: list[AxisExclusivityViolation] = []
    for atom in raw.rows:
        key = (atom.line_index, atom.word_index)
        position = seen_in_word.get(key, 0)
        seen_in_word[key] = position + 1
        rows.append(
            OccurrenceRow(
                line_index=atom.line_index,
                word_index=atom.word_index,
                position_in_word=position,
                boundary=_boundary_of(position, per_word[key]),
                word=atom.word,
                carrier=atom.carrier,
                state_vector=read_state_vector(atom, schema),
                deferred_axis_marks=_deferred_marks(atom, schema),
                unread_marks=_unread_marks(atom, schema),
            )
        )
        violations.extend(_exclusivity_violations(atom, schema))
    return ObservedFiberTable(
        deposit=deposit,
        schema=schema,
        rows=tuple(rows),
        axis_exclusivity_violations=tuple(violations),
        unattached_mark_count=len(raw.unattached_marks),
        unclassified_codepoints=raw.unclassified_codepoints,
    )


def derive_cross_axis_cooccurrences(
    table: ObservedFiberTable,
) -> tuple[CrossAxisCooccurrence, ...]:
    """اشتقّ اجتماعَ المحاور مثنى مثنى: شاهدُ أنّها ليست قيمًا في محورٍ واحد.

    وهو شاهدٌ على عدم التنافي لا برهانٌ على استقلالٍ إحصائيّ؛ والفرقُ مُسمًّى
    في `AXIS_ORTHOGONALITY_IS_DECLARED_NOT_PROVEN`.
    """

    if type(table) is not ObservedFiberTable:
        raise ObservedStateFiberError("الاشتقاقُ يلزمه جدولَ وقوعاتٍ مقيسًا")
    axes = [axis.axis_id for axis in table.schema.measured_axes]
    counts: dict[tuple[str, str], int] = {}
    for row in table.rows:
        present = {axis_id for axis_id, value in row.state_vector if value != ABSENT}
        for index, first in enumerate(axes):
            for second in axes[index + 1 :]:
                if first in present and second in present:
                    key = (first, second)
                    counts[key] = counts.get(key, 0) + 1
    return tuple(
        CrossAxisCooccurrence(
            first_axis_id=first, second_axis_id=second, occurrence_count=count
        )
        for (first, second), count in counts.items()
    )


# --- المدخلُ عديمُ الوسائط: معايرةٌ على النصّ المُودَع ------------------------


def run_observed_fiber_on_the_deposited_fatiha() -> ObservedFiberTable:
    """شغِّل القياسَ على الفاتحة المُودَعة بوصفه معايرةً لا اختبارًا حاسمًا.

    والبصمةُ والطولُ مأخوذان من وحدة النصّ المُودَع نفسِها، فلا يُكتَب رقمٌ هنا
    يمكن أن ينحرف عن مصدره.
    """

    deposit = CorpusDeposit(
        source_id=FATIHA_SOURCE_ID,
        sha256=source_sha256(),
        byte_length=source_byte_length(),
        normalization_form=NORMALIZATION_FORM,
    )
    return tabulate_observed_fibers(FATIHA_LINES, deposit=deposit)


def capacity_by_carrier(table: ObservedFiberTable) -> Mapping[str, int]:
    """سعةُ ليف كلّ حامل، مُشتقّةً من الجدول لا مكتوبةً بجانبه."""

    return {fiber.carrier: fiber.capacity for fiber in table.fibers}


# --- ما لا يحسمه هذا القياس، مُسمًّى ------------------------------------------


OBSERVED_SPACE_IS_NOT_A_GLOBAL_PRODUCT: Final[str] = (
    "OBSERVED_SPACE_IS_NOT_A_GLOBAL_PRODUCT: ما يُفنَّد بهذا الشاهد هو "
    "`E_observed = C × S_observed-global` في هذه المدوّنة وهذا الترميز وحدَهما؛ "
    "ولا يمتدّ التفنيدُ إلى مدوّنةٍ أخرى ولا إلى ترميزٍ آخر"
)

OBSERVED_FIBER_IS_NOT_LICENSED_FIBER: Final[str] = (
    "OBSERVED_FIBER_IS_NOT_LICENSED_FIBER: `S_observed(c)` ما رُصِد، و"
    "`S_licensed(c)` ما يُسمَح به؛ وغيابُ حالةٍ عن ليفٍ مرصودٍ قد يكون منعًا أو "
    "ندرةً أو تعذّرًا بالموضع، ولا يفصل بينها رصدٌ وحدَه"
)

PRODUCT_REFUTATION_IS_NOT_FIBER_PROOF: Final[str] = (
    "PRODUCT_REFUTATION_IS_NOT_FIBER_PROOF: تفنيدُ الحاصل المسطَّح لا يُثبِت "
    "بنيةً ليفيةً؛ فالبنيةُ تحتاج `π: E → C` يُسقِط كلَّ وقوعٍ إلى حاملٍ واحدٍ "
    "وليفُه مجموعةُ حالاته المرخَّصة، ولا تُنشِئ هذه الوحدةُ ذلك الإسقاط"
)

AN_EXCLUSIVITY_VIOLATION_IS_A_ROW_NOT_A_CORRECTION: Final[str] = (
    "AN_EXCLUSIVITY_VIOLATION_IS_A_ROW_NOT_A_CORRECTION: خرقُ دعوى التنافي "
    "داخلَ محورٍ يُحفَظ صفًّا مُسمًّى ولا يُصحَّح ولا يُطرَح؛ فالتصحيحُ الصامتُ "
    "يجعل المخطَّطَ شاهدًا لنفسه"
)

A_CALIBRATION_RUN_IS_NOT_A_DECISIVE_RUN: Final[str] = (
    "A_CALIBRATION_RUN_IS_NOT_A_DECISIVE_RUN: النصُّ المُودَعُ قصيرٌ، وتشغيلُه "
    "معايرةٌ وشاهدٌ بنيويٌّ على أنّ القياسَ يعمل؛ والحسمُ يحتاج تشغيلَ المواصفة "
    "نفسِها على مدوّنةٍ مستقلّةٍ تُقدَّم بايتاتُها وبصمتُها"
)

CARRIER_STATE_OBSERVED_FIBER_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "OBSERVED_SPACE_IS_NOT_A_GLOBAL_PRODUCT": OBSERVED_SPACE_IS_NOT_A_GLOBAL_PRODUCT,
    "OBSERVED_FIBER_IS_NOT_LICENSED_FIBER": OBSERVED_FIBER_IS_NOT_LICENSED_FIBER,
    "PRODUCT_REFUTATION_IS_NOT_FIBER_PROOF": PRODUCT_REFUTATION_IS_NOT_FIBER_PROOF,
    "AN_EXCLUSIVITY_VIOLATION_IS_A_ROW_NOT_A_CORRECTION": (
        AN_EXCLUSIVITY_VIOLATION_IS_A_ROW_NOT_A_CORRECTION
    ),
    "A_CALIBRATION_RUN_IS_NOT_A_DECISIVE_RUN": A_CALIBRATION_RUN_IS_NOT_A_DECISIVE_RUN,
}
"""ما لا يحسمه هذا القياس، مُسمًّى هنا لا متروكًا ليُفترَض."""
