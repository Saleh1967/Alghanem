"""ألفُ التأنيث زيادةٌ بعد الأصول (ADR ٥٣) — مرآةُ `A116.Tanith`.

التوقّعاتُ باليد من الكتاب (صحراء حمراء فقهاء أصدقاء — س10720–10731؛ حبلى — س15357) ومن أوزانٍ معروفة
(دنيا فُعْلَى من دنو، رؤيا فُعْلَى من رأي)، ومقابلاتُها التي آخرُها من الأصل (أبناء، أسماء، سماء، أنباء
أَفْعَال أو فَعَال، هدى، فتى). والطفرات: `MUTANT_SHAPE_ONLY` (الشكلُ وحدَه)، `MUTANT_STRICT_WEAK`
(لا يقع الأصلُ المعتلّ حرفَ علّة)، `MUTANT_STRICT_HAMZA` (لا يقع المهموزُ كرسيًّا)،
`MUTANT_ALIF_HAMZA_AS_MAQSURA` (الممدودُ يُقرأ مقصورًا).
"""

from __future__ import annotations

from collections.abc import Callable

from gate import enter
from gate.tanith import (
    HAMZA_LIKE,
    MAMDUDA,
    MAQSURA,
    WEAK_LIKE,
    final_alif,
    in_order,
    rad_match,
    shape,
    skeleton,
    tanith,
)

HAND: dict[tuple[str, str], str | None] = {
    ("صحراء", "صحر"): MAMDUDA, ("حمراء", "حمر"): MAMDUDA, ("فقهاء", "فقه"): MAMDUDA,
    ("اصدقاء", "صدق"): MAMDUDA, ("اولياء", "ولي"): MAMDUDA, ("حبلى", "حبل"): MAQSURA,
    ("بشرى", "بشر"): MAQSURA, ("دنيا", "دنو"): MAQSURA, ("رؤيا", "رءي"): MAQSURA,
    ("ابناء", "بني"): None, ("اسماء", "سمو"): None, ("سماء", "سمو"): None, ("انباء", "نبء"): None,
    ("هدى", "هدي"): None, ("فتى", "فتي"): None, ("كتاب", "كتب"): None,
}


def _agrees(f: Callable[[str, str], str | None]) -> bool:
    return all(f(sk, r) == want for (sk, r), want in HAND.items())


def test_hand_witnesses() -> None:
    assert _agrees(tanith)
    assert tanith("علباء", "علب") == MAMDUDA  # ILHAQ_ALIF: مستثنًى مسمًّى، الكتابُ يردّه


def test_partition_and_needs_final() -> None:
    """`tanith_partition` و`tanith_needs_final` على كلّ هيكلٍ رباعيٍّ من أبجديّةٍ صغيرة."""

    alpha = "ابءيوىلم"
    words = [a + b + c + d for a in alpha for b in alpha for c in alpha for d in "اءى"]
    for sk in words:
        for root in ("بلم", "لمي", "ءلم", "بوم"):
            got = tanith(sk, root)
            f = final_alif(sk)
            if f is None:
                assert got is None
            else:
                assert (got == f[0]) == in_order(f[1], root)


def test_on_certificates() -> None:
    """الهيكلُ من ذرّات الشهادة: الألفُ المقصورةُ ذرّةُ «اْ»، فـ«الْحُسْنَى» تأنيثٌ و«الْهُدَى» من الأصل."""

    hus = skeleton(enter("الْحُسْنَى".encode()).atoms)
    huda = skeleton(enter("الْهُدَى".encode()).atoms)
    abna = skeleton(enter("أَبْنَاءَ".encode()).atoms)
    shuf = skeleton(enter("شُفَعَاءَ".encode()).atoms)
    assert tanith(hus, "حسن") == MAQSURA and tanith(huda, "هدي") is None
    assert shape(abna) and shape(shuf)  # الشكلُ واحد
    assert tanith(abna, "بني") is None and tanith(shuf, "شفع") == MAMDUDA  # والجذرُ يفرّق


def test_mutants_are_caught() -> None:
    def shape_only(sk: str, r: str) -> str | None:
        f = final_alif(sk)
        return f[0] if f else None

    def make(match: Callable[[str, str], bool]) -> Callable[[str, str], str | None]:
        def io(sk: str, root: str) -> bool:
            i = 0
            for c in sk:
                if i < len(root) and match(root[i], c):
                    i += 1
            return i == len(root)

        def f(sk: str, r: str) -> str | None:
            fa = final_alif(sk)
            return fa[0] if fa and io(fa[1], r) else None
        return f

    def strict_weak(r: str, c: str) -> bool:
        return r == c or (r == "ء" and c in HAMZA_LIKE)

    def strict_hamza(r: str, c: str) -> bool:
        return r == c or (r in "وي" and c in WEAK_LIKE)

    def alif_hamza_as_maqsura(sk: str, r: str) -> str | None:
        got = tanith(sk, r)
        return MAQSURA if got else None

    assert _agrees(make(rad_match))  # البناءُ نفسُه يوافق
    for mutant in (shape_only, make(strict_weak), make(strict_hamza), alif_hamza_as_maqsura):
        assert not _agrees(mutant)
