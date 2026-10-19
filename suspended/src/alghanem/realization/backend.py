"""عقدُ الخلفيّة المولِّدة: `G^g_D : Σ_A ⟼ (Artifacts, Manifest)`.

    G_python(Σ_A) ,  G_rust(Σ_A) ,  …

فالمولِّداتُ كثيرةٌ والأصلُ واحد. وPython أوّلُ لغةِ تنفيذٍ مولَّدة، لا جزءٌ من
جوهر النظريّة؛ ولو بُدِّلت غدًا بلغةٍ أخرى لبقي `Σ_A` كما هو.

**والمولِّدُ دالّةٌ من المواصفة وحدها:** لا يقرأ ساعةً ولا بيئةً ولا ملفًّا
خارجيًّا، وإلّا صارت بايتاتُه دالّةً على لحظة التشغيل فانكسرت الحتميّة بلا خطأٍ
ظاهر.

**والكودُ المولَّد أثرٌ لا مصدر:** لا يُستورَد في `metaalgebra/` ولا يُعتمَد
عليه في تعريفِ الجبر؛ فذلك يفتح دائرةَ `Σ → G → Σ`.
"""

from __future__ import annotations

from typing import Final, Protocol, runtime_checkable

from ..metaalgebra.specification import AbstractSystemSpecification
from .artifact import GeneratedArtifactSet
from .manifest import GeneratedArtifactManifest

__all__ = [
    "GENERATED_CODE_IS_A_TRACE_NOT_A_SOURCE",
    "GENERATION_IS_RELATIVE_TO_THE_GENERATOR_DIGEST",
    "PYTHON_IS_THE_FIRST_GENERATED_TARGET_NOT_THE_THEORY",
    "GeneratorBackend",
]

GENERATION_IS_RELATIVE_TO_THE_GENERATOR_DIGEST: Final = (
    "التوليدُ دالّةُ `(Σ_A, g)`؛ ومولِّدٌ بلا بصمةٍ يجعل ادّعاءَ الاشتقاق " "غيرَ قابلٍ للتكذيب"
)

GENERATED_CODE_IS_A_TRACE_NOT_A_SOURCE: Final = (
    "الكودُ المولَّد أثرٌ تنفيذيٌّ مُشتَقٌّ من الدستور؛ ولا يُستورَد في "
    "`metaalgebra/` كي لا تنعقد دائرةُ `Σ → G → Σ`"
)

PYTHON_IS_THE_FIRST_GENERATED_TARGET_NOT_THE_THEORY: Final = (
    "Python أوّلُ لغةِ تنفيذٍ مولَّدة، لا جزءٌ من جوهر النظريّة؛ "
    "وتبديلُ لغةِ التنفيذ لا يغيّر `Σ_A`"
)


@runtime_checkable
class GeneratorBackend(Protocol):
    """خلفيّةٌ مولِّدة: هُويّةٌ مبصومةٌ ودالّةُ توليدٍ من المواصفة وحدها."""

    @property
    def backend_id(self) -> str:
        """اسمُ الخلفيّة، يدخل في مفتاح الحتميّة."""

    @property
    def target_language(self) -> str:
        """لغةُ الهدف التي تُعرَض بها الآثار."""

    @property
    def generator_digest(self) -> str:
        """بصمةُ المولِّد `digest(g)` من بايتات مصدره."""

    def generate(
        self, specification: AbstractSystemSpecification
    ) -> GeneratedArtifactSet:
        """آثارُ التوليد من المواصفة وحدها، بلا قراءةِ ساعةٍ ولا بيئة."""

    def manifest(
        self, specification: AbstractSystemSpecification
    ) -> GeneratedArtifactManifest:
        """بيانُ التوليد حاملًا `sigma_digest` و`generator_digest` و`backend_id`."""
