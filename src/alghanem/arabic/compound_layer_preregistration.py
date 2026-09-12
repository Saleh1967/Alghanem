"""تسجيل مسبق لمراحل طبقة المركّب الأربع، قبل مصدرها النصّي لا بعده.

الشهادات الصورية الثلاث القائمة — `word_class_formal.py`، و
`lafz_madlul_relation_formal.py`، و`madlul_alone_formal.py` — تشترك في شرطٍ
واحد لا تنازل فيه: كل فرعٍ في مجالها مسنودٌ بشاهدٍ مُثبَت **منقولٍ بنصّه** من
مصدرٍ مُسمّى بعينه، وكل سؤالٍ في مجالها منقولٌ بلفظه من ذلك المصدر. ولهذا
بالذات أُجّل المركّب: `madlul_alone_formal.py` يُصرّح بأن «أقسام المركّب
(إسنادي وغير إسنادي)... تحتاج شواهد لكل قيمة ليكون المجال مكتمل الفروع
بالبناء، ولا نملكها هنا، وإدخالها الآن ادّعاءُ نطاقٍ غير مبرهَن».

وقد طُلبت أربع مراحل لطبقة المركّب: العامل والمعمول، والنسب الإسنادية،
والتضمين والتقييد، وقيم النسبة الثلاث (الفاعلية والمفعولية والمسببية). والطلب
يُحدّد **مفردات المخرجات** و**الرفوضات المُسمّاة** و**ترتيب التبعية** بين
المراحل؛ ولا يُحدّد — ولا يستطيع أن يُحدّد — نصًّا مصدريًّا ليس في هذا
المستودع. فما يمكن بناؤه اليوم بناءٌ صادق هو هذا التسجيل المسبق، لا شهادة:

    Preregistration != Certificate

والفارق بنيويّ لا لفظيّ. الشهادة تحمل `بُرهانًا شاملًا` على مجالٍ مُجمَّد
وتنتهي إلى عنوانٍ دقيق هو "شهادة صورية شاملة ناجحة على نطاق محدود". وهذا
التسجيل لا يحمل دالّة قرار، ولا مجالًا مقبولًا، ولا شاهدًا واحدًا، ولا حقل
نتيجة البتّة — وحارسٌ عند الاستيراد يمنع تسلّل حقلٍ كهذا لاحقًا. وكلّ ما يفعله
أنه **يُجمّد المطلوب قبل دليله**، على نفس منطق `probe_preregistration.py`: من
كتب مفردةً بعد رؤية شواهده، أو وسّع مفردةً مُسجَّلة، أو أسقط رفضًا مُسمّى، أو
قدّم مرحلةً على شرطها — فشل عنده الإنشاء، لا صدر عنه تحذيرٌ يُقرأ أو يُهمَل.

`موقف الإسناد` مفردةٌ ثلاثية، وقيمتها الثالثة `شاهد_لكل_فرع` **مُعلَنة غير
قابلة للبناء** اليوم، بنفس انضباط `MeasurementProgress.CLOSED_BY_...` في
`readiness_rank.py` و`EvidenceGenus.MORPHO_FUNCTIONAL` في
`probe_preregistration.py`: لا سلطة في هذا المستودع تتحقّق من أن نصًّا مصدريًّا
يُثبِت فرعًا، فإصدارُ تلك القيمة هنا ادّعاءُ تحقّقٍ لم يجرِ. وهي مذكورة في
المفردة لا محذوفة منها، لأن حذفها يجعل الغاية التي تُقصَد غيرَ مُسمّاة أصلًا.
وترتيب الرفض مقصود: تُرَدّ `شاهد_لكل_فرع` برسالتها الخاصّة **قبل** الرسالة
العامّة، حتى لا يُقرأ رفضٌ سببه «لا سلطة تُصدرها» على أنه الأسهل: «لم يُقدَّم
المصدر بعد».

وترتيب التبعية **مُشتَقّ لا مكتوب**: المرحلة الثالثة تقرأ مخرجات الأولى،
والرابعة تقرأ مخرجات الثانية، وهذا هو ما يمنع الشهادتين من التناقض صامتتين.
فمن كتب شرطًا يخالف المُشتَقّ رُدَّ عند الإنشاء، ولا يوجد حقلٌ تُكتَب فيه
التبعية ابتداءً.

نطاق الوحدة وحدودها — تسجيل صريح، لا اعتذار لاحق:

* هذه الوحدة **ليست** المرحلة الأولى ولا جزءًا منها. لا مجال صوريّ هنا، ولا
  دالّة قرار، ولا حوامل، ولا شواهد، ولا برهان. من قرأها شهادةً فقد قرأ ما ليس
  فيها، ولذلك لا تحمل عنوان النجاح ولا أيّ عنوانٍ غيره.
* المفردات المُسجَّلة هنا **مطلوبة لا مُثبَتة**:
  `RequestedVocabularyIsNotAttestedVocabulary`. كونُ «عامل» و«معمول» مفردةً
  مطلوبةً لا يُثبت أنها مفردةُ المصدر ولا أنها مكتملة الفروع؛ وذلك بعينه ما
  ينتظر النصّ.
* سلطويًّا: `FormalClassification != BirthVerdict`، و
  `Preregistration != Certificate`، و`DeclaredStage != BornOntology`. لا نوع في
  `kernel/`، ولا `Freeze`، ولا `E0`، ولا بوّابة نواة تقرأ هذه المخرجات، ولا
  تدخل في `BirthExperimentSpecification`، ولا تغيّر نتيجة التدقيق الخارجي.
* والتأجيلان المُسجَّلان في `madlul_alone_formal.py` و
  `lafz_madlul_relation_formal.py` يبقيان قائمين بنصّهما: هذه الوحدة لا تُقسّم
  المركّب ولا تُصنّف علاقةً سببية، فتعديل نصّهما الآن يوحي بسدادِ دَينٍ لم
  يُسَدَّد.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .text_key import comparison_key


class CompoundLayerPreregistrationError(ValueError):
    """رُفض مدخلٌ خارج التسجيل المُجمَّد؛ لا يُحمَل على أقرب حالة."""


class CompoundStage(Enum):
    """مراحل طبقة المركّب الأربع المغلقة، بترتيب الطلب؛ لا خامسة لها هنا."""

    AMIL_MAMUL = "العامل_والمعمول"
    NISBA_ISNADIYYA = "النسب_الإسنادية"
    TADMIN_TAQYID = "التضمين_والتقييد"
    NISBA_ROLE = "قيم_النسبة"


class AttestationStanding(Enum):
    """موقف الإسناد النصّي؛ ثالثتها مُعلَنة غير قابلة للبناء اليوم."""

    SOURCE_NOT_SUPPLIED = "مصدر_غير_مُقدَّم"
    SOURCE_SUPPLIED_NOT_VERIFIED = "مصدر_مُقدَّم_غير_متحقَّق"
    ATTESTED_PER_BRANCH = "شاهد_لكل_فرع"


COMPOUND_UNDECIDED_TEXT: Final = "لا_ينطبق"

COMPOUND_SUCCESS_TITLE_IS_WITHHELD: Final = (
    "لا عنوان نجاح لهذه الوحدة: التسجيل المسبق ليس شهادة، ولا يصير شهادةً إلا "
    "بمجالٍ مُجمَّد ودالّة قرارٍ كلّية وشاهدٍ مُثبَت لكل فرع"
)

COMPOUND_SOURCE_REQUIREMENT: Final = (
    "لكل مرحلة يلزم: نصٌّ مصدريّ مُسمّى بعينه، وأسئلة المجال منقولةً بلفظها "
    "منه، وشاهدٌ واحدٌ مُثبَتٌ بنصّه لكل فرعٍ من فروع مفردتها، وحاملُ بياناتٍ "
    "مغلقٌ تُشتَقّ منه كل إجابة"
)

COMPOUND_SCOPE_NOTE: Final = (
    "هذه الوحدة تُجمّد المطلوب قبل دليله ولا تُنجزه: لا مجال صوريّ فيها، ولا "
    "دالّة قرار، ولا حوامل، ولا شواهد، ولا برهان"
)

COMPOUND_AUTHORITY_NOTE: Final = (
    "Preregistration != Certificate، و FormalClassification != BirthVerdict، و "
    "DeclaredStage != BornOntology: لا نوع في kernel، ولا Freeze، ولا E0، ولا "
    "بوّابة نواة تقرأ هذه المخرجات"
)

COMPOUND_REQUESTED_NOT_ATTESTED_NOTE: Final = (
    "RequestedVocabularyIsNotAttestedVocabulary: المفردات المُسجَّلة هنا "
    "مطلوبةٌ في نصّ الطلب، ولا يُثبِت ورودها فيه أنها مفردةُ المصدر ولا أنها "
    "مكتملة الفروع"
)

_ATTESTED_PER_BRANCH_REFUSAL: Final = (
    "لا سلطة في هذا المستودع تتحقّق من إسناد فرعٍ إلى نصّه، فقيمة "
    "`شاهد_لكل_فرع` مُعلَنة غير قابلة للبناء؛ وهي مذكورة في المفردة لا محذوفة "
    "منها لئلّا تصير الغاية المقصودة غيرَ مُسمّاة"
)

_SOURCE_MISSING_REFUSAL: Final = (
    "لم يُقدَّم لهذه المرحلة نصٌّ مصدريّ في هذا المستودع، فالموقف الوحيد "
    "القابل للبناء اليوم هو `مصدر_غير_مُقدَّم`"
)

_DERIVED_PREREQUISITES: Final[dict[CompoundStage, tuple[CompoundStage, ...]]] = {
    CompoundStage.AMIL_MAMUL: (),
    CompoundStage.NISBA_ISNADIYYA: (),
    CompoundStage.TADMIN_TAQYID: (CompoundStage.AMIL_MAMUL,),
    CompoundStage.NISBA_ROLE: (CompoundStage.NISBA_ISNADIYYA,),
}

_FORBIDDEN_FIELD_TOKENS: Final = (
    "result",
    "outcome_value",
    "verdict",
    "birth",
    "certificate",
    "classification",
    "proof",
)


def derived_prerequisites(stage: CompoundStage) -> tuple[CompoundStage, ...]:
    """شروط المرحلة السابقة عليها، مُشتَقّةً لا مكتوبةً في أي حقل."""
    return _DERIVED_PREREQUISITES[stage]


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CompoundLayerPreregistrationError(
            f"{field_name} يجب أن يكون نصًّا غير فارغ؛ ولا يُقبَل فيه الفراغ صمتًا."
        )
    return value


@dataclass(frozen=True, slots=True)
class NamedRefusal:
    """رفضٌ مُسمّى بنصّه؛ الاسم وحده بلا بيانٍ لا يمنع شيئًا."""

    name: str
    statement: str

    def __post_init__(self) -> None:
        _require_text(self.name, "اسم الرفض")
        _require_text(self.statement, "بيان الرفض")


@dataclass(frozen=True, slots=True)
class CompoundStageRegistration:
    """تسجيل مرحلةٍ واحدة قبل مصدرها؛ لا حقل نتيجة فيه البتّة."""

    stage: CompoundStage
    declared_outcomes: tuple[str, ...]
    undecided_outcome: str
    refusals: tuple[NamedRefusal, ...]
    prerequisites: tuple[CompoundStage, ...]
    attestation: AttestationStanding
    missing_source_note: str

    def __post_init__(self) -> None:
        if not isinstance(self.stage, CompoundStage):
            raise CompoundLayerPreregistrationError(
                "المرحلة يجب أن تكون عضوًا في مفردة المراحل المغلقة."
            )
        if not isinstance(self.attestation, AttestationStanding):
            raise CompoundLayerPreregistrationError(
                "موقف الإسناد يجب أن يكون عضوًا في مفردته المغلقة."
            )
        if self.attestation is AttestationStanding.ATTESTED_PER_BRANCH:
            raise CompoundLayerPreregistrationError(_ATTESTED_PER_BRANCH_REFUSAL)
        if self.attestation is not AttestationStanding.SOURCE_NOT_SUPPLIED:
            raise CompoundLayerPreregistrationError(_SOURCE_MISSING_REFUSAL)

        _require_text(self.missing_source_note, "بيان غياب المصدر")
        _require_text(self.undecided_outcome, "قيمة عدم الانطباق")

        if len(self.declared_outcomes) < 2:
            raise CompoundLayerPreregistrationError(
                "مفردة المخرجات يجب أن تحمل قيمتين فأكثر، وإلّا فلا تقسيم فيها."
            )
        seen: set[str] = set()
        for value in self.declared_outcomes:
            _require_text(value, "قيمة في مفردة المخرجات")
            key = comparison_key(value)
            if key in seen:
                raise CompoundLayerPreregistrationError(
                    f"قيمةٌ مكرّرة في مفردة مخرجات {self.stage.value}: {value}؛ "
                    "والتكرار يُخفي قيمةً تحت أخرى."
                )
            seen.add(key)
        if comparison_key(self.undecided_outcome) not in seen:
            raise CompoundLayerPreregistrationError(
                f"قيمة عدم الانطباق لمرحلة {self.stage.value} ليست عضوًا في "
                "مفردتها؛ وعدم الانطباق تصريحٌ في المفردة لا ثغرةٌ خارجها."
            )

        if not self.refusals:
            raise CompoundLayerPreregistrationError(
                f"مرحلة {self.stage.value} بلا رفضٍ مُسمّى واحد؛ وحدودُ المرحلة "
                "تُسمّى ولا تُترَك للقارئ."
            )
        refusal_names: set[str] = set()
        for refusal in self.refusals:
            if not isinstance(refusal, NamedRefusal):
                raise CompoundLayerPreregistrationError(
                    "كل رفضٍ يجب أن يكون `NamedRefusal` باسمه وبيانه."
                )
            if refusal.name in refusal_names:
                raise CompoundLayerPreregistrationError(
                    f"رفضٌ مكرّر في مرحلة {self.stage.value}: {refusal.name}."
                )
            refusal_names.add(refusal.name)

        derived = derived_prerequisites(self.stage)
        if tuple(self.prerequisites) != derived:
            raise CompoundLayerPreregistrationError(
                f"شروط مرحلة {self.stage.value} مكتوبةٌ على خلاف المُشتَقّ؛ "
                "والتبعية تُشتَقّ من قراءة مرحلةٍ لمخرجات أخرى، ولا تُكتَب."
            )


@dataclass(frozen=True, slots=True)
class CompoundLayerPreregistration:
    """التسجيل المسبق لطبقة المركّب كلّها؛ تغطيةٌ قبل حكم، وترتيبٌ قبل قراءة."""

    registrations: tuple[CompoundStageRegistration, ...]

    def __post_init__(self) -> None:
        seen: list[CompoundStage] = []
        for registration in self.registrations:
            if not isinstance(registration, CompoundStageRegistration):
                raise CompoundLayerPreregistrationError(
                    "كل عنصرٍ يجب أن يكون `CompoundStageRegistration`."
                )
            if registration.stage in seen:
                raise CompoundLayerPreregistrationError(
                    f"مرحلةٌ مكرّرة في التسجيل: {registration.stage.value}؛ "
                    "والتكرار يُخفي تسجيلًا تحت آخر."
                )
            for prerequisite in registration.prerequisites:
                if prerequisite not in seen:
                    raise CompoundLayerPreregistrationError(
                        f"مرحلة {registration.stage.value} سبقت شرطها "
                        f"{prerequisite.value}؛ وتقديم المرحلة على شرطها يجعل "
                        "قراءتها لمخرجاته قراءةً لما لم يُسجَّل بعد."
                    )
            seen.append(registration.stage)

        missing = tuple(stage for stage in CompoundStage if stage not in seen)
        if missing:
            raise CompoundLayerPreregistrationError(
                "مرحلةٌ مفقودة من التسجيل: "
                + "، ".join(stage.value for stage in missing)
                + "؛ والتغطية تسبق الحكم، ومرحلةٌ لم تُسجَّل ليست مرحلةً بلا حدود."
            )

    @property
    def stages(self) -> tuple[CompoundStage, ...]:
        """المراحل بترتيب تسجيلها، مُشتَقّةً من التسجيلات نفسها."""
        return tuple(registration.stage for registration in self.registrations)

    @property
    def certificate_is_constructible(self) -> bool:
        """`False` على كل فرع: لا شهادة بلا نصٍّ مصدريّ وشاهدٍ لكل فرع."""
        return False

    def registration_for(self, stage: CompoundStage) -> CompoundStageRegistration:
        """تسجيل مرحلةٍ بعينها؛ والمرحلة المسجَّلة موجودةٌ بحكم التغطية."""
        for registration in self.registrations:
            if registration.stage is stage:
                return registration
        raise CompoundLayerPreregistrationError(f"لا تسجيل للمرحلة {stage.value}.")


_AMIL_MAMUL: Final = CompoundStageRegistration(
    stage=CompoundStage.AMIL_MAMUL,
    declared_outcomes=("عامل", "معمول", COMPOUND_UNDECIDED_TEXT),
    undecided_outcome=COMPOUND_UNDECIDED_TEXT,
    refusals=(
        NamedRefusal(
            name="GovernanceRelationIsNotBornOntology",
            statement=(
                "علاقة العمل المُصنَّفة وصفٌ لتركيبٍ مُختبَر، لا كائنٌ مولودٌ في "
                "أنطولوجيا؛ ولا يقرؤها `FractalSnapshot` ولا غيره"
            ),
        ),
        NamedRefusal(
            name="DeclaredAmil != BornOperator",
            statement=(
                "كون اللفظ مُصنَّفًا «عاملًا» لا يجعله `Operation` في النواة ولا "
                "عاملًا مولودًا له مجال مصدرٍ مُرخَّص"
            ),
        ),
        NamedRefusal(
            name="FormalClassification != BirthVerdict",
            statement=(
                "التصنيف الصوري ليس حكم ولادة: لا `Freeze`، ولا `E0`، ولا "
                "بوّابة نواة تقرؤه"
            ),
        ),
        NamedRefusal(
            name="SurfaceEffectIsNotSemanticRole",
            statement=(
                "كون لفظٍ عاملًا في آخر لا يقول شيئًا عن فاعليته ولا مفعوليته؛ "
                "تلك مرحلةٌ رابعةٌ لها مفردتها وشواهدها"
            ),
        ),
    ),
    prerequisites=(),
    attestation=AttestationStanding.SOURCE_NOT_SUPPLIED,
    missing_source_note=(
        "لم يُقدَّم نصٌّ يُثبِت أسئلة العمل ولا حوامله (حامل الاقتضاء، وحامل "
        "الأثر، وحامل الموقع)، ولا شاهدٌ واحدٌ لكلٍّ من الفروع الثلاثة"
    ),
)

_NISBA_ISNADIYYA: Final = CompoundStageRegistration(
    stage=CompoundStage.NISBA_ISNADIYYA,
    declared_outcomes=("مركّب_إسنادي", "مركّب_غير_إسنادي", COMPOUND_UNDECIDED_TEXT),
    undecided_outcome=COMPOUND_UNDECIDED_TEXT,
    refusals=(
        NamedRefusal(
            name="IsnadiyyaIsNotTruth",
            statement=(
                "تصنيف النسبة إسناديةً تصنيفُ بنيةٍ لا تصديقٌ بمضمونها؛ فلا "
                "تُقرَأ نسبةٌ مُصنَّفة `ClaimCore` ولا دعوى مُثبَتة"
            ),
        ),
        NamedRefusal(
            name="DeclaredNisba != BornRelation",
            statement=(
                "النسبة المُعلَنة وصفٌ لتركيبٍ مُختبَر، لا علاقةٌ مولودةٌ في "
                "رسم العلاقات المشتقّة"
            ),
        ),
    ),
    prerequisites=(),
    attestation=AttestationStanding.SOURCE_NOT_SUPPLIED,
    missing_source_note=(
        "لم يُقدَّم نصٌّ يُثبِت قسمة المركّب إسناديًّا وغير إسنادي بلفظه، ولا "
        "شاهدٌ واحدٌ لكلٍّ من الفروع؛ وهو عين ما أجّله `madlul_alone_formal.py`"
    ),
)

_TADMIN_TAQYID: Final = CompoundStageRegistration(
    stage=CompoundStage.TADMIN_TAQYID,
    declared_outcomes=("تضمين", "تقييد", COMPOUND_UNDECIDED_TEXT),
    undecided_outcome=COMPOUND_UNDECIDED_TEXT,
    refusals=(
        NamedRefusal(
            name="TadminIsNotLogicalEntailment",
            statement=(
                "التضمين هنا دخولُ معنى المعمول في معنى العامل، وليس الاستلزام "
                "المنطقي `⊨`؛ وهذا أقرب سوء قراءةٍ لهذه المرحلة"
            ),
        ),
        NamedRefusal(
            name="TaqyidIsNotQuantification",
            statement=(
                "التقييد تضييقُ سعةِ معنًى تامّ، لا تسويرٌ ولا كمٌّ منطقيّ على " "متغيّر"
            ),
        ),
        NamedRefusal(
            name="DeclaredMode != BornOntology",
            statement=(
                "جهةُ تأثير المعمول مُعلَنةٌ موصوفة، لا كائنٌ مولود؛ ولا يقرؤها " "أيُّ بوّابة"
            ),
        ),
    ),
    prerequisites=(CompoundStage.AMIL_MAMUL,),
    attestation=AttestationStanding.SOURCE_NOT_SUPPLIED,
    missing_source_note=(
        "لم يُقدَّم نصٌّ يُثبِت الفرق بين التضمين والتقييد بلفظه، ولا حوامله "
        "(حامل دخول المعنى، وحامل موضع التقييد)، ولا شاهدٌ لكل فرع"
    ),
)

_NISBA_ROLE: Final = CompoundStageRegistration(
    stage=CompoundStage.NISBA_ROLE,
    declared_outcomes=("فاعلية", "مفعولية", "مسببية", COMPOUND_UNDECIDED_TEXT),
    undecided_outcome=COMPOUND_UNDECIDED_TEXT,
    refusals=(
        NamedRefusal(
            name="MusabbibiyyaIsNotCausation",
            statement=(
                "المسببية قيمةُ نسبةٍ مُعلَنة في تركيبٍ مُختبَر، لا واقعةُ "
                "سببيّةٍ مُثبَتة في العالم: لا دليل، ولا بقيّة، ولا بوّابة"
            ),
        ),
        NamedRefusal(
            name="RoleIsNotAgencyOfAnAgent",
            statement=(
                "الفاعلية قيمةُ موضعٍ في النسبة، ولا تُثبِت أن مرجع اللفظ فاعلٌ "
                "مختارٌ في الخارج"
            ),
        ),
        NamedRefusal(
            name="SemanticRoleIsNotSurfaceGovernance",
            statement=(
                "قيمة النسبة لا تُشتَقّ من العمل النحوي ولا تُشتَقّ منه؛ وهو "
                "عكسُ رفضِ المرحلة الأولى لا تكرارٌ له"
            ),
        ),
    ),
    prerequisites=(CompoundStage.NISBA_ISNADIYYA,),
    attestation=AttestationStanding.SOURCE_NOT_SUPPLIED,
    missing_source_note=(
        "لم يُقدَّم نصٌّ يُثبِت حصر قيم النسبة في الثلاث، ولا حامل جهة النسبة "
        "الذي يفرّق المسببية من الفاعلية، ولا شاهدٌ لكل قيمة"
    ),
)


COMPOUND_LAYER_PREREGISTRATION: Final = CompoundLayerPreregistration(
    registrations=(_AMIL_MAMUL, _NISBA_ISNADIYYA, _TADMIN_TAQYID, _NISBA_ROLE)
)


def _assert_no_result_field() -> None:
    """حارس استيراد: لا حقل نتيجةٍ يتسلّل إلى تسجيلٍ مسبق لاحقًا."""
    for dataclass_type in (
        NamedRefusal,
        CompoundStageRegistration,
        CompoundLayerPreregistration,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise CompoundLayerPreregistrationError(
                        f"حقلٌ يحمل نتيجة تسلّل إلى {dataclass_type.__name__}: "
                        f"{declared.name}؛ والتسجيل المسبق لا نتيجة فيه."
                    )


_assert_no_result_field()
