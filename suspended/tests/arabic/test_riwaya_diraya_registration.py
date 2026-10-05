"""Tests for the two separate acceptance gates: riwaya and diraya."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    DirayaBranch,
    DirayaReading,
    DirayaStanding,
    IndependentApplication,
    Remedy,
    RiwayaDirayaRegistrationError,
    RiwayaReading,
    RiwayaStanding,
    derive_remedy,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def riwaya(**overrides: object) -> RiwayaReading:
    base: dict[str, object] = {
        "tool_identity": "isti-la-probe",
        "tool_digest": "sha256:" + "0" * 64,
        "change_log_reference": "v1..v5",
        "reproduced_independently": True,
        "declared_standing": RiwayaStanding.قناة_سليمة,
    }
    base.update(overrides)
    return RiwayaReading(**base)  # type: ignore[arg-type]


def application(
    application_id: str = "app-1",
    standing: DirayaStanding = DirayaStanding.لم_يُهزَم_بعد,
) -> IndependentApplication:
    return IndependentApplication(
        application_id=application_id,
        independent_scope="كوربص مستقل",
        standing=standing,
    )


def test_the_two_gates_are_separate_types_not_two_fields_of_one() -> None:
    riwaya_fields = {item.name for item in fields(RiwayaReading)}
    diraya_fields = {item.name for item in fields(DirayaReading)}
    assert riwaya_fields.isdisjoint(diraya_fields)
    assert "branch" not in riwaya_fields
    assert "tool_digest" not in diraya_fields


def test_the_channel_standing_is_derived_from_independent_reproduction() -> None:
    assert riwaya().standing is RiwayaStanding.قناة_سليمة
    broken = riwaya(
        reproduced_independently=False,
        declared_standing=RiwayaStanding.قناة_معطوبة,
    )
    assert broken.standing is RiwayaStanding.قناة_معطوبة


def test_a_written_channel_standing_contradicting_its_carrier_is_refused() -> None:
    with pytest.raises(RiwayaDirayaRegistrationError, match="تُشتَقّ ولا تُكتَب"):
        riwaya(reproduced_independently=False)


def test_a_riwaya_failure_is_remedied_by_repairing_the_tool_only() -> None:
    broken = riwaya(
        reproduced_independently=False,
        declared_standing=RiwayaStanding.قناة_معطوبة,
    )
    assert broken.remedy is Remedy.إصلاح_الأداة
    assert riwaya().remedy is None


def test_the_remedy_is_derived_from_the_failure_kind_not_written() -> None:
    assert derive_remedy(DirayaBranch.أنطولوجي) is Remedy.إعادة_تعريف_الفئات
    assert derive_remedy(DirayaBranch.ابستمولوجي) is Remedy.تشديد_اختبار_الأدلة
    assert derive_remedy(RiwayaStanding.قناة_معطوبة) is Remedy.إصلاح_الأداة


def test_an_intact_channel_has_no_remedy_to_derive() -> None:
    with pytest.raises(RiwayaDirayaRegistrationError, match="لا علاجَ لقناةٍ سليمة"):
        derive_remedy(RiwayaStanding.قناة_سليمة)


def test_category_redefinition_is_never_derived_for_an_evidential_failure() -> None:
    epistemological = DirayaReading(
        matn_reference="idgham-bighunnah",
        branch=DirayaBranch.ابستمولوجي,
        stronger_frozen_reference="permutation-test-frozen",
        applications=(application(standing=DirayaStanding.مهزوم),),
    )
    assert epistemological.remedy is Remedy.تشديد_اختبار_الأدلة
    assert epistemological.remedy is not Remedy.إعادة_تعريف_الفئات

    ontological = DirayaReading(
        matn_reference="prefixes-subset-ziyada",
        branch=DirayaBranch.أنطولوجي,
        stronger_frozen_reference=None,
        applications=(application(standing=DirayaStanding.مهزوم),),
    )
    assert ontological.remedy is Remedy.إعادة_تعريف_الفئات
    assert ontological.remedy is not Remedy.تشديد_اختبار_الأدلة


def test_an_epistemological_reading_must_name_the_stronger_frozen_matn() -> None:
    with pytest.raises(RiwayaDirayaRegistrationError, match="أقوى مُجمَّدًا"):
        DirayaReading(
            matn_reference="idgham-bighunnah",
            branch=DirayaBranch.ابستمولوجي,
            stronger_frozen_reference=None,
            applications=(application(),),
        )


def test_an_ontological_reading_precedes_evidence_so_names_no_stronger_matn() -> None:
    with pytest.raises(RiwayaDirayaRegistrationError, match="سابقةٌ على أيّ دليل"):
        DirayaReading(
            matn_reference="prefixes-subset-ziyada",
            branch=DirayaBranch.أنطولوجي,
            stronger_frozen_reference="permutation-test-frozen",
            applications=(application(),),
        )


def test_scrutiny_is_continuing_so_a_reading_needs_at_least_one_application() -> None:
    with pytest.raises(RiwayaDirayaRegistrationError, match="عمليةٌ مستمرة"):
        DirayaReading(
            matn_reference="matn",
            branch=DirayaBranch.أنطولوجي,
            stronger_frozen_reference=None,
            applications=(),
        )


def test_a_repeated_application_identifier_is_not_a_second_application() -> None:
    with pytest.raises(RiwayaDirayaRegistrationError, match="ليس تطبيقًا ثانيًا"):
        DirayaReading(
            matn_reference="matn",
            branch=DirayaBranch.أنطولوجي,
            stronger_frozen_reference=None,
            applications=(application("app-1"), application("app-1")),
        )


def test_repeated_survival_reads_as_not_yet_defeated_never_as_established() -> None:
    survived = DirayaReading(
        matn_reference="matn",
        branch=DirayaBranch.أنطولوجي,
        stronger_frozen_reference=None,
        applications=(
            application("app-1"),
            application("app-2"),
            application("app-3"),
        ),
    )
    assert survived.defeated is False
    assert survived.remedy is None
    assert "لم يُهزَم بعد" in survived.reading
    assert "ثابت" not in survived.reading


def test_one_defeat_among_many_survivals_still_reads_as_defeated() -> None:
    mixed = DirayaReading(
        matn_reference="matn",
        branch=DirayaBranch.أنطولوجي,
        stronger_frozen_reference=None,
        applications=(
            application("app-1"),
            application("app-2", DirayaStanding.مهزوم),
        ),
    )
    assert mixed.defeated is True


def test_no_type_here_carries_a_count_or_passed_or_verdict_field() -> None:
    for declaring_type in (RiwayaReading, DirayaReading, IndependentApplication):
        declared = {item.name for item in fields(declaring_type)}
        for marker in ("count", "number", "total", "verdict", "birth", "passed"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "riwaya_diraya_registration.py"
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
        for name in ("riwaya_diraya", "RiwayaReading", "DirayaReading", "Remedy"):
            assert name not in text, (module.name, name)


@pytest.mark.parametrize("card", _CARDS)
def test_this_registration_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    riwaya()
    DirayaReading(
        matn_reference="matn",
        branch=DirayaBranch.أنطولوجي,
        stronger_frozen_reference=None,
        applications=(application(),),
    )
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
