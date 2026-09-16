"""شاهدٌ خارجيٌّ للّزوم والتعدّي، مُبصَّمٌ ومُحصًى، غيرُ مأخوذٍ من وَسْم المجهول.

القياسُ السابقُ في `transitivity_corpus_census` قسَم الجذورَ بوجود المجهول
المجرَّد وغيابه، ثمّ اختبر القسمةَ باسم المفعول — وهو صيغةُ مجهولٍ أيضًا. وقد
سُجِّل التحفّظُ هناك باسمه `TheIndicatorAndItsTestShareAParent`: مؤشّرٌ واختبارُه
من أصلٍ واحد، فالتوافقُ بينهما تقاربٌ لا شهادةٌ مستقلّة. وهذه الوحدة **تُودِع
الشاهدَ المستقلَّ نفسَه**، لا نتيجتَه.

والشاهدُ جدولُ أفعالٍ ثلاثيةٍ جُمِع بأيدي غيرنا قبل أن يُطرَح سؤالُنا هذا ولا
يعلم به: `triverbtable.py` — لكلِّ مدخلٍ فيه فعلٌ مشكولٌ وجذرُه وبابُه وحركةُ
عينِه ووَسْمُ لزومه أو تعدّيه. ووَسْمُ اللزوم/التعدّي فيه **حكمٌ معجميٌّ بشريّ
منطوقٌ به**، لا اشتقاقٌ من صيغةٍ صرفية؛ فهو مستقلٌّ عن وَسْم المجهول في مدوَّنة
القرآن استقلالًا تامًّا.

`THE_MARKS_MEANING_IS_UPSTREAMS_NOT_OURS`: دلالةُ الحروف الثلاثة ليست تخمينًا
منّا: يُصرِّح `libqutrub/verb_db.py` بأنّ الميم والكاف يُقرآن تعدّيًا واللامَ
لزومًا (`if transitive in (araby.KAF, araby.MEEM)`)، والكافُ عنده «مشترك» بين
اللزوم والتعدّي. فما يُقرأ هنا من الحروف مأخوذٌ من شفرة أهل الجدول لا من ظنّنا
بالعربية.

`TWO_MIRRORS_ONE_DIGEST_IS_NOT_TWO_WITNESSES`: الملفُّ عينُه موجودٌ في مستودعين
(`arramooz` و`qutrub`)، وقد فُتِحا كلاهما فخرجت منهما بصمةٌ واحدة. وهذا يُثبِت
أنّ المرآتين لم تختلفا، **ولا يُثبِت أنّ الشاهدَين اثنان**: هو شاهدٌ واحدٌ رُئي
من موضعين.

`THE_JOIN_WAS_NOT_TAKEN`: لم يُوصَل هذا الجدولُ بعدُ بقسمة `transitivity_corpus_census`.
وجذورُ مدوَّنة القرآن مكتوبةٌ بترميز Buckwalter بثمانيةٍ وعشرين محرفًا من ASCII،
وجذورُ هذا الجدول بالعربية بتسعةٍ وعشرين محرفًا (فيها الهمزةُ مفردةً «ء» ومحمولةً
«أ» معًا). فالتقاطعُ الحرفيُّ بين الجذور الثمانيةِ والتسعين وثلاثمئةٍ المقسومةِ
وجذورِ هذا الجدول **صفر**، وهو رقمٌ مقيسٌ لا مُقدَّر. ووصلُهما يستلزم جدولَ
تحويلٍ وقرارَ توحيدِ همزة، وكلاهما **قاعدةٌ تُسَنّ** لا قراءةٌ تُقرأ؛ فتُجمَّد
قبل القياس في مواصفةٍ مستقلّة أو لا تُسَنّ. فهذه الوحدة تقف عند الإيداع
والإحصاء، ولا تُخرِج رقمًا عن اتّفاق الشاهدين.

`A_LEXICON_IS_NOT_A_CORPUS`: هذا الجدولُ معجمُ أفعالٍ لا مدوَّنةَ نصّ: مداخلُه
أفعالٌ مُجرَّدةٌ من السياق، ولا تواترَ فيه ولا موضعَ ورودٍ في نصّ. فمن قاس عليه
شيوعًا قاس ما ليس فيه؛ والمقيسُ منه حكمُ لزومٍ وتعدٍّ لا غير.

`THE_TABLE_IS_TRILATERAL_ONLY`: كلُّ جذرٍ فيه ثلاثيّ، فلا شهادةَ فيه على رباعيٍّ
ولا على وزنٍ مزيد. وسؤالُ «هل يصير اللازمُ متعدّيًا بالتزيّد» لا يُجاب من هذا
الجدول وحدَه.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. وبايتاتُ الجدول غيرُ
منسوخةٍ إلى الشجرة؛ والمُودَعُ بصمةٌ وطولٌ ومسارٌ ورخصة.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .irab_corpus_witness import (
    ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE,
    WITNESS_BYTES_ARE_NOT_VENDORED_NOTE,
    IrabCorpusWitness,
)

__all__ = [
    "ARRAMOOZ_BRUT_VERB_DATA_WITNESS",
    "A_LEXICON_IS_NOT_A_CORPUS_NOTE",
    "QAC_ROOT_ALPHABET",
    "QUTRUB_TRILATERAL_VERB_TABLE_WITNESS",
    "QUTRUB_TRILATERAL_VERB_TABLE_WITNESS_SECOND_MIRROR",
    "REDERIVED_BAB_COUNTS",
    "REDERIVED_DISTINCT_ROOTS",
    "REDERIVED_DISTINCT_VERBS",
    "REDERIVED_ENTRIES",
    "REDERIVED_HARAKA_COUNTS",
    "REDERIVED_MARK_COUNTS",
    "REDERIVED_ROOT_LEVEL_COUNTS",
    "REDERIVED_ROOTS_JOINING_THE_PARTITION_UNCHANGED",
    "THE_JOIN_WAS_NOT_TAKEN_NOTE",
    "THE_MARKS_MEANING_IS_UPSTREAMS_NOT_OURS_NOTE",
    "THE_TABLE_IS_TRILATERAL_ONLY_NOTE",
    "TRANSITIVITY_LEXICON_NAMED_RESIDUALS",
    "TWO_MIRRORS_ONE_DIGEST_IS_NOT_TWO_WITNESSES_NOTE",
    "WITNESS_ROOT_ALPHABET",
    "TransitivityLexiconError",
    "TransitivityMark",
    "TrilateralVerbEntry",
    "read_trilateral_entries",
    "roots_by_mark",
]


class TransitivityLexiconError(ValueError):
    """تُرفَع حين يُقرأ جدولُ الأفعال قراءةً لا يُعاد بها اشتقاقُ عدده."""


THE_MARKS_MEANING_IS_UPSTREAMS_NOT_OURS_NOTE: Final[str] = (
    "TheMarksMeaningIsUpstreamsNotOurs: دلالةُ «م» و«ك» و«ل» مأخوذةٌ من شفرة "
    "أهل الجدول (`libqutrub/verb_db.py`): الميمُ تعدٍّ، والكافُ مشتركٌ بين "
    "اللزوم والتعدّي، واللامُ لزوم؛ ولم نستنبطها من الحروف بأنفسنا"
)

TWO_MIRRORS_ONE_DIGEST_IS_NOT_TWO_WITNESSES_NOTE: Final[str] = (
    "TwoMirrorsOneDigestIsNotTwoWitnesses: فُتِحت المرآتان فخرجت منهما بصمةٌ "
    "واحدة؛ فثبت أنّهما لم تختلفا، ولم يثبت أنّ الشاهدَين اثنان"
)

THE_JOIN_WAS_NOT_TAKEN_NOTE: Final[str] = (
    "TheJoinWasNotTaken: جذورُ المدوَّنة بترميز Buckwalter وجذورُ الجدول "
    "بالعربية، فالتقاطعُ الحرفيُّ صفرٌ مقيس؛ ووصلُهما قاعدةُ تحويلٍ تُسَنّ "
    "وتُجمَّد قبل القياس، لا قراءةٌ تُقرأ، فوُقِف عند الإيداع"
)

A_LEXICON_IS_NOT_A_CORPUS_NOTE: Final[str] = (
    "ALexiconIsNotACorpus: مداخلُ الجدول أفعالٌ مجرَّدةٌ من السياق بلا تواترٍ "
    "ولا موضعِ ورود؛ فالمقيسُ منه حكمُ لزومٍ وتعدٍّ لا شيوع"
)

THE_TABLE_IS_TRILATERAL_ONLY_NOTE: Final[str] = (
    "TheTableIsTrilateralOnly: كلُّ جذرٍ فيه ثلاثيّ، فلا شهادةَ فيه على رباعيٍّ "
    "ولا على وزنٍ مزيد"
)

TRANSITIVITY_LEXICON_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TheMarksMeaningIsUpstreamsNotOurs": THE_MARKS_MEANING_IS_UPSTREAMS_NOT_OURS_NOTE,
    "TwoMirrorsOneDigestIsNotTwoWitnesses": (
        TWO_MIRRORS_ONE_DIGEST_IS_NOT_TWO_WITNESSES_NOTE
    ),
    "TheJoinWasNotTaken": THE_JOIN_WAS_NOT_TAKEN_NOTE,
    "ALexiconIsNotACorpus": A_LEXICON_IS_NOT_A_CORPUS_NOTE,
    "TheTableIsTrilateralOnly": THE_TABLE_IS_TRILATERAL_ONLY_NOTE,
}


_TABLE_ANNOTATION_NOTE: Final[str] = (
    "ملفُّ بايثون فيه قاموسٌ واحدٌ `TriVerbTable`، كلُّ سطرٍ منه مدخلُ فعلٍ "
    "ثلاثيٍّ بخمسة حقول: `verb` مشكولًا، و`root` بالعربية، و`bab` من واحدٍ إلى "
    "ستّة، و`transitive` بحرفٍ واحدٍ من «م ك ل»، و`haraka` حركةَ عينِ المضارع. "
    "ووَسْمُ اللزوم/التعدّي حكمٌ معجميٌّ منصوصٌ عليه، لا اشتقاقٌ من صيغة. "
    + THE_MARKS_MEANING_IS_UPSTREAMS_NOT_OURS_NOTE
)

_GPL_ATTRIBUTION_NOTE: Final[str] = (
    "الجدولُ مرخَّصٌ بـ`GPL` المنصوصةِ في المستودع، وهي تشترط التصريحَ بالمصدر "
    "والإبقاءَ على الرخصة نفسِها في أيِّ عملٍ مشتقّ؛ ولم تُنسَخ بايتةٌ واحدةٌ "
    "إلى هذه الشجرة، فالمُودَعُ بصمةٌ وطولٌ ورخصة. "
    + ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE
    + " — "
    + WITNESS_BYTES_ARE_NOT_VENDORED_NOTE
)


QUTRUB_TRILATERAL_VERB_TABLE_WITNESS: Final[IrabCorpusWitness] = IrabCorpusWitness(
    corpus="Qutrub trilateral verb table, as carried in Arramooz Alwaseet",
    version="master branch as measured",
    upstream="https://github.com/linuxscout/arramooz",
    measured_mirror="raw.githubusercontent.com/linuxscout/arramooz",
    measured_path="data/verbs/triverbtable.py",
    sha256="75fc716f39b0ee151a1f292a7576a41856f423bf3d837bfb7e92a9a557aa7d8a",
    byte_length=846_066,
    licenses=("GNU General Public License, version 2",),
    required_attribution_links=(
        "https://github.com/linuxscout/arramooz",
        "http://arramooz.sourceforge.net/",
        "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
    ),
    attribution_requirement=(
        "يُنسَب الجدولُ إلى Taha Zerrouki وجامعِ بياناته Mohamed Kebdani بنصِّ "
        "الاستشهاد المُعلَن في ترويسة المستودع. " + _GPL_ATTRIBUTION_NOTE
    ),
    annotation_note=_TABLE_ANNOTATION_NOTE,
)

QUTRUB_TRILATERAL_VERB_TABLE_WITNESS_SECOND_MIRROR: Final[IrabCorpusWitness] = (
    IrabCorpusWitness(
        corpus="Qutrub trilateral verb table, in the Qutrub conjugator itself",
        version="master branch as measured",
        upstream="https://github.com/linuxscout/qutrub",
        measured_mirror="raw.githubusercontent.com/linuxscout/qutrub",
        measured_path="libqutrub/triverbtable.py",
        sha256="75fc716f39b0ee151a1f292a7576a41856f423bf3d837bfb7e92a9a557aa7d8a",
        byte_length=846_066,
        licenses=("GNU General Public License",),
        required_attribution_links=(
            "https://github.com/linuxscout/qutrub",
            "https://www.gnu.org/licenses/gpl.html",
        ),
        attribution_requirement=(
            "المرآةُ الثانيةُ للجدول نفسِه في مُصرِّف Qutrub، ورخصتُه `GPL` "
            "منصوصةٌ في `COPYING` بالمستودع. "
            + TWO_MIRRORS_ONE_DIGEST_IS_NOT_TWO_WITNESSES_NOTE
            + " — "
            + _GPL_ATTRIBUTION_NOTE
        ),
        annotation_note=_TABLE_ANNOTATION_NOTE,
    )
)

ARRAMOOZ_BRUT_VERB_DATA_WITNESS: Final[IrabCorpusWitness] = IrabCorpusWitness(
    corpus="Arramooz Alwaseet manual verb data",
    version="release 0.3, master branch as measured",
    upstream="https://github.com/linuxscout/arramooz",
    measured_mirror="raw.githubusercontent.com/linuxscout/arramooz",
    measured_path="data/verbs/verb_dic_data-net.csv",
    sha256="e54cb3fe3992e45344dba34058e08a67fe61fce4d1d06b447dd0e5971cfbd970",
    byte_length=580_755,
    licenses=("GNU General Public License, version 2",),
    required_attribution_links=(
        "https://github.com/linuxscout/arramooz",
        "http://arramooz.sourceforge.net/",
        "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
    ),
    attribution_requirement=(
        "بياناتٌ جُمِعت يدويًّا، يُنسَب جمعُها في ترويسة المستودع إلى "
        "Mohamed Kebdani والمشروعُ إلى Taha Zerrouki. " + _GPL_ATTRIBUTION_NOTE
    ),
    annotation_note=(
        "ملفٌّ مفصولٌ بالجدولة باثني عشر عمودًا مُسمّاةً في سطرٍ أوّلَ يبدأ "
        "بـ`#`: منها `root` و`verb` و`class` و`bab`. وحُكمُ اللزوم/التعدّي "
        "**ليس عمودًا فيه**، بل يُولَّد من رمز النموذج بشفرة المستودع؛ "
        "فهو مُودَعٌ هنا شاهدًا على منشأ الجدول لا مصدرًا للحكم. "
        + A_LEXICON_IS_NOT_A_CORPUS_NOTE
    ),
)


class TransitivityMark(Enum):
    """حرفُ اللزوم/التعدّي كما هو في الجدول، بدلالته المنصوصة عند أهله."""

    TRANSITIVE = "م"
    COMMON = "ك"
    INTRANSITIVE = "ل"


@dataclass(frozen=True, slots=True)
class TrilateralVerbEntry:
    """مدخلُ فعلٍ ثلاثيٍّ واحدٍ من الجدول، بحقوله الخمسة كما قُرِئت."""

    verb: str
    root: str
    bab: int
    mark: TransitivityMark
    haraka: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.verb, "صورةُ الفعل"),
            (self.root, "جذرُ الفعل"),
            (self.haraka, "حركةُ عينِ المضارع"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise TransitivityLexiconError(f"{label} نصٌّ غير فارغ.")
        if not isinstance(self.bab, int) or self.bab < 1:
            raise TransitivityLexiconError("بابُ الفعل عددٌ صحيحٌ موجب.")
        if not isinstance(self.mark, TransitivityMark):
            raise TransitivityLexiconError(
                "وَسْمُ اللزوم/التعدّي من `TransitivityMark` وحدَها؛ وحرفٌ "
                "خارجَها لا يُقرَأ بالظنّ."
            )


_ENTRY_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\{'verb':u'(?P<verb>[^']*)',"
    r"'root':u'(?P<root>[^']*)',"
    r"'bab':(?P<bab>\d+),"
    r"'transitive':u'(?P<mark>[^']*)',"
    r"'haraka':u'(?P<haraka>[^']*)'\}"
)


def read_trilateral_entries(text: str) -> tuple[TrilateralVerbEntry, ...]:
    """يقرأ مداخلَ الجدول بمطابقةِ نصٍّ لا بتنفيذِ الملفّ.

    `THE_TABLE_IS_READ_NOT_EXECUTED`: الملفُّ شفرةُ بايثون، وتنفيذُه لقراءةِ
    بياناته يُدخِل شفرةَ غيرِنا في عمليَّتنا. فيُقرأ نصًّا بمطابقةٍ مُعلَنة؛
    ومن نفّذه ليقرأه ائتمن ما لم يفحص.
    """
    if not isinstance(text, str):
        raise TransitivityLexiconError("نصُّ الجدول نصٌّ لا بايتات؛ فيُفَكُّ ترميزُه أوّلًا.")
    entries: list[TrilateralVerbEntry] = []
    for match in _ENTRY_PATTERN.finditer(text):
        mark = match.group("mark")
        try:
            parsed_mark = TransitivityMark(mark)
        except ValueError as error:
            raise TransitivityLexiconError(
                f"وَسْمٌ غيرُ معروفٍ في الجدول: {mark!r}؛ ولا يُقرَأ بالظنّ."
            ) from error
        entries.append(
            TrilateralVerbEntry(
                verb=match.group("verb"),
                root=match.group("root"),
                bab=int(match.group("bab")),
                mark=parsed_mark,
                haraka=match.group("haraka"),
            )
        )
    if not entries:
        raise TransitivityLexiconError(
            "لم يُقرَأ من الجدول مدخلٌ واحد؛ وجدولٌ فارغٌ ليس شاهدًا."
        )
    return tuple(entries)


def roots_by_mark(
    entries: tuple[TrilateralVerbEntry, ...],
) -> dict[str, frozenset[TransitivityMark]]:
    """يجمع لكلِّ جذرٍ وسومَ مداخله كلَّها، ولا يختار بينها.

    `A_ROOT_MAY_CARRY_MORE_THAN_ONE_MARK`: للجذر الواحد أبوابٌ عدّة، وقد
    يختلف وَسْمُها. فتُجمَع الوسومُ كما هي ولا يُرجَّح أحدُها على الآخر هنا؛
    والترجيحُ قاعدةٌ تُسَنّ في مواصفةٍ لا نتيجةٌ تُقرأ من الجدول.
    """
    collected: dict[str, set[TransitivityMark]] = {}
    for entry in entries:
        collected.setdefault(entry.root, set()).add(entry.mark)
    return {root: frozenset(marks) for root, marks in collected.items()}


REDERIVED_ENTRIES: Final[int] = 7_953
REDERIVED_DISTINCT_VERBS: Final[int] = 6_909
REDERIVED_DISTINCT_ROOTS: Final[int] = 5_196

REDERIVED_MARK_COUNTS: Final[dict[TransitivityMark, int]] = {
    TransitivityMark.INTRANSITIVE: 3_656,
    TransitivityMark.COMMON: 2_977,
    TransitivityMark.TRANSITIVE: 1_320,
}

REDERIVED_ROOT_LEVEL_COUNTS: Final[dict[tuple[str, ...], int]] = {
    ("ل",): 1_587,
    ("ك",): 1_502,
    ("ك", "ل"): 905,
    ("م",): 740,
    ("ل", "م"): 331,
    ("ك", "م"): 78,
    ("ك", "ل", "م"): 53,
}

REDERIVED_BAB_COUNTS: Final[dict[int, int]] = {
    1: 2_210,
    2: 1_920,
    3: 1_200,
    4: 2_071,
    5: 523,
    6: 29,
}

REDERIVED_HARAKA_COUNTS: Final[dict[str, int]] = {
    "فتحة": 3_271,
    "ضمة": 2_733,
    "كسرة": 1_949,
}

WITNESS_ROOT_ALPHABET: Final[str] = "ءأبتثجحخدذرزسشصضطظعغفقكلمنهوي"

QAC_ROOT_ALPHABET: Final[str] = "$*ADEHSTZbdfghjklmnqrstvwxyz"

REDERIVED_ROOTS_JOINING_THE_PARTITION_UNCHANGED: Final[int] = 0


def _assert_the_deposit_is_a_witness_not_a_result() -> None:
    forbidden = {"agree", "agreement", "confirms", "supports", "result", "verdict"}
    for field in fields(TrilateralVerbEntry):
        for word in field.name.split("_"):
            if word in forbidden:
                raise TransitivityLexiconError(
                    f"`{field.name}` حقلٌ يحمل نتيجةً؛ والمُودَعُ شاهدٌ لا حكم."
                )


def _assert_the_mark_counts_sum_to_the_entries() -> None:
    if sum(REDERIVED_MARK_COUNTS.values()) != REDERIVED_ENTRIES:
        raise TransitivityLexiconError(
            "مجموعُ الوسوم لا يساوي عددَ المداخل؛ وإحصاءٌ لا يُجمَع لا يُودَع."
        )
    if sum(REDERIVED_BAB_COUNTS.values()) != REDERIVED_ENTRIES:
        raise TransitivityLexiconError(
            "مجموعُ الأبواب لا يساوي عددَ المداخل؛ وإحصاءٌ لا يُجمَع لا يُودَع."
        )
    if sum(REDERIVED_HARAKA_COUNTS.values()) != REDERIVED_ENTRIES:
        raise TransitivityLexiconError(
            "مجموعُ الحركات لا يساوي عددَ المداخل؛ وإحصاءٌ لا يُجمَع لا يُودَع."
        )
    if sum(REDERIVED_ROOT_LEVEL_COUNTS.values()) != REDERIVED_DISTINCT_ROOTS:
        raise TransitivityLexiconError(
            "مجموعُ تجميعات الوسوم لا يساوي عددَ الجذور؛ وإحصاءٌ لا يُجمَع لا يُودَع."
        )


def _assert_the_two_mirrors_carry_one_digest() -> None:
    first = QUTRUB_TRILATERAL_VERB_TABLE_WITNESS
    second = QUTRUB_TRILATERAL_VERB_TABLE_WITNESS_SECOND_MIRROR
    if first.sha256 != second.sha256 or first.byte_length != second.byte_length:
        raise TransitivityLexiconError(
            "المرآتان أُودِعتا بوصفهما ملفًّا واحدًا، فاختلافُ البصمة أو الطول "
            "يُكذِّب الوصف؛ ولا يُصحَّح بإخفاء أحدهما."
        )
    if first.measured_mirror == second.measured_mirror:
        raise TransitivityLexiconError(
            "المرآتان موضعان مختلفان؛ ومرآةٌ مكرّرةٌ لا تُسمّى ثانية."
        )


_assert_the_deposit_is_a_witness_not_a_result()
_assert_the_mark_counts_sum_to_the_entries()
_assert_the_two_mirrors_carry_one_digest()
