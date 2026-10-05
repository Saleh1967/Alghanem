"""المعرفةُ بالعالم: قواعدُ لزومٍ بدرجتها ومنزلتها ودليلها، والاستدلالُ بالصور المنتجة وحدها.

منقولٌ من `alghanem/src/alghanem/ontology/world_knowledge.py` بلا اعتمادٍ على الغانم.
والفرقُ الجوهريّ أنّ قرارَ «أهذه الصورةُ منتجة؟» لا يُكتب هنا شرطًا باليد: يُحسب من
جدول البتّات (`productive`) الذي برهن Lean أنه جدولُ الغزالي بعينه
(`Slge.Ghazali.ghazali_table`)، وتطابقُ الحسابين يفحصه `tests/test_conformance.py`.

والمنهج (النبهاني، «التفكير»): الحكمُ بالمعلومات السابقة لا بالآراء. فما يقترحه مولِّدٌ
**رأيٌ** يدخل `Admission.مرشح` ولا يُنتج أبدًا؛ ولا يصير معلومةً إلّا بدليلٍ جنسُه
موافقٌ لمنزلة القاعدة (`GENERA_OF_STANDING`). والعاديُّ لا يُقبل بلا موانعَ مسمّاة،
لأنّ «الاقتران بين ما يعتقد في العادة سببًا وما يعتقد مسبَّبًا ليس ضروريًّا» (التهافت).
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from enum import Enum
from typing import Final

__all__ = [
    "GENERA_OF_STANDING",
    "MAFHUM_ROUTE",
    "Admission",
    "Degree",
    "Evidence",
    "Form",
    "Genus",
    "Licence",
    "LicenceGround",
    "Literal",
    "Outcome",
    "Standing",
    "Step",
    "Verdict",
    "WorldKnowledgeError",
    "WorldRule",
    "infer",
    "productive",
]


class WorldKnowledgeError(ValueError):
    """قاعدةٌ أو رافعٌ لا يستوفي شرطه."""


class Degree(Enum):
    """درجةُ اللزوم: المقدَّمُ أخصُّ من التالي، أو مساوٍ له."""

    اخص = "akhass"
    مساو = "musawi"


class Form(Enum):
    """صورُ الاستثناء الأربع في الشرطيّ المتّصل."""

    عين_المقدم = "ayn_muqaddam"
    نقيض_التالي = "naqid_tali"
    نقيض_المقدم = "naqid_muqaddam"
    عين_التالي = "ayn_tali"


_MODELS: Final[tuple[tuple[bool, bool], ...]] = (
    (False, False), (False, True), (True, False), (True, True),
)


def _holds(d: Degree, a: bool, b: bool) -> bool:
    return (not a or b) if d is Degree.اخص else a == b


def _premise(f: Form, a: bool, b: bool) -> bool:
    return {Form.عين_المقدم: a, Form.نقيض_التالي: not b,
            Form.نقيض_المقدم: not a, Form.عين_التالي: b}[f]


def _conclusion(f: Form, a: bool, b: bool) -> bool:
    return {Form.عين_المقدم: b, Form.نقيض_التالي: not a,
            Form.نقيض_المقدم: not b, Form.عين_التالي: a}[f]


def productive(d: Degree, f: Form) -> bool:
    """منتجة: النتيجةُ صادقةٌ في كلّ نموذجٍ ثنائيٍّ يصدق فيه القيدُ والمقدّمة.

    نظيرُ `Slge.Ghazali.productive` حرفًا؛ وجدولُها مبرهَنٌ أنه جدولُ الغزالي.
    """

    return all(
        _conclusion(f, a, b) for a, b in _MODELS if _holds(d, a, b) and _premise(f, a, b)
    )


class Standing(Enum):
    """منزلةُ القاعدة: من أين ثبت اللزوم."""

    تعريفي = "definitional"
    وضعي = "lexical"
    عادي = "habitual"
    شرعي = "textual"

    @property
    def is_defeasible(self) -> bool:
        """العاديُّ وحده قابلٌ للنقض."""

        return self is Standing.عادي


class Genus(Enum):
    """جنسُ الدليل."""

    تعريف_مشترط = "stipulated_definition"
    شاهد_معجمي = "lexical_attestation"
    مشاهدة = "direct_observation"
    قياس_كمي = "measurement"
    خبر_مقبول = "accepted_report"
    فرضية = "declared_hypothesis"


GENERA_OF_STANDING: Final[dict[Standing, frozenset[Genus]]] = {
    Standing.تعريفي: frozenset({Genus.تعريف_مشترط, Genus.شاهد_معجمي}),
    Standing.وضعي: frozenset({Genus.شاهد_معجمي}),
    Standing.عادي: frozenset({Genus.مشاهدة, Genus.قياس_كمي, Genus.خبر_مقبول}),
    Standing.شرعي: frozenset({Genus.خبر_مقبول}),
}
"""العاديُّ لا يقبل شهادةَ المعجم: المعجمُ يثبت وضعَ اللفظ لا وقوعَ الاقتران في الوجود.
والفرضيّةُ لا تُثبت منزلةً أصلًا."""


@dataclass(frozen=True, slots=True)
class Evidence:
    """دليلٌ مسمّى: جنسُه ونصُّه ومصدرُه وبصمةُ المصدر إن كان ملفًّا."""

    evidence_id: str
    genus: Genus
    statement: str
    source: str
    sha256: str | None = None

    def __post_init__(self) -> None:
        if not (self.evidence_id.strip() and self.statement.strip() and self.source.strip()):
            raise WorldKnowledgeError("الدليلُ له اسمٌ ونصٌّ ومصدر")


class Admission(Enum):
    """حالُ القاعدة: مرشَّحٌ من مولِّدٍ لا يُستعمل، أو مقبولٌ بدليل."""

    مرشح = "candidate"
    مقبول = "admitted"


@dataclass(frozen=True, slots=True)
class WorldRule:
    """قاعدةُ لزومٍ واحدة: كلّما وُجد المقدَّمُ وُجد التالي، بدرجةٍ ومنزلةٍ ودليل."""

    rule_id: str
    antecedent: str
    consequent: str
    degree: Degree
    standing: Standing
    admission: Admission
    origin: str
    evidence: Evidence | None = None
    blocker_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("rule_id", "antecedent", "consequent", "origin"):
            if not getattr(self, name).strip():
                raise WorldKnowledgeError(f"{name} نصٌّ غير فارغ")
        if self.antecedent == self.consequent:
            raise WorldKnowledgeError("المقدَّمُ والتالي شيئان لا شيءٌ واحد")
        if self.admission is Admission.مقبول:
            if self.evidence is None:
                raise WorldKnowledgeError("قاعدةٌ مقبولةٌ بلا دليل: مرشَّحٌ في ثوب مقبول")
            if self.evidence.genus not in GENERA_OF_STANDING[self.standing]:
                raise WorldKnowledgeError(
                    f"جنسُ الدليل {self.evidence.genus.name} لا يثبت منزلة {self.standing.name}"
                )
        if self.standing.is_defeasible and not self.blocker_ids:
            raise WorldKnowledgeError("قاعدةٌ عاديّةٌ بلا مانعٍ مسمّى: قاطعةٌ في ثوب عادة")

    def admit(self, evidence: Evidence) -> WorldRule:
        """ارفع المرشَّح إلى مقبولٍ بدليل؛ ولا يُقبل مقبولٌ مرّتين."""

        if self.admission is Admission.مقبول:
            raise WorldKnowledgeError("القاعدةُ مقبولةٌ أصلًا")
        return replace(self, admission=Admission.مقبول, evidence=evidence)


class LicenceGround(Enum):
    """ما يرفع الأخصَّ إلى المساوي."""

    علة_واحدة = "single_cause"
    وصف_مفهم = "causal_description"
    سياق = "context"
    أداة_شرط = "conditional_particle"


MAFHUM_ROUTE: Final[dict[str, tuple[Form, LicenceGround | None]]] = {
    "موافقة": (Form.عين_المقدم, None),
    "مخالفة_صفة": (Form.نقيض_المقدم, LicenceGround.وصف_مفهم),
    "مخالفة_شرط": (Form.نقيض_المقدم, LicenceGround.أداة_شرط),
}
"""طريقُ كلّ مفهومٍ من `semantics.MAFHUM` إلى صورة: الموافقةُ سلسلةُ أخصّ (عينُ المقدَّم)،
والمخالفةُ نقيضُ المقدَّم ولا تُنتج إلّا برافع. ومخالفةُ الغاية والعدد لم يُكتب لهما
طريقٌ بعد، وهما مسجّلتان سؤالًا مفتوحًا."""


@dataclass(frozen=True, slots=True)
class Licence:
    """رافعُ قاعدةٍ بعينها إلى المساواة، بسببٍ مسمّى ودليل."""

    rule_id: str
    ground: LicenceGround
    evidence: Evidence

    @property
    def is_candidate(self) -> bool:
        """رافعٌ دليلُه فرضيّة: رأيٌ مقترحٌ لا يدخل الإنتاج."""

        return self.evidence.genus is Genus.فرضية


@dataclass(frozen=True, slots=True)
class Literal:
    """مفهومٌ مثبَتٌ أو منفيّ."""

    concept: str
    affirmed: bool


class Outcome(Enum):
    """مخرجُ الاستدلال؛ وكلُّ ما ليس إنتاجًا يُسمّى سببه."""

    منتج = "produced"
    غير_منتج = "non_productive_form"
    ناقص = "needs_admission"
    لا_طريق = "no_path"


@dataclass(frozen=True, slots=True)
class Step:
    """خطوةٌ واحدة: قاعدة، وصورة، ورافعٌ إن استُعمل."""

    rule_id: str
    form: Form
    licence: LicenceGround | None


@dataclass(frozen=True, slots=True)
class Verdict:
    """نتيجةُ الاستدلال بطريقها كلّه."""

    outcome: Outcome
    conclusion: Literal | None
    would_conclude: Literal | None
    path: tuple[Step, ...]
    defeasible: bool
    blocked_by: tuple[str, ...]
    note: str


def _moves(rule: WorldRule, at: Literal, lifted: bool) -> list[tuple[Literal, Form, bool]]:
    """الانتقالاتُ من حرفٍ عبر قاعدة: (إلى، الصورة، أهي منتجة بالجدول المبرهَن)."""

    degree = Degree.مساو if lifted else rule.degree
    moves: list[tuple[Literal, Form, bool]] = []
    if at.concept == rule.antecedent:
        form = Form.عين_المقدم if at.affirmed else Form.نقيض_المقدم
        moves.append((Literal(rule.consequent, at.affirmed), form, productive(degree, form)))
    if at.concept == rule.consequent:
        form = Form.عين_التالي if at.affirmed else Form.نقيض_التالي
        moves.append((Literal(rule.antecedent, at.affirmed), form, productive(degree, form)))
    return moves


def _search(
    given: Literal,
    target: str,
    rules: tuple[WorldRule, ...],
    licences: dict[str, Licence],
    allow_candidates: bool,
    allow_unproductive: bool,
) -> tuple[Literal, tuple[Step, ...]] | None:
    queue: deque[tuple[Literal, tuple[Step, ...]]] = deque([(given, ())])
    seen = {given}
    while queue:
        at, path = queue.popleft()
        if at.concept == target and path:
            return at, path
        for rule in rules:
            if rule.admission is Admission.مرشح and not allow_candidates:
                continue
            licence = licences.get(rule.rule_id)
            for nxt, form, ok in _moves(rule, at, licence is not None):
                if (not ok and not allow_unproductive) or nxt in seen:
                    continue
                seen.add(nxt)
                used = (
                    licence.ground
                    if licence is not None and not productive(rule.degree, form)
                    else None
                )
                queue.append((nxt, (*path, Step(rule.rule_id, form, used))))
    return None


def infer(
    given: Literal,
    target: str,
    rules: tuple[WorldRule, ...],
    licences: tuple[Licence, ...] = (),
    present_blockers: frozenset[str] = frozenset(),
) -> Verdict:
    """من حرفٍ معطًى إلى حكمٍ في مفهوم: بالمقبول وحده، وبالصور المنتجة وحدها.

    فإن لم يوجد طريقٌ منتجٌ سُمّي السبب: طريقٌ يمرّ بمرشَّح (`ناقص`)، أو طريقٌ لا يقوم إلّا
    بصورةٍ عقيمةٍ بلا رافع (`غير_منتج`)، أو لا طريقَ أصلًا (`لا_طريق`).
    """

    by_id = {rule.rule_id: rule for rule in rules}
    if len(by_id) != len(rules):
        raise WorldKnowledgeError("معرّفُ القاعدة مكرّر")
    for lic in licences:
        if lic.rule_id not in by_id:
            raise WorldKnowledgeError(f"رافعٌ لقاعدةٍ غير موجودة: {lic.rule_id}")
    admitted = {lic.rule_id: lic for lic in licences if not lic.is_candidate}
    every = {lic.rule_id: lic for lic in licences}
    found = _search(given, target, rules, admitted, False, False)
    if found is not None:
        conclusion, path = found
        used = [by_id[step.rule_id] for step in path]
        blocked = tuple(sorted({b for r in used for b in r.blocker_ids if b in present_blockers}))
        if blocked:
            return Verdict(Outcome.لا_طريق, None, None, path, True, blocked, "مانعٌ قائم")
        defeasible = any(r.standing.is_defeasible for r in used) or any(
            s.licence is not None for s in path
        )
        return Verdict(Outcome.منتج, conclusion, conclusion, path, defeasible, (), "")
    pending = _search(given, target, rules, every, True, False)
    if pending is not None:
        would, path = pending
        waiting = [
            s.rule_id for s in path
            if by_id[s.rule_id].admission is Admission.مرشح
            or (s.licence is not None and every[s.rule_id].is_candidate)
        ]
        return Verdict(Outcome.ناقص, None, would, path, False, (),
                       "مرشَّحٌ لم يُقبل: " + "، ".join(waiting))
    fallacy = _search(given, target, rules, admitted, True, True)
    if fallacy is not None:
        return Verdict(Outcome.غير_منتج, None, None, fallacy[1], False, (),
                       "«وأما عين التالي ونقيض المقدم فلا ينتجان» ما لم تُرفع القاعدةُ إلى المساواة")
    return Verdict(Outcome.لا_طريق, None, None, (), False, (), "")
