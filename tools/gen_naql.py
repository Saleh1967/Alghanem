"""شهاداتُ الوضع من أصحاب المعاجم: المفهومُ اللغويّ بالنقل (ADR ١٠٠، أمرُ المالك 2026-10-17).

قال المالك: «بناء المعجم مع lean دالة الوضع سيبني شبكة مفاهيم معجمية بشهادة بشريه من صاحب
المعجم المقاييس او ابن منظور او لدالفراهيدي فجميع شهاداتهم مقبولة وكذلك معاجمهم مقبولة والشهادات
تعاضد بعضها وهذا هو النقل الذي تعرف بها اللغة». والسندُ ج3 المختوم س367: «فإذا قالوا هم إن لفظ
كذا موضوع لمعنى كذا … فيقبل قولهم، ويسلم به» (والضميرُ للعرب الواضعين)، و«طريق معرفة اللغة العربية
هي النقل المتواتر وخبر الآحاد»، وأصحابُ المعاجم رواةُ آحاد «كالخليل». فالمودَعُ من نوع **وضع**
(الدستور، المادّة ١٢)، وكلُّ صفٍّ فيه روايةٌ لا «مفهوم» (ADR ١٠٠).

**المعاجمُ الثلاثة المختومة**:
* `k`: «العين» للخليل (`corpora/kitab/`، JK000930).
* `f`: «مقاييس اللغة» لابن فارس (`maqayis_by_root_csv_999.csv`).
* `m`: «لسان العرب» لابن منظور (`corpora/lisan/`، Shamela0001687).

**القواعدُ المعلنة**:
* `RULE_MADKHAL`: مدخلُ الجذر في كلّ معجم.
  * المقاييس: صفوفُ الجذر الثلاثيّ (`root_full` مطويًّا)، وسطورُ الطبعة داخل `body_text` تُوصل بمسافة
    (هي كسرُ سطرٍ في الجملة: «والمِداد:» ثمّ «ما يكتب به»).
  * اللسان: سطرُ «### $ جذر:» إلى السطر التالي المبدوء بـ«### ».
  * العين: سطرُ «# جذر» وحدَه، وقد تليه علامةُ المخطوط «msNNNN» (ثلاثةُ أحرف، أو حرفان للمضاعف فيُضاعَف
    الثاني)، إلى أيّ سطرٍ بشكله أو «### ».
  * لا يُفتح مدخلٌ إلّا لجذرٍ ثلاثيٍّ من جذور المقاييس.
* `RULE_B` (قاعدةُ `gen_hadith_roots` بعينها): اللفظُ هيكلٌ بلا حركات، مطويُّ الكراسيّ همزةً والمقصورة
  ياءً. ويُعدّ من الجذر إن وقعت أصولُه الثلاثة فيه بترتيبها.
* `RULE_ATF`: واوُ العطف أو فاؤه في أوّل الهيكل تُحذف مرّةً إن بقيت الأصولُ بعد حذفها بترتيبها
  («والكتاب» = «الكتاب»، و«ولد» من ولد يبقى).
* `RULE_ISNAD`: الشاهدُ من نُسب إليه القول.
  * الجملةُ تُقطع بالنقطة، وبالسطر في «العين» وحدَه (سطورُ اللسان والمقاييس كسرُ طبعةٍ تُوصل بمسافة).
  * إن ذُكر فيها «الخليل» أو «الليث» فشاهدُها الخليل، وإلّا فصاحبُ المعجم.
  * وكلُّ ما في «العين» شاهدُه الخليل.
  * فنقلُ الواحد عن الواحد شاهدٌ واحد («المعنعنة»، ج3 س367).
* `RULE_ASL`: حكمُ ابن فارس على الجذر من جملته الأولى (وإن لم يكن فيها إلّا أسماءُ الحروف وُصلت
  بالتي بعدها)، بأوّل ما يطابق بهذا الترتيب:
  1. `laysa`: «ليس بأصل»، «ليس أصل(ًا)»، «ليس فيه»، «ليس بشيء/بشئ».
  2. `usul`: «أصلان/معنيان/كلمتان» = 2، «ثلاثة/ثلاث» = 3، «أربعة» = 4، «خمسة» = 5.
  3. `wahid`: «أصل واحد»، «أصل صحيح»، «أصل يدل»، «متقاربة القياس»؛ أو «أصلٌ … وهو» بلا «مشترك».
     فـ«أصلٌ يدلّ على كذا، وعلى كذا» أصلٌ واحدٌ بلفظ ابن فارس.
  4. «يدل على/تدل على/يدل بناؤها على»: `wahid` إن لم تأتِ بعدها «وعلى»، وإلّا `usul` بعدد «على».
  5. `kalima`: «كلمة».
  6. وإلّا `laHukm`.
* `RULE_ILAQA` (ADR ١٠١): جملةٌ من نصّ ابن فارس فيها لفظٌ من الجذر (`RULE_B`، `RULE_ATF`)، وليست شعرًا
  (لا «…» ولا «*» ولا تبدأ بـ«قال»):
  * `haml` إن كان فيها لفظٌ أوّلُه «كأن»، أو لفظٌ من «شبه، شبهه، شبهت، شبهوا، يشبه، تشبيه، تشبيها،
    مجاز، مجازا، المجاز، استعارة» بعينه (بعد واوٍ أو فاء)، أو «يحمل/حمل/حملا عليه»؛ ولا يُعدّ لفظٌ
    من الجذر نفسه (فـ«مجازاة» في «جزي» ليست حملًا).
  * وإلّا `taalil` إن كان فيها «لأن» أو «سمي/سميت».
  * وإلّا فليست صفًّا.

المخرَجات:
* `corpora/naql/lawazim.tsv` (ADR ١٠١): الجذر، حكمُ ابن فارس، الصنف، رقمُ المدخل، الألفاظ، الجملةُ
  بعينها.
* `corpora/naql/shuhud.tsv.gz`: الجذر، الهيكل، المعاجم، القائلون، وأزواجُ (المعجم:القائل).
* `corpora/naql/usul.tsv`: الجذر، الحكم، العدد، الجملة الأولى بعينها.
* `corpora/naql/madakhil.tsv`: الجذر، المعجم، أوّلُ سطرٍ وآخرُه.
* `formal/a116/A116/NaqlData.lean`.

`--check` يُسقط البناءَ بأسمائها: `LISAN_SEAL_BROKEN`، `AYN_SEAL_BROKEN`، `MAQAYIS_SOURCE_DRIFTED`،
`NAQL_DEPOSIT_DRIFTED`، `NAQL_LEAN_DRIFTED`، `LAZIM_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAQAYIS = ROOT / "maqayis_by_root_csv_999.csv"
MAQAYIS_SHA256 = "2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0"
AYN = ROOT / "corpora" / "kitab" / "0170KhalilFarahidi.Cayn.JK000930-ara1.gz"
AYN_SHA256 = "e809c626239dee34bddd688b4382a8e314a559a0c700831b8b747fb01ed7d8a1"
LISAN = (ROOT / "corpora" / "lisan"
         / "0711IbnManzurIfriqi.LisanCarab.Shamela0001687-ara1.mARkdown.gz")
LISAN_SHA256 = "34fa56710a5b701532a34cb70f8fe440b261e80ae3c40d9667d18b65be7ed86d"
LISAN_BYTES = 30670791
OUT = ROOT / "corpora" / "naql"
SHUHUD = OUT / "shuhud.tsv.gz"
USUL = OUT / "usul.tsv"
MADAKHIL = OUT / "madakhil.tsv"
LEAN = ROOT / "formal" / "a116" / "A116" / "NaqlData.lean"
LAWAZIM = OUT / "lawazim.tsv"
LEAN_LAZIM = ROOT / "formal" / "a116" / "A116" / "LazimData.lean"
HAML_TOKENS = frozenset({"شبه", "شبهه", "شبهت", "شبهوا", "يشبه", "تشبيه", "تشبيها", "مجاز", "مجازا",
                         "المجاز", "استعارة", "واستعارة"})
TAALIL = re.compile(r"لأن|سمي|سميت")
LAZIM_SHAWAHID = (("مدد", "المداد"), ("تلو", "تلاوة"), ("كنف", "الكنف"), ("خشي", "خشيت"),
                  ("شرب", "الشرب"), ("طرف", "الطرف"))

FOLD = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ى": "ي"}
MARKS = re.compile(r"[ً-ْٰـ]")
WORD = re.compile(r"[ء-يً-ْٰ]+")
RADICALS = set("ءبتثجحخدذرزسشصضطظعغفقكلمنهوي")
KHALIL = re.compile(r"الخليل|الليث")
AYN_HEAD = re.compile(r"# ([ء-ي]{2,3})(?: ms\d+)?\s*")
DICTS = ("k", "f", "m")
OWN = {"k": "khalil", "f": "ibn-faris", "m": "ibn-manzur"}
WITNESS_ROOTS = ("كتب", "خشي", "ولد", "حبس", "ودد")


def fold(s: str) -> str:
    return "".join(FOLD.get(c, c) for c in s.replace("آ", "ءا"))


def skeleton(token: str) -> str:
    return fold(MARKS.sub("", token))


def in_order(sk: str, root: str) -> bool:
    i = 0
    for c in root:
        k = sk.find(c, i)
        if k < 0:
            return False
        i = k + 1
    return True


def _sealed(path: Path, sha: str, name: str) -> str:
    raw = gzip.decompress(path.read_bytes())
    if hashlib.sha256(raw).hexdigest() != sha:
        raise SystemExit(name)
    return raw.decode("utf-8")


def maqayis() -> dict[str, list[tuple[int, str]]]:
    """الجذرُ الثلاثيّ ← [(رقمُ المدخل، النصّ)] بترتيب الجدول."""

    data = MAQAYIS.read_bytes()
    if hashlib.sha256(data).hexdigest() != MAQAYIS_SHA256:
        raise SystemExit("MAQAYIS_SOURCE_DRIFTED")
    out: dict[str, list[tuple[int, str]]] = {}
    for row in csv.DictReader(io.StringIO(data.decode("utf-8"), newline="")):
        root = fold(row["root_full"])
        if len(root) == 3 and set(root) <= RADICALS:
            text = " ".join(row["body_text"].split("\n")).strip()
            out.setdefault(root, []).append((int(row["entry_num"]), text))
    return out


def ayn(roots: set[str]) -> dict[str, list[tuple[int, str]]]:
    out: dict[str, list[tuple[int, str]]] = {}
    cur: str | None = None
    for i, ln in enumerate(_sealed(AYN, AYN_SHA256, "AYN_SEAL_BROKEN").splitlines(), 1):
        m = AYN_HEAD.fullmatch(ln)
        if m or ln.startswith("### "):
            cur = None
            if m:
                h = fold(m.group(1))
                h = h + h[-1] if len(h) == 2 else h
                if h in roots:
                    cur = h
                    out.setdefault(h, [])
            continue
        if cur:
            out[cur].append((i, ln.lstrip("#~ ")))
    return out


def lisan(roots: set[str]) -> dict[str, list[tuple[int, str]]]:
    text = _sealed(LISAN, LISAN_SHA256, "LISAN_SEAL_BROKEN")
    if len(text.encode("utf-8")) != LISAN_BYTES:
        raise SystemExit("LISAN_SEAL_BROKEN")
    out: dict[str, list[tuple[int, str]]] = {}
    cur: str | None = None
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.startswith("### "):
            cur = None
            m = re.match(r"### \$ ([ء-ي]+):", ln)
            if m and fold(m.group(1)) in roots:
                cur = fold(m.group(1))
                out.setdefault(cur, [])
                ln = ln[m.end():]
        if cur:
            out[cur].append((i, ln.removeprefix("~~")))
    return out


def attest(root: str, text: str, own: str) -> dict[str, set[str]]:
    """`RULE_B` و`RULE_ISNAD`: هيكلٌ ← شهودُه في نصّ المدخل."""

    out: dict[str, set[str]] = {}
    for sent in re.split(r"[.\n]", text):
        who = "khalil" if KHALIL.search(sent) else own
        for tok in WORD.findall(sent):
            sk = skeleton(tok)
            if sk[:1] in ("و", "ف") and in_order(sk[1:], root):
                sk = sk[1:]
            if in_order(sk, root):
                out.setdefault(sk, set()).add(who)
    return out


def asl_hukm(clause: str) -> tuple[str, int]:
    """`RULE_ASL` على الجملة الأولى بلا حركات، بالترتيب المعلن في رأس الأداة."""

    c = MARKS.sub("", clause)
    if re.search(r"ليس بأصل|ليس أصل|ليس فيه|ليس بشيء|ليس بشئ", c):
        return "laysa", 0
    for pat, n in ((r"أصلان|معنيان|كلمتان", 2), (r"ثلاثة|ثلاث ", 3), (r"أربعة", 4), (r"خمسة", 5)):
        if re.search(pat, c):
            return "usul", n
    if re.search(r"أصل واحد|أصل صحيح|أصل يدل|متقاربة القياس", c):
        return "wahid", 1
    if re.search(r"أصل[^،.]*،? وهو", c) and "مشترك" not in c:
        return "wahid", 1
    m = re.search(r"يدل على|تدل على|يدل بناؤها على|تدل بناؤها على", c)
    if m:
        extra = len(re.findall(r"وعلى", c[m.end():]))
        return ("wahid", 1) if extra == 0 else ("usul", 1 + extra)
    if "كلمة" in c:
        return "kalima", 1
    return "laHukm", 0


LETTER_NAMES = re.compile(
    r"(?:و?ال)?(?:همزة|باء|تاء|ثاء|جيم|حاء|خاء|دال|ذال|راء|زاء|زاي|سين|شين|صاد|ضاد|طاء|ظاء|عين|غين"
    r"|فاء|قاف|كاف|لام|ميم|نون|هاء|واو|ياء|حرف|المعتل|معتل)")


def first_clause(body: str) -> str:
    """الجملةُ الأولى؛ وإن لم يكن فيها إلّا أسماءُ الحروف وُصلت بالتي بعدها (`RULE_ASL`)."""

    sents = [x.strip() for x in body.split(".")]
    words = [MARKS.sub("", w) for w in WORD.findall(sents[0])]
    if len(sents) > 1 and words and all(LETTER_NAMES.fullmatch(w) for w in words):
        return sents[0] + ". " + sents[1]
    return sents[0]


def build() -> tuple[list[tuple[str, str, str, str, str]], list[tuple[str, str, int, str]],
                     list[tuple[str, str, int, int]]]:
    mq = maqayis()
    roots = set(mq)
    k, m = ayn(roots), lisan(roots)
    shuhud: list[tuple[str, str, str, str, str]] = []
    usul: list[tuple[str, str, int, str]] = []
    madakhil: list[tuple[str, str, int, int]] = []
    for root in sorted(roots):
        texts = {
            "k": "\n".join(t for _, t in k.get(root, [])),
            "f": "\n".join(b for _, b in mq[root]),
            "m": " ".join(t.strip() for _, t in m.get(root, [])).replace(" ~~", " "),
        }
        at = {d: attest(root, texts[d], OWN[d]) for d in DICTS}
        for sk in sorted(set().union(*(at[d].keys() for d in DICTS))):
            ds = "".join(d for d in DICTS if sk in at[d])
            who = sorted(set().union(*(at[d].get(sk, set()) for d in DICTS)))
            pairs = [f"{d}:{q}" for d in DICTS for q in sorted(at[d].get(sk, set()))]
            shuhud.append((root, sk, ds, ",".join(who), ",".join(pairs)))
        clause = first_clause(mq[root][0][1])
        h, n = asl_hukm(clause)
        usul.append((root, h, n, clause))
        for d, src in (("k", k), ("m", m)):
            if src.get(root):
                madakhil.append((root, d, src[root][0][0], src[root][-1][0]))
        madakhil.append((root, "f", mq[root][0][0], mq[root][-1][0]))
    return shuhud, usul, madakhil


def render_tsv(rows: list[tuple[object, ...]]) -> str:
    return "".join("\t".join(str(x) for x in r) + "\n" for r in rows)


def _s(x: str) -> str:
    return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean(shuhud: list[tuple[str, str, str, str, str]], usul: list[tuple[str, str, int, str]],
                madakhil: list[tuple[str, str, int, int]]) -> str:
    by_w = [sum(1 for r in shuhud if len(r[3].split(",")) == n) for n in (1, 2, 3)]
    by_d = [sum(1 for r in shuhud if len(r[2]) == n) for n in (1, 2, 3)]
    reduced = sum(1 for r in shuhud if len(r[3].split(",")) < len(r[2]))
    classes = ("wahid", "usul", "kalima", "laysa", "laHukm")
    cls = [sum(1 for u in usul if u[1] == c) for c in classes]
    entries = [sum(1 for e in madakhil if e[1] == d) for d in DICTS]
    out = [
        "-- مولَّدٌ بـ`tools/gen_naql.py` من المعاجم الثلاثة المختومة؛ لا يُحرَّر باليد (ADR ١٠٠).",
        "",
        "namespace A116.NaqlData",
        "",
        "/-- عددُ جذور المقاييس الثلاثيّة، ومداخلُها في العين والمقاييس واللسان. -/",
        f"def jidhrCount : Nat := {len(usul)}",
        f"def madakhil : List Nat := {entries}",
        "/-- عددُ أزواج (الجذر، الهيكل) المشهودة. -/",
        f"def zawjCount : Nat := {len(shuhud)}",
        "/-- الأزواجُ بعدد الشهود المستقلّين ١، ٢، ٣ (`RULE_ISNAD`). -/",
        f"def biShuhud : List Nat := {by_w}",
        "/-- الأزواجُ بعدد المعاجم ١، ٢، ٣. -/",
        f"def biMaajim : List Nat := {by_d}",
        "/-- الأزواجُ التي شهودُها أقلُّ من معاجمها: نقلُ الواحد عن الواحد. -/",
        f"def naqlAnWahid : Nat := {reduced}",
        "/-- حكمُ ابن فارس على الجذر: wahid، usul، kalima، laysa، laHukm (`RULE_ASL`). -/",
        f"def hukmAsl : List Nat := {cls}",
        "",
        "/-- صفوفُ الشواهد: (الجذر، الهيكل، المعاجم، الشهود)، والشاهدُ (المعجم، القائل، السطر). -/",
        "def shawahid : List (String × String × String × List (String × String × Nat)) := [",
    ]
    line = {(e[0], e[1]): e[2] for e in madakhil}
    rows = [r for r in shuhud if r[0] in WITNESS_ROOTS and len(r[3].split(",")) >= 2]

    def wit(r: tuple[str, str, str, str, str]) -> str:
        ws = [p.split(":") for p in r[4].split(",")]
        return ", ".join(f"({_s(d)}, {_s(q)}, {line[(r[0], d)]})" for d, q in ws)

    out.append(",\n".join(f"  ({_s(r[0])}, {_s(r[1])}, {_s(r[2])}, [{wit(r)}])" for r in rows))
    out += ["]", "", "/-- حكمُ ابن فارس على جذور الشواهد: (الجذر، الحكم، العدد، الجملة الأولى). -/",
            "def uslShawahid : List (String × String × Nat × String) := ["]
    out.append(",\n".join(f"  ({_s(u[0])}, {_s(u[1])}, {u[2]}, {_s(u[3])})"
                          for u in usul if u[0] in WITNESS_ROOTS))
    out += ["]", "", "end A116.NaqlData", ""]
    return "\n".join(out)


def lawazim(usul: list[tuple[str, str, int, str]]) -> list[tuple[str, str, str, int, str, str]]:
    """`RULE_ILAQA`: جملُ ابن فارس التي تربط لفظًا من الجذر بأصله تعليلًا أو حملًا."""

    hukm = {u[0]: u[1] for u in usul}
    out: list[tuple[str, str, str, int, str, str]] = []
    for root, entries in sorted(maqayis().items()):
        for num, body in entries:
            for sent in re.split(r"[.\n]", body):
                bare = MARKS.sub("", sent).strip()
                if "…" in bare or "*" in bare or bare.startswith("قال"):
                    continue
                ws: list[str] = []
                for tok in WORD.findall(sent):
                    sk = skeleton(tok)
                    if sk[:1] in ("و", "ف") and in_order(sk[1:], root):
                        sk = sk[1:]
                    if in_order(sk, root) and sk not in ws:
                        ws.append(sk)
                if not ws:
                    continue
                toks = [t.removeprefix("و").removeprefix("ف") for t in re.findall(r"[ء-ي]+", bare)]
                haml = [t for t in toks if (t.startswith("كأن") or t in HAML_TOKENS)
                        and not in_order(fold(t), root)]
                haml += re.findall(r"(?:يحمل|حمل|حملا) عليه", bare) if root != "حمل" else []
                kind = "haml" if haml else ("taalil" if TAALIL.search(bare) else "")
                if kind:
                    out.append((root, hukm[root], kind, num, " ".join(ws), sent.strip()))
    return out


def render_lazim(rows: list[tuple[str, str, str, int, str, str]],
                 usul: list[tuple[str, str, int, str]]) -> str:
    kinds = [sum(1 for r in rows if r[2] == k) for k in ("taalil", "haml")]
    wahid = [sum(1 for r in rows if r[2] == k and r[1] in ("wahid", "kalima"))
             for k in ("taalil", "haml")]
    picked = []
    for root, w in LAZIM_SHAWAHID:
        r = min((x for x in rows if x[0] == root and w in x[4].split(" ")), key=lambda x: len(x[5]))
        picked.append(r)
    out = [
        "-- مولَّدٌ بـ`tools/gen_naql.py` من «مقاييس اللغة» المختومة؛ لا يُحرَّر باليد (ADR ١٠١).",
        "",
        "namespace A116.LazimData",
        "",
        "/-- عددُ جمل التعليل والحمل (`RULE_ILAQA`). -/",
        f"def bisinf : List Nat := {kinds}",
        "/-- منها ما جذرُه أصلٌ واحدٌ أو كلمةٌ واحدة عند ابن فارس. -/",
        f"def biAslWahid : List Nat := {wahid}",
        "",
        "/-- صفوفُ الشواهد: (الجذر، حكمُ ابن فارس، الصنف، رقمُ المدخل، الألفاظ، الجملة). -/",
        "def shawahid : List (String × String × String × Nat × List String × String) := [",
        ",\n".join(f"  ({_s(r[0])}, {_s(r[1])}, {_s(r[2])}, {r[3]}, "
                   f"[{', '.join(_s(w) for w in r[4].split(' '))}], {_s(r[5])})"
                   for r in picked),
        "]", "",
        "/-- حكمُ ابن فارس على جذور الشواهد: (الجذر، الحكم، العدد، الجملة الأولى). -/",
        "def usul : List (String × String × Nat × String) := [",
        ",\n".join(f"  ({_s(u[0])}, {_s(u[1])}, {u[2]}, {_s(u[3])})" for u in usul
                   if u[0] in {r for r, _ in LAZIM_SHAWAHID}),
        "]", "", "end A116.LazimData", ""]
    return "\n".join(out)


def gz(text: str) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=9, mtime=0) as f:
        f.write(text.encode("utf-8"))
    return buf.getvalue()


def main(argv: list[str]) -> int:
    shuhud, usul, madakhil = build()
    s_tsv, u_tsv, m_tsv = render_tsv(shuhud), render_tsv(usul), render_tsv(madakhil)
    lean = render_lean(shuhud, usul, madakhil)
    lz = lawazim(usul)
    l_tsv, l_lean = render_tsv(lz), render_lazim(lz, usul)
    if "--check" in argv:
        bad = 0
        if (not LAWAZIM.exists() or LAWAZIM.read_text(encoding="utf-8") != l_tsv
                or not LEAN_LAZIM.exists() or LEAN_LAZIM.read_text(encoding="utf-8") != l_lean):
            sys.stderr.write("LAZIM_DRIFTED: شغّل python tools/gen_naql.py\n")
            bad = 1
        if (not SHUHUD.exists() or gzip.decompress(SHUHUD.read_bytes()).decode("utf-8") != s_tsv
                or USUL.read_text(encoding="utf-8") != u_tsv
                or MADAKHIL.read_text(encoding="utf-8") != m_tsv):
            sys.stderr.write("NAQL_DEPOSIT_DRIFTED: شغّل python tools/gen_naql.py\n")
            bad = 1
        if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != lean:
            sys.stderr.write("NAQL_LEAN_DRIFTED: شغّل python tools/gen_naql.py\n")
            bad = 1
        if not bad:
            sys.stdout.write(f"naql مطابق: {len(shuhud)} زوجًا، {len(usul)} جذرًا\n")
        return bad
    OUT.mkdir(parents=True, exist_ok=True)
    SHUHUD.write_bytes(gz(s_tsv))
    USUL.write_text(u_tsv, encoding="utf-8")
    MADAKHIL.write_text(m_tsv, encoding="utf-8")
    LEAN.write_text(lean, encoding="utf-8")
    LAWAZIM.write_text(l_tsv, encoding="utf-8")
    LEAN_LAZIM.write_text(l_lean, encoding="utf-8")
    sys.stdout.write(f"كُتب المودَع ({len(shuhud)} زوجًا، {len(usul)} جذرًا) و{LEAN.name}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
