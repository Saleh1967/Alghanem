"""اسمُ الشاهد يُشتَقّ من الشجرة ولا يُنقَل عن مُخبِر.

كشفت قراءةٌ خارجيةٌ لهذه الشجرة موضعًا لم تُغلِقه مرحلةٌ قبلها: تقريرٌ عن
المستودع أحال إلى اختبارٍ باسم `test_silent_overwrite_is_refused`، ولا وجودَ
لهذا الاسم في الشجرة؛ والشاهدُ القائم في موضعه اسمُه
`test_a_second_write_over_a_read_state_is_refused_not_absorbed`. وخلاصةُ التقرير
كانت صحيحةً في مضمونها — فالكتابةُ الثانية فوق حالةٍ مقروءة مردودةٌ فعلًا —
فمرّ الاسمُ المُلفَّق تحت خلاصةٍ صادقة::

    ReportIsRight   != WitnessExists
    NameSounds      != NameIsInTheTree
    CitedByAReader  != DerivedFromTheFile

**وهذا جنسٌ لم تُغلِقه المرحلةُ الرابعة عشرة.** تلك ربطت خطوةَ البروتوكول
بكودها، فسألت «أهذه الدالةُ دالةُ هذه الخطوة؟»؛ وهذه تسأل ما قبله: «أهذا الاسمُ
قائمٌ في الملفّ المُحال إليه أصلًا؟». وفارقُ السؤالين فارقُ طبقةٍ لا فارقُ
صياغة: ربطٌ يُحكَم فيه بين مُسجَّلَين، وهذا يُحكَم فيه بين مكتوبٍ ومُشتَقّ.

**والاشتقاق بالقراءة لا بالاستيراد.** تُقرأ أسماءُ الشواهد من نصّ الملفّ
بتحليلٍ نحويّ (`ast`)، فلا يُشترَط أن يُستورَد ملفُّ اختبارٍ ولا أن يُشغَّل
شيءٌ منه لتُعرَف أسماؤه؛ وما لا يُقرأ من الملفّ لا يُقال إنّه فيه.

**والأحوال ثلاثةٌ لا اثنتان.** مُشتَقٌّ من الملفّ المُسمّى، أو غائبٌ عنه وهو
جنسُ الواقعة المُسجَّلة هنا، أو **ملفٌّ لا وجود له في الشجرة** — والثالثةُ
تُفصَل عن الثانية لأن «الاسمُ غيرُ موجودٍ في ملفٍّ غيرِ موجود» حكمٌ على غير
محلِّه، وجمعُهما يُخفي أيَّ الدعويين سقطت.

**وغيابُ الاسم عن ملفٍّ ليس غيابَه عن الشجرة.** يُحكَم هنا على **الاستشهاد**،
وهو زوجُ (اسمٍ، ملفٍّ)، لا على الاسم وحده؛ فاسمٌ قائمٌ في ملفٍّ آخر يبقى
استشهادًا ساقطًا في موضعه، ولا يُقرأ ذلك نفيًا لوجوده في الشجرة
(`ABSENCE_IN_ONE_FILE_IS_NOT_ABSENCE_IN_THE_TREE`).

**وهذه الوحدةُ قارئٌ لا بوّابة.** لا تُعدِّل `assess_freeze` ولا تُغلِّظ شرطَه،
ولا تستوردها `direct_certainty`، ولا تقرؤها بوّابةٌ في `kernel/`؛ واستشهادٌ
تردّه هذه القراءةُ لا يمنع تجميدًا ولا يُسقِط ولادة
(`CITATION_READER_IS_NOT_A_GATE`).

**والمتبقّي مُسمًّى لا مطويّ**: اسمٌ مُشتَقٌّ يقول إنّ شاهدًا بهذا الاسم مكتوبٌ
في ذلك الملفّ، ولا يقول إنّه يُشغَّل، ولا إنّه ينجح، ولا إنّه يفحص ما ادّعاه
التقرير (`A_DERIVED_NAME_IS_NOT_A_PASSING_TEST`).
"""

from __future__ import annotations

import ast
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .binary_outcome import DeeperLayerRecord

__all__ = [
    "ABSENCE_IN_ONE_FILE_IS_NOT_ABSENCE_IN_THE_TREE",
    "A_DERIVED_NAME_IS_NOT_A_PASSING_TEST",
    "CITATION_READER_IS_NOT_A_GATE",
    "FABRICATED_WITNESS_NAME_DISCOVERY",
    "THE_CITED_PAIR_IS_STILL_SUPPLIED_BY_THE_REPORTER",
    "WITNESS_CITATION_NAMED_RESIDUALS",
    "WITNESS_NAME_PREFIX",
    "CitationStanding",
    "WitnessCitation",
    "WitnessCitationError",
    "audit_report_citations",
    "cite_witness",
    "derive_unsupported_citations",
    "derive_witness_names",
    "repository_root_path",
]

WITNESS_NAME_PREFIX: Final[str] = "test"
"""بادئةُ اسم الشاهد كما يلتقطها `pytest`؛ وهي عرفُ الأداة لا اختيارُ هذه الوحدة."""


class WitnessCitationError(ValueError):
    """رُوجِعت القراءةُ بما لا تقوم به: استشهادٌ بلا اسم، أو مسارٌ خارج الشجرة."""


def repository_root_path() -> Path:
    """جذرُ المستودع، مشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


def _resolved_inside_the_tree(relative_path: str, root: Path | None) -> Path:
    """حُلَّ المسارَ داخل الشجرة، وارفُضْ ما خرج عنها بدل قراءته صامتًا."""

    if not isinstance(relative_path, str) or not relative_path.strip():
        raise WitnessCitationError(
            "الاستشهادُ يُسمّي ملفَّه، والاسمُ لا يُترك فارغًا؛ وملفٌّ بلا اسمٍ "
            "لا يُقرأ منه شيء."
        )
    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise WitnessCitationError("جذر المستودع مسارٌ")
    candidate = Path(relative_path)
    if candidate.is_absolute():
        raise WitnessCitationError(
            f"موضعُ الشاهد يُكتَب نسبيًّا إلى جذر المستودع: {relative_path}"
        )
    resolved = (base / candidate).resolve()
    if resolved != base.resolve() and base.resolve() not in resolved.parents:
        raise WitnessCitationError(
            f"موضعٌ خارج شجرة المستودع: {relative_path}؛ وقراءةُ ما خرج عنها "
            "تُخرج أسماءً لا يملك هذا المستودعُ شهادتَها."
        )
    return resolved


def derive_witness_names(
    relative_path: str, root: Path | None = None
) -> tuple[str, ...] | None:
    """أسماءُ الشواهد المكتوبة في ملفٍّ، مُشتَقّةً من نصّه لا منقولةً عن أحد.

    تُقرأ الأسماءُ بتحليلٍ نحويّ لا باستيرادٍ ولا بتشغيل، فلا يُشترَط أن يكون
    الملفُّ قابلًا للاستيراد لتُعرَف أسماؤه، ولا يُنفَّذ منه شيءٌ لأجل القراءة.

    ويُرَدّ `None` — لا مجموعةً خالية — إن لم يكن الملفُّ في الشجرة: خلوٌّ
    مقروءٌ من ملفٍّ قائمٍ غيرُ غيابِ الملفّ، وجمعُهما في قيمةٍ واحدة يُخفي
    أيَّهما وقع.
    """

    resolved = _resolved_inside_the_tree(relative_path, root)
    if not resolved.is_file():
        return None
    try:
        text = resolved.read_text(encoding="utf-8")
    except OSError as error:  # pragma: no cover - نادرٌ ولا يُطوى صامتًا
        raise WitnessCitationError(
            f"تعذّرت قراءةُ ملفِّ الشواهد عند {relative_path}: ملفٌّ لا يُقرأ "
            "يُقرَأ «بلا شواهد» وهو ادّعاءٌ لم يُقرأ الملفُّ لأجله."
        ) from error
    try:
        tree = ast.parse(text, filename=str(resolved))
    except SyntaxError as error:
        raise WitnessCitationError(
            f"ملفُّ الشواهد لا يُحلَّل نحويًّا: {relative_path}؛ وما لا يُحلَّل "
            "لا تُشتقّ منه أسماء."
        ) from error

    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and (
            node.name.startswith(WITNESS_NAME_PREFIX)
        ):
            names.append(node.name)
    return tuple(sorted(set(names)))


class CitationStanding(Enum):
    """أحوالُ الاستشهاد الثلاثة؛ والثالثةُ حكمٌ على الملفّ لا على الاسم."""

    DERIVED_FROM_THE_NAMED_FILE = "derived_from_the_named_file"
    ABSENT_FROM_THE_NAMED_FILE = "absent_from_the_named_file"
    FILE_NOT_IN_THE_TREE = "file_not_in_the_tree"

    @property
    def is_supported_by_the_tree(self) -> bool:
        """أشهدت الشجرةُ لهذا الاستشهاد، أم لم تشهد؟"""

        return self is CitationStanding.DERIVED_FROM_THE_NAMED_FILE


@dataclass(frozen=True)
class WitnessCitation:
    """استشهادٌ واحد: اسمُه، وملفُّه، ورتبتُه، والأسماءُ المُشتَقّة من ملفّه.

    وتُحمَل الأسماءُ المُشتَقّة في الصفّ نفسِه لا تُطرَح بعد الحكم: الحكمُ بلا
    ما اشتُقّ منه يُعاد تصديقُه بالكلام، وهو بعينه العيبُ الذي قام له هذا الصفّ.
    """

    claimed_name: str
    relative_path: str
    standing: CitationStanding
    derived_names: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.claimed_name, str) or not self.claimed_name.strip():
            raise WitnessCitationError("الاستشهادُ يُسمّي شاهدَه، والاسمُ لا يُترك فارغًا.")
        if not isinstance(self.relative_path, str) or not self.relative_path.strip():
            raise WitnessCitationError("الاستشهادُ يُسمّي ملفَّه، والاسمُ غيرُ فارغ.")
        if not isinstance(self.standing, CitationStanding):
            raise WitnessCitationError("رتبةُ الاستشهاد عضوٌ في `CitationStanding`.")
        if not isinstance(self.derived_names, tuple) or not all(
            isinstance(name, str) for name in self.derived_names
        ):
            raise WitnessCitationError("الأسماءُ المُشتَقّة صفٌّ من نصوص.")
        if self.standing is CitationStanding.DERIVED_FROM_THE_NAMED_FILE and (
            self.claimed_name not in self.derived_names
        ):
            raise WitnessCitationError(
                f"رتبةٌ تقول إنّ {self.claimed_name} مُشتَقٌّ من "
                f"{self.relative_path}، وهو ليس في الأسماء المُشتَقّة؛ "
                "وصفٌّ يُخالف ما اشتُقّ منه هو الدعوى بعينها."
            )
        if self.standing is CitationStanding.ABSENT_FROM_THE_NAMED_FILE and (
            self.claimed_name in self.derived_names
        ):
            raise WitnessCitationError(
                f"رتبةٌ تقول إنّ {self.claimed_name} غائبٌ عن "
                f"{self.relative_path}، وهو في الأسماء المُشتَقّة منه."
            )
        if (
            self.standing is CitationStanding.FILE_NOT_IN_THE_TREE
            and self.derived_names
        ):
            raise WitnessCitationError(
                "ملفٌّ غيرُ قائمٍ لا تُشتَقّ منه أسماء؛ فصفٌّ يجمعهما متناقض."
            )


def cite_witness(
    claimed_name: str, relative_path: str, root: Path | None = None
) -> WitnessCitation:
    """احكُم على استشهادٍ واحد باشتقاق أسماء ملفِّه، لا بتصديق ناقله."""

    if not isinstance(claimed_name, str) or not claimed_name.strip():
        raise WitnessCitationError("الاستشهادُ يُسمّي شاهدَه، والاسمُ غيرُ فارغ.")
    derived = derive_witness_names(relative_path, root)
    if derived is None:
        return WitnessCitation(
            claimed_name=claimed_name,
            relative_path=relative_path,
            standing=CitationStanding.FILE_NOT_IN_THE_TREE,
            derived_names=(),
        )
    standing = (
        CitationStanding.DERIVED_FROM_THE_NAMED_FILE
        if claimed_name in derived
        else CitationStanding.ABSENT_FROM_THE_NAMED_FILE
    )
    return WitnessCitation(
        claimed_name=claimed_name,
        relative_path=relative_path,
        standing=standing,
        derived_names=derived,
    )


def audit_report_citations(
    citations: Iterable[tuple[str, str]], root: Path | None = None
) -> tuple[WitnessCitation, ...]:
    """صفٌّ لكلّ استشهادٍ في تقريرٍ بترتيبه، ولا يُختصَر التقريرُ إلى حكمٍ واحد.

    ولا تُرَدّ حصيلةٌ جامعة «مقبول/مردود» عن قصد: جمعُ الصفوف في كلمةٍ واحدة
    يُنشئ حكمًا يُنقَل بدوره، فيعود التقريرُ يُصدَّق بكلمةٍ لا يُقرأ بصفوفه.
    """

    rows: list[WitnessCitation] = []
    for index, citation in enumerate(citations):
        if not isinstance(citation, tuple) or len(citation) != 2:
            raise WitnessCitationError(
                f"الاستشهادُ رقم {index + 1} ليس زوجَ (اسمٍ، ملفٍّ)؛ واسمٌ بلا "
                "ملفٍّ لا يُحكَم فيه."
            )
        name, path = citation
        rows.append(cite_witness(name, path, root))
    return tuple(rows)


def derive_unsupported_citations(
    rows: Iterable[WitnessCitation],
) -> tuple[WitnessCitation, ...]:
    """الاستشهاداتُ التي لم تشهد لها الشجرة، بحالَيها لا بحالٍ واحدة."""

    unsupported: list[WitnessCitation] = []
    for row in rows:
        if not isinstance(row, WitnessCitation):
            raise WitnessCitationError("المقروءُ `WitnessCitation`.")
        if not row.standing.is_supported_by_the_tree:
            unsupported.append(row)
    return tuple(unsupported)


# --- الواقعةُ نفسُها، مُسجَّلةً بآلة قاعدة النتيجتين لا بنثرٍ على هامشها -------

FABRICATED_WITNESS_NAME_DISCOVERY: Final[DeeperLayerRecord] = DeeperLayerRecord(
    subject="الإحالةُ إلى شاهدٍ في هذه الشجرة من تقريرٍ يُكتَب عنها",
    narrowed_unknown=(
        "أُحيل في تقريرٍ عن هذه الشجرة إلى اختبارٍ باسم "
        "`test_silent_overwrite_is_refused` ولا وجودَ له في الشجرة كلِّها، "
        "والشاهدُ القائم في موضعه اسمُه "
        "`test_a_second_write_over_a_read_state_is_refused_not_absorbed`؛ "
        "فموضعُ الخلل ليس الخلاصةَ — وهي صحيحةٌ ومُشتَقّةٌ بالتشغيل — بل "
        "الإحالةَ إلى موضع الدليل، ولم تكن في الشجرة آلةٌ تردّ اسمَ شاهدٍ "
        "مكتوبًا لا مُشتَقًّا"
    ),
    reason=(
        "الخلاصةُ الصحيحة تحمل الاسمَ المُلفَّق معها فلا يُفحَص، والقارئُ "
        "الذي صدّق الخلاصةَ صدّق الإحالةَ تبعًا؛ فضاق المجهولُ بموضعٍ قابلٍ "
        "للقياس هو زوجُ (اسمِ الشاهد، ملفِّه) لا بغيابٍ عامّ للثقة"
    ),
)
"""نتيجةٌ من الفئة الثانية: لم تُغلَق الثقةُ بالتقارير، وضاق موضعُ الخلل باسمه."""


if FABRICATED_WITNESS_NAME_DISCOVERY.mid_figure_classification is not None:
    raise RuntimeError("this discovery opens on no middle figure")  # pragma: no cover


# --- ما تتركه هذه القراءة مفتوحًا، مُسمًّى -----------------------------------

CITATION_READER_IS_NOT_A_GATE: Final[str] = (
    "CITATION_READER_IS_NOT_A_GATE: لا تُعدِّل هذه الوحدةُ `assess_freeze` ولا "
    "تُغلِّظ شرطَه، ولا تستوردها `direct_certainty`، ولا تقرؤها بوّابةٌ في "
    "`kernel/`؛ فاستشهادٌ تردّه هذه القراءةُ لا يمنع تجميدًا ولا يُسقِط ولادة"
)

A_DERIVED_NAME_IS_NOT_A_PASSING_TEST: Final[str] = (
    "A_DERIVED_NAME_IS_NOT_A_PASSING_TEST: اسمٌ مُشتَقٌّ يقول إنّ دالةً بهذا "
    "الاسم مكتوبةٌ في ذلك الملفّ، ولا يقول إنّها تُجمَع ولا إنّها تنجح ولا "
    "إنّها تفحص ما ادّعاه التقرير؛ وهو نظيرُ "
    "`A_BOUND_STEP_IS_NOT_A_CORRECT_MEASUREMENT` في طبقةِ الاستشهاد"
)

ABSENCE_IN_ONE_FILE_IS_NOT_ABSENCE_IN_THE_TREE: Final[str] = (
    "ABSENCE_IN_ONE_FILE_IS_NOT_ABSENCE_IN_THE_TREE: الحكمُ هنا على زوجِ "
    "(اسمٍ، ملفٍّ) لا على الاسم وحده؛ فاسمٌ غائبٌ عن ملفِّه المُسمّى قد يكون "
    "قائمًا في ملفٍّ آخر، ولا يُقرأ ردُّ الاستشهاد نفيًا لوجوده في الشجرة"
)

THE_CITED_PAIR_IS_STILL_SUPPLIED_BY_THE_REPORTER: Final[str] = (
    "THE_CITED_PAIR_IS_STILL_SUPPLIED_BY_THE_REPORTER: الاسمُ والملفُّ "
    "يصلان من كاتب التقرير، فتقريرٌ يسكت عن شاهدٍ يُخالفه لا تكشفه هذه "
    "القراءة؛ وهي تردّ المُلفَّق ولا تستقصي المسكوتَ عنه"
)

WITNESS_CITATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    CITATION_READER_IS_NOT_A_GATE,
    A_DERIVED_NAME_IS_NOT_A_PASSING_TEST,
    ABSENCE_IN_ONE_FILE_IS_NOT_ABSENCE_IN_THE_TREE,
    THE_CITED_PAIR_IS_STILL_SUPPLIED_BY_THE_REPORTER,
)
"""ما بقي مفتوحًا بعد هذه القراءة، مُسمًّى بأسمائه لا مطويًّا في «تمّ»."""
