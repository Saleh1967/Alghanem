"""`G0.EVAL-0.REPORT`: تقريرُ تشغيلٍ مُجمَّد، وأوّلُه مرجعٌ لا يُستبدَل.

    AFirstRunHappensOnce

التشغيلُ الأوّل بهويّة نظامٍ وطلبٍ بعينهما هو المرجع. وإعادةٌ مطابقةٌ بايتًا
بايتًا تُسجَّل شاهدًا على الحتميّة ولا تحلّ محلّه. وإعادةٌ مختلفةٌ بالمفتاح نفسه
تُرفَض وتُسجَّل مخالفةً مُسمّاةً، ولا تُطوى ولا تُكتَب فوق الأوّل.

والتقريرُ يُطابَق على ما سُلِّم فعلًا: بصمةُ الحمولة، وبصماتُ الطلب الأربع. فلو
اختلف أحدُها كان التقريرُ عن امتحانٍ آخر ولو تشابهت مخرجاتُه.

والتغطيةُ تامّةٌ لا أحسنُ جهد: كلُّ عضوٍ في المجال إمّا مُصنَّفٌ في المخرجات أو
مُسمًّى في البقايا، ولا يُطوى متروك.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .binding import BoundEvaluationRequest, EvaluationBinding
from .laws import A_FIRST_RUN_HAPPENS_ONCE, EvaluationError

__all__ = [
    "FrozenRunReport",
    "RunLedger",
]


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{label} نصٌّ غير فارغ")
    return value


def _require_digest(value: object, label: str) -> str:
    if not is_canonical_digest(value):
        raise EvaluationError(f"{label} بصمةٌ قانونيّةٌ لا نصٌّ حرّ")
    assert isinstance(value, str)
    return value


@dataclass(frozen=True, slots=True)
class FrozenRunReport:
    """تقريرُ تشغيلٍ مُجمَّد: ما رُبِط به، وما سُلِّم إليه، وما أخرجه، وما تركه."""

    request_id: str
    system_content_id: str
    payload_digest: str
    outputs: tuple[tuple[str, str], ...]
    residuals: tuple[str, ...]
    trace: tuple[str, ...]
    run_ordinal: int

    def __post_init__(self) -> None:
        _require_digest(self.request_id, "بصمةُ الطلب")
        _require_digest(self.system_content_id, "بصمةُ هويّة القارئ")
        _require_digest(self.payload_digest, "بصمةُ الحمولة المُسلَّمة")
        if not isinstance(self.outputs, tuple):
            raise EvaluationError("مخرجاتُ التشغيل صفٌّ مُجمَّد لا قائمة")
        member_ids = []
        for entry in self.outputs:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise EvaluationError("المخرَجُ زوجٌ: عضوٌ وتصنيفُه")
            _require_text(entry[0], "مُعرِّفُ العضو في المخرَج")
            _require_text(entry[1], f"تصنيفُ `{entry[0]}`")
            member_ids.append(entry[0])
        if len(set(member_ids)) != len(member_ids):
            raise EvaluationError("عضوٌ مُصنَّفٌ مرّتين؛ والمكرّرُ يُرفَض لا يُطوى")
        if not isinstance(self.residuals, tuple):
            raise EvaluationError("البقايا صفٌّ مُجمَّد لا قائمة")
        for residual in self.residuals:
            _require_text(residual, "عضوٌ في البقايا")
        if len(set(self.residuals)) != len(self.residuals):
            raise EvaluationError("بقيّةٌ مُكرَّرة؛ والمكرّرُ يُرفَض لا يُطوى")
        overlap = set(member_ids) & set(self.residuals)
        if overlap:
            raise EvaluationError("عضوٌ مُصنَّفٌ وبقيّةٌ معًا: " + "، ".join(sorted(overlap)))
        if not self.outputs and not self.residuals:
            raise EvaluationError("تقريرٌ بلا مخرَجٍ ولا بقيّةٍ لا يشهد بشيء")
        if not isinstance(self.trace, tuple) or not self.trace:
            raise EvaluationError("تقريرٌ بلا أثرٍ لا يُدقَّق")
        for line in self.trace:
            _require_text(line, "سطرٌ في الأثر")
        if not isinstance(self.run_ordinal, int) or self.run_ordinal < 1:
            raise EvaluationError("رتبةُ التشغيل عددٌ صحيحٌ موجب، وأوّلُها واحد")

    @property
    def is_a_first_run(self) -> bool:
        """أهذا تشغيلٌ أوّلُ بهويّته وطلبه؟"""

        return self.run_ordinal == 1

    @property
    def first_run_law(self) -> str:
        """قانونُ التشغيل الأوّل."""

        return A_FIRST_RUN_HAPPENS_ONCE

    @property
    def classified_member_ids(self) -> tuple[str, ...]:
        """أعضاءُ المجال المُصنَّفون في هذا التشغيل."""

        return tuple(sorted(member_id for member_id, _ in self.outputs))

    def as_run_content(self) -> dict[str, object]:
        """محتوى التشغيل بلا رتبته؛ عليه تُقاس الحتميّةُ بين إعادتين."""

        return {
            "request_id": self.request_id,
            "system_content_id": self.system_content_id,
            "payload_digest": self.payload_digest,
            "outputs": [list(entry) for entry in sorted(self.outputs)],
            "residuals": list(sorted(self.residuals)),
            "trace": list(self.trace),
        }

    @property
    def run_content_digest(self) -> str:
        """بصمةُ محتوى التشغيل بلا رتبته."""

        return canonical_digest(canonical_bytes(self.as_run_content()))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التقرير للبصمة، ورتبتُه فيه."""

        return {**self.as_run_content(), "run_ordinal": self.run_ordinal}

    @property
    def report_digest(self) -> str:
        """بصمةُ التقرير؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


class RunLedger:
    """سجلُّ التشغيلات: يُثبِّت الأوّلَ، ويقبل المطابق شاهدًا، ويرفض المختلف."""

    def __init__(self, binding: EvaluationBinding) -> None:
        if not isinstance(binding, EvaluationBinding):
            raise EvaluationError("السجلُّ يقوم على ربطٍ مُجمَّدٍ من نوعه")
        self._binding = binding
        self._requests: dict[str, BoundEvaluationRequest] = {
            request.request_id: request for request in binding.requests
        }
        self._first: dict[str, FrozenRunReport] = {}
        self._repeats: list[FrozenRunReport] = []
        self._violations: list[str] = []

    @property
    def binding(self) -> EvaluationBinding:
        """الربطُ الذي يُدقَّق عليه كلُّ تقرير."""

        return self._binding

    @property
    def violations(self) -> tuple[str, ...]:
        """المخالفاتُ المُسجَّلة؛ تُسمّى جميعًا ولا يُوقَف عند أوّلها."""

        return tuple(self._violations)

    @property
    def repeat_reports(self) -> tuple[FrozenRunReport, ...]:
        """الإعاداتُ المطابقة، شواهدَ حتميّةٍ لا بدائلَ عن الأوّل."""

        return tuple(self._repeats)

    def first_report(self, system_content_id: str) -> FrozenRunReport:
        """تقريرُ التشغيل الأوّل لهذا القارئ؛ والغيابُ رفضٌ لا `None`."""

        report = self._first.get(system_content_id)
        if report is None:
            raise EvaluationError(
                "لا تقريرَ تشغيلٍ أوّلَ لهذا القارئ؛ ولا فتحَ قبل تقارير التشغيل"
            )
        return report

    @property
    def has_a_first_report_for_every_reader(self) -> bool:
        """أَلِكلِّ قارئٍ مطلوبٍ تقريرُ تشغيلٍ أوّلُ مُجمَّد؟"""

        return set(self._binding.required_system_content_ids) <= set(self._first)

    @property
    def missing_system_content_ids(self) -> tuple[str, ...]:
        """القرّاءُ الذين لم يُسجَّل لهم تشغيلٌ أوّل، مُسمَّين جميعًا."""

        return tuple(
            sorted(set(self._binding.required_system_content_ids) - set(self._first))
        )

    def _refuse_an_unbound_report(self, report: FrozenRunReport) -> None:
        request = self._requests.get(report.request_id)
        if request is None:
            raise EvaluationError("تقريرٌ بطلبٍ خارج هذا الربط؛ فهو عن امتحانٍ آخر")
        if request.system_content_id != report.system_content_id:
            raise EvaluationError("تقريرٌ بهويّة قارئٍ غيرِ التي رُبِط بها طلبُه")
        if report.payload_digest != self._binding.payload.payload_digest:
            raise EvaluationError("تقريرٌ على حمولةٍ غيرِ التي سُلِّمت؛ فهو عن غيرها")

    def _refuse_an_incomplete_coverage(self, report: FrozenRunReport) -> None:
        declared = set(report.classified_member_ids) | set(report.residuals)
        members = set(self._binding.contract.body.member_ids)
        stray = declared - members
        if stray:
            raise EvaluationError(
                "عضوٌ خارج المجال في التقرير: " + "، ".join(sorted(stray))
            )
        missing = members - declared
        if missing:
            raise EvaluationError(
                "التغطيةُ تامّةٌ لا أحسنَ جهد؛ والأعضاءُ المتروكون: "
                + "، ".join(sorted(missing))
            )

    def record(self, report: FrozenRunReport) -> FrozenRunReport:
        """سجِّل تقريرًا مُجمَّدًا؛ الأوّلُ مرجعٌ، والمطابقُ شاهد، والمختلفُ رفض."""

        if not isinstance(report, FrozenRunReport):
            raise EvaluationError("السجلُّ يقبل تقريرًا مُجمَّدًا من نوعه")
        self._refuse_an_unbound_report(report)
        self._refuse_an_incomplete_coverage(report)
        reference = self._first.get(report.system_content_id)
        if reference is None:
            if not report.is_a_first_run:
                raise EvaluationError(
                    "أوّلُ تشغيلٍ رتبتُه واحد؛ ولا يُقدَّم تشغيلٌ لاحقٌ في موضعه"
                )
            self._first[report.system_content_id] = report
            return report
        if report.is_a_first_run:
            violation = (
                "إعادةُ تشغيلٍ تدّعي أنّها الأولى بهويّة النظام نفسِها: "
                + report.system_content_id[:16]
            )
            self._violations.append(violation)
            raise EvaluationError(A_FIRST_RUN_HAPPENS_ONCE + "؛ و" + violation)
        if report.run_content_digest != reference.run_content_digest:
            violation = (
                "إعادةُ تشغيلٍ مختلفةٌ بالمفتاح نفسه: "
                + report.system_content_id[:16]
                + "/"
                + report.request_id[:16]
            )
            self._violations.append(violation)
            raise EvaluationError(A_FIRST_RUN_HAPPENS_ONCE + "؛ و" + violation)
        if any(
            repeat.run_ordinal == report.run_ordinal
            and repeat.system_content_id == report.system_content_id
            for repeat in self._repeats
        ):
            raise EvaluationError("رتبةُ تشغيلٍ مُكرَّرة؛ والمكرّرُ يُرفَض لا يُطوى")
        self._repeats.append(report)
        return reference
