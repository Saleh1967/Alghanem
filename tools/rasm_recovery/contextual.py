"""Finite, context-indexed orthographic recovery; NOT whole-word licensing.

Copyright (c) 2026 Saleh1967, MIT (see LICENSE). Moved into Alghanem from
Progressive_Licensing_Contextual_Rasm_v4: the pinned copy of the bridge is
replaced by the live `canonical116.bridge` (protocol 1.1), whose version is
written into every codebook so a certificate names the bridge that made it.
The decoder needs the complete shared codebook, not merely its digest.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from math import isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from canonical116.bridge import A116, PROTOCOL_VERSION, SUKUN, bridge  # noqa: E402

INDEX = {a: i for i, a in enumerate(A116)}


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


@dataclass(frozen=True)
class Context:
    entry: str = "start"
    exit: str = "continue"
    left: str = ""
    profile: str = "modern-vocalized"

    def __post_init__(self):
        if self.entry not in ("start", "joined") or self.exit not in (
            "continue",
            "pause",
        ):
            raise ValueError("UNKNOWN_BOUNDARY")
        if self.profile not in ("modern-vocalized", "uthmani-explicit"):
            raise ValueError("UNKNOWN_PROFILE")
        if self.entry == "joined" and (
            not self.left or any(c.isspace() for c in self.left)
        ):
            raise ValueError("JOINED_NEEDS_EXPLICIT_ONE_WORD_LEFT_CONTEXT")
        if self.entry == "start" and self.left:
            raise ValueError("START_DOES_NOT_CONSUME_LEFT_CONTEXT")

    @property
    def key(self):
        return digest(self.__dict__)


def project(surface: str, context: Context):
    """No annotations or guessed start vowels. Inspect ALL upstream blockers.

    Joined evaluation uses the supplied actual left word, which must itself
    pass the upstream bridge. A named guard rejects bare-alif vowel atoms and
    un-repaired initial sukun. This is still a bounded textual projection.
    """
    if not surface or any(c.isspace() for c in surface):
        raise ValueError("DOMAIN_ELEMENT_MUST_BE_ONE_NONEMPTY_TOKEN")
    joined = context.entry == "joined"
    target = int(joined)
    source = context.left + " " + surface if joined else surface
    boundaries = {0: {"entry": "start", "exit": "continue"}} if joined else {}
    boundaries[target] = {"entry": context.entry, "exit": context.exit}
    report = bridge(source, profile=context.profile, contexts=boundaries)
    reasons = [dict(x) for k in ("deferrals", "rejections") for x in report.get(k, [])]
    if report.get("error"):
        reasons.append({"upstream_error": report["error"]})
    if report["status"] != "READY":
        return {"status": report["status"], "reasons": reasons, "atoms": None}
    words = report["words"]
    if len(words) != target + 1 or words[target]["source"] != surface:
        return {
            "status": "DEFER",
            "reasons": [{"reason": "NOT_ONE_EXACT_WORD_SPAN"}],
            "atoms": None,
        }
    for w in words:
        if any(
            c["role"] == "ALIF_WITH_ITS_OWN_MARK" and c["reading"]["vowel"] is not None
            for c in w["clusters"]
        ):
            return {
                "status": "REJECT",
                "reasons": [
                    {"reason": "BARE_ALIF_OWN_MARK_NOT_LICENSED", "word": w["index"]}
                ],
                "atoms": None,
            }
        if w["entry"] == "start" and w["atoms"] and w["atoms"][0].endswith(SUKUN):
            return {
                "status": "REJECT",
                "reasons": [
                    {"reason": "INITIAL_SUKUN_WITHOUT_REPAIR", "word": w["index"]}
                ],
                "atoms": None,
            }
    return {"status": "READY", "reasons": [], "atoms": tuple(words[target]["atoms"])}


def fold_atoms(atoms):
    """Bijective length-free code for ALL finite A116 strings, no license claim."""
    offset, power, value = 0, 1, 0
    for atom in atoms:
        value = 116 * value + INDEX[atom]
        offset += power
        power *= 116
    return offset + value


def unfold_atoms(number):
    if type(number) is not int or number < 0:
        raise ValueError("NONNEGATIVE_INTEGER_REQUIRED")
    n, capacity = 0, 1
    while number >= capacity:
        number -= capacity
        capacity *= 116
        n += 1
    result = []
    for _ in range(n):
        number, d = divmod(number, 116)
        result.append(A116[d])
    return tuple(reversed(result))


def pair(a, b):
    return (a + b) * (a + b + 1) // 2 + b


def unpair(z):
    if type(z) is not int or z < 0:
        raise ValueError("NONNEGATIVE_INTEGER_REQUIRED")
    s = (isqrt(8 * z + 1) - 1) // 2
    b = z - s * (s + 1) // 2
    return s - b, b


@dataclass(frozen=True)
class Certificate:
    book_digest: str
    context_key: str
    atoms: tuple[str, ...]
    ordinal: int
    fiber_size: int
    residual_bits: int
    integer: int
    standing: str = "EXACT_RECOVERY_RELATIVE_TO_DECLARED_CODEBOOK"


class Codebook:
    """Finite fibers built by executing projection, then UTF-8 sorting.

    Original surfaces are stored in the SHARED book. This is not free
    compression: report book bytes separately from per-word residual bits.
    """

    def __init__(self, surfaces, context):
        self.context = context
        self.domain = tuple(sorted(set(surfaces), key=lambda x: x.encode("utf-8")))
        self.decisions = {s: project(s, context) for s in self.domain}
        fibers = defaultdict(list)
        for surface, decision in self.decisions.items():
            if decision["status"] == "READY":
                fibers[decision["atoms"]].append(surface)
        self.fibers = {a: tuple(ss) for a, ss in fibers.items()}
        self.payload = {
            "version": 1,
            "bridge_protocol": PROTOCOL_VERSION,
            "context": context.__dict__,
            "domain": self.domain,
            "decisions": self.decisions,
        }
        self.digest = digest(self.payload)
        self.serialized_bytes = len(
            json.dumps(
                self.payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode()
        )

    def encode(self, surface):
        if surface not in self.decisions:
            raise ValueError("OUTSIDE_DECLARED_DOMAIN")
        d = self.decisions[surface]
        if d["status"] != "READY":
            raise ValueError("NONREADY_CANNOT_RECEIVE_RECOVERY_CERTIFICATE")
        atoms = d["atoms"]
        fiber = self.fibers[atoms]
        rank = fiber.index(surface)
        size = len(fiber)
        return Certificate(
            self.digest,
            self.context.key,
            atoms,
            rank,
            size,
            (size - 1).bit_length(),
            pair(fold_atoms(atoms), rank),
        )

    def decode(self, cert):
        if cert.book_digest != self.digest or cert.context_key != self.context.key:
            raise ValueError("WRONG_CODEBOOK_OR_CONTEXT")
        fiber = self.fibers.get(cert.atoms)
        if (
            fiber is None
            or type(cert.ordinal) is not int
            or not 0 <= cert.ordinal < len(fiber)
        ):
            raise ValueError("INVALID_FIBER_ORDINAL")
        source = fiber[cert.ordinal]
        if cert != self.encode(source):
            raise ValueError("ALTERED_CERTIFICATE")
        return source

    def decode_integer(self, z):
        atom_number, rank = unpair(z)
        atoms = unfold_atoms(atom_number)
        fiber = self.fibers.get(atoms)
        if fiber is None or rank >= len(fiber):
            raise ValueError("INTEGER_NOT_IN_THIS_CODEBOOK_IMAGE")
        return fiber[rank]


def transport(cert, source_book, destination_book):
    """Reconstruct source, then re-evaluate destination; never inherit READY."""
    surface = source_book.decode(cert)
    return destination_book.encode(surface)
