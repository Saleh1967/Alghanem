"""اختباراتُ `G0.EVAL-0`: الالتزامُ، والهويّةُ، والحدُّ، والتشغيلُ، والفتحُ المشروط."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from alghanem.arabic.fiber_contracts import (
    MADLUL_CONTRACT_INTERFACE_VERSION,
    build_madlul_fiber_contract,
    commit_madlul_gold,
    madlul_member_id,
)
from alghanem.arabic.madlul_alone_formal import (
    ATTESTED_SIGNIFIED_WITNESSES,
    MadlulSection,
)
from alghanem.evaluation import (
    EVALUATION_LAWS,
    NO_EVALUATION_VERDICT_BEFORE,
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    BoundEvaluationRequest,
    BoundExecutionReceipt,
    EvaluationBinding,
    EvaluationError,
    EvaluationProtocolKind,
    FrozenEvaluationProtocol,
    FrozenRunReport,
    FrozenSystemIdentity,
    GoldRevealAuthority,
    GoldRevealRecord,
    ProcessConfinementDeclaration,
    ProcessConfinementStanding,
    ResidualCode,
    RunLedger,
    RunResidual,
    evaluation_import_isolation_audit,
    freeze_system_identity,
    reader_import_audit,
    report_from_receipt,
)
from alghanem.evaluation_execution import ExecutionAuthority, ReaderExecutionRequest
from alghanem.prior_fiber import SuccessCriterion, fiber_import_isolation_audit

_READERS = Path(__file__).resolve().parent / "readers"

_NONCE = bytes(range(32))

_GOLD = {
    madlul_member_id(witness): witness.attested_section.value
    for witness in ATTESTED_SIGNIFIED_WITNESSES
}


def _contract():  # type: ignore[no-untyped-def]
    return build_madlul_fiber_contract(commit_madlul_gold(_NONCE))


def _protocol(
    kind: EvaluationProtocolKind = EvaluationProtocolKind.FORMAL_CLASSIFICATION,
) -> FrozenEvaluationProtocol:
    return FrozenEvaluationProtocol(
        protocol_id="protocol.madlul.g0_eval_0",
        kind=kind,
        success_criteria=tuple(SuccessCriterion),
        residual_policy_ref="residual.declared",
        payload_scheme="scheme.blind.bytes",
        contract_interface_version=MADLUL_CONTRACT_INTERFACE_VERSION,
    )


def _identity(
    name: str, *, configuration: dict[str, str] | None = None
) -> FrozenSystemIdentity:
    files = (_READERS / name,)
    return freeze_system_identity(
        implementation_files=files,
        configuration=configuration or {"mode": name},
        boundary_report=reader_import_audit(files),
        contract_interface_version=MADLUL_CONTRACT_INTERFACE_VERSION,
    )


def _binding(
    names: tuple[str, ...] = ("reader_one.py", "reader_two.py"),
) -> EvaluationBinding:
    return EvaluationBinding(
        contract=_contract(),
        protocol=_protocol(),
        reader_identities=tuple(_identity(name) for name in names),
    )


_RECEIPTS: dict[tuple[str, str], BoundExecutionReceipt] = {}


def _reader_name(identity: FrozenSystemIdentity) -> str:
    return identity.implementation_files[0].rsplit("/", 1)[-1]


def _receipt(
    binding: EvaluationBinding, identity: FrozenSystemIdentity
) -> BoundExecutionReceipt:
    """شغِّل بايتاتِ القارئ المُجمَّدةَ فعلًا؛ ولا تقريرَ إلّا من إيصال سلطته."""

    key = (binding.payload.payload_digest, identity.content_id)
    receipt = _RECEIPTS.get(key)
    if receipt is None:
        name = _reader_name(identity)
        path = _READERS / name
        receipt = ExecutionAuthority(binding).execute(
            ReaderExecutionRequest(
                identity=identity,
                implementation_files=(path,),
                entry_file=path,
                configuration={"mode": name},
            )
        )
        _RECEIPTS[key] = receipt
    return receipt


def _report(
    binding: EvaluationBinding,
    identity: FrozenSystemIdentity,
    *,
    run_ordinal: int = 1,
) -> FrozenRunReport:
    return report_from_receipt(_receipt(binding, identity), run_ordinal=run_ordinal)


def _complete_ledger() -> tuple[RunLedger, EvaluationBinding]:
    binding = _binding()
    ledger = RunLedger(binding)
    for identity in binding.reader_identities:
        ledger.record(_report(binding, identity))
    return ledger, binding


def test_the_commitment_moves_with_the_nonce_and_keeps_it_out_of_its_fields() -> None:
    first = commit_madlul_gold(_NONCE)
    second = commit_madlul_gold(bytes(range(1, 33)))

    assert first.commitment_digest != second.commitment_digest
    assert first.withholds_its_nonce
    assert "nonce" not in tuple(type(first).__dataclass_fields__)


def test_the_commitment_opens_only_with_its_own_gold_and_its_own_nonce() -> None:
    contract = _contract()
    body_digest = contract.contract_body_digest

    assert contract.gold_commitment.opens_with(
        _GOLD, nonce=_NONCE, contract_body_digest=body_digest
    )
    assert not contract.gold_commitment.opens_with(
        _GOLD, nonce=bytes(range(1, 33)), contract_body_digest=body_digest
    )
    wrong = dict(_GOLD)
    wrong[next(iter(wrong))] = "قسمٌ آخر"
    assert not contract.gold_commitment.opens_with(
        wrong, nonce=_NONCE, contract_body_digest=body_digest
    )


def test_the_hiding_claim_is_declared_as_binding_not_as_secrecy() -> None:
    ceiling = _contract().gold_commitment.hiding_claim_ceiling

    assert "DigestOnly" in ceiling or "التزام" in ceiling


def test_the_protocol_kind_enters_its_digest() -> None:
    formal = _protocol(EvaluationProtocolKind.FORMAL_CLASSIFICATION)
    discovery = _protocol(EvaluationProtocolKind.RULE_DISCOVERY)

    assert formal.protocol_digest != discovery.protocol_digest
    assert formal.kind.declares_the_admissible_rules
    assert not discovery.kind.declares_the_admissible_rules


def test_one_changed_source_byte_changes_the_reader_identity(tmp_path: Path) -> None:
    source = (_READERS / "reader_one.py").read_bytes()
    first_file = tmp_path / "reader_a.py"
    first_file.write_bytes(source)
    second_dir = tmp_path / "other"
    second_dir.mkdir()
    second_file = second_dir / "reader_a.py"
    second_file.write_bytes(source + b"\n")

    def freeze(path: Path) -> FrozenSystemIdentity:
        return freeze_system_identity(
            implementation_files=(path,),
            configuration={"mode": "declared"},
            boundary_report=reader_import_audit((path,)),
            contract_interface_version=MADLUL_CONTRACT_INTERFACE_VERSION,
        )

    assert freeze(first_file).content_id != freeze(second_file).content_id


def test_the_identity_carries_no_system_name_and_moves_with_configuration() -> None:
    identity = _identity("reader_one.py")
    other = _identity("reader_one.py", configuration={"mode": "other"})

    assert identity.carries_no_system_name
    assert identity.content_id != other.content_id
    assert set(identity.as_identity_content()) == {
        "implementation_digest",
        "configuration_digest",
        "dependency_boundary_digest",
        "contract_interface_version",
    }


def test_a_reader_that_reaches_the_answer_material_is_not_frozen() -> None:
    with pytest.raises(EvaluationError, match="خرق حدَّ مصدره"):
        _identity("reader_leaky.py")


def test_a_reader_that_opens_a_dynamic_path_is_not_frozen() -> None:
    with pytest.raises(EvaluationError, match="خرق حدَّ مصدره"):
        _identity("reader_dynamic.py")


def test_the_static_audit_does_not_claim_process_isolation() -> None:
    declaration = ProcessConfinementDeclaration()

    assert not declaration.is_proven
    assert declaration.standing is ProcessConfinementStanding.DECLARED_DEFERRED
    assert declaration.ceiling == STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION
    assert STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION in EVALUATION_LAWS


def test_the_payload_is_bytes_and_withholds_every_attested_section() -> None:
    payload = _binding().payload

    assert type(payload.payload_bytes) is bytes
    for section in MadlulSection:
        assert payload.withholds(section.value)
    decoded = json.loads(payload.payload_bytes.decode("utf-8"))
    assert "gold_commitment" not in decoded
    assert "authored_by" not in decoded
    assert "trace" not in decoded


def test_the_bound_request_binds_the_four_digests() -> None:
    binding = _binding()
    identity = binding.reader_identities[0]
    request = binding.request_for(identity)

    assert request.system_content_id == identity.content_id
    assert request.contract_digest == binding.contract.contract_digest
    assert request.domain_digest == binding.contract.domain_digest
    assert request.evaluation_protocol_digest == binding.protocol.protocol_digest
    assert len({request.request_id for request in binding.requests}) == 2


def test_a_reader_outside_the_binding_gets_no_request() -> None:
    binding = _binding()

    with pytest.raises(EvaluationError, match="خارج الربط"):
        binding.request_for(_identity("reader_one.py", configuration={"mode": "x"}))


def test_a_report_bound_to_another_payload_is_refused() -> None:
    binding = _binding()
    elsewhere = EvaluationBinding(
        contract=build_madlul_fiber_contract(commit_madlul_gold(bytes(range(1, 33)))),
        protocol=_protocol(),
        reader_identities=binding.reader_identities,
    )
    ledger = RunLedger(binding)
    stray = _report(elsewhere, elsewhere.reader_identities[0])

    with pytest.raises(EvaluationError, match="خارج هذا الربط"):
        ledger.record(stray)


def test_no_report_is_written_beside_a_bound_execution() -> None:
    binding = _binding()
    receipt = _receipt(binding, binding.reader_identities[0])

    with pytest.raises(TypeError):
        FrozenRunReport(  # type: ignore[call-arg]
            request_id=receipt.request_id,
            system_content_id=receipt.system_content_id,
            payload_digest=receipt.payload_digest,
            outputs=receipt.outputs,
            residuals=receipt.residuals,
            trace=receipt.trace,
            run_ordinal=1,
        )


def test_the_first_run_is_the_reference_and_an_identical_repeat_is_a_witness() -> None:
    binding = _binding()
    ledger = RunLedger(binding)
    identity = binding.reader_identities[0]
    first = ledger.record(_report(binding, identity))
    repeat = ledger.record(_report(binding, identity, run_ordinal=2))

    assert first.is_a_first_run
    assert repeat is first
    assert len(ledger.repeat_reports) == 1
    assert not ledger.violations


def test_a_differing_repeat_under_the_same_identity_is_refused_and_recorded() -> None:
    binding = _binding(("reader_nondeterministic.py", "reader_two.py"))
    ledger = RunLedger(binding)
    identity = binding.reader_identities[0]
    authority = ExecutionAuthority(binding)
    path = _READERS / "reader_nondeterministic.py"

    def run(ordinal: int) -> FrozenRunReport:
        receipt = authority.execute(
            ReaderExecutionRequest(
                identity=identity,
                implementation_files=(path,),
                entry_file=path,
                configuration={"mode": "reader_nondeterministic.py"},
            )
        )
        return report_from_receipt(receipt, run_ordinal=ordinal)

    ledger.record(run(1))
    with pytest.raises(EvaluationError, match="AFirstRunHappensOnce|إعادةُ تشغيل"):
        ledger.record(run(2))

    assert ledger.violations


def test_a_second_claim_of_being_the_first_run_is_refused_and_recorded() -> None:
    binding = _binding()
    ledger = RunLedger(binding)
    identity = binding.reader_identities[0]
    ledger.record(_report(binding, identity))

    with pytest.raises(EvaluationError):
        ledger.record(_report(binding, identity))

    assert ledger.violations


def test_no_reveal_before_a_first_report_for_every_reader() -> None:
    binding = _binding()
    ledger = RunLedger(binding)
    ledger.record(_report(binding, binding.reader_identities[0]))
    authority = GoldRevealAuthority(ledger)

    assert not authority.may_reveal
    assert ledger.missing_system_content_ids
    with pytest.raises(EvaluationError, match="NoEvaluationVerdictBefore"):
        authority.reveal(_GOLD, nonce=_NONCE)


def test_the_reveal_refuses_a_gold_or_a_nonce_that_does_not_open_it() -> None:
    ledger, _ = _complete_ledger()
    authority = GoldRevealAuthority(ledger)

    with pytest.raises(EvaluationError, match="لا يفتحان الالتزام"):
        authority.reveal(_GOLD, nonce=bytes(range(1, 33)))
    wrong = dict(_GOLD)
    wrong[next(iter(wrong))] = "قسمٌ آخر"
    with pytest.raises(EvaluationError, match="لا يفتحان الالتزام"):
        authority.reveal(wrong, nonce=_NONCE)


def test_a_valid_reveal_issues_a_record_that_carries_no_gold_and_no_nonce() -> None:
    ledger, binding = _complete_ledger()
    record = GoldRevealAuthority(ledger).reveal(_GOLD, nonce=_NONCE)

    assert isinstance(record, GoldRevealRecord)
    assert record.withholds_gold_and_nonce
    assert record.is_not_a_verdict
    assert record.contract_digest == binding.contract.contract_digest
    assert len(record.first_report_digests) == 2
    content = json.dumps(record.as_canonical_content(), ensure_ascii=False)
    for label in _GOLD.values():
        assert label not in content
    assert NO_EVALUATION_VERDICT_BEFORE in record.verdict_law


def test_a_residual_is_named_and_covers_its_member_without_blocking_the_reveal() -> (
    None
):
    binding = _binding(("reader_residual.py", "reader_two.py"))
    ledger = RunLedger(binding)
    left, right = binding.reader_identities
    ledger.record(_report(binding, left))
    ledger.record(_report(binding, right))
    record = GoldRevealAuthority(ledger).reveal(_GOLD, nonce=_NONCE)

    assert ledger.blocking_residuals
    assert ledger.blocking_residuals[0].residual_code is (
        ResidualCode.UNCLASSIFIED_BY_READER
    )
    assert ledger.blocking_residuals[0].residual_digest
    assert isinstance(record, GoldRevealRecord)


def test_a_residual_refuses_a_free_string_and_an_empty_reason_or_evidence() -> None:
    binding = _binding()
    member = binding.contract.body.member_ids[0]
    with pytest.raises(EvaluationError, match="سببُ البقيّة"):
        RunResidual(
            member_id=member,
            residual_code=ResidualCode.REFUSED_BY_READER,
            blocking=False,
            reason="   ",
            evidence_ref="stdout:residuals[0]",
        )
    with pytest.raises(EvaluationError, match="إحالةُ شاهد"):
        RunResidual(
            member_id=member,
            residual_code=ResidualCode.REFUSED_BY_READER,
            blocking=False,
            reason="رفضه القارئ",
            evidence_ref="",
        )
    with pytest.raises(EvaluationError, match="مفردته المغلقة"):
        RunResidual(
            member_id=member,
            residual_code="unclassified_by_reader",  # type: ignore[arg-type]
            blocking=False,
            reason="رفضه القارئ",
            evidence_ref="stdout:residuals[0]",
        )


def test_no_verdict_or_dominance_function_is_exported_in_this_phase() -> None:
    import alghanem.evaluation as evaluation

    exported = set(evaluation.__all__)
    callables = {name for name in exported if not name.isupper()}
    for forbidden in ("verdict", "dominance", "compare", "winner", "rank"):
        assert not any(forbidden in name.lower() for name in callables)
    assert not hasattr(evaluation, "compare_run_reports")


def test_the_prior_fiber_layer_does_not_reach_the_evaluation_layer() -> None:
    report = fiber_import_isolation_audit()

    assert report.is_isolated, report.violations
    assert not any("evaluation" in reached for reached in report.alghanem_imports)


def test_the_evaluation_layer_reaches_no_domain_or_kernel_material() -> None:
    report = evaluation_import_isolation_audit()

    assert report.is_isolated, report.violations
    assert not report.dynamic_accesses
    for reached in report.reached_modules:
        head = reached.split(".")[1]
        assert head in {
            "canonical_content",
            "evaluation",
            "import_boundary",
            "prior",
            "prior_fiber",
        }


def test_the_request_refuses_a_digest_that_is_not_a_canonical_digest() -> None:
    with pytest.raises(EvaluationError, match="بصمةٌ قانونيّة"):
        BoundEvaluationRequest(
            system_content_id="ليس بصمة",
            contract_digest="a" * 64,
            domain_digest="b" * 64,
            evaluation_protocol_digest="c" * 64,
        )
