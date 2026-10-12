"""المجالُ المعلَنُ الرابع — معجمُ لين مرجعًا محجوبًا للمصدر والجمع (ADR ٣٣، قرارُ المالك 2026-10-12).

**الواقع.** `An Arabic-English Lexicon` لإدوارد وليم لين (لندن، 1863–1893)، رقمنةُ Perseus
بتصحيحات Alpheios، رخصةُ CC BY-SA 3.0 US (`corpora/lane/LICENSE.md`)، مثبَّتةً عند
`alpheios-project/lan@7dd04e1`. ملفّاتُ TEI الثمانيةُ والثلاثون في `corpora/lane/tei/` مضغوطةً
بلا طابع زمن، وبصمةُ كلٍّ منها بعد فكّ الضغط في `LANE_SOURCES` — الختم. العربيّةُ فيها
بالحرف العربيّ مشكولةً بيد لين.

**المدوّنةُ المختومة** (`lines`): كلُّ وسمٍ عربيّ (`<foreign lang="ar">`، `<orth lang="ar">`) بترتيب
الملفّات ثمّ بترتيب الوثيقة، وسمٌ في سطر — والتحويلُ الوحيد أنّ فواصلَ الأسطر داخلَ الوسم تصير فراغًا.
تُكتب في `corpora/lane/lane-lines.txt.gz` وتُختم بصمتُها في `gate.api.SEALED_CORPORA`
(`LANE_LINES_SHA256`)؛ فكلماتُها تدخل من البوّابة نفسها `Gate(corpus=LANE_CORPUS)` ولا تُقرأ بغيرها.

**السجلّات** (`records`) — الإطارُ المسجَّلُ مسبقًا في `docs/lane/PREREG.md`:

* الجذرُ (`div2 type="root"`) ثلاثةُ أحرفٍ متمايزة ليس فيها حرفُ علّةٍ ولا همزة (`WEAK`).
* **المصدر**: مدخلٌ `itype` = 1، مفتاحُه كلمةٌ واحدة حروفُها بعد نزع «هُ» الأخيرة هي الجذرُ بعينه؛
  والتعديةُ = وجودُ «هُ» (علامةُ لين نفسِه: كَتَبَهُ)؛ والمصادرُ وسومٌ عربيّةٌ متتاليةٌ بعد أوّل علامة
  «inf. n.»/«inf. ns.» في المدخل يليها وسم، لا يفصلها إلّا فاصلٌ مسمًّى (`SEP`) وتقطعها الإحالةُ (↓)،
  وكلٌّ منها كلمةٌ واحدةٌ آخرُها رفعٌ (ٌ أو ُ) أو ألفٌ مقصورة (`cited_noun`).
* **الجمع**: مدخلٌ بلا `itype`، مفتاحُه كلمةٌ واحدةٌ حروفُها الجذرُ أو الجذرُ وتاءٌ مربوطة؛ والجموعُ
  كذلك بعد أوّل «pl.» (لا «pl. pl.») يليها وسم.
* ملفّا حرف الكاف (`DEV_FILES`) استُعملا لبناء الاستخراج فهما **خارجَ القياس**؛ وجذورُ الأمثلة كذلك.

**القياس** (`measure`): كلُّ كلمةٍ تدخل `Gate(corpus=LANE_CORPUS, domain=…)` ابتداءً واستمرارًا؛
والوزنُ من ذرّات الشهادة (`pattern`): الأصولُ بترتيبها أرقامًا، وحركةُ الإعراب الأخيرة ونونُ التنوين
محذوفتان. والمتنبّئُ من الألفية بأمثلة شرح ابن عقيل (`MASDAR_RULES`، `PLURAL_RULES`)، **ووزنُ كلّ
قاعدةٍ وزنُ مثالها كما شكله لين** — لا حركةَ من الذاكرة. والنتيجةُ `docs/lane/result.json`.

`--check` يُسقط البناءَ بأسمائها: `LANE_SOURCE_DRIFTED` (بصمةُ مصدر)، `LANE_LINES_DRIFTED`،
`LANE_NOT_SEALED` (بصمةُ السطور غيرُ المسجَّلة في البوّابة)، `LANE_RECORDS_DRIFTED`،
`LANE_RESULT_DRIFTED`. الأداةُ معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from collections.abc import Callable, Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LANE = ROOT / "corpora" / "lane"
TEI = LANE / "tei"
LINES = LANE / "lane-lines.txt.gz"
MASDAR_TSV = LANE / "lane-masdar.tsv"
PLURAL_TSV = LANE / "lane-plural.tsv"
RESULT = ROOT / "docs" / "lane" / "result.json"
LANE_COMMIT = "7dd04e1182c13a4b0883978867d2a3b04616542a"
LANE_SOURCES: dict[str, str] = {
    "u$0.xml": "8cbb5c01e8a371a214fa305ad40b94137878c77e114a2dae0e7c5683f375f3c6",
    "u_0.xml": "9e889c4d3611bfba5e2ae8b5c46719f8d1ec83c32b337f677e4c64bf575d512c",
    "u_A0.xml": "28cec30dc2576a63a079b65d97d15fe117ed6133a4c097e6e7e7327cd6d424bf",
    "u_D0.xml": "3559d0b3b1a0405299512f06cd389e8a0b89da192d3c6818a5050aec1c0ed738",
    "u_E0.xml": "c7b38ba89561b5fa998faaa617730530a9e78da1f32c8c0174fe80806cfee516",
    "u_H0.xml": "fa7c008e2a4bcae8603d0efb8f93b2c542334b7f430a4abaf427156a4bba191a",
    "u_S0.xml": "f46740c25bdc88db360cd72ae5e8491532cb8413e960e75b6e556d34ba25cb5b",
    "u_T0.xml": "7325116775e2d04b86271d14ddc1df8383cfeb6f37ca9f78786d302439324de5",
    "u_Y0.xml": "0bb7228f544aeee98f91081955bf17d23c242923a4f37bc0e124a01de8744e75",
    "u_Y1.xml": "ebcfaad3805f65851a70b1b2678e088695dd68a9e5c9c050cf3afa5091077216",
    "u_Z0.xml": "3f5e419aebf8f8a3330133c519c062a7ba46610a33b6d9043b00df3c5618f959",
    "ua0.xml": "9c5fd3465d8795d675f64f369c989383c48264ab96b5c7921f9d0d3ef75dc61a",
    "ub0.xml": "57beb1d97ada6343d35c9973def8aa5fe3f5009fd1b1116c4b81efe9d20ac65b",
    "ud0.xml": "7bfea62cb42b36900c867ee888f589d3db3fa51c646af19e124d0f0a301c877c",
    "uf0.xml": "8e997f398af3f70c43d37d4d0b83c9195e2ea27139a0413675b38f06137852c5",
    "ug0.xml": "b48d99dd3798580fc4cf8e6dc463bf2e2b58b097d3bac5510d5038955865cb89",
    "uh0.xml": "170ef496f55bde9bd9502106b65276b2727f60c1a527d6dc9170035dd51f6b02",
    "uh1.xml": "c41ace2f48abcb19193ad863a666fd47a8df56fcfae8973b96b8acc067701e34",
    "uj0.xml": "839540b4b502659ff473fc08c01b28533600d1e3fb113602b33e3a7cf7d94157",
    "uk0.xml": "b7d3f3d7a91f0ac6dd5e7726d455075119c4cbb37f4b9a6e74ef08a33a2d432b",
    "uk1.xml": "c0fb537772f25fa34aa6edc33fb70975ea145bb5bfa6a6636b6cd331bd9c27b6",
    "ul0.xml": "a5b3b91df2ca805cc3167e2746d64a53992814990b2a36d4f2c5b95f62d9ef55",
    "ul1.xml": "c5e7fe78251a82fd549d77ea128118e31b1242937296f467e728f2efa11e4662",
    "um0.xml": "c6355f3bf54b24091f0a38e7b253d1fbbf0d875965ff0772e2746afcee534c77",
    "um1.xml": "e749bf1ce708174bba6ce671197db72f52b4b77896a1fd25e739e8433df2c420",
    "un0.xml": "fe8cfa4ebde9bd7d251f29fe43d572d76b02a6bfb1742e93bc18bd53a2bc87c0",
    "un1.xml": "d5de6d9cc3094e32131d3f7e5aa94a2fc806c6d63ec1ad5aeea6ab0ab7cff17f",
    "uq0.xml": "50fa31d6bc8a1e2e23f1303d5117d431c08b3eb8ae16364991d7e25ec9922a47",
    "uq1.xml": "09127783c4de4ca9fae079e24cc46b5756b0e9498a5504604070b3ed54bb3e73",
    "uq2.xml": "dcbd9e794ae92fe681ec3c9b1eaa75cb864423a4376347497b20f4e8ffb73c3c",
    "ur0.xml": "4a43634c26f130b4030fe88cde234f0daa069dddb3650332c97a917b6d1c2b03",
    "us0.xml": "f13525d5f460d1ca7bd5148e213befff91560074313c403ff181c695996ef946",
    "ut0.xml": "678eeb2947fbab3653f7ab6e507cff3a1952c1f2048a6d83798a571525cb088e",
    "uv0.xml": "788a195ccfb9ccea8d88798157ccce6c8de8a8d366107991240d93c905104dbb",
    "uw0.xml": "1bca47d7544b4285d196e24fbb4076fa252a871cc7b1b26f0129fbed84b6f8fa",
    "uw1.xml": "fd962b520f33038f716dd115d3b143c9297e4205b0f0db03249895122a0f156d",
    "ux0.xml": "057371e17e4c5aee95c234056bff8a7afe91324be60eeedc1d3658093917ec77",
    "uz0.xml": "acadfc18b189c7d0acf68d25ca07664aabf67c15017eccaac0d05c18dd861259",
}
"""بصمةُ كلّ ملفّ TEI بعد فكّ الضغط — الختم."""

DEV_FILES = ("uk0.xml", "uk1.xml")
"""ملفّا الكاف: عليهما بُني الاستخراج، فهما خارجَ القياس (PREREG §٣)."""

WEAK = frozenset("اأإآءؤئويىٱ")
HARAKAT = frozenset("ًٌٍَُِّْٰ")
TANWIN = frozenset("ًٌٍ")
SEP = re.compile(r"^(?:[\s,;:.]|\([^()]*\)|\[[^\[\]]*\]|\b(?:and|or|also|is|are)\b|↓)*$")
"""الفاصلُ المسمّى بين العلامة والوسم وبين وسمين متتاليين: فراغ، ترقيم، مرجعٌ بين قوسين، تعليقٌ
بين معقوفين، and/or/also/is/are، ↓."""
INF = re.compile(r"\binf\. ns?\.")
PL = re.compile(r"(?<!pl\. )\bpl\.(?! pl\.)")
"""«pl.» لا «pl. pl.» (جمعُ الجمع)."""
PRONOUN = "هُ"

# --- القواعد: الألفية بأمثلة شرح ابن عقيل --------------------------------------------------------
# (OpenITI/0775AH@61b0c789، 0769IbnCaqilBahaDinMisri.SharhCalaAlfiyya.Shamela0009904-ara1،
#  sha256 661e43ea…471f09)
MASDAR_RULES: tuple[tuple[str, str, str], ...] = (
    # «فعل قياس مصدر المعدى من ذي ثلاثة» — «ردّ ردًّا وضرب ضربًا وفهم فهمًا»
    ("transitive", "ضرب", "ضرب"), ("transitive", "فهم", "فهم"),
    # «وفعل اللازم بابه فعل» — «كفرح فرحًا»
    ("intransitive_i", "فرح", "فرح"),
    # «وفعل اللازم مثل قعدا له فعول» — «قعد قعودًا … وبكر بكورًا»
    ("intransitive_a", "قعد", "قعود"), ("intransitive_a", "بكر", "بكور"),
    # «فعولة فعالة لفعلا» — «سهل سهولة وصعب صعوبة وعذب عذوبة … جزل جزالة وفصح فصاحة وضخم ضخامة»
    ("u", "سهل", "سهولة"), ("u", "صعب", "صعوبة"), ("u", "عذب", "عذوبة"), ("u", "جزل", "جزالة"),
    ("u", "فصح", "فصاحة"), ("u", "ضخم", "ضخامة"),
)
"""(الصنف، جذرُ المثال، حروفُ مصدره): الوزنُ المتوقَّع للصنف وزنُ ذلك المصدر كما شكله لين في مدخل
المثال (`itype` 1)، بشرط أن يكون فعلُ المثال عند لين من الصنف نفسِه (`verb_class`)."""

PLURAL_RULES: tuple[tuple[str, str], ...] = (
    # «لفعل اسما صح عينا أفعل» — «كلب وأكلب»
    ("كلب", "أكلب"),
    # «وغير ما أفعل فيه مطرد من الثلاثي اسما بأفعال يرد» — «جمل وأجمال وعضد وأعضاد وحمل وأحمال
    # وعنب وأعناب … وقفل وأقفال»؛ «وأما فعل فجاء بعضه على أفعال كرطب وأرطاب»
    ("جمل", "أجمال"), ("عضد", "أعضاد"), ("حمل", "أحمال"), ("عنب", "أعناب"), ("قفل", "أقفال"),
    ("رطب", "أرطاب"),
    # «والغالب مجيئه على فعلان كصرد وصردان ونغر ونغران»
    ("صرد", "صردان"), ("نغر", "نغران"),
    # «ولفعلة فعل» — «كقربة وقرب وغرفة وغرف»؛ «لاسم على فعلة نحو كسرة وكسر»
    ("قربة", "قرب"), ("غرفة", "غرف"), ("كسرة", "كسر"),
    # «لفعل اسما صح لاما فعلة» — «قرط وقرطة ودرج ودرجة»
    ("قرط", "قرطة"), ("درج", "درجة"),
    # «فعل وفعلة فعال لهما» — «كعب وكعاب … وقصعة وقصاع … صعب وصعاب»؛ «وفعل أيضا له فعال» — «جبل
    # وجبال وجمل وجمال ورقبة ورقاب وثمرة وثمار … ورمح ورماح»
    ("كعب", "كعاب"), ("قصعة", "قصاع"), ("صعب", "صعاب"), ("جبل", "جبال"), ("جمل", "جمال"),
    ("رقبة", "رقاب"), ("ثمرة", "ثمار"), ("رمح", "رماح"),
    # «وبفعول فعل نحو كبد» — «كبد وكبود»؛ «كعب وكعوب وفلس وفلوس … حمل وحمول وضرس وضروس … جند
    # وجنود وبرد وبرود»
    ("كبد", "كبود"), ("كعب", "كعوب"), ("فلس", "فلوس"), ("حمل", "حمول"), ("ضرس", "ضروس"),
    ("جند", "جنود"), ("برد", "برود"),
    # «وفعلا اسما وفعيلا وفعل غير معل العين فعلان شمل» — «ظهر وظهران وبطن وبطنان … ذكر وذكران
    # وحمل وحملان»
    ("ظهر", "ظهران"), ("بطن", "بطنان"), ("ذكر", "ذكران"), ("حمل", "حملان"),
)
"""(المفرد، الجمع) بحروفهما من أمثلة ابن عقيل لجذورٍ صحيحة: القاعدةُ وزنُ المفرد كما شكله لين ← وزنُ
الجمع كما شكله لين، لكلّ مدخلٍ في جذر المثال حروفُ مفتاحه حروفُ المفرد ويذكر جمعًا حروفُه حروفُ الجمع.
ولأنّ الأمثلةَ بحروفها (المصدرُ غيرُ مشكول) فقد يقع المثالُ على تشكيلٍ آخرَ عند لين (قِرْبَة لا قُرْبَة)
— يُسمّى في النتيجة ولا يُصحَّح باليد."""


def letters(w: str) -> str:
    return "".join(c for c in w if c not in HARAKAT and c != "ـ")


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def source(name: str) -> bytes:
    raw = gzip.decompress((TEI / (name + ".gz")).read_bytes())
    if sha(raw) != LANE_SOURCES[name]:
        raise SystemExit(f"LANE_SOURCE_DRIFTED:{name}:{sha(raw)}")
    return raw


def parse(name: str) -> ET.Element:
    return ET.fromstring(source(name))


# --- المدوّنة المختومة -------------------------------------------------------------------------


def lines() -> list[str]:
    out: list[str] = []
    for name in sorted(LANE_SOURCES):
        for el in parse(name).iter():
            if el.tag in ("foreign", "orth") and el.get("lang") == "ar":
                text = "".join(el.itertext()).replace("\r", " ").replace("\n", " ")
                if text.strip():
                    out.append(text)
    return out


def render(text: list[str]) -> bytes:
    return ("\n".join(text) + "\n").encode("utf-8")


def gz(blob: bytes) -> bytes:
    return gzip.compress(blob, compresslevel=9, mtime=0)


# --- السجلّات ----------------------------------------------------------------------------------

Token = tuple[str, str]


def stream(entry: ET.Element) -> list[Token]:
    """المدخلُ رموزًا: ('t', نصّ) | ('ar', وسمٌ عربيّ) | ('arrow', إحالةٌ ↓ إلى صيغةٍ أخرى) | ('ms',
    '')."""

    out: list[Token] = []

    def walk(e: ET.Element) -> None:
        if e.tag == "milestone":
            out.append(("ms", ""))
        elif e.tag in ("foreign", "orth") and e.get("lang") == "ar":
            kind = "arrow" if e.get("type") == "arrow" else "ar"
            out.append((kind, "".join(e.itertext())))
        else:
            if e.text:
                out.append(("t", e.text))
            for c in e:
                walk(c)
                if c.tail:
                    out.append(("t", c.tail))

    walk(entry)
    return out


def spans_after(tokens: list[Token], marker: re.Pattern[str]) -> list[str]:
    """الوسومُ العربيّةُ المتتاليةُ بعد علامةٍ في المدخل لا يفصلها إلّا `SEP`، من أوّل علامةٍ يليها
    وسم؛
    والإحالةُ (↓) وغيرُ الفاصل يقطعانها."""

    for i, (kind, text) in enumerate(tokens):
        if kind != "t":
            continue
        for m in marker.finditer(text):
            out: list[str] = []
            sep = text[m.end():]
            for k2, t2 in tokens[i + 1:]:
                if k2 == "t":
                    sep += t2
                    continue
                if k2 != "ar" or not SEP.match(sep):
                    break
                out.append(t2)
                sep = ""
            if out:
                return out
    return []


def cited_noun(w: str) -> bool:
    """كلمةٌ واحدةٌ مذكورةٌ اسمًا: آخرُها رفعٌ (ٌ أو ُ) أو ألفٌ مقصورة."""

    w = w.strip()
    if not w or any(c.isspace() for c in w):
        return False
    return w[-1] in ("ٌ", "ُ") or w[-1] == "ى"


def sound_root(head: str) -> bool:
    return len(head) == 3 and len(set(head)) == 3 and not (set(head) & WEAK)


def roots(name: str) -> Iterator[tuple[str, ET.Element]]:
    for d in parse(name).iter("div2"):
        if d.get("type") != "root":
            continue
        h = d.find("head")
        if h is None:
            continue
        yield letters("".join(h.itertext())).strip(), d


def records() -> tuple[list[list[str]], list[list[str]]]:
    masdar: list[list[str]] = []
    plural: list[list[str]] = []
    for name in sorted(LANE_SOURCES):
        for head, d in roots(name):
            if not sound_root(head):
                continue
            for e in d.iter("entryFree"):
                key = (e.get("key") or "").strip()
                if not key or any(c.isspace() for c in key):
                    continue
                it = e.find("form/itype")
                toks = stream(e)
                if it is not None and (it.text or "").strip() == "1":
                    trans = key.endswith(PRONOUN)
                    verb = key[: -len(PRONOUN)] if trans else key
                    if letters(verb) != head:
                        continue
                    ms = [s.strip() for s in spans_after(toks, INF) if cited_noun(s)]
                    if ms:
                        masdar.append([name, e.get("id") or "", head, verb, "1" if trans else "0",
                                       " ".join(ms)])
                elif it is None:
                    if letters(key) not in (head, head + "ة"):
                        continue
                    ps = [s.strip() for s in spans_after(toks, PL) if cited_noun(s)]
                    if ps:
                        plural.append([name, e.get("id") or "", head, key, " ".join(ps)])
    return masdar, plural


def tsv(header: list[str], rows: list[list[str]]) -> bytes:
    return ("\n".join("\t".join(r) for r in [header, *rows]) + "\n").encode("utf-8")


MASDAR_HEADER = ["file", "entry", "root", "verb", "transitive", "masadir"]
PLURAL_HEADER = ["file", "entry", "root", "singular", "plurals"]


def read_tsv(path: Path) -> list[list[str]]:
    rows = [r.split("\t") for r in path.read_text(encoding="utf-8").splitlines()]
    return rows[1:]


# --- الوزنُ من الشهادة -------------------------------------------------------------------------


def pattern(atoms: tuple[str, ...], root: str, surface: str) -> str | None:
    """وزنُ الكلمة من ذرّات شهادتها: الأصولُ بترتيبها 1 2 3، ونونُ التنوين وحركةُ الإعراب الأخيرة
    محذوفتان،
    والتاءُ الأخيرةُ من مربوطةٍ تُكتب ة. لا وزنَ إن لم تقع الأصولُ الثلاثة بترتيبها."""

    seq = list(atoms)
    if surface and surface[-1] in TANWIN and seq and seq[-1] == "نْ":
        seq = seq[:-1]
    if not seq:
        return None
    out: list[str] = []
    k = 0
    for a in seq:
        ch, mark = a[0], a[1:]
        if k < 3 and ch == root[k]:
            out.append(f"{k + 1}{mark}")
            k += 1
        else:
            out.append(a)
    if k != 3:
        return None
    last = out[-1]
    base = last.rstrip("".join(HARAKAT))
    if letters(surface).endswith("ة") and base == "ت":
        base = "ة"
    out[-1] = base
    return " ".join(out)


def wilson(hits: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    z = 1.959963984540054
    p = hits / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (round(mid - half, 4), round(mid + half, 4))


def verb_class(vp: str | None, transitive: str) -> str | None:
    """صنفُ الفعل للمتنبّئ: فَعُلَ (u)، وإلّا المتعدّي بعلامة لين، وإلّا اللازمُ ببابه (i | a)."""

    if vp is None:
        return None
    parts = vp.split()
    if len(parts) != 3 or parts[0] != "1\u064e" or parts[2] != "3":
        return None
    bab = parts[1][1:]
    if bab == "\u064f":
        return "u"
    if transitive == "1":
        return "transitive"
    return {"\u0650": "intransitive_i", "\u064e": "intransitive_a"}.get(bab)


PatFn = Callable[[str, str], "str | None"]
Rows = list[list[str]]


def setup() -> tuple[Rows, Rows, PatFn, Counter[str]]:
    """السجلّاتُ، ودالّةُ الوزن عبر البوّابة على مجال لين المختوم (القاموسُ على كلمات السجلّات
    وحدَها)."""

    from gate.api import LANE_CORPUS, Gate, Refusal, sealed_forms
    from gate.residue import repair

    masdar = read_tsv(MASDAR_TSV)
    plural = read_tsv(PLURAL_TSV)
    words: set[str] = set()
    for r in masdar:
        words.add(r[3])
        words.update(r[5].split())
    for r in plural:
        words.add(r[3])
        words.update(r[4].split())
    sealed = sealed_forms(LANE_CORPUS)
    domain = {repair(w)[0] for w in words} & sealed
    gate = Gate(corpus=LANE_CORPUS, domain=domain)
    refusals: Counter[str] = Counter()
    cache: dict[str, tuple[str, ...] | None] = {}

    def atoms(w: str) -> tuple[str, ...] | None:
        if w not in cache:
            c = gate.enter(w.encode("utf-8"))
            if isinstance(c, Refusal):
                refusals[c.status + ":" + ",".join(c.reasons)] += 1
                cache[w] = None
            else:
                cache[w] = tuple(c.atoms)
        return cache[w]

    def pat(w: str, root: str) -> str | None:
        a = atoms(w)
        return None if a is None else pattern(a, root, w)

    return masdar, plural, pat, refusals


RuleTables = tuple[dict[str, set[str]], list[dict[str, str]], dict[str, set[str]],
                   list[dict[str, str]]]


def rules(masdar: Rows, plural: Rows, pat: PatFn) -> RuleTables:
    """القواعدُ من الأمثلة: أوزانُها كما شكلها لين — تعريفٌ لا نتيجة (PREREG §٤)."""

    by_root: dict[str, list[list[str]]] = {}
    for r in masdar:
        by_root.setdefault(r[2], []).append(r)
    m_rules: dict[str, set[str]] = {}
    m_examples: list[dict[str, str]] = []
    for cls, root, ml in MASDAR_RULES:
        got = None
        for r in by_root.get(root, []):
            if verb_class(pat(r[3], root), r[4]) != cls:
                continue
            for w in r[5].split():
                mp = pat(w, root) if letters(w) == ml else None
                if mp:
                    got = (r[3], w, mp)
                    break
            if got:
                break
        if got is None:
            m_examples.append({"class": cls, "root": root, "masdar": ml, "status": "UNRESOLVED"})
            continue
        m_rules.setdefault(cls, set()).add(got[2])
        m_examples.append({"class": cls, "root": root, "verb": got[0], "masdar": got[1],
                           "pattern": got[2]})
    p_by_root: dict[str, list[list[str]]] = {}
    for r in plural:
        p_by_root.setdefault(r[2], []).append(r)
    p_rules: dict[str, set[str]] = {}
    p_examples: list[dict[str, str]] = []
    for sing, pl in PLURAL_RULES:
        root = sing[:3]
        found = False
        for r in p_by_root.get(root, []):
            if letters(r[3]) != sing:
                continue
            for p in r[4].split():
                if letters(p) != pl:
                    continue
                sp, pp = pat(r[3], root), pat(p, root)
                if sp and pp:
                    p_rules.setdefault(sp, set()).add(pp)
                    p_examples.append({"singular": r[3], "plural": p, "from": sp, "to": pp})
                    found = True
        if not found:
            p_examples.append({"singular": sing, "plural": pl, "status": "UNRESOLVED"})
    return m_rules, m_examples, p_rules, p_examples


def measure() -> dict[str, object]:
    masdar, plural, pat, refusals = setup()
    m_rules, m_examples, p_rules, p_examples = rules(masdar, plural, pat)
    example_roots = ({r for _, r, _ in MASDAR_RULES}
                     | {letters(s)[:3] for s, _ in PLURAL_RULES})

    # ٢. المجتمعُ: خارجَ ملفّات التطوير وجذور الأمثلة
    def in_scope(r: list[str]) -> bool:
        return r[0] not in DEV_FILES and r[2] not in example_roots

    # ٣. المصدر
    m_n = m_any = m_first = 0
    m_base: Counter[str] = Counter()
    m_rows: list[list[str]] = []
    m_excluded: Counter[str] = Counter()
    for r in masdar:
        if not in_scope(r):
            continue
        cls = verb_class(pat(r[3], r[2]), r[4])
        if cls is None:
            m_excluded["VERB_NOT_FACALA_OR_NO_CERTIFICATE"] += 1
            continue
        ps = [p for p in (pat(w, r[2]) for w in r[5].split()) if p]
        if not ps:
            m_excluded["NO_MASDAR_PATTERN"] += 1
            continue
        m_n += 1
        pred = m_rules.get(cls, set())
        m_any += any(p in pred for p in ps)
        m_first += ps[0] in pred
        m_base[ps[0]] += 1
        m_rows.append(ps)
    m_top, m_top_n = m_base.most_common(1)[0] if m_base else ("", 0)
    m_base_any = sum(1 for ps in m_rows if m_top in ps)

    # ٤. الجمع
    p_n = p_any = p_first = 0
    p_base: Counter[str] = Counter()
    p_rows: list[list[str]] = []
    p_excluded: Counter[str] = Counter()
    for r in plural:
        if not in_scope(r):
            continue
        sp = pat(r[3], r[2])
        if sp is None:
            p_excluded["SINGULAR_NO_CERTIFICATE_OR_PATTERN"] += 1
            continue
        ps = [p for p in (pat(w, r[2]) for w in r[4].split()) if p]
        if not ps:
            p_excluded["NO_PLURAL_PATTERN"] += 1
            continue
        p_n += 1
        pred = p_rules.get(sp, set())
        p_any += any(p in pred for p in ps)
        p_first += ps[0] in pred
        p_base[ps[0]] += 1
        p_rows.append(ps)
    p_top, p_top_n = p_base.most_common(1)[0] if p_base else ("", 0)
    p_base_any = sum(1 for ps in p_rows if p_top in ps)

    def share(h: int, n: int) -> dict[str, object]:
        return {"hits": h, "n": n, "rate": round(h / n, 4) if n else None, "ci95": wilson(h, n),
                "transmitted": round(1 - h / n, 4) if n else None}

    return {
        "lines_sha256": sha(render(lines())),
        "masdar": {
            "rules": {k: sorted(v) for k, v in sorted(m_rules.items())},
            "examples": m_examples,
            "excluded": dict(sorted(m_excluded.items())),
            "primary_any": share(m_any, m_n),
            "secondary_first": share(m_first, m_n),
            "baseline_most_frequent": {"pattern": m_top, "first": share(m_top_n, m_n),
                                       "any": share(m_base_any, m_n)},
        },
        "plural": {
            "rules": {k: sorted(v) for k, v in sorted(p_rules.items())},
            "examples": p_examples,
            "excluded": dict(sorted(p_excluded.items())),
            "primary_any": share(p_any, p_n),
            "secondary_first": share(p_first, p_n),
            "baseline_most_frequent": {"pattern": p_top, "first": share(p_top_n, p_n),
                                       "any": share(p_base_any, p_n)},
        },
        "refusals": dict(sorted(refusals.items())),
    }


def dump(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False) + "\n").encode("utf-8")


def main(argv: list[str]) -> int:
    from gate.api import LANE_LINES_SHA256

    check = "--check" in argv
    blob = render(lines())
    digest = sha(blob)
    m, p = records()
    mt, pt = tsv(MASDAR_HEADER, m), tsv(PLURAL_HEADER, p)
    if check:
        if gzip.decompress(LINES.read_bytes()) != blob:
            sys.stderr.write("LANE_LINES_DRIFTED\n")
            return 1
        if digest != LANE_LINES_SHA256:
            sys.stderr.write(f"LANE_NOT_SEALED:{digest}\n")
            return 1
        if MASDAR_TSV.read_bytes() != mt or PLURAL_TSV.read_bytes() != pt:
            sys.stderr.write("LANE_RECORDS_DRIFTED\n")
            return 1
        if RESULT.exists() and RESULT.read_bytes() != dump(measure()):
            sys.stderr.write("LANE_RESULT_DRIFTED\n")
            return 1
        spans = blob.count(b"\n")
        sys.stdout.write(f"معجمُ لين مطابق: {spans:,} وسمًا، {len(m):,} مدخلَ مصدر، "
                         f"{len(p):,} مدخلَ جمع؛ بصمةُ السطور {digest}\n")
        return 0
    if "rules" in argv:
        masdar, plural, pat, refusals = setup()
        mr, me, pr, pe = rules(masdar, plural, pat)
        sys.stdout.write(dump({"masdar_rules": {k: sorted(v) for k, v in sorted(mr.items())},
                               "masdar_examples": me,
                               "plural_rules": {k: sorted(v) for k, v in sorted(pr.items())},
                               "plural_examples": pe}).decode("utf-8"))
        return 0
    if "measure" in argv:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_bytes(dump(measure()))
        sys.stdout.write(f"كُتب {RESULT.relative_to(ROOT)}\n")
        return 0
    LINES.write_bytes(gz(blob))
    MASDAR_TSV.write_bytes(mt)
    PLURAL_TSV.write_bytes(pt)
    sys.stdout.write(f"كُتب {LINES.name} ({digest})، {len(m):,} مدخلَ مصدر، {len(p):,} مدخلَ جمع\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
