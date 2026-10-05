"""`G0.EVAL-0.COMMITMENT`: التزامُ الجواب، رابطًا لا مشحونًا ولا مُخمَّنًا.

بصمةُ الجواب وحدَها التزامٌ ضعيفٌ في مجالٍ صغير: تُجرَّب التركيباتُ الممكنة
وتُحسَب بصماتُها حتّى تُصاب المطابقة. فالالتزامُ هنا يُحسَب على أربعةٍ معًا:

    commitment = H( canonical_gold ‖ nonce ‖ contract_body_digest ‖ scheme )

و`nonce` يدخل وسيطًا صريحًا من الخارج: لا قيمةَ افتراضيّة، ولا اشتقاقَ له من
محتوى العقد، ولا تعرف هذه الطبقةُ من أين جاء. وهو لا يُخزَّن في أيّ حقلٍ هنا،
فيُفحَص ذلك على الحقول لا بالدعوى.

وسقفُ الدعوى مُعلَنٌ قبل أيّ نتيجة: `DigestOnly != CryptographicallyHiddenGold`.
الالتزامُ يمنع تبديلَ الجواب بعد رؤية المخرجات، ويمنع التخمينَ على من لا يملك
المادّة؛ ولا يُسمّى إخفاءً تشفيريًّا ما دامت المادّةُ مقروءةً من موضعٍ آخر.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .laws import (
    A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED,
    DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD,
    PriorFiberError,
)

__all__ = [
    "COMMITMENT_SCHEME",
    "MINIMUM_NONCE_BITS",
    "GoldCommitment",
    "commit_gold",
    "gold_commitment_digest",
]

MINIMUM_NONCE_BITS: Final = 256
"""أدنى عشوائيّةٍ مقبولةٍ في الـnonce؛ وما دونها التزامٌ قابلٌ للتجربة الشاملة."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PriorFiberError(f"{label} نصٌّ غير فارغ")
    return value


def _require_nonce(nonce: object) -> bytes:
    if type(nonce) is not bytes:
        raise PriorFiberError("الـnonce بايتاتٌ صريحةٌ تُمرَّر، ولا يُشتَقُّ ولا يُفترَض")
    if len(nonce) * 8 < MINIMUM_NONCE_BITS:
        raise PriorFiberError(
            f"الـnonce أقصرُ من {MINIMUM_NONCE_BITS} بت؛ والقصيرُ يُجرَّب حتّى يُصاب"
        )
    if len(set(nonce)) < 2:
        raise PriorFiberError("الـnonce ثابتُ البايتات؛ وهذا عشوائيّةٌ مُدَّعاةٌ لا واقعة")
    return nonce


def _canonical_gold(labels: Mapping[str, str]) -> list[list[str]]:
    if not isinstance(labels, Mapping) or not labels:
        raise PriorFiberError("الجوابُ الملتزَمُ به مطابقةٌ غيرُ فارغة")
    for member_id, label in labels.items():
        _require_text(member_id, "مُعرِّفُ العضو في الجواب")
        _require_text(label, f"جوابُ `{member_id}`")
    return [[key, labels[key]] for key in sorted(labels)]


def gold_commitment_digest(
    labels: Mapping[str, str],
    *,
    gold_scheme: str,
    nonce: bytes,
    contract_body_digest: str,
) -> str:
    """احسب بصمةَ الالتزام على الجواب والـnonce وجسم العقد والصيغة معًا."""

    payload = {
        "canonical_gold": _canonical_gold(labels),
        "nonce": _require_nonce(nonce).hex(),
        "contract_body_digest": _require_body_digest(contract_body_digest),
        "gold_scheme": _require_text(gold_scheme, "بيانُ صيغة الجواب"),
    }
    return canonical_digest(canonical_bytes(payload))


def _require_body_digest(value: object) -> str:
    if not is_canonical_digest(value):
        raise PriorFiberError("بصمةُ جسم العقد بصمةٌ قانونيّةٌ لا نصٌّ حرّ")
    assert isinstance(value, str)
    return value


@dataclass(frozen=True, slots=True)
class GoldCommitment:
    """التزامُ الجواب: بصمتُه الرابطة، وصيغتُه، وعشوائيّتُه مُعلَنةً لا مُخزَّنة."""

    commitment_digest: str
    commitment_scheme: str
    gold_scheme: str
    contract_body_digest: str
    committed_member_count: int
    nonce_length_bits: int

    def __post_init__(self) -> None:
        if not is_canonical_digest(self.commitment_digest):
            raise PriorFiberError("بصمةُ الالتزام بصمةٌ قانونيّةٌ لا نصٌّ حرّ")
        _require_text(self.commitment_scheme, "بيانُ صيغة الالتزام")
        _require_text(self.gold_scheme, "بيانُ صيغة الجواب")
        _require_body_digest(self.contract_body_digest)
        if (
            not isinstance(self.committed_member_count, int)
            or self.committed_member_count < 1
        ):
            raise PriorFiberError("عددُ الأعضاء الملتزَم بها عددٌ صحيحٌ موجب")
        if (
            not isinstance(self.nonce_length_bits, int)
            or self.nonce_length_bits < MINIMUM_NONCE_BITS
        ):
            raise PriorFiberError(
                f"عشوائيّةُ الالتزام المُعلَنة دون {MINIMUM_NONCE_BITS} بت"
            )

    @property
    def binding_law(self) -> str:
        """قانونُ الالتزام: الجوابُ مربوطٌ لا مشحون."""

        return A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED

    @property
    def hiding_claim_ceiling(self) -> str:
        """سقفُ الدعوى: التزامٌ رابط، لا إخفاءٌ تشفيريٌّ للمادّة."""

        return DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD

    @property
    def withholds_its_nonce(self) -> bool:
        """أيخلو الالتزامُ من حقلٍ يحمل عشوائيّتَه؟ يُفحَص على الحقول لا بالدعوى."""

        return "nonce" not in tuple(GoldCommitment.__dataclass_fields__)

    def opens_with(
        self, labels: Mapping[str, str], *, nonce: bytes, contract_body_digest: str
    ) -> bool:
        """أيفتح هذا الجوابُ بهذه العشوائيّة هذا الالتزامَ بعينه؟"""

        if len(labels) != self.committed_member_count:
            return False
        if contract_body_digest != self.contract_body_digest:
            return False
        recomputed = gold_commitment_digest(
            labels,
            gold_scheme=self.gold_scheme,
            nonce=nonce,
            contract_body_digest=contract_body_digest,
        )
        return recomputed == self.commitment_digest

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الالتزام للبصمة."""

        return {
            "commitment_digest": self.commitment_digest,
            "commitment_scheme": self.commitment_scheme,
            "gold_scheme": self.gold_scheme,
            "contract_body_digest": self.contract_body_digest,
            "committed_member_count": self.committed_member_count,
            "nonce_length_bits": self.nonce_length_bits,
        }


COMMITMENT_SCHEME: Final = (
    "H(canonical_gold ‖ nonce ‖ contract_body_digest ‖ gold_scheme) بخوارزمية "
    "البصمة القانونيّة الواحدة في المشروع"
)


def commit_gold(
    labels: Mapping[str, str],
    *,
    gold_scheme: str,
    nonce: bytes,
    contract_body_digest: str,
) -> GoldCommitment:
    """التزِم بجوابٍ محجوب: احسب التزامَه ثمّ لا تحتفظ بجوابٍ ولا بعشوائيّة.

    الـ`nonce` وسيطٌ إلزاميّ: لا قيمةَ افتراضيّة، ولا يُشتَقُّ من العقد، ولا
    تعرف هذه الطبقةُ مصدرَه. ومن ولّده فهو مسؤولٌ عن إبقائه خارج المستودع.
    """

    digest = gold_commitment_digest(
        labels,
        gold_scheme=gold_scheme,
        nonce=nonce,
        contract_body_digest=contract_body_digest,
    )
    return GoldCommitment(
        commitment_digest=digest,
        commitment_scheme=COMMITMENT_SCHEME,
        gold_scheme=gold_scheme,
        contract_body_digest=contract_body_digest,
        committed_member_count=len(labels),
        nonce_length_bits=len(nonce) * 8,
    )
