"""قوالبُ الاسم على أبنية سيبويه: المودَعُ مختوم، والهيكلُ على الخانات، والقوالبُ المضافة بشرطها الثلاثيّ
(هيكلٌ عند سيبويه، حافّةٌ من أب، رقمٌ يرتفع)، والتمايزُ لا يقرأ ملءً واحدًا على أصلين نظيفين.

التوقّعاتُ من المصدر المختوم (749 صفًّا، 158 هيكلًا) ومن كتب الصرف (فِعْل/فَعَال/فُعَيْل/فَاعُول هياكلُها فعل
فعال فعيل فاعول) ومن قسمة MASAQ المحجوبة، والطفرةُ (هيكلٌ بلا أصول؛ زوجٌ غيرُ مفصول يُدَّعى فصلُه؛ أصلٌ فيه
حرفُ زيادةٍ يلتبس) تُرفَض.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from slge.abniya import (
    AMBIGUOUS,
    AUGMENTS,
    ISM,
    OUTSIDE,
    SHA256,
    SKELETONS,
    ambiguous_pairs,
    clean,
    in_abniya,
    separated,
    skeleton_of,
)
from slge.cells import ALPHABET, licensed
from slge.shabaka import CLASSICAL, apply, diff
from slge.wazn import AWZAN, fill, mizan, parse, root_of
from slge.zuruf import set_last

ROOT_DIR = Path(__file__).resolve().parent.parent
DEPOSIT = ROOT_DIR / "tests" / "data" / "sibawayh-abniya.tsv"


def test_deposit_is_sealed_and_the_tables_are_generated_from_it() -> None:
    raw = DEPOSIT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA256
    assert SHA256 == "678ca5144698b571a42804b19b8d1680766df7f2339cf6c9c53d84994051fdd9"
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines(), delimiter="\t"))
    assert len(rows) == 749 and {r["tier"] for r in rows} == {"N", "V", "P"}
    assert {tuple(ALPHABET.index(ch) for ch in r["skeleton"]) for r in rows} == set(SKELETONS)
    assert len(SKELETONS) == 158 == len(set(SKELETONS))
    lean = (ROOT_DIR / "formal" / "Slge" / "AbniyaTable.lean").read_text(encoding="utf-8")
    body = lean.split("def abniya")[1].split("]\n\n")[0]
    assert body.count("[") == 159 and "theorem abniya_length : abniya.length = 158" in lean
    # الطفرة: هيكلٌ لا أصولَ فيه ليس بناءً
    assert (20, 20, 20) not in set(SKELETONS)


def test_skeleton_is_on_cells_with_named_conventions() -> None:
    by = {w.name: w.template for w in AWZAN}
    assert skeleton_of(by["فَعَلَ"]) == (20, 18, 23)
    assert skeleton_of(by["فَعَّلَ"]) == (20, 18, 23)  # الشدّةُ حرفٌ واحد
    assert skeleton_of(by["فَعَالَةٌ"]) == (20, 18, 1, 23)  # التاءُ الأخيرةُ تُسقط
    assert skeleton_of(by["اِفْعَلْ"]) == (0, 20, 18, 23) and in_abniya(by["اِفْعَلْ"])  # وصلًا أو قطعًا
    assert in_abniya(parse("فِعْلُ")) and in_abniya(parse("فَعَالُ")) and in_abniya(parse("فَاعُولُ"))
    assert tuple(k for k in range(len(AWZAN)) if not in_abniya(AWZAN[k].template)) == OUTSIDE
    assert len(OUTSIDE) == 14 and all(AWZAN[k].name for k in OUTSIDE)
    # الطفرة: قالبٌ هيكلُه ليس عند سيبويه
    assert not in_abniya(parse("فَفَعْلُ"))


def test_added_noun_templates_satisfy_the_three_conditions() -> None:
    names = {k: AWZAN[k].name for k in ISM}
    assert list(names.values()) == ["فِعْلٌ", "فَعَالٌ", "فُعَيْلٌ", "فَاعُولٌ"]
    by = {w.name: w.template for w in AWZAN}
    for k in ISM:
        t = AWZAN[k].template
        assert in_abniya(t)  # (١) الهيكلُ عند سيبويه
        parent = CLASSICAL[AWZAN[k].name]  # (٢) حافّةٌ من أبٍ في الشبكة، بعمليّاتٍ تُفحص
        assert apply(by[parent], diff(by[parent], t)) == t
        assert licensed(mizan(t)) and root_of(t, fill(t, ("ذ", "ك", "ر"))) == ("ذ", "ك", "ر")
    assert CLASSICAL["فِعْلٌ"] == "فَعْلٌ" and CLASSICAL["فَاعُولٌ"] == "فَاعِلٌ"
    # ذِكْرٌ على فِعْل، عَذَابٌ على فَعَال، طَاغُوتٌ على فَاعُول — بعد تسوية الآخر
    from slge.jidh import stem_senses
    from slge.rawabit import cells_of

    assert 121 in stem_senses(cells_of("ذِكْرِ")) and 122 in stem_senses(cells_of("عَذَابَ"))
    assert 124 in stem_senses(cells_of("طَاغُوتِ"))
    assert 123 in stem_senses(set_last(fill(by["فُعَيْلٌ"], ("ب", "ن", "ي")), "فتح"))
    assert 121 not in stem_senses(cells_of("ذَكَرَ"))  # الطفرة: فَعَلَ ليس فِعْلًا


def test_separation_refuses_one_fill_for_two_templates_on_clean_roots() -> None:
    by = {w.name: w.template for w in AWZAN}
    assert separated(by["فِعْلٌ"], by["فَعْلٌ"]) and separated(by["فَعَالٌ"], by["فِعَالٌ"])
    assert not separated(by["فَعَلَ"], by["فَعَلٌ"]) and (0, 36) in AMBIGUOUS
    assert ambiguous_pairs() == AMBIGUOUS and len(AMBIGUOUS) == 11
    r1, r2 = ("ذ", "ك", "ر"), ("ض", "ر", "ب")
    assert clean(r1) and clean(r2)
    for k in range(len(AWZAN)):
        for q in range(k + 1, len(AWZAN)):
            if separated(AWZAN[k].template, AWZAN[q].template):
                for st in ("فتح", "كسر", "ضم", "سكون"):
                    a = set_last(fill(AWZAN[k].template, r1), st)
                    assert a != set_last(fill(AWZAN[q].template, r1), st)
                    assert a != set_last(fill(AWZAN[q].template, r2), st)
            else:
                assert (k, q) in AMBIGUOUS
    # الطفرة: أصلٌ فيه حرفُ زيادة يلتبس: فَاعَلَ (ك ا ت ب)؟ لا — بل فَعْلَلَ غيرُ مودَع؛ الشاهدُ: الياءُ أصلًا
    assert not clean(("ب", "ي", "ن")) and any(c in AUGMENTS for c in ("ب", "ي", "ن"))


def test_numbers_before_and_after_on_the_same_deposit() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_abniya_index import measure

    m = measure()
    assert m["forms"] == 18179 and m["n"] == 125 and m["in_abniya"] == 111
    # كانت 15,510 قبل زوائد سيبويه (ADR ١٨)، و14,912 قبل القوالب الأربعة
    assert m["step2"] == 15673 and m["read"] == 15673
    for k in ISM:
        assert m["with"][k] >= m["only"][k] > 0  # كلُّ قالبٍ مضاف يرفع الرقم
    assert m["only"][121] == 396 and m["only"][122] == 265  # فِعْل كانت 406 قبل زوائد سيبويه
    assert m["gold"][121] == 1197 and m["gold"][122] == 763  # فَعَال كانت 756 قبل زوائد سيبويه
    gen = str(ROOT_DIR / "tools" / "gen_abniya_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
