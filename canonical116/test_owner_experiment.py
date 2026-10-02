"""اختباراتُ القناة التجريبيّة المؤقّتة؛ تُشغَّل بـ`unittest` لا بـ`pytest`.

    python -m unittest canonical116.test_owner_experiment

واختبارُ التصنيف يُشغِّل الجسرَ على كلِّ شكلٍ مختلفٍ في المُودَع، فيطول؛ وهو
مكتوبٌ ليُشغَّل لا ليُتجاوَز، لأنّ الفرقَ الذي يُخرِجه هو موضعُ الفائدة.
"""

from __future__ import annotations

import unittest

from . import owner_experiment as experiment


class TestTheSignatureIsAnAuthorisationNotASeal(unittest.TestCase):
    def test_the_signature_never_reads_as_a_seal(self) -> None:
        self.assertFalse(experiment.OWNER_SIGNATURE.is_a_seal)

    def test_what_the_signature_refuses_is_written_and_not_left_to_inference(
        self,
    ) -> None:
        refused = experiment.OWNER_SIGNATURE.does_not_authorise
        self.assertTrue(refused)
        self.assertTrue(any("حارس" in line for line in refused))
        self.assertTrue(any("اصطناع" in line for line in refused))

    def test_the_channel_is_revocable_by_deletion(self) -> None:
        self.assertIn("حذف", experiment.OWNER_SIGNATURE.revocation)


class TestTheInventoryIsMeasuredNotTranscribed(unittest.TestCase):
    def test_the_twenty_nine_and_the_four_make_one_hundred_and_sixteen(self) -> None:
        figures = {figure.name: figure for figure in experiment.inventory_reading()}
        self.assertEqual(figures["الحوامل"].value, 29)
        self.assertEqual(figures["الحالات"].value, 4)
        self.assertEqual(figures["الخانات"].value, 116)
        self.assertEqual(figures["فضاءُ الإمكان الخام A×B"].value, 3364)

    def test_every_inventory_figure_is_measured_here(self) -> None:
        for figure in experiment.inventory_reading():
            self.assertIs(figure.provenance, experiment.Provenance.MEASURED_HERE)

    def test_the_numbering_round_trip_is_total(self) -> None:
        self.assertTrue(experiment.numbering_round_trip_is_total())


class TestTheLedgerIsReproducedFromTheDeposit(unittest.TestCase):
    def test_the_quoted_ledger_is_reproduced_exactly(self) -> None:
        reading = experiment.ledger_reading()
        self.assertTrue(reading.reproduces_the_quoted_ledger)
        self.assertEqual(reading.measured[0].value, 78245)
        self.assertEqual(reading.measured[1].value, 18200)

    def test_the_editorial_markers_are_counted_and_not_silently_dropped(self) -> None:
        self.assertEqual(experiment.ledger_reading().editorial_markers_dropped, 4287)

    def test_the_seal_is_derived_from_the_disk(self) -> None:
        reading = experiment.ledger_reading()
        _, seal = experiment.read_deposit()
        self.assertEqual(reading.deposit_sha256, seal)


class TestTheWitnessesAreAtTheirStatedPositions(unittest.TestCase):
    def test_both_witnesses_sit_where_the_study_said_they_sit(self) -> None:
        readings = {reading.form: reading for reading in experiment.witness_readings()}
        self.assertEqual(
            (readings["نِعْمَةَ"].line_number, readings["نِعْمَةَ"].word_number),
            (218, 11),
        )
        self.assertEqual(
            (readings["نِعْمَتَ"].line_number, readings["نِعْمَتَ"].word_number),
            (238, 27),
        )

    def test_the_collision_holds_in_wasl_and_is_lifted_in_waqf(self) -> None:
        by_exit = dict(experiment.collision_by_exit(experiment.witness_readings()))
        self.assertTrue(by_exit["continue"])
        self.assertFalse(by_exit["pause"])

    def test_the_two_forms_separate_in_waqf_by_their_final_atom(self) -> None:
        readings = {
            reading.form: dict(reading.atoms_by_exit)
            for reading in experiment.witness_readings()
        }
        self.assertEqual(readings["نِعْمَةَ"]["pause"][-1], "هْ")
        self.assertEqual(readings["نِعْمَتَ"]["pause"][-1], "تْ")


class TestTheClassificationIsNotReproduced(unittest.TestCase):
    def test_the_gap_from_the_quoted_classification_is_named_not_rounded(self) -> None:
        reading = experiment.classification_reading()
        self.assertFalse(reading.reproduces_the_quoted_classification)
        self.assertEqual(reading.gap_from_the_quoted, (211, 1373))

    def test_the_two_classes_exhaust_the_reproduced_ledger(self) -> None:
        reading = experiment.classification_reading()
        self.assertEqual(reading.ready_forms + reading.withheld_forms, 18200)
        self.assertEqual(
            reading.ready_occurrences + reading.withheld_occurrences, 78245
        )


class TestTheClosedChannelsNameTheirKeys(unittest.TestCase):
    def test_every_closed_channel_names_its_missing_material_and_its_key(self) -> None:
        channels = experiment.closed_channels()
        self.assertTrue(channels)
        for channel in channels:
            self.assertTrue(channel.missing_material.strip())
            self.assertTrue(channel.what_opens_it.strip())

    def test_the_absent_study_package_is_one_of_them(self) -> None:
        materials = " ".join(
            channel.missing_material for channel in experiment.closed_channels()
        )
        self.assertIn("Scientific_116_Evidence_Study.zip", materials)


if __name__ == "__main__":
    unittest.main()
