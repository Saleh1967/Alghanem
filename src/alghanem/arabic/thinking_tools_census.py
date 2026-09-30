"""جدولُ «منهج التفكير» الوارد، مُشغَّلًا على البايتات المختومة — **وأكثرُه لم يُعَد**.

وصل جدولٌ من خارج الشجرة يدّعي أنّه **جردُ أدوات التفكير في المدوّنة مقيسًا على
البتات**، ثمانيةَ صفوفٍ بأرقامها: الأمثال 112، والتحدي 366، والاستدلال الحسّي
185، و«كأنّ» 70، واليقين 440 مقابل الظنّ 174، والحساب 33، والإحكام 18، والشبكة
114 · 6,236 · 77,801. وهذه الوحدةُ تفعل به ما تفعله الشجرةُ بكلّ رقمٍ يصلها:
تُودِعه كما ورد، وتُعلِن قاعدةَ عدٍّ **مكتوبةً قبل التشغيل**، وتُشغِّلها على
بايتات `corpora/quran-simple-enhanced.txt` المبصومة، ثمّ تنشر المقيسَ إلى جانب
المنقول بلا تقريبٍ ولا تلطيف::

    الصفّ            المنقول            المقيس ههنا
    الأمثال          112               148 وقوعًا · 130 آية
    التحدي           366                12 وقوعًا
    الاستدلال الحسّي   185                47 وقوعًا
    «كأنّ»             70                40 وقوعًا · 37 آية
    اليقين/الظنّ    440 : 174           17 : 85  — **الاتجاهُ مقلوب**
    الحساب            33                45 وقوعًا
    الإحكام           18                17 وقوعًا
    الشبكة    114 · 6,236 · 77,801   لا سورةَ تُقاس · 6,236 · 82,532

**أوّلًا: القاعدةُ لم تصل، فلا يُقرأ الفرقُ تكذيبًا لعدٍّ آخر.** الجدولُ
الواردُ لم يذكر قاعدةَ مطابقةٍ واحدة: أبالوقوع عُدَّ أم بالآيات؟ أبالرسم
المشكول أم بالمجرَّد؟ أبمِجَسٍّ فرعيٍّ أم بصورةٍ تامّة؟ ولا مدوّنةً مبصومةً
سمّاها. فرقمٌ بلا قاعدةٍ **غيرُ قابلٍ لإعادة الاشتقاق** أصلًا، وما ههنا مقابلةُ
رقمٍ مقيسٍ بقاعدةٍ معلنةٍ برقمٍ لا قاعدةَ له، لا نقضُ قياسٍ بقياس
(`A_FIGURE_WITHOUT_A_RULE_IS_NOT_REFUTED_IT_IS_UNREDERIVABLE`).

**وثانيًا: الصفُّ الوحيدُ الذي انقلب اتجاهُه، لا مقدارُه فحسب.** ادّعى الجدولُ
أنّ أدوات اليقين **٢٫٥ ضعفِ** أدوات الظنّ، وبنى عليه أنّ «النصَّ يفكّر باليقين
قبل الظنّ عددًا». والمقيسُ تحت مِجَسّاتٍ معلنةٍ عكسُه: اليقين 17 والظنّ 85، أي
الظنُّ **خمسةُ أضعافِ** اليقين تقريبًا. وانقلابُ الاتجاه ليس خلافًا في المقدار
يُحتمَل، فيُنشَر صفًّا مستقلًّا مسمًّى
(`THE_DIRECTION_ITSELF_INVERTED_UNDER_A_DECLARED_RULE`).

**وثالثًا: «صدفةُ الأمثال 112» سقطت في موضعها.** الجدولُ أعلن اكتشافًا: أنّ
أدوات القياس بالمشابهة **112** «مساويةً للحقل خليةً خليةً»، وسجّله «صدفةً معلنة
لا دلالة». والمقيسُ ههنا تحت مِجَسِّ «مثل» المجرَّد: **148 وقوعًا في 130 آية**،
و**27 صورةً متمايزة** — فلا 112 ولا 114. فالصدفةُ لم تُنقَض معناها، بل **لم
يوجَد طرفُها الأوّل** على هذه البايتات بهذه القاعدة. ومن أراد إحياءها فعليه أن
يُعلن القاعدةَ التي تُخرِج 112 **قبل** أن يعدّ، لا أن يبحث عن قاعدةٍ تُخرِجها
بعد أن عَلِمها (`A_COINCIDENCE_NEEDS_ITS_FIRST_TERM_MEASURED_TOO`).

**ورابعًا: صفُّ الشبكة فيه رقمٌ لا تبلغه هذه البايتات ألبتّة.** المدوّنةُ
المودَعةُ **بلا حقول**: سطرٌ لكلّ آيةٍ بلا رقم سورةٍ ولا رقم آية — ولذلك تُخرِج
`count_words` عليها صفرًا تحت قاعدة `WHITESPACE_TOKENS_IN_AYAH_TEXT` المبنيّةِ
على فاصل الحقول. فعددُ السور **114 غيرُ مقيسٍ ههنا**، لا مُكذَّبًا ولا
مُصدَّقًا، ويُسجَّل `THE_SURA_COUNT_IS_NOT_IN_THESE_BYTES`. وأمّا الآياتُ
فـ6,236 مطابقةٌ للمنقول، والكلماتُ 82,532 تحت قاعدة «رموزٌ يفصلها بياضٌ في
السطر» لا 77,801 — وهذا ثالثُ رقمِ كلماتٍ يُقابَل في الشجرة بعد 78,215 المنقول
في `quran_corpus_word_total` و78,081 المجموع فيه.

**وخامسًا: الأرقامُ حدودٌ عليا، وقد قِيس مقدارُ العلوّ لا أُعلن وصفًا.** الجدولُ
الواردُ أقرّ أنّ «ألم» تلتقط غيرَ الاستفهام فالأرقامُ حدودٌ عليا. ونحن نُثبِت
ذلك عددًا لا إقرارًا: تحت مِجَسِّ «شك» **80 وقوعًا، منها 15 فقط صورةُ «شك»
نفسِها**، والباقي شُكرٌ وشكلٌ وشكوى — فأُخرِج المِجَسُّ من صفّ الظنّ بهذا
السبب المقيس. وتحت مِجَسَّي اليقين بقي في المُطابِق **«الفريقين» ثلاثًا
و«والصديقين» مرّة**: أربعةُ وقوعاتٍ ليست من اليقين في شيء، فالسبعةَ عشرَ حدٌّ
أعلى ثلاثةَ عشرَ في جوفه (`THE_UPPER_BOUND_IS_MEASURED_NOT_DECLARED`).

**وسادسًا: المِجَسّاتُ غيرُ متداخلةٍ بحكم الإنشاء.** لا يُقبَل مِجَسٌّ هو جزءٌ
من مِجَسٍّ آخرَ في الأداة نفسِها («موقن» مع «موقنون» مثلًا)، إذ يُعَدُّ الوقوعُ
الواحدُ مرّتين فيُنفَخ الرقم. والحارسُ في `__post_init__` لا في النثر
(`NESTED_PROBES_DOUBLE_COUNT_SO_THEY_ARE_REFUSED`).

**وسابعًا: تجريدُ التشكيل تامٌّ على هذه البايتات، ومقيسٌ.** المِجَسّاتُ مكتوبةٌ
مجرَّدةً وتُطابَق على نصٍّ مجرَّد بـ`strip_diacritics`، ومجالُها 064B–0652.
وقد مُسِحت المدوّنةُ فلم يقع فيها علامةٌ متّصلةٌ خارجَ هذا المجال ولا تطويل،
فالتجريدُ ههنا **تامٌّ بالقياس لا بالدعوى**.

**وثامنًا: ما ليس ههنا.** لا يُقال إنّ هذه الأرقامَ «أدواتُ تفكيرٍ»: المقيسُ
**صورٌ سطحيّةٌ في رسمٍ مجرَّد**، وبين الصورة وأداةِ التفكير تأويلٌ لم تدخله
الشجرة. والترتيبُ الزمنيُّ (مكّيّ/مدنيّ · نزول) خارجُ البايتات فخارجُ الجدول.
ولا يُبنى على صفٍّ ههنا حكمٌ إبستمولوجيّ: كونُ الظنّ أكثرَ ورودًا من اليقين
عددًا **لا يقول شيئًا** عن رتب المعرفة، كما أنّ عكسَه لم يكن ليقوله
(`A_SURFACE_COUNT_LICENSES_NO_EPISTEMOLOGY`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/` ولا من `program/`، والبايتاتُ تُقرأ من بابها الوحيد
`read_quran_corpus_bytes`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Final

from .quran_corpus_word_total import read_quran_corpus_bytes, strip_diacritics

__all__ = [
    "A_COINCIDENCE_NEEDS_ITS_FIRST_TERM_MEASURED_TOO",
    "A_FIGURE_WITHOUT_A_RULE_IS_NOT_REFUTED_IT_IS_UNREDERIVABLE",
    "A_SURFACE_COUNT_LICENSES_NO_EPISTEMOLOGY",
    "NESTED_PROBES_DOUBLE_COUNT_SO_THEY_ARE_REFUSED",
    "THE_DIRECTION_ITSELF_INVERTED_UNDER_A_DECLARED_RULE",
    "THE_NAMED_CONTAMINANTS",
    "THE_REFUSED_PROBES",
    "THE_SURA_COUNT_IS_NOT_IN_THESE_BYTES",
    "THE_TOOL_PROBES",
    "THE_TRANSCRIBED_TABLE",
    "THE_UPPER_BOUND_IS_MEASURED_NOT_DECLARED",
    "THINKING_TOOLS_NAMED_RESIDUALS",
    "ClaimStanding",
    "Contaminant",
    "NetworkReading",
    "ThinkingTool",
    "ThinkingToolsCensusError",
    "ToolMeasurement",
    "ToolProbes",
    "TranscribedRow",
    "certainty_to_conjecture",
    "every_measurement",
    "measure_tool",
    "network_reading",
    "standing_of",
]


class ThinkingToolsCensusError(ValueError):
    """رفضٌ في هذا الباب: مِجَسٌّ متداخل، أو أداةٌ بلا مِجَسّ، أو رقمٌ سالب."""


class ThinkingTool(Enum):
    """صفوفُ الجدول الوارد، أداةً أداةً؛ ولا يُفتَح صفٌّ ليس فيه."""

    CLASSIFICATION = "التصنيف"
    ANALOGY = "القياس_بالمشابهة"
    EXHAUSTIVE_CHALLENGE = "التحدي_الاستنفادي"
    SENSORY_INFERENCE = "الاستدلال_بالمشاهدة"
    SENSORY_IMAGERY = "التصوير_الحسي"
    CERTAINTY = "أدوات_اليقين"
    CONJECTURE = "أدوات_الظن"
    RECKONING = "الحساب"
    EXHAUSTIVE_PRECISION = "الإحكام_الاستنفادي"


class ClaimStanding(Enum):
    """منزلةُ صفٍّ واردٍ بعد التشغيل؛ تُشتَقّ من الرقمين ولا تُكتَب في حقل."""

    REPRODUCED = "أُعيد_اشتقاقُه"
    DIVERGED = "خالف_المقيس"
    DIRECTION_INVERTED = "انقلب_اتجاهُه"
    NOT_IN_THESE_BYTES = "لا_تبلغه_هذه_البايتات"


A_FIGURE_WITHOUT_A_RULE_IS_NOT_REFUTED_IT_IS_UNREDERIVABLE: Final[str] = (
    "الجدولُ الواردُ لم يُعلن قاعدةَ مطابقةٍ ولا مدوّنةً مبصومة؛ فالفرقُ ههنا "
    "مقابلةُ مقيسٍ بقاعدةٍ معلنةٍ بمنقولٍ لا قاعدةَ له، لا نقضُ قياسٍ بقياس"
)

THE_DIRECTION_ITSELF_INVERTED_UNDER_A_DECLARED_RULE: Final[str] = (
    "ادّعى المنقولُ يقينًا 2.5× الظنّ، والمقيسُ ظنٌّ يفوق اليقينَ أضعافًا؛ "
    "وانقلابُ الاتجاه منزلةٌ مستقلّةٌ عن الخلاف في المقدار فيُنشَر باسمه"
)

A_COINCIDENCE_NEEDS_ITS_FIRST_TERM_MEASURED_TOO: Final[str] = (
    "«الأمثال 112 = خلايا الحقل» لم تُنقَض دلالتُها بل لم يوجَد طرفُها الأوّل: "
    "فمن أرادها فليُعلن القاعدةَ التي تُخرِج 112 قبل العدّ لا بعد أن عَلِمها"
)

THE_UPPER_BOUND_IS_MEASURED_NOT_DECLARED: Final[str] = (
    "كونُ الأرقام حدودًا عليا يُثبَت بعدِّ الملوِّثات بأعيانها لا بإقرارٍ في "
    "النثر؛ وما لم يُعَدَّ ملوِّثُه فحدُّه الأعلى غيرُ معلوم المقدار"
)

NESTED_PROBES_DOUBLE_COUNT_SO_THEY_ARE_REFUSED: Final[str] = (
    "مِجَسٌّ هو جزءٌ من مِجَسٍّ آخرَ في الأداة نفسِها يُعَدُّ وقوعُه مرّتين، "
    "فيُرفَض عند الإنشاء لا في التعليق"
)

A_SURFACE_COUNT_LICENSES_NO_EPISTEMOLOGY: Final[str] = (
    "عددُ صورٍ سطحيّةٍ في رسمٍ مجرَّدٍ لا يُصدِر حكمًا في رتب المعرفة؛ ولو خرج "
    "على العكس لما أصدره أيضًا"
)

THE_SURA_COUNT_IS_NOT_IN_THESE_BYTES: Final[str] = (
    "المدوّنةُ المودَعةُ سطرٌ لكلّ آيةٍ بلا حقلِ سورةٍ ولا حقلِ آية، فعددُ "
    "السور 114 غيرُ مقيسٍ ههنا: لا مُصدَّقًا ولا مُكذَّبًا"
)


@dataclass(frozen=True, slots=True)
class TranscribedRow:
    """صفٌّ واردٌ كما وصل: عنوانُه، ودليلُه المذكور، ورقمُه — بلا تبنٍّ."""

    tool: ThinkingTool
    stated_evidence: str
    stated_figure: int

    def __post_init__(self) -> None:
        if self.stated_figure < 0:
            raise ThinkingToolsCensusError("رقمٌ سالبٌ لا يُودَع.")
        if not self.stated_evidence.strip():
            raise ThinkingToolsCensusError("صفٌّ بلا دليلٍ مذكورٍ لا يُودَع.")


THE_TRANSCRIBED_TABLE: Final[tuple[TranscribedRow, ...]] = (
    TranscribedRow(ThinkingTool.ANALOGY, "«ضرب الله مثلًا» · «مثل الذين»", 112),
    TranscribedRow(
        ThinkingTool.EXHAUSTIVE_CHALLENGE, "«فأتوا بسورةٍ مثله» · «فادعوا»", 366
    ),
    TranscribedRow(
        ThinkingTool.SENSORY_INFERENCE, "«ألم ترَ» · «أفلا ينظرون» · «أفرأيت»", 185
    ),
    TranscribedRow(ThinkingTool.SENSORY_IMAGERY, "«كأنّ» وصورها", 70),
    TranscribedRow(ThinkingTool.CERTAINTY, "أدوات التحقق", 440),
    TranscribedRow(ThinkingTool.CONJECTURE, "أدوات الظنّ", 174),
    TranscribedRow(ThinkingTool.RECKONING, "«يُحاسب» · «فليحاسب»", 33),
    TranscribedRow(ThinkingTool.EXHAUSTIVE_PRECISION, "«أحكم آياته» · «فصّلناه»", 18),
)
"""الجدولُ الواردُ بأرقامه، مُودَعًا لا مُتبنًّى؛ وصفُّ التصنيف في `NetworkReading`."""

THE_TRANSCRIBED_NETWORK: Final[tuple[int, int, int]] = (114, 6_236, 77_801)
"""شبكةُ الصفّ الأوّل كما وردت: سورةً فآيةً فكلمة."""


@dataclass(frozen=True, slots=True)
class ToolProbes:
    """مِجَسّاتُ أداةٍ، مكتوبةً مجرَّدةً من التشكيل، وغيرَ متداخلةٍ بالإنشاء."""

    tool: ThinkingTool
    probes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.probes:
            raise ThinkingToolsCensusError("أداةٌ بلا مِجَسٍّ لا تُقاس.")
        for probe in self.probes:
            if not probe.strip():
                raise ThinkingToolsCensusError("مِجَسٌّ خالٍ لا يُطابَق.")
            if strip_diacritics(probe) != probe:
                raise ThinkingToolsCensusError(f"مِجَسٌّ مشكولٌ لا يُطابِق نصًّا مجرَّدًا: {probe}")
        for probe in self.probes:
            for other in self.probes:
                if probe is not other and probe in other:
                    raise ThinkingToolsCensusError(
                        f"مِجَسٌّ متداخلٌ يُعَدُّ مرّتين: «{probe}» في «{other}»"
                    )


THE_TOOL_PROBES: Final[tuple[ToolProbes, ...]] = (
    ToolProbes(ThinkingTool.ANALOGY, ("مثل",)),
    ToolProbes(ThinkingTool.EXHAUSTIVE_CHALLENGE, ("فأتوا", "فادعوا")),
    ToolProbes(
        ThinkingTool.SENSORY_INFERENCE,
        ("ألم تر", "أفرأيت", "أفلا ينظرون", "أفلا يرون"),
    ),
    ToolProbes(ThinkingTool.SENSORY_IMAGERY, ("كأن",)),
    ToolProbes(ThinkingTool.CERTAINTY, ("يقين", "موقن")),
    ToolProbes(ThinkingTool.CONJECTURE, ("ظن", "زعم")),
    ToolProbes(ThinkingTool.RECKONING, ("حساب", "يحاسب", "حسيب")),
    ToolProbes(
        ThinkingTool.EXHAUSTIVE_PRECISION,
        ("أحكم", "محكم", "فصلنا", "فصلت", "مفصل"),
    ),
)
"""مِجَسّاتُ هذا القياس؛ وهي **قاعدتُنا المعلنة** لا قاعدةُ الجدول الوارد."""

THE_REFUSED_PROBES: Final[tuple[tuple[str, ThinkingTool, str], ...]] = (
    (
        "شك",
        ThinkingTool.CONJECTURE,
        "يُطابِق 80 وقوعًا، منها 15 فقط صورةُ «شك»؛ والباقي شكرٌ وشكلٌ وشكوى",
    ),
    (
        "وإن",
        ThinkingTool.EXHAUSTIVE_CHALLENGE,
        "أداةُ شرطٍ عامّةٌ لا تخصُّ التحدي، فمطابقتُها تقيس الشرطَ لا التحدي",
    ),
    (
        "الحق",
        ThinkingTool.CERTAINTY,
        "اسمٌ ووصفٌ ومصدرٌ في أبوابٍ شتّى، فليس مِجَسَّ تحقُّقٍ بل مِجَسُّ لفظ",
    ),
)
"""مِجَسّاتٌ خطرت فرُفِضت، ومعها سببُ الرفض مقيسًا — تُنشَر ولا تُطوى."""


@dataclass(frozen=True, slots=True)
class Contaminant:
    """صورةٌ دخلت المُطابِقَ وليست من الأداة، بعددِ وقوعها؛ مفتَّشةً بالعين."""

    tool: ThinkingTool
    surface: str
    occurrences: int
    note: str

    def __post_init__(self) -> None:
        if self.occurrences < 1:
            raise ThinkingToolsCensusError("ملوِّثٌ دون الوقوع الواحد لا يُنشَر.")


THE_NAMED_CONTAMINANTS: Final[tuple[Contaminant, ...]] = (
    Contaminant(ThinkingTool.CERTAINTY, "الفريقين", 3, "مثنّى «فريق» لا يقين فيه"),
    Contaminant(ThinkingTool.CERTAINTY, "والصديقين", 1, "جمعُ «صدّيق» لا يقين فيه"),
    Contaminant(ThinkingTool.CONJECTURE, "وحفظناها", 1, "من الحفظ لا من الظنّ"),
    Contaminant(ThinkingTool.CONJECTURE, "ويحفظن", 1, "من الحفظ لا من الظنّ"),
)
"""ملوِّثاتٌ مسمّاةٌ بأعيانها؛ وهي **دليلُ العلوّ** لا اعتذارٌ عنه."""


@dataclass(frozen=True, slots=True)
class ToolMeasurement:
    """ما خرج لأداةٍ من البايتات: وقوعًا، وآياتٍ، وصورًا متمايزة."""

    tool: ThinkingTool
    occurrences: int
    ayahs: int
    distinct_surfaces: int

    def __post_init__(self) -> None:
        if min(self.occurrences, self.ayahs, self.distinct_surfaces) < 0:
            raise ThinkingToolsCensusError("عددٌ سالبٌ لا يُنشَر.")
        if self.ayahs > self.occurrences:
            raise ThinkingToolsCensusError("آياتٌ فوق الوقوع لا تكون.")

    @property
    def named_contamination(self) -> int:
        """مجموعُ ما سُمِّي من الملوِّثات في هذه الأداة؛ ولا يُدَّعى استيعابُه."""

        return sum(
            item.occurrences
            for item in THE_NAMED_CONTAMINANTS
            if item.tool is self.tool
        )

    @property
    def floor_after_named_contamination(self) -> int:
        """الحدُّ الأدنى الباقي بعد طرح المسمّى؛ وما بينهما لم يُفتَّش."""

        return self.occurrences - self.named_contamination


@dataclass(frozen=True, slots=True)
class NetworkReading:
    """شبكةُ صفّ التصنيف مقيسةً: السورةُ غائبةٌ عن البايتات، والباقي مقيس."""

    suras: int | None
    ayah_lines: int
    whitespace_tokens: int

    def __post_init__(self) -> None:
        if self.ayah_lines < 1 or self.whitespace_tokens < 1:
            raise ThinkingToolsCensusError("شبكةٌ خاليةٌ لا تُنشَر.")

    @property
    def standing(self) -> ClaimStanding:
        """منزلةُ الصفّ: غيابُ السورة يحكم عليه قبل موافقة الآيات."""

        if self.suras is None:
            return ClaimStanding.NOT_IN_THESE_BYTES
        return ClaimStanding.REPRODUCED


def _bare_ayahs(path: Path | str | None = None) -> tuple[str, ...]:
    """آياتُ المدوّنة مجرَّدةً من التشكيل؛ سطرٌ غيرُ خالٍ = آية."""

    text = read_quran_corpus_bytes(path).decode("utf-8")
    return tuple(
        strip_diacritics(line.strip()) for line in text.split("\n") if line.strip()
    )


@lru_cache(maxsize=1)
def _cached_bare_ayahs() -> tuple[str, ...]:
    return _bare_ayahs()


def _probes_for(tool: ThinkingTool) -> tuple[str, ...]:
    for entry in THE_TOOL_PROBES:
        if entry.tool is tool:
            return entry.probes
    raise ThinkingToolsCensusError(f"أداةٌ بلا مِجَسّاتٍ مُعلَنة: {tool.value}")


def measure_tool(tool: ThinkingTool, path: Path | str | None = None) -> ToolMeasurement:
    """يُشغِّل مِجَسّاتِ الأداة على البايتات المبصومة ويُخرِج ما خرج."""

    probes = _probes_for(tool)
    ayahs = _cached_bare_ayahs() if path is None else _bare_ayahs(path)
    occurrences = 0
    matched_ayahs = 0
    surfaces: set[str] = set()
    for ayah in ayahs:
        hits = sum(ayah.count(probe) for probe in probes)
        if hits:
            occurrences += hits
            matched_ayahs += 1
            surfaces.update(
                token
                for token in ayah.split()
                if any(probe in token for probe in probes)
            )
    return ToolMeasurement(
        tool=tool,
        occurrences=occurrences,
        ayahs=matched_ayahs,
        distinct_surfaces=len(surfaces),
    )


def every_measurement(
    path: Path | str | None = None,
) -> tuple[ToolMeasurement, ...]:
    """قياسُ الأدوات الثماني التي لها مِجَسّات، بترتيب الجدول."""

    return tuple(measure_tool(entry.tool, path) for entry in THE_TOOL_PROBES)


def network_reading(path: Path | str | None = None) -> NetworkReading:
    """شبكةُ التصنيف: السورةُ `None` لأنّها ليست في البايتات، لا لأنّها صفر."""

    ayahs = _cached_bare_ayahs() if path is None else _bare_ayahs(path)
    return NetworkReading(
        suras=None,
        ayah_lines=len(ayahs),
        whitespace_tokens=sum(len(ayah.split()) for ayah in ayahs),
    )


def certainty_to_conjecture(path: Path | str | None = None) -> tuple[int, int]:
    """وقوعُ اليقين إلى وقوع الظنّ، رقمين خامّين بلا قسمةٍ مُعلَّبة."""

    certainty = measure_tool(ThinkingTool.CERTAINTY, path)
    conjecture = measure_tool(ThinkingTool.CONJECTURE, path)
    return certainty.occurrences, conjecture.occurrences


def standing_of(row: TranscribedRow, path: Path | str | None = None) -> ClaimStanding:
    """منزلةُ صفٍّ واردٍ بعد التشغيل؛ مشتقّةٌ من الرقمين لا مكتوبةٌ في حقل.

    وصفّا اليقين والظنّ يُحكَم عليهما بالاتجاه: إن كذّب المقيسُ ترتيبَ
    المنقول فالمنزلةُ `DIRECTION_INVERTED`، وهي أثقلُ من مجرّد الخلاف.
    """

    measured = measure_tool(row.tool, path)
    if row.tool in (ThinkingTool.CERTAINTY, ThinkingTool.CONJECTURE):
        certainty, conjecture = certainty_to_conjecture(path)
        transcribed_certainty_leads = _transcribed(
            ThinkingTool.CERTAINTY
        ) > _transcribed(ThinkingTool.CONJECTURE)
        if transcribed_certainty_leads != (certainty > conjecture):
            return ClaimStanding.DIRECTION_INVERTED
    if measured.occurrences == row.stated_figure:
        return ClaimStanding.REPRODUCED
    return ClaimStanding.DIVERGED


def _transcribed(tool: ThinkingTool) -> int:
    for row in THE_TRANSCRIBED_TABLE:
        if row.tool is tool:
            return row.stated_figure
    raise ThinkingToolsCensusError(f"صفٌّ غيرُ وارد: {tool.value}")


THINKING_TOOLS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "قاعدةُ الجدول الوارد": (
        "لم تصل، فأرقامُه الثمانيةُ غيرُ قابلةٍ لإعادة الاشتقاق ههنا؛ وما في "
        "هذه الوحدة قياسٌ بقاعدةٍ أخرى معلنة، لا إعادةُ اشتقاقٍ لقاعدته."
    ),
    "عددُ السور": (
        "لا حقلَ سورةٍ في البايتات المودَعة، فالـ114 خارجُ القياس ههنا؛ "
        "ويلزم لإدخاله إيداعُ مدوّنةٍ مُحقَّلةٍ مبصومةٍ أو سجلُّ حدودٍ للسور."
    ),
    "الترتيب الزمني": (
        "مكّيّ/مدنيّ وترتيبُ النزول ليسا في البايتات، فلا صفَّ لهما في الجدول "
        "لا بالإثبات ولا بالنفي."
    ),
    "الصورةُ ليست أداةَ تفكير": (
        "المقيسُ صورٌ سطحيّةٌ في رسمٍ مجرَّد؛ وحملُها على «أداة تفكير» تأويلٌ "
        "لم تدخله هذه الوحدة، ويلزمه وسمٌ نحويٌّ ودلاليٌّ غيرُ مودَعٍ ههنا."
    ),
    "استيعابُ الملوِّثات": (
        "المسمّى في `THE_NAMED_CONTAMINANTS` ما فُتِّش بالعين؛ فـ"
        "`floor_after_named_contamination` حدٌّ أدنى لا عددٌ منقّى."
    ),
}
"""ما لم تحسمه هذه الوحدة، مسمًّى ومعه شرطُ حسمه."""

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "birth",
    "certificate",
    "verdict_value",
    "proof",
    "authority",
)


def _assert_no_authority_field() -> None:
    """حارسٌ عند الاستيراد يمنع تسلُّلَ حقلِ سلطةٍ إلى هذه الأصناف لاحقًا."""

    for holder in (
        TranscribedRow,
        ToolProbes,
        Contaminant,
        ToolMeasurement,
        NetworkReading,
    ):
        for field in fields(holder):
            lowered = field.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise ThinkingToolsCensusError(
                        f"حقلٌ سلطويٌّ في {holder.__name__}: {field.name}"
                    )


_assert_no_authority_field()
