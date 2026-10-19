"""الطبقاتُ الخمس: إدراكٌ فثوابتُ فترابطٌ فتقديرٌ فبيانٌ مختوم.

الطبقاتُ ليست تقسيمَ عملٍ بل **سلسلةَ إذن**: لا تبدأ طبقةٌ حتّى تُسلِّمها
سابقتُها. ولذلك لا تُصدَّر ههنا خمسُ دوالَّ مستقلّةٍ تُنادى بأيّ ترتيب، بل
ماشيةٌ واحدةٌ تحمل ما بلغته، وكلُّ طبقةٍ ترفض أن تُستدعى على حالٍ لم تبلغها
(`A_LAYER_CALLED_OUT_OF_ORDER_FORGES_A_SANAD`)::

    QuestionDomain != WordCategory
    Proxy          != Certificate
    MethodOfDomain != StrongestMethod
    Sealed         != True

**وتصنيفُ السؤال ليس تصنيفَ الكلمة.** في هذه الشجرة وحدةٌ اسمُها
`classification_coverage_scheme`، وهي تُصنّف **كلماتِ مُودَعٍ** تصنيفًا صرفيًّا
وتقيس تغطيتَه؛ وليست تصنيفَ أسئلةٍ إلى نظريٍّ وتجريبيٍّ ولغويٍّ وأصوليّ. فلو
مُدَّت تلك الوحدةُ لتحمل هذا لصار اللفظُ الواحدُ جنسَين، كما كان «الدالُّ
وحدَه» و«الدراية» (`QUESTION_CLASSIFICATION_IS_NOT_WORD_CLASSIFICATION`).

**والثقةُ مُعلَنةٌ مع كلّ تصنيف.** التصنيفُ ههنا بقرائنَ لفظيّةٍ مسنونةٍ بيدٍ،
فهو **وكيلٌ** لا قاطع، ولا يُقرأ قطعيًّا إلّا حين تنفرد قرينةُ مجالٍ واحدٍ
ولا تُنازعها غيرُها. وأمّا انعدامُ القرائن فليس تصنيفًا بثقةٍ ضعيفة بل **امتناعٌ
عن التصنيف** يُسمّى باسمه (`NO_MARKER_IS_A_REFUSAL_NOT_A_WEAK_GUESS`).

**والثابتُ لا يُسترَدُّ إلّا بشهادته.** الموصِّلُ ههنا لا يحمل قيمةً مخزونة، بل
يستدعي مولِّدَ الختم الآن ويصادمه بمنقوله، فإن لم يكن للاسم ختمٌ في السجلّ رُدَّ
**دعوى** لا ثابتًا، وإن انزاح ختمُه رُدَّ منزاحًا مسمًّى
(`A_NAME_WITHOUT_A_SEAL_IS_A_CLAIM_NOT_A_CONSTANT`).

**ولكلِّ مجالٍ أسلوبُه، ولا يُستعار أقواها.** النظريُّ بالصوريّ، والتجريبيُّ
بفرضيّةٍ وبندٍ متوقَّعٍ وقياس، واللغويُّ بقناةٍ مختومة، والأصوليُّ ببابٍ
مرخَّصٍ ببنيانه. والبرهانُ الصوريُّ في مسألةٍ تجريبيّةٍ خطأٌ وإن صحّ شكلُه
(`A_METHOD_BORROWED_FROM_ANOTHER_DOMAIN_IS_A_SHAPED_ERROR`).

**ولا جوابَ بلا ختم.** الجوابُ الخارجُ من هذه الماشية يحمل ختمًا من جنس
`SealGenus.ANSWER_SEALED`، وأدلّتُه تُستدعى عند كلّ نداءٍ فتُصادَم؛ فإن خلا من
دليلٍ واحدٍ لم يخرج ناقصًا بل لم يخرج
(`AN_ANSWER_WITHOUT_A_SEAL_IS_NOT_EMITTED_AT_ALL`).

**وغيابُ وثائق المحكمة الأربع مقيسٌ لا مذكور.** طُلب إيداعُ `CHARTER` و
`CHAPTER-72-EPISTEME` و`CHAPTER-76-THINKING` و`FORMAL-PROOF` في
`exhibits/court-docs/`، ولم تصل بايتاتُها إلى هذه الشجرة. فغيابُها يُمسَح
بماسحٍ يحمل **شاهدَ عافية**: لا يُقبَل نفيُه حتّى يُثبت أنّه يرى وثائقَ
موجودةً بالفعل، لأنّ ماسحًا أعمى ينفي كلَّ شيء
(`A_BLIND_SCANNER_DENIES_EVERYTHING_SO_ITS_DENIAL_IS_WORTHLESS`).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from alghanem.arabic.turuq_balance import (
    BalanceRule,
    Claim,
    Weighing,
    weigh,
)
from alghanem.seals import Seal, SealGenus, SealVerdict

__all__ = [
    "AN_ANSWER_WITHOUT_A_SEAL_IS_NOT_EMITTED_AT_ALL",
    "A_BLIND_SCANNER_DENIES_EVERYTHING_SO_ITS_DENIAL_IS_WORTHLESS",
    "A_LAYER_CALLED_OUT_OF_ORDER_FORGES_A_SANAD",
    "A_METHOD_BORROWED_FROM_ANOTHER_DOMAIN_IS_A_SHAPED_ERROR",
    "A_NAME_WITHOUT_A_SEAL_IS_A_CLAIM_NOT_A_CONSTANT",
    "NO_MARKER_IS_A_REFUSAL_NOT_A_WEAK_GUESS",
    "QUESTION_CLASSIFICATION_IS_NOT_WORD_CLASSIFICATION",
    "THE_COURT_DOCUMENT_NAMES",
    "Answer",
    "Confidence",
    "ConstantLookup",
    "CourtDocumentScan",
    "Domain",
    "Method",
    "Perception",
    "PipelineError",
    "court_document_scan",
    "method_for",
    "perceive",
    "recall_constant",
    "seal_the_answer",
    "answer_question",
]

A_LAYER_CALLED_OUT_OF_ORDER_FORGES_A_SANAD: Final[str] = (
    "A_LAYER_CALLED_OUT_OF_ORDER_FORGES_A_SANAD: طبقةٌ تُستدعى قبل التي "
    "تُسلِّمها تُصدِر جوابًا يحمل ثقةً لم تُكتسَب؛ فكسرُ الترتيب تزويرُ سندٍ "
    "لا تعجُّلُ إجراء."
)

QUESTION_CLASSIFICATION_IS_NOT_WORD_CLASSIFICATION: Final[str] = (
    "QUESTION_CLASSIFICATION_IS_NOT_WORD_CLASSIFICATION: تصنيفُ السؤال إلى "
    "مجالٍ غيرُ تصنيف الكلمة إلى بابٍ صرفيّ؛ و`classification_coverage_scheme` "
    "للثاني وحدَه، فلا يُحمَّل الأوّل."
)

NO_MARKER_IS_A_REFUSAL_NOT_A_WEAK_GUESS: Final[str] = (
    "NO_MARKER_IS_A_REFUSAL_NOT_A_WEAK_GUESS: سؤالٌ لا قرينةَ فيه لا يُصنَّف "
    "تصنيفًا ضعيفًا بل لا يُصنَّف؛ والامتناعُ يُسمّى باسمه ولا يُلبَس ثوبَ "
    "حُكمٍ قليل الثقة."
)

A_NAME_WITHOUT_A_SEAL_IS_A_CLAIM_NOT_A_CONSTANT: Final[str] = (
    "A_NAME_WITHOUT_A_SEAL_IS_A_CLAIM_NOT_A_CONSTANT: اسمٌ لا ختمَ له في "
    "السجلّ يُردُّ دعوى؛ ولا يُستأنَس به في بناء جوابٍ ولا يُذكَر مؤيِّدًا."
)

A_METHOD_BORROWED_FROM_ANOTHER_DOMAIN_IS_A_SHAPED_ERROR: Final[str] = (
    "A_METHOD_BORROWED_FROM_ANOTHER_DOMAIN_IS_A_SHAPED_ERROR: أسلوبٌ "
    "يُستعار من مجالٍ إلى مجالٍ يُنتج جملةً صحيحةَ الشكل بلا فاتورة؛ "
    "والخطأُ في نوع ما بيدك أشدُّ من الخطأ في مقداره."
)

AN_ANSWER_WITHOUT_A_SEAL_IS_NOT_EMITTED_AT_ALL: Final[str] = (
    "AN_ANSWER_WITHOUT_A_SEAL_IS_NOT_EMITTED_AT_ALL: جوابٌ بلا ختمٍ لا يخرج "
    "ناقصًا بل لا يخرج؛ فالرفضُ ههنا امتناعُ إصدارٍ لا وسمُ تحذير."
)

A_BLIND_SCANNER_DENIES_EVERYTHING_SO_ITS_DENIAL_IS_WORTHLESS: Final[str] = (
    "A_BLIND_SCANNER_DENIES_EVERYTHING_SO_ITS_DENIAL_IS_WORTHLESS: ماسحٌ لا "
    "يرى شيئًا ينفي كلَّ شيء؛ فلا يُقبَل نفيُ غيابٍ حتّى يُبرز الماسحُ شاهدَ "
    "عافيةٍ يرى به موجودًا."
)


class PipelineError(ValueError):
    """رفضٌ صريحٌ في ماشية الطبقات الخمس."""


class Domain(Enum):
    """مجالاتُ السؤال الأربعة؛ والأسلوبُ تابعٌ للمجال."""

    THEORETICAL = "نظريّ"
    EMPIRICAL = "تجريبيّ"
    LINGUISTIC = "لغويّ"
    USOOLI = "أصوليّ"


class Confidence(Enum):
    """ثقةُ التصنيف مُعلَنةٌ دائمًا، ولا تصنيفَ بلا ثقة."""

    DECISIVE = "قطعيّ"
    PROXY = "وكيل"


class Method(Enum):
    """أسلوبُ الترابط، واحدٌ لكلِّ مجالٍ لا يُستعار."""

    FORMAL = "جبرٌ_صوريّ"
    HYPOTHESIS_AND_MEASURE = "فرضيةٌ_وبندٌ_متوقَّعٌ_وقياس"
    SEALED_CHANNEL = "قناةٌ_مختومة"
    LICENSED_DOOR = "بابٌ_مرخَّصٌ_ببنيانه"


_METHOD_OF_DOMAIN: Final[dict[Domain, Method]] = {
    Domain.THEORETICAL: Method.FORMAL,
    Domain.EMPIRICAL: Method.HYPOTHESIS_AND_MEASURE,
    Domain.LINGUISTIC: Method.SEALED_CHANNEL,
    Domain.USOOLI: Method.LICENSED_DOOR,
}

THE_MARKERS: Final[dict[Domain, tuple[str, ...]]] = {
    Domain.THEORETICAL: ("برهان", "استلزام", "تناقض", "بديهة"),
    Domain.EMPIRICAL: ("قياس", "عدّ", "مُودَع", "بايتات", "فرضية"),
    Domain.LINGUISTIC: ("لفظ", "حرف", "صرف", "اشتقاق", "جذر"),
    Domain.USOOLI: ("حكم", "دليل", "مناط", "علّة", "باب"),
}


@dataclass(frozen=True)
class Perception:
    """حصيلةُ الطبقة الأولى: مجالٌ مع ثقته، أو امتناعٌ مُعلَن."""

    question: str
    domain: Domain | None
    confidence: Confidence | None
    matched: tuple[str, ...]

    @property
    def is_refusal(self) -> bool:
        """أامتنع التصنيفُ لانعدام القرينة؟"""

        return self.domain is None


def perceive(question: str) -> Perception:
    """الطبقة ١: يُصنّف السؤالَ بقرائنَ مسنونةٍ ويُعلن ثقتَه أو امتناعَه."""

    if not question.strip():
        raise PipelineError("سؤالٌ خالٍ لا يُصنَّف.")
    hits = {
        domain: tuple(marker for marker in markers if marker in question)
        for domain, markers in THE_MARKERS.items()
    }
    present = {domain: found for domain, found in hits.items() if found}
    if not present:
        return Perception(
            question=question,
            domain=None,
            confidence=None,
            matched=(),
        )
    if len(present) == 1:
        domain, found = next(iter(present.items()))
        return Perception(
            question=question,
            domain=domain,
            confidence=Confidence.DECISIVE,
            matched=found,
        )
    domain = max(present, key=lambda key: (len(present[key]), key.value))
    return Perception(
        question=question,
        domain=domain,
        confidence=Confidence.PROXY,
        matched=present[domain],
    )


@dataclass(frozen=True)
class ConstantLookup:
    """حصيلةُ الطبقة ٢: ختمٌ صُودم الآن، أو ردُّ دعوى باسمها."""

    name: str
    verdict: SealVerdict | None
    refused_as_claim: bool

    @property
    def is_usable(self) -> bool:
        """أيصلح ثابتًا: له ختمٌ صُودم فلم ينزح؟"""

        if self.verdict is None:
            return False
        return not self.verdict.has_drifted


def recall_constant(name: str, seals: tuple[Seal, ...]) -> ConstantLookup:
    """الطبقة ٢: لا يُرجع قيمةً مخزونة؛ يستدعي المولِّدَ ويصادمه الآن."""

    for seal in seals:
        if seal.name == name:
            return ConstantLookup(
                name=name,
                verdict=SealVerdict(seal=seal, readings=seal.collide()),
                refused_as_claim=False,
            )
    return ConstantLookup(name=name, verdict=None, refused_as_claim=True)


def method_for(perception: Perception) -> Method:
    """الطبقة ٣: أسلوبُ المجال وحدَه، ولا يُستعار أقواها."""

    if perception.is_refusal or perception.domain is None:
        raise PipelineError(
            "لا ترابطَ قبل إدراك؛ والسؤالُ ههنا لم يُصنَّف: "
            f"{A_LAYER_CALLED_OUT_OF_ORDER_FORGES_A_SANAD}"
        )
    return _METHOD_OF_DOMAIN[perception.domain]


@dataclass(frozen=True)
class Answer:
    """جوابٌ مختوم: مجالُه وأسلوبُه وحكمُ ميزانه وأدلّتُه المصادَمة."""

    perception: Perception
    method: Method
    weighing: Weighing
    evidence: tuple[ConstantLookup, ...]
    seal_genus: SealGenus

    def __post_init__(self) -> None:
        if self.seal_genus is not SealGenus.ANSWER_SEALED:
            raise PipelineError("ختمُ الجواب جنسُه `مختومُ_جواب` ولا يُحشَر في غيره.")
        if not self.evidence:
            raise PipelineError(AN_ANSWER_WITHOUT_A_SEAL_IS_NOT_EMITTED_AT_ALL)

    @property
    def footer(self) -> str:
        """تذييلُ الجواب: بصمةُ أدلّته بأسمائها وحالها، لا بأعدادها."""

        marks = " · ".join(
            f"{item.name}:{'مصادَمٌ_فوافق' if item.is_usable else 'مردودٌ_دعوى'}"
            for item in self.evidence
        )
        return f"[{self.seal_genus.value}] {marks}"


def seal_the_answer(
    perception: Perception,
    method: Method,
    weighing: Weighing,
    evidence: tuple[ConstantLookup, ...],
) -> Answer:
    """الطبقة ٥: لا يُصدِر جوابًا إلّا بأدلّةٍ حاضرةٍ وختمٍ من جنسه."""

    if perception.is_refusal:
        raise PipelineError(NO_MARKER_IS_A_REFUSAL_NOT_A_WEAK_GUESS)
    if method is not method_for(perception):
        raise PipelineError(A_METHOD_BORROWED_FROM_ANOTHER_DOMAIN_IS_A_SHAPED_ERROR)
    usable = tuple(item for item in evidence if item.is_usable)
    if not usable:
        raise PipelineError(
            f"{A_NAME_WITHOUT_A_SEAL_IS_A_CLAIM_NOT_A_CONSTANT} — "
            f"{AN_ANSWER_WITHOUT_A_SEAL_IS_NOT_EMITTED_AT_ALL}"
        )
    return Answer(
        perception=perception,
        method=method,
        weighing=weighing,
        evidence=evidence,
        seal_genus=SealGenus.ANSWER_SEALED,
    )


def answer_question(
    question: str,
    constant_names: tuple[str, ...],
    seals: tuple[Seal, ...],
    contender: Claim,
    incumbent: Claim,
) -> Answer:
    """يمشي الطبقات الخمس بترتيبها؛ وأيُّ طبقةٍ ترفض تُوقف ما بعدها."""

    perception = perceive(question)
    if perception.is_refusal:
        raise PipelineError(NO_MARKER_IS_A_REFUSAL_NOT_A_WEAK_GUESS)
    evidence = tuple(recall_constant(name, seals) for name in constant_names)
    method = method_for(perception)
    weighing = weigh(contender, incumbent)
    if weighing.deciding_rule is BalanceRule.D0_NAMED_IS_COUNTED:
        raise PipelineError(weighing.reason)
    return seal_the_answer(perception, method, weighing, evidence)


THE_COURT_DOCUMENT_NAMES: Final[tuple[str, ...]] = (
    "CHARTER",
    "CHAPTER-72-EPISTEME",
    "CHAPTER-76-THINKING",
    "FORMAL-PROOF",
)


@dataclass(frozen=True)
class CourtDocumentScan:
    """مسحُ وثائق المحكمة: ما وُجد منها، وشاهدُ عافية الماسح."""

    present: tuple[str, ...]
    absent: tuple[str, ...]
    documents_the_scanner_did_see: int

    @property
    def scanner_is_not_blind(self) -> bool:
        """شاهدُ العافية: أرأى الماسحُ وثائقَ موجودةً بالفعل؟"""

        return self.documents_the_scanner_did_see > 0

    @property
    def absence_is_admissible(self) -> bool:
        """لا يُقبَل نفيُ الغياب من ماسحٍ لم يُثبت أنّه يرى."""

        return self.scanner_is_not_blind


def _tree_root() -> Path:
    return Path(__file__).resolve().parents[3]


def court_document_scan() -> CourtDocumentScan:
    """يمسح الشجرةَ عن الوثائق الأربع ويحمل شاهدَ عافيته معه."""

    root = _tree_root()
    seen = [
        path
        for path in root.rglob("*.md")
        if ".git" not in path.parts and path.is_file()
    ]
    stems = {path.stem.upper() for path in seen}
    present = tuple(name for name in THE_COURT_DOCUMENT_NAMES if name in stems)
    absent = tuple(name for name in THE_COURT_DOCUMENT_NAMES if name not in stems)
    return CourtDocumentScan(
        present=present,
        absent=absent,
        documents_the_scanner_did_see=len(seen),
    )


THE_DOMAIN_METHODS_ARE_ONE_TO_ONE: Final[bool] = len(
    set(_METHOD_OF_DOMAIN.values())
) == len(Domain)
