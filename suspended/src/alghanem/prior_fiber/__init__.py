"""`G0.FIBER-0`: المعلوماتُ السابقة المنظَّمة عقدةً ليفيّةً، وثلاثةَ ألياف متوازية.

هذه الطبقةُ تُجمِّد ما يُقرَأ لاحقًا بنظامين متوازيين، ولا تملك نظامًا ولا تُجري
مقارنةً ولا تفتح جوابًا محجوبًا. وهي محايدةٌ عن كلِّ مجالٍ بعينه: مادّةُ المجال
تدخل عبر مُحوِّلٍ خارجها، ولا تُستورَد من داخلها.
"""

from __future__ import annotations

from .audit import (
    FORBIDDEN_ALGHANEM_PACKAGES,
    FORBIDDEN_NAME_FRAGMENTS,
    PERMITTED_ALGHANEM_MODULES,
    PRIOR_FIBER_IMPORT_POLICY,
    FiberImportIsolationReport,
    FiberVocabularyReport,
    fiber_import_isolation_audit,
    fiber_vocabulary_audit,
)
from .commitment import (
    COMMITMENT_SCHEME,
    MINIMUM_NONCE_BITS,
    GoldCommitment,
    commit_gold,
    gold_commitment_digest,
)
from .contract import (
    DomainMember,
    FiberContract,
    FiberContractBody,
    SuccessCriterion,
)
from .fibers import (
    FIBER_AXIS_COUNT_IS_NOT_FROZEN_NOTE,
    FiberAxis,
    ParallelFiberBundle,
    ProjectedFiber,
    project_all_fibers,
    project_fiber,
)
from .laws import (
    A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED,
    AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE,
    DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD,
    FROZEN_CONTRACT_BEFORE_READERS,
    NO_POSITIVE_ROLE_FROM_A_NEUTRAL_FIBER_INPUT,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
    PRIOR_FIBER_LAWS,
    THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY,
    THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL,
    PriorFiberError,
)
from .node import (
    PRIOR_FIBER_NODE_POSITIONS,
    AdmissibleDistinction,
    ExternalRankReference,
    PriorFiberNode,
    SlotStanding,
)

__all__ = [
    "AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE",
    "A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED",
    "COMMITMENT_SCHEME",
    "DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD",
    "FIBER_AXIS_COUNT_IS_NOT_FROZEN_NOTE",
    "FROZEN_CONTRACT_BEFORE_READERS",
    "FORBIDDEN_ALGHANEM_PACKAGES",
    "FORBIDDEN_NAME_FRAGMENTS",
    "NO_POSITIVE_ROLE_FROM_A_NEUTRAL_FIBER_INPUT",
    "MINIMUM_NONCE_BITS",
    "NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY",
    "OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN",
    "PERMITTED_ALGHANEM_MODULES",
    "PRIOR_FIBER_IMPORT_POLICY",
    "PRIOR_FIBER_LAWS",
    "PRIOR_FIBER_NODE_POSITIONS",
    "THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY",
    "THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL",
    "AdmissibleDistinction",
    "DomainMember",
    "ExternalRankReference",
    "FiberAxis",
    "FiberContract",
    "FiberContractBody",
    "FiberImportIsolationReport",
    "FiberVocabularyReport",
    "GoldCommitment",
    "ParallelFiberBundle",
    "PriorFiberError",
    "PriorFiberNode",
    "ProjectedFiber",
    "SlotStanding",
    "SuccessCriterion",
    "commit_gold",
    "fiber_import_isolation_audit",
    "fiber_vocabulary_audit",
    "gold_commitment_digest",
    "project_all_fibers",
    "project_fiber",
]
