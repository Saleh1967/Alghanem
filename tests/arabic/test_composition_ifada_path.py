"""اختبارُ المسار العربيّ الموصول من الترميز إلى مرشّح الإفادة.

ثلاثةُ محاورَ مفصولة: الاسترجاعُ الكتابيّ، وقراءةُ التركيب، وقراءةُ الإفادة.
ولا يُقرأ نجاحُ أحدِها دليلًا على الآخر.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from alghanem.arabic import composition_ifada_path
from alghanem.arabic.composition_ifada_experiment import (
    ACCOUNTED_TOKEN,
    COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS,
    DECLARED_CASES,
    UNACCOUNTED_TOKEN,
    DeclaredCase,
    PathCensus,
    measure,
    render_census,
    run_under_the_experimental_authority,
)
from alghanem.arabic.composition_ifada_interpretation import (
    DeclaredRootAnnotation,
    MasaqStanding,
    interpret,
    render_interpretation,
)
from alghanem.arabic.composition_ifada_path import (
    COMPOSITION_IFADA_PATH_NAMED_LAWS,
    CaseMark,
    CompositionReading,
    PathStage,
    PathStop,
    StageOutcome,
    run_bytes,
    run_text,
)
from alghanem.arabic.mantuq_mafhum_ifada import IfadaStanding
from alghanem.arabic.maqayis_lexical_origin import RootAttestation
from alghanem.arabic.maqayis_root_table_deposit import FROZEN_ROOT_TABLE
from alghanem.kernel.experimental import (
    ExperimentalAuthority,
    ExperimentalOutcomeStatus,
    ExperimentalRunRecord,
)


def test_the_positive_reading_reaches_a_derived_benefit() -> None:
    """«اللَّهُ نُورٌ»: ضمّتان، فالإسنادُ مقروءٌ والإفادةُ مُشتقّة."""

    run = run_text("اللَّهُ نُورٌ")

    assert run.reached is PathStage.IFADA
    assert run.outcome is StageOutcome.ADVANCED
    assert run.stop is None
    assert run.composition is CompositionReading.إسناد
    assert run.ifada is IfadaStanding.مُفيد


def test_the_negative_reading_is_a_composition_that_does_not_benefit() -> None:
    """«نُورُ السَّمَاوَاتِ»: ضمّةٌ فكسرة، فالإضافةُ قائمةٌ ولا تُفيد."""

    run = run_text("نُورُ السَّمَاوَاتِ")

    assert run.reached is PathStage.IFADA
    assert run.composition is CompositionReading.إضافة
    assert run.ifada is IfadaStanding.غير_مُفيد
    assert run.record is not None
    assert run.record.composition_benefits is False
    assert run.record.benefit_witness.strip()


def test_the_ambiguous_reading_defers_by_a_named_preventer() -> None:
    """«الْحَمْدُ لِلَّهِ»: لامٌ مكسورةٌ في الأوّل، فالكسرةُ لا تُميّز الإضافة."""

    run = run_text("الْحَمْدُ لِلَّهِ")

    assert run.reached is PathStage.COMPOSITION
    assert run.outcome is StageOutcome.DEFERRED
    assert run.stop is PathStop.PROCLITIC_JARR_UNDECIDED
    assert run.composition is None
    assert run.ifada is IfadaStanding.غير_مقروء


def test_an_unwritten_final_mark_stops_below_composition() -> None:
    """«قُلْ هُوَ»: لا علامةَ آخِرٍ مكتوبةً تُقرأ، فالتوقّفُ دون التركيب."""

    run = run_text("قُلْ هُوَ")

    assert run.reached is PathStage.CASE_MARK
    assert run.stop is PathStop.FINAL_MARK_NOT_WRITTEN
    assert run.ifada is IfadaStanding.غير_مقروء


def test_a_tanwined_first_word_blocks_the_idafa_reading() -> None:
    """«كِتَابٌ الْبَيْتِ»: المضافُ لا يُنوَّن، فالمانعُ محدَّدٌ لا غامض."""

    run = run_text("كِتَابٌ الْبَيْتِ")

    assert run.outcome is StageOutcome.BLOCKED
    assert run.stop is PathStop.MUDAF_CARRIES_TANWIN
    assert run.ifada is IfadaStanding.غير_مقروء


@pytest.mark.parametrize(
    ("text", "stop"),
    [
        ("الْعَالَمِينَ نُورٌ", PathStop.FIRST_MARK_IS_NOT_RAF),
        ("رَبُّ الْعَالَمِينَ", PathStop.SECOND_MARK_IS_NASB),
        ("اللَّهُ", PathStop.NOT_TWO_WORDS),
    ],
)
def test_each_refused_reading_names_its_own_genus(text: str, stop: PathStop) -> None:
    """كلُّ امتناعٍ يُنسَب إلى جنسه المُسمّى، لا إلى «فشلٍ» واحدٍ مُبهَم."""

    run = run_text(text)

    assert run.stop is stop
    assert run.outcome is not StageOutcome.ADVANCED
    assert run.ifada is IfadaStanding.غير_مقروء


def test_the_benefit_is_never_taken_from_the_caller() -> None:
    """لا مدخلَ في `run_text` يَكتب الفائدة؛ توقيعُها هو الشاهد."""

    signature = inspect.signature(run_text)

    assert list(signature.parameters) == ["text"]
    assert "composition_benefits" not in signature.parameters


def test_a_read_benefit_always_carries_its_own_witness() -> None:
    """كلُّ فائدةٍ مقروءةٍ تحمل شاهدَها، وكلُّ غيرِ مقروءةٍ لا سجلَّ لها."""

    for case in DECLARED_CASES:
        run = run_bytes(case.source)
        if run.record is None:
            assert run.ifada is IfadaStanding.غير_مقروء
            assert run.composition is None
            continue
        assert run.record.composition_benefits is not None
        assert run.record.benefit_witness.strip()


def test_written_retrieval_is_measured_apart_from_analysis() -> None:
    """الاسترجاعُ الكتابيّ يَتمّ لكلمات نصوصٍ لم تبلغ إفادةً، فهما محوران."""

    stopped = run_text("الْحَمْدُ لِلَّهِ")

    assert not stopped.reached_ifada
    assert all(word.crossed_the_written_chain for word in stopped.words)


def test_analysis_success_is_measured_apart_from_the_benefit() -> None:
    """قراءةُ التركيب تَتمّ حيث الإفادةُ منفيّة، فقراءتُه ليست قراءتَها."""

    run = run_text("نُورُ كِتَابٍ")

    assert run.composition is CompositionReading.إضافة
    assert run.ifada is IfadaStanding.غير_مُفيد


def test_every_stage_record_carries_its_identity_and_ground() -> None:
    """كلُّ انتقالٍ يَحفظ هويّةَ مدخله وعمليتَه وشرطَه ورتبتَه وأثرَه."""

    run = run_text("اللَّهُ نُورٌ")

    assert run.stages
    ranks = [record.rank for record in run.stages]
    assert ranks == sorted(ranks)
    for record in run.stages:
        assert record.operation.strip()
        assert record.condition.strip()
        assert record.input_digest.strip()
        assert record.evidence.strip()
        assert record.trace.events
        assert (record.preventer is None) is (record.outcome is StageOutcome.ADVANCED)


def test_the_case_mark_is_read_from_the_carrier_states() -> None:
    """علامةُ الآخِر تُقرأ من حالات الحامل، لا من معجمٍ ولا من جدولِ جواب."""

    run = run_text("اللَّهُ نُورٌ")

    assert [word.final_mark for word in run.words] == [CaseMark.ضمّة, CaseMark.ضمّة]
    assert [word.final_is_tanwin for word in run.words] == [False, True]


def test_the_run_completes_under_the_experimental_authority() -> None:
    """السَّوقُ يَتمّ بسلطةٍ قائمةٍ وطلبٍ مربوطٍ بتجربةٍ مجمّدة."""

    record = run_under_the_experimental_authority()

    assert type(record) is ExperimentalRunRecord
    assert record.outcome_status is ExperimentalOutcomeStatus.COMPLETED
    assert record.failure is None
    assert record.operations_used == ("run_bytes",)
    assert record.request_content_digest.strip()


def test_the_run_is_neither_asked_for_nor_issues_a_certificate() -> None:
    """التجريبُ لا يشترط شهادةَ ولادة، ولا يُصدرها، فالسلطتان مفصولتان."""

    parameters = inspect.signature(ExperimentalAuthority.run).parameters
    record = run_under_the_experimental_authority()

    assert "certificate" not in parameters
    assert "verdict" not in parameters
    assert not any(
        "certificate" in name for name in ExperimentalRunRecord.__annotations__
    )
    assert not any("certificate:" in event for event in record.trace.events)


def test_each_declared_case_is_answered_by_exactly_one_frozen_token() -> None:
    """كلُّ حالةٍ مُعلَنةٍ تُجاب بمفردةٍ واحدةٍ من المفردتين المجمّدتين."""

    record = run_under_the_experimental_authority()
    assert record.output_content is not None
    lines = record.output_content.splitlines()

    assert len(lines) == len(DECLARED_CASES)
    for line, case in zip(lines, DECLARED_CASES, strict=True):
        prefix, token = line.split("=", 1)
        assert prefix == case.case_id
        assert token in {ACCOUNTED_TOKEN, UNACCOUNTED_TOKEN}


def test_the_census_keeps_every_stop_in_its_denominator() -> None:
    """المقامُ يَشمل الواقفَ والممنوعَ والمؤجَّل، ولا يُنقّى لترتفع نسبة."""

    census = measure()

    assert census.input_total == len(DECLARED_CASES)
    assert sum(census.outcome_counts.values()) == census.input_total
    assert sum(census.ifada_counts.values()) == census.input_total
    assert census.reached_counts[PathStage.UTF8_BYTES] == census.input_total
    assert census.reached_counts[PathStage.IFADA] == census.reached_ifada
    assert census.reached_ifada < census.input_total
    assert sum(census.stop_counts.values()) == census.input_total - census.reached_ifada


def test_the_census_ranks_are_monotone_down_the_path() -> None:
    """ما بلغ طبقةً أعلى لا يزيد على ما بلغ ما دونها؛ فالسلسلةُ متّصلة."""

    counts = measure().reached_counts
    ordered = [counts[stage] for stage in PathStage]

    assert ordered == sorted(ordered, reverse=True)


def test_the_census_reading_is_rendered_without_an_unnamed_ratio() -> None:
    """العرضُ يَذكر المقاماتِ صريحةً، ولا يكتب نسبةً بلا مقامٍ مُسمّى."""

    text = render_census(measure())

    assert "%" not in text
    for stage in PathStage:
        assert stage.value in text
    for stop in PathStop:
        assert stop.value in text


def test_an_empty_census_is_refused() -> None:
    """إحصاءٌ بلا سَوقٍ واحدٍ لا يُقرأ، فلا مقامَ له."""

    record = run_under_the_experimental_authority()

    with pytest.raises(ValueError):
        PathCensus(record=record, cases=(), runs=())


def test_a_census_is_refused_over_runs_that_are_not_its_own_cases() -> None:
    """الإحصاءُ يُقرأ من بايتات حالاته نفسِها، فلا يُركَّب سَوقٌ على حالةٍ أخرى."""

    record = run_under_the_experimental_authority()
    foreign = tuple(run_bytes(case.source) for case in reversed(DECLARED_CASES))

    with pytest.raises(ValueError):
        PathCensus(record=record, cases=DECLARED_CASES, runs=foreign)


@pytest.mark.parametrize(
    "laws",
    [COMPOSITION_IFADA_PATH_NAMED_LAWS, COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS],
)
def test_every_named_law_opens_with_its_own_name(laws: dict[str, str]) -> None:
    """كلُّ قانونٍ مُسمًّى يفتتح نصُّه باسمه، فلا قانونَ بلا اسمٍ مقروء."""

    assert laws
    for name, statement in laws.items():
        assert statement.startswith(f"{name}:")


# ————— المدخلُ بايتاتٌ، وفكُّ ترميزها انتقالٌ مقيس —————


def test_the_entry_is_bytes_and_the_decode_is_a_measured_transition() -> None:
    """أوّلُ انتقالٍ فكُّ ترميزٍ صارمٍ، ببصمة البايتات مدخلًا ونصًّا مخرجًا."""

    source = "اللَّهُ نُورٌ".encode()
    run = run_bytes(source)
    first = run.stages[0]

    assert run.source == source
    assert first.stage is PathStage.UTF8_BYTES
    assert first.rank == 1
    assert first.operation == "decode the declared bytes as strict UTF-8"
    assert first.outcome is StageOutcome.ADVANCED
    assert first.output_digest is not None
    assert first.input_digest != first.output_digest


def test_bytes_that_are_not_utf8_are_blocked_by_a_named_preventer() -> None:
    """بايتاتٌ ليست UTF-8 تقف بمانعها، ولا تُصلَح ولا تُقرأ بإبدال."""

    run = run_bytes(b"\xff\xfe \xd8")

    assert run.reached is PathStage.UTF8_BYTES
    assert run.outcome is StageOutcome.BLOCKED
    assert run.stop is PathStop.BYTES_ARE_NOT_UTF8
    assert run.text == ""
    assert run.words == ()
    assert run.ifada is IfadaStanding.غير_مقروء


def test_the_text_entry_only_encodes_and_delegates_to_the_bytes_entry() -> None:
    """`run_text` تُرمِّز وتُسلِّم، ولا تتخطّى بها طبقةُ الترميز."""

    text = "نُورُ السَّمَاوَاتِ"

    by_text = run_text(text)
    by_bytes = run_bytes(text.encode())

    assert by_text.source == text.encode()
    assert by_text.trace.events == by_bytes.trace.events
    assert by_text.ifada is by_bytes.ifada


def test_the_word_split_reads_the_normalized_text_not_the_raw_one() -> None:
    """القسمةُ تقع على النصّ المُسوَّى، فالتسويةُ تسبق كلَّ قراءة."""

    run = run_text("اللَّهُ نُورٌ")
    split = next(
        record for record in run.stages if record.stage is PathStage.WORD_SPLIT
    )
    normalized = next(
        record for record in run.stages if record.stage is PathStage.UNICODE_NFC
    )

    assert split.input_digest == normalized.output_digest
    assert split.rank > normalized.rank


# ————— التفسيرُ يعلو الاشتقاقَ ولا يدخل فيه —————


def test_the_interpretation_changes_neither_the_stages_nor_the_standing() -> None:
    """التعليقُ لا يُبدّل حكمَ انتقالٍ ولا حالَ إفادة، وذلك مقيسٌ لا موعود."""

    run = run_text("اللَّهُ نُورٌ")
    before = (run.reached, run.outcome, run.stop, run.ifada, run.trace.events)

    interpretation = interpret(
        run,
        (
            DeclaredRootAnnotation(
                word_index=1,
                root="نور",
                declared_by="يدُ المحرِّر",
                why="تعليقٌ مكتوبٌ بيدٍ لقياس طبقة التفسير",
            ),
        ),
    )

    assert interpretation.derivation_is_unchanged
    assert (run.reached, run.outcome, run.stop, run.ifada, run.trace.events) == before


def test_an_attested_declared_root_carries_a_quoted_gloss() -> None:
    """الجذرُ المُعلَنُ المشهودُ يُنقَل عنه محورُ المعجم كما ورد، لا معنًى مُثبَتًا."""

    run = run_text("اللَّهُ نُورٌ")

    gloss = interpret(
        run,
        (
            DeclaredRootAnnotation(
                word_index=1,
                root="نور",
                declared_by="يدُ المحرِّر",
                why="تعليقٌ مكتوبٌ بيدٍ لقياس طبقة التفسير",
            ),
        ),
    ).glosses[1]

    assert gloss.attestation is RootAttestation.ATTESTED
    assert gloss.quoted_axes
    assert gloss.carries_a_quoted_gloss


def test_an_unattested_declared_root_is_a_finding_not_a_hidden_failure() -> None:
    """غيرُ المشهودِ يخرج كما خرج، ولا يُنقَل عنه محورٌ ولا نوع."""

    run = run_text("اللَّهُ نُورٌ")

    gloss = interpret(
        run,
        (
            DeclaredRootAnnotation(
                word_index=1,
                root="سلسلةٌ_ليست_مدخلًا_في_المعجم",
                declared_by="يدُ المحرِّر",
                why="قياسُ عدم الشهادة بعينه",
            ),
        ),
    ).glosses[1]

    assert gloss.attestation is RootAttestation.NOT_ATTESTED
    assert gloss.quoted_axes == ()
    assert gloss.root_types == ()
    assert not gloss.carries_a_quoted_gloss


def test_a_word_without_an_annotation_declares_its_own_abstention() -> None:
    """كلمةٌ بلا تعليقٍ تخرج بامتناعٍ مُصرَّحٍ به، لا بإهمالٍ صامت."""

    interpretation = interpret(run_text("اللَّهُ نُورٌ"))

    assert len(interpretation.glosses) == 2
    for gloss in interpretation.glosses:
        assert gloss.annotation is None
        assert gloss.attestation is RootAttestation.NOT_LICENSED_FOR_THIS_WORD
    assert interpretation.glossed_words == 0


def test_the_masaq_bytes_are_named_absent_and_nothing_is_invented() -> None:
    """غيابُ بايتات MASAQ يُعرَض غيابًا مُسمًّى بموضعه وبصمته، بلا وسمٍ مختلَق."""

    interpretation = interpret(run_text("اللَّهُ نُورٌ"))

    assert interpretation.masaq in set(MasaqStanding)
    if interpretation.masaq is MasaqStanding.BYTES_ABSENT:
        rendered = render_interpretation(interpretation)
        assert "corpora/MASAQ.csv" in rendered
        assert "ALGHANEM_MASAQ_PATH" in rendered


def test_the_interpretation_reads_the_digest_verified_lexicon_bytes() -> None:
    """سندُ التفسير بصمةُ بايتاتٍ مُجمَّدةٍ في الشجرة، لا اسمُ معجمٍ مذكور."""

    interpretation = interpret(run_text("اللَّهُ نُورٌ"))

    assert interpretation.lexicon_digest == FROZEN_ROOT_TABLE.sha256_hex
    assert len(interpretation.lexicon_digest) == 64


def test_the_interpretation_refuses_an_annotation_outside_the_run() -> None:
    """تعليقٌ على كلمةٍ لم يقرأها السَّوق مردودٌ، فلا يُفسَّر ما لم يُشتَقّ."""

    stopped = run_text("اللَّهُ")

    with pytest.raises(ValueError):
        interpret(
            stopped,
            (
                DeclaredRootAnnotation(
                    word_index=0,
                    root="اله",
                    declared_by="يدُ المحرِّر",
                    why="قياسُ ردّ التعليق على سَوقٍ لم يبلغ الكلمات",
                ),
            ),
        )


def test_the_path_module_never_imports_the_interpretation_layer() -> None:
    """الاتّجاهُ مقطوعٌ بنيويًّا: التفسيرُ يستورد المسار ولا يستورده."""

    source = Path(composition_ifada_path.__file__).read_text(encoding="utf-8")

    assert "composition_ifada_interpretation" not in source
    assert "maqayis" not in source
    assert "masaq" not in source.lower()


# ————— تغييراتٌ بايتيّةٌ وترميزٌ غيرُ صالح —————


def _case(case_id: str) -> DeclaredCase:
    """الحالةُ المُعلَنةُ بمعرّفها؛ ومعرّفٌ غيرُ موجودٍ خطأُ اختبارٍ لا نتيجة."""

    return next(case for case in DECLARED_CASES if case.case_id == case_id)


def test_a_one_vowel_byte_change_changes_the_measured_reading() -> None:
    """إبدالُ ضمّةِ الأوّل كسرةً تغييرٌ بايتيٌّ يُغيّر الحكم، لا يُتجاوَز."""

    original = run_bytes(_case("isnad-1").source)
    mutated = run_bytes(_case("byte-mutation-vowel").source)

    assert len(mutated.source) == len(original.source)
    assert mutated.source != original.source
    assert original.ifada is IfadaStanding.مُفيد
    assert mutated.stop is PathStop.FIRST_MARK_IS_NOT_RAF
    assert mutated.ifada is IfadaStanding.غير_مقروء


def test_removing_the_space_byte_leaves_the_declared_scope() -> None:
    """حذفُ بايت البياض يُخرج المدخلَ من النطاق، فيقف بجنسه لا بخطأ."""

    mutated = run_bytes(_case("byte-mutation-space").source)

    assert mutated.reached is PathStage.WORD_SPLIT
    assert mutated.stop is PathStop.NOT_TWO_WORDS
    assert mutated.ifada is IfadaStanding.غير_مقروء


@pytest.mark.parametrize(
    "case_id",
    ["byte-truncated-utf8", "byte-invalid-lead", "byte-lone-continuation"],
)
def test_each_invalid_encoding_blocks_at_the_decode_transition(case_id: str) -> None:
    """صورُ الترميز غيرِ الصالح الثلاثُ تقف كلُّها عند فكِّ الترميز بشاهدها."""

    run = run_bytes(_case(case_id).source)
    first = run.stages[0]

    assert run.reached is PathStage.UTF8_BYTES
    assert run.outcome is StageOutcome.BLOCKED
    assert run.stop is PathStop.BYTES_ARE_NOT_UTF8
    assert first.evidence.startswith("utf8_decode_error:")
    assert first.output_digest is None
    assert run.words == ()


def test_the_declared_sample_covers_every_stop_genus_that_it_names() -> None:
    """العيّنةُ تبلغ كلَّ جنسٍ يُدّعى قياسُه، ولا يبقى جنسٌ بلا شاهدٍ إلّا مُسمًّى."""

    census = measure()
    counts = census.stop_counts

    reached_genera = {stop for stop, count in counts.items() if count}
    assert PathStop.BYTES_ARE_NOT_UTF8 in reached_genera
    assert PathStop.NOT_TWO_WORDS in reached_genera
    assert PathStop.PROCLITIC_JARR_UNDECIDED in reached_genera
    assert PathStop.MUDAF_CARRIES_TANWIN in reached_genera
    assert set(counts) - reached_genera == {PathStop.WORD_HALTED_IN_THE_WRITTEN_CHAIN}


# ————— المدخلُ الخامُّ وبصمتُه محفوظان —————


def test_every_declared_case_keeps_its_raw_bytes_and_their_digest() -> None:
    """كلُّ حالةٍ تحفظ بايتاتها الخامَّ وطولَها وبصمتَها وسببَ إدخالها."""

    assert DECLARED_CASES
    seen: set[str] = set()
    for case in DECLARED_CASES:
        assert type(case.source) is bytes
        assert case.byte_length == len(case.source)
        assert len(case.source_digest) == 64
        assert case.why.strip()
        assert case.source_digest not in seen
        seen.add(case.source_digest)


def test_the_request_carries_the_raw_bytes_as_hex_not_as_text() -> None:
    """محتوى الحالة في الطلب هو البايتاتُ ستَّ عشريّة، فلا يُستثنى ما لا يُفَكّ."""

    for case in DECLARED_CASES:
        assert bytes.fromhex(case.hex_content) == case.source

    invalid = _case("byte-invalid-lead")
    with pytest.raises(UnicodeDecodeError):
        invalid.source.decode("utf-8")
    assert bytes.fromhex(invalid.hex_content) == invalid.source


def test_a_case_without_bytes_is_refused() -> None:
    """حالةٌ بلا بايتاتٍ لا تُعلَن، فلا مدخلَ خامَّ لها يُبصَّم."""

    with pytest.raises(ValueError):
        DeclaredCase("empty", b"", "قياسُ ردّ الحالة الفارغة")


def test_the_run_reads_the_case_bytes_unchanged() -> None:
    """السَّوقُ يحفظ بايتاتِ مدخله كما وردت، فبصمتُه بصمتُها."""

    for case in DECLARED_CASES:
        run = run_bytes(case.source)
        assert run.source == case.source
        assert f"source_bytes:{case.source_digest}" in run.trace.events[0]


# ————— الإحصاءُ مربوطٌ بسجلّ التشغيل نفسِه —————


def test_the_census_is_bound_to_a_completed_run_record() -> None:
    """الإحصاءُ يحمل سجلَّ تشغيله وبصمةَ محتوى طلبه، ولا يُقرأ خارجَ سلطة."""

    census = measure()

    assert type(census.record) is ExperimentalRunRecord
    assert census.record.outcome_status is ExperimentalOutcomeStatus.COMPLETED
    assert census.record.request_content_digest.strip()
    assert census.record.operations_used == ("run_bytes",)


def test_the_census_agreement_with_its_record_is_measured_case_by_case() -> None:
    """موافقةُ الإحصاء للسجلّ تُقاس حالةً حالةً، ولا تُفترَض باشتراك الدالّة."""

    census = measure()
    tokens = census.record_tokens

    assert census.agrees_with_the_run_record
    assert set(tokens) == {case.case_id for case in DECLARED_CASES}
    for case, run in zip(census.cases, census.runs, strict=True):
        expected = ACCOUNTED_TOKEN if run.reached_ifada else UNACCOUNTED_TOKEN
        assert tokens[case.case_id] == expected


def test_the_record_accounts_exactly_the_runs_that_reached_ifada() -> None:
    """ما عدّه السجلُّ مُجابًا هو ما بلغ الإفادة بعينه، لا أكثرَ ولا أقلّ."""

    census = measure()
    accounted = {
        case_id
        for case_id, token in census.record_tokens.items()
        if token == ACCOUNTED_TOKEN
    }
    reached = {
        case.case_id
        for case, run in zip(census.cases, census.runs, strict=True)
        if run.reached_ifada
    }

    assert accounted == reached
    assert len(accounted) == census.reached_ifada


def test_the_rendered_census_publishes_the_raw_byte_identities() -> None:
    """العرضُ يُظهر سجلَّ التشغيل وبصمةَ كلّ مدخلٍ خامّ، فلا رقمَ بلا هويّة."""

    census = measure()
    rendered = render_census(census)

    assert census.record.run_id in rendered
    assert census.record.request_content_digest[:16] in rendered
    for case in census.cases:
        assert case.case_id in rendered
        assert case.source_digest[:12] in rendered
