"""سجلّ دعاوى التقارب: تسجيلُ الدعوى وموقفها، لا إصدارُ حكم تقارب.

`ConvergenceClaimRegister != ConvergenceAuthority`. لا توجد في هذا المستودع —
اليوم — أيّ آلةٍ تُشغَّل فتقيس تقارب تصنيفين ولا تُصدر حكمًا به: لا نوع في
`kernel/`، ولا بوّابة، ولا دالّة قياس. فكلّ ما تفعله هذه الوحدة أن تُسجِّل دعوى
تقاربٍ **طُرحت** ثم فُحصت فحصًا مباشرًا في المستودع نفسه، وتُثبِّت موقفها بعبارةٍ
مغلقة ومُسبَّبة. ولو صار في المستودع يومًا قياسُ تقاربٍ فعليّ، فهذه الوحدة لا
تُغني عنه ولا تُقدَّم دليلًا بين يديه.

ولهذا التمييز أثرٌ واجب التصريح: أن يُقال عن دعوى إنها "تستوفي معيار تقارب" ليس
اختبارًا جرى، ما لم يكن الاختبار مبنيًّا في شيفرةٍ تُشغَّل. والقول بغير ذلك يُقدِّم
تقديرًا شخصيًّا في صورة فحصٍ آليّ، وهو بعينه ما تمنعه
`NamedCriterionIsNotABuiltGate` المسجَّلة هنا بنصّها.

الدعويان المُسجَّلتان اليوم، وموقف كلٍّ منهما:

* **دعوى تقارب الأسماء الشرعية** — أن تصنيف الأسماء الشرعية إلى «متباينة
  ومترادفة ومشتركة ومشكِّكة ومتواطئة» تطبيقٌ ثانٍ مستقلّ لتصنيفٍ واحد على مادّة
  مختلفة، فيكون تقاربًا مضمونيًّا لا تشابهًا شكليًّا. وموقفها
  `مرفوضة_بفحصٍ_مباشر`: القائمة تجمع **ثلاثة فروع** من تصنيف اللفظ باعتبار
  الدالّ والمدلول (`lafz_madlul_relation_formal.py`: متباين، مترادف، مشترك)
  **مع مخرَجَين** من محور التواطؤ والتشكيك تحت الكلّي
  (`kulli_juzi_formal.py`: متواطئ، مشكِّك). فهي دمجُ تصنيفين مستقلّين في قائمة
  واحدة، لا إعادةُ إصدارِ تصنيفٍ واحدٍ على حالة اختبارٍ أخرى. والرفض هنا **باتٌّ
  للدعوى بصيغتها**، لا تعليقٌ في انتظار شهادةٍ لاحقة: فالعيب في بنية الدعوى
  نفسها، ولا يرفعه أيُّ دليلٍ يُضاف بعدُ إلى أيٍّ من التصنيفين.
* **دعوى المتوسطة** — أن في المصدر قسمًا مُسمّى «المتوسطة». وموقفها
  `مصدر_مُسمّى_غائب`: لم يرد هذا المصطلح في أيّ نصٍّ قُدِّم إلى هذا المستودع،
  ولا يجوز إحلال مرادفٍ محلّه ولا افتراض وروده تحت اسمٍ آخر بلا تصريح. والغياب
  هنا **مُسمّى لا مسكوتٌ عنه**، على انضباط `مصدر_غير_مُقدَّم` في
  `compound_layer_preregistration.py` نفسه.

وقيمة `مقبولة_بسلطة_تقارب` مُعلَنة في المفردة **غير قابلة للبناء اليوم**، بنفس
انضباط `شاهد_لكل_فرع` في التسجيل المسبق للمركّب: إصدارُها ادّعاءُ فحصٍ لم يجرِ،
لأن السلطة التي تُصدره غير موجودة أصلًا. وهي مذكورةٌ في المفردة لا محذوفةٌ منها
لئلّا تصير الغاية المقصودة غيرَ مُسمّاة.

حدود الوحدة — تسجيل صريح لا اعتذار لاحق: لا نوع هنا يحمل حقل نتيجة أو حكم أو
ولادة أو شهادة أو برهان (يُفحَص ذلك عند الاستيراد على حقول المفردات نفسها)، ولا
تستورد هذه الوحدة شيئًا من `kernel/`، ولا تُغيّر حقلًا واحدًا في التدقيق
الخارجي، ولا عنوان نجاح لها البتّة.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .text_key import comparison_key


class ConvergenceClaimRegisterError(ValueError):
    """رُفض مدخلٌ خارج السجلّ المُجمَّد؛ لا يُحمَل على أقرب حالة."""


class ConvergenceClaim(Enum):
    """الدعاوى المُسجَّلة المغلقة؛ لا ثالثة لها اليوم."""

    SHARI_NAMES_CONVERGENCE = "تقارب_تصنيف_الأسماء_الشرعية"
    MUTAWASSITA_SECTION = "قسم_المتوسطة"


class ClaimStanding(Enum):
    """موقف الدعوى؛ ثالثتها مُعلَنة غير قابلة للبناء اليوم."""

    REFUTED_BY_DIRECT_INSPECTION = "مرفوضة_بفحصٍ_مباشر"
    NAMED_SOURCE_ABSENT = "مصدر_مُسمّى_غائب"
    UPHELD_BY_CONVERGENCE_AUTHORITY = "مقبولة_بسلطة_تقارب"


CONVERGENCE_NOT_APPLICABLE_TEXT: Final = "لا_ينطبق"

CONVERGENCE_SUCCESS_TITLE_IS_WITHHELD: Final = (
    "لا عنوان نجاح لهذه الوحدة: تسجيلُ دعوى وموقفِها ليس حكم تقارب، ولا يصير "
    "حكمًا إلا بسلطة قياسٍ مبنيّةٍ تُشغَّل وتُصدر نتيجتها"
)

NO_CONVERGENCE_AUTHORITY_NOTE: Final = (
    "لا آلة تقاربٍ في هذا المستودع: لا نوع في kernel، ولا بوّابة، ولا دالّة "
    "قياس. فموقفُ الدعوى هنا محضرُ فحصٍ مباشر مُسبَّب، لا نتيجةَ اختبارٍ جرى"
)

CONVERGENCE_AUTHORITY_NOTE: Final = (
    "ClaimRegister != ConvergenceVerdict، و FormalClassification != "
    "BirthVerdict: لا نوع في kernel، ولا Freeze، ولا E0، ولا بوّابة نواة تقرأ "
    "هذه المخرجات"
)

CONVERGENCE_SCOPE_NOTE: Final = (
    "هذه الوحدة تُسجّل دعويين بعينهما وموقفَ كلٍّ منهما، ولا تُعمّم: ما لم يُسجَّل "
    "فيها فلا موقف له هنا، لا قبولًا ولا ردًّا"
)

_UPHELD_REFUSAL: Final = (
    "لا سلطة تقاربٍ في هذا المستودع تُصدر قبولًا، فقيمة `مقبولة_بسلطة_تقارب` "
    "مُعلَنة غير قابلة للبناء؛ وهي مذكورة في المفردة لا محذوفة منها لئلّا تصير "
    "الغاية المقصودة غيرَ مُسمّاة"
)

_FORBIDDEN_FIELD_TOKENS: Final = (
    "result",
    "outcome_value",
    "verdict",
    "birth",
    "certificate",
    "proof",
    "score",
)


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConvergenceClaimRegisterError(
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
class MergedClassification:
    """تصنيفٌ مستقلّ دُمج في الدعوى، باسم وحدته وبالفروع المأخوذة منه."""

    module: str
    classification: str
    borrowed_values: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.module, "اسم الوحدة")
        _require_text(self.classification, "اسم التصنيف")
        if len(self.borrowed_values) < 1:
            raise ConvergenceClaimRegisterError(
                "التصنيف المدموج يلزمه فرعٌ مأخوذٌ منه على الأقل، وإلّا فلا دمج."
            )
        seen: set[str] = set()
        for value in self.borrowed_values:
            _require_text(value, "فرعٌ مأخوذ")
            key = comparison_key(value)
            if key in seen:
                raise ConvergenceClaimRegisterError(
                    f"فرعٌ مكرّر في {self.classification}: {value}؛ والتكرار "
                    "يُخفي فرعًا تحت آخر."
                )
            seen.add(key)


@dataclass(frozen=True, slots=True)
class ConvergenceClaimRecord:
    """تسجيل دعوى واحدة وموقفها؛ لا حقل نتيجة ولا حكم فيه البتّة."""

    claim: ConvergenceClaim
    statement: str
    standing: ClaimStanding
    ground: str
    merged_classifications: tuple[MergedClassification, ...]
    absent_term: str
    refusals: tuple[NamedRefusal, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.claim, ConvergenceClaim):
            raise ConvergenceClaimRegisterError(
                "الدعوى يجب أن تكون عضوًا في مفردة الدعاوى المغلقة."
            )
        if not isinstance(self.standing, ClaimStanding):
            raise ConvergenceClaimRegisterError(
                "الموقف يجب أن يكون عضوًا في مفردته المغلقة."
            )
        if self.standing is ClaimStanding.UPHELD_BY_CONVERGENCE_AUTHORITY:
            raise ConvergenceClaimRegisterError(_UPHELD_REFUSAL)
        _require_text(self.statement, "نصّ الدعوى")
        _require_text(self.ground, "بيان الموقف")
        _require_text(self.absent_term, "المصطلح الغائب")

        if not self.refusals:
            raise ConvergenceClaimRegisterError(
                f"دعوى {self.claim.value} بلا رفضٍ مُسمّى واحد؛ وحدودُ الموقف "
                "تُسمّى ولا تُترَك للقارئ."
            )
        refusal_names: set[str] = set()
        for refusal in self.refusals:
            if not isinstance(refusal, NamedRefusal):
                raise ConvergenceClaimRegisterError(
                    "كل رفضٍ يجب أن يكون `NamedRefusal` باسمه وبيانه."
                )
            if refusal.name in refusal_names:
                raise ConvergenceClaimRegisterError(
                    f"رفضٌ مكرّر في دعوى {self.claim.value}: {refusal.name}."
                )
            refusal_names.add(refusal.name)

        not_applicable = comparison_key(CONVERGENCE_NOT_APPLICABLE_TEXT)
        refuted = self.standing is ClaimStanding.REFUTED_BY_DIRECT_INSPECTION
        absent = self.standing is ClaimStanding.NAMED_SOURCE_ABSENT

        if refuted:
            modules = {
                comparison_key(merged.module) for merged in self.merged_classifications
            }
            if len(self.merged_classifications) < 2 or len(modules) < 2:
                raise ConvergenceClaimRegisterError(
                    "الرفض بالدمج يلزمه تسميةُ تصنيفين مستقلّين فأكثر بوحدتيهما؛ "
                    "ودعوى الدمج بلا مدموجَين مُسمّيَين دعوى بلا بيان."
                )
            if comparison_key(self.absent_term) != not_applicable:
                raise ConvergenceClaimRegisterError(
                    "المصطلح الغائب يُصرَّح على دعوى الغياب وحدها، وعلى ما عداها "
                    f"يكون {CONVERGENCE_NOT_APPLICABLE_TEXT}."
                )
        if absent:
            if self.merged_classifications:
                raise ConvergenceClaimRegisterError(
                    "دعوى الغياب لا تُدمَج فيها تصنيفات: لا مادّة تُفحَص أصلًا."
                )
            if comparison_key(self.absent_term) == not_applicable:
                raise ConvergenceClaimRegisterError(
                    "دعوى الغياب يلزمها تسميةُ المصطلح الغائب بعينه؛ والغياب "
                    "يُسمّى ولا يُسكَت عنه."
                )
        for merged in self.merged_classifications:
            if not isinstance(merged, MergedClassification):
                raise ConvergenceClaimRegisterError(
                    "كل تصنيفٍ مدموج يجب أن يكون `MergedClassification`."
                )

    @property
    def is_refuted_as_stated(self) -> bool:
        """هل رُدّت الدعوى بصيغتها ردًّا باتًّا لا تعليقًا؟"""

        return self.standing is ClaimStanding.REFUTED_BY_DIRECT_INSPECTION

    @property
    def claim_is_operative(self) -> bool:
        """`False` على كل دعوى: لا دالّة في المستودع تقرأ هذا السجلّ."""

        return False


@dataclass(frozen=True, slots=True)
class ConvergenceClaimRegister:
    """السجلّ كلّه؛ تغطيةٌ قبل حكم: دعوى مفقودة ليست دعوى بلا موقف."""

    records: tuple[ConvergenceClaimRecord, ...]

    def __post_init__(self) -> None:
        seen: list[ConvergenceClaim] = []
        for record in self.records:
            if not isinstance(record, ConvergenceClaimRecord):
                raise ConvergenceClaimRegisterError(
                    "كل عنصرٍ يجب أن يكون `ConvergenceClaimRecord`."
                )
            if record.claim in seen:
                raise ConvergenceClaimRegisterError(
                    f"دعوى مكرّرة في السجلّ: {record.claim.value}؛ والتكرار "
                    "يُخفي موقفًا تحت آخر."
                )
            seen.append(record.claim)
        missing = tuple(claim for claim in ConvergenceClaim if claim not in seen)
        if missing:
            raise ConvergenceClaimRegisterError(
                "دعوى مفقودة من السجلّ: "
                + "، ".join(claim.value for claim in missing)
                + "؛ والتغطية تسبق الحكم، ودعوى لم تُسجَّل ليست دعوى بلا موقف."
            )

    @property
    def claims(self) -> tuple[ConvergenceClaim, ...]:
        """الدعاوى بترتيب تسجيلها، مُشتَقّةً من السجلّات نفسها."""

        return tuple(record.claim for record in self.records)

    @property
    def convergence_verdict_is_constructible(self) -> bool:
        """`False` دائمًا: لا سلطة تقاربٍ في هذا المستودع تُصدر حكمًا."""

        return False

    def record_for(self, claim: ConvergenceClaim) -> ConvergenceClaimRecord:
        """تسجيل دعوى بعينها؛ والدعوى المسجَّلة موجودةٌ بحكم التغطية."""

        if not isinstance(claim, ConvergenceClaim):
            raise ConvergenceClaimRegisterError(
                "الدعوى يجب أن تكون عضوًا في مفردة الدعاوى المغلقة."
            )
        for record in self.records:
            if record.claim is claim:
                return record
        raise ConvergenceClaimRegisterError(f"لا تسجيل للدعوى {claim.value}.")


_SHARI_NAMES: Final = ConvergenceClaimRecord(
    claim=ConvergenceClaim.SHARI_NAMES_CONVERGENCE,
    statement=(
        "تصنيف الأسماء الشرعية إلى متباينة ومترادفة ومشتركة ومشكِّكة ومتواطئة "
        "تطبيقٌ ثانٍ مستقلّ لتصنيفٍ واحد على مادّة مختلفة، فهو تقاربٌ مضمونيّ لا "
        "تشابهٌ شكليّ"
    ),
    standing=ClaimStanding.REFUTED_BY_DIRECT_INSPECTION,
    ground=(
        "القائمة تجمع ثلاثة فروع من تصنيف اللفظ باعتبار الدالّ والمدلول مع "
        "مخرَجَين من محور التواطؤ والتشكيك تحت الكلّي، وهما تصنيفان مستقلّان "
        "بمجالين مجمَّدين منفصلين وأسئلةٍ مختلفة؛ فالقائمة دمجٌ بينهما لا إعادةُ "
        "إصدارِ تصنيفٍ واحدٍ على حالة اختبارٍ أخرى. والردّ باتٌّ للدعوى بصيغتها "
        "لا معلَّقٌ في انتظار شهادةٍ لاحقة، لأن العيب في بنية الدعوى نفسها"
    ),
    merged_classifications=(
        MergedClassification(
            module="lafz_madlul_relation_formal.py",
            classification="تصنيف اللفظ باعتبار الدالّ والمدلول",
            borrowed_values=("متباين", "مترادف", "مشترك"),
        ),
        MergedClassification(
            module="kulli_juzi_formal.py",
            classification="محور التواطؤ والتشكيك تحت الكلّي",
            borrowed_values=("متواطئ", "مشكِّك"),
        ),
    ),
    absent_term=CONVERGENCE_NOT_APPLICABLE_TEXT,
    refusals=(
        NamedRefusal(
            name="MergedListIsNotASecondApplication",
            statement=(
                "قائمةٌ تأخذ فروعًا من تصنيفين مستقلّين ليست تطبيقًا ثانيًا "
                "لأحدهما؛ والتقارب يُقاس بين حكمين لتصنيفٍ واحد على حالتَي "
                "اختبار، لا بين قائمةٍ وجزئَيها"
            ),
        ),
        NamedRefusal(
            name="NamedCriterionIsNotABuiltGate",
            statement=(
                "تسميةُ معيارٍ في محاورة لا تجعله اختبارًا مبنيًّا في هذا "
                "المستودع؛ فالقول بأن دعوى «تستوفي معياره» تقديرٌ خارجيّ لا "
                "نتيجةَ فحصٍ جرى"
            ),
        ),
        NamedRefusal(
            name="SharedVocabularyIsNotSharedClassification",
            statement=(
                "ورودُ أسماءٍ متشابهة في تصنيفين لا يُثبِت أنهما تصنيفٌ واحد؛ "
                "وهو عين انضباط RequestedVocabularyIsNotAttestedVocabulary"
            ),
        ),
        NamedRefusal(
            name="RefusalIsNotDeferral",
            statement=(
                "هذا ردٌّ للدعوى بصيغتها لا تأجيلٌ لها: لا يرفعه دليلٌ يُضاف بعدُ "
                "إلى أيٍّ من التصنيفين، وإنما ترفعه دعوى أخرى تُصاغ من جديد"
            ),
        ),
    ),
)

_MUTAWASSITA: Final = ConvergenceClaimRecord(
    claim=ConvergenceClaim.MUTAWASSITA_SECTION,
    statement="في المصدر قسمٌ مُسمّى «المتوسطة» يُضاف إلى الأقسام المُسجَّلة",
    standing=ClaimStanding.NAMED_SOURCE_ABSENT,
    ground=(
        "لم يرد هذا المصطلح في أيّ نصٍّ قُدِّم إلى هذا المستودع، ولا في أيّ وحدةٍ "
        "فيه؛ فالغياب مُسجَّل بالاسم، ولا يُفترَض وروده تحت اسمٍ آخر"
    ),
    merged_classifications=(),
    absent_term="المتوسطة",
    refusals=(
        NamedRefusal(
            name="NoSynonymSubstitutionWithoutInstruction",
            statement=(
                "لا يُحلّ مرادفٌ محلّ مصطلحٍ غائب ولا يُبحَث عنه بلا تصريح؛ "
                "والإحلال الصامت يُنتج فرعًا بلا شاهد"
            ),
        ),
        NamedRefusal(
            name="AbsenceIsNamedNotSilent",
            statement=(
                "الغياب يُسمّى في السجلّ ولا يُحذَف منه، وإلّا صارت الغاية "
                "المقصودة غيرَ مُسمّاة"
            ),
        ),
    ),
)

CONVERGENCE_CLAIM_REGISTER: Final = ConvergenceClaimRegister(
    records=(_SHARI_NAMES, _MUTAWASSITA)
)

for _dataclass in (
    NamedRefusal,
    MergedClassification,
    ConvergenceClaimRecord,
    ConvergenceClaimRegister,
):  # pragma: no cover - guard
    for _field in fields(_dataclass):
        if any(token in _field.name for token in _FORBIDDEN_FIELD_TOKENS):
            raise RuntimeError(
                "a register type carries a result, verdict, birth, or proof field"
            )

if CONVERGENCE_CLAIM_REGISTER.convergence_verdict_is_constructible:
    raise RuntimeError(  # pragma: no cover - guard
        "the register claims a constructible convergence verdict"
    )
if any(
    record.claim_is_operative for record in CONVERGENCE_CLAIM_REGISTER.records
):  # pragma: no cover - guard
    raise RuntimeError("a registered claim declares itself operative")
