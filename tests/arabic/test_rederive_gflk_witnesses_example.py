"""شاهدٌ يُشغِّل `examples/arabic/rederive_gflk_witnesses.py` لا يذكره فحسب.

السكربتُ يُعيد اشتقاقَ الشواهد من البايتات ويخرج بغير صفرٍ عند أيّ انحراف؛
وهذا الشاهدُ يُحمِّله من مساره ويُشغِّل سجلّاته الثلاثة، ويفحص أنّ الفصلَ
بينها قائمٌ: المُعادُ اشتقاقُه غيرُ الفحص المرجعيِّ لنفسه، وكلاهما غيرُ
المحجوب لغياب بايتاته.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

EXAMPLE_RELATIVE_PATH = "examples/arabic/rederive_gflk_witnesses.py"


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def example() -> ModuleType:
    """حمِّل السكربتَ بمساره: `examples/` ليست حزمةً تُستورَد باسمها."""

    path = repository_root() / EXAMPLE_RELATIVE_PATH
    spec = importlib.util.spec_from_file_location("rederive_gflk_witnesses", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_script_runs_and_every_witness_rederives(
    example: ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    """التشغيلُ نفسُه هو الفحص؛ وأيُّ انحرافٍ يخرج بغير صفر."""

    assert example.main() == 0
    captured = capsys.readouterr()
    assert "DRIFT" not in captured.out
    assert captured.err == ""


def test_every_rederived_witness_matches_its_declared_value(
    example: ModuleType,
) -> None:
    """كلُّ رقمٍ يُشتَقّ عند النداء، ولا يُقارَن رقمٌ بنسخةٍ من نفسه مكتوبة."""

    assert len(example.REDERIVED) == 9
    for witness in example.REDERIVED:
        assert witness.derive() == witness.expected
        assert witness.counting_rule.strip()


def test_a_rule_free_figure_has_no_place_in_the_rederived_register(
    example: ModuleType,
) -> None:
    """رقمٌ بلا قاعدةِ عدٍّ لا يُعَدّ مُعادَ الاشتقاق ولو طابقت قيمتُه."""

    for witness in example.REDERIVED + example.SELF_REFERENTIAL:
        assert witness.counting_rule.strip(), witness.name


def test_the_two_line_counting_rules_are_both_carried(example: ModuleType) -> None:
    """٣٦٬٥٩٧ و«لا فاصلَ أخيرًا» يسيران معًا: العددُ بلا علّةِ فرقه ناقص."""

    by_name = {witness.name: witness for witness in example.REDERIVED}
    assert by_name["Maqāyīs root table — file lines"].derive() == 36_597
    assert by_name["Maqāyīs root table — no final line separator"].derive() is False


def test_the_freeze_check_is_kept_out_of_the_witness_register(
    example: ModuleType,
) -> None:
    """بصمةُ جدولٍ مضمَّنٍ في المصدر تُثبت الثباتَ لا صدقًا عن العربية."""

    names = {witness.name for witness in example.SELF_REFERENTIAL}
    assert "Classical makhārij table — frozen digest" in names
    assert names.isdisjoint({witness.name for witness in example.REDERIVED})
    for witness in example.SELF_REFERENTIAL:
        assert "immutability" in witness.counting_rule or "embedded" in (
            witness.counting_rule
        )


def test_an_absent_source_is_asserted_absent_never_assumed(
    example: ModuleType,
) -> None:
    """الغيابُ يُفحَص: لو وصلت البايتاتُ لَسقط السجلُّ ولَخرج السكربتُ بخطأ."""

    root = repository_root()
    for source_name, what_it_would_carry in example.NOT_IN_THIS_TREE:
        assert what_it_would_carry.strip()
        assert list(root.rglob(source_name)) == []
