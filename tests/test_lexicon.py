"""المبنيّاتُ والأدوات."""

from __future__ import annotations

from slge.cells import licensed
from slge.lexicon import CLOSED, MABNI, PARTICLES, WASL, entry
from slge.orthography import to_atoms


def test_every_entry_is_licensed() -> None:
    for label in (*PARTICLES, *MABNI):
        assert licensed(entry(label)), label
    for label in WASL:
        assert not licensed(to_atoms(label))  # يبدأ بوصل: لا يُنطق إلّا بالابتداء أو الوصل


def test_no_two_labels_share_atoms() -> None:
    labels = (*PARTICLES, *MABNI)
    assert len(set(labels)) == len(labels) == len(CLOSED)


def test_corrected_entries() -> None:
    assert entry("هِيَ") == [("ه", "كسر"), ("ي", "فتح")]
    assert entry("إِنَّ") == [("ء", "كسر"), ("ن", "سكون"), ("ن", "فتح")]
    assert entry("ذَانِكَ")[:2] == [("ذ", "فتح"), ("ا", "سكون")]
