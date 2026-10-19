"""قارئٌ لوديعة الخطّ: البتاتُ، وبصماتُها، وما يرفض القارئُ قراءته.

python examples/arabic/read_font_deposit.py
"""

from __future__ import annotations

from alghanem.arabic.font_deposit import (
    FONT_DEPOSIT,
    FontDepositError,
    deposit_path,
    every_deposit_matches_its_manifest,
    load_font,
    measured_manifest_of,
)
from alghanem.arabic.font_deposit import (
    FONT_DEPOSIT_NAMED_RESIDUALS as RESIDUALS,
)

_LETTERS = ("\u0628", "\u062a", "\u062b", "\u0627", "\u0623")


def main() -> None:
    """يعرض المانيفست المجمَّد، ثمّ ما تقوله البتاتُ عن حرفٍ حرف."""

    print("الوديعةُ ومانيفستُها المجمَّد:")
    print(f"  {'الملفّ':<28}{'بايت':>10}{'glyphs':>9}{'upem':>7}  البصمة")
    for entry in FONT_DEPOSIT:
        print(
            f"  {entry.filename:<28}{entry.byte_length:>10}"
            f"{entry.glyph_count:>9}{entry.units_per_em:>7}  {entry.sha256[:16]}…"
        )

    print()
    matched = every_deposit_matches_its_manifest()
    print(f"كلُّ وديعةٍ مطابقةٌ لمانيفستها عند القراءة: {matched}")
    for entry in FONT_DEPOSIT:
        measured = measured_manifest_of(entry.filename)
        where = deposit_path(entry.filename)
        print(f"  {entry.filename:<28} {measured == entry}  {where}")

    print()
    print("جداولُ كلِّ ملفّ:")
    for entry in FONT_DEPOSIT:
        print(f"  {entry.filename:<28}{len(entry.tables):>3}: {' '.join(entry.tables)}")

    print()
    print("ما تقوله البتاتُ عن الحرف، لا ما يقوله الجدول:")
    print(f"  {'الملفّ':<28}{'الحرف':>6}{'gid':>6}{'مركّب':>8}{'كنتورات':>9}  البصمة")
    for entry in FONT_DEPOSIT:
        font = load_font(entry.filename)
        for letter in _LETTERS:
            glyph = font.glyph_for(letter)
            composite = font.is_composite(glyph)
            try:
                outline = font.outline_of(glyph)
            except FontDepositError as refusal:
                print(f"  {entry.filename:<28}{letter:>6}{glyph:>6}  رُفض: {refusal}")
                continue
            print(
                f"  {entry.filename:<28}{letter:>6}{glyph:>6}"
                f"{'نعم' if composite else 'لا':>8}{len(outline):>9}"
                f"  {font.outline_hash(glyph)[:16]}…"
            )

    print()
    print("التفكيكُ المُعلَن، حيث يُعلَن:")
    for entry in FONT_DEPOSIT:
        font = load_font(entry.filename)
        glyph = font.glyph_for("\u0628")
        if not font.is_composite(glyph):
            print(f"  {entry.filename:<28} لا يعلن شيئًا: الرسمُ بسيط")
            continue
        components = font.components_of(glyph)
        drawn = "  ".join(f"({index}, {x}, {y})" for index, x, y in components)
        print(f"  {entry.filename:<28} ب = {drawn}")

    print()
    print("ما يرفضه القارئُ بدل أن يخمّنه:")
    for filename, argument in (
        ("DejaVuSans.ttf", "خطٌّ بلا مانيفست مجمَّد"),
        ("NoSuchFont-Regular.ttf", "ملفٌّ ليس في الوديعة"),
    ):
        try:
            load_font(filename)
        except FontDepositError as refusal:
            print(f"  {argument:<28} → {refusal}")

    print()
    print("المتبقّياتُ المسمّاة:")
    for text in RESIDUALS.values():
        print(f"  - {text}")


if __name__ == "__main__":
    main()
