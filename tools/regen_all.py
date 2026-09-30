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
from alghanem.arabic import pair_sample_widening as widening  # noqa: E402
from alghanem.arabic import powers_two_regime_measure as powers  # noqa: E402
from alghanem.arabic import quran_corpus_word_total as word_total  # noqa: E402
from alghanem.arabic import turath_coverage_tally as turath  # noqa: E402
from alghanem.arabic import zipf_block_entropy_measure as zipf  # noqa: E402
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


def _zipf_ladders_measured() -> Mapping[str, str]:
    """سُلَّما زِبف والكتل مقيسَين الآن من البايتات المختومة."""

    census = zipf.vocabulary_census()
    fold: dict[str, str] = {
        "tokens": str(census.tokens),
        "types": str(census.types),
        "hapax": str(census.hapax),
    }
    for fit in zipf.zipf_ladder():
        fold[f"window.{fit.window}"] = f"{fit.magnitude:.4f} · {fit.r_squared:.4f}"
    stride = zipf.block_entropy_ladder(
        zipf.StreamKey.AS_SEALED, zipf.SamplingRule.EVERY_SEVENTH
    )
    for size, value in zip(zipf.THE_BLOCK_SIZES, stride.per_character):
        fold[f"stride.k{size}"] = f"{value:.4f}"
    return fold


def _zipf_ladders_transcribed() -> Mapping[str, str]:
    """السُّلَّمان كما جُمِّدا في الوحدة، ليُصادَما بما يقيسه القرصُ الآن."""

    tokens, types, hapax = zipf.THE_VOCABULARY_AT_MEASUREMENT
    fold: dict[str, str] = {
        "tokens": str(tokens),
        "types": str(types),
        "hapax": str(hapax),
    }
    for window, magnitude, r_squared in zipf.THE_LADDER_AT_MEASUREMENT:
        fold[f"window.{window}"] = f"{magnitude:.4f} · {r_squared:.4f}"
    for size, value in zip(zipf.THE_BLOCK_SIZES, zipf.THE_STRIDE_LADDER_AT_MEASUREMENT):
        fold[f"stride.k{size}"] = f"{value:.4f}"
    return fold


def _zipf_prose_renderings() -> Mapping[str, str]:
    """أرقامُ نثر وحدة زِبف: مقامُها، وسُلَّمُ نوافذها، وما تُنقِصه الخطوة."""

    census = zipf.vocabulary_census()
    renderings = {
        "tokens": f"{census.tokens:,}",
        "types": f"{census.types:,}",
    }
    for fit in zipf.zipf_ladder():
        renderings[f"window.{fit.window}.magnitude"] = f"{fit.magnitude:.4f}"
        renderings[f"window.{fit.window}.r_squared"] = f"{fit.r_squared:.4f}"
    return renderings


def _powers_tail_zipf() -> float:
    """جودةُ ربط الذيل على زِبف الخام، على المفتاح المختوم."""

    return powers.tail_fit(powers.TokenRule.AS_SEALED, powers.Law.ZIPF).r_squared


def _powers_figures_measured() -> Mapping[str, str]:
    """أرقامُ ورقة Powers مقيسةً الآن من البايتات المختومة."""

    sealed = powers.token_census(powers.TokenRule.AS_SEALED)
    dropped = powers.token_census(powers.TokenRule.PUBLISHER_MARKUP_DROPPED)
    fold: dict[str, str] = {
        "tokens.sealed": str(sealed.tokens),
        "tokens.dropped": str(dropped.tokens),
        "markup": str(powers.the_publisher_markup_census().occurrences),
        "head.zipf": f"{powers.head_fit().r_squared:.4f}",
        "tail.zipf": f"{_powers_tail_zipf():.4f}",
        "tail.powers": f"{powers.tail_fit().r_squared:.4f}",
        "head.dropped": (
            f"{powers.head_fit(powers.TokenRule.PUBLISHER_MARKUP_DROPPED).r_squared:.4f}"
        ),
    }
    for index, band in enumerate(powers.band_lengths()):
        fold[f"length.band{index + 1}"] = f"{band.mean_length:.4f}"
    return fold


def _powers_figures_transcribed() -> Mapping[str, str]:
    """الأرقامُ كما جُمِّدت في الوحدة، لتُصادَم بما يقيسه القرصُ الآن."""

    sealed, dropped, markup = powers.THE_TOKENS_AT_MEASUREMENT
    head, tail_zipf, tail_powers, head_dropped = powers.THE_REGIMES_AT_MEASUREMENT
    fold: dict[str, str] = {
        "tokens.sealed": str(sealed),
        "tokens.dropped": str(dropped),
        "markup": str(markup),
        "head.zipf": f"{head:.4f}",
        "tail.zipf": f"{tail_zipf:.4f}",
        "tail.powers": f"{tail_powers:.4f}",
        "head.dropped": f"{head_dropped:.4f}",
    }
    for index, value in enumerate(powers.THE_LENGTHS_AT_MEASUREMENT):
        fold[f"length.band{index + 1}"] = f"{value:.4f}"
    return fold


def _powers_prose_renderings() -> Mapping[str, str]:
    """أرقامُ نثر وحدة Powers: مقامُها، ونظاماها، وسُلَّمُ أطوالها."""

    renderings = {
        "tokens.dropped": (
            f"{powers.token_census(powers.TokenRule.PUBLISHER_MARKUP_DROPPED).tokens:,}"
        ),
        "markup": f"{powers.the_publisher_markup_census().occurrences:,}",
        "head.zipf": f"{powers.head_fit().r_squared:.4f}",
        "tail.powers": f"{powers.tail_fit().r_squared:.4f}",
        "tail.zipf": f"{_powers_tail_zipf():.4f}",
    }
    for index, band in enumerate(powers.band_lengths()):
        renderings[f"length.band{index + 1}"] = f"{band.mean_length:.3f}"
    return renderings


def _turath_tally_measured() -> Mapping[str, str]:
    """إحصاءُ جدول التغطية مُعادًا الآن من صفوفه ومن القرص."""

    current = turath.tally()
    fold: dict[str, str] = {
        "rows": str(current.rows),
        "covered": str(current.covered),
        "absent": str(current.absent),
        "hedged": str(current.hedged),
        "overstated": str(turath.the_header_overstates_the_covered_rows_by()),
        "unnamed": str(turath.unnamed_nodes()),
        "title_gap": str(turath.the_title_is_unreached_even_by_the_header()),
    }
    for ground in turath.Ground:
        fold[f"ground.{ground.name}"] = str(turath.ground_census()[ground])
    return fold


def _turath_tally_transcribed() -> Mapping[str, str]:
    """الإحصاءُ كما جُمِّد في الوحدة، ليُصادَم بما تُخرِجه الصفوفُ الآن."""

    rows, covered, absent, hedged = turath.THE_TALLY_AT_MEASUREMENT
    overstated, unnamed, title_gap = turath.THE_BREACHES_AT_MEASUREMENT
    fold: dict[str, str] = {
        "rows": str(rows),
        "covered": str(covered),
        "absent": str(absent),
        "hedged": str(hedged),
        "overstated": str(overstated),
        "unnamed": str(unnamed),
        "title_gap": str(title_gap),
    }
    for ground, count in zip(turath.Ground, turath.THE_GROUND_CENSUS_AT_MEASUREMENT):
        fold[f"ground.{ground.name}"] = str(count)
    return fold


def _turath_prose_renderings() -> Mapping[str, str]:
    """أرقامُ نثر وحدة التغطية: مجاميعُها الثلاثة وخروقُها وتوزيعُ مقاماتها."""

    current = turath.tally()
    return {
        "rows": str(current.rows),
        "covered": str(current.covered),
        "absent": str(current.absent),
        "overstated": str(turath.the_header_overstates_the_covered_rows_by()),
        "unnamed": str(turath.unnamed_nodes()),
        "not_deposited": str(turath.ground_census()[turath.Ground.NOT_DEPOSITED]),
        "no_figure": str(turath.ground_census()[turath.Ground.NO_FIGURE]),
        "ayah_lines": f"{turath.deposited_ayah_lines():,}",
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
            Seal(
                name="zipf_block_entropy_measure.ladders",
                genus=SealGenus.GENERATED,
                origin=(
                    "THE_VOCABULARY_AT_MEASUREMENT · THE_LADDER_AT_MEASUREMENT · "
                    "THE_STRIDE_LADDER_AT_MEASUREMENT ↔ القياسُ من البايتات المختومة"
                ),
                generate=_zipf_ladders_measured,
                transcription=_zipf_ladders_transcribed,
            ),
            _prose_seal(
                name="zipf_block_entropy_measure.prose ← نثرُ الوحدة",
                origin="zipf_ladder() · vocabulary_census() ↔ نثرُ الوحدة",
                prose=Path(zipf.__file__),
                measure=_zipf_prose_renderings,
            ),
            _quoted(
                name="zipf_block_entropy_measure.THE_QUOTED_ZIPF",
                origin="نقلٌ عن `mujammad.norm.txt`؛ بايتاتُه ليست في هذه الشجرة",
                rendering=(
                    f"α={zipf.THE_QUOTED_ZIPF.magnitude} · "
                    f"R²={zipf.THE_QUOTED_ZIPF.r_squared}"
                ),
                why=(
                    "لا نافذةَ رتبٍ مُعلَنةٌ معه، ويقع في نافذتنا العاشرة الألفيّة "
                    "وحدَها؛ فيُعرَض ولا يُصادَم"
                ),
            ),
            Seal(
                name="powers_two_regime_measure.figures",
                genus=SealGenus.GENERATED,
                origin=(
                    "THE_TOKENS_AT_MEASUREMENT · THE_REGIMES_AT_MEASUREMENT · "
                    "THE_LENGTHS_AT_MEASUREMENT ↔ القياسُ من البايتات المختومة"
                ),
                generate=_powers_figures_measured,
                transcription=_powers_figures_transcribed,
            ),
            _prose_seal(
                name="powers_two_regime_measure.prose ← نثرُ الوحدة",
                origin="head_fit() · tail_fit() · band_lengths() ↔ نثرُ الوحدة",
                prose=Path(powers.__file__),
                measure=_powers_prose_renderings,
            ),
            _quoted(
                name="powers_two_regime_measure.THE_QUOTED_POWERS_FIGURES",
                origin="نقلٌ عن شهادةٍ مرفوعةٍ على `mujammad.norm.txt` وورقة 1998",
                rendering=" · ".join(
                    f"{figure.value}" for figure in powers.THE_QUOTED_POWERS_FIGURES
                ),
                why=(
                    "بايتاتُ مقامها ليست في هذه الشجرة؛ فتُعرَض وتُقابَل بحدٍّ "
                    "مُعلَنٍ ولا تُتَّخَذ مرجعًا"
                ),
            ),
            Seal(
                name="turath_coverage_tally.tally",
                genus=SealGenus.GENERATED,
                origin=(
                    "THE_TALLY_AT_MEASUREMENT · THE_BREACHES_AT_MEASUREMENT · "
                    "THE_GROUND_CENSUS_AT_MEASUREMENT ↔ العدُّ من الصفوف ومن القرص"
                ),
                generate=_turath_tally_measured,
                transcription=_turath_tally_transcribed,
            ),
            _prose_seal(
                name="turath_coverage_tally.prose ← نثرُ الوحدة",
                origin="tally() · ground_census() ↔ نثرُ الوحدة",
                prose=Path(turath.__file__),
                measure=_turath_prose_renderings,
            ),
            _quoted(
                name="turath_coverage_tally.THE_QUOTED_HEADER",
                origin="نقلٌ عن ترويسة جدول التغطية وعنوانه",
                rendering=(
                    f"{turath.THE_QUOTED_HEADER.covered} مغطاة · "
                    f"{turath.THE_QUOTED_HEADER.absent} غياب · "
                    f"على {turath.THE_QUOTED_NODE_COUNT} عقدة"
                ),
                why=(
                    "يُعرَض بنصّه ثمّ يُصادَم بعدّ الصفوف؛ ولا يُصحَّح في مكانه "
                    "ولا تُزاد صفوفٌ تسويةً له"
                ),
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
