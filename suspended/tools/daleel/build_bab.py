"""الباني: يستخرج الدليل من البايتات بإزاحته، ولا يكتبه من عنده.

القرارُ الحامل لهذه الأداة — يُسجَّل ههنا لا في مراسلة:

    الآلةُ تبني برهانَها ولا تنتظر النقلَ اليدويّ. فما كان يدويًّا في إيداع
    عقد `encyclopedia/tariqa/` إنما هو **إدخالُ الاقتباسات**، وهو استخراجٌ
    لا اجتهاد؛ وما استقرّ ميكانيكيًّا في التحقيق جاز تعميمُه في التوليد:
    **ما لا يستطيع الفاحصُ إثباتَه من البايتات لا يولّده الباني أصلًا.**

    والفاتورة: **صفرُ طيٍّ** — الباني لا يختصر نصًّا ولا يُعيد كتابته، بل
    يستخرجه بإزاحته وطوله، فيكون نصُّ المخرَج شريحةً من نصّ المصدر لا نسخةً
    منه. وبابُ الإبطال: إن ولّد اقتباسًا لا يطابق البايتاتِ مرّةً واحدة
    يُوقَف ويُراجَع بناؤه — فالكاذبُ الواحد يقتل الثقةَ كلَّها.

**وتصحيحُ مقدّمة القرار من القرص، لا تلطيفًا بل نقضًا لما لا يقوم:**

* **لا فاحصَ كان قائمًا قبل هذه الأداة.** لم يكن في الشجرة ملفُّ بايثون
  واحدٌ يذكر `encyclopedia/tariqa` ولا بايتاتِ المقام؛ فالمطابقةُ التي جرت
  في الجلسات جرت بأوامرَ عابرةٍ لم تُودَع. فهذه الأداةُ **أوّلُ** فاحصٍ لا
  تعميمُ فاحصٍ سابق، والحجّةُ عليها من عملها الآن لا من تاريخٍ مرويّ.
* **العقدتان `03` و`04` ليستا في هذه الشجرة.** فأعدادُ إثباتهما أرقامُ
  جلسةٍ لا موضعَ لها على القرص، وهي تحت البابِ الثاني عشر من
  `docs/USOOL_AL-UNBOOB.md` تُنقَل نصًّا ولا تُحوَّل عددًا. وتمرينُ الباني
  الأوّلُ على **ما وُجد** من العقد لا على ما رُوي أنّه أُودِع.

**وما يبقى بيد العقل — إعلانٌ لا تقصير.** ثلاثةٌ لا تؤول إلى هذه الأداة:
القياسُ بالأثر، والترجمةُ على الآلة، وبابُ الإبطال. فالآلةُ تستخرج وتعدّ
وتَسِم وتصدّ، والعقلُ يحكم ويقيس ويجرّب — والباني **واعظُ الاستخراج لا
عاقلُه**.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Final

REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[2]

SOURCE_BYTES: Final[Path] = REPO_ROOT / "التفكير(71)(3).doc"

NODES_ROOT: Final[Path] = REPO_ROOT / "encyclopedia" / "tariqa"

THE_RULER: Final[str] = (
    "فكُّ الملفّ كلِّه `utf-16-le` متساهلًا، ثمّ `NFC`، ثمّ طيُّ كلِّ بياضٍ "
    "متتالٍ إلى فراغٍ واحد — بلا تجريدِ تشكيلٍ ولا إسقاطِ ترقيم."
)

OPEN_QUOTE: Final[str] = "«"
CLOSE_QUOTE: Final[str] = "»"

DEPOSITOR_ELISION: Final[str] = "[…]"
THE_BOOKS_OWN_ELLIPSIS: Final[str] = "…"

REASONED_SLOT: Final[str] = "<<بناءَ العقل — لا يملؤه الباني>>"

A_QUOTE_IS_A_SLICE_NOT_A_COPY: Final[str] = (
    "A_QUOTE_IS_A_SLICE_NOT_A_COPY: نصُّ كلِّ اقتباسٍ يُقرَأ من نصّ المصدر "
    "بإزاحته وطوله؛ فلا يمرّ عبر الباني حرفٌ كُتب من خارج البايتات."
)

THE_BUILDER_DOES_NOT_REASON: Final[str] = (
    "THE_BUILDER_DOES_NOT_REASON: القياسُ بالأثر واللزوميةُ بناءُ عقلٍ لا "
    "استخراج؛ فيترك الباني موضعَهما فارغًا موسومًا ولا يملؤه."
)

A_SOURCE_DEFECT_IS_COPIED_AND_NAMED_NOT_MENDED: Final[str] = (
    "A_SOURCE_DEFECT_IS_COPIED_AND_NAMED_NOT_MENDED: عطبُ نصّ المصدر يخرج "
    "كما هو لأنّ المخرَج شريحة؛ وتصحيحُه ههنا ممتنعٌ بنيويًّا لا مكروهًا أدبًا."
)

A_VERSE_COMES_FROM_THE_SOURCE_NOT_FROM_A_MUSHAF: Final[str] = (
    "A_VERSE_COMES_FROM_THE_SOURCE_NOT_FROM_A_MUSHAF: الآيةُ تُستخرَج من نصّ "
    "الكتاب برسمه الذي فيه؛ ولا يقرأ الباني مدوّنةً أخرى فيختلف الرسم."
)

THE_TWO_BASES_ARE_DECLARED_NEVER_MIXED: Final[str] = (
    "THE_TWO_BASES_ARE_DECLARED_NEVER_MIXED: العدُّ يخرج بأساسين مُعلَنين — "
    "المركّبِ (العبارة بتمامها) والمفردِ (كلمتها الأخيرة وحدها) — ولا يُعرَض "
    "عددٌ بلا أساسه."
)

THE_UNIQUENESS_CLAIM: Final[str] = "وُجد في نصّ الحاوية مرّةً واحدةً"

OCCURRENCE_IS_NOT_UNIQUENESS_AND_THE_CLAIM_IS_MEASURED: Final[str] = (
    "OCCURRENCE_IS_NOT_UNIQUENESS_AND_THE_CLAIM_IS_MEASURED: وقوعُ الشريحة "
    "في البايتات غيرُ تفرّدها فيها؛ فصفحةٌ تكتفي بدعوى الوقوع لا يُطالَبُ "
    "نقلُها بالتفرّد، وصفحةٌ تدّعي «مرّةً واحدةً» يُقاس تفرُّدُ كلِّ شريحةٍ "
    "فيها ويسقط بناؤها إن كذبت الدعوى. فالحارسُ يتبع الدعوى ولا يفرض عليها "
    "شرطًا لم ترفعه."
)

A_RULE_CITED_IN_PROSE_IS_LOCATED_NOT_TRANSCRIBED: Final[str] = (
    "قاعدتا القياس اللتان يحملهما البابُ الخامس عشر من وثيقة الأصول تُفتَحان "
    "ههنا من البايتات عند كلّ تشغيل، فإن زالت واحدةٌ منهما أو تبدّل حرفٌ فيها "
    "سقطت البوّابة. ولا يُنقَل موضعُهما عددًا إلى نثر الوثيقة: العددُ المنقول "
    "لا فاتورةَ له، والموضعُ ههنا مولَّدٌ من مولِّده."
)

THE_NOTES: Final[tuple[str, ...]] = (
    A_QUOTE_IS_A_SLICE_NOT_A_COPY,
    THE_BUILDER_DOES_NOT_REASON,
    A_SOURCE_DEFECT_IS_COPIED_AND_NAMED_NOT_MENDED,
    A_VERSE_COMES_FROM_THE_SOURCE_NOT_FROM_A_MUSHAF,
    THE_TWO_BASES_ARE_DECLARED_NEVER_MIXED,
    OCCURRENCE_IS_NOT_UNIQUENESS_AND_THE_CLAIM_IS_MEASURED,
    A_RULE_CITED_IN_PROSE_IS_LOCATED_NOT_TRANSCRIBED,
)


class BuilderError(ValueError):
    """رُفض مدخلٌ أو انكشف اقتباسٌ لا تسنده البايتات؛ ولا يُحمَل على أقربَ موضع."""


def fold(text: str) -> str:
    """المسطرةُ المُعلَنة، مطبَّقةً على أيّ نصٍّ قبل الموازنة."""

    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


@lru_cache(maxsize=1)
def source_text() -> str:
    """نصُّ المقام كما تخرجه المسطرةُ من بايتاته؛ يُقرَأ مرّةً ويُشارَك."""

    if not SOURCE_BYTES.is_file():
        raise BuilderError(
            f"بايتاتُ المقام غائبةٌ عن `{SOURCE_BYTES.name}`؛ ولا يبني الباني "
            "على مصدرٍ لا يفتحه."
        )
    raw = SOURCE_BYTES.read_bytes()
    return fold(raw.decode("utf-16-le", errors="ignore"))


def source_fingerprint() -> str:
    """بصمةُ البايتات — لا بصمةُ النصّ المفكوك — فالمقامُ بايتاتُه لا قراءتُه."""

    return hashlib.sha256(SOURCE_BYTES.read_bytes()).hexdigest()


@dataclass(frozen=True, slots=True)
class Locus:
    """موضعُ شريحةٍ في نصّ المصدر: إزاحةٌ وطول، ونصُّها يُقرَأ ولا يُخزَّن."""

    offset: int
    length: int

    def __post_init__(self) -> None:
        if self.offset < 0 or self.length <= 0:
            raise BuilderError("الإزاحةُ غيرُ سالبة والطولُ موجب.")
        if self.offset + self.length > len(source_text()):
            raise BuilderError("موضعٌ يتجاوز نهايةَ نصّ المصدر.")

    @property
    def text(self) -> str:
        """النصُّ مقروءًا من المصدر عند كلّ طلب — فلا نسخةَ تُعدَّل في الطريق."""

        return source_text()[self.offset : self.offset + self.length]


def locate(fragment: str) -> Locus:
    """موضعُ شريحةٍ واحدةٍ في المصدر؛ ويُرفَض ما لا تسنده البايتات."""

    needle = fold(fragment)
    if not needle:
        raise BuilderError("شريحةٌ فارغةٌ لا موضعَ لها.")
    offset = source_text().find(needle)
    if offset < 0:
        raise BuilderError(
            f"شريحةٌ لا تقع في البايتات: «{needle[:60]}» — والباني لا يولّد "
            "ما لا يثبته الفاحصُ من المصدر."
        )
    return Locus(offset=offset, length=len(needle))


def occurrences(fragment: str) -> int:
    """عددُ وقوعِ شريحةٍ في المصدر؛ عددٌ خامٌ لا حكمَ فيه على تفرّدها."""

    needle = fold(fragment)
    if not needle:
        raise BuilderError("شريحةٌ فارغةٌ لا تُعَدّ.")
    return source_text().count(needle)


THE_ANALOGY_RULES: Final[tuple[str, ...]] = (
    "لأن الجنس الواحد الذي لا يختلف، أو النوع الواحد الذي يختلف، ينطبق على "
    "جنسه وعلى نوعه كل ما ثبت لفرد من أفراده، لأنه جنس واحد ونوع واحد",
    "فلا يعمم على غيرها ولا يقاس عليها. لا قياساً شمولياً ولا قياساً حقيقياً، "
    "بل يجب أن يؤخذ لتلك الحادثة وحدها",
)


def analogy_rule_loci() -> tuple[Locus, ...]:
    """مواضعُ قاعدتَي القياس في المصدر — مولَّدةٌ لا منقولة."""

    return tuple(locate(rule) for rule in THE_ANALOGY_RULES)


@dataclass(frozen=True, slots=True)
class TermCensus:
    """عدُّ مصطلحٍ بأساسَيه مُعلَنَين؛ ولا يُقرأ أحدهما مكان الآخر."""

    term: str
    compound_base: str
    compound: int
    simple_base: str
    simple: int


def census(term: str) -> TermCensus:
    """العدُّ بأساسين: العبارةُ بتمامها، وكلمتُها الأخيرة وحدها."""

    compound = fold(term)
    if not compound:
        raise BuilderError("مصطلحٌ فارغٌ لا يُعَدّ.")
    simple = compound.split(" ")[-1]
    return TermCensus(
        term=compound,
        compound_base="العبارةُ بتمامها",
        compound=source_text().count(compound),
        simple_base="الكلمةُ الأخيرةُ وحدها",
        simple=source_text().count(simple),
    )


@dataclass(frozen=True, slots=True)
class Passage:
    """اقتباسٌ مؤلَّفٌ من شرائحَ متتاليةٍ يفصلها حذفُ المودِع، كلٌّ بموضعه."""

    loci: tuple[Locus, ...]

    def __post_init__(self) -> None:
        if not self.loci:
            raise BuilderError("اقتباسٌ بلا شريحةٍ واحدة.")
        previous = self.loci[0]
        for locus in self.loci[1:]:
            if locus.offset < previous.offset + previous.length:
                raise BuilderError(
                    "شرائحُ اقتباسٍ غيرُ متتاليةٍ في المصدر؛ وجملةٌ تُركَّب من "
                    "موضعين متداخلين أو معكوسين تلفيقٌ لا نقل."
                )
            previous = locus

    @property
    def rendered(self) -> str:
        """الاقتباسُ مبنيًّا من شرائحه وحدها، وعلامةُ الحذف علامةُ المودِع."""

        return f" {DEPOSITOR_ELISION} ".join(locus.text for locus in self.loci)

    @property
    def elision_spans(self) -> tuple[int, ...]:
        """طولُ ما طواه المودِع عند كلِّ حذف — فيُرى الطيُّ ولا يُخفى."""

        return tuple(
            following.offset - (earlier.offset + earlier.length)
            for earlier, following in zip(self.loci, self.loci[1:], strict=False)
        )


def build_passage(quoted: str) -> Passage:
    """يبني اقتباسًا من نصٍّ مُرسَل: يقسمه على حذف المودِع ويُثبت كلَّ شريحة."""

    fragments = [part for part in fold(quoted).split(DEPOSITOR_ELISION) if fold(part)]
    if not fragments:
        raise BuilderError("اقتباسٌ لا شريحةَ فيه بعد رفع علامات الحذف.")
    return Passage(loci=tuple(locate(fragment) for fragment in fragments))


def reasoned_slot(question: str) -> str:
    """موضعٌ يتركه الباني فارغًا موسومًا؛ الأثرُ واللزوميةُ ليسا استخراجًا."""

    if not fold(question):
        raise BuilderError("موضعُ العقل يُسمّى سؤالُه ولا يُترَك بلا عنوان.")
    return f"{REASONED_SLOT} {fold(question)}"


def standing_in_tree(path: str) -> str:
    """وسمُ الموضع: حاضرٌ في الشجرة أو خارجَها — فلا يمرّ شاهدٌ بلا موضع."""

    if (REPO_ROOT / path).exists():
        return "حاضرٌ في الشجرة"
    return "خارجُ الشجرة (شاهدٌ موسوم)"


_QUOTE = re.compile(f"{OPEN_QUOTE}([^{OPEN_QUOTE}{CLOSE_QUOTE}]+){CLOSE_QUOTE}")

_DEPOSITOR_MARKUP = re.compile(r"\*\*|`")

_BLOCKQUOTE_MARK = re.compile(r"^[ \t]*>[ \t]?", re.MULTILINE)

_CODE_SPAN = re.compile(r"`[^`]*`")

THE_SEPARATOR: Final[str] = "---"

THE_AUDITED_REGION_IS_THE_TRANSCRIPTION_NOT_THE_VERDICT: Final[str] = (
    "THE_AUDITED_REGION_IS_THE_TRANSCRIPTION_NOT_THE_VERDICT: عهدُ «كلُّ ما "
    "بين «» منقولٌ» إنما هو فوق الخطّ الفاصل؛ وتحتَه حكمُ الشجرة، وفيه تُستعمل "
    "«» لتسمية مصطلحاتها هي. فلا يُمرَّر ما تحت الخطّ على بايتات المقام، وإمرارُه "
    "يقلب أداةَ صدقٍ إلى مولِّد إنذارٍ كاذب."
)

THE_TREE_KEEPS_TWO_PAGE_SHAPES_AND_ONE_RULE_WOULD_BLIND_THE_TOOL: Final[str] = (
    "THE_TREE_KEEPS_TWO_PAGE_SHAPES_AND_ONE_RULE_WOULD_BLIND_THE_TOOL: "
    "صفحاتُ العقد على شكلين مقيسين من القرص، لا واحدٍ. منها ما يفتح بترويسةٍ "
    "يُغلقها خطٌّ ثمّ يأتي النقلُ ثمّ خطٌّ ثانٍ ثمّ الحكم — وهو ما تصرّح به "
    "ترويسةُ 00_aqida بنصّها: «ما دون الخطّ الأول نصُّ العقدة… وما بعد الخطّ "
    "الفاصل الثاني حكمُ هذه الشجرة». ومنها ما يفتح بالنقل مباشرةً فخطٌّ واحدٌ "
    "يليه الحكم. فالقاعدةُ: الحكمُ يبدأ عند الخطّ الأخير، والنقلُ ينتهي عنده؛ "
    "ويُطرَح ما قبل الخطّ الأول إن كانت الخطوطُ أكثرَ من واحد. وقطعُ الأداة عند "
    "الخطّ الأول وحدَه كان يُخرِج صفحاتٍ كاملةً من الفحص ثمّ يطبع لها علامةَ "
    "سلامة — وهو أسوأ من سكوتها، لأنّه سكوتٌ يدّعي الكلام."
)

THE_DEPOSITORS_MARKUP_IS_NOT_THE_BOOKS_LETTERS: Final[str] = (
    "THE_DEPOSITORS_MARKUP_IS_NOT_THE_BOOKS_LETTERS: تشديدُ المودِع "
    "(`**` و`` ` ``) وَسْمُ صفحةٍ لا حرفٌ من الكتاب؛ فيُرفَع قبل الموازنة ولا "
    "يُحمَّل على المصدر. وكذلك علامةُ الاقتباس في ماركداون (`>`) في أوّل السطر: "
    "نقلٌ طويلٌ يمتدّ أسطرًا يحملها في وسطه، فتُحمَّل على الكتاب حروفًا لم يكتبها "
    "ويُردّ النقلُ الصحيحُ تسميةً — وهو إنذارٌ كاذبٌ من جنس ما يمنعه حدُّ الأداة."
)


def transcription_region(document: str) -> str:
    """موضعُ عهد النقل: ما انتهى عند الخطّ الأخير، وبدأ بعد الأول إن تعدّدت."""

    lines = document.splitlines()
    rules = [index for index, line in enumerate(lines) if line.strip() == THE_SEPARATOR]
    if not rules:
        return document
    if len(rules) == 1:
        return "\n".join(lines[: rules[0]])
    return "\n".join(lines[rules[0] + 1 : rules[-1]])


def quotes_in(document: str) -> tuple[str, ...]:
    """اقتباساتُ صفحةٍ كما كُتبت بين «»، مرفوعًا عنها وَسْمُ المودِع وحدَه."""

    return tuple(
        _DEPOSITOR_MARKUP.sub("", _BLOCKQUOTE_MARK.sub("", match.group(1)))
        for match in _QUOTE.finditer(document)
    )


def stray_ellipses_outside_quotes(document: str) -> int:
    """نقاطٌ مفردةٌ خارج «» — اشتباهٌ بنقاط الكتاب؛ حذفُ المودِع `[…]` وحده.

    ونطاقُ الشيفرة مطروحٌ على حكم منازل الأداة الثلاث: نقطةٌ بين علامتَي
    `` ` `` **تسميةٌ للعلامة** لا استعمالٌ لها — كقول الصفحة إنّ الكتاب
    يستعمل `…` فاصلًا. وعدُّها اشتباهًا يجعل الصفحةَ تسقط لأنّها **شرحت**
    قاعدةَ نقلها، وذاك إنذارٌ كاذبٌ يعاقب الإفصاح.
    """

    outside = _QUOTE.sub(" ", document).replace(DEPOSITOR_ELISION, " ")
    return _CODE_SPAN.sub(" ", outside).count(THE_BOOKS_OWN_ELLIPSIS)


@dataclass(frozen=True, slots=True)
class NodeAudit:
    """حكمُ الفاحص على عقدةٍ واحدة بثلاث منازلَ لا منزلتين.

    وثلاثُ المنازل ضرورةٌ مقيسةٌ لا تفصيلٌ زائد: علامتا «» في هذه الشجرة
    تحملان عملين — نقلًا من المقام، وتسميةً لمصطلحٍ من مصطلحات الشجرة
    (كـ«بناء المودِع») أو للفظٍ **يُنفى وقوعُه** في الكتاب (كـ«ترجيح»).
    فردُّ كلِّ ما لا تسنده البايتاتُ كذبًا يقلب الأداةَ مولِّدَ إنذارٍ كاذب،
    وهو أخطرُ على الثقة من سكوتها. فالمنزلةُ القاتلةُ واحدة: **التلفيق** —
    شريحتان تُعرَضان متتاليتين وهما في المصدر معكوستان أو متداخلتان — وهذه
    وحدَها لا تحتمل براءةً، فعليها وحدَها يقف بابُ الإبطال.
    """

    node: str
    quotes: int
    established: int
    not_in_source: tuple[str, ...]
    fabricated: tuple[str, ...]
    stray_ellipses: int
    claims_uniqueness: bool
    repeated_slices: tuple[str, ...]

    @property
    def is_clean(self) -> bool:
        """`True` حين لا تلفيقَ ولا نقطةَ حذفٍ ملتبسةٌ، ولا دعوى تفرّدٍ مكذوبة."""

        return (
            not self.fabricated
            and self.stray_ellipses == 0
            and not self.unsupported_uniqueness
        )

    @property
    def unsupported_uniqueness(self) -> tuple[str, ...]:
        """شرائحُ تقع أكثرَ من مرّةٍ في صفحةٍ ادّعت أنّ كلَّ اقتباسٍ فيها فريد."""

        return self.repeated_slices if self.claims_uniqueness else ()


def audit_node(path: Path) -> NodeAudit:
    """يُمرّ كلَّ اقتباسٍ فوق الخطّ على البايتات ويُنزِله منزلتَه."""

    document = path.read_text(encoding="utf-8")
    region = transcription_region(document)
    quoted_all = quotes_in(region)
    not_in_source: list[str] = []
    fabricated: list[str] = []
    repeated: list[str] = []
    established = 0
    for quoted in quoted_all:
        try:
            passage = build_passage(quoted)
        except BuilderError as failure:
            entry = f"{fold(quoted)[:70]} — {failure}"
            if "تلفيقٌ لا نقل" in str(failure):
                fabricated.append(entry)
            else:
                not_in_source.append(fold(quoted)[:70])
        else:
            established += 1
            for locus in passage.loci:
                tally = occurrences(locus.text)
                if tally != 1:
                    repeated.append(f"{locus.text[:60]} — وقع {tally} مرّات")
    return NodeAudit(
        node=path.parent.name,
        quotes=len(quoted_all),
        established=established,
        not_in_source=tuple(not_in_source),
        fabricated=tuple(fabricated),
        stray_ellipses=stray_ellipses_outside_quotes(region),
        claims_uniqueness=THE_UNIQUENESS_CLAIM in fold(document),
        repeated_slices=tuple(repeated),
    )


def deposited_nodes() -> tuple[Path, ...]:
    """صفحاتُ العقد المودَعة فعلًا على القرص — لا ما رُوي أنّه مودَع."""

    return tuple(sorted(NODES_ROOT.glob("*/README.md")))


def audit_all() -> tuple[NodeAudit, ...]:
    """تمرينُ الباني الأوّل: يختبر نفسه على ما أُودِع قبل أن يولّد جديدًا."""

    return tuple(audit_node(path) for path in deposited_nodes())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="الباني: استخراجٌ بإزاحةٍ لا نقلٌ بيد.")
    parser.add_argument(
        "--locate",
        metavar="نص",
        help="يُخرِج إزاحةَ شريحةٍ وطولَها من المصدر",
    )
    parser.add_argument(
        "--census",
        metavar="مصطلح",
        help="يُخرِج العدَّ بأساسيه المُعلَنين",
    )
    arguments = parser.parse_args(argv)

    if arguments.locate:
        locus = locate(arguments.locate)
        print(f"الإزاحة: {locus.offset} · الطول: {locus.length}")
        print(locus.text)
        return 0

    if arguments.census:
        tally = census(arguments.census)
        print(f"{tally.compound_base}: {tally.compound}")
        print(f"{tally.simple_base}: {tally.simple}")
        return 0

    audits = audit_all()
    if not audits:
        print("لا عقدةَ مودَعةً على القرص؛ ولا يُفتعَل تمرينٌ بلا مادّة.")
        return 1
    print(f"المقام: {SOURCE_BYTES.name} · بصمةُ بايتاته: {source_fingerprint()[:12]}")
    print(f"المسطرة: {THE_RULER}")
    rules = analogy_rule_loci()
    print(
        "قاعدتا القياس (البابُ الخامس عشر) مفتوحتان من البايتات: "
        + " · ".join(f"{locus.offset}+{locus.length}" for locus in rules)
    )
    failed = False
    for audit in audits:
        mark = "✓" if audit.is_clean else "✗"
        print(
            f"{mark} {audit.node}: {audit.established}/{audit.quotes} شريحةٌ "
            f"مُثبَتةٌ بإزاحتها · {len(audit.not_in_source)} تسميةٌ لا نقلَ "
            f"فيها · {len(audit.fabricated)} تلفيق · نقاطٌ ملتبسةٌ خارج «»: "
            f"{audit.stray_ellipses} · دعوى التفرّد: "
            f"{'مرفوعةٌ ومقيسة' if audit.claims_uniqueness else 'غيرُ مرفوعة'}"
        )
        for mention in audit.not_in_source:
            print(f"    · ليس نقلًا من المقام: {mention}")
        for repetition in audit.unsupported_uniqueness:
            print(f"    ✗ دعوى تفرّدٍ مكذوبة: {repetition}")
        for forgery in audit.fabricated:
            print(f"    ✗ تلفيق: {forgery}")
        if not audit.is_clean:
            failed = True
    if failed:
        print("بابُ الإبطال: شريحتان مُرتَّبتان على غير ترتيب المصدر — يُوقَف البناء.")
        return 1
    print("لا تلفيقَ في المودَع: كلُّ شريحةٍ مُثبَتةٍ على ترتيبها في المصدر.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
