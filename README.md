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
runs the full 5 × 5 type matrix over seven named coordinate configurations
(`adjacent`, `distant`, `at_zero`, `same_coordinate`, `descending`,
`upper_edge`, `append_edge`) on a six-atom sequence, excluding identical
interventions by declaration, and reports 41 commuting pairs, 102 critical
pairs (`overlap` or `shift`), and 8 undefined pairs across 151 configured
pairs, with every predicted verdict confirmed by `observe_commutation`
applying both orders through the real application path (MATCH_ALL, 151/151).
The scope is declared, not silently widened: the model reads coordinates and
not values, so a sequence with repeated atoms can make two orders agree by
**value coincidence** rather than structural commutation. That limit is
recorded in `VALUE_COINCIDENCE_NOTE` and demonstrated by an explicit test,
and the reference matrix therefore runs on distinct atoms only.

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
