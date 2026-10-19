"""الإعلال والإبدال: الشواهدُ الاثنا عشر تُطبَّق وتُردّ بعينها (`*_restore`)، وصورُها مرخَّصةٌ ثلاثيًّا،
وحذفُ عين الأجوف ملزَمٌ لأنّ أصله غيرُ مرخَّص (`hadhf_ayn_forced`)، وصورُ الأفعال من المولِّد توافقها."""

from __future__ import annotations

import pytest

from gate import derive
from gate.ilal import RULES, apply, restore
from gate.licence import binary_ok, continue_licensed, kind_of, strict_licensed


def w(s: str) -> tuple[str, ...]:
    """ذرّاتٌ مفصولةٌ بمسافات: «قَ وَ لَ»."""

    return tuple(s.split())


WITNESSES: dict[str, tuple[tuple[str, ...], int, tuple[str, ...]]] = {
    # القاعدة: (الأصل، الموضع، الصورة)
    "QALB_AYN": (w("قَ وَ لَ"), 1, w("قَ اْ لَ")),  # قَوَلَ ← قَالَ
    "HADHF_AYN": (w("قَ اْ لْ تُ"), 1, w("قُ لْ تُ")),  # قَالْتُ ← قُلْتُ
    "NAQL": (w("يَ قْ وُ لُ"), 1, w("يَ قُ وْ لُ")),  # يَقْوُلُ ← يَقُولُ
    "QALB_LAM": (w("دَ عَ وَ"), 2, w("دَ عَ اْ")),  # دَعَوَ ← دَعَا
    "HADHF_LAM": (w("دَ عَ وُ وْ"), 2, w("دَ عَ وْ")),  # دَعَوُوْا ← دَعَوْا
    "HADHF_WAW": (w("يَ وْ عِ دُ"), 1, w("يَ عِ دُ")),  # يَوْعِدُ ← يَعِدُ
    "HAMZA_MADD": (w("ءَ ءْ مَ نَ"), 1, w("ءَ اْ مَ نَ")),  # آمَنَ
    "TA_TTA": (w("ءِ صْ تَ بَ رَ"), 2, w("ءِ صْ طَ بَ رَ")),  # اصْطَبَرَ
    "TA_DAL": (w("ءِ زْ تَ اْ دَ"), 2, w("ءِ زْ دَ اْ دَ")),  # ازْدَادَ
    "FA_TA": (w("ءِ وْ تَ صَ لَ"), 1, w("ءِ تْ تَ صَ لَ")),  # اتَّصَلَ
    "WAW_YA": (w("مِ وْ زَ اْ نُ"), 1, w("مِ يْ زَ اْ نُ")),  # مِيزَانُ
    "YA_WAW": (w("مُ يْ قِ نُ"), 1, w("مُ وْ قِ نُ")),  # مُوقِنُ
}


def test_witness_table_covers_every_rule() -> None:
    assert set(WITNESSES) == set(RULES)


@pytest.mark.parametrize("rule", RULES)
def test_apply_then_restore_is_identity(rule: str) -> None:
    source, i, expected = WITNESSES[rule]
    surface, record = apply(rule, source, i)
    assert surface == expected, rule
    assert restore(surface, record) == source, rule


@pytest.mark.parametrize("rule", RULES)
def test_surface_is_continue_licensed(rule: str) -> None:
    _, _, surface = WITNESSES[rule]
    assert continue_licensed(kind_of(surface)), rule
    assert strict_licensed(surface), rule


def test_hadhf_ayn_is_forced_by_the_binary_licence() -> None:
    """`hadhf_ayn_forced` (على `Admissible` الثنائيّ): قَالْتُ ساكنان متجاوران فغيرُ مرخَّصة، وقُلْتُ مرخَّصة.

    والثلاثيُّ (`ContinueLicensed`) وحدَه يقبل قَالْتُ (CVVC-CV) لأنّه لا يميّز قافيةَ المدّ المدغمةَ من
    غيرها؛ وكان ذلك دَينًا مسمًّى، سدّه قيدُ الحدّ (`Hadd.hadd_debt_closed`): مرفوضةٌ بـ`strictB`، فالحذفُ —
    وهو نطقًا تقصيرُ الحركة الطويلة — ملزَمٌ على الثلاثيّ أيضًا. والمقيسُ في المصحف: 65 من 66 قوافي CVVC
    مدغمة (حَاجَّ)، والواحدةُ الباقية مدُّ الفرق (آلْآنَ)، وكلاهما مقبولٌ بالقيد."""

    source, _, surface = WITNESSES["HADHF_AYN"]
    assert not binary_ok(kind_of(source))
    assert continue_licensed(kind_of(source))  # الثلاثيُّ وحدَه لا يُلزم الحذف…
    assert not strict_licensed(source)  # …وقيدُ الحدّ يُلزمه (`hadd_debt_closed`)
    assert binary_ok(kind_of(surface)) and strict_licensed(surface)


def test_rules_refuse_by_name_when_not_applicable() -> None:
    with pytest.raises(ValueError, match="QALB_AYN_NOT_APPLICABLE"):
        apply("QALB_AYN", w("كَ تَ بَ"), 1)
    with pytest.raises(ValueError, match="UNKNOWN_RULE"):
        apply("NOPE", w("كَ"), 0)


def test_generator_agrees_with_the_hollow_and_defective_witnesses() -> None:
    """صورُ المولِّد (770 جذرًا، مقيسٌ على MASAQ) هي صورُ القواعد في الماضي والأمر: قَالَ، قُلْتُ، قُولُوا، دَعَا،
    دَعَوْا، عِدْ؛ ولا يولّد الأصولَ المعلَّة (قَوَلَ، قَالْتُ). **والمضارعُ غيرُ مولَّدٍ أصلًا** (الأصنافُ
    PAST/PASSIVE/IMPERATIVE فقط) — دَينٌ مسمًّى على المولِّد."""

    qwl, dcw, wcd = derive("قول"), derive("دعو"), derive("وعد")
    assert "قَالَ" in qwl and "قُلْتُ" in qwl and "قُولُوا" in qwl
    assert "دَعَا" in dcw and "دَعَوْا" in dcw
    assert "عِدْ" in wcd
    assert "قَوَلَ" not in qwl and "قَالْتُ" not in qwl
    kinds = {kind for ws in qwl.values() for kind, _, _ in ws}
    assert kinds == {"PAST", "PASSIVE", "IMPERATIVE"}  # لا PRESENT: يَقُولُ ويَعِدُ لا يُولَّدان بعد
