"""`G0.FIBER-0.CONTRACT`: عقدُ المجال المحايد، بجوابٍ مختومٍ لا مشحون.

العقدُ يُجمَّد **قبل** أن يُقرَأ بأيّ نظام، ويحمل:

* مجالًا مُعلَنًا: أعضاءً بمدخلاتٍ مرصودةٍ فقط، لا أحكامَ فيها.
* شروطَ نجاحٍ بتغطيةٍ تامّةٍ لمعاييرها المغلقة.
* ختمَ جوابٍ: بصمةً وحدَها، لا الجوابَ ولا ما يُشتَقُّ منه.
* إحالةَ رتبةٍ وسياسةَ بقايا مأخوذتين من العقدة لا مُخترَعتين هنا.

ولا يجوز أن يكون مؤلِّفُ العقد أحدَ النظامين اللذين سيُقرَأ بهما: فمن عرّف
الامتحان فاز به، والمقارنةُ حينئذٍ صورةٌ لا حجّة.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from ..canonical_content import canonical_bytes, canonical_digest
from .laws import (
    A_SEALED_GOLD_IS_A_DIGEST_NOT_AN_ANSWER,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
    PriorFiberError,
)
from .node import PriorFiberNode

__all__ = [
    "DomainMember",
    "FiberContract",
    "GoldSeal",
    "SuccessCriterion",
    "seal_gold",
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
class GoldSeal:
    """ختمُ الجواب: بصمةٌ وعدد، ولا جوابَ في العقد ولا أثرَ منه."""

    gold_digest: str
    gold_scheme: str
    sealed_member_count: int

    def __post_init__(self) -> None:
        _require_text(self.gold_digest, "بصمةُ الجواب المختوم")
        _require_text(self.gold_scheme, "بيانُ صيغة الجواب")
        if (
            not isinstance(self.sealed_member_count, int)
            or self.sealed_member_count < 1
        ):
            raise PriorFiberError("عددُ الأعضاء المختومة عددٌ صحيحٌ موجب")

    @property
    def withholding_law(self) -> str:
        """قانونُ حجب الجواب عن العقد."""

        return A_SEALED_GOLD_IS_A_DIGEST_NOT_AN_ANSWER

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الختم للبصمة."""

        return {
            "gold_digest": self.gold_digest,
            "gold_scheme": self.gold_scheme,
            "sealed_member_count": self.sealed_member_count,
        }


def seal_gold(labels: Mapping[str, str], *, gold_scheme: str) -> GoldSeal:
    """اختم جوابًا: احسب بصمتَه ثمّ لا تحتفظ به؛ يُمرَّر ولا يُخزَّن."""

    if not isinstance(labels, Mapping) or not labels:
        raise PriorFiberError("الجوابُ المختوم مطابقةٌ غيرُ فارغة")
    for member_id, label in labels.items():
        _require_text(member_id, "مُعرِّفُ العضو في الجواب")
        _require_text(label, f"جوابُ `{member_id}`")
    payload = {
        "gold_scheme": _require_text(gold_scheme, "بيانُ صيغة الجواب"),
        "labels": [[key, labels[key]] for key in sorted(labels)],
    }
    return GoldSeal(
        gold_digest=canonical_digest(canonical_bytes(payload)),
        gold_scheme=gold_scheme,
        sealed_member_count=len(labels),
    )


@dataclass(frozen=True, slots=True)
class FiberContract:
    """عقدُ مجالٍ محايد: مُجمَّدٌ قبل القراءة، ومحايدٌ عن كلِّ نظامٍ سيقرؤه."""

    contract_id: str
    node: PriorFiberNode
    members: tuple[DomainMember, ...]
    success_criteria: tuple[SuccessCriterion, ...]
    gold_seal: GoldSeal
    authored_by: str
    reading_systems: tuple[str, ...]

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
        if not isinstance(self.gold_seal, GoldSeal):
            raise PriorFiberError(A_SEALED_GOLD_IS_A_DIGEST_NOT_AN_ANSWER)
        if self.gold_seal.sealed_member_count != len(self.members):
            raise PriorFiberError(
                "عددُ الأعضاء المختومة يطابق أعضاءَ المجال؛ وإلّا فالمجالُ غيرُ "
                "مُغطًّى بالختم"
            )
        _require_text(self.authored_by, "مؤلِّفُ العقد")
        if not isinstance(self.reading_systems, tuple) or len(self.reading_systems) < 2:
            raise PriorFiberError("العقدُ يُقرَأ بنظامين فأكثر؛ ونظامٌ واحدٌ لا يُقارَن")
        for system in self.reading_systems:
            _require_text(system, "اسمُ النظام القارئ")
        if len(set(self.reading_systems)) != len(self.reading_systems):
            raise PriorFiberError("نظامٌ قارئٌ مُكرَّر؛ والمكرّرُ يُرفَض لا يُطوى")
        if self.authored_by in self.reading_systems:
            raise PriorFiberError(NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY)

    def _refuse_an_unlicensed_input(self, member: DomainMember) -> None:
        for distinction_id, value in member.observed_inputs:
            distinction = self.node.distinction(distinction_id)
            if value not in distinction.options:
                raise PriorFiberError(
                    f"قيمةُ `{value}` خارج قيم الفرق `{distinction_id}`؛ "
                    "والمجالُ لا يتّسع بالسهو"
                )

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
    def is_neutral_between_its_readers(self) -> bool:
        """أمحايدٌ العقدُ عن كلِّ نظامٍ سيقرؤه؟"""

        return self.authored_by not in self.reading_systems

    @property
    def gold_is_sealed_by_digest_only(self) -> bool:
        """أيحمل الختمُ بصمةً وعددًا فحسب؟ يُفحَص على الحقول لا بالدعوى."""

        declared = tuple(GoldSeal.__dataclass_fields__)
        return declared == ("gold_digest", "gold_scheme", "sealed_member_count")

    def withholds(self, label: str) -> bool:
        """أمحجوبٌ هذا الجوابُ عن محتوى العقد؟ يُسأَل به من يملك الجوابَ وحده."""

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

        return self.node.residual_policy

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العقد للبصمة."""

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
            "gold_seal": self.gold_seal.as_canonical_content(),
            "authored_by": self.authored_by,
            "reading_systems": list(self.reading_systems),
        }

    @property
    def preregistration_digest(self) -> str:
        """بصمةُ التسجيل المسبق؛ مُشتَقّةٌ لا مكتوبة، وتُجمَّد قبل أيّ قراءة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
