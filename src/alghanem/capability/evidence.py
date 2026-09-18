"""`G0.METRIC-0`: الشاهدُ مُنطَّقًا بمسار سلطته، لا مردودًا إلى إيصالٍ واحد.

`EvidenceMustHaveAnAuthorityPath`: للتجربة التنفيذيّة سلطتُها، وللقياس سلطتُه،
وللبرهان الصوريّ والإحصاء والمدوَّنة سلطاتُها؛ وإحالةُ هذه كلِّها قسرًا إلى
عمليّة قارئٍ لتدخل النظامَ تزييفٌ لجنس الشاهد لا تقويةٌ له.

ولكلّ مسارٍ **بوّاباتٌ يرخّصها وحدَها**: الاستدعاءُ المباشر داخل العمليّة لا
يمنح `BLIND` ولا `TRANSFER` ولا `GOLD`، وإنّما يُسجَّل برتبته الأدنى الصريحة.
والإحالةُ المكرَّرة إلى الشاهد نفسِه شاهدٌ واحد، تُوحَّد على مفتاحٍ مُسنون.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .maturity import MaturityStage

__all__ = [
    "AuthorityPath",
    "EvidenceError",
    "EvidenceLedger",
    "EvidencePolarity",
    "EvidenceRefusal",
    "EvidenceScope",
    "RefusalCode",
    "ResidualDisclosure",
    "ScopedCapabilityEvidence",
    "licensable_gates",
]


class EvidenceError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في بناء الشاهد؛ لا حملَ على أقرب حالة."""


class AuthorityPath(Enum):
    """مساراتُ السلطة المُنمَّطة؛ مفردةٌ مغلقة لا يُضاف إليها مسارٌ صمتًا."""

    DECLARATION_RECORD = "DECLARATION_RECORD"
    FROZEN_FORMAL_PROOF = "FROZEN_FORMAL_PROOF"
    PREREGISTERED_MEASUREMENT = "PREREGISTERED_MEASUREMENT"
    MEASUREMENT_RUN_MANIFEST = "MEASUREMENT_RUN_MANIFEST"
    BOUND_EXECUTION_RECEIPT = "BOUND_EXECUTION_RECEIPT"
    CORPUS_WITNESS = "CORPUS_WITNESS"
    GOLD_CONTRACT_RESULT = "GOLD_CONTRACT_RESULT"
    BLIND_EVALUATION_REPORT = "BLIND_EVALUATION_REPORT"
    TRANSFER_RESULT = "TRANSFER_RESULT"
    REPRODUCED_HISTORICAL_EXPERIMENT = "REPRODUCED_HISTORICAL_EXPERIMENT"
    IN_PROCESS_MEASUREMENT_REPLAY = "IN_PROCESS_MEASUREMENT_REPLAY"


_LICENSABLE_GATES: Final[dict[AuthorityPath, frozenset[MaturityStage]]] = {
    AuthorityPath.DECLARATION_RECORD: frozenset({MaturityStage.S1_DECLARED}),
    AuthorityPath.FROZEN_FORMAL_PROOF: frozenset(
        {
            MaturityStage.S1_DECLARED,
            MaturityStage.S2_MODELED,
            MaturityStage.S5_FROZEN_DOMAIN,
        }
    ),
    AuthorityPath.PREREGISTERED_MEASUREMENT: frozenset(
        {
            MaturityStage.S1_DECLARED,
            MaturityStage.S2_MODELED,
            MaturityStage.S5_FROZEN_DOMAIN,
        }
    ),
    AuthorityPath.MEASUREMENT_RUN_MANIFEST: frozenset(
        {
            MaturityStage.S2_MODELED,
            MaturityStage.S3_EXECUTABLE,
            MaturityStage.S4_TESTED,
            MaturityStage.S5_FROZEN_DOMAIN,
        }
    ),
    AuthorityPath.BOUND_EXECUTION_RECEIPT: frozenset(
        {MaturityStage.S3_EXECUTABLE, MaturityStage.S4_TESTED}
    ),
    AuthorityPath.CORPUS_WITNESS: frozenset(
        {MaturityStage.S4_TESTED, MaturityStage.S5_FROZEN_DOMAIN}
    ),
    AuthorityPath.GOLD_CONTRACT_RESULT: frozenset({MaturityStage.S6_GOLD_EVALUATED}),
    AuthorityPath.BLIND_EVALUATION_REPORT: frozenset({MaturityStage.S7_BLIND_VERIFIED}),
    AuthorityPath.TRANSFER_RESULT: frozenset({MaturityStage.S8_TRANSFER_VERIFIED}),
    AuthorityPath.REPRODUCED_HISTORICAL_EXPERIMENT: frozenset(
        {MaturityStage.S9_REPRODUCED}
    ),
    AuthorityPath.IN_PROCESS_MEASUREMENT_REPLAY: frozenset(
        {
            MaturityStage.S1_DECLARED,
            MaturityStage.S2_MODELED,
            MaturityStage.S3_EXECUTABLE,
        }
    ),
}
"""ما يرخّصه كلُّ مسارٍ من البوّابات؛ وما وراءه ترقيةٌ بلا إذنٍ تُرفَض وتُسجَّل."""


def licensable_gates(path: AuthorityPath) -> frozenset[MaturityStage]:
    """البوّاباتُ التي يرخّصها هذا المسارُ وحدَه."""

    if not isinstance(path, AuthorityPath):
        raise EvidenceError("a licensing question requires an authority path")
    return _LICENSABLE_GATES[path]


class EvidencePolarity(Enum):
    """قطبُ الشاهد: مُثبِتٌ للبوّابة أو ناقضٌ لها؛ والناقضُ لا يُحذَف."""

    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


class ResidualDisclosure(Enum):
    """هل أفصح الشاهدُ عن بواقيه؟ الإفصاحُ بالصفر إفصاحٌ، والسكوتُ ليس إفصاحًا."""

    DISCLOSED = "DISCLOSED"
    UNDISCLOSED = "UNDISCLOSED"


class RefusalCode(Enum):
    """أجناسُ الرفض عند النظر في الشاهد؛ تُسجَّل ولا تُبتلَع."""

    UNKNOWN_CAPABILITY = "UNKNOWN_CAPABILITY"
    UNAUTHORIZED_UPGRADE = "UNAUTHORIZED_UPGRADE"
    UNDISCLOSED_RESIDUALS = "UNDISCLOSED_RESIDUALS"
    REPEATED_REFERENCE = "REPEATED_REFERENCE"


@dataclass(frozen=True)
class EvidenceScope:
    """نطاقُ الشاهد: مدوَّنتُه وبصمتُها وطبقتُه وجمهورُه؛ شاهدٌ بلا نطاقٍ ليس شاهدًا."""

    corpus_id: str
    corpus_digest: str
    layer: str
    population: str

    def __post_init__(self) -> None:
        for name in ("corpus_id", "layer", "population"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise EvidenceError(f"an evidence scope requires a non-empty «{name}»")
        if not is_canonical_digest(self.corpus_digest):
            raise EvidenceError("an evidence scope requires a canonical corpus digest")

    def as_canonical_content(self) -> dict[str, str]:
        """المحتوى القانونيّ للنطاق."""

        return {
            "corpus_id": self.corpus_id,
            "corpus_digest": self.corpus_digest,
            "layer": self.layer,
            "population": self.population,
        }

    @property
    def scope_digest(self) -> str:
        """مُلخَّصُ النطاق؛ جزءٌ من مفتاح توحيد الشواهد."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True)
class ScopedCapabilityEvidence:
    """شاهدٌ مُنطَّقٌ لقدرةٍ بعينها عند بوّابةٍ بعينها، بمسار سلطةٍ مُصرَّحٍ به."""

    capability_id: str
    attested_gate: MaturityStage
    authority_path: AuthorityPath
    scope: EvidenceScope
    authority_reference: str
    experiment_content_digest: str
    protocol_digest: str
    gold_contract_digest: str | None = None
    polarity: EvidencePolarity = EvidencePolarity.POSITIVE
    identity_preserved: bool = True
    residual_disclosure: ResidualDisclosure = ResidualDisclosure.DISCLOSED
    residuals: tuple[str, ...] = field(default=())

    def __post_init__(self) -> None:
        if type(self.capability_id) is not str or not self.capability_id.strip():
            raise EvidenceError("evidence requires a capability_id")
        if not isinstance(self.attested_gate, MaturityStage):
            raise EvidenceError("evidence attests a maturity gate")
        if not self.attested_gate.is_an_attestable_gate:
            raise EvidenceError("absence is measured by want of evidence, not attested")
        if not isinstance(self.authority_path, AuthorityPath):
            raise EvidenceError(
                "evidence must have an authority path: an unsourced record is "
                "a claim, not evidence"
            )
        if not isinstance(self.scope, EvidenceScope):
            raise EvidenceError("evidence requires a declared scope")
        if type(self.authority_reference) is not str or not self.authority_reference:
            raise EvidenceError("evidence names the artifact its authority issued")
        for name in ("experiment_content_digest", "protocol_digest"):
            if not is_canonical_digest(getattr(self, name)):
                raise EvidenceError(f"evidence requires a canonical «{name}»")
        if self.gold_contract_digest is not None and not is_canonical_digest(
            self.gold_contract_digest
        ):
            raise EvidenceError("a gold contract digest must be canonical when present")
        if not isinstance(self.polarity, EvidencePolarity):
            raise EvidenceError("evidence carries a polarity")
        if type(self.identity_preserved) is not bool:
            raise EvidenceError("identity preservation is a bool, never a truthy value")
        if not isinstance(self.residual_disclosure, ResidualDisclosure):
            raise EvidenceError("evidence declares whether it disclosed its residuals")
        if type(self.residuals) is not tuple or any(
            type(item) is not str or not item.strip() for item in self.residuals
        ):
            raise EvidenceError("residuals are a tuple of named codes")
        if (
            self.residual_disclosure is ResidualDisclosure.UNDISCLOSED
            and self.residuals
        ):
            raise EvidenceError("undisclosed residuals cannot also be listed")

    @property
    def licenses_its_gate(self) -> bool:
        """هل يرخّص مسارُ هذا الشاهد البوّابةَ التي يدّعيها؟"""

        return self.attested_gate in licensable_gates(self.authority_path)

    @property
    def evidence_key(self) -> tuple[str, str, str, str, str]:
        """مفتاحُ التوحيد المُسنون؛ الإحالةُ المكرَّرة ليست شاهدًا مستقلًّا."""

        return (
            self.capability_id,
            self.scope.scope_digest,
            self.experiment_content_digest,
            self.gold_contract_digest or "",
            self.protocol_digest,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للشاهد."""

        return {
            "capability_id": self.capability_id,
            "attested_gate": self.attested_gate.value,
            "authority_path": self.authority_path.value,
            "scope": self.scope.as_canonical_content(),
            "authority_reference": self.authority_reference,
            "experiment_content_digest": self.experiment_content_digest,
            "protocol_digest": self.protocol_digest,
            "gold_contract_digest": self.gold_contract_digest,
            "polarity": self.polarity.value,
            "identity_preserved": self.identity_preserved,
            "residual_disclosure": self.residual_disclosure.value,
            "residuals": list(self.residuals),
        }

    @property
    def evidence_digest(self) -> str:
        """مُلخَّصُ محتوى الشاهد."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True)
class EvidenceRefusal:
    """شاهدٌ نُظِر فيه فرُدَّ؛ يُسجَّل بجنس رفضه ليُقاس، لا يُطرح صامتًا."""

    evidence: ScopedCapabilityEvidence
    refusal_code: RefusalCode

    def __post_init__(self) -> None:
        if not isinstance(self.evidence, ScopedCapabilityEvidence):
            raise EvidenceError("a refusal records the evidence it refused")
        if not isinstance(self.refusal_code, RefusalCode):
            raise EvidenceError("a refusal is named from the closed vocabulary")

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للرفض."""

        return {
            "refusal_code": self.refusal_code.value,
            "evidence_digest": self.evidence.evidence_digest,
            "capability_id": self.evidence.capability_id,
            "attested_gate": self.evidence.attested_gate.value,
            "authority_path": self.evidence.authority_path.value,
        }


class EvidenceLedger:
    """دفترُ الشواهد: يقبل ويرفض ويسجّل الرفضَ، ويوحّد المكرَّر على مفتاحه."""

    __slots__ = ("_known_capabilities", "_admitted", "_refusals", "_keys")

    def __init__(self, known_capabilities: Iterable[str]) -> None:
        self._known_capabilities = frozenset(known_capabilities)
        self._admitted: list[ScopedCapabilityEvidence] = []
        self._refusals: list[EvidenceRefusal] = []
        self._keys: set[tuple[str, str, str, str, str]] = set()

    def consider(
        self, evidence: ScopedCapabilityEvidence
    ) -> EvidenceRefusal | ScopedCapabilityEvidence:
        """انظر في الشاهد: فإمّا أُدخِل في الدفتر، وإمّا رُدَّ بجنسٍ مُسمًّى."""

        if not isinstance(evidence, ScopedCapabilityEvidence):
            raise EvidenceError("a ledger considers scoped capability evidence")
        refusal_code = self._refusal_code_for(evidence)
        if refusal_code is not None:
            refusal = EvidenceRefusal(evidence=evidence, refusal_code=refusal_code)
            self._refusals.append(refusal)
            return refusal
        self._keys.add(evidence.evidence_key)
        self._admitted.append(evidence)
        return evidence

    def _refusal_code_for(
        self, evidence: ScopedCapabilityEvidence
    ) -> RefusalCode | None:
        if evidence.capability_id not in self._known_capabilities:
            return RefusalCode.UNKNOWN_CAPABILITY
        if not evidence.licenses_its_gate:
            return RefusalCode.UNAUTHORIZED_UPGRADE
        if evidence.residual_disclosure is ResidualDisclosure.UNDISCLOSED:
            return RefusalCode.UNDISCLOSED_RESIDUALS
        if evidence.evidence_key in self._keys:
            return RefusalCode.REPEATED_REFERENCE
        return None

    def extend(self, items: Iterable[ScopedCapabilityEvidence]) -> None:
        """انظر في جملةٍ من الشواهد على الترتيب."""

        for item in items:
            self.consider(item)

    @property
    def admitted(self) -> tuple[ScopedCapabilityEvidence, ...]:
        """الشواهدُ المقبولة بترتيب نظرها."""

        return tuple(self._admitted)

    @property
    def refusals(self) -> tuple[EvidenceRefusal, ...]:
        """الشواهدُ المردودة بجنس ردّها؛ منها تُشتَقّ مؤشّراتُ الحوكمة."""

        return tuple(self._refusals)

    @property
    def considered_count(self) -> int:
        """عددُ ما نُظِر فيه: المقبولُ والمردودُ معًا، وهو مقامُ الحوكمة."""

        return len(self._admitted) + len(self._refusals)

    def for_capability(self, capability_id: str) -> tuple[ScopedCapabilityEvidence, ...]:
        """شواهدُ قدرةٍ بعينها من المقبول وحدَه."""

        return tuple(
            item for item in self._admitted if item.capability_id == capability_id
        )
