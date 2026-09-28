"""حارسُ الباني: يختبر نفسه على ما أُودِع قبل أن يُسلَّم مستقبلُ الإيداع إليه.

وشرطُ الحكم كما نصّ عليه قرارُ الباني: **ما أعاد بناءً مطابقًا للمودَع نجا،
وما اختلف فمراجعةٌ بانية**. وقد سقط عليه — أوّلَ تمرينٍ له — اقتباسٌ من
`06_asalib` شريحتاه مقلوبتان عن ترتيب الحاوية، فصُحِّح المودَعُ لا الأداة.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILDER_PATH = REPO_ROOT / "tools" / "daleel" / "build_bab.py"


def _load_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("daleel_build_bab", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا يُحمَّل الباني من مساره.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = _load_builder()


def test_the_source_bytes_are_the_ones_the_deposits_name() -> None:
    """المقامُ واحدٌ لا يُبدَّل: بصمةُ البايتات هي المنقولةُ في صفحات العقد."""

    assert builder.SOURCE_BYTES.is_file()
    assert builder.source_fingerprint().startswith("e917d9a0")
    assert builder.SOURCE_BYTES.stat().st_size == 415232


def test_a_quote_is_read_from_the_source_and_never_retyped() -> None:
    """صفرُ طيٍّ: نصُّ الشريحة شريحةٌ من نصّ المصدر لا نسخةٌ مكتوبة."""

    locus = builder.locate("لأن التشابه قد يضلل عن الأسلوب الفعال")
    assert (
        locus.text == builder.source_text()[locus.offset : locus.offset + locus.length]
    )


def test_a_fragment_absent_from_the_bytes_is_refused_not_approximated() -> None:
    """ما لا يثبته الفاحصُ من البايتات لا يولّده الباني، ولا يُقرَّب لأشبهه."""

    with pytest.raises(builder.BuilderError):
        builder.locate("لفظٌ لم يكتبه النبهاني قطُّ في هذا الكتاب البتّة")


def test_two_slices_in_reversed_order_are_refused_as_fabrication() -> None:
    """بابُ الإبطال مُجرَّبٌ لا موصوف: الشريحتان المقلوبتان تُرفَضان."""

    earlier = builder.locate("لأن التشابه قد يضلل عن الأسلوب الفعال")
    later = builder.locate("فأسلوب الدعاية إذا استعمل في أسلوب الدعوة")
    assert earlier.offset < later.offset
    with pytest.raises(builder.BuilderError):
        builder.Passage(loci=(later, earlier))


def test_the_elision_span_is_published_so_a_fold_is_never_silent() -> None:
    """الحذفُ علامةٌ بمقدار: يُخرِج الباني طولَ ما طُوي عند كلِّ `[…]`."""

    passage = builder.build_passage(
        "لأن التشابه قد يضلل عن الأسلوب الفعال […] "
        "فأسلوب الدعاية إذا استعمل في أسلوب الدعوة"
    )
    assert len(passage.elision_spans) == 1
    assert passage.elision_spans[0] > 0


def test_the_counting_carries_its_two_declared_bases() -> None:
    """لا عددَ بلا أساسه: المركّبُ والمفردُ يخرجان معًا مُسمَّيَين."""

    tally = builder.census("الأسلوب الفعال")
    assert tally.compound_base == "العبارةُ بتمامها"
    assert tally.simple_base == "الكلمةُ الأخيرةُ وحدها"
    assert tally.simple >= tally.compound >= 1


def test_the_builder_leaves_a_reasoned_slot_empty_and_marked() -> None:
    """القياسُ بالأثر بناءُ عقل: يُترَك موضعُه موسومًا ولا يملؤه الباني."""

    slot = builder.reasoned_slot("هل الختمُ شرطٌ أم موجب؟")
    assert slot.startswith(builder.REASONED_SLOT)


def test_a_cited_path_is_tagged_present_or_outside_the_tree() -> None:
    """لا شاهدَ بلا موضع: كلُّ مسارٍ يُوسَم حاضرًا أو خارجَ الشجرة."""

    assert builder.standing_in_tree("docs/USOOL_AL-UNBOOB.md") == "حاضرٌ في الشجرة"
    assert "خارجُ الشجرة" in builder.standing_in_tree("لا/موضعَ/له.md")


def test_the_deposited_nodes_are_what_disk_holds_not_what_was_narrated() -> None:
    """أربعُ عقدٍ على القرص؛ وما رُوي إيداعُه ولم يُودَع لا يُعَدّ مودَعًا."""

    names = [path.parent.name for path in builder.deposited_nodes()]
    assert names == ["05_maalumat", "06_asalib", "12_maqamat", "13_tabaqat"]


def test_no_deposited_node_carries_a_fabricated_passage() -> None:
    """تمرينُ الباني الأوّل على تاريخنا: لا شريحةَ مقلوبةً في المودَع كلِّه."""

    for audit in builder.audit_all():
        assert audit.fabricated == (), (audit.node, audit.fabricated)


def test_no_bare_ellipsis_outside_quotes_can_be_mistaken_for_an_elision() -> None:
    """نقاطُ الكتاب لا تُشتبَه بحذف المودِع: خارج «» لا نقطةَ مفردة."""

    for audit in builder.audit_all():
        assert audit.stray_ellipses == 0, audit.node


def test_every_node_declaring_the_covenant_establishes_some_slice() -> None:
    """عهدُ النقل يُبرَّر بعملٍ: كلُّ عقدةٍ فيها اقتباسٌ تُثبِت منه شريحةً."""

    for audit in builder.audit_all():
        if audit.quotes:
            assert audit.established >= 1, audit.node


def test_the_exercise_over_the_whole_deposit_exits_clean() -> None:
    """مخرَجُ الأداة نفسُه هو الحكم؛ ولا يُقرأ نجاحٌ من وصفٍ دون تشغيل."""

    assert builder.main([]) == 0
