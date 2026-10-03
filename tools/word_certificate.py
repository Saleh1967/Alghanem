"""`word_certificate.py` — مُخرِجُ شهادات الكلمة في سياقها، وتقريرِها العربيّ.

وهذا هو المستهلِك الفعليُّ لسلسلة التسليم: يُعيد اشتقاقَ كلّ شهادةٍ من
بايتاتِ المصادر المختومة، ويُودِع السجلَّ والتقريرَ في `exhibits/`، فيُصادَم
المُودَعُ بما يولّده القرصُ عند كلّ مراجعة.

والحالاتُ المُشهَدُ لها ثلاثٌ، وكلٌّ منها قياسٌ لا دعوى:

- **المُرخَّصة**: «حَيَاةٌ» في `QURAN_SIMPLE@L186:W4`، بشهادةِ منشأٍ مُودَعةٍ
  وشاهدَي تحليل.
- **المعلَّقة**: الموضعُ عينُه بلا شواهد، فتُسمّى كلُّ مقدّمةٍ عالقةٍ باسمها.
- **المردودة**: «وَفِي الْفَرْقِ نَظَرٌ» — عبارةُ التدقيق السابق، غائبةٌ عن
  كلّ مصدرٍ مختومٍ في الشجرة، فلا يُنقَل إليها سياقٌ ولا تُبنى لها شهادة.

والاستعمال::

    python tools/word_certificate.py             # يُعرَض الموجزُ ويُكتَب السجلّ
    python tools/word_certificate.py --check     # يُصادَم المُودَعُ بما يولّده القرصُ
    python tools/word_certificate.py --stdout    # يُطبَع السجلُّ ولا يُكتَب ملفّ

ولا يُحرَّر المُودَعُ يدويًّا: من غيَّره دون إعادةِ تشغيلٍ سقطت `--check`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Final

REPO_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
SRC_ROOT: Final[Path] = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from alghanem.arabic.excerpt_origin_bridge import (  # noqa: E402
    OriginWitness,
    WordAddress,
    address_collisions,
    origin_readings,
    prior_audit_standing,
)
from alghanem.arabic.word_certificate_chain import (  # noqa: E402
    THE_DECLARED_SCOPE,
    AnalysisSubject,
    AnalysisWitness,
    LayerStanding,
    WordCertificate,
    certify,
    fingerprint,
)

EXHIBIT_DIR: Final[Path] = REPO_ROOT / "exhibits" / "word-certificate"
LEDGER_PATH: Final[Path] = EXHIBIT_DIR / "certificates.jsonl"
REPORT_PATH: Final[Path] = EXHIBIT_DIR / "REPORT.md"

THE_CERTIFIED_ADDRESS: Final[WordAddress] = WordAddress("QURAN_SIMPLE", 186, 4)

THE_PRIOR_AUDIT_SURFACE: Final[str] = "\u0646\u064e\u0638\u064e\u0631\u064c"

THE_ORIGIN_WITNESS: Final[OriginWitness] = OriginWitness(
    dataset_id="ALGHANEM-WORD-CERTIFICATE-1",
    dataset_line_id="L186:W4",
    source_key="QURAN_SIMPLE",
    source_char_offset=30204,
    method="حلُّ عنوانٍ إلى إزاحةٍ في بايتاتٍ مختومةٍ ثمّ مصادمةُ السطح",
    examiner="tools/word_certificate.py",
)

THE_ANALYSIS_WITNESSES: Final[tuple[AnalysisWitness, ...]] = (
    AnalysisWitness(
        subject=AnalysisSubject.ROOT_AND_WAZN,
        claim="الحوامل «حَيَاة» بعد عزل علامة التنوين؛ والتاءُ مربوطةٌ في الرسم",
        surface="\u062d\u064e\u064a\u064e\u0627\u0629\u064c",
        lexical_source="corpora/quran-simple-enhanced.txt",
        lexical_locus="2:179 — «وَلَكُمْ فِي الْقِصَاصِ حَيَاةٌ»",
        examiner="tools/word_certificate.py",
    ),
    AnalysisWitness(
        subject=AnalysisSubject.SYNTACTIC_FUNCTION,
        claim="نكرةٌ مرفوعةٌ بالضمّة، وقبلها شبهُ جملةٍ «فِي الْقِصَاصِ»",
        surface="\u062d\u064e\u064a\u064e\u0627\u0629\u064c",
        lexical_source="corpora/quran-simple-enhanced.txt",
        lexical_locus="2:179 — السطرُ نفسُه",
        examiner="tools/word_certificate.py",
    ),
)


def _certificate_row(label: str, certificate: WordCertificate) -> dict[str, Any]:
    """صفٌّ واحدٌ في السجلّ، مأخوذٌ من الشهادة المُشتَقّة لا من حقلٍ مكتوب."""

    located = certificate.located
    return {
        "الحالة": label,
        "العنوان": located.address.rendered,
        "السطح": located.surface,
        "إزاحة_المحارف": located.char_offset,
        "إزاحة_البايتات": located.byte_offset,
        "حدّا_المقتطف": list(located.excerpt_bounds),
        "قبله": located.preceding_word,
        "بعده": located.following_word,
        "ذرّات_116": list(certificate.admission.atoms),
        "حالة_البروتوكول": certificate.admission.status,
        "ما_سقط_في_التصيير": list(certificate.admission.lost_in_the_rendering),
        "التنوين": certificate.tanwin.mark_name,
        "أحكام_الطبقات": {
            one.layer.value: {
                "المنزلة": one.standing.value,
                "السبب": one.cause,
                "العالقة": list(one.blocking_premises),
            }
            for one in certificate.verdicts
        },
        "الحكم_الإجمالي": {
            "المنزلة": certificate.overall.standing.value,
            "السبب": certificate.overall.cause,
            "العالقة": list(certificate.overall.blocking_premises),
        },
        "المقدّمات": [
            {
                "الاسم": one.name,
                "الطبقة": one.layer.value,
                "لماذا_استُدعيت": one.why_invoked,
                "دليل_قبولها": one.admission_evidence,
                "لماذا_تنطبق": one.why_it_applies_here,
                "ماذا_تثبت": one.what_it_establishes,
                "المنزلة": one.standing.value,
                "لازمة": one.required_for_the_claim,
                "تبعيّاتها": list(one.depends_on),
            }
            for one in certificate.premises
        ],
        "الانتقالات": [
            {
                "مدخل": one.station_in,
                "عملية": one.operation,
                "شرط": one.condition,
                "مانع": one.obstacle,
                "شاهد": one.witness,
                "رتبة": one.rank.value,
                "مخرج": one.station_out,
                "تبعيّات": list(one.dependencies),
                "بقايا": list(one.residue),
            }
            for one in certificate.transitions
        ],
        "البصمة": fingerprint(certificate),
    }


def _refused_row() -> dict[str, Any]:
    """صفُّ العبارةِ المردودة: منشؤها مجهولٌ فلا شهادةَ ولا نقلَ سياق."""

    readings = origin_readings(THE_PRIOR_AUDIT_SURFACE)
    audit = prior_audit_standing()
    collisions = address_collisions(329, 3)
    return {
        "الحالة": "مردودة — عبارةُ التدقيق السابق",
        "السطح": THE_PRIOR_AUDIT_SURFACE,
        "العنوان_المدَّعى": "L329:W3",
        "مادّة_التدقيق_حاضرة": audit.archive_present,
        "قابلة_لإعادة_الإنتاج": audit.is_reproducible,
        "ما_يُخرجه_العنوان_في_كلّ_مصدر": [
            {"المصدر": key, "المدلول": surface} for key, surface in collisions
        ],
        "الدعاوى": [
            {
                "الدعوى": one.claim.value,
                "المنزلة": one.standing.value,
                "الدليل": one.evidence,
                "المواضع": [list(two) for two in one.positions],
            }
            for one in readings
        ],
    }


def ledger_rows() -> tuple[dict[str, Any], ...]:
    """الصفوفُ الثلاثةُ مُشتقّةً من القرص عند كلّ نداء، ولا تُخزَّن."""

    licensed = certify(
        THE_CERTIFIED_ADDRESS,
        witnesses=(THE_ORIGIN_WITNESS,),
        analysis_witnesses=THE_ANALYSIS_WITNESSES,
    )
    suspended = certify(THE_CERTIFIED_ADDRESS)
    return (
        _certificate_row("مُرخَّصة — بشهادةٍ وشاهدَين", licensed),
        _certificate_row("معلَّقة — بلا شواهد", suspended),
        _refused_row(),
    )


def render_ledger(rows: tuple[dict[str, Any], ...]) -> str:
    """السجلُّ سطرًا سطرًا، مُرتَّبَ المفاتيح ليثبت نصُّه بين التشغيلات."""

    return (
        "\n".join(json.dumps(one, ensure_ascii=False, sort_keys=True) for one in rows)
        + "\n"
    )


def render_report(rows: tuple[dict[str, Any], ...]) -> str:
    """التقريرُ العربيُّ يُميّز المغلقَ والممتنعَ والمعلَّق، بدليل كلّ حكم."""

    licensed, suspended, refused = rows
    lines: list[str] = [
        "# تقريرُ شهادةِ الكلمة في سياقها",
        "",
        "> هذا الملفُّ مُولَّدٌ بـ`python tools/word_certificate.py`؛ " "ولا يُحرَّر يدويًّا.",
        "",
        "## النطاقُ، مُعلَنًا قبل القياس",
        "",
    ]
    lines.extend(f"- **المشمول**: {one}" for one in THE_DECLARED_SCOPE.included)
    lines.extend(f"- **المستثنى**: {one}" for one in THE_DECLARED_SCOPE.excluded)
    lines.append("- **المؤجَّل**: " + " · ".join(THE_DECLARED_SCOPE.deferred))
    lines.extend(f"- **العزل**: {one}" for one in THE_DECLARED_SCOPE.insulation)
    lines += [
        "",
        "## أوّلًا: المغلَق — شهادةٌ مُرخَّصةٌ داخل نطاقها",
        "",
        f"الموضع: `{licensed['العنوان']}` · السطح: «{licensed['السطح']}» · "
        f"إزاحةُ المحارف {licensed['إزاحة_المحارف']} · إزاحةُ البايتات "
        f"{licensed['إزاحة_البايتات']} · الحدّان {licensed['حدّا_المقتطف']}.",
        "",
        f"الحكم: **{licensed['الحكم_الإجمالي']['المنزلة']}** — "
        f"{licensed['الحكم_الإجمالي']['السبب']}",
        "",
        f"البصمة: `{licensed['البصمة']}`",
        "",
        "### أحكامُ الطبقات",
        "",
        "| الطبقة | المنزلة | العالقة |",
        "| --- | --- | --- |",
    ]
    for layer, verdict in licensed["أحكام_الطبقات"].items():
        blocked = " · ".join(verdict["العالقة"]) or "—"
        lines.append(f"| {layer} | {verdict['المنزلة']} | {blocked} |")
    lines += [
        "",
        "### السلسلةُ بانتقالاتها",
        "",
        "| مدخل | عملية | رتبة | مخرج | بقايا |",
        "| --- | --- | --- | --- | --- |",
    ]
    for step in licensed["الانتقالات"]:
        residue = " · ".join(step["بقايا"]) or "—"
        lines.append(
            f"| {step['مدخل']} | {step['عملية']} | {step['رتبة']} | "
            f"{step['مخرج']} | {residue} |"
        )
    lines += [
        "",
        "## ثانيًا: المعلَّق — الموضعُ نفسُه بلا شواهد",
        "",
        f"الحكم: **{suspended['الحكم_الإجمالي']['المنزلة']}** — "
        f"{suspended['الحكم_الإجمالي']['السبب']}",
        "",
        "والمقدّماتُ العالقةُ مُسمّاةٌ بأسمائها: "
        + " · ".join(suspended["الحكم_الإجمالي"]["العالقة"]),
        "",
        "وهذا هو **فرقُ ما قبلَ التعديل وما بعده** في نتائج التشغيل الفعليّة: "
        "الموضعُ واحدٌ والبايتاتُ واحدة، والحكمُ يتحرّك بحركةِ الشواهد وحدَها.",
        "",
        "## ثالثًا: الممتنع — عبارةُ التدقيق السابق",
        "",
        f"السطح: «{refused['السطح']}» · العنوانُ المدَّعى: "
        f"`{refused['العنوان_المدَّعى']}`.",
        "",
        "مادّةُ التدقيق السابق غائبةٌ عن الشجرة، فالتدقيقُ غيرُ قابلٍ "
        "لإعادة الإنتاج: "
        f"`archive_is_present={refused['مادّة_التدقيق_حاضرة']}` · "
        f"`is_reproducible={refused['قابلة_لإعادة_الإنتاج']}`.",
        "",
        "والعنوانُ المجرَّدُ من مفتاح مصدرٍ ليس هويّةً، بل إزاحةٌ تُخرج في كلّ "
        "مصدرٍ مدلولًا آخَر:",
        "",
        "| المصدر | ما يُخرجه `L329:W3` |",
        "| --- | --- |",
    ]
    for one in refused["ما_يُخرجه_العنوان_في_كلّ_مصدر"]:
        lines.append(f"| {one['المصدر']} | «{one['المدلول']}» |")
    lines += [
        "",
        "ودعاوى المنشأ الثلاثُ مفصولةٌ بمنازلها:",
        "",
        "| الدعوى | المنزلة | الدليل |",
        "| --- | --- | --- |",
    ]
    for one in refused["الدعاوى"]:
        lines.append(f"| {one['الدعوى']} | {one['المنزلة']} | {one['الدليل']} |")
    lines += [
        "",
        "فلا يُنقَل إلى هذا المقتطف سياقٌ من موضعٍ مرشَّح، ولا يُحتسَب الموضعُ "
        "الجديدُ المُشهَدُ له حلًّا لمنشأ السطر القديم. وهذا تقدُّمٌ تنفيذيٌّ "
        "مع بقاءِ منشأ المقتطف مجهولًا، لا إغلاقٌ للشهادة السياقيّة.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """يكتب أو يُصادم أو يطبع؛ ولا يُحرَّر المُودَعُ بغير هذا الأمر."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="يُصادَم المُودَعُ بما يولّده القرصُ، ولا يُكتَب شيء",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="يُطبَع السجلُّ ولا يُكتَب ملفّ",
    )
    args = parser.parse_args(argv)

    rows = ledger_rows()
    ledger = render_ledger(rows)
    report = render_report(rows)

    if args.stdout:
        sys.stdout.write(ledger)
        return 0

    if args.check:
        drift: list[str] = []
        for path, generated in ((LEDGER_PATH, ledger), (REPORT_PATH, report)):
            if not path.is_file():
                drift.append(f"{path.relative_to(REPO_ROOT)}: غائبٌ عن الشجرة")
            elif path.read_text(encoding="utf-8") != generated:
                drift.append(f"{path.relative_to(REPO_ROOT)}: يخالف ما يولّده القرصُ")
        if drift:
            sys.stderr.write(
                "المُودَعُ لا يُطابق المولَّد:\n"
                + "".join(f"  - {one}\n" for one in drift)
                + "  أعد التشغيل: python tools/word_certificate.py\n"
            )
            return 1
        sys.stdout.write("المُودَعُ يُطابق ما يولّده القرصُ.\n")
        return 0

    EXHIBIT_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(ledger, encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")
    for one in rows:
        if "الحكم_الإجمالي" in one:
            sys.stdout.write(f"{one['الحالة']}: {one['الحكم_الإجمالي']['المنزلة']}\n")
        else:
            sys.stdout.write(
                f"{one['الحالة']}: إعادةُ الإنتاج " f"{one['قابلة_لإعادة_الإنتاج']}\n"
            )
    sys.stdout.write(
        f"كُتِب: {LEDGER_PATH.relative_to(REPO_ROOT)} · "
        f"{REPORT_PATH.relative_to(REPO_ROOT)}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


_ = LayerStanding
