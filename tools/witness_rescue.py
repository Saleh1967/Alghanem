"""`witness_rescue.py` — أمرٌ واحدٌ يُعيد تشغيلَ إنقاذ الشاهد كلِّه.

يُعيد هذا الأمرُ، من بايتات المصادر المختومة في كلّ نداء:

- **الحالَ الصحيحة**: شاهدٌ مُسنَدٌ مرّت بوّاباتُه الخمس، فتُقبَل شهادتُه في
  حدود مصدره وقاعدته.
- **الشاهدَ المختلَق**: الموضعُ عينُه، ودعوى غيرُ مسندة، ومصدرٌ `README.md`،
  وموضعٌ لا وجودَ له، وسطحٌ مطابق — فيُرَدّ، وتُسمّى بوّاباتُه الساقطةُ واحدةً
  واحدة، وتتحرّك البصمةُ وإن ثبتت البايتات.
- **السحبَ والسندَ البديلَ والتصحيح**: فوق `KnowledgeStock` القائم، لا فوق
  محرّكٍ موازٍ: سحبُ الشاهد يُعلّق اشتقاقاتِه وحدَها، وتبقى الدعوى مدعومةً
  بالسند البديل، وسحبُ البديل يُعلّقها، ونقضُ اعتماد القاعدة يُعلّق ما اشتُقّ
  بها، والتصحيحُ يُنشئ إصدارًا ثانيًا ويحفظ التاريخ.

والاستعمال::

    python tools/witness_rescue.py             # يُعرَض الموجزُ ويُكتَب السجلّ
    python tools/witness_rescue.py --check     # يُصادَم المُودَعُ بما يولّده القرصُ
    python tools/witness_rescue.py --stdout    # يُطبَع السجلُّ ولا يُكتَب ملفّ

ولا يُحرَّر المُودَعُ يدويًّا: من غيَّره دون إعادةِ تشغيلٍ سقطت `--check`.

وحدُّ هذا الأمر مُعلَنٌ في مخرجه: نجاحُ سيناريو مُركَّبٍ ليس إثباتًا لصحّة
معرفة، والمصادمةُ تكشف العبثَ عند مقابلةِ المُودَعِ بما يولّده القرصُ، ولا
تجعل السجلَّ غيرَ قابلٍ لإعادة الكتابة بذاته.
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

from alghanem.arabic.witness_retraction_run import run  # noqa: E402
from alghanem.arabic.word_certificate_chain import (  # noqa: E402
    WordCertificate,
    certify,
    fingerprint,
)
from tools.word_certificate import (  # noqa: E402
    THE_ANALYSIS_WITNESSES,
    THE_CERTIFIED_ADDRESS,
    THE_FABRICATED_WITNESSES,
    THE_ORIGIN_WITNESS,
)

EXHIBIT_DIR: Final[Path] = REPO_ROOT / "exhibits" / "witness-rescue"
LEDGER_PATH: Final[Path] = EXHIBIT_DIR / "rescue.jsonl"
REPORT_PATH: Final[Path] = EXHIBIT_DIR / "REPORT.md"


def _witness_row(label: str, certificate: WordCertificate) -> dict[str, Any]:
    """صفُّ شهادةٍ بشواهدها المُدقَّقة، مُشتقٌّ من القرص لا مكتوبٌ فيه."""

    return {
        "الحالة": label,
        "العنوان": certificate.located.address.rendered,
        "السطح": certificate.located.surface,
        "الحكم_الإجمالي": certificate.overall.standing.value,
        "البصمة": fingerprint(certificate),
        "الشواهد": [
            {
                "الموضوع": one.subject.value,
                "المصدر": one.source_key,
                "الموضع": one.locus,
                "القاعدة": one.rule_versioned_id,
                "مقبول": one.admitted,
                "البوّابات_الساقطة": [two.value for two in one.failed_gates],
                "البوّابات": [
                    {"البوّابة": two.gate.value, "مرّت": two.passed, "السبب": two.cause}
                    for two in one.gates
                ],
                "ما_يُغلقها": one.what_would_close_it,
                "المراجعة_مسجَّلة": one.review is not None,
            }
            for one in certificate.witnesses
        ],
    }


def rescue_rows() -> tuple[dict[str, Any], ...]:
    """صفوفُ التشغيل: القبولُ ثمّ الردُّ ثمّ أحوالُ السحب والتصحيح."""

    sound = certify(
        THE_CERTIFIED_ADDRESS,
        witnesses=(THE_ORIGIN_WITNESS,),
        analysis_witnesses=THE_ANALYSIS_WITNESSES,
    )
    fabricated = certify(
        THE_CERTIFIED_ADDRESS,
        witnesses=(THE_ORIGIN_WITNESS,),
        analysis_witnesses=THE_FABRICATED_WITNESSES,
    )
    outcome = run()
    return (
        _witness_row("قبولٌ — شاهدان مُسنَدان", sound),
        _witness_row("ردٌّ — شاهدٌ مختلَق", fabricated),
        {
            "الحالة": "الإبطالُ المتسلسل فوق الرصيد القائم",
            "الأحوال": [
                {
                    "الاسم": one.label,
                    "منزلة_الدعوى": one.claim_standing.value,
                    "أسانيدُها_الحيّة": list(one.live_supports),
                    "طوائفُ_مستقلّة": one.independent_families,
                    "المعلَّق": list(one.suspended_ids),
                    "إصدارُ_الرصيد": one.stock_version,
                    "هويّةُ_المحتوى": one.stock_content_id,
                }
                for one in outcome.readings
            ],
            "الأثر": list(outcome.lines),
            "الحدودُ_المُعلَنة": list(outcome.limits),
        },
    )


def render_ledger(rows: tuple[dict[str, Any], ...]) -> str:
    """السجلُّ سطرًا سطرًا، مُرتَّبَ المفاتيح ليثبت نصُّه بين التشغيلات."""

    return (
        "\n".join(json.dumps(one, ensure_ascii=False, sort_keys=True) for one in rows)
        + "\n"
    )


def render_report(rows: tuple[dict[str, Any], ...]) -> str:
    """التقريرُ العربيُّ: القبولُ، والردُّ ببوّاباته، والإبطالُ حالًا حالًا."""

    sound, fabricated, cascade = rows
    lines: list[str] = [
        "# تقريرُ إنقاذِ الشاهد: قبولٌ مُسنَدٌ وإبطالٌ متسلسل",
        "",
        "> هذا الملفُّ مُولَّدٌ بـ`python tools/witness_rescue.py`؛ "
        "ولا يُحرَّر يدويًّا.",
        "",
        "## أوّلًا: القبولُ — شاهدان مرّت بوّاباتُهما الخمس",
        "",
        f"الموضع: `{sound['العنوان']}` · السطح: «{sound['السطح']}» · "
        f"الحكمُ الإجماليُّ: **{sound['الحكم_الإجمالي']}** · "
        f"البصمة: `{sound['البصمة']}`.",
        "",
        "| الموضوع | المصدر | الموضع | القاعدة | مقبول |",
        "| --- | --- | --- | --- | --- |",
    ]
    for one in sound["الشواهد"]:
        lines.append(
            f"| {one['الموضوع']} | `{one['المصدر']}` | `{one['الموضع']}` | "
            f"`{one['القاعدة']}` | {'نعم' if one['مقبول'] else 'لا'} |"
        )
    lines += [
        "",
        "والحكمُ الإجماليُّ معلَّقٌ بسببٍ مسمًّى لا مُرخَّص: المقدّماتُ اللازمةُ "
        "التي لا شاهدَ من جنسها تبقى معلَّقةً باسمها، والقبولُ ههنا قبولُ "
        "الشاهدِ في حدوده لا إغلاقُ الشهادة.",
        "",
        "## ثانيًا: الردُّ — شاهدٌ مختلَقٌ على الموضع نفسه",
        "",
        f"البصمة: `{fabricated['البصمة']}` — وتخالف بصمةَ الحال الصحيحة "
        f"`{sound['البصمة']}` والبايتاتُ واحدةٌ والسطحُ واحد.",
        "",
        "| البوّابة | مرّت | السبب |",
        "| --- | --- | --- |",
    ]
    for one in fabricated["الشواهد"]:
        for two in one["البوّابات"]:
            lines.append(
                f"| {two['البوّابة']} | {'نعم' if two['مرّت'] else 'لا'} | "
                f"{two['السبب']} |"
            )
    for one in fabricated["الشواهد"]:
        lines += [
            "",
            f"ومراجعتُه مسجَّلةٌ: `{one['المراجعة_مسجَّلة']}` — ولم تفتح بوّابةً "
            "ساقطة؛ فالمراجعةُ تُحفَظ بهويّتها ونطاقها ورتبتها ولا تُحوَّل إلى "
            "برهان.",
        ]
    lines += [
        "",
        "## ثالثًا: الإبطالُ المتسلسل فوق الرصيد القائم",
        "",
        "| الحال | منزلةُ الدعوى | أسانيدُها الحيّة | طوائفُ مستقلّة | المعلَّق |",
        "| --- | --- | --- | --- | --- |",
    ]
    for one in cascade["الأحوال"]:
        supports = " · ".join(one["أسانيدُها_الحيّة"]) or "—"
        suspended = " · ".join(one["المعلَّق"]) or "—"
        lines.append(
            f"| {one['الاسم']} | {one['منزلة_الدعوى']} | {supports} | "
            f"{one['طوائفُ_مستقلّة']} | {suspended} |"
        )
    lines += ["", "### الأثرُ مقروءًا", ""]
    lines.extend(f"- {one}" for one in cascade["الأثر"])
    lines += ["", "## الحدودُ المُعلَنة", ""]
    lines.extend(f"- {one}" for one in cascade["الحدودُ_المُعلَنة"])
    lines += [
        "",
        "ونجاحُ هذا السيناريو نجاحُ آليّةٍ على مُدخَلاتٍ مُركَّبة، وليس إثباتًا "
        "لصحّة معرفة؛ ومصادمةُ `--check` تكشف العبثَ بمقابلةِ المُودَعِ بما "
        "يولّده القرصُ، ولا تجعل السجلَّ غيرَ قابلٍ لإعادة الكتابة بذاته.",
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

    rows = rescue_rows()
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
                + "  أعد التشغيل: python tools/witness_rescue.py\n"
            )
            return 1
        sys.stdout.write("المُودَعُ يُطابق ما يولّده القرصُ.\n")
        return 0

    EXHIBIT_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(ledger, encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")
    for one in rows[:2]:
        admitted = sum(1 for two in one["الشواهد"] if two["مقبول"])
        sys.stdout.write(
            f"{one['الحالة']}: مقبولٌ منها {admitted} من {len(one['الشواهد'])} · "
            f"البصمة {one['البصمة'][:12]}…\n"
        )
    for one in rows[2]["الأحوال"]:
        sys.stdout.write(f"{one['الاسم']}: {one['منزلة_الدعوى']}\n")
    sys.stdout.write(
        f"كُتِب: {LEDGER_PATH.relative_to(REPO_ROOT)} · "
        f"{REPORT_PATH.relative_to(REPO_ROOT)}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
