"""انتقاءُ الأبنية الموقَّع — المجالُ المعلَنُ الثالث (ADR ١٣، قرارُ المالك 2026-10-11).

الكتابُ المختوم (طبعةُ هارون، دار الجيل) بلا حركات؛ فتشكيلُ أبنية سيبويه لا يُشتقّ من مودَع. يُنقل
بيد المالك من طبعةٍ مشكولةٍ بموضعها ويوقَّع، ثمّ **يمرّ على البوّابة نفسها** — مدوّنةً مختومةً
ثالثة في `gate.api.SEALED_CORPORA` (`ABNIYA_INTIQA_CORPUS`) كما دخل الصحيحان (ADR ٧) — فلا يدخل
الشجرةَ لفظٌ إلّا من `gate.enter` ولا تُكتب حالةٌ بيد.

الإطار `corpora/abniya-intiqa.tsv`، صفٌّ لكلّ هيكلٍ من الـ158:

* أعمدةُ الآلة (`frame --slge DIR` من مودَعَي SLGE المختومَين ببصمتهما: `sibawayh-abniya.tsv`
  والكتاب): `id` (رقمُ الهيكل بترتيب SLGE)، `skeleton`، `kitab_lines` (أسطرُه في الكتاب المختوم
  JK006989 وحدَه؛ و«—» لهيكلٍ لم يُوجد إلّا في نسخة «sham» غيرِ المختومة هنا)، `sealed_page` (ج/ص
  من علامات الصفحات في المختوم نفسه، طبعة دار الجيل)، `priority` (1 = غيرُ ثلاثيّ الأصول، 2 =
  ثلاثيّ)؛ والصفوفُ مرتّبةٌ بالأولويّة ثمّ بأوّل سطرٍ في الكتاب.
* أعمدةُ المالك: `vocalized` (كلمةُ البناء مشكولةً كما في الطبعة — حروفُ الهيكل بعينها، وهمزةُ
  الوصل ٱ)، `edition` (الطبعة)، `page` (ج/ص فيها)، `note`.

`seal` يكتب `corpora/abniya-intiqa-lines.txt` من الصفوف المملوءة (كلمةٌ في سطر، بترتيب الإطار)
ويطبع بصمتَه لتُسجَّل في `ABNIYA_INTIQA_SHA256`. والتوقيعُ `corpora/owner-intiqa.json`
(`signed_by`، `signed_on`، `lines_sha256`) — ولا يُعدّ صفٌّ شاهدًا قبل التوقيع على بصمة السطور
الحاليّة.

`--check` (وبه `--slge DIR` للمطابقة عبر المستودعين، و`--deposit PATH` لمطابقة مودَع SLGE) يُسقط
البناءَ بأسمائها: `INTIQA_ROW_MALFORMED` (مملوءٌ بلا طبعةٍ أو موضع، أو فيه فراغ)،
`INTIQA_LINES_DRIFTED` (السطورُ غيرُ ما يولَّد من الإطار)، `INTIQA_NOT_SEALED` (بصمتُها غيرُ
المسجَّلة في البوّابة)، `INTIQA_SIGNATURE_STALE` (التوقيعُ على بصمةٍ أخرى)،
`INTIQA_SKELETON_MISMATCH` (حواملُ الشهادة غيرُ حروف الهيكل)، `INTIQA_FRAME_DRIFTED` (أعمدةُ الآلة
غيرُ ما يولَّد من مختومَي SLGE)، `DEPOSIT_DRIFTED_FROM_GATE`. ورفضُ البوّابة لصفٍّ **بيانٌ لا
خطأ**: يُسجَّل باسمه في المودَع (نقضٌ مسمًّى إن وُقِّع).

مطابقةُ الحوامل: حواملُ الشهادة = حروفُ الهيكل (والألفُ الأولى في هيكل الوصل همزة)، ولا زيادةَ إلّا
المعلَنتان: نونُ التنوين الأخيرة إن خُتمت الكلمةُ بعلامة تنوين، والتاءُ من التاء المربوطة (اصطلاحُ
الهياكل: لا ة فيها). والحالاتُ المودَعةُ حالاتُ حروف الهيكل وحدَها.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from gate.api import ABNIYA_INTIQA_CORPUS, ABNIYA_INTIQA_SHA256, Certificate, Gate

ROOT = Path(__file__).resolve().parent.parent
FRAME = ROOT / "corpora" / "abniya-intiqa.tsv"
LINES = ABNIYA_INTIQA_CORPUS
SIGNATURE = ROOT / "corpora" / "owner-intiqa.json"
ALPHABET = "ءابتثجحخدذرزسشصضطظعغفقكلمنهوي"
"""أبجديّةُ الحوامل بترتيب SLGE (`slge.cells.ALPHABET`): ترتيبُ الهياكل ترتيبُ رموزها فيها."""
SLGE_SOURCES = {
    "tests/data/sibawayh-abniya.tsv":
        "678ca5144698b571a42804b19b8d1680766df7f2339cf6c9c53d84994051fdd9",
    "tests/data/openiti-sibawayh-kitab.txt.gz":
        "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625",
}
"""مودَعا SLGE المختومان ببصمة محتواهما (بعد فكّ الضغط)، كما في `slge.manifest.DEPOSITS`."""
MACHINE = ("id", "skeleton", "kitab_lines", "sealed_page", "priority")
OWNER = ("vocalized", "edition", "page", "note")
TANWIN = "ًٌٍ"
TAA_MARBUTA = "ة"
ATOM_STATE = {"َ": "فتح", "ِ": "كسر", "ُ": "ضم", "ْ": "سكون"}
LAW = ("الكتابُ المختوم بلا حركات؛ فتشكيلُ الأبنية سماعٌ موقَّع من طبعةٍ مشكولةٍ بموضعها، يمرّ على البوّابة "
       "مدوّنةً مختومةً ثالثة (ADR ١٣)؛ والتوقيعُ واحدٌ فهو آحاد، والمالئُ الثاني يرفعه")


def _slge_bytes(slge: Path, rel: str) -> bytes:
    raw = (slge / rel).read_bytes()
    content = gzip.decompress(raw) if rel.endswith(".gz") else raw
    if hashlib.sha256(content).hexdigest() != SLGE_SOURCES[rel]:
        raise SystemExit(f"SLGE_SOURCE_SHA_MISMATCH {rel}")
    return raw if not rel.endswith(".gz") else content


def machine_rows(slge: Path) -> list[dict[str, str]]:
    """أعمدةُ الآلة من مختومَي SLGE: الهياكلُ بترتيب رموزها، وأسطرُها، وصفحاتُها في الطبعة المختومة."""

    src = _slge_bytes(slge, "tests/data/sibawayh-abniya.tsv").decode("utf-8")
    lines: dict[str, set[int]] = {}
    for r in csv.DictReader(src.splitlines(), delimiter="\t"):
        lines.setdefault(r["skeleton"], set())
        if r["edition"] == "jk":  # أسطرُ النصّ المختوم وحدَه (JK006989)؛ «sham» نصٌّ غيرُ مختومٍ هنا
            lines[r["skeleton"]].add(int(r["line"]))
    kitab_raw = _slge_bytes(slge, "tests/data/openiti-sibawayh-kitab.txt.gz")
    kitab = kitab_raw.decode("utf-8").splitlines()
    page: list[str] = []
    cur = "?"
    for ln in kitab:
        m = re.findall(r"PageV(\d+)P(\d+)", ln)
        page.append(cur)  # الصفحةُ التي يبدأ فيها السطر: آخرُ علامةٍ قبله
        if m:
            cur = f"{int(m[-1][0])}/{int(m[-1][1])}"
    order = sorted(lines, key=lambda s: tuple(ALPHABET.index(c) for c in s))
    rows = []
    for i, sk in enumerate(order, 1):
        roots = sorted(c for c in sk if c in "فعل")
        tri = roots == sorted("فعل")
        ls = sorted(lines[sk])
        pages = list(dict.fromkeys(page[n - 1] for n in ls))
        rows.append({"id": f"A{i:03d}", "skeleton": sk,
                     "kitab_lines": " ".join(map(str, ls)) or "—",
                     "sealed_page": " ".join(pages) or "—", "priority": "2" if tri else "1"})
    rows.sort(key=lambda r: (r["priority"], int(r["kitab_lines"].split()[0])
                             if r["kitab_lines"] != "—" else 10 ** 9))
    return rows


def read_frame() -> list[dict[str, str]]:
    with FRAME.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_frame(rows: list[dict[str, str]]) -> None:
    with FRAME.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=(*MACHINE, *OWNER), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def filled(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [r for r in rows if r["vocalized"].strip()]


def lines_text(rows: list[dict[str, str]]) -> str:
    return "".join(r["vocalized"].strip() + "\n" for r in filled(rows))


def malformed(rows: list[dict[str, str]]) -> list[str]:
    out = []
    for r in rows:
        v = r["vocalized"]
        if v.strip():
            if not r["edition"].strip() or not r["page"].strip() or v != v.strip() or " " in v:
                out.append(f"INTIQA_ROW_MALFORMED {r['id']}")
        elif r["edition"].strip() or r["page"].strip():
            out.append(f"INTIQA_ROW_MALFORMED {r['id']}")
    return out


def _carriers(atom: str) -> str:
    return atom[0]


def match(skeleton: str, vocalized: str, atoms: tuple[str, ...]) -> tuple[str, ...] | None:
    """حالاتُ حروف الهيكل من ذرّات الشهادة، أو لا شيء إن خالفت الحواملُ الهيكل (بالزيادتين
    المعلنتين)."""

    want = ("ء" + skeleton[1:]) if skeleton.startswith("ا") else skeleton
    got = [_carriers(a) for a in atoms]
    extra = len(got) - len(want)
    if vocalized and vocalized[-1] in TANWIN and extra >= 1 and got[-1] == "ن":
        got, atoms, extra = got[:-1], atoms[:-1], extra - 1
    if TAA_MARBUTA in vocalized and extra == 1 and got[-1] == "ت":
        got, atoms, extra = got[:-1], atoms[:-1], 0
    if extra != 0 or "".join(got) != want:
        return None
    return tuple(ATOM_STATE.get(a[-1], "?") for a in atoms)


def results(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    """لكلّ صفٍّ مملوء: شهادةُ البوّابة على المجال الثالث أو رفضُها المسمّى، ومطابقةُ الهيكل."""

    gate = Gate(corpus=LINES)
    out: list[dict[str, Any]] = []
    for r in filled(rows):
        v = r["vocalized"].strip()
        res = gate.enter(v.encode("utf-8"))
        row: dict[str, Any] = {"id": r["id"], "skeleton": r["skeleton"], "edition": r["edition"],
                               "page": r["page"]}
        if isinstance(res, Certificate):
            states = match(r["skeleton"], v, res.atoms)
            row.update(status="CERTIFICATE", atoms=list(res.atoms),
                       states=list(states) if states else None, reasons=[])
        else:
            row.update(status=res.status, atoms=None, states=None, reasons=list(res.reasons))
        out.append(row)
    return out


def signature() -> dict[str, Any]:
    d: dict[str, Any] = json.loads(SIGNATURE.read_text(encoding="utf-8"))
    return d


def deposit(rows: list[dict[str, str]]) -> dict[str, Any]:
    sha = hashlib.sha256(lines_text(rows).encode("utf-8")).hexdigest()
    sig = signature()
    return {"version": 1, "law": LAW, "lines_sha256": sha,
            "signed": bool(sig.get("signed_by")) and sig.get("lines_sha256") == sha,
            "signed_by": sig.get("signed_by"), "signed_on": sig.get("signed_on"),
            "frame": [{k: r[k] for k in MACHINE} for r in rows],
            "rows": results(rows)}


def canonical(d: dict[str, Any]) -> str:
    blob = json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def check(slge: Path | None, dep: Path | None) -> list[str]:
    rows = read_frame()
    bad = malformed(rows)
    text = lines_text(rows)
    on_disk = LINES.read_bytes()
    if on_disk != text.encode("utf-8"):
        bad.append("INTIQA_LINES_DRIFTED")
    sha = hashlib.sha256(on_disk).hexdigest()  # الختمُ على ما تقرؤه البوّابةُ بعينه
    if sha != ABNIYA_INTIQA_SHA256:
        bad.append("INTIQA_NOT_SEALED")
    sig = signature()
    if sig.get("signed_by") and sig.get("lines_sha256") != sha:
        bad.append("INTIQA_SIGNATURE_STALE")
    if not bad:
        bad += [f"INTIQA_SKELETON_MISMATCH {r['id']}" for r in results(rows)
                if r["status"] == "CERTIFICATE" and r["states"] is None]
    if slge is not None and [{k: r[k] for k in MACHINE} for r in rows] != machine_rows(slge):
        bad.append("INTIQA_FRAME_DRIFTED")
    if dep is not None and not bad:
        have = json.loads(gzip.decompress(dep.read_bytes()) if dep.name.endswith(".gz")
                          else dep.read_bytes())
        if canonical(have) != canonical(deposit(rows)):
            bad.append("DEPOSIT_DRIFTED_FROM_GATE")
    return bad


def _arg(argv: list[str], name: str) -> Path | None:
    return Path(argv[argv.index(name) + 1]) if name in argv else None


def main(argv: list[str]) -> int:
    if argv[:1] == ["frame"]:
        slge = _arg(argv, "--slge")
        assert slge, "frame --slge DIR"
        old = {r["id"]: r for r in read_frame()} if FRAME.exists() else {}
        rows = [{**m, **{k: old.get(m["id"], {}).get(k, "") for k in OWNER}}
                for m in machine_rows(slge)]
        write_frame(rows)
        if not SIGNATURE.exists():
            SIGNATURE.write_text(json.dumps({"signed_by": None, "signed_on": None,
                                             "lines_sha256": None, "law": LAW},
                                            ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        sys.stdout.write(f"كُتب الإطار: {len(rows)} هيكلًا، مملوءٌ {len(filled(rows))}\n")
        return 0
    if argv[:1] == ["seal"]:
        text = lines_text(read_frame())
        LINES.write_text(text, encoding="utf-8")
        sys.stdout.write(f"ABNIYA_INTIQA_SHA256 = {hashlib.sha256(text.encode()).hexdigest()}\n")
        return 0
    if argv[:1] == ["deposit"]:
        out = Path(argv[1])
        d = deposit(read_frame())
        out.write_text(json.dumps(d, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                       encoding="utf-8")
        sys.stdout.write(f"كُتب المودَع: {len(d['rows'])} صفًّا مملوءًا، موقَّع: {d['signed']}؛ "
                         f"بصمتُه {canonical(d)}\n")
        return 0
    if "--check" in argv:
        bad = check(_arg(argv, "--slge"), _arg(argv, "--deposit"))
        for b in bad:
            sys.stdout.write(b + "\n")
        if not bad:
            rows = read_frame()
            res = results(rows)
            refused = sum(r["status"] != "CERTIFICATE" for r in res)
            sys.stdout.write(f"الانتقاءُ مطابق: {len(rows)} هيكلًا، مملوءٌ {len(res)} (رفضتها البوّابة "
                             f"{refused})، موقَّع: {deposit(rows)['signed']}\n")
        return 1 if bad else 0
    sys.stdout.write("الاستعمال: frame --slge DIR | seal | deposit OUT | --check [--slge DIR] "
                     "[--deposit PATH]\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
