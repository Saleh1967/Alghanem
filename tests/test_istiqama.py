"""الاستقامةُ من اللفظ والصدقُ من المودَع (`A116.Istiqama`، `A116.Sidq`، ADR ٨٨).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Istiqama.marasi` نصٌّ في سطرها بعينه (1-based) من «الكتاب» المختوم
   (JK006989، ببصمته هنا).
٢. كلماتُ كلّ شاهدٍ برسمها متواليةٌ في سطره (الواوُ متّصلةٌ بما بعدها).
٣. القسمُ بقاعدةٍ مكتوبةٍ هنا: الجملُ يفصلها العطف، والمحالُ فعلٌ وظرفٌ في جملةٍ واحدة على جانبين من «الآن»،
   والقبيحُ حرفٌ لا يليه إلّا الفعل وليه غيرُه؛ وتساوي قسمَ سيبويه المكتوبَ هنا باليد لكلّ سطر.
٤. الصدقُ بقراءةٍ مستقلّةٍ لـ`corpora/nabhani/malumat.tsv`: الشاهدُ صفٌّ ذو مرتبة، والغيابُ «لا حكم».
الطفرات: `MUTANT_NO_ATF_SPLIT`، `MUTANT_CLOSED_WORLD`، `MUTANT_TAMYIZ_SHAHID`،
`MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KITAB = ROOT / "corpora" / "kitab" / "0180Sibawayhi.KitabSibawayhi.JK006989-ara1.gz"
KITAB_SHA = "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"
LEAN = ROOT / "formal" / "a116" / "A116" / "Istiqama.lean"
MALUMAT = ROOT / "corpora" / "nabhani" / "malumat.tsv"
# قسمُ سيبويه لكلّ شاهد، باليد من الأسطر 263–267 و350.
# الاستقامةُ وحدَها: «المستقيم الكذب» مستقيمٌ حسنٌ لفظًا، و«المحال الكذب» محال.
SIBAWAYH = {"hasan": (263, "hasan"), "muhal": (264, "muhal"), "kadhib": (265, "hasan"),
            "qabih1": (266, "qabih"), "qabih2": (266, "qabih"), "muhalKadhib": (267, "muhal"),
            "hasan2": (350, "hasan")}


def kitab() -> list[str]:
    raw = gzip.decompress(KITAB.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == KITAB_SHA
    return raw.decode("utf-8").splitlines()


def lean() -> str:
    return LEAN.read_text(encoding="utf-8")


def marasi() -> list[tuple[int, str]]:
    src = lean()
    block = src[src.index("def marasi"):src.index("theorem shawahid_sinf")]
    return [(int(n), q) for n, q in re.findall(r'\((\d+), "([^"]+)"\)', block)]


def shahid(name: str) -> list[tuple[str, str]]:
    src = lean()
    m = re.search(rf"def {name} : Kalam :=\s*\[(.*?)\]\n", src, re.S)
    assert m, name
    tok = r'\("([^"]+)", \.([a-zA-Z]+(?: \.[a-zA-Z]+| "[^"]+" (?:true|false))?)\)'
    return re.findall(tok, m.group(1))


def rasm(toks: list[tuple[str, str]]) -> str:
    out, prev = "", ""
    for w, _ in toks:
        out += w if prev == "و" else (" " + w if out else w)
        prev = w
    return out


def times(c: list[str]) -> tuple[list[int], list[int]]:
    fil, zarf = [], []
    for i, f in enumerate(c):
        if f == "fil .madi":
            fil.append(-1)
        elif f == "fil .mustaqbal":
            fil.append(1)
        elif f == "fil .mudari" and i > 0 and c[i - 1].startswith("harfFil") \
                and c[i - 1].endswith("true"):
            fil.append(1)
        elif f == "zarf .ams":
            zarf.append(-1)
        elif f == "zarf .ghad":
            zarf.append(1)
    return fil, zarf


def classify(feats: list[str], split: bool = True) -> str:
    clauses: list[list[str]] = [[]]
    for f in feats:
        if f == "atf" and split:
            clauses.append([])
        elif f != "atf":
            clauses[-1].append(f)
    muhal = any(a != b for c in clauses for a in times(c)[0] for b in times(c)[1])
    qabih = any(f.startswith("harfFil")
                and (i + 1 == len(feats) or not feats[i + 1].startswith("fil"))
                for i, f in enumerate(feats))
    return "muhal" if muhal else "qabih" if qabih else "hasan"


def sidq(mawdu: str, mahmul: str, ijab: bool, closed: bool = False, tamyiz: bool = False) -> str:
    lines = MALUMAT.read_text(encoding="utf-8").splitlines()
    keys = lines[0].split("\t")
    for ln in lines[1:]:
        r = dict(zip(keys, ln.split("\t"), strict=True))
        if r["mawdu"] == mawdu and r["mahmul"] == mahmul and (r["martaba"] != "-" or tamyiz):
            return "sadiq" if (r["ijab"] == "+") == ijab else "kadhib"
    return "kadhib" if closed else "laHukm"


def test_marasi_in_sealed_kitab() -> None:
    ls, ms = kitab(), marasi()
    assert len(ms) == 12 and all(q in ls[n - 1] for n, q in ms)


def test_shawahid_in_their_lines() -> None:
    ls = kitab()
    for name, (n, _) in SIBAWAYH.items():
        assert rasm(shahid(name)) in ls[n - 1], name


def test_classes_by_independent_rule() -> None:
    for name, (_, cls) in SIBAWAYH.items():
        assert classify([f for _, f in shahid(name)]) == cls, name


def test_sidq_on_deposit() -> None:
    assert sidq("المرآة", "الانعكاس", True) == "sadiq"
    assert sidq("الدماغ", "الانعكاس", True) == "kadhib"
    assert sidq("دماغ الحيوان", "ربط المعلومات", True) == "kadhib"
    assert sidq("الجبل", "يُحمل", True) == "laHukm"
    assert sidq("التفاحة", "تؤكل", True) == "laHukm"


def test_mutants_rejected() -> None:
    assert classify([f for _, f in shahid("hasan")], split=False) != "hasan"
    assert sidq("الجبل", "يُحمل", True, closed=True) != "laHukm"
    assert sidq("التفاحة", "تؤكل", True, tamyiz=True) != "laHukm"
    ls = kitab()
    assert not all(q in ls[n] for n, q in marasi())
