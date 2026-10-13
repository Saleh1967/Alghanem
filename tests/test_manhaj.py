"""سلسلةُ القرار (ADR ٥٨): `gate.manhaj` مرآةً لـ`A116.Qarar.judge1` و`A116.Manhaj.judgeT`.

١. المطابقة: الحكمان على كلّ سطرٍ من `lake exe a116-table qarar` (33,296 سلسلةً حتى ثلاثِ دعاوى،
   بأصلٍ مفقودٍ وبدونه).
٢. الشواهد باليد: سلسلةُ المدخل الثالث (ج1 س45، س86، س87، س348) والحكمُ المتوقَّع لكلّ دعوى مكتوبٌ
   هنا من النصّ، وشاهدُ `Qarar` الأوّل (الشوط الأوّل) كما حوكم في الجلسة.
٣. مبرهنتا `Manhaj` مفحوصتين على المرآة في كلّ سلسلةٍ من الجدول: لا مدخلَ ثالث (`roots_mahsus`)،
   والامتحانُ المضادّ (`monotone`: حذفُ سندٍ أو زرعُ معارضٍ لا يرفع حكمًا).
٤. الطفرات: `TASLIM_WITHOUT_PREMISES` (يقبل ما لا يُحسّ ولا أصلَ له)، `QATI_IGNORES_PREMISES`
   (القطعُ للوجود ولو على ظنّيّ)، `MUARID_IGNORED` (المعارضُ لا يُسقط).
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import pytest

from gate.manhaj import (
    DAWR,
    FALLEN,
    KHATA,
    LA_HUKM,
    QATI,
    SAQIT,
    SAWAB,
    ZANNI,
    Daawa,
    Judge,
    judge1,
    judge_t,
    run,
)

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "qarar.csv"
Chains = list[tuple[list[Daawa], list[str], list[str]]]


def d(i: int, w: bool, s: bool, m: bool, *us: int) -> Daawa:
    return Daawa(i, w, s, m, tuple(us))


def _parse(enc: str) -> list[Daawa]:
    out = []
    for node in enc.split(";"):
        i, bits, us = node.split(":")
        out.append(Daawa(int(i), bits[0] == "1", bits[1] == "1", bits[2] == "1",
                         tuple(int(u) for u in us.split(".") if u)))
    return out


def _chains() -> list[tuple[list[Daawa], list[str], list[str]]]:
    rows = []
    with TABLE.open(encoding="utf-8") as fh:
        for line in fh:
            enc, v1, vt = line.rstrip("\n").split(",")
            rows.append((_parse(enc), v1.split(" "), vt.split(" ")))
    return rows


@pytest.fixture(scope="module")
def chains() -> list[tuple[list[Daawa], list[str], list[str]]]:
    return _chains()


def _verdicts(cs: Sequence[Daawa], judge: Judge = judge_t) -> list[str]:
    return [h for _, h in run(cs, judge)]


# ١. المطابقة ---

def test_mirror_matches_lean(chains: list[tuple[list[Daawa], list[str], list[str]]]) -> None:
    assert len(chains) == 16 + 512 + 32768
    for cs, v1, vt in chains:
        assert _verdicts(cs, judge1) == v1, cs
        assert _verdicts(cs, judge_t) == vt, cs


# ٢. الشواهد باليد ---

TASLIM = [  # (الدعوى، حكمُ judge_t، حكمُ judge1) — من نصّ ج1
    (d(41, True, True, False), QATI, QATI),            # القرآنُ مدرَكٌ محسوسٌ وإعجازُه (س87)
    (d(42, True, True, False, 41), QATI, QATI),        # كونُه دليلًا ثبت بالعقل (س86)
    (d(43, True, False, False, 42), QATI, LA_HUKM),    # الملائكة «دليله نقلي» (س87، س45)
    (d(44, True, False, True), LA_HUKM, LA_HUKM),      # مدخلٌ نقليٌّ مستقلّ: لا حسَّ ولا أصل (س86)
    (d(45, False, True, False), ZANNI, ZANNI),         # صحّةُ خبر الآحاد ظنّ (س348)
    (d(46, True, False, False, 45), ZANNI, LA_HUKM),   # غيبٌ بالآحاد: ظنّيٌّ لا يصلح للعقيدة (س348)
    (d(47, True, True, False, 44), LA_HUKM, LA_HUKM),  # ما بُني على المدخل المستقلّ
]


def test_taslim_by_hand() -> None:
    cs = [c for c, _, _ in TASLIM]
    assert _verdicts(cs) == [t for _, t, _ in TASLIM]
    assert _verdicts(cs, judge1) == [o for _, _, o in TASLIM]


def test_qarar_witnesses_by_hand() -> None:
    seal_l0 = [d(1, True, True, True), d(2, True, True, True), d(3, False, True, False),
               d(4, False, True, True), d(5, True, True, True), d(6, False, False, False),
               d(7, True, True, True, 1), d(8, False, False, False), d(9, True, True, False),
               d(10, False, True, True), d(11, False, True, False), d(12, False, True, True),
               d(13, False, True, False, 1, 2), d(14, False, True, True)]
    expect = [KHATA, KHATA, ZANNI, KHATA, KHATA, LA_HUKM, SAQIT, LA_HUKM, QATI, KHATA, ZANNI,
              KHATA, SAQIT, KHATA]
    assert _verdicts(seal_l0, judge1) == expect == _verdicts(seal_l0, judge_t)
    assert _verdicts([d(1, True, True, False, 2)]) == [DAWR]


# ٣. المبرهنتان على المرآة ---

def _roots_ok(cs: Sequence[Daawa], verdicts: Sequence[str]) -> bool:
    by_id = {c.id: (c, h) for c, h in zip(cs, verdicts, strict=True)}
    for c, h in zip(cs, verdicts, strict=True):
        if h not in SAWAB:
            continue
        stack, seen = [c.id], set()
        while stack:
            a = stack.pop()
            if a in seen or a not in by_id:
                continue
            seen.add(a)
            x, hx = by_id[a]
            if hx not in SAWAB or (not x.usul and not x.mahsus):
                return False
            stack.extend(x.usul)
    return True


def _le(h2: str, h: str) -> bool:
    return (h2 not in SAWAB or h in SAWAB) and (h2 != QATI or h == QATI)


def test_theorems_on_every_chain(chains: list[tuple[list[Daawa], list[str], list[str]]]) -> None:
    for cs, _, vt in chains:
        assert _roots_ok(cs, vt), cs
        for i, c in enumerate(cs):
            for weak in (c._replace(mahsus=False), c._replace(muarid=True)):
                v2 = _verdicts([*cs[:i], weak, *cs[i + 1:]])
                assert all(_le(a, b) for a, b in zip(v2, vt, strict=True)), (cs, i, weak)
            if vt[i] in SAWAB:
                v3 = _verdicts([*cs[:i], c._replace(muarid=True), *cs[i + 1:]])
                assert v3[i] == KHATA
                assert all(v3[j] in FALLEN for j, x in enumerate(cs) if c.id in x.usul)


# ٤. الطفرات ---

def _mutant(kind: str) -> Judge:
    def judge(prior: dict[int, str], c: Daawa) -> str:
        prem = [prior.get(u) for u in c.usul]
        if any(p is None for p in prem):
            return DAWR
        if any(p in FALLEN for p in prem):
            return SAQIT
        ungrounded = not c.mahsus and not c.usul and kind != "TASLIM_WITHOUT_PREMISES"
        if any(p == LA_HUKM for p in prem) or ungrounded:
            return LA_HUKM
        if c.muarid and kind != "MUARID_IGNORED":
            return KHATA
        if c.wujud and (kind == "QATI_IGNORES_PREMISES" or all(p == QATI for p in prem)):
            return QATI
        return ZANNI
    return judge


@pytest.mark.parametrize("kind", ["TASLIM_WITHOUT_PREMISES", "QATI_IGNORES_PREMISES",
                                  "MUARID_IGNORED"])
def test_mutants_rejected(kind: str, chains: Chains) -> None:
    mutant = _mutant(kind)
    cs = [c for c, _, _ in TASLIM]
    by_hand = _verdicts(cs, mutant) != [t for _, t, _ in TASLIM]
    by_table = any(_verdicts(c, mutant) != vt for c, _, vt in chains)
    assert by_table
    if kind != "MUARID_IGNORED":
        assert by_hand  # 44 يصير صائبًا، أو 46 قطعيًّا
