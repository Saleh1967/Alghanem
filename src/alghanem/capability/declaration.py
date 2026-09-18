"""`G0.METRIC-0`: شاهدُ الإعلان مُشتَقًّا من المقام، لا مكتوبًا بجانبه.

عضويّةُ البابِ في المقام المُعلَن **هي** إعلانُه؛ فبوّابةُ `S1_DECLARED` تُغلَق
من `UniverseManifest` نفسِه ولا تُكتب يدويًّا لعقدةٍ دون أخرى. وما فوقها لا
يُغلَق بهذا المسار البتّة: `DECLARATION_RECORD` لا يرخّص إلّا درجةَ الإعلان،
فالإعلانُ لا يصير نموذجًا ولا تنفيذًا بكثرة تكراره.
"""

from __future__ import annotations

from ..canonical_content import canonical_bytes, canonical_digest
from .evidence import AuthorityPath, EvidenceScope, ScopedCapabilityEvidence
from .maturity import MaturityStage
from .universe import CapabilityUniverse

__all__ = [
    "DECLARATION_PROTOCOL_ID",
    "declaration_protocol_digest",
    "derive_declaration_evidence",
]

DECLARATION_PROTOCOL_ID: str = "alghanem.g0_metric_0.declaration_record.v1"
"""بروتوكولُ شاهد الإعلان: إعلانُ العقدة في المقام، ولا شيءَ فوقه."""


def declaration_protocol_digest() -> str:
    """مُلخَّصُ بروتوكول الإعلان؛ جزءٌ من مفتاح توحيد الشواهد."""

    return canonical_digest(
        canonical_bytes(
            {
                "protocol_id": DECLARATION_PROTOCOL_ID,
                "licensed_gate": MaturityStage.S1_DECLARED.value,
            }
        )
    )


def derive_declaration_evidence(
    universe: CapabilityUniverse,
) -> tuple[ScopedCapabilityEvidence, ...]:
    """اشتقّ شاهدَ الإعلان لكلّ ورقةٍ في المقام، من بيان المقام وحدَه."""

    manifest = universe.manifest
    protocol = declaration_protocol_digest()
    scope = EvidenceScope(
        corpus_id=manifest.universe_id,
        corpus_digest=manifest.content_digest,
        layer="declared_denominator",
        population="declared_capability_leaves",
    )
    return tuple(
        ScopedCapabilityEvidence(
            capability_id=leaf_id,
            attested_gate=MaturityStage.S1_DECLARED,
            authority_path=AuthorityPath.DECLARATION_RECORD,
            scope=scope,
            authority_reference=f"{manifest.universe_id}#{leaf_id}",
            experiment_content_digest=universe.node(leaf_id).node_digest,
            protocol_digest=protocol,
        )
        for leaf_id in universe.leaf_ids()
    )
