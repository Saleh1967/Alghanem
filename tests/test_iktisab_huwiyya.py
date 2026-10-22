"""اكتسابُ قوانين الهويّة بالحدّ الأدنى المكتمل (ADR ١٢٤).

الأداة `tools/gen_iktisab_huwiyya.py`، والعقودُ `A116/IktisabHuwiyyaAqd.lean`.

* **التوقّعاتُ باليد** على `formal/a116/huruf.csv`:
  * القوانين بقواعد مكتوبةٍ هنا:
    * الوجودُ يمتنع في الألف المتحرّكة وحدَها.
    * الابتداءُ هو الحركة.
    * المبتدأُ به كلاهما، وهو 84 خانة.
  * ولماذا يكفي زوجُ (الحالة، مخرجُ الجزريّ): الألفُ وحدَها مخرجُها عند الجزريّ 0 (الجوف).
  * ولماذا لا يكفي (الحالة، مخرجُ سيبويه): الألفُ والهمزةُ في مخرجٍ واحد.
* **عدٌّ مستقلّ:** مُعدِّدٌ مكتوبٌ هنا بالترتيب المعلَن يجد أوّلَ مجموعة أوصافٍ تعيّن كلَّ قانون وموضعَها. فيساوي ما
  اكتسبه المتعلّم وعددَ ما عدّه. والأمثلةُ المضادّة (الموانع) خانتان بأوصافٍ واحدة وقانونٍ مختلف.
* **المولَّدُ هو المكتسَب:** `IktisabHuwiyyaData.lean` نصُّ ما في `huwiyya.json`.
* **طفرتان على الأداة**، يُعاد بعد كلٍّ منهما الاكتسابُ ويُفحص مخرجُه:
  * قانونُ وجودٍ مقلوبٌ في المعلّم (يمنع الألفَ الساكنة أيضًا).
  * حذفُ مخرج الجزريّ من أوصاف المتعلّم.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import re
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "gen_iktisab_huwiyya", ROOT / "tools" / "gen_iktisab_huwiyya.py")
assert _spec and _spec.loader
TOOL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(TOOL)

ROWS = list(csv.DictReader((ROOT / "formal" / "a116" / "huruf.csv").open(encoding="utf-8")))
RESULT = json.loads((ROOT / "docs" / "iktisab" / "huwiyya.json").read_text(encoding="utf-8"))
DATA = (ROOT / "formal" / "a116" / "A116" / "IktisabHuwiyyaData.lean").read_text(encoding="utf-8")

ORDER = ("hala", "makhraj16", "jazari17", "khalil11", "hams", "shidda", "tawassut", "istila",
         "itbaq", "idhlaq", "safir", "qalqala", "lin", "inhiraf", "takrir", "tafashi",
         "istitala", "ghunna")
"""ترتيبُ الأوصاف كما أعلنه ADR ١٢٤، مكتوبًا هنا؛ والحالةُ عمودُ `haraka`."""
COL = {"hala": "haraka"}


def col(w: str) -> str:
    return COL.get(w, w)


def wujud(r: dict[str, str]) -> bool:
    return not (r["harf"] == "ا" and r["haraka"] != "sukun")


def ibtida(r: dict[str, str]) -> bool:
    return r["haraka"] != "sukun"


def mubtada(r: dict[str, str]) -> bool:
    return wujud(r) and ibtida(r)


HAND = {"wujud": wujud, "ibtida": ibtida, "mubtada": mubtada}


def determines(ws: tuple[str, ...], law) -> bool:  # type: ignore[no-untyped-def]
    seen: dict[tuple[str, ...], bool] = {}
    for r in ROWS:
        k = tuple(r[col(w)] for w in ws)
        if seen.setdefault(k, law(r)) != law(r):
            return False
    return True


def test_hand_laws_match_lean_columns() -> None:
    assert len(ROWS) == 116
    assert sum(not wujud(r) for r in ROWS) == 3
    assert sum(mubtada(r) for r in ROWS) == 84
    for r in ROWS:
        assert (r["licensable"] == "true") == wujud(r)
        assert (r["ibtida"] == "true") == mubtada(r)


def test_why_jazari_and_not_sibawayh() -> None:
    assert {r["harf"] for r in ROWS if r["jazari17"] == "0"} == {"ا"}
    alif = {r["makhraj16"] for r in ROWS if r["harf"] == "ا"}
    hamza = {r["makhraj16"] for r in ROWS if r["harf"] == "ء"}
    assert alif == hamza


def test_recounted_independently() -> None:
    for name, law in HAND.items():
        n, found = 0, None
        for size in range(1, 5):
            for ws in combinations(ORDER, size):
                n += 1
                if determines(ws, law):
                    found = ws
                    break
            if found:
                break
        got = RESULT["laws"][name]
        assert list(found or ()) == got["wasf"], name
        assert n == got["enumerated"], name
        assert got["teacher_queries"] == len(got["manis"]) + 1, name


def test_minimal_complete_and_unique_by_hand() -> None:
    expected = {"wujud": [("hala", "jazari17")], "mubtada": [("hala", "jazari17")],
                "ibtida": [("hala",)]}
    for name, law in HAND.items():
        k = len(expected[name][0])
        assert [ws for ws in combinations(ORDER, k) if determines(ws, law)] == expected[name]
        assert not any(determines(ws, law) for j in range(1, k) for ws in combinations(ORDER, j))
        ws = expected[name][0]
        assert all(not determines(ws[:i] + ws[i + 1:], law) for i in range(len(ws)))


def test_ibtida_pairs_by_hand() -> None:
    for ws in combinations(ORDER, 2):
        assert determines(ws, ibtida) == ("hala" in ws), ws


def test_manis_are_real() -> None:
    by_name = {r["harf"] + r["haraka"]: r for r in ROWS}
    for name, law in HAND.items():
        for m in RESULT["laws"][name]["manis"]:
            a, b = (by_name[x] for x in m["mani"])
            assert all(a[col(w)] == b[col(w)] for w in m["wasf"]) and law(a) != law(b), (name, m)


def test_data_is_learned() -> None:
    for name in HAND:
        line = re.search(rf"/-- `{name}`: ([^.]+)\. -/", DATA)
        assert line and line.group(1).split(" + ") == RESULT["laws"][name]["wasf"]


def test_mutant_teacher_law(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setitem(TOOL.LAWS, "wujud", lambda r: r["harf"] != "ا")
    got = TOOL.acquire("wujud")
    assert not determines(tuple(got["wasf"]), wujud) or got["wasf"] != ["hala", "jazari17"]


def test_mutant_vocabulary_without_jazari(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(TOOL, "WASF", tuple(w for w in TOOL.WASF if w != "jazari17"))
    real = TOOL.features

    def feats(r):  # type: ignore[no-untyped-def]
        f = real(r)
        return f[:2] + f[3:]

    monkeypatch.setattr(TOOL, "features", feats)
    got = TOOL.acquire("wujud")
    assert got["wasf"] != ["hala", "jazari17"] and len(got["wasf"]) == 3
