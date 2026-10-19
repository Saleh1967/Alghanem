"""شواهدُ سجلِّ الإيداع المؤرَّخ: السلسلةُ تُعاد حسابًا، والأحكامُ تُشتَقّ.

تُثبِّت هذه الشواهدُ ستّة أمور: بصماتُ السجلّ مُعادةٌ من الجذر لا مُصدَّقةٌ
كما كُتبت، وتبديلُ بايتٍ واحدٍ في حمولةٍ يقطع السلسلةَ عندها وبعدها، ولا
حقلَ حكمٍ في البايتات ألبتّة فالحكمُ مشتقٌّ عند القراءة، وما لم تصل مادّتُه
لا يُقرأ موافقةً، والأعدادُ الصوريّةُ تُصادَم بتنفيذٍ ثانٍ مستقلٍّ استقصاءً،
والوحدةُ خاملةٌ سلطويًّا لا تستورد `kernel/` ولا `program/` ولا تقرأ مدوّنة.
"""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from alghanem.arabic.tawlid_algebra_ledger import (
    A_PROOF_OVER_THE_ALGEBRA_IS_NOT_A_PROOF_OVER_THE_LANGUAGE,
    AN_UNBOUNDED_EXPECTATION_CANNOT_FAIL_SO_IT_IS_NOT_ONE,
    AN_UNMEASURED_EXPECTATION_IS_NOT_A_CONFIRMED_ONE,
    PREREGISTRATION_IS_INERT_ON_WHAT_A_MACHINE_CAN_REDERIVE,
    ROOT_DIGEST,
    THE_CHAIN_ORDERS_THE_LINKS_AND_GIT_DATES_THEM,
    THE_RESERVED_PHONETIC_NAMES,
    LedgerLink,
    LinkGenus,
    LinkStanding,
    bare_positions_are_not_sukun,
    boundary_collisions_under_initial_ban,
    cell_digests,
    chain_is_unbroken,
    extras_count_forcing,
    folded_digests,
    generatorless_reserved_names,
    initial_silent_cells,
    ledger_path,
    read_deposited_ledger,
    realized_against_licensed_cells,
    recomputed_link_digests,
    shadda_sources_on_our_deposits,
    standing_of,
    standings,
    surviving_chains,
    surviving_chains_by_enumeration,
)

MODULE = Path(__file__).resolve().parents[2] / (
    "src/alghanem/arabic/tawlid_algebra_ledger.py"
)


def test_the_deposited_bytes_are_present_and_parse() -> None:
    document = json.loads(ledger_path().read_text(encoding="utf-8"))
    assert document["بصمة_الجذر"] == ROOT_DIGEST
    assert len(document["الحلقات"]) == len(read_deposited_ledger())


def test_every_written_digest_is_recomputed_from_the_root_and_matches() -> None:
    links = read_deposited_ledger()
    assert chain_is_unbroken()
    assert tuple(link.link_digest for link in links) == recomputed_link_digests()
    assert links[0].previous_digest == ROOT_DIGEST


def test_the_chain_is_shackled_so_one_altered_payload_breaks_it_onward(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = json.loads(ledger_path().read_text(encoding="utf-8"))
    document["الحلقات"][1]["الحمولة"]["العدد"] = 113
    forged = tmp_path / "ledger.json"
    forged.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(
        "alghanem.arabic.tawlid_algebra_ledger.ledger_path", lambda: forged
    )
    assert not chain_is_unbroken()
    recomputed = recomputed_link_digests()
    written = tuple(link.link_digest for link in read_deposited_ledger())
    broken = [
        index
        for index, pair in enumerate(zip(written, recomputed))
        if pair[0] != pair[1]
    ]
    assert broken and broken[0] == 1
    assert broken == list(range(1, len(written)))


def test_the_deposited_bytes_carry_no_verdict_field_at_all() -> None:
    document = json.loads(ledger_path().read_text(encoding="utf-8"))
    forbidden = {"الحكم", "الموقف", "standing", "verdict", "الحالة"}
    for entry in document["الحلقات"]:
        assert not (set(entry) & forbidden)
        assert not (set(entry["الحمولة"]) & forbidden)


def test_no_formal_link_can_agree_once_its_figure_is_moved() -> None:
    formal = [
        item for item in read_deposited_ledger() if item.genus is LinkGenus.FORMAL
    ]
    assert len(formal) >= 7
    agreeing = [
        link
        for link in formal
        if standing_of(link) is LinkStanding.REDERIVED_AND_AGREES
    ]
    assert agreeing
    for link in agreeing:
        moved = replace(link, payload={**link.payload, **_moved_figure(link)})
        assert standing_of(moved) is LinkStanding.REDERIVED_AND_DIFFERS


def test_the_differing_formal_links_are_exactly_the_two_named_refutations() -> None:
    differing = [
        link.name
        for link in read_deposited_ledger()
        if link.genus is LinkGenus.FORMAL
        and standing_of(link) is LinkStanding.REDERIVED_AND_DIFFERS
    ]
    assert differing == [
        "الفصل ١٤ · مبرهنةُ الابتداء — الشقُّ الجبريّ: " "أيولِّد الجبرُ ابتداءً ساكنًا ذرّيًّا؟",
        "الفصل ٣٧ · المتحقَّقُ ليس حقلًا",
    ]


def test_the_realized_count_moved_and_so_refuted_its_own_promotion_to_a_field() -> None:
    """١٠٨ نُصِّبت حقلًا فصارت ١١٠ بنموّ النثر وحدَه؛ فالعددُ نفسُه هو الناقض."""

    link = next(
        item for item in read_deposited_ledger() if "المتحقَّقُ ليس حقلًا" in item.name
    )
    assert link.payload["المتحقَّق"] == 108
    assert standing_of(link) is LinkStanding.REDERIVED_AND_DIFFERS


def _moved_figure(link: LedgerLink) -> dict[str, int]:
    for key in (
        "العدد",
        "البصمات_الفريدة",
        "الجذر_الوحيد",
        "الشدّات",
        "العاري_من_علامة",
        "المتحقَّق",
    ):
        if key in link.payload:
            return {key: int(link.payload[key]) + 1}
    raise AssertionError("حلقةٌ صوريّةٌ بلا عددٍ يُحرَّك")


def test_an_expectation_whose_material_is_absent_is_not_read_as_agreement() -> None:
    waiting = [
        standing
        for link, standing in standings()
        if link.genus is LinkGenus.AWAITING_ITS_MATERIAL
    ]
    assert waiting
    assert set(waiting) == {LinkStanding.ITS_MATERIAL_HAS_NOT_ARRIVED}
    assert LinkStanding.REDERIVED_AND_AGREES not in waiting


def test_the_declared_clash_is_deposited_with_both_sides_and_lifted_by_neither() -> (
    None
):
    clashes = [
        link for link, _ in standings() if link.genus is LinkGenus.DECLARED_CLASH
    ]
    assert clashes
    for clash in clashes:
        assert clash.payload["الطرف_الأول"] != clash.payload["الطرف_الثاني"]
        assert standing_of(clash) is LinkStanding.TWO_SIDES_NOT_LIFTED_HERE


def test_the_formal_counts_survive_an_independent_exhaustive_recount() -> None:
    for length in (1, 2, 3):
        assert surviving_chains(length) == surviving_chains_by_enumeration(length)


def test_the_partition_constraint_has_one_root_and_refuses_what_does_not_divide() -> (
    None
):
    assert extras_count_forcing(144) == 4
    assert extras_count_forcing(112) == 0
    assert extras_count_forcing(145) is None
    assert extras_count_forcing(0) is None


def test_the_fingerprints_the_ledger_claims_unique_are_measured_unique() -> None:
    assert len(set(cell_digests())) == len(cell_digests())
    assert len(set(folded_digests())) == len(folded_digests())
    assert len(folded_digests()) == surviving_chains(2)


def test_the_module_declares_what_the_chain_does_not_prove() -> None:
    for sentence in (
        THE_CHAIN_ORDERS_THE_LINKS_AND_GIT_DATES_THEM,
        PREREGISTRATION_IS_INERT_ON_WHAT_A_MACHINE_CAN_REDERIVE,
        AN_UNMEASURED_EXPECTATION_IS_NOT_A_CONFIRMED_ONE,
    ):
        assert sentence.strip()
    assert "git" in THE_CHAIN_ORDERS_THE_LINKS_AND_GIT_DATES_THEM


def test_the_reader_is_authority_inert_and_reads_no_corpus() -> None:
    text = MODULE.read_text(encoding="utf-8")
    for forbidden in ("kernel", "program", "corpora"):
        assert f"import {forbidden}" not in text
        assert f"from alghanem.{forbidden}" not in text
        assert f"from ..{forbidden}" not in text


def _chapter_fourteen() -> tuple[LedgerLink, ...]:
    return tuple(
        link
        for link in read_deposited_ledger()
        if link.stamp.startswith("2026-09-29T23")
    )


def test_the_later_segment_is_appended_and_rewrites_no_earlier_digest() -> None:
    links = read_deposited_ledger()
    later = _chapter_fourteen()
    assert later
    earlier = links[: links.index(later[0])]
    assert [link.link_digest for link in links[: len(earlier)]] == [
        link.link_digest for link in earlier
    ]
    assert later[0].previous_digest == earlier[-1].link_digest
    assert {link.stamp for link in earlier} == {"2026-09-29T22:42:23+00:00"}


def _chapter_thirty_seven() -> list[LedgerLink]:
    return [
        link for link in read_deposited_ledger() if link.stamp.startswith("2026-09-30")
    ]


def test_the_third_segment_appends_and_rewrites_no_earlier_digest() -> None:
    links = read_deposited_ledger()
    later = _chapter_thirty_seven()
    assert later
    earlier = links[: links.index(later[0])]
    assert [link.link_digest for link in links[: len(earlier)]] == [
        link.link_digest for link in earlier
    ]
    assert later[0].previous_digest == earlier[-1].link_digest
    assert {link.stamp for link in earlier} == {
        "2026-09-29T22:42:23+00:00",
        "2026-09-29T23:42:31+00:00",
    }


def test_a_measured_proxy_is_never_read_as_agreeing_with_its_named_phenomenon() -> None:
    proxies = [
        (link, standing)
        for link, standing in standings()
        if link.genus is LinkGenus.PROXY_NOT_THE_PHENOMENON
    ]
    assert proxies
    for link, standing in proxies:
        assert standing is LinkStanding.THE_MARK_IS_MEASURED_AND_THE_NAME_IS_NOT
        assert standing is not LinkStanding.REDERIVED_AND_AGREES
        assert link.payload["المقيس"] != link.payload["المنسوبُ_إليه"]


def test_the_dichotomy_of_chapter_thirty_seven_is_refuted_by_a_third_genus() -> None:
    """«إمّا بصمةٌ فتُقاس وإمّا لا بصمةَ فتُحجَز — ولا ثالث» — وههنا ثالثُها."""

    genera = {link.genus for link in _chapter_thirty_seven()}
    assert LinkGenus.PROXY_NOT_THE_PHENOMENON in genera
    assert LinkGenus.FORMAL in genera


def test_a_shadda_that_no_article_explains_is_measured_on_both_deposits() -> None:
    censuses = shadda_sources_on_our_deposits()
    assert len(censuses) == 2
    for census in censuses:
        assert census.at_least_other_than_assimilation > 0
        assert census.total > census.at_most_article_assimilation


def test_widening_the_assimilation_side_cannot_rescue_the_identification() -> None:
    """القسمةُ مُنحازةٌ ضدّ نفسها، فتدقيقُها لا يُنقِص الطرفَ الآخر."""

    for census in shadda_sources_on_our_deposits():
        assert (
            census.at_least_other_than_assimilation
            == census.total - census.at_most_article_assimilation
        )
        assert census.at_most_article_assimilation < census.total


def test_bareness_is_reported_apart_from_the_sukun_it_was_once_read_as() -> None:
    for _, bare, implied, gap in bare_positions_are_not_sukun():
        assert bare + gap == implied
        assert gap > 0


def test_the_realized_cells_are_fewer_than_the_licensed_field() -> None:
    realized, licensed = realized_against_licensed_cells()
    assert realized < licensed


def test_the_reservation_is_measured_by_absent_generators_not_asserted() -> None:
    assert set(generatorless_reserved_names()) == set(THE_RESERVED_PHONETIC_NAMES)


def test_the_claimed_starting_theorem_is_refuted_by_the_deposited_algebra() -> None:
    link = next(item for item in _chapter_fourteen() if "الشقُّ الجبريّ" in item.name)
    assert link.payload["المدَّعى_في_الفصل"] == 0
    assert standing_of(link) is LinkStanding.REDERIVED_AND_DIFFERS
    assert initial_silent_cells() > 0
    honest = replace(link, payload={**link.payload, "العدد": initial_silent_cells()})
    assert standing_of(honest) is LinkStanding.REDERIVED_AND_AGREES


def test_the_banned_start_is_a_priced_amendment_not_the_deposited_algebra() -> None:
    priced = [link for link in _chapter_fourteen() if "ثمنُ التعديل" in link.name]
    assert len(priced) == 3
    for link in priced:
        assert standing_of(link) is LinkStanding.REDERIVED_AND_AGREES
        length = int(link.payload["الطول"])
        assert link.payload["العدد"] < link.payload["المُودَعُ_بلا_القيد"]
        assert surviving_chains(length) == link.payload["المُودَعُ_بلا_القيد"]
        assert (
            surviving_chains(length, forbid_initial_silence=True)
            == (link.payload["العدد"])
        )


def test_the_entailment_is_valid_while_its_premise_stays_refuted() -> None:
    entailment = next(item for item in _chapter_fourteen() if "الاستتباع" in item.name)
    premise = next(item for item in _chapter_fourteen() if "الشقُّ الجبريّ" in item.name)
    assert standing_of(entailment) is LinkStanding.REDERIVED_AND_AGREES
    assert standing_of(premise) is LinkStanding.REDERIVED_AND_DIFFERS
    assert boundary_collisions_under_initial_ban() == 0


def test_an_unbounded_expectation_is_read_as_neither_agreement_nor_contradiction() -> (
    None
):
    unbound = [
        (link, standing)
        for link, standing in standings()
        if link.genus is LinkGenus.UNBOUND_EXPECTATION
    ]
    assert len(unbound) == 2
    for link, standing in unbound:
        assert standing is LinkStanding.NOT_FALSIFIABLE_AS_WORDED
        assert standing is not LinkStanding.REDERIVED_AND_AGREES
        assert standing is not LinkStanding.ITS_MATERIAL_HAS_NOT_ARRIVED
        assert "ما_ينقصه" in link.payload
        assert "العدد" not in link.payload


def test_the_sealed_corpus_expectations_carry_a_named_check_that_has_not_run() -> None:
    promised = [
        link
        for link in _chapter_fourteen()
        if link.genus is LinkGenus.AWAITING_ITS_MATERIAL
    ]
    assert len(promised) == 2
    for link in promised:
        assert link.payload["الفحص_الموعود"] == "CERT-W2"
        assert standing_of(link) is LinkStanding.ITS_MATERIAL_HAS_NOT_ARRIVED


def test_agreeing_with_one_horn_of_an_open_clash_is_not_recorded_as_support() -> None:
    link = next(
        item for item in _chapter_fourteen() if item.genus is LinkGenus.DECLARED_CLASH
    )
    assert link.payload["الطرف_الأول"] != link.payload["الطرف_الثاني"]
    assert standing_of(link) is LinkStanding.TWO_SIDES_NOT_LIFTED_HERE
    assert "لماذا_لا_يُعَدُّ_تعضيدًا" in link.payload


def test_the_two_new_sentences_separate_the_algebra_from_the_language() -> None:
    assert "الجبر" in A_PROOF_OVER_THE_ALGEBRA_IS_NOT_A_PROOF_OVER_THE_LANGUAGE
    assert "العربيّة" in A_PROOF_OVER_THE_ALGEBRA_IS_NOT_A_PROOF_OVER_THE_LANGUAGE
    assert AN_UNBOUNDED_EXPECTATION_CANNOT_FAIL_SO_IT_IS_NOT_ONE.strip()
