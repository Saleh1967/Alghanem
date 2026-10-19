"""`G0.EXEC-0.ENVELOPE`: مغلّفُ تنفيذٍ مؤطَّر، يعبُر به الإعدادُ إلى القارئ.

    ConfigurationIsExecutedNotOnlyIdentified

إعدادٌ يدخل تركيبَ الهويّة ولا يبلغ نداءَ القارئ يُثبِت هويّةَ إعدادٍ لا تنفيذَه.
فالقارئُ لا يستلم بايتاتِ الحمولة عاريةً على `stdin`، بل مغلّفًا مؤطَّرًا:

    b"<header_length> <payload_length>\\n" + header_bytes + payload_bytes

والترويسةُ بايتاتٌ قانونيّةٌ فيها إصدارُ المغلّف والإعدادُ وبصمتُه وبصمةُ الحمولة
وطولُها. والحمولةُ بعدها بايتاتٌ حرفيّةٌ كما سُلِّمت: لا `base64` ولا إعادةَ
ترميز، فتبقى `payload_digest` في الإيصال بصمةَ ما استلمه القارئ نفسِه.

وتأطيرٌ بطولٍ مُعلَنٍ لا بفاصلٍ مُخترَع: الفاصلُ يظهر في البايتات المحمولة،
والطولُ لا يظهر فيها.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..evaluation import measure_configuration_digest
from .laws import CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED, ExecutionError

__all__ = [
    "EXECUTION_ENVELOPE_PROTOCOL",
    "ExecutionEnvelope",
    "build_execution_envelope",
]

EXECUTION_ENVELOPE_PROTOCOL: Final[str] = "alghanem.g0_exec_0.execution_envelope.v1"
"""إصدارُ المغلّف؛ يدخل بصمةَ المدخل، فلا يُنسَب ناتجُ مغلّفٍ إلى آخر."""


class ExecutionEnvelope:
    """مغلّفٌ مُهيَّأ للتسليم: بايتاتُه المؤطَّرة، وبصمةُ ترويسته التي تُقارَن."""

    __slots__ = ("_configuration_digest", "_framed_bytes", "_header_bytes")

    def __init__(self, header_bytes: bytes, payload_bytes: bytes) -> None:
        if type(header_bytes) is not bytes or type(payload_bytes) is not bytes:
            raise ExecutionError("المغلّفُ يُبنى من بايتاتٍ لا من كائن")
        self._header_bytes = header_bytes
        self._framed_bytes = (
            f"{len(header_bytes)} {len(payload_bytes)}\n".encode("ascii")
            + header_bytes
            + payload_bytes
        )
        self._configuration_digest = canonical_digest(header_bytes)

    @property
    def framed_bytes(self) -> bytes:
        """البايتاتُ التي تدخل `stdin`: طولٌ مُعلَن، ثمّ ترويسة، ثمّ حمولةٌ حرفيّة."""

        return self._framed_bytes

    @property
    def header_bytes(self) -> bytes:
        """بايتاتُ الترويسة كما كُتِبت؛ منها تُشتَقُّ البصمةُ التي تُقارَن."""

        return self._header_bytes

    @property
    def envelope_digest(self) -> str:
        """بصمةُ الترويسة المكتوبة؛ يشهد المُشغِّلُ بمثلها عمّا استلم."""

        return self._configuration_digest

    @property
    def delivery_law(self) -> str:
        """قانونُ تسليم الإعداد: يُنفَّذ لا يُهوَّى فقط."""

        return CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED


def build_execution_envelope(
    *, configuration: Mapping[str, str], payload_bytes: bytes, payload_digest: str
) -> ExecutionEnvelope:
    """ابنِ مغلّفَ تنفيذٍ من إعدادٍ مقيسٍ وحمولةٍ مُجمَّدة، بلا تغييرٍ لبايتاتها."""

    if not isinstance(configuration, Mapping):
        raise ExecutionError("إعدادُ القارئ مطابقةٌ مُعلَنة")
    if type(payload_bytes) is not bytes:
        raise ExecutionError("حمولةُ القارئ بايتاتٌ مُسلسَلةٌ لا كائن")
    header = canonical_bytes(
        {
            "envelope_protocol": EXECUTION_ENVELOPE_PROTOCOL,
            "configuration": [
                [key, configuration[key]] for key in sorted(configuration)
            ],
            "configuration_digest": measure_configuration_digest(configuration),
            "payload_digest": payload_digest,
            "payload_length": len(payload_bytes),
        }
    )
    return ExecutionEnvelope(header, payload_bytes)
