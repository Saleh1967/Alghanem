"""تجميدُ مقامِ الضمائر وقيودِها ونافذةِ البحث قبل أيّ حصرٍ لمرشَّحي الإحالة.

**السؤالُ الذي وُضِعت له هذه الوحدة**: كم يُحصَر الضميرُ في القرآن؟ لا **مَن**
مرجعُه. والفرقُ بينهما ليس لفظًا: **المرجعُ الصحيح غير موسومٍ في أيّ مصدرٍ بين
أيدينا**، فلا ذهبَ يُقاس عليه، فلا دقّةَ ولا استدعاء. والمخرَجُ المشروعُ وحدَه:
**حجمُ مجموعةِ المرشَّحين، ونسبةُ ما يُحصَر منها لمرشَّحٍ واحد**.

`TheReferentIsNotAnnotatedAnywhere`: لا مدوَّنةَ هنا تَسِم مرجعَ ضميرٍ واحد؛
فأيُّ رقمِ دقّةٍ يخرج من هذا الباب رقمٌ بلا مقياس، ولا ترقيةَ لهذه الأداة إلى
«حسمِ مرجع» مهما تحسّنت.

`ACandidateSetIsNotAnAnswer`: حصرُ المرشَّحين تضييقُ احتمالٍ لا حسمٌ له؛ ومجموعةٌ
من واحدٍ ليست مرجعًا مُثبَتًا بل مرشَّحًا وحيدًا تحت نافذةٍ وقاعدةٍ مُعلَنتين.

`ElevenPercentIsTheRealDenominator`: الوسومُ المُجمَّلة — `SUBJ_PRON` و
`POSS_PRON` و`OBJ_PRON` — **لا تحمل شخصًا ولا عددًا ولا جنسًا**، فهي خارج
المقام بالكامل. والمقامُ الحقيقيّ ٢٬٦٠٨ من ٢٣٬٥٧٩ ضميرًا، أي نحو ١١٪؛ وهذا
القيدُ يظهر في كلّ رقمٍ يخرج من هنا.

`AnUnparsedTagYieldsNoConstraint`: وسمٌ لا يُحلَّل إلى الثلاثية كاملةً
(شخصٌ وعددٌ وجنسٌ ولو «غيرُ محدَّد» مُعلَنًا) **يُستبعَد صراحةً ويُعَدّ**، ولا
يُمنَح قيدًا افتراضيًّا.

`AWindowIsDeclaredNotOptimised`: النافذةُ — الآيةُ وسابقتُها في سورتها — تُعلَن
هنا **قبل** القياس، ولا تُوسَّع ولا تُضيَّق بعد رؤية النتائج؛ وإلّا كان ذلك
تشريعًا للرقم بعد وقوعه.

`GenderAndNumberAreInferredNotTagged`: جنسُ الاسم وعددُه **غير موسومَين في
MASAQ** — لا عمودَ جنسٍ ولا عمودَ عدد. فالمطابقةُ تستنتجهما من الصورة الصرفية
بقاعدةٍ مكتوبةٍ مُجمَّدةٍ هنا؛ وهو **استنتاجٌ بقاعدة لا وَسْمٌ بشريّ**، وجمعُ
التكسير خارجَ مقدورها صراحةً.

`NoFigureWithoutTheFingerprintedBytes`: الأعدادُ الخمسةَ عشرَ دعوًى حتّى تُعاد
من بايتاتٍ طُوبِق طولُها وبصمتُها؛ فإن غابت **لم يخرج رقم**.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .irab_column_census import SURA_COLUMN, VERSE_COLUMN
from .irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
    STANDING,
    WORD_KEY_COLUMN_NAME,
    RegistrationStanding,
)
from .masaq_corpus_deposit import (
    DERIVED_NOUN_TAGS,
    MORPH_TAG_COLUMN,
    rederive_tag_count,
)

__all__ = [
    "AGGREGATE_PRONOUN_TAGS",
    "ARRIVING_PRONOUN_TOTAL",
    "A_CANDIDATE_SET_IS_NOT_AN_ANSWER_NOTE",
    "A_NOMINAL_TAG_LIST_IS_DECLARED_NOT_DISCOVERED_NOTE",
    "A_WINDOW_IS_DECLARED_NOT_OPTIMISED_NOTE",
    "AN_UNDETERMINED_INFERENCE_IS_NOT_A_MATCH_NOTE",
    "AN_UNPARSED_TAG_YIELDS_NO_CONSTRAINT_NOTE",
    "CONSTRAINED_PRONOUN_TAGS",
    "DECLARED_DENOMINATOR_COUNT",
    "DENOMINATOR_SHARE_PERCENTAGE",
    "ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE",
    "GENDER_AND_NUMBER_ARE_INFERRED_NOT_TAGGED_NOTE",
    "INFERENCE_UNDETERMINED",
    "NOMINAL_TAG_VALUES",
    "NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE",
    "PRE_MEASUREMENT_EXPECTATION",
    "PRONOUN_CONSTRAINT_PARSING_RULE",
    "PRONOUN_DENOMINATOR",
    "REFERENT_CANDIDATE_CENSUS_COLUMNS",
    "REFERENT_CANDIDATE_PREREGISTRATION_DIGEST",
    "REFERENT_CANDIDATE_NAMED_RESIDUALS",
    "SEARCH_WINDOW",
    "SEGMENTED_WORD_COLUMN",
    "STEM_MORPH_TYPE",
    "SURFACE_INFERENCE_RULE",
    "SURFACE_INFERENCE_SUFFIXES",
    "THE_HOST_WORD_IS_NOT_ITS_OWN_CANDIDATE_NOTE",
    "THE_REFERENT_IS_NOT_ANNOTATED_ANYWHERE_NOTE",
    "AggregatePronounTag",
    "ConstrainedPronounTag",
    "DeclaredDenominator",
    "ExpectationVerdict",
    "Gender",
    "Number",
    "Person",
    "PronounConstraint",
    "ReferentPreregistrationError",
    "SearchWindow",
    "SurfaceInference",
    "SurfaceSuffixRule",
    "constraints_of",
    "expectation_verdict",
    "infer_surface",
    "is_nominal_tag",
    "pronoun_tag_figures",
    "referent_preregistration_digest",
    "strip_surface",
]


class ReferentPreregistrationError(ValueError):
    """تُرفَع حين يُودَع وسمٌ بلا ثلاثيّةٍ مُعلَنة، أو مقامٌ بلا قاعدةِ حصر."""


# ─── القوانينُ المكتوبة داخل الوحدة ────────────────────────────────────────

THE_REFERENT_IS_NOT_ANNOTATED_ANYWHERE_NOTE: Final[str] = (
    "TheReferentIsNotAnnotatedAnywhere: مرجعُ الضمير غيرُ موسومٍ في أيّ مصدرٍ "
    "بين أيدينا؛ فلا ذهبَ، فلا دقّةَ ولا استدعاء، ولا ترقيةَ لهذه الأداة إلى "
    "حسمِ مرجعٍ مهما تحسّنت قاعدتُها"
)

A_CANDIDATE_SET_IS_NOT_AN_ANSWER_NOTE: Final[str] = (
    "ACandidateSetIsNotAnAnswer: حصرُ المرشَّحين تضييقُ احتمالٍ تحت نافذةٍ "
    "وقاعدةٍ مُعلَنتين، لا حسمٌ للمرجع؛ ومجموعةٌ من واحدٍ مرشَّحٌ وحيدٌ لا مرجعٌ "
    "مُثبَت"
)

ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE: Final[str] = (
    "ElevenPercentIsTheRealDenominator: المقامُ ٢٬٦٠٨ من ٢٣٬٥٧٩ ضميرًا لا "
    "كلُّها؛ لأنّ `SUBJ_PRON` و`POSS_PRON` و`OBJ_PRON` لا تحمل شخصًا ولا عددًا "
    "ولا جنسًا، فهي خارج المقام بالكامل ولا تُحمَل على أقرب وَسْمٍ مُفصَّلٍ إليها"
)

AN_UNPARSED_TAG_YIELDS_NO_CONSTRAINT_NOTE: Final[str] = (
    "AnUnparsedTagYieldsNoConstraint: وسمٌ لا يُحلَّل إلى الثلاثية كاملةً "
    "يُستبعَد من المقام صراحةً ويُعَدُّ في حقلٍ باسمه، ولا يُمنَح قيدًا "
    "افتراضيًّا؛ فالقيدُ المُخمَّن يُخرِج حصرًا لم يقع"
)

A_WINDOW_IS_DECLARED_NOT_OPTIMISED_NOTE: Final[str] = (
    "AWindowIsDeclaredNotOptimised: نافذةُ البحث — الآيةُ وسابقتُها في سورتها "
    "— مُعلَنةٌ قبل القياس، ولا تُوسَّع ولا تُضيَّق بعد رؤية النتائج؛ وتعديلُها "
    "بعد رقمٍ تشريعٌ للرقم لا قياسٌ له"
)

GENDER_AND_NUMBER_ARE_INFERRED_NOT_TAGGED_NOTE: Final[str] = (
    "GenderAndNumberAreInferredNotTagged: لا عمودَ جنسٍ ولا عمودَ عددٍ في "
    "MASAQ للأسماء؛ فجنسُ الاسم وعددُه **مُستنتَجان من الصورة الصرفية** "
    "بقاعدةٍ مكتوبةٍ مُجمَّدة، لا موسومان بيد مُوسِّم — وجمعُ التكسير خارجَ "
    "مقدور القاعدة صراحةً"
)

AN_UNDETERMINED_INFERENCE_IS_NOT_A_MATCH_NOTE: Final[str] = (
    "AnUndeterminedInferenceIsNotAMatch: اسمٌ عجزت عنه قاعدةُ الاستنتاج لا "
    "يُقبَل مرشَّحًا ولا يُسقَط صامتًا، بل يُعَدُّ في حقلٍ باسمه؛ فالسكوتُ عنه "
    "يُضيِّق مجموعةً بغير دليل"
)

A_NOMINAL_TAG_LIST_IS_DECLARED_NOT_DISCOVERED_NOTE: Final[str] = (
    "ANominalTagListIsDeclaredNotDiscovered: أسماءُ الوسوم الاسمية مُجمَّدةٌ "
    "هنا قائمةً مطابقةً حرفيًّا، لا مُلتقَطةً باحتواءِ نصٍّ في وَسْم؛ ووسمٌ خارجَ "
    "القائمة ليس مرشَّحًا ولو بدا اسمًا"
)

THE_HOST_WORD_IS_NOT_ITS_OWN_CANDIDATE_NOTE: Final[str] = (
    "TheHostWordIsNotItsOwnCandidate: الجذعُ الحاملُ للضمير المتّصل في كلمته "
    "نفسها يخرج من المرشَّحين بقاعدةٍ مُعلَنة؛ وهذا **إخراجٌ مُصرَّحٌ به** لا "
    "حكمٌ نحويٌّ مُثبَتٌ على كلّ موضع"
)

NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE: Final[str] = (
    "NoFigureWithoutTheFingerprintedBytes: كلُّ عددٍ هنا دعوًى حتّى يُعادَ "
    "اشتقاقُه من بايتاتٍ طُوبِق طولُها وبصمتُها؛ فإن غابت لم يخرج رقمٌ ولم "
    "يُوضَع مكانَه تقديرٌ ولا قيمةٌ محفوظة"
)

REFERENT_CANDIDATE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TheReferentIsNotAnnotatedAnywhere": THE_REFERENT_IS_NOT_ANNOTATED_ANYWHERE_NOTE,
    "ACandidateSetIsNotAnAnswer": A_CANDIDATE_SET_IS_NOT_AN_ANSWER_NOTE,
    "ElevenPercentIsTheRealDenominator": (ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE),
    "GenderAndNumberAreInferredNotTagged": (
        GENDER_AND_NUMBER_ARE_INFERRED_NOT_TAGGED_NOTE
    ),
    "AnUnparsedTagYieldsNoConstraint": AN_UNPARSED_TAG_YIELDS_NO_CONSTRAINT_NOTE,
    "AWindowIsDeclaredNotOptimised": A_WINDOW_IS_DECLARED_NOT_OPTIMISED_NOTE,
    "AnUndeterminedInferenceIsNotAMatch": (
        AN_UNDETERMINED_INFERENCE_IS_NOT_A_MATCH_NOTE
    ),
    "ANominalTagListIsDeclaredNotDiscovered": (
        A_NOMINAL_TAG_LIST_IS_DECLARED_NOT_DISCOVERED_NOTE
    ),
    "TheHostWordIsNotItsOwnCandidate": THE_HOST_WORD_IS_NOT_ITS_OWN_CANDIDATE_NOTE,
    "NoFigureWithoutTheFingerprintedBytes": (
        NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
    ),
}
"""حدودُ هذه الوحدة مكتوبةً بأسمائها؛ ولا يخرج منها رقمٌ بلا حدٍّ يُقرأ معه."""


# ─── الثلاثيّةُ وقاعدةُ تحليلها ────────────────────────────────────────────


class Person(Enum):
    """الشخصُ من الرقم في الوَسْم؛ ولا رابعَ له في هذه القاعدة."""

    FIRST = "1"
    SECOND = "2"
    THIRD = "3"


class Number(Enum):
    """العددُ من حرفٍ واحدٍ في الوَسْم: مفردٌ ومثنًّى وجمع."""

    SINGULAR = "S"
    DUAL = "D"
    PLURAL = "P"


class Gender(Enum):
    """الجنسُ من حرفٍ إن حضر؛ و«غيرُ محدَّد» **بابٌ مُعلَنٌ** لا فراغٌ مطويّ."""

    MASCULINE = "M"
    FEMININE = "F"
    UNSPECIFIED = "—"


@dataclass(frozen=True, slots=True)
class PronounConstraint:
    """قيدُ الضمير ثلاثيّةً كاملة؛ ولا يُبنى ناقصًا ولا يُكمَّل بافتراض."""

    person: Person
    number: Number
    gender: Gender

    def __post_init__(self) -> None:
        for value, kind, label in (
            (self.person, Person, "الشخص"),
            (self.number, Number, "العدد"),
            (self.gender, Gender, "الجنس"),
        ):
            if not isinstance(value, kind):
                raise ReferentPreregistrationError(
                    f"{label} يُعلَن من بابه المُجمَّد لا من نصٍّ حرّ. "
                    + AN_UNPARSED_TAG_YIELDS_NO_CONSTRAINT_NOTE
                )

    @property
    def is_discourse_participant(self) -> bool:
        """أضميرُ متكلّمٍ أو مخاطَب؟ فهذان لأطراف الخطاب لا لاسمٍ سابق."""

        return self.person in (Person.FIRST, Person.SECOND)


PRONOUN_CONSTRAINT_PARSING_RULE: Final[str] = (
    "قاعدةُ التحليل المُجمَّدة: يُجرَّد الوَسْمُ من بادئةٍ واحدةٍ من "
    "«POSS_» أو «OBJ_» أو «SUBJ_»، ثمّ يجب أن يبدأ الباقي بـ«PRON_» حرفيًّا؛ "
    "وما بعدها رقمُ شخصٍ من ١ أو ٢ أو ٣، يتبعه إمّا حرفُ عددٍ وحدَه من "
    "«S/D/P» — فالجنسُ «غيرُ محدَّد» مُعلَنًا — وإمّا حرفُ جنسٍ من «M/F» ثمّ "
    "حرفُ عدد. وما خالف هذه الصورةَ حرفًا حرفًا لا يُحلَّل ولا يُقارَب"
)


def constraints_of(tag: str) -> PronounConstraint | None:
    """ثلاثيّةُ الوَسْم، أو `None` لوسمٍ لا يُحلَّل — بلا قيدٍ افتراضيّ البتّة."""

    if not isinstance(tag, str):
        return None
    body = tag.strip()
    for prefix in ("POSS_", "OBJ_", "SUBJ_"):
        if body.startswith(prefix):
            body = body[len(prefix) :]
            break
    if not body.startswith("PRON_"):
        return None
    body = body[len("PRON_") :]
    if not body:
        return None
    try:
        person = Person(body[0])
    except ValueError:
        return None
    rest = body[1:]
    if len(rest) == 1:
        gender_letter, number_letter = None, rest
    elif len(rest) == 2:
        gender_letter, number_letter = rest[0], rest[1]
    else:
        return None
    try:
        number = Number(number_letter)
    except ValueError:
        return None
    if gender_letter is None:
        gender = Gender.UNSPECIFIED
    else:
        try:
            gender = Gender(gender_letter)
        except ValueError:
            return None
    return PronounConstraint(person=person, number=number, gender=gender)


# ─── المقامُ المُعلَن ──────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class DeclaredDenominator:
    """مقامٌ منطوقٌ باسمه وقاعدةِ حصرِه؛ ولا نسبةَ في هذا الباب بغيره."""

    name: str
    column: str
    counting_rule: str

    def __post_init__(self) -> None:
        for field in fields(self):
            text = getattr(self, field.name)
            if not isinstance(text, str) or not text.strip():
                raise ReferentPreregistrationError(
                    f"{field.name} نصٌّ غير فارغ؛ ومقامٌ بلا قاعدةِ حصرٍ مكتوبةٍ "
                    "يُقرأ نسبةً بلا مقام. " + ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE
                )


PRONOUN_DENOMINATOR: Final[DeclaredDenominator] = DeclaredDenominator(
    name="الضمائرُ المُقيَّدةُ في وَسْمها",
    column=MORPH_TAG_COLUMN,
    counting_rule=(
        "الضميرُ المُقيَّد: سجلٌّ قيمةُ `Morph_Tag` فيه مطابقةٌ حرفيًّا لواحدٍ "
        "من الوسوم الخمسةَ عشرَ المُجمَّدة أدناه بعد تجريد الفراغ الطرفيّ؛ "
        "والمقامُ هذه وحدَها لا الضمائرُ كلُّها، لأنّ الوسومَ المُجمَّلة لا "
        "تحمل ثلاثيّةً تُقيَّد بها مطابقة"
    ),
)


@dataclass(frozen=True, slots=True)
class ConstrainedPronounTag:
    """وَسْمُ ضميرٍ مُقيَّدٍ بعدده الواصل وثلاثيّتِه المُعلَنةِ قبل القياس."""

    tag: str
    arabic_name: str
    deposited_count: int

    def __post_init__(self) -> None:
        for text, label in ((self.tag, "الوَسْم"), (self.arabic_name, "اسمُه")):
            if not isinstance(text, str) or not text.strip():
                raise ReferentPreregistrationError(f"{label} نصٌّ غير فارغ.")
        if (
            isinstance(self.deposited_count, bool)
            or not isinstance(self.deposited_count, int)
            or self.deposited_count < 0
        ):
            raise ReferentPreregistrationError(
                "العددُ الواصلُ عددٌ صحيحٌ غيرُ سالب؛ ولا يُودَع تقديرًا."
            )
        if constraints_of(self.tag) is None:
            raise ReferentPreregistrationError(
                f"الوَسْمُ «{self.tag}» لا يُحلَّل إلى الثلاثية كاملةً، فلا "
                "يدخل المقام. " + AN_UNPARSED_TAG_YIELDS_NO_CONSTRAINT_NOTE
            )

    @property
    def constraint(self) -> PronounConstraint:
        """ثلاثيّتُه مُشتقّةً من وَسْمه بالقاعدة، لا مكتوبةً بجانبه فتُخالِفه."""

        parsed = constraints_of(self.tag)
        if parsed is None:  # pragma: no cover - يمنعه `__post_init__`
            raise ReferentPreregistrationError(self.tag)
        return parsed


CONSTRAINED_PRONOUN_TAGS: Final[tuple[ConstrainedPronounTag, ...]] = (
    ConstrainedPronounTag("PRON_3MS", "ضمير غائب مفرد مذكّر", 710),
    ConstrainedPronounTag("PRON_3MP", "ضمير غائب جمع مذكّر", 644),
    ConstrainedPronounTag("PRON_2MP", "ضمير مخاطَب جمع مذكّر", 427),
    ConstrainedPronounTag("PRON_1S", "ضمير متكلّم مفرد", 169),
    ConstrainedPronounTag("POSS_PRON_3MS", "ضمير ملكية غائب مفرد مذكّر", 178),
    ConstrainedPronounTag("POSS_PRON_3MP", "ضمير ملكية غائب جمع مذكّر", 148),
    ConstrainedPronounTag("PRON_1P", "ضمير متكلّم جمع", 77),
    ConstrainedPronounTag("PRON_2MS", "ضمير مخاطَب مفرد مذكّر", 79),
    ConstrainedPronounTag("PRON_3FS", "ضمير غائب مفرد مؤنّث", 61),
    ConstrainedPronounTag("POSS_PRON_3D", "ضمير ملكية غائب مثنّى", 40),
    ConstrainedPronounTag("POSS_PRON_3FS", "ضمير ملكية غائب مفرد مؤنّث", 29),
    ConstrainedPronounTag("POSS_PRON_1S", "ضمير ملكية متكلّم مفرد", 24),
    ConstrainedPronounTag("PRON_3D", "ضمير غائب مثنّى", 11),
    ConstrainedPronounTag("PRON_3FP", "ضمير غائب جمع مؤنّث", 7),
    ConstrainedPronounTag("POSS_PRON_2MS", "ضمير ملكية مخاطَب مفرد مذكّر", 4),
)
"""الوسومُ الخمسةَ عشرَ التي تحمل قيدًا مُشفَّرًا فعلًا؛ وهي المقامُ كلُّه."""


DECLARED_DENOMINATOR_COUNT: Final[int] = sum(
    item.deposited_count for item in CONSTRAINED_PRONOUN_TAGS
)
"""٢٬٦٠٨: مجموعُ الخمسةَ عشرَ عدًّا لا رقمًا مكتوبًا بجانبها فقد يُخالِفها."""


@dataclass(frozen=True, slots=True)
class AggregatePronounTag:
    """وَسْمٌ مُجمَّلٌ **خارجَ المقام**؛ مُعلَنٌ بعدده كي يُرى حجمُ ما خرج."""

    tag: str
    arabic_name: str
    deposited_count: int
    why_it_is_outside: str

    def __post_init__(self) -> None:
        if constraints_of(self.tag) is not None:
            raise ReferentPreregistrationError(
                f"الوَسْمُ «{self.tag}» يُحلَّل إلى ثلاثيّةٍ، فليس مُجمَّلًا؛ "
                "ولا يُعلَن خارجَ المقام ما يحمل قيدًا."
            )
        if not self.why_it_is_outside.strip():
            raise ReferentPreregistrationError(
                "خروجُ وَسْمٍ من المقام يُكتَب بعلّته لا بإسقاطه. "
                + ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE
            )


AGGREGATE_PRONOUN_TAGS: Final[tuple[AggregatePronounTag, ...]] = (
    AggregatePronounTag(
        tag="SUBJ_PRON",
        arabic_name="ضمير رفع مُجمَّل",
        deposited_count=7_964,
        why_it_is_outside=(
            "لا شخصَ فيه ولا عددَ ولا جنس؛ فحصرُ مرشَّحيه يحتاج قيدًا ليس في "
            "وَسْمه، ولا يُستعار له قيدٌ من جارٍ ولا من سياق"
        ),
    ),
    AggregatePronounTag(
        tag="POSS_PRON",
        arabic_name="ضمير ملكية مُجمَّل",
        deposited_count=7_678,
        why_it_is_outside=(
            "مُجمَّلٌ كسابقه؛ وكِبَرُ عدده هو بعينه سببُ التصريح به: إسقاطُه "
            "صامتًا يُوهِم أنّ المقام كلُّ الضمائر"
        ),
    ),
    AggregatePronounTag(
        tag="OBJ_PRON",
        arabic_name="ضمير نصب مُجمَّل",
        deposited_count=3_211,
        why_it_is_outside=(
            "مُجمَّلٌ كسابقيه؛ ومجموعُ الثلاثة ١٨٬٨٥٣ ضميرًا لا يدخل حصرًا "
            "واحدًا في هذه الأداة"
        ),
    ),
)
"""الوسومُ الثلاثةُ المُجمَّلة؛ خارجَ المقام بعللها المكتوبة لا بصمتٍ عنها."""


ARRIVING_PRONOUN_TOTAL: Final[int] = 23_579
"""جملةُ الضمائر كما وصلت؛ مقامُ نسبة المقام أدناه، ودعوًى حتّى تُعادَ."""

DENOMINATOR_SHARE_PERCENTAGE: Final[str] = "11.0607"
"""نصيبُ المقام الحقيقيّ من الضمائر كلِّها: ٢٬٦٠٨ ÷ ٢٣٬٥٧٩، بمنازلِ مقارنتها."""


# ─── النافذةُ المُعلَنة ────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class SearchWindow:
    """نافذةُ البحث مُعلَنةً قبل القياس: آياتٌ سابقةٌ معدودةٌ، وسورةٌ لا تُعبَر."""

    preceding_verses: int
    crosses_sura_boundary: bool
    declaration: str

    def __post_init__(self) -> None:
        if (
            isinstance(self.preceding_verses, bool)
            or not isinstance(self.preceding_verses, int)
            or self.preceding_verses < 0
        ):
            raise ReferentPreregistrationError(
                "عددُ الآيات السابقة عددٌ صحيحٌ غيرُ سالب. "
                + A_WINDOW_IS_DECLARED_NOT_OPTIMISED_NOTE
            )
        if not self.declaration.strip():
            raise ReferentPreregistrationError(
                "نافذةٌ بلا نصِّ إعلانٍ نافذةٌ تُعدَّل بلا أثر. "
                + A_WINDOW_IS_DECLARED_NOT_OPTIMISED_NOTE
            )


SEARCH_WINDOW: Final[SearchWindow] = SearchWindow(
    preceding_verses=1,
    crosses_sura_boundary=False,
    declaration=(
        "الأسماءُ الواقعةُ **قبل** الضمير في ترتيب الكلمات، في آيته وفي "
        "الآيةِ السابقةِ لها وحدَها، داخلَ سورتها؛ فلا تُعبَر حدودُ السورة، "
        "ولا تُقرأ آيةٌ ثالثةٌ، ولا يُنظَر إلى ما بعد الضمير. "
        + A_WINDOW_IS_DECLARED_NOT_OPTIMISED_NOTE
    ),
)


STEM_MORPH_TYPE: Final[str] = "Stem"
"""قيمةُ `Morph_type` للجذع؛ واللواحقُ والسوابقُ ليست مرشَّحةً لإحالةِ ضمير."""

SEGMENTED_WORD_COLUMN: Final[str] = "Segmented_Word"
"""عمودُ الصورة الصرفية الذي تُقرأ منه اللواحق؛ تغطيتُه الواصلةُ ٩٨٫٢٥٥٣٪."""

REFERENT_CANDIDATE_CENSUS_COLUMNS: Final[tuple[str, ...]] = (
    SURA_COLUMN,
    VERSE_COLUMN,
    ANCHOR_COLUMN_NAME,
    MORPH_TAG_COLUMN,
    WORD_KEY_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
    SEGMENTED_WORD_COLUMN,
)
"""الأعمدةُ السبعةُ التي يقوم بها هذا الحصر؛ وغيابُ واحدٍ يُوقِف العدّ."""


NOMINAL_TAG_VALUES: Final[tuple[str, ...]] = tuple(
    sorted({item.tag for item in DERIVED_NOUN_TAGS} | {"NOUN", "PN"})
)
"""الوسومُ الاسميةُ المُجمَّدة: أبوابُ المشتقّات الأربعةَ عشرَ زائدَ الاسمِ والعَلَم.

`ANominalTagListIsDeclaredNotDiscovered`: مطابقةً حرفيّةً لا احتواءً؛ و«NOUN»
و«PN» **دعوى اسمٍ حتّى تُقرأ الترويسةُ والقيم**، كما أنّ أبوابَ المشتقّات
مأخوذةٌ من `DERIVED_NOUN_TAGS` لا مكتوبةً ثانيةً فتُخالِفها.
"""


def is_nominal_tag(tag: str) -> bool:
    """أهذا وَسْمٌ اسميٌّ مُعلَن؟ مطابقةً حرفيّةً بعد تجريد الفراغ الطرفيّ."""

    return isinstance(tag, str) and tag.strip() in NOMINAL_TAG_VALUES


# ─── قاعدةُ استنتاج الجنس والعدد من الصورة ────────────────────────────────

_DIACRITICS: Final[frozenset[str]] = frozenset(
    "\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0653\u0654\u0655"
    "\u0656\u0657\u0658\u0670\u06df\u06e0\u0640"
)
"""الحركاتُ والتطويلُ والخناجرُ تُجرَّد قبل قراءة اللاحقة؛ بقاعدةٍ لا بذوق."""

_SEGMENT_SEPARATORS: Final[frozenset[str]] = frozenset("+-|")
"""فواصلُ التقطيع في `Segmented_Word` تُجرَّد؛ فهي أثرُ مُوسِّمٍ لا حرفُ كلمة."""


def strip_surface(surface: str) -> str:
    """الصورةُ مُجرَّدةً من الحركات وفواصل التقطيع؛ خطوةً مُعلَنةً لا مطويّة."""

    return "".join(
        character
        for character in (surface or "").strip()
        if character not in _DIACRITICS and character not in _SEGMENT_SEPARATORS
    )


@dataclass(frozen=True, slots=True)
class SurfaceInference:
    """ما استنتجته القاعدةُ من الصورة: عددٌ وجنسٌ، أو عجزٌ مُسمًّى لا صمت."""

    number: Number | None
    gender: Gender | None
    rule_name: str

    @property
    def is_determined(self) -> bool:
        """أحُسِم العددُ والجنسُ معًا؟ وما دون ذلك عجزٌ يُعَدُّ ولا يُطابَق به."""

        return self.number is not None and self.gender is not None


INFERENCE_UNDETERMINED: Final[str] = "INFERENCE_UNDETERMINED"
"""اسمُ العجز؛ يُعَدُّ في حقلٍ باسمه ولا يُسحَب إلى «مذكّرٍ مفردٍ» افتراضًا."""


@dataclass(frozen=True, slots=True)
class SurfaceSuffixRule:
    """لاحقةٌ صوريّةٌ واحدةٌ بما تُفيده؛ و`None` في أحد الحقلين عجزٌ مُصرَّحٌ به."""

    suffix: str
    number: Number | None
    gender: Gender | None
    name: str
    note: str

    def __post_init__(self) -> None:
        if not self.suffix.strip():
            raise ReferentPreregistrationError("لاحقةٌ فارغةٌ تُطابِق كلَّ اسم.")
        if not self.name.strip() or not self.note.strip():
            raise ReferentPreregistrationError(
                "قاعدةٌ بلا اسمٍ أو بلا حدٍّ مكتوبٍ استنتاجٌ بلا شاهد. "
                + GENDER_AND_NUMBER_ARE_INFERRED_NOT_TAGGED_NOTE
            )


SURFACE_INFERENCE_SUFFIXES: Final[tuple[SurfaceSuffixRule, ...]] = (
    SurfaceSuffixRule(
        suffix="\u062a\u0627\u0646",
        number=Number.DUAL,
        gender=Gender.FEMININE,
        name="تاء+ألف+نون",
        note="مثنّى مؤنّث سالم؛ ويُقرأ قبل «ان» كي لا تبتلعه",
    ),
    SurfaceSuffixRule(
        suffix="\u062a\u064a\u0646",
        number=None,
        gender=None,
        name="تاء+ياء+نون",
        note=(
            "صورةُ نصبٍ وجرٍّ للمثنّى المؤنّث، وتُشارِكها جموعٌ مؤنّثةٌ أخرى؛ "
            "فالعجزُ هنا مُصرَّحٌ به لا مُرجَّح"
        ),
    ),
    SurfaceSuffixRule(
        suffix="\u0627\u062a",
        number=Number.PLURAL,
        gender=Gender.FEMININE,
        name="ألف+تاء",
        note="جمع مؤنّث سالم؛ ولا يُقاس عليه جمعُ التكسير المؤنّث",
    ),
    SurfaceSuffixRule(
        suffix="\u0648\u0646",
        number=Number.PLURAL,
        gender=Gender.MASCULINE,
        name="واو+نون",
        note="جمع مذكّر سالم في صورة الرفع وحدَها",
    ),
    SurfaceSuffixRule(
        suffix="\u064a\u0646",
        number=None,
        gender=None,
        name="ياء+نون",
        note=(
            "مشتركةٌ بين المثنّى والجمع المذكّر السالم في النصب والجرّ؛ "
            "فلا تُحسَم إلى أحدهما، والعجزُ يُسمّى ولا يُرجَّح"
        ),
    ),
    SurfaceSuffixRule(
        suffix="\u0627\u0646",
        number=Number.DUAL,
        gender=Gender.MASCULINE,
        name="ألف+نون",
        note="مثنّى مذكّر سالم في صورة الرفع؛ بعد استثناء «تان» قبلها",
    ),
    SurfaceSuffixRule(
        suffix="\u0629",
        number=Number.SINGULAR,
        gender=Gender.FEMININE,
        name="تاء التأنيث",
        note="مفرد مؤنّث بالصورة؛ ولا يُنفى بها تأنيثٌ بغير علامة",
    ),
)
"""جدولُ اللواحق مرتَّبًا ترتيبَ قراءةٍ مُعلَنًا؛ وأوّلُ ما يُطابِق هو المُطبَّق."""


SURFACE_INFERENCE_RULE: Final[str] = (
    "قاعدةُ الاستنتاج: تُجرَّد الصورةُ من الحركات وفواصل التقطيع، ثمّ تُقرأ "
    "لواحقُها بترتيب `SURFACE_INFERENCE_SUFFIXES`؛ فأوّلُ لاحقةٍ تُطابِق آخرَ "
    "الصورة هي المُطبَّقة. وما لا يُطابِق شيئًا — وفيه جمعُ التكسير والمفردُ "
    "المذكّرُ العاري — يُصنَّف «INFERENCE_UNDETERMINED» ولا يُسحَب إلى بابٍ. "
    + GENDER_AND_NUMBER_ARE_INFERRED_NOT_TAGGED_NOTE
)


def infer_surface(surface: str) -> SurfaceInference:
    """استنتجْ عددَ الاسم وجنسَه من صورته؛ والعجزُ مخرَجٌ مُسمًّى لا استثناء."""

    stripped = strip_surface(surface)
    if stripped:
        for rule in SURFACE_INFERENCE_SUFFIXES:
            if stripped.endswith(rule.suffix):
                return SurfaceInference(
                    number=rule.number, gender=rule.gender, rule_name=rule.name
                )
    return SurfaceInference(number=None, gender=None, rule_name=INFERENCE_UNDETERMINED)


# ─── التوقّعُ المكتوبُ قبل القياس ──────────────────────────────────────────

PRE_MEASUREMENT_EXPECTATION: Final[str] = (
    "PreMeasurementExpectation: المُصرَّحُ به **قبل** أيّ تشغيل: أن تكون نسبةُ "
    "الحصر لمرشَّحٍ واحدٍ في ضمير المتكلّم — `PRON_1S` و`PRON_1P` — أعلى منها "
    "في ضمير الغائب — `PRON_3MS` و`PRON_3MP` — لأنّ المتكلّم مقيَّدٌ بالسياق "
    "الخطابيّ لا بالأسماء السابقة. وشرطُ تكذيبه مكتوبٌ: إن تساوت النسبتان أو "
    "كانت نسبةُ الغائب أعلى فالتوقّعُ **مُكذَّب**، ويُعرَض مكذوبًا ولا يُعدَّل "
    "ليُطابِق ما قِيس. ولا يُقرأ هذا حكمًا على مرجعٍ: "
    + A_CANDIDATE_SET_IS_NOT_AN_ANSWER_NOTE
)


class ExpectationVerdict(Enum):
    """حكمُ التوقّع مُسمًّى ثلاثًا؛ و«لا يُقاس» بابٌ مُعلَنٌ لا صفرٌ مطويّ."""

    HELD = "صدق"
    FALSIFIED = "كُذِّب"
    NOT_MEASURABLE = "لا_يُقاس"


def expectation_verdict(
    *, speaker_single_share: float | None, absent_single_share: float | None
) -> ExpectationVerdict:
    """قارِن المقيسَ بالتوقّع بلا تعديلٍ له؛ ومقامٌ خالٍ يُقرأ «لا يُقاس»."""

    if speaker_single_share is None or absent_single_share is None:
        return ExpectationVerdict.NOT_MEASURABLE
    if speaker_single_share > absent_single_share:
        return ExpectationVerdict.HELD
    return ExpectationVerdict.FALSIFIED


# ─── الأرقامُ ومُعيداتُ اشتقاقها ───────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class _TagFigure:
    """عددُ وَسْمٍ مُودَعٌ مع دالّةِ إعادة اشتقاقه من البايتات المُبصَّمة."""

    tag: str
    arabic_name: str
    deposited: int
    derive: Callable[[bytes], int]

    def rederive(self, data: bytes) -> int:
        """أعِد اشتقاقَ العدد من البايتات، بلا مقارنةٍ ولا حكمٍ هنا."""

        return self.derive(data)

    def holds(self, data: bytes) -> bool:
        """أطابق المُودَعُ ما اشتُقَّ الآن؟ والدرءُ أنّ الفرقَ يُرى لا يُطوى."""

        return self.rederive(data) == self.deposited


def _counter(tag: str) -> Callable[[bytes], int]:
    """دالّةُ عدٍّ لوَسْمٍ بعينه؛ مُسمّاةً لا مُغلَقةً على متغيّرِ حلقة."""

    def derive(data: bytes) -> int:
        return rederive_tag_count(data, tag)

    return derive


def pronoun_tag_figures() -> tuple[_TagFigure, ...]:
    """ثمانيةَ عشرَ رقمًا: خمسةَ عشرَ في المقام وثلاثةٌ مُجمَّلةٌ خارجَه."""

    figures: list[_TagFigure] = [
        _TagFigure(
            tag=item.tag,
            arabic_name=item.arabic_name,
            deposited=item.deposited_count,
            derive=_counter(item.tag),
        )
        for item in CONSTRAINED_PRONOUN_TAGS
    ]
    figures.extend(
        _TagFigure(
            tag=item.tag,
            arabic_name=item.arabic_name,
            deposited=item.deposited_count,
            derive=_counter(item.tag),
        )
        for item in AGGREGATE_PRONOUN_TAGS
    )
    return tuple(figures)


def referent_preregistration_digest() -> str:
    """بصمةُ محتوى التسجيل؛ فتبديلُ وسمٍ أو نافذةٍ أو لاحقةٍ تُغيّرها."""

    return canonical_digest(
        canonical_bytes(
            {
                "standing": STANDING.value,
                "denominator": [
                    PRONOUN_DENOMINATOR.name,
                    PRONOUN_DENOMINATOR.column,
                    PRONOUN_DENOMINATOR.counting_rule,
                ],
                "constrained_tags": [
                    [item.tag, item.deposited_count]
                    for item in CONSTRAINED_PRONOUN_TAGS
                ],
                "aggregate_tags": [
                    [item.tag, item.deposited_count] for item in AGGREGATE_PRONOUN_TAGS
                ],
                "denominator_count": DECLARED_DENOMINATOR_COUNT,
                "pronoun_total": ARRIVING_PRONOUN_TOTAL,
                "share": DENOMINATOR_SHARE_PERCENTAGE,
                "window": [
                    SEARCH_WINDOW.preceding_verses,
                    SEARCH_WINDOW.crosses_sura_boundary,
                    SEARCH_WINDOW.declaration,
                ],
                "nominal_tags": list(NOMINAL_TAG_VALUES),
                "suffixes": [
                    [
                        rule.suffix,
                        rule.number.value if rule.number else INFERENCE_UNDETERMINED,
                        rule.gender.value if rule.gender else INFERENCE_UNDETERMINED,
                    ]
                    for rule in SURFACE_INFERENCE_SUFFIXES
                ],
                "parsing_rule": PRONOUN_CONSTRAINT_PARSING_RULE,
                "expectation": PRE_MEASUREMENT_EXPECTATION,
                "residuals": REFERENT_CANDIDATE_NAMED_RESIDUALS,
            }
        )
    )


REFERENT_CANDIDATE_PREREGISTRATION_DIGEST: Final[str] = (
    referent_preregistration_digest()
)
"""بصمةُ التسجيل عند استيراده؛ وتُربَط بكلّ مخرَجٍ كي يُعرَف تحت أيّ قاعدةٍ قِيس."""


if STANDING is not RegistrationStanding.FORMULATED_AFTER_THE_NUMBER:  # pragma: no cover
    raise ReferentPreregistrationError(
        "منزلةُ التسجيل تُقرأ من بابها المُعلَن لا تُكتَب هنا ثانيةً."
    )
