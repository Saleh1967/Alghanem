"""اختبارُ الإيداع: تعارضاتٌ بمراجعها، وملفّاتٌ لم تصل، ولا حقلَ حسمٍ واحد."""

from __future__ import annotations

import dataclasses

import pytest

from alghanem.arabic.hollow_root_levels_deposit import (
    HOLLOW_ROOT_CONFLICTS,
    HOLLOW_ROOT_CONVERGENCES,
    HOLLOW_ROOT_DEPOSIT_NAMED_RESIDUALS,
    HOLLOW_ROOT_NUMERIC_CLAIMS,
    THE_BYTES_NEVER_REACHED_THIS_TREE,
    UNARRIVED_ARTEFACTS,
    ConflictStanding,
    HollowRootConflict,
    HollowRootDepositError,
    UnarrivedArtefact,
)

_RECORD_TYPES = (
    UnarrivedArtefact,
    HollowRootConflict,
)


def test_no_record_carries_a_resolution_field() -> None:
    for record in _RECORD_TYPES:
        names = {field.name for field in dataclasses.fields(record)}
        assert not {"resolution", "resolved", "verdict", "ruling"} & names


def test_every_unarrived_file_is_tagged_with_the_open_item() -> None:
    assert len(UNARRIVED_ARTEFACTS) == 3
    for artefact in UNARRIVED_ARTEFACTS:
        assert artefact.open_item == THE_BYTES_NEVER_REACHED_THIS_TREE


def test_a_quoted_digest_prefix_is_never_presented_as_a_full_digest() -> None:
    """صدرُ البصمة يُنقَل كما ورد، ولا يُكمَّل إلى أربعةٍ وستّين محرفًا اختلاقًا."""

    for artefact in UNARRIVED_ARTEFACTS:
        assert len(artefact.declared_digest_prefix) < 64


def test_the_open_item_name_cannot_be_softened() -> None:
    with pytest.raises(HollowRootDepositError):
        UnarrivedArtefact(
            file_name="x.py",
            declared_digest_prefix="00000000…",
            what_it_was_said_to_contain="شيء",
            never_arrived_because="سبب",
            open_item="A_PENDING_TRANSFER",
        )


def test_every_conflict_names_a_locus_and_a_tree_reference() -> None:
    assert len(HOLLOW_ROOT_CONFLICTS) == 6
    for conflict in HOLLOW_ROOT_CONFLICTS:
        assert conflict.locus.strip()
        assert "`" in conflict.tree_reference
        assert conflict.what_would_resolve_it.strip()
        assert isinstance(conflict.standing, ConflictStanding)


def test_a_conflict_without_a_resolving_condition_is_refused() -> None:
    with pytest.raises(HollowRootDepositError):
        HollowRootConflict(
            locus="موضع",
            the_claim_says="دعوى",
            this_tree_says="ردّ",
            tree_reference="`مرجع`",
            what_would_resolve_it="   ",
            standing=ConflictStanding.THE_TREE_CANNOT_TEST_IT,
        )


def test_the_inverted_claims_are_recorded_as_rederived_opposites() -> None:
    inverted = [
        conflict
        for conflict in HOLLOW_ROOT_CONFLICTS
        if conflict.standing is ConflictStanding.THE_TREE_REDERIVED_THE_OPPOSITE
    ]
    assert len(inverted) == 3


def test_the_mudari_limit_is_recorded_as_predating_the_claim() -> None:
    restated = [
        conflict
        for conflict in HOLLOW_ROOT_CONFLICTS
        if conflict.standing
        is ConflictStanding.THE_CLAIM_RESTATES_A_LIMIT_ALREADY_RECORDED_HERE
    ]
    assert len(restated) == 1
    assert "gflk_arabic_letter_specification" in restated[0].tree_reference


def test_every_corpus_number_is_recorded_as_not_rederivable() -> None:
    assert HOLLOW_ROOT_NUMERIC_CLAIMS
    for claim in HOLLOW_ROOT_NUMERIC_CLAIMS:
        assert claim.not_rederivable_because.strip()
        assert claim.what_would_make_it_rederivable.strip()


def test_the_two_contradictory_source_digests_are_both_recorded() -> None:
    quoted = " ".join(claim.claim_text for claim in HOLLOW_ROOT_NUMERIC_CLAIMS)
    assert "3763" in quoted
    figures = {claim.figure for claim in HOLLOW_ROOT_NUMERIC_CLAIMS}
    assert "2b95f2d1" in figures


def test_every_convergence_states_what_it_does_not_establish() -> None:
    assert HOLLOW_ROOT_CONVERGENCES
    for convergence in HOLLOW_ROOT_CONVERGENCES:
        assert convergence.what_it_does_not_establish.strip()


def test_no_submitted_freeze_identifier_is_copied_into_this_deposit() -> None:
    """المُعرِّفُ الوارد مُسجَّلٌ في وحدة إيداعه وحدَها؛ وتكرارُه يجعله شاهدين."""

    import pathlib

    source = (
        pathlib.Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "hollow_root_levels_deposit.py"
    ).read_text(encoding="utf-8")
    from alghanem.arabic.gflk_specification_deposit import (
        SUBMITTED_FREEZE_IDENTIFIERS,
    )

    for submitted in SUBMITTED_FREEZE_IDENTIFIERS:
        assert submitted.identifier not in source
    assert "gflk_specification_deposit" in source


def test_the_named_residuals_are_present() -> None:
    assert HOLLOW_ROOT_DEPOSIT_NAMED_RESIDUALS
    assert all(note.strip() for note in HOLLOW_ROOT_DEPOSIT_NAMED_RESIDUALS)


def test_the_three_modules_read_no_kernel_authority() -> None:
    import pathlib

    root = pathlib.Path(__file__).resolve().parents[2] / "src" / "alghanem" / "arabic"
    for name in (
        "hollow_root_levels_preregistration.py",
        "hollow_root_levels_measurement.py",
        "hollow_root_levels_deposit.py",
    ):
        source = (root / name).read_text(encoding="utf-8")
        imports = tuple(
            line
            for line in source.splitlines()
            if line.startswith(("import ", "from "))
        )
        assert imports, name
        assert not any("kernel" in line for line in imports), name


def test_no_kernel_module_reads_the_hollow_root_ladder() -> None:
    import pathlib
    import pkgutil

    import alghanem.kernel as kernel_package

    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = pathlib.Path(spec.origin).read_text(encoding="utf-8")
        assert "hollow_root_levels" not in text, module.name
