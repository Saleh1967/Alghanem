"""توقيعُ الحاجة (ADR ٥٦): التوقّعاتُ من النصّين المختومَين ومن جدول الحروف الموحَّد المبنيّ قبلها، لا
من الشيفرة.

١. المرساة: كلُّ مفتاحٍ عباراتُه في سطرٍ واحدٍ من كتابه بقراءةٍ مستقلّة هنا.
٢. معيارُ النبهانيّ: الحرفُ له حاجة، والمستقلُّ لا حاجةَ له، والمضمرُ حاجتُه مفسِّر.
٣. أبوابُ حروفٍ مكتوبةٌ باليد من نصوص ج3 (حروفُ الإضافة، المشبّهة، العطف، النفي، النداء، الاستفهام…).
٤. الصنفُ في `huruf.TABLE` (اسم/فعل) يوافق الحاجةَ بعد الحرف إلّا مسمّاةً.
وكلُّ قسمٍ بطفرةٍ مرفوضةٍ باسمها.
"""

from __future__ import annotations

import gzip
import hashlib
from collections.abc import Callable
from pathlib import Path

from slge import haja as H
from slge.haja_table import ANCHORS
from slge.huruf import TABLE as HURUF

DATA = Path(__file__).resolve().parent / "data"
BOOKS = {"shakhsiyya-3": ("nabhani-shakhsiyya-3.txt.gz",
                          "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4"),
         "kitab": ("openiti-sibawayh-kitab.txt.gz",
                   "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625")}


def _lines(book: str) -> list[str]:
    path, sha = BOOKS[book]
    raw = gzip.decompress((DATA / path).read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").split("\n")


def test_every_anchor_on_its_line() -> None:
    books = {b: _lines(b) for b in BOOKS}
    assert len(ANCHORS) == 18
    for key, book, _name, ln, phrases in ANCHORS:
        assert all(p in books[book][ln - 1] for p in phrases), key
        assert sum(all(p in x for p in phrases) for x in books[book]) == 1, key


def test_nabhani_criterion() -> None:
    for b in H.BAB_ALL:
        if b in H.HARF_BABS:
            assert H.NEEDS[b], b  # «لا يستقل بمعناه»
    assert H.NEEDS["mustaqill"] == ()  # «من غير حاجة للفظ آخر»
    assert H.NEEDS["damir"] == (("ayy", "ism", False, "H_DAMIR"),)  # «يفتقر إلى شيء يفسره»
    assert {"shart", "istifham"} == H.SADR  # س9213
    assert all(h[2] for b in ("istithna", "shart") for h in H.NEEDS[b])  # «متصلاً… بقاء الاتصال»
    # ولا اتّصالَ مفروضٌ حيث لا ينصّ النصّ
    assert [b for b in H.BAB_ALL if any(h[2] for h in H.NEEDS[b])] == ["istithna", "shart"]
    # المتعلَّقُ لا جهةَ له في «يفضي بمعاني الأفعال إلى الأسماء»
    assert ("ayy", "fil", False, "H_IDAFA") in H.NEEDS["jarr"]


# أبوابٌ باليد من نصوص ج3 499–539 والكتاب: (اسمُ الحرف في الجدول، البابُ المتوقَّع)
BY_HAND: tuple[tuple[str, str], ...] = (
    ("مِنْ", "jarr"), ("إِلَى", "jarr"), ("رُبَّ", "jarr"),            # حروفُ الإضافة
    ("خَلَا", "istithna"), ("حَاشَا", "istithna"),                       # «ومعناها الاستثناء»
    ("إِنَّ", "mushabbaha"), ("لَيْتَ", "mushabbaha"),                  # المشبّهة بالفعل
    ("ثُمَّ", "atf"), ("بَلْ", "atf"),                                  # حروفُ العطف
    ("إِنْ (النفي)", "nafy"),                                           # حروفُ النفي
    ("يَا", "nida"), ("أَيَا", "nida"),                                 # حروفُ النداء
    ("هَلْ", "istifham"), ("أَلَا", "tanbih"), ("كَلَّا", "rad"),
    ("سَوْفَ", "amilFil"), ("قَدْ", "amilFil"), ("إِذْمَا", "shart"),
)


def _hand_failures(bab: Callable[[int], str]) -> list[str]:
    idx: dict[str, list[int]] = {}
    for i, h in enumerate(HURUF):
        idx.setdefault(h.name, []).append(i)
    return [n for n, b in BY_HAND if all(bab(i) != b for i in idx[n])]


def test_babs_by_hand() -> None:
    assert _hand_failures(H.bab_of) == []
    assert [i for i in range(len(HURUF)) if H.bab_of(i) not in H.HARF_BABS] == [30, 65]


def test_mutant_istithna_as_jarr_rejected() -> None:
    """ISTITHNA_AS_JARR: خلا وعدا وحاشا بابَ الجرّ — يخالف «ومعناها الاستثناء» (ج3 516)."""

    def mutant(i: int) -> str:
        return "jarr" if H.bab_of(i) == "istithna" else H.bab_of(i)

    assert _hand_failures(mutant) == ["خَلَا", "حَاشَا"]


def test_class_agrees_with_huruf_table() -> None:
    def after(b: str, kind: str) -> bool:
        return any(j == "bad" and m == kind for j, m, _, _ in H.NEEDS[b])

    off = [i for i, h in enumerate(HURUF)
           if (h.cls == "اسم" and not after(H.bab_of(i), "ism"))
           or (h.cls == "فعل" and not after(H.bab_of(i), "fil"))]
    assert off == [30, 43, 44, 47]


def test_mutant_harf_without_need_rejected() -> None:
    """HARF_WITHOUT_NEED: حرفٌ بلا حاجة — يخالف «لا يستقل بمعناه» (ج3 500)."""

    needs = {**H.NEEDS, "tanbih": ()}
    assert [b for b in sorted(H.HARF_BABS) if not needs[b]] == ["tanbih"]


def test_mufrad_partition() -> None:
    assert H.mufrad_of("jarr", False) == "harf"
    assert H.mufrad_of("damir", False) == "mudmar"
    assert H.mufrad_of("mawsul", True) == "mudmar"
    assert H.mufrad_of("mustaqill", True) == "fil"
    assert H.mufrad_of("mustaqill", False) == "ism"
    assert H.mufrad_of("ghayrMusnad", False) == "ism"


def test_particles_named_in_their_anchor() -> None:
    """كلُّ أداةِ ربطٍ خارج الجدول اسمُها بين «» في عبارة مرساها، وهي في جدول الربط بصورتها."""

    from slge.rawabit import PARTICLES as RAWABIT

    phrases = {k: " ".join(ph) for k, _, _, _, ph in ANCHORS}
    names = {p.name for p in RAWABIT}
    for voc, bare, bab, key in H.PARTICLES:
        assert f"«{bare}»" in phrases[key], (voc, key)
        assert voc in names, voc
        assert bab in H.HARF_BABS


def test_mutant_unsourced_particle_rejected() -> None:
    """PARTICLE_WITHOUT_ANCHOR: «مَتَى» شرطًا بمرسى الشرط — اسمُها ليس في عبارته."""

    phrases = {k: " ".join(ph) for k, _, _, _, ph in ANCHORS}
    assert "«متى»" not in phrases["H_SHART"]
