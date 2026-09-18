"""Apply the `G0.LEX-0` lexical evidence layer to the frozen Maqāyīs root table.

This runs the whole ladder end to end on hand-declared inputs and prints what
each stage does and does not establish::

    python examples/arabic/apply_lexical_layer_to_maqayis.py

**The roots here are declared by hand, not derived by a stemmer.** This tree has
no morphological analyser, and inventing one inside an example would make the
example the measurement. So each surface form arrives with a root and a written
`derivation_basis` saying who proposed it, and the run measures the *lexicon
lookup*, never the root proposal — `SurfaceIsNotRoot` is honoured by passing
through `DerivedMorphologicalCandidate` rather than by matching the raw surface.

**Coverage and discrimination are printed apart.** `LexicalTaskOutcome` answers
whether the lookup found an entry; `LexicalComparativeStanding` answers how it
stands against a weaker model. The weaker model here is a surface-indexed
comparator, so the standing is `NOT_COMPARABLE` — and that is a refusal to
compare two different indexing units, not a loss. Printing a single "accuracy"
would fuse exactly these two questions.

**Every normalization branch is run and none wins.** The price of each branch is
printed as the named roots it fuses, not as a count: under the bare-alif rule
`حدأ` and `حدا` become one entry, and a reader who will not pay that price reads
the `EXACT` column instead.

What this does not establish: no matched entry is a meaning
(`AMatchIsNotAMeaning`), no root entry is the surface word's signified
(`RootEvidenceIsNotSurfaceMeaning`), and Ibn Fāris's own text is quoted by
reference only (`QuotedDefinitionIsNotDerivedSignified`). The ladder stops at
`LexicalEvidenceCandidate`.
"""

from __future__ import annotations

from alghanem.arabic import (
    DerivedMorphologicalCandidate,
    LexicalAmbiguityRecord,
    LexicalNormalizationTrace,
    NormalizationBranch,
    SignifierCandidate,
    SurfaceOccurrence,
    derive_comparative_standing,
    derive_task_outcome,
)
from alghanem.arabic.maqayis_lexical_evidence import (
    BRANCH_RULE_CHAINS,
    MAQAYIS_INDEXING_UNIT,
    build_root_index,
    evidence_for_match,
    match_derived_root,
    read_root_evidence,
)
from alghanem.arabic.root_orthography_bridge import normalise_root

_DECLARED_CASES: tuple[tuple[str, str, str], ...] = (
    ("كَتَبَ", "كتب", "جذرٌ مُصرَّحٌ به يدويًّا في هذا المثال"),
    ("حَدَأَة", "حدأ", "جذرٌ مُصرَّحٌ به يدويًّا في هذا المثال"),
    ("سُنْدُس", "سندس", "جذرٌ مُصرَّحٌ به يدويًّا في هذا المثال"),
    ("زقفونة", "زقفن", "جذرٌ مُصرَّحٌ به يدويًّا، ولا يُنتظَر له مدخل"),
)

_SURFACE_COMPARATOR_INDEXING_UNIT = "surface"


def _signifier(raw_form: str, branch: NormalizationBranch) -> SignifierCandidate:
    chain = BRANCH_RULE_CHAINS[branch]
    normalized = raw_form
    destroys = ""
    if chain:
        normalized = normalise_root(raw_form, chain).after
        destroys = " ؛ ".join(rule.what_it_destroys for rule in chain)
    return SignifierCandidate(
        occurrence=SurfaceOccurrence(
            source_id="declared:example",
            occurrence_id=raw_form,
            raw_form=raw_form,
            source_position="declared",
            local_position=0,
        ),
        trace=LexicalNormalizationTrace(
            branch=branch,
            raw_form=raw_form,
            normalized_form=normalized,
            what_it_destroys=destroys,
        ),
    )


def main() -> None:
    entries = read_root_evidence()
    by_ref = {entry.entry_ref: entry for entry in entries}
    print(f"مداخلُ الجذور المقروءةُ من البايتات المُبصَّمة: {len(entries)}")
    print()

    for branch in NormalizationBranch:
        index = build_root_index(branch)
        print(f"== الفرع: {branch.value} ==")
        rule_names = tuple(rule.name for rule in index.rule_chain)
        print(f"   القواعدُ المُعمَلة: {rule_names or 'لا قاعدة'}")
        if index.fusions:
            for normalised, sources in index.fusions:
                print(f"   ثمنٌ — انصهر تحت «{normalised}»: {' و '.join(sources)}")
        else:
            print("   ثمنٌ — لا انصهار تحت هذا الفرع")

        for raw_form, proposed_root, basis in _DECLARED_CASES:
            derived = DerivedMorphologicalCandidate(
                signifier=_signifier(raw_form, branch),
                proposed_root=proposed_root,
                derivation_basis=basis,
            )
            matches = match_derived_root(derived, index)
            outcome = derive_task_outcome(
                reached_evidence=bool(matches), anchor_resolved=True
            )
            standing = derive_comparative_standing(
                lexicon_indexing_unit=MAQAYIS_INDEXING_UNIT,
                comparator_indexing_unit=_SURFACE_COMPARATOR_INDEXING_UNIT,
                lexical_reached=bool(matches),
                comparator_reached=False,
            )
            refs = tuple(match.matched_entry_ref for match in matches)
            print(
                f"   {raw_form} (جذرٌ مُقترَح: {proposed_root}) — "
                f"{outcome.value} / {standing.value} — مداخل: {refs or '—'}"
            )
            for match in matches:
                evidence = evidence_for_match(match, by_ref[match.matched_entry_ref])
                assert evidence.is_a_meaning is False
            if len(matches) > 1:
                record = LexicalAmbiguityRecord(
                    occurrence_ref=derived.signifier.occurrence.reference,
                    candidate_refs=refs,
                )
                print(
                    f"      تعدُّدٌ مُسجَّلٌ لا محسوم: {len(record.candidate_refs)} "
                    "مدخلًا، والقاعدةُ وحدَها أنتجته"
                )
        print()

    print("ما لم يُثبَت: الشاهدُ المعجميُّ ليس معنًى، والمطابقةُ ليست مدلولًا،")
    print("و`NOT_COMPARABLE` امتناعٌ عن مقارنة وحدتَي فهرسةٍ مختلفتين لا خسارة.")


if __name__ == "__main__":
    main()
