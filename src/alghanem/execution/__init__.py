"""`G0.RUN-0`: أوّلُ شريحةٍ عموديّةٍ قابلةٍ للتشغيل — محرّكُ ترخيصٍ وتدقيق.

    PK_0 → O_0 → O_L² → ExistenceLineage → Nisbah_v3 → PASS | BLOCK | DEFER

وليس المقصودُ هنا فهمَ جملةٍ عربيّةٍ، بل أن تُعطى القضيّةُ **مُصرَّحًا بعناصرها**
فتُنفَّذ سلسلةُ الترخيص الحقيقيّةُ ويصدر قرارٌ قابلٌ للتدقيق وإعادة التشغيل.

وهذه الطبقةُ **فوق** محور الوجود: تستورد `PK_0` و`O_0` و`O_L²` والسلسلةَ و`v3`،
ولا يستوردها منها شيء؛ فبقاءُ معاني الطبقات السابقة غيرُ متوقّفٍ على وجودها.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from .audit import AN_AUDIT_READS_THE_TRACE_IT_DOES_NOT_JUDGE_AGAIN, audit_lines
from .contract import DecodedDocument, decode_document, encode_declaration
from .coverage import (
    A_MATRIX_MEASURES_THE_ENGINE_AS_FROZEN,
    A_MATRIX_NAMES_NO_CASE_AND_NO_DIGEST,
    AN_UNREACHABLE_CELL_IS_JUSTIFIED_NOT_INVENTED,
    CASE_EXPECTATION_IS_FROZEN_BEFORE_FIRST_ENGINE_READOUT,
    COVERAGE_MATRIX,
    COVERAGE_MATRIX_DIGEST,
    COVERAGE_MATRIX_ID,
    COVERAGE_REQUIREMENT_IS_FROZEN_BEFORE_CASE_SELECTION,
    CoverageAxis,
    CoverageMatrix,
    CoverageMatrixError,
    CoverageRequirement,
    ExpectedOutcome,
)
from .declaration import (
    A_DECLARATION_IS_NOT_AN_AUTHORITY,
    EXECUTION_DOCUMENT_SCHEMA,
    JUDGMENT_PRECEDES_CONSTRUCTION,
    AnchorDeclaration,
    CandidateDeclaration,
    CaseDeclaration,
    ConditionSiteDeclaration,
    GeneralOntologyDeclaration,
    LicenseDeclaration,
    LineageDeclaration,
    LinguisticOntologyDeclaration,
    NisbahDeclaration,
    PredicateDeclaration,
    PriorBaseDeclaration,
    PriorConditionDeclaration,
    RoleSiteDeclaration,
    SlotDeclaration,
)
from .derivation import (
    A_DERIVATION_IS_NOT_A_VERDICT,
    DerivedSite,
    PartialAuthorityDerivation,
    RefusalKind,
    SiteKey,
    SiteOwnerKind,
    SiteStanding,
    derive_partial_authority,
)
from .engine import ExecutionReport, execute_declaration, execute_document
from .invariant import (
    A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK,
    PASS_IFF_MATERIALIZED_IDENTITY,
    ExecutionInvariantError,
)
from .laws import (
    EVERY_LAW_IS_EVALUATED,
    aggregate_outcome,
    evaluate_laws,
    residuals_of,
    violations_of,
)
from .lawset import (
    A_LAW_SET_IS_NOT_REINTERPRETED_BY_A_LATER_ONE,
    DEPENDENT_LAWS,
    LAW_SET,
    LAW_SET_DIGEST,
    LAW_SET_ID,
    ExecutionLaw,
)
from .outcome import (
    A_BLOCKED_DEPENDENT_IS_NOT_MISSING_EVIDENCE,
    NO_CLAIM_IS_NOT_AN_AGREEMENT,
    NO_DEFAULT_SUCCESS_AND_NO_DEFAULT_BLOCK,
    CheckStanding,
    ExecutionOutcome,
    Identity,
    LawCheckEntry,
    Violation,
)
from .replay import SAME_INPUT_SAME_LAWS_SAME_RESULT, is_reproducible, replay
from .requirement import (
    AN_UNRESOLVED_REQUIREMENT_IS_NOT_A_FORGED_REFERENCE,
    UNRESOLVED_EVIDENCE_IS_NOT_INVALID_INPUT,
    RequiredAuthority,
    RequirementStanding,
    UnresolvedRequirement,
)
from .result import (
    A_DIGEST_DOES_NOT_CONTAIN_ITSELF,
    A_REPLAY_NEEDS_THE_DECLARATION_NOT_ITS_DIGEST,
    AN_ENVELOPE_HOLDS_AN_UNALTERABLE_DECLARATION,
    EXECUTION_RESULT_SCHEMA,
    ExecutionResultCore,
    ExecutionResultEnvelope,
    ExecutionResultError,
    LineageIdentity,
)
from .standing import (
    INVALID_INPUT_IS_NOT_A_BLOCK,
    InputFault,
    InputFaultKind,
    InputStanding,
    InputValidation,
)
from .validation import DeclaredLevels, validate_declaration

__all__ = [
    "AN_AUDIT_READS_THE_TRACE_IT_DOES_NOT_JUDGE_AGAIN",
    "AN_ENVELOPE_HOLDS_AN_UNALTERABLE_DECLARATION",
    "AN_UNREACHABLE_CELL_IS_JUSTIFIED_NOT_INVENTED",
    "AN_UNRESOLVED_REQUIREMENT_IS_NOT_A_FORGED_REFERENCE",
    "A_BLOCKED_DEPENDENT_IS_NOT_MISSING_EVIDENCE",
    "A_DECLARATION_IS_NOT_AN_AUTHORITY",
    "A_DERIVATION_IS_NOT_A_VERDICT",
    "A_DIGEST_DOES_NOT_CONTAIN_ITSELF",
    "A_LAW_SET_IS_NOT_REINTERPRETED_BY_A_LATER_ONE",
    "A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK",
    "A_MATRIX_MEASURES_THE_ENGINE_AS_FROZEN",
    "A_MATRIX_NAMES_NO_CASE_AND_NO_DIGEST",
    "A_REPLAY_NEEDS_THE_DECLARATION_NOT_ITS_DIGEST",
    "CASE_EXPECTATION_IS_FROZEN_BEFORE_FIRST_ENGINE_READOUT",
    "COVERAGE_MATRIX",
    "COVERAGE_MATRIX_DIGEST",
    "COVERAGE_MATRIX_ID",
    "COVERAGE_REQUIREMENT_IS_FROZEN_BEFORE_CASE_SELECTION",
    "DEPENDENT_LAWS",
    "EVERY_LAW_IS_EVALUATED",
    "EXECUTION_DOCUMENT_SCHEMA",
    "EXECUTION_RESULT_SCHEMA",
    "INVALID_INPUT_IS_NOT_A_BLOCK",
    "JUDGMENT_PRECEDES_CONSTRUCTION",
    "LAW_SET",
    "LAW_SET_DIGEST",
    "LAW_SET_ID",
    "NO_CLAIM_IS_NOT_AN_AGREEMENT",
    "NO_DEFAULT_SUCCESS_AND_NO_DEFAULT_BLOCK",
    "PASS_IFF_MATERIALIZED_IDENTITY",
    "SAME_INPUT_SAME_LAWS_SAME_RESULT",
    "UNRESOLVED_EVIDENCE_IS_NOT_INVALID_INPUT",
    "AnchorDeclaration",
    "CandidateDeclaration",
    "CaseDeclaration",
    "CheckStanding",
    "ConditionSiteDeclaration",
    "CoverageAxis",
    "CoverageMatrix",
    "CoverageMatrixError",
    "CoverageRequirement",
    "DecodedDocument",
    "DeclaredLevels",
    "DerivedSite",
    "ExecutionInvariantError",
    "ExecutionLaw",
    "ExecutionOutcome",
    "ExecutionReport",
    "ExecutionResultCore",
    "ExecutionResultEnvelope",
    "ExecutionResultError",
    "ExpectedOutcome",
    "GeneralOntologyDeclaration",
    "Identity",
    "InputFault",
    "InputFaultKind",
    "InputStanding",
    "InputValidation",
    "LawCheckEntry",
    "LicenseDeclaration",
    "LineageDeclaration",
    "LineageIdentity",
    "LinguisticOntologyDeclaration",
    "NisbahDeclaration",
    "PartialAuthorityDerivation",
    "PredicateDeclaration",
    "PriorBaseDeclaration",
    "PriorConditionDeclaration",
    "RefusalKind",
    "RequiredAuthority",
    "RequirementStanding",
    "RoleSiteDeclaration",
    "SiteKey",
    "SiteOwnerKind",
    "SiteStanding",
    "SlotDeclaration",
    "UnresolvedRequirement",
    "Violation",
    "aggregate_outcome",
    "audit_lines",
    "decode_document",
    "derive_partial_authority",
    "encode_declaration",
    "evaluate_laws",
    "execute_declaration",
    "execute_document",
    "is_reproducible",
    "replay",
    "residuals_of",
    "validate_declaration",
    "violations_of",
]
