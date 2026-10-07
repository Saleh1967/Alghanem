"""الجهةُ الوجوديّة: التقسيمُ المغلق على الـ125، ومطابقتُه مع القوائم والقارئ، والترتيبُ لا يُسقط،
والرقمُ على المرجع.

التوقّعاتُ من كتب الصرف (فَعَلَ فعل، فَعْلٌ مصدر، فَاعِلٌ وصف، مَفْعَلٌ زمانٌ ومكان، أَفْعَالٌ
جمع، فِعْلٌ اسم) ومن وسوم MASAQ المحجوبة؛ والطفرةُ (صنفٌ سابع؛ قالبٌ بلا صنف؛ ترتيبٌ يُسقط؛
قراءةٌ بلا قوالب) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.jidh import jidh
from slge.rawabit import cells_of
from slge.wazn import AWZAN
from slge.wujud import (
    FIL,
    ISM,
    JAM,
    KIND_OF,
    MASDAR,
    ONT,
    WASF,
    ZARF,
    of_class,
    ont_of,
    ont_of_reading,
    rank,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
BY = {w.name: k for k, w in enumerate(AWZAN)}


def test_partition_is_total_and_six_fold() -> None:
    assert len(ONT) == 125 and set(ONT) == {FIL, MASDAR, WASF, ZARF, JAM, ISM}
    assert sum(len(of_class(o)) for o in (FIL, MASDAR, WASF, ZARF, JAM, ISM)) == 125
    assert ont_of(BY["فَعَلَ"]) == FIL and ont_of(BY["فَعْلٌ"]) == MASDAR and ont_of(BY["فَاعِلٌ"]) == WASF
    assert ont_of(BY["مَفْعَلٌ"]) == ZARF and ont_of(BY["أَفْعَالٌ"]) == JAM and ont_of(BY["فِعْلٌ"]) == ISM
    assert ont_of(BY["يَفْعَلُ"]) == FIL and ont_of(BY["اِفْعَلْ"]) == FIL and ont_of(BY["فَعْلَةٌ"]) == MASDAR
    assert ont_of(BY["فُعَلَاءُ"]) == JAM and ont_of(BY["فُعَيْلٌ"]) == ISM
    assert (len(of_class(FIL)), len(of_class(MASDAR)), len(of_class(WASF))) == (37, 22, 25)
    assert (len(of_class(ZARF)), len(of_class(JAM)), len(of_class(ISM))) == (7, 30, 4)
    # الطفرة: قالبٌ خارج الجدول اسمٌ لا صنفٌ سابع
    assert ont_of(125) == ISM and ont_of(-1) == ISM and set(KIND_OF) == set(ONT)


def test_closure_against_existing_lists_and_network() -> None:
    from slge.filiyya import MASDAR_TEMPLATES
    from slge.mansubat import DERIVED
    from slge.maqam import AMR_TEMPLATES, PAST_TEMPLATES, PRESENT_TEMPLATES
    from slge.shabaka import CLASSICAL, ROOT
    from slge.talil import derives

    assert set(of_class(FIL)) == set(PAST_TEMPLATES) | set(PRESENT_TEMPLATES) | set(AMR_TEMPLATES)
    assert set(of_class(MASDAR)) == set(MASDAR_TEMPLATES)
    assert set(of_class(WASF)) < set(DERIVED)
    assert set(DERIVED) - set(of_class(WASF)) == {BY["فُعَلَاءُ"]}
    assert ont_of(BY[ROOT]) == MASDAR  # أصلُ الشبكة مصدر
    names = [w.name for w in AWZAN]
    for k in (*of_class(ISM), *of_class(JAM)):  # الاسمُ والجمعُ طرفان: لا شيءَ ينحدر منهما
        assert not any(derives(q, k) for q in range(len(AWZAN))), names[k]
    for k in (*of_class(WASF), *of_class(ZARF)):  # المشتقُّ أبوه فعلٌ أو مشتقّ
        assert ont_of(BY[CLASSICAL[names[k]]]) in (FIL, WASF, ZARF), names[k]
    # الطفرة: الفعلُ ليس طرفًا — المشتقّاتُ تنحدر منه
    assert any(derives(q, BY["فَعَلَ"]) for q in range(len(AWZAN)))


def test_reader_agreement_names_its_exceptions() -> None:
    from slge.kulli import kulli
    from slge.wazn import mizan

    bad = [k for k in range(len(AWZAN)) if kulli(mizan(AWZAN[k].template)) != KIND_OF[ont_of(k)]]
    assert bad == [40, 54, 60, 62, 81, 82, 83, 86, 93, 94, 99, 108, 109, 110]
    assert AWZAN[54].name == "أَفْعَلُ" and AWZAN[83].name == "أَفْعُلٌ"  # صورةُ مضارع المتكلّم
    assert AWZAN[86].name == "فِعْلَةٌ (جمع)" and AWZAN[93].name == "فِعَالٌ (جمع)"


def test_reading_ontology_and_rank_drop_nothing() -> None:
    rs = jidh(cells_of("فَرِيقٌ"))
    assert [ont_of_reading(r) for r in rs] == [WASF, ISM]
    assert [ont_of_reading(r) for r in rank(ISM, rs)] == [ISM, WASF]
    assert set(rank(ISM, rs)) == set(rs) and len(rank(FIL, rs)) == 2
    assert {ont_of_reading(r) for r in jidh(cells_of("قَالَ"))} == {FIL}
    assert [ont_of_reading(r) for r in jidh(cells_of("بِكِتَابِهِمْ"))] == [MASDAR]  # فِعَال: مصدرٌ أو اسم
    assert rank(FIL, ()) == ()


def test_numbers_on_the_deposit_and_masaq() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_wujud_index import measure

    F = FIL
    m = measure()
    assert m["forms"] == 18179 and sum(m["dist"].values()) == 18179 and m["dist"]["—"] == 2669
    assert m["dist"][F] == 7250 and m["masaq"] == 25799 and m["none"] == 1952
    b, a = m["before"], m["after"]
    assert sum(b.values()) == sum(a.values()) == 23847
    assert b[(F, F)] == 6817 and a[(F, F)] == 6804  # الفعلُ 83.4% ← 83.3% بترتيب الأداة
    hit_b = sum(b[(g, g)] for g in ("فعل", "مصدر", "وصف", "اسم"))
    hit_a = sum(a[(g, g)] for g in ("فعل", "مصدر", "وصف", "اسم"))
    assert hit_b == 12456 and hit_a == 12487  # 52.2% ← 52.4%
    gen = str(ROOT_DIR / "tools" / "gen_wujud_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
