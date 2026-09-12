"""الوضعُ بشريٌّ لا توقيفيّ، ولا يُعرَف إلا بالنقل (الحلقة الرابعة من سلسلة القرار).

الحلقتان الثالثتان تفترقان ولا تلتقيان تلقائيًّا: **الدالُّ وحده** تحليلٌ توزيعيٌّ
إحصائيّ (`distributional_probe_report`)، و**المدلولُ وحده** تحليلٌ فلسفيٌّ صوريّ
(`madlul_alone_formal` وأخواتها)، وليس في واحدةٍ منهما لفظٌ بعينه مقترنٌ بمعنًى
بعينه. واقترانُهما هو **الوضع**، وهذه الوحدة موضعُه::

    Wad              != DerivedFromDistribution
    Wad              != DerivedFromMadlulAnalysis
    DistributionalTrace != WadPath

**والوضعُ من وضع البشر ليس من الله**، ببرهانٍ ثنائيّ لا يقوم بشِقٍّ واحد: لا
طريقَ إليه بالوحي (دورٌ محال، إذ الوحيُ نفسه لا يُفهَم إلا بلغةٍ سابقةٍ عليه)،
ولا بعلمٍ ضروريّ (إذ يستلزم معرفةَ الله بالضرورة، وهو خلافُ الواقع المشاهَد).
و«وعلَّم آدم الأسماء كلها» تعليمُ **حقائق الأشياء وخواصّها** — مفهومٌ مباشر:
معنًى وواقعٌ مُدرَك على معنى `ContentStanding.مفهوم` — لا تعليمُ ألفاظ.

**المصدر النصّي — يُذكَر بالاسم لا إحالةً مبهمة** — كتاب "الشخصية الإسلامية"
الجزء الأول، لتقي الدين النبهاني، مبحث "الوضع":

    "وأما الواضع للغات فهو أن اللغات كلها اصطلاحية، فهي من وضع الناس، وليست من
    وضع الله... وأما قوله تعالى ﴿وعلَّم آدم الأسماء كلها﴾ فإن المراد منه
    مسمّيات الأشياء لا اللغات، أي علّمه حقائق الأشياء وخواصها... فسياق الآية
    يدل على أن المراد من كلمة ﴿الأسماء كلها﴾ المسمَّيات، أي الحقائق
    والخواص... وبذلك يتبين أنه لا يوجد دليل شرعي على أن اللغات توقيفية من
    الله، بل الواقع المشاهد أنها اصطلاح من الناس، فهي من وضع البشر وليست من
    الله"

وكلُّ شِقٍّ من البرهان، وكلُّ قراءةٍ لتعليم آدم، يلزمه اقتباسٌ **منقولٌ بنصّه**
من هذا النصّ نفسه، يُتحقَّق منه بالاحتواء لا بالتصديق — على منوال الشهادات
الصورية في `word_class_formal` وأخواتها.

**وأثرُ الوضع غيرُ طريقِ معرفته، ولا يُطوى أحدُهما في الآخر.** فالوضعُ — بوصفه
حدثًا تاريخيًّا بشريًّا واصطلاحًا جمعيًّا مستقرًّا — يترك أثرًا توزيعيًّا حقيقيًّا
في الاستعمال، وهذا بعينه ما يصفه `ONLY_LEGITIMATE_TARGET_NOTE` في
`maluma_mafhum`، وهو صحيحٌ في مجاله ولا يُمَسّ. لكنّ **معرفتنا بأيّ لفظٍ اقترن
بأيّ معنى** لا تُشتَقّ من رصد الأثر، لأن انتظامًا إحصائيًّا مماثلًا قد ينشأ عن
تكرارٍ عرضيٍّ أو تحيّزِ عيّنة. فالإحصاء **يُصادِق على وضعٍ معروفٍ بالنقل مسبقًا
فيرفع درايةً، ولا يكتشف وضعًا من الصفر فيصنع روايةً**.

**وهذه الوحدة تسجيلٌ وشهادةُ مصدر، لا سلطة**: لا تُصدر ولادةً ولا تجميدًا ولا
`E0`، ولا تقرؤها وحدةٌ في `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .text_key import comparison_key
from .transmission_standing import TransmissionStanding

__all__ = [
    "ADAM_TEACHING_EVIDENCE",
    "BOTH_GROUNDS_ARE_REQUIRED_NOTE",
    "DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH_NOTE",
    "HUMAN_WAD_IS_NOT_ARBITRARY_CHOICE_NOTE",
    "NAQL_IS_NOT_SANCTITY_NOTE",
    "REFUSED_DERIVATION_NOTES",
    "STATISTICS_RAISE_DIRAYA_NEVER_MAKE_RIWAYA_NOTE",
    "WAD_NAQL_IS_NOT_A_GATE_NOTE",
    "WAD_SOURCE",
    "WAD_SOURCE_TEXT",
    "RECORDED_TAWQIF_REFUTATION",
    "RECORDED_ADAM_TEACHING_READING",
    "AdamTeachingReading",
    "AdamTeachingRecord",
    "DistributionalCorroboration",
    "RefutationGround",
    "StatisticalFunction",
    "TawqifRefutation",
    "TawqifRefutationGround",
    "WadNaqlError",
    "WadOrigin",
    "WadRecord",
    "WadDerivationRefusal",
    "refuse_derivation",
]


class WadNaqlError(ValueError):
    """رفضٌ صريحٌ في وحدة الوضع والنقل؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


class WadOrigin(Enum):
    """واضعُ اللغة؛ مفردةٌ ثنائيةٌ مغلقةٌ لا ثالثَ لها ولا درجةَ بينهما."""

    وضع_بشري = "وضع_بشري"
    توقيف_إلهي = "توقيف_إلهي"


class TawqifRefutationGround(Enum):
    """شِقّا البرهان على نفي التوقيف؛ مفردةٌ ثنائيةٌ مغلقة، والشِّقّان لازمان معًا."""

    لا_طريق_بالوحي = "لا_طريق_بالوحي"
    لا_طريق_بعلم_ضروري = "لا_طريق_بعلم_ضروري"


class AdamTeachingReading(Enum):
    """قراءتا «وعلَّم آدم الأسماء»؛ مفردةٌ ثنائيةٌ مغلقة، والمُثبَتةُ منهما واحدة."""

    حقائق_الأشياء_وخواصها = "حقائق_الأشياء_وخواصها"
    ألفاظ_اللغة = "ألفاظ_اللغة"


class WadDerivationRefusal(Enum):
    """طريقانِ مرفوضان لمعرفة الوضع؛ رفضُهما بالإنشاء لا بالتحذير."""

    استنباط_من_التحليل_التوزيعي = "استنباط_من_التحليل_التوزيعي"
    استنباط_من_تحليل_المدلول = "استنباط_من_تحليل_المدلول"


class StatisticalFunction(Enum):
    """وظيفةُ الإحصاء تجاه الوضع؛ إحداهما قائمةٌ والأخرى ممتنعةٌ بنيويًّا."""

    يرفع_دراية = "يرفع_دراية"
    يصنع_رواية = "يصنع_رواية"


WAD_SOURCE: Final[str] = (
    "الشخصية الإسلامية، الجزء الأول، تقي الدين النبهاني، مبحث الوضع"
)

WAD_SOURCE_TEXT: Final[str] = (
    "وأما الواضع للغات فهو أن اللغات كلها اصطلاحية، فهي من وضع الناس، وليست من "
    "وضع الله... وأما قوله تعالى ﴿وعلَّم آدم الأسماء كلها﴾ فإن المراد منه "
    "مسمّيات الأشياء لا اللغات، أي علّمه حقائق الأشياء وخواصها... فسياق الآية "
    "يدل على أن المراد من كلمة ﴿الأسماء كلها﴾ المسمَّيات، أي الحقائق "
    "والخواص... وبذلك يتبين أنه لا يوجد دليل شرعي على أن اللغات توقيفية من "
    "الله، بل الواقع المشاهد أنها اصطلاح من الناس، فهي من وضع البشر وليست من "
    "الله"
)

BOTH_GROUNDS_ARE_REQUIRED_NOTE: Final[str] = (
    "البرهانُ على نفي التوقيف ثنائيٌّ لا يقوم بشِقٍّ واحد: من أتى بنفي طريق "
    "الوحي وحده بقي عليه احتمالُ العلم الضروري، ومن أتى بنفي العلم الضروري "
    "وحده بقي عليه احتمالُ الوحي. فإعلانُ `وضع_بشري` بشِقٍّ واحدٍ استنفادٌ لم "
    "يقع، ويفشل عنده الإنشاء لا يصدر عنه تحذير."
)

HUMAN_WAD_IS_NOT_ARBITRARY_CHOICE_NOTE: Final[str] = (
    "بشريّةُ الوضع لا تُنزِله إلى اختيارٍ اعتباطيّ: هو اصطلاحٌ جمعيٌّ مستقرٌّ "
    "وقع فعلاً في تاريخٍ بعينه، فيُنقَل كما وقع ولا يُخترَع كما يُشتهى. "
    "و`HumanWad != ArbitraryChoice` على منوال `KnotNotEssence` في طرفه "
    "الآخر: لا كشفُ كنهٍ كامن، ولا اختيارٌ بلا قيد."
)

NAQL_IS_NOT_SANCTITY_NOTE: Final[str] = (
    "لا يُعرَف الوضعُ بالنقل لقداسته، بل لعرضيّته التاريخية البحتة: حدثٌ "
    "بشريٌّ ماضٍ لا يُستنبَط بعقلٍ ولا يُقاس عليه، فلا طريقَ إليه إلا خبرُ من "
    "شهده أو نقل عمّن شهده. و`Naql != Sanctity`."
)

DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH_NOTE: Final[str] = (
    "أثرُ الوضع غيرُ طريقِ معرفته: الاصطلاحُ الجمعيُّ المستقرّ يُخلِّف بالضرورة "
    "انتظامًا توزيعيًّا حقيقيًّا في الاستعمال، وهو ما يصفه "
    "`ONLY_LEGITIMATE_TARGET_NOTE` وصفًا صحيحًا في مجاله. لكنّ الانتظام "
    "المماثل قد ينشأ عن تكرارٍ عرضيٍّ أو تحيّزِ عيّنة، فلا يُشتَقّ منه **أيُّ "
    "لفظٍ اقترن بأيّ معنى**. فالنصّان صحيحان معًا في مجالَيهما، وهذا الحدُّ "
    "يفصلهما ولا يُصحِّح أحدَهما."
)

STATISTICS_RAISE_DIRAYA_NEVER_MAKE_RIWAYA_NOTE: Final[str] = (
    "الإحصاءُ يُصادِق على وضعٍ معروفٍ بالنقل مسبقًا فيرفع درايةً، ولا يكتشف "
    "وضعًا من الصفر فيصنع روايةً. ولذلك تُبنى المصادقةُ على سجلٍّ قائمٍ لا "
    "تُنشئه، ولا تُغيِّر درجةَ نقله."
)

REFUSED_DERIVATION_NOTES: Final[dict[WadDerivationRefusal, str]] = {
    WadDerivationRefusal.استنباط_من_التحليل_التوزيعي: (
        "التحليلُ التوزيعيّ (الحلقة ٣أ) يعرف علاقاتِ الحوامل والحالات فيما "
        "بينها، ولا يعرف لفظًا بعينه مقترنًا بمعنًى بعينه؛ فاشتقاقُ الوضع منه "
        "خروجٌ من مجاله."
    ),
    WadDerivationRefusal.استنباط_من_تحليل_المدلول: (
        "التحليلُ الفلسفيّ للمدلول (الحلقة ٣ب) يعرف الكنهَ والخاصّةَ والصفةَ "
        "والقابليةَ والعلاقة، ولا يعرف أيّ لفظٍ بعينه؛ فاشتقاقُ الوضع منه "
        "خروجٌ من مجاله."
    ),
}

WAD_NAQL_IS_NOT_A_GATE_NOTE: Final[str] = (
    "شهادةُ مصدرٍ وتسجيلٌ لا سلطة: لا تُصدر هذه الوحدة ولادةً ولا حكمَ ولادة "
    "ولا تجميدًا ولا `E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ "
    "فيه."
)

_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "count",
    "number",
    "total",
    "verdict",
    "birth",
    "freeze",
    "rank",
)

_WAD_RECORD_FORBIDDEN_MARKERS: Final[tuple[str, ...]] = (
    "distribution",
    "cluster",
    "frequency",
    "probe",
    "silhouette",
    "corpus",
)


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WadNaqlError(f"{label} نصٌّ غير فارغ.")
    return value


def _require_attested(excerpt: str, label: str) -> str:
    """اشترط أن يكون الاقتباس منقولًا بنصّه من نصّ المصدر المُثبَت."""

    _require_non_blank(excerpt, label)
    if comparison_key(excerpt) not in comparison_key(WAD_SOURCE_TEXT):
        raise WadNaqlError(
            f"{label} يلزمه نقلٌ بنصّه من نصّ المصدر المُثبَت؛ ونصٌّ لا يرِد "
            "فيه شاهدٌ مُدَّعًى لا شاهدٌ مُثبَت."
        )
    return excerpt


def refuse_derivation(path: WadDerivationRefusal) -> None:
    """ارفض طريقَ استنباطٍ للوضع من الحلقة ٣أ أو ٣ب؛ دالّةٌ ترفع دائمًا."""

    if not isinstance(path, WadDerivationRefusal):
        raise WadNaqlError("الطريقُ المرفوض من مفردته المغلقة الثنائية.")
    raise WadNaqlError(REFUSED_DERIVATION_NOTES[path])


@dataclass(frozen=True, slots=True)
class RefutationGround:
    """شِقٌّ واحدٌ من برهان نفي التوقيف، باقتباسه المنقول وبيانِ وجهه."""

    ground: TawqifRefutationGround
    excerpt: str
    argument: str

    def __post_init__(self) -> None:
        if not isinstance(self.ground, TawqifRefutationGround):
            raise WadNaqlError("شِقُّ البرهان من مفردته المغلقة الثنائية.")
        _require_attested(self.excerpt, "اقتباسُ الشِّقّ")
        _require_non_blank(self.argument, "وجهُ الشِّقّ")


@dataclass(frozen=True, slots=True)
class TawqifRefutation:
    """برهانُ نفي التوقيف؛ والواضعُ يُشتَقّ منه ولا يُكتَب في حقل."""

    source: str
    grounds: tuple[RefutationGround, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.source, "المصدر")
        if self.source != WAD_SOURCE:
            raise WadNaqlError(
                "المصدرُ هو المصدرُ المُسمّى بعينه؛ واسمٌ حرٌّ لا يصلح شاهدًا."
            )
        if not isinstance(self.grounds, tuple):
            raise WadNaqlError("شِقّا البرهان سلسلةٌ مُجمَّدة.")
        declared = tuple(item.ground for item in self.grounds)
        if len(set(declared)) != len(declared):
            raise WadNaqlError("شِقٌّ مُعادٌ باسمه نفسه ليس شِقًّا ثانيًا.")
        if set(declared) != set(TawqifRefutationGround):
            raise WadNaqlError(BOTH_GROUNDS_ARE_REQUIRED_NOTE)

    @property
    def origin(self) -> WadOrigin:
        """الواضعُ مُشتَقًّا من استنفاد الشِّقّين، لا مُعلَنًا في حقل."""

        return WadOrigin.وضع_بشري


@dataclass(frozen=True, slots=True)
class AdamTeachingRecord:
    """قراءةُ «وعلَّم آدم الأسماء»: المُعلَّمُ حقائقُ الأشياء لا ألفاظُ اللغة."""

    reading: AdamTeachingReading
    excerpt: str

    def __post_init__(self) -> None:
        if not isinstance(self.reading, AdamTeachingReading):
            raise WadNaqlError("قراءةُ الآية من مفردتها المغلقة الثنائية.")
        if self.reading is AdamTeachingReading.ألفاظ_اللغة:
            raise WadNaqlError(
                "قراءةُ «الأسماء» ألفاظًا مرفوضةٌ بنصّ المصدر نفسه: «المراد منه "
                "مسمّيات الأشياء لا اللغات»؛ فلا تُسجَّل قراءةً ثانيةً قائمة."
            )
        _require_attested(self.excerpt, "اقتباسُ القراءة")

    @property
    def teaches_realities_not_lexemes(self) -> bool:
        """المُعلَّمُ حقائقُ الأشياء وخواصُّها، وهو مفهومٌ مباشر لا لفظ."""

        return True


@dataclass(frozen=True, slots=True)
class WadRecord:
    """وضعٌ مُسجَّل: اقترانُ لفظٍ بمدلولٍ مع طريق معرفته نقلًا وحده."""

    lafz: str
    madlul: str
    naql_source: str
    transmission: TransmissionStanding

    def __post_init__(self) -> None:
        _require_non_blank(self.lafz, "اللفظ")
        _require_non_blank(self.madlul, "المدلول")
        _require_non_blank(self.naql_source, "مصدرُ النقل")
        if not isinstance(self.transmission, TransmissionStanding):
            raise WadNaqlError(
                "طريقُ معرفة الوضع من مفردة `TransmissionStanding` وحدها "
                "(متواتر/آحاد/فرض)، مستوردةً لا منسوخة."
            )

    @property
    def origin(self) -> WadOrigin:
        """كلُّ وضعٍ مُسجَّلٍ هنا بشريٌّ بالاشتقاق، لا بإعلانٍ في حقل."""

        return WadOrigin.وضع_بشري

    @property
    def known_only_by_naql(self) -> bool:
        """لا طريقَ إلى هذا الاقتران إلا النقل؛ وهي حالٌ بنيويةٌ لا خيار."""

        return True


@dataclass(frozen=True, slots=True)
class DistributionalCorroboration:
    """مصادقةٌ توزيعيةٌ على وضعٍ **قائمٍ بالنقل**، لا اكتشافُ وضعٍ من الصفر."""

    wad: WadRecord
    probe_reference: str
    observed_regularity: str

    def __post_init__(self) -> None:
        if not isinstance(self.wad, WadRecord):
            raise WadNaqlError(
                "المصادقةُ تقع على وضعٍ مُسجَّلٍ بالنقل سابقًا؛ ومصادقةٌ بلا "
                "منقولٍ تُصادِق عليه دعوى اكتشافٍ لا مصادقة."
            )
        _require_non_blank(self.probe_reference, "مرجعُ المسبار")
        _require_non_blank(self.observed_regularity, "الانتظامُ المرصود")

    @property
    def function(self) -> StatisticalFunction:
        """وظيفةُ الإحصاء مُشتَقّةٌ ثابتة: يرفع درايةً ولا يصنع روايةً."""

        return StatisticalFunction.يرفع_دراية

    @property
    def transmission_after_corroboration(self) -> TransmissionStanding:
        """درجةُ النقل بعد المصادقة هي درجتُها قبلها؛ فلا رفعَ بالإحصاء."""

        return self.wad.transmission


RECORDED_TAWQIF_REFUTATION: Final[TawqifRefutation] = TawqifRefutation(
    source=WAD_SOURCE,
    grounds=(
        RefutationGround(
            ground=TawqifRefutationGround.لا_طريق_بالوحي,
            excerpt="لا يوجد دليل شرعي على أن اللغات توقيفية من الله",
            argument=(
                "لا طريقَ إلى الوضع بالوحي: الوحيُ خطابٌ لا يُفهَم إلا بلغةٍ "
                "سابقةٍ عليه، فجعلُه طريقَ العلم بأصل اللغة دورٌ محال. ولا "
                "دليلَ شرعيًّا يُثبِت التوقيف أصلاً بنصّ المصدر."
            ),
        ),
        RefutationGround(
            ground=TawqifRefutationGround.لا_طريق_بعلم_ضروري,
            excerpt="الواقع المشاهد أنها اصطلاح من الناس",
            argument=(
                "ولا طريقَ إليه بعلمٍ ضروريّ: العلمُ الضروريُّ بأن اللغة من "
                "الله يستلزم معرفةَ الله بالضرورة عند كل واضعٍ ومتكلّم، وهو "
                "خلافُ الواقع المشاهَد الذي يشهد باصطلاح الناس."
            ),
        ),
    ),
)

ADAM_TEACHING_EVIDENCE: Final[str] = (
    "فإن المراد منه مسمّيات الأشياء لا اللغات، أي علّمه حقائق الأشياء وخواصها"
)

RECORDED_ADAM_TEACHING_READING: Final[AdamTeachingRecord] = AdamTeachingRecord(
    reading=AdamTeachingReading.حقائق_الأشياء_وخواصها,
    excerpt=ADAM_TEACHING_EVIDENCE,
)


def _assert_no_fields_matching(
    markers: tuple[str, ...],
    declaring_types: tuple[type, ...],
) -> None:
    for declaring_type in declaring_types:
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name.lower():
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(WadOrigin) != 2:  # pragma: no cover - guard
    raise RuntimeError("الواضعُ ثنائيٌّ مغلقٌ لا ثالثَ له.")
if len(TawqifRefutationGround) != 2:  # pragma: no cover - guard
    raise RuntimeError("برهانُ نفي التوقيف شِقّان لا واحد.")
if len(AdamTeachingReading) != 2:  # pragma: no cover - guard
    raise RuntimeError("قراءتا الآية اثنتان، والمرفوضةُ منهما مُسمّاةٌ لا مطويّة.")
if len(WadDerivationRefusal) != 2:  # pragma: no cover - guard
    raise RuntimeError("الطريقان المرفوضان اثنان: من الدالِّ وحده ومن المدلولِ وحده.")
if len(StatisticalFunction) != 2:  # pragma: no cover - guard
    raise RuntimeError("وظيفةُ الإحصاء ثنائيةٌ مغلقة، والممتنعُ منها عضوٌ مُسمًّى.")
if set(REFUSED_DERIVATION_NOTES) != set(WadDerivationRefusal):  # pragma: no cover
    raise RuntimeError("كلُّ طريقٍ مرفوضٍ يحمل سببَ رفضه بالاسم.")
if RECORDED_TAWQIF_REFUTATION.origin is not WadOrigin.وضع_بشري:  # pragma: no cover
    raise RuntimeError("الواضعُ المُشتَقّ من البرهان المُسجَّل بشريّ.")
_assert_no_fields_matching(
    _FORBIDDEN_FIELD_MARKERS,
    (
        RefutationGround,
        TawqifRefutation,
        AdamTeachingRecord,
        WadRecord,
        DistributionalCorroboration,
    ),
)
_assert_no_fields_matching(_WAD_RECORD_FORBIDDEN_MARKERS, (WadRecord,))
