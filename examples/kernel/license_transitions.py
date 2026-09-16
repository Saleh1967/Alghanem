"""جبرُ التحويلات المُرخَّصة، مُطبَّقًا على خمس حالاتٍ تُشغَّل لا تُوصَف.

سكربتٌ مرجعيٌّ لا سلطةَ له: لا يُولِّد كائنًا، ولا يُجمِّد `E0`، ولا يُصدر
`CertifiedOutcome`، ولا يُقاس به شيءٌ على مدوّنة. وهو يستورد `kernel/` وحدَه،
ولا يقرأ طبقةَ العربيّة ولا يُقرَأ منها؛ والعربيّةُ في حمولاته **مادّةُ مثالٍ
معتمةٌ** يمرّرها الجبرُ ولا يفهمها، فالجبرُ لغةً-محايدٌ كما هو مكتوبٌ في
`docs/CONSTITUTION.md`.

والمقصودُ إظهارُ الفروق التي يقوم عليها الجبرُ **بتشغيلها** لا بشرحها:

* **`DeclaredInvariant != VerifiedInvariant`** (الحالتان ١ و٢): دعوى حفظٍ
  مكتوبةٌ في `preserved` تعبر القبولَ البنيويَّ سليمةً، ثمّ تُفنَّد عند الفحص
  المستقلّ. فالقبولُ البنيويُّ حسنُ صياغةٍ لا صدقُ مضمون.
* **الرفضُ يُسجَّل ولا يُرفَع استثناءً** (الحالة ٣): البوّابةُ تُرجِع `BLOCK`
  ومعه `NonSuccessDecisionAudit` بأثرِ المرشَّح نفسِه وبقاياه وسببٍ غيرِ
  فارغ؛ فلا يضيع موضعُ الرفض.
* **`StructuralAdmission != CertifiedBranchBirth`** (الحالة ٤): دعوى ولادةِ
  فرعٍ تُقبَل بنيويًّا ببيّنةِ أصلٍ صريحة، ولا تصير بذلك ولادةً مُصدَّقة؛
  بوّابةُ الحكم مؤجَّلةٌ خارج هذا المستوى.
* **`Unauthorized != Disproved`** (الحالة ٥): مستخرِجٌ مُسجَّلٌ غيرُ مُرخَّصٍ
  لنطاقه يُخرِج `DEFER` لا `BLOCK`؛ ثمّ إذا اجتمع مُفنَّدٌ ومتعذّرٌ في
  انتقالٍ واحدٍ غلب `BLOCK` (`False ∧ Unknown == False`).

    python examples/kernel/license_transitions.py
"""

from __future__ import annotations

from typing import Final

from alghanem.kernel import (
    Anchor,
    BranchOriginProvenance,
    Claim,
    Evidence,
    InvariantExtractorRegistry,
    InvariantSpec,
    InvariantVerificationDecision,
    InvariantVerificationGate,
    Operation,
    OperationResult,
    RegisteredInvariantDefinition,
    SealedInvariantExtractorRegistry,
    State,
    StructuralAdmissionDecision,
    StructuralAdmissionGate,
    Trace,
    TransitionCandidate,
    TransitionKind,
)

SURFACE_DOMAIN: Final[str] = "arabic_surface"
SYLLABLE_DOMAIN: Final[str] = "arabic_syllable"

SKELETON: Final[str] = "consonantal_skeleton"
MARKS: Final[str] = "diacritic_marks"
LETTER_COUNT: Final[str] = "letter_count"
LAYER: Final[str] = "layer_of_reading"

SKELETON_INVARIANT: Final[str] = "skeleton_survives_mark_stripping"
SKELETON_ACROSS_LAYERS: Final[str] = "skeleton_survives_layer_birth"
COUNT_INVARIANT: Final[str] = "letter_count_survives_mark_stripping"

SKELETON_EXTRACTOR: Final[str] = "skeleton_of_state"
COUNT_EXTRACTOR: Final[str] = "letter_count_of_state"


def _payload(state: State) -> dict[str, object]:
    value = state.value
    if not isinstance(value, dict):
        raise TypeError("هذا المثال يقرأ حمولةً من نوع dict")
    return value


def _skeleton_of(state: State) -> object:
    """استخرِج الهيكلَ الساكن من أيٍّ من صورتَي الحمولة في هذا المثال.

    البوّابةُ — لا المرشَّح — تملك الاستخراجَ والمقارنة، فالمستخرِجُ واحدٌ
    يُطبَّق على الحالتين قبلَ وبعد. وقراءتُه صورتين (حروفٌ متتابعةٌ، أو مقاطعُ
    تُوصَل) هي ما يجعل الفحصَ عبر طبقتين ممكنًا أصلًا في الحالة ٤.
    """

    payload = _payload(state)
    letters = payload.get("letters")
    if isinstance(letters, str):
        return letters
    syllables = payload.get("syllables")
    if isinstance(syllables, tuple):
        return "".join(str(syllable) for syllable in syllables)
    raise KeyError("لا حروفَ ولا مقاطعَ في الحمولة")


def _letter_count_of(state: State) -> object:
    return len(str(_skeleton_of(state)))


def sealed_registry() -> SealedInvariantExtractorRegistry:
    """سجلٌّ مختومٌ: التسجيلُ يُتيح الحلَّ، والترخيصُ وحدَه يُتيح الفحص.

    `COUNT_EXTRACTOR` مُسجَّلٌ عمدًا **بلا ترخيصٍ** لأيّ نطاق، ليُظهِر في
    الحالة ٥ أنّ «مُسجَّلٌ غيرُ مُرخَّص» يُرفَض كما يُرفَض «غيرُ مُسجَّل»،
    وأنّ رفضَه تعذّرٌ لا تفنيد.
    """

    registry = InvariantExtractorRegistry()
    registry.register(SKELETON_EXTRACTOR, _skeleton_of)
    registry.register(COUNT_EXTRACTOR, _letter_count_of)
    for invariant_id in (SKELETON_INVARIANT, SKELETON_ACROSS_LAYERS):
        registry.authorize(
            RegisteredInvariantDefinition(
                domain=SURFACE_DOMAIN,
                component=SKELETON,
                invariant_id=invariant_id,
                extractor_id=SKELETON_EXTRACTOR,
            )
        )
    return registry.seal()


def strip_marks_candidate(
    *,
    before_letters: str,
    after_letters: str,
    preserved: tuple[str, ...] = (SKELETON,),
    claim_id: str = "CLAIM-STRIP-MARKS",
    evidence_claim_id: str | None = None,
) -> TransitionCandidate:
    """مرشَّحُ «تجريدِ التشكيل»: دعوى حفظِ هيكلٍ مع تغييرِ علاماتٍ مُعلَن.

    `after_letters` مُعامِلٌ لأنّ هذا المثال يُشغِّل صورتين من العملية نفسِها:
    واحدةٌ تحفظ الهيكلَ فعلًا، وأخرى تُسقِط حرفًا وتبقى دعواها مكتوبةً كما
    هي — والفرقُ بينهما لا يظهر في القبول البنيويّ، بل في الفحص المستقلّ.
    """

    anchor = Anchor(identifier="كَتَبَ", domain=SURFACE_DOMAIN)
    claim = Claim(
        claim_id=claim_id,
        statement="تجريدُ التشكيل يُغيّر العلاماتِ ويحفظ الهيكلَ الساكن",
    )
    bound_claim_id = claim_id if evidence_claim_id is None else evidence_claim_id
    evidence = (
        Evidence(
            claim_id=bound_claim_id,
            basis="قراءةُ الحمولتين قبلَ العملية وبعدَها",
        ),
    )
    before = State({"letters": before_letters, "marks": ("\u064e",) * 3})
    after = State({"letters": after_letters, "marks": ()})
    return TransitionCandidate(
        anchor=anchor,
        before_state=before,
        operation=Operation(
            name="تجريد التشكيل",
            declared_change=MARKS,
            source_domain=SURFACE_DOMAIN,
            target_domain=SURFACE_DOMAIN,
        ),
        after_state=after,
        claim=claim,
        evidence=evidence,
        preserved=preserved,
        changed=(MARKS,),
        trace=Trace(("قُرئت الحمولةُ قبلَ العملية", "أُجريت العمليةُ وسُجِّل ناتجُها")),
        residuals=(),
        kind=TransitionKind.IDENTITY_PRESERVATION_CLAIM,
        result=OperationResult(after.value),
        target_anchor=anchor,
    )


def syllable_birth_candidate() -> TransitionCandidate:
    """مرشَّحُ ولادةِ فرعٍ: طبقةُ المقاطع من طبقة السطح، ببيّنةِ أصلٍ صريحة.

    حمولةُ الفرع تُبقي الهيكلَ مفصولًا عن حركاته، فيقرأ المستخرِجُ الواحدُ
    الطبقتين بلا قاعدةٍ عربيّةٍ مُقحَمةٍ فيه. ولو مُزِجت الحركاتُ بالهيكل
    لخرج الفحصُ `BLOCK` — لا لأنّ الطبقةَ كاذبةٌ بل لأنّ التعريفَ المُستخرَجَ
    به تغيّر؛ وهذا بعينه ما يجعل نصَّ التعريف جزءًا من الدعوى لا حاشيةً لها.
    """

    origin = Anchor(identifier="كَتَبَ", domain=SURFACE_DOMAIN)
    branch = Anchor(identifier="كَتَبَ/مقاطع", domain=SYLLABLE_DOMAIN)
    claim = Claim(
        claim_id="CLAIM-SYLLABLE-BIRTH",
        statement="قراءةُ المقاطع طبقةٌ جديدةٌ تحفظ الهيكلَ الساكن لأصلها",
    )
    before = State({"letters": "كتب", "marks": ("\u064e",) * 3})
    after = State({"syllables": ("ك", "ت", "ب"), "nuclei": ("\u064e",) * 3})
    return TransitionCandidate(
        anchor=origin,
        before_state=before,
        operation=Operation(
            name="تقطيعٌ إلى مقاطع",
            declared_change=LAYER,
            source_domain=SURFACE_DOMAIN,
            target_domain=SYLLABLE_DOMAIN,
        ),
        after_state=after,
        claim=claim,
        evidence=(
            Evidence(
                claim_id=claim.claim_id,
                basis="مقابلةُ حروف الأصل بوصلِ مقاطع الفرع",
            ),
        ),
        preserved=(SKELETON,),
        changed=(LAYER,),
        trace=Trace(("قُرئ السطحُ", "قُطِّع إلى مقاطعَ وسُجِّلت")),
        residuals=(),
        kind=TransitionKind.BRANCH_BIRTH_CLAIM,
        result=OperationResult(after.value),
        branch_origin_provenance=BranchOriginProvenance(
            origin_anchor=origin,
            branch_anchor=branch,
            preserved_components=(SKELETON,),
        ),
        target_anchor=branch,
    )


def _print_structural(label: str, decision: StructuralAdmissionDecision) -> None:
    print(f"\n{label}")
    print(f"  القرارُ البنيويّ: {decision.status.name}")
    transition = decision.transition
    if transition is None:
        audit = decision.audit
        if audit is None:  # pragma: no cover - البوّابةُ لا تُرجِع رفضًا بلا تدقيق
            raise AssertionError("رفضٌ بلا تدقيقٍ مُسجَّل")
        print(f"  السبب: {audit.reason}")
        print(f"  الأثرُ المحفوظ: {len(audit.trace.events)} حدثًا")
        return
    print(f"  الدعوى المُسمّاة: {transition.kind.name}")
    print(f"  محفوظٌ: {'، '.join(transition.preserved)}")
    print(f"  مُغيَّرٌ: {'، '.join(transition.changed)}")


def _print_invariant(label: str, decision: InvariantVerificationDecision) -> None:
    print(f"  {label}: {decision.status.name} — {decision.reason}")
    if decision.failed_components:
        print(f"    مُفنَّدٌ: {'، '.join(decision.failed_components)}")
    if decision.deferred_components:
        print(f"    متعذّرٌ: {'، '.join(decision.deferred_components)}")


def run() -> dict[str, str]:
    """شغِّل الحالاتِ الخمسَ وأرجِع اسمَ قرارِ كلٍّ منها لا نصًّا مسرودًا."""

    registry = sealed_registry()
    statuses: dict[str, str] = {}

    faithful = StructuralAdmissionGate.assess(
        strip_marks_candidate(before_letters="كتب", after_letters="كتب")
    )
    _print_structural("الحالة ١ — تجريدُ تشكيلٍ حفظ الهيكل", faithful)
    statuses["case_1_admission"] = faithful.status.name
    faithful_transition = faithful.transition
    assert faithful_transition is not None
    verified = InvariantVerificationGate.assess_all_preserved(
        faithful_transition,
        (
            InvariantSpec(
                invariant_id=SKELETON_INVARIANT,
                component=SKELETON,
                extractor_id=SKELETON_EXTRACTOR,
            ),
        ),
        registry,
    )
    _print_invariant("الفحصُ المستقلّ", verified)
    statuses["case_1_invariant"] = verified.status.name

    lossy = StructuralAdmissionGate.assess(
        strip_marks_candidate(
            before_letters="كتب",
            after_letters="كب",
            claim_id="CLAIM-STRIP-MARKS-LOSSY",
        )
    )
    _print_structural("الحالة ٢ — الدعوى نفسُها وقد سقط حرفٌ", lossy)
    statuses["case_2_admission"] = lossy.status.name
    lossy_transition = lossy.transition
    assert lossy_transition is not None
    disproved = InvariantVerificationGate.assess_all_preserved(
        lossy_transition,
        (
            InvariantSpec(
                invariant_id=SKELETON_INVARIANT,
                component=SKELETON,
                extractor_id=SKELETON_EXTRACTOR,
            ),
        ),
        registry,
    )
    _print_invariant("الفحصُ المستقلّ", disproved)
    statuses["case_2_invariant"] = disproved.status.name

    misbound = StructuralAdmissionGate.assess(
        strip_marks_candidate(
            before_letters="كتب",
            after_letters="كتب",
            evidence_claim_id="CLAIM-SOMETHING-ELSE",
        )
    )
    _print_structural("الحالة ٣ — بيّنةٌ مربوطةٌ بدعوى أخرى", misbound)
    statuses["case_3_admission"] = misbound.status.name

    birth = StructuralAdmissionGate.assess(syllable_birth_candidate())
    _print_structural("الحالة ٤ — دعوى ولادةِ فرعٍ ببيّنةِ أصل", birth)
    statuses["case_4_admission"] = birth.status.name
    birth_transition = birth.transition
    assert birth_transition is not None
    survived = InvariantVerificationGate.assess_all_preserved(
        birth_transition,
        (
            InvariantSpec(
                invariant_id=SKELETON_ACROSS_LAYERS,
                component=SKELETON,
                extractor_id=SKELETON_EXTRACTOR,
            ),
        ),
        registry,
    )
    _print_invariant("الفحصُ المستقلّ عبر الطبقتين", survived)
    statuses["case_4_invariant"] = survived.status.name
    print("  القبولُ البنيويُّ ليس ولادةً مُصدَّقة: بوّابةُ الحكم خارج هذا المستوى.")

    print("\nالحالة ٥ — المتعذّرُ ليس مُفنَّدًا، وإذا اجتمعا غلب التفنيد")
    unauthorized = InvariantVerificationGate.assess_all_preserved(
        faithful_transition,
        (
            InvariantSpec(
                invariant_id=COUNT_INVARIANT,
                component=SKELETON,
                extractor_id=COUNT_EXTRACTOR,
            ),
        ),
        registry,
    )
    _print_invariant("مستخرِجٌ مُسجَّلٌ بلا ترخيص", unauthorized)
    statuses["case_5_unauthorized"] = unauthorized.status.name

    mixed_admission = StructuralAdmissionGate.assess(
        strip_marks_candidate(
            before_letters="كتب",
            after_letters="كب",
            preserved=(SKELETON, LETTER_COUNT),
            claim_id="CLAIM-STRIP-MARKS-MIXED",
        )
    )
    mixed_transition = mixed_admission.transition
    assert mixed_transition is not None
    mixed = InvariantVerificationGate.assess_all_preserved(
        mixed_transition,
        (
            InvariantSpec(
                invariant_id=SKELETON_INVARIANT,
                component=SKELETON,
                extractor_id=SKELETON_EXTRACTOR,
            ),
            InvariantSpec(
                invariant_id=COUNT_INVARIANT,
                component=LETTER_COUNT,
                extractor_id=COUNT_EXTRACTOR,
            ),
        ),
        registry,
    )
    _print_invariant("مُفنَّدٌ ومتعذّرٌ معًا", mixed)
    statuses["case_5_mixed"] = mixed.status.name

    return statuses


def main() -> None:
    run()


if __name__ == "__main__":
    main()
