"""`G0.FIBER-0.CONTRACT`: عقدُ المجال المحايد، بجوابٍ ملتزَمٍ به لا مشحون.

العقدُ يُجمَّد **قبل أن يوجد قارئٌ أصلًا**، لا قبل أن يُقرَأ فحسب. فهو يصف
المجالَ والامتحان، ولا يحمل هويّةَ نظامٍ ولا اسمَه ولا ينتظر خصمًا:

    FrozenContractBeforeReaders

وهو يحمل:

* مجالًا مُعلَنًا: أعضاءً بمدخلاتٍ مرصودةٍ فقط، لا أحكامَ فيها.
* شروطَ نجاحٍ بتغطيةٍ تامّةٍ لمعاييرها المغلقة.
* التزامَ جوابٍ: بصمةً رابطةً بعشوائيّةٍ خارجيّةٍ وبجسم العقد، لا الجوابَ.
* إحالةَ رتبةٍ وسياسةَ بقايا مأخوذتين من العقدة لا مُخترَعتين هنا.

والبصماتُ تُشتَقُّ بلا دائرة:

    contract_body_digest  =  H(جسمُ العقد بلا التزام)
    commitment            =  H(gold ‖ nonce ‖ contract_body_digest ‖ scheme)
    contract_digest       =  H(جسمُ العقد ‖ الالتزام)

وربطُ القرّاء — ومعه شرطُ ألّا يكون مؤلِّفُ العقد أحدَهم — يقع في طبقة التقييم
بعد هذا العقد، لا فيه.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..canonical_content import canonical_bytes, canonical_digest
from .commitment import GoldCommitment
from .laws import (
    A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED,
    FROZEN_CONTRACT_BEFORE_READERS,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
    PriorFiberError,
)
from .node import PriorFiberNode

__all__ = [
    "DomainMember",
    "FiberContract",
    "FiberContractBody",
    "SuccessCriterion",
]


class SuccessCriterion(Enum):
    """معاييرُ النجاح المغلقة؛ يُغطّيها العقدُ تغطيةً تامّةً لا أحسنَ جهد."""

    COVERAGE = "coverage"
    IDENTITY_PRESERVATION = "identity_preservation"
    BRANCH_BOUNDARY = "branch_boundary"
    RESIDUAL_DISCLOSURE = "residual_disclosure"
    NO_JUMP = "no_jump"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PriorFiberError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class DomainMember:
    """عضوٌ واحدٌ في المجال: مدخلاتُه المرصودة فقط، بلا حكمٍ مصحوب."""

    member_id: str
    observed_inputs: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        _require_text(self.member_id, "مُعرِّفُ عضو المجال")
        if not isinstance(self.observed_inputs, tuple) or not self.observed_inputs:
            raise PriorFiberError("عضوٌ بلا مدخلٍ مرصودٍ لا يُقرَأ")
        keys = []
        for entry in self.observed_inputs:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise PriorFiberError("المدخلُ المرصود زوجٌ: فرقٌ وقيمتُه")
            _require_text(entry[0], "مُعرِّفُ الفرق في المدخل")
            _require_text(entry[1], "قيمةُ الفرق في المدخل")
            keys.append(entry[0])
        if len(set(keys)) != len(keys):
            raise PriorFiberError("فرقٌ مُكرَّرٌ في مدخلات العضو؛ والمكرّرُ يُرفَض")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العضو للبصمة."""

        return {
            "member_id": self.member_id,
            "observed_inputs": [list(entry) for entry in self.observed_inputs],
        }


@dataclass(frozen=True, slots=True)
class FiberContractBody:
    """جسمُ العقد: كلُّ ما يُجمَّد قبل الالتزام وقبل وجود قارئ."""

    contract_id: str
    node: PriorFiberNode
    members: tuple[DomainMember, ...]
    success_criteria: tuple[SuccessCriterion, ...]
    authored_by: str

    def __post_init__(self) -> None:
        _require_text(self.contract_id, "مُعرِّفُ العقد")
        if not isinstance(self.node, PriorFiberNode):
            raise PriorFiberError("عقدُ المجال يقوم على عقدةٍ ليفيّةٍ من نوعها")
        if not isinstance(self.members, tuple) or not self.members:
            raise PriorFiberError("مجالٌ بلا عضوٍ لا يُستقرَأ")
        member_ids = []
        for member in self.members:
            if not isinstance(member, DomainMember):
                raise PriorFiberError("عضوٌ في المجال خارج نوعه")
            member_ids.append(member.member_id)
            self._refuse_an_unlicensed_input(member)
        if len(set(member_ids)) != len(member_ids):
            raise PriorFiberError("مُعرِّفُ العضو لا يتكرّر؛ والمكرّرُ يُرفَض لا يُطوى")
        self._refuse_incomplete_criteria()
        _require_text(self.authored_by, "مؤلِّفُ العقد")
        self._refuse_a_declared_reader()

    def _refuse_an_unlicensed_input(self, member: DomainMember) -> None:
        for distinction_id, value in member.observed_inputs:
            distinction = self.node.distinction(distinction_id)
            if value not in distinction.options:
                raise PriorFiberError(
                    f"قيمةُ `{value}` خارج قيم الفرق `{distinction_id}`؛ "
                    "والمجالُ لا يتّسع بالسهو"
                )

    def _refuse_a_declared_reader(self) -> None:
        if "reading_systems" in tuple(FiberContractBody.__dataclass_fields__):
            raise PriorFiberError(FROZEN_CONTRACT_BEFORE_READERS)

    def _refuse_incomplete_criteria(self) -> None:
        if not isinstance(self.success_criteria, tuple):
            raise PriorFiberError("معاييرُ النجاح صفٌّ مُجمَّد")
        for criterion in self.success_criteria:
            if not isinstance(criterion, SuccessCriterion):
                raise PriorFiberError("معيارٌ خارج مفردته المغلقة")
        if len(set(self.success_criteria)) != len(self.success_criteria):
            raise PriorFiberError("معيارٌ مُكرَّر؛ والمكرّرُ يُرفَض لا يُطوى")
        missing = tuple(
            criterion.value
            for criterion in SuccessCriterion
            if criterion not in set(self.success_criteria)
        )
        if missing:
            raise PriorFiberError(
                "شروطُ النجاح تُغطّى تغطيةً تامّةً؛ والمعاييرُ الغائبة: " + "، ".join(missing)
            )

    @property
    def member_ids(self) -> tuple[str, ...]:
        """مُعرِّفاتُ أعضاء المجال مرتَّبةً."""

        return tuple(sorted(member.member_id for member in self.members))

    @property
    def freezing_law(self) -> str:
        """قانونُ التجميد قبل القرّاء."""

        return FROZEN_CONTRACT_BEFORE_READERS

    @property
    def residual_policy(self) -> str:
        """سياسةُ البقايا؛ تُقرَأ من العقدة ولا تُكتَب هنا ثانيةً."""

        return self.node.residual_policy

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الجسم للبصمة؛ ولا التزامَ فيه، فلا دائرةَ في الاشتقاق."""

        return {
            "contract_id": self.contract_id,
            "node": self.node.as_canonical_content(),
            "members": [
                member.as_canonical_content()
                for member in sorted(self.members, key=lambda item: item.member_id)
            ],
            "success_criteria": [
                criterion.value
                for criterion in sorted(
                    self.success_criteria, key=lambda item: item.value
                )
            ],
            "authored_by": self.authored_by,
        }

    @property
    def body_digest(self) -> str:
        """بصمةُ جسم العقد؛ يُلتزَم بالجواب عليها قبل أن يحملها العقدُ التامّ."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    @property
    def domain_digest(self) -> str:
        """بصمةُ المجال: أعضاؤه بمدخلاتها المرصودة وحدها، لا جوابَ فيها."""

        return canonical_digest(
            canonical_bytes(
                [
                    member.as_canonical_content()
                    for member in sorted(self.members, key=lambda item: item.member_id)
                ]
            )
        )

    def withholds(self, label: str) -> bool:
        """أمحجوبٌ هذا الجوابُ عن محتوى الجسم؟ يُسأَل به من يملك الجوابَ وحده."""

        _require_text(label, "الجوابُ المسؤولُ عنه")
        content = canonical_bytes(self.as_canonical_content()).decode("utf-8")
        return label not in content


@dataclass(frozen=True, slots=True)
class FiberContract:
    """عقدُ مجالٍ مُجمَّد: جسمٌ مُجمَّدٌ قبل القرّاء، والتزامٌ مربوطٌ به."""

    body: FiberContractBody
    gold_commitment: GoldCommitment

    def __post_init__(self) -> None:
        if not isinstance(self.body, FiberContractBody):
            raise PriorFiberError("جسمُ العقد من نوعه لا نصًّا حرًّا")
        if not isinstance(self.gold_commitment, GoldCommitment):
            raise PriorFiberError(A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED)
        if self.gold_commitment.contract_body_digest != self.body.body_digest:
            raise PriorFiberError(
                "الالتزامُ مربوطٌ بجسم عقدٍ آخر؛ فليس التزامًا بهذا الامتحان"
            )
        if self.gold_commitment.committed_member_count != len(self.body.members):
            raise PriorFiberError(
                "عددُ الأعضاء الملتزَم بها يطابق أعضاءَ المجال؛ وإلّا فالمجالُ "
                "غيرُ مُغطًّى بالالتزام"
            )

    @property
    def contract_id(self) -> str:
        """مُعرِّفُ العقد؛ يُقرَأ من جسمه ولا يُكتَب هنا ثانيةً."""

        return self.body.contract_id

    @property
    def node(self) -> PriorFiberNode:
        """عقدةُ العقد الليفيّة."""

        return self.body.node

    @property
    def members(self) -> tuple[DomainMember, ...]:
        """أعضاءُ المجال."""

        return self.body.members

    @property
    def success_criteria(self) -> tuple[SuccessCriterion, ...]:
        """معاييرُ النجاح المُغطّاة تغطيةً تامّة."""

        return self.body.success_criteria

    @property
    def authored_by(self) -> str:
        """مؤلِّفُ العقد؛ ويُمنَع لاحقًا أن يكون أحدَ قرّائه في طبقة الربط."""

        return self.body.authored_by

    @property
    def contract_body_digest(self) -> str:
        """بصمةُ الجسم التي التُزِم بالجواب عليها."""

        return self.body.body_digest

    @property
    def domain_digest(self) -> str:
        """بصمةُ المجال بمدخلاته المرصودة وحدها."""

        return self.body.domain_digest

    @property
    def carries_no_reader_identity(self) -> bool:
        """أيخلو العقدُ من هويّة قارئٍ؟ يُفحَص على الحقول لا بالدعوى."""

        declared = tuple(FiberContract.__dataclass_fields__) + tuple(
            FiberContractBody.__dataclass_fields__
        )
        return not any(
            name in declared
            for name in ("reading_systems", "readers", "system_identities")
        )

    @property
    def gold_is_committed_not_shipped(self) -> bool:
        """أيحمل الالتزامُ بصماتٍ وأعدادًا فحسب، بلا جوابٍ ولا عشوائيّة؟"""

        declared = tuple(GoldCommitment.__dataclass_fields__)
        return declared == (
            "commitment_digest",
            "commitment_scheme",
            "gold_scheme",
            "contract_body_digest",
            "committed_member_count",
            "nonce_length_bits",
        )

    def withholds(self, label: str) -> bool:
        """أمحجوبٌ هذا الجوابُ عن محتوى العقد كلِّه؟"""

        _require_text(label, "الجوابُ المسؤولُ عنه")
        content = canonical_bytes(self.as_canonical_content()).decode("utf-8")
        return label not in content

    @property
    def strength_claim_ceiling(self) -> str:
        """أقصى ما يجوز أن تُنتِجه قراءةٌ لاحقةٌ لهذا العقد."""

        return OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN

    @property
    def residual_policy(self) -> str:
        """سياسةُ البقايا؛ تُقرَأ من العقدة ولا تُكتَب هنا ثانيةً."""

        return self.body.residual_policy

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العقد للبصمة: جسمُه والتزامُه معًا."""

        return {
            "body": self.body.as_canonical_content(),
            "gold_commitment": self.gold_commitment.as_canonical_content(),
        }

    @property
    def contract_digest(self) -> str:
        """بصمةُ العقد التامّ؛ مُشتَقّةٌ من الجسم والالتزام بلا دائرة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
