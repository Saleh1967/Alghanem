"""`G0.EXEC-0.RUNNER`: مُشغِّلٌ قائمٌ بنفسه، يُنسَخ إلى مساحة التنفيذ ويُشغَّل فيها.

هذا الملفُّ لا يستورد `alghanem` ولا يبلغ المستودع: فهو يُنفَّذ في عمليّةٍ منفصلةٍ
بمساحةِ عملٍ مؤقّتةٍ خارج الشجرة، وسبيلُ استيراده مساحتُها وحدَها. ولذلك هو
قائمٌ بنفسه على المكتبة القياسيّة، ويُستورَد في عمليّة السلطة لقراءة ثوابته
وقياس بصمته فقط.

وسبيلُ الاستيراد يُضاف صراحةً: مساحةُ العمل وحدَها، لا شجرةُ المستودع ولا
`PYTHONPATH`، لأنّ `-I` يُسقِط مجلّدَ السكربت من المسار ولا يقرأ بيئة.

    stdin   ← مغلّفٌ مؤطَّر: طولٌ مُعلَن، ثمّ ترويسةٌ قانونيّة، ثمّ بايتاتُ الحمولة
    stdout  → بايتاتٌ قانونيّةٌ بصيغةٍ مغلقة: تصنيفاتٌ وبقايا وبصمةُ ما استُلِم
    exit    → 0 تمّ، 3 رفع القارئُ خطأً، 4 شكلُ ناتجٍ غيرُ قابلٍ للنقل،
              5 مغلّفٌ غيرُ قانونيّ، 6 مدخلٌ بتوقيعٍ غيرِ المُعلَن

    ConfigurationIsExecutedNotOnlyIdentified
    AWireValueIsRefusedNotCoerced

والقارئُ يُنادى بأرقامٍ ثابتة: `read(payload_bytes, configuration)`. ومن خالف
التوقيعَ يُرفَض تحت حالٍ مُسمّاة، ولا يُستدعى بأقرب شكل.

ولا `repr` ولا `pickle` في هذه القناة: ما لا يُسلسَل قانونيًّا لا يُنقَل. ولا
تطبيعَ متسامحًا: `"false"` ليست `False`، و`None` ليست `"None"`.
"""

from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import os
import sys
from types import MappingProxyType
from typing import Any

RUNNER_WIRE_PROTOCOL = "alghanem.g0_exec_0.reader_wire.v2"
"""إصدارُ قناة التسليم؛ يدخل بصمةَ المدخل، فلا يُنسَب ناتجُ قناةٍ إلى أخرى."""

READER_ENTRYPOINT_NAME = "read"
"""اسمُ المدخل المُثبَت؛ لا يُقرأ من القارئ ولا يُخمَّن."""

READER_ENTRYPOINT_PARAMETERS = ("payload_bytes", "configuration")
"""أرقامُ المدخل المُثبَتة؛ توقيعٌ صارمٌ بلا طريقٍ مهجورٍ مقبول."""

RESIDUAL_WIRE_FIELDS = (
    "blocking",
    "evidence_ref",
    "member_id",
    "reason",
    "residual_code",
)
"""حقولُ البقيّة في القناة؛ مجموعةٌ مطابقةٌ تمامًا، لا ناقصَ فيها ولا زائد."""

EXIT_COMPLETED = 0
EXIT_READER_RAISED = 3
EXIT_UNUSABLE_RESULT = 4
EXIT_UNUSABLE_ENVELOPE = 5
EXIT_REFUSED_ENTRYPOINT_SIGNATURE = 6


def split_envelope(framed: bytes) -> tuple[bytes, bytes]:
    """افصل الترويسةَ عن الحمولة بالأطوال المُعلَنة، لا بفاصلٍ يظهر في البايتات."""

    newline = framed.find(b"\n")
    if newline < 0:
        raise ValueError("مغلّفٌ بلا سطرِ أطوالٍ مُعلَن")
    lengths = framed[:newline].decode("ascii").split(" ")
    if len(lengths) != 2:
        raise ValueError("سطرُ الأطوال طولان: ترويسةٌ وحمولة")
    header_length = int(lengths[0])
    payload_length = int(lengths[1])
    if header_length < 0 or payload_length < 0:
        raise ValueError("طولٌ سالبٌ في سطر الأطوال")
    start = newline + 1
    header = framed[start : start + header_length]
    payload = framed[start + header_length : start + header_length + payload_length]
    if len(header) != header_length or len(payload) != payload_length:
        raise ValueError("مغلّفٌ أقصرُ من أطواله المُعلَنة")
    return header, payload


def _refused_text(value: Any, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{label} نصٌّ غير فارغ؛ ولا يُحوَّل نوعٌ خاطئ")
    return value


def normalized_result(result: Any) -> dict[str, Any]:
    """طبِّع ما أعاده القارئ إلى الصيغة المغلقة، رفضًا للنوع الخاطئ لا تحويلًا."""

    if isinstance(result, dict):
        outputs = result.get("outputs", ())
        residuals = result.get("residuals", ())
    else:
        outputs = result
        residuals = ()
    if not isinstance(outputs, list | tuple) or not isinstance(residuals, list | tuple):
        raise ValueError("التصنيفاتُ والبقايا متسلسلتان مُعلَنتان")
    normalized_outputs = []
    for entry in outputs:
        if not isinstance(entry, list | tuple) or len(entry) != 2:
            raise ValueError("المخرَجُ زوجٌ: عضوٌ وتصنيفُه")
        member_id = _refused_text(entry[0], "مُعرِّفُ العضو في المخرَج")
        normalized_outputs.append([member_id, _refused_text(entry[1], "تصنيفُ العضو")])
    normalized_residuals = []
    for residual in residuals:
        if not isinstance(residual, dict):
            raise ValueError("البقيّةُ بنيةٌ مُسمّاةٌ لا نصّ")
        if tuple(sorted(residual)) != RESIDUAL_WIRE_FIELDS:
            raise ValueError("حقولُ البقيّة مجموعةٌ مطابقة؛ ولا ناقصَ ولا زائد")
        if type(residual["blocking"]) is not bool:
            raise ValueError('صفةُ الإعاقة قيمةٌ ثنائيّة؛ و"false" ليست False')
        normalized_residuals.append(
            {
                "member_id": _refused_text(residual["member_id"], "عضوُ البقيّة"),
                "residual_code": _refused_text(residual["residual_code"], "رمزُ البقيّة"),
                "blocking": residual["blocking"],
                "reason": _refused_text(residual["reason"], "سببُ البقيّة"),
                "evidence_ref": _refused_text(
                    residual["evidence_ref"], "إحالةُ شاهد البقيّة"
                ),
            }
        )
    return {
        "protocol": RUNNER_WIRE_PROTOCOL,
        "outputs": normalized_outputs,
        "residuals": normalized_residuals,
    }


def takes_the_declared_signature(entrypoint: Any) -> bool:
    """أيقبل المدخلُ الأرقامَ المُثبَتة بعينها؟ يُقرَأ توقيعُه ولا يُجرَّب نداؤه."""

    try:
        parameters = inspect.signature(entrypoint).parameters
    except (TypeError, ValueError):
        return False
    positional = [
        parameter
        for parameter in parameters.values()
        if parameter.kind
        in (parameter.POSITIONAL_ONLY, parameter.POSITIONAL_OR_KEYWORD)
    ]
    if len(positional) != len(READER_ENTRYPOINT_PARAMETERS):
        return False
    return len(parameters) == len(positional)


def main(argv: list[str]) -> int:
    """استورد وحدةَ القارئ المنسوخة، سلِّمها البايتاتِ والإعدادَ، وانقل ناتجَها."""

    workspace = os.path.dirname(os.path.abspath(__file__))
    if workspace not in sys.path:
        sys.path.insert(0, workspace)
    module_name = argv[1]
    entrypoint_name = argv[2]
    try:
        header_bytes, payload_bytes = split_envelope(sys.stdin.buffer.read())
        header = json.loads(header_bytes.decode("utf-8"))
        configuration = MappingProxyType(
            {str(key): str(value) for key, value in header["configuration"]}
        )
    except Exception as error:  # noqa: BLE001 - مغلّفٌ غيرُ قانونيٍّ يُسمّى
        sys.stderr.write(f"unusable envelope: {type(error).__name__}: {error}\n")
        return EXIT_UNUSABLE_ENVELOPE
    envelope_digest = hashlib.sha256(header_bytes).hexdigest()
    module = importlib.import_module(module_name)
    entrypoint = getattr(module, entrypoint_name, None)
    if entrypoint is None or not callable(entrypoint):
        sys.stderr.write(f"no entrypoint named {entrypoint_name}\n")
        return EXIT_REFUSED_ENTRYPOINT_SIGNATURE
    if not takes_the_declared_signature(entrypoint):
        sys.stderr.write(
            f"{entrypoint_name} must take exactly"
            f" {', '.join(READER_ENTRYPOINT_PARAMETERS)}\n"
        )
        return EXIT_REFUSED_ENTRYPOINT_SIGNATURE
    try:
        result = entrypoint(payload_bytes, configuration)
    except Exception as error:  # noqa: BLE001 - الفشلُ يُنقَل ولا يُطوى
        sys.stderr.write(f"{type(error).__name__}: {error}\n")
        return EXIT_READER_RAISED
    try:
        normalized = normalized_result(result)
        normalized["envelope_digest"] = envelope_digest
        encoded = json.dumps(
            normalized,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8", "surrogatepass")
    except Exception as error:  # noqa: BLE001 - شكلٌ غيرُ قابلٍ للنقل يُسمّى
        sys.stderr.write(f"unusable result: {type(error).__name__}: {error}\n")
        return EXIT_UNUSABLE_RESULT
    sys.stdout.buffer.write(encoded)
    return EXIT_COMPLETED


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
