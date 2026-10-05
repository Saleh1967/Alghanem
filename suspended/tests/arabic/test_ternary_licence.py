"""الترخيصُ الثلاثيّ على نصٍّ مشكولٍ خارجَ القرآن: ما يرفضه الثنائيُّ وما يقبله الوصلُ والوقف."""

from alghanem.arabic.ternary_licence import (
    binary_licensed,
    licences,
    longest_syllabified_word,
    tashkeela_reading,
)


def test_the_three_licences_on_the_witnesses_proved_in_lean() -> None:
    hajja = ("CV", "V", "C", "CV")
    bahr = ("CV", "C", "C")
    tamm = ("CV", "V", "C", "C")
    assert not binary_licensed(hajja) and licences(hajja) == (True, True)
    assert not binary_licensed(bahr) and licences(bahr) == (False, True)
    assert licences(tamm) == (False, True)
    assert binary_licensed(("CV", "V", "CV")) and licences(("CV", "V", "CV")) == (
        True,
        True,
    )


def test_every_ready_word_of_the_external_text_is_syllabified() -> None:
    reading = tashkeela_reading()
    assert reading["words"] == 107291
    assert reading["syllabified"] == 95400
    assert "NOT_SYLLABIFIABLE" not in reading["deferred"]
    assert reading["syllabified"] + sum(reading["deferred"].values()) == 107291


def test_the_syllable_inventory_outside_the_quran() -> None:
    syllables = tashkeela_reading()["syllables"]
    assert syllables == {
        "CV": 148025,
        "CVC": 80329,
        "CVV": 39524,
        "CVVC": 139,
        "C|": 607,
        "V|": 18,
    }


def test_the_binary_model_rejects_exactly_cvvc_and_the_two_fragments() -> None:
    reading = tashkeela_reading()
    assert reading["binary_rejected"] == {"C|": 607, "CVVC": 139, "V|": 18}
    assert reading["continue_rejected"] == {"C|": 607, "V|": 18}


def test_pause_forms_need_the_pause_licence() -> None:
    pause = tashkeela_reading()["pause"]
    assert pause == {
        "deferred": 1106,
        "ready": 1394,
        "binary_rejected": 309,
        "continue_licensed": 1177,
        "pause_licensed": 1392,
    }


def test_all_116_cells_are_witnessed_and_the_vowelled_alif_only_by_spelling() -> None:
    reading = tashkeela_reading()
    assert reading["cells_witnessed"] == 116
    assert reading["vowelled_alif"] == {"اَ": 41, "اُ": 88, "اِ": 5}


def test_the_conformance_bound_covers_the_longest_word() -> None:
    assert longest_syllabified_word() == 11
