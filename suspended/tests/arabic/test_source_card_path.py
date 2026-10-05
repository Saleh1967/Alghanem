"""شواهدُ مسار البطاقة المصدريّة: تُصادِم النصَّ والترخيصَ والشهادة.

والملفُّ مقسومٌ ثلاثةَ أقسامٍ مُعلَنةٍ لا تختلط:

١. **اختباراتٌ مصدريّة** على بايتات الكتابين وإزاحاتهما الفعليّة.
٢. **اختباراتٌ مصطنعةٌ** تفحص الحُرّاس بتحريفٍ نُعلِن أنّه منّا، ولا يُنسَب إلى
   الكتاب ولا إلى مراجعةٍ واقعيّة.
٣. **حالاتُ تقييمٍ** لم تُستعمَل في كتابة شروط التنفيذ: تُعرَّف ههنا وحدَها،
   وتمرّ بالآلة العامّة نفسِها، وتُعلَن نتيجتُها المتوقَّعةُ ومسوّغُها قبل
   التشغيل في نصّ كلّ اختبار.

ولا تُحسَب إعادةُ عبارةٍ منسوخةٍ تطبيقًا جديدًا للقاعدة: الشواهدُ تُقابِل
الشرائحَ بما يُقرَأ من القرص الآن، وتُقابِل الشهاداتِ بمضمون السجلّ.
"""

from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

from alghanem.arabic.source_card_path import (
    THE_CARDS,
    THE_CASES,
    THE_INTERPRETATION_PREMISE_CARD,
    THE_SOURCES,
    ApplicationVerdict,
    CaseFact,
    KnowledgeCard,
    PremiseKind,
    SourceCardError,
    SpeechGenus,
    UsageCase,
    apply_to_case,
    base_stock,
    card_of,
    cards_of_material,
    claim_of_case,
    corrected_card,
    extracted_text,
    extractor_fingerprint,
    read_cards,
    run_experiment,
    seal_of,
    the_rule,
    verify_certificate,
)
from alghanem.ontology.accumulation import AccumulationError
from alghanem.ontology.content import Polarity
from alghanem.ontology.substance import RuleKind

MODULE_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "source_card_path.py"
).read_text(encoding="utf-8")


# ----- ١. اختباراتٌ مصدريّة على البايتات -------------------------------------


@pytest.mark.parametrize("source", THE_SOURCES, ids=lambda item: item.key)
def test_each_declared_seal_is_recomputed_from_the_bytes_on_disk(
    source: object,
) -> None:
    """البصمةُ تُحسَب الآن من البايتات، ولا يُقرَأ رقمٌ منقولٌ بدلَ الحساب."""

    seal = seal_of(source.key)  # type: ignore[attr-defined]
    assert seal.present
    assert seal.measured_byte_length == source.declared_byte_length  # type: ignore[attr-defined]
    assert seal.measured_sha256 == source.declared_sha256  # type: ignore[attr-defined]
    assert seal.matches_declared


def test_every_card_is_resliced_from_its_sealed_material() -> None:
    """كلُّ بطاقةٍ تُعاد من مستخرَج مصدرها نفسِه، لا من ذاكرة النموذج."""

    readings = read_cards()
    assert len(readings) == len(THE_CARDS)
    for reading in readings:
        assert reading.is_reproduced, reading.card.versioned_id
        assert reading.measured_excerpt == reading.card.excerpt


def test_each_excerpt_occurs_once_so_the_offset_names_one_place() -> None:
    """الإزاحةُ تُسمّي موضعًا واحدًا؛ ولو تكرّر المقطعُ لَما سمّته وحدَه."""

    for card in THE_CARDS:
        text = extracted_text(card.material_key)
        assert text.count(card.excerpt) == 1, card.versioned_id
        assert text[card.start : card.end] == card.excerpt


def test_the_context_window_strictly_contains_the_slice() -> None:
    """السياقُ قبلَ المقطع وبعدَه يُقرَأ لئلّا تُقتطَع جملةٌ من قيدها."""

    for card in THE_CARDS:
        assert card.context_start <= card.start
        assert card.context_end >= card.end
        assert (card.context_end - card.context_start) > (card.end - card.start)


def test_both_materials_carry_cards_and_the_offset_units_differ_by_name() -> None:
    """الكتابان كلاهما مُمثَّلان، ووحدةُ الإزاحة مُعلَنةٌ لكلٍّ على حِدَة."""

    assert cards_of_material("SHAKHSIYYA_THREE")
    assert cards_of_material("TAFKIR")
    units = {source.offset_unit for source in THE_SOURCES}
    assert len(units) == len(THE_SOURCES)
    assert not any("صفحة" in unit for unit in units)


def test_the_extractor_fingerprint_is_the_digest_of_the_declared_rulers() -> None:
    """بصمةُ المستخرِج تُحسَب من شفرته؛ فلو تغيّر المسطرةُ تغيّرت البصمة."""

    first = extractor_fingerprint()
    assert first == extractor_fingerprint()
    assert len(first) == len(hashlib.sha256(b"").hexdigest())


def test_the_two_books_are_held_apart_by_material_key() -> None:
    """ج٣ والتفكير مادّتان لا واحدة، ولا تُخلَط إزاحاتُهما."""

    keys = {card.material_key for card in THE_CARDS}
    assert keys == {"SHAKHSIYYA_THREE", "TAFKIR"}


def test_the_genus_of_each_card_is_declared_and_our_formulations_are_marked() -> None:
    """نوعُ القول مُعلَنٌ لكلّ بطاقة، وما صغناه نحن مُسمًّى صياغةً لنا."""

    for card in THE_CARDS:
        assert isinstance(card.genus, SpeechGenus)
    ours = [card for card in THE_CARDS if card.genus is SpeechGenus.OUR_FORMULATION]
    assert not ours, "لا تُدخَل صياغتُنا بطاقةً مصدريّةً تُقرَأ نصًّا للمؤلّف"


# ----- ٢. اختباراتٌ مصطنعةٌ لفحص الحُرّاس ------------------------------------


def test_a_distorted_excerpt_is_refused_and_never_admitted() -> None:
    """تحريفُ الشاهد — وهو تحريفٌ منّا في بيانات الاختبار — يُردّ ولا يُدخَل."""

    card = card_of(THE_INTERPRETATION_PREMISE_CARD)
    forged = replace(card, excerpt="ـ" + card.excerpt[1:])
    reading = read_cards(cards=(forged,))[0]
    assert not reading.is_reproduced
    with pytest.raises(SourceCardError):
        base_stock(cards=(forged,), cases=())


def test_moving_the_reference_to_an_unrelated_offset_breaks_reproduction() -> None:
    """نقلُ الإحالة إلى مقطعٍ غيرِ متعلِّقٍ يُكشَف بالمقابلة لا بالثقة."""

    card = card_of(THE_INTERPRETATION_PREMISE_CARD)
    width = card.end - card.start
    moved = replace(
        card,
        start=card.start + 5_000,
        end=card.start + 5_000 + width,
        context_start=card.context_start + 5_000,
        context_end=card.context_end + 5_000,
    )
    assert not read_cards(cards=(moved,))[0].is_reproduced


def test_swapping_the_speaker_changes_the_evidence_fingerprint_and_voids_the_certificate() -> (  # noqa: E501
    None
):
    """تبديلُ صاحب القول يُغيِّر بصمةَ الدليل، فتُرفَض شهادةٌ أُخرِجت قبله."""

    stock = base_stock()
    case = THE_CASES[0]
    applied, certificate = apply_to_case(stock, case)
    assert certificate.verdict is ApplicationVerdict.FIRED
    assert verify_certificate(applied, certificate).holds

    evidence_id = f"دليل-تفسير-{card_of(THE_INTERPRETATION_PREMISE_CARD).versioned_id}"
    original = applied.register.evidence_of(evidence_id)
    swapped = replace(
        original,
        statement=original.statement.replace(
            card_of(THE_INTERPRETATION_PREMISE_CARD).speaker,
            "قائلٌ آخرُ بدّلناه في بيانات الاختبار",
        ),
    )
    moved = replace(applied, register=applied.register.amend_evidence(swapped))
    reading = verify_certificate(moved, certificate)
    assert not reading.holds
    assert any("بصمةُ مضمون الدليل" in breach for breach in reading.breaches)


def test_dropping_a_condition_suspends_the_verdict_and_names_what_is_missing() -> None:
    """إسقاطُ شرطٍ لا يُقرَأ عدمًا: يُعلَّق الحكمُ ويُسمّى الناقصُ باسمه."""

    case = THE_CASES[0]
    stripped = replace(
        case,
        case_id=case.case_id + "-منقوص",
        facts=tuple(
            fact
            for fact in case.facts
            if fact.kind is not PremiseKind.DIVERTING_INDICATION
        ),
    )
    stock = base_stock(cases=(stripped,))
    _, certificate = apply_to_case(stock, stripped)
    assert certificate.verdict is ApplicationVerdict.SUSPENDED_FOR_A_MISSING_PREMISE
    assert any(
        PremiseKind.DIVERTING_INDICATION.value in name
        for name in certificate.missing_premises
    )


def test_a_revoked_adoption_refuses_the_application_outright() -> None:
    """سحبُ الترخيص يمنع التطبيق؛ ولا تُقبَل نتيجةٌ بترخيصٍ منقوض."""

    stock = base_stock()
    case = THE_CASES[0]
    applied, certificate = apply_to_case(stock, case)
    revoked = applied.revoke_adoption(certificate.rule_versioned_id)
    with pytest.raises(SourceCardError):
        apply_to_case(revoked, case, attempt=9)
    with pytest.raises(AccumulationError):
        revoked.revoke_adoption(certificate.rule_versioned_id)
    reading = verify_certificate(revoked, certificate)
    assert not reading.holds
    assert any("اعتماد" in breach for breach in reading.breaches)


def test_a_sound_seal_over_changed_bytes_is_not_a_corrupt_seal(tmp_path: Path) -> None:
    """فسادُ البصمة غيرُ نسخةٍ جديدةٍ سليمةِ البصمة بدّلت مضمونَها."""

    source = THE_SOURCES[0]
    target = tmp_path / source.relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"\x50\x4b\x03\x04 bytes we wrote ourselves")
    seal = seal_of(source.key, root=tmp_path)
    assert seal.present
    assert seal.measured_sha256 == hashlib.sha256(target.read_bytes()).hexdigest()
    assert not seal.matches_declared
    with pytest.raises(SourceCardError):
        extracted_text(source.key, root=tmp_path)


def test_a_missing_copy_is_a_named_refusal_and_not_a_silent_empty_text(
    tmp_path: Path,
) -> None:
    """غيابُ النسخة رفضٌ مُسمًّى، ولا يُعوَّض بنصٍّ من ذاكرة النموذج."""

    source = THE_SOURCES[1]
    seal = seal_of(source.key, root=tmp_path)
    assert not seal.present
    assert seal.measured_sha256 is None
    with pytest.raises(SourceCardError):
        extracted_text(source.key, root=tmp_path)


def test_the_rule_is_defeasible_and_carries_its_named_blockers() -> None:
    """قاعدةٌ مُرجَّحةٌ بلا موانعَ مُسمّاةٍ لا تُعتمَد؛ والموانعُ مُعلَنةٌ معها."""

    rule = the_rule()
    assert rule.kind is RuleKind.DEFEASIBLE
    assert rule.blocker_ids
    assert "@" not in rule.rule_id


def test_the_adoption_evidence_is_not_a_claim_of_learning_from_the_books() -> None:
    """طريقةُ الحصول مُصرَّحٌ بها: تحريرٌ يدويٌّ موثَّقٌ لا تعلُّمٌ عامٌّ."""

    stock = base_stock(cases=())
    adoption = stock.adoption_of(f"{the_rule().rule_id}@1")
    evidence = stock.register.evidence_of(adoption.evidence_ref.evidence_id)
    assert evidence.genus.is_fact_establishing
    assert "تحريرٌ يدويٌّ موثَّقٌ" in evidence.statement
    assert "تعلُّم" not in evidence.statement


def test_the_connected_experiment_meets_every_declared_expectation() -> None:
    """الحالاتُ السبعُ تُخرِج ما أُعلِن قبل تشغيلها، لا ما يُفسَّر بعدَه."""

    trace = run_experiment()
    keys = {step.key for step in trace.steps}
    assert keys == {"أ", "أ-٢", "ب", "ج", "د", "هـ", "و", "ز"}
    assert "صمد" in " ".join(trace.step("أ").observations)
    assert any("الناقص" in line for line in trace.step("ب").observations)
    assert any("خُرِق" in line for line in trace.step("ج").observations)
    assert any("مدعومة" in line for line in trace.step("د").observations)
    assert any("@2" in line for line in trace.step("هـ").observations)
    before, after = (
        line for line in trace.step("و").observations if "بصمةُ الرصيد" in line
    )
    assert before != after
    assert "صمد" in " ".join(trace.step("و").observations)
    assert any("خُرِق" in line for line in trace.step("ز").observations)


def test_an_unrelated_amendment_moves_the_fingerprint_and_no_case_verdict() -> None:
    """تغيُّرُ بصمة السجلّ ليس تغيُّرًا في الأحكام؛ تُقارَن النتائجُ أنفسُها."""

    trace = run_experiment()
    step = trace.step("و")
    verdicts = [
        line for line in step.observations if ":" in line and "بصمة" not in line
    ]
    assert any("أسد-في-الغابة" in line and "مدعوم" in line for line in verdicts)


def test_the_correction_keeps_the_old_version_and_never_touches_the_slice() -> None:
    """التصحيحُ يُنشئ إصدارًا ويحفظ القديم، والنصُّ شريحةٌ لا تُمَسّ."""

    card = card_of(THE_INTERPRETATION_PREMISE_CARD)
    later = corrected_card(card, "تفسيرٌ مصحَّحٌ أُعلِن أنّه منّا")
    assert later.version == card.version + 1
    assert later.excerpt == card.excerpt
    assert (later.start, later.end) == (card.start, card.end)
    assert later.versioned_id != card.versioned_id


# ----- ٣. حالاتُ تقييمٍ لم تُستعمَل في كتابة الشروط --------------------------


def _evaluation_case(
    case_id: str,
    phrase: str,
    word: str,
    facts: tuple[tuple[PremiseKind, str, bool], ...],
) -> UsageCase:
    return UsageCase(
        case_id=case_id,
        phrase=phrase,
        word=word,
        facts=tuple(
            CaseFact(
                kind=kind,
                polarity=Polarity.AFFIRMED if affirmed else Polarity.NEGATED,
                value=value,
                evidence_statement=(
                    f"واقعةٌ أودعناها عن «{phrase}» في شواهد التقييم وحدَها، "
                    "بدليلٍ مُعلَنٍ أنّه منّا لا منقولٍ عن الكتاب"
                ),
            )
            for kind, value, affirmed in facts
        ),
        provenance="حالةُ تقييمٍ عُرِّفت في ملفّ الشواهد وحدَه",
    )


EVALUATION_CASES: tuple[UsageCase, ...] = (
    _evaluation_case(
        "تقييم-يد-الطفل",
        "غسل الطفل يده",
        "يد",
        (
            (PremiseKind.FIRST_COINAGE, "الجارحةُ المعروفة", True),
            (PremiseKind.USAGE_IS_AMBULANT, "بين الجارحة والنعمة والقدرة", True),
            (PremiseKind.ADMITS_MAJAZ_BY_ITSELF, "اسمُ جنس", True),
            (PremiseKind.DIVERTING_INDICATION, "لا قرينةَ صارفةً في الجملة", False),
        ),
    ),
    _evaluation_case(
        "تقييم-يد-الدولة",
        "يد الدولة طويلة",
        "يد",
        (
            (PremiseKind.FIRST_COINAGE, "الجارحةُ المعروفة", True),
            (PremiseKind.USAGE_IS_AMBULANT, "بين الجارحة والسلطان", True),
            (PremiseKind.ADMITS_MAJAZ_BY_ITSELF, "اسمُ جنس", True),
            (
                PremiseKind.DIVERTING_INDICATION,
                "إسنادُ الطول إلى يد الدولة قرينةٌ صارفة",
                True,
            ),
        ),
    ),
    _evaluation_case(
        "تقييم-نور-مبهم",
        "رأيت النور",
        "النور",
        (
            (PremiseKind.FIRST_COINAGE, "الضياءُ المحسوس", True),
            (PremiseKind.ADMITS_MAJAZ_BY_ITSELF, "اسمُ جنس", True),
        ),
    ),
)


@pytest.mark.parametrize(
    ("case", "expected"),
    (
        (EVALUATION_CASES[0], ApplicationVerdict.FIRED),
        (EVALUATION_CASES[1], ApplicationVerdict.BLOCKED_BY_A_NAMED_BLOCKER),
        (
            EVALUATION_CASES[2],
            ApplicationVerdict.SUSPENDED_FOR_A_MISSING_PREMISE,
        ),
    ),
    ids=lambda item: getattr(item, "case_id", getattr(item, "name", "")),
)
def test_evaluation_cases_run_through_the_same_generic_machinery(
    case: UsageCase, expected: ApplicationVerdict
) -> None:
    """النتائجُ المتوقَّعةُ ومسوّغاتُها مُعلَنةٌ قبل التشغيل:

    - «غسل الطفل يده»: الوضعُ الأوّلُ قائمٌ والدورانُ قائمٌ ولا قرينةَ صارفةً
      **بدليلٍ مُودَع**، فيُرجَّح الحملُ على الحقيقة.
    - «يد الدولة طويلة»: القرينةُ الصارفةُ مُثبَتةٌ بدليل، فيُمنَع الترجيحُ
      بمانعٍ مُسمًّى، ولا يُحكَم بالمجاز إلّا بشرط العلاقة.
    - «رأيت النور»: الدورانُ والقرينةُ لم يُودَعا، فيُعلَّق الحكمُ ويُسمّى
      الناقصُ، إذ ليس غيابُ الإيداع نفيًا.
    """

    stock = base_stock(cases=(case,))
    _, certificate = apply_to_case(stock, case)
    assert certificate.verdict is expected
    assert certificate.case_id == case.case_id


def test_no_implementation_condition_recognises_an_evaluation_case_by_name() -> None:
    """لا شرطَ في التنفيذ يتعرّف على جملة اختبارٍ باسمها."""

    for case in EVALUATION_CASES:
        assert case.case_id not in MODULE_SOURCE
        assert case.phrase not in MODULE_SOURCE
        assert case.word not in MODULE_SOURCE or case.word in {"يد"}


def test_an_evaluation_verdict_is_verifiable_from_its_own_certificate() -> None:
    """يصل المراجعُ من الحكم إلى مقدّماته وأدلّتها وترخيصه، ويُعاد فحصُها."""

    case = EVALUATION_CASES[0]
    stock = base_stock(cases=(case,))
    applied, certificate = apply_to_case(stock, case)
    reading = verify_certificate(applied, certificate)
    assert reading.holds
    assert reading.machine_checked
    assert reading.left_to_human_review
    assert certificate.conclusion_proposition_id is not None
    for proposition_id, evidence_id, _ in certificate.premise_rows:
        assert applied.register.proposition_of(proposition_id)
        assert applied.register.evidence_of(evidence_id)
    assert applied.verdict_for(claim_of_case(case)).standing.value


def test_a_malformed_card_is_refused_before_it_becomes_a_card() -> None:
    """الحارسُ يَردّ الصياغةَ الفاسدةَ قبل أن تصير بطاقةً تُقرَأ."""

    card = card_of(THE_INTERPRETATION_PREMISE_CARD)
    with pytest.raises(SourceCardError):
        replace(card, version=0)
    with pytest.raises(SourceCardError):
        replace(card, end=card.start)
    assert isinstance(card, KnowledgeCard)
