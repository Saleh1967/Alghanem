"""اختباراتُ `G0.METRIC-0`: المقامُ المُعلَن، والغيابُ المقيس، والشهادةُ المُشتَقّة."""

from __future__ import annotations

import pytest

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.capability import (
    ARABIC_TOTAL_ID,
    CAPABILITY_LAWS,
    DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1,
    DECLARED_SOURCES,
    GATE_SEQUENCE,
    UNIVERSE_V1_ID,
    AggregationError,
    AuthorityPath,
    CapabilityCitation,
    CapabilityNode,
    CapabilityNodeError,
    CapabilityUniverse,
    CapabilityUniverseError,
    DerivedRatio,
    EvidenceError,
    EvidenceLedger,
    EvidencePolarity,
    EvidenceRefusal,
    EvidenceScope,
    MaturityStage,
    NodeKind,
    RefusalCode,
    Requirement,
    ResidualDisclosure,
    ScopedCapabilityEvidence,
    build_declared_universe_v1,
    capability_import_isolation_audit,
    derive_arabic_state_certificate,
    derive_declaration_evidence,
    licensable_gates,
    measure_leaves,
)

_UNIVERSE = DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1


def _digest(label: str) -> str:
    return canonical_digest(canonical_bytes({"label": label}))


def _scope(label: str = "corpus.test") -> EvidenceScope:
    return EvidenceScope(
        corpus_id=label,
        corpus_digest=_digest(label),
        layer="test_layer",
        population="test_population",
    )


def _evidence(
    capability_id: str,
    gate: MaturityStage,
    path: AuthorityPath,
    *,
    experiment: str = "experiment.one",
    polarity: EvidencePolarity = EvidencePolarity.POSITIVE,
    identity_preserved: bool = True,
    residuals: tuple[str, ...] = (),
) -> ScopedCapabilityEvidence:
    return ScopedCapabilityEvidence(
        capability_id=capability_id,
        attested_gate=gate,
        authority_path=path,
        scope=_scope(),
        authority_reference=f"artifact::{capability_id}::{gate.value}",
        experiment_content_digest=_digest(experiment),
        protocol_digest=_digest("protocol"),
        polarity=polarity,
        identity_preserved=identity_preserved,
        residuals=residuals,
    )


def _seeded_ledger() -> EvidenceLedger:
    ledger = EvidenceLedger(_UNIVERSE.leaf_ids())
    ledger.extend(derive_declaration_evidence(_UNIVERSE))
    return ledger


# ---------------------------------------------------------------- the denominator


def test_the_denominator_holds_every_declared_top_domain() -> None:
    """المقامُ يحمل المجالات العليا السبعةَ عشرَ كاملةً لا ما بُني منها."""

    assert _UNIVERSE.universe_id == UNIVERSE_V1_ID
    assert _UNIVERSE.root_id == ARABIC_TOTAL_ID
    assert set(_UNIVERSE.domain_ids()) == {f"A{index}" for index in range(17)}


def test_the_denominator_contains_capabilities_no_module_implements() -> None:
    """أبوابٌ لا تنفيذَ لها في الشجرة تبقى عقدًا في المقام لا فراغًا خارجه."""

    for absent in (
        "A14.EVENT_REFERENCE_TIME_RELATION",
        "A13.INSHA_MODE",
        "A15.MAFHUM_MUKHALAFA",
        "A16.TANZIL",
    ):
        assert _UNIVERSE.node(absent).kind is NodeKind.CAPABILITY


def test_the_denominator_is_not_derived_from_the_implementation() -> None:
    """لا تبلغ طبقةُ القياس مادّةَ مجالٍ مبنيّةً ولا سلطةَ نواة."""

    report = capability_import_isolation_audit()
    assert report.violations == ()
    assert not any(
        module.startswith("alghanem.arabic") or module.startswith("alghanem.kernel")
        for module in report.reached_modules
    )


def test_every_denominator_node_carries_a_citation() -> None:
    """عقدةٌ بلا استشهادٍ رأيٌ لا مقام؛ وكلُّ استشهادٍ من المصادر المُعلَنة."""

    declared = {source.source_id for source in DECLARED_SOURCES}
    for node_id in _UNIVERSE.node_ids():
        node = _UNIVERSE.node(node_id)
        assert node.citation.source_id in declared
        assert node.citation.locus.strip()


def test_a_node_cannot_cite_an_undeclared_source() -> None:
    """المصدرُ المُخترَع يُرفَض عند البناء لا بعد ظهوره في رقم."""

    with pytest.raises(CapabilityNodeError):
        CapabilityCitation(source_id="a_book_i_invented", locus="بابٌ ما")


def test_a_capability_node_has_no_status_field() -> None:
    """ليس في العقدة حقلُ حالةٍ ولا نسبةٍ ولا درجةٍ يكتبها صاحبُها."""

    fields = set(CapabilityNode.__dataclass_fields__)
    assert fields == {
        "node_id",
        "title",
        "kind",
        "parent_id",
        "requirement",
        "citation",
        "readiness_gate",
    }
    for forbidden in ("stage", "attained", "coverage", "percent", "done", "status"):
        assert forbidden not in fields


def test_the_manifest_freezes_the_denominator_content() -> None:
    """بيانُ المقام مُشتَقٌّ ومستقرّ؛ إعادةُ البناء تُخرِج المُلخَّصَ نفسَه."""

    rebuilt = build_declared_universe_v1()
    assert rebuilt.manifest == _UNIVERSE.manifest
    assert rebuilt.manifest.leaf_count == len(_UNIVERSE.leaf_ids())


def test_an_orphan_node_is_outside_the_denominator() -> None:
    """عقدةٌ لا تبلغ الجذرَ خارجُ المقام؛ تُرفَض ولا تُلحَق صمتًا."""

    citation = CapabilityCitation(source_id="sharh_ibn_aqil", locus="بابٌ")
    root = CapabilityNode(
        node_id="ROOT",
        title="جذر",
        kind=NodeKind.TOTAL,
        parent_id=None,
        requirement=Requirement.REQUIRED,
        citation=citation,
        readiness_gate=MaturityStage.S4_TESTED,
    )
    orphan = CapabilityNode(
        node_id="ORPHAN",
        title="يتيمة",
        kind=NodeKind.CAPABILITY,
        parent_id="ABSENT_PARENT",
        requirement=Requirement.REQUIRED,
        citation=citation,
        readiness_gate=MaturityStage.S4_TESTED,
    )
    with pytest.raises(CapabilityUniverseError):
        CapabilityUniverse("u", (root, orphan))


# ------------------------------------------------------------- absence is a number


def test_a_leaf_without_evidence_is_measured_not_refused() -> None:
    """ورقةٌ بلا شاهدٍ غيابٌ مقيسٌ بمانِعِه وبوّابته، لا خطأُ بناء."""

    measurements = measure_leaves(_UNIVERSE, EvidenceLedger(_UNIVERSE.leaf_ids()))
    row = measurements["A14.EVENT_REFERENCE_TIME_RELATION"]
    assert row.attained_stage is MaturityStage.S0_ABSENT
    assert row.blocking_reason == "DECLARATION_ABSENT"
    assert row.next_gate is MaturityStage.S1_DECLARED
    assert row.evidence_count == 0


def test_an_unimplemented_capability_lowers_coverage_rather_than_vanishing() -> None:
    """القدرةُ غيرُ المبنيّة تُخفِض التغطية؛ ولا تُخرَج من المقام لترتفع."""

    certificate = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger())
    executable = certificate.coverage["ExecutableCoverage"]
    assert executable.denominator == _UNIVERSE.manifest.leaf_count
    assert executable.numerator == 0
    assert certificate.coverage["DeclaredCoverage"].value == 1.0


def test_expanding_the_denominator_lowers_the_ratio() -> None:
    """توسعةُ المقام تُنقِص النسبةَ؛ ومقياسٌ لا ينزل ليس مقياسًا."""

    small = CapabilityUniverse(
        "small",
        (
            _UNIVERSE.node(ARABIC_TOTAL_ID),
            _UNIVERSE.node("A0"),
            _UNIVERSE.node("A0.SOUND"),
        ),
    )
    small_ledger = EvidenceLedger(small.leaf_ids())
    small_ledger.extend(derive_declaration_evidence(small))
    before = derive_arabic_state_certificate(small, small_ledger)

    wide = CapabilityUniverse(
        "wide",
        (
            _UNIVERSE.node(ARABIC_TOTAL_ID),
            _UNIVERSE.node("A0"),
            _UNIVERSE.node("A0.SOUND"),
            _UNIVERSE.node("A0.MAKHARIJ"),
            _UNIVERSE.node("A0.SYLLABLE"),
        ),
    )
    wide_ledger = EvidenceLedger(wide.leaf_ids())
    wide_ledger.extend(
        item
        for item in derive_declaration_evidence(wide)
        if item.capability_id == "A0.SOUND"
    )
    after = derive_arabic_state_certificate(wide, wide_ledger)

    assert before.coverage["DeclaredCoverage"].value == 1.0
    assert after.coverage["DeclaredCoverage"].value == pytest.approx(1 / 3)


# ---------------------------------------------------------------- maturity gates


def test_the_maturity_ladder_has_ten_named_gates() -> None:
    """سلّمُ النضج عشرُ بوّابات مُسمّاة، لا خمسُ رتبٍ مختصرة."""

    assert len(GATE_SEQUENCE) == 10
    assert GATE_SEQUENCE[0] is MaturityStage.S0_ABSENT
    assert GATE_SEQUENCE[-1] is MaturityStage.S9_REPRODUCED
    assert MaturityStage.S7_BLIND_VERIFIED in GATE_SEQUENCE
    assert MaturityStage.S8_TRANSFER_VERIFIED in GATE_SEQUENCE


def test_a_gate_carries_its_reading_law() -> None:
    """البوّابةُ تحمل سقفَ قراءتها: ترخيصٌ لا مقدارٌ معرفيّ يُجمَع."""

    assert "StandingsAreGatesNotEpistemicMagnitudes" in (
        MaturityStage.S6_GOLD_EVALUATED.ordering_law
    )


def test_a_gate_claimed_over_an_open_gate_does_not_raise_the_stage() -> None:
    """ادّعاءٌ عند بوّابةٍ فوق أخرى مفتوحة يُرصَد قفزًا ولا يرفع الدرجة."""

    ledger = _seeded_ledger()
    ledger.consider(
        _evidence(
            "A0.SOUND",
            MaturityStage.S6_GOLD_EVALUATED,
            AuthorityPath.GOLD_CONTRACT_RESULT,
        )
    )
    row = measure_leaves(_UNIVERSE, ledger)["A0.SOUND"]
    assert row.attained_stage is MaturityStage.S1_DECLARED
    assert row.jumped_gates == (MaturityStage.S6_GOLD_EVALUATED,)
    assert not row.has_no_jump


def test_a_contiguous_chain_raises_the_stage() -> None:
    """إغلاقُ البوّابات على التوالي يرفع الدرجةَ بلا قفز."""

    ledger = _seeded_ledger()
    chain = (
        (MaturityStage.S2_MODELED, AuthorityPath.FROZEN_FORMAL_PROOF),
        (MaturityStage.S3_EXECUTABLE, AuthorityPath.BOUND_EXECUTION_RECEIPT),
        (MaturityStage.S4_TESTED, AuthorityPath.BOUND_EXECUTION_RECEIPT),
        (MaturityStage.S5_FROZEN_DOMAIN, AuthorityPath.CORPUS_WITNESS),
    )
    for gate, path in chain:
        ledger.consider(_evidence("A0.SOUND", gate, path, experiment=gate.value))
    row = measure_leaves(_UNIVERSE, ledger)["A0.SOUND"]
    assert row.attained_stage is MaturityStage.S5_FROZEN_DOMAIN
    assert row.has_no_jump
    assert row.is_ready


# ------------------------------------------------------------- authority of evidence


def test_evidence_paths_are_not_reduced_to_execution_receipts() -> None:
    """للقياس والبرهان والمدوَّنة سلطاتُها؛ لا تُحال قسرًا إلى إيصال تنفيذ."""

    for path in (
        AuthorityPath.MEASUREMENT_RUN_MANIFEST,
        AuthorityPath.FROZEN_FORMAL_PROOF,
        AuthorityPath.CORPUS_WITNESS,
        AuthorityPath.PREREGISTERED_MEASUREMENT,
    ):
        assert licensable_gates(path)


def test_an_in_process_replay_can_never_license_blind_or_transfer() -> None:
    """الاستدعاءُ المباشر لا يمنح `BLIND` ولا `TRANSFER` ولا `GOLD`."""

    licensed = licensable_gates(AuthorityPath.IN_PROCESS_MEASUREMENT_REPLAY)
    assert MaturityStage.S7_BLIND_VERIFIED not in licensed
    assert MaturityStage.S8_TRANSFER_VERIFIED not in licensed
    assert MaturityStage.S6_GOLD_EVALUATED not in licensed
    assert MaturityStage.S9_REPRODUCED not in licensed


def test_an_unauthorized_upgrade_is_refused_and_recorded() -> None:
    """الترقيةُ بلا إذنٍ تُردّ وتُسجَّل بجنسها، فتدخل مؤشّرَ الحوكمة."""

    ledger = _seeded_ledger()
    outcome = ledger.consider(
        _evidence(
            "A0.SOUND",
            MaturityStage.S7_BLIND_VERIFIED,
            AuthorityPath.IN_PROCESS_MEASUREMENT_REPLAY,
        )
    )
    assert isinstance(outcome, EvidenceRefusal)
    assert outcome.refusal_code is RefusalCode.UNAUTHORIZED_UPGRADE
    certificate = derive_arabic_state_certificate(_UNIVERSE, ledger)
    assert certificate.governance.unauthorized_upgrade_rate.numerator == 1
    assert not certificate.governance.zero_targets_are_met


def test_evidence_requires_an_authority_path_object() -> None:
    """شاهدٌ بمسارٍ نصّيٍّ غيرِ مُنمَّط يُرفَض عند البناء."""

    with pytest.raises(EvidenceError):
        ScopedCapabilityEvidence(
            capability_id="A0.SOUND",
            attested_gate=MaturityStage.S3_EXECUTABLE,
            authority_path="BOUND_EXECUTION_RECEIPT",  # type: ignore[arg-type]
            scope=_scope(),
            authority_reference="artifact",
            experiment_content_digest=_digest("e"),
            protocol_digest=_digest("p"),
        )


def test_absence_cannot_be_attested_as_evidence() -> None:
    """الغيابُ يُقاس بانتفاء الشاهد، ولا يُشهَد عليه بشاهد."""

    with pytest.raises(EvidenceError):
        _evidence("A0.SOUND", MaturityStage.S0_ABSENT, AuthorityPath.DECLARATION_RECORD)


def test_a_repeated_reference_is_one_evidence() -> None:
    """الإحالةُ المكرَّرة على المفتاح نفسِه شاهدٌ واحد لا شاهدان."""

    ledger = _seeded_ledger()
    first = _evidence(
        "A0.SOUND", MaturityStage.S2_MODELED, AuthorityPath.FROZEN_FORMAL_PROOF
    )
    admitted = ledger.consider(first)
    repeated = ledger.consider(first)
    assert admitted is first
    assert isinstance(repeated, EvidenceRefusal)
    assert repeated.refusal_code is RefusalCode.REPEATED_REFERENCE
    assert len(ledger.for_capability("A0.SOUND")) == 2


def test_evidence_for_an_undeclared_capability_is_refused() -> None:
    """شاهدٌ لقدرةٍ خارج المقام يُردّ؛ فالبسطُ لا يوسّع مقامَه."""

    ledger = _seeded_ledger()
    outcome = ledger.consider(
        _evidence(
            "A99.INVENTED", MaturityStage.S2_MODELED, AuthorityPath.FROZEN_FORMAL_PROOF
        )
    )
    assert isinstance(outcome, EvidenceRefusal)
    assert outcome.refusal_code is RefusalCode.UNKNOWN_CAPABILITY


def test_undisclosed_residuals_are_refused_and_counted() -> None:
    """السكوتُ عن البواقي ليس إفصاحًا بالصفر؛ يُردّ ويُعَدّ."""

    ledger = _seeded_ledger()
    outcome = ledger.consider(
        ScopedCapabilityEvidence(
            capability_id="A0.SOUND",
            attested_gate=MaturityStage.S2_MODELED,
            authority_path=AuthorityPath.FROZEN_FORMAL_PROOF,
            scope=_scope(),
            authority_reference="artifact",
            experiment_content_digest=_digest("e"),
            protocol_digest=_digest("p"),
            residual_disclosure=ResidualDisclosure.UNDISCLOSED,
        )
    )
    assert isinstance(outcome, EvidenceRefusal)
    assert outcome.refusal_code is RefusalCode.UNDISCLOSED_RESIDUALS
    certificate = derive_arabic_state_certificate(_UNIVERSE, ledger)
    assert certificate.governance.undisclosed_residual_rate.numerator == 1


# ------------------------------------------------------- the metric may go down


def test_negative_evidence_lowers_the_attained_stage() -> None:
    """الشاهدُ الناقضُ يُبطِل بوّابتَه ولا يُحذَف؛ فالمقياسُ ينزل."""

    ledger = _seeded_ledger()
    ledger.consider(
        _evidence(
            "A0.SOUND", MaturityStage.S2_MODELED, AuthorityPath.FROZEN_FORMAL_PROOF
        )
    )
    before = measure_leaves(_UNIVERSE, ledger)["A0.SOUND"]
    assert before.attained_stage is MaturityStage.S2_MODELED

    ledger.consider(
        _evidence(
            "A0.SOUND",
            MaturityStage.S2_MODELED,
            AuthorityPath.FROZEN_FORMAL_PROOF,
            experiment="contradiction",
            polarity=EvidencePolarity.NEGATIVE,
        )
    )
    after = measure_leaves(_UNIVERSE, ledger)["A0.SOUND"]
    assert after.attained_stage is MaturityStage.S1_DECLARED
    assert after.contested_gates == (MaturityStage.S2_MODELED,)


# ----------------------------------------------------------- coverage vs readiness


def test_coverage_and_readiness_are_separate_numbers() -> None:
    """التغطيةُ ليست الأهليّة؛ رقمان مستقلّان لا يُدمَجان."""

    certificate = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger())
    assert certificate.coverage["DeclaredCoverage"].value == 1.0
    assert certificate.readiness.value == 0.0
    assert "Breadth != Readiness" in (
        certificate.rows[ARABIC_TOTAL_ID].aggregate.breadth_law
    )


def test_a_parent_is_capped_by_its_weakest_required_child() -> None:
    """الأبُ لا يتجاوز أضعفَ أبنائه المُلزِمين في الأهليّة."""

    ledger = _seeded_ledger()
    for gate, path in (
        (MaturityStage.S2_MODELED, AuthorityPath.FROZEN_FORMAL_PROOF),
        (MaturityStage.S3_EXECUTABLE, AuthorityPath.BOUND_EXECUTION_RECEIPT),
        (MaturityStage.S4_TESTED, AuthorityPath.BOUND_EXECUTION_RECEIPT),
        (MaturityStage.S5_FROZEN_DOMAIN, AuthorityPath.CORPUS_WITNESS),
    ):
        ledger.consider(_evidence("A0.SOUND", gate, path, experiment=gate.value))
    certificate = derive_arabic_state_certificate(_UNIVERSE, ledger)
    domain = certificate.rows["A0"].aggregate
    assert domain.own_readiness.numerator == 1
    assert domain.readiness.value == 0.0
    assert certificate.readiness.value == 0.0


def test_blind_and_transfer_are_never_merged_into_one_ratio() -> None:
    """`Blind` و`Transfer` رقمان مستقلّان؛ دمجُهما يُخفي الفرقَ المقصود."""

    certificate = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger())
    assert "BlindVerifiedCoverage" in certificate.coverage
    assert "TransferVerifiedCoverage" in certificate.coverage
    assert (
        certificate.coverage["BlindVerifiedCoverage"]
        is not certificate.coverage["TransferVerifiedCoverage"]
    )
    assert len(certificate.coverage) == 9


# --------------------------------------------------------------------- ratios


def test_a_ratio_carries_its_denominator_and_its_source() -> None:
    """لا نسبةَ مجرّدةً عن مقامها ومصدرِ تجميده."""

    certificate = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger())
    ratio = certificate.coverage["GoldCoverage"]
    assert ratio.denominator == _UNIVERSE.manifest.leaf_count
    assert ratio.denominator_source == UNIVERSE_V1_ID
    assert "ARatioCarriesItsDenominator" in ratio.reading_law


def test_a_zero_denominator_ratio_is_undefined_not_zero() -> None:
    """نسبةٌ مقامُها صفرٌ غيرُ معرَّفة؛ لا صفرٌ ولا تمام."""

    assert DerivedRatio(0, 0, "empty").value is None


def test_a_numerator_cannot_exceed_its_denominator() -> None:
    """بسطٌ فوق مقامه رفضٌ بنيويّ لا تقريبٌ إلى الواحد."""

    with pytest.raises(AggregationError):
        DerivedRatio(2, 1, "source")


# ----------------------------------------------------------------- the certificate


def test_the_certificate_answers_every_gate_for_every_node() -> None:
    """الشهادةُ تجيب عن كلّ بوّابةٍ لكلّ عقدةٍ في المقام."""

    certificate = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger())
    assert set(certificate.rows) == set(_UNIVERSE.node_ids())
    answers = certificate.rows["A14.EVENT_REFERENCE_TIME_RELATION"].gate_answers
    assert answers["S1_DECLARED"] is True
    assert answers["S3_EXECUTABLE"] is False
    assert answers["S7_BLIND_VERIFIED"] is False


def test_the_certificate_names_the_next_gate_by_what_it_unblocks() -> None:
    """البوّابةُ التالية أكثرُ المُعوِّقات حجبًا، لا أحدثُها ولا أقربُها."""

    certificate = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger())
    assert certificate.next_gate == "MODEL_ABSENT"
    assert certificate.blockers[0].blocked_leaf_count == (_UNIVERSE.manifest.leaf_count)


def test_the_certificate_carries_its_laws_and_is_reproducible() -> None:
    """الشهادةُ تحمل قوانينَها، ومُلخَّصُها مستقرٌّ عند إعادة الاشتقاق."""

    first = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger())
    second = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger())
    assert first.certificate_digest == second.certificate_digest
    assert first.laws == CAPABILITY_LAWS
    assert first.universe_manifest.content_digest == _UNIVERSE.manifest.content_digest


def test_the_certificate_holds_no_hand_entered_field() -> None:
    """ليس في الشهادة حقلٌ يُملأ يدويًّا؛ كلُّ رقمٍ له طريقُ اشتقاق."""

    content = derive_arabic_state_certificate(
        _UNIVERSE, _seeded_ledger()
    ).as_canonical_content()
    assert set(content) == {
        "universe_manifest",
        "coverage",
        "readiness",
        "certified_completion",
        "arabic_total_coverage",
        "governance",
        "blockers",
        "next_gate",
        "rows",
        "laws",
    }


def test_governance_names_its_three_zero_targets() -> None:
    """ثلاثةُ مؤشّراتٍ هدفُها صفرٌ صريحٌ لا «قليل»."""

    governance = derive_arabic_state_certificate(_UNIVERSE, _seeded_ledger()).governance
    assert governance.zero_target_indicators == (
        "ForbiddenJumpRate",
        "UnauthorizedUpgradeRate",
        "UndisclosedResidualRate",
    )
    assert governance.zero_targets_are_met


def test_identity_loss_lowers_the_identity_preservation_rate() -> None:
    """ضياعُ الهويّة في شاهدٍ يُخفِض مؤشّرَ حفظها، ولا يُبتلَع."""

    ledger = _seeded_ledger()
    ledger.consider(
        _evidence(
            "A0.SOUND",
            MaturityStage.S2_MODELED,
            AuthorityPath.FROZEN_FORMAL_PROOF,
            identity_preserved=False,
        )
    )
    governance = derive_arabic_state_certificate(_UNIVERSE, ledger).governance
    assert governance.identity_preservation_rate.numerator == (
        governance.identity_preservation_rate.denominator - 1
    )


def test_aggregation_refuses_a_partially_measured_denominator() -> None:
    """لا تُجمَّع شجرةٌ بعضُ أوراقها غيرُ مقيس؛ الغيابُ يُقاس لا يُسقَط."""

    from alghanem.capability import aggregate_universe

    measurements = measure_leaves(_UNIVERSE, _seeded_ledger())
    del measurements["A0.SOUND"]
    with pytest.raises(AggregationError):
        aggregate_universe(_UNIVERSE, measurements)
