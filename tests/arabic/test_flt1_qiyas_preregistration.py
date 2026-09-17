"""شواهدُ إيداع قانون القياس: النصُّ أمينٌ، والآلةُ مُرتَّبةٌ، ولا قراءةَ بعدُ."""

from __future__ import annotations

import pathlib

import pytest

from alghanem.arabic.flt1_hypothesis import FLT1_TEXT_DIGEST
from alghanem.arabic.flt1_preregistration import (
    FLT1_FROZEN_SURFACES,
    WEAKER_REPRESENTATIONS,
)
from alghanem.arabic.flt1_qiyas_law import (
    FLT1_QIYAS_TEXT,
    FLT1_QIYAS_TEXT_DIGEST,
    REQUIRED_QIYAS_NOTATION_SITES,
    SUPERSESSION_RECORD,
    FidelityStanding,
    QiyasLawError,
    derive_qiyas_fidelity_report,
    qiyas_text_digest,
)
from alghanem.arabic.flt1_qiyas_preregistration import (
    DECISION_RULES,
    GATE_DECLARATIONS,
    GREAT_CHAIN,
    ORIGIN_DECLARATION,
    RECONSTRUCTION_TARGET,
    QiyasOutcome,
    QiyasPreregistrationError,
    flt1_qiyas_preregistration_digest,
    gate_named,
    rule_for_gate,
)


def test_the_frozen_text_carries_every_decisive_notation_site() -> None:
    report = derive_qiyas_fidelity_report()

    assert report.absent_sites == ()
    assert report.standing is FidelityStanding.TEXT_CARRIES_EVERY_DECISIVE_SITE
    assert len(report.present_sites) == len(REQUIRED_QIYAS_NOTATION_SITES)


def test_a_text_that_drops_the_negation_of_the_qadih_difference_diverges() -> None:
    mutilated = FLT1_QIYAS_TEXT.replace(
        r"\land \neg \Delta_q(O,F)", r"\land \Delta_q(O,F)"
    )
    report = derive_qiyas_fidelity_report(mutilated)

    assert "continuity-negated-qadih" in report.absent_sites
    assert report.standing is FidelityStanding.TEXT_DIVERGES_FROM_THE_LAW


def test_a_text_that_drops_the_effectiveness_clause_diverges() -> None:
    mutilated = FLT1_QIYAS_TEXT.replace(r"\operatorname{Effective}(\Delta_q)", "")
    report = derive_qiyas_fidelity_report(mutilated)

    assert "effective-qadih" in report.absent_sites


def test_the_digest_is_derived_from_the_text_not_transcribed() -> None:
    assert qiyas_text_digest() == FLT1_QIYAS_TEXT_DIGEST
    assert qiyas_text_digest(FLT1_QIYAS_TEXT + " ") != FLT1_QIYAS_TEXT_DIGEST


def test_supersession_names_the_superseded_text_without_touching_it() -> None:
    assert SUPERSESSION_RECORD.superseded_text_digest == FLT1_TEXT_DIGEST
    assert SUPERSESSION_RECORD.superseding_text_digest == FLT1_QIYAS_TEXT_DIGEST
    assert "لم يُقرَأ" in SUPERSESSION_RECORD.why_supersession_is_licensed_here
    assert (
        "ضبطٌ" in SUPERSESSION_RECORD.what_would_have_made_it_illegitimate
        or "رجعيٌّ" in SUPERSESSION_RECORD.what_would_have_made_it_illegitimate
    )


def test_a_text_cannot_supersede_itself() -> None:
    from alghanem.arabic.flt1_qiyas_law import SupersessionRecord

    with pytest.raises(QiyasLawError):
        SupersessionRecord(
            superseded_text_digest="a" * 64,
            superseding_text_digest="a" * 64,
            what_is_kept_from_the_superseded="شيء",
            why_supersession_is_licensed_here="شيء",
            what_would_have_made_it_illegitimate="شيء",
        )


def test_the_signature_carries_exactly_the_nine_declared_gates() -> None:
    symbols = {gate.symbol for gate in GATE_DECLARATIONS}

    assert symbols == {"Sh", "Sb", "Mn", r"w^\*", r"\mu", r"\Delta_q", "J", "I", "Cl"}
    assert gate_named("Mn").is_a_preventer is True


def test_an_undeclared_gate_is_refused_not_invented() -> None:
    with pytest.raises(QiyasPreregistrationError):
        gate_named("Xz")


def test_the_decision_rules_are_deposited_in_a_declared_precedence() -> None:
    orders = [rule.order for rule in DECISION_RULES]

    assert orders == list(range(1, len(DECISION_RULES) + 1))
    assert DECISION_RULES[0].outcome is QiyasOutcome.BLOCK
    assert DECISION_RULES[1].outcome is QiyasOutcome.DEFER_OR_BLOCK
    assert DECISION_RULES[-1].outcome is QiyasOutcome.INDEPENDENT_BRANCH_CANDIDATE


def test_the_qadih_gate_carries_the_three_separating_rules() -> None:
    rules = rule_for_gate(r"\Delta_q")

    assert tuple(rule.outcome for rule in rules) == (
        QiyasOutcome.CONTINUITY_UNDER_ORIGIN,
        QiyasOutcome.FORMAL_DIFFERENCE_ONLY,
        QiyasOutcome.INDEPENDENT_BRANCH_CANDIDATE,
    )


def test_the_great_chain_puts_closure_immediately_before_the_higher_center() -> None:
    assert GREAT_CHAIN[0] == "Origin"
    assert GREAT_CHAIN[-2:] == ("Closure", "Higher Center")
    assert len(GREAT_CHAIN) == 11


def test_the_origin_is_declared_before_any_branch_is_seen() -> None:
    assert ORIGIN_DECLARATION.origin_id == "CV-open-center"
    assert ORIGIN_DECLARATION.what_would_make_this_origin_illegitimate.strip()


def test_the_reconstruction_target_is_outside_both_models() -> None:
    assert RECONSTRUCTION_TARGET.target_id == "syllable-template-sequence"
    assert "دائرةً" in RECONSTRUCTION_TARGET.why_it_is_not_the_licensed_model_output
    assert "التساوي" in RECONSTRUCTION_TARGET.tie_rule


def test_the_preregistration_digest_is_derived_from_its_whole_structure() -> None:
    assert flt1_qiyas_preregistration_digest() == (flt1_qiyas_preregistration_digest())
    assert len(flt1_qiyas_preregistration_digest()) == 64


def test_the_qiyas_registration_reuses_the_frozen_surfaces_and_weaker_models() -> None:
    assert len(FLT1_FROZEN_SURFACES) == 7
    assert {item.model_id for item in WEAKER_REPRESENTATIONS} == {
        "carrier-alone",
        "state-alone",
        "unordered-carrier-state-pair",
    }


_DEPOSIT_COMMIT_SHA = "146cbac8e39ed2c67977321a3dbf21b3e90374e1"


def test_the_deposit_precedes_the_readout_in_the_repository_history() -> None:
    """شاهدُ ترتيبٍ من التاريخ نفسِه: التجميدُ التزامٌ سابقٌ لوحدة القراءة.

    وكان هذا الشاهدُ عند الإيداع نفيًا لوجود وحدة القراءة أصلًا. ولمّا
    شُغِّلت القراءةُ في التزامٍ تالٍ لم يُحذَف الشاهدُ بل أُعيدت صياغتُه على
    ما يُثبِته التاريخ: أنّ التزامَ التجميد يحوي ملفَّ القانون ولا يحوي وحدةَ
    القراءة. وحذفُه كان سيُضيِّع الدعوى، وإبقاؤه على صيغته كان سيُكذِّبها.

    والالتزامُ مُثبَّتٌ ببصمته لا مُستنبَطٌ من `git log`؛ لأنّ الاستنباط
    يتعذّر في نسخةٍ ضحلةٍ أو بعد دمجٍ يطوي التاريخ، فيُخرِج التزامًا آخرَ
    ويُكذِّب الدعوى بلا موجب. وإن لم تُحَلّ البصمةُ في النسخة قيل ذلك باسمه
    ولم يُدَّعَ الترتيبُ من لا شيء.
    """

    import subprocess

    root = pathlib.Path(__file__).resolve().parents[2]

    def resolves(revision: str) -> bool:
        return (
            subprocess.run(
                ["git", "cat-file", "-e", revision],
                cwd=root,
                capture_output=True,
            ).returncode
            == 0
        )

    if not resolves(f"{_DEPOSIT_COMMIT_SHA}^{{commit}}"):
        pytest.skip("THE_DEPOSIT_COMMIT_DOES_NOT_RESOLVE_IN_THIS_CHECKOUT")

    assert resolves(f"{_DEPOSIT_COMMIT_SHA}:src/alghanem/arabic/flt1_qiyas_law.py")
    assert resolves(
        f"{_DEPOSIT_COMMIT_SHA}:src/alghanem/arabic/flt1_qiyas_preregistration.py"
    )
    assert not resolves(
        f"{_DEPOSIT_COMMIT_SHA}:src/alghanem/arabic/flt1_qiyas_readout.py"
    )
