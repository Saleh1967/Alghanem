"""طبقةُ التفسير: المقاييسُ وMASAQ يُقرآن **بعد** الاشتقاق ولا يدخلان فيه.

المسارُ في `composition_ifada_path` يُساق من البايتات وحدَها: لا معجمَ يُستدعى
فيه، ولا مدوّنةً مُعلَّمة، ولا جذرًا. وهذه الوحدةُ تأتي بعدَه فتُعلِّق على ما
اشتُقّ، ولا تُبدّل منه حرفًا. فـ«مقاييس اللغة» شاهدٌ للأصل، وMASAQ مدوّنةٌ
مُعلَّمة، وكلاهما — بنصّ الطلب — **للتفسير**.

`InterpretationFollowsDerivationAndNeverFeedsIt`: هذه الوحدةُ تستورد من المسار
ولا يستورد منها، فالاتّجاهُ مقطوعٌ بنيويًّا لا بوعد. ومدخلُها `PathRun` تامٌّ
قد وقع، فلا سبيل لها إلى تغيير حكم انتقالٍ ولا حال إفادة. والفقرةُ التي تُقاس
هي: سَوقُ البايتات نفسِها مرّةً ثانيةً يُخرج الحكمَ عينَه، عُلِّق عليه أو لم
يُعلَّق.

`ADeclaredRootIsNotADerivedRoot`: المقاييسُ مفهرسٌ بالجذر والوقوعُ سطحٌ، ولا
مُستخرِجَ جذورٍ في هذا الخطّ (`SurfaceIsNotRoot` في `maqayis_lexical_evidence`،
و`A_CANDIDATE_ROOT_IS_DECLARED_NOT_DERIVED` في `maqayis_lexical_origin`). فالجذرُ
الذي يُبحَث عنه ههنا **مكتوبٌ بيدٍ تعليقًا**، مُصرَّحٌ بكاتبه، والمقيسُ وقوعُه
في البايتات المُبصَّمة لا صحّتُه ولا اشتقاقُ الكلمة منه. ولو دخل هذا المكتوبُ
في الاشتقاق لكان جوابًا مرجعيًّا مُمرَّرًا، وهو عينُ الممنوع.

`AnAxisIsAQuotedGlossNotADerivedMeaning`: «المحاور الدلالية» في الملفّ نصٌّ كتبه
المصدر، يُنقَل كما ورد ولا يُحوَّل معنًى مُثبَتًا ولا يُجمَع ولا يُرجَّح. وشهادةُ
المعجم بالمدخل لا تقول إنّ الكلمة مشتقّةٌ منه (`AttestationIsNotBinding`).

`MasaqBytesAreAbsentNotRefused`: بايتاتُ MASAQ ليست في هذه الشجرة الآن، وموضعُها
مسنونٌ ببصمته في `masaq_corpus_deposit`. فيُعرَض غيابُها غيابًا مُسمًّى، ولا
يُختلَق وسمٌ ولا يُقرأ الغيابُ منعًا (`APermissionUnexaminedIsNotAPermission
Refused`).

`TheGlossIsNotAnEvidenceOffer`: ما يخرج من هنا تعليقٌ مقروءُ السند، لا دليلَ
ولادةٍ ولا مُدخَلَ تقييم. وتقديمُه — إن قُدّم يومًا — يمرُّ بسلسلة اكتساب
الأدلّة المرخَّصة، ولا يقع بمجرّد قراءته هنا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .composition_ifada_path import PathRun, PathStage, run_bytes
from .maqayis_lexical_origin import RootAttestation, root_index
from .maqayis_root_table_deposit import FROZEN_ROOT_TABLE, root_table_rows
from .masaq_corpus_deposit import (
    MASAQ_ATTRIBUTION,
    MASAQ_PATH_VARIABLE,
    MASAQ_RELATIVE_PATH,
    MASAQ_SHA256,
    masaq_bytes_are_resolvable,
)

__all__ = [
    "COMPOSITION_IFADA_INTERPRETATION_NAMED_LAWS",
    "DeclaredRootAnnotation",
    "Interpretation",
    "InterpretationError",
    "MasaqStanding",
    "WordGloss",
    "interpret",
    "masaq_standing",
    "render_interpretation",
]


class InterpretationError(ValueError):
    """رفضٌ بنيويٌّ في بناء التعليق، لا حكمٌ على النصّ المُفسَّر."""


class MasaqStanding(Enum):
    """حالُ بايتات MASAQ عند القراءة؛ والغيابُ عضوٌ مُصرَّحٌ به لا صمت."""

    BYTES_RESOLVED = "بايتاتٌ مُحَلَّةٌ بمسارها"
    BYTES_ABSENT = "بايتاتٌ غيرُ موجودةٍ في هذه الشجرة ولا في مسارٍ مُصرَّح"


COMPOSITION_IFADA_INTERPRETATION_NAMED_LAWS: Final[dict[str, str]] = {
    "InterpretationFollowsDerivationAndNeverFeedsIt": (
        "InterpretationFollowsDerivationAndNeverFeedsIt: التفسيرُ يقرأ سَوقًا "
        "تامًّا قد وقع، ولا يدخل في اشتقاقه. والاتّجاهُ مقطوعٌ بنيويًّا: هذه "
        "الوحدةُ تستورد من المسار ولا يستورد منها. والفقرةُ المقيسة أنّ سَوقَ "
        "البايتات نفسِها يُخرج الحكمَ عينَه، عُلِّق عليه أو لم يُعلَّق"
    ),
    "ADeclaredRootIsNotADerivedRoot": (
        "ADeclaredRootIsNotADerivedRoot: الجذرُ المبحوثُ عنه ههنا مكتوبٌ بيدٍ "
        "تعليقًا ومُصرَّحٌ بكاتبه، لا مُستخرَجٌ من الكلمة. والمقيسُ وقوعُه في "
        "البايتات المُبصَّمة لا صحّتُه ولا اشتقاقُ الكلمة منه. ولو دخل في "
        "الاشتقاق لكان جوابًا مرجعيًّا مُمرَّرًا"
    ),
    "AnAxisIsAQuotedGlossNotADerivedMeaning": (
        "AnAxisIsAQuotedGlossNotADerivedMeaning: محاورُ المعجم نصٌّ كتبه "
        "المصدر، يُنقَل كما ورد ولا يُحوَّل معنًى مُثبَتًا ولا يُجمَع ولا "
        "يُرجَّح؛ وشهادةُ المدخل ليست ربطَ الكلمة بجذرها"
    ),
    "MasaqBytesAreAbsentNotRefused": (
        "MasaqBytesAreAbsentNotRefused: غيابُ بايتات MASAQ يُعرَض غيابًا "
        "مُسمًّى بموضعه وبصمته، ولا يُختلَق وسمٌ مكانه ولا يُقرأ الغيابُ منعًا"
    ),
    "TheGlossIsNotAnEvidenceOffer": (
        "TheGlossIsNotAnEvidenceOffer: ما يخرج من هنا تعليقٌ مقروءُ السند لا "
        "دليلَ ولادةٍ ولا مُدخَلَ تقييم، وتقديمُه يمرُّ بسلسلة اكتساب الأدلّة "
        "المرخَّصة ولا يقع بقراءته"
    ),
}
"""القيودُ المُسمّاةُ لهذه الطبقة؛ كلُّ نصٍّ يفتتح باسم قانونه."""


_MASAQ_ABSENCE_LAW: Final[str] = COMPOSITION_IFADA_INTERPRETATION_NAMED_LAWS[
    "MasaqBytesAreAbsentNotRefused"
]


@dataclass(frozen=True, slots=True)
class DeclaredRootAnnotation:
    """جذرٌ مكتوبٌ بيدٍ تعليقًا على كلمةٍ بموضعها، بكاتبه وسبب كتابته."""

    word_index: int
    root: str
    declared_by: str
    why: str

    def __post_init__(self) -> None:
        if type(self.word_index) is not int or self.word_index < 0:
            raise InterpretationError("التعليقُ يُنسَب إلى موضع كلمةٍ غيرِ سالب.")
        for name in ("root", "declared_by", "why"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise InterpretationError(f"{name} نصٌّ غير فارغ.")


@dataclass(frozen=True, slots=True)
class WordGloss:
    """تعليقٌ على كلمةٍ واحدة: جذرُها المُعلَن، وشهادةُ المعجم، ومحاورُه منقولة."""

    word_index: int
    surface: str
    annotation: DeclaredRootAnnotation | None
    attestation: RootAttestation
    root_types: tuple[str, ...]
    quoted_axes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.attestation, RootAttestation):
            raise InterpretationError("الشهادةُ عضوٌ في مفردتها المغلقة.")
        if self.annotation is None:
            if self.attestation is not RootAttestation.NOT_LICENSED_FOR_THIS_WORD:
                raise InterpretationError(
                    "كلمةٌ بلا جذرٍ مُعلَنٍ لا تُشهَد ولا تُنفى، بل يُصرَّح " "بامتناع الترخيص."
                )
            if self.root_types or self.quoted_axes:
                raise InterpretationError("لا منقولَ لكلمةٍ لم يُعلَن لها جذر.")
        if self.attestation is RootAttestation.NOT_ATTESTED and (
            self.root_types or self.quoted_axes
        ):
            raise InterpretationError("غيرُ المشهود لا يُنقَل عنه محورٌ ولا نوع.")

    @property
    def carries_a_quoted_gloss(self) -> bool:
        """أنُقِل عن المعجم شيءٌ بعينه لهذه الكلمة؟ ولا يُقرأ ذلك معنًى مُثبَتًا."""

        return self.attestation is RootAttestation.ATTESTED and bool(self.quoted_axes)


def masaq_standing(path: Path | str | None = None) -> MasaqStanding:
    """حالُ بايتات MASAQ: مُحَلَّةٌ أو غائبة، وكلتاهما مُسمّاةٌ لا صامتة."""

    if masaq_bytes_are_resolvable(path):
        return MasaqStanding.BYTES_RESOLVED
    return MasaqStanding.BYTES_ABSENT


@dataclass(frozen=True, slots=True)
class Interpretation:
    """تعليقٌ على سَوقٍ تامّ: تعاليقُ كلماته، وحالُ المدوّنة المُعلَّمة."""

    run: PathRun
    glosses: tuple[WordGloss, ...]
    masaq: MasaqStanding
    lexicon_digest: str

    def __post_init__(self) -> None:
        if type(self.run) is not PathRun:
            raise InterpretationError("المُفسَّرُ سَوقٌ مُصاغٌ قد تمّ.")
        if type(self.glosses) is not tuple:
            raise InterpretationError("التعاليقُ مجموعةٌ مُصاغة.")
        if len(self.glosses) != len(self.run.words):
            raise InterpretationError(
                "لكلّ كلمةٍ مقروءةٍ تعليقُها، ولو كان امتناعًا مُصرَّحًا به."
            )
        for position, gloss in enumerate(self.glosses):
            if gloss.word_index != position:
                raise InterpretationError("ترتيبُ التعاليق ترتيبُ كلمات السَّوق.")
        if not isinstance(self.masaq, MasaqStanding):
            raise InterpretationError("حالُ المدوّنة عضوٌ في مفردتها المغلقة.")
        if len(self.lexicon_digest) != 64:
            raise InterpretationError("بصمةُ المعجم بصمةُ البايتات المقروءة.")

    @property
    def derivation_is_unchanged(self) -> bool:
        """أيُخرِج سَوقُ البايتات نفسِها الحكمَ عينَه بعد التعليق؟

        وهذا قياسٌ لا وعد: تُعاد البايتاتُ إلى `run_bytes` فتُقارَن الطبقةُ
        المبلوغة وحالُ الإفادة وأثرُ السَّوق كلُّه.
        """

        again = run_bytes(self.run.source)
        return (
            again.reached is self.run.reached
            and again.outcome is self.run.outcome
            and again.stop is self.run.stop
            and again.ifada is self.run.ifada
            and again.trace.events == self.run.trace.events
        )

    @property
    def glossed_words(self) -> int:
        """كم كلمةً نُقِل عنها شيءٌ بعينه؛ والباقي مُصرَّحٌ به لا مطويّ."""

        return sum(1 for gloss in self.glosses if gloss.carries_a_quoted_gloss)


def _axes_by_root(root: str, tree_root: Path | None = None) -> tuple[str, ...]:
    """محاورُ المعجم لهذا المدخل، منقولةً كما وردت بترتيب ورودها بلا تكرار."""

    seen: list[str] = []
    for row in root_table_rows(tree_root):
        if row["root_full"] != root:
            continue
        axes = row["semantic_axes"]
        if axes and axes not in seen:
            seen.append(axes)
    return tuple(seen)


def interpret(
    run: PathRun,
    annotations: tuple[DeclaredRootAnnotation, ...] = (),
    *,
    tree_root: Path | None = None,
    masaq_path: Path | str | None = None,
) -> Interpretation:
    """علِّق على سَوقٍ تامّ بشواهد المقاييس، بلا مساسٍ باشتقاقه.

    والتعاليقُ مكتوبةٌ بيدٍ ومُصرَّحٌ بكاتبها؛ وما لم يُكتَب لكلمةٍ تعليقٌ
    خرجت بـ`NOT_LICENSED_FOR_THIS_WORD` تصريحًا لا إهمالًا.
    """

    if type(run) is not PathRun:
        raise InterpretationError("المُفسَّرُ سَوقٌ مُصاغٌ قد تمّ.")
    if type(annotations) is not tuple:
        raise InterpretationError("التعاليقُ مجموعةٌ مُصاغة.")
    declared: dict[int, DeclaredRootAnnotation] = {}
    for annotation in annotations:
        if type(annotation) is not DeclaredRootAnnotation:
            raise InterpretationError("كلُّ تعليقٍ جذرٌ مُعلَنٌ مُصاغ.")
        if annotation.word_index in declared:
            raise InterpretationError("لا تعليقان لكلمةٍ واحدةٍ في موضعٍ واحد.")
        if annotation.word_index >= len(run.words):
            raise InterpretationError("التعليقُ يُنسَب إلى كلمةٍ قرأها السَّوق.")
        declared[annotation.word_index] = annotation

    index = root_index(tree_root)
    glosses: list[WordGloss] = []
    for position, word in enumerate(run.words):
        found = declared.get(position)
        if found is None:
            glosses.append(
                WordGloss(
                    word_index=position,
                    surface=word.surface,
                    annotation=None,
                    attestation=RootAttestation.NOT_LICENSED_FOR_THIS_WORD,
                    root_types=(),
                    quoted_axes=(),
                )
            )
            continue
        annotation = found
        types = index.get(annotation.root, ())
        if not types:
            glosses.append(
                WordGloss(
                    word_index=position,
                    surface=word.surface,
                    annotation=annotation,
                    attestation=RootAttestation.NOT_ATTESTED,
                    root_types=(),
                    quoted_axes=(),
                )
            )
            continue
        glosses.append(
            WordGloss(
                word_index=position,
                surface=word.surface,
                annotation=annotation,
                attestation=RootAttestation.ATTESTED,
                root_types=types,
                quoted_axes=_axes_by_root(annotation.root, tree_root),
            )
        )

    return Interpretation(
        run=run,
        glosses=tuple(glosses),
        masaq=masaq_standing(masaq_path),
        lexicon_digest=FROZEN_ROOT_TABLE.sha256_hex,
    )


def render_interpretation(interpretation: Interpretation) -> str:
    """اعرض التعليقَ نصًّا، مفصولًا عن الاشتقاق ومصحوبًا بسنده."""

    run = interpretation.run
    lines = [
        f"الطبقةُ المبلوغة: {run.reached.value}",
        f"حالُ الإفادة: {run.ifada.value}",
        f"الاشتقاقُ لم يتغيّر بالتعليق: {interpretation.derivation_is_unchanged}",
        "",
        f"معجمُ التفسير: {FROZEN_ROOT_TABLE.source_name}"
        f" ({interpretation.lexicon_digest[:16]}…)",
        f"المدوّنةُ المُعلَّمة MASAQ: {interpretation.masaq.value}",
    ]
    if interpretation.masaq is MasaqStanding.BYTES_ABSENT:
        lines.extend(
            [
                f"  موضعُها المسنون: {MASAQ_RELATIVE_PATH} أو {MASAQ_PATH_VARIABLE}",
                f"  بصمتُها المُجمَّدة: {MASAQ_SHA256[:16]}…",
                "  " + _MASAQ_ABSENCE_LAW,
            ]
        )
    else:
        lines.append(f"  الإسناد: {MASAQ_ATTRIBUTION}")
    lines.extend(
        [
            "",
            "| الكلمة | الجذرُ المُعلَن | الشهادة | المنقول |",
            "| --- | --- | --- | --- |",
        ]
    )
    for gloss in interpretation.glosses:
        root = gloss.annotation.root if gloss.annotation is not None else "—"
        axes = " ؛ ".join(gloss.quoted_axes) if gloss.quoted_axes else "—"
        lines.append(
            f"| {gloss.surface} | {root} | {gloss.attestation.value} | {axes} |"
        )
    return "\n".join(lines)


for _law_name, _law_text in COMPOSITION_IFADA_INTERPRETATION_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("كلُّ نصِّ قانونٍ يفتتح باسم قانونه.")
if len(MasaqStanding) != 2:
    raise RuntimeError("حالُ البايتات اثنتان: مُحَلَّةٌ أو غائبة.")
if PathStage.UTF8_BYTES.rank != 1:
    raise RuntimeError("التفسيرُ يعلو مسارًا يبدأ من البايتات.")
