"""ختمُ «الكتاب» (ADR ٦٨، إذنُ المالك في الجلسة 2026-10-15: «قم بالإيداع»).

ثلاثةُ نصوصٍ من OpenITI مختومةٌ ببصمتها:
* «الكتاب» لسيبويه، نسخة JK006989 — مصدرُ صفوف `A116.Makharij` و`A116.MakharijIdgham` ومراسيها.
* «الكتاب» نسخة Shamela0023018 — شاهدٌ ثانٍ على الباب نفسِه؛ وفيها كذلك سقطُ مخرج اللام.
* «شرح كتاب سيبويه» للسيرافيّ، نسخة Sham19Y0017726 — ينقل نصَّ الباب بعد «قال سيبويه» وفيه
  مخرجُ اللام؛ فهو روايةُ الشارح لمتن الكتاب لا مخطوطٌ للكتاب نفسِه، ويُوسَم كذلك.

كلٌّ منسوخٌ بعينه من مستودع OpenITI بإيداعه المسمّى، ومضغوطٌ بلا طابعٍ زمنيّ (`mtime=0`) في
`corpora/kitab/`. الحالُ «مختوم» بإذن المالك؛ لا تقرؤه شيفرةٌ في `gate/`، ويقرؤه
`tests/test_makharij.py` شاهدًا على صفوف Lean.

`--check` يُسقط البناءَ بـ`KITAB_SEAL_BROKEN` (بصمةٌ أو حجمٌ لا يطابق) أو `KITAB_SEAL_MISSING` أو
`KITAB_MANIFEST_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "corpora" / "kitab"
MANIFEST = DIR / "MANIFEST.tsv"
STATUS = "مختوم"
LICENCE = "CC BY-NC-SA 4.0 (OpenITI)"

# (الملفّ، العنوان، مستودعُ OpenITI@الإيداع، sha256 قبل الضغط، الحجمُ بالبايت)
SEALS: tuple[tuple[str, str, str, str, int], ...] = (
    ("0180Sibawayhi.KitabSibawayhi.JK006989-ara1", "الكتاب لسيبويه (JK006989)",
     "OpenITI/0200AH@599f22fe249871f602efe2e0ddc801d3742960a3",
     "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625", 2639395),
    ("0180Sibawayhi.KitabSibawayhi.Shamela0023018-ara1.mARkdown", "الكتاب لسيبويه (Shamela0023018)",
     "OpenITI/0200AH@599f22fe249871f602efe2e0ddc801d3742960a3",
     "ad676dffaa6df22a7b2ef4c4dbc4424d1e214e09e3f296a538ce887c89affcad", 2692552),
    ("0368AbuSacidSirafi.SharhKitabSibawayhi.Sham19Y0017726-ara1", "شرح كتاب سيبويه للسيرافي",
     "OpenITI/0375AH@ab52219710c6bf15a93d6e39886f0ca602d27952",
     "d53137fd4151028c5dee8ab9ff3e42275ecf0c39089e15fbf50bf0eefaa1603a", 7000693),
)


def render_manifest() -> str:
    head = "file\ttitle\tsource\tsha256\tbytes\tstatus\tlicence\n"
    return head + "".join(f"{f}.gz\t{t}\t{s}\t{h}\t{n}\t{STATUS}\t{LICENCE}\n"
                          for f, t, s, h, n in SEALS)


def text(name: str) -> str:
    """النصُّ المختوم بعينه بعد التحقّق من بصمته؛ يُسقط بـ`KITAB_SEAL_BROKEN` إن لم تطابق."""
    for f, _, _, sha, size in SEALS:
        if f == name:
            raw = gzip.decompress((DIR / f"{f}.gz").read_bytes())
            if hashlib.sha256(raw).hexdigest() != sha or len(raw) != size:
                raise ValueError(f"KITAB_SEAL_BROKEN:{f}")
            return raw.decode("utf-8")
    raise KeyError(name)


def breaches() -> list[str]:
    bad: list[str] = []
    for name, _, _, sha, size in SEALS:
        path = DIR / f"{name}.gz"
        if not path.exists():
            bad.append(f"KITAB_SEAL_MISSING:{name}")
            continue
        raw = gzip.decompress(path.read_bytes())
        if hashlib.sha256(raw).hexdigest() != sha or len(raw) != size:
            bad.append(f"KITAB_SEAL_BROKEN:{name}")
    if not MANIFEST.exists() or MANIFEST.read_text(encoding="utf-8") != render_manifest():
        bad.append("KITAB_MANIFEST_DRIFTED")
    return bad


def main(argv: list[str]) -> int:
    if "--check" not in argv:
        MANIFEST.write_text(render_manifest(), encoding="utf-8")
    bad = breaches()
    if bad:
        sys.stderr.write("\n".join(bad) + "\n")
        return 1
    sys.stdout.write(f"ختمُ الكتاب مطابق: {len(SEALS)} نصوص\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
