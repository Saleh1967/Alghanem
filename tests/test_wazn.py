"""الوزن: التوقّعاتُ من قانون الميزان لا من شيفرته، مطعَّمةٌ بالطفرة، وهياكلُه مقيسةٌ على سيبويه."""

from __future__ import annotations

import csv
import hashlib
import unicodedata
from collections import Counter
from itertools import product
from pathlib import Path

import pytest

from slge.cells import ALPHABET, STATES, licensed
from slge.wazn import AWZAN, DEBTS, FAL, MASDAR_OF, Sym, fill, mizan, parse, root_of, states_of

SUKUN = STATES[3]
ROOTS = ("كتب", "خرج", "ءمن", "مدد", "قول", "وعد", "رمي")
SIBAWAYH = Path(__file__).parent / "data" / "sibawayh-abniya.tsv"
SIBAWAYH_SHA = "678ca5144698b571a42804b19b8d1680766df7f2339cf6c9c53d84994051fdd9"


def test_fill_then_root_of_recovers_every_root() -> None:
    for w in AWZAN:
        for root in ROOTS:
            word = fill(w.template, root)
            assert root_of(w.template, word) == tuple(root), (w.name, root)
            assert len(word) == len(w.template)


def test_licence_is_root_independent() -> None:
    """`licensed_fill_indep`: الحالاتُ من القالب وحدَه، فالحكمُ واحدٌ لكلّ الأصول."""

    for w in AWZAN:
        verdicts = {licensed(fill(w.template, r)) for r in ROOTS}
        assert verdicts == {True}, w.name
        assert all(tuple(s for _, s in fill(w.template, r)) == states_of(w.template) for r in ROOTS)


def test_mutating_one_state_can_unlicense_but_never_changes_the_root() -> None:
    """طفرة: تسكينُ خانتين متجاورتين يُسقط الترخيصَ ولا يمسّ الأصل."""

    t = parse("فَعَلَ")
    mutant = (Sym(0, None, STATES[0]), Sym(1, None, SUKUN), Sym(2, None, SUKUN))
    assert not licensed(fill(mutant, "كتب")) and licensed(fill(t, "كتب"))
    assert root_of(mutant, fill(mutant, "كتب")) == ("ك", "ت", "ب")


def test_parse_refuses_what_the_gate_refuses() -> None:
    with pytest.raises(ValueError):
        parse("فعل")  # بلا حركات: لا يُخمَّن
    with pytest.raises(ValueError):
        parse("فَعَلَx")
    assert parse("اِفْعَلْ")[0] == Sym(None, "ء", STATES[1])  # همزةُ الوصل همزةٌ بحركتها
    assert parse("فَعَّلَ")[1:3] == (Sym(1, None, SUKUN), Sym(1, None, STATES[0]))  # الشدّة خانتان
    assert parse("فَاعِلُ")[1] == Sym(None, "ا", SUKUN)  # الألفُ لا تتحرّك
    assert parse("فَعْلَةُ")[-1] == Sym(None, "ت", STATES[2])  # التاءُ المربوطة تاء


def test_root_of_refuses_wrong_length_or_missing_slot() -> None:
    t = parse("فَعَلَ")
    assert root_of(t, fill(t, "كتب")[:2]) is None
    two = (Sym(0, None, STATES[0]), Sym(1, None, STATES[0]))
    assert root_of(two, (("ك", STATES[0]),) * 2) is None


def test_every_wazn_distinct_as_cells_and_names_unique() -> None:
    names = [w.name for w in AWZAN]
    assert len(set(names)) == len(names)
    forms = Counter(mizan(w.template) for w in AWZAN)
    dup = {k: v for k, v in forms.items() if v > 1}
    # الصورةُ الواحدة قد تكون في بابين (فِعَالٌ مصدرًا وجمعًا؛ مِفْعَالٌ مبالغةً وآلة): تعدّدٌ معلَن، لا خطأ
    assert sorted(dup.values()) == [2, 2, 2, 3], dup


def test_masdar_of_mazid_is_a_declared_pair_of_deposited_awzan() -> None:
    names = {w.name for w in AWZAN}
    for verb, masdar in MASDAR_OF.items():
        assert verb in names and masdar in names


def test_skeletons_measured_against_sibawayh() -> None:
    """هياكلُ الأوزان (حروفًا بلا حركات) مقابل أبنية سيبويه المجمَّدة: 103 من 121 مذكورةٌ عنده؛
    والـ18 الباقيةُ مسمّاةٌ: الأمرُ والمصدرُ القياسيُّ للمزيد وبعضُ المشتقّات والجموع ليست في
    أبواب الأبنية؛ و122 من هياكله الـ158 خارج الجدول (الجدولُ يصيب 36 هيكلًا بـ103 أوزانٍ مشكولة؛
    وأكثرُ الباقي رباعيٌّ ونادر): دَين."""

    raw = SIBAWAYH.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SIBAWAYH_SHA
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines(), delimiter="\t"))
    skeletons = {r["skeleton"] for r in rows}
    assert len(skeletons) == 158 and len({r["token"] for r in rows}) == 163

    def key(name: str) -> str:
        t = "".join(c for c in name.split(" ")[0] if unicodedata.category(c) != "Mn")
        t = t.replace("ة", "").replace("ى", "ا")
        return t.replace("أ", "ء").replace("إ", "ء")

    hit = [w.name for w in AWZAN if key(w.name) in skeletons]
    miss = [w.name for w in AWZAN if key(w.name) not in skeletons]
    assert len(hit) == 103 and len(miss) == 18, miss
    assert len(skeletons - {key(w.name) for w in AWZAN}) == 122


def test_debts_are_named() -> None:
    assert len(DEBTS) == 5 and any("الرباعيُّ" in d for d in DEBTS)


@pytest.mark.parametrize("root", ["".join(p) for p in product(ALPHABET[:3], repeat=3)])
def test_small_root_sweep(root: str) -> None:
    t = parse("مُسْتَفْعِلُ")
    assert root_of(t, fill(t, root)) == tuple(root) and licensed(fill(t, root))
    assert mizan(t) == fill(t, FAL)
