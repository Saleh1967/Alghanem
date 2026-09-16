"""قاعدةُ تجاهلٍ تمنع الإيداعَ صامتةً، فتُمسَك اختبارًا لا تنبيهًا.

هذا الاختبارُ مسنونٌ على **خطرٍ مقيس**: `corpora/MASAQ.csv` لا يُتجاهَل اليوم،
ولا قاعدةَ `*.csv` في الشجرة أصلًا. ولو سُنَّت لاحقًا — في `.gitignore` الجذر
أو في `corpora/.gitignore` — لصار `git add corpora/MASAQ.csv` **بلا أثر**:
لا رسالةَ خطأٍ ظاهرةً في كلّ الحالات، وإنّما ملفٌّ لا يُدرَج. وذلك عطبٌ صامت،
وأخبثُ من الرفع الفاشل باسمٍ طارئ لأنّه لا يترك في الشجرة ما يدلّ عليه.

وفرقُه عن `unsanctioned_deposit_files()` مقصود: تلك تُمسك ما **نزل** في موضع
الإيداع بلا إذن، وهذه تُمسك ما يمنع البايتاتِ من النزول أصلًا. فالحارسانِ
يقعانِ على طرفَي الإيداع، ولا يُغني أحدُهما عن الآخر.

وحدُّه مكتوبٌ فلا يُوسَّع بعده: لا يقرأ بايتةً، ولا يُعيد اشتقاقَ رقمٍ، ولا
يحكم على بصمةٍ ولا طول — تلك موضعُها `read_masaq_bytes`. وهو لا يوجب حضورَ
البايتات: يُمنَع تجاهلُ الموضع حاضرةً كانت أو غائبة، لأنّ المنعَ يُسَنّ قبل
الحاجة إليه لا بعد وقوع الضرر.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from alghanem.arabic.masaq_corpus_deposit import (
    DEPOSIT_DIRECTORY,
    MASAQ_RELATIVE_PATH,
    SANCTIONED_DEPOSIT_FILENAMES,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

SANCTIONED_DEPOSIT_PATHS = tuple(
    f"{DEPOSIT_DIRECTORY}/{name}" for name in SANCTIONED_DEPOSIT_FILENAMES
)
"""مسارا ما يجوز أن يسكن موضعَ الإيداع، مشتقّانِ من السَّنّ لا مُعادانِ كتابةً."""


def _git_available() -> bool:
    return shutil.which("git") is not None and (REPOSITORY_ROOT / ".git").exists()


def _ignore_rule_for(relative_path: str) -> str | None:
    """قاعدةُ التجاهل التي تُصيب المسار، أو `None` إن لم يُتجاهَل.

    و`git check-ignore -v` يُخرِج عند الإصابة سطرَ القاعدة بمصدرها ورقمها،
    ويخرج برمز `1` إن لم يُصَب المسارُ بشيء؛ وأيُّ رمزٍ آخر عطبٌ في الأداة
    لا حكمٌ على المسار، فيُرفَع.
    """

    completed = subprocess.run(
        ["git", "check-ignore", "-v", "--no-index", "--", relative_path],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 1:
        return None
    if completed.returncode == 0:
        return completed.stdout.strip()
    raise RuntimeError(
        f"`git check-ignore` أخفق برمز {completed.returncode}: "
        f"{completed.stderr.strip()}"
    )


@pytest.mark.skipif(not _git_available(), reason="لا شجرةَ git هنا فلا قاعدةَ تُقرأ")
@pytest.mark.parametrize("relative_path", SANCTIONED_DEPOSIT_PATHS)
def test_no_ignore_rule_hides_a_sanctioned_deposit_path(relative_path: str) -> None:
    """لا قاعدةَ تجاهلٍ تُصيب موضعًا مسنونًا في مجلَّد الإيداع."""

    rule = _ignore_rule_for(relative_path)
    assert rule is None, (
        f"`{relative_path}` يُصيبه تجاهلٌ: {rule}. وهذا يجعل إضافتَه تفشل "
        "صامتةً، فتبقى دعوى الإيداع بلا بايتات. فإمّا أن تُرفَع القاعدة، "
        f"وإمّا أن يُستثنى `{MASAQ_RELATIVE_PATH}` منها صراحةً."
    )


@pytest.mark.skipif(not _git_available(), reason="لا شجرةَ git هنا فلا قاعدةَ تُقرأ")
def test_the_probe_detects_an_ignore_rule_when_one_exists() -> None:
    """المِجسُّ يُصيب فعلًا؛ ومِجسٌّ لا يَكشف تجاهلًا قائمًا لا يمنع شيئًا.

    ويُقاس على مسارٍ متجاهَلٍ في الشجرة فعلًا، فلا تُكتَب قاعدةٌ لأجل اختبار.
    """

    assert _ignore_rule_for(f"{DEPOSIT_DIRECTORY}/__pycache__/x.pyc") is not None
