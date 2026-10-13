"""المعقوليّة: حكمٌ ثلاثيٌّ على الحجّة بنيةً، وبطاقةُ مادّة الحوار، وطيُّ المرفوض في «ز» (ADR ٤٩).

مرآةُ `Slge.Maqool` سطرًا بسطر. طبقةُ «الحكم» فوق البوّابات لا فيها (دستورُ الوكيل، المادّة ١٠):
لا تقرأ شهادةً ولا نصًّا؛ مدخلُها حجّةٌ بنيةً تُرسى أبوابُها في معايير `mayaatir_table` المختومة.

* `maqool`: لا بابَ ينفتح والشاهدُ واقعٌ مختوم؛ الدرجةُ قطعيّةٌ للوجود وظنّيّةٌ للحقيقة والصفة (U8).
* `ghayr`: أوّلُ بابٍ ينفتح من البنية وحدَها، بترتيبٍ مثبَّت: الدور (U4)، الرأيُ السابق (U2)،
  تحريفُ الواقع (U1)، الخروجُ عن الموضوع (U6)، ثمّ في الخبر وحدَه التجريدُ والتعميمُ والقياسُ
  الشموليّ (U5).
* `la_hukm`: لا بابَ ولا شاهدٌ مختوم — «مجرّد معلومات» (U3)، لا رفض.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from typing import Final, Literal

from slge.mayaatir_table import KEYS

Kind = Literal["wujud", "haqiqa"]
Daraja = Literal["qati", "zanni"]
Bab = Literal["dawar", "ray_mutanakkir", "tahrif_waqi", "khuruj_mawdu", "tajrid", "taamim",
              "qiyas_shumuli", "khata"]
Sabab = Literal["bila_shahid", "shahid_bitaqa"]

ANCHOR: Final[dict[str, str]] = {
    "dawar": "U4", "ray_mutanakkir": "U2", "tahrif_waqi": "U1", "khuruj_mawdu": "U6",
    "tajrid": "U5", "taamim": "U5", "qiyas_shumuli": "U5", "khata": "U8",
    "bila_shahid": "U3", "shahid_bitaqa": "U3",
}
"""مرساةُ كلّ بابٍ وسببٍ: مفتاحُ معياره في الجدول المختوم (`Maqool.anchor`)."""

assert set(ANCHOR.values()) <= set(KEYS)


@dataclass(frozen=True)
class Shahid:
    """الشاهد: `makhtum` موضعٌ في المودَع المختوم، أو `bitaqa` مادّةُ حوارٍ ببطاقة."""

    kind: Literal["makhtum", "bitaqa"]
    id: int


@dataclass(frozen=True)
class Sabiqa:
    """معلومةٌ سابقة: رقمُها، أهي رأيٌ سابق (U2)، وما تقوم عليه."""

    id: int
    ray: bool = False
    deps: tuple[int, ...] = ()


@dataclass(frozen=True)
class Hujja:
    claim: int
    kind: Kind
    shahid: Shahid | None
    presented: int
    judged_on: int
    mawdu: int
    prem_topics: tuple[int, ...] = ()
    sabiqa: tuple[Sabiqa, ...] = ()
    khabar: bool = False
    with_circumstances: bool = True
    covered: tuple[int, ...] = ()
    witnessed: tuple[int, ...] = ()
    shumuli: bool = False


@dataclass(frozen=True)
class Hukm:
    """الحكمُ الثلاثيّ: `tag` ∈ {maqool, ghayr, la_hukm} ومعه الدرجة أو البابُ أو السبب."""

    tag: Literal["maqool", "ghayr", "la_hukm"]
    value: str


def succ(h: Hujja, v: int) -> list[int]:
    out = [s.id for s in h.sabiqa] if v == h.claim else []
    for s in h.sabiqa:
        if s.id == v:
            out.extend(s.deps)
    return out


def reach(h: Hujja, n: int, xs: list[int]) -> list[int]:
    for _ in range(n):
        xs = xs + [w for x in xs for w in succ(h, x)]
    return xs


def nodes(h: Hujja) -> list[int]:
    return [h.claim] + [s.id for s in h.sabiqa]


def cyclic(h: Hujja) -> bool:
    ns = nodes(h)
    return any(v in reach(h, len(ns), succ(h, v)) for v in ns)


def door(h: Hujja) -> Bab | None:
    """أوّلُ بابٍ ينفتح من بنية الحجّة وحدَها — لا يقرأ الشاهد."""

    if cyclic(h):
        return "dawar"
    if any(s.ray for s in h.sabiqa):
        return "ray_mutanakkir"
    if h.presented != h.judged_on:
        return "tahrif_waqi"
    if any(t != h.mawdu for t in h.prem_topics):
        return "khuruj_mawdu"
    if h.khabar and not h.with_circumstances:
        return "tajrid"
    if h.khabar and any(e not in h.witnessed for e in h.covered):
        return "taamim"
    if h.khabar and h.shumuli:
        return "qiyas_shumuli"
    return None


def judge(h: Hujja) -> Hukm:
    b = door(h)
    if b is not None:
        return Hukm("ghayr", b)
    if h.shahid is None:
        return Hukm("la_hukm", "bila_shahid")
    if h.shahid.kind == "bitaqa":
        return Hukm("la_hukm", "shahid_bitaqa")
    return Hukm("maqool", "qati" if h.kind == "wujud" else "zanni")


# — بطاقةُ مادّة الحوار (المرحلة الثالثة) —

@dataclass(frozen=True)
class Bitaqa:
    masdar: str
    sha256: str
    naw: Literal["intiqa", "qarina"]
    hadd: str


HEX: Final[frozenset[str]] = frozenset("0123456789abcdef")


def valid(c: Bitaqa) -> bool:
    return bool(c.masdar) and len(c.sha256) == 64 and set(c.sha256) <= HEX and bool(c.hadd)


def admit(c: Bitaqa | None, id_: int) -> Sabiqa | None:
    """لا مادّةَ بلا بطاقةٍ تامّة؛ والمقبولُ معلومةٌ سابقةٌ بلا سوالف — لا رأيٌ ولا مرساة."""

    if c is None or not valid(c):
        return None
    return Sabiqa(id_, False, ())


# — الطيّ في «ز» (المرحلة الرابعة) —

@dataclass(frozen=True)
class Archive:
    maqool: tuple[Hujja, ...] = ()
    muajjal: tuple[Hujja, ...] = ()
    zur: tuple[tuple[Hujja, str], ...] = field(default=())


def archive(hs: Sequence[Hujja]) -> Archive:
    js = [(h, judge(h)) for h in hs]
    return Archive(tuple(h for h, j in js if j.tag == "maqool"),
                   tuple(h for h, j in js if j.tag == "la_hukm"),
                   tuple((h, j.value) for h, j in js if j.tag == "ghayr"))


# — الجولات (دَينُ D-RATING، على U8: «تبقى فكراً صائباً حتى يتبين خطؤها») —

@dataclass(frozen=True)
class Jawla:
    """جولة: شاهدٌ مختومٌ جديد إن وُجد، وهل تبيّن فيها الخطأ."""

    shahid: int | None = None
    khata: bool = False


def run_rounds(h: Hujja, js: Sequence[Jawla], khata: bool = False) -> tuple[Hujja, bool]:
    """`Maqool.runJ`: الشاهدُ الجديدُ يحلّ محلّ القديم مختومًا، والخطأُ إذا تبيّن لا يزول."""

    for j in js:
        if j.shahid is not None:
            h = replace(h, shahid=Shahid("makhtum", j.shahid))
        khata = khata or j.khata
    return h, khata


def judge_rounds(h: Hujja, js: Sequence[Jawla], khata: bool = False) -> Hukm:
    """`Maqool.judgeJ ∘ runJ`: ما تبيّن خطؤه بابُه `khata` (U8)، وإلّا حكمُ الحجّة بعد الجولات."""

    h2, k = run_rounds(h, js, khata)
    return Hukm("ghayr", "khata") if k else judge(h2)
