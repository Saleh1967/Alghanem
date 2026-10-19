"""استيرادُ معنى «فتح» من مقاييس اللغة، وتمييزُ المستوردِ عن المُصطلَحِ عليه.

المعنى المعجميُّ هنا **مستوردٌ** من بايتاتٍ مودَعةٍ مختومة: مادّةُ «فتح» في
مقاييس اللغة، ومحورُها «خلاف الإغلاق». ويُودَع دليلًا جنسُه
`LEXICAL_ATTESTATION`، وهو **غيرُ مُثبِتٍ للوقائع** بتصريح: شهادةُ معجمٍ تقول
ما يدلُّ عليه اللفظُ، ولا تقول إنّ بابًا فُتِح.

**والمحورُ المعجميُّ ليس نوعَ حدثٍ مُعيَّنًا**
(`A_LEXICAL_AXIS_IS_NOT_AN_EVENT_TYPE`): «خلاف الإغلاق» يسع الفتحَ الحسّيَّ
وفتحَ البلاد والحُكْمَ والفتاحةَ — والمادّةُ نفسُها تذكر الحُكْمَ. فتضييقُه إلى
الفتح الحسّيِّ للأبواب **اصطلاحٌ مُعلَنٌ** جنسُه `STIPULATED_DEFINITION`، لا
قراءةٌ من المعجم. وشاهدُ المادّة «يقال: فتحت البابَ» يُقرِّب ولا يُغني.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from ..ontology import Evidence, EvidenceGenus, Scope
from .maqayis_root_table_deposit import root_table_digest, root_table_rows

__all__ = [
    "A_LEXICAL_AXIS_IS_NOT_AN_EVENT_TYPE",
    "AN_ATTESTATION_ESTABLISHES_NO_FACT",
    "THE_PHYSICAL_NARROWING",
    "LexicalSenseError",
    "SenseImport",
    "import_sense_of_root",
    "physical_opening_stipulation",
]


class LexicalSenseError(ValueError):
    """رفضٌ بنيويٌّ في استيراد المعنى؛ لا حملَ على أقرب مادّة."""


A_LEXICAL_AXIS_IS_NOT_AN_EVENT_TYPE: Final[str] = (
    "محورُ المادّة «خلاف الإغلاق» ليس نوعَ حدثٍ مُعيَّنًا: المادّةُ نفسُها "
    "تحمل عليه الحُكْمَ والفتاحةَ؛ فتضييقُه إلى فتحٍ حسّيٍّ لبابٍ اصطلاحٌ "
    "يُعلَن بجنسه، ومن قرأه من المعجم نسب إليه ما لم يقله"
)

AN_ATTESTATION_ESTABLISHES_NO_FACT: Final[str] = (
    "شهادةُ المعجم تُؤسِّس رصيدًا ولا تُودِع واقعة: تقول ما يدلُّ عليه اللفظُ "
    "عند أهله، ولا تقول إنّ بابًا بعينه فُتِح في وقتٍ بعينه"
)

THE_PHYSICAL_NARROWING: Final[str] = (
    "الفتحُ الحسّيُّ المقصودُ في هذا المجال: حدثٌ يُحوِّل حالَ بابٍ من مغلقٍ "
    "إلى مفتوح؛ وهو تضييقٌ مُصطلَحٌ عليه لمحور «خلاف الإغلاق»، مُقرَّبٌ بشاهد "
    "المادّة «يقال: فتحت البابَ وغيرَه فتحاً»"
)


@dataclass(frozen=True, slots=True)
class SenseImport:
    """معنًى مستوردٌ لجذر: محورُه، ومتنُه، وبصمةُ الملفّ، ودليلُه بجنسه."""

    root: str
    entry_number: str
    semantic_axes: tuple[str, ...]
    body_excerpt: str
    table_digest: str
    evidence: Evidence

    def __post_init__(self) -> None:
        if self.evidence.genus is not EvidenceGenus.LEXICAL_ATTESTATION:
            raise LexicalSenseError(
                AN_ATTESTATION_ESTABLISHES_NO_FACT
                + "؛ وجنسُ دليل المعنى المستورد شهادةُ معجمٍ لا غير"
            )
        if self.evidence.establishes_facts:
            raise LexicalSenseError(AN_ATTESTATION_ESTABLISHES_NO_FACT)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الاستيراد للبصمة."""

        return {
            "root": self.root,
            "entry_number": self.entry_number,
            "semantic_axes": list(self.semantic_axes),
            "body_excerpt": self.body_excerpt,
            "table_digest": self.table_digest,
            "evidence": self.evidence.as_canonical_content(),
        }


def import_sense_of_root(root: str, scope: Scope) -> SenseImport:
    """استورد مادّةَ جذرٍ من بايتات المقاييس المودَعة، بدليلٍ غيرِ مُثبِتٍ للوقائع.

    المدخل: جذرٌ ثلاثيٌّ كما يقع في عمود `root_full`، ونطاقُ استعماله.
    الشرط: المادّةُ موجودةٌ مرّةً واحدةً؛ وتعدّدُها أو غيابُها وقفٌ لا اختيار.
    المخرج: استيرادٌ فيه المحورُ والمتنُ وبصمةُ الملفّ ودليلٌ جنسُه شهادةُ معجم.
    حدُّها: لا يُخرِج نوعَ حدثٍ ولا أدوارًا؛ التضييقُ اصطلاحٌ آخرُ مُعلَن.
    """

    if not isinstance(root, str) or not root.strip():
        raise LexicalSenseError("الجذرُ نصٌّ غير فارغ")
    rows = [row for row in root_table_rows() if row["root_full"] == root]
    if not rows:
        raise LexicalSenseError(f"لا مادّةَ للجذر «{root}» في الجدول المودَع")
    if len(rows) > 1:
        raise LexicalSenseError(
            f"للجذر «{root}» {len(rows)} موادَّ في الجدول؛ والاختيارُ بينها "
            "يحتاج ترخيصًا لا يُفتَرض هنا"
        )
    row = rows[0]
    digest = root_table_digest()
    axes = tuple(
        axis.strip() for axis in row["semantic_axes"].split("،") if axis.strip()
    )
    body = row["body_text"]
    evidence = Evidence(
        evidence_id=f"شهادة-معجم-{root}",
        genus=EvidenceGenus.LEXICAL_ATTESTATION,
        statement=(
            f"مادّةُ «{root}» رقم {row['entry_num']} في مقاييس اللغة، "
            f"محورُها: {row['semantic_axes']}؛ وأوّلُ متنها: "
            f"{body.splitlines()[0]}"
        ),
        source_name="maqayis_by_root_csv_999.csv",
        scope=scope,
        source_digest=digest,
    )
    return SenseImport(
        root=root,
        entry_number=row["entry_num"],
        semantic_axes=axes,
        body_excerpt=body[:400],
        table_digest=digest,
        evidence=evidence,
    )


def physical_opening_stipulation(scope: Scope) -> Evidence:
    """أعلِن تضييقَ المحور إلى الفتح الحسّيّ **اصطلاحًا**، لا قراءةً من المعجم.

    المدخل: نطاقُ الاصطلاح.
    الشرط: لا شيء؛ الاصطلاحُ يُعلَن بجنسه ويُقرَأ به.
    المخرج: دليلٌ جنسُه `STIPULATED_DEFINITION`، يؤسِّس رصيدًا ولا يُودِع واقعة.
    حدُّها: لا يُرقَّى إلى حقيقةٍ مُثبَتةٍ لأنّه مُودَعٌ في الرصيد.
    """

    return Evidence(
        evidence_id="اصطلاح-الفتح-الحسّيّ",
        genus=EvidenceGenus.STIPULATED_DEFINITION,
        statement=THE_PHYSICAL_NARROWING + "؛ و" + A_LEXICAL_AXIS_IS_NOT_AN_EVENT_TYPE,
        source_name="هذا المجالُ المُعلَن",
        scope=scope,
        source_digest=None,
    )
