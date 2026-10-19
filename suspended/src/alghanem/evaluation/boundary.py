"""`G0.EVAL-0.BOUNDARY`: حدُّ القارئ المحجوب، تسليمًا ببايتاتٍ مُسلسَلةٍ فقط.

القارئُ لا يستلم كائنَ بايثون: لا عقدًا، ولا عقدةً ليفيّة، ولا مُحوِّلَ مجال.
فمن سلّم كائنًا سلّم معه طريقًا إلى الوحدات التي بنته، ومنها مادّةُ الجواب.
إنّما يستلم `canonical bytes` لحمولةٍ مُسقَطة:

* تدخل: أعضاءُ المجال بمدخلاتها المرصودة، والفروقُ المقبولة بقيمها، وهندسةُ
  الخانات، ومعاييرُ النجاح، وإحالةُ سقف الرتبة.
* لا تدخل: الالتزامُ، ومؤلِّفُ العقد، وأثرُ العقدة — فالأثرُ يسمّي مصدرَ المادّة
  وقد يسمّي فرعًا، وتسميةُ الفرع كشفٌ لجوابه.

وحدُّ الاستيراد هنا مقيسٌ على مصدر القارئ المُصرَّح وما يبلغه، وسقفُه مُعلَنٌ لا
مُدَّعًى: `StaticImportAudit != ProcessIsolation`. وحبسُ العمليّة يُسجَّل
`DECLARED_DEFERRED` في هذا الطور، ولا يُدَّعى إنجازُه صمتًا.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..import_boundary import (
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    ImportBoundaryPolicy,
    ImportBoundaryReport,
    audit_import_boundary,
)
from ..prior_fiber import FiberContract
from .laws import (
    A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES,
    EvaluationError,
    ProcessConfinementStanding,
)

__all__ = [
    "BLIND_PAYLOAD_SCHEME",
    "READER_FORBIDDEN_MODULES",
    "READER_FORBIDDEN_PACKAGES",
    "READER_IMPORT_POLICY",
    "READER_PERMITTED_MODULES",
    "BlindPayload",
    "ProcessConfinementDeclaration",
    "issue_blind_payload",
    "reader_import_audit",
]

BLIND_PAYLOAD_SCHEME: Final = (
    "حمولةُ قراءةٍ مُسقَطة: أعضاءٌ بمدخلاتٍ مرصودة، وفروقٌ بقيمها، وخاناتٌ، "
    "ومعاييرُ نجاح، وإحالةُ سقف رتبة؛ بلا التزامٍ ولا مؤلِّفٍ ولا أثر"
)

READER_FORBIDDEN_PACKAGES: tuple[str, ...] = (
    "arabic",
    "prior_fiber",
    "evaluation",
    "prior",
    "kernel",
    "linguistic",
    "realization",
    "ontology",
    "metaalgebra",
    "structural_dal",
    "fractal_generation",
    "fractal_experiment",
    "generation",
    "program",
    "execution",
    "encyclopedia",
)
"""حزمٌ لا يبلغها قارئٌ مُمتحَن: مادّةُ المجال، وطبقةُ العقد، وسلطةُ الفتح."""

READER_FORBIDDEN_MODULES: tuple[str, ...] = (
    "alghanem.arabic.madlul_alone_formal",
    "alghanem.arabic.fiber_contracts",
    "alghanem.prior_fiber.commitment",
    "alghanem.evaluation.reveal",
)
"""وحداتٌ مُسمّاةٌ بعينها: مادّةُ الجواب، ومُحوِّلُه، والتزامُه، وسلطةُ فتحه."""

READER_PERMITTED_MODULES: tuple[str, ...] = ("canonical_content",)
"""ما يجوز بلوغُه من المشروع: البصمةُ القانونيّة وحدَها، والحمولةُ بايتاتٌ تُمرَّر."""

READER_IMPORT_POLICY: ImportBoundaryPolicy = ImportBoundaryPolicy(
    policy_id="policy.evaluation.reader.g0_eval_0",
    permitted_modules=READER_PERMITTED_MODULES,
    forbidden_packages=READER_FORBIDDEN_PACKAGES,
    forbidden_modules=READER_FORBIDDEN_MODULES,
    forbid_dynamic_access=True,
)
"""سياسةُ حدِّ القارئ فوق البدائيّة المشتركة، لا منطقٌ ثانٍ بجانبها."""


def reader_import_audit(implementation_files: tuple[Path, ...]) -> ImportBoundaryReport:
    """افحص حدَّ قارئٍ على مصدره المُصرَّح وما يبلغه منه."""

    return audit_import_boundary(implementation_files, READER_IMPORT_POLICY)


@dataclass(frozen=True, slots=True)
class ProcessConfinementDeclaration:
    """تصريحٌ بحال حبس العمليّة؛ يُسجَّل تأجيلُه ولا يُدَّعى إنجازُه."""

    standing: ProcessConfinementStanding = ProcessConfinementStanding.DECLARED_DEFERRED

    def __post_init__(self) -> None:
        if not isinstance(self.standing, ProcessConfinementStanding):
            raise EvaluationError("حالُ حبس العمليّة عضوٌ في مفردته المغلقة")

    @property
    def is_proven(self) -> bool:
        """أمُثبَتٌ حبسُ العمليّة؟ ولا إثباتَ في هذا الطور بالبناء."""

        return self.standing.is_proven

    @property
    def ceiling(self) -> str:
        """سقفُ ما يُدَّعى بالفحص الثابت."""

        return STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للسجلّ."""

        return {
            "standing": self.standing.value,
            "is_proven": self.is_proven,
            "ceiling": self.ceiling,
        }


@dataclass(frozen=True, slots=True)
class BlindPayload:
    """ما يستلمه القارئ فعلًا: بايتاتٌ قانونيّةٌ وبصمتُها، لا كائنٌ ولا مرجع."""

    payload_bytes: bytes
    contract_digest: str
    domain_digest: str
    protocol_digest: str

    def __post_init__(self) -> None:
        if type(self.payload_bytes) is not bytes or not self.payload_bytes:
            raise EvaluationError(A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES)

    @property
    def payload_digest(self) -> str:
        """بصمةُ ما سُلِّم فعلًا؛ يُطابَق عليها تقريرُ التشغيل."""

        return canonical_digest(self.payload_bytes)

    @property
    def delivery_law(self) -> str:
        """قانونُ التسليم: بايتاتٌ مُسلسَلة لا كائن."""

        return A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES

    def withholds(self, label: str) -> bool:
        """أمحجوبٌ هذا الجوابُ عن البايتات المُسلَّمة؟ يُفحَص على ما سُلِّم."""

        if not isinstance(label, str) or not label.strip():
            raise EvaluationError("الجوابُ المسؤولُ عنه نصٌّ غير فارغ")
        return label not in self.payload_bytes.decode("utf-8", "surrogatepass")


def _payload_content(
    contract: FiberContract, protocol_digest: str
) -> dict[str, object]:
    node = contract.node
    return {
        "payload_scheme": BLIND_PAYLOAD_SCHEME,
        "contract_id": contract.contract_id,
        "contract_digest": contract.contract_digest,
        "domain_digest": contract.domain_digest,
        "protocol_digest": protocol_digest,
        "slot_geometry": list(node.slot_geometry),
        "admissible_distinctions": [
            distinction.as_canonical_content()
            for distinction in sorted(
                node.admissible_distinctions, key=lambda item: item.distinction_id
            )
        ],
        "relations": list(node.relations),
        "capabilities": list(node.capabilities),
        "gates": list(node.gates),
        "residual_policy": contract.residual_policy,
        "rank_ceiling_ref": node.rank_reference.rank_ceiling_ref,
        "success_criteria": [
            criterion.value
            for criterion in sorted(
                contract.success_criteria, key=lambda item: item.value
            )
        ],
        "members": [
            member.as_canonical_content()
            for member in sorted(contract.members, key=lambda item: item.member_id)
        ],
    }


def issue_blind_payload(
    contract: FiberContract, *, protocol_digest: str
) -> BlindPayload:
    """أصدِر حمولةَ القراءة بايتاتٍ قانونيّةً مُسقَطةً من عقدٍ مُجمَّد."""

    if not isinstance(contract, FiberContract):
        raise EvaluationError("الحمولةُ تُشتَقُّ من عقدٍ مُجمَّدٍ من نوعه")
    payload = _payload_content(contract, protocol_digest)
    encoded = canonical_bytes(payload)
    decoded = encoded.decode("utf-8", "surrogatepass")
    if contract.gold_commitment.commitment_digest in decoded:
        raise EvaluationError("الالتزامُ لا يُسلَّم إلى القارئ؛ فالحمولةُ مجالٌ لا ختم")
    if contract.authored_by in decoded:
        raise EvaluationError("مؤلِّفُ العقد لا يُسلَّم إلى القارئ؛ فهو طريقٌ إلى مادّته")
    return BlindPayload(
        payload_bytes=encoded,
        contract_digest=contract.contract_digest,
        domain_digest=contract.domain_digest,
        protocol_digest=protocol_digest,
    )
