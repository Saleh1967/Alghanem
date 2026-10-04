"""اختباراتُ سُلَّم الترخيص المتدرِّج: ما يُفحَص هو امتناعُه لا طواعيتُه."""

from __future__ import annotations

import pytest

from alghanem.arabic.masaq_corpus_deposit import (
    masaq_bytes_are_resolvable,
    masaq_records,
    read_masaq_bytes,
)
from alghanem.arabic.tadarruj_bina_licence import (
    THE_LADDER_AT_MEASUREMENT,
    THE_RUNGS,
    THE_STOP_AT_MEASUREMENT,
    THE_WORDS_DECIDED_AT_MEASUREMENT,
    Binding,
    CellKind,
    LadderReading,
    Rung,
    RungReading,
    RungStanding,
    TadarrujLicenceError,
    cell_kind,
    ladder_reading,
    licensing_stops_at,
    reads_as,
    report_on_word,
    rung_named,
    rung_reading,
)


@pytest.fixture(scope="module")
def records() -> tuple[dict[str, str], ...]:
    return masaq_records(read_masaq_bytes())


# --- بنيةُ السُّلَّم: تُفحَص بلا بايتات -----------------------------------


def test_the_rungs_are_ordered_and_the_declined_one_is_last() -> None:
    assert [rung.index for rung in THE_RUNGS] == list(range(1, len(THE_RUNGS) + 1))
    assert THE_RUNGS[-1].claimed_binding is Binding.DECLINED
    assert all(
        rung.claimed_binding is Binding.BUILT for rung in THE_RUNGS[:-1]
    ), "المبنيّاتُ كلُّها دون المعرَب؛ ولا يُقدَّم معرَبٌ على مبنيّ"


def test_no_tag_is_claimed_by_two_rungs() -> None:
    seen: dict[str, str] = {}
    for rung in THE_RUNGS:
        for tag in rung.tags:
            assert tag not in seen, f"الوسمُ `{tag}` في رتبتين: {seen[tag]} و{rung.name}"
            seen[tag] = rung.name


def test_the_derived_nouns_are_not_admitted_among_the_particles() -> None:
    particles = rung_named("الأدواتُ والحروفُ الوظيفيّة")
    assert "NOUN_ACTIVE_PART" not in particles.tags
    assert "NOUN_PASSIVE_PART" not in particles.tags


def test_a_rung_with_a_column_refuses_an_empty_inventory() -> None:
    with pytest.raises(TadarrujLicenceError):
        Rung(index=1, name="رتبةٌ بلا وسم", tags=(), claimed_binding=Binding.BUILT)


def test_a_suspended_rung_refuses_to_carry_tags() -> None:
    with pytest.raises(TadarrujLicenceError):
        Rung(
            index=1,
            name="رتبةٌ موقوفةٌ تُعدَّد",
            tags=("PV",),
            claimed_binding=Binding.BUILT,
            has_a_column=False,
        )


def test_a_rung_may_not_claim_an_unreadable_binding() -> None:
    with pytest.raises(TadarrujLicenceError):
        Rung(
            index=1,
            name="رتبةٌ تدّعي ما لا يُقرَأ",
            tags=("PV",),
            claimed_binding=Binding.NOT_READABLE,
        )


def test_the_augmented_past_rung_is_suspended_for_a_missing_column() -> None:
    rung = rung_named("الفعلُ الماضي المزيدُ مفروزًا عن المجرَّد")
    assert not rung.has_a_column
    reading = rung_reading((), rung)
    assert reading.standing is RungStanding.HAS_NO_COLUMN_IN_THE_MATERIAL
    assert not reading.is_exhausted, "الموقوفةُ لا تُستنفَد، فلا تُرخِّص ما فوقها"


# --- العمودُ المختلط: الحكمُ والبابُ لا يُخلَطان -----------------------------


def test_the_mixed_column_is_sorted_before_it_is_read() -> None:
    assert cell_kind("مبني") is CellKind.A_JUDGEMENT
    assert cell_kind("اسم موصول") is CellKind.A_DOOR
    assert cell_kind("None") is CellKind.EMPTY
    assert cell_kind("") is CellKind.EMPTY
    assert cell_kind("قيمةٌ لم تَرِد قطّ") is CellKind.UNKNOWN


def test_a_door_cell_still_reads_as_built() -> None:
    assert reads_as("اسم موصول") is Binding.BUILT
    assert reads_as("ضمير متصل") is Binding.BUILT
    assert reads_as("معرب") is Binding.DECLINED


def test_an_empty_or_unknown_cell_is_never_read_as_declined() -> None:
    for cell in ("", "None", "قيمةٌ لم تَرِد قطّ"):
        assert (
            reads_as(cell) is Binding.NOT_READABLE
        ), "الخلوُّ والجهلُ يُسمَّيان؛ وحملُهما على `معرب` يُنتِج حكمًا لم يُقَس"


# --- حسابُ الرتبة: لا مقطعَ يسقط، ولا أغلبيّةَ تُرخِّص ------------------------


def _row(tag: str, cell: str, word: str = "ص") -> dict[str, str]:
    return {
        "Morph_tag": tag,
        "Invariable_Declinable": cell,
        "Segmented_Word": word,
        "Without_Diacritics": word,
        "Sura_No": "1",
        "Verse_No": "1",
    }


def test_the_parts_of_a_rung_reading_sum_to_its_segments() -> None:
    rung = rung_named("الأسماءُ الموصولة")
    reading = rung_reading(
        [_row("REL_PRON", "اسم موصول"), _row("REL_PRON", "معرب"), _row("REL_PRON", "")],
        rung,
    )
    assert reading.segments == 3
    assert reading.licensed + reading.disagreeing + reading.unreadable == 3


def test_a_sum_that_does_not_close_is_refused_structurally() -> None:
    with pytest.raises(TadarrujLicenceError):
        RungReading(
            rung=rung_named("الأسماءُ الموصولة"),
            segments=3,
            distinct_forms=1,
            licensed=1,
            disagreeing=0,
            unreadable=0,
            disagreeing_cells=(),
            standing=RungStanding.LICENSED_NOT_EXHAUSTED,
        )


def test_a_single_disagreement_withholds_exhaustion_against_the_majority() -> None:
    rung = rung_named("الأسماءُ الموصولة")
    rows = [_row("REL_PRON", "اسم موصول") for _ in range(999)]
    rows.append(_row("REL_PRON", "معرب"))
    reading = rung_reading(rows, rung)
    assert reading.licensed == 999
    assert reading.disagreeing == 1
    assert not reading.is_exhausted, "تسعُمئةٍ وتسعةٌ وتسعون لا تبتلع واحدًا مخالفًا"
    assert reading.disagreeing_cells == (("معرب", 1),)


def test_a_rung_with_no_segments_is_not_exhausted() -> None:
    reading = rung_reading([], rung_named("الأسماءُ الموصولة"))
    assert reading.segments == 0
    assert not reading.is_exhausted, "الخلوُّ من المقاييس ليس استنفادًا"


# --- الصعود: ما فوق الموقف لم يُبلَغ ---------------------------------------


def test_everything_above_the_stop_is_marked_not_reached() -> None:
    rows = [_row("PREP", "معرب")] + [
        _row(rung.tags[0], "مبني") for rung in THE_RUNGS[1:] if rung.tags
    ]
    reading = ladder_reading(rows)
    assert reading.stops_at.rung.index == 1
    above = [
        item for item in reading.rungs if item.rung.index > 1 and item.rung.has_a_column
    ]
    assert all(
        item.standing is RungStanding.NOT_REACHED for item in above
    ), "رتبةٌ فوق الموقف لم تُفحَص، فلا تُقرَأ نجاحًا ولا فشلًا"
    suspended = reading.reading_of("الفعلُ الماضي المزيدُ مفروزًا عن المجرَّد")
    assert suspended.standing is RungStanding.HAS_NO_COLUMN_IN_THE_MATERIAL, (
        "انعدامُ العمود صفةٌ في المادّة لا في الصعود، فلا يُبدَّل اسمُها "
        "بـ«لم تُبلَغ» وإن وقف السُّلَّمُ دونها"
    )


def test_a_ladder_reading_refuses_to_drop_a_rung() -> None:
    with pytest.raises(TadarrujLicenceError):
        LadderReading(rungs=())


def test_a_word_outside_the_material_is_named_not_guessed() -> None:
    with pytest.raises(TadarrujLicenceError):
        report_on_word([_row("PREP", "مبني", "من")], "رجل")


def test_a_transmitted_label_does_not_lift_our_stop() -> None:
    rows = [_row("PREP", "معرب", "رب"), _row("NOUN_CONCRETE", "معرب", "رجل")]
    report = report_on_word(rows, "رجل")
    assert report.transmitted_bindings == (
        Binding.DECLINED,
    ), "المُوسِّمُ جازمٌ بالإعراب، ويُنقَل جزمُه كما هو"
    assert report.our_standing is RungStanding.NOT_REACHED
    assert (
        not report.is_licensed_by_our_ladder
    ), "جزمُ المُوسِّم خبرٌ عنه؛ ولا يُرقَّى ترخيصًا من سُلَّمنا"


# --- على البايتات المختومة --------------------------------------------------


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason="بايتاتُ MASAQ غيرُ محلولةٍ في هذه البيئة؛ ولا يخرج رقمٌ بلا بايتات",
)
def test_the_transcribed_ladder_matches_what_the_sealed_bytes_measure(
    records: tuple[dict[str, str], ...],
) -> None:
    reading = ladder_reading(records)
    measured = {
        item.rung.name: (
            item.segments,
            item.distinct_forms,
            item.licensed,
            item.disagreeing,
            item.unreadable,
        )
        for item in reading.rungs
    }
    assert measured == dict(THE_LADDER_AT_MEASUREMENT)


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason="بايتاتُ MASAQ غيرُ محلولةٍ في هذه البيئة؛ ولا يخرج رقمٌ بلا بايتات",
)
def test_the_ladder_stops_at_its_first_rung_on_this_material(
    records: tuple[dict[str, str], ...],
) -> None:
    stop = licensing_stops_at(records)
    assert stop.rung.name == THE_STOP_AT_MEASUREMENT
    assert stop.rung.index == 1
    assert stop.standing is RungStanding.LICENSED_NOT_EXHAUSTED


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason="بايتاتُ MASAQ غيرُ محلولةٍ في هذه البيئة؛ ولا يخرج رقمٌ بلا بايتات",
)
def test_the_two_words_are_reported_and_not_licensed(
    records: tuple[dict[str, str], ...],
) -> None:
    reading = ladder_reading(records)
    for word, (segments, rung_name) in THE_WORDS_DECIDED_AT_MEASUREMENT.items():
        report = report_on_word(records, word, reading=reading)
        assert len(report.rows) == segments
        assert report.our_rung is not None
        assert report.our_rung.name == rung_name
        assert report.our_standing is RungStanding.NOT_REACHED
        assert not report.is_licensed_by_our_ladder


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason="بايتاتُ MASAQ غيرُ محلولةٍ في هذه البيئة؛ ولا يخرج رقمٌ بلا بايتات",
)
def test_reading_the_column_as_two_values_loses_the_built_doors(
    records: tuple[dict[str, str], ...],
) -> None:
    literal = sum(1 for row in records if row["Invariable_Declinable"] == "مبني")
    read_properly = sum(
        1 for row in records if reads_as(row["Invariable_Declinable"]) is Binding.BUILT
    )
    assert (
        read_properly - literal > 38_000
    ), "البابُ المكتوبُ مكانَ الحكم ليس قلّةً تُهمَل؛ وإهمالُه يُسقِط عشراتِ الآلاف من المبنيّات"
