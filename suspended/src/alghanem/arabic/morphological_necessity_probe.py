"""تجميدُ فحصٍ قبل إجرائه: أزواجُ التمييز، ومخروطُ المجالات الأضعف.

**السؤالُ الذي وقفت عنده البطاقة**: بندُ «الاشتقاق والصرف» في
`sentence_card_preregistration` واقفٌ **لا لنقص نقل** — فنصُّه مُزوَّدٌ مُسنَدٌ
ومعه مُعاضِد — بل لأنّه «لا يقوم مقامَ **مجالٍ صوريٍّ** للجذر والمصدر لا يزال
غيرَ مُرمَّز». فزيادةُ شاهدٍ رابعٍ عليه تُراكم نقلًا حيث الحاجزُ صوريّ. والسؤالُ
المستقيمُ إذن: **أيعجز كلُّ مجالٍ صوريٍّ قائمٍ في هذه الشجرة عن تمييز أزواجٍ
يلزم تمييزُها؟**

**وهذه الوحدة تُجمِّد الفحصَ ولا تُجريه** (`FreezeBeforeMeasurement`، على منوال
`probe_preregistration`): لا مفردةَ مُخرَجاتٍ فيها، ولا دالّةَ اشتقاق، ولا نتيجة.
فاختبارٌ يُصاغ هدفُه بعد رؤية أوّل نتيجةٍ اختبارٌ بُني لينجح، ومن جمّد بأثرٍ
رجعيّ برّر ولم يفحص.

**وهدفُ التمييز منقولٌ من موضعٍ سابقٍ للسؤال** (`TargetPredatesTheQuestion`):
الأزواجُ الثلاثة مأخوذةٌ بحروفها من `docs/reference/arabic_identity_confusion_catalog.md`
§٣.١، وهي مُسجَّلةٌ هناك **قبل أن يُطرَح سؤالُ الضرورة هذا**، ويُحيل إليها رفضٌ
قائمٌ في البطاقة نفسها (`WaznIsNotDerivedFromSurfaceSkeleton`). ولو صِيغت الأزواجُ
الآن لأجل الدعوى لكانت شاهدًا مصنوعًا لها.

**والتصادمُ مقيسٌ لا مُدَّعًى** (`CollisionIsRederivedNotAsserted`): كلُّ زوجٍ
يُعاد اشتقاقُ تصادمه من `comparison_key` المستعمَل في هذه الشجرة نفسها —
استيرادًا لا نسخًا — فمن أعلن زوجًا لا يتصادم طرفاه تحت مفتاح المقارنة أعلن
هدفَ تمييزٍ لا يحتاج مجالًا أصلًا، ويُرَدّ عند الإنشاء.

**ومخروطُ المجالات يُقرأ من الشجرة لا يُكتَب** (`ConeIsReadNotChosen`، على منوال
`pipeline_stations` و`BirthExperimentSpecification.frozen_weaker_models`): المجالاتُ
الصوريةُ المُجمَّدةُ الأربعةُ القائمة تُستورَد بأعيانها ويُفحَص وجودُ ملفّاتها في
الشجرة. فمخروطٌ مكتوبٌ بالاسم يُنتقى أعضاؤه بعد رؤية النتيجة، وانتقاءُ النموذج
الأضعف بعد الجواب هو عينُ ما يصنع «ضرورةً» كاذبة.

**والتوقّعُ يُكتَب قبل القياس** (`PreRegisteredExpectation`): المُتوقَّعُ أن
يخرج الفحصُ **`غير_محسوم_لتعذّر_القياس`** — لأنّ المجالات الأربعة تستقبل شواهدَ
مُصنَّفةً بإجاباتٍ مُعلَنةٍ وأدلّةٍ منصوصة، لا أشكالًا سطحية؛ فتطبيقُها على زوجٍ
سطحيٍّ يستلزم خطوةَ تصنيفٍ غيرَ موجودةٍ في الشجرة. وتجميدُ التوقّع قبل رؤية
النتيجة يجعل مطابقتَه تأكيدًا ومخالفتَه مفاجأةً تُوثَّق، لا يجعل أحدَهما قابلًا
للصياغة بعد وقوعه.

**وليس في هذه الوحدة حكمُ ضرورة** (`MeasuredNegativeIsNotAConstitutionalNecessity`):
الدستورُ يُثبت ضرورةَ الإحداثيّات بتصادم الإسقاط **نسبةً إلى هدف تمييزٍ مُعلَن**
ويُصرّح أنّها ليست ضرورةً دلالية؛ وبوّابةُ استنفاد النماذج الأضعف في `kernel/`
لا تقرؤها هذه الطبقةُ ولا تُصدر أحكامَها. فغايةُ ما يبلغه هذا الفحصُ **سالبةٌ
مقيسة**، واستنتاجُ فتحِ مجالٍ جديدٍ منها قرارٌ يُكتَب في موضع القرارات لا مُخرَجٌ
تلقائيٌّ من أداة.

**وهذه الوحدة تسجيلٌ لا سلطة**: لا ولادة، ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا
تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .kulli_juzi_formal import FROZEN_KULLI_JUZI_DOMAIN
from .lafz_madlul_relation_formal import FROZEN_RELATION_DOMAIN
from .madlul_alone_formal import FROZEN_MADLUL_DOMAIN
from .pipeline_stations import ARABIC_PACKAGE_RELATIVE_PATH, repository_root_path
from .text_key import comparison_key
from .word_class_formal import FROZEN_FORMAL_DOMAIN

__all__ = [
    "COLLISION_IS_REDERIVED_NOT_ASSERTED_NOTE",
    "CONE_IS_READ_NOT_CHOSEN_NOTE",
    "DISCRIMINATION_TARGET_DIGEST",
    "FREEZE_BEFORE_MEASUREMENT_NOTE",
    "FROZEN_DISCRIMINATION_TARGET",
    "MEASURED_NEGATIVE_IS_NOT_A_NECESSITY_NOTE",
    "NAMED_RESIDUALS",
    "PRE_REGISTERED_EXPECTATION",
    "PROBE_IS_NOT_A_GATE_NOTE",
    "TARGET_PREDATES_THE_QUESTION_NOTE",
    "DiscriminationPair",
    "MorphologicalNecessityProbeError",
    "WeakerDomainReference",
    "discrimination_target_digest",
    "read_weaker_domain_cone",
]


class MorphologicalNecessityProbeError(ValueError):
    """رفضٌ صريحٌ في تجميد الفحص؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


CATALOG_RELATIVE_PATH: Final[str] = (
    "docs/reference/arabic_identity_confusion_catalog.md"
)

CATALOG_SECTION: Final[str] = "§٣.١ — تصادم المتجانسات تحت التجريد إلى الهيكل الصامت"


FREEZE_BEFORE_MEASUREMENT_NOTE: Final[str] = (
    "FreezeBeforeMeasurement: يُجمَّد هدفُ التمييز ومخروطُ المجالات **قبل** أوّل "
    "قياس، ولا تُكتَب في هذه الوحدة مفردةُ مُخرَجاتٍ ولا دالّةُ اشتقاق. فهدفٌ "
    "يُصاغ بعد رؤية النتيجة اختبارٌ بُني لينجح، وتجميدٌ بأثرٍ رجعيّ تبريرٌ لا فحص"
)

TARGET_PREDATES_THE_QUESTION_NOTE: Final[str] = (
    "TargetPredatesTheQuestion: الأزواجُ الثلاثة منقولةٌ بحروفها من فهرس التباس "
    "الهويّة §٣.١، وهي مُسجَّلةٌ هناك قبل أن يُطرَح سؤالُ ضرورة المجال الصرفيّ، "
    "ويُحيل إليها رفضُ `WaznIsNotDerivedFromSurfaceSkeleton` القائم في بطاقة "
    "الجملة. وزوجٌ يُصاغ الآن لأجل الدعوى شاهدٌ مصنوعٌ لها لا شاهدٌ عليها"
)

COLLISION_IS_REDERIVED_NOT_ASSERTED_NOTE: Final[str] = (
    "CollisionIsRederivedNotAsserted: تصادمُ الطرفين يُعاد اشتقاقُه من "
    "`comparison_key` المستعمَل في هذه الشجرة نفسها — استيرادًا لا نسخًا — ولا "
    "يُصدَّق مُعلَنًا في حقل. وزوجٌ لا يتصادم طرفاه تحته ليس هدفَ تمييزٍ يحتاج "
    "مجالًا، فيُرَدّ عند الإنشاء"
)

CONE_IS_READ_NOT_CHOSEN_NOTE: Final[str] = (
    "ConeIsReadNotChosen: مخروطُ المجالات الأضعف يُقرأ من الشجرة — تُستورَد "
    "المجالاتُ المُجمَّدةُ بأعيانها ويُفحَص وجودُ ملفّاتها — لا يُكتَب بالاسم. "
    "فمخروطٌ مكتوبٌ يُنتقى أعضاؤه بعد رؤية النتيجة، وانتقاءُ النموذج الأضعف بعد "
    "الجواب هو عينُ ما يصنع ضرورةً كاذبة"
)

MEASURED_NEGATIVE_IS_NOT_A_NECESSITY_NOTE: Final[str] = (
    "MeasuredNegativeIsNotAConstitutionalNecessity: غايةُ ما يبلغه هذا الفحصُ "
    "سالبةٌ مقيسةٌ عن مجالاتٍ بعينها في شجرةٍ بعينها. والضرورةُ في الدستور "
    "تُثبَت بتصادم الإسقاط نسبةً إلى هدف تمييزٍ مُعلَن ومع التصريح بأنّها ليست "
    "ضرورةً دلالية، واستنفادُ النماذج الأضعف بوّابةٌ في `kernel/` لا تقرؤها هذه "
    "الطبقة؛ فاستنتاجُ فتحِ مجالٍ جديدٍ قرارٌ يُكتَب لا مُخرَجٌ تلقائيّ"
)

PROBE_IS_NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا تُصدر هذه الوحدة ولادةً ولا حكمَ ولادة ولا تجميدًا ولا "
    "`E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه"
)

PRE_REGISTERED_EXPECTATION: Final[str] = (
    "PreRegisteredExpectation: **المُتوقَّع قبل القياس** أن يخرج الفحصُ "
    "`غير_محسوم_لتعذّر_القياس` لا سالبةً تامّة، لأنّ المجالات الأربعة تستقبل "
    "شواهدَ مُصنَّفةً بإجاباتٍ مُعلَنةٍ وأدلّةٍ منصوصة لا أشكالًا سطحية؛ فتطبيقُها "
    "على زوجٍ سطحيٍّ يستلزم خطوةَ تصنيفٍ غيرَ موجودةٍ في الشجرة. وهذا التوقّعُ "
    "مُجمَّدٌ في كوميت التجميد قبل كتابة أيّ دالّة قياس، فمطابقتُه تأكيدٌ "
    "ومخالفتُه مفاجأةٌ تُوثَّق بتفصيل تطبيق كلّ مجالٍ على كلّ زوج"
)


NAMED_RESIDUALS: Final[dict[str, str]] = {
    "FREEZE_BEFORE_MEASUREMENT": FREEZE_BEFORE_MEASUREMENT_NOTE,
    "TARGET_PREDATES_THE_QUESTION": TARGET_PREDATES_THE_QUESTION_NOTE,
    "COLLISION_IS_REDERIVED_NOT_ASSERTED": COLLISION_IS_REDERIVED_NOT_ASSERTED_NOTE,
    "CONE_IS_READ_NOT_CHOSEN": CONE_IS_READ_NOT_CHOSEN_NOTE,
    "MEASURED_NEGATIVE_IS_NOT_A_CONSTITUTIONAL_NECESSITY": (
        MEASURED_NEGATIVE_IS_NOT_A_NECESSITY_NOTE
    ),
    "THREE_PAIRS_ARE_NOT_THE_LANGUAGE": (
        "الأزواجُ الثلاثة هي ما رُصِد في الفهرس، وليست تعدادًا لأزواج العربية "
        "المتصادمة؛ فسالبةٌ تامّةٌ عليها سالبةٌ عليها وحدها، على منوال "
        "`ExhaustedSourceIsNotAnExhaustedWorld`. **وأيُّ مدخلٍ يوسّعها؟** زوجٌ "
        "يُرصَد في موضعٍ سابقٍ لسؤاله، لا زوجٌ يُصاغ لأجل نتيجةٍ مرجوّة"
    ),
    "COMPARISON_KEY_IS_A_TOOL_LIMIT_NOT_A_LANGUAGE_FACT": (
        "تصادمُ الطرفين واقعٌ تحت `comparison_key` بحدوده المُعلَنة — إسقاطُ "
        "العلامات وطيُّ الألفات والتاء المربوطة — وهو قيدُ أداةٍ في هذه الشجرة "
        "لا دعوى أنّ العربية لا تفرّق بينهما؛ ومن قرأه حقيقةً في اللغة قرأ حدَّ "
        "الأداة نصًّا في العالم"
    ),
    "CATALOG_IS_TESTIMONY_NOT_MEASUREMENT": (
        "الفهرسُ المنقولةُ منه الأزواجُ شهادةُ أعطابٍ من دورةٍ مستقلّة، مُصرَّحٌ "
        "في متنه بأنّه `DEFER` وبأنّه بلا مواصفةِ قياسٍ ولا هويّةِ جولةٍ ولا "
        "سكربتِ إعادة اشتقاق (`Testimony != Measurement`). فالمنقولُ منه **أزواجٌ "
        "تُفحَص**، لا أرقامٌ يُحتَجّ بها ولا تصنيفٌ يُصدَّق"
    ),
    "NO_DOMAIN_IS_APPLIED_IN_THIS_MODULE": (
        "لا يُطبَّق في وحدة التجميد هذه مجالٌ على زوج، ولا تُشتَقّ نتيجة، ولا "
        "مفردةَ مُخرَجاتٍ فيها أصلًا؛ فالتجميدُ يسبق القياسَ في الترتيب لا في "
        "الوصف وحده"
    ),
}


@dataclass(frozen=True, slots=True)
class DiscriminationPair:
    """زوجٌ يلزم تمييزُه: طرفاه، وموضعُ رصده، ونصُّ رصده المنقول."""

    surface_a: str
    surface_b: str
    catalog_locus: str
    catalog_excerpt: str

    def __post_init__(self) -> None:
        for name in ("surface_a", "surface_b", "catalog_locus", "catalog_excerpt"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise MorphologicalNecessityProbeError(
                    f"{name} نصٌّ غير فارغ؛ ولا يُترَك صمتًا."
                )
        if self.surface_a == self.surface_b:
            raise MorphologicalNecessityProbeError(
                "طرفا الزوج لفظان متمايزان في الرسم؛ ولفظٌ مع نفسه ليس هدفَ تمييز."
            )
        for surface in (self.surface_a, self.surface_b):
            if surface not in self.catalog_excerpt:
                raise MorphologicalNecessityProbeError(
                    f"الطرفُ «{surface}» غيرُ واقعٍ في النصّ المرصود بحروفه؛ "
                    "وزوجٌ لا يُقرأ طرفاه في موضع رصده مُصاغٌ الآن لا منقول."
                )
        if comparison_key(self.surface_a) != comparison_key(self.surface_b):
            raise MorphologicalNecessityProbeError(
                f"«{self.surface_a}» و«{self.surface_b}» لا يتصادمان تحت مفتاح "
                "المقارنة المستعمَل في هذه الشجرة؛ وزوجٌ لا يتصادم طرفاه لا "
                "يحتاج مجالًا يُميِّزه أصلًا. " + COLLISION_IS_REDERIVED_NOT_ASSERTED_NOTE
            )

    @property
    def collided_key(self) -> str:
        """الهيكلُ الواحدُ الذي انطبق عليه الطرفان، مُعادَ الاشتقاق لا مكتوبًا."""

        return comparison_key(self.surface_a)

    def encoded(self) -> dict[str, str]:
        """الصورةُ المُعمَّاة للزوج، وهي وحدُها ما تُبصَم عليه البصمةُ المُجمَّدة."""

        return {
            "surface_a": self.surface_a,
            "surface_b": self.surface_b,
            "catalog_locus": self.catalog_locus,
            "catalog_excerpt": self.catalog_excerpt,
        }


_CATALOG_EXCERPT_HOMOGRAPHS: Final[str] = (
    "إسقاط الحركات للحصول على هيكلٍ صامتٍ مجرَّد — وهي خطوةٌ طبيعية أولى نحو أيّ "
    "تحليلٍ على شاكلة `SurfaceAtomCandidate` — يُطبق بانتظامٍ هويّتين معجميّتين "
    "مختلفتين على هيكلٍ واحد. الأمثلة المتكرّرة: مِن (حرف جرّ) / مَن (اسم "
    "استفهام أو موصول)؛ أَمْ (حرف عطف) / أُمّ (اسم)؛ هَمَّ (فعل) / هُمْ (ضمير) "
    "بوصفه مُلوِّثًا نادرًا."
)


FROZEN_DISCRIMINATION_TARGET: Final[tuple[DiscriminationPair, ...]] = (
    DiscriminationPair(
        surface_a="مِن",
        surface_b="مَن",
        catalog_locus=f"{CATALOG_RELATIVE_PATH} {CATALOG_SECTION}",
        catalog_excerpt=_CATALOG_EXCERPT_HOMOGRAPHS,
    ),
    DiscriminationPair(
        surface_a="أَمْ",
        surface_b="أُمّ",
        catalog_locus=f"{CATALOG_RELATIVE_PATH} {CATALOG_SECTION}",
        catalog_excerpt=_CATALOG_EXCERPT_HOMOGRAPHS,
    ),
    DiscriminationPair(
        surface_a="هَمَّ",
        surface_b="هُمْ",
        catalog_locus=f"{CATALOG_RELATIVE_PATH} {CATALOG_SECTION}",
        catalog_excerpt=_CATALOG_EXCERPT_HOMOGRAPHS,
    ),
)


def discrimination_target_digest(
    target: tuple[DiscriminationPair, ...] | None = None,
) -> str:
    """بصمةُ هدف التمييز، مُعادةَ الاشتقاق من الأزواج نفسها لا مُعلَنةً في حقل."""

    pairs = FROZEN_DISCRIMINATION_TARGET if target is None else target
    if not isinstance(pairs, tuple):
        raise MorphologicalNecessityProbeError("هدفُ التمييز تعدادٌ مُجمَّد.")
    for pair in pairs:
        if not isinstance(pair, DiscriminationPair):
            raise MorphologicalNecessityProbeError("كلُّ عنصرٍ زوجُ تمييزٍ مُصاغ.")
    return canonical_digest(canonical_bytes([pair.encoded() for pair in pairs]))


DISCRIMINATION_TARGET_DIGEST: Final[str] = (
    "a004e6719ca786e87d57459e8dce03a57e46fed13b675851a8f0f46d820bc21f"
)


@dataclass(frozen=True, slots=True)
class WeakerDomainReference:
    """مجالٌ صوريٌّ مُجمَّدٌ قائمٌ في الشجرة: وحدتُه، وعينُه، وعددُ حالاته."""

    module_relative_path: str
    domain: object

    def __post_init__(self) -> None:
        if not isinstance(self.module_relative_path, str) or not (
            self.module_relative_path.strip()
        ):
            raise MorphologicalNecessityProbeError("مسارُ الوحدة نصٌّ غير فارغ.")
        if self.domain is None:
            raise MorphologicalNecessityProbeError(
                "المجالُ عينٌ مستورَدةٌ من وحدته لا اسمٌ مكتوب."
            )

    @property
    def module_path(self) -> Path:
        """موضعُ الوحدة في الشجرة، مُشتقًّا من جذر المستودع لا مكتوبًا مطلقًا."""

        return repository_root_path() / self.module_relative_path

    @property
    def is_present_in_tree(self) -> bool:
        """أموجودةٌ وحدةُ المجال في الشجرة؟ تُقرأ عند النداء ولا تُصدَّق مُعلَنة."""

        return self.module_path.is_file()


_CONE_MEMBERS: Final[tuple[tuple[str, object], ...]] = (
    ("word_class_formal.py", FROZEN_FORMAL_DOMAIN),
    ("kulli_juzi_formal.py", FROZEN_KULLI_JUZI_DOMAIN),
    ("lafz_madlul_relation_formal.py", FROZEN_RELATION_DOMAIN),
    ("madlul_alone_formal.py", FROZEN_MADLUL_DOMAIN),
)


def read_weaker_domain_cone() -> tuple[WeakerDomainReference, ...]:
    """اقرأ مخروطَ المجالات الأضعف من الشجرة؛ وغيابُ وحدةٍ يُرَدّ ولا يُتخطّى."""

    references: list[WeakerDomainReference] = []
    for file_name, domain in _CONE_MEMBERS:
        reference = WeakerDomainReference(
            module_relative_path=f"{ARABIC_PACKAGE_RELATIVE_PATH}/{file_name}",
            domain=domain,
        )
        if not reference.is_present_in_tree:
            raise MorphologicalNecessityProbeError(
                f"وحدةُ المجال غائبةٌ عن الشجرة: {reference.module_relative_path}؛ "
                "ومخروطٌ ينقص عضوًا صامتًا مخروطٌ مُنتقًى. " + CONE_IS_READ_NOT_CHOSEN_NOTE
            )
        references.append(reference)
    return tuple(references)


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "result",
    "standing",
    "verdict",
    "necessity",
    "answer",
    "birth",
    "freeze",
)


def _assert_no_outcome_field() -> None:
    """احرسْ خلوَّ وحدة التجميد من حقلِ مُخرَجٍ أو نتيجة؛ فالقياسُ لم يقع بعد."""

    for declaring_type in (DiscriminationPair, WeakerDomainReference):
        for field in fields(declaring_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise RuntimeError(
                        f"{declaring_type.__name__}.{field.name} حقلٌ ممنوع: "
                        "هذه وحدةُ تجميدٍ قبل القياس ولا مُخرَج فيها."
                    )


def _assert_target_is_frozen() -> None:
    """احرسْ هدفَ التمييز ببصمةٍ مُعادةِ الاشتقاق؛ فزوجٌ يُزاد بعدها يُرَدّ."""

    if len(FROZEN_DISCRIMINATION_TARGET) != 3:  # pragma: no cover - guard
        raise RuntimeError("هدفُ التمييز ثلاثةُ أزواجٍ مرصودةٍ في الفهرس لا غير")
    recomputed = discrimination_target_digest()
    if recomputed != DISCRIMINATION_TARGET_DIGEST:
        raise RuntimeError(
            "هدفُ التمييز تغيّر بعد تجميده: البصمةُ المُعادُ اشتقاقُها "
            f"{recomputed} تخالف المُجمَّدة {DISCRIMINATION_TARGET_DIGEST}. "
            + FREEZE_BEFORE_MEASUREMENT_NOTE
        )


_assert_no_outcome_field()
_assert_target_is_frozen()
