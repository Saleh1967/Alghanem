"""اختباراتُ معيار مجرّد/مزيد: تسجيلُه القبْليُّ، وأداتُه، وحدودُها المُعلَنة."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from alghanem.arabic.jarad_mazid import (
    JARAD_MAZID_NAMED_RESIDUALS,
    JaradMazidError,
    JaradMazidReading,
    RootMatch,
    RootMatchKind,
    SlotCount,
    classify_slot_count,
    consonant_skeleton,
    match_roots,
    read_jarad_mazid,
    root_skeletons,
)
from alghanem.arabic.jarad_mazid_preregistration import (
    CORPUS_BUCKET_RULES,
    MAZID_MINIMUM_SLOTS,
    MUJARRAD_SLOT_COUNT,
    PREREGISTRATION_DIGEST,
    CorpusBucketRule,
    JaradMazidPreregistrationError,
    PublicationPrerequisite,
    bucket_named,
    layer_registration,
    root_table_reference,
)
from alghanem.arabic.maqayis_root_table_deposit import FROZEN_ROOT_TABLE
from alghanem.arabic.p_extractor import read_surface
from alghanem.arabic.word_structure_dictionary_preregistration import (
    DictionaryLayer,
    LayerEpistemicStanding,
)

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src"


def _roots() -> tuple[tuple[str, ...], ...]:
    return root_skeletons()


class TestPreregistration:
    def test_the_slot_thresholds_are_frozen_and_adjacent(self) -> None:
        assert MUJARRAD_SLOT_COUNT == 3
        assert MAZID_MINIMUM_SLOTS == MUJARRAD_SLOT_COUNT + 1

    def test_the_four_buckets_are_closed_and_named(self) -> None:
        assert len(CORPUS_BUCKET_RULES) == 4
        names = [bucket.name for bucket in CORPUS_BUCKET_RULES]
        assert len(set(names)) == 4
        for name in names:
            assert bucket_named(name).name == name

    def test_an_unknown_bucket_is_refused_not_invented(self) -> None:
        with pytest.raises(JaradMazidPreregistrationError):
            bucket_named("MUJARRAD_CERTAIN")

    def test_no_deposited_figure_may_be_marked_adopted(self) -> None:
        with pytest.raises(JaradMazidPreregistrationError):
            CorpusBucketRule(
                name="X",
                counting_rule="قاعدة",
                deposited_figure="1",
                is_adopted=True,
            )

    def test_every_publication_prerequisite_is_registered(self) -> None:
        assert len(PublicationPrerequisite) == 4

    def test_the_root_table_reference_is_read_not_retyped(self) -> None:
        assert root_table_reference() == FROZEN_ROOT_TABLE.sha256_hex

    def test_the_jarad_layer_is_still_withheld(self) -> None:
        registration = layer_registration()
        assert registration.layer is DictionaryLayer.JARAD_ANALYSIS
        assert registration.standing in set(LayerEpistemicStanding)
        assert registration.refusal_field_name

    def test_the_digest_is_stable_across_calls(self) -> None:
        from alghanem.arabic.jarad_mazid_preregistration import preregistration_digest

        assert preregistration_digest() == PREREGISTRATION_DIGEST
        assert len(PREREGISTRATION_DIGEST) == 64


class TestSkeleton:
    def test_a_sound_trilateral_reads_as_three_slots(self) -> None:
        skeleton = consonant_skeleton(read_surface("كَتَبَ"))
        assert skeleton == ("ك", "ت", "ب")
        assert classify_slot_count(skeleton) is SlotCount.MUJARRAD

    def test_a_madd_fills_a_slot_rather_than_being_dropped(self) -> None:
        skeleton = consonant_skeleton(read_surface("كِتَابٌ"))
        assert skeleton == ("ك", "ت", "ا", "ب")
        assert classify_slot_count(skeleton) is SlotCount.MAZID

    def test_the_tanween_carrier_alif_is_not_a_slot(self) -> None:
        assert consonant_skeleton(read_surface("نَارًا")) == ("ن", "ا", "ر")

    def test_a_too_short_skeleton_is_named_not_coerced(self) -> None:
        assert classify_slot_count(("ب", "ت")) is SlotCount.TOO_SHORT_TO_CLASSIFY

    def test_the_slot_count_is_derived_from_the_skeleton(self) -> None:
        reading = read_jarad_mazid("كَتَبَ", roots=_roots())
        assert reading.slots == len(reading.skeleton)


class TestMatching:
    def test_an_exact_skeleton_match_is_named_as_such(self) -> None:
        reading = read_jarad_mazid("كَتَبَ", roots=_roots())
        assert reading.exact_matches
        assert all(
            match.kind is RootMatchKind.EXACT_SKELETON
            for match in reading.exact_matches
        )
        assert "كتب" in {match.root for match in reading.exact_matches}

    def test_a_longer_word_matches_only_as_an_ordered_subsequence(self) -> None:
        reading = read_jarad_mazid("كِتَابٌ", roots=_roots())
        assert not reading.exact_matches
        assert any(
            match.root == "كتب" and match.kind is RootMatchKind.ORDERED_SUBSEQUENCE
            for match in reading.matches
        )

    def test_a_prefix_is_never_reported_as_an_exact_skeleton(self) -> None:
        roots = _roots()
        assert ("ك", "ت", "ب") in roots
        matches = match_roots(("ك", "ت", "ب", "ر"), roots=roots)
        assert all(
            len(match.root) == 4
            for match in matches
            if match.kind is RootMatchKind.EXACT_SKELETON
        )
        assert any(
            match.root == "كتب" and match.kind is RootMatchKind.ORDERED_SUBSEQUENCE
            for match in matches
        )

    def test_an_empty_skeleton_is_refused_not_matched(self) -> None:
        with pytest.raises(JaradMazidError):
            match_roots((), roots=_roots())

    def test_the_root_table_is_read_through_its_digest_check(self) -> None:
        with pytest.raises(Exception):
            root_skeletons(Path(__file__))

    def test_a_reading_carries_the_digest_of_the_criterion_it_used(self) -> None:
        reading = read_jarad_mazid("كَتَبَ", roots=_roots())
        assert reading.preregistration_digest == PREREGISTRATION_DIGEST

    def test_a_reading_under_another_criterion_is_refused(self) -> None:
        with pytest.raises(JaradMazidError):
            JaradMazidReading(
                surface="كتب",
                skeleton=("ك", "ت", "ب"),
                slot_count=SlotCount.MUJARRAD,
                preregistration_digest="0" * 64,
            )

    def test_a_match_kind_must_belong_to_the_closed_vocabulary(self) -> None:
        with pytest.raises(JaradMazidError):
            RootMatch(root="كتب", kind="exact")  # type: ignore[arg-type]


class TestStructuralLimits:
    def test_the_match_kinds_stay_closed_at_two(self) -> None:
        assert len(RootMatchKind) == 2

    def test_the_slot_counts_stay_closed_at_three(self) -> None:
        assert len(SlotCount) == 3

    def test_no_reading_field_names_a_weak_letter_identity(self) -> None:
        fields = set(JaradMazidReading.__dataclass_fields__)
        for forbidden in ("weak_letter", "is_original", "is_augmented", "wazn"):
            assert forbidden not in fields

    def test_no_module_in_the_tree_names_a_prefix_match_kind(self) -> None:
        offenders: list[str] = []
        for path in _SOURCE_ROOT.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == "RootMatchKind":
                    for statement in node.body:
                        if isinstance(statement, ast.Assign):
                            for target in statement.targets:
                                if (
                                    isinstance(target, ast.Name)
                                    and "PREFIX" in target.id
                                ):
                                    offenders.append(f"{path}:{target.id}")
        assert offenders == []

    def test_the_named_residuals_are_sorted_and_unique(self) -> None:
        assert list(JARAD_MAZID_NAMED_RESIDUALS) == sorted(JARAD_MAZID_NAMED_RESIDUALS)
        assert len(set(JARAD_MAZID_NAMED_RESIDUALS)) == len(JARAD_MAZID_NAMED_RESIDUALS)

    def test_the_module_issues_no_corpus_figure(self) -> None:
        import alghanem.arabic.jarad_mazid as module

        for figure in ("10599", "11467", "37682", "18333"):
            assert figure not in Path(module.__file__ or "").read_text(encoding="utf-8")
