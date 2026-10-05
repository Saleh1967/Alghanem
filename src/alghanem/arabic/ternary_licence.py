"""الترخيصُ الثلاثيّ (CV · V · C) بدل الثنائيّ (M · S)، مقيسًا على نصٍّ مشكولٍ خارجَ القرآن.

النظيرُ في Lean: `formal/a116/A116/Ternary.lean`. والتطابقُ على كلّ سلسلةٍ بطول
‎1 … 11‎ يفحصه `tools/lean_a116_conformance.py --syllables` في CI، وحدُّه ‎11‎ =
أطولُ كلمةٍ مقطَّعةٍ في هذا النصّ (`longest_syllabified_word`):

* `binary_licensed`: قبولُ النموذج الثنائيّ — يبدأ بمتحرّك، ولا غيرُ متحرّكَين متجاورين.
  وهو `Admissible` في `Model.lean` بعد إسقاط المدّ والإغلاق على السكون
  (`Ternary.admissible_iff_admissibleB` و`binOK_eq_admissibleB`).
* `licences`: الوصلُ — تقطيعٌ بلا قطعةٍ صادرةٍ ولا CVCC ولا CVVCC؛ والوقفُ — كذلك،
  والمقطعُ الأخيرُ وحدَه يجوز أحدَهما.

والقراءةُ `tashkeela_reading` على `corpora/tashkeela-fadel-test.txt` — نصٌّ فقهيٌّ مشكول
(مدوّنة Tashkeela بقسمة Fadel وآخرين، MIT)، وقد يقتبس آياتٍ لم تُفصَل — تُخرج:
ما يرفضه الثنائيُّ ولا يرفضه الوصلُ الثلاثيّ (CVVC: مدٌّ قبل مضعَّف)، وما يرفضه الوصلُ
ويقبله الوقف (CVCC في الطرف)، وشهودَ الخانات الـ116، والأحاديَّ خارجَ قائمة القرآن.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from functools import lru_cache
from typing import Any, Final

from .a116_closure_gates import THE_116_ATOMS
from .mabni_stages import _DAGGER_ATOM, atom_kinds, stage_reading, syllabify
from .pipeline_stations import repository_root_path

__all__ = [
    "TASHKEELA_PATH",
    "binary_licensed",
    "longest_syllabified_word",
    "licences",
    "tashkeela_reading",
]

TASHKEELA_PATH: Final[str] = "corpora/tashkeela-fadel-test.txt"
_TASHKEELA_SHA256: Final[str] = (
    "4e851ff836f0a178abb15d9f4a8bcf92748b77cc0d67030d9fae2fbe698baa12"
)
_TASHKEELA_BYTES: Final[int] = 1747544
_WORD: Final[re.Pattern[str]] = re.compile(r"[\u0621-\u064a\u064b-\u0652\u0670\u0671]+")
_VOWELLED_ALIF: Final[tuple[str, ...]] = tuple(
    "\u0627" + chr(mark) for mark in (0x064E, 0x064F, 0x0650)
)
"""الألفُ بفتحةٍ وضمّةٍ وكسرة، مبنيّةً من نقاط الشفرة لا مكتوبةً حروفًا: هذا الملفُّ
داخلَ نطاق نثر الشجرة الذي تقيسه `letter_haraka_partition`، فلا يُقحَم فيه شاهدٌ."""

_PAUSE_ONLY: Final[frozenset[str]] = frozenset({"CVCC", "CVVCC"})
"""مقطعان لا يقعان إلّا طرفًا موقوفًا عليه: «بَحْر» و«تَامّ» موقوفًا عليهما."""

_PAUSE: Final[dict[str, dict[str, str]]] = {"0": {"entry": "start", "exit": "pause"}}


def binary_licensed(kinds: tuple[str, ...]) -> bool:
    """`binOK`: يبدأ بمتحرّك، ولا غيرُ متحرّكَين متجاورين (والفارغُ مقبول)."""

    if not kinds:
        return True
    if kinds[0] != "CV":
        return False
    return all(a == "CV" or b == "CV" for a, b in zip(kinds, kinds[1:]))


def licences(kinds: tuple[str, ...]) -> tuple[bool, bool]:
    """`(continueB, pauseB)`: الوصلُ ثمّ الوقف، من التقطيع وحدَه."""

    syllables = syllabify(kinds)
    if not syllables or syllables[0].endswith("|"):
        return False, False
    return (
        not any(s in _PAUSE_ONLY for s in syllables),
        not any(s in _PAUSE_ONLY for s in syllables[:-1]),
    )


@lru_cache(maxsize=1)
def _text() -> str:
    data = (repository_root_path() / TASHKEELA_PATH).read_bytes()
    if len(data) != _TASHKEELA_BYTES or hashlib.sha256(data).hexdigest() != (
        _TASHKEELA_SHA256
    ):
        raise ValueError("نصُّ Tashkeela المودَعُ خالف طولَه أو بصمتَه")
    return data.decode("utf-8")


def _cause(parsed: tuple[str, ...]) -> str:
    """سببُ الرفض مسمًّى: قطعةٌ صادرة، أو مقطعٌ مفرطُ الثِّقَل، ولا ثالث في هذا النصّ."""

    if parsed[0].endswith("|"):
        return parsed[0]
    for heavy in ("CVVCC", "CVCC", "CVVC"):
        if heavy in parsed:
            return heavy
    return "OTHER"


def _record_kinds(record: dict[str, Any]) -> tuple[str, ...]:
    """أنواعُ الذرّات من سجلّ الجسر بالقاعدة نفسِها في `mabni_stages.atom_kinds`."""

    kinds: list[str] = []
    for word in record["words"]:
        for cluster in word["clusters"]:
            for atom in cluster["atoms"]:
                if not atom.endswith("ْ"):
                    kinds.append("CV")
                elif cluster["role"] == "MADD" or atom == _DAGGER_ATOM:
                    kinds.append("V")
                else:
                    kinds.append("C")
    return tuple(kinds)


def longest_syllabified_word() -> int:
    """أطولُ كلمةٍ مقطَّعةٍ في النصّ بالذرّات: حدُّ ما يجب أن تغطّيه مطابقةُ Lean."""

    longest = 0
    for word in set(_WORD.findall(_text())):
        result = atom_kinds(word, verb=True)
        if isinstance(result, str) or syllabify(result[1]) is None:
            continue
        longest = max(longest, len(result[1]))
    return longest


def tashkeela_reading() -> dict[str, Any]:
    """القراءةُ كلُّها على النصّ الخارجيّ المودَع."""

    from canonical116.bridge import bridge

    lines = [_WORD.findall(line) for line in _text().splitlines()]
    cache: dict[str, Any] = {}
    deferred: Counter[str] = Counter()
    syllables: Counter[str] = Counter()
    cells: Counter[str] = Counter()
    binary_rejected: Counter[str] = Counter()
    continue_rejected: Counter[str] = Counter()
    monosyllables: Counter[str] = Counter()
    words = ready = 0
    for line in lines:
        for word in line:
            words += 1
            if word not in cache:
                cache[word] = atom_kinds(word, verb=True)
            result = cache[word]
            if isinstance(result, str):
                deferred[result] += 1
                continue
            atoms, kinds = result
            parsed = syllabify(kinds)
            if parsed is None:
                deferred["NOT_SYLLABIFIABLE"] += 1
                continue
            ready += 1
            syllables.update(parsed)
            cells.update(atoms)
            continuing, _ = licences(kinds)
            if not binary_licensed(kinds):
                binary_rejected[_cause(parsed)] += 1
            if not continuing:
                continue_rejected[_cause(parsed)] += 1
            if len(parsed) == 1:
                monosyllables[word] += 1
    stages = stage_reading()["lexical_monosyllables"]
    quran = {form for forms in stages.values() for form in forms}
    pause: Counter[str] = Counter()
    for line in lines:
        if not line:
            continue
        record = bridge(line[-1], contexts=_PAUSE)
        if record["status"] != "READY":
            pause["deferred"] += 1
            continue
        pause["ready"] += 1
        kinds = _record_kinds(record)
        if not binary_licensed(kinds):
            pause["binary_rejected"] += 1
        continuing, pausing = licences(kinds)
        pause["continue_licensed"] += continuing
        pause["pause_licensed"] += pausing
    vowelled_alif = {atom: cells[atom] for atom in _VOWELLED_ALIF if cells[atom]}
    return {
        "words": words,
        "syllabified": ready,
        "deferred": dict(deferred),
        "syllables": dict(syllables),
        "binary_rejected": dict(binary_rejected),
        "continue_rejected": dict(continue_rejected),
        "cells_witnessed": sum(1 for atom in THE_116_ATOMS if cells[atom]),
        "vowelled_alif": vowelled_alif,
        "pause": dict(pause),
        "new_monosyllables": sorted(
            word for word in monosyllables if word not in quran
        ),
    }
