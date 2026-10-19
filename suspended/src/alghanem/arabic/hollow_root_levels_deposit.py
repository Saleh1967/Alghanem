"""إيداعُ ما وردَ عن سُلَّمِ الجذر الأجوف: مُسجَّلًا بما فيه من تعارضٍ، بلا حسم.

`THE_DEPOSIT_IS_NOT_AN_ADOPTION`: تسجيلُ دعوى في هذه الوحدة ليس تبنّيًا لها؛
وقد أُعيد اشتقاقُ ما أمكنَ اشتقاقُه بأدوات هذه الشجرة، وما انقلب انقلب بنصّه.

`THE_BYTES_NEVER_REACHED_THIS_TREE`: الملفّاتُ الثلاثةُ التي أُعلنت بصماتُها في
المحادثة الخارجية لم تصل هذه الشجرةَ قطّ — لا مرفقاتٍ ولا نصًّا سليمَ البايتات.
وقد أفسد ترميزُ HTML ما لُصِق منها (`-&gt;` بدل `->`)، فبطلت مطابقةُ SHA-256
حتمًا. فهذه البصماتُ تُسجَّل **بندًا مفتوحًا معلومَ الاسم**، لا شاهدًا يُحتجّ به
ولا عائقًا يوقف العمل: ما في هذه الشجرة أُعيد بناؤه من أدواتها المُبصَّمة وحدَها.

`A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT`: كلُّ رقمٍ ورد منسوبًا إلى
مدوّنةٍ (`quran-simple-enhanced.txt` وأمثالِها) غيرُ قابلٍ لإعادة الاشتقاق هنا:
لا ملفَّ مدوّنةٍ واحدًا في هذه الشجرة. فيُسجَّل الرقمُ بنصّه وبسببِ تعذّره.

`A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE`: لكلّ تعارضٍ موضعُه، وما تقوله
الشجرة، ومرجعُه فيها، وشرطُ حسمه — ولا حقلَ حسمٍ في هذه الوحدة البتّة.

`A_SUBMITTED_FREEZE_IS_RECORDED_IN_ONE_PLACE_ONLY`: مُعرِّفُ التجميد الوارد
المتّصلُ بهذا السُّلَّم مُسجَّلٌ في وحدة إيداعه وحدَها موسومًا بأنّه غيرُ صادرٍ عن
هذه الشجرة، ولا يُعاد نسخُه هنا: تكرارُ المُعرِّف في موضعين يجعله يُقرأ مُثبَتًا
بشاهدين، وهو شاهدٌ واحدٌ مكرَّر. فيُشار إلى موضعه ولا يُنقَل نصُّه.

`AN_INDEPENDENT_CONVERGENCE_IS_WORTH_RECORDING_TOO`: لا يُسجَّل المتعارضُ وحدَه؛
فتوافقُ أداةٍ خارجيةٍ مع قاعدةٍ في هذه الشجرة توافقًا تامًّا شاهدٌ يُسجَّل بمثلِ
ما يُسجَّل به الخلاف.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا رفعَ
حجبٍ عن طبقة، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "AN_INDEPENDENT_CONVERGENCE_IS_WORTH_RECORDING_TOO_NOTE",
    "A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT_NOTE",
    "A_QUOTED_DIGEST_PREFIX_IS_NOT_A_DIGEST_NOTE",
    "A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE",
    "A_SUBMITTED_FREEZE_IS_RECORDED_IN_ONE_PLACE_ONLY_NOTE",
    "HOLLOW_ROOT_CONFLICTS",
    "HOLLOW_ROOT_CONVERGENCES",
    "HOLLOW_ROOT_DEPOSIT_NAMED_RESIDUALS",
    "HOLLOW_ROOT_NUMERIC_CLAIMS",
    "THE_BYTES_NEVER_REACHED_THIS_TREE",
    "THE_BYTES_NEVER_REACHED_THIS_TREE_NOTE",
    "THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE",
    "UNARRIVED_ARTEFACTS",
    "ConflictStanding",
    "HollowRootConflict",
    "HollowRootDepositError",
    "HollowRootNumericClaim",
    "IndependentConvergence",
    "UnarrivedArtefact",
]


class HollowRootDepositError(ValueError):
    """رفضٌ عند الإيداع: سجلٌّ بلا موضعٍ أو بلا مرجعٍ أو بلا شرطِ حسم."""


A_QUOTED_DIGEST_PREFIX_IS_NOT_A_DIGEST_NOTE: Final[str] = (
    "AQuotedDigestPrefixIsNotADigest: يُسجَّل صدرُ البصمة كما نُقِل، لا بصمةٌ "
    "تامّةُ الطول؛ وإكمالُ البصمة من غير مصدرها اختلاقٌ لا نقل، وصدرُ بصمةٍ "
    "لا يُطابَق به ملفّ"
)

THE_BYTES_NEVER_REACHED_THIS_TREE: Final[str] = (
    "THE_BYTES_NEVER_REACHED_THIS_TREE: لم يصل الملفُّ هذه الشجرةَ قطّ؛ "
    "والبصمةُ مذكورةٌ نقلًا عن المحادثة الخارجية لا مُعادةَ الاشتقاق هنا"
)

_NO_CORPUS_REACHED_THIS_TREE: Final[str] = (
    "لا ملفَّ مدوّنةٍ واحدًا في هذه الشجرة، فلا يُعاد اشتقاقُ رقمٍ منسوبٍ إليها"
)

_REDERIVATION_CONDITION: Final[str] = (
    "أن تصل المدوّنةُ المُبصَّمةُ نفسُها هذه الشجرةَ بايتًا بايتًا، ويُعاد العدُّ "
    "بأدواتها المُستورَدة لا بأرقامٍ منقولة"
)

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "resolution",
    "resolved",
    "verdict",
    "ruling",
    "settled",
    "accepted",
    "adopted",
)


class ConflictStanding(Enum):
    """مرتبةُ التعارض كما رُصِد، لا كما يُرجى أن يُحسَم."""

    THE_TREE_REDERIVED_THE_OPPOSITE = "أعادت الشجرةُ الاشتقاقَ فخرج بعكس الدعوى"
    THE_TREE_CANNOT_TEST_IT = "لا تملك الشجرةُ ما تختبر به الدعوى"
    THE_CLAIM_RESTATES_A_LIMIT_ALREADY_RECORDED_HERE = (
        "الدعوى تُعيد صياغةَ حدٍّ مُسجَّلٍ في الشجرة قبل ورودها"
    )


@dataclass(frozen=True, slots=True)
class UnarrivedArtefact:
    """ملفٌّ أُعلنت بصمتُه خارجًا ولم يصل: اسمُه، وصدرُ بصمته، وسببُ تعذّره.

    `A_QUOTED_DIGEST_PREFIX_IS_NOT_A_DIGEST`: يُسجَّل **صدرُ** البصمة كما نُقِل
    في المحادثة لا بصمةٌ تامّةُ الطول: البصمةُ التامّة لم تُعَد كتابتُها هنا،
    وإكمالُها من عندي اختلاقٌ لا نقل. وصدرُ بصمةٍ لا يُطابَق به ملفّ أصلًا،
    فالحقلُ أثرٌ يُتتبَّع به لا شاهدٌ يُحتجّ به.
    """

    file_name: str
    declared_digest_prefix: str
    what_it_was_said_to_contain: str
    never_arrived_because: str
    open_item: str = THE_BYTES_NEVER_REACHED_THIS_TREE

    def __post_init__(self) -> None:
        for field_name in (
            "file_name",
            "declared_digest_prefix",
            "what_it_was_said_to_contain",
            "never_arrived_because",
            "open_item",
        ):
            if not str(getattr(self, field_name)).strip():
                raise HollowRootDepositError(
                    "ملفٌّ لم يصل يُسجَّل باسمه وبصمته المنقولة وسببِ تعذّره؛ "
                    "وسجلٌّ ناقصٌ يُقرأ بعد جلساتٍ وصولًا، وهو ما لم يقع"
                )
        if self.open_item != THE_BYTES_NEVER_REACHED_THIS_TREE:
            raise HollowRootDepositError(
                "البندُ المفتوحُ لهذه السجلّات واحدٌ باسمه المُجمَّد، ولا يُبدَّل "
                "باسمٍ ألينَ منه"
            )


@dataclass(frozen=True, slots=True)
class HollowRootNumericClaim:
    """رقمٌ ورد: نصُّه، وموضعُه، وسببُ تعذّر اشتقاقه، وشرطُ اشتقاقه."""

    figure: str
    locus: str
    claim_text: str
    not_rederivable_because: str
    what_would_make_it_rederivable: str

    def __post_init__(self) -> None:
        for field_name in dataclasses.asdict(self):
            if not str(getattr(self, field_name)).strip():
                raise HollowRootDepositError(
                    "رقمٌ بلا سببِ تعذّرٍ أو بلا شرطِ اشتقاقٍ يُقرأ مقيسًا في هذه "
                    "الشجرة، وهو ما لم يقع"
                )


@dataclass(frozen=True, slots=True)
class HollowRootConflict:
    """تعارضٌ مرصود: موضعُه، وما وردَ، وما تقوله الشجرة، وما يلزم لحسمه — بلا حسم."""

    locus: str
    the_claim_says: str
    this_tree_says: str
    tree_reference: str
    what_would_resolve_it: str
    standing: ConflictStanding

    def __post_init__(self) -> None:
        for field_name in (
            "locus",
            "the_claim_says",
            "this_tree_says",
            "tree_reference",
            "what_would_resolve_it",
        ):
            if not str(getattr(self, field_name)).strip():
                raise HollowRootDepositError(
                    "تعارضٌ بلا موضعٍ أو بلا مرجعٍ أو بلا شرطِ حسمٍ ليس تعارضًا "
                    "مرصودًا بل انطباعًا"
                )
        if not isinstance(self.standing, ConflictStanding):
            raise HollowRootDepositError("مرتبةُ التعارض عضوٌ من `ConflictStanding`")


@dataclass(frozen=True, slots=True)
class IndependentConvergence:
    """توافقٌ مستقلّ: ما وافقَ، وما وافقه في الشجرة، ومدى التوافق وحدُّه."""

    locus: str
    what_converged: str
    tree_reference: str
    extent_of_agreement: str
    what_it_does_not_establish: str

    def __post_init__(self) -> None:
        for field_name in dataclasses.asdict(self):
            if not str(getattr(self, field_name)).strip():
                raise HollowRootDepositError(
                    "توافقٌ بلا حدٍّ يُسمّي ما لا يُثبِته يُقرأ تصديقًا عامًّا، "
                    "والتوافقُ في موضعٍ ليس تصديقًا في غيره"
                )


UNARRIVED_ARTEFACTS: Final[tuple[UnarrivedArtefact, ...]] = (
    UnarrivedArtefact(
        file_name="hollow_root_corrected.py",
        declared_digest_prefix="7cfc0307…",
        what_it_was_said_to_contain=(
            "سكربتُ كشفِ التصادم بعد إصلاح عطليه: شرطِ اختلاف الحالات، ودهسِ "
            "التسجيل السابق"
        ),
        never_arrived_because=(
            "ما لُصِق منه أفسده ترميزُ HTML (`-&gt;` بدل `->`)، فبطلت مطابقةُ "
            "البصمة؛ ولم يُرفَع الملفُّ مرفقًا قطّ"
        ),
    ),
    UnarrivedArtefact(
        file_name="p_extractor_pilot1.py",
        declared_digest_prefix="3673baa6…",
        what_it_was_said_to_contain="نسخةُ مرماز P المستعملة في الحساب الخارجي",
        never_arrived_because="وصل النصُّ مقطوعًا في منتصف سطر، فلا بايتاتٍ تُطابَق",
    ),
    UnarrivedArtefact(
        file_name="syllabifier_wazn_pilot1.py",
        declared_digest_prefix="aea319da…",
        what_it_was_said_to_contain="مُقطِّعُ الأوزان المستعمل في الحساب الخارجي",
        never_arrived_because=(
            "لم يصل إلا جزءٌ من دالّة الوقف ومن `main`؛ ومسارُ الرفع "
            "`/mnt/user-data/uploads/` لا وجودَ له في هذه البيئة"
        ),
    ),
)


HOLLOW_ROOT_NUMERIC_CLAIMS: Final[tuple[HollowRootNumericClaim, ...]] = (
    HollowRootNumericClaim(
        figure="1,319,901 بايت",
        locus="بصمةُ المصدر المُعلَنة مع سُلَّم المستويات",
        claim_text=(
            "`quran-simple-enhanced.txt` بحجم 1,319,901 بايت وبصمة "
            "`37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a`"
        ),
        not_rederivable_because=_NO_CORPUS_REACHED_THIS_TREE,
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
    ),
    HollowRootNumericClaim(
        figure="2b95f2d1",
        locus="بصمةُ المصدر في الصياغة الثانية للسُّلَّم",
        claim_text="بصمةٌ للمصدر نفسه مذكورةٌ بثمانيةِ محارفَ عشريةً ستّ عشريّة",
        not_rederivable_because=(
            "ثمانيةُ محارفَ ليست SHA-256؛ والصياغةُ الأولى ذكرت للمصدر نفسِه "
            "بصمةً أخرى تامّةَ الطول تبدأ بـ`3763`، فالبصمتان لا تجتمعان على ملفّ"
        ),
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
    ),
    HollowRootNumericClaim(
        figure="11/11",
        locus="اختبارُ اللاحقات المُشار إليه بوصفه سابقًا على هذا السُّلَّم",
        claim_text="«11/11 لكليهما» في اختبارٍ سابقٍ على جذورٍ سالمة",
        not_rederivable_because=(
            "لا أثرَ لهذا الاختبار ولا لمخرجاته في هذه الشجرة، ولا مدوّنةَ " "يُعاد عليها"
        ),
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
    ),
    HollowRootNumericClaim(
        figure="4-6 لكلّ مستوى",
        locus="حدُّ العيّنة المُقرُّ به مع السُّلَّم",
        claim_text="«الأمثلةُ يدويّةُ الاختيار، 4-6 لكلّ مستوى، لا إحصاءً شاملًا»",
        not_rederivable_because=(
            "هذا إقرارٌ بحدٍّ لا رقمٌ مقيس؛ وقد أُعيد بناءُ العيّنة هنا بأربعٍ "
            "وعشرين صورةً مُجمَّدةً باسمها، وحدُّها مُسجَّلٌ في وحدة التسجيل"
        ),
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
    ),
)


HOLLOW_ROOT_CONFLICTS: Final[tuple[HollowRootConflict, ...]] = (
    HollowRootConflict(
        locus="المستوى ٠ — «قَالَ وقُلْ كلاهما ← قل بالضبط»",
        the_claim_says="الجذرُ المجرَّد يُسقِط الفرقَ بين قَالَ وقُلْ إسقاطًا تامًّا",
        this_tree_says=(
            "ينقلب بحسب الإسقاط المقصود، وهما إسقاطان لا واحد: بإسقاط العلامات "
            "وحدها (`text_key.comparison_key`) تخرج «قال» و«قل» متمايزتين فلا "
            "تصادم؛ وبإسقاط حاملِ دور المدّ معهما تخرج «قل» و«قل» فيقع التصادم. "
            "فالدعوى صحيحةٌ تحت الإسقاط الثاني وحدَه، وقد وردت بلا تسميةِ إسقاطها"
        ),
        tree_reference=(
            "`text_key.comparison_key`؛ "
            "`hollow_root_levels_measurement.level_fingerprint` عند "
            "`HARAKAT_STRIPPED` و`MADD_ALSO_DROPPED`"
        ),
        what_would_resolve_it=(
            "أن يُسمّى الإسقاطُ المقصود بعينه قبل الدعوى، فتُقاس الدعوى عليه"
        ),
        standing=ConflictStanding.THE_TREE_REDERIVED_THE_OPPOSITE,
    ),
    HollowRootConflict(
        locus="المستوى ١+٢ — «أربعُ بصماتٍ متمايزة تمامًا بلا تصادمٍ واحد»",
        the_claim_says=(
            "قالبُ المقطع مع الحركة الفعلية يحسم الصيغةَ السطحيةَ كاملةً، "
            "ولا يقع تحتها تصادمٌ واحد"
        ),
        this_tree_says=(
            "انتفاءُ التصادم خاصّيّةُ العيّنة الرباعية لا خاصّيّةُ البصمة. وعلى "
            "الصور الأربعِ والعشرين المُجمَّدة تقع تحت «قالب+حالة» ستُّ طبقات "
            "تصادمٍ تُطبِق أربعًا وعشرين صورةً على عشرِ بصماتٍ فقط؛ وأشدُّها "
            "`قَوْلٌ`/`بَيْعٌ`/`خَوْفٌ`/`نَوْمٌ` متطابقةً قالبًا وحالةً معًا رغم "
            "ظهور و/ي في رسمها"
        ),
        tree_reference=(
            "`hollow_root_levels_measurement.template_and_state_collisions`"
        ),
        what_would_resolve_it=(
            "أن تُقاس الدعوى على عيّنةٍ تضمّ جذورًا جوفاءَ مختلفةً لا على تصريفات "
            "جذرٍ واحد، أو أن تُقيَّد بالجذر الواحد صراحةً"
        ),
        standing=ConflictStanding.THE_TREE_REDERIVED_THE_OPPOSITE,
    ),
    HollowRootConflict(
        locus="ترتيبُ السُّلَّم — «كلُّ مستوًى يحلّ ما عجز عنه سابقُه»",
        the_claim_says="المستوياتُ مرتَّبةٌ ترتيبَ دقّةٍ متزايدة، كلٌّ أحسمُ ممّا قبله",
        this_tree_says=(
            "الترتيبُ ينقلب على هذه العيّنة: عددُ البصمات المتمايزة ينخفض كلّما "
            "تقدّمنا في السُّلَّم لا يرتفع، فالمستوى المتأخِّرُ يتصادم أكثرَ من "
            "المتقدِّم. والسُّلَّمُ ترتيبُ تسميةٍ لا ترتيبُ دقّة"
        ),
        tree_reference=(
            "`hollow_root_levels_measurement.read_all_levels`؛ "
            "`A_LATER_LEVEL_IS_NOT_NECESSARILY_A_FINER_ONE_NOTE`"
        ),
        what_would_resolve_it=(
            "أن يُذكَر لكلّ مستوًى ما يحسمه وما يُسقِطه معًا، لا فضلُه على سابقه " "وحدَه"
        ),
        standing=ConflictStanding.THE_TREE_REDERIVED_THE_OPPOSITE,
    ),
    HollowRootConflict(
        locus="المستوى ٣ — «ضمّةٌ قبل المدّ ← واويّ، وكسرةٌ قبل المدّ ← يائيّ»",
        the_claim_says="نمطُ المضارع يحسم هويّةَ العلّة (و/ي) التي لا يحسمها ما قبله",
        this_tree_says=(
            "يصحّ حيث كانت الحركةُ قبل المدّ ضمّةً أو كسرةً، ويسقط حيث كانت "
            "فتحةً: `يَخَافُ` (خوف، واويّ) و`يَهَابُ` (هيب، يائيّ) متطابقتان "
            "قالبًا وحالةً تطابقًا تامًّا، فالبصمةُ عمياءُ عن العلّة فيهما. "
            "وهذا حدٌّ مُسجَّلٌ في هذه الشجرة قبل ورود الدعوى"
        ),
        tree_reference=(
            "`docs/reference/gflk_arabic_letter_specification.md` — «فتحة ما قبل "
            "مدّ المضارع عمياء بنيويًّا لهوية العلة»؛ والجذرانِ مقروءان من "
            "`maqayis_root_table_deposit.root_table_rows`؛ ومُعرِّفُ التجميد "
            "الوارد المتّصل بهذا الحدّ مُسجَّلٌ في `gflk_specification_deposit` "
            "وحدَه، ولا يُنقَل نصُّه هنا"
        ),
        what_would_resolve_it=(
            "أن تُقيَّد الدعوى بنمطَي الضمّة والكسرة صراحةً، ويُستثنى نمطُ الفتحة " "باسمه"
        ),
        standing=ConflictStanding.THE_CLAIM_RESTATES_A_LIMIT_ALREADY_RECORDED_HERE,
    ),
    HollowRootConflict(
        locus="اقتراحُ حسمِ العلّة بالرجوع إلى المصدر أو إلى جدول الجذور",
        the_claim_says="يُحسَم و/ي بمطابقة الهيكل الساكن بمدخلٍ في جدول الجذور",
        this_tree_says=(
            "المطابقةُ دوريّة: `خيف` و`نيم` و`هوب` و`قيل` مُدرَجةٌ في جدول "
            "المقاييس مداخلَ مستقلّةً كما `خوف` و`نوم` و`هيب` و`قول`، فالهيكلُ "
            "الساكنُ يُرجِع كلا الاحتمالين. وليس في هذه الشجرة مستخرِجُ جذورٍ من "
            "الصور السطحية أصلًا، فالجذرُ مُعلَنٌ مع الصورة لا مُستخرَجٌ منها"
        ),
        tree_reference=(
            "`maqayis_root_table_deposit.root_table_rows`؛ "
            "`THE_WEAK_RADICAL_IS_DECLARED_NOT_EXTRACTED_NOTE`؛ "
            "والشاهدُ الخارجيُّ الذي يستوفي شرطَ الحسم صار مُسمًّى ومُشغَّلًا في "
            "`hollow_root_root_census` وفي "
            "`examples/irab/measure_hollow_root_census.py`، مربوطًا ببصمة "
            "`irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS` وطولِها"
        ),
        what_would_resolve_it=(
            "شاهدٌ خارجَ الصورة السطحية يُسنِد هويّةَ العلّة إسنادًا مُبصَّمًا، "
            "أو مستخرِجُ جذورٍ يُبنى ويُختبَر ويُودَع في هذه الشجرة. والمسارُ "
            "الأوّلُ صار قائمًا مُشغَّلًا لا مُقترَحًا: خانةُ `ROOT` في "
            "المدوَّنة الصرفية تُسنِد هويّةَ العلّة لكلّ مقطعٍ بعينه. ويبقى "
            "لتبديل المنزلة أمران لا يُطويان: أن يُسجَّل تشغيلٌ على بايتاتٍ "
            "طابقت البصمةَ والطول، وأن يُسمّى مدى ما حسمه — فالمحسومُ انتفاءُ "
            "المُنازِع **في هذه المدوَّنة** لا انكشافُ قاعدةٍ تأخذ صورةً "
            "سطحيةً فتُرجِع جذرَها؛ وتبديلُ المنزلة قرارٌ مستقلٌّ لا أثرٌ "
            "جانبيٌّ لإيداع أرقام"
        ),
        standing=ConflictStanding.THE_TREE_CANNOT_TEST_IT,
    ),
    HollowRootConflict(
        locus="كاشفُ التصادم الوارد — شرطُ `!= states` ودهسُ التسجيل",
        the_claim_says=("العطلانِ مُصلَحانِ في البيئة الخارجية، والمخرجُ بعد الإصلاح مطابق"),
        this_tree_says=(
            "العطلانِ مرصودانِ في النصّ الوارد بعينه: اشتراطُ اختلاف الحالات "
            "يُخفي التصادمَ التامّ وهو أشدُّه، وإسنادُ القيمة يدهس السابقَ فلا "
            "تُقارَن الصورةُ إلا بآخر صورة. وعطلٌ ثالث: `return` بدل `continue` "
            "في دالّة الوقف يُميت فرعَ تنوين الفتح كلَّه. أمّا الإصلاحُ ذاته فلم "
            "يصل هذه الشجرةَ فلا يُشهَد عليه؛ وقد بُني الكشفُ هنا بالتجميع ابتداءً"
        ),
        tree_reference=(
            "`hollow_root_levels_measurement` — "
            "`A_COLLISION_IS_FOUND_BY_GROUPING_NOT_BY_PAIRWISE_COMPARISON_NOTE` "
            "و`A_TOTAL_COLLISION_IS_THE_STRONGEST_ONE_NOT_THE_INVISIBLE_ONE_NOTE`؛ "
            "و`syllabifier.apply_stated_waqf` التي تمرّ على الوحدات بـ`continue`"
        ),
        what_would_resolve_it=(
            "أن يصل الملفُّ المُصلَح بايتًا بايتًا فتُطابَق بصمتُه ويُشغَّل هنا"
        ),
        standing=ConflictStanding.THE_TREE_CANNOT_TEST_IT,
    ),
)


HOLLOW_ROOT_CONVERGENCES: Final[tuple[IndependentConvergence, ...]] = (
    IndependentConvergence(
        locus="دالّةُ `to_waqf_form` الواردة مقابلَ قواعد الوقف المُجمَّدة هنا",
        what_converged=(
            "فروعُ الوقف الأربعةُ في الدالّة الواردة تطابق "
            "`WAQF_TRANSFORM_RULES` أربعةً من أربعة، اسمًا وشرطًا وأثرًا"
        ),
        tree_reference="`syllable_preregistration.WAQF_TRANSFORM_RULES`",
        extent_of_agreement=(
            "تطابقٌ تامّ في القواعد الأربع، بُلِغ إليه من طريقين منفصلين لم "
            "يطّلع أحدهما على الآخر"
        ),
        what_it_does_not_establish=(
            "لا يُثبِت صحّةَ التنفيذ الوارد: فيه عطلُ `return` بدل `continue` "
            "الذي يُميت فرعَ تنوين الفتح، فالقواعدُ تطابقت والتنفيذُ لم يتطابق. "
            "ولا يُثبِت أنّ الوقفَ مقروءٌ من مدوّنة: الوقفُ مُدخَلٌ مُعلَنٌ في "
            "هذه الشجرة لا مُستخرَجٌ من نصّ"
        ),
    ),
    IndependentConvergence(
        locus="طبقاتُ التصادم الستُّ تحت «قالب+حالة»",
        what_converged=(
            "ستُّ طبقاتٍ أُعيد اشتقاقُها هنا بأدوات هذه الشجرة المُستورَدة، "
            "وطابقت في أعضائها ما أُبلِغ به من الطرف الآخر"
        ),
        tree_reference=(
            "`hollow_root_levels_measurement.template_and_state_collisions`"
        ),
        extent_of_agreement=(
            "تطابقٌ في أعضاء الطبقات على الصور المشتركة، من حسابين منفصلين"
        ),
        what_it_does_not_establish=(
            "لا يُثبِت شيئًا خارج الصور المُجمَّدة بأعيانها: العيّنةُ منشأةٌ "
            "يدويًّا لا مسحوبةٌ من مدوّنة، فلا يُقرأ منها تردُّدٌ ولا نسبة"
        ),
    ),
)


THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE: Final[str] = (
    "TheDepositIsNotAnAdoption: تسجيلُ الدعوى ليس تبنّيًا لها؛ وما أمكن "
    "اشتقاقُه أُعيد اشتقاقُه، وما انقلب سُجِّل انقلابُه بنصّه"
)

THE_BYTES_NEVER_REACHED_THIS_TREE_NOTE: Final[str] = (
    "TheBytesNeverReachedThisTree: الملفّاتُ الثلاثةُ المُعلَنةُ البصماتِ لم تصل "
    "هذه الشجرةَ قطّ؛ فبصماتُها منقولةٌ لا مُعادةُ الاشتقاق، وهي بندٌ مفتوحٌ "
    "معلومُ الاسم لا شاهدٌ ولا عائق"
)

A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "ANumberWithoutACorpusIsNotAMeasurement: رقمٌ منسوبٌ إلى مدوّنةٍ لم تصل "
    "يُسجَّل بنصّه وبسببِ تعذّره، ولا يُقرأ مقيسًا في هذه الشجرة"
)

A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE: Final[str] = (
    "ARecordedConflictIsNotAResolvedOne: لكلّ تعارضٍ موضعُه ومرجعُه وشرطُ حسمه، "
    "ولا حقلَ حسمٍ في هذه الوحدة البتّة"
)

A_SUBMITTED_FREEZE_IS_RECORDED_IN_ONE_PLACE_ONLY_NOTE: Final[str] = (
    "ASubmittedFreezeIsRecordedInOnePlaceOnly: مُعرِّفُ التجميد الوارد مُسجَّلٌ "
    "في وحدة إيداعه وحدَها؛ وتكرارُه هنا يجعله يُقرأ مُثبَتًا بشاهدين وهو واحدٌ "
    "مكرَّر، فيُشار إلى موضعه ولا يُنقَل نصُّه"
)

AN_INDEPENDENT_CONVERGENCE_IS_WORTH_RECORDING_TOO_NOTE: Final[str] = (
    "AnIndependentConvergenceIsWorthRecordingToo: التوافقُ المستقلّ يُسجَّل "
    "بحدِّه كما يُسجَّل الخلاف؛ وتوافقٌ في موضعٍ ليس تصديقًا في غيره"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "ThisIsRegistrationNotAuthority: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا رفعَ "
    "حجبٍ عن طبقة، ولا استيرادَ من `kernel/`"
)

HOLLOW_ROOT_DEPOSIT_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_INDEPENDENT_CONVERGENCE_IS_WORTH_RECORDING_TOO_NOTE,
    A_QUOTED_DIGEST_PREFIX_IS_NOT_A_DIGEST_NOTE,
    A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT_NOTE,
    A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE,
    A_SUBMITTED_FREEZE_IS_RECORDED_IN_ONE_PLACE_ONLY_NOTE,
    THE_BYTES_NEVER_REACHED_THIS_TREE_NOTE,
    THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE,
    THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE,
)


def _assert_no_resolution_field() -> None:
    """امنعْ حقلَ حسمٍ في أيّ سجلٍّ هنا؛ فالإيداعُ يرصد ولا يقضي."""

    for record in (
        UnarrivedArtefact,
        HollowRootNumericClaim,
        HollowRootConflict,
        IndependentConvergence,
    ):
        for field in dataclasses.fields(record):
            lowered = field.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered and "what_would_resolve_it" != field.name:
                    raise RuntimeError(
                        f"الحقلُ `{record.__name__}.{field.name}` يحمل وسمَ حسمٍ "
                        f"(`{token}`)، والإيداعُ يرصد ولا يقضي. "
                        + A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE
                    )


def _assert_every_conflict_names_a_tree_reference() -> None:
    """لا تعارضَ بلا مرجعٍ في هذه الشجرة؛ فدعوى بلا مرجعٍ انطباعٌ لا رصد."""

    for conflict in HOLLOW_ROOT_CONFLICTS:
        if "`" not in conflict.tree_reference:
            raise RuntimeError(
                f"التعارضُ عند «{conflict.locus}» بلا مرجعٍ مُسمًّى في هذه "
                "الشجرة؛ والمرجعُ يُسمّى بموضعه لا بالإشارة العامّة."
            )


_assert_no_resolution_field()
_assert_every_conflict_names_a_tree_reference()
