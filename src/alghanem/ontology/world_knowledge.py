"""هيكل المعرفة بالعالم: قواعد اللزوم بدرجتها ومنزلتها ودليلها، وصيغ الانتاج المغلقة.

هذه الوحدة تبني فوق `InferenceRule` في `substance` ولا بجانبها: كل قاعدة مقبولة هنا
تتحول الى `InferenceRule` بالدالة `WorldRule.as_inference_rule`، فلا يقوم محرك ثان.
والذي تضيفه اربعة اشياء لم تكن في الرصيد، وكل واحد منها منقول عن نص مقروء:

* **درجة اللزوم** `Degree`: الملزوم اخص من اللازم او مساو له. نص الغزالي في محك
  النظر (OpenITI `0505Ghazali.MihakkNazar`، نمط التلازم): «فينبغي ألا يكون الملزوم
  أعم من اللازم ، بل إما أخص ، وإما مساويا».
* **صيغ الانتاج** `Form`: في معيار العلم (`0505Ghazali.MicyarCilm`): «والمنتج منه
  إثنان وهو عين المقدم ونقيض التالي. وأما عين التالي ونقيض المقدم فلا ينتجان».
  وفي محك النظر للمساوي: «معلول له علة واحدة وهو مساو لعلته، ويلزم أحدهما
  الآخر.. فينتج فيه التسليمات الأربع».
* **منزلة القاعدة** `Standing`: العادي قابل للنقض بنص التهافت (`0505Ghazali.Tahafut`):
  «الاقتران بين ما يعتقد في العادة سببا وما يعتقد مسببا ليس ضروريا عندنا».
  فالعادي لا يدخل الا بموانع مسماة، على شرط `InferenceRule` نفسه.
* **المرشح والمقبول** `Admission`: ما يقترحه مولد (نموذج لغوي، او قاعدة مستخرجة من
  الويب) يدخل مرشحا ولا يستعمل في انتاج ابدا؛ ولا يصير مقبولا الا بدليل جنسه
  موافق لمنزلته (`_GENERA_OF_STANDING`). فالمولد يقترح ولا يحكم.

والرافع الى المساواة `EquivalenceLicence` كائن مستقل بدليل: به وحده تنتج الصيغتان
اللتان لا تنتجان في الاخص، وهما صيغتا مفهوم المخالفة والكناية.

والوسط (ابن سينا، الاشارات `0428IbnSina.IsharatWaTanbihat`: «وأعني بالوسط ما يقرن
بقولنا لأنه») لا يكتب حقلا: يشتق من سلسلة القواعد التي مر بها الانتاج، فيظهر في
`Verdict.path` بعينه.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .epistemics import Evidence, EvidenceGenus
from .substance import InferenceRule, RuleKind

__all__ = [
    "Admission",
    "Degree",
    "EquivalenceGround",
    "EquivalenceLicence",
    "Form",
    "Literal",
    "Outcome",
    "Step",
    "Standing",
    "Verdict",
    "WorldKnowledgeError",
    "WorldRule",
    "infer",
]


class WorldKnowledgeError(ValueError):
    """قاعدة او رافع لا يستوفي شرطه."""


class Degree(Enum):
    """درجة اللزوم: الملزوم اخص من اللازم، او مساو له."""

    اخص = "akhass"
    مساو = "musawi"


class Standing(Enum):
    """منزلة القاعدة: من اين ثبت اللزوم."""

    تعريفي = "definitional"
    وضعي = "lexical"
    عادي = "habitual"
    شرعي = "textual"

    @property
    def is_defeasible(self) -> bool:
        """العادي وحده قابل للنقض: الاقتران فيه ليس ضروريا."""

        return self is Standing.عادي


_GENERA_OF_STANDING: Final[dict[Standing, frozenset[EvidenceGenus]]] = {
    Standing.تعريفي: frozenset(
        {EvidenceGenus.STIPULATED_DEFINITION, EvidenceGenus.LEXICAL_ATTESTATION}
    ),
    Standing.وضعي: frozenset({EvidenceGenus.LEXICAL_ATTESTATION}),
    Standing.عادي: frozenset(
        {
            EvidenceGenus.DIRECT_OBSERVATION,
            EvidenceGenus.MEASUREMENT,
            EvidenceGenus.ACCEPTED_REPORT,
        }
    ),
    Standing.شرعي: frozenset({EvidenceGenus.ACCEPTED_REPORT}),
}
"""جنس الدليل الذي يقبل كل منزلة. والعادي لا يقبل شهادة المعجم: المعجم يثبت وضع
اللفظ لا وقوع الاقتران في الوجود، على ما في `EvidenceGenus.is_fact_establishing`."""


class Admission(Enum):
    """حال القاعدة: مرشح من مولد لا يستعمل، او مقبول بدليل."""

    مرشح = "candidate"
    مقبول = "admitted"


@dataclass(frozen=True, slots=True)
class WorldRule:
    """قاعدة لزوم واحدة: كلما وجد المقدم وجد التالي، بدرجة ومنزلة ودليل."""

    rule_id: str
    antecedent: str
    consequent: str
    degree: Degree
    standing: Standing
    admission: Admission
    origin: str
    evidence: Evidence | None
    blocker_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("rule_id", "antecedent", "consequent", "origin"):
            if not getattr(self, name).strip():
                raise WorldKnowledgeError(f"{name} نص غير فارغ")
        if self.antecedent == self.consequent:
            raise WorldKnowledgeError("المقدم والتالي شيئان لا شيء واحد")
        if self.admission is Admission.مقبول:
            if self.evidence is None:
                raise WorldKnowledgeError("قاعدة مقبولة بلا دليل مرشح في ثوب مقبول")
            if self.evidence.genus not in _GENERA_OF_STANDING[self.standing]:
                raise WorldKnowledgeError(
                    f"جنس الدليل {self.evidence.genus.value} لا يثبت منزلة "
                    f"{self.standing.value}"
                )
        if self.standing.is_defeasible and not self.blocker_ids:
            raise WorldKnowledgeError(
                "العادي ليس ضروريا: قاعدة عادية بلا مانع مسمى قاطعة في ثوب عادة"
            )

    def admit(self, evidence: Evidence) -> WorldRule:
        """ارفع المرشح الى مقبول بدليل؛ ولا يقبل مقبول مرتين."""

        if self.admission is Admission.مقبول:
            raise WorldKnowledgeError("القاعدة مقبولة اصلا")
        return WorldRule(
            rule_id=self.rule_id,
            antecedent=self.antecedent,
            consequent=self.consequent,
            degree=self.degree,
            standing=self.standing,
            admission=Admission.مقبول,
            origin=self.origin,
            evidence=evidence,
            blocker_ids=self.blocker_ids,
        )

    def as_inference_rule(self, version: str = "1") -> InferenceRule:
        """القاعدة المقبولة في صورة `InferenceRule` الرصيد؛ والمرشح لا يتحول."""

        if self.admission is not Admission.مقبول or self.evidence is None:
            raise WorldKnowledgeError("المرشح لا يدخل الرصيد")
        return InferenceRule(
            rule_id=self.rule_id,
            version=version,
            kind=(
                RuleKind.DEFEASIBLE
                if self.standing.is_defeasible
                else RuleKind.STRICT_IN_THE_DECLARED_MODEL
            ),
            premise_patterns=(self.antecedent,),
            conclusion_pattern=self.consequent,
            applicability_note=f"{self.degree.value}/{self.standing.value}",
            blocker_ids=self.blocker_ids,
            evidence_ref=self.evidence.ref,
        )


class EquivalenceGround(Enum):
    """ما يرفع الاخص الى المساوي."""

    علة_واحدة = "single_cause"
    وصف_مفهم = "causal_description"
    سياق = "context"


@dataclass(frozen=True, slots=True)
class EquivalenceLicence:
    """رافع قاعدة بعينها الى المساواة، بسبب مسمى ودليل."""

    rule_id: str
    ground: EquivalenceGround
    evidence: Evidence

    def __post_init__(self) -> None:
        if not self.rule_id.strip():
            raise WorldKnowledgeError("الرافع يسمي قاعدته")


class Form(Enum):
    """صيغ الاستثناء الاربع في الشرطي المتصل."""

    عين_المقدم = "modus_ponens"
    نقيض_التالي = "modus_tollens"
    نقيض_المقدم = "denying_antecedent"
    عين_التالي = "affirming_consequent"

    @property
    def productive_for_akhass(self) -> bool:
        """«والمنتج منه إثنان وهو عين المقدم ونقيض التالي»."""

        return self in (Form.عين_المقدم, Form.نقيض_التالي)


@dataclass(frozen=True, slots=True)
class Literal:
    """مفهوم مثبت او منفي."""

    concept: str
    affirmed: bool


class Outcome(Enum):
    """مخرج الاستدلال؛ وكل ما ليس انتاجا يسمى سببه."""

    منتج = "produced"
    غير_منتج = "non_productive_form"
    ناقص = "needs_admission"
    لا_طريق = "no_path"


@dataclass(frozen=True, slots=True)
class Step:
    """خطوة واحدة: قاعدة، وصيغة، ورافع ان استعمل."""

    rule_id: str
    form: Form
    licence: EquivalenceGround | None


@dataclass(frozen=True, slots=True)
class Verdict:
    """نتيجة الاستدلال بطريقها كله."""

    outcome: Outcome
    conclusion: Literal | None
    path: tuple[Step, ...]
    defeasible: bool
    blocked_by: tuple[str, ...]
    note: str


def _moves(
    rule: WorldRule, at: Literal, licensed: bool
) -> list[tuple[Literal, Form, bool]]:
    """الانتقالات الممكنة من حرف عبر قاعدة: (الى، الصيغة، اهي منتجة)."""

    equal = rule.degree is Degree.مساو or licensed
    moves: list[tuple[Literal, Form, bool]] = []
    if at.concept == rule.antecedent:
        if at.affirmed:
            moves.append((Literal(rule.consequent, True), Form.عين_المقدم, True))
        else:
            moves.append((Literal(rule.consequent, False), Form.نقيض_المقدم, equal))
    if at.concept == rule.consequent:
        if at.affirmed:
            moves.append((Literal(rule.antecedent, True), Form.عين_التالي, equal))
        else:
            moves.append((Literal(rule.antecedent, False), Form.نقيض_التالي, True))
    return moves


def _search(
    given: Literal,
    target: str,
    rules: tuple[WorldRule, ...],
    licences: dict[str, EquivalenceLicence],
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
            for nxt, form, productive in _moves(rule, at, licence is not None):
                if not productive and not allow_unproductive:
                    continue
                if nxt in seen:
                    continue
                seen.add(nxt)
                used = (
                    licence.ground
                    if licence is not None
                    and rule.degree is Degree.اخص
                    and not form.productive_for_akhass
                    else None
                )
                queue.append((nxt, (*path, Step(rule.rule_id, form, used))))
    return None


def infer(
    given: Literal,
    target: str,
    rules: tuple[WorldRule, ...],
    licences: tuple[EquivalenceLicence, ...] = (),
    present_blockers: frozenset[str] = frozenset(),
) -> Verdict:
    """من حرف معطى الى حكم في مفهوم: بالمقبول وحده، وبالصيغ المنتجة وحدها.

    فان لم يوجد طريق منتج سمي السبب: طريق يمر بمرشح غير مقبول (`ناقص`)، او طريق
    لا يقوم الا بصيغة غير منتجة بلا رافع (`غير_منتج`)، او لا طريق اصلا.
    """

    by_id = {rule.rule_id: rule for rule in rules}
    licence_map = {lic.rule_id: lic for lic in licences}
    for lic in licences:
        if lic.rule_id not in by_id:
            raise WorldKnowledgeError(f"رافع لقاعدة غير موجودة: {lic.rule_id}")
    found = _search(given, target, rules, licence_map, False, False)
    if found is not None:
        conclusion, path = found
        used = [by_id[step.rule_id] for step in path]
        blocked = tuple(
            sorted(
                {b for rule in used for b in rule.blocker_ids if b in present_blockers}
            )
        )
        if blocked:
            return Verdict(Outcome.لا_طريق, None, path, True, blocked, "مانع قائم")
        return Verdict(
            Outcome.منتج,
            conclusion,
            path,
            any(rule.standing.is_defeasible for rule in used),
            (),
            "",
        )
    pending = _search(given, target, rules, licence_map, True, False)
    if pending is not None:
        _, path = pending
        waiting = [
            step.rule_id
            for step in path
            if by_id[step.rule_id].admission is Admission.مرشح
        ]
        return Verdict(
            Outcome.ناقص,
            None,
            path,
            False,
            (),
            "قاعدة مرشحة لم تقبل: " + "، ".join(waiting),
        )
    fallacy = _search(given, target, rules, licence_map, True, True)
    if fallacy is not None:
        _, path = fallacy
        return Verdict(
            Outcome.غير_منتج,
            None,
            path,
            False,
            (),
            "«وأما عين التالي ونقيض المقدم فلا ينتجان» ما لم ترفع القاعدة إلى المساواة",
        )
    return Verdict(Outcome.لا_طريق, None, (), False, (), "")
