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
    """العقدُ تُقاس من القرص لا تُنسَخ قائمةً: ولا عقدةَ تمرّ بلا فحص.

    وكانت ههنا قائمةٌ مجمَّدةٌ بأسماء أربعِ عقد. فلمّا وصلت خمسٌ أخرى سقط
    الاختبارُ — وهو محقٌّ في سقوطه لكنّه سقط عن **نقلٍ** لا عن **قياس**:
    ما حرسه أنّ الأسماء هي هي، لا أنّ كلّ عقدةٍ على القرص مفحوصة. فصار
    الحدُّ مقيسًا: مجموعةُ ما يفحصه الباني هي عينُ مجموعةِ ما يحمل صفحةً
    على القرص، لا تزيد ولا تنقص.
    """

    audited = {path.parent.name for path in builder.deposited_nodes()}
    on_disk = {
        child.name
        for child in builder.NODES_ROOT.iterdir()
        if child.is_dir() and (child / "README.md").is_file()
    }
    assert audited == on_disk
    assert audited


def test_no_node_is_waved_through_with_nothing_audited() -> None:
    """سكوتٌ يدّعي الكلام: صفحةٌ فيها «» ويُطبَع لها ✓ على صفرِ فحص.

    وهذا عطبٌ وقع فعلًا: قاعدةُ القطع عند الخطّ الأوّل أخرجت خمسَ عقدٍ
    كاملةً من الفحص ثمّ منحتها علامةَ سلامة.
    """

    for audit in builder.audit_all():
        page = (builder.NODES_ROOT / audit.node / "README.md").read_text(
            encoding="utf-8"
        )
        if builder.OPEN_QUOTE in page:
            assert audit.quotes > 0, audit.node


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


def test_occurrence_is_not_uniqueness_and_both_are_measured() -> None:
    """الوقوعُ غيرُ التفرّد: شريحةٌ ثابتةٌ في البايتات قد تقع مرّاتٍ فيها."""

    assert builder.occurrences("فأسلوب الدعاية إذا استعمل") == 1
    assert builder.occurrences("تعارض") > 1


def test_a_node_claiming_uniqueness_has_every_slice_occurring_once() -> None:
    """دعوى «مرّةً واحدةً» مقيسةٌ لا مأخوذةٌ على حسن الظنّ."""

    claimants = [audit for audit in builder.audit_all() if audit.claims_uniqueness]
    assert claimants, "صفحةٌ واحدةٌ على الأقلّ ترفع دعوى التفرّد"
    for audit in claimants:
        assert audit.unsupported_uniqueness == (), (
            audit.node,
            audit.unsupported_uniqueness,
        )


def test_a_node_that_never_claims_uniqueness_is_not_held_to_it() -> None:
    """الحارسُ يتبع الدعوى ولا يفرض شرطًا لم ترفعه الصفحة."""

    silent = [audit for audit in builder.audit_all() if not audit.claims_uniqueness]
    assert silent, "صفحةٌ واحدةٌ على الأقلّ تسكت عن التفرّد"
    assert any(audit.repeated_slices for audit in silent)
    for audit in silent:
        assert audit.unsupported_uniqueness == ()


def test_a_forged_uniqueness_claim_is_refused(tmp_path: Path) -> None:
    """بابُ إبطال الدعوى مُجرَّب: صفحةٌ تدّعي التفرّدَ بشريحةٍ مكرّرةٍ تسقط."""

    node = tmp_path / "99_forged"
    node.mkdir()
    page = node / "README.md"
    page.write_text(
        f"«تعارض»\n\n{builder.THE_UNIQUENESS_CLAIM} حرفًا بحرف.\n",
        encoding="utf-8",
    )
    audit = builder.audit_node(page)
    assert audit.claims_uniqueness
    assert audit.unsupported_uniqueness
    assert not audit.is_clean


def test_the_analogy_rules_are_located_in_the_bytes_not_transcribed() -> None:
    """البابُ الخامس عشر يستند إلى مولِّدٍ يفتح قاعدتيه، لا إلى عددٍ منقول."""

    loci = builder.analogy_rule_loci()
    assert len(loci) == len(builder.THE_ANALOGY_RULES)
    for locus, rule in zip(loci, builder.THE_ANALOGY_RULES, strict=True):
        assert locus.text == builder.fold(rule)
        assert locus.length > 0


def test_a_rule_that_left_the_bytes_drops_the_gate(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """سقوطُ المولِّد مُجرَّبٌ لا موصوف: قاعدةٌ لا تقع في البايتات تُسقِطه."""

    monkeypatch.setattr(builder, "THE_ANALOGY_RULES", ("قاعدةٌ لا يعرفها الكتابُ البتّة",))
    with pytest.raises(builder.BuilderError):
        builder.analogy_rule_loci()


def test_a_page_whose_header_is_closed_by_a_rule_is_read_not_skipped() -> None:
    """شكلا الصفحة مقروءان: ترويسةٌ يغلقها خطٌّ ثمّ نقلٌ ثمّ خطٌّ ثمّ حكم."""

    document = "\n".join(
        [
            "# عنوان",
            "",
            "> ترويسةٌ تصف المسطرة.",
            "",
            "---",
            "",
            "«فأسلوب الدعاية إذا استعمل»",
            "",
            "---",
            "",
            "«مصطلحُ الشجرة» تحت الخطّ فلا يُفحَص.",
            "",
        ]
    )
    quotes = builder.quotes_in(builder.transcription_region(document))
    assert quotes == ("فأسلوب الدعاية إذا استعمل",)


def test_a_page_with_one_rule_still_reads_everything_above_it() -> None:
    """والشكلُ الآخر لم يُكسَر: خطٌّ واحدٌ فالنقلُ كلُّ ما فوقه."""

    document = "«فأسلوب الدعاية إذا استعمل»\n\n---\n\n«مصطلحُ الشجرة»\n"
    assert builder.quotes_in(builder.transcription_region(document)) == (
        "فأسلوب الدعاية إذا استعمل",
    )


def test_a_blockquote_mark_inside_a_long_quote_is_not_charged_to_the_book() -> None:
    """علامةُ الاقتباس في أوّل السطر وَسْمُ صفحةٍ، فلا تُحمَّل على المصدر."""

    document = "> «فأسلوب الدعاية\n> إذا استعمل»\n"
    (quoted,) = builder.quotes_in(document)
    assert ">" not in quoted
    assert builder.locate(quoted).length > 0


def test_an_ellipsis_named_inside_a_code_span_is_not_a_suspected_elision() -> None:
    """تسميةُ العلامة ليست استعمالَها؛ ولا تُعاقَب صفحةٌ شرحت قاعدةَ نقلها."""

    named = "الكتابُ يستعمل `…` فاصلًا بين فقراته.\n"
    used = "وقال الكاتب … ثمّ سكت.\n"
    assert builder.stray_ellipses_outside_quotes(named) == 0
    assert builder.stray_ellipses_outside_quotes(used) == 1
