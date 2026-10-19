"""`G0.EXEC-0.WORKSPACE`: مساحةُ تنفيذٍ مؤقّتةٌ خارج الشجرة، تُكتَب من المقيس.

    MeasuredBytesAreExecutedBytes

لا يُشغَّل مسارُ الملفّ الذي قيس، بل تُكتَب بايتاتُه المقيسةُ نفسُها في مساحةٍ
مؤقّتةٍ خارج المستودع ثمّ تُشغَّل تلك النسخة. فبين القياس والتشغيل لحظةٌ يتغيّر
فيها المصدر، ومن شغّل المسارَ لم يُشغِّل بالضرورة ما قاس.

والمساحةُ لا تحوي إلّا بايتاتِ القارئ المقيسةَ ومُشغِّلًا قائمًا بنفسه، فسبيلُ
الاستيراد في العمليّة المنفصلة هو هذه المساحةُ وحدَها، لا شجرةُ المستودع.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from ..canonical_content import canonical_bytes, canonical_digest
from .envelope import EXECUTION_ENVELOPE_PROTOCOL
from .laws import MEASURED_BYTES_ARE_EXECUTED_BYTES, ExecutionError
from .runner import (
    READER_ENTRYPOINT_NAME,
    READER_ENTRYPOINT_PARAMETERS,
    RUNNER_WIRE_PROTOCOL,
)

__all__ = [
    "EXECUTION_WORKSPACE_PREFIX",
    "RUNNER_FILE_NAME",
    "entry_module_name",
    "execution_entrypoint_digest",
    "materialize_measured_bytes",
    "runner_source_bytes",
]

EXECUTION_WORKSPACE_PREFIX = "alghanem-g0-exec-0-"
"""بادئةُ مساحة التنفيذ المؤقّتة؛ تُنشَأ خارج الشجرة وتُزال بعد التشغيل."""

RUNNER_FILE_NAME = "_alghanem_execution_runner.py"
"""اسمُ المُشغِّل في المساحة؛ مُسمًّى بما لا يتصادم مع وحدةِ قارئ."""

_RUNNER_SOURCE = Path(__file__).resolve().parent / "runner.py"


def runner_source_bytes() -> bytes:
    """بايتاتُ المُشغِّل كما هي؛ تُنسَخ إلى المساحة وتدخل بصمةَ المدخل."""

    return _RUNNER_SOURCE.read_bytes()


def entry_module_name(entry_file_name: str) -> str:
    """اسمُ وحدةِ المدخل في المساحة؛ مُشتَقٌّ من اسم ملفّها لا من دعوى القارئ."""

    if not entry_file_name.endswith(".py"):
        raise ExecutionError("ملفُّ مدخل القارئ وحدةُ بايثون مُسمّاةٌ بامتدادها")
    return entry_file_name[: -len(".py")]


def materialize_measured_bytes(
    root: Path, measured: Mapping[str, bytes], *, entry_displayed_name: str
) -> str:
    """اكتب البايتاتِ المقيسةَ والمُشغِّلَ في المساحة، وأعِد اسمَ وحدةِ المدخل."""

    if not measured:
        raise ExecutionError(MEASURED_BYTES_ARE_EXECUTED_BYTES)
    written: dict[str, str] = {}
    entry_file_name: str | None = None
    for displayed, content in sorted(measured.items()):
        file_name = Path(displayed).name
        if file_name in written:
            raise ExecutionError(
                "ملفّا تنفيذٍ يتصادمان باسمهما في المساحة: "
                + "، ".join(sorted((written[file_name], displayed)))
            )
        written[file_name] = displayed
        (root / file_name).write_bytes(content)
        if displayed == entry_displayed_name:
            entry_file_name = file_name
    if entry_file_name is None:
        raise ExecutionError("ملفُّ المدخل ليس من ملفّات التنفيذ المقيسة")
    if RUNNER_FILE_NAME in written:
        raise ExecutionError("اسمُ المُشغِّل محجوز؛ ولا يُسمّى به ملفُّ قارئ")
    (root / RUNNER_FILE_NAME).write_bytes(runner_source_bytes())
    return entry_module_name(entry_file_name)


def execution_entrypoint_digest(*, contract_interface_version: str) -> str:
    """بصمةُ المدخل: اسمُه وأرقامُه، والواجهةُ، والمُشغِّلُ، والقناةُ، والمغلّف."""

    return canonical_digest(
        canonical_bytes(
            {
                "entrypoint_name": READER_ENTRYPOINT_NAME,
                "entrypoint_parameters": list(READER_ENTRYPOINT_PARAMETERS),
                "contract_interface_version": contract_interface_version,
                "runner_digest": canonical_digest(runner_source_bytes()),
                "wire_protocol": RUNNER_WIRE_PROTOCOL,
                "envelope_protocol": EXECUTION_ENVELOPE_PROTOCOL,
            }
        )
    )
