"""`G0.METRIC-0`: عقدةُ القدرة، بلا حقلِ حالةٍ يكتبه صاحبُها.

ليس في `CapabilityNode` حقلٌ اسمُه «مُنجَز» ولا «نسبة» ولا «درجة»: الحالةُ
تُشتَقّ من الشواهد في `measure.py`، فالادّعاءُ اليدويّ هنا **غيرُ قابلٍ للقول**
لا مرفوضٌ بعد وقوعه — وهو انضباطُ `arabic/epistemic_layers.py` نفسُه.

وكلُّ عقدةٍ تحمل استشهادَها: مصدرًا مُعلَنًا وموضعًا فيه
(`TheDenominatorIsCitedNotInvented`). والمصدرُ لا يُقرأ تصديقًا لعقدةٍ ولا
تكفيرًا لأخرى، وإنّما يُثبِت أنّ البابَ مُصطلَحٌ عليه في فنّه لا مُخترَعٌ هنا.

و`G0.METRIC-0.HARDEN` يفصل تسميةَ المصدر عن توثيق الموضع
(`CitationName != VerifiedSourceLocus`): لكلّ استشهادٍ **مرتبةٌ** مُصرَّحٌ بها،
ومرساةُ نصِّ المصدر غيرُ بصمةِ صياغتنا نحن
(`OurConceptualMapping != SourceTextAnchor`). والمصطلحُ الحديثُ لا يحمل صفحةً
ولا بابًا يُوهم أنّه منقولٌ من الكتاب القديم، والبابُ يبقى في المقام بمرتبةٍ
نازلةٍ ولا يُنسَب زورًا (`KeepingAQuestionDoesNotLicenseAFalseCitation`).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .maturity import MaturityStage

__all__ = [
    "CITATION_STANDING_SEQUENCE",
    "DECLARED_EDITIONS",
    "DECLARED_SOURCES",
    "CapabilityCitation",
    "CapabilityNode",
    "CapabilityNodeError",
    "CitationStanding",
    "DeclaredEdition",
    "DeclaredSource",
    "NodeKind",
    "ReadinessGateOrigin",
    "Requirement",
]


class CapabilityNodeError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في بناء العقدة؛ لا حملَ على أقرب حالة."""


class NodeKind(Enum):
    """جنسُ العقدة في الشجرة الفركتاليّة؛ مفردةٌ مغلقة."""

    TOTAL = "TOTAL"
    DOMAIN = "DOMAIN"
    CAPABILITY = "CAPABILITY"
    SUBCAPABILITY = "SUBCAPABILITY"


class Requirement(Enum):
    """علاقةُ الابن بأبيه: هل يسقف الأبَ أم يُسهِم في تغطيته فقط؟"""

    REQUIRED = "REQUIRED"
    CONTRIBUTING = "CONTRIBUTING"


@dataclass(frozen=True)
class DeclaredSource:
    """مصدرٌ مُعلَنٌ يُستشهَد به على وجود الباب في فنّه، لا على صحّة قولٍ فيه."""

    source_id: str
    title: str
    discipline: str

    def __post_init__(self) -> None:
        for name in ("source_id", "title", "discipline"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise CapabilityNodeError(
                    f"a declared source requires a non-empty «{name}»"
                )

    def as_canonical_content(self) -> dict[str, str]:
        """المحتوى القانونيّ للمصدر؛ لا بايتاتِ مصدرٍ ولا نقلَ نصّ."""

        return {
            "source_id": self.source_id,
            "title": self.title,
            "discipline": self.discipline,
        }


DECLARED_SOURCES: Final[tuple[DeclaredSource, ...]] = (
    DeclaredSource(
        source_id="sirr_sinaat_al_irab",
        title="سرُّ صناعة الإعراب — ابن جنّي",
        discipline="الأصوات والحروف",
    ),
    DeclaredSource(
        source_id="shafiya_ibn_al_hajib",
        title="الشافية في التصريف — ابن الحاجب",
        discipline="الصرف",
    ),
    DeclaredSource(
        source_id="sharh_ibn_aqil",
        title="شرح ابن عقيل على ألفيّة ابن مالك",
        discipline="النحو",
    ),
    DeclaredSource(
        source_id="mughni_al_labib",
        title="مغني اللبيب عن كتب الأعاريب — ابن هشام",
        discipline="الحروف والأدوات والإعراب",
    ),
    DeclaredSource(
        source_id="al_mustasfa",
        title="المستصفى من علم الأصول — الغزالي",
        discipline="أصول الفقه والدلالة",
    ),
    DeclaredSource(
        source_id="sharh_al_tahdhib",
        title="شرح تهذيب المنطق — التفتازاني وحواشيه",
        discipline="المنطق والدلالة الوضعيّة",
    ),
    DeclaredSource(
        source_id="miftah_al_ulum",
        title="مفتاح العلوم — السكّاكي",
        discipline="المعاني والبيان والخطاب",
    ),
)
"""المصادرُ المُعلَنةُ التي يُستشهَد بها على أبواب المقام؛ لا رابعَ لها يُضاف صمتًا."""

_SOURCE_IDS: Final[frozenset[str]] = frozenset(
    source.source_id for source in DECLARED_SOURCES
)


@dataclass(frozen=True)
class DeclaredEdition:
    """طبعةٌ بعينها من مصدرٍ مُعلَن؛ الكتابُ ليس الطبعة، والموضعُ يتبع الطبعة."""

    edition_id: str
    source_id: str
    description: str

    def __post_init__(self) -> None:
        for name in ("edition_id", "description"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise CapabilityNodeError(
                    f"a declared edition requires a non-empty «{name}»"
                )
        if type(self.source_id) is not str or self.source_id not in _SOURCE_IDS:
            raise CapabilityNodeError(
                "a declared edition belongs to one of the declared sources"
            )

    def as_canonical_content(self) -> dict[str, str]:
        """المحتوى القانونيّ للطبعة؛ لا نقلَ نصٍّ ولا بايتاتِ مصدر."""

        return {
            "edition_id": self.edition_id,
            "source_id": self.source_id,
            "description": self.description,
        }


DECLARED_EDITIONS: Final[tuple[DeclaredEdition, ...]] = ()
"""سِجِلُّ الطبعات المُحقَّقة؛ فارغٌ في V1 لأنّنا لم نتحقّق من طبعةٍ بعينها بعد."""

_EDITION_IDS: Final[frozenset[str]] = frozenset(
    edition.edition_id for edition in DECLARED_EDITIONS
)


class CitationStanding(Enum):
    """مرتبةُ الاستشهاد: ما تحقّق منه فعلًا، لا ما نودّ أن يكون."""

    EXACT_TEXTUAL_LOCUS = "EXACT_TEXTUAL_LOCUS"
    SECTION_LEVEL_LOCUS = "SECTION_LEVEL_LOCUS"
    CONCEPTUAL_CORRESPONDENCE = "CONCEPTUAL_CORRESPONDENCE"
    MODERN_FORMAL_EXTENSION = "MODERN_FORMAL_EXTENSION"
    UNVERIFIED_LOCUS = "UNVERIFIED_LOCUS"


CITATION_STANDING_SEQUENCE: Final[tuple[CitationStanding, ...]] = (
    CitationStanding.EXACT_TEXTUAL_LOCUS,
    CitationStanding.SECTION_LEVEL_LOCUS,
    CitationStanding.CONCEPTUAL_CORRESPONDENCE,
    CitationStanding.MODERN_FORMAL_EXTENSION,
    CitationStanding.UNVERIFIED_LOCUS,
)
"""ترتيبُ عرضِ المراتب؛ ترتيبُ توثيقٍ لا ترتيبُ صحّةٍ علميّة ولا درجةُ نضج."""


class ReadinessGateOrigin(Enum):
    """أصلُ بوّابة الأهليّة: تصريحٌ موحَّدٌ أوّليّ، أم اشتقاقٌ من دور القدرة؟"""

    DECLARED_UNIFORM_V1 = "DECLARED_UNIFORM_V1"
    DERIVED_FROM_CAPABILITY_ROLE = "DERIVED_FROM_CAPABILITY_ROLE"


@dataclass(frozen=True)
class CapabilityCitation:
    """استشهادُ العقدة: مصدرٌ مُعلَن، ومرتبةٌ مُصرَّحٌ بها، وموضعٌ بقدر ما تحقّق.

    الحقولُ المجهولةُ تبقى `None` ولا تُملأ بقيمٍ وهميّة: موضعٌ مُختلَقٌ أسوأُ
    من موضعٍ غائب، لأنّه يُقرأ توثيقًا.
    """

    source_id: str
    citation_standing: CitationStanding
    locus: str | None = None
    edition_id: str | None = None
    volume: str | None = None
    page_range: str | None = None
    chapter_bab: str | None = None
    source_text_anchor_digest: str | None = None
    conceptual_mapping_digest: str | None = None

    def __post_init__(self) -> None:
        if type(self.source_id) is not str or self.source_id not in _SOURCE_IDS:
            raise CapabilityNodeError(
                "a citation names one of the declared sources and no other"
            )
        if not isinstance(self.citation_standing, CitationStanding):
            raise CapabilityNodeError(
                "a citation declares its standing: naming a source is not "
                "verifying a locus"
            )
        self._assert_optional_text()
        self._assert_digests()
        self._assert_edition()
        self._assert_standing_requirements()

    def _assert_optional_text(self) -> None:
        for name in (
            "locus",
            "volume",
            "page_range",
            "chapter_bab",
        ):
            value = getattr(self, name)
            if value is None:
                continue
            if type(value) is not str or not value.strip():
                raise CapabilityNodeError(
                    f"«{name}» is either absent or a non-empty string; an empty "
                    "locator is not a locator"
                )

    def _assert_digests(self) -> None:
        for name in ("source_text_anchor_digest", "conceptual_mapping_digest"):
            value = getattr(self, name)
            if value is None:
                continue
            if not is_canonical_digest(value):
                raise CapabilityNodeError(f"«{name}» requires a canonical digest")
        if (
            self.source_text_anchor_digest is not None
            and self.source_text_anchor_digest == self.conceptual_mapping_digest
        ):
            raise CapabilityNodeError(
                "our conceptual mapping is not a source text anchor: one digest "
                "cannot stand as both"
            )

    def _assert_edition(self) -> None:
        if self.edition_id is None:
            return
        if type(self.edition_id) is not str or self.edition_id not in _EDITION_IDS:
            raise CapabilityNodeError(
                "a citation names a verified edition from the edition registry, "
                "never an invented edition identifier"
            )
        if _edition_source(self.edition_id) != self.source_id:
            raise CapabilityNodeError(
                "a citation's edition belongs to the cited source itself"
            )

    def _assert_standing_requirements(self) -> None:
        standing = self.citation_standing
        if standing is CitationStanding.EXACT_TEXTUAL_LOCUS:
            if self.edition_id is None:
                raise CapabilityNodeError(
                    "an exact textual locus requires a verified edition"
                )
            if self.volume is None and self.page_range is None:
                raise CapabilityNodeError(
                    "an exact textual locus requires a volume or a page range"
                )
            if self.chapter_bab is None:
                raise CapabilityNodeError(
                    "an exact textual locus requires the chapter or bab it sits in"
                )
            if self.source_text_anchor_digest is None:
                raise CapabilityNodeError(
                    "an exact textual locus requires a source text anchor digest"
                )
            return
        if standing is CitationStanding.SECTION_LEVEL_LOCUS:
            if self.chapter_bab is None:
                raise CapabilityNodeError(
                    "a section level locus requires a real chapter or bab"
                )
            if self.page_range is not None and self.edition_id is None:
                raise CapabilityNodeError(
                    "a page range depends on an edition: name the edition or drop "
                    "the page"
                )
            return
        if standing is CitationStanding.CONCEPTUAL_CORRESPONDENCE:
            if self.conceptual_mapping_digest is None and self.locus is None:
                raise CapabilityNodeError(
                    "a conceptual correspondence states the mapping it claims"
                )
            if self.source_text_anchor_digest is not None:
                raise CapabilityNodeError(
                    "a conceptual correspondence carries no source text anchor; "
                    "an anchored locus is not a correspondence"
                )
            return
        if standing is CitationStanding.MODERN_FORMAL_EXTENSION:
            if (
                self.page_range is not None
                or self.chapter_bab is not None
                or self.volume is not None
                or self.source_text_anchor_digest is not None
            ):
                raise CapabilityNodeError(
                    "a modern formal extension carries no page, volume, bab or "
                    "source anchor: the modern formulation is not in the old text"
                )
            return
        if self.source_text_anchor_digest is not None:
            raise CapabilityNodeError(
                "an unverified locus cannot carry a source text anchor"
            )

    @property
    def is_textually_anchored(self) -> bool:
        """هل هذا الاستشهادُ مرسًى في نصّ طبعةٍ مُحقَّقة؟"""

        return self.citation_standing is CitationStanding.EXACT_TEXTUAL_LOCUS

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للاستشهاد، بمرتبته وبما تحقّق من موضعه."""

        return {
            "source_id": self.source_id,
            "citation_standing": self.citation_standing.value,
            "locus": self.locus,
            "edition_id": self.edition_id,
            "volume": self.volume,
            "page_range": self.page_range,
            "chapter_bab": self.chapter_bab,
            "source_text_anchor_digest": self.source_text_anchor_digest,
            "conceptual_mapping_digest": self.conceptual_mapping_digest,
        }


def _edition_source(edition_id: str) -> str | None:
    for edition in DECLARED_EDITIONS:
        if edition.edition_id == edition_id:
            return edition.source_id
    return None


@dataclass(frozen=True)
class CapabilityNode:
    """عقدةٌ في المقام المُعلَن؛ بلا حقلِ حالةٍ ولا نسبةٍ ولا درجةٍ مكتوبة."""

    node_id: str
    title: str
    kind: NodeKind
    parent_id: str | None
    requirement: Requirement
    citation: CapabilityCitation
    readiness_gate: MaturityStage
    readiness_gate_origin: ReadinessGateOrigin

    def __post_init__(self) -> None:
        if type(self.node_id) is not str or not self.node_id.strip():
            raise CapabilityNodeError("a capability node requires a node_id")
        if type(self.title) is not str or not self.title.strip():
            raise CapabilityNodeError(f"«{self.node_id}» requires a title")
        if not isinstance(self.kind, NodeKind):
            raise CapabilityNodeError(f"«{self.node_id}» requires a NodeKind")
        if not isinstance(self.requirement, Requirement):
            raise CapabilityNodeError(f"«{self.node_id}» requires a Requirement")
        if not isinstance(self.citation, CapabilityCitation):
            raise CapabilityNodeError(
                f"«{self.node_id}» requires a citation: a denominator node is "
                "cited, never invented"
            )
        if not isinstance(self.readiness_gate, MaturityStage):
            raise CapabilityNodeError(
                f"«{self.node_id}» requires a declared readiness gate"
            )
        if not self.readiness_gate.is_an_attestable_gate:
            raise CapabilityNodeError(
                f"«{self.node_id}» cannot declare absence as its readiness gate"
            )
        if not isinstance(self.readiness_gate_origin, ReadinessGateOrigin):
            raise CapabilityNodeError(
                f"«{self.node_id}» declares where its readiness gate came from: a "
                "uniform declaration is not a derived requirement"
            )
        if self.kind is NodeKind.TOTAL:
            if self.parent_id is not None:
                raise CapabilityNodeError("the total node has no parent")
        else:
            if type(self.parent_id) is not str or not self.parent_id.strip():
                raise CapabilityNodeError(f"«{self.node_id}» requires a parent_id")
            if self.parent_id == self.node_id:
                raise CapabilityNodeError(f"«{self.node_id}» cannot be its own parent")

    @property
    def is_root(self) -> bool:
        """هل هي عقدةُ العربيةِ الجامعة؟"""

        return self.kind is NodeKind.TOTAL

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للعقدة، بلا حالةٍ ولا شاهدٍ ولا رقم."""

        return {
            "node_id": self.node_id,
            "title": self.title,
            "kind": self.kind.value,
            "parent_id": self.parent_id,
            "requirement": self.requirement.value,
            "citation": self.citation.as_canonical_content(),
            "readiness_gate": self.readiness_gate.value,
            "readiness_gate_origin": self.readiness_gate_origin.value,
        }

    @property
    def node_digest(self) -> str:
        """مُلخَّصُ محتوى العقدة؛ يتغيّر بتغيّر إعلانها لا بتغيّر شواهدها."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
