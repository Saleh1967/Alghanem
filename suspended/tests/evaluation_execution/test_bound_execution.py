"""اختباراتُ `G0.EXEC-0`: لا تقريرَ تشغيلٍ بلا تنفيذٍ مربوطٍ تُصدِر إيصالَه سلطتُه."""

from __future__ import annotations

import shutil
from collections.abc import Mapping
from pathlib import Path

import pytest

from alghanem.arabic.fiber_contracts import (
    MADLUL_CONTRACT_INTERFACE_VERSION,
    build_madlul_fiber_contract,
    commit_madlul_gold,
    madlul_member_id,
)
from alghanem.arabic.madlul_alone_formal import ATTESTED_SIGNIFIED_WITNESSES
from alghanem.evaluation import (
    AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE,
    BoundExecutionReceipt,
    EvaluationBinding,
    EvaluationError,
    EvaluationProtocolKind,
    ExecutionExitStatus,
    ExecutionMode,
    FrozenEvaluationProtocol,
    FrozenRunReport,
    FrozenSystemIdentity,
    GoldRevealAuthority,
    ReceiptIssuanceKey,
    ResidualCode,
    RunLedger,
    evaluation_import_isolation_audit,
    freeze_system_identity,
    reader_import_audit,
    report_from_receipt,
    verify_receipt_issuance,
)
from alghanem.evaluation_execution import (
    A_TIMEOUT_IS_NAMED_NOT_FOLDED_INTO_A_NONZERO_EXIT,
    A_WIRE_VALUE_IS_REFUSED_NOT_COERCED,
    CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED,
    EXECUTION_LAWS,
    NO_COMPARISON_BEFORE_BOUND_EXECUTION,
    RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED,
    SEPARATE_PROCESS_IS_NOT_A_SANDBOX,
    ExecutionAuthority,
    ExecutionError,
    ReaderExecutionRequest,
    SeparateProcessOutcome,
    execution_import_isolation_audit,
)
from alghanem.prior_fiber import SuccessCriterion

_READERS = Path(__file__).resolve().parents[1] / "evaluation" / "readers"

_NONCE = bytes(range(32))

_GOLD = {
    madlul_member_id(witness): witness.attested_section.value
    for witness in ATTESTED_SIGNIFIED_WITNESSES
}


def _protocol() -> FrozenEvaluationProtocol:
    return FrozenEvaluationProtocol(
        protocol_id="protocol.madlul.g0_exec_0",
        kind=EvaluationProtocolKind.FORMAL_CLASSIFICATION,
        success_criteria=tuple(SuccessCriterion),
        residual_policy_ref="residual.declared",
        payload_scheme="scheme.blind.bytes",
        contract_interface_version=MADLUL_CONTRACT_INTERFACE_VERSION,
    )


def _identity(path: Path, configuration: Mapping[str, str]) -> FrozenSystemIdentity:
    return freeze_system_identity(
        implementation_files=(path,),
        configuration=configuration,
        boundary_report=reader_import_audit((path,)),
        contract_interface_version=MADLUL_CONTRACT_INTERFACE_VERSION,
    )


_COMPANION = "reader_two.py"


def _bound(
    identities: tuple[FrozenSystemIdentity, ...], *, nonce: bytes = _NONCE
) -> EvaluationBinding:
    """الامتحانُ يُقرَأ بنظامين فأكثر، فيُضَمُّ قارئٌ ثانٍ إلى محلِّ الاختبار."""

    if len(identities) >= 2:
        return EvaluationBinding(
            contract=build_madlul_fiber_contract(commit_madlul_gold(nonce)),
            protocol=_protocol(),
            reader_identities=identities,
        )
    companion = _identity(_READERS / _COMPANION, {"mode": _COMPANION})
    if all(other.content_id != companion.content_id for other in identities):
        identities = (*identities, companion)
    else:
        first = _identity(_READERS / "reader_one.py", {"mode": "reader_one.py"})
        identities = (*identities, first)
    return EvaluationBinding(
        contract=build_madlul_fiber_contract(commit_madlul_gold(nonce)),
        protocol=_protocol(),
        reader_identities=identities,
    )


def _binding(names: tuple[str, ...], *, nonce: bytes = _NONCE) -> EvaluationBinding:
    return _bound(
        tuple(_identity(_READERS / name, {"mode": name}) for name in names),
        nonce=nonce,
    )


def _request(path: Path) -> ReaderExecutionRequest:
    configuration = {"mode": path.name}
    return ReaderExecutionRequest(
        identity=_identity(path, configuration),
        implementation_files=(path,),
        entry_file=path,
        configuration=configuration,
    )


def _run(name: str, *, nonce: bytes = _NONCE) -> BoundExecutionReceipt:
    binding = _binding((name,), nonce=nonce)
    authority = ExecutionAuthority(binding)
    return authority.execute(_request(_READERS / name))


def _configured_request(
    name: str, configuration: Mapping[str, str]
) -> tuple[ExecutionAuthority, ReaderExecutionRequest]:
    """سلطةٌ وطلبٌ بإعدادٍ مُعلَنٍ غيرِ اسمِ الملفّ، ليُقاس بلوغُ الإعداد للقارئ."""

    path = _READERS / name
    identity = _identity(path, configuration)
    binding = _bound((identity,))
    return ExecutionAuthority(binding), ReaderExecutionRequest(
        identity=identity,
        implementation_files=(path,),
        entry_file=path,
        configuration=configuration,
    )


def test_the_frozen_bytes_are_executed_and_their_outputs_are_receipted() -> None:
    receipt = _run("reader_one.py")
    assert receipt.exit_status is ExecutionExitStatus.COMPLETED
    assert receipt.execution_mode is ExecutionMode.SEPARATE_PROCESS
    assert len(receipt.outputs) == len(_GOLD)
    assert receipt.residuals == ()
    assert receipt.receipt_digest != receipt.output_digest


def test_the_receipt_carries_the_identity_it_remeasured_at_execution_time() -> None:
    binding = _binding(("reader_one.py",))
    receipt = ExecutionAuthority(binding).execute(_request(_READERS / "reader_one.py"))
    identity = binding.reader_identities[0]
    assert receipt.system_content_id == identity.content_id
    assert receipt.implementation_digest == identity.implementation_digest
    assert receipt.configuration_digest == identity.configuration_digest
    assert receipt.dependency_boundary_digest == identity.dependency_boundary_digest
    assert receipt.request_id == binding.request_for(identity).request_id
    assert receipt.payload_digest == binding.payload.payload_digest


def test_one_changed_source_byte_after_the_freeze_refuses_the_execution(
    tmp_path: Path,
) -> None:
    path = tmp_path / "reader_one.py"
    shutil.copyfile(_READERS / "reader_one.py", path)
    configuration = {"mode": "reader_one.py"}
    identity = _identity(path, configuration)
    binding = _bound((identity,))
    path.write_bytes(path.read_bytes() + b"\n")
    receipt = ExecutionAuthority(binding).execute(
        ReaderExecutionRequest(
            identity=identity,
            implementation_files=(path,),
            entry_file=path,
            configuration=configuration,
        )
    )
    assert receipt.exit_status is ExecutionExitStatus.IDENTITY_MISMATCH
    assert receipt.outputs == ()
    with pytest.raises(EvaluationError):
        report_from_receipt(receipt, run_ordinal=1)


def test_a_configuration_that_departs_from_the_frozen_one_is_refused(
    tmp_path: Path,
) -> None:
    path = _READERS / "reader_one.py"
    identity = _identity(path, {"mode": "reader_one.py"})
    binding = _bound((identity,))
    receipt = ExecutionAuthority(binding).execute(
        ReaderExecutionRequest(
            identity=identity,
            implementation_files=(path,),
            entry_file=path,
            configuration={"mode": "إعدادٌ آخر"},
        )
    )
    assert receipt.exit_status is ExecutionExitStatus.IDENTITY_MISMATCH


def test_a_reader_that_breaks_its_declared_boundary_is_refused_before_execution(
    tmp_path: Path,
) -> None:
    source = (_READERS / "reader_one.py").read_bytes()
    path = tmp_path / "reader_leaky_two.py"
    path.write_bytes(
        source.replace(
            b"import json",
            b"import json\nfrom alghanem.arabic.madlul_alone_formal import"
            b" MadlulSection",
        )
    )
    configuration = {"mode": path.name}
    identity = _identity(_READERS / "reader_one.py", {"mode": "reader_one.py"})
    binding = _bound((identity,))
    receipt = ExecutionAuthority(binding).execute(
        ReaderExecutionRequest(
            identity=identity,
            implementation_files=(path,),
            entry_file=path,
            configuration=configuration,
        )
    )
    assert receipt.exit_status is ExecutionExitStatus.BOUNDARY_VIOLATION
    assert receipt.outputs == ()


def test_the_output_digest_moves_with_the_bytes_that_actually_came_out() -> None:
    one = _run("reader_one.py")
    two = _run("reader_two.py")
    assert one.output_digest != two.output_digest
    assert one.output_digest == _run("reader_one.py").output_digest


def test_a_payload_from_another_binding_yields_another_receipt() -> None:
    here = _run("reader_one.py")
    elsewhere = _run("reader_one.py", nonce=bytes(range(1, 33)))
    assert here.payload_digest != elsewhere.payload_digest
    assert here.request_id != elsewhere.request_id
    assert here.receipt_digest != elsewhere.receipt_digest


def test_a_report_whose_receipt_is_bound_elsewhere_is_refused_by_the_ledger() -> None:
    binding = _binding(("reader_one.py", "reader_two.py"))
    ledger = RunLedger(binding)
    stray = _run("reader_one.py", nonce=bytes(range(1, 33)))
    with pytest.raises(EvaluationError):
        ledger.record(report_from_receipt(stray, run_ordinal=1))


def test_a_reader_that_raises_is_receipted_but_not_promoted_to_a_reference() -> None:
    receipt = _run("reader_raises.py")
    assert receipt.exit_status is ExecutionExitStatus.RAISED
    assert receipt.outputs == ()
    with pytest.raises(EvaluationError):
        report_from_receipt(receipt, run_ordinal=1)


def test_a_result_outside_the_closed_wire_shape_is_receipted_as_refused() -> None:
    receipt = _run("reader_bad_shape.py")
    assert receipt.exit_status is ExecutionExitStatus.REFUSED_OUTPUT_SHAPE


def test_a_member_outside_the_domain_is_receipted_as_an_unknown_member() -> None:
    receipt = _run("reader_unknown_member.py")
    assert receipt.exit_status is ExecutionExitStatus.REFUSED_UNKNOWN_MEMBER


def test_a_member_left_without_a_residual_is_refused_for_incomplete_coverage() -> None:
    receipt = _run("reader_partial.py")
    assert receipt.exit_status is ExecutionExitStatus.REFUSED_OUTPUT_SHAPE


def test_a_member_classified_and_left_as_a_residual_at_once_is_refused() -> None:
    receipt = _run("reader_overlap.py")
    assert receipt.exit_status is ExecutionExitStatus.REFUSED_OUTPUT_SHAPE


def test_a_residual_code_outside_the_closed_vocabulary_is_refused() -> None:
    receipt = _run("reader_untyped_residual.py")
    assert receipt.exit_status is ExecutionExitStatus.REFUSED_OUTPUT_SHAPE


def test_a_named_residual_crosses_the_wire_and_covers_its_member() -> None:
    receipt = _run("reader_residual.py")
    assert receipt.exit_status is ExecutionExitStatus.COMPLETED
    assert len(receipt.residuals) == 1
    residual = receipt.residuals[0]
    assert residual.residual_code is ResidualCode.UNCLASSIFIED_BY_READER
    assert residual.blocking is True
    assert len(receipt.outputs) + 1 == len(_GOLD)


def test_a_blocking_residual_is_recorded_and_does_not_block_the_reveal() -> None:
    binding = _binding(("reader_residual.py", "reader_two.py"))
    ledger = RunLedger(binding)
    for name in ("reader_residual.py", "reader_two.py"):
        authority = ExecutionAuthority(binding)
        receipt = authority.execute(_request(_READERS / name))
        assert receipt.exit_status is ExecutionExitStatus.COMPLETED
        ledger.record(report_from_receipt(receipt, run_ordinal=1))
    assert len(ledger.blocking_residuals) == 1
    record = GoldRevealAuthority(ledger).reveal(_GOLD, nonce=_NONCE)
    assert len(record.first_report_digests) == 2
    assert not hasattr(record, "verdict")
    assert not hasattr(record, "gold")
    assert not hasattr(record, "nonce")


def test_an_identical_repeat_is_a_determinism_witness_and_does_not_replace_it() -> None:
    binding = _binding(("reader_one.py",))
    authority = ExecutionAuthority(binding)
    ledger = RunLedger(binding)
    first = ledger.record(
        report_from_receipt(
            authority.execute(_request(_READERS / "reader_one.py")), run_ordinal=1
        )
    )
    witness = report_from_receipt(
        authority.execute(_request(_READERS / "reader_one.py")), run_ordinal=2
    )
    assert ledger.record(witness) is first
    assert first.is_a_first_run is True
    assert witness.is_a_first_run is False
    assert witness.run_content_digest == first.run_content_digest
    assert len(ledger.repeat_reports) == 1
    assert ledger.violations == ()


def test_a_differing_repeat_records_a_violation_and_blocks_the_reveal() -> None:
    binding = _binding(("reader_nondeterministic.py",))
    authority = ExecutionAuthority(binding)
    ledger = RunLedger(binding)
    ledger.record(
        report_from_receipt(
            authority.execute(_request(_READERS / "reader_nondeterministic.py")),
            run_ordinal=1,
        )
    )
    with pytest.raises(EvaluationError):
        ledger.record(
            report_from_receipt(
                authority.execute(_request(_READERS / "reader_nondeterministic.py")),
                run_ordinal=2,
            )
        )
    assert len(ledger.violations) == 1
    with pytest.raises(EvaluationError):
        GoldRevealAuthority(ledger).reveal(_GOLD, nonce=_NONCE)


def test_a_harness_cannot_forge_a_receipt_through_the_public_api() -> None:
    receipt = _run("reader_one.py")
    with pytest.raises(EvaluationError):
        BoundExecutionReceipt(
            seal=object(),
            execution_envelope_digest=receipt.execution_envelope_digest,
            issuer_key_id=receipt.issuer_key_id,
            issuance_signature=receipt.issuance_signature,
            system_content_id=receipt.system_content_id,
            request_id=receipt.request_id,
            implementation_digest=receipt.implementation_digest,
            configuration_digest=receipt.configuration_digest,
            dependency_boundary_digest=receipt.dependency_boundary_digest,
            payload_digest=receipt.payload_digest,
            execution_entrypoint_digest=receipt.execution_entrypoint_digest,
            output_digest=receipt.output_digest,
            trace_digest=receipt.trace_digest,
            exit_status=receipt.exit_status,
            execution_mode=receipt.execution_mode,
            outputs=receipt.outputs,
            residuals=receipt.residuals,
            trace=receipt.trace,
        )


def test_a_harness_cannot_write_a_reference_report_beside_the_receipt() -> None:
    receipt = _run("reader_one.py")
    with pytest.raises(EvaluationError):
        FrozenRunReport(
            seal=object(),
            execution_receipt=receipt,
            request_id=receipt.request_id,
            system_content_id=receipt.system_content_id,
            payload_digest=receipt.payload_digest,
            outputs=receipt.outputs,
            residuals=receipt.residuals,
            trace=receipt.trace,
            run_ordinal=1,
        )


def test_the_report_takes_every_field_from_its_receipt() -> None:
    receipt = _run("reader_one.py")
    report = report_from_receipt(receipt, run_ordinal=1)
    assert report.request_id == receipt.request_id
    assert report.system_content_id == receipt.system_content_id
    assert report.payload_digest == receipt.payload_digest
    assert report.outputs == receipt.outputs
    assert report.residuals == receipt.residuals
    assert report.trace == receipt.trace


def test_the_authority_owns_the_trace_that_the_receipt_digests() -> None:
    receipt = _run("reader_one.py")
    assert any(entry.startswith("identity.confirmed=") for entry in receipt.trace)
    assert any(entry.startswith("process.stdout_digest=") for entry in receipt.trace)
    assert any(
        entry.startswith("implementation.post_execution=") for entry in receipt.trace
    )


def test_the_execution_mechanism_is_declared_separate_and_not_proven_confinement() -> (
    None
):
    authority = ExecutionAuthority(_binding(("reader_one.py",)))
    assert authority.confinement.is_proven is False
    assert authority.confinement.ceiling == SEPARATE_PROCESS_IS_NOT_A_SANDBOX


def test_the_execution_package_declares_every_operational_access_it_takes() -> None:
    report = execution_import_isolation_audit()
    assert report.measured.violations == ()
    assert report.undeclared_accesses == ()
    assert report.unused_declarations == ()
    assert report.is_isolated_within_declared_accesses is True


def test_the_evaluation_layer_does_not_reach_the_execution_mechanism() -> None:
    assert evaluation_import_isolation_audit().is_isolated is True
    import alghanem.evaluation as evaluation

    assert not hasattr(evaluation, "ExecutionAuthority")


def test_no_comparison_or_second_system_is_built_in_this_phase() -> None:
    import alghanem.evaluation_execution as execution

    assert not hasattr(execution, "compare_run_reports")
    assert not hasattr(execution, "ParetoFrontier")
    assert NO_COMPARISON_BEFORE_BOUND_EXECUTION in EXECUTION_LAWS


def test_an_execution_request_outside_its_frozen_files_is_refused() -> None:
    with pytest.raises(ExecutionError):
        ReaderExecutionRequest(
            identity=_identity(_READERS / "reader_one.py", {"mode": "reader_one.py"}),
            implementation_files=(_READERS / "reader_one.py",),
            entry_file=_READERS / "reader_two.py",
            configuration={"mode": "reader_one.py"},
        )


def test_the_receipt_is_signed_by_the_key_of_the_authority_that_issued_it() -> None:
    binding = _binding(("reader_one.py",))
    authority = ExecutionAuthority(binding)
    receipt = authority.execute(_request(_READERS / "reader_one.py"))
    assert receipt.issuer_key_id == authority.issuer_key_id
    assert authority.verify_issuance(receipt) is True
    assert receipt.issuance_provenance_law == (
        RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED
    )


def test_another_authority_does_not_vouch_for_a_receipt_it_did_not_issue() -> None:
    binding = _binding(("reader_one.py",))
    receipt = ExecutionAuthority(binding).execute(_request(_READERS / "reader_one.py"))
    assert ExecutionAuthority(binding).verify_issuance(receipt) is False
    assert verify_receipt_issuance(receipt, ReceiptIssuanceKey()) is False


def test_a_signature_over_other_content_does_not_verify() -> None:
    binding = _binding(("reader_one.py",))
    authority = ExecutionAuthority(binding)
    here = authority.execute(_request(_READERS / "reader_one.py"))
    elsewhere = authority.execute(_request(_READERS / "reader_two.py"))
    assert here.issuance_signature != elsewhere.issuance_signature
    assert authority.verify_issuance(here) is True
    assert authority.verify_issuance(elsewhere) is True


def test_the_issuance_key_never_leaves_its_authority_as_content_or_text() -> None:
    key = ReceiptIssuanceKey()
    assert "secret" not in repr(key)
    assert key.key_id in repr(key)
    assert "secret" not in str(sorted(key.as_canonical_content()))
    assert key.is_proven is False
    assert key.ceiling == AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE
    assert not hasattr(key, "secret")


def test_the_issuance_provenance_ceiling_is_declared_not_claimed_as_proven() -> None:
    authority = ExecutionAuthority(_binding(("reader_one.py",)))
    assert authority.issuance_provenance_standing.is_proven is False
    assert authority.issuance_provenance_ceiling == (
        AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE
    )


def test_the_configuration_reaches_the_reader_call_and_moves_its_outputs() -> None:
    first, first_request = _configured_request(
        "reader_configured.py", {"observed_input_index": "0"}
    )
    last, last_request = _configured_request(
        "reader_configured.py", {"observed_input_index": "-1"}
    )
    head = first.execute(first_request)
    tail = last.execute(last_request)
    assert head.exit_status is ExecutionExitStatus.COMPLETED
    assert tail.exit_status is ExecutionExitStatus.COMPLETED
    assert head.output_digest != tail.output_digest
    assert head.execution_envelope_digest != tail.execution_envelope_digest


def test_the_payload_bytes_cross_the_envelope_unchanged() -> None:
    binding = _binding(("reader_one.py",))
    authority = ExecutionAuthority(binding)
    receipt = authority.execute(_request(_READERS / "reader_one.py"))
    assert receipt.payload_digest == binding.payload.payload_digest
    assert len(receipt.outputs) == len(_GOLD)


def test_a_configuration_that_did_not_arrive_as_written_is_named_not_read() -> None:
    binding = _binding(("reader_one.py",))

    class _DeliveringSomethingElse(ExecutionAuthority):
        def _run_in_a_separate_process(
            self, measured: object, entry_displayed: object, envelope: object
        ) -> SeparateProcessOutcome:
            outcome = super()._run_in_a_separate_process(  # type: ignore[arg-type]
                measured, entry_displayed, envelope
            )
            tampered = outcome.stdout.replace(
                b'"envelope_digest":"' + envelope.envelope_digest.encode("ascii"),  # type: ignore[attr-defined]
                b'"envelope_digest":"' + b"0" * 64,
            )
            return SeparateProcessOutcome(
                timed_out=False,
                return_code=outcome.return_code,
                stdout=tampered,
                stderr=outcome.stderr,
            )

    receipt = _DeliveringSomethingElse(binding).execute(
        _request(_READERS / "reader_one.py")
    )
    assert receipt.exit_status is ExecutionExitStatus.CONFIGURATION_DELIVERY_MISMATCH
    assert receipt.outputs == ()
    assert any(
        entry == "envelope.law=" + CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED
        for entry in receipt.trace
    )


def test_a_reader_with_the_abandoned_signature_is_refused_under_its_own_status() -> (
    None
):
    receipt = _run("reader_legacy_signature.py")
    assert receipt.exit_status is ExecutionExitStatus.REFUSED_ENTRYPOINT_SIGNATURE
    assert receipt.outputs == ()
    with pytest.raises(EvaluationError):
        report_from_receipt(receipt, run_ordinal=1)


def test_a_wire_value_of_the_wrong_type_is_refused_and_not_coerced() -> None:
    receipt = _run("reader_coerced_residual.py")
    assert receipt.exit_status is ExecutionExitStatus.REFUSED_OUTPUT_SHAPE
    assert receipt.residuals == ()
    assert A_WIRE_VALUE_IS_REFUSED_NOT_COERCED in EXECUTION_LAWS


def test_a_run_that_exceeds_its_declared_ceiling_is_named_a_timeout() -> None:
    configuration = {"sleep_seconds": "30"}
    authority, request = _configured_request("reader_slow.py", configuration)
    receipt = ExecutionAuthority(authority.binding, timeout_seconds=1).execute(request)
    assert receipt.exit_status is ExecutionExitStatus.TIMEOUT
    assert receipt.is_a_reference_run is False
    assert "process.timed_out=true" in receipt.trace
    assert "process.timeout_seconds=1" in receipt.trace
    with pytest.raises(EvaluationError):
        report_from_receipt(receipt, run_ordinal=1)


def test_a_process_killed_by_a_signal_is_named_apart_from_a_nonzero_exit() -> None:
    receipt = _run("reader_signalled.py")
    assert receipt.exit_status is ExecutionExitStatus.SIGNALLED
    assert receipt.exit_status is not ExecutionExitStatus.NONZERO_EXIT
    assert A_TIMEOUT_IS_NAMED_NOT_FOLDED_INTO_A_NONZERO_EXIT in EXECUTION_LAWS


def test_no_guard_return_code_is_invented_for_a_run_that_never_exited() -> None:
    timed_out = SeparateProcessOutcome(
        timed_out=True, return_code=None, stdout=b"", stderr=b""
    )
    assert timed_out.was_signalled is False
    with pytest.raises(ExecutionError):
        SeparateProcessOutcome(timed_out=True, return_code=-1, stdout=b"", stderr=b"")
    assert (
        SeparateProcessOutcome(
            timed_out=False, return_code=-9, stdout=b"", stderr=b""
        ).was_signalled
        is True
    )
