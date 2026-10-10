"""الختمُ بإذن المالك: كلُّ مودَعٍ مختوم بصمتُه (بعد فكّ الضغط) ورخصتُه مثبَّتتان، والبايتُ الواحد يُسقطه."""

from __future__ import annotations

import gzip
import hashlib

from conftest import ROOT
from slge.manifest import DEPOSITS

DATA = ROOT / "tests" / "data"
SEALED = tuple(d for d in DEPOSITS if d.licence.startswith("CC BY-NC-SA"))
SIGNED = tuple(d for d in DEPOSITS if d.licence == "بتوقيع المالك")
OWNER_SEALED = tuple(d for d in DEPOSITS if d.licence == "بإذن المالك")


def test_sealed_sources_match_their_hash_and_carry_a_licence() -> None:
    # الغزاليُّ ثلاثةً بإذن المالك «نختم وفق النبهاني» (2026-10-10، ADR ٣٢)
    assert [d.path for d in SEALED] == ["openiti-mukhassas.txt.gz", "openiti-maqayis.txt.gz",
                                         "openiti-sibawayh-kitab.txt.gz",
                                         "openiti-ghazali-mustasfa.txt.gz",
                                         "openiti-ghazali-mihakk.txt.gz",
                                         "openiti-ghazali-micyar.txt.gz",
                                         "openiti-majaz-quran.txt.gz"]
    for d in SEALED:
        raw = gzip.decompress((DATA / d.path).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == d.sha256, d.path
        assert d.licence.startswith("CC BY-NC-SA 4.0") and d.kind in ("وضع", "مرجع محجوب"), d.path
        assert raw.startswith(b"######OpenITI#"), d.path


def test_owner_signed_deposits_match_their_hash_and_name_the_signer() -> None:
    assert [d.path for d in SIGNED] == ["owner-alam.json"]
    for d in SIGNED:
        raw = (DATA / d.path).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == d.sha256 and d.kind == "وضع", d.path
        assert "بتوقيع المالك" in raw.decode("utf-8"), d.path


def test_owner_sealed_books_match_their_hash() -> None:
    assert [d.path for d in OWNER_SEALED] == ["nabhani-shakhsiyya-3.txt.gz",
                                               "nabhani-tafkir.txt.gz"]
    for d in OWNER_SEALED:
        raw = gzip.decompress((DATA / d.path).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == d.sha256 and d.kind == "وضع", d.path
        assert "النبهاني" in raw.decode("utf-8") or "أبحاث اللغة" in raw.decode("utf-8"), d.path
    assert len(SEALED) + len(SIGNED) + len(OWNER_SEALED) == sum(1 for d in DEPOSITS if d.sha256)


def test_one_byte_breaks_the_seal() -> None:
    d = SEALED[2]
    raw = bytearray(gzip.decompress((DATA / d.path).read_bytes()))
    raw[len(raw) // 2] ^= 1
    assert hashlib.sha256(bytes(raw)).hexdigest() != d.sha256


def test_unsealed_deposits_have_no_hash_claim() -> None:
    for d in DEPOSITS:
        assert bool(d.sha256) == bool(d.licence), d.path
