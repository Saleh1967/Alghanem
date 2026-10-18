"""البروتوكول في الدستور (الباب الرابع، ADR ١١١): توثيقُ كلّ خطوة، وسجلُّ طفرات Lean.

* سجلُّ الخطوات يُقرأ بقاعدته، والرسالةُ بلا خطوةٍ أو بخطوةٍ غيرِ مسجَّلة مرفوضةٌ باسمها.
* سجلُّ الطفرات: كلُّ نصٍّ يقع مرّةً واحدة في ملفّه، وADR كلِّ طفرةٍ موجود؛ والمكرَّرُ والملتبسُ مرفوضان.
* الدستورُ يحمل المواد ١٨–٢٤ بأسمائها، ونصَّ المالك بعينه.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONST = (ROOT / "AGENT_CONSTITUTION.md").read_text(encoding="utf-8")


def _load(name: str) -> Any:
    path = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P = _load("gen_protocol")
T = _load("gen_tafrat")
H = "khutwa\ttarikh\tunwan\tadr\tfuhus\n"


def test_log_by_hand() -> None:
    rows, errs = P.parse(H + "STEP-0001\t2026-10-18\tت\t111\ttafrat;protocol\n")
    assert errs == [] and rows == {"STEP-0001": ["tafrat", "protocol"]}
    # حالةٌ سالبة (لا طفرة): فحصٌ خارج القائمة المغلقة.
    _, errs = P.parse(H + "STEP-0001\t2026-10-18\tت\t111\ttafrat;مرّ_كلّه\n")
    assert errs == ["STEP_CHECK_UNKNOWN STEP-0001 مرّ_كلّه"]
    # حالةٌ سالبة: قفزٌ في الترقيم.
    row = "\t2026-10-18\tت\t111\ttafrat\n"
    _, errs = P.parse(H + "STEP-0001" + row + "STEP-0003" + row)
    assert errs == ["STEP_ORDER_BROKEN STEP-0003"]
    # ADR لا ملفَّ له.
    _, errs = P.parse(H + "STEP-0001\t2026-10-18\tت\t9999\ttafrat\n")
    assert errs == ["STEP_ADR_MISSING STEP-0001 9999"]


def test_message_by_hand() -> None:
    rows = {"STEP-0001": ["tafrat"]}
    assert P.message_errors("عنوان\n\nخطوة: STEP-0001\n", rows) == []
    assert P.message_errors("عنوانٌ بلا خطوة\n", rows) == ["STEP_UNDOCUMENTED"]
    assert P.message_errors("خطوة: STEP-0002\n", rows) == ["STEP_UNKNOWN STEP-0002"]


def _repo(tmp: Path) -> Path:
    def g(*a: str) -> None:
        subprocess.run(["git", *a], cwd=tmp, check=True, capture_output=True)
    tmp.mkdir(parents=True, exist_ok=True)
    g("init", "-q")
    g("config", "user.email", "t@t")
    g("config", "user.name", "t")
    g("commit", "-q", "--allow-empty", "-m", "أوّل")
    g("commit", "-q", "--allow-empty", "-m", "اعتماد\n\nخطوة: STEP-0001")
    return tmp


def test_git_path(tmp_path: Path) -> None:
    """الطريقُ عبر git: HEAD بخطوةٍ مسجَّلة يمرّ، وبلا خطوةٍ يُرفض، و--all يقف عند الاعتماد."""
    repo = _repo(tmp_path)
    log = H + "STEP-0001\t2026-10-18\tت\t111\ttafrat\n"
    errs, n, k = P.run(repo, log, False)
    assert (errs, n, k) == ([], 1, 1)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "بلا خطوة"], cwd=repo, check=True)
    errs, _, _ = P.run(repo, log, False)
    assert len(errs) == 1 and errs[0].startswith("STEP_UNDOCUMENTED")
    errs, _, k = P.run(repo, log, True)
    assert k == 2 and len(errs) == 1    # الإيداعُ الأوّل قبل الاعتماد لا يُفحص


def _shallow_refused(tmp_path: Path) -> bool:
    """شرطُ الضحل مكتوبًا مرّةً واحدة: لا إيداعَ مفحوص، والرفضُ باسمه لا مرور."""
    src = _repo(tmp_path / "src")
    dst = tmp_path / "dst"
    subprocess.run(["git", "clone", "-q", "--depth", "1", f"file://{src}", str(dst)], check=True)
    errs, _, k = P.run(dst, H + "STEP-0001\t2026-10-18\tت\t111\ttafrat\n", False)
    return k == 0 and errs == ["STEP_HISTORY_MISSING"]


def test_shallow_is_refused(tmp_path: Path) -> None:
    """استنساخٌ ضحل (STEP-0002)."""
    assert _shallow_refused(tmp_path)


def test_merge_commit(tmp_path: Path) -> None:
    """إيداعُ الدمج: في `pull_request` يُفحص رأسُ الفرع (الأبُ الثاني)، وفي `push` الدمجُ نفسُه."""
    repo = _repo(tmp_path)

    def g(*a: str) -> None:
        subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True)
    g("checkout", "-q", "-b", "far")
    g("commit", "-q", "--allow-empty", "-m", "فرعٌ بلا خطوة")
    g("checkout", "-q", "-")
    g("commit", "-q", "--allow-empty", "-m", "أصل\n\nخطوة: STEP-0001")
    g("merge", "-q", "--no-ff", "far", "-m", "دمج\n\nخطوة: STEP-0001")
    log = H + "STEP-0001\t2026-10-18\tت\t111\ttafrat\n"
    errs, _, _ = P.run(repo, log, False, "push")
    assert errs == []                       # رسالةُ الدمج نفسُه موثَّقة
    errs, _, _ = P.run(repo, log, False, "pull_request")
    assert len(errs) == 1 and errs[0].startswith("STEP_UNDOCUMENTED")   # رأسُ الفرع لا خطوةَ فيه
    # دمجُ المالك بزرّ GitHub: رسالتُه بلا خطوة، ورأسُ الفرع بخطوة — يُقبل في push.
    g("checkout", "-q", "-b", "far2")
    g("commit", "-q", "--allow-empty", "-m", "فرعٌ\n\nخطوة: STEP-0001")
    g("checkout", "-q", "-")
    g("commit", "-q", "--allow-empty", "-m", "أصلٌ ثانٍ\n\nخطوة: STEP-0001")
    g("merge", "-q", "--no-ff", "far2", "-m", "Merge pull request #1 from x/far2")
    assert P.run(repo, log, False, "push")[0] == []
    # ولا خطوةَ في الدمج ولا في رأس الفرع: يُرفض.
    g("checkout", "-q", "-b", "far3")
    g("commit", "-q", "--allow-empty", "-m", "بلا خطوة")
    g("checkout", "-q", "-")
    g("commit", "-q", "--allow-empty", "-m", "أصلٌ ثالث\n\nخطوة: STEP-0001")
    g("merge", "-q", "--no-ff", "far3", "-m", "Merge pull request #2 from x/far3")
    errs = P.run(repo, log, False, "push")[0]
    assert len(errs) == 1 and errs[0].startswith("STEP_UNDOCUMENTED")


def test_adoption_missing(tmp_path: Path) -> None:
    repo = tmp_path / "r"
    repo.mkdir()
    for a in (("init", "-q"), ("config", "user.email", "t@t"), ("config", "user.name", "t"),
              ("commit", "-q", "--allow-empty", "-m", "جذرٌ بلا خطوة")):
        subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True)
    log = H + "STEP-0001\t2026-10-18\tت\t111\ttafrat\n"
    errs, _, k = P.run(repo, log, True)
    assert k == 0 and errs == ["STEP_ADOPTION_MISSING STEP-0001"]
    errs, _, k = P.run(repo, log, False)      # الجذرُ نفسُه يُفحص، لا يُعدّ ضحلًا
    assert k == 1 and errs[0].startswith("STEP_UNDOCUMENTED")


def test_mutant_shallow_passes(tmp_path: Path, monkeypatch: Any) -> None:
    """طفرةٌ دائمة (لا «في الجلسة»): `checked_commit` يعيد HEAD في الضحل فيمرّ بلا رفض؛
    فشرطُ `test_shallow_is_refused` يسقط عليها."""
    monkeypatch.setattr(P, "checked_commit",
                        lambda repo, event: [P.git(repo, "rev-parse", "HEAD").strip()])
    assert not _shallow_refused(tmp_path)


def test_gen_check_names() -> None:
    _, errs = P.parse(H + "STEP-0001\t2026-10-18\tت\t111\tgen:lane;gen:naql\n")
    assert errs == []
    for bad in ("gen:لا_مولّد", "gen:protocol"):     # لا مولِّد، أو يكرّر اسمًا مغلقًا
        _, errs = P.parse(H + f"STEP-0001\t2026-10-18\tت\t111\t{bad}\n")
        assert errs == [f"STEP_CHECK_UNKNOWN STEP-0001 {bad}"]


def test_deposited_log() -> None:
    rows, errs = P.parse((ROOT / "docs/protocol/khutuwat.tsv").read_text(encoding="utf-8"))
    assert errs == [] and "STEP-0001" in rows
    assert P.ADOPTION == "STEP-0001"


def test_tafrat_registry() -> None:
    rows = json.loads((ROOT / "docs/tafrat.json").read_text(encoding="utf-8"))
    assert T.validate(rows) == []
    assert len({r["ism"] for r in rows}) == len(rows) >= 10
    # حالتان سالبتان (MUTANT_NAME_DUPLICATED، MUTANT_TEXT_NOT_UNIQUE):
    # اسمٌ مكرّر، ونصٌّ يقع أكثر من مرّة.
    bad = [dict(rows[0]), dict(rows[0], min="theorem", ila="lemma")]
    errs = T.validate(bad)
    assert f"MUTANT_NAME_DUPLICATED {rows[0]['ism']}" in errs
    assert any(e.startswith(f"MUTANT_TEXT_NOT_UNIQUE {rows[0]['ism']}") for e in errs)


def test_constitution_part_four() -> None:
    for n in ("١٨", "١٩", "٢٠", "٢١", "٢٢", "٢٣", "٢٤"):
        assert f"## المادّة {n} —" in CONST, n
    for v in ("PROTOCOL_BYPASSED", "STEP_UNDOCUMENTED", "MUTANT_NOT_IN_CI",
              "ABSENCE_WITHOUT_SEARCH", "QUOTE_NOT_VERBATIM", "BUILDER_CHOICE_UNDECLARED",
              "COVERAGE_AS_ACCURACY",
              "MAFHUM_USUL_AS_MARTABA"):
        assert f"`{v}`" in CONST, v
    words = ("موافق على الخطة وان تكون بروتوكول جزء من الدستور وان تكون حاكمة لكل مدخلات"
             " ومخرجات المستودعات وان توثق كل خطوة")
    assert f"«{words}»" in CONST
