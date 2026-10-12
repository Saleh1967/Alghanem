"""القانونُ على الأشجار (`A116.NizamTree`، ADR ٣٠): ترخيصُ الشجرة ترخيصُ تسطيحها بشروط حدودها.

التوقّعاتُ مستقلّةٌ عن Lean: قاعدةُ الشجرة مكتوبةٌ هنا **بنيويًّا** — لكلّ أبٍ، بين كلّ ابنين
متجاورين حدٌّ: لا (مدّ، مُغلِق) عابرٌ (آخرُ ورقةٍ في الأوّل، أوّلُ ورقةٍ في الثاني)، ولا (مدّ، مُغلِق)
آخرَ الورقة الأخيرة في الأوّل داخلَها؛ والأصنافُ من السطر موصولًا — وتُقابَل بالبوّابة
(`strict_licensed` وكلُّ `straddles` بين السابق كلِّه واللاحق كلِّه):
١. كلُّ تجميعٍ لثلاث كلماتٍ من {بَ، بْ، تْ، اْ} بطول 1 … 2 (سبعةُ أشكال، منها العمقُ الثلاثة):
   القاعدةُ البنيويّة تساوي البوّابةَ على أوراقها — فإعادةُ التجميع لا تغيّر الترخيص
   (`tree_eq_line`، `regroup_invariant`).
٢. شجرةٌ عمقُها واحدٌ من ورقتين هي `strict_joined` بعينه (`tree_two`).
٣. الطفرتان: حدودُ الجذر وحدَه (`MUTANT_SEAM_ROOT_ONLY`)، وأصنافُ كلّ ورقةٍ وحدَها لا السطر
   (`MUTANT_LOCAL_KINDS`).
"""

from __future__ import annotations

from itertools import product

from gate.licence import SUKUN, kind_of, straddles, strict_joined, strict_licensed

ALPHABET = ("بَ", "بْ", "تْ", "ا" + SUKUN)
Word = tuple[str, ...]
Tree = Word | list["Tree"]


def words(max_len: int) -> list[Word]:
    return [w for n in range(1, max_len + 1) for w in product(ALPHABET, repeat=n)]


def leaves(t: Tree) -> list[Word]:
    if isinstance(t, tuple):
        return [t]
    return [w for c in t for w in leaves(c)]


def tree_rule(t: Tree, root_only: bool = False, local_kinds: bool = False) -> bool:
    ls = leaves(t)
    flat = tuple(a for w in ls for a in w)
    if not strict_licensed(flat):
        return False
    k = [x for w in ls for x in kind_of(w)] if local_kinds else kind_of(flat)

    def walk(node: Tree, start: int, depth: int) -> bool:
        if isinstance(node, tuple):
            return True
        pos = start
        for i, child in enumerate(node):
            child_len = sum(len(w) for w in leaves(child))
            if not (root_only and depth > 0) and not walk(child, pos, depth + 1):
                return False
            pos += child_len
            if i + 1 < len(node) and not (root_only and depth > 0):
                last = leaves(child)[-1]
                if k[pos - 1] == "v" and k[pos] == "c":
                    return False
                if len(last) >= 2 and k[pos - 2] == "v" and k[pos - 1] == "c":
                    return False
        return True

    return walk(t, 0, 0)


def gate_line(ws: list[Word]) -> bool:
    flat = tuple(a for w in ws for a in w)
    if not strict_licensed(flat):
        return False
    for i in range(1, len(ws)):
        if straddles(tuple(a for w in ws[:i] for a in w), tuple(a for w in ws[i:] for a in w)):
            return False
    return True


def shapes(a: Word, b: Word, c: Word) -> list[Tree]:
    return [[a, b, c], [[a, b], c], [a, [b, c]], [[a], [b, c]], [[[a, b]], c],
            [a, [[b], [c]]], [[a, [b]], [c]]]


W2 = words(2)
TRIPLES = [(a, b, c) for a in W2 for b in W2 for c in W2]


def test_every_grouping_is_its_line() -> None:
    for a, b, c in TRIPLES:
        expected = gate_line([a, b, c])
        for t in shapes(a, b, c):
            assert tree_rule(t) == expected, t


def test_depth_one_two_leaves_is_strict_joined() -> None:
    for left in words(3):
        for right in words(3):
            assert tree_rule([left, right]) == strict_joined(left, right), (left, right)


def test_named_mutants_disagree() -> None:
    trees = [t for a, b, c in TRIPLES for t in shapes(a, b, c)]
    # MUTANT_SEAM_ROOT_ONLY
    assert any(tree_rule(t, root_only=True) != gate_line(leaves(t)) for t in trees)
    # MUTANT_LOCAL_KINDS
    assert any(tree_rule(t, local_kinds=True) != gate_line(leaves(t)) for t in trees)
