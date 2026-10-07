"""البوّاباتُ المتتابعة: الشهادةُ تصعد بوّابةً بوّابةً ولا بوّابةَ فوق مرفوضة، والمخرجُ ذرّاتٌ بعينها، والسجلُّ
يشهد أنّ كلَّ وحدةٍ موصولةٌ في كلّ موضع.

التوقّعاتُ مستقلّةٌ عن `gates`: تُعاد من الدوالّ الأصليّة ومن مودَع شهادات المصحف، والطفرةُ (ذرّةٌ ليست من
الـ116؛ ساكنٌ في الصدر؛ ثلاثيٌّ فقط يطلب عددًا؛ بوّابةٌ فوق مرفوضة) تُرفَض.
"""

from __future__ import annotations

import gzip
import json
from collections import Counter
from functools import cache
from pathlib import Path

from slge.cells import fold, licensed
from slge.entry import to_atoms
from slge.gates import LADDER, Pass, Refusal, climb, exit_atoms
from slge.madd import continue_licensed
from slge.manifest import MODULES, index_tools, tables

ROOT_DIR = Path(__file__).resolve().parent.parent


@cache
def _forms() -> list[tuple[tuple[str, str], ...]]:
    path = ROOT_DIR / "tests" / "data" / "corpus-certificates.json.gz"
    with gzip.open(path, "rt", encoding="utf-8") as f:
        d = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def test_ladder_order_and_named_refusals() -> None:
    names = [g.name for g in LADDER]
    assert names == ["الخانة", "الترخيص", "العدد", "الجداول", "الجذع", "الأدوات", "الصرف",
                     "الإعراب", "الجواب"]
    assert [g.governing for g in LADDER] == [True, True, True] + [False] * 6
    t = climb(("كَ", "تَ", "بَ"))
    assert all(isinstance(x, Pass) for x in t) and exit_atoms(t) == ("كَ", "تَ", "بَ")
    # الطفرة: ذرّةٌ ليست من الـ116 — تقف عند الخانة باسمها ولا بوّابةَ فوقها
    assert climb(("كَ", "ب")) == (Refusal("الخانة", "NOT_A_116_ATOM"),)
    # الطفرة: ساكنٌ في الصدر — تقف عند الترخيص
    assert climb(("كْ", "تَ"))[1:] == (Refusal("الترخيص", "NOT_CONTINUE_LICENSED"),)
    # الثلاثيُّ فقط: يمرّ الترخيصَ ويُرفض في العدد باسمه (عددُه في شهادته)
    t = climb(("حَ", "اْ", "جْ", "جَ"))
    assert isinstance(t[1], Pass) and len(t) == 3
    assert t[2] == Refusal("العدد", "TERNARY_ONLY_NO_NUMBER")


def test_whole_mushaf_climbs_consistently() -> None:
    forms = _forms()
    stops: Counter[int] = Counter()
    for w in forms:
        t = climb(to_atoms(w))
        stops[len(t)] += 1
        assert isinstance(t[0], Pass) and t[0].out == w and exit_atoms(t) == to_atoms(w)
        assert isinstance(t[1], Pass) == continue_licensed(w)
        if licensed(w):
            assert isinstance(t[2], Pass) and t[2].out == fold(w) and len(t) == len(LADDER)
        else:
            assert t[2] == Refusal("العدد", "TERNARY_ONLY_NO_NUMBER") and len(t) == 3
    assert stops == {len(LADDER): 18114, 3: 65}  # كما في BITS_INDEX: 18,114 ثنائيّ و65 ثلاثيٌّ فقط
    # البوّاباتُ القارئة لا ترفض: قراءةٌ أو «لا قراءة» باسمه
    tabled: Counter[str] = Counter()
    for w in forms[:3000]:
        t = climb(to_atoms(w))
        if len(t) == len(LADDER):
            assert isinstance(t[3], Pass)
            tabled[str(t[3].out)] += 1
    assert set(tabled) <= {"ضمير", "إشارة", "موصول", "أداة", "None"} and tabled["None"] > 2000


def test_manifest_covers_the_tree() -> None:
    import subprocess
    import sys

    assert len(MODULES) >= 50 and len(tables()) == 53 and len(index_tools()) == 43
    res = subprocess.run([sys.executable, str(ROOT_DIR / "tools" / "check_manifest.py")],
                         capture_output=True, text=True, cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr


def test_readers_under_the_law() -> None:
    """قانونُ القارئ: (١) بوّابةٌ في السُّلَّم لا دالّةٌ منفردة، (٢) مقيسٌ على مودَع المصحف قبل أيّ
    شريحة، (٣) لا يطابق قالبًا إلّا عبر تسوية الآخر المبرهَنة."""

    import re

    from slge.manifest import readers_under_law

    gates_src = (ROOT_DIR / "src" / "slge" / "gates.py").read_text(encoding="utf-8")
    law = readers_under_law()
    assert {m.name for m in law} >= {"madd", "jidh", "maqayis", "adawat", "wujud"}
    for m in law:
        assert re.search(rf"^from slge\.{m.name} import ", gates_src, re.M), f"{m.name}: ليس بوّابة"
        assert m.index, f"{m.name}: بلا فهرسٍ يقيسه"
        tool = (ROOT_DIR / "tools" / m.index).read_text(encoding="utf-8")
        assert "corpus-certificates.json.gz" in tool, f"{m.name}: لا يُقاس على المصحف"
        src = (ROOT_DIR / "src" / "slge" / f"{m.name}.py").read_text(encoding="utf-8")
        uses_templates = "on_template" in src or "senses(" in src
        if uses_templates and m.name != "jidh":
            assert "on_template_mod" in src or "jidh" in src, f"{m.name}: بلا تسوية الآخر"
