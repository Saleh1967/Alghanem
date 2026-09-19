"""اطبع جدولَ `ArabicRoundTripV1` على بايتاتٍ عربيّةٍ خام، طبقةً طبقة.

هذا المثالُ مرجعٌ لا جزءٌ من النواة: لا يُولّد كائنًا، ولا يرخّص انتقالًا، ولا
يُصدر شهادة. يأخذ بايتاتٍ ويطبع ما فعله الخطُّ بها:

```
raw bytes → UTF-8 → NFC → carrier/state → syllable → word structure
          → reverse → desegment → retrieve → raw bytes
```

ثلاثةُ أوجهٍ للتشغيل، ولا يُدمَج مخرجُ أحدها في الآخر:

* على الحالات المُضمَّنة في `carrier_state_candidate`، وهي حالاتُ اختبارٍ لا
  مدوّنة::

      python examples/arabic/measure_arabic_round_trip_v1.py

* على إيداع الفاتحة المُبصَّم في الشجرة، فيُعاد اشتقاقُ `FATIHA_ROUND_TRIP`
  بأعداده وببصمة جدوله، ويفشل التشغيلُ إن انحرف::

      python examples/arabic/measure_arabic_round_trip_v1.py --deposit

* على ملفٍّ نصّيٍّ خارجيٍّ يُقسَّم على البياض، ولا يُجمَّد لمخرجه رقمٌ في
  الشجرة ما دامت بايتاتُه خارجَها::

      python examples/arabic/measure_arabic_round_trip_v1.py path/to/file.txt

ومع المدخلِ غيرِ المُجمَّد يُطبع جدولان لا يُدمجان: الأوّلُ على البايتات كما
وردت، والثاني على البايتات بعد تسويةِ `NFC` قبل الخطّ. والثاني ليس تصحيحًا
للأوّل بل قياسٌ لمدخلٍ آخر، فمن قرأهما رقمًا واحدًا خلط مُدخلين.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import unicodedata
from pathlib import Path
from typing import Final

from alghanem.arabic.arabic_round_trip_corpus import (
    FATIHA_ROUND_TRIP,
    UNMEASURED_ROUND_TRIP_SOURCES,
    measure_deposited_text,
)
from alghanem.arabic.arabic_round_trip_v1 import (
    LAYER_FUNCTIONS,
    LAYERS_NOT_IN_THIS_PIPELINE,
    LayerOutcome,
    RoundTripTable,
    measure_round_trip,
    render_table,
    tokens_from_text,
)
from alghanem.arabic.encoding.carrier_state_candidate import EMBEDDED_ROUND_TRIP_CASES
from alghanem.arabic.fatiha_source_text import (
    FATIHA_SOURCE_ID,
    FATIHA_SOURCE_TEXT,
    source_byte_length,
    source_sha256,
)


def _normalised(tokens: tuple[bytes, ...]) -> tuple[bytes, ...]:
    normalised: list[bytes] = []
    for token in tokens:
        try:
            text = token.decode("utf-8")
        except UnicodeDecodeError:
            normalised.append(token)
            continue
        normalised.append(unicodedata.normalize("NFC", text).encode("utf-8"))
    return tuple(normalised)


_EXAMPLES_PER_CLASS: Final[int] = 5


def _class_examples(
    table: RoundTripTable, tokens: tuple[bytes, ...]
) -> dict[tuple[str, str, str], list[str]]:
    """اجمع أمثلةَ كلِّ صنفِ رفضٍ أو اختلافٍ بعينها؛ فالعددُ وحدَه لا يُفحَص."""

    examples: dict[tuple[str, str, str], list[str]] = {}
    for trace in table.traces:
        if trace.outcome is LayerOutcome.RECONSTRUCTED:
            continue
        reason = "—" if trace.refusal is None else trace.refusal.value
        key = (trace.reached.value, trace.outcome.value, reason)
        bucket = examples.setdefault(key, [])
        if len(bucket) >= _EXAMPLES_PER_CLASS:
            continue
        if trace.token_index >= len(tokens):  # pragma: no cover - defensive
            continue
        bucket.append(tokens[trace.token_index].decode("utf-8", errors="replace"))
    return examples


def _report(title: str, table: RoundTripTable, tokens: tuple[bytes, ...] = ()) -> None:
    print(title)
    print(render_table(table))
    for halt in table.halt_profile:
        reason = "" if halt.refusal is None else f"/{halt.refusal.value}"
        print(f"  {halt.layer.value}/{halt.outcome.value}{reason}: {halt.count}")
    if tokens:
        examples = _class_examples(table, tokens)
        if examples:
            print("  examples of each halting class, not counts alone:")
            for layer, outcome, reason in sorted(examples):
                shown = " ".join(examples[(layer, outcome, reason)])
                print(f"    {layer}/{outcome}/{reason}: {shown}")
    print(
        f"  end-to-end reconstructed: {table.end_to_end_reconstructed}"
        f"/{table.token_total}"
    )
    print(f"  table digest: {table.digest}")
    print()


def _declared_functions() -> None:
    print("declared functions, layer by layer:")
    for functions in LAYER_FUNCTIONS:
        print(f"  {functions.layer.value}: {functions.forward} ↔ {functions.inverse}")
    print()
    print("not in this pipeline:")
    for absent in LAYERS_NOT_IN_THIS_PIPELINE:
        print(f"  - {absent}")


def _run_deposit() -> int:
    """أعِد اشتقاقَ القياس المُجمَّد على إيداع الفاتحة، وافشل عند أيّ انحراف."""

    measurement = measure_deposited_text(
        FATIHA_SOURCE_TEXT,
        source_id=FATIHA_SOURCE_ID,
        source_sha256=source_sha256(),
        source_byte_length=source_byte_length(),
    )
    _report(
        f"deposited text: {measurement.source_id} "
        f"sha256={measurement.source_sha256} bytes={measurement.source_byte_length}",
        measure_round_trip(tokens_from_text(FATIHA_SOURCE_TEXT)),
    )
    rate = measurement.reconstruction_rate
    rendered = "—" if rate is None else f"{rate:.6f}"
    print(
        f"  reconstruction over everything that entered: "
        f"{measurement.end_to_end_reconstructed}/{measurement.token_total} = {rendered}"
    )
    if not measurement.agrees_in_figures_with(FATIHA_ROUND_TRIP):
        print(
            "error: the re-derived figures do not match the frozen "
            f"FATIHA_ROUND_TRIP figures digest {FATIHA_ROUND_TRIP.figures_digest}",
            file=sys.stderr,
        )
        return 1
    print(
        f"  matches the frozen FATIHA_ROUND_TRIP figures {measurement.figures_digest}"
    )
    if measurement.ran_in_the_same_environment_as(FATIHA_ROUND_TRIP):
        print(f"  same environment, so the full digest holds too: {measurement.digest}")
    else:
        print(
            "  a different environment ran it — "
            f"unicode database {measurement.unicode_database_version} against the "
            f"frozen {FATIHA_ROUND_TRIP.unicode_database_version} — so the full "
            f"digest reads {measurement.digest}; the figures are unchanged, which "
            "is a result, not a drift"
        )
    return 0


def _run_external(path: Path) -> int:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    print(f"external file: {path} sha256={digest} bytes={len(raw)}")
    for source in UNMEASURED_ROUND_TRIP_SOURCES:
        if digest == source.source_sha256:
            print(f"  recognised as: {source.source_id}")
            print(f"  no figure is frozen for it: {source.why_no_figure_is_frozen}")
    print()

    tokens = tokens_from_text(raw.decode("utf-8", errors="replace"))
    if not tokens:
        print("لا كلمةَ واحدةَ في المدخل، فلا جدولَ يُطبع.", file=sys.stderr)
        return 1
    _report("raw bytes as they arrived", measure_round_trip(tokens), tokens)
    normalised = _normalised(tokens)
    _report(
        "the same bytes, NFC before the pipeline",
        measure_round_trip(normalised),
        normalised,
    )
    return 0


def _run_embedded() -> int:
    embedded = tuple(case.encode("utf-8") for case in EMBEDDED_ROUND_TRIP_CASES)
    if not embedded:
        print("لا كلمةَ واحدةَ في المدخل، فلا جدولَ يُطبع.", file=sys.stderr)
        return 1
    _report(
        "embedded test surfaces, not a corpus", measure_round_trip(embedded), embedded
    )
    normalised = _normalised(embedded)
    _report(
        "the same surfaces, NFC before the pipeline",
        measure_round_trip(normalised),
        normalised,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="ملفٌّ نصّيٌّ يُقسَّم على البياض؛ وبلا مسارٍ تُقاس الحالاتُ المُضمَّنة",
    )
    parser.add_argument(
        "--deposit",
        action="store_true",
        help="أعِد اشتقاقَ القياس المُجمَّد على إيداع الفاتحة المُبصَّم في الشجرة",
    )
    args = parser.parse_args(argv)

    if args.deposit and args.path is not None:
        print(
            "error: a deposited measurement and an external file are two "
            "different measurements; run them separately",
            file=sys.stderr,
        )
        return 1

    if args.deposit:
        status = _run_deposit()
    elif args.path is not None:
        status = _run_external(args.path)
    else:
        status = _run_embedded()
    if status != 0:
        return status
    print()
    _declared_functions()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
