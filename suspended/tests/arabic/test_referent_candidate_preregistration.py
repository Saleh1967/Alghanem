"""اختباراتُ تسجيلِ مقامِ الضمائر وقيودِها ونافذتِها، بأسطرٍ مُصرَّحٍ باصطناعها.

`SyntheticLinesAreDeclaredNotHidden`: كلُّ ما يُبنى هنا **مُصطنَعٌ**، يُحاكي
بنيةَ الوَسْم والصورة وحدَها؛ ولا يخرج منه رقمٌ عن MASAQ البتّة. والأعدادُ
الثمانيةَ عشرَ لا تُقاس إلّا من البايتات المُبصَّمة، واختبارُها الواحدُ يُفعَّل
حين تكون في `corpora/MASAQ.csv` أو في `ALGHANEM_MASAQ_PATH`.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_RELATIVE_PATH,
    masaq_bytes_are_resolvable,
    read_masaq_bytes,
)
from alghanem.arabic.referent_candidate_preregistration import (
    AGGREGATE_PRONOUN_TAGS,
    ARRIVING_PRONOUN_TOTAL,
    CONSTRAINED_PRONOUN_TAGS,
    DECLARED_DENOMINATOR_COUNT,
    DENOMINATOR_SHARE_PERCENTAGE,
    INFERENCE_UNDETERMINED,
    NOMINAL_TAG_VALUES,
    PRE_MEASUREMENT_EXPECTATION,
    REFERENT_CANDIDATE_NAMED_RESIDUALS,
    REFERENT_CANDIDATE_PREREGISTRATION_DIGEST,
    SEARCH_WINDOW,
    ExpectationVerdict,
    Gender,
    Number,
    Person,
    PronounConstraint,
    ReferentPreregistrationError,
    constraints_of,
    expectation_verdict,
    infer_surface,
    is_nominal_tag,
    pronoun_tag_figures,
    referent_preregistration_digest,
    strip_surface,
)


def test_a_constrained_tag_parses_into_the_whole_triple() -> None:
    """الوسومُ الخمسةَ عشرَ تُحلَّل كلُّها، وثلاثيّتُها من وسمها لا بجانبه."""

    assert constraints_of("PRON_3MS") == PronounConstraint(
        person=Person.THIRD, number=Number.SINGULAR, gender=Gender.MASCULINE
    )
    assert constraints_of("POSS_PRON_3D") == PronounConstraint(
        person=Person.THIRD, number=Number.DUAL, gender=Gender.UNSPECIFIED
    )
    assert constraints_of("PRON_1P") == PronounConstraint(
        person=Person.FIRST, number=Number.PLURAL, gender=Gender.UNSPECIFIED
    )
    for item in CONSTRAINED_PRONOUN_TAGS:
        assert item.constraint is not None


@pytest.mark.parametrize(
    "tag",
    [
        "SUBJ_PRON",
        "POSS_PRON",
        "OBJ_PRON",
        "PRON",
        "PRON_",
        "PRON_4MS",
        "PRON_3XS",
        "PRON_3MX",
        "PRON_3MSS",
        "NOUN",
        "",
    ],
)
def test_an_unparsed_tag_yields_no_constraint(tag: str) -> None:
    """وسمٌ لا يُحلَّل يُعيد `None`، ولا يُمنَح قيدًا افتراضيًّا ولا أقربَ قيد."""

    assert constraints_of(tag) is None


def test_the_aggregate_tags_are_declared_outside_the_denominator() -> None:
    """الوسومُ المُجمَّلةُ ثلاثةٌ، بعللِ خروجها مكتوبةً، ولا تدخل مقامًا."""

    tags = {item.tag: item for item in AGGREGATE_PRONOUN_TAGS}
    assert set(tags) == {"SUBJ_PRON", "POSS_PRON", "OBJ_PRON"}
    assert tags["SUBJ_PRON"].deposited_count == 7_964
    assert tags["POSS_PRON"].deposited_count == 7_678
    assert tags["OBJ_PRON"].deposited_count == 3_211
    for item in AGGREGATE_PRONOUN_TAGS:
        assert constraints_of(item.tag) is None
        assert item.why_it_is_outside.strip()
    assert all(
        item.tag not in {entry.tag for entry in CONSTRAINED_PRONOUN_TAGS}
        for item in AGGREGATE_PRONOUN_TAGS
    )


def test_eleven_percent_is_the_real_denominator() -> None:
    """المقامُ ٢٬٦٠٨ من ٢٣٬٥٧٩، والنسبةُ مكتوبةٌ بمنازلِ مقارنتها لا مُقرَّبة."""

    assert len(CONSTRAINED_PRONOUN_TAGS) == 15
    assert DECLARED_DENOMINATOR_COUNT == 2_608
    assert ARRIVING_PRONOUN_TOTAL == 23_579
    share = 100.0 * DECLARED_DENOMINATOR_COUNT / ARRIVING_PRONOUN_TOTAL
    places = len(DENOMINATOR_SHARE_PERCENTAGE.split(".")[1])
    assert f"{share:.{places}f}" == DENOMINATOR_SHARE_PERCENTAGE
    assert share < 12.0


def test_a_tag_without_a_triple_is_refused_from_the_denominator() -> None:
    """لا يُودَع في المقام وَسْمٌ لا يُحلَّل، ولا يُعلَن خارجَه وَسْمٌ يُحلَّل."""

    from alghanem.arabic.referent_candidate_preregistration import (
        AggregatePronounTag,
        ConstrainedPronounTag,
    )

    with pytest.raises(ReferentPreregistrationError):
        ConstrainedPronounTag("SUBJ_PRON", "مُجمَّل", 1)
    with pytest.raises(ReferentPreregistrationError):
        ConstrainedPronounTag("PRON_3MS", "بلا عدد", -1)
    with pytest.raises(ReferentPreregistrationError):
        AggregatePronounTag(
            tag="PRON_3MS",
            arabic_name="مُقيَّد",
            deposited_count=1,
            why_it_is_outside="علّة",
        )
    with pytest.raises(ReferentPreregistrationError):
        AggregatePronounTag(
            tag="SUBJ_PRON",
            arabic_name="مُجمَّل",
            deposited_count=1,
            why_it_is_outside="  ",
        )


def test_the_window_is_declared_before_the_measurement() -> None:
    """النافذةُ آيةٌ وسابقتُها، ولا تعبر سورةً، ونصُّ إعلانها مكتوبٌ معها."""

    assert SEARCH_WINDOW.preceding_verses == 1
    assert SEARCH_WINDOW.crosses_sura_boundary is False
    assert "AWindowIsDeclaredNotOptimised" in SEARCH_WINDOW.declaration


def test_discourse_participants_are_named_in_the_constraint() -> None:
    """المتكلّمُ والمخاطَبُ طرفا خطابٍ في القيد نفسه، لا في تعليقٍ خارجه."""

    assert constraints_of("PRON_1S") is not None
    speaker = constraints_of("PRON_1S")
    addressee = constraints_of("PRON_2MP")
    absent = constraints_of("PRON_3MS")
    assert speaker is not None and addressee is not None and absent is not None
    assert speaker.is_discourse_participant
    assert addressee.is_discourse_participant
    assert not absent.is_discourse_participant


def test_the_surface_inference_names_its_failure() -> None:
    """قاعدةُ الاستنتاج تُصرِّح بعجزها ولا تسحب الاسمَ إلى «مذكّرٍ مفرد»."""

    feminine = infer_surface("\u0645\u0644\u0643\u0629")
    assert feminine.number is Number.SINGULAR
    assert feminine.gender is Gender.FEMININE

    plural_f = infer_surface("\u0645\u0624\u0645\u0646\u0627\u062a")
    assert plural_f.number is Number.PLURAL
    assert plural_f.gender is Gender.FEMININE

    plural_m = infer_surface("\u0645\u0624\u0645\u0646\u0648\u0646")
    assert plural_m.number is Number.PLURAL
    assert plural_m.gender is Gender.MASCULINE

    dual_m = infer_surface("\u0631\u062c\u0644\u0627\u0646")
    assert dual_m.number is Number.DUAL
    assert dual_m.gender is Gender.MASCULINE

    ambiguous = infer_surface("\u0645\u0624\u0645\u0646\u064a\u0646")
    assert ambiguous.number is None
    assert ambiguous.gender is None
    assert ambiguous.rule_name == "\u064a\u0627\u0621+\u0646\u0648\u0646"
    assert not ambiguous.is_determined

    broken_plural = infer_surface("\u0631\u062c\u0627\u0644")
    assert broken_plural.rule_name == INFERENCE_UNDETERMINED
    assert not broken_plural.is_determined

    empty = infer_surface("")
    assert empty.rule_name == INFERENCE_UNDETERMINED


def test_diacritics_and_segment_separators_are_stripped_by_a_declared_step() -> None:
    """التجريدُ خطوةٌ مُعلَنةٌ: حركاتٌ وفواصلُ تقطيعٍ تُزال قبل قراءة اللاحقة."""

    assert strip_surface("\u0645\u064e\u0644\u0650\u0643\u064e\u0629\u064c").endswith(
        "\u0629"
    )
    assert strip_surface("\u0627\u0644+\u0645\u0644\u0643\u0629") == (
        "\u0627\u0644\u0645\u0644\u0643\u0629"
    )
    inferred = infer_surface(
        "\u0627\u0644+\u0645\u064f\u0624\u0645\u0650\u0646\u0648\u0646"
    )
    assert inferred.number is Number.PLURAL


def test_a_nominal_tag_list_is_declared_not_discovered() -> None:
    """الوسومُ الاسميةُ مطابقةً حرفيّةً؛ ووسمٌ خارجَ القائمة ليس مرشَّحًا."""

    assert "NOUN" in NOMINAL_TAG_VALUES
    assert "GERUND" in NOMINAL_TAG_VALUES
    assert is_nominal_tag("NOUN_ACTIVE_PART")
    assert is_nominal_tag("  PN  ")
    assert not is_nominal_tag("NOUNISH")
    assert not is_nominal_tag("PRON_3MS")
    assert not is_nominal_tag("VERB")


def test_the_expectation_is_written_with_its_falsifier() -> None:
    """التوقّعُ مكتوبٌ وشرطُ تكذيبه معه، والدالّةُ تُكذِّبه ولا تُعدِّله."""

    assert "PreMeasurementExpectation" in PRE_MEASUREMENT_EXPECTATION
    assert "PRON_1S" in PRE_MEASUREMENT_EXPECTATION
    assert "PRON_3MS" in PRE_MEASUREMENT_EXPECTATION
    assert (
        expectation_verdict(speaker_single_share=40.0, absent_single_share=10.0)
        is ExpectationVerdict.HELD
    )
    assert (
        expectation_verdict(speaker_single_share=10.0, absent_single_share=40.0)
        is ExpectationVerdict.FALSIFIED
    )
    assert (
        expectation_verdict(speaker_single_share=10.0, absent_single_share=10.0)
        is ExpectationVerdict.FALSIFIED
    )
    assert (
        expectation_verdict(speaker_single_share=None, absent_single_share=10.0)
        is ExpectationVerdict.NOT_MEASURABLE
    )


def test_the_named_limits_are_written_inside_the_unit() -> None:
    """الحدودُ الأربعةُ وما معها مكتوبةٌ بأسمائها، لا في وثيقةٍ خارج الوحدة."""

    for name in (
        "TheReferentIsNotAnnotatedAnywhere",
        "GenderAndNumberAreInferredNotTagged",
        "ElevenPercentIsTheRealDenominator",
        "ACandidateSetIsNotAnAnswer",
        "AnUnparsedTagYieldsNoConstraint",
        "AWindowIsDeclaredNotOptimised",
        "NoFigureWithoutTheFingerprintedBytes",
    ):
        assert name in REFERENT_CANDIDATE_NAMED_RESIDUALS
        assert name in REFERENT_CANDIDATE_NAMED_RESIDUALS[name]


def test_the_digest_binds_the_content_of_the_registration() -> None:
    """بصمةُ التسجيل ثابتةٌ على محتواه؛ فبها يُعرَف تحت أيّ قاعدةٍ خرج رقمٌ."""

    assert referent_preregistration_digest() == (
        REFERENT_CANDIDATE_PREREGISTRATION_DIGEST
    )
    assert len(REFERENT_CANDIDATE_PREREGISTRATION_DIGEST) == 64


def test_every_deposited_figure_carries_a_rederiver() -> None:
    """ثمانيةَ عشرَ رقمًا، كلٌّ بدالّةِ إعادةِ اشتقاقه؛ فلا رقمَ بلا شاهد."""

    figures = pronoun_tag_figures()
    assert len(figures) == len(CONSTRAINED_PRONOUN_TAGS) + len(AGGREGATE_PRONOUN_TAGS)
    assert {figure.tag for figure in figures} == {
        item.tag for item in CONSTRAINED_PRONOUN_TAGS
    } | {item.tag for item in AGGREGATE_PRONOUN_TAGS}
    for figure in figures:
        assert callable(figure.derive)


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason=(
        f"no MASAQ bytes resolve from {MASAQ_RELATIVE_PATH} nor from a "
        "declared path; the eighteen pronoun-tag counts are derived only from "
        "the fingerprinted bytes. Bytes that resolve and differ are not "
        "skipped: they fail"
    ),
)
def test_the_pronoun_tag_counts_are_rederived_from_the_deposited_bytes() -> None:
    """يُعرَض المُدَّعى والمُشتَقّ معًا؛ ولا يُعدَّل مُدَّعًى ليُطابِق ما قِيس."""

    data = read_masaq_bytes()
    mismatched = [
        (figure.tag, figure.deposited, figure.rederive(data))
        for figure in pronoun_tag_figures()
        if not figure.holds(data)
    ]
    assert not mismatched, f"أعدادٌ خالفت المُودَع: {mismatched}"

    constrained_total = sum(
        figure.rederive(data)
        for figure in pronoun_tag_figures()
        if figure.tag in {item.tag for item in CONSTRAINED_PRONOUN_TAGS}
    )
    assert constrained_total == DECLARED_DENOMINATOR_COUNT
