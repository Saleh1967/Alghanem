"""تسجيلٌ مسبقٌ لبطاقة الجملة الواحدة: تسعةَ عشرَ بندًا، ومرجعٌ واحدٌ لكلّ بند.

**وحدةُ التحليل هنا جديدةٌ ولا تُقرأ امتدادًا صامتًا لما قبلها**
(`SentenceIsNotALexeme`): الشهاداتُ الصوريةُ الأربعُ القائمة — `word_class_formal`
و`kulli_juzi_formal` و`lafz_madlul_relation_formal` و`madlul_alone_formal` —
وحدةُ التصنيف فيها **لفظٌ مفردٌ أو عنقودُ ألفاظ**، لا تركيبٌ إسناديّ. والبطاقةُ
المُسجَّلة هنا تُصنِّف **جملةً**، فبنودُها التي تخصّ الكلمات تُساق على كلمات
الجملة واحدةً واحدة، وبنودُها التي تخصّ التركيب لا شهادةَ لها اليوم. وقراءةُ
ذلك توسعةً للشهادات المفردة تُسقط الفارقَ بين الجنسين تحت اسمٍ واحد، وهو عينُ ما
تمنعه تلك الوحداتُ في نفسها.

**والتسجيلُ ليس شهادة** (`CardIsNotACertificate`)، على منوال
`compound_layer_preregistration.py` حرفًا بحرف: لا دالّةَ قرارٍ هنا، ولا مجالَ
مقبولًا، ولا شاهدًا واحدًا، ولا حقلَ نتيجةٍ البتّة — وحارسٌ عند الاستيراد يمنع
تسلّلَ حقلٍ كهذا لاحقًا. وكلُّ ما يفعله أنه **يُجمّد بطاقةَ الأسئلة قبل جوابها**.

**ومرجعٌ واحدٌ مُجمَّدٌ لكلّ بند** (`OneFrozenReferencePerItem`): مفردةُ المراجع
ثلاثيةٌ مغلقة (الشخصية الإسلامية ج٣، ولسان العرب، والنحو الواضح)، ولكلّ بندٍ
مرجعٌ واحدٌ لا أكثر. وتعدُّدُ المراجع في البند الواحد يفتح بابَ انتقاءِ المصدر
بعد رؤية الجواب، وهو ما يُبطِل التسجيلَ المسبق من أصله.

**وموقفُ البند رباعيّ**: بندٌ **مُشتَقٌّ من شهادةٍ قائمة** يُسمّي وحدتَها بمسارها،
ووجودُ الوحدة **يُقرأ من الشجرة** لا يُكتَب (على منوال `pipeline_stations`)؛ وبندٌ
**مؤجَّلٌ بقانونٍ مُسمّى**، وهو ما وقع لبندَي طبقة المركّب؛ وبندٌ **ينتظر نصًّا
مصدريًّا** لم يُقدَّم في هذه الشجرة؛ وبندٌ **زُوِّد نصُّه المصدريُّ بحروفه ولا
شهادةَ صوريةَ له**، وهو العضوُ الرابع الذي فتحته حالةٌ وقعت فعلًا حين نُقِلت
نصوصُ الجزء الثالث ومقطعان من مادة (ن و ر). ولا قيمةَ خامسة اسمُها «مُنجَز»،
لأنّ الإنجازَ شهادةٌ لا موقفُ تسجيل.

**وستّةُ بنودٍ من التسعةَ عشرَ تنتظر نصًّا، وأربعةٌ زُوِّدت نصوصُها بلا شهادة،
وبندان مؤجَّلان — وهذه نتيجةٌ لا عطل** (`IncompleteCardIsTheResultNotADefect`).
فالبطاقةُ التي تُملأ خاناتُها كلُّها اليوم إنما تُملأ بغير سند. **وتزويدُ النصّ
ليس شهادة** (`SuppliedTextIsNotAFormalCertificate`): بندٌ زُوِّد نصُّه يبقى غيرَ
مقروءٍ في أيّ بطاقة حتى يقوم له مجالٌ مُجمَّدٌ ودالّةُ قرارٍ وشاهدٌ لكلّ فرع.

**وترتيبُ التبعية مُشتَقٌّ لا مكتوب**: لكلّ بندٍ مخروطُ شرطٍ مُشتَقّ، ومن كتب
شرطًا يخالف المُشتَقّ رُدَّ عند الإنشاء، ومن سجّل بندًا قبل شرطه رُدَّ كذلك.

**ولا حكمَ فركتاليًّا (Φ)** (`OneCardOnThreeSentencesIsNotFractality`): كونُ
البطاقة الواحدة تُساق على جملةٍ اسميةٍ وفعليةٍ وشبهِ جملة لا يُثبِت فركتاليّةً؛
تكرارُ البنية ليس دليلَها، وهو عينُ
`IDENTICAL_STOP_GENUS_IS_NOT_FRACTAL_EVIDENCE_NOTE` في
`level_two_discrimination.py`.

**خمولٌ سلطويّ**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا `E0`، ولا تدخل هذه
المخرجاتُ في `BirthExperimentSpecification`، ولا تقرؤها بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .compound_layer_preregistration import NamedRefusal
from .pipeline_stations import ARABIC_PACKAGE_RELATIVE_PATH, repository_root_path

__all__ = [
    "CARD_AUTHORITY_NOTE",
    "CARD_IS_NOT_A_CERTIFICATE_NOTE",
    "CARD_SCOPE_NOTE",
    "CARD_SUCCESS_TITLE_IS_WITHHELD",
    "FRACTAL_VERDICT_IS_NOT_ISSUED_HERE_NOTE",
    "INCOMPLETE_CARD_IS_THE_RESULT_NOTE",
    "NAMED_REFUSALS",
    "NAMED_RESIDUALS",
    "ONE_FROZEN_REFERENCE_PER_ITEM_NOTE",
    "PARALLEL_FRONT_READING_NOTE",
    "SENTENCE_CARD_PREREGISTRATION",
    "SENTENCE_IS_NOT_A_LEXEME_NOTE",
    "SUPPLIED_TEXT_IS_NOT_A_CERTIFICATE_NOTE",
    "CardItem",
    "CardItemRegistration",
    "CardItemSupportReading",
    "FrozenReference",
    "ItemStanding",
    "SentenceCardPreregistration",
    "SentenceCardPreregistrationError",
    "SupportCoding",
    "derived_prerequisites",
    "read_item_support",
]


class SentenceCardPreregistrationError(ValueError):
    """رُفض مدخلٌ خارج التسجيل المُجمَّد؛ لا يُحمَل على أقرب حالة."""


class CardItem(Enum):
    """بنودُ البطاقة التسعةَ عشرَ المغلقة، بترتيب الطلب؛ لا عشرين لها هنا."""

    WORD_CLASS = "اسم_فعل_حرف"
    IRAB_MARK = "العلامة_الإعرابية"
    MURAB_MABNI = "معرب_مبني"
    JAMID_MUSHTAQ = "جامد_مشتق"
    KULLI_JUZI = "كلي_جزئي"
    LAFZ_MADLUL_RELATION = "متباين_مشترك_مشكك_مترادف_منقول"
    HAQIQA_MAJAZ = "حقيقة_مجاز"
    MUTABAQA_TADAMMUN_ILTIZAM = "مطابقة_تضمن_التزام"
    DAL_ALONE = "الدال_وحده"
    MADLUL_ALONE = "المدلول_وحده"
    DAL_MADLUL_COUPLING = "اقتران_الدال_والمدلول"
    WAZN = "الوزن"
    ISHTIQAQ_SARF = "الاشتقاق_والصرف"
    AMIL_MAMUL = "العامل_والمعمول"
    NISAB_TADMIN_TAQYID = "النسب_الإسنادية_والتضمين_والتقييد"
    MAQAM = "المقام"
    KHABAR_INSHA = "خبري_إنشائي"
    MANTUQ_MAFHUM = "منطوق_مفهوم"
    IFADA = "الإفادة"


class FrozenReference(Enum):
    """المراجعُ الثلاثةُ المُجمَّدة؛ لكلّ بندٍ واحدٌ منها لا أكثر."""

    SHAKHSIYYA_THREE = "الشخصية_الإسلامية_ج٣"
    LISAN_AL_ARAB = "لسان_العرب"
    AL_NAHW_AL_WADIH = "النحو_الواضح"


class ItemStanding(Enum):
    """موقفُ البند اليوم؛ رباعيٌّ مغلق، ولا عضوَ فيه اسمُه «مُنجَز».

    والعضوُ الرابع `SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE` فُتِح لحالةٍ وقعت
    فعلًا فلم تَسَعها الثلاثيةُ الأولى: بندٌ **زُوِّد نصُّه المصدريُّ بحروفه**
    فلم يعد ينتظر نقلًا، ولا وحدةَ صوريةً يُشتَقّ منها، ولا قانونَ تأجيلٍ
    يحجبه. وجمعُه مع `AWAITING_SOURCE_TEXT` يُخفي تزويدًا وقع، وجمعُه مع
    `DERIVED_FROM_EXISTING_CERTIFICATE` يقرأ نصًّا منقولًا شهادةً صورية؛ وكلاهما
    خلطُ جنسين تحت اسم. وهو **ليس «مُنجَزًا»**: الإنجازُ شهادةٌ لا موقفُ تسجيل.
    """

    DERIVED_FROM_EXISTING_CERTIFICATE = "مُشتَقّ_من_شهادة_قائمة"
    DEFERRED_BY_NAMED_LAW = "مؤجَّل_بقانونٍ_مُسمّى"
    AWAITING_SOURCE_TEXT = "ينتظر_نصًّا_مصدريًّا"
    SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE = "نصٌّ_مُزوَّدٌ_بلا_شهادة_صورية"


class SupportCoding(Enum):
    """حالُ ترميز وحدة البند، مُشتقّةً من الشجرة لا مكتوبةً."""

    CODED = "مُرمَّزة"
    NOT_CODED = "وحدة_غير_مُرمَّزة"
    NO_MODULE_DECLARED = "لا_وحدة_مُعلَنة"


SENTENCE_IS_NOT_A_LEXEME_NOTE: Final[str] = (
    "SentenceIsNotALexeme: وحدةُ التصنيف في الشهادات الصورية القائمة لفظٌ مفردٌ "
    "أو عنقودُ ألفاظ، ووحدةُ هذه البطاقة جملة؛ فقراءةُ البطاقة توسعةً لتلك "
    "الشهادات تُسقط فارقًا بين جنسين تحت اسمٍ واحد"
)

CARD_IS_NOT_A_CERTIFICATE_NOTE: Final[str] = (
    "CardIsNotACertificate: لا دالّةَ قرارٍ في هذا التسجيل، ولا مجالَ مقبولًا، "
    "ولا شاهدًا واحدًا، ولا برهان؛ ومن قرأه شهادةً فقد قرأ ما ليس فيه"
)

ONE_FROZEN_REFERENCE_PER_ITEM_NOTE: Final[str] = (
    "OneFrozenReferencePerItem: لكلّ بندٍ مرجعٌ واحدٌ مُجمَّدٌ من مفردةٍ ثلاثيةٍ "
    "مغلقة؛ وتعدُّدُ المراجع في البند الواحد يفتح بابَ انتقاء المصدر بعد رؤية "
    "الجواب فيُبطِل التسجيلَ المسبق من أصله"
)

INCOMPLETE_CARD_IS_THE_RESULT_NOTE: Final[str] = (
    "IncompleteCardIsTheResultNotADefect: بندٌ بلا نصٍّ مصدريّ يُسجَّل موقفًا "
    "مُسمًّى لا خانةً فارغة؛ وعدمُ اكتمال البطاقة نتيجةٌ تُقرأ لا عطلٌ يُستدرَك"
)

FRACTAL_VERDICT_IS_NOT_ISSUED_HERE_NOTE: Final[str] = (
    "OneCardOnThreeSentencesIsNotFractality: سَوقُ البطاقة الواحدة على جملةٍ "
    "اسميةٍ وفعليةٍ وشبهِ جملة لا يُثبِت فركتاليّةً ولا ينفيها؛ تكرارُ البنية "
    "ليس دليلَها"
)

SUPPLIED_TEXT_IS_NOT_A_CERTIFICATE_NOTE: Final[str] = (
    "SuppliedTextIsNotAFormalCertificate: تزويدُ نصٍّ مصدريٍّ يرفع نقصَ النقل "
    "وحده؛ ولا يُنشئ مجالًا مُجمَّدًا ولا دالّةَ قرارٍ ولا حاملًا يُشتَقّ منه، "
    "فالبندُ المُزوَّدُ نصُّه يبقى غيرَ مقروءٍ في البطاقة كما كان"
)

PARALLEL_FRONT_READING_NOTE: Final[str] = (
    "ParallelFrontIsNotABlockedFront: `NoRicherStructureBeforeLowerOpenResidual"
    "Closure` يحجب الفحصَ على مخروط الشرط `Down_E(q)` وحده لا على كلّ عملٍ في "
    "الشجرة. وبطاقةُ الجملة لا تستهلك مُخرَجَ تجربة «سائمة الغنم» ولا تُستهلَك "
    "فيها، وبنودُها القابلةُ للاشتقاق تُعيد استعمال شهاداتٍ مُجمَّدةٍ قبلهما "
    "معًا، وبنودُ طبقة المركّب — وهي وحدها «الأغنى» — مؤجَّلةٌ بقانونها. فهذه "
    "جبهةٌ غيرُ قابلةٍ للمقارنة (∥) لا جبهةٌ محجوبة؛ والقراءةُ مُسجَّلةٌ هنا "
    "بنصّها لتُفنَّد إن كانت خطأً، لا مطويّةٌ في نيّة"
)

CARD_SCOPE_NOTE: Final[str] = (
    "هذه الوحدة تُجمّد بطاقةَ الأسئلة قبل جوابها ولا تُجيبها: لا مجال صوريّ "
    "فيها، ولا دالّة قرار، ولا حوامل، ولا شواهد، ولا برهان"
)

CARD_AUTHORITY_NOTE: Final[str] = (
    "Preregistration != Certificate، و FormalClassification != BirthVerdict: لا "
    "نوع في kernel، ولا Freeze، ولا E0، ولا بوّابة نواة تقرأ هذه المخرجات، ولا "
    "تدخل في BirthExperimentSpecification"
)

CARD_SUCCESS_TITLE_IS_WITHHELD: Final[str] = (
    "لا عنوان نجاح لهذه الوحدة: التسجيل المسبق ليس شهادة، ولا يصير شهادةً إلا "
    "بمجالٍ مُجمَّد ودالّة قرارٍ كلّية وشاهدٍ مُثبَتٍ بنصّه لكل فرع"
)

_MODULE_REQUIRED_REFUSAL: Final[str] = (
    "البندُ المُشتَقُّ من شهادةٍ قائمة يُسمّي وحدتَها بمسارها، ولا يُسمّي قانونًا "
    "مؤجِّلًا؛ فالاشتقاقُ من وحدةٍ لا يكون تأجيلًا بقانون"
)

_LAW_REQUIRED_REFUSAL: Final[str] = (
    "البندُ المؤجَّلُ يُسمّي قانونَ تأجيله، ولا يُسمّي وحدةً يُشتَقّ منها؛ "
    "وتأجيلٌ بلا اسمِ قانونٍ تأجيلٌ بلا حجّة"
)

_AWAITING_REFUSAL: Final[str] = (
    "البندُ الذي ينتظر نصًّا مصدريًّا لا وحدةَ له ولا قانونَ تأجيل ولا مفتاحَ "
    "نصٍّ مُزوَّد: نقصُه في النقل لا في السلطة، وخلطُ الأجناس يُخفي أيَّها "
    "يُرفَع بالنصّ"
)

_SUPPLIED_KEY_REQUIRED_REFUSAL: Final[str] = (
    "البندُ الذي زُوِّد نصُّه يُسمّي مفتاحَ ذلك النصّ في "
    "`sentence_card_source_texts`، ولا يُسمّي وحدةً صوريةً ولا قانونَ تأجيل؛ "
    "فالنقلُ المُزوَّد ليس شهادةً ولا حجبًا"
)

_DERIVED_PREREQUISITES: Final[dict[CardItem, tuple[CardItem, ...]]] = {
    CardItem.WORD_CLASS: (),
    CardItem.IRAB_MARK: (CardItem.WORD_CLASS,),
    CardItem.MURAB_MABNI: (CardItem.WORD_CLASS,),
    CardItem.JAMID_MUSHTAQ: (CardItem.WORD_CLASS,),
    CardItem.KULLI_JUZI: (CardItem.WORD_CLASS,),
    CardItem.LAFZ_MADLUL_RELATION: (),
    CardItem.HAQIQA_MAJAZ: (CardItem.LAFZ_MADLUL_RELATION,),
    CardItem.MUTABAQA_TADAMMUN_ILTIZAM: (CardItem.HAQIQA_MAJAZ,),
    CardItem.DAL_ALONE: (),
    CardItem.MADLUL_ALONE: (),
    CardItem.DAL_MADLUL_COUPLING: (CardItem.DAL_ALONE, CardItem.MADLUL_ALONE),
    CardItem.WAZN: (),
    CardItem.ISHTIQAQ_SARF: (CardItem.WAZN,),
    CardItem.AMIL_MAMUL: (),
    CardItem.NISAB_TADMIN_TAQYID: (CardItem.AMIL_MAMUL,),
    CardItem.MAQAM: (),
    CardItem.KHABAR_INSHA: (),
    CardItem.MANTUQ_MAFHUM: (CardItem.MUTABAQA_TADAMMUN_ILTIZAM,),
    CardItem.IFADA: (CardItem.NISAB_TADMIN_TAQYID,),
}

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "result",
    "outcome",
    "verdict",
    "birth",
    "certificate",
    "classification",
    "proof",
    "score",
    "fractal",
)


def derived_prerequisites(item: CardItem) -> tuple[CardItem, ...]:
    """شروطُ البند، مُشتَقّةً لا مكتوبةً في أيّ حقل."""

    if not isinstance(item, CardItem):
        raise SentenceCardPreregistrationError("البند عضوٌ في مفردته المغلقة.")
    return _DERIVED_PREREQUISITES[item]


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SentenceCardPreregistrationError(
            f"{field_name} نصٌّ غير فارغ؛ ولا يُقبَل فيه الفراغ صمتًا."
        )
    return value


def _require_blank(value: str, field_name: str, reason: str) -> str:
    if not isinstance(value, str) or value:
        raise SentenceCardPreregistrationError(f"{field_name} يبقى فارغًا: {reason}")
    return value


@dataclass(frozen=True, slots=True)
class CardItemRegistration:
    """تسجيلُ بندٍ واحدٍ قبل جوابه؛ لا حقلَ نتيجةٍ فيه البتّة."""

    item: CardItem
    reference: FrozenReference
    standing: ItemStanding
    supporting_module: str
    deferring_law: str
    supplied_text_key: str
    prerequisites: tuple[CardItem, ...]
    refusals: tuple[NamedRefusal, ...]
    note: str

    def __post_init__(self) -> None:
        if not isinstance(self.item, CardItem):
            raise SentenceCardPreregistrationError("البند عضوٌ في مفردته المغلقة.")
        if not isinstance(self.reference, FrozenReference):
            raise SentenceCardPreregistrationError(
                "المرجعُ عضوٌ في مفردته الثلاثية المغلقة؛ "
                + ONE_FROZEN_REFERENCE_PER_ITEM_NOTE
            )
        if not isinstance(self.standing, ItemStanding):
            raise SentenceCardPreregistrationError("موقفُ البند عضوٌ في مفردته المغلقة.")

        _require_text(self.note, f"بيانُ البند {self.item.value}")

        if self.standing is ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE:
            _require_text(self.supporting_module, "وحدةُ البند")
            _require_blank(
                self.deferring_law, "قانونُ التأجيل", _MODULE_REQUIRED_REFUSAL
            )
            _require_blank(
                self.supplied_text_key, "مفتاحُ النصّ المُزوَّد", _MODULE_REQUIRED_REFUSAL
            )
            if self.supporting_module.endswith("__init__.py"):
                raise SentenceCardPreregistrationError(
                    "وحدةُ البند وحدةٌ مُسمّاة، لا ملفَّ تجميعِ حزمة."
                )
        elif self.standing is ItemStanding.DEFERRED_BY_NAMED_LAW:
            _require_text(self.deferring_law, "قانونُ التأجيل")
            _require_blank(self.supporting_module, "وحدةُ البند", _LAW_REQUIRED_REFUSAL)
            _require_blank(
                self.supplied_text_key, "مفتاحُ النصّ المُزوَّد", _LAW_REQUIRED_REFUSAL
            )
        elif self.standing is ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE:
            _require_text(self.supplied_text_key, "مفتاحُ النصّ المُزوَّد")
            _require_blank(
                self.supporting_module, "وحدةُ البند", _SUPPLIED_KEY_REQUIRED_REFUSAL
            )
            _require_blank(
                self.deferring_law,
                "قانونُ التأجيل",
                _SUPPLIED_KEY_REQUIRED_REFUSAL,
            )
        else:
            _require_blank(self.supporting_module, "وحدةُ البند", _AWAITING_REFUSAL)
            _require_blank(self.deferring_law, "قانونُ التأجيل", _AWAITING_REFUSAL)
            _require_blank(
                self.supplied_text_key, "مفتاحُ النصّ المُزوَّد", _AWAITING_REFUSAL
            )

        if not self.refusals:
            raise SentenceCardPreregistrationError(
                f"بندُ {self.item.value} بلا رفضٍ مُسمًّى واحد؛ وحدودُ البند "
                "تُسمّى ولا تُترَك للقارئ."
            )
        seen_names: set[str] = set()
        for refusal in self.refusals:
            if not isinstance(refusal, NamedRefusal):
                raise SentenceCardPreregistrationError(
                    "كلُّ رفضٍ `NamedRefusal` مستوردةً لا منسوخةً، باسمه وبيانه."
                )
            if refusal.name in seen_names:
                raise SentenceCardPreregistrationError(
                    f"رفضٌ مكرّرٌ في بند {self.item.value}: {refusal.name}."
                )
            seen_names.add(refusal.name)

        derived = derived_prerequisites(self.item)
        if tuple(self.prerequisites) != derived:
            raise SentenceCardPreregistrationError(
                f"شروطُ بند {self.item.value} مكتوبةٌ على خلاف المُشتَقّ؛ "
                "والتبعيةُ تُشتَقّ من قراءة بندٍ لمخرجات آخر، ولا تُكتَب."
            )

    @property
    def module_path(self) -> str:
        """مسارُ وحدة البند منسوبًا إلى جذر المستودع، أو فراغٌ إن لم تُعلَن."""

        if not self.supporting_module:
            return ""
        return f"{ARABIC_PACKAGE_RELATIVE_PATH}/{self.supporting_module}"


@dataclass(frozen=True, slots=True)
class SentenceCardPreregistration:
    """تسجيلُ البطاقة كلّها: تغطيةٌ قبل جواب، وترتيبٌ قبل قراءة."""

    registrations: tuple[CardItemRegistration, ...]

    def __post_init__(self) -> None:
        seen: list[CardItem] = []
        for registration in self.registrations:
            if not isinstance(registration, CardItemRegistration):
                raise SentenceCardPreregistrationError(
                    "كلُّ عنصرٍ `CardItemRegistration`."
                )
            if registration.item in seen:
                raise SentenceCardPreregistrationError(
                    f"بندٌ مكرّرٌ في التسجيل: {registration.item.value}؛ "
                    "والتكرارُ يُخفي تسجيلًا تحت آخر."
                )
            for prerequisite in registration.prerequisites:
                if prerequisite not in seen:
                    raise SentenceCardPreregistrationError(
                        f"بندُ {registration.item.value} سبق شرطَه "
                        f"{prerequisite.value}؛ وتقديمُ البند على شرطه يجعل "
                        "قراءتَه لمخرجاته قراءةً لما لم يُسجَّل بعد."
                    )
            seen.append(registration.item)

        missing = tuple(item for item in CardItem if item not in seen)
        if missing:
            raise SentenceCardPreregistrationError(
                "بندٌ مفقودٌ من التسجيل: "
                + "، ".join(item.value for item in missing)
                + "؛ والتغطيةُ تسبق الجواب، وبندٌ لم يُسجَّل ليس بندًا بلا حدود."
            )

    @property
    def items(self) -> tuple[CardItem, ...]:
        """البنودُ بترتيب تسجيلها، مُشتَقّةً من التسجيلات نفسها."""

        return tuple(registration.item for registration in self.registrations)

    @property
    def certificate_is_constructible(self) -> bool:
        """`False` على كلّ فرع: لا شهادةَ بلا نصٍّ مصدريٍّ وشاهدٍ لكلّ فرع."""

        return False

    def registration_for(self, item: CardItem) -> CardItemRegistration:
        """تسجيلُ بندٍ بعينه؛ والبندُ المُسجَّل موجودٌ بحكم التغطية."""

        for registration in self.registrations:
            if registration.item is item:
                return registration
        raise SentenceCardPreregistrationError(f"لا تسجيل للبند {item.value}.")

    def items_with_standing(self, standing: ItemStanding) -> tuple[CardItem, ...]:
        """البنودُ ذاتُ موقفٍ بعينه، مُشتَقّةً من التسجيلات لا من حقل عدد."""

        if not isinstance(standing, ItemStanding):
            raise SentenceCardPreregistrationError("الموقفُ عضوٌ في مفردته المغلقة.")
        return tuple(
            registration.item
            for registration in self.registrations
            if registration.standing is standing
        )


@dataclass(frozen=True, slots=True)
class CardItemSupportReading:
    """قراءةُ بندٍ واحد: تسجيلُه، وحالُ ترميز وحدته المُشتقّة من الشجرة."""

    registration: CardItemRegistration
    coding: SupportCoding

    def __post_init__(self) -> None:
        if not isinstance(self.registration, CardItemRegistration):
            raise SentenceCardPreregistrationError("تسجيلُ البند تسجيلٌ مُصاغ.")
        if not isinstance(self.coding, SupportCoding):
            raise SentenceCardPreregistrationError(
                "حالُ الترميز عضوٌ في مفردتها المغلقة."
            )

    @property
    def is_coded(self) -> bool:
        return self.coding is SupportCoding.CODED


def read_item_support(root: Path | None = None) -> tuple[CardItemSupportReading, ...]:
    """اقرأ البنودَ، مُشتقًّا وجودَ كلّ وحدةٍ مُعلَنةٍ من الشجرة لا من حقل."""

    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise SentenceCardPreregistrationError("جذرُ المستودع مسار.")
    package = base / ARABIC_PACKAGE_RELATIVE_PATH
    if not package.is_dir():
        raise SentenceCardPreregistrationError(
            f"طبقةُ العربية غير موجودة عند {package}: شجرةٌ غائبةٌ تُقرأ «لا "
            "وحدات» وهو ادّعاءٌ لم تُقرأ الشجرة لأجله."
        )
    readings: list[CardItemSupportReading] = []
    for registration in SENTENCE_CARD_PREREGISTRATION.registrations:
        if not registration.supporting_module:
            coding = SupportCoding.NO_MODULE_DECLARED
        elif (package / registration.supporting_module).is_file():
            coding = SupportCoding.CODED
        else:
            coding = SupportCoding.NOT_CODED
        readings.append(
            CardItemSupportReading(registration=registration, coding=coding)
        )
    return tuple(readings)


_FORMAL_CLASSIFICATION_REFUSAL: Final = NamedRefusal(
    name="FormalClassification != BirthVerdict",
    statement=(
        "التصنيفُ الصوريُّ ليس حكمَ ولادة: لا `Freeze`، ولا `E0`، ولا بوّابةَ " "نواةٍ تقرؤه"
    ),
)

_SENTENCE_IS_NOT_A_LEXEME_REFUSAL: Final = NamedRefusal(
    name="SentenceIsNotALexeme",
    statement=SENTENCE_IS_NOT_A_LEXEME_NOTE,
)


def _registration(
    item: CardItem,
    reference: FrozenReference,
    standing: ItemStanding,
    note: str,
    refusals: tuple[NamedRefusal, ...],
    supporting_module: str = "",
    deferring_law: str = "",
    supplied_text_key: str = "",
) -> CardItemRegistration:
    return CardItemRegistration(
        item=item,
        reference=reference,
        standing=standing,
        supporting_module=supporting_module,
        deferring_law=deferring_law,
        supplied_text_key=supplied_text_key,
        prerequisites=derived_prerequisites(item),
        refusals=refusals,
        note=note,
    )


SENTENCE_CARD_PREREGISTRATION: Final = SentenceCardPreregistration(
    registrations=(
        _registration(
            item=CardItem.WORD_CLASS,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE,
            supporting_module="word_class_formal.py",
            note=(
                "يُساق سؤالا المجال المُجمَّد على كلّ كلمةٍ من كلمات الجملة "
                "واحدةً واحدة، ويُشتَقّ الصنفُ بـ`classify` لا يُكتَب"
            ),
            refusals=(
                _SENTENCE_IS_NOT_A_LEXEME_REFUSAL,
                _FORMAL_CLASSIFICATION_REFUSAL,
            ),
        ),
        _registration(
            item=CardItem.IRAB_MARK,
            reference=FrozenReference.AL_NAHW_AL_WADIH,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            note=(
                "«النحو الواضح» عملٌ حديثٌ محميٌّ بحقوق نشرٍ فعلية، ولا يُتوقَّع "
                "وجودُه في كوربصٍ مفتوح؛ فوقوفُ هذا البند امتناعٌ قانونيٌّ دائمٌ "
                "مُسمًّى (`MODERN_COPYRIGHTED_SOURCE_NOT_DIGITIZED_OPENLY`) لا "
                "فجوةُ بحثٍ مؤقتة، ولا يُطلَب له بحثٌ إضافيّ"
            ),
            refusals=(
                NamedRefusal(
                    name="DeclaredMarkIsNotAnAttestedMark",
                    statement=(
                        "كتابةُ «رفعٌ بالضمة» في بطاقةٍ لا تُثبِتها؛ الإثباتُ نصٌّ "
                        "مصدريٌّ مُسمًّى وحاملٌ يُشتَقّ منه، لا تقريرٌ في خانة"
                    ),
                ),
                NamedRefusal(
                    name="IrabMarkIsNotASurfaceObservation",
                    statement=(
                        "العلامةُ حكمٌ نحويٌّ على موقعٍ لا رصدٌ لحركةٍ في السطح؛ "
                        "ولا تُشتَقّ من `SurfaceNormalization` ولا من ذرّاتها"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.MURAB_MABNI,
            reference=FrozenReference.AL_NAHW_AL_WADIH,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            note=(
                "المصدرُ نفسُه ممتنعٌ بالجنس الدائم نفسه، فالقسمةُ بلا نصّ؛ والمعيارُ "
                "المذكورُ في الطلب (أسماءُ الإشارة والموصول والضمائر وحدها "
                "مبنية) دعوى حصرٍ تحتاج نصَّها لا تعدادَ أمثلة"
            ),
            refusals=(
                NamedRefusal(
                    name="EnumeratedExamplesAreNotAnExhaustiveCriterion",
                    statement=(
                        "تعدادُ ما وقع مبنيًّا في جملةٍ واحدة لا يُثبِت حصرَ "
                        "المبنيّات؛ والحصرُ دعوى نصٍّ لا استقراءُ بطاقة"
                    ),
                ),
                NamedRefusal(
                    name="MabniIsNotAnUnchangedSurfaceForm",
                    statement=(
                        "البناءُ حكمٌ على جنس اللفظ لا ثباتٌ مرصودٌ في السطح؛ "
                        "ولفظٌ لم تتغيّر صورتُه في شاهدين ليس مبنيًّا بذلك"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.JAMID_MUSHTAQ,
            reference=FrozenReference.LISAN_AL_ARAB,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            note=(
                "مادةُ (ن و ر) قُرِئت في شاهدٍ رقميٍّ مُسمًّى ومُسِحت، فلم يقع "
                "فيها لفظُ «مشتق» ولا «اشتقاق» ولا مرّةً واحدة؛ فالبندُ يقف "
                "**نتيجةَ مسحٍ جرى** لا لغياب بحث. ويُسجَّل هنا فارقٌ يُخشى "
                "طيُّه: «المشتق» في قسمة الكلّي غيرُ «المشتق» الصرفيّ المقصود "
                "في هذا البند"
            ),
            refusals=(
                NamedRefusal(
                    name="DerivedUniversalIsNotMorphologicalDerivation",
                    statement=(
                        "`SubOutcome.MUSHTAQQ` في `kulli_juzi_formal` كلّيٌّ دلّ "
                        "على ذي صفةٍ معيّنة، و«المشتق» هنا بناءٌ صرفيٌّ من جذر؛ "
                        "واتّفاقُ الاسمين لا يجعلهما سؤالًا واحدًا"
                    ),
                ),
                NamedRefusal(
                    name="LexiconEntryIsNotSuppliedHere",
                    statement=(
                        "مدخلُ المعجم يُنقَل بحروفه حاملًا اسمَ سلطته نصًّا، ولا "
                        "يُحكى معناه؛ وما لم يُنقَل بحروفه ممتنع"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.KULLI_JUZI,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE,
            supporting_module="kulli_juzi_formal.py",
            note=(
                "يُساق المجالُ المُجمَّد على كلّ كلمة، ويُشتَقّ التصنيفُ بـ"
                "`classify_kulli_juzi` من حاملَي الشركة والتفريع لا يُكتَب"
            ),
            refusals=(
                _SENTENCE_IS_NOT_A_LEXEME_REFUSAL,
                NamedRefusal(
                    name="CarrierIsDeclaredNotInferredFromTheVerse",
                    statement=(
                        "حاملُ التفريع (يستوي معناه في أفراده أم يختلف) يُعلَن "
                        "في البطاقة ويُقابَل بنصّ المصدر، ولا يُستنبَط من الآية "
                        "نفسها؛ وإلا صارت البطاقةُ مصدرَ حكمها"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.LAFZ_MADLUL_RELATION,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE,
            supporting_module="lafz_madlul_relation_formal.py",
            note=(
                "الأقسامُ السبعةُ مجالٌ واحدٌ مُجمَّد، فلا يُفرَد «متباين/مشترك/"
                "مشكِّك/مترادف/منقول» عنه؛ و«المشكِّك» ليس عضوًا فيه أصلًا بل في "
                "قسمة الكلّي، وخلطُهما خلطُ مجالين"
            ),
            refusals=(
                NamedRefusal(
                    name="MushakkikBelongsToTheUniversalPartition",
                    statement=(
                        "«المشكِّك» فرعٌ في قسمة الكلّي لا عضوٌ في الأقسام السبعة "
                        "لعلاقة اللفظ بمدلوله؛ وإدراجُه في صفٍّ واحدٍ معها يُنشئ "
                        "مفردةً ثامنةً لا وجودَ لها في المصدر"
                    ),
                ),
                _FORMAL_CLASSIFICATION_REFUSAL,
            ),
        ),
        _registration(
            item=CardItem.HAQIQA_MAJAZ,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE,
            supporting_module="lafz_madlul_relation_formal.py",
            note=(
                "الحقيقةُ والمجازُ فرعا السؤال الخامس في المجال نفسه، فيُشتَقّان "
                "من المعنى المُراد المُعلَن لا يُكتَبان؛ وأنواعُ العلاقة "
                "المجازية غيرُ مُرمَّزةٍ في هذه الشجرة"
            ),
            refusals=(
                NamedRefusal(
                    name="MajazTypeIsNotClassifiedHere",
                    statement=(
                        "كونُ اللفظ مجازًا مُشتَقٌّ من المجال المُجمَّد، أمّا نوعُ "
                        "العلاقة (سببيةً كانت أو غيرَها) فلا مفردةَ له هنا ولا "
                        "شاهدَ لفروعها، فلا يُصنَّف"
                    ),
                ),
                NamedRefusal(
                    name="QarinaIsDeclaredNotDerived",
                    statement=(
                        "القرينةُ المانعةُ من إرادة الحقيقة تُعلَن في البطاقة "
                        "شاهدًا مقروءًا، ولا تُشتَقّ من كون التصنيف مجازًا؛ وإلا "
                        "دارت الحجّة على نفسها"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.MUTABAQA_TADAMMUN_ILTIZAM,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE,
            supplied_text_key="MUTABAQA_TADAMMUN_ILTIZAM_SHAKHSIYYA_THREE",
            note=(
                "زُوِّد نصُّ الدلالات الثلاث بحروفه في `sentence_card_source_"
                "texts`، فسقط عن البند نقصُ النقل وحده: لا مفردةَ له بعد، ولا "
                "دالّةَ قرار، ولا شاهدَ لكلّ فرع؛ وموضعُه `موضع_غير_متحقق` لأنّ "
                "المصدرَ ملفُّ `.docx` بلا بيانات طبعةٍ مؤكَّدة"
            ),
            refusals=(
                NamedRefusal(
                    name="IltizamIsNotLogicalEntailment",
                    statement=(
                        "الالتزامُ دلالةُ لفظٍ على لازمٍ ذهنيّ، لا الاستلزامَ "
                        "المنطقيّ `⊨`؛ وهذا أقربُ سوءِ قراءةٍ لهذا البند"
                    ),
                ),
                NamedRefusal(
                    name="ThreeDalalatAreNotTheDalalaChannelPair",
                    statement=(
                        "`DalalaChannel` ثنائيةٌ (منطوق/مفهوم) ولا تُوسَّع إلى "
                        "ثلاث لتستوعب هذه الدلالات؛ وتوسيعُ مفردةٍ مُجمَّدةٍ بعد "
                        "رؤية حالةٍ بعينها هو ما يمنعه `MarkerVocabularyIsFrozen"
                        "BeforeItsText`"
                    ),
                ),
                NamedRefusal(
                    name="SuppliedTextIsNotAFormalCertificate",
                    statement=(
                        "تزويدُ النصّ يرفع نقصَ النقل ولا يُنشئ مجالًا مُجمَّدًا "
                        "ولا حاملًا يُشتَقّ منه؛ فالبندُ لا يزال غيرَ مقروءٍ في "
                        "أيّ بطاقة"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.DAL_ALONE,
            reference=FrozenReference.LISAN_AL_ARAB,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            note=(
                "الدالُّ وحده بنيةٌ صوتيةٌ صرفيةٌ مجرّدة؛ والمُزوَّدُ من مادة "
                "(ن و ر) معانٍ ومنقولاتُ سلطاتٍ لا تحليلَ دالٍّ مجرّدٍ عن مدلوله، "
                "فالبندُ يقف بعد قراءة المادة لا قبلها. والمسبارُ التوزيعيُّ في "
                "هذه الشجرة يقيس توزيعًا ولا يَنقُل معجمًا"
            ),
            refusals=(
                NamedRefusal(
                    name="DistributionalProbeIsNotALexiconCitation",
                    statement=(
                        "`distributional_probe_report` تقريرٌ ظنّيٌّ عن توزيع، "
                        "ولا يقوم مقام نقلٍ حرفيٍّ من معجمٍ مُسمًّى"
                    ),
                ),
                NamedRefusal(
                    name="DalAloneIsNotRecordedSound",
                    statement=(
                        "بياناتُ هذه الشجرة نصٌّ مُرمَّزٌ لا صوتٌ مُسجَّل، على "
                        "منوال `UnicodeIsNotRecordedSound` و`STATION_ZERO_NOTE`"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.MADLUL_ALONE,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE,
            supporting_module="madlul_alone_formal.py",
            note=(
                "أقسامُ المدلول الخمسةُ مجالٌ مُجمَّد، يُشتَقّ منه القسمُ بـ"
                "`classify_madlul` من أسئلته الثلاثة لا يُكتَب"
            ),
            refusals=(
                NamedRefusal(
                    name="MadlulSectionIsNotTheMeaningItself",
                    statement=(
                        "تصنيفُ المدلول «معنًى» يقول إنّ مدلولَ اللفظ ليس لفظًا، "
                        "ولا يقول ما هو ذلك المعنى ولا يُثبِته"
                    ),
                ),
                _FORMAL_CLASSIFICATION_REFUSAL,
            ),
        ),
        _registration(
            item=CardItem.DAL_MADLUL_COUPLING,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            note=(
                "الاقترانُ لا يُعرَف إلا بالنقل كما يُقرّره `wad_naql`، ولم "
                "يُقدَّم هنا نقلٌ تفسيريٌّ مُسنَدٌ بحروفه لهذا الاستعمال بعينه؛ "
                "فالبندُ `مصدر_غير_مُقدَّم` نتيجةً لا خانةً فارغة. ورفعُ بندَي "
                "الوزن والاشتقاق بنصٍّ مُزوَّدٍ لا يمسّه، ولا يرفعه رفعُ «الدال "
                "وحده» لو وقع، لأنّ `refuse_derivation` يرفض الطريقين معًا"
            ),
            refusals=(
                NamedRefusal(
                    name="WadIsNotDerivedFromTheTwoHalves",
                    statement=(
                        "`refuse_derivation` يرفع دائمًا على طريقَي الاستنباط "
                        "من التحليل التوزيعيّ ومن تحليل المدلول؛ فاجتماعُ "
                        "البندين التاسع والعاشر لا يُنتِج اقترانًا"
                    ),
                ),
                NamedRefusal(
                    name="WadSourceIsVolumeOneNotThree",
                    statement=(
                        "نصُّ الوضع المُثبَتُ في `wad_naql` من الجزء الأول، "
                        "ومرجعُ هذه البطاقة المُجمَّدُ الجزءُ الثالث؛ والفارقُ "
                        "يُسجَّل ولا يُطوى بجمعهما تحت اسمٍ واحد"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.WAZN,
            reference=FrozenReference.LISAN_AL_ARAB,
            standing=ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE,
            supplied_text_key="WAZN_LISAN_NUR",
            note=(
                "زُوِّد من مادة (ن و ر) نصٌّ يُسمّي وزنًا بعينه مُسنَدًا إلى ثعلب "
                "(«منارة وهي مفعلة من النور»)؛ ووزنُ «نور» نفسه غيرُ منصوصٍ في "
                "المقطع، فالمزوَّدُ نصُّ سلطةٍ في وزن مشتقٍّ من المادة لا وزنُ "
                "كلمة البطاقة، والفارقُ يُسجَّل ولا يُطوى"
            ),
            refusals=(
                NamedRefusal(
                    name="PatternSpaceIsNotLexicalInventory",
                    statement=(
                        "اشتقاقُ وزنٍ لا يُثبِت أنّ كلَّ ما على ذلك الوزن لفظٌ "
                        "مستعمَل؛ وهي شهادةٌ مرصودةٌ في `docs/reference` غيرُ "
                        "مُدقَّقة، لا قياسٌ في هذه الشجرة"
                    ),
                ),
                NamedRefusal(
                    name="WaznIsNotDerivedFromSurfaceSkeleton",
                    statement=(
                        "الوزنُ لا يُشتَقّ من هيكلٍ حرفيٍّ مُجرَّدٍ من الحركات؛ "
                        "وذلك عينُ تصادم المتجانسات المرصود في السجلّ نفسه"
                    ),
                ),
                NamedRefusal(
                    name="WaznOfADerivativeIsNotTheWaznOfTheCardWord",
                    statement=(
                        "«مفعلة» وزنُ «منارة» في النصّ المنقول، ولا يُقرأ وزنًا "
                        "لـ«نور» في الآية؛ وحملُ أحدهما على الآخر كتابةُ نتيجةٍ "
                        "لا يحملها النصّ"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.ISHTIQAQ_SARF,
            reference=FrozenReference.LISAN_AL_ARAB,
            standing=ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE,
            supplied_text_key="ISHTIQAQ_SARF_LISAN_NUR",
            note=(
                "زُوِّد نصٌّ مُسنَدٌ إلى الجوهري يَنسِب «مناور» إلى النور ويُعلِّل "
                "الهمزَ تشبيهًا بالأصليّ؛ وهو نقلُ سلطةٍ في اشتقاق المادة، ولا "
                "يقوم مقامَ مجالٍ صوريٍّ للجذر والمصدر لا يزال غيرَ مُرمَّز"
            ),
            refusals=(
                NamedRefusal(
                    name="RootDatasetIsNotALexiconEntry",
                    statement=(
                        "`lisan345` مجموعةُ جذورٍ مقيسةٌ لأجل التجاور، ولا تقوم "
                        "مقامَ مدخلٍ معجميٍّ يُنقَل بحروفه لمادةٍ بعينها"
                    ),
                ),
                NamedRefusal(
                    name="TriliteralRootIsADeclaredReadingNotAMeasurement",
                    statement=(
                        "كونُ المادة ثلاثيةً جوفاء قراءةٌ صرفيةٌ تحتاج سندَها، "
                        "ولا تُقرأ من عدد حروف السطح"
                    ),
                ),
                NamedRefusal(
                    name="SuppliedLexiconLineIsNotAMorphologicalDomain",
                    statement=(
                        "سطرٌ معجميٌّ مُسنَدٌ يرفع نقصَ النقل ولا يُنشئ قسمةً "
                        "صرفيةً مغلقةً ولا دالّةَ اشتقاقٍ تُقرأ بها البطاقة"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.AMIL_MAMUL,
            reference=FrozenReference.AL_NAHW_AL_WADIH,
            standing=ItemStanding.DEFERRED_BY_NAMED_LAW,
            deferring_law="Preregistration != Certificate",
            note=(
                "هذا البندُ هو بعينه المرحلةُ الأولى في "
                "`compound_layer_preregistration`، وموقفُها هناك "
                "`مصدر_غير_مُقدَّم`؛ وإصدارُه شهادةً هنا يُسقط ذلك التسجيلَ صامتًا"
            ),
            refusals=(
                NamedRefusal(
                    name="CompoundStageIsDeferredNotReopened",
                    statement=(
                        "رفعُ التأجيل يكون بتزويد نصّ المرحلة في موضعها لا "
                        "بإعادة تسميتها في بطاقةٍ أخرى؛ وإعادةُ التسمية تعريفٌ "
                        "جديدٌ لا تشديدُ دليل"
                    ),
                ),
                NamedRefusal(
                    name="DeclaredAmil != BornOperator",
                    statement=(
                        "كونُ اللفظ مُصنَّفًا «عاملًا» لا يجعله `Operation` في "
                        "النواة ولا عاملًا مولودًا له مجالُ مصدرٍ مُرخَّص"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.NISAB_TADMIN_TAQYID,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DEFERRED_BY_NAMED_LAW,
            deferring_law="Preregistration != Certificate",
            note=(
                "هذا البندُ يجمع المرحلتين الثانية والثالثة في "
                "`compound_layer_preregistration`، وكلتاهما `مصدر_غير_مُقدَّم`؛ "
                "والنسبةُ الإضافيةُ المذكورةُ في الطلب لا مفردةَ لها هناك أصلًا"
            ),
            refusals=(
                NamedRefusal(
                    name="IdafaIsNotARegisteredStage",
                    statement=(
                        "النسبةُ الإضافية ليست عضوًا في مراحل طبقة المركّب "
                        "المُسجَّلة؛ وإضافتُها الآن فتحُ فرعٍ خامسٍ في تسجيلٍ "
                        "مُجمَّدٍ قبل نصّه"
                    ),
                ),
                NamedRefusal(
                    name="IsnadiyyaIsNotTruth",
                    statement=(
                        "تصنيفُ النسبة إسناديةً تصنيفُ بنيةٍ لا تصديقٌ بمضمونها؛ "
                        "فلا تُقرَأ نسبةٌ مُصنَّفة `ClaimCore` ولا دعوى مُثبَتة"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.MAQAM,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            note=(
                "بُحِث عن تعريفٍ إجرائيٍّ للمقام في المصدر المُعلَن (ج٣) فلم "
                "يُوجَد أصلًا، فجنسُ وقوفه غيرُ جنس ما سبق: "
                "`TERM_NOT_LOCATED_IN_DECLARED_SOURCE` لا «موضعٌ غيرُ متحقَّق». "
                "وقد يكون مصطلحًا بلاغيًّا في علم المعاني لا أصوليًّا، ولا "
                "يُبدَّل مرجعُه المُعلَن بعد رؤية النتيجة"
            ),
            refusals=(
                NamedRefusal(
                    name="ContextIsNotACitedSource",
                    statement=(
                        "قراءةُ السياق اجتهادُ قارئٍ ما لم تُنقَل عن سلطةٍ "
                        "مُسمّاةٍ بحروفها؛ وسندٌ من هذا الجنس لا يُقبَل هنا "
                        "كما لم يُقبَل في بطاقات التدقيق"
                    ),
                ),
                NamedRefusal(
                    name="MaqamVocabularyIsNotEnumerated",
                    statement=(
                        "لا مفردةَ مغلقةً للمقامات في هذه الشجرة، ومقامٌ يُكتَب "
                        "نصًّا حرًّا ليس عضوًا في قسمةٍ مُحكَمة"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.KHABAR_INSHA,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE,
            supplied_text_key="KHABAR_INSHA_SHAKHSIYYA_THREE",
            note=(
                "زُوِّد نصُّ الفرق بين الخبر والإنشاء بحروفه، وفيه فارقٌ ثانٍ لم "
                "يذكره الطلب: مقارنةُ الإنشاء للفظ دون الخبر. ولا مفردةَ للقسمة "
                "بعد ولا شاهدَ لفرعيها، والموضعُ `موضع_غير_متحقق`"
            ),
            refusals=(
                NamedRefusal(
                    name="KhabarDefinitionIsNotATruthVerdict",
                    statement=(
                        "احتمالُ الصدق والكذب حدُّ جنسٍ لا حكمٌ على هذا الخبر "
                        "بعينه؛ وخلطُهما يجعل التصنيفَ تصديقًا أو تكذيبًا"
                    ),
                ),
                NamedRefusal(
                    name="InshaIsNotADeclaredSpeechAct",
                    statement=(
                        "الإنشاءُ قسمٌ في اللفظ لا فعلُ كلامٍ مستوردٌ من مفردةٍ "
                        "أجنبية؛ واستيرادُ تقسيمٍ خارجيٍّ يحتاج بصمةَ مصدره"
                    ),
                ),
            ),
        ),
        _registration(
            item=CardItem.MANTUQ_MAFHUM,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE,
            supporting_module="mantuq_mafhum_ifada.py",
            note=(
                "القناةُ وقسمُ المفهوم يُشتَقّان من حاملَيهما في `DalalaRecord` "
                "ولا يُكتَبان؛ و«لا مفهومَ مخالفةٍ ظاهر» تصريحٌ بعضوٍ مُسمًّى "
                "(`لا_ينطبق`) لا خانةٌ فارغة"
            ),
            refusals=(
                NamedRefusal(
                    name="MafhumChannelIsNotContentStanding",
                    statement=(
                        "`DalalaChannel.مفهوم` قناةُ دلالةٍ في لفظ، و"
                        "`ContentStanding.مفهوم` حالُ محتوًى أُسنِد إلى حسّ؛ "
                        "واتّفاقُ اللفظين لا يجمعهما"
                    ),
                ),
                _SENTENCE_IS_NOT_A_LEXEME_REFUSAL,
            ),
        ),
        _registration(
            item=CardItem.IFADA,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE,
            supporting_module="mantuq_mafhum_ifada.py",
            note=(
                "حالُ الإفادة تُشتَقّ من حاملها، و`غير_مقروء` عضوٌ فيها يُفرِّق "
                "«لم تُقرَأ فائدتُه» من «لا فائدةَ فيه»؛ وشرطُ هذا البند المُشتَقّ "
                "هو بندُ النسب، وهو مؤجَّل، فبلوغُه موقوفٌ بالتتابع"
            ),
            refusals=(
                NamedRefusal(
                    name="UnreadBenefitIsNotAbsentBenefit",
                    statement=(
                        "`غير_مقروء` ليست `غير_مُفيد`: الجهلُ بالفائدة عضوٌ "
                        "مُسمًّى، وقراءتُه انتفاءً هي الخطأُ الذي تمنعه المفردة"
                    ),
                ),
                NamedRefusal(
                    name="ShibhJumlaPredictionIsRegisteredNotRun",
                    statement=(
                        "التنبّؤُ بأنّ «في بيوتٍ» تقف عند هذا البند معزولةً عن "
                        "متعلَّقها مُسجَّلٌ في `NAMED_RESIDUALS` ولا يُشغَّل قبل "
                        "إغلاق الجملة الأولى بنتيجةٍ واحدةٍ كاملة"
                    ),
                ),
            ),
        ),
    )
)


NAMED_REFUSALS: Final[tuple[NamedRefusal, ...]] = (
    _SENTENCE_IS_NOT_A_LEXEME_REFUSAL,
    NamedRefusal(
        name="CardIsNotACertificate", statement=CARD_IS_NOT_A_CERTIFICATE_NOTE
    ),
    NamedRefusal(
        name="OneFrozenReferencePerItem", statement=ONE_FROZEN_REFERENCE_PER_ITEM_NOTE
    ),
    NamedRefusal(
        name="IncompleteCardIsTheResultNotADefect",
        statement=INCOMPLETE_CARD_IS_THE_RESULT_NOTE,
    ),
    NamedRefusal(
        name="OneCardOnThreeSentencesIsNotFractality",
        statement=FRACTAL_VERDICT_IS_NOT_ISSUED_HERE_NOTE,
    ),
    NamedRefusal(
        name="ParallelFrontIsNotABlockedFront", statement=PARALLEL_FRONT_READING_NOTE
    ),
    NamedRefusal(
        name="SuppliedTextIsNotAFormalCertificate",
        statement=SUPPLIED_TEXT_IS_NOT_A_CERTIFICATE_NOTE,
    ),
)


NAMED_RESIDUALS: Final[MappingProxyType[str, str]] = MappingProxyType(
    {
        "SECOND_AND_THIRD_SENTENCES_ARE_REGISTERED_NOT_OPENED": (
            "الجملةُ الفعلية «خَلَقَ اللهُ السماواتِ والأرضَ» وشبهُ الجملة «في "
            "بيوتٍ» مُسمّاتان هنا ولا يُعمَل فيهما: لا بطاقةَ لهما ولا سَوقَ "
            "عليهما قبل أن تُغلَق الجملةُ الاسمية بنتيجةٍ واحدةٍ كاملة. "
            "وتسجيلُ جبهةٍ ليس ترخيصًا بالعمل فيها، وهو قانونُ هذه الشجرة "
            "التسلسليُّ نازلًا درجة: `OpenFrontIsRegisteredNotOpened`"
        ),
        "SHIBH_JUMLA_IFADA_PREDICTION_IS_FROZEN_BEFORE_ITS_RUN": (
            "تنبّؤٌ مُجمَّدٌ قبل تشغيله: «في بيوتٍ» معزولةً عن متعلَّقها يُتوقَّع "
            "أن تُشتَقّ لها `IfadaStanding.غير_مُفيد` لا `غير_مقروء`، وأن يكون "
            "ذلك فرقًا فئويًّا بين جنس الجملة التامّة وجنس شبه الجملة لا عطلَ "
            "أداة. وتجميدُه الآن هو ما يجعله قابلًا للتفنيد؛ ولو كُتِب بعد "
            "تشغيله لكان وصفًا لا تنبّؤًا. **وأيُّ مدخلٍ يُفنّده؟** شبهُ جملةٍ "
            "مُعلَنٍ متعلَّقُها في البطاقة نفسها تُشتَقّ لها `مُفيد`"
        ),
        "SHAKHSIYYA_VOLUME_THREE_LOCUS_NOT_VERIFIED": (
            "مواضعُ الجزء الثالث المذكورةُ في الطلب (743-745، و719، و761، و"
            "1024، و1028) لم تُقابَل بطبعةٍ محقَّقةٍ في اليد؛ فهي إحالةٌ غيرُ "
            "متحقَّقة على منوال `PRINT_EDITION_LOCUS_NOT_VERIFIED`. **وقد "
            "نُقِلت منها حروفٌ بعد ذلك**: نصّا الدلالات الثلاث والخبر/الإنشاء "
            "مُثبَتان الآن في `sentence_card_source_texts` عن نسخة `.docx` "
            "مرفوعةٍ بلا بيانات طبعةٍ مؤكَّدة، فارتفع نقصُ النقل وحده وبقي نقصُ "
            "الموضع بحاله، وأرقامُ تلك «السطور» ترقيمُ استخراجٍ آليّ "
            "(`EXTRACTED_LINE_NUMBERS_ARE_NOT_PRINT_PAGINATION`). وهذه البقيّةُ "
            "لا تمسّ المُشتَقّ: البنودُ المُشتَقّة تقرأ مجالاتٍ مُجمَّدةً قائمةً "
            "في الشجرة لا أرقامَ صفحات"
        ),
        "NAHW_AND_LISAN_TEXTS_ARE_ABSENT_FROM_THIS_TREE": (
            "**هذه البقيّةُ سقطت شطرُها وبقي شطرُها، ولا تُمحى بل تُقرأ "
            "مؤرَّخة**. نصُّها الأوّل: «لا يَرِد في هذه الشجرة حرفٌ واحدٌ منقولٌ "
            "من النحو الواضح ولا مادةُ (ن و ر) من لسان العرب، فستّةُ بنودٍ تقف "
            "بذلك». وقد أُجري البحثُ فعلًا فوُجِدت مادةُ (ن و ر) في شاهدٍ رقميٍّ "
            "مُسمًّى، ونُقِل منها مقطعان مُسنَدان إلى ثعلب والجوهري، فارتفع "
            "الشطرُ المعجميُّ في بندَين (الوزن، والاشتقاق والصرف) وبقي بندان "
            "معجميّان واقفَين لأنّ المادة لا تحمل نصَّهما "
            "(`LISAN_NUR_MATERIAL_CARRIES_NO_JAMID_MUSHTAQ_OR_DAL_ALONE_"
            "STATEMENT`). أمّا شطرُ «النحو الواضح» فلم يسقط ولا يُتوقَّع سقوطُه: "
            "جنسُه `MODERN_COPYRIGHTED_SOURCE_NOT_DIGITIZED_OPENLY`. **وأيُّ "
            "مدخلٍ يُفنّد ما بقي؟** مقطعٌ منقولٌ بحروفه يحمل اسمَ سلطته نصًّا "
            "كما يُلزِم `LexicalAttribution`"
        ),
        "LISAN_NUR_MATERIAL_CARRIES_NO_JAMID_MUSHTAQ_OR_DAL_ALONE_STATEMENT": (
            "مادةُ (ن و ر) قُرِئت كاملةً في الشاهد الرقميّ المُسمّى ومُسِحت، "
            "فلم يقع فيها لفظُ «مشتق» ولا «اشتقاق»، ولا تحليلٌ للدالّ مجرّدًا عن "
            "مدلوله؛ فبندا «جامد/مشتق» و«الدال وحده» يقفان **بعد قراءة المصدر "
            "لا قبله**، وهذا وقوفٌ بنتيجةِ مسحٍ جرى لا بغياب بحث. ومن قرأ "
            "«زُوِّدت المادةُ» رفعًا لكلّ بندٍ معجميٍّ فقد عمّم ما لم يُقرَأ. "
            "**وأيُّ مدخلٍ يُفنّده؟** موضعٌ في المادة نفسها — أو تصريحٌ بمادةٍ "
            "أخرى مُعلَنةٍ قبل قراءتها — يحمل نصَّ أحد البندين بحروفه"
        ),
        "TERM_NOT_LOCATED_IN_DECLARED_SOURCE": (
            "**جنسٌ غيرُ جنس «الموضع غير المتحقَّق»، والفرقُ حامل**: هناك موضعٌ "
            "مذكورٌ لم يُقابَل بطبعة، وهنا **المصطلحُ غائبٌ عن المصدر المُعلَن "
            "أصلًا**. بُحِث عن تعريفٍ إجرائيٍّ لـ«المقام» في الجزء الثالث فلم "
            "يُوجَد، فبقي البندُ معلَّقًا بهذا الجنس وحده. ولم يُبدَّل مرجعُه "
            "المُعلَن ولم تُوسَّع مفردةُ `FrozenReference` لتسَع مرجعًا بلاغيًّا، "
            "لأنّ تبديلَ المصدر بعد رؤية النتيجة هو عينُ ما يُبطِل التسجيلَ "
            "المسبق. **وأيُّ مدخلٍ يُفنّده؟** موضعٌ في ج٣ يحمل حدَّ المقام "
            "وقسمتَه بحروفه"
        ),
        "MODERN_COPYRIGHTED_SOURCE_NOT_DIGITIZED_OPENLY": (
            "**امتناعٌ قانونيٌّ دائم لا فجوةُ بحثٍ مؤقتة**: «النحو الواضح» — "
            "ومثلُه «المعجم الوسيط» الذي لا بندَ في هذه البطاقة مُحالٌ عليه "
            "أصلًا فيُسجَّل امتناعُه عامًّا بلا ربطٍ مُختلَق — عملان حديثان "
            "محميّان بحقوق نشرٍ فعلية، لا تراثيّان كلسان العرب؛ فلا يُتوقَّع "
            "وجودُهما في كوربصٍ مفتوح، ولا يُهدَر في طلبهما بحثٌ إضافيّ. "
            "**وأيُّ مدخلٍ يرفعه؟** نسخةٌ مُرخَّصةٌ مشروعةٌ في اليد يُنقَل منها "
            "بحروفها؛ ولا يرفعه وجودُ نصٍّ منشورٍ بلا ترخيص"
        ),
        "DIGITALLY_ENCODED_PRINT_PAGINATION_UNCOLLATED": (
            "**مرتبةٌ وسطى مُسمّاة، لا شاهدٌ رقميٌّ خام ولا مقابلةٌ باليد**: "
            "علاماتُ `PageV05P240`…`PageV05P245` في الشاهد المُعتمَد ترقيمُ "
            "**طبعةٍ ورقيةٍ مُسمّاةٍ ببياناتها** (دار صادر، ط٣، ١٤١٤هـ) مُضمَّنٌ "
            "في النصّ، لا ترقيمُ موقعٍ إلكترونيّ؛ فهو أوثقُ ممّا رُدَّ به "
            "الطبريُّ وأدنى ممّا تُثبِته مقابلةُ نسخةٍ ورقيةٍ محقَّقةٍ في اليد، "
            "على منوال «[ص: 372]» في مقطع فتح الباري. وجنسُه مُسمًّى في "
            "`LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل`، ويبقى العضوُ "
            "الأعلى `مقابل_بنسخة_ورقية_محققة` **بلا مدخلٍ اليوم** فلا يُقرأ "
            "الوسطُ سقفًا. **وأيُّ مدخلٍ يرفعه؟** مقابلةُ هذه الحروف بنسخةٍ "
            "ورقيةٍ محدَّدةِ الدار والسنة والطبعة"
        ),
        "EXTRACTED_LINE_NUMBERS_ARE_NOT_PRINT_PAGINATION": (
            "كلُّ ترقيم «سطر» ورد في طلبات هذه البطاقة (٧١٩، و٨٩٢، و١٠٢٤، "
            "و١٠٢٨، و٧٤٣-٧٤٥…) **ترقيمٌ آليٌّ من استخراجٍ نصيٍّ لملفّ `.docx`، "
            "لا ترقيمُ صفحاتِ طبعةٍ مطبوعةٍ معتمَدة**؛ فهو غيرُ قابلٍ للاستشهاد "
            "الخارجيّ حتى تُقابَل تلك الفقراتُ بنسخةٍ ورقيةٍ محدَّدة الدار "
            "والسنة والطبعة. وهذا يسري على كلّ ما نُقِل من الجزء الثالث في هذه "
            "الشجرة، ومنه النصّان المُزوَّدان في `sentence_card_source_texts`. "
            "**وأيُّ مدخلٍ يرفعه؟** بياناتُ طبعةٍ مُسمّاةٍ وصفحةٌ فيها تُقابَل "
            "بها الحروفُ المنقولة"
        ),
        "LISAN_MATN_IS_QUOTED_NOT_VENDORED_WHOLESALE": (
            "متنُ لسان العرب (ابن منظور، ت٧١١هـ) مِلكٌ عامٌّ في نفسه، ولا ملفَّ "
            "ترخيصٍ في مستودع الشاهد الرقميّ المُعتمَد؛ فالمنقولُ هنا "
            "**اقتباساتٌ قصيرةٌ مُسنَدةٌ من المتن** لا المادةُ كاملةً ببنيتها "
            "المُوسَّمة وعلامات صفحاتها، إذ الذي قد يحمل جهدًا محميًّا هو "
            "التوسيمُ والترقيمُ الرقميّان لا كلماتُ ابن منظور. "
            "`PublicDomainMatnIsNotAnOpenLicence`"
        ),
        "TASHKIK_DIVERGENCE_IS_A_READING_NOT_A_CORRECTION": (
            "نصُّ المصدر المُثبَتُ في `kulli_juzi_formal` يَسوق «النور» في مثال "
            "المشكِّك («مثل الوجود والنور»)، والطلبُ يقرؤه «كلّيًّا متواطئًا». "
            "والفارقُ يُسجَّل بقيّةً مُسمّاةً ولا يُحسَم هنا: لا تُوسَّع مفردةٌ "
            "ولا يُعدَّل شاهدٌ مُثبَتٌ لتوافق قراءةَ الطلب، و«الوجود» وحده هو "
            "المُثبَتُ مشكِّكًا شاهدًا في تلك الوحدة لا «النور»"
        ),
    }
)


def _assert_no_result_field() -> None:
    """حارسُ استيراد: لا حقلَ نتيجةٍ يتسلّل إلى تسجيلٍ مسبقٍ لاحقًا."""

    for dataclass_type in (
        CardItemRegistration,
        SentenceCardPreregistration,
        CardItemSupportReading,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise SentenceCardPreregistrationError(
                        f"حقلٌ يحمل نتيجة تسلّل إلى {dataclass_type.__name__}: "
                        f"{declared.name}؛ والتسجيلُ المسبق لا نتيجة فيه."
                    )


if len(CardItem) != 19:  # pragma: no cover - guard
    raise RuntimeError("بنودُ البطاقة تسعةَ عشرَ بندًا مغلقة.")
if len(FrozenReference) != 3:  # pragma: no cover - guard
    raise RuntimeError("المراجعُ ثلاثةٌ مُجمَّدةٌ مغلقة.")
if len(ItemStanding) != 4:  # pragma: no cover - guard
    raise RuntimeError(
        "موقفُ البند رباعيٌّ مغلق: ثلاثيةٌ تُخفي حالةَ نصٍّ زُوِّد بلا شهادةٍ صورية."
    )
if len(SupportCoding) != 3:  # pragma: no cover - guard
    raise RuntimeError("حالُ الترميز ثلاثيةٌ مغلقة.")
if set(_DERIVED_PREREQUISITES) != set(CardItem):  # pragma: no cover - guard
    raise RuntimeError("مخروطُ الشرط مُشتَقٌّ لكلّ بند، ولا بندَ بلا مخروط.")

_assert_no_result_field()
