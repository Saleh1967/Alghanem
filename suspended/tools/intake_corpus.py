"""استقبالُ بايتات مدوّنةٍ إلى موضعها المسنون — عبر البوّابة لا بالالتفاف.

نسخُ ملفٍّ بـ`cp` إلى `corpora/` يُنزِل بايتاتٍ في موضعٍ مسنونٍ **بلا مطابقة**:
فإن خالفت الطولَ أو البصمةَ بقيت ساكنةً توهم أنّ المدوّنة حاضرة، ولا يُمسَك
ذلك إلّا عند أوّل قراءةٍ بعدها. وهذه الأداةُ تجعل النزولَ نفسَه عبورًا مأذونًا:

1. تُحَلّ البايتاتُ المصدريّةُ من `--source` أو من `--source-root`.
2. يُطابَق الطولُ والبصمةُ معًا على المُجمَّد في الشجرة قبل أيّ كتابة.
3. لا تُكتَب بايتةٌ واحدةٌ إلّا بعد نجاح المطابقتَين، والمخالفُ يُرفَض صريحًا
   ولا يُترَك أثرٌ منه في موضع الإيداع.

والاسمُ المقصدُ ليس اختيارًا: لا يُستقبَل إلّا ما هو مسنونٌ في
`SANCTIONED_DEPOSIT_FILENAMES`، فلا تُنشئ هذه الأداةُ اسمًا طارئًا في موضع
الإيداع. وإعادةُ التشغيل على بايتاتٍ مُودَعةٍ سلفًا لا تُعيد الكتابة.

**ومحضرُ «الدرجة الثالثة عند القياس» إجراءٌ ههنا لا درسٌ مكتوب.** في #186 خرج
16,796 مزدوجًا مقيسًا حيث كان المنقولُ إلى النثر 16,781: فانفصل المنقولُ عن
المقيس بلا أن يسقط شاهد. فقاعدةُ هذا الباب الآن: **لا رقمَ يُنسَخ من عرضٍ
خارجيّ إلى وديعة**. وكلُّ رقمٍ تُخرِجه هذه الأداةُ — الطولُ والبصمةُ — يُولَّد
من بايتات المقصد **بعد كتابتها** لا من بايتات المصدر في الذاكرة ولا من صفحةٍ
مقروءة؛ فتُمسَك الكتابةُ الناقصةُ عند بابها. وما لم يولَّد ههنا يُسمّى في
الوديعة `QUOTED_INCOMING_NOT_REPRODUCED` ولا يُقرأ مقيسًا
(`alghanem.arabic.audit_corpus_deposit`).

    python tools/intake_corpus.py --source-root /tmp/src
    python tools/intake_corpus.py --corpus quran-simple-enhanced.txt \\
        --source /path/to/quran-simple-enhanced.txt

ولا سلطةَ لهذه الأداة: لا تُصدِر رقمًا، ولا تُعدّل مُجمَّدًا، ولا تستورد من
`alghanem.kernel` شيئًا.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from alghanem.arabic.audit_corpus_deposit import (  # noqa: E402
    AUDIT_CORPUS_RELATIVE_PATH,
    THE_AUDIT_CORPUS,
)
from alghanem.arabic.compression_model_preregistration import (  # noqa: E402
    FROZEN_CORPUS,
)
from alghanem.arabic.masaq_corpus_deposit import (  # noqa: E402
    MASAQ_BYTE_LENGTH,
    MASAQ_RELATIVE_PATH,
    MASAQ_SHA256,
    SANCTIONED_DEPOSIT_FILENAMES,
)
from alghanem.arabic.quran_corpus_word_total import (  # noqa: E402
    QURAN_CORPUS_RELATIVE_PATH,
)


class IntakeRefusal(Exception):
    """رفضٌ عند البوّابة: مصدرٌ لا يُحَلّ، أو بايتاتٌ لا تطابق المُجمَّد."""


@dataclass(frozen=True, slots=True)
class SanctionedDeposit:
    """مقصدٌ مسنونٌ وبصمتُه وطولُه، مقروءَين من مُجمَّد الشجرة لا مكتوبَين هنا."""

    relative_path: str
    byte_length: int
    sha256_hex: str

    @property
    def name(self) -> str:
        return Path(self.relative_path).name

    @property
    def destination(self) -> Path:
        return REPOSITORY_ROOT / self.relative_path


SANCTIONED_DEPOSITS: tuple[SanctionedDeposit, ...] = (
    SanctionedDeposit(
        relative_path=MASAQ_RELATIVE_PATH,
        byte_length=MASAQ_BYTE_LENGTH,
        sha256_hex=MASAQ_SHA256,
    ),
    SanctionedDeposit(
        relative_path=QURAN_CORPUS_RELATIVE_PATH,
        byte_length=FROZEN_CORPUS.byte_length,
        sha256_hex=FROZEN_CORPUS.sha256_hex,
    ),
    SanctionedDeposit(
        relative_path=AUDIT_CORPUS_RELATIVE_PATH,
        byte_length=THE_AUDIT_CORPUS.byte_length,
        sha256_hex=THE_AUDIT_CORPUS.sha256_hex,
    ),
)


def _assert_every_destination_is_sanctioned() -> None:
    """حارسٌ: لا مقصدَ ههنا خارجَ ما أذن به `SANCTIONED_DEPOSIT_FILENAMES`."""

    for deposit in SANCTIONED_DEPOSITS:
        if deposit.name not in SANCTIONED_DEPOSIT_FILENAMES:
            raise IntakeRefusal(f"مقصدٌ غيرُ مأذونٍ به: {deposit.relative_path}")


_assert_every_destination_is_sanctioned()


def verify(data: bytes, deposit: SanctionedDeposit) -> None:
    """يُطابق الطولَ والبصمةَ معًا، ولا تُغني إحداهما عن الأخرى."""

    if len(data) != deposit.byte_length:
        raise IntakeRefusal(
            f"طولُ البايتات {len(data)} لا يطابق المُجمَّد {deposit.byte_length}"
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != deposit.sha256_hex:
        raise IntakeRefusal(
            f"بصمةُ البايتات {digest} لا تطابق المُجمَّدة {deposit.sha256_hex}"
        )


def locate_source(
    deposit: SanctionedDeposit, source: Path | None, source_root: Path | None
) -> Path | None:
    """المصدرُ المُصرَّحُ به وحدَه: المُمرَّرُ، وإلّا موضعُه تحت جذر المصدر."""

    if source is not None:
        return source
    if source_root is None:
        return None
    candidate = source_root / deposit.relative_path
    if candidate.is_file():
        return candidate
    flat = source_root / deposit.name
    return flat if flat.is_file() else None


def intake(deposit: SanctionedDeposit, source: Path) -> str:
    """يستقبل بايتاتٍ إلى موضعها المسنون بعد المطابقة، ويصف ما وقع.

    والوصفُ يحمل أرقامًا **مولَّدةً من القرص بعد الكتابة** لا منقولةً عن
    المصدر ولا عن عرضٍ خارجيّ: تُعاد قراءةُ المقصد وتُطابَق ثانيةً، فكتابةٌ
    ناقصةٌ أو مقطوعةٌ تُمسَك ههنا لا عند أوّل قراءةٍ بعد أيّام
    (`NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT`).
    """

    if not source.is_file():
        raise IntakeRefusal(f"لا ملفَّ في مسار المصدر: {source}")
    data = source.read_bytes()
    verify(data, deposit)
    destination = deposit.destination
    already = destination.is_file() and destination.read_bytes() == data
    if not already:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    settled = destination.read_bytes()
    verify(settled, deposit)
    generated = (
        f"طولٌ مولَّدٌ من القرص {len(settled)}؛ "
        f"بصمةٌ مولَّدةٌ من القرص {hashlib.sha256(settled).hexdigest()}"
    )
    if already:
        return f"مُودَعٌ سلفًا بالبصمة نفسِها: {deposit.relative_path} — {generated}"
    return f"أُودِعَ بعد مطابقة الطول والبصمة: {deposit.relative_path} — {generated}"


def _selected_deposits(names: list[str] | None) -> tuple[SanctionedDeposit, ...]:
    if not names:
        return SANCTIONED_DEPOSITS
    by_name = {deposit.name: deposit for deposit in SANCTIONED_DEPOSITS}
    chosen = []
    for name in names:
        key = Path(name).name
        if key not in by_name:
            raise IntakeRefusal(
                f"مدوّنةٌ غيرُ مسنونة: {name}؛ والمسنونُ: " + "، ".join(sorted(by_name))
            )
        chosen.append(by_name[key])
    return tuple(chosen)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        action="append",
        help="اسمُ المدوّنة المسنون؛ وبتركه تُنظَر المدوّناتُ كلُّها",
    )
    parser.add_argument("--source", type=Path, help="مسارُ البايتات المصدريّة")
    parser.add_argument(
        "--source-root",
        type=Path,
        help="جذرٌ يُبحَث تحته عن البايتات بمسارها المسنون أو باسمها",
    )
    arguments = parser.parse_args(argv)

    try:
        deposits = _selected_deposits(arguments.corpus)
    except IntakeRefusal as refusal:
        print(f"رفض: {refusal}", file=sys.stderr)
        return 2
    if arguments.source is not None and len(deposits) != 1:
        print(
            "رفض: `--source` يلزمه `--corpus` واحدةً، فلا يُخمَّن مقصدُ بايتات.",
            file=sys.stderr,
        )
        return 2
    if arguments.source is None and arguments.source_root is None:
        print(
            "رفض: لا مصدرَ مُصرَّحٌ به؛ فيُمرَّر `--source` أو `--source-root`.",
            file=sys.stderr,
        )
        return 2

    received = 0
    refusals = 0
    for deposit in deposits:
        source = locate_source(deposit, arguments.source, arguments.source_root)
        if source is None:
            print(f"  [تُرِك] لا مصدرَ لـ{deposit.relative_path}")
            continue
        try:
            print(f"  [تمّ] {intake(deposit, source)}")
            received += 1
        except IntakeRefusal as refusal:
            print(f"  [رفض] {deposit.relative_path}: {refusal}", file=sys.stderr)
            refusals += 1
    print(f"المُستقبَل: {received}؛ المرفوض: {refusals}.")
    return 1 if refusals else 0


if __name__ == "__main__":
    raise SystemExit(main())
