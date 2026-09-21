"""إغلاقُ فرعِ العدِّ التوكنيّ الخام: أثرٌ معجميٌّ مُشخَّصٌ لا رقمٌ دون العتبة.

**أوّلًا: والإغلاقُ ليس حذفًا، وليس «دون العتبة».** حين تُستبعَد دعوى، فلها
منزلتان لا تُخلَطان: أن تُقاس فتقصُر عن عتبةٍ مُعلَنة، وأن **تُشخَّص آليةُ
فسادها** فتخرج من باب الدليل الصوتيّ أصلًا. الأولى تبقى مرشَّحةً لعيّنةٍ أكبر،
والثانية لا تُعيدها عيّنةٌ أكبر، لأنّ التوسيعَ يزيد الآليةَ قوّةً لا ضعفًا.
فَوُضِع للثانية موقفٌ باسمه `CLOSED_AS_LEXICAL_ARTIFACT`، ومُنِع أن يُكتَب
موقفُ دعوًى مُغلَقةٍ `BELOW_THRESHOLD`
(`A_CLOSED_ARTIFACT_IS_NOT_A_FIGURE_BELOW_A_THRESHOLD`).

**وثانيًا: والآليةُ مسمّاةٌ لا موصوفة.** الفسادُ ههنا `TOKEN_REPETITION_INFLATION`:
أن يُعَدَّ الحضورُ توكنًا توكنًا، فتُصبح كلمةٌ واحدةٌ شديدةُ التكرار دليلًا
مُضاعَفًا على نفسها. وهذا يُصيب كلَّ دعوى **حضورٍ** تُقاس على التوكنات، ولا
يُصيب دعوى **غيابٍ** بالقدر نفسِه، لأنّ تكرارَ كلمةٍ لا يملأ خليةً فارغة.

**وثالثًا: وللآلية شاهدٌ مُودَعٌ في الشجرة، لا استشهادٌ من خارج.** تقريرُ
التحقيق التوزيعيّ (`distributional_probe_report`) قِيس على 2,193 شكلًا سطحيًّا
بشرط دعمٍ ≥ 5، فكان أفضلُ k هو **2 لا 3**، بتقسيمٍ غيرِ متوازن **2,159 مقابل
34**. والعنقودُ الصغيرُ لم يكن فئةً نحويّة: فيه حروفٌ حقيقيّة (في، من، على،
لا) **مختلطةً بكلمات محتوًى فائقةِ التكرار** (الله، الذين، ما، قال، كان).
فالعدُّ التوكنيُّ الخام لم يُخرِج مقولةً لغويّة، بل أخرج ما يتكرّر كثيرًا —
وهذا هو الأثرُ المعجميُّ بعينه (`THE_MECHANISM_HAS_A_DEPOSITED_WITNESS`).

**ورابعًا: ونصيبُ التكرار مقيسٌ على الودائع الحاضرة.** لا يُقال «التكرار
يضخّم» إرسالًا، بل يُقاس نصيبُ ما ليس شاهدًا جديدًا من التوكنات:

\\[
ExposedShare = \\frac{Tokens - Types}{Tokens}
\\]

| الوديعة | الطبقة | توكنات | أنماط | أعلى نمط | نصيبُه | النصيبُ المُعرَّض |
|---|---|---|---|---|---|---|
| الفاتحة | مكتوبة | 29 | 26 | 2 | 6.897% | 10.345% |
| الفاتحة | مُسقَطة | 29 | 26 | 2 | 6.897% | 10.345% |
| الفتح ٢٩ | مكتوبة | 54 | 50 | 3 | 5.556% | 7.407% |
| الفتح ٢٩ | مُسقَطة | 54 | 47 | 3 | 5.556% | 12.963% |

فعلى ثلاثٍ وثمانين كلمةً تكفي كلمةٌ واحدةٌ لتحريك نسبةٍ بنقاط. والأعدادُ
مشتقّةٌ عند القراءة من بايتات الإيداع، لا منقولةً إلى هذا النثر
(`THE_EXPOSED_SHARE_IS_DERIVED_AT_READ_TIME_NOT_TRANSCRIBED`).

**وخامسًا: والإغلاقُ الجزئيُّ يُقاس ولا يُعمَّم.** «سكون-تراكب» مُغلَقٌ
بتمامه، لأنّ دعواه دعوى حضورٍ تُعَدّ توكنًا توكنًا. أمّا «فتحة-فقط» فلا
يُستبعَد استبعادًا كلّيًّا غيرَ مقيس: يُغلَق منه **نصيبُه المُعرَّض للآلية**
وهو مقيسٌ لا مُقدَّر، ويبقى ما سواه **غيرَ مُغلَقٍ بهذه الآلية** — وليس ذلك
قبولًا له، بل امتناعٌ عن إغلاقه بما لا يُثبِته
(`A_PARTIAL_CLOSURE_CLOSES_ITS_MEASURED_SHARE_AND_NO_MORE`).

**وسادسًا: والمُغلَقُ لا يعود.** أرقامُ دعوًى مُغلَقةٍ لا تدخل تجميدًا ولا
تُستشهَد شاهدًا صوتيًّا؛ و`refuse_to_freeze` ترفضها نصًّا، وحارسُ استيرادٍ
يمنع أن يُوسَم مُغلَقٌ بموقفٍ أضعف من إغلاقه
(`A_CLOSED_CLAIM_DOES_NOT_RE_ENTER_A_FREEZE`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`، ولا
تستورد من `kernel/` شيئًا.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from functools import cache
from typing import Final

from alghanem.arabic.carrier_projection_deposit import (
    THE_DEPOSITS_PROJECTED,
    WordBoundary,
    deposited_text,
    project_word,
    words_of,
)
from alghanem.arabic.distributional_probe_report import RECORDED_PROBE_REPORT

__all__ = [
    "A_CLOSED_ARTIFACT_IS_NOT_A_FIGURE_BELOW_A_THRESHOLD",
    "A_CLOSED_CLAIM_DOES_NOT_RE_ENTER_A_FREEZE",
    "A_PARTIAL_CLOSURE_CLOSES_ITS_MEASURED_SHARE_AND_NO_MORE",
    "LEXICAL_ARTIFACT_NAMED_RESIDUALS",
    "THE_CLOSED_CLAIMS",
    "THE_EXPOSED_SHARE_IS_DERIVED_AT_READ_TIME_NOT_TRANSCRIBED",
    "THE_MECHANISM_HAS_A_DEPOSITED_WITNESS",
    "ClosedClaim",
    "ClosureExtent",
    "CorruptionMechanism",
    "DominanceReading",
    "ExclusionStanding",
    "LexicalArtifactError",
    "ProbeWitness",
    "closed_claim",
    "dominance_of",
    "refuse_to_freeze",
    "the_probe_witness",
]


class LexicalArtifactError(ValueError):
    """رفضٌ عند الإغلاق: موقفٌ لا يُناسب مداه، أو رقمٌ مُغلَقٌ أُريد تجميدُه."""


# --- المواقفُ والآليات -----------------------------------------------------


class ExclusionStanding(Enum):
    """منازلُ الدعوى المستبعَدة، وأُولاها ليست الثانية بحالٍ.

    `BELOW_THRESHOLD` تبقى مرشَّحةً لعيّنةٍ أكبر؛ و`CLOSED_AS_LEXICAL_ARTIFACT`
    لا تعود، لأنّ توسيعَ العيّنة يزيد آليّةَ فسادها قوّةً لا ضعفًا.
    """

    ADMITTED = "مقبولة"
    BELOW_THRESHOLD = "دون-العتبة"
    CLOSED_AS_LEXICAL_ARTIFACT = "مُغلَقة-أثرًا-معجميًّا"


class CorruptionMechanism(Enum):
    """آلياتُ الفساد المسمّاة؛ ولا إغلاقَ بغير واحدةٍ منها."""

    TOKEN_REPETITION_INFLATION = "تضخُّمٌ-بتكرار-التوكن"


class ClosureExtent(Enum):
    """مدى الإغلاق: كلُّ الدعوى أم نصيبُها المقيسُ وحدَه."""

    WHOLE_CLAIM = "الدعوى-كلُّها"
    MEASURED_SHARE_ONLY = "النصيبُ-المقيسُ-وحدَه"


# --- البقايا المسمّاة ------------------------------------------------------

A_CLOSED_ARTIFACT_IS_NOT_A_FIGURE_BELOW_A_THRESHOLD: Final[str] = (
    "A_CLOSED_ARTIFACT_IS_NOT_A_FIGURE_BELOW_A_THRESHOLD: الدعوى المُشخَّصةُ "
    "آليّةُ فسادها لا تُسجَّل «دون العتبة»، لأنّ ما دون العتبة يبقى مرشَّحًا "
    "لعيّنةٍ أكبر، والمُشخَّصُ لا تُصلِحه عيّنةٌ أكبر بل تزيد آليّتَه قوّةً؛ "
    "فالموقفان متمايزان بالتعداد ولا يُحمَل أحدُهما على الآخر"
)

THE_MECHANISM_HAS_A_DEPOSITED_WITNESS: Final[str] = (
    "THE_MECHANISM_HAS_A_DEPOSITED_WITNESS: آليّةُ التضخُّم ليست وصفًا "
    "مُرسَلًا؛ شاهدُها في هذه الشجرة تقريرُ التحقيق التوزيعيّ: 2,193 شكلًا، "
    "وأفضلُ k اثنان لا ثلاثة، وتقسيمٌ 2,159 مقابل 34، والعنقودُ الصغيرُ خلط "
    "حروفًا حقيقيّةً بكلمات محتوًى فائقةِ التكرار؛ فما تجمّع تجمّع بالتكرار "
    "لا بالمقولة"
)

THE_EXPOSED_SHARE_IS_DERIVED_AT_READ_TIME_NOT_TRANSCRIBED: Final[str] = (
    "THE_EXPOSED_SHARE_IS_DERIVED_AT_READ_TIME_NOT_TRANSCRIBED: نصيبُ "
    "التوكنات المُعرَّضُ للآلية — (التوكنات ناقصةَ الأنماط) على التوكنات — "
    "يُقاس من بايتات الإيداع عند كلّ نداء، ولا يُكتَب رقمًا في حقلٍ يُصدَّق "
    "بلا إعادة اشتقاق"
)

A_PARTIAL_CLOSURE_CLOSES_ITS_MEASURED_SHARE_AND_NO_MORE: Final[str] = (
    "A_PARTIAL_CLOSURE_CLOSES_ITS_MEASURED_SHARE_AND_NO_MORE: «فتحة-فقط» "
    "يُغلَق منه نصيبُه المُعرَّض للآلية وهو مقيس، ولا يُستبعَد كلُّه استبعادًا "
    "غيرَ مقيس؛ وما بقي ليس مقبولًا، وإنّما هو غيرُ مُغلَقٍ بهذه الآلية، "
    "والفرقُ بين الأمرين فرقُ ما لم يُثبَت وما ثبت نفيُه"
)

A_CLOSED_CLAIM_DOES_NOT_RE_ENTER_A_FREEZE: Final[str] = (
    "A_CLOSED_CLAIM_DOES_NOT_RE_ENTER_A_FREEZE: أرقامُ دعوًى مُغلَقةٍ لا تدخل "
    "تجميدًا ولا تُستشهَد دليلًا صوتيًّا؛ و`refuse_to_freeze` ترفضها نصًّا، "
    "فلا يعود المُغلَقُ من بابٍ آخر باسمٍ آخر"
)

LEXICAL_ARTIFACT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_CLOSED_ARTIFACT_IS_NOT_A_FIGURE_BELOW_A_THRESHOLD": (
        A_CLOSED_ARTIFACT_IS_NOT_A_FIGURE_BELOW_A_THRESHOLD
    ),
    "THE_MECHANISM_HAS_A_DEPOSITED_WITNESS": THE_MECHANISM_HAS_A_DEPOSITED_WITNESS,
    "THE_EXPOSED_SHARE_IS_DERIVED_AT_READ_TIME_NOT_TRANSCRIBED": (
        THE_EXPOSED_SHARE_IS_DERIVED_AT_READ_TIME_NOT_TRANSCRIBED
    ),
    "A_PARTIAL_CLOSURE_CLOSES_ITS_MEASURED_SHARE_AND_NO_MORE": (
        A_PARTIAL_CLOSURE_CLOSES_ITS_MEASURED_SHARE_AND_NO_MORE
    ),
    "A_CLOSED_CLAIM_DOES_NOT_RE_ENTER_A_FREEZE": (
        A_CLOSED_CLAIM_DOES_NOT_RE_ENTER_A_FREEZE
    ),
}


# --- شاهدُ الآلية ----------------------------------------------------------


@dataclass(frozen=True)
class ProbeWitness:
    """شاهدُ الآلية مقروءًا من تقرير التحقيق، لا منقولًا إلى هذه الوحدة."""

    surface_forms: int
    selected_k: int
    cluster_sizes: tuple[int, ...]
    mixed_members: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.surface_forms < 1:
            raise LexicalArtifactError("شاهدٌ بلا أشكالٍ سطحيّةٍ لا يشهد.")
        if len(self.cluster_sizes) != self.selected_k:
            raise LexicalArtifactError("أحجامُ العناقيد تخالف k المختار.")
        if len(self.mixed_members) < 2:
            raise LexicalArtifactError("اختلاطٌ دون عضوَين لا يُسمّى اختلاطًا.")

    @property
    def smallest_cluster(self) -> int:
        """أصغرُ العناقيد، وهو موضعُ الاختلاط المشهودِ له."""

        return min(self.cluster_sizes)


@cache
def the_probe_witness() -> ProbeWitness:
    """شاهدُ الآلية مشتقًّا من `distributional_probe_report` عند القراءة."""

    report = RECORDED_PROBE_REPORT
    selected = next(
        partition for partition in report.partitions if partition.k == report.selected_k
    )
    layer = report.discovered_layers[0]
    return ProbeWitness(
        surface_forms=report.specification.surface_form_count,
        selected_k=report.selected_k,
        cluster_sizes=selected.cluster_sizes,
        mixed_members=tuple(layer.member_examples),
    )


# --- الهيمنةُ والنصيبُ المُعرَّض ---------------------------------------------


@dataclass(frozen=True)
class DominanceReading:
    """قراءةُ هيمنةٍ على وديعةٍ: أعلى نمطٍ ونصيبُه، والنصيبُ المُعرَّض للتكرار."""

    source_identity: str
    projected: bool
    tokens: int
    types: int
    leading_type: str
    leading_occurrences: int

    def __post_init__(self) -> None:
        if self.tokens < 1:
            raise LexicalArtifactError("وديعةٌ بلا توكناتٍ لا تُقاس هيمنتُها.")
        if not 1 <= self.types <= self.tokens:
            raise LexicalArtifactError("عددُ الأنماط خارجَ ما تحتمله التوكنات.")
        if not 1 <= self.leading_occurrences <= self.tokens:
            raise LexicalArtifactError("وقوعاتُ المتصدّر خارجَ عدد التوكنات.")

    @property
    def leading_share(self) -> float:
        """نصيبُ أعلى نمطٍ من التوكنات."""

        return self.leading_occurrences / self.tokens

    @property
    def exposed_share(self) -> float:
        """نصيبُ التوكنات الذي ليس شاهدًا جديدًا: (التوكنات − الأنماط)/التوكنات."""

        return (self.tokens - self.types) / self.tokens


@cache
def dominance_of(source_id: str, projected: bool) -> DominanceReading:
    """هيمنةُ وديعةٍ مقيسةً من بايتاتها، مكتوبةً كانت الطبقةُ أم مُسقَطة."""

    if source_id not in THE_DEPOSITS_PROJECTED:
        raise LexicalArtifactError(f"لا هيمنةَ لوديعةٍ خارج النطاق: {source_id!r}.")
    written = words_of(deposited_text(source_id), WordBoundary.ANY_WHITESPACE)
    tokens = tuple(project_word(word) for word in written) if projected else written
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    leader = max(sorted(counts), key=lambda key: counts[key])
    return DominanceReading(
        source_identity=source_id,
        projected=projected,
        tokens=len(tokens),
        types=len(counts),
        leading_type=leader,
        leading_occurrences=counts[leader],
    )


# --- الدعاوى المُغلَقة ------------------------------------------------------


@dataclass(frozen=True)
class ClosedClaim:
    """دعوًى مستبعَدةٌ بموقفها ومداها وآليّةِ فسادها وسندِ ذلك كلِّه."""

    claim_key: str
    claim_text: str
    standing: ExclusionStanding
    extent: ClosureExtent
    mechanism: CorruptionMechanism
    ground: str

    def __post_init__(self) -> None:
        if not self.claim_key.strip() or not self.claim_text.strip():
            raise LexicalArtifactError("دعوًى بلا مفتاحٍ أو بلا نصٍّ لا تُغلَق.")
        if not self.ground.strip():
            raise LexicalArtifactError("إغلاقٌ بلا سندٍ مكتوبٍ لا يُصدَر.")
        if self.standing is not ExclusionStanding.CLOSED_AS_LEXICAL_ARTIFACT:
            raise LexicalArtifactError(
                "المُودَعُ ههنا مُغلَقٌ أثرًا معجميًّا؛ ولا يُسجَّل بموقفٍ أضعف."
            )

    @property
    def is_whole(self) -> bool:
        """أمُغلَقةٌ بتمامها أم بنصيبها المقيسِ وحدَه؟"""

        return self.extent is ClosureExtent.WHOLE_CLAIM


def closed_claim(claim_key: str) -> ClosedClaim:
    """دعوًى مُغلَقةٌ بمفتاحها، والمجهولُ رفضٌ لا فراغ."""

    for claim in THE_CLOSED_CLAIMS:
        if claim.claim_key == claim_key:
            return claim
    raise LexicalArtifactError(f"لا دعوى مُغلَقةً بهذا المفتاح: {claim_key!r}.")


THE_CLOSED_CLAIMS: Final[tuple[ClosedClaim, ...]] = (
    ClosedClaim(
        claim_key="sukun-overlap",
        claim_text=(
            "«سكون-تراكب» دليلًا صوتيًّا بالعدّ التوكنيّ الخام: أن يُقاس حضورُ "
            "تراكبِ السكون توكنًا توكنًا فيُقرأ انتظامًا صوتيًّا"
        ),
        standing=ExclusionStanding.CLOSED_AS_LEXICAL_ARTIFACT,
        extent=ClosureExtent.WHOLE_CLAIM,
        ground=(
            "دعوى حضورٍ تُعَدّ توكنًا توكنًا، فتُصبح كلمةٌ شديدةُ التكرار دليلًا "
            "مُضاعَفًا على نفسها؛ وشاهدُ الآلية أنّ العنقدةَ التوزيعيّة خلطت "
            "الحرفَ الحقيقيَّ بكلمة المحتوى فائقةِ التكرار"
        ),
        mechanism=CorruptionMechanism.TOKEN_REPETITION_INFLATION,
    ),
    ClosedClaim(
        claim_key="fatha-only",
        claim_text=(
            "«فتحة-فقط» دليلًا صوتيًّا بالعدّ التوكنيّ الخام على النصيب الذي "
            "تصنعه إعادةُ عدِّ التوكن الواحد"
        ),
        standing=ExclusionStanding.CLOSED_AS_LEXICAL_ARTIFACT,
        extent=ClosureExtent.MEASURED_SHARE_ONLY,
        ground=(
            "يشارك الآليّةَ نفسَها بقدر نصيبه المُعرَّض المقيس على الودائع، "
            "ولا يُستبعَد ما سواه استبعادًا غيرَ مقيس؛ فالباقي غيرُ مُغلَقٍ "
            "بهذه الآلية لا مقبولٌ بها"
        ),
        mechanism=CorruptionMechanism.TOKEN_REPETITION_INFLATION,
    ),
)


def refuse_to_freeze(claim_key: str) -> None:
    """ترفض إدخالَ أرقام دعوًى مُغلَقةٍ في تجميدٍ أو استشهادٍ صوتيّ."""

    claim = closed_claim(claim_key)
    raise LexicalArtifactError(
        f"دعوًى مُغلَقةٌ أثرًا معجميًّا لا تدخل تجميدًا: {claim.claim_key!r}؛ "
        f"وآليّتُها {claim.mechanism.value}."
    )


# --- حرّاسُ الاستيراد ------------------------------------------------------


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ في إغلاقٍ لا سلطةَ فيه."""

    forbidden = {"verdict", "licensed", "born", "frozen", "authority", "rank"}
    for holder in (ClosedClaim, DominanceReading, ProbeWitness):
        named = {field.name for field in fields(holder)}
        if named & forbidden:
            raise LexicalArtifactError(
                f"حقلُ سلطةٍ في {holder.__name__}: {sorted(named & forbidden)}."
            )


def _assert_the_two_standings_are_not_one() -> None:
    """حارسُ استيراد: «مُغلَق» و«دون العتبة» موقفان متمايزان بالتعداد."""

    if len(ExclusionStanding) != 3:  # pragma: no cover - التعدادُ يمنعه
        raise LexicalArtifactError("الموقفان اتّحدا، والتمييزُ بينهما هو المقصود.")
    values = {member.value for member in ExclusionStanding}
    if len(values) != len(ExclusionStanding):  # pragma: no cover - التعدادُ يمنعه
        raise LexicalArtifactError("موقفان بقيمةٍ واحدة؛ فلا يتمايزان في المخرَج.")


def _assert_every_closed_claim_is_closed_and_grounded() -> None:
    """حارسُ استيراد: كلُّ مُودَعٍ ههنا مُغلَقٌ بسندٍ وآليّةٍ مسمّاة."""

    if not THE_CLOSED_CLAIMS:
        raise LexicalArtifactError("سجلُّ الإغلاق فارغٌ، وهذه الوحدةُ سجلُّ إغلاق.")
    keys = [claim.claim_key for claim in THE_CLOSED_CLAIMS]
    if len(set(keys)) != len(keys):
        raise LexicalArtifactError("مفتاحُ دعوًى مُكرَّرٌ في سجلّ الإغلاق.")
    for claim in THE_CLOSED_CLAIMS:
        if claim.standing is not ExclusionStanding.CLOSED_AS_LEXICAL_ARTIFACT:
            raise LexicalArtifactError(f"مُودَعٌ غيرُ مُغلَقٍ: {claim.claim_key!r}.")


def _assert_a_closed_claim_cannot_be_frozen() -> None:
    """حارسُ استيراد: كلُّ مُغلَقٍ يُرفَض عند التجميد، ولا استثناءَ صامت."""

    for claim in THE_CLOSED_CLAIMS:
        try:
            refuse_to_freeze(claim.claim_key)
        except LexicalArtifactError:
            continue
        raise LexicalArtifactError(  # pragma: no cover - الرفضُ فوقُ يمنعه
            f"دعوًى مُغلَقةٌ قبِلت التجميد: {claim.claim_key!r}."
        )


def _assert_the_witness_is_read_and_not_written_here() -> None:
    """حارسُ استيراد: شاهدُ الآلية مقروءٌ من التقرير المُودَع لا مكتوبٌ ههنا."""

    witness = the_probe_witness()
    if witness.surface_forms != RECORDED_PROBE_REPORT.specification.surface_form_count:
        raise LexicalArtifactError("شاهدٌ لا يطابق التقريرَ الذي قُرئ منه.")
    if witness.smallest_cluster >= max(witness.cluster_sizes):
        raise LexicalArtifactError("التقسيمُ متوازنٌ، والاختلاطُ مقروءٌ من صغره.")


def _assert_the_exposed_share_is_positive_where_a_type_repeats() -> None:
    """حارسُ استيراد: النصيبُ المُعرَّض مشتقٌّ، ويظهر حيث تكرّر نمطٌ فعلًا."""

    for source_id in THE_DEPOSITS_PROJECTED:
        for projected in (False, True):
            reading = dominance_of(source_id, projected)
            repeats = reading.tokens > reading.types
            if repeats != (reading.exposed_share > 0.0):
                raise LexicalArtifactError(
                    f"نصيبٌ مُعرَّضٌ لا يطابق تكرارَ الأنماط في {source_id!r}."
                )
            if reading.leading_share <= 0.0:
                raise LexicalArtifactError("متصدّرٌ بنصيبٍ غيرِ موجب.")


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in LEXICAL_ARTIFACT_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise LexicalArtifactError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_two_standings_are_not_one()
_assert_every_closed_claim_is_closed_and_grounded()
_assert_a_closed_claim_cannot_be_frozen()
_assert_the_witness_is_read_and_not_written_here()
_assert_the_exposed_share_is_positive_where_a_type_repeats()
_assert_every_residual_is_named_by_its_key()
