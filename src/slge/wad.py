"""الوضعُ والمشتركُ والترادف: الوضعُ ملءُ قالبٍ بجذر، والمشتركُ ما قرأته قالبان، والمترادفان صورتان لجذر —
مرآةُ `Wad`.

الوضعُ على الخانات `fill t r` متباينٌ في الجذر (`wad_injective`) ويُستردّ قالبُه من الكلمة
(`sense_of_fill`).
المشتركُ على مرتبتين: اشتراكُ الوضع — القالبُ الواحد مودَعٌ لأكثر من باب (ستّةُ أزواجٍ متطابقة
`duplicate_templates`)؛ واشتراكُ الصورة — قالبان مختلفان يلتقيان في كلمة (اِنْتِشَارٌ، مَنْحَةٌ)، والالتقاءُ
محصورٌ بشرطٍ على الرمزين (`may_collide`، `mayCollide_sound`) وأزواجُه 42 بعينها (`collision_pairs_eq`).
الميزانُ لا يُشترَك (`mizan_unaided`). المترادفان الصرفيّان يشتركان في الجذر ويختلفان في الصورة
(`taraduf_same_root`، `masdar_forms_distinct`). القارئُ `wad` يقرأ الوضعَ من الخانة بعد ردّ التنوين.
القياسُ على MASAQ في `tools/gen_wad_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.categories import PRONOUNS
from slge.cells import Cell
from slge.jumla import mubtada_kind
from slge.maqam import _on_template_root as on_template_root
from slge.marifa import drop_tanwin
from slge.wazn import AWZAN, Sym, Template, fill, mizan, root_of

__all__ = ["classes", "collision_pairs", "duplicates", "may_collide", "senses", "unaided", "wad"]

Word = tuple[Cell, ...]
_TEMPLATES: Final[tuple[Template, ...]] = tuple(w.template for w in AWZAN)


def senses(w: Word) -> tuple[int, ...]:
    """معاني الكلمة: أرقامُ القوالب التي تقرؤها بجذرٍ لا ألفَ فيه."""

    return tuple(k for k in range(len(AWZAN)) if on_template_root(k, w))


def classes(w: Word) -> tuple[int, ...]:
    """صورُ الكلمة: معانيها بعد طيّ القوالب المتطابقة إلى أوّلها."""

    return tuple(k for k in senses(w) if all(_TEMPLATES[q] != _TEMPLATES[k] for q in range(k)))


def unaided(w: Word) -> bool:
    """الفهمُ بلا قرينة: قالبٌ واحد يقرؤها."""

    return len(senses(w)) == 1


def _compat(a: Sym, b: Sym) -> bool:
    if a.slot is None and b.slot is None:
        return a.carrier == b.carrier and a.state == b.state
    if a.slot is None:
        return a.carrier != "ا" and a.state == b.state
    if b.slot is None:
        return b.carrier != "ا" and a.state == b.state
    return a.state == b.state


def may_collide(t: Template, u: Template) -> bool:
    """قالبان قد يلتقيان في كلمة: تساوي الطول، ورمزٌ برمز (زائدان متساويان، أو زائدٌ غيرُ ألفٍ بحالة
    الموضع، أو موضعان بحالةٍ واحدة)."""

    return len(t) == len(u) and all(_compat(a, b) for a, b in zip(t, u, strict=True))


def duplicates() -> tuple[tuple[int, int], ...]:
    """أزواجُ القوالب المتطابقة (اشتراكُ الوضع)."""

    n = len(AWZAN)
    return tuple((k, q) for k in range(n) for q in range(k + 1, n)
                 if _TEMPLATES[k] == _TEMPLATES[q])


def collision_pairs() -> tuple[tuple[int, int], ...]:
    """أزواجُ القوالب التي قد تلتقي (`k < q`)."""

    n = len(AWZAN)
    return tuple((k, q) for k in range(n) for q in range(k + 1, n)
                 if may_collide(_TEMPLATES[k], _TEMPLATES[q]))


def wad(w: Word) -> str:
    """مجدوَل، أو مفردُ الوضع، أو مشتركُ الوضع (صورةٌ واحدةٌ لأكثر من باب)، أو مشتركُ الصورة (قالبان
    مختلفان)، أو لا يُقرأ — بعد ردّ التنوين."""

    if w in PRONOUNS or mubtada_kind(w) == "مبني":
        return "مجدوَل"
    v = drop_tanwin(w)
    n = len(senses(v))
    if n == 0:
        return "—"
    if n == 1:
        return "مفرد الوضع"
    return "مشترك الوضع" if len(classes(v)) == 1 else "مشترك الصورة"


def _check() -> None:
    from slge.rawabit import cells_of

    t = AWZAN[0].template
    assert fill(t, ("ك", "ت", "ب")) != fill(t, ("د", "ر", "س"))  # الوضعُ متباينٌ في الجذر
    assert root_of(t, fill(t, ("ك", "ت", "ب"))) == ("ك", "ت", "ب")
    for k in range(len(AWZAN)):
        assert k in senses(fill(AWZAN[k].template, ("ك", "ت", "ب")))  # الموضوعُ يُستردّ
        assert len(classes(mizan(AWZAN[k].template))) == 1  # الميزانُ لا يُشترَك
    assert duplicates() == ((30, 94), (35, 41), (35, 93), (41, 93), (51, 60), (64, 86))
    pairs = collision_pairs()
    assert len(pairs) == 42 and all(p in pairs for p in duplicates())
    assert sum(_TEMPLATES[k] != _TEMPLATES[q] for k, q in pairs) == 36
    intishar = drop_tanwin(cells_of("اِنْتِشَارٌ"))
    assert fill(AWZAN[44].template, ("ت", "ش", "ر")) == intishar
    assert fill(AWZAN[45].template, ("ن", "ش", "ر")) == intishar and (44, 45) in pairs
    assert wad(cells_of("اِنْتِشَارٌ")) == "مشترك الصورة" and wad(cells_of("مَنْحَةٌ")) == "مشترك الصورة"
    assert wad(cells_of("كِتَابٌ")) == "مشترك الوضع" and wad(cells_of("هِلَالٌ")) == "مشترك الوضع"
    for w in ("عَيْنٌ", "قَمَرٌ", "كَاتِبٌ", "يَكْتُبُ", "ءَامَنَ"):  # آمَنَ: فَاعَلَ بالخانة، وأَفْعَلَ تقتضي ألفًا في الجذر
        assert wad(cells_of(w)) == "مفرد الوضع", w
    assert wad(cells_of("هُوَ")) == "مجدوَل" and wad(cells_of("هَذَا")) == "مجدوَل"
    assert wad(cells_of("لَا")) == "—"


_check()
