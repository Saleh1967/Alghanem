"""`G0.EVAL-0.BINDING`: ربطُ عقدٍ مُجمَّدٍ بقرّاءَ مُجمَّدين وببروتوكولٍ مُجمَّد.

العقدُ لا يحمل قارئًا ولا ينتظره: `FrozenContractBeforeReaders`. والربطُ يقع هنا
بعده، ويُنتِج لكلِّ قارئٍ طلبًا يربط أربعةً صراحةً:

    BoundEvaluationRequest
      =  system_content_id
       + contract_digest
       + domain_digest
       + evaluation_protocol_digest

وهنا — لا في العقد — يُمنَع أن يكون مؤلِّفُ العقد أحدَ قرّائه: فمن عرّف الامتحانَ
فاز به. ويُقاس ذلك على ملفّات المصدر لا على الأسماء، لأنّ الاسمَ يُنتحَل.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from ..import_boundary import displayed_path, module_files
from ..prior_fiber import FiberContract
from .boundary import BlindPayload, issue_blind_payload
from .identity import FrozenSystemIdentity
from .laws import (
    FROZEN_CONTRACT_BEFORE_READERS,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    EvaluationError,
)
from .protocol import FrozenEvaluationProtocol

__all__ = [
    "BoundEvaluationRequest",
    "EvaluationBinding",
]


def _require_digest(value: object, label: str) -> str:
    if not is_canonical_digest(value):
        raise EvaluationError(f"{label} بصمةٌ قانونيّةٌ لا نصٌّ حرّ")
    assert isinstance(value, str)
    return value


@dataclass(frozen=True, slots=True)
class BoundEvaluationRequest:
    """طلبُ تقييمٍ مربوط: قارئٌ، وعقدٌ، ومجالٌ، وبروتوكولٌ، ببصماتها الأربع."""

    system_content_id: str
    contract_digest: str
    domain_digest: str
    evaluation_protocol_digest: str

    def __post_init__(self) -> None:
        _require_digest(self.system_content_id, "بصمةُ هويّة القارئ")
        _require_digest(self.contract_digest, "بصمةُ العقد")
        _require_digest(self.domain_digest, "بصمةُ المجال")
        _require_digest(self.evaluation_protocol_digest, "بصمةُ البروتوكول")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الطلب للبصمة."""

        return {
            "system_content_id": self.system_content_id,
            "contract_digest": self.contract_digest,
            "domain_digest": self.domain_digest,
            "evaluation_protocol_digest": self.evaluation_protocol_digest,
        }

    @property
    def request_id(self) -> str:
        """بصمةُ الطلب؛ مُشتَقّةٌ من الأربعة، فلا يُفهرَس تقريرٌ بغير ما رُبِط به."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True, slots=True)
class EvaluationBinding:
    """ربطٌ مُجمَّد: عقدٌ، وبروتوكولٌ، وهويّاتُ قرّاءٍ متمايزةٌ لا أسماءُهم."""

    contract: FiberContract
    protocol: FrozenEvaluationProtocol
    reader_identities: tuple[FrozenSystemIdentity, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.contract, FiberContract):
            raise EvaluationError("الربطُ يقع على عقدٍ مُجمَّدٍ من نوعه")
        if not self.contract.carries_no_reader_identity:
            raise EvaluationError(FROZEN_CONTRACT_BEFORE_READERS)
        if not isinstance(self.protocol, FrozenEvaluationProtocol):
            raise EvaluationError("البروتوكولُ مُجمَّدٌ من نوعه لا وصفٌ حرّ")
        if (
            not isinstance(self.reader_identities, tuple)
            or len(self.reader_identities) < 2
        ):
            raise EvaluationError("الامتحانُ يُقرَأ بنظامين فأكثر؛ وواحدٌ لا يُقارَن")
        content_ids = []
        for identity in self.reader_identities:
            if not isinstance(identity, FrozenSystemIdentity):
                raise EvaluationError("هويّةُ القارئ مُجمَّدةٌ من نوعها لا اسمٌ نصّيّ")
            content_ids.append(identity.content_id)
        if len(set(content_ids)) != len(content_ids):
            raise EvaluationError("هويّةُ قارئٍ مُكرَّرة؛ والمكرّرُ يُرفَض لا يُطوى")
        self._refuse_a_reader_that_authored_the_contract()
        self._refuse_an_interface_mismatch()

    def _refuse_an_interface_mismatch(self) -> None:
        for identity in self.reader_identities:
            if (
                identity.contract_interface_version
                != self.protocol.contract_interface_version
            ):
                raise EvaluationError(
                    "قارئٌ على إصدارِ واجهةٍ غير إصدار البروتوكول؛ فالامتحانُ "
                    "المقروءُ غيرُ الامتحان المُجمَّد"
                )

    def _refuse_a_reader_that_authored_the_contract(self) -> None:
        author_files = {
            displayed_path(path) for path in module_files(self.contract.authored_by)
        }
        if not author_files:
            raise EvaluationError(
                "مؤلِّفُ العقد يُحَلُّ إلى مصدرٍ يُقاس عليه الحياد؛ والاسمُ وحده " "لا يُفحَص"
            )
        for identity in self.reader_identities:
            overlap = author_files & set(identity.implementation_files)
            if overlap:
                raise EvaluationError(
                    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY
                    + "؛ والمصدرُ المشترك: "
                    + "، ".join(sorted(overlap))
                )

    @property
    def payload(self) -> BlindPayload:
        """الحمولةُ المُسلسَلة التي يستلمها كلُّ قارئ، واحدةً لهم جميعًا."""

        return issue_blind_payload(
            self.contract, protocol_digest=self.protocol.protocol_digest
        )

    def request_for(self, identity: FrozenSystemIdentity) -> BoundEvaluationRequest:
        """طلبُ التقييم المربوط لهذا القارئ بعينه."""

        if identity.content_id not in {
            reader.content_id for reader in self.reader_identities
        }:
            raise EvaluationError("قارئٌ خارج الربط لا يُصدَر له طلب")
        return BoundEvaluationRequest(
            system_content_id=identity.content_id,
            contract_digest=self.contract.contract_digest,
            domain_digest=self.contract.domain_digest,
            evaluation_protocol_digest=self.protocol.protocol_digest,
        )

    @property
    def requests(self) -> tuple[BoundEvaluationRequest, ...]:
        """طلباتُ التقييم المربوطة، طلبًا لكلِّ قارئ."""

        return tuple(self.request_for(identity) for identity in self.reader_identities)

    @property
    def required_system_content_ids(self) -> tuple[str, ...]:
        """بصماتُ القرّاء المطلوبةُ تقاريرُهم قبل أيّ فتح."""

        return tuple(sorted(reader.content_id for reader in self.reader_identities))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الربط للبصمة."""

        return {
            "contract_digest": self.contract.contract_digest,
            "protocol_digest": self.protocol.protocol_digest,
            "payload_digest": self.payload.payload_digest,
            "reader_content_ids": list(self.required_system_content_ids),
        }

    @property
    def binding_digest(self) -> str:
        """بصمةُ الربط."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
