"""بيانُ التوليد: بصمتان لا واحدة، وإلّا صار ادّعاءُ الاشتقاق غيرَ قابلٍ للتكذيب.

    (digest Σ_A, digest g, backend_id)  ⟼  bytes

**والحتميّةُ نسبيّةٌ إلى المولِّد كما هي نسبيّةٌ إلى المواصفة:** لو بُنيت على
`Σ_A` وحدها لأمكن تبديلُ المولِّد وإخراجُ بايتاتٍ أخرى مع ثبات المواصفة، ثمّ
ادّعاءُ أنّ «`Σ` ولّدت هذا الكود». فالبيانُ يحمل `sigma_digest` و
`generator_digest` و`backend_id` و`schema_digest`، ويُقارَن بهذه الأربعة.

**والبيانُ لا يحمل حكمًا:** مطابقةُ بايتاتٍ إثباتُ اشتقاقٍ لا إثباتُ صدقِ
النظريّة؛ وكودٌ مولَّدٌ من مواصفةٍ خاطئةٍ كودٌ خاطئٌ مُشتَقٌّ بأمانة.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from ..metaalgebra.specification import AbstractSystemSpecification
from .artifact import GeneratedArtifactSet

__all__ = [
    "DETERMINISM_LAW",
    "A_MANIFEST_IS_NOT_A_PROOF_OF_TRUTH",
    "GeneratedArtifactManifest",
    "GeneratedArtifactManifestError",
]

DETERMINISM_LAW: Final = (
    "تساوي (بصمةِ Σ_A، بصمةِ المولِّد) يوجب تساوي البايتات؛ "
    "والحتميّةُ نسبيّةٌ إلى الاثنين لا إلى المواصفة وحدها"
)

A_MANIFEST_IS_NOT_A_PROOF_OF_TRUTH: Final = (
    "مطابقةُ البايتات إثباتُ اشتقاقٍ لا إثباتُ صدق؛ "
    "وكودٌ مولَّدٌ من مواصفةٍ خاطئةٍ كودٌ خاطئٌ مُشتَقٌّ بأمانة"
)


class GeneratedArtifactManifestError(ValueError):
    """خطأُ بيانِ توليد: بصمةٌ ناقصةٌ أو غيرُ مطابقةٍ للمواصفة."""


def _require_digest(value: object, label: str) -> str:
    if not is_canonical_digest(value):
        raise GeneratedArtifactManifestError(f"{label} بصمةٌ قانونيّة")
    assert isinstance(value, str)
    return value


@dataclass(frozen=True, slots=True)
class GeneratedArtifactManifest:
    """بيانُ مجموعةِ آثارٍ: من أيِّ مواصفةٍ وبأيِّ مولِّدٍ وإلى أيِّ لغة."""

    backend_id: str
    target_language: str
    schema_digest: str
    sigma_digest: str
    generator_digest: str
    artifacts: GeneratedArtifactSet

    def __post_init__(self) -> None:
        for value, label in (
            (self.backend_id, "اسمُ الخلفيّة"),
            (self.target_language, "لغةُ الهدف"),
        ):
            if type(value) is not str or not value.strip():
                raise GeneratedArtifactManifestError(f"{label} نصٌّ غيرُ فارغ")
        _require_digest(self.schema_digest, "بصمةُ اللغة `Σ_M`")
        _require_digest(self.sigma_digest, "بصمةُ المواصفة `Σ_A`")
        _require_digest(self.generator_digest, "بصمةُ المولِّد")
        if self.sigma_digest == self.generator_digest:
            raise GeneratedArtifactManifestError(
                f"بصمةُ المواصفة غيرُ بصمةِ المولِّد؛ و{DETERMINISM_LAW}"
            )
        if not isinstance(self.artifacts, GeneratedArtifactSet):
            raise GeneratedArtifactManifestError("آثارُ البيان مجموعةُ آثارٍ مولَّدة")

    @property
    def artifact_count(self) -> int:
        """عددُ الآثار، مُشتَقٌّ من المجموعة."""

        return self.artifacts.artifact_count

    @property
    def artifact_paths(self) -> tuple[str, ...]:
        """مساراتُ الآثار مرتّبةً."""

        return self.artifacts.artifact_paths

    @property
    def determinism_key(self) -> tuple[str, str, str]:
        """مفتاحُ الحتميّة `(backend_id, digest Σ_A, digest g)`."""

        return (self.backend_id, self.sigma_digest, self.generator_digest)

    def describes(self, specification: AbstractSystemSpecification) -> bool:
        """هل يصف هذا البيانُ هذه المواصفةَ بعينها لغةً ومحتوى؟"""

        if not isinstance(specification, AbstractSystemSpecification):
            raise GeneratedArtifactManifestError("المقارَنُ مواصفةُ نظامٍ مجرّدة")
        return (
            specification.content_id == self.sigma_digest
            and specification.schema_ref.content_id == self.schema_digest
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البيان للبصمة."""

        return {
            "backend_id": self.backend_id,
            "target_language": self.target_language,
            "schema_digest": self.schema_digest,
            "sigma_digest": self.sigma_digest,
            "generator_digest": self.generator_digest,
            "artifacts": self.artifacts.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ البيان."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


_JUDGEMENT_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "verdict",
    "status",
    "standing",
    "birth",
    "proved",
)

for _field in fields(GeneratedArtifactManifest):  # pragma: no cover - import guard
    if any(marker in _field.name for marker in _JUDGEMENT_FIELD_MARKERS):
        raise RuntimeError(A_MANIFEST_IS_NOT_A_PROOF_OF_TRUTH)
    if any(marker in _field.name for marker in ("count", "coverage", "total")):
        raise RuntimeError("العدُّ مُشتَقٌّ من الآثار لا مكتوبٌ في البيان")
