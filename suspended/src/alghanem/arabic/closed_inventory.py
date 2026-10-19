"""«الجرد المغلق» مصوغًا قابلًا للكذب: أبنيةُ سيبويه مجمَّدةً قبل الفحص، ثم الفحصُ آليًّا.

الجردُ `corpora/sibawayh-abniya.tsv` استخرجه `tools/sibawayh_abniya_extract.py` من
أبواب الأبنية في نشرتين للكتاب، بقواعدَ معلنةٍ في رأسه وبصمتين مثبَّتتين. والنشرتان
غيرُ مشكولتين في هذه الأبواب، فالجردُ **هياكلُ حروف**؛ وهو متساهلٌ عمدًا (يقبل كلَّ
حرفٍ في خانات ف ع ل، ويقرأ الشدّةَ حرفًا وحرفين)، فالحكمُ القطعيُّ الوحيد عنده
«لا يطابق بناءً»، وأمّا «يطابق» فمعناه «لم يُنقَض بالهيكل» لا «على بنائهم».

* `calibration`: الجردُ على قوائم سيبويه نفسِه في «باب ما أعرب من الأعجمية».
* `masaq_reading`: الجردُ على جذوع الأسماء في MASAQ، وغيرُ المطابق مسمًّى.
"""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from functools import lru_cache
from typing import Any, Final

from .mabni_bridge import _real, align, masaq_words
from .pipeline_stations import repository_root_path

__all__ = [
    "INVENTORY_PATH",
    "calibration",
    "inventory",
    "masaq_reading",
    "matches",
]

INVENTORY_PATH: Final[str] = "corpora/sibawayh-abniya.tsv"
_INVENTORY_SHA256: Final[str] = (
    "678ca5144698b571a42804b19b8d1680766df7f2339cf6c9c53d84994051fdd9"
)
_SLOTS: Final[str] = "فعل"
_SHADDA: Final[str] = chr(0x0651)
_MARKS: Final[re.Pattern[str]] = re.compile("[ً-ِْٰـ]")
_HAMZA_SEATS: Final[re.Pattern[str]] = re.compile("[أإؤئ]")

_ATTACHED: Final[tuple[str, ...]] = tuple(
    "درهم بهرج دينار ديباج إسحاق يعقوب جورب آجور شبارق رستاق".split()
)
"""ما «ألحقوه ببناء كلامهم» (sham 24277-24283)."""
_NOT_REACHED: Final[tuple[str, ...]] = tuple(
    "آجر إبريسم إسماعيل سراويل فيروز قهرمان".split()
)
"""ما «لا يبلغون به بناء كلامهم» (sham 24286-24292)؛ «القهرمان» بلا أداة التعريف."""
_LEFT_AS_IS: Final[tuple[str, ...]] = tuple("خراسان خرم كركم".split())
"""ما «تركوا الاسم على حاله … كان على بنائهم أو لم يكن» (sham 24295-24296)."""

_NOUNY_TAGS: Final[tuple[str, ...]] = ("GERUND", "FOREIGN")


@lru_cache(maxsize=1)
def inventory() -> dict[str, frozenset[str]]:
    """الهياكلُ وطبقاتُها (N الأسماء، V الأفعال، P أسماءُ المزيد بقاعدة الميم)."""

    data = (repository_root_path() / INVENTORY_PATH).read_bytes()
    if hashlib.sha256(data).hexdigest() != _INVENTORY_SHA256:
        raise ValueError("الجردُ المجمَّدُ خالف بصمتَه")
    tiers: dict[str, set[str]] = {}
    for row in csv.DictReader(data.decode("utf-8").splitlines(), delimiter="\t"):
        tiers.setdefault(row["skeleton"], set()).add(row["tier"])
    return {skeleton: frozenset(t) for skeleton, t in tiers.items()}


def _skeletons(form: str) -> set[str]:
    """هياكلُ الصورة: بلا حركات، والهمزةُ ء، وآ = ءا، وى = ي، والشدّةُ حرفٌ أو حرفان."""

    bare = _MARKS.sub("", form)
    readings = {""}
    for ch in bare:
        if ch == _SHADDA:
            readings |= {r + r[-1] for r in readings if r}
        else:
            readings = {r + ch for r in readings}
    out = set()
    for r in readings:
        r = _HAMZA_SEATS.sub("ء", r.replace("آ", "ءا"))
        out.add(r.replace("ى", "ي"))
    return out


def matches(form: str) -> dict[str, frozenset[str]]:
    """الهياكلُ المجمَّدةُ التي تطابق الصورةَ في أيّ قراءةٍ لها، بطبقاتها."""

    found: dict[str, frozenset[str]] = {}
    for word in _skeletons(form):
        for skeleton, tiers in inventory().items():
            if len(skeleton) == len(word) and all(
                p in _SLOTS or p == w for p, w in zip(skeleton, word)
            ):
                found[skeleton] = tiers
    return found


def calibration() -> dict[str, dict[str, list[str]]]:
    """قوائمُ سيبويه في الدخيل: لكلّ كلمةٍ ما يطابقها من الهياكل."""

    return {
        name: {word: sorted(matches(word)) for word in words}
        for name, words in (
            ("attached", _ATTACHED),
            ("not_reached", _NOT_REACHED),
            ("left_as_is", _LEFT_AS_IS),
        )
    }


def masaq_reading() -> dict[str, Any]:
    """جذوعُ الأسماء في MASAQ مشكولةً: المطابقُ وغيرُه، وغيرُ المطابق باسمه ووسمه."""

    stems: Counter[str] = Counter()
    tags: dict[str, Counter[str]] = {}
    unaligned = 0
    for group in masaq_words():
        segs = [row for row in group if _real(row)]
        pieces = align(group[0]["Word"], [row["Segmented_Word"] for row in segs])
        for i, row in enumerate(segs):
            tag = row["Morph_tag"]
            if row["Morph_type"] != "Stem" or not (
                tag.startswith(("NOUN", "ADJ")) or tag in _NOUNY_TAGS
            ):
                continue
            if pieces is None:
                unaligned += 1
                continue
            stems[pieces[i]] += 1
            tags.setdefault(pieces[i], Counter())[tag] += 1
    unmatched = {form: n for form, n in stems.items() if not matches(form)}
    by_tier: Counter[str] = Counter()
    for form in stems:
        found = matches(form)
        if found:
            tiers = set().union(*found.values())
            by_tier["N" if "N" in tiers else "".join(sorted(tiers))] += 1
    return {
        "stem_types": len(stems),
        "stem_tokens": sum(stems.values()),
        "unaligned_tokens": unaligned,
        "matched_types_by_first_tier": dict(by_tier),
        "unmatched": {
            form: (n, tags[form].most_common(1)[0][0])
            for form, n in sorted(unmatched.items(), key=lambda kv: (-kv[1], kv[0]))
        },
    }
