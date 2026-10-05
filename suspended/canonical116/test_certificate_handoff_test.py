"""اختباراتُ القناة الرابعة: حلُّ انقطاع الشهادة، مقيسًا لا منقولًا."""

from __future__ import annotations

import unittest

from .certificate_handoff_test import (
    THE_INCOMING_PARTITION,
    THE_PACKAGE_MATERIALS,
    THE_WITNESS_PAIR,
    deferral_census,
    identity_key_readings,
    incoming_sum_reading,
    material_readings,
    partition_reading,
    rows,
    verdict_table,
    witness_pair_reading,
)
from .owner_experiment import Provenance


class MaterialTest(unittest.TestCase):
    def test_four_materials_are_absent_and_one_only_matches_by_name(
        self,
    ) -> None:
        readings = material_readings()
        self.assertEqual(len(readings), len(THE_PACKAGE_MATERIALS))
        absent = [item for item in readings if not item.name_matches]
        matched = [item for item in readings if item.name_matches]
        self.assertEqual(len(absent), 4)
        self.assertEqual([item.name for item in matched], ["manifest.json"])

    def test_a_name_match_is_never_read_as_the_named_material(self) -> None:
        for item in material_readings():
            self.assertFalse(item.is_the_named_material, item.name)

    def test_the_name_match_is_named_by_its_own_place_in_the_tree(self) -> None:
        matched = [item for item in material_readings() if item.name_matches][0]
        self.assertEqual(
            matched.name_matches,
            ("src/alghanem/realization/generated/manifest.json",),
        )


class IncomingPartitionTest(unittest.TestCase):
    def test_no_incoming_figure_is_ever_promoted_to_measured(self) -> None:
        for figure in THE_INCOMING_PARTITION:
            self.assertIs(
                figure.provenance,
                Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
                figure.name,
            )

    def test_the_three_classes_exhaust_the_deposit_exactly(self) -> None:
        total, measured, agrees = incoming_sum_reading()
        self.assertEqual(total, 78245)
        self.assertEqual(measured, 78245)
        self.assertTrue(agrees)

    def test_an_exhaustive_sum_is_not_read_as_agreement_on_the_cut(
        self,
    ) -> None:
        _, _, verdict = verdict_table()[1]
        self.assertIn("اتّساقٌ داخليٌّ", verdict)
        self.assertIn("ليس اتّفاقًا", verdict)


class BridgePartitionTest(unittest.TestCase):
    def test_the_form_and_occurrence_totals_are_reproduced_exactly(
        self,
    ) -> None:
        forms, occurrences = partition_reading()[0], partition_reading()[1]
        self.assertIs(forms.provenance, Provenance.MEASURED_HERE)
        self.assertEqual(forms.value, 18200)
        self.assertEqual(occurrences.value, 78245)

    def test_this_bridge_has_two_classes_and_never_three(self) -> None:
        self.assertEqual(partition_reading()[2].value, 2)

    def test_the_cut_line_moves_by_five_hundred_and_twenty_five(self) -> None:
        reading = partition_reading()
        ready, defer, shift = reading[3], reading[4], reading[5]
        self.assertEqual(ready.value, 41820)
        self.assertEqual(defer.value, 36425)
        self.assertEqual(ready.value + defer.value, 78245)
        self.assertEqual(shift.value, 525)
        self.assertEqual(36950 - defer.value, 525)

    def test_the_deferred_side_is_a_total_partition_of_three_named_classes(
        self,
    ) -> None:
        census = deferral_census()
        self.assertEqual(len(census), 3)
        self.assertEqual(sum(forms for _, forms, _ in census), 8820)
        self.assertEqual(sum(occ for _, _, occ in census), 36425)

    def test_no_deferred_class_here_is_the_incoming_middle_figure(self) -> None:
        for name, forms, occurrences in deferral_census():
            self.assertNotEqual(occurrences, 848, name)
            self.assertNotEqual(forms, 848, name)


class IdentityKeyTest(unittest.TestCase):
    def test_the_canonical_text_collides_exactly_where_the_atoms_do(
        self,
    ) -> None:
        keys = {key.name: key for key in identity_key_readings()}
        atoms, text = keys["canonical_atoms"], keys["canonical_text"]
        self.assertEqual(atoms.colliding_classes, 18)
        self.assertEqual(atoms.colliding_forms, 36)
        self.assertEqual(text.colliding_classes, atoms.colliding_classes)
        self.assertEqual(text.colliding_forms, atoms.colliding_forms)

    def test_only_the_source_digest_lifts_the_rasm(self) -> None:
        keys = {key.name: key for key in identity_key_readings()}
        self.assertFalse(keys["canonical_atoms"].lifts_the_rasm)
        self.assertFalse(keys["canonical_text"].lifts_the_rasm)
        self.assertTrue(keys["source_sha256"].lifts_the_rasm)
        self.assertEqual(keys["source_sha256"].colliding_forms, 0)

    def test_the_witness_pair_agrees_in_atoms_and_in_canonical_text_too(
        self,
    ) -> None:
        pair = witness_pair_reading()
        self.assertEqual(len(pair), 2)
        self.assertEqual({row[0] for row in pair}, set(THE_WITNESS_PAIR))
        self.assertEqual(len({row[1] for row in pair}), 1)
        self.assertEqual(len({row[2] for row in pair}), 1)
        self.assertEqual(len({row[3] for row in pair}), 2)

    def test_pinning_the_canonical_text_would_not_block_the_swap(self) -> None:
        """تثبيتُ النصّ المعياريّ يقبل «أَبَى» تحت هويّة «أَبَا» ولا يردّه."""

        first, second = witness_pair_reading()
        self.assertEqual(first[2], second[2])
        self.assertNotEqual(first[3], second[3])


class VerdictTest(unittest.TestCase):
    def test_the_rasm_claim_holds_only_under_the_source_bytes(self) -> None:
        _, measured, verdict = verdict_table()[4]
        self.assertIn("البصمةُ 0", measured)
        self.assertIn("لا يصحّ إلّا بالبايتات", verdict)

    def test_the_zero_licensed_upper_rules_are_carried_not_scored(self) -> None:
        _, _, verdict = verdict_table()[5]
        self.assertIn("لا يُقاس ههنا", verdict)

    def test_every_verdict_row_carries_a_claim_a_measurement_and_a_ruling(
        self,
    ) -> None:
        table = verdict_table()
        self.assertEqual(len(table), 6)
        for row in table:
            self.assertEqual(len(row), 3)
            for cell in row:
                self.assertTrue(cell.strip())

    def test_the_printed_report_names_the_owner_and_every_section(self) -> None:
        text = "\n".join(rows())
        self.assertIn("Saleh1967", text)
        self.assertIn("licensed_dal.py", text)
        self.assertIn("مفاتيحُ الهويّة", text)
        self.assertIn("جدولُ الأحكام", text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
