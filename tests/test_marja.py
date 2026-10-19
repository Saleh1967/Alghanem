"""مرجعُ المالك (`A116.Marja`، ADR ١١٨) مقروءًا من الجداول المولَّدة لا من Lean.

التوقّعاتُ مكتوبةٌ هنا باليد:

١. **سُلَّمُ الباب**: أصنافُ الجهر والأصنافُ الثمانية التي أسمّيها «الشدّة وما يقابلها» (عبارتي،
   لا لفظُ الكتاب) والإطباق باليد، وكلُّ صنفٍ يُقرأ في سطره من «الكتاب» المختوم بأسماء حروفه
   (`NAMES`)؛ والمخارجُ الستّةَ عشر باليد وتُقارن بصفوف `Makharij.lean` التي يرسيها
   `tests/test_makharij.py` في الباب المختوم (واللامُ من نقل السيرافيّ)؛ ثمّ يُعاد حسابُ الموانع
   بالدرجات ودرجةُ الولادة وقرناءُ كلّ حرف بشيفرةٍ مستقلّة، ويُقارن بـ`marja-huruf.csv`.
٢. **الولادات**: الدورُ بقاعدة المدّ (الألفُ بعد الفتحة، والواوُ بعد الضمّة، والياءُ بعد
   الكسرة)، والحكمُ بأزواج الجوار الستّة وزوج الوقف مكتوبةً هنا، وقيدِ الألف و«لا يُبتدأ بساكن
   ولا يُوقف على متحرّك»؛ لكلّ صفٍّ من الـ1044 في `marja.csv`، والعددُ ‎n = 9k + m‎، والبرجُ
   نفسُه في `huruf.csv`. والقاعدةُ هنا تعيد صياغةَ قاعدة `A116.Marja.hukm` بيدٍ أخرى، فهي تشهد
   على توليد الجدول لا على مصدر القاعدة (`TEST_MIRRORS_CODE` معلنًا).
٣. **الأزواج**: 841 زوجًا، والمثلُ والمثلُ الممتنعُ باليد، وأعمدةُ الحرف في `marja-huruf.csv`
   مجموعُها صفوفُ `marja-azwaj.csv`.
٤. **الختم**: بصماتُ `Marja.lean` والجداول الثلاثة والتسجيل وأداةِ الشاهد في `docs/marja/khatm.json`
   (والشاهدُ يُضاف بعد تشغيله)، ونصُّ المالك كاملًا بلفظه.
٥. **أداةُ الشاهد**: `tools/gen_marja.births` على تيّارٍ مصطنع (لا مصحف) يغطّي وجوهَ الوصل الثلاثة على
   الحدّ، والمثلين بعد مدٍّ وبلا مدّ، ومدَّ الفرق، والساكنَ بعد ساكنٍ على الحدّ، والرمزَ المرفوض، والكلمةَ
   الأخيرةَ من خانةٍ واحدة — والمتوقَّعُ مكتوبٌ باليد ولادةً ولادة.
٦. **الشاهد**: `docs/marja/shahid.json` متّسقٌ في نفسه وببصمات ما يقرؤه (وإعادتُه بـ
   `tools/gen_marja.py --check`).

الطفرات: على الشاهد اليدويّ `MUTANT_WASL_CC`، `MUTANT_LADDER_ORDER`، `MUTANT_HAND_MAJHURA`؛ وعلى
الجدول المولَّد `MUTANT_CSV_HUKM_FLIP`؛ وعلى الختم `MUTANT_SEAL_BYTE`؛ وعلى الأداة نفسِها
`MUTANT_TOOL_SEAM_IN_H2`، `MUTANT_TOOL_NO_ISLAH`، `MUTANT_TOOL_NO_MADD_IN_H2`،
`MUTANT_TOOL_MADD_ALWAYS`، `MUTANT_TOOL_ONE_CELL_WASL`، `MUTANT_TOOL_GEMINATE_SAKIN`،
`MUTANT_TOOL_FARQ_ANY_LETTER`، `MUTANT_TOOL_FARQ_ANY_POS`. وطفراتُ Lean في `docs/tafrat.json`.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import json
import types
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
A116 = ROOT / "formal" / "a116"
MARJA = A116 / "marja.csv"
HURUF_M = A116 / "marja-huruf.csv"
AZWAJ = A116 / "marja-azwaj.csv"
HURUF = A116 / "huruf.csv"
LEAN = A116 / "A116" / "Marja.lean"
AUDIT = A116 / "Audit.lean"
KITAB = ROOT / "corpora" / "kitab" / "0180Sibawayhi.KitabSibawayhi.JK006989-ara1.gz"
KHATM = ROOT / "docs" / "marja" / "khatm.json"
SHAHID = ROOT / "docs" / "marja" / "shahid.json"
PREREG = ROOT / "docs" / "marja" / "PREREG.md"
TOOL = ROOT / "tools" / "gen_marja.py"
OWNER = ("جدول الكندي: لا يُبنى قبل أن ترفع صفحات الجدول من التحقيق، وأن تقرّر نوع المودَع ومعنى "
         "«التجاور» الذي نقارن به. ابني جدولنا الخاص ابحث بعمق عن الكندي وما شابه ولكن ابني جدولنا "
         "الخاص واجمع فيه قانون الابتداء وقانون الوصل وقانون الفصل وقانون الوقف  ليكون مرجع خاص "
         "بالمالك ومعتمده ونختمه كمرجع خاص ويجب ان تراجع الليف في جذر المشروع للمخارج والصفات "
         "وحروف كل مخرج وترخيصها التدريجي اعمل بعمق")

NAMES = {
    "الهمزة": "ء", "الألف": "ا", "الهاء": "ه", "العين": "ع", "الحاء": "ح", "الغين": "غ",
    "الخاء": "خ", "القاف": "ق", "الكاف": "ك", "الجيم": "ج", "الشين": "ش", "الياء": "ي",
    "الضاد": "ض", "اللام": "ل", "النون": "ن", "الراء": "ر", "الطاء": "ط", "الدال": "د",
    "التاء": "ت", "الزاي": "ز", "السين": "س", "الصاد": "ص", "الظاء": "ظ", "الذال": "ذ",
    "الثاء": "ث", "الفاء": "ف", "الباء": "ب", "الميم": "م", "الواو": "و",
}
# المخارجُ بترتيب الباب، واللامُ بعد الضاد من نقل السيرافيّ، والخياشيمُ بلا حرف — باليد، ومرساها صفوفُ
# `Makharij.lean` التي يفحصها `tests/test_makharij.py` في الباب المختوم (`test_makharij_anchored`).
MAKHARIJ = ["ءها", "عح", "غخ", "ق", "ك", "جشي", "ض", "ل", "ن", "ر", "طدت", "زسص", "ظذث", "ف", "بمو",
            ""]
# (بدايةُ الجملة في النصّ المختوم، نهايتُها، الحروف) — بترتيب فقرات الباب.
MAJHURA = ("فأما المجهورة", "فذلك تسعة عشر", "ءاعغقجيضلنرطدزظذبمو")
MAHMUSA = ("وأما المهموسة", "فذلك عشرة", "هحخكشستصثف")
MANNERS = [
    ("وهو الذي يمنع الصوت أن يجري فيه", "", "ءقكجطتدب"),
    ("ومنها الرخوة وهي", "", "هحغخشصضزسظثذف"),
    ("وأما العين فبين الرخوة والشديدة", "", "ع"),
    ("كاعتراض الحروف الشديدة وهو اللام", "", "ل"),
    ("لم يجر معه الصوت وهو النون وكذلك الميم", "", "نم"),
    ("لم يجر الصوت فيه وهو الراء", "", "ر"),
    ("ومنها اللينة وهي الواو والياء", "", "وي"),
    ("وترفع في الياء لسانك قبل الحنك وهي الألف", "", "ا"),
]
MUTBAQA = ("فأما المطبقة", "", "صضطظ")
WASL = {("cv", "cv"), ("cv", "v"), ("cv", "c"), ("v", "cv"), ("v", "c"), ("c", "cv")}
WAQF = {("c", "c")}
MADD = {("ا", "fatha"), ("و", "damma"), ("ي", "kasra")}
HARAKAT = ["fatha", "damma", "kasra", "sukun"]
MAWADI = ["ibtida"] + [f"wasl:{h}" for h in HARAKAT] + [f"waqf:{h}" for h in HARAKAT]
THEOREMS = ["sabab_take", "tadarruj", "mani_darajat", "mani_qabla_itbaq_lawla", "mani_qabla_itbaq",
            "fasl_akhir",
            "tayin_akhir", "mukhtamal_sibawayh", "tartib_la_yughayyir_al_akhir", "wilada_le",
            "wilada_adad", "wilada_itbaq", "mani_tadarruj", "lif_ahjam", "lif_wilada", "mawadi_idx",
            "dawr_kindOne", "qablK_mada", "n_tamam", "adad_ibtida", "adad_wasl_mutaharrik",
            "adad_wasl_sakin", "adad_waqf", "qanun_tadarruj", "shahid_ibtida",
            "shahid_wasl_mutaharrik", "shahid_wasl_sakin", "shahid_waqf", "shahid_yuskan",
            "idgham_jumla"]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def kitab() -> str:
    return gzip.decompress(KITAB.read_bytes()).decode("utf-8")


def named(sentence: str) -> str:
    """الحروفُ التي تسمّيها الجملة بأسمائها بترتيبها."""

    words = [w.lstrip("و").lstrip("ف") for w in sentence.replace("،", " ").split()]
    out = []
    for w in words:
        for name, ch in NAMES.items():
            if w in (name, name[2:]) and ch not in out:
                out.append(ch)
    return "".join(out)


def sentence_after(text: str, start: str, stop: str) -> str:
    flat = " ".join(line.removeprefix("~~").strip() for line in text.splitlines())
    i = flat.find(start)
    assert i >= 0, start
    j = flat.find(stop, i) if stop else flat.find(" ", i + len(start) + 120)
    return flat[i:j if j > 0 else i + 200]


def ladder(majhura: str, manners: list[str], mutbaqa: str,
           order: tuple[int, ...] = (0, 1, 2)) -> dict[str, Any]:
    """درجةُ الولادة والقرناء بالسُّلَّم: المخرجُ ثمّ الصفاتُ بترتيب `order` (0 الجهر، 1 الصنف،
    2 الإطباق)."""

    letters = [c for g in MAKHARIJ for c in g]
    feat = {c: (next(i for i, g in enumerate(MAKHARIJ) if c in g), int(c in majhura),
                next(i for i, g in enumerate(manners) if c in g), int(c in mutbaqa))
            for c in letters}

    def key(c: str, d: int) -> tuple:
        return (feat[c][0], *[feat[c][1 + order[i]] for i in range(d)])

    mani = [[(a, b) for a in letters for b in letters if a != b and key(a, d) == key(b, d)]
            for d in range(4)]
    wil = {c: next((d for d in range(4) if all(p[0] != c for p in mani[d])), 4) for c in letters}
    qur = {c: ["".join(b for a, b in mani[d] if a == c) for d in range(3)] for c in letters}
    return {"letters": letters, "mani": [len(m) for m in mani], "wilada": wil, "qurana": qur,
            "feat": feat}


def check_ladder(table: list[dict[str, str]], lad: dict[str, Any]) -> list[str]:
    bad = []
    if [r["harf"] for r in table] != lad["letters"]:
        bad.append("LETTER_ORDER")
    if lad["mani"] != [40, 16, 6, 0]:
        bad.append("MANI_DARAJAT")
    for r in table:
        c = r["harf"]
        if int(r["wilada"]) != lad["wilada"][c]:
            bad.append(f"WILADA:{c}")
        if [r["qurana0"], r["qurana1"], r["qurana2"]] != lad["qurana"][c]:
            bad.append(f"QURANA:{c}")
        if int(r["lif"]) != len(next(g for g in MAKHARIJ if c in g)):
            bad.append(f"LIF:{c}")
        f = lad["feat"][c]
        if (int(r["makhraj16"]), int(r["jahr"]), int(r["manner"]), int(r["itbaq"])) != f:
            bad.append(f"SIFAT:{c}")
    return bad


def dawr(before: str | None, harf: str, haraka: str) -> str:
    if haraka != "sukun":
        return "cv"
    return "v" if before is not None and (harf, before) in MADD else "c"


def hukm(mawdi: str, harf: str, haraka: str, wasl: set[tuple[str, str]]) -> tuple[str, str, str]:
    """(الحكم، أصنافُ السابق في المشروط، الشرط أو اسمُ الرفض) — مستقلٌّ عن Lean."""

    if harf == "ا" and haraka != "sukun":
        return ("marfud", "", "BARE_ALIF_OWN_MARK_NOT_LICENSED")
    if mawdi == "ibtida":
        if haraka != "sukun":
            return ("murakhkhas", "", "")
        return ("marfud", "", "INITIAL_SUKUN_WITHOUT_REPAIR")
    kind, before = mawdi.split(":")
    if kind == "waqf" and haraka != "sukun":
        return ("yuskan", "", "")
    prev = ["v", "c"] if before == "sukun" else ["cv"]
    d = dawr(before, harf, haraka)
    ok = [k for k in prev if (k, d) in wasl or (kind == "waqf" and (k, d) in WAQF)]
    if ok == prev:
        return ("murakhkhas", "", "")
    if not ok:
        return ("marfud", "", "JUNCTION_NOT_LICENSED" if kind == "wasl" else "NOT_PAUSE_LICENSED")
    if kind == "waqf":
        return ("mashrut", " ".join(ok), "PAUSE")
    if harf == "ا":
        return ("marfud", "", "CVVC_NOT_GEMINATE")
    return ("mashrut", " ".join(ok), "CVVC_NOT_GEMINATE")


def check_births(table: list[dict[str, str]], huruf: list[dict[str, str]],
                 wasl: set[tuple[str, str]] = WASL) -> list[str]:
    bad = []
    if len(table) != 1044 or [int(r["n"]) for r in table] != list(range(1044)):
        bad.append("N_RANGE")
    tower = [(r["harf"], r["haraka"]) for r in huruf]
    for r in table:
        k, m = divmod(int(r["n"]), 9)
        if int(r["k"]) != k or tower[k] != (r["harf"], r["haraka"]) or r["mawdi"] != MAWADI[m]:
            bad.append(f"N:{r['n']}")
            continue
        before = None if r["mawdi"] == "ibtida" else r["mawdi"].split(":")[1]
        if r["dawr"] != dawr(before, r["harf"], r["haraka"]):
            bad.append(f"DAWR:{r['n']}")
        if (r["hukm"], r["qabl"], r["shart"]) != hukm(r["mawdi"], r["harf"], r["haraka"], wasl):
            bad.append(f"HUKM:{r['n']}")
    return bad


def check_azwaj(azwaj: list[dict[str, str]], hm: list[dict[str, str]]) -> list[str]:
    bad = []
    if len(azwaj) != 841:
        bad.append("AZWAJ_841")
    mithl = [r for r in azwaj if r["a"] == r["b"]]
    if sorted(r["a"] for r in mithl if r["qism"] == "mithl_mumtani") != sorted("ءا") or \
            any(r["qism"] != "mithl" for r in mithl if r["a"] not in "ءا"):
        bad.append("MITHL")
    cols = ["mithl", "mithl_mumtani", "shahid_idgham", "shahid_mumtani", "maskut", "mumtani",
            "izhar"]
    for r in hm:
        for q in cols:
            if int(r[q]) != sum(1 for z in azwaj if z["a"] == r["harf"] and z["qism"] == q):
                bad.append(f"AZWAJ_COL:{r['harf']}:{q}")
    return bad


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_khatm(khatm: dict) -> list[str]:
    bad = []
    for rel, h in khatm["files"].items():
        if sha(ROOT / rel) != h:
            bad.append(f"SEAL:{rel}")
    if khatm["owner_words"] != OWNER:
        bad.append("OWNER_WORDS")
    return bad


def test_ladder_from_sealed_kitab() -> None:
    text = kitab()
    for start, stop, letters in [MAJHURA, MAHMUSA, MUTBAQA, *MANNERS[:2]]:
        # الجملُ التي تعدّ حروفَها: الحروفُ بأعيانها وبترتيبها.
        assert named(sentence_after(text, start, stop)) == letters, start
    for start, stop, letters in MANNERS[2:]:
        # جملُ الأصناف المفردة: الحرفُ مسمًّى فيها (وقد تسمّي غيرَه شبيهًا).
        assert set(letters) <= set(named(sentence_after(text, start, stop))), start
    assert set(MAJHURA[2]) | set(MAHMUSA[2]) == set(NAMES.values())
    assert not set(MAJHURA[2]) & set(MAHMUSA[2])
    lad = ladder(MAJHURA[2], [m[2] for m in MANNERS], MUTBAQA[2])
    assert check_ladder(rows(HURUF_M), lad) == []
    born = [sum(1 for c in lad["letters"] if lad["wilada"][c] == d) for d in range(4)]
    assert born == [7, 9, 7, 6]


def test_births() -> None:
    assert check_births(rows(MARJA), rows(HURUF)) == []


def test_azwaj() -> None:
    assert check_azwaj(rows(AZWAJ), rows(HURUF_M)) == []


def test_khatm() -> None:
    assert check_khatm(json.loads(KHATM.read_text(encoding="utf-8"))) == []


def test_makharij_anchored() -> None:
    path = ROOT / "tests" / "test_makharij.py"
    spec = importlib.util.spec_from_file_location("test_makharij", path)
    assert spec is not None and spec.loader is not None
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    rows = tm._rows()
    lam = tm._lam_row(rows)
    take = tm._take()
    kitab_rows = rows[:15]
    assert kitab_rows[-1][1] == [] and lam not in kitab_rows
    anchored = kitab_rows[:take] + [lam] + kitab_rows[take:]
    assert ["".join(r[1]) for r in anchored] == MAKHARIJ


# تيّارٌ مصطنع بصيغة `gen_context_certificates.generate` (الحالةُ بأسمائها هناك) — لا مصحف.
F = {
    "fi": [["ف", "كسر"], ["ي", "سكون"]],               # فِي
    "lard": [["ل", "سكون"], ["ء", "فتح"], ["ر", "سكون"], ["ض", "كسر"]],  # (ا)لْأَرْضِ موصولةً
    "hajja": [["ح", "فتح"], ["ا", "سكون"], ["ج", "سكون"], ["ج", "فتح"]],  # حَاجَّ: مثلان بعد مدّ
    "qaltu": [["ق", "فتح"], ["ا", "سكون"], ["ل", "سكون"], ["ت", "ضم"]],   # قَالْتُ: مخالفةُ H2
    "alan": [["ء", "فتح"], ["ا", "سكون"], ["ل", "سكون"], ["ء", "فتح"], ["ا", "سكون"],
             ["ن", "فتح"]],                                              # آلْآنَ: مدُّ الفرق
    "min": [["م", "كسر"], ["ن", "سكون"]],                                 # مِنْ
    "bka": [["ب", "سكون"], ["ك", "فتح"]],                                 # ساكنٌ أوّلًا بلا إصلاح
    "wa": [["و", "ضم"], ["ا", "سكون"]],                                  # وُ اْ: الألفُ الفارقة
    "qablla": [["ق", "فتح"], ["ب", "سكون"], ["ل", "سكون"], ["ل", "فتح"]],  # مثلان بلا مدٍّ: مخالفة
    "bi": [["ب", "كسر"]],                                                # كلمةٌ من خانةٍ واحدةٍ آخرًا
    "qaall": [["ق", "فتح"], ["ا", "سكون"], ["ل", "سكون"], ["ل", "سكون"]],  # مثلٌ ساكنٌ لا متحرّك
    "aabt": [["ء", "فتح"], ["ا", "سكون"], ["ب", "سكون"], ["ت", "فتح"]],    # «ءَ اْ» بلا لام: لا فرق
    "aabaalt": [["ء", "فتح"], ["ا", "سكون"], ["ب", "فتح"], ["ا", "سكون"], ["ل", "سكون"],
                ["ت", "فتح"]],                                           # لامٌ بعد مدٍّ في غير الثالثة
}
ORDER = list(F)
WUJUH = ["FARQ_ALIF_DROPPED", "MADD_DROPPED", "SAKIN_KASRA"]


def synthetic() -> dict[str, Any]:
    def e(name: str | None, last: bool, wajh: str | None = None) -> list[int]:
        return [ORDER.index(name) if name else -1, int(last), 0 if name is None else -1,
                WUJUH.index(wajh) if wajh else -1]
    lines = [
        [e("fi", False), e("lard", True, "MADD_DROPPED")],
        [e("hajja", False), e("qaltu", False), e("alan", True)],
        [e("min", False), e("lard", True, "SAKIN_KASRA")],
        [e("min", False), e("bka", True)],
        [e(None, False), e("fi", True)],
        [e("wa", False), e("lard", True, "FARQ_ALIF_DROPPED")],
        [e("min", False), e("qablla", False), e("bi", True)],
        [e("qaall", False), e("aabt", False), e("aabaalt", True)],
    ]
    return {"forms": [{"cells": F[k]} for k in ORDER], "junctions": WUJUH,
            "line_lengths": [len(x) for x in lines], "stream": [t for x in lines for t in x]}


# المتوقَّعُ باليد ولادةً ولادة على السطر المصلَح.
EXPECTED = [
    ("ف", "kasra", "ibtida"), ("ل", "sukun", "wasl:kasra"), ("ء", "fatha", "wasl:sukun"),
    ("ر", "sukun", "wasl:fatha"), ("ض", "kasra", "waqf:sukun"),
    ("ح", "fatha", "ibtida"), ("ا", "sukun", "wasl:fatha"), ("ج", "sukun", "wasl:sukun"),
    ("ج", "fatha", "wasl:sukun"), ("ق", "fatha", "wasl:fatha"), ("ا", "sukun", "wasl:fatha"),
    ("ل", "sukun", "wasl:sukun"), ("ت", "damma", "wasl:sukun"), ("ء", "fatha", "wasl:damma"),
    ("ا", "sukun", "wasl:fatha"), ("ل", "sukun", "wasl:sukun"), ("ء", "fatha", "wasl:sukun"),
    ("ا", "sukun", "wasl:fatha"), ("ن", "fatha", "waqf:sukun"),
    ("م", "kasra", "ibtida"), ("ن", "kasra", "wasl:kasra"), ("ل", "sukun", "wasl:kasra"),
    ("ء", "fatha", "wasl:sukun"), ("ر", "sukun", "wasl:fatha"), ("ض", "kasra", "waqf:sukun"),
    ("م", "kasra", "ibtida"), ("ن", "sukun", "wasl:kasra"), ("ب", "sukun", "wasl:sukun"),
    ("ك", "fatha", "waqf:sukun"),
    ("ي", "sukun", "waqf:kasra"),
    ("و", "damma", "ibtida"), ("ل", "sukun", "wasl:damma"), ("ء", "fatha", "wasl:sukun"),
    ("ر", "sukun", "wasl:fatha"), ("ض", "kasra", "waqf:sukun"),
    ("م", "kasra", "ibtida"), ("ن", "sukun", "wasl:kasra"), ("ق", "fatha", "wasl:sukun"),
    ("ب", "sukun", "wasl:fatha"), ("ل", "sukun", "wasl:sukun"), ("ل", "fatha", "wasl:sukun"),
    ("ب", "kasra", "waqf:fatha"),
    ("ق", "fatha", "ibtida"), ("ا", "sukun", "wasl:fatha"), ("ل", "sukun", "wasl:sukun"),
    ("ل", "sukun", "wasl:sukun"), ("ء", "fatha", "wasl:sukun"), ("ا", "sukun", "wasl:fatha"),
    ("ب", "sukun", "wasl:sukun"), ("ت", "fatha", "wasl:sukun"), ("ء", "fatha", "wasl:fatha"),
    ("ا", "sukun", "wasl:fatha"), ("ب", "fatha", "wasl:sukun"), ("ا", "sukun", "wasl:fatha"),
    ("ل", "sukun", "wasl:sukun"), ("ت", "fatha", "waqf:sukun"),
]
EXPECTED_H2 = [  # (السطر، الكلمة، j، الحرف، مخالف؟)
    (1, 0, 2, "ج", False), (1, 1, 2, "ل", True), (1, 2, 2, "ل", False), (6, 1, 2, "ل", True),
    (7, 0, 2, "ل", True), (7, 0, 3, "ل", True), (7, 1, 2, "ب", True), (7, 2, 4, "ل", True)]
EXPECTED_SEAM = {("ف", "ل"): 1, ("ج", "ق"): 1, ("ت", "ء"): 2, ("ن", "ل"): 1, ("ن", "ب"): 1,
                 ("و", "ل"): 1, ("ن", "ق"): 1, ("ل", "ب"): 1, ("ل", "ء"): 1}
EXPECTED_EXTRA = {"wajh:MADD_DROPPED": 1, "wajh:SAKIN_KASRA": 1, "wajh:FARQ_ALIF_DROPPED": 1,
                  "hadd_sakin_ba3d_sakin": 1}
EXPECTED_SKIPPED = {"REFUSED_TOKEN": 1, "LEFT_REFUSED": 1}


def load_tool(src: str) -> types.ModuleType:
    mod = types.ModuleType("gen_marja_under_test")
    mod.__dict__["__file__"] = str(TOOL)
    exec(compile(src, str(TOOL), "exec"), mod.__dict__)  # noqa: S102 — أداةُ المستودع نفسُها
    return mod


def check_tool(mod: types.ModuleType) -> list[str]:
    seen, skipped, mashrut, inside, seam, extra = mod.births(synthetic())
    bad = []
    if seen != Counter(EXPECTED):
        bad.append("BIRTHS")
    if [(m["satr"], m["kalima"], m["j"], m["harf"], mod.h2_mukhalif(m)) for m in mashrut] != \
            EXPECTED_H2:
        bad.append("H2_SITES")
    if dict(seam) != EXPECTED_SEAM:
        bad.append("SEAM")
    if sum(inside.values()) != 39:
        bad.append("INSIDE")
    if dict(extra) != EXPECTED_EXTRA:
        bad.append("EXTRA")
    if dict(skipped) != EXPECTED_SKIPPED:
        bad.append("SKIPPED")
    return bad


def test_births_tool_synthetic() -> None:
    assert check_tool(load_tool(TOOL.read_text(encoding="utf-8"))) == []


def test_shahid_consistent() -> None:
    if not SHAHID.exists():
        # الشاهدُ في إيداعٍ بعد التسجيل المسبق (STEP-0013)؛ التخطّي معلَّقٌ بالبايتات لا بمتغيّر.
        pytest.skip("SHAHID_NOT_YET_DEPOSITED")
    s = json.loads(SHAHID.read_text(encoding="utf-8"))
    assert s["prereg_sha256"] == sha(PREREG)
    assert s["marja_sha256"] == sha(MARJA) and s["azwaj_sha256"] == sha(AZWAJ)
    assert s["tool_sha256"] == sha(TOOL)
    assert sum(b["count"] for b in s["births"]) == s["cells_counted"]
    assert s["H1"]["violations"] == len(s["H1"]["list"])
    assert s["H2"]["violations"] == len(s["H2"]["list"])
    licensed = [r for r in rows(MARJA) if r["hukm"] in ("murakhkhas", "mashrut")]
    assert s["births_licensed"] == len(licensed)
    assert s["births_licensed_unattested"] == len(s["unattested"])
    law = {int(r["n"]): r for r in rows(MARJA)}
    assert all(law[b["n"]]["harf"] == b["harf"] and law[b["n"]]["mawdi"] == b["mawdi"]
               for b in s["births"])
    assert not {b["n"] for b in s["births"]} & {u["n"] for u in s["unattested"]}


def test_theorems_named_and_audited() -> None:
    src = LEAN.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    for t in THEOREMS:
        assert f"theorem {t}" in src, t
        assert f"#print axioms A116.Marja.{t}\n" in audit, t
    assert "sorry" not in src and "native_decide" not in src and "\naxiom " not in src


def test_mutants_rejected() -> None:
    table, huruf, hm = rows(MARJA), rows(HURUF), rows(HURUF_M)
    assert check_births(table, huruf, WASL | {("c", "c")}), "MUTANT_WASL_CC"
    lad = ladder(MAJHURA[2], [m[2] for m in MANNERS], MUTBAQA[2], order=(1, 0, 2))
    assert check_ladder(hm, lad), "MUTANT_LADDER_ORDER"
    target = next(r["n"] for r in table if r["hukm"] == "yuskan")
    flipped = [dict(r, hukm="murakhkhas", shart="") if r["n"] == target else r for r in table]
    assert check_births(flipped, huruf), "MUTANT_CSV_HUKM_FLIP"
    khatm = json.loads(KHATM.read_text(encoding="utf-8"))
    rel = next(iter(khatm["files"]))
    khatm["files"][rel] = ("0" if khatm["files"][rel][0] != "0" else "1") + khatm["files"][rel][1:]
    assert check_khatm(khatm), "MUTANT_SEAL_BYTE"
    lad2 = ladder(MAJHURA[2].replace("ق", ""), [m[2] for m in MANNERS], MUTBAQA[2])
    assert check_ladder(hm, lad2), "MUTANT_HAND_MAJHURA"
    src = TOOL.read_text(encoding="utf-8")
    for name, a, b in [
        ("MUTANT_TOOL_SEAM_IN_H2", "if sakin2 and j == 0:", "if sakin2 and j < 0:"),
        ("MUTANT_TOOL_NO_ISLAH", "line[i - 1] = islah(left, wujuh[jw])", "line[i - 1] = left"),
        ("MUTANT_TOOL_NO_MADD_IN_H2",
         'return not (m["madd_before"] and (m["geminate"] or m["farq"]))',
         'return not (m["geminate"] or m["farq"])'),
        ("MUTANT_TOOL_MADD_ALWAYS", "madd = ante is not None and (before[0], ante[1]) in MADD",
         "madd = True"),
        ("MUTANT_TOOL_GEMINATE_SAKIN", 'nxt[0] == c and nxt[1] != "sukun"', "nxt[0] == c"),
        ("MUTANT_TOOL_FARQ_ANY_LETTER", 'tuple(w[:2]) == FARQ and c == "ل"',
         "tuple(w[:2]) == FARQ"),
        ("MUTANT_TOOL_FARQ_ANY_POS", 'farq = j == 2 and tuple(w[:2])', "farq = tuple(w[:2])"),
        ("MUTANT_TOOL_ONE_CELL_WASL",
         'mawdi = "waqf" if (last_word and exit_ == 1 and len(w) == 1) else "wasl"',
         'mawdi = "wasl"'),
    ]:
        assert src.count(a) == 1, name
        assert check_tool(load_tool(src.replace(a, b))), name


if __name__ == "__main__":
    test_ladder_from_sealed_kitab()
    test_births()
    test_azwaj()
    test_khatm()
    test_makharij_anchored()
    test_births_tool_synthetic()
    test_shahid_consistent()
    test_theorems_named_and_audited()
    test_mutants_rejected()
    print("9/9")
