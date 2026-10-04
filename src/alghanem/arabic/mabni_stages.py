"""استنفادُ المبنيّات درجةً درجة: من الخانة إلى المقطع إلى الصيغة إلى التركيب.

الترتيبُ والتركيبُ معًا، والاستنفادُ في كلّ درجةٍ قبل ترخيص التي تليها:

1. **الذرّة**: كلُّ صورةٍ مبنيّةٍ تُرسَل إلى جسر الـ116 (‎1.1‎)، فتخرج ذرّاتٍ لكلٍّ منها
   **نوعٌ** واحدٌ من ثلاثة: `CV` (خانةٌ متحرّكة)، `V` (ساكنةٌ دورُها مدّ: حرفُ مدٍّ أو
   ألفٌ خنجريّة)، `C` (ساكنةٌ تُغلق). والنوعُ يُقرأ من دور الجسر، لا من النصّ.
2. **المقطع**: ذرّةٌ متحرّكةٌ تفتح، وما بعدها من غير المتحرّك يُتمّه: `CV` · `CVV` ·
   `CVC` · `CVVC` · `CVCC`. وقطعةٌ تبدأ بساكنٍ شقُّ تضعيفٍ قطعه التجزيءُ (`C|`)، أو
   تبدأ بحرفِ مدٍّ عارٍ نواتُه في القطعة السابقة (`V|`: واوُ الجماعة، ألفُ الاثنين،
   ياءُ المخاطَبة…)؛ والقطعتان حدّا تجزيء MASAQ لا مقطعان.
   والتقطيعُ دالّةٌ وحيدةُ الناتج؛ وبرهانُه العامّ في `formal/a116/A116/Stages.lean`.
3. **الصيغة**: تسلسلُ مقاطع. والدرجةُ عددُ مقاطعها؛ ويُستنفَد الأحاديُّ (`CV` ثمّ `CVV`
   ثمّ `CVC`) قائمةً مغلقةً قبل ما فوقه.
4. **التركيب**: صيغةٌ متعدّدةُ المقاطع تُقطَّع إلى صيغٍ مرخَّصةٍ أقصر بشرط الموضع
   (`Prefix* Stem+ Suffix*`). والتقطيعُ **مرشَّحٌ لا حكم**: يجوز أن يجمع وحداتٍ
   وظائفُها مختلفة (`A_COMPOSITION_IS_A_CANDIDATE_NOT_A_VERDICT`).

**الجامعُ المانع**: كلُّ صورةٍ مبنيّةٍ إمّا مقطَّعةٌ وإمّا معلَّقةٌ بسببٍ مسمًّى من الجسر،
ولا ثالث؛ ومجموعُ القسمين هو الكلّ (`stage_reading`).

**الحدّ**: المجالُ قطعُ MASAQ المبنيّةُ على النصّ القرآنيّ؛ وما يُقال هنا قولٌ فيه،
لا في العربيّة كلِّها.
"""

from __future__ import annotations

import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Final

from .mabni_bridge import (
    CONTEXTS,
    DAMMA,
    FATHA,
    KASRA,
    SUKUN,
    MabniGenus,
    _clusters,
    _starts_with_definite_article,
    mabni_segments,
    wasl_start_vowel,
)

__all__ = [
    "A_COMPOSITION_IS_A_CANDIDATE_NOT_A_VERDICT",
    "ATOM_KINDS",
    "SYLLABLES",
    "FormRecord",
    "atom_kinds",
    "compositions",
    "form_records",
    "stage_reading",
    "syllabify",
]

A_COMPOSITION_IS_A_CANDIDATE_NOT_A_VERDICT: Final[str] = (
    "التقطيعُ إلى صيغٍ مرخَّصةٍ أقصر مرشَّحٌ لا حكم: «إِنَّ» تُقطَّع «إِنْ + نَ» "
    "والنونُ اللاحقةُ وظيفتُها غيرُ وظيفة الشقّ الثاني من التضعيف"
)

ATOM_KINDS: Final[tuple[str, ...]] = ("CV", "V", "C")
SYLLABLES: Final[tuple[str, ...]] = (
    "CV",
    "CVV",
    "CVC",
    "CVVC",
    "CVCC",
    "C|",
    "V|",
    "VC|",
)

_DAGGER_ATOM: Final[str] = "ا" + SUKUN


_ARTICLE_SEGMENTS: Final[frozenset[str]] = frozenset({"ال", "الْ"})
"""قطعةُ «ال» وحدَها كما يفصلها MASAQ: همزةُ وصلٍ مفتوحةُ الابتداء ولامٌ ساكنة."""

_MADD_LETTERS: Final[frozenset[str]] = frozenset("اوي")

_SILENT_WAW: Final[str] = "أُول"
"""«أُولَئِكَ، أُولَاءِ، أُولِي…»: واوُها رسمٌ لا يُنطق، ولا دورَ في الجسر لواوٍ صامتة،
فتبقى معلَّقةً بسبب الجسر لا مقروءةً مدًّا (استثناءٌ مسمًّى واحد)."""


def _record(form: str, verb: bool = False) -> dict[str, Any]:
    """سجلُّ الجسر للصورة المعجميّة، بتعليقاتٍ معلنةٍ ثلاثٍ لا غير.

    ١. «ال» في أوّل الصورة، أو قطعةُ «ال» وحدَها: همزةُ وصلٍ تُفتح، ولامُ القطعة ساكنة.
    ٢. فعلٌ يبدأ بألفٍ عاريةٍ يليها ساكن: همزةُ وصلٍ حركتُها `wasl_start_vowel`
       (ضمٌّ إن ضُمّ الثالث وإلا كسر) — القاعدةُ نفسُها في `mabni_bridge`.
    ٣. ياءٌ عاريةٌ بعد كسرٍ، أو واوٌ عاريةٌ بعد ضمّ: مدٌّ في أيّ موضع (الَّذِينَ، قُولُ)،
       إلا ما بدأ بـ`_SILENT_WAW`.
    """

    from canonical116.bridge import bridge

    notes: dict[str, dict[str, str]] = {}
    clusters = _clusters(unicodedata.normalize("NFD", form))
    if form in _ARTICLE_SEGMENTS or _starts_with_definite_article(form):
        notes["0"] = {
            "role": "WASL",
            "start_vowel": FATHA,
            "evidence": "همزةُ وصل «ال» تُفتح في الابتداء",
        }
        if form == "ال":
            notes["1"] = {"state": SUKUN, "evidence": "لامُ التعريف ساكنة"}
    elif verb and (vowel := wasl_start_vowel(form)) is not None:
        notes["0"] = {
            "role": "WASL",
            "start_vowel": vowel,
            "evidence": "همزةُ وصلٍ في أوّل فعل: تُضمّ إن ضُمّ الثالث وإلا تُكسر",
        }
    for k in range(1, len(clusters)):
        letter, previous = clusters[k], clusters[k - 1]
        madd = (letter == "ي" and KASRA in previous) or (
            letter == "و" and DAMMA in previous and not form.startswith(_SILENT_WAW)
        )
        if madd:
            notes[str(k)] = {
                "state": SUKUN,
                "evidence": "حرفُ مدٍّ عارٍ: ياءٌ بعد كسر، أو واوٌ طرفٌ بعد ضمّ",
            }
    annotations = {"0": notes} if notes else None
    return bridge(form, contexts=CONTEXTS["start_continue"], annotations=annotations)


def atom_kinds(
    form: str, suffix: bool = False, verb: bool = False
) -> tuple[tuple[str, ...], tuple[str, ...]] | str:
    """الذرّاتُ وأنواعُها، أو سببُ تعليق الجسر باسمه.

    وواوٌ أو ياءٌ عاريةٌ في أوّل القطعة، أو ألفٌ عاريةٌ في أوّل **لاحقة** (`suffix`): حرفُ
    مدٍّ نواتُه في القطعة السابقة (يُـ|وعَدُ، ـهُـ|وا)، فيُعَدّ `V` بلا جسر؛ والألفُ بعد
    واوٍ في آخرها فارقةٌ لا تُنطق. ولا يُطبَّق على ألفٍ في غير اللاحقة: ألفُ «ابْتَغَى»
    ألفُ وصل.
    """

    clusters = _clusters(unicodedata.normalize("NFC", form))
    if clusters and (clusters[0] in "وي" or (suffix and clusters[0] == "ا")):
        rest = "".join(clusters[1:])
        if rest in ("", "ا") and clusters[0] == "و" or rest == "":
            return (clusters[0] + SUKUN,), ("V",)
        tail = atom_kinds(rest)
        if isinstance(tail, str):
            return tail
        return (clusters[0] + SUKUN, *tail[0]), ("V", *tail[1])
    record = _record(form, verb)
    if record["status"] != "READY":
        reasons = [r["reason"] for r in record["deferrals"] + record["rejections"]]
        return str(reasons[0]) if reasons else str(record["status"])
    atoms: list[str] = []
    kinds: list[str] = []
    for word in record["words"]:
        for cluster in word["clusters"]:
            for atom in cluster["atoms"]:
                atoms.append(atom)
                if not atom.endswith(SUKUN):
                    kinds.append("CV")
                elif cluster["role"] == "MADD" or atom == _DAGGER_ATOM:
                    kinds.append("V")
                else:
                    kinds.append("C")
    return tuple(atoms), tuple(kinds)


_CODA: Final[dict[tuple[str, ...], str]] = {
    (): "CV",
    ("V",): "CVV",
    ("C",): "CVC",
    ("V", "C"): "CVVC",
    ("C", "C"): "CVCC",
}


_LEAD: Final[dict[tuple[str, ...], str]] = {
    ("C",): "C|",
    ("V",): "V|",
    ("V", "C"): "VC|",
}


def syllabify(kinds: tuple[str, ...]) -> tuple[str, ...] | None:
    """التقطيعُ المقطعيّ: متحرّكٌ يفتح وما بعده يُتمّ؛ وما لا يُقطَّع يُرَدّ `None`."""

    out: list[str] = []
    i = 0
    while i < len(kinds) and kinds[i] != "CV":
        i += 1
    if i:
        lead = _LEAD.get(kinds[:i])
        if lead is None:
            return None
        out.append(lead)
    while i < len(kinds):
        if kinds[i] != "CV":
            return None
        j = i + 1
        while j < len(kinds) and kinds[j] != "CV":
            j += 1
        coda = _CODA.get(kinds[i + 1 : j])
        if coda is None:
            return None
        out.append(coda)
        i = j
    return tuple(out) if out else None


@dataclass(frozen=True)
class FormRecord:
    """صورةٌ مبنيّةٌ بجنسها وموضعها وعدد وقوعها، وتقطيعُها أو سببُ تعليقها."""

    form: str
    genus: str
    morph_type: str
    tokens: int
    atoms: tuple[str, ...]
    kinds: tuple[str, ...]
    syllables: tuple[str, ...] | None
    deferral: str | None

    @property
    def degree(self) -> int:
        """الدرجة: عددُ المقاطع، والقطعتان `C|` و`V|` لا تُعَدّان مقطعًا."""

        return sum(1 for s in self.syllables or () if not s.endswith("|"))


@lru_cache(maxsize=1)
def form_records() -> tuple[FormRecord, ...]:
    """كلُّ صورةٍ مبنيّةٍ مختلفة (بجنسها وموضعها) مرّةً واحدة، مرتّبةً ترتيبًا ثابتًا."""

    segments, _ = mabni_segments()
    counts: Counter[tuple[str, str, str]] = Counter(
        (s.genus.name, s.morph_type, s.vocalized) for s in segments
    )
    out: list[FormRecord] = []
    for (genus, morph_type, form), tokens in sorted(counts.items()):
        result = atom_kinds(
            form,
            suffix=morph_type == "Suffix",
            verb=genus == MabniGenus.MORPHOLOGICAL.name,
        )
        if isinstance(result, str):
            out.append(
                FormRecord(form, genus, morph_type, tokens, (), (), None, result)
            )
            continue
        atoms, kinds = result
        syllables = syllabify(kinds)
        deferral = None if syllables else "NOT_SYLLABIFIABLE"
        out.append(
            FormRecord(
                form, genus, morph_type, tokens, atoms, kinds, syllables, deferral
            )
        )
    return tuple(out)


_ROLE_ORDER: Final[dict[str, int]] = {"Prefix": 0, "Stem": 1, "Suffix": 2}


def compositions(record: FormRecord) -> list[list[tuple[str, str]]]:
    """تقطيعاتُ الصيغة إلى صيغٍ معجميّةٍ مرخَّصةٍ أقصر، بشرط `Prefix* Stem+ Suffix*`."""

    units: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for other in form_records():
        if other.genus == MabniGenus.LEXICAL.name and other.syllables:
            units[other.atoms].add(other.morph_type)
    atoms = record.atoms
    found: list[list[tuple[str, str]]] = []

    def walk(i: int, last: int, stems: int, parts: list[tuple[str, str]]) -> None:
        if i == len(atoms):
            if len(parts) >= 2 and stems >= 1:
                found.append(list(parts))
            return
        for j in range(i + 1, len(atoms) + 1):
            if j - i == len(atoms):
                continue
            for role in sorted(units.get(atoms[i:j], ())):
                rank = _ROLE_ORDER.get(role)
                if rank is None or rank < last:
                    continue
                parts.append(("".join(atoms[i:j]), role))
                walk(j, rank, stems + (role == "Stem"), parts)
                parts.pop()

    walk(0, 0, 0, [])
    return found


def stage_reading() -> dict[str, Any]:
    """القراءةُ كلُّها: الجامعُ المانع، والاستنفادُ بالدرجة، وأنماطُ المقاطع بالجنس."""

    records = form_records()
    ready = [r for r in records if r.syllables]
    deferred = [r for r in records if not r.syllables]
    by_genus: dict[str, Counter[str]] = defaultdict(Counter)
    for r in ready:
        for s in r.syllables or ():
            by_genus[r.genus][s] += 1
    monosyllables: dict[str, list[str]] = {}
    for kind in ("CV", "CVV", "CVC"):
        monosyllables[kind] = sorted(
            {
                r.form
                for r in ready
                if r.genus == MabniGenus.LEXICAL.name and r.syllables == (kind,)
            }
        )
    lexical_multi = [
        r for r in ready if r.genus == MabniGenus.LEXICAL.name and r.degree >= 2
    ]
    composed = [r for r in lexical_multi if compositions(r)]
    return {
        "forms": len(records),
        "syllabified": len(ready),
        "deferred": dict(Counter(r.deferral for r in deferred)),
        "forms_by_genus": dict(Counter(r.genus for r in records)),
        "syllables_by_genus": {g: dict(c) for g, c in sorted(by_genus.items())},
        "degree_by_genus": {
            g: dict(sorted(Counter(r.degree for r in ready if r.genus == g).items()))
            for g in sorted({r.genus for r in ready})
        },
        "lexical_monosyllables": monosyllables,
        "lexical_multisyllabic": len(lexical_multi),
        "lexical_with_a_candidate_composition": len(composed),
    }
