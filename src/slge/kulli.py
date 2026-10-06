"""الكليُّ والجزئيّ: القالبُ كليٌّ وجودُه في أفراده، والجزئيُّ من جدول، والمصدرُ مجرّدٌ من الزمن — مرآةُ `Kulli`.

الكليُّ (الماهية) قالبٌ لا يوجد في الخانات إلّا مملوءًا بجذر (`universal_in_particulars`)؛ الجزئيُّ (الضميرُ
والإشارةُ والموصول) من جدولٍ لا من قالب، والقارئُ يقدّم الجدولَ على القالب؛ الكليُّ العرضيُّ مشتقٌّ على قالب
الوصف والماهويُّ على غيره؛ والمصدرُ حدثٌ مجرّدٌ لا يُقرأ ماضيًا ولا مضارعًا ولا أمرًا (`masdar_no_sigha`) ولا
تدخله أدواتُ الإزاحة. القارئُ `kulli` يقرأ الجهةَ الوجوديّة من الخانة. القياسُ على MASAQ في
`tools/gen_kulli_index.py`.
"""

from __future__ import annotations

from slge.categories import PRONOUNS
from slge.cells import Cell
from slge.filiyya import is_masdar
from slge.jiha import sigha
from slge.jumla import mubtada_kind
from slge.mansubat import derived
from slge.marifa import drop_tanwin
from slge.sarf import on_template
from slge.tawabi import case_class
from slge.uslub import present_any_mood
from slge.wazn import AWZAN, fill, root_of

__all__ = ["kulli"]

Word = tuple[Cell, ...]


def kulli(w: Word) -> str:
    """جزئيٌّ مجدوَل، أو كليٌّ عرضيّ (مشتقّ)، أو حدثٌ مجرّد (مصدر)، أو حدثٌ مهيّأ (فعل)، أو كليٌّ ماهويّ."""

    if w in PRONOUNS or mubtada_kind(w) == "مبني":
        return "جزئيّ"
    if sigha(w) is not None or present_any_mood(w):
        return "حدث مهيّأ"
    if derived(drop_tanwin(w)):
        return "كليّ عرضيّ"
    if is_masdar(w):
        return "حدث مجرّد"
    if case_class(w) != "لا تقرؤه الخانة":
        return "كليّ ماهويّ"
    return "—"


def _check() -> None:
    from slge.rawabit import cells_of

    for k in range(len(AWZAN)):
        t = AWZAN[k].template
        for r in (("ك", "ت", "ب"), ("د", "ر", "س")):  # الكليُّ في أفراده
            assert on_template(k, fill(t, r)) and root_of(t, fill(t, r)) == r
    assert kulli(cells_of("هُوَ")) == "جزئيّ" and kulli(cells_of("هَذَا")) == "جزئيّ"
    assert kulli(cells_of("نَحْنُ")) == "جزئيّ"  # يشابه فَعْلُ بالخانة والجدولُ يفصله
    assert kulli(cells_of("كَاتِبٌ")) == "كليّ عرضيّ" and kulli(cells_of("كِتَابَةٌ")) == "حدث مجرّد"
    assert kulli(cells_of("ضَرْبٌ")) == "حدث مجرّد"
    for w in ("كَتَبَ", "يَكْتُبُ", "اُكْتُبْ", "يَكْتُبْ"):
        assert kulli(cells_of(w)) == "حدث مهيّأ", w
    assert kulli(cells_of("رَجُلٌ")) == "كليّ ماهويّ" and kulli(cells_of("اَرَّجُلُ")) == "كليّ ماهويّ"
    assert kulli(cells_of("لَا")) == "—"
    from slge.filiyya import MASDAR_TEMPLATES
    from slge.jiha import shift
    for k in MASDAR_TEMPLATES:
        m = fill(AWZAN[k].template, ("ك", "ت", "ب"))
        assert sigha(m) is None and all(shift(s, m) is None for s in ("س", "لم", "لن", "كان"))


_check()
