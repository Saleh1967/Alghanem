"""ذرّاتُ الكلمات في `Ladder.lean` هي ما يُخرجه الجسرُ لها بعينه."""

import re
from pathlib import Path

from canonical116.bridge import bridge

LEAN = Path(__file__).resolve().parents[2] / "formal/a116/A116/Ladder.lean"
MARK = {"fatha": "َ", "damma": "ُ", "kasra": "ِ", "sukun": "ْ"}
WORDS = {
    "kataba": "كَتَبَ",
    "kana": "كَانَ",
    "laysa": "لَيْسَ",
    "layta": "لَيْتَ",
    "inna": "إِنَّ",
    "laalla": "لَعَلَّ",
    "kaanna": "كَأَنَّ",
    "lakinna": "لَكِنَّ",
}


def _lean_atoms(name: str) -> list[str]:
    text = LEAN.read_text("utf-8")
    line = re.search(rf"def {name} : List Cell := \[(.*)\]", text)
    assert line, name
    pairs = re.findall(r"atom '(.)' (\w+)", line.group(1))
    return [letter + MARK[haraka] for letter, haraka in pairs]


def test_every_cited_word_matches_the_bridge() -> None:
    for name, word in WORDS.items():
        record = bridge(word)
        assert record["status"] == "READY", word
        assert record["canonical_atoms"] == _lean_atoms(name), word
