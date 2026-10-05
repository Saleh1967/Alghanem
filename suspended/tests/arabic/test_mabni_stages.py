"""استنفادُ المبنيّات درجةً درجة: الجامعُ المانع، والقوائمُ المغلقة، والتقطيع."""

from itertools import product

from alghanem.arabic.mabni_stages import (
    SYLLABLES,
    atom_kinds,
    form_records,
    stage_reading,
    syllabify,
)

CVC_STAGE = (
    "أَمْ",
    "أَنْ",
    "أَوْ",
    "أَيْ",
    "إِذْ",
    "إِنْ",
    "ئِنْ",
    "ال",
    "الْ",
    "بَلْ",
    "تُمْ",
    "عَنْ",
    "قَدْ",
    "كَمْ",
    "كَيْ",
    "كُمْ",
    "لَسْ",
    "لَمْ",
    "لَنْ",
    "لَوْ",
    "مَنْ",
    "مِنْ",
    "هَلْ",
    "هُمْ",
    "هِمْ",
)

DEFERRALS = {
    "THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED": 14,
    "HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED": 18,
    "TANWIN_ATTACHMENT_IS_AMBIGUOUS": 1,
}


def test_every_form_is_either_syllabified_or_deferred_by_a_named_reason() -> None:
    reading = stage_reading()
    assert reading["forms"] == 2947
    assert reading["syllabified"] == 2914
    assert reading["deferred"] == DEFERRALS
    assert reading["syllabified"] + sum(DEFERRALS.values()) == reading["forms"]
    assert "NOT_SYLLABIFIABLE" not in reading["deferred"]


def test_coverage_by_genus_in_forms_and_tokens() -> None:
    records = form_records()
    expected = {
        "LEXICAL": (262, 291, 72967, 73451),
        "MORPHOLOGICAL": (2519, 2520, 13160, 13167),
        "POSITIONAL": (133, 136, 461, 468),
    }
    for genus, figures in expected.items():
        mine = [r for r in records if r.genus == genus]
        done = [r for r in mine if r.syllables]
        got = (
            len(done),
            len(mine),
            sum(r.tokens for r in done),
            sum(r.tokens for r in mine),
        )
        assert got == figures, genus


def test_the_monosyllabic_lexical_stages_are_closed_lists() -> None:
    stages = stage_reading()["lexical_monosyllables"]
    assert stages["CV"] == sorted(
        "أَ ئَ بِ تَ تُ تِ سَ فَ كَ كِ لَ لِ مَ نَ نُ نِ هَ هُ هِ وَ وُ يَ يُ يِ".split()
    )
    assert stages["CVV"] == sorted("إِي ذَا فِي لَا مَا نَا هَا وَا يَا".split())
    assert stages["CVC"] == sorted(CVC_STAGE)


def test_cvcc_never_occurs_and_cvvc_is_madd_before_a_geminate() -> None:
    records = [r for r in form_records() if r.syllables]
    assert not any("CVCC" in (r.syllables or ()) for r in records)
    superheavy = sorted(r.form for r in records if "CVVC" in (r.syllables or ()))
    assert superheavy == sorted("آلْ تَحَاجُّ حَاجَّ حَاجُّ حَادُّ شَاقُّ حَادَّ رَادَّ".split())


def test_examples_from_the_staged_reading() -> None:
    def syllables(form: str) -> tuple[str, ...] | None:
        result = atom_kinds(form)
        assert not isinstance(result, str), form
        return syllabify(result[1])

    assert syllables("هَٰذَا") == ("CVV", "CVV")
    assert syllables("هَذَا") == ("CV", "CVV")
    assert syllables("الَّذِينَ") == ("CVC", "CV", "CVV", "CV")
    assert syllables("مِنْهُمْ") == ("CVC", "CVC")
    assert syllables("مَا") == ("CVV",) and syllables("مِنْ") == ("CVC",)


def test_cvv_and_cvc_share_one_open_close_pattern() -> None:
    def pattern(form: str) -> str:
        result = atom_kinds(form)
        assert not isinstance(result, str)
        return "".join("M" if kind == "CV" else "S" for kind in result[1])

    assert pattern("مَا") == pattern("مِنْ") == "MS"


def test_syllabification_is_unique_and_reverses_on_short_strings() -> None:
    codas = {
        "CV": (),
        "CVV": ("V",),
        "CVC": ("C",),
        "CVVC": ("V", "C"),
        "CVCC": ("C", "C"),
        "CVVCC": ("V", "C", "C"),
    }
    leads = {"C|": ("C",), "V|": ("V",), "VC|": ("V", "C")}
    for n in range(1, 7):
        for kinds in product(("CV", "V", "C"), repeat=n):
            result = syllabify(kinds)
            if result is None:
                continue
            assert set(result) <= set(SYLLABLES)
            rebuilt: tuple[str, ...] = ()
            for piece in result:
                if piece in leads:
                    rebuilt += leads[piece]
                else:
                    rebuilt += ("CV", *codas[piece])
            assert rebuilt == kinds
