# Alghanem

> **Start here: [`docs/VISION.md`](docs/VISION.md)** — what Alghanem is, why it
> exists, and what it does not claim. This README is a cumulative engineering
> log; the vision document is the entry point, and its "current state" section
> is rendered from `src/alghanem/program/project_state.py`, never hand-edited.
>
> **In one sentence.** Alghanem is a research system for building *licensed,
> reconstructible epistemic transitions*: it takes Arabic as its first proving
> ground, and grants no result an authority higher than its evidence. The
> product is not the linguistic findings but the chain behind them — where a
> claim came from, what licensed it, in what scope it holds, what rank it
> carries, what still blocks its promotion, and what the next permitted step
> is.
>
> Reading order: **`docs/VISION.md` → `docs/AIMS.md` → `docs/CONSTITUTION.md` →
> source → tests → the derived state block.**

Alghanem is a research codebase for a general algebra of licensed
transformations. The current release is the language-agnostic **Kernel v0.1**:
small, shallowly immutable data structures for anchors, operations, evidence,
traces, residuals, and certified transition outcomes.

Kernel v0.1 only proves `StructurallyAdmissibleTransition`: a transition that
is well-formed under the kernel's structural laws. It deliberately does not
yet prove evidential sufficiency, domain-transition authority, or
inter-layer authority; a `LicensedTransition` — carrying those additional
guarantees — is a future gate, not a synonym for structural admission. What a
candidate claims to be (its `TransitionKind`) is likewise kept distinct from
any certified outcome. See `docs/CONSTITUTION.md` for the full law-by-law
status.

G0.OB.1 bridges a source-specific, authority-issued authenticated observation
to a kernel `AuthenticatedObservationBinding`; identifiers alone never
constitute authentication. G0.EB.1 then adds a claim-relative
`EvidenceRoleCandidate` over that binding, a `ClaimCandidate`, and an opaque
`EvidenceRoleRef`. It does not judge applicability, sufficiency, truth, or
knowledge: authentication or a proposed role does not by itself make an
observation evidence for a claim.

Bindings are source-bound authenticated coordinates, not portable observation
identities; portable identity remains deferred.

G0.EA.1 assesses an existing `EvidenceRoleCandidate` only for applicability in
the claim's scope. Its gate-issued `EvidenceApplicabilityAssessment` is
`PASS`, `BLOCK`, or `DEFER`, with reason, trace, residuals, and the identities
of its frozen specification and sealed evaluator registry. Evaluators are
authority-issued and bound to the candidate's role and claim scope. The gate
selects the weakest declared model that closes applicability rather than
aggregating every model's worst status. This stage does not assess sufficiency,
truth, licensed-claim status, or knowledge.

The initial Arabic layer is limited to `RawSurfaceObservation` and
`SurfaceNormalization`. It emits versioned normalization traces, residuals,
and uninterpreted surface-atom candidates. `ObservationAuditLedger` preserves
every occurrence under measurement-protocol-supplied source and occurrence
identities; distinct candidates are only a derived projection. It does not
infer identities, bindings, Arabic cardinalities, or grammatical concepts;
those require separate future birth gates and a later E0 audit.

P0.1 freezes measurement authority with `MeasurementProtocolSpec`,
`MeasurementRunIdentity`, `MeasurementRunManifest`, and
`ObservationLedgerManifest`. An observation provenance must name its measurement
run, and manifests bind an audit ledger to one run plus the run's declared
normalization policy and Unicode database version before later factorization or
identity-birth gates may consume it.

The next audit artifact is `NormalizationResidualTable`: an occurrence-complete
derived table with one row per audit, including unchanged rows, raw and
normalized codepoint sequences, atom counts, prefix/suffix delta boundaries,
removed/inserted segments, and the current candidate surface. The weaker
`NormalizationEquivalenceProjection` remains only a quotient projection over
equal normalized `SurfaceAtomCandidate`s; it is not a born object and does not
introduce Carrier, State, binding, or Arabic cardinality claims.

G0 freezes the birth protocol itself, ahead of any experiment: before any new
Arabic candidate, factor, or structural coordinate may be born, either a
measured residual (empirical mode) or an exhaustive proof over a declared
finite formal domain (formal mode) — never a synthetic-intervention artifact
alone — must survive exhaustion of every weaker model licensed and frozen for
that experiment. G0.1 supplies a language-agnostic pre-evidence
`BirthExperimentSpecification` with a `BirthQuery`, a derived prerequisite
cone, stable residual/closure identities, and a later
`BirthAssessmentRequest` that binds the evidence snapshot. G0.1 stops at that
request: it has no birth-verdict or freeze authority. G0.2a adds executable
residual, weaker-model, and closure contracts that must match the frozen
residual/closure identities. Evaluator ids in those contracts are declarations
only unless a sealed evaluator registry authorizes the exact scope, and
G0.BV.1's birth branch remains deferred: no runtime authority issues
`BIRTH_IN_SCOPE` or `NO_BIRTH_IN_SCOPE` until an
assessment authority, `BirthCandidate`, and `IndependentClosure` exist.
G0.BV.1a makes only the deferral branch executable
(`src/alghanem/kernel/birth_verdict.py`): `BirthVerdictScopeRegistry` issues
and seals `AuthorizedBirthVerdictScope`s whose conditions are derived from a
verified frozen experiment binding, and `BirthVerdictGate.assess` is the sole
issuer of a `BirthVerdictDecision`. The gate accepts no status, reason, or
closure claim from its caller (`CallerDoesNotOwnVerdictAuthority`) and derives
`DEFER_IN_SCOPE` from the request's own frozen projection poset. Its codomain
is currently that single value, because the other two statuses require a
gate-issued `IndependentClosureDecision` no authority here can produce
(`DeferredVerdict != Birth`). It issues no `Freeze` and no `E0` mapping, and a
`DEFER_IN_SCOPE` decision may not be frozen.
G0.IC.1a (`src/alghanem/kernel/independent_closure.py`) closes exactly one
conjunct of that missing closure, using the same register -> seal -> gate shape:
`ClosureScopeRegistry` issues and seals `AuthorizedClosureScope`s, and
`IndependentClosureGate.assess` is the sole issuer of an
`IndependentClosureAssessment`. It accepts no comparability claim from its
caller and reads only the request's own frozen `ProjectionPoset`; because that
question is exhaustively decidable over a finite projection set, both
`COMPETITION_RESOLVED_IN_POSET` and `COMPETITION_UNRESOLVED_IN_POSET` are
reachable. An absent strict relation is always counted as unresolved, so an
undetermined relation is never read as a resolution. This is still not closure:
`is_independent_closure` is `False` unconditionally, because a surviving
residual and an exhausted licensed weaker model set have no authority here, and
`BirthVerdictGate` is deliberately not wired to consume the assessment.
G0.BA.1b (`src/alghanem/kernel/evaluator_input_provenance.py`) closes exactly
one of the three claims G0.BA.1a refused to make: `InputProvenance =
DECLARED_DEFERRED`. G0.BA.1a runs a bound implementation on caller-supplied
input and merely attaches the request's evidence snapshot, so a record proves
an implementation ran on *some* content alongside *some* evidence, never that
the one came from the other. Here an `EvaluatorInputDerivation` receives
exactly one argument — the canonical bytes of the request's own authorized
evidence manifest — and `EvaluatorInputDerivationGate.derive` accepts no input
content and no domain at all (`CallerDoesNotOwnInputContent`): the caller
chooses which registry-sealed derivation runs, never what the evaluator sees.
The issued `EvaluatorInputContentIdentity` digests the source evidence
identity, the derivation id, the implementation identity, and the produced
content together, so it binds what was produced, from which exact evidence,
and by which declared derivation (`OutputDigest != DerivationIdentity`).
`ProvenanceBoundEvaluatorExecutionGate` delegates the invocation to the
unchanged `BirthEvaluatorExecutionGate` and binds the resulting record to the
derivation that fed it; G0.BA.1a itself is preserved exactly, still accepting
unrelated input by design. Three claims stay refused:
`DerivationIdIsContentAuthenticated = DEFERRED`, the inherited
`AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment`, and
`ProvenInputProvenance != AssessedEvidence` — `is_assessment` is `False`
unconditionally, so proven provenance still says nothing about residual
survival, weaker-model exhaustion, or closure.
G0.IC.1b (`src/alghanem/kernel/weaker_model_closure.py`) takes the first step
into what those records *mean*, for exactly one weaker model at a time. It
invents no vocabulary: `ClosureCriterionSpec` already declared the closed
three-member outcome set of `Close(W_i, R)`, and the frozen projection poset
already derived which models must be closed. The one missing relation was
between an evaluator's `output_content` — a plain string — and a member of
that set. `DeclaredClosureOutcomeVocabulary` supplies it as declared data,
frozen in a sealed registry against a content-bound closure criterion, and
required to cover every declared outcome exactly once so that none is
unreachable by construction. `WeakerModelClosureGate.assess` accepts no status
and no reason, and matches the output by exact string equality: no trimming,
no case folding, no prefix match, and no default. An unrecognized output is
refused by model id and is never read as `DEFER`, because reading ignorance as
a declared outcome is the exact failure the gate exists to prevent; a record
under any other role, or naming a target outside the derived prerequisite cone,
is refused too. What stays refused is named: `LocalClosureOutcome !=
WeakerModelExhaustion` (nothing here aggregates the cone, and
`is_weaker_model_exhaustion` is `False` unconditionally),
`WeakerModelClosure != IndependentClosure` (`is_independent_closure` is `False`
on every branch and `IndependentClosureAssessment` is untouched),
`DeclaredVocabularyIsNotProvenSemantics`, and
`SealedBeforeAssessmentIsNotSealedBeforeEvidence`.
G0.IC.1c (`src/alghanem/kernel/weaker_model_exhaustion.py`) aggregates those
per-model certificates into the second conjunct of closure, and stops there.
The licensed set is not invented: the frozen projection poset already derived
the cone before any evidence existed, so how many models must be answered is
fixed in advance and cannot be trimmed to fit whichever certificates happen to
exist. Coverage therefore comes before judgement, copied from
`InvariantVerificationGate.assess_all_preserved`: a missing model, a model
answered twice, and a model the poset never licensed are each a malformed
request that raises, because an unevaluated model is ignorance and reading
ignorance as a failure to close is exactly how a fabricated exhaustion would be
manufactured. Certificates must also share one `BirthAssessmentRequest`, since
certificates from different requests describe different evidence.
`WeakerModelExhaustionGate.assess` then accepts no status and no reason, reads
every certificate rather than stopping at the first, and applies a fixed
precedence — `WEAKER_MODEL_CLOSES_RESIDUAL` beats `EXHAUSTION_UNDETERMINED`
beats `LICENSED_WEAKER_MODELS_EXHAUSTED` — so a known `CLOSE` is never erased
by an unrelated `DEFER`, and the aggregate does not depend on the order the
certificates were given in. Two of the three conjuncts of closure are now
derived, comparability by G0.IC.1a and exhaustion here; the third, a residual
surviving measurement or formal proof, is certified by no authority in this
repository, so `is_independent_closure` is still `False` on every branch and
`IndependentClosureAssessment` is untouched. `WeakerModelClosesResidual !=
NoBirthVerdict`, `CoverageIsNotCorrectness`, `FrozenConeIsDeclaredNotProven`,
and `SameRequestIsNotSameEvidenceRun` stay open by name.
G0.IC.1d (`src/alghanem/kernel/residual_survival.py`) reads the third and last
conjunct, for exactly one witness. Nothing new is invented here either: the
residual whose survival is at stake is already declared by
`ResidualDefinitionSpec`, and the closed three-member vocabulary of a survival
reading is declared on that same frozen contract, exactly as
`ClosureCriterionSpec` declares the vocabulary of `Close(W_i, R)`. The missing
relation was again between an evaluator's `output_content` — a plain string —
and a member of that set, and `DeclaredResidualSurvivalVocabulary` supplies it
as declared data, frozen in a sealed registry against a content-bound residual
definition. `ResidualSurvivalGate.assess` accepts no status and no reason, and
matches by exact string equality: an unrecognized output is refused by residual
id and never read as `DEFER`, as are a record under any other role and a target
that is not the request's own frozen `residual_definition_id`. The evidence mode
is read from the frozen experiment rather than from the caller, and `MIXED` is
refused by name (`MixedModeNeedsTwoScopedWitnesses`): that mode is an explicitly
typed scoped pair, and no authority here proves its two declared scopes or that
neither component compensated for the other, so one certificate a later reader
could take as satisfying both modes is refused rather than issued. All three
conjuncts of closure are now derived on their own — comparability by G0.IC.1a,
exhaustion by G0.IC.1c, survival here — but *composing* them is a separate
question with no authority in this repository, so `is_independent_closure` is
still `False` on every branch and `IndependentClosureAssessment` stays untouched.
`DoesNotSurvive != NO_BIRTH_IN_SCOPE`,
`SurvivalReadIsNotMeasuredReplicatedResidual`, `FormalNecessityIsNotProvedHere`,
`DeclaredVocabularyIsNotProvenSemantics`,
`SealedBeforeAssessmentIsNotSealedBeforeEvidence`, and
`OneWitnessIsNotResidualCertification` stay open by name.
G0.IC.1e (`src/alghanem/kernel/independent_closure_composition.py`) composes
those three readings, and claims nothing beyond what they say. It reads nothing
new — no evidence is opened, no evaluator executed, no poset inspected — because
every input is already a gate-issued reading
(`ThreeReadingsAreNotAFourth`). `IndependentClosureCompositionGate.assess` takes
exactly the three readings and no status, reason, or closure claim, and refuses
readings that do not all speak for the same `BirthAssessmentRequest`
(`OneRequestOrRefusal`). All `2 x 3 x 3 = 18` combinations were enumerated
before the module was written and are asserted by name in the tests: a
refuting conjunct (a weaker model that closes the residual, or a residual that
does not survive) outranks every deferral, an unresolved comparability counts as
ignorance and never as refutation
(`UnresolvedComparabilityIsIgnoranceNotRefutation`), and refuted and
undetermined conjuncts are tracked separately, as
`InvariantVerificationDecision` tracks failed and deferred components. Ten
combinations are refuted, seven undetermined, and exactly one — resolved
comparability, exhausted licensed weaker models, and a surviving residual —
reaches `CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION`. Even that one
yields `is_independent_closure == False`
(`SatisfiedConjunctsIsNotIndependentClosure`): the conjuncts hold *as read*, and
`OneWitnessIsNotResidualCertification`,
`SurvivalReadIsNotMeasuredReplicatedResidual` and `CoverageIsNotCorrectness`
remain open by name, so the status says what was reached and what it is pending
on rather than overstating it. `CompositionIsNotAVerdict`: the stage is not
wired to `BirthVerdictGate`, and `ClosureRefutedInScope != NO_BIRTH_IN_SCOPE`.
G0.BC.1a (`src/alghanem/kernel/birth_certificate.py`) supplies the contract both
of those stages stop short of, and activates neither birth branch.
`BirthVerdict != BirthCertificate != Execution`: a verdict decides that the
conditions for existence of this genus were met in this scope, a certificate
preserves that decision with its scope, necessity readings, evidence references,
preventers and trace, and execution uses what was born and may never create it.
Two authorities exist and neither can perform the other's act — only
`ConstitutionalBirthAuthority.assess` may produce a `BirthCertificate` and it
exposes no method that runs anything, and only `ExecutiveAdmissionGate.admit`
may produce an `ExecutableEntity` and it exposes no method that certifies
anything — so `ExecutiveAuthorityCannotIssueBirth` and
`ConstitutionalBirthAuthorityCannotExecuteTheBornEntity` are enforced by the two
classes' public surfaces rather than by prose, and successful execution is never
evidence of valid birth. A candidate's existence does not oblige its birth, a
use for it does not, and frequent use of it does not; what obliges it is an
unclosed residual that the exhausted lower layer did not close and that no
weaker reconstruction still suffices to explain, and all three conjuncts are
*read* from the closure decision rather than re-derived
(`NoBirthWithoutUnclosedResidual`, `NoBirthBeforeLowerLayerExhaustion`,
`NoBirthWhenAWeakerReconstructionStillSuffices`).
`APreventerHasAnIdentityNotABoolean`: every member of `BirthPreventer` is
derived on every assessment, held or cleared, each carrying its own reason, so a
refusal records *which* ground stopped the birth. `NoCertificateIsReachableInThisTree`
is declared rather than discovered — three preventers hold on every branch,
naming three different missing authorities (no `BirthCandidate` issuer, no
identity proof, no proof of difference from the origin), and a fourth holds
because G0.BV.1a still only defers — and all `3^5 = 243` reading combinations
are enumerated in test with none yielding a certificate. A certificate would
still confer neither `Freeze` nor truth nor any global ontology claim
(`BirthDoesNotMeanFreeze`, `BirthDoesNotMeanTruth`), and no
instruction/rule/law/constitution ladder is encoded, since each such genus would
need its own certificate first (`NoGenusLadderIsEncodedHere`).

`BirthCandidate` is distinct from a scoped birth verdict and from `Freeze`;
the future G0.BV.1 authority may issue `BIRTH_IN_SCOPE`, then a later freeze
authority may freeze it before a separate `E0` step. See the
"G0 — Birth Protocol" section of
`docs/CONSTITUTION.md` for the full declared laws; no birth-issuing `BirthGate`
or rank/complexity runtime exists yet. A non-linguistic
`SurfaceAtomIntervention`/`SurfaceInterventionTrace` runtime does exist
(`src/alghanem/arabic/encoding/intervention.py`), but per
`InterventionOperationIsNotOntology` and
`SyntheticInterventionMayGenerateHypothesisOnly` it is an explicit,
non-exhaustive experimental tool that can license at most a hypothesis, never
a `BirthGate` verdict on its own. That "at most a hypothesis" is no longer
prose only: `src/alghanem/arabic/encoding/provenance_genus.py` derives an
`EvidenceProvenanceGenus` (`MEASURED`, `SYNTHETIC`, and deliberately no
`MIXED`) from the artifact's own type rather than from any caller-written
label — `DeclaredProvenanceLabel != DerivedProvenanceGenus` — so an
intervention result cannot enter a `MeasuredContrastSet`, measured evidence
cannot enter a `HypothesisResidual`, and only `EvidenceProvenanceGate` may
issue a classification at all. The module deliberately contains no rank, no
promotion, and no freeze: birth eligibility needs a measured contrast that
survives every licensed weaker projection *and* replicates in a second
independent measurement run, and no authority here assesses either, so
`HypothesisResidual.is_birth_eligible` is structurally `False` and counting
measured sources may not stand in for that assessment. This genus is
deliberately *not* named `EvidenceGenus`, which already names an unrelated
linguistic-evidence distinction in
`src/alghanem/arabic/probe_preregistration.py`.

`src/alghanem/arabic/encoding/intervention_footprint.py` closes the one
question that intervention runtime left open — whether two interventions on
the same occurrence commute — using no data beyond the intervention
definitions themselves. Each intervention's footprint (its ReadSet, its
WriteSet, and its coordinate shift) is *derived, never written*:
`InterventionFootprint` holds exactly one field, the intervention, and
exposes `read_set`, `write_set`, `shift`, and `touched` as properties, so a
footprint contradicting its own intervention is structurally unconstructible
— `DerivedFootprint != DeclaredFootprint`. Shift is modelled explicitly
rather than folded away: `delete` and `repeat` shift from `i + 1`, `insert`
from `i`, so two interventions with disjoint write sets still conflict when
one sits at or past the other's shift origin. The verdict is three-valued
(`COMMUTES`, `CONFLICTS`, `UNDEFINED`) with an ordered precedence:
`out_of_range` → `UNDEFINED` is decided **before** overlap and **before**
shift, because an order whose second step falls outside the shifted sequence
is not merely different but inapplicable, and its oracle is asserted against
`InterventionCoordinateError` by name.

What the module delivers is a **named pair list**, not a generalized
confluence law — `NamedCriticalPairs != GeneralizedLaw`. `reference_matrix`
runs the full 5 × 5 type matrix over nine named coordinate configurations
(`adjacent`, `distant`, `at_zero`, `same_coordinate`, `descending`,
`upper_edge`, `append_edge`, `straddling_swap`, `swap_shares_one_coordinate`)
on a six-atom sequence, excluding identical interventions by declaration, and
reports 48 commuting pairs, 141 critical pairs (`overlap` or `shift`), and 9
undefined pairs across 198 configured pairs, with every predicted verdict
confirmed by `observe_commutation` applying both orders through the real
application path (MATCH_ALL, 198/198). The last two configurations exercise
the shapes an adjacent-only matrix cannot reach: a non-adjacent `swap` whose
coordinates straddle a `delete`'s shift origin (`delete@2 × swap@1,4 ::
shift`) and a `swap` sharing exactly one coordinate with a `delete`
(`delete@1 × swap@1,3 :: overlap`). The same matrix is run over a minimal
two-atom sequence and over a second, disjoint six-atom sequence, whose named
pair lists are byte-identical to the reference run: verdicts follow
coordinates and length alone, never atom values
(`PAYLOAD_INDEPENDENCE_NOTE`). The scope is declared, not silently widened:
the model reads coordinates and not values, so a sequence with repeated atoms
can make two orders agree by **value coincidence** rather than structural
commutation. That limit is recorded in `VALUE_COINCIDENCE_NOTE` and
demonstrated by an explicit test, and the reference matrix therefore runs on
distinct atoms only. Ordered pairs are the whole measured domain:
`ORDERED_TRIPLES_ABSENCE_NOTE` records that a three-way critical-pair set is
not derivable from pairwise verdicts and is therefore not claimed, rather
than left to silence.

Two absences are deliberate. First, a disagreement between the predicted and
the observed verdict is recorded, never folded: it is labelled
`PREDICTION_ORACLE_MISMATCH(τᵢ,τⱼ)`, kept in the list, and drops the derived
`law_status()` to `PARTIAL_WITH_NAMED_RESIDUALS` — the status is derived from
the matrix rather than written into it, and the footprint definition is not
retrofitted to match what was observed (`PredictedVerdict != ObservedVerdict`).
Second, nothing consumes the result:
`NO_KERNEL_MODULE_CONSUMES_INTERVENTION_FOOTPRINT_NOTE` records that no
kernel module, no gate, no `Freeze`, and no `E0` reads anything here, and
exporting the module from `alghanem.arabic.encoding` is availability, not
consumption. That absence is enforced by an import-tree sweep test rather
than asserted in prose, because agreement between a model and its oracle
disciplines the model and grants no authority at all —
`AgreedVerdict != GrantedAuthority`.

For bounded card-level review, the repository also includes
`src/alghanem/arabic/external_audit.py` with a golden example at
`examples/external_audit/man_2_255.yaml`. This auditor is explicitly
non-authoritative (`ExternalAuditor != KernelAuthority`): it emits only
external audit status (`نتيجة_التدقيق_الخارجي`), derives
`مخروط_الأضعف_المشتق` from the frozen projection poset (rejecting
caller-declared weaker cones), reports all competing readings, and exposes
explicit `حالة_إغلاق_Down_E`/`سبب_حالة_إغلاق_Down_E` fields.
An optional `الأدلة` list of non-blank declared witnesses is now read and
structurally validated, and its size is reported as `عدد_الشواهد`. This is a
count only: `DeclaredWitness != AssessedEvidence`. The auditor does not
classify witnesses, relate them to the tested model, or let them affect
`نتيجة_التدقيق_الخارجي`; a card without the field is still well-formed and
counts zero. Adding or removing witnesses leaves every other reported field
byte-identical. The count is no longer uniform across the example cards: it is
`1` on `man_2_255.yaml`, `maa_2_197.yaml`, and `imran_3_33.yaml`, and `5` on
`hadhan_20_63.yaml` (طه:63), whose five witnesses each name their own
grammarian. That variation is still only a count of declared text; it grants
the richer card no additional standing, and `hadhan_20_63.yaml` defers exactly
like the others.
`علاقة_بالنموذج_المختبر` is a closed vocabulary — `غير_متعينة`,
`أضعف_صوريًّا`, `مكافئ_صوريًّا`, `غير_قابل_للمقارنة` — and any other text
(a misspelling or an invented term) is rejected instead of silently counting
as a resolved relation. Following
`NoRicherStructureBeforeLowerOpenResidualClosure`, an incomparable competing
reading defers unless the card declares `تفسير_منافس_كامل: false`; when the
flag is absent or true the reading still blocks, because an incomparable
projection that offers a complete competing explanation is unresolved until
discriminating evidence exists. Card text is
compared through `comparison_key`, an orthography-insensitive key (NFC plus
removal of combining marks, invisible formatting characters, and `TATWEEL`,
plus `ALEF`/`ALEF MAQSURA`/`TEH MARBUTA` folding), so an optional diacritic or
an invisible character can no longer turn a deferred relation into a passing
one; the key is used only for comparison and never replaces the card's own
reported text.

Each competing reading may also carry an optional `سبب_الإخلال_بالفهم`, a
second closed vocabulary drawn from the usuli list of causes of defective
comprehension — `اشتراك`, `نقل`, `مجاز`, `إضمار`, `تخصيص` — plus the explicit
`لا_ينطبق`. `src/alghanem/arabic/comprehension_defect.py` also fixes the
documented priority order `تخصيص > مجاز = إضمار > نقل > اشتراك`, with a full
textual argument and a named source recorded for each of the ten pairwise
comparisons, so no rank in that order rests on estimation. Two limits are
recorded deliberately. First, `DeclaredDefectCause != AssessedRelation`: the
classification is reported as `تصنيف_أسباب_الإخلال_بالفهم` and moves nothing
— it never enters the derived `BirthExperimentSpecification`, never changes
`نتيجة_التدقيق_الخارجي`, and neither `IndependentClosureGate` nor
`BirthVerdictGate` reads it. Second, the framework addresses **ambiguity of
meaning in a fixed text**, not **multiplicity of recited readings** and not
**weakness of transmission**; so a card whose dispute is over the wording
itself, or over whether a report is `آحاد` rather than `متواتر`, falls outside
it by construction. Its partial applicability to the example cards is
therefore an expected structural result, not a gap: across the four cards only
three of eight competing readings are described by one of the five causes
(`تخفيف_إن_وضمير_شأن` in `hadhan_20_63.yaml` as `إضمار`, and the `مَن`/`ما`
readings in `man_2_255.yaml` and `maa_2_197.yaml` as `اشتراك`); the remaining
five are declared `لا_ينطبق` rather than forced into a label.

That priority order also carries an obligation, now made visible. Declaring a
cause that sits late in the order is an implicit claim that every cause ranked
ahead of it has already been excluded by evidence, so classifying a word as
`اشتراك` — the last of the five — before excluding `نقل`, `مجاز`, `إضمار`, and
`تخصيص` is methodologically premature even where it happens to be right
(`EXHAUSTION_PRECEDES_CLASSIFICATION_NOTE`). A classified competing reading may
therefore declare `استبعاد_الأسباب_الأقوى`, each entry naming one cause, its
exclusion evidence, and its named source; *which* causes are owed is derived
from the existing order alone, never declared by the card, and an entry naming
a cause that is not stronger — or naming one twice — is refused at read time
rather than silently counted. The derived three-valued result
(`استنفاد_مكتمل` / `استنفاد_ناقص` with the remaining causes named / `لا_يلزم_استنفاد`)
is reported as `حالة_استنفاد_الأسباب_الأقوى` and judges nothing: it changes no
`نتيجة_التدقيق_الخارجي` and fails no card (`REPORTED_EXHAUSTION_IS_NOT_A_GATE_NOTE`),
and the analogy to `NoBirthBeforeLicensedWeakerExhaustion` is named with its
difference rather than claimed as identity — there exhaustion closes a gate,
here it is only reported. As it stands, `quru_2_228.yaml` reads
`استنفاد_ناقص` with all four stronger causes still unexcluded, which is the
point: the gap in the argument is now visible instead of silent.

A third closed vocabulary, `src/alghanem/arabic/apparent_conflict.py`, sits
beside those five without merging into them, because it answers a different
question: not *what makes one word's meaning unclear* but *whether a claimed
conflict between two witnesses is real at all*. Its governing rule is that mere
resemblance between two texts creates no contradiction — the default between
them is **difference**, and conflict is a claim requiring proof rather than a
presumption (`DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE`). It names exactly
three causes of *apparent* conflict — `التعميم` (treating a ruling tied to one
incident as general), `التجريد` (stripping an incident of its circumstances
before comparing), `الاشتباه` (surface resemblance between incidents that
differ in substance) — plus the explicit `لا_ينطبق`, and records for each the
matching remedy of the threefold treatment: separate each incident, tie the
treatment to its own incident, tie the incident to its circumstances; that is,
restore every text to its full context *before* any comparison. Deliberately
there is **no** priority order among the three: they are distinct kinds, not
degrees of one severity, so `defect_priority` is not replicated here and the
absence is recorded rather than left implicit
(`NO_PRIORITY_AMONG_APPARENT_CONFLICT_CAUSES_NOTE`). `الاشتباه` is not
`الاشتراك` — resemblance between two incidents is not multiplicity of
assignment in one word — and an import-time guard checks that the comparison
keys of the two vocabularies do not intersect
(`ISHTIBAH_IS_NOT_ISHTIRAK_NOTE`). A competing reading may carry the optional
`سبب_التعارض_الظاهر`, reported as `تصنيف_أسباب_التعارض_الظاهر` under exactly
the same inertness: absent from the derived specification, absent from the
audit outcome, read by no kernel gate.

Finally, a deferred result is no longer treated as a closed one. A balance
between two probable indications never settles in fact, because accepting it
would require one of three impermissible things — acting on both at once,
discarding both, or preferring one arbitrarily — so `DEFER` is read as *the
preponderating indication has not been found yet*, never as *none exists*
(`TAADUL_IS_NEVER_A_SETTLED_RESULT_NOTE`). Nothing in the gate changes: no
`BLOCK` path is introduced, and the status is neither softened nor hardened.
What changes is that the residual now says in its own text that the search for
a further preponderating indication remains open, and a deferred external audit
reports `حالة_البحث` as `بحث_مستمرّ_مطلوب` together with `ما_يُبحَث_عنه`, which
names the specific readings still sought rather than gesturing at openness in
general. Seeking a *preponderating* indication is a weaker claim than
establishing an *eliminating* one, so this marker licenses no elimination and
no accumulation of supporting indications into one
(`PREPONDERANCE_SOUGHT_IS_NOT_ELIMINATION_LICENSED_NOTE`);
`ONE_SOUND_ELIMINATION_SUFFICES_NOTE` stands unchanged.

`src/alghanem/arabic/manat_verification.py` runs the G0.EA.1 applicability gate
over one real Arabic word for the first time: `قُرُوء` in البقرة:228, through
`examples/external_audit/quru_2_228.yaml`. It adds no constitutional law; the
gate has existed since G0.EA.1 and had never been applied to linguistic
material. The card declares each `قرينة` with a closed two-value `جنس_البيان` —
`بيان_بالقول` for a textual indication (the verse's own
`وَلَا يَحِلُّ لَهُنَّ أَن يَكْتُمْنَ مَا خَلَقَ اللَّهُ فِي أَرْحَامِهِنَّ`, and Ṭabarī's
`جامع البيان` transmitting both readings by name) and `بيان_بالفعل` for a
lexical-usage indication (`لسان العرب`, مادة ق ر أ) — and no rank at all: a
`رتبة`/`أولوية`/`نتيجة` key on a `قرينة` fails the read rather than being
ignored, and the order is derived from the genus alone. The precedence of
`قول` over `فعل` is stated in this gate's own terms rather than assumed:
G0.EA.1 decides by the *weakest* model that closes and a stronger unresolved
model cannot override it, so `بيان_بالقول` is placed in the weakest, and
therefore non-overridable, position and `بيان_بالفعل` is declared stronger than
it (`QAWL_OCCUPIES_THE_NON_OVERRIDABLE_POSITION_NOTE`). A card declaring a
`بيان_بالفعل` قرينة without a single `بيان_بالقول` one is refused at read time,
so no lexical indication can ever be the weakest model and decide alone
(`FIL_NEVER_DECIDES_ALONE_NOTE`). `BLOCK` has no path in this layer and its
absence is declared, not covered. The named sources are cited as testimony and
nothing more: no corpus is read and no file digest is re-derived here
(`NAMED_SOURCE_IS_TESTIMONY_NOT_MEASUREMENT_NOTE`), and the two `بيان` terms
are used in the declared narrow sense, not the full usuli sense of the
Lawgiver's exposition. The result on the `قُرُوء` card is `DEFER` with one named
residual per unresolved rival reading — the competing `طهر` reading is declared
`غير_متعينة`, and the قول قرائن themselves transmit both senses from one named
source — and that deferral is the intended outcome, not a gap to be engineered
away into `PASS`. `ExternalAuditor != KernelAuthority` holds throughout: adding
a declared verdict field to the card leaves the gate's status unchanged, and an
evaluator sealed for a different claim scope is refused by the gate.

The same module now carries a second, independent genus beside `جنس_البيان`:
`QarinaFunction`, a closed two-value vocabulary of `قرينة_مؤيِّدة` (tilts toward
a reading without cancelling another) and `قرينة_مُقصِية` (voids one named rival
reading entirely at this position). It is added *beside* the qawl/fiʿl genus,
not in its place: neither `BayanKind` nor the derived order of
`derive_bayan_models` changed. Elimination is a **kind, not a degree**: a
`قرينة_مُقصِية` whose own statement merely calls the rival less likely — or
states no impossibility at all — fails at construction rather than being
silently demoted to `قرينة_مؤيِّدة` (`ELIMINATION_IS_A_KIND_NOT_A_DEGREE_NOTE`).
The impossibility test reads the qarina's own declared text, because a separate
`مستحيل: true` flag would let a preference-worded statement pass a formal check
on an unverified premise. One qarina names exactly one excluded rival — never a
list — and no function accumulates supporting qarain into an elimination, so a
single sound elimination closes the gate with no reinforcement, and repeating a
supporting qarina any number of times changes nothing
(`ONE_SOUND_ELIMINATION_SUFFICES_NOTE`). A `بيان_بالفعل` elimination removes
nothing by itself: this extends the existing `FIL_NEVER_DECIDES_ALONE_NOTE` by
naming it as its origin and testing the same عِلّة — the lexical indication does
not decide alone, therefore it does not eliminate alone
(`FIL_NEGATION_NEVER_ELIMINATES_ALONE_NOTE`). An undeclared `وظيفة_القرينة`
reads as `قرينة_مؤيِّدة`, because the default state must always be the weaker
claim, so `quru_2_228.yaml` is untouched and still defers.
`examples/external_audit/anna_2_223.yaml` is the first card to use the genus:
`أنّى` in البقرة:223, where the word `حَرْثَكُمْ` in the same verse — a
`بيان_بالقول` قرينة, no external inference — makes the `من أين` reading
impossible at this position, since what is not a place of tillage admits no
question about the direction of coming. The card closes at `PASS` with no
residual on a single elimination, against the `قُرُوء` card's `DEFER`. `BLOCK`
still has no path here and the elimination opens none: it removes a rival
reading, it does not falsify the tested model. This adds no constitutional row;
it extends G0.EA.1 by the same method as the قُرُوء application.

`src/alghanem/arabic/word_class_formal.py` adds the first Layer B proof whose
own structure aims at a *positive* result rather than a documented deferral. It
states, in `FORMAL` mode terms only, a `FrozenFormalDomain` of exactly two
binary questions taken verbatim from *الشخصية الإسلامية*, part 3, on the
division of the single word: "هل يستقلّ اللفظ بمعناه بلا حاجة للفظ آخر؟" and,
asked only when the first answer is `نعم`, "هل يدلّ اللفظ بهيئته الصرفية (لا
بذاته) على أحد الأزمنة الثلاثة؟". The admissible state set is exactly three —
`(لا، غير_مطروح)`, `(نعم، نعم)`, `(نعم، لا)` — because `غير_مطروح` is a
declared vocabulary value rather than a silent `None`, so the fourth state (`لا`
with the second question answered) is closed structurally instead of leaking in.
`classify` derives `حرف`/`فعل`/`اسم` directly from the two answers with no
default branch, and refuses any state outside the domain instead of mapping it
to the nearest one. Each of the four textually attested lexemes carries its two
explicit answers with their quoted evidence plus a closed
`حامل الدلالة الزمنية` field (`بالهيئة`/`بالذات`/`لا_دلالة_زمنية`) *from which*
the second answer is derived and checked, which is what keeps `أمس` — temporal
"بذاته لا بهيئته" — an `اسم` rather than a `فعل` by construction, not by
comment. `prove_over_attested_corpus` reports one row per lexeme without
stopping at a first failure; on the four attested lexemes (`مِن`, `قام`, `زيد`,
`أمس`) the derived class matches the attested class in every case, with no
exception and no ambiguous state, so the report carries the deliberately exact
title "أول شهادة صورية شاملة ناجحة على نطاق محدود".

Two limits are recorded as deliberately as the result. First,
`FormalClassification != BirthVerdict` and `DeclaredWordClass != BornOntology`:
this is documentation and formal classification only — no type in `kernel/`, no
`Freeze`, no `E0`, no gate reads it, it never enters a
`BirthExperimentSpecification`, and it leaves every external-audit field
byte-identical. It is therefore *not* a birth; that name would require a freeze
and an `E0` step that do not exist yet. Second, the scope is exactly four
lexemes from one named source and three classes: `مصدر`, `مضارع`, and
`لازم/متعدي` are excluded by declaration, because they need a morphological
source this repository has not supplied.

`src/alghanem/arabic/lafz_madlul_relation_formal.py` repeats that structure for
the relation between a lafẓ and its madlūl, from the same named source
(*الشخصية الإسلامية*, part 3), with one deliberate structural difference: the
classified unit is a *lafẓ cluster* (`عنقود لفظي` — one or more lafẓ, one or
more meanings, and the tested usage itself), not an isolated single word,
because `متباين` and `مترادف` describe a relation *between* several lafẓ and
because `حقيقة` and `مجاز` are separated by the tested usage rather than by the
bare word, so `الأسد` used of the beast and `الأسد` used of the brave man are
two distinct clusters. The `FrozenRelationDomain` states five questions — the
number of lafẓ, the number of meanings, then (only when one lafẓ carries
several meanings) whether the lafẓ was assigned to each meaning initially,
then (only when it was not) whether it became famous in the second meaning
until the first was abandoned, then (only when it did not) which meaning the
tested usage intends — whose admissible state set is exactly seven, one per
class: `منفرد`, `متباين`, `مترادف`, `مشترك`, `منقول`, `حقيقة`, `مجاز`. As in
the first certificate, `غير_مطروح` is a declared vocabulary value rather than a
silent `None`, `classify_relation` is total on those seven states with no
default branch and refuses every other state instead of approximating it, and
no answer is written freely: the first two are derived from the actual lexeme
and meaning counts, and the last three from closed carrier fields
(`حامل الوضع الابتدائي`, `حامل الاشتهار والهجر`,
`حامل المعنى المقصود بالاستعمال`) against which any hand-written answer is
checked and rejected — which is what makes flipping the fame carrier of the
`مجاز` cluster produce `منقول` by construction.
`prove_relations_over_attested_corpus` reports one row per cluster without
stopping at a first failure; on the seven
textually attested clusters (`الله`, `السواد`/`البياض`, `الأسد`/`السبع`,
`العين`, `الصلاة`, `الأسد` as `حقيقة`, `الأسد` as `مجاز`) the derived class
matches the attested class in every case, so the report carries the exact title
"شهادة صورية شاملة ناجحة على نطاق محدود". Its two limits are the same, and as
deliberate: `FormalClassification != BirthVerdict` and
`DeclaredRelation != BornOntology` — no type in `kernel/`, no `Freeze`, no
`E0`, no gate reads it, and every external-audit field stays byte-identical;
and the scope is exactly seven clusters from one named source and seven
classes, so the kinds of majāz relation (`مشابهة`, `مجاورة`, …), `كناية`, and
`استعارة` are excluded by declaration, because a closed vocabulary for them
would need one attestation per value to be branch-complete by construction, and
this repository has only one.

`src/alghanem/arabic/madlul_alone_formal.py` completes the set with a third
certificate from the same named source (*الشخصية الإسلامية*, part 3), on the
division of the **madlūl alone** into five sections. Its classified unit is a
single lafẓ *whose own signified is tested* — the question is what kind of thing
the madlūl itself is, not how the lafẓ relates to some other meaning — so it is
structurally simpler than the previous two: only three binary questions. The
`FrozenMadlulDomain` states them verbatim: "نوع مدلول اللفظ؟" (`معنى`/`لفظ`),
asked always; then, asked only when the first answer is `لفظ`, "تركيب اللفظ
المدلول؟" (`مفرد`/`مركّب`) and "حالة وضعه؟" (`مستعمَل`/`مهمَل`). The admissible
state set is exactly five, one per section: `معنى`, `لفظ_مفرد_مستعمَل`,
`لفظ_مفرد_مهمَل`, `لفظ_مركّب_مستعمَل`, and `هذيان`. As in the first two
certificates `غير_مطروح` is a declared vocabulary value rather than a silent
`None`, `classify_madlul` is total on those five states with no default branch
and refuses every other state instead of approximating it, and no answer is
written freely: each is derived from a closed carrier field
(`حامل جنس المدلول`, `حامل تركيب اللفظ المدلول`, `حامل حال الوضع`) against which
any hand-written answer is checked and rejected — which is what makes flipping
the usage carrier of `الكلمة` produce `لفظ_مفرد_مهمَل` by construction.
`prove_madlul_over_attested_corpus` reports one row per witness without stopping
at a first failure; on the five textually attested witnesses (`الحيوان`,
`الكلمة`, `الضاد`, `الخبر`, `الهذيان`) the derived section matches the attested
section in every case, so the report carries the exact title
"شهادة صورية شاملة ناجحة على نطاق محدود".

Its two limits are again recorded as deliberately as the result.
`FormalClassification != BirthVerdict` and
`DeclaredSignifiedKind != BornOntology` — no type in `kernel/`, no `Freeze`, no
`E0`, no gate reads it, and every external-audit field stays byte-identical; and
the scope is exactly five witnesses from one named source and five sections, so
the division of the signified lafẓ into `اسم`/`فعل`/`حرف`, the kinds of
compound, and the degrees of neglect are excluded by declaration. One further
scope limit belongs to the fifth branch alone and is recorded structurally
rather than hidden: the source itself says of `الهذيان` that "هذا القسم غير
موضوع، أي لم تضعه العرب؛ لأن الغرض من التركيب الإفادة، وهذا لا يفيد؛ ولكنه
موجود". That branch is therefore structurally valid and *must* be classified
like the rest, yet it falls **outside the scope of linguistic assignment**
unlike the other four. So, exactly as the `مجاز` branch of the second
certificate must declare its documented `علاقة`, the `هذيان` branch must declare
that out-of-assignment note and every other branch must leave it `لا_ينطبق`; the
note is a required field checked at construction, not a comment.

`src/alghanem/arabic/compound_layer_preregistration.py` is the compound layer's
registration, and deliberately **not** a fourth certificate:
`Preregistration != Certificate`. Four stages were requested for the compound —
the governance pair (`العامل والمعمول`), the predicative relations
(`النسب الإسنادية`), the two modes by which a maʿmūl affects the meaning
(`التضمين والتقييد`), and the three relational values
(`الفاعلية والمفعولية والمسببية`) — and the request fixes their outcome
vocabularies, their named refusals, and which stage reads another's output. What
it cannot fix is the one thing every existing certificate rests on: a named
source, its questions quoted by their own wording, and one textually attested
witness per branch. This repository contains none for the compound, which is
precisely why `madlul_alone_formal.py` deferred «أقسام المركّب (إسنادي وغير
إسنادي)» by name in the first place. So the honest artifact today is the frozen
*requirement*, not the proof: each stage is registered with its closed outcome
vocabulary (each including `لا_ينطبق` as a declared member rather than a gap),
its refusals by name and statement, and a non-blank note saying exactly which
source material is missing. There is no frozen domain, no carriers, no decision
function, no witness, and no proof, so the module carries no success title at all
— only `COMPOUND_SUCCESS_TITLE_IS_WITHHELD`, which says why one is withheld.

Three structural guards keep the registration from drifting into the thing it is
not. `AttestationStanding` is three-valued and its third member,
`شاهد_لكل_فرع`, is **declared but unconstructible** today under exactly the
discipline of `MeasurementProgress.CLOSED_BY_FROZEN_EXPERIMENT` and
`EvidenceGenus.MORPHO_FUNCTIONAL`: no authority here verifies that a text attests
a branch, so issuing that value would claim a check that never ran, and it is
refused *before* the general "no source supplied" message so that a refusal
grounded in absent authority is not read as the shallower absent source. The
dependency order is derived rather than written — stage three reads stage one's
outcome and stage four reads stage two's, which is what would keep two
certificates from disagreeing silently — so a registration whose written
prerequisites differ from the derived ones is refused at construction, as is a
stage placed before its prerequisite. And coverage precedes judgement as in
`WeakerModelExhaustionGate`: a missing stage and a duplicated stage each raise,
because a stage left unregistered is not a stage without limits.
`certificate_is_constructible` is `False` on every branch, no type here carries a
result, verdict, birth, or proof field (checked at import against its own
dataclass fields), the module imports nothing from `kernel/`, and every
external-audit field stays byte-identical. Two limits are recorded as
deliberately as the registration itself:
`RequestedVocabularyIsNotAttestedVocabulary` — that `عامل` and `معمول` are the
vocabulary the request names does not make them the source's vocabulary, nor
branch-complete — and the two standing deferrals in `madlul_alone_formal.py` and
`lafz_madlul_relation_formal.py` are left in their own wording, because editing
them now would suggest a debt was paid when the compound is still undivided and
`سببية` still unclassified.

`src/alghanem/arabic/kulli_juzi_formal.py` is a fourth certificate from the same
named source (*الشخصية الإسلامية*, part 3), on the division of the **name** into
`كلّي` and `جزئي` and the sub-divisions of each. Its structure differs from the
first three in one respect that is stated before the code rather than after it:
this passage does *not* yield a single four-level decision tree. It gives one
first-level partition and **three mutually independent sub-partitions** — two of
them partition the kullī set twice over (`متواطئ`/`مشكِّك` and `جنس`/`مشتق`) and
one partitions the juzʾī set (`علَم`/`ضمير`). Treating the two kullī axes as one
two-step tree would force every witness into a joint cell such as
`(كلّي، متواطئ، جنس)`, and the source attests no such cell: `الوجود` is attested
as `مشكِّك` and never placed on the genus axis, `الأسود` is attested as `مشتق` and
never placed on the equivocation axis. So the frozen domain is axis-aware:
`card(Ω) = 8`, each witness declares exactly *one* attested axis, asking a kullī
axis of a juzʾī name (or the reverse) is refused by `classify_kulli_juzi`, and
every witness on a kullī axis must carry a required
`ملاحظة استقلال المحورين` field — `لا_ينطبق` on every other branch — saying in
its own words that attestation on one axis is not attestation on the other. As
in the earlier certificates `غير_مطروح` and `لا_محور_مُثبَت` are declared
vocabulary values rather than silent `None`s, the decision function is total with
no default branch, and no answer is written freely: the first is derived from
`حامل وقوع الشركة` and both the declared axis *and* its outcome are derived
together from a single `حامل التفريع`, so flipping that carrier on `الإنسان`
produces `كلّي_مشكِّك` by construction. `prove_kulli_juzi_over_attested_corpus`
reports one row per witness without stopping at a first failure; on the nine
attested witnesses (`الحيوان`, `الكاتب`, `الإنسان`, `الوجود`, `السواد`,
`الأسود`, `زيد`, `عبد الله`, `هو`) the derived class matches the attested class
in every case, so the report carries the exact title "شهادة صورية شاملة ناجحة
على نطاق محدود".

Its limits are recorded as deliberately as the result.
`FormalClassification != BirthVerdict` and
`DeclaredUniversality != BornOntology` — no type in `kernel/`, no `Freeze`, no
`E0`, no gate reads it, and every external-audit field stays byte-identical; and
the scope is the attested witnesses of one named source and eight classes, so the
five Aristotelian universals, the degrees of `تشكيك`, the kinds of pronoun, and
any link between this division and the division of the lafẓ by signifier and
signified are excluded by declaration. One further limit belongs to the term
`جنس` alone and is recorded rather than assumed: in this source `جنس` is a
specific term *inside* the `جنس`/`مشتق` pair under the kullī — the lafẓ signifying
an unspecified essence. This certificate does **not** establish that it is the
Aristotelian logical genus, nor that it coincides with what another vocabulary
calls `الجامد`. That equation is an independent claim with no proof here, so it
is recorded verbatim in `JINS_IS_NOT_A_PROVED_SYNONYM_NOTE` as an unproved claim
that no function in the module reads — the same discipline as
`RequestedVocabularyIsNotAttestedVocabulary`: a name occurring in two
vocabularies does not make them one vocabulary.

Two additions to `src/alghanem/arabic/lafz_madlul_relation_formal.py` strengthen
what was already there without changing a single state, carrier, witness, or
result. First, the source's own **closure sentence** — «ينقسم اللفظ باعتبار
الدال والمدلول... إلى سبعة أقسام: هي المنفرد، والمتباين، والمترادف، والمشترك،
والمنقول، والحقيقة، والمجاز» — is recorded in `RELATION_CLOSURE_ATTESTATION` and
carried as a field of the frozen domain. Until now `card(Ω) = 7` rested on this
repository's reading of the source; it now rests on a quoted statement, and the
tie is checked rather than asserted: an import-time guard, repeated in
`FrozenRelationDomain.__post_init__`, verifies that every one of the seven
declared relation names actually occurs in that sentence, so adding an eighth
branch or renaming one to something the sentence does not name fails at import
instead of passing silently. Second, the source's preference rule on the
synonymy branch — «الترادف خلاف الأصل» — is recorded in
`MURADIF_PRESUMPTION_NOTE` and deliberately left **inert**: no function reads it,
it enters neither the domain nor any carrier, and a test asserts it is mentioned
exactly once in the module body. That is not timidity but typing: it is a
defeasible preference to be applied *under doubt*, whereas the decision function
is total on a closed domain that has no doubt state, so making it operative would
mean introducing a hesitation state the domain does not have — a change to the
certificate's structure rather than a strengthening of it.

`src/alghanem/arabic/convergence_claim_register.py` records **claims about
convergence and their standing**, and is emphatically not a convergence verdict:
`ClaimRegister != ConvergenceVerdict`. There is no convergence machinery in this
repository at all — no type, no gate, no measuring function — so a named
criterion invented in conversation is not a test that ran, and saying a claim
"satisfies" one presents a personal judgement in the shape of an automated check.
That refusal is registered by name as `NamedCriterionIsNotABuiltGate`. Two claims
are registered today. The first — that classifying the *shariʿ* names into
«متباينة ومترادفة ومشتركة ومشكِّكة ومتواطئة» is a second independent application
of one classification to different material — stands as `مرفوضة_بفحصٍ_مباشر`,
because direct inspection shows the list takes **three branches** from the
sevenfold signifier/signified classification (`متباين`, `مترادف`, `مشترك`) and
**two outcomes** from the equivocation axis under the kullī (`متواطئ`, `مشكِّك`):
it merges two independent classifications rather than re-issuing one of them on a
new test case. The refutation is required by construction to name both merged
classifications with their own modules and borrowed branches, and it is recorded
as final for the claim *as stated* rather than pending — `RefusalIsNotDeferral` —
because the defect is in the claim's structure and no later evidence added to
either classification removes it. The second claim, that the source contains a
section named «المتوسطة», stands as `مصدر_مُسمّى_غائب`: the term occurs in no
text supplied to this repository, and substituting a synonym or hunting for one
without instruction is refused by name. Coverage precedes judgement as elsewhere:
a missing or duplicated claim raises, the third standing
(`مقبولة_بسلطة_تقارب`) is declared but **unconstructible** today under exactly the
discipline of `شاهد_لكل_فرع`, no type carries a result, verdict, birth,
certificate, or proof field (checked at import against its own dataclass fields),
the module imports nothing from `kernel/`, every external-audit field stays
byte-identical, and there is no success title at all — only
`CONVERGENCE_SUCCESS_TITLE_IS_WITHHELD`, which says why one is withheld.

`src/alghanem/arabic/distributional_probe_report.py` is deliberately **not** a
fourth certificate: it records a *negative* measurement with the same
discipline the three positive ones use. Over 2193 surface forms (support ≥ 5),
with five purely distributional features — length, final-position ratio,
successor diversity, predecessor diversity, and silent-skeleton host diversity
— a scan of `k` from 2 to 11 under `silhouette` alone selected **k = 2, not
3**, with an unbalanced split (2159 vs 34). That partition did not reproduce
the `اسم`/`فعل`/`حرف` division, and the module says so structurally rather
than in prose: `ProbeOutcome` is a closed three-value vocabulary
(`أعاد_اكتشاف_التقسيم`, `اكتشف_طبقة_أخرى`, `لم_يفصل`), the recorded report
declares `اكتشف_طبقة_أخرى`, and `الادّعاء_المنفي` is a **required** field on
every negative outcome that must be `لا_ينطبق` on a rediscovery outcome —
exactly as the `هذيان` branch above must declare its out-of-assignment note
and every other branch must not. What the probe did find is recorded as two
named layers rather than forced onto a grammatical label: `فرط_اتصال` (34
members at k=2, 26 at k=3), which mixes true particles (`في`, `من`, `على`,
`إلّا`, `إنّ`) with very high-frequency content words (`الله`, `الذين`,
`قال`, `كان`) under one distinguishing signature — huge frequency, near-zero
final ratio, very high connection diversity; and `فاصلة_قرآنية` (289 members
at k=3), whose high final ratio (0.5–1.0) with near-zero successor diversity
structurally favours `يَعْلَمُونَ`-type plural imperfects and the `فعيل`
pattern. The second is a **stylistic/rhythmic** effect — Qur'anic verse
cadence — not a grammatical class, and that distinction is enforced rather
than annotated: each layer's `طبيعة` is derived from its kind, and no
discovered layer may declare itself `نحوي`, because that is precisely the
claim the measurement failed to establish. Consistency is checked too: cluster
sizes must total the declared form count, every partition's `k` must lie
inside the scanned range, and a layer's member count must be an actual cluster
size of the partition it is claimed at.

Its limits are recorded as deliberately as the result. This module is a
*record of a measurement, not a measurement pipeline*: it reads no corpus,
computes no feature, runs no clustering, and cannot reproduce its own numbers;
reproduction would need a deterministic pipeline with a named corpus, a frozen
seed, and a declared stopping rule, which does not exist here. It declares no
replacement feature and no second experiment either, because choosing features
*after* seeing the clusters is exactly what the pre-evidence gate in `kernel/`
forbids, so any follow-up needs a specification frozen before its evidence.
And authority-wise it is inert like the rest: `ProbeOutcome != BirthVerdict`
and `DiscoveredCluster != BornOntology` — no type in `kernel/`, no `Freeze`, no
`E0`, no gate reads it, and every external-audit field stays byte-identical.
The module carries no success title at all, since dressing a negative result
in the three certificates' title would be disguise rather than record.

`src/alghanem/arabic/probe_preregistration.py` closes the one gap that record
left open. That module freezes a *past* experiment's specification alongside
its result, but for a *future* experiment it offered only a prose constant, so
nothing structurally prevented a later result from having its features chosen
after its clusters were seen:

```
FrozenProbeSpecification (recorded past run)
    != EnforcedPreEvidenceSpecification (binding future run)
```

`FrozenFollowupProbeSpecification` declares `experiment_id`, `revision_id`,
`revision_sequence`, an `EvidenceGenus`, the frozen feature set, support
threshold, scanned-`k` range, `SelectionCriterion`, `StoppingRule`, and a
declared evaluation criterion — and carries **no result field at all**, which
is checked at import against the dataclass's own fields rather than trusted.
`PreEvidenceProbeSpecificationRegistry.freeze` is the only issuer of a
`FrozenPreEvidenceProbeManifest`, and refuses different content re-frozen under
the same `(experiment_id, revision_id, revision_sequence)` identity;
`FollowupProbeSpecificationContentBinding` re-encodes the live specification
and compares canonical bytes, so post-freeze drift cannot be bound. A
`ProbeResultAttachment` is then *unconstructible* without that binding, and
refuses at construction — never as a warning — any feature outside the frozen
set, any selection criterion or stopping rule other than the frozen ones, and
any `k` outside the frozen range.

`EvidenceGenus` is deliberately two-valued (`توزيعي`, `صرفي_وظيفي`) with **no**
`MIXED`: combining two genera is an explicit composition
`(E_distributional, E_morphological, CompositionRule)` needing a contract that
does not exist yet, and a shorthand enum value would hide that structure. The
morpho-functional genus is declared but not yet constructible, because no
frozen morphological feature vocabulary has been born — refused with that exact
reason rather than silently admitted.

`Phase2OpenQuestion` records the scientific question with **no answer or
verdict field**, and requires all three hypotheses rather than a false
dichotomy: (A) only these five features are insufficient; (B) the
`اسم`/`فعل`/`حرف` division is not a surface-distributional kind at all, so no
enlargement of that evidence genus recovers it; (C) the division is recoverable
distributionally, but only after lower structural variables (boundary,
position, morphological transformation) are themselves born as licensed
carriers — which is what `Closure_L -> Handoff_L -> Birth_{L+1}` would predict.
This PR answers none of them.

`src/alghanem/arabic/readiness_rank.py` closes the level-up of that same gap:
the four-rank phase-2 status table (`BUILT_AND_CHECKED`, `NOT_YET_FROZEN`,
`NOT_STARTED`, `OPEN`) previously existed only as prose in a pull-request body,
where nothing stopped it from later being read as an enforced fact —
`RecordedStatusProse != EnforcedReadinessRecord`. It is now a
`ReadinessRankRecord` over **four independent closed vocabularies**
(`StructuralReadiness`, `SpecificationFreeze`, `MeasurementProgress`,
`QuestionStatus`) rather than one enum with four values, because a single
ladder implies a false total order in which a higher rank looks entailed by its
position. Four is the minimum sufficient count, not an assumption: merging
structure with freeze would make freezing an automatic promotion of a checked
build, though a checked build with no frozen future specification is exactly
today's state; merging freeze with measurement would erase the difference
between a frozen specification that binds every later measurement and no
specification at all; merging measurement with the question would make a
completed measurement a settlement. Implication runs **one way only**, as a
prior condition: measurement beyond `NOT_STARTED` requires `FROZEN`, `FROZEN`
requires `BUILT_AND_CHECKED`, and closure requires `COMPLETED` — while a frozen
specification with no measurement yet, and a completed measurement with an open
question, are both admissible states now. `CLOSED_BY_FROZEN_EXPERIMENT` is
declared in the vocabulary but unconstructible, under the same discipline as
`MORPHO_FUNCTIONAL`, and is refused at construction of *any* record rather than
only in the module-level one, with its own named reason (no birth gate exists
here to issue a closure) checked before the general implication message. Each
rank carries a non-blank justification, and the single `PHASE2_READINESS` takes
its `question_id` from `PHASE2_OPEN_QUESTION` rather than copying it, so the two
cannot drift.

Authority-wise the module is inert like the record it guards:
`ProbeResultAttachment != BirthVerdict`,
`FrozenFollowupProbeSpecification != BirthExperimentSpecification`, and its
freeze registry is a local documentation-layer registry, not a kernel
authority — no `Freeze`, no `E0`, and no kernel gate reads any of it, which is
asserted by a test that scans every `kernel/` module for such a reference. The
only thing shared with the kernel is `src/alghanem/canonical_content.py`, an
authority-free canonical-encoding and digest primitive now used by both this
module and the kernel's two encoders, so that one canonicalization rule cannot
drift into two; `Canonicalization != Authority`, and importing it transfers a
byte encoding and nothing else. No measurement pipeline, corpus, or Phase-2
experiment is created here.

`src/alghanem/arabic/imported_feature_vocabulary.py` builds the Alghanem half of
the cross-project import that the readiness work named as missing: the source
project `GFLK-Taaqol-GPT` exports the `OriginType` vocabulary
`gflk.origin_type.v1`, derived from the `ORIGIN_LEDGER_AR_v1` ledger, with a
deterministic content id and a self-declared `FROZEN_LOCAL` freeze scope. The
boundary the module keeps is `ForeignFrozenExport != LocalFreeze`, one level
above `Canonicalization != Authority`: `ForeignFreezeScope.FROZEN_LOCAL` is read
as declared and never promoted — no function here turns it into
`SpecificationFreeze.FROZEN`, a kernel `Freeze`, an `E0`, or a birth. The
imported vocabulary is bound to `EvidenceGenus.MORPHO_FUNCTIONAL` and refuses
any other genus, its `OriginType` vocabulary is closed with `UNRESOLVED` as a
member rather than a gap, and its distribution is a *derived* count over the
entries: a declared distribution or row count that disagrees with the derived
one is refused, so no field exists that the answer can simply be written into.
`ImportedVocabularyContentVerifier` is the sole issuer of a
`VerifiedVocabularyImport`, re-deriving an Alghanem-side content id through the
same shared `canonical_content` primitive rather than trusting the digest the
export declares, with the encoding schema checked at import against the
dataclass fields. `assert_matches_recorded_release` pins the recorded release —
270 rows, 126 `EVENT` / 56 `ENTITY` / 88 `UNRESOLVED`, the source ids and the
declared source digest — so a mismatched import is refused rather than passed
through silently.

Two things this deliberately is *not*. It is not the deferred born
morpho-functional vocabulary: an imported foreign vocabulary is not one born
here, and the five distributional features and `RECORDED_PROBE_REPORT` are
untouched, byte for byte. And it is not a kernel authority: no `Freeze`, no
`E0`, no verdict, and no kernel gate reads it, asserted by a test that scans
every `kernel/` module. The scope stays narrow to `OriginType` alone, because
the weight and structure vocabularies have not been exported yet and a general
frame assuming them would be an abstraction ahead of its referent.
`src/alghanem/arabic/imported_vocabulary_source_digest.py` makes the source
digest *testable* rather than verified, and the distinction is load-bearing. It
deposits the source's `gflk.canonical.v1` schema byte-precisely
— each entry's `root` and `origin_type` joined by `U+001F`, entries sorted by
root and joined by `U+001E`, UTF-8 with no BOM and no additional Unicode
normalization, hashed with the shared `canonical_content` digest primitive — so
`verify_source_declared_content_id` recomputes a source id from the entries
instead of comparing a declared number to itself. Separators inside a field,
duplicate roots, an out-of-vocabulary origin type, and an unrecorded
canonicalization version are all refused, a mismatch names both of its possible
causes (a changed payload versus a differently applied schema), and
`RederivedSourceContentIdentity` is issuable only by that verification.
Re-derivation transfers no authority: `REDERIVATION_IS_NOT_AUTHORITY_NOTE`
records that identical bytes are not a promoted freeze, a birth, or a kernel
permission.

What this does *not* change is the evidence state of the pinned number itself.
The full 270-row source payload is still not in this repository, so
`facf6720…ba85f` remains **declared and not re-derived**, exactly as before the
schema was deposited; only its testability changed. The decisive test
(`test_recorded_release_digest_is_rederived_from_the_deposited_export`) is
`skipped`, not `passed`, and a companion test asserts the fixture is still
absent so the skip cannot rot into a silent pass.
`SOURCE_DIGEST_REDERIVATION_NOTE` is therefore left in its original cautionary
wording rather than rewritten to sound settled, and
`SOURCE_DIGEST_REMAINS_DECLARED_NOTE` states the point in the module. Nothing in
the current pipeline depends on that digest being correct: no kernel module, no
gate, and no other Arabic module calls anything in this file — exporting it from
`alghanem.arabic` is availability, not consumption — which a tree-scanning test
enforces, so a future mismatch has no accumulated implicit assumptions to trace.
Tool readiness is not evidence; only the deposited payload closes this part.

What *is* known about that digest is recorded and enforced: by the
export generator's own self-check, the source content id is computed over only
each entry's `root` and `origin_type`, so `raw_category` and `batch_note` can
change without moving it. The Alghanem-side identity covers every entry field,
making it strictly finer rather than equivalent — an import-time guard asserts
that `SOURCE_DIGEST_COVERED_FIELDS` is a proper subset of the entry fields, so
the two digests can never be read as attesting the same thing.

`src/alghanem/arabic/mantuq_mafhum_ifada.py` gains the eighth link's one strict
qualification. That link's division is exhaustive — مطابقة and تضمن are منطوق,
التزام is مفهوم, and there is no third — but one thing never falls on the مفهوم
side: **the type of the ruling itself**. It is منطوق always, never derived by
مفهوم موافقة or مخالفة from an accompanying descriptor; only a ruling's side
qualifications are read that way. `SignifiedAspect` names what a reading falls
upon, `نوع_الحكم` or `قيد_جانبي`, and `RulingAspectReading` refuses exactly one
combination at construction: the type of the ruling read through
`DalalaChannel.مفهوم`. The aspect is not a rung inside the channel and ranks
nothing: reading a side qualification by مفهوم stays open, and a test asserts
it. The channel is read off the held `DalalaRecord` rather than rewritten, so it
stays derived in one place, and the descriptor a مفهوم was read from must be
named while a منطوق carries none — so no مفهوم is attributed to an unnamed وصف.

`src/alghanem/arabic/wad_naql.py`, `src/alghanem/arabic/umum_khusus.py`, and
`src/alghanem/arabic/decision_chain.py` build the fourth link, the tenth link,
and the ledger of the decision chain itself (G0.W in `docs/CONSTITUTION.md`).
The chain runs from an identity-free codepoint to a concept grounded in sense,
and its two third links — the signifier alone (statistical) and the signified
alone (philosophical) — do not meet on their own: neither knows one particular
lexeme paired with one particular meaning. Their pairing is the **وضع**, and
`wad_naql` is its place. The origin is not written into a field: `WadOrigin`
becomes `وضع_بشري` only by a two-part refutation of divine institution — no path
by revelation (a vicious circle, since revelation is understood only through a
prior language) and no path by necessary knowledge (which would entail necessary
knowledge of God, contrary to observed fact) — with both grounds required and
each quoted verbatim from one named source, *الشخصية الإسلامية* part 1, on
الوضع. `وعلَّم آدم الأسماء` is read there as the teaching of the realities and
properties of things, a direct concept rather than lexemes, and the lexeme
reading is a named refused member rather than a silent absence. The consequence
is the point of the link: a `WadRecord` carries its path of knowledge only as a
`TransmissionStanding`, and the two derivational routes are refused by a
function that always raises. This is deliberately *not* a correction of
`ONLY_LEGITIMATE_TARGET_NOTE` in `maluma_mafhum`: a settled convention really
does leave a distributional trace, and that note describes it correctly. What a
trace cannot do is say which lexeme was paired with which meaning, since an
equivalent regularity can arise from incidental repetition or sample bias — so
`DistributionalCorroboration` is constructible only over an already transmitted
record, its function is fixed at `يرفع_دراية`, and the standing after
corroboration is the standing before it.

`umum_khusus` closes the tenth link on one rule: the general is specialized by a
`مفهوم` **without the first evidence being dropped**. A `TakhsisRegistration`
holds the general, the specializer, and a named conflict locus, and there is no
field into which a discarded evidence could be written — an import-time sweep
refuses one, so `Takhsis != Ihmal` is unconstructible to violate rather than
merely discouraged. The channel is derived from the specializer's own
`DalalaChannel`, imported from `mantuq_mafhum_ifada` rather than duplicated, and
a specialization with no named locus is refused because the default between two
texts is difference, not contradiction. Its second half keeps two branchings
apart: a general rule branches onto individuals, a universal rule onto
particulars. `RuleGenus` is its own closed vocabulary and not `Universality`
from `kulli_juzi_formal`, because that one classifies a single *word* and
mapping its `جزئي` onto a general rule would be the genus confusion the rule
forbids; a foreign value is refused rather than coerced. Like its siblings it is
a registration, not a certificate: it names no source text and issues nothing.

`decision_chain` reads the chain's fifteen positions off the tree in the manner
of `pipeline_stations`, and adds what a station table does not need: **reach is
derived by succession**, because each link conditions the next. A coded link
preceded by an unreached one reads `مسبوقة_بحلقة_غير_بالغة`, which is what keeps
the chain from appearing complete while links 1 and 2 — the carrier, and the
(carrier, state) derivative — remain deferred under `KnotNotEssence`. Deferral
by law is declared and names its constitutional law; absence of a module is
never read as deferral by itself. The two governing constraints are recorded as
the chain's frame rather than positions in it, and neither can be declared
coded: constraint (أ) would need a written universal idea for GFLK against which
an epistemically loaded tool could be measured, and this repository has none —
the gap is recorded structurally here instead of being smoothed over in prose,
and writing that idea is left as separate work. Constraint (ب) admits only one
acceptable test, a complete application to a real word or verse, and not the
description of yet another stage of the measuring apparatus — and that test has
now been *run* rather than argued about. `examples/external_audit/malik_114_2.yaml`
carries مَلِك at الناس:٢, chosen because the word's spelling there is not
disputed: the مالك/مَلِك contest belongs to الفاتحة:٤ and is a contest of
*reading*, not of signification, which the card excludes by name rather than by
silence. `tests/arabic/test_malik_114_2_card.py` drives that one card through
links ٤–١٣ and derives, from the card's own text, which link stops it: the
fourth, الوضع بالنقل, because a manat-shaped card declares its named sources but
never declares the *path* by which they arrived — no member of
`TransmissionStanding` appears in it, which is the very same absence that stops
link ١٢. Links ٥, ٦ and ٧ stand up on the card, and are therefore *not* read as
reached, by the same succession rule the ledger applies everywhere. So the two
governing constraints stay `مُصرَّح_غير_مُرمَّز` but no longer for one reason:
(أ) lacks a theory nobody has written, while (ب) lacks nothing but a traversal
that stopped at a named position. No `jiddiya_ifada.py` is created, because a
module measuring an application that did not complete is exactly the *further
stage of the measuring apparatus* that constraint (ب) forbids; and no third
standing member is opened, since a distinction is admitted here only when one
side can be derived.

`src/alghanem/arabic/classical_kernel_map.py` adds the seventh and last G0.N
module, the twelve-row map of §8. Every row carries a `سند` from a closed
three-member vocabulary — `مُشتقّ_من_الشيفرة`, `اجتهاد_ترجمة`,
`مُصرَّح_غير_مُتحقَّق` — and the row is checked against the tree rather than
trusted: the named kernel structure's existence is read from
`src/alghanem/kernel` itself (by parsing definitions, not by importing, so the
Arabic layer still imports nothing from the kernel). A structure that does not
exist may not claim derivation from the code, and a structure that does exist
may not be recorded as merely declared, because in either case the check
actually ran and came out otherwise. That rule is what makes the `Carrier` row
honest: the document's map assumes a kernel `Carrier`, and there is none in
this tree, so the row reads `مُصرَّح_غير_مُتحقَّق` derived from absence rather
than asserted. The `اجتهاد_ترجمة` rows record the remaining, more important
caution: matching a classical concept to a kernel structure is a **translation
judgement, not a transmission** — naming `State` opposite الحال does not mean
the classical authors meant this structure, only that the structure named is
really there. The map issues nothing and is read by nothing.

`src/alghanem/arabic/pipeline_stations.py` adds the sixth G0.N module, the
eleven-station table of §9. The table is **derived, not written**, on the model
of `milestone_ledger`: each station names its module by path, and whether that
module exists is read from the tree itself, so a station whose module is absent
reads as `محطة_غير_مُرمَّزة` rather than being skipped in silence — and an
absent Arabic package is refused outright rather than read as "no modules",
because an unread tree cannot report emptiness. Every station carries an
epistemic state from a closed five-member vocabulary (`معلومة`, `فرض`, `آحاد`,
`آحاد_مُجمَّد`, `ظنّي`), so the epistemic distance between raw observation and
a distributional probe is visible in the table rather than assumed by position.
Station 0 — the spoken sound — is **refused inside the table by its own
message**: this repository's data is encoded text and not recorded sound, the
same refusal `UnicodeIsNotRecordedSound` makes in `epistemic_layers`. Station ∞
is moduleless by necessity rather than by omission, and is therefore declared in
a note and never given an ordinal that could later be "filled in". Like its
siblings the ledger is a reading of the tree, not an authority over it.

`src/alghanem/arabic/qiyas_rabt_registration.py` adds the fifth G0.N module,
on analogy and linking (§10). It is a **registration, not a certificate**, on
the model of `compound_layer_preregistration`. A `QiyasRegistration` carries
the four classical pillars, and its origin is not free text: `asl_reference`
must name one of the frozen formal domains **derived by import** from the
repository itself (`frozen_asl_references()`), so an analogy cannot be anchored
to something that was never frozen here — which is exactly why the document's
own examples (`prefixes ⊂ ziyada`, `SUN-MOON-LETTERS-AR-1`) cannot be
registered as origins at all and are recorded instead as `ForeignDeclaredCase`,
declared and never verified, on the model of `ForeignDeclaredAim`. The standing
is derived from `illa_application` alone: an illa that actually applies yields
`صحيح_من_أصله`, while mere categorial resemblance or an illa absent from the
text yields **`باطل_من_أصله`, not "weak"** — weakness is a degree within a
standing analogy, invalidity from the origin denies that one stands, so the
vocabulary has exactly two members and no gradation between them. For linking,
an imported connection that was never tested is `استرجاع`; `ربط` is declared
and structurally unconstructible, refused with its own message when no held-out
sample is supplied and with the unconstructibility note when one is, because no
authority here runs a generalization over cases withheld from the certificate's
own formation. No kernel module reads any of it, and external-audit output is
unchanged.

`src/alghanem/arabic/maluma_mafhum.py` adds the fourth G0.N module, on the
ontological triad of §3. A correct structural/syntactic reading of a text is
**information only**: `UnderstandingRecord` derives `معلومة` whenever the sanad
is empty, and writing `مفهوم` there is refused, so the promotion cannot be made
by assertion. Information becomes a concept only through a delegation chain
that terminates in direct sense, modelled exactly like the delegation chain of
`SealedInvariantExtractorRegistry`: each `SanadLink` either *is* direct sense
(and therefore has no earlier link) or delegates to a named earlier link, the
chain must be connected, a link delegating to itself is refused, a second
direct sense inside the chain breaks it, and a chain that never reaches sense
yields no concept **however long it is** — length is not a substitute for
termination. The other two targets of "meaning" are excluded **structurally,
not practically**: correspondence to the external world needs evidence entirely
outside language, and the individual speaker's intention is excluded by the
explicit text of `NoIntentProjection`; both are declared members of the closed
`SemanticTarget` vocabulary and refused at construction with their own reasons,
leaving `استرجاع_الوضع` — stable distributional regularity across a linguistic
community — as the only legitimate target. The module is inert: no verdict, no
intent field, no kernel module mentions it, and external-audit output is
unchanged.

`src/alghanem/arabic/riwaya_diraya_registration.py` adds the third G0.N
module, on the two acceptance gates of §4. They are two structurally separate
readers, not one record with two fields: `RiwayaReading` carries only the
channel — tool identity, digest, change-log reference, and whether the result
was reproduced independently — and `DirayaReading` carries only the matn, on
one of two typed branches. The channel standing is derived from independent
reproduction alone and a written standing contradicting it is refused, so a
tool cannot be declared sound while its result fails to reproduce (the
`isti'la p=0.000` shape). The **remedy is derived from the kind of failure,
never written**: a riwaya failure yields `إصلاح_الأداة`, an ontological diraya
failure yields `إعادة_تعريف_الفئات`, an epistemological one yields
`تشديد_اختبار_الأدلة`. That derivation is the refusal named
`CategoryRedefinitionIsNotEvidenceTightening`: a matn that is of the wrong
genus cannot be rescued by tightening an evidence test that does not touch it,
and a matn defeated by something stronger and already frozen cannot be rescued
by reclassifying its categories. The branch distinction is enforced at
construction rather than trusted: an epistemological reading must name the
stronger frozen matn it was tested against, and an ontological reading — being
prior to any evidence — is refused if it names one at all, because its question
is classificatory. Continuing scrutiny is structural too: a reading carries
one or more `IndependentApplication` entries and **no `اجتيزت`/passed field**,
repeated survival reads as "لم يُهزَم بعد" and never as "ثابت", and a single
defeat among many survivals still reads as defeated. Like its siblings the
module is a **registration, not a gate**: it issues no verdict, and no kernel
module mentions it.

`src/alghanem/arabic/transmission_standing.py` adds the second G0.N module,
on the three degrees of certainty and the two scopes of induction. The three
degrees — `متواتر`, `آحاد`, `فرض` — are not a ladder that a growing number
climbs: their conditions are qualitative, and the module carries **no count
field at all**, checked at import against the dataclasses' own fields, because
a field counting sources would reopen the very door ("many narrators make
recurrence") the qualitative conditions close. The degree is derived from
three closed carriers — basis of knowledge (direct observation versus
inference), source independence (collusion impossible versus not
established), and repetition pattern (successive independent cycles, a single
batch, or none) — and `derive_standing` is total over them with no default
branch; a written degree contradicting its carriers is refused at
construction, so there is no place to write the answer directly.
`متواتر` is declared in the vocabulary and unconstructible, but — under
`TawaturRequiresDiachronicSuccession` (G0.N) — by a **category mismatch rather
than a missing tool**: recurrence presupposes succession through time, and a
closed corpus is a frozen synchronic section that carries no temporal
dimension in which successive independent cycles could occur, so asking
whether a finding over it is `متواتر` is ill-posed rather than unanswered for
now. The two genera are kept apart in `UnconstructibilityGenus` instead of
being merged into one "unconstructible", on the model of what
`DeferredValueShape` revealed about holds: over a synchronic structure the
refusal is categorical and no future authority lifts it, while over a genuinely
diachronic succession it falls back to an ordinary hold for missing authority,
and `unconstructibility_genus` derives which from the structure alone with no
default branch (a third member, `GENUS_NOT_SETTLED`, is declared and never
derived, so nothing is carried onto the nearer genus). The refusal is still
raised with its own message before the general carrier-mismatch one. For the
same categorical reason there is **no import entry for a foreign recurrence
claim**: importing a declared-unverified claim makes sense where the concept
applies and only the check is missing, as with `ForeignDeclaredCase`, not
where the question does not stand at all — so `متواتر` stays a member with no
entrance, with that reason written rather than left silent. Three residuals
are named in the module instead of being folded away: the succession carrier
stays writable because no authority here derives a report's temporal
structure; the sibling holds elsewhere in the tree are deliberately not
classified by genus here; and the provenance of this design's convergence with
a prior external discussion is recorded as unverifiable in this repository and
is never read as independent corroboration. The two
induction scopes are handled the same way: a complete enumeration over a
closed corpus is certain **inside that corpus only**, and the scope sentence
is derived by `derive_scope_statement` rather than written, with a declared
sentence that differs from the derived one refused at construction — so
generalizing directly from a closed corpus to the open language it was drawn
from is structurally unsayable rather than avoided by hedging prose
(`is_certain_beyond_the_enumerated_set` is `False` structurally). Finally the
exemption of "the first organized information" from the full birth protocol
is recorded as `FIRST_ORGANIZED_INFORMATION_QUESTION`, an open question with
all three hypotheses and **no answer field**, on the model of
`Phase2OpenQuestion`: self-evidence to the researcher is not recurrence, and
that difference is exactly what the qualitative conditions separate. The
module is inert like its siblings: `TransmissionStanding != BirthVerdict`, no
`Freeze`, no `E0`, no kernel gate reads it, and every external-audit field
stays byte-identical.

`src/alghanem/arabic/epistemic_layers.py` is the first module written under
G0.N, and it closes the layer confusion that law names rather than the law
itself. Three layers are kept apart as one closed vocabulary — physical
existence (sound as a perceived phenomenon), the conventional knot (the
letter as a written convention), and statistical attribute analysis — and a
piece of evidence never carries a written layer label:
`DeclaredLayerLabel != DerivedOntologicalLayer`, enforced exactly as
`provenance_genus.py` enforces its own genus. `OntologicalLayerGate` is the
sole issuer of a classification and derives it from the artifact's own type,
so a `RawSurfaceObservation` or a `NormalizationAudit` is the conventional
knot and a `DistributionalProbeReport` or one of its `DiscoveredLayer`s is
statistical attribute analysis, while an artifact of any other type is
refused by its type name rather than mapped to the nearest layer. Each
layer's epistemic standing is derived from the layer and never written
beside it, and the three standings are checked at import to be pairwise
distinct. The physical layer is declared in the vocabulary and structurally
unconstructible: no artifact here is recorded sound, so issuing a physical
classification would claim a measurement that never ran
(`UnicodeIsNotRecordedSound`), and dropping the member instead of refusing it
would suggest the two remaining layers are all there is — which is the
confusion being avoided. `CrossLayerInferenceRecord` then models the one
legitimate way the layers may be related at all: a declared external
citation, recorded as `مُصرَّح_غير_مُتحقَّق` and never promoted, because
`CrossLayerInferenceIsImported` — reading a statistical cluster as physical
homogeneity is an inference imported from outside this pipeline, not a
product of it. `VERIFIED_LOCALLY` is declared and refused at construction
under the same discipline, since no authority here inspects evidence outside
language, and `is_produced_by_this_pipeline` is `False` structurally.
Authority-wise the module is inert like its siblings:
`OntologicalLayerClassification != BirthVerdict`, no `Freeze`, no `E0`, no
kernel gate reads it — asserted by a sweep over every `kernel/` module — and
every external-audit field stays byte-identical.

G0.N declares, law-only and ahead of any runtime, what a carrier *is*:
`Carrier != DiscoveredEssence`, and a carrier is instead a knot tied by
convention at the one point on a fiber of regularity that survived every
weaker model licensed and frozen for its own experiment. Its structural
consequence is about `Freeze`: freezing fixes a knot at one declared version
of the fiber — one tool, one corpus, one normalization policy — so reopening
when that version changes is the condition of the knot's continuity rather
than a defect of the earlier freeze, which is why `FreezeIsFiberVersionScoped`
composes the existing `G0.F.1` reopen protocol instead of forking a second
one. `NodeContinuityIsContentNotOccurrence` names exactly which half of the
continuity question the repository already answers and which it does not:
`TransitionContentIdentity` and `OCCURRENCE_ONLY_EXCLUSIONS`
(`src/alghanem/kernel/content_identity.py`) already make it impossible for
`admission_id` — a fingerprint that an execution happened, not of which
phenomenon it was about — to enter a content identity, but deciding that two
content identities produced under two tool versions name one knot is issued
by no authority here and does not follow from digest equality alone.
`NoIntentProjection` unifies `NoLabelLeak` and `NoOracleTuningBeforeFreeze` as
two applications of one origin, forbidding both the original author's intent
and the running researcher's expectation as grounds for settling a
candidate's meaning. `ExistenceIsBinaryRankIsGraded` and
`RankNeverCertifiesEssence` separate the binary existence judgement, which
`StructuralDecisionStatus` already carries, from graded evidential rank, which
has no machinery in this repository at all; and
`CompleteInductionIsCorpusBounded` and
`NoBedrockWithoutRecurringDirayaSurvival` bound what an exhaustive corpus
result may be said to establish and refuse to read repeated survivals as
bedrock. The whole section is declared law: no runtime, class, enum, gate,
rank primitive, or continuity authority is introduced by it. See the "G0.N"
section of `docs/CONSTITUTION.md`.

G0.F declares, ahead of any runtime, that factorization is the general case
of birth (a domain may close with one factor, several jointly-necessary
factors, or none) and that fractality is a law, not a folder layout: a
frozen factor must be reopenable inside a later, higher experiment without
being reborn, copied, or renamed. G0.F.1 adds contract skeletons for that
reopen protocol —`FrozenFactorRef`, `BornBridgeRef`, `DerivedRelationSpec`,
`ReopenExperimentSpecification`, `FractalProvenancePath`, `ProofLineageEdge`, and
`FractalSnapshot` (`src/alghanem/kernel/fractal.py`) — but issues none of
them from any authority yet: constructing one only proves it is
well-formed, never that a factor was actually born and frozen. See the
"G0.F" section of `docs/CONSTITUTION.md` for the full declared laws.

The encyclopedia (`src/alghanem/encyclopedia/`) is an application consumer of
the kernel, never a replacement for it. Its minimal state is
`EncyclopediaNucleusSnapshot = FractalSnapshot + GrowthFrontier`, where the
frontier holds only open questions: `RootInquiry` values, each requiring a
`BirthExperimentSpecificationContentBinding` so that question *generation* is
kept distinct from question *authorization* (a `QuestionProposal` carries no
experiment or execution field at all), and kernel
`ReopenExperimentSpecification` values, whose parents must exactly equal a
frozen factor or born bridge present in the paired `FractalSnapshot` —
identifier equality alone is refused. The nucleus deliberately has no domain,
ontology, claim, knowledge, article, or text field, and defines no growth
engine: `EncyclopediaGrowthTransition` remains the deferred boundary for
applying authorized kernel outcomes to a snapshot.

`src/alghanem/encyclopedia/self_observation/` applies that same discipline to
this repository itself, under
`System != RepositoryRepresentation != SelfModel != KnowledgeAboutSystem`. It
defines only the first link of
`RepositorySnapshot -> Evidence -> Claim -> EpistemicLicensing -> SelfKnowledge`:
address-only refs anchored to an explicit `commit_sha`/`tree_sha`/`blob_sha`
rather than a branch name, plus a `RepositoryObservationAuthority` that opens a
run and verifies repository→commit→tree and tree/path→blob before issuing
authenticated snapshots and artifacts. Authentication is not evidence
(`AuthenticatedObservationIsNotEvidence`), and content authentication holds
only within the provider's returned observations, never as universal
repository truth. `RepositoryArtifactChangeRef` records both sides of a change
so a delta is reconstructible, but `Change != Improvement`; and distinct commit
shas alone are not a historical transition — an `AuthenticatedRepositoryTransition`
needs two authenticated snapshots from one run plus a provider ancestry
witness. No `Claim`, `EvidenceBinding`, or `SelfKnowledge` runtime exists here;
that is a later `SelfKnowledgeBridgeExperiment`. See the "Encyclopedia Nucleus"
and "Encyclopedia Self-Observation" sections of `docs/CONSTITUTION.md`.

[`docs/AIMS.md`](docs/AIMS.md) (AIM.1) declares the programme's own aims, in
Arabic like the other programme/Arabic-layer documents, extracted from this
record rather than dictated from outside it: each aim names its question, what
would count as reaching it, what would not count even though it resembles it,
and its citation. Progress indicators are declared **epistemic and never
engineering**, with the reason named rather than left implicit: an engineering
indicator answers "does the code run?", while this programme's indicators
answer "is the judgment the code issues earned by its evidence?" — two
independent questions, since an empty function that always returns `PASS` can
carry full coverage and a green CI. `pytest`/`ruff`/`mypy` therefore remain a
CI requirement and are not an aim or an indicator of one. Aims that have not
started are kept distinct from aims blocked by a named obstacle
(`NamedObstacle != SilentAbsence`), the cross-project import loop (`A0.PP.3`)
is declared as an aim in its own right rather than left implicit, and two
foreign aims from that source project are recorded as declared only
(`DeclaredForeignAim != AlghanemRecord`). The boundary of that document is
unchanged: `DeclaredAim != LicensedProgramme`, `Aim != Achievement`,
`AimsDocument != Authority`.

Stage two of AIM.1 has begun in `alghanem.program.aims`, one milestone at a
time. `AimRecord` holds each aim's question, what would count as reaching it,
what would not count even though it resembles it, and its citation, across two
independent vocabularies — `AimEngagement` and `AttainmentStanding` — rather
than one ordinal scale, with every refused merge justified in writing as
`readiness_rank.py` does. `AttainmentStanding.REACHED` is declared but refused
at construction itself, like `QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT`: no
authority here issues an aim's attainment. Missing classification is a
vocabulary member (`UNCLASSIFIED_IN_RECORD`), never a blank that reads as
progress later, and the two foreign aims live in a separate `ForeignDeclaredAim`
type so that their exclusion from any later derivation is structural rather than
remembered. The module cites the open audit question
`DeclaredVersusDerivedRecurrenceNotExplained` as its direct design source, as §5
requires, and a test enforces that citation. The layer is authority-inert,
orders nothing by priority, and an automated scan asserts that no `kernel/`
module reads it.

The next milestone adds the two derivation readers §4 names, and only those:
`alghanem.program.constitution_ledger` derives, from `docs/CONSTITUTION.md`
itself, one `LawRow` per law-table row with its declared status, and one
`AuditQuestionRow` per open or resolved audit question with its lineage. Counts
are derived properties, never written fields, so no number can disagree with the
document. A status outside the closed `DeclaredLawStatus` vocabulary stops the
read with a named refusal instead of skipping the row, since a silently short
count reads later as a complete table; a missing section or an unreadable
document is likewise a named refusal rather than an empty ledger. An open
question whose status the record never declares carries
`NO_STATUS_DECLARED_IN_RECORD` rather than a blank. The reader binds to no aim:
it imports no `AimId` and no `AimRecord`, because joining a count to a
particular aim *is* the indicator, which remains deferred along with everything
§4 requires of it.

Selecting law tables by their `Law | Status` header was a validity condition,
but *non*-selection used to be silent: a law table whose header drifted by a
space, a case, or a neighbouring word would vanish from the count with no error
raised, because nothing *conflicted* — something was simply never counted. The
refusal rule therefore moved one layer up, from the cell to the table:
`DeclaredTableHeader` is a closed vocabulary extracted from the document, and
every pipe table is now either read, or excluded under a declared header, or
refused by name and line; a table without a delimiter row after its header is
refused too, instead of having one of its rows consumed as a header. A derived
`TableCensus` records each table found, so an excluded table is visible rather
than merely absent. What remains is named rather than hidden in
`NAMED_RESIDUALS`: `TABLE_HEADER_MATCH_COMPLETENESS_UNVERIFIED` (a law table
written under another declared header is still excluded without refusal) and
`NO_DECLARED_TOTAL_TO_CROSS_CHECK` (the document declares no total, so the
derived count rests on "no refusal fired", which is *no shortfall was detected*,
not *no shortfall exists*). Inventing a declared total in the document to close
that gap would be fabrication, not verification: §4's "a declared value that
contradicts the derived one is refused" presupposes a genuine declared value.

The third and last reader §4 names follows in
`alghanem.program.deferred_value_ledger`, and only it: the declared-but-unbuildable
values that still hold an aim open — `BIRTH_IN_SCOPE`, `MORPHO_FUNCTIONAL`, and
`CLOSED_BY_FROZEN_EXPERIMENT`. Its source is the `src/` tree rather than a
document: each member is imported live, so a rename is a named refusal rather
than a value silently read as released, and the holding module's own text is
parsed so the site and shape of the hold are derived rather than written.
Coding it showed that "unbuildable" is not one shape but three, and they are
kept apart in a three-valued `DeferredValueShape` instead of merged: a guard
that names the value and raises; a guard that never names it at all and merely
admits its only sibling in a two-valued vocabulary; and a value no guard refuses
at all, because its sole authority never writes it and so its derived codomain
never reaches it. Merging them would drop a live distinction — the first is
found by searching for the member's name, the second never is, and the third
raises nothing because no attempt is ever refused.

Each row carries both its declared shape and the shape derived from the code,
and a disagreement is refused at construction rather than recorded: the
`DeclaredVersusDerivedRecurrenceNotExplained` form finally doing real work,
where the previous reader had no declared total to compare against. The refusal
rule rises one more layer, from the table to the guard: every guard over a
tracked vocabulary lands in a derived `GuardCensus`, and a declared site with no
witness in its module's text halts the read by name instead of being skipped,
since a short ledger reads later as "this value is no longer held". What remains
is named rather than hidden: `REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY`
(nothing in the record obliges a hold to take one of the three observed shapes),
`SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE` (that hold is written
nowhere and follows from an allow-list over a two-valued vocabulary, whose size
is checked live), `CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY` (a codomain read
from literal writes means *no reaching write was found*, not *no execution
reaches it*), and `SECTION_4_NAMES_THREE_VALUES_ONLY` (other held values exist —
`AttainmentStanding.REACHED`, `BirthVerdictStatus.NO_BIRTH_IN_SCOPE` — and
widening §4's list is a judgment this milestone does not hold). This reader binds
to no aim either: it imports no `AimId`, no `AimRecord`, and no
`AttainmentStanding`, and the indicator remains deferred with everything §4
requires of it.

The fourth milestone follows in `alghanem.program.aims_document_ledger`, and only
it: the aims layer is finally subjected to the rule it had been imposing on
everything else. The three earlier readers checked declared against derived in the
constitution and in the `src/` tree, while the aim record itself remained a hand
copy of `docs/AIMS.md` prose that nothing checked — a layer exempting itself from
its own law. Coding it showed that the record's prose is a paraphrase rather than a
transcription: markup is dropped and citations are normalised, so comparing text
verbatim would have rejected the standing record outright or forced a shape onto
the document that the document never declared. What is derived instead is the
structure the document really does declare — aim identity and order, bullet labels,
the §3 classification, and the partial-attainment remainder — and the gap is named
rather than hidden (`RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION`).

The bullet vocabulary turned out to be six labels rather than the expected four,
because one aim carries two variant labels with a different separator: dropping
them would have silently dropped that aim from the read, and merging them into the
ordinary attainment label would have erased the very distinction from which the
record derives partial attainment. The field-presence laws of `AimRecord` — three
mandatory bullets, exactly one attainment bullet, a remainder if and only if the
attainment is partial — are now enforced against the document that is their source,
not only against the record copied from it. `AimRecordCorrespondence` carries no
pass/fail field at all: its construction *is* the correspondence, and disagreement
is a named refusal rather than a recorded verdict, since a result field would allow
a failed correspondence to be carried around and reported. Importing `AimId` here
is not the indicator, and the difference is structural rather than promised: the
indicator would bind a derived *count* to an aim, while this reader binds an aim to
its own source text, imports none of the three readers, and a test parses its
imports to enforce that. Transcription fidelity is not an aim's truth
(`TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH`): a false aim copied faithfully passes
this reader entirely, and `SECTION_3_CLASSIFIES_SIX_OF_THIRTEEN` records that the
document's silence about the other seven is now derived and enforced but still
silence. The indicator remains deferred with everything §4 requires of it.

The fifth milestone adds no fifth reader. It pays the debt the fourth one named
in its own closing lines: the audit-question bullet in
`alghanem.program.constitution_ledger` was the last known place where an
unexpected shape was skipped in silence, while the same rule had already been
raised to table headers, to guards, and to the aims document's bullets. Coding it
showed the skip was in three places, not one: a top-level bullet written in
another shape dropped its whole question from the count; a sub-bullet under an
unrecognised label was read as blank; and a label repeated inside one question
silently preferred its first occurrence. The second is the worst of them, because
a question whose status is written under an unknown label was read as
`NO_STATUS_DECLARED_IN_RECORD` — the *declared ignorance* that §4 insists upon
becoming a cover for a failed read.

Two closed vocabularies now carry that: `DeclaredQuestionBulletShape` (a name
alone, or a name followed by inline prose — both really occur, so accepting only
one would drop two questions, and accepting any dash would reopen the silent
skip), and `DeclaredQuestionBulletLabel`, whose eleven members hold the three
labels that are read into a row and the eight that are *declared excluded* rather
than passed over unmentioned, exactly as `DeclaredTableHeader` does. Every bullet
in both sections is now read, or excluded under a declared label, or refused by
name and line, and all of them land in a derived `QuestionBulletCensus` with no
written count; a sub-bullet appearing before any named question is a label with no
owner and is refused too. The repository document still reads as five open and
four resolved questions: the hardening corrected no number, it removed that
number's reliance on "no strange shape happened to appear". What remains is named
rather than hidden: `QUESTION_BULLET_LABEL_VOCABULARY_IS_NOT_DECLARED_IN_RECORD`
(the two vocabularies are extracted from today's text, and no constitutional row
obliges a question to take a shape from them) and
`EXCLUDED_QUESTION_BULLET_MAY_CARRY_A_DECLARED_STATUS` (exclusion is by label,
not by content, so a status written tomorrow under a declared-excluded label is
excluded without refusal). Tighter reading is not truth of what is read, and the
indicator remains deferred with everything §4 requires of it.

The sixth milestone is that indicator, in `alghanem.program.aim_indicator`. It is
the one thing the three readers were forbidden to do — bind a derived count to a
named aim — so it imports `AimId` and all three of them, and the boundary it keeps
is authority, not imports: no verdict, no freeze, no `E0`, and it neither imports
nor writes `AttainmentStanding` anywhere, which a test enforces by parsing the
module. The binding is derived, not written: a hand-written table of aim to
supporting rows would be exactly the written field §4 forbids, so the only source
is `AimRecord.citation`. The citation *declares* a support; the ledgers *derive*
whether that support exists, and a citation naming a row, a section, or a path
that does not exist is refused at construction rather than reported.

Coding it corrected the plan in several places, all recorded in §7 of
`docs/AIMS.md`. The parenthetical status in a citation describes *some* of its
supports and not all — `AIM-K1` cites one `ENFORCED` row and one
`DECLARED_DEFERRED` row and declares only the second — so the rule is that it must
match at least one, and matching none is refused. The per-aim standing is
homogeneity of declared statuses, not a split into "deferred" and "enforced": no
document declares that split, and inventing it here would be a judgement this
layer has no authority to make. Its ignorance member had to be renamed from "no
resolvable support" to "no status-bearing support", because `AIM-E2` cites a real
section and a real path, neither of which carries a status column. Indexing rows
by their first word raised a false duplicate on a healthy document, so the
identifier shape is declared explicitly, and `G0.BV.1` is matched whole so that it
cannot silently claim `G0.BV.1a` too. Reading the status parenthesis by a separate
scan read `P_0` out of `` `ExactFactorization(P_0) = OPEN` `` — stage two's
"reading a cell from the wrong position" returning one layer up — so the
parenthesis is only a status where no reference already covers it.

The refusal rule rises a fifth layer, from the bullet to the citation reference:
every position in a citation is a reference read under a declared shape, or a
declared connective, or a reference *declared unresolvable* and counted in
`CitationReferenceCensus` so that it is seen, or refused by aim and character
offset. Every count is a property over what was read; no type here has a count
field, and every vocabulary member appears in every census even at zero. What
stays open is named in code, not prose: the third of §4's readers is cited by no
aim at all (`THIRD_READER_IS_CITED_BY_NO_AIM`, a zero that is derived by scanning
for those value names, not assumed by dropping the reader); the binding runs one
way, so a row that *should* support an aim but is uncited is invisible here
(`CITATION_SUPPORT_IS_DECLARED_BY_THE_RECORD_NOT_BY_THE_CONSTITUTION`); and no
document declares how many supports an aim has, so the count rests on "no refusal
was raised" rather than on proof of completeness
(`NO_DECLARED_SUPPORT_TOTAL_TO_CROSS_CHECK`). Above all, a support count is not
progress (`SUPPORT_COUNT_IS_NOT_PROGRESS`): the ledger orders no aims, compares
none, derives no ratio or rank, and reaches none of them.

That milestone was coded twice, in two parallel branches neither of which saw the
other, and both landed. Merging them spliced one version's module docstring onto
the other's code, so neither the module nor its test could even be imported, and
§7 carried two sections of the same name. One version is now kept whole, and the
other is refused by name rather than erased: it called its vocabularies
`CitedTokenShape` and `CitedSourceGenus` and named residuals
(`CITATION_LINK_IS_NOT_ATTAINMENT`, `CITATION_PROSE_IS_NOT_A_TOKEN_STREAM`,
`LEDGER_COUNT_MOVEMENT_IS_NOT_AIM_MOVEMENT`) that no code reads today, so §7 of
[`docs/AIMS.md`](docs/AIMS.md) names them as open positions instead of folding
them away. Two independent codings of one milestone certify neither of them, and
each branch passed `pytest`, `ruff`, and `mypy --strict` on its own while their
merge did not import at all — a measured witness for §1's refusal of engineering
indicators as indicators of this programme's aims. What this restoration does not
close is named too: nothing derives that a §7 section corresponds to exactly one
module in the tree
(`MILESTONE_SECTION_TO_MODULE_CORRESPONDENCE_IS_NOT_DERIVED`).

The seventh milestone, in `alghanem.program.milestone_ledger`, pays that debt: the
correspondence between a §7 section and a module is now derived rather than read
by eye, and two sections for one milestone — precisely what happened and nothing
prevented — is refused at construction. The map is declared twice, in the
document's header sentence and again in each §7 section, and the reader
corresponds the two declarations without ranking either, because preferring one
would be the reader's choice and not the document's declaration. Existence in the
tree is then derived in both directions: every claimed module must be present, and
every module in the programme layer must be claimed by some milestone, since a
module that lands with no §7 section is code whose coding revealed nothing on
record, which §5 forbids.

Coding it corrected the plan again. The map is not one-to-one: the fifth milestone
created no module but reopened the second's `constitution_ledger.py`, so a binary
"claims / does not claim" would have had to either refuse the fifth or fold away
that it returned to an earlier module, and the standing is three-valued instead —
first claim, reopening, and no claim at all. The first milestone's section names
no module in its own body; its module is named in §7's preamble, so that is
accepted under an explicit `NAMED_IN_SECTION_PREAMBLE` mark rather than by a silent
skip. One module is named in two shapes — a bare filename for the fifth, full paths
elsewhere — and the shapes are kept apart because a bare name resolves only inside
the programme package. And not every §7 section is a milestone: the double-landing
record is an incident that names a milestone and claims no module, so reading it as
a milestone would have raised a false duplicate while dropping it from the census
would have hidden a section behind silence. What stays open is named in code:
existence is not authorship (`MODULE_EXISTENCE_IS_NOT_MODULE_AUTHORSHIP`), both
corresponded declarations are prose so their agreement on one error is invisible
here (`BOTH_DECLARATIONS_ARE_PROSE_NOT_TREE_DERIVED`), and why a module was
reopened is prose the ledger does not derive
(`REOPENING_IS_DERIVED_BUT_ITS_REASON_IS_NOT`). Reaching a seventh milestone is
not reaching an aim: this ledger brings no §2 aim closer and promotes none.

The eighth milestone, in `alghanem.program.dalala_indicator`, reads *how* a
citation reaches its support rather than how many supports it has. Its source was
a request to make *mantūq* (what the wording utters), *mafhūm* (what is understood
from it), and *ifāda* (benefit) into **performance indicators**; coding it found
that name refused by §1 of `docs/AIMS.md`, which separates "does the code work?"
from "is the verdict earned by its evidence?", so the refusal was recorded in the
document as a declaration and the indicator was built epistemically under §4
instead of smuggling performance in under another name. The three closed
vocabularies live once, in `alghanem.arabic.mantuq_mafhum_ifada`, and the
programme reader imports them rather than minting a second set with the same
words. The channel itself is derived by a second independent reading: the sixth
milestone records what a reference resolved to but not by which road, since the
declared name and the derived target read alike whether the citation named a
constitution row in full or reached it through an identifier that stands in for
the full name. So this reader builds its own index — names present verbatim are
uttered, names that only reach a support through something unsaid are understood
— and a reference the sixth milestone resolved but this index cannot reach is
refused by name, with neither reading outranking the other. A reference excluded
by declaration is uttered in the prose yet reaches nothing, so it carries no
channel at all (`UNRESOLVED_REFERENCE_HAS_NO_CHANNEL`) and is counted as
`غير_مُفيد`, which is the classical "it exists and does not benefit" case quoted
in `madlul_alone_formal.py`. What stays open is named: benefit here means reaching
a declared status, not linguistic benefit
(`IFADA_HERE_IS_READ_STATUS_NOT_LINGUISTIC_BENEFIT`); what is read is citation
prose, not a measured Arabic surface
(`CHANNEL_READS_THE_CITATION_NOT_THE_MEASURED_ARABIC_SURFACE`); the count of
`مخالفة` is zero today, derived by checking every understood reference rather than
assumed (`MUKHALAFA_IS_UNREAD_IN_TODAYS_TRACE`); and an uttered-support count is
not performance and not a distance to attainment
(`MANTUQ_COUNT_IS_NOT_PERFORMANCE`).

The ninth milestone added no module. It returned to the first milestone's
`alghanem.program.aims`, where refusing `AttainmentStanding.REACHED` carried a
note asserting that "no authority here issues attainment" — that is, it declared
one refusal genus, *held by a missing authority today*, over all thirteen aims at
once and derived it from nothing. Review proposed the opposite verdict: that
attainment is refused by a permanent category mismatch, since open-ended
discovery aims have no end for attainment to fall in. Coding found both answers
to be the same error in opposite directions. AIM-K4's attainment is an existence
condition on a named artefact — a freeze authority that issues `FrozenFactorRef`
— not an endless fractal level, so the aims are not one genus and no blanket
verdict over them is derived. The refusal genus is therefore split into a closed
vocabulary and derived per aim from its termination structure, after
`UnconstructibilityGenus` and `EvidenceTemporalStructure` in
`alghanem.arabic.transmission_standing`, cited rather than re-derived. The
derivation here is weaker than its sibling and the gap is named: there synchrony
was provable by re-deriving a closure digest, while here neither side is provable
today, so every aim reads `GENUS_NOT_SETTLED`
(`NO_TERMINATION_PROOF_EXISTS_TODAY_NOTE`) — an honest weakening of a claim that
was stronger than its evidence, not a retreat, and not a midpoint between the two
genera (`NOT_SETTLED_IS_NOT_A_MIDPOINT_NOTE`). Behaviour is unchanged: `REACHED`
is still refused at construction. Proof sites are named though none exists, so
the remainder is named rather than silent, and a descriptor carrying a proof no
authority issued is refused at construction. The claim that every birth opens a
higher fractal level is recorded and deliberately not coded as a derivor, because
no constitution row supports it and coding it would make it an unverified premise
the whole division succeeds on
(`FRACTAL_OPEN_ENDEDNESS_IS_AN_UNSOURCED_CLAIM_NOTE`).

The tenth §7 milestone added no module either. It returned to
`alghanem.program.deferred_value_ledger` to answer the question its ninth
predecessor wrote down and left pending: does "absent from the read trace" need
splitting between *not searched for in this source* and *searched and not
found*? The question was decided on the trace of that ledger itself rather than
on prose, and the answer is that absence is not one category and not two but
three. A value whose hold is already established by a naming guard or by a
sibling guard was never searched for at all; a value searched for over a text
every one of whose references is a readable form is genuinely not found; and a
value searched for over a text holding even one reference the reader cannot
classify is not-found without exhaustion, so the third member
`SEARCHED_OVER_UNREAD_FORMS` exists and is counted at zero rather than folded
away. Because the two searched genera differ only in the scope actually read,
whoever declares one is now required to carry that scope — the closed
`ReferenceForm` vocabulary it covered and the document lines it could not read —
and a descriptor declaring a search with no read scope, or an exhaustion over a
line it admits it could not read, is refused at construction. The reference
census that makes this derivable also corrected a claim the module would
otherwise have made: `BirthVerdictStatus.BIRTH_IN_SCOPE` *is* written in
`alghanem.kernel.birth_verdict`, as an operand of a comparison, so the honest
statement is that it is mentioned and never constructed, not that it is never
written (`members_mentioned_without_construction`). Nothing was promoted:
`AttainmentStanding.REACHED` is still refused at construction and no aim moved.
What was not lifted is named — a declared search scope is readable in the tree
and not proved about the world (`SEARCH_SCOPE_IS_DECLARED_NOT_PROVEN`), the form
vocabulary is a reader's four positions and not a law about Python
(`FORM_VOCABULARY_IS_READ_NOT_LAWFUL`), and the third genus has no occupant in
today's trace, which is a fact about today and not a proof that it cannot occur
(`SEARCHED_OVER_UNREAD_FORMS_IS_UNOCCUPIED_TODAY`).

The tenth milestone answered one question and refused to leave it pending.
Three independent cards — قُروء (2:228), أنّى (2:223), and مَلِك (114:2) —
had stopped at exactly the same place, the fourth link (الوضع بالنقل), because
none of them declares how the meaning it cites *reached* it. Whether that stop
was a permanent category error or a temporary gap was decided by applying the
method already tested in `transmission_standing` to a new source — the lexicon
rather than a corpus — instead of building a fourth card in the hope that the
barrier would lift by itself. `src/alghanem/arabic/lexical_transmission.py`
adds `LexicalTransmissionDescriptor`, built exactly like
`EvidenceBaseDescriptor`: a claim about structure whose digest is re-derived
from the enumeration itself and refused at construction when it disagrees. The
hypothesis under test was that لسان العرب is not genuinely synchronic — Ibn
Manẓūr compiled it from successive lexicographers named inside his own text —
so a card that transcribes that internal attribution chain would carry a
structure the closed-corpus argument never covered. The derivation is
asymmetric like its sibling: a flat title citation is *proved* by re-deriving
the digest of an empty chain, a named successive attribution is *proved* by
re-deriving the digest of an ordered enumeration of two or more attributions
each quoting its own authority verbatim, and a card that declares no lexical
path at all reads `بنية_الاستشهاد_غير_محسومة` rather than being carried onto
either side. Order is load-bearing here and members are therefore not sorted
before digesting (`ORDER_IS_LOAD_BEARING_NOTE`), and an empty enumeration is
accepted here though refused there, because the claim it carries is the
*absence* of a transcribed chain rather than closure
(`EMPTY_CHAIN_IS_A_CLAIM_NOT_A_CLOSURE_NOTE`). The test ran, and the answer is
the negative one: all three cards declare a flat title citation, so the genus
is `REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH` and the tawatur question is
ill-posed on that structure — named as
`FlatTitleCitationIsNotATransmissionChain`, a permanent category error of the
same kind as `TawaturRequiresDiachronicSuccession`, not a hold waiting for a
tool. The fourth link therefore still stops, but the stop is now derived and
explained rather than pending, and `decision_chain`'s constraint (ب) says so.
Even in the positive branch recurrence would stay out of reach: an internal
attribution is containment inside one compiler's text, not a proof of source
independence, so `SourceIndependence.NOT_ESTABLISHED` is structural on this
path and the derived degree is `آحاد` or `فرض` and never `متواتر`
(`INTERNAL_ATTRIBUTION_IS_NOT_SOURCE_INDEPENDENCE_NOTE`,
`MUTAWATIR_HAS_NO_ENTRY_ON_THIS_PATH_NOTE`). `wad_naql` is untouched: a derived
degree is handed to it through a thin `LexicalWadPath` and recorded as an
ordinary `WadRecord`. What was not lifted is named: no لسان العرب text is
vendored here, so attributions remain declared by the caller — now as a
byte-checkable structural claim rather than a passed title
(`LISAN_TEXT_IS_NOT_VENDORED_HERE`) — and whether the compiler is itself a
frozen synchronic section is a question this module neither decides nor needs
(`COMPILER_SYNCHRONY_IS_NOT_DECIDED_HERE`).

The eleventh milestone asks whether the fourth link is a fact about single
words or about a shape that recurs one level up, and it isolates that single
variable rather than testing it on material that already carries another one.
Every level-one card standing today (قُروء, أنّى, مَلِك, عسعس) is lexically
مُجمَل, so a stop above it could always be read two ways: the composition
mechanism failed, or level-one ambiguity leaked upward. «الغنم السائمة» has
neither term in dispute, so any stop is attributable to the mechanism alone.
`src/alghanem/arabic/level_two_manat.py` builds `TaqyeedManatGate`, the link
parallel to link four but asked of the *constraint* rather than of a word: does
a transmission path exist for this qualifier specifically — not for الغنم and
not for السائمة separately — establishing that it is مُخصِّص (producing مفهوم
المخالفة) rather than a وصف طردي? Level-one inputs are read from their actual
issued closure through `ClosedLevelOneCard`, which accepts only a gate-issued
`EvidenceApplicabilityAssessment` bound to that card's own scope and refuses
re-analysing raw text (`LEVEL_ONE_CLOSURE_IS_READ_NOT_REPEATED_NOTE`).
`CompositionGenus` is derived from the relation declared in a named source and
refused when a written field disagrees. The order of reading was fixed in
advance and kept: the synthetic `test_only` control in
`tests/arabic/test_level_two_manat_negative_control.py` proves the link *stands*
when the constraint's path stands and stops when a single attribution is
removed, and only then were the real cards read. They stop —
`وقوف_آلة_لانقطاع_نقل_القيد`, flat-title structure,
`REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH` — and the stop is recorded as issued,
not engineered away. Three things this unit does not establish are named rather
than implied: it is not the frozen `TADMIN_TAQYID` certificate and does not
widen that stage's frozen outcome vocabulary
(`LEVEL_TWO_LINK_IS_NOT_THE_TADMIN_TAQYID_CERTIFICATE_NOTE`,
`COMPOSITION_GENUS_IS_NOT_A_FROZEN_STAGE_OUTCOME_NOTE`), it issues no fractal
(Φ) verdict about its own resemblance to link four, because a unit that judged
its own parallel would be both litigant and judge
(`FRACTAL_VERDICT_IS_NOT_ISSUED_HERE_NOTE`), and it decides no fiqh question
about zakāt. An input stop (genus undecided) is kept in a different member from
a mechanism stop so the two variables do not merge again by the back door
(`INPUT_STOP_IS_NOT_A_MECHANISM_FAILURE_NOTE`). The hadith is a new witness, not
a previously coded example, and its cards live in `examples/level_two_manat/`
rather than among the Quranic audit cards; no member of `BayanKind` was added
for it (`NEW_WITNESS_IS_NOT_AN_ESTABLISHED_EXAMPLE_NOTE`,
`HADITH_SOURCE_DOES_NOT_WIDEN_THE_BAYAN_VOCABULARY_NOTE`).

The twelfth milestone asks what that stop is worth, and the first finding is
about the tool, not the text. `derive_lexical_citation_structure` treats a
citation as a chain only at or above a threshold now named
`LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS` (two), so a citation carrying **one
genuinely transmitted attribution** derives the same flat-title structure, and
therefore the same `REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH`, as a card that
transmitted nothing at all. The level-two stop was consequently not falsifiable
by a single real attribution: a structurally unreadable negative, the same shape
as the earlier demand for `متواتر` by name that made link four permanently
impossible rather than contingently stopped. That recurrence is now named as a
pattern with a prospective question for every future gate — *which real input
falsifies this stop?* — in
`STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE`.
`src/alghanem/arabic/level_two_discrimination.py` freezes, before any text is
transmitted, the single variable the discriminating experiment may move (the
`الإسنادات` enumeration of the «سائمة الغنم» composition card and nothing else),
what stays fixed, and what each of the six named branches licenses and refuses.
`StopDataStanding` separates "nothing transmitted" from "one below the
threshold" from "a chain at or above it", and `stop_match_genus` reads several
stops together: identical genera count as `تطابق_رواية` while any side is still
empty, as `تطابق_غير_محسوم` while any side sits at one attribution, and only as
`تطابق_دراية_مرشح` when every side is a real chain. Read across the four
level-one cards and the composition card, the match is `تطابق_رواية`, and no
fractal claim may rest on it (`IDENTICAL_STOP_GENUS_IS_NOT_FRACTAL_EVIDENCE_NOTE`,
`ARITY_IS_NOT_A_LINGUISTIC_STRUCTURE_NOTE`). The same milestone stops the tool
from crashing on the most common real case it will meet: a path transmitting
both a specification and a طردي reading is now read as a named case,
`QaydSignification.دلالة_القيد_متعارضة` with its own stop genus, instead of
raising (`TRANSMITTED_CONFLICT_IS_A_CASE_NOT_A_CRASH_NOTE`). The source text was
first sought and not obtained — the primary مَتْن was unreachable and only
paraphrasing secondary summaries came back, refused under
`SecondaryParaphraseIsNotAVerbatimExcerpt` for inability to match the text
letter-for-letter, not for any weakness of the source — and was then supplied
whole from outside this tree, so **the experiment has now actually been run for
the first time on transmitted text**. Three things fell, none of them the thing
predicted. First, the passage names exactly **one** authority inside itself
(«الزين بن المنير»); Ibn Hajar is the compiler of the containing work and does
not occur in it by name, so he stays in `المصدر`, and manufacturing a second
attribution to reach the arity threshold would write words the text does not
contain. Second, that single genuine attribution lands precisely on the arity
artifact named above: the composition card derives the same
`REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH` and the same
`وقوف_آلة_لانقطاع_نقل_القيد` as it did while transmitting nothing, and only the
discrimination branch moves, from `لم_يُزوَّد_بإسناد_بعد` to
`وقف_بإسناد_واحد_منقول`. The prospective question *which real input falsifies
this stop?* therefore has its first real answer, and the answer is that this one
does not. Third, the predicted `دلالة_القيد_متعارضة` did **not** occur:
`derive_qayd_signification` returned `دلالة_القيد_غير_محسومة`, because Ibn Hajar
writes «مفهوم الصفة» and «اعتبرت / لم يعتبر» while the frozen marker vocabularies
carry «مفهوم المخالفة», «أخرج» and «لا زكاة». Neither vocabulary was widened to
make the prediction come true; doing so after reading this particular text is
exactly what `MarkerVocabularyIsFrozenBeforeItsText` forbids, and if «مفهوم
الصفة» deserves membership that decision must be registered away from this case
and applied to it afterwards as a result rather than as a cause. The locus
residual is raised only in part and is recorded as such
(`PRINT_EDITION_LOCUS_NOT_VERIFIED`): the bracketed «[ص: 372]» is cross-edition
reference pagination rather than one site's page number, but the volume is
unstated and no critical print edition was collated by hand — and that gap
touches documentation only, since the marker scan reads the excerpt alone. No
fiqh question and no fractal (Φ) verdict is decided here either. One further open variable observed while freezing that
preregistration — whether `طريق_النقل_المعجمي` is a third path read in its own
right or a dependent of the constraint's path — is entered in
`qayd_marker_preregistration.NAMED_RESIDUALS` as
`LEXICAL_PATH_FRONT_IS_REGISTERED_NOT_OPENED`, and nothing more: no tool, no
vocabulary member, and no run against it until the «سائمة الغنم» experiment
closes with one complete result. Registering a front is a ledger entry, not a
licence to work it; that is this repository's own sequential law
`NoRicherStructureBeforeLowerOpenResidualClosure` applied one level down, and
the refusal is named `OpenFrontIsRegisteredNotOpened`. Its observation date is
the commit that added the residual, read from commit metadata rather than
written into the text as an unverifiable field.

The next preregistration freezes a *sentence* card, and the first thing it
establishes is a boundary rather than a reading. The four standing formal
certificates all classify a **lexeme or a cluster of lexemes**; a sentence is a
new unit of analysis, and reading the new card as a silent widening of those
certificates would merge two genera under one name
(`SentenceIsNotALexeme`).
`src/alghanem/arabic/sentence_card_preregistration.py` therefore registers
nineteen card items before their answers, in the shape of
`compound_layer_preregistration.py`: one frozen reference per item from a
closed three-member vocabulary (`OneFrozenReferencePerItem`), a three-valued
standing with no member named "done", a derived prerequisite cone that refuses
any written cone that differs from it, a named refusal on every item, and no
result field at all under an import-time guard. Seven items are derived from
certificates already in the tree, **two are deferred by their own law** — they
are the first and the second-plus-third stages of
`compound_layer_preregistration` themselves, not look-alikes, and issuing them
as a certificate here would silently retire that registration
(`CompoundStageIsDeferredNotReopened`) — and **ten await a source text that is
not transmitted in this tree**: six of them wait on books of which not one
letter is carried here — no «النحو الواضح» and no (ن و ر) entry from «لسان
العرب» — and four on loci of الشخصية الإسلامية ج٣ that no critical print
edition in hand was collated against. An unanswerable
item is recorded as a named standing rather than an empty cell, because an
incomplete card is the result and not a defect
(`IncompleteCardIsTheResultNotADefect`).

Running it once, on «اللهُ نورُ السماواتِ والأرضِ» (النور:٣٥), produced two
findings that were not predicted. First, **five items are read, not seven**:
`منطوق_مفهوم` stops although its own module is coded, because its derived
prerequisite — the مطابقة/تضمّن/التزام item — awaits a text, and attainment is
derived by succession exactly as in `decision_chain`. Coding a unit is
therefore not reaching it. Second, the card's `كلّي` derivation for «نور»
returns `كلّي_مشكِّك`, while the request that commissioned the card read it
`كلّي_متواطئ`; the transmitted excerpt frozen in `kulli_juzi_formal` names
النور among the مشكِّك examples («مثل الوجود والنور»). Neither the vocabulary
nor the attested witness was edited to make the commissioned reading come out,
and the divergence is recorded as a named residual rather than resolved, since
only «الوجود» is an attested witness in that module. The `الإفادة` item stops
too, and stops for a stated reason: its prerequisite is one of the deferred
compound-layer items, so `غير_مقروء` is not read as `غير_مُفيد`. The
prediction that «في بيوتٍ» will derive `غير_مُفيد` when isolated from its
متعلَّق is frozen in `NAMED_RESIDUALS` **before** it is run, together with the
input that would falsify it, and the second and third sentences are named there
as fronts registered and not opened. The card's own placement against the open
«سائمة الغنم» front is argued in the module rather than assumed: it consumes no
output of that experiment and is consumed by none, its derivable items reuse
certificates frozen before both, and its only richer items are the deferred
ones, so it is read as `∥` and not as a blocked front
(`ParallelFrontIsNotABlockedFront`). No birth, no verdict, no freeze, no `E0`,
no kernel gate reads any of it, and no fractal (Φ) claim is made from one card
fitting three sentence genera (`OneCardOnThreeSentencesIsNotFractality`). The
first application lives in `examples/sentence_card/nur_24_35.yaml` plus a
single traversal in `tests/arabic/test_sentence_card_nur_24_35.py`, not in a
production module, because the card has not yet proved its worth on one
complete sentence.

Four of the card's ten items awaiting a source text have since been **supplied
with one, and the search behind two of them was actually run rather than
assumed**. The material «ن و ر» of *Lisān al-ʿArab* was located inside the
OpenITI corpus at
`OpenITI/RELEASE:data/0711IbnManzurIfriqi/0711IbnManzurIfriqi.LisanCarab/…Shamela0001687-ara1.mARkdown`,
whose own header declares the print edition it paginates (Dār Ṣādir, 3rd ed.
1414 AH, 15 vols.) and whose embedded `PageV05P240…P245` markers bound the
material to volume 5. Two short attributed lines were transcribed from it — one
to Thaʿlab on the pattern «مفعلة», one to al-Jawharī on the derivation of
«مناور» — raising `الوزن` and `الاشتقاق والصرف`; two passages from the third
volume of *al-Shakhṣiyya al-Islāmiyya* were transcribed for
`مطابقة/تضمن/التزام` and `خبري/إنشائي`. That forced a structural decision
rather than a cosmetic one: a supplied text is neither a waiting item, nor a
formal certificate, nor a deferred one, so `ItemStanding` gained a named fourth
member, `نصٌّ_مُزوَّدٌ_بلا_شهادة_صورية`, and the traversal now stops those items
by that genus instead of reporting «مصدر غير مُقدَّم» for a source that was in
fact supplied (`SuppliedTextIsNotAFormalCertificate`). Locus verification gained
its own three-ranked vocabulary in
`src/alghanem/arabic/sentence_card_source_texts.py`, whose **middle** rank is
the point: digitally encoded pagination of a *named print edition*, uncollated
by hand (`DIGITALLY_ENCODED_PRINT_PAGINATION_UNCOLLATED`), ranks above a source
that names no edition at all and below hand collation — and the top member
`مقابل_بنسخة_ورقية_محققة` deliberately has **no entry today**. Only short
attributed excerpts were transcribed, never the tagged material wholesale:
Ibn Manẓūr's متن is public domain while the digital tagging effort is not
(`PublicDomainMatnIsNotAnOpenLicence`). What did **not** fall is recorded with
the same care as what did. Scanning the whole material returned zero
occurrences of «مشتق» or «اشتقاق» and no signifier-alone analysis, so
`جامد/مشتق` and `الدال وحده` stop *after* reading the source rather than before
it; «المقام» has no operational definition anywhere in the declared volume, so
it stops by a different genus altogether
(`TERM_NOT_LOCATED_IN_DECLARED_SOURCE`) and its frozen reference was **not**
swapped after seeing that result; *al-Naḥw al-Wāḍiḥ* and *al-Muʿjam al-Wasīṭ*
are modern copyrighted works whose absence is a permanent legal refusal, not a
research gap (`MODERN_COPYRIGHTED_SOURCE_NOT_DIGITIZED_OPENLY`); and every
«line number» quoted from the `.docx` extraction is marked non-citable until
collated against a named print edition
(`EXTRACTED_LINE_NUMBERS_ARE_NOT_PRINT_PAGINATION`). One unprompted finding came
out of the traversal: `الاشتقاق والصرف` still stops, although its own text is
now supplied, because its derived prerequisite `الوزن` has not been reached —
the sequential law again, one level down. The card's `طريق_النقل_المعجمي` now
carries four internally named attributions (Ibn al-Athīr, Abū Manṣūr, Thaʿlab,
al-Jawharī) and therefore derives `إسناد_داخلي_متعاقب_مسمى` rather than
`عنوان_واحد_مسطح` — the first real entry on that path — while source
independence remains `NOT_ESTABLISHED` structurally, since all of it is
transmitted inside one compiler's text. That the material opens by citing the
card's own verse («قال الله عز وجل: الله نور السماوات والأرض») is recorded as a
textual coincidence in the test, not read as an argument for anything.

A second witness to the same material then arrived from a *fourth* book —
the «ن و ر» entry of Ibn Fāris's *Maqāyīs al-Lugha* — and the first thing it
forced was a genus decision rather than a filling-in. The card's reference
vocabulary is a closed three-member set with exactly one reference per item
(`OneFrozenReferencePerItem`), so a text from outside it has only two ways in:
swapping an item's declared reference **after** seeing what the new text says,
which is precisely what was refused for «المقام»; or adding a second reference
to an item, which reopens source-selection after the answer and voids the
preregistration at its root. Neither was taken. The entry is transcribed
verbatim in `sentence_card_source_texts.py` as a **corroborating** text
(`CorroboratingSourceText`), a genus that names the items it corroborates
rather than an item it supplies, carries no reference field at all, and is
required by its own constructor to declare the boundary
`CORROBORATION_IS_NOT_A_DECLARED_REFERENCE` among its residuals. **No item's
standing or reference changed**, and a test asserts that. Its locus is
`موضع_غير_متحقق` and not the middle rank: an "entry number" is a finding-list
index, not the pagination of a named print edition, and no edition, editor, or
digital witness was named (`ENTRY_NUMBER_IS_NOT_PRINT_PAGINATION`,
`PRINT_EDITION_NOT_NAMED`). Two findings are recorded rather than smoothed. The
wazn witness it carries — «والمنارة: مفعلة من الاستنارة، والأصل منورة» — is a
morphological analysis of the *same derivative* «منارة» that the Thaʿlab line
already gave, not of the card word «نور», so the standing residual
`WaznOfADerivativeIsNotTheWaznOfTheCardWord` survives the corroboration instead
of being retired by it. And the entry's «سُمِّيا بذلك من طريقة الإضاءة» is a
lexicographer's account of *why the thing was so named*, referring the branches
of a root to one shared semantic measure; the card's question is whether the
word «نور» is itself morphologically جامد or مشتق. Those are two genera, and
reading the first as an answer to the second is the same category error the
tree refuses elsewhere, so `جامد/مشتق` **remains** `ينتظر_نصًّا_مصدريًّا` under
a named refusal, `ETYMOLOGICAL_DERIVATION_IS_NOT_MORPHOLOGICAL_JUMUD_MUSHTAQ_STATUS`,
with the reason now being a text that was read rather than a text not found.

The compound layer received its own first supplied text next, and it needed a
separate module rather than a widening of the card's vocabulary. A compound
*stage* is not a card *item* (`CompoundStageIsNotACardItem`): the card draws
from a frozen three-member reference set, while Ibn ʿAqīl's *Sharḥ* and Ibn
Hishām's *Mughnī al-Labīb* are not members of it at all, so pushing them in
there would be exactly the widening-after-the-text that
`MarkerVocabularyIsFrozenBeforeItsText` forbids.
`src/alghanem/arabic/compound_layer_source_texts.py` therefore opens its own
two-member vocabulary and records the uncomfortable fact that it was opened
**after** its text was seen rather than before
(`REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_WAS_SEEN`, required in every entry
by the constructor); that inversion was tolerated only because the module holds
no outcome vocabulary and no decision function that could be cut to fit the
text, and because the stage vocabularies themselves were not touched. Both
excerpts earn the **middle** locus rank honestly: their OpenITI witnesses carry
`PageV..P..` markers referring to named print editions — Dār al-Turāth, ed.
Muḥammad Muḥyī al-Dīn ʿAbd al-Ḥamīd for Ibn ʿAqīl; Dār al-Fikr Damascus 1985,
ed. Māzin al-Mubārak and Muḥammad ʿAlī Ḥamd Allāh for the *Mughnī* — which is
print pagination, not a website's own page division, though nothing was
collated against paper. The two editorial teams are **different**, so no
"single-editor continuity" argument spans the two sources, and a test asserts
that. The decisive residual is the one that would have been easiest to omit:
`TERM_IS_USED_NOT_DEFINED_IN_THE_SUPPLIED_TEXT`. Both works *use* عامل and
معمول inside a particular problem and presuppose the definition; neither states
it, and neither divides the word exhaustively into those branches. So supplying
them lifted the missing-transcription deficit for the first stage only, moving
it alone to `مصدر_مُقدَّم_غير_متحقَّق` while the other three stay at
`مصدر_غير_مُقدَّم`. `شاهد_لكل_فرع` remains declared-but-unconstructible,
`certificate_is_constructible` is still `False`, the first stage's outcome
vocabulary and refusals are unchanged, and the card's own `العامل_والمعمول`
item keeps both its standing and its declared reference, because
`CompoundStageIsDeferredNotReopened` requires the deferral to be lifted in the
stage's own place. A derived `standing_refusal_statement` now names which of
the two genera blocks each stage: absence of a text, which a source lifts, or
absence of any authority to verify branch-to-text attestation, which no number
of further texts lifts.

A fifth supplied section then arrived with five pieces of material at once, and
the first thing it forced was a distinction the repository had not needed until
now: **transcription versus description**.
`src/alghanem/arabic/usul_section_source_texts.py` sorts what was supplied by
the *genus of its supply* rather than by its subject
(`SectionMaterialStanding`). Three pieces arrived inside quotation marks and are
held as `SectionExcerpt`, checked by containment like every other transcription
in this layer. Four arrived as *descriptions of an argument or an example* with
no words of their source attached, and are held as `DescribedSectionMaterial`,
which carries **no `verbatim_text` field at all** so that no containment check
can ever be run against it and read a paraphrase as its source's own wording —
the same line `CASCADE_WORDING_IS_NOT_TRANSCRIBED` draws elsewhere, enforced
here by the absence of the field rather than by a note. Every entry of both
kinds is required by its constructor to declare
`SECTION_SOURCE_BOOK_IS_NOT_NAMED`, and the excerpt constructor **refuses** any
locus above `موضع_غير_متحقق`: no title, author, death-year, volume, page,
edition, or digital witness was given for this section, so the middle rank is
not merely unclaimed but unreachable.

What this repaired is narrower than it first looked. The priority ladder of the
five comprehension defects — `تخصيص > مجاز = إضمار > نقل > اشتراك` — was already
in `comprehension_defect.py` with ten pairwise arguments, so nothing was
*filled*. What the ten arguments lacked was transcription: they are this
module's own wording argued to named books with no locus inside them. The new
excerpt supplies the actual words of exactly **one** of the ten comparisons
(«النقل أولى من الاشتراك؛ لأن المنقول مدلوله بمعنى واحد... بخلاف المشترك
فمدلوله متعدد»), and a test walks all ten verdicts against the excerpt to assert
that only that one is attested. The gap is therefore recorded, not closed, by
`PRIORITY_LADDER_ARGUMENTS_ARE_PARAPHRASE_NOT_TRANSCRIPTION`. The ladder
notation `الاشتراك < النقل < …` is the requester's, not the source's, and says
so in a residual. The dawr proof for classifying «طلقتك» as إنشاء, and the
examples الحج / الطهور / الفرض‑الواجب, arrived as descriptions only, so
`CardItem.KHABAR_INSHA` keeps its standing untouched and the sevenfold and
kullī decision domains keep their attested witnesses, each asserted by a test.

`src/alghanem/arabic/tawlid_lafzi.py` holds the sharpest claim in that section
and is deliberately kept as a separate, declared-but-unactivated module. Three
generation tools each own exactly one domain — تعريب for things and proper
names, اشتقاق for meanings, مجاز for imagery — so an operation is classified by
the *kind of its content* before any tool is judged, and mixing them is the
named error the source condemned. The verdict itself turns on a single binary:
was the foreign **word** taken and shaped to an Arabic pattern (Arabic by
correct تعريب), or was only its **meaning** taken and dressed in a word from an
unrelated Arabic root (outside the language entirely)? `غير_محسوم` is a declared
member on both the mode and the standing vocabularies, so a lexeme whose
generation was never established is never pushed to either side. Two boundaries
are written into the module because both were easy to cross silently.
`OutsideTheLanguageIsNotADistributionalOutlier` refuses any reading of this
verdict as rarity or as a `distributional_probe_report` result: it is a textual
judgement about how a word was made, and usage counts neither establish nor
rebut it. `HaqiqaGeneraExhaustionIsQuotedNotDerived` refuses the tempting move
of completing the source's negation from `HaqiqaGenus`; the source itself named
لغوية, شرعية, and عرفية, and an import-time guard only *checks* that all three
appear in the quoted letters — coverage verification, not derivation. The five
lexemes the source judged (هاتف، سيارة، قطار، عربة، مقود) are held as cited
witnesses whose standing is a derived property with no field behind it, and they
are explicitly **not** rows of `ImportedFeatureVocabulary`, which is frozen at
its foreign source with an expected row count that a sixth row would invalidate.
Neither module is read by any gate, changes any item's standing, or opens a
member in any frozen vocabulary.

The five governing sections of *uṣūl al-dalāla* now have a ceiling of their own
in `usul_dalala_sections.py`, written before the modules it measures so that it
is a standard rather than a description of what happened to be built. Its five
members are closed, and `attribute_proposal` returns `مردود` for any proposal
attributed to no section — silence is refusal, never quiet admission. The
rejection of «الظاهر والمؤوَّل» is recorded there as a named precedent with its
ground. Coverage is not written in a table but read from the tree by
`read_sections`, so الناسخ والمنسوخ reads `غير_مُرمَّز` for exactly one reason:
no module answers to it, because no ج٣ wording for it has been extracted. That
absence is carried as `NASKH_TEXT_NOT_EXTRACTED_RESIDUAL` rather than filled by
a vocabulary built ahead of its text.

`dalalat_thalath.py` encodes مطابقة، تضمّن، التزام as an *independent* closed
vocabulary, not as a widening of the frozen binary `DalalaChannel`, which
`ThreeDalalatAreNotTheDalalaChannelPair` already refuses by name. A one-way
derivation maps مطابقة and تضمّن to منطوق and التزام to مفهوم;
`dalalat_of_channel` returns every match and chooses none, since منطوق answers
to two dalālāt and picking one would be preference without a preferrer. The
condition «اللزومُ شرطٌ وليس بموجِب» is recorded as a named refusal, not as a
logical entailment flag. This module is the only one of the five bound to a text
actually transcribed in the repository.

`mutlaq_muqayyad.py` makes carrying conditional on *both* unities at once — of
the ruling and of its cause — and registers the ẓihār / accidental-killing pair
as a witness of **non**-carrying: the ruling is the same عتق رقبة in both, yet
the causes differ, so the قيد does not travel. A non-carrying witness is the
sharper one, because a carrying witness satisfies both conditions together and
so cannot show that either alone is insufficient. `DalilScope` and
`TAKHSIS_IS_NOT_IHMAL_NOTE` are imported from `umum_khusus`, never copied, and a
guard asserts the two standings vocabularies stay distinct.

Inside `lafz_madlul_relation_formal.py`, the carrying cascade — شرعية، then
عرفية، then لغوية، then مجاز «صوناً للكلام عن الإهمال» — is added as a derived
ordering, `haml_cascade`, under exactly the rule already applied to «الترادف
خلاف الأصل»: declared, not activated. Neither `classify_relation` nor
`prove_relations_over_attested_corpus` reads it, the frozen domain stays at
seven states, and a guard refuses any ḥaqīqa genus that appears in the closure
attestation, since `HaqiqaGenus` is the genus carried onto and
`LafzMadlulRelation.HAQIQA` is a division of the relation itself.

Four of these five rest on wording supplied in a request rather than
transcribed from ج٣. Each therefore names its own gap —
`SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED`, `MUTLAQ_WORDING_NOT_TRANSCRIBED`,
`CASCADE_WORDING_IS_NOT_TRANSCRIBED` — and each module declares itself a
registration, not a certificate. None of them holds authority: no birth, no
`E0`, no read from `kernel/`.

The «سائمة الغنم» front, open since it was registered, is now **closed by a
negative result rather than lifted by one**. The composition card stopped at
`وقوف_آلة_لانقطاع_نقل_القيد` with `REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH`, and
the reason was an arity artifact: the chain threshold is two attributions and the
card transmits one. What that stop left genuinely open was *which* kind of
deficit it recorded — an incomplete transcription that a fuller reading would
lift, or a source that simply contains no second attribution. The question was
answered by running it. `src/alghanem/arabic/level_two_source_texts.py` freezes a
scan of **the whole of** *Fatḥ al-Bārī* — not its book of zakāt, and not its
chapter on زكاة الغنم — in the OpenITI witness of a named print edition (Dār
al-Maʿrifa, Beirut, 1379 AH, 13 vols.), identified by file digest and byte length
because the corpus is not vendored here. The two frozen tokens «سائمة» and
«السوم» occur thirty-three times; three of those co-occur with an attribution
formula; exactly **one** lies in the material of the قيد. The other two are named
individually with the ground of their exclusion rather than absorbed into a
count: Mujāhid glosses «المسومة» outside the zakāt verse, and Abū ʿUbayda derives
«مسومة» in Āl ʿImrān — sharing a root is not sharing a question. So the stop is
**final for this source**, and no transcription effort lifts it.

Three things are recorded that it would have been easier to leave out. First,
nothing was promoted: the stop genus, the unconstructibility genus, the flat-title
citation structure and `دلالة_القيد_غير_محسومة` are all unchanged, and
`EXHAUSTION_DOES_NOT_CHANGE_THE_STOP_GENUS` says so, because reading an
exhaustion as a promotion reads a negative result as a positive one. Second, the
excerpt the card transmitted «from outside this tree» was collated against this
independent witness and **matched letter for letter** — the first external
confirmation of a transcribed excerpt in this repository — but the match is on
bare letters, since the digital witness carries no vocalisation or punctuation to
compare, and the residual names that limit instead of claiming the orthography
was collated. Third, the locus was raised only in part and the disagreement was
not smoothed: the volume is settled at three by the `PageV03P317` and
`PageV03P318` milestones that bracket the passage, but whether a milestone closes
its page or opens it was not verified, so the page is left standing between 317
and 318 (`PAGE_MILESTONE_CONVENTION_NOT_VERIFIED`) rather than guessed. The card's
own «[ص: ٣٧٢]» belongs to a different edition and was **not** overwritten by this
one, which is the same refusal applied earlier to «المقام»; and
`مقابل_بنسخة_ورقية_محققة` still has no entry, because pagination encoded from a
named print edition is not collation against paper.

Two boundaries carry the weight. `ExhaustedSourceIsNotAnExhaustedWorld`: one book
named in the card's own `المصدر` field was exhausted, not the question — reading
this as a finding that later commentators added nothing to Zayn ibn al-Munīr
would write the tool's limit into the world. And
`ClosureIsNotTheOpeningOfWhatItUnblocks`: satisfying the condition that
`LEXICAL_PATH_FRONT_IS_REGISTERED_NOT_OPENED` attached to `طريق_النقل_المعجمي`
proves the sequential block has lifted, and does nothing else. No tool, no
vocabulary, and no member of any existing enumeration was built for that front in
the step that closed its prerequisite, since opening a level in the same act that
closes the one below it runs the two together — which is exactly what
`NoRicherStructureBeforeLowerOpenResidualClosure` forbids. The module issues no
birth, no verdict, no freeze, no `E0`, and not one character of
`qayd_marker_preregistration` or `level_two_manat` changed.

### الناسخ والمنسوخ: the last uncoded section of `usul_dalala_sections`

Of the five governing sections of دلالة الألفاظ, four have carried modules for
some time; `الناسخ_والمنسوخ` was the only one that read `غير_مُرمَّز`. That was
not an oversight but a refusal with a named ground —
`NASKH_TEXT_NOT_EXTRACTED_RESIDUAL`: no text for it had been transcribed, and
building a vocabulary for a section before its text arrives means the text, when
it does arrive, gets fitted to a vocabulary that preceded it rather than derived
from it. That is precisely what `MarkerVocabularyIsFrozenBeforeItsText` forbids.
The text has now been supplied, so `naskh_mansukh.py` is built *from* it, and the
section's reading flipped to `مُرمَّز` **by reading the tree** — the coverage map
is derived from module presence, never written in a table, so no coverage
declaration was edited to produce that flip.

The definition is transcribed as given: «النسخُ هو إبطالُ الحكم المستفاد من نصٍّ
سابقٍ بنصٍّ لاحق». Its three conditions — that the abrogated ruling be
شرعي, that the lifting evidence be متراخٍ in time, and that the original address
not be مقيَّد بوقت معيَّن — are conjunctive and **derived**, never written in a
field, on the same `BothUnitiesOrNoCarrying` pattern that `mutlaq_muqayyad`
already uses. Settling for two of the three would abrogate rulings that are not
abrogable.

Four distinctions do the real work, each one preventing a specific collapse:

- `ExpiryIsNotNaskh`. A time-bound address lapses when its time lapses, by
  itself, needing no abrogator at all. Reading that lapse as naskh would admit
  into the chapter what was never in it and hand naskh a stock of false
  supporting instances. So `انتهاء_وقت_لا_نسخ` is a *third member* of the outcome
  vocabulary, not a politer spelling of `لا_نسخ`, and it is evaluated first —
  an address outside the chapter must not be described as having failed the
  chapter's conditions.
- `NoNaskhOfTheCertainByTheProbable`. «لا يجوز أن ينسخ المتواتر إلا بالمتواتر».
  The ladder is **imported** from `TransmissionStanding`, not rebuilt here, so
  there is no second ranking to drift out of step with the first.
- `FardIsNotAWeakerRankButNoRankAtAll`. Refusing an آحاد abrogator of a متواتر
  refuses something measured that fell short; refusing a فرض abrogator refuses
  something never measured. Folding both into one ground would suggest a فرض can
  be argued up into an abrogator, when it can only be *measured* into one. Each
  gets its own refusal member.
- `IbtalIsNotButlan`. «الإبطالُ هو نسخُ الحكم، وأمّا الباطلُ فهو ضدُّ الحقّ».
  Naskh lifts a ruling that was **sound** and whose term ended; it is no verdict
  against it. An import-time guard therefore rejects any candidate field naming
  invalidity, corruption, or weakness.

نسخ التلاوة is recorded exactly as transmitted: `لم_يثبت_بالقطعي`. That is a
denial of establishment, not a denial of possibility, so `واقع` and `ممتنع` both
remain in the vocabulary with no entry, and the emptiness of both must not be
read as preferring either.

What this does *not* do is named as carefully. The wording arrived in a request
citing الشخصية الإسلامية ج٣ by extracted line numbers, and was never collated
against a named print edition: `NASKH_WORDING_IS_SUPPLIED_NOT_COLLATED` and
`EXTRACTED_LINE_NUMBERS_ARE_NOT_PRINT_PAGINATION` say so, and the module is a
registration, not a certificate. No verse and no ḥadīth is judged abrogated
here (`NoRulingIsIssuedOnAnyText`); the venue قرآن/سنة is declared by the caller
and derived from nothing; and naskh across the two venues has no transmitted
wording, so the module neither permits nor forbids it. The lifted residual stays
in the tree marked as lifted rather than deleted, because a residual's lifting is
an event to be read, not a trace to be erased — and lifting it did not lift its
neighbour: `SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED` stands exactly where it
stood. The module issues no birth, no verdict, no freeze, no `E0`, and imports
nothing from `kernel/`.

### Opening the `طريق_النقل_المعجمي` front by answering its variable

`LEXICAL_PATH_FRONT_IS_REGISTERED_NOT_OPENED` registered one open variable and
forbade work on it until the سائمة الغنم experiment closed with a single complete
result. That experiment closed with a complete negative, so the sequential block
of `NoRicherStructureBeforeLowerOpenResidualClosure` has lifted and the front may
be opened. It is opened the only way that counts: by **answering its variable** —
«أهو طريقٌ ثالثٌ يُقرأ في نفسه أم تابعٌ لطريق نقل القيد؟» — not by widening a
vocabulary. `LexicalCitationStructure` still has exactly three members, and not
one character of `qayd_marker_preregistration` changed, because answering a
question by editing the place that records it removes the question instead of
answering it.

`lexical_path_census.py` reads the cards in `examples/` **at call time** and
derives the answer: `يقرأ_في_نفسه`. Both keys are imported, never re-spelled —
`CARD_LEXICAL_PATH_KEY` from `lexical_transmission` and
`CARD_COMPOSITION_RELATION_KEY` from `level_two_manat` — since a key written
twice gets changed in one place and left in the other.

The argument is not the tally. The dependency claim is universal — *the lexical
path is never declared except alongside the qayd path* — so a single counter-
instance refutes it (`OneCounterInstanceDecidesADependencyClaim`). The derivation
therefore tests for the **existence** of a card declaring the lexical path with
no composition relation, and the standing would be identical if the ratio were
one to five instead of five to one. Arguing from the count would make the answer
hostage to whichever card gets written tomorrow. In this tree the counter-
instances are named individually, not merely counted.

Three limits are recorded rather than absorbed. `DeclaringAPathIsNotWalkingIt`:
four of the six declare the key with an **empty** attribution list, so what is
derived is that the declaration is independent of the qayd path, not that the
path was walked — chain strength stays in `lexical_transmission` behind
`LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS`, and this census derives no citation
structure and no transmission standing at all. (An empty declaration still
counts as a counter-instance, because the refuted claim is a claim about
*declaration*.) `SchemaIdentityIsNotSemanticIndependence`: all six agree on the
same three keys, which witnesses one shape wherever the field occurs and proves
nothing about independence of meaning. And `ThisTreeIsNotTheWorld` — the same
limit as `ExhaustedSourceIsNotAnExhaustedWorld`, applied to a tree instead of a
book: exhaustive over `examples/` is not exhaustive over cards. One further gap
is named: only dependence *in declaration* was tested, and a dependence in
content — the lexical path being read for the sake of the qayd even when declared
alone — is neither examined nor denied, since refuting one shape of dependence is
not refuting every shape. No card list is frozen here either, so the census is
true with the tree and false with it, and is not a certificate to be cited after
the cards change. The module issues no birth, no verdict, no freeze, no `E0`, and
imports nothing from `kernel/`.

### Depositing a carrier/state codec as a measured round trip, not as an atom

An externally built (carrier, state) codec for vocalized Arabic was offered to
this tree with the claim that the pair is "the only consistent atomic unit of
the vocalized Arabic letter", proved to four decimal places over three
independent texts. `src/alghanem/arabic/encoding/carrier_state_candidate.py`
accepts the codec and declines the claim, because what was measured is a round
trip: `retrieve(generate(s)) == s`. Losing nothing is a property of *every*
information-preserving re-encoding — "the unit is the whole word" round-trips
too — so a rate is evidence about loss and never evidence that the chosen unit
is atomic, minimal, or unique (`ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY`).
G0.N licenses a knot by the weaker models it survived, and no weaker model was
licensed or frozen here, so nothing is born, ranked, or frozen
(`NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN`), and the type is a
`CarrierStateUnit` produced by a candidate codec rather than an `Atom` or a
`Protocol`.

Three defects were found by running the deposited codec rather than by reading
its prose, and the third is the one that decided the design. Two consecutive
harakat, two tanwin marks, a harakah followed by a tanwin, and a doubled shadda
each wrote over a value already derived and returned a surface different from
the input; the deposit's own revision closed the first of these by hand, which
would have closed an instance while the genus stayed open, so a single rule now
refuses every second write into a slot that already holds a derived value. Every
non-carrier codepoint was dropped silently — `العربية!` came back without its
exclamation mark — and is now carried as an explicit passthrough unit, which
also means the Uthmani residue reported with the deposit mixes a codec defect
with the five Uthmani phenomena it was read as measuring, and arrived as two
figures that disagree with each other
(`UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS`). Third, a dedicated
`madd_self` state wrote `tanwin`, `silent` and `waw_madda` onto the unit for
`آ` and then returned from retrieval before reading any of them, so inspecting
the unit showed information that retrieval had already discarded. `آ` is now an
ordinary seat on the `ء` carrier, which makes the special case disappear rather
than be guarded, and units whose state is structural are checked at
construction to carry nothing else — so "no field is written and never read" is
a property of the type instead of a claim about one branch.

The layer registry's first claim was settled by derivation rather than by
editing its wording. It asserted that the alef carries `sukun_implicit`
exclusively; `derive_alef_states` runs the codec and returns the states an alef
actually holds, and it returns more than one, because ordinary orthography
writes tanwin on the alef. Enforcing the claim would refuse real text, so it is
recorded as declared and deliberately unenforced
(`ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED`). The carrier set is written
out in the module instead of being `str.isalpha`, which had made every
alphabetic codepoint of every script a carrier, and it says of itself that it is
declared and not derived from any property of Arabic
(`CARRIER_SET_IS_DECLARED_NOT_DERIVED`).

No percentage over any external text was recorded at first. A rate is
re-derivable only by a holder of the same bytes, so `InvertibilityMeasurement`
requires the source's `sha256`, its byte length, the normalization form and the
Unicode database version, on the pattern of `QaydAttributionScan`, and derives
its counts by running the codec rather than accepting them; it carries no
percentage field at all. One source is now measured. A second external revision
of the deposited codec arrived later, claiming a clean round trip at 100.0000%
over "78,245" Quranic words and over an unnamed modern-Arabic sample, and
re-deriving that claim required a corpus that *is* fingerprinted — the Quranic
Arabic Corpus deposit already recorded in `irab_corpus_witness`, digest and byte
length only, never vendored bytes. The result is
`QURANIC_CORPUS_INVERTIBILITY`, and it is stated with the bound that makes it
honest: six of its 77,429 words are refused at construction by the
already-closed silent-overwrite rule rather than read, so the derived fraction
is a fraction over accepted tokens and `token_refusals` is carried beside the
other two totals (`REFUSAL_IS_NOT_A_ROUND_TRIP`). The two Uthmani figures that
came with the original deposit stay unmeasured
(`ONE_SOURCE_IS_MEASURED_TWO_REMAIN_UNMEASURED`), and a clean round trip over a
closed text stays bounded by it under `CompleteInductionIsCorpusBounded`
(`THREE_SOURCES_ARE_CORPUS_BOUNDED`). What the tests establish is stated with
its bound: every embedded case and a bounded probe of a few thousand generated
surfaces round-trip exactly and no two distinct surfaces share one unit sequence
*within that probe*.

### Auditing a deposited revision by running it, not by reading it

`src/alghanem/arabic/gflk_codec_revision_audit.py` records what that 100.0000%
claim did when it was re-derived here. It came back **99.992251%**: six real
words of the corpus are corrupted silently, `فَٱدَّٰرَْٰٔتُمْ` losing a fatha
with no warning, and all six are one genus — a second write over a state already
read, which is the first defect this tree had already named and closed, restored
by the revision's own loop (`SILENT_OVERWRITE_DEFECT_REINSTATED`). The second
closed defect is restored too: `madd_self` still returns before reading the
fields written beside it, so `آً` comes back as `آ`. Those forms never occur in
the Quranic corpus, which is exactly why a corpus rate could read as 100% while
they were broken (`A_CORPUS_RATE_DOES_NOT_COVER_THE_UNATTESTED`). The claimed
population is unidentified — no digest, no byte length, no tokenization rule, so
the 816-word gap from the measured 77,429 cannot be attributed
(`THE_CLAIMED_CORPUS_IS_UNIDENTIFIED`) — and the "independent" second source was
run with the same tool and the same success criterion, which is one line of
evidence run twice rather than two (`SECOND_SOURCE_IS_NOT_AN_INDEPENDENT_LINE`).
One thing in the revision is a genuine repair and is credited by running it:
non-carrier symbols are no longer dropped, so `العربية!` and `hello` survive
(`PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT`).

The refusal is computed, not written. `CodecRevisionAudit` has no field a
verdict could be placed in — a guard runs at import to keep one from being added
later — and `outcome` is derived from comparing the claim against the
measurement and from the standing residuals, so both branches are reachable and
changing the verdict means changing an input that shows. Every number above is
re-derived by `examples/irab/measure_carrier_state_invertibility.py` against the
fingerprinted bytes, including the six locations by `(sura:aya:word)`; none is
written by hand into the tree. And a clean round trip, had it held, would still
have shown only that the encoding loses nothing
(`ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY`): nothing here is born, ranked or
frozen, and no gate in `kernel/` reads any of it.

### Scanning two adjacent sukuns without buying a hundred per cent

`src/alghanem/arabic/encoding/sakin_adjacency.py` reads the units of
`carrier_state_candidate` and reports, for every adjacent pair whose members
both hold a sukun, whether the pair is counted or excluded and by which named
exclusion. It reports one row per pair, excluded rows included, so nothing is
subtracted before it can be looked at. It records no rate. A predicate that
names an exclusion for every pair it meets reaches a clean residue by
construction, and that cleanliness is a property of the predicate rather than a
measurement of the language (`CLOSURE_IS_A_PREDICATE_NOT_A_MEASURED_RATE`).
Sharper still, an exclusion written *after* inspecting what an earlier pass left
over is a description of that residue and cannot also be evidence for the rule it
rescues; `SakinClashExclusion.is_residue_defined` marks the three that were
(`RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE`). No source text is
vendored here, so no figure quoted elsewhere is re-derivable and none is written
down; `SakinClashScan` requires a digest, a byte length, a normalization form
and a Unicode database version, derives its counts by running the scan, holds no
percentage field, and `MEASURED_SAKIN_CLASH_SOURCES` is empty.

Three things were settled by running the codec rather than by reasoning about
it. `derive_article_gemination_offsets` shows that the definite article puts the
gemination mark at unit offset 2 before a sun letter that is not `lam`, and at
offset 1 in `ٱلَّذين` where the `lam` is itself geminated — so the pair (`ٱ`, `ل`)
in `ٱلشَّمس` carries the mark on *neither* member and no gemination check of any
single position reaches it. What reaches it is that `ٱ` extends a sound instead
of closing a syllable; the assimilation check reaches the *next* pair, (`ل`, `ش`),
and there the mark sits on the second member. Both checks are needed and they
answer about different pairs. Second, the silent zero is already carried on the
unit it follows rather than arriving as a stray unit, so `قَالُوا۟` yields five
units and a scan expecting a sixth would find nothing to repair. Third,
`derive_ha_and_ta_marbuta_units` shows that the small waw and small yeh writing
the connecting vowel after `ه` arrive as passthrough units — sound extension,
never a sukun holder — while `ة` arrives as carrier `ت` under
`CarrierSeat.TA_MARBUTA`, so at a stop, where it is read `ه`, the unit still
reports `ت` (`TA_MARBUTA_PAUSAL_HA_IS_NOT_ENCODED`).

Writing the module surfaced one defect of the kind the tree already refuses. The
dagger-alef exclusion named a case no pair could reach, because a dagger unit
holds no sukun and so was never a member of a pair while silently resetting
adjacency: a name written and never read. A dagger is now read through like a
passthrough unit and the exclusion is reported on the pair that spans it, and a
test asserts that *every* member of the exclusion enum is reachable — the guard
is the genus, not that instance. Passthrough units are read through rather than
treated as separators, because the classic adjacency is the one across a word
boundary and a space is a passthrough unit; the number skipped is recorded so a
wide gap stays visible. A stop mark is only a passthrough unit, so a sukun read
because the reader stopped cannot be told from a sukun of the connected reading
(`PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN`), and the rulings of
the sukun-bearing nun act where the following consonant carries a vowel and so
decide no pair counted here (`NUN_SAKINA_RULINGS_ARE_NOT_MODELLED_HERE`). The
disconnected letter openings are placed outside the rule's scope by a written
list, because each letter is uttered under its own name and the question is not
posed of such a sequence — a declaration about scope, not a result
(`MUQATTAAT_ARE_EXCLUDED_BY_DEFINITION_NOT_MEASURED`). Finally, an argument that
a language avoids the adjacency because avoiding it is easier is an induction
over the utterances met and bounded by them; no weaker model was licensed or
frozen for this predicate, so nothing here is born, ranked, or frozen
(`PHONETIC_ECONOMY_IS_AN_INDUCTION_NOT_A_LICENCE`).

### Asking whether a relation layer exists at all, before writing a reader for it

The previous round closed with a named absence: the Quranic Arabic Corpus
morphology file carries four columns, not ten, and no head or relation among
them — `SYNTACTIC_LAYER_ABSENT_IN_THIS_FORMAT`. That closed one format, not the
question. `src/alghanem/arabic/ud_relation_layer_step0.py` is a step-zero record
for the separate question: does *any* reachable Arabic treebank actually carry a
populated dependency layer? It is a census and a deposit, not a reader
(`STEP_ZERO_IS_NOT_A_READER`). It measures no syntactic function and compares no
claim of objecthood against another; whether such a measurement is ever run is a
separate decision this module does not take.

Five files were fetched and read as bytes rather than as project descriptions.
`ar_pud-ud-test` (1,000 sentences, 20,747 tokens) and the three
`ar_padt-ud-*` files (7,664 sentences, 282,384 tokens in total) carry `HEAD` and
`DEPREL` populated on *every* token line, so the outcome for them is
`RELATION_LAYER_PRESENT`. `ar_nyuad-ud-test` is the case that a project
description would have hidden: its `HEAD` and `DEPREL` are populated on all
74,125 tokens while `FORM` and `LEMMA` are an underscore on all 74,125, because
the underlying Penn Arabic Treebank text is LDC-licensed and was removed. That
is `RELATION_LAYER_PRESENT_BUT_LICENCE_BLOCKED`: an annotation layer over words
that are not there (`SURFACE_WITHHELD_IS_NOT_A_CORPUS`). No repository named
`UD_Classical_Arabic` exists at all; the probe returned 404
(`UD_CLASSICAL_ARABIC_DOES_NOT_EXIST`), so the reachable sources are newswire
and not the register every earlier Arabic number in this tree was measured on
(`REGISTER_IS_NEWSWIRE_NOT_QURANIC`).

`OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED` is named in the module before any reader
exists, because it is a known property of the UD schema and not a finding to be
discovered after an accuracy figure — which is exactly how
`ACCUSATIVE_IS_NOT_OBJECTHOOD` was named too late last round. The census then
measures the size of that gap instead of assuming it: in `ar_padt-ud-train`,
23,002 tokens carry `Case=Acc` and only 5,449 of them are labelled `obj`, so
case alone over-predicts objecthood more than fourfold. A test asserts this
separation holds in every measured file, and it is asserted over counts, not
over a prose claim.

No treebank bytes are vendored. Each file is deposited as its own independent
witness — digest, byte length and licence terms, in the `IrabCorpusWitness`
style — and none of them reuses or extends `QURANIC_ARABIC_CORPUS_WITNESS`.
PADT is CC BY-NC-SA 3.0 while this repository is MIT, and that non-commercial
condition follows the bytes rather than the digest
(`NON_COMMERCIAL_IS_NOT_THIS_TREES_LICENCE`). `FORM` is unvocalised in both
usable treebanks, with PADT carrying the vocalised form only in `MISC` under
`Vform` and PUD not carrying it at all, so anything fed to `CarrierStateCodec`
from here must name which column it was fed
(`UNVOCALIZED_FORMS_ARE_NOT_CARRIER_STATE_INPUT`). The outcome is a derived
property over a closed three-value vocabulary, never a stored field, and every
number in the module is re-derived by
`examples/irab/measure_ud_relation_layer.py` against the recorded digests.

### The claim that started this measured, at last, against syntactic function

The census closed with a condition written into its own module: a step-zero
count "does not substitute for a frozen pre-registration preceding any later
measurement" (`STEP_ZERO_IS_NOT_A_READER`).
`src/alghanem/arabic/ud_objecthood_preregistration.py` is that pre-registration
and was committed on its own, before a single relation byte was read, so the
ordering is in the repository's history rather than in a sentence claiming it.
It freezes the claim as stated, the predictor rule, the column the vowel is
read from (`MISC:Vform`, never `FORM`), the population, the definition of an
unreadable position, the development and held-out files, the two decision
thresholds, and four readings that are refused in advance whatever the number
turns out to be. It carries no result field at all, and an import-time guard
keeps one from being added later. What *had* already been seen is named rather
than hidden: the token, `obj` and `Case=Acc` totals of those files were
deposited by the census
(`STEP_ZERO_COUNTS_WERE_KNOWN_BEFORE_THIS_PREREGISTRATION`); no vowel and no
position adjacent to a perfect verb had ever been read from them.

`src/alghanem/arabic/ud_objecthood_measurement.py` then runs it. **The claim
falls**: on the held-out `ar_padt-ud-test`, of the 419 positions the claim
decides it gets 150 right — **35.8%**; on `ar_padt-ud-dev`, 30.1% of 449. The
declared threshold for refutation was 60%, fixed before the reading, so
`CLAIM_REFUTED` is derived by that threshold and not by an impression of the
number. Each measurement is bound to the digest of the specification it ran
under, so editing the specification after the fact makes the measurement fail
to *construct* rather than emit a warning. This is the first time the original
hypothesis has been measured against a **function** annotation rather than a
**case** annotation; it had stood unmeasured since
`ACCUSATIVE_IS_NOT_OBJECTHOOD` was named.

The 97.1% of `irab_case_readout` is untouched by this. That number is a reading
of the *case mark*, and it stands. What falls here is only the second step —
the move from the mark to the syntactic function.

Most of the failure is not a misread vowel but the population the claim itself
defines (`FUNCTION_WORDS_ARE_IN_THE_POPULATION_AS_STATED`): 188 of the 269
held-out errors are function words — `إِلَى`, `أَنَّ`, `وَ`, `لَ` — which end
in fatḥa and are not nouns at all. The claim as stated excludes no class, so
they count against it, and excluding them would be measuring a different claim.
Reach is reported beside precision instead of under it: the rule reaches 68.2%
of the objects actually present, and 10.1% of positions are unreadable and are
recorded as `متعذّر_القياس`, never as wrong.

A defect in the frozen specification surfaced during the run and is filed
rather than quietly repaired
(`PREREGISTERED_VOCABULARY_COVERS_PREDICTED_POSITIONS_ONLY`): its three-value
position vocabulary covers predicted and unreadable positions and has no place
for a readable position the claim does not predict. `classify_position()`
raises on that case instead of granting it a value it does not have, and the
class is counted in a fourth named field. Two further residuals are named
before anyone reads the number the wrong way: `obj` in UD is not the *mafʿūl
bihi* of Arabic grammar (`OBJ_IS_UD_OBJECTHOOD_NOT_CLASSICAL_MAFUL`), and
"following the verb" in the claim is linear adjacency in the file, not
government (`ADJACENCY_IS_NOT_GOVERNMENT`). The two splits ran the identical
rule with nothing tuned on either, so their gap measures the difference between
two splits and not fitting (`NO_RULE_DEVELOPMENT_HAPPENED_THIS_ROUND`). Every
frozen number is re-derived by `examples/irab/measure_ud_objecthood.py` against
the recorded digests, which imports the vowel reader and the threshold rather
than re-implementing either.

### Correcting those two defects without editing what was frozen

Both defects are now corrected, and neither is corrected in place.
`src/alghanem/arabic/ud_objecthood_amendment.py` is a second specification with
its own digest; the first specification, its digest and its 35.8% are untouched
(`THE_FROZEN_SPECIFICATION_IS_NOT_EDITED`). Editing a specification after
seeing the number it produced is the one thing the freeze exists to prevent,
and it stays prevented even when the edit would be an honest repair — whoever
edits theirs after the number no longer holds a specification that preceded its
evidence.

The amendment says so in its own structure rather than in prose that can be
skipped: its `standing` field is constrained to `معدَّلة_بعد_الرقم`, and it
cannot be constructed with the stronger value at all
(`AN_AMENDMENT_AFTER_THE_NUMBER_IS_WEAKER_THAN_A_PREREGISTRATION`). The
population defect is corrected by excluding exactly the function-word `UPOS`
list that classified the errors in the first place — a second, hand-picked list
is refused — and the vocabulary defect by a four-value vocabulary in which a
readable position the claim does not predict finally has a place of its own, so
`classify_amended_position()` no longer raises where `classify_position()`
must. Both thresholds are *imported* from the first specification rather than
restated, so no threshold can drift toward the new number.

**The correction does not rescue the claim.** On the held-out split precision
rises from 35.8% to **64.5%** — inside the undecided band, not above the 90%
standing threshold — while the development split reaches 54.7% and stays below
the 60% refutation threshold. The two splits therefore return *different*
verdicts on one treebank under one rule
(`THE_TWO_SPLITS_DISAGREE_UNDER_THE_AMENDMENT`), and that disagreement is
itself the reason "the claim stands" cannot be said; the higher of the two
numbers is not taken and the lower left behind. Reach did not improve either:
it falls slightly, because the exclusion removes four positions that really
were `obj`, and that loss is carried in its own field rather than netted away.

The correction has a price, and it is named: excluding function words reads the
treebank's own `UPOS` column, so the amended reader is no longer a purely
surface one (`THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_ANNOTATION`). It
consumes one annotated column to define its population and is then scored
against another. Running this claim on unannotated text would need a
part-of-speech classifier that does not exist here, and that classifier's own
accuracy would enter the number.

### Reading the GFLK extractor as roles over units, without a new state

The deposited GFLK specification asks for a state machine whose second pass
assigns letters states such as `MADD_EXTENSION`, `ASSIMILATED_SILENT` and
`TANWEEN_ALIF_CARRIER`. Those are not states here. `CarrierState` stays closed
at seven measured members, and
`src/alghanem/arabic/p_extractor.py` reads the specification's proposals as
*roles over units the codec already emits* — a derived reading, not an
enlargement of the vocabulary. `HARAKA_BEARING` follows the same discipline: it
is a predicate computed from state and roles, never a stored flag that could
drift from them.

The rule order is frozen before the reader exists.
`p_extractor_preregistration.py` fixes the eight Pass-2 rules as an ordered
tuple with, per rule, its trigger, what it reads from the unit, and whether it
is decidable from the written marks at all. Two are registered as **not**
decidable up front — the waṣl-lām branch and the shamsiyya/qamariyya split —
so the reader emits an `UndecidedSite` there instead of a guess, and the
implementation refuses to import if its rule names ever disagree with the
frozen tuple.

**What was measured:** the acceptance floor was written before running, and it
is the existing codec's own round trip — no regression in the percentage *and*
no token newly corrupted. The six tokens the codec already loses are named test
cases rather than absorbed into a percentage, because a percentage hides a
single word and a named case does not.
`examples/letter_fingerprint/measure_p_extractor_floor.py` re-derives the
figure from the corpus bytes and exits non-zero on drift.

**What it does not establish:** nothing about the phonetic reality of these
roles. It establishes that the specification's second pass can be *stated* over
this tree's units without adding a state, and that stating it costs no round
trip. Writing the vowel of a waṣl alif remains impossible here, and that is the
reader's refusal, not its silence.

### One proposal that stays outside the vocabulary altogether

The specification's last Pass-2 rule reclassifies a letter as
`AMBIGUOUS_MADD_OR_TANWEEN_ROOT`, calling it an explicit DEFER. A vocabulary
that contains a member meaning "undecided" can no longer be read as a closed
set of decided values, so this tree refuses membership
(`REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY`). The condition is still detected:
it comes back as a separate `AmbiguityRecord` collection beside the reading,
with the site, the competing readings, and what would decide between them. A
structural test walks every enum in `src/` with the AST and asserts the name
appears as a member of none of them — the same zero-match sweep used elsewhere
in this tree, pointed at a name this tree was invited to adopt.

### Alif on two scopes that must not be merged

`src/alghanem/arabic/alif_neutrality_registration.py` records the
specification's alif reading as what it is: two claims on two different scopes.
Featurally the alif is N/A on all four axes together — not "low" and not
"original" by default, but absent — and that is a claim about a feature grid.
Informationally it is neutral in three of its four roles and *not* neutral in
the fourth, where it carries the tanwīn mark itself; that is a claim about an
information projection. The two do not contradict each other and are not
averaged into one "mostly neutral" verdict.

**What was measured:** after the extractor landed, three of the four roles are
separable from the written marks in this tree — madd, differentiating alif, and
tanwīn carrier all have named roles. The fourth, waṣl, is not, and the
amendment in `gflk_specification_deposit` was updated to say exactly that
rather than to keep claiming all four are unreadable.

**What it does not establish:** the informational claim itself. Testing "π with
the alif equals π without it" needs a projection this tree does not compute, so
the claim is recorded as untestable here rather than as unsupported. Tāʾ
marbūṭa is recorded as conventionally excluded, with the note that its
connected-speech pronunciation — the actual reason the exclusion is different
in kind from the alif's — is read nowhere in this tree.

### Six templates, and a wazn that is a projection rather than an object

`syllable_preregistration.py` freezes, before any segmentation runs: the six
templates as a closed enum; shadda expansion into a closing sākin plus an
opening mutaḥarrik; the declaration that wazn is a **derived projection, not a
born morphological object**; the reading of tanwīn as a vowel plus a closing
nūn that is not written; and four structural acceptance conditions — closure,
reconstruction, totality, determinism — each written down before it could be
checked.

`syllabifier.py` then segments deterministically over the extractor's output.
A word it cannot segment is emitted in `wazn_unresolved` with a named reason,
never as `None`, and when the stopping point coincides with a standing refusal
the refusal is named in the record: words opening on a waṣl alif fail because
the alif's vowel is not decidable, and the record says so instead of reporting
a mysterious failure. The waqf transform is a separate, explicitly named
function taking a *stated* pausal input, because this tree cannot tell a pausal
sukūn from a connected one by looking.

**What it does not establish:** `DictionaryLayer.SYLLABLES_AND_WAZN` is still
withheld. The floor script prints the unresolved share with **no threshold
attached** (`NO_THRESHOLD_IS_INVENTED_AFTER_THE_FACT`), and the corpus is not
vendored, so no figure is issued here. Two limits are recorded rather than
quietly handled: the tanwīn seat on alif maqṣūra is not read, and the free
madda mark is not read as length.

### A root criterion that counts slots and refuses to name a weak letter

`jarad_mazid_preregistration.py` freezes the corrected criterion — a slot is a
real consonant **or a madd**, three slots is mujarrad, four or more is mazīd —
together with a limit declared permanent rather than temporary: this criterion
measures **length only** and says nothing about whether a given wāw or yāʾ is
root or augment. No wider measurement lifts that; it is a property of the
criterion, not of the sample size.

`jarad_mazid.py` matches full consonant skeletons against the digest-checked
Maqāyīs root table, which re-verifies byte length, SHA-256 and header on every
read. Prefix matching — the defect the specification corrects in itself — is
absent, and the two match kinds it does emit, exact skeleton and ordered
subsequence, stay separate and unranked. A structural test asserts no
`RootMatchKind` member anywhere in `src/` contains `PREFIX`.

**What it does not establish:** any corpus figure. The four deposited counts
(10,599 / 11,467 / 37,682 / 18,333) are carried in the preregistration as
figures **to be compared against**, with `is_adopted=True` refused at
construction, because they lack a `MeasurementRunManifest` and a written
pre-measurement expectation — two of the four prerequisites frozen alongside
them. Their arithmetic gap against 78,215 was already recorded in the deposit
and is not restated here. What ships is a criterion and a tool, not a count.

### Naming the four milestones that were not built, and why

`gflk_milestone_blocking_registration.py` records the rest of the plan rather
than omitting it. Four milestones are named with their missing input, the kind
of block, and what would lift it: the feature tables (no digest-able source for
the 13-category scheme, no bytes for the 12-axis sifa table), the OCP
permutation test (its classification source is undefined until the tables
resolve), the conditional-bit tree encoding (its bit inventory *is* the sifa
table), and the compression ladder (a scope decision not taken). The
distinction the module insists on is between "not measured yet" and "not
measurable from here"; all four are the second kind.

No figure crosses a standing block. 88.34%, 18.75%–23.2% and p≈0.027 are listed
in the records as figures explicitly *not* carried across, since mentioning a
number inside a Python module does not make it measured. The import barriers in
`gflk_feature_table_import_barrier` stay `OPEN`, and an import-time guard makes
this registration refuse to load if one is ever lifted without revisiting it.

## Reference material

`docs/reference/` holds frozen external measurements kept for future
experiments. It is non-normative: nothing there licenses a transition, births
an object, or amends `docs/CONSTITUTION.md`. The first record,
[`docs/reference/lisan345_cluster_adjacency.md`](docs/reference/lisan345_cluster_adjacency.md),
measures same-place adjacency in the 6,529 triliteral roots of the open
`lisan345` dataset: under a declared 0.5 threshold six of nine clusters show
avoidance and three do not, and the record states in its own body what it does
not establish, including two open questions it leaves unresolved. The
dataset is not vendored; `examples/reference/lisan345_cluster_adjacency.py`
re-derives the table from a hash-checked copy of the frozen input.

The second record,
[`docs/reference/arabic_identity_confusion_catalog.md`](docs/reference/arabic_identity_confusion_catalog.md),
catalogs five Arabic identity-confusion failure modes reported by an independent
session that ran a structurally similar five-gate protocol over a different
corpus: homograph collision under bare-skeleton reduction, a tanwīn-bearing
silent letter read as vowel-bearing, gemination erased by undifferentiated mark
stripping, a case ending folded into template identity, and a pattern space
whose members are mostly not lexical items. Each is offered as a candidate test
case for the deferred G0.2 or a later Arabic identity-birth layer, with its
proposed law named in negative form. Unlike the first record it carries no
frozen dataset, no hash, and no re-derivation script, so it is testimony rather
than measurement, and its numbers are unaudited; the record says so in its own
body and names the measurement-wrapping path any promotion would have to take.

The third record,
[`docs/reference/word_hierarchy_rebuild.md`](docs/reference/word_hierarchy_rebuild.md),
deposits an externally supplied six-level hierarchy of Arabic word structure —
letter, vowel, syllable, pattern, word, and `mabnī` — in both of the versions it
arrived in, the second of which declares that it fully replaces the first, plus a
third text that declares a freeze and retracts the hierarchy's word-boundary gap
figure. Depositing only the corrected version would erase that claims were
withdrawn, so
`src/alghanem/arabic/word_hierarchy_deposit.py` records each withdrawal with its
successor and its stated reason, and names the figures that were dropped with no
reason given as exactly that. Every node carries its standing from the existing
four-member `LayerEpistemicStanding` vocabulary, and a node may be marked
measured only if it names a layer that is actually in
`word_structure_dictionary.MEASURED_LAYERS` — so the deposit cannot promote a
withheld layer by writing a word. No corpus, measurement manifest, or
observation ledger arrived with the text, so all eighteen of its figures,
including its "zero breach" universals, are registered as not re-derivable in
this tree, each with a named reason and the condition that would make it
re-derivable. A figure that rests on another names it in `depends_on_figure`, and
a figure the text presents as the output of a class defined as "whatever is left"
is refused at construction unless it carries that tag — so the third text's three
headline results are recorded as one witness read three times, not three. The two
freeze identifiers it cites are kept verbatim alongside a field stating that
neither was issued by this tree. Seventeen conflicts with this tree are recorded
and none is resolved; ten of them block import, and the newest level collides
with three standing refusal texts rather than merely lacking a corpus. The four
withheld dictionary layers remain withheld after the deposit exactly as before it.

The fourth record,
[`docs/reference/gflk_arabic_letter_specification.md`](docs/reference/gflk_arabic_letter_specification.md),
deposits the language-independent GFLK specification for processing the Arabic
letter, now in both of the versions it arrived in. The second version qualifies
claims the first stated flatly — every "analytic", "proof", and "logical
certainty" in it is now read relative to a declared definition rather than
absolutely — and adds four blocks the first did not contain: a corrected
free-versus-augmented root criterion with four corpus counts, a neutral-alif
reading, a uniform CVC-CVC syllable signature for the imperative, and a
nine-level transitivity hierarchy ending in "a passive exists, therefore the verb
is genuinely transitive". Depositing the expanded version alone would erase that
a claim was first asserted and then narrowed, so
`src/alghanem/arabic/gflk_specification_deposit.py` records each changed locus
with what both versions said and what this tree reads in the change, and refuses
a deposit that declares fewer than two versions. No corpus arrived with the text,
and neither did the root file it names, so all seven of its new figures are
registered as not re-derivable, each with a named reason and the condition that
would change that; the "unconfirmed" count is defined by non-match against that
absent root list, so it is refused at construction unless it names the figure it
depends on. Its "zero deviation on 4/4" and "6/6" sweeps are recorded as
enumerated examples rather than populations. The freeze identifiers it cites
have zero matches in `src/`, `docs/`, and `tests/`, and a test enforces that,
keeping them verbatim beside a field stating that none was issued here. Five new
conflicts are recorded and none resolved: the imperative signature alone collides
with three refusals that were written before the text arrived — the syllable
layer is withheld, hamzat waṣl is not decidable from the written marks, and a
final sukūn is not distinguished pausal from connected — all three wider than the
one open limit the text declares for itself.

A later message from the same conversation, deposited verbatim in §٢-ب, closed
two gaps in that text without changing anything's standing. It names the nine
freeze identifiers that had been referred to only as a count, so all nine are now
registered here, swept for, and found nowhere in the tree — naming made the check
possible, and the sender says plainly that it does not make them frozen here, so
that agreement is recorded rather than argued. It also names the two sources the
figures came from. One of them, `quran-simple-enhanced.txt`, is cited by a
truncated digest, and the full digest is already frozen in this tree in
`compression_model_preregistration.FROZEN_CORPUS`; the module asserts that
equality at import rather than restating the hex, and a truncated digest like
`3763...6c5a` is refused outright, since two ends are not a fingerprint. The
other, `maqayis_by_root_csv_999.csv`, first arrived as a name only — its origin
given as Ibn Fāris's *Maqāyīs al-Lugha*, and copies of a dictionary differ byte
for byte, so naming an origin is not fingerprinting a file. Its bytes have since
been uploaded into this tree, so
`src/alghanem/arabic/maqayis_root_table_deposit.py` freezes their length and
digest and re-checks both on every read, and the figures the text named leave
the withheld register for `REDERIVED_SPECIFICATION_FIGURES`, each carrying the
counting rule that produced it: 4,576 records under a rule that a record is a CSV
row and not a file line; 36,597 lines under a rule that counts line separators in
the bytes, the file having no final separator so a `splitlines` rule yields 36,598
— two rules, not a contradiction; and 4,087 trilateral roots
under a rule that counts distinct `root_full` values and not rows (4,089 rows are
typed `ثلاثي`, two roots appearing twice). What that buys is re-derivability, not
vindication: a matching count shows the counter counted this file under this
rule, and each entry carries a written limit on what it still does not establish
— that this is the copy measured there, since the incoming text quoted no digest;
that a freeze identifier is issued; or anything about how many trilateral roots
Arabic has. The reason attached to the corpus counts is narrowed to what is
actually still missing — a `MeasurementRunManifest` and a written pre-measurement
expectation — rather than deleted, because a named corpus is not a performed
measurement, and those four counts are measured against the corpus rather than
against the root table. One arithmetic observation is recorded for a later
reader and decided by no one: the four counts sum to 78,081, while 78,215 appears
for the same corpus in the third record.

### A purity gate before any raw count, and a protocol that refuses quoted numbers

`src/alghanem/program/direct_certainty.py` encodes one governing rule: the
source of a claim never exempts it from being re-run. Prose from another
conversation, my own result in an earlier message, and an "obvious" mathematical
axiom are one genus here — `CertaintySourceGenus` gives exactly one member,
`RERUN_NOW_IN_THIS_PROCESS`, the property `supports_freeze`. The operational
test is coded rather than described: a `StepRecord` must name a module and a
callable, and `run_step` imports and calls them, so a step declared complete
without code that runs now fails at the first call
(`COMPLETION_IS_A_RUN_NOT_A_DECLARATION`). `ProtocolRun` refuses a skipped,
reordered, or repeated step, and `assess_freeze` returns an admissible freeze
only for six complete steps all re-run now, naming what is missing and what was
merely quoted as separate fields so neither hides the other.

The step that comes first is the one that used to come after. `DATA_PURITY_CHECK`
is step zero: no raw count may run over a text that has not passed a
contamination gate, and that gate is
`src/alghanem/arabic/encoding/contamination_gate.py`. It reads whitespace tokens
and reports one row per token — rejected rows kept, not subtracted — admitting
only a token built entirely from declared Arabic ranges and holding at least one
Arabic letter.

Why the filter is positive rather than negative is derived, not argued.
`derive_negative_filter_blind_spots` runs both filters over an embedded sample
and returns what the historical `[A-Za-z0-9]` filter admits and this gate
rejects: a decorative rule of `#` and `=` holds neither a Latin letter nor a
digit, and a lone stop mark is inside the Arabic block and is still not a word.
Neither shape is reachable by a filter that enumerates contamination; both are
reachable by one that names the single admitted shape. Separately,
`derive_head_tail_blind_spot` takes the same sample and returns the lines a
head-and-tail window does not read, so inspecting the first and last lines of a
file is recorded as a sample that may raise a suspicion and may not close one
(`HEAD_AND_TAIL_INSPECTION_IS_A_SAMPLE_NOT_A_GATE`).

The protocol is then applied to its own founding text. The figures that arrived
with it — the contaminated token count, the line number, what the first negative
filter stopped, and the classification rates before and after purification —
reached this tree as prose from another conversation, and no text is deposited
here that re-derives any of them. They are not accepted as measurements and they
are not deleted either: `REPORTED_UNVERIFIED_FIGURES` keeps each one with its
source genus and its constraint, because deleting a report hides it while
accepting one believes it (`RECORDING_IS_NOT_ENDORSING`). A figure that *was*
re-run now is refused entry to that register, so the quoted and the reproduced
never share a list. No purity rate is recorded anywhere: `PurityScan` requires a
digest, a byte length, a normalization form and a Unicode database version,
derives its counts by running the gate, holds no percentage field, and
`MEASURED_PURITY_SOURCES` is empty.

### A certainty ladder whose ceiling is derived, not announced

A five-rung ladder was put to this tree — bits ↔ number ↔ (carrier, state) ↔
vocalized text ↔ syntax ↔ meaning — with the first three marked "certain, 100%"
and the last two marked "not reached". Stopping short of meaning is right. The
line, however, was drawn one rung too high, and
`src/alghanem/program/certainty_ladder.py` derives where it actually falls.

`RungStanding` carries no member meaning *absolutely certain*. Every rung lands
in one of three genera instead: certain relative to a declaration, corpus-bounded
induction, or not reached with a counterexample in hand. These are different
kinds of reason, not points on a scale.

The third rung is the correction. "(carrier, state) ↔ vocalized text" is a
round-trip claim over a closed corpus, which is precisely the case
`CompleteInductionIsCorpusBounded` (`docs/CONSTITUTION.md`) was written for:
exhaustive enumeration over a closed finite set yields certainty inside that set
and conjecture beyond it. Enlarging the corpus does not lift that bound, because
the bound is on the genus of the inference, not on the sample size.

The first two rungs are certain only relative to declarations: the carrier set is
written down rather than derived (`CARRIER_SET_IS_DECLARED_NOT_DERIVED`), and the
bit correspondence rests on a declared width and order.

`derive_ladder_ceiling()` walks the rungs in order and halts at the first one not
reached, so the ceiling moves if any standing moves — it is never a number parked
somewhere else. None of the quoted figures (131/131, 100.0000% over 78,245 words,
28/28) is re-derivable here; they are filed in `REPORTED_UNVERIFIED_FIGURES` as
prose, while `derive_declared_carrier_state_product()` reports what this tree
actually declares, for comparison rather than substitution.

### Two outcomes and no third, so a comfortable middle result is unsayable

Section 7 of the direct-certainty protocol says every attempt to close a gap ends
in exactly one of two outcomes, and
`src/alghanem/program/binary_outcome.py` encodes that by leaving no third member
in the vocabulary: `GapClosureOutcome` has `TOTAL_CERTAINTY` and
`DEEPER_LAYER_REVEALED` and nothing else, so a comfortable mixed verdict is not
expressible rather than merely discouraged — the same move `RungStanding` makes
by carrying no member meaning *absolutely certain*. The two are a partition of
attempts, not points on a scale: revealing a deeper layer does not sit below
total certainty (`TWO_OUTCOMES_ARE_A_PARTITION_NOT_A_SCALE`).

Admission to the first outcome is computed, not asserted here.
`TotalCertaintyRecord` only constructs when bound to a `ProtocolRun` that
`assess_freeze` admits, so the certainty is relative to that run and its six
re-run steps rather than absolute
(`TOTAL_CERTAINTY_IS_RELATIVE_TO_ITS_BOUND_RUN`), and the dependency runs one
way only — this module reads `direct_certainty.py` and is never read by it. A
record carrying a declared exception that needs extra justification is refused at
construction, so "total certainty, except for…" cannot be written and then read
as certainty.

The second outcome is a successful diagnostic step recorded with the same clarity
as the first, not an apology for failure. `DeeperLayerRecord` refuses to exist
without naming what measurably narrowed the unknown — a contamination newly
named, a design shown to need rebuilding rather than extending, an unnoticed
fourth entangled class. An un-certain middle figure may not be left hanging:
once one is written down it must be classified by `MidFigureClassification` as
either a correct measurement of a wrong question or an incomplete measurement of
a right one, both of which are sub-genera of the second outcome. A classification
without a written figure is refused too, since it classifies something nobody can
read.

The evasive closing formulas the protocol names — "partial result", "a
preliminary signal needing more work", "close to the target" — are refused in
the reason fields against `REFUSED_CLOSING_PHRASES`, matched over text stripped
of diacritics. That is a shape check over a declared list and not a proof that no
evasive wording survives (`REFUSED_PHRASES_ARE_DECLARED_NOT_DERIVED`), stated in
the module with the same honesty the contamination gate applies to its own
declared ranges. `classify_attempt()` has no return path carrying "unclassified":
anything that is not one of the two records raises. The figures quoted in the
rule's own text — the 69.2% → 96.55% → 99.83% → "100%" escalation, the 69.57%
middle figure, and the total-certainty examples — arrived as prose and are filed
in the one existing `REPORTED_UNVERIFIED_FIGURES` register rather than a second
one, because two registers for one report split it.

### A step bound to code, so "something ran" cannot pass for "this step ran"

Encoding the two-outcome rule exposed a gap in the protocol module while
building its own examples, not while looking for it: `StepRecord` demands a
module name and a function name, `run_step` imports and calls them, and nothing
ties the callable to the step it claims. A `ProtocolRun` pointing all six steps
at a single contamination-gate function still freezes as `FROZEN_ADMISSIBLE`
today. `src/alghanem/program/step_reproducers.py` reads that binding instead of
asserting it: `STEP_REPRODUCERS` names, per step, which callables in this tree
actually perform it, and `assess_record_binding()` reports whether a record
points at its own step's code, at another step's code, or at something the
registry has not judged.

The third standing is an abstention, not a refusal. Reading absence from a
written registry as a refusal would let a declared list contradict correct code
that was simply never registered
(`ABSENCE_FROM_THE_REGISTRY_IS_NOT_A_REFUSAL`), and five of the six steps had
no code in this tree at all when that reading was filed — their emptiness is
readable, and their standing is derived from the empty row rather than written
into it. A second, unintended
narrowing surfaced from the same reading: `run_step` calls its target with no
arguments, so the protocol's practical test — "do you have the code that
produces it?" — narrows in practice to "do you have a zero-argument entry
point?". `derive_reproducers_run_step_cannot_call()` derives from the
signatures that `scan_lines` and `scan_tokens`, which *are* the purity gate,
fail that narrowing.

The finding is filed with the previous stage's own machinery rather than as
prose beside it: `STEP_BINDING_DISCOVERY` is a `DeeperLayerRecord`, so the
second outcome is used at the first place it occurred instead of being declared
and then left idle. This module is a reader and not a gate — it does not tighten
`assess_freeze`, is not imported by `direct_certainty.py`, and is read by no
gate in `kernel/` (`THIS_READER_IS_NOT_A_GATE`). A conforming binding says the
function is registered for that step; it does not say its output was correct or
that the step ran on the intended data
(`A_BOUND_STEP_IS_NOT_A_CORRECT_MEASUREMENT`).

### One empty row filled: a raw count of alif states on a deposited text

The first of those empty rows now holds code.
`src/alghanem/arabic/fatiha_source_text.py` deposits one short vocalized Arabic
text — al-Fātiḥa, seven lines — with its normal form checked at import and its
digest derived from the letters rather than written beside them. The requested
Uthmani edition (Tanzil Project) could not be reached from this environment, so
the deposit does not claim it: the letters are a transcription made in this tree
and collated against nothing, declared in a three-valued
`TranscriptionStanding` whose two higher members stay empty
(`A_TRANSCRIPTION_IS_NOT_AN_EDITION`, `RASM_IS_IMLAI_NOT_UTHMANI`).

`src/alghanem/arabic/alif_state_raw_count.py` writes the measured claim as text
before counting it (`ALIF_STATE_CLAIM`): that a `ا` carrier never holds one of
{fatḥa, ḍamma, kasra}, while other carriers do in real positions. It then
decomposes text into `(carrier, state)` atoms and keeps one row per occurrence,
marks that precede any carrier and codepoints that are neither carrier nor mark
included, so nothing is dropped before a reader sees it. Any alif that *does*
carry one of the three would be kept as a named row in
`alif_rows_carrying_a_short_vowel` rather than summarized away; on the deposited
transcription that field is empty, which is neither a proof nor a verdict
(`A_COUNT_IS_NOT_A_VERDICT`, `ONE_TEXT_IS_NOT_A_CORPUS`).

`count_alif_states()` takes any lines and knows no particular text; the
zero-argument entry point `run_raw_count_on_the_deposited_fatiha()` pins the
deposit, runs step zero (the contamination gate) first and refuses to count if
one token is rejected. That shape is deliberate: it is exactly the narrowing
`THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS` named, so the
entry point passes `derive_reproducers_run_step_cannot_call()` while the general
counter stays general. Only `DirectCertaintyStep.RAW_COUNT` was registered;
the other four rows stay empty and are asserted to stay empty, and
`assess_freeze` was not touched, so this reader is still not a gate. The
measurement itself is filed in the second-outcome machinery by
`derive_raw_count_record()`, whose figures are computed from a run rather than
written as constants, and classified as an incomplete measurement on a right
question.

### The second row filled: reading those rows before any condition is written

`src/alghanem/arabic/alif_carrier_inspection.py` fills
`DirectCertaintyStep.RAW_SAMPLE_INSPECTION`, and only that row. It reads the
table the raw count produced — it does not recount the text and does not touch
that module's code. For every alif carrier row it returns the context a human
reads a row by: the verse line, the ordinal position in that line, and the
immediate neighbour atoms on each side (an honest `None` at a line edge, never a
placeholder). All 23 rows come back, not a selection, which is why the module
names `FULL_SET_NOT_A_SAMPLE`: "sample" applies to the other half only.

That other half is the slice of non-alif carriers, chosen by a principle written
in code and carried on the record rather than explained in a comment —
`ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE`: the first vowel-carrying
non-alif row in each verse line, seven rows, the same on every run, every line
covered. A chosen slice is not a representative one
(`THE_SLICE_IS_CHOSEN_NOT_REPRESENTATIVE`).

The rows are read against `RASM_IS_IMLAI_NOT_UTHMANI` specifically. Each sample
carries a `RasmForm` field read from the characters of its own word — plain `ا`
or explicit waṣl `ٱ` — per row, never a summary count. On the deposited
transcription the explicit waṣla does not occur at all, and that absence is the
finding: `WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT` is filed as a named row,
conditionally on the measurement, so a deposit that did contain `ٱ` would not
file it. A count that never met the form the residual warns about is narrower
than it looks, and the narrowing is stated instead of being left inside a zero.
The residual itself stays open and unresolved, only better characterized
(`RASM_RESIDUAL_STAYS_OPEN`).

No record in the module has a verdict, status or pass/fail field; judgment stays
outside, as in the raw count. No exclusion condition was written
(`INSPECTION_WRITES_NO_CONDITION`) — `ONE_CONDITION_AT_A_TIME` and the two steps
after it stay empty and are asserted to stay empty, and `assess_freeze` was not
touched.

### A proposed grammar source checked before it was built on

A new syntactic source was proposed for later tree work — *النحو الواضح في
قواعد اللغة العربية* by علي الجارم ومصطفى أمين, reported as 421 numbered rules
across three parts, each with worked examples and exercises. The same discipline
that governed the QAC witness was applied first:
`src/alghanem/arabic/nahw_wadih_source_probe.py` is step zero and nothing after
it.

Five places were asked for the book, in the order written in
`PROBED_CANDIDATES`: the two Shamela hosts, ketabonline, an archive.org item's
metadata, and Hindawi — the last included so that a publisher who *does* state
an open licence is a recorded negative rather than an unexamined gap. None of
them opened: the host names themselves did not resolve from this environment, so
no page, no licence line and no byte was read. That is recorded as its own
standing, `UNREACHABLE_FROM_THIS_SANDBOX`, not as "unavailable" — the same
distinction `REQUESTED_EDITION_WAS_NOT_REACHED` drew for the Tanzil edition. A
page that was not opened may not be read as silent either: its licence standing
is `NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED`, and a candidate that claims a digest,
a text layer or a rule heading without an opened page is refused at
construction. What a search engine *said* about those licences arrived as prose
about pages nobody here opened, so it is not written down as a verbatim licence
string (`SECOND_HAND_LICENCE_REPORT_IS_NOT_A_READ_PAGE`).

The outcome is therefore **`SOURCE_LICENCE_UNRESOLVED`**, and it is computed
rather than declared: `derive_probe_outcome()` reads the rows, and licence
dominates order — if no candidate reaches an explicit open licence, the
structure standing is forced to `NOT_INSPECTED_LICENCE_BLOCKED_FIRST`, so an
"extractable structure" finding over a text of unresolved rights is not
expressible rather than merely discouraged. `GrammarSourceProbeOutcome` has
exactly three members and no fourth meaning "partially usable", on the pattern
`GapClosureOutcome` set. Rights-reserved and silence both block, and the first is
the stronger bar, not the weaker one
(`RIGHTS_RESERVED_IS_A_STRONGER_BAR_THAN_SILENCE`).

Two constraints are named before any extraction rather than after.
`A_DIGEST_IS_NOT_A_PERMISSION` separates the two moves that look alike: a hash
over bytes we may not redistribute is admissible as a pin — that is exactly the
QAC case — while lifting the book's 421 rule statements, or even "just the
headings", is a derivative of the text and is not deposited without a named
permission. And `A_RULE_STATEMENT_IS_NOT_A_DECISION_PROCEDURE` is filed now, at
step zero, so it cannot later be discovered as a surprise: a numbered rule states
a generalisation in prose (*الفاعل مرفوع دائمًا*) and carries no algorithmic test
for recognising when it applies to a token sequence, so "421 rules → 421 decision
nodes" is a conversion of a different genus and a larger size than depositing the
book's structure. Whether the source is usable at all is what this step asks;
whether a tree is buildable from it is not.

The wrong book is refused mechanically rather than remembered: *معاني النحو*
(السامرائي) is kept as `MAANI_AL_NAHW_REJECTED_WORK` with its rejection ground —
semantic-justification prose, no numbered rule spine — and a candidate naming it,
or any work other than the intended one, raises. The reported figures (421 rules,
3 parts) reached this tree as prose and are filed in the one existing
`REPORTED_UNVERIFIED_FIGURES` register, not stored as validated constants. The
question of whether the matn has fallen into the public domain by age in some
jurisdictions, while a particular modern printing has not, is recorded open as
`PUBLIC_DOMAIN_BY_AGE_IS_A_JURISDICTIONAL_QUESTION` and is not read as a
permission here.

Nothing follows in this step: no pre-registration, no extraction, no rule node,
no `DirectCertaintyStep` row, no import from `kernel/`
(`THIS_PROBE_IS_NOT_A_GATE`).

### Three laws registered, and the instrument that could not read the first one

Three laws arrived formally stated — ابتداء, وصل, وقف — together with a logical
derivation of منع التقاء الساكنين, a figure of **99.9974%** said to be measured
on the Quran, an exclusion named *after* that figure (لام الأمر الساكنة) said to
raise it to **100.0000%**, and a freeze identifier. Those are four different
genera and `src/alghanem/arabic/ibtida_wasl_waqf_registration.py` keeps them
apart instead of accepting them as one submission.

The laws themselves are registered with their words and their formal text, at
the lowest of three verification ranks: no book, author, edition or locus was
supplied, so `SuppliedLaw` **refuses construction** at either higher rank, which
makes the bottom rank a rank rather than a ceiling — the same shape
`fatiha_source_text` uses. The figures went where quoted figures go, into the
one existing `REPORTED_UNVERIFIED_FIGURES` register with their source genus and
constraint: this tree vendors no Quranic corpus, so 99.9974% is not re-derivable
here, and recording it is not endorsing it.

What *is* run is one small reading, on the only text deposited in this tree by
its letters, with a declared surface criterion: the written state of the first
carrier of each written word. It found **no position beginning with a written
sukun** in the deposited Fatiha — and that result is worth much less than it
looks, because of what the same run exposed. Of 29 positions only **15** are
decidable at all; the other **14** carry no written mark on their first carrier
and are recorded as `لا_حالة_مكتوبة`, never as compliant. Those fourteen are
precisely the hamzat-wasl positions — `الْحَمْدُ`, `اهْدِنَا`, `الصِّرَاطَ` —
and that is the finding that bears on the submitted figure:
`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`. The law's own escape
clause `IsHamzatWasl(a₁)` has **no surface test**; deciding it needs lexical or
morphological knowledge that the marks do not carry. So a reader that scores
this law on written words is either silently reading the unmarked carrier as
compliant, or it is using an identifier that was never declared. Either way the
instrument, not the law, is what the percentage measured.

The exclusion is treated the same way. It may well be a true description of
recitation — لام الأمر الساكنة does not begin a recitation — and it is still an
amendment made after seeing the number it repairs
(`EXCLUDING_A_COUNTEREXAMPLE_AFTER_THE_NUMBER_IS_AN_AMENDMENT`), the standing
that `ud_objecthood_amendment` was forced to declare in its own structure. Two
consequences are named rather than left implicit: the amended population is
defined by the very feature that produced the two counterexamples, so
100.0000% is derived from the definition and not from the text
(`THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_COUNTEREXAMPLES`); and a criterion
that can reclassify *any* counterexample as "not a real beginning" is no longer
falsifiable at all
(`AN_EXCLUSION_RULE_THAT_ADMITS_NO_COUNTEREXAMPLE_IS_NOT_MEASURABLE`). The
repair is not refused, only its order: the identifier of a non-beginning has to
be written **before** the next reading, so that the law keeps a position that
could refute it.

The derivation of منع التقاء الساكنين is neither measured nor contradicted here
(`THE_DERIVATION_IS_NOT_A_MEASUREMENT`). The adjacency scan finds zero pairs of
written sukuns in the deposited text, and that zero is explicitly not a
confirmation: a bare carrier and the first half of a geminate are both quiescent
in speech and carry no sukun mark
(`A_WRITTEN_SUKUN_IS_NOT_EVERY_QUIESCENCE`). A second shape — an unmarked
carrier before a geminate — is therefore reported so the positions are visible,
and running it exposed the scan's own limit in the same breath: the shape
catches the assimilated article lām of `اللَّهِ` alongside the madd alif of
`الضَّالِّينَ`, and separating them is again lexical knowledge the marks do not
hold (`THE_SHAPE_DOES_NOT_SEPARATE_THE_ARTICLE_LAM_FROM_THE_MADD_ALIF`). Its ten
rows are not ten madd positions, and the module says so rather than letting the
count be read that way.

The freeze is refused, and refused by derivation rather than by assertion:
`derive_submitted_freeze_standing` reads the source identity of what was
actually read, and a reading over a text deposited in this tree is not a reading
over the population the figure speaks about, however many rows it has. The
acceptance branch is reachable and stays reachable, so the refusal is
conditional rather than decorative. Wasl and waqf are registered with no reading
at all (`WASL_AND_WAQF_ARE_REGISTERED_WITHOUT_A_READING`): both speak about a
phonetic juncture or a stopping place, and written word boundaries do not
record either — which is the same confusion between «حدّ الكلمة المكتوبة»
and «موضع الابتداء الصوتيّ» that the submission itself named. The module issues
no birth, no verdict, no freeze, no `E0`, and imports neither `kernel/` nor the
program layer.

### A cited witness name, derived from the tree instead of taken from a report

An external reading of this tree found a place no earlier stage closed: a report
about this repository pointed at a test named `test_silent_overwrite_is_refused`,
which exists nowhere in the tree, while the witness that actually stands there is
named `test_a_second_write_over_a_read_state_is_refused_not_absorbed`. The
report's conclusion was correct and derived by running the tests — a second write
over an already-read state *is* refused — so the true conclusion carried the
fabricated name past inspection, and whoever believed the conclusion believed the
pointer with it.

`src/alghanem/program/witness_citation.py` judges the pointer rather than the
conclusion. `derive_witness_names()` parses a file with `ast` and returns the
witness names written in it, so a test file need not be importable for its names
to be read and nothing in it is executed to read them; a path outside the tree is
refused rather than read. `cite_witness()` returns one of three standings —
derived from the named file, absent from it, or the file is not in the tree — and
the third is kept separate because "this name is missing from a file that does
not exist" judges the wrong thing. For the same reason a missing file returns
`None` while an existing file with no witnesses returns an empty tuple.

Each `WitnessCitation` carries the derived names beside its standing and is
refused at construction if the two disagree, because a verdict without what it
was derived from has to be believed again on someone's word — the very defect the
row exists for. `audit_report_citations()` returns one row per citation and
deliberately returns no aggregate "accepted/refused" word, since that word would
itself be quoted onward. The incident is filed with the previous stage's
machinery, as `FABRICATED_WITNESS_NAME_DISCOVERY`, a `DeeperLayerRecord` naming
both the fabricated and the real name.

This module is a reader and not a gate: it does not tighten `assess_freeze`, is
not imported by `direct_certainty.py`, and is read by no gate in `kernel/`
(`CITATION_READER_IS_NOT_A_GATE`). A derived name says a function with that name
is written in that file; it does not say the test is collected, that it passes,
or that it checks what the report claimed
(`A_DERIVED_NAME_IS_NOT_A_PASSING_TEST`). The judgement is on the (name, file)
pair, so a refused citation is not a claim that the name is absent from the tree
(`ABSENCE_IN_ONE_FILE_IS_NOT_ABSENCE_IN_THE_TREE`), and the pair still arrives
from whoever wrote the report, so a report that stays silent about a witness
contradicting it is not exposed here
(`THE_CITED_PAIR_IS_STILL_SUPPLIED_BY_THE_REPORTER`).

### Reading this README instead of trusting it

The tree already had a reader for `docs/CONSTITUTION.md`, another for
`docs/AIMS.md`, and a third mapping the milestone sections of that document onto
the modules they claim. This file was the last declaring document with no reader
at all, so every achievement announced here was accepted because it was written.
`src/alghanem/program/achievement_ledger.py` closes that: it derives the
achievement claims out of this text rather than reading them by eye.

A claim is read by one written shape and never by estimated meaning: a gate
identifier, then prose carrying no code span and no parenthesis, then the
module path in a parenthesised code span. Seven claims are read that way today,
and every other mention of a gate identifier is a mention rather than a claim.
Estimating a claim from a nearby path instead would attach a surface
intervention module to one gate and a content-identity module to another, both
wrongly, so the boundary is written into the reader and named rather than left
to judgement.

Naming a path that happens to exist proves only that a string was written
twice. Each claimed module is therefore imported, and the symbols the prose
names inside the claim's span are matched against what that module actually
carries; a claim with no resident symbol at all is refused by gate id and line
number. The witness is derived from the tree's own convention —
`src/alghanem/X/Y.py` is witnessed by `tests/X/test_Y.py` — and its standing has
three members, not two: derived and present, registered elsewhere, or not
registered at all, the last being an abstention rather than a refusal.

The three-way correspondence between this file and the constitution found
something that was not known before: `P0.1`, announced above as freezing
measurement authority, is named nowhere in `docs/CONSTITUTION.md`. Refusal runs
in one direction only, and that asymmetry is derived rather than polite: a gate
that *claims a module* without a constitutional row is refused at construction,
while a gate merely mentioned — which is what `P0.1` is — is recorded under a
named standing, because raising it to a refusal would oblige a read-only ledger
to edit the constitution. Gates heading constitutional sections without a
mention here are enumerated under a third standing of their own, so nothing
falls silently on either side.

Two standing gaps are now counted rather than assumed away. The scripts under
`examples/` that no test calls are recorded as declared-but-not-reproduced —
all of them until `examples/kernel/license_transitions.py` and
`examples/arabic/rederive_gflk_witnesses.py` each arrived with a witness that
loads and runs it, leaving those two alone in the other standing — and the two
skipped tests are classified into two declared genera —
conditional on an undeposited input, and a case inapplicable by construction —
with any third skip form refused by file and line, since a skip whose genus is
unnamed is counted as a pass and is not one. What stays open is named:
`getattr` sees an imported symbol exactly as it sees a defined one, a witness
file that collects is not a witness that checks this claim, and a test that
mentions an example script does not thereby run it.

The first hypothesis in this tree that arrived already formalised from outside
is the fractal licensed-transition claim: that one transition structure
`K = (Carrier, Gate, Operation, Identity, Evidence, Residual, Trace, Closure)`
survives a change of linguistic scale. The intent was to freeze its text
verbatim, preregister the ten items it demands before anything was measured,
and only then read. The ordering held — the preregistration was committed in
its own commit while no readout module existed yet, because the text's own
`PostHocSimilarity != FractalEvidence` rule cannot be honoured by a promise —
but the freeze itself did not. Direct inspection found that the deposited text
diverges from the supplied one at the site that decides the success condition:
the requested text puts an explicit order relation between `StructureMatch` and
`BestWeakerReconstruction`, and the deposited text carries no relation there,
while the module declares in the same breath that notation is part of the
frozen text. So the digest attests a different hypothesis, and the run's
standing is `INVALID_PREREGISTRATION`.

That is recorded, not repaired. The divergent text is left exactly as it is,
because fixing it would erase the only evidence of the defect, and
`src/alghanem/arabic/fractal_transition_calibration.py` derives the divergence
from the deposited text rather than asserting it, withholds the verdict from
being attributed to the requested hypothesis, and states the instrument's
capability envelope: reachable are `REFUTED`, `UNDERPOWERED` and
`WEAKER_MODEL_RECONSTRUCTS`; unreachable by construction is `SUPPORTED`, since
every ladder name occurs in the frozen text and no declared pair can be a
holdout. An instrument that can refute and cannot support is a refutation
instrument, not a balanced test, and it is named as one.

The reading itself is carried whole. On `syllable-to-word` the transported
structure agreed in 24 of 30 field/case comparisons and a constant model that
reads nothing agreed in 28; two further pairs were `UNDERPOWERED` by
declaration, their upper layers having no coded carrier here. But the more
useful half of the result is what the instrument revealed about itself: in the
present encoders Trace and Closure are true by construction and Gate and
Residual are one predicate under two names, so four of six compared fields
cannot discriminate anything; what is being compared is boolean agreement
between two encoders on one surface, not `S ∘ K_n ≅ K_m ∘ S`, because no
independent scale-transport contract exists; and `Identity` is a boolean from
an encoder that never passes the invariant gate, so
`DeclaredInvariant != VerifiedInvariant` applies to it. The machine found the
defects of the test before it could find anything about Arabic, and 24 against
28 is therefore not a refutation of the claim.

The successor is declared by name and not executed. `G0.FLT-1` needs a newly
frozen text checked site by site, a real independent `S`, scales that were not
used to formulate `K`, a signature whose fields can read false, a verified
`Identity`, and inputs unread in `G0.FLT-0`; repairing the criterion and
re-running the same five surfaces would not be prospective. The laws are
collected in `docs/CONSTITUTION.md` under `G0.FLT-0`.

The successor is now frozen. `G0.FLT-1` asks whether a licensed Carrier/State
centre generates syllabic closure better than every weaker representation, and
it is deposited as text and registration only — no readout module exists in this
branch, because a reading built alongside its own preregistration cannot testify
to the order in which they were written. The chain under test runs from carrier
to a Carrier/State centre, through a licensed join and a closure, to a higher
centre, and it is registered as six hypotheses that fail separately: the two
quotients, their predicted product, birth under an opening vowel with its
negative control, closure under sukūn, and the higher centre itself. `28 × 4` is
a prediction and never an input; the equivalence relation is declared first and
counted afterwards.

Two corrections to `G0.FLT-0` are built in. Verbatim fidelity is checked rather
than promised: fourteen decisive notation sites are enumerated and their
presence derived from the deposited text at import, which is exactly the check
whose absence invalidated the previous registration. And the negative controls
are the experiment rather than its margin — the carrier alone, the state alone,
and the unordered pair are run on the same surfaces, and a tie is enough to
defeat the claim that the licensed pair is the lower centre. The name "higher
centre" is earned only by Reconstruction, Minimality, NoBypass and Closure
together; `Identity` counts only if verified, otherwise the pair is
`UNDERPOWERED`; and the seven frozen surfaces are disjoint from the five already
read, checked at import. The laws are in `docs/CONSTITUTION.md` under
`G0.FLT-1`.

`G0.FLT-1.Q` then corrected the law itself before running it. The frozen chain
treated every transition as a move upward; the correction adds a licensed
*qiyās* between an origin and a candidate branch, with the *qādiḥ* difference
**tested** rather than required: `Q(O,F) = Sh ∧ Sb ∧ ¬Mn ∧ I ∧ w* ∧ μ ∧ ¬Δq`.
Absence of the difference is continuity under the origin, presence with a shown
effect opens an independent branch, and presence without a shown effect is a
formal difference only. The earlier text was superseded rather than edited — it
keeps its letter and its digest, and the supersession record states why the
exchange was licensed: nothing had been read from it yet. The same commit
ordering was repeated, the new text and machine landing before the readout
existed.

The run is recorded as it came out, and no surface earned the name "higher
centre". Nine of eighteen branches read as continuity and nine as
independent-branch candidates. `فَتَحَ` lost `NoBypass` outright, because the
no-join path reproduces `CV-CV-CV` exactly and the join is ornament there;
`بَابٌ` lost `Reconstruction` and `Closure` together, because the madd seat
enters no syllable. The rest are `UNDERPOWERED`, since the reconstruction target
comes from the same reader that embodies the licensed model — so a tie by a
weaker representation would refute the claim, while the licensed model's win
proves nothing. `w*` and `μ` held everywhere and are reported as analytic in
this deposit rather than counted as evidence, and the five decision outcomes the
corpus never triggered are listed as untested.

## Development

The first measurement in this tree against an *externally* annotated corpus is
`src/alghanem/arabic/irab_case_readout.py`. A claim arrived here that a word
following a perfect verb and ending in *fatḥa* is a direct object, at "100%"
accuracy; that figure was an artefact of a harness comparing its own expected
string against itself, and a later hand-check reported 48% without measuring
against any annotated source. Run as stated against the Quranic Arabic Corpus
(morphology 0.4, attributed and digest-pinned in
`src/alghanem/arabic/irab_corpus_witness.py`, bytes deliberately not vendored),
it scores **33.9%**.

After fixing four defects the corpus itself exposed — the final vowel belonging
to an attached pronoun, a bound preposition, the alif of accusative *tanwīn*
read as a *maqṣūr* ending, and shadda/fatḥa byte order closed by NFC — a
surface reader recovers the *case* marking at **97.1%** on a held-out split
(odd-numbered suras; rules were developed on the even-numbered half, whose
97.4% is recorded beside it so the fitting gap is visible). Shapes with no
visible case mark are a third outcome, `متعذّر_القياس`, never counted as wrong.

That is a weaker claim than the one that arrived: the corpus annotates *case*,
not syntactic function, and the accusative also carries ḥāl, tamyīz, ẓarf and
the noun of `inna`, so `ACCUSATIVE_IS_NOT_OBJECTHOOD` stays an open residual and
97.1% is not an answer to the original hypothesis. That hypothesis has since
been measured on its own terms, against the syntactic function annotated in
`ar_padt-ud-test`, and it falls at 35.8%; the case reading above is unaffected
by that fall. Every frozen number is
re-derived, not asserted: `examples/irab/measure_case_readout.py` verifies the
corpus digest and recomputes them, exiting non-zero on any drift.

### Naming what a refusal is, and what a state rests on

`src/alghanem/arabic/encoding/state_evidence.py` does two things to the
deposited codec without editing one byte of it.

It **names what is already there**. `carrier_state_candidate` refuses at
construction in thirty places, and each refusal belongs to a different classical
genus, and none carried the name of its genus. The sites are read out of that
module's own abstract syntax tree by `derive_refusal_sites`, never from a
hand-written list, and classified into a closed triad: **condition** (a positive
constraint on the input, sixteen sites), **preventer** (a structure present that
blocks a judgement whose condition is met, twelve), and **undecidable** (a place
where the marks settle nothing, so the refusal is an abstention rather than a
verdict, two — both of them a second write into a slot already derived once).
Adding a refusal without a genus, or removing one that is classified, fails at
import rather than passing with a warning
(`CLASSIFICATION_READS_THE_DEPOSITED_MODULE_AND_DOES_NOT_AMEND_IT`).

It **fills the one gap that probing found**. The codec produces `الحمد` as five
`SUKUN_IMPLICIT` units while the surface writes no mark at all, so an assumed
state and a read one were the same value. `StateEvidence` separates them, and a
`CarrierStateUnit` is not wrapped without the genus of the sign it rests on:
`WRITTEN_MARK` names the mark and its offset, `ABSENCE_ASSUMPTION` is named for
what the codec actually does rather than for an underlying sukun it cannot see
(`ABSENCE_ASSUMPTION_IS_NAMED_FOR_THE_CODE_NOT_FOR_A_LINGUISTIC_CLAIM`), and
`UNDECIDABLE` is reported for an unmarked alef opening a run of carriers. That
last one settles a disagreement between two modules of this tree:
`ibtida_wasl_waqf_registration` records such an alef as unmeasurable
(`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`) while the codec asserted
sukun. Nothing is declared undecidable for the alef as such — a written wasla
`ٱ` is not undecidable, because whoever wrote it decided
(`UNDECIDABILITY_IS_DERIVED_FROM_THE_SURFACE_NOT_DECLARED_FOR_THE_ALEF`).

`MarkObservation` records a codepoint at an offset and carries no state, and the
two genera stay apart by derivation rather than by wording: `بَُ` yields two
observations and zero units, since the codec refuses it
(`AN_OBSERVED_MARK_IS_NOT_A_DERIVED_STATE`). Offsets are derived by writing each
prefix back through the deposited codec, so no second mark reader exists to
disagree with the first; the reader checks that what it wrote is a prefix of the
surface instead of assuming it. Two defects were found by probing the module's
own rules rather than by reasoning about them: `retrieve` emits shadda before
harakah while NFC orders them the other way, which pointed nine of forty-six
offsets at the wrong codepoint until the written prefix was normalized before
being diffed; and a tatweel is a passthrough that *joins*, so it opened a new
word and made a mid-word alef undecidable until `DECLARED_JOINERS` was named. A
boundary here is a passthrough, never a lexical fact, and the joiner set is
declared and derived from no property of Arabic
(`A_WORD_BOUNDARY_HERE_IS_A_PASSTHROUGH_AND_NOT_A_LEXICAL_BOUNDARY`).

Capacities are derived and never tabulated: `derive_observed_capacities` reports
which marks actually fell on which carriers in the surfaces it was handed, and a
pair no surface exhibits is recorded as unobserved and never as impossible
(`ABSENCE_OF_A_WITNESS_IS_NOT_A_WITNESS_OF_ABSENCE`). Three things are
deliberately absent with their reasons written down: no essence of a letter,
since identity in this tree is deferred to a birth gate that is not built
(`LETTER_EXISTENCE_HERE_IS_OBSERVED_NOT_ESSENTIAL`); no declared relation table,
which would owe the separation `letter_fingerprint` applies to its imported
tables (`NO_RELATION_TABLE_IS_DECLARED_HERE`); and no efficient cause, which is
omitted as a recorded decision that stays open to challenge rather than absorbed
into the existence of the letter and passed over
(`EFFICIENT_CAUSE_IS_OMITTED_BY_DECISION_NOT_BY_SILENCE`).
`examples/state_evidence/read_state_evidence.py` prints the genus of every state
of any surface passed to it. Nothing here is born, ranked or frozen, and no gate
in `kernel/` reads it.

`compression_model_preregistration` freezes a compression measurement before it
is taken: the bytes it may be taken on (a length and a SHA-256, not a vendored
copy), the declared table representation, the first-symbol context, and two
*total* tie-break rules. The measurement itself lives in
`compression_model_measurement`, and three things about it are structural
rather than advisory. Its input is raw bytes whose length and digest are
checked before they are decoded, never an intermediate representation — the
first version of this measurement was arithmetically correct on a rebuilt
representation that had silently dropped the ḥarakāt, so it reported 36 symbols
where the bytes hold 51 and an alphabet is now counted from the bytes rather
than declared (`MEASUREMENT_IS_BOUND_TO_BYTES_NOT_TO_A_REPRESENTATION`). A
byte-identical round trip is a precondition of issuing any figure at all, not a
line in the report: `ModelMeasurement` refuses construction without it, so
there is no path in the module that emits a ratio for an encoding that was
never decoded back (`ROUND_TRIP_IS_A_PRECONDITION_OF_ISSUANCE`). And two sizes
are emitted or none — the encoded payload and the total that is actually
decodable from scratch with its tables — because a payload figure presented as
a file size is a size that cannot be decoded without knowledge it never
counted (`TWO_SIZES_OR_NONE`).

The tie-break is declared because the table is not invariant, and this cuts the
opposite way from the obvious guess: Huffman's cost is optimal and therefore
numerically unique however many optimal trees exist, so the payload figures are
reproducible byte-for-byte under any rule, while the *sum of code lengths* —
and with it the table — differs between equal-cost trees. Canonical coding does
not close that, since it fixes the code given the lengths and not the length
multiset. `MINIMAL_TABLE` (frequency, then shallower subtree, then fewer
leaves, then smallest codepoint) is total and leaves no tie, and preferring the
shallower subtree minimises the sum of lengths, so it never yields a larger
table than the simpler rule. On the frozen corpus the measured figures are
68.8837% and 68.8674% at order zero, and 78.7818% payload with **78.5774%
total** at order one, against zlib -9 at 80.5551% quoted as an external ceiling
and not as a model from this layer. `compression_model_revision_audit` keeps
the superseded figures on the record with the defect and the closure for each —
44.85%/50.03%, the bare 78.78%, the estimated 78.45% — because erasing a wrong
number hides the lesson and leaves the door it came through open. A compression
ratio here is a re-derivable number about bytes and never a linguistic claim
(`A_COMPRESSION_RATIO_IS_NOT_A_LINGUISTIC_CLAIM`); nothing is born, ranked or
frozen as evidence, and no gate in `kernel/` reads it.
`examples/compression/measure_compression_model.py` re-derives every frozen
figure from a copy of the bytes and exits non-zero on any drift.

`hollow_root_levels_preregistration` freezes twenty-four hand-built hollow-root
surfaces and four named projections before a single measuring function was
written, and guards the set with a re-derived digest. `hollow_root_levels_measurement`
then reads the ladder with the tree's own frozen readers — `text_key.comparison_key`,
`p_extractor.read_surface`, `syllabifier.syllabify_surface` — and finds
collisions by *grouping* surfaces under a shared fingerprint rather than by
comparing each surface against the previous one
(`A_COLLISION_IS_FOUND_BY_GROUPING_NOT_BY_PAIRWISE_COMPARISON`); a detector that
requires the states to *differ* before reporting a collision hides the total
collision, which is the strongest one, not the weakest
(`A_TOTAL_COLLISION_IS_THE_STRONGEST_ONE_NOT_THE_INVISIBLE_ONE`). Two incoming
claims invert under this reading. The claim that a "root skeleton" collapses
قَالَ and قُلْ holds only under the projection that also drops the madd carrier,
not under `comparison_key`, and the projection was never named. The claim that
template-plus-vowel-state "resolves the surface form completely with not one
collision" is a property of the four-form sample, not of the fingerprint: on the
frozen twenty-four, six collision classes collapse them to ten fingerprints, the
strongest being قَوْلٌ/بَيْعٌ/خَوْفٌ/نَوْمٌ, identical in template and state
although و and ي are visible in the orthography. The ladder is also not
monotone: distinct fingerprints fall 23 → 18 → 5 → 10 as the levels advance, so
the order is one of naming, not of increasing resolution
(`A_LATER_LEVEL_IS_NOT_NECESSARILY_A_FINER_ONE`). The surviving level-3 claim is
bounded — يَخَافُ (waw) and يَهَابُ (ya) share one fingerprint exactly, a limit
`docs/reference/gflk_arabic_letter_specification.md` had already recorded before
the claim arrived. `hollow_root_levels_deposit` records all of this without a
resolution field, along with the three files whose declared digests were quoted
but whose bytes never reached this tree
(`THE_BYTES_NEVER_REACHED_THIS_TREE`) — only the quoted digest *prefixes* are
stored, since completing a digest from anywhere but its source is invention, not
transcription (`A_QUOTED_DIGEST_PREFIX_IS_NOT_A_DIGEST`). Every corpus-derived
figure is filed as not re-derivable here, because no corpus file exists in this
tree. The independent convergences are recorded too, each with what it does not
establish. Nothing is born, ranked or frozen as evidence, and no module in
`kernel/` reads any of it.

One of those conflicts named a condition rather than a defeat: resolving the
weak radical by matching a consonantal skeleton against the root table is
circular, since `خيف`, `نيم`, `هوب` and `قيل` are separate entries there
alongside `خوف`, `نوم`, `هيب` and `قول`, so the skeleton returns both. The
condition written before any witness arrived was "a fingerprinted witness
outside the surface form". `hollow_root_root_census` is that witness put to
work: the `ROOT` feature of the Quranic Arabic Corpus morphology file, tagged
word by word by others before this question was asked, bound to the digest and
byte length already frozen in `irab_corpus_witness`. Counting under three named
rules — segments, words, verses, since 124 without its rule is not a number —
one side of every competing pair is untagged in that corpus: خوف 124 against
خيف 0, نوم 9 against نيم 0, قول 1,722 against قيل 2, and هوب/هيب both 0, over
128,219 morphological segments. The numbers arrived declared *before* the count
was run here and matched exactly, which makes the match predictive rather than
fitted (`THE_NUMBERS_ARRIVED_BEFORE_THE_RUN`). The two قيل occurrences were
examined individually and are not mistagged قول: (7:4:10:1) قَآئِلُونَ and
(25:24:7:1) مَقِيلًا carry lemmas `qaA^}iluwn` and `maqiyl`, the midday-rest
root, distinguished in the bytes themselves. The zero for هوب/هيب confirms what
`hollow_root_levels_preregistration` already declared: يَهَابُ was a
hand-built example, never an observed corpus form, so it is neither deleted nor
promoted. What this does *not* establish is named as loudly: a tagged root is a
human judgement, not a measurement, so a zero means "untagged in this corpus",
not "absent from Arabic"; and the census is not a root extractor — the
circularity loses its live alternative *inside this corpus*, which is not the
same as a rule from surface form to root (`THE_CENSUS_IS_NOT_A_ROOT_EXTRACTOR`).
Accordingly the recorded conflict's `tree_reference` and
`what_would_resolve_it` now point at the census and its re-derivation script,
while its standing stays `THE_TREE_CANNOT_TEST_IT`: changing a rank is a
separate, deliberate decision, never a side effect of depositing numbers. The
corpus bytes are still not vendored — permission to copy them under its GPL
licence and the CC BY-ND Tanzil text it embeds has not been examined here — so
the re-derivation runs at the holder of
the bytes via `examples/irab/measure_hollow_root_census.py`, and no number
passes before the digest and length match.

### Four transitivity results kept, and fifteen arriving numbers that failed

A second claim arrived against the same fingerprinted corpus: that roots whose
bare perfect is never tagged passive are intransitive candidates, that they
differ sharply from confirmed transitives in the passive participle, and that
"an intransitive becomes transitive by augmentation" is refuted as a rule.
`transitivity_probe_preregistration` freezes the rules before the numbers —
both classification rules rest on *absences* read from the schema, since this
corpus tags neither `ACT` on active verbs nor `(I)` on form I, so an active
verb is one without `PASS` and a bare verb is one without a form tag; a reader
who demanded the positive tags would report zero active verbs in the Qurʾān.
It also freezes the permutation protocol with its seed, and states before any
figure that a permutation *p* has a floor of `1/5001` rather than reaching
`0.0000`, and that the passive-participle test is **not independent of its own
definition**: the groups were defined by the presence and absence of the
passive, and the passive participle is a passive form.
`transitivity_corpus_census` then re-derives, at the holder of the bytes via
`examples/irab/measure_transitivity_census.py`: 1,642 tagged roots, 398 with a
bare active perfect, splitting into 68 confirmed transitive and 330
intransitive candidates; 48 roots carry a bare imperfect passive with no bare
perfect passive against 34 with both, so one tense is not the voice of a root;
the passive participle stands at 44.1% against 17.0%, a 27.15-point gap with
`p = 1/5001`; and the augmentation hypothesis is refuted as a rule from two
directions at once — 13.3% of intransitive candidates against 14.7% of
transitives, a difference that is not significant (`p ≈ 0.85`) — while
surviving as a possibility in named, located forms (علم → II at (6:91:31:2),
عود → IV at (22:22:8:1), حفظ → X at (5:44:17:1)). Two things are recorded
against the arriving text rather than smoothed over. First, **none of its
fifteen figures re-derived**: 1,532 against 1,642, 67/312 against 68/330,
46/35 against 48/34, 27.47 against 27.15, 18.40 against 20.05. The rule was
not tuned until they matched; the divergence table is printed by the script
and frozen in `ARRIVING_FIGURE_DIVERGENCES`, and what survived is the
*direction* of two results, not their arithmetic. Second, its criterion
"the gap exceeds the maximum null gap" is shown to drop a real effect: the
active-participle gap of 21.07 points falls *below* the maximum null gap of
24.62 and is nevertheless significant at `p = 0.0012`. What was never measured
is left without a number rather than with a zero — the maṣdar, the
morphological noun of place and of time, the noun of instrument, and tamyīz
are not tagged in this corpus at all, and `POS:LOC` and `POS:T` are syntactic
adverbials, not morphological patterns, so any figure about them from these
bytes would be fabricated. The corpus bytes remain unvendored.

### An independent lāzim/mutaʿaddin witness, deposited fingerprinted

The reservation above — that the passive-participle test shares a parent with
the definition it tests — needs a witness authored outside this question, and
`transitivity_lexicon_witness` deposits one: the trilateral verb table carried
by Qutrub and Arramooz Alwaseet, whose transitivity mark is a **stated lexical
judgement**, not a morphological derivation. Its bytes were opened at two
mirrors — `linuxscout/arramooz/data/verbs/triverbtable.py` and
`linuxscout/qutrub/libqutrub/triverbtable.py` — and both returned the same
SHA-256 `75fc716f…aa7d8a` at 846,066 bytes, which proves the mirrors do not
differ and does *not* make them two witnesses. The manual CSV the table is
generated from is deposited beside it (`e54cb3fe…bd970`, 580,755 bytes) as
provenance, with it recorded that the transitivity judgement is **not a column
in it**. The meaning of the three marks is taken from upstream's own code
rather than guessed: `libqutrub/verb_db.py` reads mīm and kāf as transitive and
lām as intransitive, with kāf common to both. Re-derived at the holder of the
bytes via `examples/irab/measure_transitivity_lexicon.py`, which reads the file
as text and never executes it: 7,953 entries, 6,909 distinct verbs, 5,196
distinct trilateral roots; 3,656 lām, 2,977 kāf, 1,320 mīm; and at root level
1,587 roots marked intransitive only against 3,609 with at least one transitive
or common reading. What is deliberately **not** done is the join: the Quranic
roots are written in 28 Buckwalter ASCII characters and these in 29 Arabic ones
(with hamza appearing both bare and seated), so their literal intersection with
the 398 partitioned roots is **zero, measured**. Bridging them requires a
transliteration table and a hamza-unification decision, and both are rules that
would be legislated, not readings that can be taken; so this unit stops at the
deposit and the census, and issues no figure about agreement between the two
sources. Nor does the table speak to augmented forms or quadriliterals: every
root in it is trilateral. The table's bytes remain unvendored; its GPL requires
attribution to T. Zerrouki, with verb data collected by M. Kebdani.

The next unit measures **hamzat al-waṣl in the bare imperative by root shape**
on the same fingerprinted bytes, and it begins with a correction to the frame
it arrived in: SHA-256 has **no order-preserving property whatever**. The
avalanche effect makes two adjacent inputs produce two unrelated digests, so a
digest can be "followed up and down" in no sense at all; it fixes identity, not
order. The ordering work that *was* done earlier in this tree was over Unicode
code points, which do order, and that remains untouched. The specification
(`src/alghanem/arabic/imperative_wasla_specification.py`, digest
`994d8b9e…6e23`) is marked `مُصاغة_بعد_الرقم` — **formulated after the number**
— because it was: the bytes were read first and the rules written afterwards,
and saying so is cheaper than pretending otherwise. It therefore freezes
**four** competing definitions of the weak radical rather than one, because the
result depends on the choice and hiding the choice would hide the result: waw
and yāʾ alone, or waw and yāʾ and hamza; and with the doubled root left inside
the sound class or separated out of it. Across all 1,181 bare imperative
segments (all trilateral; the corpus has no quadriliteral bare imperative), one
thing is **invariant under every rule**: the hollow root takes hamzat al-waṣl
in **zero** positions — 0/425 under the narrowest rule, 0/445 under the widest
— and the assimilated root is near it. What is **not** invariant is the number
quoted for the sound root: it moves from 510/604 = 84.4% to 493/493 = 100.0%
purely by changing the rule. The arriving figure of 96.9% appears under none of
the four, and of seventeen arriving figures only two re-derived: lafīf 14/44,
and the count of one nāqiṣ exception. The sample size 838 was 938; the mithāl
0/52 was 1/99; 217/258 roots was 116/149. The arriving table is reproducible
only if **hamza is counted as a weak letter**, which conflates المهموز with
المعتلّ — so the whole pattern rests on an undeclared rule, which is why all
four are now declared. The claimed `p = 0.0000` is **arithmetically
impossible**: a permutation p-value over 5,000 permutations has a hard floor of
1/5001 = 0.0002, which is what both tests return (gap 84.44 and 100.00 points,
zero null draws as extreme, maximum null gap ~11.2). The strongest finding was
not in the arriving table at all: the fourteen sound-class exceptions turn out
to be, **without a single exception, doubled roots** — and inside that one
class the proposed mechanism can be tested *within* a group rather than
correlated *between* two groups. It holds 21 of 22: where the gemination is
assimilated the waṣl is absent 13/13, where it is broken the waṣl is present
8/8. The one disagreement is 33:33 `qaro` — the classically contested form,
where QAC's own tagging is internally inconsistent (tagged bare while its lemma
`taqar~a` is form V) — and the single nāqiṣ exception is 2:186 `daEa`, tagged
IMPV but commonly read as a perfect with nūn al-wiqāya. Both are recorded as
named residual positions rather than corrected into agreement. The claim that
the imperfect is a precondition of the imperative is **neither proved nor
refuted here**: 116 of 149 imperative roots have a bare imperfect and 33 do
not, but a bounded corpus yields absence of evidence, not evidence of absence,
and that limit is written into the module instead of being argued around.
Re-derived by `examples/irab/measure_imperative_wasla.py`.

A second table then arrived for the same question — sound 481 at 86%, nāqiṣ 100
at 99%, hollow 401 at zero, mithāl 16 at zero, split lafīf 6 at zero — and it
is recorded as **divergence, not as a second measurement**
(`SECOND_ARRIVING_SHAPE_FIGURES`): the frozen specification and its digest were
not touched, because the tree's rule is that a rule is never tuned until it
matches an arriving number. Of its ten figures **two re-derived**, and both are
zeros: the hollow root's zero waṣl, which holds under all four rules, and the
mithāl's zero, which holds under the two narrow ones. The counts themselves do
not: 481 against 604, 100 against 107, 401 against 425–445, 16 against 38–99.
The gap is unexplained because the arriving table never declared its **scope** —
bare imperative only, or the imperative in every form; and from which corpus —
and the same undeclared scope is the likeliest reason 217/258 stands against
the re-derived 116/149. "Split lafīf" is not a class in `RootShape` at all:
separating it is a **fifth rule that would have to be legislated**, and
legislating it after seeing its number would be legislating to the number, so
the figure 6 is recorded as **not re-derivable under the frozen rules** rather
than made re-derivable by a new door. The reservation attached to the arriving
result 1 — absence in a corpus is not absence in the language — was already
written in the module and stays.

The third arriving result, **"the maṣdar comes first"**, is genuinely new to
this tree, and it is the one that **could not be measured at all**. Its corpus,
MASAQ.csv, arrived as a digest (`d43d2a81…6f3a`) and nothing else. A digest
alone is not a deposit: `IrabCorpusWitness` also requires the byte length, the
mirror that was actually opened, the licence and its attribution condition, and
none of those were given — so `MASAQ_CORPUS_WITNESS` is **`None`**, with two
open barriers naming exactly what would lift it
(`src/alghanem/arabic/masaq_corpus_witness.py`). The column names are likewise
**not guessed**: `MasaqColumnBinding` must be declared by whoever holds the
bytes and is digested into every figure it produces, because which column
carries the tag is a decision, not a reading. The hypothesis is nevertheless
pre-registered and frozen (digest `6e042d75…e213c`, standing
`مُصاغة_بعد_الرقم`), with its three claims separately falsifiable — the maṣdar
distinguishes the form where the verb is shared; it separates senses that the
root identity merges; it reveals a transitivity the passive misses — and with a
permutation protocol fixed before any number. The census
(`masdar_priority_census.py`) carries the pipeline and **zero re-derived
figures**: standing `لم_تُفتَح_البايتات`, six arriving figures with no
re-derivation. Four named residuals bound what the result could have meant even
if measured. A `GERUND` tag is a **human annotator's judgement, not a property
measured from bytes**. **One root is not a corpus**: قوم with its four
distinct maṣdars (قيام، إقامة/إقام، تقويم، مقام) is a witness of possibility,
not a corpus rate, and a single root cannot overturn the order of a structure.
A present maṣdar is **not a measured transitivity**: moving from "إقامة is
tagged" to "أقام is transitive" needs a rule joining maṣdar to transitivity,
and no such rule has been legislated, so `transitivity_from_masdar` **raises
instead of returning a number**. And the zero passive of أقام is absence in a
bounded corpus — the very reservation accepted for result 1, applied here at
the same weight. The claim also spans **two corpora**: the passive was measured
in QAC, the maṣdar is tagged in MASAQ, and joining them is a root-transliteration
rule that would be legislated, exactly the join that `THE_JOIN_WAS_NOT_TAKEN`
already stopped once in this tree. Two corpora annotating the same text are two
hands agreeing, not twice the text, and no count from one is added to a count
from the other (`TwoCorporaAreNotOneCorpus`). The verdict that the structure
`verb → transitivity → derivatives` is mis-ordered and that the maṣdar must
precede is therefore **recorded as a named open objection with the weight it
actually carries**, not executed: it rests on one root, and `pipeline_stations`
derives its stations from the tree, so promoting an unencoded station would
only produce an unencoded station. `examples/irab/measure_masdar_priority.py`
will run the whole census the moment the holder of the bytes declares the
length, the mirror, the licence and the six column names.

MASAQ then arrived **whole**, and is deposited as a fingerprinted witness
rather than adopted (`src/alghanem/arabic/masaq_corpus_deposit.py`): digest
`d43d2a81…6f3a`, byte length 20,302,008, licence CC BY 3.0, and the attribution
its licence requires carried in the module as a condition of every figure. It
closes what QAC could not: QAC tags `VN` and nothing below it, while MASAQ names
the derived-noun categories — 4,216 `GERUND`, 125 `GERUND_MEEM`, 84
`GERUND_INSTANT`, 38 `GERUND_PROFESSION`, 2 `GERUND_STATE`, 225
`NOUN_TIME_PLACE`, 24 `NOUN_INSTRUMENT`, 3,156 `NOUN_ACTIVE_PART`, 501
`NOUN_PASSIVE_PART`, 1,646 `ADJ_QUALIT`, 459 `ADJ_INTENS`, 643 `ADJ_COMP`, 125
`NOUN_RELATIVE`, 1 `NOUN_DIMINUTIVE` — so those categories move from *candidate
without a referent* to *measurable against a human gold*. Each of the twenty
deposited figures carries its counting rule, its written limit and a
re-derivation function; `examples/arabic/rederive_masaq_witnesses.py` re-derives
all twenty in one pass and exits non-zero on drift. Two figures are rule-free
twice over and are therefore **declared rather than picked**: `splitlines()`
gives 157,854 lines, `csv.DictReader` gives 157,677 records, and the gap of 177
is measured, not estimated — one header row plus 176 line breaks inside quoted
fields, spread over 154 records. `Word_No` is a **segment** index inside a word,
not a word index; the word key is `Column5`, and confusing the two dropped a
precision measurement from 23.3% to 0.3% before it was caught. The witness
caught a defect on its first run: `embedded_newline_records` re-derived as 0
against a deposited 154, and the fault was in the re-derivation function, not
the deposit — `splitlines()` had already split the embedded newlines before
`csv.reader` saw them. Four named laws bound the deposit:
`CompleteInductionIsCorpusBounded` (4,216 is a count **in these bytes**, not a
count of Arabic verbal nouns), `AnImportedTagIsAHumanJudgementNotAMeasurement`
(a zero means *not annotated here*), `AConservationAuditIsNotAnAccuracyClaim`
and `SyntheticLinesAreDeclaredNotHidden`. What it does **not** close: MASAQ has
**no root column**, so joining it to QAC or to Maqāyīs is positional
`(sura, verse, word)` — exactly where the 23.3% → 0.3% failure came from — and
**no cross-corpus figure is deposited**. A public mirror of a different byte
length and a different digest re-derives the fourteen tag counts exactly and
diverges on all six byte-and-line figures; that is recorded as corroboration
under `AMirrorWithAnotherDigestIsNotTheseBytes`, not as a second witness, and
the column binding of the deposited bytes remains the depositor's declaration,
not a reading taken from the mirror. One sanctioned place is reserved for those
bytes — `corpora/MASAQ.csv` — on the strength of the recorded `CC BY 3.0`
label. That reservation asserts **nothing** about QAC or Tanzil: their bytes
stay outside this tree because permission to copy them **has not been examined
and not been deposited here**, not because it was examined and found absent —
forbidding derivatives is not forbidding verbatim copies, and requiring
attribution and notice is not forbidding anything
(`APermissionUnexaminedIsNotAPermissionRefused`). And **the bytes are not in
this tree yet**, and
the place alone re-derives nothing: until they are deposited there, the twenty
figures require a path in `ALGHANEM_MASAQ_PATH` and the re-derivation test
skips without one. Neither route weakens the gate — the deposited location
is a declared place, not a certificate, and length and digest are matched
before any figure is returned. What has twice reached that directory instead is
a failed web upload under another name, and `AFailedUploadIsNotADeposit` now
states the consequence: only `README.md` and `MASAQ.csv` may sit in `corpora/`,
any other name fails a test rather than resting there implying the corpus has
arrived.

The state of that path has a name in this README, and nowhere else:
**Empirical Witness Activation — تفعيل الشاهد التجريبي**. It is a documentary
label for the state of the MASAQ witness alone. It is **not** a programme
milestone, **not** a readiness rank, **not** a constitutional status, and
nothing in `docs/AIMS.md`, `milestone_ledger` or `readiness_rank` records it —
those track a different axis. Two axes run side by side and are not one:
*programme construction* (laws, gates, evidence, ranks, aims, execution) and
the *empirical witness lifecycle* (specified → path prepared → bytes absent →
bytes resolved → identity verified → figures re-derived → differences
classified). MASAQ sits at *bytes absent* on the second axis, and moving it
along that axis moves nothing on the first.
`TheReadyPathIsTheMasaqWitnessPathNotProgrammeCompletion` says the consequence:
what is ready is the path that receives this witness, verifies its identity and
re-derives its figures — not the programme. Arriving bytes enact no
`DECLARED_DEFERRED` law, create no authority to judge or to birth, close no
epistemic aim, raise no result's rank merely because a file is now in hand, and
turn no induction over this corpus into a claim about open Arabic; the limit in
`CompleteInductionIsCorpusBounded` is unchanged by their arrival. Reaching the
end of the witness lifecycle is not the completion of the project.
`RederivationIsComparisonNotAutomaticEndorsement` closes the second door: the
bytes do not adopt the twenty frozen figures, they run the re-derivation
functions against them. A match holds **within the scope of this witness**; a
mismatch is recorded as it fell. The frozen figure is never edited to fit the
result, nor is its counting rule, and re-derivation is a comparison rather than
an automatic epistemic promotion — a prior claim does not become true because
its witness became available.

MASAQ turned out to carry **i'rab, not only morphology**, and that is where the
next module goes. Three of its columns annotate it — `Syntactic_Role`,
`Case_Mood_Marker` and `Phrasal_Function` — and two more, `Word_No` and
`Column5`, decide whether a count counts segments or words.
`src/alghanem/arabic/irab_column_preregistration.py` freezes those five columns,
four counting rules and the thirteen figures that **arrived from the holder of
the bytes**: 66 distinct syntactic roles, fāʿil 10,483, mafʿūl bihi 8,878, muḍāf
ilayhi 9,123, mubtadaʾ 3,598; 14 distinct case/mood markers, of which the
sub-markers are thabāt al-nūn 2,611, ḥadhf al-nūn 1,913, yāʾ 1,884, wāw 723; the
**estimated** markers, ḍamma 1,632 and fatḥa 1,404; and nāʾib fāʿil 57 in the
phrasal column. Its standing is `مُصاغ_بعد_الرقم` and
`TheFiguresArrivedFromTheHolderOfTheBytes` says plainly that these were measured
elsewhere, so the freeze records a **claimed** number, not a measured one; they
were not adopted, and `irab_column_census.py` re-derives every one of them from
the fingerprinted bytes or produces nothing at all. Four named laws bound it.
`AnAbsentValueIsNotAZero` splits what a single zero used to hide into three
standings — present and agreeing, present and differing, and **not a value of
that column at all** — because a difference of spacing, hamza or vowelling in a
transcribed label would otherwise be read as a measured absence in Arabic.
`AMissingColumnStopsTheCount` refuses a missing column instead of returning zero
for it, since a zero passes through a report looking like a measurement.
`SegmentsAndWordsAreTwoCounts` returns both counts for every value, that
confusion being exactly the one that dropped an alignment from 23.3% to 0.3%.
`CountingAJudgementIsNotSettlingIt` holds that the 1,632 estimated ḍammas are a
count of annotator judgements about something with **no written trace**, so the
question this tree could not settle is not settled by counting it — and that
nāʾib fāʿil here is a witness inside MASAQ, never added to QAC's `PASS`.

A second consignment then arrived, and with it the one thing that could be
checked here and now without the bytes: the **literal spelling** of every value.
All thirteen frozen strings matched it character for character — "فعل ماضٍ" with
the hamza on a dotted yāʾ, "ضمة مقدرة" with no shadda, "ال التعريف" with the
space — so the likeliest way the re-derivation could have failed is now closed.
`PRE_REGISTERED_EXPECTATION` was **not edited** to say so; editing a frozen
expectation once its answer is in hand erases the thing it was measuring
against, so `SpellingCheckBesideTheExpectation` is written next to it instead,
and `ATransmittedSpellingIsNotTheHeader` states its limit: agreeing with a
transmitted list is agreeing with the transmitter, not with the header. The
consignment also brought two further columns — `Case_Mood` (mabnī 53,687, marfūʿ
27,015, majrūr 23,255, manṣūb 19,327, majzūm 1,490; five values and no sixth)
and `Invariable_Declinable` (twelve values, mabnī 54,734 and muʿrab 39,509 among
them) — thirty-six further figures, the 157,677-segment total, and the per-column
**coverage**. Coverage is what stops a count being read as a census of Arabic:
`AThinlyCoveredColumnIsNotACensusOfArabic` holds that 57 nāʾib fāʿil in a column
filled in 1.79% of segments is 57 of what was annotated, not 57 passives in the
Quran, and is not to be set beside a figure from a column filled in 76%.
`ACoverageIsNotACount` refuses the other direction: a percentage is compared at
the places it was declared to — 84.45% is two — and multiplying it back by the
denominator yields a range thousands of segments wide, not a measurement, so the
157,677 is counted row by row and never derived from 100.0000%. Twenty-five
synthetic-row tests, declared as synthetic, plus two that run the moment the
bytes are resolvable; `examples/arabic/measure_irab_columns.py` prints each claim
beside its derivation and exits non-zero on any figure or coverage that does not
re-derive.

### The join finally legislated, and six numbers where one was claimed

A message arrived claiming that Ibn Fāris's *Maqāyīs al-Lugha* covers roots the
Quran does not: 4,565 roots there against 1,532 tagged in the Quranic Arabic
Corpus, 1,204 shared, 3,361 (73.6%) uncovered, 3,011 of them trilateral — and,
in the other direction, 328 roots tagged in the corpus but absent from Maqāyīs,
which the sender diagnosed as **a transliteration fault in their own tool**:
Buckwalter `A` supposedly standing for hamza-on-alif and being read as bare
alif. Nothing about that could be adopted as it stood, because the join it
assumes is exactly the one this tree had twice refused to take:
`TheJoinWasNotTaken` recorded a literal intersection of **zero, measured**,
between Buckwalter roots and Arabic ones, and said plainly that bridging them
needs a transliteration table and a hamza decision, both of which are **rules
legislated, not readings taken**, and both of which must be frozen in a
separate specification before any measurement. `root_orthography_bridge` is
that specification: it opens no file and emits no count — a guard refuses any
field whose name carries one — and holds the Buckwalter table character by
character from the corpus's own documentation, in which `A` is **bare alif**
and the six hamza characters `' | > & < }` are each distinct. So the incoming
diagnosis is not adopted either: it is frozen as one of **two competing
hypotheses**, against the rival reading that the corpus's `ROOT` field unifies
hamza by convention, in which case no tool is broken and a normalisation rule
is unavoidable. The two differ on a single observable — whether any of the six
hamza characters occurs in that field at all — so `qac_root_alphabet` emits the
field's alphabet **before any transliteration**, the transliteration itself
being the accused. The cause of the 328 is therefore left unwritten until that
observation is made, and neither hypothesis is deleted afterwards, since
deleting the refuted one would make the survivor read as obvious rather than as
a result.

Six counting questions were put to the sender and none was answered, so none
was decided on their behalf: each is recorded in
`UNANSWERED_COUNTING_DECISIONS` with the number it moves and how it was handled
instead. The hamza target — bare `ا` or seated `أ` — is enacted **both ways**
as two named rules, which is why the overlap table has six stages rather than
four: raw, transliterated only, transliterated plus each hamza rule, and
transliterated plus each full chain with `ى ← ي` and `ة ← ت`. `ا ← و/ي` is
**refused by name** rather than omitted, because deciding a weak radical is the
conflict already ranked `THE_TREE_CANNOT_TEST_IT`, not a difference of
spelling. No stage is declared "the" number: `overlap_readouts` emits all six
or raises, and there is no function that computes one alone, since a figure
printed only after normalisation hides the rule that produced it. Every rule
states **what it destroys**, and `fusions_under` names the merged roots
themselves rather than their total — سأل and سال become one form under the
bare-alif rule, and that is the price of the intersection it buys. The `ة ← ت`
rule fires on nothing in the Maqāyīs root column, which is a **measured** zero
fixed by a test against the fingerprinted bytes, not an assumption; the rule
stays enacted because silence on one table is not silence on every table.

What re-derives here and now is the Maqāyīs side, its bytes being in this tree:
4,565 distinct `root_full` values over all four `root_type` values under a
counting rule that did not exist before — `maqayis_root_table_deposit` had
rules for records and for trilaterals only, and 4,565 is neither — and 4,087
trilaterals under the existing one, both emitted together since the sender did
not say which side of that line their figure sat on. The corpus side does not
re-derive here and is not guessed: its bytes stay unvendored under GPL and CC
BY-ND, so `qac_roots` takes a path from whoever holds them and matches the
frozen digest and byte length before a single character leaves it, and the
tests that depend on them **skip with a written reason** rather than passing in
silence. `examples/irab/measure_maqayis_qac_root_overlap.py` prints the
alphabet, all six stages, the distinctions each destroyed, and each arriving
figure beside the stages at which it matches, exiting non-zero when a claimed
figure matches no stage under any frozen rule. Two limits are written into the
modules rather than left to a reader. `AbsenceInQacIsAbsenceFromATagging`: the
`ROOT` field is an annotators' classification, so an uncovered root is one
**not tagged in this edition**, never one the Quran does not contain.
`The3361CarryNoMorphologicalTag`: Maqāyīs is an etymological-semantic
dictionary and not an annotated corpus, so what it adds widens the **space of
roots**, not the space of morphological measurement, and no form, bāb or
augmentation is read out of any of its entries. `TheJoinWasNotTaken` itself is
left **unedited**, with a note recorded beside it that its condition has since
been met — a test asserts its wording character for character — because erasing
a reservation once it has been answered hides that it was ever a barrier.
Two things are settled before the bytes arrive rather than after. The first is
the order of reading: `Morph_type` is the only column declared filled in 100% of
segments, so `read_anchor` is read **before any figure** and
`TheAnchorIsReadBeforeTheFigures` records why — if that column is not full, or
the record total is not 157,677, what is at fault is the reading itself, record
splitting or a newline embedded in a quoted field, and a difference in some
figure read at that point is a reading of a broken pipe. The second is what
happens to a figure that differs. `ADifferenceIsClassifiedNotAbsorbed` forbids
editing the frozen figure or its counting rule until they match; the difference
is recorded as it fell and classed by `IrabDifferenceClass`, whose four classes
are frozen into the preregistration digest **before** any of them was seen: a
counting-rule difference (the word count, not the segment count, is what the
claim matched), a value-name difference (the frozen spelling is not a value of
that column at all), a difference in the bytes, and **not yet classified** —
which is a declared class precisely so that no difference is pushed into a box
too small for it. Finally, `masaq_bytes_are_resolvable()` is now the skip
condition for every byte-gated test, so
`ASkipIsConditionedOnTheBytesNotTheVariable`: a variable pointing at a file that
is not there skips, and bytes that resolve but differ do **not** skip — they
fail, because the place is not a certificate.

The 76.36% coverage of `Syntactic_Role` reads as a gap in the annotation, and
it is not one: it is a ratio taken over the wrong denominator. Restricted to
**stems** — `Morph_type == "Stem"`, 77,797 of them — the same column is filled
in 99.6838%, because prefixes and suffixes have no i'rab case to begin with and
counting them lowers a ratio that never fell.
`src/alghanem/arabic/irab_operator_preregistration.py` freezes that denominator
with its counting rule, and `ADenominatorIsDeclaredNotAssumed` is the law that
follows: 76.36% and 99.68% are not rival numbers but two ratios with two
denominators, so no ratio leaves either module without its denominator in the
same structure — `ArrivingStemCoverage` and `StemCoverageReading` both carry it,
and a coverage built without one cannot be constructed at all. The acceptance
threshold is 99% on the stem denominator, and it is declared as what it is:
the coverage arrived first, so the threshold is a stated measure for future
readings, not a bar this figure cleared before anyone saw it.

The residue — 246 stems with no role — is **named before it is excused**. It is
neither noise nor one fault: 190 verses at 1.29 stems each, in two distinct
patterns. A verse whose other stems are annotated and one is not is a lapse in
a cell; a verse left wholly unannotated is a skipped verse, and the largest,
2:13, holds thirteen of them in consecutive positions. `ResiduePattern` freezes
both patterns and a declared third, **neither pattern**, so that no verse is
pushed into a box too small for it, and `measure_residue` classes every verse
by them from the bytes. What did not arrive is how the remaining 82 stems split
between the second and third patterns, and `AnUndeclaredSplitIsNotAZero` keeps
that place declared and empty: `ArrivingResidueAccount.stems` is `None` there,
meaning *did not arrive*, never *zero*. `CoverageIsNotCorrectness` states the
other limit, and the residue itself witnesses it: in that same 2:13, "آمَنَ" —
a perfect verb — is tagged `مجزوم`, so 99.68% counts the stems that were
annotated, not the stems annotated rightly.

The relation itself is the weakest claim of the three and says so.
`irab_operator_census.py` reads eight frozen detectors — three operators (ḥarf
jarr, past verb, imperfect verb), three dependents (ism majrūr, fāʿil, mafʿūl
bihi) and two neutrals — whose **counts are imported from the figures already
frozen** in `irab_column_preregistration`, never restated, since a number frozen
twice is two numbers that can drift apart without either failing. Every value
outside those eight answers `خارج_الكواشف`, a declared standing rather than a
side it was pushed into. `ARelationNeedsTwoPresentTerms` bounds every pair by
one verse: a dependent is never joined to an operator in another verse to
complete a count, and each dependent gets one of three standings that no zero
collapses — an operator before it, an operator after it, or **no operator
observed** — with the distance to the nearest one reported in words, not merely
its existence. `AnUnreadableWordKeyIsCountedNotDropped` counts a row whose word
key is not an integer in a field of its own instead of dropping it silently out
of a denominator. `AnOperatorTagIsNotAProvenGovernment` is the limit that
matters: the corpus has no column binding an operator to its own dependent, so
these are counts of neighbourhood under a frozen rule, and neighbourhood is not
government. `PreMeasurementExpectation` is the one thing here written before its
answer — that operators precede their dependents in the great majority, and that
one word is the commonest distance — and both halves are falsifiable. The unit
reads the `Phrase` column not at all (`ThePhraseColumnIsNotUsed`: 1.80% filled,
and structurally skewed, since it tags the embedded clause and not the main
one), infers no marker from a case (`TheMarkerIsNotInferredFromTheCase`), and
settles nothing about estimated markers by counting them.
`examples/arabic/measure_irab_operators.py` prints each arriving figure beside
its derivation and exits non-zero on any that differs.

A third denominator follows, and the unit built on it opens with a retraction.
`src/alghanem/arabic/ibtida_preregistration.py` freezes the **positions that
admit inchoativity** — mubtadaʾ 3,598 (imported from the first freeze, never
restated), mubtadaʾ muʾakhkhar 570, khabar 2,057, ism ḥarf nāsikh 2,086 and its
khabar 929, ism fiʿl nāsikh 1,199 and its khabar 799, and ism lā al-nāfiya
li-l-jins 111 — and the denominator is their **sum**, 11,349, derived rather
than written as a ninth figure that could drift from the eight. It is not the
stems and not the segments: 11,349, 77,797 and 157,677 are three declared
denominators under `ADenominatorIsDeclaredNotAssumed`, and a module-level guard
refuses the unit outright if the inchoative total ever equals either of the
other two. Four mutually exclusive and jointly exhaustive classes partition
those eight values — bare, particle-nasḵẖ, verb-nasḵẖ, and lā of absolute
negation — with a guard that no value falls in two classes, none outside all
four, and their sum is the denominator exactly. The lā class has **no khabar
value in this column at all**, which is recorded as *did not arrive*, never as
a zero. `TheTwoColumnsAreNotOneFigure` keeps the earlier freeze untouched:
"khabar" in `Syntactic_Role` is 2,057 and "khabar" in `Phrasal_Function` is
1,398, two tags under two conditions rather than two rival numbers, and the
constructor refuses any position declared on the phrasal column.

Two limits are written into the unit rather than left to a reader.
`ARoleTagIsNotALink`: a "khabar" tag says *this is a predicate*, not *this is
the predicate of that mubtadaʾ*; the corpus binds no two terms, so
`ibtida_census.py` reports three standings for each inchoative **inside its own
verse** — one tagged predicate, no tagged predicate, or more than one candidate
— and the second is named by its place, not summed into a zero. There is no
gold for that link, so the output structures carry no accuracy, precision,
recall or score field and a guard refuses one (`NoGoldForTheInchoativeLink`).
`AnInchoativeGovernorIsSemanticNotLexical`: inchoativity is a semantic
governor, so no lexical detector is sought for it, and 35.4% of mubtadaʾ
positions are marked by sukūn — the ruling stands while the marker is absent.
Four residues are named before they are excused, in five lines so that neither
of the two nasikh differences hides inside a sum: three accusative mubtadaʾ,
whose **individual inspection is mandatory** and whose places are emitted one
by one rather than summarised; an arriving 187 that does **not** derive by
subtraction from the eight (3,598 + 570 − 2,057 = 2,111), so its two terms stay
a declared empty place; 1,157 and 400 derived by subtraction and never written
as third numbers; and a fronted predicate that carries no tag at all, so its
size is `None` rather than zero. The three-part `PreMeasurementExpectation` is
the only thing written before its answer, and each part is falsifiable: the
three accusatives stay three, the nasikh ratios stay near 2.25:1 and 1.5:1 —
**if the two sides come out equal the hypothesis fails** — and every tagged
nāsikh has a tagged name in its own verse, a governor without one being a
residue that gets named, not zeroed.

The retraction is recorded in the unit itself rather than quietly corrected.
It was declared earlier along this path that the predicate is not annotated;
that was wrong, and it came from scanning the top ten values of a column and
then denying the rest of it. The predicate is annotated by four values — khabar,
khabar ḥarf nāsikh, khabar fiʿl nāsikh, and mubtadaʾ muʾakhkhar. The arithmetic
is recorded as it fell rather than tidied: the first three sum to exactly 3,785,
and adding mubtadaʾ muʾakhkhar gives 4,355, so the figure 3,785 arrived
attributed to four values while being the sum of three. From that error
`APartialScanForbidsATotalDenial` is enacted — a partial scan licenses no total
denial; its answer is *not examined*, never *not there* — this being its third
recurrence on this path. `examples/arabic/measure_ibtida_census.py` prints the
declared denominator, each arriving figure beside its derivation, the class
conservation check and the named residues, and exits non-zero on any
difference, and the byte-gated test skips with a written reason until the
fingerprinted bytes resolve.

### A census whose numbers no one claimed first

While those bytes are awaited, `src/alghanem/arabic/maqayis_witness_census.py`
measures bytes that are already here. `maqayis_by_root_csv_999.csv` is
fingerprinted in this tree, so its poetry-evidence and semantic-axes columns can
be counted without waiting for anyone, and a census is measured from them:
1,944 records carrying poetry evidence, 4,176 witness segments, of which 4,176
bear the hemistich marker, a `root_type` census of 4,089 / 428 / 56 / 3 summing
to the 4,576 records, and a comparison of each record's declared `axes_count`
against the segments of its own `semantic_axes` cell — 2,890 agreeing, 822
differing, 864 blank. The epistemic position here is the inverse of the MASAQ
one and is written down as such. `NoClaimPrecededTheseNumbers`: nobody
transmitted these figures in advance, so a match tests no transmitter and
vindicates no one; and `TheRulesWereWrittenAfterTheseNumbersWereSeen`, recorded
rather than hidden, since what keeps a rule from having been cut to fit a
pleasing number is that it is written out in full and re-derived from
fingerprinted bytes, not that it was written first.

Three of the module's limits are the reason the figures are not one number.
`ASeparatorIsTheProducersNotThePoets`: `|` is the file producer's mark, so a
segment count is a count of his separators, and a bar falling inside a line
would inflate it — which is why the segments bearing the `…` marker are counted
alongside, their equality being a corroboration that closes nothing.
`AWitnessSegmentIsNotAVerse`: metre, attribution and completeness are
unverified, so 4,176 is a count of segments in a file, not of witnesses in
Arabic or in Ibn Fāris. And `ABlankIsNotAZero`: the 864 records declaring no
`axes_count` are a third class, never folded into agreement or disagreement, so
no agreement ratio is published — the denominator itself would be in dispute.
Of the 822 differences, 597 are an empty axes cell against a declared 1, and
neither side is adjusted to remove any of them.
`ADeclaredCellIsCheckedAgainstItsOwnFile` keeps the comparison inside one
record, and `TheBytesHereAreNotTheWithheldBytes` keeps this census from being
read as progress on MASAQ: a figure reached from one file does not stand in for
the bytes of another. `examples/arabic/measure_maqayis_witnesses.py` re-derives
every one of them beside its rule and its limit, and exits non-zero on any
drift.

### Conditions frozen where a verdict used to be written

`vv_birth_hypothesis.py` and `vv_birth_preregistration.py` open
`G0.VV-BIRTH-1` as a preregistration and nothing else. The point of the pair
is that four different answers are reachable from them: the extension may
preserve identity without ever being a neutral element; VV neutrality may be
refuted outright; the syllable may hold structurally and still not be born
constitutionally; and CV/CVV may turn out to be one type in two quantity states
or two types. None of the four is written anywhere in the freeze.

What is frozen is the vocabulary that makes those answers separable. The two
projections are declared before any run — `π_I` onto a closed vowel quality and
`π_Q` onto `{1, 2}`, explicitly counting rather than physical time — and
`letter_index` is named in `BANNED_IDENTITY_PROXIES`, because a program offset
would make `π_I(E(v)) = π_I(v)` true by storage rather than by phonology.
`H_E` (an identity-preserving, quantity-changing operator) and `H_N` (a neutral
element with respect to a stated `⊗` and a stated `∼_I`) are two hypotheses,
not one, and `NEUTRAL_ELEMENT_SUPPORTED` is not in the outcome vocabulary at
all. `ExperimentOutcome` has no `BORN` member, so no template match can emit a
birth. Closure is written as the quotient law `Obs(k[g]) = Obs(k[π(g)])` plus
`NoCrossBoundaryActiveResidual`, with membership in the syllable template table
named as what does **not** substitute for it. `LicensedJoin` is a partial typed
operation carrying its impediments, and a trace counts as reconstruction only
if every strict subset of it fails the audit.

Four adverse facts about this tree are deposited before the run rather than
discovered after it: `C` and `V` hold no birth certificate, no recorded sound
exists here, no reconstruction target independent of the candidate model exists
— `syllabifier` segments by the very templates `H_S` is about, and
`p_extractor` attaches `MADD_EXTENSION` by the rule under test — and the madd
label is itself a rule output. They force, in advance,
`INDEPENDENT_TARGET_MISSING`, `PHYSICAL_PHONETIC_VERIFICATION = UNDERPOWERED`,
and a ceiling of `CONDITIONAL_STRUCTURAL_BIRTH` on `H_S` and `UNDEFINED` on
`H_N`.

Two defects of the earlier freeze are closed by construction.
`REQUIRED_NOTATION_SITES` is a hand-written list of seventeen
`(module, symbol)` pairs, never derived from the frozen text, so deleting a
clause cannot delete its own requirement — the tests check both that no site is
missing today and that removing one is actually detected. And a self-recomputed
digest is named as no seal: `ASelfRecomputedDigestIsNotASeal` says outright
that editing text and digest in one commit is undetectable here, so the seal
obligation is placed on the readout, which must carry `prereg_commit_sha` and
`expected_preregistration_digest` from a strictly earlier commit.
`ACommitCannotContainItsOwnSha` records why this module cannot carry it.

**What it does not establish:** anything at all about VV. There is no readout
in this commit, and the tests assert that `alghanem.arabic.vv_birth_readout`
does not exist. `TheCitedFreezeIsAbsentFromThisTree` records that
`vv_neutral_birth_freeze.py` is nowhere in this tree or its history, so the
circular fidelity check and the non-sealing digest are closed here by design,
not by inspecting that file.

### Closing the execution freedom that a preregistration alone leaves open

`vv_birth_amendment.py` is the intermediate commit `G0.VV-BIRTH-1A`, and it
exists because freezing hypotheses is not the same as freezing their
execution. It edits neither parent module by a single character:
`AnAmendmentThatEditsItsParentBreaksTheSeal` records why — rewriting
`vv_birth_hypothesis` to repair a defect would change
`PREREGISTRATION_DIGEST`, destroying the seal the future readout is required
to check. `SUPERSEDED_PREREGISTRATION_PARENT` therefore carries the parent
commit SHA and the parent content digest, and refuses to import if the living
digest no longer matches the recorded one. Its scope is stated and checked:
execution detail only, with all five hypothesis identifiers preserved.

Five gaps are closed. `E` was existential — `∃E: X_V ⇀ X_V` leaves the
function itself to be written in the next commit, where it could be shaped to
the data. It now has allowed input fields, forbidden sources, a domain
predicate, a five-step transformation rule, undefinedness conditions, and
output invariants; `PhoneticRole.MADD_EXTENSION` and every `syllabifier`
output are named as forbidden, and an input whose provenance is `MODEL_OUTPUT`
is refused at construction. Because `E` must read `ا/و/ي` to find the
extension at all, it is classed `ORTHOGRAPHIC_EXTENSION_OPERATOR` and not
called a phonetic witness. `X_V` contradicted `𝓠`: its membership admitted
"zero or more" extension slots while `𝓠 = {1, 2}`. The first of the two
branches is frozen — `#Extension ∈ {0, 1}` — so the sealed codomain is left
untouched, and the unchosen branch is recorded with what it would have
required. The four rivals were prose; each now carries a numbered algorithm
with its inputs, output and `UNDEFINED` cases, so none can be written weaker or
stronger inside the readout. The leak ban was by field name, which a rename
defeats: it is now by `ProvenanceClass`, and `π_I` may read nothing whose
provenance is `ORTHOGRAPHIC_IDENTITY`, `PROGRAM_POSITION` or `MODEL_OUTPUT` —
the test renames a banned proxy to `unicode_scalar` and it is still refused.
And `T' ⊊ T` was undefined on a typed record: the order is now `T' ≺_T T`,
declared projections over three named trace fields, with a structural refusal
of any field from which the whole input is recoverable.

A sixth correction is logical rather than executable. The two type hypotheses
were not symmetric: one distinguishing context refutes `H_same_type`, but
*failing to find* one does not refute `H_different_type` — the distinguishing
context may simply be the untested one. The claim is now bounded by a frozen
context set `K_0`, and the only admissible outcomes are
`DISTINGUISHED_ON_K0`, `NOT_DISTINGUISHED_ON_K0` and `UNDERPOWERED`, with
`AbsenceOnAFiniteContextSetIsNotIdentityOfType` stating that the second is a
claim about `K_0` and not an ontological identity of type.

Three adversarial controls — `E_no_extension`, `E_wrong_quality`,
`E_wrong_partner` — are frozen so the criterion can be shown to fail
something. If any of them passes, the outcome is
`REPRESENTATION_TAUTOLOGY`: a criterion nothing fails measures nothing. The
outcome vocabulary they need is declared in a second enum here rather than
injected into the sealed one, and it has no `BORN` member either.

**What it does not establish:** still nothing about VV. There is no readout in
this commit either, and both this module's tests and the parent's assert that
`alghanem.arabic.vv_birth_readout` does not exist. `E`'s output invariants
hold by construction on `E` itself, which is precisely why the module records
that they are not read as a result without the adversarial controls beside
them.
`referent_candidate_preregistration` and `referent_candidate_census` add a
pronoun candidate-enumeration tool that **never names a referent**. Its
declared denominator is only the fifteen pronoun tags that actually encode a
person/number/gender triple — 2,608 of MASAQ's 23,579 pronouns, about 11%;
`ElevenPercentIsTheRealDenominator` keeps the aggregate `SUBJ_PRON` (7,964),
`POSS_PRON` (7,678) and `OBJ_PRON` (3,211) tags outside the denominator with
their reasons written, and `AnUnparsedTagYieldsNoConstraint` counts any tag
that fails to parse instead of granting it a default constraint. The search
window — the pronoun's own verse plus the one before it, inside its sura, and
only nouns preceding it — is frozen before measurement under
`AWindowIsDeclaredNotOptimised`. Because MASAQ tags neither gender nor number
on nouns, agreement is decided by a frozen suffix rule over `Segmented_Word`,
declared as `GenderAndNumberAreInferredNotTagged`; broken plurals and the
ya-nun ending stay `INFERENCE_UNDETERMINED` and are counted, never matched. No
precision or recall figure is issued here, and none ever can be:
`TheReferentIsNotAnnotatedAnywhere` — there is no gold standard in any source
at hand, so `CandidateSetCensus.__post_init__` refuses any field claiming
precision, recall, accuracy or a gold referent rather than ignoring it. The
only legitimate outputs are candidate-set size, the share narrowed to a single
candidate, the distribution by triple, and the listed zero-candidate
positions, under `ACandidateSetIsNotAnAnswer`. Each pronoun gets one of four
named standings — single, multiple, zero, or discourse participant (first and
second person leave nominal matching before any search) — and no zero gathers
two of them.

Source: the Quranic Arabic Corpus, http://corpus.quran.com — built on the
Tanzil Quran text, http://tanzil.info. Qutrub and Arramooz Alwaseet,
T. Zerrouki, http://arramooz.sourceforge.net/ and
https://github.com/linuxscout/qutrub. MASAQ: Morphologically-Analyzed and
Syntactically-Annotated Quran, Majdi Sawalha, University of Jordan,
DOI 10.17632/9yvrzxktmr.2, licensed CC BY 3.0 — its licence permits depositing
its bytes at `corpora/MASAQ.csv`, and whoever opens them owes its authors
that attribution, which is recorded as a condition of the deposit before any
figure is issued. All
attributions are licence conditions, not courtesies.

### A closure defined once, and the thin column that reads half of it

`src/alghanem/arabic/waqf_closure_preregistration.py` freezes a syntactic waqf
— the point at which a predicative unit closes — and keeps it apart from the
phonetic waqf already registered in `ibtida_wasl_waqf_registration`, which is
the quiescing of a final state in recitation. `ThePhoneticWaqfIsNotThisWaqf`:
one word for two subjects does not make them one subject, and neither is
measured by the other.

The proposed law is one sentence: a predicative unit closes when both of its
terms are present, and a prepositional phrase never closes by itself. Three
standings follow, with no zero gathering them — **closed**, **open**, and
**dependent** — and `waqf_closure_census.py` measures them inside one verse
over a declared denominator, **the keys**: stems carrying a frozen
opening-term value. `ANullifiedDenominatorIsNotAZero` makes the conservation a
check rather than an assumption; closed plus open plus dependent equals the
keys exactly, or the gap is printed rather than adjusted away.

Every detector is a **pair of (column, value)**, and the tree itself supplies
the witness for why. `فاعل` in `Syntactic_Role` is 10,483; `فاعل` in
`Phrasal_Function` is 1. Those are two values, not one value with two numbers,
which is what `AValueWithoutItsColumnIsTwoValues` says and what the test
asserts against the frozen figures. The same rule keeps four arriving values
out of every count: `ظرف زمان` (1,426), `ظرف مكان` (758), a second
`نائب فاعل` (747, against the 57 frozen for `Phrasal_Function`), and
`اسم ناسخ`, whose own count never arrived at all — only a difference of 1,157
from its predicate, and a difference without both of its terms yields no
number. They are registered suspended by name with a written reason, under
`AnUnfrozenValueIsNotADetector`, because a guessed spelling turns "not among
this column's values" into a silent zero.

Three limits are written inside the unit rather than around it.
`AClosureIsInferredFromNeighbourhoodNotTagged`: no column says "the sentence
closed here", so closure is an inference from two tagged terms in one verse.
`AVerseBoundaryIsNotASentenceBoundary` is the sharpest of them, because every
figure the unit issues uses the verse as its unit while a sentence spans
verses and a verse holds sentences — a unit called open may close in the next
one. And `APhraseIsNotAClause` is a definition, not a finding: a prepositional
phrase stays dependent even when an attachment is observed in its verse, and
that observation is counted in a field of its own rather than promoting the
standing.

The nominal figures carry a fourth limit that the tree forced on the design.
`AThinColumnIsNotAThickOne`: the two terms of a nominal clause are read from
two columns of very different coverage — `مبتدأ` from `Syntactic_Role` at
76.3631% of segments, `خبر` and its kinds from `Phrasal_Function` at 1.79% —
so the count of **open** nominal units reads first as an empty column, not as
an unclosed clause, and no closure rate is issued from it as a statement about
Arabic. That is the very objection that excluded `Phrase` (1.80%), so it could
not be raised against one column and passed over in silence for the other;
`Phrase` is read nowhere here, and a test asserts its absence from the columns
this census reads. `APartialScanForbidsATotalDenial` governs the other
direction: nothing is denied of a column until `scan_column_values` has walked
all of its values, so "this closing spelling is absent" is a statement about a
spelling in these bytes, never about a category in Arabic.

The expectation is written before the measurement and is falsifiable in two of
its three parts: verbal keys should exceed nominal keys on this denominator —
the common traditional claim, tested with its denominator rather than with the
biased `Phrase` column — and the open share of nominal clauses should exceed
the verbal one by roughly the gap between the two columns' coverage. The third
part, that no phrase is ever closed, is declared **not** a discovery but a
reading of the definition, and it is written down as such.
`examples/arabic/measure_waqf_closure.py` prints every frozen detector beside
its count, every suspended value beside its reason, and every measured figure
beside its limit, exiting non-zero on any drift; the measurement itself waits
on the fingerprinted MASAQ bytes, and in their absence nothing is estimated.

`src/alghanem/arabic/transition_authority.py` gathers one constraint that was
already distributed across the tree without a common name: nothing is derived
from a carrier except what that carrier preserves or what a licensed bridge
permits. The module is a **gathering, not an authority** — it judges no
transition, licenses none, and imports nothing from `kernel/`. It deposits four
named limits plus three about itself:
`NoDerivationBeyondTheAuthorityOfItsCarrier`;
`AZeroShowsAnUnbuiltBridgeNotAnImpossibleOne` (a zero shows *that* bridge was
never built, not that building it is impossible);
`ASignIsNotItsReferentAndNeitherIsItUnrelatedToIt` (what is denied is the direct
transition, not the relation); `FormalEncodingIsNotConceptualMeaning` (expressly
*not* `Language != Meaning`);
`ADerivedCrossModuleLawIsNotAnAttestedSourceLaw` (this is an Alghanem
construction from existing constraints, not a transmitted text, not attributed
to al-Nabhani, and it raises no row's status in `docs/CONSTITUTION.md`);
`SupportIsACheckedInvariantNotAnImport`; and
`TheFourLayerSeriesIsAnAlghanemComposition` (the reality/concept/lafẓ/carrier
ordering rests on transmitted texts not yet collated against a printed source,
so the series is neither attributed nor encoded as a vocabulary). Support is
evidence only where it is checked: each of the five positions in
`CARRIER_AUTHORITY_SUPPORTS` carries a probe that is run against the structural
guard in its own module — the physical layer that cannot be constructed in
`epistemic_layers`, the two refused derivation paths in `wad_naql`, the
structurally excluded external-correspondence target and the unsanaded reading
that stays معلومة in `maluma_mafhum`, and the non-invertible channel derivation
in `dalalat_thalath`. `supported_positions()` returns only what passed;
`unsupported_positions()` surfaces the rest rather than folding them into a
silent count.

### Running what has not been born, without letting the run prove it was born

Two authorities faced each other with nothing between them. `kernel/
birth_certificate.py` gave the constitutional side a method that certifies and
cannot run, and the executive side a method that runs and cannot certify, which
settled who may do what and left no place at all to *try* a candidate. The only
way to try one would have been to execute it and then argue from the execution
— the exact move `ExecutiveAuthorityCannotIssueBirth` exists to refuse.

`kernel/experimental.py` opens a third path. `ExperimentalAuthority.run` takes a
*bound* run request — a declared candidate, a case set frozen before the run,
one input per case, a set of permitted operations, already tied to one frozen
experiment — and an implementation, and returns an `ExperimentalRunRecord` that
says one thing: this declared candidate, under these declared conditions,
produced this output — or this failure. Every other
question is answered `False` on the record itself rather than in prose:
`confers_birth`, `confers_validity`, `confers_constitutional_evidence`,
`confers_identity_proof`, `confers_difference_from_origin`, `confers_necessity`.
An implementation that raises does not escape into the caller; the exception
becomes an `ExperimentalFailureRecord` naming the kind, the case, the message
and the trace so far, because a failure is one of the facts the experiment
produced. An operation is reachable only through `ExperimentalRunContext`, the capability
the authority issues for the case being run: an unpermitted id is refused
*before* the action runs, the refusal is raised as a `BaseException` so an
implementation's own `except Exception` cannot swallow it, the run aborts by
name, and the capability is revoked when its case ends. The authority alone
writes the run's `operation:` events, so an implementation that writes one into
its own trace fails the run instead of being believed —
`UnpermittedOperationCannotExecute` rather than *reported operations are
audited*. And what counts as "the declared model did not account for this case" is a token
frozen in the request *before* the run, so an output matching neither token
fails the run instead of being reinterpreted into whichever reading suits.

`kernel/experimental_comparison.py` is where the instruction-versus-rule
question becomes answerable without being nameable. Two models are run over one
case set compared by canonical content digest — two different case sets are
refused, never reconciled — and `ModelContrastObservation` derives which cases
each left unaccounted and whether one set is strictly inside the other. The
useful direction is the negative one: if the model with fewer parts accounts for
everything, the status reads `NO_DIFFERENCE_OBSERVED` and there is nothing for a
richer candidate to be necessary for. When the richer model does close strictly
more, `confers_necessity` is still `False`, and both models are opaque strings,
so no contrast decided here can announce which genus won.
`ReplayObservation` reads whether repeated runs agreed, and denies
reproducibility in the same breath: agreement inside one process is not the
independent second measurement run that `SyntheticInterventionMayGenerateHypothesisOnly`
requires.

`kernel/experimental_request_content_identity.py` answers one question for the
whole path: when are two experimental artifacts *the same artifact*? By one
rule — the canonical content digest of every declared field, each case input
included, taken over `alghanem.canonical_content`, the repository's single
canonicalization primitive. That closes the earlier split in which a contrast
compared case sets by Python object identity while a replay compared requests
by dataclass equality, so two artifacts could be the same for one authority and
different for another.

`kernel/experimental_run_binding.py` answers the other: *which* frozen
experiment is a run a run of? `ExperimentalRunBindingAuthority.bind` ties one
request's content id to one frozen experiment's content id before anything
runs, and `ExperimentalAuthority.run` accepts nothing else. A domain holds many
experiments and an experiment id holds many revisions, so reading the domain
alone would let a record produced under one experiment be offered against
another — and the offer's trace would then name an experiment the run had never
touched. Hence `SameDomain != SameExperiment` and
`SameExperimentName != SameFrozenContent`. A binding confers nothing:
`confers_authorized_evidence`, `confers_birth` and `confers_necessity` are all
structurally `False`, because it makes a run attributable, never admissible.

`kernel/experimental_evidence_gate.py` is the single door out, and it is
deliberately narrow. `offer` derives its admission conditions — the bound
request the record was produced from, a binding whose content id is the very
one that request was bound to, the record's own request content digest, scope
equal to the frozen experiment's own domain read from the binding, a replay
covering this very record whose outputs, traces and statuses agreed, a trace,
and a canonical manifest encoded from the record rather than written by the
caller — and issues no `AuthorizedEvidenceSnapshot` at all. The manifest is
structural rather than delimiter-joined, and carries the request identity, the
candidate declaration, the case set, every case input, the permitted
operations, the outcome vocabulary, the outputs or the failure, the trace, the
replay and contrast readings, and the frozen experiment's content id — so two
different observations cannot encode to one payload, which joined text could
not guarantee. The payload must still travel
the whole G0.2a.3 chain, authorization to run to `ingest`, to become assessable,
which leaves `FrozenExperimentPrecedesAuthorizedEvidenceIngestion` exactly where
it was. A failed run may be offered and is marked as such, because dropping
failures at the door would make the record of an experiment better than the
experiment was.

The isolation is authority isolation and capability mediation, and the module
says so rather than implying more: `CapturedFailure != SandboxedExecution`,
mediation is not confinement, and nothing here restricts filesystem, network,
memory or time. An ambient effect taken without asking the capability is not
refused — it is simply not seen, which is why the sandbox remains a declared,
deferred milestone. Two sweeps hold the paths apart.
`experimental` and `experimental_comparison` import nothing from the birth,
verdict, certificate, closure, survival or acquisition modules; no kernel module
outside the gate imports any experimental type; and a test asserts that the
surfaces of `ConstitutionalBirthAuthority`, `ExecutiveAdmissionGate` and
`BirthVerdictGate` gained nothing. The named laws are collected in
`docs/CONSTITUTION.md` under `G0.EX`, and the short form of all of them is
`ExperimentalSuccess != Birth`, `ExperimentalFailure != NoBirth`, and
`ExperimentalEvidenceOffer = BoundRun + FrozenExperimentContentIdentity +
CanonicalObservedPayload`.
`examples/kernel/contrast_two_models.py` runs the contrast end to end and prints,
as its last line, that no birth occurred.

The meta-algebra now has two levels above its realizations rather than one.
`Σ_M` (`metaalgebra/schema.py`) is the *language*: it says what a layer, a
transition, an audit certificate and a realization are, and it deliberately
contains no concrete layer at all. `Σ_A`
(`metaalgebra/specification.py`) is a *theory written in that language*: named
layers, named transitions, digested by content. Its digest excludes its
realizations, which is the structural witness that the theory is an origin and
not a description of one of its images. From that single origin two realizations
run in parallel — `arabic/realization.py` and `realization/python_realization.py`
— so that the relation is `Σ_A → {R_arabic, R_python}` and never
`Arabic → Python` or `Python → Arabic`. Both are structural bindings today:
every component realization names a place in its domain and a falsifier distinct
from that name, every condition is a `DeclarativeClause` carrying its own reason
for not being executable, and the Arabic side binds no syllable, vowel or
weight. Residuals may be dispositioned `CLOSE`, `REFINE`, `REVISE_DOMAIN` or
`DEFER`, so a failed binding can indict the domain mapping instead of always
indicting the theory.

`realization/` is the generation package: `G_py` renders a Python module from
`Σ_A` alone, and the committed tree under `realization/generated/` is checked
byte-for-byte against regeneration. Determinism is declared relative to
`(digest Σ_A, digest g)` rather than to `Σ_A` alone — the generator's digest is
computed from its own source bytes, not from a hand-written version string —
and every manifest carries `sigma_digest`, `generator_digest` and `backend_id`.
No executable meaning is invented from prose: each prose condition becomes an
explicit `UnimplementedSemantics` refusal that fails loudly when called, and
only an `ExecutableClause` compiles to a predicate. `metaalgebra/` stays
handwritten and imports nothing from the generation package, so `Σ → G → Σ` does
not close. Two domains prove coverage, not representation independence; the
commutative square `R_{i+1}^D ∘ T_i = T_i^D ∘ R_i^D` is recorded as an
obligation in `metaalgebra/commutation.py`, and the named laws are collected in
`docs/CONSTITUTION.md` under `G0.R`.

The carrier-fiber experiment asks one question and refuses the rest: does the
state space depend on the identity of the carrier, or only on how often and
where that carrier happens to occur? It runs in three frozen stages.
`arabic/carrier_fiber_preregistration.py` freezes the contract *before* any
evidence: a `StateSchema` that declares state as a product of axes — vowel,
nunation, gemination, quiescence — rather than one flat set of mutually
exclusive values, with *madd* declared `DEFERRED_NOT_READ_AS_A_STATE` because it
may be a transition and not an alternative state; three frozen controls
(frequency, position, boundary); and `word_role` structurally forced to
`DEFERRED_COVARIATE`, since the morphological tagging it needs is not available
and inventing it would be fabricating the control. Capacity and composition are
frozen as two separate measures, because two carriers may admit the same number
of states and not the same states.

`arabic/carrier_state_observed_fiber.py` measures. It accepts the bytes of any
corpus with its digest, refuses bytes that miss it, keeps one row per
occurrence, and keeps deferred-axis marks and unread marks on the row instead of
dropping them. `arabic/carrier_fiber_null_model.py` then tests
`State ⟂ Carrier | Frequency, Position, Boundary` by permuting state vectors
within strata, so the carrier's frequency, position and boundary are preserved
by construction rather than modelled. All statistics are exact fractions
reported in permille; a probability is never read as zero in a finite sample.
Carriers below the frozen support threshold read `UNDETERMINED`, because rarity
is not a result.

Run on the deposited text these modules refute `E_observed = C × S_global` *in
this corpus and this encoding* and nothing wider, and they find gemination
co-occurring with vowels — the empirical reason the state was not frozen as one
flat axis. The deposited run is declared `CALIBRATION_WITNESS`: a short text
calibrates the instrument, it does not decide the question, and
`E_licensed = ⨆_c S_licensed(c)` remains a hypothesis, not a finding. What is
observed to be absent is not thereby shown to be forbidden.

`metaalgebra/generalization.py` carries the blocker that this work made
unavoidable: `LocalClosure ⇏ GlobalClosure`. Extending a claim from the
subdomain it was measured on to a wider domain requires one declared warrant —
a proved domain identity with its own cited evidence, or a named generalization
law with a statement and a precondition — and is refused at construction
otherwise. Refusal blocks promotion, never the record: the claim stays readable
in its own subdomain. The named laws are collected in `docs/CONSTITUTION.md`
under `G0.GEN`.

`src/alghanem/prior/` and `src/alghanem/ontology/` open a level *beneath* the
linguistic nucleus. `Σ_L` (`G0.NSB-0`) already named `GENUS`, `INDIVIDUAL`,
`REFERENCE`, `EVENT_ANCHOR` and `QUANTITY_ANCHOR` as branches of `TermAnchor`,
but those are not purely linguistic sorts — they are ontological candidates that
language *uses* after some earlier layer has fixed them. So the chain splits into
two axes: an existence axis `PK₀ → O₀ → O_L → O_AR` (the last deferred), and the
algebra axis `Σ_M ⇝ Σ_L ⇝ Σ_AR` that operates on those objects. The load-bearing
consequence is `TheAlgebraDoesNotCreateItsObjects`: `Σ_L` does not create `O_L`;
it works on what `O_L` has licensed.

`prior/conditions.py` is `PK₀`, and it is deliberately narrower than a store of
facts. It never says "this thing is a genus"; it records the nine conditions
under which it is legitimate for such a kind to be born — domain, unit criterion,
identity criterion, attribute possibility, relation possibility, transformation
conditions, conditions and preventers, preserved trace, and the remainder that
blocks closure — with exact coverage, each naming what it forbids and the genus
of its own license. Depositing a ready-made fact there is unsayable, not merely
refused: a field carrying such a name fails at import.

`ontology/general.py` registers `O₀` candidates, each bound to the digest of the
base that licensed it and each carrying both a necessity and an irreducibility
claim. `ontology/linguistic.py` carries the correction the dialogue turned on:
`OntologicalKind ≠ LinguisticRole`, enforced on field *types* the way
`RelationIsNotRepresentation` is one level up. `Genus → TermAnchorRole` is a
license with a condition that could fail; `Genus ⊆ TermAnchor` asserted as a
primitive truth is not. "Event" is a kind; "event anchor inside a nisbah" is a
role that object plays.

This is a testbed, not a verdict. It issues no birth, no freeze and no `E0`; no
`kernel/` module reads it; and `src/alghanem/linguistic/` is untouched — its
text, digest, schema version and Arabic meeting point are byte-identical to what
`G0.NSB-0` left, because a layer under which a missing layer was found is not a
refuted layer. Re-anchoring `Σ_L` to `O_L` and migrating `TermAnchorKind` into a
licensing reference are declared next steps, not steps taken. The named laws are
collected in `docs/CONSTITUTION.md` under `G0.PK-0 / G0.ONT-0`.

`src/alghanem/linguistic/anchored.py` then closes the gap on the algebra side.
`G0.ONT-0` said `Σ_L` operates on what `O_L` licenses, but `Σ_L` still named its
own sorts. In the anchored layer a term anchor no longer *writes* its kind: it
carries a `LicensedRoleRef` derived from a license in a standing `O_L`, so
`GENUS`, `INDIVIDUAL`, `REFERENCE`, `EVENT_ANCHOR` and `QUANTITY_ANCHOR` stop
being branches of a linguistic primitive. Identity and admissibility conditions
stop being free prose and become `LicensedConditionRef`s bound to born `PK₀`
conditions and to the digest of their base — free text is an acceptable
recording stage, and not enough once an ontological proof is claimed. The whole
nisbah is bound to one `O_L` digest, so licenses from two ontologies cannot be
mixed into one structure.

`linguistic-nisbah.schema.v2` stands *beside* `v1`, built on its digest and
refused if it reuses its version name: `v1` is a text that was read, and
overwriting a text that was read erases the history of the argument rather than
correcting it. Exactly one module of the package reads the existence axis, and a
witness asserts the reader set is exactly `anchored.py` while `ontology/` still
reads no algebra at all.

This migration is deliberately decoupled from any empirical threshold: no
measurement can correct a confusion of an object's nature with its function in
language. Nothing here names a corpus, computes a score or registers an
acceptance criterion, and the negative controls stay suspended. The open
question is recorded rather than answered — an absolute match level cannot on
its own license an adoption, because a weaker model that *ties* already defeats
the claim, so any future criterion must carry both an absolute floor and a
margin over each registered null model separately. The named laws are collected
in `docs/CONSTITUTION.md` under `G0.ONT-1`.

Two remainders stayed open after that. The prose did not leave the chain, it
moved one step back into `FunctionalLicense.condition_statement`, so a license
could still be founded on an interpretive sentence; and a nisbah bound its role
references to one `O_L` digest while nothing stopped its *conditions* from
coming out of a different prior base. Digest unity inside a nisbah is not origin
unity along the chain. `src/alghanem/prior/references.py`,
`src/alghanem/ontology/linguistic_v2.py`,
`src/alghanem/ontology/lineage.py` and
`src/alghanem/linguistic/anchored_v3.py` close both, standing beside `v2`
without editing a single historical file. A `ReferencedFunctionalLicense`
carries no statement at all but a `PriorConditionRef` naming the very condition
that licensed it and the digest of its base; an `ExistenceLineageRef` records
the chain `PK₀ → O₀ → O_L²`; and `linguistic-nisbah.schema.v3` refuses any role
from another ontology and any condition from another base, naming every
offender. A paired witness shows the mixed-origin case being admitted by `v2`
and refused by `v3`.

Two disciplines make that claim honest. References are derived, never
constructed: `of(...)` is the only door, because authority is a condition of a
reference coming into being and not a property attached to it afterwards — a
forgeable twin would make the type mean less. And preserving a historical layer
means its own bytes *plus* the identity of everything it depends on: a file left
untouched whose imports moved beneath it no longer means what it meant, so a
witness freezes the digest of every module in `anchored.py`'s transitive import
closure and asserts the closure gained no new member. `v3` reads its parent's
identity, not its implementation: one imported name, no construction through
`v2`. Conditions here are registered, standing, usable, licensed — never *born*,
since no birth gate exists at this stage. The named laws are collected in
`docs/CONSTITUTION.md` under `G0.ONT-2`.

Up to that point nothing in the repository *runs*. `src/alghanem/execution/`
closes the smallest gap that is still non-trivial: a fully declared case is
carried through the real chain `PK₀ → O₀ → O_L² → ExistenceLineage → Nisbah_v3`
and emits an auditable, replayable `PASS`, `BLOCK` or `DEFER`. The product is a
licensing and audit engine, not a model of language — there is no Arabic
material here, no parser, and nothing that turns prose into meaning. The input
document is an inert *candidate declaration*: it may name identifiers, digests
and closed-vocabulary members, but it may not carry a derived reference, a
licensed role, a lineage or a verdict. All authority is re-derived through the
existing `of(...)` doors, and a document from which no case can be constituted
yields an `InputValidation` rather than a verdict, because a malformed input is
not a judgment against the case.

Three separations make the verdict readable. A standing is five-valued, not
three: proved true, proved violated, evidence incomplete, *check blocked by a
prior law*, and *no claim was ever made*. The last two do not bear on the
verdict, and they differ causally — a case blocked by origin mixture must not be
displayed as one with missing evidence, and an undeclared identity is never read
as an identity that agreed. Judgment also precedes construction: the `v3`
signature is built only after a provisional `PASS`, since its constructor
refuses origin mixture and would otherwise issue the verdict itself with no
readable trace. And replay runs from the declaration, not from a digest — a
digest cannot be inverted, so the envelope carries the full document bound by
`Digest(document) == core.input_digest`, while `execution_digest` lives outside
the core it measures. The law set is frozen and ordered, and its digest is part
of every result's identity, so an old verdict is never silently re-read under a
newer set. No clock, randomness or filesystem path enters the result: the same
declaration under the same laws reproduces the same verdict and the same trace,
byte for byte. The named laws are collected in `docs/CONSTITUTION.md` under
`G0.RUN-0`.

`G0.RUN-0H` hardens that engine without adding a law. Two invariants belong to
the engine rather than to the law set, so the frozen law list and its digest are
untouched: a materialization that fails *after* a provisional `PASS` is an
`ExecutionInvariantError`, never a `BLOCK`, because a block is issued only when
a declared law was evaluated and proved violated; and success and authoritative
material are biconditional — `PASS` requires a materialized identity and
`BLOCK`/`DEFER` forbid one. The sealed envelope now carries the frozen
declaration itself and projects the document afresh on every read, since
freezing a dataclass never froze the dictionary inside it. Under `DEFER` the
dependent identity law is recorded as blocked by the first unresolved law rather
than as missing evidence of its own. This last correction changes
`execution_digest` for deferred cases that claim a nisbah identity, which is
admissible only because hardening precedes the freezing of the golden corpus.

`G0.CASE-0.MATRIX` is the constitution of the golden cases, written before any
case exists. It freezes what must be covered along three independent axes: every
one of the eighteen laws in every one of the five standings, ninety cells of
which fifty-six are reachable and thirty-four are refused with a named reason;
an independent reachability witness for each of the five case dispositions
`PASS`, `BLOCK`, `DEFER`, `INVALID_INPUT` and `INVARIANT_ERROR`; and seven
separations between the stages, such as `BLOCK` never producing a materialized
identity and a blocked dependent law never producing a residual. The three
layers are separately typed and never collapsed — `CheckStanding →
VerdictEffect → CaseDisposition` — so a law read `SATISFIED` states only that it
forces nothing on the aggregate, never that the case passes, since another law
may be violated and the aggregate reads `BLOCK > DEFER > PASS`. Each reachable
cell also names the standings forbidden alongside it, read in the law's frozen
evaluation scope: a subject-scoped law may hold at one site and fail at another,
but never both at the same site in the same reading. No cell names a case: `case_id` is `None`
throughout, and no engine module may import the matrix. The order is
deliberate — the specification precedes the cases, and the cases precede the
first engine readout — so that a later agreement is evidence rather than an
expectation edited after seeing the result.

`G0.CASE-0.DATA` derives the corpus from that frozen matrix, one stage before
the engine has run once: `MATRIX ≺ DATA ≺ READOUT ≺ DIGEST LEDGER`. The golden
cases are reviewed `JSON` files under `case_data/`, never the output of Python
builders, and no execution digest appears anywhere in them — a digest is born of
the readout, and admitting it here, even as `None`, would merge two stages. Four
independent types carry the corpus: a case holds its document alone; an
expectation, frozen before any reading, holds the disposition, the trace, the
residuals, the materialized identity and the coverage citations; an
invalid-input witness holds a document from which no case is constituted; and an
engine-seam witness, for the internal invariant error, holds no document at all,
since that error is not in the space of user cases. A counter-case is a valid
baseline plus exactly one declared difference, and two differences are admitted
only where multiplicity is itself the proof — one law satisfied on one subject
and violated on another. A citation is a *claim* of coverage: the data checker
proves only that it is legitimate against the matrix and coherent with the
case's own frozen expectation, and the readout alone will prove that the case
actually reached the cell. What the first tranche does not yet cover is named in
`case_data/MANIFEST.json`, and the checker refuses any drift between that
declared residual and the residual derived from the citations.

`G0.CASE-0.DATA-H` hardens that layer before the remaining cases are written.
The documents are now frozen transitively rather than nominally — read-only
mappings and tuples, projected afresh on every read — so a later readout cannot
rewrite the evidence it is measured against. And a declared difference is no
longer the author's word: the two authored documents are compared directly and
the difference is typed — `ADD`, `REMOVE` or `REPLACE` at a named path, with the
content before and after — so an added anchor is `ADD nisbah.anchors[1]` rather
than a vague change of length, and an element changed beside an element added is
two differences. The declaration must equal that actual difference exactly, the
comparison is one hop to the named baseline, and any cycle in the baseline graph
is refused. Expected input faults are read as members of the existing closed
`InputFaultKind` vocabulary, and `INVALID_INPUT` is now named as constitutional
invalidity — the case never came into being — rather than as a corrupted
process, which is where `BLOCK` belongs.

`G0.CASE-0.DATA-HH` closes the remaining ways around those gates. Freezing now
happens inside the classes themselves, not only inside their readers, so the
general Python constructor cannot be handed a live dictionary and keep a handle
on it. `NaN` and `±Infinity` are refused at the freeze, since they are not
`JSON` numbers even though Python's reader accepts them. And the structural
difference deliberately stays unclever: because it is positional and knows
nothing of element identity, a list may change its tail or change a standing
position, but not both at once, and a mid-list insertion or removal is refused
until an explicit `SequenceIdentityPolicy` settles whether a list position is an
identity or merely an order. Finally, the two Arabic phrases inside the frozen
coverage matrix are recorded as legacy wording rather than corrected: they enter
`COVERAGE_MATRIX_DIGEST`, and rewriting a frozen specification to improve its
language would breach `MATRIX ≺ DATA`.

`G0.CASE-0.DATA-1` is the first growth of the corpus after those gates. Five
counter-cases are authored against the single baseline: a duplicated anchor id,
an arity that exceeds its own slots, an argument place named after a deferred
role, an absent condition site declared as a standing requirement, and a role
site naming a licence the ontology never granted. Each is an input that stands
as a case and is then judged; each is measured one hop against
`case0.baseline.pass`, with its difference proved from the two texts rather than
asserted. The corpus now reaches all three verdicts a standing case can reach,
and the residual falls from forty-three requirements to thirty-one. Every
expected trace is authored from the frozen law set, not derived — no engine was
run to write a row, and each cell claimed remains a claim until
`G0.CASE-0.READOUT`.

`G0.CASE-0.DATA-1H` corrects that tranche before it grows further, without
moving either frozen digest. The duplicated-anchor case was an impure witness:
the frozen law computes a count bound *and* an identity-uniqueness clause under
one name, and two anchors against `arity: 2` never exceeded the bound at all, so
the case proved the unnamed half of the law. It is withdrawn and replaced by a
clean chain — a second uniquely named anchor, expected to pass, and then a third
that violates the bound at `3 > 2` — which also settles that `baseline_case_id`
is the immediate structural parent, not the root. The conflation itself is kept
as the named architectural residual
`RES.RUN0.AnchorArityConflatesIdentityUniqueness`, with the withdrawn document
preserved outside the corpus as its evidence. Second, the unit of the experiment
is now the *perturbation* rather than the structural difference: one authored
change of meaning may need more than one surface operation to keep the case well
formed, so each counter-case carries a nested `perturbation` whose
`atomicity_kind` is one of `SINGLE_OPERATION`,
`COMPOUND_CONSTITUTION_PRESERVATION_CLAIM` or `MULTIPLICITY_IS_THE_PROOF` — the
last reserved for cases where the multiplicity is itself what is proved. And
third, the rank is kept behind its evidence: `DATA` declares a perturbation and
names an *expected-pass* baseline, while only `READOUT` can license either.
That last law is now enforced rather than merely written — a case whose frozen
expectation is `BLOCK` or `DEFER` can no longer serve as anyone's baseline — and
what the gate establishes is bounded to the author's expectation, not to
success, so the order reads `MATRIX ≺ Authored DATA ≺ DeclaredPerturbation ≺
ExpectedPassParent ≺ READOUT ≺ VerifiedPassParent ≺ LicensedPerturbation ≺
DIGEST LEDGER`. For the same reason an authored case no longer calls its own
input *standing*: `Authored ⇏ Valid`, exactly as `Declared ⇏ Licensed`.

`G0.GEN-0.SPEC` opens the second direction over the same structure. Until now
every layer read a surface and asked what licensed it; this one produces a
surface from a structure that a previous execution already judged. It is a
specification only — primitives, laws and gates, with synthetic tests and no
Arabic datum. The first law is that the new direction is not the old one
inverted: `Analysis ≠ Generation⁻¹`. The entry point is therefore not a
structure but a verdict — a `PassedNisbahSourceRef` that can be minted only from
an execution envelope whose outcome is `PASS` with a materialized identity —
and the specification stays thin, restating neither the relation nor its
anchors, and writing neither its own rank nor its own residuals. Roles are not
opened: `فاعل ≠ Agent` and `مفعول به ≠ Patient` always, so generation binds an
anchor identity to a syntactic *position* without redescribing it semantically.
The unrealized layers branch rather than block — phonology is withheld while
orthography may still be produced from a frozen lexical form — and `withheld` is
a type, not a flag, so `GeneratedStage[T] ≠ WithheldStage` structurally. No
morphology is claimed: only `LEXICALLY_ATTESTED_FORM_SELECTION`, never
`DERIVED_FROM_ROOT`. Three ranks are separated as types, and the third is
deliberately unreachable: the round-trip certificate requires an analyser that
recovers function, which cannot exist while the corpus tags case rather than
function, so `RoundTripGate` returns exactly one named deferral. The frozen
first family is `PastActiveTransitiveVSO`, and the axis runs
`SPEC ≺ DATA ≺ READOUT ≺ RT` under one highest law:
`NoGenerationAuthorityBeyondItsSource`.

`G0.GEN-0.SPEC-H` reviews that specification and lowers three of its claims to
the rank the evidence supports, changing no goal — and it is the last hardening
of the linear generator, not a step toward a large `GEN-0` corpus. First, a
contract must bind the type and not the road that builds it:
`PassedNisbahSourceRef` and `ProductionSpecification` were freely constructible,
so the envelope check and the source-membership check could both be walked
around; both are now closed by an internal issuance capability that never enters
canonical content, and every source check moves into the constructor, covering
the lexical choices and the realization constraints the factory never examined.
The source is no longer summarized by a digest alone — a digest proves the
inventory's identity without saying what is in it — but carried as a certified
projection, `SourceInventorySnapshot`, a tuple of `SourceElementRef(element_id,
element_kind)` with a derived content id, so the specification re-checks its own
targets, choices and constraints against it. Second, the second rank was named
for a licence it never issued: the gate reads the realization targets the caller
wrote and then verifies the product honours them, so `CallerClaim →
ConformsToCallerClaim ⇏ Licensed`. It is renamed `SpecificationConformantSurface`
behind a `SpecificationConformanceGate`, with no compatibility aliases, since the
problem was an epistemic claim and not an API name; `StructurallyLicensedSurface`
is reserved by text until an independent `SyntacticBindingCertificate` exists.
Third, what the layer cannot prove is separated from what a run observed:
`GenerationAuthorityGap` in `generation/authority_gaps.py` is an *architectural*
gap with a claim, a missing authority and a discharge condition, distinct in type
from the observed `GenerationResidual`, and two are frozen —
`RES.GEN0.NoIndependentAnchorToSyntacticFunctionAuthority` (nothing in the source
binds an anchor to subjecthood or objecthood, so the gate conforms an inverted
assignment just as readily, and a test witnesses it) and
`RES.GEN0.NoVerifiedLexicalAttestation` (`LexicalChoiceRef_SPEC ≠
VerifiedLexicalChoice_READOUT`). Every conformant decision carries both as
`open_authority_gaps`, so the rank carries its own boundary. Provenance is closed
structurally rather than by a repeated check: `GeneratedArabicUtterance` no
longer holds `orthographic_content_id` and `tokens` as two claims that may drift
apart, it holds the `OrthographicProjection` itself and derives both from it, and
its construction requires that the trace start at the specification digest and
end at an orthographic-projection step whose output is that projection's digest.
The historical `G0.GEN-0` law set is left untouched; the revision is a second law
set, `G0.GEN-0.SPEC-H`, with its own digest. The order reads `GEN-SPEC ≺ GEN-DATA
≺ LexicalVerification ≺ GenerationReadout ≺ SpecificationConformance ≺
SyntacticLicensing ≺ RoundTripCertification`, under `ConformanceIsNotLicensing`,
and the next milestone is not `GEN-0.DATA` but `G0.FGEN-0.SPEC`, where this line
becomes the base case of a fractal generation under `LinearGeneration ⊂
FractalGeneration`.

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
ruff format --check .
mypy src
```

See [`docs/CONSTITUTION.md`](docs/CONSTITUTION.md) for the initial
constitutional laws governing the kernel.
