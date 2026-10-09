"""شهاداتُ المصحف كلِّه **بسياقها** خاناتٍ وأعدادًا — المودَعُ الثاني الذي يستهلكه SLGE
(`tests/data/context-certificates.json.gz`).

`python tools/gen_context_certificates.py OUT.json.gz` يمرّر كلَّ موقعٍ من المدوّنة المختومة على
`gate.enter` **في سياقه** بترتيب المصحف: الآيةُ سطرٌ، أوّلُ كلمةٍ فيها ابتداءٌ (`entry="start"`) وما
بعدها موصولٌ بما قبله (`entry="joined"`، `left` = الكلمةُ السابقة بصورتها القانونيّة)، وآخرُها وقفٌ
(`exit="pause"`) وما سواه استمرار. القاموسُ لكلّ سياقٍ (كلمةٌ يساريّة، حدٌّ) مبنيٌّ على ما وقع بعد تلك
الكلمة في المدوّنة (`Gate(context, domain=…)`؛ كما يفعل `gate.audit`) — مجالٌ مسمًّى ببصمته لا مخمَّن.

المخرَج: الصورَ المتمايزة **في سياقها** (خاناتُ الشهادة كما رخّصها الحدّ: همزةُ الوصل ساقطةٌ بعد كلمة،
والآخرُ ساكنٌ وقفًا، وعرضُ عدد ذرّاتها)، وطولَ كلّ سطر، والتيارَ لكلّ موقع: (رقمُ الصورة أو −1، الحدُّ
0 استمرار / 1 وقف، رقمُ الرفض المسمّى أو −1، رقمُ وجه الوصل في آخر الكلمة اليساريّة أو −1 —
`A116.Iltiqa`: الألفُ الفارقة تسقط / المدُّ يُحذف / الساكنُ يُكسَر). ترتيبُ المواقع هو ترتيبُ
`corpus-certificates.json.gz` نفسُه (78,245 موقعًا) فيُقرأ الموقعُ هناك ابتداءً وهنا في سياقه. لا نصَّ في
المخرَج: خاناتٌ وأعداد.

`--check DEPOSIT.json.gz` يعيد التوليدَ ويقارنه بالمودَع قيمةً قيمة؛ أيُّ فرقٍ يُسقط البناءَ باسم
`DEPOSIT_DRIFTED_FROM_GATE` مع أوّل موضعٍ مختلف.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from gate import Refusal, gate
from gate.api import CORPUS_SHA256, Gate
from gate.bridge import PROTOCOL_VERSION
from gate.contextual import Context, fold_atoms
from gate.licence import REPAIRS
from gate.residue import repair

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
STATE = {"َ": "فتح", "ِ": "كسر", "ُ": "ضم", "ْ": "سكون"}
EXITS = ("continue", "pause")
POLICY = {
    "line": "الآيةُ سطرٌ واحد: أوّلُها ابتداءٌ وآخرُها وقف؛ وما بينهما وصلٌ واستمرار",
    "entry": "الموقعُ الأوّل start؛ وما بعده joined وleft الكلمةُ السابقةُ بصورتها القانونيّة",
    "exit": "الموقعُ الأخير pause؛ وما سواه continue",
    "domain": "قاموسُ كلّ سياقٍ (left, exit) على ما وقع بعد left في المدوّنة بذلك الحدّ",
}


def cells_of(atoms: tuple[str, ...]) -> list[list[str]]:
    """ذرّاتُ الشهادة ← خانات SLGE (حامل، حالة) — مرآةُ `slge.entry.from_atoms` بلا استيراد."""

    return [[a[0], STATE[a[1]]] for a in atoms]


def lines_of(raw: bytes) -> list[list[str]]:
    return [[w for w in line.split() if w != "<sel>"] for line in raw.decode("utf-8").splitlines()]


def gates_for(lines: list[list[str]]) -> dict[tuple[str, str], Gate]:
    """بوّابةٌ لكلّ سياقٍ موصول (الكلمةُ اليساريّة القانونيّة، الحدّ) على مجالها المشهود."""

    domains: dict[tuple[str, str], set[str]] = defaultdict(set)
    for tokens in lines:
        for i in range(1, len(tokens)):
            exit_ = EXITS[i == len(tokens) - 1]
            domains[(repair(tokens[i - 1])[0], exit_)].add(repair(tokens[i])[0])
    return {
        (left, exit_): Gate(Context(entry="joined", exit=exit_, left=left), domain=domain)
        for (left, exit_), domain in sorted(domains.items())
    }


def generate() -> dict[str, Any]:
    raw = CORPUS.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CORPUS_SHA256
    lines = lines_of(raw)
    joined = gates_for(lines)
    start = {"continue": gate(), "pause": Gate(Context(exit="pause"))}
    forms: list[dict[str, Any]] = []
    form_index: dict[tuple[str, ...], int] = {}
    refusals: list[str] = []
    refusal_index: dict[str, int] = {}
    counts: Counter[str] = Counter()
    status: Counter[str] = Counter()
    junctions: Counter[str] = Counter()
    stream: list[list[int]] = []
    for tokens in lines:
        for i, w in enumerate(tokens):
            exit_ = EXITS[i == len(tokens) - 1]
            g = start[exit_] if i == 0 else joined[(repair(tokens[i - 1])[0], exit_)]
            cert = g.enter(w.encode("utf-8"))
            if isinstance(cert, Refusal):
                name = f"{cert.status}:{','.join(cert.reasons)}"
                if name not in refusal_index:
                    refusal_index[name] = len(refusals)
                    refusals.append(name)
                counts[name] += 1
                status[cert.status] += 1
                stream.append([-1, EXITS.index(exit_), refusal_index[name], -1])
                continue
            status["READY"] += 1
            if cert.atoms not in form_index:
                form_index[cert.atoms] = len(forms)
                forms.append({
                    "cells": cells_of(cert.atoms),
                    "atoms_number_bits": fold_atoms(cert.atoms).bit_length(),
                })
            j = REPAIRS.index(cert.junction) if cert.junction else -1
            if cert.junction:
                junctions[cert.junction] += 1
            stream.append([form_index[cert.atoms], EXITS.index(exit_), -1, j])
    return {
        "version": 1,
        "source": "gate.enter في سياق كلّ موقع على المدوّنة المختومة؛ لا نصَّ هنا: خاناتٌ وأعداد",
        "corpus_sha256": CORPUS_SHA256,
        "bridge_protocol": PROTOCOL_VERSION,
        "boundary_policy": POLICY,
        "lines": len(lines),
        "tokens": len(stream),
        "codebooks": len(joined) + len(start),
        "status": dict(sorted(status.items())),
        "refusals": refusals,
        "refusal_counts": {k: counts[k] for k in refusals},
        "junctions": list(REPAIRS),
        "junction_counts": {k: junctions[k] for k in REPAIRS},
        "line_lengths": [len(t) for t in lines],
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
        if k in ("forms", "stream", "line_lengths"):
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
        sys.stdout.write(f"المودَعُ بسياقه هو ما تطبعه البوّابة: {canonical_sha(fresh)} "
                         f"({len(fresh['forms']):,} صورة في سياقها، {fresh['tokens']:,} موقعًا، "
                         f"{fresh['status'].get('READY', 0):,} جاهزًا)\n")
        return 0
    if len(argv) != 2:
        sys.stderr.write("gen_context_certificates.py OUT.json.gz | --check DEPOSIT.json.gz\n")
        return 2
    fresh = generate()
    with gzip.open(argv[1], "wt", encoding="utf-8") as f:
        json.dump(fresh, f, ensure_ascii=False)
    sys.stdout.write(f"كُتب {argv[1]}: {canonical_sha(fresh)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
