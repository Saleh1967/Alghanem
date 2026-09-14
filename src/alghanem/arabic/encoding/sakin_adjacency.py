"""Two adjacent sukun-holding units, scanned occurrence-complete over a surface.

What this module is
-------------------
`alghanem.arabic.encoding.carrier_state_candidate` reads a written surface into
`CarrierStateUnit` values. This module reads those units and reports, for every
adjacent pair in which both units hold a sukun, whether the pair is a *counted*
two-sukun adjacency or is excluded, and by which named exclusion. It reports one
row per pair, including the excluded ones, so the excluded cases stay inspectable
rather than being subtracted before anyone can look at them.

What this module does not claim
-------------------------------
It does not claim that Arabic forbids two adjacent sukuns. It does not claim a
rate. A predicate that names an exclusion for every pair it meets reaches a clean
residue by construction, and a clean residue reached that way is a property of
the predicate and not a measurement of the language
(`CLOSURE_IS_A_PREDICATE_NOT_A_MEASURED_RATE`). Worse, an exclusion class that
was written *after* looking at what the previous pass left over cannot then be
counted as evidence for the rule it rescues; it is a description of the residue
(`RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE`). Both are named here
rather than argued away, and the exclusions each carry
`SakinClashExclusion.is_residue_defined` so the two kinds never blur.

No percentage over any text is recorded. This tree vendors no corpus, so no
figure quoted elsewhere can be re-derived here, and an unreproducible figure is
not written down (`NO_CORPUS_IS_VENDORED_SO_NO_RATE_IS_RECORDED`). `SakinClashScan`
exists for the day a digest arrives: it requires the source's `sha256`, byte
length, normalization form and Unicode database version, and derives its counts
by running this scan rather than accepting them. `MEASURED_SAKIN_CLASH_SOURCES`
is empty.

Three things settled by running the codec rather than by reasoning about it
--------------------------------------------------------------------------
1. In the definite article the gemination mark does **not** sit where a single
   check of the first unit, nor a single check of the second, would find it.
   `derive_article_gemination_offsets` returns offset 2 for a sun letter that is
   not `lam` (`ٱلشَّمس`, `ٱلنَّاس`, `ٱلرَّحمٰن`) and offset 1 for `ٱلَّذين`, where the
   `lam` is itself the geminated letter. So the pair (`ٱ`, `ل`) in `ٱلشَّمس` has
   `PAIR_START` on *neither* member and no gemination check of any single
   position rescues it: what rescues it is that `ٱ` is a connecting alef, an
   extension and not a closing consonant. The pair (`ل`, `ش`) one step later is
   the assimilation pair, and there the mark is on the *second* member. Both
   checks are therefore needed, and they answer about different pairs.
2. The silent-zero `\u06df` is not a stray unit here. The codec already reads it
   into `CarrierStateUnit.silent` on the unit it follows, so `قَالُوا۟` yields five
   units and not six, and a scan that expected a third unit to inspect would
   find nothing to fix.
3. `ه` and `ة` do not behave alike, and neither behaves as its pausal reading.
   The small waw and small yeh that write the connecting vowel after `ه`
   (`لَهُۥ`, `فِيهِۦ`) are `PASSTHROUGH` units: they are sound extension, they are
   never a sukun holder, and adjacency reads through them. `ة` is encoded as
   carrier `ت` under `CarrierSeat.TA_MARBUTA`, so at a stop, where it is read
   `ه`, the unit still says `ت` (`TA_MARBUTA_PAUSAL_HA_IS_NOT_ENCODED`).

Scope kept out on purpose
-------------------------
The rulings of the sukun-bearing nun act where the following consonant carries a
vowel, so they do not decide any pair this module counts, except that an
unwritten assimilation appears here as an ordinary gemination pair; nothing about
those rulings is modelled (`NUN_SAKINA_RULINGS_ARE_NOT_MODELLED_HERE`). A stop
mark is a `PASSTHROUGH` unit and nothing else: this module does not read a
pausal sukun onto the unit before it, and therefore cannot tell a sukun of the
connected reading from a sukun of the stop
(`PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN`).

The disconnected letter openings are excluded because the rule does not reach
them, not because they survived it: each letter there is uttered under its own
name, so the sequence is not connected speech and the question of two adjacent
sukuns is not posed of it. That is a declaration about scope made in this module,
not a result (`MUQATTAAT_ARE_EXCLUDED_BY_DEFINITION_NOT_MEASURED`).

Finally, an argument from economy of articulation — that a language avoids the
adjacency because avoiding it is easier — is an induction over the utterances
anyone has met, not a licence over the ones they have not. G0.N licenses a knot
by the weaker models it outlived, and no weaker model was licensed or frozen for
this predicate, so nothing here is born, ranked, or frozen
(`PHONETIC_ECONOMY_IS_AN_INDUCTION_NOT_A_LICENCE`).
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.arabic.encoding.carrier_state_candidate import (
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
    GeminationRole,
)

__all__ = [
    "ARTICLE_DERIVATION_CASES",
    "CLOSURE_IS_A_PREDICATE_NOT_A_MEASURED_RATE",
    "DECLARED_ARTIFACT_CODEPOINTS",
    "DECLARED_EXTENSION_CARRIERS",
    "DECLARED_EXTENSION_CARRIERS_ARE_NOT_DERIVED",
    "HA_DERIVATION_CASES",
    "DECLARED_RARE_READING_MARKS",
    "EMBEDDED_ADJACENCY_CASES",
    "MEASURED_SAKIN_CLASH_SOURCES",
    "MUQATTAAT_ARE_EXCLUDED_BY_DEFINITION_NOT_MEASURED",
    "MUQATTAAT_OPENINGS",
    "NO_CORPUS_IS_VENDORED_SO_NO_RATE_IS_RECORDED",
    "NUN_SAKINA_RULINGS_ARE_NOT_MODELLED_HERE",
    "PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN",
    "PHONETIC_ECONOMY_IS_AN_INDUCTION_NOT_A_LICENCE",
    "RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE",
    "SAKIN_ADJACENCY_NAMED_RESIDUALS",
    "TA_MARBUTA_PAUSAL_HA_IS_NOT_ENCODED",
    "AdjacentSakinPair",
    "SakinAdjacencyError",
    "SakinAdjacencyReport",
    "SakinClashExclusion",
    "SakinClashScan",
    "derive_article_gemination_offsets",
    "derive_ha_and_ta_marbuta_units",
    "holds_sukun",
    "is_extension_unit",
    "scan_surface",
    "scan_units",
]


class SakinAdjacencyError(ValueError):
    """Raised when a scan is asked for something it cannot honestly report."""


# --- named residuals -------------------------------------------------------

CLOSURE_IS_A_PREDICATE_NOT_A_MEASURED_RATE: Final = (
    "a predicate that names an exclusion for every pair it meets leaves a clean "
    "residue by construction; the cleanliness is a property of the predicate and "
    "is not a measurement of Arabic"
)

RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE: Final = (
    "an exclusion written after inspecting what an earlier pass left over "
    "describes that residue and cannot also be counted as evidence for the rule "
    "it rescues; SakinClashExclusion.is_residue_defined keeps the two apart"
)

DECLARED_EXTENSION_CARRIERS_ARE_NOT_DERIVED: Final = (
    "DECLARED_EXTENSION_CARRIERS is written in this module; that alef, waw and "
    "yeh extend a sound rather than close a syllable is asserted here and is not "
    "derived from any measurement made in this tree"
)

MUQATTAAT_ARE_EXCLUDED_BY_DEFINITION_NOT_MEASURED: Final = (
    "the disconnected letter openings are placed outside the rule's scope by a "
    "declaration in this module, because each letter is uttered under its own "
    "name; no measurement established that, and MUQATTAAT_OPENINGS is a written "
    "list rather than a derived one"
)

PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN: Final = (
    "a stop mark is only a passthrough unit here, so a sukun read because the "
    "reader stopped is indistinguishable from a sukun of the connected reading"
)

TA_MARBUTA_PAUSAL_HA_IS_NOT_ENCODED: Final = (
    "the tied taa is encoded as carrier taa under CarrierSeat.TA_MARBUTA, so at "
    "a stop, where it is read as haa, the unit still reports taa"
)

NUN_SAKINA_RULINGS_ARE_NOT_MODELLED_HERE: Final = (
    "the rulings of the sukun-bearing nun act where the following consonant "
    "carries a vowel and so decide no pair counted here; an unwritten "
    "assimilation reaches this scan as an ordinary gemination pair and nothing "
    "distinguishes it from a written one"
)

NO_CORPUS_IS_VENDORED_SO_NO_RATE_IS_RECORDED: Final = (
    "no source text is vendored in this tree, so no rate quoted elsewhere can be "
    "re-derived here; SakinClashScan requires a digest and derives its counts, "
    "and MEASURED_SAKIN_CLASH_SOURCES is empty until one is supplied"
)

PHONETIC_ECONOMY_IS_AN_INDUCTION_NOT_A_LICENCE: Final = (
    "that a language avoids an adjacency because avoiding it is easier is an "
    "induction over the utterances met, bounded by them; no weaker model was "
    "licensed or frozen for this predicate, so nothing here is born or ranked"
)

SAKIN_ADJACENCY_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "CLOSURE_IS_A_PREDICATE_NOT_A_MEASURED_RATE": (
        CLOSURE_IS_A_PREDICATE_NOT_A_MEASURED_RATE
    ),
    "RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE": (
        RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE
    ),
    "DECLARED_EXTENSION_CARRIERS_ARE_NOT_DERIVED": (
        DECLARED_EXTENSION_CARRIERS_ARE_NOT_DERIVED
    ),
    "MUQATTAAT_ARE_EXCLUDED_BY_DEFINITION_NOT_MEASURED": (
        MUQATTAAT_ARE_EXCLUDED_BY_DEFINITION_NOT_MEASURED
    ),
    "PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN": (
        PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN
    ),
    "TA_MARBUTA_PAUSAL_HA_IS_NOT_ENCODED": TA_MARBUTA_PAUSAL_HA_IS_NOT_ENCODED,
    "NUN_SAKINA_RULINGS_ARE_NOT_MODELLED_HERE": (
        NUN_SAKINA_RULINGS_ARE_NOT_MODELLED_HERE
    ),
    "NO_CORPUS_IS_VENDORED_SO_NO_RATE_IS_RECORDED": (
        NO_CORPUS_IS_VENDORED_SO_NO_RATE_IS_RECORDED
    ),
    "PHONETIC_ECONOMY_IS_AN_INDUCTION_NOT_A_LICENCE": (
        PHONETIC_ECONOMY_IS_AN_INDUCTION_NOT_A_LICENCE
    ),
}


# --- declared sets ---------------------------------------------------------

DECLARED_EXTENSION_CARRIERS: Final[frozenset[str]] = frozenset(
    (
        "\u0627",  # ا
        "\u0648",  # و
        "\u064a",  # ي
        "\u0671",  # ٱ
    )
)
"""Carriers this module reads as extending a sound, never as closing one."""

DECLARED_ARTIFACT_CODEPOINTS: Final[frozenset[str]] = frozenset(
    (
        "\u0640",  # tatweel: a drawn line, not a letter
        "=",
    )
)
"""Codepoints written into a text by its typesetting, not by its language."""

DECLARED_RARE_READING_MARKS: Final[frozenset[str]] = frozenset(
    (
        "\u06dc",  # ۜ
        "\u06ea",  # ۪
        "\u06ec",  # ۬
        "\u06e2",  # ۢ
        "\u06e3",  # ۣ
    )
)
"""Marks that record a minority reading rather than the reading being scanned."""

MUQATTAAT_OPENINGS: Final[frozenset[str]] = frozenset(
    (
        "\u0627\u0644\u0645",  # الم
        "\u0627\u0644\u0645\u0635",  # المص
        "\u0627\u0644\u0631",  # الر
        "\u0627\u0644\u0645\u0631",  # المر
        "\u0643\u0647\u064a\u0639\u0635",  # كهيعص
        "\u0637\u0647",  # طه
        "\u0637\u0633\u0645",  # طسم
        "\u0637\u0633",  # طس
        "\u064a\u0633",  # يس
        "\u0635",  # ص
        "\u062d\u0645",  # حم
        "\u0639\u0633\u0642",  # عسق
        "\u0642",  # ق
        "\u0646",  # ن
    )
)
"""The written letter openings, listed rather than recognised by a rule."""

_LATIN: Final = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

_SUKUN_STATES: Final[frozenset[CarrierState]] = frozenset(
    (CarrierState.SUKUN_EXPLICIT, CarrierState.SUKUN_IMPLICIT)
)


# --- the exclusions --------------------------------------------------------


class SakinClashExclusion(Enum):
    """Why an adjacent sukun-holding pair is not counted.

    `is_residue_defined` marks the exclusions that were written after inspecting
    what earlier passes left over. Those describe a residue and are not evidence
    for the rule they rescue.
    """

    EXTENSION_CARRIER_FIRST = "extension_carrier_first"
    EXTENSION_CARRIER_SECOND = "extension_carrier_second"
    DAGGER_ALIF = "dagger_alif"
    SILENT_UNIT = "silent_unit"
    ASSIMILATION_PAIR = "assimilation_pair"
    DISCONNECTED_LETTER_NAMES = "disconnected_letter_names"
    NON_ARABIC_ARTIFACT = "non_arabic_artifact"
    RARE_READING_MARK = "rare_reading_mark"

    @property
    def is_residue_defined(self) -> bool:
        """Was this exclusion written after inspecting an earlier residue?"""
        return self in (
            SakinClashExclusion.DISCONNECTED_LETTER_NAMES,
            SakinClashExclusion.NON_ARABIC_ARTIFACT,
            SakinClashExclusion.RARE_READING_MARK,
        )


def holds_sukun(unit: CarrierStateUnit) -> bool:
    """Does this unit hold a sukun, written or unwritten?"""
    return unit.state in _SUKUN_STATES


def is_extension_unit(unit: CarrierStateUnit) -> bool:
    """Is this unit a sound extension rather than a closing consonant?"""
    if unit.state is CarrierState.DAGGER:
        return True
    if unit.carrier in DECLARED_EXTENSION_CARRIERS:
        return True
    return bool(unit.waw_madda)


# --- one pair --------------------------------------------------------------


@dataclass(frozen=True)
class AdjacentSakinPair:
    """One adjacency of two sukun-holding units, counted or excluded by name.

    `first_index` and `second_index` are positions in the scanned unit tuple and
    need not be consecutive, because passthrough units are read through: a stop
    mark, a space, or the small waw that writes a connecting vowel stands between
    two units without being a member of the pair.
    """

    first_index: int
    second_index: int
    first: CarrierStateUnit
    second: CarrierStateUnit
    exclusion: SakinClashExclusion | None
    skipped_passthrough: int = 0

    def __post_init__(self) -> None:
        if self.second_index <= self.first_index:
            raise SakinAdjacencyError("a pair runs forward through the units")
        if not holds_sukun(self.first) or not holds_sukun(self.second):
            raise SakinAdjacencyError("both members of a pair hold a sukun")
        if self.skipped_passthrough < 0:
            raise SakinAdjacencyError("a skipped count is never negative")
        if self.skipped_passthrough != self.second_index - self.first_index - 1:
            raise SakinAdjacencyError(
                "the skipped count is the gap between the two members"
            )
        if self.exclusion is not None and not isinstance(
            self.exclusion, SakinClashExclusion
        ):
            raise SakinAdjacencyError("an exclusion is a SakinClashExclusion member")

    @property
    def is_counted(self) -> bool:
        """Is this pair counted as a two-sukun adjacency?"""
        return self.exclusion is None

    @property
    def is_residue_defined_exclusion(self) -> bool:
        """Was this pair excluded by a rule written to describe a residue?"""
        return self.exclusion is not None and self.exclusion.is_residue_defined


# --- the scan --------------------------------------------------------------

_CODEC: Final = CarrierStateCodec()


def _exclusion_for(
    first: CarrierStateUnit,
    second: CarrierStateUnit,
    *,
    in_letter_names: bool,
    near_artifact: bool,
    near_rare_mark: bool,
    spans_dagger: bool,
) -> SakinClashExclusion | None:
    """Name the first exclusion that reaches this pair, or None if none does.

    The order is fixed and total: an earlier exclusion hides a later one, so the
    reported name is the first reason and not the only possible one. Gemination
    is tested on **both** members, because the definite article puts the mark on
    the second member before a sun letter and on the first before `ٱلَّذين`, and a
    check of one position alone misses one of the two.
    """
    if in_letter_names:
        return SakinClashExclusion.DISCONNECTED_LETTER_NAMES
    if near_artifact:
        return SakinClashExclusion.NON_ARABIC_ARTIFACT
    if near_rare_mark:
        return SakinClashExclusion.RARE_READING_MARK
    if (
        first.gemination is GeminationRole.PAIR_START
        or second.gemination is GeminationRole.PAIR_START
    ):
        return SakinClashExclusion.ASSIMILATION_PAIR
    if spans_dagger:
        return SakinClashExclusion.DAGGER_ALIF
    if first.silent or second.silent:
        return SakinClashExclusion.SILENT_UNIT
    if is_extension_unit(first):
        return SakinClashExclusion.EXTENSION_CARRIER_FIRST
    if is_extension_unit(second):
        return SakinClashExclusion.EXTENSION_CARRIER_SECOND
    return None


def scan_units(
    units: Iterable[CarrierStateUnit],
    *,
    in_letter_names: bool = False,
) -> tuple[AdjacentSakinPair, ...]:
    """Report every adjacent sukun-holding pair, excluded ones included.

    Passthrough units are read through rather than treated as separators,
    because the classic adjacency is the one across a word boundary and a space
    is a passthrough unit. A dagger alef is read through in the same way, since
    its state holds no sukun and it could otherwise never reach the exclusion
    that names it. Neither is ever a member of a pair, and the number skipped is
    recorded on the pair so a wide gap stays visible.
    """
    ordered = tuple(units)
    for unit in ordered:
        if not isinstance(unit, CarrierStateUnit):
            raise SakinAdjacencyError("a scan reads CarrierStateUnit values")
    pairs: list[AdjacentSakinPair] = []
    previous: int | None = None
    artifact_since = False
    rare_since = False
    dagger_since = False
    for index, unit in enumerate(ordered):
        if unit.state is CarrierState.DAGGER:
            dagger_since = True
            continue
        if unit.state is CarrierState.PASSTHROUGH:
            if unit.carrier in DECLARED_ARTIFACT_CODEPOINTS or unit.carrier in _LATIN:
                artifact_since = True
            if unit.carrier in DECLARED_RARE_READING_MARKS:
                rare_since = True
            continue
        if not holds_sukun(unit):
            previous = None
            artifact_since = False
            rare_since = False
            dagger_since = False
            continue
        if previous is not None:
            first = ordered[previous]
            near_artifact = (
                artifact_since
                or first.carrier in DECLARED_ARTIFACT_CODEPOINTS
                or unit.carrier in DECLARED_ARTIFACT_CODEPOINTS
            )
            pairs.append(
                AdjacentSakinPair(
                    previous,
                    index,
                    first,
                    unit,
                    _exclusion_for(
                        first,
                        unit,
                        in_letter_names=in_letter_names,
                        near_artifact=near_artifact,
                        near_rare_mark=rare_since,
                        spans_dagger=dagger_since,
                    ),
                    index - previous - 1,
                )
            )
        previous = index
        artifact_since = False
        rare_since = False
        dagger_since = False
    return tuple(pairs)


@dataclass(frozen=True)
class SakinAdjacencyReport:
    """The pairs found in one surface, with the surface kept beside them."""

    surface: str
    pairs: tuple[AdjacentSakinPair, ...]
    treated_as_letter_names: bool

    def __post_init__(self) -> None:
        if not isinstance(self.surface, str):
            raise SakinAdjacencyError("a scanned surface is a string")
        if not isinstance(self.pairs, tuple):
            raise SakinAdjacencyError("scanned pairs are held in a tuple")

    @property
    def counted(self) -> tuple[AdjacentSakinPair, ...]:
        """The pairs no exclusion reached."""
        return tuple(pair for pair in self.pairs if pair.is_counted)

    @property
    def excluded(self) -> tuple[AdjacentSakinPair, ...]:
        """The pairs an exclusion reached, kept rather than subtracted."""
        return tuple(pair for pair in self.pairs if not pair.is_counted)

    def excluded_by(
        self, exclusion: SakinClashExclusion
    ) -> tuple[AdjacentSakinPair, ...]:
        """The pairs this one named exclusion reached."""
        return tuple(pair for pair in self.pairs if pair.exclusion is exclusion)


def _is_letter_names(surface: str) -> bool:
    """Is this surface one of the written letter openings, marks removed?"""
    bare = "".join(
        char
        for char in unicodedata.normalize("NFD", surface)
        if not unicodedata.combining(char) and char not in {"\u0640", " "}
    )
    return unicodedata.normalize("NFC", bare) in MUQATTAAT_OPENINGS


def scan_surface(surface: str) -> SakinAdjacencyReport:
    """Read a surface into units and report its adjacent sukun-holding pairs."""
    if not isinstance(surface, str):
        raise SakinAdjacencyError("a scanned surface is a string")
    letter_names = _is_letter_names(surface)
    units = _CODEC.generate(surface)
    return SakinAdjacencyReport(
        surface, scan_units(units, in_letter_names=letter_names), letter_names
    )


# --- derivations -----------------------------------------------------------

ARTICLE_DERIVATION_CASES: Final[tuple[str, ...]] = (
    "\u0671\u0644\u0634\u0651\u064e\u0645\u0652\u0633\u0650",  # ٱلشَّمْسِ
    "\u0671\u0644\u0646\u0651\u064e\u0627\u0633\u0650",  # ٱلنَّاسِ
    "\u0671\u0644\u0651\u064e\u0630\u0650\u064a\u0646\u064e",  # ٱلَّذِينَ
    "\u0671\u0644\u0652\u0642\u064e\u0645\u064e\u0631\u0650",  # ٱلْقَمَرِ
)
"""Surfaces whose gemination offsets settle where the article's mark sits."""


def derive_article_gemination_offsets(
    surfaces: Iterable[str] = ARTICLE_DERIVATION_CASES,
) -> dict[str, tuple[int, ...]]:
    """Return, per surface, the unit offsets that carry `PAIR_START`.

    This is the derivation, not a restatement: a sun letter that is not `lam`
    puts the mark at offset 2, `ٱلَّذين` puts it at offset 1, and `ٱلْقَمَر` has none.
    A gemination check fixed to the first member alone therefore misses the sun
    letter case, and one fixed to the second member alone misses `ٱلَّذين`, while
    the pair (`ٱ`, `ل`) before a sun letter carries the mark on neither member
    and is reached by no gemination check at all.
    """
    found: dict[str, tuple[int, ...]] = {}
    for surface in surfaces:
        units = _CODEC.generate(surface)
        found[surface] = tuple(
            index
            for index, unit in enumerate(units)
            if unit.gemination is GeminationRole.PAIR_START
        )
    return found


HA_DERIVATION_CASES: Final[tuple[str, ...]] = (
    "\u0644\u064e\u0647\u064f\u06e5",  # لَهُۥ
    "\u0641\u0650\u064a\u0647\u0650\u06e6",  # فِيهِۦ
    "\u0645\u0650\u0646\u0652\u0647\u064f\u0645\u0652",  # مِنْهُمْ
    "\u0631\u064e\u062d\u0652\u0645\u064e\u0629\u064c",  # رَحْمَةٌ
    "\u0645\u064e\u062f\u0650\u064a\u0646\u064e\u0629\u0650",  # مَدِينَةِ
)
"""Surfaces that settle how the haa and the tied taa are actually encoded."""


def derive_ha_and_ta_marbuta_units(
    surfaces: Iterable[str] = HA_DERIVATION_CASES,
) -> tuple[tuple[str, str, str, str | None, bool], ...]:
    """Return every haa, tied taa, and connecting-vowel unit these surfaces hold.

    Each row is `(surface, carrier, state, seat, is_passthrough)`. The derivation
    shows two things this module then has to live with. The small waw and small
    yeh that write the connecting vowel after a haa arrive as `PASSTHROUGH`
    units, so they hold no sukun and adjacency reads through them. The tied taa
    arrives as carrier taa under `CarrierSeat.TA_MARBUTA`, so the unit reports
    taa even where a stop would have it read as haa.
    """
    marks = {"\u0647", "\u062a", "\u06e5", "\u06e6"}
    rows: list[tuple[str, str, str, str | None, bool]] = []
    for surface in surfaces:
        for unit in _CODEC.generate(surface):
            if unit.carrier not in marks:
                continue
            rows.append(
                (
                    surface,
                    unit.carrier,
                    unit.state.value,
                    unit.seat.value if unit.seat is not None else None,
                    unit.state is CarrierState.PASSTHROUGH,
                )
            )
    return tuple(rows)


EMBEDDED_ADJACENCY_CASES: Final[tuple[str, ...]] = (
    "\u0671\u0644\u0634\u0651\u064e\u0645\u0652\u0633\u0650",  # ٱلشَّمْسِ
    "\u0671\u0644\u0651\u064e\u0630\u0650\u064a\u0646\u064e",  # ٱلَّذِينَ
    "\u0671\u0644\u0652\u0642\u064e\u0645\u064e\u0631\u0650",  # ٱلْقَمَرِ
    "\u0642\u064e\u0627\u0644\u064f\u0648\u0627\u06df",  # قَالُوا۟
    "\u0621\u064e\u0627\u0645\u064e\u0646\u064f\u0648\u0627\u06df",  # ءَامَنُوا۟
    "\u0631\u064e\u062d\u0652\u0645\u064e\u0629\u064c",  # رَحْمَةٌ
    "\u0645\u064e\u062f\u0650\u064a\u0646\u064e\u0629\u0650",  # مَدِينَةِ
    "\u0639\u064e\u0644\u064e\u064a\u0652\u0647\u0650\u0645\u0652",  # عَلَيْهِمْ
    "\u0645\u0650\u0646\u0652\u0647\u064f\u0645\u0652",  # مِنْهُمْ
    "\u0644\u064e\u0647\u064f\u06e5",  # لَهُۥ
    "\u0641\u0650\u064a\u0647\u0650\u06e6",  # فِيهِۦ
    "\u0643\u0647\u064a\u0639\u0635",  # كهيعص
    "\u0637\u0647",  # طه
)
"""Surfaces this module's tests read, each carrying a distinct question."""


# --- measurement, withheld until a digest arrives --------------------------


@dataclass(frozen=True)
class SakinClashScan:
    """A scan of one source text, re-derivable only by a holder of its bytes.

    The pattern is `alghanem.arabic.level_two_source_texts.QaydAttributionScan`:
    the text is not vendored, and the digest, byte length, normalization form
    and Unicode database version are what let a reader re-derive the counts.
    The counts themselves are produced by running the scan rather than accepted,
    and no percentage is a field: a rate is a division anyone can perform, while
    a stored rate is a figure nobody can check.
    """

    source_id: str
    source_sha256: str
    source_byte_length: int
    normalization_form: str
    unicode_database_version: str
    pair_total: int
    counted_total: int
    residue_defined_exclusion_total: int

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise SakinAdjacencyError("a scanned source carries a non-blank id")
        digest = self.source_sha256
        if len(digest) != 64 or any(
            char not in "0123456789abcdef" for char in digest.lower()
        ):
            raise SakinAdjacencyError("a source digest is 64 hexadecimal characters")
        if self.source_byte_length <= 0:
            raise SakinAdjacencyError("a scanned source has a positive byte length")
        if not self.normalization_form.strip():
            raise SakinAdjacencyError("a scan records the normalization form it used")
        if not self.unicode_database_version.strip():
            raise SakinAdjacencyError("a scan records the Unicode database version")
        if self.pair_total < 0 or self.counted_total < 0:
            raise SakinAdjacencyError("a scanned total is never negative")
        if self.counted_total > self.pair_total:
            raise SakinAdjacencyError("more pairs were counted than were found")
        if not 0 <= self.residue_defined_exclusion_total <= self.pair_total:
            raise SakinAdjacencyError(
                "residue-defined exclusions are a part of the pairs found"
            )

    @property
    def excluded_total(self) -> int:
        """How many pairs an exclusion reached."""
        return self.pair_total - self.counted_total

    @property
    def counted_fraction(self) -> float:
        """The counted share, derived on request and never stored."""
        if self.pair_total == 0:
            raise SakinAdjacencyError("no share is derivable from an empty scan")
        return self.counted_total / self.pair_total

    @classmethod
    def measure(
        cls,
        *,
        source_id: str,
        source_sha256: str,
        source_byte_length: int,
        normalization_form: str,
        unicode_database_version: str,
        surfaces: Iterable[str],
    ) -> SakinClashScan:
        """Run the scan over the surfaces and derive the counts from it."""
        pair_total = 0
        counted_total = 0
        residue_total = 0
        for surface in surfaces:
            report = scan_surface(surface)
            pair_total += len(report.pairs)
            counted_total += len(report.counted)
            residue_total += sum(
                1 for pair in report.pairs if pair.is_residue_defined_exclusion
            )
        return cls(
            source_id=source_id,
            source_sha256=source_sha256,
            source_byte_length=source_byte_length,
            normalization_form=normalization_form,
            unicode_database_version=unicode_database_version,
            pair_total=pair_total,
            counted_total=counted_total,
            residue_defined_exclusion_total=residue_total,
        )


MEASURED_SAKIN_CLASH_SOURCES: Final[tuple[SakinClashScan, ...]] = ()
"""Empty: no source text was supplied with a digest, so no rate is written."""
