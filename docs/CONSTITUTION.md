# Alghanem Kernel Constitution

These are the initial laws of the language-agnostic kernel:

| Law | Status | Kernel v0.1 scope |
| --- | --- | --- |
| Explicit domain | ENFORCED | Anchors require a non-blank domain. When an operation declares a source domain, it must match the source anchor's domain. When an operation declares a target domain, it must match the target anchor's domain. |
| Explicit target anchor | ENFORCED | No successful transition without an explicitly declared target anchor; a default derived from the source anchor never satisfies admission. Identity-preserving transformations require source anchor = target anchor. Branch-birth claims require source anchor != target anchor, and branch provenance must bind the actual source and target anchors. |
| Evidence present | ENFORCED | Successful transitions require at least one evidence record. |
| Evidence-to-claim binding | ENFORCED | Successful-transition evidence is structurally bound by claim id to the transition's own claim. This is not proof sufficiency. |
| G0.C.1 minimal claim constitution | ENFORCED_AT_CONTENT_ENCODER | See **G0.C.1 — Minimal claim constitution** below. |
| Structural admission boundary | ENFORCED | Candidates become `StructurallyAdmissibleTransition`s only through `StructuralAdmissionGate`. The gate is a controlled construction boundary inside the Python API, not a cryptographic or security-grade mechanism, and it certifies structural completeness only — not evidential sufficiency, domain-transition authority, or layer authority. Structural admission must not be conflated with a future `LicensedTransition`: `Representability != Licensability` and `StructuralValidity != EvidentialSufficiency`. |
| Claimed kind vs. certified outcome | ENFORCED | Every candidate declares what it represents via `TransitionKind` (`IDENTITY_PRESERVATION_CLAIM` or `BRANCH_BIRTH_CLAIM`). Candidates do not carry certified outcomes or decision statuses (`Candidate != Decision`); a candidate cannot decide or certify its own outcome. `StructuralAdmissionGate` evaluates the candidate and yields a `StructuralAdmissionDecision` with a status (`ADMITTED`, `BLOCK`, `DEFER`, `UNDEFINED`). `CertifiedOutcome` (`IDENTITY_PRESERVING_TRANSFORMATION`, `CERTIFIED_BRANCH_BIRTH`) is strictly reserved for the final certification stage (`CertifiedTransition`), not asserted by structural admission alone. In particular, `target_anchor == anchor` is a structural check, not proof: `AnchorEquality != ProvenIdentityPreservation`. Declaring a name in `preserved`/`changed` is not proof it was extracted from `before_state`/`after_state`: `DeclaredInvariant != VerifiedInvariant`. |
| Declared invariant presence | ENFORCED | Identity-preserving transformations require a declared invariant. |
| Verified invariant preservation | ENFORCED_AT_INVARIANT_GATE | Structural admission issues an opaque `admission_id`; verification provenance binds that exact transition identity and the sealed registry's `registry_snapshot_id`, in addition to claim, anchors, and trace. `InvariantVerificationGate.assess_all_preserved` and `InvariantVerificationBundle` require exactly one successful verification for every declared preserved component; both `InvariantVerificationDecision` and `InvariantVerificationBundle` are gate-issued only, mirroring each other (`VerificationDecision must be gate-issued`, and `InvariantVerificationBundle` now enforces this with its own private token), so a caller cannot hand-build a `VERIFIED` decision or a bundle, and a later layer that trusts either cannot be fooled by a self-declared result. An `InvariantSpec`'s `extractor_id` is only a claim, never a grant of authority: `InvariantExtractorRegistry.authorize` binds a trusted, registry-owned `RegisteredInvariantDefinition` (`domain`, `component`, `invariant_id` -> exactly one `extractor_id`), and `InvariantVerificationGate.verify` resolves only through `SealedInvariantExtractorRegistry.resolve_authorized`, which raises `UnauthorizedExtractorError` unless that exact extractor id is authorized for that exact scope (`Candidate/Caller does not own verifier selection authority`). `DEFER` is a real, distinct status: epistemic non-answers (unregistered or unauthorized extractor, failing extractor, ambiguous non-`bool` comparison) are `DEFER`, a disproved invariant is `BLOCK`, and internal/programming errors are caught into neither -- they propagate. `assess_all_preserved` evaluates every declared component independently rather than stopping at the first untestable one, and aggregates with strict precedence `BLOCK` (any disproved component) > `DEFER` (else, any untestable component) > `VERIFIED`, recording disproved (`failed_components`) and untestable (`deferred_components`) components as separate, sorted sets so the aggregate judgment never depends on the order components were declared in (`Known falsification dominates epistemic deferral`). Failures remain in an auditable `InvariantVerificationDecision`, and the convenience API raises a typed error carrying that decision. Registration authority, authorization authority, and snapshot resolution authority are three distinct concerns, but none of them is an evidential authority license. `StructurallyAdmissibleTransition.transition_projection_fingerprint` and `SealedInvariantExtractorRegistry.registry_projection_hash` are corroborating, deterministic *projections* of part of the transition/registry content, recorded alongside the opaque `admission_id`/`registry_snapshot_id` (`OccurrenceIdentity != ContentIdentity` for both transitions and registries) -- they are explicitly **not** canonical content identity or reproducibility proofs (each omits significant structurally-relevant content; see their docstrings), and must not be used to promote epistemic status. A full `CanonicalTransitionManifest`/`ExtractorRegistration` content-identity and reproducibility design is deferred to a dedicated follow-up. Verification is not yet wired into `StructuralAdmissionGate` or evidential sufficiency; `No epistemic promotion` remains `DECLARED_DEFERRED`. |
| Preserved/changed separation | ENFORCED | Preserved and changed components are non-blank, unique, and disjoint. |
| Declared change | ENFORCED | Every successful transition has a result and a changed component matching the operation's declared change. |
| Branch birth separation | ENFORCED | A branch-birth claim is distinct from identity preservation and requires origin provenance whose preserved components exactly equal its declared preserved components, plus a distinct branch anchor equal to the target anchor. |
| Non-admitted decisions | ENFORCED | `BLOCK`, `DEFER`, and `UNDEFINED` are external decision statuses (`StructuralDecisionStatus`), never properties of a candidate or `StructurallyAdmissibleTransition`s. |
| Non-success audit | ENFORCED | No non-success decision without reviewable audit information. Every non-success decision preserves its trace, its residuals, and a non-blank structural reason; the assessed candidate is preserved when one exists, and the audit's trace and residuals are then bound to that candidate's own history — no history without provenance from the assessed attempt. Without a candidate, the audit owns its trace and residuals directly. Non-success decision histories must not be erased: `require_admitted` raises `StructuralAdmissionError`, which carries the complete non-admitted decision. An optional `DecisionReasonCode` provides a coarse-grained, machine-auditable classification alongside the human-readable `reason`; it does not replace `reason` or carry additional structural authority. |
| Residual presence | PARTIALLY_ENFORCED | Residual records cannot be blank when present and are preserved in non-success audits, but residual provenance is not defined and residuals are not interpreted or ranked. |
| No epistemic promotion | DECLARED_DEFERRED | Claim/evidence binding is structural only; evidential sufficiency is not implemented. |
| No partial invariant coverage | DECLARED_DEFERRED | No transition may be promoted as preserved from partial invariant coverage; complete invariant verification is available as a separate gate before evidential sufficiency. |
| No higher-layer repair | DECLARED_DEFERRED | Higher layers may not repair invalid lower-layer transitions, but layer authority is not defined. |
| Canonical transition content snapshot | ENFORCED_AT_CONTENT_ENCODER | `CanonicalTransitionEncoder` is the sole issuer of `CanonicalTransitionManifest` and `TransitionContentIdentity`. The manifest preserves immutable canonical bytes for every structural transition field, including branch-origin provenance; occurrence-only `admission_id` and projection fingerprint are explicit exclusions. Its SHA-256 value is a digest reference, not proof of canonical-byte equality. Canonical values accept only exact built-in types, distinguish list from tuple and bytes from bytearray, preserve raw Unicode code points without normalization, encode finite floats as IEEE-754 binary64, and reject unsupported values and cycles. `preserved`, `changed`, and branch provenance components are sets; trace, evidence, and residuals are ordered sequences. Schema coverage rejects unaccounted structural fields. |
| G0.RC.1 certified residual constitution | DECLARED_DEFERRED_CONTRACT_ONLY | `ResidualCertificationCandidate` accepts one existing `BirthAssessmentContentBinding`, not independent definition and content-id values. Its residual definition and content identity are derived from the binding, which verifies byte-exact equality against the sealed registry and frozen pre-evidence experiment. It is not an authority-issued certification: `FrozenFactorRef`/`BornBridgeRef` remain caller-constructible contract references until G0.FA.1, and reconstruction-attempt and comparison authorities are absent. `ResidualDefinitionSpec != ObservedDifference != CertifiedResidual != LegacyResidual` remains a declared distinction only. G0.RC.1 must not be marked enforced until those authorities exist. Residual typing and structural expansion remain deferred to G0.RT.1 and G0.SE.1. |
| G0.FA.1 authority-issued frozen reference | DECLARED_DEFERRED | `FrozenFactorRef` and `BornBridgeRef` validate reference shape and exact membership, but successful construction does not prove that a factor was frozen. A future freeze authority must issue trusted references before residual certification can claim `Freeze(F) -> Residual(F, observation)`. |
| G0.BV.1 authority-issued birth verdict | DECLARED_DEFERRED_CONTRACT_ONLY | `BirthVerdictStatus` remains future vocabulary only. No runtime authority may convert caller-declared assessment status into a verdict. A future assessment authority must first execute authorized evaluators and preserve the `BirthCandidate`/`IndependentClosure` boundary before a verdict authority can issue `BIRTH_IN_SCOPE`, `NO_BIRTH_IN_SCOPE`, or `DEFER_IN_SCOPE`; Freeze and residual certification remain separate later authorities. `BIRTH_IN_SCOPE` and `NO_BIRTH_IN_SCOPE` therefore remain unreachable at runtime; only the deferral branch is now executable, under G0.BV.1a below. |
| G0.BV.1a gate-derived scoped deferral | ENFORCED_AT_VERDICT_GATE | The first executable authority boundary for a `BirthVerdictStatus`, copying the register -> seal -> gate shape already enforced by `EvidenceAcquisitionAuthority`, `InvariantVerificationGate`/`SealedInvariantExtractorRegistry`, and `BirthEvaluatorExecutionGate`. `BirthVerdictScopeRegistry.register` is the sole issuer of an `AuthorizedBirthVerdictScope` and requires a verified `BirthExperimentSpecificationContentBinding`; every scope condition (`experiment_content_id`, `domain`, `experiment_id`, `revision_id`, `revision_sequence`, `evidence_mode`, `test_model`) is derived from that binding, never independently caller-supplied. Only `BirthVerdictScopeRegistry.seal` produces a `SealedBirthVerdictScopeRegistry`, and only `BirthVerdictGate.assess` produces a `BirthVerdictDecision`, which is not caller-constructible. `CallerDoesNotOwnVerdictAuthority` is enforced by the signature, not only by prose: `assess` accepts no status, reason, or closure claim, and derives the status from the request's own frozen projection poset. `DeferredVerdict != Birth`: the gate's codomain is currently the single value `DEFER_IN_SCOPE`, because `BIRTH_IN_SCOPE`/`NO_BIRTH_IN_SCOPE` require a gate-issued `IndependentClosureDecision` that no authority here can issue; the recorded reason distinguishes which obstacle applied (unresolved incomparable competitors, an open prerequisite cone, or the missing closure authority). This stage issues no `Freeze`, no `E0` mapping, and no `TraditionalName`; a `DEFER_IN_SCOPE` decision may not be frozen. `AuthorizedScope != AssessedEvidence`: no evaluator is executed, no residual measured, and no weaker model exhausted here. |
| G0.IC.1a gate-derived comparability closure | ENFORCED_AT_CLOSURE_GATE | Closes exactly one conjunct of the `IndependentClosure` that G0.BV.1a declared missing, and refuses the rest. The same register -> seal -> gate shape applies: `ClosureScopeRegistry.register` is the sole issuer of an `AuthorizedClosureScope` (every condition derived from a verified `BirthExperimentSpecificationContentBinding`), `ClosureScopeRegistry.seal` alone produces a `SealedClosureScopeRegistry`, and `IndependentClosureGate.assess` alone produces an `IndependentClosureAssessment`. `CallerDoesNotOwnClosureAuthority`: `assess` accepts no status, reason, or comparability claim, and reads exactly one thing -- the request's own frozen `ProjectionPoset`. Because comparability over a finite frozen projection set is exhaustively decidable, this status is genuinely two-valued and both `COMPETITION_RESOLVED_IN_POSET` and `COMPETITION_UNRESOLVED_IN_POSET` are reachable. `AbsentRelation != DeclaredIncomparability`: a frozen poset cannot distinguish a declared incomparability from a relation never determined, so both are counted as unresolved competition and `COMPETITION_RESOLVED_IN_POSET` is reachable only when every other projection is strictly related to the test model; ignorance is never read as resolution. `ComparabilityClosure != IndependentClosure` is the boundary this stage does not cross: `NoRicherStructureBeforeLowerOpenResidualClosure` makes an empty competitor set only one conjunct, and the others -- a residual surviving under `NoBirthWithoutResidualOrFormalNecessity` and an exhausted licensed weaker model set under `NoBirthBeforeLicensedWeakerExhaustion` -- have no authority here and cannot be obtained by copying any existing pattern, because both require evaluating evidence content that `G0.BA.1a` explicitly does not evaluate (`InputProvenance = DECLARED_DEFERRED`). `IndependentClosureAssessment.is_independent_closure` is therefore `False` unconditionally, even on the resolved branch. `ComparabilityAssessment != Verdict`: `BirthVerdictGate` is deliberately not wired to consume this assessment, since consuming it would imply the missing conjuncts were satisfied. This stage issues no `BirthVerdict`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.IC.1b evidence-derived weaker-model closure outcome | ENFORCED_AT_CLOSURE_GATE | Closes the first of the two conjuncts AIM-K3 names, and only for one weaker model at a time. Nothing new is invented: `ClosureCriterionSpec.supported_statuses` already declares the closed three-member vocabulary of `Close(W_i, R)`, `BirthExperimentSpecification.frozen_weaker_models` already derives the prerequisite cone from the frozen projection poset before any evidence exists, and `ProvenanceBoundEvaluatorExecutionRecord` (G0.BA.1b) already proves `EvaluatorExecutedOnEvidence`. The single missing step was that nothing related an evaluator's `output_content` -- a plain string -- to a member of that closed vocabulary. `DeclaredClosureOutcomeVocabulary` is that relation, declared as data rather than computed as a judgement: it must cover every `ClosureAssessmentStatus` member exactly once, must not bind one token to two outcomes, and refuses a token carrying surrounding whitespace because matching is exact. The same register -> seal -> gate shape applies: `ClosureOutcomeVocabularyRegistry.register` is the sole issuer of an `AuthorizedClosureOutcomeVocabulary` and requires a verified `BirthAssessmentContentBinding`, so the criterion spoken for is content-frozen in a sealed semantics registry and not merely named; `seal` alone produces a `SealedClosureOutcomeVocabularyRegistry`; and `WeakerModelClosureGate.assess` alone produces a `WeakerModelClosureCertificate`. `CallerDoesNotOwnClosureOutcome`: `assess` accepts no status, reason, or outcome claim, and takes exactly two parameters. `ExactTokenOrRefusal`: the output is matched by exact string equality, with no trimming, case folding, prefix or substring match, nearest match, or default -- an unrecognized output is refused by model id and is never read as `DEFER`, because silently reading ignorance as a declared outcome is precisely the failure this gate exists to prevent. The gate also refuses a record executed under any role other than `WEAKER_MODEL`, and a target outside the derived frozen prerequisite cone. All three declared outcomes are reachable. Four claims remain refused. `LocalClosureOutcome != WeakerModelExhaustion`: a certificate speaks for exactly one model, nothing here aggregates the cone or checks its coverage, and `is_weaker_model_exhaustion` is `False` unconditionally. `WeakerModelClosure != IndependentClosure`: the residual-survival conjunct has no authority here and the comparability conjunct belongs to G0.IC.1a, so `is_independent_closure` is `False` on every branch, `IndependentClosureAssessment` is untouched, and this stage is deliberately wired to neither it nor `BirthVerdictGate`. `DeclaredVocabularyIsNotProvenSemantics`: freezing the token-to-status map before the gate runs prevents a map tailored to an output already seen, and proves nothing about why the evaluator emitted that token. `SealedBeforeAssessmentIsNotSealedBeforeEvidence`: no authority in this repository timestamps a seal against an evidence acquisition run, so the vocabulary is proven frozen relative to the gate, not relative to the evidence. This stage issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.IC.1c derived weaker-model exhaustion | ENFORCED_AT_CLOSURE_GATE | Aggregates G0.IC.1b's per-model certificates into the second conjunct of `IndependentClosure`, and nothing beyond it. The licensed set is not invented here: `BirthExperimentSpecification.frozen_weaker_models` already derives the cone from the frozen projection poset before any evidence exists, so how many models must be answered is fixed in advance and cannot be trimmed to fit the certificates that happen to exist. `MalformedRequestIsNotNonExhaustion`, copied from `InvariantVerificationGate.assess_all_preserved`: certificates that do not exactly cover the cone, that name one model twice, or that name a model the frozen poset never licensed are a malformed request and raise, because an unevaluated model is ignorance and reading ignorance as a failure to close is exactly how a fabricated exhaustion would be manufactured. `OneRequestOnly`: every certificate must be bound to the same `BirthAssessmentRequest` object, since certificates from different requests describe different evidence. `CallerDoesNotOwnExhaustion`: `WeakerModelExhaustionGate.assess` accepts no status and no reason, takes exactly two parameters, reads every certificate rather than stopping at the first, and derives the status under a fixed precedence -- `WEAKER_MODEL_CLOSES_RESIDUAL` > `EXHAUSTION_UNDETERMINED` > `LICENSED_WEAKER_MODELS_EXHAUSTED` -- so a known `CLOSE` is never erased by an unrelated `DEFER` (`False and Unknown == False`) and the aggregate does not depend on certificate order. All three statuses are reachable, and `outcome_counts` is a derived property covering every declared outcome including zeros, never a written field. Claims still refused: `WeakerModelExhaustion != IndependentClosure` -- the surviving-residual conjunct has no authority in this repository and comparability belongs to G0.IC.1a, so `is_independent_closure` is `False` on every branch here too, `IndependentClosureAssessment` is untouched, and this stage is wired to neither it nor `BirthVerdictGate`. `WeakerModelClosesResidual != NoBirthVerdict`: the `CLOSE` branch is the shape of an argument against birth in this scope, not that verdict. `CoverageIsNotCorrectness` and `FrozenConeIsDeclaredNotProven`: the gate proves every licensed model was evaluated on this request's own authorized evidence and reported a declared outcome, not that those outcomes are true or that the poset licensed the right models. `SameRequestIsNotSameEvidenceRun`: sharing one request proves one frozen experiment and one evidence snapshot, not any ordering or co-execution of the evaluators. This stage issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.IC.1d evidence-derived residual survival outcome | ENFORCED_AT_CLOSURE_GATE | Reads the third and last conjunct of `IndependentClosure` for one witness, and stops there. Nothing new is invented: `ResidualDefinitionSpec` already declares the residual whose survival is at stake, its `supported_statuses` declares the closed three-member `ResidualSurvivalStatus` vocabulary exactly as `ClosureCriterionSpec.supported_statuses` declares `Close(W_i, R)`'s, and `ProvenanceBoundEvaluatorExecutionRecord` (G0.BA.1b) already proves `EvaluatorExecutedOnEvidence`. The missing step was the same one G0.IC.1b closed for closure outcomes: nothing related an evaluator's `output_content` -- a plain string -- to a member of that closed vocabulary. `DeclaredResidualSurvivalVocabulary` is that relation, declared as data rather than computed as a judgement: it must cover every `ResidualSurvivalStatus` member exactly once, must not bind one token to two outcomes, and refuses a token carrying surrounding whitespace because matching is exact. The same register -> seal -> gate shape applies: `ResidualSurvivalVocabularyRegistry.register` is the sole issuer of an `AuthorizedResidualSurvivalVocabulary` and requires a verified `BirthAssessmentContentBinding`, so the residual spoken for is content-frozen in a sealed semantics registry and not merely named; `seal` alone produces a `SealedResidualSurvivalVocabularyRegistry`, resolving only by the exact `(domain, residual_id)` scope; and `ResidualSurvivalGate.assess` alone produces a `ResidualSurvivalCertificate`. `CallerDoesNotOwnResidualSurvival`: `assess` accepts no status, reason, or survival claim, and takes exactly two parameters. `ExactTokenOrRefusal`: the output is matched by exact string equality, with no trimming, case folding, prefix or substring match, nearest match, or default -- an unrecognized output is refused by residual id and is never read as `DEFER`. The gate also refuses a record executed under any role other than `RESIDUAL_DEFINITION`, and a target that is not the request's own frozen `residual_definition_id`. `MixedModeNeedsTwoScopedWitnesses`: `evidence_mode` is read from the frozen experiment and never from the caller, and a `MIXED` experiment is refused by name, because that mode is an explicitly typed scoped pair `<(D_emp, S_emp), (D_formal, S_formal)>` and no authority here proves those declared scopes or `NoCrossSubstitution(D_emp, D_formal)`; a named refusal is safer than one certificate a later reader could take as having satisfied both modes. All three declared outcomes are reachable. Claims still refused. `ResidualSurvivalOutcome != IndependentClosure`: the three conjuncts are now each derived on their own -- comparability by G0.IC.1a, exhaustion by G0.IC.1c, survival here -- but composing them is a separate question with no authority in this repository, so `is_independent_closure` is `False` on every branch, `IndependentClosureAssessment` is untouched, and this stage is wired to neither it nor `BirthVerdictGate`. `DoesNotSurvive != NO_BIRTH_IN_SCOPE`: a residual failing to survive is the shape of an argument against birth in this scope, not that verdict. `SurvivalReadIsNotMeasuredReplicatedResidual`: in `EMPIRICAL` mode `NoBirthWithoutResidualOrFormalNecessity` requires a *measured* residual that survives every licensed weaker projection and replicates in a second independent measurement run, and nothing here inspects provenance genus or knows of a second run. `FormalNecessityIsNotProvedHere`: in `FORMAL` mode a declared outcome is read, not an exhaustive proof over the declared closed domain verified. `DeclaredVocabularyIsNotProvenSemantics` and `SealedBeforeAssessmentIsNotSealedBeforeEvidence` are inherited unchanged from G0.IC.1b. `OneWitnessIsNotResidualCertification`: G0.RC.1 remains deferred exactly as written, `ResidualCertificationCandidate` is untouched, and no freeze, reconstruction, or comparison authority is created here. This stage issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.IC.1e composed independent-closure decision | ENFORCED_AT_CLOSURE_GATE | Composes the three conjunct readings G0.IC.1a, G0.IC.1c and G0.IC.1d each derived on their own, and claims nothing beyond what they say. Nothing new is read: the gate opens no evidence, executes no evaluator, and inspects no frozen poset, because every input is already a gate-issued reading (`ThreeReadingsAreNotAFourth` -- a composition that re-derived a conjunct would be a second authority over a question already answered, and the two answers could disagree). `IndependentClosureCompositionGate.assess` alone produces an `IndependentClosureDecision`, and `CallerDoesNotOwnComposition`: it takes exactly three parameters -- the comparability assessment, the exhaustion assessment and the survival certificate -- and no status, reason, or closure claim. `OneRequestOrRefusal`: the three readings must speak for the same `BirthAssessmentRequest` by object identity, exactly as G0.IC.1c requires of its certificates, and the survival reading must carry that request's own authorized evidence snapshot; readings of different requests are refused, never composed. The enumeration was performed before the module was written: comparability is two-valued and exhaustion and survival are three-valued, so there are exactly `2 x 3 x 3 = 18` combinations, and each conjunct falls into exactly one of three roles -- satisfied (`COMPETITION_RESOLVED_IN_POSET`, `LICENSED_WEAKER_MODELS_EXHAUSTED`, `SURVIVES`), refuting (`WEAKER_MODEL_CLOSES_RESIDUAL`, `DOES_NOT_SURVIVE`), or undetermined (`EXHAUSTION_UNDETERMINED`, `DEFER`, `COMPETITION_UNRESOLVED_IN_POSET`). `UnresolvedComparabilityIsIgnoranceNotRefutation`: comparability has no refuting branch at all, because G0.IC.1a already resolves `AbsentRelation != DeclaredIncomparability` conservatively, so reading its unresolved branch as a refutation would manufacture knowledge out of silence. Aggregation follows the precedence already enforced twice in this kernel: `CLOSURE_REFUTED_IN_SCOPE > CLOSURE_UNDETERMINED_IN_SCOPE > CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION`, with refuted and undetermined conjuncts tracked in separate fields, as `InvariantVerificationDecision` tracks `failed_components` and `deferred_components`, and reported in a fixed conjunct order independent of caller order. Of the 18 combinations, 10 are refuted, 7 are undetermined, and exactly 1 -- resolved comparability, exhausted licensed weaker models, and a surviving residual -- reaches the third status. Claims still refused. `SatisfiedConjunctsIsNotIndependentClosure`: even that one combination yields `is_independent_closure == False`, because the three conjuncts hold *as read* and reading is all that happened -- `OneWitnessIsNotResidualCertification` (G0.RC.1 is deferred, so no certified residual exists to close over), `SurvivalReadIsNotMeasuredReplicatedResidual`, and `CoverageIsNotCorrectness` with `FrozenConeIsDeclaredNotProven` each remain open by name. The status name states exactly what was reached and what it is pending on, rather than overstating it, so AIM-K3 is narrowed by name rather than declared met. `CompositionIsNotAVerdict`: this stage is deliberately not wired to `BirthVerdictGate`, the readings it consumes keep their own `False` constants, and `ClosureRefutedInScope != NO_BIRTH_IN_SCOPE`. It issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| A0.CD.1 usuli comprehension-defect vocabulary | DOCUMENTED_CLASSIFICATION_ONLY | An Arabic-layer classification with no authority whatsoever. `ComprehensionDefectCause` is the closed five-value vocabulary the usuliyyun counted as the causes of defective comprehension -- `اشتراك`, `نقل`, `مجاز`, `إضمار`, `تخصيص` -- with the explicit non-member value `لا_ينطبق`; any other text, misspelling or invented term, is rejected rather than folded onto the nearest member. Its priority order at conflict is `تخصيص > مجاز = إضمار > نقل > اشتراك`, and each of the ten pairwise comparisons carries its own textual argument and named source in `PRIORITY_ARGUMENTS`, so no rank rests on estimation; the `مجاز = إضمار` tie adopts the view that counts `إضمار` a `مجاز` by omission and records the competing ordering rather than hiding it. `DeclaredDefectCause != AssessedRelation`: an optional per-reading `سبب_الإخلال_بالفهم` on an external audit card is validated and reported as `تصنيف_أسباب_الإخلال_بالفهم` and nothing else -- it never enters the derived `BirthExperimentSpecification`, never changes `نتيجة_التدقيق_الخارجي`, and neither `IndependentClosureGate` nor `BirthVerdictGate` reads it; removing every classification leaves all other reported fields identical. `FixedTextAmbiguity != ReadingMultiplicity != TransmissionWeakness` is the declared scope limit: the five causes address ambiguity of meaning in a fixed text, not disagreement over the recited wording and not the strength of a report's transmission. Partial applicability is therefore an expected structural result, not an implementation gap: across the four example cards only three of eight competing readings are described by a cause (`تخفيف_إن_وضمير_شأن` as `إضمار`; the `مَن`/`ما` readings of `man_2_255` and `maa_2_197` as `اشتراك`), and the remaining five are declared `لا_ينطبق` rather than forced into a label. |
| A0.PP.1 probe preregistration | ENFORCED_AT_PROBE_PREREGISTRATION | An Arabic documentation-layer boundary with no kernel authority, closing the gap between a *recorded past* probe specification and an *enforced pre-evidence* one: `FrozenProbeSpecification != EnforcedPreEvidenceSpecification`. `FrozenFollowupProbeSpecification` carries no result field at all, checked at import against its own dataclass fields rather than asserted in prose. `PreEvidenceProbeSpecificationRegistry.freeze` is the sole issuer of a `FrozenPreEvidenceProbeManifest` and refuses different content re-frozen under one `(experiment_id, revision_id, revision_sequence)` identity; `FollowupProbeSpecificationContentBinding` re-encodes the live specification and compares canonical bytes, so post-freeze drift cannot be bound. `NoResultWithoutPriorSpecification`: a `ProbeResultAttachment` is unconstructible without that binding, and construction fails -- never warns -- on a feature outside the frozen set, a selection criterion or stopping rule other than the frozen ones, or a `k` outside the frozen range, which is what makes `NoOracleTuningBeforeFreeze` structural instead of remembered. `EvidenceGenus` is deliberately two-valued (`DISTRIBUTIONAL`, `MORPHO_FUNCTIONAL`) with no `MIXED`: mixing genera requires an explicit `(E_D, E_M, CompositionRule)` composition contract that does not exist yet, and `MORPHO_FUNCTIONAL` is declared-but-unconstructible because no frozen morphological feature vocabulary has been born. `ProbeResultAttachment != BirthVerdict` and `FrozenFollowupProbeSpecification != BirthExperimentSpecification`: this registry is a local documentation-layer freeze, not a kernel authority; no `Freeze`, no `E0`, and no kernel gate reads it. |
| A0.PP.1a phase-2 question stays open | DOCUMENTED_OPEN_QUESTION | `Phase2OpenQuestion` records the question the recorded negative result raises, with no answer, verdict, conclusion, resolution, or decision field, checked at import. It requires all three hypotheses rather than a false dichotomy: (A) only the five current features are insufficient; (B) the `اسم`/`فعل`/`حرف` division is not a surface-distributional kind at all, so no enlargement of that evidence genus recovers it; (C) the division becomes distributionally recoverable only after lower structural variables (boundary, position, morphological transformation) are themselves born as licensed carriers, per `Closure_L -> Handoff_L -> Birth_{L+1}`. `RecordedQuestion != Answer`: dropping or repeating a hypothesis is refused, and no authority here may resolve any of the three. |
| A0.PP.1b one canonicalization, no authority transfer | ENFORCED_AT_CANONICAL_PRIMITIVE | `Canonicalization != Authority`. `src/alghanem/canonical_content.py` is the single place canonical bytes and digests are produced, used by both the kernel's content encoders and the Arabic preregistration layer, because two copies of a canonicalization rule are two rules that can silently drift apart. It encodes and hashes and decides nothing: it has no notion of a specification, experiment, freeze, verdict, or birth, so a layer importing it inherits a deterministic byte encoding and no permission from any other importing layer. |
| A0.PP.2 four-rank readiness ladder | ENFORCED_AT_READINESS_RECORD | `RecordedStatusProse != EnforcedReadinessRecord`, one level above `FrozenProbeSpecification != EnforcedPreEvidenceSpecification`: the phase-2 status table lived only as prose in a pull-request body, where it could later be read as an enforced fact while being guarded by nothing. `src/alghanem/arabic/readiness_rank.py` makes it a record that refuses false combinations at construction. Four independent closed vocabularies, deliberately not one enum with four values, because a single ladder implies a false total order in which a higher rank looks entailed by its position rather than by a prior condition: `StructuralReadiness` (`NOT_BUILT`, `BUILT_AND_CHECKED`), `SpecificationFreeze` (`NOT_YET_FROZEN`, `FROZEN`), `MeasurementProgress` (`NOT_STARTED`, `STARTED`, `COMPLETED`), `QuestionStatus` (`OPEN`, `CLOSED_BY_FROZEN_EXPERIMENT`). Four is the minimum sufficient count, not an assumed one: merging structure with freeze would make freezing an automatic promotion of a checked build, though a checked build with no frozen future specification is exactly today's state; merging freeze with measurement would erase the difference between a frozen specification that binds every later measurement and no specification at all; merging measurement with the question would make a completed measurement a settlement, though completion settles nothing without a specification frozen before its evidence. Implication runs one way only, as a prior condition and never its converse: measurement beyond `NOT_STARTED` requires `FROZEN`, `FROZEN` requires `BUILT_AND_CHECKED`, and closure requires `COMPLETED`; a frozen specification with no measurement yet, and a completed measurement with an open question, are both admissible states now. `CLOSED_BY_FROZEN_EXPERIMENT` is declared in the vocabulary rather than omitted, and is unconstructible today under the same discipline as `EvidenceGenus.MORPHO_FUNCTIONAL` -- refused at construction of any record, not only in the module-level one, since no birth gate or verdict authority exists here to issue a closure, and refusing it only in one place would leave every other record free to write it. That refusal is checked before the general implication message, so a refusal grounded in "no issuing authority exists" is not read as the shallower "measurement is not finished". Each rank carries its own non-blank justification, and the single module-level `PHASE2_READINESS` takes its `question_id` from `PHASE2_OPEN_QUESTION` rather than copying the string, with an import-time guard against openness drift between the two. `ReadinessRankRecord != BirthVerdict` and `SpecificationFreeze != Freeze`: the record carries no answer, verdict, or birth field (checked at import against its own dataclass fields), and no kernel gate reads it, which a test enforces by scanning every `kernel/` module. |
| A0.PP.3 cross-project vocabulary import contract | ENFORCED_AT_IMPORT_CONTRACT | `ForeignFrozenExport != LocalFreeze`, one level above `Canonicalization != Authority`: the source project `GFLK-Taaqol-GPT` exports the `OriginType` vocabulary `gflk.origin_type.v1` over the `ORIGIN_LEDGER_AR_v1` ledger with a deterministic content id and a self-declared `FROZEN_LOCAL` scope, and `src/alghanem/arabic/imported_feature_vocabulary.py` is the receiving contract. `ForeignFreezeScope` is a one-valued closed vocabulary read as declared and never promoted: no function converts it into `SpecificationFreeze.FROZEN`, a kernel `Freeze`, an `E0`, or a birth, since promotion would claim a gate this repository does not hold. `ImportedFeatureVocabulary` is bound to `EvidenceGenus.MORPHO_FUNCTIONAL` and refuses any other genus -- the binding named as missing when the import workstream was deferred. `ImportedOriginType` is closed over `EVENT`, `ENTITY`, and `UNRESOLVED`, with `UNRESOLVED` a member rather than a gap, and an unknown value is refused instead of folded into it. The distribution and row count are *derived* by counting the entries; a declared distribution or count that disagrees with the derived one is refused, so no field exists into which the answer may be written directly, and duplicate roots are refused because a duplicate hides one entry under another's identity. `ImportedVocabularyContentVerifier` is the sole issuer of `VerifiedVocabularyImport` and `LocalVocabularyContentIdentity` (private-token issuance), re-deriving an Alghanem-side content id through the shared `alghanem.canonical_content` primitive rather than trusting the declared digest, with schema coverage checked at import against the vocabulary and entry dataclass fields. `assert_matches_recorded_release` pins the recorded release -- 270 rows, 126 `EVENT` / 56 `ENTITY` / 88 `UNRESOLVED`, the source ids, and the declared source digest -- so a mismatched import is refused, not passed through silently. Boundaries: `ImportedVocabulary != BornOntology`, so this is not the deferred born morpho-functional vocabulary and leaves the five distributional features and `RECORDED_PROBE_REPORT` byte-identical; the scope stays narrow to `OriginType` because the weight and structure vocabularies have not been exported; and the module carries no result, verdict, or birth field (checked at import) and no kernel gate reads it, enforced by a test scanning every `kernel/` module. The source digest is recorded as declared and pinned, not independently re-derived: doing so would require the source's byte-precise canonicalization schema and its full payload, neither of which is in this repository, which the module states rather than conceals. What is known of that digest is recorded and enforced rather than assumed: by the export generator's own self-check it covers only each entry's `root` and `origin_type`, so `raw_category` and `batch_note` move without it, while the Alghanem-side identity covers every entry field. `SOURCE_DIGEST_COVERED_FIELDS` is asserted at import to be a *proper* subset of the entry fields, so the local identity is strictly finer than the source's and the two can never be read as attesting the same thing. |
| G0.2a.1 birth semantics content identity | ENFORCED_AT_CONTENT_ENCODER | `NoResidualIdDriftAfterFreeze`/`NoClosureCriterionIdDriftAfterFreeze` (G0.2a's id-equality checks) are label identity, not content identity: `ResidualDefinitionId != ResidualDefinitionContentIdentity`, and the same distinction holds for `ClosureCriterionSpec` and `WeakerModelSpec`. `CanonicalBirthSemanticsEncoder` is the sole issuer of `CanonicalResidualDefinitionManifest`, `CanonicalClosureCriterionManifest`, `CanonicalWeakerModelManifest`, and their `BirthSemanticsContentIdentity` SHA-256 digest references, covering every declared field of each spec. `BirthSemanticsContentRegistry` freezes the *first* canonical content bound to an exact `(domain, role, target_id)` scope; a later attempt to bind different content to that same scope is content drift and is rejected, not silently accepted because the id string still matches. `BirthAssessmentContentBinding` resolves every scope a `BirthAssessmentSemanticsContract` declares against a `SealedBirthSemanticsContentRegistry` and requires `CID(runtime) == CID(frozen)` for the residual definition, the closure criterion, and every weaker model; an unresolvable scope raises rather than passing silently. This closes `NoSemanticDriftAfterFreeze` for content, distinct from and in addition to `NoResidualDefinitionDriftAfterFreeze`/`NoClosureCriterionDriftAfterFreeze` for ids. It performs no evaluation and issues no `BirthVerdict`, `BirthCandidate`, or `Freeze`; `EvaluatorId != EvaluatorImplementationIdentity` and evaluator execution authority remain out of scope. |
| G0.2a.3 evidence acquisition authority | ENFORCED_AT_ACQUISITION_AUTHORITY | Binding evidence to a frozen experiment (G0.2a.2) proves only `FreezePrecedesRequestConstruction`, not that the freeze authorized the evidence's own acquisition; a caller could still select evidence first and attach a freeze afterward. This stage closes the narrower, code-provable `FrozenExperimentPrecedesAuthorizedEvidenceIngestion` instead of an unprovable external-world chronology claim (`AuthorizedCapture != ProofOfExternalAcquisitionChronology`). `EvidenceAcquisitionAuthority.authorize` is the sole issuer of an `EvidenceAcquisitionAuthorization`, requiring a genuine, verified `BirthExperimentSpecificationContentBinding` (`NoEvidenceAcquisitionAuthorizationWithoutFrozenExperiment`); its `experiment_content_id`, `domain`, `evidence_mode`, `evidence_requirements`, `revision_id`, and `revision_sequence` are derived properties of that binding, never independent caller-supplied facts. Only that authorization can issue an `EvidenceAcquisitionRun` (`open_run`), and only that run can issue an `AuthorizedEvidenceSnapshot` (`ingest`), closing `NoAssessableEvidenceSnapshotWithoutAcquisitionAuthorization`; none of the three is caller-constructible. `CanonicalEvidenceContentEncoder` alone issues the ingested payload's `EvidenceContentIdentity`, keeping `EvidenceOccurrenceIdentity != EvidenceContentIdentity` (`snapshot_id`/`run_id`/`authorization_id` name one occurrence; `content_id` is a digest over ingested bytes). `BirthAssessmentRequest` now requires an `AuthorizedEvidenceSnapshot` (rejecting the deprecated, unauthorized `EvidenceSnapshot`) and rejects a snapshot whose `experiment_content_id` does not equal its own experiment binding's `content_id`. `AuthorizedEvidence != SufficientEvidence`: this stage does not imply `ResidualSurvival` or `Birth`, and issues no `ResidualAssessment` or `BirthVerdict`. |
| G0.2a.3.1 issuer-scoped occurrence issuance integrity | ENFORCED_AT_ACQUISITION_AUTHORITY | Before this stage, `authorization_id`/`run_id`/`snapshot_id` were caller-chosen strings with no uniqueness authority: an issuer accepted a repeat of the same id, so `same(id) => same(occurrence)` did not hold and these were `EvidenceOccurrenceCoordinates`, not a proven identity. Each issuer now keeps its own registry of ids it has already issued -- `EvidenceAcquisitionAuthority` for `authorization_id`, one `EvidenceAcquisitionAuthorization` for its own `run_id`s, one `EvidenceAcquisitionRun` for its own `snapshot_id`s -- and `EvidenceAcquisitionAuthorityError` rejects a repeat within that scope, even for a snapshot repeat carrying different content. Each registry's check-and-insert is synchronized with an internal lock so concurrent calls on one instance cannot race past the uniqueness check. This makes issuance injective *within its declared scope* (`IssuerScopedOccurrenceUniqueness = PROVED`): two ids from the same issuer that are equal name the same occurrence, and two ids from the same issuer that differ name different occurrences. `LocalInjectivity != PortableIdentity`: `AuthorizedEvidenceSnapshot` carries no `issuer_scope_id`, so two distinct `EvidenceAcquisitionAuthority` instances are separate, uncoordinated issuance scopes whose ids are not thereby proven to differ from each other, and two snapshots from different authorities can share identical comparable representations despite being genuinely independent occurrences. `PortableEvidenceOccurrenceIdentity` remains `DEFERRED` pending a self-issuing `EvidenceIssuerScopeIdentity` propagated through the chain. `EvidenceAcquisitionRun`/`EvidenceAcquisitionAuthorization` are `ExternallyFrozen, InternallyStatefulAuthority` objects: `frozen=True` fixes their own declared identity fields, but each also holds a private, mutable `_issued_*` registry and lock (excluded from equality, `repr`, and content identity) as operational bookkeeping only. |
| G0.BA.1a authorized evaluator implementation binding | ENFORCED_AT_EXECUTION_GATE | Closes exactly one narrower residual left open by G0.2a: `AuthorizedBirthAssessmentEvaluatorDefinition != AuthorizedEvaluatorImplementation != EvaluatorExecution`. G0.2a's registry authorizes evaluator *declarations* (`domain`, `role`, `target_id`, `evaluator_id`) only, and performs no execution. `AuthorizedBirthEvaluatorImplementationBinding` is unchanged from and does not retroactively grant execution semantics to `AuthorizedBirthAssessmentEvaluatorDefinition`; instead, `BirthEvaluatorImplementationRegistry.register` requires an already-authorized definition plus an `implementation_identity` and an executable callable, and only `BirthEvaluatorImplementationRegistry.seal` freezes those bindings into a `SealedBirthEvaluatorImplementationRegistry`. `BirthEvaluatorExecutionGate.execute` is the sole authority that may resolve a binding by exact `(domain, role, target_id, evaluator_id, implementation_identity)` scope and invoke it, producing a `BirthEvaluatorExecutionRecord` -- a non-caller-constructible audit record preserving the authorized definition, implementation identity, role, target, the exact `BirthAssessmentRequest` and its own bound `AuthorizedEvidenceSnapshot`, input/output content, and trace. This record carries no `ResidualEvaluationResult`, `WeakerModelEvaluationResult`, `ClosureEvaluationResult`, aggregate assessment, residual survival, weaker-model exhaustion, `BirthCandidate`, `IndependentClosure`, `BirthVerdict`, or `Freeze` meaning: `Definition != ImplementationBinding != ExecutionRecord != Assessment`. Composing per-role execution records into any assessment remains a separate, later, still-deferred question. `AuthorizedCallableInvocation`, not `AuthorizedAssessmentEvidenceExecution`: the gate invokes the bound callable on caller-supplied `input_content`; it does not prove that content was derived from, or equals, the attached `AuthorizedEvidenceSnapshot`'s own payload (`EvidenceAttachedToRecord != EvaluatorExecutedOnEvidence`; `InputProvenance = DECLARED_DEFERRED`). Nor does it prove the resolved definition belongs to this request's own frozen `BirthAssessmentContentBinding`/`BirthAssessmentEvaluatorDefinitions` -- only that its `domain` matches (`AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment`). `implementation_identity` is a declared, caller-chosen string with no canonical manifest or digest of its own (`DeclaredImplementationId != ImplementationContentIdentity`; `ImplementationIdentityIsContentAuthenticated = DEFERRED`). |
| G0.BA.1b evidence-derived evaluator input provenance | ENFORCED_AT_DERIVATION_GATE | Closes exactly one of the three claims G0.BA.1a refused to make: `InputProvenance = DECLARED_DEFERRED`. The fix is structural, not a comparison added to the old gate. An `EvaluatorInputDerivation` receives exactly one argument -- the `canonical_bytes` of the request's own `AuthorizedEvidenceSnapshot` manifest -- and `EvaluatorInputDerivationGate.derive` accepts no `input_content` and no domain parameter at all (`CallerDoesNotOwnInputContent`): the caller chooses which authorized derivation runs, never what the evaluator sees, and the domain is read from the request's own frozen experiment. The same register -> seal -> gate shape applies: `EvaluatorInputDerivationRegistry.register` is the sole issuer of an `AuthorizedEvaluatorInputDerivationBinding`, `seal` alone produces a `SealedEvaluatorInputDerivationRegistry` resolving only by the exact three-part scope `(domain, derivation_id, implementation_identity)`, and only `EvaluatorInputDerivationGate.derive` issues an `EvidenceDerivedEvaluatorInput`. The gate re-verifies that the snapshot's bytes hash to the snapshot's own `EvidenceContentIdentity` before deriving, and rejects a derivation that returns non-text, blank content, or a different result for the same authorized bytes (`ObservedDeterminism != ProvenPurity`: this rejects observed nondeterminism, it does not prove purity). `CanonicalEvaluatorInputDerivationEncoder` digests the source evidence identity, the derivation id, the implementation identity, and the produced content together under length-prefixed canonical bytes, so the issued `EvaluatorInputContentIdentity` binds what was produced, from which exact evidence, and by which declared derivation (`OutputDigest != DerivationIdentity`). `ProvenanceBoundEvaluatorExecutionGate.execute` delegates the invocation itself to the unchanged `BirthEvaluatorExecutionGate` and then binds the issued record to the derivation that produced its input, requiring the same request object, the same evidence snapshot object, and exactly the derived content. G0.BA.1a is preserved completely unchanged and still accepts unrelated caller-supplied input by design: provenance is proven only for records issued by this stage. Three claims remain refused. `DerivationIdIsContentAuthenticated = DEFERRED`: `derivation_id` and `implementation_identity` are plain, caller-chosen strings with no manifest or digest of the derivation code (`DeclaredDerivationId != DerivationContentIdentity`), and `declared_transformation` is carried for audit and never verified against the callable (`DeclaredTransformation != VerifiedTransformation`). `AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment` is inherited unchanged: the execution boundary still matches only `domain`. `ProvenInputProvenance != AssessedEvidence`: `is_assessment` is `False` unconditionally, and the record carries no residual survival, weaker-model exhaustion, closure, `BirthCandidate`, `IndependentClosure`, `BirthVerdict`, or `Freeze` meaning -- `Derivation != ExecutionRecord != Assessment`. |
| AIM.1 declared programme aims, stage two record | ENFORCED_AT_AIM_RECORD | `DeclaredAim != LicensedProgramme`, `Aim != Achievement`, `AimsDocument != Authority`. [`docs/AIMS.md`](AIMS.md) names the programme's aims, each with its question, what would count as reaching it, what would not count even though it resembles it, and its citation in this record; aims are *extracted* from the existing record rather than dictated from outside it. Indicators of progress are declared epistemic and never engineering, and the reason is named rather than left implicit: an engineering indicator answers "does the code run?", while this programme's indicators answer "is the judgment the code issues earned by its evidence?" — two independent questions, since an empty function that always returns `PASS` can hold full test coverage and a green CI, so merging the two axes reproduces that defect at the scale of the whole programme instead of one unit. `TestPassIsNotUniversalTruth` (Encyclopedia Self-Observation, below) is the same refusal stated from inside this constitution. Aims that have not started are kept distinct from aims blocked by a *named* obstacle (`NamedObstacle != SilentAbsence`), and two foreign aims imported from the `A0.PP.3` source project are recorded as declared only (`DeclaredForeignAim != AlghanemRecord`): nothing here verifies them, and they enter no indicator. Stage two has begun and is enforced at `alghanem.program.aims`, one milestone at a time: `AimRecord` carries each aim's question, both boundaries, and its citation, across two independent vocabularies (`AimEngagement`, `AttainmentStanding`) rather than one ordinal scale, with each refused merge justified in writing. `AttainmentStanding.REACHED` is declared and refused at construction itself, exactly like `QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT`: no authority here may issue an aim's attainment. Absence of classification is a vocabulary member (`UNCLASSIFIED_IN_RECORD`), never a silent blank read later as progress, and `DeclaredForeignAim != AlghanemRecord` is a type boundary (`ForeignDeclaredAim`) rather than a field value, so exclusion from every later derivation is structural rather than disciplined. The module cites the open audit question `DeclaredVersusDerivedRecurrenceNotExplained` as its direct design source, as §5 of that document requires, and a test enforces the citation rather than trusting prose. The next milestone adds exactly the two derivation readers §4 names and nothing more, at `alghanem.program.constitution_ledger`: the law-table rows of this document and its open and resolved audit questions are read into two separate ledgers whose counts are derived properties rather than written fields, so no recorded number can disagree with this document. A status outside the closed `DeclaredLawStatus` vocabulary halts the read with a named refusal rather than skipping the row, because a silently short count is read later as a complete table; a missing section or an unreadable document is a named refusal too, never an empty ledger. An open question whose status this record does not declare carries `NO_STATUS_DECLARED_IN_RECORD` instead of a blank, and a resolved one keeps its previous audit label and closure law. That reader binds to no aim and imports neither `AimId` nor `AimRecord`, and a test enforces it. The third and last reader §4 names follows at `alghanem.program.deferred_value_ledger`, and only it: the declared-but-unbuildable values that still hold an aim open (`BIRTH_IN_SCOPE`, `MORPHO_FUNCTIONAL`, `CLOSED_BY_FROZEN_EXPERIMENT`). Its source is the `src/` tree rather than a document: each member is imported live so a rename is a named refusal rather than a value read as released, and the holding module's own text is parsed so the hold's site and shape are *derived*. Coding it showed that "unbuildable" is not one shape but three, kept in a three-valued `DeferredValueShape` rather than merged: a guard that names the value and raises; a guard that names it nowhere at all and merely admits its only sibling in a two-valued vocabulary; and a value no guard refuses because its sole authority never writes it, so the authority's derived codomain does not reach it. Each row carries both its declared shape and the shape derived from the code, and a disagreement is refused at construction — the `DeclaredVersusDerivedRecurrenceNotExplained` form doing real work here, where the previous reader had no declared total to compare against. The refusal rule rises one more layer, from the table to the guard: every guard over a tracked vocabulary is recorded in a derived `GuardCensus`, and a declared site with no witness in its module's text halts the read by name instead of being skipped. What remains is named rather than hidden: `REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY` (nothing in this record obliges a hold to take one of the three observed shapes), `SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE` (that hold is written nowhere and follows from an allow-list over a two-valued vocabulary, whose size is checked live), `CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY` (a codomain read from literal writes is *no reaching write was found*, not *no execution reaches it*), and `SECTION_4_NAMES_THREE_VALUES_ONLY` (other held values exist, and widening the list is a judgment this milestone does not hold). That reader binds to no aim either, importing neither `AimId` nor `AimRecord` nor `AttainmentStanding`, which a test enforces. The fourth milestone follows at `alghanem.program.aims_document_ledger`, and only it: the aims layer is subjected to the very rule it imposed on others. The three earlier readers checked declared against derived in *this* document and in the `src/` tree, while the aim record itself stayed a hand copy of `docs/AIMS.md` prose that nothing checked, so the layer exempted itself from its own law. Coding it showed that the record's prose is a paraphrase rather than a transcription — markup dropped, citations normalised — so verbatim comparison would have rejected the standing record or forced a shape the document never declared; what is derived instead is the structure the document does declare: aim identity and order, bullet labels, the §3 classification, and the partial-attainment remainder, with the untested remainder named (`RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION`). The bullet vocabulary is six labels rather than four, because one aim carries two variant labels; dropping them would have silently dropped that aim, and merging them would have erased the partial-attainment distinction the record itself derives. The field-presence laws of `AimRecord` are now enforced against the document that is their source, not only against the record. `AimRecordCorrespondence` carries no pass/fail field: its construction *is* the correspondence, and disagreement is a named refusal rather than a recorded verdict. Importing `AimId` here is not the indicator, and the distinction is structural rather than promised: the indicator binds a derived *count* to an aim, while this reader binds an aim to its own source text, imports none of the three readers, and a test parses its imports to enforce that. Transcription fidelity is not an aim's truth (`TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH`): a false aim faithfully copied passes this reader entirely. Still deferred and not present here: no indicator value is derived, and no field carries one — joining a derived count to a particular aim is the indicator itself and belongs to a later milestone under §4's conditions. The layer remains authority-inert: `AimRecord != BirthVerdict`, it issues no `Freeze`, no `E0`, no birth, and no verdict, it orders nothing by priority, and an automated scan asserts that no `kernel/` module reads it. |
| G0.MA.0 no predetermined pattern architecture (law only) | DECLARED_LAW_ONLY | See **G0.MA — Meta-architecture law** below. No runtime type or gate exists yet; this is a constitutional constraint on all future pattern-discovery, factorization-search, or architecture-selection work, including any future G0.BA/G0.F stage. |


### G0.C.1 — Minimal claim constitution

- `ClaimCandidate` is a reviewable occurrence of
  `ClaimContentManifest(ClaimCore, qualifications)`, not truth, evidence,
  knowledge, or a license.
- For the declared structured-claim distinction target, no-weaker projection
  collisions prove `anchor`, opaque `PredicateRef`, `polarity`, and `scope` are
  necessary in `ClaimCore`; broader semantic minimality remains
  `DECLARED_DEFERRED`.
- Predicate rendering and semantics are deferred; text is not claim input or
  primary identity.
- `CanonicalClaimContentEncoder` is the sole public issuer of
  `ClaimContentIdentity` through the controlled canonical-encoder API. Coverage
  guards fail closed for every field of `ClaimContentManifest`, `ClaimCore`,
  `Anchor`, `PredicateRef`, `ClaimScopeRef`, and `ClaimQualification`.
- Qualification tuple order is content-significant
  (`NoUnlicensedQualificationCommutation`); scope and polarity are encoded
  content.
- `ClaimOccurrenceRef != ClaimOccurrenceIdentity`: it is a reusable local
  reference; portable occurrence identity is `DECLARED_DEFERRED`.
- Legacy `Claim(claim_id, statement)`/`ClaimEvidenceBinding` remains separate;
  its claim-id equality is not G0.EB.1 evidence binding.
- `ClaimCandidate` has no evidence or evidence-binding field; claim-specific
  evidence binding is deferred to G0.EB.1.

### G0.OB.1 — Authenticated-observation bridge

- `AuthenticationIdentifier != AuthenticationCertificate`: strings naming an
  observation and its authentication never constitute an authenticated
  observation.
- `AuthenticatedObservationBinding` is issued only through a private,
  source-agnostic kernel bridge. A source-specific authority must invoke that
  internal bridge only after issuing its own authenticated
  observation. The G0.SO.1 repository adapter is
  `RepositoryObservationRun.bridge_authenticated_fragment`, which accepts only
  its own authority-issued `AuthenticatedRepositoryFragment`.
- The bridge is absent from the public kernel API. This establishes
  `NoPublicCallerIssuancePath` as a controlled Python API boundary, not
  cryptographic impossibility of forgery.
- The kernel imports no source-layer type. Repository-source coordinates use
  canonical JSON over every declared field, so delimiter-bearing values cannot
  collapse distinct provenance tuples. A binding is a
  `SourceBoundAuthenticatedCoordinate`, not a portable identity:
  `PortableAuthenticatedObservationIdentity = DECLARED_DEFERRED` until an
  issuer-scope identity is explicitly propagated.

### G0.EB.1 — Claim-relative evidence-role constitution

- `EvidenceRoleCandidate(AuthenticatedObservationBinding, ClaimCandidate,
  EvidenceRoleRef)` is a proposed evidence role. `EvidenceRoleRef` is opaque:
  `EvidenceRoleRef != EvidenceRoleSemantics != EvidenceApplicability`.
- Projection collisions prove the three coordinates are necessary for the
  declared distinction target: deleting observation, claim, or role collapses
  distinct candidates. This is
  `EvidenceRoleCandidateCoreMinimality`, not a claim of semantic minimality.
- `EvidenceRoleCandidate != EvidenceApplicability`: it does not assert that
  the observation is evidence or that the proposed role applies.
- `LegacyEvidence != EvidenceRoleCandidate`: legacy `Evidence(claim_id, basis)`
  and `ClaimEvidenceBinding` remain a separate claim-id system and never issue
  or substitute for a G0.EB.1 candidate.
- `EvidenceApplicability != EvidenceSufficiency`,
  `EvidenceSufficiency != Truth`, and `TruthAssessment != Knowledge` remain
  outside this milestone. `EvidenceRoleCandidate` has no fields for any of
  those judgments.

### G0.EA.1 — Evidence applicability assessment

- `ApplicabilityAssessmentGate` consumes an existing
  `EvidenceRoleCandidate`; it does not create or alter an observation, claim,
  or role.
- `EvidenceApplicabilityAssessment` is limited to `PASS`, `BLOCK`, or `DEFER`
  for the candidate's claim scope, and preserves a reason, trace, and
  residuals, plus the content identity of its specification and the snapshot
  identity of its sealed evaluator registry. `PASS` carries no unresolved
  residuals; `DEFER` carries at least one.
- Applicability models are content-bound to authority-issued evaluator
  bindings, including evaluator implementation identity, candidate role, and
  claim scope. A caller-supplied callable is not a frozen applicability
  semantics. The gate validates that the weakening graph is well-formed and
  acyclic.
- Models are competing closure models ordered by their declared weaker-model
  relation. The result is `PASS` when the weakest declared model that closes
  applicability passes; a stronger unresolved model cannot override it. If no
  model closes, a licensed block yields `BLOCK`, otherwise unresolved residuals
  yield `DEFER`.
- No anchor, scope, role, or provenance checklist is born as a primitive
  without a declared, authorized model and its residual boundary.
- The assessment does not assert evidence sufficiency, truth, licensed-claim
  status, or knowledge. A `DEFER` result is an unresolved applicability
  boundary, not a negative truth judgment.

Invariant assessment request semantics are closed at the gate: `BLOCK` means an
authorized verifier observed at least one invariant as false; `DEFER` means no
invariant was false but at least one could not be checked; and `VERIFIED` means
every declared component was checked and preserved. Missing, extra, or duplicate
specifications are malformed requests and raise
`InvariantAssessmentSpecificationError`; they produce no epistemic decision and
must not be recorded as failed components.

At Kernel v0.1, an operation's target domain is declared structural metadata
only; it does not grant transition or domain-transition authority. Source and
target domains may differ; whether they must coincide is a licensing question
deferred beyond Kernel v0.1.

Structural admission is not full licensing. `StructuralAdmissionGate` proves
only that a transition is well-formed under the laws above; it does not prove
evidential sufficiency, cross-domain authority, or inter-layer authority.
Those remain declared-deferred laws, and a future `LicensedTransition` — issued
only once those gates exist — must not be assumed to already exist because a
transition is structurally admissible.

Kernel v0.1's epistemic ladder, current rung marked with `*`:

```
Representable (TransitionCandidate) -> *StructurallyAdmissible* (StructurallyAdmissibleTransition) -> EvidentiallySupported -> AuthorityLicensed -> Certified (CertifiedTransition)
```

`TransitionKind` names the claim a candidate makes (what it is *representing*);
`StructurallyAdmissibleTransition` certifies only that the claim is
well-formed under structural laws. `StructuralAdmissionGate` evaluates candidates
to produce `StructuralAdmissionDecision`s (`ADMITTED`, `BLOCK`, `DEFER`, `UNDEFINED`).
Evidential sufficiency (`EvidentiallySupportedTransition`), authority to license a
transition (`AuthorityLicensedTransition`), and final certification
(`CertifiedTransition` carrying `CertifiedOutcome`) are later rungs, deferred
beyond Kernel v0.1. A linguistic layer (for example, a future Carrier/J
adapter) must be built as a client that produces evidence and invariant
claims for this kernel to structurally admit; it must not be granted
certification the kernel itself does not yet issue.

Kernel dataclasses are shallowly immutable: field reassignment is blocked, but
payload objects stored in `State.value` and `OperationResult.value` are not
deep-frozen by the kernel.

Canonical manifests are independent snapshots: mutation of a shallow payload
after encoding cannot alter existing canonical bytes, but a later encoding may
produce a different content digest for the same admission occurrence.

The kernel does not assume reversibility, global composition, path
independence, a group, or a groupoid. Those questions are intentionally
deferred until later milestones.

## G−1 — Pre-Algebraic Conditions of Intelligibility (law-only)

This milestone declares one constitutional boundary question:

```
What must be true before the first algebraic representation is even possible?
```

Intelligibility here carries no post-algebraic licensing, evidence, rank,
truth, or authority semantics.

It is law-only and boundary-only. It introduces no runtime, class, enum, gate,
evidence machinery, residual machinery, algebra primitive, or learning
architecture.

| Law | Status | Scope |
| --- | --- | --- |
| `NoTotalAlgebraicSelfBootstrap` | DECLARED_DEFERRED | The first algebraic representation may not be the complete ground of its own possibility. `NoTotalSelfBootstrap` is required; `RecursiveSelfExtensionAllowed` is explicitly preserved for later stages (`A_n -> A_{n+1}` is allowed). |
| `PreAlgebraicEnablingConditionIsNotOrganizedPriorContent` | DECLARED_DEFERRED | `E_-1 != P_0`. Pre-algebraic enabling conditions are not the same object as organized prior content. `ConditionOfPossibility != OrganizedPriorContent`. |
| `PriorAvailabilityIsNotPriorAuthority` | DECLARED_DEFERRED | `PriorAvailability != PriorAuthority` and `PriorInformation != PriorJudgment`. Availability for possible binding does not license truth, correctness, or judgment authority. |
| `PreAlgebraicIntelligibilityIsNotPostAlgebraicLicense` | DECLARED_DEFERRED | Any first differentiation/binding step at this boundary is an intelligibility/usability candidate only, not a post-algebraic licensing-authority act. |
| `FirstAlgebraRepresentabilityIsNotG0Birth` | DECLARED_DEFERRED | `FirstAlgebraRepresentability != G0Birth`. The representability boundary question must not be collapsed into post-algebraic birth authority semantics. |
| `NoHiddenEncyclopediaInFoundation` | DECLARED_DEFERRED | Foundation cannot be treated as a hidden finished inventory of truths. Availability of prior structure does not imply pre-certified knowledge. |
| `DifferenceCandidateIsNotCertifiedResidual` | DECLARED_DEFERRED | `DifferenceCandidate != CertifiedResidual`. A certified residual requires reconstruction/comparison capacity and explicit scope; before that, only candidates exist. |
| `NoResidualBeforeReconstructionCapacity` | DECLARED_DEFERRED | `Observed + Reconstructed + Comparator + Scope -> ResidualCandidate`. Therefore no residual is licensed before reconstruction capacity exists. |
| `NoPrematureGMinus1PrimitivePromotion` | DECLARED_DEFERRED | Evidence, Rank, Closure, and Residual are not G−1 primitives and must not be installed as foundational atoms at this stage. |
| `GenesisIsNotRetrospectiveReconstruction` | DECLARED_DEFERRED | `Genesis != RetrospectiveReconstruction` and `RetrospectiveFormalization != HistoricalGeneration`. Later formal reconstruction can describe prior conditions but does not historically generate them. |
| `ConditionOfPossibilityIsNotTruthGuarantee` | DECLARED_DEFERRED | `ConditionOfPossibility != TruthGuarantee`. Being necessary for intelligible start does not certify truth-status of the content. |
| `FoundationalInventoryOpen` | DECLARED_DEFERRED | `FoundationalInventory = OPEN` at the level of exact internal factorization. `NecessityOfUsablePriorInformationRelatedToReality = FOUNDATIONAL_GIVEN`, but no exact or partially closed three-factor ontology is frozen at G−1. `RetrospectiveMinimalityAudit != FoundationalGeneration`. |
| `NoPreAlgebraicUseOfPostAlgebraicProofMachinery` | DECLARED_DEFERRED | Later algebra may retrospectively audit G−1 boundary commitments, but post-algebraic proof machinery may not be used to retroactively generate G−1 itself. |
| `EpistemicPrecedenceIsNotFileOrderOrImplementationChronology` | DECLARED_DEFERRED | `EpistemicPrecedence != FileOrder != ImplementationChronology`. Existing G0+ laws/runtime are not invalidated or rewritten; G−1 states prior conditions they presuppose, not historical implementation order. |
| `NoClosedOPI0TupleAtGMinus1` | DECLARED_DEFERRED | If `OPI_0` is referenced, it is only a provisional analytical name. It must not be frozen here as a closed tuple, ontology identity, birth-certified object, rank, or evidence-certified status. |

The declared epistemic ordering is:

```
E_-1 -> P_0^{given} -> Encounter -> FirstIntelligibleDifferentiationOrBindingCandidate
    -> StableRepeatableRegularityCandidate
    -> CaseBoundDescriptionInsufficientCandidate
    -> ParticularInstanceIdentityInsufficientCandidate
    -> RepresentativeIndependentStructuralDeterminationCandidate
    -> ?

? = FirstAlgebraRepresentabilityCriterionNotYetDerived
```

PR47 is an open-audit boundary update only: it records falsifiable pressure
toward first algebra representability while leaving
`FirstAlgebraRepresentabilityCriterionNotYetDerived` explicitly unresolved.

Only after representational birth, recurrence is evidence-mode typed:

```
P_n + Q_{n+1} + EvidenceMode_{n+1} -> DemandAssessment

D_{n+1} =
  EMPIRICAL -> Demand(EMPIRICAL), as defined by G0.MA
  FORMAL    -> Demand(FORMAL), as defined by G0.MA
  MIXED     -> Demand(MIXED), as defined by G0.MA

D_{n+1} -> MinimalSatisfyingExtension? -> Birth? -> Freeze -> P_{n+1}
```

Mode-specific demand routes:

```
EMPIRICAL: Observation -> Reconstruction -> Difference -> CertifiedResidualGeometry
FORMAL:    FormalQuestion -> ExhaustiveNecessityProof -> CertifiedFormalNecessityWitness
MIXED:     EMPIRICAL and FORMAL tracks both required; neither substitutes for the other
```

### ClosedClaims

- G−1 is declared as pre-algebraic boundary law only.
- `ClosedClaims` at G−1 means constitutionally fixed boundary commitments for
  this milestone only; it is not runtime proof or runtime enforcement status.
- `ClosedAtConstitutionalBoundary != PROVED != ENFORCED`.
- Total algebraic self-bootstrap is disallowed, while later recursive
  self-extension is allowed.
- `E_-1 != P_0`, and `ConditionOfPossibility != TruthGuarantee`.
- `DifferenceCandidate != CertifiedResidual`; no residual before reconstruction
  capacity.
- `AlgebraRepresentability != AlgebraNecessity`.
- `FirstAlgebraRepresentability != G0Birth`.
- `RepresentabilityCandidate != LicensedAlgebraBirth`.
- `RepresentabilityPressure != RepresentabilityProof`.
- `OpenAuditUpdate != CriterionClosure`.
- Post-algebraic recurrence remains mode-typed (`EMPIRICAL/FORMAL/MIXED`) and
  is not reduced to residual-only flow.
- G0+ remains valid in implementation; G−1 asserts epistemic precedence only.

### UnprovedClaims

- Exact functional/internal factorization of `P_0`.
- Final foundational inventory membership and cardinality.
- Any proof that a particular candidate foundational dimension is strictly
  necessary.
- Historical generation path of pre-algebraic conditions.

### SourceAttestedPriorDimensions

- `NecessityOfUsablePriorInformationRelatedToReality = FOUNDATIONAL_GIVEN`.
- `SourceAttestedPriorDimensions ⊇ {ThingDirectedInformation,
  RealityOrWhatTheThingIsDirectedInformation, PropertyDirectedInformation}`.
- `ExactFactorization(P_0) = OPEN`.
- `PriorAvailability != PriorAuthority`.
- `PriorInformation != PriorJudgment`.
- `ConditionOfPossibility != TruthGuarantee`.
- `NoHiddenEncyclopediaInFoundation`.

These are boundary commitments, not a frozen ontology or closed primitive tuple.

### ResolvedAuditQuestions (lineage preserved)

- `PreAlgebraicLicensingVocabularyUnresolved`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: `PreAlgebraicIntelligibilityIsNotPostAlgebraicLicense`
- `GMinus1PostAlgebraicRecurrenceEvidenceModeMismatch`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: evidence-mode typed recurrence with
    `Demand(EvidenceMode) as defined by G0.MA`.
- `ClosedClaimsStatusSemanticsAmbiguous`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: `ClosedAtConstitutionalBoundary != PROVED != ENFORCED`.
- `PostAlgebraicAuditMustNotBecomeFoundationalGenerator`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: `NoPreAlgebraicUseOfPostAlgebraicProofMachinery`.

### OpenAuditQuestions

- `OrganizedPriorContentBoundaryNotDerived`: exact boundary between `E_-1` and
  organized prior content is not yet fully derived.
- `FirstAlgebraRepresentabilityCriterionNotDerived`: the criterion that upgrades
  stable repeatable regularity to first algebra representability remains open.
- `P0FunctionalMinimalityNotAudited`
  - Status: `DEFERRED_UNTIL_POSTALGEBRAIC_RETROSPECTIVE_AUDIT`
  - Note: prior-information necessity is given; minimal internal/functional
    factorization remains open.
- `ThirdTransmittedEvidenceModeNotDecided`
  - Status: `OPEN`
  - Question: is there a third, transmission-based evidence path independent of
    `EMPIRICAL` and `FORMAL`, in which a claim rests on *what was transmitted or
    reported* rather than on a measured residual or an exhaustive formal proof?
  - Standing evidence: the only concrete support currently in this repository is
    empirical, not theoretical, and it is named card by card rather than by any
    "two of three" generality. `maa_2_197.yaml` declares "خلاف نحوي مُسجَّل"
    and `imran_3_33.yaml` declares "تنازع مُسجَّل": both are records of a
    *disagreement between sources*, not derivations from a text, and they fit
    neither `EMPIRICAL` (no measurement run) nor `FORMAL` (no exhaustive proof
    over a closed domain). `man_2_255.yaml` is explicitly *not* of that kind:
    its witness ("وجود (ذا) بعد (من) قرينة نحوية تقليدية على الاستفهام") is a
    traditional grammatical clue about the text itself, not a transmitted
    disagreement. `hadhan_20_63.yaml` (طه:63) declares five witnesses, each
    naming its own grammarian (الطبري نقلًا عن لغة بلحارث بن كعب، أبو عمرو بن
    العلاء ورفض الزجّاج له، قراءة عاصم والخليل، مذهب كنانة، والشاذ الآحاد عن
    أُبَيّ بن كعب والخليل); these too are records of transmitted disagreement.
    Only those cards, named individually, stand behind this question.
  - Measured standing: `عدد_الشواهد` is no longer uniform. It is `1` on
    `man_2_255.yaml`, `maa_2_197.yaml`, and `imran_3_33.yaml`, and `5` on
    `hadhan_20_63.yaml`. This records a change in measurement only; it is not
    an upgrade of this question, which stays `OPEN`. A larger count is still a
    count of declared text: `DeclaredWitness != AssessedEvidence` still holds,
    the auditor does not read the *kind* of a witness's source, classifying
    witnesses remains out of scope, and multiplicity of named transmitters is
    not itself evidence that a third transmission-based `EvidenceMode` exists.
    The richer card also defers exactly like the other three, so nothing in the
    reported outcome distinguishes it.
  - Not decided here: this question is recorded, not answered. Status remains
    `OPEN`. `EvidenceMode` is unchanged, and `evidence_requirements` is part of
    frozen experiment content identity, so no mode may be added without a
    dedicated milestone that addresses that content-identity impact.
- `DeclaredVersusDerivedRecurrenceNotExplained`
  - Status: `OBSERVED_NOT_EXPLAINED`
  - Observation: the shape "a caller/card *declares* something; an authority
    *derives* or *verifies* it independently; the declaration never becomes the
    verified thing" recurs across this repository well beyond the four sites it
    was first noticed at. Located by search, not by recollection:
    `DeclaredInvariant != VerifiedInvariant`
    (`kernel/transition.py:86`, `kernel/invariant.py:4`),
    `ClaimedInvariant != VerifiedInvariant` (`kernel/invariant.py:313`),
    an `InvariantSpec.extractor_id` as "only a claim, not a grant of authority"
    with `Candidate/Caller does not own verifier selection authority`
    (`kernel/invariant.py:148`, `kernel/invariant.py:183`,
    `kernel/invariant.py:861`), gate-issued-only verification decisions and
    bundles that a caller cannot hand-build, `Candidate != Decision` and
    `AnchorEquality != ProvenIdentityPreservation`
    (`kernel/transition.py:83`), `DeclaredEvaluatorId != AuthorizedEvaluator`
    with `CallerDoesNotOwnEvaluatorAuthority`,
    `AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment` and
    `EvidenceAttachedToRecord != EvaluatorExecutedOnEvidence`
    (`kernel/evaluator_execution.py:41`, `kernel/evaluator_execution.py:257`),
    `DeclaredImplementationId != ImplementationContentIdentity`,
    `AuthorizedCapture != ProofOfExternalAcquisitionChronology` and
    `AuthorizedEvidence != SufficientEvidence`
    (`kernel/evidence_acquisition.py:19-22`),
    `ConstructibleContract != IssuedByAuthority` /
    `WellFormedFrozenFactorRef != AuthorityIssuedFrozenFactorRef`
    (`kernel/fractal.py:31-32`), `SameId != SameSemantics` /
    `ResidualDefinitionId != ResidualDefinitionContentIdentity`
    (`kernel/birth_content_identity.py:1`,
    `kernel/birth_content_identity.py:11`), the refusal of a caller-declared
    weaker cone (`arabic/external_audit.py:231`), and
    `DeclaredWitness != AssessedEvidence` (`arabic/external_audit.py:194`).
  - Two distinct sub-shapes, not one: in some sites the declaration is *checked
    against* the derived value and a mismatch is rejected outright (unauthorized
    `extractor_id`, caller-declared weaker cone, content drift under
    `SameId != SameSemantics`); in others the declaration is merely *carried and
    reported* with no authority ever attached to it (`DeclaredWitness`,
    `DeclaredImplementationId`, `AuthorizedEvidence != SufficientEvidence`).
    Whether these are one structure or two is not decided here.
  - Not a law and not named: this entry records a recurrence, nothing more. No
    law, type, base class, shared abstraction, or general name is created for
    it, and none may be introduced on the strength of this observation alone.
    A recurrence of phrasing is not proof of a shared underlying structure; the
    recurrence itself is what has yet to be explained.

### TheoreticalProgramBeforePostAlgebraicAudit

This section freezes the *question form* for the next theoretical stage. It
does not claim completion of derivation, minimality, or closure.

- `NecessityOfUsablePriorInformationRelatedToReality = FOUNDATIONAL_GIVEN`.
- `ExactFactorization(P_0) = OPEN`.
- `FirstAlgebraRepresentabilityCriterionNotDerived` remains open.

The immediate target is to separate three layers that must not be conflated:

- `PriorContent`: what is already present in prior information.
- `PriorAvailability`: what makes that prior content retrievable and usable.
- `RealityBindingCapacity`: what makes usable prior content connectable to new
  encountered reality.

Boundary law for this stage:

- `PriorContent != PriorAvailability`.
- `PriorAvailability != RealityBindingCapacity`.
- No item is declared primitive only because it appears early in explanation.

Central open question (theoretical, not yet a derived criterion):

- What is the minimal set of preconditions under which first intelligibility is
  possible at all?

Audit-position clarification:

- Philosophical/theoretical analysis of candidate preconditions is allowed now.
- Proof that a candidate set is minimal and irreducible remains
  `DEFERRED_UNTIL_POSTALGEBRAIC_RETROSPECTIVE_AUDIT`.

### First Algebra Representability — Falsifiable Boundary Candidate

This subsection stays inside G−1 and remains boundary-law only.

It does not claim that algebra is born, nor that a fully unified regularity or algebraic
element has already been derived.

Target form for this stage:

```
StableRepeatableRegularityCandidate
  -> CaseBoundDescriptionInsufficientCandidate
  -> ParticularInstanceIdentityInsufficientCandidate
  -> RepresentativeIndependentStructuralDeterminationCandidate
  -> FirstAlgebraRepresentabilityCriterionNotYetDerived
```

Interpretive boundary for this target form:

- Re-identifiable regularity across differentiated cases can pressure a
  representation demand.
- `CaseBoundDescriptionInsufficientCandidate != FirstAlgebraRepresentability`.
- `ParticularInstanceIdentityInsufficientCandidate != FirstAlgebraRepresentability`.
- `RepresentativeIndependentStructuralDeterminationCandidate != FirstAlgebraRepresentability`.
- Pressure toward representation is not completed representation.
- The candidate pressure is: identity of the revealing instance is insufficient
  to determine the result; structural determination must survive across
  independently differentiated representatives.

Conservative non-equivalence guards:

- `Repetition != FirstAlgebraicRepresentation`.
- `Similarity != ProvenSingleRegularity`.
- `RepeatableRegularity != IndependentRepresentationOfThatRegularity`.
- `CrossCaseReIdentification != ProvenUnifiedRegularity`.
- `CaseBoundDescription != RepresentativeIndependentStructuralDetermination`.
- `DependenceOnParticularInstanceIdentity != FirstAlgebraRepresentability`.
- `TrivialOneExampleAbstraction != FirstAlgebraRepresentability`.
- `NeedForHigherRepresentation != AchievedHigherRepresentation`.
- `AlgebraRepresentability != AlgebraNecessity`.
- `FirstAlgebraRepresentability != G0Birth`.
- `RepresentabilityCandidate != LicensedAlgebraBirth`.

Refutation-question matrix (questioning only; no final derivation here):

Rows for prior persistence, binding capacity, and linguistic-carrier analysis
belong to first-intelligibility/language sections, not this algebra
representability boundary subsection.

| Explanatory candidate | Piercing question |
| --- | --- |
| Repetition-only candidate | Can mere repetition, with no unified regularity claim, explain the observed invariance? |
| Similarity-only candidate | Can loose similarity explain the observations without one structurally unified regularity? |
| Case-bound description candidate | Can a strictly case-bound description preserve what repeats across differentiated cases? |
| Particular-instance-identity dependence candidate | If representative identity is changed while structural role-pattern is preserved, does determination collapse? |
| Structural nondeterminacy candidate | Can the same role-pattern map to incompatible determinations without violating the candidate boundary? |
| Trivial one-example abstraction candidate | Can a one-example or one-representative abstraction stand without independent differentiated support? |

Matrix output constraint:

- Failure of a weaker explanatory model yields only
  `CandidateNecessityForFurtherAudit`.
- It does not yield a necessity certificate at G−1.
- Minimality and irreducibility remain
  `DEFERRED_UNTIL_POSTALGEBRAIC_RETROSPECTIVE_AUDIT`.
- No-weaker closure, independent validation, reconstruction, and birth authority
  remain later/post-algebraic audit questions.

### ForbiddenNextJumps

- Do not introduce runtime/classes/enums/gates/evaluator machinery under G−1.
- Do not treat Evidence, Rank, Closure, or Residual as G−1 primitives.
- Do not close `OPI_0` into a fixed tuple or ontology identity.
- Do not reinterpret retrospective formalization as historical generation.
- Do not claim G−1 rewrites or invalidates existing G0/G0.MA/G0.F/BA/BV/RC law.

## G0.N — Knot ontology of the carrier (law-only)

This milestone declares one ontological commitment about what a carrier *is*,
ahead of any runtime that could issue one:

```
Carrier != DiscoveredEssence
Carrier  = KnotTiedOnAFiberOfRegularity
```

A carrier is not an essence that was latent in the material and finally
found. It is a knot tied, by convention and justified statistically or
formally, at a point on a continuous fiber of regularity — the one point that
survived every weaker model licensed and frozen for that experiment. Nothing
below promotes that convention into a discovery, and nothing below weakens it
into an arbitrary choice: a knot is licensed exactly by what it survived.

The structural consequence is about `Freeze`, and it is stated here rather
than left to be noticed later. Freezing does not fix a final essence; it
fixes a knot *at one version of the fiber* — one tool, one corpus, one
moment. Reopening when the fiber changes is therefore not a contradiction of
the earlier freeze but the condition of the knot's continuity, which is why
this section binds itself to the existing `G0.F.1` reopen protocol instead of
forking a parallel one.

| Law | Status | Scope |
| --- | --- | --- |
| `KnotNotEssence` | DECLARED_DEFERRED | A carrier is a conventional knot tied at a point that survived every licensed, frozen weaker model for its own experiment, never an essence that pre-existed the experiment and was uncovered by it. `SurvivedEveryLicensedWeakerModel` is the whole warrant for the knot; no separate act of recognition, intuition, or traditional naming adds anything to it, and `TraditionalName` remains strictly posterior per `NamingIsPosterior` below in G0. |
| `FreezeIsFiberVersionScoped` | DECLARED_DEFERRED | `Freeze(K)` fixes a knot at one declared version of the fiber (tool identity, corpus, normalization policy, Unicode database version), never an essence independent of that version. Consequently reopening `K` when the fiber version changes is required rather than merely permitted, and is not a defect of the earlier freeze. This composes `G0.F.1`'s `ReopenDoesNotRebirth` and `RevisionDoesNotEraseHistoricalFreeze` and forks neither: a fiber-version change opens a new revision on `K` itself and leaves the historical frozen record intact. |
| `NodeContinuityIsContentNotOccurrence` | DECLARED_DEFERRED | Two results separated in time or tool version may be read as *the same carrier* only if their content identity matches. Name equality is never sufficient, and occurrence identity is never sufficient: `admission_id` fingerprints that an execution happened, not which phenomenon it was about. `TransitionContentIdentity` and `OCCURRENCE_ONLY_EXCLUSIONS` (`src/alghanem/kernel/content_identity.py`) already enforce the exclusion half of this law — an occurrence field cannot enter a content identity — but the comparison half, deciding that two content identities produced under two tool versions name one knot, is issued by no authority in this repository and is not implied by digest equality alone. |
| `NoIntentProjection` | DECLARED_DEFERRED | No candidate's meaning may be settled by (a) the intent of whoever originally laid down the phenomenon, or (b) the intent of the researcher running the experiment. The only admissible meaning is what a surviving residual forces after every weaker model licensed and frozen *for that experiment* has been exhausted. `NoLabelLeak` (case a) and `NoOracleTuningBeforeFreeze` (case b) are two applications of this one origin, not two independent prohibitions, and neither is weakened by the other's satisfaction. |
| `ExistenceIsBinaryRankIsGraded` | DECLARED_DEFERRED | Two different questions may not share one verdict type. Whether a thing exists at all is binary and ungraded, and corresponds to `StructuralDecisionStatus` as a purely logical judgement. How well a judgement about a thing's attributes matches reality is graded by strength of evidence, and corresponds to whatever lower-confidence-bound, z-score, or p-value machinery a later measurement layer supplies. No such rank machinery exists in this repository today, so this law is declared over a codomain that is not yet constructible here. |
| `RankNeverCertifiesEssence` | DECLARED_DEFERRED | A rank may reach any height and still remain a measurement of the strength of presumptive evidence about an attribute. It never converts into the binary existence judgement, and never certifies an essence. Retractions of high-rank results are therefore structural rather than accidental: those results answered attribute questions, which stay presumptive at every rank. |
| `CompleteInductionIsCorpusBounded` | DECLARED_DEFERRED | Exhaustive enumeration over a closed finite set yields certainty *inside that set only*. A `PASS` over a complete corpus must be stated as established within that corpus and presumptive beyond it until a second independent corpus is enumerated. Direct generalization from one closed corpus to the open language it is drawn from is refused by name, not softened by hedging prose. |
| `NoBedrockWithoutRecurringDirayaSurvival` | DECLARED_DEFERRED | Ontological and epistemological scrutiny is a continuing process, not a gate passed once. Every independent new application — another corpus, another tool, another scope — is a fresh occasion to fail. Repeated survivals never fix the framework as bedrock; they license only the reading that it has not been defeated yet. |
| `TawaturRequiresDiachronicSuccession` | DECLARED_DEFERRED | `متواتر` presupposes succession *through time*: independent witnesses arriving in successive, temporally separated cycles. A closed corpus is a frozen synchronic section — one fixed text that neither grows nor renews — and therefore carries no temporal dimension in which succession could occur at all. Asking whether a finding over such a corpus is `متواتر` is therefore a category mismatch, ill-posed in the manner of asking whether the number five is univocal or equivocal, and not a question left unanswered until some future measuring authority arrives. The consequence is stated in this precise form and no wider: the obstacle to *earning* `متواتر` inside this repository is the structure of the evidence base, not the absence of a tool, so no future authority over closed corpora removes it — while the obstacle to *verifying* a genuinely diachronic transmission remains ordinary missing authority, held under `NoReachingWrite != ProvenUnreachable` like any other hold. The temporal structure a hold is derived *from* is itself derived, never passed in: a base is a frozen synchronic section only when its closure binding is re-derived by byte-exact rematch of its own full enumeration through the authority-free canonical content primitive, so an unenumerable base proves no closure. That derivation is necessarily asymmetric and partial: `DIACHRONIC_INDEPENDENT_SUCCESSION` is never derived from any descriptor, because proving succession is precisely the temporal authority this repository lacks, and deriving it would invert `NoReachingWrite != ProvenUnreachable` under the appearance of repair. Nor may its absence be inferred: "not a proven frozen closure" does not entail "therefore a genuine succession", so a failed closure proof yields `TEMPORAL_STRUCTURE_NOT_SETTLED` and an unsettled genus, never the nearer of the two. One level of the regress is removed and no more: the enumeration itself remains caller-declared, and what changed is that the declaration is now a structural claim rematched byte for byte rather than a temporal verdict nothing could check. This law neither grants nor withholds any exemption resting on recurrence; `FIRST_ORGANIZED_INFORMATION_QUESTION` stays open with all three of its hypotheses. |

This section is law-only and boundary-only, in the manner of `G−1` above. It
introduces no runtime, class, enum, gate, rank primitive, or continuity
authority, and it neither invalidates nor rewrites any existing G0, G0.MA,
G0.F, G0.BA, G0.BV, or G0.IC law. In particular it issues no
`CarrierNodeContinuityReading`: deciding that two frozen results name one knot
across two tool versions is exactly the authority this repository does not
have, and declaring the law is not exercising it.

## G0.W — The decision chain: wad, umum/khusus, and the chain ledger

This milestone builds three Arabic-layer modules for the fourth, tenth, and
framing positions of the decision chain that runs from an identity-free
codepoint to a concept grounded in sense. It adds no kernel authority: none of
the three imports anything from `kernel/`, none is read by anything in it, and
none issues a birth, a `Freeze`, or an `E0`.

The founding correction is stated as law rather than left in prose. Language is
laid down by human beings and not by God: neither revelation (a vicious circle,
since revelation is itself understood only through a language prior to it) nor
necessary knowledge (which would entail necessary knowledge of God, contrary to
observed fact) is a path to it. `وعلَّم آدم الأسماء` is therefore the teaching
of the *realities and properties of things* — a direct concept in the sense of
`ContentStanding.مفهوم` — not the teaching of lexemes. The consequence is the
one that matters structurally: because the laying-down is a purely human,
historically contingent event, it is knowable only by transmission — not
because it is sacred, but because nothing else reaches a past convention.

| Law | Status | Scope |
| --- | --- | --- |
| `WadIsHumanNotDivine` | ENFORCED_AT_WAD_NAQL | `WadOrigin` is a closed two-member vocabulary and `وضع_بشري` is **derived from an exhausted two-part refutation, never declared in a field**: a `TawqifRefutation` must carry both `لا_طريق_بالوحي` and `لا_طريق_بعلم_ضروري`, each with an excerpt quoted verbatim from the one named source and checked by containment (`src/alghanem/arabic/wad_naql.py`). One ground alone leaves the other possibility standing, so a single-ground refutation fails at construction rather than producing a warning. The rejected reading of `وعلَّم آدم الأسماء` as lexemes is a named member of `AdamTeachingReading` refused by the source's own words, not a silent absence. `HumanWad != ArbitraryChoice`: a human convention is a collective settlement that actually occurred, transmitted as it occurred and not invented as one wishes. |
| `WadKnownOnlyByNaql` | ENFORCED_AT_WAD_NAQL | A `WadRecord` — the pairing of one `لفظ` with one `مدلول` — carries its path of knowledge only as a `TransmissionStanding` (متواتر/آحاد/فرض), imported rather than copied, and `known_only_by_naql` is structural rather than optional. The two refused paths are refused by name and by construction: `refuse_derivation` always raises for `استنباط_من_التحليل_التوزيعي` and `استنباط_من_تحليل_المدلول`, because link 3a knows only relations among carriers and states and link 3b knows no particular lexeme at all. `Naql != Sanctity`. |
| `DistributionalTraceIsNotWadPath` | ENFORCED_AT_WAD_NAQL | The trace of a convention is not the path to knowing it, and neither statement corrects the other. `ONLY_LEGITIMATE_TARGET_NOTE` in `maluma_mafhum` describes a real distributional regularity left by a settled convention and stands unchanged; what it may not do is yield *which* lexeme was paired with *which* meaning, since an equivalent regularity can arise from incidental repetition or sample bias. `DistributionalCorroboration` is therefore constructible only over an already transmitted `WadRecord`, its `function` is fixed at `يرفع_دراية`, and `transmission_after_corroboration` returns the prior standing unchanged: statistics raise diraya and never manufacture riwaya. |
| `TakhsisIsNotIhmal` | ENFORCED_AT_UMUM_KHUSUS | Specialization is the operation of *both* evidences, never the dropping of one: the specializer operates at its locus and the general remains authoritative beyond it. `TakhsisRegistration` (`src/alghanem/arabic/umum_khusus.py`) holds exactly the general evidence, the specializer, and a named conflict locus; there is no field into which a dropped or outweighed evidence could be written, and an import-time sweep refuses one. The channel of specialization is **derived** from the specializer's own `DalalaChannel` — imported from `mantuq_mafhum_ifada` rather than duplicated — so specializing a general by a `مفهوم` is read off the evidence rather than asserted. A general specializing a general, a specializer that is itself general, an evidence specializing itself, or a specialization with no named locus each fail at construction, the last because the default is difference rather than contradiction (`DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE`). `TakhsisChannel.لا_تخصيص` is a declared member that no derivation from a standing specializer can ever produce. |
| `TafriPathsAreNotMixed` | ENFORCED_AT_UMUM_KHUSUS | A general rule branches onto its individuals and a universal rule branches onto its particulars; the two are distinct paths, not synonyms. `TafriRegistration` derives its path from a closed `RuleGenus` and refuses a declared path that disagrees. `RuleGenus` is deliberately *not* `Universality` from `kulli_juzi_formal`: that vocabulary classifies a single word as كلّي or جزئي on attested evidence, and mapping its `جزئي` onto a general rule would be the very genus confusion this row forbids — a foreign value passed to `tafri_path_of` is refused rather than coerced. |
| `TypeSignificationIsAlwaysMantuq` | ENFORCED_AT_MANTUQ_MAFHUM_IFADA | The eighth link divides signification exhaustively — مطابقة and تضمن are منطوق, التزام is مفهوم, and there is no third — but one thing never falls on the مفهوم side: **the type of the ruling itself**. It is منطوق always, and is never derived by مفهوم موافقة or مخالفة from an accompanying descriptor; only the side qualifications of a ruling are read that way. `SignifiedAspect` (`src/alghanem/arabic/mantuq_mafhum_ifada.py`) names what a reading falls upon — `نوع_الحكم` or `قيد_جانبي` — and `RulingAspectReading` refuses exactly one combination at construction: `نوع_الحكم` read through `DalalaChannel.مفهوم`. The aspect is not a rung in the channel and does not rank منطوق above مفهوم: reading a side qualification by مفهوم stays open. The channel is not rewritten here but read off the held `DalalaRecord`, so it remains derived in one place; and the accompanying descriptor a مفهوم was read from must be named, while a منطوق may carry none, so no مفهوم is attributed to an unnamed وصف. |
| `ChainReachIsDerivedNotCoded` | ENFORCED_AT_DECISION_CHAIN | `decision_chain` reads the fifteen positions of the chain off the tree, and reach is derived by succession rather than from coding alone: each link conditions the next, so a coded link preceded by an unreached one reads `مسبوقة_بحلقة_غير_بالغة` and never `بالغة`. This is what keeps the chain from reading as complete while links 1 and 2 (the carrier, and the (carrier, state) derivative) stay deferred under `KnotNotEssence`. Deferral by law is **declared, not inferred from absence**: a link with no module at all names the constitutional law that defers it, while a link naming a module has its coding read from the tree like any other. The two governing constraints — the idea/method/means test and the seriousness/benefit test — are recorded as the chain's *frame* rather than positions in it, both `مُصرَّح_غير_مُرمَّز`, and no `GoverningConstraint` declaring itself coded is constructible today: constraint (أ) awaits a written universal idea for GFLK, which this repository does not have and which this milestone deliberately does not invent, and constraint (ب) admits only one acceptable test — a complete application to a real word or verse. The ledger is a reading of the tree and not an authority over it. |

## G0 — Birth Protocol (declared law, no runtime gate yet)

The kernel and Arabic layer never introduce a new named object, cardinality,
or ontology term because it is convenient, expected, or traditional. A
candidate object is only permitted to be *born* — closed independently and
eventually handed a traditional name — through the following declared chain.
At Kernel v0.1 this chain is **law only** except for its deferral branch: no
`BirthGate` that can birth anything, no rank/complexity class, and no
Arabic-specific carrier/state/relation ontology type exists yet. G0.BV.1a's
`BirthVerdictGate` executes only the `DEFER_IN_SCOPE` outcome of this chain
and can never advance it. A
non-linguistic intervention-operation runtime does already exist (see
`InterventionOperationIsNotOntology` below); it is a declared experimental
tool, not one of these ontology types, and does not itself satisfy this
chain. Those ontology types are separate, later milestones that must
themselves be structurally admitted like any other change, and must not be
named in advance of the residual that would force them (`G0.F` below); this
section only freezes the constraints they will have to satisfy if and when
they are born.

```
BirthQuery -> Evidence -> Residual -> LicensedWeakerExhaustion
-> NecessaryInvariantCandidate -> BirthCandidate -> IndependentClosure
-> BirthVerdict -> Freeze -> E0 -> TraditionalName
```

`BirthCandidate != BirthVerdict`: a candidate remains only a proposal until
`IndependentClosure` produces `BIRTH_IN_SCOPE` through a future gate. `Freeze`
is the separate, later act of fixing only that successful scoped verdict;
`E0` consumes that frozen result in a subsequent stage. `NO_BIRTH_IN_SCOPE`
and `DEFER_IN_SCOPE` cannot be frozen. Naming never occurs before birth
verdict, freeze, and `E0` have happened.

| Law | Status | Scope |
| --- | --- | --- |
| `NoBirthWithoutResidualOrFormalNecessity` | DECLARED_DEFERRED | No candidate object, factor, or axis may be born without one of two independent evidence modes. In `EMPIRICAL` mode, a *measured* residual (from real observations, not synthetic interventions alone) must remain unexplained after every licensed weaker projection has been applied. In `FORMAL` mode, over a declared `FrozenFormalDomain` with `card(Ω) < ∞` (or another exhaustively decidable closed domain), an exhaustive proof over every element of that domain, with no weaker formal model sufficing, may license birth without any measurement run. A `MIXED` mode combines both and must satisfy each mode's own condition on its own part of the claim. `FormalProof ⇏ EmpiricalReality` and `EmpiricalPattern ⇏ MathematicalNecessity`: neither mode substitutes for the other, and every birth must declare which mode(s) it relies on. |
| `NoBirthBeforeLicensedWeakerExhaustion` | DECLARED_DEFERRED | Before any `BirthCandidate` may be proposed, every weaker projection or formal model *licensed and frozen for that experiment* (`W_E = {W_1, ..., W_n}`), not an unbounded or open-ended "every weaker model conceivable," must first be tried and shown insufficient. A birth proposal that skips a licensed weaker model is malformed, not merely unproven. Discovering a new weaker model `W_{n+1}` afterward opens a new, separately recorded revision; it does not erase the historical closure in its original scope. |
| `NoRicherStructureBeforeLowerOpenResidualClosure` | DECLARED_DEFERRED | For a queried structure `q`, its prerequisite cone is exactly `Down_E(q) = {p ∈ P_E : p ≺_E q}`, derived from the experiment's frozen projection poset, never selected independently by the caller. If any `p ∈ Down_E(q)` has an open residual, examination of `q` is blocked. This is a partial-order constraint, not a linear "rank `r+1`" constraint. An incomparable projection (`p ∥ q`) does not block examination; however, if it offers a complete competing explanation of the residual, `BIRTH_IN_SCOPE(q)` is blocked until discriminating evidence resolves the competition. |
| `ScopedBirthIsNotGlobalOntologyClaim` | DECLARED_DEFERRED | Every verdict is scoped to the exact `(experiment, revision, domain, licensed weaker-model set, evidence mode, measurement run or formal domain, evidence snapshot)` tuple that produced it: `BIRTH_IN_SCOPE(...)`, `NO_BIRTH_IN_SCOPE(...)`, or `DEFER_IN_SCOPE(...)`. A malformed specification produces no verdict; `DEFER_IN_SCOPE` is reserved for a structurally valid but epistemically unresolved assessment. A later revision may become the active epistemic assessment, but cannot erase a prior verdict's historical scoped record. No scoped verdict generalizes into a global ontology claim. |
| `ProjectionIsNotOntology` | DECLARED_DEFERRED | Weaker-model projections (for example count, set, multiset, ordered-tuple) are analysis tools for deciding whether a residual survives, not born objects and not linguistic claims. Projections form a partial order, not a total order: `P_count` and `P_set` are incomparable (`P_count ∥ P_set`), while both are recoverable from `P_multiset`, and `P_multiset` is recoverable from `P_seq` (`P_count ⪯ P_multi`, `P_set ⪯ P_multi`, `P_multi ⪯ P_seq`). No total-order complexity vector may be assumed across projections or coordinates that have not themselves been born. |
| `InterventionOperationIsNotOntology` | DECLARED_DEFERRED | A declared basis of experimental interventions (for example an "ExperimentalInterventionBasisV0" of delete/insert/substitute/repeat/swap) is an explicit, named, non-exhaustive experimental tool. It must never be asserted to be the complete set of primitive operations, and its members are not linguistic or structural objects. |
| `CounterfactualResultIsNotObservation` | DECLARED_DEFERRED | The output of a synthetic/counterfactual intervention applied to a previously observed occurrence is not itself a `RawSurfaceObservation` or any other measured observation. This is a type/authority separation, not an implementation detail: a counterfactual result must belong to a distinct type that cannot be admitted into the observation or normalization ledgers, regardless of how any particular field on it is named or valued. Partially enforced for the two artifact kinds that exist in the Arabic encoding layer (`src/alghanem/arabic/encoding/provenance_genus.py`): `EvidenceProvenanceGate` is the sole issuer of an `EvidenceProvenanceClassification`, and derives its genus from the artifact's own type (`NormalizationAudit` bound to a manifest is `MEASURED`, `SurfaceInterventionAuditRow` is `SYNTHETIC`), so no caller may write a genus anywhere — `DeclaredProvenanceLabel != DerivedProvenanceGenus`. A synthetic classification is refused at construction by `MeasuredContrastSet`. The law remains `DECLARED_DEFERRED` in general because only these two artifact kinds are covered, and nothing yet prevents a future artifact kind from bypassing the gate. |
| `SyntheticInterventionMayGenerateHypothesisOnly` | DECLARED_DEFERRED | A residual discovered only through synthetic/counterfactual interventions (`R_synthetic`) may license nothing beyond a hypothesis (recorded as a `HypothesisResidual`, not a `FactorCandidate`). It cannot by itself satisfy `NoBirthWithoutResidualOrFormalNecessity`. A hypothesis becomes birth-eligible only after an independently measured contrast (`R_measured`), drawn from real observations under a measurement run, is found to match the hypothesis and itself survives every licensed weaker projection, with replication in a second, independent measurement run. For example, a `swap` intervention showing `(a, b) != (b, a)` at the codepoint-sequence level proves only `CodepointSequenceIsOrderSensitive` within the synthetic domain; it does not by itself birth any order-related linguistic or structural candidate. The 'hypothesis only' half is enforced in the Arabic encoding layer: `HypothesisResidual` is the only thing constructible from synthetic classifications, it refuses measured evidence, it is checked at import to declare no candidate, verdict, birth, or rank field, and its `is_birth_eligible` is structurally `False` with no method able to raise it. The promotion half remains `DECLARED_DEFERRED`: no authority in that layer assesses residual survival under licensed weaker projections or replication in a second independent measurement run, so no rank, count of measured sources, or freeze exists there — a rank ladder ascending on a count would be precisely the caller-owned freeze authority this constitution refuses. |
| `DerivedFootprint != DeclaredFootprint` | ENFORCED_AT_INTERVENTION_FOOTPRINT | The ReadSet, WriteSet, and coordinate shift of an intervention are derived from the intervention itself and are never accepted from a caller. `InterventionFootprint` (`src/alghanem/arabic/encoding/intervention_footprint.py`) holds exactly one field — the intervention — and exposes `read_set`, `write_set`, `shift`, and `touched` as computed properties, so a footprint contradicting its own intervention is unconstructible rather than merely unverified. Shift is modelled explicitly (`delete` and `repeat` from `i + 1`, `insert` from `i`) instead of being folded into overlap, so disjoint write sets still conflict when one operand sits at or past the other's shift origin. |
| `PredictedVerdict != ObservedVerdict` | ENFORCED_AT_INTERVENTION_FOOTPRINT | A commutation verdict predicted from footprints alone is a distinct object from the verdict observed by applying both orders through the real application path (`observe_commutation`), and the two are never conflated. A disagreement is named `PREDICTION_ORACLE_MISMATCH(τᵢ,τⱼ)`, retained in the reported pair list, and drops the derived `law_status()` to `PARTIAL_WITH_NAMED_RESIDUALS`; the status is derived from the matrix rather than written into it, the mismatched pair may not be dropped, and the footprint definition may not be retrofitted to match what was observed. This is `NoLabelLeak` raised to the level of a verdict. |
| `NamedCriticalPairs != GeneralizedLaw` | ENFORCED_AT_INTERVENTION_FOOTPRINT | The product of the footprint module is an enumerated list of named pairs with their verdicts and reasons (`overlap`, `shift`, `out_of_range`) over named coordinate configurations, not a generalized confluence or commutation law over the whole intervention algebra. `reference_matrix` covers the five intervention types pairwise across nine declared configurations on a distinct-atom sequence, excluding identical interventions by declaration; its scope and its limits are recorded in `DERIVED_LAW_SCOPE_NOTE`, `IDENTICAL_PAIR_EXCLUSION_NOTE`, `PAYLOAD_INDEPENDENCE_NOTE`, `ORDERED_TRIPLES_ABSENCE_NOTE`, and `VALUE_COINCIDENCE_NOTE`. The measured domain is ordered pairs only: a three-way critical-pair set is not derivable from pairwise verdicts, so it is recorded as absent rather than assumed. Because the model reads coordinates and not values, agreement produced by repeated atoms is value coincidence, not structural commutation, and is demonstrated by an explicit test instead of absorbed by widening the definition. Nothing beyond the measured configurations is claimed. |
| `AgreedVerdict != GrantedAuthority` | ENFORCED_AT_INTERVENTION_FOOTPRINT | Agreement between the predicted and the observed verdict disciplines a model of non-linguistic surface interventions and grants no authority whatsoever. No kernel type, gate, `Freeze`, or `E0` reads anything from the footprint module, and exporting it from `alghanem.arabic.encoding` is availability, not consumption; the absence is recorded in `NO_KERNEL_MODULE_CONSUMES_INTERVENTION_FOOTPRINT_NOTE` and enforced by an import-tree sweep test rather than asserted in prose. Subject to `InterventionOperationIsNotOntology` and `SyntheticInterventionMayGenerateHypothesisOnly`, a confirmed derived law here remains non-authoritative: it licenses at most a hypothesis and never a birth verdict. |
| `TraditionalNamingOnlyAfterFreezeAndE0` | DECLARED_DEFERRED | A traditional name (linguistic, grammatical, or morphological) may only be attached after the full chain `BirthCandidate -> IndependentClosure -> BIRTH_IN_SCOPE -> Freeze -> E0` has completed. The name is never part of the birth proof, never influences whether birth, closure, or freeze occurs, and the kernel itself must never define or reference `TraditionalName`; any such naming step belongs strictly to a downstream, kernel-independent evaluation/oracle layer. |

These laws are declared now, ahead of any experiment, precisely so that the
question being asked cannot be quietly reshaped by the answer an experiment
later produces. Implementing `BirthGate`, a rank/complexity representation,
or any Arabic-specific carrier/state/relation ontology type is out of scope
for this section and must occur in later, separately reviewed milestones
that are held to these same laws. No such type -- including any general
linguistic "binding" relation -- is to be named or scaffolded before a
residual is shown to force it: see `G0.F`'s `DerivedRelationDoesNotBirth` and
`NoTraditionalSchemaBeforeFactorization` below. (`kernel/binding.py`'s
`ClaimEvidenceBinding` is an unrelated kernel-level evidence/claim binding,
not an Arabic linguistic relation, and is out of scope of this paragraph.)

#### Recorded external-source conflict (not a law, not a relaxation)

An external jurisprudential source consulted while reviewing this protocol
licenses answering a question with *more* than was asked ("الجواب بأكثر مما
سُئل"): a valid answer may legitimately settle matters beyond the question's
own subject. This directly conflicts with
`NoRicherStructureBeforeLowerOpenResidualClosure` above, which blocks
examination of a richer structure `q` while any `p ∈ Down_E(q)` has an open
residual, and with `TraditionalNamingOnlyAfterFreezeAndE0`, which forbids
naming anything a residual has not forced.

The conflict is recorded, not resolved, and neither side is weakened to fit
the other. In this repository the constitutional laws govern: an audit or
experiment may not answer beyond the structure its own query and prerequisite
cone license, regardless of that external precedent. This paragraph exists so
that the conflict cannot later be presented as agreement, and so that the
external precedent cannot be cited as grounds for relaxing either law.

### G0.1 — Birth experiment contract

`BirthExperimentSpecification` is a language-agnostic, frozen pre-evidence
contract. It contains an experiment identity, revision identity and monotonic
revision sequence, evidence mode, domain, frozen projection poset,
`BirthQuery`, stable residual-definition identity, residual-definition text,
stable closure-criterion identity, closure-criterion text, and evidence
requirements. The stable identities are the freeze boundary; descriptive text
alone cannot identify a later executable contract. It does not contain an
evidence snapshot, a candidate, a verdict, or caller-selected weaker models.
Its frozen weaker-model set and `PrerequisiteCone` are both derived as
`Down_E(q)` from the poset and query: they share values in G0.1, but name the
distinct frozen-model-set and query-relative order roles. Its incomparable
projections are recorded as possible competing explanations.

`BirthAssessmentRequest = AuthorizedFrozenExperimentBinding +
AuthorizedEvidenceSnapshot`; the request refuses a raw
`BirthExperimentSpecification` and refuses the legacy, unauthorized
`EvidenceSnapshot` (deprecated: it carries no acquisition provenance). This
ordering enforces `NoAssessmentRequestWithoutAuthorizedPreEvidenceFreeze` and
`EvidenceMayBeAttachedOnlyToAnAuthorizedFrozenExperiment`, preventing evidence
from redesigning the question or its closure criterion. The contract validates
malformed bindings before any request can enter a future runtime. G0.1 stops at
`BirthAssessmentRequest`: it has no
executable verdict, revision-history, competing-explanation assessment, or
freeze authority. G0.BV.1's birth branch remains deferred: no runtime authority may issue
`BIRTH_IN_SCOPE` or `NO_BIRTH_IN_SCOPE` until an assessment authority,
BirthCandidate, and IndependentClosure exist. Its deferral branch is now
executable at G0.BV.1a (`kernel/birth_verdict.py`): `BirthVerdictGate.assess`
derives `DEFER_IN_SCOPE` itself from the request's own frozen projection poset,
for a frozen experiment authorized in a sealed `BirthVerdictScopeRegistry`. A
gate that can only defer still refuses every unlicensed birth, which is the
boundary G0.BV.1 exists to protect; it issues no `Freeze` and no `E0`.
G0.IC.1a (`kernel/independent_closure.py`) then closes exactly one conjunct of
the missing `IndependentClosure` and openly refuses the rest:
`IndependentClosureGate.assess` derives, from the frozen projection poset
alone, whether any projection is left incomparable with the test model. Over a
finite frozen projection set that question is exhaustively decidable, so unlike
the verdict gate both of its statuses are reachable. It remains far from
closure: `IndependentClosureAssessment.is_independent_closure` is `False`
unconditionally, and `BirthVerdictGate` is deliberately not wired to consume
it.

The current repository-level Arabic card auditor
(`src/alghanem/arabic/external_audit.py`) is intentionally outside kernel
verdict authority. It may parse an external card and emit an external audit
result (`نتيجة_التدقيق_الخارجي`) for communication/audit traceability, but it
must not be interpreted as issuing `BirthVerdict` or freeze authority. Its
weaker-prerequisite cone is derived from the experiment's frozen projection
poset, not caller-declared, and it may defer when competing-relation typing or
`Down_E` closure documentation is unresolved. Competing-relation typing draws
on a closed vocabulary (`غير_متعينة`, `أضعف_صوريًّا`, `مكافئ_صوريًّا`,
`غير_قابل_للمقارنة`); an unrecognized value is rejected rather than treated as
a resolved relation, and, per
`NoRicherStructureBeforeLowerOpenResidualClosure`, a `غير_قابل_للمقارنة`
reading stops blocking only when the card explicitly denies that it offers a
complete competing explanation. Because a surface spelling is not
an epistemic distinction, every card comparison runs over an
orthography-insensitive key rather than raw text: optional diacritics,
invisible formatting characters, `TATWEEL`, and equivalent `ALEF`/`ALEF
MAQSURA`/`TEH MARBUTA` forms may not decide whether a relation counts as
determined or a `Down_E` prerequisite counts as closed. The key governs
comparison only; reported fields keep the card's own spelling.

### G0.2a.3 — Evidence acquisition authority

Binding evidence to a frozen experiment is not enough: a caller could still
select or construct evidence before designing an experiment, then attach it
to a `BirthExperimentSpecificationContentBinding` produced afterward. This
proves only `FreezePrecedesRequestConstruction`, not that the freeze
authorized the evidence's own acquisition. G0.2a.3 closes the narrower,
code-provable claim `FrozenExperimentPrecedesAuthorizedEvidenceIngestion`
instead of an unprovable external-world chronology claim.

The chain is
`BirthExperimentSpecification -> FrozenPreEvidenceExperimentManifest ->
BirthExperimentSpecificationContentBinding -> EvidenceAcquisitionAuthorization
-> EvidenceAcquisitionRun -> AuthorizedEvidenceSnapshot`.
`EvidenceAcquisitionAuthority.authorize` is the sole issuer of an
`EvidenceAcquisitionAuthorization`, and requires a genuine, already-verified
`BirthExperimentSpecificationContentBinding`
(`NoEvidenceAcquisitionAuthorizationWithoutFrozenExperiment`). The
authorization does not accept caller-supplied `experiment_content_id`,
`domain`, `evidence_mode`, `evidence_requirements`, `revision_id`, or
`revision_sequence`: every one of these is a derived property read from the
verified binding, so an authorization can never assert a condition the frozen
experiment did not itself freeze.

An `EvidenceAcquisitionAuthorization` is also the sole issuer of an
`EvidenceAcquisitionRun` (`authorization.open_run(...)`), and an
`EvidenceAcquisitionRun` is the sole issuer of an `AuthorizedEvidenceSnapshot`
(`run.ingest(...)`), closing
`NoAssessableEvidenceSnapshotWithoutAcquisitionAuthorization`: no caller can
construct any of the three objects directly, each raising
`EvidenceAcquisitionAuthorityError` when its authority token is missing.
`CanonicalEvidenceContentEncoder` is the sole issuer of the ingested payload's
`EvidenceContentIdentity`; a snapshot never accepts a caller-supplied content
identity. This keeps `EvidenceOccurrenceIdentity != EvidenceContentIdentity`:
`snapshot_id`, `run_id`, and `authorization_id` name one acquisition
occurrence, while `content_id` is a digest over the ingested bytes, shared by
any two occurrences that ingest byte-identical content.
`BirthAssessmentRequest` further checks that its evidence snapshot's
`experiment_content_id` equals its own experiment binding's `content_id`,
rejecting a snapshot authorized under a different frozen experiment.

`AuthorizedCapture != ProofOfExternalAcquisitionChronology`: this stage does
not prove when or how evidence was first observed or produced outside this
process, and pre-existing evidence could still be ingested through an
authorized run. It also does not claim anything about evidence quality:
`AuthorizedEvidence != SufficientEvidence`, and authorized evidence does not
imply `ResidualSurvival` or `Birth`. G0.2a.3 issues no `ResidualAssessment`
and no `BirthVerdict`.

### G0.2a.3.1 — Issuer-scoped occurrence issuance integrity

G0.2a.3 alone let `authorization_id`, `run_id`, and `snapshot_id` be any
non-empty, caller-chosen string: nothing stopped
`EvidenceAcquisitionAuthority.authorize` from issuing two authorizations for
the same `authorization_id`, an authorization from opening the same `run_id`
twice, or a run from ingesting two different payloads under the same
`snapshot_id`. These strings were therefore `EvidenceOccurrenceCoordinates`
with real provenance, but not yet a proven `EvidenceOccurrenceIdentity`:
`same(id)` did not imply `same(occurrence)`, since an issuer would accept the
id again.

Each issuer now keeps its own registry of the ids it has already issued and
rejects a repeat with `EvidenceAcquisitionAuthorityError`: an
`EvidenceAcquisitionAuthority` instance tracks its issued `authorization_id`s,
one `EvidenceAcquisitionAuthorization` tracks its own issued `run_id`s, and
one `EvidenceAcquisitionRun` tracks its own issued `snapshot_id`s (rejecting a
repeat even when the later `ingest` call carries different content). Each
registry's check-and-insert is synchronized with an internal lock, so
concurrent calls on the same authority, authorization, or run instance cannot
race past the uniqueness check. This makes issuance injective within its
declared scope: two ids issued by the same issuer are equal only if they name
the same occurrence, and distinct ids issued by the same issuer always name
distinct occurrences. This is `IssuerScopedOccurrenceUniqueness`, precisely:

```
forall issuer, id:
    Issued_issuer(o1) = id and Issued_issuer(o2) = id => o1 = o2
```

This is deliberately **not** named `EvidenceOccurrenceIdentity`, because
`LocalInjectivity != PortableIdentity`: proving an id is never repeated
*within one issuer's own registry* does not prove it is never repeated
*across issuers*. Nothing in `AuthorizedEvidenceSnapshot` carries an
`issuer_scope_id`, so two distinct `EvidenceAcquisitionAuthority` instances
remain two distinct, uncoordinated issuance scopes: each is free to issue
`authorization_id="a1"`, whose `open_run("r1")` issues `run_id="r1"`, whose
`ingest(snapshot_id="s1", ...)` issues `snapshot_id="s1"`, and nothing in the
resulting snapshot's comparable fields (`snapshot_id`, `run_id`,
`authorization_id`, `experiment_content_id`, `domain`, `evidence_mode`,
`trace`) distinguishes which authority issued it. If both authorities also
share the same frozen experiment binding, payload, and trace, the two
snapshots' comparable representations coincide even though the two
acquisition occurrences are genuinely independent
(`Occurrence_A != Occurrence_B` yet
`Representation(Occurrence_A) == Representation(Occurrence_B)`). A portable
identity would require an issuer-scope identity of its own -- one that
carries its own issuance authority rather than being another caller-chosen
string -- propagated through `Authorization -> Run -> Snapshot`; that is not
built here. So the accurate judgment is:

```
IssuerScopedOccurrenceUniqueness = PROVED
PortableEvidenceOccurrenceIdentity = DEFERRED
```

`BirthAssessmentRequest` does not hold an authority or issuer-scope object
either: it only checks `snapshot.experiment_content_id ==
binding.content_id`, so it cannot and does not distinguish which authority
scope produced an otherwise-matching snapshot. This is an accepted, narrower
surface than a caller might assume from the name "occurrence identity" alone,
and is the reason this stage's claim is `IssuerScopedOccurrenceUniqueness`,
not `EvidenceOccurrenceIdentity`.

This closes `IssuerScopedOccurrenceUniqueness` only within each issuer's own
scope, not globally: two different `EvidenceAcquisitionAuthority` instances
are two different issuance scopes, and nothing proves their respective
`authorization_id`s differ from one another. `EvidenceAcquisitionAuthority()`
remains a construction boundary, not a permission or security authority --
identical to how `StructuralAdmissionGate` construction is not itself a claim
of external authorization.

`EvidenceAcquisitionRun` and `EvidenceAcquisitionAuthorization` are
`ExternallyFrozen, InternallyStatefulAuthority` objects, not plain immutable
value objects: their dataclass is `frozen=True` so their *own* declared
identity fields (`run_id`, `authorization_id`, `binding`, etc.) can never be
reassigned after construction, but each also holds a private, mutable
`_issued_*` registry `set` and a `threading.Lock` (both `compare=False`,
`repr=False`, `init=False`) as internal operational bookkeeping state. This
bookkeeping is deliberately excluded from equality, `repr`, and from any
content-identity computation (it is never hashed or serialized into
`EvidenceContentIdentity` or any experiment content identity): it exists only
to enforce this stage's issuance uniqueness, not to describe the object's own
identity or content.


### G0.BA.1a — Authorized evaluator implementation binding

G0.2a's `BirthAssessmentEvaluatorRegistry` authorizes evaluator
*declarations* for an exact `(domain, role, target_id, evaluator_id)` scope
and explicitly performs no assessment. That leaves a narrower residual than
"birth assessment execution is missing": `AuthorizedBirthAssessmentEvaluatorDefinition`
does not, and must not, imply `AuthorizedEvaluatorImplementation`, and neither
implies `EvaluatorExecution`. This stage closes exactly that one narrower
question: can an already registry-authorized definition be bound to an exact
implementation identity and executed through an authority boundary that
produces a non-caller-constructible record?

`AuthorizedBirthAssessmentEvaluatorDefinition` is preserved completely
unchanged; it gains no execution semantics here. A separate
`AuthorizedBirthEvaluatorImplementationBinding` binds one such definition to
one `implementation_identity` and one executable callable.
`BirthEvaluatorImplementationRegistry.register` is the only way to construct
one, and it requires the caller to already hold a genuine, registry-issued
`AuthorizedBirthAssessmentEvaluatorDefinition` -- a bare evaluator id string
cannot substitute for it. `BirthEvaluatorImplementationRegistry.seal` freezes
the registered bindings into a `SealedBirthEvaluatorImplementationRegistry`,
which resolves only by the exact five-part scope
`(domain, role, target_id, evaluator_id, implementation_identity)`; an
unregistered implementation identity, or a definition mismatched on domain,
role, target, or evaluator id, is rejected rather than silently resolved.

`BirthEvaluatorExecutionGate.execute` is the sole authority that may invoke a
bound implementation. It resolves the exact binding, re-checks that the
resolved binding's own definition equals the caller-supplied definition,
requires the request's frozen experiment domain to match the definition's
domain, and calls the bound implementation with the caller-supplied input
content. The bound implementation must return `(output_content, trace)`; any
other shape is rejected. Only the gate can construct the resulting
`BirthEvaluatorExecutionRecord`, which preserves the exact authorized
definition, implementation identity, role, target, the exact
`BirthAssessmentRequest`, that request's own bound `AuthorizedEvidenceSnapshot`
(not a caller-substituted one), input content, output content, and trace.

This record answers only "did a specific, registry-bound implementation run
within the context of a specific, authorized assessment request, while
preserving that request and its attached evidence reference?"
(`ExecutedInContextOfAuthorizedRequest + AttachedEvidenceReference`, not
`ExecutedAgainstAuthorizedEvidence`): `EvidenceAttachedToRecord !=
EvaluatorExecutedOnEvidence`, and `InputProvenance = DECLARED_DEFERRED`. It
carries no
`ResidualEvaluationResult`, `WeakerModelEvaluationResult`,
`ClosureEvaluationResult`, aggregate execution status, residual survival,
weaker-model exhaustion, `BirthCandidate`, `IndependentClosure`,
`BirthVerdict`, or `Freeze` meaning:

```
Definition != ImplementationBinding != ExecutionRecord != Assessment
```

Composing per-role execution records (residual, weaker-model, closure) into
any assessment, and any question of whether the frozen weaker-model family as
a whole has been exhausted (`WeakerFamilyExhausted <=> forall W_i in
FrozenWeakerSet: AuthorizedExecution(W_i)`, distinct from
`Executed(W_i)` for any single model), remain separate, later, and still
undecided questions. This stage does not assume they will be closed next, or
in this shape; it closes only the one question stated above.


G0.2 is split into smaller authority-preserving stages. G0.2a defines only
executable assessment contracts: `ResidualDefinitionSpec` identifies the
residual domain, input projection, output schema, evaluator-id declaration,
invariants, and failure semantics; each `WeakerModelSpec` binds a frozen weaker
model to its evaluator, information loss, result schema, and exact poset
relations; and `ClosureCriterionSpec` defines the local
`Close(W_i, R) ∈ {CLOSE, FAIL_TO_CLOSE, DEFER}` vocabulary for weaker-model
closure. `BirthAssessmentSemanticsContract` validates that these executable
contracts match the frozen residual-definition and closure-criterion
identities, experiment, domain, queried projection, prerequisite cone, schemas,
and poset relations. Matching only domain or schema is insufficient:
`NoResidualDefinitionDriftAfterFreeze` and
`NoClosureCriterionDriftAfterFreeze` require exact identity equality.

Evaluator ids in these contracts are declarations only:
`DeclaredEvaluatorId != AuthorizedEvaluator`. `CallerDoesNotOwnEvaluatorAuthority`
requires registry-issued definitions before those ids can become authorized for
an exact `(domain, role, target_id, evaluator_id)` scope.
`BirthAssessmentEvaluatorRegistry` and
`SealedBirthAssessmentEvaluatorRegistry` provide that sealed definition
boundary while executing no assessment. G0.2a obeys `NoVerdictYet`: it issues
no `ResidualAssessment`, `BirthCandidate`, `BirthVerdict`, `Freeze`, or E0
result.

G0.2a's id-equality checks close *label* identity, not *content* identity:
`SameId` does not imply `SameSemantics`. G0.2a.1 closes that separately.
`ResidualDefinitionId != ResidualDefinitionContentIdentity`, and the same
distinction holds for `ClosureCriterionSpec` and `WeakerModelSpec`.
`CanonicalBirthSemanticsEncoder` issues immutable canonical manifests and
`BirthSemanticsContentIdentity` digests for each; `BirthSemanticsContentRegistry`
freezes the canonical bytes of the first canonical content bound to an exact
`(domain, role, target_id)` scope, rejecting later content drift under the
same id; and `BirthAssessmentContentBinding` proves
exact canonical-byte equality for the residual definition, the closure
criterion, and every weaker model bound to a `BirthAssessmentSemanticsContract`.
This closes `NoDeclaredSemanticDigestDriftAfterFreeze`; the registry retains
the canonical bytes and binding compares those bytes directly, so it also
enforces `ExactCanonicalContentFreeze` rather than treating digest equality as
content equality. G0.2a.2 separately gives every complete
`BirthExperimentSpecification` an encoder-issued canonical manifest and
content identity, covering its revision, evidence mode, domain, poset, query
and hypothesis, residual/closure declarations, and evidence requirements.
`PreEvidenceSpecificationRegistry` alone issues a
`FrozenPreEvidenceExperimentManifest`; semantic-registry sealing requires that
manifest, so a semantic snapshot cannot float independently of its frozen
experiment specification. All canonical encoders enforce schema coverage:
every declared field is either encoded or listed as an explicit derived
exclusion, including `ProjectionPoset`, `BirthQuery`, and
`StructureHypothesis`; adding an unaccounted field rejects encoding. It still
performs no evaluation and
issues no birth authority. `EvaluatorId != EvaluatorImplementationIdentity`
remains open: this stage authorizes evaluator *declarations*, not evaluator
*implementations*. `G0.BA.1a` already provides a runtime invocation boundary
that resolves evaluator execution through a registry-owned implementation,
never a caller-supplied callable, but proves only registry-bound invocation:
`ImplementationIdentityIsContentAuthenticated = DEFERRED`. Any later runtime
that claims reproducible or content-authenticated evaluator implementation
identity must instead bind that implementation to independently
authenticated content; `G0.BA.1a` does not yet close that requirement
(`AuthorizedCallableInvocation != ReproducibleImplementationIdentity`).

Later G0.2 stages alone may implement the complete authority chain:
`BirthAssessmentRequest -> ResidualAssessment ->
LicensedWeakerExhaustion -> NecessaryInvariantCandidate -> BirthCandidate ->
IndependentClosureDecision -> gate-issued BirthVerdict -> Freeze -> E0`.
That gate must assess every relevant incomparable model itself; callers cannot
omit a competitor or promote string placeholders as discriminating evidence.
It must keep `Freeze` distinct from the subsequent `E0` assessment. No
Arabic-specific type is part of G0.1 or this deferred G0.2 design.

### G0.BA.1b — Evidence-derived evaluator input provenance

G0.BA.1a states three claims it refuses to make. This stage closes exactly
one of them, `InputProvenance = DECLARED_DEFERRED`, and leaves the other two
standing.

The refused claim is precise. `BirthEvaluatorExecutionGate` invokes a
registry-bound implementation on *caller-supplied* `input_content` and
attaches the request's own `AuthorizedEvidenceSnapshot` for audit, but
nothing there relates the two. A `BirthEvaluatorExecutionRecord` therefore
proves that an implementation ran on *some* content alongside *some*
authorized evidence -- never that the one came from the other
(`EvidenceAttachedToRecord != EvaluatorExecutedOnEvidence`). Passing the real
measured numbers rather than invented ones was, at that boundary, a caller's
discipline and not a kernel guarantee.

The correction is structural rather than a comparison bolted onto the old
gate. An `EvaluatorInputDerivation` receives exactly one argument: the
`canonical_bytes` of the request's own authorized evidence manifest. It is
handed nothing else, so it cannot source content from outside that snapshot
except by ignoring its input, which the recorded derivation identity then
exposes. `EvaluatorInputDerivationGate.derive` accepts no `input_content`
parameter and no domain parameter at all (`CallerDoesNotOwnInputContent`):
the caller chooses *which* authorized derivation runs, never what the
evaluator sees, and the domain is read from the request's own frozen
experiment specification.

The authority shape is the one used throughout this repository.
`EvaluatorInputDerivationRegistry.register` is the sole issuer of an
`AuthorizedEvaluatorInputDerivationBinding`; `seal` alone produces a
`SealedEvaluatorInputDerivationRegistry`, which resolves only by the exact
three-part scope `(domain, derivation_id, implementation_identity)`; and only
`EvaluatorInputDerivationGate.derive` may issue an
`EvidenceDerivedEvaluatorInput`. Before deriving, the gate re-verifies that
the snapshot's own bytes hash to the snapshot's own `EvidenceContentIdentity`.
A derivation that returns non-text, returns blank content, or returns a
different result for the same authorized bytes is rejected. That last check
rejects *observed* nondeterminism only: `ObservedDeterminism != ProvenPurity`.

Identity binds the whole triple, not the output alone.
`CanonicalEvaluatorInputDerivationEncoder` digests the source evidence
content identity, the derivation id, the implementation identity, and the
produced content together under length-prefixed canonical bytes, so no two
distinct tuples share an encoding by concatenation. The issued
`EvaluatorInputContentIdentity` therefore records what was produced, from
which exact evidence, and by which declared derivation:

```
OutputDigest != DerivationIdentity
```

Execution stays layered, not rewritten.
`ProvenanceBoundEvaluatorExecutionGate.execute` delegates the invocation
itself to the completely unchanged `BirthEvaluatorExecutionGate`, then binds
the issued record to the derivation that produced its input: the same
request object, the same evidence snapshot object, and exactly the derived
content. G0.BA.1a keeps `InputProvenance = DECLARED_DEFERRED` and still
accepts unrelated caller-supplied input by design; provenance is proven only
for records this stage issues.

Three claims remain refused here, and must not be read into a
`ProvenanceBoundEvaluatorExecutionRecord`:

* `DerivationIdIsContentAuthenticated = DEFERRED`. `derivation_id` and
  `implementation_identity` are plain, caller-chosen strings, exactly as in
  G0.BA.1a, with no canonical manifest or digest of the derivation code
  (`DeclaredDerivationId != DerivationContentIdentity`). The
  `declared_transformation` text is carried for audit and never verified
  against the callable (`DeclaredTransformation != VerifiedTransformation`).
  What is proven is that this record's input came from this evidence through
  *the* callable registered under that name -- not that the name describes
  the callable truthfully.
* `AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment`,
  inherited unchanged from G0.BA.1a: the execution boundary still matches
  only `domain`.
* `ProvenInputProvenance != AssessedEvidence`. `is_assessment` is `False`
  unconditionally. Knowing that an evaluator truly ran on the authorized
  evidence says nothing about what its output means, so the record carries
  no residual survival, weaker-model exhaustion, closure, `BirthCandidate`,
  `IndependentClosure`, `BirthVerdict`, or `Freeze` meaning:

```
Derivation != ExecutionRecord != Assessment
```

This stage does not move `IndependentClosureAssessment.is_independent_closure`
off `False`. It removes a necessary-but-insufficient obstacle beneath the two
conjuncts AIM-K3 still lacks: an authority that evaluates residual survival
and licensed weaker exhaustion. Such an authority would previously have been
built on input no gate could relate to the authorized evidence; it now has a
boundary to build on, and nothing more.

## G0.IC.1b — Evidence-derived weaker-model closure outcome

`ClosureCriterionSpec` already declared the closed outcome vocabulary of
`Close(W_i, R)`, the frozen projection poset already derived which weaker
models must be closed, and G0.BA.1b already proved that an evaluator ran on
this request's own authorized evidence. What no authority did was relate an
evaluator's output string to a member of that closed vocabulary.

`DeclaredClosureOutcomeVocabulary` is that relation, declared as data by the
closure criterion's owner and frozen in a sealed registry before any gate
reads it. It must cover every `ClosureAssessmentStatus` member exactly once,
so no declared outcome is unreachable by construction and none is silently
dropped:

```
DeclaredToken -> ClosureAssessmentStatus, exact match or refusal
```

The gate reads, and does not decide:

* `CallerDoesNotOwnClosureOutcome`. `WeakerModelClosureGate.assess` accepts
  no status, no reason, and no outcome claim.
* `ExactTokenOrRefusal`. An output outside the declared vocabulary is refused
  by model id. It is never mapped to `DEFER` as a convenience, because reading
  ignorance as a declared outcome is the exact failure this gate prevents.
* `VocabularyIsBoundToFrozenCriterionContent`. Authorization requires a
  verified `BirthAssessmentContentBinding`, and the gate additionally requires
  the resolved vocabulary's contract to carry this request's own frozen
  experiment specification.

What this stage does not reach:

```
LocalClosureOutcome != WeakerModelExhaustion != IndependentClosure
```

A certificate speaks for one model in the cone. Nothing here aggregates the
cone, and `IndependentClosureAssessment.is_independent_closure` is untouched
and still `False`. `DeclaredVocabularyIsNotProvenSemantics` and
`SealedBeforeAssessmentIsNotSealedBeforeEvidence` remain open by name: a
frozen map cannot be tailored to an output already seen, but it proves nothing
about why the evaluator emitted that token, and no authority here timestamps a
seal against an evidence acquisition run.

## G0.IC.1c — Derived weaker-model exhaustion

G0.IC.1b answers one weaker model and says so: its certificate's
`is_weaker_model_exhaustion` is `False` unconditionally, because one model is
not the set. This stage is the set, and nothing more.

The set was already derived rather than written, so the question has a
decidable shape -- exact coverage of a frozen finite cone -- and this gate
answers only that shape:

```
coverage of frozen_weaker_models, exactly once, then aggregation
```

Coverage before judgement, copied from `assess_all_preserved`:

* A missing model is refused, never read as exhaustion-so-far
  (`MissingModelIsNotFailureToClose`).
* A model named twice is refused, because two outcomes for one model would let
  ordering choose the result.
* A model outside the frozen cone is refused, because the poset never licensed
  it (`FrozenPosetIsTheLicensedSet`).

Then the declared precedence, mirroring `BLOCK > DEFER > VERIFIED`:

```
WEAKER_MODEL_CLOSES_RESIDUAL
  > EXHAUSTION_UNDETERMINED
  > LICENSED_WEAKER_MODELS_EXHAUSTED
```

A single `CLOSE` outranks every deferral, because knowing that some weaker
model *does* close the residual is knowledge an unrelated `DEFER` must not
erase.

What this stage does not reach:

```
WeakerModelExhaustion != IndependentClosure
```

Two of three conjuncts are now derived -- comparability by G0.IC.1a and
exhaustion here. The third, a residual surviving under
`NoBirthWithoutResidualOrFormalNecessity`, is certified by no authority in this
repository, so `is_independent_closure` remains `False` and
`IndependentClosureAssessment` is untouched. `WeakerModelClosesResidual !=
NoBirthVerdict`, `CoverageIsNotCorrectness`, and
`SameRequestIsNotSameEvidenceRun` remain open by name.

## G0.IC.1d — Evidence-derived residual survival outcome

G0.IC.1a and G0.IC.1c each said the same thing about the conjunct they did not
reach: a residual surviving under `NoBirthWithoutResidualOrFormalNecessity` is
certified by no authority in this repository. This stage is that reading, for
one witness, and nothing more.

Nothing new is invented. The residual whose survival is at stake is already
declared by `ResidualDefinitionSpec`, and the closed three-member vocabulary of
a survival reading is declared on that same frozen contract
(`supported_statuses`), exactly as `ClosureCriterionSpec` declares the
vocabulary of `Close(W_i, R)`. The single missing relation is the one G0.IC.1b
supplied for closure outcomes:

```
evaluator output_content --(frozen declared vocabulary)--> ResidualSurvivalStatus
```

`ExactTokenOrRefusal` is inherited verbatim: exact string equality, no
trimming, no case folding, no prefix match, no default, and an unrecognized
output refused by residual id rather than read as `DEFER`. A record under any
role other than `RESIDUAL_DEFINITION`, or naming a target that is not the
request's own frozen `residual_definition_id`, is refused too.

The one mode refused by name:

```
MixedModeNeedsTwoScopedWitnesses
```

`evidence_mode` is read from the frozen experiment, never from the caller. A
`MIXED` experiment declares the explicitly typed scoped pair
`<(D_emp, S_emp), (D_formal, S_formal)>`, and no authority here proves those
declared scopes or `NoCrossSubstitution(D_emp, D_formal)`. One certificate that
a later reader could take as having satisfied both modes is exactly the
fabricated closure this constitution refuses, so the gate refuses the mode
instead.

What this stage does not reach:

```
ResidualSurvivalOutcome != IndependentClosure
```

The three conjuncts are now each derived on their own — comparability by
G0.IC.1a, weaker-model exhaustion by G0.IC.1c, and residual survival here — but
**composing** them is a separate question with no authority in this repository.
`is_independent_closure` is therefore still `False` on every branch,
`IndependentClosureAssessment` is untouched, and this stage is wired to neither
it nor `BirthVerdictGate`. `DoesNotSurvive != NO_BIRTH_IN_SCOPE`,
`SurvivalReadIsNotMeasuredReplicatedResidual`, `FormalNecessityIsNotProvedHere`,
`DeclaredVocabularyIsNotProvenSemantics`,
`SealedBeforeAssessmentIsNotSealedBeforeEvidence`, and
`OneWitnessIsNotResidualCertification` remain open by name.

## G0.IC.1e — Composed independent-closure decision

G0.IC.1a, G0.IC.1c and G0.IC.1d each closed one conjunct of
`IndependentClosure`, and each said the same thing in the same words: composing
them is a separate question with no authority in this repository. This stage is
that composition, and nothing more.

Nothing new is read:

```
ThreeReadingsAreNotAFourth
```

The gate opens no evidence, executes no evaluator, and inspects no frozen poset.
Every input is already a gate-issued reading, and a composition that re-derived
any conjunct would be a second authority over a question already answered — two
authorities whose answers could disagree.

`CallerDoesNotOwnComposition`: `IndependentClosureCompositionGate.assess` takes
exactly three parameters — the comparability assessment, the exhaustion
assessment and the survival certificate — and no status, no reason, and no
closure claim. `OneRequestOrRefusal`: the three readings must speak for the same
`BirthAssessmentRequest`, compared by object identity exactly as G0.IC.1c
requires of its certificates, and the survival reading must carry that request's
own authorized evidence snapshot. A comparability result for one frozen
experiment composed with a survival reading of another would be a closure claim
no single experiment ever supported.

The enumeration performed before the module was written. Comparability is
two-valued and exhaustion and survival are three-valued, so there are exactly
`2 x 3 x 3 = 18` combinations. Each conjunct falls into exactly one of three
roles:

* *satisfied* — `COMPETITION_RESOLVED_IN_POSET`,
  `LICENSED_WEAKER_MODELS_EXHAUSTED`, `SURVIVES`.
* *refuting* — `WEAKER_MODEL_CLOSES_RESIDUAL`, `DOES_NOT_SURVIVE`.
* *undetermined* — `EXHAUSTION_UNDETERMINED`, `DEFER`,
  `COMPETITION_UNRESOLVED_IN_POSET`.

```
UnresolvedComparabilityIsIgnoranceNotRefutation
```

Comparability has no refuting branch at all. G0.IC.1a already resolves
`AbsentRelation != DeclaredIncomparability` conservatively, so its unresolved
branch means the frozen poset did not settle the relation — not that a competing
explanation was established. Reading it as a refutation would manufacture
knowledge out of silence, the mirror image of the fabricated closure this chain
forbids.

Aggregation follows the precedence already enforced twice in this kernel
(`BLOCK > DEFER > VERIFIED`, and `WEAKER_MODEL_CLOSES_RESIDUAL >
EXHAUSTION_UNDETERMINED > LICENSED_WEAKER_MODELS_EXHAUSTED`):

```
CLOSURE_REFUTED_IN_SCOPE
  > CLOSURE_UNDETERMINED_IN_SCOPE
  > CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION
```

A single refuting conjunct outranks every deferral (`False and Unknown ==
False`), and refuted and undetermined conjuncts are tracked in separate fields,
as `InvariantVerificationDecision` tracks `failed_components` and
`deferred_components`, reported in a fixed conjunct order independent of caller
order. Of the 18 combinations, 10 are refuted, 7 are undetermined, and exactly 1
— resolved comparability, exhausted licensed weaker models, and a surviving
residual — reaches the third status.

What this stage does not reach:

```
SatisfiedConjunctsIsNotIndependentClosure
```

Even that one reachable combination yields `is_independent_closure == False`.
The three conjuncts hold *as read*, and reading is all that happened. Three
barriers already declared by the stages that produced these very inputs stand
between that and closure: `OneWitnessIsNotResidualCertification` (G0.RC.1 is
deferred, so no certified residual exists to be closed over),
`SurvivalReadIsNotMeasuredReplicatedResidual`, and `CoverageIsNotCorrectness`
with `FrozenConeIsDeclaredNotProven`. The status name states exactly what was
reached and what it is pending on, rather than overstating it; AIM-K3 is thereby
narrowed by name, not declared met.

`CompositionIsNotAVerdict`. This stage is deliberately not wired to
`BirthVerdictGate`, and the readings it consumes are untouched: their own
`is_independent_closure` properties remain `False` constants.
`ClosureRefutedInScope != NO_BIRTH_IN_SCOPE` — a refuted conjunct is the shape
of an argument against birth in this scope, not that verdict. This stage issues
no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no
`TraditionalName`.

## G0.MA — Meta-architecture law (declared law, no runtime yet)

This law governs every future stage that searches for, selects, or names a
pattern, factorization, or architecture -- including any future extension of
G0.BA beyond G0.BA.1a, and any future stage of G0.F. It is declared now, as
law only, with no accompanying type or gate, precisely so that it constrains
those future stages before their first line of runtime code is written.

The recurring risk this law closes: an agent (human or automated) with
foreknowledge of common pattern-discovery techniques -- bigrams, trigrams,
graphs, hypergraphs, transformers, or any other named architecture -- reaches
for one of them because it is familiar, not because the system's own frozen
residuals have forced it. That is exactly the same failure mode `G0.BV.1` and
`G0.BA.1a` were written to refuse for birth verdicts and evaluator execution:
naming or licensing a structure before the evidence that would force it.

The following are declared, law-only constraints; none has a runtime
enforcement mechanism yet:

* `NoPredeterminedPatternArchitecture` -- no future stage may fix, in
  advance, which family of pattern-recognition architecture (bigram,
  trigram, graph, hypergraph, transformer, or any other) will be used to
  discover structure in residuals. The choice must be an output of the
  process, never an input to it.
* `PatternType ∉ PriorOntology` -- the vocabulary of pattern types available
  to a future discovery stage is not fixed by this constitution, this
  codebase, or any prior stage's ontology. A pattern type is only real once
  something forces its birth; it cannot be pre-declared "just in case."
* `NoPatternNameBeforeIndependentBirth` -- a pattern may not be named,
  typed, or exposed as an API surface before an independent birth process
  (mirroring G0.1-G0.BV.1's own chain) has forced it into existence. A name
  is not a license: naming ahead of birth is exactly the failure this law
  refuses.
* `LicensedStructuralDemandConstrainsArchitectureSearch` -- whatever
  architecture search a future stage performs must be constrained by the
  actual licensed structural demand on hand, not by a convenient or popular
  prior architecture. Licensed structural demand is evidence-mode-sensitive
  (`LicensedStructuralDemand_n = Demand(EvidenceMode_n)`), because
  `NoBirthWithoutResidualOrFormalNecessity` already declares three
  independent evidence modes and architecture search must not contradict
  them:
  `Demand(EMPIRICAL) = CertifiedResidualGeometry`,
  `Demand(FORMAL) = CertifiedFormalNecessityWitness`, and
  `Demand(MIXED) = <(D_emp, S_emp), (D_formal, S_formal)>` -- an explicitly
  typed *scoped* pair, not a sum: `S_emp` and `S_formal` are independently
  declared scopes of the claim, with no prior assumption that they are
  disjoint, equal, or exhaustive (the same part of a claim may need both
  formal necessity and empirical support), and
  `NoCrossSubstitution(D_emp, D_formal)` -- neither component may compensate
  for the other on the part of the claim that belongs to it
  (`FormalProof ⇏ EmpiricalReality`,
  `EmpiricalPattern ⇏ MathematicalNecessity`). Licensed demand is not
  claimed to be the only thing constraining search overall: frozen prior
  structure, admissibility, licensed operations, and prior invariants also
  constrain every future search, alongside the licensed demand:
  `Search_{n+1} = ConstrainedBy(FrozenPrior_n, LicensedOperations_n,
  LicensedStructuralDemand_n)`. What licensed structural demand alone
  licenses is new structural complexity:
  `NewStructuralComplexity must be demanded by LicensedStructuralDemand_n`,
  not by `rho_n` alone.
* `NoFixedComplexityOrder` -- no future stage may assume, in advance, an
  ordering of model complexity (for example, "try bigrams before trigrams
  before graphs") as a structural law. Any such ordering, if it appears,
  must itself be derived from evidence, not declared upfront.
* `FuturePossibility != CurrentImplementationLicense` -- that a future
  architecture is conceivable, discussed, or even likely, does not license
  building it now, or building scaffolding for it now. This mirrors
  `RoadmapKnowledge != ExecutionAuthority` below at the level of technical
  architecture rather than agent process.
* `AgentRoadmapKnowledge != ExecutionAuthority` -- an agent's own knowledge
  of where a roadmap is likely headed is not, by itself, authority to
  implement the next stage in the same session that closed the current one.
  What licenses the next stage is the next session's fresh audit of the
  frozen parent's own residuals, not carried-over foresight.

These combine into one governing law for any future architecture search:

```
Architecture_{n+1} = Min_ (relation)
    { A : Preserve(A_n) and SatisfyLicensedDemand(A, D_n)
          and Validation_n(A) }
```

where `D_n = LicensedStructuralDemand_n`. That is: the next architecture is
the *minimal* structure (under whatever partial order the future stage
defines and justifies) that preserves the previous architecture's proven
guarantees, satisfies the licensed structural demand that forced this step,
and passes the evidence-mode-sensitive validation of its own claim.
Satisfaction is itself mode-relative
(`Demand != Residual`: a residual is only the EMPIRICAL special case of
licensed demand, so the satisfaction relation is named neutrally rather than
borrowed from residual logic): in `EMPIRICAL` mode,
`SatisfyLicensedDemand(A, D)` specializes to residual closure
(`Close(A, CertifiedResidualGeometry)`); in `FORMAL` mode, it means that `A`
realizes -- fulfills and instantiates -- the structural necessity that the
`CertifiedFormalNecessityWitness` proved within its frozen formal domain,
not that it "closes a residual" (a necessity witness is not a residual to be
closed); in `MIXED` mode, each component of the typed scoped pair
`<(D_emp, S_emp), (D_formal, S_formal)>` is satisfied by its own mode's
relation within its own declared scope.
Validation is mode-relative
(`Validation_n(A) = Validation(EvidenceMode_n, A)`), matching
`NoBirthWithoutResidualOrFormalNecessity`'s three modes:
`Validation(EMPIRICAL, A) = HeldOutStable(A)` -- the architecture remains
stable under held-out evidence it was not fitted to;
`Validation(FORMAL, A) = ExhaustivelyProvedClosure(A)` -- exhaustive formal
closure over the declared closed domain, with no held-out measurement
required, since a formal birth needs no measurement run; and
`Validation(MIXED, A) = Validation_emp(A | S_emp) and
Validation_formal(A | S_formal)` -- each mode's validation applies to `A`
restricted to its own declared scope, with no assumption here about whether
the two scopes overlap, are disjoint, or are exhaustive, and with neither
substituting for the other. No future stage may skip the
minimality requirement by asserting that a richer, named architecture is
"obviously" going to be needed eventually --
`FuturePossibility != CurrentImplementationLicense` applies here exactly as
everywhere else in this constitution.

One deferred residual is exposed by this reconciliation and recorded here
without being closed: G0.F's stated *general* factorization law below
(`K_L -> Residual(O_L | K_L) -> candidate factorizations`) is still
residual-only and has not yet been reconciled with the `FORMAL`/`MIXED`
birth paths that `NoBirthWithoutResidualOrFormalNecessity` declares
(`G0.F EvidenceModeConsistencyNotAudited`). Auditing and, if needed,
reconciling G0.F's general law is a separate future frozen-parent question;
this section neither modifies G0.F nor licenses doing so now.


G0's chain as written above reads as *one* candidate object, closed
independently and frozen. That phrasing is a special case, not the general
law: a domain `L`'s residual over everything frozen prior to experiment
(`K_L`) does not name in advance how many candidate objects, or which ones,
would close it. Requiring `Residual(O_L | K_L) = 0` may force a single
factor, several jointly-necessary factors, or none at all
(`NO_BIRTH_IN_SCOPE`). This section restates G0's chain, for any domain `L`,
as closing a **minimal sufficient irreducible factorization** rather than a
single named object, and it is held to the same discipline as G0: **law
only**, ahead of any runtime, ahead of any Arabic-specific folder structure,
and ahead of any decision about how many factors traditional grammar expects.

```
K_L -> Residual(O_L | K_L) -> candidate factorizations F (poset-ordered)
    -> Sufficiency(F) & FamilyMinimality(F) & ComponentIrreducibility(F)
    -> IndependentClosure -> BirthVerdict -> Freeze(F*) -> Bridge stage -> E0
```

`Bridge stage`: once (and only once) two factors are each independently
frozen, a *separate* birth protocol -- not automatic adjacency -- decides
whether any relation between them is itself born or merely derived. `E0`
here names a mapping graph from the frozen factor/bridge network to external
(traditional) terminology, not a single rename step. Neither the
factorization runtime nor the bridge runtime nor the E0-mapping runtime is
implemented by this section; as with G0, only the constraints they must
satisfy are frozen now.

| Law | Status | Scope |
| --- | --- | --- |
| `NoTraditionalSchemaBeforeFactorization` | DECLARED_DEFERRED | A domain `L`'s factorization is discovered from `Residual(O_L \| K_L)`, never assumed from a traditional grammatical schema (for example, a presumed phonology/morphology/syntax/semantics split) before that residual is examined. A traditional category name may describe a result after `E0`; it must never seed or constrain the search for one. |
| `NoPredeterminedFactorCount` | DECLARED_DEFERRED | No experiment, spec, or runtime may fix in advance how many factors a domain's minimal factorization contains. `Residual(O_L \| K_L) = 0` licenses `NO_BIRTH_IN_SCOPE` for the whole domain; a nonzero residual licenses exactly the factor family the closure proof produces, whether that is one factor, several, or (pending further evidence) none yet decidable. |
| `FactorizationMinimalityIsPartialOrderRelative` | DECLARED_DEFERRED | The set of admissible minimal factorizations for `L` is `M_L = Min_{≺_L}{F : Sufficient_L(F) and Closed_L(F)}`, where `≺_L` is the domain's frozen partial order over candidate factor families and `Min` selects its minimal elements. `M_L` is never computed as `argmin` of a linear/scalar complexity measure: `ProjectionIsNotOntology`'s ban on assuming a total-order complexity vector across projections applies equally here to factor families. |
| `MultipleIncomparableMinimalFactorizationsDefer` | DECLARED_DEFERRED | If `\|M_L\| > 1` and two members of `M_L` are pairwise incomparable under `≺_L` (neither is derivable from, nor a refinement of, the other under currently licensed weaker models), no verdict may pick one: the assessment is `DEFER_IN_SCOPE`, mirroring `NoRicherStructureBeforeLowerOpenResidualClosure`'s treatment of an incomparable competing explanation, until discriminating evidence resolves the competition. |
| `DerivedRelationDoesNotBirth` | DECLARED_DEFERRED | A relation between two already-frozen factors `F_i`, `F_j` is not itself a candidate for birth merely because both endpoints exist. If the relation's value is fully reconstructible from `F_i`, `F_j`, and shared already-frozen context (`ReconstructibleRelation => Derived, not Born`), it is recorded as a derived relationship (`D*`), not promoted to an ontology object, regardless of how useful or traditionally named that relationship is. |
| `NoBridgeBeforeIndependentEndpointFreeze` | DECLARED_DEFERRED | A `BridgeResidualExperiment(F_i, F_j)` may only be opened after both `F_i` and `F_j` have each already completed their own independent `Freeze`. Endpoint existence as an in-progress candidate, hypothesis, or unclosed factor never licenses opening a bridge experiment between them. |
| `NoBridgeBirthIfReconstructible` | DECLARED_DEFERRED | Given frozen `F_i`, `F_j`, and shared context, if every licensed weaker reconstruction model accounts for the coupling between them (residual `R_ij = 0`), the relation is `DERIVED`, not a `BridgeCandidate`. Only a coupling residual that survives every licensed weaker reconstruction model (`R_ij != 0` after exhaustion) may proceed to `BridgeCandidate -> IndependentClosure -> Freeze`, mirroring `NoBirthBeforeLicensedWeakerExhaustion` for bridges. |
| `FrozenFactorReopeningRequiresNewRevision` | DECLARED_DEFERRED | A frozen factor's content is fixed at freeze time and is never silently mutated by later evidence. New evidence bearing on an already-frozen factor opens a new, separately recorded revision (mirroring `NoBirthBeforeLicensedWeakerExhaustion`'s treatment of a newly discovered weaker model); it does not erase, edit in place, or retroactively rewrite the original frozen verdict's historical scoped record. |
| `LayerIsDiscoveryJurisdictionNotOntology` | DECLARED_DEFERRED | A domain `L` (however named -- "encoding," "phonology," "morphology," or otherwise) denotes only the scope of experiment, evidence, and residual under examination: a `DiscoveryJurisdiction`, not a promise that factorization will reproduce any traditional layer boundary. A single born factor may cut across what tradition calls two layers, or one traditional layer may fracture into several independently born factors; neither outcome is a failure of this law. |
| `E0IsExternalAuditOnly` | DECLARED_DEFERRED | `E0` maps the frozen factor/bridge network to external (traditional or reference) terminology for audit and communication only. `E0` certifies no birth, closure, or freeze decision, and a factor's or bridge's epistemic status never depends on whether, or how, `E0` maps it to an external name. |
| `E0MappingMayBePartialAndManyToMany` | DECLARED_DEFERRED | The `E0` mapping `Π^E0 : FrozenDiscoveryGraph ⇀ ExternalConceptGraph` is a partial relation, not a total function: an entry may be one-to-one, one-to-many, many-to-one, or absent entirely (a frozen factor with no traditional counterpart, or a traditional term matching no single frozen factor). An unmapped frozen factor, or a traditional term left unmatched, is not itself evidence against either side. |
| `RuleTableIsDerivedArtifact` | DECLARED_DEFERRED | Any future "Arabic rule table" is a compiled, read-only projection of the frozen factor set, frozen bridge set, derived-relation set, and `E0` mapping (`ArabicRuleTable = Compile(F*, B*, D*, Π^E0)`), produced strictly after those inputs are frozen. It is never hand-authored ahead of, or independently of, that frozen network. |
| `NoRuleTableFeedbackIntoDiscovery` | DECLARED_DEFERRED | A compiled rule table, or any traditional inventory or category count it reflects, may never feed back into an open experiment, residual criterion, weaker-model set, or factorization search (`ArabicRuleTable ↛ Discovery`, `TraditionalInventory ↛ FactorCount`, `TraditionalCategory ↛ ResidualCriterion`). Discovery in progress must not be steered toward reproducing a table that has not yet been compiled from it. |
| `NoOracleLabelCriterionOrFunctionLeakBeforeFreeze` | DECLARED_DEFERRED | No caller-supplied oracle label, closure criterion, or evaluator function/callable may be substituted for, or silently override, the frozen residual definition, closure criterion, or weaker-model specifications bound at G0.1/G0.2a, for any stage of factorization, bridge, or `E0` assessment. This extends `EvaluatorId != EvaluatorImplementationIdentity` and `CallerDoesNotOwnEvaluatorAuthority` (G0.2a) to the factorization and bridge stages: a caller may declare which evaluator it expects, but never supply, swap, or leak the executing implementation itself ahead of a sealed registry's authorization. |

These fourteen laws are declared now, before any factorization runtime,
`EvaluatorImplementationIdentity`/execution-authority stage (itself still
open per `EvaluatorId != EvaluatorImplementationIdentity` above), typed
residual/provenance stage, bridge-assessment stage, or `E0`-mapping-audit
stage exists. As with G0, no Arabic-specific `phonology`/`morphology`/
`syntax`/`semantics` (or similarly pre-committed) module or folder is created
by this section, and none should be created merely to anticipate a
factorization that has not yet been discovered
(`LayerIsDiscoveryJurisdictionNotOntology`). This section governs, but does
not implement, the milestones that must be built to close it.

### G0.F.1 — Fractal reopen protocol (declared law, contracts only)

G0.F above closes one experiment's factorization question. Fractality is not
a folder layout; it is the same execution law applied recursively: a frozen
result from one experiment must be capable of being read, unmodified, inside
a *later, higher* experiment, without being reborn, copied, or having its
identity re-decided:

```
Birth -> Freeze -> Reopen -> Residual -> MinimalFactorization
-> Freeze -> Reopen -> ...
```

Formally, for a jurisdiction (domain) `L` at level `n`, given the already
frozen set `F_n = {F_1, ..., F_m}` opened in a new jurisdiction `J_{n+1}`:

```
W_0 = Reopen(F_n) + KnownDerivedRelations
R_{n+1} = Residual(O_{n+1} | W_0)
```

`R_{n+1} = 0` licenses `NoBirthAtReopen`: reopening never forces a new layer
to appear. Otherwise the next frozen layer is exactly:

```
F_{n+1} = Freeze(MinimalFactorization(Residual(O_{n+1} | Reopen(F_{<=n}))))
```

which is itself immediately reopenable, making the recurrence indefinite.
Every higher-layer result is exactly one of three kinds, and the three are
never conflated: a `BornFactor` (irreducible under every licensed weaker
reconstruction), a `DerivedRelation` (reconstructible from already-frozen
factors and shared context; `DERIVED_NO_BIRTH`, per `DerivedRelationDoesNotBirth`
above), or a `BornBridge` (a coupling between two independently frozen
factors that survives every licensed weaker reconstruction model). So:

```
FractalGraph = FrozenFactors + DerivedRelations + BornBridges
```

| Law | Status | Scope |
| --- | --- | --- |
| `BirthOnceFreezeOnceReopenMany` | DECLARED_DEFERRED | A factor is born and frozen exactly once; after that, every later experiment that needs it must `Reopen` that one frozen result rather than re-run its birth. Nothing licenses a second, independent birth of what is content-identically the same factor inside the same scope. |
| `ReopenDoesNotRebirth` | DECLARED_DEFERRED | `Reopen(FrozenFactorRef, E_{n+1})` opens a read-only, licensed window onto an already-frozen factor for use in a new experiment; it is not a second construction of that factor and issues no new `BirthVerdict` for it. Formally `Reopen(F) != Rebirth(F)` and `Id_after(F) == Id_before(F)`: reopening a factor can never change the factor's own declared identity, only license a new question about it. |
| `NoBridgeForSequentialInquiry` | PROVED (at contract level) | A later question about a frozen factor is represented only by `ReopenExperimentSpecification` and, once its result is frozen, `ProofLineageEdge`. A proof-lineage edge records discovery history and is not accepted as a `BornBridgeRef` or `DerivedRelationSpec`. |
| `ParentageIsNotOntologicalRelation` | PROVED (at contract level) | `FractalSnapshot` keeps `proof_lineage_edges` separate from `born_bridges` and `derived_relations`: parentage belongs exclusively to the provenance graph and cannot populate the born ontology or derived-relation graphs. |
| `ProofLineageGraphIsAcyclic` | PROVED (at contract level) | `FractalSnapshot` rejects any cycle in `proof_lineage_edges`, including indirect cycles; reopening an ancestor remains valid because it does not add a reverse ancestor edge. |
| `LineageEdgeBindsExactReopenSpecification` | PROVED (at contract level) | Every `ProofLineageEdge` carries one exact `ReopenExperimentSpecification`; the child birth experiment and declared parent are checked against that specification, with no duplicated lineage identity strings. |
| `FrozenOntologyRefIncludesBornBridge` | PROVED (at contract level) | Reopen and proof-lineage parent references may be either `FrozenFactorRef` or `BornBridgeRef`; `DerivedRelationRef` is not an ontology reference and cannot become a lineage parent. |
| `DistinctBridgeExperimentFromEndpointExperiments` | PROVED (at contract level) | `BornBridgeRef` requires a bridge birth experiment identifier distinct from every endpoint birth experiment identifier. This is identifier-level contract evidence only; independent endpoint birth remains deferred until freeze authority exists. |
| `BridgeRequiresIndependentEndpointBirth` | DECLARED_DEFERRED | Independent endpoint birth requires authority to prove the ordering `Freeze(F_i) < BridgeExperiment`; caller-constructible references and distinct identifiers cannot establish that authority claim. |
| `BridgeRequiresResidualBeyondEndpointReconstruction` | DECLARED_DEFERRED | A future bridge gate may freeze a `BornBridgeRef` only after its own G0 experiment shows a coupling residual beyond both endpoints and shared frozen context; a zero residual produces `DerivedRelationSpec`, never a bridge. |
| `NoUpstreamIdentityMutation` | DECLARED_DEFERRED | If `F_i` is frozen, no later result `G` computed from a `Reopen` of `F_i` may modify `F_i`, rename it, reinterpret its identity, merge it with another frozen factor, or change its rank. `G` may only carry `ParentRef(G, F_i)`; new evidence that bears on `F_i` opens a new revision on `F_i` itself (`NewEvidence => NewRevision != HistoricalOverwrite`, consistent with `BirthExperimentSpecification.revision_id`/`revision_sequence`), never a retroactive edit performed by `G`. |
| `HigherExperimentHoldsRefsNotCopies` | DECLARED_DEFERRED | A higher-level experiment or result holds a `FrozenFactorRef` (`factor_id`, `factor_content_id`, `freeze_certificate_id`, `domain`, `birth_experiment_id`, `birth_revision_id`) to a parent factor, never a reconstructed or mutable copy of the parent's own content. `HigherLayerOwnsReference != HigherLayerOwnsIdentity`: owning the reference grants no authority over the referenced factor's identity. |
| `NoTraditionalLayerEnum` | DECLARED_DEFERRED | No fixed enumeration of traditional layers (for example `ORTHOGRAPHY`/`PHONOLOGY`/`MORPHOLOGY`/`SYNTAX`/`SEMANTICS`) may be declared as a closed type in the kernel or Arabic runtime. A domain `L` is identified only by its own frozen experiment/jurisdiction scope (`Layer = FrozenExperimentJurisdiction`); two jurisdictions may later be shown to share a factor without that implying either was ever a case of the other. |
| `FractalParentageDoesNotDefineIdentity` | DECLARED_DEFERRED | A `FractalProvenancePath` records which frozen factors, bridges, derived relations, and reopen experiments produced a later result, strictly for audit and reconstruction of the proof path. `Parentage != Identity`: this path is never part of the later result's own declared identity or content identity, and two results with identical content but different provenance paths remain distinct occurrences, exactly as `EvidenceOccurrenceIdentity != EvidenceContentIdentity` already separates occurrence from content elsewhere in this kernel. |
| `RevisionDoesNotEraseHistoricalFreeze` | DECLARED_DEFERRED | Restates `FrozenFactorReopeningRequiresNewRevision` (G0.F above) at the fractal-reopen level: new evidence discovered through a `Reopen` never edits, deletes, or silently supersedes a parent's historical frozen record. `ContentIdentity_new(F) == ContentIdentity_old(F)` is required for any claim that a later step merely *reopened* `F`; a change in `F`'s own content identity is not a reopen at all -- it is a new revision or a new birth, recorded separately. |
| `ExactFrozenReferencePreservation` | PROVED (at contract level) | `FractalSnapshot` checks a derived relation's or bridge's referenced factor against the *exact* `FrozenFactorRef` recorded in the snapshot -- every declared field (`factor_id`, `factor_content_id`, `freeze_certificate_id`, `domain`, `birth_experiment_id`, `birth_revision_id`), never against a bare `factor_id` string. A reference sharing a `factor_id` but differing in content id, domain, birth experiment/revision, or freeze certificate names a different, unrecognized occurrence and is rejected. `factor_id` equality alone is never sufficient membership proof. |
| `ReopenComposesG0DoesNotForkG0` | PROVED (at contract level) | `ReopenExperimentSpecification` embeds one ordinary, complete `BirthExperimentSpecification` (`experiment`) rather than redeclaring its own `new_question`/`residual_definition`/`closure_criterion` fields. This preserves G0's own revision identity, `EvidenceMode`, `ProjectionPoset`, `BirthQuery`, residual/closure identities, and derived prerequisite cone verbatim, so reopen semantics cannot drift from G0 semantics over time (`G0SemanticsDriftBetweenBirthAndReopen` is closed, not merely avoided by convention). Reopen uses G0; Reopen does not fork G0. |
| `DerivedRelationProvenanceIsContentBound` | PROVED (at contract level) | `FractalProvenancePath.derived_relation_refs` holds `DerivedRelationRef` values (`relation_id` plus `derivation_content_id`), never bare `relation_id` strings. `SameRelationId != SameDerivationSemantics`: two derivations that happen to reuse the same `relation_id` but disagree on `derivation_content_id` are distinguishable, so drift in a derived relation's own recorded content is detectable from its provenance rather than silently trusted by id alone. |

`FrozenFactorRef`, `BornBridgeRef`, `DerivedRelationSpec`,
`DerivedRelationRef`, `ReopenExperimentSpecification`,
`FractalProvenancePath`, `ProofLineageEdge`, and `FractalSnapshot`
(`src/alghanem/kernel/fractal.py`) are contract *skeletons* only: their
constructors validate internal well-formedness (non-blank identities,
non-empty/non-duplicate parent or endpoint sets, exact-reference membership,
and so on), exactly as `BirthExperimentSpecification` and its G0.2a siblings
do ahead of any executable assessment runtime. None of them is issued by a
freeze or reopen authority yet, because no such authority exists: a caller
can construct a syntactically valid `FrozenFactorRef` by hand today, which
proves only that the contract is well-formed, never that a factor was
actually born, closed, and frozen (`ConstructibleContract != IssuedByAuthority`,
equivalently `WellFormedFrozenFactorRef != AuthorityIssuedFrozenFactorRef`).
No code anywhere in the kernel may treat successful construction, or a
passing `isinstance(x, FrozenFactorRef)` check, as proof that a genuine
freeze occurred. A future `FreezeAuthority`/`ReopenAuthority` -- analogous to
`EvidenceAcquisitionAuthority`'s sole-issuer pattern -- is a separate, later
milestone; only that authority may make an issued `FrozenFactorRef`
trustworthy. `FractalSnapshot` contains no `ArabicRuleTable` and no other
compiled artifact; per `RuleTableIsDerivedArtifact` above, any such table
remains a strictly later, derived projection of a frozen snapshot like this
one.

## Encyclopedia Nucleus — Constitution

The encyclopedia is an application consumer of the kernel, never a replacement
for it. Its minimal state is:

```
EncyclopediaNucleusSnapshot = FractalSnapshot + GrowthFrontier
GrowthFrontier = RootInquiries + ReopenInquiries
```

`FractalSnapshot` remains a discovery graph, not a knowledge graph. It holds
only frozen discovery contracts, whose construction remains non-authoritative
until the future birth and freeze authorities exist. The frontier holds open
questions. Frontier immutability is a contract property; preserving an inquiry
after a `DEFER` verdict is deferred until a growth transition mechanism exists.

| Law | Status | Scope |
| --- | --- | --- |
| `NoDedicatedTraditionalSchemaFields` | PROVED (at contract level) | The encyclopedia namespace has no dedicated domain, ontology, or human-science label fields. |
| `NoSemanticLabelLeakThroughIdentifiers` | DECLARED_DEFERRED | Identifiers are opaque keys, not semantic evidence; a future registry and evaluator authority must ensure their values cannot influence discovery. |
| `QuestionGenerationIsNotAuthorization` | PROVED (at contract level) | `QuestionProposal` has no experiment or execution field. `RootInquiry` requires a `BirthExperimentSpecificationContentBinding`, which proves its complete G0 specification exactly matches registry-frozen pre-evidence content. |
| `QuestionGrowthUsesReopen` | PROVED (at contract level) | Later questions around frozen results are represented by kernel `ReopenExperimentSpecification`; sequential inquiry is not an ontological bridge. |
| `FrontierReopenParentMustExistInSnapshot` | PROVED (at contract level) | Every reopen parent in the frontier must exactly equal a frozen factor or born bridge reference present in the paired `FractalSnapshot`; identifier equality alone is insufficient. |
| `FrontierImmutability` | PROVED (at contract level) | The frozen frontier contract cannot be mutated after construction. |
| `DeferPreservesOpenQuestion` | DECLARED_DEFERRED | A future `EncyclopediaGrowthTransition` must retain an inquiry after a `DEFER` result; no verdict-to-frontier transition exists yet. |
| `NoKnowledgeBeforeLicensedClaim` | PROVED (at contract level) | The nucleus contains no claim or knowledge fields. Frozen factors are not knowledge states. |
| `NoTextBeforeKnowledgeProjection` | PROVED (at contract level) | The nucleus contains no article or text fields; rendering is a later projection and cannot create knowledge. |
| `NoIndexFeedbackIntoDiscovery` | DECLARED_DEFERRED | A future index or renderer may project licensed knowledge but may not authorize or alter discovery. |

`src/alghanem/encyclopedia/inquiry.py`,
`src/alghanem/encyclopedia/frontier.py`, and
`src/alghanem/encyclopedia/snapshot.py` intentionally define no growth engine,
domain taxonomy, knowledge graph, article store, or evaluator authority.
`EncyclopediaGrowthTransition` is the deferred future boundary for applying
authorized kernel outcomes to a nucleus snapshot.

## Encyclopedia Self-Observation — Constitution

`Alghanem` is not exempt from its own encyclopedia's discipline: the
repository the encyclopedia is implemented in is itself a legitimate future
`ObjectOfInquiry`. But a four-way separation must hold before any claim
about the repository can be licensed as knowledge:

```
System != RepositoryRepresentation != SelfModel != KnowledgeAboutSystem
```

A GitHub repository is a `SourceArtifact` carrying traces of the system; a
commit is one exact `SourceVersion`; a file is a `SourceFragmentCarrier`;
a line, node, or function is an `EvidenceCandidate`
(`CodeFragment != Evidence` until a future claim-specific
`EvidenceBinding` exists). This module intentionally goes no further than
naming these carriers:

```
RepositorySnapshot -> Evidence -> Claim -> EpistemicLicensing -> SelfKnowledge
```

`src/alghanem/encyclopedia/self_observation/` defines only the first link,
`RepositorySnapshotRef` plus the artifact/fragment/transition refs anchored
to it. It defines no `Claim`, `EvidenceBinding`, or `SelfEpistemicState`
runtime; those remain a later, separate `SelfKnowledgeBridgeExperiment`
milestone, built only once a claim/evidence constitution exists.

| Law | Status | Scope |
| --- | --- | --- |
| `RepositorySnapshotIsNotKnowledge` | PROVED (at contract level) | `RepositorySnapshotRef` has no claim, evidence, or knowledge field; it names one explicitly-addressed repository state and nothing else. |
| `RepositoryArtifactIsNotEvidenceByItself` | PROVED (at contract level) | `RepositoryArtifactRef` and `RepositoryFragmentRef` name a file or fragment carrier only; naming a fragment proves nothing about any claim until a future `EvidenceBinding` exists. |
| `DocumentationIsNotImplementation` | DECLARED_DEFERRED | A future claim constitution must keep `DeclaredSelfModel` (from `docs/CONSTITUTION.md` and other prose) distinct from `ImplementedSelfModel` (from source); this module records neither yet. |
| `TestPassIsNotUniversalTruth` | DECLARED_DEFERRED | A future evidence constitution must keep `TestedSelfModel` (from passing tests/CI at one commit) distinct from `FormalProofEvidence` and from universal correctness; no test-evidence field exists yet. |
| `SelfModelIsNotSystem` | PROVED (at contract level) | `RepositorySnapshotRef`, `RepositoryArtifactRef`, `RepositoryFragmentRef`, and `RepositoryTransitionRef` are all references anchored to a commit; none of them is, contains, or executes the repository itself. |
| `SelfDescriptionDoesNotGrantAuthority` | PROVED (at contract level) | This module defines no freeze, reopen, or mutation authority; constructing or observing any of its refs grants no permission to alter the kernel or encyclopedia they describe. |
| `RepositoryVersionMustBeContentBound` | CONSTITUTIONAL REQUIREMENT | Every ref in this module is anchored to an explicit `commit_sha` (never a branch name); `RepositoryArtifactRef` and `RepositoryFragmentRef` are anchored to their exact snapshot, and `RepositoryTransitionRef` requires distinct `from_snapshot`/`to_snapshot` commit shas. This requirement is only *proved* at the weaker `RepositoryVersionIsExplicitlyAddressed` level below; full content authentication remains `RepositoryVersionIsContentAuthenticated` (DECLARED_DEFERRED). |
| `RepositoryVersionIsExplicitlyAddressed` | PROVED (at contract level) | `RepositorySnapshotRef` and `RepositoryArtifactRef` require non-blank `commit_sha`/`tree_sha`/`blob_sha` fields, each anchored to an explicit version, never a bare identifier without context. |
| `RepositoryVersionIsContentAuthenticated` | PROVED (within provider scope) | `RepositoryObservationAuthority` opens an authority-issued `RepositoryObservationRun`; the run verifies repository→commit→tree and tree/path→blob, and issues authenticated snapshots/artifacts only after those checks. This remains scoped to the provider's returned observations, not universal repository truth. |
| `SameRepositoryIdentity` | PROVED (at contract level) | `RepositoryTransitionRef` requires `from_snapshot.repository_identity == to_snapshot.repository_identity`; a pair naming two different repositories is rejected, not silently accepted as a transition. |
| `DifferentCommitsIsNotHistoricalTransition` | PROVED (within provider scope) | `RepositoryTransitionRef` remains address-only; an `AuthenticatedRepositoryTransition` requires two authenticated snapshots from the same observation run and a provider ancestry witness. Distinct commit shas alone remain insufficient. |
| `AuthenticatedObservationIsNotEvidence` | PROVED (at contract level) | Authenticated snapshots, artifacts, fragments, and transitions contain no claim or evidence binding; authentication of repository structure does not make an observation evidence or knowledge. |
| `ProviderDeclaredImplementationIdIsNotExecutionIdentity` | DECLARED_DEFERRED | `implementation_identity` is provider-declared provenance metadata. This milestone does not independently bind that string to the implementation that executed the run. |
| `ArtifactChangeRecordsBothSides` | PROVED (at contract level) | `RepositoryArtifactChangeRef` requires both a `before` (anchored to `from_snapshot`) and an `after` (anchored to `to_snapshot`) `RepositoryArtifactRef`, sharing the same `artifact_path` with distinct `blob_sha`s, so a delta can be reconstructed instead of only naming the post-change file. It also independently requires `before.snapshot.repository_identity == after.snapshot.repository_identity` and distinct `commit_sha`s, so a well-formed change pair is coherent even when constructed outside a `RepositoryTransitionRef`. |

`RepositoryTransitionRef` records `changed_artifacts` (as
`RepositoryArtifactChangeRef` before/after pairs), `added_artifacts`, and
`removed_artifacts` between two explicitly-addressed snapshots of the *same*
repository, but `Change != Improvement`: it makes no claim that a later
commit is better, safer, or more correct than an earlier one.
`RevisionDoesNotEraseHistoricalFreeze` follows directly from
`RepositoryVersionMustBeContentBound`: a later snapshot never invalidates
what a licensed claim once said about an earlier one, because the two are
distinct, equally addressable versions. A path renamed or moved between
`from_snapshot` and `to_snapshot` (`SameContent+DifferentPath`) is
deliberately out of scope for `RepositoryArtifactChangeRef`, which requires
an identical `artifact_path` on both sides; a future
`RepositoryArtifactMoveCandidate` would carry that separate identity
question.

## G0.T.0 — Intended theorem for the pure derivational core (DRAFT — NOT LAW)

**Status: DRAFT_TEXT_ONLY.** This section is a text experiment, not a law and
not a merged constitutional clause. It adds no row to any law table, changes
no gate, authorizes nothing, and grants no epistemic promotion. Its only
purpose is to find out whether the intended theorem can be *stated* at all in
current kernel terms. Nothing here is proved; where this text asserts, it
asserts as a declared assumption.

### Scope of the draft statement

The kernel divides, for provability purposes, into two halves that must not
be conflated:

- a **pure derivational core** — `BirthVerdictGate.assess` and
  `IndependentClosureGate.assess`, which read no evidence payload and compute
  their status from frozen specification fields alone; and
- an **opaque oracle edge** — registry-bound invariant extractors, evaluator
  input derivations, and evaluator implementations, which are arbitrary
  callables with no declared denotation (`ObservedDeterminism != ProvenPurity`).

This draft states a theorem about the first half only. The second half enters
only as explicitly assumed axioms (§ *Assumed oracle axioms*), never as
proved content.

### T-1 (intended, unproved) — Verdict derivation is specification-local

> For every `BirthAssessmentRequest` `r` that is successfully constructed, and
> every `SealedBirthVerdictScopeRegistry` `R` that resolves a scope `s` for
> `r`'s own `(domain, experiment_content_id)`, the `BirthVerdictDecision`
> issued by `BirthVerdictGate.assess(registry=R, request=r)` is a total
> function of `r.specification.competing_projections` and
> `r.specification.frozen_weaker_models` alone — both of which are derived by
> `BirthExperimentSpecification` from its own frozen `projection_poset` and
> `birth_query`. In particular the decision's `status` and `reason` are
> independent of `r.evidence_snapshot`'s payload, of every evaluator, every
> derivation, and every extractor, and of `R`'s other scopes.

**T-1′ (companion, same shape).** The same statement holds for
`IndependentClosureGate.assess` with `ComparabilityClosureStatus` in place of
`BirthVerdictStatus`.

**Intended corollary (weak).** Because the codomain reachable by the current
gate is the single value `DEFER_IN_SCOPE`, T-1 currently entails no claim
about any birth. The theorem is stated now so that its *shape* is fixed before
`BIRTH_IN_SCOPE` becomes reachable; today its subject matter is deferral.

**What T-1 does not say.** It does not say the verdict is *correct*, *sound*,
*justified by the evidence*, or *consistent with its inputs* in any sense
richer than "computed from these frozen fields". `SpecificationLocality !=
EvidentialConsistency`. It is a non-interference/locality statement, not a
soundness statement.

### Assumed oracle axioms (declared, not proved)

Any future statement that reaches past the pure core must discharge or assume
these. They are recorded here as assumptions precisely because the kernel
cannot establish them:

This list is written as prose, not as a table: the document's table grammar
is a closed vocabulary of declared headers, and inventing a new header shape
for a draft would either be refused outright or silently widen that grammar.

- `OracleTotality` — *assumed*: a registry-bound extractor, derivation, or
  implementation returns a value for every input it is invoked on. *Not proved
  here*: bound callables are arbitrary Python and may raise or diverge. The
  kernel converts raising into `DEFER`, which records an epistemic non-answer
  rather than establishing totality.
- `OracleDeterminism` — *assumed*: a bound callable returns equal output for
  equal input, across invocations and processes. *Not proved here*:
  `EvaluatorInputDerivationGate` observes one repeat invocation only and
  explicitly records `ObservedDeterminism != ProvenPurity`; nothing excludes
  hidden state, clock, or environment dependence.
- `OraclePurity` — *assumed*: a bound callable has no effect on kernel or
  external state. *Not proved here*: Python imposes no effect discipline and
  the kernel performs no static analysis of bound callables.
- `OracleIdentityFaithfulness` — *assumed*: a declared
  `implementation_identity` names the code that actually ran. *Not proved
  here*: declared identity is caller/provider metadata; the kernel compares
  strings, it does not attest the executing artifact.
- `SchemaDenotation` — *assumed*: declared schema strings (`result_schema`,
  `residual_schema`, `model_result_schema`, `output_schema`) denote sets of
  values, and a returned value lies in the denoted set. *Not proved here*:
  these fields are opaque text compared only by equality; no interpretation
  function from schema text to a value set exists anywhere in the kernel.
- `FailureSemanticsDenotation` — *assumed*: `failure_semantics` and
  `declared_information_loss` denote something a judgment could be checked
  against. *Not proved here*: same — declarative text, never interpreted.

An oracle-touching theorem is therefore, at best, of the form
"assuming `OracleTotality ∧ OracleDeterminism ∧ …`, then …". None of these
assumptions is currently testable inside the kernel, and asserting them is not
weaker than asserting the conclusion by inspection.

### Where the intended statement is not expressible (the actual finding)

Writing T-1 exposed that the *originally intended* theorem — "every
successfully constructed request yields a judgment consistent with its
inputs" — cannot be written down in current kernel terms. The following
phrases have no referent here, and each needs a different remedy:

- **"consistent with its inputs"** — there is no relation in the kernel
  between an evidence payload and a verdict. The gate never reads the payload,
  and no predicate `Consistent(evidence, verdict)` is definable because
  evidence bytes are deliberately uninterpreted. *Remedy*: an interpretation of
  evidence content — a genuine denotational layer — which G0 deliberately does
  not have.
- **"a judgment" as a semantic object** — `BirthVerdictStatus` is an enum
  label carrying no truth condition; `DEFER_IN_SCOPE` is defined by its issuing
  procedure, not by a condition on the world. *Remedy*: semantics for statuses,
  stated independently of the procedure that emits them.
- **"for every request" as a quantifier** — quantification over all
  constructible `BirthAssessmentRequest`s is not expressible in Python or in
  mypy-strict types; construction validity lives in `__post_init__` raises,
  which are a procedure, not a predicate. *Remedy*: an external proof object
  (dependent types / a proof assistant), or at minimum an explicit predicate
  mirroring every `__post_init__` check.
- **"successfully constructed" as a predicate** — success is defined
  operationally as "no exception was raised by some constructor", and the set
  of raises is distributed across many `__post_init__` bodies in several
  modules. There is no single, quotable well-formedness predicate to appear as
  the theorem's hypothesis. *Remedy*: a consolidated, auditable statement of the
  admission predicate, derived from — and kept in step with — the constructors.
- **"the same request" across runs** — request identity is partly occurrence
  identity (`uuid4`, `admission_id`) and only partly content identity;
  `OccurrenceIdentity != ContentIdentity` is declared law. A theorem
  quantifying over requests-up-to-content cannot yet name its own equivalence
  relation. *Remedy*: total content identity coverage for requests, not only for
  experiment specifications, residuals, criteria, and weaker models.
- **"necessarily" / "must"** — the kernel's modality is runtime refusal: a
  violation raises. Refusal establishes that *this* execution did not proceed,
  never that no execution could. *Remedy*: a proof-carrying notion of
  impossibility, which runtime raises cannot supply.

`BirthAssessmentSemanticsContract` is **not** this theorem and does not
approach it: it is a per-instance referential well-formedness predicate
(matching ids, domains, schemas, exact prerequisite-cone coverage, poset
agreement) evaluated in `__post_init__`. It quantifies over nothing and issues
no verdict. In the shape above it belongs in T-1's *hypothesis*, not its
conclusion; `ReferentialConsistencyContract != DenotationalSemantics`, and the
name "semantics contract" overstates what it establishes.

### Reconsideration condition (tracked, not scheduled)

This draft is not to be promoted to law, and the "prove once vs. re-verify per
instance" question is not to be reopened, until **both** hold: `BIRTH_IN_SCOPE`
is actually reachable through a real closure authority, **and** the law tables
above have stopped moving. Until then any theorem proved here has `DEFER` as
its only subject.
