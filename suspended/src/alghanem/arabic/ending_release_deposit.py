"""إيداعُ «مولِّدات الخاتمة»: ما قِيس على بايتاتنا، وما منعته البوّابة.

وصلت إلى هذه الشجرة دفعةٌ من المستودع الشقيق (`hamil-hala-zaman-program`)
تدّعي أنّ خاتمةَ الكلمة تُولَّد بأربعة مولِّدات، وأنّ الحاكمَ فيها ما **قبلها**،
وتُقدِّم على ذلك ربحًا مقدارُه 0.52 بت. وهذا الملفّ **لا ينقل** شيئًا من ذلك
تصديقًا؛ بل يُعيد القياسَ من `corpora/quran-simple-enhanced.txt` وحدَها، عبر
البابِ المختوم `read_quran_corpus_bytes` الذي يفحص الطولَ والبصمةَ قبل أن
يُسلِّم بايتًا. فما وافق وُصِف موافقًا، وما خالف سُمِّي مخالفًا، وما مُنِع لم
يُنشَر أصلًا.

**أوّلًا: ثلاثةُ أجناسٍ لا جنسٌ واحد.** كانت الأرقامُ تُقرأ كلُّها «نتائج»،
وههنا تفترق::

    MEASURED_ON_THE_SEALED_BYTES  != REFUSED_BY_THE_TOKEN_MARKOV_GATE
    AFigureWithAScope             != AFigureWithoutOne
    NotMeasuredYet                != NotMeasurableOnThisPointing

فالمقيسُ يُعاد حسابُه من البايتات عند كلّ طلب، والممنوعُ **لا رقمَ له في هذا
الملفّ** ولو كنّا حسبناه في محادثة، والممتنعُ يُسمَّى امتناعَه لا نقصَه.

**وثانيًا: القانونان البنيويّان صمدا أشدَّ ممّا ادُّعي.** السكونان
المتجاوران داخل الكلمة: **صفرٌ مطلق**، لا استثناءَ مدٍّ ولا شدّة. والسكونُ
في أوّل الكلمة: **اثنان لا غير**، `لْيَقْطَعْ` و`لْيَقْضُوا`، وكلاهما بعد
«ثُمَّ». وفي الآيتين أنفسِهما تَرِدُ `فَلْيَمْدُدْ` و`وَلْيُوفُوا` موصولةً،
ولامُ الأمر موصولةٌ في 212 كلمةً من المدوّنة كلِّها. فالاثنان **عُرفُ تفريقٍ
في الرسم لا خرقٌ للقانون**، ولا يحتاج الحارسُ استثناءً
(`THE_TWO_INITIAL_SUKUNS_ARE_A_SPACING_HABIT_NOT_AN_EXCEPTION`).

**وثالثًا: الحاكمُ هو اللاحقُ لا السابق، والاسمُ «ق-تخلّص» لا «ق-وقف».**
على الصيغ المتناوبة: خاتمةٌ ساكنةٌ قبل ألفِ وصل = **صفرٌ من 4,534**، وخانةُ
الجدولِ هذه **غائبةٌ بالكلّيّة** لا نادرة. فالسكونُ لا يصمد أمام ألف الوصل.

**ورابعًا — وهو شرطُ الصفر:** الصفرُ صفرُ **ألفِ الوصل المجرّدة** وحدَها.
فإن وُسِّع الشرطُ إلى كلّ ألفٍ (أ إ آ) عاد إلى الخانة 1,232، وانهدم القانون.
فليست القاعدةُ «قبل الألف» بل «قبل الهمزة الواصلة»
(`THE_ZERO_BELONGS_TO_THE_CONNECTING_HAMZA_ALONE`).

**وخامسًا: مفتاحُ الصيغة يُحرِّك الرقمَ أكثرَ ممّا تُحرِّكه الظاهرة.** ثلاثةُ
مفاتيحَ تعطي ثلاثةَ أعداد: إسقاطُ كلّ العلامات 301 صيغةً و2,039 فتحة، وإبقاءُ
الشدّة 292 و1,038، وإبقاءُ كلّ العلامات الداخليّة 243 و799. فالرقمُ المنشور
هناك هو أعلى المفاتيح الثلاثة سخاءً. ولا يُنشَر ههنا رقمٌ مفردٌ بل السلّمُ
كلُّه (`A_FORM_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE`).

**وسادسًا: المفتاحُ السخيُّ يَدمِج متجانساتِ الرسم فيختلق تناوبًا.** من 301
صيغةً «متناوبة» تحت مفتاح الإسقاط، **155 صيغةً** أكثرُ من جذعٍ مشكولٍ واحد:
`أنزل` = أُنزِلَ وأَنزَلَ وأَنزِلْ، و`لم` = لَمْ ولَّمْ ولِمَ. فبعضُ «التناوب»
اتّفاقُ رسمٍ لا تصريف (`A_MERGED_HOMOGRAPH_MANUFACTURES_ITS_OWN_ALTERNATION`).

**وسابعًا: الوقفُ غيرُ قابلٍ للقياس على هذا الشكل.** خواتمُ الآيات: 95 ساكنةً
من 6,236 — والنصُّ مشكولٌ للوصل في عامّته. فدعوى «أصلُ الخاتمة السكون» مأخوذةٌ
من نحوٍ خارجَ المدوّنة لا مقيسةٌ فيها، ودَينُ «ق» يبقى مفتوحًا
(`PAUSE_IS_ABSENT_FROM_THIS_POINTING_SO_THE_Q_DEBT_STAYS_OPEN`).

**وثامنًا: ربحُ 0.52 بت لا يُنشَر ههنا، وبوّابةٌ لا رأيٌ هي المانع.** كلُّ
انتروبيا شرطيّةٍ على توكناتٍ متجاورة رقمٌ ماركوفيٌّ من الرتبة الأولى، وبوّابةُ
`markov_readiness_gate` واقفةٌ. فالخانةُ ههنا فارغةٌ عمدًا: لا رقمَ ولا مقارنة
(`A_SCRATCH_MEASUREMENT_IS_NOT_A_DEPOSIT`). وقد قِيس في محادثةٍ أنّ خلطًا
عشوائيًّا للخواتم يُهبِط الانتروبيا الشرطيّة وحدَه — وهذا سببٌ زائدٌ للامتناع،
لا هو السببَ الأوّل.

**وتاسعًا: إسنادٌ إلى موضعٍ خالٍ.** طُلِب ههنا فحصُ `FRACTAL-T3` و`G-SUK-1`
بوصفهما «تجميدَك»، ولا وجودَ لهذين المعرِّفين في هذه الشجرة البتّة. فهما —
كالختم `8b387e8` قبلهما — من المستودع الآخر، وذلك حسمُ سؤالٍ لا عجزٌ عنه
(`AN_IDENTIFIER_ABSENT_FROM_THIS_TREE_IS_NOT_A_FREEZE_OF_OURS`).

**وعاشرًا: إذنُ المالك ليس قياسًا.** أُودِع هذا الملفّ بتفويضٍ صريحٍ من مالك
المستودع. والتفويضُ يرفع المنعَ عن **الإيداع**، ولا يُصيِّر رقمًا مقيسًا ولا
يفتح بوّابةً (`AN_OWNER_AUTHORIZATION_LICENSES_THE_DEPOSIT_NOT_THE_FIGURE`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادة، ولا استيرادَ من `kernel/` ولا
من `program/`، ولا بوّابةَ تقرأ هذا الإيداع، ولا تزحزح فيه بوّابةَ ماركوف.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, fields
from enum import Enum
from functools import cache
from typing import Final

from .markov_readiness_gate import ChainReading, token_markov_standing
from .quran_corpus_word_total import read_quran_corpus_bytes

__all__ = [
    "AN_IDENTIFIER_ABSENT_FROM_THIS_TREE_IS_NOT_A_FREEZE_OF_OURS",
    "AN_OWNER_AUTHORIZATION_LICENSES_THE_DEPOSIT_NOT_THE_FIGURE",
    "A_FORM_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE",
    "A_MERGED_HOMOGRAPH_MANUFACTURES_ITS_OWN_ALTERNATION",
    "A_SCRATCH_MEASUREMENT_IS_NOT_A_DEPOSIT",
    "ENDING_RELEASE_NAMED_RESIDUALS",
    "PAUSE_IS_ABSENT_FROM_THIS_POINTING_SO_THE_Q_DEBT_STAYS_OPEN",
    "THE_ABSENT_IDENTIFIERS",
    "THE_ENDING_FIGURES",
    "THE_TWO_INITIAL_SUKUNS_ARE_A_SPACING_HABIT_NOT_AN_EXCEPTION",
    "THE_ZERO_BELONGS_TO_THE_CONNECTING_HAMZA_ALONE",
    "CorpusFigures",
    "EndingClass",
    "EndingReleaseError",
    "FigureGenus",
    "FigureStanding",
    "FormKey",
    "KeyLadderRow",
    "TranscribedFigure",
    "contradicting_figures",
    "identifier_is_present_in_this_tree",
    "measure_the_sealed_corpus",
    "the_corpus_gate_is_untouched",
    "the_key_ladder",
]


class EndingReleaseError(RuntimeError):
    """رفضٌ في هذه الوحدة: رقمٌ بلا مقياس، أو حكمٌ مكتوبٌ بلا حساب."""


# ---------------------------------------------------------------------------
# حروفُ العلامات، وأدواتُ القراءة
# ---------------------------------------------------------------------------


THE_ARABIC_COMBINING_MARKS: Final[frozenset[str]] = frozenset(
    chr(codepoint)
    for codepoint in range(0x0600, 0x0700)
    if unicodedata.category(chr(codepoint)) == "Mn"
)
"""علاماتُ الكتلة العربيّة غيرُ المتباعدة؛ تُشتقّ من قاعدة يونيكود لا تُسرَد."""

THE_SUKUN: Final[str] = "\u0652"
THE_SHADDA: Final[str] = "\u0651"
THE_CONNECTING_ALIF: Final[str] = "\u0627"
THE_SELECTION_TAG: Final[str] = "<sel>"

THE_SHORT_VOWELS: Final[dict[str, str]] = {
    "\u064e": "a",
    "\u064f": "u",
    "\u0650": "i",
}
THE_TANWIN_MARKS: Final[dict[str, str]] = {
    "\u064b": "aN",
    "\u064c": "uN",
    "\u064d": "iN",
}
THE_MADD_CARRIERS: Final[frozenset[str]] = frozenset("اوىيٰآ")

_THE_READABLE_ENDINGS: Final[frozenset[str]] = frozenset({"a", "u", "i", "S"})


class EndingClass(Enum):
    """قسمةُ خاتمةِ الكلمة خمسًا بالرسم وحدَه، لا بالإعراب."""

    HARAKA = "حركةٌ مكتوبة"
    MADD_CARRIER = "حاملُ مدٍّ بلا علامة"
    WRITTEN_SUKUN = "سكونٌ مكتوب"
    TANWIN = "تنوين"
    BARE_CONSONANT = "صامتٌ بلا علامة"


class FormKey(Enum):
    """مفاتيحُ تجميع الصيغة الثلاثة، مرتّبةً من الأسخى إلى الأضيق."""

    MARKS_DROPPED = "إسقاطُ كلّ العلامات"
    SHADDA_KEPT = "إبقاءُ الشدّة وحدَها"
    ALL_MARKS_KEPT = "إبقاءُ كلّ العلامات الداخليّة"


def _units(word: str) -> list[tuple[str, frozenset[str]]]:
    """أفكّ الكلمةَ إلى حروفٍ، كلُّ حرفٍ ومعه علاماتُه."""

    letters: list[str] = []
    marks: list[set[str]] = []
    for character in word:
        if character in THE_ARABIC_COMBINING_MARKS:
            if letters:
                marks[-1].add(character)
            continue
        letters.append(character)
        marks.append(set())
    return [(letter, frozenset(mark)) for letter, mark in zip(letters, marks)]


def _split_ending(word: str) -> tuple[str, str | None]:
    """أعزل علامةَ الخاتمة عن جذعها؛ وأردُّ `None` إن لم تُكتَب علامة."""

    index = len(word) - 1
    while index >= 0 and word[index] in THE_ARABIC_COMBINING_MARKS:
        mark = word[index]
        stem = word[:index] + word[index + 1 :]
        if mark == THE_SUKUN:
            return stem, "S"
        if mark in THE_SHORT_VOWELS:
            return stem, THE_SHORT_VOWELS[mark]
        if mark in THE_TANWIN_MARKS:
            return stem, THE_TANWIN_MARKS[mark]
        index -= 1
    return word, None


def _bare(word: str) -> str:
    """أُجرِّد الكلمةَ من كلّ علامة."""

    return "".join(
        character for character in word if character not in THE_ARABIC_COMBINING_MARKS
    )


def _form_key(stem: str, key: FormKey) -> str:
    """أُطبِّق أحدَ المفاتيح الثلاثة على جذعٍ منزوعِ الخاتمة."""

    if key is FormKey.ALL_MARKS_KEPT:
        return stem
    if key is FormKey.SHADDA_KEPT:
        return "".join(
            character
            for character in stem
            if character not in THE_ARABIC_COMBINING_MARKS or character == THE_SHADDA
        )
    return _bare(stem)


@cache
def _ayahs() -> tuple[tuple[str, ...], ...]:
    """أقرأ المدوّنةَ المختومة آيةً آية، مُسقِطًا وسمَ الاختيار."""

    text = read_quran_corpus_bytes().decode("utf-8")
    ayahs = []
    for line in text.splitlines():
        tokens = tuple(token for token in line.split() if token != THE_SELECTION_TAG)
        if tokens:
            ayahs.append(tokens)
    return tuple(ayahs)


# ---------------------------------------------------------------------------
# القياسُ نفسُه
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CorpusFigures:
    """كلُّ ما يُعاد حسابُه من البايتات المختومة، عددًا صحيحًا لا نسبة."""

    ayah_count: int
    token_count: int
    word_initial_written_sukun: int
    adjacent_written_sukun_inside_a_word: int
    joined_lam_of_command_tokens: int
    ayah_final_written_sukun: int
    ending_haraka: int
    ending_madd_carrier: int
    ending_written_sukun: int
    ending_tanwin: int
    ending_bare_consonant: int
    forms_marks_dropped: int
    fatha_marks_dropped: int
    forms_shadda_kept: int
    fatha_shadda_kept: int
    forms_all_marks_kept: int
    fatha_all_marks_kept: int
    damma_all_marks_kept: int
    kasra_all_marks_kept: int
    fatha_on_the_min_forms: int
    multi_stem_forms_under_the_dropping_key: int
    sukun_before_the_connecting_alif: int
    sukun_before_anything_else: int
    voweled_before_the_connecting_alif: int
    voweled_before_anything_else: int
    sukun_before_any_alif_shape: int
    bare_inna_readable_next: int
    bare_inna_next_is_fatha: int
    attached_inna_readable_next: int
    attached_inna_next_is_fatha: int

    def __post_init__(self) -> None:
        if self.token_count <= 0 or self.ayah_count <= 0:
            raise EndingReleaseError("the sealed corpus measured empty")
        if self.ending_total != self.token_count:
            raise EndingReleaseError("the five ending classes do not partition")

    @property
    def ending_total(self) -> int:
        """مجموعُ الأصناف الخمسة؛ ويجب أن يساوي عددَ التوكنات حتمًا."""

        return (
            self.ending_haraka
            + self.ending_madd_carrier
            + self.ending_written_sukun
            + self.ending_tanwin
            + self.ending_bare_consonant
        )

    @property
    def dominant_ending_share(self) -> float:
        """قراءةُ الهيمنة التي لا يُصدَر رقمُ توكنٍ ههنا بدونها."""

        return (
            max(
                self.ending_haraka,
                self.ending_madd_carrier,
                self.ending_written_sukun,
                self.ending_tanwin,
                self.ending_bare_consonant,
            )
            / self.token_count
        )

    @property
    def the_release_zero_survives_only_the_connecting_alif(self) -> bool:
        """أصفرُ الخانةِ خاصٌّ بألفِ الوصل، ويزول باتّساع الشرط؟"""

        return (
            self.sukun_before_the_connecting_alif == 0
            and self.sukun_before_any_alif_shape > 0
        )


def _measure_structure(
    ayahs: tuple[tuple[str, ...], ...],
) -> tuple[int, int, int, int]:
    """أعُدّ السكونَ الأوّلَ والمتجاور، ولامَ الأمر الموصولة، وسكونَ الفاصلة."""

    initial = 0
    adjacent = 0
    joined_lam = 0
    ayah_final = 0
    for ayah in ayahs:
        for token in ayah:
            units = _units(token)
            if not units:
                continue
            if THE_SUKUN in units[0][1]:
                initial += 1
            for position in range(len(units) - 1):
                if (
                    THE_SUKUN in units[position][1]
                    and THE_SUKUN in units[position + 1][1]
                ):
                    adjacent += 1
            for position in range(1, len(units) - 1):
                if (
                    units[position][0] == "ل"
                    and THE_SUKUN in units[position][1]
                    and units[position + 1][0] == "ي"
                ):
                    joined_lam += 1
                    break
        if _split_ending(ayah[-1])[1] == "S":
            ayah_final += 1
    return initial, adjacent, joined_lam, ayah_final


def _measure_ending_classes(
    ayahs: tuple[tuple[str, ...], ...],
) -> dict[EndingClass, int]:
    """أقسِم خواتمَ التوكنات خمسًا؛ والقسمةُ مُستغرِقةٌ بالبناء."""

    counts = dict.fromkeys(EndingClass, 0)
    for ayah in ayahs:
        for token in ayah:
            units = _units(token)
            if not units:
                continue
            letter, marks = units[-1]
            if marks & frozenset(THE_TANWIN_MARKS):
                counts[EndingClass.TANWIN] += 1
            elif THE_SUKUN in marks:
                counts[EndingClass.WRITTEN_SUKUN] += 1
            elif marks & frozenset(THE_SHORT_VOWELS):
                counts[EndingClass.HARAKA] += 1
            elif letter in THE_MADD_CARRIERS:
                counts[EndingClass.MADD_CARRIER] += 1
            else:
                counts[EndingClass.BARE_CONSONANT] += 1
    return counts


def _alternating_forms(
    ayahs: tuple[tuple[str, ...], ...], key: FormKey
) -> dict[str, dict[str, int]]:
    """أجمع الصيغَ التي تحمل سكونًا وحركةً معًا، تحت مفتاحٍ بعينه."""

    table: dict[str, dict[str, int]] = {}
    for ayah in ayahs:
        for token in ayah:
            stem, ending = _split_ending(token)
            if ending is None:
                continue
            row = table.setdefault(_form_key(stem, key), {})
            row[ending] = row.get(ending, 0) + 1
    return {
        form: row
        for form, row in table.items()
        if row.get("S", 0) > 0 and len(_THE_READABLE_ENDINGS.intersection(row)) >= 2
    }


def _is_inna(token: str) -> bool:
    """أهي إنّ أو أنّ — بشدّةٍ على النون — وحدَها أو بلاحقة؟"""

    units = _units(token)
    bare = _bare(token)
    if len(units) < 2 or bare[:1] not in {"إ", "أ"} or bare[1:2] != "ن":
        return False
    return THE_SHADDA in units[1][1]


@cache
def measure_the_sealed_corpus() -> CorpusFigures:
    """أُعيد كلَّ رقمٍ في هذا الإيداع من البايتات المختومة، لا من نقل.

    والقراءةُ عبر `read_quran_corpus_bytes` وحدَه: يفحص الطولَ والبصمةَ قبل
    أن يُسلِّم بايتًا، فلا يُقرأ المسارُ مباشرةً ههنا البتّة.
    """

    ayahs = _ayahs()
    initial, adjacent, joined_lam, ayah_final = _measure_structure(ayahs)
    classes = _measure_ending_classes(ayahs)

    ladder: dict[FormKey, dict[str, dict[str, int]]] = {
        key: _alternating_forms(ayahs, key) for key in FormKey
    }
    full = ladder[FormKey.ALL_MARKS_KEPT]
    dropped = ladder[FormKey.MARKS_DROPPED]

    stems_per_dropped_form: dict[str, set[str]] = {}
    for ayah in ayahs:
        for token in ayah:
            stem, ending = _split_ending(token)
            if ending is None:
                continue
            stems_per_dropped_form.setdefault(_bare(stem), set()).add(stem)

    release = dict.fromkeys(
        (
            ("S", "wasl"),
            ("S", "other"),
            ("V", "wasl"),
            ("V", "other"),
        ),
        0,
    )
    sukun_before_any_alif = 0
    bare_inna: dict[str, int] = {}
    attached_inna: dict[str, int] = {}
    for ayah in ayahs:
        for position, token in enumerate(ayah[:-1]):
            following = _bare(ayah[position + 1])[:1]
            stem, ending = _split_ending(token)
            if _is_inna(token):
                next_ending = _split_ending(ayah[position + 1])[1]
                if next_ending is not None:
                    target = bare_inna if len(_bare(token)) == 2 else attached_inna
                    target[next_ending] = target.get(next_ending, 0) + 1
            if ending is None or stem not in full:
                continue
            side = "S" if ending == "S" else "V"
            place = "wasl" if following == THE_CONNECTING_ALIF else "other"
            release[(side, place)] += 1
            if side == "S" and following in {"ا", "أ", "إ", "آ"}:
                sukun_before_any_alif += 1

    def _column(forms: dict[str, dict[str, int]], ending: str) -> int:
        return sum(row.get(ending, 0) for row in forms.values())

    return CorpusFigures(
        ayah_count=len(ayahs),
        token_count=sum(len(ayah) for ayah in ayahs),
        word_initial_written_sukun=initial,
        adjacent_written_sukun_inside_a_word=adjacent,
        joined_lam_of_command_tokens=joined_lam,
        ayah_final_written_sukun=ayah_final,
        ending_haraka=classes[EndingClass.HARAKA],
        ending_madd_carrier=classes[EndingClass.MADD_CARRIER],
        ending_written_sukun=classes[EndingClass.WRITTEN_SUKUN],
        ending_tanwin=classes[EndingClass.TANWIN],
        ending_bare_consonant=classes[EndingClass.BARE_CONSONANT],
        forms_marks_dropped=len(dropped),
        fatha_marks_dropped=_column(dropped, "a"),
        forms_shadda_kept=len(ladder[FormKey.SHADDA_KEPT]),
        fatha_shadda_kept=_column(ladder[FormKey.SHADDA_KEPT], "a"),
        forms_all_marks_kept=len(full),
        fatha_all_marks_kept=_column(full, "a"),
        damma_all_marks_kept=_column(full, "u"),
        kasra_all_marks_kept=_column(full, "i"),
        fatha_on_the_min_forms=sum(
            row.get("a", 0) for form, row in full.items() if _bare(form) == "من"
        ),
        multi_stem_forms_under_the_dropping_key=sum(
            1 for form in dropped if len(stems_per_dropped_form.get(form, set())) > 1
        ),
        sukun_before_the_connecting_alif=release[("S", "wasl")],
        sukun_before_anything_else=release[("S", "other")],
        voweled_before_the_connecting_alif=release[("V", "wasl")],
        voweled_before_anything_else=release[("V", "other")],
        sukun_before_any_alif_shape=sukun_before_any_alif,
        bare_inna_readable_next=sum(bare_inna.values()),
        bare_inna_next_is_fatha=bare_inna.get("a", 0),
        attached_inna_readable_next=sum(attached_inna.values()),
        attached_inna_next_is_fatha=attached_inna.get("a", 0),
    )


# ---------------------------------------------------------------------------
# الأرقامُ المنقولة، وأحكامُها المشتقّة
# ---------------------------------------------------------------------------


class FigureGenus(Enum):
    """أجناسُ الأرقام الثلاثة؛ ولكلّ جنسٍ ما يجوز فيه."""

    MEASURED_ON_THE_SEALED_BYTES = "مقيسٌ على بايتاتنا المختومة"
    REFUSED_BY_THE_TOKEN_MARKOV_GATE = "ممنوعٌ ببوّابة ماركوف"
    UNMEASURABLE_ON_THIS_POINTING = "ممتنعُ القياس على هذا الشكل"


class FigureStanding(Enum):
    """حكمُ الرقم؛ مشتقٌّ من طرفَيه دائمًا، ولا يُكتَب في حقل."""

    AGREES = "وافق المقيسَ"
    CONTRADICTS = "خالف المقيسَ"
    NOT_ISSUED_HERE = "لا رقمَ له في هذه الشجرة"


@dataclass(frozen=True)
class TranscribedFigure:
    """رقمٌ نُقِل إلينا، ومعه البابُ الذي يُعاد منه — أو سببُ امتناعه."""

    name: str
    genus: FigureGenus
    attribute: str | None
    transcribed: int | None

    def __post_init__(self) -> None:
        measured_genus = self.genus is FigureGenus.MEASURED_ON_THE_SEALED_BYTES
        if measured_genus != (self.attribute is not None):
            raise EndingReleaseError("a measured figure must name its attribute")
        if not measured_genus and self.transcribed is not None:
            raise EndingReleaseError("an unissued figure carries a number")
        if self.attribute is not None and not any(
            field.name == self.attribute for field in fields(CorpusFigures)
        ):
            raise EndingReleaseError("a figure names no attribute we measure")

    @property
    def measured(self) -> int | None:
        """القيمةُ كما تُقاس الآن من البايتات، لا كما نُقِلت."""

        if self.attribute is None:
            return None
        value = getattr(measure_the_sealed_corpus(), self.attribute)
        assert isinstance(value, int)
        return value

    @property
    def standing(self) -> FigureStanding:
        """الحكمُ يتبع الطرفَين حتمًا؛ فلا حقلَ حكمٍ في هذا الملفّ."""

        measured = self.measured
        if measured is None or self.transcribed is None:
            return FigureStanding.NOT_ISSUED_HERE
        if measured == self.transcribed:
            return FigureStanding.AGREES
        return FigureStanding.CONTRADICTS


THE_ENDING_FIGURES: Final[tuple[TranscribedFigure, ...]] = (
    TranscribedFigure(
        name="السكونُ في أوّل الكلمة",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="word_initial_written_sukun",
        transcribed=2,
    ),
    TranscribedFigure(
        name="سكونان متجاوران داخل الكلمة",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="adjacent_written_sukun_inside_a_word",
        transcribed=0,
    ),
    TranscribedFigure(
        name="لامُ الأمر موصولةً",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="joined_lam_of_command_tokens",
        transcribed=212,
    ),
    TranscribedFigure(
        name="فواصلُ الآي الساكنة",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="ayah_final_written_sukun",
        transcribed=95,
    ),
    TranscribedFigure(
        name="ساكنٌ قبل ألفِ الوصل",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="sukun_before_the_connecting_alif",
        transcribed=0,
    ),
    TranscribedFigure(
        name="ساكنٌ قبل سواها",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="sukun_before_anything_else",
        transcribed=4_534,
    ),
    TranscribedFigure(
        name="متحرّكٌ قبل ألفِ الوصل",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="voweled_before_the_connecting_alif",
        transcribed=1_643,
    ),
    TranscribedFigure(
        name="متحرّكٌ قبل سواها",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="voweled_before_anything_else",
        transcribed=170,
    ),
    TranscribedFigure(
        name="الصيغُ المتناوبة بإسقاط العلامات",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="forms_marks_dropped",
        transcribed=301,
    ),
    TranscribedFigure(
        name="الفتحُ بإسقاط العلامات",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="fatha_marks_dropped",
        transcribed=2_039,
    ),
    TranscribedFigure(
        name="الفتحُ على صيغ «من» وحدَها",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="fatha_on_the_min_forms",
        transcribed=693,
    ),
    TranscribedFigure(
        name="الضمُّ بالمفتاح الكامل",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="damma_all_marks_kept",
        transcribed=555,
    ),
    TranscribedFigure(
        name="الكسرُ بالمفتاح الكامل",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="kasra_all_marks_kept",
        transcribed=382,
    ),
    TranscribedFigure(
        name="خاتمةُ حاملِ المدّ بلا علامة",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="ending_madd_carrier",
        transcribed=19_205,
    ),
    TranscribedFigure(
        name="خاتمةُ التنوين",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="ending_tanwin",
        transcribed=8_894,
    ),
    TranscribedFigure(
        name="خاتمةُ السكون المكتوب",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="ending_written_sukun",
        transcribed=8_368,
    ),
    TranscribedFigure(
        name="خاتمةُ الصامت بلا علامة",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="ending_bare_consonant",
        transcribed=4_767,
    ),
    TranscribedFigure(
        name="الفتحُ بعد إنّ المجرّدة",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="bare_inna_next_is_fatha",
        transcribed=516,
    ),
    TranscribedFigure(
        name="ما بعد إنّ المجرّدة ممّا يُقرأ",
        genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
        attribute="bare_inna_readable_next",
        transcribed=571,
    ),
    TranscribedFigure(
        name="ربحُ الحاكم السابق بالبتّات",
        genus=FigureGenus.REFUSED_BY_THE_TOKEN_MARKOV_GATE,
        attribute=None,
        transcribed=None,
    ),
    TranscribedFigure(
        name="فضلُ السابق على اللاحق بالبتّات",
        genus=FigureGenus.REFUSED_BY_THE_TOKEN_MARKOV_GATE,
        attribute=None,
        transcribed=None,
    ),
    TranscribedFigure(
        name="أصلُ الخاتمة في الوقف",
        genus=FigureGenus.UNMEASURABLE_ON_THIS_POINTING,
        attribute=None,
        transcribed=None,
    ),
    TranscribedFigure(
        name="الصورةُ العميقة قبل الإعلال",
        genus=FigureGenus.UNMEASURABLE_ON_THIS_POINTING,
        attribute=None,
        transcribed=None,
    ),
)


def contradicting_figures() -> tuple[TranscribedFigure, ...]:
    """الأرقامُ المنقولة التي خالفها القياسُ ههنا."""

    return tuple(
        figure
        for figure in THE_ENDING_FIGURES
        if figure.standing is FigureStanding.CONTRADICTS
    )


@dataclass(frozen=True)
class KeyLadderRow:
    """درجةٌ من سلّم المفاتيح: كم صيغةً تناوبت، وكم فتحةً حملت."""

    key: FormKey
    alternating_forms: int
    fatha_releases: int

    def __post_init__(self) -> None:
        if self.alternating_forms <= 0 or self.fatha_releases <= 0:
            raise EndingReleaseError("a ladder rung measured empty")


def the_key_ladder() -> tuple[KeyLadderRow, ...]:
    """السلّمُ كاملًا، لأنّ نشرَ درجةٍ واحدةٍ منه يُخفي أنّ المفتاح اختيار."""

    figures = measure_the_sealed_corpus()
    return (
        KeyLadderRow(
            key=FormKey.MARKS_DROPPED,
            alternating_forms=figures.forms_marks_dropped,
            fatha_releases=figures.fatha_marks_dropped,
        ),
        KeyLadderRow(
            key=FormKey.SHADDA_KEPT,
            alternating_forms=figures.forms_shadda_kept,
            fatha_releases=figures.fatha_shadda_kept,
        ),
        KeyLadderRow(
            key=FormKey.ALL_MARKS_KEPT,
            alternating_forms=figures.forms_all_marks_kept,
            fatha_releases=figures.fatha_all_marks_kept,
        ),
    )


# ---------------------------------------------------------------------------
# الإسنادُ إلى موضعٍ خالٍ
# ---------------------------------------------------------------------------


THE_ABSENT_IDENTIFIERS: Final[tuple[str, ...]] = ("FRACTAL-T3", "G-SUK-1")
"""معرِّفان طُلِب فحصُهما بوصفهما تجميدًا لنا، ولا وجودَ لهما في هذه الشجرة."""


def identifier_is_present_in_this_tree(identifier: str) -> bool:
    """أموجودٌ هذا المعرِّفُ في شيفرة هذه الحزمة؟ يُفحَص بالقراءة لا بالظنّ.

    ويُستثنى هذا الملفُّ نفسُه باسمه: فهو يسرد المعرِّفَين ليُخبر عن غيابهما،
    فلو قُرئ في نفسِه لأثبت وجودَهما بذكرِه إيّاهما — وذلك دورٌ لا فحص.
    """

    from pathlib import Path

    here = Path(__file__).resolve()
    root = here.parent.parent
    for path in sorted(root.rglob("*.py")):
        if path.resolve() == here:
            continue
        if identifier in path.read_text(encoding="utf-8"):
            return True
    return False


# ---------------------------------------------------------------------------
# البوّابةُ كما قُرئت، والقيودُ المسمّاة
# ---------------------------------------------------------------------------


_THE_GATE_AS_READ_AT_IMPORT: Final[ChainReading] = token_markov_standing()
"""قراءةُ بوّابة ماركوف عند الاستيراد، ليكون القياسُ إلى ملحوظٍ لا إلى رمز."""


def the_corpus_gate_is_untouched() -> bool:
    """أزحزح شيءٌ من هذا الإيداع بوّابةَ ماركوف عمّا كانت عليه؟"""

    return token_markov_standing() == _THE_GATE_AS_READ_AT_IMPORT


THE_TWO_INITIAL_SUKUNS_ARE_A_SPACING_HABIT_NOT_AN_EXCEPTION: Final[str] = (
    "THE_TWO_INITIAL_SUKUNS_ARE_A_SPACING_HABIT_NOT_AN_EXCEPTION: "
    "الكلمتان الوحيدتان المبتدئتان بساكنٍ لامُ أمرٍ فُصِلت في الرسم بعد «ثُمَّ»، "
    "ونظيرتُها موصولةٌ في الآية نفسِها وفي مئاتٍ سواها. فالقانونُ لا يُستثنى "
    "منه شيءٌ، والحارسُ لا يحتاج بابًا خلفيًّا؛ وإصلاحُ الفصل في الرسم غيرُ "
    "إصلاحِ خرقٍ في البنية."
)

THE_ZERO_BELONGS_TO_THE_CONNECTING_HAMZA_ALONE: Final[str] = (
    "THE_ZERO_BELONGS_TO_THE_CONNECTING_HAMZA_ALONE: "
    "خانةُ «ساكنٌ قبل ألفِ الوصل» غائبةٌ بالكلّيّة، فإن وُسِّع الشرطُ إلى كلّ "
    "صورة ألفٍ عادت الخانةُ ممتلئة. فالصفرُ شهادةٌ على الهمزة الواصلة وحدَها، "
    "وأيُّ نقلٍ للقانون إلى «الألف» مطلقًا يُسقِطه."
)

A_FORM_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE: Final[str] = (
    "A_FORM_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE: "
    "عددُ الصيغ المتناوبة وعددُ الفتحات يتبدّلان بتبدّل مفتاح التجميع وحدَه، "
    "من غير أن يتبدّل في المدوّنة حرفٌ واحد. فلا يُنشَر رقمٌ منها مفردًا، بل "
    "بدرجاته الثلاث، وإلّا صار اختيارُ المفتاح نتيجةً مضمرة."
)

A_MERGED_HOMOGRAPH_MANUFACTURES_ITS_OWN_ALTERNATION: Final[str] = (
    "A_MERGED_HOMOGRAPH_MANUFACTURES_ITS_OWN_ALTERNATION: "
    "المفتاحُ الذي يُسقِط العلامات يجمع جذوعًا مشكولةً مختلفةً تحت رسمٍ واحد، "
    "فيظهر «تناوبٌ» هو اتّفاقُ رسمٍ لا تصريف. وإبقاءُ الشدّة وحدَها لا يكفي: "
    "يبقى أكثرُ من نصف الصيغ مُدمَجًا."
)

PAUSE_IS_ABSENT_FROM_THIS_POINTING_SO_THE_Q_DEBT_STAYS_OPEN: Final[str] = (
    "PAUSE_IS_ABSENT_FROM_THIS_POINTING_SO_THE_Q_DEBT_STAYS_OPEN: "
    "المدوّنةُ مشكولةٌ للوصل في عامّتها، وفواصلُ الآي الساكنةُ قلّةٌ منها. "
    "فالوقفُ لا يُقاس ههنا البتّة، ودعوى «أصلُ الخاتمة السكون» مأخوذةٌ من "
    "نحوٍ خارجَ المدوّنة؛ ولذلك سُمّي القانونُ «ق-تخلّص» لا «ق-وقف»."
)

A_SCRATCH_MEASUREMENT_IS_NOT_A_DEPOSIT: Final[str] = (
    "A_SCRATCH_MEASUREMENT_IS_NOT_A_DEPOSIT: "
    "الانتروبيا الشرطيّةُ على توكنَين متجاورَين رقمٌ ماركوفيٌّ من الرتبة "
    "الأولى، وبوّابةُ الاستعداد واقفة. فما حُسِب في محادثةٍ لا يصير إيداعًا "
    "بحسابه، وخانةُ الربح ههنا فارغةٌ عمدًا لا نسيانًا."
)

AN_IDENTIFIER_ABSENT_FROM_THIS_TREE_IS_NOT_A_FREEZE_OF_OURS: Final[str] = (
    "AN_IDENTIFIER_ABSENT_FROM_THIS_TREE_IS_NOT_A_FREEZE_OF_OURS: "
    "طُلِب فحصُ معرِّفَين بوصفهما تجميدًا لنا، ولا وجودَ لهما في شيفرة هذه "
    "الحزمة. فالإسنادُ إلى موضعٍ خالٍ يُحسَم نفيًا، ولا يُقرأ عجزًا عن الفحص."
)

AN_OWNER_AUTHORIZATION_LICENSES_THE_DEPOSIT_NOT_THE_FIGURE: Final[str] = (
    "AN_OWNER_AUTHORIZATION_LICENSES_THE_DEPOSIT_NOT_THE_FIGURE: "
    "أُودِع هذا الملفّ بتفويضٍ صريحٍ من مالك المستودع. والتفويضُ يرفع المنعَ "
    "عن الإيداع وحدَه؛ فلا يُصيِّر منقولًا مقيسًا، ولا يفتح بوّابةً موقوفة، "
    "ولا يُبدِّل حكمًا من أحكام هذا الملفّ."
)

ENDING_RELEASE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "initial_sukun": THE_TWO_INITIAL_SUKUNS_ARE_A_SPACING_HABIT_NOT_AN_EXCEPTION,
    "connecting_hamza": THE_ZERO_BELONGS_TO_THE_CONNECTING_HAMZA_ALONE,
    "form_key": A_FORM_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE,
    "homograph": A_MERGED_HOMOGRAPH_MANUFACTURES_ITS_OWN_ALTERNATION,
    "pause": PAUSE_IS_ABSENT_FROM_THIS_POINTING_SO_THE_Q_DEBT_STAYS_OPEN,
    "markov_gate": A_SCRATCH_MEASUREMENT_IS_NOT_A_DEPOSIT,
    "absent_identifier": AN_IDENTIFIER_ABSENT_FROM_THIS_TREE_IS_NOT_A_FREEZE_OF_OURS,
    "owner_authorization": AN_OWNER_AUTHORIZATION_LICENSES_THE_DEPOSIT_NOT_THE_FIGURE,
}
"""القيودُ الثمانيةُ مسمّاةً؛ وكلُّ قيدٍ يُصدِّر اسمَه في نصّه."""


# ---------------------------------------------------------------------------
# مبرهناتُ الاستيراد: تصميمٌ لا واقعةٌ مؤرَّخة
# ---------------------------------------------------------------------------


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "standing",
    "verdict",
    "conclusion",
)


def _verify_no_standing_is_ever_a_field() -> None:
    """مبرهنة: لا حقلَ حكمٍ ههنا؛ فالحكمُ يتبع طرفَيه حتمًا."""

    for declared in (TranscribedFigure, CorpusFigures, KeyLadderRow):
        for field in fields(declared):
            if any(token in field.name for token in _FORBIDDEN_FIELD_TOKENS):
                raise EndingReleaseError("a deposit type carries a verdict field")


def _verify_every_residual_names_itself() -> None:
    """مبرهنة: كلُّ قيدٍ يبدأ باسمه، فلا يُقتطَع نصُّه عن معرِّفه."""

    for residual in ENDING_RELEASE_NAMED_RESIDUALS.values():
        name, separator, _rest = residual.partition(":")
        if not separator or name != name.upper() or not name.strip():
            raise EndingReleaseError("a residual does not carry its own name")


def _verify_no_unissued_figure_carries_a_number() -> None:
    """مبرهنة: ما مُنِع أو امتنع لا رقمَ له — وهذه ثابتةٌ لا واقعة."""

    for figure in THE_ENDING_FIGURES:
        if figure.genus is FigureGenus.MEASURED_ON_THE_SEALED_BYTES:
            continue
        if figure.transcribed is not None or figure.attribute is not None:
            raise EndingReleaseError("an unissued figure was given a number")


def _verify_the_deposit_imports_no_authority() -> None:
    """مبرهنة: هذا الملفّ لا يستورد من النواة ولا من البرنامج."""

    from pathlib import Path

    source = Path(__file__).read_text(encoding="utf-8")
    for forbidden in ("alghanem.kernel", "alghanem.program", "from ..kernel"):
        if f"import {forbidden}" in source or f"{forbidden} import" in source:
            raise EndingReleaseError("the deposit imports an authority module")


_verify_no_standing_is_ever_a_field()
_verify_every_residual_names_itself()
_verify_no_unissued_figure_carries_a_number()
_verify_the_deposit_imports_no_authority()

if len(ENDING_RELEASE_NAMED_RESIDUALS) != 8:  # pragma: no cover - guard
    raise EndingReleaseError("the named residuals were silently thinned")
