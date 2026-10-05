"""يقرأ السكونَ المُضمَر في نصٍّ ثانٍ مُودَع، ويقابله بالفاتحة موضعًا بموضع."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.implicit_sukun_treatment import SukunSource  # noqa: E402
from alghanem.arabic.sukun_second_scope import (  # noqa: E402
    SECOND_SCOPE_NAMED_RESIDUALS,
    ScopeComparison,
    alif_replication,
    measured_onset_comparison,
    measured_text_comparison,
)


def _read(comparison: ScopeComparison) -> None:
    first, second = comparison.first, comparison.second
    print(f"\n— {first.scope}  ×  {second.scope}")
    print(f"  الكلماتُ المقيسة      : {first.words} | {second.words}")
    print(f"  الحواملُ الساكنة      : {first.total} | {second.total}")
    print(f"  المكتوبُ منها         : {first.written} | {second.written}")
    print(
        f"  نصيبُ المكتوب         : {first.written_share:.3f}% | "
        f"{second.written_share:.3f}%"
    )
    print(f"  الفرقُ بالنقاط        : {comparison.written_share_gap:.3f}")
    print("  التفصيلُ بالمصدر      :")
    for name, here, there in comparison.rows():
        print(f"    {name:<20} : {here} | {there}")
    print("  فرقُ نصيب المُضمَر     :")
    for source in SukunSource:
        if not source.is_written:
            gap = comparison.unwritten_share_gap(source)
            print(f"    {source.value:<20} : {gap:+.3f} نقطة")


def main() -> None:
    print("السكونُ المُضمَر في موضعٍ ثانٍ: اتّفاقٌ قريبٌ لا نسبةُ مصحف")
    print("=" * 62)
    _read(measured_text_comparison())
    _read(measured_onset_comparison())

    print("\n— الألفُ في الموضعين")
    for reading in alif_replication():
        print(
            f"  {reading.scope:<10} : ألفٌ مكتوبة {reading.alifs}، "
            f"بعلامة {reading.marked}، خنجريّة {reading.dagger_units}"
        )

    print("\n— ما لا يُثبِته هذا الموضعُ الثاني، مُسمًّى")
    for key in SECOND_SCOPE_NAMED_RESIDUALS:
        print(f"  • {key}")


if __name__ == "__main__":
    main()
