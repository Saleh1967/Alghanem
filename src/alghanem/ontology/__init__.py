"""`O_0` و`O_L` — الأنطولوجيا: ما الموجود، ثمّ ما يستطيع أن يفعله لغةً.

    PK_0  →  O_0  →  O_L  →  O_{AR}

وهذه الحزمةُ ثاني مستوًى في محور الموجودات: تستورد من `prior/` و
`canonical_content` وحدَهما، ولا تستورد من `metaalgebra/` ولا `linguistic/` ولا
`arabic/` ولا `kernel/`؛ ويُفحَص الاتّجاهُ بشاهدٍ لا يُترَك لانتباه.

وحدتاها:

* `general` — `O_0`: مرشَّحو الأنواع العامّة، وكلُّ مرشَّحٍ بضرورةٍ وعدمِ
  اختزالٍ وموضعِ شرطٍ مُرخِّصٍ في `PK_0`.
* `linguistic` — `O_L`: الرخصُ الوظيفيّة، بجهةِ ترخيصٍ من النوع إلى الوظيفة،
  وبفصلٍ **نوعيٍّ** بين مرجع المرشَّح ومرجع الوظيفة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا تقرأ هذه الحزمةَ
بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

from .general import (
    AN_ONTOLOGICAL_CANDIDATE_IS_NOT_A_BORN_KIND,
    NECESSITY_AND_IRREDUCIBILITY_ARE_BOTH_REQUIRED,
    NO_LINGUISTIC_ROLE_IN_THE_GENERAL_ONTOLOGY,
    ONTOLOGICAL_CANDIDATE_NAMES,
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
    OntologyError,
    PriorBaseRef,
)
from .linguistic import (
    A_LICENSE_WITHOUT_A_CONDITION_IS_A_CONTAINMENT_CLAIM,
    AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE,
    LICENSING_IS_A_DIRECTION_NOT_A_CONTAINMENT,
    LINGUISTIC_FUNCTION_NAMES,
    ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE,
    THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS,
    FunctionalLicense,
    LinguisticFunction,
    LinguisticFunctionRef,
    LinguisticOntology,
    LinguisticOntologyError,
    OntologicalCandidateRef,
)

__all__ = [
    "AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE",
    "AN_ONTOLOGICAL_CANDIDATE_IS_NOT_A_BORN_KIND",
    "A_LICENSE_WITHOUT_A_CONDITION_IS_A_CONTAINMENT_CLAIM",
    "LICENSING_IS_A_DIRECTION_NOT_A_CONTAINMENT",
    "LINGUISTIC_FUNCTION_NAMES",
    "NECESSITY_AND_IRREDUCIBILITY_ARE_BOTH_REQUIRED",
    "NO_LINGUISTIC_ROLE_IN_THE_GENERAL_ONTOLOGY",
    "ONTOLOGICAL_CANDIDATE_NAMES",
    "ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE",
    "THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS",
    "FunctionalLicense",
    "GeneralOntology",
    "LinguisticFunction",
    "LinguisticFunctionRef",
    "LinguisticOntology",
    "LinguisticOntologyError",
    "OntologicalCandidate",
    "OntologicalCandidateRef",
    "OntologicalKind",
    "OntologyError",
    "PriorBaseRef",
]
