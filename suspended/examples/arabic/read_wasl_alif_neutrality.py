"""يقرأ أثرَ همزة الوصل في سكون الابتداء، وحيادَ الألف محدودًا بما لا صفَّ له."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.position_haraka_bit_account import (  # noqa: E402
    THE_LAST_POSITION_TABLE,
)
from alghanem.arabic.wasl_alif_neutrality import (  # noqa: E402
    WASL_ALIF_NEUTRALITY_NAMED_RESIDUALS,
    alif_neutrality_bound,
    assess_shortfall_signature,
    sukun_onset_reading,
)


def main() -> None:
    print("همزةُ الوصل تُعَدُّ بأثرها، والألفُ تُقرأ صفرًا محدودًا")
    print("=" * 62)

    bound = alif_neutrality_bound()
    print(f"\n— حيادُ الألف في {bound.table_name}")
    print(f"  خلايا الصفّ           : {bound.printed_cells}")
    print(f"  الوقعاتُ المعدودة     : {bound.counted_occurrences:,}")
    print(f"  ما لا صفَّ له          : {bound.unaccounted_occurrences:,}")
    print(f"  المنزلة              : {bound.standing.value}")
    print(f"  النصيبُ المرصود       : {bound.observed_share:.3f}%")
    print(f"  أقصى نصيبٍ ممكن       : {bound.maximum_share:.3f}%")
    print(f"  أمُثبَتٌ الصفر؟         : {bound.zero_is_established()}")

    ending = alif_neutrality_bound(THE_LAST_POSITION_TABLE)
    print(f"\n— صفُّ الألف في {ending.table_name}")
    print(f"  خلايا الصفّ           : {ending.printed_cells}")
    print(f"  المنزلة              : {ending.standing.value}")

    reading = sukun_onset_reading()
    print("\n— أثرُ همزة الوصل: سكونُ الابتداء")
    print(f"  السكونُ المشتقّ        : {reading.derived_sukun:,}")
    print(f"  السكونُ المُعلَن        : {reading.stated_sukun:,}")
    print(f"  نصيبُه من المطبوع     : {reading.share_of_printed:.3f}%")
    print(f"  حواملُ ذاتُ سكونٍ      : {reading.carriers_with_a_sukun_onset}")
    for letter, count in reading.heaviest_carriers:
        print(f"    {letter} : {count:,}")
    print(f"  مجموعُهما             : {reading.heaviest_total:,}")
    print(f"  على المقام المشتقّ    : {reading.heaviest_share_on_derived():.3f}%")
    print(f"  على المقام المُعلَن    : {reading.heaviest_share_on_stated():.3f}%")

    standing, shortfall_share, reference_share = assess_shortfall_signature()
    print("\n— بصمةُ العجز مقابلَ صفّ الهمزة")
    print(f"  سكونُ العجز           : {shortfall_share:.3f}%")
    print(f"  سكونُ صفّ الهمزة       : {reference_share:.3f}%")
    print(f"  سكونُ الجدول المطبوع  : {reading.share_of_printed:.3f}%")
    print(f"  الحكم                : {standing.value}")

    print("\n— ما لا يُثبِته هذا الحساب، مُسمًّى")
    for key in WASL_ALIF_NEUTRALITY_NAMED_RESIDUALS:
        print(f"  • {key}")


if __name__ == "__main__":
    main()
