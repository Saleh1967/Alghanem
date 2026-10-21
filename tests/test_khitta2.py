"""الخطّةُ الثانية مودَعةً بلفظها (STEP-0014، ADR ١٢٠).

* **الختم:** النصُّ بين العلامتين بصمتُه مكتوبةٌ هنا باليد عند الإيداع.
  وهذا ختمٌ بعد الإيداع لا مطابقة، كما في `khitta.md`.
* **المراسي شاهدٌ مستقلّ:**
  * كلُّ اقتباسٍ بين «» في النصّ إمّا اصطلاحٌ من قائمةٍ مغلقة،
    وإمّا مرسًى بسطره من «التفكير» المختوم، وتقع أجزاؤه فيه بترتيبها.
  * والإزاحةُ سطرًا قبلُ أو بعدُ تُرفض لكلّ مرساة.
* **ج3:** ما تُسند إليه الخطّةُ وADR ١٢٠ من ج3 المختوم
  (س1071، س1073، س1074، س1076) في أسطره.
* **قولا المالك:** بلفظهما في الرأس.
  وهذا ختمٌ للنقل لا شاهدٌ على القول، لأنّ سجلّ الجلسة ليس في المستودع.
"""

from __future__ import annotations

import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KHITTA = (ROOT / "docs" / "protocol" / "khitta-2.md").read_text(encoding="utf-8")
ADR = (ROOT / "docs" / "adr" / "0120-khitta-2.md").read_text(encoding="utf-8")
SHA = "0dd951cc95f98ddd57df2977f3ede16d5a54bced0255d029db591352ae8bd828"


def sealed(name: str) -> list[str]:
    path = ROOT / "corpora" / "nabhani" / name
    return gzip.open(path, "rt", encoding="utf-8").read().splitlines()


TAFKIR = sealed("tafkir.txt.gz")
J3 = sealed("shakhsiyya_j3.txt.gz")
OWNER = (
    "انت لم تفهم الهدف الاستراتيجي هذا فيه منهج للوصول للهدف افم الهدف وانت خبير خوارزميات واقترح"
    " خطة للتطوير",
    "Mashru يبقى منفصل تماما ولا يسمح ان تكتب به شيء يبقى الباقي فهو لك وابني خطة\n  ووظف اي قدرات"
    " للوصول للهدف وانا موافق",
)
# اصطلاحاتٌ بين «» ليست نقلًا: مراتبُ المخرج، وأوسامُ الدستور، واسمُ خطّة Mashru، ولفظُ ADR ١١٨،
# ولفظةٌ من س1071 تُفحص في test_j3_anchors.
LABELS = {"مفهوم", "معلومة", "لا حكم", "من حيث هي", "تقدير على عيّنة", "الجبر يقود", "مطلقاً",
          "أسلوبَ", "مفحوص", "المقيسُ", "الخطوةَ التالية"}
QUOTE = re.compile(r"«([^«»]+)»(?:\s*\(|،\s*)س(\d+)\)")


def block() -> str:
    a = "<!-- نصّ الخطّة الثانية: بدء -->\n"
    b = "<!-- نصّ الخطّة الثانية: نهاية -->"
    return KHITTA[KHITTA.index(a) + len(a):KHITTA.index(b)]


def test_block_sealed() -> None:
    assert hashlib.sha256(block().encode("utf-8")).hexdigest() == SHA


def test_owner_words() -> None:
    head = KHITTA[:KHITTA.index("<!-- نصّ الخطّة الثانية: بدء -->")]
    for w in OWNER:
        assert f"«{w}»" in head, w[:20]


def in_line(q: str, n: int) -> bool:
    if not 1 <= n <= len(TAFKIR):
        return False
    line, at = TAFKIR[n - 1], 0
    for part in (p.strip(" .،") for p in q.split("…")):
        if not part:
            continue
        at = line.find(part, at)
        if at < 0:
            return False
        at += len(part)
    return True


def test_every_quote_anchored_or_label() -> None:
    anchored = {q for q, _ in QUOTE.findall(block())}
    for q in re.findall(r"«([^«»]+)»", block()):
        assert q in LABELS or q in anchored, q[:30]


def test_tafkir_quotes_in_their_lines() -> None:
    found = [(q, int(n)) for q, n in QUOTE.findall(block())]
    assert len(found) >= 5
    for q, n in found:
        assert in_line(q, n), (n, q[:30])


def test_shifted_lines_refused() -> None:
    """ضبطٌ سالب لكلّ مرساة: السطرُ قبلها وبعدها لا يقبلان الاقتباس."""
    for q, n in ((q, int(n)) for q, n in QUOTE.findall(block())):
        assert not in_line(q, n - 1) and not in_line(q, n + 1), (n, q[:30])


def test_order_matters() -> None:
    """ضبطٌ سالب: قلبُ جزأي اقتباسٍ محذوفٍ وسطُه يُرفض."""
    assert in_line("مرئية … ممكنة التحقيق", 92)
    assert not in_line("ممكنة التحقيق … مرئية", 92)


# كلُّ سطرٍ من ج3 تُسند إليه الخطّةُ أو ADR ١٢٠، ولفظُه المطلوب فيه (مكتوبٌ باليد من النصّ المختوم).
J3_LINES = {
    1071: "فلا تعادل بين الأدلة مطلقاً",
    1073: "والترجيح يختص بالأدلة الظنية",
    1074: "إعمال الدليلين أولى",
    1076: "يرجح الخاص على العام",
}
J3_REF = re.compile(r"ج3 س(\d+)(?:–(\d+))?")


def j3_refs(text: str) -> set[int]:
    out: set[int] = set()
    for a, b in J3_REF.findall(text):
        out.update(range(int(a), int(b or a) + 1))
    return out


def test_j3_anchors() -> None:
    for n, phrase in J3_LINES.items():
        assert phrase in J3[n - 1], n
    refs = j3_refs(block()) | j3_refs(ADR)
    assert refs and refs <= set(J3_LINES), sorted(refs - set(J3_LINES))
    assert "«يرجح الخاص على العام»" in ADR


def test_j3_shift_refused() -> None:
    """ضبطٌ سالب: مرجعٌ مُزاح (س1075–1076) يخرج عن الأسطر المفحوصة."""
    assert not j3_refs("ج3 س1075–1076") <= set(J3_LINES)


def share(path: str, *keys: str) -> float:
    import json
    d = json.loads((ROOT / path).read_text(encoding="utf-8"))
    for k in keys:
        d = d[k]
    return float(d)


def test_baselines_from_results() -> None:
    plan = block()
    pairs = {
        "21.56٪": share("docs/qism-khanat/result-5.json", "D3", "muayyan_share"),
        "99.95٪": share("docs/qism-khanat/result-5.json", "D3", "precision"),
        "98.16٪": share("docs/silsila/result-2.json", "qac_even_surahs", "A_haml", "precision"),
        "92.01٪": share("docs/silsila/result-2.json", "qac_even_surahs", "B_sigha", "precision"),
    }
    for text, value in pairs.items():
        assert text in plan, text
        assert f"{100 * value:.2f}٪" == text, (text, value)


def test_targets_agree() -> None:
    for t in ("40٪", "99.9٪"):
        assert t in block() and t in ADR, t
    assert "99.5٪" not in block() and "99.5٪" not in ADR


def test_phases() -> None:
    plan = block()
    status = KHITTA[KHITTA.index("## حالُ كلّ مرحلة"):]
    for k in "٠١٢٣٤٥٦":
        assert f"\n| م{k} |" in plan, k
        assert f"\n| م{k} |" in status, k
    assert "مهمّةٌ واحدة لكلّ جلسة** (م١٩)" in plan
