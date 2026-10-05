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
    _bound_names_from,
    _called_names,
    _imports_of,
    _module_file,
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
    assert "أيستورد المسارُ جبرًا أوسعَ: False" in rendered
    assert "أيستدعي منه شيئًا: False" in rendered
    assert "أيمكن قياسُ بلوغ المخرج: False" in rendered
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


# ————— تدقيقُ المطابقة: كلُّ حافّةٍ تُحَلّ إلى ملفٍ قائم —————


def test_every_derived_edge_resolves_to_a_file_on_disk() -> None:
    """لا اسمَ في الإغلاقة بلا ملفٍ يقابله؛ فالخللُ في المطابقة يُكشَف لا يُطوى."""

    for module in derive_import_closure():
        assert _module_file(module) is not None, module


def test_a_package_init_resolves_its_relative_imports_to_itself() -> None:
    """نسبيُّ `__init__.py` يُحَلّ إلى حزمته لا إلى أمّها؛ وهذا خللٌ صُحِّح."""

    module = "alghanem.structural_dal"
    path = _module_file(module)
    assert path is not None and path.name == "__init__.py"
    imported = _imports_of(path, module)
    assert imported
    assert all(name.startswith(f"{module}.") for name in imported)
    assert all(_module_file(name) is not None for name in imported)


def test_importing_a_submodule_from_its_package_is_its_own_edge() -> None:
    """`from حزمة import وحدة` حافّةٌ إلى الوحدة، لا إلى حزمتها وحدَها."""

    module = "alghanem.structural_dal"
    path = _module_file(module)
    assert path is not None
    imported = _imports_of(path, module)
    assert f"{module}.laws" in imported
    assert f"{module}.slots" in imported


def test_the_resolution_audit_holds_across_the_whole_source_tree() -> None:
    """والتدقيقُ لا يخصّ الإغلاقة: كلُّ وحدةٍ في الشجرة تُخرِج حوافَّ قابلةً للحلّ."""

    root = Path(__file__).resolve().parents[2] / "src"
    unresolved: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*.py")):
        parts = path.relative_to(root).with_suffix("").parts
        module = ".".join(parts[:-1] if parts[-1] == "__init__" else parts)
        for edge in _imports_of(path, module):
            if _module_file(edge) is None:
                unresolved.append((module, edge))
    assert unresolved == []


# ————— الاستيرادُ ليس استدعاءً، والاستدعاءُ ليس مخرجًا —————


def test_no_wider_algebra_is_called_by_the_ifada_path() -> None:
    """ولا اسمَ واحدًا يُستدعى من جبرٍ أوسع؛ وهو سؤالٌ وراء الاستيراد لا عينُه."""

    census = derive_consumption_census()
    assert census.any_wider_algebra_is_called is False
    assert census.called == ()
    assert all(row.called_names == () for row in census.rows)


def test_output_reach_is_unmeasurable_where_nothing_is_called() -> None:
    """لا مخرجَ يُتتبَّع حيث لا استدعاء؛ فالتتبّعُ يعلن تعذُّرَه ولا يزعم صفرًا."""

    census = derive_consumption_census()
    assert census.output_reach_is_measured is False
    assert "TheCallTraceIsStaticNotDynamic" in census.what_the_call_trace_cannot_see


def test_an_imported_name_that_is_never_called_is_counted_apart() -> None:
    """المستورَدُ غيرُ المُستدعى يُعَدّ على حِدة، فلا يُقرأ جوارٌ ساكنٌ اعتمادًا."""

    row = ConsumptionRow(
        algebra=CANDIDATE_ALGEBRAS[0],
        reached_modules=("alghanem.prior_fiber.node",),
        bound_names=("PriorFiberNode", "SlotStanding"),
        called_names=("PriorFiberNode",),
    )
    assert row.is_consumed is True
    assert row.is_called is True
    assert row.imported_but_unused == ("SlotStanding",)


def test_a_call_without_a_matching_import_is_refused() -> None:
    """مُستدعًى لا يقابله مستورَدٌ من الجبر نفسِه تناقضٌ يُرَدّ لا يُصحَّح صامتًا."""

    with pytest.raises(IfadaConsumptionError):
        ConsumptionRow(
            algebra=CANDIDATE_ALGEBRAS[0],
            reached_modules=("alghanem.prior_fiber.node",),
            bound_names=("PriorFiberNode",),
            called_names=("SomethingElse",),
        )


def test_bound_names_without_a_reached_module_are_refused() -> None:
    """أسماءٌ مربوطةٌ من جبرٍ لم تُبلَغ وحدةٌ منه تناقضٌ في القياس نفسِه."""

    with pytest.raises(IfadaConsumptionError):
        ConsumptionRow(
            algebra=CANDIDATE_ALGEBRAS[0],
            reached_modules=(),
            bound_names=("PriorFiberNode",),
        )


def test_unsorted_name_columns_are_refused() -> None:
    """عمودا الأسماء مرتَّبان ترتيبًا واحدًا، فلا يُخفي ترتيبٌ ثانٍ فرقًا."""

    with pytest.raises(IfadaConsumptionError):
        ConsumptionRow(
            algebra=CANDIDATE_ALGEBRAS[0],
            reached_modules=("alghanem.prior_fiber.node",),
            bound_names=("Zayd", "Amr"),
        )


def test_the_call_trace_detects_a_real_call_where_one_exists() -> None:
    """شاهدُ ضبطٍ موجَب: ما يستدعيه المسارُ فعلًا يُرصَد مربوطًا ومُستدعًى."""

    entry = _module_file(THE_PATH_ENTRY_MODULE)
    assert entry is not None
    bound = _bound_names_from(
        entry, THE_PATH_ENTRY_MODULE, "alghanem.canonical_content"
    )
    called = bound & _called_names(entry, THE_PATH_ENTRY_MODULE)
    assert "canonical_digest" in bound
    assert "canonical_digest" in called


def test_the_digest_separates_import_from_call() -> None:
    """بصمةُ الإحصاء تفرّق بين المستورَد والمُستدعى، فلا يُطوى أحدُهما في الآخر."""

    census = derive_consumption_census()
    called_row = ConsumptionRow(
        algebra=CANDIDATE_ALGEBRAS[0],
        reached_modules=("alghanem.prior_fiber.node",),
        bound_names=("PriorFiberNode",),
        called_names=("PriorFiberNode",),
    )
    shifted = ConsumptionCensus(
        closure=census.closure, rows=(called_row, *census.rows[1:])
    )
    assert shifted.any_wider_algebra_is_called is True
    assert shifted.output_reach_is_measured is True
    assert shifted.census_digest != census.census_digest
