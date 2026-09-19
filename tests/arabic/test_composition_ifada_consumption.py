"""اختباراتُ إحصاء الاستهلاك: أيمرّ مسارُ الإفادة بجبرٍ أوسعَ، أم يجاوره؟"""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic.composition_ifada_consumption import (
    CANDIDATE_ALGEBRAS,
    COMPOSITION_IFADA_CONSUMPTION_NAMED_LAWS,
    THE_PATH_ENTRY_MODULE,
    CandidateAlgebra,
    ConsumptionCensus,
    ConsumptionRow,
    IfadaConsumptionError,
    derive_consumption_census,
    derive_import_closure,
    render_consumption_census,
)

# ————— الإغلاقةُ مُشتَقّةٌ لا مُصرَّحة —————


def test_the_closure_contains_its_own_entry_module() -> None:
    """الإغلاقةُ تبدأ بوحدة `run_bytes` نفسِها، فليست جردًا لحزمةٍ مجاورة."""

    closure = derive_import_closure()
    assert THE_PATH_ENTRY_MODULE in closure
    assert closure == tuple(sorted(closure))
    assert len(set(closure)) == len(closure)


def test_every_module_in_the_closure_is_an_alghanem_module() -> None:
    """الإغلاقةُ تُحصي وحداتِ المشروع وحدَها؛ فمكتباتُ المعيار ليست قياسًا له."""

    assert all(module.startswith("alghanem") for module in derive_import_closure())


def test_the_closure_is_far_smaller_than_the_arabic_package() -> None:
    """إغلاقةُ المسار جزءٌ صغيرٌ من حزمة العربيّة، والنسبةُ مقيسةٌ لا موصوفة."""

    closure = derive_import_closure()
    arabic_modules = list(
        Path(__file__).resolve().parents[2].glob("src/alghanem/arabic/*.py")
    )
    assert len(closure) < len(arabic_modules)


# ————— كلُّ جبرٍ مرشَّحٍ له صفٌّ، ولا يُطوى —————


def test_each_candidate_algebra_gets_exactly_one_row() -> None:
    """لكلِّ جبرٍ مرشَّحٍ صفٌّ واحد؛ فلا يُحذف جبرٌ ليَحسُن الإحصاء."""

    census = derive_consumption_census()
    assert len(census.rows) == len(CANDIDATE_ALGEBRAS)
    assert tuple(row.algebra for row in census.rows) == CANDIDATE_ALGEBRAS


def test_the_candidate_prefixes_are_distinct_and_resolvable() -> None:
    """بادئاتُ الجبور متمايزةٌ، وكلُّ بادئةٍ تشير إلى موضعٍ قائمٍ في الشجرة."""

    prefixes = [algebra.module_prefix for algebra in CANDIDATE_ALGEBRAS]
    assert len(set(prefixes)) == len(prefixes)
    root = Path(__file__).resolve().parents[2] / "src"
    for prefix in prefixes:
        target = root.joinpath(*prefix.split("."))
        assert (
            target.is_dir()
            or target.with_suffix(".py").is_file()
            or any(target.parent.glob(f"{target.name}*.py"))
        )


# ————— الجوابُ المقيس: لا جبرَ أوسعَ مستهلَك —————


def test_no_wider_algebra_is_consumed_by_the_ifada_path() -> None:
    """لا حافّةَ استيرادٍ واحدةً تصل مسارَ الإفادة بجبرٍ من المرشَّحين."""

    census = derive_consumption_census()
    assert census.any_wider_algebra_is_consumed is False
    assert census.consumed == ()
    assert all(row.reached_modules == () for row in census.rows)


def test_every_gap_carries_a_named_residual_not_a_refusal() -> None:
    """كلُّ فجوةٍ تحمل بقيّةً مُسمّاةً تقول «لم يُقَس»، لا رفضًا يقول «لا يكون»."""

    census = derive_consumption_census()
    assert len(census.residuals) == len(CANDIDATE_ALGEBRAS)
    for residual in census.residuals:
        assert "لم يُقَس بعد" in residual
        assert "موجودٌ في المستودع" in residual


def test_a_consumed_algebra_would_carry_no_residual() -> None:
    """والبقيّةُ مشروطةٌ ببلوغٍ منعدم؛ فلو بُلِغ الجبرُ سقطت بقيّتُه."""

    algebra = CANDIDATE_ALGEBRAS[0]
    reached = ConsumptionRow(
        algebra=algebra, reached_modules=(f"{algebra.module_prefix}.node",)
    )
    assert reached.is_consumed is True
    assert reached.residual is None


# ————— الإحصاءُ يقدر على رصد اتّصالٍ لو وقع —————


def test_the_measurement_detects_a_real_edge_where_one_exists() -> None:
    """شاهدُ ضبطٍ موجَب: الحزمةُ التي يستوردها المسارُ فعلًا تُرصَد مستهلَكةً."""

    census = derive_consumption_census()
    probe = CandidateAlgebra(
        name="محتوى التقنين",
        module_prefix="alghanem.canonical_content",
        what_it_offers="بصماتٌ قانونيّةٌ للمحتوى",
    )
    row = ConsumptionRow(
        algebra=probe,
        reached_modules=tuple(
            module
            for module in census.closure
            if module == probe.module_prefix
            or module.startswith(f"{probe.module_prefix}.")
        ),
    )
    assert row.is_consumed is True
    assert row.residual is None


def test_a_prefix_is_not_matched_by_a_mere_name_overlap() -> None:
    """المطابقةُ على حدود النقطة؛ فلا تُحسَب وحدةٌ يشترك اسمُها في بادئةٍ ناقصة."""

    census = derive_consumption_census()
    probe = CandidateAlgebra(
        name="بادئةٌ ناقصة",
        module_prefix="alghanem.arabic.composition_ifada",
        what_it_offers="بادئةٌ تشترك في أوّل اسم وحدة المسار",
    )
    reached = tuple(
        module
        for module in census.closure
        if module == probe.module_prefix or module.startswith(f"{probe.module_prefix}.")
    )
    assert THE_PATH_ENTRY_MODULE not in reached


# ————— حرّاسُ البناء والبصمة —————


def test_the_census_digest_changes_with_its_consumed_set() -> None:
    """بصمةُ الإحصاء تتغيّر بتغيّر إغلاقته؛ فليست ثابتًا مكتوبًا بجانبه."""

    census = derive_consumption_census()
    other = ConsumptionCensus(
        closure=(*census.closure, "alghanem.structural_dal.laws"),
        rows=census.rows,
    )
    assert len(census.census_digest) == 64
    assert other.census_digest != census.census_digest


def test_an_empty_closure_is_not_a_measurement() -> None:
    """إغلاقةٌ فارغةٌ تُرَدّ؛ فغيابُ القياس ليس قياسًا بنتيجةٍ صفريّة."""

    census = derive_consumption_census()
    with pytest.raises(IfadaConsumptionError):
        ConsumptionCensus(closure=(), rows=census.rows)


def test_a_census_missing_its_entry_module_is_refused() -> None:
    """إغلاقةٌ لا تشمل وحدةَ مبدئها ليست إغلاقةَ هذا المسار."""

    census = derive_consumption_census()
    with pytest.raises(IfadaConsumptionError):
        ConsumptionCensus(
            closure=tuple(
                module for module in census.closure if module != THE_PATH_ENTRY_MODULE
            ),
            rows=census.rows,
        )


def test_a_census_that_drops_a_candidate_row_is_refused() -> None:
    """إحصاءٌ يُسقِط صفَّ جبرٍ مرشَّحٍ يُرَدّ، فلا يُحسَّن الجوابُ بحذف سؤاله."""

    census = derive_consumption_census()
    with pytest.raises(IfadaConsumptionError):
        ConsumptionCensus(closure=census.closure, rows=census.rows[:-1])


def test_unsorted_reached_modules_are_refused() -> None:
    """الوحداتُ المبلوغةُ مرتَّبةٌ ترتيبًا واحدًا، فلا يُخفي ترتيبٌ ثانٍ فرقًا."""

    with pytest.raises(IfadaConsumptionError):
        ConsumptionRow(
            algebra=CANDIDATE_ALGEBRAS[0],
            reached_modules=("alghanem.b", "alghanem.a"),
        )


def test_a_blank_candidate_field_is_refused() -> None:
    """جبرٌ بلا اسمٍ أو بلا بادئةٍ أو بلا وصفٍ ليس مرشَّحًا يُسأل عنه."""

    for blank in ("name", "module_prefix", "what_it_offers"):
        fields = {
            "name": "اسم",
            "module_prefix": "alghanem.x",
            "what_it_offers": "وصف",
        }
        fields[blank] = "   "
        with pytest.raises(IfadaConsumptionError):
            CandidateAlgebra(**fields)


# ————— القوانينُ المُسمّاةُ والعرض —————


def test_every_named_law_opens_with_its_own_name() -> None:
    """كلُّ قانونٍ مُسمًّى يفتتح نصُّه باسمه، فلا يُقرأ نصٌّ بلا قانونه."""

    assert COMPOSITION_IFADA_CONSUMPTION_NAMED_LAWS
    for name, text in COMPOSITION_IFADA_CONSUMPTION_NAMED_LAWS.items():
        assert text.startswith(f"{name}:")


def test_the_render_carries_the_measured_answer_and_the_residuals() -> None:
    """العرضُ يحمل الجوابَ المقيسَ وبقاياه، لا وصفًا يُكتَب بجانب الإحصاء."""

    census = derive_consumption_census()
    rendered = render_consumption_census(census)
    assert census.census_digest in rendered
    assert str(census.closure_size) in rendered
    assert "أيستهلك المسارُ جبرًا أوسعَ: False" in rendered
    for algebra in CANDIDATE_ALGEBRAS:
        assert algebra.name in rendered


def test_the_module_claims_no_chain_among_its_counts() -> None:
    """لا موضعَ في الوحدة يجمع أعدادًا متفرّقةً فيسمّيها سلسلةَ انتقالٍ مغلقة."""

    text = (
        Path(__file__)
        .resolve()
        .parents[2]
        .joinpath("src/alghanem/arabic/composition_ifada_consumption.py")
        .read_text(encoding="utf-8")
    )
    for claim in ("closed_chain", "the_chain_is_closed", "proves_consumption"):
        assert claim not in text
