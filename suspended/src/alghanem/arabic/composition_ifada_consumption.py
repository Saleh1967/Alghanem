"""`G0.IFADA-USE`: ما يستهلكه مسارُ الإفادة فعلًا، مُشتقًّا من الشيفرة لا مُدَّعًى.

وجودُ جبرٍ في المستودع شيء، واستهلاكُ مسار الإفادة له شيءٌ آخر
(`AnAlgebraExistsIsNotAnAlgebraIsUsed`). وهذه الوحدة تقطع بينهما بقياسٍ واحد:
تُشتَقّ **إغلاقةُ الاستيراد** لوحدة `composition_ifada_path` من شجرة الصيغة
المجرّدة، ثمّ يُسأَل عن كلِّ جبرٍ مرشَّحٍ: أهو داخلَ الإغلاقة أم خارجَها؟

والخارجُ يُسجَّل **بقيّةً مُسمّاةً** لا رفضًا. فالبقيّةُ تقول «لم يُقَس هذا
الاتّصال بعد»، والرفضُ يقول «لا يكون»؛ وبينهما فرقٌ لا يُطوى
(`AnAbsentEdgeIsAResidualNotARefusal`).

ولا تُصدِر هذه الوحدةُ حكمًا على قيمة جبرٍ ولا على صحّته، ولا تمنع وصلَه
مستقبلًا. إنّما تمنع أن يُقال «مسارُ الإفادة يمرّ بالجبر الأوسع» بلا حافّةٍ
مقروءةٍ في الشيفرة.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "CANDIDATE_ALGEBRAS",
    "COMPOSITION_IFADA_CONSUMPTION_NAMED_LAWS",
    "THE_PATH_ENTRY_MODULE",
    "CandidateAlgebra",
    "ConsumptionCensus",
    "ConsumptionRow",
    "IfadaConsumptionError",
    "derive_consumption_census",
    "derive_import_closure",
    "render_consumption_census",
]


class IfadaConsumptionError(ValueError):
    """خطأُ قياسِ الاستهلاك؛ ويُرفَع عند تعذُّر القراءة لا عند غياب حافّة."""


THE_PATH_ENTRY_MODULE: Final[str] = "alghanem.arabic.composition_ifada_path"
"""الوحدةُ التي تحمل `run_bytes`؛ وهي مبدأُ الإغلاقة لا واحدةٌ من أعضائها فقط."""


COMPOSITION_IFADA_CONSUMPTION_NAMED_LAWS: Final[dict[str, str]] = {
    "AnAlgebraExistsIsNotAnAlgebraIsUsed": (
        "AnAlgebraExistsIsNotAnAlgebraIsUsed: وجودُ بنيةٍ جبريّةٍ في المستودع "
        "لا يُثبِت أنّ مسار الإفادة يستهلكها. والفاصلُ حافّةُ استيرادٍ مقروءةٌ "
        "في الشيفرة، تُشتَقّ ولا تُدَّعى؛ فمن استدلّ بوجود الوحدة على استعمالها "
        "فقد عبَر انتقالًا لم يُقَس"
    ),
    "AnAbsentEdgeIsAResidualNotARefusal": (
        "AnAbsentEdgeIsAResidualNotARefusal: جبرٌ خارجَ الإغلاقة بقيّةٌ مُسمّاةٌ "
        "لا رفض. فهي تقول «لم يُقَس هذا الاتّصال» ولا تقول «لا يكون»، ولا تمنع "
        "وصلًا لاحقًا بانتقالٍ مرخّصٍ محفوظِ الهويّة"
    ),
    "TheClosureIsDerivedFromTheSourceNotDeclared": (
        "TheClosureIsDerivedFromTheSourceNotDeclared: الإغلاقةُ تُقرأ من شجرة "
        "الصيغة المجرّدة للوحدات نفسِها، فلا تُكتَب قائمةٌ يدويّةٌ تُصدَّق. وكلُّ "
        "عددٍ في هذا الإحصاء مخرجُ قياسٍ لا رقمٌ مُصرَّح"
    ),
    "EveryDerivedEdgeMustResolveToAFile": (
        "EveryDerivedEdgeMustResolveToAFile: كلُّ حافّةٍ مُشتَقّةٍ تُسمّي وحدةً "
        "قائمةً على القرص. فاسمٌ لا يُحَلّ إلى ملفٍ خللٌ في المطابقة لا غيابُ "
        "اتّصال، ويُكشَف بتدقيقٍ يمرّ على الحوافّ كلِّها قبل أن يُقرأ الإحصاء"
    ),
    "AnImportIsNotACall": (
        "AnImportIsNotACall: استيرادُ اسمٍ ليس استدعاءَه. فقد يُستورَد ما لا "
        "يُستعمَل، فيُعَدّ الاستيرادُ وحدَه اعتمادًا وهو جوارٌ ساكن؛ ولذلك "
        "يُفصَل عدُّ المستورَد عن عدِّ المُستدعى، ولا يُطوى أحدُهما في الآخر"
    ),
    "ACallIsNotAnOutput": (
        "ACallIsNotAnOutput: استدعاءُ دالّةٍ ليس بلوغَ مخرجها سجلَّ السَّوق. "
        "فقد يُستدعى ما يُتحقَّق به أو يُسجَّل به ثمّ لا يدخل في المخرج؛ "
        "وبلوغُ المخرج يُقاس على حِدة أو يُسمّى بقيّة"
    ),
    "TheCallTraceIsStaticNotDynamic": (
        "TheCallTraceIsStaticNotDynamic: تتبُّعُ الاستدعاء يقرأ شجرةَ الصيغة "
        "المجرّدة، فلا يرى استيرادًا يقع زمنَ التشغيل ولا إرسالًا غيرَ مباشرٍ "
        "عبر متغيّرٍ أو جدول. وهذه بقيّةٌ مُسمّاةٌ لازمةٌ للمقياس لا عيبٌ عارض"
    ),
    "ACountIsNotAChain": (
        "ACountIsNotAChain: اجتماعُ أعدادٍ في مستودعٍ واحدٍ لا يجعلها سلسلةَ "
        "انتقالٍ مغلقة. فيلزم لكلِّ حافّةٍ مصدرٌ ومقصدٌ وهويّةٌ محفوظةٌ وبقيّةٌ "
        "عند فجوتها؛ وما لم تُقرَأ الحافّةُ فالعددان جاران لا موصولان"
    ),
}
"""القيودُ المُسمّاةُ التي تُجمّدها هذه الوحدة؛ كلُّ نصٍّ يفتتح باسم قانونه."""


@dataclass(frozen=True, slots=True)
class CandidateAlgebra:
    """جبرٌ مرشَّحٌ للاتّصال بمسار الإفادة، باسمه ووحدته ووصفِ ما يقدّمه."""

    name: str
    module_prefix: str
    what_it_offers: str

    def __post_init__(self) -> None:
        for field_name in ("name", "module_prefix", "what_it_offers"):
            if not str(getattr(self, field_name)).strip():
                raise IfadaConsumptionError(f"{field_name} نصٌّ غيرُ فارغ.")


CANDIDATE_ALGEBRAS: Final[tuple[CandidateAlgebra, ...]] = (
    CandidateAlgebra(
        name="العقدةُ الليفيّةُ المحايدة",
        module_prefix="alghanem.prior_fiber",
        what_it_offers="اثنتا عشرة خانةً مُصرَّحةً حالُها `UNASSIGNED` ابتداءً",
    ),
    CandidateAlgebra(
        name="الليفُ المرصودُ للحامل والحالة",
        module_prefix="alghanem.arabic.carrier_state_observed_fiber",
        what_it_offers="جداولُ وقوعٍ مرصودةٌ وشواهدُ نقضٍ للجداء",
    ),
    CandidateAlgebra(
        name="عقودُ الألياف",
        module_prefix="alghanem.arabic.fiber_contracts",
        what_it_offers="عقودُ ليفٍ مُصرَّحةٌ للمدلول وما يجاوره",
    ),
    CandidateAlgebra(
        name="النموذجُ العدميُّ لليف الحامل",
        module_prefix="alghanem.arabic.carrier_fiber_null_model",
        what_it_offers="نموذجٌ عدميٌّ يُقابَل به المرصود",
    ),
    CandidateAlgebra(
        name="فرضيّةُ `FLT-1` وعددُها المتنبَّأُ به",
        module_prefix="alghanem.arabic.flt1",
        what_it_offers="حاصلُ قسمةٍ يُشتَقّ ثمّ يُختبَر عددُه، و`28` تنبّؤٌ يُكذَّب",
    ),
    CandidateAlgebra(
        name="جبرُ `zero-one` البنيويّ",
        module_prefix="alghanem.structural_dal",
        what_it_offers="خانتان وصعودٌ محفوظُ المِرساة، وستّ عشرة فرضيّةَ تقسيم",
    ),
    CandidateAlgebra(
        name="جسرُ البتّين",
        module_prefix="alghanem.structural_bridge",
        what_it_offers="وصلُ وقوعَي بتٍّ حقيقيّين بخانتين بنيويّتين",
    ),
)
"""الجبورُ المرشَّحةُ التي يُسأَل عن استهلاك مسار الإفادة لها، واحدًا واحدًا."""


def _source_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _module_file(module: str) -> Path | None:
    root = _source_root()
    flat = root.joinpath(*module.split(".")).with_suffix(".py")
    if flat.is_file():
        return flat
    package = root.joinpath(*module.split(".")) / "__init__.py"
    return package if package.is_file() else None


def _parse(path: Path, module: str) -> ast.Module:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as error:  # pragma: no cover - حارسُ قراءة
        raise IfadaConsumptionError(f"تعذّرت قراءةُ {module}: {error}") from error


def _containing_package(path: Path, module: str) -> str:
    """الحزمةُ التي يُحَلّ إليها الاستيرادُ النسبيّ؛ و`__init__` حزمتُه نفسُها.

    وهذا موضعُ خللٍ مقصودِ التصحيح: مَن حَلَّ نسبيَّ `__init__.py` إلى حزمته
    الأمّ أخرج أسماءَ وحداتٍ لا وجودَ لها، فأسقط حوافَّ إعادة التصدير كلَّها
    صامتًا (`EveryDerivedEdgeMustResolveToAFile`).
    """

    return module if path.name == "__init__.py" else module.rsplit(".", 1)[0]


def _imports_of(path: Path, module: str) -> frozenset[str]:
    """اقرأ وحداتِ `alghanem` المستورَدةَ في ملفٍ واحد، والنسبيُّ يُحَلّ لمطلقه.

    و`from حزمة import وحدة` حافّةٌ إلى الوحدة لا إلى حزمتها وحدَها؛ فمن عدَّها
    حافّةً واحدةً أسقط المقصودَ وأبقى وسيطَه.
    """

    tree = _parse(path, module)
    found: set[str] = set()
    package = _containing_package(path, module)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(
                alias.name
                for alias in node.names
                if alias.name.split(".")[0] == "alghanem"
            )
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package
                for _ in range(node.level - 1):
                    base = base.rsplit(".", 1)[0]
                target = f"{base}.{node.module}" if node.module else base
            elif node.module and node.module.split(".")[0] == "alghanem":
                target = node.module
            else:
                continue
            found.add(target)
            found.update(
                candidate
                for alias in node.names
                if _module_file(candidate := f"{target}.{alias.name}") is not None
            )
    return frozenset(found)


@lru_cache(maxsize=1)
def derive_import_closure() -> tuple[str, ...]:
    """اشتقّ إغلاقةَ استيراد مسار الإفادة كلَّها، مرتّبةً، من الشيفرة نفسِها."""

    entry = _module_file(THE_PATH_ENTRY_MODULE)
    if entry is None:  # pragma: no cover - حارسُ بناء
        raise IfadaConsumptionError("وحدةُ مبدأ المسار غيرُ موجودة.")
    seen: set[str] = set()
    pending = [THE_PATH_ENTRY_MODULE]
    while pending:
        module = pending.pop()
        if module in seen:
            continue
        seen.add(module)
        path = _module_file(module)
        if path is None:
            continue
        pending.extend(name for name in _imports_of(path, module) if name not in seen)
    return tuple(sorted(seen))


def _bound_names_from(module_path: Path, module: str, prefix: str) -> set[str]:
    """الأسماءُ التي تُربَط في هذه الوحدة من جبرٍ بعينه، لا أسماءُ وحداته."""

    package = _containing_package(module_path, module)
    bound: set[str] = set()
    for node in ast.walk(_parse(module_path, module)):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level:
            base = package
            for _ in range(node.level - 1):
                base = base.rsplit(".", 1)[0]
            target = f"{base}.{node.module}" if node.module else base
        elif node.module:
            target = node.module
        else:  # pragma: no cover - حارسُ قراءة
            continue
        if target == prefix or target.startswith(f"{prefix}."):
            bound.update(alias.asname or alias.name for alias in node.names)
    return bound


def _called_names(module_path: Path, module: str) -> set[str]:
    """الأسماءُ الواقعةُ في موضع الاستدعاء؛ والمنقوطُ يُرَدّ إلى جذره."""

    called: set[str] = set()
    for node in ast.walk(_parse(module_path, module)):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        while isinstance(func, ast.Attribute):
            func = func.value
        if isinstance(func, ast.Name):
            called.add(func.id)
    return called


@dataclass(frozen=True, slots=True)
class ConsumptionRow:
    """صفُّ جبرٍ واحد: أهو داخلَ الإغلاقة، وبأيِّ وحداتٍ إن كان؟"""

    algebra: CandidateAlgebra
    reached_modules: tuple[str, ...]
    bound_names: tuple[str, ...] = ()
    called_names: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.algebra) is not CandidateAlgebra:
            raise IfadaConsumptionError("صفُّ الإحصاء يحمل جبرًا مرشَّحًا من نوعه.")
        if not isinstance(self.reached_modules, tuple):
            raise IfadaConsumptionError("الوحداتُ المبلوغةُ صفٌّ مرتَّب.")
        if tuple(sorted(self.reached_modules)) != self.reached_modules:
            raise IfadaConsumptionError("الوحداتُ المبلوغةُ مرتَّبةٌ ترتيبًا واحدًا.")
        for field_name in ("bound_names", "called_names"):
            names = getattr(self, field_name)
            if not isinstance(names, tuple):
                raise IfadaConsumptionError(f"{field_name} صفٌّ مرتَّب.")
            if tuple(sorted(names)) != names:
                raise IfadaConsumptionError(f"{field_name} مرتَّبٌ ترتيبًا واحدًا.")
        if not set(self.called_names) <= set(self.bound_names):
            raise IfadaConsumptionError(
                "المُستدعى من هذا الجبر جزءٌ من المربوط منه؛ و"
                + COMPOSITION_IFADA_CONSUMPTION_NAMED_LAWS["AnImportIsNotACall"]
            )
        if self.bound_names and not self.reached_modules:
            raise IfadaConsumptionError("أسماءٌ مربوطةٌ بلا وحدةٍ مبلوغةٍ تناقض.")

    @property
    def is_consumed(self) -> bool:
        """أيستهلك مسارُ الإفادة هذا الجبرَ بحافّةِ استيرادٍ مقروءة؟"""

        return bool(self.reached_modules)

    @property
    def is_called(self) -> bool:
        """أيُستدعى من هذا الجبر اسمٌ واحدٌ؟ فالاستيرادُ وحدَه جوارٌ ساكن."""

        return bool(self.called_names)

    @property
    def imported_but_unused(self) -> tuple[str, ...]:
        """ما استُورِد من هذا الجبر ولم يقع في موضع استدعاء."""

        return tuple(
            name for name in self.bound_names if name not in set(self.called_names)
        )

    @property
    def residual(self) -> str | None:
        """البقيّةُ المُسمّاةُ عند الفجوة، و`None` لمن بُلِغ فلا فجوةَ فيه."""

        if self.is_consumed:
            return None
        return (
            f"{self.algebra.name}: موجودٌ في المستودع ويقدّم "
            f"{self.algebra.what_it_offers}؛ ولا حافّةَ استيرادٍ تصله بمسار "
            "الإفادة، فاتّصالُه لم يُقَس بعد."
        )


@dataclass(frozen=True, slots=True)
class ConsumptionCensus:
    """إحصاءُ ما يستهلكه مسارُ الإفادة؛ كلُّ عددٍ فيه مُشتَقٌّ من صفوفه."""

    closure: tuple[str, ...]
    rows: tuple[ConsumptionRow, ...]

    def __post_init__(self) -> None:
        if not self.closure:
            raise IfadaConsumptionError("إغلاقةٌ فارغةٌ ليست قياسًا.")
        if THE_PATH_ENTRY_MODULE not in self.closure:
            raise IfadaConsumptionError("الإغلاقةُ تشمل وحدةَ مبدئها.")
        if len(self.rows) != len(CANDIDATE_ALGEBRAS):
            raise IfadaConsumptionError("لكلِّ جبرٍ مرشَّحٍ صفٌّ واحدٌ لا يُطوى.")

    @property
    def closure_size(self) -> int:
        """عددُ وحدات الإغلاقة كلِّها."""

        return len(self.closure)

    @property
    def consumed(self) -> tuple[ConsumptionRow, ...]:
        """الجبورُ المستهلَكةُ بحافّةٍ مقروءة."""

        return tuple(row for row in self.rows if row.is_consumed)

    @property
    def residuals(self) -> tuple[str, ...]:
        """البقايا المُسمّاةُ عند كلِّ فجوة، بترتيب صفوفها."""

        return tuple(row.residual for row in self.rows if row.residual is not None)

    @property
    def any_wider_algebra_is_consumed(self) -> bool:
        """أيستهلك المسارُ جبرًا واحدًا من المرشَّحين؟ والجوابُ مقيسٌ لا مُصرَّح."""

        return bool(self.consumed)

    @property
    def called(self) -> tuple[ConsumptionRow, ...]:
        """الجبورُ التي استُدعي منها اسمٌ واحدٌ على الأقلّ داخل الإغلاقة."""

        return tuple(row for row in self.rows if row.is_called)

    @property
    def any_wider_algebra_is_called(self) -> bool:
        """أيُستدعى من جبرٍ أوسعَ شيءٌ؟ وهو سؤالٌ وراء الاستيراد لا عينُه."""

        return bool(self.called)

    @property
    def output_reach_is_measured(self) -> bool:
        """أيمكن أصلًا قياسُ بلوغ المخرج؟ ولا مخرجَ يُتتبَّع حيث لا استدعاء."""

        return self.any_wider_algebra_is_called

    @property
    def what_the_call_trace_cannot_see(self) -> str:
        """البقيّةُ اللازمةُ للمقياس: ما لا تراه القراءةُ الساكنةُ بحال."""

        return COMPOSITION_IFADA_CONSUMPTION_NAMED_LAWS[
            "TheCallTraceIsStaticNotDynamic"
        ]

    @property
    def census_digest(self) -> str:
        """بصمةُ الإحصاء؛ تتغيّر بتغيّر الإغلاقة أو صفوفها."""

        return canonical_digest(
            canonical_bytes(
                {
                    "closure": list(self.closure),
                    "consumed": [row.algebra.module_prefix for row in self.consumed],
                    "called": [row.algebra.module_prefix for row in self.called],
                }
            )
        )


def derive_consumption_census() -> ConsumptionCensus:
    """اشتقّ الإحصاءَ كلَّه من الشيفرة؛ ولا يُصرَّح فيه عددٌ ولا عضويّة."""

    closure = derive_import_closure()
    members = tuple(
        (module, path)
        for module in closure
        if (path := _module_file(module)) is not None
    )
    rows: list[ConsumptionRow] = []
    for algebra in CANDIDATE_ALGEBRAS:
        prefix = algebra.module_prefix
        reached = tuple(
            module
            for module in closure
            if module == prefix or module.startswith(f"{prefix}.")
        )
        bound: set[str] = set()
        called: set[str] = set()
        for module, path in members:
            names = _bound_names_from(path, module, prefix)
            if not names:
                continue
            bound |= names
            called |= names & _called_names(path, module)
        rows.append(
            ConsumptionRow(
                algebra=algebra,
                reached_modules=reached,
                bound_names=tuple(sorted(bound)),
                called_names=tuple(sorted(called)),
            )
        )
    return ConsumptionCensus(closure=closure, rows=tuple(rows))


def render_consumption_census(census: ConsumptionCensus) -> str:
    """اعرِض الإحصاءَ نصًّا؛ والعرضُ قراءةٌ للمُشتَقّ لا مصدرٌ ثانٍ له."""

    lines = [
        f"مبدأُ الإغلاقة: {THE_PATH_ENTRY_MODULE}",
        f"وحداتُ الإغلاقة: {census.closure_size}",
        f"بصمةُ الإحصاء: {census.census_digest}",
        "",
        "| الجبرُ المرشَّح | مستورَد | مُستدعى | وحداتٌ مبلوغة |",
        "| --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| {row.algebra.name} | {'نعم' if row.is_consumed else 'لا'} "
        f"| {'نعم' if row.is_called else 'لا'} | {len(row.reached_modules)} |"
        for row in census.rows
    )
    lines.extend(
        [
            "",
            f"أيستورد المسارُ جبرًا أوسعَ: {census.any_wider_algebra_is_consumed}",
            f"أيستدعي منه شيئًا: {census.any_wider_algebra_is_called}",
            f"أيمكن قياسُ بلوغ المخرج: {census.output_reach_is_measured}",
            "",
            f"ما لا يراه التتبّع: {census.what_the_call_trace_cannot_see}",
            "",
            "البقايا المُسمّاةُ عند الفجوات:",
        ]
    )
    lines.extend(f"  - {residual}" for residual in census.residuals)
    return "\n".join(lines)


for _law_name, _law_text in COMPOSITION_IFADA_CONSUMPTION_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):  # pragma: no cover - حارسُ بناء
        raise RuntimeError("كلُّ قانونٍ مُسمًّى يفتتح نصُّه باسمه")
