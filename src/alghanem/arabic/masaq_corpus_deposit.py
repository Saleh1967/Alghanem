"""إيداعُ مدوَّنة MASAQ شاهدًا مُبصَّمًا، وعشرون رقمًا كلُّ رقمٍ بقاعدة عدّه.

**ما تفعله هذه الوحدة**: تُجمِّد بصمةَ `MASAQ.csv` وطولَ بايتاتها ورخصتَها
وشرطَ إسنادها، ثمّ تُودِع عشرين رقمًا يحمل كلٌّ منها **قاعدةَ عدّه ودالّةَ
إعادة اشتقاقه**، وترفض إخراجَ رقمٍ من بايتاتٍ لا تطابق البصمةَ والطول. ولا
تُنسَخ البايتاتُ إلى الشجرة، وإن كانت الرخصةُ تُجيز.

`WHAT_QAC_COULD_NOT_CLOSE`: المدوَّنةُ الصرفيةُ للقرآن تَسِم `VN` ولا تنزل تحته،
فبقيت أبوابُ المشتقّات **مُرشَّحةً بلا مرجِع**. و MASAQ تَسِمها بأسمائها
(`GERUND`، `GERUND_MEEM`، `NOUN_ACTIVE_PART`، `ADJ_QUALIT`، …)، فصارت
**قابلةً للقياس على وَسْمٍ بشريّ**. وليست بذلك مُتبنّاةً دعوى في العربية:
حدُّها مكتوبٌ في `CompleteInductionIsCorpusBounded` أدناه.

`A_COUNT_IS_RELATIVE_TO_ITS_COUNTING_RULE`: تنطبق هنا مرّتين في موضعٍ واحد.
`data.decode("utf-8-sig").splitlines()` يُعطي ١٥٧٬٨٥٤، و
`list(csv.DictReader(...))` يُعطي ١٥٧٬٦٧٧؛ والعددان صحيحان كلٌّ تحت قاعدته،
والفرقُ **مقيسٌ لا مُقدَّر**: صفُّ ترويسةٍ واحد، و١٧٦ فاصلَ سطرٍ داخل حقولٍ
مُقتبَسة موزَّعةً على ١٥٤ سجلًّا. وهذا ما يُثبته `CONSERVATION_OF_LINES` ولا
يزيد.

`WORD_NO_IS_A_SEGMENT_INDEX`: `Word_No` فهرسُ **مقطعٍ داخل كلمة** لا فهرسُ
كلمة، ومفتاحُ الكلمة `Column5`. وليس هذا تجميلًا: الخلطُ بينهما أهبط قياسَ
دقّةٍ من ٢٣٫٣٪ إلى ٠٫٣٪ قبل أن يُمسَك، فالواقعةُ مُثبَتةٌ في اختبارٍ لا في
تعليق.

`THE_WITNESS_CAUGHT_A_DEFECT_ON_ITS_FIRST_RUN`: أوّلُ تشغيلٍ لدالّة إعادة
الاشتقاق أعطى `embedded_newline_records = 0` مقابل ١٥٤ مُودَعة. والعلّةُ في
**الدالّة لا في الإيداع**: `splitlines()` كان قد شقَّ فواصلَ الأسطر الداخليّة
قبل أن يراها `csv.reader`، فلم يبقَ حقلٌ يحمل فاصلًا. فأُصلِحت بالقراءة عبر
`io.StringIO`، ويمنع الرجوعَ اختبارٌ مُسمًّى. فرقمٌ مُنِع من أن يستقرّ صامتًا.

`NO_ROOT_COLUMN_SO_NO_CROSS_CORPUS_FIGURE`: ليس في MASAQ عمودُ جذر. فربطُها
بالمدوَّنة الصرفية أو بـ«مقاييس اللغة» ربطٌ **موضعيّ** `(سورة، آية، كلمة)` لا
ربطٌ بالجذر؛ ومن هناك جاء فشلُ المحاذاة المذكور. فلا يُودَع في هذه الوحدة رقمٌ
عابرٌ للمدوَّنات البتّة: المُودَعُ كلُّه عددٌ في مدوَّنةٍ واحدة.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.

`THE_READY_PATH_IS_THE_MASAQ_WITNESS_PATH_NOT_PROGRAMME_COMPLETION`: ما اكتمل
هنا **مسارُ شاهدٍ واحد** لا بناءُ البرنامج. فمحورُ بناء البرنامج — القوانين
والبوّابات والأدلّة والرتب والغايات — مستقلٌّ عن محور **دورة حياة الشاهد
التجريبيّ**، ودمجُهما يجعل «تقدُّمَ البرنامج» و«توفُّرَ الدليل» شيئًا واحدًا
وهما اثنان. و`REDERIVATION_IS_COMPARISON_NOT_AUTOMATIC_ENDORSEMENT` يقفل الباب
الثاني: نزولُ البايتات يُشغِّل المقارنة ولا يُصدِّق ما جُمِّد قبلها.
"""

from __future__ import annotations

import csv
import hashlib
import io
import os
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final

__all__ = [
    "BYTE_LENGTH_RULE",
    "DIGEST_RULE",
    "A_CONSERVATION_AUDIT_IS_NOT_AN_ACCURACY_CLAIM_NOTE",
    "AN_IMPORTED_TAG_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT_NOTE",
    "A_FAILED_UPLOAD_IS_NOT_A_DEPOSIT_NOTE",
    "AN_IGNORED_PATH_CANNOT_RECEIVE_A_DEPOSIT_NOTE",
    "A_MIRROR_WITH_ANOTHER_DIGEST_IS_NOT_THESE_BYTES_NOTE",
    "A_PERMISSION_UNEXAMINED_IS_NOT_A_PERMISSION_REFUSED_NOTE",
    "A_SKIP_IS_CONDITIONED_ON_THE_BYTES_NOT_THE_VARIABLE_NOTE",
    "COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE",
    "DEPOSITED_DERIVED_NOUN_COUNTS",
    "DEPOSIT_DIRECTORY",
    "DEPOSITED_EMBEDDED_NEWLINE_BREAKS",
    "DEPOSITED_EMBEDDED_NEWLINE_RECORDS",
    "DEPOSITED_LINE_COUNT",
    "DEPOSITED_RECORD_COUNT",
    "DERIVED_NOUN_TAGS",
    "EMBEDDED_NEWLINE_COUNTING_RULE",
    "LINE_COUNTING_RULE",
    "MASAQ_ATTRIBUTION",
    "MASAQ_BYTE_LENGTH",
    "MASAQ_DOI",
    "MASAQ_LICENCE",
    "MASAQ_PATH_VARIABLE",
    "MASAQ_REDERIVED_FIGURES",
    "MASAQ_RELATIVE_PATH",
    "MASAQ_SHA256",
    "MASAQ_DEPOSIT_NAMED_RESIDUALS",
    "MIRROR_CORROBORATION",
    "MORPH_TAG_COLUMN",
    "NO_ROOT_COLUMN_SO_NO_CROSS_CORPUS_FIGURE_NOTE",
    "RECORD_COUNTING_RULE",
    "REDERIVATION_IS_COMPARISON_NOT_AUTOMATIC_ENDORSEMENT_NOTE",
    "SANCTIONED_DEPOSIT_FILENAMES",
    "SEGMENT_INDEX_COLUMN",
    "SHA_256_ORDERS_NOTHING_NOTE",
    "SYNTHETIC_LINES_ARE_DECLARED_NOT_HIDDEN_NOTE",
    "TAG_COUNTING_RULE",
    "THE_READY_PATH_IS_THE_MASAQ_WITNESS_PATH_NOT_PROGRAMME_COMPLETION_NOTE",
    "WORD_KEY_COLUMN",
    "DerivedNounTag",
    "MasaqDepositError",
    "MirrorCorroboration",
    "RederivedFigure",
    "deposit_directory_path",
    "deposit_place_is_clean",
    "figures_named",
    "deposit_path_ignore_rule",
    "unsanctioned_deposit_files",
    "masaq_bytes_are_resolvable",
    "masaq_digest",
    "masaq_path",
    "masaq_records",
    "masaq_text",
    "read_masaq_bytes",
    "vendored_masaq_path",
    "rederive_embedded_newline_breaks",
    "rederive_embedded_newline_records",
    "rederive_line_count",
    "rederive_record_count",
    "rederive_tag_count",
    "lines_are_conserved",
]


class MasaqDepositError(ValueError):
    """تُرفَع حين تُقرأ بايتاتٌ غيرُ المُبصَّمة أو يُودَع رقمٌ بلا قاعدةِ عدّ."""


MASAQ_SHA256: Final[str] = (
    "d43d2a813afbe0490254bb26623d6041ed352a273d333e731ddbcda3bd0b6f3a"
)
"""بصمةُ `MASAQ.csv` المُودَعة؛ ولا يُخرِج هذا البابُ رقمًا من غيرها."""

MASAQ_BYTE_LENGTH: Final[int] = 20_302_008
"""طولُ بايتاتها كما هي على القرص، بلا تطبيعٍ ولا إعادةِ ترميز."""

MASAQ_DOI: Final[str] = "10.17632/9yvrzxktmr.2"

MASAQ_LICENCE: Final[str] = "CC BY 3.0"

MASAQ_ATTRIBUTION: Final[str] = (
    "MASAQ: Morphologically-Analyzed and Syntactically-Annotated Quran, "
    "Majdi Sawalha, University of Jordan, DOI 10.17632/9yvrzxktmr.2, "
    f"licensed {MASAQ_LICENCE}"
)
"""نصُّ الإسناد؛ وهو **شرطُ رخصةٍ** لا لطفَ عبارة، فلا يُخرَج رقمٌ بحذفه."""

MASAQ_PATH_VARIABLE: Final[str] = "ALGHANEM_MASAQ_PATH"
"""متغيّرُ البيئة الذي يُمرَّر به مسارُ البايتات حين تكون خارجَ الشجرة."""

MASAQ_RELATIVE_PATH: Final[str] = "corpora/MASAQ.csv"
"""موضعُ البايتات داخل الشجرة إن أُودِعت؛ موضعٌ **مسنونٌ** لا مُخمَّن.

والوسمُ المُودَع `CC BY 3.0` هو ما بُني عليه حجزُ هذا الموضع. وليس في هذه
الوحدة دعوى أنّ غيرَ MASAQ **ممنوعُ** النسخ: بايتاتُ سائر المدوَّنات باقيةٌ
خارجَ الشجرة لأنّ إذنَ نسخها **لم يُفحَص ولم يُودَع هنا**، لا لأنّه فُحِص
فانتفى (`A_PERMISSION_UNEXAMINED_IS_NOT_A_PERMISSION_REFUSED`).
ووجودُ الملفّ في هذا الموضع **لا يُغني عن المطابقة**: البصمةُ والطولُ
يُفحصان كما يُفحصان لأيّ مسارٍ مُمرَّر، فالموضعُ ليس شهادة.
"""

_REPOSITORY_ROOT: Final[Path] = Path(__file__).resolve().parents[3]


def vendored_masaq_path() -> Path:
    """الموضعُ المسنونُ داخل الشجرة، محسوبًا من موضع هذه الوحدة لا من `cwd`."""

    return _REPOSITORY_ROOT / MASAQ_RELATIVE_PATH


DEPOSIT_DIRECTORY: Final[str] = "corpora"
"""مجلَّدُ الإيداع؛ يُقرأ من موضع هذه الوحدة لا من `cwd`."""

SANCTIONED_DEPOSIT_FILENAMES: Final[tuple[str, ...]] = (
    "README.md",
    "MASAQ.csv",
    "quran-simple-enhanced.txt",
)
"""ما يجوز أن يسكن مجلَّدَ الإيداع: بيانُه، وبايتاتُ مدوّنتَيه بأسمائها المسنونة.

والثالثُ مسنونٌ في `quran_corpus_word_total.QURAN_CORPUS_RELATIVE_PATH`
وبايتاتُه ليست في الشجرة بعدُ كبايتات MASAQ؛ وسَنُّ الموضع ليس إيداعًا، لكنّ
تركَه خارجَ المأذون كان يجعل نزولَ البايتات الصحيحةِ يُقرَأ رفعًا فاشلًا.
"""

A_FAILED_UPLOAD_IS_NOT_A_DEPOSIT_NOTE: Final[str] = (
    "AFailedUploadIsNotADeposit: ملفٌّ يصل إلى مجلَّد الإيداع باسمٍ غيرِ "
    f"`{SANCTIONED_DEPOSIT_FILENAMES[1]}` — أو بطولٍ وبصمةٍ لا يطابقان "
    "المُودَعَين — ليس إيداعًا ناقصًا بل **ليس إيداعًا**: لا يُقرأ منه رقمٌ، "
    "ولا يُصحِّح دعوى الإيداع في البيان، ولا يُترَك ساكنًا في موضعٍ يُوهِم أنّ "
    "البايتات حاضرة"
)


def deposit_directory_path() -> Path:
    """مسارُ مجلَّد الإيداع داخل الشجرة."""

    return _REPOSITORY_ROOT / DEPOSIT_DIRECTORY


def unsanctioned_deposit_files(directory: Path | str | None = None) -> tuple[Path, ...]:
    """الملفّاتُ الساكنةُ في موضع الإيداع بلا إذنٍ، مرتَّبةً بأسمائها.

    ولا تحكم هذه الدالّةُ على بايتات `MASAQ.csv` نفسِها: المطابقةُ على الطول
    والبصمة موضعُها `read_masaq_bytes`، وهذه تُمسك ما هو أسبقُ منها — اسمًا
    طارئًا نزل في موضع الإيداع ولا قاعدةَ له.
    """

    resolved = deposit_directory_path() if directory is None else Path(directory)
    if not resolved.is_dir():
        return ()
    return tuple(
        sorted(
            (
                entry
                for entry in resolved.iterdir()
                if entry.name not in SANCTIONED_DEPOSIT_FILENAMES
            ),
            key=lambda entry: entry.name,
        )
    )


def deposit_place_is_clean(directory: Path | str | None = None) -> bool:
    """صِدْقُ أنّ موضعَ الإيداع لا يسكنه إلّا مأذونٌ فيه."""

    return not unsanctioned_deposit_files(directory)


AN_IGNORED_PATH_CANNOT_RECEIVE_A_DEPOSIT_NOTE: Final[str] = (
    "AnIgnoredPathCannotReceiveADeposit: قاعدةُ تجاهلٍ تُصيب "
    f"`{MASAQ_RELATIVE_PATH}` تجعل إضافتَه تفشل **صامتةً** — لا رسالةَ خطأٍ "
    "في كلّ الحالات، وإنّما ملفٌّ لا يُدرَج. وذلك أخفى من الرفع الفاشل باسمٍ "
    "طارئ، لأنّ ذاك يترك في الشجرة ما يدلّ عليه وهذا لا يترك شيئًا"
)


def deposit_path_ignore_rule(relative_path: str = MASAQ_RELATIVE_PATH) -> str | None:
    """قاعدةُ التجاهل التي تُصيب مسارًا في الشجرة، أو `None` إن لم يُتجاهَل.

    وهذه تُمسك ما هو أسبقُ من `unsanctioned_deposit_files()`: تلك تحكم على ما
    **نزل** في موضع الإيداع، وهذه على ما يمنع البايتاتِ من النزول أصلًا؛
    فالحارسانِ على طرفَي الإيداع ولا يُغني أحدُهما عن الآخر.

    ولا تحكم على البايتات: المطابقةُ على الطول والبصمة موضعُها
    `read_masaq_bytes`. ويُرفَع `MasaqDepositError` إن تعذّر سؤالُ `git`،
    فغيابُ الجواب ليس جوابًا بالنفي.
    """

    try:
        completed = subprocess.run(
            ["git", "check-ignore", "-v", "--no-index", "--", relative_path],
            cwd=_REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:  # pragma: no cover - يعتمد على غياب `git` من النظام
        raise MasaqDepositError(f"تعذّر تشغيل `git check-ignore`: {error}") from error
    if completed.returncode == 1:
        return None
    if completed.returncode == 0:
        return completed.stdout.strip()
    raise MasaqDepositError(
        f"`git check-ignore` أخفق برمز {completed.returncode}: "
        f"{completed.stderr.strip()}"
    )


MORPH_TAG_COLUMN: Final[str] = "Morph_Tag"
"""العمودُ الذي يحمل وَسْمَ الصرف؛ ربطٌ يُسَنّ ويُعلَن، لا يُقرأ من بصمة."""

SEGMENT_INDEX_COLUMN: Final[str] = "Word_No"
"""`Word_No` فهرسُ مقطعٍ داخل كلمة لا فهرسُ كلمة؛ والخلطُ بينهما قد وقع فعلًا."""

WORD_KEY_COLUMN: Final[str] = "Column5"
"""مفتاحُ الكلمة؛ وهو غيرُ `Word_No`، وعليه تدور المحاذاةُ الموضعيّة."""


COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE: Final[str] = (
    "CompleteInductionIsCorpusBounded: ٤٬٢١٦ عددُ مقاطع `GERUND` **في هذه "
    "البايتات** تحت قاعدة عدِّها؛ وليس عددَ المصادر في العربية ولا حدًّا "
    "عليه، ولا يُقرأ منه استقراءٌ تامٌّ لبابٍ من أبواب المشتقّات"
)

AN_IMPORTED_TAG_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "AnImportedTagIsAHumanJudgementNotAMeasurement: الوَسْمُ حكمُ مُوسِّمٍ "
    "بشرٍ على منهج الإعراب لا خاصّيّةٌ تُقاس من البايتات؛ فالصفرُ يعني «لم "
    "يُوسَم هنا» ولا يعني «غيرُ موجودٍ في العربية» البتّة"
)

A_CONSERVATION_AUDIT_IS_NOT_AN_ACCURACY_CLAIM_NOTE: Final[str] = (
    "AConservationAuditIsNotAnAccuracyClaim: حفظُ الأسطر يُثبت أنّ كلَّ مقطعٍ "
    "نال حسابًا في أحد الأبواب، ولا يُثبت أنّ الحسابَ صوابٌ ولا أنّ الوَسْمَ "
    "صحيح؛ فالجردُ تمامُ تغطيةٍ لا تصديقُ مضمون"
)

SYNTHETIC_LINES_ARE_DECLARED_NOT_HIDDEN_NOTE: Final[str] = (
    "SyntheticLinesAreDeclaredNotHidden: الأسطرُ في الاختبارات مُصطنَعةٌ "
    "مُصرَّحٌ بجنسها، تُحاكي بنيةَ الصفّ وحدَها؛ ولا يُقرأ من سطرٍ مُصطنَعٍ "
    "رقمٌ عن المدوَّنة، فالأرقامُ كلُّها من البايتات المُبصَّمة أو لا تكون"
)

NO_ROOT_COLUMN_SO_NO_CROSS_CORPUS_FIGURE_NOTE: Final[str] = (
    "NoRootColumnSoNoCrossCorpusFigure: ليس في MASAQ عمودُ جذر، فربطُها بغيرها "
    "ربطٌ موضعيٌّ `(سورة، آية، كلمة)` لا ربطٌ بالجذر؛ ومن هناك جاء هبوطُ "
    "المحاذاة من ٢٣٫٣٪ إلى ٠٫٣٪، فلا رقمَ عابرًا للمدوَّنات في هذا الإيداع"
)

A_MIRROR_WITH_ANOTHER_DIGEST_IS_NOT_THESE_BYTES_NOTE: Final[str] = (
    "AMirrorWithAnotherDigestIsNotTheseBytes: مرآةٌ عامّةٌ بطولٍ آخرَ وبصمةٍ "
    "أخرى قد تُعطي أعدادَ الوسوم نفسَها وتُخالف في عدّ الأسطر والسجلّات؛ "
    "فالموافقةُ في عددٍ لا تجعلها هذه البايتات، والمطابقةُ على الطول والبصمة "
    "شرطُ كلِّ رقمٍ يخرج من هنا"
)

SHA_256_ORDERS_NOTHING_NOTE: Final[str] = (
    "Sha256OrdersNothing: لا خاصيّةَ حفظِ ترتيبٍ في `SHA-256` البتّة، "
    "فالبصمةُ تُثبِت الهويّةَ ولا تُرتِّب؛ وتبديلُ بايتٍ واحدٍ يُبدِّل البصمةَ "
    "كلَّها بلا جوارٍ بين المدخلين"
)

A_SKIP_IS_CONDITIONED_ON_THE_BYTES_NOT_THE_VARIABLE_NOTE: Final[str] = (
    "ASkipIsConditionedOnTheBytesNotTheVariable: يُتخطّى الاختبارُ حين "
    "**لا يُحلّ مسارٌ إلى ملفٍّ موجود** لا حين يخلو متغيّرُ البيئة؛ فمتغيّرٌ "
    "مضبوطٌ على مسارٍ لا ملفَّ فيه كان يُنتِج خطأً يُقرأ فشلَ قياس، ومسارٌ "
    "مُحلٌّ إلى ملفٍّ مخالفِ البصمة **لا يُتخطّى** بل يفشل: الموضعُ ليس شهادة"
)

A_PERMISSION_UNEXAMINED_IS_NOT_A_PERMISSION_REFUSED_NOTE: Final[str] = (
    "APermissionUnexaminedIsNotAPermissionRefused: بقاءُ بايتاتِ مدوَّنةٍ "
    "أخرى خارجَ هذه الشجرة حالةُ **إذنٍ لم يُفحَص ولم يُودَع**، لا حكمٌ بأنّ "
    "ناشرَها يمنع النسخ. ومنعُ الاشتقاق ليس منعَ النسخ الحرفيّ، وشرطُ "
    "النسبة والإشعار ليس منعًا؛ فمن قرأ الغيابَ تحريمًا فقد أصدر عن رخصةٍ "
    "حكمًا لم يقرأه فيها، وذلك عينُ ما تمنعه هذه الشجرة في الأرقام"
)

THE_READY_PATH_IS_THE_MASAQ_WITNESS_PATH_NOT_PROGRAMME_COMPLETION_NOTE: Final[str] = (
    "TheReadyPathIsTheMasaqWitnessPathNotProgrammeCompletion: الجاهزُ في هذه "
    "الوحدة **مسارُ شاهدٍ واحد**: استقبالُ بايتات MASAQ، والتحقّقُ من هويّتها "
    "بالطول والبصمة، وإعادةُ اشتقاق أرقامها بقواعد عدّها. وليس الجاهزُ "
    "المشروعَ. فنزولُ البايتات لا يُنفِّذ قانونًا مُصرَّحًا بتأجيله "
    "(`DECLARED_DEFERRED`)، ولا يُنشئ سلطةَ حكمٍ ولا ولادة، ولا يُغلِق غايةً "
    "معرفية، ولا يرفع رتبةَ نتيجةٍ لمجرّد أنّ الملفَّ صار في اليد، ولا يُحيل "
    "استقراءً على هذه المدوَّنة دعوى عن العربية المفتوحة، ولا يُغيّر حدَّ "
    "`CompleteInductionIsCorpusBounded` ولا يُوسِّعه"
)

REDERIVATION_IS_COMPARISON_NOT_AUTOMATIC_ENDORSEMENT_NOTE: Final[str] = (
    "RederivationIsComparisonNotAutomaticEndorsement: وصولُ البايتات لا يعتمد "
    "الأرقامَ المُجمَّدة اعتمادًا تلقائيًّا، وإنّما يُشغِّل دوالَّ إعادة "
    "الاشتقاق عليها. فإن وافق الناتجُ المُجمَّدَ ثبتت المطابقةُ **في نطاق هذا "
    "الشاهد وحدَه**، وإن خالفه سُجِّل الفرقُ كما وقع. ولا يُعدَّل المُجمَّدُ "
    "ليُلائم الناتج، ولا قاعدةُ عدّه؛ فإعادةُ الاشتقاق مقارنةٌ لا ترقيةٌ "
    "معرفيةٌ آلية، ولا تصير الدعوى السابقة حقيقةً لمجرّد أنّ الشاهد صار متاحًا"
)

MASAQ_DEPOSIT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "CompleteInductionIsCorpusBounded": COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE,
    "AnImportedTagIsAHumanJudgementNotAMeasurement": (
        AN_IMPORTED_TAG_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT_NOTE
    ),
    "AConservationAuditIsNotAnAccuracyClaim": (
        A_CONSERVATION_AUDIT_IS_NOT_AN_ACCURACY_CLAIM_NOTE
    ),
    "SyntheticLinesAreDeclaredNotHidden": (
        SYNTHETIC_LINES_ARE_DECLARED_NOT_HIDDEN_NOTE
    ),
    "NoRootColumnSoNoCrossCorpusFigure": (
        NO_ROOT_COLUMN_SO_NO_CROSS_CORPUS_FIGURE_NOTE
    ),
    "AMirrorWithAnotherDigestIsNotTheseBytes": (
        A_MIRROR_WITH_ANOTHER_DIGEST_IS_NOT_THESE_BYTES_NOTE
    ),
    "Sha256OrdersNothing": SHA_256_ORDERS_NOTHING_NOTE,
    "AFailedUploadIsNotADeposit": A_FAILED_UPLOAD_IS_NOT_A_DEPOSIT_NOTE,
    "AnIgnoredPathCannotReceiveADeposit": (
        AN_IGNORED_PATH_CANNOT_RECEIVE_A_DEPOSIT_NOTE
    ),
    "ASkipIsConditionedOnTheBytesNotTheVariable": (
        A_SKIP_IS_CONDITIONED_ON_THE_BYTES_NOT_THE_VARIABLE_NOTE
    ),
    "APermissionUnexaminedIsNotAPermissionRefused": (
        A_PERMISSION_UNEXAMINED_IS_NOT_A_PERMISSION_REFUSED_NOTE
    ),
    "TheReadyPathIsTheMasaqWitnessPathNotProgrammeCompletion": (
        THE_READY_PATH_IS_THE_MASAQ_WITNESS_PATH_NOT_PROGRAMME_COMPLETION_NOTE
    ),
    "RederivationIsComparisonNotAutomaticEndorsement": (
        REDERIVATION_IS_COMPARISON_NOT_AUTOMATIC_ENDORSEMENT_NOTE
    ),
}


BYTE_LENGTH_RULE: Final[str] = (
    "طولُ البايتات على القرص كما هي، بلا تطبيعٍ ولا فَكِّ ترميزٍ ولا حذفِ "
    "علامة ترتيبٍ في أوّلها"
)

DIGEST_RULE: Final[str] = (
    "`SHA-256` على تلك البايتات نفسِها؛ والبصمةُ هويّةٌ لا ترتيب. "
    + SHA_256_ORDERS_NOTHING_NOTE
)

LINE_COUNTING_RULE: Final[str] = (
    'السطرُ مقطعٌ من مقاطع `data.decode("utf-8-sig").splitlines()`، وعددُها '
    "١٥٧٬٨٥٤. وهي **ليست** قاعدةَ السجلّات: `list(csv.DictReader(...))` يُعطي "
    "١٥٧٬٦٧٧، والفرقُ ١٧٧ مقيسٌ لا مُقدَّر — صفُّ ترويسةٍ واحد، و١٧٦ فاصلَ "
    "سطرٍ داخل حقولٍ مُقتبَسة موزَّعةً على ١٥٤ سجلًّا"
)

RECORD_COUNTING_RULE: Final[str] = (
    "السجلُّ صفٌّ في `csv` بعد صفّ الترويسة، مقروءًا بقارئٍ يحترم الاقتباسَ "
    "وفواصلَ الأسطر داخل الحقول؛ فسطرُ الملفّ ليس سجلًّا، وعددُ الأسطر ليس "
    "عددَ السجلّات"
)

EMBEDDED_NEWLINE_COUNTING_RULE: Final[str] = (
    "السجلُّ ذو الفاصل الداخليّ سجلٌّ في أحد حقوله فاصلُ سطرٍ داخل اقتباس، "
    "مقروءًا من `io.StringIO` لا من `splitlines()`: الثاني يشقُّ الفواصلَ قبل "
    "أن يراها القارئُ فيُعطي صفرًا. وعددُ **الفواصل** ١٧٦ وعددُ **السجلّات** "
    "الحاملةِ لها ١٥٤، فبعضُ السجلّات يحمل أكثرَ من فاصل"
)

TAG_COUNTING_RULE: Final[str] = (
    f"المقطعُ سجلٌّ في `csv`، ويُعَدُّ للوَسْم إذا كانت قيمةُ العمود "
    f"«{MORPH_TAG_COLUMN}» **مطابقةً حرفيًّا** للوَسْم لا محتويةً له: "
    "`GERUND_MEEM` ليس `GERUND`، ومن عدَّ بالاحتواء ضمَّ خمسةَ أبوابٍ في باب. "
    + AN_IMPORTED_TAG_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT_NOTE
)


@dataclass(frozen=True, slots=True)
class DerivedNounTag:
    """بابٌ من أبواب المشتقّات: اسمُه العربيّ، ووَسْمُه، وعددُه في هذه البايتات."""

    arabic_name: str
    tag: str
    deposited_count: int

    def __post_init__(self) -> None:
        for value, label in ((self.arabic_name, "الاسمُ العربيّ"), (self.tag, "الوَسْم")):
            if not isinstance(value, str) or not value.strip():
                raise MasaqDepositError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
        if self.deposited_count < 0:
            raise MasaqDepositError("عددٌ مُودَعٌ لا يكون سالبًا.")


DERIVED_NOUN_TAGS: Final[tuple[DerivedNounTag, ...]] = (
    DerivedNounTag("مصدر", "GERUND", 4_216),
    DerivedNounTag("مصدر ميميّ", "GERUND_MEEM", 125),
    DerivedNounTag("مصدر مرّة", "GERUND_INSTANT", 84),
    DerivedNounTag("مصدر حرفة", "GERUND_PROFESSION", 38),
    DerivedNounTag("مصدر هيئة", "GERUND_STATE", 2),
    DerivedNounTag("اسم زمان/مكان", "NOUN_TIME_PLACE", 225),
    DerivedNounTag("اسم آلة", "NOUN_INSTRUMENT", 24),
    DerivedNounTag("اسم فاعل", "NOUN_ACTIVE_PART", 3_156),
    DerivedNounTag("اسم مفعول", "NOUN_PASSIVE_PART", 501),
    DerivedNounTag("صفة مشبَّهة", "ADJ_QUALIT", 1_646),
    DerivedNounTag("صيغة مبالغة", "ADJ_INTENS", 459),
    DerivedNounTag("اسم تفضيل", "ADJ_COMP", 643),
    DerivedNounTag("منسوب", "NOUN_RELATIVE", 125),
    DerivedNounTag("مصغَّر", "NOUN_DIMINUTIVE", 1),
)
"""الأبوابُ التي تَسِمها MASAQ بأسمائها، وتقف المدوَّنةُ الصرفيةُ دونها عند `VN`."""

DEPOSITED_DERIVED_NOUN_COUNTS: Final[dict[str, int]] = {
    item.tag: item.deposited_count for item in DERIVED_NOUN_TAGS
}

DEPOSITED_LINE_COUNT: Final[int] = 157_854
"""١٥٧٬٨٥٤ تحت `LINE_COUNTING_RULE` وحدَها؛ ورقمُ السجلّات غيرُه بقاعدته."""

DEPOSITED_RECORD_COUNT: Final[int] = 157_677
"""١٥٧٬٦٧٧ تحت `RECORD_COUNTING_RULE`؛ والفرقُ عن الأسطر مُسمًّى بعلّته."""

DEPOSITED_EMBEDDED_NEWLINE_RECORDS: Final[int] = 154
"""السجلّاتُ الحاملةُ فاصلَ سطرٍ داخل حقلٍ مُقتبَس؛ وهو الرقمُ الذي كُشِف عطبُه."""

DEPOSITED_EMBEDDED_NEWLINE_BREAKS: Final[int] = 176
"""عددُ الفواصل نفسِها: ١٧٧ = ١ ترويسة + ١٧٦ فاصلًا، وهو جردُ الفرق بلا بقيّة."""


@dataclass(frozen=True, slots=True)
class MirrorCorroboration:
    """ما قِيس على مرآةٍ عامّةٍ **ببصمةٍ أخرى**، مُصرَّحًا بأنّه ليس هذه البايتات."""

    mirror_byte_length: int
    mirror_sha256: str
    figures_that_matched: tuple[str, ...]
    figures_that_did_not: tuple[str, ...]
    what_it_establishes: str
    what_it_does_not_establish: str

    def __post_init__(self) -> None:
        if not self.figures_that_matched or not self.figures_that_did_not:
            raise MasaqDepositError(
                "مرآةٌ تُوافق في كلّ شيءٍ أو تُخالف في كلّ شيءٍ لا تُسجَّل "
                "قرينةً: المُسجَّلُ ما وافق وما خالف معًا."
            )
        if self.mirror_sha256 == MASAQ_SHA256:
            raise MasaqDepositError("مرآةٌ ببصمة الإيداع ليست مرآةً أخرى بل هي هي.")


MIRROR_CORROBORATION: Final[MirrorCorroboration] = MirrorCorroboration(
    mirror_byte_length=18_650_409,
    mirror_sha256="777d0cc8f24f4c17d07ad83a522056fe7ebd5c83dbbae86161f1fdc95aaca900",
    figures_that_matched=tuple(item.tag for item in DERIVED_NOUN_TAGS),
    figures_that_did_not=(
        "طولُ البايتات",
        "بصمةُ البايتات",
        "أسطرُ الملفّ (`splitlines`)",
        "سجلّاتُ `csv`",
        "سجلّاتٌ بفاصل سطرٍ داخليّ",
        "فواصلُ الأسطر داخل الحقول",
    ),
    what_it_establishes=(
        "أنّ أعدادَ الأبواب الأربعةَ عشرَ خرجت مطابقةً من ملفٍّ آخرَ مُعلَنِ "
        "الطول والبصمة، عمودُ الوَسْم فيه «Morph_Tag»؛ فهي قرينةُ استقرارٍ "
        "على قاعدة العدّ نفسِها في نسختين"
    ),
    what_it_does_not_establish=(
        "أنّ المرآةَ هي البايتاتُ المُودَعة: طولُها وبصمتُها مختلفان، "
        "وأعدادُ الأسطر والسجلّات والفواصل الداخليّة خالفت (١٥٧٬٦٧٧ سطرًا "
        "و١٥٧٬٦٧٦ سجلًّا وصفرُ فواصل). وترويستُها ليست ترويسةَ المُودَع: ليس "
        "فيها «Column5»، و`Word_No` فيها فهرسُ كلمةٍ لا فهرسُ مقطع؛ فربطُ "
        "مفتاح الكلمة وفهرسِ المقطع أعلاه **تصريحُ حائز البايتات** لا قراءةٌ "
        "قُرِئت من هذه المرآة. " + A_MIRROR_WITH_ANOTHER_DIGEST_IS_NOT_THESE_BYTES_NOTE
    ),
)
"""قرينةٌ مقيسةٌ لا شاهدٌ ثانٍ: مرآتان ببصمتين ليستا نصًّا مرّتين."""


def masaq_path(path: Path | str | None = None) -> Path:
    """مسارُ البايتات: المُمرَّرُ، وإلّا `ALGHANEM_MASAQ_PATH`، وإلّا المُودَعُ في الشجرة.

    والترتيبُ مقصود: تصريحُ المستدعي أوّلًا، ثمّ تصريحُ البيئة، ثمّ الموضعُ
    المسنونُ `corpora/MASAQ.csv` **إن كان موجودًا فعلًا**. ولا رابعَ لها:
    غيابُ الثلاثة رفضٌ صريح، ولا يُخمَّن موضعُ الملفّ من اسمٍ ولا من `cwd`.
    """

    if path is not None:
        return Path(path)
    declared = os.environ.get(MASAQ_PATH_VARIABLE)
    if declared:
        return Path(declared)
    vendored = vendored_masaq_path()
    if vendored.is_file():
        return vendored
    raise MasaqDepositError(
        "بايتاتُ MASAQ ليست في هذه الشجرة ولا صُرِّح بمسارها؛ فتُودَع في "
        f"`{MASAQ_RELATIVE_PATH}` أو يُصرَّح به في `{MASAQ_PATH_VARIABLE}`، "
        "ولا يُخمَّن موضعُها."
    )


def masaq_bytes_are_resolvable(path: Path | str | None = None) -> bool:
    """أيُحَلُّ مسارٌ إلى ملفٍّ **موجود** بأبواب `masaq_path` الثلاثة؟

    وهذا شرطُ التخطّي وحدَه: `ASkipIsConditionedOnTheBytesNotTheVariable`.
    فلا يُقرأ منها طولٌ ولا بصمة، ولا تُصدِّق ملفًّا: ملفٌّ موجودٌ بالاسم
    المسنون ومخالفُ البصمة **يُحَلّ ولا يُتخطّى**، فيقع الرفضُ في
    `read_masaq_bytes` حيث موضعُه، لا هنا صامتًا.
    """

    try:
        resolved = masaq_path(path)
    except MasaqDepositError:
        return False
    return resolved.is_file()


def read_masaq_bytes(path: Path | str | None = None) -> bytes:
    """البايتاتُ مرفوضةً إن خالفت الطولَ أو البصمةَ المُودَعَين.

    والمطابقتان معًا لا إحداهما: ملفٌّ بالاسم نفسِه ليس هذا الملفَّ حتّى
    يُطابِقه في طوله وبصمته، والموافقةُ في رقمٍ لا تُغني عن ذلك.
    """

    resolved = masaq_path(path)
    if not resolved.is_file():
        raise MasaqDepositError(f"ملفُّ MASAQ غيرُ موجودٍ في المسار: {resolved}")
    data = resolved.read_bytes()
    if len(data) != MASAQ_BYTE_LENGTH:
        raise MasaqDepositError(
            f"طولُ البايتات {len(data)} لا يطابق المُودَع {MASAQ_BYTE_LENGTH}؛ "
            + A_MIRROR_WITH_ANOTHER_DIGEST_IS_NOT_THESE_BYTES_NOTE
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != MASAQ_SHA256:
        raise MasaqDepositError(
            f"بصمةُ البايتات {digest} لا تطابق المُودَعة {MASAQ_SHA256}؛ "
            + A_MIRROR_WITH_ANOTHER_DIGEST_IS_NOT_THESE_BYTES_NOTE
        )
    return data


def masaq_digest(path: Path | str | None = None) -> str:
    """بصمةُ البايتات مُشتقّةً منها، لا منسوخةً من حقلٍ في وحدةٍ أخرى."""

    return hashlib.sha256(read_masaq_bytes(path)).hexdigest()


def masaq_text(data: bytes) -> str:
    """فَكُّ الترميز مرّةً واحدةً بـ`utf-8-sig`، وعليه تدور القاعدتان معًا."""

    return data.decode("utf-8-sig")


def rederive_line_count(data: bytes) -> int:
    """عددُ الأسطر تحت `LINE_COUNTING_RULE`."""

    return len(masaq_text(data).splitlines())


def masaq_records(data: bytes) -> tuple[dict[str, str], ...]:
    """السجلّاتُ تحت `RECORD_COUNTING_RULE`، مقروءةً عبر `io.StringIO`.

    والقراءةُ من `io.StringIO` لا من `splitlines()`: الثاني يشقُّ فواصلَ
    الأسطر الداخليّة قبل أن يراها القارئ، فيُخفيها عن كلّ عدٍّ بعدَه.
    """

    reader = csv.DictReader(io.StringIO(masaq_text(data), newline=""))
    if reader.fieldnames is None:
        raise MasaqDepositError("ملفٌّ بلا ترويسةٍ لا يُقرأ بربطٍ بالأسماء.")
    return tuple(
        {key: (value if isinstance(value, str) else "") for key, value in row.items()}
        for row in reader
    )


def rederive_record_count(data: bytes) -> int:
    """عددُ السجلّات تحت `RECORD_COUNTING_RULE`."""

    return len(masaq_records(data))


def _field_rows(data: bytes) -> list[list[str]]:
    return list(csv.reader(io.StringIO(masaq_text(data), newline="")))


def rederive_embedded_newline_records(data: bytes) -> int:
    """السجلّاتُ التي في أحد حقولها فاصلُ سطرٍ داخل اقتباس، ترويسةً وما بعدها."""

    return sum(
        1
        for row in _field_rows(data)
        if any(len(field.splitlines()) > 1 for field in row)
    )


def rederive_embedded_newline_breaks(data: bytes) -> int:
    """عددُ الفواصل نفسِها لا عددُ حامليها؛ فالسجلُّ قد يحمل أكثرَ من فاصل."""

    return sum(
        max(len(field.splitlines()) - 1, 0)
        for row in _field_rows(data)
        for field in row
    )


def rederive_tag_count(data: bytes, tag: str) -> int:
    """عددُ المقاطع الموسومةِ بالوَسْم تحت `TAG_COUNTING_RULE`، مطابقةً لا احتواءً."""

    records = masaq_records(data)
    if records and MORPH_TAG_COLUMN not in records[0]:
        raise MasaqDepositError(
            f"العمودُ «{MORPH_TAG_COLUMN}» غائبٌ عن الترويسة؛ ولا يُحمَل عمودٌ "
            "على أقرب اسمٍ إليه، فالعدُّ يقف."
        )
    return sum(1 for record in records if record.get(MORPH_TAG_COLUMN) == tag)


def lines_are_conserved(data: bytes) -> bool:
    """أكلُّ سطرٍ نال حسابًا؟ ترويسةٌ + سجلّاتٌ + فواصلُ داخليّة = الأسطرُ كلُّها.

    `AConservationAuditIsNotAnAccuracyClaim`: هذا جردُ تغطيةٍ لا تصديقُ وَسْم.
    """

    return rederive_line_count(data) == (
        1 + rederive_record_count(data) + rederive_embedded_newline_breaks(data)
    )


@dataclass(frozen=True, slots=True)
class RederivedFigure:
    """رقمٌ مُودَعٌ لا يقوم إلّا بقاعدة عدّه ودالّةِ إعادة اشتقاقه وحدِّه المكتوب.

    ولا تُبنى بلا قاعدة: رقمٌ بلا قاعدةٍ غيرُ قابلٍ لإعادة الاشتقاق ولو
    طابقت بصمةُ ملفّه، ويُقرأ بعد جلساتٍ خاصّيّةً في العربية.
    """

    name: str
    deposited: object
    counting_rule: str
    what_it_does_not_establish: str
    derive: Callable[[bytes], object]

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ الرقم"),
            (self.counting_rule, "قاعدةُ العدّ"),
            (self.what_it_does_not_establish, "حدُّ الرقم"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MasaqDepositError(
                    f"{label} نصٌّ غير فارغ؛ ورقمٌ بلا قاعدةِ عدٍّ أو بلا حدٍّ "
                    "مكتوبٍ لا يُودَع في هذا الباب."
                )
        if not callable(self.derive):
            raise MasaqDepositError("رقمٌ بلا دالّةِ إعادةِ اشتقاقٍ إيداعٌ بلا شاهد.")

    def rederive(self, data: bytes) -> object:
        """أعِد اشتقاقَ الرقم من البايتات المُطابَقة، بلا مقارنةٍ ولا حكم."""

        return self.derive(data)

    def holds(self, data: bytes) -> bool:
        """أيُطابِق المُودَعُ ما اشتُقَّ الآن؟ والدرءُ أنّ الاختلافَ يُرى لا يُطوى."""

        return self.rederive(data) == self.deposited


def _tag_counter(tag: str) -> Callable[[bytes], object]:
    """دالّةُ عدٍّ لوَسْمٍ بعينه؛ مُسمّاةً لا مُغلَقةً على متغيّرِ حلقة."""

    def derive(data: bytes) -> object:
        return rederive_tag_count(data, tag)

    return derive


def _tag_figure(item: DerivedNounTag) -> RederivedFigure:
    return RederivedFigure(
        name=f"{item.arabic_name} — {item.tag}",
        deposited=item.deposited_count,
        counting_rule=TAG_COUNTING_RULE,
        what_it_does_not_establish=COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE,
        derive=_tag_counter(item.tag),
    )


MASAQ_REDERIVED_FIGURES: Final[tuple[RederivedFigure, ...]] = (
    RederivedFigure(
        name="طولُ البايتات",
        deposited=MASAQ_BYTE_LENGTH,
        counting_rule=BYTE_LENGTH_RULE,
        what_it_does_not_establish=(
            "أنّ الملفَّ هو النسخةُ المنشورةُ عند صاحبها: الطولُ يُثبت ما "
            "فُتِح هنا، والمرآةُ ليست المنبع"
        ),
        derive=len,
    ),
    RederivedFigure(
        name="بصمةُ البايتات",
        deposited=MASAQ_SHA256,
        counting_rule=DIGEST_RULE,
        what_it_does_not_establish=(
            "صحّةَ وَسْمٍ واحدٍ فيها: البصمةُ هويّةُ بايتاتٍ لا تصديقٌ على " "حكمِ مُوسِّم"
        ),
        derive=lambda data: hashlib.sha256(data).hexdigest(),
    ),
    RederivedFigure(
        name="أسطرُ الملفّ (`splitlines`)",
        deposited=DEPOSITED_LINE_COUNT,
        counting_rule=LINE_COUNTING_RULE,
        what_it_does_not_establish=(
            "أنّه عددُ المقاطع المُوسَّمة: السطرُ ليس سجلًّا، والفرقُ ١٧٧ " "مُسمًّى بعلّته لا مطويّ"
        ),
        derive=rederive_line_count,
    ),
    RederivedFigure(
        name="سجلّاتُ `csv`",
        deposited=DEPOSITED_RECORD_COUNT,
        counting_rule=RECORD_COUNTING_RULE,
        what_it_does_not_establish=(
            "أنّها عددُ كلماتِ القرآن: السجلُّ **مقطعٌ** لا كلمة، و`Word_No` "
            "فهرسُ مقطعٍ لا فهرسُ كلمة"
        ),
        derive=rederive_record_count,
    ),
    RederivedFigure(
        name="سجلّاتٌ بفاصل سطرٍ داخليّ",
        deposited=DEPOSITED_EMBEDDED_NEWLINE_RECORDS,
        counting_rule=EMBEDDED_NEWLINE_COUNTING_RULE,
        what_it_does_not_establish=(
            "أنّ الفرقَ بين القاعدتين مُفسَّرٌ بهذا العدد وحدَه: السجلُّ قد "
            "يحمل أكثرَ من فاصل، ولذلك أُودِع عددُ الفواصل معه"
        ),
        derive=rederive_embedded_newline_records,
    ),
    RederivedFigure(
        name="فواصلُ الأسطر داخل الحقول",
        deposited=DEPOSITED_EMBEDDED_NEWLINE_BREAKS,
        counting_rule=EMBEDDED_NEWLINE_COUNTING_RULE,
        what_it_does_not_establish=(
            "أنّ الأسطرَ المُقتبَسة أُحصِيت صحيحةً في مضمونها: الجردُ تمامُ "
            "تغطيةٍ لا تصديقُ محتوى. "
            + A_CONSERVATION_AUDIT_IS_NOT_AN_ACCURACY_CLAIM_NOTE
        ),
        derive=rederive_embedded_newline_breaks,
    ),
) + tuple(_tag_figure(item) for item in DERIVED_NOUN_TAGS)
"""عشرون رقمًا: ستّةٌ عن البايتات وقواعدِ العدّ، وأربعةَ عشرَ عن أبواب المشتقّات."""


def figures_named(names: Sequence[str]) -> tuple[RederivedFigure, ...]:
    """الأرقامُ بأسمائها؛ واسمٌ لا يُطابِق شيئًا يُرفَع به خطأٌ لا يُتخطّى صامتًا."""

    index = {figure.name: figure for figure in MASAQ_REDERIVED_FIGURES}
    missing = [name for name in names if name not in index]
    if missing:
        raise MasaqDepositError(f"أرقامٌ مطلوبةٌ غيرُ مُودَعةٍ بأسمائها: {missing}")
    return tuple(index[name] for name in names)
