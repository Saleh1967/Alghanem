"""اختباراتُ عقدِ إيداع الطبعة: شرطُ الصفحة، والحسمُ قبل الاستيراد، وفرقٌ مُشتَقّ."""

from __future__ import annotations

import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.classical_makharij_table import (
    CLASSICAL_MAKHARIJ,
    CLASSICAL_ORDERING_IS_NOT_EDITION_CITED_NOTE,
    JAWF_AND_KHAYSHUM_ARE_UNRANKED_NOTE,
    ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP_NOTE,
)
from alghanem.arabic.gflk_feature_table_import_barrier import (
    FEATURE_TABLE_IMPORT_BARRIERS,
    ImportBarrierStanding,
)
from alghanem.arabic.makharij_edition_citation import (
    ATTESTED_REGION_COUNTS,
    ATTESTED_TOTAL_MAKHARIJ,
    DEPOSITED_EDITION_ORDERINGS,
    DIVISION_DIFFERENCES,
    MAKHARIJ_EDITION_NAMED_RESIDUALS,
    MAKHARIJ_EDITION_REGISTRATION_DIGEST,
    SCOPE_RESOLUTION,
    UNRANKED_DECLARED_MAKHARIJ,
    AttestedRegionCount,
    DepositedEditionOrdering,
    EditionCitation,
    MakharijEditionError,
    MakhrajRegion,
    RankDifference,
    RegionCountDifference,
    ScopeResolution,
    ScopeResolutionRecord,
    compare_to_frozen_table,
    derive_division_differences,
    derive_frozen_region_counts,
    edition_matches_the_frozen_table,
    frozen_ranked_makhraj_count,
    makharij_edition_registration_digest,
    region_of_makhraj_name,
)
from alghanem.arabic.phonetic_economy_candidate import (
    PHONETIC_ECONOMY_CANDIDATE,
    ChainVerdict,
    ClosureOutcome,
)

_A_CITATION = EditionCitation(
    work_title="كتابٌ مفترضٌ للاختبار",
    editor="محقّقٌ مفترض",
    publisher="ناشرٌ مفترض",
    edition_year="١٤٠٠هـ",
    volume="١",
    page="٥",
    deposited_quotation="اقتباسٌ مفترضٌ لا يُقرأ نسبةً إلى طبعةٍ قائمة",
)


def _ordering_from(rows: tuple[tuple[int, str, str], ...]) -> DepositedEditionOrdering:
    return DepositedEditionOrdering(citation=_A_CITATION, rows=rows)


class TestTheEditionCitationContract:
    @pytest.mark.parametrize(
        "field_name",
        (
            "work_title",
            "editor",
            "publisher",
            "edition_year",
            "volume",
            "page",
            "deposited_quotation",
        ),
    )
    def test_every_field_is_a_construction_condition(self, field_name: str) -> None:
        values = dict(_A_CITATION.as_canonical_content())
        values[field_name] = "   "
        with pytest.raises(MakharijEditionError):
            EditionCitation(**values)

    def test_no_edition_has_been_deposited_today(self) -> None:
        assert DEPOSITED_EDITION_ORDERINGS == ()

    def test_the_deposited_digest_is_rederived_from_the_bytes(self) -> None:
        ordering = _ordering_from(tuple(CLASSICAL_MAKHARIJ))
        assert ordering.rederive_edition_digest() == ordering.rederive_edition_digest()
        other = _ordering_from(tuple(CLASSICAL_MAKHARIJ[:-1]))
        assert other.rederive_edition_digest() != ordering.rederive_edition_digest()

    def test_a_gap_in_the_ranking_is_refused(self) -> None:
        with pytest.raises(MakharijEditionError):
            _ordering_from(((1, "أقصى الحلق", "ءه"), (3, "أدنى الحلق", "غخ")))

    def test_one_letter_in_two_makharij_is_refused(self) -> None:
        with pytest.raises(MakharijEditionError):
            _ordering_from(((1, "أوّل", "ءه"), (2, "ثانٍ", "هع")))


class TestTheComparisonIsRunNotClaimed:
    def test_an_identical_ordering_matches_rank_by_rank(self) -> None:
        ordering = _ordering_from(tuple(CLASSICAL_MAKHARIJ))
        assert compare_to_frozen_table(ordering) == ()
        assert edition_matches_the_frozen_table(ordering)

    def test_a_differing_letter_is_reported_at_its_rank(self) -> None:
        rows = tuple(CLASSICAL_MAKHARIJ[:14]) + ((15, "الشفتان", "بمو"),)
        ordering = _ordering_from(rows)
        differences = compare_to_frozen_table(ordering)
        assert not edition_matches_the_frozen_table(ordering)
        by_rank = {item.rank: item for item in differences}
        assert by_rank[15].edition_letters == "بمو"
        assert by_rank[15].frozen_letters == "بم"
        assert by_rank[16].edition_letters is None
        assert by_rank[16].frozen_letters == "و"

    def test_a_difference_without_a_difference_is_refused(self) -> None:
        with pytest.raises(MakharijEditionError):
            RankDifference(rank=1, edition_letters="ءه", frozen_letters="ءه")

    def test_the_comparison_refuses_a_foreign_argument(self) -> None:
        with pytest.raises(MakharijEditionError):
            compare_to_frozen_table(CLASSICAL_MAKHARIJ)  # type: ignore[arg-type]


class TestTheFrozenTableAgainstItsOwnAttestation:
    def test_every_attested_count_quotes_the_attestation_verbatim(self) -> None:
        assert ATTESTED_REGION_COUNTS
        for attested in ATTESTED_REGION_COUNTS:
            assert attested.quoted_phrase.strip()

    def test_a_count_without_its_quotation_is_refused(self) -> None:
        with pytest.raises(MakharijEditionError):
            AttestedRegionCount(
                region=MakhrajRegion.LIPS,
                quoted_phrase="الشفتان ثلاثة",
                attested_count=3,
            )

    def test_the_region_counts_are_derived_from_the_frozen_bytes(self) -> None:
        counts = derive_frozen_region_counts()
        assert counts[MakhrajRegion.THROAT] == 3
        assert counts[MakhrajRegion.TONGUE] == 10
        assert counts[MakhrajRegion.LIPS] == 3
        assert sum(counts.values()) == frozen_ranked_makhraj_count()

    def test_the_surplus_is_exactly_one_and_sits_at_the_lips(self) -> None:
        assert DIVISION_DIFFERENCES == derive_division_differences()
        assert len(DIVISION_DIFFERENCES) == 1
        difference = DIVISION_DIFFERENCES[0]
        assert difference.region is MakhrajRegion.LIPS
        assert difference.attested_count == 2
        assert difference.frozen_count == 3
        assert tuple(rank for rank, _n, _l in difference.frozen_rows) == (14, 15, 16)

    def test_the_attested_total_minus_the_unranked_two_is_not_the_frozen_count(
        self,
    ) -> None:
        expected_ranked = ATTESTED_TOTAL_MAKHARIJ - len(UNRANKED_DECLARED_MAKHARIJ)
        assert expected_ranked == 15
        assert frozen_ranked_makhraj_count() - expected_ranked == 1

    def test_an_ambiguous_makhraj_name_is_refused_not_guessed(self) -> None:
        with pytest.raises(MakharijEditionError):
            region_of_makhraj_name("طرفُ اللسان مع باطن الشفة السفلى")
        with pytest.raises(MakharijEditionError):
            region_of_makhraj_name("الخيشوم")

    def test_a_region_difference_without_a_difference_is_refused(self) -> None:
        with pytest.raises(MakharijEditionError):
            RegionCountDifference(
                region=MakhrajRegion.THROAT,
                attested_count=3,
                frozen_count=3,
                quoted_phrase="الحلقُ ثلاثة",
                frozen_rows=((1, "أقصى الحلق", "ءه"),),
            )


class TestTheConflictIsResolvedBeforeTheImport:
    def test_the_scope_decision_is_recorded_as_not_taken(self) -> None:
        assert SCOPE_RESOLUTION.resolution is ScopeResolution.NOT_TAKEN
        assert not SCOPE_RESOLUTION.is_taken
        assert SCOPE_RESOLUTION.why_it_stands_here.strip()
        assert len(SCOPE_RESOLUTION.admissible_resolutions) == 2

    def test_not_taken_is_not_admissible_as_a_resolution(self) -> None:
        with pytest.raises(MakharijEditionError):
            ScopeResolutionRecord(
                resolution=ScopeResolution.NOT_TAKEN,
                admissible_resolutions=(
                    ScopeResolution.NOT_TAKEN,
                    ScopeResolution.RESTATE_THE_SPECIFICATION_ON_THE_FROZEN_SIXTEEN,
                ),
                open_question_identifier="THIRTEEN_VERSUS_SIXTEEN_MAKHARIJ",
                why_it_stands_here="نصٌّ غير فارغ",
            )

    def test_the_record_must_name_an_existing_open_question(self) -> None:
        with pytest.raises(Exception):
            ScopeResolutionRecord(
                resolution=ScopeResolution.NOT_TAKEN,
                admissible_resolutions=(
                    ScopeResolution.RESTATE_THE_SPECIFICATION_ON_THE_FROZEN_SIXTEEN,
                    ScopeResolution.IMPORT_THE_THIRTEEN_AS_A_SECOND_ATTRIBUTED_TABLE,
                ),
                open_question_identifier="NO_SUCH_QUESTION",
                why_it_stands_here="نصٌّ غير فارغ",
            )


class TestNothingElseIsLiftedByThis:
    def test_both_import_barriers_stay_open(self) -> None:
        assert FEATURE_TABLE_IMPORT_BARRIERS
        for barrier in FEATURE_TABLE_IMPORT_BARRIERS:
            assert barrier.standing is ImportBarrierStanding.OPEN
            assert barrier.what_lifts_it.strip()

    def test_the_three_classical_table_residuals_stand_unchanged(self) -> None:
        assert CLASSICAL_ORDERING_IS_NOT_EDITION_CITED_NOTE.startswith(
            "CLASSICAL_ORDERING_NOT_EDITION_CITED:"
        )
        assert ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP_NOTE.startswith(
            "ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP:"
        )
        assert JAWF_AND_KHAYSHUM_ARE_UNRANKED_NOTE.startswith(
            "JAWF_AND_KHAYSHUM_UNRANKED:"
        )

    def test_the_recorded_card_is_untouched(self) -> None:
        assert PHONETIC_ECONOMY_CANDIDATE.verdict is ChainVerdict.DEFER_IN_SCOPE
        assert PHONETIC_ECONOMY_CANDIDATE.closure_check.outcome is ClosureOutcome.FAIL


class TestRegistrationNotAuthority:
    def test_the_digest_is_rederived_at_import(self) -> None:
        assert MAKHARIJ_EDITION_REGISTRATION_DIGEST == (
            makharij_edition_registration_digest()
        )
        assert len(MAKHARIJ_EDITION_REGISTRATION_DIGEST) == 64

    def test_the_named_residuals_are_sorted_and_complete(self) -> None:
        assert list(MAKHARIJ_EDITION_NAMED_RESIDUALS) == sorted(
            MAKHARIJ_EDITION_NAMED_RESIDUALS
        )
        assert len(set(MAKHARIJ_EDITION_NAMED_RESIDUALS)) == len(
            MAKHARIJ_EDITION_NAMED_RESIDUALS
        )

    def test_no_type_here_carries_a_verdict_or_birth_field(self) -> None:
        for declaring_type in (
            EditionCitation,
            DepositedEditionOrdering,
            RankDifference,
            RegionCountDifference,
            ScopeResolutionRecord,
            AttestedRegionCount,
        ):
            declared = {item.name for item in fields(declaring_type)}
            for marker in ("verdict", "birth", "result", "outcome", "certified"):
                assert not any(marker in name for name in declared), marker

    def test_the_module_reads_no_kernel_authority(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "alghanem"
            / "arabic"
            / "makharij_edition_citation.py"
        ).read_text(encoding="utf-8")
        imports = tuple(
            line
            for line in source.splitlines()
            if line.startswith(("import ", "from "))
        )
        assert imports
        assert not any("kernel" in line for line in imports)

    def test_no_kernel_module_reads_this_registration(self) -> None:
        for module in pkgutil.walk_packages(
            kernel_package.__path__, prefix="alghanem.kernel."
        ):
            spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
            assert spec is not None and spec.origin is not None
            text = Path(spec.origin).read_text(encoding="utf-8")
            assert "makharij_edition_citation" not in text, module.name
            assert "DepositedEditionOrdering" not in text, module.name
