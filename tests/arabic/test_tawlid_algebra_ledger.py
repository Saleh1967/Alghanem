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
    AN_UNMEASURED_EXPECTATION_IS_NOT_A_CONFIRMED_ONE,
    PREREGISTRATION_IS_INERT_ON_WHAT_A_MACHINE_CAN_REDERIVE,
    ROOT_DIGEST,
    THE_CHAIN_ORDERS_THE_LINKS_AND_GIT_DATES_THEM,
    LedgerLink,
    LinkGenus,
    LinkStanding,
    cell_digests,
    chain_is_unbroken,
    extras_count_forcing,
    folded_digests,
    ledger_path,
    read_deposited_ledger,
    recomputed_link_digests,
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


def test_every_formal_link_flips_on_its_own_when_its_figure_is_moved() -> None:
    formal = [
        item for item in read_deposited_ledger() if item.genus is LinkGenus.FORMAL
    ]
    assert len(formal) >= 7
    for link in formal:
        assert standing_of(link) is LinkStanding.REDERIVED_AND_AGREES
        moved = replace(link, payload={**link.payload, **_moved_figure(link)})
        assert standing_of(moved) is LinkStanding.REDERIVED_AND_DIFFERS


def _moved_figure(link: LedgerLink) -> dict[str, int]:
    for key in ("العدد", "البصمات_الفريدة", "الجذر_الوحيد"):
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
    assert len(clashes) == 1
    payload = clashes[0].payload
    assert payload["الطرف_الأول"] != payload["الطرف_الثاني"]
    assert standing_of(clashes[0]) is LinkStanding.TWO_SIDES_NOT_LIFTED_HERE


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
