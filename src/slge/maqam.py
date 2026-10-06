"""المقام: الشخصُ من خانات الفعل، والمستترُ لا خانةَ له، والظاهرُ للغائب، والتوكيدُ مطابقة — `Maqam`.

الشخصُ يُقرأ من صدر المضارع (همزةٌ ونونٌ متكلّم، ياءٌ غائب، تاءٌ مخاطبٌ أو غائبة: لا تفصل) أو لاحقةِ
الماضي من جدول `filiyya.SUBJECT_SUFFIXES` أو قالبه (الماضي بلا لاحقةٍ غائب، والأمرُ مخاطب) — `shakhs`.
المستترُ غيابُ لاحقةٍ لا حضورُها؛ حكمُه وجوبًا للحاضر وجوازًا للغائب (`hukm_istitar`). الظاهرُ (اسمٌ
مرفوعٌ بعد الفعل) للغائب وحده (`valid`)، والظهورُ يُقرأ من الفعل والكلمة التالية (`zuhur`). التوكيدُ
اللفظيّ: منفصلٌ من `categories.PRONOUNS` يطابق شخصَ الفعل (`tawkid`). القياسُ على MASAQ في
`tools/gen_maqam_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.categories import PRONOUNS
from slge.cells import STATES, Cell
from slge.fil import MAZID, MAZID_AMR
from slge.filiyya import SUBJECT_SUFFIXES, _ends_with_state, has_subject
from slge.tawabi import case_class
from slge.wazn import AWZAN, fill, root_of
from slge.zuruf import set_last

__all__ = ["DETACHED", "PRESENT_TEMPLATES", "SUFFIX_SHAKHS", "hukm_istitar", "same", "shakhs",
           "shakhs_detached", "tawkid", "valid", "with_prefix", "zuhur"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]

PRESENT_TEMPLATES: Final[tuple[int, ...]] = (4, 5, 6, 7, 20, 21, 22, 23, 24, 25, 26, 27, 28)
PAST_TEMPLATES: Final[tuple[int, ...]] = (0, 1, 2, 3, *MAZID)
AMR_TEMPLATES: Final[tuple[int, ...]] = (8, 9, 10, *MAZID_AMR)
_PREFIX: Final[dict[str, str]] = {"ء": "متكلم", "ن": "متكلم", "ت": "مخاطب/غائبة", "ي": "غائب"}
# شخصُ لاحقة الماضي بترتيب الجدول: تُ ونا متكلّم؛ تَ تِ تما تم تنّ وي وين مخاطب؛ وا ا نَ ون ان غائب
SUFFIX_SHAKHS: Final[tuple[str, ...]] = (
    "متكلم", "مخاطب", "مخاطب", "مخاطب", "مخاطب", "مخاطب", "غائب", "غائب", "غائب", "مخاطب",
    "متكلم", "غائب", "مخاطب", "غائب",
)
# شخصُ المنفصل بترتيب جدول `categories.PRONOUNS`
DETACHED: Final[tuple[str, ...]] = ("متكلم",) * 2 + ("مخاطب",) * 5 + ("غائب",) * 5


def with_prefix(k: str, v: Word) -> Word:
    """إبدالُ حامل الصدر بحالته."""

    return ((k, v[0][1]), *v[1:]) if v else v


def _on_template_root(k: int, u: Word) -> bool:
    """على القالب وأصلُه بلا ألف: الألفُ ليست أصلًا."""

    t = AWZAN[k].template
    r = root_of(t, u)
    return r is not None and fill(t, r) == u and "ا" not in r


def _is_present(v: Word) -> bool:
    return any(_on_template_root(k, with_prefix("ي", v)) for k in PRESENT_TEMPLATES)


def _shakhs_present(v: Word) -> str | None:
    """قارئُ الصدر: شخصُ المضارع من حامله الأوّل."""

    return _PREFIX.get(v[0][0]) if v and _is_present(v) else None


def _verb_stem(b: Word) -> bool:
    """جذعُ فعلٍ قبل لاحقة: ماضٍ بفتح الآخر، أو أمرٌ بسكونه، أو مضارعٌ بضمّه بعد ردّ الصدر، أو أجوفٌ محذوفُ
    العين (قُمْ، بِعْ: حرفان ساكنُ الآخر)."""

    return ((len(b) == 2 and b[-1][1] == SUKUN)
            or any(_on_template_root(k, set_last(b, _A)) for k in PAST_TEMPLATES)
            or any(_on_template_root(k, set_last(b, SUKUN)) for k in AMR_TEMPLATES)
            or _is_present(set_last(b, _U)))


def _shakhs_suffix(v: Word) -> str | None:
    """شخصُ اللاحقة: المضارعُ بلاحقةٍ (تَفْعَلُونَ، يَفْعَلُونَ) صدرُه يفصل؛ وإلّا الجدول."""

    for (p, st), s in zip(SUBJECT_SUFFIXES, SUFFIX_SHAKHS, strict=True):
        b = v[: -len(p)]
        if _ends_with_state(v, p, st) and _verb_stem(b):
            if _is_present(set_last(b, _U)):
                return {"ت": "مخاطب", "ي": "غائب"}.get(v[0][0])
            return s
    return None


def _shakhs_past(v: Word) -> str | None:
    if has_subject(v):
        return None
    if any(_on_template_root(k, v) for k in PAST_TEMPLATES):
        return "غائب"
    if v[-1:] == (("ت", SUKUN),) and any(_on_template_root(k, v[:-1]) for k in PAST_TEMPLATES):
        return "غائب"  # فَعَلَتْ
    if any(_on_template_root(k, v) for k in AMR_TEMPLATES):
        return "مخاطب"
    return None


def shakhs(v: Word) -> str | None:
    """الشخصُ من الخانات: اللاحقةُ على جذعِ فعل، وإلّا الصدرُ، وإلّا الماضي بقالبه والأمرُ مخاطب."""

    for f in (_shakhs_suffix, _shakhs_present, _shakhs_past):
        s = f(v)
        if s is not None:
            return s
    return None


def hukm_istitar(s: str) -> str | None:
    """وجوبًا للحاضر، جوازًا للغائب؛ وتاءُ المضارع لا تفصل."""

    if s in ("متكلم", "مخاطب"):
        return "وجوب"
    return "جواز" if s == "غائب" else None


def valid(s: str, z: str) -> bool:
    """الظهورُ الجائز: الاسمُ الظاهر للغائب (أو تاءِ الغائبة)، والمتّصلُ والمستترُ لكلّ شخص."""

    return s in ("غائب", "مخاطب/غائبة") if z == "ظاهر" else True


def zuhur(v: Word, nxt: Word | None) -> str:
    """لاحقةُ فاعلٍ ⇒ متّصل؛ وإلّا مرفوعٌ بعده ⇒ ظاهر، وإلّا مستتر."""

    if has_subject(v):
        return "متصل"
    return "ظاهر" if nxt is not None and case_class(nxt) == "رفع" else "مستتر"


def shakhs_detached(d: Word) -> str | None:
    return next((s for p, s in zip(PRONOUNS, DETACHED, strict=True) if p == d), None)


def same(a: str, b: str) -> bool:
    return b in ("مخاطب", "غائب") if a == "مخاطب/غائبة" else a == b


def tawkid(v: Word, d: Word) -> bool:
    """التوكيدُ اللفظيّ للضمير: منفصلٌ من الجدول بعد الفعل يطابق شخصَه."""

    a, b = shakhs(v), shakhs_detached(d)
    return a is not None and b is not None and same(a, b)


def _check() -> None:
    from slge.rawabit import cells_of
    from slge.wazn import mizan

    for k in PRESENT_TEMPLATES:
        m = mizan(AWZAN[k].template)
        got = [shakhs(with_prefix(p, m)) for p in "ءنتي"]
        assert got == ["متكلم", "متكلم", "مخاطب/غائبة", "غائب"], k
    assert len(SUFFIX_SHAKHS) == len(SUBJECT_SUFFIXES) and len(DETACHED) == len(PRONOUNS) == 12
    adrusu, darasa, darabtu = cells_of("أَدْرُسُ"), cells_of("دَرَسَ"), cells_of("ضَرَبْتُ")
    assert shakhs(adrusu) == "متكلم" and not has_subject(adrusu)
    assert shakhs(darasa) == "غائب" and not has_subject(darasa)
    assert shakhs(darabtu) == "متكلم" and has_subject(darabtu)
    assert shakhs(cells_of("دَرَسَتْ")) == "غائب" and shakhs(cells_of("اُدْرُسْ")) == "مخاطب"
    assert shakhs(cells_of("تَدْرُسُ")) == "مخاطب/غائبة" and shakhs(cells_of("زَيْدٌ")) is None
    assert hukm_istitar("متكلم") == "وجوب" and hukm_istitar("غائب") == "جواز"
    assert valid("غائب", "ظاهر") and not valid("متكلم", "ظاهر") and valid("متكلم", "مستتر")
    zayd = cells_of("زَيْدٌ")
    assert zuhur(darasa, zayd) == "ظاهر" and zuhur(darasa, cells_of("اَدَّرْسَ")) == "مستتر"
    assert zuhur(darabtu, None) == "متصل"
    ana, anta, huwa, hiya = (cells_of(w) for w in ("أَنَا", "أَنْتَ", "هُوَ", "هِيَ"))
    assert tawkid(darabtu, ana) and tawkid(adrusu, ana) and tawkid(darasa, huwa)
    assert tawkid(cells_of("تَدْرُسُ"), anta) and tawkid(cells_of("تَدْرُسُ"), hiya)
    assert not tawkid(darabtu, anta) and not tawkid(adrusu, huwa) and not tawkid(darasa, zayd)
    assert all(shakhs_detached(p) is not None for p in PRONOUNS)


_check()
