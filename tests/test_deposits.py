"""لا مودَعَ بلا نوع (دستورُ الوكيل، المادّة ١٢): كلُّ ملفٍّ في `tests/data/` مسجَّلٌ في `manifest.DEPOSITS`
بنوعٍ من الأربعة، وكلُّ مسجَّلٍ موجود؛ ولا مودَعَ من نوع «معلومات سابقة» يُقرأ من طبقةٍ دون «الحكم»."""

from __future__ import annotations

from conftest import ROOT
from slge.manifest import CERTIFICATES_DIGEST, DEPOSIT_KINDS, DEPOSITS, GATE_REV, Deposit
from slge.order import MODULE_LAYER, ancestors

DATA = ROOT / "tests" / "data"


def _problems(deposits: tuple[Deposit, ...], present: set[str]) -> list[str]:
    registered = {d.path for d in deposits}
    out = [f"UNREGISTERED_DEPOSIT:{p}" for p in sorted(present - registered)]
    out += [f"MISSING_DEPOSIT:{p}" for p in sorted(registered - present)]
    out += [f"DEPOSIT_KIND_UNDECLARED:{d.path}:{d.kind}" for d in deposits
            if d.kind not in DEPOSIT_KINDS]
    return out


def test_every_deposit_has_a_kind_and_exists() -> None:
    present = {p.name for p in DATA.iterdir() if p.is_file()}
    assert _problems(DEPOSITS, present) == []
    assert len(DEPOSITS) == len({d.path for d in DEPOSITS})
    assert {d.kind for d in DEPOSITS} == DEPOSIT_KINDS - {"معلومات سابقة"}


def test_mutations_are_named() -> None:
    present = {d.path for d in DEPOSITS}
    extra = present | {"mukhassas.json.gz"}
    assert _problems(DEPOSITS, extra) == ["UNREGISTERED_DEPOSIT:mukhassas.json.gz"]
    gone = present - {"sibawayh-abniya.tsv"}
    assert _problems(DEPOSITS, gone) == ["MISSING_DEPOSIT:sibawayh-abniya.tsv"]
    bent = (*DEPOSITS, Deposit("x.json", "حقيقة"))
    assert _problems(bent, present | {"x.json"}) == ["DEPOSIT_KIND_UNDECLARED:x.json:حقيقة"]


def test_prior_knowledge_is_read_only_above_the_gates() -> None:
    """المادّة ١٠: «الحكم» فوق «البوابات»، فلا بوّابةَ تستورد منه؛ وما يقرأ مودَعًا من نوع
    «معلومات سابقة» (حين يوجد) يسكن طبقةَ الحكم أو فوقها."""
    assert "البوابات" in ancestors("الحكم")
    assert "الحكم" not in ancestors("البوابات")
    hukm = [m for m, layer in MODULE_LAYER.items() if layer == "الحكم"]
    # لا وحدةَ في الحكم بلا إذنٍ مسجَّل (المادّة ٩): المخصّص ADR ١٥؛ والتغطيةُ بإذن المالك «غطي بالبرهان
    # وعرف الشاهد» (2026-10-09، ADR ٢٩)
    assert hukm == ["mukhassas", "coverage"], "HUKM_MODULE_WITHOUT_RECORDED_PERMISSION"


def _canonical(d: object) -> str:
    import hashlib
    import json

    blob = json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def test_certificates_deposit_is_what_the_pinned_gate_printed() -> None:
    """خياطةُ الطبقتين: بصمةُ المودَع القانونيّة هي ما طبعته بوّابةُ الغانم على `GATE_REV`؛ وCI
    (`ci.yml`) يستنسخ البوّابةَ على الإيداع نفسه ويعيد التوليدَ قيمةً قيمة
    (`DEPOSIT_DRIFTED_FROM_GATE`)."""

    import gzip
    import json

    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d = json.load(f)
    assert _canonical(d) == CERTIFICATES_DIGEST
    assert len(GATE_REV) == 40 and d["tokens"] == 78245 and len(d["forms"]) == 18179
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "GATE_REV" in ci and "gen_certificates.py --check" in ci  # CI يقرأ الإيداعَ من هنا
    d["forms"][7]["fiber_size"] += 1
    assert _canonical(d) != CERTIFICATES_DIGEST


def test_context_deposit_is_what_the_pinned_gate_printed() -> None:
    """المودَعُ الثاني (ADR ٢٨): المصحفُ موقعًا موقعًا في سياقه؛ بصمتُه القانونيّة ما طبعته البوّابةُ على
    `GATE_REV` نفسِه، ومواقعُه مواقعُ الأوّل، وCI يعيد توليدَه من البوّابة نفسِها."""

    import gzip
    import json

    from slge.manifest import CONTEXT_CERTIFICATES_DIGEST

    with gzip.open(DATA / "context-certificates.json.gz", "rt", encoding="utf-8") as f:
        d = json.load(f)
    assert _canonical(d) == CONTEXT_CERTIFICATES_DIGEST
    assert d["tokens"] == 78245 == len(d["stream"]) == sum(d["line_lengths"]) and d["lines"] == 6236
    assert set(d["status"]) == {"READY", "REJECT", "DEFER"} and sum(d["status"].values()) == 78245
    assert all(r.split(":")[0] in ("REJECT", "DEFER") for r in d["refusals"])
    assert set(d["boundary_policy"]) == {"line", "entry", "exit", "domain"}
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "gen_context_certificates.py --check" in ci
    d["stream"][3][1] ^= 1
    assert _canonical(d) != CONTEXT_CERTIFICATES_DIGEST
