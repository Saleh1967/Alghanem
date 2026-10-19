"""Prove the `G0.SDAL-0` structural algebra at `zero` and `one` on synthetic slots.

Run it::

    python examples/structural_dal/prove_zero_one_algebra.py

**No language enters this proof.** The slots are opaque symbols (`SlotA`,
`SlotB`). There is no root, no weight, no augmentation, no lexicon and no
meaning here, and the layer refuses to import any package that carries them.
The claim is lowered to its purpose: `StructuralOperatorProof ->
EligibleForFiberIntegration`, nothing more.

**`zero` is not nothing, and it is not a core either.** It is the smallest
complete whole, one slot, declared `UNASSIGNED`, with every positive role empty:
`NeutralFiberInput -/-> PositiveStructuralRole`. It establishes exact
reconstruction, complete coverage, identity preservation and trace preservation
— and it carries a blocking residual that refuses every promotion until a proved
role basis arrives from outside this layer.

**`one` does not pick a partition.** Adding a slot yields a
`ShapePartitionHypothesisSet` with no forced winner:
`ShapePartitionHypothesis != RootCandidate` and
`ShapePartitionHypothesis != WeightCandidate`.

**Residuals are classified, not a sink.** An unproved role basis is *blocking*,
so every partition at `one` reconstructs the whole exactly and is still refused
promotion: `UnprovedRoleBasis -> BlockingResidual`.

**Identity mode is declared, never defaulted.** Only `SameEntityRescaling` is
open here; `CertifiedBranchBirth` is named and deferred, because this layer may
not issue its own birth certificate.

**The output-contract reading is not a strength claim.** The contract is defined
by this layer, so `SelfDefinedContract -/-> ComparativeStrength`.
"""

from __future__ import annotations

from alghanem.structural_dal import (
    PartWholeRelation,
    ResidualClass,
    SlotRole,
    prove_zero_one_algebra,
)


def main() -> None:
    """Print every stage of the `zero-one` proof with its operational evidence."""

    report = prove_zero_one_algebra()

    print("=" * 72)
    print("G0.SDAL-0 — برهانُ جبر zero-one على خاناتٍ مُصطنَعة")
    print("=" * 72)
    print(f"بصمةُ التسجيل المسبق: {report.preregistration_digest}")
    print()

    print("-" * 72)
    print("1) ZeroStructuralState — أصغرُ كلٍّ مكتملٍ محايد")
    print("-" * 72)
    zero = report.zero
    print(f"الكلّ             : {zero.whole.whole_id}")
    print(f"المِرساة          : {zero.whole.anchor_id}")
    print(f"الخانات           : {list(zero.whole.tokens)}")
    for role in SlotRole:
        part = zero.decomposition.part_of(role)
        print(
            f"  {role.value:<10}: {list(part.tokens)} "
            f"({part.relation_to_whole.value})"
        )
    print(f"إعادةُ البناء      : {list(zero.decomposition.reconstruction)}")
    print(f"تُطابق الكلَّ      : {zero.reconstructs_exactly}")
    print(f"ما يُثبِته         : {list(zero.establishes)}")
    print(f"دورٌ إيجابيٌّ مُسنَد : {not zero.assigns_no_positive_role}")
    print(f"موقفُ الترقية      : {zero.promotion_standing.value}")
    for reading in zero.residuals:
        print(f"  residual (حاجبة): {reading.reason}")
    print(f"ما لا يُثبِته      : {zero.does_not_establish}")
    print()

    print("-" * 72)
    print("2) الانتقال zero → one — العقدُ السباعيُّ بنمطٍ مُصرَّح")
    print("-" * 72)
    transition = report.ascent.transition
    print(f"نمطُ الهويّة       : {report.ascent.mode.value} (مُصرَّحٌ لا مفترَض)")
    print(f"Input      : {transition.input_identity}")
    print(f"Difference : {transition.difference.description}")
    print(f"Invariant  : {list(transition.invariant)}")
    print(f"Gate       : {list(transition.gate)}")
    print(f"Output     : {transition.output_identity}")
    print(f"Residual   : {[reading.reason for reading in transition.residual]}")
    print(f"Trace      : {len(transition.trace.steps)} خطوة")
    print(f"الخانةُ المُضافة   : موضع {transition.added_slot_index}")
    print(f"parent_anchor_id  : {transition.parent_anchor_id}")
    print(
        "الأثرُ تراكميّ     : "
        f"{report.ascent.before.trace_steps} → {report.ascent.after.trace_steps} "
        f"({report.ascent.trace_is_cumulative})"
    )
    print(f"عينُ المِرساة محفوظة: {transition.preserves_instance_identity}")
    print()

    print("-" * 72)
    print("3) ShapePartitionHypothesisSet — بلا فائزٍ مفروض")
    print("-" * 72)
    print(f"الكلُّ بعد الصعود  : {list(report.ascent.after.tokens)}")
    print(f"عددُ الفرضيّات     : {report.one_hypotheses.count} (مُشتَقٌّ لا مُجمَّد)")
    print(f"الفائزُ المفروض    : {report.one_hypotheses.forced_winner}")
    print(f"القانون           : {report.one_hypotheses.refusal}")
    for law in report.one_hypotheses.what_it_is_not:
        print(f"  - {law}")
    print()

    print("-" * 72)
    print("4) التفكيكُ والبقايا والترقية")
    print("-" * 72)
    attempts = {
        attempt.decomposition_id: attempt for attempt in report.promotion_attempts
    }
    for decomposition in report.one_decompositions:
        roles = "/".join(role.value for role in decomposition.hypothesis.roles)
        print(f"• {roles}")
        for role in SlotRole:
            part = decomposition.part_of(role)
            marker = (
                " ← إسقاطٌ مرتّبٌ لا مقطعٌ متّصل"
                if part.relation_to_whole is PartWholeRelation.ORDERED_PROJECTION
                else ""
            )
            print(
                f"    {role.value:<10}: indices={list(part.indices)} "
                f"tokens={list(part.tokens)} anchor={part.part_anchor_id} "
                f"relation={part.relation_to_whole.value}{marker}"
            )
        print(f"    reconstruction : {list(decomposition.reconstruction)}")
        print(f"    يُطابق الكلَّ    : {decomposition.reconstructs_whole}")
        print(f"    تغطيةٌ تامّة     : {decomposition.covers_every_slot_once}")
        for reading in decomposition.residuals:
            mark = (
                "حاجبة"
                if reading.residual_class is ResidualClass.BLOCKING
                else "غير حاجبة"
            )
            print(f"    residual ({mark}): {reading.reason}")
        attempt = attempts[decomposition.decomposition_id]
        print(f"    الترقية        : {attempt.standing.value} — {attempt.refusal}")
        if attempt.deferred_birth is not None:
            birth = attempt.deferred_birth
            print(
                f"    ولادةُ الفرع    : {birth.availability.value} — "
                f"{birth.requested_anchor_id}"
            )
        print()

    print("-" * 72)
    print("5) قراءةُ عقد المخرج الذاتيِّ — وصفٌ لا حكمُ قوّة")
    print("-" * 72)
    print(f"النموذجُ الأضعف    : {report.weaker.model_id} — {report.weaker.description}")
    print(f"مخرجُه            : {list(report.weaker.output)}")
    print(
        "ما وفّاه          : "
        f"{[component.value for component in report.weaker.satisfied]}"
    )
    print(f"حالُه             : {report.weaker.outcome.value}")
    print(
        "ما وفّاه الجبر     : "
        f"{[component.value for component in report.structural_satisfied]}"
    )
    print(f"حالُ الجبر         : {report.structural_outcome.value}")
    reading = report.self_defined_contract_reading
    print(f"قراءةُ العقد الذاتيّ: {reading.value}")
    print(f"ما لا تُثبِته      : {reading.does_not_establish}")
    print()

    print("-" * 72)
    print("6) العزلُ البنيويُّ والمفردات")
    print("-" * 72)
    print(f"وحداتٌ مفحوصة      : {len(report.isolation.scanned_files)}")
    print(f"ما استوردته       : {list(report.isolation.alghanem_imports)}")
    print(f"مخالفاتُ العزل     : {list(report.isolation.violations)}")
    print(f"معزولة            : {report.isolation.is_isolated}")
    print(f"أسماءٌ مفحوصة      : {len(report.vocabulary.inspected_names)}")
    print(f"مخالفاتُ المفردات  : {list(report.vocabulary.violations)}")
    print(f"خاليةٌ من اللغويّ  : {report.vocabulary.is_clean}")
    print()

    print("=" * 72)
    print("7) بنودُ القبول (مُشتَقّةٌ لا مُجمَّدةُ العدد)")
    print("=" * 72)
    for item, held in report.findings.items():
        print(f"  [{'x' if held else ' '}] {item.value}")
    print()
    print(f"الجبرُ ثابت       : {report.algebra_holds}")
    print(f"بنودٌ لم تثبت     : {[item.value for item in report.unmet_items]}")
    print()
    print("ما لا يُثبِته هذا البرهان:")
    for statement in report.what_is_not_established:
        print(f"  - {statement}")


if __name__ == "__main__":
    main()
