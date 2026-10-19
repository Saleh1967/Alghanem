"""مسارُ الهويّة عاملًا: من وقوعٍ مختومٍ إلى قضيّةٍ محكومٍ عليها، ثمّ مراجعتُها.

المجالُ ههنا **بيانات**: أشخاصٌ ومدنٌ وتسمياتٌ ومعاييرُ وروابط. ولا اسمَ شخصٍ
ولا اسمَ مدينةٍ في مفردةٍ مغلقة؛ المفرداتُ المغلقةُ للقرارات وحدَها (جنسُ
التسمية، منزلةُ المفتاح، سياسةُ التعارض). فإضافةُ شخصٍ أو مدينةٍ سطرُ بيانٍ
ههنا لا تعديلُ محرّك، و`test_identity_path_run` يُثبِت ذلك بإضافةِ فردٍ ثالثٍ
داخلَ الاختبار دون أن يُمَسّ شيءٌ من الوحدات.

**المواضعُ الثلاثةُ مصدريّةٌ حقيقيّةٌ قابلةٌ لإعادة الاستخراج** من
`corpora/quran-simple-enhanced.txt` بختمه `37633090…`: «زَيْدٌ» عند [499020,
499026) و«يَثْرِبَ» عند [494543, 494551) و«الْمَدِينَةِ» عند [194912, 194924).
وشهادةُ التمثيل تقطع البايتاتِ وتقابلها، فليست دعوى.

**وما عدا ذلك مُعلَنُ الاصطناع.** مَن يحمل الاسمَ، وأيُّ فردٍ هو، ومتى وُحِّد
— كلُّ ذلك أدلّةٌ اصطناعيّةٌ من جنس `DECLARED_HYPOTHESIS` أو `ACCEPTED_REPORT`
عن مصدرٍ مُسمًّى، ولا واحدةَ منها `DIRECT_OBSERVATION`: فلا اختبارَ ههنا يكتب
مشاهدةً. والوقوعُ اللفظيُّ وحدَه `MEASUREMENT`، لأنّه مقيسٌ من بايتاتٍ مختومة.

**وزيدٌ الذي في ٣٣:٣٧ ليس زيدَ المثال.** الفردانِ ههنا `فرد-زيد-الأوّل` و
`فرد-زيد-الثاني` مفروضانِ لتجربة التعيين؛ والوقوعُ المصدريُّ يُستعمَل لفظًا
واقعًا لا تعيينًا لشخصٍ تاريخيّ. وهذا عينُ ما تمنعه `A_WORD_IS_NOT_ITS_BEARER`.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from alghanem.ontology import (
    ConflictPolicy,
    DesignationMethod,
    Evidence,
    EvidenceGenus,
    ExistenceStanding,
    FactRegister,
    IdentityCriterion,
    IdentityLink,
    IdentityNetwork,
    Individual,
    KeyReading,
    NamedKind,
    Naming,
    NamingCandidate,
    NamingGenus,
    Occurrence,
    OffsetUnit,
    Polarity,
    Proposition,
    PropositionForm,
    RepresentationWitness,
    Scope,
    candidates_for_surface,
    canonical_reading,
    linked_individual_ids,
    witness_occurrence,
)
from alghanem.ontology.occurrence import CanonicalReading

THE_SOURCE_PATH: Final[str] = "corpora/quran-simple-enhanced.txt"
THE_SOURCE_SEAL: Final[str] = (
    "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
)

NO_TEST_WRITES_AN_OBSERVATION: Final[str] = (
    "لا دليلَ ههنا من جنس `DIRECT_OBSERVATION`: ما قِيس من البايتات "
    "`MEASUREMENT`، وما فُرِض للتجربة `DECLARED_HYPOTHESIS`، وما نُسِب إلى "
    "مصدرٍ مُسمًّى `ACCEPTED_REPORT`؛ وغيابُ مصدرٍ واقعيٍّ لا يُبرِّر اختراعَه"
)

THE_ANSWER_IS_NOT_IN_THE_INPUT: Final[str] = (
    "مرشَّحو التعيين يُشتقّون من تسمياتٍ مودَعةٍ بأدلّتها، لا من قائمةٍ "
    "مكتوبةٍ في مدخل المنتج؛ فإضافةُ فردٍ رابعٍ تُغيِّر المخرجَ بلا سطرِ شفرة"
)

THE_DOMAIN: Final[str] = "مجال-شبكة-الهويّة"
THE_TIMELINE: Final[str] = "محور-سنوات-الهجرة"

PERSON_TYPE_ID: Final[str] = "نوع-الإنسان"
CITY_TYPE_ID: Final[str] = "نوع-المدينة"

FIRST_ZAYD: Final[str] = "فرد-زيد-الأوّل"
SECOND_ZAYD: Final[str] = "فرد-زيد-الثاني"
THE_CITY: Final[str] = "فرد-المدينة"

THE_CRITERION: Final[str] = "معيار-هويّة-الأشخاص"
THE_LINK: Final[str] = "رابط-زيدَين"


def _scope(start: int | None = None, end: int | None = None) -> Scope:
    if start is None:
        return Scope(domain_id=THE_DOMAIN)
    return Scope(domain_id=THE_DOMAIN, timeline_id=THE_TIMELINE, start=start, end=end)


def declared_evidence() -> tuple[Evidence, ...]:
    """أدلّةُ المجال كلُّها، كلٌّ بجنسه المُعلَن؛ ولا مشاهدةَ فيها البتّة."""

    return (
        Evidence(
            evidence_id="دليل-وقوع-زيد",
            genus=EvidenceGenus.MEASUREMENT,
            statement=(
                f"اللفظُ «زَيْدٌ» مقيسٌ في `{THE_SOURCE_PATH}` عند [499020, 499026) "
                "بوحدة نقطة الرمز، والختمُ مقابَل"
            ),
            source_name=THE_SOURCE_PATH,
            scope=_scope(),
            source_digest=THE_SOURCE_SEAL,
        ),
        Evidence(
            evidence_id="دليل-وجود-زيد-الأوّل",
            genus=EvidenceGenus.DECLARED_HYPOTHESIS,
            statement="فردٌ مفروضٌ للتجربة يُسمّى «زيد»، سجلُّه مجالُ الشبكة",
            source_name="فرضٌ مُعلَنٌ في هذه الوحدة",
            scope=_scope(),
        ),
        Evidence(
            evidence_id="دليل-وجود-زيد-الثاني",
            genus=EvidenceGenus.DECLARED_HYPOTHESIS,
            statement="فردٌ ثانٍ مفروضٌ للتجربة يُسمّى «زيد» أيضًا، ولا يُطوى في الأوّل",
            source_name="فرضٌ مُعلَنٌ في هذه الوحدة",
            scope=_scope(),
        ),
        Evidence(
            evidence_id="دليل-وجود-المدينة",
            genus=EvidenceGenus.DECLARED_HYPOTHESIS,
            statement="فردُ مدينةٍ مفروضٌ للتجربة، يحمل تسميتَين في زمنَين",
            source_name="فرضٌ مُعلَنٌ في هذه الوحدة",
            scope=_scope(),
        ),
        Evidence(
            evidence_id="دليل-تسمية-يثرب",
            genus=EvidenceGenus.LEXICAL_ATTESTATION,
            statement=(
                f"اللفظُ «يَثْرِبَ» واقعٌ في `{THE_SOURCE_PATH}` عند [494543, 494551)"
            ),
            source_name=THE_SOURCE_PATH,
            scope=_scope(0, 1),
            source_digest=THE_SOURCE_SEAL,
        ),
        Evidence(
            evidence_id="دليل-تسمية-المدينة",
            genus=EvidenceGenus.LEXICAL_ATTESTATION,
            statement=(
                f"اللفظُ «الْمَدِينَةِ» واقعٌ في `{THE_SOURCE_PATH}` عند [194912, 194924)"
            ),
            source_name=THE_SOURCE_PATH,
            scope=_scope(1, 9),
            source_digest=THE_SOURCE_SEAL,
        ),
        Evidence(
            evidence_id="دليل-تسمية-زيد-الأوّل",
            genus=EvidenceGenus.LEXICAL_ATTESTATION,
            statement="اللفظُ «زيد» يُسمّي الفردَ الأوّلَ في سجلّ المجال",
            source_name="سجلُّ تسمياتِ المجال",
            scope=_scope(),
        ),
        Evidence(
            evidence_id="دليل-تسمية-زيد-الثاني",
            genus=EvidenceGenus.LEXICAL_ATTESTATION,
            statement="اللفظُ «زيد» يُسمّي الفردَ الثانيَ أيضًا، واللفظُ واحد",
            source_name="سجلُّ تسمياتِ المجال",
            scope=_scope(),
        ),
        Evidence(
            evidence_id="دليل-كنية-زيد-الثاني",
            genus=EvidenceGenus.LEXICAL_ATTESTATION,
            statement="اللفظُ «أبو أسامة» يُسمّي الفردَ الثانيَ كنيةً",
            source_name="سجلُّ تسمياتِ المجال",
            scope=_scope(),
        ),
        Evidence(
            evidence_id="دليل-رابط-الهويّة",
            genus=EvidenceGenus.ACCEPTED_REPORT,
            statement=(
                "خبرٌ معتمدٌ يذكر أنّ صاحبَ السجلّين واحد: اتّفق مفتاحا "
                "«موضع-الميلاد» و«سنة-الميلاد» عند الطرفَين"
            ),
            source_name="سجلُّ تراجمِ المجال المفروض",
            scope=_scope(0, 20),
        ),
        Evidence(
            evidence_id="دليل-وصول-الأوّل",
            genus=EvidenceGenus.ACCEPTED_REPORT,
            statement="خبرٌ معتمدٌ يذكر وصولَ الفرد الأوّل إلى المدينة في السنة ٥",
            source_name="سجلُّ أخبارِ المجال المفروض",
            scope=_scope(5, 5),
        ),
        Evidence(
            evidence_id="دليل-وصول-الثاني-مباشر",
            genus=EvidenceGenus.ACCEPTED_REPORT,
            statement=(
                "خبرٌ معتمدٌ **مستقلٌّ** يذكر وصولَ الفرد الثاني نفسِه إلى "
                "المدينة في السنة ٥، لا يمرّ برابط الهويّة"
            ),
            source_name="سجلُّ أخبارِ المجال المفروض، بابٌ آخَر",
            scope=_scope(5, 5),
        ),
        Evidence(
            evidence_id="دليل-لا-متعلّق",
            genus=EvidenceGenus.ACCEPTED_REPORT,
            statement="خبرٌ معتمدٌ عن مطرٍ في السنة ٧، لا يمسّ شيئًا ممّا سبق",
            source_name="سجلُّ أخبارِ المجال المفروض",
            scope=_scope(7, 7),
        ),
        Evidence(
            evidence_id="دليل-نقض-الرابط",
            genus=EvidenceGenus.ACCEPTED_REPORT,
            statement=(
                "خبرٌ معتمدٌ معارضٌ يذكر أنّ موضعَ ميلاد الطرفَين مختلف، "
                "فمفتاحُ المعيار الأوّلُ لا يوافق"
            ),
            source_name="سجلُّ تراجمِ المجال المفروض، نسخةٌ ثانية",
            scope=_scope(0, 20),
        ),
    )


def declared_occurrences() -> tuple[Occurrence, ...]:
    """المواضعُ الثلاثةُ المصدريّةُ بمداها ووحدتها؛ قابلةٌ لإعادة الاستخراج."""

    return (
        Occurrence(
            occurrence_id="وقوع-زيد",
            source_path=THE_SOURCE_PATH,
            source_sha256=THE_SOURCE_SEAL,
            offset_unit=OffsetUnit.CODEPOINT,
            start=499020,
            end=499026,
            surface="زَيْدٌ",
        ),
        Occurrence(
            occurrence_id="وقوع-يثرب",
            source_path=THE_SOURCE_PATH,
            source_sha256=THE_SOURCE_SEAL,
            offset_unit=OffsetUnit.CODEPOINT,
            start=494543,
            end=494551,
            surface="يَثْرِبَ",
        ),
        Occurrence(
            occurrence_id="وقوع-المدينة",
            source_path=THE_SOURCE_PATH,
            source_sha256=THE_SOURCE_SEAL,
            offset_unit=OffsetUnit.CODEPOINT,
            start=194912,
            end=194924,
            surface="الْمَدِينَةِ",
        ),
    )


def base_register() -> FactRegister:
    """سجلُّ الوقائع بأدلّته وأفراده؛ والأفرادُ بياناتٌ لا أعضاءُ مفردةٍ مغلقة."""

    register = FactRegister(register_id="سجلّ-شبكة-الهويّة")
    for evidence in declared_evidence():
        register = register.with_evidence(evidence)
    for individual_id, evidence_id, type_id in (
        (FIRST_ZAYD, "دليل-وجود-زيد-الأوّل", PERSON_TYPE_ID),
        (SECOND_ZAYD, "دليل-وجود-زيد-الثاني", PERSON_TYPE_ID),
        (THE_CITY, "دليل-وجود-المدينة", CITY_TYPE_ID),
    ):
        register = register.with_individual(
            Individual(
                individual_id=individual_id,
                designation_method=DesignationMethod.PROPER_NAME,
                candidate_type_ids=(type_id,),
                existence=ExistenceStanding.ASSUMED_FOR_THE_DISCOURSE,
                evidence_ref=register.evidence_of(evidence_id).ref,
            )
        )
    return register


def base_network(register: FactRegister) -> IdentityNetwork:
    """شبكةُ التسميات والمعيار؛ بلا رابطٍ بعدُ، فالرابطُ خطوةٌ تُشتَرى بدليل."""

    network = IdentityNetwork(network_id="شبكة-الهويّة")
    for naming_id, surface, named_id, genus, evidence_id, scope in (
        (
            "تسمية-زيد-الأوّل",
            "زيد",
            FIRST_ZAYD,
            NamingGenus.PROPER_NAME,
            "دليل-تسمية-زيد-الأوّل",
            _scope(),
        ),
        (
            "تسمية-زيد-الثاني",
            "زيد",
            SECOND_ZAYD,
            NamingGenus.PROPER_NAME,
            "دليل-تسمية-زيد-الثاني",
            _scope(),
        ),
        (
            "كنية-زيد-الثاني",
            "أبو أسامة",
            SECOND_ZAYD,
            NamingGenus.BYNAME,
            "دليل-كنية-زيد-الثاني",
            _scope(),
        ),
        (
            "تسمية-يثرب",
            "يَثْرِبَ",
            THE_CITY,
            NamingGenus.FORMER_NAME,
            "دليل-تسمية-يثرب",
            _scope(0, 1),
        ),
        (
            "تسمية-المدينة",
            "الْمَدِينَةِ",
            THE_CITY,
            NamingGenus.TOPONYM,
            "دليل-تسمية-المدينة",
            _scope(1, 9),
        ),
    ):
        network = network.with_naming(
            Naming(
                naming_id=naming_id,
                surface=surface,
                named_id=named_id,
                named_kind=NamedKind.INDIVIDUAL,
                genus=genus,
                language_id="ar",
                scope=scope,
                evidence_ref=register.evidence_of(evidence_id).ref,
            ),
            register,
        )
    return network.with_criterion(
        IdentityCriterion(
            criterion_id=THE_CRITERION,
            key_names=("موضع-الميلاد", "سنة-الميلاد"),
            scope=_scope(0, 20),
            authority="سجلُّ تراجمِ المجال المفروض",
        )
    )


def agreeing_link(register: FactRegister) -> IdentityLink:
    """رابطٌ مفاتيحُه كلُّها موافقة؛ وهو وحدَه ما يُقبَل إيداعُه."""

    return IdentityLink(
        link_id=THE_LINK,
        left_individual_id=FIRST_ZAYD,
        right_individual_id=SECOND_ZAYD,
        criterion_id=THE_CRITERION,
        key_readings=(
            KeyReading(key_name="موضع-الميلاد", left_value="مكّة", right_value="مكّة"),
            KeyReading(key_name="سنة-الميلاد", left_value="-20", right_value="-20"),
        ),
        evidence_ref=register.evidence_of("دليل-رابط-الهويّة").ref,
    )


def contested_readings() -> tuple[KeyReading, ...]:
    """قراءةُ المفاتيح بعد الخبر المعارض: موضعُ الميلاد مختلفٌ فيُنقَض.

    ولا يُودَع رابطٌ بهذه القراءة ابتداءً؛ إنّما يُعاد بها قراءةُ رابطٍ قائم،
    فالتعارضُ حادثٌ في الأدلّة لا حالٌ تُكتَب.
    """

    return (
        KeyReading(key_name="موضع-الميلاد", left_value="مكّة", right_value="الطائف"),
        KeyReading(key_name="سنة-الميلاد", left_value="-20", right_value="-20"),
    )


@dataclass(frozen=True, slots=True)
class IdentityRunOutcome:
    """أثرُ التشغيل الكامل: كلُّ محطّةٍ باسمها ومخرجها، ولا مرحلةَ مطويّة."""

    witnesses: tuple[RepresentationWitness, ...]
    readings: tuple[CanonicalReading, ...]
    zayd_candidates: tuple[NamingCandidate, ...]
    city_names: tuple[str, ...]
    linked_before: tuple[str, ...]
    linked_after_link: tuple[str, ...]
    linked_after_retraction: tuple[str, ...]
    arrival_before_link: str
    arrival_after_link: str
    arrival_after_retraction: str
    arrival_after_independent: str
    suspended_by_policy: tuple[str, ...]
    trace: tuple[str, ...]


def _standing_of(register: FactRegister, proposition_id: str) -> str:
    try:
        item = register.proposition_of(proposition_id)
    except Exception:
        return "غيرُ مودَعة"
    return "معلَّقة" if item.suspended else "مدعومة"


def full_run(root: Path | None = None) -> IdentityRunOutcome:
    """شغِّل المسارَ من المصدر المختوم إلى المراجعة، وأخرِج أثرَه محطّةً محطّة.

    المدخل: جذرُ الشجرة.
    الشرط: البايتاتُ مودَعةٌ بختمها، والتسمياتُ والمعيارُ مودَعة.
    المخرج: الشهاداتُ والقراءاتُ والمرشَّحون ومنازلُ القضيّة في أربعة أزمنة.
    ما تحفظه: لا يُنشَأ فردٌ ولا دليلٌ خارجَ `declared_evidence`.
    """

    tree = Path(__file__).resolve().parents[3] if root is None else root
    occurrences = declared_occurrences()
    witnesses = tuple(witness_occurrence(one, tree) for one in occurrences)
    readings = tuple(
        canonical_reading(one, witness)
        for one, witness in zip(occurrences, witnesses, strict=True)
        if witness.standing.is_reproduced
    )

    register = base_register()
    network = base_network(register)
    candidates = candidates_for_surface("زيد", network, register)
    city_names = tuple(
        sorted(one.surface for one in network.namings_of_individual(THE_CITY))
    )
    linked_before = linked_individual_ids(FIRST_ZAYD, network)

    arrival_evidence = register.evidence_of("دليل-وصول-الأوّل")
    register = register.with_proposition(
        Proposition(
            proposition_id="قضيّة-وصول-الأوّل",
            form=PropositionForm.EVENT_OCCURRED,
            subject_id=FIRST_ZAYD,
            predicate_id="حدث-الوصول",
            value=None,
            polarity=Polarity.AFFIRMED,
            scope=_scope(5, 5),
            evidence_ref=arrival_evidence.ref,
        )
    )
    before = _standing_of(register, "قضيّة-وصول-الثاني")

    network = network.with_link(agreeing_link(register), register)
    linked_after = linked_individual_ids(FIRST_ZAYD, network)
    link_evidence = register.evidence_of("دليل-رابط-الهويّة")
    register = register.with_proposition(
        Proposition(
            proposition_id="قضيّة-وصول-الثاني",
            form=PropositionForm.EVENT_OCCURRED,
            subject_id=SECOND_ZAYD,
            predicate_id="حدث-الوصول",
            value=None,
            polarity=Polarity.AFFIRMED,
            scope=_scope(5, 5),
            evidence_ref=link_evidence.ref,
            derived_from_proposition_ids=("قضيّة-وصول-الأوّل",),
            derived_by_rule="قاعدة-نقل-المحمول-عبر-الهويّة@١",
        )
    )
    after_link = _standing_of(register, "قضيّة-وصول-الثاني")

    register = register.retract("دليل-رابط-الهويّة")
    network = network.retract_link(THE_LINK)
    linked_after_retraction = linked_individual_ids(FIRST_ZAYD, network)
    after_retraction = _standing_of(register, "قضيّة-وصول-الثاني")

    register = register.reinstate(
        "قضيّة-وصول-الثاني", register.evidence_of("دليل-وصول-الثاني-مباشر")
    )
    after_independent = _standing_of(register, "قضيّة-وصول-الثاني")

    contested_network = (
        base_network(register)
        .with_link(agreeing_link(register), register)
        .amend_link_readings(
            THE_LINK,
            contested_readings(),
            register.evidence_of("دليل-نقض-الرابط").ref,
        )
    )
    _, suspended = contested_network.apply_conflict_policy(
        ConflictPolicy.SUSPEND_THE_CONTESTED_LINKS
    )

    trace = (
        f"١ · المصدرُ `{THE_SOURCE_PATH}` بختم `{THE_SOURCE_SEAL[:12]}…`",
        "٢ · ثلاثةُ مواضعَ قُطِعت وقُوبلت: "
        + "، ".join(f"{one.occurrence_id}={one.standing.value}" for one in witnesses),
        "٣ · ١١٦ قرأت: "
        + "، ".join(f"{one.occurrence_id}={one.standing.value}" for one in readings),
        f"٤ · «زيد» رشّح {len(candidates)} فردًا، ولم يُحصَر في واحد",
        f"٥ · المدينةُ تحمل {len(city_names)} تسميةً بمُعرِّفٍ واحد: {THE_CITY}",
        f"٦ · وصولُ الثاني قبل الرابط: {before}",
        f"٧ · بعد الرابط: {after_link} (موحَّدٌ مع {linked_after})",
        f"٨ · بعد سحب الرابط: {after_retraction} (موحَّدٌ مع {linked_after_retraction})",
        f"٩ · بعد الشاهد المستقلّ: {after_independent}",
        f"١٠ · سياسةُ التعارض علّقت: {suspended}",
    )
    return IdentityRunOutcome(
        witnesses=witnesses,
        readings=readings,
        zayd_candidates=candidates,
        city_names=city_names,
        linked_before=linked_before,
        linked_after_link=linked_after,
        linked_after_retraction=linked_after_retraction,
        arrival_before_link=before,
        arrival_after_link=after_link,
        arrival_after_retraction=after_retraction,
        arrival_after_independent=after_independent,
        suspended_by_policy=suspended,
        trace=trace,
    )
