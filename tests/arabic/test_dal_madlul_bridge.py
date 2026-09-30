"""شواهدُ جسر الدالّ بالمدلول: يُصادَم المخرَجُ بالوديعة، ولا يُصدَّق رقم."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from alghanem.arabic.dal_madlul_bridge import (
    AN_EMPTY_CHANNEL_IS_REPORTED_NOT_FILLED,
    A_COOCCURRENCE_WINDOW_IS_NOT_A_TRANSFER_OF_THE_MIND,
    A_SEMANTIC_AXIS_IS_NOT_THE_WHOLE_OF_A_DEFINIENDUM,
    NO_PAIR_CARRIES_BOTH_SIDES_AS_ONE_OBJECT,
    THE_CLASS_ANCHORS,
    THE_CONDITION_IS_QUOTED_FROM_THE_DEPOSIT_NOT_ASSERTED,
    THE_DEFERRED,
    THE_ILTIZAM_CONDITION_ANCHOR,
    THE_MATN_PATH,
    THE_PAIR_ANCHORS,
    THE_SHAPE_OF_A_GLOSS_IS_NOT_THE_GENUS_OF_A_MADLUL,
    BridgeError,
    BridgePair,
    DalalaChannel,
    IltizamStanding,
    MadlulClass,
    class_of_dal,
    coverage,
    derive_pairs,
    matn_deposit,
    pairs_in,
    pairs_joining_both_sides,
    pending_dawal,
    separation_count,
    unopened_channels,
)
from alghanem.arabic.owner_licensed_deposit import DepositStanding, standing_of

REPO_ROOT = Path(__file__).resolve().parents[2]


def _matn_text() -> str:
    return (REPO_ROOT / THE_MATN_PATH).read_text(encoding="utf-8").replace(
        "\u0640", ""
    )


def test_the_bridge_reads_only_a_deposit_that_matches_its_seal() -> None:
    """الشرطُ الأول: الختمُ قبل القراءة."""

    assert standing_of(matn_deposit()) is DepositStanding.SIGNED_AND_SEALED


def test_every_pair_carries_all_six_pillars() -> None:
    for one in derive_pairs():
        assert one.dal.strip()
        assert isinstance(one.channel, DalalaChannel)
        assert one.madlul.strip()
        assert isinstance(one.madlul_class, MadlulClass)
        assert one.literal_evidence.strip()
        assert one.sealed_source.startswith(THE_MATN_PATH + "#")


def test_every_evidence_line_is_actually_in_the_sealed_deposit() -> None:
    """الشرطُ الرابع: دليلٌ حرفيٌّ من الحاوية المختومة، لا نصٌّ مكتوبٌ باليد."""

    text = _matn_text()
    for one in derive_pairs():
        assert one.literal_evidence in text


def test_every_evidence_shows_both_its_dal_and_its_madlul() -> None:
    for one in derive_pairs():
        assert one.dal in one.literal_evidence
        assert one.madlul in one.literal_evidence


def test_the_sealed_source_carries_the_measured_digest() -> None:
    deposit = matn_deposit()
    for one in derive_pairs():
        assert one.sealed_source.endswith(deposit.transcribed_sha256)


def test_a_pair_without_literal_evidence_is_refused() -> None:
    with pytest.raises(BridgeError):
        BridgePair(
            dal="الإنسان",
            channel=DalalaChannel.MUTABAQA,
            madlul="الحيوان الناطق",
            madlul_class=MadlulClass.MEANING,
            literal_evidence="   ",
            sealed_source=THE_MATN_PATH,
        )


def test_evidence_that_does_not_show_the_pair_is_refused() -> None:
    with pytest.raises(BridgeError):
        BridgePair(
            dal="الإنسان",
            channel=DalalaChannel.MUTABAQA,
            madlul="الحيوان الناطق",
            madlul_class=MadlulClass.MEANING,
            literal_evidence="نصٌّ لا يذكر شيئًا من هذا",
            sealed_source=THE_MATN_PATH,
        )


def test_the_three_channels_are_each_populated_from_the_deposit() -> None:
    for channel in DalalaChannel:
        assert pairs_in(channel), channel.value


def test_the_iltizam_mark_is_condition_and_never_cause() -> None:
    """الشرطُ الثالث: اللزومُ شرطٌ لا موجِب."""

    for one in pairs_in(DalalaChannel.ILTIZAM):
        assert one.iltizam is IltizamStanding.CONDITION_NOT_CAUSE


def test_no_other_channel_carries_the_iltizam_mark() -> None:
    for one in derive_pairs():
        if one.channel is not DalalaChannel.ILTIZAM:
            assert one.iltizam is IltizamStanding.NOT_ASKED


def test_an_iltizam_pair_that_drops_the_condition_mark_is_refused() -> None:
    with pytest.raises(BridgeError):
        BridgePair(
            dal="الأسد",
            channel=DalalaChannel.ILTIZAM,
            madlul="الشجاعة",
            madlul_class=MadlulClass.UNTAGGED_FOR_WANT_OF_EVIDENCE,
            literal_evidence="كدلالة الأسد على الشجاعة",
            sealed_source=THE_MATN_PATH,
            iltizam=IltizamStanding.NOT_ASKED,
        )


def test_the_condition_mark_is_quoted_from_the_deposit_not_asserted() -> None:
    assert THE_ILTIZAM_CONDITION_ANCHOR in _matn_text()
    assert "مُشتَقٌّ" in THE_CONDITION_IS_QUOTED_FROM_THE_DEPOSIT_NOT_ASSERTED


def test_a_gloss_of_two_words_is_not_tagged_a_compound_madlul() -> None:
    """أخطرُ ما في العقد: صورةُ المخرَج ليست جنسَ المدلول."""

    mutabaqa = pairs_in(DalalaChannel.MUTABAQA)[0]
    assert len(mutabaqa.madlul.split()) == 2
    assert mutabaqa.madlul_class is not MadlulClass.COMPOUND_USED
    assert mutabaqa.madlul_class is MadlulClass.UNTAGGED_FOR_WANT_OF_EVIDENCE
    assert "الحبرَ" in THE_SHAPE_OF_A_GLOSS_IS_NOT_THE_GENUS_OF_A_MADLUL


def test_a_class_is_never_tagged_without_an_anchor_in_the_deposit() -> None:
    for dal, _, anchor in THE_CLASS_ANCHORS:
        assert anchor in _matn_text()
        assert class_of_dal(dal) is not (
            MadlulClass.UNTAGGED_FOR_WANT_OF_EVIDENCE
        )
    assert class_of_dal("الأسد") is (
        MadlulClass.UNTAGGED_FOR_WANT_OF_EVIDENCE
    )
    assert class_of_dal("لفظٌ لم يرد في المتن قطّ") is (
        MadlulClass.UNTAGGED_FOR_WANT_OF_EVIDENCE
    )


def test_the_five_stated_classes_are_each_named_exactly_once() -> None:
    tagged = [klass for _, klass, _ in THE_CLASS_ANCHORS]
    assert len(tagged) == len(set(tagged)) == 5
    assert MadlulClass.UNTAGGED_FOR_WANT_OF_EVIDENCE not in tagged


def test_no_bridge_dal_is_among_the_dawal_the_matn_classified() -> None:
    """هذا سببُ انضباطِ الأقسام صفرًا، ويُقاس لا يُقال."""

    classified = {dal for dal, _, _ in THE_CLASS_ANCHORS}
    assert {one.dal for one in derive_pairs()}.isdisjoint(classified)


def test_class_discipline_is_zero_and_it_is_reported_not_hidden() -> None:
    pairs = derive_pairs()
    assert sum(1 for one in pairs if one.is_tagged_by_evidence) == 0
    assert "لا تُستكمَل" in AN_EMPTY_CHANNEL_IS_REPORTED_NOT_FILLED


def test_the_unopened_channels_are_named_with_their_reason() -> None:
    reasons = dict(unopened_channels())
    assert len(reasons) == 2
    assert A_SEMANTIC_AXIS_IS_NOT_THE_WHOLE_OF_A_DEFINIENDUM in (
        reasons.values()
    )
    assert A_COOCCURRENCE_WINDOW_IS_NOT_A_TRANSFER_OF_THE_MIND in (
        reasons.values()
    )


def test_the_mental_entailment_wording_is_in_the_deposit() -> None:
    """امتناعُ نافذة الاقتران مسنودٌ بنصّ المتن لا برأي."""

    text = _matn_text()
    assert "وهو الذي ينتقل الذهن إليه عند سماع اللفظ" in text
    assert "كالعمى والبصر" in text


def test_the_pending_are_kept_and_never_guessed_away() -> None:
    """الشرطُ الخامس: المعلَّقُ صنفٌ أوّل."""

    pending = pending_dawal()
    assert pending
    for one in pending:
        assert one.why.strip()


def test_coverage_counts_the_pending_in_its_denominator() -> None:
    matched, every = coverage()
    assert matched < every
    assert every >= len({one.dal for one in derive_pairs()})


def test_a_pending_without_a_stated_reason_is_refused() -> None:
    from alghanem.arabic.dal_madlul_bridge import PendingDal

    with pytest.raises(BridgeError):
        PendingDal(dal="الأسد", why="  ")


def test_separation_is_zero_and_it_is_derived_from_the_pairs() -> None:
    """حدُّ العقد: صفرُ زوجٍ جُمع فيه الطرفان."""

    assert pairs_joining_both_sides() == ()
    assert separation_count() == 0
    assert "يُعاد اشتقاقُه" in NO_PAIR_CARRIES_BOTH_SIDES_AS_ONE_OBJECT


def test_the_bridge_does_not_import_the_deferred_seven() -> None:
    import alghanem.arabic.dal_madlul_bridge as module

    source = Path(module.__file__).read_text(encoding="utf-8")
    assert "lafz_madlul_relation_formal" not in source
    assert "signifier_signified_relation" not in source
    assert "from ..kernel" not in source


def test_the_deferred_line_is_stated_verbatim() -> None:
    assert "لم يُبنَ" in THE_DEFERRED.what
    assert "السباعيّ" in THE_DEFERRED.why


def test_no_evidence_line_is_transcribed_into_the_module() -> None:
    """السجلُّ مُشتَقٌّ لا منقول: لا سطرَ دليلٍ مكتوبٌ في الوحدة."""

    import alghanem.arabic.dal_madlul_bridge as module

    source = Path(module.__file__).read_text(encoding="utf-8")
    for one in derive_pairs():
        assert one.literal_evidence not in source


def test_an_anchor_that_occurs_twice_is_refused_as_an_anchor() -> None:
    """مرساةُ الأسد ضُيِّقت لأنّ المثال مُستشهَدٌ به في بابَين."""

    text = _matn_text()
    assert text.count("كدلالة الأسد على الشجاعة") == 2
    iltizam_anchor = next(
        anchor
        for _, channel, _, anchor in THE_PAIR_ANCHORS
        if channel is DalalaChannel.ILTIZAM
    )
    assert text.count(iltizam_anchor) == 1


def test_the_emitted_jsonl_matches_what_the_bridge_derives_now() -> None:
    deposited = REPO_ROOT / "exhibits/dal-madlul-bridge/bridge_report.jsonl"
    rows = [
        json.loads(line)
        for line in deposited.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    pairs = derive_pairs()
    assert len(rows) == len(pairs)
    for row, pair in zip(rows, pairs, strict=True):
        assert row["دال"] == pair.dal
        assert row["قناة"] == pair.channel.value
        assert row["مدلول"] == pair.madlul
        assert row["صنف_المدلول"] == pair.madlul_class.value
        assert row["دليل_حرفي"] == pair.literal_evidence
        assert row["مصدر_مختوم"] == pair.sealed_source


def test_no_emitted_row_fuses_the_two_sides_into_one_field() -> None:
    deposited = REPO_ROOT / "exhibits/dal-madlul-bridge/bridge_report.jsonl"
    for line in deposited.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        assert "مفهوم" not in row
        assert f"{row['دال']} {row['مدلول']}" not in row.values()
