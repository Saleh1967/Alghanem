"""Small independent finite-table checker; no import of producer/bridge.

Proves consistency, injectivity and exact residual capacity of the deposited
finite tables. Does NOT independently adjudicate Arabic projection rules.

Added in Alghanem: every READY row must also be derivable from its own rasm by
the declared cluster expansions in `rasm_consistency` (no bridge import). Before
this, a row given wrong atoms and re-digested passed; now it is refused with
RASM_ATOMS_INCONSISTENT. The injectivity and minimal-capacity checks below are
true by construction of the fibers; they are kept as guards, not as evidence.
"""

import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from rasm_consistency import consistent


def check(path):
    total = Counter()
    with gzip.open(path, "rt", encoding="utf-8") as inp:
        for line in inp:
            row = json.loads(line)
            book = row["book"]
            content = json.dumps(
                book, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode()
            if hashlib.sha256(content).hexdigest() != row["book_digest"]:
                raise ValueError("BOOK_CONTENT_DIGEST_MISMATCH")
            domain = book["domain"]
            if domain != sorted(set(domain), key=lambda s: s.encode()):
                raise ValueError("DOMAIN_NOT_CANONICAL_UNIQUE")
            if set(domain) != set(book["decisions"]):
                raise ValueError("DECISIONS_DO_NOT_EXHAUST_DOMAIN")
            fibers = defaultdict(list)
            for surface in domain:
                d = book["decisions"][surface]
                if d["status"] == "READY":
                    if not isinstance(d["atoms"], list):
                        raise ValueError("MISSING_ATOMS")
                    if not consistent(surface, d["atoms"]):
                        raise ValueError(f"RASM_ATOMS_INCONSISTENT: {surface}")
                    fibers[tuple(d["atoms"])].append(surface)
                elif d["atoms"] is not None or not d["reasons"]:
                    raise ValueError("UNEXPLAINED_NONREADY_OR_ATOM_LEAK")
            seen = set()
            for atoms, members in fibers.items():
                m = len(members)
                bits = 0
                while 2**bits < m:
                    bits += 1
                if bits and 2 ** (bits - 1) >= m:
                    raise ValueError("NONMINIMAL_FIXED_RESIDUAL_CAPACITY")
                for rank, surface in enumerate(members):
                    key = (atoms, rank)
                    if key in seen or members[rank] != surface:
                        raise ValueError("INJECTIVITY_OR_INVERSE_FAILURE")
                    seen.add(key)
            total["books"] += 1
            total["domain_cases"] += len(domain)
            total["ready_cases"] += len(seen)
            total["fibers"] += len(fibers)
    return dict(total)


if __name__ == "__main__":
    import sys

    print(json.dumps(check(Path(sys.argv[1])), indent=2))
