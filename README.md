# Alghanem

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

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
ruff format --check .
mypy src
```

See [`docs/CONSTITUTION.md`](docs/CONSTITUTION.md) for the initial
constitutional laws governing the kernel.
