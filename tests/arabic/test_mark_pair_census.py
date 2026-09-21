"""يختبر عدَّ المزدوجات: ما قِيس على المُودَعَين، وما رُفض عن المدوّنة."""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.mark_pair_census import (
    MARK_PAIR_NAMED_RESIDUALS,
    THE_NINE_MARKS,
    MarkPairError,
    PairCensus,
    PairCount,
    combining_classes_are_all_distinct,
    corpus_run_is_available,
    pair_census_over,
    pair_census_over_corpus,
    possible_pairs,
)

_FATIHA = "\n".join(FATIHA_LINES)
_FATH = FATH_AYAH_SOURCE_TEXT
_SCOPES = (("الفاتحة", _FATIHA), ("الفتح ٢٩", _FATH))

_FATHA = "\u064e"
_DAMMA = "\u064f"
_KASRA = "\u0650"
_SHADDA = "\u0651"
_DAGGER = "\u0670"


def test_the_corpus_bytes_are_absent_from_this_tree() -> None:
    """السؤالُ عن كلّ المدوّنة لا يُجاب ههنا: بايتاتُها ليست في الشجرة."""

    assert corpus_run_is_available() is False


def test_the_corpus_run_refuses_rather_than_estimating() -> None:
    """ولا تُقدَّر المدوّنةُ من المُودَعَين، بل يُرفَض الطلبُ صريحًا."""

    with pytest.raises(Exception) as raised:
        pair_census_over_corpus()
    assert "المدوّنة" in str(raised.value)


def test_the_nine_combining_classes_are_all_distinct() -> None:
    """وتمايزُ الأصنافِ مشتقٌّ من الجدول، وعليه يدور الجوازُ والترتيب."""

    assert combining_classes_are_all_distinct()
    classes = [unicodedata.combining(mark) for mark in THE_NINE_MARKS]
    assert classes == list(range(27, 36))


def test_unicode_forbids_none_of_the_thirty_six_pairs() -> None:
    """فلمّا تمايزت لم يمنع اليونيكودُ مزدوجًا واحدًا من الستّة والثلاثين."""

    pairs = possible_pairs()
    assert len(pairs) == 36
    assert len(set(pairs)) == 36
    for first, second in pairs:
        assert unicodedata.combining(first) < unicodedata.combining(second)


def test_the_order_inside_a_pair_is_fixed_by_the_class_not_by_the_scribe() -> None:
    """وترتيبُ المزدوج تُتمّه التسويةُ بالصنف، فلا خبرَ في تقدُّم إحداهما."""

    nine = set(THE_NINE_MARKS)
    for _, text in _SCOPES:
        raw = _pair_runs(text, nine)
        normalized = _pair_runs(unicodedata.normalize("NFC", text), nine)
        assert raw == normalized
        assert len(raw) == 16
        for run in raw:
            assert [unicodedata.combining(mark) for mark in run] == sorted(
                unicodedata.combining(mark) for mark in run
            )


def _pair_runs(text: str, nine: set[str]) -> list[tuple[str, ...]]:
    """يجمع تتابعاتِ العلامات الطويلةَ اثنتين فصاعدًا، بلا مرور بالوحدة."""

    runs: list[tuple[str, ...]] = []
    current: list[str] = []
    for character in text:
        if unicodedata.category(character) == "Mn":
            current.append(character)
            continue
        if len(current) >= 2:
            runs.append(tuple(current))
        current = []
    if len(current) >= 2:
        runs.append(tuple(current))
    return [run for run in runs if all(mark in nine for mark in run)]


def test_the_measured_census_of_the_fatiha_is_exact() -> None:
    """وتعدادُ الفاتحة معدودٌ مزدوجًا مزدوجًا لا موصوف."""

    census = pair_census_over(_FATIHA, "الفاتحة")
    assert (census.positions_read, census.total_pairs, census.realized) == (143, 16, 3)
    assert [(count.pair, count.occurrences) for count in census.ranked] == [
        ((_FATHA, _SHADDA), 10),
        ((_KASRA, _SHADDA), 4),
        ((_FATHA, _DAGGER), 2),
    ]


def test_the_measured_census_of_the_fath_is_exact() -> None:
    """وكذلك تعدادُ الفتح، وفيه مزدوجٌ لم يقع في الفاتحة."""

    census = pair_census_over(_FATH, "الفتح ٢٩")
    assert (census.positions_read, census.total_pairs, census.realized) == (249, 16, 2)
    assert [(count.pair, count.occurrences) for count in census.ranked] == [
        ((_FATHA, _SHADDA), 14),
        ((_DAMMA, _SHADDA), 2),
    ]


def test_the_same_pair_leads_in_both_deposits_uncontested() -> None:
    """فالمتصدّرُ في النصّين واحدٌ: فتحةٌ وشدّة، ولا منازعَ له في كلٍّ منهما."""

    for scope, text in _SCOPES:
        census = pair_census_over(text, scope)
        assert census.the_lead_is_uncontested
        assert len(census.leaders) == 1
        assert census.leaders[0].pair == (_FATHA, _SHADDA)


def test_the_sixteen_pairs_are_the_sixteen_enlarged_fibers() -> None:
    """ومجموعُ المزدوجات هو عينُ الألياف التي اتّسعت، لا عددًا آخرَ صادفه."""

    from alghanem.arabic.haraka_fiber_structure import widening_effect_on

    for scope, text in _SCOPES:
        assert pair_census_over(text, scope).total_pairs == (
            widening_effect_on(text, scope).fibers_enlarged
        )


def test_most_of_the_thirty_six_never_occur_in_either_deposit() -> None:
    """وأكثرُ المُجاز لم يقع، وغيابُه ليس منعًا بل خبرٌ عن قِصَر النصّين."""

    realized = {
        count.pair
        for scope, text in _SCOPES
        for count in pair_census_over(text, scope).ranked
    }
    assert len(realized) == 4
    assert len(set(possible_pairs()) - realized) == 32


def test_every_realized_pair_contains_a_contested_mark() -> None:
    """ولا مزدوجَ إلّا وفيه شدّةٌ أو خنجريّة، وهما المُخرَجتان بالاستيراد."""

    for scope, text in _SCOPES:
        for count in pair_census_over(text, scope).ranked:
            assert set(count.pair) & {_SHADDA, _DAGGER}


def test_a_tie_is_reported_as_a_tie_and_not_broken() -> None:
    """وعند التساوي يُعلَن التساوي ولا يُكسَر باختيارٍ من خارج العدّ."""

    census = PairCensus(
        scope="مُصطنَع",
        counts=(
            PairCount(pair=(_FATHA, _SHADDA), occurrences=5),
            PairCount(pair=(_KASRA, _SHADDA), occurrences=5),
            PairCount(pair=(_DAMMA, _SHADDA), occurrences=1),
        ),
        positions_read=11,
    )
    assert len(census.leaders) == 2
    assert not census.the_lead_is_uncontested
    assert census.realized == 3


def test_an_empty_census_has_no_leader_at_all() -> None:
    """ونطاقٌ لا مزدوجَ فيه لا متصدّرَ له، ولا يُختلَق له واحد."""

    census = pair_census_over("\u0628\u064e\u0628\u064e", "بلا مزدوج")
    assert census.total_pairs == 0
    assert census.ranked == ()
    assert census.leaders == ()
    assert not census.the_lead_is_uncontested


def test_a_census_refuses_a_repeated_pair_and_a_self_pair() -> None:
    """ولا يُقبَل مزدوجٌ مكرَّرٌ في تعدادٍ واحد ولا شيءٌ يزدوج بنفسه."""

    with pytest.raises(MarkPairError):
        PairCount(pair=(_FATHA, _FATHA), occurrences=1)
    with pytest.raises(MarkPairError):
        PairCount(pair=(_FATHA, _SHADDA), occurrences=-1)
    with pytest.raises(MarkPairError):
        PairCensus(
            scope="مكرَّر",
            counts=(
                PairCount(pair=(_FATHA, _SHADDA), occurrences=1),
                PairCount(pair=(_FATHA, _SHADDA), occurrences=2),
            ),
            positions_read=3,
        )
    with pytest.raises(MarkPairError):
        PairCensus(scope="  ", counts=(), positions_read=0)


def test_a_triple_is_not_counted_as_a_pair() -> None:
    """وثلاثُ علاماتٍ على موضعٍ ليست مزدوجًا، فلا تُحشَر في العدّ."""

    triple = f"\u0628{_FATHA}{_SHADDA}{_DAGGER}"
    census = pair_census_over(triple, "ثلاثيّ")
    assert census.positions_read == 1
    assert census.total_pairs == 0


def test_a_constructed_pair_is_counted_wherever_it_occurs() -> None:
    """وكلُّ مزدوجٍ من الستّة والثلاثين يُعَدّ متى وقع، لا المتحقّقُ وحدَه."""

    census = pair_census_over(f"\u0628{_KASRA}\u0652", "مُصطنَع")
    assert census.total_pairs == 1
    assert census.leaders[0].pair == (_KASRA, "\u0652")


def test_every_residual_is_named_by_its_own_key() -> None:
    """وكلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    assert set(MARK_PAIR_NAMED_RESIDUALS) == {
        "THE_CORPUS_BYTES_ARE_ABSENT_SO_NO_CORPUS_FIGURE_IS_PUBLISHED",
        "A_RANKING_ON_TWO_TEXTS_IS_NOT_A_CORPUS_RANKING",
        "AN_UNREALIZED_PAIR_IS_NOT_A_FORBIDDEN_PAIR",
        "THE_ORDER_INSIDE_A_PAIR_CARRIES_NO_INFORMATION",
        "A_TIE_IS_REPORTED_AND_NOT_BROKEN",
        "A_PAIR_OF_MARKS_IS_NOT_A_PHONETIC_UNIT",
    }
    for key, text in MARK_PAIR_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_this_count_carries_no_authority_field() -> None:
    """وعدٌّ لا سلطةَ فيه لا يحمل حقلَ سلطةٍ ولا رتبة."""

    for holder in (PairCount, PairCensus):
        for name in holder.__dataclass_fields__:
            lowered = name.lower()
            for token in ("authority", "born", "birth", "gate", "rank", "verdict"):
                assert token not in lowered
