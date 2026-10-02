"""اختبارُ الدعوى الديكارتيّة والفراكتاليّة للدالِّ وحدَه — قناةٌ ثانيةٌ بتوقيع المالك.

امتدادٌ لـ`owner_experiment` بالإذن نفسِه وبحدوده نفسِها: التوقيعُ يأذن بتشغيلٍ
ولا يختم بايتاتٍ غائبة، والقناةُ تُحذَف بتمامها ولا تُرخي حارسًا في موضعه. ولم
تُمَسّ بايتةٌ من `bridge.py` ولا من حرّاس الشجرة::

    AnExhaustiveParser  != AnIndependentReference
    ASuccessfulSquare   != AnInjectiveProjection
    AMatchingResidue    != AMatchingTotal
    ACountableSet       != AFractal

**أوّلًا: الاستنفادُ استقلالُ خوارزميّةٍ لا استقلالُ مرجع.** المحلّلُ ههنا
يُعدِّد **كلَّ** تقسيمٍ تسمح به قواعدُ `CV|CVV|CVC` ثمّ يُقابَل بما يُخرِجه
الجسر، والقواعدُ والنصُّ من المشروع نفسِه. فلا يُسمّى هذا مرجعًا لغويًّا
مستقلًّا ولا اختبارًا محجوبَ البيانات
(`AN_EXHAUSTIVE_PARSER_IS_NOT_AN_INDEPENDENT_LINGUISTIC_REFERENCE`).

**وثانيًا: ونجاحُ المربّع لا يستلزم حقنيّةَ الإسقاط.** المربّعُ نجح ههنا
بتقابلٍ تامٍّ مع حاصل الألياف، **ومع ذلك** فوق 18 تسلسلًا ذرّيًّا رسمان
مختلفان. ولا تناقض: الزوجُ يحمل الرسمَ معه، فلا يُطلَب من التقسيم أن يستعيده
(`A_SUCCESSFUL_SQUARE_DOES_NOT_MAKE_THE_PROJECTION_INJECTIVE`).

**وثالثًا: والأدوارُ لا ترفع التصادم، وصفرُها بلغه التعريفُ لا القياس.**
الألياف الثمانيةَ عشرَ لا يفصل بينها دورٌ صوتيٌّ واحد — ولكن **لأنّ الأدوار
في هذا النموذج مشتقّةٌ من الذرّات**، فعجزُها لازمٌ عن التعريف. فيُعرَض الصفرُ
ومعه ما بلغه به، ولا يُقرأ ظفرًا بضبطٍ لم يُمتحَن؛ ورفعُ التصادم يحتاج معلومةً
خارجَ الذرّات
(`ADDING_THE_ROLES_SEPARATES_NOT_ONE_OF_THE_EIGHTEEN_FIBERS`،
`A_ZERO_REACHED_BY_DEFINITION_IS_NOT_A_ZERO_EARNED`).

**ورابعًا: وبقيّةُ «لا تقسيم» تنقسم قسمين، ولا يُقرأ مجموعُها رقمًا واحدًا.**
منها ما يبدأ بساكنٍ — وهو أثرُ نموذج الكلمة المعزولة على مُودَعٍ فيه إدغامٌ
مكتوب، لا امتناعٌ عربيّ — ومنها ما سوى ذلك. والقسمُ الثاني وحدَه هو الذي
يوافق رقمَ الدراسة؛ فجمعُهما كان سيُخفي الموافقة
(`THE_UNPARTITIONED_RESIDUE_IS_TWO_NAMED_CLASSES_NOT_ONE_FIGURE`).

**وخامسًا: والبعدُ الهاوسدورفيُّ الموجبُ ممتنعٌ على جردٍ معدود، وامتناعُه
بُرهانٌ لا قياس.** لا يُشغَّل برهانٌ بالعدّ؛ فالمُخرَجُ ههنا **شاهدُ تغطيةٍ
منتهٍ** يُظهِر أنّ مجموع أقطار الغطاء مرفوعةً إلى `s` يُصغَّر دون أيِّ `ε`،
والبرهانُ نفسُه مكتوبٌ ولا يُدَّعى أنّ تشغيلَ الشاهد يقوم مقامه
(`A_FINITE_COVERING_WITNESS_ILLUSTRATES_THE_THEOREM_AND_DOES_NOT_PROVE_IT`).

**وسادسًا: وما لم يُعيَّن يبقى مؤجَّلًا باسم ما ينقصه.** بوّاباتُ `G4..G8`
ومربّعاتُها ومراجعُها غيرُ معيَّنةٍ في المادّة المفحوصة، و`IFS` اللغويُّ بلا
متريّةٍ ولا خرائطِ تحجيم. فالحكمُ `DEFER` بموادّه لا `FAIL`.

ولا سلطةَ لهذه الوحدة: لا حكمَ لغويًّا، ولا تعديلَ مُجمَّد، ولا استيرادَ من
`alghanem`، ولا تقرؤها بوّابةٌ في الشجرة.
"""

from __future__ import annotations

import collections
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .bridge import A116, SUKUN, BridgeStatus, bridge
from .owner_experiment import (
    OWNER_SIGNATURE,
    Figure,
    Provenance,
    _occurrences,
    read_deposit,
)

__all__ = [
    "OWNER_SIGNATURE",
    "ClaimVerdict",
    "Syllable",
    "every_partition_of",
    "fiber_reading",
    "hausdorff_reading",
    "partition_reading",
    "square_reading",
    "the_roles_are_a_function_of_the_atoms",
    "verdict_table",
]


AN_EXHAUSTIVE_PARSER_IS_NOT_AN_INDEPENDENT_LINGUISTIC_REFERENCE: Final[str] = (
    "AN_EXHAUSTIVE_PARSER_IS_NOT_AN_INDEPENDENT_LINGUISTIC_REFERENCE: استنفادُ "
    "التقسيمات يستقلّ بخوارزميّته عن الجسر، وقواعدُه ونصُّه من المشروع نفسِه؛ "
    "فليس مرجعًا لغويًّا مستقلًّا ولا اختبارًا محجوبَ البيانات."
)

A_SUCCESSFUL_SQUARE_DOES_NOT_MAKE_THE_PROJECTION_INJECTIVE: Final[str] = (
    "A_SUCCESSFUL_SQUARE_DOES_NOT_MAKE_THE_PROJECTION_INJECTIVE: المربّعُ يتمّ "
    "والرسمُ محفوظٌ في الزوج، فوجودُ رسمين فوق تسلسلٍ واحدٍ لا يبطله ولا يُقرأ "
    "استعادةً للرسم من الذرّات."
)

ADDING_THE_ROLES_SEPARATES_NOT_ONE_OF_THE_EIGHTEEN_FIBERS: Final[str] = (
    "ADDING_THE_ROLES_SEPARATES_NOT_ONE_OF_THE_EIGHTEEN_FIBERS: تواقيعُ أصناف "
    "المقاطع متّحدةٌ داخل كلِّ ليفٍ متصادم، وذلك لازمٌ عن كونها دالّةً في "
    "الذرّات؛ فالأدوارُ لا تُنشئ معكوسًا وحيدًا."
)

THE_UNPARTITIONED_RESIDUE_IS_TWO_NAMED_CLASSES_NOT_ONE_FIGURE: Final[str] = (
    "THE_UNPARTITIONED_RESIDUE_IS_TWO_NAMED_CLASSES_NOT_ONE_FIGURE: البادئُ "
    "بساكنٍ أثرُ نموذج الكلمة المعزولة على مُودَعٍ فيه إدغامٌ مكتوب، وما سواه "
    "حدُّ نموذج المقاطع؛ فلا يُجمَعان في رقم."
)

A_FINITE_COVERING_WITNESS_ILLUSTRATES_THE_THEOREM_AND_DOES_NOT_PROVE_IT: Final[str] = (
    "A_FINITE_COVERING_WITNESS_ILLUSTRATES_THE_THEOREM_AND_DOES_NOT_PROVE_IT: "
    "البرهانُ على البعد الصفريِّ برهانٌ لا تشغيل؛ والشاهدُ المنتهي ههنا يُريه "
    "ولا يقوم مقامه."
)

A_COUNTABLE_SET_IS_NOT_A_FRACTAL: Final[str] = (
    "A_COUNTABLE_SET_IS_NOT_A_FRACTAL: صفرُ البعد الهاوسدورفيّ ينفي الصيغةَ "
    "الهندسيّةَ على السلاسل المنتهية وحدَها، ولا ينفي كلَّ تعريفٍ آخر للفراكتال."
)


# ---------------------------------------------------------------------------
# أوّلًا: المادّةُ المفحوصة — أشكالٌ جاهزةٌ بسياسةٍ مُعلَنةٍ قبل القياس
# ---------------------------------------------------------------------------

THE_DECLARED_POLICY: Final[dict[str, str]] = {"entry": "start", "exit": "continue"}
"""نموذجُ الكلمة المعزولة؛ مُعلَنٌ قبل القياس ولا يُبدَّل بعده."""

MADD_ATOMS: Final[frozenset[str]] = frozenset({"اْ", "وْ", "يْ"})
"""الذرّاتُ الساكنةُ التي تُقرأ مدًّا فتجعل المقطعَ `CVV` لا `CVC`."""


def ready_forms() -> dict[str, tuple[str, ...]]:
    """كلُّ شكلٍ مختلفٍ بلغ الجاهزيّةَ في الجسر، مع تسلسل ذرّاته."""

    text, _ = read_deposit()
    forms: dict[str, tuple[str, ...]] = {}
    for form in collections.Counter(_occurrences(text)):
        record = bridge(form, contexts={0: dict(THE_DECLARED_POLICY)})
        if record["status"] == BridgeStatus.READY.value:
            forms[form] = tuple(record["canonical_atoms"])
    return forms


# ---------------------------------------------------------------------------
# ثانيًا: فحصُ الحقن — أليافُ الإسقاط
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FiberReading:
    """أليافُ الإسقاط: كم شكلًا فوق كم تسلسلًا، وأين تصادما."""

    forms: int
    distinct_atom_sequences: int
    collided_fibers: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...]

    @property
    def forms_inside_collisions(self) -> int:
        return sum(len(members) for _, members in self.collided_fibers)

    @property
    def projection_is_injective(self) -> bool:
        return not self.collided_fibers

    @property
    def no_retraction_recovers_the_rasm(self) -> bool:
        """π(w₁)=π(w₂) مع w₁≠w₂ ⇒ لا دالّةَ r تحقّق r∘π=id على هويّة الرسم."""

        return not self.projection_is_injective


def fiber_reading(forms: dict[str, tuple[str, ...]] | None = None) -> FiberReading:
    """قياسُ الحقن على كلِّ شكلٍ جاهز؛ والتصادمُ يُسمّى بأعضائه لا بعدده."""

    forms = ready_forms() if forms is None else forms
    fibers: dict[tuple[str, ...], list[str]] = collections.defaultdict(list)
    for form, atoms in forms.items():
        fibers[atoms].append(form)
    collided = tuple(
        (atoms, tuple(sorted(members)))
        for atoms, members in sorted(fibers.items())
        if len(members) > 1
    )
    return FiberReading(
        forms=len(forms),
        distinct_atom_sequences=len(fibers),
        collided_fibers=collided,
    )


# ---------------------------------------------------------------------------
# ثالثًا: المحلّلُ الاستنفاديّ — كلُّ تقسيمٍ تسمح به القواعد
# ---------------------------------------------------------------------------


class Syllable(str, Enum):
    """أصنافُ المقاطع في النموذج المُعلَن؛ وما سواها لا يُدخَل بالتخمين."""

    CV = "CV"
    CVV = "CVV"
    CVC = "CVC"


Partition = tuple[tuple[Syllable, tuple[str, ...]], ...]


def every_partition_of(atoms: tuple[str, ...]) -> tuple[Partition, ...]:
    """استنفادٌ تامّ: كلُّ تقسيمٍ تسمح به `CV|CVV|CVC`، لا تقسيمُ الجشع وحدَه.

    ولا يُفرَض فيه ترتيبُ أفضليّة: الفرعان يُفتحان معًا عند كلِّ موضع، فإن خرج
    تقسيمٌ واحدٌ فذلك لأنّ القواعد أوجبته لا لأنّ الخوارزميّة اختارته.
    """

    length = len(atoms)
    found: list[Partition] = []

    def walk(position: int, built: list[tuple[Syllable, tuple[str, ...]]]) -> None:
        if position == length:
            found.append(tuple(built))
            return
        head = atoms[position]
        if head.endswith(SUKUN):
            return
        walk(position + 1, [*built, (Syllable.CV, (head,))])
        if position + 1 < length and atoms[position + 1].endswith(SUKUN):
            tail = atoms[position + 1]
            kind = Syllable.CVV if tail in MADD_ATOMS else Syllable.CVC
            walk(position + 2, [*built, (kind, (head, tail))])

    walk(0, [])
    return tuple(found)


def role_signature(atoms: tuple[str, ...]) -> tuple[str, ...]:
    """توقيعُ الأدوار الصوتيّة؛ وهو في هذا النموذج **دالّةٌ في الذرّات**."""

    partitions = every_partition_of(atoms)
    if len(partitions) != 1:
        return ()
    return tuple(kind.value for kind, _ in partitions[0])


def the_roles_are_a_function_of_the_atoms(
    forms: dict[str, tuple[str, ...]] | None = None,
) -> bool:
    """هل يتعيّن توقيعُ الأدوار بالذرّات وحدَها؟ إن كان، فصفرُ الفصل بنيويّ.

    وهذا ما يجعل «صفرَ الألياف التي يفصلها دورٌ صوتيّ» **صفرًا بلغه التعريفُ
    لا القياس**: الأدوارُ مشتقّةٌ من الذرّات، فلا يمكنها أن تفصل بين شكلين
    اتّحدت ذرّاتهما. فالصفرُ يُعرَض ومعه ما بلغه به، ولا يُقرأ ظفرًا بضبطٍ لم
    يُمتحَن (`A_ZERO_REACHED_BY_DEFINITION_IS_NOT_A_ZERO_EARNED`).
    """

    forms = ready_forms() if forms is None else forms
    seen: dict[tuple[str, ...], tuple[str, ...]] = {}
    for atoms in forms.values():
        signature = role_signature(atoms)
        if atoms in seen and seen[atoms] != signature:
            return False
        seen[atoms] = signature
    return True


A_ZERO_REACHED_BY_DEFINITION_IS_NOT_A_ZERO_EARNED: Final[str] = (
    "A_ZERO_REACHED_BY_DEFINITION_IS_NOT_A_ZERO_EARNED: الأدوارُ في هذا النموذج "
    "مشتقّةٌ من الذرّات، فعجزُها عن فصل ليفٍ متصادمٍ لازمٌ عن التعريف لا نتيجةٌ "
    "تجريبيّة؛ ورفعُ التصادم يحتاج معلومةً خارجَ الذرّات."
)


def unfold(partition: Partition) -> tuple[str, ...]:
    """فكُّ التقسيم إلى ذرّاته؛ وهو `g` في المربّع."""

    return tuple(atom for _, syllable in partition for atom in syllable)


@dataclass(frozen=True)
class PartitionReading:
    """جردُ التقسيمات: واحدٌ، أو لا شيء بقسمَيه، أو أكثر من واحد."""

    exactly_one: int
    starts_with_a_sakin: int
    other_without_a_partition: int
    more_than_one: int
    fold_unfold_losses: int

    @property
    def without_a_partition(self) -> int:
        return self.starts_with_a_sakin + self.other_without_a_partition

    @property
    def the_partition_is_unique_wherever_it_exists(self) -> bool:
        return self.more_than_one == 0


def partition_reading(
    forms: dict[str, tuple[str, ...]] | None = None,
) -> PartitionReading:
    """تشغيلُ الاستنفاد على كلِّ شكلٍ جاهز، وقسمةُ البقيّة بأسبابها."""

    forms = ready_forms() if forms is None else forms
    exactly_one = starts_sakin = other_absent = more_than_one = losses = 0
    for atoms in forms.values():
        partitions = every_partition_of(atoms)
        if len(partitions) == 1:
            exactly_one += 1
            if unfold(partitions[0]) != atoms:
                losses += 1
        elif not partitions:
            if atoms and atoms[0].endswith(SUKUN):
                starts_sakin += 1
            else:
                other_absent += 1
        else:
            more_than_one += 1
    return PartitionReading(
        exactly_one=exactly_one,
        starts_with_a_sakin=starts_sakin,
        other_without_a_partition=other_absent,
        more_than_one=more_than_one,
        fold_unfold_losses=losses,
    )


# ---------------------------------------------------------------------------
# رابعًا: المربّعُ المحلّيّ — تقابلُ θ مع حاصل الألياف
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SquareReading:
    """المربّعُ المفحوص: مجموعاتُه وتبادلُ خرائطه وتقابلُ θ."""

    w: int
    x: int
    s: int
    certificates: int
    fiber_product_pairs: int
    maps_commute: bool
    pairs_without_a_certificate: int
    pairs_with_two_certificates: int
    collided_fibers_inside_w: int

    @property
    def theta_is_a_bijection(self) -> bool:
        return (
            self.certificates == self.fiber_product_pairs
            and self.pairs_without_a_certificate == 0
            and self.pairs_with_two_certificates == 0
            and self.maps_commute
        )

    @property
    def the_square_succeeds_while_the_projection_collides(self) -> bool:
        """نجاحٌ تامٌّ مع تصادمٍ قائم؛ وهذا ليس تناقضًا بل حدُّ الدعوى."""

        return self.theta_is_a_bijection and self.collided_fibers_inside_w > 0


def square_reading(forms: dict[str, tuple[str, ...]] | None = None) -> SquareReading:
    """بناءُ المرجع `S` بالاستنفاد، ثمّ فحصُ الشهادات بمقابلتها به.

    ولم تُعرَّف عناصرُ `S` بأنّها مقاطعُ البرنامج المقبولة؛ لو فُعِل لكان
    المرجعُ مخرجاتِ التنفيذ فتُحسَب المطابقةُ برهانًا.
    """

    forms = ready_forms() if forms is None else forms
    certificates: dict[str, Partition] = {}
    for form, atoms in forms.items():
        partitions = every_partition_of(atoms)
        if len(partitions) == 1:
            certificates[form] = partitions[0]

    w = set(certificates)
    x = {forms[form] for form in w}
    s = set(certificates.values())

    by_atoms: dict[tuple[str, ...], list[Partition]] = collections.defaultdict(list)
    for partition in s:
        by_atoms[unfold(partition)].append(partition)

    pairs = sum(len(by_atoms[forms[form]]) for form in w)
    without = sum(1 for form in w if not by_atoms[forms[form]])
    doubled = sum(1 for form in w if len(by_atoms[forms[form]]) > 1)
    commute = all(unfold(certificates[form]) == forms[form] for form in w)

    inside: dict[tuple[str, ...], int] = collections.Counter(forms[form] for form in w)
    collided = sum(1 for count in inside.values() if count > 1)

    return SquareReading(
        w=len(w),
        x=len(x),
        s=len(s),
        certificates=len(certificates),
        fiber_product_pairs=pairs,
        maps_commute=commute,
        pairs_without_a_certificate=without,
        pairs_with_two_certificates=doubled,
        collided_fibers_inside_w=collided,
    )


# ---------------------------------------------------------------------------
# خامسًا: البعدُ الهاوسدورفيّ — برهانٌ مكتوبٌ وشاهدُ تغطيةٍ منتهٍ
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HausdorffReading:
    """شاهدُ التغطية: مجموعُ `dⁱˢ` أصغرُ من `ε` لكلِّ `s` موجب."""

    alphabet_size: int
    prefix_lengths: tuple[int, ...]
    finite_level_sizes: tuple[int, ...]
    epsilon: float
    exponent: float
    covering_sum: float
    largest_diameter: float

    @property
    def every_level_is_finite(self) -> bool:
        return all(size > 0 for size in self.finite_level_sizes)

    @property
    def the_covering_sum_is_under_epsilon(self) -> bool:
        return self.covering_sum <= self.epsilon

    @property
    def a_positive_dimension_is_refused(self) -> bool:
        """الدعوى مرفوضةٌ رياضيًّا؛ والشاهدُ يُريها ولا يقوم مقام البرهان."""

        return self.every_level_is_finite and self.the_covering_sum_is_under_epsilon


def hausdorff_reading(
    *,
    levels: int = 6,
    epsilon: float = 1e-6,
    exponent: float = 0.5,
    points: int = 4096,
) -> HausdorffReading:
    """`|Aⁿ|=116ⁿ` منتهٍ لكلِّ `n`، فـ`A*` معدود؛ ثمّ غطاءٌ بقطرٍ `(ε·2⁻ⁱ)^(1/s)`.

    فيكون `Σᵢ dᵢˢ = ε·Σᵢ 2⁻ⁱ ≤ 2ε`، ويُصغَّر دون أيِّ موجبٍ بإنزال `ε`. وهذا
    شاهدٌ منتهٍ على مقدّمة البرهان، لا تشغيلٌ للبرهان نفسِه.
    """

    alphabet = len(set(A116))
    sizes = tuple(alphabet**n for n in range(levels))
    diameters = [
        (epsilon * 2.0 ** (-(index + 1))) ** (1.0 / exponent) for index in range(points)
    ]
    covering = sum(diameter**exponent for diameter in diameters)
    return HausdorffReading(
        alphabet_size=alphabet,
        prefix_lengths=tuple(range(levels)),
        finite_level_sizes=sizes,
        epsilon=epsilon,
        exponent=exponent,
        covering_sum=covering,
        largest_diameter=max(diameters),
    )


# ---------------------------------------------------------------------------
# سادسًا: جدولُ الأحكام بحسب صيغة الدعوى
# ---------------------------------------------------------------------------


class ClaimVerdict(str, Enum):
    """حكمٌ بصيغةٍ واحدةٍ لا بالدعوى جملةً."""

    PASS = "PASS"
    FAIL = "FAIL"
    DEFER = "DEFER"


@dataclass(frozen=True)
class Claim:
    """صيغةُ دعوى، وحكمُها، ودليلُه، وحدُّ قراءته."""

    wording: str
    verdict: ClaimVerdict
    evidence: str
    limit: str


def verdict_table() -> tuple[Claim, ...]:
    """الأحكامُ مشتقّةٌ من القياس، وكلُّ حكمٍ مقيَّدٌ بصيغته."""

    fibers = fiber_reading()
    partitions = partition_reading()
    square = square_reading()
    hausdorff = hausdorff_reading()

    return (
        Claim(
            wording="مربّعُ التجسير والمقاطع داخل النموذج المحدّد",
            verdict=(
                ClaimVerdict.PASS if square.theta_is_a_bijection else ClaimVerdict.FAIL
            ),
            evidence=(
                f"{square.certificates} شهادةً تقابل "
                f"{square.fiber_product_pairs} زوجًا، بلا ناقصٍ ولا رفعٍ مزدوج، "
                f"و{partitions.fold_unfold_losses} فقدًا في الطيّ والفكّ"
            ),
            limit="W رسومٌ بلغت الحاملَ البنيويّ، لا وحداتٌ معجميّةٌ مرخَّصة.",
        ),
        Claim(
            wording="معكوسٌ وحيدٌ للرسم من الذرّات والأدوار وحدَها",
            verdict=(
                ClaimVerdict.FAIL
                if fibers.no_retraction_recovers_the_rasm
                else ClaimVerdict.PASS
            ),
            evidence=(
                f"{len(fibers.collided_fibers)} ليفًا تضمّ "
                f"{fibers.forms_inside_collisions} شكلًا فعليًّا متطابقَ الإسقاط"
            ),
            limit=(
                "تفنيدٌ للاسترجاع الوحيد وحدَه؛ لا يمسّ توليدًا متعدّدَ المخرجات "
                "ولا نموذجًا يحمل سجلَّ الهويّة."
            ),
        ),
        Claim(
            wording="ديكارتيّةُ جميع الانتقالات حتّى الإفادة",
            verdict=ClaimVerdict.DEFER,
            evidence="مربّعاتُ G4..G8 ومراجعُها غيرُ معيَّنةٍ في المادّة المفحوصة",
            limit="عدمُ استحقاقِ شهادةٍ الآن، لا حكمٌ باستحالةٍ ولا تفنيدٌ عامّ.",
        ),
        Claim(
            wording="بعدٌ هاوسدورفيٌّ موجبٌ للدوالّ المنتهية المرمَّزة من 116",
            verdict=(
                ClaimVerdict.FAIL
                if hausdorff.a_positive_dimension_is_refused
                else ClaimVerdict.DEFER
            ),
            evidence=(
                f"|Aⁿ|={hausdorff.alphabet_size}ⁿ منتهٍ فالاتّحادُ معدود، "
                f"ومجموعُ الغطاء {hausdorff.covering_sum:.3e} ≤ {hausdorff.epsilon:.0e}"
            ),
            limit=(
                "يُبطِل الصيغةَ الهندسيّةَ على السلاسل المنتهية؛ ولا ينفي بعدًا "
                "صندوقيًّا ولا تشابهًا بنيويًّا ولا إشارةً صوتيّةً متّصلة."
            ),
        ),
        Claim(
            wording="IFS لغويٌّ أو تشابهٌ ذاتيٌّ بنيويٌّ بين الطبقات",
            verdict=ClaimVerdict.DEFER,
            evidence="لا متريّةَ ولا خرائطَ تحجيمٍ ولا علاقةَ تشابهٍ مُعيَّنةٌ بعد",
            limit="التأجيلُ لغيابِ التعيين، لا لفشلٍ مقيس.",
        ),
    )


# ---------------------------------------------------------------------------
# سابعًا: مقابلةُ المنقول بالمقيس
# ---------------------------------------------------------------------------

THE_STUDY_FIGURES: Final[tuple[Figure, ...]] = (
    Figure(
        name="أليافُ الإسقاط المتصادمة",
        value=18,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من الدراسة الثانية قبل إعادة الحساب.",
    ),
    Figure(
        name="الأشكالُ داخل هذه الألياف",
        value=36,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من الدراسة الثانية قبل إعادة الحساب.",
    ),
    Figure(
        name="أليافٌ يفصلها دورٌ صوتيّ",
        value=0,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من الدراسة الثانية قبل إعادة الحساب.",
    ),
    Figure(
        name="أشكالٌ بأكثر من تقسيم",
        value=0,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من الدراسة الثانية قبل إعادة الحساب.",
    ),
    Figure(
        name="فقدُ ذرّاتٍ في الطيّ والفكّ",
        value=0,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من الدراسة الثانية قبل إعادة الحساب.",
    ),
    Figure(
        name="أشكالٌ بلا تقسيمٍ سوى البادئ بساكن",
        value=385,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من الدراسة الثانية؛ ويُقابَل بالقسم الثاني وحدَه.",
    ),
)

THE_STUDY_TOTALS_THAT_ARE_NOT_REPRODUCED: Final[tuple[Figure, ...]] = (
    Figure(
        name="الأشكالُ الجاهزة",
        value=9554,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="جسرُ الدراسة غيرُ هذا الجسر؛ الفرقُ يُسمّى ولا يُقرَّب.",
    ),
    Figure(
        name="|W| ذوو التقسيم الواحد",
        value=9169,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="جسرُ الدراسة غيرُ هذا الجسر؛ الفرقُ يُسمّى ولا يُقرَّب.",
    ),
)


def rows() -> Iterator[str]:
    """عرضٌ نصّيٌّ موجزٌ للقناة؛ للقراءة لا للاستناد."""

    fibers = fiber_reading()
    partitions = partition_reading()
    square = square_reading()
    yield f"توقيعُ المالك: {OWNER_SIGNATURE.owner} — {OWNER_SIGNATURE.granted_on}"
    yield (
        f"أشكالٌ جاهزة {fibers.forms} · تسلسلاتٌ مختلفة {fibers.distinct_atom_sequences}"
    )
    yield (
        f"أليافٌ متصادمة {len(fibers.collided_fibers)} · "
        f"أشكالٌ فيها {fibers.forms_inside_collisions}"
    )
    yield (
        f"تقسيمٌ واحد {partitions.exactly_one} · "
        f"بادئٌ بساكن {partitions.starts_with_a_sakin} · "
        f"بلا تقسيمٍ سواه {partitions.other_without_a_partition} · "
        f"أكثر من تقسيم {partitions.more_than_one}"
    )
    yield (
        f"|W|={square.w} |X|={square.x} |S|={square.s} "
        f"|P|={square.certificates} |W×ₓS|={square.fiber_product_pairs}"
    )
    yield f"θ تقابل: {square.theta_is_a_bijection}"
    for claim in verdict_table():
        yield f"[{claim.verdict.value}] {claim.wording}"
