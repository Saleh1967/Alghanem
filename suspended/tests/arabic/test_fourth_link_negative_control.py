"""ضابطٌ سالب: أتتجاوز الأداةُ الحلقةَ الرابعة فعلًا حين تقوم بنيةُ الاستشهاد؟

**هذا ضابطُ أداةٍ لا بطاقةُ بحث**: بطاقتُه مصنوعةٌ لهذا الغرض وحده
(`test_only`)، لفظُها ومدلولُها مخترعان بالتصريح، ولا تُقرأ منها شهادةٌ على لفظٍ
قرآنيٍّ ولا على معجمٍ بعينه. ولذلك تبقى في ملفّ الاختبار ولا تُكتَب في
`examples/external_audit/`: تلك البطاقاتُ يجري عليها التدقيقُ الخارجيُّ بالكامل،
فوضعُ بطاقةٍ اصطناعيةٍ بينها يمنحها شهادةً إنتاجيةً هي عينُ ما يمنعه غرضُها.

**والسؤالُ المحسوم قبلَه**: الحلقةُ الرابعة لا تشترط `متواتر` باسمه، بل تشترط
**اشتقاقَ** عضوٍ من `TransmissionStanding`؛ و`متواتر` عضوٌ بلا مدخلٍ في كلّ
طريقٍ هنا، فاشتراطُه باسمه يجعل الحلقةَ ممتنعةً أبدًا لا واقفةً بعارض.

**ومعيارُ النجاح واحد**: أن تتجاوز الأداةُ الحلقةَ الرابعة على هذه البطاقة
بعينها. فإن لم تتجاوزها فوقوفُ البطاقات الثلاث في `test_lexical_transmission`
يُقرأ بأثرٍ رجعيّ «توقّفٌ حتميٌّ بعطل أداة» لا «توقّفٌ مُشتَقٌّ صحيح».

**والحلقةُ الرابعة وحدها هي المفحوصة هنا**، فتُستدعى `link_four` مباشرةً ولا
تُساق البطاقةُ على `traverse`: سَوقُها كاملةً يحتاج قرائنَ مناطٍ ومنافساتٍ
مصوغةً لحلقاتٍ أُخَر، وهي زيادةٌ تُقحِم على الضابط ما ليس من غرضه.
"""

from typing import Any, Final

from card_traversal import lexical_citation_genus, link_four

from alghanem.arabic.lexical_transmission import (
    LexicalCitationStructure,
    card_lexical_citation_structure,
    card_lexical_wad_path,
    card_transmission_standing,
)
from alghanem.arabic.transmission_standing import (
    TawaturQuestionStanding,
    TransmissionStanding,
    UnconstructibilityGenus,
)
from alghanem.arabic.wad_naql import WadRecord

_TEST_ONLY_MARKER: Final = "test_only"


def _synthetic_card() -> dict[str, Any]:
    """بطاقةٌ اصطناعيةٌ صريحةُ الغرض، بإسنادين داخليين مُسمَّيين مرتَّبين."""

    return {
        "معرف_السؤال": f"q-{_TEST_ONLY_MARKER}-fourth-link-control",
        "الكلمة_المدروسة": "لفظٌ مخترعٌ لهذا الضابط لا شاهدَ له في نصّ",
        "الغرض": (
            f"{_TEST_ONLY_MARKER}: ضبطُ الأداة وحدها، فلا شهادةَ إنتاجيةً في هذه "
            "البطاقة ولا حكمَ منها على لفظٍ قائم"
        ),
        "طريق_النقل_المعجمي": {
            "المصدر": "مُجمِّعٌ مخترعٌ لهذا الضابط",
            "المادة": "مادّةٌ مخترعةٌ لهذا الضابط",
            "الإسنادات": [
                {
                    "السلطة": "سلطةٌ أولى مخترعة",
                    "الاقتباس_المنقول": "قالت سلطةٌ أولى مخترعة: كذا في هذه المادّة",
                    "الموضع": "موضعٌ مخترعٌ أوّل",
                    "جنس_المحتوى": "نقل_قول_منسوب",
                },
                {
                    "السلطة": "سلطةٌ ثانية مخترعة",
                    "الاقتباس_المنقول": "وقالت سلطةٌ ثانية مخترعة: كذا في هذه المادّة",
                    "الموضع": "موضعٌ مخترعٌ ثانٍ",
                    "جنس_المحتوى": "نقل_قول_منسوب",
                },
            ],
        },
    }


def _flattened_card() -> dict[str, Any]:
    """البطاقةُ نفسها بإسنادٍ واحد: موضعٌ مُسمًّى لا تعاقبَ فيه."""

    card = _synthetic_card()
    card["طريق_النقل_المعجمي"]["الإسنادات"] = card["طريق_النقل_المعجمي"]["الإسنادات"][
        :1
    ]
    return card


def test_the_card_declares_itself_a_control_and_carries_no_production_witness() -> None:
    """غرضُ البطاقة مكتوبٌ فيها، فلا تُقرأ شهادةً على لفظٍ قائم."""

    card = _synthetic_card()

    assert _TEST_ONLY_MARKER in card["معرف_السؤال"]
    assert _TEST_ONLY_MARKER in card["الغرض"]
    assert "الأدلة" not in card
    assert "تعريف_التجربة" not in card


def test_the_tool_actually_passes_the_fourth_link_on_this_card() -> None:
    """معيارُ النجاح الوحيد: الحلقةُ الرابعة تقوم فعلًا، ولا تقف كعادتها."""

    card = _synthetic_card()
    attempt = link_four(card)

    assert attempt.label == "٤"
    assert attempt.module_relative_path == "wad_naql.py"
    assert attempt.stood_up is True
    assert attempt.missing_declaration == ""


def test_the_standing_is_a_real_declared_member_derived_from_the_path() -> None:
    """الدرجةُ عضوٌ مُعلَنٌ حقيقيّ، مُشتَقٌّ من الطريق لا مقروءٌ من نصّ البطاقة."""

    card = _synthetic_card()
    standing = card_transmission_standing(card)

    assert standing is TransmissionStanding.AHAD
    assert standing is not TransmissionStanding.MUTAWATIR
    assert not any(
        member.value in str(card) for member in TransmissionStanding
    ), "الدرجةُ لم تُكتَب في البطاقة نصًّا، فقيامُ الحلقة اشتقاقٌ لا قراءة"


def test_the_citation_structure_and_its_genus_are_the_chained_ones() -> None:
    """بنيتُها متعاقبةٌ مُسمّاة، وجنسُ امتناعها حجزٌ لغياب سلطةٍ لا خطأٌ فئويّ."""

    card = _synthetic_card()

    assert (
        card_lexical_citation_structure(card)
        is LexicalCitationStructure.إسناد_داخلي_متعاقب_مسمى
    )
    assert lexical_citation_genus(card) is (
        UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY
    )


def test_the_derived_standing_records_a_wad_without_touching_wad_naql() -> None:
    """الدرجةُ المُشتَقّة تُبنى منها `WadRecord` كما هي، بلا تعديلٍ في الوحدة."""

    standing = card_transmission_standing(_synthetic_card())
    assert standing is not None

    record = WadRecord(
        lafz="لفظٌ مخترعٌ لهذا الضابط",
        madlul="مدلولٌ مخترعٌ لهذا الضابط",
        naql_source="مُجمِّعٌ مخترعٌ لهذا الضابط، مادّةٌ مخترعةٌ لهذا الضابط",
        transmission=standing,
    )

    assert record.transmission is TransmissionStanding.AHAD
    assert record.known_only_by_naql is True


def test_removing_one_attribution_stops_the_same_link_again() -> None:
    """القيامُ والوقوفُ كلاهما مُشتَقٌّ من البنية، فلا أحدَهما ثابتٌ في الأداة."""

    card = _flattened_card()
    attempt = link_four(card)

    assert attempt.stood_up is False
    assert "عنوان_واحد_مسطح" in attempt.missing_declaration
    assert "ممتنعة_بخطأ_فئوي_بنيوي" in attempt.missing_declaration
    assert card_transmission_standing(card) is None


def test_a_well_posed_tawatur_question_is_still_not_a_tawatur_claim() -> None:
    """سؤالُ التواتر هنا مستقيمُ الوضع وغيرُ محقَّق، و`متواتر` بلا مدخلٍ بعد."""

    wad_path = card_lexical_wad_path(_synthetic_card())
    assert wad_path is not None
    assert wad_path.question_standing is (
        TawaturQuestionStanding.WELL_POSED_AND_UNVERIFIED_HERE
    )
    assert wad_path.standing is not TransmissionStanding.MUTAWATIR
