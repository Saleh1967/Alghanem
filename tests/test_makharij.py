"""المخارجُ والصفات: توقّعاتٌ مستقلّةٌ عن الشيفرة (ترتيبُ سيبويه تبديلٌ للأبجديّة؛ القسماتُ تامّة؛ الساقطُ
اللامُ باسمه؛ والفروعُ ستّةٌ وثمانية)، وطفراتٌ مرفوضة."""

from __future__ import annotations

from slge.makharij import (
    BAYN,
    FURU_BAD,
    FURU_GOOD,
    MAKHARIJ,
    MISSING,
    ORDER,
    SIFAT,
    is_majhur,
    makhraj_of,
)
from slge.phonology import LETTERS, MAHRAJ, PAIRS


def test_order_is_a_permutation_of_the_alphabet() -> None:
    assert sorted(ORDER) == sorted(LETTERS) and ORDER != LETTERS
    # من أقصى الحلق إلى الشفتين
    assert ORDER[:3] == ("ء", "ا", "ه") and ORDER[-3:] == ("ب", "م", "و")


def test_fifteen_counted_sixteen_stated_lam_missing() -> None:
    assert len(MAKHARIJ) == 15 and MISSING == ("ل",)
    assert makhraj_of("ل") == () and makhraj_of("ن") == (7, 14)
    assert MAKHARIJ[14][2] is True  # الخفيفة في الخياشيم
    assert MAKHARIJ[0][1] == ("ء", "ه", "ا") and MAKHARIJ[-2][1] == ("ب", "م", "و")
    covered = {c for _, cs, _ in MAKHARIJ for c in cs}
    assert covered == set(ORDER) - {"ل"}


def test_partitions_are_exact() -> None:
    maj, mah = set(SIFAT["majhura"][1]), set(SIFAT["mahmusa"][1])
    assert len(maj) == 19 and len(mah) == 10 and maj | mah == set(ORDER) and not maj & mah
    sh, rk, bn = set(SIFAT["shadida"][1]), set(SIFAT["rikhwa"][1]), set(BAYN)
    assert (len(sh), len(rk), len(bn)) == (8, 13, 8) and sh | rk | bn == set(ORDER)
    assert not sh & rk and not sh & bn and not rk & bn
    assert set(SIFAT["mutbaqa"][1]) == {"ص", "ض", "ط", "ظ"}
    assert set(SIFAT["munfatiha"][1]) == set(ORDER) - {"ص", "ض", "ط", "ظ"}


def test_sibawayh_hams_differs_from_the_declared_phonology_by_sad() -> None:
    """المهموسةُ عند سيبويه عشرة وفيها الصاد؛ `phonology.PAIRS` المعلَنة تعدّ تسعة بلا الصاد — فرقٌ مقيس
    لا يُصحَّح من الذاكرة بل من المختوم (ADR ١٩)."""

    declared = next(pos for name, _, pos, _ in PAIRS if name == "همس")
    assert set(SIFAT["mahmusa"][1]) - set(declared) == {"ص"}
    assert set(declared) <= set(SIFAT["mahmusa"][1])
    assert is_majhur("ض") and not is_majhur("ص")


def test_declared_places_agree_with_sibawayh_on_the_throat() -> None:
    throat = {c for m in MAKHARIJ[:3] for c in m[1]}
    assert throat == {"ء", "ه", "ا", "ع", "ح", "غ", "خ"}
    assert all(MAHRAJ[c][0] == "الحلق" for c in throat - {"ا"})  # الألفُ عند المعلَن في الجوف


def test_furu_and_mutants() -> None:
    assert len(FURU_GOOD) == 6 and FURU_GOOD[0] == "النون الخفيفة" and len(FURU_BAD) == 8
    assert all(x.startswith(("ال", "ألف")) for x in FURU_GOOD + FURU_BAD)
    assert "ل" not in {c for _, cs, _ in MAKHARIJ for c in cs}  # لا تُرمَّم اللامُ من الذاكرة
    assert SIFAT["mutbaqa"][1][:1] != ("ص",) or SIFAT["mutbaqa"][1] == ("ص", "ض", "ط", "ظ")
