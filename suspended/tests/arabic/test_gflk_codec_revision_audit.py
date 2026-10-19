"""Tests for the audit of the externally deposited carrier/state revision."""

from __future__ import annotations

import pkgutil
import unicodedata
from dataclasses import fields, replace

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.encoding.carrier_state_candidate import (
    QURANIC_CORPUS_INVERTIBILITY,
    CarrierStateCodec,
    CarrierStateEncodingError,
    round_trip_holds,
)
from alghanem.arabic.gflk_codec_revision_audit import (
    CLAIMED_ROUND_TRIP_FRACTION,
    CLAIMED_TOKEN_TOTAL,
    GFLK_CODEC_REVISION_AUDIT,
    GFLK_REVISION_AUDIT_RESIDUALS,
    PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT,
    REVISION_AUDIT_AUTHORITY_NOTE,
    SILENT_OVERWRITE_LOCATIONS,
    AdoptionOutcome,
    CodecRevisionAudit,
    CorruptedToken,
    GflkCodecRevisionAuditError,
)
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS

CODEC = CarrierStateCodec()

SHADDA = "\u0651"
FATHA = "\u064e"
DAMMA = "\u064f"
KASRA = "\u0650"
SUKUN = "\u0652"
TANWIN_FATHA = "\u064b"
TANWIN_DAMMA = "\u064c"
MADDA_ALEF = "\u0622"


# --- the negative controls: the two genera the revision reinstates ----------


@pytest.mark.parametrize(
    "surface",
    [
        "\u0628" + FATHA + DAMMA,
        "\u0628" + TANWIN_FATHA + TANWIN_DAMMA,
        "\u0628" + TANWIN_FATHA + FATHA,
        "\u0628" + SHADDA + SHADDA,
        "\u0628" + KASRA + SUKUN,
    ],
)
def test_a_second_write_over_a_read_state_is_refused_not_absorbed(
    surface: str,
) -> None:
    """The genus the deposited revision reinstates, pinned as a regression.

    The deposited loop assigns over an already-derived state and emits a
    shorter surface with no warning. Refusal here is what makes the six corpus
    corruptions impossible in this tree, so a future simplification toward that
    loop fails a test rather than a review.
    """

    with pytest.raises(CarrierStateEncodingError):
        CODEC.generate(surface)


@pytest.mark.parametrize(
    "surface",
    [
        MADDA_ALEF,
        MADDA_ALEF + TANWIN_FATHA,
        MADDA_ALEF + FATHA,
        MADDA_ALEF + SHADDA,
        MADDA_ALEF + SHADDA + DAMMA,
    ],
)
def test_the_madda_alef_keeps_every_field_written_beside_it(surface: str) -> None:
    """`آً` must not come back as `آ`: the second reinstated genus.

    These surfaces do not occur in the Quranic corpus, so a corpus rate near
    100% never reaches them; that is A_CORPUS_RATE_DOES_NOT_COVER_THE_UNATTESTED
    made executable rather than asserted.
    """

    assert round_trip_holds(surface)


def test_the_repaired_defect_is_credited_by_running_it_not_by_asserting_it() -> None:
    for surface in ("\u0627\u0644\u0639\u0631\u0628\u064a\u0629!", "hello"):
        assert round_trip_holds(surface)
    assert "العربية" in PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT


# --- the recorded corruptions ----------------------------------------------


def test_every_recorded_corruption_names_its_location_and_both_surfaces() -> None:
    assert len(SILENT_OVERWRITE_LOCATIONS) == 6
    locations = [token.location for token in SILENT_OVERWRITE_LOCATIONS]
    assert len(set(locations)) == 6
    for token in SILENT_OVERWRITE_LOCATIONS:
        assert token.surface_in != token.surface_out
        assert unicodedata.normalize("NFC", token.surface_in) == token.surface_in


def test_the_corpus_refuses_exactly_the_recorded_locations() -> None:
    """Each recorded input is a surface this tree's codec declines to read."""

    for token in SILENT_OVERWRITE_LOCATIONS:
        with pytest.raises(CarrierStateEncodingError):
            CODEC.generate(token.surface_in)


def test_a_token_that_came_back_unchanged_is_not_a_corruption() -> None:
    with pytest.raises(GflkCodecRevisionAuditError, match="عادت كما دخلت"):
        CorruptedToken(sura=1, aya=1, word=1, surface_in="\u0628", surface_out="\u0628")
    with pytest.raises(GflkCodecRevisionAuditError, match="عددٌ صحيحٌ موجب"):
        CorruptedToken(sura=0, aya=1, word=1, surface_in="\u0628", surface_out="\u062a")
    with pytest.raises(GflkCodecRevisionAuditError, match="نصٌّ غير فارغ"):
        CorruptedToken(sura=1, aya=1, word=1, surface_in="  ", surface_out="\u062a")


# --- the verdict is computed, not written ----------------------------------


def test_the_audit_carries_no_field_a_verdict_could_be_written_into() -> None:
    declared = {item.name for item in fields(CodecRevisionAudit)}
    for forbidden in ("outcome", "verdict", "adopted", "birth", "freeze", "rank"):
        assert not any(forbidden in name.split("_") for name in declared), forbidden


def test_the_refusal_is_derived_from_the_comparison_and_the_residuals() -> None:
    audit = GFLK_CODEC_REVISION_AUDIT
    assert audit.outcome is AdoptionOutcome.ADOPTION_REFUSED
    assert audit.claim_reproduced is False
    assert audit.claimed_round_trip_fraction == CLAIMED_ROUND_TRIP_FRACTION == 1.0
    assert audit.claimed_token_total == CLAIMED_TOKEN_TOTAL == 78_245
    assert audit.measured_token_total == QURANIC_CORPUS_INVERTIBILITY.token_total
    assert audit.token_total_gap == 78_245 - audit.measured_token_total
    assert round(audit.measured_round_trip_fraction, 8) == 0.99992251
    assert audit.measured_round_trip_fraction < audit.claimed_round_trip_fraction


def test_clearing_the_residuals_alone_does_not_buy_a_reproduced_claim() -> None:
    """Emptying the blocking set leaves the measured shortfall standing."""

    audit = replace(GFLK_CODEC_REVISION_AUDIT, blocking_residual_codes=frozenset())
    assert audit.outcome is AdoptionOutcome.ADOPTION_REFUSED
    assert audit.claim_reproduced is False


def test_the_other_branch_of_the_outcome_is_reachable_by_measurement() -> None:
    """A computed verdict must have both branches reachable, or it is a label."""

    audit = replace(
        GFLK_CODEC_REVISION_AUDIT,
        blocking_residual_codes=frozenset(),
        corrupted_tokens=(),
        claimed_token_total=QURANIC_CORPUS_INVERTIBILITY.token_total,
    )
    assert audit.claim_reproduced is True
    assert audit.outcome is AdoptionOutcome.CLAIM_REPRODUCED_PENDING_AUTHORITY
    assert not any(
        "born" in member.value.lower() or "certified" in member.value.lower()
        for member in AdoptionOutcome
    )


def test_the_audit_is_bound_to_the_bytes_it_claims_to_have_measured() -> None:
    audit = GFLK_CODEC_REVISION_AUDIT
    assert audit.witness is QURANIC_ARABIC_CORPUS_WITNESS
    with pytest.raises(GflkCodecRevisionAuditError, match="بصمةُ القياس"):
        replace(
            audit,
            tree_codec_measurement=replace(
                QURANIC_CORPUS_INVERTIBILITY, source_sha256="b" * 64
            ),
        )
    with pytest.raises(GflkCodecRevisionAuditError, match="بصمةُ القياس"):
        replace(
            audit,
            tree_codec_measurement=replace(
                QURANIC_CORPUS_INVERTIBILITY, source_byte_length=1
            ),
        )


def test_an_unregistered_blocking_residual_is_refused() -> None:
    with pytest.raises(GflkCodecRevisionAuditError, match="غيرُ مُسجَّلة"):
        replace(
            GFLK_CODEC_REVISION_AUDIT,
            blocking_residual_codes=frozenset({"NOT_A_REGISTERED_CODE"}),
        )


def test_a_duplicated_corruption_location_is_refused() -> None:
    first = SILENT_OVERWRITE_LOCATIONS[0]
    with pytest.raises(GflkCodecRevisionAuditError, match="مكرَّرٌ"):
        replace(GFLK_CODEC_REVISION_AUDIT, corrupted_tokens=(first, first))


# --- the residuals ----------------------------------------------------------


def test_every_named_residual_is_registered_and_non_blank() -> None:
    assert set(GFLK_REVISION_AUDIT_RESIDUALS) == {
        "ROUND_TRIP_IS_NOT_100_PERCENT_ON_THIS_CORPUS",
        "SILENT_OVERWRITE_DEFECT_REINSTATED",
        "MADD_SELF_STILL_DROPS_EVERY_OTHER_FIELD",
        "A_CORPUS_RATE_DOES_NOT_COVER_THE_UNATTESTED",
        "THE_CLAIMED_CORPUS_IS_UNIDENTIFIED",
        "SECOND_SOURCE_IS_NOT_AN_INDEPENDENT_LINE",
        "DOCSTRING_CONTRADICTS_ITS_OWN_CODE",
        "PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT",
    }
    assert all(text.strip() for text in GFLK_REVISION_AUDIT_RESIDUALS.values())
    assert GFLK_CODEC_REVISION_AUDIT.blocking_residual_codes <= set(
        GFLK_REVISION_AUDIT_RESIDUALS
    )
    assert (
        "PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT"
        not in GFLK_CODEC_REVISION_AUDIT.blocking_residual_codes
    )


# --- authority: this module is inert ---------------------------------------


def test_no_kernel_module_reads_this_audit() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "gflk_codec_revision_audit" not in text, module.name
        assert "CodecRevisionAudit" not in text, module.name


def test_the_audit_module_imports_nothing_from_the_kernel() -> None:
    import alghanem.arabic.gflk_codec_revision_audit as module

    with open(module.__file__ or "", encoding="utf-8") as handle:
        text = handle.read()
    imports = [
        line
        for line in text.splitlines()
        if line.startswith(("import ", "from ")) and "kernel" in line
    ]
    assert imports == []
    assert "REVISION_AUDIT_IS_A_RECORD_NOT_A_GATE" in REVISION_AUDIT_AUTHORITY_NOTE
