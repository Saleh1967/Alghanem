"""الليفُ مرشَّحٌ لمبدأ تنظيمٍ لا تقنيةَ ترميز — مُرشَّحًا، ولا ولادةَ بالقياس.

**الفرضيّةُ المُودَعة ههنا**، منصوصةً كما عُرضت:

> الليفُ قد يمثّل مبدأً لتنظيم الهويّة والتحوّل عبر مستويات الجبر، لا مجرّدَ
> تقنيةٍ لترميز الحركات. وهذا انتقالٌ من هندسة الترميز إلى **مرشَّحٍ** لجبر
> التحوّلات، من غير رفعِ القياس إلى شهادة ولادةٍ قبل اكتمال البرهان.

وهي تُودَع **مرشَّحةً** بالبناء: `HypothesisStanding.A_CANDIDATE` هو الحالُ
الوحيدُ الذي يقبله `OrganizingPrincipleCandidate`، ويُرفَع استثناءٌ عند أيّ
محاولةٍ لوسمها مولودةً أو مبرهَنة. والقياسُ لا يُرقّى شهادةً: كلُّ رقمٍ ههنا
يُقرَن بما لا يُثبِته (`A_MEASUREMENT_IS_NOT_A_BIRTH_CERTIFICATE`).

**وشاهدُ الألف يُقاس حيًّا، ويُقرأ بحدّه.** قراءاتُ الدعوى أربعٌ: اثنتان
منعقدتان قياسًا، وواحدةٌ محتمَلةٌ **قرارَ نمذجةٍ** لا قياسًا، وواحدةٌ
**منتقضة**. فالشاهدُ ليس كتلةً واحدة، ومن استشهد به جملةً استشهد بمنتقضٍ في
ضمنه (`THE_ALIF_WITNESS_IS_FOUR_READINGS_NOT_ONE`).

**وعليه مانعٌ قائمٌ لا يرفعه عددٌ من هذا الإيداع**: محورُ المدّ مُجمَّدٌ
مؤجَّلًا، والألفُ أَولى الحوامل بحملِه؛ فقد يكون حيادُها أثرَ تأجيلِ المحورِ
الذي عليه وحدَها تتغيّر. والشاهدُ يحمل مانعَه معه أو لا يُحمَل
(`THE_WITNESS_CARRIES_ITS_OWN_BLOCKER`).

**والعمومُ يُفحَص ولا يُفترَض.** خاصّيّةُ الألف — أن يكون ليفُها **المحايدَ
وحدَه** — تصدق على **١ من ٢٣**. أمّا المحايدُ نفسُه فيشارك في ليف **٤ من ٢٣**
حاملًا: `ا` و`ل` و`و` و`ي`. فالمقيسُ لا فردٌ ولا عموم؛ وأن تكون الأربعةُ هي
بعينها حروفَ العلّة مع لام التعريف **ملاحظةٌ تُسجَّل ولا تُفسَّر ههنا**
(`FOUR_CARRIERS_IS_NEITHER_ONE_NOR_GENERAL`).

**والمسائلُ الأربعُ متمايزةٌ حكمًا ولا تُطوى في واحدة**: العموم، وضرورةُ
`RefineSlot`، وولادةُ CV، والإفادةُ من الطرف إلى الطرف. لكلٍّ شرطُ إبراءٍ
مكتوب، وحالٌ مُسمّاة، وسببٌ لحالها — وإحداها **ممتنعةٌ بنيويًّا** لا مؤجَّلة:
حارسُ الاستيراد في `vv_birth_preregistration` يرفض التسجيلَ القبليَّ كلَّما
**وُجدت** وحدةُ القراءة، فلا تُكتَب وحدةُ قراءةِ CV ما دام الحارسُ قائمًا
(`ONE_OBLIGATION_IS_BARRED_NOT_MERELY_DEFERRED`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادة، ولا ترخيصَ `RefineSlot`، ولا
استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .alif_neutrality import AlifClaimReading, AlifVerdict, read_the_alif_claim
from .carrier_state_observed_fiber import ObservedFiberTable
from .fiber_rank_function import Fiber, observed_fibers

__all__ = [
    "A_MEASUREMENT_IS_NOT_A_BIRTH_CERTIFICATE_NOTE",
    "FOUR_CARRIERS_IS_NEITHER_ONE_NOR_GENERAL_NOTE",
    "ONE_OBLIGATION_IS_BARRED_NOT_MERELY_DEFERRED_NOTE",
    "ORGANIZING_PRINCIPLE_NAMED_RESIDUALS",
    "THE_ALIF_WITNESS_IS_FOUR_READINGS_NOT_ONE_NOTE",
    "THE_CANDIDATE",
    "THE_CANDIDATE_RECORD",
    "THE_HYPOTHESIS",
    "THE_OBLIGATIONS",
    "THE_WITNESS_CARRIES_ITS_OWN_BLOCKER_NOTE",
    "DischargeStanding",
    "HypothesisStanding",
    "IdentityParticipation",
    "ObligationRecord",
    "OrganizingPrincipleCandidate",
    "OrganizingPrincipleError",
    "ProofObligation",
    "measure_identity_participation",
    "read_the_alif_witness",
]


class OrganizingPrincipleError(ValueError):
    """رفضٌ صريح: فرضيّةٌ تُرفَع فوق الترشيح، أو التزامٌ بلا شرط إبراء."""


THE_HYPOTHESIS: Final[str] = (
    "الليفُ قد يمثّل مبدأً لتنظيم الهويّة والتحوّل عبر مستويات الجبر، لا مجرّدَ "
    "تقنيةٍ لترميز الحركات"
)

THE_CANDIDATE: Final[str] = (
    "انتقالٌ من هندسة الترميز إلى مرشَّحٍ لجبر التحوّلات، من غير رفعِ القياس "
    "إلى شهادة ولادةٍ قبل اكتمال البرهان"
)


class HypothesisStanding(Enum):
    """حالُ الفرضيّة؛ وهي مفردةٌ ذاتُ عضوٍ واحدٍ عمدًا، فلا ترقيةَ بالإغفال."""

    A_CANDIDATE = "مرشَّحةٌ_لا_مبرهَنةٌ_ولا_مولودة"


class ProofObligation(Enum):
    """المسائلُ البرهانيّةُ المتمايزة؛ أربعٌ لا تُطوى في واحدة."""

    GENERALITY_BEYOND_ONE_CARRIER = "العمومُ_وراءَ_حاملٍ_واحد"
    REFINE_SLOT_NECESSITY = "ضرورةُ_RefineSlot"
    CV_BIRTH = "ولادةُ_CV"
    END_TO_END_UTILITY = "الإفادةُ_من_الطرف_إلى_الطرف"


class DischargeStanding(Enum):
    """حالُ الالتزام؛ والممتنعُ غيرُ المؤجَّل، والمنتقضُ غيرُ غيرِ المُبرَأ."""

    NOT_ATTEMPTED = "لم_يُطرَق_بعد"
    ATTEMPTED_AND_UNDISCHARGED = "طُرِق_ولم_يُبرَأ"
    REFUTED_AS_STATED = "منتقضٌ_بصيغته_المعروضة"
    BARRED_BY_A_STANDING_GUARD = "ممتنعٌ_بحارسٍ_قائم"


@dataclass(frozen=True, slots=True)
class ObligationRecord:
    """التزامٌ واحد: حالُه، وشرطُ إبرائه، وسببُ حاله — ولا يُكتَب أحدُها فارغًا."""

    obligation: ProofObligation
    standing: DischargeStanding
    what_would_discharge_it: str
    why_it_stands_there: str

    def __post_init__(self) -> None:
        if not self.what_would_discharge_it.strip():
            raise OrganizingPrincipleError(
                "التزامٌ بلا شرطِ إبراءٍ مكتوبٍ يبقى مفتوحًا بلا بابٍ يُغلَق به"
            )
        if not self.why_it_stands_there.strip():
            raise OrganizingPrincipleError("حالٌ بلا سببٍ مكتوبٍ تُقرَأ حكمًا بعد حين")

    @property
    def is_discharged(self) -> bool:
        """أأُبرئ هذا الالتزام؟ لا — ولا حالَ في المفردة تعني الإبراء."""

        return False


THE_OBLIGATIONS: Final[tuple[ObligationRecord, ...]] = (
    ObligationRecord(
        obligation=ProofObligation.GENERALITY_BEYOND_ONE_CARRIER,
        standing=DischargeStanding.ATTEMPTED_AND_UNDISCHARGED,
        what_would_discharge_it=(
            "قانونٌ يُنبِئ بليف حاملٍ لم يُرصَد بعد، ويُكذَّب برصدٍ مخالف؛ لا "
            "نسبةُ نجاحٍ على الإيداع نفسه"
        ),
        why_it_stands_there=(
            "خاصّيّةُ الألف تصدق على واحدٍ من ثلاثةٍ وعشرين، والمحايدُ يشارك في "
            "أربعةٍ منها؛ فالمقيسُ لا فردٌ ولا عمومٌ ولا قانون"
        ),
    ),
    ObligationRecord(
        obligation=ProofObligation.REFINE_SLOT_NECESSITY,
        standing=DischargeStanding.REFUTED_AS_STATED,
        what_would_discharge_it=(
            "انقسامٌ داخليٌّ مرصودٌ في خانةٍ واحدة لا تردُّه دالّةُ حجمٍ على "
            "الليف، أو دالّةٌ مستقلّةٌ يتعذّر التعبيرُ عنها بغير عمليّة تقسيم"
        ),
        why_it_stands_there=(
            "لا انقسامَ داخليًّا مرصودٌ، بل تدرّجٌ في حجم الليف؛ والرتبةُ "
            "المقترحةُ بديلًا لا وجودَ لها على القاعدة، فسقطت العمليّتان معًا"
        ),
    ),
    ObligationRecord(
        obligation=ProofObligation.CV_BIRTH,
        standing=DischargeStanding.BARRED_BY_A_STANDING_GUARD,
        what_would_discharge_it=(
            "قراءةٌ مختومةٌ بعد تسجيلٍ قبليٍّ مُجمَّد، يسبق فيها التجميدُ "
            "الدليلَ بترتيبٍ تاريخيٍّ يُتحقَّق منه"
        ),
        why_it_stands_there=(
            "حارسُ الاستيراد في `vv_birth_preregistration` يرفض التسجيلَ "
            "القبليَّ كلَّما وُجدت وحدةُ القراءة أصلًا، فلا تُكتَب القراءةُ ما "
            "دام الحارسُ قائمًا؛ وهذا امتناعٌ بنيويٌّ لا تأجيل"
        ),
    ),
    ObligationRecord(
        obligation=ProofObligation.END_TO_END_UTILITY,
        standing=DischargeStanding.NOT_ATTEMPTED,
        what_would_discharge_it=(
            "هدفٌ مستقلٌّ عن المِرماز يُقاس عليه، لا سطحٌ يُعاد بناؤه بقراءة "
            "المِرماز الذي بُني به"
        ),
        why_it_stands_there=(
            "مبرهنةُ التفكيك وإعادة البناء تقرأ المِرمازَ الذي تُعيد البناءَ "
            "خلاله، فغلقُها على السطح دائريُّ الهدف ولم يُفتَح له هدفٌ ثانٍ"
        ),
    ),
)
"""أربعةُ التزاماتٍ متمايزةِ الحال؛ ولا واحدَ منها مُبرَأ."""


@dataclass(frozen=True, slots=True)
class OrganizingPrincipleCandidate:
    """الفرضيّةُ مُودَعةً مرشَّحةً؛ والترقيةُ فوق الترشيح مرفوضةٌ بالبناء."""

    hypothesis: str
    standing: HypothesisStanding
    obligations: tuple[ObligationRecord, ...]

    def __post_init__(self) -> None:
        if not self.hypothesis.strip():
            raise OrganizingPrincipleError("فرضيّةٌ بلا نصٍّ لا تُودَع")
        if self.standing is not HypothesisStanding.A_CANDIDATE:
            raise OrganizingPrincipleError(
                "الترشيحُ هو الحالُ الوحيدة؛ ولا تُرفَع فرضيّةٌ إلى ولادةٍ ههنا"
            )
        if len(self.obligations) != len(ProofObligation):
            raise OrganizingPrincipleError(
                "الالتزاماتُ تُذكَر كلُّها أو لا تُذكَر؛ وإسقاطُ واحدٍ إبراءٌ صامت"
            )
        if len({item.obligation for item in self.obligations}) != len(self.obligations):
            raise OrganizingPrincipleError("التزامٌ تكرّر؛ والتكرارُ يُخفي نقصًا")

    @property
    def is_born(self) -> bool:
        """أوُلدت؟ لا — والجوابُ ثابتٌ بالبناء لا بالحال الراهنة."""

        return False

    @property
    def undischarged_obligations(self) -> tuple[ProofObligation, ...]:
        """ما بقي مفتوحًا؛ وهو الأربعةُ كلُّها، مُشتقًّا بالعدّ لا مكتوبًا."""

        return tuple(
            item.obligation for item in self.obligations if not item.is_discharged
        )


THE_CANDIDATE_RECORD: Final[OrganizingPrincipleCandidate] = (
    OrganizingPrincipleCandidate(
        hypothesis=THE_HYPOTHESIS,
        standing=HypothesisStanding.A_CANDIDATE,
        obligations=THE_OBLIGATIONS,
    )
)
"""الإيداعُ نفسُه، مُنشَأً عند الاستيراد فيُفحَص شرطُه كلَّ مرّة."""


# --- شاهدُ الألف: أربعُ قراءاتٍ لا قراءة -------------------------------------


def read_the_alif_witness() -> tuple[tuple[AlifClaimReading, AlifVerdict], ...]:
    """اقرأ الشاهدَ حيًّا قراءةً قراءة؛ ولا يُنقَل حكمُه جملةً واحدة."""

    return tuple((item.reading, item.verdict) for item in read_the_alif_claim())


# --- العموم: مشاركةُ المحايد عبر الحوامل --------------------------------------


@dataclass(frozen=True, slots=True)
class IdentityParticipation:
    """مَن يشارك في المحايد، ومَن ليفُه المحايدُ وحدَه — وهما عددان لا عدد."""

    identity_state: tuple[tuple[str, str], ...]
    carrier_count: int
    carriers_containing_identity: tuple[str, ...]
    carriers_whose_fiber_is_only_identity: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.identity_state:
            raise OrganizingPrincipleError("محايدٌ بلا محاورَ مُسمّاةٍ لا يُقاس عليه")
        if len(self.carriers_containing_identity) > self.carrier_count:
            raise OrganizingPrincipleError("المشاركون أكثرُ من الحوامل كلِّها")
        if not set(self.carriers_whose_fiber_is_only_identity) <= set(
            self.carriers_containing_identity
        ):
            raise OrganizingPrincipleError(
                "حاملٌ ليفُه المحايدُ وحدَه وليس في المشاركين؛ عدٌّ متناقض"
            )

    @property
    def the_alif_property_is_unique(self) -> bool:
        """أخاصّيّةُ الألف مفردةٌ في الإيداع؟ يُعَدّ ولا يُدَّعى."""

        return len(self.carriers_whose_fiber_is_only_identity) == 1

    @property
    def participation_is_neither_singular_nor_general(self) -> bool:
        """أالمشاركةُ بين الفرد والعموم؟ أي أكثرُ من واحدٍ وأقلُّ من الكلّ."""

        return 1 < len(self.carriers_containing_identity) < self.carrier_count


def _identity_of(fibers: dict[str, Fiber]) -> tuple[tuple[str, str], ...]:
    candidates = {
        state
        for fiber in fibers.values()
        for state in fiber
        if all(value == "ABSENT" for _, value in state)
    }
    if len(candidates) != 1:
        raise OrganizingPrincipleError(
            "المحايدُ ليس واحدًا في هذا الإيداع؛ ولا يُختار أحدُهما بالذوق"
        )
    return next(iter(candidates))


def measure_identity_participation(
    table: ObservedFiberTable | None = None,
) -> IdentityParticipation:
    """قِس مشاركةَ المحايد عبر الحوامل؛ فالعمومُ يُفحَص ولا يُفترَض من حاملٍ واحد."""

    fibers = dict(observed_fibers(table))
    identity = _identity_of(fibers)
    return IdentityParticipation(
        identity_state=identity,
        carrier_count=len(fibers),
        carriers_containing_identity=tuple(
            sorted(carrier for carrier, fiber in fibers.items() if identity in fiber)
        ),
        carriers_whose_fiber_is_only_identity=tuple(
            sorted(carrier for carrier, fiber in fibers.items() if fiber == {identity})
        ),
    )


# --- البواقي المُسمّاة --------------------------------------------------------


A_MEASUREMENT_IS_NOT_A_BIRTH_CERTIFICATE_NOTE: Final[str] = (
    "AMeasurementIsNotABirthCertificate: الأرقامُ المُودَعةُ تصف ما وقع في "
    "إيداعٍ مُبصَّم، ولا تُرقَّى شهادةَ ولادةٍ بتراكمها؛ فالولادةُ حكمُ بوّابةٍ "
    "لها شرطُها، وبلوغُ نسبةٍ عاليةٍ ليس بلوغَ الشرط"
)

FOUR_CARRIERS_IS_NEITHER_ONE_NOR_GENERAL_NOTE: Final[str] = (
    "FourCarriersIsNeitherOneNorGeneral: المحايدُ يشارك في ليف أربعةٍ من ثلاثةٍ "
    "وعشرين، وخاصّيّةُ الألف مفردةٌ في واحد؛ فلا الشاهدُ فردٌ يُهمَل ولا عمومٌ "
    "يُعمَّم، وكونُ الأربعة حروفَ علّةٍ ولامَ تعريفٍ ملاحظةٌ لم تُفسَّر ههنا"
)

ONE_OBLIGATION_IS_BARRED_NOT_MERELY_DEFERRED_NOTE: Final[str] = (
    "OneObligationIsBarredNotMerelyDeferred: ولادةُ CV ليست مؤجَّلةً بل "
    "ممتنعةٌ ما دام حارسُ الاستيراد يرفض التسجيلَ القبليَّ لمجرّد وجود وحدة "
    "القراءة؛ فالطريقُ مسدودٌ ببناءٍ في الشجرة لا بنقصٍ في الدليل"
)

THE_ALIF_WITNESS_IS_FOUR_READINGS_NOT_ONE_NOTE: Final[str] = (
    "TheAlifWitnessIsFourReadingsNotOne: قراءتان منعقدتان قياسًا، وثالثةٌ "
    "محتمَلةٌ قرارَ نمذجةٍ لا قياسًا، ورابعةٌ منتقضة؛ فمن استشهد بالألف جملةً "
    "أدخل منتقضًا في شهادته، والاستشهادُ يكون بقراءةٍ مُسمّاة"
)

THE_WITNESS_CARRIES_ITS_OWN_BLOCKER_NOTE: Final[str] = (
    "TheWitnessCarriesItsOwnBlocker: محورُ المدّ مُجمَّدٌ مؤجَّلًا، والألفُ "
    "أَولى الحوامل بحملِه؛ فقد يكون حيادُها أثرَ تأجيلِ المحورِ الذي عليه "
    "وحدَها تتغيّر، ولا يرفع هذا المانعَ عددٌ من هذا الإيداع"
)

ORGANIZING_PRINCIPLE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_MEASUREMENT_IS_NOT_A_BIRTH_CERTIFICATE_NOTE,
    THE_ALIF_WITNESS_IS_FOUR_READINGS_NOT_ONE_NOTE,
    THE_WITNESS_CARRIES_ITS_OWN_BLOCKER_NOTE,
    FOUR_CARRIERS_IS_NEITHER_ONE_NOR_GENERAL_NOTE,
    ONE_OBLIGATION_IS_BARRED_NOT_MERELY_DEFERRED_NOTE,
)
"""خمسُ بقايا مُسمّاةٍ تُقابَل بها أيُّ إحالةٍ إلى «المبدأ» أو «الشاهد»."""
