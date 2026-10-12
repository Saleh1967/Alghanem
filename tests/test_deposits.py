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
    assert {d.kind for d in DEPOSITS} == DEPOSIT_KINDS  # الأنواعُ الأربعة كلُّها مودَعة (ADR ٣٤)


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
    # والسلسلةُ بإذن المالك «موافق راجع النبهاني أولا ونفذ» (2026-10-10، ADR ٣١)
    # والحكمُ بإذن المالك «نفذ وفق أفضل الممارسات SLGE والبرهان» (2026-10-10، ADR ٣٤)
    assert hukm == ["mukhassas", "coverage", "salsala", "hukm"], (
        "HUKM_MODULE_WITHOUT_RECORDED_PERMISSION")


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


def test_certificate_n_is_carried_whole() -> None:
    """الـn (الغانم ADR ١٤، `A116.Certificate`): لكلّ صورةٍ عددُ شهادتها ورتبتُها في ليفها وبقيّةُ رسمها؛
    والعددُ هو ‎P(F(الخانات)، الرتبة)‎ بترقيم SLGE نفسِه (`shahada.atom_number`، `shahada.pair`) على
    المودَع كلِّه. الخاناتُ وحدَها تُسقط الرتبة: «عَلَى» و«عَلَا» خاناتٌ واحدة وعددان (رتبتاهما 1 و0)."""

    import gzip
    import json

    from slge.shahada import atom_number, pair

    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        forms = json.load(f)["forms"]
    for x in forms:
        w = tuple((a, b) for a, b in x["cells"])
        assert 0 <= x["ordinal"] < x["fiber_size"]
        assert x["integer"] == pair(atom_number(w), x["ordinal"])
    ala = [x for x in forms if x["cells"] == [["ع", "فتح"], ["ل", "فتح"], ["ا", "سكون"]]]
    assert sorted(x["ordinal"] for x in ala) == [0, 1] and len({x["integer"] for x in ala}) == 2
    # الطفرة: الخاناتُ وحدَها مفتاحًا تجعلهما صورةً واحدة
    assert len({tuple(map(tuple, x["cells"])) for x in ala}) == 1


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


def test_hadith_context_deposit_is_what_the_pinned_gate_printed() -> None:
    """المدوّنةُ المختومةُ الثانية (الغانم ADR ٧): الصحيحان موقعًا موقعًا في سياقهما من البوّابة نفسِها
    على `GATE_REV` نفسِه، بالقانون نفسِه (سياسةُ الحدّ واحدة) وبصمةِ مدوّنتها المختومة؛ CI يعيد توليدَه
    من البوّابة. رموزُ الطبعة ليست مواقع فلا تُعدّ."""

    import gzip
    import json

    from slge.manifest import HADITH_CONTEXT_CERTIFICATES_DIGEST

    with gzip.open(DATA / "hadith-context-certificates.json.gz", "rt", encoding="utf-8") as f:
        d = json.load(f)
    with gzip.open(DATA / "context-certificates.json.gz", "rt", encoding="utf-8") as f:
        quran = json.load(f)
    assert _canonical(d) == HADITH_CONTEXT_CERTIFICATES_DIGEST
    assert d["tokens"] == 995413 == len(d["stream"]) == sum(d["line_lengths"])
    assert d["lines"] == 12370
    assert d["corpus_sha256"] != quran["corpus_sha256"] and len(d["corpus_sha256"]) == 64
    assert d["boundary_policy"] == quran["boundary_policy"]
    assert d["bridge_protocol"] == quran["bridge_protocol"]
    assert set(d["status"]) == {"READY", "REJECT", "DEFER"} and sum(d["status"].values()) == 995413
    assert all(r.split(":")[0] in ("REJECT", "DEFER") for r in d["refusals"])
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "--corpus sahihain --check tests/data/hadith-context-certificates.json.gz" in ci
    d["stream"][3][1] ^= 1
    assert _canonical(d) != HADITH_CONTEXT_CERTIFICATES_DIGEST


def test_lane_context_deposit_is_what_the_pinned_gate_printed() -> None:
    """المجالُ المختومُ الرابع (الغانم ADR ٣٣، ٤٥): معجمُ لين كلُّ وسمٍ عربيٍّ سطرٌ، موقعًا موقعًا في
    سياقه من البوّابة نفسِها على `GATE_REV`، بالقانون نفسِه وبصمةِ مدوّنته المختومة؛ والرفضُ بحالتيه
    وحدَهما (لا حالةَ رابعة: كان الموصولُ بحرفٍ خارج الحوامل يُخرج INVALID_CONFIGURATION حتى الغانم
    ADR ٤٥)؛ CI يعيد توليدَه من البوّابة."""

    import gzip
    import json

    from slge.manifest import LANE_CONTEXT_CERTIFICATES_DIGEST

    with gzip.open(DATA / "lane-context-certificates.json.gz", "rt", encoding="utf-8") as f:
        d = json.load(f)
    with gzip.open(DATA / "context-certificates.json.gz", "rt", encoding="utf-8") as f:
        quran = json.load(f)
    assert _canonical(d) == LANE_CONTEXT_CERTIFICATES_DIGEST
    assert d["tokens"] == 518930 == len(d["stream"]) == sum(d["line_lengths"])
    assert d["lines"] == 382852
    assert d["corpus_sha256"] == (
        "248def99adaf4ba565f250685b102591b3cbce4c1d09524fbb58f92bf270a1d5")
    assert d["boundary_policy"] == quran["boundary_policy"]
    assert d["bridge_protocol"] == quran["bridge_protocol"]
    assert set(d["status"]) == {"READY", "REJECT", "DEFER"} and sum(d["status"].values()) == 518930
    assert all(r.split(":")[0] in ("REJECT", "DEFER") for r in d["refusals"])
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "--corpus lane --check tests/data/lane-context-certificates.json.gz" in ci
    d["stream"][7][1] ^= 1
    assert _canonical(d) != LANE_CONTEXT_CERTIFICATES_DIGEST
