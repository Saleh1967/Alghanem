"""جسرُ رسمِ الجذور بين معجمين: قاعدةُ تحويلٍ وقواعدُ تطبيعٍ، بلا رقمٍ واحد.

**المانعُ الذي جاءت هذه الوحدةُ إليه**: سجّل `transitivity_lexicon_witness`
تحفّظَه باسمه `TheJoinWasNotTaken`: جذورُ مدوَّنة القرآن بترميز Buckwalter
وجذورُ المعاجم العربية بالعربية، فالتقاطعُ الحرفيُّ بينهما **صفرٌ مقيس**،
«ووصلُهما يستلزم جدولَ تحويلٍ وقرارَ توحيدِ همزة، وكلاهما **قاعدةٌ تُسَنّ**
لا قراءةٌ تُقرأ؛ فتُجمَّد قبل القياس في مواصفةٍ مستقلّة أو لا تُسَنّ».
وكرّره `masdar_priority_preregistration` باسم
`TheJoinBetweenTwoCorporaIsLegislatedNotRead`. وهذه الوحدةُ **المواصفةُ
المستقلّة** التي اشترطها التحفّظان: تُسَنّ فيها القاعدةُ وحدَها، ولا يُقاس بها
هنا شيء.

`THIS_MODULE_READS_NO_FILE_AND_EMITS_NO_COUNT`: لا تُفتَح في هذه الوحدة بايتاتٌ
ولا يخرج منها عدد. وذلك شرطٌ في صحّة القاعدة لا ترتيبٌ للملفّات: قاعدةٌ تُسَنّ
في الوحدة التي ترى رقمَها تُسَنّ على الرقم. وحارسٌ في آخرها يرفض إدخالَ حقلٍ
يحمل عددًا.

`THE_TRANSLITERATION_TABLE_IS_UPSTREAMS_NOT_OURS`: جدولُ Buckwalter مأخوذٌ من
توثيق مدوَّنة القرآن الصرفية نفسِها، على منوال
`TheMarksMeaningIsUpstreamsNotOurs` في `transitivity_lexicon_witness`. وفيه
**محارفُ الهمزة الستّةُ متمايزةٌ بأعيانها**: `'`=ء و`>`=أ و`<`=إ و`&`=ؤ
و`}`=ئ و`|`=آ، و`A`=ا **ألفًا عاريةً لا همزة**. فمن قرأ `A` همزةً مكتوبةً
ألفًا قرأ غيرَ هذا الجدول، ومن حوّل `Abd` إلى «أبد» أدخل همزةً ليست في
البايتات.

`NORMALISATION_IS_A_RULE_ENACTED_NOT_A_FACT_READ`: التطبيعُ **قرارٌ يُغيّر
الرقم**، لا خاصّيّةٌ تُقرأ من الحروف. ولذلك لا تُخرِج `normalise_root` صورةً
مُطبَّعةً مفردةً البتّة: تُخرِج الصورتين معًا (قبل/بعد) وأسماءَ القواعد التي
أُعمِلت فعلًا في هذه السلسلة، فلا يمرّ جذرٌ مُطبَّعٌ بلا سجلِّ تطبيعه.

`A_RULE_DESTROYS_A_DISTINCTION_THAT_WAS_IN_THE_BYTES`: كلُّ قاعدةٍ هنا تُسقِط
تمييزًا كان مكتوبًا. فلكلِّ قاعدةٍ حقلُ `what_it_destroys` بنصّه، وفيها
`fusions_under` تُخرِج **الأزواجَ التي انصهرت بعينها** — جذران متمايزان قبل
القاعدة صارا واحدًا بعدها — لا أثرَها الإجماليَّ وحدَه؛ فأثرٌ إجماليٌّ بلا
أعيانه يُقرأ خسارةً صغيرةً وهو لا يُعرَف.

`THE_HAMZA_TARGET_WAS_NOT_CHOSEN_HERE`: سُئل صاحبُ الطلب: أتُوحَّد الهمزةُ
إلى ألفٍ عاريةٍ (`ا`) أم إلى ألفٍ حاملةٍ (`أ`)؟ ولم يَرِد جواب. فلم تُختَر
واحدةٌ صامتًا: القاعدتان **مسنونتان كلتاهما** باسمين متمايزين، ويُخرَج بهما
عدّان، ويبقى الاختيارُ لصاحبه. واختيارُ قاعدةِ عدٍّ نيابةً عمّن لم يُجب يجعل
الرقمَ رقمَنا وهو يُقرأ رقمَه.

`AN_ORTHOGRAPHIC_RULE_IS_NOT_A_MORPHOLOGICAL_ONE`: `ى ← ي` و`ة ← ت` قاعدتان
**إملائيّتان**: الحرفان صورتان لمكتوبٍ واحدٍ في رسمين. أمّا `ا ← و` أو
`ا ← ي` في المعتلّ فقرارٌ **صرفيّ**: حسمٌ لهويّة العلّة، وهو بعينه ما سُجِّل
في `hollow_root_levels_deposit` تعارضًا مرتبتُه `THE_TREE_CANNOT_TEST_IT`.
فهو مرفوضٌ هنا بنصّه في `REFUSED_RULES`، ورفضُه مكتوبٌ ليُرى أنّه لم يُنسَ.

`NORMALISATION_IS_NOT_INVERTIBLE`: ليس في هذه الوحدة دالّةٌ تأخذ صورةً
مُطبَّعةً فتُرجِع رسمَها في معجمٍ بعينه، ولن تكون: القاعدةُ تجمع أكثرَ من
حرفٍ في حرف، فعكسُها اختيارٌ بين أصولٍ لا استخراجٌ لأصل. ومن قرأ صورةً
مُطبَّعةً رسمًا في معجمٍ أسنَد إلى المعجم ما ليس فيه. واختبارٌ يمسك إضافةَ
دالّةٍ عكسيّة.

وهذه الوحدة تشريعٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.

المصدر: مدوَّنة القرآن الصرفية، http://corpus.quran.com — وجدولُ الترميز من
توثيقها؛ والإسنادُ إليها شرطُ رخصةٍ لا لطفَ عبارة.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, fields
from typing import Final

__all__ = [
    "ALIF_MAQSURA_RULE",
    "AN_ORTHOGRAPHIC_RULE_IS_NOT_A_MORPHOLOGICAL_ONE_NOTE",
    "A_RULE_DESTROYS_A_DISTINCTION_THAT_WAS_IN_THE_BYTES_NOTE",
    "BUCKWALTER_TO_ARABIC",
    "HAMZA_CHARACTERS_IN_BUCKWALTER",
    "HAMZA_TO_BARE_ALIF_RULE",
    "HAMZA_TO_CARRIED_ALIF_RULE",
    "NORMALISATION_IS_A_RULE_ENACTED_NOT_A_FACT_READ_NOTE",
    "NORMALISATION_IS_NOT_INVERTIBLE_NOTE",
    "NORMALISATION_RULES",
    "REFUSED_RULES",
    "ROOT_ORTHOGRAPHY_BRIDGE_NAMED_RESIDUALS",
    "TA_MARBUTA_RULE",
    "THE_HAMZA_TARGET_WAS_NOT_CHOSEN_HERE_NOTE",
    "THE_TRANSLITERATION_TABLE_IS_UPSTREAMS_NOT_OURS_NOTE",
    "THIS_MODULE_READS_NO_FILE_AND_EMITS_NO_COUNT_NOTE",
    "FusionRecord",
    "NormalisationReadout",
    "NormalisationRule",
    "RefusedRule",
    "RootOrthographyBridgeError",
    "fusions_under",
    "normalise_root",
    "rule_by_name",
    "transliterate_root",
]


class RootOrthographyBridgeError(ValueError):
    """رفضٌ صريح: محرفٌ خارج الجدول، أو قاعدةٌ بلا نصٍّ، أو تطبيعٌ بلا سجلّ."""


THE_TRANSLITERATION_TABLE_IS_UPSTREAMS_NOT_OURS_NOTE: Final[str] = (
    "TheTransliterationTableIsUpstreamsNotOurs: جدولُ Buckwalter مأخوذٌ من "
    "توثيق مدوَّنة القرآن الصرفية، وفيه محارفُ الهمزة الستّةُ متمايزةٌ "
    "بأعيانها و`A` ألفٌ عاريةٌ لا همزة؛ فمن قرأ `A` همزةً قرأ غيرَ هذا الجدول"
)

NORMALISATION_IS_A_RULE_ENACTED_NOT_A_FACT_READ_NOTE: Final[str] = (
    "NormalisationIsARuleEnactedNotAFactRead: التطبيعُ قرارٌ يُغيّر الرقم لا "
    "خاصّيّةٌ تُقرأ؛ فلا تخرج صورةٌ مُطبَّعةٌ مفردةً، بل الصورتان معًا "
    "وأسماءُ القواعد التي أُعمِلت فعلًا"
)

A_RULE_DESTROYS_A_DISTINCTION_THAT_WAS_IN_THE_BYTES_NOTE: Final[str] = (
    "ARuleDestroysADistinctionThatWasInTheBytes: كلُّ قاعدةٍ تُسقِط تمييزًا "
    "كان مكتوبًا؛ فلها حقلُ ما تُتلفه بنصّه، وتُخرَج الأزواجُ المنصهرةُ "
    "بأعيانها لا أثرُها الإجماليُّ وحدَه"
)

THE_HAMZA_TARGET_WAS_NOT_CHOSEN_HERE_NOTE: Final[str] = (
    "TheHamzaTargetWasNotChosenHere: سُئل صاحبُ الطلب أتُوحَّد الهمزةُ إلى "
    "«ا» أم إلى «أ» فلم يُجب؛ فسُنّت القاعدتان كلتاهما ويُخرَج بهما عدّان، "
    "ولم تُختَر واحدةٌ نيابةً عنه — فاختيارُ قاعدةِ عدٍّ عمّن لم يُجب يجعل "
    "الرقمَ رقمَنا وهو يُقرأ رقمَه"
)

AN_ORTHOGRAPHIC_RULE_IS_NOT_A_MORPHOLOGICAL_ONE_NOTE: Final[str] = (
    "AnOrthographicRuleIsNotAMorphologicalOne: «ى ← ي» و«ة ← ت» صورتان "
    "لمكتوبٍ واحد، أمّا «ا ← و/ي» فحسمٌ لهويّة العلّة سُجِّل تعارضًا مرتبتُه "
    "`THE_TREE_CANNOT_TEST_IT`؛ فهو مرفوضٌ بنصّه لا متروكٌ سهوًا"
)

NORMALISATION_IS_NOT_INVERTIBLE_NOTE: Final[str] = (
    "NormalisationIsNotInvertible: القاعدةُ تجمع أكثرَ من حرفٍ في حرف، فعكسُها "
    "اختيارٌ بين أصولٍ لا استخراجٌ لأصل؛ ولا دالّةَ عكسيّةً هنا، ومن قرأ صورةً "
    "مُطبَّعةً رسمًا في معجمٍ أسنَد إليه ما ليس فيه"
)

THIS_MODULE_READS_NO_FILE_AND_EMITS_NO_COUNT_NOTE: Final[str] = (
    "ThisModuleReadsNoFileAndEmitsNoCount: لا بايتاتٍ تُفتَح هنا ولا عددَ "
    "يخرج؛ وقاعدةٌ تُسَنّ في الوحدة التي ترى رقمَها تُسَنّ على الرقم"
)

ROOT_ORTHOGRAPHY_BRIDGE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TheTransliterationTableIsUpstreamsNotOurs": (
        THE_TRANSLITERATION_TABLE_IS_UPSTREAMS_NOT_OURS_NOTE
    ),
    "NormalisationIsARuleEnactedNotAFactRead": (
        NORMALISATION_IS_A_RULE_ENACTED_NOT_A_FACT_READ_NOTE
    ),
    "ARuleDestroysADistinctionThatWasInTheBytes": (
        A_RULE_DESTROYS_A_DISTINCTION_THAT_WAS_IN_THE_BYTES_NOTE
    ),
    "TheHamzaTargetWasNotChosenHere": THE_HAMZA_TARGET_WAS_NOT_CHOSEN_HERE_NOTE,
    "AnOrthographicRuleIsNotAMorphologicalOne": (
        AN_ORTHOGRAPHIC_RULE_IS_NOT_A_MORPHOLOGICAL_ONE_NOTE
    ),
    "NormalisationIsNotInvertible": NORMALISATION_IS_NOT_INVERTIBLE_NOTE,
    "ThisModuleReadsNoFileAndEmitsNoCount": (
        THIS_MODULE_READS_NO_FILE_AND_EMITS_NO_COUNT_NOTE
    ),
}


BUCKWALTER_TO_ARABIC: Final[dict[str, str]] = {
    "'": "ء",
    "|": "آ",
    ">": "أ",
    "&": "ؤ",
    "<": "إ",
    "}": "ئ",
    "A": "ا",
    "b": "ب",
    "p": "ة",
    "t": "ت",
    "v": "ث",
    "j": "ج",
    "H": "ح",
    "x": "خ",
    "d": "د",
    "*": "ذ",
    "r": "ر",
    "z": "ز",
    "s": "س",
    "$": "ش",
    "S": "ص",
    "D": "ض",
    "T": "ط",
    "Z": "ظ",
    "E": "ع",
    "g": "غ",
    "f": "ف",
    "q": "ق",
    "k": "ك",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "h": "ه",
    "w": "و",
    "Y": "ى",
    "y": "ي",
}
"""جدولُ التحويل محرفًا بمحرف، حروفًا لا حركات؛ وخانةُ `ROOT` بلا حركات.

ومحارفُ الهمزة الستّةُ فيه بأعيانها، و`A` ألفٌ عاريةٌ؛ فالجدولُ وحدَه يفصل
في دعوى «عطل التحويل» متى قُوبِل بأبجدية الخانة كما هي.
"""

HAMZA_CHARACTERS_IN_BUCKWALTER: Final[tuple[str, ...]] = ("'", "|", ">", "&", "<", "}")
"""محارفُ الهمزة الستّةُ في الترميز؛ حضورُها في خانةٍ أو غيابُه واقعةٌ تُقاس."""


def transliterate_root(root: str) -> str:
    """يُحوِّل جذرًا من Buckwalter إلى العربية بالجدول المُعلَن، ولا يُطبِّع شيئًا.

    والمحرفُ الخارجُ عن الجدول يُرفَع به خطأٌ ولا يُمرَّر كما هو: تمريرُه
    يُخرِج جذرًا نصفُه عربيٌّ ونصفُه ASCII فيُعَدُّ غيرَ مطابقٍ بلا سبب.
    """

    if not isinstance(root, str) or not root:
        raise RootOrthographyBridgeError("الجذرُ المُحوَّلُ نصٌّ غيرُ فارغ.")
    letters: list[str] = []
    for character in root:
        arabic = BUCKWALTER_TO_ARABIC.get(character)
        if arabic is None:
            raise RootOrthographyBridgeError(
                f"محرفٌ خارجَ جدول التحويل المُعلَن: {character!r} في {root!r}"
            )
        letters.append(arabic)
    return "".join(letters)


@dataclass(frozen=True, slots=True)
class NormalisationRule:
    """قاعدةُ تطبيعٍ واحدة: اسمُها ونصُّها وخريطتُها وما تُتلفه من تمييز."""

    name: str
    statement: str
    mapping: tuple[tuple[str, str], ...]
    what_it_destroys: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ القاعدة"),
            (self.statement, "نصُّ القاعدة"),
            (self.what_it_destroys, "ما تُتلفه القاعدة"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise RootOrthographyBridgeError(
                    f"{label} نصٌّ غيرُ فارغ؛ وقاعدةٌ بلا نصٍّ تُقرأ بعد جلساتٍ "
                    "على غير ما سُنَّت له"
                )
        if not self.mapping:
            raise RootOrthographyBridgeError("قاعدةٌ بلا خريطةِ محارفَ لا تُطبِّق شيئًا.")
        sources = [source for source, _ in self.mapping]
        if len(set(sources)) != len(sources):
            raise RootOrthographyBridgeError("محرفٌ مصدرٌ مكرَّرٌ في خريطةٍ واحدة.")
        for source, target in self.mapping:
            if len(source) != 1 or len(target) != 1:
                raise RootOrthographyBridgeError("الخريطةُ محرفٌ واحدٌ بمحرفٍ واحد.")
            if source == target:
                raise RootOrthographyBridgeError(
                    "محرفٌ يُطبَّع إلى نفسه ليس قاعدةً، وهو يُوهِم أثرًا لا يقع."
                )

    def apply_to(self, form: str) -> str:
        """تُطبِّق خريطةَ القاعدة على صورةٍ، ولا تُخرَج نتيجتُها وحدَها للقارئ."""

        table = dict(self.mapping)
        return "".join(table.get(character, character) for character in form)

    def changes(self, form: str) -> bool:
        """هل تُغيّر هذه القاعدةُ هذه الصورةَ فعلًا؟ عليه يدور سجلُّ الإعمال."""

        return self.apply_to(form) != form


HAMZA_TO_BARE_ALIF_RULE: Final[NormalisationRule] = NormalisationRule(
    name="همزة_إلى_ألف_عارية",
    statement=(
        "كلُّ محارف الهمزة — أ إ آ ؤ ئ ء — تصير ألفًا عاريةً «ا» حيثما وقعت "
        "من الجذر: أوّلَه ووسطَه وآخرَه سواء، فلا يُفرَّق بينها بالموضع"
    ),
    mapping=(("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ؤ", "ا"), ("ئ", "ا"), ("ء", "ا")),
    what_it_destroys=(
        "تمييزَ الهمزة من الألف، وتمييزَ حواملها بعضِها من بعض: «أبد» و«ابد» "
        "يصيران واحدًا، و«سأل» و«سال» يصيران واحدًا وهما جذران متمايزان في "
        "العربية؛ فهذه القاعدةُ أوسعُ إتلافًا من أختها"
    ),
)

HAMZA_TO_CARRIED_ALIF_RULE: Final[NormalisationRule] = NormalisationRule(
    name="همزة_إلى_ألف_حاملة",
    statement=(
        "كلُّ محارف الهمزة — إ آ ؤ ئ ء — تصير ألفًا حاملةً «أ» حيثما وقعت، "
        "وتبقى الألفُ العاريةُ «ا» متمايزةً عنها"
    ),
    mapping=(("إ", "أ"), ("آ", "أ"), ("ؤ", "أ"), ("ئ", "أ"), ("ء", "أ")),
    what_it_destroys=(
        "تمييزَ حوامل الهمزة بعضِها من بعض، ويُبقي تمييزَ المهموز من الألف؛ "
        "فمعجمٌ يكتب «ا» ومعجمٌ يكتب «أ» يبقيان مفترقين تحتها"
    ),
)

ALIF_MAQSURA_RULE: Final[NormalisationRule] = NormalisationRule(
    name="ألف_مقصورة_إلى_ياء",
    statement="الألفُ المقصورةُ «ى» تصير ياءً «ي» حيثما وقعت من الجذر",
    mapping=(("ى", "ي"),),
    what_it_destroys=(
        "تمييزَ رسمين لمكتوبٍ واحد؛ ولا يُقرأ منها حسمٌ لهويّة العلّة، فالياءُ "
        "هنا رسمٌ لا حكمٌ على أصل الحرف"
    ),
)

TA_MARBUTA_RULE: Final[NormalisationRule] = NormalisationRule(
    name="تاء_مربوطة_إلى_تاء",
    statement="التاءُ المربوطةُ «ة» تصير تاءً مبسوطةً «ت» حيثما وقعت",
    mapping=(("ة", "ت"),),
    what_it_destroys=(
        "تمييزَ رسمي التاء؛ وأثرُها على جذور «مقاييس» **صفرٌ مقيس** إذ لا "
        "ترد «ة» في عمود `root_full` البتّة، وهي واقعةٌ تُثبَّت في الاختبار "
        "لا تُفترَض — فالقاعدةُ تُعلَن ولو لم تعمل، إذ سكوتُها عن جدولٍ ليس "
        "سكوتًا عن كلّ جدول"
    ),
)

NORMALISATION_RULES: Final[tuple[NormalisationRule, ...]] = (
    HAMZA_TO_BARE_ALIF_RULE,
    HAMZA_TO_CARRIED_ALIF_RULE,
    ALIF_MAQSURA_RULE,
    TA_MARBUTA_RULE,
)
"""القواعدُ المسنونةُ بأعيانها؛ وقاعدتا الهمزة متعارضتان فلا تُجمَعان في سلسلة."""


@dataclass(frozen=True, slots=True)
class RefusedRule:
    """قاعدةٌ نُظِر فيها فرُدَّت: نصُّها وسببُ ردِّها وما يلزم لِتُسَنّ."""

    name: str
    statement: str
    why_it_is_refused: str
    what_would_admit_it: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ القاعدة المردودة"),
            (self.statement, "نصُّها"),
            (self.why_it_is_refused, "سببُ الردّ"),
            (self.what_would_admit_it, "شرطُ قبولها"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise RootOrthographyBridgeError(f"{label} نصٌّ غيرُ فارغ.")


REFUSED_RULES: Final[tuple[RefusedRule, ...]] = (
    RefusedRule(
        name="ألف_إلى_واو_أو_ياء",
        statement="الألفُ «ا» في وسط الجذر تصير واوًا أو ياءً توحيدًا للمعتلّ",
        why_it_is_refused=(
            "هذا حسمٌ لهويّة العلّة لا توحيدُ رسم، وهو التعارضُ المُسجَّلُ في "
            "`hollow_root_levels_deposit` مرتبتُه `THE_TREE_CANNOT_TEST_IT`: "
            "«خوف» و«خيف» مدخلان مستقلّان في «مقاييس»، فالهيكلُ يُرجِع "
            "الاحتمالين معًا. وقاعدةٌ تختار أحدَهما تُنشئ تطابقًا وتسمّيه قياسًا"
        ),
        what_would_admit_it=(
            "شاهدٌ خارجَ الصورة السطحية يُسنِد هويّةَ العلّة إسنادًا مُبصَّمًا، "
            "وهو الشرطُ المكتوبُ هناك قبل هذه الوحدة؛ ولا يُغني عنه رجحانُ رسمٍ "
            "في جدول"
        ),
    ),
    RefusedRule(
        name="حذف_التضعيف",
        statement="الجذرُ المضاعفُ «مدد» يُردّ إلى «مد» حذفًا لتكرار اللام",
        why_it_is_refused=(
            "تبديلُ عدد حروف الجذر يُغيّر نوعَه، و`root_type` في «مقاييس» يفصل "
            "«مضاعف» من «ثلاثي» بنصّه؛ فقاعدةٌ تُذيب الفصلَ تُبدِّل المعدودَ "
            "لا رسمَه"
        ),
        what_would_admit_it=(
            "قرارٌ مُعلَنٌ بأنّ المعدودَ هيكلُ الجذر لا الجذرُ، يُجمَّد قبل "
            "القياس ويُخرَج معه العدُّ القديمُ بجنبه"
        ),
    ),
)
"""قواعدُ نُظِر فيها فرُدَّت؛ ورفضٌ مكتوبٌ يُرى، ورفضٌ مسكوتٌ عنه يُقرأ سهوًا."""


def rule_by_name(name: str) -> NormalisationRule:
    """القاعدةُ باسمها؛ ولا تُصطنَع قاعدةٌ ليُطابَق بها رقم."""

    for rule in NORMALISATION_RULES:
        if rule.name == name:
            return rule
    raise RootOrthographyBridgeError(f"لا قاعدةَ تطبيعٍ بهذا الاسم: {name}")


@dataclass(frozen=True, slots=True)
class NormalisationReadout:
    """سجلُّ تطبيعٍ واحد: الصورتان معًا، والقواعدُ المعروضةُ والمُعمَلةُ منها.

    ولا يُخرَج من هذه الوحدة نصٌّ مُطبَّعٌ مجرَّدًا عن هذا السجلّ: صورةٌ بلا
    سجلِّ تطبيعها تُقرأ بعد جلساتٍ صورةً في معجمها.
    """

    before: str
    after: str
    offered_rules: tuple[str, ...]
    applied_rules: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.before, str) or not self.before:
            raise RootOrthographyBridgeError("الصورةُ قبل التطبيع نصٌّ غيرُ فارغ.")
        if not isinstance(self.after, str) or not self.after:
            raise RootOrthographyBridgeError("الصورةُ بعد التطبيع نصٌّ غيرُ فارغ.")
        if len(set(self.offered_rules)) != len(self.offered_rules):
            raise RootOrthographyBridgeError("قاعدةٌ مكرَّرةٌ في السلسلة المعروضة.")
        for name in self.applied_rules:
            if name not in self.offered_rules:
                raise RootOrthographyBridgeError(
                    f"قاعدةٌ مُعمَلةٌ خارجَ المعروض: {name}؛ والسجلُّ لا يُخالف سلسلتَه."
                )
        if (self.before != self.after) != bool(self.applied_rules):
            raise RootOrthographyBridgeError(
                "سجلٌّ يقول تغييرًا بلا قاعدةٍ مُعمَلة، أو قاعدةً مُعمَلةً بلا "
                "تغيير؛ وكلاهما يُخفي أيَّ قاعدةٍ غيَّرت الرقم."
            )

    @property
    def was_changed(self) -> bool:
        """هل غيَّر التطبيعُ هذه الصورةَ؟ لا يُستدَلّ عليه بمقارنةٍ من القارئ."""

        return self.before != self.after


def normalise_root(
    form: str, rules: Iterable[NormalisationRule]
) -> NormalisationReadout:
    """يُطبِّق سلسلةَ قواعدَ مُعلَنةً، ويُخرِج الصورتين معًا وسجلَّ ما أُعمِل.

    والسلسلةُ تُمرَّر صريحةً بترتيبها، ولا سلسلةَ ضمنيّةٌ افتراضيّة: قاعدةٌ
    تُعمَل بلا أن تُطلَب تُغيّر الرقمَ بلا أن تُرى.
    """

    if not isinstance(form, str) or not form:
        raise RootOrthographyBridgeError("الصورةُ المُطبَّعةُ نصٌّ غيرُ فارغ.")
    chain = tuple(rules)
    names = tuple(rule.name for rule in chain)
    if len(set(names)) != len(names):
        raise RootOrthographyBridgeError("قاعدةٌ مكرَّرةٌ في السلسلة الممرَّرة.")
    if HAMZA_TO_BARE_ALIF_RULE in chain and HAMZA_TO_CARRIED_ALIF_RULE in chain:
        raise RootOrthographyBridgeError(
            "قاعدتا الهمزة متعارضتان: إحداهما تُذيب الألفَ في الهمزة والأخرى "
            "تُبقيها؛ فجمعُهما يُخرِج صورةً لا قاعدةَ لها."
        )
    current = form
    applied: list[str] = []
    for rule in chain:
        stepped = rule.apply_to(current)
        if stepped != current:
            applied.append(rule.name)
        current = stepped
    return NormalisationReadout(
        before=form,
        after=current,
        offered_rules=names,
        applied_rules=tuple(applied),
    )


@dataclass(frozen=True, slots=True)
class FusionRecord:
    """انصهارٌ واحد: صورةٌ مُطبَّعةٌ اجتمع عليها أكثرُ من جذرٍ متمايزٍ قبلها."""

    normalised: str
    sources: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.normalised, str) or not self.normalised:
            raise RootOrthographyBridgeError("الصورةُ المُطبَّعةُ نصٌّ غيرُ فارغ.")
        if len(self.sources) < 2:
            raise RootOrthographyBridgeError(
                "الانصهارُ اجتماعُ اثنين فأكثر؛ وواحدٌ ليس انصهارًا."
            )
        if len(set(self.sources)) != len(self.sources):
            raise RootOrthographyBridgeError("مصدرٌ مكرَّرٌ في انصهار.")
        if tuple(sorted(self.sources)) != self.sources:
            raise RootOrthographyBridgeError(
                "مصادرُ الانصهار مرتَّبةٌ ترتيبًا واحدًا، فلا يختلف سجلّان "
                "بترتيبِ مدخلاتهما."
            )

    @property
    def lost_distinctions(self) -> int:
        """عددُ التمييزات التي أتلفها هذا الانصهار: مصادرُه إلّا واحدًا."""

        return len(self.sources) - 1


def fusions_under(
    forms: Iterable[str], rules: Iterable[NormalisationRule]
) -> tuple[FusionRecord, ...]:
    """الأزواجُ المنصهرةُ بأعيانها تحت سلسلةٍ مُعلَنة، مرتَّبةً ترتيبًا واحدًا.

    وهذا هو ثمنُ التطبيع معروضًا: كم جذرًا متمايزًا في البايتات صار جذرًا
    واحدًا بالقاعدة، وأيُّها بعينه. وتقليصُ العدد وحدَه يُخفي أنّ الثمنَ
    وقع على جذورٍ مُسمّاة.
    """

    chain = tuple(rules)
    groups: dict[str, set[str]] = {}
    for form in forms:
        readout = normalise_root(form, chain)
        groups.setdefault(readout.after, set()).add(form)
    return tuple(
        FusionRecord(normalised=normalised, sources=tuple(sorted(sources)))
        for normalised, sources in sorted(groups.items())
        if len(sources) > 1
    )


def _assert_the_bridge_carries_no_count() -> None:
    forbidden = {"count", "total", "figure", "percentage", "عدد"}
    for carrier in (NormalisationRule, NormalisationReadout, RefusedRule):
        for field in fields(carrier):
            for word in field.name.split("_"):
                if word in forbidden:
                    raise RootOrthographyBridgeError(
                        f"`{field.name}` حقلٌ يحمل عددًا في وحدةِ تشريع؛ "
                        "والقاعدةُ تُسَنّ قبل الرقم لا معه."
                    )


_assert_the_bridge_carries_no_count()
