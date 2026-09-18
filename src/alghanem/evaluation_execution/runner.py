"""`G0.EXEC-0.RUNNER`: مُشغِّلٌ قائمٌ بنفسه، يُنسَخ إلى مساحة التنفيذ ويُشغَّل فيها.

هذا الملفُّ لا يستورد `alghanem` ولا يبلغ المستودع: فهو يُنفَّذ في عمليّةٍ منفصلةٍ
بمساحةِ عملٍ مؤقّتةٍ خارج الشجرة، وسبيلُ استيراده مساحتُها وحدَها. ولذلك هو
قائمٌ بنفسه على المكتبة القياسيّة، ويُستورَد في عمليّة السلطة لقراءة ثوابته
وقياس بصمته فقط.

وسبيلُ الاستيراد يُضاف صراحةً: مساحةُ العمل وحدَها، لا شجرةُ المستودع ولا
`PYTHONPATH`، لأنّ `-I` يُسقِط مجلّدَ السكربت من المسار ولا يقرأ بيئة.

    stdin   ← بايتاتُ الحمولة العمياء
    stdout  → بايتاتٌ قانونيّةٌ بصيغةٍ مغلقة: تصنيفاتٌ وبقايا
    exit    → 0 تمّ، 3 رفع القارئُ خطأً، 4 شكلُ ناتجٍ غيرُ قابلٍ للنقل

ولا `repr` ولا `pickle` في هذه القناة: ما لا يُسلسَل قانونيًّا لا يُنقَل.
"""

from __future__ import annotations

import importlib
import json
import os
import sys
from typing import Any

RUNNER_WIRE_PROTOCOL = "alghanem.g0_exec_0.reader_wire.v1"
"""إصدارُ قناة التسليم؛ يدخل بصمةَ المدخل، فلا يُنسَب ناتجُ قناةٍ إلى أخرى."""

READER_ENTRYPOINT_NAME = "read"
"""اسمُ المدخل المُثبَت؛ لا يُقرأ من القارئ ولا يُخمَّن."""

EXIT_COMPLETED = 0
EXIT_READER_RAISED = 3
EXIT_UNUSABLE_RESULT = 4


def normalized_result(result: Any) -> dict[str, Any]:
    """طبِّع ما أعاده القارئ إلى الصيغة المغلقة: تصنيفاتٌ وبقايا."""

    if isinstance(result, dict):
        outputs = result.get("outputs", ())
        residuals = result.get("residuals", ())
    else:
        outputs = result
        residuals = ()
    normalized_outputs = []
    for entry in outputs:
        pair = list(entry)
        if len(pair) != 2:
            raise ValueError("المخرَجُ زوجٌ: عضوٌ وتصنيفُه")
        normalized_outputs.append([str(pair[0]), str(pair[1])])
    normalized_residuals = []
    for residual in residuals:
        normalized_residuals.append(
            {
                "member_id": str(residual["member_id"]),
                "residual_code": str(residual["residual_code"]),
                "blocking": bool(residual["blocking"]),
                "reason": str(residual["reason"]),
                "evidence_ref": str(residual["evidence_ref"]),
            }
        )
    return {
        "protocol": RUNNER_WIRE_PROTOCOL,
        "outputs": normalized_outputs,
        "residuals": normalized_residuals,
    }


def main(argv: list[str]) -> int:
    """استورد وحدةَ القارئ المنسوخة، سلِّمها البايتات، وانقل ناتجَها قانونيًّا."""

    workspace = os.path.dirname(os.path.abspath(__file__))
    if workspace not in sys.path:
        sys.path.insert(0, workspace)
    module_name = argv[1]
    entrypoint_name = argv[2]
    payload_bytes = sys.stdin.buffer.read()
    module = importlib.import_module(module_name)
    entrypoint = getattr(module, entrypoint_name, None)
    if entrypoint is None:
        sys.stderr.write(f"no entrypoint named {entrypoint_name}\n")
        return EXIT_UNUSABLE_RESULT
    try:
        result = entrypoint(payload_bytes)
    except Exception as error:  # noqa: BLE001 - الفشلُ يُنقَل ولا يُطوى
        sys.stderr.write(f"{type(error).__name__}: {error}\n")
        return EXIT_READER_RAISED
    try:
        encoded = json.dumps(
            normalized_result(result),
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
