"""اختباراتُ إيداع هرمية إعادة بناء الكلمة: البصمةُ من الملفّ، ولا حسمَ ولا رفعَ حجب."""

from __future__ import annotations

import hashlib
from dataclasses import fields

import pytest

from alghanem.arabic.gflk_specification_deposit import (
    ConflictStanding,
    ProvenanceGenus,
)
from alghanem.arabic.word_hierarchy_deposit import (
    HIERARCHY_RELATIVE_PATH,
    NOT_ISSUED_BY_THIS_TREE,
    SUBMITTED_FREEZE_IDENTIFIERS,
    SUPERSEDED_CLAIMS,
    WORD_HIERARCHY_CONFLICTS,
    WORD_HIERARCHY_DEPOSIT,
    WORD_HIERARCHY_NODES,
    WORD_HIERARCHY_NUMERIC_CLAIMS,
    HierarchyConflict,
    HierarchyLevel,
    HierarchyNode,
    HierarchyNumericClaim,
    SubmittedFreezeIdentifier,
    SupersededClaim,
    WordHierarchyDeposit,
    WordHierarchyDepositError,
    hierarchy_digest,
    hierarchy_path,
    read_hierarchy_bytes,
)
from alghanem.arabic.word_structure_dictionary import MEASURED_LAYERS, WITHHELD_LAYERS
from alghanem.arabic.word_structure_dictionary_preregistration import (
    DictionaryLayer,
    LayerEpistemicStanding,
)

_ANY_CONDITION = "إيداعُ مدوّنةٍ مُبصَّمة"


def test_the_deposited_document_exists_in_the_tree() -> None:
    assert hierarchy_path().is_file()
    assert read_hierarchy_bytes()


def test_the_digest_is_rederived_from_the_file_not_stored() -> None:
    """البصمةُ تُشتَقّ من بايتات الملفّ في كلّ نداء، فلا تُصادق على غيره."""

    expected = hashlib.sha256(read_hierarchy_bytes()).hexdigest()
    assert hierarchy_digest() == expected
    assert WORD_HIERARCHY_DEPOSIT.digest() == expected


def test_the_deposit_declares_a_foreign_genus_and_three_texts() -> None:
    assert (
        WORD_HIERARCHY_DEPOSIT.genus is ProvenanceGenus.PROSE_FROM_ANOTHER_CONVERSATION
    )
    assert WORD_HIERARCHY_DEPOSIT.arrival_date == "2026-09-15"
    assert WORD_HIERARCHY_DEPOSIT.relative_path == HIERARCHY_RELATIVE_PATH
    assert WORD_HIERARCHY_DEPOSIT.deposited_versions == 3


def test_depositing_the_corrected_version_alone_is_refused() -> None:
    """إيداعُ المُصحَّح وحده يمحو أنّ دعاوى سُحبت؛ فالنسختان معًا أو لا إيداع."""

    with pytest.raises(WordHierarchyDepositError):
        WordHierarchyDeposit(
            genus=ProvenanceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
            arrival_date="2026-09-15",
            relative_path=HIERARCHY_RELATIVE_PATH,
            deposited_versions=1,
        )


def test_both_versions_are_deposited_verbatim_in_the_document() -> None:
    """§٢ و§٢-أ و§٢-ب تحمل النصوصَ كما وصلت، فلا يُحرَّر المُودَع صامتًا."""

    text = read_hierarchy_bytes().decode("utf-8")
    assert "## ٢ — النصّ المُودَع حرفيًّا (النسخة الثانية)" in text
    assert "## ٢-أ — النصّ المُودَع حرفيًّا (النسخة الأولى، المنسوخة)" in text
    assert "## ٢-ب — النصّ المُودَع حرفيًّا (التجميد الثالث الوارد)" in text
    # سطورٌ من النسخة الثانية وحدها
    assert "> ## المستوى ٥ — المبني (عابر لكل ما سبق)" in text.replace("\u200f", "")
    assert "مسحوب من الخواص الموثوقة" in text
    # سطورٌ من النسخة الأولى وحدها، لم تُحذَف عند نسخها
    assert "صفر خرق/8,756" in text
    assert "٩٥.٦٧٪" in text
    assert "6/6 أمثلة" in text
    # سطورٌ من التجميد الثالث وحده، بما فيها ما يُخالف الشجرة
    assert "**تم التجميد — SPEECH-PARTS-AND-COMPOSITION-AR-1**" in text
    assert "مكتشَف الآن، يُفسِّر كل ما تبقّى" in text
    assert "يُلغي كل من 4.76% و1% المذكورتين سابقًا" in text


def test_the_third_text_carries_a_header_denying_it_is_frozen_here() -> None:
    """إعلانُ تجميدٍ خارجيٍّ لا يُقرأ تجميدًا هنا؛ والترويسةُ تسبق النصّ."""

    text = read_hierarchy_bytes().decode("utf-8")
    header = text.index("**ترويسةٌ لازمةٌ قبل النصّ:**")
    body = text.index("**تم التجميد — SPEECH-PARTS-AND-COMPOSITION-AR-1**")
    assert header < body
    assert "غيرُ موجودين في هذه الشجرة" in text
    assert "محفوظٌ بحروفه ليُراجَع لا ليُعمَل به" in text


def test_the_document_declares_deferred_standing_and_no_authority() -> None:
    text = read_hierarchy_bytes().decode("utf-8")
    assert "`DEFER`" in text
    assert "لا تلد كائنًا في النواة" in text
    assert "ولا ترفع حجبًا عن طبقةٍ" in text


def test_every_node_carries_a_standing_from_the_existing_closed_vocabulary() -> None:
    """المنازلُ من المفردة الرباعية القائمة؛ ولا خامسةَ تُفتَح للإيداع."""

    assert WORD_HIERARCHY_NODES
    for node in WORD_HIERARCHY_NODES:
        assert node.standing in set(LayerEpistemicStanding)
        assert node.tree_reference.strip()
    assert len(LayerEpistemicStanding) == 4


def test_every_hierarchy_level_is_represented_once_at_least() -> None:
    assert {node.level for node in WORD_HIERARCHY_NODES} == set(HierarchyLevel)
    assert len(HierarchyLevel) == 6


def test_a_measured_standing_is_bound_to_an_actually_measured_layer() -> None:
    """لا عقدةَ «مقيسة» إلا وطبقتُها في `MEASURED_LAYERS` بعينها."""

    measured = [
        node
        for node in WORD_HIERARCHY_NODES
        if node.standing is LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC
    ]
    assert measured
    for node in measured:
        assert node.dictionary_layer in MEASURED_LAYERS


def test_a_withheld_layer_cannot_be_declared_measured_by_this_deposit() -> None:
    """رفعُ حجبٍ بكتابة منزلةٍ في إيداعٍ ممنوعٌ عند الإنشاء لا بالمراجعة."""

    withheld = WITHHELD_LAYERS[0].layer
    with pytest.raises(WordHierarchyDepositError):
        HierarchyNode(
            node_id="محاولةُ ترقية",
            level=HierarchyLevel.SYLLABLE,
            what_the_hierarchy_says="المقطعُ مقيس",
            standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
            tree_reference="مرجع",
            dictionary_layer=withheld,
        )


def test_a_measured_standing_without_a_named_layer_is_refused() -> None:
    with pytest.raises(WordHierarchyDepositError):
        HierarchyNode(
            node_id="قياسٌ بلا مقيسٍ عليه",
            level=HierarchyLevel.LETTER,
            what_the_hierarchy_says="شيءٌ مقيس",
            standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
            tree_reference="مرجع",
        )


def test_the_four_withheld_layers_are_still_withheld_after_the_deposit() -> None:
    """الإيداعُ لا يرفع حجبًا: الطبقاتُ الأربعُ تبقى بعده كما كانت قبله."""

    withheld = {entry.layer for entry in WITHHELD_LAYERS}
    assert withheld == {
        DictionaryLayer.SYLLABLES_AND_WAZN,
        DictionaryLayer.PHONETIC_FEATURES,
        DictionaryLayer.AL_ANALYSIS,
        DictionaryLayer.JARAD_ANALYSIS,
    }
    assert not withheld & set(MEASURED_LAYERS)


def test_every_superseded_claim_names_its_successor_and_reason() -> None:
    assert SUPERSEDED_CLAIMS
    for claim in SUPERSEDED_CLAIMS:
        assert claim.first_version_said.strip()
        assert claim.second_version_says.strip()
        assert claim.why_it_was_withdrawn.strip()


def test_the_four_named_withdrawals_are_recorded() -> None:
    loci = " | ".join(claim.locus for claim in SUPERSEDED_CLAIMS)
    assert "الصفة" in loci
    assert "مجرد/مزيد" in loci
    assert "الزيادة الصرفية" in loci
    assert "همزة الوصل" in loci


def test_the_gap_withdrawal_names_a_reason_unlike_the_six_silent_figures() -> None:
    """سحبُ ٤٫٧٦٪ جاء بسببٍ مذكور، فلا يُسجَّل «ساقطًا بلا سبب»."""

    gap = [claim for claim in SUPERSEDED_CLAIMS if "الفجوة" in claim.locus]
    assert len(gap) == 1
    assert "بإدغام عابر" in gap[0].why_it_was_withdrawn
    assert "لا `WITHDRAWN_WITHOUT_A_STATED_REASON`" in gap[0].why_it_was_withdrawn
    assert "«١٪» لم تصل هذه الشجرةَ قطّ" in gap[0].second_version_says


def test_a_withdrawal_without_a_reason_is_refused() -> None:
    with pytest.raises(WordHierarchyDepositError):
        SupersededClaim(
            locus="§٢",
            first_version_said="دعوى",
            second_version_says="دعوى أخرى",
            why_it_was_withdrawn="   ",
        )


def test_every_number_is_marked_not_rederivable_with_a_named_reason() -> None:
    """لا رقمَ يُقرأ مقيسًا في هذه الشجرة: لكلٍّ سببُ تعذّرٍ وشرطُ اشتقاق."""

    assert WORD_HIERARCHY_NUMERIC_CLAIMS
    for claim in WORD_HIERARCHY_NUMERIC_CLAIMS:
        assert claim.not_rederivable_because.strip()
        assert claim.what_would_make_it_rederivable.strip()


def test_the_numeric_register_covers_the_figures_of_both_versions() -> None:
    figures = {claim.figure for claim in WORD_HIERARCHY_NUMERIC_CLAIMS}
    assert {"35.7%", "4.46%", "4.76%", "2/2", "3/3", "20/20", "×43-160"} <= figures
    zero_claims = [figure for figure in figures if figure.startswith("صفر")]
    assert len(zero_claims) >= 3


def test_a_number_without_a_rederivation_condition_is_refused() -> None:
    with pytest.raises(WordHierarchyDepositError):
        HierarchyNumericClaim(
            figure="99%",
            locus="§٢",
            claim_text="دعوى",
            not_rederivable_because="لا مدوّنة",
            what_would_make_it_rederivable="  ",
        )


def test_a_residue_defined_zero_is_refused_without_a_dependency_tag() -> None:
    """فئةٌ عُرِّفت بالباقي لا يتبقّى بعدها شيء؛ فصفرُها تابعٌ يُسمّي ما يقوم عليه."""

    with pytest.raises(WordHierarchyDepositError):
        HierarchyNumericClaim(
            figure="صفر تمامًا",
            locus="§٢-ب",
            claim_text="صفرُ فجوةٍ بعد تفسير كلّ المرشَّحين",
            not_rederivable_because="لا مدوّنة",
            what_would_make_it_rederivable=_ANY_CONDITION,
            is_residue_defined=True,
        )


def test_the_same_zero_is_accepted_once_it_names_what_it_rests_on() -> None:
    claim = HierarchyNumericClaim(
        figure="صفر تمامًا",
        locus="§٢-ب",
        claim_text="صفرُ فجوةٍ بعد تفسير كلّ المرشَّحين",
        not_rederivable_because="لا مدوّنة",
        what_would_make_it_rederivable=_ANY_CONDITION,
        depends_on_figure="مُغلَق 100% — التركيب النحويّ",
        is_residue_defined=True,
    )
    assert claim.depends_on_figure == "مُغلَق 100% — التركيب النحويّ"


def test_an_empty_dependency_tag_is_refused() -> None:
    with pytest.raises(WordHierarchyDepositError):
        HierarchyNumericClaim(
            figure="صفر",
            locus="§٢-ب",
            claim_text="دعوى",
            not_rederivable_because="لا مدوّنة",
            what_would_make_it_rederivable=_ANY_CONDITION,
            depends_on_figure="   ",
        )


def test_the_three_results_of_the_third_text_are_recorded_as_one_witness() -> None:
    """إغلاقُ النحويّ وصفرُ الفجوة وصفرُ المزجيّ مخرجُ فئةٍ واحدةٍ لا ثلاثةُ شهود."""

    by_figure = {claim.figure: claim for claim in WORD_HIERARCHY_NUMERIC_CLAIMS}
    closure = by_figure["مُغلَق 100% — التركيب النحويّ"]
    assert closure.is_residue_defined
    assert closure.depends_on_figure == "98.9%"
    for dependent in (
        "صفر تمامًا — الفجوة بين الكلمة المنطقيّة والفراغيّة",
        "صفر حالة — التركيب المزجيّ",
    ):
        assert by_figure[dependent].depends_on_figure == closure.figure
        assert by_figure[dependent].is_residue_defined


def test_every_dependency_tag_points_at_a_figure_in_the_same_register() -> None:
    figures = {claim.figure for claim in WORD_HIERARCHY_NUMERIC_CLAIMS}
    for claim in WORD_HIERARCHY_NUMERIC_CLAIMS:
        if claim.depends_on_figure is None:
            continue
        assert claim.depends_on_figure in figures
        assert claim.depends_on_figure != claim.figure


def test_the_third_texts_figures_are_registered_not_rederivable() -> None:
    figures = {claim.figure for claim in WORD_HIERARCHY_NUMERIC_CLAIMS}
    assert {"98.9%", "56%", "23%"} <= figures
    assert "مُغلَق 100% — التركيب النحويّ" in figures


def test_a_submitted_freeze_identifier_is_kept_but_disowned() -> None:
    """مُعرِّفُ تجميدٍ واردٍ محفوظٌ بحروفه ومعه أنّه غيرُ صادرٍ عن هذه الشجرة."""

    identifiers = {entry.identifier for entry in SUBMITTED_FREEZE_IDENTIFIERS}
    assert identifiers == {
        "SPEECH-PARTS-AND-COMPOSITION-AR-1",
        "WAQF-SEL-MARKER-PROXY-AR-1",
    }
    for entry in SUBMITTED_FREEZE_IDENTIFIERS:
        assert entry.not_issued_by_this_tree == NOT_ISSUED_BY_THIS_TREE
        assert "ليُراجَع لا ليُعمَل به" in entry.not_issued_by_this_tree


def test_a_submitted_freeze_identifier_without_the_disclaimer_is_refused() -> None:
    with pytest.raises(WordHierarchyDepositError):
        SubmittedFreezeIdentifier(
            identifier="SOME-FREEZE-AR-1",
            what_it_declares="تجميدٌ ما",
            not_issued_by_this_tree="   ",
        )


def test_neither_submitted_identifier_exists_anywhere_else_in_the_tree() -> None:
    """المُعرِّفان لا يوجدان في الشجرة إلا في هذا الإيداع وفي وثيقته واختبارها."""

    root = hierarchy_path().parent.parent.parent
    allowed = {
        root / "docs" / "reference" / "word_hierarchy_rebuild.md",
        root / "src" / "alghanem" / "arabic" / "word_hierarchy_deposit.py",
        root / "tests" / "arabic" / "test_word_hierarchy_deposit.py",
    }
    for identifier in (
        "SPEECH-PARTS-AND-COMPOSITION-AR-1",
        "WAQF-SEL-MARKER-PROXY-AR-1",
    ):
        for folder, suffix in (("src", ".py"), ("docs", ".md"), ("tests", ".py")):
            for path in (root / folder).rglob(f"*{suffix}"):
                if path in allowed:
                    continue
                assert identifier not in path.read_text(encoding="utf-8")


def test_no_conflict_carries_a_resolution_field() -> None:
    """التعارضُ يحمل شرطَ حسمه ولا يحمل حسمًا؛ ولا عضوَ «محسوم» في المنزلة."""

    names = {field.name for field in fields(HierarchyConflict)}
    assert "resolution" not in names
    assert "resolved" not in names
    assert "verdict" not in names
    assert {member.name for member in ConflictStanding} == {
        "RECORDED_UNRESOLVED",
        "BLOCKS_IMPORT_UNTIL_RESOLVED",
    }


def test_every_conflict_names_its_locus_reference_and_resolution_condition() -> None:
    assert WORD_HIERARCHY_CONFLICTS
    for conflict in WORD_HIERARCHY_CONFLICTS:
        assert conflict.locus_in_hierarchy.strip()
        assert conflict.tree_reference.strip()
        assert conflict.what_would_resolve_it.strip()


def test_the_ten_import_barriers_are_recorded() -> None:
    barriers = [
        conflict
        for conflict in WORD_HIERARCHY_CONFLICTS
        if conflict.standing is ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED
    ]
    assert len(barriers) == 10
    loci = " | ".join(conflict.locus_in_hierarchy for conflict in barriers)
    assert "همزة الوصل" in loci
    assert "الشدّة" in loci
    assert "المقطع" in loci
    assert "المخرج" in loci
    assert "الصفة" in loci
    assert "المبنيّ" in loci
    assert "فئةُ الإدغام الثالثة" in loci
    assert "وكيلُ الوقف" in loci


def test_the_residue_defined_closure_is_blocked_by_the_standing_refusal() -> None:
    """فئةٌ كُتبت بعد فحص البواقي ليست شاهدًا للقاعدة التي أنقذتها."""

    closure = [
        conflict
        for conflict in WORD_HIERARCHY_CONFLICTS
        if "فئةُ الإدغام الثالثة" in conflict.locus_in_hierarchy
    ]
    assert len(closure) == 1
    assert (
        "RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE"
        in closure[0].tree_reference
    )
    assert closure[0].standing is ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED
    assert "قبل الفحص" in closure[0].what_would_resolve_it


def test_the_waqf_proxy_is_blocked_because_the_signal_is_undefined() -> None:
    """الإشارةُ المُميِّزةُ غيرُ مُعرَّفةٍ في المرماز، لا ضعيفةٌ ولا ناقصة."""

    proxy = [
        conflict
        for conflict in WORD_HIERARCHY_CONFLICTS
        if "وكيلُ الوقف" in conflict.locus_in_hierarchy
    ]
    assert len(proxy) == 1
    assert (
        "PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN"
        in proxy[0].tree_reference
    )
    assert proxy[0].standing is ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED


def test_the_fifth_level_conflict_cites_the_three_refusing_texts() -> None:
    """المستوى الخامس يصطدم بنصوصٍ رافضةٍ قائمة، لا برقمٍ بلا مدوّنة فحسب."""

    mabni = [
        conflict
        for conflict in WORD_HIERARCHY_CONFLICTS
        if "المستوى ٥" in conflict.locus_in_hierarchy
    ]
    assert len(mabni) == 1
    reference = mabni[0].tree_reference
    assert "MabniIsNotAnUnchangedSurfaceForm" in reference
    assert "EnumeratedExamplesAreNotAnExhaustiveCriterion" in reference
    assert "MAWSUL_WORDS" in mabni[0].this_tree_says
    assert mabni[0].standing is ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED


def test_an_agreement_is_recorded_as_an_agreement_not_as_a_conflict() -> None:
    """التوافقُ غيرُ المُسجَّل يُقرأ بعد جلساتٍ خلافًا، فيُسجَّل ولا يُحسَم."""

    jarad = [
        conflict
        for conflict in WORD_HIERARCHY_CONFLICTS
        if "مجرد/مزيد" in conflict.locus_in_hierarchy
    ]
    assert len(jarad) == 1
    assert jarad[0].standing is ConflictStanding.RECORDED_UNRESOLVED
    assert "توافقٌ" in jarad[0].what_would_resolve_it


def test_a_conflict_without_a_resolution_condition_is_refused() -> None:
    with pytest.raises(WordHierarchyDepositError):
        HierarchyConflict(
            locus_in_hierarchy="§٢",
            hierarchy_says="شيء",
            this_tree_says="شيء آخر",
            tree_reference="مرجع",
            what_would_resolve_it="   ",
            standing=ConflictStanding.RECORDED_UNRESOLVED,
        )


def test_the_deposit_carries_no_analysis_function_and_no_result_field() -> None:
    """إيداعٌ لا مُحلِّل: لا دالّةَ تحليلٍ ولا حقلَ نتيجةٍ ولا حسم."""

    from alghanem.arabic import word_hierarchy_deposit as module

    for name in ("analyze_word", "analyze", "classify", "decide", "resolve"):
        assert not hasattr(module, name)
    forbidden = ("result", "verdict", "birth", "certificate", "resolution", "resolved")
    for dataclass_type in (
        HierarchyNode,
        SupersededClaim,
        HierarchyNumericClaim,
        HierarchyConflict,
        SubmittedFreezeIdentifier,
        WordHierarchyDeposit,
    ):
        for declared in fields(dataclass_type):
            assert not any(token in declared.name.lower() for token in forbidden)


def test_the_deposit_does_not_import_the_kernel() -> None:
    source = (
        hierarchy_path().parent.parent.parent
        / "src"
        / "alghanem"
        / "arabic"
        / "word_hierarchy_deposit.py"
    ).read_text(encoding="utf-8")
    assert "alghanem.kernel" not in source
    assert "from ..kernel" not in source
