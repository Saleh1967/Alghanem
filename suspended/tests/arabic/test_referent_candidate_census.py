"""اختباراتُ حصرِ المرشَّحين وإحصائه، بأسطرٍ مُصرَّحٍ باصطناعها لا مدوَّنةً.

`SyntheticLinesAreDeclaredNotHidden`: الصفوفُ هنا **مُصطنَعة**، تُحاكي بنيةَ
الصفّ وحدَها، وصورُها مكتوبةٌ بأحرفها لتُقرأ قاعدةُ الاستنتاج عليها؛ ولا يخرج
منها رقمٌ عن MASAQ البتّة. وما يُقاس من البايتات المُبصَّمة مكانُه اختبارُ
التسجيل المُعلَّق، لا هذا الملفّ.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.irab_column_census import SURA_COLUMN, VERSE_COLUMN
from alghanem.arabic.irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
    WORD_KEY_COLUMN_NAME,
)
from alghanem.arabic.masaq_corpus_deposit import MORPH_TAG_COLUMN
from alghanem.arabic.referent_candidate_census import (
    REFERENT_CANDIDATE_CENSUS_NAMED_RESIDUALS,
    CandidateSetCensus,
    CandidateStanding,
    ReferentCandidateCensusError,
    candidates_for,
    enumerate_candidate_sets,
    measure_candidates,
    nominal_positions,
    pronoun_positions,
    refuse_gold_fields,
    size_by_constraint,
)
from alghanem.arabic.referent_candidate_preregistration import (
    SEGMENTED_WORD_COLUMN,
    STEM_MORPH_TYPE,
)

MUMINUN = "\u0645\u0624\u0645\u0646\u0648\u0646"
"""«مؤمنون»: صورةٌ تُقرأ جمعًا مذكّرًا سالمًا بالقاعدة المُعلَنة."""

MALIKA = "\u0645\u0644\u0643\u0629"
"""«ملكة»: صورةٌ تُقرأ مفردًا مؤنّثًا بتاء التأنيث."""

RIJAL = "\u0631\u062c\u0627\u0644"
"""«رجال»: جمعُ تكسيرٍ خارجَ مقدور القاعدة، فيُعَدُّ عجزًا لا يُطابَق به."""


def _row(
    *,
    sura: str = "2",
    verse: str = "5",
    word: str = "1",
    segment: str = "1",
    morph_type: str = STEM_MORPH_TYPE,
    tag: str = "NOUN",
    surface: str = "",
) -> dict[str, str]:
    """صفٌّ مُصطنَعٌ واحد؛ بنيةً لا مدوَّنة."""

    return {
        SURA_COLUMN: sura,
        VERSE_COLUMN: verse,
        ANCHOR_COLUMN_NAME: morph_type,
        MORPH_TAG_COLUMN: tag,
        WORD_KEY_COLUMN_NAME: word,
        SEGMENT_INDEX_COLUMN_NAME: segment,
        SEGMENTED_WORD_COLUMN: surface,
    }


def _noun(
    *, sura: str = "2", verse: str = "5", word: str, surface: str
) -> dict[str, str]:
    return _row(sura=sura, verse=verse, word=word, tag="NOUN", surface=surface)


def _pronoun(
    *, sura: str = "2", verse: str = "5", word: str, tag: str
) -> dict[str, str]:
    return _row(sura=sura, verse=verse, word=word, morph_type="Suffix", tag=tag)


def test_a_missing_column_stops_the_count() -> None:
    """عمودٌ غائبٌ يُوقِف العدَّ ولا يُصفِّره ولا يُحمَل على أقرب اسمٍ إليه."""

    with pytest.raises(ReferentCandidateCensusError):
        pronoun_positions([])
    row = _row()
    del row[SEGMENTED_WORD_COLUMN]
    with pytest.raises(ReferentCandidateCensusError):
        pronoun_positions([row])


def test_an_aggregate_tag_is_counted_unparsed_not_given_a_constraint() -> None:
    """وسمٌ مُجمَّلٌ يُعَدُّ في `unparsed_tags` ولا يدخل مقامًا بقيدٍ مُخمَّن."""

    records = [
        _pronoun(word="2", tag="SUBJ_PRON"),
        _pronoun(word="3", tag="POSS_PRON"),
        _pronoun(word="4", tag="PRON_3MP"),
    ]
    positions, unparsed, unreadable = pronoun_positions(records)
    assert len(positions) == 1
    assert positions[0].tag == "PRON_3MP"
    assert unparsed == 2
    assert unreadable == 0


def test_an_unreadable_position_is_counted_not_dropped() -> None:
    """موضعٌ لا يُقرأ عددًا يُعَدُّ في حقلٍ باسمه ولا يدخل ترتيبًا ولا نافذة."""

    records = [
        _pronoun(word="لا-عدد", tag="PRON_3MP"),
        _pronoun(word="2", tag="PRON_3MP"),
    ]
    positions, unparsed, unreadable = pronoun_positions(records)
    assert len(positions) == 1
    assert unparsed == 0
    assert unreadable == 1


def test_the_window_does_not_reach_beyond_the_preceding_verse() -> None:
    """اسمٌ في الآية قبل السابقة لا يدخل، والنافذةُ لا تُوسَّع بعد النتيجة."""

    records = [
        _noun(verse="3", word="1", surface=MUMINUN),
        _noun(verse="4", word="1", surface=MUMINUN),
        _pronoun(verse="5", word="2", tag="PRON_3MP"),
    ]
    pronouns, _unparsed, _unreadable = pronoun_positions(records)
    nominals, _undetermined, _rows = nominal_positions(records)
    found = candidates_for(pronouns[0], nominals)
    assert [nominal.position.verse for nominal in found] == [4]


def test_the_window_does_not_cross_the_sura_boundary() -> None:
    """اسمٌ في سورةٍ أخرى لا يدخل ولو كانت آيتُه سابقةً بالرقم."""

    records = [
        _noun(sura="1", verse="4", word="1", surface=MUMINUN),
        _pronoun(sura="2", verse="5", word="2", tag="PRON_3MP"),
    ]
    pronouns, _unparsed, _unreadable = pronoun_positions(records)
    nominals, _undetermined, _rows = nominal_positions(records)
    assert candidates_for(pronouns[0], nominals) == ()


def test_a_noun_after_the_pronoun_is_not_a_candidate() -> None:
    """ما بعد الضمير ليس مرشَّحًا؛ فالنافذةُ سابقةٌ لا محيطة."""

    records = [
        _pronoun(verse="5", word="2", tag="PRON_3MP"),
        _noun(verse="5", word="3", surface=MUMINUN),
    ]
    pronouns, _unparsed, _unreadable = pronoun_positions(records)
    nominals, _undetermined, _rows = nominal_positions(records)
    assert candidates_for(pronouns[0], nominals) == ()


def test_the_host_word_is_not_its_own_candidate() -> None:
    """الجذعُ في كلمة الضمير نفسِها يخرج بقاعدةٍ مُعلَنة، لا بصمتٍ عنه."""

    records = [
        _noun(verse="5", word="2", surface=MUMINUN),
        _row(
            verse="5",
            word="2",
            segment="2",
            morph_type="Suffix",
            tag="POSS_PRON_3MP",
        ),
        _noun(verse="4", word="1", surface=MUMINUN),
    ]
    pronouns, _unparsed, _unreadable = pronoun_positions(records)
    nominals, _undetermined, _rows = nominal_positions(records)
    found = candidates_for(pronouns[0], nominals)
    assert [nominal.position.verse for nominal in found] == [4]


def test_a_discourse_participant_leaves_the_nominal_matching() -> None:
    """المتكلّمُ والمخاطَبُ يخرجان قبل أيّ بحثٍ ولو حضر اسمٌ موافقٌ تمامًا."""

    for tag in ("PRON_1S", "PRON_2MP"):
        records = [
            _noun(verse="5", word="1", surface=MALIKA),
            _noun(verse="5", word="2", surface=MUMINUN),
            _pronoun(verse="5", word="3", tag=tag),
        ]
        pronouns, _unparsed, _unreadable = pronoun_positions(records)
        nominals, _undetermined, _rows = nominal_positions(records)
        assert candidates_for(pronouns[0], nominals) == ()
        sets, _u, _r, _n = enumerate_candidate_sets(records)
        assert sets[0].standing is CandidateStanding.DISCOURSE_PARTICIPANT


def test_an_undetermined_inference_is_not_a_match_and_is_counted() -> None:
    """اسمٌ عجزت عنه القاعدةُ لا يُقبَل مرشَّحًا ولا يُسقَط صامتًا، بل يُعَدّ."""

    records = [
        _noun(verse="5", word="1", surface=RIJAL),
        _pronoun(verse="5", word="2", tag="PRON_3MP"),
    ]
    nominals, undetermined, _rows = nominal_positions(records)
    assert len(nominals) == 1
    assert undetermined == 1
    pronouns, _unparsed, _unreadable = pronoun_positions(records)
    assert candidates_for(pronouns[0], nominals) == ()


def test_gender_and_number_must_both_agree() -> None:
    """المطابقةُ في العدد والجنس معًا؛ ومخالفُ أحدِهما ليس مرشَّحًا."""

    records = [
        _noun(verse="5", word="1", surface=MALIKA),
        _noun(verse="5", word="2", surface=MUMINUN),
        _pronoun(verse="5", word="3", tag="PRON_3MP"),
    ]
    pronouns, _unparsed, _unreadable = pronoun_positions(records)
    nominals, _undetermined, _rows = nominal_positions(records)
    found = candidates_for(pronouns[0], nominals)
    assert [nominal.position.word_number for nominal in found] == [2]


def test_an_unspecified_gender_constraint_matches_on_number_alone() -> None:
    """قيدٌ جنسُه «غيرُ محدَّد» يُطابِق على العدد وحدَه، مُعلَنًا لا مُخمَّنًا."""

    records = [
        _noun(verse="5", word="1", surface=MALIKA),
        _noun(verse="5", word="2", surface=MUMINUN),
        _pronoun(verse="5", word="3", tag="PRON_3D"),
    ]
    pronouns, _unparsed, _unreadable = pronoun_positions(records)
    nominals, _undetermined, _rows = nominal_positions(records)
    assert candidates_for(pronouns[0], nominals) == ()

    dual = [
        _noun(verse="5", word="1", surface="\u0631\u062c\u0644\u0627\u0646"),
        _noun(verse="5", word="2", surface="\u0645\u0644\u0643\u062a\u0627\u0646"),
        _pronoun(verse="5", word="3", tag="PRON_3D"),
    ]
    pronouns, _unparsed, _unreadable = pronoun_positions(dual)
    nominals, _undetermined, _rows = nominal_positions(dual)
    assert len(candidates_for(pronouns[0], nominals)) == 2


def test_the_three_standings_conserve_the_nominal_denominator() -> None:
    """واحدٌ + متعدّدٌ + صفرٌ = مقامُ المطابقة الاسمية بالضبط، بلا فرقٍ مطويّ."""

    records = [
        _noun(verse="5", word="1", surface=MUMINUN),
        _pronoun(verse="5", word="2", tag="PRON_3MP"),
        _noun(verse="5", word="3", surface=MUMINUN),
        _pronoun(verse="5", word="4", tag="PRON_3MP"),
        _pronoun(verse="5", word="5", tag="PRON_3FS"),
        _pronoun(verse="5", word="6", tag="PRON_1S"),
    ]
    census = measure_candidates(records)
    assert census.denominator == 4
    assert census.standings[CandidateStanding.SINGLE.value] == 1
    assert census.standings[CandidateStanding.MULTIPLE.value] == 1
    assert census.standings[CandidateStanding.NONE.value] == 1
    assert census.standings[CandidateStanding.DISCOURSE_PARTICIPANT.value] == 1
    assert census.nominal_denominator == 3
    assert (
        census.standings[CandidateStanding.SINGLE.value]
        + census.standings[CandidateStanding.MULTIPLE.value]
        + census.standings[CandidateStanding.NONE.value]
        == census.nominal_denominator
    )
    assert sum(census.standings.values()) == census.denominator
    assert census.candidate_total == 3
    assert census.mean_candidate_set_size == pytest.approx(1.0)
    assert census.single_candidate_share == pytest.approx(100.0 / 3)


def test_the_zero_candidate_positions_are_listed_not_aggregated() -> None:
    """مواضعُ «صفر مرشَّح» تُسرَد بمواضعها؛ وعددٌ بلا مواضعَ يُرفَع به خطأ."""

    records = [
        _noun(verse="5", word="1", surface=MALIKA),
        _pronoun(verse="5", word="2", tag="PRON_3MP"),
    ]
    census = measure_candidates(records)
    assert census.zero_candidate_positions == ((2, 5, 2, 1),)

    with pytest.raises(ReferentCandidateCensusError):
        CandidateSetCensus(
            denominator=1,
            standings={
                CandidateStanding.SINGLE.value: 0,
                CandidateStanding.MULTIPLE.value: 0,
                CandidateStanding.NONE.value: 1,
                CandidateStanding.DISCOURSE_PARTICIPANT.value: 0,
            },
            candidate_total=0,
            zero_candidate_positions=(),
            unparsed_tags=0,
            unreadable_pronoun_positions=0,
            undetermined_nominals=0,
            preregistration_digest="d" * 64,
            corpus_digest="c" * 64,
        )


def test_a_broken_conservation_is_refused() -> None:
    """مجموعُ المنازل إن خالف المقامَ رُفِع خطأٌ، ولا يُطوى الفرقُ في منزلة."""

    with pytest.raises(ReferentCandidateCensusError):
        CandidateSetCensus(
            denominator=5,
            standings={
                CandidateStanding.SINGLE.value: 1,
                CandidateStanding.MULTIPLE.value: 1,
                CandidateStanding.NONE.value: 0,
                CandidateStanding.DISCOURSE_PARTICIPANT.value: 0,
            },
            candidate_total=1,
            zero_candidate_positions=(),
            unparsed_tags=0,
            unreadable_pronoun_positions=0,
            undetermined_nominals=0,
            preregistration_digest="d" * 64,
            corpus_digest="c" * 64,
        )
    with pytest.raises(ReferentCandidateCensusError):
        CandidateSetCensus(
            denominator=1,
            standings={CandidateStanding.SINGLE.value: 1},
            candidate_total=1,
            zero_candidate_positions=(),
            unparsed_tags=0,
            unreadable_pronoun_positions=0,
            undetermined_nominals=0,
            preregistration_digest="d" * 64,
            corpus_digest="c" * 64,
        )


def test_a_precision_field_is_refused_not_ignored() -> None:
    """أيُّ حقلٍ يدّعي دقّةً أو استدعاءً أو ذهبًا يُرفَع به خطأٌ في البنية."""

    for name in ("precision", "recall", "f1_score", "gold_referent", "accuracy"):
        with pytest.raises(ReferentCandidateCensusError):
            refuse_gold_fields({name: 1.0})
        with pytest.raises(ReferentCandidateCensusError):
            CandidateSetCensus(
                denominator=0,
                standings={standing.value: 0 for standing in CandidateStanding},
                candidate_total=0,
                zero_candidate_positions=(),
                unparsed_tags=0,
                unreadable_pronoun_positions=0,
                undetermined_nominals=0,
                preregistration_digest="d" * 64,
                corpus_digest="c" * 64,
                extra_fields={name: 1.0},
            )
    refuse_gold_fields({"denominator": 1, "candidate_total": 2})
    assert not any(
        stem in name.lower()
        for name in CandidateSetCensus.__dataclass_fields__
        for stem in ("precision", "recall", "gold", "accuracy")
    )


def test_no_mean_is_taken_over_a_zero_denominator() -> None:
    """لا متوسّطَ ولا نسبةَ بمقامٍ صفر؛ ويُرفَع بها خطأٌ لا تُخرَج صفرًا."""

    census = CandidateSetCensus(
        denominator=1,
        standings={
            CandidateStanding.SINGLE.value: 0,
            CandidateStanding.MULTIPLE.value: 0,
            CandidateStanding.NONE.value: 0,
            CandidateStanding.DISCOURSE_PARTICIPANT.value: 1,
        },
        candidate_total=0,
        zero_candidate_positions=(),
        unparsed_tags=0,
        unreadable_pronoun_positions=0,
        undetermined_nominals=0,
        preregistration_digest="d" * 64,
        corpus_digest="c" * 64,
    )
    assert census.nominal_denominator == 0
    with pytest.raises(ReferentCandidateCensusError):
        _ = census.mean_candidate_set_size
    with pytest.raises(ReferentCandidateCensusError):
        _ = census.single_candidate_share


def test_the_distribution_is_keyed_by_the_whole_triple() -> None:
    """التوزيعُ بالثلاثية كاملةً: شخصٌ وعددٌ وجنسٌ، لا بالوَسْم نصًّا."""

    records = [
        _noun(verse="5", word="1", surface=MUMINUN),
        _pronoun(verse="5", word="2", tag="PRON_3MP"),
        _pronoun(verse="5", word="3", tag="POSS_PRON_3MP"),
        _pronoun(verse="5", word="4", tag="PRON_1S"),
    ]
    sets, _u, _r, _n = enumerate_candidate_sets(records)
    table = size_by_constraint(sets)
    assert table[("3", "P", "M")] == (2, 2)
    assert table[("1", "S", "—")] == (1, 0)


def test_the_census_names_no_referent_and_ranks_nothing() -> None:
    """المرشَّحون بترتيبٍ موضعيٍّ وحدَه؛ ولا دالّةَ تُسمّي مرجعًا ولا تُرجِّح."""

    import alghanem.arabic.referent_candidate_census as module

    exported = set(module.__all__)
    assert not any(
        word in name.lower()
        for name in exported
        for word in ("resolve", "choose", "select", "rank", "best")
    )
    records = [
        _noun(verse="4", word="9", surface=MUMINUN),
        _noun(verse="5", word="1", surface=MUMINUN),
        _pronoun(verse="5", word="2", tag="PRON_3MP"),
    ]
    pronouns, _unparsed, _unreadable = pronoun_positions(records)
    nominals, _undetermined, _rows = nominal_positions(records)
    found = candidates_for(pronouns[0], nominals)
    assert [nominal.position.order_key for nominal in found] == [
        (2, 4, 9, 1),
        (2, 5, 1, 1),
    ]


def test_the_census_named_limits_are_written_inside_the_unit() -> None:
    """حدودُ الإحصاء مكتوبةٌ بأسمائها في الوحدة، لا في وثيقةٍ خارجها."""

    for name in (
        "TheReferentIsNotAnnotatedAnywhere",
        "GenderAndNumberAreInferredNotTagged",
        "ElevenPercentIsTheRealDenominator",
        "ACandidateSetIsNotAnAnswer",
        "APrecisionFieldIsRefusedNotIgnored",
        "FourStandingsAndNoZeroGathersThem",
        "AnUnreadablePositionIsCountedNotDropped",
    ):
        assert name in REFERENT_CANDIDATE_CENSUS_NAMED_RESIDUALS
        assert name in REFERENT_CANDIDATE_CENSUS_NAMED_RESIDUALS[name]
