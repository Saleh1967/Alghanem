"""شواهدُ سجلّ مختبر الاكتشاف: تُصادم السجلَّ ولا تنقل ما فيه."""

from __future__ import annotations

import json

import pytest

from alghanem.arabic.discovery_lab_ledger import (
    THE_DEMO_TAG,
    THE_LEDGER_RELATIVE_PATH,
    THE_RESULT_BEARING_FIELDS,
    THE_ROOT_DIGEST,
    EntryKind,
    LedgerError,
    RunStanding,
    audit_of,
    chain_breaks,
    counted_runs,
    demo_runs,
    entry_by_id,
    ledger_path,
    link_digest,
    read_ledger,
    registrations_naming_their_outcome,
    rung_standing,
)


def test_the_deposited_ledger_is_present_where_the_lab_looks_for_it() -> None:
    """موضعُ السجلّ واحدٌ في الوحدتين، وإلّا قاس كلٌّ منهما غيرَ ما يقيس الآخر."""

    from alghanem.arabic.discovery_lab import THE_RUN_LEDGER

    assert THE_RUN_LEDGER == THE_LEDGER_RELATIVE_PATH
    assert ledger_path().is_file()


def test_the_chain_is_unbroken_from_the_root_to_the_last_link() -> None:
    """بصمةُ كلّ حلقةٍ تضمّ سالفتها؛ فانقطاعٌ واحدٌ يكشف إقحامًا أو تبديلًا."""

    assert chain_breaks() == ()
    entries = read_ledger()
    assert entries[0].previous == THE_ROOT_DIGEST
    for earlier, later in zip(entries, entries[1:]):
        assert later.previous == earlier.digest


def test_a_tampered_payload_breaks_its_own_link_and_everything_after() -> None:
    """السلسلةُ تُصادَم لا تُوصَف: تبديلُ حمولةٍ يقلب بصمتَها فيُكشَف."""

    entries = read_ledger()
    target = entries[1]
    tampered = dict(target.payload)
    tampered["المسألة"] = "مسألةٌ أُبدِلت بعد الختم"
    assert (
        link_digest(
            target.previous,
            target.stamp,
            target.entry_id,
            target.kind.value,
            tampered,
        )
        != target.digest
    )


def test_no_pre_registration_names_its_own_outcome() -> None:
    """بندُ تسجيلٍ يحمل نتيجتَه تقريرٌ لا تسجيل، ويُكشَف بحقوله."""

    assert registrations_naming_their_outcome() == ()
    assert THE_RESULT_BEARING_FIELDS


def test_the_first_run_is_a_demo_that_is_tagged_and_kept() -> None:
    """الاستعراضيّةُ محفوظةٌ بوسمها، ساقطةٌ من المحتسَب، غيرُ ممحوّة."""

    demos = demo_runs()
    assert [entry.entry_id for entry in demos] == ["R0"]
    assert all(entry.tag == THE_DEMO_TAG for entry in demos)
    assert "R0" not in {entry.entry_id for entry in counted_runs()}


def test_a_run_without_a_registration_is_refused_and_not_audited() -> None:
    """جولةٌ بلا تسجيلٍ مسبقٍ لا تُصادَم مصادمةَ جولةٍ محتسَبة."""

    with pytest.raises(LedgerError):
        audit_of("R0")


def test_the_registration_precedes_its_run_in_the_chain() -> None:
    """سَبقُ البند على جولته سبقٌ في الترتيب، وهو ما تحرسه السلسلة."""

    registration = entry_by_id("R1-pre")
    run = entry_by_id("R1")
    assert registration.kind is EntryKind.PRE_REGISTRATION
    assert run.kind is EntryKind.RUN
    assert run.cites == ("R1-pre",)
    assert registration.rank < run.rank


def test_the_sealed_material_is_present_and_matches_its_registered_seal() -> None:
    """المادّةُ تُقابَل بختمها قبل أن تُقرأ؛ وخلافُ الختم ردٌّ لا تسامح."""

    audit = audit_of("R1")
    assert audit.seal_faults == ()


def test_the_recorded_count_is_re_derived_and_does_not_drift() -> None:
    """العددُ المكتوبُ يُعاد اشتقاقُه من الوصفة المسجَّلة ويُقابَل به."""

    audit = audit_of("R1")
    assert audit.recomputed_count == audit.recorded_count
    assert audit.count_drifted is False


def test_the_zero_is_only_read_after_the_instrument_is_heard() -> None:
    """ضوابطُ السمع مسجَّلةٌ قبل العدّ، وكلُّها بلغت حدَّها فالصفرُ صفرُ نصّ."""

    audit = audit_of("R1")
    assert audit.recomputed_count == 0
    assert audit.controls
    for control in audit.controls:
        assert control.heard
    assert audit.arabic_letters >= audit.arabic_letters_floor
    assert audit.instrument_is_heard is True
    assert audit.standing is RunStanding.STOOD_ON_A_HEARD_INSTRUMENT


def test_a_deaf_instrument_would_refuse_the_run_rather_than_publish_its_zero() -> None:
    """لو لم يبلغ ضابطٌ حدَّه لرُدّت الجولةُ؛ والمنزلةُ مشتقّةٌ لا مكتوبة."""

    audit = audit_of("R1")
    lowered = type(audit)(
        **{
            **{
                field: getattr(audit, field)
                for field in audit.__dataclass_fields__
                if field != "arabic_letters"
            },
            "arabic_letters": 0,
        }
    )
    assert lowered.instrument_is_heard is False
    assert lowered.standing is RunStanding.REFUSED_FOR_A_DEAF_INSTRUMENT


def test_the_literal_count_falls_on_the_lafz_and_the_near_miss_is_counted() -> None:
    """«ذكاء» صفرٌ و«ذكي» حاضرة؛ فالقريبُ يُعَدّ ولا يُطوى ليُقوَّى به النفي."""

    audit = audit_of("R1")
    found = dict(audit.near_misses_found)
    assert found.get("ذكي", 0) > 0
    assert audit.near_misses


def test_the_unmeasured_conjunct_is_recorded_as_pending_not_as_fallen() -> None:
    """شِقٌّ لم يمسّه المقياسُ يبقى في المعلَّق، ولا يُحسَب للاختبار ما لم يفعله."""

    audit = audit_of("R1")
    assert audit.pending
    assert len(audit.pending) >= 2
    assert audit.upheld
    assert audit.fell


def test_the_pending_column_is_never_empty_while_a_conjunct_is_unmeasured() -> None:
    """حصيلةٌ بلا معلَّقٍ دعوى حسمٍ تامّ؛ وهي ههنا مكذوبةٌ بنصّ البند."""

    registration = entry_by_id("R1-pre")
    second = registration.payload["الفرضان"][1]
    assert "لا يمسّه" in second["حدّ_نجاحه"]


def test_only_the_first_rung_is_reached_from_the_ledger() -> None:
    """الدرجاتُ تُقاس من بنود السجلّ: الأولى مبلوغةٌ والثلاثُ ممنوعة."""

    standings = {number: reached for number, reached, _ in rung_standing()}
    assert standings[1] is True
    for number in (2, 3, 4):
        assert standings[number] is False


def test_the_third_rung_is_blocked_although_the_ledger_is_deposited() -> None:
    """إيداعُ السجلّ ليس تراكمًا: يُشترَط بندٌ يستشهد ببندٍ من جنسه."""

    from alghanem.arabic.discovery_lab import (
        reads_a_prior_ledger,
        runs_citing_a_prior_run,
    )

    assert ledger_path().is_file()
    assert runs_citing_a_prior_run() == ()
    assert reads_a_prior_ledger() is False


def test_the_fourth_rung_is_counted_from_the_declared_domain_field() -> None:
    """حقلُ المجال هو بوّابةُ الدرجة الرابعة، ويُعَدّ منه لا يُقدَّر."""

    domains = {entry.domain for entry in counted_runs()}
    assert domains == {"tafkir-text"}
    for entry in read_ledger():
        assert entry.domain.strip()


def test_every_rung_standing_carries_a_measured_reason() -> None:
    """لا منزلةَ بلا تعليلٍ مشتقٍّ عند القراءة؛ فالإعلانُ وحدَه لا يُبلِغ درجة."""

    for number, reached, why in rung_standing():
        assert number in (1, 2, 3, 4)
        assert isinstance(reached, bool)
        assert why.strip()


def test_an_unknown_entry_is_refused_and_not_guessed() -> None:
    """معرّفٌ غائبٌ لا يُحمَل على أقرب حاضر."""

    with pytest.raises(LedgerError):
        entry_by_id("R9")


def test_the_ledger_bytes_are_valid_json_with_the_declared_link_recipe() -> None:
    """صيغةُ الحلقة مُعلَنةٌ في بايتات السجلّ نفسِها، فتُقرأ ولا تُفترَض."""

    document = json.loads(ledger_path().read_text(encoding="utf-8"))
    assert document["بصمة_الجذر"] == THE_ROOT_DIGEST
    assert "بصمة_السلف" in document["صيغة_الحلقة"]
    assert len(document["الحلقات"]) == len(read_ledger())
