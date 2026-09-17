"""`PK_0` — المعلومات السابقة المنظَّمة: شروطُ إمكان الأنطولوجيا، لا حقائقُها.

    المعلومات السابقة المنظَّمة  →  الأنطولوجيا العامّة  →  الأنطولوجيا اللغويّة
                                 →  أنطولوجيا العربيّة

وهذه الحزمةُ أسبقُ مستوًى في **محور الموجودات**؛ ومحورُ الجبر
(`Σ_M ⇝ Σ_L ⇝ Σ_AR`) يعمل على هذه الموجودات ولا يخلقها.

**والتبعيّةُ أحاديّةُ الاتّجاه**: هذه الحزمةُ تستورد من `canonical_content`
وحدَه، ولا تستورد من `metaalgebra/` ولا `linguistic/` ولا `arabic/` ولا
`kernel/` حرفًا؛ ويُفحَص الاتّجاهُ بشاهدٍ لا يُترَك لانتباه.

وحدتاها:

* `hypothesis` — نصُّ `G0.PK-0` مُجمَّدًا، وفاحصُ أمانةٍ قبليٌّ لمواضعه الحاسمة.
* `conditions` — المواضعُ التسعةُ وقاعدتُها، بتغطيةٍ تامّةٍ ومصدرِ ترخيصٍ لكلِّ شرط.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا تقرأ هذه الحزمةَ
بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

from .conditions import (
    A_CONDITION_NAMES_WHAT_IT_FORBIDS,
    AN_UNREAD_CONDITION_IS_NOT_A_SATISFIED_ONE,
    NO_READY_MADE_FACT_IN_THE_PRIOR_BASE,
    PRIOR_CONDITION_NAMES,
    PRIOR_COVERAGE_IS_EXACT_NOT_BEST_EFFORT,
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorInformationError,
    PriorLicenseGenus,
)
from .hypothesis import (
    A_LAYER_THAT_FOUND_A_LAYER_BENEATH_IT_IS_NOT_REFUTED_NOTE,
    AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE_NOTE,
    AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE,
    FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE,
    FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION_NOTE,
    NO_READOUT_EXISTS_FOR_PK0_YET_NOTE,
    ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE_NOTE,
    PRIOR_HYPOTHESIS_NAMED_RESIDUALS,
    PRIOR_HYPOTHESIS_TEXT,
    PRIOR_INFORMATION_ORDERS_POSSIBILITY_NOT_RESULT_NOTE,
    PRIOR_TEXT_DIGEST,
    REQUIRED_NOTATION_SITES,
    THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS_NOTE,
    FidelityReport,
    FidelitySiteReading,
    FidelityStanding,
    NotationSite,
    PriorHypothesisError,
    derive_fidelity_report,
    prior_text_digest,
)

__all__ = [
    "AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE_NOTE",
    "AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE",
    "AN_UNREAD_CONDITION_IS_NOT_A_SATISFIED_ONE",
    "A_CONDITION_NAMES_WHAT_IT_FORBIDS",
    "A_LAYER_THAT_FOUND_A_LAYER_BENEATH_IT_IS_NOT_REFUTED_NOTE",
    "FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE",
    "FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION_NOTE",
    "NO_READOUT_EXISTS_FOR_PK0_YET_NOTE",
    "NO_READY_MADE_FACT_IN_THE_PRIOR_BASE",
    "ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE_NOTE",
    "PRIOR_CONDITION_NAMES",
    "PRIOR_COVERAGE_IS_EXACT_NOT_BEST_EFFORT",
    "PRIOR_HYPOTHESIS_NAMED_RESIDUALS",
    "PRIOR_HYPOTHESIS_TEXT",
    "PRIOR_INFORMATION_ORDERS_POSSIBILITY_NOT_RESULT_NOTE",
    "PRIOR_TEXT_DIGEST",
    "REQUIRED_NOTATION_SITES",
    "THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS_NOTE",
    "FidelityReport",
    "FidelitySiteReading",
    "FidelityStanding",
    "NotationSite",
    "PriorCondition",
    "PriorConditionKind",
    "PriorHypothesisError",
    "PriorInformationBase",
    "PriorInformationError",
    "PriorLicenseGenus",
    "derive_fidelity_report",
    "prior_text_digest",
]
