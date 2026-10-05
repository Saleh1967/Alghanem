"""Freeze Sibawayh's pattern inventory (أبنية) from his own chapters, line by line.

Reads the two editions of al-Kitab deposited in hamil-hala-zaman-program
(``corpora/sources/sibawayh_kitab_sham.txt`` and ``..._jk.txt``), refuses any
byte that does not match the pinned digest, and writes
``corpora/sibawayh-abniya.tsv``. Every rule below is declared before any word
is tested; nothing is added after looking at a test word.

Rules
-----
* A *pattern token* is a word made only of the radical slots ف ع ل (in that
  order, ف before ع before the last ل) and the augment letters, standing
  immediately after one of the heads على / وعلى / مثال / يكون / ويكون / فيكون.
* Tier ``N``: the noun chapters (from «باب ما بنت العرب من الأسماء والصفات …» up
  to, not including, «باب ما أعرب من الأعجمية»), verb chapters excluded.
  A token is kept only when its clause is positive: no negation particle
  before it in the clause, unless a later positive marker (إلا, ولكن,
  فيكون, ويكون, وتلحق, قالوا, وقد) follows that negation.
* Tier ``V``: the two verb chapters (لحاق الزيادة بنات الثلاثة من الفعل … ما
  تسكن أوائله; تمثيل الفعل من بنات الأربعة), every token whatever its clause.
* Tier ``P``: Sibawayh's own rule for the nouns of augmented verbs (sham
  23891-23895: «وليس اسم منها إلا والميم لاحقته أولا … فالأسماء من الأفعال
  المزيدة على يفعل ويفعل»): each tier-V token that begins with ي, with that ي
  replaced by م.
* Variants (each written as its own row, never replacing the token): the
  article dropped (``article_dropped``); after a يكون head, a final alif read
  as tanwin and dropped (``tanwin_alif_dropped``); in tier V a final ت read as
  the subject suffix and dropped (``subject_ta_dropped``).
* Skeleton normalisation: hamza on any seat -> ء, آ -> ءا, ى -> ي.

The editions carry no vowels in these chapters, so a skeleton is all the
source supports; the inventory is a deliberate *superset* (lenient), which
makes "matches no pattern" the only decisive verdict a test can return.

Usage: python tools/sibawayh_abniya_extract.py HAMIL_SOURCES_DIR OUT_TSV
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

EDITIONS = {
    "sham": (
        "sibawayh_kitab_sham.txt",
        "ad676dffaa6df22a7b2ef4c4dbc4424d1e214e09e3f296a538ce887c89affcad",
        {
            "N": [(23235, 23840), (23961, 24199), (24224, 24273)],
            "V": [(23841, 23960), (24200, 24223)],
        },
    ),
    "jk": (
        "sibawayh_kitab_jk.txt",
        "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625",
        {
            "N": [(18621, 19035), (19133, 19314), (19334, 19373)],
            "V": [(19036, 19132), (19315, 19333)],
        },
    ),
}
AUGMENTS = set("ءأإآاتسلمنهويى")
NEG = {"ليس", "ليست", "لا", "ولا", "لم", "ولم", "فلا", "فليس", "وليس"}
POS = {"إلا", "ولكن", "ولكنه", "فيكون", "ويكون", "وتلحق", "قالوا", "وقد"}
HEADS = {"على", "وعلى", "مثال", "يكون", "ويكون", "فيكون"}
YAKUN = {"يكون", "ويكون", "فيكون"}
TOKEN = re.compile(r"[ء-ي]+|[.؛|]")


def is_pattern(t: str) -> bool:
    if not all(c in AUGMENTS or c in "فعل" for c in t):
        return False
    if "ف" not in t or "ع" not in t or "ل" not in t:
        return False
    return t.index("ف") < t.index("ع") < t.rindex("ل")


def skeleton(t: str) -> str:
    t = t.replace("آ", "ءا")
    t = re.sub("[أإؤئ]", "ء", t)
    return t.replace("ى", "ي")


def tokens(lines: list[str], lo: int, hi: int) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for n in range(lo, hi + 1):
        line = lines[n - 1]
        if line.startswith(("###", "PageV")) or "هذا باب" in line:
            continue
        line = re.sub(r"PageV\d+P\d+|ms\d+", "", line)
        out.extend((n, t) for t in TOKEN.findall(line))
    return out


def rows(edition: str, lines: list[str], tier: str, lo: int, hi: int):
    stream = tokens(lines, lo, hi)
    start = 0
    for k, (n, t) in enumerate(stream):
        if t in ".؛|":
            start = k + 1
            continue
        if not k or stream[k - 1][1] not in HEADS or not is_pattern(t):
            continue
        head = stream[k - 1][1]
        before = [w for _, w in stream[start : k - 1]]
        negs = [j for j, w in enumerate(before) if w in NEG]
        poss = [j for j, w in enumerate(before) if w in POS]
        positive = not negs or bool(poss and poss[-1] > negs[-1])
        if tier == "N" and not positive:
            continue
        found = [("as_written", t)]
        if t.startswith("ال"):
            found.append(("article_dropped", t[2:]))
        if head in YAKUN and t.endswith("ا"):
            found.append(("tanwin_alif_dropped", t[:-1]))
        if tier == "V" and t.endswith("ت"):
            found.append(("subject_ta_dropped", t[:-1]))
        for rule, form in found:
            if is_pattern(form):
                yield tier, skeleton(form), t, rule, edition, n
                if tier == "V" and form.startswith("ي"):
                    yield "P", skeleton("م" + form[1:]), t, "mim_for_ya", edition, n


def main(src: Path, out: Path) -> None:
    table = []
    for edition, (name, digest, tiers) in EDITIONS.items():
        data = (src / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise SystemExit(f"{name}: digest mismatch")
        lines = data.decode("utf-8").split("\n")
        for tier, ranges in tiers.items():
            for lo, hi in ranges:
                table.extend(rows(edition, lines, tier, lo, hi))
    header = "tier\tskeleton\ttoken\trule\tedition\tline"
    body = sorted(set(table), key=lambda r: (r[0], r[1], r[4], r[5], r[2], r[3]))
    out.write_text(
        header + "\n" + "".join("\t".join(map(str, r)) + "\n" for r in body),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
