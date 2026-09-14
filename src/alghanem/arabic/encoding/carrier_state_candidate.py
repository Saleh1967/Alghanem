"""A measured-invertible candidate encoding of vocalized Arabic surfaces.

This module deposits an externally built (carrier, state) encoding into this
tree, and it deposits it as exactly what was measured and no more:

    RoundTrip(retrieve, generate) == identity   on the surfaces it was run on

An encoding that loses nothing is *invertible*. Invertibility is a property of
every information-preserving re-encoding, including trivial ones — "the unit is
the whole word" is invertible too — so a round-trip rate is evidence about loss
and never evidence that the chosen unit is atomic, minimal, or unique. The
depositing claim that the (carrier, state) pair is "the only consistent atomic
unit of the vocalized Arabic letter" is therefore **not** carried here:
`ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY`.

Nor is anything born. `docs/CONSTITUTION.md` G0.N states that a carrier is a
knot tied at the one point that survived every weaker model *licensed and
frozen for its own experiment*; no weaker model was licensed or frozen for this
encoding, so nothing here is a carrier in that sense and nothing here is
promoted (`NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN`). The name of the type says
so: it is a `CarrierStateUnit` produced by a candidate codec, not an `Atom` and
not a `Protocol`.

Three defects found by running the deposited codec — not read off its prose —
are closed here rather than carried in:

* **Writing over a value already set was silent.** Two consecutive harakat
  (``بَُ``), two consecutive tanwin marks, a harakah followed by a tanwin, and
  a doubled shadda all overwrote an already-derived value and produced a
  surface different from the input. The genus is closed, not the instance:
  `_read_marks` refuses every second write to a slot that already holds a
  derived value, so all four are refused at construction with one rule.
* **A dedicated ``madd_self`` state silently dropped every other field.** The
  deposited codec collapsed ``آ`` into a state, then returned from `retrieve`
  before reading `tanwin`, `silent`, or `waw_madda` — fields it had just
  written. ``آ`` is now an ordinary `CarrierSeat.MADD` on the ``ء`` carrier, so
  each field is read exactly where it is written, and ``آَ``, ``آً``, ``آ۟``
  and a geminated ``آ`` round-trip instead of being truncated. Units whose
  state is `PASSTHROUGH` or `DAGGER` are checked at construction to carry no
  other structure, which is what makes "no field is written and never read"
  true of the whole type rather than of one branch.
* **Non-carrier symbols were dropped silently.** ``العربية!`` came back without
  its exclamation mark. Every codepoint outside the declared carrier set is now
  carried explicitly as a `PASSTHROUGH` unit.

The carrier set itself is declared in this module and is not derived from any
property of Arabic (`CARRIER_SET_IS_DECLARED_NOT_DERIVED`); the deposited codec
used `str.isalpha`, which made every alphabetic codepoint of every script a
carrier, so a Latin word read as a sequence of carriers with implied sukun.

What the layer registry claimed about the alef is now decided by derivation
rather than by editing its wording. `derive_alef_states` runs the codec and
returns the states an alef actually carries; over `EMBEDDED_ROUND_TRIP_CASES`
plus ``اً`` it returns more than one, so the exclusivity claim is refuted by
this module's own trace and is recorded as declared-not-enforced
(`ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED`). Enforcing it would refuse
ordinary orthography, which is the stronger reason not to.

No percentage over any external text is written here. A percentage is only
re-derivable by a holder of the same bytes, so `InvertibilityMeasurement`
requires the source's `sha256`, its byte length, the normalization form and the
Unicode database version, on the pattern of
`alghanem.arabic.level_two_source_texts.QaydAttributionScan`, and its counts
are derived by running the codec rather than passed in.
`MEASURED_INVERTIBILITY_SOURCES` is empty because no digest came with the deposit
(`SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE`), and the two Uthmani figures that
arrived with it (93.38% and 95.76%) disagree with each other and were measured
before the dropped-symbol defect was known, so they mix a codec defect with the
Uthmani phenomena they were read as measuring
(`UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS`).

Finally, a clean round trip over any closed text stays bounded by that text.
`CompleteInductionIsCorpusBounded` refuses the step from an exhausted corpus to
the open language, so `THREE_SOURCES_ARE_CORPUS_BOUNDED` is named rather than
softened in prose.

This module is inert with respect to authority: it issues no verdict, no
freeze, no birth, and no rank, and nothing in `kernel/` reads it.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED",
    "CARRIER_SET_IS_DECLARED_NOT_DERIVED",
    "CARRIER_STATE_NAMED_RESIDUALS",
    "DECLARED_CARRIERS",
    "EMBEDDED_ROUND_TRIP_CASES",
    "ENCODING_LAYER_REGISTRY",
    "MEASURED_INVERTIBILITY_SOURCES",
    "NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN",
    "ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY",
    "SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE",
    "THREE_SOURCES_ARE_CORPUS_BOUNDED",
    "UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS",
    "CarrierSeat",
    "CarrierState",
    "CarrierStateCodec",
    "CarrierStateEncodingError",
    "CarrierStateUnit",
    "EncodingLayer",
    "GeminationRole",
    "InvertibilityMeasurement",
    "derive_alef_states",
    "round_trip_holds",
]


class CarrierStateEncodingError(ValueError):
    """Raised when a surface or a unit sequence is refused at construction."""


# --- named residuals -------------------------------------------------------

ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY: Final = (
    "a clean round trip shows the encoding loses nothing; it is no evidence "
    "that the (carrier, state) pair is atomic, minimal, or the only consistent "
    "unit, since every information-preserving re-encoding round-trips"
)

NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN: Final = (
    "G0.N licenses a knot by what it survived; no weaker model was licensed or "
    "frozen for this encoding, so nothing here is a carrier in that sense and "
    "no unit produced here is born, ranked, or frozen"
)

THREE_SOURCES_ARE_CORPUS_BOUNDED: Final = (
    "a round trip exhausted over a closed text is established inside that text "
    "and presumptive beyond it, per CompleteInductionIsCorpusBounded; the step "
    "to the open language is refused by name, not softened"
)

CARRIER_SET_IS_DECLARED_NOT_DERIVED: Final = (
    "DECLARED_CARRIERS is written in this module, not derived from any property "
    "of Arabic; a codepoint outside it is carried as a passthrough unit rather "
    "than judged not to be a carrier"
)

SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE: Final = (
    "no percentage over any external text is recorded here: a rate is only "
    "re-derivable by a holder of the same bytes, and no source digest or byte "
    "length was supplied with the deposit, so MEASURED_INVERTIBILITY_SOURCES is empty"
)

UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS: Final = (
    "the Uthmani residue reported with the deposit arrived as two disagreeing "
    "figures (93.38% and 95.76%) measured before the silent dropping of "
    "non-carrier symbols was known, so it mixes a codec defect with the "
    "Uthmani phenomena it was read as measuring and separates neither"
)

ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED: Final = (
    "the layer registry claimed the alef carries sukun_implicit exclusively; "
    "derive_alef_states refutes it on this module's own trace, since ordinary "
    "orthography writes tanwin on the alef, so the claim is recorded as "
    "declared and is deliberately not enforced"
)

CARRIER_STATE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY": (
        ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY
    ),
    "NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN": NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN,
    "THREE_SOURCES_ARE_CORPUS_BOUNDED": THREE_SOURCES_ARE_CORPUS_BOUNDED,
    "CARRIER_SET_IS_DECLARED_NOT_DERIVED": CARRIER_SET_IS_DECLARED_NOT_DERIVED,
    "SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE": SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE,
    "UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS": (
        UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS
    ),
    "ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED": (
        ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED
    ),
}


# --- the declared alphabet -------------------------------------------------

_SHADDA: Final = "\u0651"
_DAGGER_ALIF: Final = "\u0670"
_SILENT_ZERO: Final = "\u06df"
_WAW_MADDA: Final = "\u0653"


class CarrierState(Enum):
    """The state a carrier may hold. `SUKUN_IMPLICIT` is the unmarked reading."""

    FATHA = "fatha"
    DAMMA = "damma"
    KASRA = "kasra"
    SUKUN_EXPLICIT = "sukun_explicit"
    SUKUN_IMPLICIT = "sukun_implicit"
    DAGGER = "dagger"
    PASSTHROUGH = "passthrough"

    @property
    def is_structural_only(self) -> bool:
        """Is this a state whose unit carries no seat, tanwin, or mark?"""
        return self in (CarrierState.DAGGER, CarrierState.PASSTHROUGH)


class CarrierSeat(Enum):
    """The written seat a carrier appears on, recorded rather than inferred."""

    ON_ALEF = "on_alef"
    ON_ALEF_KASRA = "on_alef_kasra"
    ON_WAW = "on_waw"
    ON_YEH = "on_yeh"
    MADD = "madd"
    TA_MARBUTA = "ta_marbuta"
    ALEF_MAQSURA = "alef_maqsura"


class GeminationRole(Enum):
    """The first half of a gemination pair; the second half carries no role."""

    PAIR_START = "pair_start"


_HARAKAT: Final[dict[str, CarrierState]] = {
    "\u064e": CarrierState.FATHA,
    "\u064f": CarrierState.DAMMA,
    "\u0650": CarrierState.KASRA,
    "\u0652": CarrierState.SUKUN_EXPLICIT,
}
_TANWIN: Final[dict[str, CarrierState]] = {
    "\u064b": CarrierState.FATHA,
    "\u064c": CarrierState.DAMMA,
    "\u064d": CarrierState.KASRA,
}

_SEATED_FORMS: Final[dict[str, tuple[str, CarrierSeat]]] = {
    "\u0623": ("\u0621", CarrierSeat.ON_ALEF),
    "\u0625": ("\u0621", CarrierSeat.ON_ALEF_KASRA),
    "\u0624": ("\u0621", CarrierSeat.ON_WAW),
    "\u0626": ("\u0621", CarrierSeat.ON_YEH),
    "\u0622": ("\u0621", CarrierSeat.MADD),
    "\u0629": ("\u062a", CarrierSeat.TA_MARBUTA),
    "\u0649": ("\u064a", CarrierSeat.ALEF_MAQSURA),
}

_BASE_FROM_SEAT: Final[dict[tuple[str, CarrierSeat], str]] = {
    (base, seat): written for written, (base, seat) in _SEATED_FORMS.items()
}

_SEAT_HOSTS: Final[dict[CarrierSeat, str]] = {
    seat: base for base, seat in _SEATED_FORMS.values()
}

_PLAIN_CARRIERS: Final[frozenset[str]] = frozenset(
    "\u0621"  # ء
    "\u0627"  # ا
    "\u0628\u062a\u062b\u062c\u062d\u062e"
    "\u062f\u0630\u0631\u0632\u0633\u0634"
    "\u0635\u0636\u0637\u0638\u0639\u063a"
    "\u0641\u0642\u0643\u0644\u0645\u0646"
    "\u0647\u0648\u064a"
    "\u0671"  # ٱ
)

DECLARED_CARRIERS: Final[frozenset[str]] = _PLAIN_CARRIERS | frozenset(_SEATED_FORMS)
"""Every codepoint this module reads as a carrier. Declared, never derived."""


# --- the unit --------------------------------------------------------------


@dataclass(frozen=True, order=True)
class CarrierStateUnit:
    """One (carrier, state) pair with the structure its surface actually wrote.

    Every field is read back by `CarrierStateCodec.retrieve`. A unit whose
    state `is_structural_only` is refused if it carries anything else, which is
    what keeps a written-and-never-read field unsayable rather than merely
    absent today.
    """

    carrier: str
    state: CarrierState
    gemination: GeminationRole | None = None
    tanwin: bool = False
    seat: CarrierSeat | None = None
    tanwin_alif_seat: bool = False
    silent: bool = False
    waw_madda: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.carrier, str) or len(self.carrier) != 1:
            raise CarrierStateEncodingError("a carrier is exactly one codepoint")
        if not isinstance(self.state, CarrierState):
            raise CarrierStateEncodingError("a unit state is a CarrierState member")
        if self.state.is_structural_only:
            self._refuse_structure_on_a_bare_state()
            return
        if self.carrier not in DECLARED_CARRIERS:
            raise CarrierStateEncodingError(
                f"{self.carrier!r} is outside DECLARED_CARRIERS, so it may only "
                "be carried as a passthrough unit"
            )
        if self.state is CarrierState.DAGGER:  # pragma: no cover - unreachable
            raise CarrierStateEncodingError("a dagger unit carries no structure")
        self._refuse_mismatched_seat()
        self._refuse_unheld_flags()

    def _refuse_structure_on_a_bare_state(self) -> None:
        carried = (
            self.gemination is not None,
            self.tanwin,
            self.seat is not None,
            self.tanwin_alif_seat,
            self.silent,
            self.waw_madda,
        )
        if any(carried):
            raise CarrierStateEncodingError(
                f"a {self.state.value} unit carries no seat, tanwin, gemination, "
                "or mark: a field written here would never be read back"
            )
        if self.state is CarrierState.DAGGER and self.carrier != "\u0627":
            raise CarrierStateEncodingError("a dagger unit is written on the alef")

    def _refuse_mismatched_seat(self) -> None:
        if self.seat is None:
            return
        if not isinstance(self.seat, CarrierSeat):
            raise CarrierStateEncodingError("a unit seat is a CarrierSeat member")
        host = _SEAT_HOSTS[self.seat]
        if self.carrier != host:
            raise CarrierStateEncodingError(
                f"seat {self.seat.value} is written on {host!r}, not "
                f"on {self.carrier!r}"
            )

    def _refuse_unheld_flags(self) -> None:
        if self.gemination is not None:
            if not isinstance(self.gemination, GeminationRole):
                raise CarrierStateEncodingError(
                    "a gemination role is a GeminationRole member"
                )
            if self.state is not CarrierState.SUKUN_IMPLICIT:
                raise CarrierStateEncodingError(
                    "the first half of a gemination pair holds sukun_implicit"
                )
            if self.tanwin or self.silent or self.waw_madda:
                raise CarrierStateEncodingError(
                    "the first half of a gemination pair carries no tanwin or mark"
                )
        if self.tanwin_alif_seat:
            if not self.tanwin or self.state is not CarrierState.FATHA:
                raise CarrierStateEncodingError(
                    "an alef seat is consumed only by a fatha tanwin"
                )
        if self.tanwin and self.state not in (
            CarrierState.FATHA,
            CarrierState.DAMMA,
            CarrierState.KASRA,
        ):
            raise CarrierStateEncodingError("a tanwin holds fatha, damma, or kasra")
        if self.waw_madda and self.carrier != "\u0648":
            raise CarrierStateEncodingError("an explicit madda is read on the waw only")

    @property
    def written_form(self) -> str:
        """The seated letter this unit's carrier is written as."""
        if self.seat is None:
            return self.carrier
        return _BASE_FROM_SEAT[(self.carrier, self.seat)]


# --- the layer registry ----------------------------------------------------


@dataclass(frozen=True, order=True)
class EncodingLayer:
    """One named phenomenon the codec handles, with the claim it carries."""

    order: int
    name: str
    description: str

    def __post_init__(self) -> None:
        if not isinstance(self.order, int) or self.order < 1:
            raise CarrierStateEncodingError("a layer order is a positive integer")
        if not self.name or not self.description:
            raise CarrierStateEncodingError("a layer names itself and its claim")


ENCODING_LAYER_REGISTRY: Final[tuple[EncodingLayer, ...]] = (
    EncodingLayer(
        1,
        "the state of the alef",
        "the alef holds sukun_implicit wherever no mark is written on it; the "
        "deposited claim that it holds sukun_implicit *exclusively* is refuted "
        "by derive_alef_states and is not enforced, see "
        "ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED",
    ),
    EncodingLayer(
        2,
        "four harakat and two sukuns",
        "fatha, damma, kasra, plus sukun_explicit when written and "
        "sukun_implicit when nothing is",
    ),
    EncodingLayer(
        3,
        "the five written hamza seats",
        "the seat is recorded as written and never inferred from the state",
    ),
    EncodingLayer(
        4,
        "gemination",
        "a shadda becomes a sukun_implicit PAIR_START followed by the same "
        "carrier holding the written state; no doubled letter is invented",
    ),
    EncodingLayer(
        5,
        "the alef seat of fatha tanwin",
        "whether an actual alef codepoint was consumed as the tanwin's seat is "
        "recorded, since ta marbuta, alef maqsura, and hamza need none",
    ),
    EncodingLayer(
        6,
        "ta marbuta and alef maqsura",
        "seats on the ta and the yeh, read back through the same seat table",
    ),
    EncodingLayer(
        7,
        "the dagger alef",
        "a unit of its own holding CarrierState.DAGGER and nothing else",
    ),
    EncodingLayer(
        8,
        "mandatory NFC normalization",
        "any compatibility decomposition is composed before anything is read",
    ),
    EncodingLayer(
        9,
        "the small high rounded zero",
        "U+06DF is carried and reproduced rather than dropped",
    ),
    EncodingLayer(
        10,
        "the explicit madda on the waw",
        "U+0653 after a waw, independent of the seated madd of the hamza",
    ),
    EncodingLayer(
        11,
        "every non-carrier codepoint",
        "a codepoint outside DECLARED_CARRIERS is carried as a PASSTHROUGH unit "
        "rather than dropped, so punctuation and other scripts survive intact",
    ),
)


# --- the codec -------------------------------------------------------------


class CarrierStateCodec:
    """Generate units from a surface and retrieve the surface from units.

    The codec holds no mutable state, so every call is independent. It refuses
    rather than repairs: a surface that writes twice into one derived slot is
    refused at construction, because silently keeping the last write is what
    produced a surface different from its input in the deposited codec.
    """

    def generate(self, surface: str) -> tuple[CarrierStateUnit, ...]:
        """Read a surface into units, refusing every ambiguous double write."""
        if not isinstance(surface, str):
            raise CarrierStateEncodingError("a surface is a string")
        text = unicodedata.normalize("NFC", surface)
        units: list[CarrierStateUnit] = []
        chars = list(text)
        total = len(chars)
        index = 0
        while index < total:
            char = chars[index]
            if char == _DAGGER_ALIF:
                units.append(CarrierStateUnit("\u0627", CarrierState.DAGGER))
                index += 1
                continue
            if char not in DECLARED_CARRIERS:
                units.append(CarrierStateUnit(char, CarrierState.PASSTHROUGH))
                index += 1
                continue
            carrier, seat = _SEATED_FORMS.get(char, (char, None))
            index += 1
            state, tanwin, geminated, index = self._read_marks(chars, index, text)
            waw_madda = False
            if carrier == "\u0648" and index < total and chars[index] == _WAW_MADDA:
                waw_madda = True
                index += 1
            tanwin_alif_seat = False
            if (
                state is None
                and not geminated
                and index + 1 < total
                and chars[index] == "\u0627"
                and chars[index + 1] in _TANWIN
            ):
                state = _TANWIN[chars[index + 1]]
                tanwin = True
                tanwin_alif_seat = True
                index += 2
            silent = False
            if index < total and chars[index] == _SILENT_ZERO:
                silent = True
                index += 1
            held = state or CarrierState.SUKUN_IMPLICIT
            if geminated:
                units.append(
                    CarrierStateUnit(
                        carrier,
                        CarrierState.SUKUN_IMPLICIT,
                        GeminationRole.PAIR_START,
                        seat=seat,
                    )
                )
            units.append(
                CarrierStateUnit(
                    carrier,
                    held,
                    None,
                    tanwin,
                    seat,
                    tanwin_alif_seat,
                    silent,
                    waw_madda,
                )
            )
        return tuple(units)

    @staticmethod
    def _read_marks(
        chars: list[str], index: int, surface: str
    ) -> tuple[CarrierState | None, bool, bool, int]:
        """Consume the marks after a carrier, refusing any second write.

        One rule closes the whole genus: a harakah after a harakah, a tanwin
        after a tanwin, a tanwin after a harakah, and a shadda after a shadda
        are each a second write into a slot that already holds a derived value,
        and each is refused here instead of overwriting what was read first.
        """
        state: CarrierState | None = None
        tanwin = False
        geminated = False
        total = len(chars)
        while index < total:
            char = chars[index]
            if char == _SHADDA:
                if geminated:
                    raise CarrierStateEncodingError(
                        "a second shadda writes over a gemination already read "
                        f"in {surface!r}"
                    )
                geminated = True
            elif char in _HARAKAT or char in _TANWIN:
                if state is not None:
                    raise CarrierStateEncodingError(
                        "a second vowel mark writes over a state already read "
                        f"in {surface!r}"
                    )
                if char in _HARAKAT:
                    state = _HARAKAT[char]
                else:
                    state = _TANWIN[char]
                    tanwin = True
            else:
                break
            index += 1
        return state, tanwin, geminated, index

    def retrieve(self, units: Iterable[CarrierStateUnit]) -> str:
        """Write the units back out, refusing a pair whose half is missing."""
        ordered = tuple(units)
        for unit in ordered:
            if not isinstance(unit, CarrierStateUnit):
                raise CarrierStateEncodingError(
                    "every retrieved element is a CarrierStateUnit"
                )
        out: list[str] = []
        index = 0
        total = len(ordered)
        while index < total:
            unit = ordered[index]
            if unit.state is CarrierState.PASSTHROUGH:
                out.append(unit.carrier)
                index += 1
                continue
            if unit.state is CarrierState.DAGGER:
                out.append(_DAGGER_ALIF)
                index += 1
                continue
            if unit.gemination is GeminationRole.PAIR_START:
                if index + 1 >= total or ordered[index + 1].carrier != unit.carrier:
                    raise CarrierStateEncodingError(
                        "a gemination pair start is not followed by its own "
                        "carrier, so the pair cannot be written back"
                    )
                out.append(unit.written_form + _SHADDA)
                out.append(self._tail(ordered[index + 1], seated=False))
                index += 2
                continue
            out.append(self._tail(unit, seated=True))
            index += 1
        return "".join(out)

    @staticmethod
    def _tail(unit: CarrierStateUnit, *, seated: bool) -> str:
        marks = {
            CarrierState.FATHA: "\u064e",
            CarrierState.DAMMA: "\u064f",
            CarrierState.KASRA: "\u0650",
            CarrierState.SUKUN_EXPLICIT: "\u0652",
        }
        tanwin_marks = {
            CarrierState.FATHA: "\u064b",
            CarrierState.DAMMA: "\u064c",
            CarrierState.KASRA: "\u064d",
        }
        out = unit.written_form if seated else ""
        if unit.tanwin_alif_seat:
            # `generate` reads the explicit waw madda before it looks ahead for
            # the tanwin's alef seat, so the two are written back in that same
            # order; emitting the madda last would let NFC compose it onto the
            # seat alef and return a different surface.
            if unit.waw_madda:
                out += _WAW_MADDA
            out += "\u0627" + tanwin_marks[unit.state]
        else:
            if unit.tanwin:
                out += tanwin_marks[unit.state]
            else:
                out += marks.get(unit.state, "")
            if unit.waw_madda:
                out += _WAW_MADDA
        if unit.silent:
            out += _SILENT_ZERO
        return out


_CODEC: Final = CarrierStateCodec()


def round_trip_holds(surface: str) -> bool:
    """Does this surface come back byte-identical under NFC? Derived, not told."""
    normalized = unicodedata.normalize("NFC", surface)
    retrieved = _CODEC.retrieve(_CODEC.generate(normalized))
    return unicodedata.normalize("NFC", retrieved) == normalized


EMBEDDED_ROUND_TRIP_CASES: Final[tuple[str, ...]] = (
    "\u0628\u0650\u0633\u0652\u0645\u0650",
    "\u0627\u0644\u0644\u0651\u064e\u0647\u0650",
    "\u0627\u0644\u0631\u0651\u064e\u062d\u0652\u0645\u064e\u0670\u0646\u0650",
    "\u0627\u0644\u0631\u0651\u064e\u062d\u0650\u064a\u0645\u0650",
    "\u0625\u0650\u0646\u0651\u064e\u0627",
    "\u0623\u064e\u0639\u0652\u0637\u064e\u064a\u0652\u0646\u064e\u0627\u0643\u064e",
    "\u0645\u064f\u0635\u064e\u0644\u0651\u064b\u0649",
    "\u0645\u0651\u064f\u0633\u064e\u0645\u064b\u0649",
    "\u063a\u064f\u0632\u0651\u064b\u0649",
    "\u0623\u064f\u0645\u0651\u064e\u0629\u064c",
    "\u0631\u064e\u0628\u0651\u064f\u0643\u064e",
    "\u0645\u064e\u0642\u064e\u0627\u0639\u0650\u062f\u0650\u0646\u0627",
    "\u0627\u0644\u0639\u0631\u0628\u064a\u0629!",
    "\u0622\u0645\u064e\u0646\u064e",
    "\u0642\u064f\u0631\u0652\u0622\u0646\u064c",
    "\u0648\u064e\u0653",
    "\u0628\u06df",
    "\u0627\u064b",
)
"""The surfaces this module round-trips, carried as literals and not as paths."""


def derive_alef_states(
    surfaces: Iterable[str] = EMBEDDED_ROUND_TRIP_CASES,
) -> frozenset[CarrierState]:
    """Return the states an alef actually holds across these surfaces.

    This is what decides layer 1 rather than its wording: if the returned set
    holds more than one member, the exclusivity claim is refuted on this
    module's own trace.
    """
    held: set[CarrierState] = set()
    for surface in surfaces:
        for unit in _CODEC.generate(surface):
            if unit.carrier == "\u0627" and unit.seat is None:
                held.add(unit.state)
    return frozenset(held)


# --- measurement over an external source -----------------------------------


@dataclass(frozen=True, order=True)
class InvertibilityMeasurement:
    """A round-trip measurement over one external source, re-derivable by bytes.

    It carries no percentage field. The rate is a property derived from the two
    counts, and the counts are produced by `measure` rather than passed in, so
    a written rate with no measurement behind it is unsayable here.
    """

    source_id: str
    source_sha256: str
    source_byte_length: int
    normalization_form: str
    unicode_database_version: str
    token_total: int
    token_mismatches: int

    def __post_init__(self) -> None:
        for value, name in (
            (self.source_id, "source id"),
            (self.source_sha256, "source sha256"),
            (self.normalization_form, "normalization form"),
            (self.unicode_database_version, "unicode database version"),
        ):
            if not isinstance(value, str) or not value:
                raise CarrierStateEncodingError(f"{name} must be a non-empty string")
        if len(self.source_sha256) != 64:
            raise CarrierStateEncodingError(
                "a source sha256 is 64 characters; a partial digest re-derives "
                "no measurement"
            )
        if not isinstance(self.source_byte_length, int) or self.source_byte_length < 1:
            raise CarrierStateEncodingError(
                "a source byte length is a positive integer"
            )
        if not isinstance(self.token_total, int) or self.token_total < 1:
            raise CarrierStateEncodingError(
                "a measurement over no token at all is not a measurement"
            )
        if not isinstance(self.token_mismatches, int) or self.token_mismatches < 0:
            raise CarrierStateEncodingError(
                "a mismatch total is a non-negative integer"
            )
        if self.token_mismatches > self.token_total:
            raise CarrierStateEncodingError(
                "more mismatches than tokens is two contradictory claims in one "
                "measurement"
            )

    @property
    def matched_tokens(self) -> int:
        """Tokens that came back identical. Derived from the two totals."""
        return self.token_total - self.token_mismatches

    @property
    def matched_fraction(self) -> float:
        """The round-trip fraction, derived; see THREE_SOURCES_ARE_CORPUS_BOUNDED."""
        return self.matched_tokens / self.token_total

    @classmethod
    def measure(
        cls,
        tokens: Iterable[str],
        *,
        source_id: str,
        source_sha256: str,
        source_byte_length: int,
    ) -> InvertibilityMeasurement:
        """Run the codec over these tokens and record what it did, not a claim."""
        counted = 0
        mismatched = 0
        for token in tokens:
            counted += 1
            if not round_trip_holds(token):
                mismatched += 1
        return cls(
            source_id=source_id,
            source_sha256=source_sha256,
            source_byte_length=source_byte_length,
            normalization_form="NFC",
            unicode_database_version=unicodedata.unidata_version,
            token_total=counted,
            token_mismatches=mismatched,
        )


MEASURED_INVERTIBILITY_SOURCES: Final[tuple[InvertibilityMeasurement, ...]] = ()
"""Empty: see SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE. Absence is not a failure."""
