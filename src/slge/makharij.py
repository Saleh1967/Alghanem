"""المخارجُ والصفات عند سيبويه — مرآةُ `Slge.Makharij` (الحدُّ الأدنى المكتمل).

المصدرُ «باب عدد الحروف العربية ومخارجها ومهموسها ومجهورها» من الكتاب المختوم (`makharij_table`
مولَّدٌ منه). ترتيبُ سيبويه تبديلٌ للحوامل التسعة والعشرين (`order_is_the_alphabet`)؛ المخارجُ المعدودةُ 15
والمنطوقُ 16 والساقطُ مخرجُ اللام وحدَه (`lacuna_is_lam`)؛ الجهرُ/الهمس، الشدّةُ/الرخاوةُ/البينيّة،
الإطباقُ/الانفتاح قسماتٌ تامّة مبرهَنة (`jahr_partition`، `shidda_partition`، `itbaq_partition`).
الطبقةُ «الصفات» لا تستورد الأبجديّةَ من `cells`: تُعلن حروفَها من المودَع ويفحص الاختبارُ أنّها الـ29
بعينها.
"""

from __future__ import annotations

from typing import Final

from slge.makharij_table import FURU_BAD, FURU_GOOD, MAKHARIJ, MISSING, ORDER, SIFAT, STATED_COUNT

__all__ = ["BAYN", "FURU_BAD", "FURU_GOOD", "MAKHARIJ", "MISSING", "ORDER", "SIFAT", "STATED_COUNT",
           "is_majhur", "makhraj_of", "sifat_of"]

_BAYN_KEYS: Final[tuple[str, ...]] = ("baynBayn", "munharif", "ghunna", "mukarrar", "layyina",
                                      "hawi")
BAYN: Final[tuple[str, ...]] = tuple(c for key in _BAYN_KEYS for c in SIFAT[key][1])
"""بين الشديدة والرخوة: العينُ والمنحرفُ والغنّةُ والمكرّرُ واللينتان والهاوي (`bayn`)."""


def makhraj_of(letter: str) -> tuple[int, ...]:
    """فهارسُ المخارج التي ورد فيها الحرف (النونُ في اثنين؛ اللامُ في لا شيء — نقصُ النشرة)."""

    return tuple(i for i, (_, cs, _) in enumerate(MAKHARIJ) if letter in cs)


def is_majhur(letter: str) -> bool:
    return letter in SIFAT["majhura"][1]


def sifat_of(letter: str) -> tuple[str, ...]:
    """أسماءُ الصفات التي ورد فيها الحرف بترتيب الباب."""

    return tuple(name for name, cs in SIFAT.values() if letter in cs)


def _check() -> None:
    assert len(ORDER) == 29 == len(set(ORDER)) and ORDER[0] == "ء" and ORDER[-1] == "و"
    assert len(MAKHARIJ) == 15 and STATED_COUNT == 16 and MISSING == ("ل",)
    assert makhraj_of("ن") == (7, 14) and makhraj_of("ل") == () and makhraj_of("ق") == (3,)
    maj, mah = SIFAT["majhura"][1], SIFAT["mahmusa"][1]
    assert len(maj) == 19 and len(mah) == 10 and not set(maj) & set(mah)
    assert set(maj) | set(mah) == set(ORDER)
    sh, rk = SIFAT["shadida"][1], SIFAT["rikhwa"][1]
    assert len(sh) == 8 and len(rk) == 13 and len(BAYN) == 8
    assert set(sh) | set(rk) | set(BAYN) == set(ORDER)
    assert not (set(sh) & set(rk)) and not (set(sh) & set(BAYN)) and not (set(rk) & set(BAYN))
    assert SIFAT["mutbaqa"][1] == ("ص", "ض", "ط", "ظ") and len(SIFAT["munfatiha"][1]) == 25
    assert sifat_of("ص") == ("المهموسة", "الرخوة", "المطبقة")
    assert is_majhur("ض") and not is_majhur("ص")
    assert len(FURU_GOOD) == 6 and len(FURU_BAD) == 8


_check()
