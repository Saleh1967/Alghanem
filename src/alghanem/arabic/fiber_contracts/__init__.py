"""عقودُ المجالات العربيّة الموجَّهة إلى الطبقة الليفيّة المحايدة.

الاتّجاهُ واحدٌ: مادّةُ المجال تدخل إلى `prior_fiber` عبر مُحوِّلٍ هنا، ولا
تستورد الطبقةُ الليفيّة شيئًا من هذه الحزمة.
"""

from __future__ import annotations

from .madlul import (
    MADLUL_ASSIGNMENT_DISTINCTION_ID,
    MADLUL_CONTRACT_AUTHOR,
    MADLUL_GOLD_SCHEME,
    MADLUL_NATURE_DISTINCTION_ID,
    MADLUL_READING_SYSTEMS,
    MADLUL_STRUCTURE_DISTINCTION_ID,
    build_madlul_fiber_contract,
    build_madlul_fiber_node,
    madlul_domain_members,
    madlul_member_id,
    madlul_parallel_fibers,
    madlul_prior_base,
)

__all__ = [
    "MADLUL_ASSIGNMENT_DISTINCTION_ID",
    "MADLUL_CONTRACT_AUTHOR",
    "MADLUL_GOLD_SCHEME",
    "MADLUL_NATURE_DISTINCTION_ID",
    "MADLUL_READING_SYSTEMS",
    "MADLUL_STRUCTURE_DISTINCTION_ID",
    "build_madlul_fiber_contract",
    "build_madlul_fiber_node",
    "madlul_domain_members",
    "madlul_member_id",
    "madlul_parallel_fibers",
    "madlul_prior_base",
]
