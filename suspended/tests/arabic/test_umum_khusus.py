"""اختباراتُ الحلقة العاشرة: العمومُ والخصوص، وتخصيصُ العام بالمفهوم."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    CONFLICT_MUST_BE_NAMED_NOTE,
    GENERAL_REMAINS_AUTHORITATIVE_OUTSIDE_NOTE,
    TAFRI_PATHS_ARE_NOT_MIXED_NOTE,
    TAKHSIS_IS_NOT_IHMAL_NOTE,
    UMUM_KHUSUS_IS_NOT_A_GATE_NOTE,
    DalalaChannel,
    DalilRegistration,
    DalilScope,
    RuleGenus,
    TafriPath,
    TafriRegistration,
    TakhsisChannel,
    TakhsisRegistration,
    UmumKhususError,
    derive_takhsis_channel,
    tafri_path_of,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = ("man_2_255.yaml", "quru_2_228.yaml", "anna_2_223.yaml")

_MODULE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "umum_khusus.py"
)


def general(**overrides: object) -> DalilRegistration:
    base: dict[str, object] = {
        "reference": "الدليل العام",
        "wording": "لفظٌ يشمل أفرادًا",
        "scope": DalilScope.عام,
        "channel": DalalaChannel.منطوق,
    }
    base.update(overrides)
    return DalilRegistration(**base)  # type: ignore[arg-type]


def specializer(**overrides: object) -> DalilRegistration:
    base: dict[str, object] = {
        "reference": "الدليل المُخصِّص",
        "wording": "لفظٌ يقصر الحكم على موضعٍ منه",
        "scope": DalilScope.خاص,
        "channel": DalalaChannel.مفهوم,
    }
    base.update(overrides)
    return DalilRegistration(**base)  # type: ignore[arg-type]


def takhsis(**overrides: object) -> TakhsisRegistration:
    base: dict[str, object] = {
        "general": general(),
        "specializer": specializer(),
        "conflict_locus": "موضعُ التعارض المُسمّى",
    }
    base.update(overrides)
    return TakhsisRegistration(**base)  # type: ignore[arg-type]


def test_the_general_is_specialized_by_a_mafhum_without_dropping_it() -> None:
    record = takhsis()
    assert record.channel is TakhsisChannel.تخصيص_بمفهوم
    assert record.specialized_by_mafhum is True
    assert record.retained == (record.general, record.specializer)
    assert record.general_remains_authoritative_outside_locus is True


def test_no_field_exists_into_which_a_dropped_evidence_could_be_written() -> None:
    declared = {item.name for item in fields(TakhsisRegistration)}
    assert declared == {"general", "specializer", "conflict_locus"}
    for marker in ("dropped", "ignored", "مهمل", "verdict", "rank"):
        assert not any(marker in name for name in declared), marker


def test_a_specializer_that_is_itself_general_is_refused() -> None:
    with pytest.raises(UmumKhususError, match="عامٌّ لا يُخصِّص عامًّا"):
        takhsis(specializer=specializer(scope=DalilScope.عام))


def test_a_specialized_evidence_that_is_not_general_is_refused() -> None:
    with pytest.raises(UmumKhususError, match="تخصيصُ خاصٍّ بخاصٍّ"):
        takhsis(general=general(scope=DalilScope.خاص))


def test_one_evidence_may_not_specialize_itself() -> None:
    with pytest.raises(UmumKhususError, match="يُخصِّص نفسَه"):
        takhsis(specializer=specializer(reference="الدليل العام"))


def test_a_takhsis_without_a_named_conflict_locus_is_refused() -> None:
    with pytest.raises(UmumKhususError, match="موضعُ التعارض"):
        takhsis(conflict_locus="   ")
    assert "دعوًى تحتاج إثباتًا" in CONFLICT_MUST_BE_NAMED_NOTE


def test_the_channel_is_derived_from_the_specializer_not_written() -> None:
    assert takhsis().channel is TakhsisChannel.تخصيص_بمفهوم
    by_mantuq = takhsis(specializer=specializer(channel=DalalaChannel.منطوق))
    assert by_mantuq.channel is TakhsisChannel.تخصيص_بمنطوق
    assert by_mantuq.specialized_by_mafhum is False


def test_no_takhsis_is_ever_derived_from_a_standing_specializer() -> None:
    assert len(TakhsisChannel) == 3
    derived = {derive_takhsis_channel(channel) for channel in DalalaChannel}
    assert TakhsisChannel.لا_تخصيص not in derived
    assert derived == {TakhsisChannel.تخصيص_بمنطوق, TakhsisChannel.تخصيص_بمفهوم}


def test_a_foreign_channel_value_is_refused_rather_than_coerced() -> None:
    with pytest.raises(UmumKhususError, match="مستورَدةً لا منسوخة"):
        derive_takhsis_channel("مفهوم")  # type: ignore[arg-type]
    with pytest.raises(UmumKhususError, match="مستورَدةً لا منسوخة"):
        general(channel="منطوق")


def test_the_scope_comes_from_its_closed_two_member_vocabulary() -> None:
    assert len(DalilScope) == 2
    with pytest.raises(UmumKhususError, match="مفردتها المغلقة الثنائية"):
        general(scope="عام")


def test_the_two_tafri_paths_are_derived_from_the_rule_genus() -> None:
    assert len(RuleGenus) == 2
    assert len(TafriPath) == 2
    assert tafri_path_of(RuleGenus.قاعدة_عامة) is TafriPath.قاعدة_عامة_على_أفراد
    assert tafri_path_of(RuleGenus.قاعدة_كلية) is TafriPath.قاعدة_كلية_على_جزئيات


def test_a_rule_branched_along_the_other_path_is_refused_not_reinterpreted() -> None:
    with pytest.raises(UmumKhususError, match="يخالف المُشتَقّ"):
        TafriRegistration(
            rule_reference="قاعدةٌ عامّة",
            rule_genus=RuleGenus.قاعدة_عامة,
            branched_onto=("جزئيٌّ من معناها",),
            declared_path=TafriPath.قاعدة_كلية_على_جزئيات,
        )
    assert "متغايران لا مترادفان" in TAFRI_PATHS_ARE_NOT_MIXED_NOTE


def test_a_tafri_onto_nothing_or_onto_a_repeated_item_is_refused() -> None:
    with pytest.raises(UmumKhususError, match="تفريعٌ على لا شيء"):
        TafriRegistration(
            rule_reference="قاعدةٌ كلّية",
            rule_genus=RuleGenus.قاعدة_كلية,
            branched_onto=(),
            declared_path=TafriPath.قاعدة_كلية_على_جزئيات,
        )
    with pytest.raises(UmumKhususError, match="ليس عنصرًا ثانيًا"):
        TafriRegistration(
            rule_reference="قاعدةٌ كلّية",
            rule_genus=RuleGenus.قاعدة_كلية,
            branched_onto=("جزئيّ", "جزئيّ"),
            declared_path=TafriPath.قاعدة_كلية_على_جزئيات,
        )


def test_a_rule_genus_is_not_the_single_word_classification() -> None:
    from alghanem.arabic import Universality

    with pytest.raises(UmumKhususError, match="لا من تصنيف اللفظ المفرد"):
        tafri_path_of(Universality.KULLI)  # type: ignore[arg-type]


def test_the_module_declares_its_own_limits_by_name() -> None:
    assert "إعمالُ الدليلين معًا" in TAKHSIS_IS_NOT_IHMAL_NOTE
    assert "حالٌ مُشتَقّةٌ" in GENERAL_REMAINS_AUTHORITATIVE_OUTSIDE_NOTE
    assert "لا سلطة" in UMUM_KHUSUS_IS_NOT_A_GATE_NOTE


def test_the_module_imports_no_kernel_authority() -> None:
    source = _MODULE.read_text(encoding="utf-8")
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
        for name in ("umum_khusus", "TakhsisRegistration", "TafriRegistration"):
            assert name not in text, (module.name, name)


@pytest.mark.parametrize("card", _CARDS)
def test_this_registration_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    takhsis()
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
