"""حلقةُ التعلّم."""

from __future__ import annotations

from slge.knowledge import Genus, Licence, LicenceGround, Outcome
from slge.learning import Base, TableGenerator, TableWitness, learn, learn_round, measure
from world_fixture import ADMITTED, GOLD, PROPOSED_LICENCES, PROPOSED_RULES, ev

TRAIN = GOLD[:2]
HELD_OUT = GOLD[2:]


def _generator() -> TableGenerator:
    return TableGenerator({
        "موافقة": PROPOSED_RULES,
        "مخالفة-صفة": PROPOSED_LICENCES[:1],
        "مخالفة-شرط": PROPOSED_LICENCES[1:],
    })


def test_candidates_alone_answer_nothing() -> None:
    base = Base(ADMITTED + PROPOSED_RULES, PROPOSED_LICENCES)
    score, _ = measure(base, GOLD)
    assert score.wrong == 0 and score.correct == 1  # الضابطُ وحده: السكوتُ صواب
    assert all(base.ask(q).outcome is not Outcome.منتج for q in GOLD)


def test_held_out_is_never_shown() -> None:
    gen = _generator()
    learn(Base(ADMITTED), TRAIN, HELD_OUT, gen, TableWitness({}))
    assert set(gen.seen) <= {q.question_id for q in TRAIN}


def test_independent_witness_closes_gaps() -> None:
    witness = TableWitness({
        "أذى-محرم": ev("نص-الإسراء", Genus.خبر_مقبول, "corpora/quran"),
        "ضرب-أذى": ev("مشاهدة", Genus.مشاهدة, "مشاهدة معلنة"),
        "سائمة-زكاة": ev("وصف-مفهم", Genus.خبر_مقبول, "أصول"),
    })
    rounds = learn(Base(ADMITTED), TRAIN, HELD_OUT, _generator(), witness)
    first = rounds[0]
    assert first.accepted
    assert (first.train_before.correct, first.train_after.correct) == (0, 2)
    assert first.held_out_after.wrong == 0


def test_wrong_admission_is_retracted() -> None:
    bad = Licence("إنسان-حيوان", LicenceGround.علة_واحدة, ev("ر", Genus.فرضية, "مولد"))
    wrong_generator = TableGenerator({"موافقة": (bad,)})
    sloppy = TableWitness({"إنسان-حيوان": ev("خطأ", Genus.خبر_مقبول, "شاهد متساهل")})
    r = learn_round(Base(ADMITTED), GOLD, (), wrong_generator, sloppy)
    assert any(e.kind == "قبول" and e.subject == "رافع:إنسان-حيوان" for e in r.events)
    assert any(e.kind == "سحب" and e.subject == "رافع:إنسان-حيوان" for e in r.events)
    assert measure(r.base, GOLD)[0].wrong == 0
    assert all(lic.rule_id != "إنسان-حيوان" or lic.is_candidate for lic in r.base.licences)


def test_every_proposal_has_one_verdict() -> None:
    r = learn_round(Base(ADMITTED), GOLD, (), _generator(), TableWitness({}))
    proposed = [e.subject for e in r.events if e.kind == "اقتراح"]
    verdicts = [e.subject for e in r.events if e.kind in ("قبول", "رفض")]
    assert sorted(proposed) == sorted(verdicts) and len(set(proposed)) == len(proposed)
