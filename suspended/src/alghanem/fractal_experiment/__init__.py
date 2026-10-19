"""`G0.FGEN-EX-0`: سلطةُ تشغيلٍ فراكتاليّةٌ تجريبيّةٌ مؤقّتة، لا ترخيصَ فيها.

    FrozenExperimentBinding
      → ExperimentalRunPermit (ISSUED → ACTIVE)
      → FractalTransition (من النواة)
      → ExperimentalFractalTransition
      → ExperimentalLiftPermit → ExperimentalNextScaleSeed
      → FractalExperimentalWitness
      → WitnessBundle
      → REVOKED

**والقانونُ الأعلى**: `ExperimentBeforeLicense`.

**والطبقةُ فوق النواة لا داخلَها**:

    fractal_experiment  →  fractal_generation
    fractal_generation  ↛  fractal_experiment

فلا تُعدَّل `fractal_generation/`، وتبقى `ScaleNecessityCertificate` مغلقةً
و`NextScaleSeed` غيرَ قابلةٍ للإصدار؛ وبذرةُ هذه الطبقة تجريبيّةٌ لا تُحوَّل
إلى الدائمة.

**وما لا يوجد هنا**: `License` ولا `LicensedPattern` ولا `LicensedTransition`
ولا `SufficiencyAssessment` ولا `LicensingCandidate`؛ وأكثرُ ما تبلغه الشواهدُ
المتراكمةُ في مرحلةٍ لاحقةٍ مرشَّحُ ترخيصٍ لا ترخيص.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from .authority import (
    ExperimentalAuthorityError,
    ExperimentalFractalAuthority,
    ExperimentalPermitState,
    ExperimentalRunPermit,
)
from .authority_gaps import (
    EXPERIMENTAL_AUTHORITY_GAPS,
    NO_LICENSING_AUTHORITY,
    NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
    NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT,
    NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,
    ExperimentalAuthorityGap,
    ExperimentalAuthorityGapError,
)
from .binding import (
    FrozenExperimentBinding,
    FrozenExperimentBindingError,
    FrozenInputEntry,
)
from .bundle import (
    WitnessBundle,
    WitnessBundleError,
    WitnessSufficiencyContract,
)
from .laws import (
    EXPERIMENT_BEFORE_LICENSE,
    EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN,
    EXPERIMENTAL_LIFT_TESTS_NECESSITY_IT_DOES_NOT_CERTIFY_NECESSITY,
    EXPERIMENTAL_NEXT_SCALE_SEED_IS_NOT_NEXT_SCALE_SEED,
    EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE,
    EXPERIMENTAL_SUCCESS_IS_A_WITNESS_NOT_A_LICENSE,
    EXPERIMENTAL_TRANSITION_IS_NOT_LICENSED_TRANSITION,
    FRACTAL_EXPERIMENT_LAW_SET_DIGEST,
    FRACTAL_EXPERIMENT_LAW_SET_ID,
    FRACTAL_EXPERIMENT_LAWS,
    FROZEN_EXPECTATION_IS_NOT_GENERATIVE_INPUT,
    FROZEN_INPUT_IS_NOT_PROVEN_STRUCTURE,
    SUFFICIENCY_CRITERION_MUST_PRECEDE_ITS_MEASUREMENT,
    SUFFICIENT_WITNESSES_OPEN_LICENSING_CANDIDATE_NOT_LICENSE,
    TEMPORARY_EXPERIMENTAL_AUTHORITY_IS_NOT_LICENSING_AUTHORITY,
    WITNESS_ACCUMULATION_PRECEDES_LICENSING,
    WITNESS_IS_NOT_JUDGMENT,
)
from .lift import (
    ExperimentalLiftCandidate,
    ExperimentalLiftDecision,
    ExperimentalLiftError,
    ExperimentalLiftGate,
    ExperimentalLiftPermit,
    ExperimentalLiftStatus,
    ExperimentalNextScaleSeed,
    issue_experimental_lift_permit,
)
from .transition import (
    ExperimentalFractalTransition,
    ExperimentalTransitionError,
    ExperimentalTransitionGate,
)
from .witness import (
    FORBIDDEN_RANK_VOCABULARY,
    ExperimentalStanding,
    FractalExperimentalWitness,
    WitnessError,
)

__all__ = [
    "EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN",
    "EXPERIMENTAL_AUTHORITY_GAPS",
    "EXPERIMENTAL_LIFT_TESTS_NECESSITY_IT_DOES_NOT_CERTIFY_NECESSITY",
    "EXPERIMENTAL_NEXT_SCALE_SEED_IS_NOT_NEXT_SCALE_SEED",
    "EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE",
    "EXPERIMENTAL_SUCCESS_IS_A_WITNESS_NOT_A_LICENSE",
    "EXPERIMENTAL_TRANSITION_IS_NOT_LICENSED_TRANSITION",
    "EXPERIMENT_BEFORE_LICENSE",
    "FORBIDDEN_RANK_VOCABULARY",
    "FRACTAL_EXPERIMENT_LAWS",
    "FRACTAL_EXPERIMENT_LAW_SET_DIGEST",
    "FRACTAL_EXPERIMENT_LAW_SET_ID",
    "FROZEN_EXPECTATION_IS_NOT_GENERATIVE_INPUT",
    "FROZEN_INPUT_IS_NOT_PROVEN_STRUCTURE",
    "ExperimentalAuthorityError",
    "ExperimentalAuthorityGap",
    "ExperimentalAuthorityGapError",
    "ExperimentalFractalAuthority",
    "ExperimentalFractalTransition",
    "ExperimentalLiftCandidate",
    "ExperimentalLiftDecision",
    "ExperimentalLiftError",
    "ExperimentalLiftGate",
    "ExperimentalLiftPermit",
    "ExperimentalLiftStatus",
    "ExperimentalNextScaleSeed",
    "ExperimentalPermitState",
    "ExperimentalRunPermit",
    "ExperimentalStanding",
    "ExperimentalTransitionError",
    "ExperimentalTransitionGate",
    "FractalExperimentalWitness",
    "FrozenExperimentBinding",
    "FrozenExperimentBindingError",
    "FrozenInputEntry",
    "NO_LICENSING_AUTHORITY",
    "NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT",
    "NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT",
    "NO_SUFFICIENCY_ASSESSMENT_AUTHORITY",
    "SUFFICIENCY_CRITERION_MUST_PRECEDE_ITS_MEASUREMENT",
    "SUFFICIENT_WITNESSES_OPEN_LICENSING_CANDIDATE_NOT_LICENSE",
    "TEMPORARY_EXPERIMENTAL_AUTHORITY_IS_NOT_LICENSING_AUTHORITY",
    "WITNESS_ACCUMULATION_PRECEDES_LICENSING",
    "WITNESS_IS_NOT_JUDGMENT",
    "WitnessBundle",
    "WitnessBundleError",
    "WitnessError",
    "WitnessSufficiencyContract",
    "issue_experimental_lift_permit",
]
