"""النظم: الجداولُ المنقولة من تعقّل مغلقةٌ بأسمائها، وتوافقُ الإعراب بتٌّ على الخانة الأخيرة."""

from __future__ import annotations

import pytest

from slge.nazm import PATTERNS, RELATIONS, SOURCE, case_agree, roles


def test_six_patterns_three_relations_as_in_taaqol() -> None:
    assert set(PATTERNS) == {
        "الجملة الاسمية", "الجملة الفعلية", "الإضافة", "الصفة والموصوف", "العطف", "البدل",
    }
    assert {"إسنادية", "تضمنية", "تقييدية"} == RELATIONS
    assert SOURCE.startswith("sonaiso/taaqol-gpt@91dad10")


def test_every_pattern_has_slots_boundary_and_exclusion() -> None:
    for p in PATTERNS.values():
        assert len(p.slots) >= 2 and p.boundary and p.exclusion, p.name
        assert roles(p.name) == p.slots


def test_case_agreement_is_last_cell_state() -> None:
    zaydun = (("ز", "فتح"), ("ي", "سكون"), ("د", "ضم"))
    qaimun = (("ق", "فتح"), ("ا", "سكون"), ("ء", "كسر"), ("م", "ضم"))
    zaydan = (("ز", "فتح"), ("ي", "سكون"), ("د", "فتح"))
    assert case_agree(zaydun, qaimun)
    assert not case_agree(zaydan, qaimun)
    with pytest.raises(ValueError):
        case_agree((), zaydun)
