"""بوّاباتُ الإغلاق الثلاث التي تركها «مونوغراف a116» التزاماتٍ، مقيسةً على المجال.

المونوغرافُ (الإصدار 1.0) سجّل الإغلاقَ بالعدّ التزامًا ببوّاباتٍ لم تُشغَّل، وبنى
«شهادةَ الولادة» على دعوى «صفرُ جذوعٍ بطول ≤ 2»، وترك مشغّلَ الوقف ناقصَ التحديد.
وهذه الوحدةُ تشغّلها كلَّها على مجالٍ معلن، بقواعد `mabni_stages` نفسِها:

* **بوّابةُ التغطية (α)** `segment_coverage`: كلُّ قطعةٍ في MASAQ — مبنيّةً ومعربة —
  إمّا مقطَّعةٌ وإمّا معلَّقةٌ بسببٍ مسمًّى من الجسر، وكلماتٌ لم تُحاذَ تُعَدّ باسمها.
* **بوّابةُ الضرورة (ج)** `cell_witnesses`: أيُّ خانات الـ116 لها شاهدٌ في القطع
  المقطَّعة، وأيُّها لا شاهدَ له.
* **بديلُ شهادة الولادة** `short_nouns`: الأسماءُ (جذوعًا وكلماتٍ تامّة) التي لا تتجاوز
  ذرّتين. وهي شاهدٌ مضادٌّ للدعوى: «يَدُ» كلمةٌ تامّةٌ من ذرّتين (الفتح 48:10).
* **فجوةُ الوقف** `pause_final_clusters`: خواتيمُ الآيات وقفًا على الجسر، وكم منها
  ينتهي بساكنين — وكلُّها يرفضها النموذجُ المعلن، والبديلُ `PauseAdmissible` في
  `formal/a116/A116/Pause.lean`.

والمجالُ MASAQ والنصُّ القرآنيُّ المودَع؛ وكلُّ رقمٍ هنا قولٌ فيهما لا في العربيّة كلِّها.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from functools import lru_cache
from typing import Any, Final

from .mabni_bridge import MabniGenus, _real, align, genus_of, masaq_words
from .mabni_stages import atom_kinds, syllabify
from .pipeline_stations import repository_root_path

__all__ = [
    "THE_116_ATOMS",
    "cell_witnesses",
    "pause_final_clusters",
    "segment_coverage",
    "short_nouns",
]

_LETTERS: Final[str] = "ابتثجحخدذرزسشصضطظعغفقكلمنهويء"
_HARAKAT: Final[str] = "َُِْ"
THE_116_ATOMS: Final[tuple[str, ...]] = tuple(
    letter + haraka for letter in _LETTERS for haraka in _HARAKAT
)

_QURAN: Final[str] = "corpora/quran-simple-enhanced.txt"
_QURAN_SHA256: Final[str] = (
    "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
)


@lru_cache(maxsize=1)
def _segments() -> tuple[tuple[str, str, str, Any], ...]:
    """كلُّ قطعةٍ محاذاةٍ: (الصورة، نوعُ القطعة، الوسم، الذرّاتُ وأنواعُها أو السبب)."""

    cache: dict[tuple[str, bool, bool], Any] = {}
    out: list[tuple[str, str, str, Any]] = []
    for group in masaq_words():
        segs = [row for row in group if _real(row)]
        pieces = align(group[0]["Word"], [row["Segmented_Word"] for row in segs])
        if pieces is None:
            out.append(
                (group[0]["Word"], "", "", "UNDERLYING_SEGMENTATION_NOT_ALIGNED")
            )
            continue
        for row, piece in zip(segs, pieces, strict=True):
            suffix = row["Morph_type"] == "Suffix"
            verb = genus_of(row["Morph_tag"]) is MabniGenus.MORPHOLOGICAL
            key = (piece, suffix, verb)
            if key not in cache:
                cache[key] = atom_kinds(piece, suffix=suffix, verb=verb)
            out.append((piece, row["Morph_type"], row["Morph_tag"], cache[key]))
    return tuple(out)


def segment_coverage() -> dict[str, Any]:
    """بوّابةُ التغطية: القطعُ المقطَّعة، والمعلَّقةُ بأسبابها، والكلماتُ غيرُ المحاذاة."""

    reasons: Counter[str] = Counter()
    syllabified = 0
    segments = 0
    unaligned = 0
    for _, _, _, result in _segments():
        if result == "UNDERLYING_SEGMENTATION_NOT_ALIGNED":
            unaligned += 1
            continue
        segments += 1
        if isinstance(result, str):
            reasons[result] += 1
        elif syllabify(result[1]) is None:
            reasons["NOT_SYLLABIFIABLE"] += 1
        else:
            syllabified += 1
    return {
        "segments": segments,
        "syllabified": syllabified,
        "deferred": dict(reasons),
        "unaligned_words": unaligned,
    }


def cell_witnesses() -> dict[str, Any]:
    """بوّابةُ الضرورة: لكلّ خانةٍ من الـ116 عددُ وقوعها في القطع المقطَّعة."""

    counts: Counter[str] = Counter()
    for _, _, _, result in _segments():
        if isinstance(result, str) or syllabify(result[1]) is None:
            continue
        counts.update(result[0])
    outside = sorted(atom for atom in counts if atom not in THE_116_ATOMS)
    return {
        "witnessed": sum(1 for atom in THE_116_ATOMS if counts[atom]),
        "unwitnessed": [atom for atom in THE_116_ATOMS if not counts[atom]],
        "atoms_outside_the_116": outside,
    }


def short_nouns() -> dict[str, Any]:
    """الأسماءُ من ذرّتين فأقلّ: جذوعًا، وكلماتٍ تامّةً لا قطعةَ معها."""

    stems: Counter[str] = Counter()
    words: Counter[str] = Counter()
    for group in masaq_words():
        segs = [row for row in group if _real(row)]
        pieces = align(group[0]["Word"], [row["Segmented_Word"] for row in segs])
        if pieces is None:
            continue
        for row, piece in zip(segs, pieces, strict=True):
            if row["Morph_type"] != "Stem" or not row["Morph_tag"].startswith("NOUN"):
                continue
            result = atom_kinds(piece)
            if isinstance(result, str) or len(result[0]) > 2:
                continue
            stems[piece] += 1
            if len(segs) == 1:
                words[piece] += 1
    return {"stems": dict(stems), "whole_words": dict(words)}


def pause_final_clusters() -> dict[str, Any]:
    """خواتيمُ الآيات وقفًا على الجسر: الجاهزة، وما ينتهي منها بساكنين، والمعلَّقة."""

    from canonical116.bridge import bridge

    path = repository_root_path() / _QURAN
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != _QURAN_SHA256:
        raise ValueError("النصُّ القرآنيُّ المودَع خالف بصمتَه")
    ready = final_ss = deferred = 0
    examples: list[str] = []
    for line in data.decode("utf-8").splitlines():
        words = line.split()
        if not words:
            continue
        record = bridge(words[-1], contexts={"0": {"entry": "start", "exit": "pause"}})
        if record["status"] != "READY":
            deferred += 1
            continue
        ready += 1
        atoms = record["canonical_atoms"]
        if len(atoms) >= 2 and atoms[-1].endswith("ْ") and atoms[-2].endswith("ْ"):
            final_ss += 1
            if len(examples) < 5:
                examples.append(words[-1])
    return {
        "ready": ready,
        "final_double_sukun": final_ss,
        "deferred": deferred,
        "examples": examples,
    }
