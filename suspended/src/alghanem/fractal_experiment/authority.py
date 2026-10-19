"""السلطةُ التشغيليّةُ المؤقّتة: إذنُ تشغيلٍ مقيَّدٌ بمداه، لا ترخيصَ فيه ألبتّة.

    ISSUED  →  ACTIVE  →  REVOKED

**والإذنُ إذنُ تشغيلٍ بعينه**: `ExperimentalRunPermit` مربوطٌ بـ`run_id` واحد،
فلا يُستعمَل في تشغيلٍ آخر، ولا يُستعمَل بعد إلغائه، ولا يُعاد تنشيطُه.

**والصلاحيةُ حالٌ لا ساعة** (`ExperimentalAuthorityExpiresWithItsRun`): لا وقتٌ
ولا مدّةٌ ولا بيئةٌ تدخل في صلاحية الإذن؛ الصلاحيةُ حالُه التشغيليّةُ وهويّةُ
تشغيله وحدَهما.

**ولا مُرخِّصَ هنا** (`TemporaryExperimentalAuthority ≠ LicensingAuthority`):
ليس في هذه السلطة بابٌ اسمُه ترخيصٌ ولا شهادة، ولا تُصدِر رتبةً دائمة.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from ..fractal_generation import FractalScaleRef, PatternRef
from .binding import FrozenExperimentBinding
from .laws import (
    EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN,
    EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE,
    TEMPORARY_EXPERIMENTAL_AUTHORITY_IS_NOT_LICENSING_AUTHORITY,
)

__all__ = [
    "ExperimentalAuthorityError",
    "ExperimentalFractalAuthority",
    "ExperimentalPermitState",
    "ExperimentalRunPermit",
]


class ExperimentalAuthorityError(ValueError):
    """رفضٌ عند إصدار إذنٍ تجريبيٍّ أو تنشيطه أو استعماله بعد إلغائه."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد السلطة وحدَها لا بيد المستدعي."""

    __slots__ = ()


_PERMIT_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExperimentalAuthorityError(f"{label} نصٌّ غير فارغ")
    return value


def _named_texts(values: object, label: str) -> tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ExperimentalAuthorityError(f"{label} عضوٌ واحدٌ فأكثر مُصرَّحٌ به")
    for value in values:
        _named_text(value, f"عضوٌ في {label}")
    if len(set(values)) != len(values):
        raise ExperimentalAuthorityError(f"عضوٌ مُكرَّرٌ في {label}")
    return values


class ExperimentalPermitState(Enum):
    """حالُ الإذن التجريبيّ؛ ثلاثةٌ لا رابعَ لها، ولا رجوعَ بعد الإلغاء."""

    ISSUED = "issued"
    ACTIVE = "active"
    REVOKED = "revoked"


@dataclass(frozen=True, slots=True)
class ExperimentalRunPermit:
    """إذنُ تشغيلٍ تجريبيٍّ مؤقّت: مداه مُسمًّى، وهو مربوطٌ بتشغيله بعينه."""

    authority_id: str
    experiment_id: str
    run_id: str
    frozen_specification_ref: str
    frozen_input_set_ref: str
    binding_content_id: str
    permitted_patterns: tuple[PatternRef, ...]
    permitted_operations: tuple[str, ...]
    permitted_source_scales: tuple[FractalScaleRef, ...]
    permitted_target_scales: tuple[FractalScaleRef, ...]
    permitted_branch_birth: bool
    permitted_experimental_lift: bool
    authority_scope: str
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _PERMIT_ISSUANCE:
            raise ExperimentalAuthorityError(
                "الإذنُ ناتجُ سلطةٍ لا حقلٌ يكتبه المستدعي؛ و"
                + EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE
            )
        _named_text(self.authority_id, "مُعرِّفُ السلطة المُصدِرة")
        _named_text(self.experiment_id, "مُعرِّفُ التجربة")
        _named_text(self.run_id, "مُعرِّفُ التشغيل")
        for value, label in (
            (self.frozen_specification_ref, "مرجعُ المواصفة المُجمَّدة"),
            (self.frozen_input_set_ref, "مرجعُ مجموعة المدخلات المُجمَّدة"),
            (self.binding_content_id, "بصمةُ رباط التجميد"),
        ):
            if not is_canonical_digest(value):
                raise ExperimentalAuthorityError(f"{label} بصمةٌ قانونيّة")
        if (
            not isinstance(self.permitted_patterns, tuple)
            or not self.permitted_patterns
        ):
            raise ExperimentalAuthorityError("الأنماطُ المأذونُ فيها نمطٌ واحدٌ فأكثر")
        for pattern_ref in self.permitted_patterns:
            if not isinstance(pattern_ref, PatternRef):
                raise ExperimentalAuthorityError("عضوٌ في أنماط الإذن خارج نوع المرجع")
        _named_texts(self.permitted_operations, "العملياتُ المأذونُ فيها")
        for scales, label in (
            (self.permitted_source_scales, "مقاييسُ المصدر المأذونُ فيها"),
            (self.permitted_target_scales, "مقاييسُ الهدف المأذونُ فيها"),
        ):
            if not isinstance(scales, tuple) or not scales:
                raise ExperimentalAuthorityError(f"{label} مقياسٌ واحدٌ فأكثر")
            for scale_ref in scales:
                if not isinstance(scale_ref, FractalScaleRef):
                    raise ExperimentalAuthorityError(f"عضوٌ في {label} خارج نوع المرجع")
        for flag, label in (
            (self.permitted_branch_birth, "الإذنُ بولادة الفروع"),
            (self.permitted_experimental_lift, "الإذنُ بالرفع التجريبيّ"),
        ):
            if type(flag) is not bool:
                raise ExperimentalAuthorityError(f"{label} حكمٌ ثنائيٌّ صريح")
        _named_text(self.authority_scope, "مدى سلطة الإذن")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإذن للبصمة."""

        return {
            "authority_id": self.authority_id,
            "experiment_id": self.experiment_id,
            "run_id": self.run_id,
            "frozen_specification_ref": self.frozen_specification_ref,
            "frozen_input_set_ref": self.frozen_input_set_ref,
            "binding_content_id": self.binding_content_id,
            "permitted_patterns": [
                {
                    "pattern_id": ref.pattern_id,
                    "contract_content_id": ref.contract_content_id,
                }
                for ref in self.permitted_patterns
            ],
            "permitted_operations": list(self.permitted_operations),
            "permitted_source_scales": [
                {
                    "scale_id": ref.scale_id,
                    "contract_content_id": ref.contract_content_id,
                }
                for ref in self.permitted_source_scales
            ],
            "permitted_target_scales": [
                {
                    "scale_id": ref.scale_id,
                    "contract_content_id": ref.contract_content_id,
                }
                for ref in self.permitted_target_scales
            ],
            "permitted_branch_birth": self.permitted_branch_birth,
            "permitted_experimental_lift": self.permitted_experimental_lift,
            "authority_scope": self.authority_scope,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الإذن؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    def permits_pattern(self, pattern_ref: object) -> bool:
        """أهذا النمطُ ببصمة عقده داخلَ مدى الإذن؟"""

        return pattern_ref in self.permitted_patterns

    def permits_operation(self, operation: object) -> bool:
        """أهذه العمليّةُ باسمها داخلَ مدى الإذن؟"""

        return operation in self.permitted_operations

    def permits_source_scale(self, scale_ref: object) -> bool:
        """أمقياسُ المصدر هذا داخلَ مدى الإذن؟"""

        return scale_ref in self.permitted_source_scales

    def permits_target_scale(self, scale_ref: object) -> bool:
        """أمقياسُ الهدف هذا داخلَ مدى الإذن؟"""

        return scale_ref in self.permitted_target_scales

    def belongs_to_run(self, run_id: object) -> bool:
        """أهذا إذنُ هذا التشغيل بعينه؟"""

        return run_id == self.run_id


class ExperimentalFractalAuthority:
    """سلطةُ تشغيلٍ تجريبيّةٌ مؤقّتة: تُصدِر إذنًا وتُنشِّطه وتُلغيه، ولا تُرخِّص."""

    __slots__ = ("_authority_id", "_states", "_runs")

    def __init__(self, *, authority_id: str) -> None:
        self._authority_id = _named_text(authority_id, "مُعرِّفُ السلطة")
        self._states: dict[str, ExperimentalPermitState] = {}
        self._runs: dict[str, str] = {}

    @property
    def authority_id(self) -> str:
        """مُعرِّفُ هذه السلطة."""

        return self._authority_id

    def issue(
        self,
        *,
        binding: FrozenExperimentBinding,
        experiment_id: str,
        run_id: str,
        permitted_patterns: tuple[PatternRef, ...],
        permitted_operations: tuple[str, ...],
        permitted_source_scales: tuple[FractalScaleRef, ...],
        permitted_target_scales: tuple[FractalScaleRef, ...],
        permitted_branch_birth: bool,
        permitted_experimental_lift: bool,
        authority_scope: str,
    ) -> ExperimentalRunPermit:
        """أصدِر إذنَ تشغيلٍ واحدًا لتشغيلٍ واحد فوق رباطِ تجميدٍ قائم."""

        if not isinstance(binding, FrozenExperimentBinding):
            raise ExperimentalAuthorityError(
                "الإذنُ يقوم على رباطِ تجميدٍ من نوعه لا على مدخلٍ حرٍّ من المستدعي"
            )
        checked_run_id = _named_text(run_id, "مُعرِّفُ التشغيل")
        if checked_run_id in self._runs:
            raise ExperimentalAuthorityError(
                "لهذا التشغيل إذنٌ صادرٌ من هذه السلطة؛ ولا إذنان لتشغيلٍ واحد"
            )
        permit = ExperimentalRunPermit(
            authority_id=self._authority_id,
            experiment_id=_named_text(experiment_id, "مُعرِّفُ التجربة"),
            run_id=checked_run_id,
            frozen_specification_ref=binding.frozen_specification_ref,
            frozen_input_set_ref=binding.frozen_input_set_ref,
            binding_content_id=binding.content_id,
            permitted_patterns=permitted_patterns,
            permitted_operations=permitted_operations,
            permitted_source_scales=permitted_source_scales,
            permitted_target_scales=permitted_target_scales,
            permitted_branch_birth=permitted_branch_birth,
            permitted_experimental_lift=permitted_experimental_lift,
            authority_scope=_named_text(authority_scope, "مدى سلطة الإذن"),
            issuance=_PERMIT_ISSUANCE,
        )
        self._states[permit.content_id] = ExperimentalPermitState.ISSUED
        self._runs[checked_run_id] = permit.content_id
        return permit

    def _checked(self, permit: object) -> ExperimentalRunPermit:
        if not isinstance(permit, ExperimentalRunPermit):
            raise ExperimentalAuthorityError("المقروءُ إذنُ تشغيلٍ من نوعه")
        if permit.authority_id != self._authority_id:
            raise ExperimentalAuthorityError(
                "إذنٌ صادرٌ عن سلطةٍ أخرى لا تتصرّف فيه هذه السلطة؛ و"
                + TEMPORARY_EXPERIMENTAL_AUTHORITY_IS_NOT_LICENSING_AUTHORITY
            )
        if permit.content_id not in self._states:
            raise ExperimentalAuthorityError("إذنٌ غيرُ مُسجَّلٍ في هذه السلطة")
        return permit

    def state_of(self, permit: ExperimentalRunPermit) -> ExperimentalPermitState:
        """حالُ الإذن كما هي في سجلّ سلطته."""

        return self._states[self._checked(permit).content_id]

    def activate(self, permit: ExperimentalRunPermit) -> ExperimentalRunPermit:
        """نشِّط إذنًا صادرًا لم يُنشَّط بعد؛ ولا تنشيطَ بعد الإلغاء."""

        checked = self._checked(permit)
        state = self._states[checked.content_id]
        if state is ExperimentalPermitState.REVOKED:
            raise ExperimentalAuthorityError(
                "لا تنشيطَ لإذنٍ أُلغي؛ و" + EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN
            )
        if state is ExperimentalPermitState.ACTIVE:
            raise ExperimentalAuthorityError("الإذنُ نشطٌ، ولا تنشيطَ مرّتين")
        self._states[checked.content_id] = ExperimentalPermitState.ACTIVE
        return checked

    def revoke(self, permit: ExperimentalRunPermit) -> ExperimentalRunPermit:
        """ألغِ الإذنَ بانتهاء تشغيله؛ ولو نجحت التجربة، فالسلطةُ مؤقّتة."""

        checked = self._checked(permit)
        self._states[checked.content_id] = ExperimentalPermitState.REVOKED
        return checked

    def is_active_for_run(self, permit: ExperimentalRunPermit, *, run_id: str) -> bool:
        """أهذا الإذنُ نشطٌ لهذا التشغيل بعينه؟"""

        checked = self._checked(permit)
        return self._states[
            checked.content_id
        ] is ExperimentalPermitState.ACTIVE and checked.belongs_to_run(run_id)

    def require_active_for_run(
        self, permit: ExperimentalRunPermit, *, run_id: str
    ) -> ExperimentalRunPermit:
        """اطلب إذنًا نشطًا لهذا التشغيل، أو ارفض بسببٍ مُسمًّى."""

        checked = self._checked(permit)
        state = self._states[checked.content_id]
        if state is not ExperimentalPermitState.ACTIVE:
            raise ExperimentalAuthorityError(
                f"الإذنُ في الحال `{state.value}` فلا يُشغَّل به؛ و"
                + EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN
            )
        if not checked.belongs_to_run(_named_text(run_id, "مُعرِّفُ التشغيل")):
            raise ExperimentalAuthorityError(
                "إذنُ تشغيلٍ يُستعمَل في تشغيلٍ آخر؛ و"
                + EXPERIMENTAL_AUTHORITY_EXPIRES_WITH_ITS_RUN
            )
        return checked
