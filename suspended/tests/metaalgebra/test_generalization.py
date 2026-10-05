"""اختباراتُ مانع التعميم G0.GEN: الامتدادُ يُرفَض عند الإنشاء لا عند القراءة."""

from __future__ import annotations

import pytest

from alghanem.metaalgebra.generalization import (
    AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN,
    DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE,
    ENUMERATION_IS_NOT_A_GENERALIZATION_LAW,
    GENERALIZATION_NAMED_RESIDUALS,
    LOCAL_CLOSURE_IS_NOT_GLOBAL_CLOSURE,
    DomainIdentityEvidence,
    GeneralizationLaw,
    GeneralizationWarrant,
    MetaAlgebraGeneralizationError,
    ScopedClaim,
    ScopedClaimExtension,
)

_CLAIM = ScopedClaim(
    claim_id="alif-fiber",
    predicate="فضاءُ الحالة تابعٌ لهوية الحامل",
    measured_domain_id="fatiha-nfc",
)
_EVIDENCE = DomainIdentityEvidence(
    subdomain_id="fatiha-nfc",
    domain_id="arabic-open",
    citation="docs/CONSTITUTION.md#G0.GEN",
    argument="النطاقان واحدٌ بحجّةٍ تُراجَع",
)
_LAW = GeneralizationLaw(
    law_id="closure-transfer",
    statement="ما انغلق في النطاق الجزئيّ ينغلق في الكلّيّ بشرطه",
    precondition="أن يكون النطاقُ الجزئيّ ممثِّلًا بالمعنى المُسمّى",
)


def _extension(**overrides: object) -> ScopedClaimExtension:
    arguments: dict[str, object] = {
        "claim": _CLAIM,
        "target_domain_id": "arabic-open",
        "warrant": GeneralizationWarrant.NAMED_GENERALIZATION_LAW,
        "domain_identity_evidence": None,
        "generalization_law": _LAW,
        "reason": "امتدادٌ مُبرَّرٌ بقانونٍ مُسمًّى",
    }
    arguments.update(overrides)
    return ScopedClaimExtension(**arguments)  # type: ignore[arg-type]


# --- الدعوى مقيَّدةٌ بنطاقها --------------------------------------------------


def test_a_claim_carries_its_measured_domain_as_part_of_itself() -> None:
    assert _CLAIM.measured_domain_id == "fatiha-nfc"


def test_a_claim_without_a_measured_domain_is_refused() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError):
        ScopedClaim(claim_id="c", predicate="p", measured_domain_id="  ")


# --- لا امتدادَ بلا سند -------------------------------------------------------


def test_an_extension_without_a_warrant_is_refused_at_construction() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError) as error:
        _extension(warrant=GeneralizationWarrant.NO_WARRANT, generalization_law=None)
    message = str(error.value)
    assert LOCAL_CLOSURE_IS_NOT_GLOBAL_CLOSURE in message
    assert AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN in message


def test_absence_of_a_warrant_blocks_promotion_not_the_record() -> None:
    assert _CLAIM.measured_domain_id == "fatiha-nfc"
    assert not GeneralizationWarrant.NO_WARRANT.licenses_extension


def test_extending_a_claim_to_its_own_measured_domain_is_not_an_extension() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError):
        _extension(target_domain_id="fatiha-nfc")


def test_a_warrant_outside_the_closed_vocabulary_is_refused() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError):
        _extension(warrant="NAMED_GENERALIZATION_LAW")


# --- مطابقةُ النطاقين دعوى لا تُقبَل مرسلة ------------------------------------


def test_a_domain_identity_warrant_without_its_evidence_is_refused() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError) as error:
        _extension(
            warrant=GeneralizationWarrant.DOMAIN_IDENTITY_PROVED,
            generalization_law=None,
        )
    assert DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE in str(error.value)


def test_evidence_about_two_other_domains_is_not_evidence_here() -> None:
    elsewhere = DomainIdentityEvidence(
        subdomain_id="another-corpus",
        domain_id="arabic-open",
        citation="x",
        argument="y",
    )
    with pytest.raises(MetaAlgebraGeneralizationError):
        _extension(
            warrant=GeneralizationWarrant.DOMAIN_IDENTITY_PROVED,
            domain_identity_evidence=elsewhere,
            generalization_law=None,
        )


def test_a_proved_domain_identity_with_its_own_evidence_is_licensed() -> None:
    extension = _extension(
        warrant=GeneralizationWarrant.DOMAIN_IDENTITY_PROVED,
        domain_identity_evidence=_EVIDENCE,
        generalization_law=None,
    )
    assert extension.is_licensed_extension


def test_evidence_may_not_be_ignored_beside_another_warrant() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError):
        _extension(domain_identity_evidence=_EVIDENCE)


# --- قانونُ التعميم اسمٌ ونصّ -------------------------------------------------


def test_a_law_warrant_without_its_law_is_refused() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError) as error:
        _extension(generalization_law=None)
    assert ENUMERATION_IS_NOT_A_GENERALIZATION_LAW in str(error.value)


def test_a_law_without_its_precondition_is_refused() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError):
        GeneralizationLaw(law_id="l", statement="s", precondition="")


def test_a_named_law_with_its_precondition_licenses_the_extension() -> None:
    assert _extension().is_licensed_extension


# --- سندٌ واحدٌ يُعلَن لا سندان -----------------------------------------------


def test_two_warrants_at_once_are_refused_because_neither_is_readable() -> None:
    with pytest.raises(MetaAlgebraGeneralizationError):
        _extension(
            warrant=GeneralizationWarrant.DOMAIN_IDENTITY_PROVED,
            domain_identity_evidence=_EVIDENCE,
            generalization_law=_LAW,
        )


# --- الترخيصُ مُشتَقٌّ لا مكتوب ------------------------------------------------


def test_no_extension_field_declares_its_own_licensing() -> None:
    for name in ScopedClaimExtension.__slots__:
        for marker in ("licensed", "granted", "approved", "verdict", "rank", "status"):
            assert marker not in name


def test_every_named_residual_is_keyed_by_its_own_name() -> None:
    for name, text in GENERALIZATION_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}:")


# --- سلطة: هذا المانع خاملٌ في النواة -----------------------------------------


def test_no_kernel_module_reads_this_blocker() -> None:
    import pkgutil

    import alghanem.kernel as kernel_package

    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "metaalgebra.generalization" not in text, module.name
        assert "ScopedClaimExtension" not in text, module.name
