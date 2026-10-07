"""لا مودَعَ بلا نوع (دستورُ الوكيل، المادّة ١٢): كلُّ ملفٍّ في `tests/data/` مسجَّلٌ في `manifest.DEPOSITS`
بنوعٍ من الأربعة، وكلُّ مسجَّلٍ موجود؛ ولا مودَعَ من نوع «معلومات سابقة» يُقرأ من طبقةٍ دون «الحكم»."""

from __future__ import annotations

from conftest import ROOT
from slge.manifest import DEPOSIT_KINDS, DEPOSITS, Deposit
from slge.order import MODULE_LAYER, ancestors

DATA = ROOT / "tests" / "data"


def _problems(deposits: tuple[Deposit, ...], present: set[str]) -> list[str]:
    registered = {d.path for d in deposits}
    out = [f"UNREGISTERED_DEPOSIT:{p}" for p in sorted(present - registered)]
    out += [f"MISSING_DEPOSIT:{p}" for p in sorted(registered - present)]
    out += [f"DEPOSIT_KIND_UNDECLARED:{d.path}:{d.kind}" for d in deposits
            if d.kind not in DEPOSIT_KINDS]
    return out


def test_every_deposit_has_a_kind_and_exists() -> None:
    present = {p.name for p in DATA.iterdir() if p.is_file()}
    assert _problems(DEPOSITS, present) == []
    assert len(DEPOSITS) == len({d.path for d in DEPOSITS})
    assert {d.kind for d in DEPOSITS} == DEPOSIT_KINDS - {"معلومات سابقة"}


def test_mutations_are_named() -> None:
    present = {d.path for d in DEPOSITS}
    extra = present | {"mukhassas.json.gz"}
    assert _problems(DEPOSITS, extra) == ["UNREGISTERED_DEPOSIT:mukhassas.json.gz"]
    gone = present - {"sibawayh-abniya.tsv"}
    assert _problems(DEPOSITS, gone) == ["MISSING_DEPOSIT:sibawayh-abniya.tsv"]
    bent = (*DEPOSITS, Deposit("x.json", "حقيقة"))
    assert _problems(bent, present | {"x.json"}) == ["DEPOSIT_KIND_UNDECLARED:x.json:حقيقة"]


def test_prior_knowledge_is_read_only_above_the_gates() -> None:
    """المادّة ١٠: «الحكم» فوق «البوابات»، فلا بوّابةَ تستورد منه؛ وما يقرأ مودَعًا من نوع
    «معلومات سابقة» (حين يوجد) يسكن طبقةَ الحكم أو فوقها."""
    assert "البوابات" in ancestors("الحكم")
    assert "الحكم" not in ancestors("البوابات")
    for module, layer in MODULE_LAYER.items():
        assert layer != "الحكم", f"{module}: لا وحدةَ في الحكم قبل الإذن (المادّة ٩)"
