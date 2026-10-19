"""الملحَقُ بالرباعيّ (الكتاب س19135–19138، س21110، س21122): قوالبُ الإلحاق من الثلاثيّ الصحيح تُفحص
**ردًّا** لا قياسًا — لا مرجعَ محجوبًا فيها (إذنُ المالك 2026-10-09، وقّع عنه الوكيل). التوقّعاتُ من نصّ
الكتاب لا من الشيفرة:

١. صورُ الباب بأعيانها تُولَّد: جلببت، شمللت (س19136)، حوقلت (س19137)، بيطرت، هينمت (س19137–19138)،
   هرولة، جهورة (س19138)، تجلبب (س21110)، يتحوقل (س19099 — ماضيه تَحَوْقَلَ).
٢. الردّ: كلُّ صورةٍ مولَّدة تدخل الجسرَ (بعد إصلاح الرسم كما في `Gate.enter`) READY وتُرخَّص وصلًا
   بقيد الحدّ ووقفًا.
٣. مرآةُ `A116.Hadd.ilhaq_not_geminate`: أوّلُ لامَي الإلحاق صنفُه `cv` في كلّ صورة (لا `c`)؛ والإدغامُ
   (أَعَدَّ) أوّلُ مثليه `c`.
٤. السماعُ معجمًا: الإلحاقُ لا يدخل الفهرسَ المعكوس المقيسَ على MASAQ — `recover` لا يجد جَلْبَبَ،
   و`derive` بلا `ilhaq` لا يولّدها.
٥. طفراتٌ مرفوضة: الأجوفُ والناقصُ والمضاعفُ لا يُلحَقون هنا (الكتابُ على بنات الثلاثة الصحيحة في
   هذا الباب)؛ ولا ‎Q-IV‎ (افْعَلَلَّ ليس إلحاقًا)؛ والقالبُ المزعوم فَعْيَلَ (شَرْيَفَ) ليس في الباب.
"""

from __future__ import annotations

from gate import derive, recover
from gate.contextual import Context, project
from gate.licence import kind_of, strict_licensed, strict_pause_licensed
from gate.mabni_verbs import ILHAQ_SHAPES
from gate.residue import repair

KITAB = {
    "جلب": ("جَلْبَبَ", "جَلْبَبْتُ", "تَجَلْبَبَ"),
    "شمل": ("شَمْلَلَ", "شَمْلَلْتُ"),
    "حقل": ("حَوْقَلَ", "حَوْقَلْتُ", "تَحَوْقَلَ"),
    "بطر": ("بَيْطَرَ", "بَيْطَرْتُ"),
    "هنم": ("هَيْنَمَ", "هَيْنَمْتُ"),
    "هرل": ("هَرْوَلَ",),
    "جهر": ("جَهْوَرَ",),
}


def _atoms(word: str) -> tuple[str, ...]:
    """كما يفعل `Gate.enter`: الرسمُ يُصلَح بقواعد الطبعة المسمّاة (`residue`) ثمّ يُسقَط على الذرّات."""

    d = project(repair(word)[0], Context())
    assert d["status"] == "READY", word
    return tuple(d["atoms"])


def test_the_kitab_forms_are_generated_with_their_shape() -> None:
    assert [s for s, _, _ in ILHAQ_SHAPES] == ["QL", "QW", "QY", "QV"]
    for root, words in KITAB.items():
        forms = derive(root, ilhaq=True)
        for w in words:
            assert w in forms, (root, w)
    assert any(f == "QL-I" and k == "PAST" for k, f, _ in derive("جلب", ilhaq=True)["جَلْبَبَ"])
    assert any(f == "QL-II" for _, f, _ in derive("جلب", ilhaq=True)["تَجَلْبَبَ"])
    assert any(f == "QW-I" for _, f, _ in derive("حقل", ilhaq=True)["حَوْقَلَ"])
    assert any(f == "QY-I" for _, f, _ in derive("بطر", ilhaq=True)["بَيْطَرَ"])
    assert any(f == "QV-I" for _, f, _ in derive("هرل", ilhaq=True)["هَرْوَلَ"])


def test_every_generated_form_returns_through_the_bridge_licensed() -> None:
    """الردُّ: derive → project READY → مرخَّصةٌ وصلًا ووقفًا؛ وكلُّ صورةٍ لها قراءةٌ واحدةٌ على الأقلّ."""

    n = 0
    for root in KITAB:
        for word, analyses in derive(root, ilhaq=True).items():
            atoms = _atoms(word)
            assert analyses and strict_licensed(atoms), word
            paused = (*atoms[:-1], atoms[-1][0] + "ْ")
            assert strict_pause_licensed(paused), word
            n += 1
    assert n == 7 * 184


def test_ilhaq_lam_is_cv_and_idgham_is_c() -> None:
    """مرآةُ `ilhaq_not_geminate`/`idgham_closer` على كلّ صور ‎QL‎: المثلان المتحرّكُ أوّلُهما `cv`."""

    for root in KITAB:
        for word, analyses in derive(root, ilhaq=True).items():
            if not any(f.startswith("QL") for _, f, _ in analyses):
                continue
            atoms = _atoms(word)
            kinds = kind_of(atoms)
            pairs = [i for i in range(len(atoms) - 1)
                     if atoms[i][0] == atoms[i + 1][0] == root[2] and atoms[i][1] != "ْ"]
            assert pairs, word
            assert all(kinds[i] == "cv" for i in pairs), (word, kinds)
    aadda = _atoms("أَعَدَّ")
    assert list(kind_of(aadda)) == ["cv", "cv", "c", "cv"]
    assert list(kind_of(_atoms("جَلْبَبَ"))) == ["cv", "c", "cv", "cv"]


def test_ilhaq_is_lexical_and_outside_the_measured_index() -> None:
    assert recover("جَلْبَبَ")[0] == "NOT_GENERATED"
    assert "جَلْبَبَ" not in derive("جلب") and "حَوْقَلَ" not in derive("حقل")


def test_mutations_are_refused() -> None:
    # الأجوفُ والناقصُ والمضاعف: لا إلحاقَ من هذا الباب
    assert derive("قول", ilhaq=True) == {} and derive("دعو", ilhaq=True) == {}
    assert derive("مدد", ilhaq=True) == {}
    forms = derive("جلب", ilhaq=True)
    # لا Q-IV ولا فَعْيَلَ (جَلْيَبَ) — ليسا في الباب
    assert not any(f.endswith("-IV") for v in forms.values() for _, f, _ in v)
    assert "جَلْيَبَ" not in forms and "جَلَبَّ" not in forms
    # الطفرة: من عدّ لامَ الإلحاق مُدغَمةً خالف الكتاب (س21122) والخانات
    assert _atoms("جَلْبَبَ") != _atoms("جَلَبَّ")
