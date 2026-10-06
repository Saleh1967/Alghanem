"""فهرسُ البتّات على درجات الترخيص التدريجيّ (BITS_INDEX.md): شهاداتُ المدوّنة المختومة درجةً درجةً بالعدد.

المودَع `tests/data/corpus-certificates.json.gz` أصدرته بوّابةُ الغانم على المدوّنة المختومة (بصمتُها
فيه): خاناتُ كلّ صورةٍ مشهودة، وأعدادُ شهادتها (طولُ عددها بالبتّات، طولُ عدد ذرّاتها قبل الاقتران، بتّاتُ
الرتبة، حجمُ الليف، قيودُ البقيّة)، وتيارُ المصحف أرقامَ صورٍ بترتيبه، وعدُّ الرفض بأسمائه — لا نصَّ فيه.
كلُّ رقمٍ هنا يُحسَب الآن من المودَع ويُقابَل بالحدّ الذي يبرهنه Lean باسمه.
"""

from __future__ import annotations

import gzip
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.cells import count, fold, licensed, unfold
from slge.entry import from_atoms, to_atoms
from slge.grant import climb
from slge.stream import cost, decode, decode_word, encode, encode_word, width

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "BITS_INDEX.md"
DATA = ROOT / "tests" / "data" / "corpus-certificates.json.gz"
Word = tuple[tuple[str, str], ...]
SAMPLE = 3000  # التيارُ المتّصل يُفكّ على عيّنةٍ: مرآةُ `decode` تنسخ البقيّةَ كلَّ كلمة (O(n²))


def deposit() -> dict[str, Any]:
    with gzip.open(DATA, "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return d


def measure() -> dict[str, Any]:
    d = deposit()
    forms: list[Word] = [tuple((a, b) for a, b in f["cells"]) for f in d["forms"]]
    stream_idx: list[int] = d["stream"]
    # د٣ الخانة: الخاناتُ ذرّاتٌ بعينها
    atoms_ok = sum(from_atoms(to_atoms(w)) == w for w in forms)
    cells_n = sum(len(w) for w in forms)
    # د٤ الترخيص الثنائيّ (الثلاثيُّ حكمُ البوّابة: كلُّ مودَعٍ مرخَّصٌ ثلاثيًّا بشهادته)
    bin_ok = [w for w in forms if licensed(w)]
    tern_only = len(forms) - len(bin_ok)
    # د٦ الطيّ
    fold_bits = fold_lt = roundtrip = 0
    bound = 0
    for w in bin_ok:
        z = fold(w)
        fold_bits += z.bit_length()
        fold_lt += z < count(len(w))
        roundtrip += tuple(unfold(len(w), z)) == w
        bound += width(len(w))
    # الشهادة: عددُها (اقترانُ كانتور) وعددُ ذرّاتها قبل الاقتران
    cert_bits = sum(f["integer_bits"] for f in d["forms"])
    atoms_number_bits = sum(f["atoms_number_bits"] for f in d["forms"])
    residual_bits = sum(f["residual_bits"] for f in d["forms"])
    fibers_gt1 = sum(f["fiber_size"] > 1 for f in d["forms"])
    residue_edits = sum(f["residue_edits"] for f in d["forms"])
    log116 = round(cells_n * math.log2(116))
    # د١٢ التسلسل على المصحف كلِّه بترتيبه
    stream = [forms[i] for i in stream_idx if i >= 0 and licensed(forms[i])]
    bits = encode(stream)
    cost_sum = sum(cost(len(w)) for w in stream)
    per_word = sum(decode_word(encode_word(w)) == (w, []) for w in stream)
    sample_ok = decode(encode(stream[:SAMPLE])) == stream[:SAMPLE]
    # د١٣ المنح
    granted = sum(len(climb(w)) for w in forms)
    return {
        "forms": len(forms), "tokens": d["tokens"],
        "certified_tokens": sum(i >= 0 for i in stream_idx),
        "refusals": d["refusals"], "codebook_bytes": d["codebook_serialized_bytes"],
        "corpus_sha256": d["corpus_sha256"], "protocol": d["bridge_protocol"],
        "cells": cells_n, "atoms_ok": atoms_ok, "log116": log116,
        "binary": len(bin_ok), "ternary_only": tern_only,
        "fold_bits": fold_bits, "fold_lt": fold_lt, "fold_roundtrip": roundtrip,
        "fold_bound": bound, "cert_bits": cert_bits, "atoms_number_bits": atoms_number_bits,
        "residual_bits": residual_bits, "fibers_gt1": fibers_gt1, "residue_edits": residue_edits,
        "stream_words": len(stream), "stream_bits": len(bits), "cost_sum": cost_sum,
        "per_word": per_word, "sample_ok": sample_ok, "granted": granted,
        "widths": Counter(len(w) for w in stream),
    }


def render() -> str:
    m = measure()
    # بتّاتُ UTF-8 لكلمات التيار نفسها: قيست في الغانم (خارجَ الشجرة) لا هنا — لا نصَّ هنا
    utf8 = "9,708,256"
    lines = [
        "# فهرسُ البتّات على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_bits_index.py` من `tests/data/corpus-certificates.json.gz`؛ "
        "لا يُحرَّر "
        "باليد. المودَعُ أصدرته بوّابةُ الغانم على المدوّنة المختومة "
        f"(`{m['corpus_sha256'][:16]}…`، بروتوكول `{m['protocol']}`): خاناتٌ وأعدادٌ لا نصّ.",
        "",
        "## المدخل", "",
        f"{m['tokens']:,} كلمةً في المصحف؛ شهاداتٌ {m['certified_tokens']:,} كلمةً على "
        f"{m['forms']:,} صورةً "
        "متميّزة؛ والرفضُ بالاسم: "
        + "، ".join(f"`{k}` {v}" for k, v in m["refusals"].items())
        + f". القاموسُ المختوم {m['codebook_bytes']:,} بايتًا (يُذكر على حدة: ليس ضغطًا حرًّا).",
        "",
        "## د٣ الخانة", "",
        f"{m['cells']:,} خانةً ({m['cells'] / m['forms']:.2f} للصورة)؛ `from_atoms∘to_atoms = "
        f"id` على "
        f"{m['atoms_ok']:,}/{m['forms']:,} — البرهان `Slge.ofCell_toCell_on`/`toCell_ofCell_on`. "
        f"الحدُّ النظريّ بلا ترخيص: log₂116 × الخانات = {m['log116']:,} بتًّا.",
        "",
        "## د٤ الترخيص", "",
        f"مرخَّصةٌ ثنائيًّا {m['binary']:,}؛ ثلاثيًّا فقط {m['ternary_only']} (مدٌّ ثمّ مشدَّد: "
        f"عددُها في "
        "شهادتها لا هنا) — `Slge.licensed_iff`، `Ternary.binary_is_blind_to_madd`.",
        "",
        "## د٦ الطيّ", "",
        f"`fold < U(n)` على {m['fold_lt']:,}/{m['binary']:,} (`Slge.slgeFold_lt`)؛ `unfold∘fold "
        f"= id` على "
        f"{m['fold_roundtrip']:,}/{m['binary']:,} (`Slge.slgeUnfold_slgeFold`). مجموعُ بتّات الطيّ "
        f"**{m['fold_bits']:,}** ≤ Σ width(n) = {m['fold_bound']:,} "
        f"(`Sequence.U_lt_two_pow_width`).",
        "",
        "## الشهادة (في الغانم) مقابلَ الطيّ", "",
        f"Σ bit_length(`Certificate.integer`) = **{m['cert_bits']:,}** "
        f"({m['cert_bits'] / m['forms']:.1f} "
        f"للصورة)؛ وعددُ الذرّات قبل اقتران كانتور Σ = {m['atoms_number_bits']:,}؛ بتّاتُ الرتبة "
        f"في الليف "
        f"{m['residual_bits']} (الألياف التي حجمُها > 1: {m['fibers_gt1']})؛ قيودُ البقيّة "
        f"{m['residue_edits']:,}. فالاقترانُ `pair(fold_atoms, rank)` يضاعف الطولَ تقريبًا "
        f"({m['cert_bits'] / m['atoms_number_bits']:.2f}×) ليحمل {m['residual_bits']} بتًّا من "
        f"الرتبة — "
        "مقيس؛ وتغييرُه قرارُ برهانٍ (`A116.Numbering`) لا شيفرة.",
        "",
        "## د١٢ التسلسل", "",
        f"المصحفُ كلُّه تيارًا واحدًا بترتيبه: {m['stream_words']:,} كلمةً مرخَّصةً ثنائيًّا ← "
        f"**{m['stream_bits']:,} بتًّا** = Σ cost(k) "
        f"{'✓' if m['stream_bits'] == m['cost_sum'] else '✗'} "
        f"({m['stream_bits'] / m['stream_words']:.2f} بتًّا للكلمة؛ مقابل UTF-8 {utf8} بتًّا "
        f"للكلمات نفسها "
        f"= {m['stream_bits'] / 9708256:.3f}). `decodeWord∘encodeWord = id` على "
        f"{m['per_word']:,}/{m['stream_words']:,} (`Sequence.decodeWord_encodeWord`)؛ والتيارُ "
        f"المتّصل يعود "
        f"على أوّل {SAMPLE:,} كلمة {'✓' if m['sample_ok'] else '✗'} (`Sequence.decode_encode`، "
        "`encodeWord_prefix_free`). نقلٌ لا بنك: بلا قاموس.",
        "",
        "| طولُ الكلمة k | كلمات | cost(k) |", "|---|---|---|",
        *[f"| {k} | {v:,} | {cost(k)} |" for k, v in sorted(m["widths"].items())],
        "",
        "## د١٣ المنح", "",
        f"مرسومٌ {m['granted']:,} = المرخَّصةُ ثنائيًّا بالضبط (`Slge.Grant.mursam_sound`)؛ "
        f"ولا منحَ للثلاثيّ فقط {m['ternary_only']}.",
        "",
        "## ما ليس هنا — باسمه", "",
        "- بتّاتُ UTF-8 تُقاس في الغانم (النصُّ هناك)؛ هنا رقمُها مودَعٌ ثابتًا لا محسوبًا.",
        "- مرآةُ `stream.decode` تنسخ البقيّةَ كلَّ كلمة (O(n²)): مطابقةٌ لِـLean لا محرّك، "
        "فالتيارُ المتّصل على عيّنة.",
        "- القرّاءُ (د١٤–١٨) على صور المصحف بسوابقها ولواحقها خارجَ هذا الفهرس: فصلُ الزوائد "
        "درجةٌ لا توجد بعد.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("BITS_INDEX.md غيرُ مطابق؛ شغّل tools/gen_bits_index.py\n")
            return 1
        sys.stdout.write("BITS_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب BITS_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
