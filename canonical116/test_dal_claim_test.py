"""اختباراتُ القناة الثانية؛ تُشغَّل بـ`unittest` لا بـ`pytest`.

    python -m unittest canonical116.test_dal_claim_test

تُقاس المادّةُ مرّةً واحدةً في `setUpClass` لأنّ تشغيل الجسر على كلِّ شكلٍ
مختلفٍ في المُودَع ليس رخيصًا؛ ولا يُتجاوَز اختبارٌ لأجل ذلك.
"""

from __future__ import annotations

import unittest

from . import dal_claim_test as claim


class TestTheChannelCarriesTheSameSignature(unittest.TestCase):
    def test_the_signature_is_an_authorisation_and_not_a_seal(self) -> None:
        self.assertFalse(claim.OWNER_SIGNATURE.is_a_seal)

    def test_the_declared_policy_is_fixed_before_measurement(self) -> None:
        self.assertEqual(
            claim.THE_DECLARED_POLICY, {"entry": "start", "exit": "continue"}
        )


class TestTheMeasuredClaims(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.forms = claim.ready_forms()
        cls.fibers = claim.fiber_reading(cls.forms)
        cls.partitions = claim.partition_reading(cls.forms)
        cls.square = claim.square_reading(cls.forms)

    # ---- الألياف -------------------------------------------------------

    def test_the_eighteen_collided_fibers_hold_thirty_six_forms(self) -> None:
        self.assertEqual(len(self.fibers.collided_fibers), 18)
        self.assertEqual(self.fibers.forms_inside_collisions, 36)

    def test_the_projection_is_not_injective_so_no_retraction_exists(self) -> None:
        self.assertFalse(self.fibers.projection_is_injective)
        self.assertTrue(self.fibers.no_retraction_recovers_the_rasm)

    def test_the_named_witnesses_sit_inside_the_collided_fibers(self) -> None:
        members = {form for _, forms in self.fibers.collided_fibers for form in forms}
        for witness in ("نِعْمَةَ", "نِعْمَتَ", "أَإِذَا", "أَئِذَا", "أَبَا", "أَبَى"):
            self.assertIn(witness, members)

    def test_every_collided_fiber_holds_exactly_two_forms_here(self) -> None:
        for _, forms in self.fibers.collided_fibers:
            self.assertEqual(len(forms), 2)

    # ---- التقسيم -------------------------------------------------------

    def test_no_form_admits_more_than_one_partition(self) -> None:
        self.assertEqual(self.partitions.more_than_one, 0)
        self.assertTrue(self.partitions.the_partition_is_unique_wherever_it_exists)

    def test_the_fold_and_unfold_lose_no_atom(self) -> None:
        self.assertEqual(self.partitions.fold_unfold_losses, 0)

    def test_the_residue_is_two_named_classes_and_the_second_matches_the_study(
        self,
    ) -> None:
        self.assertEqual(self.partitions.starts_with_a_sakin, 485)
        self.assertEqual(self.partitions.other_without_a_partition, 385)
        self.assertEqual(self.partitions.without_a_partition, 870)

    def test_the_three_classes_exhaust_the_ready_forms(self) -> None:
        self.assertEqual(
            self.partitions.exactly_one
            + self.partitions.without_a_partition
            + self.partitions.more_than_one,
            self.fibers.forms,
        )

    # ---- المربّع --------------------------------------------------------

    def test_theta_is_a_bijection_onto_the_fiber_product(self) -> None:
        self.assertTrue(self.square.theta_is_a_bijection)
        self.assertEqual(self.square.certificates, self.square.fiber_product_pairs)
        self.assertEqual(self.square.pairs_without_a_certificate, 0)
        self.assertEqual(self.square.pairs_with_two_certificates, 0)

    def test_the_maps_commute_so_unfolding_returns_the_atoms(self) -> None:
        self.assertTrue(self.square.maps_commute)

    def test_the_reference_set_matches_the_atom_sequences_one_to_one(self) -> None:
        self.assertEqual(self.square.x, self.square.s)

    def test_the_square_succeeds_while_eighteen_fibers_still_collide(self) -> None:
        self.assertEqual(self.square.collided_fibers_inside_w, 18)
        self.assertTrue(self.square.the_square_succeeds_while_the_projection_collides)

    def test_the_gap_between_w_and_x_is_exactly_the_collision_count(self) -> None:
        self.assertEqual(self.square.w - self.square.x, 18)

    # ---- الأدوار -------------------------------------------------------

    def test_the_roles_cannot_separate_a_fiber_because_they_derive_from_the_atoms(
        self,
    ) -> None:
        self.assertTrue(claim.the_roles_are_a_function_of_the_atoms(self.forms))


class TestTheExhaustiveParserIsExhaustive(unittest.TestCase):
    def test_a_sakin_can_never_open_a_syllable(self) -> None:
        self.assertEqual(claim.every_partition_of(("بْ", "تَ")), ())

    def test_a_madd_tail_is_read_cvv_and_a_consonant_tail_cvc(self) -> None:
        madd = claim.every_partition_of(("بَ", "اْ"))
        self.assertEqual(len(madd), 1)
        self.assertEqual(madd[0][0][0], claim.Syllable.CVV)
        consonant = claim.every_partition_of(("بَ", "تْ"))
        self.assertEqual(len(consonant), 1)
        self.assertEqual(consonant[0][0][0], claim.Syllable.CVC)

    def test_an_open_chain_is_a_run_of_cv(self) -> None:
        found = claim.every_partition_of(("بَ", "تِ", "كُ"))
        self.assertEqual(len(found), 1)
        self.assertEqual(
            tuple(kind for kind, _ in found[0]),
            (claim.Syllable.CV, claim.Syllable.CV, claim.Syllable.CV),
        )

    def test_both_branches_are_opened_so_uniqueness_is_forced_not_chosen(self) -> None:
        atoms = ("بَ", "تْ", "كَ")
        self.assertEqual(len(claim.every_partition_of(atoms)), 1)
        self.assertEqual(claim.unfold(claim.every_partition_of(atoms)[0]), atoms)


class TestTheHausdorffRefusal(unittest.TestCase):
    def test_every_level_of_the_alphabet_is_finite(self) -> None:
        reading = claim.hausdorff_reading()
        self.assertEqual(reading.alphabet_size, 116)
        self.assertTrue(reading.every_level_is_finite)
        self.assertEqual(reading.finite_level_sizes[1], 116)
        self.assertEqual(reading.finite_level_sizes[2], 116**2)

    def test_the_covering_sum_stays_under_epsilon_for_a_positive_exponent(self) -> None:
        reading = claim.hausdorff_reading()
        self.assertTrue(reading.the_covering_sum_is_under_epsilon)
        self.assertTrue(reading.a_positive_dimension_is_refused)

    def test_the_refusal_holds_for_several_exponents(self) -> None:
        for exponent in (0.25, 0.5, 1.0, 2.0):
            reading = claim.hausdorff_reading(exponent=exponent)
            self.assertTrue(
                reading.a_positive_dimension_is_refused,
                msg=f"s={exponent}",
            )

    def test_the_witness_is_named_an_illustration_not_a_proof(self) -> None:
        self.assertIn(
            "لا تشغيل",
            claim.A_FINITE_COVERING_WITNESS_ILLUSTRATES_THE_THEOREM_AND_DOES_NOT_PROVE_IT,
        )


class TestTheVerdictTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.claims = claim.verdict_table()

    def test_each_wording_carries_its_own_verdict(self) -> None:
        verdicts = [row.verdict for row in self.claims]
        self.assertEqual(
            verdicts,
            [
                claim.ClaimVerdict.PASS,
                claim.ClaimVerdict.FAIL,
                claim.ClaimVerdict.DEFER,
                claim.ClaimVerdict.FAIL,
                claim.ClaimVerdict.DEFER,
            ],
        )

    def test_every_row_names_its_evidence_and_its_limit(self) -> None:
        for row in self.claims:
            self.assertTrue(row.evidence.strip())
            self.assertTrue(row.limit.strip())

    def test_a_pass_and_a_fail_stand_together_without_contradiction(self) -> None:
        self.assertIs(self.claims[0].verdict, claim.ClaimVerdict.PASS)
        self.assertIs(self.claims[1].verdict, claim.ClaimVerdict.FAIL)

    def test_the_deferred_rows_name_what_is_missing_not_a_failure(self) -> None:
        for row in self.claims:
            if row.verdict is claim.ClaimVerdict.DEFER:
                self.assertTrue(
                    "غير" in row.evidence or "لا " in row.evidence,
                    msg=row.wording,
                )


class TestTheQuotedFiguresAreNotPromoted(unittest.TestCase):
    def test_the_study_totals_stay_quoted_and_are_not_reproduced(self) -> None:
        for figure in claim.THE_STUDY_TOTALS_THAT_ARE_NOT_REPRODUCED:
            self.assertIs(
                figure.provenance,
                claim.Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
            )

    def test_the_reproduced_structure_is_not_the_reproduced_total(self) -> None:
        quoted = {figure.name: figure.value for figure in claim.THE_STUDY_FIGURES}
        self.assertEqual(quoted["أليافُ الإسقاط المتصادمة"], 18)
        self.assertEqual(quoted["الأشكالُ داخل هذه الألياف"], 36)
        totals = {
            figure.name: figure.value
            for figure in claim.THE_STUDY_TOTALS_THAT_ARE_NOT_REPRODUCED
        }
        self.assertNotEqual(totals["الأشكالُ الجاهزة"], 9380)


if __name__ == "__main__":
    unittest.main()
