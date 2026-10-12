"""ملءُ العيّنتين بتفويض المالك (ADR ٣٩): الوسمُ على كلّ صفّ، والملءُ متّسق، ورقمُ الاسترجاع يُعاد.

العيّنتان (`corpora/hukm-sample-frame.tsv`، `corpora/hadith/sample-frame.tsv`) ملأهما الوكيل
بتفويض المالك (`corpora/agent-fill.json`) — فهما **ليستا مرجعًا بشريًّا محجوبًا**،
والقياسُ عليهما «مفحوص» لا «مقيس».
ويُفحص هنا: بصمتا الإطارين كما سُجِّلتا، والوسمُ في كلّ صفّ، والجذرُ من الثمانية والعشرين، والقسمةُ تُعيد هيكلَ
الكلمة بعينه؛ ثمّ اتّفاقُ `gate.recover` مع جذور الوكيل على عيّنة الصحيحين يُعاد حسابُه ويطابق المسجَّل.
والطفرات: صفٌّ بلا وسم، وقسمةٌ لا تُعيد الهيكل، وجذرٌ بحرفٍ من خارج الأصول.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from functools import cache
from pathlib import Path

from gate import Refusal, recover
from gate.api import HADITH_CORPUS, Gate

ROOT = Path(__file__).resolve().parents[1]
FILL = ROOT / "corpora" / "agent-fill.json"
HUKM = ROOT / "corpora" / "hukm-sample-frame.tsv"
HADITH = ROOT / "corpora" / "hadith" / "sample-frame.tsv"
RADICALS = set("بتثجحخدذرزسشصضطظعغفقكلمنهويء")  # الحواملُ إلّا الألف — باليد
MARKS = re.compile(r"[ً-ْٰ]")


def _meta() -> dict:  # type: ignore[type-arg]
    return json.loads(FILL.read_text(encoding="utf-8"))


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def _root_ok(root: str) -> bool:
    if root == "-":
        return True
    parts = root.split(" ")
    return len(parts) in (3, 4) and all(len(p) == 1 and p in RADICALS for p in parts)


def _seg_ok(word: str, seg: str) -> bool:
    pre, stem, suf = seg.split("|")
    return bool(stem) and pre + stem + suf == MARKS.sub("", word)


def test_frames_are_the_recorded_bytes() -> None:
    for rel, info in _meta()["frames"].items():
        data = (ROOT / rel).read_bytes()
        assert hashlib.sha256(data).hexdigest() == info["sha256"], rel
        assert len(_rows(ROOT / rel)) == info["rows"]


def test_every_row_carries_the_tag_and_well_formed_values() -> None:
    tag = _meta()["tag"]
    for r in _rows(HUKM):
        assert r["note"].startswith(tag) and _root_ok(r["root"]) and r["jins"], r["id"]
        assert r["qabiliyya"] == "-" or "QABILIYYA_NEEDS_MUKHASSAS_NODE_TEXT" in r["note"]
    for r in _rows(HADITH):
        assert r["note"].startswith(tag) and _root_ok(r["root"]), r["id"]
        assert _seg_ok(r["word"], r["segmentation"]), r["id"]
        assert r["wasl_vowel"] in {"فتحة", "كسرة", "ضمة", "-"}


def test_mutants_are_caught() -> None:
    # MUTANT_UNTAGGED، MUTANT_SEG_LOSES_LETTERS، MUTANT_ROOT_WITH_ALIF
    r = _rows(HADITH)[0]
    assert not "".startswith(_meta()["tag"])
    assert not _seg_ok(r["word"], "و" + r["segmentation"])
    assert not _root_ok("ق ا ل")


@cache
def _recover_check() -> dict[str, int]:
    gate = Gate(corpus=HADITH_CORPUS)
    stat: Counter[str] = Counter()
    for r in _rows(HADITH):
        root = r["root"].replace(" ", "")
        if root == "-":
            stat["no_root"] += 1
            continue
        if isinstance(gate.enter(r["word"].encode()), Refusal):
            stat["refused"] += 1
            continue
        roots = {x[0] for x in recover(r["word"])[1]}
        if not roots:
            stat["no_reading"] += 1
        elif root in roots:
            stat["agree"] += 1
        elif root in {x.replace("ي", "و") for x in roots}:
            stat["disagree_waw_ya"] += 1
        else:
            stat["disagree"] += 1
    return dict(stat)


def test_recover_agreement_is_the_recorded_one() -> None:
    assert _recover_check() == _meta()["hadith_recover_check"]
