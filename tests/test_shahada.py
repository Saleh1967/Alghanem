"""شهادةُ SLGE: توقّعاتٌ مستقلّةٌ عن الشيفرة — البصمةُ تميّز الخاناتِ والمسارَ ونوعَ المدلول كلًّا على حدة،
والاقترانُ وترميزُ القائمة تقابلان الصيغَ المغلقة، والشهادةُ تُبنى من أثر السُّلَّم على المصحف ولا تُبنى
على مرفوض؛ وطفراتٌ مرفوضة."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

from slge.cells import licensed
from slge.entry import to_atoms
from slge.gates import LADDER, climb
from slge.nabhani import MADLUL
from slge.rawabit import cells_of
from slge.shahada import Shahada, atom_number, build, enc_list, fingerprint, pair, with_madlul

DATA = Path(__file__).parent / "data"


def test_pair_and_list_encoding_are_the_closed_forms() -> None:
    # اقترانُ كانتور: الزاويةُ الأولى 0,1,2 | 3,4,5 …
    corner = ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2))
    assert [pair(u, r) for u, r in corner] == list(range(6))
    seen = {pair(u, r) for u in range(40) for r in range(40)}
    assert len(seen) == 1600  # مميِّز على المربّع
    assert enc_list(()) == 0 and enc_list((5,)) == pair(5, 0) + 1
    assert len({enc_list(p) for p in ((), (0,), (1,), (0, 0), (0, 1), (1, 0), (0, 0, 0))}) == 7
    # عددُ الذرّات: الفارغُ صفر، والطولُ يفصل (الهمزةُ المفتوحة وحدَها ليست صفرًا)
    assert atom_number(()) == 0 and atom_number((("ء", "فتح"),)) == 1
    assert atom_number((("ا", "سكون"),)) == 116


def test_fingerprint_separates_cells_path_and_madlul() -> None:
    w = cells_of("كَتَبَ")
    s = Shahada(w, (0, 0, 2, 1, 1, 1, 1), None)
    fps = {fingerprint(s)}
    fps.add(fingerprint(Shahada(cells_of("كَتَبْ"), s.path, None)))  # خانةٌ واحدة تغيّرت
    fps.add(fingerprint(Shahada(w, (0, 0, 1, 1, 1, 1, 1), None)))  # المسارُ تغيّر
    fps.update(fingerprint(with_madlul(s, m)) for m in MADLUL)  # الأنواعُ الخمسة
    assert len(fps) == 8
    # الردُّ: الذرّاتُ من الخانات بعينها
    assert to_atoms(s.cells) == to_atoms(w)


def test_built_from_the_ladder_on_the_corpus_and_distinct_per_form() -> None:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        forms = [tuple((a, b) for a, b in x["cells"]) for x in json.load(f)["forms"]]
    readers = sum(1 for g in LADDER if not g.governing)
    fps: set[int] = set()
    distinct: set[tuple[tuple[str, str], ...]] = set()
    none = 0
    for w in forms[:1500]:
        s = build(climb(to_atoms(w)))
        if s is None:  # ثلاثيُّ الترخيص وحدَه (كحَاجَّ) يقف عند العدد — لا شهادةَ ثنائيّة
            assert not licensed(w)
            none += 1
            continue
        assert s.cells == w and len(s.path) == readers and s.madlul is None
        fps.add(fingerprint(s))
        distinct.add(w)
    # لا خاناتان مختلفتان ببصمةٍ واحدة (المودَعُ يكرّر خاناتٍ تختلف بقيّةُ رسمها — تلك في شهادة الغانم)
    assert len(fps) == len(distinct) and none < 20 and len(distinct) > 1400


def test_mutants_are_refused() -> None:
    # ذرّةٌ ليست من الـ116 تقف عند الخانة: لا شهادة
    assert build(climb(("كَ", "تَ", "xx"))) is None
    # ثلاثيُّ الترخيص (حَاجَّ) يقف عند العدد: لا شهادة
    assert build(climb(to_atoms(cells_of("حَاجَّ")))) is None
    # لا إسنادَ لنوعٍ خارج الخمسة
    s = Shahada(cells_of("كَتَبَ"), (0,), None)
    try:
        with_madlul(s, "نوعٌ سادس")
        raise AssertionError
    except AssertionError as e:
        assert str(e) == "نوعٌ سادس"
