"""اختباراتُ وصلة «كُتِبَ عَلَيْكُمُ الصِّيَامُ»: تعمل، ويتغيّر قرارُها بالدليل."""

from __future__ import annotations

import pytest

from alghanem.arabic import fard_sense_link as link
from alghanem.arabic.fard_sense_link import (
    THE_ANCHOR_AYAH,
    THE_LINK_READING_AT_MEASUREMENT,
    AbsentValueGenus,
    Claim,
    ClaimVerdict,
    FardSenseLinkError,
    PremiseGenus,
    PremiseName,
    absent_value_genus,
    anchor_ayah_text,
    available_premises,
    certificate,
    fard_segment,
    lexical_quotation,
    link_reading,
    link_reading_has_drifted,
    masaq_key_uniqueness,
    quotation_is_in_the_deposited_ayah,
    the_claims,
    verdicts_for,
)
from alghanem.arabic.maqayis_entry_boundary_audit import fold_for_comparison


def test_the_lexicon_segment_is_found_in_the_sealed_bytes() -> None:
    """مقطعُ الفرض مقروءٌ من المُودَع بحدودٍ مُشتقّةٍ لا مكتوبة."""

    start, end, segment = fard_segment()
    assert start < end
    assert "الفَرْضُ" in segment
    assert "كُتِبَ عَلَيْكُمُ" in segment


def test_the_lexicon_quotes_this_very_ayah_not_a_guess_from_the_root() -> None:
    """الرابطُ مقروءٌ من نصّ المادّة لا مُخمَّنٌ من أصل الجذر «جمع شيء إلى شيء»."""

    quotation = lexical_quotation()
    assert quotation_is_in_the_deposited_ayah()
    assert fold_for_comparison(quotation) in fold_for_comparison(anchor_ayah_text())


def test_the_deposited_line_really_is_the_anchor_ayah() -> None:
    """السطرُ المُعلَن يحمل الآيةَ بتمامها، فالعنوانُ مصادَمٌ لا مُصدَّق."""

    assert THE_ANCHOR_AYAH.sura == 2
    assert THE_ANCHOR_AYAH.ayah == 183
    text = fold_for_comparison(anchor_ayah_text())
    assert text.startswith("يا ايها الذين امنوا كتب عليكم الصيام")
    assert "لعلكم تتقون" in text


def test_the_fold_proves_the_utterance_matches_not_the_orthography() -> None:
    """الاقتباسُ والمُودَعُ مختلفا الرسم؛ فالمطابقةُ بعد طيٍّ مُعلَنٍ لا قبله."""

    assert lexical_quotation() not in anchor_ayah_text()
    assert quotation_is_in_the_deposited_ayah()


def test_the_link_produces_a_judgment_before_any_masaq_byte_lands() -> None:
    """ثلاثُ دعاوى نافذةٌ بالأدلّة الحاضرة؛ فالتشغيلُ أثرٌ لا وعد."""

    reading = link_reading()
    assert reading == THE_LINK_READING_AT_MEASUREMENT
    assert not link_reading_has_drifted()
    assert reading.the_link_produced_a_judgment
    assert reading.granted_claims == 3


def test_removing_a_necessary_premise_suspends_only_what_rests_on_it() -> None:
    """حذفُ دليلٍ لازمٍ يُعلّق تابعَه ويُبقي المستقلَّ عاملًا؛ وهذا تغيُّرُ القرار."""

    full = link.satisfied_premise_names()
    before = verdicts_for(full)
    assert before["اقتباس_المعجم_للموضع"] is ClaimVerdict.نافذ
    assert before["إسناد_معنى_الفرض"] is ClaimVerdict.نافذ

    after = verdicts_for(full - {PremiseName.مطابقة_الاقتباس})
    assert after["اقتباس_المعجم_للموضع"] is ClaimVerdict.معلق
    assert after["إسناد_معنى_الفرض"] is ClaimVerdict.معلق
    assert after["وقوع_اللفظ"] is ClaimVerdict.نافذ


def test_adding_the_pending_premises_opens_the_suspended_claims() -> None:
    """نزولُ المادّة المنتظَرة يفتح المعلَّق؛ فالتعليقُ انتظارُ دليلٍ لا امتناع."""

    opened = verdicts_for(frozenset(PremiseName))
    assert opened["البناء_للمجهول"] is ClaimVerdict.نافذ
    assert opened["تعلق_الجار_والمجرور"] is ClaimVerdict.نافذ


def test_no_evidence_whatsoever_opens_the_claim_that_they_actually_fasted() -> None:
    """«وقع الصيام» ممنوعٌ بنيويًّا، فلا تفتحه كلُّ الأدلّة مجتمعةً."""

    for satisfied in (
        frozenset(),
        link.satisfied_premise_names(),
        frozenset(PremiseName),
    ):
        assert verdicts_for(satisfied)["وقوع_الصيام_من_المخاطبين"] is ClaimVerdict.ممنوع


def test_a_barred_claim_is_not_a_suspended_one() -> None:
    """الممنوعُ يُعلَّل ولا يُعلَّق على مقدّمات، وإلّا صار وعدًا بفتحه يومًا."""

    barred = [claim for claim in the_claims() if claim.is_barred]
    assert len(barred) == 1
    assert barred[0].requires == ()
    assert barred[0].barring_reason
    assert "فرضُ الفعل غيرُ وقوعه" in barred[0].barring_reason


def test_a_barred_claim_may_not_carry_premises() -> None:
    """الرفضُ صريحٌ: ممنوعٌ بمقدّماتٍ تناقضٌ يُرَدّ عند الإنشاء."""

    with pytest.raises(FardSenseLinkError):
        Claim(
            name="x",
            statement="y",
            requires=(PremiseName.مقطع_الفرض,),
            bound="z",
            is_barred=True,
            barring_reason="سبب",
        )


def test_a_pending_premise_names_the_material_it_waits_for() -> None:
    """ما غاب يُسمّى ملفُّه بعينه، فلا يُترَك المنعُ بلا عنوانٍ يُرفَع به."""

    pending = [p for p in available_premises() if not p.is_satisfied]
    assert pending
    for premise in pending:
        assert premise.pending_material
    materials = {premise.pending_material for premise in pending}
    assert "corpora/MASAQ.csv" in materials


def test_the_suspension_is_per_claim_and_not_per_file() -> None:
    """غيابُ مصدرٍ يُعلّق دعاواه وحدَها؛ فالتبعيةُ على الدعوى لا على الملفّ."""

    without_masaq = frozenset(PremiseName) - {
        PremiseName.تجزئة_مساق,
        PremiseName.وسم_البناء_للمجهول,
    }
    verdicts = verdicts_for(without_masaq)
    assert verdicts["البناء_للمجهول"] is ClaimVerdict.معلق
    assert verdicts["إسناد_معنى_الفرض"] is ClaimVerdict.نافذ
    assert verdicts["وقوع_اللفظ"] is ClaimVerdict.نافذ


def test_a_missing_premise_is_named_and_not_merely_counted() -> None:
    """ما نقص يُسمّى بعينه في الشهادة، فلا يُقال «ناقصة» بلا تسمية."""

    satisfied = link.satisfied_premise_names()
    claim = next(c for c in the_claims() if c.name == "البناء_للمجهول")
    missing = claim.missing_under(satisfied)
    assert set(missing) == {
        PremiseName.تجزئة_مساق,
        PremiseName.وسم_البناء_للمجهول,
    }


def test_the_certificate_carries_loci_premises_bounds_and_what_is_pending() -> None:
    """الشهادةُ تحمل مواضعَ الأدلّة ومقدّماتِ الربط وحدودَه وما بقي معلَّقًا."""

    issued = certificate()
    assert issued["anchor"] == "2:183"
    assert issued["maqayis_digest"]
    assert len(issued["premises"]) == 7
    assert len(issued["claims"]) == 6
    for claim in issued["claims"]:
        assert claim["bound"]
        assert claim["verdict"] in {verdict.name for verdict in ClaimVerdict}
    for premise in issued["premises"]:
        assert premise["locus"]
        assert premise["source"]


def test_the_transmitted_is_marked_and_nothing_is_derived_from_the_116() -> None:
    """المنقولُ مُمَيَّزٌ من المشتقّ، ولا تُقرأ الشهادةُ استنباطًا من الـ١١٦."""

    issued = certificate()
    assert issued["derived_from_the_116"] is False
    assert not any(
        premise.genus is PremiseGenus.مستنبط_من_الـ116
        for premise in available_premises()
    )
    by_name = {claim["name"]: claim for claim in issued["claims"]}
    assert by_name["البناء_للمجهول"]["transmitted_not_derived"] is True
    assert by_name["إسناد_معنى_الفرض"]["transmitted_not_derived"] is False


def test_the_passive_tag_is_bounded_as_transmitted_not_discovered() -> None:
    """وَسْمُ البناء للمجهول منقولٌ، وحدُّه يمنع قراءتَه اكتشافًا من الـ١١٦."""

    claim = next(c for c in the_claims() if c.name == "البناء_للمجهول")
    assert "منقولٌ" in claim.bound
    assert "لا مستنبطٌ من الـ١١٦" in claim.bound


def test_absent_values_are_classed_and_never_turned_into_letters() -> None:
    """`None` و`(null)` علاماتٌ تقنيّةٌ لا حروفٌ ولا عناصرُ مقدَّرةٌ بغير دليل."""

    assert absent_value_genus(None) is AbsentValueGenus.علامة_تقنية
    assert absent_value_genus("(null)") is AbsentValueGenus.علامة_تقنية
    assert absent_value_genus("None") is AbsentValueGenus.علامة_تقنية
    assert absent_value_genus("  ") is AbsentValueGenus.قيمة_مفقودة
    assert absent_value_genus("كتب") is None


def test_no_absence_is_classed_as_an_elided_element_without_a_witness() -> None:
    """لا تُصنَّف خانةٌ خاليةٌ «عنصرًا مقدَّرًا موثَّقًا» إلّا بشاهدٍ يُحال إليه."""

    for value in (None, "", "(null)", "None", "null", "nan"):
        assert absent_value_genus(value) is not AbsentValueGenus.عنصر_مقدر_موثق


def test_the_key_uniqueness_is_withheld_until_the_copy_is_present() -> None:
    """الفرادةُ خاصّةُ نسخةٍ: لا تُدَّعى قبل نزول البايتات ولا تُورَث عن غيرها."""

    from alghanem.arabic.masaq_corpus_deposit import masaq_bytes_are_resolvable

    reading = masaq_key_uniqueness()
    if masaq_bytes_are_resolvable():
        assert reading is not None
        records, keys = reading
        assert records > 0 and keys > 0
    else:
        assert reading is None


def test_this_module_issues_no_birth_and_reads_no_kernel() -> None:
    """تسجيلٌ لا سلطة: لا ولادةَ ولا تجميدَ `E0`، ولا استيرادَ من `kernel/`."""

    import ast
    from pathlib import Path

    tree = ast.parse(Path(link.__file__).read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    assert not any("kernel" in name for name in imported)
