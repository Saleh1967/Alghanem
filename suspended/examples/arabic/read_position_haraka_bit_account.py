"""يقرأ محاسبةَ بتّات الجدولين: إغلاقَهما، وإنتروبياهما، وما يُغني عنه الحرف."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.position_haraka_bit_account import (  # noqa: E402
    POSITION_HARAKA_BIT_ACCOUNT_NAMED_RESIDUALS,
    THE_DECLARED_EXCLUSIONS,
    THE_FIRST_POSITION_TABLE,
    THE_LAST_POSITION_TABLE,
    ClosureStanding,
    DepositedTable,
    bit_account,
    closure_of,
    letter_information,
    table_without_letter,
)


def _read(table: DepositedTable) -> None:
    closure = closure_of(table)
    print(f"\n— {table.table_name} ({table.position})")
    print(f"  منزلةُ الأعداد        : {table.standing.value}")
    print(f"  المجموعُ المُعلَن       : {closure.stated_grand_total:,}")
    print(f"  مجموعُ الخلايا        : {closure.cell_sum:,}")
    print(f"  الإغلاق              : {closure.standing.value}")
    if closure.standing is not ClosureStanding.CLOSES_EXACTLY:
        print(
            f"  العجز                : {closure.shortfall:,} "
            f"({closure.shortfall_share:.3f}%)  موزَّعًا {closure.column_shortfalls}"
        )

    account = bit_account(table)
    print(f"  الوقعاتُ المحسوبةُ     : {account.occurrences:,}")
    print(f"  الحروفُ الحيّة         : {account.live_letters}")
    print(f"  H(حركة)              : {account.haraka_entropy:.6f} بت  من بتَّين")
    print(f"  الفائضُ عن العشوائيّ   : {account.uniform_haraka_slack:.6f} بت")
    print(f"  H(حرف)               : {account.letter_entropy:.6f} بت")
    print(f"  H(حرف,حركة)          : {account.joint_entropy:.6f} بت")
    print(f"  H(حركة | حرف)        : {account.conditional_haraka_entropy:.6f} بت")
    print(
        f"  I(حرف؛حركة)          : {account.mutual_information:.6f} بت  "
        f"= {account.explained_share:.3f}% من H(حركة)"
    )
    print(
        f"  أرضيّةُ المصادفة       : {account.chance_level_mutual_information:.6f} بت  "
        f"— وI تفوقها {account.times_chance_level:.0f} ضعفًا"
    )
    print(
        f"  كلفةُ العمود           : {account.haraka_bits_unconditioned():,.0f} بت "
        f"→ {account.haraka_bits_conditioned():,.0f} بت بعد معرفة الحرف"
    )
    print(f"  يوفّره الحرف          : {account.bits_saved_by_the_letter():,.0f} بت")

    print("  أثقلُ الحروف معلومةً   :", end=" ")
    print(
        "، ".join(
            f"{item.letter} {item.contribution:.5f}"
            for item in letter_information(table)[:5]
        )
    )


def main() -> int:
    """يطبع المحاسبةَ كاملةً، مشتقّةً عند القراءة من الخلايا المُودَعة."""

    print("محاسبةُ بتّاتٍ لجدولَي الموضع الأوّل والموضع الأخير")
    print("الأعدادُ منقولةٌ من وثيقةٍ خارجيّة؛ والبتّاتُ فوقها مشتقّةٌ ههنا.")

    _read(THE_FIRST_POSITION_TABLE)
    _read(THE_LAST_POSITION_TABLE)

    whole = bit_account(THE_LAST_POSITION_TABLE)
    trimmed = bit_account(table_without_letter(THE_LAST_POSITION_TABLE, "ا"))
    print("\nأثرُ استبعاد خليّة الألف السبعَ عشرةَ، مقيسًا بالتشغيل")
    for name, before, after in (
        ("H(حركة)", whole.haraka_entropy, trimmed.haraka_entropy),
        ("I(حرف؛حركة)", whole.mutual_information, trimmed.mutual_information),
        (
            "H(حركة|حرف)",
            whole.conditional_haraka_entropy,
            trimmed.conditional_haraka_entropy,
        ),
        ("H(حرف)", whole.letter_entropy, trimmed.letter_entropy),
    ):
        print(f"  {name:<14}: {before:.6f} → {after:.6f}   الفرق {after - before:+.3e}")
    print("  ومقاديرُ الحرف تتحرّك أكثرَ لأنّ صفًّا حُذِف، لا لأنّ سبعةَ عشرَ خرجت.")

    print("\nالاستبعاداتُ مُسجَّلةٌ لا ممحوّة")
    for exclusion in THE_DECLARED_EXCLUSIONS:
        place = "قبل الإيداع" if exclusion.excluded_before_deposit else "داخل الجدول"
        print(
            f"  {exclusion.excluded_occurrences:>6,}  {exclusion.exclusion_name} "
            f"({place}، {exclusion.table_name})"
        )

    print("\nما لم يُحسَم، مُسمًّى")
    for key in POSITION_HARAKA_BIT_ACCOUNT_NAMED_RESIDUALS:
        print(f"  - {key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
