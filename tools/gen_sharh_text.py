"""عقدُ الشرح نصًّا: الآياتُ كلُّها كلمةً كلمة، **تخرج كلُّ كلمةٍ بـ`gate.exit`** لا من الملفّ، ومعها
أسطرُ عقد SLGE (الدعوى، القيمة، الوحدة، الوسم، المرساة) — مدخلُ الواجهة البشريّة.

`python tools/gen_sharh_text.py CLAIMS.json.gz OUT.json.gz` يمرّ على المدوّنة المختومة سطرًا سطرًا
(السطرُ آيةٌ برقمه في المدوّنة)، ويمرّر كلَّ كلمةٍ على `gate.enter` ثمّ يُخرجها بـ`gate.exit(cert)`،
ويضع رقمَ صورتها في مودَع الشهادات (بالترتيب نفسِه الذي يطبعه `tools/gen_certificates.py`)؛ وأسطرُ
العقد مأخوذةٌ من مخرَج `tools/gen_sharh_index.py --claims` في SLGE كما هي (أعدادٌ وحواملُ وأسماءٌ من
مفرداتٍ مغلقة، لا نصّ). المرفوضُ يبقى برفضه المسمّى. والمخرَجُ JSON: `ledger` (لكلّ دعوى وسمُها
ومرساتُها ونصُّها من سجلّ SLGE)، و`forms` (أسطرُ كلّ صورة)، و`verses` (لكلّ سطرٍ كلماتُه: نصُّ المخرج
ورقمُ الصورة أو الرفض).

`--check CLAIMS.json.gz` يتحقّق بلا كتابة: بصمةُ المدوّنة في العقد بصمتُها هنا، وعددُ الصور فيه
عددُها هنا، وكلُّ كلمةٍ مقبولة نصُّها المخرَجُ هو كلمةُ المدوّنة بعينها؛ وأيُّ خلافٍ يُسقط البناء
باسمه (`SHARH_CORPUS_MISMATCH`، `SHARH_FORMS_MISMATCH`، `EXIT_IS_NOT_THE_WORD`).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from gate import Refusal, enter, exit  # noqa: A004 - مخرجُ البوّابة باسمه
from gate.api import CORPUS_SHA256

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"


def build(claims: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """الآياتُ كلماتٍ من `gate.exit`، وأسطرُ العقد كما هي؛ وما يُسقط البناء باسمه."""

    raw = CORPUS.read_bytes()
    bad: list[str] = []
    sha = hashlib.sha256(raw).hexdigest()
    if sha != CORPUS_SHA256 or claims.get("corpus_sha256") != sha:
        bad.append("SHARH_CORPUS_MISMATCH")
    index: dict[str, int] = {}
    texts: dict[str, str] = {}
    refused: dict[str, str] = {}
    verses: list[dict[str, Any]] = []
    for n, line in enumerate(raw.decode("utf-8").splitlines(), start=1):
        words: list[list[Any]] = []
        for w in line.split():
            if w == "<sel>":
                continue
            if w not in index and w not in refused:
                cert = enter(w.encode("utf-8"))
                if isinstance(cert, Refusal):
                    refused[w] = f"{cert.status}:{cert.reasons[0] if cert.reasons else ''}"
                else:
                    out = exit(cert).decode("utf-8")  # الكلمةُ تخرج من البوّابة لا من الملفّ
                    if out != w:
                        bad.append(f"EXIT_IS_NOT_THE_WORD {n}")
                    index[w] = len(texts)
                    texts[w] = out
            if w in refused:
                words.append([None, -1, refused[w]])
            else:
                words.append([texts[w], index[w], None])
        verses.append({"line": n, "words": words})
    if len(claims.get("forms", [])) != len(texts):
        bad.append("SHARH_FORMS_MISMATCH")
    return {"corpus_sha256": sha, "ledger": claims.get("ledger", {}),
            "forms": claims.get("forms", []), "verses": verses}, bad


def main() -> int:
    args = sys.argv[1:]
    check = "--check" in args
    args = [a for a in args if a != "--check"]
    with gzip.open(args[0], "rt", encoding="utf-8") as f:
        claims: dict[str, Any] = json.load(f)
    out, bad = build(claims)
    if bad:
        print("\n".join(sorted(set(bad))[:20]))
        return 1
    if check:
        print(f"عقدُ الشرح مطابق: {len(out['verses']):,} سطرًا، {len(out['forms']):,} صورة")
        return 0
    with gzip.open(args[1], "wt", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"كُتب {args[1]}: {len(out['verses']):,} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
