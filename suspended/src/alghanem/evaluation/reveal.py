"""`G0.EVAL-0.REVEAL`: سلطةُ فتح الجواب، مشروطةً بتجميدٍ تامٍّ قبلها.

السلطةُ لا تقرأ جوابًا ولا عشوائيّةً من المستودع: تستقبلهما وقتَ الفتح، وتتحقّق
أنّهما يفتحان الالتزامَ المربوط بجسم العقد، ثمّ تُصدِر سجلًّا لا يحمل واحدًا
منهما.

    NoEvaluationVerdictBefore:
          FrozenContract
        ∧ FrozenSystemIdentity
        ∧ FrozenProtocol
        ∧ BoundRequest
        ∧ FrozenFirstRunReports
        ∧ ValidGoldReveal

وسجلُّ الفتح ليس حكمًا: يُثبِت أنّ الالتزامَ فُتِح بعد تجميدٍ تامّ، ولا يقول أيُّ
قارئٍ أصاب. ولا دالّةَ مقارنةٍ ولا سيطرةٍ في هذا الطور أصلًا.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .laws import (
    A_REVEAL_RECORD_IS_NOT_A_VERDICT,
    NO_EVALUATION_VERDICT_BEFORE,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
    EvaluationError,
)
from .report import RunLedger

__all__ = [
    "GoldRevealAuthority",
    "GoldRevealRecord",
]


@dataclass(frozen=True, slots=True)
class GoldRevealRecord:
    """سجلُّ فتحٍ: بصماتُ ما أُثبِت، ولا جوابَ فيه ولا عشوائيّة ولا حكم."""

    contract_digest: str
    contract_body_digest: str
    commitment_digest: str
    evaluation_protocol_digest: str
    binding_digest: str
    first_report_digests: tuple[tuple[str, str], ...]
    revealed_member_count: int

    def __post_init__(self) -> None:
        for label, value in (
            ("بصمةُ العقد", self.contract_digest),
            ("بصمةُ جسم العقد", self.contract_body_digest),
            ("بصمةُ الالتزام", self.commitment_digest),
            ("بصمةُ البروتوكول", self.evaluation_protocol_digest),
            ("بصمةُ الربط", self.binding_digest),
        ):
            if not is_canonical_digest(value):
                raise EvaluationError(f"{label} بصمةٌ قانونيّةٌ لا نصٌّ حرّ")
        if not isinstance(self.first_report_digests, tuple):
            raise EvaluationError("بصماتُ التقارير الأولى صفٌّ مُجمَّد")
        if len(self.first_report_digests) < 2:
            raise EvaluationError("لا فتحَ إلّا بتقريرين أوّلين فأكثر")
        readers = [entry[0] for entry in self.first_report_digests]
        if len(set(readers)) != len(readers):
            raise EvaluationError("قارئٌ مُكرَّرٌ في سجلّ الفتح؛ والمكرّرُ يُرفَض")
        if (
            not isinstance(self.revealed_member_count, int)
            or self.revealed_member_count < 1
        ):
            raise EvaluationError("عددُ الأعضاء المفتوحة عددٌ صحيحٌ موجب")

    @property
    def withholds_gold_and_nonce(self) -> bool:
        """أيخلو السجلُّ من حقلٍ يحمل جوابًا أو عشوائيّة؟ يُفحَص على الحقول."""

        declared = tuple(GoldRevealRecord.__dataclass_fields__)
        return not any(
            name in declared
            for name in ("gold", "labels", "nonce", "canonical_gold", "answers")
        )

    @property
    def is_not_a_verdict(self) -> bool:
        """أيمتنع هذا السجلُّ عن الحكم؟ ولا حكمَ في هذا الطور بالبناء."""

        return True

    @property
    def verdict_law(self) -> str:
        """قانونُ منع الحكم قبل تمام التجميد والفتح."""

        return NO_EVALUATION_VERDICT_BEFORE

    @property
    def claim_ceiling(self) -> str:
        """سقفُ ما يجوز أن يُقرَأ من أيّ قراءةٍ لاحقةٍ لهذا المجال."""

        return OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السجلّ للبصمة."""

        return {
            "contract_digest": self.contract_digest,
            "contract_body_digest": self.contract_body_digest,
            "commitment_digest": self.commitment_digest,
            "evaluation_protocol_digest": self.evaluation_protocol_digest,
            "binding_digest": self.binding_digest,
            "first_report_digests": [
                list(entry) for entry in sorted(self.first_report_digests)
            ],
            "revealed_member_count": self.revealed_member_count,
            "not_a_verdict": A_REVEAL_RECORD_IS_NOT_A_VERDICT,
        }

    @property
    def record_digest(self) -> str:
        """بصمةُ سجلّ الفتح."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


class GoldRevealAuthority:
    """سلطةُ الفتح: لا تملك جوابًا ولا عشوائيّة، وتفتح بشروطٍ مُسمّاةٍ فقط."""

    def __init__(self, ledger: RunLedger) -> None:
        if not isinstance(ledger, RunLedger):
            raise EvaluationError("سلطةُ الفتح تقوم على سجلِّ تشغيلاتٍ من نوعه")
        self._ledger = ledger

    @property
    def ledger(self) -> RunLedger:
        """سجلُّ التشغيلات الذي يُشترَط تمامُه قبل الفتح."""

        return self._ledger

    @property
    def may_reveal(self) -> bool:
        """أتوافرت تقاريرُ التشغيل الأولى لكلِّ قارئٍ مطلوب؟"""

        return self._ledger.has_a_first_report_for_every_reader

    def reveal(self, labels: Mapping[str, str], *, nonce: bytes) -> GoldRevealRecord:
        """افتح الالتزامَ بجوابٍ وعشوائيّةٍ يُمرَّران الآن، بعد تمام التجميد."""

        binding = self._ledger.binding
        contract = binding.contract
        if not self.may_reveal:
            raise EvaluationError(
                NO_EVALUATION_VERDICT_BEFORE
                + "؛ والقرّاءُ بلا تقريرِ تشغيلٍ أوّل: "
                + "، ".join(self._ledger.missing_system_content_ids)
            )
        if self._ledger.violations:
            raise EvaluationError(
                "لا فتحَ مع مخالفةٍ مُسجَّلةٍ في التشغيل: "
                + "، ".join(self._ledger.violations)
            )
        for request in binding.requests:
            if request.contract_digest != contract.contract_digest:
                raise EvaluationError("طلبٌ مربوطٌ بعقدٍ غيرِ هذا العقد")
            if request.evaluation_protocol_digest != binding.protocol.protocol_digest:
                raise EvaluationError("طلبٌ مربوطٌ ببروتوكولٍ غيرِ هذا البروتوكول")
        if not contract.gold_commitment.opens_with(
            labels,
            nonce=nonce,
            contract_body_digest=contract.contract_body_digest,
        ):
            raise EvaluationError(
                "الجوابُ والعشوائيّةُ لا يفتحان الالتزامَ المُودَع؛ ولا يُفتَح "
                "بغير ما التُزِم به"
            )
        return GoldRevealRecord(
            contract_digest=contract.contract_digest,
            contract_body_digest=contract.contract_body_digest,
            commitment_digest=contract.gold_commitment.commitment_digest,
            evaluation_protocol_digest=binding.protocol.protocol_digest,
            binding_digest=binding.binding_digest,
            first_report_digests=tuple(
                (
                    content_id,
                    self._ledger.first_report(content_id).report_digest,
                )
                for content_id in binding.required_system_content_ids
            ),
            revealed_member_count=len(labels),
        )
