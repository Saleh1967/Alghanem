"""القرينةُ المعجميّة: المودَعُ مختوم، والعضويّةُ على الخانات، والترتيبُ لا يُسقط قراءة، والرقمُ قبلُ وبعدُ.

التوقّعاتُ من المصدر المختوم (`maqayis_by_root_csv_999.csv`: 4,576 صفًّا، 4,565 جذرًا، 3 رباعيّة) ومن
الجدول اليدويّ (كتب، قول، قيل، رمى في المقاييس؛ ذبو، ككك ليست) ومن قسمة MASAQ المحجوبة، والطفرةُ
(جذرٌ غيرُ مشهود؛ معتلّةٌ على غير الواو والياء؛ ترتيبٌ يُسقط أو يزيد) تُرفَض.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from pathlib import Path

from slge.cells import ALPHABET
from slge.jidh import jidh
from slge.maqayis import ROOTS, SHA256, WEAK, attested, decode, member, rank, roots_of
from slge.rawabit import cells_of

ROOT_DIR = Path(__file__).resolve().parent.parent
DEPOSIT = ROOT_DIR / "tests" / "data" / "maqayis-roots.json.gz"


def test_deposit_is_sealed_and_the_table_is_generated_from_it() -> None:
    with gzip.open(DEPOSIT, "rt", encoding="utf-8") as f:
        d = json.load(f)
    assert d["sha256"] == SHA256
    assert SHA256 == "2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0"
    assert d["rows"] == 4576 and d["distinct_roots"] == 4565 and d["triliteral"] == 4562
    assert sorted(d["skipped_quadriliteral"]) == ["ثأثأ", "جأجأ", "جهجه"]
    assert d["weak_code"] == WEAK == 29 and d["alphabet"] == "".join(ALPHABET)
    assert tuple(d["codes"]) == ROOTS and len(ROOTS) == 4561 == len(set(ROOTS))
    assert list(ROOTS) == sorted(ROOTS)
    assert all(max(decode(n)) <= 29 for n in ROOTS)
    assert hashlib.sha256(json.dumps(d["codes"]).encode()).hexdigest() == hashlib.sha256(
        json.dumps(list(ROOTS)).encode()).hexdigest()
    # الجدولُ في Lean مولَّدٌ من المودَع نفسه: 12 قطعةً مجموعُها 4,561
    lean = (ROOT_DIR / "formal" / "Slge" / "MaqayisTable.lean").read_text(encoding="utf-8")
    body = lean.split("def t0")[1].split("/--")[0]  # القطعُ t0…t11 قبل تعليق `table`
    nums = [int(x) for x in re.findall(r"\b(\d+)\b", body)]
    assert nums == list(ROOTS)


def test_membership_is_on_cells_and_weak_matches_waw_or_ya_only() -> None:
    assert member(("ك", "ت", "ب")) and member(("ق", "و", "ل")) and member(("ق", "ي", "ل"))
    assert member(("ر", "م", "ي")) and member(("ر", "م", "و"))  # رمى: المعتلّةُ مجهولةُ العين
    assert member(("ء", "م", "ن")) and member(("ن", "ز", "ل"))  # الهمزةُ حاملٌ كسائر الحوامل
    # الطفرة: جذرٌ ليس في المقاييس؛ وحاملٌ غيرُ و/ي في موضع المعتلّة
    assert not member(("ذ", "ب", "و")) and not member(("ك", "ك", "ك"))
    assert not member(("ر", "م", "ا"))  # الألفُ ليست أصلًا: المعتلّةُ في الطبعة أُودعت 29 لا 1
    assert not member(("ر", "م", "ت"))
    assert max(ROOTS) < 29 * 900 and decode(63) == (0, 2, 3)  # أبت


def test_rank_keeps_every_reading_and_puts_attested_first() -> None:
    kadhdhabu = cells_of("كَذَّبُو")
    rs = jidh(kadhdhabu)
    out = rank(rs)
    assert len(out) == len(rs) == 6 and set(out) == set(rs)  # `length_rank`، `mem_rank`
    assert [attested(r) for r in out] == [True] + [False] * 5
    assert roots_of(out[0]) == (("ك", "ذ", "ب"),) and out[0].al == 0
    qala = rank(jidh(cells_of("قَالَ")))
    assert [attested(r) for r in qala] == [True, True]  # قول وقيل كلاهما مشهود: لا فصل
    assert {roots_of(r)[0] for r in qala} == {("ق", "و", "ل"), ("ق", "ي", "ل")}
    jaa = rank(jidh(cells_of("جَاءَ")))
    assert [roots_of(r)[0] for r in jaa] == [("ج", "ي", "ء"), ("ج", "و", "ء")]
    assert [attested(r) for r in jaa] == [True, False]
    # الطفرة: ترتيبٌ يُسقط قراءةً أو يزيدها ليس ترتيبًا
    assert rank(()) == () and len(rank(rs[:3])) == 3
    rev = tuple(reversed(rs))
    assert rank(rev) != rev and attested(rank(rev)[0]) and rank(rev)[0] == out[0]  # المشهودُ يتقدّم
    assert sum(attested(r) for r in rank(rs)) == sum(attested(r) for r in rs)


def test_numbers_before_and_after_on_the_same_deposit() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_maqayis_index import measure

    m = measure()
    assert m["forms"] == 18179 and m["roots"] == 4561
    b, a = m["before"], m["after"]
    assert sum(b.values()) == sum(a.values()) == 15510  # لا صورةَ تسقط (كانت 14,912)
    # الأرقامُ بعد قوالب الاسم الأربعة (أ2): كانت 3,896 ← 2,895 (فُصل 1,001) و2,178 بلا قراءةٍ مشهودة؛
    # وقبل ذلك (الجذرُ من الجذع كما هو) 966 و4,347.
    assert b["2"] + b["3+"] == 4116 and a["2"] + a["3+"] == 3019  # الفصلُ 1,097
    assert a["1"] == b["1"] + 1097 and m["none_attested"] == 2238
    mb, ma = m["b"], m["a"]
    assert mb["match"] == 15475 and mb["among"] == 14118  # كانت 14,478 و13,527
    assert ma["match"] == 17533 and ma["among"] == 11349  # كانت 16,304 و11,243
    assert ma["dropped"] == 711  # كانت 458
    assert mb["match"] + mb["among"] == ma["match"] + ma["among"] + ma["dropped"]  # الذهبيُّ لا يُخفى
    assert mb["wrong"] == ma["wrong"] and mb["none"] == ma["none"]  # القرينةُ لا تُنشئ قراءة
    gen = str(ROOT_DIR / "tools" / "gen_maqayis_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
