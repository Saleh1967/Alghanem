"""اختباراتُ تسجيل المراحل المحجوبة: أسماءٌ ومَوانِع، ولا أرقامَ عابرةً للحجب."""

from __future__ import annotations

import pytest

from alghanem.arabic.gflk_feature_table_import_barrier import (
    FEATURE_TABLE_IMPORT_BARRIERS,
    ImportBarrierStanding,
)
from alghanem.arabic.gflk_milestone_blocking_registration import (
    BLOCKED_MILESTONES,
    MILESTONE_BLOCKING_NAMED_RESIDUALS,
    OPEN_QUESTIONS,
    REGISTRATION_DIGEST,
    BlockedMilestone,
    BlockKind,
    MilestoneBlockingError,
    milestone_named,
    question_named,
    registration_digest,
)


class TestBlockedMilestones:
    def test_the_four_unbuilt_milestones_are_named(self) -> None:
        identifiers = {milestone.identifier for milestone in BLOCKED_MILESTONES}
        assert identifiers == {
            "C_FEATURE_TABLES",
            "F_OCP_TEST",
            "G_TREE_BIT_ENCODING",
            "H_COMPRESSION_LADDER",
        }

    def test_every_milestone_names_an_existing_open_question(self) -> None:
        known = {question.identifier for question in OPEN_QUESTIONS}
        for milestone in BLOCKED_MILESTONES:
            assert milestone.open_question_identifiers
            for identifier in milestone.open_question_identifiers:
                assert identifier in known
                assert question_named(identifier).question

    def test_every_milestone_states_what_would_unblock_it(self) -> None:
        for milestone in BLOCKED_MILESTONES:
            assert milestone.what_would_unblock_it.strip()
            assert milestone.blocking_input.strip()

    def test_a_milestone_without_an_open_question_is_refused(self) -> None:
        with pytest.raises(MilestoneBlockingError):
            BlockedMilestone(
                identifier="X",
                title="ع",
                blocking_input="م",
                kind=BlockKind.SCOPE_DECISION_NOT_TAKEN,
                what_would_unblock_it="ش",
                open_question_identifiers=(),
            )

    def test_an_unknown_milestone_is_refused_not_invented(self) -> None:
        with pytest.raises(MilestoneBlockingError):
            milestone_named("A_P_EXTRACTOR")

    def test_an_unknown_question_is_refused_not_invented(self) -> None:
        with pytest.raises(MilestoneBlockingError):
            question_named("WHEN_WILL_IT_BE_DONE")


class TestStructuralLimits:
    def test_the_block_kinds_stay_closed_at_three(self) -> None:
        assert len(BlockKind) == 3

    def test_no_milestone_carries_a_result_field(self) -> None:
        fields = set(BlockedMilestone.__dataclass_fields__)
        for forbidden in ("result", "outcome", "resolution", "verdict", "confidence"):
            assert forbidden not in fields

    def test_the_deposited_figures_are_listed_as_not_carried_across(self) -> None:
        carried: set[str] = set()
        for milestone in BLOCKED_MILESTONES:
            carried.update(milestone.figures_not_carried_across)
        assert {"88.34%", "18.75%", "23.2%", "p≈0.027"} <= carried

    def test_the_import_barriers_are_still_open(self) -> None:
        assert FEATURE_TABLE_IMPORT_BARRIERS
        for barrier in FEATURE_TABLE_IMPORT_BARRIERS:
            assert barrier.standing is ImportBarrierStanding.OPEN

    def test_the_named_residuals_are_sorted_and_unique(self) -> None:
        assert list(MILESTONE_BLOCKING_NAMED_RESIDUALS) == sorted(
            MILESTONE_BLOCKING_NAMED_RESIDUALS
        )
        assert len(set(MILESTONE_BLOCKING_NAMED_RESIDUALS)) == len(
            MILESTONE_BLOCKING_NAMED_RESIDUALS
        )

    def test_the_digest_is_stable_across_calls(self) -> None:
        assert registration_digest() == REGISTRATION_DIGEST
        assert len(REGISTRATION_DIGEST) == 64
