"""الإبطالُ المتسلسل فوق الرصيد القائم: يسقط الاشتقاقُ وحدَه، ويُحفَظ التاريخ.

وحالُ المصدرِ غيرُ حال الاشتقاق غيرُ حال الدعوى؛ فسحبُ شاهدٍ لا يُكذِّب كلَّ
ما نُقل عنه، وغيابُ السند جهلٌ لا نفي.
"""

from __future__ import annotations

from alghanem.arabic.excerpt_origin_bridge import locate
from alghanem.arabic.witness_retraction_run import (
    THE_CLAIM,
    base_stock,
    carrier_rule,
    mirror_witness,
    primary_witness,
    read_state,
    run,
)
from alghanem.arabic.word_certificate_chain import (
    WitnessGate,
    measured_features,
    tanwin_reading,
    witness_source_of,
)
from alghanem.ontology.accumulation import ClaimStanding

_PRIMARY_EVIDENCE = "دليل-شاهد-المصحف-المبسّط"
_MIRROR_EVIDENCE = "دليل-شاهد-النسخة-الموازية"
_DERIVED = "حكم-بطاقة-الحوامل"
_DEPENDENT = "شهادة-تابعة-للحكم"
_INDEPENDENT = "حكم-الإزاحة-المستقلّ"
_SUPPORT = "سند-الدعوى-من-الشاهد-الأوّل"


def _suspended(stock: object) -> set[str]:
    return set(read_state(stock, "ل").suspended_ids)  # type: ignore[arg-type]


# ١ — الحالُ الصحيحةُ تقوم على شاهدَين مرّت بوّاباتُهما


def test_the_scenario_rests_on_witnesses_that_passed_their_five_gates() -> None:
    """لا يُبنى الإبطالُ على شاهدٍ لم يُقبَل ابتداءً."""

    for witness in (primary_witness(), mirror_witness()):
        source = witness_source_of(witness.source_key)
        located = locate(witness.locus, source=source.source)
        measured = measured_features(located, tanwin_reading(located.surface))
        audit = witness.audit(measured)
        assert audit.admitted is True
        assert audit.failed_gates == ()
        assert set(WitnessGate) == {one.gate for one in audit.gates}


def test_the_sound_state_supports_the_claim_by_two_independent_families() -> None:
    """الحالُ الصحيحة: سندان حيّان، وطائفتان مستقلّتان في الاشتقاق."""

    state = read_state(base_stock(), "الحالُ الصحيحة")
    assert state.claim_standing is ClaimStanding.SUPPORTED_IN_SCOPE
    assert state.independent_families == 2
    assert state.suspended_ids == ()


# ٢ — سحبُ الشاهد يُبطل اشتقاقَه وحدَه


def test_retracting_the_first_witness_suspends_only_its_derivations() -> None:
    """يسقط التابعُ بسقوط متبوعه، ويبقى المستقلُّ قائمًا بلا مساس."""

    withdrawn = base_stock().retract_evidence(_PRIMARY_EVIDENCE)
    suspended = _suspended(withdrawn)
    assert {_SUPPORT, _DERIVED, _DEPENDENT} <= suspended
    assert _INDEPENDENT not in suspended
    assert _MIRROR_EVIDENCE not in suspended


def test_the_claim_survives_on_the_alternative_support_alone() -> None:
    """تبقى الدعوى مدعومةً إن كفاها السندُ البديل، بطائفةٍ واحدة لا طائفتين."""

    state = read_state(base_stock().retract_evidence(_PRIMARY_EVIDENCE), "بعد السحب")
    assert state.claim_standing is ClaimStanding.SUPPORTED_IN_SCOPE
    assert state.live_supports == ("سند-بديل-من-النسخة-الموازية",)
    assert state.independent_families == 1


def test_no_derivation_that_cites_the_withdrawn_witness_stays_live() -> None:
    """ولا تبقى شهادةٌ تحتجّ بالشاهد المسحوب صالحةً بعد سحبه."""

    withdrawn = base_stock().retract_evidence(_PRIMARY_EVIDENCE)
    live = set(read_state(withdrawn, "بعد السحب").live_supports)
    assert _SUPPORT not in live
    assert _DEPENDENT not in live


# ٣ — سحبُ البديل يُعلّق الدعوى، ولا يُكذّبها


def test_retracting_the_alternative_suspends_the_claim_without_refuting_it() -> None:
    """غيابُ السند جهلٌ لا نفي: لا دعمَ ولا نفي، والمستقلُّ على حاله."""

    stripped = (
        base_stock()
        .retract_evidence(_PRIMARY_EVIDENCE)
        .retract_evidence(_MIRROR_EVIDENCE)
    )
    state = read_state(stripped, "بعد سحب البديل")
    assert state.claim_standing is ClaimStanding.UNKNOWN
    assert state.live_supports == ()
    assert _INDEPENDENT not in state.suspended_ids


# ٤ — نقضُ اعتماد القاعدة يُعلّق ما اشتُقّ بها وحدَه


def test_revoking_the_rule_adoption_suspends_only_what_it_derived() -> None:
    """لا يُعاد اعتمادُ شهادةٍ بُنيت على إصدارٍ سقط اعتمادُه."""

    revoked = base_stock().revoke_adoption(carrier_rule().versioned_id)
    suspended = _suspended(revoked)
    assert {_DERIVED, _DEPENDENT} <= suspended
    assert _SUPPORT not in suspended
    state = read_state(revoked, "بعد النقض")
    assert state.claim_standing is ClaimStanding.SUPPORTED_IN_SCOPE


# ٥ — التصحيحُ إصدارٌ جديدٌ، والتاريخُ محفوظ


def test_the_correction_deposits_a_new_version_and_keeps_the_history() -> None:
    """تصحيحُ الشاهد يُنشئ إصدارًا ثانيًا ويُعلّق القديمَ ولا يمحوه."""

    outcome = run()
    corrected = outcome.readings[-1]
    assert corrected.claim_standing is ClaimStanding.SUPPORTED_IN_SCOPE
    assert "سند-الدعوى-من-الشاهد-الأوّل-إصدار-ثانٍ" in corrected.live_supports
    assert _SUPPORT in corrected.suspended_ids


def test_every_state_moves_the_content_identity_of_the_stock() -> None:
    """كلُّ حالٍ هويّةُ محتوًى أخرى، فلا تُعاد حالٌ قديمةٌ بإعادةِ بصمها."""

    identities = {one.stock_content_id for one in run().readings}
    assert len(identities) == len(run().readings)


def test_the_run_declares_its_limits_and_does_not_claim_knowledge() -> None:
    """الحدودُ مُعلَنةٌ في المخرج: نجاحُ السيناريو ليس إثباتًا لصحّة معرفة."""

    outcome = run()
    assert len(outcome.limits) == 3
    assert all(one.strip() for one in outcome.limits)
    assert len(outcome.lines) == len(outcome.readings) == 5


def test_the_claim_subject_and_predicate_are_named_not_implied() -> None:
    """الدعوى مُعرَّفةٌ بموضوعها ومحمولها ونطاقها، لا تُستنتَج من سياق."""

    assert THE_CLAIM.subject_id
    assert THE_CLAIM.predicate_id
