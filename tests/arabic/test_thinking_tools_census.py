"""اختباراتُ جدول منهج التفكير — كلُّ رقمٍ يُعاد من القرص لا يُصدَّق عن النثر."""

from __future__ import annotations

import pytest

from alghanem.arabic.quran_corpus_word_total import (
    WordCountingRule,
    strip_diacritics,
    word_total,
)
from alghanem.arabic.thinking_tools_census import (
    THE_NAMED_CONTAMINANTS,
    THE_REFUSED_PROBES,
    THE_TOOL_PROBES,
    THE_TRANSCRIBED_NETWORK,
    THE_TRANSCRIBED_TABLE,
    THINKING_TOOLS_NAMED_RESIDUALS,
    ClaimStanding,
    Contaminant,
    ThinkingTool,
    ThinkingToolsCensusError,
    ToolProbes,
    certainty_to_conjecture,
    every_measurement,
    measure_tool,
    network_reading,
    standing_of,
)


def _measured(tool: ThinkingTool) -> int:
    return measure_tool(tool).occurrences


def test_every_transcribed_row_has_probes_and_every_probe_set_has_a_row() -> None:
    rows = {row.tool for row in THE_TRANSCRIBED_TABLE}
    probed = {entry.tool for entry in THE_TOOL_PROBES}
    assert rows == probed
    assert len(rows) == 8


def test_the_probes_of_a_tool_are_never_nested() -> None:
    with pytest.raises(ThinkingToolsCensusError):
        ToolProbes(ThinkingTool.CERTAINTY, ("موقن", "موقنون"))


def test_a_vocalised_probe_is_refused_because_the_text_is_stripped() -> None:
    with pytest.raises(ThinkingToolsCensusError):
        ToolProbes(ThinkingTool.ANALOGY, ("مَثل",))
    for entry in THE_TOOL_PROBES:
        for probe in entry.probes:
            assert strip_diacritics(probe) == probe


def test_the_analogy_row_is_not_reproduced_and_its_coincidence_has_no_first_term() -> (
    None
):
    measurement = measure_tool(ThinkingTool.ANALOGY)
    assert (measurement.occurrences, measurement.ayahs) == (148, 130)
    assert measurement.distinct_surfaces == 27
    assert measurement.occurrences != 112
    assert measurement.ayahs != 112


def test_the_transcribed_figures_diverge_row_by_row_on_these_bytes() -> None:
    for row in THE_TRANSCRIBED_TABLE:
        assert standing_of(row) is not ClaimStanding.REPRODUCED


def test_the_certainty_direction_is_inverted_not_merely_off() -> None:
    certainty, conjecture = certainty_to_conjecture()
    assert (certainty, conjecture) == (17, 85)
    assert conjecture > certainty
    for tool in (ThinkingTool.CERTAINTY, ThinkingTool.CONJECTURE):
        row = next(item for item in THE_TRANSCRIBED_TABLE if item.tool is tool)
        assert standing_of(row) is ClaimStanding.DIRECTION_INVERTED


def test_the_remaining_measured_figures_are_what_disk_says() -> None:
    assert _measured(ThinkingTool.EXHAUSTIVE_CHALLENGE) == 12
    assert _measured(ThinkingTool.SENSORY_INFERENCE) == 47
    assert _measured(ThinkingTool.SENSORY_IMAGERY) == 40
    assert _measured(ThinkingTool.RECKONING) == 45
    assert _measured(ThinkingTool.EXHAUSTIVE_PRECISION) == 17
    assert measure_tool(ThinkingTool.SENSORY_IMAGERY).ayahs == 37


def test_the_network_row_has_a_figure_these_bytes_cannot_reach() -> None:
    reading = network_reading()
    assert reading.suras is None
    assert reading.standing is ClaimStanding.NOT_IN_THESE_BYTES
    assert reading.ayah_lines == THE_TRANSCRIBED_NETWORK[1] == 6_236
    assert reading.whitespace_tokens == 82_532 != THE_TRANSCRIBED_NETWORK[2]


def test_the_field_separator_rule_reads_nothing_on_this_deposit() -> None:
    assert word_total(WordCountingRule.WHITESPACE_TOKENS_IN_AYAH_TEXT) == 0
    assert network_reading().whitespace_tokens > 0


def test_the_named_contamination_makes_each_figure_an_upper_bound() -> None:
    certainty = measure_tool(ThinkingTool.CERTAINTY)
    assert certainty.named_contamination == 4
    assert certainty.floor_after_named_contamination == 13
    conjecture = measure_tool(ThinkingTool.CONJECTURE)
    assert conjecture.named_contamination == 2
    assert conjecture.floor_after_named_contamination == 83


def test_every_named_contaminant_really_occurs_that_many_times() -> None:
    from alghanem.arabic.quran_corpus_word_total import read_quran_corpus_bytes

    text = read_quran_corpus_bytes().decode("utf-8")
    tokens = [
        token
        for line in text.split("\n")
        if line.strip()
        for token in strip_diacritics(line.strip()).split()
    ]
    for item in THE_NAMED_CONTAMINANTS:
        assert tokens.count(item.surface) == item.occurrences


def test_a_refused_probe_is_published_with_its_measured_reason() -> None:
    refused = {probe for probe, _, _ in THE_REFUSED_PROBES}
    assert "شك" in refused
    for entry in THE_TOOL_PROBES:
        assert refused.isdisjoint(entry.probes)


def test_the_refused_shakk_probe_would_have_been_mostly_contamination() -> None:
    from alghanem.arabic.quran_corpus_word_total import read_quran_corpus_bytes

    text = read_quran_corpus_bytes().decode("utf-8")
    bare = [strip_diacritics(line.strip()) for line in text.split("\n") if line.strip()]
    occurrences = sum(line.count("شك") for line in bare)
    exact = sum(line.split().count("شك") for line in bare)
    assert (occurrences, exact) == (80, 15)


def test_no_contaminant_is_declared_for_a_tool_that_cannot_hold_it() -> None:
    with pytest.raises(ThinkingToolsCensusError):
        Contaminant(ThinkingTool.ANALOGY, "مثل", 0, "وقوعٌ دون الواحد")


def test_every_measurement_covers_the_eight_probed_tools() -> None:
    measurements = every_measurement()
    assert len(measurements) == 8
    assert {item.tool for item in measurements} == {
        entry.tool for entry in THE_TOOL_PROBES
    }


def test_the_residuals_name_what_was_not_settled() -> None:
    assert "عددُ السور" in THINKING_TOOLS_NAMED_RESIDUALS
    assert all(value.strip() for value in THINKING_TOOLS_NAMED_RESIDUALS.values())
