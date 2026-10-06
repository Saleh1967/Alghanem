"""الجهةُ والزمن: الصيغةُ من الحالات لكلّ جذر، والأمرُ للمخاطب، والإزاحةُ على المضارع وحده — `Jiha`.

الصيغةُ (ماضٍ/مضارع/أمر) تفصلها حالاتُ الخانات وحدَها: أصنافُ القوالب الثلاثة متباينةُ الحالات
(`states_disjoint`)، فقارئُ الصيغة `sigha` يقرأ كلَّ صورةٍ على قالبها لكلّ جذرٍ لا ألفَ فيه. الأمرُ
مخاطبٌ عند قارئ المقام (`maqam.shakhs`)، وأمرُ الغائب باللام على المضارع. أدواتُ الإزاحة (`SHIFTS`:
السين، سَوْفَ، لَمْ، لَنْ، كَانَ) عمليّاتٌ تشترط المضارع (`shift`) وتُردّ بعينها. القارئُ `jiha` يقرأ
الجهةَ من الكلمة وما قبلها.
القياسُ على MASAQ (PV/IV/CV وسمُ السين) في `tools/gen_jiha_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell
from slge.jazm import sukun
from slge.maqam import (
    AMR_TEMPLATES,
    PAST_TEMPLATES,
    PRESENT_TEMPLATES,
    _is_present,
    _shakhs_present,
)
from slge.maqam import _on_template_root as on_template_root
from slge.nawasikh import nasb
from slge.rawabit import PARTICLES, cells_of
from slge.wazn import AWZAN
from slge.zuruf import set_last

__all__ = ["KANA", "LAM", "LAN", "SA", "SAWFA", "SHIFTS", "jiha", "shift", "sigha",
           "states_disjoint"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]

SA: Final[Word] = cells_of("سَ")
SAWFA: Final[Word] = cells_of("سَوْفَ")
LAM: Final[Word] = cells_of("لَمْ")
LAN: Final[Word] = cells_of("لَنْ")
KANA: Final[Word] = cells_of("كَانَ")
SHIFTS: Final[tuple[str, ...]] = ("س", "سوف", "لم", "لن", "كان")


def _states(k: int) -> tuple[str, ...]:
    return tuple(s.state for s in AWZAN[k].template)


def states_disjoint() -> bool:
    """أصنافُ الصيغ الثلاثة متباينةُ الحالات قالبًا قالبًا."""

    past = {_states(k) for k in PAST_TEMPLATES}
    pres = {_states(k) for k in PRESENT_TEMPLATES}
    amr = {_states(k) for k in AMR_TEMPLATES}
    return past.isdisjoint(pres) and past.isdisjoint(amr) and pres.isdisjoint(amr)


def sigha(v: Word) -> str | None:
    """ماضٍ على قالبه، أو أمرٌ على قالبه، أو مضارعٌ بصدرٍ من الأربعة على قالبه بعد ردّ الصدر."""

    if any(on_template_root(k, v) for k in PAST_TEMPLATES):
        return "ماضٍ"
    if any(on_template_root(k, v) for k in AMR_TEMPLATES):
        return "أمر"
    if _is_present(v) and _shakhs_present(v) is not None:
        return "مضارع"
    return None


def shift(s: str, v: Word) -> tuple[Word, Word] | None:
    """الإزاحةُ على المضارع وحده: (الأداةُ منفصلةً، الفعلُ بعد عملها)؛ السينُ متّصلة."""

    if sigha(v) != "مضارع":
        return None
    return {"س": ((), (*SA, *v)), "سوف": (SAWFA, v), "لم": (LAM, sukun(v)), "لن": (LAN, nasb(v)),
            "كان": (KANA, v)}[s]


def jiha(prev: Word, v: Word) -> str:
    """الجهةُ من الكلمة وما قبلها: السينُ صدرًا، أو سَوْفَ/لَمْ/لَنْ/كَانَ قبلَه، وإلّا صيغتُه."""

    if v[:1] == SA and sigha(v[1:]) == "مضارع":
        return "مستقبل"
    s = sigha(v)
    if s == "ماضٍ" or s == "أمر":
        return s
    if s == "مضارع":
        return "مستقبل" if prev == SAWFA else ("ماضٍ مستمرّ" if prev == KANA else "مضارع")
    if sigha(set_last(v, _U)) == "مضارع":
        if prev == LAM:
            return "ماضٍ منفيّ"
        if prev == LAN:
            return "مستقبل منفيّ"
    return "—"


def _check() -> None:
    from slge.maqam import shakhs, with_prefix
    from slge.wazn import mizan

    assert states_disjoint()
    for k in PAST_TEMPLATES:
        assert sigha(mizan(AWZAN[k].template)) == "ماضٍ"
    for k in AMR_TEMPLATES:
        m = mizan(AWZAN[k].template)
        assert sigha(m) == "أمر" and shakhs(m) == "مخاطب"
    for k in PRESENT_TEMPLATES:
        assert all(sigha(with_prefix(p, mizan(AWZAN[k].template))) == "مضارع" for p in "ءنتي")
    names = {p.name: p.amal for p in PARTICLES}
    assert names["سَ"] == "" == names["سَوْفَ"] and names["لَمْ"] == "جزم" and names["لَنْ"] == "نصب"
    kataba, yaktubu, uktub = cells_of("كَتَبَ"), cells_of("يَكْتُبُ"), cells_of("اُكْتُبْ")
    assert shift("س", kataba) is None and shift("س", uktub) is None
    assert shift("س", yaktubu) == ((), cells_of("سَيَكْتُبُ"))
    assert shift("لم", yaktubu) == (LAM, cells_of("يَكْتُبْ"))
    assert shift("لن", yaktubu) == (LAN, cells_of("يَكْتُبَ"))
    assert jiha((), kataba) == "ماضٍ" and jiha((), yaktubu) == "مضارع" and jiha((), uktub) == "أمر"
    assert jiha((), cells_of("سَيَكْتُبُ")) == "مستقبل" == jiha(SAWFA, yaktubu)
    assert jiha(LAM, cells_of("يَكْتُبْ")) == "ماضٍ منفيّ"
    assert jiha(LAN, cells_of("يَكْتُبَ")) == "مستقبل منفيّ"
    assert jiha(KANA, yaktubu) == "ماضٍ مستمرّ" and jiha((), cells_of("سَكَتَبَ")) == "—"
    assert jiha(SAWFA, kataba) == "ماضٍ" and jiha((), cells_of("زَيْدٌ")) == "—"


_check()
