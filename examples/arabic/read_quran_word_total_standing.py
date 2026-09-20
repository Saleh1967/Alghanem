"""Read the standing of 78,215 — the one quoted corpus total this tree carries.

The figure is attributed in ``docs/reference/word_hierarchy_rebuild.md`` to
``quran-simple-enhanced.txt``, the corpus frozen as ``FROZEN_CORPUS`` with a
byte length of 1,319,901 and a SHA-256. Until now this tree could match those
bytes but could not **find** them: ``decode_corpus_bytes`` gated a door that
had no resolver, no sanctioned place, and no runnable path. That door is now
built, on the same three-source order as MASAQ::

    python examples/arabic/read_quran_word_total_standing.py

Those bytes are **not in this tree**; what is sanctioned is their place,
``corpora/quran-simple-enhanced.txt``, which this script consults last and only
if a file is actually there. While they remain outside — the case now — their
path is declared::

    ALGHANEM_QURAN_CORPUS_PATH=/path/to/quran-simple-enhanced.txt \\
        python examples/arabic/read_quran_word_total_standing.py

No figure is printed without a length **and** digest match, and no counting
rule is implicit: every total carries the rule that produced it.

What the mirror survey established, and what it did not. Five public copies
were measured directly — none matching the frozen length or digest, all
declared as such. Four of them, spanning byte lengths 1,160,550 to 1,337,820
and differing in line endings, produced the **same** whitespace-token total of
78,245; the Uthmani text produced 77,878. So the token total does not move
with the mark options that move the byte length, and the 30 that separates
78,215 from 78,245 is therefore **not** explained by a download option. This
script does not decide what does explain it. It also does not merge that 30
with the 134 already recorded in ``gflk_specification_deposit`` against the
sum of the four deposited counts: the two gaps fall on opposite sides of the
quoted figure.

This script adopts no figure, issues no verdict, and imports nothing from
``alghanem.kernel``.
"""

from __future__ import annotations

from alghanem.arabic.compression_model_preregistration import FROZEN_CORPUS
from alghanem.arabic.quran_corpus_word_total import (
    QURAN_CORPUS_NAMED_RESIDUALS,
    QURAN_CORPUS_PATH_VARIABLE,
    QURAN_CORPUS_RELATIVE_PATH,
    SURVEYED_MIRRORS,
    QuotedTotalStanding,
    WordCountingRule,
    quran_corpus_bytes_are_resolvable,
    run_quoted_total_survey,
    word_total,
)


def main() -> int:
    """يطبع منزلةَ الرقم المنقول، ولا يُخرِج عددًا بغير البايتات المبصومة."""

    print("المدوّنة المُجمَّدة")
    print(f"  الاسم        : {FROZEN_CORPUS.source_name}")
    print(f"  طولُ البايتات : {FROZEN_CORPUS.byte_length:,}")
    print(f"  البصمة       : {FROZEN_CORPUS.sha256_hex}")
    print(f"  الموضعُ المسنون: {QURAN_CORPUS_RELATIVE_PATH}")
    print(f"  متغيّرُ المسار : {QURAN_CORPUS_PATH_VARIABLE}")

    print("\nالمرايا المقيسة — وكلُّها مُصرَّحٌ بمخالفتها المُجمَّد")
    for mirror in SURVEYED_MIRRORS:
        print(
            f"  {mirror.mirror_byte_length:>9,} بايت  "
            f"{mirror.mirror_sha256_prefix}…  "
            f"آيات {mirror.ayah_lines:,}  رموز {mirror.whitespace_tokens:,}  "
            f"— {mirror.mirror_name}"
        )

    reading = run_quoted_total_survey()
    print("\nقراءةُ الرقم المنقول")
    print(f"  الرقم                 : {reading.quoted_total:,}")
    print(f"  المنزلة               : {reading.standing.value}")
    print(f"  الثابتُ المقيسُ على المرايا: {reading.mirror_invariant_total:,}")
    print(f"  البعدُ عنه             : {reading.distance_from_mirror_invariant:+,}")
    print(f"  مراياه المطابِقة       : {reading.mirrors_matching_the_quoted_total}")

    if reading.standing is QuotedTotalStanding.WITHHELD_FOR_WANT_OF_THE_BYTES:
        print(
            "\nلا عددَ يخرج من هنا: البايتاتُ المبصومةُ ليست محلولةً، "
            "والوقفُ رفضُ إخراجٍ لا قيمةٌ افتراضيّة."
        )
    else:
        print("\nالعددُ من البايتات المبصومة، بقاعدةٍ مُعلَنة")
        for rule in WordCountingRule:
            print(f"  {rule.value}: {word_total(rule):,}")

    print("\nما لم يُحسَم، مُسمًّى")
    for key in QURAN_CORPUS_NAMED_RESIDUALS:
        print(f"  - {key}")

    if not quran_corpus_bytes_are_resolvable():
        print(
            "\nونزولُ البايتات الصحيحةِ في الموضع المسنون ينقل هذه القراءةَ "
            "بلا سطرِ تعديلٍ واحد."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
