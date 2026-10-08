"""شهاداتُ المصحف كلِّه خاناتٍ وأعدادًا — المودَعُ الذي يستهلكه SLGE
(`tests/data/corpus-certificates.json.gz`).

`python tools/gen_certificates.py OUT.json.gz` يمرّر كلَّ كلمةٍ من المدوّنة المختومة على `gate.enter`
بترتيب المصحف ويكتب: الصورَ المتمايزة (خاناتُ الشهادة، عرضُ عددها، عرضُ عدد ذرّاتها، بتّاتُ الرتبة، حجمُ
الليف، عددُ قيود البقيّة)، والتيارَ (رقمُ الصورة لكلّ موقع، و−1 للمرفوض)، والرفضَ بالاسم عدًّا على المواقع.
لا نصَّ في المخرَج: خاناتٌ وأعداد.

`--check DEPOSIT.json.gz` يعيد التوليدَ ويقارنه بالمودَع قيمةً قيمة؛ أيُّ فرقٍ يُسقط البناءَ باسم
`DEPOSIT_DRIFTED_FROM_GATE` مع أوّل موضعٍ مختلف. هذه خياطةُ الطبقتين بالشيفرة: ما يقيسه SLGE هو ما
تطبعه هذه البوّابةُ على هذه المدوّنة بهذا الإيداع، لا نسخةٌ قديمة.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from gate import Refusal, enter, gate
from gate.api import CORPUS_SHA256
from gate.bridge import PROTOCOL_VERSION
from gate.contextual import fold_atoms

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
STATE = {"َ": "فتح", "ِ": "كسر", "ُ": "ضم", "ْ": "سكون"}


def cells_of(atoms: tuple[str, ...]) -> list[list[str]]:
    """ذرّاتُ الشهادة ← خانات SLGE (حامل، حالة) — مرآةُ `slge.entry.from_atoms` بلا استيراد."""

    return [[a[0], STATE[a[1]]] for a in atoms]


def generate() -> dict[str, Any]:
    raw = CORPUS.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CORPUS_SHA256
    forms: list[dict[str, Any]] = []
    index: dict[str, int] = {}
    stream: list[int] = []
    refusals: Counter[str] = Counter()  # عدًّا على المواقع لا على الصور
    refused: dict[str, str] = {}
    for line in raw.decode("utf-8").splitlines():
        for w in line.split():
            if w == "<sel>":
                continue
            if w in index:
                stream.append(index[w])
                if index[w] == -1:
                    refusals[refused[w]] += 1
                continue
            cert = enter(w.encode("utf-8"))
            if isinstance(cert, Refusal):
                refused[w] = f"{cert.status}:{cert.reasons[0] if cert.reasons else ''}"
                refusals[refused[w]] += 1
                index[w] = -1
                stream.append(-1)
                continue
            index[w] = len(forms)
            stream.append(len(forms))
            forms.append({
                "cells": cells_of(cert.atoms),
                "integer_bits": cert.integer.bit_length(),
                "atoms_number_bits": fold_atoms(cert.atoms).bit_length(),
                "residual_bits": cert.core.residual_bits,
                "fiber_size": cert.core.fiber_size,
                "residue_edits": len(cert.residue),
            })
    book = gate().book
    return {
        "version": 1,
        "source": "gate.enter على المدوّنة المختومة؛ لا نصَّ هنا: خاناتٌ وأعداد",
        "corpus_sha256": CORPUS_SHA256,
        "bridge_protocol": PROTOCOL_VERSION,
        "codebook_digest": book.digest,
        "codebook_serialized_bytes": book.serialized_bytes,
        "tokens": len(stream),
        "refusals": dict(refusals),
        "forms": forms,
        "stream": stream,
    }


def canonical_sha(d: dict[str, Any]) -> str:
    blob = json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def drift(fresh: dict[str, Any], deposit: dict[str, Any]) -> str | None:
    """أوّلُ فرقٍ باسمه، أو لا شيء."""

    for k in sorted(set(fresh) | set(deposit)):
        if k not in fresh or k not in deposit:
            return f"المفتاح {k} في أحدهما فقط"
        if k in ("forms", "stream"):
            a, b = fresh[k], deposit[k]
            if len(a) != len(b):
                return f"{k}: الطولُ {len(a)} في البوّابة و{len(b)} في المودَع"
            for i, (x, y) in enumerate(zip(a, b, strict=True)):
                if x != y:
                    return f"{k}[{i}]: {x} في البوّابة و{y} في المودَع"
        elif fresh[k] != deposit[k]:
            return f"{k}: {fresh[k]} في البوّابة و{deposit[k]} في المودَع"
    return None


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[1] == "--check":
        with gzip.open(argv[2], "rt", encoding="utf-8") as f:
            deposit = json.load(f)
        fresh = generate()
        d = drift(fresh, deposit)
        if d:
            sys.stderr.write(f"DEPOSIT_DRIFTED_FROM_GATE: {d}\n")
            return 1
        sys.stdout.write(f"المودَعُ هو ما تطبعه البوّابة: {canonical_sha(fresh)} "
                         f"({len(fresh['forms']):,} صورة، {fresh['tokens']:,} موقعًا)\n")
        return 0
    if len(argv) != 2:
        sys.stderr.write("gen_certificates.py OUT.json.gz | --check DEPOSIT.json.gz\n")
        return 2
    fresh = generate()
    with gzip.open(argv[1], "wt", encoding="utf-8") as f:
        json.dump(fresh, f, ensure_ascii=False)
    sys.stdout.write(f"كُتب {argv[1]}: {canonical_sha(fresh)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
