"""مطابقةُ النموذج الصوريّ في Lean بالنموذج البايثونيّ — خانةً خانةً وحالةً حالة.

البرهانُ في `formal/a116/` برهانٌ عن **الدالّة المكتوبة في Lean**. ولا ينتقل إلى
`a116_bridge_licence.step` إلّا إذا ثبت أنّ الدالّتين **واحدةٌ** على مجالهما
كلِّه. وهذا الملفّ يُثبت ذلك استقصاءً لا بعيّنة:

* يقرأ جدولَ Lean (‎3 × 116 = 348‎ سطرًا من `lake exe a116-table`).
* يردّ رقمَ الحامل إلى `THE_CARRIERS` ورقمَ الحالة إلى `THE_HARAKAT`.
* يشغّل `step` البايثونيّ على الزوج نفسِه ويقابل الناتج.
* ويسقط إن نقص سطر، أو تكرّر، أو اختلف ناتج، أو اختلف ترتيبُ الحوامل والحالات
  عمّا افترضه ملفُّ Lean (الهمزةُ في الموضع 28، والسكونُ رابعُ الحالات).

ولمّا كان `run` في الطرفين طيًّا يساريًّا للانتقال نفسِه من الحالة نفسِها، فتطابقُ
الانتقال على المجال كلِّه يُوجِب تطابقَ الأثر على كلّ سلسلةٍ بأيّ طول؛ فتنتقل
مبرهناتُ Lean إلى الشيفرة البايثونيّة بهذا التطابق وحدَه.

وإن مُرِّر ملفٌّ ثانٍ (`lake exe a116-table counts`) قوبلت أعدادُ ‎U(n)‎ التي
برهن Lean تقابلَها بعدٍّ مباشرٍ في البايثون: كلُّ سلسلةٍ من الـ116 بطول ‎n ≤ 2‎
تُشغَّل بـ`run_declared_model` وتُعَدّ ما لم تسقط. فالعددُ المبرهَنُ يُصادَم
بالآلة البايثونيّة نفسِها لا بقيمةٍ مكتوبة.

الاستعمال::

    lake exe a116-table > table.csv
    lake exe a116-table counts > counts.csv
    python tools/lean_a116_conformance.py table.csv counts.csv
"""

from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

from alghanem.arabic.a116_bridge_licence import (
    THE_CARRIERS,
    THE_HARAKAT,
    SyllableState,
    a116_cells,
    fixpoint_reading,
    run_declared_model,
    step,
)

EXPECTED_ROWS = 3 * 116
HAMZA_INDEX_IN_LEAN = 28
SUKUN_INDEX_IN_LEAN = 3
BRUTE_FORCE_UP_TO = 2


def _fail(message: str) -> int:
    print(f"✗ {message}", file=sys.stderr)
    return 1


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        return _fail("الاستعمال: lean_a116_conformance.py <جدول Lean> [أعداد Lean]")

    if len(THE_CARRIERS) != 29 or len(THE_HARAKAT) != 4:
        return _fail("أبعادُ البايثون غيرُ ‎29 × 4‎ التي يفترضها ملفُّ Lean")
    if THE_CARRIERS[HAMZA_INDEX_IN_LEAN] != "ء":
        return _fail("الحاملُ 28 في البايثون ليس الهمزةَ المفردة كما في Lean")
    if THE_HARAKAT[SUKUN_INDEX_IN_LEAN] != "ْ":
        return _fail("الحالةُ 3 في البايثون ليست السكونَ كما في Lean")
    if len(a116_cells()) != 116:
        return _fail("`a116_cells` لا يُخرِج 116 خانة")
    if fixpoint_reading().rungs != (1, 3):
        return _fail("درجاتُ الإشباع في البايثون ليست ‎(1, 3)‎ كما في `saturation_rungs`")

    rows = [
        line.strip()
        for line in Path(argv[1]).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) != EXPECTED_ROWS:
        return _fail(f"جدولُ Lean فيه {len(rows)} سطرًا لا {EXPECTED_ROWS}")

    seen: set[tuple[str, int, int]] = set()
    for row in rows:
        state_name, carrier, haraka, lean_next = row.split(",")
        key = (state_name, int(carrier), int(haraka))
        if key in seen:
            return _fail(f"سطرٌ مكرّر في جدول Lean: {row}")
        seen.add(key)
        cell = (THE_CARRIERS[key[1]], THE_HARAKAT[key[2]])
        python_next = step(SyllableState[state_name], cell).name
        if python_next != lean_next:
            return _fail(f"اختلافٌ عند {row}: البايثون يُخرِج {python_next}")

    expected = {
        (state.name, carrier, haraka)
        for state in SyllableState
        for carrier in range(len(THE_CARRIERS))
        for haraka in range(len(THE_HARAKAT))
    }
    if seen != expected:
        return _fail("جدولُ Lean لا يغطّي ‎الحالات × الخانات‎ كلَّها")

    if len(argv) == 3:
        failure = _check_counts(Path(argv[2]))
        if failure is not None:
            return _fail(failure)

    print(
        f"✓ الانتقالُ في Lean والبايثون واحدٌ على {len(seen)} زوجًا من ‎(حالة، خانة)‎ "
        "— فمبرهناتُ formal/a116 تصدق على `a116_bridge_licence.step`"
    )
    return 0


def _check_counts(path: Path) -> str | None:
    """أعدادُ ‎U(n)‎ من Lean مقابلَ العدّ المباشر بالآلة البايثونيّة حتى الطول 2."""

    lean_counts: dict[int, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            length, value = line.strip().split(",")
            lean_counts[int(length)] = int(value)
    cells = a116_cells()
    for length in range(BRUTE_FORCE_UP_TO + 1):
        if length not in lean_counts:
            return f"أعدادُ Lean تخلو من ‎U({length})‎"
        accepted = sum(
            1
            for word in product(cells, repeat=length)
            if run_declared_model(word) is not SyllableState.FELL_OUT_OF_THE_MODEL
        )
        if accepted != lean_counts[length]:
            return f"‎U({length})‎: Lean {lean_counts[length]}، والعدُّ المباشر {accepted}"
    print(
        f"✓ ‎U(n)‎ المبرهَنُ في Lean يطابق العدَّ المباشر حتى الطول {BRUTE_FORCE_UP_TO}: "
        + "، ".join(str(lean_counts[n]) for n in range(BRUTE_FORCE_UP_TO + 1))
    )
    return None


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
