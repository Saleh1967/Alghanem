"""القناةُ الخامسة: تصحيحُ ما نبّه عليه التقييمُ، مقيسًا لا مُقَرًّا به لفظًا.

تشتغل بتوقيع المالك المستورَد من :mod:`canonical116.owner_experiment`. وهي
ملفٌّ يُزاد ويُحذَف بتمامه، ولا يُعدِّل بايتةً في حارسٍ قائم — بما في ذلك
القنواتُ الأربعُ السابقة: ما صحّ منها يبقى، وما قُيِّد يُقيَّد **ههنا** بقيدٍ
مقيسٍ يُقرأ معه، لا بحذفِ أثرِ الخطأ.

المآخذُ المصحَّحة، كلٌّ بقياسه:

**(١) المربّعُ يُعيد استعمال البناء نفسَه.** صحيح. في
:func:`canonical116.dal_claim_test.square_reading` يُبنى المرجعُ ``s`` من
``certificates.values()``، والشهاداتُ نفسُها من ``every_partition_of``؛ فطرفا
المقابلة مشتقّان من الدالّة الواحدة. ويُقاس ههنا سببُ ذلك: الجسرُ **لا يُخرِج
تقسيمًا مقطعيًّا أصلًا** — مفاتيحُ تقريره لا تحمل مقاطع — فلا تقسيمَ تنفيذٍ
أصليٍّ في الشجرة يُقابَل به. وأقصى ما أمكن ههنا ضبطٌ **مستقلُّ الاستراتيجيّة**
لا مستقلُّ القواعد: محلّلٌ جشعٌ من اليسار يُقابَل بالاستنفاد
(`AN_INDEPENDENT_STRATEGY_IS_NOT_AN_INDEPENDENT_RULE_SET`).

وظهر في القياس ما هو أثقلُ من المأخذ: **لا شكلَ واحدًا** من 9,380 يُخرِج
تقسيمَين. فالاستنفادُ **خامدٌ** على هذا المُودَع، والجشعُ يُطابقه في 8,510
ويرفض ما يرفضه (870). فالمربّعُ لم يكن ليختلف لو بُني على الجشع
(`AN_EXHAUSTIVE_PARSER_THAT_NEVER_BRANCHES_IS_A_DETERMINISTIC_ONE`).

**(٦أ) وهذا تصحيحٌ لحكمي أنا، لا تقييدٌ له.** قلتُ إنّ «الأدوار لا تفصل واحدًا
من الألياف الثمانيةَ عشر». هذا صحيحٌ لـ``role_signature`` وحدَه (أصنافُ
المقاطع)، و**باطلٌ** لأدوار عناقيد الجسر: فهي تفصل **إحدى عشرةَ** من الثمانيةَ
عشر — عائلةَ التاء المربوطة كلَّها، وفيها «نِعْمَةَ»/«نِعْمَتَ» شاهدُ التفنيد
في الدراسة الأولى. فالشاهدُ **مرفوعٌ بحقلٍ حاضرٍ في تقرير الجسر**
(`A_RESULT_PROVED_FOR_ONE_DEFINITION_OF_ROLE_DOES_NOT_TRANSFER_TO_ANOTHER`).

**(٤) ويتبع ذلك تنازلٌ عن اعتراضي في القناة الرابعة.** قلتُ إنّ البصمةَ وحدَها
ترفع التصادم. والمقيسُ أنّ حقل ``base`` في عناقيد الجسر يفصل **الثمانيةَ عشرَ
كلَّها**: الرسمُ محفوظٌ في التقرير نفسِه، فلا يلزم الرجوعُ إلى البصمة ولا إلى
البايتات للتمييز. واعتراضي كان على ``canonical_text`` بعينه، وهو خامدٌ كما قيس؛
أمّا جسرُك فيُقابِل النصَّ الأصليَّ المستخرَجَ من المصدر، وهو **يُميِّز**
(`THE_RASM_IS_RETAINED_IN_THE_REPORT_AND_NOT_ONLY_IN_THE_DIGEST`).

**(٢) اتّصالُ البصمات في المسار الرأسيّ مقطوعٌ في ثلاث وصلات.** صحيح ومقيس:
من ثماني وصلاتٍ بين تسع مراحل، خمسٌ متّصلةٌ (مخرجُ السابقة هو مدخلُ اللاحقة)
وثلاثٌ مقطوعة — ``SYLLABLE`` و``WORD_STRUCTURE`` و``CASE_MARK`` تأخذ جميعًا
بصمةَ ``WORD_SPLIT`` لا بصمةَ سابقتها. فتعاقبُ الأسماء ليس اتّصالًا
(`A_SEQUENCE_OF_STAGE_NAMES_IS_NOT_A_CHAIN_OF_DIGESTS`).

**(٣) والحركتان لا تعيّنان العلاقة.** مثالُك قيس فأصاب: «الطَّالِبُ
الْمُجْتَهِدُ» يُقرأ ``إسناد`` و``مُفيد`` بشاهدِ ضمّتين — وهو نعتٌ لا إسناد.
فهذا **قبولٌ خاطئٌ مقيسٌ** لا احتمالٌ نظريّ. وتصريحُ الوحدة بأنّ ``CASE_MARK
!= I'RAB`` يضبط ما تدّعيه، ولا يرفع القبولَ الخاطئ
(`DECLARING_A_LIMIT_DOES_NOT_REMOVE_A_FALSE_ADMISSION`).

**(٦ب) ومجموعُ الأعداد لا يُغني عن دفتر.** فبُني ههنا دفترُ وقوعاتٍ يُسند كلَّ
وقوعٍ إلى صنفٍ واحدٍ ويُحصي الإسنادات، فيُثبَت التنافرُ والاستغراقُ بالسجلّ لا
بالجمع.

**وما بقي على حاله:** دعوى اتّحاد المصدر من تساوي الوحدات لم أقُل بها — سمّيتُ
البقيّةَ 816 «غيرَ مُفسَّرة» ومنعتُ صرفَها بالقول وحده؛ والمحاذاةُ التي
تطلبها تحتاج ملفَّ QAC وهو غائبٌ عن الشجرة. وإثباتُ اتّصال الطبقات والإفادة
يبقى غيرَ مستوفًى.
"""

from __future__ import annotations

import collections
import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import Final

from .bridge_v1_0 import SUKUN, bridge
from .dal_claim_test import (
    MADD_ATOMS,
    Partition,
    Syllable,
    every_partition_of,
    ready_forms,
)
from .owner_experiment import OWNER_SIGNATURE, REPOSITORY_ROOT, read_deposit

__all__ = [
    "AN_EXHAUSTIVE_PARSER_THAT_NEVER_BRANCHES_IS_A_DETERMINISTIC_ONE",
    "AN_INDEPENDENT_STRATEGY_IS_NOT_AN_INDEPENDENT_RULE_SET",
    "A_RESULT_PROVED_FOR_ONE_DEFINITION_OF_ROLE_DOES_NOT_TRANSFER_TO_ANOTHER",
    "A_SEQUENCE_OF_STAGE_NAMES_IS_NOT_A_CHAIN_OF_DIGESTS",
    "DECLARING_A_LIMIT_DOES_NOT_REMOVE_A_FALSE_ADMISSION",
    "THE_RASM_IS_RETAINED_IN_THE_REPORT_AND_NOT_ONLY_IN_THE_DIGEST",
    "ChainReading",
    "CorrectedClaim",
    "SeparationReading",
    "corrected_claims",
    "digest_chain_reading",
    "false_admission_reading",
    "greedy_partition_of",
    "independence_reading",
    "occurrence_ledger",
    "rows",
    "separating_field_readings",
    "the_bridge_emits_no_syllable_partition",
]


AN_INDEPENDENT_STRATEGY_IS_NOT_AN_INDEPENDENT_RULE_SET: Final[str] = (
    "AN_INDEPENDENT_STRATEGY_IS_NOT_AN_INDEPENDENT_RULE_SET: محلّلٌ يُطبِّق "
    "القواعدَ نفسَها بترتيبِ اختيارٍ آخرَ يضبط الخوارزميّة، ولا يصير مرجعًا "
    "مستقلًّا عنها؛ فاتّفاقُهما يُثبت أنّ القواعد أوجبت الناتج لا أنّها صحيحة."
)

AN_EXHAUSTIVE_PARSER_THAT_NEVER_BRANCHES_IS_A_DETERMINISTIC_ONE: Final[str] = (
    "AN_EXHAUSTIVE_PARSER_THAT_NEVER_BRANCHES_IS_A_DETERMINISTIC_ONE: استنفادٌ "
    "لا يُخرِج تقسيمَين في موضعٍ واحدٍ من المُودَع كلِّه لا يُشترى باستنفاده "
    "شيءٌ ههنا؛ فالوحدانيّةُ خاصّةُ المادّة لا ظفرُ الخوارزميّة."
)

A_RESULT_PROVED_FOR_ONE_DEFINITION_OF_ROLE_DOES_NOT_TRANSFER_TO_ANOTHER: Final[str] = (
    "A_RESULT_PROVED_FOR_ONE_DEFINITION_OF_ROLE_DOES_NOT_TRANSFER_TO_ANOTHER: "
    "«الأدوار» في توقيع المقاطع غيرُ «الأدوار» في عناقيد الجسر؛ والأولى دالّةٌ "
    "في الذرّات فلا تفصل، والثانيةُ تفصل إحدى عشرةَ ليفًا. فلا يُنقَل حكمُ "
    "إحداهما إلى الأخرى بغير مقابلة الحقول."
)

THE_RASM_IS_RETAINED_IN_THE_REPORT_AND_NOT_ONLY_IN_THE_DIGEST: Final[str] = (
    "THE_RASM_IS_RETAINED_IN_THE_REPORT_AND_NOT_ONLY_IN_THE_DIGEST: حقلُ "
    "`base` في العناقيد يفصل الألياف الثمانيةَ عشرَ كلَّها؛ فحفظُ الرسم لا "
    "يتوقّف على البصمة، والاعتراضُ إنّما يصحّ على `canonical_text` بعينه."
)

A_SEQUENCE_OF_STAGE_NAMES_IS_NOT_A_CHAIN_OF_DIGESTS: Final[str] = (
    "A_SEQUENCE_OF_STAGE_NAMES_IS_NOT_A_CHAIN_OF_DIGESTS: مراحلُ مرتّبةُ "
    "الأسماء تأخذ جميعًا بصمةَ مرحلةٍ واحدةٍ سابقة؛ فالترتيبُ معلنٌ والاتّصالُ "
    "غيرُ مُثبَتٍ إلّا حيث طابق مخرجُ السابقة مدخلَ اللاحقة."
)

DECLARING_A_LIMIT_DOES_NOT_REMOVE_A_FALSE_ADMISSION: Final[str] = (
    "DECLARING_A_LIMIT_DOES_NOT_REMOVE_A_FALSE_ADMISSION: تصريحُ وحدةٍ بأنّ "
    "مخرجها مرشَّحٌ لا برهان يضبط ما تدّعيه ولا يمنع قبولَها تركيبًا وصفيًّا "
    "إسنادًا؛ فالقبولُ الخاطئُ يُقاس ويُسمّى ولو كان الحدُّ معلنًا."
)


# ---------------------------------------------------------------------------
# أوّلًا: هل في الجسر تقسيمٌ مقطعيٌّ يُقابَل به أصلًا؟
# ---------------------------------------------------------------------------

_CONTEXT: Final[dict[int, dict[str, str]]] = {0: {"entry": "start", "exit": "continue"}}


def the_bridge_emits_no_syllable_partition() -> tuple[str, ...]:
    """مفاتيحُ تقرير الجسر؛ وليس فيها مقاطعُ، فلا تقسيمَ تنفيذٍ يُقابَل به."""

    report = bridge("بِسْمِ", contexts=_CONTEXT)
    cluster_keys = tuple(sorted(report["words"][0]["clusters"][0]))
    return tuple(sorted(report)) + cluster_keys


# ---------------------------------------------------------------------------
# ثانيًا: ضبطٌ مستقلُّ الاستراتيجيّة — الجشعُ مقابلَ الاستنفاد
# ---------------------------------------------------------------------------


def greedy_partition_of(atoms: tuple[str, ...]) -> Partition | None:
    """جشعٌ من اليسار: أطولُ مقطعٍ ممكنٍ عند كلّ موضع، بلا تراجعٍ ولا تفريع.

    يُطبِّق القواعدَ المُعلَنةَ نفسَها بترتيبِ اختيارٍ مخالف؛ فهو ضبطٌ لاختيار
    الخوارزميّة لا مرجعٌ لغويٌّ ولا قواعدُ أخرى.
    """

    built: list[tuple[Syllable, tuple[str, ...]]] = []
    position, length = 0, len(atoms)
    while position < length:
        head = atoms[position]
        if head.endswith(SUKUN):
            return None
        if position + 1 < length and atoms[position + 1].endswith(SUKUN):
            tail = atoms[position + 1]
            kind = Syllable.CVV if tail in MADD_ATOMS else Syllable.CVC
            built.append((kind, (head, tail)))
            position += 2
        else:
            built.append((Syllable.CV, (head,)))
            position += 1
    return tuple(built)


@dataclass(frozen=True)
class IndependenceReading:
    """مقابلةُ الجشع بالاستنفاد، ومعها عددُ المواضع التي فرّع فيها الاستنفاد."""

    forms: int
    exhaustive_unique: int
    exhaustive_branched: int
    exhaustive_refused: int
    greedy_agrees: int
    greedy_disagrees: int
    greedy_refuses: int

    @property
    def the_exhaustion_is_inert(self) -> bool:
        """استنفادٌ لم يُفرّع مرّةً واحدةً لا يُضيف على الجشع شيئًا ههنا."""

        return self.exhaustive_branched == 0

    @property
    def the_two_strategies_never_disagree(self) -> bool:
        return self.greedy_disagrees == 0


@lru_cache(maxsize=1)
def independence_reading() -> IndependenceReading:
    """يُشغَّل المحلّلان على الأشكال الجاهزة كلِّها، لا على عيّنةٍ منها."""

    forms = ready_forms()
    unique = branched = refused = agrees = disagrees = greedy_refuses = 0
    for atoms in forms.values():
        partitions = every_partition_of(atoms)
        greedy = greedy_partition_of(atoms)
        if greedy is None:
            greedy_refuses += 1
        if len(partitions) == 1:
            unique += 1
            if greedy == partitions[0]:
                agrees += 1
            else:
                disagrees += 1
        elif partitions:
            branched += 1
        else:
            refused += 1
    return IndependenceReading(
        forms=len(forms),
        exhaustive_unique=unique,
        exhaustive_branched=branched,
        exhaustive_refused=refused,
        greedy_agrees=agrees,
        greedy_disagrees=disagrees,
        greedy_refuses=greedy_refuses,
    )


# ---------------------------------------------------------------------------
# ثالثًا: أيُّ حقلٍ في تقرير الجسر يفصل الألياف المتصادمة؟
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SeparationReading:
    """حقلٌ من تقرير الجسر، وكم ليفًا متصادمًا يفصل."""

    field: str
    separated: int
    of_total: int
    residue: tuple[tuple[str, ...], ...]

    @property
    def separates_them_all(self) -> bool:
        return self.separated == self.of_total


@lru_cache(maxsize=1)
def _ready_reports() -> tuple[tuple[str, dict], ...]:
    text, _ = read_deposit()
    reports = []
    for form in sorted({token for token in text.split() if token != "<sel>"}):
        report = bridge(form, contexts=_CONTEXT)
        if report["status"] == "READY":
            reports.append((form, report))
    return tuple(reports)


def _colliding_fibers() -> tuple[tuple[str, ...], ...]:
    fibers: dict[tuple[str, ...], list[str]] = collections.defaultdict(list)
    for form, report in _ready_reports():
        fibers[tuple(report["canonical_atoms"])].append(form)
    return tuple(tuple(members) for members in fibers.values() if len(members) > 1)


def separating_field_readings() -> tuple[SeparationReading, ...]:
    """ثلاثةُ حقولٍ تُستخرَج من العناقيد نفسِها وتُقاس على الألياف كلِّها."""

    reports = dict(_ready_reports())

    def clusters(form: str, key: str) -> tuple[object, ...]:
        return tuple(
            cluster[key]
            for word in reports[form]["words"]
            for cluster in word["clusters"]
        )

    def reading(form: str) -> tuple[object, ...]:
        return tuple(
            tuple(sorted(cluster["reading"].items()))
            for word in reports[form]["words"]
            for cluster in word["clusters"]
        )

    fibers = _colliding_fibers()
    out: list[SeparationReading] = []
    for field, extract in (
        ("base", lambda form: clusters(form, "base")),
        ("role", lambda form: clusters(form, "role")),
        ("reading", reading),
    ):
        residue = tuple(
            members
            for members in fibers
            if len({extract(form) for form in members}) == 1
        )
        out.append(
            SeparationReading(
                field=field,
                separated=len(fibers) - len(residue),
                of_total=len(fibers),
                residue=residue,
            )
        )
    return tuple(out)


def role_residue_classes() -> tuple[tuple[str, tuple[tuple[str, ...], ...]], ...]:
    """ما لم تفصله الأدوارُ يُسمّى صنفَين لا رقمًا: مقعدُ الهمزة، والألفُ."""

    residue = {
        reading.field: reading.residue for reading in separating_field_readings()
    }["role"]
    seated = tuple(pair for pair in residue if any("ئ" in form for form in pair))
    alif = tuple(pair for pair in residue if pair not in seated)
    return (("مقعدُ الهمزة", seated), ("الألفُ المقصورة", alif))


# ---------------------------------------------------------------------------
# رابعًا: سلسلةُ البصمات في المسار الرأسيّ
# ---------------------------------------------------------------------------


def _load_ifada_path():  # noqa: ANN202 - وحدةٌ تُحمَّل أو لا تُحمَّل
    source_root = REPOSITORY_ROOT / "src"
    if source_root.is_dir() and str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))
    try:
        from alghanem.arabic import composition_ifada_path
    except ImportError:  # pragma: no cover - مسارُ غيابِ الحزمة
        return None
    return composition_ifada_path


@dataclass(frozen=True)
class ChainReading:
    """وصلاتُ البصمات بين المراحل: ما اتّصل، وما انقطع بأسمائه."""

    stages: int
    links: int
    chained: int
    broken: tuple[str, ...]

    @property
    def the_chain_is_unbroken(self) -> bool:
        return not self.broken


THE_CHAIN_INPUT: Final[str] = "اللَّهُ نُورٌ"


def digest_chain_reading(text: str = THE_CHAIN_INPUT) -> ChainReading | None:
    """هل مدخلُ كلّ مرحلةٍ هو مخرجُ سابقتها فعلًا؟ تُقرأ البصماتُ لا الأسماء."""

    module = _load_ifada_path()
    if module is None:  # pragma: no cover - مسارُ غيابِ الحزمة
        return None
    stages = module.run_text(text).stages
    broken: list[str] = []
    chained = 0
    for previous, current in zip(stages, stages[1:], strict=False):
        if current.input_digest == previous.output_digest:
            chained += 1
        else:
            broken.append(current.stage.value)
    return ChainReading(
        stages=len(stages),
        links=len(stages) - 1,
        chained=chained,
        broken=tuple(broken),
    )


# ---------------------------------------------------------------------------
# خامسًا: القبولُ الخاطئ — الحركتان لا تعيّنان العلاقة
# ---------------------------------------------------------------------------

THE_DESCRIPTIVE_PAIR: Final[str] = "الطَّالِبُ الْمُجْتَهِدُ"
THE_PREDICATIVE_PAIR: Final[str] = "اللَّهُ نُورٌ"


def false_admission_reading() -> tuple[tuple[str, str, str, str], ...]:
    """تركيبان مرفوعا الطرفين: نعتٌ وإسناد؛ ويُقرآن قراءةً واحدة."""

    module = _load_ifada_path()
    if module is None:  # pragma: no cover - مسارُ غيابِ الحزمة
        return ()
    out: list[tuple[str, str, str, str]] = []
    for text in (THE_PREDICATIVE_PAIR, THE_DESCRIPTIVE_PAIR):
        run = module.run_text(text)
        record = run.record
        out.append(
            (
                text,
                run.composition.value if run.composition else "—",
                record.declared_ifada.value if record else "—",
                record.benefit_witness if record else "—",
            )
        )
    return tuple(out)


# ---------------------------------------------------------------------------
# سادسًا: دفترُ الوقوعات — التنافرُ والاستغراقُ بسجلٍّ لا بجمع
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LedgerReading:
    """كلُّ وقوعٍ أُسنِد كم مرّة؟ والدفترُ يُجيب، لا مجموعُ الأصناف."""

    occurrences: int
    assignments: int
    assigned_once: int
    assigned_twice_or_more: int
    assigned_never: int

    @property
    def is_a_partition(self) -> bool:
        return (
            self.assigned_once == self.occurrences
            and self.assigned_twice_or_more == 0
            and self.assigned_never == 0
            and self.assignments == self.occurrences
        )


def occurrence_ledger() -> LedgerReading:
    """يُبنى الدفترُ بموضع كلِّ وقوعٍ لا بعدّ أشكاله، ثمّ تُحصى الإسنادات."""

    text, _ = read_deposit()
    tokens = [token for token in text.split() if token != "<sel>"]
    status_of = {
        form: bridge(form, contexts=_CONTEXT)["status"] for form in sorted(set(tokens))
    }
    assignments: collections.Counter[int] = collections.Counter()
    for position, token in enumerate(tokens):
        for status in ("READY", "DEFER"):
            if status_of[token] == status:
                assignments[position] += 1
    return LedgerReading(
        occurrences=len(tokens),
        assignments=sum(assignments.values()),
        assigned_once=sum(1 for count in assignments.values() if count == 1),
        assigned_twice_or_more=sum(1 for count in assignments.values() if count > 1),
        assigned_never=len(tokens) - len(assignments),
    )


# ---------------------------------------------------------------------------
# سابعًا: ما صحّحتُه من قولي، مُسمًّى لا مطويًّا
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CorrectedClaim:
    """دعوى قلتُها، وموضعُها، وما يُقيِّدها أو يُبطلها، وبأيِّ قياس."""

    said: str
    where: str
    correction: str
    measured: str
    is_withdrawn: bool


def corrected_claims() -> tuple[CorrectedClaim, ...]:
    """تُبنى من القياس لا من النصّ؛ وكلُّ رقمٍ فيها يُشتَقّ عند القراءة."""

    separation = {item.field: item for item in separating_field_readings()}
    chain = digest_chain_reading()
    return (
        CorrectedClaim(
            said="إضافةُ الأدوار لا تفصل واحدًا من الألياف الثمانيةَ عشر",
            where="canonical116/dal_claim_test.py"
            ":ADDING_THE_ROLES_SEPARATES_NOT_ONE_OF_THE_EIGHTEEN_FIBERS",
            correction=(
                "صحيحةٌ لتوقيع المقاطع وحدَه؛ وأدوارُ عناقيد الجسر تفصل "
                f"{separation['role'].separated} منها"
            ),
            measured=f"role: {separation['role'].separated}/18",
            is_withdrawn=False,
        ),
        CorrectedClaim(
            said="لا يرفع التصادمَ إلّا بصمةُ المصدر",
            where="canonical116/certificate_handoff_test.py"
            ":PINNING_THE_CANONICAL_TEXT_IS_INERT_WHERE_THE_RASM_COLLIDES",
            correction=(
                "حقلُ `base` في التقرير نفسِه يفصلها كلَّها؛ فالاعتراضُ يصحّ "
                "على `canonical_text` بعينه لا على كلّ نصّ"
            ),
            measured=f"base: {separation['base'].separated}/18",
            is_withdrawn=True,
        ),
        CorrectedClaim(
            said="المربّعُ يقابل الشهاداتِ بمرجعٍ استنفاديّ",
            where="canonical116/dal_claim_test.py:square_reading",
            correction=(
                "طرفاه من `every_partition_of` نفسِها؛ ولا تقسيمَ في تقرير "
                "الجسر يُقابَل به، والاستنفادُ لم يُفرّع مرّةً واحدة"
            ),
            measured=(
                f"تفريعاتٌ: {independence_reading().exhaustive_branched}؛ "
                f"واتّفاقُ الجشع: {independence_reading().greedy_agrees}"
            ),
            is_withdrawn=False,
        ),
        CorrectedClaim(
            said="المسارُ الرأسيُّ موصولٌ، مخرجُ كلِّ طبقةٍ مدخلُ التي تليها",
            where="canonical116/birth_law_test.py (الوصف)",
            correction="ثلاثُ وصلاتٍ من ثمانٍ مقطوعةٌ في البصمات",
            measured=(
                f"متّصلة {chain.chained}/{chain.links}؛ المقطوعةُ: "
                f"{'، '.join(chain.broken)}"
                if chain
                else "—"
            ),
            is_withdrawn=True,
        ),
        CorrectedClaim(
            said="سجلّان مغلقان يَردّان دعوى غياب بوّابة الإفادة",
            where="canonical116/birth_law_test.py:ifada_gate_readings",
            correction=(
                "وجودُ البوّابة باقٍ؛ لكنّ إغلاقَها يقبل نعتًا إسنادًا، "
                "فلا يُقرأ سجلُّها شهادةَ علاقةٍ ولا إفادةٍ لغويّة"
            ),
            measured="الطَّالِبُ الْمُجْتَهِدُ ⇐ إسناد/مُفيد",
            is_withdrawn=False,
        ),
    )


def rows() -> list[str]:
    """تقريرٌ نصّيٌّ يُطبَع؛ كلُّ رقمٍ فيه يُشتَقّ عند التشغيل."""

    reading = independence_reading()
    chain = digest_chain_reading()
    lines = [
        f"توقيعُ المالك: {OWNER_SIGNATURE.owner} — {OWNER_SIGNATURE.granted_on}",
        "",
        "(١) الجشعُ مقابلَ الاستنفاد:",
        f"  الأشكالُ الجاهزة: {reading.forms}",
        f"  تقسيمٌ وحيد: {reading.exhaustive_unique} · تفريعٌ: "
        f"{reading.exhaustive_branched} · رفضٌ: {reading.exhaustive_refused}",
        f"  الجشعُ يوافق: {reading.greedy_agrees} · يخالف: "
        f"{reading.greedy_disagrees} · يرفض: {reading.greedy_refuses}",
        "",
        "(٦أ) الحقولُ التي تفصل الألياف المتصادمة:",
    ]
    for item in separating_field_readings():
        lines.append(f"  {item.field}: {item.separated}/{item.of_total}")
    lines.append("  وبقيّةُ الأدوار صنفان:")
    for name, pairs in role_residue_classes():
        lines.append(f"    {name}: {len(pairs)} — {[list(p) for p in pairs]}")
    lines += ["", "(٢) سلسلةُ البصمات في المسار الرأسيّ:"]
    if chain is not None:
        lines.append(
            f"  مراحل {chain.stages} · وصلات {chain.links} · متّصلة "
            f"{chain.chained} · مقطوعة {len(chain.broken)}: "
            f"{'، '.join(chain.broken)}"
        )
    lines += ["", "(٣) قراءةُ الحركتين:"]
    for text, composition, ifada, witness in false_admission_reading():
        lines.append(f"  {text}: {composition}/{ifada} — {witness}")
    ledger = occurrence_ledger()
    lines += [
        "",
        "(٦ب) دفترُ الوقوعات:",
        f"  وقوعات {ledger.occurrences} · إسنادات {ledger.assignments} · "
        f"مرّةً واحدة {ledger.assigned_once} · أكثر "
        f"{ledger.assigned_twice_or_more} · بلا إسناد {ledger.assigned_never}",
        "",
        "ما صُحِّح من قولي:",
    ]
    for claim in corrected_claims():
        mark = "مسحوبة" if claim.is_withdrawn else "مقيَّدة"
        lines.append(f"  [{mark}] {claim.said}")
        lines.append(f"      {claim.correction} ({claim.measured})")
    return lines


if __name__ == "__main__":  # pragma: no cover - تشغيلٌ يدويّ
    print("\n".join(rows()))
