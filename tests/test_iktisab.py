"""الاكتسابُ بالأمثلة المضادّة وتراكمُه (ADR ١٢٣، `tools/gen_iktisab.py`، `A116/IktisabAqd.lean`).

* **التوقّعاتُ باليد:** جداولُ الصدق مكتوبةً هنا صفًّا صفًّا (الناقص، قيمةُ البتّ، معلومُه، التعارض)،
  ومُقيِّمٌ للبرامج مكتوبٌ هنا لا مستورد من الأداة.
* **ما يُفحص:**
  * كلُّ برنامجٍ مكتسَب يستوفي جدولَه اليدويّ على الصفوف الصالحة، وهو نفسُه نصُّ `IktisabData.lean`.
  * حلقةُ الأمثلة المضادّة: كلُّ مثالٍ مضادّ ينقض مرشَّحَه، وكلُّ مرشَّحٍ سُئل عنه بعده يستوفي ما قبله.
  * **عددُ المعدود بعدٍّ مستقلّ:** مولِّدٌ مكتوبٌ هنا بالترتيب المعلَن في ADR ١٢٣
    (الحجم، ثمّ المتغيّرات والصفر، ثمّ `and`/`or`/`xor`/النداء) يجد موضعَ أوّل برنامجٍ
    يستوفي الجدولَ اليدويّ؛ ويساوي `enumerated` في النتيجة.
  * المرحلةُ الثانية تقرأ المكتبةَ من القرص: ملفٌّ فاسدٌ يغيّر ما تكتسبه، و`--check` يرفضه باسمه.
* **طفرتان على الأداة** تُشغَّل بعدهما المرحلةُ الأولى ويُطبَّق عليها الفحصُ اليدويّ نفسُه
  فيفشل: مواصفةُ المعلّم بلا النفي، وتقييمُ ‎⊕‎ ‎∨‎ في المتعلّم.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("gen_iktisab", ROOT / "tools" / "gen_iktisab.py")
assert _spec and _spec.loader
TOOL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(TOOL)

LIBRARY = json.loads((ROOT / "docs" / "iktisab" / "library.json").read_text(encoding="utf-8"))
RESULT = json.loads((ROOT / "docs" / "iktisab" / "result.json").read_text(encoding="utf-8"))
DATA = (ROOT / "formal" / "a116" / "A116" / "IktisabData.lean").read_text(encoding="utf-8")

# جداولُ باليد. الصفُّ (K1, V1, K2, V2)؛ الصالحُ: لا قيمةَ صادقةً بلا معلوم.
NAQIS = {(0, 0): 0, (1, 0): 1, (0, 1): 0, (1, 1): 0}
VALID4 = [(k1, v1, k2, v2) for k1 in (0, 1) for v1 in (0, 1) for k2 in (0, 1) for v2 in (0, 1)
          if (k1 or not v1) and (k2 or not v2)]
# البتّ: إن عُلم الأوّلُ فقيمتُه، وإلّا فالثاني.
BATT_QIMA = {(1, 1, 0, 0): 1, (1, 1, 1, 0): 1, (1, 1, 1, 1): 1, (1, 0, 0, 0): 0, (1, 0, 1, 0): 0,
             (1, 0, 1, 1): 0, (0, 0, 0, 0): 0, (0, 0, 1, 0): 0, (0, 0, 1, 1): 1}
BATT_MAALUM = {(0, 0, 0, 0): 0, (0, 0, 1, 0): 1, (0, 0, 1, 1): 1, (1, 0, 0, 0): 1, (1, 0, 1, 0): 1,
               (1, 0, 1, 1): 1, (1, 1, 0, 0): 1, (1, 1, 1, 0): 1, (1, 1, 1, 1): 1}
TAARUD = {(1, 0, 1, 1): 1, (1, 1, 1, 0): 1, (0, 0, 0, 0): 0, (0, 0, 1, 0): 0, (0, 0, 1, 1): 0,
          (1, 0, 0, 0): 0, (1, 0, 1, 0): 0, (1, 1, 0, 0): 0, (1, 1, 1, 1): 0}


def ev(s: str, env: tuple[int, ...], lib: dict[str, str]) -> int:
    """مُقيِّمٌ مستقلّ للصيغة النصّيّة."""
    s = s.strip()
    if s == "0":
        return 0
    if re.fullmatch(r"v\d+", s):
        return env[int(s[1:])]
    head, body = s.split("(", 1)
    body = body[:-1]
    depth = 0
    for i, c in enumerate(body):
        depth += (c == "(") - (c == ")")
        if c == "," and depth == 0:
            a, b = ev(body[:i], env, lib), ev(body[i + 1:], env, lib)
            break
    if head == "and":
        return a & b
    if head == "or":
        return a | b
    if head == "xor":
        return a ^ b
    return ev(lib[head], (a, b), lib)


def lib_bodies(lib: dict[str, dict[str, object]]) -> dict[str, str]:
    return {n: str(v["body"]) for n, v in lib.items()}


def test_hand_tables_complete() -> None:
    assert len(VALID4) == 9
    for t in (BATT_QIMA, BATT_MAALUM, TAARUD):
        assert sorted(t) == sorted(VALID4)


def test_naqis_acquired_and_meets_hand_table() -> None:
    body = LIBRARY["naqis"]["body"]
    assert naqis_ok(body)
    assert RESULT["stage_one"]["found"] == body


def test_stage_two_programs_meet_hand_tables() -> None:
    lib = lib_bodies(LIBRARY)
    for task, table in (("batt_qima", BATT_QIMA), ("batt_maalum", BATT_MAALUM), ("taarud", TAARUD)):
        for mode in ("bila_maktaba", "bil_maktaba"):
            prog = RESULT["stage_two"][task][mode]["found"]
            assert prog is not None, (task, mode)
            assert all(ev(prog, row, lib if mode == "bil_maktaba" else {}) == out
                       for row, out in table.items()), (task, mode)
            if mode == "bila_maktaba":
                assert "naqis" not in prog


def test_lean_data_is_what_was_learned() -> None:
    names = re.findall(r"/-- `(\w+)` \((\w+)\): `([^`]+)`", DATA)
    learned = {(t, m): RESULT["stage_two"][t][m]["found"] for t, m, _ in names}
    assert len(names) == 6 and all(p == learned[(t, m)] for t, m, p in names)
    assert f"`{LIBRARY['naqis']['body']}`. -/\ndef naqis" in DATA


def test_counterexamples_refute_and_constrain() -> None:
    trace = RESULT["stage_one"]["counterexamples"]
    assert len(trace) == RESULT["stage_one"]["teacher_queries"] - 1
    seen: list[tuple[int, ...]] = []
    for step in trace:
        row = tuple(step["row"])
        assert ev(step["candidate"], row, {}) != NAQIS[row]
        assert all(ev(step["candidate"], r, {}) == NAQIS[r] for r in seen)
        seen.append(row)


def naqis_ok(body: str) -> bool:
    return all(ev(body, row, {}) == out for row, out in NAQIS.items())


def of_size(k: int, s: int, libs: tuple[str, ...]) -> list[str]:
    """المولِّدُ المستقلّ بالترتيب المعلَن."""
    if s == 1:
        return [f"v{i}" for i in range(k)] + ["0"]
    out = []
    for head in ("and", "or", "xor", *libs):
        for left in range(1, s - 1):
            for a in of_size(k, left, libs):
                for b in of_size(k, s - 1 - left, libs):
                    out.append(f"{head}({a}, {b})")
    return out


def first_position(k: int, table: dict[tuple[int, ...], int], lib: dict[str, str]) -> int:
    n = 0
    for s in range(1, RESULT["max_size"] + 1):
        for e in of_size(k, s, tuple(sorted(lib))):
            n += 1
            if all(ev(e, row, lib) == out for row, out in table.items()):
                return n
    raise AssertionError("NOT_FOUND")


def test_enumerated_counts_recounted() -> None:
    lib = lib_bodies(LIBRARY)
    assert first_position(2, NAQIS, {}) == RESULT["stage_one"]["enumerated"]
    for task, table in (("batt_qima", BATT_QIMA), ("batt_maalum", BATT_MAALUM), ("taarud", TAARUD)):
        two = RESULT["stage_two"][task]
        assert first_position(4, table, {}) == two["bila_maktaba"]["enumerated"], task
        assert first_position(4, table, lib) == two["bil_maktaba"]["enumerated"], task


def test_stage_two_reads_library_from_disk(  # type: ignore[no-untyped-def]
        tmp_path: Path, monkeypatch) -> None:
    bad = tmp_path / "library.json"
    corrupt = {"naqis": dict(LIBRARY["naqis"], body="and(v0, v1)")}
    bad.write_text(json.dumps(corrupt), encoding="utf-8")
    out = json.loads(TOOL.stage_two(bad, RESULT["stage_one"])[TOOL.RESULT])
    before = RESULT["stage_two"]["batt_qima"]["bil_maktaba"]
    assert out["stage_two"]["batt_qima"]["bil_maktaba"] != before
    monkeypatch.setattr(TOOL, "LIBRARY", bad)
    assert TOOL.main(["--check"]) == 1


def test_mutant_teacher_spec(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """طفرةٌ على مواصفة المعلّم في جدول مهامّ الأداة: الفحصُ اليدويّ يرفض ما يُكتسب بعدها."""
    k, _spec, valid = TOOL.TASKS["naqis"]
    monkeypatch.setitem(TOOL.TASKS, "naqis", (k, lambda r: r[0] and r[1], valid))
    first, _ = TOOL.stage_one()
    assert not naqis_ok(str(first["found"]))


def test_mutant_learner_xor_as_or(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """طفرةٌ على مُقيِّم المتعلّم (‎⊕‎ تُحسب ‎∨‎): الفحصُ اليدويّ يرفض ما يُكتسب بعدها."""
    real = TOOL.column

    def bad(e, k, lib):  # type: ignore[no-untyped-def]
        if e[0] == "xor":
            return bad(e[1], k, lib) | bad(e[2], k, lib)
        if e[0] in ("and", "or"):
            a, b = bad(e[1], k, lib), bad(e[2], k, lib)
            return a & b if e[0] == "and" else a | b
        return real(e, k, lib)

    monkeypatch.setattr(TOOL, "column", bad)
    try:
        first, _ = TOOL.stage_one()
    except AssertionError as err:  # لا يُكتسب شيءٌ في الميزانية: الأداةُ ترفض باسمها
        assert "NAQIS_NOT_ACQUIRED" in str(err)
        return
    assert not naqis_ok(str(first["found"]))


def test_library_effect_as_it_came_out() -> None:
    two = RESULT["stage_two"]
    qima, taarud = two["batt_qima"], two["taarud"]
    assert qima["bil_maktaba"]["enumerated"] < qima["bila_maktaba"]["enumerated"]
    assert qima["bil_maktaba"]["size"] < qima["bila_maktaba"]["size"]
    # والمكتبةُ لها ثمن: حيث لا تُستعمل يكبر فضاءُ البحث.
    assert taarud["bil_maktaba"]["found"] == taarud["bila_maktaba"]["found"]
    assert taarud["bil_maktaba"]["enumerated"] > taarud["bila_maktaba"]["enumerated"]
