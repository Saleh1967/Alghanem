"""الجملةُ الفعليّة: نواةٌ من الخانة، ورتبةٌ ثلاثيّة، ونيابةٌ عمليّتان، ومفاعيلُ نصبٌ — مرآةُ `Filiyya.lean`.

الماضي مبنيٌّ وآخرُه تقرؤه لاحقتُه (`past_ending`، `past`)؛ والمضارعُ معربٌ (في `jazm`/`afal`)؛ والأمرُ
مبنيٌّ على ما يُجزم به مضارعُه (`fil.amr_of`). الفاعلُ رفعٌ (`fail`) وصورُه: ظاهرٌ، بارزٌ متّصلٌ بحالة ما
قبله (`has_subject`)، مستترٌ لا خانةَ له. الرتبةُ الثلاثيّةُ من الخانات لا من الموضع (`order`): الفاعلُ
متّصلٌ أو العلامةُ خفيّةٌ ⇒ الفاعلُ أوّلًا؛ المفعولُ متّصلٌ أو العائدُ في الفاعل ⇒ المفعولُ أوّلًا؛
اسمُ الصدارة ⇒ قبل الفعل؛ وما سواه جواز. المجهولُ عمليّتان على الحالات (`majhul`، `majhul_pres`)،
والنائبُ بالرفع نفسِه ويقرؤه جدولُه (`naib_kind`). المفاعيلُ نصبٌ وتنوين (`maful`): الظرفُ من جداوله،
والمصدرُ من قالبه لا المشتقّ (`sort_fadla`)، والمعيّةُ واوٌ متّصلة (`maiyya`؛ والمشاركةُ على تَفَاعَلَ عطفٌ)،
والمطلقُ
مصدرُ الفعل بجذره (`mutlaq`). القياسُ على MASAQ في `tools/gen_filiyya_index.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.damair import ATTACHED_RAF
from slge.fil import MAZID_AMR, MAZID_PRES, amr_of
from slge.jumla import _AID, bare, has_aid_pronoun, istifham, shibh_jumla
from slge.mansubat import derived
from slge.marifa import drop_tanwin
from slge.nawasikh import nasb, raf, tanwin
from slge.rawabit import cells_of
from slge.sarf import on_template
from slge.tawabi import case_class
from slge.wazn import AWZAN, Template, fill, root_of
from slge.zaman import CONSTANTS as ZAMAN_CONSTANTS
from slge.zaman import STEMS as ZAMAN_STEMS
from slge.zaman import nasb_tanwin
from slge.zuruf import CONSTANTS as ZURUF_CONSTANTS
from slge.zuruf import STEMS as ZURUF_STEMS
from slge.zuruf import mudaf, set_last

__all__ = ["MASDAR_TEMPLATES", "OBJECT_SUFFIXES", "SUBJECT_SUFFIXES", "WITNESSES", "Filiyya",
           "admissible", "amr_ends_like_jazm", "fail", "has_object", "has_subject", "is_masdar",
           "is_zarf", "maful", "maiyya", "majhul", "majhul_pres", "mutlaq", "naib", "naib_kind",
           "order", "past", "past_ending", "sort_fadla", "tafaala", "verb_root"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]

# — الفعل —

SUBJECT_SUFFIXES: Final[tuple[tuple[Word, str], ...]] = (
    *((p.cells, SUKUN) for p in ATTACHED_RAF[:6]),
    ((("و", SUKUN),), _U), ((("ا", SUKUN),), _A), ((("ن", _A),), SUKUN), ((("ي", SUKUN),), _I),
    ((("ن", _A), ("ا", SUKUN)), SUKUN),
    ((("و", SUKUN), ("ن", _A)), _U), ((("ي", SUKUN), ("ن", _A)), _I),
    ((("ا", SUKUN), ("ن", _I)), _A),
)
"""لواحقُ الفاعل البارز بحالة ما قبلها: الأحدَ عشرَ من `damair.ATTACHED_RAF` ثمّ لواحقُ المضارع."""

_NI: Final[Word] = (("ن", _I), ("ي", SUKUN))
OBJECT_SUFFIXES: Final[tuple[Word, ...]] = (_NI, *_AID)


def past_ending(suffix: Word) -> str:
    """آخرُ الماضي قبل اللاحقة: فتحٌ بلا لاحقة، سكونٌ قبل التاء ونَا ونون النسوة، ضمٌّ قبل واو الجماعة."""

    if not suffix:
        return _A
    if suffix == (("و", SUKUN),):
        return _U
    if suffix[0][0] == "ت" or suffix in ((("ن", _A), ("ا", SUKUN)), (("ن", _A),)):
        return SUKUN
    if suffix == (("ا", SUKUN),):
        return _A
    return "—"


def past(stem: Word, suffix: Word) -> Word:
    st = past_ending(suffix)
    return (*set_last(stem, _A if st == "—" else st), *suffix)


def amr_ends_like_jazm() -> bool:
    """آخرُ كلّ قالب أمرٍ مودَعٍ ساكنٌ، كآخر المضارع المجزوم."""

    amr: tuple[int, ...] = (8, 9, 10, *MAZID_AMR)
    return all(AWZAN[k].template[-1].state == SUKUN for k in amr) and all(
        amr_of(AWZAN[p].template)[-1].state == SUKUN for p in MAZID_PRES)


# — الفاعل —


def fail(w: Word) -> Word:
    return raf(w)


def _ends_with_state(v: Word, p: Word, st: str) -> bool:
    return len(p) < len(v) and v[-len(p):] == p and v[-len(p) - 1][1] == st


def has_subject(v: Word) -> bool:
    """فاعلٌ بارزٌ متّصل: لاحقةٌ بحالة ما قبلها؛ وـنِي مفعولٌ لا مخاطبة."""

    return any(_ends_with_state(v, p, st) for p, st in SUBJECT_SUFFIXES) and v[-2:] != _NI


def has_object(v: Word) -> bool:
    """مفعولٌ متّصل: لاحقةٌ من جدول النصب أو ـنِي بعد متحرّك."""

    return any(len(p) < len(v) and v[-len(p):] == p and v[-len(p) - 1][1] != SUKUN
               for p in OBJECT_SUFFIXES)


# — الرتبة —


@dataclass(frozen=True, slots=True)
class Filiyya:
    fil: Word
    fail: Word
    maful: Word
    pos: str = "ف س١ س٢"  # "ف س١ س٢" | "ف س٢ س١" | "س٢ ف س١"


def _hidden(w: Word) -> bool:
    return case_class(w) == "لا تقرؤه الخانة"


def order(j: Filiyya) -> str:
    """الرتبةُ من الخانات: كما في الحصر (أ، ب، ج) والجواز."""

    if istifham(j.maful):
        return "المفعول قبل الفعل"
    if has_subject(j.fil) and not has_object(j.fil):
        return "الفاعل أولًا"
    if has_object(j.fil) and not has_subject(j.fil):
        return "المفعول أولًا"
    if has_aid_pronoun(j.fail):
        return "المفعول أولًا"
    if _hidden(j.fail) and _hidden(j.maful):
        return "الفاعل أولًا"
    return "جواز"


def admissible(j: Filiyya) -> bool:
    r = order(j)
    need = {"الفاعل أولًا": "ف س١ س٢", "المفعول أولًا": "ف س٢ س١", "المفعول قبل الفعل": "س٢ ف س١"}
    return r == "جواز" or j.pos == need[r]


# — النيابة —


def majhul(w: Word) -> Word:
    """ضمُّ الأوّل وكسرُ ما قبل الآخر (كَتَبَ ← كُتِبَ)."""

    if len(w) < 2:
        return w
    out = [(w[0][0], _U), *w[1:]]
    out[-2] = (out[-2][0], _I)
    return tuple(out)


def majhul_pres(w: Word) -> Word:
    """ضمُّ الأوّل وفتحُ ما قبل الآخر (يَكْتُبُ ← يُكْتَبُ)."""

    if len(w) < 2:
        return w
    out = [(w[0][0], _U), *w[1:]]
    out[-2] = (out[-2][0], _A)
    return tuple(out)


def naib(w: Word) -> Word:
    return raf(w)


MASDAR_TEMPLATES: Final[tuple[int, ...]] = (*range(29, 48), 63, 64, 65)
_ZURUF: Final[frozenset[Word]] = frozenset(mudaf(z.stem) for z in ZURUF_STEMS)
_ZAMAN: Final[frozenset[Word]] = frozenset(
    op(s) for s in ZAMAN_STEMS.values() for op in (nasb_tanwin, mudaf))


def is_masdar(w: Word) -> bool:
    b = set_last(drop_tanwin(bare(w)), _U)
    return any(on_template(k, b) for k in MASDAR_TEMPLATES)


_MABNI_ZARF: Final[frozenset[Word]] = frozenset(ZURUF_CONSTANTS.values()) | frozenset(
    v[0] for v in ZAMAN_CONSTANTS.values())


def _is_zarf_bare(w: Word) -> bool:
    return set_last(w, _A) in _ZURUF or w in _ZAMAN or set_last(w, _A) in _ZAMAN or w in _MABNI_ZARF


def is_zarf(w: Word) -> bool:
    """الظرفُ من الجداول: المعربُ بالنصب والمبنيّ (إِذْ، إِذَا…)، والمضافُ إلى الضمير بعد إسقاطه."""

    return _is_zarf_bare(w) or any(
        len(p) < len(w) and w[-len(p):] == p and _is_zarf_bare(w[: -len(p)]) for p in _AID)


def naib_kind(w: Word) -> str:
    """النائبُ من جدوله وصدره: ظرفٌ، مجرورٌ، مصدرٌ، وإلّا فالمفعولُ به؛ والترتيبُ معلَن."""

    if is_zarf(w):
        return "ظرف"
    if shibh_jumla(w):
        return "مجرور"
    if is_masdar(w):
        return "مصدر"
    return "مفعول به"


# — المفاعيل —


def maful(w: Word) -> Word:
    return tanwin(nasb(w))


def _root_on(ks: tuple[int, ...], w: Word) -> tuple[str, str, str] | None:
    for k in ks:
        if on_template(k, w):
            r = root_of(AWZAN[k].template, w)
            if r is not None:
                return r
    return None


_VERB_TEMPLATES: Final[tuple[int, ...]] = tuple(range(29))


def verb_root(v: Word) -> tuple[str, str, str] | None:
    """جذرُ الفعل: بعينه، أو بعد إسقاط لاحقةٍ من الجدولين وردِّ آخره فتحًا أو ضمًّا."""

    cands = [v]
    for p in (*(p for p, _ in SUBJECT_SUFFIXES), *OBJECT_SUFFIXES):
        if len(p) < len(v) and v[-len(p):] == p:
            cands += [set_last(v[: -len(p)], _A), set_last(v[: -len(p)], _U)]
    return next((r for r in (_root_on(_VERB_TEMPLATES, c) for c in cands) if r is not None), None)


def masdar_root(w: Word) -> tuple[str, str, str] | None:
    return _root_on(MASDAR_TEMPLATES, set_last(drop_tanwin(bare(w)), _U))


def sort_fadla(w: Word, v: Word = ()) -> str:
    """قانونُ الفرز: مشتقٌّ على قالب الوصف ⇒ حال؛ مصدرٌ بجذر الفعل ⇒ مطلق؛ مصدرٌ بغيره ⇒ لأجله."""

    if derived(drop_tanwin(w)):
        return "حال"
    r = masdar_root(w)
    if r is None:
        return "—"
    return "مفعول مطلق" if r == verb_root(v) else "مفعول لأجله"


def maiyya(w: Word) -> Word:
    return (("و", _A), *nasb(w))


def tafaala(v: Word) -> bool:
    """فعلُ المشاركة على تَفَاعَلَ: الواوُ بعده عطفٌ لا معيّة."""

    return on_template(15, v)


def mutlaq(k: int, root: tuple[str, str, str]) -> Word:
    return maful(fill(AWZAN[k].template, root))


def _t(k: int) -> Template:
    return AWZAN[k].template


WITNESSES: Final[dict[str, Filiyya]] = {
    "كَتَبْتُ الدَّرْسَ": Filiyya(cells_of("كَتَبْتُ"), (), cells_of("اَدَّرْسَ")),
    "ضَرَبَ مُوسَى عِيسَى": Filiyya(cells_of("ضَرَبَ"), cells_of("مُوْسَى"), cells_of("عِيْسَى")),
    "سَكَنَ الدَّارَ صَاحِبُهَا": Filiyya(cells_of("سَكَنَ"), cells_of("صَاحِبُهَا"), cells_of("اَدَّارَ"),
                                     "ف س٢ س١"),
    "أَكْرَمَنِي أَبُوكَ": Filiyya(cells_of("أَكْرَمَنِي"), cells_of("أَبُوْكَ"), (), "ف س٢ س١"),
    "أَيَّ رَجُلٍ قَابَلْتَ": Filiyya(cells_of("قَابَلْتَ"), (), cells_of("أَيَّ"), "س٢ ف س١"),
    "أَكَلَ زَيْدٌ تُفَّاحَةً": Filiyya(cells_of("أَكَلَ"), cells_of("زَيْدٌ"), cells_of("تُفَّاحَةً")),
}


def _check() -> None:
    expected = ("الفاعل أولًا", "الفاعل أولًا", "المفعول أولًا", "المفعول أولًا", "المفعول قبل الفعل",
                "جواز")
    for (name, j), r in zip(WITNESSES.items(), expected, strict=True):
        if order(j) != r or not admissible(j):
            raise ValueError(f"ORDER:{name}")
    assert amr_ends_like_jazm()
    kataba = cells_of("كَتَبَ")
    assert past(kataba, cells_of("تُ")) == cells_of("كَتَبْتُ")
    assert past(kataba, cells_of("وْ")) == cells_of("كَتَبُوْ")
    assert majhul(kataba) == cells_of("كُتِبَ") and majhul_pres(cells_of("يَكْتُبُ")) == cells_of("يُكْتَبُ")
    assert majhul(fill(_t(0), ("ك", "ت", "ب"))) == fill(_t(3), ("ك", "ت", "ب"))
    assert naib_kind(cells_of("يَوْمُ")) == "ظرف" and naib_kind(cells_of("فَهْمٌ")) == "مصدر"
    assert sort_fadla(cells_of("رَغْبَةً"), cells_of("دَرَسْتُ")) == "مفعول لأجله"
    assert sort_fadla(cells_of("رَاغِبًا"), cells_of("قُمْتُ")) == "حال"
    assert sort_fadla(cells_of("ضَرْبًا"), cells_of("ضَرَبْتُ")) == "مفعول مطلق"
    assert licensed(maiyya(cells_of("اَنَّهْرَ"))) and tafaala(cells_of("تَخَاصَمَ"))
    assert mutlaq(29, ("ض", "ر", "ب")) == cells_of("ضَرْبًا")
    assert root_of(_t(29), fill(_t(29), ("ض", "ر", "ب"))) == ("ض", "ر", "ب")


_check()
