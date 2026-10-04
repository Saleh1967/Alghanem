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

import hashlib
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "AN_EVIDENCE_IDENTITY_IS_ITS_CONTENT",
    "A_DECLARED_WORLD_IS_NOT_A_WITNESSED_ONE",
    "A_SOURCE_NAME_IS_NOT_A_CONTENT",
    "A_WRITTEN_GENUS_IS_NOT_A_PROVENANCE",
    "KNOWING_IS_NOT_ONLY_REPORTING",
    "NO_RECORDED_VALUE_IS_NOT_A_RECORDED_ABSENCE",
    "UNKNOWN_IS_A_STATUS_NOT_A_KIND",
    "AcceptanceStanding",
    "Evidence",
    "EvidenceGenus",
    "EvidenceRef",
    "EpistemicError",
    "Scope",
    "SealedLocus",
    "ValueStatus",
    "refuse_unknown_as_a_kind",
    "verify_evidence_locus",
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

A_WRITTEN_GENUS_IS_NOT_A_PROVENANCE: Final[str] = (
    "كتابةُ الجنس ليست منشأً للدليل: من كتب `ACCEPTED_REPORT` بجانب جملةٍ "
    "صاغها بيده فقد سمّى الخبرَ باسمه ولم يَرِد به عن أحد؛ ولذلك لا يُنشَأ "
    "جنسٌ مُثبِتٌ للوقائع إلّا بموضعٍ من ملفٍّ مختومٍ يُعاد قراءتُه فيُقابَل"
)

A_DECLARED_WORLD_IS_NOT_A_WITNESSED_ONE: Final[str] = (
    "العالَمُ المُعلَنُ جملةٌ نصوغها للفحص لا واقعةٌ شاهدناها ولا خبرٌ بلغنا: "
    "`DECLARED_SCENARIO` يَحفظها بصفتها، ولا يُثبِت بها شيءٌ عن الواقع؛ ومن "
    "سمّاها مشاهدةً أثبت بسجلّ الوقائع ما لم يُشاهِده أحد"
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
    DECLARED_SCENARIO = "declared_scenario"
    UNREAD = "unread"

    @property
    def is_fact_establishing(self) -> bool:
        """أيُثبِت هذا الجنسُ قضيّةً عن الواقع؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب.

        التعريفُ الاصطلاحيُّ والفرضيّةُ المُعلَنةُ والعالَمُ المُعلَنُ تُحفَظ
        بصفتها، ولا تُرقَّى حقيقةً مثبتة؛ والشهادةُ المعجميّةُ تُثبِت وضعَ
        اللفظ لا وقوعَ الحدث، فهي مصدرُ رصيدٍ لا مصدرُ واقعة.
        """

        return self in (
            EvidenceGenus.DIRECT_OBSERVATION,
            EvidenceGenus.MEASUREMENT,
            EvidenceGenus.ACCEPTED_REPORT,
            EvidenceGenus.LICENSED_INFERENCE,
        )

    @property
    def demands_a_sealed_locus(self) -> bool:
        """أيلزم هذا الجنسَ موضعٌ من ملفٍّ مختوم؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب.

        اللازمُ موضعًا هو **النقل** وحدَه: `ACCEPTED_REPORT` يدّعي أنّ قائلًا
        قال، فيلزمه موضعٌ يُعاد قراءتُه فيُقابَل
        (`A_WRITTEN_GENUS_IS_NOT_A_PROVENANCE`). وما عداه مُثبِتٌ بحُجّةٍ
        أخرى لا بالسند النصّيّ: `DIRECT_OBSERVATION` و`MEASUREMENT` يدّعيان
        مشاهدةً أو قياسًا، وبرهانُهما إجراءُ الرصد لا ملفٌّ؛
        و`LICENSED_INFERENCE` منشأُه مقدّماتُه، فيُحاسَب عند تركيب الاستدلال.

        وحدُّ هذا الحارس مُعلَنٌ: هو يمنع **ادّعاء نقلٍ بلا سند**، ولا يمنع
        ادّعاءَ مشاهدةٍ لم تقع؛ فذاك يُحاسَب في موضع الرصد لا ههنا.
        """

        return self is EvidenceGenus.ACCEPTED_REPORT

    @property
    def is_substance_founding(self) -> bool:
        """أيصلح هذا الجنسُ مصدرًا لبندٍ في رصيد الأنواع والقواعد؟"""

        return self is not EvidenceGenus.UNREAD


THE_LOCUS_DEMAND_IS_NOT_ENFORCED_AT_CONSTRUCTION_YET: Final[str] = (
    "`demands_a_sealed_locus` خاصّيّةٌ تُقرَأ وتُفحَص بـ`verify_evidence_locus`، "
    "ولم تُجعَل رفضًا في `Evidence.__post_init__` بعدُ: فطبقةُ البرهان "
    "التجريديّة في هذا المستودع تبني أدلّةً بجنس النقل في عوالمَ مضروبةٍ "
    "للمثال (مجلسٌ · أطرافٌ · يدُ الدولة)، ولا موضعَ مختومًا لها ولا يصحّ أن "
    "يُفتعَل. فالرفضُ البنيويُّ مطبَّقٌ حيث يُدَّعى النقلُ عن مصدرٍ عربيٍّ "
    "حقيقيّ — في `source_card_path.CaseFact` — والتعميمُ موقوفٌ على قرارٍ في "
    "نحوِ خمسين موضعًا من طبقة البرهان، يُسمّى ولا يُطوى."
)


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
                "الفترةُ الزمنيّةُ محورٌ وحدّانِ معًا أو لا شيءَ منها؛ ونصفُ فترةٍ نطاقٌ لا يُقرَأ"
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
class SealedLocus:
    """موضعٌ من ملفٍّ مختوم: مسارُه النسبيُّ وختمُه ومداه والمقتطفُ المنقول.

    وهذا هو المنشأُ الذي يَفصِل ما نُقِل عمّا كُتِب
    (`A_WRITTEN_GENUS_IS_NOT_A_PROVENANCE`): المدى حدّانِ مرتّبانِ على نصِّ
    الملفّ المفكوك، و`excerpt` نسخةُ ما بينهما حرفًا بحرف. والمقابلةُ نفسُها
    تقع في `verify_evidence_locus`، فلا يقرأ هذا الصنفُ قرصًا عند بنائه.
    """

    path: str
    digest: str
    start: int
    end: int
    excerpt: str

    def __post_init__(self) -> None:
        _require_text(self.path, "مسارُ الملفّ المختوم")
        _require_text(self.digest, "ختمُ الملفّ المختوم")
        _require_text(self.excerpt, "مقتطفُ الموضع المنقول")
        for bound, label in ((self.start, "بدايةُ المدى"), (self.end, "نهايتُه")):
            if not isinstance(bound, int) or isinstance(bound, bool) or bound < 0:
                raise EpistemicError(f"{label} عددٌ صحيحٌ غيرُ سالب")
        if self.start >= self.end:
            raise EpistemicError("مدى الموضع مرتَّبٌ غيرُ خالٍ: البدايةُ دون النهاية")
        if self.end - self.start != len(self.excerpt):
            raise EpistemicError(
                "طولُ المقتطف هو طولُ المدى؛ ومقتطفٌ أطولُ أو أقصرُ من حدّيه "
                "موضعٌ آخرُ يلبس ثوبَ هذا"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الموضع للبصمة؛ فتبديلُ المقتطف يُبدّل هويّةَ الدليل."""

        return {
            "path": self.path,
            "digest": self.digest,
            "start": self.start,
            "end": self.end,
            "excerpt": self.excerpt,
        }


@dataclass(frozen=True, slots=True)
class Evidence:
    """دليلٌ واحد: جنسُه، ومضمونُه، ومصدرُه المُسمّى، ونطاقُ سريانه، ومنشؤه.

    والمنزلةُ والهويّةُ خاصّيّتانِ مشتقّتانِ لا حقلانِ يُكتَبان. وكلُّ جنسٍ
    يُخبِر عن الواقع بنقلٍ أو مشاهدةٍ أو قياسٍ **لا يُنشَأ بلا `locus`**: هذا
    هو الفصلُ بين ما نُقِل وما كُتِب، ويقع عند الإنشاء لا عند المراجعة.
    """

    evidence_id: str
    genus: EvidenceGenus
    statement: str
    source_name: str
    scope: Scope
    source_digest: str | None = None
    locus: SealedLocus | None = None

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
        if self.locus is not None and not isinstance(self.locus, SealedLocus):
            raise EpistemicError("منشأُ الدليل موضعٌ مختومٌ قائمٌ لا نصٌّ حرّ")
        if (
            self.locus is not None
            and self.source_digest is not None
            and self.source_digest != self.locus.digest
        ):
            raise EpistemicError(
                "ختمُ المصدر المكتوبُ يخالف ختمَ الموضع المنقولِ منه؛ ولا "
                "يُحمَل أحدُهما على الآخر"
            )

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
            "locus": None if self.locus is None else self.locus.as_canonical_content(),
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


def verify_evidence_locus(evidence: Evidence, root: Path) -> SealedLocus:
    """أعِد قراءةَ موضع الدليل من البايتات وقابِله؛ والمخالفةُ رفضٌ لا تنبيه.

    الجذرُ يُمرَّر ولا يُستنبَط، على منوال `witness_occurrence`، فتبقى هذه
    الطبقةُ تسجيلًا لا سلطةَ قرصٍ لها. وتُقابَل ثلاثةُ أشياء بالترتيب: حضورُ
    الملفّ، ثمّ ختمُه، ثمّ المقتطفُ عند مداه. وغيابُ الملفّ رفضٌ كذلك: دليلٌ
    مُثبِتٌ لا يُقرَأ منشؤه لا يُقرَأ مُثبِتًا.
    """

    if not isinstance(evidence, Evidence):
        raise EpistemicError("المقابلةُ تقع على دليلٍ قائم")
    if not isinstance(root, Path):
        raise EpistemicError("جذرُ القراءة مسارٌ قائمٌ لا نصٌّ حرّ")
    locus = evidence.locus
    if locus is None:
        raise EpistemicError(
            f"الدليلُ `{evidence.evidence_id}` بلا موضعٍ يُقابَل؛ و"
            + A_WRITTEN_GENUS_IS_NOT_A_PROVENANCE
        )
    path = root / locus.path
    if not path.is_file():
        raise EpistemicError(
            f"ملفُّ المنشأ `{locus.path}` غائبٌ عن الشجرة، فلا يُقابَل الموضع"
        )
    raw = path.read_bytes()
    measured = hashlib.sha256(raw).hexdigest()
    if measured != locus.digest:
        raise EpistemicError(
            f"ختمُ `{locus.path}` المقيسُ `{measured}` يخالف المكتوبَ "
            f"`{locus.digest}`؛ والبايتاتُ هي الحَكَم"
        )
    text = raw.decode("utf-8")
    if locus.end > len(text):
        raise EpistemicError(
            f"مدى الموضع `[{locus.start}:{locus.end}]` يتجاوز نصَّ "
            f"`{locus.path}` ({len(text)} محرفًا)"
        )
    read = text[locus.start : locus.end]
    if read != locus.excerpt:
        raise EpistemicError(
            f"المقتطفُ المكتوبُ في `{evidence.evidence_id}` يخالف ما يُقرَأ عند "
            f"`[{locus.start}:{locus.end}]` من `{locus.path}`"
        )
    return locus


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


for _declaring_type in (
    Evidence,
    EvidenceRef,
    Scope,
    SealedLocus,
):  # pragma: no cover - guard
    for _field in fields(_declaring_type):
        if _field.type is ValueStatus:  # pragma: no cover - guard
            raise RuntimeError(UNKNOWN_IS_A_STATUS_NOT_A_KIND)
