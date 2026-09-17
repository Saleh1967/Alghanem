"""Two declared models, one frozen case set, and no birth at the end of it.

A reference script with no authority: it certifies nothing, freezes nothing,
and issues no verdict. It runs the third path (`G0.EX`) end to end so that the
boundary can be watched rather than read --

    Candidate -> BoundRunRequest -> ExperimentalRun -> ObservedResult
    -> Contrast -> Replay -> ExperimentalEvidenceOffer
    -> [the acquisition chain, elsewhere]

Each request is bound to one frozen experiment's own content id *before* it
runs, because a domain may hold many experiments and an experiment id many
revisions: `SameDomain != SameExperiment`.

The two models are opaque strings on purpose. One declares fewer parts than the
other, and whether that difference matters is decided by which cases each fails
to account for -- never by which one is named more impressively. The last line
printed is the point of the whole script.

    python examples/kernel/contrast_two_models.py
"""

from __future__ import annotations

from typing import Final

from alghanem.kernel import (
    BirthExperimentSpecification,
    BirthExperimentSpecificationContentBinding,
    BirthQuery,
    BoundExperimentalRunRequest,
    CanonicalBirthExperimentSpecificationEncoder,
    DeclaredCaseSet,
    EvidenceMode,
    ExperimentalAuthority,
    ExperimentalCandidateDeclaration,
    ExperimentalCaseOutcomeVocabulary,
    ExperimentalContrastAuthority,
    ExperimentalOperationRef,
    ExperimentalReplayAuthority,
    ExperimentalRunBindingAuthority,
    ExperimentalRunContext,
    ExperimentalRunRecord,
    ExperimentalRunRequest,
    ModelContrastStatus,
    PreEvidenceSpecificationRegistry,
    ProjectionPoset,
    StructureHypothesis,
    Trace,
)

ACCOUNTED: Final = "ACCOUNTED:the declared model accounts for this case"
UNACCOUNTED: Final = "UNACCOUNTED:the declared model does not account for this case"

CASES: Final = DeclaredCaseSet(
    case_set_id="frozen-before-either-model-ran",
    case_ids=("case-1", "case-2", "case-3", "case-4"),
)
VOCABULARY: Final = ExperimentalCaseOutcomeVocabulary(
    accounted_token=ACCOUNTED, unaccounted_token=UNACCOUNTED
)
OPERATIONS: Final = (ExperimentalOperationRef("apply"),)


def request_for(model_ref: str) -> ExperimentalRunRequest:
    return ExperimentalRunRequest(
        candidate=ExperimentalCandidateDeclaration(
            candidate_id=f"candidate:{model_ref}",
            declared_origin_ref="origin:undeclared-genus",
            declared_scope="example-domain",
            declared_conditions=(
                "one process, no measurement provenance",
                "case set frozen before either model ran",
            ),
            declared_model_ref=model_ref,
        ),
        case_set=CASES,
        inputs=tuple((case_id, f"input:{case_id}") for case_id in CASES.case_ids),
        permitted_operations=OPERATIONS,
        case_outcome_vocabulary=VOCABULARY,
    )


def frozen_experiment() -> BirthExperimentSpecificationContentBinding:
    """One pre-evidence experiment, frozen before anything is run against it."""

    specification = BirthExperimentSpecification(
        experiment_id="experiment:is-a-richer-model-necessary",
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="example-domain",
        projection_poset=ProjectionPoset(
            ("count", "sequence"), (("count", "sequence"),)
        ),
        birth_query=BirthQuery(
            "query",
            StructureHypothesis("structure", "a richer structure is necessary"),
            "sequence",
        ),
        residual_definition_id="residual",
        residual_definition="a case the declared model does not account for",
        closure_criterion_id="closure",
        closure_criterion="the weaker model leaves a case unaccounted",
        evidence_requirements="exhaustive reading over the frozen case set",
    )
    frozen = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(specification)
    )
    return BirthExperimentSpecificationContentBinding(specification, frozen)


def model(unaccounted: frozenset[str]) -> object:
    """A model that fails to account for exactly the named cases.

    The operation is reached through the capability the authority issued for
    this case, which refuses an unpermitted one before it can run and writes
    the run's own operation event itself.
    """

    def implementation(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        case_id = input_content.removeprefix("input:")
        token = UNACCOUNTED if case_id in unaccounted else ACCOUNTED
        context.invoke("apply", lambda: None)
        return token, Trace((f"read:{case_id}",))

    return implementation


def run() -> ModelContrastStatus:
    authority = ExperimentalAuthority(authority_id="example-laboratory")
    binding_authority = ExperimentalRunBindingAuthority(authority_id="example-binding")
    experiment = frozen_experiment()
    simpler: BoundExperimentalRunRequest = binding_authority.bind(
        binding_id="binding:model-a",
        request=request_for("model-a:fewer-declared-parts"),
        binding=experiment,
    )
    richer: BoundExperimentalRunRequest = binding_authority.bind(
        binding_id="binding:model-b",
        request=request_for("model-b:more-declared-parts"),
        binding=experiment,
    )

    record_a: ExperimentalRunRecord = authority.run(
        run_id="run:model-a",
        bound_request=simpler,
        implementation=model(frozenset({"case-3", "case-4"})),  # type: ignore[arg-type]
    )
    record_b: ExperimentalRunRecord = authority.run(
        run_id="run:model-b",
        bound_request=richer,
        implementation=model(frozenset({"case-4"})),  # type: ignore[arg-type]
    )

    contrast = ExperimentalContrastAuthority(authority_id="example-contrast").observe(
        observation_id="contrast:a-vs-b", record_a=record_a, record_b=record_b
    )
    replay = ExperimentalReplayAuthority(authority_id="example-replay").observe(
        observation_id="replay:model-b",
        records=(
            record_b,
            authority.run(
                run_id="run:model-b-again",
                bound_request=richer,
                implementation=model(frozenset({"case-4"})),  # type: ignore[arg-type]
            ),
        ),
    )

    print(f"case set: {CASES.case_set_id} -> {', '.join(CASES.case_ids)}")
    print(
        f"{contrast.model_ref_a} left unaccounted: "
        f"{', '.join(contrast.cases_unexplained_by_a) or '-'}"
    )
    print(
        f"{contrast.model_ref_b} left unaccounted: "
        f"{', '.join(contrast.cases_unexplained_by_b) or '-'}"
    )
    print(
        f"closed only by the richer model: {', '.join(contrast.cases_closed_only_by_b)}"
    )
    print(f"contrast status: {contrast.status.name}")
    print(
        "replay: outputs identical "
        f"{replay.outputs_identical}, traces identical {replay.traces_identical}, "
        f"reproducibility proved {replay.proves_reproducibility}"
    )
    print(
        "case-4 survived both models, and survived nothing else: "
        "it is an observation, not a certified residual"
    )
    print(
        "what this run conferred: "
        f"birth={record_b.confers_birth}, validity={record_b.confers_validity}, "
        f"necessity={contrast.confers_necessity}, "
        f"constitutional evidence={record_b.confers_constitutional_evidence}"
    )
    print(
        "NO BIRTH OCCURRED: a better experimental fit is not a birth, and this "
        "result may enter the constitutional path only as an offered payload "
        "the acquisition chain must still ingest."
    )
    return contrast.status


def main() -> None:
    status = run()
    assert status is ModelContrastStatus.B_CLOSES_STRICT_SUPERSET


if __name__ == "__main__":
    main()
