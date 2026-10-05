"""قارئُ توسيع الموضع: العشرُ كانت خبرًا عن موضعَين، فكم تصمد في أربعة؟

python examples/arabic/read_positional_widening.py
"""

from __future__ import annotations

from alghanem.arabic.blind_skeleton_transport import THE_DEPOSITS_READ
from alghanem.arabic.positional_widening import (
    POSITIONAL_WIDENING_NAMED_RESIDUALS as RESIDUALS,
)
from alghanem.arabic.positional_widening import (
    POSITIONS,
    census_at,
    classes_that_transport_at,
    classes_that_transport_everywhere,
    letters_present_in,
    letters_uncovered_by,
    positional_classes_of,
    shared_classes_of,
    substitutions_refused_in,
    the_classes_only_a_wider_question_finds,
    the_uncovered_set_is_the_same_in_every_deposit,
)

_JOINED = ("init", "medi", "fina")


def _render(classes: tuple[frozenset[str], ...]) -> str:
    return "  ".join(
        "".join(sorted(letters))
        for letters in sorted(classes, key=lambda c: (-len(c), sorted(c)))
    )


def main() -> None:
    """يعرض التغطية، ثمّ الفئات في المواضع الأربعة، ثمّ ما يصمد فيها جميعًا."""

    print("حروفُ كلّ وديعةٍ في نطاق العيّنة العمياء:")
    for filename in THE_DEPOSITS_READ:
        letters = letters_present_in(filename)
        print(f"  {filename:<28}{len(letters):>4}")

    print()
    print("ما لا تغطّيه سمةُ الموضع، والودائعُ تُجمِع عليه:")
    print(f"  {'السمة':<8}{'أميري':>8}{'شهرزاد':>9}{'الكوفيّ':>9}  مُجمَعٌ عليه   المجموعة")
    for position in _JOINED:
        sizes = [
            len(letters_uncovered_by(name, position)) for name in THE_DEPOSITS_READ
        ]
        agreed = the_uncovered_set_is_the_same_in_every_deposit(position)
        found = "".join(sorted(letters_uncovered_by(THE_DEPOSITS_READ[0], position)))
        print(
            f"  {position:<8}{sizes[0]:>8}{sizes[1]:>9}{sizes[2]:>9}"
            f"{'نعم' if agreed else 'لا':>12}   {found}"
        )

    print()
    print("قسمةُ العيّنة في كلّ موضع — مُغطًّى / فئات / ما زاد على حرف:")
    print(f"  {'الملفّ':<28}" + "".join(f"{p:>16}" for p in POSITIONS))
    for filename in THE_DEPOSITS_READ:
        row = "".join(
            f"{c.covered:>6}/{c.classes:<4}{c.shared:<5}"
            for c in (census_at(filename, p) for p in POSITIONS)
        )
        print(f"  {filename:<28}{row}")

    print()
    print("ما يُقاس في كلّ موضع، وديعةً وديعة:")
    for filename in THE_DEPOSITS_READ:
        print(f"  {filename}")
        for position in POSITIONS:
            print(f"    {position:<6}{_render(shared_classes_of(filename, position))}")

    print()
    print("النقلُ إلى الودائع الثلاث، موضعًا موضعًا:")
    for position in POSITIONS:
        found = classes_that_transport_at(position)
        print(f"  {position:<6}{len(found):>3}   {_render(found)}")

    surviving = classes_that_transport_everywhere()
    print()
    print(f"  الأربعةُ جميعًا{len(surviving):>3}   {_render(surviving)}")

    union: set[frozenset[str]] = set()
    for position in POSITIONS:
        union |= set(classes_that_transport_at(position))
    print(f"  واتّحادُها{len(union):>7}   {_render(tuple(union))}")

    print()
    print("وما لا يراه إلّا سؤالٌ أوسع:")
    for letters in the_classes_only_a_wider_question_finds():
        where = [p for p in POSITIONS if letters in classes_that_transport_at(p)]
        absent = [p for p in POSITIONS if p not in where]
        print(
            f"  {''.join(sorted(letters))}  ينتقل في {' '.join(where)}"
            f"  ولا وجودَ له في {' '.join(absent)}"
        )

    print()
    print("وما سقط بالتوسيع، ولمَ سقط:")
    flagship = frozenset("\u0628\u062a\u062b")
    for position in POSITIONS:
        holds = flagship in classes_that_transport_at(position)
        widest = max(
            (
                c
                for c in positional_classes_of(THE_DEPOSITS_READ[0], position)
                if "\u0628" in c
            ),
            key=len,
        )
        print(
            f"  {position:<6}بتث تنتقل: {'نعم' if holds else 'لا':<4}"
            f" وفئةُ ب في أميري: {''.join(sorted(widest))}"
        )

    print()
    print("ما رُفض من الاستبدال ولم يُخمَّن:")
    for filename in THE_DEPOSITS_READ:
        counted = [substitutions_refused_in(filename, p) for p in _JOINED]
        print(f"  {filename:<28}{sum(counted):>3}  {dict(zip(_JOINED, counted))}")

    print()
    print("المتبقّياتُ المسمّاة:")
    for text in RESIDUALS.values():
        print(f"  - {text}")


if __name__ == "__main__":
    main()
