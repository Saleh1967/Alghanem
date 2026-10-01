"""قاموسُ مصطلحات النحو — المرحلةُ صفرٌ لجسر الدالّ/المدلول.

وهذه الوحدةُ **قاموسُ أدواتٍ ومصطلحات**: تُخرِج أسماءَ الأدوات وأعمالَها
وتعريفاتِها المختصرة من بايتاتٍ مختومة، كلَّ بندٍ بدليلٍ حرفيٍّ وموضعٍ يُفتَح.
ولا تَسِم نصًّا ولا تبني زوجَ دالٍّ ومدلول: كلاهما طورٌ لاحقٌ يستعمل هذا
القاموس، وسطرُ التأجيل مكتوبٌ صريحًا في `THE_DEFERRED_LINE`.

## لماذا مرحلةٌ صفرٌ أصلًا

الوسمُ («هذا اسم وهذا فعلٌ وهذا حرفُ جرّ») يحتاج **قوائمَ أدواتٍ مصرَّحًا بها**،
والمرجعُ الحاكمُ للقسمة — الشخصيةُ الإسلاميةُ ج٣ — يُعرِّف الأصنافَ ولا يُعطي
قوائمَها. فالقاموسُ يُبنى ههنا أوّلًا من مادّتَين نحويّتَين مختومتَين: مغني
اللبيب لابن هشام، وكتاب سيبويه.

## ما يَحكم هذه الوحدةَ من القيود

1. **الختمُ قبل القراءة.** لا بايتةَ تُفتَح قبل مقابلة الطول والختم معًا،
   و`SealStanding` ثلاثةٌ مغلقة لا رابعَ لها.
2. **النافذةُ مصرَّحٌ بها قبل النظر.** كلُّ استخراجٍ في `THE_EXTRACTIONS`
   يحمل مرساتَه الحرفيّةَ وحدَّه وقاعدةَ فرزه، فلا يُفصَّل بعد رؤية نتيجته.
3. **المجسُّ الذي يقيس صفرًا آلةٌ مبصِرةٌ لا بابٌ معدوم.** المجسّاتُ في
   `THE_PROBES` تُخرِج أعدادَها كما وقعت، والصفرُ يُعرَض صفرًا.
4. **المعلَّقُ صنفٌ أوّل.** بابٌ لم تُصِبه قاعدةٌ يُوسَم `SUSPENDED` ويبقى،
   ولا يُستكمَل من الذاكرة ولا من معجمٍ ثالثٍ بلا تسمية الانتقال.
5. **التعارضُ يُحفَظ بنصَّيه.** عددُ حروف الهجاء المطلوبُ ثمانيةٌ وعشرون،
   والمقيسُ من سيبويه **تسعةٌ وعشرون**؛ يُسجَّل الفرقُ ولا يُحسَم ههنا.

## البايتاتُ ليست في هذه الشجرة، ولمَ ليست

المادّتان النحويّتان منشورتان في مجموعة OpenITI بلا ملفِّ رخصةٍ في مستودعهما،
فإذنُ الإيداع **لم يُفحَص** — ولا يُقرأ ذلك منعًا
(`A_PERMISSION_UNEXAMINED_IS_NOT_A_PERMISSION_REFUSED`). فالمسارُ يُحَلّ
بمتغيّرِ بيئةٍ مسمًّى، أو بموضعِ إيداعٍ مسنونٍ إن نزلت البايتاتُ يومًا، ولا ثالثَ
لهما. ومن لا بايتاتِ عنده لا يخرج له رقمٌ ولا بند: غيابُ المادّة **رفضُ
إخراجٍ** لا قيمةٌ افتراضيّة.

## تسجيلٌ لا سلطة

لا مولدَ ولا تجميدَ ولا استيرادَ من `kernel/`: هذه وحدةُ قياسٍ تُخرِج ما تقرأ،
وحُجّيّةُ بندٍ فيها رتبةُ مادّته لا رتبةُ هذا الملفّ.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

__all__ = [
    "A_CONFLICT_IS_RECORDED_IN_BOTH_TEXTS_AND_NOT_ADJUDICATED_HERE",
    "A_CROSSING_TO_A_SECOND_MATERIAL_IS_NAMED_NOT_SILENT",
    "A_DECLARED_LABEL_IS_NOT_A_NAME_READ_FROM_THE_BYTES",
    "A_DECLARED_LIST_IS_NOT_AN_EXHAUSTIVE_ONE",
    "A_FALSE_ROW_IS_KEPT_FALSE_AND_THE_RULE_IS_NOT_REFITTED",
    "AN_UNVOCALIZED_DEPOSIT_CANNOT_SEPARATE_ANTA_FROM_ANTI",
    "A_PERMISSION_UNEXAMINED_IS_NOT_A_PERMISSION_REFUSED",
    "A_PROBE_THAT_MEASURES_ZERO_IS_A_SIGHTED_INSTRUMENT_NOT_AN_ABSENT_DOOR",
    "A_SEAL_NAMES_WHICH_BYTES_NOT_WHAT_IS_IN_THEM",
    "A_SUSPENDED_ENTRY_IS_FIRST_CLASS_NOT_A_GAP_TO_BE_GUESSED",
    "THE_DEFERRED_LINE",
    "THE_DOORS",
    "THE_EXTRACTIONS",
    "THE_HEARING_CHECK_SAMPLE_SIZE",
    "THE_HEARING_CHECK_SEED",
    "THE_HEARING_CHECK_VERDICTS",
    "THE_LETTER_COUNT_CONFLICT",
    "THE_MINIMUM_GLOSS_WORDS",
    "THE_SUSPENDED_GLOSS",
    "THE_SUSPENDED_OPERATION",
    "THE_WINDOW_CHARACTER_SPAN",
    "THE_MATERIALS",
    "THE_OPERATION_PHRASES",
    "THE_PROBES",
    "THE_WITNESS_CHARACTER_LIMIT",
    "Door",
    "DoorReading",
    "DoorStanding",
    "DeclaredExtraction",
    "DeclaredMaterial",
    "DeclaredProbe",
    "ExtractionRule",
    "LexiconEntry",
    "LexiconMetrics",
    "MaterialRole",
    "NahwLexiconError",
    "ProbeReading",
    "SealReading",
    "SealStanding",
    "door_readings",
    "hearing_check_sample",
    "lexicon_entries",
    "lexicon_metrics",
    "material_path",
    "material_text",
    "probe_readings",
    "report_markdown",
    "report_rows",
    "seal_reading_for",
    "seal_readings",
]


class NahwLexiconError(ValueError):
    """تُرفَع حين يُطلَب بندٌ بلا دليل، أو تُقرأ بايتاتٌ غيرُ المختومة."""


# --- المخلَّفاتُ المسمّاة -----------------------------------------------------


A_PERMISSION_UNEXAMINED_IS_NOT_A_PERMISSION_REFUSED: Final[str] = (
    "APermissionUnexaminedIsNotAPermissionRefused: بايتاتُ المغني وسيبويه ليست "
    "في هذه الشجرة لأنّ إذنَ إيداعها **لم يُفحَص** — لا لأنّه فُحِص فانتفى. "
    "ومستودعُ OpenITI الذي نُشرت فيه لا ملفَّ رخصةٍ فيه، والمتنُ القديمُ كونُه "
    "في الملك العامّ ليس رخصةً معلنةً على نسخةِ الرقمنة. فالمسارُ يُحَلّ "
    "بمتغيّرٍ مسمًّى، والاقتباسُ الحرفيُّ القصيرُ في السجلّ استشهادٌ لا نسخًا."
)

A_SEAL_NAMES_WHICH_BYTES_NOT_WHAT_IS_IN_THEM: Final[str] = (
    "ASealNamesWhichBytesNotWhatIsInThem: مطابقةُ الختم تُثبت **أيَّ** بايتاتٍ "
    "فُتِحت، ولا تُثبت أنّ فيها ما يُطلَب منها. فلكلّ استخراجٍ مرساةٌ حرفيّةٌ "
    "يُشتَرَط وقوعُها في البايتات نفسِها، وغيابُها يُخرِج البابَ معلَّقًا ولو "
    "كان الختمُ مطابقًا."
)

A_PROBE_THAT_MEASURES_ZERO_IS_A_SIGHTED_INSTRUMENT_NOT_AN_ABSENT_DOOR: Final[str] = (
    "AProbeThatMeasuresZeroIsASightedInstrumentNotAnAbsentDoor: «حروف المعاني» "
    "صفرُ مواضعَ في المغني وفي سيبويه معًا، و«حروف النصب» و«حروف الجزم» صفر. "
    "وهذه أصفارٌ **مقيسةٌ بمجسّاتٍ تُصيب غيرَها في المادّة نفسِها**، فتُقرأ خبرًا "
    "عن لفظِ المادّة لا حكمًا بخلوّها من الباب."
)

A_DECLARED_LIST_IS_NOT_AN_EXHAUSTIVE_ONE: Final[str] = (
    "ADeclaredListIsNotAnExhaustiveOne: قائمةٌ مصرَّحةٌ لا مستوفاة. كلُّ ما "
    "ههنا بلغته نافذةٌ مصرَّحٌ بها في بايتاتٍ مختومة؛ وكونُ أدواتِ بابٍ أكثرَ "
    "ممّا أصابته النافذةُ **مرجَّحٌ لا مُستبعَد**، والاستيفاءُ دعوى تحتاج "
    "مادّةً ثانيةً تُختَم وتُفتَح."
)

A_SUSPENDED_ENTRY_IS_FIRST_CLASS_NOT_A_GAP_TO_BE_GUESSED: Final[str] = (
    "ASuspendedEntryIsFirstClassNotAGapToBeGuessed: بابٌ لم تُصِبه قاعدةٌ "
    "يُوسَم `SUSPENDED` ويبقى في التقرير بمجسّاته وأصفارِها. ولا يُستكمَل من "
    "الذاكرة ولا من معجمٍ ثالث: استكمالٌ بلا مادّةٍ مختومةٍ دعوى لا شاهد."
)

A_CONFLICT_IS_RECORDED_IN_BOTH_TEXTS_AND_NOT_ADJUDICATED_HERE: Final[str] = (
    "AConflictIsRecordedInBothTextsAndNotAdjudicatedHere: الطلبُ سمّى حروفَ "
    "الهجاء **ثمانيةً وعشرين**، والمقيسُ من بايتات سيبويه **تسعةٌ وعشرون** — "
    "لأنّه يعُدّ الهمزةَ والألفَ حرفَين. يُسجَّل النصّان معًا ولا يُحسَم ههنا: "
    "حسمُه يحتاج مادّةً حاكمةً تُفتَح، وهي غائبة."
)

A_CROSSING_TO_A_SECOND_MATERIAL_IS_NAMED_NOT_SILENT: Final[str] = (
    "ACrossingToASecondMaterialIsNamedNotSilent: المغني شرحُ أبوابٍ لا فهرسُ "
    "حروف — لم يُصِبه مجسُّ التعداد، وأصابه في سيبويه. فالانتقالُ إلى سيبويه "
    "في الباب الأوّل **مُسمًّى في كلّ صفٍّ** بمادّته، ولا يُقرأ صفٌّ من إحداهما "
    "شاهدًا على الأخرى."
)

AN_UNVOCALIZED_DEPOSIT_CANNOT_SEPARATE_ANTA_FROM_ANTI: Final[str] = (
    "AnUnvocalizedDepositCannotSeparateAntaFromAnti: نصُّ المغني في هذه النسخة "
    "غيرُ مشكول، فقولُه «أنت وأنت وأنتما وأنتم وأنتن» يُخرِج صورتَين "
    "متطابقتَين بايتًا لضميرَين مختلفَين (المذكّر والمؤنّث). فالمكرَّرُ يُطوى "
    "بالصورة ويُعَدّ مرّةً، ويُسجَّل أنّ البايتات لا تفرّق بينهما."
)

A_DECLARED_LABEL_IS_NOT_A_NAME_READ_FROM_THE_BYTES: Final[str] = (
    "ADeclaredLabelIsNotANameReadFromTheBytes: بنودُ قاعدةِ «الجملةِ المرساة» "
    "تحمل اسمًا **مُعلَنًا عندنا** (مثل «ضابط المبني») لا مقروءًا في المادّة؛ "
    "والمقروءُ فيها جملتُها لا عنوانُها. فتُفرَز هذه البنودُ عن بنود التعداد "
    "وفواتحِ الأبواب، إذ أسماءُ تلك واقعةٌ في دليلها بالحرف، واسمُ هذه وسمٌ "
    "منّا على نصٍّ — ومن خلط الوسمَ بالمقروء نسب إلى المادّة ما لم تقله."
)

THE_DEFERRED_LINE: Final[str] = (
    "هذا قاموس أدوات ومصطلحات — لا وسمَ به نصًّا بعد، ولا جسرَ دال/مدلول؛ "
    "كلاهما طور لاحق يستعمل هذا القاموس."
)

THE_WITNESS_CHARACTER_LIMIT: Final[int] = 240
"""حدُّ محارفِ الدليل الحرفيّ؛ اقتباسٌ يُشهَد به لا نسخٌ لمادّةٍ لم يُفحَص إذنُها."""


# --- المواد المُعلَنة وأختامُها ------------------------------------------------


class MaterialRole(Enum):
    """دورُ المادّة في هذا القاموس؛ ولا يُقاس دورٌ على دور."""

    PRIMARY_EXPOSITION = "المادّة الأولى للتأصيل والشرح"
    LETTER_INDEX = "فهرسُ الحروف"
    GOVERNING_CLASSIFICATION = "التصنيفُ الحاكم"


class SealStanding(Enum):
    """حالُ ختمِ مادّة؛ ثلاثةٌ مغلقة، ولا رابعَ يُحمَل عليه المشكوك."""

    SEALED_AND_PRESENT = "مختومٌ حاضر"
    ABSENT_FROM_THIS_TREE = "غائبٌ عن هذه الشجرة"
    SEAL_MISMATCH_HALT = "مخالفةُ ختمٍ — توقُّفٌ فوريّ"


@dataclass(frozen=True, slots=True)
class DeclaredMaterial:
    """مادّةٌ مُعلَنةٌ بمسارها وطولها وختمها؛ ولا تُقرأ قبل مقابلة الثلاثة."""

    key: str
    title: str
    relative_path: str
    path_environment_variable: str
    declared_byte_length: int
    declared_sha256: str
    role: MaterialRole

    def __post_init__(self) -> None:
        if not self.key.strip() or not self.title.strip():
            raise NahwLexiconError("المادّةُ المُعلَنةُ بمفتاحٍ وعنوانٍ غيرِ فارغين.")
        if not self.relative_path.strip():
            raise NahwLexiconError("المادّةُ المُعلَنةُ بمسارٍ نسبيٍّ غيرِ فارغ.")
        if not self.path_environment_variable.strip():
            raise NahwLexiconError("المادّةُ المُعلَنةُ بمتغيّرِ مسارٍ مسمًّى.")
        if self.declared_byte_length <= 0:
            raise NahwLexiconError("طولُ البايتات المُعلَنُ لا يكون غيرَ موجب.")
        if len(self.declared_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.declared_sha256
        ):
            raise NahwLexiconError("الختمُ ليس SHA-256 ستّ عشريّةً كاملة.")


THE_MATERIALS: Final[tuple[DeclaredMaterial, ...]] = (
    DeclaredMaterial(
        key="MUGHNI_LABIB",
        title="مغني اللبيب عن كتب الأعاريب لابن هشام (ت 761هـ)، شاهدُ الشاملة",
        relative_path="corpora/mughni-labib-shamela0006972-ara1.txt",
        path_environment_variable="ALGHANEM_MUGHNI_PATH",
        declared_byte_length=1_486_890,
        declared_sha256=(
            "f37ac2bb4b273f59169053dd0ac2abf50a52846a7e87ddf689ee5c0b87f77e7d"
        ),
        role=MaterialRole.PRIMARY_EXPOSITION,
    ),
    DeclaredMaterial(
        key="KITAB_SIBAWAYH",
        title="كتاب سيبويه (ت 180هـ)، شاهدُ الجامع",
        relative_path="corpora/kitab-sibawayhi-jk006989-ara1.txt",
        path_environment_variable="ALGHANEM_SIBAWAYH_PATH",
        declared_byte_length=2_639_395,
        declared_sha256=(
            "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"
        ),
        role=MaterialRole.LETTER_INDEX,
    ),
    DeclaredMaterial(
        key="SHAKHSIYYA_THREE",
        title="الشخصية الإسلامية، الجزء الثالث — أبحاث اللغة",
        relative_path="الشخصية الاسلامية الجزء الثالث ورد (2).docx",
        path_environment_variable="ALGHANEM_SHAKHSIYYA_THREE_PATH",
        declared_byte_length=673_537,
        declared_sha256=(
            "360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd"
        ),
        role=MaterialRole.GOVERNING_CLASSIFICATION,
    ),
)
"""المواد الثلاث بأختامها؛ والحاكمةُ منها غائبةٌ عن هذه الشجرة فبابُها مقفل."""


@dataclass(frozen=True, slots=True)
class SealReading:
    """قراءةُ ختمٍ عن القرص: ما وُجد وما اشتُقّ، لا ما أُعلِن وحدَه."""

    material: DeclaredMaterial
    standing: SealStanding
    resolved_path: str | None
    measured_byte_length: int | None
    measured_sha256: str | None

    @property
    def is_readable(self) -> bool:
        """أيجوز فتحُ هذه البايتات؟ لا يجوز إلّا عند مطابقةِ الطول والختم."""

        return self.standing is SealStanding.SEALED_AND_PRESENT


def _repository_root() -> Path:
    """جذرُ المستودع، مُشتقًّا من موضع هذه الوحدة لا مكتوبًا مطلقًا."""

    return Path(__file__).resolve().parents[3]


def material_path(material: DeclaredMaterial, root: Path | None = None) -> Path | None:
    """مسارُ مادّةٍ إن حُلَّ إلى ملفٍّ موجود؛ والترتيبُ مسنونٌ ولا ثالثَ له.

    أوّلًا متغيّرُ البيئة المسمّى في المادّة، ثمّ موضعُ الإيداع المسنون تحت
    جذر الشجرة. ومسارٌ لا ملفَّ فيه يُقرأ كأنّه لم يُذكَر.
    """

    declared = os.environ.get(material.path_environment_variable, "").strip()
    if declared:
        candidate = Path(declared)
        if candidate.is_file():
            return candidate
    deposited = (root or _repository_root()) / material.relative_path
    if deposited.is_file():
        return deposited
    return None


def seal_reading_for(
    material: DeclaredMaterial, root: Path | None = None
) -> SealReading:
    """قراءةُ ختمِ مادّةٍ بعينها: يُفتَح مسارُها ويُشتَقّ ختمُها ويُقابَل المُعلَن."""

    path = material_path(material, root)
    if path is None:
        return SealReading(
            material=material,
            standing=SealStanding.ABSENT_FROM_THIS_TREE,
            resolved_path=None,
            measured_byte_length=None,
            measured_sha256=None,
        )
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    matched = (
        len(data) == material.declared_byte_length
        and digest == material.declared_sha256
    )
    return SealReading(
        material=material,
        standing=(
            SealStanding.SEALED_AND_PRESENT
            if matched
            else SealStanding.SEAL_MISMATCH_HALT
        ),
        resolved_path=str(path),
        measured_byte_length=len(data),
        measured_sha256=digest,
    )


def seal_readings(root: Path | None = None) -> tuple[SealReading, ...]:
    """أختامُ المواد الثلاث، مُشتقّةً من البايتات عند كلِّ قراءة."""

    return tuple(seal_reading_for(material, root) for material in THE_MATERIALS)


def _material_by_key(key: str) -> DeclaredMaterial:
    for material in THE_MATERIALS:
        if material.key == key:
            return material
    raise NahwLexiconError(f"لا مادّةَ بهذا المفتاح في السجلّ: {key}")


def material_text(key: str, root: Path | None = None) -> tuple[str, ...] | None:
    """أسطرُ مادّةٍ مختومةٍ حاضرة، أو `None` إن لم تُفتَح بايتاتُها.

    ولا تُفَكّ بايتةٌ قبل مطابقة الطول والختم معًا؛ فالغيابُ ومخالفةُ الختم
    سواءٌ ههنا في المنع، ويفترقان في التقرير.
    """

    reading = seal_reading_for(_material_by_key(key), root)
    if not reading.is_readable:
        return None
    assert reading.resolved_path is not None
    data = Path(reading.resolved_path).read_bytes()
    return tuple(data.decode("utf-8").split("\n"))


# --- المجسّاتُ المصرَّحُ بها قبل النظر -------------------------------------------


@dataclass(frozen=True, slots=True)
class DeclaredProbe:
    """مجسٌّ لفظيٌّ مصرَّحٌ به قبل النظر: عبارةٌ تُعَدّ مواضعُها في مادّةٍ بعينها."""

    door_number: int
    phrase: str
    material_key: str

    def __post_init__(self) -> None:
        if not 1 <= self.door_number <= 8:
            raise NahwLexiconError("رقمُ البابِ بين واحدٍ وثمانية.")
        if not self.phrase.strip():
            raise NahwLexiconError("المجسُّ بعبارةٍ غيرِ فارغة.")


THE_PROBES: Final[tuple[DeclaredProbe, ...]] = (
    DeclaredProbe(1, "حروف العربية", "KITAB_SIBAWAYH"),
    DeclaredProbe(1, "حروف المعجم", "MUGHNI_LABIB"),
    DeclaredProbe(1, "حروف المعجم", "KITAB_SIBAWAYH"),
    DeclaredProbe(2, "حروف المعاني", "MUGHNI_LABIB"),
    DeclaredProbe(2, "حروف المعاني", "KITAB_SIBAWAYH"),
    DeclaredProbe(2, "حروف الجر", "MUGHNI_LABIB"),
    DeclaredProbe(2, "حروف النصب", "MUGHNI_LABIB"),
    DeclaredProbe(2, "حروف الجزم", "MUGHNI_LABIB"),
    DeclaredProbe(2, "حروف العطف", "MUGHNI_LABIB"),
    DeclaredProbe(2, "حروف النفي", "MUGHNI_LABIB"),
    DeclaredProbe(2, "حروف التنبيه", "MUGHNI_LABIB"),
    DeclaredProbe(3, "الأصل في المبني", "MUGHNI_LABIB"),
    DeclaredProbe(3, "أسماء الإشارة", "MUGHNI_LABIB"),
    DeclaredProbe(3, "الأسماء الموصولة", "MUGHNI_LABIB"),
    DeclaredProbe(4, "الضمير المتصل", "MUGHNI_LABIB"),
    DeclaredProbe(4, "الضمير المنفصل", "MUGHNI_LABIB"),
    DeclaredProbe(4, "الضمير", "MUGHNI_LABIB"),
    DeclaredProbe(5, "الفعل الماضي", "MUGHNI_LABIB"),
    DeclaredProbe(5, "الفعل المضارع", "MUGHNI_LABIB"),
    DeclaredProbe(5, "فعل الأمر", "MUGHNI_LABIB"),
    DeclaredProbe(5, "المجرد والمزيد", "MUGHNI_LABIB"),
    DeclaredProbe(6, "فعل يفعل", "MUGHNI_LABIB"),
    DeclaredProbe(6, "فعل يفعل", "KITAB_SIBAWAYH"),
    DeclaredProbe(7, "المفعول به", "MUGHNI_LABIB"),
    DeclaredProbe(7, "المفعول فيه", "MUGHNI_LABIB"),
    DeclaredProbe(7, "المفعول لأجله", "MUGHNI_LABIB"),
    DeclaredProbe(7, "المفعول معه", "MUGHNI_LABIB"),
    DeclaredProbe(7, "التمييز", "MUGHNI_LABIB"),
    DeclaredProbe(7, "البدل", "MUGHNI_LABIB"),
    DeclaredProbe(7, "التوكيد", "MUGHNI_LABIB"),
    DeclaredProbe(8, "الأسماء الخمسة", "MUGHNI_LABIB"),
    DeclaredProbe(8, "الأسماء الستة", "MUGHNI_LABIB"),
    DeclaredProbe(8, "الأسماء الستة", "KITAB_SIBAWAYH"),
)
"""المجسّاتُ الثلاثةُ والثلاثون، مصرَّحةً قبل رؤية أعدادها؛ وصفرُها يُعرَض صفرًا."""


@dataclass(frozen=True, slots=True)
class ProbeReading:
    """قراءةُ مجسٍّ: عددُ مواضعه وأوّلُ سطرٍ أصابه، أو أنّ مادّتَه لم تُفتَح."""

    probe: DeclaredProbe
    material_opened: bool
    occurrences: int
    first_line_number: int | None


def probe_readings(root: Path | None = None) -> tuple[ProbeReading, ...]:
    """أعدادُ المجسّات، مُعادةَ الاشتقاق من البايتات عند كلِّ نداء."""

    cache: dict[str, tuple[str, ...] | None] = {}
    readings: list[ProbeReading] = []
    for probe in THE_PROBES:
        if probe.material_key not in cache:
            cache[probe.material_key] = material_text(probe.material_key, root)
        lines = cache[probe.material_key]
        if lines is None:
            readings.append(
                ProbeReading(
                    probe=probe,
                    material_opened=False,
                    occurrences=0,
                    first_line_number=None,
                )
            )
            continue
        total = 0
        first: int | None = None
        for index, line in enumerate(lines, start=1):
            hits = line.count(probe.phrase)
            if hits and first is None:
                first = index
            total += hits
        readings.append(
            ProbeReading(
                probe=probe,
                material_opened=True,
                occurrences=total,
                first_line_number=first,
            )
        )
    return tuple(readings)


# --- الاستخراجاتُ المصرَّحُ بها ---------------------------------------------


class ExtractionRule(Enum):
    """قواعدُ الاستخراج؛ مغلقةٌ، وكلُّ قاعدةٍ مكتوبةٌ قبل رؤية ما تُخرِج."""

    ENUMERATION_AFTER_ANCHOR = "تعدادٌ يلي مرساةً حرفيّة"
    LETTER_CHAPTER_OPENER = "فاتحةُ بابِ حرفٍ في المغني"
    ANCHOR_SENTENCE = "جملةٌ مرساةٌ تُخرِج بندًا واحدًا"


@dataclass(frozen=True, slots=True)
class DeclaredExtraction:
    """استخراجٌ مصرَّحٌ به: بابُه ومادّتُه ومرساتُه وحدُّه وقاعدةُ فرزه."""

    key: str
    door_number: int
    material_key: str
    rule: ExtractionRule
    anchor: str
    stop: str | None
    pattern: str | None
    entry_name: str | None

    def __post_init__(self) -> None:
        if not 1 <= self.door_number <= 8:
            raise NahwLexiconError("رقمُ البابِ بين واحدٍ وثمانية.")
        if not self.anchor.strip():
            raise NahwLexiconError("الاستخراجُ بمرساةٍ حرفيّةٍ غيرِ فارغة.")
        if self.rule is ExtractionRule.ENUMERATION_AFTER_ANCHOR and not self.pattern:
            raise NahwLexiconError("تعدادٌ بلا قاعدةِ فرزٍ ليس تعدادًا مصرَّحًا.")
        if self.rule is ExtractionRule.ANCHOR_SENTENCE and not self.entry_name:
            raise NahwLexiconError("جملةٌ مرساةٌ بلا اسمِ بندٍ ليست بندًا.")


THE_EXTRACTIONS: Final[tuple[DeclaredExtraction, ...]] = (
    DeclaredExtraction(
        key="SIBAWAYH_LETTER_ENUMERATION",
        door_number=1,
        material_key="KITAB_SIBAWAYH",
        rule=ExtractionRule.ENUMERATION_AFTER_ANCHOR,
        anchor="فأصل حروف العربية تسعة وعشرون حرفا",
        stop="وتكون خمسة",
        pattern=r"(?:(?<=\s)|^)و?(ال[^\s]+)(?=\s|$)",
        entry_name=None,
    ),
    DeclaredExtraction(
        key="MUGHNI_LETTER_CHAPTERS",
        door_number=2,
        material_key="MUGHNI_LABIB",
        rule=ExtractionRule.LETTER_CHAPTER_OPENER,
        anchor="# حرف ال",
        stop=None,
        pattern=None,
        entry_name=None,
    ),
    DeclaredExtraction(
        key="MUGHNI_PARTICLES_NAMED_WITH_THEIR_OPERATION",
        door_number=2,
        material_key="MUGHNI_LABIB",
        rule=ExtractionRule.ENUMERATION_AFTER_ANCHOR,
        anchor="وإن كان المبحوث فيه حرفا بين نوعه ومعناه وعمله",
        stop="ثم بعد الكلام",
        pattern=r"(?:(?<=\s)|^)(إن|لن|أن|لم)(?= حرف )",
        entry_name=None,
    ),
    DeclaredExtraction(
        key="MUGHNI_BUILT_FORM_RULE",
        door_number=3,
        material_key="MUGHNI_LABIB",
        rule=ExtractionRule.ANCHOR_SENTENCE,
        anchor="الأصل في المبني ألا تختلف صيغة",
        stop="وعكسه",
        pattern=None,
        entry_name="ضابط المبني",
    ),
    DeclaredExtraction(
        key="MUGHNI_DETACHED_ADDRESSEE_PRONOUNS",
        door_number=4,
        material_key="MUGHNI_LABIB",
        rule=ExtractionRule.ENUMERATION_AFTER_ANCHOR,
        anchor="وضمير المخاطب في قولك",
        stop="على قول الجمهور",
        pattern=r"(?:(?<=\s)|^)و?(أنت(?:ما|م|ن)?)(?=\s|$)",
        entry_name=None,
    ),
    DeclaredExtraction(
        key="MUGHNI_SIGNS_OF_THE_THREE_KINDS",
        door_number=5,
        material_key="MUGHNI_LABIB",
        rule=ExtractionRule.ENUMERATION_AFTER_ANCHOR,
        anchor="ومثاله أنه إذا سمع أن",
        stop="سبق وهمه",
        pattern=r"(?:(?<=\s)|^)(أل|أحرف نأيت|تاء الخطاب)(?= من علامات )",
        entry_name=None,
    ),
    DeclaredExtraction(
        key="MUGHNI_OBJECT_POSITIONS",
        door_number=7,
        material_key="MUGHNI_LABIB",
        rule=ExtractionRule.ENUMERATION_AFTER_ANCHOR,
        anchor="فتخرج بقية المفاعيل",
        stop="أنهن في",
        pattern=r"(المفعول (?:به|معه|فيه|لأجله))",
        entry_name=None,
    ),
)
"""الاستخراجاتُ السبعة؛ وما لم يُصِبه استخراجٌ بقي بابُه معلَّقًا بمجسّاته."""


THE_OPERATION_PHRASES: Final[tuple[str, ...]] = (
    "حرف جر",
    "حرف عطف",
    "حرف نصب",
    "حرف جزم",
    "حرف توكيد",
    "حرف نفي",
    "حرف مصدري",
    "حرف استفهام",
    "حرف خطاب",
    "حرف مهمل",
    "حرف تصديق",
    "حرف شرط",
    "حرف استفتاح",
    "حرف تفسير",
    "اسم فعل",
    "اسم ملازم للاضافة",
    "ظرف زمان",
    "ظرف مكان",
    "ينصب الفعل المضارع",
    "يجزم المضارع",
    "تنصب الاسم وترفع الخبر",
    "نفي ونصب واستقبال",
)
"""عباراتُ العمل المصرَّحُ بها؛ ما لم تُصِب واحدةٌ منها فالعملُ معلَّقٌ لا مُخمَّن."""

THE_SUSPENDED_OPERATION: Final[str] = "معلق — العمل غير مصرَّح في هذه النافذة"
THE_SUSPENDED_GLOSS: Final[str] = "معلق — لا تعريف في هذه النافذة"

THE_WINDOW_CHARACTER_SPAN: Final[int] = 1_200
"""طولُ النافذةِ محارفَ بعد المرساة؛ مسنونٌ قبل النظر ولا يُوسَّع بعد نتيجته.

والوصلُ قبل الالتماسِ ضرورةٌ لا زينة: النصُّ الخامُّ يقطع الجملةَ الواحدةَ على
أسطرٍ بعلامةِ استمرارٍ (`~~`)، فمرساةٌ تُلتَمَس في سطرٍ واحدٍ تُخطئ جملةً حاضرةً
بتمامها.
"""

THE_MINIMUM_GLOSS_WORDS: Final[int] = 3
"""أقلُّ ما يُعَدّ تعريفًا بعد الاسم؛ وما دونه يُوسَم معلَّقًا لا يُلفَّق."""


@dataclass(frozen=True, slots=True)
class LexiconEntry:
    """بندُ قاموس: بابُه واسمُه وتعريفُه وعملُه ودليلُه الحرفيُّ وموضعُه ومادّتُه."""

    door_number: int
    door_title: str
    extraction_key: str
    name: str
    gloss: str
    operation: str
    witness: str
    line_number: int
    material_key: str
    material_sha256: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise NahwLexiconError("بندٌ بلا اسمٍ ليس بندًا.")
        if not self.witness.strip():
            raise NahwLexiconError("بندٌ بلا دليلٍ حرفيٍّ دعوى لا شاهد؛ ولا يُقبَل ههنا.")
        if self.line_number <= 0:
            raise NahwLexiconError("موضعُ البندِ سطرٌ موجبٌ في النصّ الخام.")


def _clean(text: str) -> str:
    """تنقيةُ سطرٍ من علاماتِ الناشر الظاهرةِ في البايتات، لا من كلماتِه."""

    stripped = text.replace("~~", " ").replace("#", " ")
    stripped = re.sub(r"\bms\d+\b", " ", stripped)
    stripped = re.sub(r"\bPageV\d+P\d+\b", " ", stripped)
    return re.sub(r"\s+", " ", stripped).strip()


def _clip(text: str) -> str:
    return (
        text
        if len(text) <= THE_WITNESS_CHARACTER_LIMIT
        else (text[:THE_WITNESS_CHARACTER_LIMIT].rstrip() + "…")
    )


def _strip_leading_waw(token: str) -> str:
    """طيُّ واوِ العطفِ عن أوّل الاسم؛ والواوُ ههنا وصلُ سياقٍ لا حرفٌ من الاسم."""

    return token[1:] if len(token) > 2 and token.startswith("و") else token


def _operation_in(text: str) -> str:
    for phrase in THE_OPERATION_PHRASES:
        if phrase in text:
            return phrase
    return THE_SUSPENDED_OPERATION


def _cleaned_corpus(lines: tuple[str, ...]) -> tuple[str, tuple[int, ...]]:
    """النصُّ مُنقًّى موصولًا، ومعه إزاحةُ بدايةِ كلِّ سطرٍ فيه ليُرَدّ الموضعُ سطرًا."""

    offsets: list[int] = []
    pieces: list[str] = []
    position = 0
    for line in lines:
        cleaned = _clean(line)
        offsets.append(position)
        pieces.append(cleaned)
        position += len(cleaned) + 1
    return " ".join(pieces), tuple(offsets)


def _line_number_at(offsets: tuple[int, ...], position: int) -> int:
    low, high = 0, len(offsets) - 1
    while low < high:
        middle = (low + high + 1) // 2
        if offsets[middle] <= position:
            low = middle
        else:
            high = middle - 1
    return low + 1


def _window_for(
    lines: tuple[str, ...], extraction: DeclaredExtraction
) -> tuple[str, int] | None:
    """نافذةُ استخراجٍ: من مرساتِه الحرفيّة إلى حدِّه، مع رقمِ سطرِ المرساة.

    والالتماسُ يقع في النصِّ **موصولًا مُنقًّى** لا سطرًا سطرًا، لأنّ النصّ
    الخامَّ يقطع الجملةَ الواحدةَ على أسطرٍ بعلامةِ استمرار.
    """

    corpus, offsets = _cleaned_corpus(lines)
    position = corpus.find(extraction.anchor)
    if position < 0:
        return None
    window = corpus[position : position + THE_WINDOW_CHARACTER_SPAN]
    if extraction.stop:
        end = window.find(extraction.stop, len(extraction.anchor))
        if end > 0:
            window = window[:end]
    return window.strip(), _line_number_at(offsets, position)


def _entries_for(
    extraction: DeclaredExtraction,
    lines: tuple[str, ...],
    door_title: str,
    material_sha256: str,
) -> tuple[LexiconEntry, ...]:
    if extraction.rule is ExtractionRule.LETTER_CHAPTER_OPENER:
        entries: list[LexiconEntry] = []
        for index, line in enumerate(lines):
            if not line.startswith(extraction.anchor):
                continue
            for offset in range(index + 1, min(index + 6, len(lines))):
                if not lines[offset].startswith("# "):
                    continue
                opener = _clean(lines[offset])
                if not opener:
                    break
                entries.append(
                    LexiconEntry(
                        door_number=extraction.door_number,
                        door_title=door_title,
                        extraction_key=extraction.key,
                        name=_strip_leading_waw(opener.split(" ")[0]),
                        gloss=_clip(opener),
                        operation=_operation_in(opener),
                        witness=_clip(f"{_clean(line)} | {opener}"),
                        line_number=offset + 1,
                        material_key=extraction.material_key,
                        material_sha256=material_sha256,
                    )
                )
                break
        return tuple(entries)

    window = _window_for(lines, extraction)
    if window is None:
        return ()
    text, line_number = window

    if extraction.rule is ExtractionRule.ANCHOR_SENTENCE:
        assert extraction.entry_name is not None
        return (
            LexiconEntry(
                door_number=extraction.door_number,
                door_title=door_title,
                extraction_key=extraction.key,
                name=extraction.entry_name,
                gloss=_clip(text),
                operation=_operation_in(text),
                witness=_clip(text),
                line_number=line_number,
                material_key=extraction.material_key,
                material_sha256=material_sha256,
            ),
        )

    assert extraction.pattern is not None
    body = text[len(extraction.anchor) :]
    found: list[tuple[str, int, int]] = []
    for match in re.finditer(extraction.pattern, body):
        if any(name == match.group(1) for name, _, _ in found):
            continue
        found.append((match.group(1), match.start(1), match.end(1)))
    entries = []
    for position, (name, start, end) in enumerate(found):
        boundary = found[position + 1][1] if position + 1 < len(found) else len(body)
        segment = body[start:boundary].strip()
        tail = body[end:boundary].strip()
        entries.append(
            LexiconEntry(
                door_number=extraction.door_number,
                door_title=door_title,
                extraction_key=extraction.key,
                name=name,
                gloss=(
                    _clip(segment)
                    if len(tail.split(" ")) >= THE_MINIMUM_GLOSS_WORDS
                    else THE_SUSPENDED_GLOSS
                ),
                operation=_operation_in(segment),
                witness=_clip(text),
                line_number=line_number,
                material_key=extraction.material_key,
                material_sha256=material_sha256,
            )
        )
    return tuple(entries)


# --- الأبوابُ الثمانية ---------------------------------------------------------


class DoorStanding(Enum):
    """حالُ بابٍ؛ ثلاثةٌ مغلقة، والمعلَّقُ منها صنفٌ أوّلٌ لا فراغ."""

    CLOSED = "مقفول"
    PARTIAL = "جزئي"
    SUSPENDED = "معلق"


@dataclass(frozen=True, slots=True)
class Door:
    """بابٌ من الأبواب الثمانية: رقمُه وعنوانُه وما يُطلَب منه."""

    number: int
    title: str
    demand: str


THE_DOORS: Final[tuple[Door, ...]] = (
    Door(1, "أسماء حروف الهجاء", "قائمةُ أسماء الحروف بتعدادٍ مصرَّحٍ به"),
    Door(2, "حروف المعاني مقسّمةً بعملها", "كلُّ حرفٍ باسمه وعمله من بابه"),
    Door(3, "المبنيات من الأسماء والأفعال", "ضابطُ البناء وقوائمُ المبنيّات"),
    Door(4, "الضمائر متّصلةً ومنفصلة", "صيغُ المتكلّم والمخاطب والغائب"),
    Door(5, "أحوال الفعل والمجرّد والمزيد", "الماضي والمضارع والأمر وعلاماتُها"),
    Door(6, "الأوزان: فعَل يفعِل وأخواتها", "أمثلةُ الأبواب كما تصرّح بها المادّة"),
    Door(7, "الإعراب والمواقع", "لكلّ موقعٍ تعريفُه وعلامتُه"),
    Door(8, "الأسماء الخمسة/الستة", "إن صرّحت المادّةُ، وإلّا معلَّقٌ مسمًّى"),
)
"""الأبوابُ الثمانيةُ بعناوينها؛ وحالُ كلٍّ يُشتَقّ من قرصٍ لا يُكتَب سلفًا."""


THE_LETTER_COUNT_CONFLICT: Final[tuple[str, str]] = (
    "الطلب: أسماء حروف الهجاء الثمانية والعشرون",
    "سيبويه: فأصل حروف العربية تسعة وعشرون حرفا الهمزة والألف والهاء…",
)
"""طرفا التعارض في عدد الحروف، منقولَين بنصّيهما وغيرَ محسومَين ههنا."""


def lexicon_entries(root: Path | None = None) -> tuple[LexiconEntry, ...]:
    """بنودُ القاموس كلُّها، مُعادةَ الاشتقاق من البايتات المختومة عند كلِّ نداء."""

    titles = {door.number: door.title for door in THE_DOORS}
    seals = {reading.material.key: reading for reading in seal_readings(root)}
    cache: dict[str, tuple[str, ...] | None] = {}
    entries: list[LexiconEntry] = []
    for extraction in THE_EXTRACTIONS:
        if extraction.material_key not in cache:
            cache[extraction.material_key] = material_text(
                extraction.material_key, root
            )
        lines = cache[extraction.material_key]
        if lines is None:
            continue
        seal = seals[extraction.material_key]
        assert seal.measured_sha256 is not None
        entries.extend(
            _entries_for(
                extraction,
                lines,
                titles[extraction.door_number],
                seal.measured_sha256,
            )
        )
    return tuple(entries)


@dataclass(frozen=True, slots=True)
class DoorReading:
    """حالُ بابٍ بأرقامه الخام: عددُ بنوده وما دُلّ عليه منها ومجسّاتُه."""

    door: Door
    standing: DoorStanding
    entry_count: int
    witnessed_count: int
    glossed_count: int
    operation_count: int
    probe_total: int


def door_readings(root: Path | None = None) -> tuple[DoorReading, ...]:
    """حالُ الأبواب الثمانية، مُشتقًّا من البنود والمجسّات لا مكتوبًا سلفًا.

    والقاعدةُ مصرَّحٌ بها قبل النظر: بابٌ بلا بندٍ `SUSPENDED`؛ وبابٌ كلُّ بنوده
    مدلَّلٌ عليها وموسومةٌ بعملٍ وتعريفٍ مصرَّحَين `CLOSED`؛ وما بينهما `PARTIAL`.
    """

    entries = lexicon_entries(root)
    probes = probe_readings(root)
    readings: list[DoorReading] = []
    for door in THE_DOORS:
        mine = [entry for entry in entries if entry.door_number == door.number]
        witnessed = sum(1 for entry in mine if entry.witness.strip())
        glossed = sum(1 for entry in mine if entry.gloss != THE_SUSPENDED_GLOSS)
        operated = sum(
            1 for entry in mine if entry.operation != THE_SUSPENDED_OPERATION
        )
        probe_total = sum(
            reading.occurrences
            for reading in probes
            if reading.probe.door_number == door.number
        )
        if not mine:
            standing = DoorStanding.SUSPENDED
        elif witnessed == len(mine) == glossed == operated:
            standing = DoorStanding.CLOSED
        else:
            standing = DoorStanding.PARTIAL
        readings.append(
            DoorReading(
                door=door,
                standing=standing,
                entry_count=len(mine),
                witnessed_count=witnessed,
                glossed_count=glossed,
                operation_count=operated,
                probe_total=probe_total,
            )
        )
    return tuple(readings)


# --- فحصُ السمع ---------------------------------------------------------------


THE_HEARING_CHECK_SAMPLE_SIZE: Final[int] = 12
"""حجمُ عيّنةِ فحص السمع، مسمًّى قبل رؤية البنود؛ لا يُوسَّع بعد نتيجته."""

THE_HEARING_CHECK_SEED: Final[int] = 761
"""بذرةُ الاختيار — سنةُ وفاةِ ابن هشام — مسمّاةٌ ليُعاد الاختيارُ نفسُه بها."""


def hearing_check_sample(root: Path | None = None) -> tuple[LexiconEntry, ...]:
    """عيّنةُ فحص السمع: اختيارٌ حتميٌّ ببذرةٍ مسمّاةٍ لا عشوائيٌّ بلا إعادة."""

    import random

    entries = lexicon_entries(root)
    if len(entries) <= THE_HEARING_CHECK_SAMPLE_SIZE:
        return entries
    chooser = random.Random(THE_HEARING_CHECK_SEED)
    picked = chooser.sample(range(len(entries)), THE_HEARING_CHECK_SAMPLE_SIZE)
    return tuple(entries[index] for index in sorted(picked))


THE_HEARING_CHECK_VERDICTS: Final[tuple[tuple[str, bool, str], ...]] = (
    (
        "SIBAWAYH_LETTER_ENUMERATION::الكاف",
        True,
        "الاسمُ في تعداد سيبويه بنصّه، والدليلُ يحمله؛ والتعريفُ معلَّقٌ لأنّ "
        "التعدادَ لا يُعرِّف، وذلك خبرٌ عن المادّة لا نقصٌ في الصفّ.",
    ),
    (
        "SIBAWAYH_LETTER_ENUMERATION::اللام",
        True,
        "في التعداد بنصّه، ولا لبسَ في صورته.",
    ),
    (
        "SIBAWAYH_LETTER_ENUMERATION::الطاء",
        True,
        "في التعداد بنصّه، ولا لبسَ في صورته.",
    ),
    (
        "SIBAWAYH_LETTER_ENUMERATION::الزاي",
        True,
        "في التعداد بنصّه، ولا لبسَ في صورته.",
    ),
    (
        "SIBAWAYH_LETTER_ENUMERATION::السين",
        True,
        "في التعداد بنصّه؛ ويُنبَّه أنّ «السين» في الباب الثاني بندٌ آخرُ من "
        "مادّةٍ أخرى، والاتّحادُ في الصورة ليس اتّحادًا في البند.",
    ),
    (
        "SIBAWAYH_LETTER_ENUMERATION::الواو",
        True,
        "آخرُ أسماء التعداد، وحدُّ النافذة وقع بعده لا قبله.",
    ),
    (
        "MUGHNI_LETTER_CHAPTERS::السين",
        True,
        "فاتحةُ باب السين بنصّها، والتعريفُ منها. والعملُ خرج معلَّقًا لأنّ "
        "«حرف يختص بالمضارع» ليست من عبارات العمل المصرَّح بها — وذلك حدُّ "
        "النافذة لا خطأٌ في الصفّ.",
    ),
    (
        "MUGHNI_LETTER_CHAPTERS::غير",
        True,
        "«غير اسم ملازم للاضافة» — الاسمُ والتعريفُ والعملُ ثلاثتُها في الدليل.",
    ),
    (
        "MUGHNI_LETTER_CHAPTERS::المراد",
        False,
        "صفٌّ كاذبٌ يُحفَظ كاذبًا: «المراد» ليست أداةً، وإنّما وقعت فاتحةَ باب "
        "الألف الهاوية استئنافًا («والمراد هنا الحرف الهاوي…»). فقاعدةُ "
        "الفاتحة أصابت أوّلَ كلمةٍ لا أوّلَ أداة — وهي عينُ سابقة «البنية "
        "بلا دلالة»، ولا تُعدَّل القاعدةُ بعد رؤية نتيجتها.",
    ),
    (
        "MUGHNI_BUILT_FORM_RULE::ضابط المبني",
        True,
        "«الأصل في المبني ألا تختلف صيغة» — الضابطُ بنصّه، وهو المطلوبُ في بابه.",
    ),
    (
        "MUGHNI_SIGNS_OF_THE_THREE_KINDS::أحرف نأيت",
        True,
        "«وأن أحرف نأيت من علامات المضارع» — علامةٌ مصرَّحٌ بها في الدليل نفسِه.",
    ),
    (
        "MUGHNI_OBJECT_POSITIONS::المفعول فيه",
        True,
        "الموقعُ مذكورٌ باسمه في الدليل؛ وتعريفُه معلَّقٌ فيه لأنّ الموضعَ "
        "يَعُدّ المفاعيلَ ولا يحدّها، فلا يُلفَّق له حدٌّ من خارجها.",
    ),
)
"""شهاداتُ فحص السمع مكتوبةً بندًا بندًا، اثنتا عشرةَ شهادةً بأسبابها.

وهذه **شهادةُ عينٍ مُودَعة** لا رقمٌ يُعاد اشتقاقه: المنفّذُ يُعيد اختيارَ
العيّنة نفسِها بالبذرة المسمّاة، ولا يُعيد الحكمَ عليها. فتُعرَض بأسبابها
ليُصادَمَ الحكمُ فيها بالدليل نفسِه، والساقطُ منها معروضٌ ساقطًا.
"""


A_FALSE_ROW_IS_KEPT_FALSE_AND_THE_RULE_IS_NOT_REFITTED: Final[str] = (
    "AFalseRowIsKeptFalseAndTheRuleIsNotRefitted: أصابت قاعدةُ فاتحة الباب "
    "كلمةَ «المراد» في باب الألف الهاوية فأخرجتها أداةً، وهي ليست أداة. "
    "ويبقى الصفُّ في السجلّ كاذبًا مُعلَنًا، ولا تُضيَّق القاعدةُ بعد رؤية "
    "نتيجتها: تضييقُها ههنا تفصيلُ قاعدةٍ على مخرَجها، وهو ما تمنعه هذه الشجرة."
)


# --- المقاييسُ والتقرير --------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LexiconMetrics:
    """أرقامُ التقرير الخام؛ والساقطُ منها يُعرَض ساقطًا."""

    materials_sealed_and_present: int
    materials_absent: int
    entry_count: int
    witnessed_count: int
    glossed_count: int
    operation_count: int
    doors_closed: int
    doors_partial: int
    doors_suspended: int
    probes_declared: int
    probes_measuring_zero: int
    hearing_sample_size: int
    hearing_sample_sound: int

    @property
    def witness_ratio(self) -> float:
        """نسبةُ البنود المدلَّل عليها؛ وواحدٌ ليس ادّعاءً بل حدُّ العقد."""

        if not self.entry_count:
            return 0.0
        return self.witnessed_count / self.entry_count

    @property
    def hearing_soundness(self) -> float:
        """نسبةُ صدقِ عيّنةِ فحص السمع، بعتبةٍ لا تُحسَّن بعد رؤيتها."""

        if not self.hearing_sample_size:
            return 0.0
        return self.hearing_sample_sound / self.hearing_sample_size


def lexicon_metrics(root: Path | None = None) -> LexiconMetrics:
    """المقاييسُ كلُّها، مُعادةَ الاشتقاق من القرص لا منقولةً من عرض."""

    seals = seal_readings(root)
    entries = lexicon_entries(root)
    doors = door_readings(root)
    probes = probe_readings(root)
    sample = hearing_check_sample(root)
    sample_keys = {f"{entry.extraction_key}::{entry.name}" for entry in sample}
    sound = sum(
        1
        for key, verdict, _ in THE_HEARING_CHECK_VERDICTS
        if verdict and key in sample_keys
    )
    return LexiconMetrics(
        materials_sealed_and_present=sum(1 for seal in seals if seal.is_readable),
        materials_absent=sum(
            1 for seal in seals if seal.standing is SealStanding.ABSENT_FROM_THIS_TREE
        ),
        entry_count=len(entries),
        witnessed_count=sum(1 for entry in entries if entry.witness.strip()),
        glossed_count=sum(1 for entry in entries if entry.gloss != THE_SUSPENDED_GLOSS),
        operation_count=sum(
            1 for entry in entries if entry.operation != THE_SUSPENDED_OPERATION
        ),
        doors_closed=sum(1 for door in doors if door.standing is DoorStanding.CLOSED),
        doors_partial=sum(1 for door in doors if door.standing is DoorStanding.PARTIAL),
        doors_suspended=sum(
            1 for door in doors if door.standing is DoorStanding.SUSPENDED
        ),
        probes_declared=len(probes),
        probes_measuring_zero=sum(
            1 for probe in probes if probe.material_opened and not probe.occurrences
        ),
        hearing_sample_size=len(sample),
        hearing_sample_sound=sound,
    )


def report_rows(root: Path | None = None) -> tuple[dict[str, object], ...]:
    """صفوفُ `nahw_lexicon.jsonl`: بندٌ في كلّ سطرٍ بأركانه السبعة."""

    return tuple(
        {
            "الباب": f"{entry.door_number} — {entry.door_title}",
            "الاسم": entry.name,
            "التعريف المختصر": entry.gloss,
            "العمل": entry.operation,
            "الدليل الحرفي": entry.witness,
            "الموضع": f"سطر {entry.line_number} من النصّ الخام",
            "المادة المختومة": entry.material_key,
            "ختم المادة": entry.material_sha256,
            "قاعدة الاستخراج": entry.extraction_key,
        }
        for entry in lexicon_entries(root)
    )


def report_markdown(root: Path | None = None) -> str:
    """نصُّ `LEXICON-REPORT.md` كاملًا، مولَّدًا من القرص لا منقولًا إليه."""

    seals = seal_readings(root)
    doors = door_readings(root)
    probes = probe_readings(root)
    metrics = lexicon_metrics(root)
    lines: list[str] = [
        "# قاموس مصطلحات النحو — المرحلة صفر لجسر الدالّ/المدلول",
        "",
        "> هذا الملفُّ **مولَّدٌ** بـ`python tools/lexicon_extract.py`؛ لا يُحرَّر "
        "بيدٍ، وكلُّ رقمٍ فيه يعيده من يشغّل المنفّذ على المواد المختومة نفسِها.",
        "",
        "## المواد وأختامُها",
        "",
        "| المادّة | الدور | الحال | الطول المقيس | الختم المقيس |",
        "| --- | --- | --- | --- | --- |",
    ]
    for seal in seals:
        length = (
            f"{seal.measured_byte_length:,}"
            if seal.measured_byte_length is not None
            else "—"
        )
        digest = (
            f"`{seal.measured_sha256[:12]}…`"
            if seal.measured_sha256 is not None
            else "—"
        )
        lines.append(
            f"| {seal.material.title} | {seal.material.role.value} | "
            f"{seal.standing.value} | {length} | {digest} |"
        )
    lines += [
        "",
        "## الأبواب الثمانية وحالُ كلٍّ",
        "",
        "| # | الباب | الحال | البنود | المدلَّل عليها | المعرَّفة | الموسومة بعمل |"
        " مجموع المجسّات |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for reading in doors:
        lines.append(
            f"| {reading.door.number} | {reading.door.title} | "
            f"{reading.standing.value} | {reading.entry_count} | "
            f"{reading.witnessed_count} | {reading.glossed_count} | "
            f"{reading.operation_count} | {reading.probe_total} |"
        )
    lines += [
        "",
        "## المجسّات المصرَّح بها قبل النظر",
        "",
        "| الباب | المجسّ | المادّة | المواضع | أوّل سطر |",
        "| --- | --- | --- | --- | --- |",
    ]
    for probe in probes:
        where = (
            str(probe.first_line_number) if probe.first_line_number is not None else "—"
        )
        count = str(probe.occurrences) if probe.material_opened else "مادّة لم تُفتَح"
        lines.append(
            f"| {probe.probe.door_number} | {probe.probe.phrase} | "
            f"{probe.probe.material_key} | {count} | {where} |"
        )
    lines += [
        "",
        "## الأرقام الخام",
        "",
        f"- مواد مختومة حاضرة: **{metrics.materials_sealed_and_present}** من "
        f"{len(THE_MATERIALS)}؛ غائبة: **{metrics.materials_absent}**.",
        f"- عدد البنود: **{metrics.entry_count}**.",
        f"- المدلَّل عليها بدليلٍ حرفيّ: **{metrics.witnessed_count}** "
        f"({metrics.witness_ratio:.1%}).",
        f"- المعرَّفة بتعريفٍ مصرَّح: **{metrics.glossed_count}**؛ "
        f"الموسومة بعملٍ مصرَّح: **{metrics.operation_count}**.",
        f"- الأبواب: مقفول **{metrics.doors_closed}**، جزئي "
        f"**{metrics.doors_partial}**، معلق **{metrics.doors_suspended}**.",
        f"- المجسّات المصرَّحة: **{metrics.probes_declared}**، منها ما قاس صفرًا "
        f"على مادّةٍ مفتوحة: **{metrics.probes_measuring_zero}**.",
        f"- عيّنة فحص السمع: **{metrics.hearing_sample_size}** بندًا، "
        f"الصادق منها **{metrics.hearing_sample_sound}** "
        f"({metrics.hearing_soundness:.1%}).",
        "",
        "## التعارض، محفوظًا بنصَّيه",
        "",
        f"- {THE_LETTER_COUNT_CONFLICT[0]}",
        f"- {THE_LETTER_COUNT_CONFLICT[1]}",
        "",
        A_CONFLICT_IS_RECORDED_IN_BOTH_TEXTS_AND_NOT_ADJUDICATED_HERE,
        "",
        "## ما يُقرأ قبل أيّ رقمٍ ههنا",
        "",
        f"- {A_DECLARED_LIST_IS_NOT_AN_EXHAUSTIVE_ONE}",
        f"- {A_PROBE_THAT_MEASURES_ZERO_IS_A_SIGHTED_INSTRUMENT_NOT_AN_ABSENT_DOOR}",
        f"- {A_SUSPENDED_ENTRY_IS_FIRST_CLASS_NOT_A_GAP_TO_BE_GUESSED}",
        f"- {A_FALSE_ROW_IS_KEPT_FALSE_AND_THE_RULE_IS_NOT_REFITTED}",
        f"- {A_CROSSING_TO_A_SECOND_MATERIAL_IS_NAMED_NOT_SILENT}",
        f"- {A_DECLARED_LABEL_IS_NOT_A_NAME_READ_FROM_THE_BYTES}",
        f"- {AN_UNVOCALIZED_DEPOSIT_CANNOT_SEPARATE_ANTA_FROM_ANTI}",
        f"- {A_SEAL_NAMES_WHICH_BYTES_NOT_WHAT_IS_IN_THEM}",
        f"- {A_PERMISSION_UNEXAMINED_IS_NOT_A_PERMISSION_REFUSED}",
        "",
        "## سطر التأجيل",
        "",
        f"> {THE_DEFERRED_LINE}",
        "",
    ]
    return "\n".join(lines)
