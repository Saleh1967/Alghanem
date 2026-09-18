"""`G0.CASE-0.DATA-H`: التجميدُ العميق، والفرقُ البنيويُّ بين نصّين مؤلَّفين.

    FrozenData  ≺  Readout

فهذه الطبقةُ تثبت أنّ الوثيقةَ المجمَّدةَ لا تُحوَّر من نسخةٍ تُسلَّم لقارئ، وأنّ
الفرقَ عمليّةٌ في موضعٍ بحالتيه لا مجرَّدُ اسمِ موضع؛ ولا يُشغَّل هنا محرّك.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from typing import Any

import pytest

from alghanem.execution.frozen_json import (
    DiffOperation,
    FrozenJsonError,
    freeze_json,
    frozen_equal,
    structural_diff,
    thaw_json,
)


def _frozen(value: Any) -> Any:
    return freeze_json(value, "الوثيقة")


def test_a_frozen_mapping_refuses_every_write() -> None:
    frozen = _frozen({"a": {"b": [1, 2]}})
    assert isinstance(frozen, dict) is False
    with pytest.raises(TypeError):
        frozen["a"] = 1  # type: ignore[index]
    assert isinstance(frozen["a"]["b"], tuple)


def test_a_thawed_reading_is_a_new_tree_every_time() -> None:
    frozen = _frozen({"a": {"b": [1, 2]}})
    first = thaw_json(frozen)
    first["a"]["b"].append(3)
    second = thaw_json(frozen)
    assert second["a"]["b"] == [1, 2]
    assert first is not second


def test_a_value_outside_the_json_contract_is_refused() -> None:
    with pytest.raises(FrozenJsonError):
        _frozen({"a": object()})
    with pytest.raises(FrozenJsonError):
        _frozen({1: "a"})


def test_a_boolean_is_not_read_as_a_number() -> None:
    assert not frozen_equal(True, 1)
    assert frozen_equal(True, True)
    assert not frozen_equal(None, 0)


def test_a_changed_scalar_is_one_replacement_at_its_own_place() -> None:
    differences = structural_diff(
        _frozen({"nisbah": {"predicate": {"arity": 2}}}),
        _frozen({"nisbah": {"predicate": {"arity": 3}}}),
    )
    assert len(differences) == 1
    assert differences[0].operation is DiffOperation.REPLACE
    assert differences[0].path == "nisbah.predicate.arity"
    assert (differences[0].before, differences[0].after) == (2, 3)


def test_an_appended_element_is_an_addition_at_its_index() -> None:
    differences = structural_diff(
        _frozen({"anchors": [{"id": "first"}]}),
        _frozen({"anchors": [{"id": "first"}, {"id": "second"}]}),
    )
    assert len(differences) == 1
    assert differences[0].operation is DiffOperation.ADD
    assert differences[0].path == "anchors[1]"
    assert differences[0].before is None


def test_a_dropped_element_is_a_removal_at_its_index() -> None:
    differences = structural_diff(
        _frozen({"anchors": [{"id": "first"}, {"id": "second"}]}),
        _frozen({"anchors": [{"id": "first"}]}),
    )
    assert len(differences) == 1
    assert differences[0].operation is DiffOperation.REMOVE
    assert differences[0].path == "anchors[1]"
    assert differences[0].after is None


def test_a_changed_element_beside_an_added_one_is_two_operations() -> None:
    differences = structural_diff(
        _frozen({"anchors": [{"id": "first"}]}),
        _frozen({"anchors": [{"id": "other"}, {"id": "second"}]}),
    )
    assert [item.path for item in differences] == ["anchors[0].id", "anchors[1]"]
    assert [item.operation for item in differences] == [
        DiffOperation.REPLACE,
        DiffOperation.ADD,
    ]


def test_an_added_subtree_is_one_difference_not_one_per_leaf() -> None:
    differences = structural_diff(
        _frozen({"nisbah": {}}),
        _frozen({"nisbah": {"predicate": {"arity": 2, "slots": [1, 2]}}}),
    )
    assert len(differences) == 1
    assert differences[0].path == "nisbah.predicate"
    assert differences[0].operation is DiffOperation.ADD


def test_two_equal_documents_have_no_difference_at_all() -> None:
    document = {"a": [1, {"b": None}], "c": "نصّ"}
    assert structural_diff(_frozen(document), _frozen(document)) == ()


def test_a_type_change_at_one_place_is_one_replacement() -> None:
    differences = structural_diff(_frozen({"a": [1]}), _frozen({"a": {"0": 1}}))
    assert len(differences) == 1
    assert differences[0].path == "a"
    assert differences[0].operation is DiffOperation.REPLACE
