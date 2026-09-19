"""سَوقُ المسار العربيّ داخل السلطة التجريبية القائمة، بطلبٍ مربوطٍ بتجربةٍ مجمّدة.

لا سلطةَ جديدةَ هنا ولا بوّابة: `ExperimentalAuthority` هي المُشغِّلة،
و`ExperimentalRunBindingAuthority` هي الرابطة، وهذه الوحدة تُهيّئ الطلبَ وتقرأ
السجلَّ الصادر. و`NoBornEntityIsRequiredToRunAnExperiment` هو ما يُجيز التشغيلَ
بلا شهادةِ ولادة، و`ExperimentalSuccessIsNotBirth` هو ما يمنع قراءةَ نجاحه
شهادةً.

**طريقُ التقديم محفوظٌ لا مسلوك**: نتيجةُ هذا السَّوق يجوز أن تُقدَّم لاحقًا عبر
`experimental_evidence_gate` إلى سلسلة اكتساب الأدلّة، ولا تُرقّى تلقائيًّا؛
فالترقيةُ تقييمٌ مرخَّصٌ جديد لا أثرٌ جانبيٌّ لتشغيل.

**المقامُ الإحصائيّ لا يُنقَّى**: الواقفُ والمؤجَّلُ والممنوع يُعَدّون في محلّهم،
ولا يُحذَف أحدُهم من المقام ليرتفع ما بلغ الإفادة (`A_STOP_STAYS_IN_THE
_DENOMINATOR`).
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from alghanem.kernel.birth import (
    BirthExperimentSpecification,
    BirthQuery,
    EvidenceMode,
    ProjectionPoset,
    StructureHypothesis,
)
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)
from alghanem.kernel.experimental import (
    DeclaredCaseSet,
    ExperimentalAuthority,
    ExperimentalCandidateDeclaration,
    ExperimentalCaseOutcomeVocabulary,
    ExperimentalOperationRef,
    ExperimentalOutcomeStatus,
    ExperimentalRunContext,
    ExperimentalRunRecord,
    ExperimentalRunRequest,
)
from alghanem.kernel.experimental_run_binding import ExperimentalRunBindingAuthority
from alghanem.kernel.trace import Trace

from .composition_ifada_path import (
    DECLARED_SCOPE,
    CompositionReading,
    PathRun,
    PathStage,
    PathStop,
    StageOutcome,
    run_text,
)
from .mantuq_mafhum_ifada import IfadaStanding

__all__ = [
    "ACCOUNTED_TOKEN",
    "COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS",
    "DECLARED_INPUTS",
    "EXPERIMENT_DOMAIN",
    "UNACCOUNTED_TOKEN",
    "CompositionIfadaExperimentError",
    "PathCensus",
    "measure",
    "render_census",
    "run_under_the_experimental_authority",
]


class CompositionIfadaExperimentError(ValueError):
    """رفضٌ بنيويٌّ في تهيئة السَّوق التجريبيّ، لا في النصّ المقيس."""


EXPERIMENT_DOMAIN: Final[str] = "arabic-two-word-composition"

ACCOUNTED_TOKEN: Final[str] = "ACCOUNTED:بلغ النصُّ إفادةً مقروءة"
UNACCOUNTED_TOKEN: Final[str] = "UNACCOUNTED:وقف النصُّ دون إفادةٍ مقروءة"

DECLARED_INPUTS: Final[tuple[tuple[str, str], ...]] = (
    ("isnad-1", "اللَّهُ نُورٌ"),
    ("isnad-2", "مُحَمَّدٌ رَسُولٌ"),
    ("idafa-1", "نُورُ السَّمَاوَاتِ"),
    ("idafa-2", "نُورُ كِتَابٍ"),
    ("proclitic-1", "الْحَمْدُ لِلَّهِ"),
    ("unwritten-1", "قُلْ هُوَ"),
    ("tanwin-conflict-1", "كِتَابٌ الْبَيْتِ"),
    ("first-not-raf-1", "الْعَالَمِينَ نُورٌ"),
    ("second-nasb-1", "رَبُّ الْعَالَمِينَ"),
    ("not-two-words-1", "اللَّهُ"),
)
"""العيّنةُ المُعلَنةُ قبل التشغيل: موجبةٌ وسالبةٌ وملتبسة، وكلُّها في المقام.

وهي مُجمَّدةٌ قبل قراءة أيّ نتيجة، فلا تُوسَّع ولا تُضيَّق بعد رؤية ما بلغ
الإفادةَ منها.
"""

COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS: Final[dict[str, str]] = {
    "AStopStaysInTheDenominator": (
        "AStopStaysInTheDenominator: الواقفُ والمؤجَّلُ والممنوع يُعَدّون في "
        "المقام كلِّه، ولا يُحذَف أحدُهم ليرتفع ما بلغ الإفادة. وكلُّ توقّفٍ "
        "يُنسَب إلى طبقته وجنسه لا إلى «فشل»"
    ),
    "TheRunIsNotTheOffer": (
        "TheRunIsNotTheOffer: سَوقُ المسار داخل السلطة التجريبية يُنتج سجلَّ "
        "تشغيلٍ لا عرضَ دليل. وتقديمُ النتيجة إلى سلسلة اكتساب الأدلّة يمرّ "
        "بـ`experimental_evidence_gate` ثمّ `authorize → open_run → ingest`، "
        "ولا يقع بمجرّد اكتمال السَّوق"
    ),
    "WrittenRetrievalIsNotAnalysis": (
        "WrittenRetrievalIsNotAnalysis: نسبةُ الاسترجاع الكتابيّ تُقاس على "
        "الكلمات وحدَها، ونجاحُ التحليل يُقاس على النصوص، وبلوغُ الإفادة ثالثٌ "
        "غيرُهما. ولا يُقرأ أحدُ الثلاثة دليلًا على الآخر"
    ),
}
"""القيودُ المُسمّاةُ التي تُجمّدها هذه الوحدة؛ كلُّ نصٍّ يفتتح باسم قانونه."""


def _frozen_experiment() -> BirthExperimentSpecificationContentBinding:
    """جمِّد تجربةَ هذا النطاق قبل أيّ تشغيل، واربط محتواها ببصمتها."""

    specification = BirthExperimentSpecification(
        experiment_id="arabic-composition-ifada",
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.EMPIRICAL,
        domain=EXPERIMENT_DOMAIN,
        projection_poset=ProjectionPoset(
            ("written-marks", "composition-reading"),
            (("written-marks", "composition-reading"),),
        ),
        birth_query=BirthQuery(
            "أتُقرأ إفادةُ تركيبٍ من علامتَي إعرابه المكتوبتين وحدَهما؟",
            StructureHypothesis(
                "composition-reading",
                "قراءةُ التركيب لازمةٌ لقراءة الإفادة، ولا تكفي العلاماتُ وحدَها",
            ),
            "written-marks",
        ),
        residual_definition_id="unread-composition",
        residual_definition="تركيبٌ قائمٌ لم تُقرأ إفادتُه من علاماته المكتوبة",
        closure_criterion_id="marks-close",
        closure_criterion="العلاماتُ المكتوبةُ وحدَها تُغلق قراءةَ كلّ تركيبٍ في النطاق",
        evidence_requirements=DECLARED_SCOPE,
    )
    frozen = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(specification)
    )
    return BirthExperimentSpecificationContentBinding(specification, frozen)


def _request() -> ExperimentalRunRequest:
    return ExperimentalRunRequest(
        candidate=ExperimentalCandidateDeclaration(
            candidate_id="composition-ifada-path",
            declared_origin_ref="arabic_round_trip_v1",
            declared_scope=EXPERIMENT_DOMAIN,
            declared_conditions=(DECLARED_SCOPE, "لا معجمَ يُستدعى ولا مدوّنةٌ مُعلَّمة"),
            declared_model_ref="composition-reading",
        ),
        case_set=DeclaredCaseSet(
            case_set_id="declared-two-word-inputs",
            case_ids=tuple(case_id for case_id, _ in DECLARED_INPUTS),
        ),
        inputs=DECLARED_INPUTS,
        permitted_operations=(ExperimentalOperationRef("run_text"),),
        case_outcome_vocabulary=ExperimentalCaseOutcomeVocabulary(
            accounted_token=ACCOUNTED_TOKEN, unaccounted_token=UNACCOUNTED_TOKEN
        ),
    )


def _implementation(
    context: ExperimentalRunContext, input_content: str
) -> tuple[str, Trace]:
    """شغِّل المسارَ على نصّ حالةٍ واحدة، واقرأ مخرجَه بالمفردة المجمّدة."""

    run = context.invoke("run_text", lambda: run_text(input_content))
    token = ACCOUNTED_TOKEN if run.reached_ifada else UNACCOUNTED_TOKEN
    return token, run.trace


def run_under_the_experimental_authority(
    *, run_id: str = "composition-ifada-run"
) -> ExperimentalRunRecord:
    """سُق العيّنةَ المُعلَنةَ كلَّها تحت السلطة التجريبية، بطلبٍ مربوط."""

    bound = ExperimentalRunBindingAuthority(authority_id="arabic-binding").bind(
        binding_id="composition-ifada-binding",
        request=_request(),
        binding=_frozen_experiment(),
    )
    return ExperimentalAuthority(authority_id="arabic-lab").run(
        run_id=run_id, bound_request=bound, implementation=_implementation
    )


@dataclass(frozen=True, slots=True)
class PathCensus:
    """إحصاءُ سَوقٍ واحدٍ للعيّنة: ما بلغ كلَّ طبقة، وما وقف فيها، ولماذا."""

    runs: tuple[PathRun, ...]

    def __post_init__(self) -> None:
        if type(self.runs) is not tuple or not self.runs:
            raise CompositionIfadaExperimentError("إحصاءٌ بلا سَوقٍ واحدٍ لا يُقرأ.")
        for run in self.runs:
            if type(run) is not PathRun:
                raise CompositionIfadaExperimentError("كلُّ مقروءٍ سَوقٌ مُصاغ.")

    @property
    def input_total(self) -> int:
        """المقامُ كلُّه: كلُّ نصٍّ مُعلَنٍ دخل، بلغ أو وقف."""

        return len(self.runs)

    @property
    def reached_counts(self) -> MappingProxyType[PathStage, int]:
        """ما بلغ كلَّ طبقة، وكلُّ طبقةٍ حاضرةٌ ولو بصفر."""

        counts = dict.fromkeys(PathStage, 0)
        for run in self.runs:
            for stage in PathStage:
                if stage.rank <= run.reached.rank:
                    counts[stage] += 1
        return MappingProxyType(counts)

    @property
    def stop_counts(self) -> MappingProxyType[PathStop, int]:
        """ما وقف بكلّ جنس، وكلُّ جنسٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(PathStop, 0)
        for run in self.runs:
            if run.stop is not None:
                counts[run.stop] += 1
        return MappingProxyType(counts)

    @property
    def outcome_counts(self) -> MappingProxyType[StageOutcome, int]:
        """أحكامُ آخر انتقالٍ لكلّ نصّ، وكلُّ حكمٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(StageOutcome, 0)
        for run in self.runs:
            counts[run.outcome] += 1
        return MappingProxyType(counts)

    @property
    def ifada_counts(self) -> MappingProxyType[IfadaStanding, int]:
        """أحوالُ الإفادة، وكلُّ حالٍ حاضرةٌ ولو بصفر."""

        counts = dict.fromkeys(IfadaStanding, 0)
        for run in self.runs:
            counts[run.ifada] += 1
        return MappingProxyType(counts)

    @property
    def composition_counts(self) -> MappingProxyType[CompositionReading, int]:
        """قراءاتُ التركيب المقروءة، وكلُّ قراءةٍ حاضرةٌ ولو بصفر."""

        counts = dict.fromkeys(CompositionReading, 0)
        for run in self.runs:
            if run.composition is not None:
                counts[run.composition] += 1
        return MappingProxyType(counts)

    @property
    def word_total(self) -> int:
        """كلُّ كلمةٍ قُرئت في الطبقات المكتوبة، مقامًا مستقلًّا عن النصوص."""

        return sum(len(run.words) for run in self.runs)

    @property
    def word_retrieved(self) -> int:
        """ما عبر من الكلمات الطبقاتِ المكتوبةَ ورجع كما دخل."""

        return sum(
            1
            for run in self.runs
            for word in run.words
            if word.crossed_the_written_chain
        )

    @property
    def reached_ifada(self) -> int:
        """ما بلغ إفادةً مقروءة؛ وبلوغُ الطبقة ليس قراءةَ الفائدة."""

        return sum(1 for run in self.runs if run.reached_ifada)


def measure() -> PathCensus:
    """سُق العيّنةَ المُعلَنةَ كلَّها في المسار، واقرأ إحصاءَها."""

    return PathCensus(tuple(run_text(text) for _, text in DECLARED_INPUTS))


def render_census(census: PathCensus) -> str:
    """اعرض الإحصاءَ نصًّا، بلا نسبةٍ تُكتَب على مقامٍ لم يُسمَّ."""

    lines = [
        f"المدخلاتُ المُعلَنة: {census.input_total}",
        f"الكلماتُ المقروءة: {census.word_total}"
        f" — استرجاعًا كتابيًّا: {census.word_retrieved}",
        f"ما بلغ إفادةً مقروءة: {census.reached_ifada}",
        "",
        "| الطبقة | ما بلغها |",
        "| --- | --- |",
    ]
    for stage, count in census.reached_counts.items():
        lines.append(f"| {stage.value} | {count} |")
    lines.extend(["", "| جنسُ التوقّف | العدد |", "| --- | --- |"])
    for stop, count in census.stop_counts.items():
        lines.append(f"| {stop.value} | {count} |")
    lines.extend(["", "| حالُ الإفادة | العدد |", "| --- | --- |"])
    for standing, count in census.ifada_counts.items():
        lines.append(f"| {standing.value} | {count} |")
    return "\n".join(lines)


for _law_name, _law_text in COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("كلُّ نصِّ قانونٍ يفتتح باسم قانونه.")
if len(DECLARED_INPUTS) != len({case_id for case_id, _ in DECLARED_INPUTS}):
    raise RuntimeError("معرّفاتُ الحالات لا تتكرّر.")
if ExperimentalOutcomeStatus.COMPLETED.value != "COMPLETED":
    raise RuntimeError("مفردةُ حال التشغيل مقروءةٌ من السلطة لا مُعادةُ التعريف.")
