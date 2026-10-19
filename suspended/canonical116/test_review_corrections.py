"""اختباراتُ القناة الخامسة: تصحيحاتُ التقييم، كلٌّ بقياسه."""

from __future__ import annotations

import unittest

from .review_corrections import (
    THE_DESCRIPTIVE_PAIR,
    THE_PREDICATIVE_PAIR,
    corrected_claims,
    digest_chain_reading,
    false_admission_reading,
    greedy_partition_of,
    independence_reading,
    occurrence_ledger,
    role_residue_classes,
    rows,
    separating_field_readings,
    the_bridge_emits_no_syllable_partition,
)


class SquareIndependenceTest(unittest.TestCase):
    def test_the_bridge_report_carries_no_syllable_partition_to_compare_with(
        self,
    ) -> None:
        keys = the_bridge_emits_no_syllable_partition()
        for key in keys:
            self.assertNotIn("syllable", key.lower())
            self.assertNotIn("partition", key.lower())

    def test_the_exhaustive_parser_never_branches_on_this_deposit(self) -> None:
        reading = independence_reading()
        self.assertEqual(reading.exhaustive_branched, 0)
        self.assertTrue(reading.the_exhaustion_is_inert)

    def test_the_greedy_strategy_agrees_everywhere_and_refuses_the_same(
        self,
    ) -> None:
        reading = independence_reading()
        self.assertEqual(reading.forms, 9380)
        self.assertEqual(reading.exhaustive_unique, 8510)
        self.assertEqual(reading.greedy_agrees, 8510)
        self.assertEqual(reading.greedy_disagrees, 0)
        self.assertEqual(reading.greedy_refuses, reading.exhaustive_refused)
        self.assertEqual(reading.greedy_refuses, 870)
        self.assertTrue(reading.the_two_strategies_never_disagree)

    def test_the_two_arms_sum_to_every_ready_form(self) -> None:
        reading = independence_reading()
        self.assertEqual(
            reading.exhaustive_unique
            + reading.exhaustive_branched
            + reading.exhaustive_refused,
            reading.forms,
        )

    def test_the_greedy_parser_refuses_a_form_that_opens_with_a_sukun(
        self,
    ) -> None:
        self.assertIsNone(greedy_partition_of(("سْ", "مِ")))
        self.assertIsNotNone(greedy_partition_of(("بِ", "سْ", "مِ")))


class SeparatingFieldTest(unittest.TestCase):
    def test_the_base_field_separates_every_colliding_fiber(self) -> None:
        base = {item.field: item for item in separating_field_readings()}["base"]
        self.assertEqual(base.of_total, 18)
        self.assertEqual(base.separated, 18)
        self.assertTrue(base.separates_them_all)
        self.assertEqual(base.residue, ())

    def test_the_cluster_roles_separate_eleven_and_not_none(self) -> None:
        role = {item.field: item for item in separating_field_readings()}["role"]
        self.assertEqual(role.separated, 11)
        self.assertFalse(role.separates_them_all)
        self.assertEqual(len(role.residue), 7)

    def test_the_vowel_reading_separates_not_one_of_them(self) -> None:
        reading = {item.field: item for item in separating_field_readings()}["reading"]
        self.assertEqual(reading.separated, 0)
        self.assertEqual(len(reading.residue), 18)

    def test_the_study_refutation_witness_is_lifted_by_the_cluster_roles(
        self,
    ) -> None:
        """«نِعْمَةَ»/«نِعْمَتَ» ليس في بقيّة الأدوار؛ فالأدوارُ تفصله."""

        role = {item.field: item for item in separating_field_readings()}["role"]
        flattened = {form for pair in role.residue for form in pair}
        self.assertNotIn("نِعْمَةَ", flattened)
        self.assertNotIn("نِعْمَتَ", flattened)

    def test_the_role_residue_is_two_named_classes_not_one_figure(self) -> None:
        classes = role_residue_classes()
        self.assertEqual(
            [name for name, _ in classes], ["مقعدُ الهمزة", "الألفُ المقصورة"]
        )
        self.assertEqual([len(pairs) for _, pairs in classes], [2, 5])
        self.assertEqual(sum(len(pairs) for _, pairs in classes), 7)


class DigestChainTest(unittest.TestCase):
    def test_three_of_the_eight_links_are_broken(self) -> None:
        chain = digest_chain_reading()
        assert chain is not None
        self.assertEqual(chain.stages, 9)
        self.assertEqual(chain.links, 8)
        self.assertEqual(chain.chained, 5)
        self.assertFalse(chain.the_chain_is_unbroken)

    def test_the_broken_links_are_named_and_never_counted_only(self) -> None:
        chain = digest_chain_reading()
        assert chain is not None
        self.assertEqual(chain.broken, ("SYLLABLE", "WORD_STRUCTURE", "CASE_MARK"))
        self.assertEqual(len(chain.broken) + chain.chained, chain.links)


class FalseAdmissionTest(unittest.TestCase):
    def test_a_descriptive_pair_is_admitted_as_predication_and_as_beneficial(
        self,
    ) -> None:
        reading = dict(
            (text, (composition, ifada))
            for text, composition, ifada, _ in false_admission_reading()
        )
        self.assertEqual(reading[THE_DESCRIPTIVE_PAIR], ("إسناد", "مُفيد"))

    def test_the_two_pairs_are_read_identically_though_they_differ(
        self,
    ) -> None:
        rows_ = {
            text: (composition, ifada)
            for text, composition, ifada, _ in false_admission_reading()
        }
        self.assertEqual(rows_[THE_PREDICATIVE_PAIR], rows_[THE_DESCRIPTIVE_PAIR])

    def test_the_witness_names_only_the_two_written_marks(self) -> None:
        witnesses = {text: witness for text, _, _, witness in false_admission_reading()}
        self.assertIn("ضمّة", witnesses[THE_DESCRIPTIVE_PAIR])
        self.assertNotIn("نعت", witnesses[THE_DESCRIPTIVE_PAIR])


class OccurrenceLedgerTest(unittest.TestCase):
    def test_every_occurrence_is_assigned_exactly_once(self) -> None:
        ledger = occurrence_ledger()
        self.assertEqual(ledger.occurrences, 78245)
        self.assertEqual(ledger.assigned_once, 78245)
        self.assertEqual(ledger.assigned_twice_or_more, 0)
        self.assertEqual(ledger.assigned_never, 0)
        self.assertTrue(ledger.is_a_partition)

    def test_the_partition_is_proved_by_the_ledger_and_not_by_the_sum(
        self,
    ) -> None:
        ledger = occurrence_ledger()
        self.assertEqual(ledger.assignments, ledger.occurrences)


class CorrectedClaimTest(unittest.TestCase):
    def test_two_of_my_claims_are_withdrawn_and_three_are_bounded(self) -> None:
        claims = corrected_claims()
        self.assertEqual(len(claims), 5)
        withdrawn = [claim for claim in claims if claim.is_withdrawn]
        self.assertEqual(len(withdrawn), 2)

    def test_every_correction_names_its_place_and_its_measurement(self) -> None:
        for claim in corrected_claims():
            self.assertIn(".py", claim.where)
            self.assertTrue(claim.measured.strip())
            self.assertNotEqual(claim.measured.strip(), "—")

    def test_the_printed_report_carries_every_section(self) -> None:
        text = "\n".join(rows())
        self.assertIn("Saleh1967", text)
        self.assertIn("base: 18/18", text)
        self.assertIn("CASE_MARK", text)
        self.assertIn("ما صُحِّح من قولي", text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
