"""بطاقةُ الجملة: حراسُ التسجيل المسبق، وسَوقٌ واحدٌ على «اللهُ نورُ السماواتِ والأرضِ».

دالّةُ السَّوق هنا **معينُ اختبارٍ لا وحدةُ إنتاج**، على منوال
`tests/arabic/card_traversal.py`: لا تُنشئ سلطةً ولا مفردةً ولا دفترًا، ولا
تقرؤها وحدةٌ في الشجرة. وموضعُها هذا مقصود: البطاقةُ لم تُثبِت قيمتَها على جملةٍ
كاملةٍ بعد، وبناءُ وحدةِ إنتاجٍ حولها اليوم بناءُ بنيةٍ إجرائيةٍ حول محتًوى شحيح.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from alghanem.arabic.compound_layer_preregistration import NamedRefusal
from alghanem.arabic.kulli_juzi_formal import (
    KulliJuziClass,
    canonical_sub_outcome,
    canonical_sub_partition,
    canonical_universality,
    classify_kulli_juzi,
)
from alghanem.arabic.lafz_madlul_relation_formal import (
    LafzMadlulRelation,
    canonical_intended_meaning,
    canonical_relation_answer,
    canonical_relation_count,
    classify_relation,
)
from alghanem.arabic.madlul_alone_formal import (
    MadlulSection,
    canonical_signified_composition,
    canonical_signified_kind,
    canonical_signified_usage_state,
    classify_madlul,
)
from alghanem.arabic.mantuq_mafhum_ifada import (
    DalalaChannel,
    DalalaRecord,
    IfadaStanding,
    MafhumKind,
)
from alghanem.arabic.sentence_card_preregistration import (
    NAMED_REFUSALS,
    NAMED_RESIDUALS,
    SENTENCE_CARD_PREREGISTRATION,
    CardItem,
    CardItemRegistration,
    FrozenReference,
    ItemStanding,
    SentenceCardPreregistrationError,
    SupportCoding,
    derived_prerequisites,
    read_item_support,
)
from alghanem.arabic.word_class_formal import WordClass, canonical_answer, classify

CARD_DIRECTORY = Path(__file__).resolve().parents[2] / "examples" / "sentence_card"
CARD_PATH = CARD_DIRECTORY / "nur_24_35.yaml"


def _read_card() -> dict[str, Any]:
    payload = json.loads(CARD_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


@dataclass(frozen=True)
class ItemReading:
    """قراءةُ بندٍ واحد: إمّا مُشتَقّةٌ بنصّها، وإمّا وقوفٌ بجنسٍ مُسمًّى."""

    item: CardItem
    derived: str
    stop_genus: str

    @property
    def is_read(self) -> bool:
        return not self.stop_genus


def _stop_genus(registration: CardItemRegistration) -> str:
    """جنسُ الوقوف مُشتَقٌّ من موقف البند المُسجَّل، لا مكتوبٌ في البطاقة."""

    if registration.standing is ItemStanding.DEFERRED_BY_NAMED_LAW:
        return f"مؤجَّل_بقانونٍ_مُسمّى: {registration.deferring_law}"
    if registration.standing is ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE:
        return f"نصٌّ_مُزوَّدٌ_بلا_شهادة_صورية: {registration.supplied_text_key}"
    return "مصدر_غير_مُقدَّم"


def traverse_card(card: dict[str, Any]) -> tuple[ItemReading, ...]:
    """سُق البطاقة على البنود التسعةَ عشرَ بترتيب تسجيلها، واشتقّ ما يُشتَقّ.

    والبلوغُ مُشتَقٌّ بالتتابع: بندٌ قامت قراءتُه وقد وقف بندٌ في مخروط شرطه
    يُقرأ `مسبوق_ببندٍ_غير_بالغ` لا مقروءًا، وإلّا ظهرت البطاقةُ تامّةً وهي
    منقطعةٌ عند موضعٍ سابق.
    """

    words = card["الكلمات"]
    relation = card["علاقة_اللفظ_بالمدلول"]
    madlul = card["المدلول_وحده"]
    mantuq = card["منطوق_ومفهوم"]
    ifada = card["الإفادة"]

    readings: dict[CardItem, ItemReading] = {}
    for registration in SENTENCE_CARD_PREREGISTRATION.registrations:
        item = registration.item
        stopped_prerequisites = tuple(
            prerequisite.value
            for prerequisite in derived_prerequisites(item)
            if not readings[prerequisite].is_read
        )
        if stopped_prerequisites:
            readings[item] = ItemReading(
                item=item,
                derived="",
                stop_genus="مسبوق_ببندٍ_غير_بالغ: " + "، ".join(stopped_prerequisites),
            )
            continue
        if registration.standing is not ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE:
            readings[item] = ItemReading(
                item=item, derived="", stop_genus=_stop_genus(registration)
            )
            continue

        if item is CardItem.WORD_CLASS:
            derived = "، ".join(
                "{}={}".format(
                    word["اللفظ"],
                    classify(
                        canonical_answer(word["استقلال_بالمعنى"]),
                        canonical_answer(word["دلالة_زمنية_بالهيئة"]),
                    ).value,
                )
                for word in words
            )
        elif item is CardItem.KULLI_JUZI:
            derived = "، ".join(
                "{}={}".format(
                    word["اللفظ"],
                    classify_kulli_juzi(
                        canonical_universality(word["وقوع_الشركة"]),
                        canonical_sub_partition(word["محور_التفريع"]),
                        canonical_sub_outcome(word["مخرج_التفريع"]),
                    ).value,
                )
                for word in words
            )
        elif item in (CardItem.LAFZ_MADLUL_RELATION, CardItem.HAQIQA_MAJAZ):
            derived = classify_relation(
                canonical_relation_count(relation["تعدد_اللفظ"]),
                canonical_relation_count(relation["تعدد_المعنى"]),
                canonical_relation_answer(relation["وُضع_لكل_معنى_ابتداءً"]),
                canonical_relation_answer(relation["اشتهر_حتى_هُجر_الأول"]),
                canonical_intended_meaning(relation["المعنى_المراد"]),
            ).value
        elif item is CardItem.MADLUL_ALONE:
            derived = classify_madlul(
                canonical_signified_kind(madlul["جنس_المدلول"]),
                canonical_signified_composition(madlul["تركيب_المدلول"]),
                canonical_signified_usage_state(madlul["حال_استعمال_المدلول"]),
            ).value
        else:
            record = DalalaRecord(
                lafz=mantuq["اللفظ_المختبَر"],
                madlul=mantuq["المدلول_المقروء"],
                carried_by_the_wording=mantuq["حُمِل_على_اللفظ_نفسه"],
                agrees_with_the_uttered_ruling=mantuq["حامل_قسم_المفهوم"],
                composition_benefits=ifada["حامل_الإفادة"],
                benefit_witness=ifada["شاهد_الإفادة"],
                declared_channel=DalalaChannel.منطوق,
                declared_mafhum_kind=MafhumKind.لا_ينطبق,
                declared_ifada=IfadaStanding.غير_مقروء,
            )
            if item is CardItem.MANTUQ_MAFHUM:
                derived = f"{record.channel.value}/{record.mafhum_kind.value}"
            else:
                derived = record.ifada.value
        readings[item] = ItemReading(item=item, derived=derived, stop_genus="")
    return tuple(
        readings[registration.item]
        for registration in SENTENCE_CARD_PREREGISTRATION.registrations
    )


def test_every_item_is_registered_exactly_once() -> None:
    items = SENTENCE_CARD_PREREGISTRATION.items
    assert len(items) == 19
    assert set(items) == set(CardItem)
    assert len(set(items)) == len(items)


def test_certificate_is_not_constructible() -> None:
    assert SENTENCE_CARD_PREREGISTRATION.certificate_is_constructible is False


def test_standings_are_seven_derived_two_deferred_four_supplied_six_awaiting() -> None:
    derived = SENTENCE_CARD_PREREGISTRATION.items_with_standing(
        ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE
    )
    deferred = SENTENCE_CARD_PREREGISTRATION.items_with_standing(
        ItemStanding.DEFERRED_BY_NAMED_LAW
    )
    awaiting = SENTENCE_CARD_PREREGISTRATION.items_with_standing(
        ItemStanding.AWAITING_SOURCE_TEXT
    )
    supplied = SENTENCE_CARD_PREREGISTRATION.items_with_standing(
        ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE
    )
    assert (len(derived), len(deferred), len(supplied), len(awaiting)) == (7, 2, 4, 6)
    assert set(deferred) == {CardItem.AMIL_MAMUL, CardItem.NISAB_TADMIN_TAQYID}
    assert set(supplied) == {
        CardItem.MUTABAQA_TADAMMUN_ILTIZAM,
        CardItem.KHABAR_INSHA,
        CardItem.WAZN,
        CardItem.ISHTIQAQ_SARF,
    }


def test_each_item_carries_exactly_one_frozen_reference() -> None:
    for registration in SENTENCE_CARD_PREREGISTRATION.registrations:
        assert isinstance(registration.reference, FrozenReference)


def test_prerequisite_is_registered_before_its_dependent() -> None:
    seen: list[CardItem] = []
    for registration in SENTENCE_CARD_PREREGISTRATION.registrations:
        for prerequisite in registration.prerequisites:
            assert prerequisite in seen
        seen.append(registration.item)


def test_written_prerequisites_that_differ_from_the_derived_cone_are_refused() -> None:
    with pytest.raises(SentenceCardPreregistrationError):
        CardItemRegistration(
            item=CardItem.IFADA,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            supporting_module="",
            deferring_law="",
            supplied_text_key="",
            prerequisites=(),
            refusals=(NamedRefusal(name="n", statement="s"),),
            note="شرطٌ مكتوبٌ على خلاف المُشتَقّ",
        )


def test_derived_item_without_a_module_is_refused() -> None:
    with pytest.raises(SentenceCardPreregistrationError):
        CardItemRegistration(
            item=CardItem.WORD_CLASS,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE,
            supporting_module="",
            deferring_law="",
            supplied_text_key="",
            prerequisites=(),
            refusals=(NamedRefusal(name="n", statement="s"),),
            note="اشتقاقٌ بلا وحدة",
        )


def test_deferred_item_without_a_named_law_is_refused() -> None:
    with pytest.raises(SentenceCardPreregistrationError):
        CardItemRegistration(
            item=CardItem.AMIL_MAMUL,
            reference=FrozenReference.AL_NAHW_AL_WADIH,
            standing=ItemStanding.DEFERRED_BY_NAMED_LAW,
            supporting_module="",
            deferring_law="",
            supplied_text_key="",
            prerequisites=(),
            refusals=(NamedRefusal(name="n", statement="s"),),
            note="تأجيلٌ بلا اسمِ قانون",
        )


def test_awaiting_item_may_not_claim_a_module() -> None:
    with pytest.raises(SentenceCardPreregistrationError):
        CardItemRegistration(
            item=CardItem.WAZN,
            reference=FrozenReference.LISAN_AL_ARAB,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            supporting_module="word_class_formal.py",
            deferring_law="",
            supplied_text_key="",
            prerequisites=(),
            refusals=(NamedRefusal(name="n", statement="s"),),
            note="انتظارُ نصٍّ مع ادّعاء وحدة",
        )


def test_item_without_a_named_refusal_is_refused() -> None:
    with pytest.raises(SentenceCardPreregistrationError):
        CardItemRegistration(
            item=CardItem.MAQAM,
            reference=FrozenReference.SHAKHSIYYA_THREE,
            standing=ItemStanding.AWAITING_SOURCE_TEXT,
            supporting_module="",
            deferring_law="",
            supplied_text_key="",
            prerequisites=(),
            refusals=(),
            note="بندٌ بلا حدٍّ مُسمًّى",
        )


def test_declared_modules_are_read_from_the_tree() -> None:
    readings = read_item_support()
    assert len(readings) == 19
    for reading in readings:
        if reading.registration.supporting_module:
            assert reading.coding is SupportCoding.CODED
        else:
            assert reading.coding is SupportCoding.NO_MODULE_DECLARED


def test_absent_module_is_read_not_coded(tmp_path: Path) -> None:
    package = tmp_path / "src" / "alghanem" / "arabic"
    package.mkdir(parents=True)
    codings = {reading.coding for reading in read_item_support(tmp_path)}
    assert SupportCoding.NOT_CODED in codings


def test_named_refusals_and_residuals_are_stated_not_only_named() -> None:
    assert {refusal.name for refusal in NAMED_REFUSALS} >= {
        "SentenceIsNotALexeme",
        "CardIsNotACertificate",
        "OneCardOnThreeSentencesIsNotFractality",
        "ParallelFrontIsNotABlockedFront",
    }
    assert "SECOND_AND_THIRD_SENTENCES_ARE_REGISTERED_NOT_OPENED" in NAMED_RESIDUALS
    assert "SHIBH_JUMLA_IFADA_PREDICTION_IS_FROZEN_BEFORE_ITS_RUN" in NAMED_RESIDUALS
    for key in (
        "TERM_NOT_LOCATED_IN_DECLARED_SOURCE",
        "MODERN_COPYRIGHTED_SOURCE_NOT_DIGITIZED_OPENLY",
        "EXTRACTED_LINE_NUMBERS_ARE_NOT_PRINT_PAGINATION",
        "DIGITALLY_ENCODED_PRINT_PAGINATION_UNCOLLATED",
        "LISAN_MATN_IS_QUOTED_NOT_VENDORED_WHOLESALE",
        "LISAN_NUR_MATERIAL_CARRIES_NO_JAMID_MUSHTAQ_OR_DAL_ALONE_STATEMENT",
    ):
        assert key in NAMED_RESIDUALS
    for statement in NAMED_RESIDUALS.values():
        assert statement.strip()


def test_card_declares_carriers_and_writes_no_derived_class() -> None:
    card = _read_card()
    text = json.dumps(card, ensure_ascii=False)
    for written_result in (
        WordClass.ISM.value,
        KulliJuziClass.KULLI_MUSHAKKIK.value,
        LafzMadlulRelation.MAJAZ.value,
        MadlulSection.MEANING.value,
    ):
        assert f'"{written_result}"' not in text.replace('"معنى"', "")


def test_five_items_are_read_and_the_rest_stop_by_a_named_genus() -> None:
    """خمسةٌ من تسعةَ عشرَ تُقرأ، وعدمُ اكتمال البطاقة هو النتيجة لا العطل."""

    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    assert len(readings) == 19
    read_items = {item for item, reading in readings.items() if reading.is_read}
    assert read_items == {
        CardItem.WORD_CLASS,
        CardItem.KULLI_JUZI,
        CardItem.LAFZ_MADLUL_RELATION,
        CardItem.HAQIQA_MAJAZ,
        CardItem.MADLUL_ALONE,
    }
    for item, reading in readings.items():
        if item not in read_items:
            assert reading.stop_genus


def test_mantuq_mafhum_stops_although_its_own_module_is_coded() -> None:
    """بندٌ وحدتُه مُرمَّزةٌ ومع ذلك يقف: شرطُه المُشتَقُّ ينتظر نصًّا.

    وهذه نتيجةٌ لم تُتوقَّع في نصّ الطلب: ترميزُ وحدة البند لا يكفي لبلوغه ما
    دام مخروطُ شرطه مفتوحًا، وهو القانونُ التسلسليُّ نفسه نازلًا إلى بنود
    البطاقة.
    """

    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    registration = SENTENCE_CARD_PREREGISTRATION.registration_for(
        CardItem.MANTUQ_MAFHUM
    )
    assert registration.standing is ItemStanding.DERIVED_FROM_EXISTING_CERTIFICATE
    assert registration.supporting_module
    reading = readings[CardItem.MANTUQ_MAFHUM]
    assert not reading.is_read
    assert CardItem.MUTABAQA_TADAMMUN_ILTIZAM.value in reading.stop_genus


def test_the_four_words_are_all_nouns() -> None:
    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    derived = readings[CardItem.WORD_CLASS].derived
    assert derived.count(WordClass.ISM.value) == 4
    assert WordClass.FIL.value not in derived
    assert WordClass.HARF.value not in derived


def test_nur_is_derived_mushakkik_not_mutawati() -> None:
    """نتيجةٌ تُخالف جدولَ الطلب، ولا يُعدَّل النصُّ المُثبَت لتوافقه."""

    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    derived = readings[CardItem.KULLI_JUZI].derived
    assert KulliJuziClass.KULLI_MUSHAKKIK.value in derived
    assert KulliJuziClass.KULLI_MUTAWATI.value not in derived
    assert KulliJuziClass.JUZI_ALAM.value in derived
    assert "TASHKIK_DIVERGENCE_IS_A_READING_NOT_A_CORRECTION" in NAMED_RESIDUALS


def test_nur_relation_is_majaz_and_its_madlul_is_a_meaning() -> None:
    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    assert readings[CardItem.HAQIQA_MAJAZ].derived == LafzMadlulRelation.MAJAZ.value
    assert readings[CardItem.MADLUL_ALONE].derived == MadlulSection.MEANING.value


def test_ifada_stops_because_its_prerequisite_is_deferred_not_because_it_failed() -> (
    None
):
    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    ifada = readings[CardItem.IFADA]
    assert not ifada.is_read
    assert CardItem.NISAB_TADMIN_TAQYID.value in ifada.stop_genus
    assert IfadaStanding.غير_مُفيد.value not in ifada.stop_genus


def test_compound_layer_items_stop_by_their_named_law() -> None:
    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    assert "Preregistration != Certificate" in readings[CardItem.AMIL_MAMUL].stop_genus
    assert (
        CardItem.AMIL_MAMUL.value in readings[CardItem.NISAB_TADMIN_TAQYID].stop_genus
    )


def test_items_awaiting_a_source_text_stop_as_source_not_supplied() -> None:
    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    for item in (
        CardItem.IRAB_MARK,
        CardItem.MURAB_MABNI,
        CardItem.JAMID_MUSHTAQ,
        CardItem.DAL_ALONE,
        CardItem.MAQAM,
    ):
        assert readings[item].stop_genus == "مصدر_غير_مُقدَّم"


def test_supplied_text_items_stop_by_their_own_genus_not_as_missing_source() -> None:
    """تزويدُ النصّ نقل البندَ من جنسِ وقوفٍ إلى جنسٍ آخر، ولم يُبلِغه قراءةً."""

    readings = {reading.item: reading for reading in traverse_card(_read_card())}
    for item, key in (
        (CardItem.WAZN, "WAZN_LISAN_NUR"),
        (CardItem.KHABAR_INSHA, "KHABAR_INSHA_SHAKHSIYYA_THREE"),
        (
            CardItem.MUTABAQA_TADAMMUN_ILTIZAM,
            "MUTABAQA_TADAMMUN_ILTIZAM_SHAKHSIYYA_THREE",
        ),
    ):
        assert readings[item].stop_genus == f"نصٌّ_مُزوَّدٌ_بلا_شهادة_صورية: {key}"
        assert not readings[item].is_read
    assert (
        readings[CardItem.ISHTIQAQ_SARF].stop_genus
        == f"مسبوق_ببندٍ_غير_بالغ: {CardItem.WAZN.value}"
    )
