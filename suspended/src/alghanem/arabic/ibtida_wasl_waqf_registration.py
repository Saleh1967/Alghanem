"""قوانينُ الابتداء والوصل والوقف: تسجيلُ نصِّها، وقراءةُ ما يُقرأ منها هنا.

وصلت هذه الشجرةَ ثلاثةُ قوانينَ مصوغةٍ صياغةً رمزية، ومعها اشتقاقٌ منطقيٌّ
لمنع التقاء الساكنين، ومعهما **رقمٌ** (٩٩٫٩٩٧٤٪) قيل إنه مقيسٌ على القرآن،
ثمّ **استثناءٌ** سُمّي بعد الرقم (لامُ الأمر الساكنة) قيل إنّ إعمالَه يرفع
الرقمَ إلى ١٠٠٫٠٠٠٠٪، ثمّ **تجميدٌ** بمعرِّفٍ مكتوب. وأجناسُ هذه الأربعة
مختلفة، فلا تُعامَل معاملةً واحدة::

    FormalStatement   != TranscribedLaw
    QuotedFigure      != MeasuredFigure
    ExclusionAfterTheNumber != Preregistration
    WrittenFreezeId   != Freeze

**فالقوانينُ تُسجَّل بنصّها بمنزلتها**: لم يُسمَّ لها كتابٌ ولا طبعةٌ ولا موضع،
فمنزلتُها الدنيا `مُورَدة_بلا_مصدرٍ_مُسمًّى`، والمنزلتان الأعلى عضوان بلا مدخل
حتى يصل مصدرٌ (`THE_THREE_LAWS_ARE_SUPPLIED_WITHOUT_A_NAMED_SOURCE`).

**والرقمُ لا يُقبَل ولا يُحذَف**: لا مدوَّنةَ قرآنيةٌ مُودَعةٌ في هذه الشجرة
تُعيد اشتقاقَه، فسُجِّل بجنس مصدره وقيده في `REPORTED_UNVERIFIED_FIGURES` من
`alghanem.program.direct_certainty`، على قاعدة `RECORDING_IS_NOT_ENDORSING`.

**والمقروءُ هنا قراءةٌ واحدةٌ صغيرةٌ تُعاد الآن**: قانونُ الابتداء وحدَه، على
النصّ الوحيد المُودَع بحروفه (الفاتحة)، بمعيارٍ **سطحيٍّ مُصرَّحٍ به**: حالةُ
أوّلِ حاملٍ في كلّ كلمةٍ مكتوبة. وأخرجت هذه القراءةُ الحدَّ الذي يُبطل الرقمَ
الواصلَ أصلًا قبل أن يُناقَش: **شرطُ `IsHamzatWasl` لا اختبارَ سطحيًّا له**
(`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`) — ألفُ «الْحَمْدُ»
و«اهْدِنَا» لا تحمل علامةً أصلًا، فلا تُقرأ ساكنةً ولا متحرّكة، ولا يُعرَف
كونُها همزةَ وصلٍ إلّا بمعرفةٍ معجميةٍ أو صرفيةٍ ليست في العلامات. فمنزلةُ
هذه المواضع `لا_حالة_مكتوبة` وهي **متعذّرةُ القياس**، لا موافقةٌ ولا مخالفة.

**والمقروءُ من القوانين الثلاثة في خطّ القياس امتناعٌ لا قراءة**: اتّفقت
الثلاثةُ على أنّ ما يجري في **مفتتح الكلمة قبل أوّل حركةٍ مكتوبة** غيرُ مكتوبٍ
في الخطّ — الابتداءُ يُحرِّك بما ليس في النصّ، والوصلُ يُسقط ويستمدّ من آخر ما
قبله، والوقفُ لا يمسّ المفتتح — فوُسِّع الحيادُ في
`encoding.syllable_segmentation` إلى ذلك المفتتح كلِّه
(`THE_OPENING_BEFORE_THE_FIRST_VOWEL_IS_NOT_WRITTEN`). وهذا **لا ينقض** شيئًا
مما هنا: لا يُسمّى لامُ تعريف، ولا يُدّعى إدغام، ولا يُفصَل شكلُ اللام عن شكل
المدّ (`THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF` قائمٌ
بحاله، لأنّ ألفَ المدّ تقع بعد حركةٍ مكتوبةٍ فهي خارج المفتتح). وإنّما قيل إنّ
حالةً غيرَ مكتوبةٍ لا تُحاسَب حسابَ الساكن المكتوب، وهذا توسيعُ ما امتنع عنه
هذا التسجيلُ أصلًا.

**والاستثناءُ الذي سُمّي بعد الرقم أمانةٌ في وضعه**: قد يكون وصفًا صادقًا
للتلاوة، ولا يصير بذلك تصحيحًا لأداة قياس. فاستبعادُ المواضع التي أنتجت
المخالفةَ بعد رؤيتها **تعديلٌ بعد الرقم** لا إصلاحٌ سابقٌ له
(`EXCLUDING_A_COUNTEREXAMPLE_AFTER_THE_NUMBER_IS_AN_AMENDMENT`)، وهو المنوالُ
نفسُه الذي أُلزمت به المواصفةُ المُعدَّلة في `ud_objecthood_amendment`. والأخطرُ
منه أنّ معيارًا يُعيد تصنيفَ كلِّ مخالفٍ «ابتداءً غيرَ حقيقيّ» لا يبقى قابلًا
للتكذيب (`AN_EXCLUSION_RULE_THAT_ADMITS_NO_COUNTEREXAMPLE_IS_NOT_MEASURABLE`)؛
فـ«١٠٠٫٠٠٠٠٪» بعده ليس قياسًا ثانيًا بل إعادةُ تعريفٍ للمجتمع
(`THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_COUNTEREXAMPLES`).

**والاشتقاقُ المنطقيُّ لمنع التقاء الساكنين لم يُقَس هنا ولم يُكذَّب**: مسحُ
هذه الوحدة يرى **العلامات المكتوبة** لا السكونَ اللفظيّ، وخلوُّ النصّ من
ساكنَين مكتوبَين متجاورَين لا يُقرأ تصديقًا للاشتقاق
(`A_WRITTEN_SUKUN_IS_NOT_EVERY_QUIESCENCE`). ولذلك يُخرِج المسحُ **شكلًا
ثانيًا مُسمًّى**: حرفٌ بلا علامةٍ يليه مشدَّد، وفيه موضعُ «الضَّالِّينَ» الذي
يقرؤه أهلُ الأداء التقاءَ ساكنَين على حدّه، ليكون منظورًا لا مطويًّا.

**وكشف المسحُ حدَّ نفسِه وهو يعمل**: الشكلُ نفسُه يلتقط لامَ التعريف المُدغمة
في «اللَّهِ» و«الرَّحِيمِ»، وليست من هذا الباب في شيء — فالتفريقُ بين ألفِ
مدٍّ وبين ألفِ وصلٍ تليها لامٌ مُدغمة معرفةٌ معجميةٌ لا تُرى في العلامات
(`THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF`). فعددُ
صفوف هذا الشكل **ليس عددَ مواضع المدّ اللازم**، ولا تحكم هذه الوحدةُ في صفٍّ
منها بشيء.

**وقانونا الوصلِ والوقفِ مُسجَّلان بلا قراءة**: كلاهما يتكلّم على حدٍّ صوتيٍّ
بين كلمتين أو على موضع سكوتٍ، ولا يحمل النصُّ المكتوبُ المُودَعُ ما يدلّ على
أيّهما، فلا تُصطنَع لهما قراءةٌ من حدود الكلمات
(`WASL_AND_WAQF_ARE_REGISTERED_WITHOUT_A_READING`).

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا `E0`،
ولا تقرؤها بوّابةٌ في `kernel/`، ولا تستورد طبقةَ البرنامج
(`THIS_REGISTRATION_IS_NOT_A_GATE`).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .alif_state_raw_count import SHORT_VOWELS, CarrierAtomRow, decompose_lines
from .encoding.contamination_gate import scan_lines
from .fatiha_source_text import FATIHA_LINES, FATIHA_SOURCE_ID

__all__ = [
    "AN_EXCLUSION_RULE_THAT_ADMITS_NO_COUNTEREXAMPLE_IS_NOT_MEASURABLE",
    "A_WRITTEN_SUKUN_IS_NOT_EVERY_QUIESCENCE",
    "EXCLUDING_A_COUNTEREXAMPLE_AFTER_THE_NUMBER_IS_AN_AMENDMENT",
    "HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS",
    "IBTIDA_WASL_WAQF_NAMED_RESIDUALS",
    "SHADDA",
    "SUBMITTED_CLAIM_POPULATION_ID",
    "SUBMITTED_FREEZE_IDENTIFIER",
    "SUKUN",
    "THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_COUNTEREXAMPLES",
    "THE_DERIVATION_IS_NOT_A_MEASUREMENT",
    "THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF",
    "THE_THREE_LAWS",
    "THE_THREE_LAWS_ARE_SUPPLIED_WITHOUT_A_NAMED_SOURCE",
    "THIS_REGISTRATION_IS_NOT_A_GATE",
    "WASL_AND_WAQF_ARE_REGISTERED_WITHOUT_A_READING",
    "AdjacencyShape",
    "FirstStateReading",
    "IbtidaPositionRow",
    "IbtidaReadingTable",
    "IbtidaWaslWaqfError",
    "LawStanding",
    "QuiescenceAdjacencyRow",
    "QuiescenceAdjacencyTable",
    "SubmittedFreezeStanding",
    "SuppliedLaw",
    "derive_submitted_freeze_standing",
    "read_ibtida_on_the_deposited_fatiha",
    "read_ibtida_positions",
    "scan_quiescence_adjacency",
    "scan_quiescence_adjacency_on_the_deposited_fatiha",
]


class IbtidaWaslWaqfError(ValueError):
    """رُوجِع التسجيلُ بما لا يقوم به؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


# --- العلاماتُ المقروءة، مُعلَنةً لا مُستنبَطة --------------------------------


SUKUN: Final[str] = "\u0652"
"""السكونُ المكتوب وحدَه؛ وسكوتُ الحرف في اللفظ شيءٌ آخر لا تراه العلامات."""


SHADDA: Final[str] = "\u0651"
"""الشدّةُ المكتوبة؛ وقراءتُها ساكنًا فمتحرّكًا صنعةُ أداءٍ لا تُجرى هنا."""


# --- منزلةُ النصّ الوارد: ثلاثُ مراتبَ واثنتان بلا مدخل ------------------------


class LawStanding(Enum):
    """رتبةُ تحقُّق نصِّ القانون؛ والدنيا مرتبةٌ لأنّ فوقها مرتبتَين مُسمّاتَين."""

    MUQABALA_BI_TABA_MUSAMMAT = "مُقابَلة_بطبعةٍ_مُسمّاة"
    MIN_MASDARIN_MUSAMMAN_GHAYR_MUQABAL = "من_مصدرٍ_مُسمًّى_غير_مُقابَل"
    MUWRADA_BILA_MASDARIN_MUSAMMA = "مُورَدة_بلا_مصدرٍ_مُسمًّى"


@dataclass(frozen=True)
class SuppliedLaw:
    """قانونٌ واحدٌ كما ورد: اسمُه، ونصُّه بالكلمات، وصيغتُه الرمزية، ومنزلتُه.

    ولا يُبنى بمنزلةٍ فوق الدنيا: لم يصل لهذه القوانين كتابٌ ولا طبعةٌ ولا
    موضعٌ فيها، فالمرتبتان الأعلى غيرُ مبلوغتَين لا غيرَ مُدَّعاتَين فحسب.
    """

    key: str
    statement: str
    formal_text: str
    standing: LawStanding

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise IbtidaWaslWaqfError("قانونٌ بلا اسمٍ لا يُراجَع.")
        if not self.statement.strip():
            raise IbtidaWaslWaqfError("قانونٌ بلا نصٍّ بالكلمات ليس تسجيلًا لنصّ.")
        if not self.formal_text.strip():
            raise IbtidaWaslWaqfError("قانونٌ بلا صيغةٍ مكتوبةٍ كما وردت لا يُقابَل.")
        if self.standing is not LawStanding.MUWRADA_BILA_MASDARIN_MUSAMMA:
            raise IbtidaWaslWaqfError(
                "لم يُسمَّ لهذه القوانين مصدرٌ، فلا تُبنى بمنزلةٍ فوق "
                "`مُورَدة_بلا_مصدرٍ_مُسمًّى`؛ والمنزلةُ تُبلَغ بمصدرٍ لا بتصريح."
            )


THE_THREE_LAWS: Final[tuple[SuppliedLaw, ...]] = (
    SuppliedLaw(
        key="الابتداء",
        statement=(
            "يُمنَع بدءُ سلسلة الذرّات بحالة سكون، إلّا أن تكون الذرّةُ الأولى " "همزةَ وصل"
        ),
        formal_text="Ibtida(W) ⟺ state(a₁) ≠ sukun ∨ IsHamzatWasl(a₁)",
        standing=LawStanding.MUWRADA_BILA_MASDARIN_MUSAMMA,
    ),
    SuppliedLaw(
        key="الوصل",
        statement=(
            "عند الوصل بما قبله تسقط همزةُ الوصل، وتُستمَدّ الحركةُ العابرةُ "
            "للحدّ من آخر الكلمة السابقة لا من أوّل التالية"
        ),
        formal_text=(
            "Wasl(Wᵢ, Wᵢ₊₁) ⟺ drop(HamzatWasl(a₁^(i+1))) ∧ "
            "state(aₙ^(i)) يُموِّل الحركة اللازمة لعبور الحدّ"
        ),
        standing=LawStanding.MUWRADA_BILA_MASDARIN_MUSAMMA,
    ),
    SuppliedLaw(
        key="الوقف",
        statement=(
            "عند الوقف تُسكَّن الحالةُ الأخيرة إن كانت فتحةً أو ضمّةً أو كسرة، "
            "وتصير ألفًا ممدودةً إن كانت تنوينَ فتحٍ خاصّة"
        ),
        formal_text=(
            "Waqf(W): state(aₙ) ↦ sukun_explicit إن كانت {fatha, damma, kasra}؛ "
            "↦ fatha + مدّ الألف إن كانت تنوينَ فتح"
        ),
        standing=LawStanding.MUWRADA_BILA_MASDARIN_MUSAMMA,
    ),
)
"""القوانينُ الثلاثةُ كما وردت؛ ونصُّها محفوظٌ ليُقابَل يومَ يصل مصدرُه."""


# --- قراءةُ قانون الابتداء: معيارٌ سطحيٌّ مُصرَّحٌ به، ورابعُه متعذّر ----------


class FirstStateReading(Enum):
    """منزلةُ أوّلِ حاملٍ في كلمةٍ مكتوبة، وهي أربعٌ تستوعب كلَّ موضع.

    والعضوُ الثالثُ `لا_حالة_مكتوبة` ليس تلطيفًا لـ«ساكن»: الحاملُ العاري من
    كلّ علامةٍ لم تُكتَب حالتُه أصلًا، فقراءتُه ساكنًا تُنشئ ما لم يُقرأ،
    وقراءتُه متحرّكًا كذلك.
    """

    YABDA_BI_HARAKA = "يبدأ_بحركة"
    YABDA_BI_SUKUN_MAKTUB = "يبدأ_بسكونٍ_مكتوب"
    LA_HALA_MAKTUBA = "لا_حالة_مكتوبة"
    ALAMA_UKHRA_MAKTUBA = "علامةٌ_أخرى_مكتوبة"


@dataclass(frozen=True)
class IbtidaPositionRow:
    """موضعُ ابتداءٍ واحدٌ بحدّ الكلمة المكتوبة، ومنزلةُ أوّلِ حاملٍ فيه."""

    line_index: int
    word_index: int
    word: str
    first_carrier: str
    first_marks: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.line_index < 0 or self.word_index < 0:
            raise IbtidaWaslWaqfError("موضعُ الكلمة لا يكون سالبًا.")
        if len(self.first_carrier) != 1:
            raise IbtidaWaslWaqfError("الحاملُ الأوّلُ رمزٌ واحد.")

    @property
    def reading(self) -> FirstStateReading:
        """اقرأ المنزلةَ من العلامات المكتوبة وحدَها، بترتيبٍ مُصرَّحٍ به."""
        if any(mark in SHORT_VOWELS for mark in self.first_marks):
            return FirstStateReading.YABDA_BI_HARAKA
        if SUKUN in self.first_marks:
            return FirstStateReading.YABDA_BI_SUKUN_MAKTUB
        if self.first_marks:
            return FirstStateReading.ALAMA_UKHRA_MAKTUBA
        return FirstStateReading.LA_HALA_MAKTUBA


@dataclass(frozen=True)
class IbtidaReadingTable:
    """صفٌّ لكلّ كلمةٍ مكتوبةٍ في النصّ المقروء، لا لِما وافق منها فقط.

    ولا حقلَ نسبةٍ هنا: النسبةُ تحتاج مجتمعًا مُعرَّفًا قبل الرقم، والمجتمعُ
    الذي يتكلّم عنه الرقمُ الوارد ليس هذا النصّ.
    """

    source_id: str
    rows: tuple[IbtidaPositionRow, ...]

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise IbtidaWaslWaqfError("قراءةٌ بلا اسمِ مصدرٍ لا تُراجَع.")

    def rows_read_as(self, reading: FirstStateReading) -> tuple[IbtidaPositionRow, ...]:
        """صفوفُ منزلةٍ بعينها بترتيب ورودها."""
        return tuple(row for row in self.rows if row.reading is reading)

    @property
    def positions_beginning_with_a_written_sukun(
        self,
    ) -> tuple[IbtidaPositionRow, ...]:
        """مخالفاتُ قانون الابتداء إن وُجدت بهذا المعيار السطحيّ وحدَه."""
        return self.rows_read_as(FirstStateReading.YABDA_BI_SUKUN_MAKTUB)

    @property
    def positions_with_no_written_state(self) -> tuple[IbtidaPositionRow, ...]:
        """المواضعُ المتعذّرةُ القياس، ومنها كلُّ همزة وصلٍ في هذا الرسم."""
        return self.rows_read_as(FirstStateReading.LA_HALA_MAKTUBA)

    @property
    def decidable_positions(self) -> tuple[IbtidaPositionRow, ...]:
        """ما تحسمه العلاماتُ المكتوبةُ وحدَها: حركةٌ أو سكونٌ مكتوب."""
        return tuple(
            row
            for row in self.rows
            if row.reading
            in (
                FirstStateReading.YABDA_BI_HARAKA,
                FirstStateReading.YABDA_BI_SUKUN_MAKTUB,
            )
        )


def _first_atom_per_word(
    atoms: Iterable[CarrierAtomRow],
) -> tuple[CarrierAtomRow, ...]:
    seen: set[tuple[int, int]] = set()
    firsts: list[CarrierAtomRow] = []
    for atom in atoms:
        key = (atom.line_index, atom.word_index)
        if key in seen:
            continue
        seen.add(key)
        firsts.append(atom)
    return tuple(firsts)


def read_ibtida_positions(
    lines: Iterable[str], *, source_id: str
) -> IbtidaReadingTable:
    """اقرأ منزلةَ أوّلِ حاملٍ في كلّ كلمةٍ من هذه السطور، صفًّا لكلّ كلمة.

    وهي دالّةٌ عامّةٌ تأخذ أيّ نصٍّ عربيٍّ مُشكَّل، ولا تعرف الفاتحةَ ولا سواها؛
    وتفكيكُ الذرّات مُستورَدٌ من `alif_state_raw_count` لا مُعادٌ كتابتُه، فلا
    تنشأ قاعدةُ حاملٍ ثانيةٌ تنزلق عن الأولى.
    """
    atoms, _unattached, _unclassified = decompose_lines(lines)
    rows = tuple(
        IbtidaPositionRow(
            line_index=atom.line_index,
            word_index=atom.word_index,
            word=atom.word,
            first_carrier=atom.carrier,
            first_marks=atom.state_marks,
        )
        for atom in _first_atom_per_word(atoms)
    )
    return IbtidaReadingTable(source_id=source_id, rows=rows)


def read_ibtida_on_the_deposited_fatiha() -> IbtidaReadingTable:
    """شغِّل كاشفَ التلوّث على النصّ المُودَع، ثمّ اقرأ مواضعَ الابتداء فيه.

    ومدخلٌ عديمُ الوسائط عن قصد، على حدّ
    `THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS`.
    """
    report = scan_lines(FATIHA_LINES)
    if report.rejected:
        raise IbtidaWaslWaqfError(
            "ردَّ كاشفُ التلوّث رموزًا من النصّ المُودَع، ولا تُقرأ مواضعُ "
            "ابتداءٍ على ما لم يجتز الخطوةَ صفر."
        )
    return read_ibtida_positions(FATIHA_LINES, source_id=FATIHA_SOURCE_ID)


# --- مسحُ تجاور السكون: ما تراه العلاماتُ، وما لا تراه مُسمًّى ------------------


class AdjacencyShape(Enum):
    """شكلُ تجاورٍ مُسجَّل؛ والثاني ليس حكمًا بالتقاء ساكنَين بل موضعٌ مُسمًّى."""

    SAKINAN_MAKTUBAN = "ساكنان_مكتوبان"
    ARIN_QABLA_MUSHADDAD = "حرفٌ_بلا_علامةٍ_قبل_مشدَّد"


@dataclass(frozen=True)
class QuiescenceAdjacencyRow:
    """حاملان متجاوران في كلمةٍ واحدة، وشكلُ تجاورهما كما رُئي مكتوبًا."""

    line_index: int
    word_index: int
    word: str
    first_carrier: str
    second_carrier: str
    shape: AdjacencyShape

    def __post_init__(self) -> None:
        if not isinstance(self.shape, AdjacencyShape):
            raise IbtidaWaslWaqfError("الشكلُ عضوٌ في `AdjacencyShape`.")


@dataclass(frozen=True)
class QuiescenceAdjacencyTable:
    """صفوفُ التجاور المُسمّاة في نصٍّ واحد، ولا حكمَ فيها على الاشتقاق."""

    source_id: str
    rows: tuple[QuiescenceAdjacencyRow, ...]

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise IbtidaWaslWaqfError("مسحٌ بلا اسمِ مصدرٍ لا يُراجَع.")

    def rows_of_shape(
        self, shape: AdjacencyShape
    ) -> tuple[QuiescenceAdjacencyRow, ...]:
        """صفوفُ شكلٍ بعينه بترتيب ورودها."""
        return tuple(row for row in self.rows if row.shape is shape)

    @property
    def written_sukun_pairs(self) -> tuple[QuiescenceAdjacencyRow, ...]:
        """ما يراه المعيارُ المكتوبُ التقاءَ ساكنَين، وخلوُّه ليس تصديقًا."""
        return self.rows_of_shape(AdjacencyShape.SAKINAN_MAKTUBAN)

    @property
    def unmarked_before_shadda_positions(self) -> tuple[QuiescenceAdjacencyRow, ...]:
        """حرفٌ عارٍ يليه مشدَّد؛ شكلٌ يجمع ألفَ المدّ ولامَ التعريف المُدغمة.

        وليس هذا عدَّ مواضع المدّ اللازم: الفصلُ بين البابَين معرفةٌ معجميةٌ لا
        تُرى في العلامات، وهو ما يقوله
        `THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF`.
        """
        return self.rows_of_shape(AdjacencyShape.ARIN_QABLA_MUSHADDAD)


def _shape_of(first: CarrierAtomRow, second: CarrierAtomRow) -> AdjacencyShape | None:
    if SUKUN in first.state_marks and SUKUN in second.state_marks:
        return AdjacencyShape.SAKINAN_MAKTUBAN
    if not first.state_marks and SHADDA in second.state_marks:
        return AdjacencyShape.ARIN_QABLA_MUSHADDAD
    return None


def scan_quiescence_adjacency(
    lines: Iterable[str], *, source_id: str
) -> QuiescenceAdjacencyTable:
    """امسح كلَّ حاملَين متجاورَين داخل كلمةٍ واحدة، واحفظ ما انطبق عليه شكل.

    والتجاورُ داخلَ الكلمة وحدَه: ما بين كلمتين حدٌّ لا يُعرَف من الرسم أوُصِل
    أم وُقف عليه، فقياسُه من حدود الكلمات يقيس الأداةَ لا اللغة.
    """
    atoms, _unattached, _unclassified = decompose_lines(lines)
    rows: list[QuiescenceAdjacencyRow] = []
    for first, second in zip(atoms, atoms[1:]):
        if (first.line_index, first.word_index) != (
            second.line_index,
            second.word_index,
        ):
            continue
        shape = _shape_of(first, second)
        if shape is None:
            continue
        rows.append(
            QuiescenceAdjacencyRow(
                line_index=first.line_index,
                word_index=first.word_index,
                word=first.word,
                first_carrier=first.carrier,
                second_carrier=second.carrier,
                shape=shape,
            )
        )
    return QuiescenceAdjacencyTable(source_id=source_id, rows=tuple(rows))


def scan_quiescence_adjacency_on_the_deposited_fatiha() -> QuiescenceAdjacencyTable:
    """شغِّل كاشفَ التلوّث على النصّ المُودَع، ثمّ امسح تجاورَ حواملِه."""
    report = scan_lines(FATIHA_LINES)
    if report.rejected:
        raise IbtidaWaslWaqfError(
            "ردَّ كاشفُ التلوّث رموزًا من النصّ المُودَع، ولا يُمسَح ما لم " "يجتز الخطوةَ صفر."
        )
    return scan_quiescence_adjacency(FATIHA_LINES, source_id=FATIHA_SOURCE_ID)


# --- منزلةُ التجميد الوارد: مُشتقّةٌ من المقروء لا مُعلَنةٌ في حقل --------------


SUBMITTED_FREEZE_IDENTIFIER: Final[str] = (
    "IBTIDA_LAW-99.9974PCT-RAW-100PCT-AFTER-NAMING-LAM-AMR-EXCEPTION-AR-1"
)
"""معرِّفُ التجميد كما ورد؛ محفوظٌ بحروفه ليُراجَع لا ليُعمَل به."""


SUBMITTED_CLAIM_POPULATION_ID: Final[str] = "القرآن-كلُّه-غيرُ-مُودَعٍ-في-هذه-الشجرة"
"""المجتمعُ الذي يتكلّم عنه الرقمُ الوارد؛ ولا نصَّ في الشجرة يحمل هذا الاسم."""


class SubmittedFreezeStanding(Enum):
    """حكمُ التجميد الوارد، مُشتقًّا من المصدر المقروء لا من دعوى صاحبه."""

    MAQBUL_BI_ITADAT_TASHGHIL = "مقبولٌ_بإعادةِ_تشغيلٍ_على_مجتمعه"
    MARFUD_LI_ANNA_MUJTAMAAHU_GHAYR_MUWDA = "مرفوضٌ_لأنّ_مجتمعَه_غيرُ_مُودَعٍ_هنا"


def derive_submitted_freeze_standing(
    table: IbtidaReadingTable,
) -> SubmittedFreezeStanding:
    """احكم على التجميد الوارد بمصدر ما قُرئ فعلًا، لا بعدد ما وافق منه.

    والاشتقاقُ من اسم المصدر وحدَه: قراءةٌ على نصٍّ مُودَعٍ في هذه الشجرة ليست
    قراءةً على المجتمع الذي يتكلّم عنه الرقم، مهما بلغ عددُ صفوفها؛ ولا يُقرأ
    هذا الرفضُ تكذيبًا للقانون ولا للرقم، بل منعًا من تجميدِ ما لم يُعَد.
    """
    if table.source_id == SUBMITTED_CLAIM_POPULATION_ID:
        return SubmittedFreezeStanding.MAQBUL_BI_ITADAT_TASHGHIL
    return SubmittedFreezeStanding.MARFUD_LI_ANNA_MUJTAMAAHU_GHAYR_MUWDA


# --- ما لا يحسمه هذا التسجيل، مُسمًّى ------------------------------------------


THE_THREE_LAWS_ARE_SUPPLIED_WITHOUT_A_NAMED_SOURCE: Final[str] = (
    "THE_THREE_LAWS_ARE_SUPPLIED_WITHOUT_A_NAMED_SOURCE: وصلت القوانينُ "
    "الثلاثةُ نصًّا بلا كتابٍ ولا مؤلّفٍ ولا طبعةٍ ولا موضعٍ فيها، فمنزلتُها "
    "الدنيا، والمرتبتان الأعلى عضوان بلا مدخلٍ حتى يصل مصدرٌ يُقابَل به"
)

HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS: Final[str] = (
    "HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS: شرطُ "
    "`IsHamzatWasl(a₁)` لا اختبارَ له في العلامات المكتوبة؛ فألفُ «الْحَمْدُ» "
    "و«اهْدِنَا» عاريةٌ من كلّ علامة، ومعرفتُها همزةَ وصلٍ معرفةٌ معجميةٌ "
    "صرفية. فكلُّ هذه المواضع `لا_حالة_مكتوبة` متعذّرةُ القياس، ولا يُقاس "
    "القانونُ كما نُطِق به إلّا بمُعرِّفٍ لهمزة الوصل لم يُبنَ هنا"
)

A_WRITTEN_SUKUN_IS_NOT_EVERY_QUIESCENCE: Final[str] = (
    "A_WRITTEN_SUKUN_IS_NOT_EVERY_QUIESCENCE: المسحُ يرى علامةَ السكون "
    "المكتوبة، والسكوتُ في اللفظ أوسعُ منها: الحرفُ العاري والشطرُ الأوّلُ من "
    "المشدَّد كلاهما ساكنٌ لفظًا ولا علامةَ سكونٍ عليه. فخلوُّ `written_sukun_pairs` "
    "ليس تصديقًا لاشتقاق منع التقاء الساكنين، ولذلك سُمّي شكلُ المدّ اللازم "
    "صفًّا ثانيًا يُرى بدل أن يُطوى"
)

THE_DERIVATION_IS_NOT_A_MEASUREMENT: Final[str] = (
    "THE_DERIVATION_IS_NOT_A_MEASUREMENT: الاشتقاقُ المنطقيُّ لمنع التقاء "
    "الساكنين وارِدٌ نثرًا، وإحكامُه ليس من جنس الدليل المقيس؛ ولم يُقَس هنا "
    "ولم يُكذَّب، ولا تحمل هذه الوحدةُ حقلًا لحكمٍ فيه"
)

EXCLUDING_A_COUNTEREXAMPLE_AFTER_THE_NUMBER_IS_AN_AMENDMENT: Final[str] = (
    "EXCLUDING_A_COUNTEREXAMPLE_AFTER_THE_NUMBER_IS_AN_AMENDMENT: استبعادُ "
    "لام الأمر الساكنة سُمّي بعد رؤية الموضعَين اللذين أنتجا المخالفة، فهو "
    "تعديلٌ بعد الرقم بمنزلة `معدَّلة_بعد_الرقم` في `ud_objecthood_amendment`، "
    "لا إصلاحٌ لأداةٍ سبق الدليلَ؛ وصدقُ الوصف في التلاوة لا يُغيّر منزلتَه"
)

THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_COUNTEREXAMPLES: Final[str] = (
    "THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_COUNTEREXAMPLES: «١٠٠٫٠٠٠٠٪» "
    "بعد الاستبعاد ليس قياسًا ثانيًا: مجتمعُه مُعرَّفٌ بالسمة التي أنتجت "
    "المخالفتَين نفسَها، فالرقمُ مُشتقٌّ من التعريف لا من النصّ"
)

AN_EXCLUSION_RULE_THAT_ADMITS_NO_COUNTEREXAMPLE_IS_NOT_MEASURABLE: Final[str] = (
    "AN_EXCLUSION_RULE_THAT_ADMITS_NO_COUNTEREXAMPLE_IS_NOT_MEASURABLE: معيارٌ "
    "يُعيد تصنيفَ كلّ مخالفٍ «موضعَ ابتداءٍ غيرَ حقيقيّ» لا يبقى قابلًا "
    "للتكذيب؛ فإن أُريد إعمالُ الاستثناء وجب أن يُكتَب مُعرِّفُه المستقلُّ "
    "**قبل** القراءة التالية، فيصير للقانون موضعٌ يُكذّبه إن وُجد"
)

WASL_AND_WAQF_ARE_REGISTERED_WITHOUT_A_READING: Final[str] = (
    "WASL_AND_WAQF_ARE_REGISTERED_WITHOUT_A_READING: قانونا الوصل والوقف "
    "يتكلّمان على حدٍّ صوتيٍّ وعلى موضع سكوت، ولا يدلّ الرسمُ المُودَعُ على "
    "أيّهما؛ فنصُّهما مُسجَّلٌ ولا قراءةَ لهما هنا، ولا تُصطنَع لهما واحدةٌ من "
    "حدود الكلمات المكتوبة"
)

THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF: Final[str] = (
    "THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF: شكلُ "
    "«حرفٌ عارٍ قبل مشدَّد» يلتقط ألفَ المدّ في «الضَّالِّينَ» ولامَ التعريف "
    "المُدغمة في «اللَّهِ» معًا، والفصلُ بينهما معرفةٌ معجميةٌ لا تُرى في "
    "العلامات؛ فعددُ صفوف الشكل ليس عددَ مواضع المدّ اللازم، وقراءتُه كذلك "
    "تُحمِّل الأداةَ ما لا تراه"
)

THIS_REGISTRATION_IS_NOT_A_GATE: Final[str] = (
    "THIS_REGISTRATION_IS_NOT_A_GATE: لا ولادةَ في هذه الوحدة، ولا حكمَ "
    "ولادة، ولا تجميد، ولا `E0`، ولا تستورد من `kernel/` شيئًا ولا تقرؤها "
    "وحدةٌ فيه، ولا تستورد طبقةَ البرنامج"
)

IBTIDA_WASL_WAQF_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_THREE_LAWS_ARE_SUPPLIED_WITHOUT_A_NAMED_SOURCE": (
        THE_THREE_LAWS_ARE_SUPPLIED_WITHOUT_A_NAMED_SOURCE
    ),
    "HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS": (
        HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS
    ),
    "A_WRITTEN_SUKUN_IS_NOT_EVERY_QUIESCENCE": A_WRITTEN_SUKUN_IS_NOT_EVERY_QUIESCENCE,
    "THE_DERIVATION_IS_NOT_A_MEASUREMENT": THE_DERIVATION_IS_NOT_A_MEASUREMENT,
    "EXCLUDING_A_COUNTEREXAMPLE_AFTER_THE_NUMBER_IS_AN_AMENDMENT": (
        EXCLUDING_A_COUNTEREXAMPLE_AFTER_THE_NUMBER_IS_AN_AMENDMENT
    ),
    "THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_COUNTEREXAMPLES": (
        THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_COUNTEREXAMPLES
    ),
    "AN_EXCLUSION_RULE_THAT_ADMITS_NO_COUNTEREXAMPLE_IS_NOT_MEASURABLE": (
        AN_EXCLUSION_RULE_THAT_ADMITS_NO_COUNTEREXAMPLE_IS_NOT_MEASURABLE
    ),
    "WASL_AND_WAQF_ARE_REGISTERED_WITHOUT_A_READING": (
        WASL_AND_WAQF_ARE_REGISTERED_WITHOUT_A_READING
    ),
    "THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF": (
        THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF
    ),
    "THIS_REGISTRATION_IS_NOT_A_GATE": THIS_REGISTRATION_IS_NOT_A_GATE,
}
"""ما لا يحسمه هذا التسجيل، مُسمًّى هنا لا متروكًا ليُفترَض."""
