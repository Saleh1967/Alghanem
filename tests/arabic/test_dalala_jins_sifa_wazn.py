"""شاهدان على `formal/a116/A116/Dalala.lean` (الدلالات الثلاث بين الجنس والصفة والوزن).

١. **الاقتباسُ من المودَع لا من الذاكرة:** كلُّ نصٍّ بين «» في Dalala.lean يقع
   بحروفه (بعد نزع الحركات والتطويل وعلامات الترقيم) في ملفّ الشخصية ج٣ المودَع
   في جذر المستودع، وبصمةُ الملفّ هي المذكورةُ في رأس الوحدة. والنفيُ المذكور في
   الرأس («لا ترد الفصل ولا العرض العام ولا الكلّيات في مباحث اللغة») مفحوصٌ هنا.
   الطفرةُ المرفوضة: اقتباسٌ مُختلَق (`QUOTE_NOT_IN_DEPOSIT`).

٢. **مرآةٌ مستقلّة:** إعادةُ كتابة التعريفات بالبايثون على جداول عشوائية، وفحصُ
   الخواصّ كما نُصّت في Lean (لا أرقامٌ محسوبةٌ بالشيفرة المفحوصة). ولكلّ طفرةٍ
   مسمّاةٍ خاصيّةٌ يجب أن تُسقطها.

الوسم: «مفحوص» لا «مطابَق» — لا جدولَ مولَّدٌ من Lean هنا.
"""

from __future__ import annotations

import hashlib
import itertools
import random
import re
import unicodedata
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOCX = ROOT / "الشخصية الاسلامية الجزء الثالث ورد (2).docx"
LEAN = ROOT / "formal" / "a116" / "A116" / "Dalala.lean"
DOCX_SHA256 = "360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd"

_DIACRITICS = re.compile("[ً-ْٰـ]")
_NON_LETTER = re.compile(r"[^\w]+")


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = _DIACRITICS.sub("", text)
    return " ".join(_NON_LETTER.sub(" ", text).split())


def _docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    paragraphs = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
    return "\n".join(
        "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in paragraphs
    )


@pytest.fixture(scope="module")
def source() -> str:
    return _docx_text(DOCX)


def _lean_quotes() -> list[str]:
    return sorted(set(re.findall(r"«([^»]+)»", LEAN.read_text(encoding="utf-8"))))


def test_deposit_fingerprint_matches_header() -> None:
    assert hashlib.sha256(DOCX.read_bytes()).hexdigest() == DOCX_SHA256
    assert DOCX_SHA256 in LEAN.read_text(encoding="utf-8")


def _in_order(corpus: str, quote: str) -> bool:
    """«…» علامةُ حذف: تقع القطعُ كلُّها بترتيبها، ولا شيءَ يُحذف من داخل قطعة."""

    pos = 0
    for piece in (_norm(p) for p in quote.split("…")):
        if not piece:
            continue
        pos = corpus.find(piece, pos)
        if pos < 0:
            return False
        pos += len(piece)
    return True


def test_every_quote_is_in_the_deposit(source: str) -> None:
    """كلُّ ما بين «» نصٌّ من الكتاب بلا استثناء؛ وغيرُه في الوحدة بين “”."""

    corpus = _norm(source)
    quotes = _lean_quotes()
    assert len(quotes) >= 30
    missing = [q for q in quotes if not _in_order(corpus, q)]
    assert missing == [], f"QUOTE_NOT_IN_DEPOSIT: {missing}"


def test_fabricated_quote_is_rejected(source: str) -> None:
    corpus = _norm(source)
    for fabricated in ("والفصل هو الناطق", "الخاصة هي الضاحك", "السبب إطلاق اللفظ"):
        assert not _in_order(corpus, fabricated)


def test_header_absence_claims(source: str) -> None:
    norm = _norm(source)
    # من أوّل متن المبحث [721] إلى عنوان ما بعده [1108]؛ لا من الفهرس.
    start = norm.index(_norm("اللغات هي عبارة عن الألفاظ الموضوعة للمعاني"))
    end = norm.index(_norm("أقسام الكتاب والسنة"), start)
    section = norm[start:end]
    for absent in ("الفصل", "العرض العام", "الكليات"):
        assert _norm(absent) not in section, absent
    # «الخاصة» لا ترد إلا في الفقرة [886] (الحقيقة العرفية الخاصة).
    p886 = section.index(_norm("وأما ما لكل طائفة من العلماء"))
    p888 = section.index(_norm("الألفاظ المنقولة"), p886)
    hits = [m.start() for m in re.finditer(_norm("الخاصة"), section)]
    assert hits and all(p886 <= h < p888 for h in hits)


# ---------------------------------------------------------------- المرآة

JINS, DHU = "jins", "dhuSifa"
DHAT = ("dhat",)


def juz(T, c, m, *, mutant=None):
    kind, g = c
    if kind == JINS:
        if m[0] == "atom":
            return (g, m[1]) in T["mahiya"]
        if m[0] == "sifa":
            return mutant == "M1"
        return False
    if m == DHAT:
        return True
    if m[0] == "sifa":
        return True if mutant == "M6" else m[1] == g
    return (g, m[1]) in T["dhusifa"]


def tadammun(T, w, m, mutant=None):
    c = T["wad"].get(w)
    return c is not None and juz(T, c, m, mutant=mutant)


def iltizam(T, w, m, mutant=None):
    c = T["wad"].get(w)
    if c is None:
        return False
    lz = (c, m) in T["dhihni"] or (mutant == "M3" and (c, m) in T["khariji"])
    if mutant == "M2":
        return lz
    return lz and not juz(T, c, m, mutant=mutant)


def rand_table(rng, G, A, W):
    musamma = [(k, g) for k in (JINS, DHU) for g in G]
    mana = [DHAT] + [("sifa", g) for g in G] + [("atom", a) for a in A]
    pick = lambda xs, ys, p: {(x, y) for x in xs for y in ys if rng.random() < p}  # noqa: E731
    wad = {w: rng.choice(musamma) for w in W if rng.random() < 0.8}
    return {
        "wad": wad,
        "mahiya": pick(G, A, 0.3),
        "dhusifa": pick(G, A, 0.2),
        "dhihni": pick(musamma, mana, 0.15),
        "khariji": pick(musamma, mana, 0.15),
        "mana": mana,
    }


def section1_failures(T, mutant=None):
    fails = []
    for w, m in itertools.product(list(T["wad"]) + ["unset"], T["mana"]):
        t, i = tadammun(T, w, m, mutant), iltizam(T, w, m, mutant)
        if (t or i) and w not in T["wad"]:
            fails.append("no_wad_no_dalala")
        if t and i:
            fails.append("tadammun_iltizam_disjoint")
        c = T["wad"].get(w)
        if c and (c, m) in T["khariji"] and (c, m) not in T["dhihni"] and i:
            fails.append("khariji_alone_no_iltizam")
        if c and c[0] == JINS and m[0] == "sifa" and t:
            fails.append("jins_no_sifa_part")
        if c and c[0] == DHU and m[0] == "sifa" and t and m[1] != c[1]:
            fails.append("mushtaqq_sifa_unique")
        if c and c[0] == DHU and not (tadammun(T, w, ("sifa", c[1]), mutant)):
            fails.append("mushtaqq_tadammun")
    return fails


def tad_s(S, t, r, part, mutant=None):
    h, g = S["hayaa"].get(t), S["madda"].get(r)
    if part[0] == "hayaa":
        ok = h == part[1] and g is not None
        return ok and (mutant != "M4" or r == S["roots"][0])
    ok = g == part[1] and h is not None
    return ok and (mutant != "M7" or h == "masdar")


def ism_of(S, t, r, mutant=None):
    h, g = S["hayaa"].get(t), S["madda"].get(r)
    if h is None or g is None:
        return None
    if h == "masdar":
        return (JINS, g)
    if h.startswith("mushtaqq"):
        return (JINS, g) if mutant == "M5" else (DHU, g)
    return None


def section3_failures(S, G, mutant=None):
    fails = []
    T, R = S["templates"], S["roots"]
    hs = set(S["hayaa"].values())
    for t, r1, r2 in itertools.product(T, R, R):
        for h in hs:
            if tad_s(S, t, r1, ("hayaa", h), mutant) and S["madda"].get(r2) is not None:
                if not tad_s(S, t, r2, ("hayaa", h), mutant):
                    fails.append("hayaa_part_uniform")
    for t1, t2, r in itertools.product(T, T, R):
        for g in G:
            if tad_s(S, t1, r, ("hadath", g), mutant) and S["hayaa"].get(t2) is not None:
                if not tad_s(S, t2, r, ("hadath", g), mutant):
                    fails.append("hadath_part_uniform")
    for tm, td, r in itertools.product(T, T, R):
        g = S["madda"].get(r)
        if g is None or S["hayaa"].get(tm) != "masdar":
            continue
        if not str(S["hayaa"].get(td)).startswith("mushtaqq"):
            continue
        Tbl = {"wad": {("m", r): ism_of(S, tm, r, mutant), ("d", r): ism_of(S, td, r, mutant)},
               "mahiya": set(), "dhusifa": set()}
        if Tbl["wad"][("m", r)] != (JINS, g):
            fails.append("sifa_of_mushtaqq_is_jins_of_masdar")
        if not (Tbl["wad"][("d", r)] and juz(Tbl, Tbl["wad"][("d", r)], ("sifa", g))):
            fails.append("sifa_of_mushtaqq_is_jins_of_masdar")
    return fails


def rand_sigha(rng, G):
    templates = [f"t{i}" for i in range(6)]
    roots = [f"r{i}" for i in range(5)]
    choices = ["masdar", "mushtaqq.faail", "mushtaqq.mafuul", "zaman.madi", None]
    hayaa = {t: h for t in templates if (h := rng.choice(choices)) is not None}
    madda = {r: rng.choice(G) for r in roots if rng.random() < 0.8}
    return {"templates": templates, "roots": roots, "hayaa": hayaa, "madda": madda}


G_, A_, W_ = list("abcd"), list("xyz"), [f"w{i}" for i in range(6)]
N = 400


def test_mirror_properties_hold_on_random_tables() -> None:
    rng = random.Random(1967)
    for _ in range(N):
        assert section1_failures(rand_table(rng, G_, A_, W_)) == []
        assert section3_failures(rand_sigha(rng, G_), G_) == []


@pytest.mark.parametrize(
    ("mutant", "section", "expected"),
    [
        ("M1", 1, "jins_no_sifa_part"),
        ("M2", 1, "tadammun_iltizam_disjoint"),
        ("M3", 1, "khariji_alone_no_iltizam"),
        ("M6", 1, "mushtaqq_sifa_unique"),
        ("M4", 3, "hayaa_part_uniform"),
        ("M5", 3, "sifa_of_mushtaqq_is_jins_of_masdar"),
        ("M7", 3, "hadath_part_uniform"),
    ],
)
def test_named_mutant_is_rejected(mutant: str, section: int, expected: str) -> None:
    rng = random.Random(1967)
    seen: set[str] = set()
    for _ in range(N):
        if section == 1:
            seen.update(section1_failures(rand_table(rng, G_, A_, W_), mutant))
        else:
            seen.update(section3_failures(rand_sigha(rng, G_), G_, mutant))
    assert expected in seen
