"""التعلّم الذاتيّ: حلقةٌ مغلقة — مولِّدٌ يقترح، وشاهدٌ مستقلٌّ يقبل، وقياسٌ على أسئلةٍ محجوبة، وسحب.

ما يضمنه هذا الملفّ (وتفحصه `tests/test_learning.py`):

1. **المولِّدُ يقترح ولا يحكم:** كلُّ ما يقترحه يدخل مرشَّحًا، والمرشَّحُ لا يُنتج.
2. **الشاهدُ مستقلّ:** القبولُ بدليلٍ من `Witness`، وجنسُه موافقٌ لمنزلة القاعدة؛ والفرضيّةُ
   لا تُقبل.
3. **المحجوبُ محجوب:** أسئلةُ `held_out` لا تُعرض على المولِّد أبدًا؛ تُقاس فقط.
4. **السحبُ تلقائيّ:** إذا أنتج المقبولُ الجديدُ جوابًا خاطئًا في أيّ قسمٍ سُحب ما قُبل في
   الجولة على طريق ذلك الجواب؛ فإن بقي خطأٌ زائدٌ رُدّت الجولةُ كلُّها.
5. **السجلُّ تامّ:** لكلّ اقتراحٍ حادثةٌ ختاميّةٌ واحدة (قبولٌ أو رفض)، وللسحب حادثته.

وهذه حلقةُ النبهاني في «التفكير»: الواقعُ (السؤال) والمعلوماتُ السابقة (القواعدُ المقبولة)
والربط (`infer`)؛ والرأيُ السابقُ (المولِّد) يُحال بينه وبين الحكم حتى يصير معلومةً بدليل.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

from .knowledge import (
    Admission,
    Evidence,
    Genus,
    Licence,
    Literal,
    Outcome,
    Verdict,
    WorldKnowledgeError,
    WorldRule,
    infer,
)

__all__ = [
    "Base",
    "Event",
    "Generator",
    "GoldQuestion",
    "Mark",
    "Proposal",
    "Round",
    "Score",
    "TableGenerator",
    "TableWitness",
    "Witness",
    "grade",
    "learn",
    "learn_round",
    "measure",
]

Proposal = WorldRule | Licence


@dataclass(frozen=True, slots=True)
class GoldQuestion:
    """سؤالٌ ذهبيّ: جوابُه في مصدره بموضعه، ولا يقرأ المحرّكُ ذلك المصدر.

    ‎expected = None‎ معناه أنّ الصوابَ ألّا يُحكم (صورةٌ عقيمة).
    """

    question_id: str
    text: str
    given: Literal
    target: str
    expected: Literal | None
    locus: str
    blockers: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class Base:
    """الرصيد: قواعدُ ورافعات، مقبولةٌ ومرشَّحة. لا يتغيّر؛ كلُّ تغييرٍ رصيدٌ جديد."""

    rules: tuple[WorldRule, ...] = ()
    licences: tuple[Licence, ...] = ()

    def ask(self, q: GoldQuestion) -> Verdict:
        return infer(q.given, q.target, self.rules, self.licences, q.blockers)


class Mark(Enum):
    """تقديرُ جوابٍ واحد."""

    صواب = "correct"
    خطأ = "wrong"
    ناقص = "pending"
    صامت = "silent"


def grade(q: GoldQuestion, v: Verdict) -> Mark:
    """الإنتاجُ بغير المتوقَّع خطأ؛ والسكوتُ حيث يُتوقَّع السكوتُ صواب."""

    if q.expected is None:
        if v.outcome is Outcome.منتج:
            return Mark.خطأ
        return Mark.صواب if v.outcome is Outcome.غير_منتج else Mark.صامت
    if v.outcome is Outcome.منتج:
        return Mark.صواب if v.conclusion == q.expected else Mark.خطأ
    return Mark.ناقص if v.outcome is Outcome.ناقص else Mark.صامت


@dataclass(frozen=True, slots=True)
class Score:
    """عدُّ التقديرات."""

    correct: int = 0
    wrong: int = 0
    pending: int = 0
    silent: int = 0

    @property
    def total(self) -> int:
        return self.correct + self.wrong + self.pending + self.silent


def measure(base: Base, questions: Sequence[GoldQuestion]) -> tuple[Score, dict[str, Mark]]:
    """قِس الرصيدَ على أسئلة."""

    marks = {q.question_id: grade(q, base.ask(q)) for q in questions}
    values = list(marks.values())
    return Score(*(values.count(m) for m in Mark)), marks


class Generator(Protocol):
    """مولِّدٌ يقترح قواعدَ أو رافعاتٍ لسؤالٍ لم يُجَب (نموذجٌ لغويّ، أو مستخرِجٌ من نصّ)."""

    def propose(self, q: GoldQuestion, verdict: Verdict, base: Base) -> Sequence[Proposal]: ...


class Witness(Protocol):
    """شاهدٌ مستقلّ: يردّ دليلًا على الاقتراح من مصدرٍ غير المولِّد، أو ‎None‎."""

    def evidence_for(self, proposal: Proposal) -> Evidence | None: ...


@dataclass(frozen=True, slots=True)
class TableGenerator:
    """مولِّدٌ من جدولٍ معلن: سؤال ← اقتراحات (مثلًا ما اقترحه نموذجٌ لغويٌّ وسُجّل)."""

    table: dict[str, tuple[Proposal, ...]]
    seen: list[str] = field(default_factory=list)

    def propose(self, q: GoldQuestion, verdict: Verdict, base: Base) -> Sequence[Proposal]:
        self.seen.append(q.question_id)
        return self.table.get(q.question_id, ())


@dataclass(frozen=True, slots=True)
class TableWitness:
    """شاهدٌ من جدولٍ معلن: معرّفُ القاعدة ← دليلُها من مصدرٍ مودَعٍ ببصمته."""

    table: dict[str, Evidence]

    def evidence_for(self, proposal: Proposal) -> Evidence | None:
        return self.table.get(proposal.rule_id)


@dataclass(frozen=True, slots=True)
class Event:
    """حادثةٌ في السجلّ: «اقتراح»، «قبول»، «رفض»، «سحب»، «ردّ الجولة»."""

    kind: str
    subject: str
    reason: str


@dataclass(frozen=True, slots=True)
class Round:
    """جولةٌ واحدة: الرصيدُ بعدها، والقياسُ قبلها وبعدها، والسجلّ."""

    base: Base
    train_before: Score
    train_after: Score
    held_out_before: Score
    held_out_after: Score
    events: tuple[Event, ...]
    accepted: bool


def _key(p: Proposal) -> str:
    return f"{'رافع' if isinstance(p, Licence) else 'قاعدة'}:{p.rule_id}"


def _admit(p: Proposal, ev: Evidence) -> Proposal:
    if isinstance(p, Licence):
        if ev.genus is Genus.فرضية:
            raise WorldKnowledgeError("الفرضيّةُ لا ترفع قاعدة")
        return Licence(p.rule_id, p.ground, ev)
    return p.admit(ev)


def _wrong_paths(base: Base, qs: Sequence[GoldQuestion], marks: dict[str, Mark]) -> set[str]:
    out: set[str] = set()
    for q in qs:
        if marks[q.question_id] is Mark.خطأ:
            v = base.ask(q)
            out |= {f"قاعدة:{s.rule_id}" for s in v.path}
            out |= {f"رافع:{s.rule_id}" for s in v.path if s.licence is not None}
    return out


def learn_round(
    base: Base,
    train: Sequence[GoldQuestion],
    held_out: Sequence[GoldQuestion],
    generator: Generator,
    witness: Witness,
) -> Round:
    """جولةٌ واحدةٌ من الحلقة."""

    tr0, tr_marks = measure(base, train)
    ho0, _ = measure(base, held_out)
    events: list[Event] = []
    proposals: dict[str, Proposal] = {}
    for q in train:
        if tr_marks[q.question_id] in (Mark.ناقص, Mark.صامت):
            for p in generator.propose(q, base.ask(q), base):
                if _key(p) not in proposals:
                    proposals[_key(p)] = p
                    events.append(Event("اقتراح", _key(p), q.question_id))
    known = {f"قاعدة:{r.rule_id}" for r in base.rules if r.admission is Admission.مقبول}
    known |= {f"رافع:{lic.rule_id}" for lic in base.licences if not lic.is_candidate}
    rules = {r.rule_id: r for r in base.rules}
    licences = {lic.rule_id: lic for lic in base.licences}
    admitted_now: set[str] = set()
    for key, p in proposals.items():
        if key in known:
            events.append(Event("رفض", key, "مقبولٌ أصلًا"))
            continue
        ev = witness.evidence_for(p)
        final: Proposal = p
        if ev is None:
            events.append(Event("رفض", key, "لا شاهدَ مستقلّ؛ يبقى مرشَّحًا"))
        else:
            try:
                final = _admit(p, ev)
                admitted_now.add(key)
                events.append(Event("قبول", key, f"{ev.genus.name}: {ev.source}"))
            except WorldKnowledgeError as err:
                events.append(Event("رفض", key, str(err)))
        if isinstance(final, Licence):
            licences[final.rule_id] = final
        else:
            rules.setdefault(final.rule_id, final)
            if final.admission is Admission.مقبول:
                rules[final.rule_id] = final
    new = Base(tuple(rules.values()), tuple(lic for lic in licences.values()
                                              if lic.rule_id in rules))
    tr1, tr1_marks = measure(new, train)
    ho1, ho1_marks = measure(new, held_out)
    if tr1.wrong > tr0.wrong or ho1.wrong > ho0.wrong:
        guilty = (_wrong_paths(new, train, tr1_marks) | _wrong_paths(new, held_out, ho1_marks))
        guilty &= admitted_now
        for key in sorted(guilty):
            events.append(Event("سحب", key, "أنتج جوابًا خاطئًا"))
        new = Base(
            tuple(r for r in new.rules if f"قاعدة:{r.rule_id}" not in guilty),
            tuple(lic for lic in new.licences if f"رافع:{lic.rule_id}" not in guilty),
        )
        tr1, _ = measure(new, train)
        ho1, _ = measure(new, held_out)
    if tr1.wrong > tr0.wrong or ho1.wrong > ho0.wrong:
        events.append(Event("ردّ الجولة", "*", "بقي خطأٌ زائدٌ بعد السحب"))
        return Round(base, tr0, tr0, ho0, ho0, tuple(events), False)
    return Round(new, tr0, tr1, ho0, ho1, tuple(events), True)


def learn(
    base: Base,
    train: Sequence[GoldQuestion],
    held_out: Sequence[GoldQuestion],
    generator: Generator,
    witness: Witness,
    max_rounds: int = 10,
) -> list[Round]:
    """كرّر الجولات حتى لا يتغيّر الرصيد."""

    rounds: list[Round] = []
    for _ in range(max_rounds):
        r = learn_round(base, train, held_out, generator, witness)
        rounds.append(r)
        if r.base == base:
            break
        base = r.base
    return rounds
