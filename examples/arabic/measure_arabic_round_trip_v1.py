"""اطبع جدولَ `ArabicRoundTripV1` على بايتاتٍ عربيّةٍ خام، طبقةً طبقة.

هذا المثالُ مرجعٌ لا جزءٌ من النواة: لا يُولّد كائنًا، ولا يرخّص انتقالًا، ولا
يُصدر شهادة. يأخذ بايتاتٍ ويطبع ما فعله الخطُّ بها:

```
raw bytes → UTF-8 → NFC → carrier/state → syllable → word structure
          → reverse → desegment → retrieve → raw bytes
```

بلا مسارٍ يعمل على الحالات المُضمَّنة في `carrier_state_candidate`:

    python examples/arabic/measure_arabic_round_trip_v1.py

وبمسارِ ملفٍّ نصّيٍّ يُقاس على كلماته بعد تقسيمها على البياض:

    python examples/arabic/measure_arabic_round_trip_v1.py path/to/file.txt

ويُطبع جدولان لا يُدمجان: الأوّلُ على البايتات كما وردت، والثاني على البايتات
بعد تسويةِ `NFC` قبل الخطّ. والثاني ليس تصحيحًا للأوّل بل قياسٌ لمدخلٍ آخر،
فمن قرأهما رقمًا واحدًا خلط مُدخلين.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

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


def _read_tokens(path: Path | None) -> tuple[bytes, ...]:
    if path is None:
        return tuple(case.encode("utf-8") for case in EMBEDDED_ROUND_TRIP_CASES)
    return tokens_from_text(path.read_text(encoding="utf-8"))


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


def _report(title: str, table: RoundTripTable) -> None:
    print(title)
    print(render_table(table))
    halted: dict[str, int] = {}
    for trace in table.traces:
        if trace.outcome is LayerOutcome.RECONSTRUCTED:
            continue
        key = f"{trace.reached.value}/{trace.outcome.value}"
        if trace.refusal is not None:
            key = f"{key}/{trace.refusal.value}"
        halted[key] = halted.get(key, 0) + 1
    for key in sorted(halted):
        print(f"  {key}: {halted[key]}")
    print(
        f"  end-to-end reconstructed: {table.end_to_end_reconstructed}"
        f"/{table.token_total}"
    )
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="ملفٌّ نصّيٌّ يُقسَّم على البياض؛ وبلا مسارٍ تُقاس الحالاتُ المُضمَّنة",
    )
    args = parser.parse_args(argv)

    tokens = _read_tokens(args.path)
    if not tokens:
        print("لا كلمةَ واحدةَ في المدخل، فلا جدولَ يُطبع.", file=sys.stderr)
        return 1

    _report("raw bytes as they arrived", measure_round_trip(tokens))
    _report(
        "the same bytes, NFC before the pipeline",
        measure_round_trip(_normalised(tokens)),
    )

    print("declared functions, layer by layer:")
    for functions in LAYER_FUNCTIONS:
        print(f"  {functions.layer.value}: {functions.forward} ↔ {functions.inverse}")
    print()
    print("not in this pipeline:")
    for absent in LAYERS_NOT_IN_THIS_PIPELINE:
        print(f"  - {absent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
