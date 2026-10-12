"""عقدُ الشرح (ADR ٤٤): لكلّ صورةٍ أسطرٌ (الدعوى، القيمة، الوحدة) بوسم دعواها ومرساتها من السجلّ بعينه.

التوقّعاتُ مكتوبةٌ باليد من قوانين القرّاء لا من شيفرة العقد:
- فِيْ حرفٌ (`Qiraa.harf_no_hukm`): سطرُ «حرف» فيها، ولا سطرَ جذرٍ ولا حكم؛ وكَتَبَ لا حرفَ فيها
  وجذرُها ك ت ب مشهودٌ في المقاييس، فلها سطرُ جذرٍ وسطرُ حكم.
- عَلَى وعَلَا خاناتٌ واحدة (`cells_forget_rank`)، فأسطرُهما بلا عدد الشهادة واحدة؛ ويفرّقهما سطرُ `CERT-n`
  بعددَيهما من المودَع (الرتبةُ 1 لعَلَى و0 لعَلَا — الغانم `ala_alaa`).
- أوّلُ سطرٍ عددُ الخانات، والقيمُ أعدادٌ وأسماءٌ وأحكام لا نصّ: لا قيمةَ نصّيّةٌ هي الكلمةُ نفسُها.
- الطفراتُ تُرفض بأسمائها: دعوى ليست في السجلّ، ووحدةٌ خارج المفردات، ودعوى معلَّقة.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

from slge.cells import Cell
from slge.rawabit import cells_of
from slge.sharh import UNITS, Line, anchor, breaches, lines, tag
from slge.status import LEDGER, Status

Word = tuple[Cell, ...]
DATA = Path(__file__).resolve().parent / "data"


def claims(ls: tuple[Line, ...]) -> list[str]:
    return [ln.claim for ln in ls]


def test_particle_blocks_root_and_judgement_verb_carries_both() -> None:
    fi = lines(cells_of("فِيْ"))
    assert fi[0] == Line("ENTRY", 2, "خانة")
    assert Line("QIRAA-reader", "حرف", "صنف") in fi
    assert "MAQAYIS-member" not in claims(fi) and "HUKM-judge" not in claims(fi)
    kataba = lines(cells_of("كَتَبَ"))
    assert kataba[0] == Line("ENTRY", 3, "خانة")
    assert Line("QIRAA-reader", "حرف", "صنف") not in kataba
    roots = [ln.value for ln in kataba if ln.claim == "MAQAYIS-member"]
    assert roots == [("ك", "ت", "ب", True)]
    assert "HUKM-judge" in claims(kataba)
    assert breaches(fi) == [] and breaches(kataba) == []


def test_ala_alaa_differ_only_by_certificate_number() -> None:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        forms = json.load(f)["forms"]
    pair = [x for x in forms if x["cells"] == [["ع", "فتح"], ["ل", "فتح"], ["ا", "سكون"]]]
    ala = next(x for x in pair if x["ordinal"] == 1)  # عَلَى
    alaa = next(x for x in pair if x["ordinal"] == 0)  # عَلَا
    w1 = tuple((a, b) for a, b in ala["cells"])
    w2 = tuple((a, b) for a, b in alaa["cells"])
    assert w1 == w2  # الخاناتُ وحدَها تُسقط الرتبة
    assert lines(w1) == lines(w2)
    n1, n2 = (ala["integer"], ala["ordinal"]), (alaa["integer"], alaa["ordinal"])
    assert n1[1] == 1 and n2[1] == 0 and n1[0] != n2[0]
    l1, l2 = lines(w1, n1), lines(w2, n2)
    assert l1[1] == Line("CERT-n", n1, "عدد") and l2[1] == Line("CERT-n", n2, "عدد")
    assert [x for x in l1 if x.claim != "CERT-n"] == [x for x in l2 if x.claim != "CERT-n"]


def test_tag_and_anchor_are_the_ledgers() -> None:
    by_id = {c.claim_id: c for c in LEDGER}
    for t in ("فِيْ", "كَتَبَ", "عَلَى", "يُؤْمِنُوْنَ"):
        w = cells_of(t)
        for ln in lines(w, (0, 0)):
            assert tag(ln) == by_id[ln.claim].status.name
            assert anchor(ln) == by_id[ln.claim].support[0]
            assert ln.unit in UNITS
            assert ln.value != t  # لا نصَّ في العقد


def test_mutants_are_refused_by_name() -> None:
    suspended = next(c.claim_id for c in LEDGER if c.status is Status.معلق)
    bad = (Line("NOT-A-CLAIM", 1, "عدد"), Line("ENTRY", 1, "كلمة"), Line(suspended, 1, "عدد"))
    assert breaches(bad) == ["SHARH_CLAIM_NOT_IN_LEDGER NOT-A-CLAIM",
                             "SHARH_UNIT_NOT_IN_VOCABULARY كلمة",
                             f"SHARH_CLAIM_SUSPENDED {suspended}"]
