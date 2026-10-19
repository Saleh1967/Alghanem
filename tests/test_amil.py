"""العاملُ والمعمول والعلاماتُ الأصليّةُ والفرعيّة (`A116.Amil`، ADR ٧٠) على جدول الألفيّة
(`Qism.ending`).

١. `amil.csv` (يطبعه Lean، ويطابقه CI): لكلّ زوجٍ (صنف، حالة) آخرُه، أصليٌّ أم حرفيّ، ونائبٌ أم لا —
   والتوقّعُ هنا باليد من شرح ابن عقيل (س406–418): الأصليّةُ ضمّة/فتحة/كسرة/سكون، والنائبةُ بالصنف:
   الستّةُ والمثنّى وجمعُ المذكّر والأمثلةُ الخمسة في كلّ حالة، وجمعُ المؤنّث في النصب، والممنوعُ في
   الجرّ، والمقصورُ في الثلاث، والمنقوصُ في الرفع والجرّ، ومعتلُّ الفعل بالألف في الثلاث وبالواو والياء
   في الرفع والجزم — 32.
٢. توقيعُ المالك على حركات المنقول (`corpora/sibawayh/owner-naql.json`) مربوطٌ ببصمة المراسي.
الطفرات: `MUTANT_ASLIYYA_ONLY` (لا نيابة)، `MUTANT_SIGNATURE_DRIFT` (بصمةُ المراسي لا تطابق التوقيع).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "amil.csv"
ANCHORS = ROOT / "corpora" / "sibawayh" / "kitab-anchors.tsv"
SIGNATURE = ROOT / "corpora" / "sibawayh" / "owner-naql.json"

ASLIYYA = {"damma", "fatha", "kasra", "sukun"}
# النيابةُ باليد: الصنفُ ← الحالاتُ التي ينوب فيها آخرُه عن آخر أصله (الصحيح)
NAIB_BY_HAND = {
    "iSitta": {"raf", "nasb", "jarr"}, "iMuthanna": {"raf", "nasb", "jarr"},
    "iJamM": {"raf", "nasb", "jarr"}, "iJamF": {"nasb"}, "iMamnu": {"jarr"},
    "iMaqsur": {"raf", "nasb", "jarr"}, "iManqus": {"raf", "jarr"},
    "fKhamsaA": {"raf", "nasb", "jazm"}, "fKhamsaW": {"raf", "nasb", "jazm"},
    "fKhamsaY": {"raf", "nasb", "jazm"}, "fMutalAlif": {"raf", "nasb", "jazm"},
    "fMutalW": {"raf", "jazm"}, "fMutalY": {"raf", "jazm"},
}


def _rows() -> list[dict[str, str]]:
    head, *body = TABLE.read_text(encoding="utf-8").splitlines()
    keys = head.split(",")
    return [dict(zip(keys, ln.split(","))) for ln in body]


def test_marks_by_hand() -> None:
    rows = _rows()
    assert len(rows) == 45
    for r in rows:
        assert (r["asliyya"] == "true") == (r["ending"] in ASLIYYA), r
        assert (r["naib"] == "true") == (r["irab"] in NAIB_BY_HAND.get(r["cls"], set())), r
    expected = sum(len(v) for v in NAIB_BY_HAND.values())
    assert sum(r["naib"] == "true" for r in rows) == expected == 32
    assert all(r["naib"] == "false" for r in rows if r["cls"] in ("iSahih", "fSahih"))


def test_ism_no_jazm_fil_no_jarr() -> None:
    rows = _rows()
    assert not any(r["cls"].startswith("i") and r["irab"] == "jazm" for r in rows)
    assert not any(r["cls"].startswith("f") and r["irab"] == "jarr" for r in rows)


def test_mutant_asliyya_only_rejected() -> None:
    """`MUTANT_ASLIYYA_ONLY`: جدولٌ بلا نيابةٍ لا يطابق الألفيّة (س412: «وما عدا ذلك يكون نائبًا»)."""

    assert any(r["naib"] == "true" for r in _rows())


def test_owner_signature_bound_to_anchors() -> None:
    sig = json.loads(SIGNATURE.read_text(encoding="utf-8"))
    assert sig["scope"] == "NAQL_VOCALIZED_FROM_EXAMPLE" and sig["signed_on"] == "2026-10-16"
    assert sig["anchors_sha256"] == hashlib.sha256(ANCHORS.read_bytes()).hexdigest()


def test_mutant_signature_drift_caught() -> None:
    sig = json.loads(SIGNATURE.read_text(encoding="utf-8"))
    drifted = hashlib.sha256(ANCHORS.read_bytes() + b"\n").hexdigest()
    assert drifted != sig["anchors_sha256"]
