"""سحبُ شاهدٍ فوق اشتقاقاتٍ فعليّة: ما الذي يسقط، وما الذي يبقى، وبأيّ دليل.

الطلبُ كان: «اختبِر الإبطالَ المتسلسلَ على اشتقاقاتٍ فعليّةٍ بالآليّات
القائمة، لا بمحرِّكٍ موازٍ». وهذه الوحدةُ **خطُّ بياناتٍ** فوق
`ontology.accumulation`: `KnowledgeStock.admit` و`adopt_rule` و
`apply_adopted_rule` و`retract_evidence` و`revoke_adoption` و`correct` و
`claim_verdict` و`independent_supports` — بلا فرعٍ جديدٍ في المحرِّك ولا
دالّةٍ خاصّةٍ بهذا المجال.

**والأدلّةُ ههنا مقيسةٌ لا مفترَضة.** كلُّ سندٍ في هذا الرصيد تدقيقُ شاهدٍ
مرّت بوّاباتُه الخمسُ في `word_certificate_chain`: مصدرٌ مختومٌ يُصادَم ختمُه
من القرص، وموضعٌ يُحَلّ إلى إزاحة، ومقطعٌ منقولٌ حرفًا بحرف، ومعطياتٌ بنيويّةٌ
تُطابق المقيس، وقاعدةٌ بإصدارها تنطبق على الوقوع.

**وثلاثُ حالاتٍ تُفصَل ولا تُخلَط**
(`THE_SOURCE_THE_DERIVATION_AND_THE_CLAIM_ARE_THREE_STATES`):

- **حالُ المصدر**: أحاضرٌ مختومٌ أم مسحوب؟
- **حالُ الاشتقاق**: أقائمٌ أم معلَّقٌ لسقوط مقدّمةٍ أو نقضِ اعتمادِ قاعدته؟
- **حالُ الدعوى**: أمدعومةٌ بسندٍ حيٍّ أم بلا سند؟

فسحبُ مصدرٍ يُعلِّق ما اشتُقّ منه، ولا يُثبِت كذبَ كلّ ما نُقل عنه؛ ودعوى
يكفيها سندٌ بديلٌ تبقى مدعومةً وإن سقط أحدُ سنديها؛ وشهادةٌ احتجّت بالشاهد
المسحوب لا تبقى صالحةً لأنّ الدعوى بقيت مدعومةً بغيرها.

**والاستقلالُ ههنا استقلالُ اشتقاقٍ لا استقلالُ مادّة**
(`INDEPENDENCE_OF_DERIVATION_IS_NOT_INDEPENDENCE_OF_MATTER`): السندان مقروءان
من ملفَّين مختومَين مختلفَي البايتات، لكنّهما نسختان لمتنٍ واحد؛ فتوافقُهما
ليس شاهدَين مستقلَّين على العالم.

**وما لا تفعله هذه الوحدة**: لا تحكم بصدق دعوًى خارج هذا الرصيد، ولا تُرقّي
نجاحَ سيناريو إلى إثباتِ صحّةِ معرفة، ولا تدّعي سجلًّا غيرَ قابلٍ للتغيير:
المرساةُ المُعلَنةُ هي المُودَعُ في `exhibits/` مُصادَمًا بما يولّده القرصُ في
CI، لا بصمةٌ تحرس نفسَها (`THE_ANCHOR_IS_NAMED_AND_IT_IS_NOT_THE_HASH_ITSELF`).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from ..ontology import (
    AdmissionLicence,
    AdoptionLicence,
    ClaimKey,
    Correction,
    DesignationMethod,
    Evidence,
    EvidenceGenus,
    ExistenceStanding,
    FactRegister,
    IdentityNetwork,
    Individual,
    InferenceRule,
    KnowledgeStock,
    Polarity,
    Proposition,
    PropositionForm,
    ReinstatementPolicy,
    RuleKind,
    RuleOrigin,
    Scope,
)
from ..ontology.accumulation import ClaimStanding, independent_supports
from .excerpt_origin_bridge import WordAddress, locate
from .word_certificate_chain import (
    AnalysisSubject,
    AnalysisWitness,
    FeatureClaim,
    StructuralFeature,
    WitnessAudit,
    measured_features,
    tanwin_reading,
    witness_source_of,
)

__all__ = [
    "INDEPENDENCE_OF_DERIVATION_IS_NOT_INDEPENDENCE_OF_MATTER",
    "THE_ANCHOR_IS_NAMED_AND_IT_IS_NOT_THE_HASH_ITSELF",
    "THE_CLAIM",
    "THE_MIRROR_ADDRESS",
    "THE_SCOPE",
    "THE_WITNESSED_ADDRESS",
    "RescueOutcome",
    "StateReading",
    "audited_witness",
    "base_stock",
    "carrier_rule",
    "mirror_witness",
    "primary_witness",
    "read_state",
    "run",
]


THE_SOURCE_THE_DERIVATION_AND_THE_CLAIM_ARE_THREE_STATES: Final[str] = (
    "حالُ المصدر غيرُ حالِ الاشتقاق غيرُ حالِ الدعوى: سحبُ مصدرٍ يُعلِّق ما "
    "اشتُقّ منه ولا يُثبِت كذبَ ما نُقل عنه، وبقاءُ الدعوى مدعومةً بسندٍ آخرَ "
    "لا يُبقي شهادةً احتجّت بالمسحوب صالحة."
)

INDEPENDENCE_OF_DERIVATION_IS_NOT_INDEPENDENCE_OF_MATTER: Final[str] = (
    "سندان لا يرجع أحدهما إلى دليل الآخر مستقلّا **الاشتقاق**؛ وقد يكونان "
    "نسختين لمتنٍ واحدٍ فلا يكونان مستقلَّي المادّة. والعددُ ٢ ههنا يُقرأ "
    "بهذا القيد أو لا يُقرأ."
)

THE_ANCHOR_IS_NAMED_AND_IT_IS_NOT_THE_HASH_ITSELF: Final[str] = (
    "سلسلةُ البصمات تكشف العبثَ عند المصادمة بمرساةٍ موثوقة؛ والمرساةُ ههنا "
    "مُسمّاةٌ: المُودَعُ في `exhibits/` يُعاد توليدُه في CI ويُصادَم به. ولا "
    "يُدَّعى سجلٌّ غيرُ قابلٍ لإعادة الكتابة بغير آليّةِ تحقّقٍ ومرساةٍ."
)

THE_SCOPE: Final[Scope] = Scope(domain_id="شهادةُ-الكلمة-في-موضعها")

THE_WITNESSED_ADDRESS: Final[WordAddress] = WordAddress("QURAN_SIMPLE", 186, 4)
THE_MIRROR_ADDRESS: Final[WordAddress] = WordAddress("GLOBALQURAN_SIMPLE", 186, 4)

_SURFACE: Final[str] = "\u062d\u064e\u064a\u064e\u0627\u0629\u064c"
_CARRIERS: Final[str] = "\u062d\u064e\u064a\u064e\u0627\u0629"

THE_CLAIM: Final[ClaimKey] = ClaimKey(
    subject_id="وقوع-حياة-في-آية-القصاص",
    predicate_id="الحوامل-بعد-عزل-التنوين",
    value=_CARRIERS,
    polarity=Polarity.AFFIRMED,
    scope=THE_SCOPE,
)


def _occurrence_witness(address: WordAddress, examiner: str) -> AnalysisWitness:
    located = locate(address)
    return AnalysisWitness(
        subject=AnalysisSubject.OCCURRENCE_OF_THE_SURFACE,
        claim=(
            f"وقع السطحُ «{located.surface}» في «{address.rendered}»، وحواملُه "
            f"بعد عزل علامة التنوين «{_CARRIERS}»"
        ),
        surface=located.surface,
        source_key=address.source_key,
        locus=address,
        quoted_excerpt=located.line_text,
        claimed_features=(
            FeatureClaim(StructuralFeature.SURFACE, located.surface),
            FeatureClaim(StructuralFeature.CARRIERS_WITHOUT_TANWIN, _CARRIERS),
        ),
        claim_rests_on=(located.surface,),
        rule_versioned_id="قاعدة-الوقوع-من-مدوّنةٍ-مختومة@1",
        examiner=examiner,
    )


def primary_witness() -> AnalysisWitness:
    """الشاهدُ الأوّل: وقوعُ السطح في نسخة `QURAN_SIMPLE` المختومة."""

    return _occurrence_witness(THE_WITNESSED_ADDRESS, "witness_retraction_run")


def mirror_witness() -> AnalysisWitness:
    """السندُ البديل: الوقوعُ نفسُه في نسخة `GLOBALQURAN_SIMPLE` المختومة."""

    return _occurrence_witness(THE_MIRROR_ADDRESS, "witness_retraction_run")


def audited_witness(witness: AnalysisWitness) -> WitnessAudit:
    """تدقيقُ شاهدٍ عند موضعه هو؛ فالمعطياتُ تُقاس من بايتات ذلك الموضع.

    المدخل: شاهدٌ يُسمّي موضعَه.
    الشرط: الموضعُ يُحَلّ في مصدرٍ مُعلَنٍ مختوم.
    المخرج: تدقيقٌ ببوّاباته الخمس.
    حدُّها: لا تُرقّي شاهدًا، وإنّما تقرأ بوّاباتِه.
    """

    source = witness_source_of(witness.source_key)
    located = locate(witness.locus, source=source.source)
    return witness.audit(measured_features(located, tanwin_reading(located.surface)))


def _evidence(audit: WitnessAudit, evidence_id: str) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=EvidenceGenus.MEASUREMENT,
        statement=(
            f"تدقيقُ شاهدٍ مرّت بوّاباتُه الخمس: {audit.rendered}. "
            f"{THE_SOURCE_THE_DERIVATION_AND_THE_CLAIM_ARE_THREE_STATES}"
        ),
        source_name=witness_source_of(audit.source_key).source.relative_path,
        scope=THE_SCOPE,
    )


def carrier_rule() -> InferenceRule:
    """القاعدةُ المعتمدةُ: من ثبت وقوعُ سطحه ثبتت بطاقةُ حوامله في الشهادة."""

    return InferenceRule(
        rule_id="قاعدة-بطاقة-الحوامل",
        version="1",
        kind=RuleKind.DEFEASIBLE,
        premise_patterns=("وقوعُ سطحٍ مشهودٌ له ببوّاباتٍ خمس",),
        conclusion_pattern="بطاقةُ حواملِ ذلك الوقوع في شهادة الكلمة",
        applicability_note=(
            "تنطبق على وقوعٍ شُهِد له بتدقيقٍ مرّت بوّاباتُه الخمس في النطاق "
            "نفسِه؛ وتُخرِج بطاقةً لا جذرًا ولا إعرابًا"
        ),
        blocker_ids=("ختمُ المصدر مكسور",),
        evidence_ref=Evidence(
            evidence_id="دليل-مصدر-قاعدة-البطاقة",
            genus=EvidenceGenus.STIPULATED_DEFINITION,
            statement=(
                "اصطلاحُ هذا الرصيد: بطاقةُ الحوامل نقلٌ لما قيس في الوقوع، "
                "ولا تُخرِج تحليلًا"
            ),
            source_name="اصطلاحُ هذه الوحدة",
            scope=THE_SCOPE,
        ).ref,
    )


def _proposition(
    proposition_id: str,
    predicate_id: str,
    value: str,
    evidence: Evidence,
    *,
    subject_id: str = THE_CLAIM.subject_id,
    derived_from: tuple[str, ...] = (),
    derived_by_rule: str | None = None,
) -> Proposition:
    return Proposition(
        proposition_id=proposition_id,
        form=PropositionForm.ATTRIBUTE_VALUE,
        subject_id=subject_id,
        predicate_id=predicate_id,
        value=value,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
        evidence_ref=evidence.ref,
        derived_from_proposition_ids=derived_from,
        derived_by_rule=derived_by_rule,
    )


@dataclass(frozen=True, slots=True)
class StateReading:
    """قراءةُ حالٍ واحدة: الدعوى، والاشتقاقات، والأحكامُ المستقلّة."""

    label: str
    claim_standing: ClaimStanding
    live_supports: tuple[str, ...]
    independent_families: int
    suspended_ids: tuple[str, ...]
    stock_version: int
    stock_content_id: str

    @property
    def rendered(self) -> str:
        """سطرٌ يُقرَأ: منزلةُ الدعوى وأسانيدُها الحيّةُ وما عُلِّق."""

        supports = " · ".join(self.live_supports) or "—"
        suspended = " · ".join(self.suspended_ids) or "—"
        return (
            f"{self.label}: الدعوى {self.claim_standing.value} · أسانيدُها "
            f"الحيّة [{supports}] · طوائفُ مستقلّة {self.independent_families} · "
            f"المعلَّق [{suspended}] · الرصيد v{self.stock_version} "
            f"({self.stock_content_id[:12]}…)"
        )


def read_state(stock: KnowledgeStock, label: str) -> StateReading:
    """اقرأ حالَ الرصيد: الدعوى وأسانيدَها وما عُلِّق، بلا تعديلٍ فيه.

    المدخل: رصيدٌ قائم، واسمُ الحال.
    الشرط: لا شرط.
    المخرج: قراءةٌ مُشتقّةٌ من السجلّ لا مكتوبةٌ فيه.
    حدُّها: حكمٌ عن هذا الرصيد بمُعرِّفاته، لا عن العالم.
    """

    verdict = stock.verdict_for(THE_CLAIM)
    families = independent_supports(stock.register, verdict.supporting_proposition_ids)
    return StateReading(
        label=label,
        claim_standing=verdict.standing,
        live_supports=verdict.supporting_proposition_ids,
        independent_families=len(families),
        suspended_ids=tuple(
            one.proposition_id for one in stock.register.propositions if one.suspended
        ),
        stock_version=stock.version,
        stock_content_id=stock.content_id,
    )


def base_stock() -> KnowledgeStock:
    """الحالُ الصحيحةُ قبل أيّ سحب: شاهدان وحكمٌ مشتقٌّ وشهادةٌ تابعةٌ وحكمٌ مستقلّ.

    المدخل: لا شيء؛ كلُّ دليلٍ يُقاس من بايتاتٍ مختومةٍ عند كلّ نداء.
    الشرط: المصدران حاضران سليما الختم، وبوّاباتُ الشاهدَين الخمسُ مارّة.
    المخرج: رصيدٌ فيه: سندٌ أوّل، وحكمٌ مشتقٌّ منه، وشهادةٌ تابعةٌ للحكم،
        وحكمٌ مستقلٌّ لا يعتمد عليه، وسندٌ بديلٌ للدعوى نفسِها.
    حدُّها: لا تُثبِت تحليلًا؛ المشهودُ له وقوعُ سطحٍ وحوامله.
    """

    first = audited_witness(primary_witness())
    second = audited_witness(mirror_witness())
    if not (first.admitted and second.admitted):
        raise ValueError(
            "لا يُبنى رصيدٌ على شاهدٍ لم تمرّ بوّاباتُه: "
            f"{first.what_would_close_it} · {second.what_would_close_it}"
        )
    primary = _evidence(first, "دليل-شاهد-المصحف-المبسّط")
    mirror = _evidence(second, "دليل-شاهد-النسخة-الموازية")
    located = locate(THE_WITNESSED_ADDRESS)
    offset = Evidence(
        evidence_id="دليل-إزاحة-الموضع",
        genus=EvidenceGenus.MEASUREMENT,
        statement=(
            f"إزاحةُ المحارف {located.char_offset} وإزاحةُ البايتات "
            f"{located.byte_offset} في «{THE_WITNESSED_ADDRESS.rendered}»، مقيسةً "
            "من البايتات المختومة"
        ),
        source_name=witness_source_of(
            THE_WITNESSED_ADDRESS.source_key
        ).source.relative_path,
        scope=THE_SCOPE,
    )
    rule = carrier_rule()
    adoption_evidence = Evidence(
        evidence_id="دليل-اعتماد-قاعدة-البطاقة",
        genus=EvidenceGenus.STIPULATED_DEFINITION,
        statement=(
            f"اعتمادُ `{rule.versioned_id}` في هذا الرصيد: تُطبَّق على وقوعٍ "
            "مشهودٍ له ببوّاباتٍ خمسٍ في النطاق نفسِه"
        ),
        source_name="اصطلاحُ هذه الوحدة",
        scope=THE_SCOPE,
    )
    register = FactRegister(register_id="سجلّ-سحب-الشاهد")
    for evidence in (primary, mirror, offset):
        register = register.with_evidence(evidence)
    register = register.with_individual(
        Individual(
            individual_id=THE_CLAIM.subject_id,
            designation_method=DesignationMethod.DEFINITE_DESCRIPTION,
            candidate_type_ids=("موضعٌ-في-نصٍّ-مختوم",),
            existence=ExistenceStanding.ESTABLISHED,
            evidence_ref=offset.ref,
        )
    )
    stock = KnowledgeStock(
        stock_id="رصيد-سحب-الشاهد",
        version=0,
        register=register,
        identity=IdentityNetwork(network_id="شبكة-سحب-الشاهد"),
    )
    support = _proposition("سند-الشاهد-الأوّل", "وقوع-السطح-مشهودٌ-له", _SURFACE, primary)
    stock = stock.admit(
        support,
        AdmissionLicence(
            proposition_id=support.proposition_id,
            scope=THE_SCOPE,
            evidence_ref=primary.ref,
            recorded_order=0,
        ),
    )
    stock = stock.adopt_rule(
        rule,
        AdoptionLicence(
            rule_versioned_id=rule.versioned_id,
            origin=RuleOrigin.TRANSMITTED_FROM_A_SOURCE,
            condition_note=rule.applicability_note,
            evidence_ref=adoption_evidence.ref,
        ),
        adoption_evidence,
    )
    judgement = _proposition(
        "حكم-بطاقة-الحوامل",
        "بطاقة-الحوامل",
        _CARRIERS,
        primary,
        derived_from=(support.proposition_id,),
        derived_by_rule=rule.versioned_id,
    )
    stock, blocked = stock.apply_adopted_rule(
        rule.versioned_id,
        (support.proposition_id,),
        judgement,
        AdmissionLicence(
            proposition_id=judgement.proposition_id,
            scope=THE_SCOPE,
            evidence_ref=primary.ref,
            recorded_order=1,
            depends_on_proposition_ids=(support.proposition_id,),
        ),
    )
    if blocked is not None:  # pragma: no cover - المسارُ مُقاسٌ في الاختبار
        raise ValueError(f"لم تنطلق القاعدةُ في الحال الصحيحة: {blocked}")
    dependent = _proposition(
        "شهادة-تابعة-للحكم",
        "بطاقة-الشهادة-المحتجّة-بالشاهد-الأوّل",
        _CARRIERS,
        primary,
        derived_from=(judgement.proposition_id,),
        derived_by_rule=rule.versioned_id,
    )
    stock, blocked = stock.apply_adopted_rule(
        rule.versioned_id,
        (judgement.proposition_id,),
        dependent,
        AdmissionLicence(
            proposition_id=dependent.proposition_id,
            scope=THE_SCOPE,
            evidence_ref=primary.ref,
            recorded_order=2,
            depends_on_proposition_ids=(judgement.proposition_id,),
        ),
    )
    if blocked is not None:  # pragma: no cover - المسارُ مُقاسٌ في الاختبار
        raise ValueError(f"لم تنطلق القاعدةُ للشهادة التابعة: {blocked}")
    standalone = _proposition(
        "حكم-الإزاحة-المستقلّ",
        "إزاحة-الموضع-بالمحارف",
        str(located.char_offset),
        offset,
    )
    stock = stock.admit(
        standalone,
        AdmissionLicence(
            proposition_id=standalone.proposition_id,
            scope=THE_SCOPE,
            evidence_ref=offset.ref,
            recorded_order=3,
        ),
    )
    alternative = _proposition(
        "سند-بديل-من-النسخة-الموازية",
        THE_CLAIM.predicate_id,
        _CARRIERS,
        mirror,
    )
    stock = stock.admit(
        alternative,
        AdmissionLicence(
            proposition_id=alternative.proposition_id,
            scope=THE_SCOPE,
            evidence_ref=mirror.ref,
            recorded_order=4,
        ),
    )
    carried = _proposition(
        "سند-الدعوى-من-الشاهد-الأوّل",
        THE_CLAIM.predicate_id,
        _CARRIERS,
        primary,
    )
    return stock.admit(
        carried,
        AdmissionLicence(
            proposition_id=carried.proposition_id,
            scope=THE_SCOPE,
            evidence_ref=primary.ref,
            recorded_order=5,
        ),
    )


def _correction_branch(stock: KnowledgeStock) -> tuple[KnowledgeStock, Evidence]:
    """فرعُ التصحيح: إصدارٌ جديدٌ للشاهد وإعادةُ تحقّق، والقديمُ باقٍ بتاريخه."""

    corrected = audited_witness(primary_witness())
    evidence = Evidence(
        evidence_id="دليل-شاهد-المصحف-المبسّط-إصدار-ثانٍ",
        genus=EvidenceGenus.MEASUREMENT,
        statement=(
            "إعادةُ تدقيقِ الشاهد الأوّل بعد تصحيحه، بإصدارٍ ثانٍ مُسجَّلٍ "
            f"بتاريخه: {corrected.rendered}"
        ),
        source_name=witness_source_of(corrected.source_key).source.relative_path,
        scope=THE_SCOPE,
    )
    stock = stock.with_evidence(evidence)
    replacement = _proposition(
        "سند-الدعوى-من-الشاهد-الأوّل-إصدار-ثانٍ",
        THE_CLAIM.predicate_id,
        _CARRIERS,
        evidence,
    )
    return (
        stock.correct(
            Correction(
                correction_id="تصحيح-الشاهد-الأوّل",
                corrected_proposition_id="سند-الدعوى-من-الشاهد-الأوّل",
                replacement_proposition_id=replacement.proposition_id,
                scope=THE_SCOPE,
                recorded_order=9,
                reason=(
                    "أُعيد تدقيقُ الشاهد فأُودِع بإصدارٍ ثانٍ؛ والقديمُ يُعلَّق "
                    "ويبقى في السجلّ بتاريخه ولا يُمحى"
                ),
                evidence_ref=evidence.ref,
                policy=ReinstatementPolicy.KEEP_SUSPENDED_UNTIL_NEW_EVIDENCE,
            ),
            replacement,
            AdmissionLicence(
                proposition_id=replacement.proposition_id,
                scope=THE_SCOPE,
                evidence_ref=evidence.ref,
                recorded_order=10,
            ),
        ),
        evidence,
    )


@dataclass(frozen=True, slots=True)
class RescueOutcome:
    """أثرُ التشغيل: قراءاتُ الأحوال، وسطورٌ تُقرَأ، وحدودٌ مُعلَنة."""

    readings: tuple[StateReading, ...]
    lines: tuple[str, ...]
    limits: tuple[str, ...]


def run() -> RescueOutcome:
    """شغِّل السيناريو كلَّه فوق الآليّات القائمة، وأخرِج أثرَه حالًا حالًا.

    المدخل: لا شيء؛ البايتاتُ تُقرأ من القرص عند كلّ نداء.
    الشرط: المصدران حاضران سليما الختم.
    المخرج: قراءاتُ الأحوال الخمس، وسطورُ الأثر، والحدودُ المُعلَنة.
    حدُّها: نجاحُ سيناريو ليس إثباتًا لصحّة معرفة؛ وكلُّ حكمٍ ههنا حكمٌ عن
        هذا الرصيد بمُعرِّفاته.
    """

    readings: list[StateReading] = []
    lines: list[str] = []

    base = base_stock()
    readings.append(read_state(base, "١ · الحالُ الصحيحة"))
    lines.append(
        "١ · الحالُ الصحيحة: سندٌ أوّلٌ بشاهدٍ مرّت بوّاباتُه الخمس، ومنه حكمٌ "
        "مشتقٌّ وشهادةٌ تابعة؛ وحكمُ الإزاحة مستقلٌّ لا يعتمد عليه؛ وللدعوى "
        "سندٌ بديلٌ من نسخةٍ أخرى مختومة"
    )

    withdrawn = base.retract_evidence("دليل-شاهد-المصحف-المبسّط")
    after = read_state(withdrawn, "٢ · بعد سحب الشاهد الأوّل")
    readings.append(after)
    lines.append(
        "٢ · سحبُ الشاهد الأوّل: عُلِّق سندُه وحكمُه المشتقُّ وشهادتُه التابعة "
        f"({' · '.join(after.suspended_ids)})؛ وبقي حكمُ الإزاحة المستقلُّ "
        "قائمًا، وبقيت الدعوى مدعومةً بالسند البديل وحدَه"
    )

    without_both = withdrawn.retract_evidence("دليل-شاهد-النسخة-الموازية")
    stripped = read_state(without_both, "٣ · بعد سحب السند البديل")
    readings.append(stripped)
    lines.append(
        "٣ · سحبُ السند البديل: صارت الدعوى "
        f"{stripped.claim_standing.value} بلا سندٍ حيّ، ولم يُمَسّ حكمُ الإزاحة "
        "المستقلُّ؛ وغيابُ السند جهلٌ لا نفي"
    )

    revoked = base.revoke_adoption(carrier_rule().versioned_id)
    after_revocation = read_state(revoked, "٤ · بعد نقض اعتماد القاعدة")
    readings.append(after_revocation)
    lines.append(
        "٤ · نقضُ اعتماد القاعدة: عُلِّق ما اشتُقّ بها "
        f"({' · '.join(after_revocation.suspended_ids)})، وبقي المُودَعُ "
        "مباشرةً على حاله؛ فالشهادةُ المبنيّةُ على إصدارٍ سقط اعتمادُه لا "
        "يُعاد اعتمادُها بإعادة بصمِها"
    )

    corrected, _ = _correction_branch(base)
    after_correction = read_state(corrected, "٥ · بعد تصحيح الشاهد")
    readings.append(after_correction)
    history = corrected.corrections_of("سند-الدعوى-من-الشاهد-الأوّل")
    lines.append(
        "٥ · تصحيحُ الشاهد: أُودِع إصدارٌ ثانٍ وأُعيد التحقّق، وعُلِّق القديمُ "
        f"ولم يُمحَ — تاريخُه في السجلّ ({len(history)} قرارَ تصحيحٍ مسجَّلًا)، "
        f"والدعوى {after_correction.claim_standing.value}"
    )

    limits = (
        THE_SOURCE_THE_DERIVATION_AND_THE_CLAIM_ARE_THREE_STATES,
        INDEPENDENCE_OF_DERIVATION_IS_NOT_INDEPENDENCE_OF_MATTER,
        THE_ANCHOR_IS_NAMED_AND_IT_IS_NOT_THE_HASH_ITSELF,
    )
    return RescueOutcome(readings=tuple(readings), lines=tuple(lines), limits=limits)
