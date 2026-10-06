"""أدواتُ الربط: فهرسةٌ على درجات الترخيص الجبريّ التدريجيّ — مرآةُ `formal/Slge/Rawabit.lean`.

كلُّ أداةٍ تُفهرَس بأعلى درجةٍ يبلغها البرهانُ فيها، لا بمعناها:
- **د٤ الخانة**: خاناتُها مرخَّصة (`Rawabit.particles_licensed`، بالحساب).
- **د٨ الحدّ**: الحرفُ الواحد المتحرّك (و، ف، ل، ب، ك، س) يتّصل بما بعده ولا يُفسد ترخيصَه
  (`proclitic_keeps_licence`، لكلّ كلمة).
- **د١٦ العمل**: ما تُحدثه في آخر ما بعدها (جزم → سكون أو حذفُ النون؛ نصب → فتح أو حذفُ النون؛
  جرّ → كسر) دالّةٌ على الخانة الأخيرة (`govern`)؛ وعلى الأفعال الخمسة بـ`Afal.moodOf`.
- **د١٧ المعنى**: البابُ من الجدول المُرسَل (23 بابًا) — **معلن**؛ البرهانُ لا يبلغه.

والشاهد: خاناتُ الأداة من شهادة البوّابة إن كانت في مجالها (36 من 70)، وإلّا فبالقانون نفسِه
الذي تُخرجه البوّابة (الشدّةُ خانتان، الهمزةُ حامل، ى ألف، التنوينُ حركةٌ ونونٌ ساكنة) موسومةً
«بالقانون». والتراكيبُ (بعبارةٍ أخرى، على سبيل المثال…) **ليست أدواتٍ** بل تياراتُ شهادات: تُذكر
بأسمائها ولا تُودَع خانات.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.afal import mood_of, pronoun_of
from slge.cells import ALPHABET, STATES, Cell, licensed

__all__ = ["BABS", "COMPOUND", "PARTICLES", "Particle", "cells_of", "govern", "tier"]

SUKUN: Final[str] = STATES[3]
_MARK: Final[dict[str, str]] = {"َ": STATES[0], "ِ": STATES[1], "ُ": STATES[2],
                                "ْ": SUKUN, "ً": STATES[0], "ٍ": STATES[1],
                                "ٌ": STATES[2]}
_TANWIN: Final[frozenset[str]] = frozenset("ًٌٍ")
_FOLD: Final[dict[str, str]] = {"ة": "ت", "ى": "ا", "آ": "ءا", "أ": "ء", "إ": "ء", "ؤ": "ء",
                                "ئ": "ء"}


def cells_of(text: str) -> tuple[Cell, ...]:
    """خاناتُ لفظٍ مشكول بقانون البوّابة نفسِه (لا قراءةَ نصٍّ هنا: الثابتُ في الجدول وحدَه)."""

    t = "".join(_FOLD.get(ch, ch) for ch in text)
    out: list[Cell] = []
    i = 0
    while i < len(t):
        ch = t[i]
        if ch not in ALPHABET:
            raise ValueError(f"NOT_A_CARRIER:{ch}")
        i += 1
        shadda, state, tanwin = False, "", False
        while i < len(t) and (t[i] == "ّ" or t[i] in _MARK):
            if t[i] == "ّ":
                shadda = True
            else:
                state, tanwin = _MARK[t[i]], t[i] in _TANWIN
            i += 1
        if ch == "ا" and state:
            ch = "ء"
        elif ch == "ا" or (ch in "وي" and not state):
            state = SUKUN
        elif not state:
            raise ValueError(f"UNVOCALIZED:{ch}")
        if shadda:
            out.append((ch, SUKUN))
        out.append((ch, state))
        if tanwin:
            out.append(("ن", SUKUN))
            if i < len(t) and t[i] == "ا" and (i + 1 == len(t) or t[i + 1] not in _MARK):
                i += 1  # ألفُ التنوين بقيّةُ رسم (A116.Residue TANWIN_ALIF)
    return tuple(out)


@dataclass(frozen=True, slots=True)
class Particle:
    name: str
    bab: int
    amal: str  # "" | "جزم" | "نصب" | "جرّ" | "نصب الاسم ورفع الخبر"
    witness: str  # "شهادة" | "بالقانون"
    proclitic: bool = False

    @property
    def cells(self) -> tuple[Cell, ...]:
        return cells_of(self.name)


def govern(amal: str, word: tuple[Cell, ...]) -> bool:
    """أيَحمل آخرُ الكلمة أثرَ العمل؟ (على الأفعال الخمسة: حذفُ النون جزمًا ونصبًا)."""

    if not word:
        return False
    last = word[-1][1]
    five = pronoun_of(word) is not None and mood_of(word) == "نصب/جزم"
    if amal == "جزم":
        return last == SUKUN or five
    if amal == "نصب":
        return last == STATES[0] or five
    if amal == "جرّ":
        return last == STATES[1]
    if amal == "نصب الاسم ورفع الخبر":
        return last == STATES[0]
    return True


BABS: Final[dict[int, str]] = {
    1: "العطف", 2: "الاستدراك والغاية والتحقيق", 3: "النفي", 4: "الحصر", 5: "التفسير",
    6: "الاقتضاء", 7: "الاستشهاد والتمثيل", 8: "الظرفيّة", 9: "الجواب", 10: "الاستثناء",
    11: "المقابلة والتعارض", 12: "الشكّ والترجيح", 13: "السبب والنتيجة", 14: "السبب",
    15: "النتيجة", 16: "التعليل", 17: "التوكيد", 18: "الإقرار", 19: "الشرط الجازم",
    20: "الشرط غير الجازم", 21: "التفصيل", 22: "الوصل والتتابع", 23: "مخالفة الواقع",
}
"""الأبوابُ الثلاثةُ والعشرون كما في الجدول المُرسَل (معلن)."""

_S, _L = "شهادة", "بالقانون"
PARTICLES: Final[tuple[Particle, ...]] = (
    Particle("وَ", 1, "", _L, True), Particle("فَ", 1, "", _L, True), Particle("ثُمَّ", 1, "", _L),
    Particle("أَوْ", 1, "", _S), Particle("أَمْ", 1, "", _S), Particle("بَلْ", 1, "", _S),
    Particle("لَكِنْ", 2, "", _L), Particle("حَتَّى", 2, "جرّ", _L), Particle("قَدْ", 2, "", _S),
    Particle("لَمَّا", 2, "جزم", _L),
    Particle("لَمْ", 3, "جزم", _S), Particle("لَا", 3, "", _S), Particle("لَنْ", 3, "نصب", _S),
    Particle("لَيْسَ", 3, "", _S),
    Particle("إِنَّمَا", 4, "", _L),
    Particle("أَيْ", 5, "", _L),
    Particle("حَيْثُ", 8, "", _S), Particle("عِنْدَ", 8, "جرّ", _S), Particle("فَوْقَ", 8, "جرّ", _S),
    Particle("تَحْتَ", 8, "جرّ", _S), Particle("أَمَامَ", 8, "جرّ", _L), Particle("خَلْفَ", 8, "جرّ", _L),
    Particle("هُنَا", 8, "", _L), Particle("هُنَالِكَ", 8, "", _S), Particle("بَيْنَمَا", 8, "", _L),
    Particle("نَعَمْ", 9, "", _S), Particle("أَجَلْ", 9, "", _L), Particle("بَلَى", 9, "", _S),
    Particle("كَلَّا", 9, "", _L),
    Particle("إِلَّا", 10, "", _L), Particle("غَيْرُ", 10, "جرّ", _S),
    Particle("لَكِنَّ", 11, "نصب الاسم ورفع الخبر", _L), Particle("أَمَّا", 11, "", _L),
    Particle("لَعَلَّ", 12, "نصب الاسم ورفع الخبر", _L), Particle("رُبَّمَا", 12, "", _L),
    Particle("ظَنَّ", 12, "", _L), Particle("حَسِبَ", 12, "", _S),
    Particle("لِ", 14, "جرّ", _L, True), Particle("إِذْ", 14, "", _S),
    Particle("إِذًا", 15, "", _S),
    Particle("كَيْ", 16, "نصب", _S), Particle("لِكَيْ", 16, "نصب", _S), Particle("لِئَلَّا", 16, "نصب", _L),
    Particle("كَيْلَا", 16, "نصب", _L),
    Particle("إِنَّ", 17, "نصب الاسم ورفع الخبر", _L), Particle("أَنَّ", 17, "نصب الاسم ورفع الخبر", _L),
    Particle("سَ", 17, "", _L, True), Particle("سَوْفَ", 17, "", _S),
    Particle("إِنْ", 19, "جزم", _S), Particle("مَنْ", 19, "جزم", _S), Particle("مَا", 19, "جزم", _S),
    Particle("مَهْمَا", 19, "جزم", _S), Particle("مَتَى", 19, "جزم", _S), Particle("أَيْنَ", 19, "جزم", _S),
    Particle("أَيْنَمَا", 19, "جزم", _S), Particle("أَنَّى", 19, "جزم", _L),
    Particle("حَيْثُمَا", 19, "جزم", _L),
    Particle("كَيْفَمَا", 19, "جزم", _L), Particle("أَيُّ", 19, "جزم", _L),
    Particle("إِذَا", 20, "", _S), Particle("لَوْ", 20, "", _S), Particle("كُلَّمَا", 20, "", _L),
    Particle("لَوْلَا", 20, "", _S),
    Particle("إِمَّا", 21, "", _L),
    Particle("بِ", 14, "جرّ", _L, True), Particle("كَ", 7, "جرّ", _L, True),
    Particle("مِنْ", 13, "جرّ", _S), Particle("عَنْ", 8, "جرّ", _S), Particle("إِلَى", 8, "جرّ", _S),
    Particle("عَلَى", 8, "جرّ", _S),
)
"""70 أداةً مفردة؛ الشاهدُ «شهادة» لما عاد من `gate.enter` (2026-10-06) و«بالقانون» لما خرج عن
المجال."""

COMPOUND: Final[dict[int, tuple[str, ...]]] = {
    5: ("أعني", "بعبارة أخرى", "معنى ذلك", "المراد", "أقصد"),
    6: ("يجب", "ينبغي", "يقتضي", "يتطلّب", "من الضروري"),
    7: ("من هذا القبيل", "نحو", "من ذلك", "مثلًا", "كما", "على سبيل المثال"),
    10: ("باستثناء", "ما عدا", "خلا"),
    11: ("إلّا أنّ", "غير أنّ", "بالعكس", "فإنّ", "بالمقابل"),
    12: ("يحتمل", "محتمل", "يمكن", "ممكن", "خال", "شكّ", "أعتقد"),
    13: ("بسبب", "بفضل", "نظرًا لـ"),
    14: ("لأنّ", "بحيث", "من حيث أنّ", "بما أنّ"),
    15: ("وعلى هذا", "ونتيجة لهذا", "ولهذا", "ومن هنا", "إذن", "لذلك", "بناءً عليه", "نخلص إلى"),
    16: ("من أجل أن", "كيما"),
    17: ("نونا التوكيد", "لام التوكيد", "ضمائر الفصل"),
    18: ("من الثابت أنّ", "من المتوقّع أنّ", "من المعروف أنّ", "من المقرّر أنّ"),
    21: ("من جهة أخرى", "تارة", "مرّة"),
    22: ("أيضًا", "كذلك", "بالإضافة إلى", "إلى جانب", "كما أنّ"),
    23: ("رغم", "برغم", "بالرغم من", "مع أنّ"),
    3: ("لا بدّ",),
}
"""تراكيبُ وألفاظٌ غيرُ مشكولةٍ في الجدول المُرسَل: تياراتُ شهادات لا أدوات؛ لا تُودَع خانات."""


def tier(p: Particle) -> str:
    """أعلى درجةٍ يبلغها البرهان في الأداة."""

    if p.amal:
        return "د١٦ العمل"
    if p.proclitic:
        return "د٨ الحدّ"
    return "د٤ الخانة"


def _check() -> None:
    for p in PARTICLES:
        if not licensed(p.cells):
            raise ValueError(f"UNLICENSED_PARTICLE:{p.name}")
        if p.proclitic and len(p.cells) != 1:
            raise ValueError(f"PROCLITIC_IS_ONE_CELL:{p.name}")
    if len({p.name for p in PARTICLES}) != len(PARTICLES):
        raise ValueError("DUPLICATE_PARTICLE")


_check()
