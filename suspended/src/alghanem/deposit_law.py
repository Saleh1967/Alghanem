"""قانونُ الودائع — مصادِقٌ مركزيٌّ يمشي الشجرةَ كلَّها ويفرز قوانينَها.

كان في المستودع مئةٌ وتسعون حارسًا موزَّعةً على تسعين وحدة، كلُّ وحدةٍ تشترط
على نفسها شرطًا وتُنفِّذه عند استيرادها. وكان ذلك كافيًا لكلّ وحدةٍ على حِدَة،
وغيرَ كافٍ للمستودع: **لم يكن ثَمّ موضعٌ واحدٌ يُسأل فيه «هل هذا القانونُ
يصدق على الشجرة كلِّها، أم على من التزمه وحدَه؟»**. وهذه الوحدة ذلك الموضع.
وتفترق فيها اثنتان كانتا تُقرآن «قاعدةً» واحدة::

    Gate (بوابة)     := قانونٌ **تامٌّ اليوم** على الشجرة، يُرفَع خرقُه خطأً
    Witness (شاهد)   := مقدارٌ **مقيسٌ ومنشورٌ ولا يمنع**، لأنّه لا يعمّ بعد

**أوّلًا: كلُّ وحدةٍ وديعةٌ عند القانون، والقانونُ نفسُه وديعةٌ عنده.** يُمشى
على `src/alghanem/**/*.py` كلِّها بلا استثناءٍ ولا قائمةِ إعفاء، وهذا الملفُّ
منها. فما لم يُطِعه هذا الملفُّ لا يُشترَط على غيره
(`THE_LAW_IS_A_DEPOSIT_UNDER_ITSELF`).

**وثانيًا: ولا رقمَ مُجمَّدٍ في هذا الملفّ البتّة.** لا عددَ وحداتٍ، ولا عددَ
بقايا، ولا نسبةَ امتثال. كلُّ مقدارٍ يُحسَب من القرص عند النداء، والاختباراتُ
تؤكّد **الخروقَ صفرًا** لا المقاديرَ أعدادًا. والسببُ مقيسٌ لا مُتوهَّم: في
هذه الشجرة أرقامٌ مُجمَّدةٌ تتزحزح بمجرّد إضافة ملفٍّ إليها، فلو جمَّد القانونُ
مقدارًا لصار هو أوّلَ ما يكذب عند أوّل نموّ
(`A_LAW_THAT_FREEZES_A_MAGNITUDE_BREAKS_WHEN_THE_TREE_GROWS`).

**وثالثًا: والبوابةُ لا تُدَّعى، بل تُنتزَع من كونها تامّةً الآن.** البواباتُ
الثلاثُ أدناه بوّاباتٌ **لأنّ خرقَها صفرٌ على الشجرة وقتَ كتابتها**، وقد
فُحِصت قبل أن تُسنَّ. وما لم يكن خرقُه صفرًا **لم يُرفَع بوابةً ولم يُصلَح
قسرًا**، بل نُشر شاهدًا بمقداره وبأسماء مخالفيه. فمن أراد ترقيةَ شاهدٍ إلى
بوابةٍ لزِمَه أن يُصفِّرَ خرقَه أوّلًا، وذلك عملٌ يُرى في الفرق لا حكمٌ يُكتَب
(`A_GATE_IS_EARNED_BY_A_ZERO_NOT_DECLARED_BY_A_WISH`).

**ورابعًا: وأربعةُ شهودٍ منشورةٌ بخرقها، وهي مواضعُ التفاوت في الشجرة.**

| الشاهد | ما يقيس |
|---|---|
| لهجةُ الوعاء | البقايا المسمّاة تُودَع تارةً قاموسًا وتارةً صفًّا |
| تسميةُ البقيّة نفسَها | نصُّ البقيّة يبتدئ باسمها، وليس ذلك مطّردًا |
| الختمُ ذو المولِّد الحيّ | ختمٌ مُجمَّدٌ بلا دالّةٍ تُعيد توليدَه رقمٌ لا ينبض |
| بابُ المدوَّنة | `read_quran_corpus_bytes` بابُها الوحيد المُصرَّح |

وهذه الأربعةُ **ليست عيوبًا تُخفى ولا قوانينَ تُدَّعى**؛ هي الفرقُ بين ما
عمَّ وما لم يعمَّ بعد، منشورًا بعدده ليُعمَل عليه
(`AN_UNEVEN_CONVENTION_IS_PUBLISHED_AS_A_QUANTITY_NOT_HIDDEN_AS_A_STYLE`).

**وخامسًا: وحكمُ كلّ قانونٍ يُشتَقّ من خرقه، ولا يُكتَب في حقل.** لا حقلَ
`verdict` ولا `passed` في صفٍّ من صفوف هذه الوحدة؛ الحكمُ دالّةٌ على الخروق،
وحارسٌ عند الاستيراد يمنع إدخالَ حقلٍ يحمله.

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا تستورد
هذه الوحدةُ من `kernel/` ولا من `program/` شيئًا، ولا تقرأ مدوَّنةً، ولا
تُعدِّل ملفًّا؛ تقرأ النصَّ وتعُدّ.
"""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

__all__ = [
    "AN_UNEVEN_CONVENTION_IS_PUBLISHED_AS_A_QUANTITY_NOT_HIDDEN_AS_A_STYLE",
    "A_GATE_IS_EARNED_BY_A_ZERO_NOT_DECLARED_BY_A_WISH",
    "A_LAW_THAT_FREEZES_A_MAGNITUDE_BREAKS_WHEN_THE_TREE_GROWS",
    "DEPOSIT_LAW_NAMED_RESIDUALS",
    "THE_CORPUS_DOOR",
    "THE_GUARD_PREFIXES",
    "THE_LAW_IS_A_DEPOSIT_UNDER_ITSELF",
    "THE_RESIDUAL_SUFFIX",
    "Breach",
    "DepositLawError",
    "LawReading",
    "LawStanding",
    "ParsedModule",
    "Standing",
    "every_reading",
    "gate_readings",
    "law_source_root",
    "module_paths",
    "read_the_tree",
    "the_law_holds",
    "witness_readings",
]


class DepositLawError(ValueError):
    """تُرفَع حين يُخرَق قانونٌ بوابة، أو حين يُوصَف القانونُ وصفًا لا يُقاس."""


class Standing(Enum):
    """منزلةُ القانون: بوابةٌ تمنع، أو شاهدٌ يُنشَر ولا يمنع."""

    GATE = "بوابة"
    WITNESS = "شاهد_غير_حارس"


class LawStanding(Enum):
    """حالُ قانونٍ بعد قياسه؛ وتُشتَقّ من عدد خروقه ومن منزلته."""

    HELD = "قائم"
    BREACHED = "مخروق"
    UNEVEN = "متفاوت"


THE_RESIDUAL_SUFFIX: Final[str] = "_NAMED_RESIDUALS"
"""لاحقةُ وعاء البقايا المسمّاة، وهي عُرفُ هذا المستودع في نشر ما لم يُحسَم."""

THE_GUARD_PREFIXES: Final[tuple[str, str]] = ("_assert_", "_verify_")
"""بادئتا الحارس عند الاستيراد؛ وما حملهما لزِمَه أن يُبلَغ لا أن يُعرَّف فقط."""

THE_CORPUS_DOOR: Final[str] = "read_quran_corpus_bytes"
"""البابُ الوحيدُ المُصرَّحُ لبايتات المدوَّنة، ويفحص الطولَ والبصمةَ قبل الردّ."""


@dataclass(frozen=True, slots=True)
class ParsedModule:
    """وحدةٌ مقروءةٌ مرّةً: مسارُها النسبيّ ونصُّها وشجرتُها النحويّة."""

    name: str
    text: str
    tree: ast.Module


@dataclass(frozen=True, slots=True)
class Breach:
    """خرقٌ واحدٌ بموضعه واسمه؛ ولا حكمَ فيه، فالحكمُ على الجملة لا على الفرد."""

    module: str
    detail: str

    def __post_init__(self) -> None:
        if not self.module.strip():
            raise DepositLawError("خرقٌ بلا موضعٍ لا يُنشَر.")
        if not self.detail.strip():
            raise DepositLawError("خرقٌ بلا بيانٍ لا يُنشَر.")


@dataclass(frozen=True, slots=True)
class LawReading:
    """قراءةُ قانونٍ: منزلتُه، وما فُحِص، وما خُرِق — بلا حقلِ حكمٍ مكتوب."""

    name: str
    question: str
    standing: Standing
    examined: int
    breaches: tuple[Breach, ...]

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.question.strip():
            raise DepositLawError("قانونٌ بلا اسمٍ أو بلا سؤالٍ لا يُقاس.")
        if self.examined < 0:
            raise DepositLawError("عددُ المفحوصِ لا يكون سالبًا.")
        if len(self.breaches) > self.examined:
            raise DepositLawError("خروقٌ أكثرُ من المفحوص؛ فالعدُّ غيرُ متّسق.")

    @property
    def breach_count(self) -> int:
        """عددُ الخروق، ويُقرأ من الخروق نفسِها لا من عدّادٍ مودَع."""

        return len(self.breaches)

    @property
    def law_standing(self) -> LawStanding:
        """حالُ القانون مشتقّةً: بوابةٌ مخروقةٌ خطأٌ، وشاهدٌ مخروقٌ تفاوتٌ."""

        if not self.breaches:
            return LawStanding.HELD
        if self.standing is Standing.GATE:
            return LawStanding.BREACHED
        return LawStanding.UNEVEN

    @property
    def conformance(self) -> float:
        """نصيبُ الممتثل؛ ويُحسَب ولا يُجمَّد، فهو يتحرّك بنموّ الشجرة."""

        if self.examined == 0:
            raise DepositLawError("لا نصيبَ لقانونٍ لم يُفحَص له شيء.")
        return (self.examined - self.breach_count) / self.examined


# ---------------------------------------------------------------------------
# مسحُ الشجرة
# ---------------------------------------------------------------------------


def law_source_root() -> Path:
    """جذرُ ما يُقاس؛ وهو حزمةُ المصدر التي تقع فيها هذه الوحدةُ نفسُها."""

    return Path(__file__).resolve().parent


def module_paths() -> tuple[Path, ...]:
    """وحداتُ الشجرة مرتَّبةً، ولا قائمةَ إعفاءٍ فيها ولا استثناءَ لهذا الملفّ."""

    root = law_source_root()
    return tuple(
        path
        for path in sorted(root.rglob("*.py"))
        if path.is_file() and path.name != "__init__.py"
    )


def _relative(path: Path) -> str:
    return path.relative_to(law_source_root()).as_posix()


def read_the_tree() -> tuple[ParsedModule, ...]:
    """تُقرأ الشجرةُ وتُحلَّل مرّةً واحدةً لتُمرَّر على القوانين كلِّها.

    ولا ذاكرةَ هنا ولا تخزين: كلُّ نداءٍ يعود إلى القرص من جديد، وإنّما
    مُنِع التكرارُ داخلَ النداء الواحد لا بين النداءات.
    """

    parsed: list[ParsedModule] = []
    for path in module_paths():
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError as error:  # pragma: no cover - لا نصَّ معطوبًا اليوم
            raise DepositLawError(
                f"وحدةٌ لا تُحلَّل نحويًّا: {_relative(path)} — {error}"
            ) from error
        parsed.append(ParsedModule(_relative(path), text, tree))
    return tuple(parsed)


def _module_level_names(tree: ast.Module) -> set[str]:
    """الأسماءُ المعرَّفةُ في أعلى الوحدة: دوالُّ وأصنافٌ وإسناداتٌ وأسماءٌ مستورَدة."""

    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, ast.Import | ast.ImportFrom):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])
    return names


def _declared_exports(tree: ast.Module) -> tuple[str, ...] | None:
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            try:
                value = ast.literal_eval(node.value)
            except ValueError:
                return None
            if isinstance(value, list | tuple):
                return tuple(str(item) for item in value)
    return None


def _residual_assignments(tree: ast.Module) -> Iterator[tuple[str, ast.expr]]:
    for node in tree.body:
        if not isinstance(node, ast.Assign | ast.AnnAssign):
            continue
        target: ast.expr | None = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target = node.target
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            first = node.targets[0]
            target = first if isinstance(first, ast.Name) else None
        if (
            isinstance(target, ast.Name)
            and target.id.endswith(THE_RESIDUAL_SUFFIX)
            and node.value is not None
        ):
            yield target.id, node.value


def _residual_texts(value: ast.expr) -> tuple[tuple[str | None, str], ...] | None:
    """نصوصُ وعاء البقايا: مفتاحُها إن كان قاموسًا، وإلّا فبلا مفتاح."""

    if isinstance(value, ast.Dict):
        pairs: list[tuple[str | None, str]] = []
        for key, item in zip(value.keys, value.values, strict=True):
            key_text = key.value if isinstance(key, ast.Constant) else None
            pairs.append(
                (
                    key_text if isinstance(key_text, str) else None,
                    _flatten_text(item),
                )
            )
        return tuple(pairs)
    if isinstance(value, ast.Tuple | ast.List):
        return tuple((None, _flatten_text(item)) for item in value.elts)
    return None


def _flatten_text(node: ast.expr) -> str:
    """نصُّ تعبيرٍ إن كان نصًّا أو اسمًا؛ والاسمُ يُردّ باسمه ليُوصَل لاحقًا."""

    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _flatten_text(node.left) + _flatten_text(node.right)
    return ""


def _named_constants(tree: ast.Module) -> dict[str, str]:
    """ثوابتُ النصّ في أعلى الوحدة، ليُوصَل ما أُودِع بالاسم لا بالنصّ."""

    found: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign | ast.AnnAssign):
            continue
        target: ast.expr | None = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target = node.target
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            first = node.targets[0]
            target = first if isinstance(first, ast.Name) else None
        if isinstance(target, ast.Name) and node.value is not None:
            text = _flatten_text(node.value)
            if text and not isinstance(node.value, ast.Name):
                found[target.id] = text
    return found


# ---------------------------------------------------------------------------
# البوّابات الثلاث
# ---------------------------------------------------------------------------


def _gate_residuals_are_non_empty_texts(
    modules: tuple[ParsedModule, ...],
) -> LawReading:
    """كلُّ بقيّةٍ مسمّاةٍ نصٌّ غيرُ فارغ؛ فالبقيّةُ الفارغةُ تحفُّظٌ بلا مضمون."""

    breaches: list[Breach] = []
    examined = 0
    for parsed in modules:
        module, tree = parsed.name, parsed.tree
        constants = _named_constants(tree)
        for container, value in _residual_assignments(tree):
            entries = _residual_texts(value)
            if entries is None:
                continue
            if not entries:
                breaches.append(Breach(module, f"{container} وعاءٌ فارغ"))
                continue
            for key, body in entries:
                examined += 1
                resolved = constants.get(body, body)
                if not resolved.strip():
                    breaches.append(
                        Breach(module, f"{container}[{key or '؟'}] نصٌّ فارغ")
                    )
    return LawReading(
        name="EVERY_NAMED_RESIDUAL_IS_A_NON_EMPTY_TEXT",
        question="هل كلُّ بقيّةٍ مسمّاةٍ نصٌّ غيرُ فارغ؟",
        standing=Standing.GATE,
        examined=examined,
        breaches=tuple(breaches),
    )


def _gate_exports_are_defined_in_their_module(
    modules: tuple[ParsedModule, ...],
) -> LawReading:
    """كلُّ اسمٍ في `__all__` معرَّفٌ أو مستورَدٌ في وحدته؛ فلا تصديرَ لمعدوم."""

    breaches: list[Breach] = []
    examined = 0
    for parsed in modules:
        module, tree = parsed.name, parsed.tree
        exports = _declared_exports(tree)
        if exports is None:
            continue
        defined = _module_level_names(tree)
        for name in exports:
            examined += 1
            if name not in defined:
                breaches.append(Breach(module, f"`{name}` مُصدَّرٌ وليس معرَّفًا"))
    return LawReading(
        name="EVERY_EXPORTED_NAME_IS_DEFINED_IN_ITS_OWN_MODULE",
        question="هل كلُّ اسمٍ مُصدَّرٍ معرَّفٌ في وحدته؟",
        standing=Standing.GATE,
        examined=examined,
        breaches=tuple(breaches),
    )


def _gate_no_guard_is_left_unreached(modules: tuple[ParsedModule, ...]) -> LawReading:
    """حارسٌ يُعرَّف ثمّ لا يُبلَغ قانونٌ مكتوبٌ غيرُ مُنفَّذ، وهو أسوأُ من غيابه."""

    breaches: list[Breach] = []
    examined = 0
    for parsed in modules:
        module, tree = parsed.name, parsed.tree
        defined = {
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name.startswith(THE_GUARD_PREFIXES)
        }
        if not defined:
            continue
        called = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        for name in sorted(defined):
            examined += 1
            if name not in called:
                breaches.append(Breach(module, f"`{name}` حارسٌ معرَّفٌ لا يُبلَغ"))
    return LawReading(
        name="NO_GUARD_IS_DEFINED_AND_LEFT_UNREACHED",
        question="هل كلُّ حارسٍ معرَّفٍ مبلوغٌ في وحدته؟",
        standing=Standing.GATE,
        examined=examined,
        breaches=tuple(breaches),
    )


# ---------------------------------------------------------------------------
# الشهودُ الأربعة
# ---------------------------------------------------------------------------


def _witness_residual_container_dialect(
    modules: tuple[ParsedModule, ...],
) -> LawReading:
    """وعاءُ البقايا قاموسٌ تارةً وصفٌّ تارة؛ واللهجتان تُعدّان ولا تُوحَّد قسرًا."""

    breaches: list[Breach] = []
    examined = 0
    for parsed in modules:
        module, tree = parsed.name, parsed.tree
        for container, value in _residual_assignments(tree):
            examined += 1
            if not isinstance(value, ast.Dict):
                breaches.append(Breach(module, f"{container} صفٌّ لا قاموس"))
    return LawReading(
        name="A_RESIDUAL_CONTAINER_IS_A_MAPPING_FROM_TOKEN_TO_TEXT",
        question="هل كلُّ وعاء بقايا قاموسٌ يربط الرمزَ بنصّه؟",
        standing=Standing.WITNESS,
        examined=examined,
        breaches=tuple(breaches),
    )


def _witness_residual_texts_name_themselves(
    modules: tuple[ParsedModule, ...],
) -> LawReading:
    """نصُّ البقيّة يبتدئ باسمها، فتُقرأ منفردةً عن سياقها؛ وليس ذلك مطّردًا."""

    breaches: list[Breach] = []
    examined = 0
    for parsed in modules:
        module, tree = parsed.name, parsed.tree
        constants = _named_constants(tree)
        for container, value in _residual_assignments(tree):
            entries = _residual_texts(value)
            if entries is None:
                continue
            for key, body in entries:
                if key is None:
                    continue
                examined += 1
                resolved = constants.get(body, body)
                if not resolved.startswith(f"{key}:"):
                    breaches.append(Breach(module, f"{container}[{key}] لا يُسمّي نفسَه"))
    return LawReading(
        name="A_RESIDUAL_TEXT_OPENS_WITH_ITS_OWN_TOKEN",
        question="هل كلُّ نصِّ بقيّةٍ يبتدئ برمزها؟",
        standing=Standing.WITNESS,
        examined=examined,
        breaches=tuple(breaches),
    )


_DIGEST_CONSTANT: Final[re.Pattern[str]] = re.compile(
    r"^[A-Z0-9_]*DIGEST\s*:\s*Final\[str\]", re.MULTILINE
)
_DIGEST_GENERATOR: Final[re.Pattern[str]] = re.compile(r"def \w*digest\w*\s*\(")


def _witness_every_frozen_digest_has_a_live_generator(
    modules: tuple[ParsedModule, ...],
) -> LawReading:
    """ختمٌ مُجمَّدٌ بلا دالّةٍ تُعيد توليدَه رقمٌ لا ينبض، فيُعَدّ ولا يُغفَل."""

    breaches: list[Breach] = []
    examined = 0
    for parsed in modules:
        module, text = parsed.name, parsed.text
        if not _DIGEST_CONSTANT.search(text):
            continue
        examined += 1
        if not (_DIGEST_GENERATOR.search(text) and "canonical_digest" in text):
            breaches.append(Breach(module, "ختمٌ مُجمَّدٌ بلا مولِّدٍ حيّ"))
    return LawReading(
        name="EVERY_FROZEN_DIGEST_HAS_A_LIVE_GENERATOR",
        question="هل كلُّ ختمٍ مُجمَّدٍ تُعيد وحدتُه توليدَه؟",
        standing=Standing.WITNESS,
        examined=examined,
        breaches=tuple(breaches),
    )


_CORPUS_MENTION: Final[re.Pattern[str]] = re.compile(r"corpora[/\\]")


def _witness_the_corpus_is_reached_through_its_door(
    modules: tuple[ParsedModule, ...],
) -> LawReading:
    """المدوَّنةُ تُبلَغ من بابها الفاحصِ للبصمة، ومن ذكر مسارَها فقد جاوره."""

    breaches: list[Breach] = []
    examined = 0
    for parsed in modules:
        module, text = parsed.name, parsed.text
        if not _CORPUS_MENTION.search(text):
            continue
        examined += 1
        if THE_CORPUS_DOOR not in text:
            breaches.append(Breach(module, "يذكر مسارَ المدوَّنة دون بابها"))
    return LawReading(
        name="THE_CORPUS_IS_REACHED_THROUGH_ITS_ONE_DOOR",
        question="هل كلُّ ذاكرٍ للمدوَّنة يبلغها من بابها؟",
        standing=Standing.WITNESS,
        examined=examined,
        breaches=tuple(breaches),
    )


# ---------------------------------------------------------------------------
# القراءةُ المجموعة
# ---------------------------------------------------------------------------


_THE_LAWS: Final[tuple[object, ...]] = (
    _gate_residuals_are_non_empty_texts,
    _gate_exports_are_defined_in_their_module,
    _gate_no_guard_is_left_unreached,
    _witness_residual_container_dialect,
    _witness_residual_texts_name_themselves,
    _witness_every_frozen_digest_has_a_live_generator,
    _witness_the_corpus_is_reached_through_its_door,
)


def every_reading() -> tuple[LawReading, ...]:
    """قراءةُ القوانين كلِّها الآن، مقيسةً من القرص عند كلّ نداء."""

    modules = read_the_tree()
    readings = tuple(law(modules) for law in _THE_LAWS)  # type: ignore[operator]
    names = [reading.name for reading in readings]
    if len(names) != len(set(names)):
        raise DepositLawError("قانونان باسمٍ واحد؛ ولا يُميَّز خرقُ أحدهما عن أخيه.")
    return readings


def gate_readings() -> tuple[LawReading, ...]:
    """البوّاباتُ وحدَها؛ وخرقُ واحدةٍ منها يمنع الدمج."""

    return tuple(r for r in every_reading() if r.standing is Standing.GATE)


def witness_readings() -> tuple[LawReading, ...]:
    """الشهودُ وحدَهم؛ يُنشَرون بمقاديرهم ولا يمنعون."""

    return tuple(r for r in every_reading() if r.standing is Standing.WITNESS)


def the_law_holds() -> bool:
    """هل تقوم البوّاباتُ كلُّها الآن؟ والشاهدُ لا يدخل في هذا الحكم."""

    return all(reading.law_standing is LawStanding.HELD for reading in gate_readings())


def _format_breaches(breaches: Iterable[Breach], limit: int = 5) -> str:
    listed = list(breaches)
    head = "؛ ".join(f"{b.module}: {b.detail}" for b in listed[:limit])
    if len(listed) > limit:
        head += f"؛ وغيرُها {len(listed) - limit}"
    return head


def assert_the_gates_hold() -> None:
    """يُرفَع خطأٌ عند أوّل بوابةٍ مخروقة، وفيه موضعُ الخرق باسمه لا بعدده."""

    for reading in gate_readings():
        if reading.law_standing is LawStanding.BREACHED:
            raise DepositLawError(
                f"بوابةٌ مخروقة — {reading.name}: "
                f"{reading.breach_count} من {reading.examined}. "
                f"{_format_breaches(reading.breaches)}"
            )


# ---------------------------------------------------------------------------
# البقايا المسمّاة، وحُرّاسُ الاستيراد
# ---------------------------------------------------------------------------


THE_LAW_IS_A_DEPOSIT_UNDER_ITSELF: Final[str] = (
    "THE_LAW_IS_A_DEPOSIT_UNDER_ITSELF: يُمشى على وحدات الشجرة كلِّها بلا "
    "قائمة إعفاء، وهذا الملفُّ منها؛ فما لم يُطِعه لا يُشترَط على غيره، "
    "واختبارٌ يتحقّق من أنّه داخلٌ في المسح لا مُخرَجٌ منه"
)

A_LAW_THAT_FREEZES_A_MAGNITUDE_BREAKS_WHEN_THE_TREE_GROWS: Final[str] = (
    "A_LAW_THAT_FREEZES_A_MAGNITUDE_BREAKS_WHEN_THE_TREE_GROWS: لا رقمَ "
    "مُجمَّدٌ في هذه الوحدة البتّة — لا عددَ وحداتٍ ولا نسبةَ امتثال — لأنّ في "
    "هذه الشجرة أرقامًا تتزحزح بمجرّد إضافة ملفٍّ إليها؛ فالمقاديرُ تُحسَب عند "
    "النداء، والاختباراتُ تؤكّد الخروقَ صفرًا لا المقاديرَ أعدادًا"
)

A_GATE_IS_EARNED_BY_A_ZERO_NOT_DECLARED_BY_A_WISH: Final[str] = (
    "A_GATE_IS_EARNED_BY_A_ZERO_NOT_DECLARED_BY_A_WISH: البواباتُ الثلاثُ "
    "رُفِعت بواباتٍ بعد أن فُحِص خرقُها فكان صفرًا على الشجرة؛ وما لم يكن "
    "خرقُه صفرًا لم يُرفَع ولم يُصلَح قسرًا، بل نُشر شاهدًا بمقداره — فترقيةُ "
    "شاهدٍ إلى بوابةٍ عملٌ يُرى في الفرق لا حكمٌ يُكتَب"
)

AN_UNEVEN_CONVENTION_IS_PUBLISHED_AS_A_QUANTITY_NOT_HIDDEN_AS_A_STYLE: Final[str] = (
    "AN_UNEVEN_CONVENTION_IS_PUBLISHED_AS_A_QUANTITY_NOT_HIDDEN_AS_A_STYLE: "
    "لهجةُ وعاء البقايا، وتسميةُ البقيّة نفسَها، ومولِّدُ الختم، وبابُ "
    "المدوَّنة — أربعةُ أعرافٍ لم تعمَّ بعد؛ فلا تُدَّعى قوانينَ ولا تُخفى "
    "أساليبَ، بل تُنشَر أعدادًا بأسماء مخالفيها ليُعمَل عليها"
)

DEPOSIT_LAW_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_LAW_IS_A_DEPOSIT_UNDER_ITSELF": THE_LAW_IS_A_DEPOSIT_UNDER_ITSELF,
    "A_LAW_THAT_FREEZES_A_MAGNITUDE_BREAKS_WHEN_THE_TREE_GROWS": (
        A_LAW_THAT_FREEZES_A_MAGNITUDE_BREAKS_WHEN_THE_TREE_GROWS
    ),
    "A_GATE_IS_EARNED_BY_A_ZERO_NOT_DECLARED_BY_A_WISH": (
        A_GATE_IS_EARNED_BY_A_ZERO_NOT_DECLARED_BY_A_WISH
    ),
    "AN_UNEVEN_CONVENTION_IS_PUBLISHED_AS_A_QUANTITY_NOT_HIDDEN_AS_A_STYLE": (
        AN_UNEVEN_CONVENTION_IS_PUBLISHED_AS_A_QUANTITY_NOT_HIDDEN_AS_A_STYLE
    ),
}
"""بقايا القانون مسمّاةً؛ وهي أوّلُ ما يُفحَص به القانونُ على نفسه."""


def _assert_no_written_verdict_field() -> None:
    """حكمُ القانون يُشتَقّ من خروقه؛ فلا حقلَ يحمله في صفٍّ من صفوفه."""

    forbidden = {"verdict", "passed", "failed", "ok", "valid", "conformance"}
    for dataclass_type in (Breach, LawReading):
        for field in fields(dataclass_type):
            if forbidden & set(field.name.split("_")):
                raise DepositLawError(
                    f"`{field.name}` حكمٌ مودَعٌ في حقل؛ والحكمُ دالّةٌ على الخروق."
                )


def _assert_the_law_freezes_no_magnitude() -> None:
    """لا رقمَ مُجمَّدٌ في نصّ هذه الوحدة؛ فمن جمَّد مقدارًا كسره أوّلُ نموّ."""

    body = Path(__file__).read_text(encoding="utf-8").split('"""', 2)[2]
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith(("#", '"')) and re.search(
            r":\s*Final\[(?:int|float)\]", stripped
        ):
            raise DepositLawError(
                f"مقدارٌ مُجمَّدٌ في القانون: {stripped}؛ والمقاديرُ تُحسَب عند النداء."
            )


def _assert_the_law_measures_itself() -> None:
    """هذا الملفُّ داخلٌ في المسح؛ فقانونٌ يُعفي نفسَه ليس قانونًا."""

    own = Path(__file__).resolve()
    if own not in {path.resolve() for path in module_paths()}:
        raise DepositLawError("القانونُ خارجَ مسحه؛ ولا يُشترَط على غيره ما لا يلزمه.")


def _assert_every_law_is_named_and_placed() -> None:
    """كلُّ قانونٍ له اسمٌ وسؤالٌ ومنزلة، والمنزلتان كلتاهما مأهولتان."""

    readings = every_reading()
    if not readings:
        raise DepositLawError("قانونٌ بلا قوانينَ لا يُصادِق شيئًا.")
    standings = {reading.standing for reading in readings}
    if standings != set(Standing):
        raise DepositLawError(
            "إحدى المنزلتين خالية؛ وفرزُ البوابة عن الشاهد إنّما يُرى بهما معًا."
        )


_assert_no_written_verdict_field()
_assert_the_law_freezes_no_magnitude()
_assert_the_law_measures_itself()
_assert_every_law_is_named_and_placed()
