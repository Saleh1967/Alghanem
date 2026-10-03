"""اختباراتُ المستهلِك الفعليّ: `tools/maqayis_links.py`.

وهذا البابُ يمتحن ما لا تمتحنه اختباراتُ الوحدة: أنّ الربطَ المستخرَجَ من
المتن يُقرَأ في مجرى العمل لا في معمله وحدَه. فلو بقي نجاحُ الاعتماد داخلَ
`tests/arabic/` لكان نجاحًا في اختبارٍ منفصلٍ لا في الآلة.

ويُشغَّل المنفِّذُ عمليّةً مستقلّةً كما يُشغِّله مستعمِلُه، لا باستدعاء
دوالِّه من الذاكرة: فالمقصودُ أن يُفحَص الطريقُ كلُّه من السطر إلى السجلّ.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL = REPO_ROOT / "tools" / "maqayis_links.py"

THE_MATERIAL = "أبت:13"
THE_MEANING = "الحرّ وشدّته"
THE_DIGEST = "2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0"


def _rows() -> list[dict[str, object]]:
    completed = subprocess.run(
        [sys.executable, str(TOOL), "--stdout"],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )
    return [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]


def test_the_real_consumer_reads_the_text_derived_link() -> None:
    """المستهلِكُ الفعليُّ يُخرِج الربطَ المستخرَجَ من المتن معتمَدًا ومُسمّى مصدرُه."""

    rows = _rows()
    links = [
        row
        for row in rows
        if row.get("نوع") == "مرشح" and row.get("مصدر_المعنى", "").startswith("متنُ")
    ]
    assert len(links) == 1
    link = links[0]
    assert link["مفتاح_المادة"] == THE_MATERIAL
    assert link["معنى_مرشح"] == THE_MEANING
    assert link["حقل_الصياغة"] == "body_text"
    assert link["حال_الاعتماد"] == "معتمَد"
    assert link["بند_المصالحة"] == [0, 49]
    assert link["قرار_البند"].startswith("نسبتُه إلى هذه المادّة محقَّقة")
    assert link["طرق_حاسمة"] == ["ترويسةُ المادّة تُسمّي حروفَها بأنفسها"]
    assert link["قرائن_ترشيح"] == []


def test_the_consumer_keeps_the_axis_candidates_distinct_from_the_link() -> None:
    """مرشَّحاتُ حقل المحاور تبقى مُميَّزةً عن الربط، ولا يُمحى أحدُهما بالآخر."""

    rows = _rows()
    counts = next(row for row in rows if row.get("نوع") == "عدّ")
    assert counts["روابط_من_المتن"] == 1
    assert counts["مرشحات_من_حقل_المحاور"] == 19
    assert (
        counts["مرشحات"] == counts["روابط_من_المتن"] + (counts["مرشحات_من_حقل_المحاور"])
    )
    # والمعتمَدُ واحدٌ من المتن، والتسعةَ عشرَ معلَّقون ولم يُطوَوا.
    assert counts["معتمدون"] == counts["معتمدون_من_المتن"] == 1
    assert counts["معلقون"] == 19
    # وعددُ الشهادات غيرُ عدد المعاني، وكلاهما مُخرَجٌ على حدة.
    assert counts["شهادات_مراجعة_مودعة"] == 1
    assert counts["معانٍ_مميزة"] == 19
    assert counts["معانٍ_مميزة_معتمدة"] == 1


def test_one_admitted_link_does_not_admit_the_dals_other_meanings() -> None:
    """الدالُّ المعتمَدُ رابطُه يبقى محدودَ التغطية، وحدُّه مكتوبٌ في صفّه."""

    rows = _rows()
    dal = next(
        row
        for row in rows
        if row.get("نوع") == "دال" and row.get("مفتاح_المادة") == THE_MATERIAL
    )
    assert dal["روابط_معتمدة_من_المتن"] == 1
    assert dal["مرشحات_من_حقل_المحاور"] == 1
    assert dal["معتمدون_من_حقل_المحاور"] == 0
    assert dal["شهادات_مراجعة"] == 1
    assert dal["حدود_التغطية"]
    assert "حدُّ المادّة غيرُ محقَّق" in dal["حدود_التغطية"]
    # وبقاءُ مرشَّحٍ قديمٍ معلَّقًا لا يمحو الربطَ الجديد، والعكسُ كذلك.
    assert dal["روابط_معلقة_من_المتن"] == 0
    assert dal["معانٍ_مميزة_معتمدة"] == 1


def test_reloading_the_report_keeps_the_pair_joined_to_its_dal_and_source() -> None:
    """إعادةُ تحميل السجلّ تحفظ اتّصالَ الزوج بدالِّه وبمصدره، فلا يُقرَأ طليقًا."""

    first = _rows()
    serialised = "\n".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) for row in first
    )
    reloaded = [json.loads(line) for line in serialised.splitlines()]
    assert reloaded == first

    link = next(
        row
        for row in reloaded
        if row.get("نوع") == "مرشح" and row.get("حال_الاعتماد") == "معتمَد"
    )
    dal = next(
        row
        for row in reloaded
        if row.get("نوع") == "دال" and row.get("مفتاح_المادة") == link["مفتاح_المادة"]
    )
    source = next(row for row in reloaded if row.get("نوع") == "مصدر")
    assert link["رتبة_الصف"] == dal["رتبة_الصف"]
    assert dal["روابط_معتمدة_من_المتن"] == 1
    assert len(source["بصمة_مقيسة"]) == 64
    assert source["بصمة_مقيسة"] == THE_DIGEST
    assert link["هوية_المعنى"] == [THE_MATERIAL, "الحر وشدته"]


def test_the_routes_are_published_with_their_strength_in_the_report() -> None:
    """طرقُ النسبة تُنشَر بقوّتها: الحاسمُ يُسمّى حاسمًا والقرينةُ قرينة."""

    rows = _rows()
    routes = {row["الطريق"]: row for row in rows if row.get("نوع") == "طريق_نسبة"}
    clue = routes["اتّساقُ الجذر حتّى أوّل صيغةٍ أجنبيّة"]
    assert clue["يحسم"] is False
    assert clue["قوّة"].startswith("قرينةُ ترشيح")
    assert any("لا ينقض نسبتَها" in limit for limit in clue["حدود"])
    head = routes["ترويسةُ المادّة تُسمّي حروفَها بأنفسها"]
    assert head["يحسم"] is True


def test_the_deposited_report_is_what_the_disk_generates_now() -> None:
    """السجلُّ المُودَعُ يُصادَم بما يولّده القرصُ، فلا يُقرَأ منقولًا عن ذاكرة."""

    completed = subprocess.run(
        [sys.executable, str(TOOL), "--check"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
