"""طبقة الدلالة."""

from __future__ import annotations

from slge.knowledge import MAFHUM_ROUTE
from slge.semantics import (
    CONVENTIONS,
    DALALAT,
    MAFHUM,
    MANTUQ,
    dalala,
    haqiqa,
    mafhum_of,
    majaz,
    mantuq_or_mafhum,
)


def test_partitions_are_closed() -> None:
    assert all(dalala(m) for m in DALALAT) and not dalala("مخالفة")
    assert all(mantuq_or_mafhum(m) == "منطوق" for m in MANTUQ)
    assert all(mantuq_or_mafhum(m) == "مفهوم" for m in MAFHUM)
    assert mantuq_or_mafhum("إيماء") is None
    assert not MANTUQ & MAFHUM


def test_haqiqa_and_majaz() -> None:
    assert haqiqa("قائم", CONVENTIONS["قائم"]) and not haqiqa("قائم", "عالٍ")
    assert majaz("عِلْم", "غزير", "اصطلاح") and not majaz("عِلْم", "غزير", None)
    assert mafhum_of("عِلْم", True) and mafhum_of("عِلْم", False) is None


def test_mafhum_routes_are_named() -> None:
    assert set(MAFHUM_ROUTE) <= MAFHUM
