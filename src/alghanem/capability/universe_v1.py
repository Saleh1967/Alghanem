"""`G0.METRIC-0`: `DeclaredArabicCapabilityUniverseV1` — المقامُ المُعلَن.

هذا المقامُ **دعوى إعلانٍ لا أنطولوجيا تامّة للعربية**
(`ADeclaredDenominatorIsNotTheCompleteOntologyOfArabic`): سبعةَ عشرَ مجالًا
أعلى، وتحتها الأبوابُ المصطلَحُ عليها في فنّها، كلُّ بابٍ باستشهاده. وليس فيه
عقدةٌ واحدةٌ أُدخِلت لأنّها مبنيّةٌ في الشجرة، ولا أُخرِجت لأنّها ليست مبنيّة
(`MissingImplementationDoesNotRemoveACapabilityFromTheDenominator`).

وتوسعةُ هذا الملفّ تُنقِص النسبَ، وهو المقصود: الرقمُ المنخفضُ المُشتَقُّ أصدقُ
من الرقم المرتفع المُقدَّر.
"""

from __future__ import annotations

from typing import Final

from .maturity import MaturityStage
from .node import CapabilityCitation, CapabilityNode, NodeKind, Requirement
from .universe import CapabilityUniverse

__all__ = [
    "ARABIC_TOTAL_ID",
    "DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1",
    "DECLARED_READINESS_GATE",
    "UNIVERSE_V1_ID",
    "build_declared_universe_v1",
]

UNIVERSE_V1_ID: Final[str] = "DeclaredArabicCapabilityUniverseV1"
ARABIC_TOTAL_ID: Final[str] = "ARABIC_TOTAL"

DECLARED_READINESS_GATE: Final[MaturityStage] = MaturityStage.S5_FROZEN_DOMAIN
"""بوّابةُ الأهليّة المُعلَنة: بوّابةٌ مُصرَّحٌ بها لا مُشتَقّةٌ من خاصّةٍ للعربية."""

_C = Requirement.CONTRIBUTING
_R = Requirement.REQUIRED

_DomainSpec = tuple[str, str, str, tuple[tuple[str, str, Requirement], ...]]

_DOMAINS: Final[tuple[_DomainSpec, ...]] = (
    (
        "A0",
        "SOUND_ENCODING — الصوت والترميز",
        "sirr_sinaat_al_irab",
        (
            ("SOUND", "الصوت", _R),
            ("MAKHARIJ", "المخارج", _R),
            ("LETTERS", "الحروف", _R),
            ("HARAKAT", "الحركات", _R),
            ("SUKUN", "السكون", _R),
            ("SHADDA", "الشدّة", _R),
            ("TANWIN", "التنوين", _R),
            ("MADD", "المدّ", _R),
            ("HAMZ", "الهمز", _R),
            ("WASL_QAT", "الوصل والقطع", _R),
            ("SYLLABLE", "المقطع", _R),
        ),
    ),
    (
        "A1",
        "SURFACE_WORD_BUILD — بناء الكلمة الظاهرة",
        "shafiya_ibn_al_hajib",
        (
            ("NOUN_VERB_PARTICLE", "الاسم والفعل والحرف", _R),
            ("BUILT_VS_DECLINED", "المبنيّ والمعرب", _R),
            ("FROZEN_VS_DERIVED", "الجامد والمشتقّ", _R),
            ("MASDAR", "المصدر", _R),
            ("AUGMENT_LETTERS", "الحروف الزائدة", _R),
        ),
    ),
    (
        "A2",
        "CLOSED_CLASSES_PARTICLES — الأدوات والطبقات المغلقة",
        "mughni_al_labib",
        (
            ("JARR_PARTICLES", "حروف الجرّ", _R),
            ("ATF_PARTICLES", "حروف العطف", _R),
            ("SHART_PARTICLES", "أدوات الشرط", _R),
            ("TAQIB_PARTICLES", "حروف التعقيب", _R),
            ("TALIL_PARTICLES", "حروف التعليل", _R),
            ("NAFY_PARTICLES", "أدوات النفي", _R),
            ("NIDA_PARTICLES", "أدوات النداء", _R),
            ("ISTITHNA_PARTICLES", "أدوات الاستثناء", _R),
            ("HASR_PARTICLES", "أدوات الحصر", _R),
            ("ISTIFHAM_PARTICLES", "أدوات الاستفهام", _R),
            ("ISTIQBAL_PARTICLES", "أدوات الاستقبال", _R),
            ("NASB_PARTICLES", "حروف النصب", _R),
            ("JAZM_PARTICLES", "حروف الجزم", _R),
            ("RELATIVE_NOUNS", "الأسماء الموصولة", _R),
            ("DEMONSTRATIVES", "أسماء الإشارة", _R),
        ),
    ),
    (
        "A3",
        "ROOT_DERIVATION — الجذر والاشتقاق",
        "shafiya_ibn_al_hajib",
        (
            ("ROOT", "الجذر", _R),
            ("TRILITERAL_QUADRILITERAL", "الثلاثيّ والرباعيّ", _R),
            ("SOUND_ROOT", "الصحيح", _R),
            ("WEAK_ROOT", "المعتلّ", _R),
            ("HAMZATED_ROOT", "المهموز", _R),
            ("GEMINATE_ROOT", "المضعَّف", _R),
            ("BARE_VS_AUGMENTED", "المجرَّد والمزيد", _R),
            ("DERIVATION", "الاشتقاق", _R),
            ("PATTERN", "الوزن", _R),
            ("ILAL", "الإعلال", _R),
            ("IDGHAM", "الإدغام", _R),
        ),
    ),
    (
        "A4",
        "VERB_SYSTEM — نظام الفعل",
        "sharh_ibn_aqil",
        (
            ("PAST", "الماضي", _R),
            ("PRESENT", "المضارع", _R),
            ("IMPERATIVE", "الأمر", _R),
            ("ACTIVE_VOICE", "المعلوم", _R),
            ("PASSIVE_VOICE", "المجهول", _R),
            ("INTRANSITIVE", "اللازم", _R),
            ("TRANSITIVE", "المتعدّي", _R),
            ("MUTAWAA", "المطاوعة", _R),
            ("MUSHARAKA", "المشاركة", _R),
            ("TALAB", "الطلب", _R),
            ("AUGMENT_SEMANTICS", "دلالات الزيادة", _R),
        ),
    ),
    (
        "A5",
        "NOMINAL_DERIVATION — المشتقّات الاسميّة",
        "shafiya_ibn_al_hajib",
        (
            ("ACTIVE_PARTICIPLE", "اسم الفاعل", _R),
            ("PASSIVE_PARTICIPLE", "اسم المفعول", _R),
            ("INSTRUMENT_NOUN", "اسم الآلة", _R),
            ("TIME_NOUN", "اسم الزمان", _R),
            ("PLACE_NOUN", "اسم المكان", _R),
            ("ASSIMILATE_ADJECTIVE", "الصفة المشبَّهة", _R),
            ("COMPARATIVE", "أفعل التفضيل", _R),
            ("DIMINUTIVE", "التصغير", _C),
            ("RELATIVE_ADJECTIVE", "النسبة", _C),
        ),
    ),
    (
        "A6",
        "NOMINAL_FEATURES — سمات الاسم",
        "sharh_ibn_aqil",
        (
            ("GENDER", "التذكير والتأنيث", _R),
            ("SINGULAR", "المفرد", _R),
            ("DUAL", "المثنّى", _R),
            ("PLURAL", "الجمع", _R),
            ("SOUND_PLURALS", "الجموع السالمة", _R),
            ("BROKEN_PLURAL", "جمع التكسير", _R),
            ("NUMBER_AND_COUNTED", "العدد والمعدود", _R),
            ("DEFINITE_INDEFINITE", "المعرفة والنكرة", _R),
            ("DIPTOTE", "الممنوع من الصرف", _R),
            ("FIVE_NOUNS", "الأسماء الخمسة", _R),
            ("FIVE_VERBS", "الأفعال الخمسة", _R),
        ),
    ),
    (
        "A7",
        "SINGLE_WORD_COMPOSITION — تركيب الكلمة الواحدة",
        "shafiya_ibn_al_hajib",
        (
            ("ROOT_PATTERN_COMPOSITION", "اجتماع الجذر والوزن", _R),
            ("AFFIX_COMPOSITION", "الزوائد والضمائر المتّصلة", _R),
            ("DEFINITE_ARTICLE_ATTACHMENT", "اتّصال أل", _R),
            ("SEGMENT_BOUNDARY", "حدّ المقطع الصرفيّ", _R),
        ),
    ),
    (
        "A8",
        "SYNTAX_COMPOSITION — التركيب النحويّ",
        "sharh_ibn_aqil",
        (
            ("OPERATOR", "العامل", _R),
            ("OPERAND", "المعمول", _R),
            ("NOMINAL_SENTENCE", "الجملة الاسميّة", _R),
            ("VERBAL_SENTENCE", "الجملة الفعليّة", _R),
            ("QUASI_SENTENCE", "شبه الجملة", _R),
            ("PREDICATION", "الإسناد", _R),
            ("EMBEDDING", "التضمين", _R),
            ("RESTRICTION", "التقييد", _R),
        ),
    ),
    (
        "A9",
        "SYNTACTIC_ROLES — الوظائف النحويّة",
        "sharh_ibn_aqil",
        (
            ("MUBTADA", "المبتدأ", _R),
            ("KHABAR", "الخبر", _R),
            ("FAIL", "الفاعل", _R),
            ("NAIB_FAIL", "نائب الفاعل", _R),
            ("OBJECTS", "المفاعيل", _R),
            ("HAL", "الحال", _R),
            ("TAMYIZ", "التمييز", _R),
            ("BADAL", "البدل", _R),
            ("TAWKID", "التوكيد", _R),
            ("KANA_ISM_KHABAR", "اسم كان وخبرها", _R),
            ("INNA_ISM_KHABAR", "اسم إنّ وخبرها", _R),
            ("MAQUL_AL_QAWL", "مقول القول", _R),
            ("HIKAYA", "الحكاية", _C),
        ),
    ),
    (
        "A10",
        "IRAB — الإعراب",
        "mughni_al_labib",
        (
            ("RAF", "الرفع", _R),
            ("NASB", "النصب", _R),
            ("JARR", "الجرّ", _R),
            ("JAZM", "الجزم", _R),
            ("PRIMARY_MARKERS", "العلامات الأصليّة", _R),
            ("SECONDARY_MARKERS", "العلامات الفرعيّة", _R),
            ("OVERT_MARKERS", "العلامات الظاهرة", _R),
            ("ESTIMATED_MARKERS", "العلامات المقدَّرة", _R),
        ),
    ),
    (
        "A11",
        "RELATIONAL_SEMANTICS — الدلالة النسبيّة",
        "al_mustasfa",
        (
            ("AGENTIVITY", "الفاعليّة", _R),
            ("PATIENTIVITY", "المفعوليّة", _R),
            ("CAUSATION", "السببيّة", _R),
            ("RESULTATIVITY", "المسبَّبيّة", _R),
        ),
    ),
    (
        "A12",
        "DALALAH — الدلالة",
        "sharh_al_tahdhib",
        (
            ("MUTABAQA", "دلالة المطابقة", _R),
            ("TADAMMUN", "دلالة التضمّن", _R),
            ("ILTIZAM", "دلالة الالتزام", _R),
            ("HAQIQA", "الحقيقة", _R),
            ("MAJAZ", "المجاز", _R),
            ("KULLI", "الكلّيّ", _R),
            ("JUZI", "الجزئيّ", _R),
            ("MUTAWATI", "المتواطئ", _R),
            ("MUTABAYIN", "المتباين", _R),
            ("MUSHAKKIK", "المشكِّك", _R),
            ("MURADIF", "المترادف", _R),
            ("MANQUL", "المنقول", _R),
        ),
    ),
    (
        "A13",
        "DISCOURSE_PRAGMATICS — الخطاب والمقام",
        "miftah_al_ulum",
        (
            ("SPEAKER", "المتكلّم", _R),
            ("ADDRESSEE", "المخاطَب", _R),
            ("ABSENT_REFERENT", "الغائب", _R),
            ("KHABAR_MODE", "الخبر", _R),
            ("INSHA_MODE", "الإنشاء", _R),
            ("COMMAND", "الأمر", _R),
            ("PROHIBITION", "النهي", _R),
            ("INTERROGATION", "الاستفهام", _R),
            ("VOCATIVE", "النداء", _R),
            ("NEGATION", "النفي", _R),
            ("EMPHASIS", "التوكيد", _R),
            ("EXCEPTION", "الاستثناء", _R),
            ("EXCLUSIVITY", "الحصر", _R),
        ),
    ),
    (
        "A14",
        "TEMPORAL_SYSTEM — النظام الزمنيّ",
        "miftah_al_ulum",
        (
            ("SPEECH_TIME", "زمن التكلّم", _R),
            ("REFERENCE_TIME", "زمن الإسناد المرجعيّ", _R),
            ("EVENT_TIME", "زمن الحدث", _R),
            ("EVENT_REFERENCE_TIME_RELATION", "علاقة زمن الحدث بالمرجع", _R),
            ("CONTINUITY", "الاستمرار", _R),
            ("DISCONTINUITY", "الانقطاع", _R),
            ("NARRATIVE_TIME", "زمن الحكاية", _R),
            ("REPORTED_SPEECH", "الخطاب المنقول", _R),
        ),
    ),
    (
        "A15",
        "USUL_INFERENCE — الاستدلال الأصوليّ",
        "al_mustasfa",
        (
            ("MUTLAQ", "المطلق", _R),
            ("MUQAYYAD", "المقيَّد", _R),
            ("AMM", "العامّ", _R),
            ("KHASS", "الخاصّ", _R),
            ("MAFHUM_MUWAFAQA", "مفهوم الموافقة", _R),
            ("MAFHUM_MUKHALAFA", "مفهوم المخالفة", _R),
            ("SHART", "الشرط", _R),
            ("SABAB", "السبب", _R),
            ("MANI", "المانع", _R),
            ("SIHHA", "الصحّة", _R),
            ("BUTLAN", "البطلان", _R),
            ("FASAD", "الفساد", _R),
        ),
    ),
    (
        "A16",
        "SIGNIFIER_SIGNIFIED_FRACTAL — الدالّ والمدلول",
        "sharh_al_tahdhib",
        (
            ("SIGNIFIER_ALONE", "الدالّ وحده", _R),
            ("SIGNIFIED_ALONE", "المدلول وحده", _R),
            ("SIGNIFIER_WITH_SIGNIFIED", "الدالّ والمدلول معًا", _R),
            ("WAD", "الوضع", _R),
            ("DALALA", "الدلالة", _R),
            ("NISBA", "النسبة", _R),
            ("IFADA", "الإفادة", _R),
            ("HUKM", "الحكم", _R),
            ("TANZIL", "التنزيل", _R),
        ),
    ),
)


def build_declared_universe_v1() -> CapabilityUniverse:
    """ابنِ المقامَ المُعلَن من إعلانه وحدَه؛ لا يُقرأ هنا ملفٌّ من `src/`."""

    nodes: list[CapabilityNode] = [
        CapabilityNode(
            node_id=ARABIC_TOTAL_ID,
            title="العربية — المقام المُعلَن",
            kind=NodeKind.TOTAL,
            parent_id=None,
            requirement=Requirement.REQUIRED,
            citation=CapabilityCitation(
                source_id="sharh_ibn_aqil", locus="مقدّمة علم العربية"
            ),
            readiness_gate=DECLARED_READINESS_GATE,
        )
    ]
    for domain_id, domain_title, source_id, capabilities in _DOMAINS:
        nodes.append(
            CapabilityNode(
                node_id=domain_id,
                title=domain_title,
                kind=NodeKind.DOMAIN,
                parent_id=ARABIC_TOTAL_ID,
                requirement=Requirement.REQUIRED,
                citation=CapabilityCitation(
                    source_id=source_id, locus=domain_title.split("—")[-1].strip()
                ),
                readiness_gate=DECLARED_READINESS_GATE,
            )
        )
        for local_id, title, requirement in capabilities:
            nodes.append(
                CapabilityNode(
                    node_id=f"{domain_id}.{local_id}",
                    title=title,
                    kind=NodeKind.CAPABILITY,
                    parent_id=domain_id,
                    requirement=requirement,
                    citation=CapabilityCitation(source_id=source_id, locus=title),
                    readiness_gate=DECLARED_READINESS_GATE,
                )
            )
    return CapabilityUniverse(UNIVERSE_V1_ID, nodes)


DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1: Final[CapabilityUniverse] = (
    build_declared_universe_v1()
)
"""المقامُ المُعلَنُ الأوّل، مُجمَّدًا ببيانه ومُلخَّصِ محتواه."""
