"""مُخرِجُ جسر الدالّ/المدلول: يُشتَقُّ السجلُّ والمقاييسُ عند كلّ تشغيل.

والاستعمال::

    python tools/bridge.py            # يُعرَض السجلُّ وتقريرُ المقاييس
    python tools/bridge.py --write    # يُكتَب `bridge_report.jsonl` معهما

ولا يحمل هذا الملفُّ رقمًا واحدًا من أرقام التقرير: كلُّها تُستدعى من
`alghanem.arabic.dal_madlul_bridge`، وهي هناك مُشتقّةٌ من بايتاتٍ مختومة.
فمن شغّل هذا المُخرِج على الوديعة نفسِها أعاد كلَّ رقمٍ فيه، ومن شغّله على
وديعةٍ منزاحةٍ لم يحصل على رقمٍ ناقصٍ بل على توقُّفٍ مُسمًّى.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPOSITORY_ROOT / "src"))

from alghanem.arabic.dal_madlul_bridge import (  # noqa: E402
    THE_CLASS_ANCHORS,
    THE_DEFERRED,
    BridgePair,
    DalalaChannel,
    coverage,
    derive_pairs,
    pairs_in,
    pending_dawal,
    separation_count,
    unopened_channels,
)

REPORT_RELATIVE_PATH = "exhibits/dal-madlul-bridge/bridge_report.jsonl"


def _row(pair: BridgePair) -> dict[str, str]:
    """الأركانُ الستّة، طرفَين متجاورَين لا كائنًا ثالثًا يحملهما."""

    return {
        "دال": pair.dal,
        "قناة": pair.channel.value,
        "مدلول": pair.madlul,
        "صنف_المدلول": pair.madlul_class.value,
        "دليل_حرفي": pair.literal_evidence,
        "مصدر_مختوم": pair.sealed_source,
        "اللزوم": pair.iltizam.value,
    }


def render_report() -> str:
    """تقريرُ المقاييس بأرقامٍ خام؛ والساقطُ يُعرَض ساقطًا."""

    pairs = derive_pairs()
    matched, every = coverage()
    tagged = sum(1 for one in pairs if one.is_tagged_by_evidence)
    pending = pending_dawal()
    lines: list[str] = []
    lines.append("# تقريرُ جسر الدالّ بالمدلول — أرقامٌ خام")
    lines.append("")
    lines.append("## المقاييسُ الأربعة، كما قُيِّدت قبل الرؤية")
    lines.append("")
    lines.append(f"* التغطية (مطابقة): **{matched} من {every}** دالًّا.")
    lines.append(
        f"* انضباطُ الأقسام: **{tagged} من {len(pairs)}** زوجًا "
        "حاز مدلولُه وسمًا من الخمسة بقرينةٍ مكتوبة."
    )
    lines.append(
        f"* الانفصال: **{separation_count()}** — ولا يُقرأ صفرًا إلّا "
        "باشتقاقه من الأزواج نفسِها."
    )
    lines.append(
        "* الصدق: **لم يُقَس** — لا عيّنةَ فحصِ سمعٍ ههنا، وعدُّ الأزواج "
        f"({len(pairs)}) أصغرُ من أن تُسحَب منه عيّنةٌ عشوائيّة؛ "
        "فالأزواجُ كلُّها معروضةٌ بدليلها لتُقرأ بالعين كلُّها."
    )
    lines.append("")
    lines.append("## القنواتُ الثلاث")
    lines.append("")
    for channel in DalalaChannel:
        lines.append(f"* {channel.value}: **{len(pairs_in(channel))}** زوجًا.")
    lines.append("")
    lines.append("## قنواتٌ طُلبت ولم تُفتَح — وسببُ امتناعِ كلٍّ منها")
    lines.append("")
    for name, why in unopened_channels():
        lines.append(f"* **{name}** — {why}")
    lines.append("")
    lines.append("## الدوالُّ الموسومةُ بقرينةٍ منصوصة")
    lines.append("")
    lines.append(
        f"نصَّ المتنُ على قسم مدلول **{len(THE_CLASS_ANCHORS)}** دوالَّ "
        "بأعيانها، وليس فيها دالٌّ من دوالِّ هذا الجسر؛ فوسمُ الخمسة "
        "لا يمتدُّ إليها بغير قرينة."
    )
    lines.append("")
    lines.append("## المعلَّق — صنفٌ أوّلٌ محفوظ")
    lines.append("")
    for one in pending:
        lines.append(f"* **{one.dal}** — {one.why}")
    lines.append("")
    lines.append("## المؤجَّل بالعقد")
    lines.append("")
    lines.append(f"{THE_DEFERRED.what} — {THE_DEFERRED.why}")
    return "\n".join(lines)


def render_jsonl() -> str:
    return "\n".join(
        json.dumps(_row(one), ensure_ascii=False) for one in derive_pairs()
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="مُخرِجُ جسر الدالّ/المدلول")
    parser.add_argument(
        "--write",
        action="store_true",
        help=f"يكتب {REPORT_RELATIVE_PATH} إلى جانب العرض",
    )
    arguments = parser.parse_args(argv)
    payload = render_jsonl()
    print(payload)
    print()
    print(render_report())
    if arguments.write:
        destination = _REPOSITORY_ROOT / REPORT_RELATIVE_PATH
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
