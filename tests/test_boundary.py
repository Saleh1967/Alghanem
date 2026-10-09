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


def test_wasl_vowel_from_the_third_letter_mirrors_boundary_lean() -> None:
    """الكتاب س17530–17531: الألفُ الموصولة ابتداءً «مكسورة أبدا إلا أن يكون الحرف الثالث مضموما»،
    وهمزةُ «ال» مفتوحة (`A116.Boundary.waslVowel`؛ المرآةُ قاعدةُ الرسم `WASL`). الألفُ المجرّدة والألفُ
    المرسومةُ وصلةً (ٱ) سواء، والردُّ يعيد الرسمَ بعينه؛ ولا سكونَ أبدًا (`waslVowel_ne_sukun`).
    والأسماءُ الموصولة (اسم، ابن، امرؤ…) مكسورةٌ وإن انضمّ ثالثُها — الكتاب س17573 (`WASL_NOUNS`)؛
    كان التوقّعُ ضمًّا (277667d) قبل مراجعة الكتاب فصُحِّح باسمه لا تبعًا للمخرج."""

    from gate.contextual import Context, project
    from gate.residue import repair, unrepair

    for bare, wasla, first in (("اكْتُبْ", "ٱكْتُبْ", "ءُ"), ("انْصُرْ", "ٱنْصُرْ", "ءُ"),
                               ("اضْرِبْ", "ٱضْرِبْ", "ءِ"), ("اسْتَغْفِرْ", "ٱسْتَغْفِرْ", "ءِ"),
                               ("الْحَمْدُ", "ٱلْحَمْدُ", "ءَ"), ("اسْمُ", "ٱسْمُ", "ءِ"),
                               ("ابْنُ", "ٱبْنُ", "ءِ"), ("اسْتُخْرِجَ", "ٱسْتُخْرِجَ", "ءُ")):
        for w in (bare, wasla):
            canonical, residue = repair(w)
            assert residue and residue[0][0] == "WASL" and unrepair(canonical, residue) == w, w
            d = project(canonical, Context())
            assert d["status"] == "READY" and d["atoms"][0] == first, (w, d["atoms"][:1])
    # الطفرة: من ضمّ الوصلَ لثالثٍ مكسور خالف الكتاب — اضْرِبْ لا تُقرأ ءُ
    assert project(repair("اضْرِبْ")[0], Context())["atoms"][0] != "ءُ"
    # وصلةٌ بسكونٍ صريح: لا تُقرَّر حركتُها — رفضٌ باسمه لا تخمين
    d = project("ٱْكْتُبْ", Context())
    assert d["status"] == "DEFER" and any(
        r.get("reason") == "START_VOWEL_OF_WASL_IS_UNKNOWN" for r in d["reasons"])
