"""بوّابةُ التوليد الواحدة: كلُّ رقمٍ محروسٍ يُعاد اشتقاقُه ثمّ يُصادَم.

كانت الأرقامُ المنقولةُ في هذه الشجرة تُصادَم بمصادماتٍ مبعثرة: كلُّ وحدةٍ
تحمل ثابتَها المؤرَّخ (`*_AT_MEASUREMENT`) وكاشفَها (`*_have_drifted`)،
واختبارٌ أو اختباران يمرّان عليهما. فما لم يُكتَب له كاشفٌ بقي في النثر بلا
حارس، وانزاح صامتًا مع نموّ الشجرة — كما وقع فعلًا لأرقام
`letter_haraka_partition`.

وهذا الملفُّ **وصلةٌ لا سجلّ**: المفردات كلُّها في `alghanem.seals`، والقيمُ
كلُّها باقيةٌ حيث كُتبت، وما ههنا إلّا وصلُ كلِّ رقمٍ بمولِّده في ختمٍ واحد.
ولا يحمل هذا الملفُّ نسخةً ثانيةً من أيّ رقم، وإلّا لصار هو القبرَ الذي جاء
يفتحه.

والاستعمال::

    python tools/regen_all.py            # يُعرَض كلُّ ختمٍ بجنسه ومصدره
    python tools/regen_all.py --check    # يُصادَم، ويُخرِج 1 عند أوّل انزياح

وما أُضيف إلى الشجرة من أرقامٍ بعد اليوم يدخل من هذا الباب أو لا يدخل.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator, Mapping
from dataclasses import fields, is_dataclass
from hashlib import sha256
from pathlib import Path
from typing import Final

REPO_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
SRC_ROOT: Final[Path] = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from alghanem.arabic import hamil_audit_second_reading as second_reading  # noqa: E402
from alghanem.arabic import hamil_phase1_audit_deposit as phase1  # noqa: E402
from alghanem.arabic import hamil_phase2_audit_deposit as phase2  # noqa: E402
from alghanem.arabic import letter_haraka_partition as partition  # noqa: E402
from alghanem.arabic import methodological_sources as sources  # noqa: E402
from alghanem.arabic import owner_licensed_deposit as owner_deposit  # noqa: E402
from alghanem.arabic import pair_sample_widening as widening  # noqa: E402
from alghanem.arabic import quran_corpus_word_total as word_total  # noqa: E402
from alghanem.program import project_state  # noqa: E402
from alghanem.seals import (  # noqa: E402
    Seal,
    SealError,
    SealGenus,
    SealRegistry,
    SealVerdict,
)

SUKUN: Final[str] = "\u0652"

USOOL_DOCUMENT: Final[Path] = REPO_ROOT / "docs" / "USOOL_AL-UNBOOB.md"

_USOOL_DOOR: Final[re.Pattern[str]] = re.compile(
    r"^## (?P<title>.+)\n\n> \*\*موضعُه في الشجرة:\*\* `(?P<site>[^`]+)`",
    re.MULTILINE,
)


def _named_fields(deposit: object) -> dict[str, str]:
    """حقولُ وديعةٍ مجمَّدةٍ بأسمائها، سواءٌ حملت __dict__ أو __slots__."""

    if not is_dataclass(deposit) or isinstance(deposit, type):
        raise SealError("لا تُقرأ حقولُ ما ليس وديعةً مجمَّدة.")
    return {field.name: str(getattr(deposit, field.name)) for field in fields(deposit)}


def _presence(prose: Path, renderings: Mapping[str, str]) -> dict[str, str]:
    """حضورُ صورةِ الرقم المولَّد في نثرٍ مُسمًّى، حرفًا بحرف لا تقريبًا."""

    text = prose.read_text(encoding="utf-8")
    return {
        field: rendering if rendering in text else "غائبٌ عن النثر"
        for field, rendering in renderings.items()
    }


def _prose_seal(
    name: str,
    origin: str,
    prose: Path,
    measure: object,
) -> Seal:
    """ختمُ نثر: المولَّدُ يُقاس الآن، والمنقولُ حضورُ صورته في ذلك النثر."""

    if not callable(measure):
        raise SealError("مولِّدُ ختمِ النثر يُستدعى عند كلّ مصادمة.")

    def generate() -> Mapping[str, str]:
        return dict(measure())

    def transcription() -> Mapping[str, str]:
        return _presence(prose, dict(measure()))

    return Seal(
        name=name,
        genus=SealGenus.TRANSCRIBED,
        origin=origin,
        generate=generate,
        transcription=transcription,
    )


def _third_rung_renderings() -> Mapping[str, str]:
    figures = widening.third_rung_figures()
    return {
        "total_pairs": f"{figures.total_pairs:,}",
        "tanwin_initial_in_prose": f"{figures.tanwin_initial_in_prose:,}",
        "prose_pairs": f"{figures.prose_pairs:,}",
    }


def _widening_prose_renderings() -> Mapping[str, str]:
    """أرقامُ نثر `pair_sample_widening` نفسِه: سُلَّمُه وجُرفُه وقاعُه."""

    ladder = widening.the_widening_ladder()
    figures = widening.third_rung_figures()
    cliff = widening.the_cliff_factor()
    tail = widening.the_tail_occurrences_now()
    leader = ladder[2].leaders[0].occurrences
    renderings = {
        "fold": f"**{figures.total_pairs // ladder[1].total_pairs} ضعفًا**",
        "third_rung.row": (
            f"| + نثر الشجرة | {figures.total_pairs:,} | "
            f"{figures.realized}/36 | فتحة+شدّة ({leader:,}) |"
        ),
        "cliff.share": (
            f"{figures.shadda_bearing:,} من {figures.total_pairs:,} — أي "
            f"**{100 * figures.shadda_bearing / figures.total_pairs:.3f}%**"
        ),
        "cliff.factor": (
            f"وبين {cliff.lightest_shadda_bearing:,} و"
            f"{cliff.heaviest_without_shadda} عاملُ {cliff.factor} "
            "بالقسمة الأرضية"
        ),
        "tail.total": f"**{sum(count for _, count in tail)}** وقوعًا",
        "register.tanwin": (
            f"**{figures.tanwin_initial_in_prose:,}** من "
            f"{figures.prose_pairs:,} في النثر — أي "
            f"{100 * figures.tanwin_initial_in_prose / figures.prose_pairs:.3f}%"
        ),
    }
    for pair, count in tail:
        key = "+".join(f"U+{ord(mark):04X}" for mark in pair)
        renderings[f"tail.{key}"] = f"({count})"
    return renderings


def _phase2_tally() -> Mapping[str, str]:
    """حصيلةُ الجولة الثانية، مولَّدةً من البايتات المُودَعة عند كلّ نداء."""

    return {key: str(value) for key, value in phase2.verdict_tally().items()}


def _hamil_register_tally() -> Mapping[str, str]:
    """تعدادُ سجلّ أختامهم، مشتقًّا من قائمته لا منقولًا عن حقوله."""

    return {key: str(value) for key, value in phase2.register_tally().items()}


def _usool_doors() -> Mapping[str, str]:
    """الجانبُ الحيُّ لوثيقة الأصول: بصمتُها، وأبوابُها، ومواضعُ تلك الأبواب.

    وهي **شاهدٌ معرفيٌّ لا رقم**: لا يُنقَل منها مقدارٌ إلى حساب، ولا تُصادَم
    مصادمةَ المولَّد. والحيُّ فيها موضعُ كلّ باب: يُفتَح على القرص عند كلّ
    قراءة، فإن زال بابٌ أو انتقل موضعُه انكشف حالًا ولم يبقَ نثرًا يدّعي.

    وثلاثةٌ تُعرَف عن هذا الختم لئلّا يُتوهَّم فيه ما ليس فيه:

    * **الحارسُ على الأبواب اختبارُها لا هذا الختم.** جنسُ الشاهد المعرفيّ
      يُرجع فارقًا فارغًا دائمًا؛ فلو زال موضعُ بابٍ لكُتب في الطيّة «موضعٌ
      غائبٌ عن الشجرة» ومرّت البوّابةُ خضراء. الذي يُسقِط CI هو
      `tests/tools/test_usool_al_unboob.py`، وحذفُه يفتح البابَ صامتًا.
    * **الجانبان دالّةٌ واحدة**، وذلك موافقٌ للجنس إذ لا يُصادَم أصلًا. فإن
      رُقِّي الجنسُ يومًا إلى المولَّد صار الختمُ أخضرَ لغوًا: يُصادَم
      الجانبُ بنفسه. فترقيةُ الجنس تقتضي جانبًا ثانيًا حقيقيًّا.
    * **العددُ المجمَّدُ في الاختبار يمنع البلع.** النمطُ يشترط سطرَ الموضع
      لاصقًا بالعنوان؛ فبابٌ يُكتَب بصيغةٍ مغايرةٍ يسقط من الطيّة صامتًا،
      ولا يكشفه إلّا تجميدُ عدد الأبواب.
    """

    text = USOOL_DOCUMENT.read_text(encoding="utf-8")
    doors = tuple(
        (match.group("title"), match.group("site"))
        for match in _USOOL_DOOR.finditer(text)
    )
    if not doors:
        raise SealError("وثيقةُ أصولٍ بلا بابٍ يُسمّي موضعَه لا تُحرَس.")
    fold: dict[str, str] = {
        "بصمةُ الوثيقة": sha256(text.encode("utf-8")).hexdigest()[:12],
        "الأبوابُ المقروءة": str(len(doors)),
    }
    for title, site in doors:
        fold[f"باب: {title}"] = (
            site if (REPO_ROOT / site).is_file() else "موضعٌ غائبٌ عن الشجرة"
        )
    return fold


def _methodological_sources_sides() -> Mapping[str, str]:
    """الجانبُ الحيُّ لمصدرٍ منهجيّ: حضورُ ذكره في وحدة بابه النافذ."""

    doors = sources.doors_by_standing()
    absent = sources.missing_citations()
    fold = {
        f"باب: {dotted}": ("غائبٌ ذكرُ مصدره" if dotted in absent else marker)
        for dotted, marker in sources.citation_sites()
    }
    for standing, names in doors.items():
        fold[standing.value] = " · ".join(names) if names else "لا باب"
    return fold


def _partition_ladder_renderings() -> Mapping[str, str]:
    renderings: dict[str, str] = {}
    for rung in partition.SourceRung:
        census = partition.table_census(rung)
        key = rung.name.lower()
        renderings[f"{key}.realized"] = f"{census.realized_cells}/112"
        renderings[f"{key}.occurrences"] = f"{census.occurrences:,}"
        renderings[f"{key}.letters"] = f"{census.letters_present}/28"
    return renderings


def _partition_occurrences_rendering() -> Mapping[str, str]:
    census = partition.table_census(partition.SourceRung.WITH_PROSE)
    return {"with_prose.occurrences": f"{census.occurrences:,}"}


def _partition_margin_renderings() -> Mapping[str, str]:
    renderings: dict[str, str] = {}
    for absence in partition.absent_cells():
        key = f"{absence.letter}{absence.haraka}"
        renderings[f"{key}.expected"] = f"{absence.expected:.3f}"
        renderings[f"{key}.probability_of_zero"] = f"{absence.probability_of_zero:.3f}"
    return renderings


def _sukun_share_renderings() -> Mapping[str, str]:
    counts = partition.cell_counts(partition.SourceRung.WITH_PROSE)
    occurrences = sum(counts.values())
    if occurrences < 1:
        raise SealError("جدولٌ خالٍ لا تُقاس منه حصّة.")
    bearing = sum(value for (_, haraka), value in counts.items() if haraka == SUKUN)
    return {
        "bearing": f"{bearing:,}",
        "share": f"{100 * bearing / occurrences:.2f}%",
    }


def _phase1_tally() -> Mapping[str, str]:
    checks = phase1.THE_CHECKS
    agrees = sum(1 for check in checks if check.verdict is phase1.CheckVerdict.AGREES)
    contradicts = sum(
        1 for check in checks if check.verdict is phase1.CheckVerdict.CONTRADICTS
    )
    cross = sum(
        1
        for check in checks
        if check.genus is phase1.CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION
    )
    return {
        "checks": str(len(checks)),
        "agrees": str(agrees),
        "contradicts": str(contradicts),
        "not_checkable_here": str(len(checks) - agrees - contradicts),
        "independent_cross_checks": str(cross),
    }


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
    rows["نثرُ الكتلة (بصمة)"] = sha256("\n".join(other).encode("utf-8")).hexdigest()[
        :12
    ]
    return rows


def _vision_block_transcribed() -> Mapping[str, str]:
    document = project_state.vision_document_path().read_text(encoding="utf-8")
    return _state_block_fields(project_state.read_document_state_block(document))


def _vision_block_measured() -> Mapping[str, str]:
    return _state_block_fields(
        project_state.render_state_block(project_state.derive_project_state())
    )


def _quoted(name: str, origin: str, rendering: str, why: str) -> Seal:
    """شاهدٌ وارِدٌ: يُعلَن بمصدره ويُعرَض، ولا يُصادَم صِدامَ المولَّد."""

    def side() -> Mapping[str, str]:
        return {rendering: why}

    return Seal(
        name=name,
        genus=SealGenus.QUOTED,
        origin=origin,
        generate=side,
        transcription=side,
    )


def _owner_licensed_seals() -> Mapping[str, str]:
    """ما نُقل عن كلِّ وديعةٍ مأذونة: ختمُها وحجمُها ومنزلتُها المشتقّة."""

    renderings: dict[str, str] = {}
    for deposit in owner_deposit.THE_DEPOSITS:
        renderings[f"{deposit.path}.sha256"] = deposit.transcribed_sha256
        renderings[f"{deposit.path}.bytes"] = f"{deposit.transcribed_bytes:,}"
    return renderings


def _owner_licensed_measured() -> Mapping[str, str]:
    """وما يولِّده القرصُ الآن لها؛ ويُصادَم بالمنقول عند كلّ نداء."""

    renderings: dict[str, str] = {}
    for deposit in owner_deposit.THE_DEPOSITS:
        reading = owner_deposit.measure(deposit)
        renderings[f"{deposit.path}.sha256"] = reading.measured_sha256
        renderings[f"{deposit.path}.bytes"] = f"{reading.measured_bytes:,}"
    return renderings


def the_registry() -> SealRegistry:
    """كلُّ ختمٍ في الشجرة، مولَّدًا عند كلّ نداء ولا يُخزَن."""

    readme = REPO_ROOT / "README.md"
    partition_prose = Path(partition.__file__)
    return SealRegistry(
        seals=(
            Seal(
                name="pair_sample_widening.prose_scope",
                genus=SealGenus.GENERATED,
                origin="PROSE_SCOPE_AT_MEASUREMENT ↔ prose_scope_fingerprint()",
                generate=lambda: _named_fields(widening.prose_scope_fingerprint()),
                transcription=lambda: _named_fields(
                    widening.PROSE_SCOPE_AT_MEASUREMENT
                ),
            ),
            Seal(
                name="pair_sample_widening.third_rung",
                genus=SealGenus.GENERATED,
                origin="THE_THIRD_RUNG_AT_MEASUREMENT ↔ third_rung_figures()",
                generate=lambda: _named_fields(widening.third_rung_figures()),
                transcription=lambda: _named_fields(
                    widening.THE_THIRD_RUNG_AT_MEASUREMENT
                ),
            ),
            _prose_seal(
                name="pair_sample_widening.third_rung ← README",
                origin="third_rung_figures() ↔ README.md",
                prose=readme,
                measure=_third_rung_renderings,
            ),
            Seal(
                name="hamil_audit_second_reading.counts",
                genus=SealGenus.GENERATED,
                origin="THE_COUNTS_AT_MEASUREMENT ↔ measure_the_audit_corpus()",
                generate=lambda: _named_fields(
                    second_reading.measure_the_audit_corpus()
                ),
                transcription=lambda: _named_fields(
                    second_reading.THE_COUNTS_AT_MEASUREMENT
                ),
            ),
            _prose_seal(
                name="pair_sample_widening.prose ← نثرُ الوحدة",
                origin=(
                    "the_widening_ladder() · the_cliff_factor() · "
                    "the_tail_occurrences_now() ↔ نثرُ الوحدة"
                ),
                prose=Path(widening.__file__),
                measure=_widening_prose_renderings,
            ),
            Seal(
                name="hamil_phase2_audit_deposit.tally",
                genus=SealGenus.GENERATED,
                origin="exhibits/hamil-induction ↔ حكمٌ مشتقٌّ عند كلّ قراءة",
                generate=_phase2_tally,
                transcription=_phase2_tally,
            ),
            Seal(
                name="hamil_phase2_audit_deposit.register",
                genus=SealGenus.GENERATED,
                origin="seals.json المُودَع ↔ تعدادٌ مشتقٌّ من قائمة أختامه",
                generate=_hamil_register_tally,
                transcription=_hamil_register_tally,
            ),
            Seal(
                name="owner_licensed_deposit.seals",
                genus=SealGenus.GENERATED,
                origin="THE_DEPOSITS ↔ بايتاتُ الودائع المأذونة على القرص",
                generate=_owner_licensed_measured,
                transcription=_owner_licensed_seals,
            ),
            Seal(
                name="usool_al_unboob.doors",
                genus=SealGenus.EPISTEMIC_WITNESS,
                origin="docs/USOOL_AL-UNBOOB.md ↔ حضورُ موضعِ كلِّ بابٍ على القرص",
                generate=_usool_doors,
                transcription=_usool_doors,
            ),
            Seal(
                name="methodological_sources.T3",
                genus=SealGenus.EPISTEMIC_WITNESS,
                origin="THE_METHODOLOGICAL_SOURCES ↔ حضورُ الذكر في وحدة كلّ باب",
                generate=_methodological_sources_sides,
                transcription=_methodological_sources_sides,
            ),
            _prose_seal(
                name="letter_haraka_partition.ladder",
                origin="table_census() ↔ نثرُ الوحدة",
                prose=partition_prose,
                measure=_partition_ladder_renderings,
            ),
            _prose_seal(
                name="letter_haraka_partition.ladder ← README",
                origin="table_census(WITH_PROSE) ↔ README.md",
                prose=readme,
                measure=_partition_occurrences_rendering,
            ),
            _prose_seal(
                name="letter_haraka_partition.margins",
                origin="absent_cells() ↔ نثرُ الوحدة",
                prose=partition_prose,
                measure=_partition_margin_renderings,
            ),
            _prose_seal(
                name="letter_haraka_partition.sukun_share",
                origin="cell_counts(WITH_PROSE) ↔ نثرُ الوحدة",
                prose=partition_prose,
                measure=_sukun_share_renderings,
            ),
            _prose_seal(
                name="letter_haraka_partition.sukun_share ← README",
                origin="cell_counts(WITH_PROSE) ↔ README.md",
                prose=readme,
                measure=_sukun_share_renderings,
            ),
            Seal(
                name="hamil_phase1_audit_deposit.tally",
                genus=SealGenus.GENERATED,
                origin="THE_CHECKS ↔ حكمٌ مشتقٌّ عند كلّ استيراد لا حقلٌ يُكتَب",
                generate=_phase1_tally,
                transcription=_phase1_tally,
            ),
            Seal(
                name="program.project_state.vision_block",
                genus=SealGenus.GENERATED,
                origin="docs/VISION.md ↔ render_state_block(derive_project_state())",
                generate=_vision_block_measured,
                transcription=_vision_block_transcribed,
            ),
            _quoted(
                name="quran_corpus_word_total.THE_QUOTED_WORD_TOTAL",
                origin="نقلٌ خارجيّ؛ منزلتُه تُقرَأ بـrun_quoted_total_survey",
                rendering=f"{word_total.THE_QUOTED_WORD_TOTAL:,}",
                why="لا يولَّد ههنا؛ شاهدٌ لا بوّابة",
            ),
            _quoted(
                name="hamil_phase1_audit_deposit._QUOTED_ON_RATE",
                origin="نقلٌ عن hamil نقضَه الحسابُ ههنا",
                rendering=f"{phase1._QUOTED_ON_RATE}",
                why="شاهدُ اتّهامٍ لا رقمَ عمل؛ مناقَضٌ بالحساب فلا يُصادَم",
            ),
        )
    )


def render(verdicts: tuple[SealVerdict, ...]) -> Iterator[str]:
    """يعرض كلَّ ختمٍ بجنسه، ويُسمّي كلَّ فارقٍ بحقلِه لا بصمتٍ."""

    for verdict in verdicts:
        mark = "✗" if verdict.has_drifted else "✓"
        yield f"{mark} [{verdict.seal.genus.value}] {verdict.seal.name}"
        yield f"    المصدر: {verdict.seal.origin}"
        for reading in verdict.readings:
            if verdict.is_quoted:
                yield f"    {reading.field}: {reading.measured}"
            elif reading.agrees:
                yield f"    {reading.field}: {reading.measured}"
            else:
                yield (
                    f"    {reading.field}: المنقولُ {reading.transcribed} "
                    f"≠ المولَّدُ {reading.measured}"
                )
        yield ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="بوّابةُ التوليد الواحدة")
    parser.add_argument(
        "--check",
        action="store_true",
        help="يُخرِج 1 إن انزاح رقمٌ محروسٌ عمّا يولِّده القرصُ الآن",
    )
    args = parser.parse_args(argv)

    registry = the_registry()
    verdicts = registry.collide_all()
    for line in render(verdicts):
        print(line)

    tally = registry.genera()
    print(
        "الأختام: "
        + " · ".join(f"{genus.value} {count}" for genus, count in tally.items())
    )

    drifted = tuple(verdict for verdict in verdicts if verdict.has_drifted)
    if not drifted:
        print("لا انزياح: كلُّ رقمٍ محروسٍ نابضٌ بمولِّدِه.")
        return 0

    print("انزياحٌ مسمًّى — ولا يُقبَل رقمٌ بلا فاتورةٍ تُعرَض في رسالة الالتزام:")
    for verdict in drifted:
        for reading in verdict.discrepancies:
            print(
                f"  {verdict.seal.name} · {reading.field}: "
                f"{reading.transcribed} → {reading.measured}"
            )
    return 1 if args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
