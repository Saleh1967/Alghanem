"""اختباراتُ القناة الثالثة: قانونُ الولادة إلى الإفادة، مقيسًا لا منقولًا."""

from __future__ import annotations

import unittest

from .birth_law_test import (
    THE_NAMED_MATERIALS,
    THE_QUOTED_UPPER_FIGURES,
    THE_RUN_INPUTS,
    GateStanding,
    absence_reading,
    bism_reading,
    handoff_reading,
    ifada_gate_readings,
    rows,
    tokenisation_policies,
    unit_axis_reading,
    verdict_table,
)
from .owner_experiment import Provenance


class NamedMaterialsTest(unittest.TestCase):
    def test_every_named_material_is_measured_absent_by_opening_its_path(
        self,
    ) -> None:
        reading = absence_reading()
        self.assertEqual(len(reading), len(THE_NAMED_MATERIALS))
        for name, present in reading:
            self.assertFalse(present, f"{name} وُجِد في الشجرة خلافًا للمقيس")

    def test_no_upper_figure_is_ever_promoted_to_measured(self) -> None:
        for figure in THE_QUOTED_UPPER_FIGURES:
            self.assertIs(
                figure.provenance,
                Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
                figure.name,
            )


class UnitAxisTest(unittest.TestCase):
    def test_the_unit_count_agrees_exactly_and_is_not_rounded(self) -> None:
        lines = unit_axis_reading()[0]
        self.assertIs(lines.provenance, Provenance.MEASURED_HERE)
        self.assertEqual(lines.value, 6236)

    def test_the_word_axis_leaves_a_residue_of_eight_hundred_and_sixteen(
        self,
    ) -> None:
        occurrences, residue = unit_axis_reading()[1], unit_axis_reading()[2]
        self.assertEqual(occurrences.value, 78245)
        self.assertEqual(residue.value, 816)
        self.assertEqual(occurrences.value - residue.value, 77429)

    def test_no_tried_tokenisation_policy_reproduces_the_incoming_word_count(
        self,
    ) -> None:
        policies = tokenisation_policies()
        self.assertGreaterEqual(len(policies), 7)
        self.assertNotIn(77429, [value for _, value in policies])

    def test_the_nearest_policy_is_still_short_of_the_incoming_figure(
        self,
    ) -> None:
        nearest = unit_axis_reading()[3]
        self.assertEqual(nearest.value, 77305)
        self.assertLess(nearest.value, 77429)

    def test_agreeing_units_with_a_differing_word_count_is_one_source_not_two(
        self,
    ) -> None:
        """اتّفاقُ 6,236 يمنع صرفَ البقيّة بدعوى أنّ المصدرَ آخَر."""

        claim, measured, _ = verdict_table()[1]
        self.assertIn("6,236", measured)
        self.assertIn("816", measured)
        self.assertIn("78,245", claim)


class BismTest(unittest.TestCase):
    def test_the_handoff_word_reaches_a_ready_carrier_in_this_bridge(
        self,
    ) -> None:
        reading = bism_reading()
        self.assertEqual(reading["status"], "READY")
        self.assertEqual(reading["atoms"], ("بِ", "سْ", "مِ"))
        self.assertEqual(reading["rejections"], ())

    def test_the_source_digest_is_derived_and_never_copied(self) -> None:
        import hashlib

        self.assertEqual(
            bism_reading()["source_sha256"],
            hashlib.sha256("بِسْمِ".encode()).hexdigest(),
        )


class HandoffTest(unittest.TestCase):
    def test_neither_side_of_this_tree_accepts_a_certificate_either(
        self,
    ) -> None:
        for label, standing, _ in handoff_reading():
            self.assertIs(standing, GateStanding.NOT_WRITTEN, label)

    def test_a_missing_interface_is_recorded_as_a_debt_not_as_a_failure(
        self,
    ) -> None:
        _, _, verdict = verdict_table()[3]
        self.assertIn("دَينٌ مسمًّى", verdict)
        self.assertNotIn("فشلٌ مقيس", verdict.replace("لا فشلٌ مقيس", ""))


class IfadaGateTest(unittest.TestCase):
    def test_the_vertical_path_closes_a_record_inside_its_declared_scope(
        self,
    ) -> None:
        runs = ifada_gate_readings()
        self.assertEqual(len(runs), len(THE_RUN_INPUTS))
        closed = [r for r in runs if r.standing is GateStanding.CLOSED_IN_SCOPE]
        self.assertEqual(len(closed), 2)
        self.assertEqual([r.ifada for r in closed], ["مُفيد", "غير_مُفيد"])

    def test_a_closed_record_carries_the_two_written_marks_as_its_witness(
        self,
    ) -> None:
        beneficial = ifada_gate_readings()[0]
        self.assertEqual(beneficial.text, "اللَّهُ نُورٌ")
        self.assertIsNotNone(beneficial.witness)
        assert beneficial.witness is not None
        self.assertIn("ضمّة", beneficial.witness)

    def test_outside_the_scope_the_path_stops_with_a_named_genus_not_a_false(
        self,
    ) -> None:
        stopped = [
            run
            for run in ifada_gate_readings()
            if run.standing is GateStanding.STOPPED_WITH_A_NAMED_GENUS
        ]
        self.assertEqual(len(stopped), 2)
        self.assertEqual([run.last_outcome for run in stopped], ["DEFERRED", "BLOCKED"])
        for run in stopped:
            self.assertIsNone(run.ifada)
            self.assertTrue(run.witness)

    def test_deferral_and_blocking_are_two_genera_and_never_one(self) -> None:
        outcomes = {run.last_outcome for run in ifada_gate_readings()}
        self.assertEqual(outcomes, {"ADVANCED", "DEFERRED", "BLOCKED"})

    def test_an_existing_scoped_gate_refutes_the_claim_that_none_exists(
        self,
    ) -> None:
        _, _, verdict = verdict_table()[4]
        self.assertIn("محدودةُ النطاق لا غائبة", verdict)


class VerdictTest(unittest.TestCase):
    def test_the_generating_law_claim_stays_unproven(self) -> None:
        claim, _, verdict = verdict_table()[5]
        self.assertIn("116", claim)
        self.assertIn("غيرُ مُثبَت", verdict)

    def test_every_verdict_row_carries_a_claim_a_measurement_and_a_ruling(
        self,
    ) -> None:
        table = verdict_table()
        self.assertEqual(len(table), 6)
        for row in table:
            self.assertEqual(len(row), 3)
            for cell in row:
                self.assertTrue(cell.strip())

    def test_the_printed_report_names_the_owner_and_prints_every_section(
        self,
    ) -> None:
        text = "\n".join(rows())
        self.assertIn("Saleh1967", text)
        self.assertIn("GFLK_Mushajjir_Independent_v1.zip", text)
        self.assertIn("جدولُ الأحكام", text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
