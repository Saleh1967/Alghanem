"""حزمةُ التوليد: `G_py^g(Σ_A)` — أثرٌ تنفيذيٌّ مُشتَقّ، لا مصدرُ نظريّة.

    Σ_M  →  Σ_A  →  Realization(Σ_A, D)  →  Artifact = G_py^g(Σ_A)

**والحتميّةُ نسبيّةٌ إلى شيئين لا إلى واحد:**

    (digest Σ_A, digest g) = (digest Σ_A', digest g')  ⇒  bytes = bytes'

فلولا `g` لأمكن تغييرُ المولِّد مع ثبات `Σ_A` ثمّ ادّعاءُ أنّ «`Σ` ولّدت هذا
الكود»؛ ولذلك يحمل كلُّ بيانِ توليدٍ `sigma_digest` و`generator_digest`
و`backend_id`.

**ونواةُ `metaalgebra/` تبقى مكتوبةً يدويًّا:** لا يولِّد المولِّدُ نفسَه ولا
تعريفَ الميتا-جبر، فذلك يفتح دائرةَ تأسيسِ `Σ → G_py → Σ`. والاستضافةُ الذاتيّة
`G_py(Σ_core) ≅ Implementation_core` مبرهنةُ نقطةٍ ثابتةٍ مؤجَّلةٌ لا معلَمُ
اليوم.

**والعرضُ القانونيّ من عمل المولِّد لا من عمل مُنسِّق:** ترتيبٌ ثابت، وUTF-8،
وبلا طوابعَ زمنيّة؛ و`ruff format --check` فحصٌ بعدُ، لا تعريفٌ للحتميّة.

هذه الحزمةُ تستورد من `metaalgebra/` ولا تُستورَد فيها.
"""

from __future__ import annotations

from .artifact import (
    GENERATED_FILE_BANNER,
    GeneratedArtifact,
    GeneratedArtifactError,
    GeneratedArtifactSet,
)
from .backend import (
    GENERATED_CODE_IS_A_TRACE_NOT_A_SOURCE,
    GENERATION_IS_RELATIVE_TO_THE_GENERATOR_DIGEST,
    PYTHON_IS_THE_FIRST_GENERATED_TARGET_NOT_THE_THEORY,
    GeneratorBackend,
)
from .generator_identity import GENERATOR_SOURCE_MODULES, generator_digest
from .manifest import (
    DETERMINISM_LAW,
    GeneratedArtifactManifest,
    GeneratedArtifactManifestError,
)
from .python_backend import (
    NO_SEMANTICS_FROM_PROSE_IN_GENERATION,
    PYTHON_BACKEND_ID,
    PythonBackend,
    PythonBackendError,
    compile_expression,
    render_clause_contract,
)
from .python_realization import PYTHON_DOMAIN, python_realization
from .reference_specification import REFERENCE_SPECIFICATION

__all__ = [
    "DETERMINISM_LAW",
    "GENERATED_CODE_IS_A_TRACE_NOT_A_SOURCE",
    "GENERATED_FILE_BANNER",
    "GENERATION_IS_RELATIVE_TO_THE_GENERATOR_DIGEST",
    "GENERATOR_SOURCE_MODULES",
    "NO_SEMANTICS_FROM_PROSE_IN_GENERATION",
    "PYTHON_BACKEND_ID",
    "PYTHON_DOMAIN",
    "PYTHON_IS_THE_FIRST_GENERATED_TARGET_NOT_THE_THEORY",
    "REFERENCE_SPECIFICATION",
    "GeneratedArtifact",
    "GeneratedArtifactError",
    "GeneratedArtifactManifest",
    "GeneratedArtifactManifestError",
    "GeneratedArtifactSet",
    "GeneratorBackend",
    "PythonBackend",
    "PythonBackendError",
    "compile_expression",
    "generator_digest",
    "python_realization",
    "render_clause_contract",
]
