"""سجلُّ إيداعٍ مؤرَّخٌ مسلسلُ البصمات، يُعاد اشتقاقُه كلَّه عند القراءة.

قيل في تدقيق «الجبر المولِّد المغلق» إنّ شرطًا من شروطه لا تُثبته البصماتُ
ألبتّة: «بندُ المتوقَّع معلنٌ **قبل** التشغيل». فبصمةُ الملفّ تشهد بما كُتب
ولا تشهد بمتى كُتب. وهذا الإيداعُ جوابُ ذاك النقص على قدرِه لا فوقَه.

**أوّلًا: ما تحرسه السلسلةُ ترتيبٌ لا زمنٌ مطلق.** كلُّ حلقةٍ تأخذ بصمةَ
سالفتها في مادّتها، فمن بدَّل حلقةً أو قدَّم واحدةً على أخرى انقطعت البصماتُ
بعدها كلُّها. فهذا يمنع إقحامَ بندٍ بأثرٍ رجعيّ في وسط السجلّ. وأمّا أن
يكون الختمُ الزمنيُّ المكتوب هو زمنَ الكتابة حقًّا فلا يشهد به الملفّ:
شاهدُه خارجَ الملفّ — تاريخُ الإيداع في git. وتُعلَن هذه الحدودُ ولا تُخفى
(`THE_CHAIN_ORDERS_THE_LINKS_AND_GIT_DATES_THEM`).

**وثانيًا: سبقُ الإعلان لا ينفع في البرهان الصوريّ ولا يضرّ.** فعددُ
السلاسل الناجية على حقلٍ مرخَّصٍ عددٌ يُعاد اشتقاقُه متى شئت، لا يزيده
تقديمُ الإعلان صدقًا ولا يُنقصه تأخيرُه. فما كان من هذا الجنس يُصنَّف
`برهانٌ_صوريّ`، ويُصادَم ههنا بحسابٍ **يُنفَّذ الآن** لا بنقلٍ مُطابَق
(`PREREGISTRATION_IS_INERT_ON_WHAT_A_MACHINE_CAN_REDERIVE`).

**وثالثًا: وينفع سبقُ الإعلان حيث المادّةُ غائبة.** فأعدادُ تلك الرسالة
المقيسةُ على مدوّنتها (`mujammad.norm.txt`) ليست في هذه الشجرة، ولا يُمكن
قياسُها ههنا اليومَ ألبتّة. فتُودَع بندًا متوقَّعًا مختومًا **قبل** وصول
بايتات مقامها، فإذا وصلت يومًا كان الصِدامُ صِدامَ متوقَّعٍ سابقٍ بمقيسٍ
لاحق، لا تفصيلَ توقُّعٍ على مقيسٍ رآه صاحبُه. وحكمُ هذه الحلقات اليومَ
`لم_تصل_مادّتُه` — وهو **ليس موافقةً ولا مناقضة**
(`AN_UNMEASURED_EXPECTATION_IS_NOT_A_CONFIRMED_ONE`).

**ورابعًا: والمناقضةُ تُودَع مناقضةً.** أعلنت تلك الرسالةُ على شهادةٍ
واحدةٍ وأساسٍ واحدٍ عددَين مختلفَين لالتقاء الساكنين في الخام. فلا يُختار
أحدُهما ههنا ولا يُمحى الآخر: يُودَعان معًا موسومَين، ويُقرأ حكمُهما
`طرفان_متناقضان_لا_يُرفَعان_ههنا` لأنّ رفعَهما يحتاج بايتاتِ شهادتهم وهي
غائبة.

**خمولٌ سلطويّ**: لا ولادةَ ههنا ولا حكمَ ولادة، ولا استيرادَ من `kernel/`
ولا من `program/`، ولا قراءةَ لمدوّنةٍ من `corpora/`، ولا بوّابةَ في هذه
الشجرة تُصدِّق عددًا عربيًّا بهذا السجلّ. وما فيه من أعداد أجنبيّة نقلٌ
موسومٌ لا يُضاف إلى عددٍ من أعداد الشجرة ولا يُطرَح منه.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from itertools import product
from pathlib import Path
from typing import Any, Final

__all__ = [
    "AN_UNMEASURED_EXPECTATION_IS_NOT_A_CONFIRMED_ONE",
    "LICENSED_STATE_COUNT",
    "PREREGISTRATION_IS_INERT_ON_WHAT_A_MACHINE_CAN_REDERIVE",
    "ROOT_DIGEST",
    "SILENT_STATE_COUNT",
    "STATE_COUNT",
    "THE_CHAIN_ORDERS_THE_LINKS_AND_GIT_DATES_THEM",
    "THE_CONSONANT_COUNT",
    "LedgerLink",
    "LinkGenus",
    "LinkStanding",
    "cell_digests",
    "chain_is_unbroken",
    "extras_count_forcing",
    "folded_digests",
    "ledger_path",
    "read_deposited_ledger",
    "recomputed_link_digests",
    "standing_of",
    "standings",
    "surviving_chains",
]

THE_CHAIN_ORDERS_THE_LINKS_AND_GIT_DATES_THEM: Final[str] = (
    "بصمةُ السلف تمنع إقحامَ حلقةٍ أو تقديمَها، ولا تشهد بالزمن المطلق؛ "
    "شاهدُ الزمن تاريخُ الإيداع في git لا حقلٌ في الملفّ."
)

PREREGISTRATION_IS_INERT_ON_WHAT_A_MACHINE_CAN_REDERIVE: Final[str] = (
    "ما يُعاد اشتقاقُه بالحساب لا يزيده سبقُ الإعلان صدقًا؛ فيُصادَم بتنفيذٍ "
    "الآنَ لا بمطابقةِ نقل."
)

AN_UNMEASURED_EXPECTATION_IS_NOT_A_CONFIRMED_ONE: Final[str] = (
    "بندٌ مختومٌ لم تصل مادّةُ قياسه ليس موافقةً ولا مناقضة؛ وعدُّه موافقةً "
    "تبييضٌ، وعدُّه مناقضةً محاكمةٌ بلا بيّنة."
)

ROOT_DIGEST: Final[str] = "0" * 64

THE_CONSONANT_COUNT: Final[int] = 28
STATE_COUNT: Final[int] = 8
LICENSED_STATE_COUNT: Final[int] = 4
SILENT_STATE_COUNT: Final[int] = 1


class LinkGenus(Enum):
    """جنسُ الحلقة، مقروءًا من البايتات لا مُفترَضًا."""

    FORMAL = "برهانٌ_صوريّ"
    AWAITING_ITS_MATERIAL = "بندٌ_متوقَّعٌ_ينتظر_مادّتَه"
    DECLARED_CLASH = "مناقضةٌ_معلَنة"


class LinkStanding(Enum):
    """حكمُ الحلقة، مشتقٌّ عند القراءة ولا يُكتَب في حقل."""

    REDERIVED_AND_AGREES = "أُعيد_اشتقاقُه_فوافق"
    REDERIVED_AND_DIFFERS = "أُعيد_اشتقاقُه_فخالف"
    ITS_MATERIAL_HAS_NOT_ARRIVED = "لم_تصل_مادّتُه"
    TWO_SIDES_NOT_LIFTED_HERE = "طرفان_متناقضان_لا_يُرفَعان_ههنا"


@dataclass(frozen=True)
class LedgerLink:
    """حلقةٌ من السجلّ كما هي على القرص، بلا حقلِ حكم."""

    rank: int
    name: str
    stamp: str
    genus: LinkGenus
    payload: dict[str, Any]
    payload_digest: str
    previous_digest: str
    link_digest: str


def _canonical(payload: object) -> str:
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ledger_path() -> Path:
    """مسارُ البايتات المُودَعة."""

    root = Path(__file__).resolve().parents[3]
    return root / "exhibits" / "tawlid-algebra" / "ledger.json"


def read_deposited_ledger() -> tuple[LedgerLink, ...]:
    """يُفتَح الملفُّ في كلّ نداءٍ فتُقرأ الحلقاتُ من بايتاتها."""

    document = json.loads(ledger_path().read_text(encoding="utf-8"))
    return tuple(
        LedgerLink(
            rank=int(entry["الرتبة"]),
            name=str(entry["الاسم"]),
            stamp=str(entry["الختم_الزمني"]),
            genus=LinkGenus(entry["الصنف"]),
            payload=dict(entry["الحمولة"]),
            payload_digest=str(entry["بصمة_الحمولة"]),
            previous_digest=str(entry["بصمة_السلف"]),
            link_digest=str(entry["بصمة_الحلقة"]),
        )
        for entry in document["الحلقات"]
    )


def recomputed_link_digests() -> tuple[str, ...]:
    """تُعاد السلسلةُ حسابًا من الجذر، فلا تُصدَّق بصمةٌ مكتوبة."""

    digests: list[str] = []
    previous = ROOT_DIGEST
    for link in read_deposited_ledger():
        body = _canonical(link.payload)
        material = f"{previous}|{link.stamp}|{link.name}|{link.genus.value}|{body}"
        previous = _digest(material)
        digests.append(previous)
    return tuple(digests)


def chain_is_unbroken() -> bool:
    """أتُطابق البصماتُ المكتوبةُ ما يُعيده الحسابُ حلقةً حلقة؟"""

    links = read_deposited_ledger()
    if tuple(link.link_digest for link in links) != recomputed_link_digests():
        return False
    if any(link.rank != index for index, link in enumerate(links)):
        return False
    previous = ROOT_DIGEST
    for link in links:
        if link.previous_digest != previous:
            return False
        if link.payload_digest != _digest(_canonical(link.payload)):
            return False
        previous = link.link_digest
    return True


def extras_count_forcing(target: int) -> int | None:
    """كم زائدًا يُوجِبه مقدارُ `C \\ H`؟ يُحَلُّ القيدُ ولا يُخمَّن."""

    remainder = target - THE_CONSONANT_COUNT * LICENSED_STATE_COUNT
    if remainder < 0 or remainder % STATE_COUNT:
        return None
    return remainder // STATE_COUNT


def _cells() -> tuple[tuple[int, int], ...]:
    return tuple(
        (letter, state)
        for letter in range(THE_CONSONANT_COUNT)
        for state in range(LICENSED_STATE_COUNT)
    )


def _is_silent(cell: tuple[int, int]) -> bool:
    return cell[1] == LICENSED_STATE_COUNT - SILENT_STATE_COUNT


def surviving_chains(length: int) -> int:
    """عدُّ السلاسل التي لا يتجاور فيها ساكنان، بالتكرار المشتقّ من الحقل."""

    if length < 1:
        raise ValueError("طولُ السلسلة لا يقلُّ عن واحد")
    cells = _cells()
    moving = sum(1 for cell in cells if not _is_silent(cell))
    silent = len(cells) - moving
    ending_moving, ending_silent = moving, silent
    for _ in range(length - 1):
        ending_moving, ending_silent = (
            moving * (ending_moving + ending_silent),
            silent * ending_moving,
        )
    return ending_moving + ending_silent


def surviving_chains_by_enumeration(length: int) -> int:
    """العدُّ نفسُه استقصاءً تامًّا، تنفيذٌ ثانٍ مستقلٌّ عن التكرار."""

    cells = _cells()
    return sum(
        1
        for chain in product(cells, repeat=length)
        if not any(
            _is_silent(chain[index]) and _is_silent(chain[index + 1])
            for index in range(length - 1)
        )
    )


def cell_digests() -> tuple[str, ...]:
    """بصمةُ كلّ خليّةٍ من خلايا الحقل المرخَّص."""

    return tuple(_digest(f"{letter}:{state}") for letter, state in _cells())


def folded_digests() -> tuple[str, ...]:
    """بصمةُ كلّ زوجٍ ناجٍ بعد طيِّه، ليُقاس تفرُّدُها لا ليُفترَض."""

    cells = _cells()
    return tuple(
        _digest(f"{first[0]}:{first[1]}>{second[0]}:{second[1]}")
        for first in cells
        for second in cells
        if not (_is_silent(first) and _is_silent(second))
    )


def _formal_standing(link: LedgerLink) -> LinkStanding:
    generator = str(link.payload.get("المولّد", ""))
    if generator == "extras_count_forcing":
        # المقامُ مُعلَنٌ في الحمولة، فلا يُشتقُّ من الجواب فيُصدِّقَ نفسَه.
        measured = extras_count_forcing(int(link.payload["المقام_المطلوب"]))
        agrees = measured == link.payload["الجذر_الوحيد"]
    elif generator == "surviving_chains":
        length = int(link.payload["الطول"])
        measured = surviving_chains(length)
        agrees = measured == link.payload["العدد"]
        if agrees and length <= 3:
            agrees = surviving_chains_by_enumeration(length) == link.payload["العدد"]
    elif generator == "cell_digests":
        agrees = len(set(cell_digests())) == link.payload["البصمات_الفريدة"]
    elif generator == "folded_digests":
        agrees = len(set(folded_digests())) == link.payload["البصمات_الفريدة"]
    else:
        raise ValueError(f"حلقةٌ صوريّةٌ بلا مولِّدٍ معروف: {link.name}")
    return (
        LinkStanding.REDERIVED_AND_AGREES
        if agrees
        else LinkStanding.REDERIVED_AND_DIFFERS
    )


def standing_of(link: LedgerLink) -> LinkStanding:
    """حكمُ الحلقة، يُشتَقُّ الآنَ من جنسها وحسابها لا من حقلٍ مكتوب."""

    if link.genus is LinkGenus.FORMAL:
        return _formal_standing(link)
    if link.genus is LinkGenus.AWAITING_ITS_MATERIAL:
        return LinkStanding.ITS_MATERIAL_HAS_NOT_ARRIVED
    return LinkStanding.TWO_SIDES_NOT_LIFTED_HERE


def standings() -> tuple[tuple[LedgerLink, LinkStanding], ...]:
    """السجلُّ كلُّه مقروءًا بأحكامه المشتقّة."""

    return tuple((link, standing_of(link)) for link in read_deposited_ledger())
