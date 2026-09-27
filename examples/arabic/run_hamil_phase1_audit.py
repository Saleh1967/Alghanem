"""تشغيلُ إيداع تدقيق «حلقة ث/ع» الأولى من hamil، وطبعُ أحكامه بالحساب.

    python examples/arabic/run_hamil_phase1_audit.py

والغرضُ أن يُرى الفرقُ بين ثلاثة أجناسٍ كانت تُقرأ واحدًا: ما أُعيد من
الأرقام المنقولة وحدَها، وما أُعيد بتنفيذ هذه الشجرة المستقلّ، وما وقف على
بايتاتٍ لم تُودَع. ولا يُقاس ههنا شيءٌ على `mujammad.txt`، فليست في الشجرة.
"""

from __future__ import annotations

from alghanem.arabic.hamil_phase1_audit_deposit import (
    HAMIL_PHASE1_AUDIT_DEPOSIT,
    THE_CODE_DEFECTS,
    CheckGenus,
    CheckVerdict,
    the_chain_rule_gap,
    the_rate_denominators,
)


def main() -> None:
    deposit = HAMIL_PHASE1_AUDIT_DEPOSIT
    print(
        f"الفحوص {len(deposit.checks)} — "
        f"تطابق {deposit.agreement_count} · "
        f"تخالف {deposit.contradiction_count} · "
        f"تقاطعُ تنفيذين {deposit.cross_checked_count}"
    )
    print()
    for genus in CheckGenus:
        rows = tuple(check for check in deposit.checks if check.genus is genus)
        print(f"[{genus.value}] {len(rows)}")
        for check in rows:
            gap = "—" if check.gap is None else f"{check.gap:+.6g}"
            print(f"  {check.verdict.value:<22} {check.name:<34} فرق {gap}")
        print()
    print(f"خرقُ قاعدة السلسلة: {the_chain_rule_gap():+.4f} بت")
    rates = the_rate_denominators()
    print(
        "ربحُ ماركوف على كلّ مقامٍ معلَن: "
        + " · ".join(f"{name}={value:.4f}" for name, value in sorted(rates.items()))
    )
    print()
    print(f"عيوبُ الشيفرة الموصوفة (لم تُشغَّل ههنا): {len(THE_CODE_DEFECTS)}")
    for defect in THE_CODE_DEFECTS:
        print(f"  [{defect.genus.value}] {defect.locus}")
    print()
    corpus = deposit.corpus
    print(
        f"المدوّنتان: {corpus.their_path} بإزاء {corpus.our_path} — "
        f"فرقُ {corpus.byte_gap:,} بايتًا، وهما ليستا واحدة."
    )
    assert deposit.by_verdict(CheckVerdict.NOT_CHECKABLE_HERE)


if __name__ == "__main__":
    main()
