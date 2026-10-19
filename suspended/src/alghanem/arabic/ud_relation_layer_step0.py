"""خطوةٌ صفر وحدها: هل تحمل مدوَّنةٌ عربيةٌ بصيغة CoNLL-U طبقةَ علاقاتٍ فعلًا؟

أُغلِق السؤالُ السابق بنتيجةٍ مُسمّاة: `SYNTACTIC_LAYER_ABSENT_IN_THIS_FORMAT`
في صيغة `Quranic Arabic Corpus (morphology) 0.4` — أعمدتُها أربعةٌ لا عشرة، وليس
فيها رأسٌ ولا علاقة. فالسؤالُ هنا سؤالٌ آخر مستقلّ: **أتوجد اليومَ مدوَّنةٌ عربيةٌ
تحمل عمودَي `HEAD` و`DEPREL` مملوءَين بالفعل**، لا مُعلَنَين في وصف الصيغة وحدَه.

وهذه الوحدةُ **تسجيلُ خطوةٍ صفر لا قارئ**: `STEP_ZERO_IS_NOT_A_READER`. لا تقيس
هنا وظيفةً نحويةً، ولا تقارن دعوى مفعوليةٍ بأخرى، ولا تُنشئ تسجيلًا قَبْليًّا
لقياسٍ لم يُؤذَن به. تُحصي أعمدةَ ملفّاتٍ خارجيةٍ إحصاءً، وتُودِع بصمتَها وطولَها
ورخصتَها، ثمّ تقف.

`OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED`: تُسمّى هذه قبل أن يُكتَب قارئٌ واحد، لأنّها
خاصّةٌ معلومةٌ في مخطَّط Universal Dependencies نفسِه لا اكتشافٌ يُنتظَر: التمييزُ
بين `obj` و`obl` في العربية يستند جزئيًّا إلى الحالة وإلى وجود حرف جرّ، فمن قاس
`obj` بهذه المدوَّنة ثمّ سمّى نتيجتَه «مستقلّةً عن الحالة» ادّعى استقلالًا لم
يحصل. وتسميتُها هنا سدٌّ لثغرةٍ سُمِّيت في الجولة الماضية متأخّرةً بعد الرقم لا
قبلَه (`ACCUSATIVE_IS_NOT_OBJECTHOOD`).

ومع ذلك فالإحصاءُ المُودَع هنا يُظهِر أنّ الطبقتين ليستا واحدة: في
`ar_padt-ud-train` ثلاثٌ وعشرون ألفَ كلمةٍ موسومةٍ `Case=Acc` وخمسةُ آلافٍ
وأربعُمئةٍ وتسعٌ وأربعون منها فقط علاقتُها `obj`. فالحالةُ وحدَها تُفرِط في
التنبّؤ بالمفعولية إفراطًا يزيد على أربعة أضعاف — وهذا هو الضبطُ السلبيُّ عينُه،
مقيسًا من البايتات لا مُفترَضًا.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from alghanem.arabic.irab_corpus_witness import (
    A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE,
    ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE,
    IrabCorpusWitness,
)

__all__ = [
    "ARABIC_UD_CENSUSES",
    "NON_COMMERCIAL_IS_NOT_THIS_TREES_LICENCE_NOTE",
    "OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED_NOTE",
    "REGISTER_IS_NEWSWIRE_NOT_QURANIC_NOTE",
    "STEP_ZERO_IS_NOT_A_READER_NOTE",
    "SURFACE_WITHHELD_IS_NOT_A_CORPUS_NOTE",
    "UD_ARABIC_NYUAD_TEST_CENSUS",
    "UD_ARABIC_PADT_DEV_CENSUS",
    "UD_ARABIC_PADT_TEST_CENSUS",
    "UD_ARABIC_PADT_TRAIN_CENSUS",
    "UD_ARABIC_PUD_TEST_CENSUS",
    "UD_CLASSICAL_ARABIC_DOES_NOT_EXIST_NOTE",
    "UD_RELATION_LAYER_NAMED_RESIDUALS",
    "UNVOCALIZED_FORMS_ARE_NOT_CARRIER_STATE_INPUT_NOTE",
    "UdRelationLayerCensus",
    "UdRelationLayerCensusError",
    "UdRelationLayerOutcome",
]


class UdRelationLayerCensusError(ValueError):
    """تُرفَع حين يُوصَف إحصاءُ خطوةٍ صفر وصفًا لا يُعاد به اشتقاقُه."""


class UdRelationLayerOutcome(Enum):
    """نتيجةُ خطوةِ الصفر، ثلاثُ قيمٍ مغلقةٍ لا رابعَ لها."""

    RELATION_LAYER_PRESENT = "relation_layer_present"
    RELATION_LAYER_PRESENT_BUT_LICENCE_BLOCKED = (
        "relation_layer_present_but_licence_blocked"
    )
    RELATION_LAYER_ABSENT = "relation_layer_absent"


OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED_NOTE: Final[str] = (
    "ObjVsOblIsPartlyCaseDefined: التمييزُ بين `obj` و`obl` في مخطَّط UD للعربية "
    "يستند جزئيًّا إلى الحالة وإلى وجود حرف جرٍّ تابع؛ فقياسُ المفعولية بهذه "
    "المدوَّنة ليس مستقلًّا عن الحالة استقلالًا تامًّا، ومن سمّاه كذلك ادّعى "
    "استقلالًا لم يحصل. وهذه خاصّةُ مخطَّطٍ معلومةٌ سلفًا لا اكتشافٌ يُنتظَر"
)

UD_CLASSICAL_ARABIC_DOES_NOT_EXIST_NOTE: Final[str] = (
    "UdClassicalArabicDoesNotExist: لا مستودعَ باسم `UD_Classical_Arabic` في "
    "منظّمة Universal Dependencies؛ فُحِص فأعاد 404. والمدوَّناتُ العربيةُ "
    "الموجودةُ فيها حديثةٌ أو لهجيّة، فلا يُقال «كلاسيكية» عن شيءٍ منها"
)

REGISTER_IS_NEWSWIRE_NOT_QURANIC_NOTE: Final[str] = (
    "RegisterIsNewswireNotQuranic: مدوَّنتا PADT وPUD نصٌّ صحفيٌّ حديث، والمدوَّنةُ "
    "التي قيس عليها كلُّ ما سبق في هذه الشجرة نصٌّ قرآنيّ؛ فأيُّ رقمٍ يخرج من "
    "هنا لا يُنقَل إلى تلك دون تسميةِ اختلاف المستوى اللغويّ"
)

SURFACE_WITHHELD_IS_NOT_A_CORPUS_NOTE: Final[str] = (
    "SurfaceWithheldIsNotACorpus: في `ar_nyuad` عمودا `HEAD` و`DEPREL` مملوءان، "
    "وعمودا `FORM` و`LEMMA` شُرطةٌ سفليةٌ في كلِّ سطرٍ من أربعةٍ وسبعين ألف سطر — "
    "نُزِعت الصورُ لأنّ نصَّها الأصليَّ مرخَّصٌ من LDC. فطبقةُ العلاقات حاضرةٌ "
    "والكلماتُ غائبة، ولا يُقرَأ حاملٌ ولا حالةٌ من شُرطة"
)

NON_COMMERCIAL_IS_NOT_THIS_TREES_LICENCE_NOTE: Final[str] = (
    "NonCommercialIsNotThisTreesLicence: رخصةُ PADT هي CC BY-NC-SA 3.0 ورخصةُ "
    "هذه الشجرة MIT؛ فلا بايتاتٌ تُنسَخ، والمُودَعُ بصمةٌ وطولٌ ورخصةٌ فحسب، "
    "ويبقى قيدُ «غير التجاريّ» قائمًا على كلِّ استعمالٍ لاحقٍ لتلك البايتات"
)

UNVOCALIZED_FORMS_ARE_NOT_CARRIER_STATE_INPUT_NOTE: Final[str] = (
    "UnvocalizedFormsAreNotCarrierStateInput: عمودُ `FORM` في PADT وPUD غيرُ "
    "مشكولٍ في الأعمّ الأغلب؛ وPADT وحدَها تحمل الصورةَ المشكولةَ في عمود `MISC` "
    "تحت `Vform`، وPUD لا تحملها البتّة. فمن أراد إطعامَ `CarrierStateCodec` من "
    "هنا فليُسمِّ أيَّ عمودٍ أطعمَه، ولا يقرأ حركةً من صورةٍ لا حركةَ فيها"
)

STEP_ZERO_IS_NOT_A_READER_NOTE: Final[str] = (
    "StepZeroIsNotAReader: هذه الوحدةُ إحصاءُ أعمدةٍ وإيداعُ بصماتٍ فحسب؛ لا "
    "تقيس وظيفةً نحويةً، ولا تقارن دعوى مفعوليةٍ بأخرى، ولا تُغني عن تسجيلٍ "
    "قَبْليٍّ مجمَّدٍ يسبق أيَّ قياسٍ لاحق"
)

UD_RELATION_LAYER_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ObjVsOblIsPartlyCaseDefined": OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED_NOTE,
    "UdClassicalArabicDoesNotExist": UD_CLASSICAL_ARABIC_DOES_NOT_EXIST_NOTE,
    "RegisterIsNewswireNotQuranic": REGISTER_IS_NEWSWIRE_NOT_QURANIC_NOTE,
    "SurfaceWithheldIsNotACorpus": SURFACE_WITHHELD_IS_NOT_A_CORPUS_NOTE,
    "NonCommercialIsNotThisTreesLicence": (
        NON_COMMERCIAL_IS_NOT_THIS_TREES_LICENCE_NOTE
    ),
    "UnvocalizedFormsAreNotCarrierStateInput": (
        UNVOCALIZED_FORMS_ARE_NOT_CARRIER_STATE_INPUT_NOTE
    ),
    "StepZeroIsNotAReader": STEP_ZERO_IS_NOT_A_READER_NOTE,
    "AMirrorIsNotTheUpstream": A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE,
}

_RESULT_BEARING_WORDS: Final[frozenset[str]] = frozenset(
    {"outcome", "verdict", "decision", "usable", "adopted", "accepted"}
)


@dataclass(frozen=True, slots=True)
class UdRelationLayerCensus:
    """إحصاءُ أعمدةِ ملفِّ CoNLL-U واحدٍ مُسمّى ببصمته وطوله ورخصته.

    لا حقلَ نتيجةٍ في هذا الإحصاء؛ و`outcome` خاصّيّةٌ تُشتقّ من الأعداد، فمن
    أراد تبديلَ النتيجة بدَّل العددَ الذي يُعيد الأنبوبُ اشتقاقَه فيُفتضَح.
    """

    witness: IrabCorpusWitness
    treebank: str
    sentences: int
    tokens: int
    head_populated_tokens: int
    deprel_populated_tokens: int
    form_bearing_tokens: int
    obj_tokens: int
    obl_tokens: int
    nsubj_tokens: int
    accusative_tokens: int
    accusative_obj_tokens: int

    def __post_init__(self) -> None:
        if not isinstance(self.witness, IrabCorpusWitness):
            raise UdRelationLayerCensusError(
                "الإحصاءُ مربوطٌ بشاهدٍ خارجيٍّ مُبصَّم؛ وإحصاءٌ بلا شاهدٍ رقمٌ بلا ملفّ."
            )
        if not self.treebank.strip():
            raise UdRelationLayerCensusError("اسمُ المدوَّنة نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
        counts = {
            "sentences": self.sentences,
            "tokens": self.tokens,
            "head_populated_tokens": self.head_populated_tokens,
            "deprel_populated_tokens": self.deprel_populated_tokens,
            "form_bearing_tokens": self.form_bearing_tokens,
            "obj_tokens": self.obj_tokens,
            "obl_tokens": self.obl_tokens,
            "nsubj_tokens": self.nsubj_tokens,
            "accusative_tokens": self.accusative_tokens,
            "accusative_obj_tokens": self.accusative_obj_tokens,
        }
        for label, number in counts.items():
            if not isinstance(number, int) or number < 0:
                raise UdRelationLayerCensusError(
                    f"`{label}` عددٌ صحيحٌ غيرُ سالب؛ وعددٌ سالبٌ ليس إحصاءً."
                )
        if self.tokens < 1 or self.sentences < 1:
            raise UdRelationLayerCensusError(
                "ملفٌّ بلا جملةٍ أو بلا كلمةٍ لا يُحصى؛ وصفرٌ هنا يعني أنّ القارئ "
                "لم يقرأ، لا أنّ الملفَّ فارغ."
            )
        for label in (
            "head_populated_tokens",
            "deprel_populated_tokens",
            "form_bearing_tokens",
            "obj_tokens",
            "obl_tokens",
            "nsubj_tokens",
            "accusative_tokens",
        ):
            if counts[label] > self.tokens:
                raise UdRelationLayerCensusError(
                    f"`{label}` يزيد على عدد الكلمات؛ وجزءٌ أكبرُ من كلٍّ خطأُ عدّ."
                )
        if self.accusative_obj_tokens > min(self.accusative_tokens, self.obj_tokens):
            raise UdRelationLayerCensusError(
                "الكلماتُ المنصوبةُ الموسومةُ `obj` جزءٌ من المنصوبات ومن "
                "`obj` معًا؛ ولا يزيد الجزءُ على أيِّ كلٍّ من الكلَّين."
            )

    @property
    def outcome(self) -> UdRelationLayerOutcome:
        """النتيجةُ مُشتقّةٌ من الأعداد لا مُودَعةٌ حقلًا."""

        if self.head_populated_tokens == 0 or self.deprel_populated_tokens == 0:
            return UdRelationLayerOutcome.RELATION_LAYER_ABSENT
        if self.form_bearing_tokens == 0:
            return UdRelationLayerOutcome.RELATION_LAYER_PRESENT_BUT_LICENCE_BLOCKED
        return UdRelationLayerOutcome.RELATION_LAYER_PRESENT

    @property
    def relation_layer_is_complete(self) -> bool:
        """أمملوءٌ العمودان في كلِّ سطرٍ لا في بعضه."""

        return (
            self.head_populated_tokens == self.tokens
            and self.deprel_populated_tokens == self.tokens
        )

    @property
    def non_obj_accusative_tokens(self) -> int:
        """المنصوباتُ التي ليست `obj` — الضبطُ السلبيُّ معدودًا لا مُفترَضًا."""

        return self.accusative_tokens - self.accusative_obj_tokens


def _refuse_result_bearing_fields() -> None:
    """يمنع عند الاستيراد إيداعَ نتيجةٍ حقلًا بدل اشتقاقها."""

    for field in fields(UdRelationLayerCensus):
        for word in field.name.split("_"):
            if word in _RESULT_BEARING_WORDS:
                raise UdRelationLayerCensusError(
                    f"`{field.name}` حقلٌ يحمل نتيجةً؛ والنتيجةُ تُشتقّ من "
                    f"الأعداد ولا تُودَع."
                )


_refuse_result_bearing_fields()


UD_ARABIC_PUD_TEST_CENSUS: Final[UdRelationLayerCensus] = UdRelationLayerCensus(
    witness=IrabCorpusWitness(
        corpus="Universal Dependencies Arabic-PUD",
        version="CoNLL-U, master branch as measured",
        upstream="https://github.com/UniversalDependencies/UD_Arabic-PUD",
        measured_mirror="raw.githubusercontent.com/UniversalDependencies/UD_Arabic-PUD",
        measured_path="ar_pud-ud-test.conllu",
        sha256="befc6dd18b5b8803644ae8208e2e5f52c0957a36437627c05110914ec42281a3",
        byte_length=2_401_101,
        licenses=("Creative Commons BY-SA 3.0",),
        required_attribution_links=(
            "https://github.com/UniversalDependencies/UD_Arabic-PUD",
            "https://creativecommons.org/licenses/by-sa/3.0/",
        ),
        attribution_requirement=(
            "تشترط رخصةُ `CC BY-SA 3.0` المنصوصةُ في `LICENSE.txt` بالمستودع "
            "التصريحَ بالمصدر والإبقاءَ على الرخصة نفسِها في أيِّ عملٍ مشتقّ؛ "
            "ولم تُنسَخ بايتةٌ واحدةٌ إلى هذه الشجرة، فالمُودَعُ بصمةٌ وطولٌ ورخصة. "
            + ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE
        ),
        annotation_note=(
            "ملفٌّ بصيغة CoNLL-U عشرةِ أعمدة، وعمودا `HEAD` و`DEPREL` مملوءان "
            "في كلِّ سطرِ كلمة. وليس في عمود `MISC` حقلُ `Vform`، فالصورُ غيرُ "
            "مشكولةٍ ولا يُشتقُّ منها شكلٌ. "
            + UNVOCALIZED_FORMS_ARE_NOT_CARRIER_STATE_INPUT_NOTE
        ),
    ),
    treebank="ar_pud",
    sentences=1_000,
    tokens=20_747,
    head_populated_tokens=20_747,
    deprel_populated_tokens=20_747,
    form_bearing_tokens=20_747,
    obj_tokens=742,
    obl_tokens=2_065,
    nsubj_tokens=1_510,
    accusative_tokens=1_415,
    accusative_obj_tokens=522,
)


def _padt_witness(
    measured_path: str, sha256: str, byte_length: int
) -> IrabCorpusWitness:
    return IrabCorpusWitness(
        corpus="Universal Dependencies Arabic-PADT",
        version="CoNLL-U, master branch as measured",
        upstream="https://github.com/UniversalDependencies/UD_Arabic-PADT",
        measured_mirror=(
            "raw.githubusercontent.com/UniversalDependencies/UD_Arabic-PADT"
        ),
        measured_path=measured_path,
        sha256=sha256,
        byte_length=byte_length,
        licenses=("Creative Commons BY-NC-SA 3.0",),
        required_attribution_links=(
            "https://github.com/UniversalDependencies/UD_Arabic-PADT",
            "http://ufal.mff.cuni.cz/padt/",
            "http://creativecommons.org/licenses/by-nc-sa/3.0/",
        ),
        attribution_requirement=(
            "تشترط رخصةُ `CC BY-NC-SA 3.0` المنصوصةُ في `LICENSE.txt` بالمستودع "
            "التصريحَ بالمصدر ومنعَ الاستعمال التجاريّ والإبقاءَ على الرخصة "
            "نفسِها في أيِّ عملٍ مشتقّ؛ ولم تُنسَخ بايتةٌ واحدةٌ إلى هذه الشجرة. "
            + NON_COMMERCIAL_IS_NOT_THIS_TREES_LICENCE_NOTE
        ),
        annotation_note=(
            "ملفٌّ بصيغة CoNLL-U عشرةِ أعمدة، وعمودا `HEAD` و`DEPREL` مملوءان "
            "في كلِّ سطرِ كلمة، ووَسْمُهما — بتصريح ترويسة المستودع — يدويٌّ في "
            "أصل PADT ثمّ حُوِّل آليًّا إلى UD. والصورةُ في `FORM` غيرُ مشكولة، "
            "والمشكولةُ في `MISC` تحت `Vform`. "
            + UNVOCALIZED_FORMS_ARE_NOT_CARRIER_STATE_INPUT_NOTE
        ),
    )


UD_ARABIC_PADT_TRAIN_CENSUS: Final[UdRelationLayerCensus] = UdRelationLayerCensus(
    witness=_padt_witness(
        "ar_padt-ud-train.conllu",
        "f0b56962b340f5325bb5d293f47717522e706112c19029e82c225355c6d65e85",
        40_698_415,
    ),
    treebank="ar_padt (train)",
    sentences=6_075,
    tokens=223_881,
    head_populated_tokens=223_881,
    deprel_populated_tokens=223_881,
    form_bearing_tokens=223_881,
    obj_tokens=6_710,
    obl_tokens=17_405,
    nsubj_tokens=13_933,
    accusative_tokens=23_002,
    accusative_obj_tokens=5_449,
)

UD_ARABIC_PADT_DEV_CENSUS: Final[UdRelationLayerCensus] = UdRelationLayerCensus(
    witness=_padt_witness(
        "ar_padt-ud-dev.conllu",
        "0d95ee511cf2f26a64e229e86e5e9b37851555ebc8b53c5ebb261f2dfbc185e7",
        5_397_917,
    ),
    treebank="ar_padt (dev)",
    sentences=909,
    tokens=30_239,
    head_populated_tokens=30_239,
    deprel_populated_tokens=30_239,
    form_bearing_tokens=30_239,
    obj_tokens=882,
    obl_tokens=2_341,
    nsubj_tokens=1_925,
    accusative_tokens=3_105,
    accusative_obj_tokens=732,
)

UD_ARABIC_PADT_TEST_CENSUS: Final[UdRelationLayerCensus] = UdRelationLayerCensus(
    witness=_padt_witness(
        "ar_padt-ud-test.conllu",
        "793c87bf173d491af2092ef7f87b04a2cf6c596490e7347a2065058a053a6389",
        5_163_066,
    ),
    treebank="ar_padt (test)",
    sentences=680,
    tokens=28_264,
    head_populated_tokens=28_264,
    deprel_populated_tokens=28_264,
    form_bearing_tokens=28_264,
    obj_tokens=879,
    obl_tokens=2_240,
    nsubj_tokens=1_781,
    accusative_tokens=2_979,
    accusative_obj_tokens=736,
)

UD_ARABIC_NYUAD_TEST_CENSUS: Final[UdRelationLayerCensus] = UdRelationLayerCensus(
    witness=IrabCorpusWitness(
        corpus="Universal Dependencies Arabic-NYUAD",
        version="CoNLL-U, master branch as measured",
        upstream="https://github.com/UniversalDependencies/UD_Arabic-NYUAD",
        measured_mirror=(
            "raw.githubusercontent.com/UniversalDependencies/UD_Arabic-NYUAD"
        ),
        measured_path="ar_nyuad-ud-test.conllu",
        sha256="bc4670763e0e3f282ef079b55af0c58d73ac541aafc421161eb4d904bbaca52b",
        byte_length=5_856_617,
        licenses=(
            "Creative Commons BY-SA 4.0 (annotation only)",
            "Linguistic Data Consortium (Penn Arabic Treebank text, not included)",
        ),
        required_attribution_links=(
            "https://github.com/UniversalDependencies/UD_Arabic-NYUAD",
            "http://creativecommons.org/licenses/by-sa/4.0/",
        ),
        attribution_requirement=(
            "ترخِّص `LICENSE.txt` التوسيمَ وحدَه بـ`CC BY-SA 4.0`، والنصُّ "
            "الأصليُّ مرخَّصٌ من LDC ولم يُضمَّن؛ فمن أراد الصورَ لزِمَه اقتناءُ "
            "رخصةٍ أخرى. " + ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE
        ),
        annotation_note=(
            "ملفٌّ بصيغة CoNLL-U عشرةِ أعمدة: عمودا `HEAD` و`DEPREL` مملوءان في "
            "كلِّ سطر، وعمودا `FORM` و`LEMMA` شُرطةٌ سفليةٌ في كلِّ سطر. "
            + SURFACE_WITHHELD_IS_NOT_A_CORPUS_NOTE
        ),
    ),
    treebank="ar_nyuad (test)",
    sentences=1_963,
    tokens=74_125,
    head_populated_tokens=74_125,
    deprel_populated_tokens=74_125,
    form_bearing_tokens=0,
    obj_tokens=11_970,
    obl_tokens=0,
    nsubj_tokens=2_944,
    accusative_tokens=7_523,
    accusative_obj_tokens=2_635,
)

ARABIC_UD_CENSUSES: Final[tuple[UdRelationLayerCensus, ...]] = (
    UD_ARABIC_PUD_TEST_CENSUS,
    UD_ARABIC_PADT_TRAIN_CENSUS,
    UD_ARABIC_PADT_DEV_CENSUS,
    UD_ARABIC_PADT_TEST_CENSUS,
    UD_ARABIC_NYUAD_TEST_CENSUS,
)
