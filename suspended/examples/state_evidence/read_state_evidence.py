"""اقرأ سطحًا عربيًّا، وأخرِج لكلّ حالةِ حاملٍ جنسَ سببِها لا الحالةَ وحدَها.

سكربتٌ مرجعيٌّ لا سلطةَ له: لا يُولِّد ولا يُجمِّد ولا يُصدر حكمًا، ولا يقرؤه
شيءٌ في `kernel/`. وهو يُظهِر ما كان مطويًّا في `CarrierState` وحدَها:

* **علامةٌ مكتوبة**: حالةٌ قرأها السطحُ فعلًا، ومعها موضعُ علامتها.
* **افتراضٌ عند الغياب**: حالةٌ أنتجها المولِّدُ حيث لا علامةَ أصلًا.
* **متعذِّر**: ألفٌ تفتتح حواملَ بلا علامة، فلا تُقرأ ساكنةً ولا متحرّكة.

ويُخرِج معها تصنيفَ مواضع الرفض القائمة في المولِّد المُودَع إلى شرطٍ ومانعٍ
ومتعذِّر، مُشتقًّا من شجرة نحوه لا من قائمةٍ مكتوبةٍ يدًا.

    python examples/state_evidence/read_state_evidence.py الْحَمْدُ

فإن لم يُمرَّر سطحٌ قُرئت السطوحُ المضمَّنة في `EMBEDDED_ROUND_TRIP_CASES`.
"""

from __future__ import annotations

import argparse
from collections import Counter

from alghanem.arabic.encoding.carrier_state_candidate import (
    EMBEDDED_ROUND_TRIP_CASES,
)
from alghanem.arabic.encoding.state_evidence import (
    REFUSAL_GENUS_REGISTRY,
    STATE_EVIDENCE_NAMED_RESIDUALS,
    EvidencingReader,
    RefusalGenus,
    StateEvidence,
    derive_observed_capacities,
    derive_refusal_sites,
    derive_unclassified_refusal_sites,
)


def _report_refusal_genera() -> None:
    sites = derive_refusal_sites()
    counts = Counter(REFUSAL_GENUS_REGISTRY[site].arabic_name for site in sites)
    print(f"مواضعُ الرفض القائمة في المولِّد المُودَع: {len(sites)}")
    for genus in RefusalGenus:
        print(f"  {genus.arabic_name}: {counts.get(genus.arabic_name, 0)}")
    unclassified = derive_unclassified_refusal_sites()
    if unclassified:
        print("  مواضعُ بلا جنسٍ مُسمًّى:")
        for site in unclassified:
            print(f"    {site.function}: {site.message}")
    else:
        print("  لا موضعَ رفضٍ بلا جنسٍ مُسمًّى.")


def _report_surface(surface: str) -> None:
    print(f"\n{surface}")
    for item in EvidencingReader().read(surface):
        if item.evidence is None:
            carried = "، ".join(str(mark.offset) for mark in item.marks)
            note = f" (علاماتٌ يتيمةٌ عند {carried})" if item.marks else ""
            print(f"  {item.unit.carrier}  عابرٌ، لا حالةَ حاملٍ له{note}")
            continue
        places = "، ".join(str(mark.offset) for mark in item.marks) or "لا موضع"
        print(
            f"  {item.unit.carrier}  {item.unit.state.value:16}"
            f"  {item.evidence.arabic_name}  [{places}]"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("surfaces", nargs="*", help="سطوحٌ عربيّةٌ تُقرأ")
    surfaces = tuple(parser.parse_args().surfaces) or EMBEDDED_ROUND_TRIP_CASES

    _report_refusal_genera()
    for surface in surfaces:
        _report_surface(surface)

    read = tuple(
        item for surface in surfaces for item in EvidencingReader().read(surface)
    )
    stated = tuple(item for item in read if item.evidence is not None)
    written = sum(1 for item in stated if item.evidence is StateEvidence.WRITTEN_MARK)
    print(f"\nحالاتٌ مقروءة: {len(stated)}")
    print(f"  منها بعلامةٍ مكتوبة: {written}")
    print(f"  ومنها بلا علامةٍ البتّة: {len(stated) - written}")

    census = derive_observed_capacities(surfaces)
    print(
        f"قابليّةٌ مرصودة: {len(census.observed)} حاملًا حمل علامةً، "
        f"و{len(census.unobserved_pairs())} زوجًا لم يُرصَد — غيرَ مرصودٍ لا ممتنعًا."
    )
    print("\nمُخلَّفاتٌ مُسمّاة:")
    for name in STATE_EVIDENCE_NAMED_RESIDUALS:
        print(f"  {name}")


if __name__ == "__main__":
    main()
