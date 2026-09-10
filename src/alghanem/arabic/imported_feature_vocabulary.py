"""عقد استيراد مفردةٍ مُجمَّدة عند مصدرها الأجنبي، لا ترقيةَ تجميدٍ لها.

سجَّل طلب الدمج #64 الثغرة باسمها: استيراد مفردات المصدر عبر المشاريع
"يحتاجها مُجمَّدةً قابلةً للتصدير عند مصدرها، وعقدَ استيرادٍ هنا؛ ولا واحد
منهما قائم". وقد صار النصف الأول قائمًا فعلًا: مشروع `GFLK-Taaqol-GPT`
يُصدِّر مفردة `gflk.origin_type.v1` عن دفتر `ORIGIN_LEDGER_AR_v1`، ببصمة
محتوًى حتمية ونطاق تجميدٍ مُصرَّح به `FROZEN_LOCAL`. وهذه الوحدة هي النصف
الثاني: عقد الاستيراد داخل الغانم.

الحدّ الذي تحرسه هذه الوحدة كلّها:

```
ForeignFrozenExport != LocalFreeze
ImportedVocabulary  != BornOntology
DerivedDistribution != DeclaredResult
verified content_id != granted authority
```

وهو `A0.PP.1b` (`Canonicalization != Authority`) مرفوعًا درجةً واحدة:
استيراد بايتات يَنقل **هوية محتوًى متحقَّقًا منها**، ولا يَنقل إذنًا البتّة.

وتفصيل ذلك بلا تلطيف:

* **`FROZEN_LOCAL` نطاقٌ أجنبيّ يُقرَأ ولا يُرقَّى**: لا دالّة هنا تحوّله إلى
  `SpecificationFreeze.FROZEN`، ولا إلى `Freeze` أو `E0` أو ولادةٍ في النواة.
  إعلانه في المفردة تصريحٌ بمصدر السلطة، لا اعترافٌ بها.
* **التوزيع مشتقٌّ لا مكتوب**: عدد كل نوع أصل يُحسَب من المُدخَلات نفسها،
  ويُرفَض أيّ توزيعٍ مُعلَنٍ يخالف المشتقّ. وهو الدرس عينه الذي تقوم عليه
  `readiness_rank`: لا حقلَ يُكتَب فيه الحكم مباشرةً.
* **البصمة تُعاد اشتقاقًا لا تُصدَّق**: `ImportedVocabularyContentVerifier`
  هو المُصدِر الوحيد لِـ`VerifiedVocabularyImport`، ويُعيد ترميز المُدخَلات
  عبر `alghanem.canonical_content` وحدها -- لا نسخة ثانية من قاعدة الترميز،
  لأن نسختين قاعدتان تنحرفان.
* **جنس الدليل مربوط**: لا تُبنى مفردةٌ مستوردة بغير
  `EvidenceGenus.MORPHO_FUNCTIONAL`؛ وهو الربط الذي سمّاه #64 مفقودًا.

ونطاق الوحدة وحدوده، مسجَّلةً لا مؤجَّلةً بالصمت:

* هذه **ليست** Workstream B: مفردةٌ مستورَدة من مشروعٍ آخر ليست مفردةً
  **مولودة** هنا، والسمات التوزيعية الخمس و`RECORDED_PROBE_REPORT` لا يمسّها
  هذا العقد ولا بايتًا واحدًا.
* النطاق ضيّقٌ عمدًا على `OriginType` وحده: مفردتا الوزن والبناء لم تُصدَّرا
  بعد، وبناء هيكلٍ عامّ يفترضهما قبل وجودهما اقتصادٌ قبل تعيين.
* لا سلطة نواة: لا نوع في `kernel/`، ولا بوّابة تقرأ شيئًا من هنا، وهو ما
  يفحصه اختبارٌ يمسح كل وحدات `kernel/`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Final

from alghanem.canonical_content import (
    CANONICAL_HASH_ALGORITHM,
    canonical_bytes,
    canonical_digest,
    is_canonical_digest,
)

from .probe_preregistration import EvidenceGenus

_IMPORT_TOKEN = object()

LOCAL_CANONICALIZATION_VERSION: Final = "imported-origin-type-vocabulary-v1"

SOURCE_PROJECT: Final = "GFLK-Taaqol-GPT"
SOURCE_LEDGER_ID: Final = "ORIGIN_LEDGER_AR_v1"
SOURCE_VOCABULARY_ID: Final = "gflk.origin_type.v1"
SOURCE_CANONICALIZATION_VERSION: Final = "gflk.canonical.v1"
SOURCE_DECLARED_CONTENT_ID: Final = (
    "facf6720dc3f55f7079b061d0375cf7a82f9093fcea64a1cd7f4a429d03ba85f"
)
EXPECTED_ROW_COUNT: Final = 270


class ImportedFeatureVocabularyError(ValueError):
    """رُفض استيرادٌ خارج العقد؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


class ForeignFreezeScope(Enum):
    """نطاق تجميدٍ أجنبيّ يُقرَأ كما صُرِّح به؛ قيمةٌ واحدة لا تُرقَّى."""

    FROZEN_LOCAL = "FROZEN_LOCAL"


class ImportedOriginType(Enum):
    """أنواع الأصل المستورَدة المغلقة؛ `UNRESOLVED` عضوٌ لا ثغرة."""

    EVENT = "ORIGIN_TYPE_EVENT"
    ENTITY = "ORIGIN_TYPE_ENTITY"
    UNRESOLVED = "ORIGIN_TYPE_UNRESOLVED"


if len(ForeignFreezeScope) != 1:  # pragma: no cover - guard
    raise RuntimeError("exactly one foreign freeze scope is declared here")
if len(ImportedOriginType) != 3:  # pragma: no cover - guard
    raise RuntimeError("the imported origin-type vocabulary is three-valued")


EXPECTED_DISTRIBUTION: Final = {
    ImportedOriginType.EVENT: 126,
    ImportedOriginType.ENTITY: 56,
    ImportedOriginType.UNRESOLVED: 88,
}

_PINNED_TOTAL = sum(EXPECTED_DISTRIBUTION.values())
if _PINNED_TOTAL != EXPECTED_ROW_COUNT:  # pragma: no cover - guard
    raise RuntimeError("the pinned distribution must exhaust the pinned row count")


IMPORT_CONTRACT_NOTE: Final = (
    "المستورَد مفردةُ أنواع أصلٍ واحدة (gflk.origin_type.v1) عن دفتر "
    "ORIGIN_LEDGER_AR_v1 في مشروع GFLK-Taaqol-GPT، مُجمَّدةً عند مصدرها "
    "بنطاقه هو (FROZEN_LOCAL) لا بنطاقنا، مربوطةً بجنس الدليل الصرفي "
    "الوظيفي، مُعادَ اشتقاق هوية محتواها هنا لا مُصدَّقةً بدعواها"
)

FOREIGN_SCOPE_IS_NOT_LOCAL_FREEZE_NOTE: Final = (
    "نطاق التجميد الأجنبي FROZEN_LOCAL يُقرَأ ولا يُرقَّى: لا يصير "
    "SpecificationFreeze.FROZEN ولا Freeze ولا E0 ولا ولادةً، فترقيته "
    "ادّعاءُ بوّابةٍ لا نملكها -- ولا دالّة في هذه الوحدة تُجريها"
)

IMPORT_AUTHORITY_NOTE: Final = (
    "استيرادٌ وتوثيق فقط: لا يُنتج هذا العقد ولادةً ولا حكم ولادة، ولا "
    "يُجمَّد في النواة، ولا تقرأه أيّ بوّابة فيها"
)

IMPORTED_VOCABULARY_IS_NOT_BORN_NOTE: Final = (
    "المفردة المستورَدة ليست مفردةً مولودة هنا: ولادة مفردة سماتٍ صرفية "
    "وظيفية في الغانم تحتاج تجربةً مُجمَّدة قبل دليلها لم تُنشأ بعد، "
    "والاستيراد لا يقوم مقامها"
)

SOURCE_DIGEST_REDERIVATION_NOTE: Final = (
    "بصمة المصدر (gflk.canonical.v1) مُسجَّلة كما صُرِّح بها، وإعادة اشتقاقها "
    "هنا تحتاج مخطَّط ترميزها بدقّة البايت وحمولته الكاملة؛ فحتى يُودَعا في "
    "هذا المستودع تبقى مقارنةً بمرجعٍ مُثبَّت لا إعادةَ حسابٍ مستقلّة، "
    "والبصمة المُعاد اشتقاقها فعليًّا هي بصمة الغانم المحلّية وحدها"
)

_RESULT_BEARING_FIELD_MARKERS: Final = (
    "result",
    "outcome",
    "answer",
    "verdict",
    "conclusion",
    "decision",
    "birth",
    "promotion",
)

_ORIGIN_TYPE_BY_VALUE: Final = {member.value: member for member in ImportedOriginType}


def _require_non_blank(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ImportedFeatureVocabularyError(f"{field_name} نصٌّ غير فارغ")
    return value


def canonical_origin_type(value: object) -> ImportedOriginType:
    """أعِد نوع الأصل المسمّى بقيمته المصدرية، أو ارفض ما خرج عن المفردة."""

    if isinstance(value, ImportedOriginType):
        return value
    member = _ORIGIN_TYPE_BY_VALUE.get(value) if isinstance(value, str) else None
    if member is None:
        allowed = "، ".join(member.value for member in ImportedOriginType)
        raise ImportedFeatureVocabularyError(
            "نوع الأصل must come from the closed vocabulary: " + allowed
        )
    return member


@dataclass(frozen=True, slots=True)
class ImportedVocabularyEntry:
    """مُدخَلٌ واحد من المفردة المستورَدة، بتصنيفه الخام كما ورد."""

    root: str
    origin_type: ImportedOriginType
    raw_category: str
    batch_note: str

    def __post_init__(self) -> None:
        _require_non_blank(self.root, "الجذر")
        _require_non_blank(self.raw_category, "التصنيف الخام")
        _require_non_blank(self.batch_note, "ملاحظة الدفعة")
        if not isinstance(self.origin_type, ImportedOriginType):
            raise ImportedFeatureVocabularyError(
                "نوع الأصل must come from the closed vocabulary"
            )


@dataclass(frozen=True, slots=True)
class ImportedFeatureVocabulary:
    """مفردةٌ مستورَدة كاملة، مربوطةً بجنسها، وتوزيعُها مشتقٌّ لا مكتوب."""

    vocabulary_id: str
    evidence_genus: EvidenceGenus
    source_project: str
    source_ledger_id: str
    source_canonicalization_version: str
    source_declared_content_id: str
    freeze_scope: ForeignFreezeScope
    declared_row_count: int
    declared_distribution: tuple[tuple[ImportedOriginType, int], ...]
    entries: tuple[ImportedVocabularyEntry, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.vocabulary_id, "معرّف المفردة")
        _require_non_blank(self.source_project, "المشروع المصدر")
        _require_non_blank(self.source_ledger_id, "معرّف الدفتر المصدر")
        _require_non_blank(
            self.source_canonicalization_version, "إصدار الترميز القانوني المصدر"
        )
        if not isinstance(self.evidence_genus, EvidenceGenus):
            raise ImportedFeatureVocabularyError(
                "جنس الدليل must come from the closed vocabulary"
            )
        if self.evidence_genus is not EvidenceGenus.MORPHO_FUNCTIONAL:
            raise ImportedFeatureVocabularyError(
                "المفردة المستورَدة مربوطةٌ بالجنس الصرفي الوظيفي وحده؛ "
                "واستيرادها تحت جنسٍ آخر ادّعاءُ نطاقٍ غير مبرهَن"
            )
        if not isinstance(self.freeze_scope, ForeignFreezeScope):
            raise ImportedFeatureVocabularyError(
                "نطاق التجميد must come from the closed vocabulary"
            )
        if not is_canonical_digest(self.source_declared_content_id):
            raise ImportedFeatureVocabularyError("بصمة المصدر المُعلَنة غير سليمة")
        if not isinstance(self.entries, tuple) or not self.entries:
            raise ImportedFeatureVocabularyError("المُدخَلات تُعلَن مجموعةً غير فارغة")
        for entry in self.entries:
            if type(entry) is not ImportedVocabularyEntry:
                raise ImportedFeatureVocabularyError("كل مُدخَلٍ من نوع المُدخَل المستورَد")
        roots = [entry.root for entry in self.entries]
        if len(set(roots)) != len(roots):
            raise ImportedFeatureVocabularyError(
                "تكرّر جذرٌ واحد في المفردة المستورَدة؛ والتكرار يُخفي مُدخَلًا "
                "مختلفًا تحت هوية غيره"
            )
        if (
            not isinstance(self.declared_row_count, int)
            or isinstance(self.declared_row_count, bool)
            or self.declared_row_count != len(self.entries)
        ):
            raise ImportedFeatureVocabularyError(
                "عدد الصفوف المُعلَن يخالف عدد المُدخَلات المستورَدة فعلًا"
            )
        if not isinstance(self.declared_distribution, tuple):
            raise ImportedFeatureVocabularyError("التوزيع المُعلَن يُعلَن مجموعةً مرتَّبة")
        declared: dict[ImportedOriginType, int] = {}
        for item in self.declared_distribution:
            if (
                not isinstance(item, tuple)
                or len(item) != 2
                or not isinstance(item[0], ImportedOriginType)
                or not isinstance(item[1], int)
                or isinstance(item[1], bool)
                or item[1] < 0
            ):
                raise ImportedFeatureVocabularyError(
                    "كل بندٍ في التوزيع المُعلَن زوجُ نوعِ أصلٍ وعددٍ غير سالب"
                )
            if item[0] in declared:
                raise ImportedFeatureVocabularyError("تكرّر نوع أصلٍ في التوزيع المُعلَن")
            declared[item[0]] = item[1]
        if declared != dict(self.derived_distribution):
            raise ImportedFeatureVocabularyError(
                "التوزيع المُعلَن يخالف التوزيع المشتقّ من المُدخَلات؛ والتوزيع "
                "يُحسَب من الصفوف ولا يُكتَب فوقها"
            )

    @property
    def derived_distribution(self) -> tuple[tuple[ImportedOriginType, int], ...]:
        """التوزيع محسوبًا من المُدخَلات نفسها، بكل نوعٍ ولو كان صفرًا."""

        counts = {member: 0 for member in ImportedOriginType}
        for entry in self.entries:
            counts[entry.origin_type] += 1
        return tuple((member, counts[member]) for member in ImportedOriginType)

    @property
    def row_count(self) -> int:
        """عدد الصفوف المشتقّ من المُدخَلات."""

        return len(self.entries)


@dataclass(frozen=True, slots=True)
class LocalVocabularyContentIdentity:
    """بصمةُ الغانم لمحتوى مفردةٍ مستورَدة؛ لا تصدر إلا عن المتحقِّق."""

    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _IMPORT_TOKEN:
            raise ImportedFeatureVocabularyError(
                "بصمة المحتوى المحلّية لا تصدر إلا عن "
                "ImportedVocabularyContentVerifier"
            )
        if (
            self.algorithm != CANONICAL_HASH_ALGORITHM
            or self.canonicalization_version != LOCAL_CANONICALIZATION_VERSION
            or not is_canonical_digest(self.digest)
        ):
            raise ImportedFeatureVocabularyError("بصمة المحتوى المحلّية غير سليمة")


@dataclass(frozen=True, slots=True)
class VerifiedVocabularyImport:
    """استيرادٌ أُعيد اشتقاق محتواه محلّيًّا؛ لا يصدر إلا عن المتحقِّق."""

    vocabulary: ImportedFeatureVocabulary
    content_bytes: bytes
    local_content_id: LocalVocabularyContentIdentity
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _IMPORT_TOKEN:
            raise ImportedFeatureVocabularyError(
                "الاستيراد المتحقَّق منه لا يصدر إلا عن المتحقِّق"
            )
        if canonical_digest(self.content_bytes) != self.local_content_id.digest:
            raise ImportedFeatureVocabularyError("بايتات الاستيراد تخالف بصمته المحلّية")

    @property
    def source_declared_content_id(self) -> str:
        """بصمة المصدر كما صُرِّح بها؛ مُسجَّلة لا مُرقَّاة إلى سلطة."""

        return self.vocabulary.source_declared_content_id


class ImportedVocabularyContentVerifier:
    """المُصدِر الوحيد للاستيراد المتحقَّق منه؛ يُعيد الاشتقاق ولا يُصدِّق دعوى."""

    COVERAGE: Final = (
        "vocabulary_id",
        "evidence_genus",
        "source_project",
        "source_ledger_id",
        "source_canonicalization_version",
        "source_declared_content_id",
        "freeze_scope",
        "declared_row_count",
        "declared_distribution",
        "entries",
    )

    ENTRY_COVERAGE: Final = ("root", "origin_type", "raw_category", "batch_note")

    @classmethod
    def verify(cls, vocabulary: ImportedFeatureVocabulary) -> VerifiedVocabularyImport:
        """أعِد اشتقاق محتوى المفردة محلّيًّا، وأصدِر استيرادًا متحقَّقًا منه."""

        if type(vocabulary) is not ImportedFeatureVocabulary:
            raise ImportedFeatureVocabularyError("التحقّق يلزمه مفردةٌ مستورَدة")
        cls._assert_schema_coverage()
        encoded = {
            "declared_distribution": [
                [member.name, count]
                for member, count in vocabulary.derived_distribution
            ],
            "declared_row_count": vocabulary.row_count,
            "entries": [
                {
                    "batch_note": entry.batch_note,
                    "origin_type": entry.origin_type.name,
                    "raw_category": entry.raw_category,
                    "root": entry.root,
                }
                for entry in vocabulary.entries
            ],
            "evidence_genus": vocabulary.evidence_genus.name,
            "freeze_scope": vocabulary.freeze_scope.name,
            "source_canonicalization_version": (
                vocabulary.source_canonicalization_version
            ),
            "source_declared_content_id": vocabulary.source_declared_content_id,
            "source_ledger_id": vocabulary.source_ledger_id,
            "source_project": vocabulary.source_project,
            "version": LOCAL_CANONICALIZATION_VERSION,
            "vocabulary_id": vocabulary.vocabulary_id,
        }
        content = canonical_bytes(encoded)
        local_content_id = LocalVocabularyContentIdentity(
            algorithm=CANONICAL_HASH_ALGORITHM,
            canonicalization_version=LOCAL_CANONICALIZATION_VERSION,
            digest=canonical_digest(content),
            _token=_IMPORT_TOKEN,
        )
        return VerifiedVocabularyImport(
            vocabulary=vocabulary,
            content_bytes=content,
            local_content_id=local_content_id,
            _token=_IMPORT_TOKEN,
        )

    @classmethod
    def _assert_schema_coverage(cls) -> None:
        declared = {item.name for item in fields(ImportedFeatureVocabulary)}
        if declared != set(cls.COVERAGE):
            raise RuntimeError(
                "the local canonical encoding must explicitly account for every "
                "imported vocabulary field"
            )
        entry_declared = {item.name for item in fields(ImportedVocabularyEntry)}
        if entry_declared != set(cls.ENTRY_COVERAGE):
            raise RuntimeError(
                "the local canonical encoding must explicitly account for every "
                "imported entry field"
            )


def vocabulary_from_export_mapping(payload: Mapping[str, Any]) -> (
    ImportedFeatureVocabulary
):
    """اقرأ حمولة تصديرٍ مصدرية، وارفض كل ما خرج عن المفردات المغلقة."""

    if not isinstance(payload, Mapping):
        raise ImportedFeatureVocabularyError("حمولة التصدير خريطةٌ من مفاتيح ونصوص")
    missing = {
        "vocabulary_id",
        "genus",
        "source_project",
        "source_ledger_id",
        "row_count",
        "content_id",
        "canonicalization_version",
        "freeze_scope",
        "declared_distribution",
        "entries",
    } - set(payload)
    if missing:
        raise ImportedFeatureVocabularyError(
            "حمولة التصدير ينقصها حقلٌ مُلزَم: " + "، ".join(sorted(missing))
        )
    genus_name = payload["genus"]
    if genus_name not in {member.name for member in EvidenceGenus}:
        raise ImportedFeatureVocabularyError(
            "جنس الدليل must come from the closed vocabulary"
        )
    scope_name = payload["freeze_scope"]
    if scope_name not in {member.name for member in ForeignFreezeScope}:
        raise ImportedFeatureVocabularyError(
            "نطاق التجميد must come from the closed vocabulary"
        )
    raw_entries = payload["entries"]
    if not isinstance(raw_entries, list | tuple) or not raw_entries:
        raise ImportedFeatureVocabularyError("مُدخَلات التصدير قائمةٌ غير فارغة")
    entries = tuple(
        ImportedVocabularyEntry(
            root=_require_non_blank(_field(raw, "root"), "الجذر"),
            origin_type=canonical_origin_type(_field(raw, "origin_type")),
            raw_category=_require_non_blank(
                _field(raw, "raw_category"), "التصنيف الخام"
            ),
            batch_note=_require_non_blank(_field(raw, "batch_note"), "ملاحظة الدفعة"),
        )
        for raw in raw_entries
    )
    raw_distribution = payload["declared_distribution"]
    if not isinstance(raw_distribution, Mapping):
        raise ImportedFeatureVocabularyError("التوزيع المُعلَن خريطةٌ من نوعٍ إلى عدد")
    declared_distribution = tuple(
        (member, int(raw_distribution.get(member.value, 0)))
        for member in ImportedOriginType
    )
    unknown = set(raw_distribution) - {member.value for member in ImportedOriginType}
    if unknown:
        raise ImportedFeatureVocabularyError(
            "التوزيع المُعلَن يذكر نوع أصلٍ خارج المفردة: " + "، ".join(sorted(unknown))
        )
    return ImportedFeatureVocabulary(
        vocabulary_id=payload["vocabulary_id"],
        evidence_genus=EvidenceGenus[genus_name],
        source_project=payload["source_project"],
        source_ledger_id=payload["source_ledger_id"],
        source_canonicalization_version=payload["canonicalization_version"],
        source_declared_content_id=payload["content_id"],
        freeze_scope=ForeignFreezeScope[scope_name],
        declared_row_count=payload["row_count"],
        declared_distribution=declared_distribution,
        entries=entries,
    )


def _field(raw: object, name: str) -> object:
    if not isinstance(raw, Mapping) or name not in raw:
        raise ImportedFeatureVocabularyError(f"مُدخَل التصدير ينقصه الحقل {name}")
    return raw[name]


def assert_matches_recorded_release(vocabulary: ImportedFeatureVocabulary) -> None:
    """ارفض استيرادًا يخالف الإصدار المُثبَّت بأعداده وهويّته وبصمة مصدره."""

    if type(vocabulary) is not ImportedFeatureVocabulary:
        raise ImportedFeatureVocabularyError("المطابقة تلزمها مفردةٌ مستورَدة")
    if vocabulary.vocabulary_id != SOURCE_VOCABULARY_ID:
        raise ImportedFeatureVocabularyError("معرّف المفردة يخالف الإصدار المُثبَّت")
    if vocabulary.source_project != SOURCE_PROJECT:
        raise ImportedFeatureVocabularyError("المشروع المصدر يخالف الإصدار المُثبَّت")
    if vocabulary.source_ledger_id != SOURCE_LEDGER_ID:
        raise ImportedFeatureVocabularyError("الدفتر المصدر يخالف الإصدار المُثبَّت")
    if vocabulary.source_canonicalization_version != SOURCE_CANONICALIZATION_VERSION:
        raise ImportedFeatureVocabularyError(
            "إصدار الترميز القانوني المصدر يخالف الإصدار المُثبَّت"
        )
    if vocabulary.source_declared_content_id != SOURCE_DECLARED_CONTENT_ID:
        raise ImportedFeatureVocabularyError("بصمة المصدر تخالف الإصدار المُثبَّت")
    if vocabulary.row_count != EXPECTED_ROW_COUNT:
        raise ImportedFeatureVocabularyError(
            "عدد الصفوف يخالف الإصدار المُثبَّت؛ فالاستيراد يُرفَض ولا يمرّ صامتًا"
        )
    if dict(vocabulary.derived_distribution) != EXPECTED_DISTRIBUTION:
        raise ImportedFeatureVocabularyError(
            "التوزيع المشتقّ يخالف الإصدار المُثبَّت؛ فالاستيراد يُرفَض ولا يمرّ صامتًا"
        )


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


_assert_no_fields_matching(
    ImportedFeatureVocabulary,
    _RESULT_BEARING_FIELD_MARKERS,
    "an imported vocabulary may not carry a result, verdict, or birth field",
)
_assert_no_fields_matching(
    ImportedVocabularyEntry,
    _RESULT_BEARING_FIELD_MARKERS,
    "an imported entry may not carry a result, verdict, or birth field",
)


__all__ = [
    "EXPECTED_DISTRIBUTION",
    "EXPECTED_ROW_COUNT",
    "FOREIGN_SCOPE_IS_NOT_LOCAL_FREEZE_NOTE",
    "IMPORTED_VOCABULARY_IS_NOT_BORN_NOTE",
    "IMPORT_AUTHORITY_NOTE",
    "IMPORT_CONTRACT_NOTE",
    "LOCAL_CANONICALIZATION_VERSION",
    "SOURCE_CANONICALIZATION_VERSION",
    "SOURCE_DECLARED_CONTENT_ID",
    "SOURCE_DIGEST_REDERIVATION_NOTE",
    "SOURCE_LEDGER_ID",
    "SOURCE_PROJECT",
    "SOURCE_VOCABULARY_ID",
    "ForeignFreezeScope",
    "ImportedFeatureVocabulary",
    "ImportedFeatureVocabularyError",
    "ImportedOriginType",
    "ImportedVocabularyContentVerifier",
    "ImportedVocabularyEntry",
    "LocalVocabularyContentIdentity",
    "VerifiedVocabularyImport",
    "assert_matches_recorded_release",
    "canonical_origin_type",
    "vocabulary_from_export_mapping",
]
