"""قراءةٌ **مشتقّةٌ من البايتات** لعائلة الفتح: وزنٌ وإعرابٌ وتركيب، لا تحليلٌ منقول.

تأخذ هذه الوحدةُ بايتاتِ العبارة، وتُعيد كلَّ حرفٍ بحامله وحركته من
`word_structure_dictionary`، ثمّ تقرأ من تتابع الحركات وزنَ الفعل وعلامةَ
الإعراب ونوعَ التركيب. ولا يدخلها جدولٌ مكتوبٌ باليد يقول «هذا فاعل»؛ وما لم
تُصِبه قواعدُ القراءة يخرج `UNRECOGNISED` باسمه لا بتخمين.

**والفاعلُ النحويُّ ليس الدورَ الدلاليّ** (`A_SURFACE_FUNCTION_IS_NOT_A_ROLE`):
هذه الوحدةُ تقف عند الوظيفة النحويّة — فعلٌ، ومرفوعٌ بعده، ومنصوب — ولا تُسمّي
فاعلًا للحدث ولا مفعولًا به دلاليًّا. وجسرُ `fath_ontology_bridge` هو الذي
ينقل، بشرطه.

**ولا جذرَ لكلّ لفظ** (`A_FROZEN_NOUN_HAS_NO_DERIVED_ROOT`): «زيدٌ» عَلَمٌ،
و«البابَ» جامدٌ في هذه القراءة؛ فجذرُهما **موقوفٌ** لا مُستخرَجٌ بالقوّة. والذي
يُشتَقّ جذرُه هنا هو الفعلُ وحدَه بعد حذف زوائدَ **مقروءةٍ** لا مفترضة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .word_structure_dictionary import analyze_word

__all__ = [
    "A_FROZEN_NOUN_HAS_NO_DERIVED_ROOT",
    "A_SURFACE_FUNCTION_IS_NOT_A_ROLE",
    "AN_UNREAD_SHAPE_IS_NAMED_NOT_GUESSED",
    "Construction",
    "SurfaceAnalysisError",
    "SyntacticFunction",
    "UtteranceReading",
    "WordReading",
    "WordShape",
    "read_utterance",
    "read_word",
]


class SurfaceAnalysisError(ValueError):
    """رفضٌ بنيويٌّ في القراءة السطحيّة؛ لا حملَ على أقرب حالة."""


A_SURFACE_FUNCTION_IS_NOT_A_ROLE: Final[str] = (
    "الوظيفةُ النحويّةُ ليست الدورَ الدلاليّ: «مرفوعٌ بعد الفعل» وصفُ إعرابٍ، "
    "و«فاعلُ الحدث» وصفُ مشاركةٍ في واقعة؛ ونقلُ الأوّل إلى الثاني يحتاج وزنًا "
    "وتركيبًا ومعنًى معتمدًا، ولا يُفعَل في هذه الوحدة"
)

A_FROZEN_NOUN_HAS_NO_DERIVED_ROOT: Final[str] = (
    "العَلَمُ واللفظُ الجامدُ لا يُحمَلان على جذرٍ مشتقّ: جذرُهما موقوفٌ "
    "بالتصريح، وإخراجُ ثلاثيٍّ منهما بالحذف صناعةُ معلومةٍ لا قراءتُها"
)

AN_UNREAD_SHAPE_IS_NAMED_NOT_GUESSED: Final[str] = (
    "ما لم تُصِبه قواعدُ القراءة يخرج `UNRECOGNISED` باسمه: الصمتُ عن الشكل "
    "خيرٌ من حملِه على أقرب وزنٍ، لأنّ الحملَ يَعبر إلى المضمون بلا شاهد"
)


class WordShape(Enum):
    """أشكالُ الكلمة المقروءةُ من الحركات؛ مفردةٌ مغلقةٌ فيها عضوُ الجهل."""

    VERB_FORM_I_ACTIVE_PERFECT = "verb_form_i_active_perfect"
    VERB_FORM_I_PASSIVE_PERFECT = "verb_form_i_passive_perfect"
    VERB_FORM_VII_PERFECT = "verb_form_vii_perfect"
    VERB_FORM_I_IMPERFECT_JUSSIVE = "verb_form_i_imperfect_jussive"
    NOUN_NOMINATIVE_INDEFINITE = "noun_nominative_indefinite"
    NOUN_ACCUSATIVE_DEFINITE = "noun_accusative_definite"
    NOUN_NOMINATIVE_DEFINITE = "noun_nominative_definite"
    JUSSIVE_NEGATION_PARTICLE = "jussive_negation_particle"
    CONDITIONAL_PARTICLE = "conditional_particle"
    UNRECOGNISED = "unrecognised"

    @property
    def is_verb(self) -> bool:
        """أفعلٌ هو؟ خاصّيّةٌ تُشتَقّ من العضو لا حقلٌ يُكتَب بجنبه."""

        return self.value.startswith("verb_")

    @property
    def is_noun(self) -> bool:
        """أاسمٌ هو؟"""

        return self.value.startswith("noun_")


class SyntacticFunction(Enum):
    """الوظائفُ النحويّةُ المقروءة؛ وهي **إعرابٌ** لا أدوارَ حدث."""

    VERB = "verb"
    NOMINATIVE_AFTER_VERB = "nominative_after_verb"
    ACCUSATIVE_AFTER_VERB = "accusative_after_verb"
    NEGATION_PARTICLE = "negation_particle"
    CONDITIONAL_PARTICLE = "conditional_particle"
    UNASSIGNED = "unassigned"


class Construction(Enum):
    """أنواعُ التركيب المقروءةُ من تتابع الأشكال؛ وما خرج عنها يُسمّى مجهولًا."""

    ACTIVE_TRANSITIVE = "active_transitive"
    PASSIVE_ONE_NOMINATIVE = "passive_one_nominative"
    FORM_VII_ONE_NOMINATIVE = "form_vii_one_nominative"
    NEGATED_ACTIVE_TRANSITIVE = "negated_active_transitive"
    CONDITIONAL_ACTIVE_TRANSITIVE = "conditional_active_transitive"
    UNRECOGNISED = "unrecognised"


_FATHA: Final[str] = "FATHA"
_DAMMA: Final[str] = "DAMMA"
_KASRA: Final[str] = "KASRA"
_SUKUN_EXPLICIT: Final[str] = "SUKUN_EXPLICIT"
_SUKUN_IMPLICIT: Final[str] = "SUKUN_IMPLICIT"


@dataclass(frozen=True, slots=True)
class WordReading:
    """قراءةُ كلمةٍ واحدة: شكلُها، وحوامِلُها وحركاتُها، وجذرُها إن رُخِّص."""

    surface: str
    shape: WordShape
    carriers: tuple[str, ...]
    states: tuple[str, ...]
    root_letters: tuple[str, ...]
    root_is_withheld: bool
    carries_tanwin: bool

    def __post_init__(self) -> None:
        if len(self.carriers) != len(self.states):
            raise SurfaceAnalysisError("عددُ الحوامل يخالف عددَ الحركات")
        if self.root_is_withheld and self.root_letters:
            raise SurfaceAnalysisError(
                A_FROZEN_NOUN_HAS_NO_DERIVED_ROOT + "؛ وجذرٌ موقوفٌ لا يحمل حروفًا"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القراءة للبصمة."""

        return {
            "surface": self.surface,
            "shape": self.shape.value,
            "carriers": list(self.carriers),
            "states": list(self.states),
            "root_letters": list(self.root_letters),
            "root_is_withheld": self.root_is_withheld,
            "carries_tanwin": self.carries_tanwin,
        }


def _shape_of(
    carriers: tuple[str, ...], states: tuple[str, ...], tanwin: bool
) -> tuple[WordShape, tuple[str, ...], bool]:
    """اقرأ الشكلَ من تتابع الحركات وحدَه؛ ثمّ قل أجذرٌ يخرج أم يُوقَف."""

    if carriers == ("ل", "م") and states == (_FATHA, _SUKUN_EXPLICIT):
        return WordShape.JUSSIVE_NEGATION_PARTICLE, (), True
    if carriers == ("ء", "ن") and states == (_KASRA, _SUKUN_EXPLICIT):
        return WordShape.CONDITIONAL_PARTICLE, (), True
    if len(carriers) == 3 and states == (_FATHA, _FATHA, _FATHA):
        return WordShape.VERB_FORM_I_ACTIVE_PERFECT, carriers, False
    if len(carriers) == 3 and states == (_DAMMA, _KASRA, _FATHA):
        return WordShape.VERB_FORM_I_PASSIVE_PERFECT, carriers, False
    if (
        len(carriers) == 5
        and carriers[0] == "ا"
        and carriers[1] == "ن"
        and states[0] == _SUKUN_IMPLICIT
        and states[1] == _SUKUN_EXPLICIT
        and states[2:] == (_FATHA, _FATHA, _FATHA)
    ):
        return WordShape.VERB_FORM_VII_PERFECT, carriers[2:], False
    if (
        len(carriers) == 4
        and carriers[0] == "ي"
        and states == (_FATHA, _SUKUN_EXPLICIT, _FATHA, _SUKUN_EXPLICIT)
    ):
        return WordShape.VERB_FORM_I_IMPERFECT_JUSSIVE, carriers[1:], False
    definite = (
        len(carriers) > 2
        and carriers[0] == "ا"
        and carriers[1] == "ل"
        and states[0] == _SUKUN_IMPLICIT
        and states[1] == _SUKUN_EXPLICIT
    )
    if tanwin and states[-1] == _DAMMA and not definite:
        return WordShape.NOUN_NOMINATIVE_INDEFINITE, (), True
    if definite and not tanwin and states[-1] == _FATHA:
        return WordShape.NOUN_ACCUSATIVE_DEFINITE, (), True
    if definite and not tanwin and states[-1] == _DAMMA:
        return WordShape.NOUN_NOMINATIVE_DEFINITE, (), True
    return WordShape.UNRECOGNISED, (), True


def read_word(surface: str) -> WordReading:
    """اقرأ كلمةً واحدةً قراءةً مشتقّةً من حواملها وحركاتها.

    المدخل: سطحُ الكلمة مشكولًا.
    الشرط: الكلمةُ تعود إلى نفسها في التحليل (`surface_round_trips`).
    المخرج: قراءةٌ فيها الشكلُ والحواملُ والحركاتُ والجذرُ إن رُخِّص.
    حدُّها: لا تُسمّي وظيفةً نحويّةً ولا دورًا؛ ولا تُخمِّن شكلًا لم تُصِبه قواعدُها.
    """

    if not isinstance(surface, str) or not surface.strip():
        raise SurfaceAnalysisError("سطحُ الكلمة نصٌّ غير فارغ")
    analysis = analyze_word(surface)
    if not analysis.surface_round_trips:
        raise SurfaceAnalysisError(
            f"الكلمةُ «{surface}» لا تعود إلى نفسها في التحليل؛ ولا قراءةَ على خطّ مكسور"
        )
    carriers = tuple(letter.carrier for letter in analysis.letters)
    states: list[str] = []
    for letter in analysis.letters:
        if letter.state is None:
            raise SurfaceAnalysisError(
                f"حرفٌ بلا حالٍ مقروءةٍ في «{surface}»؛ والقراءةُ تقف ولا تفترض"
            )
        states.append(letter.state.name)
    tanwin = bool(analysis.letters[-1].tanwin)
    shape, root, withheld = _shape_of(carriers, tuple(states), tanwin)
    return WordReading(
        surface=surface,
        shape=shape,
        carriers=carriers,
        states=tuple(states),
        root_letters=root,
        root_is_withheld=withheld,
        carries_tanwin=tanwin,
    )


@dataclass(frozen=True, slots=True)
class UtteranceReading:
    """قراءةُ عبارةٍ كاملة: بصمةُ بايتاتها، وكلماتُها، ووظائفُها، وتركيبُها."""

    surface: str
    utterance_digest: str
    words: tuple[WordReading, ...]
    functions: tuple[SyntacticFunction, ...]
    construction: Construction

    def __post_init__(self) -> None:
        if len(self.words) != len(self.functions):
            raise SurfaceAnalysisError("عددُ الكلمات يخالف عددَ الوظائف")

    def function_of(self, function: SyntacticFunction) -> WordReading | None:
        """الكلمةُ التي أخذت وظيفةً بعينها، أو لا شيءَ إن لم تقع."""

        for word, assigned in zip(self.words, self.functions, strict=True):
            if assigned is function:
                return word
        return None

    @property
    def verb(self) -> WordReading | None:
        """الفعلُ في العبارة إن وُجِد؛ خاصّيّةٌ تُشتَقّ ولا تُكتَب."""

        return self.function_of(SyntacticFunction.VERB)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القراءة للبصمة."""

        return {
            "surface": self.surface,
            "utterance_digest": self.utterance_digest,
            "words": [word.as_canonical_content() for word in self.words],
            "functions": [function.value for function in self.functions],
            "construction": self.construction.value,
        }


def _construction_of(
    shapes: tuple[WordShape, ...],
) -> tuple[Construction, tuple[SyntacticFunction, ...]]:
    """اقرأ التركيبَ من تتابع الأشكال؛ وما خرج عنه يُسمّى مجهولًا لا يُحمَل."""

    unassigned = tuple(SyntacticFunction.UNASSIGNED for _ in shapes)
    if shapes == (
        WordShape.VERB_FORM_I_ACTIVE_PERFECT,
        WordShape.NOUN_NOMINATIVE_INDEFINITE,
        WordShape.NOUN_ACCUSATIVE_DEFINITE,
    ):
        return Construction.ACTIVE_TRANSITIVE, (
            SyntacticFunction.VERB,
            SyntacticFunction.NOMINATIVE_AFTER_VERB,
            SyntacticFunction.ACCUSATIVE_AFTER_VERB,
        )
    if shapes == (
        WordShape.VERB_FORM_I_PASSIVE_PERFECT,
        WordShape.NOUN_NOMINATIVE_DEFINITE,
    ):
        return Construction.PASSIVE_ONE_NOMINATIVE, (
            SyntacticFunction.VERB,
            SyntacticFunction.NOMINATIVE_AFTER_VERB,
        )
    if shapes == (
        WordShape.VERB_FORM_VII_PERFECT,
        WordShape.NOUN_NOMINATIVE_DEFINITE,
    ):
        return Construction.FORM_VII_ONE_NOMINATIVE, (
            SyntacticFunction.VERB,
            SyntacticFunction.NOMINATIVE_AFTER_VERB,
        )
    if shapes == (
        WordShape.JUSSIVE_NEGATION_PARTICLE,
        WordShape.VERB_FORM_I_IMPERFECT_JUSSIVE,
        WordShape.NOUN_NOMINATIVE_INDEFINITE,
        WordShape.NOUN_ACCUSATIVE_DEFINITE,
    ):
        return Construction.NEGATED_ACTIVE_TRANSITIVE, (
            SyntacticFunction.NEGATION_PARTICLE,
            SyntacticFunction.VERB,
            SyntacticFunction.NOMINATIVE_AFTER_VERB,
            SyntacticFunction.ACCUSATIVE_AFTER_VERB,
        )
    if shapes == (
        WordShape.CONDITIONAL_PARTICLE,
        WordShape.VERB_FORM_I_ACTIVE_PERFECT,
        WordShape.NOUN_NOMINATIVE_INDEFINITE,
        WordShape.NOUN_ACCUSATIVE_DEFINITE,
    ):
        return Construction.CONDITIONAL_ACTIVE_TRANSITIVE, (
            SyntacticFunction.CONDITIONAL_PARTICLE,
            SyntacticFunction.VERB,
            SyntacticFunction.NOMINATIVE_AFTER_VERB,
            SyntacticFunction.ACCUSATIVE_AFTER_VERB,
        )
    return Construction.UNRECOGNISED, unassigned


def read_utterance(utterance_bytes: bytes) -> UtteranceReading:
    """اقرأ عبارةً من **بايتاتها**: كلمةً كلمةً، ثمّ تركيبًا، ثمّ وظائفَ إعراب.

    المدخل: بايتاتُ العبارة بترميز UTF-8؛ ونصٌّ جاهزٌ يُرَدّ لأنّ البصمةَ على البايتات.
    الشرط: كلُّ كلمةٍ تعود إلى نفسها، وإلّا وقفت القراءة.
    المخرج: قراءةٌ فيها بصمةُ البايتات، والكلماتُ بأشكالها، والتركيبُ والوظائف.
    حدُّها: الوظائفُ **إعرابٌ** لا أدوارُ حدث؛ والعبورُ إلى الدور في الجسر وحدَه.
    """

    if not isinstance(utterance_bytes, bytes):
        raise SurfaceAnalysisError(
            "مدخلُ العبارة بايتاتٌ خام؛ والنصُّ الجاهزُ يُخفي ما يُبصَم عليه"
        )
    surface = utterance_bytes.decode("utf-8")
    tokens = tuple(token for token in surface.split(" ") if token)
    if not tokens:
        raise SurfaceAnalysisError("عبارةٌ بلا كلمات")
    words = tuple(read_word(token) for token in tokens)
    construction, functions = _construction_of(tuple(word.shape for word in words))
    digest = canonical_digest(canonical_bytes({"utterance_bytes": surface}))
    return UtteranceReading(
        surface=surface,
        utterance_digest=digest,
        words=words,
        functions=functions,
        construction=construction,
    )
