"""اختباراتُ الجسر المرجعيّ: قبولٌ ومنعٌ لكلِّ قاعدةٍ مصرَّحٍ بها في العقد."""

from __future__ import annotations

import unittest
from typing import Any

from canonical116 import A116, HARAKAT, PROTOCOL_VERSION, bridge, count_atoms, verify
from canonical116.bridge import CountingRefused

START_CONTINUE = {"0": {"entry": "start", "exit": "continue"}}
START_PAUSE = {"0": {"entry": "start", "exit": "pause"}}


def atoms_of(text: str, **kwargs: Any) -> list[str]:
    atoms = bridge(text, **kwargs)["canonical_atoms"]
    assert isinstance(atoms, list)
    return atoms


class AWaslAlifAfterAPrefixIsNotReadAsMadd(unittest.TestCase):
    """فَ + اتَّبِعْ: ألفُ الوصل بعد السابقة تسقط في النطق، فلا تُقرأ ألفَ مدّ.

    وصورتُها السطحيّة (حرفُ سابقةٍ مفتوح + ألفٌ عارية + ساكنٌ أو مشدَّد) هي صورةُ
    `كَافَّةً` ذاتِ المدّ اللازم؛ فالجسرُ يعلّق ولا يحسم.
    """

    def test_wasl_after_fa_defers_with_its_name(self) -> None:
        for word in ("فَاتَّبِعْ", "فَاجْعَلْ", "وَالْكِتَابِ", "أَفَاتَّخَذْتُمْ", "لَّاتَّبَعْنَاكُمْ"):
            record = bridge(word, contexts=START_CONTINUE)
            self.assertEqual(record["status"], "DEFER", word)
            self.assertEqual(
                record["deferrals"][0]["reason"],
                "ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL",
            )
            self.assertIsNone(record["canonical_atoms"])

    def test_the_same_surface_shape_with_a_true_madd_also_defers(self) -> None:
        self.assertEqual(bridge("كَافَّةً", contexts=START_CONTINUE)["status"], "DEFER")

    def test_a_madd_before_a_vowelled_letter_stays_madd(self) -> None:
        self.assertEqual(
            atoms_of("فَاطِرِ", contexts=START_CONTINUE), ["فَ", "اْ", "طِ", "رِ"]
        )
        self.assertEqual(atoms_of("كَانَ", contexts=START_CONTINUE), ["كَ", "اْ", "نَ"])
        self.assertEqual(atoms_of("لَا", contexts=START_CONTINUE), ["لَ", "اْ"])

    def test_a_madd_lazim_after_a_non_prefix_letter_stays_madd(self) -> None:
        self.assertEqual(
            atoms_of("دَابَّةٍ", contexts=START_CONTINUE), ["دَ", "اْ", "بْ", "بَ", "تِ", "نْ"]
        )


class TheAlphabetIsOneHundredAndSixteen(unittest.TestCase):
    def test_the_product_is_twenty_nine_by_four(self) -> None:
        self.assertEqual(len(A116), 116)
        self.assertEqual(len(set(A116)), 116)
        self.assertEqual(len(HARAKAT), 4)

    def test_the_protocol_names_its_version(self) -> None:
        self.assertEqual(PROTOCOL_VERSION, "A116-CANONICAL-TXT-1.1")

    def test_version_one_zero_is_kept_byte_for_byte(self) -> None:
        import hashlib
        from pathlib import Path

        from canonical116 import bridge_v1_0

        frozen = Path(bridge_v1_0.__file__).read_bytes()
        self.assertEqual(
            hashlib.sha256(frozen).hexdigest(),
            "982586e4b8fd7c91ca7243c132cf6de6356d81b3d8ce4b2d3832e37db393e1ab",
        )
        self.assertEqual(bridge_v1_0.PROTOCOL_VERSION, "A116-CANONICAL-TXT-1.0")

    def test_a_one_zero_certificate_replays_under_one_zero(self) -> None:
        from canonical116 import bridge_v1_0

        old = bridge_v1_0.bridge("فَاتَّبِعْ", contexts=START_CONTINUE)
        self.assertEqual(old["status"], "READY")
        self.assertTrue(verify(old)["reproduced"])
        self.assertEqual(bridge("فَاتَّبِعْ", contexts=START_CONTINUE)["status"], "DEFER")


class TheOrthographicRasmIsProjected(unittest.TestCase):
    def test_a_fully_vocalised_word_is_ready(self) -> None:
        record = bridge("مَلِكِ", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "READY")
        self.assertEqual(record["canonical_atoms"], ["مَ", "لِ", "كِ"])
        self.assertTrue(record["count_eligible"])

    def test_madd_alif_after_an_explicit_fatha(self) -> None:
        self.assertEqual(atoms_of("قَالَ", contexts=START_CONTINUE), ["قَ", "اْ", "لَ"])

    def test_madda_resolves_to_hamza_then_madd_alif(self) -> None:
        self.assertEqual(atoms_of("آمَنَ", contexts=START_CONTINUE), ["ءَ", "اْ", "مَ", "نَ"])

    def test_a_hamza_seat_is_projected_to_the_bare_hamza(self) -> None:
        self.assertEqual(
            atoms_of("مُؤْمِنٌ", contexts=START_CONTINUE),
            ["مُ", "ءْ", "مِ", "نُ", "نْ"],
        )

    def test_shadda_is_two_halves(self) -> None:
        self.assertEqual(
            atoms_of("مُحَمَّدٌ", contexts=START_CONTINUE),
            ["مُ", "حَ", "مْ", "مَ", "دُ", "نْ"],
        )

    def test_shadda_in_pause_is_two_sakin_halves(self) -> None:
        self.assertEqual(atoms_of("قَوِيٌّ", contexts=START_PAUSE)[-2:], ["يْ", "يْ"])

    def test_waw_and_ya_of_madd_keep_their_carriers(self) -> None:
        self.assertEqual(atoms_of("شَيْءٌ", contexts=START_PAUSE), ["شَ", "يْ", "ءْ"])


class TheBoundaryAxesMoveTheProjection(unittest.TestCase):
    def test_ta_marbuta_is_ta_in_continuation_and_ha_in_pause(self) -> None:
        self.assertEqual(
            atoms_of("رَحْمَةٌ", contexts=START_CONTINUE),
            ["رَ", "حْ", "مَ", "تُ", "نْ"],
        )
        self.assertEqual(atoms_of("رَحْمَةٌ", contexts=START_PAUSE), ["رَ", "حْ", "مَ", "هْ"])

    def test_tanwin_fath_in_pause_becomes_a_madd_alif(self) -> None:
        self.assertEqual(
            atoms_of("كِتَابًا", contexts=START_PAUSE), ["كِ", "تَ", "اْ", "بَ", "اْ"]
        )

    def test_tanwin_damm_and_kasr_in_pause_leave_a_sakin_consonant(self) -> None:
        self.assertEqual(atoms_of("مَلِكٌ", contexts=START_PAUSE), ["مَ", "لِ", "كْ"])

    def test_the_tanwin_support_alif_is_an_orthographic_zero(self) -> None:
        record = bridge("هُدًى", contexts=START_PAUSE)
        self.assertEqual(record["canonical_atoms"], ["هُ", "دَ", "اْ"])
        roles = [cluster["role"] for cluster in record["words"][0]["clusters"]]
        self.assertIn("TANWIN_SUPPORT", roles)

    def test_a_final_haraka_is_dropped_in_pause_only(self) -> None:
        self.assertEqual(atoms_of("مَلِكِ", contexts=START_PAUSE)[-1], "كْ")


class TheWaslIsDecidedByItsWitness(unittest.TestCase):
    def test_the_documented_example_resolves_with_an_annotation(self) -> None:
        record = bridge(
            "ابْنُ",
            annotations={
                "0": {
                    "0": {
                        "role": "WASL",
                        "start_vowel": "\u0650",
                        "evidence": "lexicon:approved-entry:ibn",
                    }
                }
            },
        )
        self.assertEqual(record["canonical_atoms"], ["ءِ", "بْ", "نُ"])

    def test_a_wasl_alif_is_a_zero_when_the_word_is_joined(self) -> None:
        record = bridge(
            "ٱلْحَمْدُ",
            contexts={"0": {"entry": "start", "exit": "pause"}},
            annotations={
                "0": {"0": {"start_vowel": "\u064e", "evidence": "quran:1:2"}}
            },
        )
        self.assertEqual(record["status"], "READY")
        self.assertEqual(record["canonical_atoms"][0], "ءَ")

    def test_an_undeclared_start_vowel_defers(self) -> None:
        record = bridge("ٱلْحَمْدُ", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "DEFER")
        self.assertIsNone(record["canonical_atoms"])

    def test_a_joined_first_word_has_no_left_context(self) -> None:
        record = bridge("ٱلْحَمْدُ", contexts={"0": {"entry": "joined"}})
        self.assertEqual(record["status"], "INVALID_CONFIGURATION")

    def test_an_annotation_without_evidence_is_refused(self) -> None:
        record = bridge("ابْنُ", annotations={"0": {"0": {"role": "WASL"}}})
        self.assertEqual(record["status"], "INVALID_CONFIGURATION")

    def test_an_unsupported_role_is_refused(self) -> None:
        record = bridge(
            "ابْنُ", annotations={"0": {"0": {"role": "GUESS", "evidence": "x"}}}
        )
        self.assertEqual(record["status"], "INVALID_CONFIGURATION")


class TheSilentSupportNeedsAWitness(unittest.TestCase):
    def test_an_internal_silent_alif_defers_without_its_witness(self) -> None:
        record = bridge("مِائَةٌ", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "DEFER")

    def test_the_annotated_silent_alif_projects_like_the_shorter_spelling(self) -> None:
        annotated = bridge(
            "مِائَةٌ",
            contexts=START_CONTINUE,
            annotations={
                "0": {"1": {"role": "SILENT_SUPPORT", "evidence": "lexicon:mi-a"}}
            },
        )
        plain = bridge("مِئَةٌ", contexts=START_CONTINUE)
        self.assertEqual(annotated["status"], "READY")
        self.assertEqual(annotated["canonical_atoms"], plain["canonical_atoms"])
        self.assertNotEqual(
            annotated["words"][0]["source"], plain["words"][0]["source"]
        )


class TheRefusalsAreNamedNotSilent(unittest.TestCase):
    def test_an_absent_internal_haraka_is_never_guessed(self) -> None:
        record = bridge("كتاب", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "DEFER")
        self.assertEqual(
            record["deferrals"][0]["reason"], "HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED"
        )

    def test_a_vowel_with_a_sukun_is_a_rejection(self) -> None:
        record = bridge("بَْ", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "REJECT")

    def test_a_shadda_with_a_sukun_is_a_rejection(self) -> None:
        record = bridge("مَبّْ", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "REJECT")

    def test_a_foreign_letter_blocks_the_count_instead_of_dropping(self) -> None:
        record = bridge("مَلِكِ x", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "READY")
        self.assertEqual([span["source"] for span in record["boundaries"]], [" x"])
        self.assertFalse(any(span["atomic"] for span in record["boundaries"]))

    def test_an_unsupported_mark_defers(self) -> None:
        record = bridge("مَ\u06e1لِكِ", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "DEFER")
        self.assertEqual(record["deferrals"][0]["reason"], "UNSUPPORTED_MARK")

    def test_a_multi_word_text_without_a_boundary_interface_defers(self) -> None:
        record = bridge("مَلِكِ مَلِكِ")
        self.assertEqual(record["status"], "DEFER")

    def test_a_contradictory_boundary_interface_is_refused(self) -> None:
        record = bridge(
            "مَلِكِ مَلِكِ",
            contexts={
                "0": {"entry": "start", "exit": "continue"},
                "1": {"entry": "start", "exit": "pause"},
            },
        )
        self.assertEqual(record["status"], "INVALID_CONFIGURATION")

    def test_broken_bytes_are_refused_without_replacement(self) -> None:
        record = bridge(b"\xff\xfe\x00mal", encoding="utf-8")
        self.assertEqual(record["status"], "INVALID_ENCODING_OR_TYPE")
        self.assertIsNone(record["canonical_atoms"])

    def test_a_non_text_input_is_refused(self) -> None:
        record = bridge(116)  # type: ignore[arg-type]
        self.assertEqual(record["status"], "INVALID_ENCODING_OR_TYPE")

    def test_an_unknown_profile_is_refused(self) -> None:
        record = bridge("مَلِكِ", profile="unknown-profile")
        self.assertEqual(record["status"], "INVALID_CONFIGURATION")


class TheSourceAndIdentityAreKept(unittest.TestCase):
    def test_the_source_is_kept_whole_with_its_digest(self) -> None:
        record = bridge("مَلِكِ", contexts=START_CONTINUE)
        self.assertEqual(record["source_text"], "مَلِكِ")
        self.assertEqual(len(record["source_sha256"]), 64)
        self.assertIsNotNone(record["source_bytes_base64"])

    def test_the_register_separates_two_words_that_share_a_projection(self) -> None:
        ta = bridge("رَحْمَةٌ", contexts=START_PAUSE)
        ha = bridge("رَحْمَهْ", contexts=START_PAUSE)
        self.assertEqual(ta["canonical_atoms"], ha["canonical_atoms"])
        self.assertNotEqual(ta["source_text"], ha["source_text"])
        ta_roles = [cluster["role"] for cluster in ta["words"][0]["clusters"]]
        self.assertIn("TA_MARBUTA", ta_roles)

    def test_the_tatweel_is_dropped_from_the_projection_and_recorded(self) -> None:
        record = bridge("مَلـِكِ", contexts=START_CONTINUE)
        self.assertEqual(record["status"], "READY")
        self.assertEqual(record["typographic_notes"][0]["note"], "TATWEEL_DROPPED")

    def test_an_equivalent_mark_order_does_not_move_the_atom(self) -> None:
        first = bridge("قَوِيٌّ", contexts=START_CONTINUE)
        second = bridge("قَوِي\u064c\u0651", contexts=START_CONTINUE)
        self.assertEqual(first["canonical_atoms"], second["canonical_atoms"])


class TheCountGateIsTheOnlyDoor(unittest.TestCase):
    def test_the_count_covers_every_key_including_the_zeros(self) -> None:
        record = bridge("مَلِكِ", contexts=START_CONTINUE)
        counts = count_atoms(record)
        self.assertEqual(len(counts), 116)
        self.assertEqual(sum(counts.values()), 3)
        self.assertEqual(counts["مَ"], 1)
        self.assertEqual(counts["زْ"], 0)

    def test_the_count_is_refused_for_every_status_but_ready(self) -> None:
        for text in ("كتاب", "بَْ", "مَلِكِ مَلِكِ"):
            with self.assertRaises(CountingRefused):
                count_atoms(bridge(text))

    def test_verification_replays_the_certificate_from_its_source(self) -> None:
        record = bridge("مَلِكِ", contexts=START_CONTINUE)
        self.assertTrue(verify(record)["reproduced"])

    def test_a_tampered_certificate_does_not_reproduce(self) -> None:
        record = bridge("مَلِكِ", contexts=START_CONTINUE)
        record["canonical_atoms"] = ["مَ"]
        self.assertFalse(verify(record)["reproduced"])
        with self.assertRaises(CountingRefused):
            count_atoms(record)

    def test_every_counted_atom_is_a_cell_of_the_one_hundred_and_sixteen(self) -> None:
        record = bridge("كِتَابًا", contexts=START_PAUSE)
        for atom in record["canonical_atoms"]:
            self.assertIn(atom, A116)


if __name__ == "__main__":
    unittest.main()
