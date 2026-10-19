"""شواهدُ العقود الليفيّة: لا انتقالَ بلا عقدٍ مكتوبٍ مفحوص."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from alghanem.arabic import fiber_transfer_contracts
from alghanem.arabic.fiber_transfer_contracts import (
    CV_BIRTH_CERTIFICATE_STANDING,
    FIBER_TRANSFER_LEDGER,
    FIBER_TRANSFER_NAMED_RESIDUALS,
    CertificateStanding,
    FiberTransferContract,
    FiberTransferError,
    TrackId,
    TransferEvidence,
    compose,
    contract_for,
)
from alghanem.canonical_content import canonical_bytes, canonical_digest


def _evidence(
    track: TrackId = TrackId.FLT1_QIYAS,
    anchor: str = "minimality.يَكْتُبُ",
) -> TransferEvidence:
    return TransferEvidence(
        origin_track=track,
        origin_anchor=anchor,
        what_it_attests="انعقادُ الشروط الأربعة على هذه الصورة",
        content_digest=canonical_digest(canonical_bytes({"surface": "يَكْتُبُ"})),
    )


def _contract(**overrides: object) -> FiberTransferContract:
    base = FiberTransferContract(
        contract_id="flt1→vv.مثالُ شاهد",
        origin_track=TrackId.FLT1_QIYAS,
        origin_anchor="minimality.يَكْتُبُ",
        branch_track=TrackId.VV_BIRTH,
        branch_anchor="H_S.يَكْتُبُ",
        preserved_identity=("صورةُ المقطع", "ترتيبُ الحاملِ والحال"),
        evidence=_evidence(),
        licensed_conclusions=("الشروطُ الأربعةُ انعقدت على هذه الصورة",),
        what_it_does_not_license=("شهادةُ ولادة CV", "حيادُ VV"),
        named_residuals=("لا صوتَ مُسجَّلًا في الطرفين",),
    )
    return replace(base, **overrides)  # type: ignore[arg-type]


def test_a_written_contract_names_its_five_parts() -> None:
    contract = _contract()

    assert contract.origin_track is TrackId.FLT1_QIYAS
    assert contract.branch_track is TrackId.VV_BIRTH
    assert contract.preserved_identity
    assert contract.evidence.origin_anchor == contract.origin_anchor
    assert contract.named_residuals


def test_a_contract_licenses_only_what_is_written_in_it() -> None:
    contract = _contract()

    assert contract.licenses("الشروطُ الأربعةُ انعقدت على هذه الصورة")
    assert not contract.licenses("حيادُ VV")
    assert not contract.licenses("شهادةُ ولادة CV")


def test_a_contract_whose_origin_is_its_own_branch_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        _contract(branch_track=TrackId.FLT1_QIYAS)


def test_a_contract_with_no_preserved_identity_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        _contract(preserved_identity=())


def test_a_contract_with_no_named_residual_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        _contract(named_residuals=())


def test_a_contract_that_both_licenses_and_forbids_one_conclusion_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        _contract(what_it_does_not_license=("الشروطُ الأربعةُ انعقدت على هذه الصورة",))


def test_borrowed_evidence_from_another_track_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        _contract(evidence=_evidence(track=TrackId.VV_BIRTH))


def test_evidence_from_another_anchor_of_the_same_track_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        _contract(evidence=_evidence(anchor="minimality.فَتَحَ"))


def test_evidence_without_a_canonical_digest_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        TransferEvidence(
            origin_track=TrackId.FLT1_QIYAS,
            origin_anchor="minimality.يَكْتُبُ",
            what_it_attests="شهادةٌ بلا بصمة",
            content_digest="ليست بصمة",
        )


def test_two_contracts_do_not_compose_into_a_third() -> None:
    first = _contract()
    second = _contract(
        contract_id="vv→flt1.مثالٌ معكوس",
        origin_track=TrackId.VV_BIRTH,
        origin_anchor="H_S.يَكْتُبُ",
        branch_track=TrackId.FLT1_QIYAS,
        branch_anchor="minimality.يَكْتُبُ",
        evidence=_evidence(track=TrackId.VV_BIRTH, anchor="H_S.يَكْتُبُ"),
    )

    with pytest.raises(FiberTransferError, match="ATransferDoesNotCompose"):
        compose(first, second)


def test_no_transfer_from_flt1_to_vv_birth_is_written_today() -> None:
    assert FIBER_TRANSFER_LEDGER == ()

    with pytest.raises(FiberTransferError, match="AnEmptyLedgerIsNotARefutation"):
        contract_for(TrackId.FLT1_QIYAS, TrackId.VV_BIRTH)


def test_a_written_contract_is_found_in_the_ledger_it_is_written_in() -> None:
    contract = _contract()

    assert contract_for(TrackId.FLT1_QIYAS, TrackId.VV_BIRTH, (contract,)) is contract

    with pytest.raises(FiberTransferError):
        contract_for(TrackId.VV_BIRTH, TrackId.FLT1_QIYAS, (contract,))


def test_the_cv_birth_certificate_is_unissued_and_its_lack_is_enumerated() -> None:
    standing = CV_BIRTH_CERTIFICATE_STANDING

    assert standing.issued is False
    assert len(standing.what_is_still_missing) == 4
    assert any("G0.VV-BIRTH-1" in item for item in standing.what_is_still_missing)


def test_an_unissued_certificate_without_a_reason_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        CertificateStanding(
            certificate_id="CV.birth", issued=False, what_is_still_missing=()
        )


def test_an_issued_certificate_that_still_lists_a_lack_is_refused() -> None:
    with pytest.raises(FiberTransferError):
        CertificateStanding(
            certificate_id="CV.birth",
            issued=True,
            what_is_still_missing=("ما زال ينقصها شيء",),
        )


def test_the_module_names_its_own_limits_as_residuals() -> None:
    assert len(FIBER_TRANSFER_NAMED_RESIDUALS) == 6
    assert any(
        "ASuccessfulMinimalityTestDoesNotCrossTracks" in note
        for note in FIBER_TRANSFER_NAMED_RESIDUALS
    )
    assert any(
        "ATransferContractIsNotABirthCertificate" in note
        for note in FIBER_TRANSFER_NAMED_RESIDUALS
    )


def test_this_module_reaches_no_kernel_module() -> None:
    from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary

    report = audit_import_boundary(
        (Path(fiber_transfer_contracts.__file__),),
        ImportBoundaryPolicy(
            policy_id="fiber-transfer-contracts-are-not-wired-to-the-kernel",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )

    assert not any(
        reached == "alghanem.kernel" or reached.startswith("alghanem.kernel.")
        for reached in report.reached_modules
    ), report.reached_modules
