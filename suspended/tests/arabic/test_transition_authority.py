"""اختباراتُ جمعِ قيدِ سلطةِ الحامل: قيدٌ مُشتَقٌّ مفحوصٌ لا سلطةٌ جديدة."""

from __future__ import annotations

import pkgutil
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    A_DERIVED_CROSS_MODULE_LAW_IS_NOT_AN_ATTESTED_SOURCE_LAW_NOTE,
    A_SIGN_IS_NOT_ITS_REFERENT_AND_NEITHER_IS_IT_UNRELATED_TO_IT_NOTE,
    A_ZERO_SHOWS_AN_UNBUILT_BRIDGE_NOT_AN_IMPOSSIBLE_ONE_NOTE,
    CARRIER_AUTHORITY_SUPPORTS,
    FORMAL_ENCODING_IS_NOT_CONCEPTUAL_MEANING_NOTE,
    NO_DERIVATION_BEYOND_THE_AUTHORITY_OF_ITS_CARRIER_NOTE,
    SUPPORT_IS_A_CHECKED_INVARIANT_NOT_AN_IMPORT_NOTE,
    THE_FOUR_LAYER_SERIES_IS_AN_ALGHANEM_COMPOSITION_NOTE,
    TRANSITION_AUTHORITY_IS_NOT_A_GATE_NOTE,
    TRANSITION_AUTHORITY_NAMED_RESIDUALS,
    CarrierAuthoritySupport,
    TransitionAuthorityError,
    supported_positions,
    unsupported_positions,
)

_MODULE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "transition_authority.py"
)


def test_every_named_residual_opens_with_its_own_law_name() -> None:
    for name, text in TRANSITION_AUTHORITY_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}:")


def test_the_four_laws_the_user_asked_for_are_deposited() -> None:
    for note in (
        NO_DERIVATION_BEYOND_THE_AUTHORITY_OF_ITS_CARRIER_NOTE,
        A_ZERO_SHOWS_AN_UNBUILT_BRIDGE_NOT_AN_IMPOSSIBLE_ONE_NOTE,
        A_SIGN_IS_NOT_ITS_REFERENT_AND_NEITHER_IS_IT_UNRELATED_TO_IT_NOTE,
        FORMAL_ENCODING_IS_NOT_CONCEPTUAL_MEANING_NOTE,
    ):
        assert note in TRANSITION_AUTHORITY_NAMED_RESIDUALS.values()


def test_the_gathered_law_is_not_attributed_to_a_source() -> None:
    note = A_DERIVED_CROSS_MODULE_LAW_IS_NOT_AN_ATTESTED_SOURCE_LAW_NOTE
    assert "تركيبُ هذا" in note
    assert "لا نصٌّ منقولٌ" in note
    assert "CONSTITUTION" in note


def test_the_four_layer_series_is_not_called_a_nabhani_theory() -> None:
    note = THE_FOUR_LAYER_SERIES_IS_AN_ALGHANEM_COMPOSITION_NOTE
    assert "تركيبٌ مقترحٌ في مشروع الغانم" in note
    assert "لم تُقابَل بعدُ بمصدرٍ مطبوع" in note
    source = _MODULE.read_text(encoding="utf-8")
    for forbidden in (
        "نظرية النبهاني في الطبقات الأربع",
        "نظريةُ النبهاني في الطبقات الأربع",
    ):
        assert forbidden not in source


def test_the_sign_law_denies_the_jump_and_not_the_relation() -> None:
    note = A_SIGN_IS_NOT_ITS_REFERENT_AND_NEITHER_IS_IT_UNRELATED_TO_IT_NOTE
    assert "لا الصلةَ" in note or "لا الصلة" in note
    assert "الانتقالُ المباشر" in note


def test_the_encoding_law_does_not_say_language_is_not_meaning() -> None:
    note = FORMAL_ENCODING_IS_NOT_CONCEPTUAL_MEANING_NOTE
    assert "ليس أنّ اللغةَ ليست معنًى" in note


def test_a_zero_is_read_as_an_unbuilt_bridge_only() -> None:
    note = A_ZERO_SHOWS_AN_UNBUILT_BRIDGE_NOT_AN_IMPOSSIBLE_ONE_NOTE
    assert "لا يُثبِت امتناعَ بنائه" in note
    assert "CompleteInductionIsCorpusBounded" in note


def test_every_support_position_is_actually_checked_now() -> None:
    assert CARRIER_AUTHORITY_SUPPORTS
    assert supported_positions() == CARRIER_AUTHORITY_SUPPORTS
    assert unsupported_positions() == ()


def test_a_failing_guard_drops_its_position_from_the_support() -> None:
    """الدعمُ يسقط بسقوط الحارس؛ ولا يبقى بمجرّد بقاء الوحدة في الشجرة."""

    pretender = CarrierAuthoritySupport(
        law_name="NoDerivationBeyondTheAuthorityOfItsCarrier",
        module_name="alghanem.arabic.epistemic_layers",
        invariant_name="فحصٌ لا يجتاز",
        invariant_text="نصُّ قيدٍ مكتوبٌ بلا حارسٍ يُنفِّذه.",
        what_the_guard_refuses="لا شيء؛ هذا موضعُ دعوى لا موضعُ تحقُّق.",
        check=lambda: False,
    )
    assert pretender.holds() is False
    assert pretender not in supported_positions()


def test_a_support_position_needs_a_deposited_law_name() -> None:
    with pytest.raises(TransitionAuthorityError):
        CarrierAuthoritySupport(
            law_name="ALawNeverDeposited",
            module_name="alghanem.arabic.wad_naql",
            invariant_name="اسم",
            invariant_text="نص",
            what_the_guard_refuses="شيء",
            check=lambda: True,
        )


def test_a_support_position_needs_a_check_not_an_import() -> None:
    with pytest.raises(TransitionAuthorityError):
        CarrierAuthoritySupport(
            law_name="NoDerivationBeyondTheAuthorityOfItsCarrier",
            module_name="alghanem.arabic.wad_naql",
            invariant_name="اسم",
            invariant_text="نص",
            what_the_guard_refuses="شيء",
            check="alghanem.arabic.wad_naql",  # type: ignore[arg-type]
        )


def test_each_support_carries_the_invariant_text_of_its_own_module() -> None:
    for support in CARRIER_AUTHORITY_SUPPORTS:
        assert support.module_name.startswith("alghanem.arabic.")
        assert support.invariant_text.strip()
        assert support.what_the_guard_refuses.strip()


def test_the_gathered_law_has_at_least_one_checked_position() -> None:
    laws = {support.law_name for support in supported_positions()}
    assert "NoDerivationBeyondTheAuthorityOfItsCarrier" in laws


def test_no_four_authority_vocabulary_was_created() -> None:
    """لا مفردةَ سلطاتٍ رباعية ولا سُلَّمَ انتقالٍ مغلق."""

    source = _MODULE.read_text(encoding="utf-8")
    assert "class TransitionAuthority(Enum)" not in source
    assert "TransitionAuthority(Enum)" not in source
    for forbidden in ("تصوّر_وتصديق", "TasawwurTasdiq", "FourLayer(Enum)"):
        assert forbidden not in source


def test_this_module_is_not_a_gate() -> None:
    assert "ولا ترخّصه" in TRANSITION_AUTHORITY_IS_NOT_A_GATE_NOTE
    source = _MODULE.read_text(encoding="utf-8")
    for forbidden in ("Verdict", "verdict", "birth", "Birth"):
        assert forbidden not in source


def test_support_is_not_an_import_claim() -> None:
    note = SUPPORT_IS_A_CHECKED_INVARIANT_NOT_AN_IMPORT_NOTE
    assert "ولا يُثبِت أنّ المبدأ تحقَّق فيها" in note


def test_the_module_reads_no_kernel_authority() -> None:
    imports = [
        line
        for line in _MODULE.read_text(encoding="utf-8").splitlines()
        if line.startswith(("import ", "from "))
    ]
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_gathering() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        path = Path(str(module.module_finder.path)) / f"{module.name.split('.')[-1]}.py"
        if not path.exists():
            continue
        assert "transition_authority" not in path.read_text(encoding="utf-8")
