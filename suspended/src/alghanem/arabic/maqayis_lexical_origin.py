"""`MAQAYIS` مرجعُ الأصل المعجميّ؛ والعثورُ على الجذر ليس فهمًا للكلمة.

بلغ `ArabicRoundTripV1` تسعًا وعشرين من تسعٍ وعشرين على إيداع الفاتحة، وذلك
**عددٌ كتابيّ**. وقد بقي محورُ الأصل والبنية في `classification_coverage_scheme`
بلا فحصٍ محسوم، لأنّ المرجعَ التحليليَّ لم يكن مُودَعًا. وبايتاتُ «مقاييس
اللغة» مُودَعةٌ في هذه الشجرة مُبصَّمةً في `maqayis_root_table_deposit`، فتُرفَع
بها ههنا **مسألةٌ واحدةٌ بعينها**: هل الجذرُ المُعلَن مشهودٌ في هذا المعجم؟
ويُقاس ذلك بالبحث في البايتات المُبصَّمة، فيخرج عددٌ يُعاد اشتقاقُه.

`ATTESTATION_IS_NOT_BINDING`: شهادةُ المعجم بأنّ «ضلل» مدخلٌ فيه **لا تقول** إنّ
«الضَّالِّينَ» مشتقّةٌ منه. الأولى وقوعُ سلسلةٍ في جدولٍ مُبصَّم، والثانية
دعوى اشتقاقٍ في كلمةٍ بعينها، ولا يلزم من الأولى الثانية. فرَبطُ الكلمة بجذرها
`BindingStanding.NOT_ESTABLISHED_NO_MORPHOLOGY_RAN`، ومرتبتُه العليا بلا مدخل.

`FINDING_A_ROOT_IS_NOT_UNDERSTANDING_A_WORD`: لو شهد المعجمُ بكلّ جذرٍ مُعلَنٍ
ههنا لم يُعرَف بعدُ أجامدةٌ الكلمةُ أم مصدرٌ أم مشتقّ، ولا وزنُها، ولا حكمُها
الإعرابيّ. فإثباتُ الصيغة والتصنيف عملٌ صرفيٌّ لم يجرِ، وهو مُسمًّى في
`MORPHOLOGICAL_WORK_STILL_OWED` بندًا بندًا لا مطويًّا في «لاحقًا».

`A_CANDIDATE_ROOT_IS_DECLARED_NOT_DERIVED`: لا مُستخرِجَ جذورٍ في هذا الخطّ،
فالجذرُ المُعلَن ههنا **مكتوبٌ بيدٍ هدفًا للاختبار**، والمقيسُ وقوعُه في
المعجم لا صحّتُه. ولو اشتُقّ الجذرُ من الكلمة بقاعدةٍ في هذه الشجرة ثمّ قِيس
بها لكان القياسُ على نفسه.

`AN_UNATTESTED_ROOT_IS_A_FINDING_NOT_AN_ERROR_TO_HIDE`: «هدي» مكتوبةً بالياء
ليست مدخلًا في هذا المعجم، والمدخلُ فيه «هدى» بالألف المقصورة. فيُعرَض عدمُ
الشهادة كما خرج، ولا تُبدَّل السلسلةُ بعد رؤية النتيجة لتُرفَع النسبة؛ وسببُه
المُسمّى أنّ الشهادةَ **تابعةٌ لرسم الجذر في المرجع نفسِه**، وهذا حدٌّ على
القياس يُكتَب ولا يُطوى.

`NOT_EVERY_WORD_IS_LICENSED_A_ROOT`: الحروفُ والأدواتُ والأسماءُ المبنيّةُ لا
يُنتزَع لها جذرٌ ليُبحَث عنه، فـ«الَّذِينَ» تخرج من المقسوم عليه بالتصريح
`NOT_LICENSED_FOR_THIS_WORD` لا بالإهمال، ولا تُحسَب إخفاقَ بحث.

`THE_LEXICON_IS_A_COPY_NOT_A_CENSUS_OF_ARABIC`: ما يشهد به هذا الملفُّ فهو
شهادتُه هو، بهذه النسخة وبرسمها؛ وغيابُ سلسلةٍ عنه ليس نفيًا لوجودها في
العربية، كما في `A_COUNT_IN_A_FILE_IS_NOT_A_COUNT_IN_ARABIC`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .classification_coverage_scheme import (
    COVERAGE_ITEMS,
    ClassificationCategory,
    CoverageItem,
)
from .maqayis_root_table_deposit import (
    FROZEN_ROOT_TABLE,
    root_table_rows,
)

__all__ = [
    "ATTESTATION_IS_NOT_BINDING_NOTE",
    "A_CANDIDATE_ROOT_IS_DECLARED_NOT_DERIVED_NOTE",
    "AN_UNATTESTED_ROOT_IS_A_FINDING_NOT_AN_ERROR_TO_HIDE_NOTE",
    "DECLARED_CANDIDATE_ROOTS",
    "FINDING_A_ROOT_IS_NOT_UNDERSTANDING_A_WORD_NOTE",
    "LEXICAL_ORIGIN_REFERENCE",
    "MORPHOLOGICAL_WORK_STILL_OWED",
    "NOT_EVERY_WORD_IS_LICENSED_A_ROOT_NOTE",
    "THE_LEXICON_IS_A_COPY_NOT_A_CENSUS_OF_ARABIC_NOTE",
    "BindingStanding",
    "CandidateRoot",
    "LexicalOriginError",
    "LexicalOriginReference",
    "LexicalOriginReport",
    "LexicalOriginRow",
    "MorphologicalDebt",
    "MorphologicalQuestion",
    "RootAttestation",
    "attested_root_types",
    "render_lexical_origin",
    "root_index",
    "run_lexical_origin",
]


class LexicalOriginError(ValueError):
    """رُوجِع مرجعُ الأصل بما لا يقوم به؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class RootAttestation(Enum):
    """حكمُ البحث في المعجم المُبصَّم؛ ثلاثةٌ لا رابعَ لها ولا «قريب»."""

    ATTESTED = "مشهود_في_المعجم_المُودَع"
    NOT_ATTESTED = "غير_مشهودٍ_في_المعجم_المُودَع"
    NOT_LICENSED_FOR_THIS_WORD = "غير_مُرخَّصٍ_لهذه_الكلمة"


class BindingStanding(Enum):
    """منزلةُ ربطِ الكلمة بجذرها؛ والعليا بلا مدخلٍ حتى يجري عملٌ صرفيّ."""

    ESTABLISHED_BY_A_MORPHOLOGICAL_DERIVATION = "مُثبَت_باشتقاقٍ_صرفيّ"
    NOT_ESTABLISHED_NO_MORPHOLOGY_RAN = "غير_مُثبَتٍ_لم_يجرِ_صرف"


class MorphologicalQuestion(Enum):
    """ما يبقى عملًا صرفيًّا بعد الشهادة المعجميّة؛ مفردةٌ مغلقةٌ لا وعدٌ عامّ."""

    THE_WORD_DERIVES_FROM_THIS_ROOT = "THE_WORD_DERIVES_FROM_THIS_ROOT"
    THE_PATTERN_OF_THE_WORD = "THE_PATTERN_OF_THE_WORD"
    JAMID_OR_MASDAR_OR_MUSHTAQQ = "JAMID_OR_MASDAR_OR_MUSHTAQQ"
    THE_IRAB_STANDING_AND_ITS_MARKER = "THE_IRAB_STANDING_AND_ITS_MARKER"


@dataclass(frozen=True, slots=True)
class LexicalOriginReference:
    """المرجعُ المعجميّ: اسمُه، وبصمتُه، وما يشهد به، وما لا يشهد به."""

    name: str
    digest: str
    what_it_settles: str
    what_it_does_not_settle: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise LexicalOriginError("المرجعُ يُسمّى باسمه لا بوصفه")
        if len(self.digest) != 64 or any(
            character not in "0123456789abcdef" for character in self.digest
        ):
            raise LexicalOriginError("مرجعُ الأصل لا يُعتمَد إلّا ببصمةٍ كاملة")
        if not self.what_it_settles.strip():
            raise LexicalOriginError("ما يحسمه المرجعُ يُكتَب ولا يُترَك مُبهَمًا")
        if not self.what_it_does_not_settle.strip():
            raise LexicalOriginError(
                "حدُّ المرجع لازمٌ لا زينة؛ فمن لم يكتب ما لا يحسمه قرأ شهادتَه فهمًا"
            )


LEXICAL_ORIGIN_REFERENCE: Final[LexicalOriginReference] = LexicalOriginReference(
    name="MAQAYIS",
    digest=FROZEN_ROOT_TABLE.sha256_hex,
    what_it_settles=(
        "وقوعُ سلسلةٍ مُعلَنةٍ مدخلًا في `root_full` من هذا الملفّ المُبصَّم، "
        "ومعها نوعُ الجذر كما كتبه الملفُّ نفسُه"
    ),
    what_it_does_not_settle=(
        "أنّ كلمةً بعينها مشتقّةٌ من ذلك المدخل، ولا وزنَها، ولا كونَها جامدةً "
        "أو مصدرًا أو مشتقّةً، ولا حكمَها الإعرابيّ؛ وهذه كلُّها عملٌ صرفيٌّ "
        "لم يجرِ، ولا يُقرأ من شهادةِ وقوعٍ في جدول"
    ),
)
"""مرجعُ الأصل المعجميّ، مُبصَّمًا؛ وبصمتُه مقروءةٌ من إيداعه لا منسوخةٌ بيد."""


MORPHOLOGICAL_WORK_STILL_OWED: Final[tuple[MorphologicalQuestion, ...]] = (
    MorphologicalQuestion.THE_WORD_DERIVES_FROM_THIS_ROOT,
    MorphologicalQuestion.THE_PATTERN_OF_THE_WORD,
    MorphologicalQuestion.JAMID_OR_MASDAR_OR_MUSHTAQQ,
    MorphologicalQuestion.THE_IRAB_STANDING_AND_ITS_MARKER,
)
"""ما يبقى مدينًا به بعد الشهادة؛ أربعةٌ تُسمّى ولا تُطوى في «لاحقًا»."""


def root_index(root: Path | None = None) -> dict[str, tuple[str, ...]]:
    """فهرسُ المداخل من البايتات المُبصَّمة: لكلّ سلسلةٍ أنواعُ جذرها كما وردت."""

    index: dict[str, list[str]] = {}
    for row in root_table_rows(root):
        index.setdefault(row["root_full"], []).append(row["root_type"])
    return {key: tuple(value) for key, value in index.items()}


@dataclass(frozen=True, slots=True)
class CandidateRoot:
    """جذرٌ مُعلَنٌ لكلمةٍ من الجدول: سلسلتُه، أو تصريحٌ بامتناع الترخيص."""

    word_key: str
    root: str | None
    licensed: bool
    why: str

    def __post_init__(self) -> None:
        if not self.word_key.strip():
            raise LexicalOriginError("الجذرُ المُعلَن يُنسَب إلى كلمةٍ بمفتاحها")
        if self.licensed and not (self.root and self.root.strip()):
            raise LexicalOriginError("جذرٌ مُرخَّصٌ بلا سلسلةٍ مكتوبةٍ لا يُبحَث عنه")
        if not self.licensed and self.root is not None:
            raise LexicalOriginError(
                "ما لا يُرخَّص له تحليلٌ جذريٌّ لا يُكتَب له جذرٌ ثمّ يُبحَث عنه"
            )
        if not self.why.strip():
            raise LexicalOriginError("الترخيصُ ومنعُه يُعلَّلان ولا يُتركان بلا سبب")


DECLARED_CANDIDATE_ROOTS: Final[tuple[CandidateRoot, ...]] = (
    CandidateRoot(
        word_key="allathina",
        root=None,
        licensed=False,
        why=(
            "اسمٌ موصولٌ مبنيٌّ لا يُتاح له تحليلٌ جذريٌّ مُرخَّص، فلا يُنتزَع له "
            "جذرٌ ليُبحَث عنه، ولا يُحسَب إخفاقَ بحث"
        ),
    ),
    CandidateRoot(
        word_key="ad_dallina",
        root="ضلل",
        licensed=True,
        why="مشتقٌّ يُتاح له تحليلٌ جذريّ، والسلسلةُ مُعلَنةٌ هدفًا للبحث",
    ),
    CandidateRoot(
        word_key="ihdina",
        root="هدي",
        licensed=True,
        why=(
            "فعلٌ معتلُّ الآخر، وسلسلتُه مكتوبةٌ بالياء كما يُعلِنها الكاتب؛ "
            "ولا تُبدَّل بعد رؤية نتيجة البحث"
        ),
    ),
    CandidateRoot(
        word_key="nabudu",
        root="عبد",
        licensed=True,
        why="فعلٌ صحيحٌ يُتاح له تحليلٌ جذريّ، والسلسلةُ مُعلَنةٌ هدفًا للبحث",
    ),
    CandidateRoot(
        word_key="anamta",
        root="نعم",
        licensed=True,
        why="فعلٌ صحيحٌ يُتاح له تحليلٌ جذريّ، والسلسلةُ مُعلَنةٌ هدفًا للبحث",
    ),
)
"""الجذورُ المُعلَنةُ قبل البحث؛ مكتوبةٌ بيدٍ، والمقيسُ وقوعُها لا صحّتُها."""


@dataclass(frozen=True, slots=True)
class LexicalOriginRow:
    """صفُّ كلمةٍ واحدة: جذرُها المُعلَن، وشهادةُ المعجم، ورَبطٌ لم يُثبَت."""

    item: CoverageItem
    candidate: CandidateRoot
    attestation: RootAttestation
    attested_types: tuple[str, ...]
    binding: BindingStanding

    def __post_init__(self) -> None:
        if self.item.key != self.candidate.word_key:
            raise LexicalOriginError("الجذرُ المُعلَن لا يُنسَب إلى كلمةٍ أخرى")
        if self.binding is not BindingStanding.NOT_ESTABLISHED_NO_MORPHOLOGY_RAN:
            raise LexicalOriginError(
                "لا اشتقاقَ صرفيًّا في هذا الخطّ، فلا يُكتَب ربطُ كلمةٍ بجذرها مُثبَتًا"
            )
        licensed = self.candidate.licensed
        if licensed == (self.attestation is RootAttestation.NOT_LICENSED_FOR_THIS_WORD):
            raise LexicalOriginError(
                "امتناعُ الترخيص يُقرأ في حكم البحث نفسِه، ولا يُخلَط بعدم الشهادة"
            )
        if self.attestation is not RootAttestation.ATTESTED and self.attested_types:
            raise LexicalOriginError("نوعُ جذرٍ بلا شهادةٍ دعوى قراءةٍ من غير مدخل")
        if self.attestation is RootAttestation.ATTESTED and not self.attested_types:
            raise LexicalOriginError("الشهادةُ تُقرأ من مدخلٍ له نوعٌ مكتوبٌ في الملفّ")

    @property
    def searched(self) -> bool:
        """أدخلت هذه الكلمةُ البحثَ أصلًا؟ وغيرُ المُرخَّص خارجُ المقسوم عليه."""

        return self.attestation is not RootAttestation.NOT_LICENSED_FOR_THIS_WORD

    @property
    def structural_categories(self) -> tuple[ClassificationCategory, ...]:
        """فئاتُ محور البنية لهذه الكلمة؛ تُعرَض ولا يُحسَم منها شيءٌ بالشهادة."""

        return tuple(
            category
            for category in self.item.categories
            if category
            in (
                ClassificationCategory.JAMID,
                ClassificationCategory.MASDAR,
                ClassificationCategory.MUSHTAQQ,
            )
        )


@dataclass(frozen=True, slots=True)
class MorphologicalDebt:
    """ما بقي عملًا صرفيًّا لكلّ كلمةٍ دخلت البحث، مُسمًّى سؤالًا سؤالًا."""

    word_key: str
    questions: tuple[MorphologicalQuestion, ...]

    def __post_init__(self) -> None:
        if not self.questions:
            raise LexicalOriginError("لا كلمةَ تُعفى من العمل الصرفيّ بشهادةِ وقوع")
        if set(self.questions) != set(MORPHOLOGICAL_WORK_STILL_OWED):
            raise LexicalOriginError(
                "الدَّينُ الصرفيُّ يُسمّى تامًّا؛ ولا يُسقَط سؤالٌ منه بلا عملٍ يُسقطه"
            )


@dataclass(frozen=True, slots=True)
class LexicalOriginReport:
    """تقريرُ الأصل المعجميّ: بحثٌ مقيس، ورَبطٌ لم يُثبَت، ودَينٌ صرفيٌّ قائم."""

    rows: tuple[LexicalOriginRow, ...]
    debts: tuple[MorphologicalDebt, ...]
    reference: LexicalOriginReference

    def __post_init__(self) -> None:
        if not self.rows:
            raise LexicalOriginError("تقريرٌ بلا صفٍّ واحدٍ ليس تقريرًا")
        keys = [row.item.key for row in self.rows]
        if len(set(keys)) != len(keys):
            raise LexicalOriginError("مفاتيحُ التقرير لا تتكرّر")
        owed = {debt.word_key for debt in self.debts}
        searched = {row.item.key for row in self.rows if row.searched}
        if owed != searched:
            raise LexicalOriginError("كلُّ كلمةٍ بُحث عن جذرها يبقى عليها دَينٌ صرفيٌّ مكتوب")

    @property
    def searched_total(self) -> int:
        """كم كلمةً دخلت البحثَ؟ وغيرُ المُرخَّص لا يدخل المقسومَ عليه."""

        return sum(1 for row in self.rows if row.searched)

    @property
    def attested_total(self) -> int:
        return sum(
            1 for row in self.rows if row.attestation is RootAttestation.ATTESTED
        )

    @property
    def unattested_total(self) -> int:
        return sum(
            1 for row in self.rows if row.attestation is RootAttestation.NOT_ATTESTED
        )

    @property
    def not_licensed_total(self) -> int:
        return sum(1 for row in self.rows if not row.searched)

    @property
    def attestation_rate(self) -> float | None:
        """نسبةُ الشهادة؛ ممتنعةٌ إن لم يدخل البحثَ جذرٌ واحد."""

        if self.searched_total == 0:
            return None
        return self.attested_total / self.searched_total

    @property
    def established_binding_total(self) -> int:
        """كم كلمةً ثبت ربطُها بجذرها؟ صفرٌ ما لم يجرِ عملٌ صرفيّ."""

        return sum(
            1
            for row in self.rows
            if row.binding is BindingStanding.ESTABLISHED_BY_A_MORPHOLOGICAL_DERIVATION
        )

    @property
    def owed_question_total(self) -> int:
        """مجموعُ الأسئلة الصرفيّة الباقية؛ مشتقٌّ بالعدّ لا مكتوب."""

        return sum(len(debt.questions) for debt in self.debts)

    def row(self, word_key: str) -> LexicalOriginRow:
        for row in self.rows:
            if row.item.key == word_key:
                return row
        raise LexicalOriginError(f"لا صفَّ للكلمة {word_key!r}")


def attested_root_types(root_string: str, root: Path | None = None) -> tuple[str, ...]:
    """أنواعُ الجذر كما كتبها الملفُّ لهذه السلسلة، أو لا شيءَ إن لم تقع فيه."""

    if not root_string.strip():
        raise LexicalOriginError("لا يُبحَث عن سلسلةٍ فارغة")
    return root_index(root).get(root_string, ())


def run_lexical_origin(
    candidates: tuple[CandidateRoot, ...] = DECLARED_CANDIDATE_ROOTS,
    items: tuple[CoverageItem, ...] = COVERAGE_ITEMS,
    root: Path | None = None,
) -> LexicalOriginReport:
    """ابحث عن الجذور المُعلَنة في المعجم المُبصَّم؛ ولا يُقرأ من الشهادة صرف."""

    if not candidates:
        raise LexicalOriginError("تقريرٌ بلا جذرٍ مُعلَنٍ واحدٍ لا يُشغَّل")
    by_key = {item.key: item for item in items}
    index = root_index(root)
    rows: list[LexicalOriginRow] = []
    debts: list[MorphologicalDebt] = []
    for candidate in candidates:
        item = by_key.get(candidate.word_key)
        if item is None:
            raise LexicalOriginError(
                f"الجذرُ المُعلَن يُحيل إلى كلمةٍ ليست في الجدول: {candidate.word_key!r}"
            )
        if not candidate.licensed:
            attestation = RootAttestation.NOT_LICENSED_FOR_THIS_WORD
            types: tuple[str, ...] = ()
        elif candidate.root is None:  # pragma: no cover - يمنعه بناءُ المُعلَن
            raise LexicalOriginError("جذرٌ مُرخَّصٌ بلا سلسلةٍ لا يُبحَث عنه")
        else:
            types = index.get(candidate.root, ())
            attestation = (
                RootAttestation.ATTESTED if types else RootAttestation.NOT_ATTESTED
            )
        row = LexicalOriginRow(
            item=item,
            candidate=candidate,
            attestation=attestation,
            attested_types=types,
            binding=BindingStanding.NOT_ESTABLISHED_NO_MORPHOLOGY_RAN,
        )
        rows.append(row)
        if row.searched:
            debts.append(
                MorphologicalDebt(
                    word_key=item.key, questions=MORPHOLOGICAL_WORK_STILL_OWED
                )
            )
    return LexicalOriginReport(
        rows=tuple(rows), debts=tuple(debts), reference=LEXICAL_ORIGIN_REFERENCE
    )


def render_lexical_origin(report: LexicalOriginReport) -> str:
    """اعرض التقريرَ: بحثٌ مقيس، ثمّ ربطٌ لم يُثبَت، ثمّ دَينٌ صرفيٌّ قائم."""

    lines = [
        f"{'word':<14}{'root':<8}{'attestation':<30}{'type':<14}binding",
        "-" * 88,
    ]
    for row in report.rows:
        root = "—" if row.candidate.root is None else row.candidate.root
        kind = "—" if not row.attested_types else "/".join(row.attested_types)
        lines.append(
            f"{row.item.key:<14}{root:<8}{row.attestation.value:<30}"
            f"{kind:<14}{row.binding.value}"
        )
    lines.append("")
    rate = report.attestation_rate
    shown = "—" if rate is None else f"{rate * 100:.4f}%"
    lines.append(
        f"searched: {report.searched_total}; attested: {report.attested_total}; "
        f"unattested: {report.unattested_total}; "
        f"not licensed: {report.not_licensed_total}; attestation rate: {shown}"
    )
    lines.append(
        f"bindings established: {report.established_binding_total}"
        f"/{report.searched_total} — لا اشتقاقَ صرفيًّا جرى، فالشهادةُ ليست ربطًا"
    )
    lines.append(
        f"morphological questions still owed: {report.owed_question_total} "
        f"({len(MORPHOLOGICAL_WORK_STILL_OWED)} لكلّ كلمةٍ بُحث عن جذرها)"
    )
    lines.append(
        f"reference: {report.reference.name} ({report.reference.digest[:16]}…) — "
        "يشهد بالوقوع في جدوله، ولا يشهد بصيغةٍ ولا بتصنيف"
    )
    return "\n".join(lines)


ATTESTATION_IS_NOT_BINDING_NOTE: Final[str] = (
    "AttestationIsNotBinding: شهادةُ `MAQAYIS` بوقوع سلسلةٍ مدخلًا في جدوله "
    "لا تقول إنّ كلمةً بعينها مشتقّةٌ منها؛ الأولى واقعةٌ في ملفٍّ مُبصَّم، "
    "والثانية دعوى اشتقاقٍ لا تُقرأ من جدول، فمنزلةُ الربط "
    "`غير_مُثبَتٍ_لم_يجرِ_صرف` ومرتبتُها العليا بلا مدخل"
)

FINDING_A_ROOT_IS_NOT_UNDERSTANDING_A_WORD_NOTE: Final[str] = (
    "FindingARootIsNotUnderstandingAWord: لو شُهد بكلّ جذرٍ مُعلَنٍ لم يُعرَف "
    "بعدُ أجامدةٌ الكلمةُ أم مصدرٌ أم مشتقّ، ولا وزنُها، ولا حكمُها الإعرابيّ؛ "
    "فإثباتُ الصيغة والتصنيف عملٌ صرفيٌّ مُسمًّى في `MORPHOLOGICAL_WORK_STILL_OWED`"
)

A_CANDIDATE_ROOT_IS_DECLARED_NOT_DERIVED_NOTE: Final[str] = (
    "ACandidateRootIsDeclaredNotDerived: لا مُستخرِجَ جذورٍ في هذا الخطّ، "
    "فالجذرُ مكتوبٌ بيدٍ هدفًا للاختبار والمقيسُ وقوعُه لا صحّتُه؛ ولو اشتُقّ "
    "بقاعدةٍ في هذه الشجرة ثمّ قِيس بها لكان القياسُ على نفسه"
)

AN_UNATTESTED_ROOT_IS_A_FINDING_NOT_AN_ERROR_TO_HIDE_NOTE: Final[str] = (
    "AnUnattestedRootIsAFindingNotAnErrorToHide: «هدي» بالياء ليست مدخلًا في "
    "هذا المعجم والمدخلُ فيه «هدى»؛ فتُعرَض عدمُ الشهادة كما خرجت ولا تُبدَّل "
    "السلسلةُ بعد رؤية النتيجة، وسببُها أنّ الشهادةَ تابعةٌ لرسم الجذر في المرجع"
)

NOT_EVERY_WORD_IS_LICENSED_A_ROOT_NOTE: Final[str] = (
    "NotEveryWordIsLicensedARoot: الحروفُ والأدواتُ والأسماءُ المبنيّةُ لا "
    "يُنتزَع لها جذرٌ ليُبحَث عنه؛ فتخرج من المقسوم عليه بالتصريح "
    "`غير_مُرخَّصٍ_لهذه_الكلمة` لا بالإهمال، ولا تُحسَب إخفاقَ بحث"
)

THE_LEXICON_IS_A_COPY_NOT_A_CENSUS_OF_ARABIC_NOTE: Final[str] = (
    "TheLexiconIsACopyNotACensusOfArabic: ما يشهد به هذا الملفُّ شهادتُه هو "
    "بهذه النسخة وبرسمها، وغيابُ سلسلةٍ عنه ليس نفيًا لوجودها في العربية؛ "
    "كما في `A_COUNT_IN_A_FILE_IS_NOT_A_COUNT_IN_ARABIC`"
)
