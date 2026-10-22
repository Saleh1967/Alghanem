"""اكتسابُ قوانين الهويّة بالحدّ الأدنى المكتمل — الشريحةُ الأولى: الوجودُ والابتداء (ADR ١٢٤).

* **القيمة:** الخانةُ هويّةٌ (حاملٌ، حالة) في موضعها. والقانونُ دالّةٌ عليها.
* **أوصافُ الهويّة** التي يُعطاها المتعلّم (تعيينٌ معلَن) من `formal/a116/huruf.csv` الذي يطبعه `Jadwal`.
  والوجودُ والمبتدأُ به من عمودَي `licensable` و`ibtida` فيه، والابتداءُ قاعدةٌ هنا على
  تعريف `Hadd.kindOne`. والأوصاف:
  * الحالة.
  * مخرجُ سيبويه، ومخرجُ الجزريّ، وحيّزُ الخليل.
  * والصفاتُ الأربعَ عشرة.
  ولا يُعطى المتعلّمُ الحرفَ نفسه.
* **المعلّم** (`Teacher`) يحمل القانونَ وحدَه، و`learn` لا تُعطى إلّا الأوصافَ والمعلّم.
  ويُسأل عن مجموعة أوصاف، فيردّ «ثبت» إن عيّنت القانون،
  أو **مانعًا**: خانتين بأوصافٍ واحدة وقانونٍ مختلف (`Fasl`).
* **المتعلّم** يعدّد مجموعاتِ الأوصاف بالحجم ثمّ بترتيبها، ويُسقط بلا سؤال ما لا يفصل مانعًا سبق.
  فإذا ثبتت مجموعةٌ بنى جدولَها بسؤال المعلّم عن قيمة ممثّلٍ واحد لكلّ مفتاح.
* **القوانين الثلاثة** (وتعريفُها في Lean `A116/IktisabHuwiyya.lean`):
  * الوجود: `Jadwal.licensableCell`.
  * الابتداءُ على صنف الخانة: `Hadd.kindOne none · == .cv`.
  * المبتدأُ به: الوجودُ والابتداءُ معًا (`TawrithSitta.qawanin_sitta`).
* **المخرجات:** `docs/iktisab/huwiyya.json`، و`formal/a116/A116/IktisabHuwiyyaData.lean`؛
  و`--check` يعيد ويقارن بالبايت.
"""

from __future__ import annotations

import csv
import json
import sys
from collections.abc import Callable
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HURUF = ROOT / "formal" / "a116" / "huruf.csv"
RESULT = ROOT / "docs" / "iktisab" / "huwiyya.json"
DATA = ROOT / "formal" / "a116" / "A116" / "IktisabHuwiyyaData.lean"
MAX_SIZE = 4

SIFAT = ("hams", "shidda", "tawassut", "istila", "itbaq", "idhlaq", "safir", "qalqala", "lin",
         "inhiraf", "takrir", "tafashi", "istitala", "ghunna")
WASF = ("hala", "makhraj16", "jazari17", "khalil11", *SIFAT)
"""أوصافُ الهويّة بترتيبها المعلَن؛ والرقمُ في Lean موضعُ الوصف هنا."""
HALA = {"fatha": 0, "damma": 1, "kasra": 2, "sukun": 3}

Row = dict[str, str]


def rows() -> list[Row]:
    with HURUF.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def features(r: Row) -> tuple[int, ...]:
    """ما يراه المتعلّم من الخانة: الأوصافُ وحدَها."""
    return (HALA[r["haraka"]], int(r["makhraj16"]), int(r["jazari17"]), int(r["khalil11"]),
            *(int(r[s]) for s in SIFAT))


# ---------------------------------------------------------------- المعلّم: القوانينُ من جدول Lean


def law_wujud(r: Row) -> bool:
    return r["licensable"] == "true"


def law_ibtida(r: Row) -> bool:
    """صنفُ الخانة أوّلًا `cv` (`Hadd.kindOne none`): كلُّ متحرّكٍ cv وكلُّ ساكنٍ c."""
    return r["haraka"] != "sukun"


def law_mubtada(r: Row) -> bool:
    return r["ibtida"] == "true"


LAWS: dict[str, Callable[[Row], bool]] = {
    "wujud": law_wujud, "ibtida": law_ibtida, "mubtada": law_mubtada}


class Teacher:
    """يحمل القانونَ ويُخفيه؛ يردّ على مجموعة أوصافٍ بمانعٍ أو بـ«ثبت»، وعلى خانةٍ بقيمتها."""

    def __init__(self, law: Callable[[Row], bool], table: list[Row]) -> None:
        self._law = [law(r) for r in table]
        self._feat = [features(r) for r in table]

    def mani(self, ws: tuple[int, ...]) -> tuple[int, int] | None:
        seen: dict[tuple[int, ...], int] = {}
        for i, f in enumerate(self._feat):
            k = tuple(f[w] for w in ws)
            if k in seen and self._law[seen[k]] != self._law[i]:
                return seen[k], i
            seen.setdefault(k, i)
        return None

    def label(self, i: int) -> bool:
        return self._law[i]


# ---------------------------------------------------------------- المتعلّم


def learn(feats: list[tuple[int, ...]], teacher: Teacher) -> dict[str, object]:
    """المتعلّم: لا يرى إلّا الأوصافَ وردودَ المعلّم (مانعٌ برقمي خانتيه، أو قيمةُ خانة)."""
    manis: list[tuple[int, int]] = []
    enumerated = queries = 0
    asked: list[tuple[tuple[int, ...], tuple[int, int]]] = []
    for size in range(1, MAX_SIZE + 1):
        for ws in combinations(range(len(WASF)), size):
            enumerated += 1
            if any(all(feats[a][w] == feats[b][w] for w in ws) for a, b in manis):
                continue  # لا يفصل مانعًا سبق: يُسقط بلا سؤال
            queries += 1
            m = teacher.mani(ws)
            if m is not None:
                manis.append(m)
                asked.append((ws, m))
                continue
            jadwal: dict[tuple[int, ...], bool] = {}
            for i, f in enumerate(feats):
                k = tuple(f[w] for w in ws)
                if k not in jadwal:
                    jadwal[k] = teacher.label(i)
            return {"ws": ws, "enumerated": enumerated, "queries": queries,
                    "labels": len(jadwal), "asked": asked, "jadwal": jadwal}
    return {"ws": None, "enumerated": enumerated, "queries": queries, "asked": asked}


def acquire(name: str) -> dict[str, object]:
    """يبني المعلّمَ من الجدول، ويعطي المتعلّمَ الأوصافَ وحدَها؛ ثمّ يُسمّي الخاناتِ للتقرير."""
    table = rows()
    got = learn([features(r) for r in table], Teacher(LAWS[name], table))
    trace = [{"wasf": [WASF[w] for w in ws],
              "mani": [table[i]["harf"] + table[i]["haraka"] for i in m]}
             for ws, m in got["asked"]]  # type: ignore[attr-defined]
    ws = got["ws"]
    if ws is None:
        return {"law": name, "wasf": None, "enumerated": got["enumerated"],
                "teacher_queries": got["queries"], "manis": trace}
    return {"law": name, "wasf": [WASF[w] for w in ws], "index": list(ws),  # type: ignore[union-attr]
            "enumerated": got["enumerated"], "teacher_queries": got["queries"],
            "label_queries": got["labels"], "manis": trace,
            "jadwal": [[list(k), v] for k, v in sorted(got["jadwal"].items())]}  # type: ignore[attr-defined]


def lean_wasf(i: int) -> str:
    return [".hala", ".makhraj", ".jazari", ".hayyiz"][i] if i < 4 else f"(.sifa {i - 4})"


def build() -> dict[Path, str]:
    out = {name: acquire(name) for name in LAWS}
    lines = [
        "import A116.IktisabHuwiyya",
        "",
        "/-! مولَّدٌ بـ`tools/gen_iktisab_huwiyya.py` (ADR ١٢٤) — لا يُحرَّر باليد.",
        "    ما اكتسبه المتعلّم: أصغرُ مجموعة أوصافٍ تعيّن كلَّ قانون، وجدولُه عليها. -/",
        "",
        "namespace A116.IktisabHuwiyyaData",
        "",
        "open A116.IktisabHuwiyya",
    ]
    for name, r in out.items():
        assert r["wasf"] is not None, f"{name}_NOT_ACQUIRED"
        ws = ", ".join(lean_wasf(i) for i in r["index"])  # type: ignore[union-attr]
        rows_ = ", ".join(f"([{', '.join(map(str, k))}], {str(v).lower()})"
                          for k, v in r["jadwal"])  # type: ignore[union-attr]
        lines += ["", f"/-- `{name}`: {' + '.join(r['wasf'])}. -/",  # type: ignore[arg-type]
                  f"def {name}W : List Wasf := [{ws}]",
                  "", f"def {name}J : List (List Nat × Bool) := [{rows_}]"]
    lines += ["", "end A116.IktisabHuwiyyaData", ""]
    text = json.dumps({"adr": 124, "max_size": MAX_SIZE, "wasf": list(WASF), "laws": out},
                      ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return {RESULT: text, DATA: "\n".join(lines)}


def _name(p: Path) -> str:
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def main(argv: list[str]) -> int:
    out = build()
    if "--check" in argv:
        drift = [_name(p) for p, t in out.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != t]
        if drift:
            print("IKTISAB_HUWIYYA_DRIFT: " + ", ".join(drift))
            return 1
        print("iktisab-huwiyya: ok")
        return 0
    for p, t in out.items():
        p.write_text(t, encoding="utf-8")
    laws = json.loads(out[RESULT])["laws"]
    print(json.dumps({k: (v["wasf"], v["enumerated"], v["teacher_queries"], v["label_queries"])
                      for k, v in laws.items()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
