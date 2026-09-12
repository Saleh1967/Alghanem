"""Tests for the qiyas and rabt registrations."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    FROZEN_ASL_REFERENCES,
    ForeignDeclaredCase,
    IllaApplication,
    LinkStanding,
    QiyasRabtRegistrationError,
    QiyasRegistration,
    QiyasStanding,
    RabtRegistration,
    frozen_asl_references,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def qiyas(**overrides: object) -> QiyasRegistration:
    base: dict[str, object] = {
        "asl_reference": "FrozenFormalDomain",
        "far_reference": "far-1",
        "illa": "علة",
        "hukm": "حكم",
        "illa_application": IllaApplication.منطبقة_فعلاً,
    }
    base.update(overrides)
    return QiyasRegistration(**base)  # type: ignore[arg-type]


def test_the_frozen_origins_are_derived_by_import_not_written() -> None:
    assert frozen_asl_references() == FROZEN_ASL_REFERENCES
    assert set(FROZEN_ASL_REFERENCES) == {
        "FrozenFormalDomain",
        "FrozenKulliJuziDomain",
        "FrozenMadlulDomain",
        "FrozenRelationDomain",
    }


@pytest.mark.parametrize("asl", FROZEN_ASL_REFERENCES)
def test_every_frozen_domain_in_the_repository_is_an_admissible_origin(
    asl: str,
) -> None:
    assert qiyas(asl_reference=asl).asl_reference == asl


def test_a_free_text_origin_is_refused() -> None:
    with pytest.raises(QiyasRabtRegistrationError, match="لا اسمٌ حرّ"):
        qiyas(asl_reference="SUN-MOON-LETTERS-AR-1")


def test_a_branch_identical_to_its_origin_is_not_an_analogy() -> None:
    with pytest.raises(QiyasRabtRegistrationError, match="إعادةَ نصّ"):
        qiyas(far_reference="FrozenFormalDomain")


def test_an_actually_applying_illa_yields_a_sound_analogy() -> None:
    assert qiyas().standing is QiyasStanding.صحيح_من_أصله
    assert qiyas().is_invalid_from_origin is False


@pytest.mark.parametrize(
    "application",
    (IllaApplication.تشابه_فئوي_فقط, IllaApplication.لا_علة_في_النص),
)
def test_categorial_resemblance_or_a_missing_illa_is_invalid_from_origin(
    application: IllaApplication,
) -> None:
    registered = qiyas(illa_application=application)
    assert registered.standing is QiyasStanding.باطل_من_أصله
    assert registered.is_invalid_from_origin is True


def test_there_is_no_weak_degree_between_the_two_analogy_standings() -> None:
    assert len(QiyasStanding) == 2
    assert not any("ضعيف" in standing.value for standing in QiyasStanding)
    declared = {item.name for item in fields(QiyasRegistration)}
    assert not any("weak" in name or "ضعيف" in name for name in declared)


def test_an_illa_application_outside_its_vocabulary_is_refused() -> None:
    with pytest.raises(QiyasRabtRegistrationError, match="مفردته المغلقة"):
        qiyas(illa_application="منطبقة")


def rabt(**overrides: object) -> RabtRegistration:
    base: dict[str, object] = {
        "link_id": "link-1",
        "imported_from": "مصدر خارجي",
        "certificate_reference": "FrozenFormalDomain",
        "held_out_cases": (),
        "declared_standing": LinkStanding.استرجاع,
    }
    base.update(overrides)
    return RabtRegistration(**base)  # type: ignore[arg-type]


def test_an_imported_link_without_a_test_is_retrieval_only() -> None:
    assert rabt().standing is LinkStanding.استرجاع
    assert rabt(held_out_cases=("case-1",)).standing is LinkStanding.استرجاع


def test_linking_without_a_held_out_sample_is_refused_by_its_own_message() -> None:
    with pytest.raises(QiyasRabtRegistrationError, match="باسمٍ أعلى منه"):
        rabt(declared_standing=LinkStanding.ربط)


def test_linking_is_declared_and_unconstructible_even_with_a_held_out_sample() -> None:
    with pytest.raises(QiyasRabtRegistrationError, match="ادّعاءُ تعميمٍ لم يجرِ"):
        rabt(
            held_out_cases=("case-1", "case-2"),
            declared_standing=LinkStanding.ربط,
        )


def test_a_repeated_held_out_case_is_not_a_second_case() -> None:
    with pytest.raises(QiyasRabtRegistrationError, match="ليست واقعةً ثانية"):
        rabt(held_out_cases=("case-1", "case-1"))


def test_the_documents_own_examples_are_foreign_declared_cases_only() -> None:
    foreign = ForeignDeclaredCase(
        case_id="SUN-MOON-LETTERS-AR-1",
        declared_in="وثيقة G0.N",
        why_not_verifiable_here="لا وحدةَ ولا شهادةَ لها في هذا المستودع",
    )
    assert foreign.verified_here is False
    with pytest.raises(QiyasRabtRegistrationError):
        qiyas(asl_reference=foreign.case_id)


def test_no_type_here_carries_a_count_or_verdict_field() -> None:
    for declaring_type in (QiyasRegistration, RabtRegistration, ForeignDeclaredCase):
        declared = {item.name for item in fields(declaring_type)}
        for marker in ("count", "number", "total", "verdict", "birth"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "qiyas_rabt_registration.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_registration() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("qiyas_rabt", "QiyasRegistration", "RabtRegistration"):
            assert name not in text, (module.name, name)


@pytest.mark.parametrize("card", _CARDS)
def test_these_registrations_change_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    qiyas()
    rabt()
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
