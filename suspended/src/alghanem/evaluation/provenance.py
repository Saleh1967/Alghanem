"""`G0.EXEC-0.PROVENANCE`: إصدارٌ بمفتاحٍ تملكه السلطة، وسقفُه مُعلَنٌ لا مُدَّعًى.

    ReceiptIssuanceIsKeyedNotMerelySealed
    AnInProcessSealIsNotUnforgeableProvenance

الختمُ الخاصُّ بوحدةٍ يمنع البناءَ من الواجهة العامّة ولا يُنتِج أثرًا يُتحقَّق
منه بعد الإصدار: من حمل الختمَ أصدر، ومن نظر في الإيصال بعدئذٍ لم يجد في متنه ما
يشهد لمن أصدره. فيُضاف إلى الختم مفتاحُ إصدارٍ تملكه سلطةُ التنفيذ، ويُوقَّع به
محتوى الإيصال، فيصير في المتن أثرٌ يُقارَن.

وسقفُ هذا الطور مُعلَنٌ صراحةً: المفتاحُ يُولَّد في عمليّة السلطة نفسِها ويعيش
فيها، فالشفرةُ الجارية في العمليّة ذاتها تبلغه كما تبلغ الختم. فهذا إصدارٌ
مُفتَّحٌ داخل عمليّةٍ واحدة، لا إصدارٌ غيرُ قابلٍ للتزوير عبر حدِّ ثقة؛ وذاك
يحتاج أمينَ مفاتيحَ خارجَ العمليّة أو سجلَّ إصدارٍ تملكه سلطةٌ معزولة، وهو
مؤجَّلٌ مُعلَنًا. ولذلك `is_proven` كاذبةٌ بالبناء، والثقةُ العابرةُ للجلسات
ليست مُدَّعاةً هنا: المفتاحُ لكلِّ سلطةٍ ولا يعبُر إعادةَ تشغيل.
"""

from __future__ import annotations

import hmac
import secrets
from enum import Enum
from typing import Final

from ..canonical_content import (
    CANONICAL_HASH_ALGORITHM,
    canonical_bytes,
    canonical_digest,
    is_canonical_digest,
)
from .laws import (
    AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE,
    RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED,
    EvaluationError,
)

__all__ = [
    "ISSUANCE_SIGNATURE_ALGORITHM",
    "IssuanceProvenanceStanding",
    "ReceiptIssuanceKey",
    "issuance_signature",
    "verify_issuance_signature",
]

ISSUANCE_SIGNATURE_ALGORITHM: Final[str] = f"hmac-{CANONICAL_HASH_ALGORITHM}"
"""خوارزميّةُ التوقيع المُعلَنة؛ فوق البدائيّة القانونيّة نفسِها لا بجانبها."""

_KEY_BYTES: Final[int] = 32
"""طولُ سرِّ الإصدار؛ يُولَّد من مصدرٍ عشوائيٍّ مناسبٍ للاستعمال المفتاحيّ."""


class IssuanceProvenanceStanding(Enum):
    """حالُ نسبِ الإصدار؛ ويُسجَّل تأجيلُ ما لم يُبنَ تصريحًا لا صمتًا."""

    IN_PROCESS_KEYED_DECLARED = "in_process_keyed_declared"

    @property
    def is_proven(self) -> bool:
        """أمُثبَتٌ نسبُ الإصدار عبر حدِّ ثقة؟ ولا عضوَ كذلك فيه بالبناء."""

        return False

    @property
    def ceiling(self) -> str:
        """سقفُ ما يُدَّعى بمفتاحٍ يعيش في عمليّة السلطة نفسِها."""

        return AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE


class ReceiptIssuanceKey:
    """مفتاحُ إصدارٍ تملكه سلطةُ تنفيذٍ واحدة؛ سرُّه لا يُسلسَل ولا يُعرَض.

    ليس هذا `dataclass`: التجميدُ يصف محتوًى يُقرَأ، والمفتاحُ سرٌّ لا يُقرَأ.
    و`key_id` مُشتَقٌّ من مادّةٍ عامّةٍ مرافقة لا من السرّ، فلا يكون المُعرِّفُ
    نفسُه بابًا إليه.
    """

    __slots__ = ("_public_material", "_secret")

    def __init__(self) -> None:
        self._secret = secrets.token_bytes(_KEY_BYTES)
        self._public_material = secrets.token_hex(_KEY_BYTES)

    @property
    def key_id(self) -> str:
        """مُعرِّفُ المفتاح العامّ؛ يدخل الإيصالَ ويُقارَن، ولا يُشتَقُّ من السرّ."""

        return canonical_digest(
            canonical_bytes(
                {
                    "issuance_key_material": self._public_material,
                    "signature_algorithm": ISSUANCE_SIGNATURE_ALGORITHM,
                }
            )
        )

    @property
    def standing(self) -> IssuanceProvenanceStanding:
        """حالُ نسبِ الإصدار بهذا المفتاح؛ مُعلَنٌ داخل العمليّة لا مُثبَت."""

        return IssuanceProvenanceStanding.IN_PROCESS_KEYED_DECLARED

    @property
    def is_proven(self) -> bool:
        """أمُثبَتٌ نسبُ الإصدار؟ كاذبةٌ بالبناء في هذا الطور."""

        return self.standing.is_proven

    @property
    def ceiling(self) -> str:
        """سقفُ ما يُدَّعى بهذا المفتاح."""

        return self.standing.ceiling

    @property
    def issuance_law(self) -> str:
        """قانونُ الإصدار المُفتَّح."""

        return RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED

    def _sign(self, content: bytes) -> str:
        if type(content) is not bytes:
            raise EvaluationError("التوقيعُ يقع على بايتاتٍ قانونيّةٍ لا على كائن")
        return hmac.new(self._secret, content, CANONICAL_HASH_ALGORITHM).hexdigest()

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المفتاح للعرض والسجلّ: مُعرِّفُه وسقفُه، ولا سرَّ فيه."""

        return {
            "key_id": self.key_id,
            "signature_algorithm": ISSUANCE_SIGNATURE_ALGORITHM,
            "standing": self.standing.value,
            "is_proven": self.is_proven,
            "ceiling": self.ceiling,
        }

    def __repr__(self) -> str:
        """عرضٌ لا يحمل سرًّا؛ فالسرُّ لا يُطبَع في أثرٍ ولا في رسالة خطأ."""

        return f"ReceiptIssuanceKey(key_id={self.key_id!r})"


def issuance_signature(key: ReceiptIssuanceKey, content: dict[str, object]) -> str:
    """وقِّع محتوى إيصالٍ بمفتاح سلطته؛ التوقيعُ أثرٌ في المتن لا ختمٌ في الذاكرة."""

    if not isinstance(key, ReceiptIssuanceKey):
        raise EvaluationError("التوقيعُ يقع بمفتاح إصدارٍ من نوعه")
    if not isinstance(content, dict):
        raise EvaluationError("محتوى التوقيع بنيةٌ مُسمّاةٌ قانونيّة")
    return key._sign(canonical_bytes(content))


def verify_issuance_signature(
    key: ReceiptIssuanceKey, content: dict[str, object], signature: object
) -> bool:
    """أتَشهدُ هذه السلطةُ لهذا المحتوى بهذا التوقيع؟ مقارنةً ثابتةَ الزمن."""

    if not is_canonical_digest(signature):
        return False
    assert isinstance(signature, str)
    return hmac.compare_digest(issuance_signature(key, content), signature)
