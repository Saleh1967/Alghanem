"""الجسرُ من المنطوق إلى المفهوم الأصوليّ في `gate` (ADR ١١٢، ١١٣): مرآةٌ لـ`A116.MantuqMafhum`.

طبقةُ حكمٍ فوق الترخيص (م١٠): لا تقرأ شهادةً ولا تمسّها، ولا تدخل `gate.enter` (م١١).
والمطابقةُ مع Lean سطرًا سطرًا على `formal/a116/mantuq.csv` (`tests/test_gate_mantuq.py`).
والأسطرُ المذكورة أسطرُ ج3 بترقيم الغانم (`corpora/nabhani/shakhsiyya_j3.txt.gz`).

* `naw(shart, illiyya, maqsud, muwafiq)`: النوعُ من صفات اللازم الأربع (س520–534).
* `mukhalafa(qayd, mana, mufhim, siyaq, aghlab, muattil)`: `Yumal(MafhumUsul)` أو `Layumal(mani)`
  (س534–555).
* `martaba_waqi(mudaa, hukm)` و`hukm_naql(jisr, mudaa, hukm, tawatur)`: الرتبةُ من شهادات
  المفهوم الذي يحمله الحكمُ بعينه (المادّة ٢٤).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Final, NamedTuple

NAW: Final = ("iqtida", "tanbih", "ishara", "muwafaqa", "mukhalafa")
QAYD: Final = ("sifa", "shart", "ghaya", "adad", "ism", "innama")
MANI: Final = ("adadBilaSiyaq", "ism", "wasfGhayrMufhim", "innama", "aghlab", "muattil")
JISR: Final = ("wad", "waqi")


class MafhumUsul(NamedTuple):
    naw: str
    mana: str


class Yumal(NamedTuple):
    m: MafhumUsul


class Layumal(NamedTuple):
    mani: str


Hukm = Yumal | Layumal


def naw(shart: bool, illiyya: bool, maqsud: bool, muwafiq: bool) -> str:
    if shart:
        return "iqtida"
    if illiyya:
        return "tanbih"
    if not maqsud:
        return "ishara"
    return "muwafaqa" if muwafiq else "mukhalafa"


def mani_qayd(qayd: str, mufhim: bool = False, siyaq: bool = False) -> str | None:
    if qayd not in QAYD:
        raise ValueError(f"QAYD_UNKNOWN {qayd}")
    if qayd == "sifa":
        return None if mufhim else "wasfGhayrMufhim"
    if qayd == "adad":
        return None if siyaq else "adadBilaSiyaq"
    if qayd in ("ism", "innama"):
        return qayd
    return None


def mukhalafa(qayd: str, mana: str, mufhim: bool = False, siyaq: bool = False,
              aghlab: bool = False, muattil: bool = False) -> Hukm:
    m = mani_qayd(qayd, mufhim, siyaq)
    if m is not None:
        return Layumal(m)
    if aghlab:
        return Layumal("aghlab")
    if muattil:
        return Layumal("muattil")
    return Yumal(MafhumUsul("mukhalafa", mana))


class Shahada(NamedTuple):
    tariq: str   # naql | hiss | aql
    mawda: str   # waqiMakhtum | wad | malumat | marjaMahjub


Mudaa = Sequence[tuple[MafhumUsul, Shahada]]   # كلُّ شهادةٍ مقرونةٌ بالمفهوم الذي تشهد له


def shuhud_for(d: Mudaa, m: MafhumUsul) -> list[Shahada]:
    return [s for k, s in d if k == m]


def martaba_waqi(d: Mudaa, h: Hukm) -> str:
    if isinstance(h, Layumal):
        return "minHaythuHiya"
    ok = any(s.tariq == "hiss" and s.mawda == "waqiMakhtum" for s in shuhud_for(d, h.m))
    return "mafhum" if ok else "maluma"


def hukm_naql(jisr: str, d: Mudaa, h: Hukm, tawatur: bool = False) -> str:
    """`jisr` «wad» (و`tawatur` حكمُ التواتر) أو «waqi».

    المقبولُ الكافي مفهوم، وإلّا معلومةٌ بعدد المقبول؛ وجسرٌ غيرُهما رفضٌ باسمه `JISR_UNKNOWN`.
    """
    if jisr not in JISR:
        raise ValueError(f"JISR_UNKNOWN {jisr}")
    if isinstance(h, Layumal):
        return "minHaythuHiya"
    tariq = "naql" if jisr == "wad" else "hiss"
    maqbul = [s for s in shuhud_for(d, h.m) if s.tariq == tariq]
    if not maqbul:
        return "maluma:0"
    if jisr == "wad":
        kafi = all(s.mawda in ("wad", "malumat") for s in maqbul)
        rutba = "qati" if tawatur else "zanni"
    else:
        kafi = all(s.mawda == "waqiMakhtum" for s in maqbul)
        rutba = "qati"
    return f"mafhum:{rutba}:{len(maqbul)}" if kafi else f"maluma:{len(maqbul)}"
