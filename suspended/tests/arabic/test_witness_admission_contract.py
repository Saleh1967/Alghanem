"""عقدُ قبول الشاهد: خمسُ بوّاباتٍ مفصولة، ومراجعةٌ تُحفَظ ولا تُرخِّص.

وهذه الشواهدُ اختباراتُ انحدار: كانت تسقط قبل التعديل، إذ كان القبولُ
مطابقةَ سطحٍ وحضورَ ملفّ، وكانت البصمةُ لا تتحرّك بتحريف الشاهد.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.epistemic_layers import EpistemicStanding
from alghanem.arabic.excerpt_origin_bridge import WordAddress, locate
from alghanem.arabic.word_certificate_chain import (
    THE_ANALYSIS_RULES,
    AnalysisSubject,
    AnalysisWitness,
    FeatureClaim,
    ReviewAttestation,
    StructuralFeature,
    WitnessGate,
    WordCertificateError,
    certify,
    fingerprint,
    measured_features,
    rule_of,
    tanwin_reading,
    witness_source_of,
)

THE_SURFACE = "\u062d\u064e\u064a\u064e\u0627\u0629\u064c"
THE_ADDRESS = WordAddress("QURAN_SIMPLE", 186, 4)
THE_MAQAYIS_LOCUS = WordAddress("MAQAYIS_BY_ROOT", 9041, 1)
THE_MAQAYIS_EXCERPT = (
    'حيي,مضاعف,874,حي,,,,"الحاء والياء والحرف المعتل أصلان: أحدهما خِلاف '
    "المَوْت، والآخر الاستحياء"
)


def _measured() -> dict[StructuralFeature, str]:
    located = locate(THE_ADDRESS)
    return measured_features(located, tanwin_reading(located.surface))


def _sound_root_witness(**overrides: object) -> AnalysisWitness:
    fields: dict[str, object] = {
        "subject": AnalysisSubject.ROOT_AND_WAZN,
        "claim": "مادّةُ «حيي» في مقاييس اللغة، بنصّ بابها",
        "surface": THE_SURFACE,
        "source_key": "MAQAYIS_BY_ROOT",
        "locus": THE_MAQAYIS_LOCUS,
        "quoted_excerpt": THE_MAQAYIS_EXCERPT,
        "claimed_features": (FeatureClaim(StructuralFeature.SURFACE, THE_SURFACE),),
        "claim_rests_on": ("الحاء والياء والحرف المعتل أصلان",),
        "rule_versioned_id": "قاعدة-المادّة-من-معجمٍ-مختوم@1",
        "examiner": "tests",
    }
    fields.update(overrides)
    return AnalysisWitness(**fields)  # type: ignore[arg-type]


def _fabricated_witness() -> AnalysisWitness:
    """الشاهدُ المختلَقُ نفسُه: دعوى غيرُ مسندة، ومصدرٌ وموضعٌ لا يُسنِدانها."""

    return AnalysisWitness(
        subject=AnalysisSubject.ROOT_AND_WAZN,
        claim="دعوى غيرُ مسندة: «حَيَاةٌ» فعلٌ ماضٍ مبنيٌّ على السكون",
        surface=THE_SURFACE,
        source_key="README.md",
        locus=WordAddress("README.md", 9999, 9999),
        quoted_excerpt="إحالةٌ لا وجودَ لها",
        claimed_features=(FeatureClaim(StructuralFeature.TANWIN_MARK, "لا تنوين"),),
        claim_rests_on=("فعلٌ ماضٍ",),
        rule_versioned_id="قاعدة-المادّة-من-معجمٍ-مختوم@1",
        examiner="مُختلِق",
    )


# ١ — الشاهدُ المختلَقُ يُرَدّ، وسطحُه مطابقٌ وملفُّه حاضر


def test_the_fabricated_witness_is_refused_though_its_surface_matches() -> None:
    """مطابقةُ السطح وحضورُ ملفٍّ في الشجرة ليسا قبولًا لشاهد."""

    audit = _fabricated_witness().audit(_measured())
    assert audit.admitted is False
    assert WitnessGate.SOURCE_PRESENT_AND_SEALED in audit.failed_gates
    assert len(audit.failed_gates) >= 4


def test_the_fabricated_witness_does_not_license_the_morphology_layer() -> None:
    """ولا يُرخِّص هذا الشاهدُ المقدّمةَ الصرفيّة؛ تبقى معلَّقةً باسمها."""

    certificate = certify(THE_ADDRESS, analysis_witnesses=(_fabricated_witness(),))
    root = next(
        one for one in certificate.premises if one.name.startswith("مادّةُ المدخل")
    )
    assert root.is_settled is False
    assert root.name in certificate.overall.blocking_premises


# ٢ — البوّاباتُ الخمسُ تُقاس كلٌّ على حدة


def test_each_gate_falls_on_its_own_without_folding_into_another() -> None:
    """لكلِّ بوّابةٍ سببُها: مصدرٌ، فموضعٌ، فنسبةٌ، فإسنادٌ، فانطباقُ قاعدة."""

    measured = _measured()
    assert _sound_root_witness().audit(measured).admitted is True

    cases = (
        (
            WitnessGate.SOURCE_PRESENT_AND_SEALED,
            {
                "source_key": "README.md",
                "locus": WordAddress("README.md", 1, 1),
            },
        ),
        (
            WitnessGate.EXCERPT_EXTRACTED_AT_LOCUS,
            {"locus": WordAddress("MAQAYIS_BY_ROOT", 10**7, 1)},
        ),
        (
            WitnessGate.EXCERPT_ATTRIBUTED_TO_SOURCE,
            {
                "quoted_excerpt": "مقطعٌ لم يُنقَل من هذا السطر",
                "claim_rests_on": ("مقطعٌ لم يُنقَل من هذا السطر",),
            },
        ),
        (
            WitnessGate.EXCERPT_SUPPORTS_THE_CLAIM,
            {"claim_rests_on": ("جملةٌ ليست في المقطع المنقول",)},
        ),
        (
            WitnessGate.RULE_APPLIES_TO_THIS_OCCURRENCE,
            {"rule_versioned_id": "قاعدة-الوقوع-من-مدوّنةٍ-مختومة@1"},
        ),
    )
    for gate, overrides in cases:
        audit = _sound_root_witness(**overrides).audit(measured)
        assert audit.admitted is False
        assert gate in audit.failed_gates


def test_a_corpus_never_establishes_a_root_because_its_genus_differs() -> None:
    """جنسُ المصدر شرطُ انطباقِ القاعدة: مدوّنةٌ تُثبت وقوعًا لا مادّة."""

    audit = _sound_root_witness(
        source_key="QURAN_SIMPLE",
        locus=THE_ADDRESS,
        quoted_excerpt="فِي الْقِصَاصِ حَيَاةٌ يَا أُولِي الْأَلْبَابِ",
        claim_rests_on=(THE_SURFACE,),
    ).audit(_measured())
    assert WitnessGate.RULE_APPLIES_TO_THIS_OCCURRENCE in audit.failed_gates


def test_a_claimed_feature_that_contradicts_the_bytes_is_not_admitted() -> None:
    """الدعوى تُصادَم بمعطًى بنيويٍّ مقيس، لا تُصدَّق لذاتها."""

    audit = _sound_root_witness(
        claimed_features=(FeatureClaim(StructuralFeature.TANWIN_MARK, "لا تنوين"),)
    ).audit(_measured())
    assert WitnessGate.EXCERPT_SUPPORTS_THE_CLAIM in audit.failed_gates


# ٣ — المراجعةُ محفوظةٌ ولا تفتح بوّابةً ساقطة


def test_a_recorded_review_never_opens_a_gate_that_fell() -> None:
    """تُحفَظ هويّةُ المراجع ونطاقُه ورتبتُه، ولا يُحوَّل ذلك إلى برهان."""

    review = ReviewAttestation(
        reviewer_id="مراجعٌ مُسمًّى",
        scope="هذا الوقوعُ وحدَه",
        rank=EpistemicStanding.PRESUMPTIVE_ALWAYS,
        statement="راجعتُ ووافقت",
    )
    audit = _fabricated_witness_with_review(review).audit(_measured())
    assert audit.review is not None
    assert audit.review.reviewer_id == "مراجعٌ مُسمًّى"
    assert audit.admitted is False


def _fabricated_witness_with_review(review: ReviewAttestation) -> AnalysisWitness:
    base = _fabricated_witness()
    return AnalysisWitness(
        subject=base.subject,
        claim=base.claim,
        surface=base.surface,
        source_key=base.source_key,
        locus=base.locus,
        quoted_excerpt=base.quoted_excerpt,
        claimed_features=base.claimed_features,
        claim_rests_on=base.claim_rests_on,
        rule_versioned_id=base.rule_versioned_id,
        examiner=base.examiner,
        review=review,
    )


# ٤ — القاعدةُ بإصدارها، ولا قاعدةَ بلا إصدار


def test_a_rule_without_its_version_is_not_resolvable() -> None:
    """اسمُ قاعدةٍ بلا `@إصدار` لا يُحَلّ، فلا يُقال انطبقت."""

    assert rule_of("قاعدة-المادّة-من-معجمٍ-مختوم", THE_ANALYSIS_RULES) is None
    assert rule_of("قاعدة-المادّة-من-معجمٍ-مختوم@1", THE_ANALYSIS_RULES) is not None


def test_a_rule_absent_from_the_deposited_book_blocks_readmission() -> None:
    """إصدارٌ غيرُ معتمَدٍ في كتاب القواعد لا تُعاد به شهادةٌ قديمة."""

    audit = _sound_root_witness(rule_versioned_id="قاعدة-المادّة-من-معجمٍ-مختوم@2").audit(
        _measured()
    )
    assert WitnessGate.RULE_APPLIES_TO_THIS_OCCURRENCE in audit.failed_gates


def test_an_undeclared_source_key_is_named_and_not_guessed() -> None:
    """مفاتيحُ المصادر مُعلَنةٌ، ومن خرج عنها رُدَّ باسمه لا بإجمال."""

    with pytest.raises(WordCertificateError):
        witness_source_of("README.md")
    assert witness_source_of("MAQAYIS_BY_ROOT").genus.value


# ٥ — البصمةُ تربط القرارَ بشواهده وإصدارات قواعده


def test_the_fingerprint_moves_when_the_witness_is_tampered_with() -> None:
    """البايتاتُ واحدةٌ والسطحُ واحد، فإن تحرّك الشاهدُ تحرّكت البصمة."""

    sound = certify(THE_ADDRESS, analysis_witnesses=(_sound_root_witness(),))
    tampered = certify(THE_ADDRESS, analysis_witnesses=(_fabricated_witness(),))
    assert sound.located.surface == tampered.located.surface
    assert fingerprint(sound) != fingerprint(tampered)


def test_the_fingerprint_moves_when_only_the_rule_version_moves() -> None:
    """تغييرُ إصدارِ القاعدة وحدَه يُحرّك البصمة، فلا تُعاد شهادةٌ بإصدارٍ آخر."""

    first = certify(THE_ADDRESS, analysis_witnesses=(_sound_root_witness(),))
    second = certify(
        THE_ADDRESS,
        analysis_witnesses=(
            _sound_root_witness(rule_versioned_id="قاعدة-المادّة-من-معجمٍ-مختوم@2"),
        ),
    )
    assert fingerprint(first) != fingerprint(second)


def test_the_fingerprint_is_stable_when_nothing_moved() -> None:
    """ولا تتحرّك البصمةُ بغير سبب: تُشتَقّ من القرص عند كلّ نداء."""

    first = certify(THE_ADDRESS, analysis_witnesses=(_sound_root_witness(),))
    second = certify(THE_ADDRESS, analysis_witnesses=(_sound_root_witness(),))
    assert fingerprint(first) == fingerprint(second)


# ٦ — القبولُ في حدود مصدره، ولا يُكتَب في المنتج ما يُراد إثباتُه


def test_an_admitted_witness_establishes_the_rule_limit_not_its_own_claim() -> None:
    """ما يُثبَت هو ما تُثبته القاعدةُ من مصدرها، لا نصُّ دعوى الشاهد."""

    certificate = certify(THE_ADDRESS, analysis_witnesses=(_sound_root_witness(),))
    root = next(
        one for one in certificate.premises if one.name.startswith("مادّةُ المدخل")
    )
    assert root.is_settled is True
    assert "فعلٌ ماضٍ" not in root.what_it_establishes
    assert "بقاعدة" in root.what_it_establishes or "حدُّ" in root.what_it_establishes


def test_the_wazn_premise_stays_suspended_with_a_named_requirement() -> None:
    """ما لا سندَ له يبقى معلَّقًا باسمه، ويُذكَر ما يُغلقه."""

    certificate = certify(THE_ADDRESS, analysis_witnesses=(_sound_root_witness(),))
    wazn = next(one for one in certificate.premises if one.name.startswith("الوزنُ"))
    assert wazn.is_settled is False
    assert wazn.what_it_establishes.strip()
