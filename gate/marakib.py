"""المراكبُ الثلاثة: رقمُ الخانة في كلّ مركب، وعددُ الكلمة، وترجمةُ n بينها، والوحدةُ تحمل مركبَها.

مرآةُ `A116.Marakib` (ADR ٩٩). الخانةُ واحدة والرقمُ ثلاثة:

* `jisr`: ترتيبُ البوّابة والشهادة (`gate.bridge.A116`، ء0 … ا28) — وترتيبُ `alghanem-constitution`.
* `khanat`: ترتيبُ `A116.Cells` وحقلِ hamil (ا0 … ي27 ء28) — مشتقٌّ من الجسر
  بتبديل الصفّين كما في `Numbering.swapCarrier`.
* `makharij`: ترتيبُ «الكتاب» في `A116.Jadwal.khanat` (ءهاعحغخقكجشيضلنرطدتزسصظذثفبمو).

العددُ في كلّ مركب ‎F = Σ_{j<n} 116^j + أرقامٌ بالأساس 116‎ (`Numbering.foldAny_zero_closed`)،
والوحدةُ ‎P(رقمُ المركب، F)‎.
"""

from __future__ import annotations

from gate.contextual import A116 as _JISR_ATOMS
from gate.contextual import pair, unpair

MARAKIB: tuple[str, ...] = ("khanat", "jisr", "makharij")
"""رقمُ المركب موضعُه هنا (`Markab.n`)."""

HARAKAT: tuple[str, ...] = ("َ", "ُ", "ِ", "ْ")

_JISR: tuple[str, ...] = tuple(dict.fromkeys(a[0] for a in _JISR_ATOMS))
_KHANAT: tuple[str, ...] = (_JISR[-1], *_JISR[1:-1], _JISR[0])
_MAKHARIJ: tuple[str, ...] = tuple("ءهاعحغخقكجشيضلنرطدتزسصظذثفبمو")

CARRIERS: dict[str, tuple[str, ...]] = {"khanat": _KHANAT, "jisr": _JISR, "makharij": _MAKHARIJ}


class MarkabError(ValueError):
    """رفضٌ مسمًّى: `UNKNOWN_MARKAB`، `ATOM_NOT_IN_A116`، `NONNEGATIVE_INTEGER_REQUIRED`،
    `NOT_A_WAHDA`."""


def _markab(m: str) -> tuple[str, ...]:
    if m not in CARRIERS:
        raise MarkabError("UNKNOWN_MARKAB")
    return CARRIERS[m]


def index(m: str, atom: str) -> int:
    """رقمُ الخانة (حرفٌ ثمّ علامتُه) في المركب: ‎4·الحامل + الحالة‎."""
    carriers = _markab(m)
    if len(atom) != 2 or atom[0] not in carriers or atom[1] not in HARAKAT:
        raise MarkabError("ATOM_NOT_IN_A116")
    return 4 * carriers.index(atom[0]) + HARAKAT.index(atom[1])


def atom_at(m: str, k: int) -> str:
    carriers = _markab(m)
    if type(k) is not int or not 0 <= k < 116:
        raise MarkabError("ATOM_NOT_IN_A116")
    return carriers[k // 4] + HARAKAT[k % 4]


def number(m: str, atoms: tuple[str, ...] | list[str]) -> int:
    """‎F m w‎: عددُ سلسلة الخانات في المركب — تقابلٌ إلى ℕ."""
    offset, power, value = 0, 1, 0
    for a in atoms:
        value = 116 * value + index(m, a)
        offset += power
        power *= 116
    return offset + value


def atoms_of(m: str, n: int) -> tuple[str, ...]:
    """فكُّ ‎F m‎: العددُ ← الخانات."""
    _markab(m)
    if type(n) is not int or n < 0:
        raise MarkabError("NONNEGATIVE_INTEGER_REQUIRED")
    length, capacity = 0, 1
    while n >= capacity:
        n -= capacity
        capacity *= 116
        length += 1
    out = []
    for _ in range(length):
        n, d = divmod(n, 116)
        out.append(atom_at(m, d))
    return tuple(reversed(out))


def tarjim(n: int, src: str, dst: str) -> int:
    """‎tarjim src dst‎: عددُ الكلمة نفسِها في المركب الآخر (`A116.Marakib.tarjim_spec`)."""
    return number(dst, atoms_of(src, n))


def wahda(m: str, atoms: tuple[str, ...] | list[str]) -> int:
    """عددُ الوحدة يحمل مركبَها: ‎P(رقمُ المركب، F)‎ (`wahda_injective`)."""
    _markab(m)
    return pair(MARAKIB.index(m), number(m, atoms))


def wahda_of(n: int) -> tuple[str, tuple[str, ...]]:
    """فكُّ عدد الوحدة: المركبُ وخاناتُ الكلمة — وما ليس عددَ وحدةٍ رفضٌ باسمه."""
    tag, f = unpair(n)
    if tag >= len(MARAKIB):
        raise MarkabError("NOT_A_WAHDA")
    m = MARAKIB[tag]
    return m, atoms_of(m, f)
