"""هيكل المعرفة بالعالم على أمثلة الغزالي والجرجاني والنبهاني بنصوصها."""

import pytest

from alghanem.ontology.epistemics import Evidence, EvidenceGenus, Scope
from alghanem.ontology.substance import InferenceRule, RuleKind
from alghanem.ontology.world_knowledge import (
    Admission,
    Degree,
    EquivalenceGround,
    EquivalenceLicence,
    Form,
    Literal,
    Outcome,
    Standing,
    WorldKnowledgeError,
    WorldRule,
    infer,
)

_SCOPE = Scope(domain_id="عالم-الاختبار")


def _ev(evidence_id: str, genus: EvidenceGenus, source: str) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=genus,
        statement=evidence_id,
        source_name=source,
        scope=_SCOPE,
    )


_DEF = _ev("حد-الإنسان", EvidenceGenus.STIPULATED_DEFINITION, "0505Ghazali.MicyarCilm")
_SUN = _ev("مشاهدة-الشمس", EvidenceGenus.DIRECT_OBSERVATION, "0505Ghazali.MihakkNazar")

HUMAN = WorldRule(
    "إنسان-حيوان",
    "إنسان",
    "حيوان",
    Degree.اخص,
    Standing.تعريفي,
    Admission.مقبول,
    "معيار العلم",
    _DEF,
)
SUN = WorldRule(
    "شمس-نهار",
    "الشمس طالعة",
    "النهار موجود",
    Degree.مساو,
    Standing.عادي,
    Admission.مقبول,
    "محك النظر",
    _SUN,
    ("كسوف",),
)


def test_akhass_produces_exactly_the_two_forms_ghazali_names() -> None:
    rules = (HUMAN,)
    ponens = infer(Literal("إنسان", True), "حيوان", rules)
    assert ponens.outcome is Outcome.منتج
    assert ponens.conclusion == Literal("حيوان", True)
    assert ponens.path[0].form is Form.عين_المقدم
    tollens = infer(Literal("حيوان", False), "إنسان", rules)
    assert tollens.conclusion == Literal("إنسان", False)
    assert tollens.path[0].form is Form.نقيض_التالي
    for given, target, form in (
        (Literal("إنسان", False), "حيوان", Form.نقيض_المقدم),
        (Literal("حيوان", True), "إنسان", Form.عين_التالي),
    ):
        verdict = infer(given, target, rules)
        assert verdict.outcome is Outcome.غير_منتج
        assert verdict.path[0].form is form
        assert verdict.conclusion is None


def test_musawi_produces_all_four_forms() -> None:
    for given, target in (
        (Literal("الشمس طالعة", True), "النهار موجود"),
        (Literal("الشمس طالعة", False), "النهار موجود"),
        (Literal("النهار موجود", True), "الشمس طالعة"),
        (Literal("النهار موجود", False), "الشمس طالعة"),
    ):
        verdict = infer(given, target, (SUN,))
        assert verdict.outcome is Outcome.منتج, given
        assert verdict.conclusion == Literal(target, given.affirmed)
        assert verdict.defeasible


def test_a_present_blocker_stops_a_habitual_rule() -> None:
    verdict = infer(
        Literal("الشمس طالعة", True),
        "النهار موجود",
        (SUN,),
        present_blockers=frozenset({"كسوف"}),
    )
    assert verdict.outcome is Outcome.لا_طريق
    assert verdict.blocked_by == ("كسوف",)


def test_mafhum_muwafaqa_waits_on_its_unadmitted_link() -> None:
    uff = WorldRule(
        "أف-أذى",
        "أف",
        "أذى",
        Degree.اخص,
        Standing.وضعي,
        Admission.مقبول,
        "لسان العرب",
        _ev("لسان-أفف", EvidenceGenus.LEXICAL_ATTESTATION, "0711IbnManzurIfriqi"),
    )
    harm = WorldRule(
        "أذى-محرم",
        "أذى",
        "محرم في حق الوالدين",
        Degree.اخص,
        Standing.شرعي,
        Admission.مقبول,
        "فلا تقل لهما أف",
        _ev("نص-الإسراء", EvidenceGenus.ACCEPTED_REPORT, "النص القرآني"),
    )
    hitting = WorldRule(
        "ضرب-أذى",
        "ضرب",
        "أذى",
        Degree.اخص,
        Standing.عادي,
        Admission.مرشح,
        "مولد",
        None,
        ("ضرب لا يؤلم",),
    )
    rules = (uff, harm, hitting)
    assert infer(Literal("أف", True), "محرم في حق الوالدين", rules).outcome is (
        Outcome.منتج
    )
    waiting = infer(Literal("ضرب", True), "محرم في حق الوالدين", rules)
    assert waiting.outcome is Outcome.ناقص
    assert "ضرب-أذى" in waiting.note
    admitted = hitting.admit(
        _ev("مشاهدة-الضرب", EvidenceGenus.DIRECT_OBSERVATION, "مشاهدة معلنة")
    )
    done = infer(Literal("ضرب", True), "محرم في حق الوالدين", (uff, harm, admitted))
    assert done.outcome is Outcome.منتج
    assert [step.rule_id for step in done.path] == ["ضرب-أذى", "أذى-محرم"]
    assert done.defeasible


def test_kinaya_needs_an_equivalence_licence() -> None:
    nijad = WorldRule(
        "قامة-نجاد",
        "طويل القامة",
        "طويل النجاد",
        Degree.اخص,
        Standing.عادي,
        Admission.مقبول,
        "دلائل الإعجاز §58",
        _ev("ردف-في-الوجود", EvidenceGenus.ACCEPTED_REPORT, "0471CabdQahirJurjani"),
        ("نجاد طويل لغير الطويل",),
    )
    bare = infer(Literal("طويل النجاد", True), "طويل القامة", (nijad,))
    assert bare.outcome is Outcome.غير_منتج
    licence = EquivalenceLicence(
        "قامة-نجاد",
        EquivalenceGround.سياق,
        _ev("سياق-المدح", EvidenceGenus.ACCEPTED_REPORT, "سياق الكلام"),
    )
    licensed = infer(Literal("طويل النجاد", True), "طويل القامة", (nijad,), (licence,))
    assert licensed.outcome is Outcome.منتج
    assert licensed.path[0].form is Form.عين_التالي
    assert licensed.path[0].licence is EquivalenceGround.سياق
    assert licensed.defeasible


def test_admission_requires_evidence_of_the_right_genus() -> None:
    with pytest.raises(WorldKnowledgeError):
        WorldRule(
            "x", "أ", "ب", Degree.اخص, Standing.تعريفي, Admission.مقبول, "o", None
        )
    lexical = _ev("معجم", EvidenceGenus.LEXICAL_ATTESTATION, "معجم")
    with pytest.raises(WorldKnowledgeError):
        WorldRule(
            "x",
            "أ",
            "ب",
            Degree.اخص,
            Standing.عادي,
            Admission.مقبول,
            "o",
            lexical,
            ("م",),
        )
    with pytest.raises(WorldKnowledgeError):
        WorldRule("x", "أ", "ب", Degree.اخص, Standing.عادي, Admission.مرشح, "o", None)


def test_only_admitted_rules_become_substance_rules() -> None:
    rule = SUN.as_inference_rule()
    assert isinstance(rule, InferenceRule)
    assert rule.kind is RuleKind.DEFEASIBLE
    assert rule.blocker_ids == ("كسوف",)
    assert HUMAN.as_inference_rule().kind is RuleKind.STRICT_IN_THE_DECLARED_MODEL
    candidate = WorldRule(
        "y", "أ", "ب", Degree.اخص, Standing.وضعي, Admission.مرشح, "مولد", None
    )
    with pytest.raises(WorldKnowledgeError):
        candidate.as_inference_rule()
