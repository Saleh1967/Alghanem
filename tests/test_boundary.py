"""قانونُ الحدّ في البوّابة = مبرهناتُ `A116.Boundary`:
لا ابتداءَ بساكن، الوقفُ يُسكِّن، همزةُ الوصل تسقط موصولةً ولا تُقبل بعد ساكن."""

from __future__ import annotations

from gate import Refusal, enter
from gate.contextual import Context, project

SUKUN = "ْ"
AL_HAMD = "الْحَمْدُ"


def _atoms(word: str, **ctx: str) -> tuple[str, ...]:
    d = project(word, Context(**ctx))
    assert d["status"] == "READY", (word, ctx, d["reasons"])
    return tuple(d["atoms"])


def test_no_start_with_sukun() -> None:
    """`no_start_with_sukun`: كلُّ شهادةٍ في الابتداء تبدأ بمتحرّك."""

    for w in ("كِتَابٌ", AL_HAMD, "وَالشَّمْسِ", "لِلشَّمْسِ"):
        cert = enter(w.encode("utf-8"))
        if not isinstance(cert, Refusal):
            assert not cert.atoms[0].endswith(SUKUN), w


def test_pause_ends_with_sukun() -> None:
    """`pause_ends_with_sukun`: الوقفُ يُسكِّن الآخر (ويُسقط التنوين، ويقلب التاء المربوطة هاءً)."""

    assert _atoms("كِتَابٌ", exit="continue")[-2:] == ("بُ", "نْ")
    assert _atoms("كِتَابٌ", exit="pause")[-1] == "بْ"
    assert _atoms("رَحْمَةٌ", exit="pause")[-1] == "هْ"


def test_wasl_dropped_when_joined_and_junction_is_licensed() -> None:
    """`wasl_dropped_needs_moving_left` + `pause_then_join_is_not_join`: همزةُ الوصل تسقط في الوصل
    فتصير الكلمةُ مبدوءةً بساكن؛ تُقبل بعد متحرّك (قُلِ) بلا وجه، وبعد ساكن (قُلْ) لا يُقبل الساكنان
    (`pause_then_join_is_not_join`) إلّا بوجهٍ مسمًّى: الساكنُ يُكسَر (`Iltiqa.sakinKasra`؛ ADR ٤ — كان
    يُرفض `JUNCTION_NOT_LICENSED` حين لم يكن للوجه اسم)، وتحمله الشهادةُ لا الكلمة."""

    start = enter(AL_HAMD.encode("utf-8"))
    assert not isinstance(start, Refusal) and start.atoms[:2] == ("ءَ", "لْ")
    joined = enter(AL_HAMD.encode("utf-8"), Context(entry="joined", left="قُلِ"))
    assert not isinstance(joined, Refusal) and joined.atoms[0] == "لْ" and joined.junction is None
    after_sukun = enter(AL_HAMD.encode("utf-8"), Context(entry="joined", left="قُلْ"))
    assert not isinstance(after_sukun, Refusal) and after_sukun.junction == "SAKIN_KASRA"
    assert after_sukun.atoms == joined.atoms  # ذرّاتُ الكلمة الثانية كما هي
