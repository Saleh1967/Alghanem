"""بوّابةُ التوليد الواحدة: كلُّ رقمٍ منقولٍ يُعاد اشتقاقُه ثمّ يُصادَم.

كانت الأرقامُ المنقولةُ في هذه الشجرة تُصادَم بمصادماتٍ مبعثرة: كلُّ وحدةٍ
تحمل ثابتَها المؤرَّخ (`*_AT_MEASUREMENT`) وكاشفَها (`*_have_drifted`)،
واختبارٌ أو اختباران يمرّان عليهما. فما لم يُكتَب له كاشفٌ بقي في النثر بلا
حارس، وانزاح صامتًا مع نموّ الشجرة. وليست العلّةُ في التجميد نفسِه — فالتجميدُ
معقِلٌ سليم — بل في أن يبقى الرقمُ **مجمَّدًا بلا مولِّدٍ يقابله**.

وهذه الوحدةُ **لا تحمل نسخةً ثانيةً من أيّ رقم**، ولا تصلح أن تكون سجلَّ
أختام: النقلُ يبقى حيث هو مكتوب — ثابتًا في وحدته أو سطرًا في نثرها — ويبقى
المولِّدُ حيث هو مُعرَّف؛ وكلُّ ما ههنا أن يُجمَع الجانبان في مقامٍ واحد
فيُصادما، ويُسمّى الفارقُ باسم حقلِه لا بـ`assert` صامت.

وتُفرَّق الأرقامُ ههنا ثلاثةَ أجناس، ولا يُخلَط جنسٌ بجنس::

    AGeneratedFigure   != ATranscribedFigure   != AQuotedWitness

* **[بوابة]** — رقمٌ له ثابتٌ منقولٌ ومولِّدٌ حيّ: يُصادَم حقلًا حقلًا،
  وفارقُه يُسقِط البوّابة.
* **[نثر]** — رقمٌ يولَّد حيًّا ويُنقَل إلى نثرٍ بشريّ: يُطلَب حضورُ صورته
  المولَّدة في ذلك النثر بعينه، فغيابُها انزياحُ نثرٍ لا انزياحُ قياس.
* **[شاهد]** — رقمٌ وارِدٌ من خارجٍ لا مولِّدَ له عندنا: يُعلَن بمصدره
  و**لا يُصادَم**، إذ ليس ادّعاءً لهذه الشجرة حتى يُحاسَب حسابَها.

والاستعمال::

    python tools/regen_all.py            # يُعرَض كلُّ رقمٍ بجنسه ومصدره
    python tools/regen_all.py --check    # يُصادَم، ويُخرِج 1 عند أوّل فارق

وما أُضيف إلى الشجرة من أرقامٍ بعد اليوم يدخل من هذا الباب أو لا يدخل.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, fields, is_dataclass
from hashlib import sha256
from pathlib import Path
from typing import Final

REPO_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
SRC_ROOT: Final[Path] = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from alghanem.arabic import hamil_audit_second_reading as second_reading  # noqa: E402
from alghanem.arabic import hamil_phase1_audit_deposit as phase1  # noqa: E402
from alghanem.arabic import letter_haraka_partition as partition  # noqa: E402
from alghanem.arabic import pair_sample_widening as widening  # noqa: E402
from alghanem.arabic import quran_corpus_word_total as word_total  # noqa: E402
from alghanem.program import project_state  # noqa: E402

GATE: Final[str] = "[بوابة]"
PROSE: Final[str] = "[نثر]"
WITNESS: Final[str] = "[شاهد]"


class RegenerationError(RuntimeError):
    """خللٌ في البوّابة نفسِها، لا في رقمٍ تحرسه."""


@dataclass(frozen=True)
class FieldReading:
    """حقلٌ واحد: ما نُقل، وما وَلَّده القرصُ الآن."""

    field: str
    transcribed: str
    measured: str

    @property
    def agrees(self) -> bool:
        return self.transcribed == self.measured


@dataclass(frozen=True)
class FigureReport:
    """رقمٌ مسمًّى بجنسه ومصدره وحقولِه المصادَمة."""

    figure: str
    genus: str
    source: str
    readings: tuple[FieldReading, ...]

    def __post_init__(self) -> None:
        if self.genus not in {GATE, PROSE, WITNESS}:
            raise RegenerationError(f"جنسٌ غيرُ معلَن: {self.genus}")
        if self.genus is not WITNESS and not self.readings:
            raise RegenerationError(f"بوّابةٌ بلا حقلٍ تحرسه: {self.figure}")

    @property
    def discrepancies(self) -> tuple[FieldReading, ...]:
        if self.genus == WITNESS:
            return ()
        return tuple(reading for reading in self.readings if not reading.agrees)


def _named_fields(deposit: object) -> Mapping[str, object]:
    """حقولُ وديعةٍ مجمَّدةٍ بأسمائها، سواءٌ حملت __dict__ أو __slots__."""

    if not is_dataclass(deposit) or isinstance(deposit, type):
        raise RegenerationError("لا تُقرأ حقولُ ما ليس وديعةً مجمَّدة.")
    return {field.name: getattr(deposit, field.name) for field in fields(deposit)}


def _collide(
    figure: str,
    source: str,
    transcribed: Mapping[str, object],
    measured: Mapping[str, object],
) -> FigureReport:
    """يُصادِم ثابتًا منقولًا بمولِّدِه حقلًا حقلًا، فلا يمرّ فارقٌ بلا اسم."""

    if set(transcribed) != set(measured):
        raise RegenerationError(f"حقولُ المنقول والمقيس لا تتطابق في {figure}")
    return FigureReport(
        figure=figure,
        genus=GATE,
        source=source,
        readings=tuple(
            FieldReading(
                field=field,
                transcribed=str(transcribed[field]),
                measured=str(measured[field]),
            )
            for field in sorted(transcribed)
        ),
    )


def _appears_in(
    figure: str,
    prose_paths: Mapping[str, Path],
    renderings: Mapping[str, str],
) -> FigureReport:
    """يطلب حضورَ صورةِ الرقم المولَّد في النثر الذي ينقله، حرفًا بحرف."""

    texts = {
        name: path.read_text(encoding="utf-8") for name, path in prose_paths.items()
    }
    readings: list[FieldReading] = []
    for field in sorted(renderings):
        rendering = renderings[field]
        for name, text in texts.items():
            present = rendering in text
            readings.append(
                FieldReading(
                    field=f"{field} @ {name}",
                    transcribed=rendering if present else "غائبٌ عن النثر",
                    measured=rendering,
                )
            )
    return FigureReport(
        figure=figure,
        genus=PROSE,
        source=" · ".join(sorted(prose_paths)),
        readings=tuple(readings),
    )


def _prose_scope() -> FigureReport:
    return _collide(
        figure="pair_sample_widening.prose_scope",
        source="PROSE_SCOPE_AT_MEASUREMENT ↔ prose_scope_fingerprint()",
        transcribed=_named_fields(widening.PROSE_SCOPE_AT_MEASUREMENT),
        measured=_named_fields(widening.prose_scope_fingerprint()),
    )


def _third_rung() -> FigureReport:
    return _collide(
        figure="pair_sample_widening.third_rung",
        source="THE_THIRD_RUNG_AT_MEASUREMENT ↔ third_rung_figures()",
        transcribed=_named_fields(widening.THE_THIRD_RUNG_AT_MEASUREMENT),
        measured=_named_fields(widening.third_rung_figures()),
    )


def _third_rung_in_prose() -> FigureReport:
    figures = widening.third_rung_figures()
    return _appears_in(
        figure="pair_sample_widening.third_rung ← النثر",
        prose_paths={"README.md": REPO_ROOT / "README.md"},
        renderings={
            "total_pairs": f"{figures.total_pairs:,}",
            "tanwin_initial_in_prose": f"{figures.tanwin_initial_in_prose:,}",
            "prose_pairs": f"{figures.prose_pairs:,}",
        },
    )


def _audit_corpus_counts() -> FigureReport:
    return _collide(
        figure="hamil_audit_second_reading.counts",
        source="THE_COUNTS_AT_MEASUREMENT ↔ measure_the_audit_corpus()",
        transcribed=_named_fields(second_reading.THE_COUNTS_AT_MEASUREMENT),
        measured=_named_fields(second_reading.measure_the_audit_corpus()),
    )


def _partition_ladder() -> FigureReport:
    """جدولُ الدرجات كما تكتبه الوحدةُ في جدولِ نثرها: خلايا · وقوعات · حروف."""

    renderings: dict[str, str] = {}
    for rung in partition.SourceRung:
        census = partition.table_census(rung)
        key = rung.name.lower()
        renderings[f"{key}.realized"] = f"{census.realized_cells}/112"
        renderings[f"{key}.occurrences"] = f"{census.occurrences:,}"
        renderings[f"{key}.letters"] = f"{census.letters_present}/28"
    return _appears_in(
        figure="letter_haraka_partition.ladder",
        prose_paths={"letter_haraka_partition.py": Path(partition.__file__)},
        renderings=renderings,
    )


def _partition_ladder_in_readme() -> FigureReport:
    """ونثرُ README يكتب الوقوعاتِ وحدَها برقمها، فهي وحدَها تُطلَب فيه."""

    census = partition.table_census(partition.SourceRung.WITH_PROSE)
    return _appears_in(
        figure="letter_haraka_partition.ladder ← README",
        prose_paths={"README.md": REPO_ROOT / "README.md"},
        renderings={"with_prose.occurrences": f"{census.occurrences:,}"},
    )


def _partition_margins() -> FigureReport:
    renderings: dict[str, str] = {}
    for absence in partition.absent_cells():
        key = f"{absence.letter}{absence.haraka}"
        renderings[f"{key}.expected"] = f"{absence.expected:.3f}"
        renderings[f"{key}.probability_of_zero"] = f"{absence.probability_of_zero:.3f}"
    return _appears_in(
        figure="letter_haraka_partition.margins",
        prose_paths={"letter_haraka_partition.py": Path(partition.__file__)},
        renderings=renderings,
    )


def _partition_sukun_share() -> FigureReport:
    counts = partition.cell_counts(partition.SourceRung.WITH_PROSE)
    sukun = "\u0652"
    occurrences = sum(counts.values())
    if occurrences < 1:
        raise RegenerationError("جدولٌ خالٍ لا تُقاس منه حصّة.")
    bearing = sum(value for (_, haraka), value in counts.items() if haraka == sukun)
    return _appears_in(
        figure="letter_haraka_partition.sukun_share",
        prose_paths={
            "letter_haraka_partition.py": Path(partition.__file__),
            "README.md": REPO_ROOT / "README.md",
        },
        renderings={
            "bearing": f"{bearing:,}",
            "share": f"{100 * bearing / occurrences:.2f}%",
        },
    )


def _phase1_tally() -> FigureReport:
    checks = phase1.THE_CHECKS
    agrees = sum(1 for check in checks if check.verdict is phase1.CheckVerdict.AGREES)
    contradicts = sum(
        1 for check in checks if check.verdict is phase1.CheckVerdict.CONTRADICTS
    )
    not_checkable = len(checks) - agrees - contradicts
    cross = len(
        [
            check
            for check in checks
            if check.genus
            is phase1.CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION
        ]
    )
    live = {
        "checks": len(checks),
        "agrees": agrees,
        "contradicts": contradicts,
        "not_checkable_here": not_checkable,
        "independent_cross_checks": cross,
    }
    return _collide(
        figure="hamil_phase1_audit_deposit.tally",
        source="THE_CHECKS ↔ حكمٌ مشتقٌّ عند كلّ استيراد (لا حقلَ حكمٍ يُكتَب)",
        transcribed=live,
        measured=live,
    )


def _quoted_word_total() -> FigureReport:
    return FigureReport(
        figure="quran_corpus_word_total.THE_QUOTED_WORD_TOTAL",
        genus=WITNESS,
        source="نقلٌ خارجيّ عن tanzil؛ منزلتُه تُقرَأ بـrun_quoted_total_survey",
        readings=(
            FieldReading(
                field="quoted_word_total",
                transcribed=f"{word_total.THE_QUOTED_WORD_TOTAL:,}",
                measured="لا يولَّد ههنا؛ شاهدٌ لا بوّابة",
            ),
        ),
    )


def _quoted_on_rate() -> FigureReport:
    return FigureReport(
        figure="hamil_phase1_audit_deposit._QUOTED_ON_RATE",
        genus=WITNESS,
        source="نقلٌ عن hamil نقضَه الحسابُ ههنا؛ شاهدُ اتّهامٍ لا رقمَ عمل",
        readings=(
            FieldReading(
                field="quoted_on_rate",
                transcribed=f"{phase1._QUOTED_ON_RATE}",
                measured="مناقَضٌ بالحساب؛ لا يُصادَم صِدامَ بوّابة",
            ),
        ),
    )


def _state_block_fields(block: str) -> dict[str, str]:
    """يفكّ كتلةَ الحال إلى صفوفٍ مسمّاة، وبصمةٍ لما ليس صفًّا.

    ولولا التفكيكُ لَطُبعت الكتلةُ كلُّها عند أوّل فارق، فضاع اسمُ الحقل
    المنزاح في سطورٍ متّفقة.
    """

    rows: dict[str, str] = {}
    other: list[str] = []
    for line in block.splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) == 2 and not set(cells[0]) <= {"-"}:
            rows[cells[0]] = cells[1]
        else:
            other.append(line)
    digest = sha256("\n".join(other).encode("utf-8")).hexdigest()[:12]
    rows["نثرُ الكتلة (بصمة)"] = digest
    return rows


def _vision_state_block() -> FigureReport:
    """كتلةُ حالِ المشروع في `docs/VISION.md`: مرسومةٌ من الشجرة لا مكتوبةٌ فيها."""

    document = project_state.vision_document_path().read_text(encoding="utf-8")
    return _collide(
        figure="program.project_state.vision_block",
        source="docs/VISION.md ↔ render_state_block(derive_project_state())",
        transcribed=_state_block_fields(
            project_state.read_document_state_block(document)
        ),
        measured=_state_block_fields(
            project_state.render_state_block(project_state.derive_project_state())
        ),
    )


def the_registry() -> tuple[FigureReport, ...]:
    """كلُّ رقمٍ محروسٍ في الشجرة، مولَّدًا عند كلّ نداء ولا يُخزَن."""

    return (
        _prose_scope(),
        _third_rung(),
        _third_rung_in_prose(),
        _audit_corpus_counts(),
        _partition_ladder(),
        _partition_ladder_in_readme(),
        _partition_margins(),
        _partition_sukun_share(),
        _phase1_tally(),
        _vision_state_block(),
        _quoted_word_total(),
        _quoted_on_rate(),
    )


def render(reports: tuple[FigureReport, ...]) -> Iterator[str]:
    """يعرض كلَّ رقمٍ بجنسه، ويُسمّي كلَّ فارقٍ بحقلِه."""

    for report in reports:
        marks = "✓" if not report.discrepancies else "✗"
        yield f"{marks} {report.genus} {report.figure}"
        yield f"    المصدر: {report.source}"
        for reading in report.readings:
            if report.genus == WITNESS:
                yield f"    {reading.field}: {reading.transcribed} — {reading.measured}"
            elif reading.agrees:
                yield f"    {reading.field}: {reading.measured}"
            else:
                yield (
                    f"    {reading.field}: المنقولُ {reading.transcribed} "
                    f"≠ المولَّدُ {reading.measured}"
                )
        yield ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="يُخرِج 1 إن انزاح رقمٌ منقولٌ عمّا يولِّده القرصُ الآن",
    )
    args = parser.parse_args(argv)

    reports = the_registry()
    for line in render(reports):
        print(line)

    drifted = tuple(report for report in reports if report.discrepancies)
    if not drifted:
        print("لا انزياح: كلُّ رقمٍ محروسٍ نابضٌ بمولِّدِه.")
        return 0

    print("انزياحٌ مسمًّى — ولا يُقبَل رقمٌ بلا فاتورةٍ تُعرَض في رسالة الالتزام:")
    for report in drifted:
        for reading in report.discrepancies:
            print(
                f"  {report.figure} · {reading.field}: "
                f"{reading.transcribed} → {reading.measured}"
            )
    return 1 if args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
