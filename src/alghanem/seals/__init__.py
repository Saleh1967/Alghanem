"""عدّةُ المحاسبة: سجلُّ أختامٍ لا يخزن رقمًا، وقانونُ وديعةٍ لا يقبل بلا فاتورة."""

from .deposit_law import (
    A_DELTA_ACROSS_TWO_SCOPES_IS_NOT_A_DELTA,
    A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED,
    A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN,
    AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE,
    DepositLawError,
    DepositRuling,
    Invoice,
    rule_on_deposit,
)
from .seal_registry import (
    A_QUOTATION_IS_NOT_A_CLAIM_OF_THIS_TREE,
    A_REGISTRY_THAT_STORES_A_VALUE_IS_A_SECOND_GRAVE,
    A_SEAL_WITHOUT_A_LIVE_GENERATOR_IS_A_GRAVE_NOT_A_SEAL,
    TWO_SIDES_THAT_NAME_DIFFERENT_FIELDS_DO_NOT_COLLIDE,
    Seal,
    SealError,
    SealGenus,
    SealReading,
    SealRegistry,
    SealVerdict,
)

__all__ = [
    "AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE",
    "A_DELTA_ACROSS_TWO_SCOPES_IS_NOT_A_DELTA",
    "A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED",
    "A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN",
    "A_QUOTATION_IS_NOT_A_CLAIM_OF_THIS_TREE",
    "A_REGISTRY_THAT_STORES_A_VALUE_IS_A_SECOND_GRAVE",
    "A_SEAL_WITHOUT_A_LIVE_GENERATOR_IS_A_GRAVE_NOT_A_SEAL",
    "DepositLawError",
    "DepositRuling",
    "Invoice",
    "Seal",
    "SealError",
    "SealGenus",
    "SealReading",
    "SealRegistry",
    "SealVerdict",
    "TWO_SIDES_THAT_NAME_DIFFERENT_FIELDS_DO_NOT_COLLIDE",
    "rule_on_deposit",
]
