"""تسجيلٌ قبْليٌّ للمُحلِّل البنيويّ الموحَّد، ومنازلُ طبقاته السبع المتفاوتة.

وصلت هذه الشجرةَ أداةٌ مقترحةٌ باسم `word_structure_dictionary.py` تُخرِج
«القاموسَ الداخليَّ الكامل» لأيّ كلمةٍ عربيّةٍ مُشكَّلة، مُجمِّعةً سبعَ طبقاتٍ
في نقطةِ دخولٍ واحدة. والأداةُ ووحداتُها الرافدةُ الثلاث
(`p_extractor_pilot1`، `syllabifier_wazn_pilot1`، `samit_sifat_vs_makhraj_pilot1`)
**ليست في هذه الشجرة**، ولم تُودَع بايتاتُها فيها، فجنسُ ما وصل
`PROSE_FROM_ANOTHER_CONVERSATION` لا قياسَ هذه الشجرة
(`gflk_specification_deposit.ProvenanceGenus`).

وهذه الوحدةُ **تسجيلٌ قبْليٌّ لا مُحلِّل**، على منوال
`compound_layer_preregistration`: لا تحمل دالّةَ تحليلٍ واحدة، ولا مخرجَ طبقةٍ
واحدًا، ولا حقلَ نتيجةٍ البتّة — وحارسٌ عند الاستيراد يمنع تسلُّلَ حقلٍ كهذا
لاحقًا. وما تفعله أنّها تُجمّد، قبل أيِّ قياس، **منزلةَ كلِّ طبقةٍ** وشرطَ
دخولها، وتُسجِّل أوّلَ تصادمين بين قاموس المحادثة الأخرى ومفردةِ هذه الشجرة.

`AGGREGATION_DOES_NOT_LEVEL_EPISTEMIC_RANK`: الطبقاتُ السبعُ متفاوتةُ المنزلة
تفاوتًا جنسيًّا لا درجيًّا: منها المقيسُ على مرمازٍ قائم، ومنها المستورَدُ خلف
حاجزٍ مفتوح، ومنها المتعذّرُ من العلامات المكتوبة، ومنها الفرضُ المُعلَنُ
العطب. وجمعُها في قاموسٍ واحدٍ متجانسِ الشكل يُسوّي بينها في القراءة، فيُستشهَد
بعد جلساتٍ بالطبقة المستورَدة كأنّها مقيسةٌ هنا — وهو عينُ ما يمنعه
`AN_IMPORTED_TABLE_IS_NOT_A_CLAIM_OF_THIS_TREE` في
`gflk_feature_table_import_barrier`. فكلُّ طبقةٍ تحمل منزلتَها من مفردةٍ مغلقة،
والتجميعُ لا يُسقِطها.

`AN_UNMEASURED_LAYER_IS_A_SEPARATE_REFUSAL_FIELD_NOT_A_NULL`: الأداةُ الواردةُ
تكتب `wazn=None` و`syllables=None` عند تعذّر الحلّ، فيستوي في السجلّ «لم
يُقَس» و«قِيس فكان لا شيء». والتعذّرُ مفردةٌ مستقلّةٌ لا تُجمَع مع مفردة
الفشل (`REFUSAL_IS_NOT_FAILURE_TO_DISCRIMINATE` في
`morphological_necessity_measurement`)، فيُخرَج في **حقلِ تعذّرٍ منفصلٍ
مُسمًّى** لا في قيمةٍ خاليةٍ تُقرأ نتيجةً.

`A_POSITIONAL_INFERENCE_IS_NOT_A_READING_OF_THE_WRITTEN_MARKS`: هذا أوّلُ
تصادمٍ حُسِم فعلًا. تعريفُ `IMPLICIT_SUKUN` في القاموس الوارد يستثني «الوصل»
صراحةً، وتصنيفُ `ALIF_WASL` فيه يقع بمعيارٍ **موضعيّ** (أوّلُ حرفٍ + ألفٌ
عارية) لا بعلامةٍ مكتوبةٍ تخصّه. والشجرةُ قرّرت قبل ذلك
`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`
(`ibtida_wasl_waqf_registration`): ألفُ «الْحَمْدُ» لا تحمل علامةً أصلًا،
فمنزلتُها `لا_حالة_مكتوبة` متعذّرةُ القياس. والاستدلالُ الموضعيّ قد يكون
صادقًا، ولا يصير بذلك قراءةً للعلامات؛ فيُفصَل في منزلةٍ مستقلّةٍ ولا يُدمَج
صامتًا داخل حالةٍ واحدة.

`THE_SAME_CONCEPT_UNDER_TWO_NAMES_IS_ONE_ENTRY_NOT_TWO`: وهذا التصادمُ الثاني،
وقد حُسِم بالتسمية القائمة: `SUKUN`/`IMPLICIT_SUKUN` في القاموس الوارد هما
بعينهما `CarrierState.SUKUN_EXPLICIT`/`CarrierState.SUKUN_IMPLICIT`، مفهومًا لا
تسميةً فقط. والمفردةُ القائمة مغلقةٌ ومُسجَّلةٌ قبلُ، فهي المرجع؛ وإبقاءُ
الاسمين يُنتج بعد جلساتٍ اسمين لشيءٍ واحدٍ يُختار بينهما بما يوافق نتيجةً
مرغوبة، وهو ما يمنعه `THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOT_AFTER`.

`THE_GLOSSARY_TEXT_HAS_NOT_ARRIVED_IN_FULL`: لم يصل من القاموس إلّا صدرُه
(حالاتُ الحركة القصيرة، والسكونان)، وانقطع النقلُ عند `SHADDA_`. فلا تُودَع
بايتاتُه ولا تُبصَّم، ولا يُسجَّل تطابقٌ ولا تعارضٌ لفئةٍ لم يصل نصُّها؛
والفئاتُ غيرُ الواصلة تُسجَّل في حقلِ «لم يصل نصُّها» لا تُخمَّن من اسمها.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`، ولا تقرأ هذه الوحدةَ وحدةٌ فيه. ولا
تُرفَع بها حواجزُ المخرج/الصفة، ولا حاجزُ «أل»/الوصل، ولا يُصدَر بها تصنيفُ
مجرّدٍ أو مزيد.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import CarrierState

__all__ = [
    "AGGREGATION_DOES_NOT_LEVEL_EPISTEMIC_RANK_NOTE",
    "AN_UNMEASURED_LAYER_IS_A_SEPARATE_REFUSAL_FIELD_NOT_A_NULL_NOTE",
    "A_POSITIONAL_INFERENCE_IS_NOT_A_READING_OF_THE_WRITTEN_MARKS_NOTE",
    "DICTIONARY_LAYER_REGISTRATIONS",
    "GLOSSARY_CATEGORIES_NOT_YET_SUPPLIED",
    "GLOSSARY_CONCORDANCE",
    "ROLE_READINGS_OVER_THE_EXISTING_UNIT",
    "THE_GLOSSARY_TEXT_HAS_NOT_ARRIVED_IN_FULL_NOTE",
    "THE_SAME_CONCEPT_UNDER_TWO_NAMES_IS_ONE_ENTRY_NOT_TWO_NOTE",
    "ConcordanceReading",
    "DictionaryLayer",
    "GlossaryConcordanceRow",
    "LayerEpistemicStanding",
    "LayerRegistration",
    "RoleReading",
    "UnsuppliedGlossaryCategory",
    "WordStructureDictionaryPreregistrationError",
    "existing_carrier_state_names",
    "layer_registration",
]


class WordStructureDictionaryPreregistrationError(ValueError):
    """رفضٌ عند الإنشاء: طبقةٌ بلا شرطِ دخول، أو صفٌّ بلا موضعٍ أو بلا مرجع."""


class DictionaryLayer(Enum):
    """الطبقاتُ السبعُ المطلوبةُ في القاموس، بترتيب الطلب؛ لا ثامنةَ لها هنا."""

    LETTERS = "الحرف_والحركة"
    SYLLABLES_AND_WAZN = "المقطع_والوزن"
    PHONETIC_FEATURES = "المخرج_والصفة"
    SHADDA_ANALYSIS = "الشدّة_ومصدرها"
    TANWEEN_ANALYSIS = "التنوين_ونوعه"
    AL_ANALYSIS = "أل_تعريفًا_أو_وصلًا"
    JARAD_ANALYSIS = "مجرد_أو_مزيد"


class LayerEpistemicStanding(Enum):
    """منزلةُ الطبقة. مفردةٌ رباعيّةٌ مغلقة، ليس فيها `مقبولةٌ بلا قياس`."""

    MEASURED_BY_AN_EXISTING_CODEC = "مقيسٌ على مرمازٍ قائم"
    IMPORTED_BEHIND_AN_OPEN_BARRIER = "مستورَدٌ خلف حاجزٍ مفتوح"
    UNDECIDABLE_FROM_THE_WRITTEN_MARKS = "متعذّرٌ من العلامات المكتوبة"
    HYPOTHESIS_WITH_A_DECLARED_DEFECT = "فرضٌ مُعلَنُ العطب"


class ConcordanceReading(Enum):
    """قراءةُ صفِّ المقابلة. ليس فيها `مقبولٌ`؛ القبولُ ليس من شأن التسجيل."""

    SAME_CONCEPT_ONE_ENTRY = "المفهومُ واحدٌ والمدخلُ واحد"
    ROLE_OVER_AN_EXISTING_UNIT = "دورٌ على وحدةٍ قائمةٍ لا عضوٌ جديد"
    CONFLATES_TWO_EPISTEMIC_RANKS = "يخلط منزلتين معرفيّتين"


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "result",
    "outcome_value",
    "verdict",
    "birth",
    "certificate",
    "classification",
    "proof",
    "value_when_unmeasured",
)


@dataclass(frozen=True, slots=True)
class LayerRegistration:
    """تسجيلُ طبقةٍ واحدة: منزلتُها، ومصدرُها، وشرطُ دخولها، وحقلُ تعذّرها."""

    layer: DictionaryLayer
    standing: LayerEpistemicStanding
    source_in_this_tree: str
    entry_condition: str
    refusal_field_name: str
    what_the_refusal_field_says: str

    def __post_init__(self) -> None:
        if not isinstance(self.layer, DictionaryLayer):
            raise WordStructureDictionaryPreregistrationError(
                "الطبقةُ عضوٌ في مفردتها المغلقة"
            )
        if not isinstance(self.standing, LayerEpistemicStanding):
            raise WordStructureDictionaryPreregistrationError(
                "منزلةُ الطبقة عضوٌ في مفردتها المغلقة"
            )
        for name in (
            "source_in_this_tree",
            "entry_condition",
            "refusal_field_name",
            "what_the_refusal_field_says",
        ):
            if not str(getattr(self, name)).strip():
                raise WordStructureDictionaryPreregistrationError(
                    "طبقةٌ بلا مصدرٍ أو بلا شرطِ دخولٍ أو بلا حقلِ تعذّرٍ مُسمًّى "
                    "طبقةٌ تُقرأ نتيجتُها من فراغها"
                )
        if self.refusal_field_name.lower() in ("none", "null", ""):
            raise WordStructureDictionaryPreregistrationError(
                AN_UNMEASURED_LAYER_IS_A_SEPARATE_REFUSAL_FIELD_NOT_A_NULL_NOTE
            )


@dataclass(frozen=True, slots=True)
class GlossaryConcordanceRow:
    """صفُّ مقابلةٍ بين فئةٍ في القاموس الوارد وما تقوله هذه الشجرة."""

    glossary_category: str
    glossary_says: str
    this_tree_says: str
    tree_reference: str
    reading: ConcordanceReading
    what_was_settled: str

    def __post_init__(self) -> None:
        if not isinstance(self.reading, ConcordanceReading):
            raise WordStructureDictionaryPreregistrationError(
                "قراءةُ الصفّ عضوٌ في مفردتها المغلقة"
            )
        for name in (
            "glossary_category",
            "glossary_says",
            "this_tree_says",
            "tree_reference",
            "what_was_settled",
        ):
            if not str(getattr(self, name)).strip():
                raise WordStructureDictionaryPreregistrationError(
                    "صفُّ مقابلةٍ بلا موضعٍ أو بلا مرجعٍ في الشجرة صفٌّ يُقرأ "
                    "ترجيحًا لا مقابلة"
                )


@dataclass(frozen=True, slots=True)
class RoleReading:
    """اسمٌ مقترحٌ يُقرأ دورًا على وحدةٍ قائمة، بحقولها التي يُقرأ منها."""

    proposed_name: str
    existing_unit_fields: tuple[str, ...]
    grounds: str

    def __post_init__(self) -> None:
        if not self.proposed_name.strip() or not self.grounds.strip():
            raise WordStructureDictionaryPreregistrationError(
                "قراءةُ دورٍ بلا اسمٍ أو بلا مُبرِّر"
            )
        if not self.existing_unit_fields:
            raise WordStructureDictionaryPreregistrationError(
                "دورٌ بلا حقولٍ قائمةٍ يُقرأ منها ليس دورًا بل عضوًا جديدًا " "سُمِّي دورًا"
            )


@dataclass(frozen=True, slots=True)
class UnsuppliedGlossaryCategory:
    """فئةٌ في القاموس لم يصل نصُّها، فلا تُقابَل ولا تُخمَّن من اسمها."""

    category_name: str
    why_it_is_not_compared: str

    def __post_init__(self) -> None:
        if not self.category_name.strip() or not self.why_it_is_not_compared.strip():
            raise WordStructureDictionaryPreregistrationError(
                "فئةٌ غيرُ واصلةٍ بلا سببٍ مُسمًّى"
            )


def existing_carrier_state_names() -> tuple[str, ...]:
    """أسماءُ حالات الحامل القائمة، مقروءةً من المفردة لا منسوخةً هنا."""

    return tuple(state.name for state in CarrierState)


def layer_registration(layer: DictionaryLayer) -> LayerRegistration:
    """تسجيلُ طبقةٍ بعينها، مقروءًا من الجدول المُجمَّد لا مُنشأً عند النداء."""

    for registration in DICTIONARY_LAYER_REGISTRATIONS:
        if registration.layer is layer:
            return registration
    raise WordStructureDictionaryPreregistrationError(
        f"لا تسجيلَ للطبقة {layer!r}، والطبقاتُ سبعٌ مغلقة"
    )


DICTIONARY_LAYER_REGISTRATIONS: Final[tuple[LayerRegistration, ...]] = (
    LayerRegistration(
        layer=DictionaryLayer.LETTERS,
        standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
        source_in_this_tree=(
            "`encoding/carrier_state_candidate.CarrierStateCodec` ومفردتُه "
            "`CarrierState` المغلقةُ بسبعة أعضاء"
        ),
        entry_condition=(
            "تُشتَقّ الحالاتُ من المرماز القائم لا من مفردةٍ مُبتكَرة، وأرضيّةُ "
            "القبول مكتوبةٌ قبل القياس في "
            "`gflk_state_machine_registration.P_EXTRACTOR_ACCEPTANCE_CONDITION`: "
            "لا تقلّ نسبةُ الذهاب والإياب عمّا يحقّقه المرمازُ اليوم، والكلماتُ "
            "الستُّ المعطوبةُ حالاتُ اختبارٍ بأعيانها"
        ),
        refusal_field_name="letters_unread",
        what_the_refusal_field_says=(
            "الحواملُ التي رفضها المرمازُ عند الإنشاء تُسمّى بأعيانها، ولا تُقرأ "
            "حاملًا بلا حالة"
        ),
    ),
    LayerRegistration(
        layer=DictionaryLayer.SYLLABLES_AND_WAZN,
        standing=LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT,
        source_in_this_tree=(
            "لا وحدةَ سيلبنةٍ ولا وزنٍ في هذه الشجرة؛ والمصدرُ الوارد "
            "`syllabifier_wazn_pilot1` من محادثةٍ أخرى بلا إيداعٍ ولا بصمة"
        ),
        entry_condition=(
            "وحدةُ سيلبنةٍ في الشجرة، وتصريحٌ بأنّ الوزنَ **إسقاطٌ مشتقٌّ** لا "
            "كائنٌ صرفيٌّ مولود — على منوال "
            "`ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY` — وأرضيّةُ قبولٍ "
            "مكتوبةٌ قبل قياسها على مدوَّنةٍ مُبصَّمة"
        ),
        refusal_field_name="wazn_unresolved",
        what_the_refusal_field_says=(
            "تعذّرُ الحلِّ يُخرَج باسمه في حقلٍ مستقلّ؛ و`wazn=None` ممنوعٌ لأنّه "
            "يُسوّي «لم يُقَس» بـ«قِيس فكان لا شيء»"
        ),
    ),
    LayerRegistration(
        layer=DictionaryLayer.PHONETIC_FEATURES,
        standing=LayerEpistemicStanding.IMPORTED_BEHIND_AN_OPEN_BARRIER,
        source_in_this_tree=(
            "`classical_makharij_table.CLASSICAL_MAKHARIJ` بستّةَ عشرَ مخرجًا "
            "وفيه حارسٌ يرفض غيرَها؛ وجدولُ الصفة لا نظيرَ له مُبصَّمًا هنا"
        ),
        entry_condition=(
            "رفعُ الحاجزين المفتوحين في "
            "`gflk_feature_table_import_barrier.FEATURE_TABLE_IMPORT_BARRIERS`: "
            "حسمُ تعارضِ ١٣/١٦ **قبل** الاستيراد لا بعده، ومصدرٌ مسمًّى وبصمةُ "
            "بايتاتٍ لجدول الصفة على منوال `imported_feature_vocabulary`"
        ),
        refusal_field_name="phonetic_features_withheld",
        what_the_refusal_field_says=(
            "الطبقةُ محجوزةٌ ما دام الحاجزان `OPEN`؛ ولا تُصدَر منها قيمةٌ "
            "واحدةٌ في هذه الجلسة"
        ),
    ),
    LayerRegistration(
        layer=DictionaryLayer.SHADDA_ANALYSIS,
        standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
        source_in_this_tree=(
            "`GeminationRole.PAIR_START` وحقلُ `gemination` في `CarrierStateUnit`"
        ),
        entry_condition=(
            "تُقرأ الشدّةُ **دورًا** على الوحدة القائمة لا عضوًا جديدًا في "
            "`CarrierState`، حفظًا لـ`A_ROLE_IS_NOT_A_STATE`"
        ),
        refusal_field_name="shadda_source_undecided",
        what_the_refusal_field_says=(
            "تمييزُ «إدغامٍ شمسيّ» من «تضعيفٍ جذريّ» متوقّفٌ على طبقة «أل»، "
            "وهي متعذّرةٌ من العلامات؛ فمصدرُ الشدّة يبقى في حقلِ تعذّرٍ لا "
            "يُنسَب إلى أحدهما"
        ),
    ),
    LayerRegistration(
        layer=DictionaryLayer.TANWEEN_ANALYSIS,
        standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
        source_in_this_tree=(
            "حقلا `tanwin` و`tanwin_alif_seat` و`CarrierSeat.ON_ALEF` في "
            "`CarrierStateUnit`"
        ),
        entry_condition=(
            "يُقرأ التنوينُ ومَقعدُه من حقولِ الوحدة القائمة؛ ولا يُدخَل "
            "`TANWEEN_ALIF_CARRIER` عضوًا في المفردة "
            "(`gflk_state_machine_registration.PROPOSED_STATE_READINGS`)"
        ),
        refusal_field_name="tanween_position_unread",
        what_the_refusal_field_says=(
            "ما لم يُقرأ موضعُه من الحقول القائمة يُسمّى غيرَ مقروء، ولا يُحمَل "
            "على «آخرِ الكلمة» بالافتراض"
        ),
    ),
    LayerRegistration(
        layer=DictionaryLayer.AL_ANALYSIS,
        standing=LayerEpistemicStanding.UNDECIDABLE_FROM_THE_WRITTEN_MARKS,
        source_in_this_tree=(
            "`ibtida_wasl_waqf_registration` وقانونُه "
            "`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`"
        ),
        entry_condition=(
            "مُدخَلٌ معجميٌّ أو صرفيٌّ **منسوبٌ ومُبصَّم** يُميّز همزةَ الوصل؛ "
            "وما دونه فالمعيارُ موضعيٌّ لا قراءةٌ للعلامات، ويبقى في منزلته "
            "مفصولًا. وقائمةُ الموصولات المكتوبةُ في الأداة الواردة "
            "(`MAWSUL_WORDS`) لا تُستعمَل بلا مصدرٍ وبصمة"
        ),
        refusal_field_name="al_undecidable_from_marks",
        what_the_refusal_field_says=(
            "ألفُ «الْحَمْدُ» لا تحمل علامةً أصلًا، فمنزلتُها `لا_حالة_مكتوبة` "
            "متعذّرةُ القياس: لا موافقةٌ ولا مخالفة"
        ),
    ),
    LayerRegistration(
        layer=DictionaryLayer.JARAD_ANALYSIS,
        standing=LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT,
        source_in_this_tree=(
            "لا مصدرَ لها هنا؛ والمعيارُ الوارد (خلوُّ البادئة من سألتمونيها) "
            "مُقِرٌّ في نصّه بأنّه لا يُميّز حرفَ زيادةٍ مُقحَمًا عن أصليٍّ "
            "يصادف كونَه منها"
        ),
        entry_condition=(
            "قياسُ **مقدار** المبالغة على مدوَّنةٍ مُبصَّمة، وتوقّعٌ مكتوبٌ قبل "
            "القياس على منوال `OCP_PREREGISTERED_EXPECTATION`؛ فما لم يُقَس "
            "المقدارُ فالتصنيفُ رقمٌ لا شاهدَ له"
        ),
        refusal_field_name="jarad_overcount_unmeasured",
        what_the_refusal_field_says=(
            "مقدارُ المبالغة في «مزيد» غيرُ معلومٍ ولم يُقَس، فلا تُصدَر قيمةُ "
            "تصنيفٍ أصلًا — لا مع تحذيرٍ ولا بدونه"
        ),
    ),
)


GLOSSARY_CONCORDANCE: Final[tuple[GlossaryConcordanceRow, ...]] = (
    GlossaryConcordanceRow(
        glossary_category="SUKUN",
        glossary_says="سكونٌ صريحٌ مرسومٌ على الحرف",
        this_tree_says=(
            "`CarrierState.SUKUN_EXPLICIT` بعينه: المفهومُ واحدٌ والاسمُ مختلف"
        ),
        tree_reference="`encoding/carrier_state_candidate.CarrierState`",
        reading=ConcordanceReading.SAME_CONCEPT_ONE_ENTRY,
        what_was_settled=(
            "التسميةُ القائمةُ هي المرجع، فمفردتُها مغلقةٌ ومُسجَّلةٌ قبلُ؛ "
            "وإبقاءُ الاسمين يُنتج اسمين لشيءٍ واحدٍ يُختار بينهما بما يوافق "
            "نتيجةً مرغوبة"
        ),
    ),
    GlossaryConcordanceRow(
        glossary_category="IMPLICIT_SUKUN",
        glossary_says=(
            "سكونٌ غيرُ مرسومٍ استُنتِج بنيويًّا: حرفٌ صحيحٌ بلا أيّ علامة، ليس "
            "مدًّا ولا **وصلًا** ولا فارقة"
        ),
        this_tree_says=(
            "`CarrierState.SUKUN_IMPLICIT` يطابقه في أصل المفهوم؛ أمّا استثناءُ "
            "«الوصل» فيفترض تمييزَ همزة الوصل، وهو استدلالٌ موضعيٌّ لا قراءةٌ "
            "لعلامةٍ مكتوبة"
        ),
        tree_reference=(
            "`encoding/carrier_state_candidate.CarrierState` و"
            "`ibtida_wasl_waqf_registration."
            "HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`"
        ),
        reading=ConcordanceReading.CONFLATES_TWO_EPISTEMIC_RANKS,
        what_was_settled=(
            "المفهومُ الأصلُ مدخلٌ واحدٌ بالاسم القائم؛ والاستثناءُ الموضعيُّ "
            "يُفصَل في منزلةٍ مستقلّةٍ ولا يُدمَج صامتًا داخل الحالة، فقد يكون "
            "وصفًا صادقًا ولا يصير بذلك قراءةً للعلامات"
        ),
    ),
    GlossaryConcordanceRow(
        glossary_category="ALIF_WASL",
        glossary_says=("ألفُ وصلٍ تُصنَّف بمعيارٍ موضعيّ: أوّلُ حرفٍ في الكلمة + ألفٌ عارية"),
        this_tree_says=(
            "منزلةُ الموضع `لا_حالة_مكتوبة` وهي **متعذّرةُ القياس**: لا تُقرأ "
            "ساكنةً ولا متحرّكة، ولا يُعرَف كونُها همزةَ وصلٍ إلّا بمعرفةٍ "
            "معجميّةٍ أو صرفيّةٍ ليست في العلامات"
        ),
        tree_reference="`ibtida_wasl_waqf_registration`",
        reading=ConcordanceReading.CONFLATES_TWO_EPISTEMIC_RANKS,
        what_was_settled=(
            "لا تُصدَر قيمةُ «أل» من العلامات وحدها في هذه الجلسة؛ ورفعُ ذلك "
            "بمُدخَلٍ معجميٍّ منسوبٍ ومُبصَّمٍ يُقرأ في حقلٍ منفصلٍ عن الطبقات "
            "المقيسة"
        ),
    ),
    GlossaryConcordanceRow(
        glossary_category="TANWEEN_ALIF_CARRIER",
        glossary_says="حالةٌ مستقلّةٌ لألف التنوين في مفردة الحالات",
        this_tree_says=(
            "اجتماعُ `CarrierSeat.ON_ALEF` مع حقلِ التنوين في الوحدة نفسِها؛ "
            "فالمقترحُ يصف اجتماعَهما لا شيئًا ثالثًا"
        ),
        tree_reference=(
            "`gflk_state_machine_registration.PROPOSED_STATE_READINGS` و"
            "`A_ROLE_IS_NOT_A_STATE_NOTE`"
        ),
        reading=ConcordanceReading.ROLE_OVER_AN_EXISTING_UNIT,
        what_was_settled=(
            "يُقرأ دورًا على `CarrierStateUnit` ولا يُدخَل عضوًا؛ وإدخالُه "
            "يجعل الوحدةَ الواحدةَ عضوين"
        ),
    ),
    GlossaryConcordanceRow(
        glossary_category="SHADDA_*",
        glossary_says="عائلةُ حالاتٍ تجمع الشدّةَ إلى الحركة أو التنوين",
        this_tree_says=(
            "التضعيفُ مرصودٌ في `GeminationRole.PAIR_START`، والحركةُ والتنوينُ "
            "مرصودان في حقولهما؛ فالعائلةُ ضربٌ في حقولٍ قائمةٍ لا حالاتٌ جدد"
        ),
        tree_reference=(
            "`encoding/carrier_state_candidate.GeminationRole` و"
            "`gflk_state_machine_registration.PROPOSED_STATE_READINGS`"
        ),
        reading=ConcordanceReading.ROLE_OVER_AN_EXISTING_UNIT,
        what_was_settled=(
            "تُقرأ أدوارًا على الوحدة القائمة؛ وضربُ الشدّة في الحركات يُضخّم "
            "مفردةً مغلقةً بما ليس منها"
        ),
    ),
)


ROLE_READINGS_OVER_THE_EXISTING_UNIT: Final[tuple[RoleReading, ...]] = (
    RoleReading(
        proposed_name="TANWEEN_ALIF_CARRIER",
        existing_unit_fields=("tanwin", "tanwin_alif_seat", "seat"),
        grounds=(
            "ألفُ التنوين لا تحمل حركةً تخصّها، وإنّما هي مَقعدُ كتابةٍ لتنوينِ "
            "الفتح المحمول على ما قبلها"
        ),
    ),
    RoleReading(
        proposed_name="SHADDA_*",
        existing_unit_fields=("gemination", "state", "tanwin"),
        grounds=(
            "الشدّةُ تضعيفٌ مرصودٌ في `GeminationRole.PAIR_START`، وما بعدها "
            "حركةٌ أو تنوينٌ مرصودٌ في حقله"
        ),
    ),
)


GLOSSARY_CATEGORIES_NOT_YET_SUPPLIED: Final[tuple[UnsuppliedGlossaryCategory, ...]] = (
    UnsuppliedGlossaryCategory(
        category_name="ما بعد `SHADDA_` من فئات `letters[].state`",
        why_it_is_not_compared=(
            "انقطع نقلُ القاموس عند `SHADDA_`، ولم يُلصَق نصُّ `GLOSSARY.md` "
            "كاملًا بعد ذلك؛ ومقابلةُ فئةٍ لم يصل نصُّها تخمينٌ من اسمها"
        ),
    ),
    UnsuppliedGlossaryCategory(
        category_name="تعريفاتُ `wazn` و`syllables`",
        why_it_is_not_compared="لم يصل نصُّ تعريفها في القاموس",
    ),
    UnsuppliedGlossaryCategory(
        category_name="تعريفاتُ `makhraj` و`manner`",
        why_it_is_not_compared=("لم يصل نصُّ تعريفها، وجدولاها خلف حاجزين مفتوحين أصلًا"),
    ),
    UnsuppliedGlossaryCategory(
        category_name="تعريفاتُ `al_analysis` و`jarad_analysis`",
        why_it_is_not_compared="لم يصل نصُّ تعريفها في القاموس",
    ),
)


AGGREGATION_DOES_NOT_LEVEL_EPISTEMIC_RANK_NOTE: Final[str] = (
    "AggregationDoesNotLevelEpistemicRank: كلُّ طبقةٍ تحمل منزلتَها من مفردةٍ "
    "مغلقة، والجمعُ في قاموسٍ واحدٍ لا يُسوّي بين المقيس والمستورَد والمتعذّر "
    "والفرض؛ ومن سوّاها في الشكل استُشهِد عنده بالمستورَد كأنّه مقيسٌ هنا"
)

AN_UNMEASURED_LAYER_IS_A_SEPARATE_REFUSAL_FIELD_NOT_A_NULL_NOTE: Final[str] = (
    "AnUnmeasuredLayerIsASeparateRefusalFieldNotANull: الطبقةُ التي لم تُقَس "
    "تُخرَج في حقلِ تعذّرٍ مُسمًّى لا في قيمةٍ خالية؛ وإلّا استوى «لم يُقَس» "
    "و«قِيس فكان لا شيء» في السجلّ"
)

A_POSITIONAL_INFERENCE_IS_NOT_A_READING_OF_THE_WRITTEN_MARKS_NOTE: Final[str] = (
    "APositionalInferenceIsNotAReadingOfTheWrittenMarks: تصنيفُ همزة الوصل "
    "بموضعها (أوّلُ حرفٍ + ألفٌ عارية) استدلالٌ سياقيٌّ قد يصدق، ولا يصير بذلك "
    "قراءةً لعلامةٍ مكتوبة؛ فيُفصَل في منزلةٍ مستقلّةٍ ولا يُدمَج داخل حالة"
)

THE_SAME_CONCEPT_UNDER_TWO_NAMES_IS_ONE_ENTRY_NOT_TWO_NOTE: Final[str] = (
    "TheSameConceptUnderTwoNamesIsOneEntryNotTwo: `SUKUN`/`IMPLICIT_SUKUN` هما "
    "`SUKUN_EXPLICIT`/`SUKUN_IMPLICIT` مفهومًا؛ والمفردةُ القائمةُ المغلقةُ هي "
    "المرجع، وتسميةُ جلسةٍ معزولةٍ لا أسبقيّةَ لها"
)

THE_GLOSSARY_TEXT_HAS_NOT_ARRIVED_IN_FULL_NOTE: Final[str] = (
    "TheGlossaryTextHasNotArrivedInFull: لم يصل من القاموس إلّا صدرُه، فلا "
    "تُودَع بايتاتُه ولا تُبصَّم ولا تُقابَل فئةٌ لم يصل نصُّها؛ والفئاتُ "
    "غيرُ الواصلة تُسجَّل باسمها في حقلها لا تُخمَّن"
)


def _assert_no_result_field() -> None:
    """حارسُ استيراد: لا حقلَ نتيجةٍ يتسلّل إلى تسجيلٍ مسبقٍ لاحقًا."""

    for dataclass_type in (
        LayerRegistration,
        GlossaryConcordanceRow,
        RoleReading,
        UnsuppliedGlossaryCategory,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise WordStructureDictionaryPreregistrationError(
                        f"حقلٌ يحمل نتيجةً تسلّل إلى {dataclass_type.__name__}: "
                        f"{declared.name}؛ والتسجيلُ المسبق لا نتيجةَ فيه"
                    )


if len(DictionaryLayer) != 7:
    raise RuntimeError("طبقاتُ القاموس سبعٌ مغلقة.")
if len(LayerEpistemicStanding) != 4:
    raise RuntimeError("منازلُ الطبقات أربعٌ مغلقة.")
if len(DICTIONARY_LAYER_REGISTRATIONS) != len(DictionaryLayer):
    raise RuntimeError("لكلِّ طبقةٍ تسجيلٌ واحد، ولا طبقةَ بلا تسجيل.")
if len({registration.layer for registration in DICTIONARY_LAYER_REGISTRATIONS}) != len(
    DictionaryLayer
):
    raise RuntimeError("لا تُسجَّل طبقةٌ مرّتين ولا تُترَك أخرى.")
if len({row.glossary_category for row in GLOSSARY_CONCORDANCE}) != len(
    GLOSSARY_CONCORDANCE
):
    raise RuntimeError("لا يُقابَل مدخلٌ واحدٌ بصفّين.")
_assert_no_result_field()
