"""إعادة اشتقاق بصمة المصدر بدقّة البايت، لا تصديقُ رقمٍ مُعلَن.

سجَّل طلب الدمج ‎#65‎ الثغرة باسمها: بصمة المصدر ‎`gflk.canonical.v1`‎ كانت
"مرجعًا مُصرَّحًا به لا مُعادَ حسابه استقلالًا"، لأن مخطَّط ترميزها بدقّة
البايت لم يكن مودَعًا في هذا المستودع. وهذه الوحدة تُودِعه صراحةً:

```
١) لكل مُدخَل حقلان اثنان لا غير: الجذر ونوع الأصل بقيمته المصدرية
٢) يُفصَل الحقلان بـ"\\x1f"                    — U+001F حرفيًّا
٣) تُرتَّب المُدخَلات بالجذر، وتُدمَج الأسطر بـ"\\x1e" — U+001E حرفيًّا
٤) UTF-8 encode، بلا BOM، بلا تطبيع Unicode إضافي
٥) sha256 على البايتات الناتجة
```

والحدّ الذي تحرسه الوحدة هو حدّ الوحدة الأمّ نفسه، غير منقوص:

```
verified content_id != granted authority
rederived digest    != foreign freeze promoted
```

إعادة الاشتقاق تُثبت أن البايتات هي هي، ولا تمنح إذنًا ولا تُرقّي
`FROZEN_LOCAL` إلى تجميدٍ محلّي ولا إلى ولادة.

وما تُصرِّح به هذه الوحدة عن حدودها، مسجَّلًا لا مطويًّا بالصمت:

* المخطَّط مُودَعٌ هنا، والحمولة المصدرية الكاملة (٢٧٠ صفًّا) ليست في هذا
  المستودع بعد. فمتى أُودعت، تُعيد `verify_export_payload` اشتقاق
  `SOURCE_DECLARED_CONTENT_ID` منها فعلًا؛ وحتى تُودَع، تبقى الآلة قائمةً
  مُختبَرةً على مُدخَلاتٍ مرجعية، لا دعوى تحقّقٍ على بياناتٍ غائبة.
* الفواصل تُرفَض داخل الحقول رفضًا صريحًا: جذرٌ يحوي `\\x1f` أو `\\x1e`
  يُنتج بايتاتٍ يقرؤها المُتحقِّق مُدخَلَين، فتصير بصمةٌ واحدةٌ لمحتويين
  مختلفين — وهو خلطُ هوياتٍ لا خطأُ تنسيق.
* التطبيع ممنوع هنا قصدًا: التصدير المصدري لا يُطبِّع، فتطبيعُنا نحن يجعل
  بصمتنا بصمةَ نصٍّ آخر ثم يُسمّي الاختلاف تطابقًا.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any, Final

from alghanem.canonical_content import (
    CANONICAL_HASH_ALGORITHM,
    canonical_digest,
    is_canonical_digest,
)

from .imported_feature_vocabulary import (
    EXPECTED_ROW_COUNT,
    SOURCE_CANONICALIZATION_VERSION,
    SOURCE_DIGEST_COVERED_FIELDS,
    ImportedFeatureVocabulary,
    ImportedFeatureVocabularyError,
    ImportedOriginType,
    assert_matches_recorded_release,
    vocabulary_from_export_mapping,
)

_SOURCE_DIGEST_TOKEN = object()

SOURCE_FIELD_SEPARATOR: Final = "\x1f"
SOURCE_RECORD_SEPARATOR: Final = "\x1e"
SOURCE_TEXT_ENCODING: Final = "utf-8"

SOURCE_DIGEST_SCHEMA_NOTE: Final = (
    "مخطَّط بصمة المصدر gflk.canonical.v1: حقلا كل مُدخَل (الجذر ثم قيمة نوع "
    "الأصل) يُفصَلان بـU+001F، والمُدخَلات تُرتَّب بالجذر وتُدمَج بـU+001E، "
    "ثم تُرمَّز UTF-8 بلا BOM وبلا تطبيع Unicode إضافي، وتُهشَّم بـsha256"
)

SOURCE_PAYLOAD_ABSENCE_NOTE: Final = (
    "المخطَّط مُودَعٌ هنا وقابلٌ للتشغيل، والحمولة المصدرية الكاملة ليست في "
    "هذا المستودع بعد؛ فإيداعها يجعل مطابقة SOURCE_DECLARED_CONTENT_ID إعادةَ "
    "حسابٍ مستقلّة فعلًا، وغيابها لا يُبدَّل بدعوى تحقّقٍ على بياناتٍ غائبة"
)

REDERIVATION_IS_NOT_AUTHORITY_NOTE: Final = (
    "إعادة اشتقاق بصمة المصدر تُثبت هوية بايتاتٍ ولا تمنح إذنًا: لا تُرقّي "
    "FROZEN_LOCAL إلى تجميدٍ محلّي، ولا تُنشئ ولادةً، ولا تقرأها بوّابةُ نواة"
)

MISMATCH_CAUSE_NOTE: Final = (
    "عدم التطابق سببه أحد أمرين لا ثالث لهما هنا، ولا يُخلَطان: (١) الحمولة "
    "المقروءة ليست حمولة الإصدار المُثبَّت — جذرٌ أو نوع أصلٍ تغيَّر أو زِيد "
    "أو نقص؛ (٢) الحمولة هي هي والمخطَّط المُطبَّق مختلف — ترتيبٌ أو فاصلٌ أو "
    "ترميزٌ أو تطبيعٌ غير المُودَع في هذه الوحدة"
)


class SourceDigestSchemaError(ImportedFeatureVocabularyError):
    """مُدخَلٌ خارج ما يقبله مخطَّط بصمة المصدر؛ لا يُحمَل على أقرب صيغة."""


class SourceDigestMismatchError(ImportedFeatureVocabularyError):
    """بصمةٌ مُعادُ اشتقاقها تخالف المُعلَنة؛ تُرفَض ولا تمرّ صامتة."""


def _require_source_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceDigestSchemaError(f"{field_name} نصٌّ غير فارغ")
    for separator, name in (
        (SOURCE_FIELD_SEPARATOR, "U+001F"),
        (SOURCE_RECORD_SEPARATOR, "U+001E"),
    ):
        if separator in value:
            raise SourceDigestSchemaError(
                f"{field_name} يحوي الفاصل {name}؛ ووجوده داخل الحقل يجعل "
                "محتويين مختلفين يقرآن بصمةً واحدة"
            )
    return value


def source_digest_pairs(
    vocabulary: ImportedFeatureVocabulary,
) -> tuple[tuple[str, str], ...]:
    """أعِد أزواج (الجذر، قيمة نوع الأصل) التي تغطّيها بصمة المصدر وحدها."""

    if type(vocabulary) is not ImportedFeatureVocabulary:
        raise SourceDigestSchemaError("استخراج الأزواج يلزمه مفردةٌ مستورَدة")
    return tuple((entry.root, entry.origin_type.value) for entry in vocabulary.entries)


def source_canonical_bytes(pairs: Iterable[tuple[str, str]]) -> bytes:
    """رمِّز الأزواج بمخطَّط المصدر بدقّة البايت، بلا BOM وبلا تطبيع."""

    materialized: list[tuple[str, str]] = []
    seen: set[str] = set()
    for pair in pairs:
        if not isinstance(pair, tuple) or len(pair) != 2:
            raise SourceDigestSchemaError("كل مُدخَلٍ زوجُ جذرٍ ونوع أصل")
        root = _require_source_text(pair[0], "الجذر")
        origin_type = _require_source_text(pair[1], "نوع الأصل")
        if origin_type not in {member.value for member in ImportedOriginType}:
            raise SourceDigestSchemaError(
                "نوع الأصل must come from the closed vocabulary"
            )
        if root in seen:
            raise SourceDigestSchemaError(
                "تكرّر جذرٌ واحد؛ والتكرار يُخفي مُدخَلًا مختلفًا تحت هوية غيره"
            )
        seen.add(root)
        materialized.append((root, origin_type))
    if not materialized:
        raise SourceDigestSchemaError("المُدخَلات تُرمَّز مجموعةً غير فارغة")
    ordered = sorted(materialized, key=lambda item: item[0])
    lines = [
        f"{root}{SOURCE_FIELD_SEPARATOR}{origin_type}" for root, origin_type in ordered
    ]
    return SOURCE_RECORD_SEPARATOR.join(lines).encode(SOURCE_TEXT_ENCODING)


def source_content_id(pairs: Iterable[tuple[str, str]]) -> str:
    """أعِد بصمة المصدر مُشتقّةً من الأزواج نفسها بالمُهشِّم المشترك."""

    return canonical_digest(source_canonical_bytes(pairs))


@dataclass(frozen=True, slots=True)
class RederivedSourceContentIdentity:
    """بصمةُ مصدرٍ أُعيد اشتقاقها هنا؛ لا تصدر إلا عن دالّة التحقّق."""

    algorithm: str
    canonicalization_version: str
    digest: str
    covered_fields: tuple[str, ...]
    row_count: int
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _SOURCE_DIGEST_TOKEN:
            raise SourceDigestSchemaError(
                "البصمة المُعاد اشتقاقها لا تصدر إلا عن "
                "verify_source_declared_content_id"
            )
        if (
            self.algorithm != CANONICAL_HASH_ALGORITHM
            or self.canonicalization_version != SOURCE_CANONICALIZATION_VERSION
            or not is_canonical_digest(self.digest)
            or self.covered_fields != SOURCE_DIGEST_COVERED_FIELDS
            or self.row_count < 1
        ):
            raise SourceDigestSchemaError("البصمة المُعاد اشتقاقها غير سليمة")


def verify_source_declared_content_id(
    vocabulary: ImportedFeatureVocabulary,
) -> RederivedSourceContentIdentity:
    """أعِد اشتقاق بصمة المصدر من المُدخَلات، وارفض مخالفتها المُعلَنة."""

    if type(vocabulary) is not ImportedFeatureVocabulary:
        raise SourceDigestSchemaError("التحقّق يلزمه مفردةٌ مستورَدة")
    if vocabulary.source_canonicalization_version != SOURCE_CANONICALIZATION_VERSION:
        raise SourceDigestSchemaError(
            "إصدار الترميز القانوني المصدر يخالف المخطَّط المُودَع هنا؛ "
            f"والمُودَع هو {SOURCE_CANONICALIZATION_VERSION} وحده"
        )
    digest = source_content_id(source_digest_pairs(vocabulary))
    if digest != vocabulary.source_declared_content_id:
        raise SourceDigestMismatchError(
            "بصمة المصدر المُعاد اشتقاقها تخالف المُعلَنة: المُعلَنة "
            f"{vocabulary.source_declared_content_id}، والمُشتقّة {digest}، "
            f"عن {vocabulary.row_count} صفًّا. {MISMATCH_CAUSE_NOTE}"
        )
    return RederivedSourceContentIdentity(
        algorithm=CANONICAL_HASH_ALGORITHM,
        canonicalization_version=SOURCE_CANONICALIZATION_VERSION,
        digest=digest,
        covered_fields=SOURCE_DIGEST_COVERED_FIELDS,
        row_count=vocabulary.row_count,
        _token=_SOURCE_DIGEST_TOKEN,
    )


def verify_export_payload(
    payload: Mapping[str, Any],
) -> RederivedSourceContentIdentity:
    """اقرأ حمولة تصديرٍ مصدرية، وطابِقها بالإصدار المُثبَّت، وأعِد اشتقاق بصمتها."""

    vocabulary = vocabulary_from_export_mapping(payload)
    if vocabulary.row_count != EXPECTED_ROW_COUNT:
        raise SourceDigestMismatchError(
            f"عدد المُدخَلات {vocabulary.row_count} ≠ المتوقَّع {EXPECTED_ROW_COUNT}"
        )
    assert_matches_recorded_release(vocabulary)
    return verify_source_declared_content_id(vocabulary)


__all__ = [
    "MISMATCH_CAUSE_NOTE",
    "REDERIVATION_IS_NOT_AUTHORITY_NOTE",
    "SOURCE_DIGEST_SCHEMA_NOTE",
    "SOURCE_FIELD_SEPARATOR",
    "SOURCE_PAYLOAD_ABSENCE_NOTE",
    "SOURCE_RECORD_SEPARATOR",
    "SOURCE_TEXT_ENCODING",
    "RederivedSourceContentIdentity",
    "SourceDigestMismatchError",
    "SourceDigestSchemaError",
    "source_canonical_bytes",
    "source_content_id",
    "source_digest_pairs",
    "verify_export_payload",
    "verify_source_declared_content_id",
]
