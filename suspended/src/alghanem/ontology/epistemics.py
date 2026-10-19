"""حالُ المعرفة مفصولًا عن مضمونها: المصدرُ والمنزلةُ والنطاق، وحالُ القيمة.

هذه الوحدةُ **لا تقول ما الموجود**؛ تقول: ما مصدرُ هذه المعلومة، وبأيّ منزلةٍ
قُبِلت، وفي أيّ نطاقٍ تسري، وهل قيمةُ الخاصّيّة معلومةٌ أم مجهولةٌ أم متنازعٌ
عليها أم غيرُ منطبقة. والفصلُ هو المقصود:

    ما الخاصّيّة            ← `substance`
    ما حالُ قيمتها          ← `ValueStatus` ههنا
    أمُثبَتةٌ أم منفيّة      ← `Polarity` في `content` و`facts`

**ولا طرقَ معرفةٍ محصورةٌ في الرواية** (`KNOWING_IS_NOT_ONLY_REPORTING`): جنسُ
الدليل مفردةٌ فيها المشاهدةُ والقياسُ والخبرُ المعتمدُ والاستنتاجُ المُرخَّص،
وفيها كذلك **التعريفُ الاصطلاحيُّ والفرضيّةُ المُعلَنة** — تُحفَظان بصفتهما
المُعلَنة ولا تُرقَّيان حقيقةً مثبتة (`is_fact_establishing` تُشتَقّ ولا تُكتَب).

**و«مجهول» ليس جنسًا أنطولوجيًّا** (`UNKNOWN_IS_A_STATUS_NOT_A_KIND`):
`ValueStatus` يصف **إسنادَ قيمةٍ** لا يصف موجودًا؛ ولذلك يُرفَض بنيويًّا أن
يُجعَل قيمةً لحقلٍ اسمُه نوعٌ أو جنسٌ، ويُفحَص ذلك عند الاستيراد.

**وغيابُ قيمةٍ مسجَّلةٍ ليس إثباتًا لانتفاء الخاصّيّة**
(`NO_RECORDED_VALUE_IS_NOT_A_RECORDED_ABSENCE`): `UNKNOWN` و`NOT_APPLICABLE`
عضوانِ متمايزان، والأوّلُ لا يُقرَأ نفيًا بحالٍ.

**وهويّةُ الدليل مشتقّةٌ من مضمونه** (`AN_EVIDENCE_IDENTITY_IS_ITS_CONTENT`):
`Evidence.content_id` بصمةُ ما يقوله الدليلُ ونطاقِه ومصدرِه، لا اسمٌ يُكتَب
بجانبه؛ فتغييرُ المضمون يُغيِّر الهويّة حتمًا، وبه يُكشَف الحكمُ المعتمِدُ عليه.
واسمُ المصدر أو بصمتُه وحدَهما لا يُغنيان عن المضمون: `statement` حقلٌ مُلزَم.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا تستورد هذه
الوحدةُ من `metaalgebra/` ولا `linguistic/` ولا `arabic/` ولا `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "AN_EVIDENCE_IDENTITY_IS_ITS_CONTENT",
    "A_SOURCE_NAME_IS_NOT_A_CONTENT",
    "KNOWING_IS_NOT_ONLY_REPORTING",
    "NO_RECORDED_VALUE_IS_NOT_A_RECORDED_ABSENCE",
    "UNKNOWN_IS_A_STATUS_NOT_A_KIND",
    "AcceptanceStanding",
    "Evidence",
    "EvidenceGenus",
    "EvidenceRef",
    "EpistemicError",
    "Scope",
    "ValueStatus",
    "refuse_unknown_as_a_kind",
]


class EpistemicError(ValueError):
    """رفضٌ بنيويٌّ في طبقة حال المعرفة؛ لا حملَ على أقرب حالةٍ مقبولة."""


KNOWING_IS_NOT_ONLY_REPORTING: Final[str] = (
    "طرقُ المعرفة ليست الروايةَ وحدَها: المشاهدةُ والقياسُ والخبرُ المعتمدُ "
    "والاستنتاجُ المُرخَّصُ أجناسٌ مُسمّاةٌ كلُّها، ومن حصرها في الخبر ردّ ما "
    "لا يُروى وقَبِل ما لا يُشاهَد بغير تمييز"
)

UNKNOWN_IS_A_STATUS_NOT_A_KIND: Final[str] = (
    "«مجهول» حالُ إسنادِ قيمةٍ لا جنسٌ من أجناس الموجودات: من جعله نوعًا أنشأ "
    "في الرصيد موجودًا لا وجودَ له، ثمّ استدلّ على العالَم بجهله"
)

NO_RECORDED_VALUE_IS_NOT_A_RECORDED_ABSENCE: Final[str] = (
    "غيابُ قيمةٍ مسجَّلةٍ ليس تسجيلًا لانتفاء الخاصّيّة: `UNKNOWN` سكوتٌ عن "
    "القيمة، و`NOT_APPLICABLE` إخبارٌ بأنّ الخاصّيّة لا تُحمَل على هذا الحامل "
    "أصلًا؛ وجمعُهما يُخرِج نفيًا لم يقله أحد"
)

AN_EVIDENCE_IDENTITY_IS_ITS_CONTENT: Final[str] = (
    "هويّةُ الدليل مضمونُه: `content_id` بصمةُ ما يقوله الدليلُ ونطاقِه "
    "ومصدرِه، فتغييرُ المضمون يُغيِّر الهويّة؛ ودليلٌ يُعدَّل مضمونُه ويبقى "
    "مُعرِّفُه دليلٌ آخرُ يلبس ثوبَ الأوّل"
)

A_SOURCE_NAME_IS_NOT_A_CONTENT: Final[str] = (
    "اسمُ المصدر أو بصمتُه لا يُغنيان عن مضمون المعلومة: من كتب «من كتاب كذا» "
    "ولم يكتب ما الذي قاله الكتابُ ولا دليلَ انطباقه على هذا الموضع أودع "
    "إحالةً لا معلومة"
)


class EvidenceGenus(Enum):
    """أجناسُ الأدلّة؛ مفردةٌ مغلقةٌ فيها عضوُ جهلٍ مُصرَّحٌ به."""

    DIRECT_OBSERVATION = "direct_observation"
    MEASUREMENT = "measurement"
    ACCEPTED_REPORT = "accepted_report"
    LICENSED_INFERENCE = "licensed_inference"
    LEXICAL_ATTESTATION = "lexical_attestation"
    STIPULATED_DEFINITION = "stipulated_definition"
    DECLARED_HYPOTHESIS = "declared_hypothesis"
    UNREAD = "unread"

    @property
    def is_fact_establishing(self) -> bool:
        """أيُثبِت هذا الجنسُ قضيّةً عن الواقع؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب.

        التعريفُ الاصطلاحيُّ والفرضيّةُ المُعلَنةُ يُحفَظان بصفتهما، ولا
        يُرقَّيان حقيقةً مثبتة؛ والشهادةُ المعجميّةُ تُثبِت وضعَ اللفظ لا وقوعَ
        الحدث، فهي مصدرُ رصيدٍ لا مصدرُ واقعة.
        """

        return self in (
            EvidenceGenus.DIRECT_OBSERVATION,
            EvidenceGenus.MEASUREMENT,
            EvidenceGenus.ACCEPTED_REPORT,
            EvidenceGenus.LICENSED_INFERENCE,
        )

    @property
    def is_substance_founding(self) -> bool:
        """أيصلح هذا الجنسُ مصدرًا لبندٍ في رصيد الأنواع والقواعد؟"""

        return self is not EvidenceGenus.UNREAD


class AcceptanceStanding(Enum):
    """منزلةُ القبول؛ تُشتَقّ من جنس الدليل ولا تُكتَب بجانبه."""

    ESTABLISHED = "established"
    ACCEPTED_PRESUMPTION = "accepted_presumption"
    DECLARED_ONLY = "declared_only"
    UNREAD = "unread"

    @classmethod
    def of(cls, genus: EvidenceGenus) -> AcceptanceStanding:
        """منزلةُ جنسٍ بعينه؛ وجنسٌ خارج المفردة رفضٌ لا حملٌ على أقرب منزلة."""

        if not isinstance(genus, EvidenceGenus):
            raise EpistemicError("جنسُ الدليل عضوٌ في مفردته المغلقة لا نصٌّ حرّ")
        if genus in (EvidenceGenus.DIRECT_OBSERVATION, EvidenceGenus.MEASUREMENT):
            return cls.ESTABLISHED
        if genus in (EvidenceGenus.ACCEPTED_REPORT, EvidenceGenus.LICENSED_INFERENCE):
            return cls.ACCEPTED_PRESUMPTION
        if genus is EvidenceGenus.UNREAD:
            return cls.UNREAD
        return cls.DECLARED_ONLY


class ValueStatus(Enum):
    """حالُ إسنادِ قيمةٍ لخاصّيّةٍ أو علاقة؛ **وليست جنسًا من أجناس الموجودات**."""

    KNOWN = "known"
    UNKNOWN = "unknown"
    DISPUTED = "disputed"
    NOT_APPLICABLE = "not_applicable"

    @property
    def carries_a_value(self) -> bool:
        """أتحمل هذه الحالُ قيمةً مقروءة؟ `KNOWN` وحدَها."""

        return self is ValueStatus.KNOWN

    @property
    def is_a_recorded_absence(self) -> bool:
        """أهذه الحالُ تسجيلٌ لانتفاء الخاصّيّة؟ `NOT_APPLICABLE` وحدَها."""

        return self is ValueStatus.NOT_APPLICABLE


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EpistemicError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class Scope:
    """نطاقُ سريانِ معلومةٍ: مجالُها، وفترتُها الزمنيّةُ إن كانت مؤقّتة.

    والفترةُ عددانِ مرتّبانِ على محورٍ مُسمًّى، أو `None` تصريحًا بأنّ المعلومة
    **غيرُ مؤقّتة** (كتعريف نوع). وغيابُ الفترة ليس سريانًا على كلّ زمنٍ
    بالسهو: `covers` ترفض مقارنةَ غير المؤقّت بالمؤقّت وتُخرِج `False`.
    """

    domain_id: str
    timeline_id: str | None = None
    start: int | None = None
    end: int | None = None

    def __post_init__(self) -> None:
        _require_text(self.domain_id, "مجالُ النطاق")
        bounds = (self.start, self.end)
        if (self.timeline_id is None) != all(bound is None for bound in bounds):
            raise EpistemicError(
                "الفترةُ الزمنيّةُ محورٌ وحدّانِ معًا أو لا شيءَ منها؛ ونصفُ "
                "فترةٍ نطاقٌ لا يُقرَأ"
            )
        if self.start is not None and self.end is not None and self.start > self.end:
            raise EpistemicError("حدّا الفترة مرتّبان: البدايةُ لا تتجاوز النهاية")

    @property
    def is_timeless(self) -> bool:
        """أهذا نطاقٌ غيرُ مؤقّت؟ خاصّيّةٌ تُشتَقّ من حضور المحور."""

        return self.timeline_id is None

    def covers(self, other: Scope) -> bool:
        """أيشمل هذا النطاقُ ذاك؟ ومجالانِ مختلفانِ لا يشمل أحدُهما الآخر."""

        if not isinstance(other, Scope):
            raise EpistemicError("الشمولُ يُقاس بين نطاقين قائمين")
        if self.domain_id != other.domain_id:
            return False
        if self.is_timeless:
            return other.is_timeless
        if other.is_timeless:
            return False
        if self.timeline_id != other.timeline_id:
            return False
        assert self.start is not None and self.end is not None
        assert other.start is not None and other.end is not None
        return self.start <= other.start and other.end <= self.end

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النطاق للبصمة."""

        return {
            "domain_id": self.domain_id,
            "timeline_id": self.timeline_id,
            "start": self.start,
            "end": self.end,
        }


@dataclass(frozen=True, slots=True)
class Evidence:
    """دليلٌ واحد: جنسُه، ومضمونُه، ومصدرُه المُسمّى، ونطاقُ سريانه.

    والمنزلةُ والهويّةُ خاصّيّتانِ مشتقّتانِ لا حقلانِ يُكتَبان.
    """

    evidence_id: str
    genus: EvidenceGenus
    statement: str
    source_name: str
    scope: Scope
    source_digest: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.evidence_id, "مُعرِّفُ الدليل")
        if not isinstance(self.genus, EvidenceGenus):
            raise EpistemicError(
                "جنسُ الدليل عضوٌ في مفردته المغلقة؛ و" + KNOWING_IS_NOT_ONLY_REPORTING
            )
        _require_text(
            self.statement, "مضمونُ الدليل؛ و" + A_SOURCE_NAME_IS_NOT_A_CONTENT
        )
        _require_text(self.source_name, "اسمُ مصدر الدليل")
        if not isinstance(self.scope, Scope):
            raise EpistemicError("نطاقُ الدليل نطاقٌ قائمٌ لا نصٌّ حرّ")
        if self.source_digest is not None:
            _require_text(self.source_digest, "بصمةُ مصدر الدليل إن ذُكرت")

    @property
    def standing(self) -> AcceptanceStanding:
        """منزلةُ القبول؛ مشتقّةٌ من الجنس على منهج «الحالُ تُشتَقّ من حواملها»."""

        return AcceptanceStanding.of(self.genus)

    @property
    def establishes_facts(self) -> bool:
        """أيُثبِت هذا الدليلُ قضيّةً عن الواقع؟"""

        return self.genus.is_fact_establishing

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الدليل للبصمة؛ والمُعرِّفُ خارجَه عمدًا."""

        return {
            "genus": self.genus.value,
            "statement": self.statement,
            "source_name": self.source_name,
            "source_digest": self.source_digest,
            "scope": self.scope.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ مضمون الدليل؛ على معنى `AN_EVIDENCE_IDENTITY_IS_ITS_CONTENT`."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    @property
    def ref(self) -> EvidenceRef:
        """إشارةٌ مبصومةٌ إلى هذا الدليل؛ تُشتَقّ ولا تُكتَب بجانبه."""

        return EvidenceRef(evidence_id=self.evidence_id, content_id=self.content_id)


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    """إشارةٌ إلى دليلٍ بمُعرِّفه **وبصمة مضمونه** معًا؛ فالاسمُ وحدَه لا يكفي."""

    evidence_id: str
    content_id: str

    def __post_init__(self) -> None:
        _require_text(self.evidence_id, "مُعرِّفُ الدليل المُشارِ إليه")
        _require_text(self.content_id, "بصمةُ مضمون الدليل المُشارِ إليه")

    @classmethod
    def of(cls, evidence: Evidence) -> EvidenceRef:
        """اشتقّ الإشارةَ من الدليل نفسِه؛ ولا تُكتَب البصمةُ بجانبه يدويًّا."""

        if not isinstance(evidence, Evidence):
            raise EpistemicError("الإشارةُ تُشتَقّ من دليلٍ قائمٍ لا من اسمٍ حرّ")
        return evidence.ref

    def matches(self, evidence: Evidence) -> bool:
        """أتطابق هذه الإشارةُ الدليلَ المُعطى مُعرِّفًا وبصمةً معًا؟"""

        if not isinstance(evidence, Evidence):
            raise EpistemicError("المطابقةُ تُقاس على دليلٍ قائم")
        return (
            self.evidence_id == evidence.evidence_id
            and self.content_id == evidence.content_id
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {"evidence_id": self.evidence_id, "content_id": self.content_id}


_KIND_FIELD_MARKERS: Final[tuple[str, ...]] = ("kind", "genus", "type_id", "sort")
"""أسماءٌ تدلّ على جنسٍ أنطولوجيّ؛ ولا يُسنَد إليها `ValueStatus` بحال."""


def refuse_unknown_as_a_kind(field_name: str, value: object) -> None:
    """ارفض أن تُجعَل حالُ القيمةِ جنسًا؛ `UNKNOWN_IS_A_STATUS_NOT_A_KIND`."""

    if not isinstance(value, ValueStatus):
        return
    lowered = field_name.lower()
    for marker in _KIND_FIELD_MARKERS:
        if marker in lowered:
            raise EpistemicError(UNKNOWN_IS_A_STATUS_NOT_A_KIND)


for _declaring_type in (Evidence, EvidenceRef, Scope):  # pragma: no cover - guard
    for _field in fields(_declaring_type):
        if _field.type is ValueStatus:  # pragma: no cover - guard
            raise RuntimeError(UNKNOWN_IS_A_STATUS_NOT_A_KIND)
