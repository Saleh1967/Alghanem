"""تجاربُ بابِ المدوّنة: حلُّ المسار، وبوّابةُ البصمة، وقواعدُ العدّ، ومنزلةُ 78,215."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from alghanem.arabic.compression_model_preregistration import FROZEN_CORPUS
from alghanem.arabic.masaq_corpus_deposit import SANCTIONED_DEPOSIT_FILENAMES
from alghanem.arabic.quran_corpus_word_total import (
    QURAN_CORPUS_NAMED_RESIDUALS,
    QURAN_CORPUS_PATH_VARIABLE,
    QURAN_CORPUS_RELATIVE_PATH,
    SURVEYED_MIRRORS,
    THE_QUOTED_WORD_TOTAL,
    MirrorMeasurement,
    QuotedTotalStanding,
    QuranCorpusError,
    WordCountingRule,
    ayah_texts,
    count_words,
    quran_corpus_bytes_are_resolvable,
    quran_corpus_path,
    read_quran_corpus_bytes,
    run_quoted_total_survey,
    vendored_quran_corpus_path,
    word_total,
)

_SAMPLE = "1|1|بسم الله الرحمن الرحيم\n1|2|الحمد لله رب العالمين\n\n# رخصة تنزيل\n"


def test_the_sanctioned_place_is_inside_the_deposit_directory() -> None:
    """الموضعُ المسنونُ في `corpora/`، ومأذونٌ فيه، ولا يُخمَّن من `cwd`."""

    assert QURAN_CORPUS_RELATIVE_PATH == "corpora/quran-simple-enhanced.txt"
    assert Path(QURAN_CORPUS_RELATIVE_PATH).name in SANCTIONED_DEPOSIT_FILENAMES
    assert vendored_quran_corpus_path().is_absolute()
    assert vendored_quran_corpus_path().as_posix().endswith(QURAN_CORPUS_RELATIVE_PATH)


def test_the_passed_path_precedes_the_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """ترتيبُ المصادر مسنون: المُمرَّرُ أوّلًا، ثمّ البيئة، ثمّ المُودَع."""

    monkeypatch.setenv(QURAN_CORPUS_PATH_VARIABLE, str(tmp_path / "from-env.txt"))
    passed = tmp_path / "from-caller.txt"
    assert quran_corpus_path(passed) == passed
    assert quran_corpus_path() == tmp_path / "from-env.txt"


def test_absent_bytes_are_a_refusal_not_a_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """غيابُ الأبواب الثلاثة رفضٌ صريح، ولا يُخمَّن موضعُ الملفّ."""

    monkeypatch.delenv(QURAN_CORPUS_PATH_VARIABLE, raising=False)
    if vendored_quran_corpus_path().is_file():  # pragma: no cover - بحسب البايتات
        pytest.skip("البايتاتُ نزلت الموضعَ المسنون، فلا غيابَ يُختبَر")
    with pytest.raises(QuranCorpusError):
        quran_corpus_path()
    assert quran_corpus_bytes_are_resolvable() is False


def test_a_resolvable_path_is_not_a_resolvable_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """التخطّي معلَّقٌ بالبايتات لا بالمتغيّر: مسارٌ بلا ملفٍّ ليس حضورًا."""

    monkeypatch.setenv(QURAN_CORPUS_PATH_VARIABLE, str(tmp_path / "nothing.txt"))
    assert quran_corpus_bytes_are_resolvable() is False
    with pytest.raises(QuranCorpusError):
        read_quran_corpus_bytes()


def test_a_mismatched_file_fails_and_is_not_skipped(tmp_path: Path) -> None:
    """ملفٌّ مُحَلٌّ مخالفُ الطول أو البصمة يَفشَل، والموضعُ ليس شهادة."""

    wrong_length = tmp_path / "short.txt"
    wrong_length.write_bytes(b"x")
    assert quran_corpus_bytes_are_resolvable(wrong_length) is True
    with pytest.raises(QuranCorpusError, match="طولُ البايتات"):
        read_quran_corpus_bytes(wrong_length)

    right_length = tmp_path / "padded.txt"
    right_length.write_bytes(b"\x00" * FROZEN_CORPUS.byte_length)
    assert hashlib.sha256(right_length.read_bytes()).hexdigest() != (
        FROZEN_CORPUS.sha256_hex
    )
    with pytest.raises(QuranCorpusError, match="بصمةُ البايتات"):
        read_quran_corpus_bytes(right_length)


def test_no_figure_leaves_this_module_without_the_bytes(tmp_path: Path) -> None:
    """`word_total` لا تُخرِج قيمةً افتراضيّةً عند غياب البايتات."""

    with pytest.raises(QuranCorpusError):
        word_total(path=tmp_path / "absent.txt")


def test_the_licence_block_is_excluded_as_a_comment_not_by_line_count() -> None:
    """كتلةُ الرخصة تُستبعَد بأنّها تعليق، وسطرٌ بلا فاصلَي حقلٍ ليس آية."""

    assert ayah_texts(_SAMPLE) == (
        "بسم الله الرحمن الرحيم",
        "الحمد لله رب العالمين",
    )
    assert ayah_texts("# كلُّه تعليق\n") == ()
    assert ayah_texts("1|1\n") == ()


def test_each_rule_counts_something_different() -> None:
    """قواعدُ العدّ الثلاثُ تُخرِج ثلاثةَ مقاديرَ، فلا تُقارَن إلّا بقاعدتها."""

    by_text = count_words(_SAMPLE, WordCountingRule.WHITESPACE_TOKENS_IN_AYAH_TEXT)
    by_line = count_words(_SAMPLE, WordCountingRule.WHITESPACE_TOKENS_IN_WHOLE_LINE)
    lines = count_words(_SAMPLE, WordCountingRule.AYAH_LINES)
    assert by_text == 8
    assert lines == 2
    assert by_line == 8

    spaced = "1 | 1 | بسم الله\n"
    assert count_words(spaced, WordCountingRule.WHITESPACE_TOKENS_IN_AYAH_TEXT) == 2
    assert count_words(spaced, WordCountingRule.WHITESPACE_TOKENS_IN_WHOLE_LINE) == 6


def test_every_surveyed_mirror_differs_from_the_frozen_bytes() -> None:
    """المرايا مُصرَّحٌ بمخالفتها، وحارسُ الإنشاء يمنع تسلّلَ المُجمَّد منها."""

    assert len(SURVEYED_MIRRORS) == 5
    for mirror in SURVEYED_MIRRORS:
        assert mirror.mirror_byte_length != FROZEN_CORPUS.byte_length
        assert not FROZEN_CORPUS.sha256_hex.startswith(mirror.mirror_sha256_prefix)
        assert mirror.ayah_lines == 6_236

    with pytest.raises(QuranCorpusError):
        MirrorMeasurement(
            mirror_name="بطول المُجمَّد",
            mirror_byte_length=FROZEN_CORPUS.byte_length,
            mirror_sha256_prefix="deadbeef",
            ayah_lines=6_236,
            whitespace_tokens=78_245,
        )
    with pytest.raises(QuranCorpusError):
        MirrorMeasurement(
            mirror_name="ببادئة بصمة المُجمَّد",
            mirror_byte_length=1_000,
            mirror_sha256_prefix=FROZEN_CORPUS.sha256_hex[:8],
            ayah_lines=6_236,
            whitespace_tokens=78_245,
        )


def test_the_token_total_is_invariant_across_the_simple_family() -> None:
    """أربعُ نسخٍ مختلفةِ الطول والبصمة تُخرِج 78,245، والعثمانيُّ 77,878."""

    simple = {
        mirror.whitespace_tokens
        for mirror in SURVEYED_MIRRORS
        if "uthmani" not in mirror.mirror_name
    }
    uthmani = {
        mirror.whitespace_tokens
        for mirror in SURVEYED_MIRRORS
        if "uthmani" in mirror.mirror_name
    }
    assert simple == {78_245}
    assert uthmani == {77_878}
    lengths = {mirror.mirror_byte_length for mirror in SURVEYED_MIRRORS}
    assert len(lengths) == len(SURVEYED_MIRRORS)


def test_the_quoted_total_is_withheld_and_sits_thirty_below_the_invariant() -> None:
    """78,215 موقوفٌ لغياب البايتات، وبعدُه عن الثابت المقيس ثلاثون."""

    reading = run_quoted_total_survey()
    assert reading.quoted_total == THE_QUOTED_WORD_TOTAL == 78_215
    assert reading.mirror_invariant_total == 78_245
    assert reading.distance_from_mirror_invariant == -30
    assert reading.mirrors_matching_the_quoted_total == 0
    if reading.bytes_are_resolvable:  # pragma: no cover - بحسب البايتات
        assert reading.standing is not (
            QuotedTotalStanding.WITHHELD_FOR_WANT_OF_THE_BYTES
        )
    else:
        assert reading.standing is (QuotedTotalStanding.WITHHELD_FOR_WANT_OF_THE_BYTES)


def test_the_thirty_is_not_the_one_hundred_and_thirty_four() -> None:
    """الفرقان على طرفَي الرقم المنقول، ولا يُجمَعان ولا يُفسَّر أحدُهما بالآخر."""

    assert THE_QUOTED_WORD_TOTAL - 78_081 == 134
    assert THE_QUOTED_WORD_TOTAL - 78_245 == -30


def test_every_named_residual_starts_with_its_own_key() -> None:
    """ما لم يُحسَم مُسمًّى بأسمائه، وكلُّ قيمةٍ تبدأ بمفتاحها ثمّ `: `."""

    assert QURAN_CORPUS_NAMED_RESIDUALS
    for key, value in QURAN_CORPUS_NAMED_RESIDUALS.items():
        assert value.startswith(f"{key}: ")
