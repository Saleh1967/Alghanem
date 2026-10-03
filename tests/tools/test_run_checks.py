"""اختباراتُ قبولِ مُشغِّل الفحوص: يفشل الجامعُ بفشلِ فرده، ولا يُقرأ تخطٍّ نجاحًا."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = REPO_ROOT / "tools" / "run_checks.sh"
MANIFEST = REPO_ROOT / "tools" / "checks.tsv"


def _run(
    tmp_path: Path, manifest: str, *flags: str, env: dict[str, str] | None = None
) -> tuple[subprocess.CompletedProcess[str], dict[str, tuple[str, str]]]:
    """يُشغَّل المُشغِّلُ على مانيفستٍ مُعطًى، وتُعاد خلاصتُه مقروءةً بالاسم."""

    manifest_path = tmp_path / "checks.tsv"
    manifest_path.write_text(manifest, encoding="utf-8")
    logs = tmp_path / "logs"
    environment = dict(os.environ)
    environment.pop("ALGHANEM_CHECK_LOGS", None)
    if env is not None:
        environment.update(env)
    completed = subprocess.run(
        [
            "bash",
            str(RUNNER),
            "--manifest",
            str(manifest_path),
            "--logs",
            str(logs),
            *flags,
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=environment,
    )
    summary: dict[str, tuple[str, str]] = {}
    summary_path = logs / "summary.tsv"
    if summary_path.exists():
        rows = summary_path.read_text(encoding="utf-8").splitlines()[1:]
        for row in rows:
            fields = row.split("\t")
            summary[fields[0]] = (fields[1], fields[2])
    return completed, summary


def test_the_shipped_manifest_lists_the_checks_ci_must_run() -> None:
    """المانيفستُ المُودَعُ هو قائمةُ الفحوص، ومنها حزمةُ canonical116 صراحةً."""

    listed = subprocess.run(
        ["bash", str(RUNNER), "--list"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=True,
    ).stdout.split()
    assert listed == [
        "external-witness",
        "regen-all",
        "deposit-law",
        "pytest",
        "canonical116",
        "daleel",
        "hifz",
        "ruff-check",
        "ruff-format",
        "mypy",
    ]
    assert "unittest discover -s canonical116" in MANIFEST.read_text(encoding="utf-8")


def test_one_failing_check_fails_the_gathering_command(tmp_path: Path) -> None:
    """فحصٌ يفشل عمدًا يجعل الأمرَ الجامعَ يفشل، ويُسجَّل رمزُ خروجه كما هو."""

    completed, summary = _run(
        tmp_path,
        "green\t-\ttrue\nred\t-\texit 3\n",
    )
    assert completed.returncode == 1
    assert summary["green"] == ("PASS", "0")
    assert summary["red"] == ("FAIL", "3")


def test_a_failure_before_the_tee_is_not_swallowed(tmp_path: Path) -> None:
    """فشلُ أمرٍ قبل tee لا يُبتلع: الأنبوبُ يُقرأ بـpipefail لا برمز آخره."""

    completed, summary = _run(tmp_path, "piped\t-\tfalse | cat\n")
    assert completed.returncode == 1
    assert summary["piped"][0] == "FAIL"


def test_an_unreached_check_is_not_run_and_is_never_a_pass(tmp_path: Path) -> None:
    """الفحصُ غيرُ المشغَّل يظهر NOT_RUN، فلا يُنسَب إليه نجاحٌ لم يُقَس."""

    completed, summary = _run(
        tmp_path,
        "red\t-\tfalse\nlater\t-\ttrue\n",
        "--fail-fast",
    )
    assert completed.returncode == 1
    assert summary["red"][0] == "FAIL"
    assert summary["later"][0] == "NOT_RUN"


def test_a_missing_source_is_skipped_with_its_reason(tmp_path: Path) -> None:
    """غيابُ المصدر المطلوب يُسجَّل SKIPPED بسببه، و--strict يرفضه خروجًا."""

    manifest = "witness\tALGHANEM_ABSENT_SOURCE\ttrue\n"
    lenient, summary = _run(tmp_path, manifest)
    assert lenient.returncode == 0
    assert summary["witness"][0] == "SKIPPED"
    assert "ALGHANEM_ABSENT_SOURCE" in lenient.stdout

    strict, strict_summary = _run(tmp_path, manifest, "--strict")
    assert strict.returncode == 1
    assert strict_summary["witness"][0] == "SKIPPED"


def test_the_logs_carry_the_revision_they_were_measured_on(tmp_path: Path) -> None:
    """السجلُّ مربوطٌ بنسخته: الـSHA وحالةُ الشجرة وبصمةُ اليونيكود مُودَعةٌ معه."""

    completed, _ = _run(tmp_path, "green\t-\techo hello\n")
    assert completed.returncode == 0
    environment = (tmp_path / "logs" / "environment.txt").read_text(encoding="utf-8")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=True,
    ).stdout.strip()
    assert f"head_sha: {head}" in environment
    assert "tree_is_clean:" in environment
    assert "unicodedata:" in environment
    assert (tmp_path / "logs" / "green.log").read_text(encoding="utf-8") == "hello\n"
