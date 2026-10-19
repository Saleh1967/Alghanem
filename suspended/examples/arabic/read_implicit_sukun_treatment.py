"""يقرأ السكونَ المُضمَر: كم منه مكتوبٌ، وكم مستنتَجٌ من غياب، ومن أيّ باب."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.implicit_sukun_treatment import (  # noqa: E402
    IMPLICIT_SUKUN_NAMED_RESIDUALS,
    SukunCensus,
    SukunSource,
    measured_onset_census,
    measured_text_census,
)


def _read(census: SukunCensus) -> None:
    print(f"\n— {census.scope}")
    print(f"  الكلماتُ المقيسة      : {census.words}")
    print(f"  الحواملُ الساكنة      : {census.total}")
    print(f"  المكتوبُ منها         : {census.written}")
    print(f"  المُضمَرُ منها          : {census.unwritten}")
    print(f"  نصيبُ المكتوب         : {census.written_share:.3f}%")
    print(f"  الحكم                : {census.standing.value}")
    print("  التفصيلُ بالمصدر      :")
    for name, count in census.split():
        print(f"    {name:<20} : {count}")
    if census.unwritten:
        print("  نصيبُ كلِّ مُضمَرٍ منه   :")
        for source in SukunSource:
            if not source.is_written:
                share = census.share_of_unwritten(source)
                print(f"    {source.value:<20} : {share:.3f}%")


def main() -> None:
    print("السكونُ المُضمَر: عمودٌ ليس حرفًا")
    print("=" * 62)
    _read(measured_text_census())
    _read(measured_onset_census())

    print("\n— ما لا يُثبِته هذا العلاج، مُسمًّى")
    for key in IMPLICIT_SUKUN_NAMED_RESIDUALS:
        print(f"  • {key}")


if __name__ == "__main__":
    main()
