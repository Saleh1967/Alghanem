"""دستورُ `G0.FGEN-EX-0`: قوانينُ التجريب الفراكتاليِّ مُجمَّدةً قبل أوّل تشغيل.

القانونُ الأعلى في هذه الطبقة:

    ExperimentBeforeLicense

فالتجريبُ سابقٌ للترخيص، والسلطةُ التي تفتح التشغيل ليست السلطةَ التي تُرخِّص:

    TemporaryExperimentalAuthority  ≠  LicensingAuthority

**والنصوصُ هنا محتوًى مُبصَّم** (`FRACTAL_EXPERIMENT_LAW_SET_DIGEST`): تعديلُ
نصِّ قانونٍ يُغيِّر البصمةَ فيسقط اختبارُها. **والمجموعةُ مستقلّةٌ** عن مجموعة
`fractal_generation/`: بصمتُها لا تُقرَأ هنا ولا تُمَسّ.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN",
    "EXPERIMENTAL_LIFT_TESTS_NECESSITY_IT_DOES_NOT_CERTIFY_NECESSITY",
    "EXPERIMENTAL_NEXT_SCALE_SEED_IS_NOT_NEXT_SCALE_SEED",
    "EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE",
    "EXPERIMENTAL_SUCCESS_IS_A_WITNESS_NOT_A_LICENSE",
    "EXPERIMENTAL_TRANSITION_IS_NOT_LICENSED_TRANSITION",
    "EXPERIMENT_BEFORE_LICENSE",
    "FRACTAL_EXPERIMENT_LAWS",
    "FRACTAL_EXPERIMENT_LAW_SET_DIGEST",
    "FRACTAL_EXPERIMENT_LAW_SET_ID",
    "FROZEN_EXPECTATION_IS_NOT_GENERATIVE_INPUT",
    "FROZEN_INPUT_IS_NOT_PROVEN_STRUCTURE",
    "SUFFICIENCY_CRITERION_MUST_PRECEDE_ITS_MEASUREMENT",
    "SUFFICIENT_WITNESSES_OPEN_LICENSING_CANDIDATE_NOT_LICENSE",
    "TEMPORARY_EXPERIMENTAL_AUTHORITY_IS_NOT_LICENSING_AUTHORITY",
    "WITNESS_ACCUMULATION_PRECEDES_LICENSING",
    "WITNESS_IS_NOT_JUDGMENT",
]


FRACTAL_EXPERIMENT_LAW_SET_ID: Final[str] = (
    "alghanem.fractal_experiment.laws.G0.FGEN-EX-0"
)

EXPERIMENT_BEFORE_LICENSE: Final[str] = (
    "التجريبُ قبل الترخيص: `ExperimentBeforeLicense`؛ فلا يُسأل «أعندنا ترخيصٌ "
    "كي نجرّب؟» بل «أعندنا تجميدٌ وسلطةُ تشغيلٍ مؤقّتة؟»، والترخيصُ سؤالٌ لاحقٌ "
    "لا شرطٌ سابق"
)

TEMPORARY_EXPERIMENTAL_AUTHORITY_IS_NOT_LICENSING_AUTHORITY: Final[str] = (
    "سلطةُ التجريب المؤقّتةُ ليست سلطةَ الترخيص: `TemporaryExperimentalAuthority "
    "≠ LicensingAuthority`؛ فالأولى تفتح تشغيلًا مقيَّدًا بمداه، والثانيةُ "
    "تُرتِّب رتبةً دائمة، ولا تُستمَدّ إحداهما من الأخرى"
)

EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE: Final[str] = (
    "الإذنُ التجريبيُّ ليس ترخيصًا: `ExperimentalPermission ≠ License`؛ فالإذنُ "
    "يقول «جرِّب هذا في هذا التشغيل»، ولا يقول «هذا صحيحٌ» ولا «هذا مأذونٌ فيه»"
)

EXPERIMENTAL_TRANSITION_IS_NOT_LICENSED_TRANSITION: Final[str] = (
    "الانتقالُ التجريبيُّ ليس انتقالًا مرخَّصًا: `ExperimentalTransition ≠ "
    "LicensedTransition`؛ فهو واقعةُ تشغيلٍ مُسجَّلةٌ بأثرها، لا رتبةٌ تُبنى عليها"
)

EXPERIMENTAL_NEXT_SCALE_SEED_IS_NOT_NEXT_SCALE_SEED: Final[str] = (
    "بذرةُ المقياس التجريبيّةُ ليست بذرةَ المقياس الدائمة: "
    "`ExperimentalNextScaleSeed ≠ NextScaleSeed`؛ فالأولى ينتهي أثرُ سلطتها "
    "بانتهاء التشغيل، ولا تدخل مكانَ الثانية ولا تُحوَّل إليها"
)

EXPERIMENTAL_SUCCESS_IS_A_WITNESS_NOT_A_LICENSE: Final[str] = (
    "نجاحُ التجربة شاهدٌ لا ترخيص: `ExperimentalPASS → Witness` لا "
    "`ExperimentalPASS → License`؛ والفشلُ شاهدٌ كذلك، وضعفُ القوّة شاهدٌ كذلك"
)

WITNESS_ACCUMULATION_PRECEDES_LICENSING: Final[str] = (
    "تراكمُ الشواهد سابقٌ للترخيص: `WitnessAccumulationPrecedesLicensing`؛ "
    "فالتجميعُ يسبق القياسَ على معيار الكفاية، والقياسُ يسبق الإحالةَ إلى سلطة "
    "الترخيص"
)

SUFFICIENT_WITNESSES_OPEN_LICENSING_CANDIDATE_NOT_LICENSE: Final[str] = (
    "الشواهدُ الكافيةُ تفتح مرشَّحَ ترخيصٍ لا ترخيصًا: `ΣWitnesses ⇏ License`؛ "
    "وأكثرُ ما تبلغه هو `LicensingCandidate` بعد معيارِ كفايةٍ مُجمَّدٍ مستقلّ"
)

EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN: Final[str] = (
    "سلطةُ التجريب تنتهي بانتهاء تشغيلها: `RunFinished → PermitRevoked`؛ "
    "والصلاحيةُ مرتبطةٌ بالحالة التشغيليّة وهويّة التشغيل لا بساعةٍ ولا بمدّةٍ "
    "زمنيّة، ولا استعمالَ بعد الإلغاء"
)

FROZEN_INPUT_IS_NOT_PROVEN_STRUCTURE: Final[str] = (
    "المدخلُ المُجمَّدُ ليس بنيةً مُثبَتة: `FrozenInput ≠ ProvenStructure`؛ "
    "فالتجميدُ يمنع تغييرَ المدخل بعد رؤية النتيجة، ولا يجعل المدخلَ صادقًا"
)

FROZEN_EXPECTATION_IS_NOT_GENERATIVE_INPUT: Final[str] = (
    "التوقّعُ المُجمَّدُ ليس مدخلًا توليديًّا: `FrozenExpectation ≠ "
    "GenerativeInput`؛ فالنتيجةُ المتنبَّأُ بها وما يُكذِّبها يدخلان في القراءة "
    "بعد التشغيل، ولا يدخلان مُولِّدَ التحوّل فيُلقِّنه جوابَه"
)

WITNESS_IS_NOT_JUDGMENT: Final[str] = (
    "الشاهدُ ليس حكمًا: `Witness ≠ Judgment`؛ فالشاهدُ رصدٌ مُسجَّلٌ بأثره "
    "وبقاياه، والحكمُ رتبةٌ تصدر عن سلطةٍ أخرى لم تُفتَح هنا"
)

EXPERIMENTAL_LIFT_TESTS_NECESSITY_IT_DOES_NOT_CERTIFY_NECESSITY: Final[str] = (
    "الرفعُ التجريبيُّ يختبر الضرورةَ ولا يشهد بها: "
    "`ExperimentalLiftTestsNecessity; ItDoesNotCertifyNecessity`؛ فإثباتُ "
    "الضرورة هو موضوعُ التجربة لا شرطُ دخولها، و`ScaleNecessityCertificate` "
    "تبقى مغلقةً كما هي"
)

SUFFICIENCY_CRITERION_MUST_PRECEDE_ITS_MEASUREMENT: Final[str] = (
    "معيارُ الكفاية يسبق قياسَه: "
    "`SufficiencyCriterionMustPrecedeItsMeasurement`؛ فالعقدُ يُجمَّد قبل أن "
    "تُعَدَّ الشواهد، ولا يُصاغ بعد رؤيتها فيوافقها"
)

FRACTAL_EXPERIMENT_LAWS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "ExperimentBeforeLicense": EXPERIMENT_BEFORE_LICENSE,
        "TemporaryExperimentalAuthorityIsNotLicensingAuthority": (
            TEMPORARY_EXPERIMENTAL_AUTHORITY_IS_NOT_LICENSING_AUTHORITY
        ),
        "ExperimentalPermissionIsNotLicense": EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE,
        "ExperimentalTransitionIsNotLicensedTransition": (
            EXPERIMENTAL_TRANSITION_IS_NOT_LICENSED_TRANSITION
        ),
        "ExperimentalNextScaleSeedIsNotNextScaleSeed": (
            EXPERIMENTAL_NEXT_SCALE_SEED_IS_NOT_NEXT_SCALE_SEED
        ),
        "ExperimentalSuccessIsAWitnessNotALicense": (
            EXPERIMENTAL_SUCCESS_IS_A_WITNESS_NOT_A_LICENSE
        ),
        "WitnessAccumulationPrecedesLicensing": (
            WITNESS_ACCUMULATION_PRECEDES_LICENSING
        ),
        "SufficientWitnessesOpenLicensingCandidateNotLicense": (
            SUFFICIENT_WITNESSES_OPEN_LICENSING_CANDIDATE_NOT_LICENSE
        ),
        "ExperimentalAuthorityExpiresWithItsRun": (
            EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN
        ),
        "FrozenInputIsNotProvenStructure": FROZEN_INPUT_IS_NOT_PROVEN_STRUCTURE,
        "FrozenExpectationIsNotGenerativeInput": (
            FROZEN_EXPECTATION_IS_NOT_GENERATIVE_INPUT
        ),
        "WitnessIsNotJudgment": WITNESS_IS_NOT_JUDGMENT,
        "ExperimentalLiftTestsNecessityItDoesNotCertifyNecessity": (
            EXPERIMENTAL_LIFT_TESTS_NECESSITY_IT_DOES_NOT_CERTIFY_NECESSITY
        ),
        "SufficiencyCriterionMustPrecedeItsMeasurement": (
            SUFFICIENCY_CRITERION_MUST_PRECEDE_ITS_MEASUREMENT
        ),
    }
)

FRACTAL_EXPERIMENT_LAW_SET_DIGEST: Final[str] = canonical_digest(
    canonical_bytes(
        {
            "law_set_id": FRACTAL_EXPERIMENT_LAW_SET_ID,
            "laws": dict(FRACTAL_EXPERIMENT_LAWS),
        }
    )
)
