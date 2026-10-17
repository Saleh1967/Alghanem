"""شهاداتُ الوضع من أصحاب المعاجم، معلومةٌ مشهودة (`A116.Naql`، `tools/gen_naql.py`، ADR ١٠٠).

التوقّعاتُ مستقلّةٌ عن `tools/gen_naql.py` وعن Lean:
١. ختمُ اللسان: بصمتُه وحجمُه مكتوبان هنا باليد، وسطرُ «كتب» فيه بعينه.
٢. المراسي في ج3 المختوم س367 ببصمته.
٣. «الكتاب» تحت «كتب» يشهد له الثلاثة: سطرُ العين بعينه («والكتاب والكتابة مصدر كتبت»)،
   ونصُّ ابن فارس، ومدخلُ اللسان — بقراءةٍ هنا لا بالأداة.
٤. حكمُ القاعدة على جذورٍ مكتوبةٍ هنا باليد من جمل ابن فارس الأولى، ومنها ما أخطأته قاعدةٌ سابقة.
٥. اتّساقُ مولَّدَين: الأعدادُ في `NaqlData.lean` تُعاد من `shuhud.tsv.gz` و`usul.tsv` (مرآةٌ لا شاهد).
الطفرات: `MUTANT_ISNAD_IGNORED`، `MUTANT_ATF_IGNORED`، `MUTANT_FIRST_SENTENCE_ONLY`.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "formal" / "a116" / "A116"
LISAN = (ROOT / "corpora" / "lisan"
         / "0711IbnManzurIfriqi.LisanCarab.Shamela0001687-ara1.mARkdown.gz")
AYN = ROOT / "corpora" / "kitab" / "0170KhalilFarahidi.Cayn.JK000930-ara1.gz"
J3 = ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz"
NAQL = ROOT / "corpora" / "naql"
MARKS = re.compile(r"[ً-ْٰـ]")
LEAN_NAMES = ("mafhum_bishahid", "maluma_tahmil", "bila_shahid_iff", "ghayr_maqbul_la_yughayyir",
              "aql_la_yashhad", "wahid_yakfi", "qati_bi_tawatur", "kathra_la_tuwatir",
              "marja_la_yashhad", "hiss_yakfi", "naql_la_yashhad_lilmusamma", "taadud",
              "naql_an_wahid", "mustaqill_yazid", "iqtiran_mithal", "la_takhmin_asl",
              "usul_muhtamal", "mawdu_count", "shawahid_mafhum", "kataba", "kitab_hukm")


def sealed(path: Path, sha: str) -> list[str]:
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").splitlines()


def shuhud() -> list[list[str]]:
    text = gzip.decompress((NAQL / "shuhud.tsv.gz").read_bytes()).decode("utf-8")
    return [ln.split("\t") for ln in text.splitlines()]


def usul() -> dict[str, list[str]]:
    rows = (NAQL / "usul.tsv").read_text(encoding="utf-8").splitlines()
    return {r.split("\t")[0]: r.split("\t") for r in rows}


def lean_value(name: str) -> str:
    src = (A / "NaqlData.lean").read_text(encoding="utf-8")
    m = re.search(rf"def {name} : [^:=]+ := (.+)", src)
    assert m is not None, name
    return m.group(1)


def test_lisan_seal() -> None:
    raw = gzip.decompress(LISAN.read_bytes())
    assert len(raw) == 30670791
    assert hashlib.sha256(raw).hexdigest() == (
        "34fa56710a5b701532a34cb70f8fe440b261e80ae3c40d9667d18b65be7ed86d")
    lines = raw.decode("utf-8").splitlines()
    assert lines[23988].startswith("### $ كتب: الكتاب: معروف")
    manifest = (ROOT / "corpora" / "lisan" / "MANIFEST.tsv").read_text(encoding="utf-8")
    assert "056df249d6619b428a78f1d69a8ab2851b97b0a6" in manifest
    assert "\tمختوم\t" in manifest  # بإذن المالك 2026-10-18 «اختم» (ADR ١٠٤)


def test_constitution_amendment() -> None:
    """المادّتان ١٥ و١٦ معدَّلتان بنصّ المالك (ADR ١٠٤)، ومفهومُ الوضع برتبة شهادته في Lean."""
    c = " ".join((ROOT / "AGENT_CONSTITUTION.md").read_text(encoding="utf-8").split())
    for q in ("النقل عن الوضع ليس بالضرورة تويتر",
              "نقبلها شاهد برتبة الشهادة فليس كل رتبة تشترط التواتر"
              " وليس المطلوب التواتر لكل لفظ وضع لمعنى"):
        assert q in c
    src = (A / "Naql.lean").read_text(encoding="utf-8")
    assert "theorem wahid_yakfi" in src and "theorem marja_la_yashhad" in src


def test_nabhani_anchors() -> None:
    j3 = sealed(J3, "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e")
    line = j3[366]
    for q in ("اللغة العربية اصطلاح اصطلح عليه العرب",
              "فإذا قالوا هم إن لفظ كذا موضوع لمعنى كذا", "فيقبل قولهم، ويسلم به",
              "ومن هنا كانت طريق معرفة اللغة العربية هي النقل المتواتر وخبر الآحاد",
              "كالألفاظ المروية المعنعنة عن الأدباء الباحثين عن اللغة، كالخليل",
              "فالنقل المتواتر هو ما كان معلوماً بحيث لا يتشكك فيه مع التشكيك",
              "وأما العقل فلا ينفع في معرفة اللغة العربية، ولا قيمة له"):
        assert q in line
        assert q in (A / "Naql.lean").read_text(encoding="utf-8")


def test_kitab_three_witnesses() -> None:
    ayn = sealed(AYN, "e809c626239dee34bddd688b4382a8e314a559a0c700831b8b747fb01ed7d8a1")
    assert ayn[30473] == "# كتب" and ayn[30480] == "# والكتاب والكتابة مصدر كتبت"
    with (ROOT / "maqayis_by_root_csv_999.csv").open(encoding="utf-8") as f:
        body = next(r["body_text"] for r in csv.DictReader(f) if r["root_full"] == "كتب")
    assert "الكتاب" in MARKS.sub("", body)
    lisan = gzip.decompress(LISAN.read_bytes()).decode("utf-8").splitlines()
    assert lisan[23988].startswith("### $ كتب:")
    row = next(r for r in shuhud() if r[0] == "كتب" and r[1] == "الكتاب")
    # MUTANT_ATF_IGNORED يقتله هذا: سطرُ العين «والكتاب» لا يصير «الكتاب» إلّا بحذف الواو
    assert row[2] == "kfm" and row[3] == "ibn-faris,ibn-manzur,khalil"
    # سطورُ الشهود في Lean: أوّلُ سطرٍ بعد رأس العين، ورأسُ اللسان، ورقمُ مدخل المقاييس
    data = (A / "NaqlData.lean").read_text(encoding="utf-8")
    assert ('("k", "khalil", 30475), ("f", "ibn-faris", 3334), ("m", "ibn-manzur", 23989)'
            in data)


def test_ibn_faris_hukm() -> None:
    u = usul()
    expected = {"كتب": ("wahid", "1"), "عمر": ("usul", "2"), "جدو": ("usul", "5"),
                "ضرك": ("kalima", "1"), "هلج": ("laysa", "0"), "حبس": ("laHukm", "0"),
                "همع": ("wahid", "1"),
                # «أصل واحد … ثلاث لغات»، «ليست أصلًا»، «أصول متباينة»، «أصل صحيح … ليس»
                "سقم": ("wahid", "1"), "ءجص": ("laysa", "0"), "ءكد": ("laysa", "0"),
                "خرص": ("usul", "2"), "صهل": ("wahid", "1")}
    for root, (h, n) in expected.items():
        # MUTANT_FIRST_SENTENCE_ONLY يقتله توقّعُ «همع»: جملتُه الأولى أسماءُ الحروف وحدَها
        assert (u[root][1], u[root][2]) == (h, n), root
    assert MARKS.sub("", u["كتب"][3]) == "الكاف والتاء والباء أصل صحيح واحد يدل على جمع شيء إلى شيء"
    assert MARKS.sub("", u["همع"][3]).split(".")[0] == "الهاء والميم والعين"
    # «أصلٌ صحيح يدلّ على … وعلى …» أصلٌ واحدٌ بلفظ ابن فارس
    assert u["صحح"][1] == "wahid" and "وعلى" in MARKS.sub("", u["صحح"][3])


def test_deposit_counts() -> None:
    rows = shuhud()
    assert lean_value("zawjCount") == str(len(rows))
    by_w = [sum(1 for r in rows if len(r[3].split(",")) == n) for n in (1, 2, 3)]
    by_d = [sum(1 for r in rows if len(r[2]) == n) for n in (1, 2, 3)]
    assert lean_value("biShuhud") == str(by_w) and lean_value("biMaajim") == str(by_d)
    reduced = sum(1 for r in rows if len(r[3].split(",")) < len(r[2]))
    assert lean_value("naqlAnWahid") == str(reduced) and reduced > 0
    # MUTANT_ISNAD_IGNORED: لو كان الشاهدُ المعجمَ لا القائل لما نقص شاهدٌ عن معجمه
    assert any(len(r[3].split(",")) < len(r[2]) for r in rows)
    u = usul()
    assert lean_value("jidhrCount") == str(len(u))
    classes = ("wahid", "usul", "kalima", "laysa", "laHukm")
    cls = [sum(1 for r in u.values() if r[1] == c) for c in classes]
    assert lean_value("hukmAsl") == str(cls)


def test_lean_names() -> None:
    src = (A / "Naql.lean").read_text(encoding="utf-8")
    # CONCEPT_WITHOUT_WITNESS (المادّة ١٦): مُنشئُ المفهوم يحمل شاهدًا بالنوع
    assert re.search(r"\| mafhum \(r : Rutba\) \(s : Shahada\) \(ss : List Shahada\)", src)
    assert all(f"theorem {n}" in src for n in LEAN_NAMES)
    audit = (ROOT / "formal" / "a116" / "Audit.lean").read_text(encoding="utf-8")
    assert all(f"A116.Naql.{n}" in audit for n in LEAN_NAMES)
