"""«الجرد المغلق» مقيسًا: الجردُ المجمَّد، ومعايرتُه على سيبويه، وفحصُه على MASAQ."""

import re
import subprocess
import sys
from pathlib import Path

import pytest

from alghanem.arabic.closed_inventory import (
    INVENTORY_PATH,
    calibration,
    inventory,
    masaq_reading,
)
from alghanem.arabic.pipeline_stations import repository_root_path

_HAMIL_SOURCES = Path("/home/claude/hamil-hala-zaman-program/corpora/sources")


def test_the_frozen_inventory_has_its_declared_size_and_tiers() -> None:
    tiers = inventory()
    assert len(tiers) == 158
    counts: dict[str, int] = {}
    for t in tiers.values():
        key = "".join(sorted(t))
        counts[key] = counts.get(key, 0) + 1
    assert counts == {"N": 128, "V": 15, "NV": 9, "NP": 2, "PV": 2, "P": 2}


@pytest.mark.skipif(not _HAMIL_SOURCES.is_dir(), reason="hamil sources absent")
def test_the_inventory_is_reproduced_from_the_two_editions(tmp_path: Path) -> None:
    root = repository_root_path()
    out = tmp_path / "abniya.tsv"
    subprocess.run(
        [
            sys.executable,
            str(root / "tools" / "sibawayh_abniya_extract.py"),
            str(_HAMIL_SOURCES),
            str(out),
        ],
        check=True,
    )
    assert out.read_bytes() == (root / INVENTORY_PATH).read_bytes()


def test_the_skeleton_test_does_not_reproduce_sibawayh_on_loanwords() -> None:
    reading = calibration()
    assert all(reading["attached"].values())
    not_reached = reading["not_reached"]
    assert sorted(w for w, found in not_reached.items() if not found) == [
        "إبريسم",
        "إسماعيل",
    ]
    assert sorted(w for w, found in not_reached.items() if found) == [
        "آجر",
        "سراويل",
        "فيروز",
        "قهرمان",
    ]
    assert all(reading["left_as_is"].values())


def test_masaq_noun_stems_against_the_frozen_inventory() -> None:
    reading = masaq_reading()
    assert reading["stem_types"] == 5462
    assert reading["stem_tokens"] == 29752
    assert reading["unaligned_tokens"] == 598
    assert reading["matched_types_by_first_tier"] == {"N": 5383, "P": 20, "PV": 8}
    unmatched = reading["unmatched"]
    assert len(unmatched) == 51
    assert sum(n for n, _ in unmatched.values()) == 439
    beyond_two_letters = sorted(
        form for form in unmatched if len(re.sub("[ً-ْ]", "", form)) > 2
    )
    assert beyond_two_letters == sorted(
        "إِبْرَاهِيمَ إِبْرَاهِيمُ إِسْرَائِيلَ إِسْرَائِيلُ إِسْمَاعِيلَ إِسْمَاعِيلُ "
        "إِسْتَبْرَقٍ إِسْتَبْرَقٌ اسْتِكْبَارَ اسْتِبْدَالَ اسْتِحْيَاءٍ "
        "اسْتِعْجَالَ اسْتِغْفَارُ".split()
    )
    two = [form for form in unmatched if form not in beyond_two_letters]
    assert (len(two), sum(unmatched[f][0] for f in two)) == (38, 305)
