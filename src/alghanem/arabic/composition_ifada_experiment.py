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

from alghanem.canonical_content import canonical_digest
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
    run_bytes,
)
from .mantuq_mafhum_ifada import IfadaStanding

__all__ = [
    "ACCOUNTED_TOKEN",
    "COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS",
    "DECLARED_CASES",
    "DECLARED_INPUTS",
    "EXPERIMENT_DOMAIN",
    "UNACCOUNTED_TOKEN",
    "CompositionIfadaExperimentError",
    "DeclaredCase",
    "PathCensus",
    "measure",
    "render_census",
    "run_under_the_experimental_authority",
]


class CompositionIfadaExperimentError(ValueError):
    """رفضٌ بنيويٌّ في تهيئة السَّوق التجريبيّ، لا في النصّ المقيس."""


EXPERIMENT_DOMAIN: Final[str] = "arabic-two-word-composition"


@dataclass(frozen=True, slots=True)
class DeclaredCase:
    """حالةٌ مُعلَنة: معرّفُها، وبايتاتُها الخام، وسببُ إدخالها.

    والمحفوظُ بايتاتٌ لا نصّ، ليدخل الترميزُ غيرُ الصالح والتغييرُ البايتيُّ
    في العيّنة كما يدخل النصُّ السليم (`ACaseIsRawBytesNotAString`).
    """

    case_id: str
    source: bytes
    why: str

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise CompositionIfadaExperimentError("للحالة معرّفٌ غيرُ فارغ.")
        if type(self.source) is not bytes or not self.source:
            raise CompositionIfadaExperimentError("مدخلُ الحالة بايتاتٌ غيرُ فارغة.")
        if not self.why.strip():
            raise CompositionIfadaExperimentError("لكلّ حالةٍ سببُ إدخالها مكتوبًا.")

    @property
    def hex_content(self) -> str:
        """البايتاتُ الخامُ مكتوبةً ستَّ عشريّةً، وهو محتوى الحالة في الطلب."""

        return self.source.hex()

    @property
    def source_digest(self) -> str:
        """بصمةُ البايتات الخام كما وردت، بلا ترميزٍ وسيطٍ ولا تسوية."""

        return canonical_digest(self.source)

    @property
    def byte_length(self) -> int:
        """طولُ البايتات الخام، عدًّا للبايتات لا للمحارف."""

        return len(self.source)


def _WITH_BYTE_CHANGED(source: bytes, old: bytes, new: bytes) -> bytes:
    """أبدِل أوّلَ وقوعٍ لسلسلةِ بايتاتٍ بأخرى، تغييرًا بايتيًّا مُعلَنًا."""

    if old not in source:
        raise CompositionIfadaExperimentError(
            "التغييرُ البايتيُّ يُعلَن على بايتاتٍ موجودةٍ فعلًا في المدخل."
        )
    return source.replace(old, new, 1)


ACCOUNTED_TOKEN: Final[str] = "ACCOUNTED:بلغ النصُّ إفادةً مقروءة"
UNACCOUNTED_TOKEN: Final[str] = "UNACCOUNTED:وقف النصُّ دون إفادةٍ مقروءة"

DECLARED_CASES: Final[tuple[DeclaredCase, ...]] = (
    DeclaredCase("isnad-1", "اللَّهُ نُورٌ".encode(), "موجب: ضمّتان تُقرآن إسنادًا"),
    DeclaredCase("isnad-2", "مُحَمَّدٌ رَسُولٌ".encode(), "موجب: ضمّتان مع تنوين الثاني"),
    DeclaredCase("idafa-1", "نُورُ السَّمَاوَاتِ".encode(), "سالب: تركيبٌ قائمٌ لا يُفيد"),
    DeclaredCase("idafa-2", "نُورُ كِتَابٍ".encode(), "سالب: إضافةٌ بتنوين الثاني"),
    DeclaredCase("proclitic-1", "الْحَمْدُ لِلَّهِ".encode(), "ملتبس: لامٌ مكسورةٌ قد تكون جارّة"),
    DeclaredCase("unwritten-1", "قُلْ هُوَ".encode(), "غيرُ مقروءٍ: لا علامةَ آخِرٍ مكتوبة"),
    DeclaredCase("tanwin-conflict-1", "كِتَابٌ الْبَيْتِ".encode(), "ممنوع: المضافُ لا يُنوَّن"),
    DeclaredCase(
        "first-not-raf-1", "الْعَالَمِينَ نُورٌ".encode(), "غيرُ مقروءٍ: أوّلُه ليس مرفوعًا"
    ),
    DeclaredCase(
        "second-nasb-1", "رَبُّ الْعَالَمِينَ".encode(), "غيرُ مقروءٍ: ثانيه منصوبُ العلامة"
    ),
    DeclaredCase("not-two-words-1", "اللَّهُ".encode(), "خارجُ النطاق: كلمةٌ واحدة"),
    DeclaredCase(
        "byte-mutation-vowel",
        _WITH_BYTE_CHANGED("اللَّهُ نُورٌ".encode(), "\u064f".encode(), "\u0650".encode()),
        "تغييرٌ بايتيّ: ضمّةُ الأوّل تُبدَّل كسرةً، فيتغيّر الحكم",
    ),
    DeclaredCase(
        "byte-mutation-space",
        "اللَّهُ نُورٌ".encode().replace(b" ", b""),
        "تغييرٌ بايتيّ: يُحذَف البياض، فتصير كلمةً واحدة",
    ),
    DeclaredCase(
        "byte-truncated-utf8",
        "اللَّهُ نُورٌ".encode()[:-1],
        "ترميزٌ غيرُ صالح: بايتاتٌ مبتورةٌ في منتصف حرف",
    ),
    DeclaredCase(
        "byte-invalid-lead",
        b"\xff\xfe" + "اللَّهُ نُورٌ".encode(),
        "ترميزٌ غيرُ صالح: بايتُ بدءٍ لا يقع في UTF-8",
    ),
    DeclaredCase(
        "byte-lone-continuation",
        "اللَّهُ".encode() + b"\x80\x80" + " نُورٌ".encode(),
        "ترميزٌ غيرُ صالح: بايتا استمرارٍ بلا بادئة",
    ),
)
"""العيّنةُ المُعلَنةُ قبل التشغيل، ببايتاتها الخام لا بنصوصها.

وفيها الموجبُ والسالبُ والملتبس، وتغييراتٌ بايتيّةٌ تُغيّر الحكم، وترميزٌ غيرُ
صالحٍ بثلاث صورٍ متمايزة، وحالاتٌ يبقى فيها التركيبُ أو الإفادةُ غيرَ مقروءَين.
وهي مُجمَّدةٌ قبل قراءة أيّ نتيجة، فلا تُوسَّع ولا تُضيَّق بعد رؤية ما بلغ
الإفادةَ منها.
"""

DECLARED_INPUTS: Final[tuple[tuple[str, str], ...]] = tuple(
    (case.case_id, case.hex_content) for case in DECLARED_CASES
)
"""مدخلاتُ الطلب: لكلّ حالةٍ معرّفُها ومحتواها السُّتّ عشريّ لا نصُّها."""

COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS: Final[dict[str, str]] = {
    "AStopStaysInTheDenominator": (
        "AStopStaysInTheDenominator: الواقفُ والمؤجَّلُ والممنوع يُعَدّون في "
        "المقام كلِّه، ولا يُحذَف أحدُهم ليرتفع ما بلغ الإفادة. وكلُّ توقّفٍ "
        "يُنسَب إلى طبقته وجنسه لا إلى «فشل»"
    ),
    "ACaseIsRawBytesNotAString": (
        "ACaseIsRawBytesNotAString: الحالةُ المُعلَنةُ بايتاتٌ خامٌّ تُكتَب في "
        "الطلب ستَّ عشريّة، لا نصًّا مفكوكَ الترميز. وبذلك يدخل الترميزُ غيرُ "
        "الصالح والتغييرُ البايتيُّ في العيّنة كما يدخل النصُّ السليم، ولا "
        "يُستثنى ما لا يُفَكّ"
    ),
    "TheCensusIsBoundToItsRunRecord": (
        "TheCensusIsBoundToItsRunRecord: الإحصاءُ لا يُقرأ إلّا من سجلِّ تشغيلٍ "
        "تامٍّ صادرٍ عن السلطة، ويحمل بصمةَ محتوى طلبه. وموافقةُ الإحصاء "
        "للسجلّ **تُقاس** في `agrees_with_the_run_record` حالةً حالةً، ولا "
        "تُفترَض بكونهما شُغّلا في دالّةٍ واحدة"
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
        permitted_operations=(ExperimentalOperationRef("run_bytes"),),
        case_outcome_vocabulary=ExperimentalCaseOutcomeVocabulary(
            accounted_token=ACCOUNTED_TOKEN, unaccounted_token=UNACCOUNTED_TOKEN
        ),
    )


def _implementation(
    context: ExperimentalRunContext, input_content: str
) -> tuple[str, Trace]:
    """شغِّل المسارَ على نصّ حالةٍ واحدة، واقرأ مخرجَه بالمفردة المجمّدة."""

    source = bytes.fromhex(input_content)
    run = context.invoke("run_bytes", lambda: run_bytes(source))
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

    record: ExperimentalRunRecord
    cases: tuple[DeclaredCase, ...]
    runs: tuple[PathRun, ...]

    def __post_init__(self) -> None:
        if type(self.record) is not ExperimentalRunRecord:
            raise CompositionIfadaExperimentError(
                "الإحصاءُ مربوطٌ بسجلِّ تشغيلٍ صادرٍ عن السلطة، لا بقياسٍ حرّ."
            )
        if self.record.outcome_status is not ExperimentalOutcomeStatus.COMPLETED:
            raise CompositionIfadaExperimentError(
                "لا يُقرأ إحصاءٌ من سجلٍّ لم يتمّ؛ وسببُ عدم تمامه يُقرأ في موضعه."
            )
        if type(self.runs) is not tuple or not self.runs:
            raise CompositionIfadaExperimentError("إحصاءٌ بلا سَوقٍ واحدٍ لا يُقرأ.")
        if len(self.cases) != len(self.runs):
            raise CompositionIfadaExperimentError("لكلّ حالةٍ مُعلَنةٍ سَوقُها.")
        for case, run in zip(self.cases, self.runs, strict=True):
            if type(run) is not PathRun or type(case) is not DeclaredCase:
                raise CompositionIfadaExperimentError("كلُّ مقروءٍ حالةٌ وسَوقُها.")
            if run.source != case.source:
                raise CompositionIfadaExperimentError(
                    "سَوقُ الحالة يُقرأ من بايتاتها نفسِها لا من بايتاتٍ أخرى."
                )

    @property
    def record_tokens(self) -> MappingProxyType[str, str]:
        """مفرداتُ الجواب كما كتبها سجلُّ التشغيل نفسُه، لا كما أعدناها."""

        content = self.record.output_content or ""
        tokens: dict[str, str] = {}
        for line in content.splitlines():
            case_id, _, token = line.partition("=")
            tokens[case_id] = token
        return MappingProxyType(tokens)

    @property
    def agrees_with_the_run_record(self) -> bool:
        """أيوافق ما أحصيناه ما كتبه السجلُّ لكلّ حالةٍ بعينها؟

        وهذا ربطُ الإحصاء بالسجلّ قياسًا لا دعوى: لو أحصينا سَوقًا غيرَ الذي
        شغّلته السلطةُ لَظهر الخُلفُ ههنا ولم يُطوَ.
        """

        tokens = self.record_tokens
        if set(tokens) != {case.case_id for case in self.cases}:
            return False
        for case, run in zip(self.cases, self.runs, strict=True):
            expected = ACCOUNTED_TOKEN if run.reached_ifada else UNACCOUNTED_TOKEN
            if tokens[case.case_id] != expected:
                return False
        return True

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


def measure(*, run_id: str = "composition-ifada-run") -> PathCensus:
    """سُق العيّنةَ تحت السلطة، ثمّ اقرأ إحصاءَها مربوطًا بسجلِّ تشغيلها.

    ولا إحصاءَ ههنا خارجَ سلطة: السجلُّ يُشتَقّ أوّلًا، ثمّ تُعاد قراءةُ كلّ
    حالةٍ من بايتاتها نفسِها، ويُقاس توافقُ القراءتين في
    `agrees_with_the_run_record` ولا يُفترَض.
    """

    record = run_under_the_experimental_authority(run_id=run_id)
    return PathCensus(
        record=record,
        cases=DECLARED_CASES,
        runs=tuple(run_bytes(case.source) for case in DECLARED_CASES),
    )


def render_census(census: PathCensus) -> str:
    """اعرض الإحصاءَ نصًّا، بلا نسبةٍ تُكتَب على مقامٍ لم يُسمَّ."""

    lines = [
        f"سجلُّ التشغيل: {census.record.run_id}"
        f" ({census.record.outcome_status.value})",
        f"بصمةُ محتوى الطلب: {census.record.request_content_digest[:16]}…",
        f"الإحصاءُ يوافق السجلَّ: {census.agrees_with_the_run_record}",
        "",
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
    lines.extend(
        [
            "",
            "| الحالة | بايتاتٌ | بصمتُها | بلغ | الجواب |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    tokens = census.record_tokens
    for case, run in zip(census.cases, census.runs, strict=True):
        answer = tokens[case.case_id].split(":", 1)[0]
        lines.append(
            f"| {case.case_id} | {case.byte_length} | {case.source_digest[:12]}…"
            f" | {run.reached.value} | {answer} |"
        )
    return "\n".join(lines)


for _law_name, _law_text in COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("كلُّ نصِّ قانونٍ يفتتح باسم قانونه.")
if len(DECLARED_INPUTS) != len({case_id for case_id, _ in DECLARED_INPUTS}):
    raise RuntimeError("معرّفاتُ الحالات لا تتكرّر.")
if ExperimentalOutcomeStatus.COMPLETED.value != "COMPLETED":
    raise RuntimeError("مفردةُ حال التشغيل مقروءةٌ من السلطة لا مُعادةُ التعريف.")
