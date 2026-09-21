r"""شهادةُ هُويّة المسقط قبل أيِّ إغلاقٍ احتماليّ: أليافٌ، وأربعةُ مواقف، وترخيصٌ مكتوب.

أُودِع في `carrier_projection_deposit` **مَن الحوامل، وأين تنتهي الكلمة، وما
الحافة**. وبقي بعده سؤالٌ لا تجيب عنه تلك الوديعة: **ما الذي فقدَه الإسقاط،
وبأيِّ إذن؟** وهذه الوحدةُ تجيب عنه بشهادةٍ مشتقّةٍ عند القراءة، ولا تفتح
طبقةَ الاحتمال ولا تقترب منها.

**أوّلًا: والترتيبُ حدٌّ ثمّ طَيّ، لا طَيٌّ ثمّ حدّ.** المسقطُ المكتوبُ ههنا:

\[
RawText \xrightarrow{B} WrittenWords \xrightarrow{\Pi_F} CarrierWords
\xrightarrow{A} Adjacency \xrightarrow{P} Probability
\]

فالحدُّ \(B\) أوّلًا، ثمّ الطَّيُّ \(\Pi_F\) على الكلمة المكتوبة. ولمّا كان
في الشجرة عمليّتان — طَيُّ مجرى الحروف \(F_s\) وطَيُّ الكلمة \(F_w\) — لم
يُترَك توافقُهما افتراضًا مطويًّا، بل يُقاس على الوديعتَين بالحدَّين جميعًا:

\[
B(F_s(T)) = \operatorname{map}(F_w, B(T))
\]

فلمّا قيس لم يصحّ في كلّ حال، وهذا هو الكسب:

| الوديعة | الحدّ | أيتوافقان؟ |
|---|---|---|
| الفاتحة | كلُّ بياض | نعم |
| الفاتحة | فراغٌ وحدَه | **لا** |
| آيةُ الفتح | كلُّ بياض | نعم |
| آيةُ الفتح | فراغٌ وحدَه | نعم |

والعلّةُ مقيسةٌ لا موصوفة: فاصلُ آيات الفاتحة سطرٌ جديد، والمسقطُ يُسقِطه
لأنّه ليس حاملًا، وقاعدةُ «ما بين فراغَين» لا تأكله. فإن طُوي المجرى أوّلًا
بقي السطرُ داخل الكلمة، وإن قُسمت الكلمةُ أوّلًا سقط من داخلها — فاختلف
الطرفان. فالتوافقُ مشروطٌ بأن **يستهلك الحدُّ كلَّ بياضٍ يُسقِطه الطَّيّ**،
ولا شهادةَ تُصدَر حيث لا توافق. وهذا الحدُّ بعينه هو الذي اختلق ستَّ حوافَ
في الوديعة السابقة؛ فكسرُه ههنا خبرٌ ثانٍ عنه لا تكرارٌ للأوّل
(`THE_COMMUTATION_HOLDS_ONLY_WHERE_THE_BOUNDARY_EATS_THE_DISCARDED_SPACE`).

**وثانيًا: والالتقاءُ لِيفٌ لا زوج.** لا يُعَدُّ المحفوظُ والملتقي عدًّا
ثنائيًّا، بل تُبنى فئاتُ التكافؤ:

\[
[w]_\Pi = \{w' : \Pi(w') = \Pi(w)\}
\]

فما كان حجمُه واحدًا فتمييزٌ محفوظ، وما زاد فمجموعةُ التقاء. وتُشتَقُّ
الأعدادُ من الألياف لا تُكتَب:

\[
N_{written} = \sum_{f} |f| ,\qquad
N_{skeleton} = |Fibers| ,\qquad
Loss = \sum_{f} (|f| - 1)
\]

وعلى آية الفتح: \(50 - 47 = 3\). وهذا الحسابُ لا يفترض أنّ الالتقاء زوجٌ
أبدًا؛ فلو التقت أربعُ كلماتٍ في هيكلٍ واحدٍ لصحّ بلا تعديل
(`THE_COLLAPSE_IS_A_FIBER_NOT_A_PAIR`).

**وثالثًا: والطَّيُّ المُعلَنُ ليس ترخيصًا.** أن تكون قاعدةُ الطَّيِّ مكتوبةً
يُثبِت أنّ التحويلَ **مُعلَن**، ولا يُثبِت أنّ فقدَ التمييز **مأذونٌ فيه**:

\[
DeclaredFold \neq LicensedCollapse
\]

فالآليّةُ تُوصَف في `CollapseMechanism` — طَيٌّ مُعلَن، أو بقيّةٌ مُسقَطة، أو
هما — والموقفُ يُؤخَذ من `THE_LICENSE_REGISTER` وحدَه، وهو **سجلٌّ مكتوبٌ
فارغٌ في هذه الوديعة**. فلا التقاءَ ههنا مرخَّصٌ ألبتّة، والثلاثةُ في آية
الفتح — `اللَّهُ/اللَّهِ` و`الْكُفَّارَ/الْكُفَّارِ` و`مِنَ/مِنْ` — كلُّها
**تمييزٌ غيرُ محلول** لا التقاءٌ مأذونٌ فيه
(`A_DECLARED_FOLD_IS_A_MECHANISM_AND_NOT_A_LICENSE`).

**ورابعًا: والمحوُ الهادمُ يحتاج شاهدًا مربوطًا بالموضع.** لا يكفي أن تُوجَد
في الشجرة طبقةٌ أخرى تحسم التمييزَ حتى يُسمّى الالتقاءُ هدمًا؛ بل يُشترَط
شاهدٌ مُودَعٌ مستقلٌّ مربوطٌ بعين الوديعة وعين موضع الوقوع
(`DestructionWitness`). وسجلُّ الشهود **فارغٌ في هذه الوديعة**، فلا موقفَ
`DESTRUCTIVE_COLLAPSE` واحدٌ ههنا، وهذا خبرٌ عن بيّنتنا لا عن اللغة
(`NO_DESTRUCTIVE_COLLAPSE_WITHOUT_AN_OCCURRENCE_ALIGNED_WITNESS`).

**وخامسًا: والنقلُ ينفي شهادةً ولا يُثبِت مَوطِنًا.** الفئاتُ العشرُ التي
تنتقل هندسةً عبر الودائع الخطّيّة الثلاث تجمع حواملَ يفرّقها المسقط. فالتمييزُ
بين `ب` و`ت`، وبين `د` و`ذ`، ونظائرُهما **لا يُشهَد له بأنّه ثباتُ حامل**.
ولا يُقال إنّه «خاصّيّةُ موضعٍ أو خطّ»، فإنّ فشلَ النقل قد يكون من القياس أو
التفاعل أو قصور الشاهد:

\[
\neg Transport(x) \Rightarrow \neg CertifiedCarrierInvariant(x)
\]

\[
\neg Transport(x) \Rightarrow PositionProperty(x) \lor FontProperty(x)
\]

وللطَّيِّ نفسِه أثرٌ ههنا يُنشَر: هو ينقل موضعَ الشكّ فيضمّ `ة` إلى `ت` فتصير
`ت/ه` غيرَ مشهودٍ لها، ويضمّ `ؤ` إلى `ء` فتصير `ء/و` كذلك
(`A_PROPERTY_THAT_DOES_NOT_TRANSPORT_IS_NOT_CERTIFIED_AS_A_CARRIER_INVARIANT`).

**وسادسًا: ولا حالةَ ماركوف بلا شهادة، ولا ثباتَ من صُنع المسقط.** قانونان
مكتوبان: أن لا يُبنى فضاءُ حالاتٍ احتماليٌّ على مسقطٍ بلا شهادةِ هُويّة
(`NO_MARKOV_STATE_WITHOUT_A_PROJECTION_IDENTITY_CERTIFICATE`)، وأن لا يُدَّعى
ثباتٌ إحصائيٌّ مصدرُه ثباتٌ صنعه الإسقاطُ نفسُه — وبيّنتُه مقيسةٌ: ثلاثُ
كلماتٍ تتكرّر مكتوبةً في آية الفتح وخمسةُ هياكل تتكرّر بعد الإسقاط
(`NO_STATISTICAL_INVARIANCE_CLAIM_FROM_AN_INVARIANCE_THE_PROJECTION_ITSELF_MADE`).

**وسابعًا: والجوارُ المرصودُ ثلاثةُ أشياءَ لا شيءٌ واحد.** يُجمَّد ههنا فرقٌ
لا يُخلَط بعدَه:

\[
Observed\ adjacency \neq linguistic\ relation \neq probabilistic\ transition
\]

(`OBSERVED_ADJACENCY_IS_NOT_A_LINGUISTIC_RELATION_NOR_A_PROBABILISTIC_TRANSITION`).

**وثامنًا: ونطاقُ الشهادة مكتوبٌ فيها.** لا تُصدَر شهادةٌ إلّا على وديعةٍ
مسمّاةٍ بحدٍّ مذكور، والنطاقُ كلُّه وديعتان مجموعُهما ثلاثٌ وثمانون كلمة.
و`scope_rank` رتبةٌ **محلّيّةٌ مُعلَنةٌ في هذه الوحدة** لا تُوصَل بـ
`readiness_rank` ولا بسلطةٍ في النواة
(`THE_CERTIFICATE_IS_ISSUED_OVER_TWO_DEPOSITS_OF_EIGHTY_THREE_WORDS`).
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass, fields
from enum import Enum
from functools import cache
from typing import Final

from alghanem.arabic.carrier_projection_deposit import (
    THE_DEPOSITS_PROJECTED,
    THE_FOLDING,
    WordBoundary,
    census_of,
    deposited_text,
    project_letter,
    project_word,
    the_twenty_nine,
    words_of,
)
from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_ID
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID

__all__ = [
    "A_DECLARED_FOLD_IS_A_MECHANISM_AND_NOT_A_LICENSE",
    "A_PROPERTY_THAT_DOES_NOT_TRANSPORT_IS_NOT_CERTIFIED_AS_A_CARRIER_INVARIANT",
    "NO_DESTRUCTIVE_COLLAPSE_WITHOUT_AN_OCCURRENCE_ALIGNED_WITNESS",
    "NO_MARKOV_STATE_WITHOUT_A_PROJECTION_IDENTITY_CERTIFICATE",
    "NO_STATISTICAL_INVARIANCE_CLAIM_FROM_AN_INVARIANCE_THE_PROJECTION_ITSELF_MADE",
    "OBSERVED_ADJACENCY_IS_NOT_A_LINGUISTIC_RELATION_NOR_A_PROBABILISTIC_TRANSITION",
    "PROJECTION_IDENTITY_NAMED_RESIDUALS",
    "THE_CERTIFICATE_IS_ISSUED_OVER_TWO_DEPOSITS_OF_EIGHTY_THREE_WORDS",
    "THE_COLLAPSE_IS_A_FIBER_NOT_A_PAIR",
    "THE_DESTRUCTION_WITNESSES",
    "THE_COMMUTATION_HOLDS_ONLY_WHERE_THE_BOUNDARY_EATS_THE_DISCARDED_SPACE",
    "THE_LICENSE_REGISTER",
    "THE_ORDER",
    "THE_SCOPE_RANK",
    "CollapseLicense",
    "CollapseMechanism",
    "CollapseStanding",
    "DestructionWitness",
    "ProjectionCertificate",
    "ProjectionFiber",
    "ProjectionIdentityError",
    "StandingFinding",
    "carriers_a_deposit_writes",
    "certificate_of",
    "fibers_of",
    "fold_rule_digest",
    "fold_stream",
    "the_commutation_table",
    "the_fold_and_the_boundary_commute_on",
    "uncertified_carrier_distinctions",
]


class ProjectionIdentityError(ValueError):
    """رفضٌ عند الشهادة: ليفٌ لا يُشتقّ، أو موقفٌ بلا سند، أو نطاقٌ لا يُقرأ."""


# --- البقايا المسمّاة ------------------------------------------------------

THE_COMMUTATION_HOLDS_ONLY_WHERE_THE_BOUNDARY_EATS_THE_DISCARDED_SPACE: Final[str] = (
    "THE_COMMUTATION_HOLDS_ONLY_WHERE_THE_BOUNDARY_EATS_THE_DISCARDED_SPACE: "
    "توافقُ الطَّيِّ وحدِّ الكلمة مقيسٌ على الوديعتَين بالحدَّين لا مأخوذٌ "
    "تسليمًا، وقد انكسر في واحدةٍ من أربع: الفاتحةُ بحدِّ الفراغ وحدَه، إذ "
    "يُسقِط الطَّيُّ سطرَها الجديدَ ولا يأكله ذلك الحدُّ فيبقى داخل الكلمة "
    "إن طُوي المجرى أوّلًا؛ فلا شهادةَ تُصدَر حيث لا توافق"
)

THE_COLLAPSE_IS_A_FIBER_NOT_A_PAIR: Final[str] = (
    "THE_COLLAPSE_IS_A_FIBER_NOT_A_PAIR: المحفوظُ والملتقي مشتقّان من فئات "
    "التكافؤ لا من عدٍّ ثنائيّ؛ فالخسارةُ مجموعُ حجومِ الألياف ناقصةً عددَها، "
    "ويصحّ هذا الحسابُ ولو التقت أربعُ كلماتٍ في هيكلٍ واحد"
)

A_DECLARED_FOLD_IS_A_MECHANISM_AND_NOT_A_LICENSE: Final[str] = (
    "A_DECLARED_FOLD_IS_A_MECHANISM_AND_NOT_A_LICENSE: كونُ قاعدة الطَّيِّ "
    "مكتوبةً يُثبِت أنّ التحويل مُعلَن ولا يُثبِت أنّ فقدَ التمييز مأذونٌ "
    "فيه؛ فالترخيصُ لا يُؤخَذ إلّا من سجلٍّ مكتوب، وهو فارغٌ في هذه الوديعة "
    "فلا التقاءَ ههنا مرخَّص"
)

NO_DESTRUCTIVE_COLLAPSE_WITHOUT_AN_OCCURRENCE_ALIGNED_WITNESS: Final[str] = (
    "NO_DESTRUCTIVE_COLLAPSE_WITHOUT_AN_OCCURRENCE_ALIGNED_WITNESS: لا يُسمّى "
    "الالتقاءُ هدمًا لمجرّد وجودِ طبقةٍ أخرى في الشجرة، بل بشاهدٍ مُودَعٍ "
    "مستقلٍّ مربوطٍ بعين الوديعة وعين موضع الوقوع؛ وسجلُّ الشهود فارغٌ ههنا "
    "فيبقى كلُّ التقاءٍ تمييزًا غيرَ محلول"
)

A_PROPERTY_THAT_DOES_NOT_TRANSPORT_IS_NOT_CERTIFIED_AS_A_CARRIER_INVARIANT: Final[
    str
] = (
    "A_PROPERTY_THAT_DOES_NOT_TRANSPORT_IS_NOT_CERTIFIED_AS_A_CARRIER_INVARIANT: "
    "فشلُ النقل يمنع الشهادةَ ولا يُثبِت موطنًا؛ فلا يُقال إنّ الخاصّيّة "
    "خاصّيّةُ موضعٍ أو خطّ، إذ قد يكون الفشلُ من القياس أو التفاعل أو قصور "
    "الشاهد، وإنّما يُرفَع عنها وصفُ ثباتِ الحامل لا غير"
)

NO_MARKOV_STATE_WITHOUT_A_PROJECTION_IDENTITY_CERTIFICATE: Final[str] = (
    "NO_MARKOV_STATE_WITHOUT_A_PROJECTION_IDENTITY_CERTIFICATE: لا يُبنى فضاءُ "
    "حالاتٍ احتماليٌّ على مسقطٍ لم تُصدَر له شهادةُ هُويّةٍ تُسمّي مصدرَه "
    "وطَيَّه وحدَّه وأليافَه وخسارتَه وبقيّتَه ونطاقَه؛ وهذه الوحدةُ أرضُ "
    "السلسلة لا السلسلة"
)

NO_STATISTICAL_INVARIANCE_CLAIM_FROM_AN_INVARIANCE_THE_PROJECTION_ITSELF_MADE: Final[
    str
] = (
    "NO_STATISTICAL_INVARIANCE_CLAIM_FROM_AN_INVARIANCE_THE_PROJECTION_ITSELF_MADE: "
    "ثلاثُ كلماتٍ تتكرّر مكتوبةً في آية الفتح وخمسةُ هياكلَ تتكرّر بعد "
    "الإسقاط، وخمسون كلمةً متمايزةً تصير سبعةً وأربعين هيكلًا؛ فالانتظامُ قد "
    "يكون صنيعَ المسقط، ولا يُنتزَع منه ادّعاءُ ثباتٍ إحصائيّ"
)

OBSERVED_ADJACENCY_IS_NOT_A_LINGUISTIC_RELATION_NOR_A_PROBABILISTIC_TRANSITION: Final[
    str
] = (
    "OBSERVED_ADJACENCY_IS_NOT_A_LINGUISTIC_RELATION_NOR_A_PROBABILISTIC_TRANSITION: "
    "الحافةُ المشهودةُ جوارٌ مرصودٌ تحت طَيٍّ وحدٍّ معلنَين؛ لا يُقال إنّها "
    "وحدةٌ لغويّة، ولا إنّ لها قوّةً سببيّة، ولا إنّها انتقالُ حالةٍ بالمعنى "
    "الاحتماليّ، والثلاثةُ لا تُخلَط"
)

THE_CERTIFICATE_IS_ISSUED_OVER_TWO_DEPOSITS_OF_EIGHTY_THREE_WORDS: Final[str] = (
    "THE_CERTIFICATE_IS_ISSUED_OVER_TWO_DEPOSITS_OF_EIGHTY_THREE_WORDS: نطاقُ "
    "كلّ شهادةٍ ههنا وديعتان مجموعُهما ثلاثٌ وثمانون كلمة، ورتبتُها محلّيّةٌ "
    "مُعلَنةٌ في هذه الوحدة لا تُوصَل برتبة جاهزيّةٍ ولا بسلطةٍ في النواة؛ "
    "وتوسيعُ العيّنة عملٌ مستقلٌّ لا يُخلَط بصحّة العقد"
)

PROJECTION_IDENTITY_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_COMMUTATION_HOLDS_ONLY_WHERE_THE_BOUNDARY_EATS_THE_DISCARDED_SPACE": (
        THE_COMMUTATION_HOLDS_ONLY_WHERE_THE_BOUNDARY_EATS_THE_DISCARDED_SPACE
    ),
    "THE_COLLAPSE_IS_A_FIBER_NOT_A_PAIR": THE_COLLAPSE_IS_A_FIBER_NOT_A_PAIR,
    "A_DECLARED_FOLD_IS_A_MECHANISM_AND_NOT_A_LICENSE": (
        A_DECLARED_FOLD_IS_A_MECHANISM_AND_NOT_A_LICENSE
    ),
    "NO_DESTRUCTIVE_COLLAPSE_WITHOUT_AN_OCCURRENCE_ALIGNED_WITNESS": (
        NO_DESTRUCTIVE_COLLAPSE_WITHOUT_AN_OCCURRENCE_ALIGNED_WITNESS
    ),
    "A_PROPERTY_THAT_DOES_NOT_TRANSPORT_IS_NOT_CERTIFIED_AS_A_CARRIER_INVARIANT": (
        A_PROPERTY_THAT_DOES_NOT_TRANSPORT_IS_NOT_CERTIFIED_AS_A_CARRIER_INVARIANT
    ),
    "NO_MARKOV_STATE_WITHOUT_A_PROJECTION_IDENTITY_CERTIFICATE": (
        NO_MARKOV_STATE_WITHOUT_A_PROJECTION_IDENTITY_CERTIFICATE
    ),
    (
        "NO_STATISTICAL_INVARIANCE_CLAIM_FROM_AN_INVARIANCE_"
        "THE_PROJECTION_ITSELF_MADE"
    ): (NO_STATISTICAL_INVARIANCE_CLAIM_FROM_AN_INVARIANCE_THE_PROJECTION_ITSELF_MADE),
    (
        "OBSERVED_ADJACENCY_IS_NOT_A_LINGUISTIC_RELATION_NOR_A_"
        "PROBABILISTIC_TRANSITION"
    ): (OBSERVED_ADJACENCY_IS_NOT_A_LINGUISTIC_RELATION_NOR_A_PROBABILISTIC_TRANSITION),
    "THE_CERTIFICATE_IS_ISSUED_OVER_TWO_DEPOSITS_OF_EIGHTY_THREE_WORDS": (
        THE_CERTIFICATE_IS_ISSUED_OVER_TWO_DEPOSITS_OF_EIGHTY_THREE_WORDS
    ),
}


# --- الترتيب والنطاق -------------------------------------------------------

THE_ORDER: Final[tuple[str, ...]] = (
    "B: boundary over raw text",
    "F: fold each written word into carriers",
    "A: within-word adjacency",
)
"""خطواتُ المسقط على ترتيبها؛ وليس فيها خطوةُ احتمالٍ ولا تُضاف ههنا."""

THE_SCOPE_RANK: Final[str] = "two-deposits-eighty-three-words"
"""رتبةٌ محلّيّةٌ مُعلَنة؛ اسمٌ لنطاقِ البيّنة لا سلطةٌ تُنقَل إلى غير هذه الوحدة."""


# --- الطَّيُّ مجرًى وكلمةً ---------------------------------------------------


def fold_rule_digest() -> str:
    """بصمةُ جدولِ الطَّيِّ المُودَع؛ تُكتَب في الشهادة فلا ينزاح الجدولُ صامتًا."""

    written = "".join(
        f"{source}->{target};" for source, target in sorted(THE_FOLDING.items())
    )
    return hashlib.sha256(written.encode("utf-8")).hexdigest()


def fold_stream(text: str) -> str:
    """طَيُّ المجرى \\(F_s\\): حواملُ النصّ على ترتيبها، والبياضُ محفوظٌ كما هو."""

    kept: list[str] = []
    for character in text:
        if character.isspace():
            kept.append(character)
            continue
        carrier = project_letter(character)
        if carrier is not None:
            kept.append(carrier)
    return "".join(kept)


def the_fold_and_the_boundary_commute_on(
    source_id: str, boundary: WordBoundary
) -> bool:
    """أيتوافق \\(B \\circ F_s\\) مع \\(map(F_w) \\circ B\\) على وديعةٍ بحدّ؟"""

    text = deposited_text(source_id)
    folded_first = words_of(fold_stream(text), boundary)
    bounded_first = tuple(
        skeleton for skeleton in map(project_word, words_of(text, boundary)) if skeleton
    )
    return folded_first == bounded_first


@cache
def the_commutation_table() -> dict[tuple[str, WordBoundary], bool]:
    """جدولُ التوافق على الوديعتَين بالحدَّين جميعًا؛ مقيسٌ عند القراءة."""

    return {
        (source_id, boundary): the_fold_and_the_boundary_commute_on(source_id, boundary)
        for source_id in THE_DEPOSITS_PROJECTED
        for boundary in WordBoundary
    }


def carriers_a_deposit_writes(source_id: str) -> tuple[str, ...]:
    """ما وقع من الحوامل في الوديعة بعد الطَّيّ، مرتَّبًا؛ عددٌ لا حكم."""

    return tuple(sorted(set(fold_stream(deposited_text(source_id))) - {" ", "\n"}))


def _unfolded_carriers(word: str) -> str:
    """حواملُ الكلمة **قبل** الطَّيّ؛ بها يُعرَف أنّ الطَّيَّ شارك في الالتقاء."""

    return "".join(
        character for character in word if project_letter(character) is not None
    )


def _discarded_residue(word: str) -> str:
    """ما أسقطه المسقطُ من الكلمة؛ بها يُعرَف أنّ البقيّةَ شاركت في الالتقاء."""

    return "".join(
        character
        for character in word
        if not character.isspace() and project_letter(character) is None
    )


# --- الألياف ---------------------------------------------------------------


@dataclass(frozen=True)
class ProjectionFiber:
    """ليفُ هيكلٍ واحد: ما اجتمع تحته من كلماتٍ مكتوبةٍ ومواضعِ وقوعها."""

    skeleton: str
    written: tuple[str, ...]
    occurrences: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.written:
            raise ProjectionIdentityError("ليفٌ بلا كلمةٍ مكتوبة؛ والمسقطُ لا يخلق.")
        if tuple(sorted(self.written)) != self.written:
            raise ProjectionIdentityError("كلماتُ الليف غيرُ مرتَّبة؛ فالليفُ غيرُ قارّ.")
        if len(set(self.written)) != len(self.written):
            raise ProjectionIdentityError("كلمةٌ مكرَّرةٌ في ليف؛ والليفُ فئةٌ لا قائمة.")
        for word in self.written:
            if project_word(word) != self.skeleton:
                raise ProjectionIdentityError(
                    f"كلمةٌ في ليفٍ ليست منه: {word!r} لا تُسقَط إلى {self.skeleton!r}."
                )
        if not self.occurrences:
            raise ProjectionIdentityError("ليفٌ بلا موضعِ وقوع؛ ولا شهادةَ بلا موضع.")
        if tuple(sorted(self.occurrences)) != self.occurrences:
            raise ProjectionIdentityError("مواضعُ الوقوع غيرُ مرتَّبة.")

    @property
    def size(self) -> int:
        """عددُ الكلمات المكتوبة المتمايزة في الليف."""

        return len(self.written)

    @property
    def is_preserved(self) -> bool:
        """أليفٌ مفردٌ؟ فإن كان فالتمييزُ محفوظٌ ولم يُفقَد شيء."""

        return self.size == 1


@cache
def fibers_of(source_id: str, boundary: WordBoundary) -> tuple[ProjectionFiber, ...]:
    """ألياف \\(\\Pi\\) على وديعةٍ بحدٍّ معيَّن، مرتَّبةً بهياكلها."""

    words = words_of(deposited_text(source_id), boundary)
    gathered: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    for index, word in enumerate(words):
        skeleton = project_word(word)
        if not skeleton:
            raise ProjectionIdentityError(
                f"كلمةٌ بلا حاملٍ في {source_id!r} عند الموضع {index}؛ فالليفُ يخلو."
            )
        gathered[skeleton][word].append(index)
    return tuple(
        ProjectionFiber(
            skeleton=skeleton,
            written=tuple(sorted(members)),
            occurrences=tuple(
                sorted(index for places in members.values() for index in places)
            ),
        )
        for skeleton, members in sorted(gathered.items())
    )


# --- المواقفُ الأربعة ------------------------------------------------------


class CollapseStanding(Enum):
    """مواقفُ التمييز الأربعة؛ وهي مواقفُ سندٍ لا أوصافُ آليّة."""

    PRESERVED_DISTINCTION = "preserved-distinction"
    LICENSED_COLLAPSE = "licensed-collapse"
    UNRESOLVED_DISTINCTION = "unresolved-distinction"
    DESTRUCTIVE_COLLAPSE = "destructive-collapse"


class CollapseMechanism(Enum):
    """آليّةُ الالتقاء؛ تصف كيف وقع ولا تُرخّصه ألبتّة."""

    NONE = "none"
    DECLARED_FOLD = "declared-fold"
    DISCARDED_RESIDUE = "discarded-residue"
    MIXED = "mixed"


@dataclass(frozen=True)
class CollapseLicense:
    """إذنٌ مكتوبٌ بفقدِ تمييزٍ بعينه في وديعةٍ بعينها؛ ولا ترخيصَ بغيره."""

    source_id: str
    skeleton: str
    written: tuple[str, ...]
    ground: str

    def __post_init__(self) -> None:
        if not self.ground.strip():
            raise ProjectionIdentityError("ترخيصٌ بلا سندٍ مكتوب؛ فلا يُقرأ إذنًا.")
        if len(self.written) < 2:
            raise ProjectionIdentityError("ترخيصٌ لِما لم يلتقِ؛ والمفردُ لا يُرخَّص.")


@dataclass(frozen=True)
class DestructionWitness:
    """شاهدٌ مستقلٌّ مربوطٌ بعين الوديعة وعين الموضع على تمييزٍ محاه الإسقاط."""

    source_id: str
    occurrence: int
    skeleton: str
    distinction: str
    witness_id: str

    def __post_init__(self) -> None:
        if self.occurrence < 0:
            raise ProjectionIdentityError("موضعُ وقوعٍ سالب؛ ولا ربطَ بغير موضع.")
        if not self.witness_id.strip():
            raise ProjectionIdentityError("شاهدٌ بلا اسمٍ يُنسَب إليه؛ فلا يُقبَل.")


THE_LICENSE_REGISTER: Final[tuple[CollapseLicense, ...]] = ()
"""سجلُّ التراخيص المكتوب؛ **فارغٌ في هذه الوديعة**، فلا التقاءَ ههنا مرخَّص."""

THE_DESTRUCTION_WITNESSES: Final[tuple[DestructionWitness, ...]] = ()
"""سجلُّ شهود الهدم؛ **فارغٌ في هذه الوديعة**، فلا موقفَ هدمٍ يُسنَد إلى شاهد."""


@dataclass(frozen=True)
class StandingFinding:
    """موقفُ ليفٍ واحد: سندُه، وآليّتُه، ومَن رخّصه، ومَن شهد عليه."""

    skeleton: str
    standing: CollapseStanding
    mechanism: CollapseMechanism
    license_ground: str | None
    witness_id: str | None

    def __post_init__(self) -> None:
        preserved = self.standing is CollapseStanding.PRESERVED_DISTINCTION
        if preserved and self.mechanism is not CollapseMechanism.NONE:
            raise ProjectionIdentityError("تمييزٌ محفوظٌ نُسبت إليه آليّةُ التقاء.")
        if not preserved and self.mechanism is CollapseMechanism.NONE:
            raise ProjectionIdentityError("التقاءٌ بلا آليّةٍ موصوفة؛ فالوصفُ ناقص.")
        licensed = self.standing is CollapseStanding.LICENSED_COLLAPSE
        if licensed != (self.license_ground is not None):
            raise ProjectionIdentityError("ترخيصٌ بلا سندٍ أو سندٌ بلا ترخيص.")
        destructive = self.standing is CollapseStanding.DESTRUCTIVE_COLLAPSE
        if destructive != (self.witness_id is not None):
            raise ProjectionIdentityError("هدمٌ بلا شاهدٍ أو شاهدٌ بلا هدم.")


def _mechanism_of(fiber: ProjectionFiber) -> CollapseMechanism:
    """آليّةُ الليف مشتقّةً من كلماته: أطَيٌّ مُعلَنٌ أم بقيّةٌ مُسقَطةٌ أم هما."""

    if fiber.is_preserved:
        return CollapseMechanism.NONE
    folds = {_unfolded_carriers(word) for word in fiber.written}
    residues = {_discarded_residue(word) for word in fiber.written}
    by_fold = len(folds) > 1
    by_residue = len(residues) > 1
    if by_fold and by_residue:
        return CollapseMechanism.MIXED
    if by_fold:
        return CollapseMechanism.DECLARED_FOLD
    if by_residue:
        return CollapseMechanism.DISCARDED_RESIDUE
    raise ProjectionIdentityError(
        f"ليفٌ فيه كلمتان متمايزتان بلا فرقٍ يُقاس: {fiber.skeleton!r}."
    )


def _license_for(source_id: str, fiber: ProjectionFiber) -> CollapseLicense | None:
    """الترخيصُ المطابقُ لليف إن وُجد؛ والمطابقةُ على الوديعة والكلمات جميعًا."""

    for entry in THE_LICENSE_REGISTER:
        if (
            entry.source_id == source_id
            and entry.skeleton == fiber.skeleton
            and tuple(sorted(entry.written)) == fiber.written
        ):
            return entry
    return None


def _witness_for(source_id: str, fiber: ProjectionFiber) -> DestructionWitness | None:
    """الشاهدُ المربوطُ بعين الوديعة وعين موضعٍ من مواضع الليف إن وُجد."""

    for witness in THE_DESTRUCTION_WITNESSES:
        if (
            witness.source_id == source_id
            and witness.skeleton == fiber.skeleton
            and witness.occurrence in fiber.occurrences
        ):
            return witness
    return None


def _finding_for(source_id: str, fiber: ProjectionFiber) -> StandingFinding:
    """موقفُ ليفٍ واحد؛ والآليّةُ لا تُرقّي موقفًا ولا تُنزِله."""

    mechanism = _mechanism_of(fiber)
    if fiber.is_preserved:
        return StandingFinding(
            skeleton=fiber.skeleton,
            standing=CollapseStanding.PRESERVED_DISTINCTION,
            mechanism=mechanism,
            license_ground=None,
            witness_id=None,
        )
    witness = _witness_for(source_id, fiber)
    if witness is not None:
        return StandingFinding(
            skeleton=fiber.skeleton,
            standing=CollapseStanding.DESTRUCTIVE_COLLAPSE,
            mechanism=mechanism,
            license_ground=None,
            witness_id=witness.witness_id,
        )
    entry = _license_for(source_id, fiber)
    if entry is not None:
        return StandingFinding(
            skeleton=fiber.skeleton,
            standing=CollapseStanding.LICENSED_COLLAPSE,
            mechanism=mechanism,
            license_ground=entry.ground,
            witness_id=None,
        )
    return StandingFinding(
        skeleton=fiber.skeleton,
        standing=CollapseStanding.UNRESOLVED_DISTINCTION,
        mechanism=mechanism,
        license_ground=None,
        witness_id=None,
    )


# --- الشهادة ---------------------------------------------------------------


@dataclass(frozen=True)
class ProjectionCertificate:
    """شهادةُ إسقاطٍ واحدة: مصدرٌ وطَيٌّ وحدٌّ وألياف وخسارةٌ وبقيّةٌ ونطاق."""

    source_identity: str
    fold_rule: str
    boundary_rule: WordBoundary
    fibers: tuple[ProjectionFiber, ...]
    findings: tuple[StandingFinding, ...]
    residue_occurrences: int
    residue_kinds: int
    trace: tuple[str, ...]
    domain: tuple[str, ...]
    scope_rank: str

    def __post_init__(self) -> None:
        if self.fold_rule != fold_rule_digest():
            raise ProjectionIdentityError("بصمةُ الطَّيِّ لا تطابق الجدولَ المُودَع.")
        if self.trace != THE_ORDER:
            raise ProjectionIdentityError("أثرُ الشهادة ليس ترتيبَ المسقط المُودَع.")
        if self.domain != THE_DEPOSITS_PROJECTED:
            raise ProjectionIdentityError("نطاقُ الشهادة ليس الوديعتَين المُودَعتَين.")
        if self.scope_rank != THE_SCOPE_RANK:
            raise ProjectionIdentityError("رتبةُ النطاق ليست الرتبةَ المُعلَنة ههنا.")
        if not self.fibers:
            raise ProjectionIdentityError("شهادةٌ بلا ليف؛ ولا مسقطَ بلا كلمة.")
        skeletons = tuple(fiber.skeleton for fiber in self.fibers)
        if len(set(skeletons)) != len(skeletons):
            raise ProjectionIdentityError("هيكلٌ في ليفَين؛ فالتكافؤ اختلّ.")
        if tuple(finding.skeleton for finding in self.findings) != skeletons:
            raise ProjectionIdentityError("المواقفُ لا تطابق الأليافَ عددًا وترتيبًا.")
        for fiber, finding in zip(self.fibers, self.findings, strict=True):
            preserved = finding.standing is CollapseStanding.PRESERVED_DISTINCTION
            if preserved != fiber.is_preserved:
                raise ProjectionIdentityError(
                    f"موقفٌ لا يطابق حجمَ ليفه: {fiber.skeleton!r}."
                )
        if self.loss != self.written_forms - self.skeleton_count:
            raise ProjectionIdentityError("الخسارةُ ليست فرقَ المكتوب عن الهياكل.")
        census = census_of(self.source_identity, self.boundary_rule)
        if census.residue_occurrences != self.residue_occurrences:
            raise ProjectionIdentityError("بقيّةُ الشهادة لا تطابق إحصاءَ الوديعة.")
        if census.residue_kinds != self.residue_kinds:
            raise ProjectionIdentityError("أجناسُ البقيّة لا تطابق إحصاءَ الوديعة.")
        if census.distinct_words != self.written_forms:
            raise ProjectionIdentityError("عددُ المكتوب لا يطابق إحصاءَ الوديعة.")
        if census.distinct_skeletons != self.skeleton_count:
            raise ProjectionIdentityError("عددُ الهياكل لا يطابق إحصاءَ الوديعة.")

    @property
    def written_forms(self) -> int:
        """\\(N_{written}\\): مجموعُ حجومِ الألياف."""

        return sum(fiber.size for fiber in self.fibers)

    @property
    def skeleton_count(self) -> int:
        """\\(N_{skeleton}\\): عددُ الألياف."""

        return len(self.fibers)

    @property
    def loss(self) -> int:
        """\\(Loss = \\sum_f (|f| - 1)\\): ما فقده الإسقاطُ من تمييزٍ مكتوب."""

        return sum(fiber.size - 1 for fiber in self.fibers)

    @property
    def preserved(self) -> tuple[ProjectionFiber, ...]:
        """الأليافُ المفردة؛ وهي التمييزُ الذي نجا من الإسقاط."""

        return tuple(fiber for fiber in self.fibers if fiber.is_preserved)

    @property
    def collapsed(self) -> tuple[ProjectionFiber, ...]:
        """الأليافُ التي فيها أكثرُ من كلمةٍ مكتوبة."""

        return tuple(fiber for fiber in self.fibers if not fiber.is_preserved)

    def standings(self) -> dict[CollapseStanding, tuple[str, ...]]:
        """المواقفُ الأربعةُ بهياكلها؛ والفارغُ منها يُنشَر فارغًا لا يُحذَف."""

        gathered: dict[CollapseStanding, list[str]] = {
            standing: [] for standing in CollapseStanding
        }
        for finding in self.findings:
            gathered[finding.standing].append(finding.skeleton)
        return {standing: tuple(found) for standing, found in gathered.items()}


@cache
def certificate_of(
    source_id: str, boundary: WordBoundary = WordBoundary.ANY_WHITESPACE
) -> ProjectionCertificate:
    """شهادةُ وديعةٍ بحدٍّ مذكور، مشتقّةً عند القراءة من حروفها لا مكتوبة."""

    if source_id not in THE_DEPOSITS_PROJECTED:
        raise ProjectionIdentityError(f"لا شهادةَ لوديعةٍ خارج النطاق: {source_id!r}.")
    if not the_fold_and_the_boundary_commute_on(source_id, boundary):
        raise ProjectionIdentityError(
            f"الطَّيُّ وحدُّ الكلمة لا يتوافقان على {source_id!r}؛ فلا شهادة."
        )
    fibers = fibers_of(source_id, boundary)
    census = census_of(source_id, boundary)
    return ProjectionCertificate(
        source_identity=source_id,
        fold_rule=fold_rule_digest(),
        boundary_rule=boundary,
        fibers=fibers,
        findings=tuple(_finding_for(source_id, fiber) for fiber in fibers),
        residue_occurrences=census.residue_occurrences,
        residue_kinds=census.residue_kinds,
        trace=THE_ORDER,
        domain=THE_DEPOSITS_PROJECTED,
        scope_rank=THE_SCOPE_RANK,
    )


# --- النقل: ما لا يُشهَد له بأنّه ثباتُ حامل --------------------------------


@cache
def uncertified_carrier_distinctions() -> tuple[frozenset[str], ...]:
    """فئاتُ الحوامل التي يفرّقها المسقطُ ولا تشهد لها هندسةُ الخطوط الثلاثة.

    تُقرأ الفئاتُ المقيسةُ من `blind_skeleton_transport` ثمّ تُطوى بجدول
    الطَّيّ وتُقصَر على التسعة والعشرين. وما اجتمع منها في فئةٍ واحدةٍ فهو
    تمييزٌ **غيرُ مشهودٍ له**، لا تمييزٌ باطل.
    """

    from alghanem.arabic.blind_skeleton_transport import classes_that_transport

    carriers = set(the_twenty_nine())
    found: list[frozenset[str]] = []
    for klass in classes_that_transport():
        folded = {THE_FOLDING.get(letter, letter) for letter in klass} & carriers
        if len(folded) > 1:
            found.append(frozenset(folded))
    return tuple(sorted(found, key=lambda members: (-len(members), sorted(members))))


# --- حرّاسُ الاستيراد ------------------------------------------------------


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ في الشهادة؛ ورتبةُ النطاق محلّيّةٌ باسمها."""

    named = {field.name for field in fields(ProjectionCertificate)}
    forbidden = {"verdict", "licensed", "born", "frozen", "authority", "rank"}
    if named & forbidden:
        found = sorted(named & forbidden)
        raise ProjectionIdentityError(f"حقلُ سلطةٍ في شهادة: {found}.")


def _assert_no_probability_leaks_in() -> None:
    """حارسُ استيراد: لا اسمَ احتمالٍ في الواجهة إلّا بقيّةً تُسمّيه لتمنعه."""

    banned = ("entropy", "probab", "nll", "likelihood", "markov", "transition_matrix")
    for name in __all__:
        if name in PROJECTION_IDENTITY_NAMED_RESIDUALS:
            continue
        lowered = name.lower()
        if any(word in lowered for word in banned):
            raise ProjectionIdentityError(f"اسمُ احتمالٍ في واجهة الشهادة: {name}.")


def _assert_the_registers_are_empty_on_this_evidence() -> None:
    """حارسُ استيراد: سجلّا الترخيص والشهود فارغان، فلا موقفَ بلا سند."""

    for source_id in THE_DEPOSITS_PROJECTED:
        standings = certificate_of(source_id).standings()
        if standings[CollapseStanding.LICENSED_COLLAPSE]:
            raise ProjectionIdentityError(
                "التقاءٌ مرخَّصٌ والسجلُّ فارغ؛ فالترخيصُ أُخذ من غير سجلّ."
            )
        if standings[CollapseStanding.DESTRUCTIVE_COLLAPSE]:
            raise ProjectionIdentityError(
                "هدمٌ مشهودٌ وسجلُّ الشهود فارغ؛ فالشاهدُ أُخذ من غير وديعة."
            )


def _assert_the_commutation_is_measured_and_breaks_where_it_is_said_to() -> None:
    """حارسُ استيراد: جدولُ التوافق مقيسٌ، وكسرُه في موضعٍ واحدٍ منشورٌ لا مطويّ."""

    table = the_commutation_table()
    broken = tuple(pair for pair, holds in table.items() if not holds)
    if broken != ((FATIHA_SOURCE_ID, WordBoundary.SPACE_ONLY),):
        raise ProjectionIdentityError(
            f"جدولُ التوافق ليس ما نُشر؛ المكسورُ ههنا: {broken}."
        )


def _assert_no_fold_touches_whitespace() -> None:
    """حارسُ استيراد: علّةُ التوافق مكتوبةٌ ومقيسة؛ لا رسمَ مطويٌّ بياضٌ ولا إليه."""

    for source, target in THE_FOLDING.items():
        if source.isspace() or target.isspace():
            raise ProjectionIdentityError("جدولُ الطَّيِّ يمسّ بياضًا؛ فالترتيبُ يُراجَع.")


def _assert_the_loss_is_derived_from_the_fibers() -> None:
    """حارسُ استيراد: الخسارةُ مشتقّةٌ من الألياف وتطابق إحصاءَ الوديعة."""

    for source_id in THE_DEPOSITS_PROJECTED:
        certificate = certificate_of(source_id)
        from_fibers = sum(fiber.size - 1 for fiber in certificate.fibers)
        if certificate.loss != from_fibers:
            raise ProjectionIdentityError("خسارةٌ لا تُشتقّ من الألياف.")


def _assert_no_collapse_here_is_made_by_the_declared_fold() -> None:
    """حارسُ استيراد: كلُّ التقاءٍ ههنا بقيّةٌ مُسقَطة، ولا طَيٌّ مُعلَنٌ صنع واحدًا."""

    for source_id in THE_DEPOSITS_PROJECTED:
        certificate = certificate_of(source_id)
        findings = {finding.skeleton: finding for finding in certificate.findings}
        for fiber in certificate.collapsed:
            if findings[fiber.skeleton].mechanism is not (
                CollapseMechanism.DISCARDED_RESIDUE
            ):
                raise ProjectionIdentityError(
                    f"التقاءٌ ليست آليّتُه بقيّةً مُسقَطة: {fiber.skeleton!r}؛ "
                    "فالمنشورُ عن هاتين الوديعتَين يُراجَع."
                )


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in PROJECTION_IDENTITY_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise ProjectionIdentityError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


def _assert_the_deposits_are_the_two_named() -> None:
    """حارسُ استيراد: النطاقُ وديعتان باسمَيهما، ولا يُقاس ههنا نصٌّ سواهما."""

    if set(THE_DEPOSITS_PROJECTED) != {FATIHA_SOURCE_ID, FATH_AYAH_SOURCE_ID}:
        raise ProjectionIdentityError("نطاقُ الشهادة ليس الوديعتَين المسمّاتَين.")


_assert_no_authority_field()
_assert_no_probability_leaks_in()
_assert_the_deposits_are_the_two_named()
_assert_no_fold_touches_whitespace()
_assert_the_commutation_is_measured_and_breaks_where_it_is_said_to()
_assert_the_registers_are_empty_on_this_evidence()
_assert_the_loss_is_derived_from_the_fibers()
_assert_no_collapse_here_is_made_by_the_declared_fold()
_assert_every_residual_is_named_by_its_key()
