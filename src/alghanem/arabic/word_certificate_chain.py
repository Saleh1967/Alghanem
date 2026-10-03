"""سلسلةُ تسليم الشهادة: من بايتات المصدر إلى حكمٍ على الكلمة في نطاقها.

في `canonical116` شهادةٌ تُخرِج `READY`، وفي `excerpt_origin_bridge` موضعٌ
وبايتاتُه وسياقُه ومنزلةُ دعاواه. وبينهما فجوةٌ مُسمّاة: **ما الذي يُرخِّص
الكلمةَ في سياقها، وأيُّ مقدّمةٍ إن فسدت أسقطت الحكم؟** وهذه الوحدةُ تجيب
بسلسلةِ انتقالاتٍ مُشتقّةٍ عند القراءة، لكلّ انتقالٍ تسعةُ حقولٍ لا يُطوى منها
حقل.

**أوّلًا: `READY` ليس ترخيصَ الكلمة، والبصمةُ ليست صحّةَ التحليل.** فحالةُ
`canonical116` خبرٌ عن مطابقةِ بروتوكولٍ: أنّ كلّ ذرّةٍ من المئةِ والستّ عشرة،
وأنّ المصدرَ محفوظٌ يُعاد منه الاشتقاق. وليست خبرًا عن وزنٍ ولا إعرابٍ ولا
إحالة. ومن قرأها ترخيصًا نقل حكمَ طبقةٍ إلى طبقةٍ لم تُفحَص
(`A_READY_PROTOCOL_STATE_IS_NOT_A_LICENCE_OF_THE_WORD`).

**وثانيًا: الحكمُ مُشتَقٌّ لا مُستلَم.** لا يقبل المُصدِرُ من المستدعي حالةَ
«مرخَّصة» ولا قائمةَ بقايا فارغةً دليلًا؛ بل يُعيد اشتقاقَ كلّ حكمِ طبقةٍ من
مقدّماتها ومن تبعيّاتها، ويَسقُط الإجماليُّ بسقوطِ أيّ مقدّمةٍ لازمةٍ غيرِ
محسومة. وتضييقُ النطاق بعد رؤية النتيجة ممنوعٌ باسمه: النطاقُ يُعلَن قبل
القياس (`THE_SCOPE_IS_DECLARED_BEFORE_THE_MEASUREMENT_NOT_AFTER_IT`).

**وثالثًا: غيابُ الدليل ليس امتناعًا بدليل.** فالمنازلُ ثلاثٌ لا اثنتان —
مرخَّصةٌ في نطاقٍ، وممتنعةٌ بدليل، ومعلَّقةٌ بسببٍ مسمًّى — ومن حوَّل المعلَّقَ
ممتنعًا ادّعى دليلًا لا يملكه، ومن حوَّله مرخَّصًا سكت عن مقدّمةٍ لازمة
(`AN_ABSENT_EVIDENCE_IS_NOT_A_REFUTATION`).

**ورابعًا: الجذرُ والمعنى مدخلان معجميّان لا مُشتقّان من المئة والستّ عشرة.**
فالذرّاتُ تُخرِج حرفًا وحركةً، ولا تُخرِج أصليًّا من زائد، ولا تَعرِف نونَ
التنوين من نونِ الجذر. فما كان منهما مُودَعًا بشاهدٍ معجميٍّ سُمّي شاهدُه، وما
لم يُودَع بقي معلَّقًا؛ ولا يُولَّد معنًى من بنية
(`THE_ROOT_AND_THE_MEANING_ARE_LEXICAL_INPUTS_NOT_STRUCTURAL_OUTPUTS`).

**وخامسًا: نونُ التنوين ليست حرفًا من الجذر، والرسمُ المحفوظ ليس التمثيلَ
الوقفيّ.** فتنوينُ «حَيَاةٌ» نونٌ ساكنةٌ تُنطَق في الوصل وتسقط في الوقف، ولا
تدخل في «ح ي ي»؛ والتاءُ المربوطةُ تُقرأ تاءً وصلًا وهاءً وقفًا، والرسمُ واحدٌ
في الحالَين. وعلامةُ الترقيم وحدَها لا تُثبِت أداءً وقفيًّا بعينه، ولا تُختلَق
كلمةٌ لاحقةٌ لاختبار الوصل: يُختبَر على ما في البايتات لا على ما يُفترَض
(`A_PUNCTUATION_MARK_ALONE_IS_NOT_A_PAUSE_PERFORMANCE`).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Final

from .epistemic_layers import EpistemicStanding
from .excerpt_origin_bridge import (
    ClaimStanding,
    ExcerptOriginError,
    LocatedWord,
    OriginClaim,
    OriginWitness,
    WordAddress,
    locate,
    origin_readings,
)

__all__ = [
    "AN_ABSENT_EVIDENCE_IS_NOT_A_REFUTATION",
    "AnalysisSubject",
    "AnalysisWitness",
    "A_PUNCTUATION_MARK_ALONE_IS_NOT_A_PAUSE_PERFORMANCE",
    "A_READY_PROTOCOL_STATE_IS_NOT_A_LICENCE_OF_THE_WORD",
    "BoundaryReading",
    "CanonicalAdmission",
    "CertificateLayer",
    "LayerStanding",
    "LayerVerdict",
    "Premise",
    "THE_DECLARED_SCOPE",
    "THE_ROOT_AND_THE_MEANING_ARE_LEXICAL_INPUTS_NOT_STRUCTURAL_OUTPUTS",
    "THE_SCOPE_IS_DECLARED_BEFORE_THE_MEASUREMENT_NOT_AFTER_IT",
    "Transition",
    "WordCertificate",
    "WordCertificateError",
    "boundary_reading",
    "canonical_admission",
    "certify",
    "deposited_premises",
    "fingerprint",
    "layer_verdicts",
    "overall_verdict",
    "tanwin_reading",
    "the_chain",
]


class WordCertificateError(Exception):
    """خطأُ سلسلةِ الشهادة: يُرفَع باسم سببه ولا يُحوَّل حكمًا."""


A_READY_PROTOCOL_STATE_IS_NOT_A_LICENCE_OF_THE_WORD: Final[str] = (
    "حالةُ البروتوكول خبرٌ عن مطابقةِ الترميز وإعادةِ الاشتقاق، لا عن وزنٍ ولا "
    "إعرابٍ ولا إحالة؛ فلا تُقرأ ترخيصًا لطبقةٍ لم تُفحَص"
)

THE_SCOPE_IS_DECLARED_BEFORE_THE_MEASUREMENT_NOT_AFTER_IT: Final[str] = (
    "النطاقُ يُعلَن قبل القياس: فتضييقُه بعد رؤية النتيجة يُخفي تعليقًا ولا "
    "يرفعه، ويجعل الحكمَ صادقًا بتعريفه لا بدليله"
)

AN_ABSENT_EVIDENCE_IS_NOT_A_REFUTATION: Final[str] = (
    "غيابُ الدليل تعليقٌ بسببٍ مسمًّى لا امتناعٌ بدليل؛ والمنازلُ ثلاثٌ لا اثنتان"
)

THE_ROOT_AND_THE_MEANING_ARE_LEXICAL_INPUTS_NOT_STRUCTURAL_OUTPUTS: Final[str] = (
    "الوحداتُ المئةُ والستُّ عشرةَ تُخرِج حرفًا وحركة، ولا تُميّز أصليًّا من "
    "زائدٍ ولا تُولّد معنًى؛ فالجذرُ والمعنى مدخلان بشاهدٍ معجميٍّ أو معلَّقان"
)

A_PUNCTUATION_MARK_ALONE_IS_NOT_A_PAUSE_PERFORMANCE: Final[str] = (
    "علامةُ الترقيم زيادةُ ناشرٍ تحتمل الوقفَ وغيرَه، فلا تُقرأ وحدَها أداءً "
    "وقفيًّا؛ ولا تُختلَق كلمةٌ لاحقةٌ ليُختبَر بها الوصل"
)


# ----- النطاق، مُعلَنًا قبل القياس -----


@dataclass(frozen=True, slots=True)
class DeclaredScope:
    """نطاقُ الدعوى مُعلَنًا بأقسامه الثلاثة قبل أن يُقاس شيء."""

    included: tuple[str, ...]
    excluded: tuple[str, ...]
    deferred: tuple[str, ...]
    insulation: tuple[str, ...]

    def __post_init__(self) -> None:
        if not (self.included and self.excluded and self.deferred):
            raise WordCertificateError(
                "نطاقٌ ناقصُ أحدِ أقسامه لا يُعلَن: "
                f"{THE_SCOPE_IS_DECLARED_BEFORE_THE_MEASUREMENT_NOT_AFTER_IT}"
            )


THE_DECLARED_SCOPE: Final[DeclaredScope] = DeclaredScope(
    included=("نصوصٌ عربيّةٌ فصيحةٌ معياريّةٌ مشكولة، من قائمةِ مصادرَ مُحدَّدةٍ " "مؤرَّخةٍ مبصومة",),
    excluded=("المطابقةُ الصوتيّةُ المسجَّلة",),
    deferred=("غيرُ المشكول", "العامّيّ", "غيرُ المعياريّ"),
    insulation=(
        "نتائجُ القرآن تبقى مستقلّةً ولا تُرحَّل إلى الإملاء المعياريّ: فالمودَعُ "
        "المقروءُ ههنا مصحفٌ، وحكمُه حكمٌ عليه لا على كلّ نصٍّ مشكول",
    ),
)


# ----- الطبقات والمنازل -----


class CertificateLayer(Enum):
    """الطبقاتُ مفصولةٌ بأسمائها؛ ولا يُنقَل حكمُ طبقةٍ إلى أختها."""

    ENCODING = "سلامةُ الترميز والتطبيع"
    CANONICAL_ADMISSION = "قبولُ التمثيل في canonical116"
    SYLLABLE_LICENCE = "الترخيصُ المقطعيّ تحت الابتداء والوصل والوقف"
    MORPHOLOGY = "صحّةُ التحليل الصرفيّ والوزن"
    SYNTAX = "صحّةُ الوظيفة النحويّة"
    REFERENCE = "تعيينُ الإحالة والعلاقة بالسياق"


class LayerStanding(Enum):
    """منازلُ ثلاثٌ لا اثنتان، ولا رابعةَ تُخفي بها تعليقًا."""

    LICENSED_IN_SCOPE = "مرخَّصةٌ داخل نطاقٍ محدَّد"
    REFUSED_WITH_EVIDENCE = "ممتنعةٌ بدليل"
    SUSPENDED_BY_NAMED_CAUSE = "معلَّقةٌ بسببٍ مسمًّى"


# ----- المقدّمة: أربعةُ أسئلةٍ لا يُسكَت عن واحدٍ منها -----


@dataclass(frozen=True, slots=True)
class Premise:
    """مقدّمةٌ مُستدعاةٌ، ولكلٍّ أربعةُ أجوبةٍ مكتوبةٌ ومنزلةٌ وتبعيّات."""

    name: str
    layer: CertificateLayer
    why_invoked: str
    admission_evidence: str
    why_it_applies_here: str
    what_it_establishes: str
    standing: ClaimStanding
    required_for_the_claim: bool
    depends_on: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for label, value in (
            ("الاسم", self.name),
            ("لماذا استُدعيت", self.why_invoked),
            ("ما دليل قبولها", self.admission_evidence),
            ("لماذا تنطبق هنا", self.why_it_applies_here),
            ("ماذا تثبت تحديدًا", self.what_it_establishes),
        ):
            if not value.strip():
                raise WordCertificateError(
                    f"مقدّمةٌ بلا «{label}» لا تُسجَّل؛ والسكوتُ عن أحدِ الأربعة "
                    "يُخفي سندَها."
                )

    @property
    def is_settled(self) -> bool:
        """المحسومةُ ما ثبتت أو امتنعت بدليل؛ والمعلَّقةُ ليست محسومة."""

        return self.standing is not ClaimStanding.SUSPENDED

    @property
    def blocks_the_licence(self) -> bool:
        """تمنع الترخيصَ كلُّ لازمةٍ غيرِ محسومة، أو لازمةٍ ممتنعة."""

        if not self.required_for_the_claim:
            return False
        return self.standing is not ClaimStanding.ESTABLISHED


# ----- الانتقال: تسعةُ حقولٍ لا يُطوى منها حقل -----


@dataclass(frozen=True, slots=True)
class Transition:
    """انتقالٌ واحدٌ في السلسلة، مُسمّى المدخل والمخرج والمانع والبقايا."""

    station_in: str
    operation: str
    condition: str
    obstacle: str
    witness: str
    rank: EpistemicStanding
    station_out: str
    dependencies: tuple[str, ...]
    residue: tuple[str, ...]
    layer: CertificateLayer

    def __post_init__(self) -> None:
        for label, value in (
            ("مدخل", self.station_in),
            ("عملية", self.operation),
            ("شرط", self.condition),
            ("مانع", self.obstacle),
            ("شاهد", self.witness),
            ("مخرج", self.station_out),
        ):
            if not value.strip():
                raise WordCertificateError(f"انتقالٌ بلا «{label}» لا يُسجَّل.")


# ----- قراءاتٌ مقيسةٌ على البايتات -----

_HARAKAT: Final[frozenset[str]] = frozenset("\u064e\u064f\u0650\u0652")
_TANWIN: Final[dict[str, str]] = {
    "\u064b": "تنوينُ فتح",
    "\u064c": "تنوينُ ضمّ",
    "\u064d": "تنوينُ كسر",
}


@dataclass(frozen=True, slots=True)
class TanwinReading:
    """قراءةُ التنوين: أحاضرٌ هو؟ وأين موضعُه؟ وما الذي لا يُعَدّ منه جذرًا؟"""

    present: bool
    mark_name: str | None
    position: int | None
    carriers_without_the_mark: str

    @property
    def nun_is_a_root_letter(self) -> bool:
        """نونُ التنوين ليست من الجذر البتّة؛ وهذا تصريحٌ لا قياس."""

        return False


def tanwin_reading(surface: str) -> TanwinReading:
    """يقرأ التنوينَ من المحارف، ويعزل علامتَه عن حروف السطح."""

    for index, character in enumerate(surface):
        if character in _TANWIN:
            return TanwinReading(
                present=True,
                mark_name=_TANWIN[character],
                position=index,
                carriers_without_the_mark="".join(
                    one for one in surface if one not in _TANWIN
                ),
            )
    return TanwinReading(False, None, None, surface)


@dataclass(frozen=True, slots=True)
class CanonicalAdmission:
    """قبولُ التمثيل في المئة والستّ عشرة، مقيسًا بالجسر لا منقولًا عنه."""

    status: str
    replay_reproduced: bool
    atoms: tuple[str, ...]
    rasm_is_recoverable_from_the_atoms: bool
    lost_in_the_rendering: tuple[str, ...]

    @property
    def protocol_is_legal(self) -> bool:
        """شرعيّةُ البروتوكول: حالةٌ جاهزةٌ مع إعادةِ اشتقاقٍ ناجحة، لا غير."""

        return self.status == "READY" and self.replay_reproduced


def canonical_admission(surface: str) -> CanonicalAdmission:
    """يُمرّر السطحَ على جسر المئة والستّ عشرة، ويقيس ما ضاع في التصيير.

    والذرّاتُ تصييرٌ وصليّ: «ة» تُصيَّر «تُ» والتنوينُ يُصيَّر «نْ»، فلا يُستردّ
    منها الرسمُ المحفوظ. وهذا قياسٌ يُبرهن أنّ حالةَ البروتوكول ليست ترخيصَ
    الكلمة (`A_READY_PROTOCOL_STATE_IS_NOT_A_LICENCE_OF_THE_WORD`).
    """

    from canonical116.bridge import bridge, verify

    record = bridge(surface)
    atoms = tuple(record.get("canonical_atoms") or ())
    reproduced = bool(verify(record).get("reproduced"))
    rejoined = "".join(atoms)
    lost = tuple(
        sorted({one for one in surface if one not in rejoined and not one.isspace()})
    )
    return CanonicalAdmission(
        status=str(record.get("status")),
        replay_reproduced=reproduced,
        atoms=atoms,
        rasm_is_recoverable_from_the_atoms=not lost,
        lost_in_the_rendering=lost,
    )


@dataclass(frozen=True, slots=True)
class BoundaryReading:
    """حدُّ الكلمة كما تُخرجه البايتاتُ: أوّلٌ وآخِرٌ وجارٌ فعليٌّ لا مفترَض."""

    opens_the_line: bool
    closes_the_line: bool
    preceding_word: str | None
    following_word: str | None
    final_mark: str | None
    ibtida_is_readable: bool
    wasl_is_testable: bool
    waqf_is_testable: bool
    cause: str


def boundary_reading(located: LocatedWord) -> BoundaryReading:
    """يقرأ ما يُرخِّص اختبارَ الابتداء والوصل والوقف، ولا يختلق جارًا.

    فالوصلُ لا يُختبَر إلّا بوجودِ كلمةٍ تاليةٍ في البايتات، والوقفُ لا يُختبَر
    إلّا عند حدٍّ فعليّ. وعلامةُ الترقيم وحدَها لا تُقرأ أداءً وقفيًّا
    (`A_PUNCTUATION_MARK_ALONE_IS_NOT_A_PAUSE_PERFORMANCE`).
    """

    final = located.surface[-1] if located.surface else None
    opens = located.preceding_word is None
    closes = located.following_word is None
    causes: list[str] = []
    if opens:
        causes.append("أوّلُ السطر، فالابتداءُ مقروءٌ عند حدٍّ فعليّ")
    else:
        causes.append("ليس أوّلَ السطر، فالابتداءُ لا يُقاس ههنا")
    if closes:
        causes.append("لا كلمةَ تاليةً في البايتات، فالوصلُ غيرُ قابلٍ للاختبار")
    else:
        causes.append("بعده كلمةٌ في البايتات، فالوصلُ قابلٌ للاختبار")
    return BoundaryReading(
        opens_the_line=opens,
        closes_the_line=closes,
        preceding_word=located.preceding_word,
        following_word=located.following_word,
        final_mark=final if final in _HARAKAT or final in _TANWIN else None,
        ibtida_is_readable=opens,
        wasl_is_testable=not closes,
        waqf_is_testable=True,
        cause=" · ".join(causes),
    )


# ----- شاهدُ التحليل: مدخلٌ معجميٌّ أو نحويٌّ مُودَعٌ لا مولَّدٌ -----


class AnalysisSubject(Enum):
    """موضوعُ الشاهد: ما الذي يَحسِمه إن قُبِل؟"""

    ROOT_AND_WAZN = "الجذرُ والوزن"
    SYNTACTIC_FUNCTION = "الوظيفةُ النحويّة"
    REFERENT = "مرجعُ الإحالة"


@dataclass(frozen=True, slots=True)
class AnalysisWitness:
    """شاهدُ تحليلٍ مُودَع: مُسمّى المصدرِ والموضعِ والسطحِ والمنفِّذ.

    ولا يُقبَل إلّا بأربعةٍ: مصدرٌ مُسمًّى بمسارٍ نسبيّ، وسطحٌ يُطابق المقيسَ
    من البايتات، ودعوى، ومنفِّذ. فإن خالف سطحُه المقيسَ، أو غاب مصدرُه عن
    الشجرة، لم يُقبَل؛ ولا يُحوَّل ردُّه امتناعًا في موضوعه
    (`AN_ABSENT_EVIDENCE_IS_NOT_A_REFUTATION`).
    """

    subject: AnalysisSubject
    claim: str
    surface: str
    lexical_source: str
    lexical_locus: str
    examiner: str

    def __post_init__(self) -> None:
        for label, value in (
            ("الدعوى", self.claim),
            ("السطح", self.surface),
            ("المصدر", self.lexical_source),
            ("الموضع", self.lexical_locus),
            ("المنفِّذ", self.examiner),
        ):
            if not value.strip():
                raise WordCertificateError(f"شاهدُ تحليلٍ بلا «{label}» لا يُقبَل.")

    def source_is_present(self, root: Path | None = None) -> bool:
        """أحاضرٌ مصدرُ الشاهد في الشجرة؟ يُقاس من القرص لا يُصدَّق."""

        base = root if root is not None else Path(__file__).resolve().parents[3]
        return (base / self.lexical_source).is_file()

    def admits(self, surface: str, root: Path | None = None) -> bool:
        """يُقبَل إن طابق سطحُه المقيسَ وكان مصدرُه حاضرًا؛ وإلّا فلا."""

        return self.surface == surface and self.source_is_present(root)


def _witness_for(
    subject: AnalysisSubject,
    witnesses: tuple[AnalysisWitness, ...],
    surface: str,
    root: Path | None,
) -> AnalysisWitness | None:
    """أوّلُ شاهدٍ مقبولٍ في موضوعه، أو لا شيء."""

    for one in witnesses:
        if one.subject is subject and one.admits(surface, root):
            return one
    return None


def _cascade(premises: tuple[Premise, ...]) -> tuple[Premise, ...]:
    """يُبطل التابعَ وحدَه عند سقوط متبوعه، ويُبقي المستقلّ على حاله.

    فمن قامت مقدّمتُه على مقدّمةٍ لم تَثبُت لم تَثبُت هي، ولو كُتب لها ثبوت؛
    وهذا اشتقاقٌ من التبعيّات لا قبولٌ من كاتب.
    """

    by_name = {one.name: one for one in premises}
    settled_names = {
        one.name for one in premises if one.standing is ClaimStanding.ESTABLISHED
    }
    changed = True
    while changed:
        changed = False
        for premise in premises:
            if premise.name not in settled_names:
                continue
            fallen = tuple(
                one
                for one in premise.depends_on
                if one in by_name and one not in settled_names
            )
            if fallen:
                settled_names.discard(premise.name)
                changed = True
    out: list[Premise] = []
    for premise in premises:
        if premise.standing is ClaimStanding.ESTABLISHED and (
            premise.name not in settled_names
        ):
            fallen_names = " · ".join(
                one
                for one in premise.depends_on
                if one in by_name and one not in settled_names
            )
            out.append(
                Premise(
                    name=premise.name,
                    layer=premise.layer,
                    why_invoked=premise.why_invoked,
                    admission_evidence=premise.admission_evidence,
                    why_it_applies_here=premise.why_it_applies_here,
                    what_it_establishes=(
                        f"لا شيءَ بعدُ: سقط متبوعُها «{fallen_names}» فسقطت تبعًا"
                    ),
                    standing=ClaimStanding.SUSPENDED,
                    required_for_the_claim=premise.required_for_the_claim,
                    depends_on=premise.depends_on,
                )
            )
        else:
            out.append(premise)
    return tuple(out)


# ----- المقدّماتُ المُودَعة -----


def deposited_premises(
    located: LocatedWord,
    boundary: BoundaryReading,
    tanwin: TanwinReading,
    admission: CanonicalAdmission,
    origin_is_established: bool,
    analysis_witnesses: tuple[AnalysisWitness, ...] = (),
    root: Path | None = None,
) -> tuple[Premise, ...]:
    """المقدّماتُ المُستدعاةُ لهذا الموضع، كلٌّ بأجوبتها الأربعة ومنزلتها.

    وتُشتَقّ منازلُها من المقيس لا تُكتَب: فما قام عليه قياسٌ من البايتات
    ثبت، وما كان مدخلًا معجميًّا غيرَ مُودَعٍ عُلِّق باسم سببه.
    """

    settled = ClaimStanding.ESTABLISHED
    suspended = ClaimStanding.SUSPENDED
    surface = located.surface
    root_witness = _witness_for(
        AnalysisSubject.ROOT_AND_WAZN, analysis_witnesses, surface, root
    )
    syntax_witness = _witness_for(
        AnalysisSubject.SYNTACTIC_FUNCTION, analysis_witnesses, surface, root
    )
    premises: list[Premise] = [
        Premise(
            name="بايتاتُ المصدر مختومةٌ ومُعادةُ القياس",
            layer=CertificateLayer.ENCODING,
            why_invoked="لا يُقرأ موضعٌ من بايتاتٍ لا تُعرَف هويّتُها وإصدارُها",
            admission_evidence=(
                "مصادمةُ الطول والختم بالمقيس من القرص عند كلّ نداء في "
                "`excerpt_origin_bridge.source_reading`"
            ),
            why_it_applies_here=(
                f"الموضعُ «{located.address.rendered}» مقروءٌ من هذه البايتات "
                "عينِها لا من نسخةٍ منقولة"
            ),
            what_it_establishes="أنّ السطحَ المقروءَ هو ما في المصدر، لا غير",
            standing=settled,
            required_for_the_claim=True,
        ),
        Premise(
            name="الفكُّ صارمٌ وأثرُ المتسامح مقيس",
            layer=CertificateLayer.ENCODING,
            why_invoked=("الفكُّ المتسامحُ يحذف أخطاءَ الترميز صامتًا فيُفسِد الإزاحات"),
            admission_evidence=(
                "`decode_audit` يقيس ما كان المتسامحُ سيُسقطه من محارفَ ههنا"
            ),
            why_it_applies_here="الإزاحاتُ كلُّها محسوبةٌ على النصّ المفكوك صارمًا",
            what_it_establishes="أنّ خريطةَ المواضع إلى الأصل لم يُسقِط منها الفكُّ شيئًا",
            standing=settled,
            required_for_the_claim=True,
        ),
        Premise(
            name="التمثيلُ مقبولٌ في المئة والستّ عشرة",
            layer=CertificateLayer.CANONICAL_ADMISSION,
            why_invoked=("لا تُقرأ وحداتٌ وأدوارٌ من سطحٍ لم يُقبَل في جدول الذرّات"),
            admission_evidence=(
                f"الجسر: الحالةُ {admission.status} وإعادةُ الاشتقاق "
                f"{'ناجحة' if admission.replay_reproduced else 'فاشلة'}"
            ),
            why_it_applies_here=(
                f"ذرّاتُ «{located.surface}»: {' · '.join(admission.atoms)}"
            ),
            what_it_establishes=(
                "شرعيّةَ البروتوكول وحدَها — "
                f"{A_READY_PROTOCOL_STATE_IS_NOT_A_LICENCE_OF_THE_WORD}"
            ),
            standing=(
                settled if admission.protocol_is_legal else ClaimStanding.REFUTED
            ),
            required_for_the_claim=True,
            depends_on=("بايتاتُ المصدر مختومةٌ ومُعادةُ القياس",),
        ),
        Premise(
            name="الرسمُ المحفوظُ غيرُ التصيير الوصليّ",
            layer=CertificateLayer.CANONICAL_ADMISSION,
            why_invoked=("قد يُظَنّ أنّ الذرّاتِ تُعيد الرسمَ، فيُقرأ التصييرُ أصلًا"),
            admission_evidence=(
                "ما لم يُستردّ من السطح في الذرّات: "
                + (" · ".join(admission.lost_in_the_rendering) or "لا شيء")
            ),
            why_it_applies_here=(
                "الرسمُ محفوظٌ في الموضع المقروء، والذرّاتُ تصييرٌ وصليّ"
                if admission.lost_in_the_rendering
                else "لم يسقط من السطح شيءٌ في هذا التصيير"
            ),
            what_it_establishes=(
                "أنّ الرسمَ لا يُستردّ من الذرّات، فلا يُدَّعى اشتقاقُ جذرٍ " "ولا معنًى منها"
                if admission.lost_in_the_rendering
                else "أنّ التصييرَ ههنا لم يُسقِط محرفًا، وهو قياسٌ على هذا "
                "السطح لا قاعدةٌ عامّة"
            ),
            standing=settled,
            required_for_the_claim=False,
            depends_on=("التمثيلُ مقبولٌ في المئة والستّ عشرة",),
        ),
        Premise(
            name="التنوينُ معلَّمٌ ومعزولٌ عن حروف الجذر",
            layer=CertificateLayer.MORPHOLOGY,
            why_invoked=("عدُّ نون التنوين حرفًا من الجذر يُفسِد الجذرَ والوزنَ معًا"),
            admission_evidence=(
                "`tanwin_reading` يفصل علامةَ التنوين عن حوامل السطح بالمحارف"
            ),
            why_it_applies_here=(
                f"في «{located.surface}» {tanwin.mark_name or 'لا تنوين'}"
            ),
            what_it_establishes=(
                "أنّ ما بقي بعد نزع العلامة هو الحوامل، ولا يُدّعى أنّه الجذر"
            ),
            standing=settled if tanwin.present else suspended,
            required_for_the_claim=False,
        ),
        Premise(
            name="الجذرُ والوزنُ مدخلان معجميّان",
            layer=CertificateLayer.MORPHOLOGY,
            why_invoked="الدعوى تطلب جذرًا ووزنًا، وليسا في الذرّات",
            admission_evidence=(
                f"شاهدٌ معجميٌّ مُودَع: {root_witness.lexical_source} · "
                f"{root_witness.lexical_locus} · بفحص {root_witness.examiner}"
                if root_witness is not None
                else "لا شاهدَ معجميًّا مُودَعًا لهذا السطح في هذه الشجرة — "
                f"{THE_ROOT_AND_THE_MEANING_ARE_LEXICAL_INPUTS_NOT_STRUCTURAL_OUTPUTS}"
            ),
            why_it_applies_here=(
                "الحوامل المقروءةُ تحتمل أكثرَ من تقطيعٍ أصليٍّ وزائد، ولا "
                "يَحسِمها إلّا معجم"
            ),
            what_it_establishes=(
                f"الجذرَ والوزنَ بشاهدٍ مُودَع: {root_witness.claim}"
                if root_witness is not None
                else "لا شيءَ بعدُ؛ وهي مُستدعاةٌ معلَّقةٌ لا مطويّة"
            ),
            standing=settled if root_witness is not None else suspended,
            required_for_the_claim=True,
            depends_on=(
                "التنوينُ معلَّمٌ ومعزولٌ عن حروف الجذر",
                "التمثيلُ مقبولٌ في المئة والستّ عشرة",
            ),
        ),
        Premise(
            name="الوظيفةُ النحويّةُ مُثبَتةٌ بشاهد",
            layer=CertificateLayer.SYNTAX,
            why_invoked="الدعوى تطلب إعرابًا — مبتدأً أو خبرًا أو غيرَهما",
            admission_evidence=(
                f"إعرابٌ مُودَع: {syntax_witness.lexical_source} · "
                f"{syntax_witness.lexical_locus} · بفحص {syntax_witness.examiner}"
                if syntax_witness is not None
                else "لا إعرابَ مُودَعًا لهذا الموضع، والعلامةُ الظاهرةُ تحتمل " "أكثرَ من وجه"
            ),
            why_it_applies_here=(
                f"جارُ الموضع في البايتات: قبله «{boundary.preceding_word}» "
                f"وبعده «{boundary.following_word}»"
            ),
            what_it_establishes=(
                f"الوظيفةَ النحويّةَ بشاهدٍ مُودَع: {syntax_witness.claim}"
                if syntax_witness is not None
                else "لا شيءَ بعدُ؛ معلَّقةٌ حتّى يُودَع شاهدُها"
            ),
            standing=settled if syntax_witness is not None else suspended,
            required_for_the_claim=True,
            depends_on=("الجذرُ والوزنُ مدخلان معجميّان",),
        ),
        Premise(
            name="منشأُ المقتطفِ مُثبَتٌ بشهادة",
            layer=CertificateLayer.REFERENCE,
            why_invoked=(
                "الإحالةُ إلى ما قبلَ الموضعِ وما بعده لا تصحّ إن كان الموضعُ "
                "غيرَ ثابتٍ أصلًا للمقتطف"
            ),
            admission_evidence=(
                "قراءةُ الدعوى الثالثة في `origin_readings`؛ ولا تُشتَقّ من "
                "الوجدان ولا من التفرّد"
            ),
            why_it_applies_here="السياقُ خاصّةُ الموضع المُثبَت لا خاصّةُ العبارة",
            what_it_establishes=(
                "أنّ ما قبلَ الموضعِ وما بعده يُنسَب إلى هذا المقتطف"
                if origin_is_established
                else "لا شيءَ بعدُ؛ فلا يُنقَل سياقٌ إلى مقتطفٍ مجهولِ المنشأ"
            ),
            standing=settled if origin_is_established else suspended,
            required_for_the_claim=True,
            depends_on=("بايتاتُ المصدر مختومةٌ ومُعادةُ القياس",),
        ),
    ]
    if boundary.wasl_is_testable:
        premises.append(
            Premise(
                name="جارُ الوصل موجودٌ في البايتات",
                layer=CertificateLayer.SYLLABLE_LICENCE,
                why_invoked="لا يُختبَر الوصلُ بكلمةٍ مفترَضة",
                admission_evidence=(
                    f"الكلمةُ التالية «{boundary.following_word}» مقروءةٌ من "
                    "السطر نفسِه"
                ),
                why_it_applies_here=boundary.cause,
                what_it_establishes="أنّ اختبارَ الوصل يقع على جارٍ فعليّ",
                standing=settled,
                required_for_the_claim=False,
            )
        )
    else:
        premises.append(
            Premise(
                name="جارُ الوصل غائبٌ فلا يُختبَر",
                layer=CertificateLayer.SYLLABLE_LICENCE,
                why_invoked="لا يُختلَق جارٌ ليُختبَر به الوصل",
                admission_evidence="لا كلمةَ تاليةً في البايتات لهذا الموضع",
                why_it_applies_here=boundary.cause,
                what_it_establishes="امتناعَ اختبارِ الوصل ههنا، لا نفيَه في اللغة",
                standing=suspended,
                required_for_the_claim=False,
            )
        )
    premises.append(
        Premise(
            name="الأداءُ الوقفيُّ لا يُقرأ من علامةٍ وحدَها",
            layer=CertificateLayer.SYLLABLE_LICENCE,
            why_invoked="قد يُظَنّ أنّ آخِرَ السطر أو علامةَ الترقيم تُثبِت وقفًا",
            admission_evidence=A_PUNCTUATION_MARK_ALONE_IS_NOT_A_PAUSE_PERFORMANCE,
            why_it_applies_here=(
                f"الموضعُ {'يُنهي' if boundary.closes_the_line else 'لا يُنهي'} "
                "السطر، وذلك حدُّ ملفٍّ لا أداءُ قارئ"
            ),
            what_it_establishes="امتناعَ نسبةِ أداءٍ وقفيٍّ بعينه إلى هذا الموضع",
            standing=suspended,
            required_for_the_claim=False,
        )
    )
    return _cascade(tuple(premises))


# ----- السلسلة -----


def the_chain(
    located: LocatedWord,
    boundary: BoundaryReading,
    tanwin: TanwinReading,
    admission: CanonicalAdmission,
    premises: tuple[Premise, ...],
) -> tuple[Transition, ...]:
    """الانتقالاتُ من البايتات إلى حكمِ الكلمة، مُشتقّةً من المقيس لا مكتوبة."""

    by_layer: dict[CertificateLayer, list[Premise]] = {}
    for premise in premises:
        by_layer.setdefault(premise.layer, []).append(premise)

    def residue_of(layer: CertificateLayer) -> tuple[str, ...]:
        return tuple(
            f"{one.name}: {one.standing.value}"
            for one in by_layer.get(layer, ())
            if not one.is_settled
        )

    return (
        Transition(
            station_in="بايتاتُ المصدر المختومة",
            operation="فكٌّ صارمٌ بـutf-8 بعد مصادمةِ الطول والختم",
            condition="أن يُطابق المقيسُ المُعلَنَ طولًا وختمًا",
            obstacle="ختمٌ مكسورٌ أو بايتاتٌ غائبة، فلا نصَّ يُقرأ",
            witness=f"القرص: {located.address.source_key}",
            rank=EpistemicStanding.CERTAIN_BY_RECURRENT_TRANSMISSION,
            station_out="نصٌّ مفكوكٌ غيرُ مطبَّع",
            dependencies=(),
            residue=residue_of(CertificateLayer.ENCODING),
            layer=CertificateLayer.ENCODING,
        ),
        Transition(
            station_in="نصٌّ مفكوكٌ غيرُ مطبَّع",
            operation="حلُّ العنوان إلى سطرٍ وكلمةٍ ثمّ إلى إزاحةٍ ومدى",
            condition="أن يحتمل المصدرُ السطرَ والكلمةَ المطلوبَين",
            obstacle=("عنوانٌ بلا مفتاح مصدرٍ لا يُحَلّ: يُخرج في كلّ مصدرٍ مدلولًا آخَر"),
            witness=(
                f"إزاحةُ المحارف {located.char_offset} · إزاحةُ البايتات "
                f"{located.byte_offset} · المدى {located.excerpt_bounds}"
            ),
            rank=EpistemicStanding.CERTAIN_BY_RECURRENT_TRANSMISSION,
            station_out=f"رسمٌ وضبطٌ محفوظان: «{located.surface}»",
            dependencies=("بايتاتُ المصدر مختومةٌ ومُعادةُ القياس",),
            residue=(),
            layer=CertificateLayer.ENCODING,
        ),
        Transition(
            station_in=f"رسمٌ وضبطٌ محفوظان: «{located.surface}»",
            operation="قسمةُ السطح إلى حوامل وحركاتٍ بذرّات المئة والستّ عشرة",
            condition="أن تكون كلُّ ذرّةٍ من الجدول المُعلَن",
            obstacle=(
                "حالةُ البروتوكول ليست ترخيصَ الكلمة — "
                f"{A_READY_PROTOCOL_STATE_IS_NOT_A_LICENCE_OF_THE_WORD}"
            ),
            witness=(
                f"canonical116.bridge · {admission.status} · "
                f"{len(admission.atoms)} ذرّة"
            ),
            rank=EpistemicStanding.CONVENTIONAL_TRANSMITTED,
            station_out="وحداتٌ وأدوارٌ مقروءة",
            dependencies=("الفكُّ صارمٌ وأثرُ المتسامح مقيس",),
            residue=residue_of(CertificateLayer.CANONICAL_ADMISSION),
            layer=CertificateLayer.CANONICAL_ADMISSION,
        ),
        Transition(
            station_in="وحداتٌ وأدوارٌ مقروءة",
            operation="قراءةُ الحدود: أوّلُ السطر وآخِرُه والجارُ الفعليّ",
            condition="أن يُقرأ الحدُّ من البايتات لا من افتراضِ جارٍ",
            obstacle=boundary.cause,
            witness=(
                f"قبله «{boundary.preceding_word}» · بعده "
                f"«{boundary.following_word}»"
            ),
            rank=EpistemicStanding.CONVENTIONAL_TRANSMITTED,
            station_out="مقاطعُ وحدودٌ بترخيصٍ جزئيّ",
            dependencies=("وحداتٌ وأدوارٌ مقروءة",),
            residue=residue_of(CertificateLayer.SYLLABLE_LICENCE),
            layer=CertificateLayer.SYLLABLE_LICENCE,
        ),
        Transition(
            station_in="مقاطعُ وحدودٌ بترخيصٍ جزئيّ",
            operation="عزلُ علامة التنوين ثمّ طلبُ جذرٍ ووزنٍ من شاهدٍ معجميّ",
            condition="أن يُودَع شاهدٌ معجميٌّ يحسم الأصليَّ من الزائد",
            obstacle=THE_ROOT_AND_THE_MEANING_ARE_LEXICAL_INPUTS_NOT_STRUCTURAL_OUTPUTS,
            witness=(f"الحوامل بعد نزع العلامة: «{tanwin.carriers_without_the_mark}»"),
            rank=EpistemicStanding.PRESUMPTIVE_ALWAYS,
            station_out="جذعٌ وجذرٌ ووزنٌ — معلَّقةٌ بلا شاهد",
            dependencies=("مقاطعُ وحدودٌ بترخيصٍ جزئيّ",),
            residue=residue_of(CertificateLayer.MORPHOLOGY),
            layer=CertificateLayer.MORPHOLOGY,
        ),
        Transition(
            station_in="جذعٌ وجذرٌ ووزنٌ — معلَّقةٌ بلا شاهد",
            operation="طلبُ وظيفةٍ نحويّةٍ وعلاماتِ إعرابٍ بشاهدٍ مُودَع",
            condition="أن يُودَع إعرابٌ لهذا الموضع بعينه",
            obstacle="العلامةُ الظاهرةُ تحتمل أكثرَ من وجهٍ فلا تَحسِم وحدَها",
            witness=f"السطر: «{located.line_text[:48]}…»",
            rank=EpistemicStanding.PRESUMPTIVE_ALWAYS,
            station_out="علاقاتٌ نحويّة — معلَّقة",
            dependencies=("جذعٌ وجذرٌ ووزنٌ — معلَّقةٌ بلا شاهد",),
            residue=residue_of(CertificateLayer.SYNTAX),
            layer=CertificateLayer.SYNTAX,
        ),
        Transition(
            station_in="علاقاتٌ نحويّة — معلَّقة",
            operation="نسبةُ ما قبلَ الموضعِ وما بعده إلى المقتطف",
            condition="أن تُثبَت دعوى المنشأ بشهادةٍ مُسمّاةِ المنهج والمنفِّذ",
            obstacle=("وجدانُ العبارةِ وتفرُّدُها لا يُنتجان المنشأ، فلا يُنقَل سياق"),
            witness=f"سياقان مقيسان بطول {len(located.preceding_context)} محرفًا",
            rank=EpistemicStanding.PRESUMPTIVE_ALWAYS,
            station_out="حكمٌ للكلمة في نطاقها",
            dependencies=("علاقاتٌ نحويّة — معلَّقة",),
            residue=residue_of(CertificateLayer.REFERENCE),
            layer=CertificateLayer.REFERENCE,
        ),
    )


# ----- الأحكام، مُشتقّةً لا مُستلَمة -----


@dataclass(frozen=True, slots=True)
class LayerVerdict:
    """حكمُ طبقةٍ مُشتَقٌّ من مقدّماتها وتبعيّاتها، لا مُستلَمٌ من مستدعٍ."""

    layer: CertificateLayer
    standing: LayerStanding
    cause: str
    blocking_premises: tuple[str, ...]


def layer_verdicts(premises: tuple[Premise, ...]) -> tuple[LayerVerdict, ...]:
    """يشتقّ حكمَ كلّ طبقةٍ من محتوى مقدّماتها؛ ولا حقلَ يُملى عليه."""

    verdicts: list[LayerVerdict] = []
    for layer in CertificateLayer:
        own = tuple(one for one in premises if one.layer is layer)
        if not own:
            verdicts.append(
                LayerVerdict(
                    layer=layer,
                    standing=LayerStanding.SUSPENDED_BY_NAMED_CAUSE,
                    cause="لا مقدّمةَ مُستدعاةً لهذه الطبقة، فلا يُقال مرخَّصة",
                    blocking_premises=(),
                )
            )
            continue
        refuted = tuple(
            one.name for one in own if one.standing is ClaimStanding.REFUTED
        )
        blocking = tuple(one.name for one in own if one.blocks_the_licence)
        unsettled = tuple(one.name for one in own if not one.is_settled)
        if refuted:
            verdicts.append(
                LayerVerdict(
                    layer=layer,
                    standing=LayerStanding.REFUSED_WITH_EVIDENCE,
                    cause="مقدّمةٌ ممتنعةٌ بدليلٍ في هذه الطبقة",
                    blocking_premises=refuted,
                )
            )
        elif blocking or unsettled:
            verdicts.append(
                LayerVerdict(
                    layer=layer,
                    standing=LayerStanding.SUSPENDED_BY_NAMED_CAUSE,
                    cause=(
                        "مقدّمةٌ غيرُ محسومةٍ في الطبقة، لازمةً كانت أو غيرَ "
                        f"لازمة — {AN_ABSENT_EVIDENCE_IS_NOT_A_REFUTATION}"
                    ),
                    blocking_premises=blocking or unsettled,
                )
            )
        else:
            verdicts.append(
                LayerVerdict(
                    layer=layer,
                    standing=LayerStanding.LICENSED_IN_SCOPE,
                    cause=(
                        f"كلُّ لازمةٍ في هذه الطبقة مُثبَتةٌ ({len(own)} مقدّمةً)، "
                        "والترخيصُ مقيَّدٌ بالنطاق المُعلَن"
                    ),
                    blocking_premises=(),
                )
            )
    return tuple(verdicts)


def overall_verdict(
    premises: tuple[Premise, ...],
    verdicts: tuple[LayerVerdict, ...],
    transitions: tuple[Transition, ...],
) -> LayerVerdict:
    """الحكمُ الإجماليُّ مُشتَقٌّ من الثلاثة جميعًا، ولا يُستلَم من مستدعٍ.

    ويسقط بأيّ مقدّمةٍ لازمةٍ غيرِ محسومة، وبأيّ بقيّةٍ في انتقالٍ تخصّ طبقةً
    لازمة. ولا يُقرأ خلوُّ قائمةِ البقايا دليلًا: تُعاد قراءتُها من المقدّمات
    عينِها لا من دعوى المستدعي.
    """

    refused = tuple(
        one.layer.value
        for one in verdicts
        if one.standing is LayerStanding.REFUSED_WITH_EVIDENCE
    )
    blocking = tuple(one.name for one in premises if one.blocks_the_licence)
    carried = tuple(
        f"{one.layer.value}: {item}" for one in transitions for item in one.residue
    )
    if refused:
        return LayerVerdict(
            layer=CertificateLayer.REFERENCE,
            standing=LayerStanding.REFUSED_WITH_EVIDENCE,
            cause=f"طبقةٌ ممتنعةٌ بدليل: {' · '.join(refused)}",
            blocking_premises=blocking,
        )
    if blocking:
        return LayerVerdict(
            layer=CertificateLayer.REFERENCE,
            standing=LayerStanding.SUSPENDED_BY_NAMED_CAUSE,
            cause=(
                f"{len(blocking)} مقدّمةً لازمةً غيرَ محسومة، و{len(carried)} "
                "بقيّةً محمولةً في الانتقالات — "
                f"{THE_SCOPE_IS_DECLARED_BEFORE_THE_MEASUREMENT_NOT_AFTER_IT}"
            ),
            blocking_premises=blocking,
        )
    suspended_layers = tuple(
        one.layer.value
        for one in verdicts
        if one.standing is LayerStanding.SUSPENDED_BY_NAMED_CAUSE
    )
    return LayerVerdict(
        layer=CertificateLayer.REFERENCE,
        standing=LayerStanding.LICENSED_IN_SCOPE,
        cause=(
            "كلُّ مقدّمةٍ لازمةٍ مُثبَتة؛ والترخيصُ داخل النطاق المُعلَن وحدَه: "
            f"{THE_DECLARED_SCOPE.insulation[0]}. وتبقى {len(carried)} بقيّةً "
            "مُعلَنةً لا مطويّة"
            + (
                f"، وطبقاتٌ معلَّقةٌ بأسمائها: {' · '.join(suspended_layers)}"
                if suspended_layers
                else ""
            )
        ),
        blocking_premises=(),
    )


# ----- الشهادة -----


@dataclass(frozen=True, slots=True)
class WordCertificate:
    """شهادةُ كلمةٍ في سياقها: موضعٌ ومقدّماتٌ وانتقالاتٌ وأحكامٌ مشتقّة."""

    located: LocatedWord
    boundary: BoundaryReading
    tanwin: TanwinReading
    admission: CanonicalAdmission
    origin: tuple[object, ...]
    premises: tuple[Premise, ...]
    transitions: tuple[Transition, ...]
    verdicts: tuple[LayerVerdict, ...]
    overall: LayerVerdict
    scope: DeclaredScope = field(default=THE_DECLARED_SCOPE)

    @property
    def is_licensed(self) -> bool:
        """مرخَّصةٌ إجمالًا؟ مُشتَقٌّ من الحكم الإجماليّ لا حقلٌ يُكتَب."""

        return self.overall.standing is LayerStanding.LICENSED_IN_SCOPE


def certify(
    address: WordAddress,
    *,
    witnesses: tuple[OriginWitness, ...] = (),
    analysis_witnesses: tuple[AnalysisWitness, ...] = (),
    root: Path | None = None,
    standing_from_caller: object = None,
) -> WordCertificate:
    """يُصدِر شهادةَ موضعٍ باشتقاقِ كلّ حكمٍ فيها من البايتات والمقدّمات.

    ولا يقبل من المستدعي حالةً جاهزة: `standing_from_caller` مُعلَنٌ ليُرَدّ
    صراحةً، لا ليُقرأ. فمن مرّر حالةً رُفِع له خطأٌ باسم القاعدة، ولم تُبتلَع
    دعواه صامتةً (`THE_ISSUER_DERIVES_AND_NEVER_ACCEPTS_A_SUPPLIED_STANDING`).
    """

    if standing_from_caller is not None:
        raise WordCertificateError(
            "لا يقبل المُصدِرُ حالةً من المستدعي: الحكمُ يُشتَقّ من فحوص "
            "المحتوى وصلاحيةِ القواعد والتبعيّات."
        )
    located = locate(address, root)
    readings = origin_readings(located.surface, witnesses=witnesses, root=root)
    origin_established = any(
        one.claim is OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT and one.is_established
        for one in readings
    )
    boundary = boundary_reading(located)
    tanwin = tanwin_reading(located.surface)
    admission = canonical_admission(located.surface)
    premises = deposited_premises(
        located,
        boundary,
        tanwin,
        admission,
        origin_established,
        analysis_witnesses,
        root,
    )
    transitions = the_chain(located, boundary, tanwin, admission, premises)
    verdicts = layer_verdicts(premises)
    return WordCertificate(
        located=located,
        boundary=boundary,
        tanwin=tanwin,
        admission=admission,
        origin=tuple(readings),
        premises=premises,
        transitions=transitions,
        verdicts=verdicts,
        overall=overall_verdict(premises, verdicts, transitions),
    )


def fingerprint(certificate: WordCertificate) -> str:
    """بصمةُ الشهادة، مأخوذةٌ من محتواها المُشتَقّ لا من حقلٍ مخزون.

    فتُعاد من الشهادةِ عينِها كلَّ مرّة؛ ومن حرَّف سطحًا أو إزاحةً أو منزلةَ
    مقدّمةٍ تحرّكت بصمتُه. وهي شاهدُ عدمِ التحريف لا شاهدُ صحّةِ التحليل
    (`A_READY_PROTOCOL_STATE_IS_NOT_A_LICENCE_OF_THE_WORD`).
    """

    located = certificate.located
    rows: list[str] = [
        located.address.rendered,
        located.surface,
        f"{located.char_offset}:{located.char_length}",
        f"{located.byte_offset}:{located.byte_length}",
        certificate.admission.status,
        "".join(certificate.admission.atoms),
        certificate.overall.standing.value,
    ]
    rows.extend(f"{one.name}={one.standing.value}" for one in certificate.premises)
    rows.extend(
        f"{one.layer.value}={one.standing.value}" for one in certificate.verdicts
    )
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


THE_ISSUER_DERIVES_AND_NEVER_ACCEPTS_A_SUPPLIED_STANDING: Final[str] = (
    "المُصدِرُ يشتقّ حكمَه من المقدّمات والتبعيّات، ويَرُدّ أيَّ حالةٍ يمرّرها "
    "المستدعي؛ فقائمةُ بقايا فارغةٍ من غيره ليست دليلًا"
)

_ = ExcerptOriginError
