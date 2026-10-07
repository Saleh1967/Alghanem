"""الجهةُ الوجوديّة للقوالب: المصدرُ والمشتقُّ والجامدُ تقسيمًا مغلقًا على الـ125 — مرآةُ `Wujud`.

كلُّ قالبٍ على صنفٍ واحد من ستّة (`ONT`، من بابه المودَع — معلَن): فعل، مصدر، وصفٌ مشتقّ، ظرفٌ
وآلة (الزمانُ والمكانُ والآلة)، جمعٌ (صيغةٌ لا نوع)، اسمٌ (مصدرٌ أو جامدٌ لا تفصله الخانة —
الجمودُ قيدٌ معجميّ). المبرهَن: الفعلُ هو قوائمُ الماضي والمضارع والأمر (`fil_eq`)، والمصدرُ
قوالبُ `MASDAR_TEMPLATES` (`masdar_eq`)، والوصفُ داخل قوالب الوصف إلّا فُعَلَاء
(`wasf_derived`)؛ كلُّ فعلٍ له صيغةٌ على ميزانه ولا صيغةَ لمصدر (`fil_sigha_mizan`،
`masdar_no_sigha_mizan`)؛ أصلُ الشبكة مصدرٌ ولا شيءَ ينحدر من اسمٍ أو جمع (`root_masdar`،
`ism_jam_leaves`)، والمشتقُّ أبوه فعلٌ أو مشتقّ (`mushtaqq_from_fil_or_mushtaqq`)؛ والكليُّ يقرأ
الجهةَ على الميزان إلّا 14 بأرقامها (`kulli_agreement`). جهةُ القراءة من قوالبها
(`ont_of_reading`)، والترتيبُ بجهةٍ لا يُسقط (`mem_rank`، `length_rank`). القياسُ على المودَع
وعلى وسوم MASAQ في `tools/gen_wujud_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.jidh import Reading
from slge.wazn import AWZAN
from slge.wujud_table import ONT

__all__ = ["FIL", "ISM", "JAM", "KIND_OF", "MASDAR", "ONT", "WASF", "ZARF", "of_class", "ont_of",
           "ont_of_reading", "rank"]

FIL, MASDAR, WASF, ZARF, JAM, ISM = "فعل", "مصدر", "وصف", "ظرف وآلة", "جمع", "اسم"
KIND_OF: Final[dict[str, str]] = {FIL: "حدث مهيّأ", MASDAR: "حدث مجرّد", WASF: "كليّ عرضيّ",
                                  ZARF: "كليّ ماهويّ", JAM: "كليّ ماهويّ", ISM: "كليّ ماهويّ"}
"""جهةُ القارئ `kulli` التي تقابل الصنفَ المودَع (`kindOf`)."""


def ont_of(k: int) -> str:
    """صنفُ القالب (`ontOf`)."""

    return ONT[k] if 0 <= k < len(ONT) else ISM


def of_class(o: str) -> tuple[int, ...]:
    return tuple(k for k in range(len(AWZAN)) if ont_of(k) == o)


def ont_of_reading(rd: Reading) -> str:
    """جهةُ القراءة: الفعلُ إن كان فيها قالبُ فعل، وإلّا جهةُ قالبها الأوّل (`ontOfReading`)."""

    if any(ont_of(k) == FIL for k in rd.templates):
        return FIL
    return ont_of(rd.templates[0]) if rd.templates else ISM


def rank(o: str, rs: tuple[Reading, ...]) -> tuple[Reading, ...]:
    """الجهةُ المطلوبة أوّلًا ثمّ الباقي بترتيبه — لا تسقط قراءة (`rank`)."""

    return (*(r for r in rs if ont_of_reading(r) == o), *(r for r in rs if ont_of_reading(r) != o))


def _check() -> None:
    from slge.filiyya import MASDAR_TEMPLATES
    from slge.jidh import jidh
    from slge.kulli import kulli
    from slge.mansubat import DERIVED
    from slge.maqam import AMR_TEMPLATES, PAST_TEMPLATES, PRESENT_TEMPLATES
    from slge.rawabit import cells_of
    from slge.wazn import mizan

    assert len(ONT) == len(AWZAN) == 125
    assert set(of_class(FIL)) == set(PAST_TEMPLATES) | set(PRESENT_TEMPLATES) | set(AMR_TEMPLATES)
    assert set(of_class(MASDAR)) == set(MASDAR_TEMPLATES)
    assert set(of_class(WASF)) <= set(DERIVED) and set(DERIVED) - set(of_class(WASF)) == {99}
    assert ont_of(29) == MASDAR  # أصلُ الشبكة
    bad = [k for k in range(len(AWZAN)) if kulli(mizan(AWZAN[k].template)) != KIND_OF[ont_of(k)]]
    assert bad == [40, 54, 60, 62, 81, 82, 83, 86, 93, 94, 99, 108, 109, 110]
    assert [ont_of_reading(r) for r in jidh(cells_of("فَرِيقٌ"))] == [WASF, ISM]
    assert {ont_of_reading(r) for r in jidh(cells_of("قَالَ"))} == {FIL}


_check()
