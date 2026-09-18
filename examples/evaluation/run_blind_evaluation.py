"""Run the `G0.EVAL-0` blind evaluation boundary end to end, up to a reveal record.

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
    EvaluationBinding,
    EvaluationProtocolKind,
    FrozenEvaluationProtocol,
    FrozenRunReport,
    FrozenSystemIdentity,
    GoldRevealAuthority,
    ProcessConfinementDeclaration,
    RunLedger,
    evaluation_import_isolation_audit,
    freeze_system_identity,
    reader_import_audit,
)
from alghanem.prior_fiber import SuccessCriterion

READERS = Path(__file__).resolve().parents[2] / "tests" / "evaluation" / "readers"


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


def run_reader(
    binding: EvaluationBinding, identity: FrozenSystemIdentity
) -> FrozenRunReport:
    """Hand the reader serialized bytes only, and freeze what it returned."""

    payload = binding.payload
    request = binding.request_for(identity)
    outputs = tuple(
        (member_id, "قسمٌ مُقترَحٌ من المدخلات المرصودة")
        for member_id in binding.contract.body.member_ids
    )
    return FrozenRunReport(
        request_id=request.request_id,
        system_content_id=identity.content_id,
        payload_digest=payload.payload_digest,
        outputs=outputs,
        residuals=(),
        trace=("received serialized bytes", "classified every declared member"),
        run_ordinal=1,
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
    readers = (
        freeze_reader("reader_one.py", "first observed input"),
        freeze_reader("reader_two.py", "last observed input"),
    )
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

    ledger = RunLedger(binding)
    for identity in readers:
        ledger.record(run_reader(binding, identity))

    print()
    print("== the frozen run reports ==")
    for identity in readers:
        report = ledger.first_report(identity.content_id)
        print(
            f"  ordinal {report.run_ordinal} "
            f"report {report.report_digest[:16]} "
            f"classified {len(report.classified_member_ids)}"
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
    print(f"laws               : {len(EVALUATION_LAWS)}")
    print(f"verdict law        : {NO_EVALUATION_VERDICT_BEFORE[:60]}…")


if __name__ == "__main__":
    main()
