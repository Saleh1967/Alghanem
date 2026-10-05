"""اختباراتُ `G0.METRIC-0.HARDEN`: دلاليّةُ القياس، وتوثيقُ المصدر، وهندسةُ المقام.

كلُّ اختبارٍ هنا يمنع طريقًا بعينه إلى رقمٍ يوهم أكثرَ ممّا ثبت: جمعَ رتبِ
البوّابات، وتسويةَ أوزان المجالات بلا بروتوكول، وبصمةَ صياغتنا تُقرأ مرساةَ نصٍّ
قديم، وحذفَ سؤالٍ لتحسين المقام.
"""

from __future__ import annotations

import pytest

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.capability import (
    ARABIC_TOTAL_ID,
    ATTESTABLE_GATES,
    CERTIFICATE_SCHEMA_VERSION,
    COVERAGE_GEOMETRY,
    DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1,
    DECLARED_EDITIONS,
    ArabicStateCertificate,
    CapabilityCitation,
    CapabilityNodeError,
    CitationStanding,
    DerivedRatio,
    EvidenceLedger,
    GateWeight,
    MaturityStage,
    MeasurementSemanticsError,
    MeasurementWeightProtocol,
    ReadinessGateOrigin,
    ScalarStanding,
    UndeclaredScalarReason,
    derive_arabic_state_certificate,
    derive_citation_provenance_profile,
    derive_composite_coverage,
    derive_declaration_evidence,
    derive_readiness_gate_origin_profile,
)

_UNIVERSE = DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1
_SOURCE_ID = "sharh_ibn_aqil"


def _digest(label: str) -> str:
    return canonical_digest(canonical_bytes({"label": label}))


def _baseline_certificate() -> ArabicStateCertificate:
    """اشتقّ شهادةَ الأساس بشاهد الإعلان وحدَه، كما يفعل مثالُ الأساس."""

    ledger = EvidenceLedger(_UNIVERSE.leaf_ids())
    for evidence in derive_declaration_evidence(_UNIVERSE):
        ledger.consider(evidence)
    return derive_arabic_state_certificate(_UNIVERSE, ledger)


def _protocol() -> MeasurementWeightProtocol:
    """بروتوكولُ أوزانٍ اصطناعيٌّ للاختبار وحدَه؛ لا يُعلَن في المقام."""

    return MeasurementWeightProtocol(
        protocol_id="test.weight.protocol",
        weights=tuple(
            GateWeight(gate=gate, weight=1, justification="اختبارٌ لا إعلان")
            for gate in ATTESTABLE_GATES
        ),
    )


# ---------------------------------------------------------------------------
# NoOrdinalGateArithmeticWithoutDeclaredWeights
# ---------------------------------------------------------------------------


def test_no_composite_scalar_is_derived_from_gate_index() -> None:
    certificate = _baseline_certificate()
    content = certificate.as_canonical_content()
    assert "arabic_total_coverage" not in content
    assert not hasattr(certificate, "arabic_total_coverage")
    assert certificate.composite_coverage.value is None
    assert certificate.composite_coverage.standing is ScalarStanding.UNDECLARED
    assert (
        certificate.composite_coverage.reason
        is UndeclaredScalarReason.NO_DECLARED_WEIGHT_PROTOCOL
    )


def test_gate_index_is_only_ever_compared_never_accumulated() -> None:
    """`gate_index` رتبةُ ترخيصٍ تُقارَن؛ ولا تدخل جمعًا ولا قسمةً ولا متوسّطًا."""

    import ast
    from pathlib import Path

    offenders: list[str] = []
    for path in sorted(Path("src/alghanem/capability").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        parents: dict[ast.AST, ast.AST] = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Attribute) and node.attr == "gate_index"):
                continue
            parent = parents.get(node)
            if isinstance(parent, ast.Compare):
                continue
            if isinstance(parent, ast.Tuple):
                continue
            if isinstance(parent, ast.BinOp) and isinstance(parent.op, ast.Add):
                other = parent.right if parent.left is node else parent.left
                if isinstance(other, ast.Constant) and other.value == 1:
                    continue
            offenders.append(f"{path.name}:{node.lineno}")
    assert offenders == []


def test_a_composite_figure_requires_a_declared_weight_protocol() -> None:
    coverage = {gate: DerivedRatio(0, 164, "u") for gate in ATTESTABLE_GATES}
    with pytest.raises(MeasurementSemanticsError):
        derive_composite_coverage(None, coverage)  # type: ignore[arg-type]


def test_a_weight_protocol_covers_every_attestable_gate_exactly_once() -> None:
    weights = tuple(
        GateWeight(gate=gate, weight=1, justification="سبب")
        for gate in ATTESTABLE_GATES[:-1]
    )
    with pytest.raises(MeasurementSemanticsError):
        MeasurementWeightProtocol(protocol_id="partial", weights=weights)


def test_a_declared_weight_protocol_does_yield_a_declared_scalar() -> None:
    certificate = _baseline_certificate()
    coverage = {
        gate: certificate.gate_profile[name]
        for gate, name in zip(ATTESTABLE_GATES, certificate.gate_profile, strict=True)
    }
    scalar = derive_composite_coverage(_protocol(), coverage)
    assert scalar.standing is ScalarStanding.DECLARED
    assert scalar.ratio.denominator == 9 * 164
    assert scalar.ratio.numerator == 164
    assert scalar.protocol_digest == _protocol().protocol_digest


# ---------------------------------------------------------------------------
# TaxonomyGranularity != CapabilityImportance
# ---------------------------------------------------------------------------


def test_domain_balanced_coverage_has_no_scalar_without_a_weight_protocol() -> None:
    certificate = _baseline_certificate()
    assert certificate.domain_balanced_coverage.value is None
    assert (
        certificate.domain_balanced_coverage.reason
        is UndeclaredScalarReason.NO_DECLARED_DOMAIN_WEIGHT_PROTOCOL
    )
    assert certificate.dependency_weighted_coverage.value is None
    assert (
        certificate.dependency_weighted_coverage.reason
        is UndeclaredScalarReason.NO_DECLARED_DEPENDENCY_GRAPH
    )


def test_the_domain_profile_is_published_row_by_row_not_averaged() -> None:
    certificate = _baseline_certificate()
    profile = certificate.domain_coverage_profile
    assert len(profile.rows) == 17
    by_domain = {row.domain_id: row for row in profile.rows}
    assert by_domain["A2"].leaf_total > by_domain["A7"].leaf_total
    assert [row.domain_id for row in profile.rows][:3] == ["A0", "A1", "A2"]
    assert not hasattr(profile, "value")


def test_leaf_coverage_declares_its_measurement_geometry() -> None:
    certificate = _baseline_certificate()
    assert COVERAGE_GEOMETRY == "LeafCoverage"
    root = certificate.rows[ARABIC_TOTAL_ID].aggregate
    assert root.coverage_geometry == COVERAGE_GEOMETRY
    assert "granularity" in root.granularity_law.lower()


# ---------------------------------------------------------------------------
# CitationName != VerifiedSourceLocus
# ---------------------------------------------------------------------------


def test_a_source_anchor_may_not_repeat_our_conceptual_mapping_digest() -> None:
    shared = _digest("mapping")
    with pytest.raises(CapabilityNodeError):
        CapabilityCitation(
            source_id=_SOURCE_ID,
            citation_standing=CitationStanding.EXACT_TEXTUAL_LOCUS,
            edition_id=None,
            page_range="1/2",
            chapter_bab="باب",
            source_text_anchor_digest=shared,
            conceptual_mapping_digest=shared,
        )


def test_an_exact_textual_locus_requires_edition_locator_and_anchor() -> None:
    with pytest.raises(CapabilityNodeError):
        CapabilityCitation(
            source_id=_SOURCE_ID,
            citation_standing=CitationStanding.EXACT_TEXTUAL_LOCUS,
            chapter_bab="باب الماضي",
            source_text_anchor_digest=_digest("anchor"),
        )


def test_a_modern_formal_extension_carries_no_textual_locator() -> None:
    for kwargs in (
        {"page_range": "3/44"},
        {"chapter_bab": "باب"},
        {"volume": "2"},
        {"source_text_anchor_digest": _digest("anchor")},
    ):
        with pytest.raises(CapabilityNodeError):
            CapabilityCitation(
                source_id=_SOURCE_ID,
                citation_standing=CitationStanding.MODERN_FORMAL_EXTENSION,
                **kwargs,  # type: ignore[arg-type]
            )


def test_a_conceptual_correspondence_never_carries_a_source_anchor() -> None:
    with pytest.raises(CapabilityNodeError):
        CapabilityCitation(
            source_id=_SOURCE_ID,
            citation_standing=CitationStanding.CONCEPTUAL_CORRESPONDENCE,
            locus="الفاعليّة",
            source_text_anchor_digest=_digest("anchor"),
        )


def test_no_edition_is_invented_before_it_is_verified() -> None:
    assert DECLARED_EDITIONS == ()
    with pytest.raises(CapabilityNodeError):
        CapabilityCitation(
            source_id=_SOURCE_ID,
            citation_standing=CitationStanding.SECTION_LEVEL_LOCUS,
            edition_id="invented.edition",
            chapter_bab="باب",
        )


def test_the_baseline_claims_no_textually_anchored_capability() -> None:
    profile = derive_citation_provenance_profile(_UNIVERSE)
    assert profile.standing_counts[CitationStanding.EXACT_TEXTUAL_LOCUS] == 0
    assert profile.textually_anchored_coverage.numerator == 0
    assert profile.textually_anchored_coverage.denominator == 164
    assert sum(profile.standing_counts.values()) == 164


# ---------------------------------------------------------------------------
# KeepingAQuestionDoesNotLicenseAFalseCitation
# ---------------------------------------------------------------------------


def test_a7_a11_and_a14_remain_in_the_declared_denominator() -> None:
    domains = set(_UNIVERSE.domain_ids())
    assert {"A7", "A11", "A14"} <= domains
    assert len(_UNIVERSE.leaf_ids()) == 164


def test_modern_and_unverified_standings_are_declared_where_they_apply() -> None:
    standings = {
        leaf_id: _UNIVERSE.node(leaf_id).citation.citation_standing
        for leaf_id in _UNIVERSE.leaf_ids()
    }
    a7 = [value for leaf_id, value in standings.items() if leaf_id.startswith("A7.")]
    assert a7 and set(a7) == {CitationStanding.MODERN_FORMAL_EXTENSION}
    a14 = {
        leaf_id: value
        for leaf_id, value in standings.items()
        if leaf_id.startswith("A14.")
    }
    modern = [
        value
        for value in a14.values()
        if value is CitationStanding.MODERN_FORMAL_EXTENSION
    ]
    unverified = [
        value for value in a14.values() if value is CitationStanding.UNVERIFIED_LOCUS
    ]
    assert len(modern) == 4
    assert len(unverified) == 4
    assert CitationStanding.UNVERIFIED_LOCUS in {
        value for leaf_id, value in standings.items() if leaf_id.startswith("A11.")
    }


# ---------------------------------------------------------------------------
# SourceCitationDoesNotLicenseSystemCapability
# ---------------------------------------------------------------------------


def test_citation_standing_does_not_move_a_maturity_stage() -> None:
    certificate = _baseline_certificate()
    leaves = set(_UNIVERSE.leaf_ids())

    def _stages(standing: CitationStanding) -> list[MaturityStage]:
        return [
            row.measurement.attained_stage
            for node_id, row in certificate.rows.items()
            if node_id in leaves
            and row.measurement is not None
            and _UNIVERSE.node(node_id).citation.citation_standing is standing
        ]

    modern = _stages(CitationStanding.MODERN_FORMAL_EXTENSION)
    conceptual = _stages(CitationStanding.CONCEPTUAL_CORRESPONDENCE)
    unverified = _stages(CitationStanding.UNVERIFIED_LOCUS)
    assert modern and conceptual and unverified
    assert set(modern + conceptual + unverified) == {MaturityStage.S1_DECLARED}


# ---------------------------------------------------------------------------
# UniformReadinessGate != DerivedReadinessRequirement
# ---------------------------------------------------------------------------


def test_every_readiness_gate_is_still_a_declared_uniform_convention() -> None:
    profile = derive_readiness_gate_origin_profile(_UNIVERSE)
    assert profile.origin_counts[ReadinessGateOrigin.DECLARED_UNIFORM_V1] == 164
    assert profile.origin_counts[ReadinessGateOrigin.DERIVED_FROM_CAPABILITY_ROLE] == 0
    assert profile.derived_readiness_coverage.numerator == 0
    assert profile.derived_readiness_coverage.denominator == 164


# ---------------------------------------------------------------------------
# DeclaredCoverage != SystemCapability
#   DifferentMeasurementSemanticsAreNotComparableCertificates
# ---------------------------------------------------------------------------


def test_the_headline_declares_questions_not_a_percentage_of_arabic() -> None:
    certificate = _baseline_certificate()
    headline = certificate.headline_statement
    assert "164/164 declared questions" in headline
    assert "No composite Arabic capability percentage" in headline
    assert "%" not in headline


def test_the_certificate_carries_its_schema_version_in_its_own_content() -> None:
    certificate = _baseline_certificate()
    content = certificate.as_canonical_content()
    assert CERTIFICATE_SCHEMA_VERSION == "arabic-state-certificate.v2"
    assert content["certificate_schema_version"] == CERTIFICATE_SCHEMA_VERSION
    assert certificate.schema_version == CERTIFICATE_SCHEMA_VERSION


def test_two_schema_versions_are_not_directly_comparable_digests() -> None:
    certificate = _baseline_certificate()
    content = dict(certificate.as_canonical_content())
    content["certificate_schema_version"] = "arabic-state-certificate.v1"
    v1_digest = canonical_digest(canonical_bytes(content))
    assert v1_digest != certificate.certificate_digest
