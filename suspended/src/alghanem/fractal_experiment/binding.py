"""المُجمَّدُ قبل التشغيل: ربطُ تشغيلٍ بمحتوًى مُجمَّدٍ سابقٍ لا يكتبه المستدعي حرًّا.

    FrozenExperimentBinding  →  TemporaryExperimentalPermit  →  ExperimentalRun

**والمدخلُ غيرُ التوقّع** (`FrozenExpectation ≠ GenerativeInput`): الرباطُ
يُسمّي حقولَ المدخل التي يراها المُولِّد، ويُسمّي معها **الحقولَ المحجوبة**
التي لا تدخل المُولِّدَ البتّة وإنّما تُقرأ بعد التشغيل؛ فلا يُلقَّن المُولِّدُ
جوابَه من وسمٍ أو تنبّؤٍ مُجمَّدٍ معه.

**وهذه الطبقةُ عامّةٌ محايدة**: لا تستورد عربيّةً ولا لغةً بعينها؛ تقبل مرجعَ
محتوًى مُجمَّدٍ عامًّا يُصدِره مُحوِّلٌ خارجها.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .laws import (
    FROZEN_EXPECTATION_IS_NOT_GENERATIVE_INPUT,
    FROZEN_INPUT_IS_NOT_PROVEN_STRUCTURE,
)

__all__ = [
    "FrozenExperimentBinding",
    "FrozenExperimentBindingError",
    "FrozenInputEntry",
]


class FrozenExperimentBindingError(ValueError):
    """رفضٌ عند تكوين رباطِ تجميدٍ أو مدخلةٍ مُجمَّدة."""


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FrozenExperimentBindingError(f"{label} نصٌّ غير فارغ")
    return value


def _named_texts(values: object, label: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise FrozenExperimentBindingError(f"{label} مجموعةٌ مُصرَّحٌ بها")
    for value in values:
        _named_text(value, f"عضوٌ في {label}")
    if len(set(values)) != len(values):
        raise FrozenExperimentBindingError(f"عضوٌ مُكرَّرٌ في {label}")
    return values


def _canonical_digest_text(value: object, label: str) -> str:
    if not is_canonical_digest(value):
        raise FrozenExperimentBindingError(f"{label} بصمةٌ قانونيّة")
    assert isinstance(value, str)
    return value


@dataclass(frozen=True, slots=True)
class FrozenInputEntry:
    """مدخلةٌ مُجمَّدةٌ واحدة: مُعرِّفُها، وبصمةُ محتواها، وسببُ إدخالها."""

    input_id: str
    content_id: str
    admission_reason: str

    def __post_init__(self) -> None:
        _named_text(self.input_id, "مُعرِّفُ المدخلة المُجمَّدة")
        _canonical_digest_text(self.content_id, "بصمةُ المدخلة المُجمَّدة")
        _named_text(self.admission_reason, "سببُ إدخال المدخلة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المدخلة للبصمة."""

        return {
            "input_id": self.input_id,
            "content_id": self.content_id,
            "admission_reason": self.admission_reason,
        }


@dataclass(frozen=True, slots=True)
class FrozenExperimentBinding:
    """رباطُ تشغيلٍ بمحتوًى مُجمَّدٍ سابق؛ يُسمّي المرئيَّ للمُولِّد والمحجوبَ عنه."""

    binding_id: str
    source_id: str
    frozen_specification_ref: str
    frozen_input_set_ref: str
    preregistration_content_id: str
    entries: tuple[FrozenInputEntry, ...]
    generator_visible_fields: tuple[str, ...]
    held_out_readout_fields: tuple[str, ...]

    def __post_init__(self) -> None:
        _named_text(self.binding_id, "مُعرِّفُ الرباط")
        _named_text(self.source_id, "مُعرِّفُ مصدر المُجمَّد")
        _canonical_digest_text(self.frozen_specification_ref, "مرجعُ المواصفة المُجمَّدة")
        _canonical_digest_text(
            self.frozen_input_set_ref, "مرجعُ مجموعة المدخلات المُجمَّدة"
        )
        _canonical_digest_text(self.preregistration_content_id, "بصمةُ التسجيل المُسبَق")
        if not isinstance(self.entries, tuple) or not self.entries:
            raise FrozenExperimentBindingError(
                "الرباطُ مدخلةٌ مُجمَّدةٌ واحدةٌ فأكثر؛ و"
                + FROZEN_INPUT_IS_NOT_PROVEN_STRUCTURE
            )
        seen: set[str] = set()
        for entry in self.entries:
            if not isinstance(entry, FrozenInputEntry):
                raise FrozenExperimentBindingError("عضوٌ في مدخلات الرباط خارج نوعه")
            if entry.input_id in seen:
                raise FrozenExperimentBindingError("مُعرِّفُ مدخلةٍ مُكرَّرٌ في رباطٍ واحد")
            seen.add(entry.input_id)
        visible = _named_texts(self.generator_visible_fields, "حقولُ المُولِّد المرئيّة")
        held_out = _named_texts(self.held_out_readout_fields, "الحقولُ المحجوبة")
        if not visible:
            raise FrozenExperimentBindingError("حقلٌ مرئيٌّ واحدٌ فأكثر للمُولِّد")
        overlap = set(visible) & set(held_out)
        if overlap:
            raise FrozenExperimentBindingError(
                "حقلٌ مرئيٌّ ومحجوبٌ معًا يُلقِّن المُولِّدَ جوابَه؛ و"
                + FROZEN_EXPECTATION_IS_NOT_GENERATIVE_INPUT
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الرباط للبصمة."""

        return {
            "binding_id": self.binding_id,
            "source_id": self.source_id,
            "frozen_specification_ref": self.frozen_specification_ref,
            "frozen_input_set_ref": self.frozen_input_set_ref,
            "preregistration_content_id": self.preregistration_content_id,
            "entries": [entry.as_canonical_content() for entry in self.entries],
            "generator_visible_fields": list(self.generator_visible_fields),
            "held_out_readout_fields": list(self.held_out_readout_fields),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الرباط؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    @property
    def input_ids(self) -> frozenset[str]:
        """مُعرِّفاتُ المدخلات المُجمَّدة مجموعةً بلا ترتيبٍ ولا ترجيح."""

        return frozenset(entry.input_id for entry in self.entries)

    def entry_for(self, input_id: str) -> FrozenInputEntry:
        """مدخلةٌ مُجمَّدةٌ باسمها، أو رفضٌ إن لم تكن في الرباط."""

        for entry in self.entries:
            if entry.input_id == input_id:
                return entry
        raise FrozenExperimentBindingError("لا مدخلةَ بهذا المُعرِّف في هذا الرباط")

    def refuse_held_out_fields(self, projected_input: Mapping[str, object]) -> None:
        """ارفض مدخلًا توليديًّا يحمل حقلًا محجوبًا؛ فالوسمُ لا يُلقَّن للمُولِّد."""

        if not isinstance(projected_input, Mapping):
            raise FrozenExperimentBindingError("المدخلُ التوليديُّ رابطةُ أسماءٍ وقيم")
        leaked = tuple(
            sorted(
                name for name in self.held_out_readout_fields if name in projected_input
            )
        )
        if leaked:
            raise FrozenExperimentBindingError(
                "حقلٌ محجوبٌ نزل في مدخل المُولِّد: "
                + "، ".join(leaked)
                + "؛ و"
                + FROZEN_EXPECTATION_IS_NOT_GENERATIVE_INPUT
            )
        unknown = tuple(
            sorted(
                name
                for name in projected_input
                if name not in self.generator_visible_fields
            )
        )
        if unknown:
            raise FrozenExperimentBindingError(
                "حقلٌ غيرُ مُصرَّحٍ به نزل في مدخل المُولِّد: " + "، ".join(unknown)
            )
