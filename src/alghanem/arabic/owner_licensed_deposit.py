"""إيداعٌ بتفويضٍ موقَّع: بايتاتٌ مختومةٌ، وتوقيعٌ لا يُقرأ ختمًا.

وصلت إلى هذه الشجرة مادّتان لم تكونا فيها: متنُ الجزء الثالث من «الشخصية
الإسلامية»، و«سرعة البديهة». وكانتا قبل اليومِ **مذكورتَين لا مُودَعتَين**،
فكلُّ ما قيل عنهما كان مُسجَّلًا لا قابلًا لإعادة الاشتقاق. وقد فوَّض مالكُ
المستودعَين نقلَهما بنصٍّ منقولٍ بحروفه في `exhibits/owner-authorisation/`،
فنُقلت البايتاتُ وخُتمت. وهذه الوحدةُ تحرس ثلاثةَ فروقٍ لا يجوز طيُّها:

**أوّلًا: التوقيعُ إقرارٌ، والختمُ قياس.** التفويضُ نصٌّ يقوله إنسان، ولا
يُشتَقُّ منه شيء؛ والختمُ `sha256` يُعاد اشتقاقُه من القرص عند كلّ نداء
فيوافق أو ينزاح. فلو وُقِّع على ملفٍّ ثمّ تبدَّلت بايتاتُه، لبقي التوقيعُ
صحيحًا بوصفه إقرارًا وسقط الختمُ بوصفه قياسًا — ولا يستر أحدُهما الآخر
(`A_SIGNATURE_IS_A_DECLARATION_NOT_A_MEASUREMENT`).

**وثانيًا: إذنُ المالكِ يُرخِّص النسخَ لا المصنَّف.** المُفوِّضُ مالكُ
المستودع الذي أُخذت منه البايتات، وليس مصنِّفَ الكتاب: المؤلّفُ تقي الدين
النبهاني. فالمأذونُ فيه نقلُ نسخةٍ من مودَعٍ إلى مودَع، وليس المأذونُ فيه
رخصةَ المصنَّف؛ وخلطُ الاثنين يُخرِج من إذنِ نقلٍ حقًّا لا يملكه المُفوِّض
(`AN_OWNERS_AUTHORISATION_LICENSES_THE_COPY_NOT_THE_WORK`).

**وثالثًا: المضغوطُ يُختَم ولا يُقرأ.** «سرعة البديهة» مُودَعٌ بصيغة
`docx`، وهي أرشيفٌ مضغوط. فبايتاتُه تُختَم كما تُختَم أيُّ بايتات، وأمّا
نصُّه فلا يُبلَغ إلّا بقاعدةِ استخراجٍ — فكُّ الضغط، ثمّ انتقاءُ عُقَدٍ من
`document.xml` — وهذه القاعدةُ **غيرُ مُرخَّصةٍ ههنا**، فلا يُقرأ من هذا
الملفّ رقمٌ نصّيٌّ ألبتّة. وأوّلُ من سقط في هذا البابِ قارئٌ انتقى
`<w:t[^>]*>` فابتلع `<w:tab .../>` معها، فانتفخ عدُّ المحارف بنحو الثلث:
فالقاعدةُ التي تبدو بديهيّةً ليست بديهيّة، وتركُها غيرَ مُرخَّصةٍ أصدقُ من
تمريرها صامتة (`COMPRESSED_BYTES_ARE_SEALED_BUT_NOT_READ`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادة، ولا استيرادَ من `kernel/`،
ولا بوّابةَ تقرأ هذا الإيداعَ حكمًا على مادّةٍ عربيّة. وما ههنا إلّا: أهذه
البايتاتُ هي التي وُقِّع عليها، أم انزاحت؟
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from pathlib import Path
from typing import Any, Final

__all__ = [
    "AN_OWNERS_AUTHORISATION_LICENSES_THE_COPY_NOT_THE_WORK",
    "A_SIGNATURE_IS_A_DECLARATION_NOT_A_MEASUREMENT",
    "COMPRESSED_BYTES_ARE_SEALED_BUT_NOT_READ",
    "DepositGenus",
    "DepositStanding",
    "MeasuredSeal",
    "OwnerLicensedDepositError",
    "THE_AUTHORISATION_FILE",
    "THE_DEPOSITS",
    "SealedDeposit",
    "authorisation_signature",
    "drifted_deposits",
    "measure",
    "read_authorisation",
    "standing_of",
    "unsigned_deposits",
]


class OwnerLicensedDepositError(ValueError):
    """رفضٌ مُسمًّى في هذا الإيداع؛ ولا يُبتلَع خللٌ ههنا صمتًا."""


A_SIGNATURE_IS_A_DECLARATION_NOT_A_MEASUREMENT: Final[str] = (
    "التوقيعُ إقرارُ إنسانٍ لا يُشتَقُّ منه رقم، والختمُ قياسٌ يُعاد اشتقاقُه "
    "من القرص. فلا يُصحِّح توقيعٌ ختمًا منزاحًا، ولا يُسقِط انزياحُ ختمٍ "
    "صدقَ التوقيع بوصفه إقرارًا: هما جنسان، ويُعرَضان معًا ولا يُدمَجان."
)

AN_OWNERS_AUTHORISATION_LICENSES_THE_COPY_NOT_THE_WORK: Final[str] = (
    "المُفوِّضُ مالكُ المستودع المنقول منه، لا مصنِّفُ الكتاب. فالمأذونُ فيه "
    "نقلُ نسخةٍ وختمُها، وليس المأذونُ فيه رخصةَ المصنَّف؛ ومن قرأ إذنَ "
    "النقلِ رخصةً للمصنَّف فقد أخرج من المُفوِّضِ حقًّا لا يملكه."
)

COMPRESSED_BYTES_ARE_SEALED_BUT_NOT_READ: Final[str] = (
    "المضغوطُ تُختَم بايتاتُه ولا يُقرأ نصُّه: بلوغُ النصّ يفتقر إلى قاعدةِ "
    "استخراجٍ مُرخَّصة، وهي غيرُ موضوعةٍ ههنا. فلا يخرج من ملفٍّ مضغوطٍ في "
    "هذه الوحدة رقمٌ نصّيٌّ واحد، ويبقى الوقوفُ عند البايتات مُعلَنًا."
)

THE_AUTHORISATION_FILE: Final[str] = (
    "exhibits/owner-authorisation/authorisation.json"
)


class DepositGenus(Enum):
    """أنصُّ مسطَّحٌ تُقرأ محارفُه، أم مضغوطٌ تُختَم بايتاتُه وحدَها؟"""

    PLAIN_TEXT_READABLE = "نصٌّ مسطَّحٌ مقروء"
    COMPRESSED_NOT_READ = "مضغوطٌ مختومٌ غيرُ مقروء"


class DepositStanding(Enum):
    """مصيرُ الوديعة، مشتقٌّ من القرص والتفويض معًا لا مكتوبٌ في حقل."""

    SIGNED_AND_SEALED = "موقَّعٌ ومختومٌ موافق"
    SEALED_BUT_DRIFTED = "منزاحٌ عن ختمه"
    PRESENT_BUT_UNSIGNED = "حاضرٌ بلا تفويض"
    ABSENT = "غائبُ البايتات"


@dataclass(frozen=True)
class SealedDeposit:
    """وديعةٌ منقولٌ ختمُها إلى النثر، ليُصادَم بما يولِّده القرصُ الآن."""

    name: str
    path: str
    transcribed_sha256: str
    transcribed_bytes: int
    genus: DepositGenus
    source: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise OwnerLicensedDepositError("وديعةٌ بلا اسمٍ لا تُختَم.")
        if len(self.transcribed_sha256) != 64:
            raise OwnerLicensedDepositError(
                f"ختمُ «{self.name}» ليس بصمةَ sha256 كاملة."
            )
        if self.transcribed_bytes <= 0:
            raise OwnerLicensedDepositError(
                f"وديعةٌ بحجمٍ غيرِ موجبٍ «{self.name}» لا تُقرأ."
            )


@dataclass(frozen=True)
class MeasuredSeal:
    """ما ولَّده القرصُ الآن لوديعةٍ بعينها."""

    present: bool
    measured_sha256: str
    measured_bytes: int


THE_DEPOSITS: Final[tuple[SealedDeposit, ...]] = (
    SealedDeposit(
        name="الشخصية الإسلامية · الجزء الثالث · المتن",
        path="corpora/shakhsiyya-j3-matn.txt",
        transcribed_sha256=(
            "520b8e9d55135217d2c07bf521a63ed93431d46bd5cdf16f360c915d8bbfc783"
        ),
        transcribed_bytes=1_241_712,
        genus=DepositGenus.PLAIN_TEXT_READABLE,
        source="hamil-hala-zaman-program/shakhsiyya_j3_matn.txt",
    ),
    SealedDeposit(
        name="سرعة البديهة",
        path="corpora/surat-al-badiha.docx",
        transcribed_sha256=(
            "483cf19f6153cfb31bb6d965e1b7da6927f330633b49c586360f3567798bc161"
        ),
        transcribed_bytes=74_472,
        genus=DepositGenus.COMPRESSED_NOT_READ,
        source="hamil-hala-zaman-program/سرعة البديهة.docx",
    ),
)


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def measure(deposit: SealedDeposit) -> MeasuredSeal:
    """يُعاد اشتقاقُ الختم من البايتات عند كلّ نداء؛ ولا يُخزَّن."""

    on_disk = _repository_root() / deposit.path
    if not on_disk.is_file():
        return MeasuredSeal(present=False, measured_sha256="", measured_bytes=0)
    payload = on_disk.read_bytes()
    return MeasuredSeal(
        present=True,
        measured_sha256=sha256(payload).hexdigest(),
        measured_bytes=len(payload),
    )


def read_authorisation() -> dict[str, Any]:
    """يُفتَح التفويضُ المُودَع ويُقرأ، ولا يُنسَخ نصُّه إلى هذا الملفّ."""

    on_disk = _repository_root() / THE_AUTHORISATION_FILE
    if not on_disk.is_file():
        raise OwnerLicensedDepositError(
            f"التفويضُ غائبٌ عن {THE_AUTHORISATION_FILE}، فلا إيداعَ مأذونًا."
        )
    document = json.loads(on_disk.read_text(encoding="utf-8"))
    body = document.get("تفويضُ_المالك")
    if not isinstance(body, dict):
        raise OwnerLicensedDepositError("التفويضُ المُودَع بلا متنٍ مُسمًّى.")
    return body


def authorisation_signature() -> str:
    """نصُّ التوقيع كما نُقل بحروفه؛ إقرارٌ يُعرَض ولا يُشتَقُّ منه رقم."""

    signature = read_authorisation().get("نصُّ_التفويض", "")
    if not isinstance(signature, str) or not signature.strip():
        raise OwnerLicensedDepositError("تفويضٌ بلا نصِّ توقيعٍ لا يُقرأ إذنًا.")
    return signature


def _signed_paths() -> frozenset[str]:
    entries = read_authorisation().get("المودَعُ_بهذا_التفويض", [])
    if not isinstance(entries, list):
        raise OwnerLicensedDepositError("قائمةُ المودَع في التفويض ليست قائمة.")
    return frozenset(
        str(entry.get("مسار", "")) for entry in entries if isinstance(entry, dict)
    )


def unsigned_deposits() -> tuple[SealedDeposit, ...]:
    """ودائعُ حاضرةٌ في النثر لم يُسمِّها التفويضُ المُودَع؛ ولا تُقرأ مأذونة."""

    signed = _signed_paths()
    return tuple(one for one in THE_DEPOSITS if one.path not in signed)


def standing_of(deposit: SealedDeposit) -> DepositStanding:
    """مصيرٌ واحدٌ من أربعةٍ، مشتقٌّ من القرص والتفويض، لا مكتوبٌ في حقل."""

    reading = measure(deposit)
    if not reading.present:
        return DepositStanding.ABSENT
    if (
        reading.measured_sha256 != deposit.transcribed_sha256
        or reading.measured_bytes != deposit.transcribed_bytes
    ):
        return DepositStanding.SEALED_BUT_DRIFTED
    if deposit.path not in _signed_paths():
        return DepositStanding.PRESENT_BUT_UNSIGNED
    return DepositStanding.SIGNED_AND_SEALED


def drifted_deposits() -> tuple[SealedDeposit, ...]:
    """كلُّ وديعةٍ لا يوافق قرصُها ما نُقل عنها؛ والفراغُ حكمٌ لا وعد."""

    return tuple(
        one
        for one in THE_DEPOSITS
        if standing_of(one)
        in (DepositStanding.SEALED_BUT_DRIFTED, DepositStanding.ABSENT)
    )
