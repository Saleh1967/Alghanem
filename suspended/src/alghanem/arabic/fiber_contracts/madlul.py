"""`G0.FIBER-0.ADAPTER.MADLUL`: تحويلُ مجال المدلول وحده إلى عقدٍ ليفيٍّ محايد.

الاتّجاهُ واحدٌ لا يُعكَس:

    ArabicDomainAdapter  →  PriorFiber

فالطبقةُ الليفيّة لا تستورد مادّةَ هذا المجال، ولا تُنسَخ إليها نصوصُه؛ إنّما
يقرأ هذا المُحوِّلُ `madlul_alone_formal` — وهو المصدرُ الوحيد للمادّة — ويبني
منه عقدةً ليفيّةً وعقدَ مجالٍ مُجمَّدًا.

والعقدُ يُجمَّد قبل أن يوجد قارئٌ أصلًا: لا يحمل هويّةَ نظامٍ ولا اسمَه، وربطُ
القرّاء يقع في طبقة التقييم بعده لا فيه.

وما يدخل العقدَ هو **المدخلُ المرصود وحده**: الحواملُ الثلاثة التي تُشتَقُّ منها
الإجابات. وأمّا القسمُ المنصوص فجوابٌ محجوب: يُختَم ببصمةٍ ولا يُشحَن في العقد،
فلا يقرؤه نظامٌ سيُمتحَن به. ولا تدخل ملاحظةُ خروج الفرع الخامس عن نطاق الوضع
أيضًا، لأنّها تُسمّي فرعَه فتكشفه.

ومُعرِّفُ العضو بصمةُ هويّة شاهده لا رقمُ ترتيبه، لأنّ ترتيبَ المصدر ترتيبُ
الأقسام نفسِها، فلو رُقّمت الأعضاءُ به لسُرِّب الجوابُ في المُعرِّف.

والجوابُ هنا مربوطٌ لا مخفيٌّ تشفيريًّا: مادّتُه مقروءةٌ من `madlul_alone_formal`
في هذا المستودع، فالتزامُه يمنع تبديلَه بعد رؤية المخرجات، وحجبُه عن القارئ
يقع بحدِّ المصدر المُصرَّح لا بسرّيّة المادّة. ولا يُسمّى هذا إخفاءً تامًّا.

سلطويًّا — تصريحٌ لا تفصيل لاحق: هذا عقدُ امتحانٍ مُجمَّد، لا حكمَ فيه ولا
ولادةَ ولا مقارنة. ولا يُبنى هنا نظامٌ قارئٌ ولا تُقاس قوّةُ نظامٍ على آخر.
"""

from __future__ import annotations

from typing import Final

from ...canonical_content import canonical_bytes, canonical_digest
from ...prior import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorLicenseGenus,
)
from ...prior_fiber import (
    AdmissibleDistinction,
    DomainMember,
    ExternalRankReference,
    FiberContract,
    FiberContractBody,
    GoldCommitment,
    ParallelFiberBundle,
    PriorFiberNode,
    SuccessCriterion,
    commit_gold,
    project_all_fibers,
)
from ..madlul_alone_formal import (
    ATTESTED_SIGNIFIED_WITNESSES,
    MADLUL_FIRST_QUESTION,
    MADLUL_SCOPE_NOTE,
    MADLUL_SECOND_QUESTION,
    MADLUL_SECOND_QUESTION_CONDITION,
    MADLUL_SOURCE,
    MADLUL_THIRD_QUESTION,
    MADLUL_THIRD_QUESTION_CONDITION,
    AttestedSignifiedWitness,
    MadlulAloneError,
    MadlulSection,
    SignifiedAssignmentCarrier,
    SignifiedNatureCarrier,
    SignifiedStructureCarrier,
)

__all__ = [
    "MADLUL_ASSIGNMENT_DISTINCTION_ID",
    "MADLUL_CONTRACT_AUTHOR",
    "MADLUL_CONTRACT_INTERFACE_VERSION",
    "MADLUL_GOLD_SCHEME",
    "MADLUL_NATURE_DISTINCTION_ID",
    "MADLUL_STRUCTURE_DISTINCTION_ID",
    "build_madlul_fiber_contract",
    "build_madlul_fiber_node",
    "commit_madlul_gold",
    "madlul_contract_body",
    "madlul_domain_members",
    "madlul_member_id",
    "madlul_parallel_fibers",
    "madlul_prior_base",
]

MADLUL_NATURE_DISTINCTION_ID: Final = "carrier.signified_nature"

MADLUL_STRUCTURE_DISTINCTION_ID: Final = "carrier.signified_structure"

MADLUL_ASSIGNMENT_DISTINCTION_ID: Final = "carrier.signified_assignment"

MADLUL_CONTRACT_AUTHOR: Final = "alghanem.arabic.fiber_contracts.madlul"

MADLUL_CONTRACT_INTERFACE_VERSION: Final = "g0_eval_0.contract_interface.1"
"""إصدارُ واجهة العقد؛ يُطابَق عليه بروتوكولُ التقييم وهويّاتُ قرّائه لاحقًا."""

MADLUL_GOLD_SCHEME: Final = (
    "قسمُ المدلول المنصوص في المصدر لكلِّ شاهد؛ محجوبٌ عن العقد، مختومٌ ببصمته"
)

_ALWAYS_ASKED: Final = "تُطرَح دائمًا"


_MADLUL_CONDITIONS: Final[tuple[PriorCondition, ...]] = (
    PriorCondition(
        condition_id="madlul.domain",
        kind=PriorConditionKind.DOMAIN,
        statement=(
            "المجالُ تصنيفُ مدلول لفظٍ واحدٍ بعينه في نطاق نصٍّ واحد: " + MADLUL_SOURCE
        ),
        what_it_forbids=(
            "يمنع إدخال لفظٍ لم يُثبَت مدلولُه في هذا المصدر، ويمنع توسيعَ النطاق "
            "إلى أقسام اللفظ المدلول نفسِه أو مراتب الإهمال"
        ),
        licensed_by=PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
    ),
    PriorCondition(
        condition_id="madlul.unit",
        kind=PriorConditionKind.UNIT_CRITERION,
        statement="الوحدةُ لفظٌ واحدٌ يُختبَر مدلولُه هو، لا عنقودُ علاقةٍ بين طرفين",
        what_it_forbids=(
            "يمنع قراءةَ نسبة اللفظ إلى معناه أو تعدّدِ الطرفين وحدةً في هذا المجال"
        ),
        licensed_by=PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
    ),
    PriorCondition(
        condition_id="madlul.identity",
        kind=PriorConditionKind.IDENTITY_CRITERION,
        statement=("هويّةُ الشاهد لفظُه مع مدلوله المُختبَر معًا، لا اللفظُ المجرَّد وحده"),
        what_it_forbids=(
            "يمنع عدَّ لفظين مختلفَي المدلول شاهدًا واحدًا، ويمنع طيَّ أحدهما في الآخر"
        ),
        licensed_by=PriorLicenseGenus.PRIOR_PROOF,
    ),
    PriorCondition(
        condition_id="madlul.attributes",
        kind=PriorConditionKind.ATTRIBUTE_POSSIBILITY,
        statement=(
            "الصفاتُ الممكنة ثلاثةُ حواملَ مغلقة: حاملُ جنس المدلول، وحاملُ تركيب "
            "اللفظ المدلول، وحاملُ حال الوضع"
        ),
        what_it_forbids=(
            "يمنع صفةً خارج الحوامل الثلاثة، ويمنع كتابةَ إجابةٍ لا يُشتَقُّها حاملُها"
        ),
        licensed_by=PriorLicenseGenus.PRIOR_PROOF,
    ),
    PriorCondition(
        condition_id="madlul.relations",
        kind=PriorConditionKind.RELATION_POSSIBILITY,
        statement=(
            "العلاقةُ الممكنة الوحيدة في هذا المستوى شرطيّةُ طرح السؤال: "
            + MADLUL_SECOND_QUESTION_CONDITION
            + "، و"
            + MADLUL_THIRD_QUESTION_CONDITION
        ),
        what_it_forbids=(
            "يمنع طرحَ س٢ أو س٣ على مدلولٍ ليس بلفظ، ويمنع قراءةَ `لا_ينطبق` قيمةً "
            "موضوعيّةً بدل تصريحٍ بعدم الطرح"
        ),
        licensed_by=PriorLicenseGenus.PRIOR_PROOF,
    ),
    PriorCondition(
        condition_id="madlul.transformation",
        kind=PriorConditionKind.TRANSFORMATION_CONDITIONS,
        statement=(
            "التحوّلُ المرخَّص اشتقاقُ إجابةٍ من حاملها وحده، ثمّ اشتقاقُ القسم من "
            "الإجابات الثلاث مجتمعةً"
        ),
        what_it_forbids=(
            "يمنع القفزَ من الحامل إلى القسم بلا إجاباتٍ وسيطة، ويمنع تعديلَ إجابةٍ "
            "لتوافق قسمًا مقصودًا"
        ),
        licensed_by=PriorLicenseGenus.PRIOR_PROOF,
    ),
    PriorCondition(
        condition_id="madlul.gates",
        kind=PriorConditionKind.CONDITIONS_AND_PREVENTERS,
        statement=(
            "المانعُ المُعلَن: شاهدٌ بلا نصٍّ مُثبَتٍ من المصدر لا يدخل المجال، "
            "وحالةٌ خارج الحالات المقبولة تُرفَض ولا تُحمَل على أقربها"
        ),
        what_it_forbids="يمنع الحملَ على الأقرب وإكمالَ النقص بالسهو",
        licensed_by=PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
    ),
    PriorCondition(
        condition_id="madlul.trace",
        kind=PriorConditionKind.PRESERVED_TRACE,
        statement=(
            "الأثرُ المحفوظ: نصُّ المصدر لكلِّ حامل، ونطاقُ البرهان مسجَّلًا: "
            + MADLUL_SCOPE_NOTE
        ),
        what_it_forbids="يمنع إحالةً مبهمةً إلى المصدر بلا نصٍّ مُثبَت",
        licensed_by=PriorLicenseGenus.PRIOR_PROOF,
    ),
    PriorCondition(
        condition_id="madlul.residual",
        kind=PriorConditionKind.CLOSURE_BLOCKING_REMAINDER,
        statement=(
            "البقيّةُ الحاجبة: كلُّ عضوٍ لم يُصنَّف، أو صُنِّف بلا اشتقاقٍ من حوامله، "
            "أو خرج عن المجال المُعلَن، يُسجَّل بقيّةً حاجبةً تمنع دعوى التمام"
        ),
        what_it_forbids="يمنع دعوى استقراءٍ تامٍّ مع عضوٍ متروكٍ أو غيرِ مُشتَقّ",
        licensed_by=PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
    ),
)


def madlul_prior_base() -> PriorInformationBase:
    """قاعدةُ المعلومات السابقة لهذا المجال: مواضعُ الإمكان التسعةُ مُرخَّصةً."""

    return PriorInformationBase(
        base_id="PK0.madlul_alone",
        domain_note=("تصنيفُ مدلول اللفظ وحده على نطاق نصٍّ واحدٍ مُثبَت: " + MADLUL_SOURCE),
        conditions=_MADLUL_CONDITIONS,
    )


def build_madlul_fiber_node() -> PriorFiberNode:
    """ابنِ عقدةَ المجال الليفيّة فوق قاعدة معلوماته السابقة."""

    return PriorFiberNode(
        origin_id="origin.madlul_alone",
        instance_id="instance.madlul_alone.g0_fiber_0",
        prior_base=madlul_prior_base(),
        slot_geometry=(
            MADLUL_NATURE_DISTINCTION_ID,
            MADLUL_STRUCTURE_DISTINCTION_ID,
            MADLUL_ASSIGNMENT_DISTINCTION_ID,
        ),
        admissible_distinctions=(
            AdmissibleDistinction(
                distinction_id=MADLUL_NATURE_DISTINCTION_ID,
                question=MADLUL_FIRST_QUESTION,
                options=tuple(member.value for member in SignifiedNatureCarrier),
                asked_when=_ALWAYS_ASKED,
            ),
            AdmissibleDistinction(
                distinction_id=MADLUL_STRUCTURE_DISTINCTION_ID,
                question=MADLUL_SECOND_QUESTION,
                options=tuple(member.value for member in SignifiedStructureCarrier),
                asked_when=MADLUL_SECOND_QUESTION_CONDITION,
            ),
            AdmissibleDistinction(
                distinction_id=MADLUL_ASSIGNMENT_DISTINCTION_ID,
                question=MADLUL_THIRD_QUESTION,
                options=tuple(member.value for member in SignifiedAssignmentCarrier),
                asked_when=MADLUL_THIRD_QUESTION_CONDITION,
            ),
        ),
        relations=(MADLUL_SECOND_QUESTION_CONDITION, MADLUL_THIRD_QUESTION_CONDITION),
        capabilities=(
            "اشتقاقُ إجابةٍ من حاملها",
            "اشتقاقُ قسمٍ من الإجابات الثلاث مجتمعةً",
            "تسجيلُ بقيّةٍ حاجبةٍ عند تعذّر الاشتقاق",
        ),
        evidence_requirements=(
            "نصٌّ مُثبَتٌ من المصدر لكلِّ حاملٍ مُدَّعًى",
            "اشتقاقُ كلِّ إجابةٍ من حاملها لا من القسم المقصود",
        ),
        gates=(
            "شاهدٌ بلا نصٍّ مُثبَتٍ لا يدخل المجال",
            "حالةٌ خارج المجال تُرفَض ولا تُحمَل على أقربها",
        ),
        rank_reference=ExternalRankReference(
            evidence_ref="alghanem.arabic.madlul_alone_formal:ATTESTED_SIGNIFIED_WITNESSES",
            rank_ceiling_ref="FormalClassification != BirthVerdict",
            issuing_authority="alghanem.kernel (سلطةُ الرتب خارج هذه الطبقة)",
        ),
        residual_policy=(
            "كلُّ عضوٍ غيرِ مُصنَّفٍ أو غيرِ مُشتَقٍّ من حوامله بقيّةٌ حاجبةٌ تمنع "
            "دعوى التمام، وتُسمَّى جميعًا ولا يُوقَف عند أوّلها"
        ),
        trace=(MADLUL_SOURCE, MADLUL_SCOPE_NOTE),
    )


def madlul_parallel_fibers() -> ParallelFiberBundle:
    """اشتقّ محاورَ المجال الثلاثة معًا من عقدته الواحدة."""

    return project_all_fibers(build_madlul_fiber_node())


def madlul_member_id(witness: AttestedSignifiedWitness) -> str:
    """مُعرِّفُ العضو بصمةُ هويّة شاهده، لا رقمُ ترتيبه في المصدر."""

    key = witness.witness_key
    return "member." + canonical_digest(canonical_bytes([key[0], key[1]]))[:16]


def madlul_domain_members() -> tuple[DomainMember, ...]:
    """أعضاءُ المجال بمدخلاتها المرصودة وحدها؛ لا قسمَ منصوصًا فيها."""

    return tuple(
        DomainMember(
            member_id=madlul_member_id(witness),
            observed_inputs=(
                (
                    MADLUL_NATURE_DISTINCTION_ID,
                    witness.signified_nature_carrier.value,
                ),
                (
                    MADLUL_STRUCTURE_DISTINCTION_ID,
                    witness.signified_structure_carrier.value,
                ),
                (
                    MADLUL_ASSIGNMENT_DISTINCTION_ID,
                    witness.signified_assignment_carrier.value,
                ),
            ),
        )
        for witness in ATTESTED_SIGNIFIED_WITNESSES
    )


def madlul_contract_body() -> FiberContractBody:
    """جمِّد جسمَ العقد؛ يُجمَّد قبل الالتزام وقبل أن يوجد قارئٌ أصلًا."""

    return FiberContractBody(
        contract_id="contract.madlul_alone.g0_fiber_0",
        node=build_madlul_fiber_node(),
        members=madlul_domain_members(),
        success_criteria=tuple(SuccessCriterion),
        authored_by=MADLUL_CONTRACT_AUTHOR,
    )


def _madlul_gold_labels() -> dict[str, str]:
    """الجوابُ المحجوب؛ يُقرَأ هنا ليُلتزَم به ولا يُخزَّن في عقدٍ ولا مخرَج."""

    return {
        madlul_member_id(witness): witness.attested_section.value
        for witness in ATTESTED_SIGNIFIED_WITNESSES
    }


def commit_madlul_gold(nonce: bytes) -> GoldCommitment:
    """التزِم بجواب هذا المجال بعشوائيّةٍ تُمرَّر من خارج المشروع.

    لا قيمةَ افتراضيّة للـ`nonce` ولا اشتقاقَ له: من ولّده فهو مسؤولٌ عن إبقائه
    خارج المستودع وخارج كلِّ مخرَج. ولا يعرف هذا المُحوِّلُ من أين جاء.
    """

    return commit_gold(
        _madlul_gold_labels(),
        gold_scheme=MADLUL_GOLD_SCHEME,
        nonce=nonce,
        contract_body_digest=madlul_contract_body().body_digest,
    )


def build_madlul_fiber_contract(gold_commitment: GoldCommitment) -> FiberContract:
    """ابنِ العقدَ التامّ: جسمٌ مُجمَّدٌ قبل القرّاء، والتزامٌ مربوطٌ به."""

    return FiberContract(body=madlul_contract_body(), gold_commitment=gold_commitment)


def _refuse_a_leaked_answer() -> None:
    """ارفض عند الاستيراد ظهورَ قسمٍ منصوصٍ في مدخلات الأعضاء أو جسم العقد."""

    sections = tuple(section.value for section in MadlulSection)
    for member in madlul_domain_members():
        content = canonical_bytes(member.as_canonical_content()).decode("utf-8")
        for section in sections:
            if section in content:
                raise MadlulAloneError(
                    "الجوابُ المحجوب ظهر في مدخلات عضوٍ من المجال: " + member.member_id
                )
    body = madlul_contract_body()
    for section in sections:
        if not body.withholds(section):
            raise MadlulAloneError("الجوابُ المحجوب ظهر في جسم العقد: " + section)
    identifiers = tuple(
        madlul_member_id(witness) for witness in ATTESTED_SIGNIFIED_WITNESSES
    )
    if len(set(identifiers)) != len(identifiers):
        raise MadlulAloneError("مُعرِّفُ العضو لا يتكرّر؛ وهويّةُ الشاهد تُميِّزه")


_refuse_a_leaked_answer()
