"""سجلّ دعاوى التقارب: تسجيلٌ وموقفٌ مُسبَّب، لا حكم تقارب.

تُثبِّت هذه الاختبارات خمسة أمور: المفردات مغلقة وقيمة القبول مُعلَنة غير قابلة
للبناء، ودعوى الأسماء الشرعية مردودةٌ بصيغتها ردًّا باتًّا بتسمية التصنيفين
المدموجين، ودعوى المتوسطة مُسجَّلة غيابًا مُسمّى لا صمتًا، والتغطية تسبق الحكم
فلا دعوى تُترَك بلا موقف، والوحدة خاملة سلطويًّا لا تحرّك بوّابةً ولا تغيّر
تدقيقًا خارجيًّا.
"""

import json
from dataclasses import fields, replace
from pathlib import Path

import pytest

from alghanem.arabic.convergence_claim_register import (
    CONVERGENCE_AUTHORITY_NOTE,
    CONVERGENCE_CLAIM_REGISTER,
    CONVERGENCE_NOT_APPLICABLE_TEXT,
    CONVERGENCE_SCOPE_NOTE,
    CONVERGENCE_SUCCESS_TITLE_IS_WITHHELD,
    NO_CONVERGENCE_AUTHORITY_NOTE,
    ClaimStanding,
    ConvergenceClaim,
    ConvergenceClaimRecord,
    ConvergenceClaimRegister,
    ConvergenceClaimRegisterError,
    MergedClassification,
    NamedRefusal,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"

_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)

_SHARI = ConvergenceClaim.SHARI_NAMES_CONVERGENCE
_MUTAWASSITA = ConvergenceClaim.MUTAWASSITA_SECTION


def test_the_closed_vocabularies_are_exactly_the_declared_values() -> None:
    assert tuple(claim.value for claim in ConvergenceClaim) == (
        "تقارب_تصنيف_الأسماء_الشرعية",
        "قسم_المتوسطة",
    )
    assert tuple(standing.value for standing in ClaimStanding) == (
        "مرفوضة_بفحصٍ_مباشر",
        "مصدر_مُسمّى_غائب",
        "مقبولة_بسلطة_تقارب",
    )


def test_the_upheld_standing_is_declared_but_unconstructible() -> None:
    record = CONVERGENCE_CLAIM_REGISTER.record_for(_SHARI)

    with pytest.raises(ConvergenceClaimRegisterError) as raised:
        replace(record, standing=ClaimStanding.UPHELD_BY_CONVERGENCE_AUTHORITY)

    assert "غير قابلة للبناء" in str(raised.value)


def test_the_shari_names_claim_is_refuted_as_stated_not_deferred() -> None:
    record = CONVERGENCE_CLAIM_REGISTER.record_for(_SHARI)

    assert record.standing is ClaimStanding.REFUTED_BY_DIRECT_INSPECTION
    assert record.is_refuted_as_stated is True
    assert "لا معلَّقٌ في انتظار شهادةٍ لاحقة" in record.ground
    assert "RefusalIsNotDeferral" in {refusal.name for refusal in record.refusals}


def test_the_refutation_names_both_merged_classifications_by_module() -> None:
    record = CONVERGENCE_CLAIM_REGISTER.record_for(_SHARI)
    modules = {merged.module for merged in record.merged_classifications}

    assert modules == {
        "lafz_madlul_relation_formal.py",
        "kulli_juzi_formal.py",
    }
    borrowed = {
        merged.module: merged.borrowed_values
        for merged in record.merged_classifications
    }
    assert borrowed["lafz_madlul_relation_formal.py"] == (
        "متباين",
        "مترادف",
        "مشترك",
    )
    assert borrowed["kulli_juzi_formal.py"] == ("متواطئ", "مشكِّك")


def test_a_refutation_by_merger_needs_two_distinct_named_classifications() -> None:
    record = CONVERGENCE_CLAIM_REGISTER.record_for(_SHARI)

    with pytest.raises(ConvergenceClaimRegisterError):
        replace(record, merged_classifications=())
    with pytest.raises(ConvergenceClaimRegisterError):
        replace(
            record,
            merged_classifications=(record.merged_classifications[0],),
        )
    duplicated = replace(
        record.merged_classifications[1],
        module=record.merged_classifications[0].module,
    )
    with pytest.raises(ConvergenceClaimRegisterError):
        replace(
            record,
            merged_classifications=(record.merged_classifications[0], duplicated),
        )


def test_the_absent_term_is_declared_on_the_absence_claim_alone() -> None:
    absence = CONVERGENCE_CLAIM_REGISTER.record_for(_MUTAWASSITA)
    refuted = CONVERGENCE_CLAIM_REGISTER.record_for(_SHARI)

    assert absence.standing is ClaimStanding.NAMED_SOURCE_ABSENT
    assert absence.absent_term == "المتوسطة"
    assert absence.merged_classifications == ()
    assert refuted.absent_term == CONVERGENCE_NOT_APPLICABLE_TEXT

    with pytest.raises(ConvergenceClaimRegisterError):
        replace(absence, absent_term=CONVERGENCE_NOT_APPLICABLE_TEXT)
    with pytest.raises(ConvergenceClaimRegisterError):
        replace(refuted, absent_term="المتوسطة")
    with pytest.raises(ConvergenceClaimRegisterError):
        replace(
            absence,
            merged_classifications=refuted.merged_classifications,
        )


def test_the_absence_refuses_silent_synonym_substitution_by_name() -> None:
    absence = CONVERGENCE_CLAIM_REGISTER.record_for(_MUTAWASSITA)
    names = {refusal.name for refusal in absence.refusals}

    assert "NoSynonymSubstitutionWithoutInstruction" in names
    assert "AbsenceIsNamedNotSilent" in names


def test_every_record_names_at_least_one_refusal() -> None:
    for record in CONVERGENCE_CLAIM_REGISTER.records:
        assert record.refusals
        with pytest.raises(ConvergenceClaimRegisterError):
            replace(record, refusals=())
        with pytest.raises(ConvergenceClaimRegisterError):
            replace(record, refusals=(record.refusals[0], record.refusals[0]))


def test_blank_text_is_refused_everywhere_it_is_required() -> None:
    record = CONVERGENCE_CLAIM_REGISTER.record_for(_SHARI)

    with pytest.raises(ConvergenceClaimRegisterError):
        replace(record, statement="   ")
    with pytest.raises(ConvergenceClaimRegisterError):
        replace(record, ground="")
    with pytest.raises(ConvergenceClaimRegisterError):
        NamedRefusal(name="  ", statement="بيان")
    with pytest.raises(ConvergenceClaimRegisterError):
        MergedClassification(
            module="unit.py", classification="تصنيف", borrowed_values=()
        )
    with pytest.raises(ConvergenceClaimRegisterError):
        MergedClassification(
            module="unit.py",
            classification="تصنيف",
            borrowed_values=("متباين", "متباين"),
        )


def test_coverage_precedes_judgement_and_duplicates_are_refused() -> None:
    records = CONVERGENCE_CLAIM_REGISTER.records

    assert CONVERGENCE_CLAIM_REGISTER.claims == (_SHARI, _MUTAWASSITA)
    with pytest.raises(ConvergenceClaimRegisterError):
        ConvergenceClaimRegister(records=(records[0],))
    with pytest.raises(ConvergenceClaimRegisterError):
        ConvergenceClaimRegister(records=records + (records[0],))
    with pytest.raises(ConvergenceClaimRegisterError):
        ConvergenceClaimRegister(records=("دعوى",))  # type: ignore[arg-type]
    with pytest.raises(ConvergenceClaimRegisterError):
        CONVERGENCE_CLAIM_REGISTER.record_for("قسم_المتوسطة")  # type: ignore[arg-type]


def test_no_verdict_is_constructible_and_no_claim_is_operative() -> None:
    assert CONVERGENCE_CLAIM_REGISTER.convergence_verdict_is_constructible is False
    assert all(
        record.claim_is_operative is False
        for record in CONVERGENCE_CLAIM_REGISTER.records
    )
    assert "لا عنوان نجاح" in CONVERGENCE_SUCCESS_TITLE_IS_WITHHELD
    assert "لا آلة تقاربٍ في هذا المستودع" in NO_CONVERGENCE_AUTHORITY_NOTE
    assert "ClaimRegister != ConvergenceVerdict" in CONVERGENCE_AUTHORITY_NOTE
    assert "ولا تُعمّم" in CONVERGENCE_SCOPE_NOTE


def test_no_register_type_carries_a_result_or_verdict_field() -> None:
    forbidden = ("result", "outcome_value", "verdict", "birth", "certificate", "proof")

    for dataclass_type in (
        NamedRefusal,
        MergedClassification,
        ConvergenceClaimRecord,
        ConvergenceClaimRegister,
    ):
        for field in fields(dataclass_type):
            assert not any(token in field.name for token in forbidden)


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "convergence_claim_register.py"
    ).read_text(encoding="utf-8")

    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )

    assert imports
    assert not any("kernel" in line for line in imports)


@pytest.mark.parametrize("card", _CARDS)
def test_the_register_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )

    CONVERGENCE_CLAIM_REGISTER.record_for(_SHARI)

    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
