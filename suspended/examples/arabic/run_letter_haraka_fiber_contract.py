"""شغِّل العقدَ الليفيَّ للحرف والحركة، واقرأ كلَّ عنصرٍ بمنزلته ومانعه.

بايتاتُ الفاتحة المُودَعة في هذه الشجرة ومُبصَّمة، فهذا التشغيلُ لا ينتظر
ملفًّا ولا متغيّرَ بيئة::

    python examples/arabic/run_letter_haraka_fiber_contract.py

ويُطبَع لكلّ عنصرٍ ما يُدَّعى فيه، وعددُه المُشتَقّ، ومانعُه إن حُجِب. وما
يُقرأ ههنا **منزلةُ عنصرٍ على إيداعٍ بعينه** لا ولادةٌ ولا شهادة: العناصرُ
الصوتيّةُ محجوبةٌ بمانعها لأنّ `UnicodeIsNotRecordedSound` قائم، والسكونُ
المكتوب مفصولٌ عن غياب التشكيل عددًا لا دعوى.

وتشغيلُ هذا المثال غيرُ موقوفٍ على صدور شهادة ولادة `CV`؛ وهي غيرُ صادرةٍ
اليوم بنقصها المُعدَّد في `fiber_transfer_contracts`.

هذا المثالُ مرجعٌ لا جزءٌ من النواة: لا يُولّد كائنًا، ولا يرخّص انتقالًا، ولا
يُصدر شهادة، ولا يستورد من `alghanem.kernel`.
"""

from __future__ import annotations

import sys

from alghanem.arabic.fiber_transfer_contracts import CV_BIRTH_CERTIFICATE_STANDING
from alghanem.arabic.letter_haraka_fiber_contract import (
    LETTER_HARAKA_NAMED_RESIDUALS,
    ElementStanding,
    run_letter_haraka_contract,
)


def main() -> int:
    report = run_letter_haraka_contract()
    print(f"العقد: {report.contract_id}")
    print(f"بصمةُ الإيداع: {report.deposit_sha256}")
    print()

    for reading in report.readings:
        element = reading.element
        print(f"[{element.subject.value}] {element.element_id}")
        print(f"    الدعوى: {element.what_is_claimed}")
        print(f"    جنسُ الدليل: {element.evidence_genus.value}")
        if reading.standing is ElementStanding.HELD_ON_THE_DEPOSIT:
            print(
                f"    المنزلة: {reading.standing.value}"
                f" — {element.what_the_evidence_counts}: {reading.observed_count}"
            )
        else:
            print(f"    المنزلة: {reading.standing.value}")
            print(f"    المانع: {reading.withheld_because}")
        for residual in element.residuals:
            print(f"    بقيّة: {residual}")
        print()

    print(f"المنعقد: {len(report.held)}، المحجوب: {len(report.withheld)}")
    print()
    print("حدودُ هذا التشغيل، مُسمّاةً لا مطويّة:")
    for note in LETTER_HARAKA_NAMED_RESIDUALS:
        print(f"  - {note}")
    print()
    print(
        "شهادةُ ولادة CV: "
        + ("صادرة" if CV_BIRTH_CERTIFICATE_STANDING.issued else "غيرُ صادرة")
        + f"، وما ينقصها: {len(CV_BIRTH_CERTIFICATE_STANDING.what_is_still_missing)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
