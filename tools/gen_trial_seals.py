"""الختمُ التجريبيّ (ADR ٦١، أمرُ المالك 2026-10-14): أربعةُ نصوصٍ من OpenITI مختومةٌ ببصمتها،
**تجريبيّة**.

النصوص: مغني اللبيب لابن هشام، والبرهان في علوم القرآن للزركشي، وإعراب القرآن للنحّاس، والتبيان
للعكبري. كلٌّ منسوخٌ بعينه من مستودع OpenITI بإيداعه المسمّى، ومضغوطٌ بلا طابعٍ زمنيّ في
`corpora/trial/`.

**التجريبيّ** حالٌ لا رخصة:
* يُقاس عليه بتسجيلٍ مسبق.
* لا يُرسي مرساةً، ولا يُبنى عليه حكم، ولا تقرؤه شيفرةٌ في `gate/` (يفحصه `tests/test_trial_seals.py`).
* يُرقّى إلى ختمٍ نهائيّ بتوقيع المالك وحدَه، أو يُعلَّق.

النصوصُ غيرُ مشكولة (نسبةُ علامات التشكيل إلى الحروف صفر في الأربعة)، فلا تمرّ كلماتُها على
البوّابة؛ تُستعمل نصوصَ قواعد وشواهدَ تُستشهد بأسطرها، والآياتُ فيها تُردّ إلى المصحف المختوم بموضعها.

`--check` يُسقط البناءَ بـ`TRIAL_SEAL_BROKEN` (بصمةٌ لا تطابق) أو `TRIAL_SEAL_MISSING` أو
`TRIAL_MANIFEST_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "corpora" / "trial"
MANIFEST = DIR / "MANIFEST.tsv"
STATUS = "تجريبي"
LICENCE = "CC BY-NC-SA 4.0 (OpenITI)"

# (الملفّ، العنوان، مستودعُ OpenITI@الإيداع، sha256 بعد فكّ الضغط، الحجمُ بالبايت)
SEALS: tuple[tuple[str, str, str, str, int], ...] = (
    ("0761JamalDinIbnHisham.MughniLabib.Shamela0006972-ara1", "مغني اللبيب عن كتب الأعاريب",
     "OpenITI/0775AH@61b0c7891699554aeff8dffdb8b1a2a59d2d22ab",
     "f37ac2bb4b273f59169053dd0ac2abf50a52846a7e87ddf689ee5c0b87f77e7d", 1486890),
    ("0794BadrDinZarkashi.BurhanFiCulumQuran.Shamela0011436-ara1", "البرهان في علوم القرآن",
     "OpenITI/0800AH@7b745ec7b83d6d4971f937364dbdec2fe0ba2a40",
     "393283ef77be278ffc2ce35e3a8095205a2ba2567775d7c7a4be5bd26729fa88", 3203468),
    ("0338AbuJacfarNahhas.IcrabQuran.Shamela0023587-ara1", "إعراب القرآن للنحاس",
     "OpenITI/0350AH@3f52b87dc367365000b32f815a3d0077451c46f4",
     "16d81f1f7b2852cc528bf6f9edc5f5f252d78f7c59b59fc18652d117e343a3aa", 4170848),
    ("0616MuhibbDinCukbari.TibyanFiIcrabQuran.Shamela0022928-ara1", "التبيان في إعراب القرآن",
     "OpenITI/0625AH@f1e38210b32fd0d043949ff6471e869d658c3b16",
     "5a6fa8cca71cea3c1592f25e18cb49ab5efe1bbfa56345dfb41f35cafcadbb50", 2535525),
)


def render_manifest() -> str:
    head = "file\ttitle\tsource\tsha256\tbytes\tstatus\tlicence\n"
    return head + "".join(f"{f}.gz\t{t}\t{s}\t{h}\t{n}\t{STATUS}\t{LICENCE}\n"
                          for f, t, s, h, n in SEALS)


def breaches() -> list[str]:
    bad: list[str] = []
    for name, _, _, sha, size in SEALS:
        path = DIR / f"{name}.gz"
        if not path.exists():
            bad.append(f"TRIAL_SEAL_MISSING:{name}")
            continue
        raw = gzip.decompress(path.read_bytes())
        if hashlib.sha256(raw).hexdigest() != sha or len(raw) != size:
            bad.append(f"TRIAL_SEAL_BROKEN:{name}")
    if not MANIFEST.exists() or MANIFEST.read_text(encoding="utf-8") != render_manifest():
        bad.append("TRIAL_MANIFEST_DRIFTED")
    return bad


def main(argv: list[str]) -> int:
    if "--check" not in argv:
        MANIFEST.write_text(render_manifest(), encoding="utf-8")
    bad = breaches()
    if bad:
        sys.stderr.write("\n".join(bad) + "\n")
        return 1
    sys.stdout.write(f"الختمُ التجريبيّ مطابق: {len(SEALS)} نصوص\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
