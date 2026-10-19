"""كم قاعدة ينقص كل سؤال: مولد يقترح، ودليل مستقل يقبل، وأسئلة ذهبية تقيس الفجوة.

المنهج منهج النبهاني في «التفكير» (ملف المكتبة الشاملة المرفوع، بصمته
`e917d9a0…c2de492c`): العقل «نقل الحس بالواقع بواسطة الحواس إلى الدماغ، ووجود
معلومات سابقة يفسر بواسطتها هذا الواقع»، و«فالمحتم في الطريقة العقلية ليس وجود رأي
أو آراء سابقة عن الواقع، بل وجود معلومات سابقة عنه… مع الحيلولة دون وجود الرأي عند
العملية ودون تدخله». فما يقترحه المولد **رأي سابق**: يدخل `Admission.مرشح` أو رافعا
دليله `DECLARED_HYPOTHESIS`، ولا يدخل حكما أبدا. والمعلومة السابقة قاعدة مقبولة
بدليل.

والخاصية محسوسة: «والقدر هو الخاصية التي يحدثها الإنسان في الشيء كالإحراق الذي في
النار، والقطع الذي في السكين. وهذه الخاصية شيء محسوس يدركه الحس» (الشخصية
الإسلامية ج١، الملف المرفوع `5e327aa2…c88e17`). فالقاعدة العادية لا تقبل إلا بحس
أو خبر عنه، على ما في `world_knowledge._GENERA_OF_STANDING`.

**والاستقلال شرط القياس**: الأسئلة ذهبية من أمثلة ج٣ نفسها بأسطرها، فلا يقبل دليل
من ج٣ لقاعدة على طريق جوابها؛ الأدلة المقبولة هنا من النص القرآني المودع في هذه
الشجرة، ومن صحيح البخاري ولسان العرب ببصمتيهما، لا من الكتاب الذي أخذ منه الجواب.

والمولد هنا نموذج لغوي (Claude Opus 5.5) اقترح القواعد والروافع في
`GENERATED_RULES` و`GENERATED_LICENCES`؛ وهي مسماة بمصدرها ولا يدعى صوابها.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final

from ..ontology.epistemics import Evidence, EvidenceGenus, Scope
from ..ontology.world_knowledge import (
    Admission,
    Degree,
    EquivalenceGround,
    EquivalenceLicence,
    Literal,
    Outcome,
    Standing,
    Verdict,
    WorldRule,
    infer,
)

__all__ = [
    "ADMITTED_RULES",
    "GENERATED_LICENCES",
    "GENERATED_RULES",
    "GENERATOR",
    "GOLD_QUESTIONS",
    "GoldQuestion",
    "QURAN_WITNESSES",
    "gap_reading",
]

GENERATOR: Final[str] = "Claude Opus 5.5 (مولد؛ رأي سابق)"
J3: Final[str] = "hamil:shakhsiyya_j3_matn.txt sha256 520b8e9d…bfc783"
_SCOPE: Final[Scope] = Scope(domain_id="أسئلة-الفجوة")

QURAN_WITNESSES: Final[dict[str, tuple[int, str]]] = {
    "أف-محرم": (2052, "فلا تقل لهما أف"),
    "حمل-نفقة": (5223, "وإن كن أولات حمل فأنفقوا عليهن"),
    "بيع-محرم": (5186, "وذروا البيع"),
}
"""سطر الآية في `corpora/quran-simple-enhanced.txt` ونصها بلا حركات؛ يفحصه الاختبار."""


def _evidence(
    evidence_id: str, genus: EvidenceGenus, statement: str, source: str
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=genus,
        statement=statement,
        source_name=source,
        scope=_SCOPE,
    )


def _quran(rule_id: str) -> Evidence:
    line, text = QURAN_WITNESSES[rule_id]
    return _evidence(
        f"قرآن-{line}",
        EvidenceGenus.ACCEPTED_REPORT,
        text,
        f"corpora/quran-simple-enhanced.txt:{line}",
    )


def _rule(
    rule_id: str,
    antecedent: str,
    consequent: str,
    standing: Standing,
    evidence: Evidence | None,
    blockers: tuple[str, ...] = (),
) -> WorldRule:
    return WorldRule(
        rule_id=rule_id,
        antecedent=antecedent,
        consequent=consequent,
        degree=Degree.اخص,
        standing=standing,
        admission=Admission.مقبول if evidence is not None else Admission.مرشح,
        origin="دليل مستقل" if evidence is not None else GENERATOR,
        evidence=evidence,
        blocker_ids=blockers,
    )


ADMITTED_RULES: Final[tuple[WorldRule, ...]] = (
    _rule("أف-محرم", "أف", "محرم في حق الوالدين", Standing.شرعي, _quran("أف-محرم")),
    _rule("حمل-نفقة", "حامل", "تجب النفقة", Standing.شرعي, _quran("حمل-نفقة")),
    _rule(
        "بيع-محرم",
        "بيع عند النداء",
        "محرم عند النداء",
        Standing.شرعي,
        _quran("بيع-محرم"),
    ),
    _rule(
        "سائمة-زكاة",
        "سائمة",
        "تجب الزكاة",
        Standing.شرعي,
        _evidence(
            "بخاري-سائمة",
            EvidenceGenus.ACCEPTED_REPORT,
            "وفي صدقة الغنم في سائمتها إذا كانت أربعين",
            "hamil:bukhari_sahih_sham.txt sha256 16f95173…87ac8132",
        ),
    ),
    _rule(
        "أف-أذى",
        "أف",
        "أذى",
        Standing.وضعي,
        _evidence(
            "لسان-أفف",
            EvidenceGenus.LEXICAL_ATTESTATION,
            "ثم استعمل ذلك عند كل شيء يضجر منه ويتأذى به",
            "OpenITI 0711IbnManzurIfriqi.LisanCarab.JK000880 sha256 4d77d42d…fd3257",
        ),
    ),
    _rule(
        "إنسان-حيوان",
        "إنسان",
        "حيوان",
        Standing.تعريفي,
        _evidence(
            "حد-الإنسان",
            EvidenceGenus.STIPULATED_DEFINITION,
            "إن كان الشخص الذي ظهر عن بعد إنسانا فهو حيوان",
            "OpenITI 0505Ghazali.MicyarCilm sha256 b8b0f6a1…dac4e28e",
        ),
    ),
)
"""قواعد مقبولة بدليل مستقل عن ج٣: أحكام الأصل من النص، ووضع «أف» من اللسان."""

GENERATED_RULES: Final[tuple[WorldRule, ...]] = (
    _rule("أذى-محرم", "أذى", "محرم في حق الوالدين", Standing.شرعي, None),
    _rule("ضرب-أذى", "ضرب", "أذى", Standing.عادي, None, ("ضرب لا يؤلم",)),
    _rule("إلهاء-محرم", "إلهاء عن الجمعة", "محرم عند النداء", Standing.شرعي, None),
    _rule(
        "إجارة-إلهاء",
        "إجارة عند النداء",
        "إلهاء عن الجمعة",
        Standing.عادي,
        None,
        ("إجارة لا تشغل",),
    ),
    _rule(
        "قرى-رماد",
        "كثير القرى",
        "كثير رماد القدر",
        Standing.عادي,
        None,
        ("رماد لغير القرى",),
    ),
)
"""ما اقترحه المولد من قواعد؛ كلها مرشحة، لأن دليلها المستقل لم يقدم."""


def _proposal(rule_id: str, ground: EquivalenceGround) -> EquivalenceLicence:
    return EquivalenceLicence(
        rule_id,
        ground,
        _evidence(
            f"اقتراح-{rule_id}",
            EvidenceGenus.DECLARED_HYPOTHESIS,
            f"رافع مقترح لـ{rule_id}",
            GENERATOR,
        ),
    )


GENERATED_LICENCES: Final[tuple[EquivalenceLicence, ...]] = (
    _proposal("سائمة-زكاة", EquivalenceGround.وصف_مفهم),
    _proposal("حمل-نفقة", EquivalenceGround.أداة_شرط),
    _proposal("قرى-رماد", EquivalenceGround.سياق),
)
"""روافع مقترحة؛ دليلها فرضية معلنة فلا تدخل الانتاج."""


@dataclass(frozen=True, slots=True)
class GoldQuestion:
    """سؤال ذهبي: جوابه في مصدره بسطره، ولا يقرأ المحرك ذلك المصدر."""

    question_id: str
    text: str
    given: Literal
    target: str
    expected: Literal | None
    gold_locus: str


GOLD_QUESTIONS: Final[tuple[GoldQuestion, ...]] = (
    GoldQuestion(
        "موافقة",
        "هل يحرم ضرب الوالدين؟",
        Literal("ضرب", True),
        "محرم في حق الوالدين",
        Literal("محرم في حق الوالدين", True),
        f"{J3}:519",
    ),
    GoldQuestion(
        "مخالفة-صفة",
        "هل تجب الزكاة في الغنم المعلوفة؟",
        Literal("سائمة", False),
        "تجب الزكاة",
        Literal("تجب الزكاة", False),
        f"{J3}:529",
    ),
    GoldQuestion(
        "مخالفة-شرط",
        "هل تجب النفقة على المطلقة غير الحامل؟",
        Literal("حامل", False),
        "تجب النفقة",
        Literal("تجب النفقة", False),
        f"{J3}:534",
    ),
    GoldQuestion(
        "قياس",
        "هل تحرم الإجارة عند أذان الجمعة؟",
        Literal("إجارة عند النداء", True),
        "محرم عند النداء",
        Literal("محرم عند النداء", True),
        f"{J3}:801",
    ),
    GoldQuestion(
        "ضابط-منطقي",
        "إذا لم يكن الشخص إنسانا، أيلزم أنه ليس حيوانا؟",
        Literal("إنسان", False),
        "حيوان",
        None,
        "OpenITI 0505Ghazali.MicyarCilm: «فلا ينتج… إذ ربما يكون فرسا»",
    ),
    GoldQuestion(
        "كناية",
        "هل يفيد «كثير رماد القدر» أنه مضياف؟",
        Literal("كثير رماد القدر", True),
        "كثير القرى",
        Literal("كثير القرى", True),
        "OpenITI 0471CabdQahirJurjani.DalailIcjaz.Shamela0012055 §304",
    ),
)


def _missing(verdict: Verdict) -> list[str]:
    candidates = {rule.rule_id for rule in GENERATED_RULES}
    proposals = {lic.rule_id for lic in GENERATED_LICENCES}
    out: list[str] = []
    for step in verdict.path:
        if step.rule_id in candidates:
            out.append(f"قاعدة:{step.rule_id}")
        if step.licence is not None and step.rule_id in proposals:
            out.append(f"رافع:{step.rule_id}")
    return out


def gap_reading() -> dict[str, Any]:
    """لكل سؤال: الحكم بالمعلومات المقبولة وحدها، وما ينقصه، ولو قبل ما ينقصه."""

    rules = ADMITTED_RULES + GENERATED_RULES
    rows: dict[str, Any] = {}
    for question in GOLD_QUESTIONS:
        verdict = infer(question.given, question.target, rules, GENERATED_LICENCES)
        missing = _missing(verdict) if verdict.outcome is Outcome.ناقص else []
        if question.expected is None:
            agrees = verdict.outcome is Outcome.غير_منتج
        else:
            agrees = verdict.would_conclude == question.expected
        rows[question.question_id] = {
            "outcome": verdict.outcome.value,
            "missing": missing,
            "would_agree_with_gold": agrees,
        }
    return rows
