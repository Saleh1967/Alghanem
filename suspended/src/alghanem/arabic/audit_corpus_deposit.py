"""مدوّنةٌ ثانيةٌ في موضع الإيداع، بدورٍ مُعلَنٍ غيرِ دور الأولى.

نزلت في `corpora/` بايتاتُ مدوّنةٍ ثانية: النسخةُ التي يقيس عليها برنامج
`hamil` — `quran-simple-enhanced.txt` من `GlobalQuran/data`، 1,306,770 بايتًا.
ونزولُها **لا يجعلها مدوّنةً ثانيةً للقياس**: دورُها المُعلَنُ ههنا
`AUDIT_CORPUS`، أي بايتاتٌ تُقرأ لتُفحَص بها أرقامُ ذاك البرنامج وحدَها،
بإزاء `MEASUREMENT_CORPUS` التي تُقاس عليها أرقامُ هذه الشجرة. فيفترق ههنا
ثلاثةٌ كانت تُقرأ واحدًا::

    ASecondCorpus        != ASecondMeasurementCorpus
    TheSameFileName      != TheSameBytes
    AQuotedSeal          != ASealRegeneratedFromTheDisk

**أوّلًا: الدورُ مُعلَنٌ قبل القراءة، ولا يُقاس أحدُهما على الآخر أبدًا.**
لكلٍّ من المدوّنتين ختمٌ مختلفٌ ودورٌ مختلفٌ مُصرَّحٌ به في `THE_DECLARED_CORPORA`،
ولا دالّةَ ههنا تجمع رقمًا من إحداهما إلى رقمٍ من الأخرى أو تطرحه:
`refuse_to_read_one_against_the_other` تَرفض المقابلةَ عبر الدورين صراحةً،
فيُمسَك الخلطُ عند أوّل محاولةٍ لا بعد خروج رقمٍ منه
(`TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER`).

**وثانيًا: الاسمُ ليس ختمًا.** اسمُ المُودَعَين المنبعيُّ واحدٌ —
`quran-simple-enhanced.txt` في تنزيل وفي GlobalQuran معًا — وبايتاتُهما
مختلفةٌ طولًا وبصمة. فلو أُنزِلت الثانيةُ باسمها المنبعيّ لأطاحت بالأولى في
موضعها المسنون بلا رسالةِ خطأٍ واحدة؛ ولذلك سُنَّ لها اسمٌ يحمل مصدرَه:
`globalquran-simple-enhanced.txt`. والتصادمُ يُسجَّل ولا يُلطَّف: من قرأ اتّحادَ
الاسمين اتّحادَ نصٍّ فقد قاس بغير ختم (`THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES`).

**وثالثًا: أرقامُ الوديعة تولَّد من القرص لحظةَ الالتزام.** هذا هو محضرُ
«الدرجة الثالثة عند القياس» مُدوَّنًا إجراءً لا درسًا: كلُّ رقمٍ في
`THE_AUDIT_CORPUS` يحمل `FigureProvenance` معه، والمولَّدُ منه يُعاد حسابًا من
البايتات في `regenerate_every_generated_figure`، والواردُ من عرضٍ خارجيّ
يُسمّى `QUOTED_INCOMING_NOT_REPRODUCED` ولا يُترقَّى إلى مولَّدٍ إلّا بإعادة
توليدٍ فعليّة. فرقمٌ منسوخٌ من واجهةٍ إلى وديعةٍ بلا توليدٍ **وديعةٌ بلا قياس**
(`NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT`).

**ورابعًا: الختمُ المنقولُ `8b387e8` طُلِب في غير جنسه، ثم لم يُطابِق.** طُلِب
قبلُ كائنًا في مستودعٍ آخر فلم يكن كائنًا صالحًا، فسُجِّل أنّه ختمُ ذاك
المستودع. وبصمةُ SHA-256 المولَّدةُ من القرص عند الاستقبال هي
`8b387ea811bc…`، فالجنسُ المطلوبُ كان خطأً — هو ختمُ محتوًى لا كائنُ مستودع —
**والمنقولُ مع ذلك ليس صدرًا لها**: يوافقها في ستّة محارفَ ويفترق في السابع
(`a` عندنا مقابل `8` عنده). فالموافقةُ الجزئيّةُ تُقاس ولا تُقرأ مطابقة، ونسبةُ
الفرق — أهو زلّةُ نقلٍ أم ختمُ شيءٍ آخر — **مرفوضة** ههنا: ليس عندنا طرفُهم
لنحكم. والرقمُ يبقى `QUOTED_INCOMING_NOT_REPRODUCED` بحاله
(`THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS`،
`A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH`).

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` ولا من `program/`، ولا تقرؤها بوّابةٌ فيهما.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

from .compression_model_preregistration import FROZEN_CORPUS
from .pipeline_stations import repository_root_path
from .quran_corpus_word_total import (
    QURAN_CORPUS_PATH_VARIABLE,
    QURAN_CORPUS_RELATIVE_PATH,
)

__all__ = [
    "AUDIT_CORPUS_ATTRIBUTION",
    "A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH",
    "AUDIT_CORPUS_PATH_VARIABLE",
    "AUDIT_CORPUS_RELATIVE_PATH",
    "NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT",
    "AUDIT_CORPUS_NAMED_RESIDUALS",
    "THE_AUDIT_CORPUS",
    "THE_AUDIT_CORPUS_FIGURES",
    "THE_DECLARED_CORPORA",
    "THE_MEASUREMENT_CORPUS",
    "THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES",
    "THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS",
    "TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER",
    "AuditCorpusError",
    "CorpusRole",
    "CrossRoleReading",
    "DeclaredCorpus",
    "DepositedFigure",
    "FigureProvenance",
    "audit_corpus_bytes_are_resolvable",
    "audit_corpus_path",
    "git_blob_sha1",
    "read_audit_corpus_bytes",
    "refuse_to_read_one_against_the_other",
    "the_quoted_incoming_seal",
    "the_quoted_seal_agreement_length",
    "the_quoted_seal_is_a_prefix_of_the_generated_digest",
    "regenerate_every_generated_figure",
    "vendored_audit_corpus_path",
]


class AuditCorpusError(ValueError):
    """رفضٌ في باب مدوّنة التدقيق: مسارٌ لا يُحَلّ، أو بايتاتٌ لا تطابق ختمَها."""


class CrossRoleReading(AuditCorpusError):
    """رُفضت مقابلةُ رقمٍ من دورٍ برقمٍ من دورٍ آخر؛ والرفضُ عند المحاولة."""


class CorpusRole(Enum):
    """دورُ مدوّنةٍ مُودَعة، مُعلَنٌ قبل قراءتها لا مُستنبَطٌ من استعمالها."""

    MEASUREMENT_CORPUS = "مدوّنةُ_القياس"
    """ما تُقاس عليها أرقامُ هذه الشجرة، وتُنسَب إليها في نثرها."""

    AUDIT_CORPUS = "مدوّنةُ_التدقيق"
    """ما تُقرأ لتُفحَص بها أرقامُ برنامجٍ آخرَ عليها، ولا يُنسَب إليها رقمٌ لنا."""


class FigureProvenance(Enum):
    """من أين جاء رقمٌ إلى وديعة: من القرص لحظتَها، أو من عرضٍ لم يُعَد."""

    GENERATED_FROM_THE_DISK_AT_DEPOSIT = "مولَّدٌ_من_القرص_لحظةَ_الالتزام"
    QUOTED_INCOMING_NOT_REPRODUCED = "واردٌ_منقولٌ_غيرُ_مُعاد"


def _require_text(value: str, what: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise AuditCorpusError(f"{what} لا يكون فارغًا.")


@dataclass(frozen=True, slots=True)
class DepositedFigure:
    """رقمٌ في وديعةٍ بمصدره؛ والمصدرُ حقلٌ لازمٌ لا زينة."""

    name: str
    value: str
    provenance: FigureProvenance

    def __post_init__(self) -> None:
        _require_text(self.name, "اسمُ الرقم")
        _require_text(self.value, "قيمةُ الرقم")
        if not isinstance(self.provenance, FigureProvenance):
            raise AuditCorpusError("مصدرُ الرقم عضوٌ في `FigureProvenance`.")

    @property
    def is_generated(self) -> bool:
        """أمولَّدٌ من القرص؟ ولا يُرفَع واردٌ إلى مولَّدٍ إلّا بإعادة توليد."""

        return self.provenance is FigureProvenance.GENERATED_FROM_THE_DISK_AT_DEPOSIT


@dataclass(frozen=True, slots=True)
class DeclaredCorpus:
    """مدوّنةٌ مُودَعةٌ بدورها وختمها وإسنادها؛ والدورُ مُعلَنٌ لا مُستنبَط."""

    relative_path: str
    role: CorpusRole
    byte_length: int
    sha256_hex: str
    path_variable: str
    attribution: str

    def __post_init__(self) -> None:
        _require_text(self.relative_path, "مسارُ المدوّنة")
        _require_text(self.sha256_hex, "بصمةُ المدوّنة")
        _require_text(self.path_variable, "متغيّرُ مسار المدوّنة")
        _require_text(self.attribution, "نصُّ الإسناد")
        if not isinstance(self.role, CorpusRole):
            raise AuditCorpusError("دورُ المدوّنة عضوٌ في `CorpusRole`.")
        if self.byte_length < 1:
            raise AuditCorpusError("طولٌ دون الواحد ليس مدوّنة.")

    @property
    def name(self) -> str:
        return Path(self.relative_path).name


THE_MEASUREMENT_CORPUS: Final[DeclaredCorpus] = DeclaredCorpus(
    relative_path=QURAN_CORPUS_RELATIVE_PATH,
    role=CorpusRole.MEASUREMENT_CORPUS,
    byte_length=FROZEN_CORPUS.byte_length,
    sha256_hex=FROZEN_CORPUS.sha256_hex,
    path_variable=QURAN_CORPUS_PATH_VARIABLE,
    attribution=(
        "Quran text (`quran-simple-enhanced.txt`) from the Tanzil project, "
        "https://tanzil.net, licensed CC BY-ND 3.0. Verbatim copy, unmodified."
    ),
)
"""الأولى: ختمُها ودورُها مقروءان من مُجمَّد الشجرة لا مكتوبَين ههنا ثانيةً."""

AUDIT_CORPUS_RELATIVE_PATH: Final[str] = "corpora/globalquran-simple-enhanced.txt"
"""الموضعُ المسنونُ لبايتات مدوّنة التدقيق، باسمٍ يحمل مصدرَه لا باسمٍ يصطدم."""

AUDIT_CORPUS_PATH_VARIABLE: Final[str] = "ALGHANEM_AUDIT_CORPUS_PATH"
"""متغيّرُ البيئة الذي يُصرَّح به بالمسار حين تكون البايتاتُ خارج الشجرة."""

AUDIT_CORPUS_ATTRIBUTION: Final[str] = (
    "Quran text (`Quran/quran-simple-enhanced.txt`) from the GlobalQuran data "
    "repository, https://github.com/GlobalQuran/data, whose own footer names "
    "Tanzil.info as its source (ID `quran-simple-enhanced`, last update May 8, "
    "2016). Verbatim copy, unmodified; SHA-256 "
    "`8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215`, "
    "1,306,770 bytes."
)
"""إسنادُ مدوّنة التدقيق؛ وهو شرطُ رخصةٍ لا لطفَ عبارة، ولا يخرج رقمٌ بحذفه."""

THE_AUDIT_CORPUS: Final[DeclaredCorpus] = DeclaredCorpus(
    relative_path=AUDIT_CORPUS_RELATIVE_PATH,
    role=CorpusRole.AUDIT_CORPUS,
    byte_length=1_306_770,
    sha256_hex="8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215",
    path_variable=AUDIT_CORPUS_PATH_VARIABLE,
    attribution=AUDIT_CORPUS_ATTRIBUTION,
)
"""الثانية: بايتاتُ مدوّنة `hamil`، مُودَعةً بدور التدقيق لا بدور القياس."""

THE_DECLARED_CORPORA: Final[tuple[DeclaredCorpus, ...]] = (
    THE_MEASUREMENT_CORPUS,
    THE_AUDIT_CORPUS,
)

THE_UPSTREAM_NAME_COLLISION: Final[str] = "quran-simple-enhanced.txt"
"""الاسمُ المنبعيُّ المشترَك بين المُودَعَين، وبايتاتُهما مختلفة."""

THE_AUDIT_CORPUS_FIGURES: Final[tuple[DepositedFigure, ...]] = (
    DepositedFigure(
        name="طولُ البايتات",
        value="1306770",
        provenance=FigureProvenance.GENERATED_FROM_THE_DISK_AT_DEPOSIT,
    ),
    DepositedFigure(
        name="بصمةُ SHA-256",
        value="8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215",
        provenance=FigureProvenance.GENERATED_FROM_THE_DISK_AT_DEPOSIT,
    ),
    DepositedFigure(
        name="ختمُ كائن git للمصدر",
        value="7b9aed55b76cb724b670714c4ad3f537251cfeb7",
        provenance=FigureProvenance.GENERATED_FROM_THE_DISK_AT_DEPOSIT,
    ),
    DepositedFigure(
        name="الختمُ المنقول في PHASE1-STATUS",
        value="8b387e8",
        provenance=FigureProvenance.QUOTED_INCOMING_NOT_REPRODUCED,
    ),
)
"""أرقامُ الوديعة بمصادرها: ثلاثةٌ تُعاد من القرص، والرابعُ واردٌ يُسمّى واردًا.

والرابعُ يبقى موسومًا `QUOTED_INCOMING_NOT_REPRODUCED` وإن طابق: مصدرُ دخوله
الوديعةَ نقلٌ من عرضٍ خارجيّ، وموافقتُه ما ولَّده القرصُ تُسجَّل في
`the_quoted_seal_is_a_prefix_of_the_generated_digest` خبرًا عنه، ولا تُبدِّل
جنسَ دخوله بأثر رجعيّ.
"""


def vendored_audit_corpus_path() -> Path:
    """الموضعُ المسنونُ داخل الشجرة، محسوبًا لا مُخمَّنًا من `cwd`."""

    return repository_root_path() / AUDIT_CORPUS_RELATIVE_PATH


def audit_corpus_path(path: Path | str | None = None) -> Path:
    """مسارُ البايتات: المُمرَّرُ، وإلّا متغيّرُ البيئة، وإلّا المُودَعُ ههنا.

    والترتيبُ هو ترتيبُ `quran_corpus_path` و`masaq_path` نفسُه، ولا رابعَ له؛
    وغيابُ الثلاثة رفضٌ صريحٌ لا قيمةٌ افتراضيّة.
    """

    if path is not None:
        return Path(path)
    declared = os.environ.get(AUDIT_CORPUS_PATH_VARIABLE)
    if declared:
        return Path(declared)
    vendored = vendored_audit_corpus_path()
    if vendored.is_file():
        return vendored
    raise AuditCorpusError(
        "بايتاتُ مدوّنة التدقيق ليست في هذه الشجرة ولا صُرِّح بمسارها؛ فتُودَع "
        f"في `{AUDIT_CORPUS_RELATIVE_PATH}` أو يُصرَّح به في "
        f"`{AUDIT_CORPUS_PATH_VARIABLE}`، ولا يُخمَّن موضعُها."
    )


def audit_corpus_bytes_are_resolvable(path: Path | str | None = None) -> bool:
    """أيُحَلُّ مسارٌ إلى ملفٍّ **موجود** بالأبواب الثلاثة؟ وهو شرطُ التخطّي وحدَه."""

    try:
        resolved = audit_corpus_path(path)
    except AuditCorpusError:
        return False
    return resolved.is_file()


def read_audit_corpus_bytes(path: Path | str | None = None) -> bytes:
    """يقرأ البايتات ويُطابق الطولَ والبصمةَ معًا قبل أن يُسلِّمها.

    والموضعُ ليس شهادة: ملفٌّ بهذا الاسم في الموضع المسنون يُرفَض إن خالف،
    كما يُرفَض في أيّ مسارٍ آخر؛ والموافقةُ في الطول وحدَه لا تُغني عن البصمة.
    """

    resolved = audit_corpus_path(path)
    if not resolved.is_file():
        raise AuditCorpusError(f"لا ملفَّ في المسار المُحَلّ: {resolved}")
    data = resolved.read_bytes()
    if len(data) != THE_AUDIT_CORPUS.byte_length:
        raise AuditCorpusError(
            f"طولُ البايتات {len(data)} لا يطابق المُجمَّد "
            f"{THE_AUDIT_CORPUS.byte_length}"
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != THE_AUDIT_CORPUS.sha256_hex:
        raise AuditCorpusError(
            f"بصمةُ البايتات {digest} لا تطابق المُجمَّدة {THE_AUDIT_CORPUS.sha256_hex}"
        )
    return data


def git_blob_sha1(data: bytes) -> str:
    """ختمُ كائن git لهذه البايتات، محسوبًا ههنا لا منقولًا عن واجهة."""

    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data, usedforsecurity=False).hexdigest()


def regenerate_every_generated_figure(path: Path | str | None = None) -> dict[str, str]:
    """يُعيد توليدَ كلّ رقمٍ مولَّدٍ من البايتات، فيُقابَل المُودَعُ بالمقيس.

    ولا تُخرِج هذه الدالّةُ رقمًا بغير البايتات: غيابُها رفضُ إخراجٍ لا قيمةٌ
    افتراضيّة، كما في مدوّنة القياس سواءً بسواء.
    """

    data = read_audit_corpus_bytes(path)
    return {
        "طولُ البايتات": str(len(data)),
        "بصمةُ SHA-256": hashlib.sha256(data).hexdigest(),
        "ختمُ كائن git للمصدر": git_blob_sha1(data),
    }


def the_quoted_incoming_seal() -> DepositedFigure:
    """الرقمُ الواردُ وحدَه في هذه الوديعة، مأخوذًا بوسمه لا باسمه المكتوب."""

    return next(
        figure for figure in THE_AUDIT_CORPUS_FIGURES if not figure.is_generated
    )


def the_quoted_seal_is_a_prefix_of_the_generated_digest(
    path: Path | str | None = None,
) -> bool:
    """أيكون الختمُ المنقولُ `8b387e8` صدرَ البصمة المولَّدة من القرص؟

    والجوابُ ههنا **لا**، وهو مقيسٌ لا موصوف؛ ومقدارُ الموافقة في
    `the_quoted_seal_agreement_length`.
    """

    generated = regenerate_every_generated_figure(path)["بصمةُ SHA-256"]
    return generated.startswith(the_quoted_incoming_seal().value)


def the_quoted_seal_agreement_length(path: Path | str | None = None) -> int:
    """عددُ المحارف التي يوافق فيها المنقولُ صدرَ البصمة المولَّدة قبل أوّل فرق.

    فالموافقةُ الجزئيّةُ عددٌ يُخرَج، لا حكمُ «قريبٌ فيُقبَل» ولا «بعيدٌ فيُطرَح».
    """

    generated = regenerate_every_generated_figure(path)["بصمةُ SHA-256"]
    quoted = the_quoted_incoming_seal().value
    agreed = 0
    for ours, theirs in zip(generated, quoted, strict=False):
        if ours != theirs:
            break
        agreed += 1
    return agreed


def refuse_to_read_one_against_the_other(
    first: DeclaredCorpus, second: DeclaredCorpus
) -> None:
    """يَرفض مقابلةَ مدوّنتين مختلفتَي الختم؛ والرفضُ عند المحاولة لا بعدها.

    ولا استثناءَ للدور الواحد: مدوّنتان مختلفتا الختم لا تُجمَع أرقامُهما ولا
    تُطرَح ولو اتّحد دورُهما، وأشدُّ منه اختلافُ الدورين.
    """

    if first.sha256_hex == second.sha256_hex:
        return
    raise CrossRoleReading(
        f"`{first.relative_path}` ({first.role.value}) و`{second.relative_path}` "
        f"({second.role.value}) ختمان مختلفان بدورين معلنَين؛ فلا يُقاس أحدُهما "
        "على الآخر ولا يُجمَع رقمٌ من هذا إلى رقمٍ من ذاك."
    )


TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER: Final[str] = (
    "TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER: في موضع "
    "الإيداع مدوّنتان، لكلٍّ ختمٌ ودورٌ مُعلَنٌ قبل القراءة: الأولى مدوّنةُ "
    "القياس تُنسَب إليها أرقامُنا، والثانيةُ مدوّنةُ التدقيق تُفحَص بها أرقامُ "
    "برنامجٍ آخرَ على بايتاته هو؛ ولا رقمَ من إحداهما يُجمَع إلى رقمٍ من الأخرى "
    "ولا يُطرَح، و`refuse_to_read_one_against_the_other` تَرفض المقابلةَ عند "
    "أوّل محاولةٍ لا بعد خروج رقمٍ منها"
)

THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES: Final[str] = (
    "THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES: اسمُ المُودَعَين المنبعيُّ واحدٌ "
    f"(`{THE_UPSTREAM_NAME_COLLISION}`) وبايتاتُهما مختلفةٌ طولًا وبصمة، فلو "
    "نزلت الثانيةُ باسمها المنبعيّ لأطاحت بالأولى بلا رسالةِ خطأٍ واحدة؛ ولذلك "
    "سُنَّ لها اسمٌ يحمل مصدرَه، والاتّحادُ في الاسم لا يُقرأ اتّحادًا في النصّ"
)

NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT: Final[str] = (
    "NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT: كلُّ رقمٍ في وديعةٍ "
    "يولَّد من القرص لحظةَ الالتزام ويُعاد توليدُه في "
    "`regenerate_every_generated_figure`، أو يُسمّى `QUOTED_INCOMING_NOT_"
    "REPRODUCED` فلا يُقرأ مقيسًا؛ وهذا محضرُ «الدرجة الثالثة عند القياس» "
    "مُدوَّنًا إجراءً: هناك خرج 16,796 مقيسًا حيث كان المنقولُ 16,781، فالمنقولُ "
    "ينفصل عن المقيس بلا أن يسقط شاهد"
)

THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS: Final[str] = (
    "THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS: `8b387e8` طُلِب كائنًا في مستودعٍ "
    "فلم يكن كائنًا صالحًا، فسُجِّل أنّه ختمُ ذاك المستودع؛ وهو — بالتوليد من "
    "القرص عند الاستقبال — صدرُ بصمة SHA-256 لبايتات مدوّنة التدقيق نفسِها. "
    "فالخللُ في جنس المطلوب مقيسٌ لا موصوف، ويُسجَّل ولا يُبتلَع صمتًا"
)

A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH: Final[str] = (
    "A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH: المنقولُ `8b387e8` ليس صدرًا "
    "للبصمة المولَّدة من القرص: يوافقها في ستّة محارفَ ويفترق في السابع، "
    "و`the_quoted_seal_agreement_length` تُخرِج الستّةَ عددًا لا وصفًا. "
    "فالموافقةُ الجزئيّةُ لا تُقرأ مطابقةً ولا تُرقّي واردًا إلى مولَّد، ونسبةُ "
    "الفرق إلى زلّة نقلٍ أو إلى ختمِ شيءٍ آخر مرفوضةٌ لانعدام طرفهم ههنا"
)

AUDIT_CORPUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER": (
        TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER
    ),
    "THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES": (
        THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES
    ),
    "NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT": (
        NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT
    ),
    "THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS": THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS,
    "A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH": (
        A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH
    ),
}


def _verify_no_declared_corpus_carries_a_verdict_field() -> None:
    """مبرهنة: لا حقلَ حكمٍ ولا حقلَ «مُتحقَّقٍ منه» في أنواع هذه الوديعة."""

    for _dataclass in (DeclaredCorpus, DepositedFigure):
        for _field in fields(_dataclass):
            if any(token in _field.name for token in ("verdict", "verified", "status")):
                raise RuntimeError("a deposited type carries a hand-written verdict")


def _verify_the_two_corpora_are_distinct_in_seal_and_in_role() -> None:
    """مبرهنة: ختمان مختلفان ودوران مختلفان؛ وهي بنيةٌ لا واقعةٌ مؤرَّخة."""

    seals = {corpus.sha256_hex for corpus in THE_DECLARED_CORPORA}
    roles = {corpus.role for corpus in THE_DECLARED_CORPORA}
    if len(seals) != len(THE_DECLARED_CORPORA):
        raise RuntimeError("two declared corpora share one seal")
    if len(roles) != len(THE_DECLARED_CORPORA):
        raise RuntimeError("two declared corpora share one role")
    names = {corpus.name for corpus in THE_DECLARED_CORPORA}
    if len(names) != len(THE_DECLARED_CORPORA):
        raise RuntimeError("two declared corpora share one deposited name")


_verify_no_declared_corpus_carries_a_verdict_field()
_verify_the_two_corpora_are_distinct_in_seal_and_in_role()
