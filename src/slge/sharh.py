"""عقدُ الشرح: لكلّ صورةٍ أسطرٌ (الدعوى، القيمة، الوحدة) من أثر السُّلَّم، ووسمُ كلّ سطرٍ ومرساتُه من سجلّ
الدعاوى (`status.LEDGER`) لا من هنا — فلا سطرَ أقوى من سنده.

لا نصَّ في العقد: القيمُ أعدادٌ وحواملُ وأسماءٌ من مفرداتٍ مغلقة (أبوابُ السوابق، قواعدُ الإعلال، أصنافُ
الوجود، الحالات)، والجملةُ تُبنى خارج الشجرة بعد أن تخرج الكلمةُ بـ`gate.exit` (الغانم
`tools/gen_sharh_text.py`). والفحصُ الآليّ `breaches`: دعوى ليست في السجلّ
(`SHARH_CLAIM_NOT_IN_LEDGER`)، وحدةٌ خارج المفردات (`SHARH_UNIT_NOT_IN_VOCABULARY`)، ودعوى معلَّقةٌ في
السجلّ (`SHARH_CLAIM_SUSPENDED`).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import Cell, fold, licensed
from slge.hukm import judge_root
from slge.ilal import RULES
from slge.madd import continue_licensed
from slge.maqayis import attested, code_of_root, roots_of
from slge.qiraa import harf, hukm_readings, qiraa
from slge.qiraa import rank as rank_qiraa
from slge.sawabiq import sawabiq
from slge.status import LEDGER, Status
from slge.tawabi import case_class
from slge.tawzi import tawzi
from slge.wujud import ont_of_reading

__all__ = ["UNITS", "Line", "anchor", "breaches", "lines", "tag"]

Word = tuple[Cell, ...]
Value = int | str | bool | tuple[int | str | bool, ...]
UNITS: Final[tuple[str, ...]] = ("خانة", "حكم", "عدد", "باب", "قراءة", "جذر", "قاعدة", "مرتبة",
                                 "حالة", "صنف")
"""الوحداتُ المغلقة: ما يُعدّ في السطر."""
_BY_ID: Final = {c.claim_id: c for c in LEDGER}


@dataclass(frozen=True, slots=True)
class Line:
    """سطرُ العقد: الدعوى (معرّفُها في السجلّ)، القيمة، الوحدة."""

    claim: str
    value: Value
    unit: str


def tag(line: Line) -> str:
    """وسمُ السطر: وسمُ دعواه في السجلّ بعينه."""

    return _BY_ID[line.claim].status.name


def anchor(line: Line) -> str:
    """مرساةُ السطر: أوّلُ سندِ دعواه في السجلّ (مبرهنةٌ مدقَّقة أو اختبارٌ باسمه)."""

    return _BY_ID[line.claim].support[0]


def lines(w: Word, cert: tuple[int, int] | None = None) -> tuple[Line, ...]:
    """أسطرُ الصورة بترتيب السُّلَّم: الخانات، عددُ الشهادة (إن حُمل: العددُ ورتبتُه في الليف)،
    الترخيص، الطيّ، الموزِّع، السوابق، القراءة، الجذر، الإعلال، الحكم، الوجود، الإعراب — كلُّ سطرٍ من
    قارئه القائم بلا زيادة."""

    out = [Line("ENTRY", len(w), "خانة")]
    if cert is not None:
        out.append(Line("CERT-n", cert, "عدد"))
    if not continue_licensed(w):
        return (*out, Line("GRANT-check", False, "حكم"))
    out.append(Line("GRANT-mursam" if licensed(w) else "MADD-lazim", True, "حكم"))
    if licensed(w):
        out.append(Line("FOLD", fold(w), "عدد"))
    ms = tawzi(w)
    if ms:
        out.append(Line("TAWZI-reader", len(ms), "قراءة"))
    ss = sawabiq(w)
    if ss:
        out.append(Line("SAWABIQ-reader", tuple(sorted({m.kind for m in ss})), "باب"))
    qs = qiraa(w)
    out.append(Line("QIRAA-reader", len(qs), "قراءة"))
    if harf(w):
        out.append(Line("QIRAA-reader", "حرف", "صنف"))
    hs = rank_qiraa(hukm_readings(w))
    if hs:
        top = hs[0]
        rs = roots_of(top.r)
        if rs:
            out.append(Line("MAQAYIS-member", (*rs[0], attested(top.r)), "جذر"))
        if top.r.ilal:
            rule = "ILAL-samai" if any(r == "SAMAI_FA" for r, _ in top.r.ilal) else "ILAL-descent"
            out.append(Line(rule, tuple(sorted({r for r, _ in top.r.ilal}, key=RULES.index)),
                            "قاعدة"))
        code = code_of_root(rs[0]) if rs else None
        if code is not None:
            _, j, q = judge_root(code)
            out.append(Line("HUKM-judge", (j.kind, q.kind, j.witness is not None,
                                           q.witness is not None), "مرتبة"))
        out.append(Line("WUJUD-partition", ont_of_reading(top.r), "صنف"))
    out.append(Line("TAWABI-case", case_class(w), "حالة"))
    return tuple(out)


def breaches(ls: tuple[Line, ...]) -> list[str]:
    """ما يُسقط العقد باسمه."""

    out = []
    for ln in ls:
        c = _BY_ID.get(ln.claim)
        if c is None:
            out.append(f"SHARH_CLAIM_NOT_IN_LEDGER {ln.claim}")
        elif c.status is Status.معلق:
            out.append(f"SHARH_CLAIM_SUSPENDED {ln.claim}")
        if ln.unit not in UNITS:
            out.append(f"SHARH_UNIT_NOT_IN_VOCABULARY {ln.unit}")
    return out
