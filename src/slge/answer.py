"""الجواب: حكمٌ من `infer` يصير جملًا، ولكلّ جملةٍ وسمُها وسندُها.

هذا هو الشكلُ الذي ينافس به المحرّكُ جوابَ نموذجٍ لغويٍّ كبير: الطلاقةُ قد تأتي من مُعيدٍ
لغويّ (`Verbalizer`)، لكنّ المُعيدَ يُعيد صياغةَ جملةٍ واحدةٍ في كلّ مرّة، ولا يملك أن
يضيف جملةً أو يحذف وسمًا أو يغيّر سندًا: `verbalize` يبني الجوابَ من جمل `compose`
بأعيانها ويُلصق بكلّ صياغةٍ وسمَ أصلها. فما في الجواب من حكمٍ هو ما في الطريق، لا أكثر.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from .knowledge import Degree, Form, Licence, Outcome, Verdict, WorldRule, productive
from .status import Status

__all__ = ["Answer", "Sentence", "Verbalizer", "compose", "render", "verbalize"]

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


def _lit(concept: str, affirmed: bool) -> str:
    return concept if affirmed else f"ليس {concept}"


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
        for step in verdict.path:
            r = rules[step.rule_id]
            assert r.evidence is not None  # المقبولُ وحده يُنتج
            out.append(Sentence(f"لأنّ «{r.antecedent}» يلزمه «{r.consequent}».",
                                Status.دليل, f"{r.rule_id} ← {r.evidence.source}"))
            degree = Degree.مساو if step.licence is not None else r.degree
            if step.licence is not None:
                lic = licences[step.rule_id]
                out.append(Sentence(f"ورُفعت القاعدةُ إلى المساواة ({step.licence.name}).",
                                    Status.دليل, f"رافع {step.rule_id} ← {lic.evidence.source}"))
            assert productive(degree, step.form)
            out.append(Sentence(f"وصورةُ «{_FORM_AR[step.form]}» منتجةٌ في {degree.name}.",
                                Status.مبرهن, "lean:Slge.Ghazali.ghazali_table"))
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


def render(answer: Answer) -> str:
    """الجوابُ نصًّا: كلُّ سطرٍ جملةٌ ووسمُها وسندُها."""

    lines = [answer.question]
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
    )
