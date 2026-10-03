"""Run the whole source→card→admission→adoption→application→verdict path once.

One command re-runs the connected review experiment and prints its trace::

    python examples/arabic/run_source_card_path.py

**The two books are read from their sealed bytes, never from the model.** Each
card names its material, its declared SHA-256, the extractor and its
fingerprint, and a half-open offset span *in that extractor's output*. An offset
is not a page number, and offsets taken from a different extraction are not
interchangeable with these. Every card is re-sliced from disk before anything is
admitted; a card whose slice no longer reproduces its excerpt is refused.

**Five things are kept apart and the script prints them apart**: the declared
founding conditions (``PK₀``, untouched here), the accumulated stock ``K_t``,
the candidate rule, the adopted rule, and one application of it to one case. A
single successful application is not a general adoption, and admitting that the
author *said* something is not admitting that what he said holds in the world.

**The seven review scenarios run on one connected stock**, each with its
expectation declared before it runs: a complete application, a missing-premise
suspension, a withdrawal of a required witness, survival on an independent
alternative support, an interpretation correction that versions the card and
re-evaluates only its dependents, an unrelated amendment that moves the stock
fingerprint and no verdict, and a stale certificate that verification rejects.

**The correction in scenario هـ corrects our own error, not the book's.** The
first version of the ``الحقيقة`` card carried an interpretation we wrote that
read ``حقيقة``/``مجاز`` as truth and falsity. That is a mistake about the
semantics of usage types, it is declared as ours, and the quoted slice itself is
never altered.

What this does not establish: it does not establish the truth of any external
fact the books report, it does not generalise the adopted rule beyond the
declared usage scope, and it is not connected to the 116 bridge — the delivery
is a *source reading and adoption path*, and that gap is named in the module as
``THE_UNCONNECTED_GAP``.
"""

from __future__ import annotations

from alghanem.arabic.source_card_path import (
    THE_CARDS,
    THE_CASES,
    THE_SOURCES,
    THE_UNCONNECTED_GAP,
    extractor_fingerprint,
    read_cards,
    run_experiment,
    seal_of,
)


def main() -> None:
    """اطبع المصادرَ والبطاقاتِ وأثرَ التجربة وجدولَ الأحكام."""

    print("المصادر المختومة")
    print("=" * 60)
    for source in THE_SOURCES:
        seal = seal_of(source.key)
        print(f"  {source.key}: {source.title}")
        print(f"    الملفّ: {source.relative_path}")
        print(f"    حاضرٌ على القرص: {seal.present}")
        print(f"    البايتات المقيسة: {seal.measured_byte_length:,}")
        print(f"    sha256 المقيسة: {(seal.measured_sha256 or '')[:32]}…")
        print(
            f"    مطابقةُ المُعلَن: "
            f"{'مطابقٌ طولًا وبصمة' if seal.matches_declared else 'مخالف'}"
        )
        print(
            f"    المستخرِج: {source.extractor.value} — وحدةُ الإزاحة: "
            f"{source.offset_unit}"
        )
    print(f"  بصمةُ المستخرِج: {extractor_fingerprint()[:32]}…")

    print()
    print("البطاقاتُ المصدريّة")
    print("=" * 60)
    for reading in read_cards():
        card = reading.card
        print(f"  {card.versioned_id} — {card.genus.value} — {card.speaker}")
        print(f"    الموضع: [{card.start}, {card.end}) في {card.material_key}")
        print(f"    أُعيد إنتاجُه من البايتات: {reading.is_reproduced}")
        print(f"    التفسير: {card.interpretation}")
        if card.conditions:
            print(f"    الشروط: {' · '.join(card.conditions)}")
        if card.exceptions:
            print(f"    الاستثناءات: {' · '.join(card.exceptions)}")
        print(f"    حدودُ الاستعمال: {' · '.join(card.use_limits)}")
        print(f"    حالُ المراجعة: {card.review.value}")

    trace = run_experiment()

    print()
    print("تجربةُ المراجعة المتصلة")
    print("=" * 60)
    for step in trace.steps:
        print(f"  [{step.key}] {step.title}")
        print(f"    التوقُّعُ المُعلَنُ قبل التشغيل: {step.expectation}")
        for observation in step.observations:
            print(f"      • {observation}")
        print(f"    بصمةُ الرصيد: {step.stock_content_id}")

    print()
    print("جدولُ الأحكام: كلُّ حكمٍ بنصّه وشروطه وتبعيّاته")
    print("=" * 60)
    for case_id, verdict, texts, conditions in trace.judgement_rows:
        print(f"  {case_id} | {verdict}")
        print(f"    النصوص/التبعيّات: {texts}")
        print(f"    الشروط: {conditions}")

    print()
    print("الحالاتُ المُودَعة")
    print("=" * 60)
    for case in THE_CASES:
        print(f"  {case.case_id}: «{case.phrase}» — اللفظُ: {case.word}")
        for fact in case.facts:
            print(f"    {fact.kind.value} = {fact.value}")

    print()
    print("البقايا")
    print("=" * 60)
    print(f"  {THE_UNCONNECTED_GAP}")
    print(f"  عددُ البطاقات: {len(THE_CARDS)} — عددُ الحالات: {len(THE_CASES)}")


if __name__ == "__main__":
    main()
