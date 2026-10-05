"""تحقُّقٌ مستقلّ من أرقام الموضع الثاني: قاعدةٌ ثانيةٌ تُكتَب ههنا من أوّلها.

هذا الملفُّ **لا يستورد `CarrierStateCodec`**، وهو عينُ المقصود. سمّت
`sukun_second_scope` حدَّها بنفسها: `A_SHARED_CODEC_IS_A_SHARED_LIMIT` — أنّ
النصّين قُرِئا بأداةٍ واحدة، فميلُها يحرّك الرقمين معًا فيظهر اتّفاقًا. ولا
يُرفَع هذا الحدُّ بالكلام، وإنّما **بقاعدةٍ ثانيةٍ تُكتَب مستقلّةً** وتُقرأ
بها البايتاتُ نفسُها، ثمّ يُقابَل الخارجان وحدةً وحدةً لا مجموعًا بمجموع.

**وما يرفعه هذا التحقّقُ محدودٌ ومُسمًّى**: يرفع احتمالَ خطأِ تنفيذٍ في
المولّد، ولا يرفع اشتراكَ القاعدة. فالقاعدتان كلتاهما تقرآن «حاملٌ بلا علامةٍ
= ساكن» و«الشدّةُ نصفان أوّلُهما لا يُكتَب»، وهما اصطلاحٌ لا مقيس. فاستقلالُ
الأداة ليس استقلالَ القاعدة، وهذا الملفُّ لا يدّعيه.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Final

import pytest

from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.sukun_second_scope import (
    measured_onset_comparison,
    measured_text_comparison,
)

_FATHA: Final = "\u064e"
_DAMMA: Final = "\u064f"
_KASRA: Final = "\u0650"
_FATHATAN: Final = "\u064b"
_DAMMATAN: Final = "\u064c"
_KASRATAN: Final = "\u064d"
_SHADDA: Final = "\u0651"
_SUKUN: Final = "\u0652"
_DAGGER: Final = "\u0670"
_ALIF: Final = "\u0627"

_VOWELS: Final[frozenset[str]] = frozenset(
    {_FATHA, _DAMMA, _KASRA, _FATHATAN, _DAMMATAN, _KASRATAN}
)
_MARKS: Final[frozenset[str]] = _VOWELS | {_SHADDA, _SUKUN, _DAGGER}

_FATIHA: Final[str] = "\n".join(FATIHA_LINES)
_FATH: Final[str] = FATH_AYAH_SOURCE_TEXT


def _units(word: str) -> list[tuple[str, frozenset[str]]]:
    """يجمع كلَّ حرفٍ بما يتبعه من علاماتٍ حتّى الحرف التالي، ولا يفسّر شيئًا."""

    built: list[tuple[str, list[str]]] = []
    for character in word:
        if character in _MARKS:
            assert built, f"علامةٌ بلا حاملٍ في {word!r}"
            built[-1][1].append(character)
        else:
            built.append((character, []))
    return [(carrier, frozenset(marks)) for carrier, marks in built]


def _is_bare(marks: frozenset[str]) -> bool:
    """أخلا الحاملُ من حركةٍ ومن ألفٍ خنجريّةٍ ومن سكونٍ مكتوب؟"""

    return not (marks & _VOWELS) and _DAGGER not in marks and _SUKUN not in marks


def _census(text: str, alif_carriers: frozenset[str] = frozenset({_ALIF})) -> Counter:
    """القاعدةُ الثانية كاملةً: تُصنَّف الحواملُ الساكنةُ بأربعة أبوابٍ مسمّاة."""

    tally: Counter = Counter()
    for word in text.split():
        for carrier, marks in _units(word):
            if _SHADDA in marks:
                tally["pair"] += 1
            if _SUKUN in marks:
                tally["written"] += 1
            elif _is_bare(marks):
                tally["alif" if carrier in alif_carriers else "bare"] += 1
    return tally


def _onset_census(text: str) -> Counter:
    """الموضعُ الأوّل وحدَه، بعد رفع كلِّ ألفٍ عاريةٍ من أوّل الكلمة."""

    tally: Counter = Counter()
    for word in text.split():
        kept = [
            (carrier, marks)
            for carrier, marks in _units(word)
            if not (carrier == _ALIF and _is_bare(marks))
        ]
        if not kept:
            continue
        carrier, marks = kept[0]
        if _SUKUN in marks:
            tally["written"] += 1
        elif _is_bare(marks):
            tally["pair" if _SHADDA in marks else "bare"] += 1
        elif _SHADDA in marks:
            tally["pair"] += 1
    return tally


def _share(tally: Counter) -> float:
    return 100.0 * tally["written"] / sum(tally.values())


def _unwritten(tally: Counter) -> int:
    return sum(tally.values()) - tally["written"]


# --- أوّلًا: أرقامٌ تُعَدّ من البايتات وحدَها، بلا قاعدةٍ ولا تفسير ----------


@pytest.mark.parametrize(
    ("text", "mark", "expected"),
    [
        (_FATIHA, _SUKUN, 21),
        (_FATH, _SUKUN, 27),
        (_FATIHA, _SHADDA, 14),
        (_FATH, _SHADDA, 16),
        (_FATIHA, _ALIF, 23),
        (_FATH, _ALIF, 33),
        (_FATIHA, _DAGGER, 2),
        (_FATH, _DAGGER, 0),
    ],
)
def test_the_written_figures_are_plain_codepoint_counts(
    text: str, mark: str, expected: int
) -> None:
    assert text.count(mark) == expected


def test_no_alif_in_either_deposit_bears_any_mark_at_all() -> None:
    for text in (_FATIHA, _FATH):
        for word in text.split():
            for carrier, marks in _units(word):
                if carrier == _ALIF:
                    assert marks == frozenset()


# --- ثانيًا: القاعدةُ الثانيةُ تُعيد اشتقاق كلِّ رقمٍ منشور -----------------


def test_the_second_rule_reproduces_the_first_text_census() -> None:
    tally = _census(_FATIHA)
    assert dict(tally) == {"written": 21, "alif": 23, "pair": 14, "bare": 17}
    assert sum(tally.values()) == 75
    assert _share(tally) == pytest.approx(28.0, abs=1e-9)


def test_the_second_rule_reproduces_the_second_text_census() -> None:
    tally = _census(_FATH)
    assert dict(tally) == {"written": 27, "alif": 33, "pair": 16, "bare": 28}
    assert sum(tally.values()) == 104
    assert _share(tally) == pytest.approx(25.961538, abs=1e-6)


def test_the_second_rule_reproduces_both_onset_censuses() -> None:
    assert dict(_onset_census(_FATIHA)) == {"written": 5, "pair": 1, "bare": 8}
    assert dict(_onset_census(_FATH)) == {"written": 3, "pair": 1, "bare": 8}


def test_the_second_rule_reproduces_every_published_gap() -> None:
    first, second = _census(_FATIHA), _census(_FATH)
    assert _share(first) - _share(second) == pytest.approx(2.038462, abs=1e-6)
    for door, expected in (
        ("alif", -0.264550),
        ("pair", 5.146705),
        ("bare", -4.882155),
    ):
        gap = 100.0 * first[door] / _unwritten(first) - 100.0 * second[door] / (
            _unwritten(second)
        )
        assert gap == pytest.approx(expected, abs=1e-6)

    onset_gap = _share(_onset_census(_FATIHA)) - _share(_onset_census(_FATH))
    assert onset_gap == pytest.approx(10.714286, abs=1e-6)


def test_the_second_rule_reproduces_the_pooled_share_and_the_corpus_fraction() -> None:
    first, second = _census(_FATIHA), _census(_FATH)
    pooled = (
        100.0
        * (first["written"] + second["written"])
        / (sum(first.values()) + sum(second.values()))
    )
    assert pooled == pytest.approx(26.815642, abs=1e-6)
    words = len(_FATIHA.split()) + len(_FATH.split())
    assert words == 83
    assert 100.0 * words / 78_245 == pytest.approx(0.106077, abs=1e-6)


# --- ثالثًا: المقابلةُ بين القاعدتين، وهي موضعُ التحقّق -------------------


def test_the_two_rules_agree_on_every_published_number() -> None:
    text = measured_text_comparison()
    assert (text.first.total, text.first.written) == (
        sum(_census(_FATIHA).values()),
        _census(_FATIHA)["written"],
    )
    assert (text.second.total, text.second.written) == (
        sum(_census(_FATH).values()),
        _census(_FATH)["written"],
    )
    onset = measured_onset_comparison()
    assert onset.first.written == _onset_census(_FATIHA)["written"]
    assert onset.second.written == _onset_census(_FATH)["written"]


def test_the_agreement_holds_word_by_word_and_not_only_in_the_totals() -> None:
    """مجموعان متساويان قد يُخفيان خطأين متعاوضين؛ فالمقابلةُ كلمةً بكلمة."""

    from alghanem.arabic.encoding.carrier_state_candidate import (
        CarrierState,
        CarrierStateCodec,
    )

    codec = CarrierStateCodec()
    sukun_states = {CarrierState.SUKUN_EXPLICIT, CarrierState.SUKUN_IMPLICIT}

    def by_the_second_rule(word: str) -> list[str]:
        tags: list[str] = []
        for carrier, marks in _units(word):
            if _SHADDA in marks:
                tags.append("pair")
            if _SUKUN in marks:
                tags.append("written")
            elif _is_bare(marks):
                tags.append("alif" if carrier == _ALIF else "bare")
        return sorted(tags)

    def by_the_codec(word: str) -> list[str]:
        tags: list[str] = []
        for unit in codec.generate(word):
            if unit.state not in sukun_states:
                continue
            if unit.state is CarrierState.SUKUN_EXPLICIT:
                tags.append("written")
            elif unit.gemination is not None:
                tags.append("pair")
            elif unit.carrier == _ALIF:
                tags.append("alif")
            else:
                tags.append("bare")
        return sorted(tags)

    for text in (_FATIHA, _FATH):
        for word in text.split():
            assert by_the_second_rule(word) == by_the_codec(word), word


def test_the_codec_renames_carriers_where_the_second_rule_keeps_them() -> None:
    """الاتّفاقُ ليس تطابقَ تنفيذ: الأداةُ تطوي «ى» في «ي» و«آ» في «ء»."""

    from alghanem.arabic.encoding.carrier_state_candidate import (
        CarrierState,
        CarrierStateCodec,
    )

    codec = CarrierStateCodec()
    sukun_states = {CarrierState.SUKUN_EXPLICIT, CarrierState.SUKUN_IMPLICIT}
    renamed = 0
    for word in _FATH.split():
        mine = sorted(carrier for carrier, marks in _units(word) if _is_bare(marks))
        theirs = sorted(
            unit.carrier
            for unit in codec.generate(word)
            if unit.state is CarrierState.SUKUN_IMPLICIT and unit.gemination is None
        )
        assert len(mine) == len(theirs), word
        if mine != theirs:
            renamed += 1
    assert renamed == 5
    assert sukun_states
    assert "\u0649" in _FATH
    assert not any("\u0649" == unit.carrier for unit in codec.generate("عَلَى"))


# --- رابعًا: ما لا يُثبِته هذا التحقّق، مقيسًا لا مُدَّعًى ----------------


def test_the_closest_agreement_moves_with_a_convention_neither_rule_tested() -> None:
    """ربعُ النقطة في باب الألف مشروطٌ بحدّ «الألف»، ولم يُقَس هذا الحدّ."""

    def alif_share(text: str, carriers: frozenset[str]) -> float:
        tally = _census(text, carriers)
        return 100.0 * tally["alif"] / _unwritten(tally)

    narrow = frozenset({_ALIF})
    with_maksura = frozenset({_ALIF, "\u0649"})
    with_madda = frozenset({_ALIF, "\u0649", "\u0622"})

    assert alif_share(_FATIHA, narrow) - alif_share(_FATH, narrow) == pytest.approx(
        -0.264550, abs=1e-6
    )
    assert alif_share(_FATIHA, with_maksura) - alif_share(
        _FATH, with_maksura
    ) == pytest.approx(-4.160654, abs=1e-6)
    assert alif_share(_FATIHA, with_madda) - alif_share(
        _FATH, with_madda
    ) == pytest.approx(-6.758056, abs=1e-6)


def test_this_check_lifts_the_implementation_and_not_the_rule() -> None:
    """القاعدتان تشتركان في اصطلاحٍ لم تقسه واحدةٌ منهما، وهو مُسمًّى ههنا."""

    source = Path(__file__).read_text(encoding="utf-8")
    assert "A_SHARED_CODEC_IS_A_SHARED_LIMIT" in source
    assert "استقلالُ الأداة ليس استقلالَ القاعدة" in source
    assert _is_bare(frozenset())
    assert not _is_bare(frozenset({_FATHA}))
