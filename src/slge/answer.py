"""الجواب: حكمٌ من `infer` يصير جملًا، ولكلّ جملةٍ وسمُها وسندُها.

هذا هو الشكلُ الذي ينافس به المحرّكُ جوابَ نموذجٍ لغويٍّ كبير: الطلاقةُ قد تأتي من مُعيدٍ
لغويّ (`Verbalizer`)، لكنّ المُعيدَ يُعيد صياغةَ جملةٍ واحدةٍ في كلّ مرّة، ولا يملك أن
يضيف جملةً أو يحذف وسمًا أو يغيّر سندًا: `verbalize` يبني الجوابَ من جمل `compose`
بأعيانها ويُلصق بكلّ صياغةٍ وسمَ أصلها. فما في الجواب من حكمٍ هو ما في الطريق، لا أكثر.

ولكلّ جوابٍ **رتبة** (`rank.Rank`): يقينٌ أو ظنٌّ أو راجحٌ أو مرجوحٌ أو مردودٌ أو تعادل،
محسوبةً من طرق الإثبات والنفي معًا (`respond`)، وأسبابُها جملٌ في الجواب. والمُعيدُ لا يملكها.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from .knowledge import (
    Degree,
    Form,
    Licence,
    Literal,
    Outcome,
    Step,
    Verdict,
    WorldRule,
    infer,
    productive,
)
from .rank import Grade, Rank, Ranked, rank
from .status import Status

__all__ = ["Answer", "Sentence", "Verbalizer", "compose", "render", "respond", "verbalize"]

_FORM_AR = {
    Form.عين_المقدم: "عين المقدَّم",
    Form.نقيض_التالي: "نقيض التالي",
    Form.نقيض_المقدم: "نقيض المقدَّم",
    Form.عين_التالي: "عين التالي",
}


@dataclass(frozen=True, slots=True)
class Sentence:
    """جملةٌ واحدة بوسمها وسندها."""

    text: str
    status: Status
    support: str

    def __post_init__(self) -> None:
        if not self.text.strip() or not self.support.strip():
            raise ValueError("جملةٌ بلا نصٍّ أو بلا سند لا تُقال")


@dataclass(frozen=True, slots=True)
class Answer:
    """الجواب: السؤال، ومخرجُ الاستدلال، والجمل."""

    question: str
    outcome: Outcome
    sentences: tuple[Sentence, ...]
    rank: Rank = Rank.لا_علم


def _lit(concept: str, affirmed: bool) -> str:
    return concept if affirmed else f"ليس {concept}"


def _path_sentences(
    path: tuple[Step, ...], rules: Mapping[str, WorldRule], licences: Mapping[str, Licence]
) -> list[Sentence]:
    out: list[Sentence] = []
    for step in path:
        r = rules[step.rule_id]
        assert r.evidence is not None  # المقبولُ وحده يُنتج
        lazim = f"«{r.consequent}»" if r.positive else f"نفيُ «{r.consequent}»"
        out.append(Sentence(f"لأنّ «{r.antecedent}» يلزمه {lazim}.",
                            Status.دليل, f"{r.rule_id} ← {r.evidence.source}"))
        degree = Degree.مساو if step.licence is not None else r.degree
        if step.licence is not None:
            lic = licences[step.rule_id]
            out.append(Sentence(f"ورُفعت القاعدةُ إلى المساواة ({step.licence.name}).",
                                Status.دليل, f"رافع {step.rule_id} ← {lic.evidence.source}"))
        assert productive(degree, step.form)
        out.append(Sentence(f"وصورةُ «{_FORM_AR[step.form]}» منتجةٌ في {degree.name}.",
                            Status.مبرهن, "lean:Slge.Ghazali.ghazali_table"))
    return out


def compose(
    question: str,
    verdict: Verdict,
    rules: Mapping[str, WorldRule],
    licences: Mapping[str, Licence] | None = None,
) -> Answer:
    """ابنِ الجوابَ من الحكم وطريقه."""

    licences = licences or {}
    out: list[Sentence] = []
    if verdict.outcome is Outcome.منتج and verdict.conclusion is not None:
        c = verdict.conclusion
        head = f"نعم: {c.concept}." if c.affirmed else f"لا: {_lit(c.concept, False)}."
        out.append(Sentence(head, Status.دليل, "Outcome.منتج"))
        out += _path_sentences(verdict.path, rules, licences)
        if verdict.defeasible:
            blockers = sorted({b for s in verdict.path for b in rules[s.rule_id].blocker_ids})
            text = "وهذا ظنٌّ يُنقض بمانع" + (f": {'، '.join(blockers)}." if blockers else ".")
            out.append(Sentence(text, Status.معلن, "Standing.عادي/رافع"))
    elif verdict.outcome is Outcome.ناقص:
        out.append(Sentence("لا أحكم: المعلوماتُ المقبولةُ لا تكفي.", Status.معلن,
                            "Outcome.ناقص"))
        if verdict.would_conclude is not None:
            w = verdict.would_conclude
            out.append(Sentence(f"ولو قُبل المقترَحُ لكان: {_lit(w.concept, w.affirmed)}.",
                                Status.رأي, verdict.note))
    elif verdict.outcome is Outcome.غير_منتج:
        form = verdict.path[-1].form if verdict.path else Form.نقيض_المقدم
        out.append(Sentence(f"لا يلزم: صورةُ «{_FORM_AR[form]}» عقيمةٌ في الأخصّ.",
                            Status.مبرهن, "lean:Slge.Ghazali.barren_witnessed"))
    elif verdict.blocked_by:
        out.append(Sentence(f"لا أحكم: مانعٌ قائم ({'، '.join(verdict.blocked_by)}).",
                            Status.دليل, "Verdict.blocked_by"))
    else:
        out.append(Sentence("لا أعلم: لا طريقَ في المعلومات المقبولة.", Status.معلن,
                            "Outcome.لا_طريق"))
    return Answer(question, verdict.outcome, tuple(out))


_RANK_TEXT = {
    Rank.يقين: "يقين: كلُّ مقدّمةٍ قطعيّةُ الثبوت وكلُّ خطوةٍ قطعيّةُ الدلالة",
    Rank.ظن: "ظنّ: في الطريق ما لا يفيد إلّا الظنّ، والنتيجةُ تتبع أضعفَ مقدّماتها",
    Rank.راجح: "ظنٌّ راجح: عارضه ظنٌّ أقلُّ شواهدَ مستقلّة",
    Rank.مرجوح: "مرجوح",
    Rank.مردود: "مردود",
    Rank.تعادل: "تعادل",
    Rank.تناقض: "تناقض",
    Rank.مخصوص: "عامٌّ مخصوص",
    Rank.لا_علم: "لا علم",
}


def _grade_ar(g: Grade) -> str:
    return "قطعيّ" if g is Grade.قطعي else "ظنّيّ"


def _ranked_sentences(
    r: Ranked, rules: Mapping[str, WorldRule], licences: Mapping[str, Licence]
) -> list[Sentence]:
    out: list[Sentence] = []
    if r.rank is Rank.تعادل and r.side and r.opposing:
        out.append(Sentence(
            f"أتوقّف: للإثبات وللنفي {r.side.strength} شاهدٌ ظنّيٌّ مستقلٌّ لكلٍّ منهما، ولا مرجّح.",
            Status.مبرهن, "lean:Slge.Rank.taadul_iff"))
    elif r.rank is Rank.تناقض:
        out.append(Sentence(
            "لا أحكم: قطعيّان متعارضان، و«التعادل لا يقع بين الدليلين القطعيين» — فالخللُ في "
            "الرصيد المقبول لا في السؤال.", Status.مبرهن, "lean:Slge.Rank.tanaqud_iff"))
    elif r.conclusion is not None:
        c = r.conclusion
        head = f"نعم: {c.concept}." if c.affirmed else f"لا: {_lit(c.concept, False)}."
        out.append(Sentence(f"{head} — {_RANK_TEXT[r.rank]}.", Status.دليل, f"Rank.{r.rank.name}"))
    for why in r.reasons:
        out.append(Sentence(f"ثبوت: {why}.", Status.معلن, "rank.evidence_grade"))
    out.append(Sentence("والنتيجةُ لا ترقى فوق أضعف مقدّماتها، والقطعيُّ لا يُردّ.",
                        Status.مبرهن, "lean:Slge.Rank.no_promotion"))
    for path in r.support:
        out += _path_sentences(path, rules, licences)
    if r.opposing is not None and r.side is not None:
        loser = ("عامٌّ مخصوصٌ لا مردود: يُعمل به فيما سوى الخاصّ (ج٣ ¶1065)" if r.specialised
                 else "مردود" if r.rank is Rank.يقين
                 else "مرجوح" if r.rank is Rank.راجح else "مكافئ")
        towards = ("النقيض" if r.conclusion is None
                   else "النفي" if r.conclusion.affirmed else "الإثبات")
        out.append(Sentence(
            f"ويعارضه طريقٌ إلى {towards} {_grade_ar(r.opposing.grade)} "
            f"بـ{r.opposing.strength} شاهد، فهو {loser}.", Status.مبرهن,
            "lean:Slge.Rank.general_is_makhsus" if r.specialised else "lean:Slge.Rank.weigh_swap"))
        for path in r.opposition:
            out += _path_sentences(path, rules, licences)
    if r.rank in (Rank.ظن, Rank.راجح):
        out.append(Sentence("وهذا ظنٌّ يقبل الخطأ؛ يقوى بانضمام شاهدٍ مستقلّ، ويُردّ بقطعيٍّ يعارضه.",
                            Status.معلن, "الغزالي، محكّ النظر؛ التفكير"))
    return out


def respond(
    question: str,
    given: Literal | tuple[Literal, ...],
    target: str,
    rules: tuple[WorldRule, ...],
    licences: tuple[Licence, ...] = (),
    present_blockers: frozenset[str] = frozenset(),
) -> Answer:
    """الجوابُ برتبته: طرقُ الإثبات والنفي كلُّها، ثمّ الوزن، ثمّ الجمل."""

    first = given[0] if isinstance(given, tuple) else given

    by_id = {x.rule_id: x for x in rules}
    lic = {x.rule_id: x for x in licences}
    r = rank(given, target, rules, licences, present_blockers)
    if r.rank is Rank.لا_علم:
        base = compose(question, infer(first, target, rules, licences, present_blockers),
                       by_id, lic)
        return Answer(question, base.outcome, base.sentences, Rank.لا_علم)
    return Answer(question, Outcome.منتج if r.conclusion else Outcome.لا_طريق,
                  tuple(_ranked_sentences(r, by_id, lic)), r.rank)


def render(answer: Answer) -> str:
    """الجوابُ نصًّا: كلُّ سطرٍ جملةٌ ووسمُها وسندُها، والرتبةُ في رأسه."""

    lines = [f"{answer.question}  ⟦الرتبة: {answer.rank.name}⟧"]
    lines += [f"• {s.text} ⟦{s.status.name} · {s.support}⟧" for s in answer.sentences]
    return "\n".join(lines)


class Verbalizer(Protocol):
    """مُعيدُ صياغة (نموذجٌ لغويّ مثلًا): يأخذ جملةً واحدةً ويعيدها بعبارةٍ أخرى."""

    def rephrase(self, sentence: Sentence) -> str: ...


def verbalize(answer: Answer, verbalizer: Verbalizer) -> Answer:
    """أعد صياغةَ كلّ جملةٍ وحدها؛ والوسمُ والسندُ من الأصل لا من المُعيد."""

    return Answer(
        answer.question,
        answer.outcome,
        tuple(Sentence(verbalizer.rephrase(s), s.status, s.support) for s in answer.sentences),
        answer.rank,
    )
