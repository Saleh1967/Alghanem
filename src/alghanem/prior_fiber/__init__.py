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
    FiberImportIsolationReport,
    FiberVocabularyReport,
    fiber_import_isolation_audit,
    fiber_vocabulary_audit,
)
from .contract import (
    DomainMember,
    FiberContract,
    GoldSeal,
    SuccessCriterion,
    seal_gold,
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
    A_SEALED_GOLD_IS_A_DIGEST_NOT_AN_ANSWER,
    AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE,
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
    "A_SEALED_GOLD_IS_A_DIGEST_NOT_AN_ANSWER",
    "FIBER_AXIS_COUNT_IS_NOT_FROZEN_NOTE",
    "FORBIDDEN_ALGHANEM_PACKAGES",
    "FORBIDDEN_NAME_FRAGMENTS",
    "NO_POSITIVE_ROLE_FROM_A_NEUTRAL_FIBER_INPUT",
    "NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY",
    "OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN",
    "PERMITTED_ALGHANEM_MODULES",
    "PRIOR_FIBER_LAWS",
    "PRIOR_FIBER_NODE_POSITIONS",
    "THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY",
    "THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL",
    "AdmissibleDistinction",
    "DomainMember",
    "ExternalRankReference",
    "FiberAxis",
    "FiberContract",
    "FiberImportIsolationReport",
    "FiberVocabularyReport",
    "GoldSeal",
    "ParallelFiberBundle",
    "PriorFiberError",
    "PriorFiberNode",
    "ProjectedFiber",
    "SlotStanding",
    "SuccessCriterion",
    "fiber_import_isolation_audit",
    "fiber_vocabulary_audit",
    "project_all_fibers",
    "project_fiber",
    "seal_gold",
]
