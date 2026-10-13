"""بوّاباتُ المعنى (ADR ٥٥): التوقّعاتُ من أمثلة ج3 نفسِها لا من الشيفرة.

١. المرساة: كلُّ مفتاحٍ عباراتُه في سطرٍ واحدٍ من ج3 المختوم بقراءةٍ مستقلّة هنا.
٢. الزمن: «لم يفعل»، «لن أبرح»، «ما تفعل»، «ما فعل»، «قد قام زيد»، «سيفعل»، «إن كانت» — كلٌّ بوقته من
نصّه.
٣. العطف: «جاء زيد فعمرو»، «جاء زيد ثم عمرو»، «جاءني زيد لا عمرو» على واقعاتٍ مكتوبةٍ باليد.
٤. التخصيص: «أكرم المجاهدين إن فتحوا الحصن»، «أتمّوا الصيام إلى الليل» على مجالاتٍ صغيرة باليد.
٥. العموم: «أي» و«من» شرطيّتين/استفهاميّتين، «اشتر ما رأيت»، «ما أحسن زيدًا».
وكلُّ قسمٍ بطفرةٍ مرفوضةٍ باسمها.
"""

from __future__ import annotations

import gzip
import hashlib
from collections.abc import Callable
from pathlib import Path

from slge import bawwabat as B
from slge.bawwabat_table import GATES
from slge.huruf import TABLE as HURUF

DATA = Path(__file__).resolve().parent / "data"
J3_SHA = "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4"

Apply = Callable[[str, str], "B.Azmina | None"]


def _j3() -> list[str]:
    raw = gzip.decompress((DATA / "nabhani-shakhsiyya-3.txt.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest() == J3_SHA
    return raw.decode("utf-8").split("\n")


def test_every_gate_on_its_line() -> None:
    lines = _j3()
    assert len(GATES) == 24
    for key, _name, ln, phrases in GATES:
        assert all(p in lines[ln - 1] for p in phrases), key
        assert sum(all(p in x for p in phrases) for x in lines) == 1, key


# (الأداة، الهيئة، الوقتُ المسمّى في النصّ) — من أمثلة ج3 527–531، 539، 498
EXAMPLES: tuple[tuple[str, str, tuple[bool, bool, bool, bool]], ...] = (
    ("lam", "mudari", (True, True, False, False)),       # «لم يفعل» — قلبٌ إلى الماضي
    ("lamma", "mudari", (True, True, False, False)),     # «ولما يفعل»
    ("lan", "mudari", (False, False, False, True)),      # «لن أبرح اليوم مكاني»
    ("la", "mudari", (False, False, False, True)),       # «لا أبرح» — نفيُ المستقبل
    ("ma", "mudari", (False, False, True, False)),       # «ما تفعل» — نفيُ الحال
    ("ma", "madi", (False, True, False, False)),         # «ما فعل» — الماضي القريب من الحال
    ("qad", "madi", (False, True, False, False)),        # «قد قام زيد» — تقريبُ الماضي من الحال
    ("sin", "mudari", (False, False, False, True)),      # «سيفعل»
    ("sawfa", "mudari", (False, False, False, True)),    # «سوف يقوم»
    ("an", "mudari", (False, False, False, True)),       # «أريد أن تفعل»
    ("inShart", "mudari", (False, False, False, True)),  # «وإن تفعل»
    ("inNafy", "madi", (False, False, True, False)),     # «إِنْ كَانَتْ إِلَّا صَيْحَةً» — نفيُ الحال
)


def _time_failures(app: Apply) -> list[str]:
    bad = [f"{a}/{h}" for a, h, z in EXAMPLES if app(a, h) != z]
    # الهيئةُ وحدَها: «قام» ماضٍ، و«يقوم» حاضرٌ ومستقبلٌ في اللفظ واحد
    if B.zaman_of("madi") != (True, True, False, False):
        bad.append("madi")
    if B.zaman_of("mudari") != (False, False, True, True):
        bad.append("mudari")
    return bad


def test_time_from_nabhani_examples() -> None:
    assert _time_failures(B.apply) == []
    assert B.zaman_of("amr") is None  # AMR_TIME_UNSOURCED
    assert all(B.apply(a, "amr") is None for a in B.ADAT)


def test_takhlis_and_qalb() -> None:
    qalb = [(a, h) for a in B.ADAT for h in B.HAYAA if B.qalb(a, h)]
    assert qalb == [("lam", "mudari"), ("lamma", "mudari"), ("inNafy", "madi")]
    for a in B.ADAT:
        for h in B.HAYAA:
            if B.apply(a, h) is not None:
                assert B.takhlis(a, h) != B.qalb(a, h), (a, h)
    assert B.reach() == [B.PAST, B.HAL_MUSTAQBAL, B.MUSTAQBAL, B.QARIB, B.HAL]


def test_mutant_qalb_as_takhlis_rejected() -> None:
    """QALB_AS_TAKHLIS: «لم» تخليصًا للحال بدل قلبه ماضيًا."""

    def mutant(a: str, h: str) -> B.Azmina | None:
        return B.HAL if (a, h) == ("lam", "mudari") else B.apply(a, h)

    assert _time_failures(mutant) == ["lam/mudari"]


def test_mutant_three_times_rejected() -> None:
    """THREE_TIMES: إسقاطُ «الماضي القريب» إلى الماضي كلّه — يرفضه «ما فعل» و«قد قام»."""

    def mutant(a: str, h: str) -> B.Azmina | None:
        z = B.apply(a, h)
        return B.PAST if z == B.QARIB else z

    assert _time_failures(mutant) == ["ma/madi", "qad/madi"]


def test_tools_are_the_huruf_rows() -> None:
    names = {"sin": "سَ", "sawfa": "سَوْفَ", "an": "أَنْ", "inShart": "إِنْ", "la": "لَا", "lan": "لَنْ",
             "lam": "لَمْ", "lamma": "لَمَّا", "ma": "مَا", "inNafy": "إِنْ (النفي)", "qad": "قَدْ"}
    for a, i in B.ADAT_HARF.items():
        assert HURUF[i].name == names[a], a
    atf = ["وَ", "فَ", "ثُمَّ", "حَتَّى", "أَوْ", "أَمْ", "لَا", "بَلْ", "لَكِنْ"]
    assert [HURUF[B.ATF_HARF[t]].name for t in B.ATF] == atf


# العطف: (الحرف، صدقُ الأوّل، صدقُ الثاني، وقتُ الأوّل، وقتُ الثاني، الصدقُ المتوقَّع)
ATF_ROWS: tuple[tuple[str, bool, bool, int, int, bool], ...] = (
    ("fa", True, True, 0, 1, True),        # «جاء زيد فعمرو»: عقبَه
    ("fa", True, True, 0, 2, False),       # بينهما فاصل: ليس تعقيبًا
    ("thumma", True, True, 0, 2, True),    # «جاء زيد ثم عمرو»: تراخٍ
    ("thumma", True, True, 0, 1, False),
    ("waw", True, True, 2, 0, True),       # «جاء زيد وعمرو»: لا ترتيبَ ولا معيّة
    ("hatta", True, True, 1, 0, False),    # الترتيب
    ("la", True, False, 0, 0, True),       # «جاءني زيد لا عمرو»
    ("lakin", False, True, 0, 0, True),    # «ما جاءني زيد لكن عمرو»
    ("bal", True, True, 0, 0, False),
    ("aw", False, True, 0, 0, True),       # تعليقُ الحكم بأحدهما
    ("am", False, False, 0, 0, False),
)


def _atf_failures(f: Callable[[str, bool, bool, int, int], bool]) -> list[str]:
    return [f"{r[0]}{r[1:5]}" for r in ATF_ROWS if f(*r[:5]) != r[5]]


def test_atf_rows() -> None:
    assert _atf_failures(B.sidq) == []
    for a in (False, True):
        for b in (False, True):
            for ta in range(4):
                for tb in range(4):
                    assert B.sidq("waw", a, b, ta, tb) == B.sidq("waw", b, a, tb, ta)
                    assert B.sidq("hatta", a, b, ta, tb) == (
                        B.sidq("fa", a, b, ta, tb) or B.sidq("thumma", a, b, ta, tb))


def test_mutant_fa_without_taqib_rejected() -> None:
    """FA_WITHOUT_TAQIB: الفاءُ ترتيبًا بلا تعقيب — تساوي «ثمّ» في الفاصل."""

    def mutant(t: str, a: bool, b: bool, ta: int, tb: int) -> bool:
        return (a and b and ta < tb) if t == "fa" else B.sidq(t, a, b, ta, tb)

    assert _atf_failures(mutant) == ["fa(True, True, 0, 2)"]


MUJAHIDUN = range(6)
FATAHU = {1, 3}


def test_takhsis_on_hand_domains() -> None:
    amm: Callable[[int], bool] = lambda x: True  # noqa: E731 — «أكرم المجاهدين»
    fath: Callable[[int], bool] = lambda x: x in FATAHU  # noqa: E731
    assert [x for x in MUJAHIDUN if B.shart(amm, fath, x)] == [1, 3]
    assert [x for x in MUJAHIDUN if B.mafhum_shart(amm, fath, x)] == [0, 2, 4, 5]
    assert [x for x in MUJAHIDUN if B.istithna(amm, fath, x)] == [0, 2, 4, 5]
    # «أتمّوا الصيام إلى الليل»: الساعاتُ 0..23 والليلُ من 18 — ما بعد «إلى» خارج
    hours = [x for x in range(24) if B.ghaya(lambda _x: True, 18, x)]
    assert hours == list(range(18))
    assert not B.ghaya(lambda _x: True, 18, 18)
    # النكرة في سياق النفي: «ما قام أحد»
    assert B.nakira_nafy(lambda x: x in FATAHU, MUJAHIDUN) is False
    assert B.nakira_nafy(lambda x: x > 9, MUJAHIDUN) is True


def test_mutant_ghaya_inclusive_rejected() -> None:
    """GHAYA_INCLUSIVE: الحدُّ داخلٌ — يخالف «فحكم الليل الذي بعد إلى مخالف لما قبلها»."""

    def mutant(x: int) -> bool:
        return x <= 18

    assert mutant(18) != B.ghaya(lambda _x: True, 18, 18)


UMUM: tuple[tuple[str, str, str | None], ...] = (
    ("أي", "istifham", "kull"), ("أي", "mawsul", None), ("أي", "munada", None),  # «يا أيها الرجل»
    ("من", "shart", "aqil"), ("من", "mawsul", None), ("من", "mawsuf", None),
    ("ما", "mawsul", "ghayrAqil"),    # «اشتر ما رأيت»
    ("ما", "taajjub", None),          # «ما أحسن زيدًا»
    ("ما", "mawsuf", None),           # «مررت بما معجب لك»
    ("أين", "shart", "amkina"), ("حيث", "shart", "amkina"), ("متى", "shart", "zaman"),
    ("كل", "mawsul", "kull"), ("الذين", "mawsul", "kull"),
)


def _umum_failures(f: Callable[[str, str], str | None]) -> list[str]:
    return [f"{s}/{d}" for s, d, m in UMUM if f(s, d) != m]


def test_umum_from_text() -> None:
    assert _umum_failures(B.umum) == []
    assert B.umum("رجل", "shart") is None


def test_mutant_ayy_always_umum_rejected() -> None:
    """AYY_ALWAYS_UMUM: «أي» عامّةً في كلّ دور — يخالف «وشرط أي أن تكون استفهامية أو شرطية»."""

    def mutant(s: str, d: str) -> str | None:
        return "kull" if s == "أي" else B.umum(s, d)

    assert _umum_failures(mutant) == ["أي/mawsul", "أي/munada"]
