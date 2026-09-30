"""مصادماتُ الإيداع المأذون: يُعاد اشتقاقُ كلِّ ختمٍ، ولا يُقرأ توقيعٌ قياسًا."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import pytest

from alghanem.arabic.owner_licensed_deposit import (
    AN_OWNERS_AUTHORISATION_LICENSES_THE_COPY_NOT_THE_WORK,
    A_SIGNATURE_IS_A_DECLARATION_NOT_A_MEASUREMENT,
    COMPRESSED_BYTES_ARE_SEALED_BUT_NOT_READ,
    THE_AUTHORISATION_FILE,
    THE_DEPOSITS,
    DepositGenus,
    DepositStanding,
    OwnerLicensedDepositError,
    SealedDeposit,
    authorisation_signature,
    drifted_deposits,
    measure,
    read_authorisation,
    standing_of,
    unsigned_deposits,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_every_deposit_is_present_and_matches_its_transcribed_seal() -> None:
    for deposit in THE_DEPOSITS:
        reading = measure(deposit)
        assert reading.present, deposit.path
        assert reading.measured_sha256 == deposit.transcribed_sha256
        assert reading.measured_bytes == deposit.transcribed_bytes


def test_the_seal_is_rederived_from_the_bytes_and_not_read_off_the_prose() -> None:
    for deposit in THE_DEPOSITS:
        payload = (REPO_ROOT / deposit.path).read_bytes()
        assert sha256(payload).hexdigest() == deposit.transcribed_sha256
        assert len(payload) == deposit.transcribed_bytes


def test_both_deposits_stand_signed_and_sealed() -> None:
    assert {standing_of(one) for one in THE_DEPOSITS} == {
        DepositStanding.SIGNED_AND_SEALED
    }
    assert drifted_deposits() == ()
    assert unsigned_deposits() == ()


def test_a_deposit_the_authorisation_does_not_name_is_not_read_as_licensed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stranger = SealedDeposit(
        name="مادّةٌ لم يُوقَّع عليها",
        path="corpora/quran-simple-enhanced.txt",
        transcribed_sha256=sha256(
            (REPO_ROOT / "corpora/quran-simple-enhanced.txt").read_bytes()
        ).hexdigest(),
        transcribed_bytes=(
            REPO_ROOT / "corpora/quran-simple-enhanced.txt"
        ).stat().st_size,
        genus=DepositGenus.PLAIN_TEXT_READABLE,
        source="مودَعٌ آخرُ في الشجرة",
    )
    assert standing_of(stranger) is DepositStanding.PRESENT_BUT_UNSIGNED


def test_a_drifted_byte_falls_even_though_the_signature_still_stands(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """التوقيعُ يبقى إقرارًا صحيحًا، ويسقط الختمُ وحدَه؛ ولا يستر أحدُهما الآخر."""

    import alghanem.arabic.owner_licensed_deposit as unit

    shadow = tmp_path / "shadow"
    (shadow / "corpora").mkdir(parents=True)
    (shadow / "exhibits/owner-authorisation").mkdir(parents=True)
    (shadow / THE_AUTHORISATION_FILE).write_text(
        (REPO_ROOT / THE_AUTHORISATION_FILE).read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    target = THE_DEPOSITS[0]
    (shadow / target.path).write_bytes(
        (REPO_ROOT / target.path).read_bytes() + b"\n"
    )
    monkeypatch.setattr(unit, "_repository_root", lambda: shadow)

    assert unit.standing_of(target) is DepositStanding.SEALED_BUT_DRIFTED
    assert unit.authorisation_signature().strip()


def test_an_absent_deposit_reads_absent_and_not_merely_drifted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import alghanem.arabic.owner_licensed_deposit as unit

    empty = tmp_path / "empty"
    (empty / "exhibits/owner-authorisation").mkdir(parents=True)
    (empty / THE_AUTHORISATION_FILE).write_text(
        (REPO_ROOT / THE_AUTHORISATION_FILE).read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    monkeypatch.setattr(unit, "_repository_root", lambda: empty)
    assert unit.standing_of(THE_DEPOSITS[0]) is DepositStanding.ABSENT
    assert set(unit.drifted_deposits()) == set(THE_DEPOSITS)


def test_the_authorisation_names_both_what_it_licenses_and_what_it_does_not() -> None:
    body = read_authorisation()
    assert body["المُفوِّض"] == "Saleh1967"
    assert body["المأذونُ_فيه"]
    assert body["غيرُ_المأذونِ_فيه"]
    excluded = " ".join(body["غيرُ_المأذونِ_فيه"])
    assert "النبهاني" in excluded


def test_the_authorisation_seals_agree_with_the_prose_of_this_unit() -> None:
    entries = read_authorisation()["المودَعُ_بهذا_التفويض"]
    by_path = {entry["مسار"]: entry for entry in entries}
    for deposit in THE_DEPOSITS:
        entry = by_path[deposit.path]
        assert entry["sha256"] == deposit.transcribed_sha256
        assert entry["بايتات"] == deposit.transcribed_bytes
        assert entry["صنف"] == deposit.genus.value


def test_the_compressed_deposit_is_sealed_without_any_textual_figure() -> None:
    compressed = [
        one for one in THE_DEPOSITS if one.genus is DepositGenus.COMPRESSED_NOT_READ
    ]
    assert len(compressed) == 1
    source = Path(
        __import__(
            "alghanem.arabic.owner_licensed_deposit", fromlist=["__file__"]
        ).__file__
    ).read_text(encoding="utf-8")
    assert "document.xml" in source
    assert "zipfile" not in source


def test_a_malformed_deposit_is_refused_by_name() -> None:
    with pytest.raises(OwnerLicensedDepositError):
        SealedDeposit(
            name="  ",
            path="corpora/x",
            transcribed_sha256="0" * 64,
            transcribed_bytes=1,
            genus=DepositGenus.PLAIN_TEXT_READABLE,
            source="س",
        )
    with pytest.raises(OwnerLicensedDepositError):
        SealedDeposit(
            name="ختمٌ قصير",
            path="corpora/x",
            transcribed_sha256="0" * 10,
            transcribed_bytes=1,
            genus=DepositGenus.PLAIN_TEXT_READABLE,
            source="س",
        )
    with pytest.raises(OwnerLicensedDepositError):
        SealedDeposit(
            name="حجمٌ غيرُ موجب",
            path="corpora/x",
            transcribed_sha256="0" * 64,
            transcribed_bytes=0,
            genus=DepositGenus.PLAIN_TEXT_READABLE,
            source="س",
        )


def test_an_absent_authorisation_is_refused_and_not_silently_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import alghanem.arabic.owner_licensed_deposit as unit

    monkeypatch.setattr(unit, "_repository_root", lambda: tmp_path)
    with pytest.raises(OwnerLicensedDepositError):
        unit.read_authorisation()


def test_a_signatureless_authorisation_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import alghanem.arabic.owner_licensed_deposit as unit

    (tmp_path / "exhibits/owner-authorisation").mkdir(parents=True)
    (tmp_path / THE_AUTHORISATION_FILE).write_text(
        json.dumps({"تفويضُ_المالك": {"نصُّ_التفويض": "   "}}, ensure_ascii=False),
        encoding="utf-8",
    )
    monkeypatch.setattr(unit, "_repository_root", lambda: tmp_path)
    with pytest.raises(OwnerLicensedDepositError):
        unit.authorisation_signature()


def test_the_three_refusals_are_named_and_not_paraphrased() -> None:
    assert "قياس" in A_SIGNATURE_IS_A_DECLARATION_NOT_A_MEASUREMENT
    assert "المصنَّف" in AN_OWNERS_AUTHORISATION_LICENSES_THE_COPY_NOT_THE_WORK
    assert "استخراج" in COMPRESSED_BYTES_ARE_SEALED_BUT_NOT_READ


def test_the_authority_of_this_unit_stays_inert() -> None:
    source = Path(
        __import__(
            "alghanem.arabic.owner_licensed_deposit", fromlist=["__file__"]
        ).__file__
    ).read_text(encoding="utf-8")
    assert "from ..kernel" not in source
    assert "from alghanem.kernel" not in source
