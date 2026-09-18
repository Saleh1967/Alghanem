"""Run the `G0.EXEC-0` bound reader execution end to end, up to a reveal record.

Run it::

    ALGHANEM_GOLD_NONCE_FILE=/path/outside/the/tree/nonce.bin \\
        python examples/evaluation/run_blind_evaluation.py

**The nonce never lives in this repository.** The core never learns where it came
from: `commit_gold(..., nonce=...)` has no default and no derivation. This script
reads it from `ALGHANEM_GOLD_NONCE_FILE` (a file outside the tree) or from the
`ALGHANEM_GOLD_NONCE` secret environment variable as hex. If neither is present
it generates an ephemeral one in memory for the demonstration and discards it.
It is never printed and never written back.

**The gold here is bound, not cryptographically hidden.** In the current madlul
domain the answer key already lives in `madlul_alone_formal.py`, so the honest
claim is `blind-by-boundary + commitment binding`, not secret gold:
`DigestOnly != CryptographicallyHiddenGold`.

**The static import audit is not process isolation.** Refusing `importlib`,
`__import__` and dynamic file access in a reader's source strengthens the
boundary; it does not prove confinement. Process confinement stands as
`DECLARED_DEFERRED`: `StaticImportAudit != ProcessIsolation`.

**The readers are really executed.** No output in this script is fabricated by the
harness. The frozen implementation bytes were executed against the bound blind
payload under the declared separate-process execution mechanism, and the
resulting bytes were captured in an authority-issued execution receipt. Every
run report here is derived from such a receipt and from nothing else:
`NoRunReportWithoutBoundExecution` and `AHarnessIsNotAnExecutionAuthority`.

**A separate process is not a sandbox.** The reader runs in another interpreter
process with a pruned environment, a temporary out-of-tree workspace and bytes on
`stdin`; that is a declared mechanism, not proven confinement:
`SeparateProcess != Sandbox`.

Nothing here compares the readers. There is no verdict, no dominance and no
`Ω_M` in this phase: the ceiling is a `GoldRevealRecord` and nothing beyond it.
"""

from __future__ import annotations

import os
import secrets
from pathlib import Path

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
    NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION,
    BoundExecutionReceipt,
    EvaluationBinding,
    EvaluationProtocolKind,
    ExecutionExitStatus,
    FrozenEvaluationProtocol,
    FrozenSystemIdentity,
    GoldRevealAuthority,
    ProcessConfinementDeclaration,
    RunLedger,
    evaluation_import_isolation_audit,
    freeze_system_identity,
    reader_import_audit,
    report_from_receipt,
)
from alghanem.evaluation_execution import (
    EXECUTION_LAWS,
    ExecutionAuthority,
    ReaderExecutionRequest,
    execution_import_isolation_audit,
)
from alghanem.prior_fiber import SuccessCriterion

READERS = Path(__file__).resolve().parents[2] / "tests" / "evaluation" / "readers"

MODES = {
    "reader_one.py": "first observed input",
    "reader_two.py": "last observed input",
}


def read_nonce() -> bytes:
    """Read the nonce from outside the tree; never derive it and never print it."""

    named = os.environ.get("ALGHANEM_GOLD_NONCE_FILE")
    if named:
        return Path(named).read_bytes()
    hexed = os.environ.get("ALGHANEM_GOLD_NONCE")
    if hexed:
        return bytes.fromhex(hexed)
    return secrets.token_bytes(32)


def freeze_reader(file_name: str, mode: str) -> FrozenSystemIdentity:
    """Freeze a reader identity from its source bytes, not from its name."""

    files = (READERS / file_name,)
    return freeze_system_identity(
        implementation_files=files,
        configuration={"mode": mode},
        boundary_report=reader_import_audit(files),
        contract_interface_version=MADLUL_CONTRACT_INTERFACE_VERSION,
    )


def execute_reader(
    authority: ExecutionAuthority, identity: FrozenSystemIdentity, file_name: str
) -> BoundExecutionReceipt:
    """Execute the frozen bytes themselves and take the authority's receipt."""

    path = READERS / file_name
    return authority.execute(
        ReaderExecutionRequest(
            identity=identity,
            implementation_files=(path,),
            entry_file=path,
            configuration={"mode": MODES[file_name]},
        )
    )


def main() -> None:
    """Freeze the contract, bind the readers, run them blind and reveal the gold."""

    nonce = read_nonce()
    contract = build_madlul_fiber_contract(commit_madlul_gold(nonce))
    protocol = FrozenEvaluationProtocol(
        protocol_id="protocol.madlul.g0_eval_0",
        kind=EvaluationProtocolKind.FORMAL_CLASSIFICATION,
        success_criteria=tuple(SuccessCriterion),
        residual_policy_ref="residual.declared",
        payload_scheme="scheme.blind.bytes",
        contract_interface_version=MADLUL_CONTRACT_INTERFACE_VERSION,
    )
    readers = tuple(freeze_reader(name, MODES[name]) for name in MODES)
    binding = EvaluationBinding(
        contract=contract, protocol=protocol, reader_identities=readers
    )

    print("== the frozen contract and its commitment ==")
    print(f"contract body      : {contract.contract_body_digest[:16]}")
    print(f"commitment         : {contract.gold_commitment.commitment_digest[:16]}")
    print(f"contract digest    : {contract.contract_digest[:16]}")
    print(f"no reader identity : {contract.carries_no_reader_identity}")
    print(f"nonce in fields    : {not contract.gold_commitment.withholds_its_nonce}")

    print()
    print("== the frozen reader identities ==")
    for identity in readers:
        print(
            f"  content id {identity.content_id[:16]} "
            f"impl {identity.implementation_digest[:8]} "
            f"conf {identity.configuration_digest[:8]} "
            f"bound {identity.dependency_boundary_digest[:8]}"
        )

    payload = binding.payload
    print()
    print("== what the readers actually receive ==")
    print(f"payload type       : {type(payload.payload_bytes).__name__}")
    print(f"payload digest     : {payload.payload_digest[:16]}")
    for section in MadlulSection:
        print(f"  withheld({section.value:<24}) = {payload.withholds(section.value)}")

    execution = ExecutionAuthority(binding)
    ledger = RunLedger(binding)
    receipts = []
    for identity, file_name in zip(readers, MODES):
        receipt = execute_reader(execution, identity, file_name)
        receipts.append(receipt)
        if receipt.exit_status is not ExecutionExitStatus.COMPLETED:
            raise SystemExit(f"execution did not complete: {receipt.exit_status.value}")
        ledger.record(report_from_receipt(receipt, run_ordinal=1))

    print()
    print("== the authority-issued execution receipts ==")
    print(f"execution mechanism: {execution.execution_mode.value}")
    print(f"confinement proven : {execution.confinement.is_proven}")
    for receipt in receipts:
        print(
            f"  receipt {receipt.receipt_digest[:16]} "
            f"status {receipt.exit_status.value} "
            f"output {receipt.output_digest[:8]} "
            f"trace {receipt.trace_digest[:8]}"
        )

    print()
    print("== the frozen run reports, each derived from its receipt ==")
    for identity in readers:
        report = ledger.first_report(identity.content_id)
        print(
            f"  ordinal {report.run_ordinal} "
            f"report {report.report_digest[:16]} "
            f"classified {len(report.classified_member_ids)} "
            f"residuals {len(report.residuals)}"
        )
    print(f"violations         : {len(ledger.violations)}")

    authority = GoldRevealAuthority(ledger)
    labels = {
        madlul_member_id(witness): witness.attested_section.value
        for witness in ATTESTED_SIGNIFIED_WITNESSES
    }
    record = authority.reveal(labels, nonce=nonce)

    print()
    print("== the reveal record ==")
    print(f"may reveal         : {authority.may_reveal}")
    print(f"record digest      : {record.record_digest[:16]}")
    print(f"revealed members   : {record.revealed_member_count}")
    print(f"carries no gold    : {record.withholds_gold_and_nonce}")
    print(f"is not a verdict   : {record.is_not_a_verdict}")

    confinement = ProcessConfinementDeclaration()
    audit = evaluation_import_isolation_audit()
    print()
    print("== what this layer does not claim ==")
    print(f"layer isolated     : {audit.is_isolated}")
    print(f"confinement proven : {confinement.is_proven}")
    print(f"confinement stand  : {confinement.standing.value}")
    execution_audit = execution_import_isolation_audit()
    print(
        f"execution isolated : {execution_audit.is_isolated_within_declared_accesses}"
    )
    print(f"evaluation laws    : {len(EVALUATION_LAWS)}")
    print(f"execution laws     : {len(EXECUTION_LAWS)}")
    print(f"bound run law      : {NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION[:60]}…")
    print(f"verdict law        : {NO_EVALUATION_VERDICT_BEFORE[:60]}…")


if __name__ == "__main__":
    main()
