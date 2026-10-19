"""شريحةٌ تنفيذيّةٌ واحدة: حجرٌ ← شجرٌ ← بشر، ثمّ شخصٌ ومدينةٌ بالعمليّات نفسها.

الطلبُ كان: «أنجِز شريحةً كاملةً فوق المحرِّك القائم، ثمّ أعد استعمال
العمليّات نفسِها في مجالٍ آخر؛ وأضِف حالةً مصدريّةً حقيقيّةً من كتابٍ متاحٍ
تُثبِت نسبةَ قولٍ إلى مصدره، ولا تُحوِّلها إلى شهادةٍ على واقعةٍ خارجيّة».
وهذه الوحدةُ **بياناتُ مجالٍ وأدلّةٌ**، لا محرِّكٌ ثانٍ::

    AttributedSaying != AttestedFact
    SimulatedEvidence != Observation
    TwoTypes          != TwoConflictingTypes

**الحجرُ والشجرُ والبشرُ مجالُ محاكاةٍ مُعلَن.** لا دليلَ فيه من جنس
`DIRECT_OBSERVATION` البتّة؛ كلُّ ما يَرِد فرضيّاتٌ مُعلَنةٌ وتقاريرُ مقبولة،
فلا يُقرأ من مخرجاته حكمٌ على العالم (`A_SIMULATED_EVIDENCE_STAYS_SIMULATED`).

**والشخصُ والمدينةُ يمرّان بالعمليّات نفسِها**: `admit` و`adopt_rule` و
`apply_adopted_rule` و`correct` و`revoke_adoption` و`type_reading` — بلا فرعٍ
في المحرِّك ولا دالّةٍ خاصّةٍ بمجال. وهذا هو اختبارُ العموم: لا عددُ الأصناف
(`A_SECOND_DOMAIN_IS_A_DATA_LINE_NOT_AN_ENGINE_BRANCH`).

**والحالةُ المصدريّةُ الحقيقيّةُ واحدةٌ محدودةُ الدعوى.** «التفكير» حاضرٌ في
هذه الشجرة مختومًا، فتُقتطَع منه أربعةُ مواضعَ بإزاحاتٍ دقيقة، وتُودَع قضايا
**نسبةِ قولٍ إلى مصدره**: «وقع في الموضع كذا من هذا الملفّ هذا النصّ». وهذا
كلُّ ما تُثبِته: لا أنّ مضمونَ القول صحيح، ولا أنّ المؤلّف يقرّره في كلّ
سياق، ولا أنّه قاعدةٌ معتمدةٌ في هذا الرصيد
(`A_SAYING_IN_A_SOURCE_IS_NOT_AN_ADOPTED_RULE`).

**والاستخراجُ خشنٌ مُعلَنُ الخشونة**، على منوال `dal_alone_bridge`: يُفكّ
المستندُ المركَّبُ بـ`utf-16-le` فيضيع منه ما يضيع. فالإزاحاتُ إزاحاتٌ في
**المستخرَج** لا في صفحات الكتاب، ولا يُقال «صفحةُ كذا»
(`AN_OFFSET_IN_AN_EXTRACTION_IS_NOT_A_PAGE`).

**وما لا تفعله هذه الوحدة**: لا تقرأ عربيّةً من «التفكير» ولا تُحلِّلها، ولا
تستدعي مسارَ ١١٦، ولا تمنح شهادةَ قبولٍ لغويّة. والبطاقاتُ أربعٌ لا تستوفي
فروقَ الطلب كلَّها؛ وما لم يُقتطَع من «الشخصية الإسلامية» معلَّقٌ باسمه لأنّ
بايتاتِه غائبةٌ عن هذه الشجرة.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
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
    IdentityCriterion,
    IdentityLink,
    IdentityNetwork,
    IncompatibilityWitness,
    Individual,
    InferenceRule,
    KeyReading,
    KnowledgeStock,
    NamedKind,
    Naming,
    NamingGenus,
    Polarity,
    Proposition,
    PropositionForm,
    ReinstatementPolicy,
    RuleKind,
    RuleOrigin,
    Scope,
)
from ..ontology.facts import FactError

__all__ = [
    "AN_OFFSET_IN_AN_EXTRACTION_IS_NOT_A_PAGE",
    "A_SAYING_IN_A_SOURCE_IS_NOT_AN_ADOPTED_RULE",
    "A_SECOND_DOMAIN_IS_A_DATA_LINE_NOT_AN_ENGINE_BRANCH",
    "A_SIMULATED_EVIDENCE_STAYS_SIMULATED",
    "THE_BOOK_SEAL",
    "THE_SCANNED_BOOK",
    "THE_SOURCE_CARDS",
    "SourceCard",
    "SliceOutcome",
    "SourceReading",
    "base_stock",
    "living_rule",
    "read_source_cards",
    "run_slice",
    "source_propositions",
    "the_book_path",
    "the_extraction",
]


A_SAYING_IN_A_SOURCE_IS_NOT_AN_ADOPTED_RULE: Final[str] = (
    "وقوعُ قولٍ في مصدرٍ محفوظٍ يُثبِت نسبتَه إلى موضعه، ولا يُثبِت صدقَ "
    "مضمونه، ولا يجعله قاعدةً معتمدةً في هذا الرصيد. والاعتمادُ ترخيصٌ آخرُ "
    "له شروطُه."
)

AN_OFFSET_IN_AN_EXTRACTION_IS_NOT_A_PAGE: Final[str] = (
    "الإزاحةُ موضعٌ في النصّ المستخرَج بفكٍّ خشنٍ مُعلَن، لا صفحةٌ في الكتاب "
    "ولا فقرةٌ من ترقيم ناشر."
)

A_SIMULATED_EVIDENCE_STAYS_SIMULATED: Final[str] = (
    "دليلٌ كتبَته هذه الوحدةُ يبقى محاكاةً في كلّ مخرج؛ ولا يُرقّى مشاهدةً "
    "بتغيير جنسه، ولا يُقرأ منه حكمٌ على واقعةٍ خارج هذه الشجرة."
)

A_SECOND_DOMAIN_IS_A_DATA_LINE_NOT_AN_ENGINE_BRANCH: Final[str] = (
    "المجالُ الثاني يمرّ بالعمليّات نفسِها بلا فرعٍ في المحرِّك؛ ومن احتاج "
    "دالّةً خاصّةً بمجالٍ لم يبنِ نواةً عامّة."
)

THE_SCANNED_BOOK: Final[str] = "التفكير(71)(3).doc"

THE_BOOK_SEAL: Final[str] = (
    "e917d9a03b1a546d783868d3bc018b24ced19eb85df671bd41e05f50c2de492c"
)


def the_book_path() -> Path:
    """موضعُ الكتاب في الشجرة؛ يُشتَقّ من موضع هذه الوحدة لا يُكتَب مطلقًا."""

    return Path(__file__).resolve().parents[3] / THE_SCANNED_BOOK


def the_extraction() -> str:
    """النصُّ المستخرَجُ بالفكّ الخشن المُعلَن؛ لا يُخزَّن ولا يُودَع نسخةً."""

    path = the_book_path()
    if not path.is_file():
        raise FileNotFoundError(
            f"الكتابُ المُعلَن اقتطاعُه غائبٌ عن موضعه: `{THE_SCANNED_BOOK}`"
        )
    return path.read_bytes().decode("utf-16-le", errors="ignore")


@dataclass(frozen=True, slots=True)
class SourceCard:
    """بطاقةُ أصلٍ: الموضعُ والمقتطَف، والمعنى المستخلَص، والمقابلُ وحدُّه."""

    card_id: str
    start: int
    end: int
    excerpt: str
    standing_note: str
    extracted_meaning: str
    engineering_counterpart: str
    counterpart_limit: str

    def __post_init__(self) -> None:
        if self.start < 0 or self.end <= self.start:
            raise ValueError("حدّا المقتطَف مرتّبان وغيرُ سالبين")
        if len(self.excerpt) != self.end - self.start:
            raise ValueError("طولُ المقتطَف طولُ مجاله؛ ونصفُ اقتطاعٍ ليس موضعًا")


THE_SOURCE_CARDS: Final[tuple[SourceCard, ...]] = (
    SourceCard(
        card_id="بطاقة-الواقع-أساس-الفكر",
        start=6401,
        end=6475,
        excerpt=(
            "فالواقع هو أساس الفكر، والفكر إنما هو تعبير عن واقع، "
            "أو حكم على ذلك الواقع"
        ),
        standing_note="تقريرُ المؤلِّف في سياق تعريف الفكر، لا قولٌ يعرضه عن غيره",
        extracted_meaning=(
            "الموجودُ الخارجيُّ غيرُ الحكم عليه؛ والحكمُ تعبيرٌ عن واقعٍ لا " "الواقعُ نفسُه"
        ),
        engineering_counterpart=(
            "فصلُ `Individual` عن `Proposition`: إنشاءُ سجلِّ فردٍ لا يُثبِت "
            "حكمًا عليه، والحكمُ يحمل دليلَه"
        ),
        counterpart_limit=(
            "الفصلُ البرمجيُّ قرارٌ هندسيٌّ ههنا؛ ولا يُنسَب إلى المؤلِّف "
            "`dataclass` ولا حقلُ `evidence_ref`"
        ),
    ),
    SourceCard(
        card_id="بطاقة-الحس-وحده",
        start=14280,
        end=14305,
        excerpt="الحس وحده لا يحصل منه فكر",
        standing_note="تقريرُ المؤلِّف في بيان شرط المعلومات السابقة",
        extracted_meaning=(
            "الإحساسُ بالواقع وحدَه لا يُنتِج حكمًا؛ فلا بدّ من رصيدٍ سابقٍ " "يُفسَّر به المحسوس"
        ),
        engineering_counterpart=(
            "الوقوعُ المتحقَّقُ من مصدرٍ مختومٍ لا يُنتِج قضيّةً وحدَه: يلزم "
            "رصيدُ `K_t` وترخيصُ إدخالٍ"
        ),
        counterpart_limit=(
            "«المعلوماتُ السابقة» عند المؤلِّف أوسعُ من رصيدِ مُعرِّفاتٍ في "
            "سجلّ؛ والمقابلةُ قياسُ بنيةٍ لا ترجمةُ مصطلح"
        ),
    ),
    SourceCard(
        card_id="بطاقة-الحكم-على-الأشياء",
        start=20831,
        end=20897,
        excerpt=(
            "الحكم على الأشياء ما هي، لا يتم إلا بعملية ربط " "وربط بمعلومات سابقة"
        ),
        standing_note="تقريرُ المؤلِّف في تمييز العمليّة العقليّة من الاسترجاع",
        extracted_meaning=(
            "تصنيفُ الشيء تحت نوعه عمليّةُ ربطٍ برصيد، لا استرجاعُ اسمٍ " "محفوظ"
        ),
        engineering_counterpart=(
            "`apply_adopted_rule` يفحص انطباقَ القاعدة عند كلّ استعمال، فلا "
            "يكفي حضورُ القاعدة في الرصيد"
        ),
        counterpart_limit=(
            "«عمليّةُ الربط» عند المؤلِّف وصفٌ لفعلِ العقل؛ وما ههنا تطبيقُ "
            "قاعدةٍ مكتوبةٍ بيد، ولا يُدَّعى أنّه هي"
        ),
    ),
    SourceCard(
        card_id="بطاقة-الرأي-السابق",
        start=26973,
        end=27027,
        excerpt="لا بد أن يلاحظ التفريق بين الرأي السابق وبين المعلومات",
        standing_note=(
            "تقريرُ المؤلِّف في شروط البحث، وفي سياقه عرضُ قول غيره عن "
            "«الطريقة العلميّة» قبلَه"
        ),
        extracted_meaning=(
            "المعلوماتُ السابقةُ تُستعمَل في العمليّة، والرأيُ السابقُ "
            "يُمنَع من التدخُّل فيها؛ فهما لا يستويان شرطًا"
        ),
        engineering_counterpart=(
            "ترخيصانِ متمايزان: `AdmissionLicence` لإدخال الحكم، و"
            "`AdoptionLicence` لاعتماد القاعدة؛ ودليلُ واقعةٍ لا يصلح اعتمادًا"
        ),
        counterpart_limit=(
            "التمييزُ ههنا بين دليلِ واقعةٍ وشاهدِ اعتماد، وليس بين "
            "«المعلومات» و«الرأي» بحدودهما عند المؤلِّف"
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class SourceReading:
    """قراءةُ بطاقةٍ على القرص: أتطابق البايتاتُ ما نُقِل؟"""

    card_id: str
    seal_matches: bool
    excerpt_matches: bool
    found_text: str

    @property
    def is_reproduced(self) -> bool:
        """أأُعيد إنتاجُ المقتطَف من بايتاته؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.seal_matches and self.excerpt_matches


def read_source_cards() -> tuple[SourceReading, ...]:
    """اقرأ البطاقاتِ من بايتات الكتاب، ولا تُصدِّق المنقولَ في هذه الوحدة.

    المدخل: لا شيء؛ الموضعُ والختمُ مُعلَنان في الوحدة.
    الشرط: الكتابُ حاضرٌ في موضعه.
    المخرج: لكلّ بطاقةٍ قراءةٌ تُسمّي أمطابقٌ ختمُها ومقتطَفُها أم لا.
    حدُّها: تُثبِت وقوعَ النصّ في الموضع، لا صدقَ مضمونه.
    """

    path = the_book_path()
    seal_matches = (
        path.is_file()
        and hashlib.sha256(path.read_bytes()).hexdigest() == THE_BOOK_SEAL
    )
    text = the_extraction() if path.is_file() else ""
    readings: list[SourceReading] = []
    for card in THE_SOURCE_CARDS:
        found = text[card.start : card.end]
        readings.append(
            SourceReading(
                card_id=card.card_id,
                seal_matches=seal_matches,
                excerpt_matches=found == card.excerpt,
                found_text=found,
            )
        )
    return tuple(readings)


THE_SOURCE_SCOPE: Final[Scope] = Scope(domain_id="نصُّ-التفكير-المستخرَج")
THE_SIM_SCOPE: Final[Scope] = Scope(domain_id="مجالُ-المحاكاة-المُعلَن")
THE_CITY_SCOPE: Final[Scope] = Scope(domain_id="مجالُ-الشخص-والمدينة")


def _evidence(
    evidence_id: str, genus: EvidenceGenus, statement: str, source: str, scope: Scope
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=genus,
        statement=statement,
        source_name=source,
        scope=scope,
    )


def source_propositions() -> tuple[tuple[Evidence, Individual, Proposition], ...]:
    """حوِّل البطاقاتِ المُعادَ إنتاجُها إلى قضايا **نسبةِ قولٍ إلى موضعه**.

    المدخل: لا شيء؛ تُقرَأ البطاقاتُ من القرص.
    الشرط: البطاقةُ مُعادةُ الإنتاج؛ وما لم يُعَد إنتاجُه لا يُودَع.
    المخرج: لكلّ بطاقةٍ دليلٌ وفردٌ (هو موضعُ الوقوع) وقضيّةُ نسبة.
    حدُّها: المحمولُ «وقع في هذا الموضع»، لا «هذا صحيح».
    """

    rows: list[tuple[Evidence, Individual, Proposition]] = []
    for card, reading in zip(THE_SOURCE_CARDS, read_source_cards(), strict=True):
        if not reading.is_reproduced:
            continue
        evidence = _evidence(
            f"دليل-{card.card_id}",
            EvidenceGenus.MEASUREMENT,
            (
                f"قُطِع من `{THE_SCANNED_BOOK}` بختم `{THE_BOOK_SEAL[:12]}…` "
                f"المجالُ [{card.start}, {card.end}) فطابق المنقول. و"
                + A_SAYING_IN_A_SOURCE_IS_NOT_AN_ADOPTED_RULE
            ),
            THE_SCANNED_BOOK,
            THE_SOURCE_SCOPE,
        )
        individual = Individual(
            individual_id=f"موضع-{card.card_id}",
            designation_method=DesignationMethod.DEFINITE_DESCRIPTION,
            candidate_type_ids=("موضعٌ-في-نصٍّ-مختوم",),
            existence=ExistenceStanding.ESTABLISHED,
            evidence_ref=evidence.ref,
        )
        proposition = Proposition(
            proposition_id=f"قضية-{card.card_id}",
            form=PropositionForm.ATTRIBUTE_VALUE,
            subject_id=individual.individual_id,
            predicate_id="نصُّ-الوقوع",
            value=card.excerpt,
            polarity=Polarity.AFFIRMED,
            scope=THE_SOURCE_SCOPE,
            evidence_ref=evidence.ref,
        )
        rows.append((evidence, individual, proposition))
    return tuple(rows)


def living_rule() -> InferenceRule:
    """القاعدةُ الوحيدةُ المعتمدةُ في هذه الشريحة: البشرُ كائنٌ حيّ."""

    evidence = _evidence(
        "دليل-مصدر-قاعدة-الحياة",
        EvidenceGenus.STIPULATED_DEFINITION,
        "تعريفٌ اصطلاحيٌّ مُعلَنٌ في هذا المجال: كلُّ ما كان بشرًا فهو كائنٌ حيّ",
        "اصطلاحُ هذه الشريحة",
        THE_SIM_SCOPE,
    )
    return InferenceRule(
        rule_id="قاعدة-البشر-كائن-حي",
        version="1",
        kind=RuleKind.STRICT_IN_THE_DECLARED_MODEL,
        premise_patterns=("فردٌ من نوع البشر",),
        conclusion_pattern="فردٌ من نوع الكائن الحيّ",
        applicability_note="تنطبق على فردٍ أُثبِت انتماؤه إلى البشر في النطاق نفسِه",
        blocker_ids=(),
        evidence_ref=evidence.ref,
    )


@dataclass(frozen=True, slots=True)
class SliceOutcome:
    """أثرُ الشريحة: سطورٌ مرقَّمةٌ تُقرَأ، وبصمةُ الرصيد في كلّ مرحلة."""

    lines: tuple[str, ...]
    fingerprints: tuple[tuple[str, str], ...]


def base_stock() -> KnowledgeStock:
    """الرصيدُ الابتدائيّ: مشاهداتُ المجالَين قبل أيّ ترخيصِ هويّة.

    المدخل: لا شيء.
    الشرط: لا شيء؛ البياناتُ مُعلَنةٌ في هذه الوحدة.
    المخرج: رصيدٌ فيه الأفرادُ والتسمياتُ وأدلّةُ المحاكاة وبطاقاتُ المصدر.
    حدُّها: كلُّ دليلٍ فيه محاكاةٌ إلّا قطعَ الكتاب المختوم.
    """

    register = FactRegister(register_id="سجلّ-الشريحة")
    network = IdentityNetwork(network_id="شبكة-الشريحة")
    simulated = _evidence(
        "دليل-مشاهدات-المحاكاة",
        EvidenceGenus.DECLARED_HYPOTHESIS,
        "فرضيّةٌ مُعلَنةٌ كتبتها هذه الوحدة؛ و" + A_SIMULATED_EVIDENCE_STAYS_SIMULATED,
        "مجالُ المحاكاة",
        THE_SIM_SCOPE,
    )
    report = _evidence(
        "دليل-تقرير-مقبول",
        EvidenceGenus.ACCEPTED_REPORT,
        "تقريرٌ مقبولٌ في هذا المجال التجريبيّ؛ و" + A_SIMULATED_EVIDENCE_STAYS_SIMULATED,
        "مجالُ المحاكاة",
        THE_SIM_SCOPE,
    )
    city_report = _evidence(
        "دليل-تقرير-المدينة",
        EvidenceGenus.ACCEPTED_REPORT,
        "تقريرٌ مقبولٌ عن مجال الشخص والمدينة؛ و" + A_SIMULATED_EVIDENCE_STAYS_SIMULATED,
        "مجالُ الشخص والمدينة",
        THE_CITY_SCOPE,
    )
    second_report = _evidence(
        "دليل-تقرير-ثانٍ",
        EvidenceGenus.ACCEPTED_REPORT,
        "تقريرٌ مقبولٌ ثانٍ مستقلُّ المصدر في المحاكاة؛ و"
        + A_SIMULATED_EVIDENCE_STAYS_SIMULATED,
        "مجالُ المحاكاة",
        THE_SIM_SCOPE,
    )
    register = (
        register.with_evidence(simulated)
        .with_evidence(second_report)
        .with_evidence(report)
        .with_evidence(city_report)
    )
    for individual_id, scope, evidence in (
        ("عيّنة-أولى", THE_SIM_SCOPE, report),
        ("عيّنة-ثانية", THE_SIM_SCOPE, report),
        ("فرد-سكّان-أ", THE_CITY_SCOPE, city_report),
        ("فرد-سكّان-ب", THE_CITY_SCOPE, city_report),
        ("فرد-المدينة", THE_CITY_SCOPE, city_report),
    ):
        register = register.with_individual(
            Individual(
                individual_id=individual_id,
                designation_method=DesignationMethod.PROPER_NAME,
                candidate_type_ids=(),
                existence=ExistenceStanding.ESTABLISHED,
                evidence_ref=evidence.ref,
            )
        )
    for evidence, individual, proposition in source_propositions():
        register = (
            register.with_evidence(evidence)
            .with_individual(individual)
            .with_proposition(proposition)
        )
    for naming_id, surface, named_id, genus in (
        ("تسمية-أ", "سالم", "فرد-سكّان-أ", NamingGenus.PROPER_NAME),
        ("تسمية-ب", "سالم", "فرد-سكّان-ب", NamingGenus.PROPER_NAME),
        ("تسمية-المدينة", "يثرب", "فرد-المدينة", NamingGenus.TOPONYM),
        ("تسمية-المدينة-الأخرى", "المدينة", "فرد-المدينة", NamingGenus.TOPONYM),
    ):
        network = network.with_naming(
            Naming(
                naming_id=naming_id,
                surface=surface,
                named_id=named_id,
                named_kind=NamedKind.INDIVIDUAL,
                genus=genus,
                language_id="ar",
                scope=THE_CITY_SCOPE,
                evidence_ref=city_report.ref,
            ),
            register,
        )
    network = network.with_criterion(
        IdentityCriterion(
            criterion_id="معيار-السكّان",
            key_names=("رقمُ السجلّ", "مكانُ القيد"),
            scope=THE_CITY_SCOPE,
            authority="سلطةُ قيدٍ مفترَضةٌ في المحاكاة",
        )
    )
    witness = _evidence(
        "دليل-تنافي-الحجر-والشجر",
        EvidenceGenus.STIPULATED_DEFINITION,
        "اصطلاحُ هذا المجال: لا يجتمع الحجرُ والشجرُ في عيّنةٍ واحدة",
        "اصطلاحُ هذه الشريحة",
        THE_SIM_SCOPE,
    )
    register = register.with_evidence(witness)
    return KnowledgeStock(
        stock_id="رصيد-الشريحة",
        version=0,
        register=register,
        identity=network,
        incompatibilities=(
            IncompatibilityWitness(
                witness_id="شهادة-الحجر-والشجر",
                type_a_id="حجر",
                type_b_id="شجر",
                scope=THE_SIM_SCOPE,
                evidence_ref=witness.ref,
            ),
        ),
    )


def _membership(
    proposition_id: str, subject: str, type_id: str, scope: Scope, evidence: Evidence
) -> Proposition:
    return Proposition(
        proposition_id=proposition_id,
        form=PropositionForm.TYPE_MEMBERSHIP,
        subject_id=subject,
        predicate_id=type_id,
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=scope,
        evidence_ref=evidence.ref,
    )


def run_slice() -> SliceOutcome:
    """شغِّل الشريحةَ كلَّها وأخرِج أثرَها سطرًا سطرًا.

    المدخل: لا شيء.
    الشرط: الكتابُ حاضرٌ لبطاقات المصدر؛ وغيابُه يُنقِص سطرَ المصدر وحدَه.
    المخرج: سطورُ الأثر وبصماتُ الرصيد عند كلّ مرحلة.
    حدُّها: كلُّ حكمٍ فيه حكمٌ عن هذا الرصيد، لا عن العالم.
    """

    lines: list[str] = []
    marks: list[tuple[str, str]] = []
    stock = base_stock()
    marks.append(("الابتداء", stock.content_id[:12]))
    report = stock.register.evidence_of("دليل-تقرير-مقبول")
    simulated = stock.register.evidence_of("دليل-مشاهدات-المحاكاة")
    second = stock.register.evidence_of("دليل-تقرير-ثانٍ")
    city = stock.register.evidence_of("دليل-تقرير-المدينة")

    readings = read_source_cards()
    reproduced = sum(1 for one in readings if one.is_reproduced)
    lines.append(
        f"١ · بطاقاتُ المصدر: {reproduced}/{len(readings)} أُعيد إنتاجُها من "
        f"`{THE_SCANNED_BOOK}`؛ وهي نسبةُ قولٍ لا شهادةٌ على واقعة"
    )

    refusal = ""
    try:
        stock.admit(
            _membership("حكم-مفترَض", "عيّنة-ثانية", "بشر", THE_SIM_SCOPE, simulated),
            AdmissionLicence(
                proposition_id="حكم-مفترَض",
                scope=THE_SIM_SCOPE,
                evidence_ref=simulated.ref,
                recorded_order=0,
            ),
        )
    except FactError as error:  # pragma: no cover - المسارُ مُقاسٌ في الاختبار
        refusal = str(error).split("؛")[0]
    lines.append(f"٢ · فرضيّةٌ مُعلَنةٌ لا تُودِع وقوعًا: {refusal}")

    # حجرٌ ← شجرٌ: اجتماعٌ متنافٍ بشهادة
    stock = stock.admit(
        _membership("حكم-عيّنة-حجر", "عيّنة-أولى", "حجر", THE_SIM_SCOPE, report),
        AdmissionLicence(
            proposition_id="حكم-عيّنة-حجر",
            scope=THE_SIM_SCOPE,
            evidence_ref=report.ref,
            recorded_order=1,
        ),
    )
    stock = stock.admit(
        _membership("حكم-عيّنة-شجر", "عيّنة-أولى", "شجر", THE_SIM_SCOPE, second),
        AdmissionLicence(
            proposition_id="حكم-عيّنة-شجر",
            scope=THE_SIM_SCOPE,
            evidence_ref=second.ref,
            recorded_order=2,
        ),
    )
    reading = stock.types_of("عيّنة-أولى", THE_SIM_SCOPE)
    lines.append(
        f"٣ · العيّنةُ الأولى: {len(reading.type_ids)} نوعًا، والتعارضُ "
        f"{'مشهودٌ' if reading.is_conflicted else 'غيرُ مشهود'} "
        f"بـ{reading.witness_ids}"
    )

    # تصحيحٌ صريحٌ يحفظ القديم
    correction_evidence = _evidence(
        "دليل-التصحيح",
        EvidenceGenus.ACCEPTED_REPORT,
        "مراجعةٌ مقبولةٌ في المحاكاة: العيّنةُ الأولى شجرٌ لا حجر",
        "مجالُ المحاكاة",
        THE_SIM_SCOPE,
    )
    stock = stock.with_evidence(correction_evidence)
    stock = stock.correct(
        Correction(
            correction_id="تصحيح-العيّنة-الأولى",
            corrected_proposition_id="حكم-عيّنة-حجر",
            replacement_proposition_id="حكم-عيّنة-شجر-مصحَّح",
            scope=THE_SIM_SCOPE,
            recorded_order=3,
            reason="المشاهدةُ الأولى نُسِبت إلى العيّنة خطأً",
            evidence_ref=correction_evidence.ref,
            policy=ReinstatementPolicy.KEEP_SUSPENDED_UNTIL_NEW_EVIDENCE,
        ),
        _membership(
            "حكم-عيّنة-شجر-مصحَّح",
            "عيّنة-أولى",
            "شجر",
            THE_SIM_SCOPE,
            correction_evidence,
        ),
        AdmissionLicence(
            proposition_id="حكم-عيّنة-شجر-مصحَّح",
            scope=THE_SIM_SCOPE,
            evidence_ref=correction_evidence.ref,
            recorded_order=4,
        ),
    )
    old = stock.register.proposition_of("حكم-عيّنة-حجر")
    lines.append(
        f"٤ · بعد التصحيح: القديمُ {'معلَّقٌ ومحفوظ' if old.suspended else 'قائم'}، "
        f"وتاريخُه {len(stock.corrections_of('حكم-عيّنة-حجر'))} قرارًا، "
        f"والسياسةُ `{stock.corrections[-1].policy.value}`"
    )
    marks.append(("بعد التصحيح", stock.content_id[:12]))

    # بشرٌ: قاعدةٌ معتمدةٌ تُطبَّق ثمّ يُنقَض اعتمادُها
    rule = living_rule()
    adoption_evidence = _evidence(
        "دليل-اعتماد-قاعدة-الحياة",
        EvidenceGenus.STIPULATED_DEFINITION,
        f"يُعتمَد في هذا المجال تطبيقُ `{rule.versioned_id}` على أفراده",
        "اصطلاحُ هذه الشريحة",
        THE_SIM_SCOPE,
    )
    stock = stock.adopt_rule(
        rule,
        AdoptionLicence(
            rule_versioned_id=rule.versioned_id,
            origin=RuleOrigin.TRANSMITTED_FROM_A_SOURCE,
            condition_note="فردٌ أُثبِت انتماؤه إلى البشر في النطاق نفسِه",
            evidence_ref=adoption_evidence.ref,
        ),
        adoption_evidence,
    )
    stock = stock.admit(
        _membership("حكم-ب-بشر", "فرد-سكّان-ب", "بشر", THE_CITY_SCOPE, city),
        AdmissionLicence(
            proposition_id="حكم-ب-بشر",
            scope=THE_CITY_SCOPE,
            evidence_ref=city.ref,
            recorded_order=5,
        ),
    )
    derived = Proposition(
        proposition_id="حكم-ب-كائن-حي",
        form=PropositionForm.TYPE_MEMBERSHIP,
        subject_id="فرد-سكّان-ب",
        predicate_id="كائنٌ-حيّ",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_CITY_SCOPE,
        evidence_ref=city.ref,
        derived_from_proposition_ids=("حكم-ب-بشر",),
        derived_by_rule=rule.versioned_id,
    )
    stock, blocked = stock.apply_adopted_rule(
        rule.versioned_id,
        ("حكم-ب-بشر",),
        derived,
        AdmissionLicence(
            proposition_id="حكم-ب-كائن-حي",
            scope=THE_CITY_SCOPE,
            evidence_ref=city.ref,
            recorded_order=6,
            depends_on_proposition_ids=("حكم-ب-بشر",),
        ),
    )
    reading = stock.types_of("فرد-سكّان-ب", THE_CITY_SCOPE)
    lines.append(
        f"٥ · «بشر» و«كائنٌ حيّ» اجتمعا في فردٍ واحد: {reading.type_ids}؛ "
        f"والتعارضُ {'مشهودٌ' if reading.is_conflicted else 'غيرُ مشهود'} "
        f"(المانعُ: {blocked})"
    )

    # تعدّدُ المرشّحين، ثمّ رابطُ هويّةٍ ونقضُه
    from ..ontology.identity import candidates_for_surface, linked_individual_ids

    candidates = candidates_for_surface("سالم", stock.identity, stock.register)
    lines.append(f"٦ · «سالم» رشّح {len(candidates)} فردًا، ولم يُدمَجا لاتّفاق الاسم")

    link_evidence = _evidence(
        "دليل-رابط-سالم",
        EvidenceGenus.ACCEPTED_REPORT,
        "قيدٌ مفترَضٌ في المحاكاة: المفتاحان متوافقان في الفردين",
        "سلطةُ القيد المفترَضة",
        THE_CITY_SCOPE,
    )
    stock = stock.with_evidence(link_evidence)
    network = stock.identity.with_link(
        IdentityLink(
            link_id="رابط-سالم",
            left_individual_id="فرد-سكّان-أ",
            right_individual_id="فرد-سكّان-ب",
            criterion_id="معيار-السكّان",
            key_readings=(
                KeyReading(key_name="رقمُ السجلّ", left_value="٧٧", right_value="٧٧"),
                KeyReading(
                    key_name="مكانُ القيد", left_value="يثرب", right_value="يثرب"
                ),
            ),
            evidence_ref=link_evidence.ref,
        ),
        stock.register,
    )
    stock = stock.with_identity(network)
    lines.append(
        "٧ · بعد الرابط: «فرد-سكّان-أ» موحَّدٌ مع "
        + str(
            tuple(
                one
                for one in linked_individual_ids("فرد-سكّان-أ", stock.identity)
                if one != "فرد-سكّان-أ"
            )
        )
    )

    # سحبُ ترخيص القاعدة يُعطِّل تطبيقَها ويُبقي السندَ المستقلّ
    claim = ClaimKey(
        subject_id="فرد-سكّان-ب",
        predicate_id="كائنٌ-حيّ",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_CITY_SCOPE,
    )
    before = stock.verdict_for(claim)
    stock = stock.revoke_adoption(rule.versioned_id)
    after = stock.verdict_for(claim)
    lines.append(
        f"٨ · نقضُ اعتماد القاعدة: `{before.standing.value}` ← "
        f"`{after.standing.value}`"
    )
    marks.append(("بعد نقض الاعتماد", stock.content_id[:12]))

    direct = _evidence(
        "دليل-مباشر-للحياة",
        EvidenceGenus.ACCEPTED_REPORT,
        "تقريرٌ مباشرٌ مقبولٌ في المحاكاة: هذا الفردُ كائنٌ حيّ",
        "مجالُ الشخص والمدينة",
        THE_CITY_SCOPE,
    )
    stock = stock.with_evidence(direct)
    stock = stock.admit(
        _membership(
            "حكم-ب-كائن-حي-مباشر", "فرد-سكّان-ب", "كائنٌ-حيّ", THE_CITY_SCOPE, direct
        ),
        AdmissionLicence(
            proposition_id="حكم-ب-كائن-حي-مباشر",
            scope=THE_CITY_SCOPE,
            evidence_ref=direct.ref,
            recorded_order=7,
        ),
    )
    restored = stock.verdict_for(claim)
    lines.append(
        f"٩ · بعد السند المستقلّ: `{restored.standing.value}`، وطوائفُ السند "
        f"{restored.independent_support_count}"
    )
    marks.append(("بعد السند المستقلّ", stock.content_id[:12]))
    return SliceOutcome(lines=tuple(lines), fingerprints=tuple(marks))
