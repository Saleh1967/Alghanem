"""الجذع: تسويةُ الآخر قبل القالب، وفصلُ الزوائد بردٍّ بعينه — مرآةُ `Jidh`.

الإعرابُ والمزاجُ حالةُ الخانة الأخيرة لا جزءٌ من القالب: فالمطابقةُ بعد تسوية الآخر إلى حالة آخر
القالب (`on_template_mod`؛ مبرهَنٌ `rootOf_setLast`، `onTemplateMod_setLast`). وفصلُ الزوائد قطعٌ من
الجداول الحاصرة (السوابقُ المفردة وأل، والضمائرُ المتّصلة ولواحقُ الفاعل) يُردّ بالإلصاق
(`peelPrefix_sound`، `peelSuffix_sound`، `dropAl_sound`)، والقارئُ `jidh` لا يعيد قراءةً إلّا وردُّها
الكلمةُ بعينها (`jidh_restores`). القياسُ على مودَع شهادات المصحف وعلى قسمة MASAQ المحجوبة في
`tools/gen_jidh_index.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Final

from slge.cells import SUKUN, Cell
from slge.filiyya import OBJECT_SUFFIXES, SUBJECT_SUFFIXES
from slge.maqam import _on_template_root as on_template_root
from slge.maqam import with_prefix
from slge.marifa import al, drop_tanwin, has_al
from slge.wazn import AWZAN, Template
from slge.zuruf import set_last

__all__ = ["ENCLITICS", "PROCLITICS", "Reading", "jidh", "last_state", "on_template_mod",
           "stem_senses"]

Word = tuple[Cell, ...]
_A: Final = "فتح"
_I: Final = "كسر"
PROCLITICS: Final[tuple[Word, ...]] = (
    (("و", _A),), (("ف", _A),), (("ب", _I),), (("ل", _I),), (("ك", _A),), (("س", _A),),
    (("ء", _A),), (("ل", _A),),
)
"""السوابقُ المفردة: و ف ب ل ك س أ (الاستفهام) لَ (التوكيد)."""
ENCLITICS: Final[tuple[Word, ...]] = (*OBJECT_SUFFIXES, *(p for p, _ in SUBJECT_SUFFIXES))
"""اللواحق: الضمائرُ المتّصلة ولواحقُ الفاعل."""


def last_state(t: Template) -> str:
    """حالةُ آخر القالب."""

    return t[-1].state if t else _A


def on_template_mod(k: int, w: Word) -> bool:
    """المطابقةُ بعد تسوية الآخر إلى حالة القالب، بجذرٍ لا ألفَ فيه."""

    return bool(w) and on_template_root(k, set_last(w, last_state(AWZAN[k].template)))


_BY_LEN: Final[dict[int, tuple[int, ...]]] = {
    n: tuple(k for k in range(len(AWZAN)) if len(AWZAN[k].template) == n)
    for n in {len(w.template) for w in AWZAN}
}
"""القوالبُ بطولها: المطابقةُ تشترط تساوي الطول (`root_of` يردّ `None` وإلّا)."""


@cache
def stem_senses(s: Word) -> tuple[int, ...]:
    """معاني الجذع بعد تسوية آخره؛ والمضارعُ بردّ صدره ياءً إن لم يُقرأ مباشرة."""

    v = drop_tanwin(s)
    direct = tuple(k for k in _BY_LEN.get(len(v), ()) if on_template_mod(k, v))
    if direct or not v or v[0][0] not in "ءنت":
        return direct
    u = with_prefix("ي", v)
    return tuple(k for k in _BY_LEN.get(len(u), ()) if on_template_mod(k, u))


@dataclass(frozen=True, slots=True)
class Reading:
    """قراءةُ جذع: السوابقُ، أل (0 لا، 1 بهمزتها، 2 موصولةً بلا همزةٍ بعد سابقة)، الجذعُ، اللاحقةُ،
    والقوالب."""

    pre: tuple[Word, ...]
    al: int
    stem: Word
    suf: Word
    templates: tuple[int, ...]

    def restore(self) -> Word:
        """الردُّ: السوابقُ ثمّ (أل الجذع | أل الموصولة | الجذع) ثمّ اللاحقة."""

        core = al(self.stem) if self.al == 1 else al(self.stem)[1:] if self.al == 2 else self.stem
        return (*(c for p in self.pre for c in p), *core, *self.suf)


def _peel_prefix(p: Word, w: Word) -> Word | None:
    return w[len(p):] if w[: len(p)] == p else None


def _peel_suffix(q: Word, w: Word) -> Word | None:
    n = len(w) - len(q)
    return w[:n] if n >= 0 and w[n:] == q else None


def _drop_al(w: Word, kind: int) -> Word | None:
    """إسقاطُ أل بهمزتها (1) أو موصولةً بلا همزةٍ (2): الجذعُ ما تعيد `al` منه الكلمةَ بعينها."""

    if kind == 1:
        s = w[2:]
        return s if has_al(w) and al(s) == w else None
    s = w[1:]
    return s if s and al(s)[1:] == w else None


def jidh(w: Word) -> tuple[Reading, ...]:
    """قراءاتُ الكلمة: كلُّ قطعٍ من الجداول يعيد الكلمةَ بعينها وجذعُه على قالبٍ بعد التسوية."""

    pres: list[tuple[Word, ...]] = [()] + [(p,) for p in PROCLITICS]
    pres += [(p, q) for p in PROCLITICS for q in PROCLITICS]
    pres = [pre for pre in pres if _peel_prefix(tuple(c for p in pre for c in p), w) is not None]
    sufs: list[Word] = [q for q in ((), *ENCLITICS) if _peel_suffix(q, w) is not None]
    out: list[Reading] = []
    for pre in pres:
        w1 = _peel_prefix(tuple(c for p in pre for c in p), w)
        assert w1 is not None
        for suf in sufs:
            w2 = _peel_suffix(suf, w1)
            if w2 is None:
                continue
            for use_al in (0, 1, 2):
                if use_al == 2 and (not pre or pre[-1][0][0] == "ء"):
                    continue  # الموصولةُ بلا همزةٍ بعد سابقةٍ غيرِ همزة الاستفهام (آلْآنَ تُكتب بالمدّ)
                stem = _drop_al(w2, use_al) if use_al else w2
                if not stem:
                    continue
                ts = stem_senses(stem)
                if not ts:
                    continue
                r = Reading(pre, use_al, stem, suf, ts)
                if r.restore() == w:
                    out.append(r)
    return tuple(out)


def _check() -> None:
    from slge.rawabit import cells_of

    for k in (0, 29, 48):
        t = AWZAN[k].template
        from slge.wazn import fill
        w = fill(t, ("ك", "ت", "ب"))
        for st in ("فتح", "كسر", "ضم", SUKUN):
            assert on_template_mod(k, set_last(w, st)), (k, st)  # تسويةُ الآخر
    walard = cells_of("وَلْأَرْضِ")  # صورةُ الشهادة: همزةُ الوصل ساقطةٌ بعد الواو
    rs = jidh(walard)
    assert [(len(r.pre), r.al, r.templates) for r in rs] == [(1, 2, (29,))]
    assert rs[0].restore() == walard
    rs = jidh(cells_of("أَلْأَرْضُ"))
    assert [(len(r.pre), r.al, r.templates) for r in rs] == [(0, 1, (29,))]
    assert [r.templates for r in jidh(cells_of("رَبِّ"))] == [(29,)]
    r = jidh(cells_of("كَذَّبُو"))  # قراءتان على الخانة: فَعَّلَ + واو الجماعة، أو كَ + الذَّبُو — القرينةُ تفصل
    assert len(r) == 2 and r[0].suf == (("و", SUKUN),) and r[0].templates == (12,) and r[1].al == 2
    r = jidh(cells_of("وَشَّمْسِ"))
    assert len(r) == 1 and r[0].al == 2 and r[0].templates == (29,)
    r = jidh(cells_of("بِكِتَابِهِمْ"))
    assert len(r) == 1 and len(r[0].pre) == 1 and len(r[0].suf) == 2
    assert r[0].templates == (35, 41, 93)
    assert [r.templates for r in jidh(cells_of("وَجَدَ"))] == [(0, 36)]  # فعلٌ أو مصدرٌ بعد التسوية
    assert jidh(cells_of("لَا")) == ()


_check()
