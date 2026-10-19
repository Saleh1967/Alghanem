"""Count the sections of the {0,1} bundle, and type the three "laws" apart.

A construction arrived in this tree that ascends from the binary distinction
between quiescent and moving — ``B = {0,1}`` — to a level 4 whose content is
"the three laws are exactly three sections of the same bundle". This script
recomputes that level instead of restating it::

    python examples/arabic/run_position_bundle_sections.py

Four things are printed that the incoming table folded into one.

**The sections are enumerated, not described.** A section is ``s: B → E`` with
``π∘s = id_B``, so it must assign a point over *every* base point. Their count
is the product of the fibre sizes, ``1 × 3 = 3`` — which matches the count of
laws in the table. The members do not match: every genuine section takes the
sukūn over ``b=0`` and differs only in which vowel it takes over ``b=1``, and
the three laws are not distinguished by a vowel choice at all.

**The types are separated.** ``s(every word) = 1`` has words for its domain and
``B`` for its codomain, so it is an occurrence labelling and not a section; the
measured distribution is the pushforward of one such labelling along ``π``, not
a third object standing beside the other two. ``Section`` refuses at
construction anything whose domain is not the base.

**The two constants are checked against the columns that were sent with them.**
Neither survives: the first position carries 10,339 sukūn (13.2187%) against
"b=1 always", and the final position carries 68,576 non-sukūn (87.8324%)
against "b=0 always, H=0". The second refutation is internal to the table — the
12.17% written in its own third row *is* the sukūn column said to exhaust the
position. The base entropies are 0.563405 and 0.534160 bits, neither zero.

**The ascent chain is recomputed step by step.** The first two steps agree.
The third does not: ``116 × 734/29 = 2936``, while ``21,286`` is ``734 × 29``.
The ratio between written and computed is exactly ``29/4``, which names what
was substituted — the factor 4 dropped is ``|E₁|``, the whole state space the
chain claims to derive everything from.

Every figure here is computed from the declared columns at run time. The
columns themselves are recorded as supplied: their bytes are not in this tree,
so nothing here re-derives them, and a share computed from a recorded count
inherits that standing rather than lifting it. This script adopts no figure,
issues no verdict, and imports nothing from ``alghanem.kernel``.
"""

from __future__ import annotations

from alghanem.arabic.position_bundle_sections import (
    POSITION_BUNDLE_NAMED_RESIDUALS,
    BaseState,
    pushforward_to_base,
    run_position_bundle,
    total_space,
)


def main() -> None:
    """Print the recomputed level 4 beside what was declared for it."""

    reading = run_position_bundle()

    print("المستوى ٠-١ — القاعدة والليف")
    print(f"  |B| = {len(BaseState)}    |E₁| = {reading.total_space_size}")
    print()

    print(f"المستوى ٤ — قطاعات π، وعدّتها |Γ(π)| = {reading.section_count}")
    for section in reading.sections:
        print(f"  {section.reference}")
    print("  كلُّ قطاعٍ ساكنٌ فوق b=0: " f"{reading.every_section_is_quiescent_at_zero}")
    print()

    print("الدعويان «ثابتٌ قطعيّ»، مقيستان على العمودين المُرسَلين")
    for law in (reading.inchoative_law, reading.pausal_law):
        print(f"  {law.position} — «{law.claimed_base.label} دومًا»")
        print(f"    المنزلة: {law.standing.value}")
        print(
            f"    المخالف: {law.counterexamples:,} من {law.denominator:,} "
            f"({law.counterexample_share * 100:.4f}%)"
        )
        print(f"    H(B) = {law.base_entropy_bits:.6f} بِتّ (السقف بِتٌّ واحد)")
    print()

    shares = pushforward_to_base(reading.final_position)
    print("الدفعُ الأماميُّ على القاعدة في الموضع الأخير — وهو s_g مُشتقًّا")
    for base in BaseState:
        print(f"  P(b={base.value}) = {shares[base] * 100:.6f}%")
    print(
        f"  H(E₁) = {reading.final_position.total_entropy_bits:.6f} بِتّ " "(السقف بِتّان)"
    )
    print()

    print("سلسلةُ الصعود، مُعادةَ الحوسبة خطوةً خطوة")
    for step in reading.chain:
        mark = "=" if step.agrees else "≠"
        print(
            f"  {step.step.name}: {step.step.declared_input} × "
            f"{step.step.factor_numerator}/{step.step.factor_denominator} = "
            f"{step.recomputed_output:g} {mark} {step.step.declared_output:,}"
        )
    for step in reading.chain_disagreements:
        print(
            f"  نسبةُ المكتوب إلى المحسوب في «{step.step.name}» = "
            f"{step.declared_over_recomputed:.6g}"
        )
    print()

    print("ما لا تُثبِته هذه القراءة:")
    for name in POSITION_BUNDLE_NAMED_RESIDUALS:
        print(f"  - {name}")

    assert len(total_space()) == 4


if __name__ == "__main__":
    main()
