"""تسرُّبُ أسماء الحروف في «مقاييس اللغة»، مقيسًا قبلَ التنظيف وبعدَه.

كلُّ شرحٍ عند ابن فارس يفتتح بتسمية حروف جذره: «الهمزة والباء والتاء أصلٌ
واحد…». فالجذران المشتركان في حرفٍ يتقاسمان **اسمَ ذلك الحرف نصًّا**، فيقيس
مقياسُ التشابه الدلاليِّ اشتراكًا في الشكل ويُحسَب دلالة. وهذه الوحدة تقيس
الأثرَ قبلَ إزالة تلك الأسماء وبعدَها، وتُخرِج أحكامَ التنبّؤات مُشتَقّةً::

    SurfaceLeak        != SemanticSignal
    PosteriorVerdict   != PreregisteredVerdict
    MechanicalRemoval  != CorrectRemoval
    TextualAgreement   != Meaning

**لا تسجيلَ قبليًّا في هذه الشجرة، فلا حكمَ قبليّ.** الجولةُ الواردةُ تُسمّي
`PREREG-6.md` ببصمةٍ بعينها؛ وليس الملفُّ في هذه الشجرة ولا بصمتُه، فلا تُقابَل
التنبّؤاتُ بنصٍّ مُجمَّدٍ قبل البيانات. ولذلك تُقرَأ أحكامُ `S1`–`S4` ههنا
**بَعديّةً** بلا استثناء، ولو طابقت أرقامُها أرقامَ الجولة
(`THE_PREREGISTRATION_IS_NAMED_NOT_DEPOSITED`). ورقمٌ مطابقٌ لتنبّؤٍ لا يُرقّيه
إلى مُتنبَّأٍ به ما لم يُبصَّم التنبّؤُ قبله؛ فالقبليّةُ خاصّيّةُ **ترتيبٍ
موثَّق** لا خاصّيّةُ صياغة.

**القواعدُ تُعلَن قبل الرقم.** المجالُ والتقطيعُ والوزنُ والعدمُ كلُّها
مِقابضُ تُغيّر الرقم، فتُكتَب بنصّها في `THE_DECLARED_PROTOCOL` ويُشتَقّ كلُّ
عددٍ تحتها. وعددُ المجال ههنا **٢٬٩١٦** لا ٣٬٢٥٢، والفرقُ ليس خطأً يُصحَّح بل
قاعدةُ عدٍّ أخرى؛ وعدمُ مطابقةِ الجولة الواردة مُسمًّى ولا يُهندَس حوله
(`THE_DOMAIN_SIZE_DOES_NOT_MATCH_THE_REPORTED_RUN`).

**الإزالةُ آليّةٌ، وإفراطُها مقيسٌ لا مستور.** توليدُ صور أسماء الحروف بلواصقَ
يلتقط كلماتٍ ليست أسماءَ حروف: «كلام» و«وراء» و«لحاء» و«لام». فتُقاس القائمةُ
مرّتين — آليّةً موسَّعة، ومحافِظةً مقصورةً على صور `ال` و`وال` — ويُفحَص أنّ
الحكم **لا ينقلب** بينهما. فثباتُ الحكم تحت تضييق الأداة نتيجةٌ، واختلافُه كان
سيُبطل الاستنتاج (`A_MECHANICAL_REMOVAL_OVER_REMOVES`).

**النتيجةُ مسجَّلةٌ لا مُهندَسٌ حولَها**: التنظيفُ يهبط بكلّ نسبةٍ إلى ما يقارب
نصفَها، فأكثرُ ما كان يُقرَأ دلالةً كان اسمَ حرف. ويبقى بعده أثرٌ موجبٌ في
`C2C3`، ويسقط `S2` مُكذَّبًا، وينقسم `S3` بشقّيه.

**وهذا الصنفُ الثاني لا الثالث.** الطرفُ المقابلُ نصٌّ أيضًا — شرحُ ابن فارس —
لا مدلولٌ مقيسٌ خارجَ اللغة؛ فخانةُ «المدلولِ وحدَه» باقيةٌ فارغةً بنيويًّا
(`THE_SIGNIFIED_ALONE_REMAINS_STRUCTURALLY_EMPTY`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`، ولا تُرفَع بهذه الوحدة منزلةٌ محجوزة.
"""

from __future__ import annotations

import collections
import hashlib
import itertools
import math
import random
import re
import statistics
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .maqayis_root_table_deposit import root_table_rows
from .pipeline_stations import repository_root_path

__all__ = [
    "A_MECHANICAL_REMOVAL_OVER_REMOVES",
    "A_RATIO_IS_RELATIVE_TO_ITS_NULL",
    "CONSERVATIVE_PREFIXES",
    "MECHANICAL_PREFIXES",
    "MAQAYIS_LEAK_AUDIT_NAMED_RESIDUALS",
    "MINIMUM_BODY_LENGTH",
    "MINIMUM_DOCUMENT_FREQUENCY",
    "THE_DECLARED_PROTOCOL",
    "THE_DOMAIN_SIZE_DOES_NOT_MATCH_THE_REPORTED_RUN",
    "THE_LETTER_NAME_STEMS",
    "THE_PREREGISTRATION_IS_NAMED_NOT_DEPOSITED",
    "THE_MAP_IS_ONE_MANS_OPINION_IN_THE_FOURTH_CENTURY",
    "THE_FAIR_TEST_IS_POSTERIOR_AND_SAID_SO",
    "THE_NAMED_PREREGISTRATION",
    "THE_NAMED_PREREGISTRATION_DIGEST",
    "THE_SEMANTIC_AXES_COLUMN_IS_UNUSED_BECAUSE_IT_IS_DEFECTIVE",
    "THE_SIGNIFIED_ALONE_REMAINS_STRUCTURALLY_EMPTY",
    "tokenize",
    "TF_IDF_IS_A_CHOSEN_INSTRUMENT_NOT_A_MEASURED_BASIS",
    "STYLE_IS_NOT_SEPARATED_FROM_MEANING",
    "FamilyResult",
    "LeakVocabulary",
    "MaqayisLeakAuditError",
    "MeasurementProfile",
    "PairFamily",
    "PreregistrationStanding",
    "PredictionStanding",
    "RegisteredPrediction",
    "RootDocument",
    "TfIdfSpace",
    "assess_prediction",
    "assess_preregistration",
    "build_domain",
    "build_space",
    "enumerate_family",
    "leak_vocabulary",
    "matched_excess",
    "measure_family",
]


class MaqayisLeakAuditError(ValueError):
    """خطأٌ في بناء المجال أو في قياسٍ على خريطة ابن فارس."""


# --- البروتوكولُ المُعلَن قبل الرقم ------------------------------------------------


MINIMUM_BODY_LENGTH: Final[int] = 200
"""أدنى طولِ شرحٍ يدخل المجال، بنقاط الشفرة؛ مِقبَضٌ يُعلَن قبل العدد."""

MINIMUM_DOCUMENT_FREQUENCY: Final[int] = 3
"""أدنى تردُّدٍ مستنديٍّ لمفردةٍ تدخل الفضاء؛ ودونَه ضجيجُ فرادى."""

THE_DECLARED_PROTOCOL: Final[str] = (
    "المجالُ: جذرٌ من ثلاث نقاطِ شفرةٍ متمايزةٍ كلُّها، وشرحُه أطولُ من "
    f"{MINIMUM_BODY_LENGTH} محرفًا، مأخوذًا مرّةً واحدةً عند تكرار الجذر. "
    "والتقطيعُ: تُحذَف علاماتُ الشكل والتطويل، ويُقطَع على كلّ ما ليس حرفًا "
    "عربيًّا، وتُسقَط المفرداتُ الأحاديّة. والوزنُ: `tf-idf` بتردُّدٍ لوغاريتميٍّ "
    f"وعكسِ تردُّدٍ مستنديٍّ طبيعيّ، بأدنى تردُّدٍ مستنديٍّ {MINIMUM_DOCUMENT_FREQUENCY}، "
    "ثمّ تسويةٌ إقليديّة. والتشابهُ: جيبُ تمام الزاوية. والعدمُ: خلطُ إسناد "
    "الشروح إلى الجذور، فتُعاد الأزواجُ نفسُها على إسنادٍ مخلوط"
)
"""القواعدُ الأربعُ مكتوبةً بنصّها؛ ورقمٌ بلا قاعدتِه ليس قابلًا لإعادة الاشتقاق."""


_DIACRITICS: Final[re.Pattern[str]] = re.compile("[\u064b-\u0652\u0670\u0640]")
_NON_ARABIC_LETTER: Final[re.Pattern[str]] = re.compile("[^\u0621-\u064a]+")


def tokenize(text: str) -> tuple[str, ...]:
    """قطِّع شرحًا بالقاعدة المُعلَنة؛ ولا تُطبَّق قاعدةٌ غيرُ مكتوبةٍ ههنا."""

    stripped = _DIACRITICS.sub("", text)
    return tuple(word for word in _NON_ARABIC_LETTER.split(stripped) if len(word) > 1)


# --- مفرداتُ التسرُّب --------------------------------------------------------------


THE_LETTER_NAME_STEMS: Final[tuple[str, ...]] = (
    "همزة",
    "الف",
    "ألف",
    "باء",
    "تاء",
    "ثاء",
    "جيم",
    "حاء",
    "خاء",
    "دال",
    "ذال",
    "راء",
    "زاي",
    "زاء",
    "سين",
    "شين",
    "صاد",
    "ضاد",
    "طاء",
    "ظاء",
    "عين",
    "غين",
    "فاء",
    "قاف",
    "كاف",
    "لام",
    "ميم",
    "نون",
    "هاء",
    "واو",
    "ياء",
)
"""أسماءُ الحروف مجرّدةً، بصورتَي الألف المرسومتين؛ وملصوقاتُها تُولَّد.

و«ألف» اسمُ حرفٍ وعددٌ معًا، فإدخالُه يُدخِل معه العددَ؛ وذلك من إفراط
الإزالة المقيس بالقائمة المحافِظة لا من خطأٍ يُصحَّح بانتقاءٍ يدويّ.
"""

MECHANICAL_PREFIXES: Final[tuple[str, ...]] = (
    "",
    "ال",
    "و",
    "وال",
    "ف",
    "فال",
    "ب",
    "بال",
    "ل",
    "لل",
    "ك",
    "كال",
)
"""اللواصقُ المُولَّدُ بها آليًّا؛ وسَعتُها تلتقط كلماتٍ ليست أسماءَ حروف."""

CONSERVATIVE_PREFIXES: Final[tuple[str, ...]] = ("ال", "وال")
"""الصورُ التي تفتتح بها العبارةُ فعلًا؛ قائمةٌ أضيقُ تُقاس بها الحساسيّة."""


class LeakVocabulary(Enum):
    """أيُّ قائمةِ تسرُّبٍ تُستعمَل؛ ثلاثٌ لا اثنتان، والخاليةُ هي الضابط."""

    NONE = "بلا_إزالة"
    CONSERVATIVE = "إزالةٌ_محافِظة"
    MECHANICAL = "إزالةٌ_آليّةٌ_موسَّعة"


def leak_vocabulary(kind: LeakVocabulary) -> frozenset[str]:
    """صورُ أسماء الحروف تحت قائمةٍ بعينها؛ مُولَّدةً لا مكتوبةً واحدةً واحدة."""

    if kind is LeakVocabulary.NONE:
        return frozenset()
    prefixes = (
        CONSERVATIVE_PREFIXES
        if kind is LeakVocabulary.CONSERVATIVE
        else MECHANICAL_PREFIXES
    )
    return frozenset(
        prefix + stem for stem in THE_LETTER_NAME_STEMS for prefix in prefixes
    )


# --- المجالُ وفضاؤه ---------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RootDocument:
    """جذرٌ وشرحُه مقطَّعًا؛ ولا يُكتَب فيه رقمٌ يُقرَأ لاحقًا نتيجة."""

    root: str
    tokens: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.root) != 3:
            raise MaqayisLeakAuditError("المجالُ ثلاثيٌّ مُعلَنٌ؛ وغيرُه خارجَه")
        if len(set(self.root)) != 3:
            raise MaqayisLeakAuditError(
                "جذرٌ فيه حرفان متماثلان لا يُعرَّف عليه اتّفاقُ المواضع تعريفًا واحدًا"
            )


def build_domain() -> tuple[RootDocument, ...]:
    """ابنِ المجالَ من بايتات المقاييس المُبصَّمة تحت البروتوكول المُعلَن."""

    seen: set[str] = set()
    documents: list[RootDocument] = []
    for row in root_table_rows():
        root = row["root_full"]
        body = row["body_text"]
        if len(root) != 3 or len(set(root)) != 3:
            continue
        if len(body) <= MINIMUM_BODY_LENGTH or root in seen:
            continue
        seen.add(root)
        documents.append(RootDocument(root=root, tokens=tokenize(body)))
    if not documents:
        raise MaqayisLeakAuditError("مجالٌ خالٍ لا يُقاس عليه شيء")
    return tuple(documents)


@dataclass(frozen=True, slots=True)
class TfIdfSpace:
    """متّجهاتٌ مُسوّاةٌ ومفرداتُها؛ والتشابهُ يُحسَب ولا يُخزَّن."""

    roots: tuple[str, ...]
    vectors: tuple[dict[str, float], ...]

    @property
    def vocabulary_size(self) -> int:
        """عددُ المفردات الباقية بعد أدنى التردُّد، مُشتقًّا بالعدّ."""

        return len({term for vector in self.vectors for term in vector})

    @property
    def size(self) -> int:
        """عددُ المستندات."""

        return len(self.vectors)

    def cosine(self, left: int, right: int) -> float:
        """جيبُ تمام الزاوية بين متّجهين مُسوّيين؛ فهو حاصلُ ضربهما."""

        first = self.vectors[left]
        second = self.vectors[right]
        if len(first) > len(second):
            first, second = second, first
        return sum(
            weight * second[term] for term, weight in first.items() if term in second
        )


def build_space(
    documents: tuple[RootDocument, ...], removed: frozenset[str]
) -> TfIdfSpace:
    """ابنِ فضاءَ `tf-idf` بعد إسقاط مفردات التسرُّب المُعلَنة."""

    counts: list[collections.Counter[str]] = []
    document_frequency: collections.Counter[str] = collections.Counter()
    for document in documents:
        counter = collections.Counter(
            token for token in document.tokens if token not in removed
        )
        counts.append(counter)
        document_frequency.update(counter.keys())
    total = len(documents)
    kept = {
        term
        for term, frequency in document_frequency.items()
        if frequency >= MINIMUM_DOCUMENT_FREQUENCY
    }
    vectors: list[dict[str, float]] = []
    for counter in counts:
        raw = {
            term: (1.0 + math.log(frequency))
            * math.log(total / document_frequency[term])
            for term, frequency in counter.items()
            if term in kept
        }
        norm = math.sqrt(sum(value * value for value in raw.values())) or 1.0
        vectors.append({term: value / norm for term, value in raw.items()})
    return TfIdfSpace(
        roots=tuple(document.root for document in documents),
        vectors=tuple(vectors),
    )


# --- أفواجُ المقارنة ---------------------------------------------------------------


class PairFamily(Enum):
    """أفواجُ الأزواج المُقارَنة؛ ولكلٍّ ضابطُه المكافئُ حيث يلزم."""

    SHARED_C2C3 = "تشترك_في_الموضعين_الثاني_والثالث"
    SHARED_C1C2 = "تشترك_في_الموضعين_الأوّل_والثاني"
    SHARED_C1C3 = "تشترك_في_الموضعين_الأوّل_والثالث"
    SHARED_C1_ONLY = "تشترك_في_الأوّل_وحدَه"
    PERMUTATION_AGREE_ZERO = "تقليبٌ_باتّفاق_صفرِ_موضع"
    PERMUTATION_AGREE_ONE = "تقليبٌ_باتّفاق_موضعٍ_واحد"
    NON_PERMUTATION_AGREE_ZERO = "غيرُ_تقليبٍ_باتّفاق_صفرِ_موضع"
    NON_PERMUTATION_AGREE_ONE = "غيرُ_تقليبٍ_باتّفاق_موضعٍ_واحد"


def _positional_agreement(left: str, right: str) -> int:
    return sum(1 for first, second in zip(left, right) if first == second)


def _is_permutation(left: str, right: str) -> bool:
    return sorted(left) == sorted(right)


def enumerate_family(
    roots: tuple[str, ...], family: PairFamily, rng: random.Random, cap: int
) -> tuple[tuple[int, int], ...]:
    """عُدَّ أزواجَ فوجٍ بعينه؛ والأفواجُ الضابطةُ تُعايَن بمعاينةٍ مبذورة."""

    if cap < 1:
        raise MaqayisLeakAuditError("سقفُ معاينةٍ دون الواحد لا يُنتج فوجًا")
    if family in (
        PairFamily.NON_PERMUTATION_AGREE_ZERO,
        PairFamily.NON_PERMUTATION_AGREE_ONE,
    ):
        wanted = 0 if family is PairFamily.NON_PERMUTATION_AGREE_ZERO else 1
        found: list[tuple[int, int]] = []
        attempts = 0
        limit = cap * 400
        while len(found) < cap and attempts < limit:
            attempts += 1
            left = rng.randrange(len(roots))
            right = rng.randrange(len(roots))
            if left == right or _is_permutation(roots[left], roots[right]):
                continue
            if _positional_agreement(roots[left], roots[right]) == wanted:
                found.append((left, right))
        return tuple(found)

    buckets: dict[str, list[int]] = collections.defaultdict(list)
    for index, root in enumerate(roots):
        if family is PairFamily.SHARED_C2C3:
            buckets[root[1:]].append(index)
        elif family is PairFamily.SHARED_C1C2:
            buckets[root[:2]].append(index)
        elif family is PairFamily.SHARED_C1C3:
            buckets[root[0] + root[2]].append(index)
        elif family is PairFamily.SHARED_C1_ONLY:
            buckets[root[0]].append(index)
        else:
            buckets["".join(sorted(root))].append(index)

    pairs: list[tuple[int, int]] = []
    for members in buckets.values():
        for left, right in itertools.combinations(members, 2):
            first = roots[left]
            second = roots[right]
            if family is PairFamily.SHARED_C2C3 and first[0] == second[0]:
                continue
            if family is PairFamily.SHARED_C1C2 and first[2] == second[2]:
                continue
            if family is PairFamily.SHARED_C1C3 and first[1] == second[1]:
                continue
            if family is PairFamily.SHARED_C1_ONLY and (
                first[1] == second[1] or first[2] == second[2]
            ):
                continue
            if family is PairFamily.PERMUTATION_AGREE_ZERO:
                if _positional_agreement(first, second) != 0:
                    continue
            if family is PairFamily.PERMUTATION_AGREE_ONE:
                if _positional_agreement(first, second) != 1:
                    continue
            pairs.append((left, right))
    if len(pairs) > cap:
        pairs = rng.sample(pairs, cap)
    return tuple(pairs)


# --- القياسُ وعدمُه ---------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MeasurementProfile:
    """مِقابضُ القياس مكتوبةً: سقفُ المعاينة، وعددُ إعاداتِ العدم، والبذرة."""

    sample_cap: int = 15000
    replicates: int = 200
    seed: int = 20260920

    def __post_init__(self) -> None:
        if self.sample_cap < 1:
            raise MaqayisLeakAuditError("سقفُ معاينةٍ دون الواحد لا يُنتج فوجًا")
        if self.replicates < 2:
            raise MaqayisLeakAuditError(
                "عدمٌ بإعادةٍ واحدةٍ لا انحرافَ له، فلا يُشتَقّ منه `Z`"
            )


@dataclass(frozen=True, slots=True)
class FamilyResult:
    """نتيجةُ فوجٍ: الملاحَظُ وعدمُه، والنسبةُ و`Z` **مُشتقّتان** لا مكتوبتان."""

    family: PairFamily
    pair_count: int
    observed_mean: float
    null_means: tuple[float, ...]

    def __post_init__(self) -> None:
        if self.pair_count < 1:
            raise MaqayisLeakAuditError("فوجٌ خالٍ لا متوسّطَ له، ولا يُقرَأ صفرًا")
        if len(self.null_means) < 2:
            raise MaqayisLeakAuditError("عدمٌ بأقلَّ من إعادتين لا انحرافَ له")

    @property
    def null_mean(self) -> float:
        """متوسّطُ العدم، محسوبًا عند كلّ قراءة."""

        return statistics.fmean(self.null_means)

    @property
    def null_sd(self) -> float:
        """انحرافُ العدم؛ وصفرُه يُسمّى ولا يُقسَم عليه."""

        return statistics.pstdev(self.null_means)

    @property
    def ratio(self) -> float:
        """نسبةُ الملاحَظ إلى العدم؛ ولا معنى لها خارج عدمِها المُعلَن."""

        null = self.null_mean
        if null <= 0.0:
            raise MaqayisLeakAuditError("عدمٌ غيرُ موجبٍ لا تُقسَم عليه نسبة")
        return self.observed_mean / null

    @property
    def z_score(self) -> float:
        """`Z` مُشتقًّا؛ وانعدامُ الانحراف يُرفَع به خطأٌ ولا يُقرَأ لانهاية."""

        sd = self.null_sd
        if sd <= 0.0:
            raise MaqayisLeakAuditError("انحرافُ عدمٍ صفرٌ؛ و`Z` عليه ليس رقمًا يُقرَأ دلالةً")
        return (self.observed_mean - self.null_mean) / sd


def measure_family(
    space: TfIdfSpace,
    pairs: tuple[tuple[int, int], ...],
    family: PairFamily,
    profile: MeasurementProfile,
) -> FamilyResult:
    """قِس فوجًا وقابِله بعدمٍ يُبنى بخلط إسناد الشروح إلى الجذور."""

    if not pairs:
        raise MaqayisLeakAuditError(f"فوجُ «{family.value}» خالٍ، فلا يُقاس")
    observed = statistics.fmean(space.cosine(left, right) for left, right in pairs)
    rng = random.Random(profile.seed + 1)
    order = list(range(space.size))
    null_means: list[float] = []
    for _ in range(profile.replicates):
        rng.shuffle(order)
        null_means.append(
            statistics.fmean(
                space.cosine(order[left], order[right]) for left, right in pairs
            )
        )
    return FamilyResult(
        family=family,
        pair_count=len(pairs),
        observed_mean=observed,
        null_means=tuple(null_means),
    )


def matched_excess(permutation: FamilyResult, control: FamilyResult) -> float:
    """فائضُ التقليب فوقَ ضابطِه عند نفس عدد المواضع المتّفقة.

    وهذا هو الاختبارُ العادلُ لدعوى الاشتقاق الكبير، وهو **مُعلَنٌ بَعديًّا**:
    لم يكن في الصياغة الواردة، فلا يُقرَأ تنبّؤًا صمد
    (`THE_FAIR_TEST_IS_POSTERIOR_AND_SAID_SO`).
    """

    return permutation.ratio / control.ratio - 1.0


# --- التنبّؤاتُ وأحكامُها -----------------------------------------------------------


class RegisteredPrediction(Enum):
    """التنبّؤاتُ الأربعةُ كما وردت في الجولة؛ منقولةً لا مُصحَّحة."""

    S1_MINOR_DERIVATION = "الاشتقاقُ_الأصغر"
    S2_POSITIONAL_ORDER = "ترتيبُ_الأزواج_الموضعيّة"
    S3_MAJOR_DERIVATION = "الاشتقاقُ_الكبير"
    S4_PERMUTATION_EXCEEDS_POSITIONAL = "أثرُ_التقليب_فوقَ_الزوج_الموضعيّ"


class PredictionStanding(Enum):
    """منازلُ الحكم؛ خمسٌ لا اثنتان، فالانقسامُ والامتناعُ ليسا سقوطًا عاديًّا."""

    HELD = "صمد"
    REFUTED = "مُكذَّب"
    SPLIT = "صمد_بشقٍّ_وسقط_بشقّ"
    ILL_POSED_SO_NOT_TESTABLE = "غيرُ_قابلٍ_للاختبار_لعيبٍ_في_صياغته"


_RATIO_FLOOR: Final[float] = 1.20
_Z_FLOOR: Final[float] = 3.0


def assess_prediction(
    prediction: RegisteredPrediction, results: dict[PairFamily, FamilyResult]
) -> PredictionStanding:
    """احكم على تنبّؤٍ من نتائج أفواجه؛ والمنزلةُ تُشتَقّ ولا تُكتَب.

    والعتبتان (`1.20` و`Z>3`) منقولتان من الجولة الواردة بنصّهما، ولا تُلائَمان
    بعد رؤية الرقم.
    """

    def passes(family: PairFamily) -> bool:
        result = results[family]
        return result.ratio >= _RATIO_FLOOR and result.z_score > _Z_FLOOR

    if prediction is RegisteredPrediction.S1_MINOR_DERIVATION:
        return (
            PredictionStanding.HELD
            if passes(PairFamily.SHARED_C2C3)
            else PredictionStanding.REFUTED
        )
    if prediction is RegisteredPrediction.S2_POSITIONAL_ORDER:
        first = results[PairFamily.SHARED_C1C2].ratio
        middle = results[PairFamily.SHARED_C2C3].ratio
        last = results[PairFamily.SHARED_C1C3].ratio
        return (
            PredictionStanding.HELD
            if first > middle > last
            else PredictionStanding.REFUTED
        )
    if prediction is RegisteredPrediction.S3_MAJOR_DERIVATION:
        one = passes(PairFamily.PERMUTATION_AGREE_ONE)
        zero = passes(PairFamily.PERMUTATION_AGREE_ZERO)
        if one and zero:
            return PredictionStanding.HELD
        if one or zero:
            return PredictionStanding.SPLIT
        return PredictionStanding.REFUTED
    return PredictionStanding.ILL_POSED_SO_NOT_TESTABLE


# --- التسجيلُ القبليُّ وحالُه ------------------------------------------------------


class PreregistrationStanding(Enum):
    """أقبليٌّ هذا الحكمُ أم بَعديّ؟ يُقرَأ من إيداع الوثيقة لا من دعوى."""

    VERIFIED_AGAINST_A_DEPOSITED_DOCUMENT = "مُقابَلٌ_بوثيقةٍ_مُودَعة"
    POSTERIOR_FOR_WANT_OF_A_DEPOSITED_DOCUMENT = "بَعديٌّ_لانعدام_وثيقةٍ_مُودَعة"


THE_NAMED_PREREGISTRATION: Final[str] = "PREREG-6.md"
"""اسمُ الوثيقة كما ورد؛ تسميةٌ لا إيداع، فالبصمةُ لا تُقابَل بشيء."""

THE_NAMED_PREREGISTRATION_DIGEST: Final[str] = (
    "8bbf2a99f40d5273efb51e2c8fdb6a599517b9a53fceb0ab3ae45cf25d0dd23e"
)
"""البصمةُ المُعلَنةُ في الجولة؛ مكتوبةٌ لتُقابَل متى أُودِعت بايتاتُها."""


def assess_preregistration() -> PreregistrationStanding:
    """اقرأ حالَ التسجيل القبليّ الآن؛ وغيابُ الوثيقة يُقرَأ بَعديّةً لا ثقة."""

    candidate = repository_root_path() / THE_NAMED_PREREGISTRATION
    if not candidate.is_file():
        return PreregistrationStanding.POSTERIOR_FOR_WANT_OF_A_DEPOSITED_DOCUMENT
    digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
    if digest != THE_NAMED_PREREGISTRATION_DIGEST:
        return PreregistrationStanding.POSTERIOR_FOR_WANT_OF_A_DEPOSITED_DOCUMENT
    return PreregistrationStanding.VERIFIED_AGAINST_A_DEPOSITED_DOCUMENT


# --- البقايا المُسمّاة -------------------------------------------------------------


THE_PREREGISTRATION_IS_NAMED_NOT_DEPOSITED: Final[str] = (
    "THE_PREREGISTRATION_IS_NAMED_NOT_DEPOSITED: `PREREG-6.md` مُسمًّى ببصمةٍ "
    "وليس في هذه الشجرة، فلا تُقابَل التنبّؤاتُ بنصٍّ مُجمَّدٍ قبل البيانات؛ "
    "وكلُّ حكمٍ ههنا بَعديٌّ ولو طابق رقمُه رقمَ الجولة"
)

THE_DOMAIN_SIZE_DOES_NOT_MATCH_THE_REPORTED_RUN: Final[str] = (
    "THE_DOMAIN_SIZE_DOES_NOT_MATCH_THE_REPORTED_RUN: مجالُ هذه الوحدة ٢٬٩١٦ "
    "جذرًا لا ٣٬٢٥٢، فقاعدةُ العدّ ههنا غيرُ قاعدتها؛ والفرقُ مُسمًّى ولا "
    "تُلائَم القاعدةُ لتبلغَ عددَها"
)

A_MECHANICAL_REMOVAL_OVER_REMOVES: Final[str] = (
    "A_MECHANICAL_REMOVAL_OVER_REMOVES: توليدُ صور أسماء الحروف بلواصقَ يلتقط "
    "«كلام» و«وراء» و«لحاء» و«لام» وهي ليست أسماءَ حروف؛ فالإفراطُ مقيسٌ "
    "بالقائمة المحافِظة ولا يُصحَّح بانتقاءٍ يدويٍّ بعد رؤية النتيجة"
)

A_RATIO_IS_RELATIVE_TO_ITS_NULL: Final[str] = (
    "A_RATIO_IS_RELATIVE_TO_ITS_NULL: النسبةُ خارجُ قسمةٍ على عدمٍ مُعلَن، "
    "فتغييرُ العدم يغيّرها بلا أن يتغيّر شيءٌ في اللغة؛ ولا تُقرَأ مقدارًا "
    "مطلقًا للتشابه"
)

TF_IDF_IS_A_CHOSEN_INSTRUMENT_NOT_A_MEASURED_BASIS: Final[str] = (
    "TF_IDF_IS_A_CHOSEN_INSTRUMENT_NOT_A_MEASURED_BASIS: الوزنُ والتقطيعُ "
    "وأدنى التردُّد مِقابضُ مختارةٌ تُغيّر كلَّ رقمٍ ههنا؛ فالمقيسُ توافقٌ "
    "معجميٌّ تحت أداةٍ بعينها لا «معنًى» قِيس"
)

STYLE_IS_NOT_SEPARATED_FROM_MEANING: Final[str] = (
    "STYLE_IS_NOT_SEPARATED_FROM_MEANING: المتنُ كلُّه لمؤلّفٍ واحدٍ بأسلوبٍ "
    "واحد، فبعضُ التشابه المقيس أسلوبٌ لا معنى؛ ولم يُفصَل الأسلوبُ ههنا ولا "
    "يُدَّعى أنّه فُصِل"
)

THE_MAP_IS_ONE_MANS_OPINION_IN_THE_FOURTH_CENTURY: Final[str] = (
    "THE_MAP_IS_ONE_MANS_OPINION_IN_THE_FOURTH_CENTURY: الخريطةُ رأيُ ابن "
    "فارس، والبصمةُ توثّق الملفَّ لا المطبوعَ الذي استُخرج منه ولا صحّةَ "
    "الاستخراج؛ فالمقيسُ توافقُ الشكلِ مع شرحه هو، لا مع العربية"
)

THE_FAIR_TEST_IS_POSTERIOR_AND_SAID_SO: Final[str] = (
    "THE_FAIR_TEST_IS_POSTERIOR_AND_SAID_SO: مقابلةُ التقليب بغير التقليب عند "
    "نفس عدد المواضع المتّفقة لم تكن في الصياغة الواردة؛ فهي اختبارٌ بَعديٌّ "
    "مُعلَنٌ بَعديّتُه، ولا يُقرَأ تنبّؤًا صمد"
)

THE_SEMANTIC_AXES_COLUMN_IS_UNUSED_BECAUSE_IT_IS_DEFECTIVE: Final[str] = (
    "THE_SEMANTIC_AXES_COLUMN_IS_UNUSED_BECAUSE_IT_IS_DEFECTIVE: عمودُ "
    "`semantic_axes` لم يُستعمَل ههنا لخلوِّ كثيرٍ من صفوفه وتفرُّدِ أكثر "
    "وسومه؛ وتركُه اختيارٌ مكتوبٌ لا إغفال"
)

THE_SIGNIFIED_ALONE_REMAINS_STRUCTURALLY_EMPTY: Final[str] = (
    "THE_SIGNIFIED_ALONE_REMAINS_STRUCTURALLY_EMPTY: الطرفُ المقابلُ نصٌّ — "
    "شرحُ ابن فارس — لا مدلولٌ مقيسٌ خارجَ اللغة؛ فهذا الصنفُ الثاني، وخانةُ "
    "«المدلولِ وحدَه» باقيةٌ فارغةً بنيويًّا لا مؤجَّلةً لعملٍ أكثر"
)

MAQAYIS_LEAK_AUDIT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_PREREGISTRATION_IS_NAMED_NOT_DEPOSITED": (
        THE_PREREGISTRATION_IS_NAMED_NOT_DEPOSITED
    ),
    "THE_DOMAIN_SIZE_DOES_NOT_MATCH_THE_REPORTED_RUN": (
        THE_DOMAIN_SIZE_DOES_NOT_MATCH_THE_REPORTED_RUN
    ),
    "A_MECHANICAL_REMOVAL_OVER_REMOVES": A_MECHANICAL_REMOVAL_OVER_REMOVES,
    "A_RATIO_IS_RELATIVE_TO_ITS_NULL": A_RATIO_IS_RELATIVE_TO_ITS_NULL,
    "TF_IDF_IS_A_CHOSEN_INSTRUMENT_NOT_A_MEASURED_BASIS": (
        TF_IDF_IS_A_CHOSEN_INSTRUMENT_NOT_A_MEASURED_BASIS
    ),
    "STYLE_IS_NOT_SEPARATED_FROM_MEANING": STYLE_IS_NOT_SEPARATED_FROM_MEANING,
    "THE_MAP_IS_ONE_MANS_OPINION_IN_THE_FOURTH_CENTURY": (
        THE_MAP_IS_ONE_MANS_OPINION_IN_THE_FOURTH_CENTURY
    ),
    "THE_FAIR_TEST_IS_POSTERIOR_AND_SAID_SO": THE_FAIR_TEST_IS_POSTERIOR_AND_SAID_SO,
    "THE_SEMANTIC_AXES_COLUMN_IS_UNUSED_BECAUSE_IT_IS_DEFECTIVE": (
        THE_SEMANTIC_AXES_COLUMN_IS_UNUSED_BECAUSE_IT_IS_DEFECTIVE
    ),
    "THE_SIGNIFIED_ALONE_REMAINS_STRUCTURALLY_EMPTY": (
        THE_SIGNIFIED_ALONE_REMAINS_STRUCTURALLY_EMPTY
    ),
}
"""ما لا تحسمه هذه الجولة، مُسمًّى هنا لا متروكًا ليُفترَض."""
