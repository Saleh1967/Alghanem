"""Run: python audit.py corpora/quran-simple-enhanced.txt OUT_DIR

Pinned historical regression ONLY; does not establish standard Arabic coverage.
No sentence is generated. Joined inputs are actual adjacent words in a line.
"""

import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path

from contextual import (
    Codebook,
    Context,
    fold_atoms,
    pair,
    project,
    transport,
    unfold_atoms,
    unpair,
)
from rasm_consistency import consistent

from canonical116.bridge import A116, PROTOCOL_VERSION

SOURCE_SHA = "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
ROOT = Path(__file__).resolve().parent


def must_refuse(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("MUTATED_INPUT_WAS_NOT_REFUSED")


def main(path, out_dir):
    OUT = Path(out_dir)
    OUT.mkdir(parents=True, exist_ok=True)
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError("WRONG_HISTORICAL_CORPUS")
    forms = set()
    first_left = {}
    occurrence_count = 0
    for line_no, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        tokens = [t for t in line.split() if t != "<sel>"]
        occurrence_count += len(tokens)
        forms.update(tokens)
        for pos in range(1, len(tokens)):
            first_left.setdefault(tokens[pos], (tokens[pos - 1], line_no, pos + 1))
    scopes = [
        ("start_continue", Context(), forms),
        ("start_pause", Context(exit="pause"), forms),
    ]
    groups = defaultdict(set)
    for form, (left, _, _) in first_left.items():
        groups[left].add(form)
    for end in ("continue", "pause"):
        for left in sorted(groups):
            scopes.append(
                (
                    "joined_" + end,
                    Context(entry="joined", exit=end, left=left),
                    groups[left],
                )
            )

    stats = defaultdict(Counter)
    reasons = defaultdict(Counter)
    books = {}
    certificates = {}
    fiber_hist = defaultdict(Counter)
    largest = {}
    checked = 0
    with gzip.open(OUT / "codebooks.jsonl.gz", "wt", encoding="utf-8") as out:
        for label, ctx, domain in scopes:
            book = Codebook(domain, ctx)
            books[(label, ctx.left)] = book
            out.write(
                json.dumps(
                    {"book_digest": book.digest, "book": book.payload},
                    ensure_ascii=False,
                )
                + "\n"
            )
            stats[label]["domain"] += len(book.domain)
            stats[label]["codebook_bytes"] += book.serialized_bytes
            for source, d in book.decisions.items():
                stats[label][d["status"]] += 1
                for r in d["reasons"]:
                    reasons[label][r.get("reason", str(r))] += 1
                if d["status"] != "READY":
                    must_refuse(lambda: book.encode(source))
                    continue
                cert = book.encode(source)
                assert consistent(source, cert.atoms), source
                assert book.decode(cert) == source
                assert book.decode_integer(cert.integer) == source
                assert unfold_atoms(fold_atoms(cert.atoms)) == cert.atoms
                assert unpair(pair(fold_atoms(cert.atoms), cert.ordinal)) == (
                    fold_atoms(cert.atoms),
                    cert.ordinal,
                )
                certificates[(label, source)] = (book, cert)
                stats[label]["exact_roundtrips"] += 1
                stats[label]["sum_residual_bits_per_ready_form"] += cert.residual_bits
                checked += 1
            for atoms, fiber in book.fibers.items():
                m = len(fiber)
                bits = (m - 1).bit_length()
                assert 2**bits >= m and (bits == 0 or 2 ** (bits - 1) < m)
                assert len({book.encode(s).ordinal for s in fiber}) == m
                fiber_hist[label][m] += 1
                if label not in largest or len(largest[label]["forms"]) < m:
                    largest[label] = {
                        "forms": fiber,
                        "atoms": atoms,
                        "left": ctx.left,
                        "bits": bits,
                    }
            print(label, ctx.left if ctx.left else "-", len(domain), flush=True) if len(
                domain
            ) > 10000 else None

    transitions = Counter()
    for source in forms:
        for label_a, label_b in [
            ("start_continue", "start_pause"),
            ("start_pause", "start_continue"),
            ("start_continue", "joined_continue"),
            ("joined_continue", "start_continue"),
            ("joined_continue", "joined_pause"),
            ("joined_pause", "joined_continue"),
        ]:
            src = certificates.get((label_a, source))
            if src is None:
                continue
            left = (
                first_left.get(source, ("",))[0] if label_b.startswith("joined") else ""
            )
            dest = books.get((label_b, left))
            if dest is None or source not in dest.decisions:
                transitions["destination_context_unavailable"] += 1
            elif dest.decisions[source]["status"] != "READY":
                must_refuse(lambda: transport(src[1], src[0], dest))
                transitions["destination_nonready_no_promotion"] += 1
            else:
                moved = transport(src[1], src[0], dest)
                assert dest.decode(moved) == source
                returned = transport(moved, dest, src[0])
                assert returned == src[1]
                transitions["successful_reversible_context_transports"] += 1

    # Exhaustive foundational numbering through length two, including empty.
    all_short = [()] + [(a,) for a in A116] + [(a, b) for a in A116 for b in A116]
    numbers = [fold_atoms(a) for a in all_short]
    assert numbers == list(range(len(numbers)))
    assert all(unfold_atoms(n) == a for a, n in zip(all_short, numbers))

    sample_book, sample_cert = next(iter(certificates.values()))
    must_refuse(
        lambda: sample_book.decode(replace(sample_cert, ordinal=sample_cert.fiber_size))
    )
    must_refuse(lambda: sample_book.decode(replace(sample_cert, book_digest="0" * 64)))
    must_refuse(lambda: sample_book.decode(replace(sample_cert, context_key="0" * 64)))
    must_refuse(
        lambda: sample_book.decode(
            replace(sample_cert, integer=sample_cert.integer + 1)
        )
    )
    must_refuse(lambda: Context(entry="joined"))
    for mark in ("َ", "ُ", "ِ"):
        assert project("ا" + mark, Context())["status"] == "REJECT"
    assert project("بْ", Context())["status"] == "REJECT"

    summary = {
        "scope": "HISTORICAL_QURANIC_REGRESSION_NOT_STANDARD_ARABIC_COVERAGE",
        "bridge_protocol": PROTOCOL_VERSION,
        "corpus_sha256": SOURCE_SHA,
        "corpus_bytes": len(raw),
        "occurrences": occurrence_count,
        "distinct_forms": len(forms),
        "joined_forms_with_real_left": len(first_left),
        "joined_policy": (
            "first same-line observed preceding token per distinct form; "
            "no inferred vowel or annotation"
        ),
        "stats": dict(stats),
        "reason_counts": dict(reasons),
        "fiber_size_histograms": dict(fiber_hist),
        "largest_fibers": largest,
        "exact_recovery_cases": checked,
        "context_transitions": dict(transitions),
        "short_numbering_cases": len(all_short),
        "minimality_scope": (
            "fixed-length residual conditional on atoms, context and "
            "full shared finite codebook"
        ),
        "whole_word_linguistic_license": False,
        "new_lean_theorems_checked": False,
        "general_language_closure": False,
    }
    (OUT / "joined_provenance.json").write_text(
        json.dumps(first_left, ensure_ascii=False, sort_keys=True)
    )
    (ROOT / "audit_results.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
