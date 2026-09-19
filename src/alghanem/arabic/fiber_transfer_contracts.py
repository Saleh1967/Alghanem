"""العقودُ الليفيّة: لا ينتقل حكمٌ بين مسارين إلّا بعقدٍ مكتوبٍ مفحوص.

نجاحُ اختبار الأدنويّة في `G0.FLT-1` **لا ينتقل تلقائيًّا** إلى
`G0.VV-BIRTH-1`، ولا يستكمل شهادةَ ولادة `CV`. فالمساران تجربتان مستقلّتان
بفرضيّاتٍ مُجمَّدةٍ لكلٍّ منهما، وما انعقد في إحداهما يبقى فيها حتّى يُكتَب
عقدُ انتقالٍ صريحٌ يُسمّي خمسةَ أشياء مجتمعةً
(`ASuccessfulMinimalityTestDoesNotCrossTracks`):

1. **الأصل**: المسارُ والمِرساةُ اللذان خرج منهما الحكم.
2. **الفرع**: المسارُ والمِرساةُ اللذان يدخلهما، وهما غيرُ الأصل.
3. **الهويّةُ المحفوظة**: ما يُدّعى بقاؤه عبر الانتقال، مُعدَّدًا بالاسم.
4. **الدليل**: مربوطًا بأصله نفسِه ببصمةٍ ونصِّ ما يشهد به.
5. **البقايا**: ما لم يُحمَل، مُسمّى لا مطويّ.

وثلاثةُ حدودٍ تُغلِق أبوابَ التسرّب:

**العقدُ لا يتركّب** (`ATransferDoesNotCompose`): عقدُ `أ → ب` وعقدُ `ب → ج`
لا يُنتِجان `أ → ج`. فكلُّ انتقالٍ يُكتَب ويُفحَص وحدَه، و`compose` موجودةٌ
لترفض لا لتصل.

**والدليلُ مربوطٌ بأصله** (`TheEvidenceIsBoundToItsOrigin`): دليلٌ يحمل مسارًا
أو مِرساةً غيرَ مسار العقد ومِرساته يُرَدّ عند الإنشاء، فلا يُستعار شاهدُ
تجربةٍ لتجربةٍ أخرى.

**وسجلٌّ خالٍ ليس نقضًا** (`AnEmptyLedgerIsNotARefutation`): خلوُّ السجلّ من
عقد `G0.FLT-1 → G0.VV-BIRTH-1` يعني أنّ الانتقالَ **غيرُ مُرخَّصٍ اليوم**، لا
أنّه مُبطَل. والفرقُ بين «لم يُكتَب» و«رُدَّ» فرقُ جنسٍ لا فرقُ درجة.

**وعقدُ الانتقال ليس شهادةَ ولادة**
(`ATransferContractIsNotABirthCertificate`): أقصى ما يفعله العقدُ نقلُ ما نُصَّ
عليه فيه؛ ولا تُصدَر منه شهادةُ ولادةٍ لـ`CV`، ولا حكمُ ولادةٍ كرنليّ، ولا
تجميدُ `E0`، ولا تُوصَل `BirthVerdictGate` بهذه الوحدة، ولا تستورد من
`kernel/` شيئًا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import is_canonical_digest

__all__ = [
    "AN_EMPTY_LEDGER_IS_NOT_A_REFUTATION_NOTE",
    "A_SUCCESSFUL_MINIMALITY_TEST_DOES_NOT_CROSS_TRACKS_NOTE",
    "A_TRANSFER_CONTRACT_IS_NOT_A_BIRTH_CERTIFICATE_NOTE",
    "A_TRANSFER_DOES_NOT_COMPOSE_NOTE",
    "CV_BIRTH_CERTIFICATE_STANDING",
    "FIBER_TRANSFER_LEDGER",
    "FIBER_TRANSFER_NAMED_RESIDUALS",
    "THE_EVIDENCE_IS_BOUND_TO_ITS_ORIGIN_NOTE",
    "THIS_MODULE_ISSUES_NO_BIRTH_VERDICT_NOTE",
    "CertificateStanding",
    "FiberTransferContract",
    "FiberTransferError",
    "TrackId",
    "TransferEvidence",
    "compose",
    "contract_for",
]


class FiberTransferError(ValueError):
    """رفضٌ صريحٌ في العقود الليفيّة: عقدٌ ناقصٌ، أو دليلٌ مُستعار، أو تركيب."""


class TrackId(Enum):
    """المساراتُ المُجمَّدةُ التي يجوز أن يقع بينها انتقال."""

    FLT1_QIYAS = "G0.FLT-1"
    VV_BIRTH = "G0.VV-BIRTH-1"


# --- الدليل، مربوطًا بأصله ------------------------------------------------------


@dataclass(frozen=True)
class TransferEvidence:
    """الدليلُ المحمولُ في العقد، ببصمتِه ونصِّ ما يشهد به."""

    origin_track: TrackId
    origin_anchor: str
    what_it_attests: str
    content_digest: str

    def __post_init__(self) -> None:
        if not self.origin_anchor.strip():
            raise FiberTransferError("الدليلُ بلا مِرساةِ أصلٍ مكتوبة")
        if not self.what_it_attests.strip():
            raise FiberTransferError("الدليلُ بلا نصٍّ يُسمّي ما يشهد به")
        if not is_canonical_digest(self.content_digest):
            raise FiberTransferError("الدليلُ بلا بصمةٍ قانونيّةِ الشكل")


# --- العقدُ نفسُه ---------------------------------------------------------------


@dataclass(frozen=True)
class FiberTransferContract:
    """عقدُ انتقالٍ واحدٌ بين مسارين، بأصله وفرعه وهويّته ودليله وبقاياه."""

    contract_id: str
    origin_track: TrackId
    origin_anchor: str
    branch_track: TrackId
    branch_anchor: str
    preserved_identity: tuple[str, ...]
    evidence: TransferEvidence
    licensed_conclusions: tuple[str, ...]
    what_it_does_not_license: tuple[str, ...]
    named_residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("contract_id", self.contract_id),
            ("origin_anchor", self.origin_anchor),
            ("branch_anchor", self.branch_anchor),
        ):
            if not value.strip():
                raise FiberTransferError(f"العقدُ بلا «{field_name}» مكتوب")
        if self.origin_track is self.branch_track:
            raise FiberTransferError(
                "عقدُ الانتقال يعبر مسارين متمايزين؛ والأصلُ ههنا هو الفرعُ نفسُه"
            )
        if self.origin_anchor == self.branch_anchor:
            raise FiberTransferError("مِرساةُ الفرع هي مِرساةُ الأصل نفسُها")
        _require_named("preserved_identity", self.preserved_identity)
        _require_named("licensed_conclusions", self.licensed_conclusions)
        _require_named("what_it_does_not_license", self.what_it_does_not_license)
        _require_named("named_residuals", self.named_residuals)
        overlap = set(self.licensed_conclusions) & set(self.what_it_does_not_license)
        if overlap:
            raise FiberTransferError(
                "نتيجةٌ واحدةٌ مُرخَّصةٌ وممنوعةٌ معًا: " + "، ".join(sorted(overlap))
            )
        if (
            self.evidence.origin_track is not self.origin_track
            or self.evidence.origin_anchor != self.origin_anchor
        ):
            raise FiberTransferError(
                "الدليلُ ليس دليلَ أصلِ هذا العقد " "(TheEvidenceIsBoundToItsOrigin)"
            )

    def licenses(self, conclusion: str) -> bool:
        """أتُرخِّص هذه العقدُ هذه النتيجةَ بعينها؟ مطابقةً نصّيّةً لا استلزامًا."""

        return conclusion in self.licensed_conclusions


def _require_named(field_name: str, values: tuple[str, ...]) -> None:
    if not values:
        raise FiberTransferError(f"العقدُ بلا «{field_name}»؛ والخلوُّ ليس إعفاءً")
    if any(not value.strip() for value in values):
        raise FiberTransferError(f"«{field_name}» فيه مدخلٌ فارغ")
    if len(set(values)) != len(values):
        raise FiberTransferError(f"«{field_name}» فيه تكرار")


def compose(
    first: FiberTransferContract, second: FiberTransferContract
) -> FiberTransferContract:
    """لا تُركَّب العقود؛ هذه الدالّةُ ترفض دائمًا وتُسمّي سببَ رفضها."""

    raise FiberTransferError(
        "ATransferDoesNotCompose: "
        f"عقدُ «{first.contract_id}» وعقدُ «{second.contract_id}» لا يُنتِجان "
        "عقدًا ثالثًا؛ وكلُّ انتقالٍ يُكتَب ويُفحَص وحدَه"
    )


def contract_for(
    origin: TrackId,
    branch: TrackId,
    ledger: tuple[FiberTransferContract, ...] | None = None,
) -> FiberTransferContract:
    """عقدُ الانتقال المكتوبُ بين مسارين، أو رفضٌ مُسمّى إن لم يُكتَب بعد."""

    written = FIBER_TRANSFER_LEDGER if ledger is None else ledger
    for contract in written:
        if contract.origin_track is origin and contract.branch_track is branch:
            return contract
    raise FiberTransferError(
        "AnEmptyLedgerIsNotARefutation: لا عقدَ مكتوبًا من "
        f"«{origin.value}» إلى «{branch.value}»؛ فالانتقالُ غيرُ مُرخَّصٍ اليوم "
        "ولا هو مُبطَل"
    )


# --- شهادةُ ولادة CV، وما ينقصها -------------------------------------------------


@dataclass(frozen=True)
class CertificateStanding:
    """حالُ شهادةٍ: صادرةٌ بلا نقصٍ، أو غيرُ صادرةٍ بنقصٍ مُعدَّدٍ بالاسم."""

    certificate_id: str
    issued: bool
    what_is_still_missing: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.certificate_id.strip():
            raise FiberTransferError("الشهادةُ بلا مُعرِّفٍ مكتوب")
        if self.issued and self.what_is_still_missing:
            raise FiberTransferError("شهادةٌ صادرةٌ ويُعدَّد لها نقص")
        if not self.issued and not self.what_is_still_missing:
            raise FiberTransferError("شهادةٌ غيرُ صادرةٍ بلا سببٍ مكتوبٍ لتخلّفها")
        if any(not item.strip() for item in self.what_is_still_missing):
            raise FiberTransferError("في نقص الشهادة مدخلٌ فارغ")


FIBER_TRANSFER_LEDGER: Final[tuple[FiberTransferContract, ...]] = ()
"""سجلُّ العقود المكتوبة؛ وهو خالٍ اليوم، وخلوُّه مقروءٌ لا مطويّ."""


CV_BIRTH_CERTIFICATE_STANDING: Final[CertificateStanding] = CertificateStanding(
    certificate_id="CV.birth",
    issued=False,
    what_is_still_missing=(
        "هدفُ إعادة بناءٍ مستقلٌّ عن القارئ المُرخَّص، فبدونه تبقى أدنويّةُ "
        "G0.FLT-1 غيرَ بالغةٍ منزلةَ BORN",
        "عقدُ انتقالٍ مكتوبٌ من G0.FLT-1 إلى G0.VV-BIRTH-1 يُسمّي أصلَه وفرعَه "
        "وهويّتَه المحفوظة ودليلَه وبقاياه",
        "قراءةُ G0.VV-BIRTH-1 نفسُها، ولا وجودَ لها في هذه الشجرة بعد",
        "حكمُ ولادةٍ كرنليٌّ من بوّابته، وهو خارجُ سلطة هذه الطبقة بحال",
    ),
)
"""شهادةُ ولادة `CV`: غيرُ صادرةٍ، وما ينقصها مُعدَّدٌ لا مُجمَل."""


# --- الحدودُ مُسمّاةً -------------------------------------------------------------


A_SUCCESSFUL_MINIMALITY_TEST_DOES_NOT_CROSS_TRACKS_NOTE: Final[str] = (
    "ASuccessfulMinimalityTestDoesNotCrossTracks: انعقادُ الأدنويّة في "
    "G0.FLT-1 حكمٌ في مساره؛ ولا يبلغ G0.VV-BIRTH-1 إلّا بعقدٍ يُسمّي الأصلَ "
    "والفرعَ والهويّةَ المحفوظةَ والدليلَ والبقايا"
)

A_TRANSFER_DOES_NOT_COMPOSE_NOTE: Final[str] = (
    "ATransferDoesNotCompose: عقدان متتابعان لا يُنتِجان ثالثًا، و`compose` "
    "ترفض دائمًا؛ فالتركيبُ طريقٌ خفيٌّ إلى انتقالٍ لم يُفحَص"
)

THE_EVIDENCE_IS_BOUND_TO_ITS_ORIGIN_NOTE: Final[str] = (
    "TheEvidenceIsBoundToItsOrigin: دليلٌ يحمل مسارًا أو مِرساةً غيرَ مسار "
    "العقد ومِرساته يُرَدّ عند الإنشاء، فلا يُستعار شاهدُ تجربةٍ لأخرى"
)

AN_EMPTY_LEDGER_IS_NOT_A_REFUTATION_NOTE: Final[str] = (
    "AnEmptyLedgerIsNotARefutation: خلوُّ السجلّ يعني أنّ الانتقالَ غيرُ "
    "مُرخَّصٍ اليوم لا أنّه مُبطَل؛ والغيابُ ليس نقضًا"
)

A_TRANSFER_CONTRACT_IS_NOT_A_BIRTH_CERTIFICATE_NOTE: Final[str] = (
    "ATransferContractIsNotABirthCertificate: أقصى ما ينقله العقدُ ما نُصَّ "
    "عليه فيه، ولا تُستكمَل به شهادةُ ولادة CV ولا يُصدَر عنه حكمُ ولادة"
)

THIS_MODULE_ISSUES_NO_BIRTH_VERDICT_NOTE: Final[str] = (
    "ThisModuleIssuesNoBirthVerdict: لا حكمَ ولادةٍ كرنليًّا هنا، ولا تجميدَ "
    "E0، ولا وصلَ لـBirthVerdictGate، ولا استيرادَ من kernel/"
)

FIBER_TRANSFER_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_SUCCESSFUL_MINIMALITY_TEST_DOES_NOT_CROSS_TRACKS_NOTE,
    A_TRANSFER_DOES_NOT_COMPOSE_NOTE,
    THE_EVIDENCE_IS_BOUND_TO_ITS_ORIGIN_NOTE,
    AN_EMPTY_LEDGER_IS_NOT_A_REFUTATION_NOTE,
    A_TRANSFER_CONTRACT_IS_NOT_A_BIRTH_CERTIFICATE_NOTE,
    THIS_MODULE_ISSUES_NO_BIRTH_VERDICT_NOTE,
)
