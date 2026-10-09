"""سجلُّ الانتقالات: كلُّ دالّةٍ في الشجرة تنقل خاناتٍ إلى خانات (‎Word → Word‎) مسجَّلةٌ هنا باسمها
ومبرهنتها في Lean — فلا انتقالَ على الـ116 إلّا مسجَّلًا (ADR ٢٧).

الصفُّ: (الوحدة، الدالّة، المبرهنة، نوعُها، ملاحظة). نوعُ المبرهنة: «إغلاق» = تحفظ الترخيصَ أو تردّ بعينه؛
«خاصّة» = تُثبت خاصّةً مسمّاةً للانتقال (حالةً أو علامةً أو صورةً) دون الإغلاق؛ «—» = لا مبرهنةَ بعد، دَينٌ
باسمه. الحارسُ `tools/gen_intiqal_index.py --check` يمشي على `src/slge` ويرفض: دالّةَ انتقالٍ عامّةً غيرَ
مسجَّلة، وصفًّا بلا دالّة، ومبرهنةً غيرَ مدقَّقة في `Audit.lean`، ودَينًا بلا ملاحظة. السجلُّ مفحوصٌ لا
مبرهَن: Lean يرى الأسماءَ لا الدوالّ.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = ["KINDS", "REGISTRY", "Intiqal"]

KINDS: Final[tuple[str, ...]] = ("إغلاق", "خاصّة", "—")


@dataclass(frozen=True, slots=True)
class Intiqal:
    module: str
    function: str
    theorem: str
    kind: str
    note: str = ""


def _i(module: str, function: str, theorem: str = "", kind: str = "", note: str = "") -> Intiqal:
    if not theorem:
        return Intiqal(module, function, "", "—", note)
    k = kind or ("إغلاق" if theorem.endswith(("_licensed", "_restores", "_roundtrip", "_drops"))
                 else "خاصّة")
    return Intiqal(module, function, theorem, k, note)


REGISTRY: Final[tuple[Intiqal, ...]] = (
    _i("adad", "masc", "Slge.Adad.genderOf_masc"),
    _i("adad", "fem", "Slge.Adad.genderOf_fem_forms"),
    _i("adad", "compound", "Slge.Adad.compound_both_fatha"),
    _i("adad", "uqud", "Slge.Adad.uqud_case"),
    _i("adawat", "apply", "Slge.Adawat.apply_licensed"),
    _i("damair", "attach", "Slge.Damair.attach_licensed"),
    _i("fil", "qalb", "Slge.Fil.qalb_licensed"),
    _i("fil", "naql", "Slge.Fil.naql_licensed"),
    _i("fil", "ibdal", "Slge.Fil.ibdal_licensed"),
    _i("fil", "idgham", "Slge.Fil.idgham_licensed"),
    _i("filiyya", "past", "Slge.Filiyya.past_licensed"),
    _i("filiyya", "fail", "Slge.Filiyya.fail_reads_raf"),
    _i("filiyya", "majhul", "Slge.Filiyya.majhul_fill"),
    _i("filiyya", "majhul_pres", note="مضارعُ المجهول بلا مبرهنة؛ يُبرهَن مع المبنيّ للمجهول قارئًا"),
    _i("filiyya", "naib", "Slge.Filiyya.naib_eq_fail"),
    _i("filiyya", "maful", "Slge.Filiyya.maful_reads_nasb"),
    _i("filiyya", "maiyya", "Slge.Filiyya.maiyya_licensed"),
    _i("ilal", "restore", "Slge.Ilal.apply_roundtrip"),
    _i("ishara", "tanbih", "Slge.Ishara.tanbih_licensed"),
    _i("ishara", "bud", "Slge.Ishara.bud_licensed"),
    _i("ishara", "dual", "Slge.Ishara.caseOf_dual"),
    _i("ism", "nisba", "Slge.Ism.nisba_licensed"),
    _i("ism", "prepare", note="تهيئةُ الاسم للنسبة (حذفُ التاء والألف) بلا مبرهنة"),
    _i("istifham", "idgham_nm", "Slge.Istifham.idghamNM_length"),
    _i("istifham", "ma_after_jarr", "Slge.Istifham.ma_after_jarr"),
    _i("jazm", "sukun", "Slge.Jazm.sukun_licensed"),
    _i("jazm", "drop_weak", "Slge.Jazm.dropWeak_licensed"),
    _i("jazm", "amr", "Slge.Jazm.amr_licensed"),
    _i("jidh", "stem_form", "Slge.Jidh.stemSenses_eq_stemForm"),
    _i("jumla", "lam", "Slge.Jumla.lam_licensed"),
    _i("jumla", "ta_nith", "Slge.Jumla.gender_taNith"),
    _i("jumla", "dual", note="المثنّى في الجملة الاسميّة بلا مبرهنةٍ باسمه (الحالةُ في `Tawabi`)"),
    _i("jumla", "jam_m", note="جمعُ المذكّر السالم بلا مبرهنةٍ باسمه (الحالةُ في `Tawabi`)"),
    _i("jumla", "jam_f", "Slge.Jumla.gender_jamF"),
    _i("jumla", "bare", note="تجريدُ الكلمة من أل والتنوين بلا مبرهنة"),
    _i("majrurat", "jarr", "Slge.Majrurat.jarr_licensed"),
    _i("majrurat", "jarr_nakira", note="جرُّ النكرة بالتنوين بلا مبرهنةٍ باسمه"),
    _i("majrurat", "dual", "Slge.Majrurat.dual_jarr_compatible"),
    _i("majrurat", "mudaf", "Slge.Majrurat.mudaf_no_tanwin"),
    _i("majrurat", "mudaf_uqud", note="إضافةُ العقود بلا مبرهنة"),
    _i("majrurat", "mudaf_dual", note="إضافةُ المثنّى (حذفُ النون) بلا مبرهنةٍ باسمه"),
    _i("mansubat", "raf",
       note="رفعُ الاسم في بقيّة المنصوبات بلا مبرهنةٍ باسمه (`Nawasikh.raf_licensed` نظيرُه)"),
    _i("mansubat", "nasb", "Slge.Mansubat.nakira_reads_nasb"),
    _i("mansubat", "nakira_mansuba", note="النكرةُ المنصوبة بالتنوين بلا مبرهنةٍ باسمه"),
    _i("mansubat", "strip_suffix",
       note="نزعُ لاحقة الضمير بلا مبرهنة (`Jidh.peelSuffix_sound` نظيرُه)"),
    _i("mansubat", "fakk", note="فكُّ الإدغام في التوكيد بلا مبرهنة"),
    _i("mansubat", "mustathna", note="المستثنى بلا مبرهنةٍ باسمه"),
    _i("mansubat", "ghayr_of", note="غيرُ وسوى بلا مبرهنة"),
    _i("mansubat", "after_khala", "Slge.Mansubat.ma_khala_nasb"),
    _i("maqam", "with_prefix", "Slge.Maqam.withPrefix_fill"),
    _i("marifa", "shamsi", "Slge.Marifa.shamsi_licensed"),
    _i("marifa", "al", "Slge.Marifa.al_licensed"),
    _i("marifa", "drop_tanwin", "Slge.Marifa.dropTanwin_licensed"),
    _i("marifa", "idafa", "Slge.Marifa.idafa_no_tanwin"),
    _i("naat", "naat", "Slge.Naat.naatOk_agree"),
    _i("nawasikh", "raf", "Slge.Nawasikh.raf_licensed"),
    _i("nawasikh", "nasb", "Slge.Nawasikh.nasb_licensed"),
    _i("nawasikh", "tanwin", "Slge.Nawasikh.no_tanwin_setLast"),
    _i("nawasikh", "kaffa", "Slge.Nawasikh.kaffa_licensed"),
    _i("nida", "ya_junction", "Slge.Nida.ya_junction"),
    _i("nida", "nudba", "Slge.Nida.nudba_not_binary_licensed"),
    _i("nisab", "isnad", "Slge.Nisab.isnad_one_operation"),
    _i("sarf", "sarf_jarr", "Slge.Sarf.sarf_jarr_ne_nasb"),
    _i("sarf", "sarf_nasb", note="نصبُ المنصرف بلا مبرهنةٍ باسمه"),
    _i("sarf", "mamnu_jarr", "Slge.Alam.mamnu_jarr_is_fatha"),
    _i("sarf", "al_jarr", "Slge.Sarf.al_jarr_kasra"),
    _i("sarf", "idafa_jarr", "Slge.Sarf.idafa_jarr_kasra"),
    _i("sawabiq", "lift", "Slge.Sawabiq.joined_is_initial"),
    _i("shibh", "jarr_majrur", "Slge.Shibh.jarr_majrur_licensed"),
    _i("shibh", "zarf", note="الظرفُ شبهَ جملة بلا مبرهنةٍ باسمه"),
    _i("talab", "lam_amr", "Slge.Talab.lam_amr_licensed"),
    _i("talab", "lam_amr_after_waw", "Slge.Sawabiq.sakin_is_kasra"),
    _i("talab", "masdar_amr", note="المصدرُ النائبُ عن الأمر بلا مبرهنة"),
    _i("talil", "maful_li_ajlih", note="المفعولُ لأجله بلا مبرهنةٍ باسمه"),
    _i("talil", "apply", note="تطبيقُ التعليل بلا مبرهنة"),
    _i("tawabi", "tawkid", "Slge.Tawabi.tawkid_words_licensed"),
    _i("tawzi", "alif_to_ya", note="الألفُ ياءً قبل الضمير بلا مبرهنةٍ باسمه (`tawzi_restores` يردّه)"),
    _i("wasl", "drop_wasl", "Slge.Wasl.wasl_drops"),
    _i("wasl", "istifham_verb", "Slge.Wasl.istifhamVerb_licensed"),
    _i("zaman", "raf_tanwin", "Slge.Zaman.hukm_rafTanwin"),
    _i("zaman", "nasb_tanwin", "Slge.Zaman.hukm_nasbTanwin"),
    _i("zawaid", "tawkid", "Slge.Zawaid.tawkid_licensed"),
    _i("zawaid", "anith", "Slge.Zawaid.anith_licensed"),
    _i("zuruf", "set_last", "Slge.Zuruf.setLast_licensed"),
    _i("zuruf", "mudaf", "Slge.Zuruf.hukm_mudaf"),
    _i("zuruf", "jarr", "Slge.Zuruf.hukm_jarr"),
    _i("zuruf", "qat", "Slge.Zuruf.hukm_qat"),
)
"""الانتقالاتُ العامّة (‎Word → Word‎) في `src/slge` بترتيب الوحدات."""


def _check() -> None:
    keys = [(r.module, r.function) for r in REGISTRY]
    assert len(keys) == len(set(keys))
    assert all(r.kind in KINDS for r in REGISTRY)
    assert all(r.note for r in REGISTRY if r.kind == "—")


_check()
