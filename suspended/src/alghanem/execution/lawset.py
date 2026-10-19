"""قائمةُ القوانين مُجمَّدةً مرتَّبة؛ وهويّتُها مُشتَقّةٌ لا مكتوبة.

    law_set_digest = Digest(law_1, …, law_n)

**وقائمةُ القوانين جزءٌ من هويّة التنفيذ** (`ALawSetIsNotReinterpretedByALaterOne`):
تغييرُ قانونٍ أو حذفُه أو تغييرُ رتبته في القائمة يغيّر بصمةَ القائمة، فتغيّر
هويّةَ كلِّ نتيجةٍ صدرت بها. وبذلك لا يُعاد تفسيرُ حكمٍ قديمٍ بقائمةٍ جديدة:
النتيجةُ تحمل القائمةَ التي حكمت بها، لا القائمةَ القائمةَ اليوم.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "A_LAW_SET_IS_NOT_REINTERPRETED_BY_A_LATER_ONE",
    "LAW_SET",
    "LAW_SET_DIGEST",
    "LAW_SET_ID",
    "DEPENDENT_LAWS",
    "ExecutionLaw",
]


A_LAW_SET_IS_NOT_REINTERPRETED_BY_A_LATER_ONE: Final[str] = (
    "القائمةُ لا يُعاد تفسيرُها بقائمةٍ بعدها: النتيجةُ تحمل بصمةَ القوانين التي "
    "حكمت بها، فتغييرُ قانونٍ أو رتبته يُنشئ هويّةَ تنفيذٍ أخرى ولا يمسّ ما مضى"
)


class ExecutionLaw(Enum):
    """قوانينُ `G0.RUN-0`؛ مفردةٌ مغلقةٌ ورتبتُها فيها محتوًى قانونيّ."""

    NO_SELF_DERIVED_LICENSING_GENUS = "no_self_derived_licensing_genus"
    NO_UNREAD_CONDITION_IN_THE_FOUNDING_BASE = (
        "no_unread_condition_in_the_founding_base"
    )
    GENERAL_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_BASE = (
        "general_ontology_founded_on_the_lineage_base"
    )
    LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES = (
        "linguistic_licenses_name_registered_candidates"
    )
    LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE = (
        "linguistic_licenses_share_the_founding_base"
    )
    LINGUISTIC_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_GENERAL = (
        "linguistic_ontology_founded_on_the_lineage_general"
    )
    EXISTENCE_LINEAGE_REDERIVES = "existence_lineage_rederives"
    CONDITION_SITES_SHARE_THE_LINEAGE_BASE = "condition_sites_share_the_lineage_base"
    CONDITION_SITES_ARE_LICENSED_FOR_USE = "condition_sites_are_licensed_for_use"
    ROLE_SITES_SHARE_THE_LINEAGE_ONTOLOGY = "role_sites_share_the_lineage_ontology"
    ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ = (
        "role_license_granted_for_the_function_read"
    )
    ROLE_LICENSE_IS_OPERATIVE = "role_license_is_operative"
    PREDICATE_ARITY_LICENSE_PERMITS_USE = "predicate_arity_license_permits_use"
    PREDICATE_ARITY_MATCHES_ITS_SLOTS = "predicate_arity_matches_its_slots"
    ARGUMENT_SLOT_IDS_ARE_NOT_DEFERRED_ROLE_NAMES = (
        "argument_slot_ids_are_not_deferred_role_names"
    )
    ANCHORS_DO_NOT_EXCEED_ARITY = "anchors_do_not_exceed_arity"
    DECLARED_LINGUISTIC_IDENTITY_AGREES = "declared_linguistic_identity_agrees"
    MATERIALIZED_IDENTITY_AGREES = "materialized_identity_agrees"


LAW_SET: Final[tuple[ExecutionLaw, ...]] = tuple(ExecutionLaw)
"""ترتيبُ القوانين مُشتَقٌّ من المفردة نفسِها؛ ولا نسخةَ ثانيةً تنحرف عنه."""

DEPENDENT_LAWS: Final[tuple[ExecutionLaw, ...]] = (
    ExecutionLaw.DECLARED_LINGUISTIC_IDENTITY_AGREES,
    ExecutionLaw.MATERIALIZED_IDENTITY_AGREES,
)
"""القوانينُ التابعة: مادّتُها لا توجد إلّا بعد نجاح ما قبلها."""

LAW_SET_ID: Final[str] = "alghanem.execution.laws.G0.RUN-0"
"""اسمُ القائمة؛ وهويّتُها الحاكمةُ بصمتُها لا اسمُها."""

LAW_SET_DIGEST: Final[str] = canonical_digest(
    canonical_bytes({"law_set_id": LAW_SET_ID, "laws": [law.value for law in LAW_SET]})
)
"""بصمةُ القائمة المرتَّبة؛ تتغيّر بتغيّر قانونٍ أو رتبته أو حذفه."""
