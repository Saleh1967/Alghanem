"""رتبةُ الجواب: يقين، ظنّ، راجح، مرجوح، مردود، تعادل، تناقض، مخصوص."""

from __future__ import annotations

import csv
import random

from conftest import ROOT
from slge.knowledge import (
    Admission,
    Degree,
    Evidence,
    Genus,
    Literal,
    Naql,
    Standing,
    Step,
    WorldRule,
)
from slge.rank import Grade, Rank, Side, evidence_grade, rank, weigh_scoped
from world_fixture import ADMITTED, ev, rule

QURAN = "corpora/quran-simple-enhanced.txt"


def qati(eid: str) -> Evidence:
    return ev(eid, Genus.خبر_مقبول, QURAN, Naql.متواتر)


def ahad(eid: str) -> Evidence:
    return ev(eid, Genus.خبر_مقبول, "خبر آحاد", Naql.آحاد)


def r(rid: str, a: str, b: str, e: Evidence, positive: bool = True) -> WorldRule:
    return WorldRule(rid, a, b, Degree.اخص, Standing.شرعي, Admission.مقبول, "دليل", e, (),
                     positive)


def test_rank_table_matches_lean() -> None:
    names = {"zanni": Grade.ظني, "qati": Grade.قطعي}
    with (ROOT / "formal" / "out" / "rank.csv").open(encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert len(rows) == 108
    for g1, s1, x, g2, s2, y, v in rows:
        got = weigh_scoped(Side(names[g1], int(s1)), Side(names[g2], int(s2)),
                           x == "true", y == "true")
        assert got.value == v, (g1, s1, x, g2, s2, y)


def test_evidence_grades() -> None:
    assert evidence_grade(ev("ت", Genus.تعريف_مشترط, "م"))[0] is Grade.قطعي
    assert evidence_grade(ev("ق", Genus.خبر_مقبول, QURAN, Naql.متواتر))[0] is Grade.قطعي
    for n in (Naql.آحاد, Naql.مشهور, None):
        assert evidence_grade(ev("خ", Genus.خبر_مقبول, "خ", n))[0] is Grade.ظني
    assert evidence_grade(ev("م", Genus.مشاهدة, "م"))[0] is Grade.ظني
    assert evidence_grade(ev("ل", Genus.شاهد_معجمي, "لسان"))[0] is Grade.ظني


def test_yaqin_from_definition_and_from_mutawatir() -> None:
    assert rank(Literal("إنسان", True), "حيوان", ADMITTED).rank is Rank.يقين
    assert rank(Literal("أف", True), "محرم", ADMITTED).rank is Rank.يقين


def test_one_zanni_premise_makes_zann() -> None:
    hit = rule("ضرب-أذى", "ضرب", "أذى", Standing.عادي, ev("م", Genus.مشاهدة, "مشاهدة"),
               ("ضرب لا يؤلم",))
    harm = r("أذى-محرم", "أذى", "محرم", qati("إسراء"))
    got = rank(Literal("ضرب", True), "محرم", (hit, harm))
    assert got.rank is Rank.ظن and got.conclusion == Literal("محرم", True)


def test_qati_rejects_zanni() -> None:
    got = rank(Literal("ج", True), "س", (r("1", "ج", "س", qati("ق")),
                                          r("2", "ج", "س", ahad("أ"), positive=False)))
    assert got.rank is Rank.يقين and got.conclusion == Literal("س", True)
    assert got.opposing is not None and got.opposing.grade is Grade.ظني


def test_more_independent_witnesses_preponderate() -> None:
    rules = (r("1", "ج", "س", ahad("أ1")), r("2", "ج", "ص", ahad("أ2")),
             r("3", "ص", "س", ahad("أ3")), r("4", "ج", "س", ahad("أ4"), positive=False))
    got = rank(Literal("ج", True), "س", rules)
    assert got.rank is Rank.راجح and got.side == Side(Grade.ظني, 2)
    assert got.opposing == Side(Grade.ظني, 1)


def test_equal_zanni_is_taadul_and_qati_pair_is_tanaqud() -> None:
    eq = rank(Literal("ج", True), "س", (r("1", "ج", "س", ahad("أ")),
                                         r("2", "ج", "س", ahad("ب"), positive=False)))
    assert eq.rank is Rank.تعادل and eq.conclusion is None
    both = rank(Literal("ج", True), "س", (r("1", "ج", "س", qati("ق1")),
                                           r("2", "ج", "س", qati("ق2"), positive=False)))
    assert both.rank is Rank.تناقض and both.conclusion is None


def test_specific_wins_and_general_is_makhsus() -> None:
    general = r("مكلف-صوم", "مكلف", "صوم واجب", qati("فمن شهد منكم الشهر فليصمه"))
    special = r("مسافر-صوم", "مسافر", "صوم واجب", qati("أو على سفر فعدة"), positive=False)
    scope = WorldRule("مسافر-مكلف", "مسافر", "مكلف", Degree.اخص, Standing.تعريفي,
                      Admission.مقبول, "حد", ev("حد", Genus.تعريف_مشترط, "تعريف"))
    got = rank((Literal("مسافر", True), Literal("مكلف", True)), "صوم واجب",
               (general, special, scope))
    assert got.conclusion == Literal("صوم واجب", False) and got.rank is Rank.يقين
    assert got.specialised
    # عامٌّ قطعيٌّ وخاصٌّ ظنّيّ: يُعمل بالظنّيّ الخاصّ (ج٣ ¶1065)
    weak_special = r("مسافر-صوم", "مسافر", "صوم واجب", ahad("آحاد"), positive=False)
    got2 = rank((Literal("مسافر", True), Literal("مكلف", True)), "صوم واجب",
                (general, weak_special, scope))
    assert got2.conclusion == Literal("صوم واجب", False) and got2.rank is Rank.ظن


def test_blocked_rule_gives_no_support() -> None:
    sun = rule("شمس-نهار", "شمس", "نهار", Standing.عادي, ev("م", Genus.مشاهدة, "م"),
               ("كسوف",))
    assert rank(Literal("شمس", True), "نهار", (sun,), present_blockers=frozenset({"كسوف"})
                ).rank is Rank.لا_علم


def _mutawatir(path: tuple[Step, ...], by_id: dict[str, WorldRule]) -> bool:
    """فحصٌ مستقلٌّ عن `path_grade`: كلُّ دليلٍ في الطريق متواتر."""

    return all(
        (e := by_id[s.rule_id].evidence) is not None and e.naql is Naql.متواتر for s in path
    )


def test_rank_never_promotes_on_random_worlds() -> None:
    rng = random.Random(1065)
    concepts = ["أ", "ب", "ج", "د"]
    for _ in range(400):
        rules = []
        for i in range(rng.randint(1, 5)):
            a, b = rng.sample(concepts, 2)
            e = qati(f"ق{i}") if rng.random() < 0.5 else ahad(f"أ{i}")
            rules.append(r(f"r{i}", a, b, e, rng.random() < 0.7))
        got = rank(Literal(rng.choice(concepts), True), rng.choice(concepts), tuple(rules))
        by_id = {x.rule_id: x for x in rules}
        if got.rank is Rank.يقين:
            assert got.support and all(_mutawatir(p, by_id) for p in got.support)
        if got.rank in (Rank.ظن, Rank.راجح):
            assert got.support and not any(_mutawatir(p, by_id) for p in got.support)
        if got.rank is Rank.مردود:
            raise AssertionError("الجوابُ لا يكون هو المردود")
