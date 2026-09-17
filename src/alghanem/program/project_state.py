"""حالُ المشروع مُشتَقّةً من الشجرة، ووثيقةُ الرؤية إسقاطٌ لها لا سجلٌّ ثانٍ.

هذه الوحدةُ تُغلق موضعًا بقي مفتوحًا بعد المراحل الستّ عشرة: صار في الشجرة
دفترٌ يقرأ الدستور، وآخرُ يقرأ الغايات، وثالثٌ يقرأ `README.md`؛ **ولم يكن في
المستودع مدخلٌ يُعرِّف نفسه بقوانينه هو**. فكلُّ تعريفٍ للمشروع كان يُكتَب
نثرًا خارجَه، ويُملأ فراغُه بأرقامٍ لا يُعيد اشتقاقَها شيء::

    WrittenFigure   != DerivedFigure
    DocumentSection != SecondDatabase
    ProjectIdentity != CurrentTally

**واتّجاهُ الاعتماد واحدٌ لا يُعكَس**: الشجرةُ تُشتَقّ منها الحالُ، والحالُ
يُرسَم منها نصُّ الوثيقة. فوثيقةُ `docs/VISION.md` **إسقاطٌ** لهذه الحال، لا
قاعدةَ بياناتٍ ثانيةً تحتاج حراسةً بعد كتابتها. ولو عُكِس الاتّجاه — فكُتبت
الأرقامُ في الوثيقة ثمّ فُحِصت — لبقيت الوثيقةُ أصلًا والشجرةُ شاهدًا عليه،
وذلك قلبٌ للمنزلة لا تنظيمٌ للملفّات.

**والأطروحةُ ليست حالًا، والحالُ ليست أطروحة.** نصُّ الرؤية — لماذا يوجد
المشروع، وما أطروحته، وأين حدودُه — **لا رقمَ فيه**، فيبقى صادقًا يومَ تصير
القوانينُ النافذةُ ثمانين والوحداتُ ثلاثمئة. والأرقامُ كلُّها في كتلةٍ واحدةٍ
مُرسَّمةٍ بين علامتين، تُعاد كتابتُها بالاشتقاق ولا تُحرَّر باليد
(`RENDERED_BLOCK_IS_NOT_EDITED_BY_HAND`).

**والحالةُ المُعلَنة في الدستور مقروءةٌ لا مُتحقَّقٌ منها هنا**
(`A_DECLARED_STATUS_IS_READ_NOT_VERIFIED`): هذه الوحدةُ تقرأ ما **تُعلنه**
الوثيقةُ عن كلّ قانون، ولا تفتح البوّابةَ لتتأكّد أنّ القانونَ نافذٌ فيها. ومن
قرأ «٤٣ نافذًا» برهانًا على الإنفاذ قرأ ما لم يُشتَقّ هنا.

**وأجناسُ الإنفاذ خمسةٌ مغلقة، والمفردةُ مُغطّاةٌ بالكامل عند الاستيراد**: كلُّ
عضوٍ في `DeclaredLawStatus` مُسنَدٌ إلى جنسٍ بعينه في جدولٍ صريح، وحارسٌ عند
الاستيراد يُوقف الوحدةَ إن ظهر عضوٌ جديدٌ بلا إسناد. فالحالةُ الجديدةُ توقف
القراءةَ ولا تنزلق إلى خانةٍ عامّةٍ صامتة.

**وغيابُ المدوّنة يُسمّى ولا يُقرأ نفيًا** (`AN_ABSENT_CORPUS_IS_NOT_A_REFUTED_ONE`):
أنّ بايتات المدوّنة لا تُحَلّ في هذه النسخة يعني أنّ رقمًا لغويًّا لا يُشتَقّ
هنا الآن، لا أنّ دعوًى نُقِضت.

**ولا رقمَ لغويًّا يُصدَّر من هذه الوحدة** (`NO_LINGUISTIC_FIGURE_IS_DERIVED_HERE`):
لا نسبةَ تغطية، ولا انعكاسًا، ولا دقّةَ إعراب. وما وصل من ذلك مُسجَّلٌ في
`REPORTED_UNVERIFIED_FIGURES`، وهذه الوحدةُ **تعدّه ولا تتبنّاه**.

**والعدُّ ليس قدرة** (`A_MODULE_COUNT_IS_NOT_A_CAPABILITY`)، **وعدُّ دوالّ
الاختبار ليس اجتيازَها** (`A_TEST_FUNCTION_COUNT_IS_NOT_A_PASSING_SUITE`):
الاجتيازُ حدثُ تشغيلٍ لا خاصّةُ نصّ، ولا تُشغِّل هذه الوحدةُ اختبارًا.

**خمولٌ سلطويّ**: `DerivedProjectState != BirthVerdict`. لا ولادةَ هنا، ولا
حكمَ ولادة، ولا تجميد، ولا `E0`، ولا استيرادَ من `kernel/`، ولا تقرأ هذه
الوحدةَ وحدةٌ فيه، ولا تُرقّي حالةَ صفٍّ في الدستور ولا تُعدّلها، ولا تُصدِر
بلوغَ غاية.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from ..arabic.masaq_corpus_deposit import masaq_bytes_are_resolvable
from .aims import AIM_RECORDS
from .constitution_ledger import (
    AuditQuestionLedger,
    DeclaredLawStatus,
    LawRowLedger,
    load_constitution_ledger,
)
from .direct_certainty import REPORTED_UNVERIFIED_FIGURES

__all__ = [
    "A_DECLARED_STATUS_IS_READ_NOT_VERIFIED",
    "A_MODULE_COUNT_IS_NOT_A_CAPABILITY",
    "A_TEST_FUNCTION_COUNT_IS_NOT_A_PASSING_SUITE",
    "AN_ABSENT_CORPUS_IS_NOT_A_REFUTED_ONE",
    "NAMED_RESIDUALS",
    "NO_LINGUISTIC_FIGURE_IS_DERIVED_HERE",
    "PROJECT_STATE_AUTHORITY_NOTE",
    "RENDERED_BLOCK_IS_NOT_EDITED_BY_HAND",
    "SOURCE_PACKAGE_RELATIVE_PATH",
    "STATE_BLOCK_BEGIN_MARKER",
    "STATE_BLOCK_END_MARKER",
    "TESTS_RELATIVE_PATH",
    "VISION_RELATIVE_PATH",
    "CorpusReadiness",
    "LawEnforcementGenus",
    "LawStatusCensus",
    "ProjectState",
    "ProjectStateError",
    "SourceTreeCensus",
    "derive_project_state",
    "read_document_state_block",
    "render_state_block",
    "repository_root_path",
    "vision_document_path",
]


class ProjectStateError(ValueError):
    """رفضٌ صريحٌ في اشتقاق حال المشروع أو في رسم كتلتها."""


SOURCE_PACKAGE_RELATIVE_PATH: Final[str] = "src/alghanem"

TESTS_RELATIVE_PATH: Final[str] = "tests"

VISION_RELATIVE_PATH: Final[str] = "docs/VISION.md"

STATE_BLOCK_BEGIN_MARKER: Final[str] = "<!-- بداية الكتلة المُشتَقّة -->"

STATE_BLOCK_END_MARKER: Final[str] = "<!-- نهاية الكتلة المُشتَقّة -->"


PROJECT_STATE_AUTHORITY_NOTE: Final[str] = (
    "اشتقاقٌ وقراءةٌ فقط: لا تُصدِر هذه الوحدةُ ولادةً ولا حكمًا ولا تجميدًا "
    "ولا `E0`، ولا تُرقّي حالةَ صفٍّ في الدستور، ولا تُصدِر بلوغَ غاية، ولا "
    "تقرؤها بوّابةٌ في النواة"
)

A_DECLARED_STATUS_IS_READ_NOT_VERIFIED: Final[str] = (
    "A_DECLARED_STATUS_IS_READ_NOT_VERIFIED"
)

A_MODULE_COUNT_IS_NOT_A_CAPABILITY: Final[str] = "A_MODULE_COUNT_IS_NOT_A_CAPABILITY"

A_TEST_FUNCTION_COUNT_IS_NOT_A_PASSING_SUITE: Final[str] = (
    "A_TEST_FUNCTION_COUNT_IS_NOT_A_PASSING_SUITE"
)

NO_LINGUISTIC_FIGURE_IS_DERIVED_HERE: Final[str] = (
    "NO_LINGUISTIC_FIGURE_IS_DERIVED_HERE"
)

AN_ABSENT_CORPUS_IS_NOT_A_REFUTED_ONE: Final[str] = (
    "AN_ABSENT_CORPUS_IS_NOT_A_REFUTED_ONE"
)

RENDERED_BLOCK_IS_NOT_EDITED_BY_HAND: Final[str] = (
    "RENDERED_BLOCK_IS_NOT_EDITED_BY_HAND"
)


NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        A_DECLARED_STATUS_IS_READ_NOT_VERIFIED: (
            "الحالُ المقروءةُ لكلّ قانونٍ هي ما **تُعلنه** وثيقةُ الدستور عنه، "
            "لا ما تفعله بوّابتُه: لا تفتح هذه الوحدةُ بوّابةً ولا تُشغّل "
            "حارسًا، فعددُ «النافذ» عددُ صفوفٍ أُعلِنت كذلك لا عددُ قوانينَ "
            "أُعيد التأكّدُ من إنفاذها"
        ),
        A_MODULE_COUNT_IS_NOT_A_CAPABILITY: (
            "عددُ وحدات المصدر قياسُ حجمٍ لا قياسُ قدرة: وحدةٌ تُسجِّل نصًّا "
            "ووحدةٌ تحرس بوّابةً تُعَدّان واحدةً واحدة، وجمعُهما لا يُخرِج "
            "رقمًا يقول ماذا يستطيع المستودعُ أن يحكم به"
        ),
        A_TEST_FUNCTION_COUNT_IS_NOT_A_PASSING_SUITE: (
            "دوالُّ الاختبار تُعَدّ من نصّ الشجرة بلا تشغيل؛ والاجتيازُ حدثُ "
            "تشغيلٍ لا خاصّةُ نصّ. فدالّةٌ قائمةٌ تفشل عند التشغيل معدودةٌ هنا "
            "كغيرها، ومن قرأ العددَ نجاحًا قرأ ما لم يُشتَقّ"
        ),
        NO_LINGUISTIC_FIGURE_IS_DERIVED_HERE: (
            "لا تُصدِر هذه الوحدةُ نسبةً لغويّةً واحدة — لا تغطيةً ولا انعكاسًا "
            "ولا دقّةَ إعراب. وما وصل من ذلك معدودٌ في خانة الأرقام غير "
            "القابلة لإعادة الاشتقاق، وعدُّه تسجيلٌ لا تبنٍّ"
        ),
        AN_ABSENT_CORPUS_IS_NOT_A_REFUTED_ONE: (
            "تعذُّرُ حلّ بايتات المدوّنة في هذه النسخة يعني أنّ رقمًا لغويًّا "
            "لا يُشتَقّ هنا الآن، لا أنّ دعوًى نُقِضت؛ والفرقُ بين «لم يُقَس» "
            "و«قِيس فسقط» فرقُ جنسٍ لا فرقُ درجة"
        ),
        RENDERED_BLOCK_IS_NOT_EDITED_BY_HAND: (
            "كتلةُ الأرقام في وثيقة الرؤية مرسومةٌ من هذه الوحدة بين علامتين؛ "
            "وتحريرُها باليد يجعل الوثيقةَ قاعدةَ بياناتٍ ثانيةً تُصدِّق نفسَها، "
            "وهو ما يمنعه شاهدٌ يقابل المرسومَ بالمكتوب حرفًا بحرف"
        ),
    }
)


class LawEnforcementGenus(Enum):
    """جنسُ ما أعلنته الوثيقةُ عن القانون؛ خمسةٌ مغلقةٌ لا سادسَ لها."""

    ENFORCED_AT_A_NAMED_GATE = "نافذٌ_عند_بوّابةٍ_مُسمّاة"
    PARTIALLY_ENFORCED = "نافذٌ_جزئيًّا"
    PROVED_AT_CONTRACT_LEVEL = "مُبرهَنٌ_على_مستوى_العقد"
    DECLARED_DEFERRED = "مُعلَنٌ_مؤجَّل"
    DECLARED_WITHOUT_AN_ENFORCEMENT_CLASS = "مُعلَنٌ_بلا_خانةِ_إنفاذ"


_GENUS_BY_STATUS: Final[Mapping[DeclaredLawStatus, LawEnforcementGenus]] = (
    MappingProxyType(
        {
            DeclaredLawStatus.PARTIALLY_ENFORCED: (
                LawEnforcementGenus.PARTIALLY_ENFORCED
            ),
            DeclaredLawStatus.PROVED_AT_CONTRACT_LEVEL: (
                LawEnforcementGenus.PROVED_AT_CONTRACT_LEVEL
            ),
            DeclaredLawStatus.PROVED_WITHIN_PROVIDER_SCOPE: (
                LawEnforcementGenus.PROVED_AT_CONTRACT_LEVEL
            ),
            DeclaredLawStatus.DECLARED_DEFERRED: LawEnforcementGenus.DECLARED_DEFERRED,
            DeclaredLawStatus.DECLARED_DEFERRED_CONTRACT_ONLY: (
                LawEnforcementGenus.DECLARED_DEFERRED
            ),
            DeclaredLawStatus.CONSTITUTIONAL_REQUIREMENT: (
                LawEnforcementGenus.DECLARED_WITHOUT_AN_ENFORCEMENT_CLASS
            ),
            DeclaredLawStatus.DECLARED_LAW_ONLY: (
                LawEnforcementGenus.DECLARED_WITHOUT_AN_ENFORCEMENT_CLASS
            ),
            DeclaredLawStatus.DOCUMENTED_OPEN_QUESTION: (
                LawEnforcementGenus.DECLARED_WITHOUT_AN_ENFORCEMENT_CLASS
            ),
            DeclaredLawStatus.DOCUMENTED_CLASSIFICATION_ONLY: (
                LawEnforcementGenus.DECLARED_WITHOUT_AN_ENFORCEMENT_CLASS
            ),
        }
    )
)


def _genus_of(status: DeclaredLawStatus) -> LawEnforcementGenus:
    """جنسُ الحالة المُعلَنة؛ وكلُّ حالةٍ تبدأ بـ`ENFORCED_` نافذةٌ بوّابيًّا."""

    if status.name.startswith("ENFORCED"):
        return LawEnforcementGenus.ENFORCED_AT_A_NAMED_GATE
    genus = _GENUS_BY_STATUS.get(status)
    if genus is None:
        raise ProjectStateError(
            f"حالةٌ مُعلَنةٌ بلا جنسٍ مُسنَد: {status.name} — الحالةُ الجديدةُ "
            "توقف القراءةَ ولا تنزلق إلى خانةٍ عامّةٍ صامتة"
        )
    return genus


_UNASSIGNED_STATUSES: Final[tuple[str, ...]] = tuple(
    status.name
    for status in DeclaredLawStatus
    if not status.name.startswith("ENFORCED") and status not in _GENUS_BY_STATUS
)

if _UNASSIGNED_STATUSES:  # حارسٌ عند الاستيراد، لا فحصٌ يُؤجَّل إلى الاستدعاء
    raise ProjectStateError(
        "مفردةُ الحالات المُعلَنة غيرُ مُغطّاةٍ بالأجناس: "
        f"{'، '.join(_UNASSIGNED_STATUSES)}"
    )


class CorpusReadiness(Enum):
    """حالُ المدوّنة في هذه النسخة؛ ثنائيةٌ مُصرَّحٌ بطرفيها."""

    BYTES_RESOLVE_IN_THIS_CHECKOUT = "بايتاتُها_تُحَلّ_في_هذه_النسخة"
    BYTES_DO_NOT_RESOLVE_IN_THIS_CHECKOUT = "بايتاتُها_لا_تُحَلّ_في_هذه_النسخة"


@dataclass(frozen=True, slots=True)
class LawStatusCensus:
    """إحصاءُ صفوف الدستور بأجناس الإنفاذ؛ تعدادُه خاصّيةٌ لا حقل."""

    ledger: LawRowLedger

    def __post_init__(self) -> None:
        if not isinstance(self.ledger, LawRowLedger):
            raise ProjectStateError("إحصاءُ القوانين يُبنى على دفتر صفوفٍ مقروء")

    @property
    def law_count(self) -> int:
        """عددُ صفوف الدستور المقروءة."""

        return self.ledger.row_count

    @property
    def counts_by_genus(self) -> Mapping[LawEnforcementGenus, int]:
        """تعدادُ الصفوف بجنس الإنفاذ، وكلُّ جنسٍ حاضرٌ ولو بصفر."""

        counts = {genus: 0 for genus in LawEnforcementGenus}
        for status, count in self.ledger.status_counts.items():
            counts[_genus_of(status)] += count
        return MappingProxyType(counts)

    @property
    def enforcement_surface_count(self) -> int:
        """عددُ تسميات الإنفاذ المتمايزة الحاضرة فعلًا، لا عددُ أعضاء المفردة."""

        return sum(
            1
            for status, count in self.ledger.status_counts.items()
            if count > 0 and status.name.startswith("ENFORCED")
        )


@dataclass(frozen=True, slots=True)
class SourceTreeCensus:
    """عدُّ وحدات المصدر وملفّات الشواهد ودوالّ الاختبار، من النصّ بلا تشغيل."""

    source_modules: tuple[str, ...]
    test_modules: tuple[str, ...]
    test_function_count: int

    def __post_init__(self) -> None:
        for paths, label in (
            (self.source_modules, "وحداتُ المصدر"),
            (self.test_modules, "ملفّاتُ الشواهد"),
        ):
            if not isinstance(paths, tuple) or not paths:
                raise ProjectStateError(f"{label} تعدادٌ غيرُ فارغ")
            if len(set(paths)) != len(paths):
                raise ProjectStateError(f"{label} فيها مسارٌ مكرّر، والتكرار يُفسد العدّ")
            if tuple(sorted(paths)) != paths:
                raise ProjectStateError(f"{label} مرتّبةٌ ترتيبًا واحدًا لا يتغيّر")
        if isinstance(self.test_function_count, bool) or not isinstance(
            self.test_function_count, int
        ):
            raise ProjectStateError("عددُ دوالّ الاختبار عددٌ صحيح")
        if self.test_function_count < len(self.test_modules):
            raise ProjectStateError(
                "ملفُّ شاهدٍ بلا دالّةِ اختبارٍ واحدة يُقرأ شاهدًا وليس كذلك"
            )

    @property
    def source_module_count(self) -> int:
        """عددُ وحدات المصدر المقروءة من الشجرة."""

        return len(self.source_modules)

    @property
    def test_module_count(self) -> int:
        """عددُ ملفّات الشواهد المقروءة من الشجرة."""

        return len(self.test_modules)


@dataclass(frozen=True, slots=True)
class ProjectState:
    """حالُ المشروع مجموعةً: قوانينُه، وأسئلتُه، وغاياتُه، وحدودُه المقيسة."""

    laws: LawStatusCensus
    audit_questions: AuditQuestionLedger
    tree: SourceTreeCensus
    declared_aim_count: int
    unverified_figure_count: int
    corpus_readiness: CorpusReadiness

    def __post_init__(self) -> None:
        if not isinstance(self.laws, LawStatusCensus):
            raise ProjectStateError("حالُ المشروع تحمل إحصاءَ قوانينَ مقروءًا")
        if not isinstance(self.audit_questions, AuditQuestionLedger):
            raise ProjectStateError("حالُ المشروع تحمل دفترَ أسئلةٍ مقروءًا")
        if not isinstance(self.tree, SourceTreeCensus):
            raise ProjectStateError("حالُ المشروع تحمل إحصاءَ شجرةٍ مقروءًا")
        for value, label in (
            (self.declared_aim_count, "عددُ الغايات المُعلَنة"),
            (self.unverified_figure_count, "عددُ الأرقام غير القابلة للاشتقاق"),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ProjectStateError(f"{label} عددٌ صحيحٌ غيرُ سالب")
        if not isinstance(self.corpus_readiness, CorpusReadiness):
            raise ProjectStateError("حالُ المدوّنة عضوٌ في مفردتها المغلقة")

    @property
    def no_linguistic_figure_is_derived(self) -> bool:
        """`True` دائمًا: لا تُصدِر هذه الحالُ نسبةً لغويّةً واحدة."""

        return True


def repository_root_path() -> Path:
    """جذرُ شجرة المستودع، مشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


def vision_document_path(root: Path | None = None) -> Path:
    """موضعُ وثيقة الرؤية، مشتقًّا من الجذر لا مكتوبًا مطلقًا."""

    return (root or repository_root_path()) / VISION_RELATIVE_PATH


def _relative_python_files(directory: Path, root: Path) -> tuple[str, ...]:
    return tuple(
        sorted(
            path.relative_to(root).as_posix()
            for path in directory.rglob("*.py")
            if path.is_file()
        )
    )


def _count_test_functions(paths: tuple[str, ...], root: Path) -> int:
    total = 0
    for relative in paths:
        tree = ast.parse((root / relative).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(
                node, ast.FunctionDef | ast.AsyncFunctionDef
            ) and node.name.startswith("test_"):
                total += 1
    return total


def _read_source_tree_census(root: Path) -> SourceTreeCensus:
    source_directory = root / SOURCE_PACKAGE_RELATIVE_PATH
    tests_directory = root / TESTS_RELATIVE_PATH
    for directory, label in (
        (source_directory, SOURCE_PACKAGE_RELATIVE_PATH),
        (tests_directory, TESTS_RELATIVE_PATH),
    ):
        if not directory.is_dir():
            raise ProjectStateError(
                f"موضعٌ غيرُ قائمٍ في الشجرة: {label} — والاشتقاقُ يقف ولا يُقدَّر"
            )
    test_modules = tuple(
        relative
        for relative in _relative_python_files(tests_directory, root)
        if Path(relative).name.startswith("test_")
    )
    return SourceTreeCensus(
        source_modules=_relative_python_files(source_directory, root),
        test_modules=test_modules,
        test_function_count=_count_test_functions(test_modules, root),
    )


def derive_project_state(root: Path | None = None) -> ProjectState:
    """اشتقّ حالَ المشروع من الشجرة الآن؛ ولا يُقرأ منها رقمٌ مكتوبٌ في وثيقة."""

    resolved_root = root or repository_root_path()
    census = _read_source_tree_census(resolved_root)
    constitution_path = resolved_root / "docs" / "CONSTITUTION.md"
    if not constitution_path.is_file():
        raise ProjectStateError(
            "وثيقةُ الدستور غيرُ قائمةٍ في هذه الشجرة؛ والاشتقاقُ يقف ولا يُقدَّر"
        )
    ledger = load_constitution_ledger(constitution_path)
    readiness = (
        CorpusReadiness.BYTES_RESOLVE_IN_THIS_CHECKOUT
        if masaq_bytes_are_resolvable()
        else CorpusReadiness.BYTES_DO_NOT_RESOLVE_IN_THIS_CHECKOUT
    )
    return ProjectState(
        laws=LawStatusCensus(ledger=ledger.laws),
        audit_questions=ledger.audit_questions,
        tree=census,
        declared_aim_count=len(AIM_RECORDS),
        unverified_figure_count=len(REPORTED_UNVERIFIED_FIGURES),
        corpus_readiness=readiness,
    )


_GENUS_LABELS: Final[Mapping[LawEnforcementGenus, str]] = MappingProxyType(
    {
        LawEnforcementGenus.ENFORCED_AT_A_NAMED_GATE: "نافذٌ عند بوّابةٍ مُسمّاة",
        LawEnforcementGenus.PARTIALLY_ENFORCED: "نافذٌ جزئيًّا",
        LawEnforcementGenus.PROVED_AT_CONTRACT_LEVEL: "مُبرهَنٌ على مستوى العقد",
        LawEnforcementGenus.DECLARED_DEFERRED: "مُعلَنٌ مؤجَّلٌ بالاسم",
        LawEnforcementGenus.DECLARED_WITHOUT_AN_ENFORCEMENT_CLASS: (
            "مُعلَنٌ بلا خانةِ إنفاذ"
        ),
    }
)


def render_state_block(state: ProjectState) -> str:
    """ارسم كتلةَ الحال بين علامتيها؛ والرسمُ وحدَه مصدرُ ما يُكتَب في الوثيقة."""

    if not isinstance(state, ProjectState):
        raise ProjectStateError("الكتلةُ تُرسَم من حالٍ مُشتَقّةٍ لا من نصّ")
    counts = state.laws.counts_by_genus
    lines = [
        STATE_BLOCK_BEGIN_MARKER,
        "",
        "> هذه الكتلةُ **مرسومةٌ آليًّا** من `src/alghanem/program/project_state.py`،",
        "> ولا تُحرَّر باليد؛ ويقابلها شاهدٌ حرفًا بحرف.",
        "",
        "| المقروء | العدد |",
        "| --- | --- |",
        f"| صفوفُ الدستور المقروءة | {state.laws.law_count} |",
    ]
    lines.extend(
        f"| — منها {_GENUS_LABELS[genus]} | {counts[genus]} |"
        for genus in LawEnforcementGenus
    )
    lines.extend(
        [
            "| تسمياتُ الإنفاذ المتمايزة الحاضرة | "
            f"{state.laws.enforcement_surface_count} |",
            f"| أسئلةُ التدقيق المفتوحة | {state.audit_questions.open_count} |",
            f"| أسئلةُ التدقيق المُغلَقة | {state.audit_questions.resolved_count} |",
            f"| الغاياتُ المُعلَنة | {state.declared_aim_count} |",
            "| الأرقامُ الواردةُ غيرُ القابلة لإعادة الاشتقاق | "
            f"{state.unverified_figure_count} |",
            f"| وحداتُ المصدر | {state.tree.source_module_count} |",
            f"| ملفّاتُ الشواهد | {state.tree.test_module_count} |",
            f"| دوالُّ الاختبار المعدودةُ نصًّا | {state.tree.test_function_count} |",
            f"| حالُ المدوّنة | {state.corpus_readiness.value} |",
            "",
            "**حدودُ هذه الكتلة، مُسمّاةً لا مطويّة:** الحالُ المقروءةُ لكلّ "
            "قانونٍ هي ما تُعلنه الوثيقةُ عنه لا ما تفعله بوّابتُه "
            f"(`{A_DECLARED_STATUS_IS_READ_NOT_VERIFIED}`)؛ ودوالُّ الاختبار "
            "معدودةٌ من النصّ بلا تشغيل، والعددُ ليس اجتيازًا "
            f"(`{A_TEST_FUNCTION_COUNT_IS_NOT_A_PASSING_SUITE}`)؛ وعددُ "
            "الوحدات قياسُ حجمٍ لا قياسُ قدرة "
            f"(`{A_MODULE_COUNT_IS_NOT_A_CAPABILITY}`)؛ ولا نسبةَ لغويّةً "
            f"واحدةً في هذه الكتلة (`{NO_LINGUISTIC_FIGURE_IS_DERIVED_HERE}`)؛ "
            "وتعذُّرُ حلّ بايتات المدوّنة ليس نقضًا لدعوى "
            f"(`{AN_ABSENT_CORPUS_IS_NOT_A_REFUTED_ONE}`).",
            "",
            STATE_BLOCK_END_MARKER,
        ]
    )
    return "\n".join(lines)


def read_document_state_block(document_text: str) -> str:
    """اقرأ الكتلةَ المرسومةَ من نصّ الوثيقة؛ وعلامةٌ ناقصةٌ أو مكرّرةٌ رفضٌ مُسمّى."""

    if not isinstance(document_text, str) or not document_text.strip():
        raise ProjectStateError("نصُّ الوثيقة نصٌّ غيرُ فارغ")
    for marker in (STATE_BLOCK_BEGIN_MARKER, STATE_BLOCK_END_MARKER):
        occurrences = document_text.count(marker)
        if occurrences != 1:
            raise ProjectStateError(
                f"علامةُ الكتلة «{marker}» واردةٌ {occurrences} مرّة؛ وكتلةٌ بلا "
                "حدٍّ واحدٍ لا تُقابَل بالمرسوم"
            )
    start = document_text.index(STATE_BLOCK_BEGIN_MARKER)
    end = document_text.index(STATE_BLOCK_END_MARKER) + len(STATE_BLOCK_END_MARKER)
    if end <= start:
        raise ProjectStateError("علامةُ النهاية قبل علامةِ البداية؛ ولا كتلةَ بينهما")
    return document_text[start:end]
