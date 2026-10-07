"""سجلُّ الدعاوى: لكلّ قانونٍ في SLGE وسمُه وسندُه. ما لا سندَ له لا يُقال.

الوسوم (من الأقوى):

* **مبرهن** — مبرهنةٌ تفحصها نواةُ Lean، وسندُها اسمُها (`lean:…`)، ومطابقةُ البايثون لها
  في `tests/test_conformance.py`.
* **مفحوص_استقصاء** — كلُّ حالةٍ في مجالٍ محدودٍ معلن، وسندُها اختبار (`test:…`).
* **مفحوص_بعينة** — أمثلةٌ مختارة؛ لا تُعمَّم.
* **دليل** — قاعدةٌ مقبولةٌ بدليلٍ مسمّى المصدر.
* **معلن** — تعريفٌ أو بياناتٌ تراثيّةٌ معلنة؛ لا تُفحص على واقع.
* **رأي** — اقتراحُ مولِّد؛ لا يُنتج.
* **مفتوح** — سؤالٌ أو عيبٌ مسمّى لم يُحسم.

`tests/test_status.py` يفحص أنّ كلَّ سندٍ موجود: المبرهنةُ في `formal/` وفي `Audit.lean`،
والاختبارُ دالّةٌ في ملفّه. و`tools/gen_status.py` يولّد `STATUS.md` منه، ويفحص CI أنه محدَّث.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = ["LEDGER", "Claim", "Status"]


class Status(Enum):
    """وسمُ الدعوى، مرتّبًا من الأقوى."""

    مبرهن = 1
    مفحوص_استقصاء = 2
    مفحوص_بعينة = 3
    دليل = 4
    معلن = 5
    رأي = 6
    مفتوح = 7
    معلق = 8


@dataclass(frozen=True, slots=True)
class Claim:
    """دعوى واحدة بوسمها وسندها."""

    claim_id: str
    statement: str
    status: Status
    support: tuple[str, ...]
    note: str = ""


def _c(cid: str, statement: str, status: Status, *support: str, note: str = "") -> Claim:
    return Claim(cid, statement, status, support, note)


_P, _X, _S, _D, _O = (Status.مبرهن, Status.مفحوص_استقصاء, Status.مفحوص_بعينة, Status.معلن,
                      Status.مفتوح)

_DECLARED: tuple[Claim, ...] = (
    # — النظم (منقول من تعقّل) —
    _c("NAZM", "ستّةُ أنماط تركيبٍ وثلاثُ علاقاتٍ منقولةٌ من تعقّل جداولَ معلَنة؛ لا قاعدةَ تعمل", _D,
       "test:tests/test_nazm.py::test_six_patterns_three_relations_as_in_taaqol",
       note="المصدر sonaiso/taaqol-gpt@91dad10 (formal_shape_composition.py، رتبته هناك مرشَّح). "
            "ما له بتٌّ هنا شرطٌ واحد: توافقُ الإعراب (حالةُ الخانة الأخيرة)."),
    _c("NAZM-case", "توافقُ الإعراب بين كلمتين هو تساوي حالة الخانة الأخيرة", _X,
       "test:tests/test_nazm.py::test_case_agreement_is_last_cell_state"),
    # — الوزن: الميزانُ الصرفيُّ قالبًا —
    _c("WAZN-root", "الأصلُ يُستردّ من الصيغة بالقالب لكلّ قالبٍ سليمٍ ولكلّ أصل", _P,
       "lean:Slge.Wazn.rootOf_fill", "lean:Slge.Wazn.awzan_root",
       "test:tests/test_wazn.py::test_fill_then_root_of_recovers_every_root"),
    _c("WAZN-indep", "ترخيصُ الكلمة من القالب وحدَه: الوزنُ يُرخَّص مرّةً لكلّ الأصول", _P,
       "lean:Slge.Wazn.states_fill", "lean:Slge.Wazn.licensed_fill_indep",
       "test:tests/test_wazn.py::test_licence_is_root_independent"),
    _c("WAZN-table", "125 وزنًا مودَعًا (121 من كتب الصرف و4 من أبنية سيبويه) سليمةٌ ومرخَّصةٌ "
       "لكلّ أصل؛ بايثونُها مطابقٌ لجدول Lean", _P,
       "lean:Slge.Wazn.awzan_wf", "lean:Slge.Wazn.awzan_licensed",
       "test:tests/test_conformance.py::test_wazn_matches_lean"),
    _c("WAZN-sibawayh",
       "هياكلُ الأوزان مقابل أبنية سيبويه المختومة (158 هيكلًا): 111 من 125 عنده؛ 14 مسمّاةٌ بأرقامها؛ "
       "والهيكلُ دالّةٌ على القالب في Lean (الشدّةُ حرفٌ واحد، التاءُ الأخيرةُ تُسقط، الهمزةُ الأولى وصلًا "
       "أو قطعًا)", _P,
       "lean:Slge.Abniya.outside_abniya", "lean:Slge.Abniya.abniya_length",
       "test:tests/test_wazn.py::test_skeletons_measured_against_sibawayh",
       note="الحركاتُ معلَنةٌ من كتب الصرف لا مقيسة؛ الرباعيُّ والإعلالُ والمفعولُ المطلق والجامدُ "
            "خارج الجدول باسمها (DEBTS). كان القياسُ بمفتاح الاسم 103/121 قبل أن يُبرهَن الهيكل."),
    _c("WAZN-awzan", "أوزانُ الفعل والمصدر والمشتقّات والتأنيث والجموع كما في كتب الصرف", _D,
       "test:tests/test_wazn.py::test_masdar_of_mazid_is_a_declared_pair_of_deposited_awzan"),
    # — شبكةُ الأوزان: الترخيصُ الجبريُّ التدريجيُّ من المصدر —
    _c("SHABAKA-wf", "إدخالٌ وحذفٌ (بشرط بقاء الأصل) وتغييرُ حالة: كلُّ تتابعٍ يحفظ استردادَ الأصل", _P,
       "lean:Slge.Shabaka.wf_step", "lean:Slge.Shabaka.wf_run",
       "test:tests/test_shabaka.py::test_every_edit_keeps_the_root_recoverable"),
    _c("SHABAKA-edges",
       "124 حافّةً من المصدر المجرّد: الابنُ = الأبُ بعد عمليّاته، وكلُّ وزنٍ يبلغ الجذر", _P,
       "lean:Slge.Shabaka.edges_apply", "lean:Slge.Shabaka.network_rooted",
       "lean:Slge.Shabaka.run_edge_wf",
       "test:tests/test_conformance.py::test_shabaka_matches_lean"),
    _c("SHABAKA-classical",
       "ترتيبُ البصريّين: المصدرُ أصلُ المشتقّات؛ الماضي فالمضارع فالأمر؛ المزيدُ من المجرّد", _D,
       "test:tests/test_shabaka.py::test_classical_edges_are_machine_checked_and_rooted"),
    _c("SHABAKA-minimal",
       "ترتيبُ البصريّين ليس أقلَّ الأشجار كلفةً: 369 عمليّةً مقابل 166؛ يتّفقان في 22 أبًا من 124",
       _S,
       "test:tests/test_shabaka.py::test_computed_tree_is_minimal_and_classical_is_not",
       note="أقلُّ شجرةٍ (Prim على مسافة لِيفنشتاين للقوالب) محسوبةٌ لا مقرَّرة؛ ما يحمله ترتيبُ البصريّين "
            "فوق كلفة القالب شرطُ حدٍّ دلاليّ لم يُقَس بعد."),
    # — الأسماء الخمسة: الإعرابُ بالحروف دالّة —
    _c("KHAMSA-madd", "حرفُ المدّ صورةُ الحركة (و↔ضم، ا↔فتح، ي↔كسر) والحالةُ تُقرأ من الصورة بعينها", _P,
       "lean:Slge.Khamsa.madd_matches_short", "lean:Slge.Khamsa.caseOf_form",
       "lean:Slge.Khamsa.form_injective_stem",
       "test:tests/test_khamsa.py::test_case_is_read_back_from_every_form"),
    _c("KHAMSA-forms", "الصورُ الخمسَ عشرة مرخَّصةٌ متباينةُ الأعداد؛ وما خرج عن الشروط لا يُخمَّن", _P,
       "lean:Slge.Khamsa.khamsa_licensed", "lean:Slge.Khamsa.khamsa_numbers_nodup",
       "lean:Slge.Khamsa.no_guess_for_plural",
       "test:tests/test_conformance.py::test_khamsa_matches_lean"),
    _c("KHAMSA-gate",
       "صورُ أب وأخ وذو بالقانون = ذرّاتُ شهادات البوّابة (10 شواهد)؛ حمٌ وفوٌ بالقانون نفسه", _S,
       "test:tests/test_khamsa.py::test_forms_match_gate_witnesses",
       note="الشروطُ (مفرد، مكبَّر، مضاف لغير الياء) معلَنةٌ في Ctx لا مستنبَطة."),
    # — الأفعال الخمسة: الإعرابُ بالنون بتًّا واحدًا —
    _c("AFAL-nun",
       "الرفعُ يُقرأ من الآخر (نونٌ أو لا)، والضميرُ من حرفه؛ وصورةُ النصب هي صورةُ الجزم", _P,
       "lean:Slge.Afal.moodOf_raf", "lean:Slge.Afal.moodOf_nasb", "lean:Slge.Afal.pronounOf_form",
       "lean:Slge.Afal.nasb_eq_jazm",
       "test:tests/test_afal.py::test_mood_is_one_bit_and_nasb_equals_jazm"),
    _c("AFAL-harmony",
       "الحركةُ قبل الضمير من جنسه — قانونُ الأسماء الخمسة نفسُه؛ والصورُ الثلاثون مرخَّصة", _P,
       "lean:Slge.Afal.glide_matches_before", "lean:Slge.Afal.five_licensed",
       "test:tests/test_conformance.py::test_afal_matches_lean"),
    _c("AFAL-gate",
       "ستّةُ شواهد من شهادات البوّابة تطابق القانون؛ نصبُ الاثنين ورفعُ المخاطبة بالقانون", _S,
       "test:tests/test_afal.py::test_forms_match_gate_witnesses",
       note="الخمسةُ خمسةٌ بجدول مطابقةٍ معلَن (ياءُ المخاطبة لا تلحق حرفَ الغيبة)."),
    # — أدواتُ الربط: فهرسةٌ على الدرجات —
    _c("RAWABIT-cells", "90 أداةً مفردة خاناتُها مرخَّصة؛ 45 منها من شهادات البوّابة بعينها", _P,
       "lean:Slge.Rawabit.particles_licensed",
       "test:tests/test_conformance.py::test_rawabit_matches_lean",
       "test:tests/test_rawabit.py::test_every_particle_licensed_and_witness_counts"),
    _c("RAWABIT-proclitic", "الحرفُ المتحرّك المتّصل (و ف ل ب ك س) لا يُفسد ترخيصَ ما بعده", _P,
       "lean:Slge.Rawabit.proclitic_keeps_licence",
       "lean:Slge.Rawabit.proclitics_one_vowelled_cell"),
    _c("RAWABIT-amal",
       "العملُ دالّةٌ على الخانة الأخيرة؛ وعلى الأفعال الخمسة حذفُ النون جزمًا ونصبًا", _P,
       "lean:Slge.Rawabit.govern_jazm_afal", "lean:Slge.Rawabit.govern_nasb_afal",
       "lean:Slge.Rawabit.raf_not_governed_jazm",
       "test:tests/test_rawabit.py::test_govern_reads_the_last_cell_and_the_five_verbs"),
    _c("RAWABIT-babs",
       "المعاني (23 بابًا من الجدول المُرسَل) معلَنة؛ والتراكيبُ ليست أدواتٍ بل تياراتُ شهادات", _D,
       "test:tests/test_rawabit.py::test_index_is_current"),
    # — الضمائر: الحصرُ الجامع على الدرجات —
    _c("DAMAIR-na",
       "قانونُ نا: سكونُ الصحيح قبلها رفعٌ، وحركتُه أو مدُّه نصبٌ/جرّ — من الخانة، لكلّ حامل", _P,
       "lean:Slge.Damair.na_raf_reads_sukun", "lean:Slge.Damair.na_nasb_reads_vowel",
       "lean:Slge.Damair.na_after_madd_not_raf", "lean:Slge.Damair.witness_na_roles",
       "test:tests/test_damair.py::test_na_law_on_gate_witnesses"),
    _c("DAMAIR-ta", "قانونُ التاء: الشخصُ في حالتها بعد ساكن؛ وبعد المتحرّك ليست تاءَ الفاعل", _P,
       "lean:Slge.Damair.ta_person", "lean:Slge.Damair.ta_after_vowel_not_subject",
       "lean:Slge.Damair.witness_ta_persons",
       "test:tests/test_damair.py::test_ta_law_on_gate_witnesses"),
    _c("DAMAIR-iyya", "ضميرُ النصب المنفصل = الحاملُ إِيَّا + المتّصل؛ والإلحاقُ يحفظ الترخيص", _P,
       "lean:Slge.Damair.iyya_is_carrier_plus_suffix", "lean:Slge.Damair.witness_iyya",
       "lean:Slge.Damair.attach_licensed",
       "test:tests/test_damair.py::test_iyya_is_carrier_plus_attached"),
    _c("DAMAIR-forms", "33 صورةً مرخَّصةً متباينة: 12 رفعًا و12 نصبًا منفصلة و9 شواهدَ متّصلة", _P,
       "lean:Slge.Damair.damair_licensed", "lean:Slge.Damair.damair_nodup",
       "test:tests/test_conformance.py::test_damair_matches_lean"),
    _c("DAMAIR-roles",
       "الأدوارُ الإعرابيّة الثابتة من الحصر المُرسَل معلَنة؛ الياءُ والمستترُ خارج ما يقرؤه الحرف", _D,
       "test:tests/test_damair.py::test_index_is_current"),
    # — أسماءُ الإشارة: ثلاثُ عمليّات على نواة —
    _c("ISHARA-ops", "التنبيهُ في الصدر والبعدُ في العجز عمليّتان تحفظان الترخيصَ لكلّ نواة", _P,
       "lean:Slge.Ishara.tanbih_licensed", "lean:Slge.Ishara.bud_licensed",
       "test:tests/test_ishara.py::test_three_operations_and_case_reading"),
    _c("ISHARA-dual", "المثنّى: الحالةُ من المدّ قبل النون (ولو لحقت الكاف)؛ الياءُ لا تفرّق نصبًا وجرًّا",
       _P, "lean:Slge.Ishara.caseOf_dual", "lean:Slge.Ishara.caseOf_dual_bud",
       "lean:Slge.Ishara.nasb_eq_jarr_dual", "lean:Slge.Ishara.duals_have_case"),
    _c("ISHARA-mabni", "المبنيُّ ما لا تقرأ له الخانةُ حالةً: 17 صورةً من 25؛ وكلُّها مرخَّصةٌ متباينة", _P,
       "lean:Slge.Ishara.mabni_no_case", "lean:Slge.Ishara.forms_licensed",
       "lean:Slge.Ishara.forms_nodup", "test:tests/test_conformance.py::test_ishara_matches_lean"),
    _c("ISHARA-gate", "13 صورةً من شهادات البوّابة هي صورُ القانون بعينها؛ الباقي (12) بالقانون", _S,
       "lean:Slge.Ishara.witnessed_subset",
       "test:tests/test_ishara.py::test_gate_witnesses_are_the_law_forms",
       note="الدلالةُ (قريب/بعيد، عدد، جنس) من الحصر المُرسَل معلَنة."),
    # — أسماءُ الاستفهام —
    _c("ISTIFHAM-ayy",
       "أَيّ المعربُ الوحيد: صورُه تختلف في الخانة الأخيرة لا غير؛ وسائرُها صورةٌ واحدة", _P,
       "lean:Slge.Istifham.caseOf_ayy", "lean:Slge.Istifham.ayy_differs_only_in_state",
       "lean:Slge.Istifham.ayy_three_forms", "lean:Slge.Istifham.mabni_single_form",
       "test:tests/test_istifham.py::test_ayy_is_the_only_declinable"),
    _c("ISTIFHAM-tarkib",
       "مَاذَا = مَا ++ ذَا، أَمَّنْ = أَمْ ++ مَنْ، مَنْ ذَا وصلٌ مرخَّص؛ وما بعد الجارّ تحذف ألفَها "
       "ثمّ يُدغَم", _P,
       "lean:Slge.Istifham.madha_is_ma_dha", "lean:Slge.Istifham.man_dha_junction",
       "lean:Slge.Istifham.amman_is_am_man", "lean:Slge.Istifham.ma_after_jarr",
       "lean:Slge.Istifham.amma_is_an_ma_idgham", "lean:Slge.Istifham.mimma_is_min_ma_idgham",
       "lean:Slge.Istifham.idghamNM_length",
       "test:tests/test_istifham.py::test_composition_and_ma_after_jarr"),
    _c("ISTIFHAM-forms",
       "22 صورةً مرخَّصةً متباينة، 21 منها شواهدُ البوّابة بعينها؛ والهمزةُ حرفٌ متّصل", _P,
       "lean:Slge.Istifham.forms_licensed", "lean:Slge.Istifham.forms_nodup",
       "lean:Slge.Istifham.hamza_prefix_licensed",
       "test:tests/test_conformance.py::test_istifham_matches_lean"),
    _c("ISTIFHAM-sadara",
       "الصدارة على MASAQ: 100/251 في صدر الآية أو بعد عاطف/جارّ/همزة؛ 151 بعد فعل قولٍ ونظرٍ "
       "وسؤال", _S,
       "test:tests/test_istifham.py::test_tiers_and_index",
       note="صدارةُ جملةٍ لا آية: لا تُقاس بلا حدٍّ للجملة — دَينٌ على النظم. الدلالةُ من الحصر "
            "المُرسَل معلَنة."),
    # — النداء —
    _c("NIDA-hukm", "قانونُ المنادى من الخانة الأخيرة: الضمُّ بناءٌ، والتنوينُ لا يجامع البناء", _P,
       "lean:Slge.Nida.damm_is_bina", "lean:Slge.Nida.tanwin_never_bina",
       "lean:Slge.Nida.witnesses_hukm", "test:tests/test_nida.py::test_hukm_reads_the_last_cell"),
    _c("NIDA-adawat", "الأدواتُ الستّ حروفٌ مرخَّصة؛ ويَا تُوصَل بكلّ مرخَّص", _P,
       "lean:Slge.Nida.particles_licensed", "lean:Slge.Nida.particles_nodup",
       "lean:Slge.Nida.ya_junction", "test:tests/test_conformance.py::test_nida_matches_lean"),
    _c("NIDA-nudba", "الندبة (حَسْرَتَاهْ) ساكنان متجاوران: خارج الترخيص الثنائيّ لكلّ جذع", _P,
       "lean:Slge.Nida.nudba_not_binary_licensed",
       "test:tests/test_nida.py::test_nudba_is_outside_binary_licence",
       note="صورةُ وقفٍ يرخّصها الثلاثيُّ في الغانم (A116.Ternary)؛ لا تُدّعى هنا."),
    _c("NIDA-masaq",
       "على 489 منادًى بشهادات البوّابة: الضمُّ ⇒ مبنيّ 188/188؛ الفتحُ والكسرُ ⇒ معرب 195/237؛ "
       "63 لا تقرؤها الخانة", _S,
       "test:tests/test_nida.py::test_masaq_measurement_and_index",
       note="الباقي خلافُ وسمٍ في MASAQ (أَهْلَ، مَعْشَرَ، بَنِي موسومةً «مبني»)؛ لم أُصلحه."),
    # — ظروفُ المكان —
    _c("ZURUF-ops", "الإضافةُ والجرُّ والقطعُ عمليّاتٌ على الخانة الأخيرة تحفظ الترخيصَ ويقرؤها الحكم", _P,
       "lean:Slge.Zuruf.setLast_licensed", "lean:Slge.Zuruf.hukm_qat", "lean:Slge.Zuruf.hukm_mudaf",
       "lean:Slge.Zuruf.hukm_jarr", "test:tests/test_zuruf.py::test_three_operations_read_back"),
    _c("ZURUF-forms", "51 صورةً (17 جذعًا × 3) مرخَّصةً بأحكامها؛ وحَيْثُ مقطوعةٌ أبدًا", _P,
       "lean:Slge.Zuruf.forms_licensed", "lean:Slge.Zuruf.forms_hukm",
       "lean:Slge.Zuruf.haythu_always_cut", "lean:Slge.Zuruf.constants_single",
       "test:tests/test_conformance.py::test_zuruf_matches_lean"),
    _c("ZURUF-masaq", "على 1,493 ظرفًا بشهادات البوّابة: الضمُّ ⇒ مقطوع 82/82 (وحَيْثُ ثابت)؛ الفتحُ ⇒ "
       "مضاف 752/756؛ الكسرُ ⇒ بعد جارٍّ أو ياء 568/584", _S,
       "test:tests/test_zuruf.py::test_masaq_measurement_and_index",
       note="المختصُّ قيدٌ معجميّ؛ المقاديرُ بلا شاهد؛ ظرفُ الزمان حصرُه معلَّق."),
    # — ظروفُ الزمان —
    _c("ZAMAN-forms", "المتصرّفُ خمسُ صورٍ مرخَّصةٍ متباينة (مضاف/مجرور/مقطوع/مرفوعٌ منوَّن/منصوبٌ منوَّن)",
       _P, "lean:Slge.Zaman.forms_licensed", "lean:Slge.Zaman.forms_nodup",
       "lean:Slge.Zaman.forms_hukm",
       "test:tests/test_conformance.py::test_zaman_matches_lean"),
    _c("ZAMAN-tanwin", "الخانةُ تفرّق الضمَّ المنوَّن (مرفوعٌ متصرّف) من الضمّ العاري (مقطوع)", _P,
       "lean:Slge.Zaman.tanwin_vs_qat", "lean:Slge.Zaman.hukm_rafTanwin",
       "lean:Slge.Zaman.hukm_nasbTanwin", "test:tests/test_zaman.py::test_five_forms_and_readers"),
    _c("ZAMAN-mabni",
       "المبنيّةُ الثمانية صورةٌ واحدةٌ بحالةٍ ثابتة كما أُعلنت؛ وأَمْسِ بأل العهديّة معرب", _P,
       "lean:Slge.Zaman.constants_licensed", "lean:Slge.Zaman.constants_states",
       "lean:Slge.Zaman.al_amsu", "test:tests/test_zaman.py::test_constants_single_state"),
    _c("ZAMAN-masaq", "التصرُّفُ عددُ الحالات: على 1,334 موضعًا من MASAQ المتصرّفةُ 8/12 بحالتين فأكثر "
       "والمبنيّةُ 5/7 بحالةٍ واحدة (والاثنان كسرةُ وصلٍ وتصادفُ رسم)؛ وعند الفتح الظرفُ 230/326", _S,
       "test:tests/test_zaman.py::test_masaq_measurement_and_index",
       note="الظرفيّةُ (معنى في) لا تُقرأ من الخانة: دَينٌ على النظم."),
    # — العدد —
    _c("ADAD-ta",
       "المخالفةُ (3–10) خانةُ تاءٍ واحدة بعد فتحة الجذع؛ وجنسُ المعدود يُقرأ منها (وسِتُّ تاؤها أصل)",
       _P, "lean:Slge.Adad.fem_is_masc_without_ta", "lean:Slge.Adad.genderOf_masc",
       "lean:Slge.Adad.genderOf_fem_forms", "lean:Slge.Adad.six_ta_is_radical",
       "lean:Slge.Adad.ten_single_opposes",
       "test:tests/test_adad.py::test_gender_is_one_ta_and_six_is_radical"),
    _c("ADAD-tarkib",
       "التركيبُ (11–19) فتحُ الجزأين وشينُ عَشَر؛ اثنا عشر إعرابُه من مدّه؛ العقودُ واوٌ وياء", _P,
       "lean:Slge.Adad.compound_both_fatha", "lean:Slge.Adad.shin_law",
       "lean:Slge.Adad.twelve_case",
       "lean:Slge.Adad.uqud_case", "test:tests/test_adad.py::test_compound_shin_twelve_uqud"),
    _c("ADAD-forms", "82 صورةً مرخَّصةً متباينة (مذكّر/مؤنّث × 3 حالات، العقود، اثنا عشر، المركّب)", _P,
       "lean:Slge.Adad.forms_licensed", "lean:Slge.Adad.forms_nodup",
       "test:tests/test_conformance.py::test_adad_matches_lean"),
    _c("ADAD-tamyiz",
       "حالةُ المعدود دالّةٌ في مدى العدد: على 72 موضعًا من MASAQ بشهادات البوّابة 71 مطابق", _S,
       "lean:Slge.Adad.tamyiz_ranges", "test:tests/test_adad.py::test_tamyiz_function_and_masaq",
       note="الحيادُ (مائة، ألف) والمعطوفُ وتذكيرُ المعدود بمفرده: معلن."),
    # — المعارف —
    _c("MARIFA-al",
       "التعريفُ بأل عمليّةٌ تحفظ الترخيص، والإدغامُ الشمسيُّ لا يغيّر نمطَ السكون، والأداةُ تُقرأ "
       "من الصدر", _P, "lean:Slge.Marifa.shamsi_licensed", "lean:Slge.Marifa.al_licensed",
       "lean:Slge.Marifa.hasAl_al", "test:tests/test_marifa.py::test_al_and_shamsi_match_gate"),
    _c("MARIFA-idafa", "الإضافةُ تُسقط التنوينَ وتحفظ الترخيص؛ والمضافُ إلى ضميرٍ لا تنوينَ له", _P,
       "lean:Slge.Marifa.dropTanwin_licensed", "lean:Slge.Marifa.idafa_no_tanwin",
       "lean:Slge.Marifa.mudaf_is_marifa", "test:tests/test_marifa.py::test_idafa_drops_tanwin"),
    _c("MARIFA-mawsul",
       "الموصولةُ 14 صورةً مرخَّصةً متباينة؛ المبدوءُ بأل تُقرأ أداتُه؛ ومثنّاه كالإشارة", _P,
       "lean:Slge.Marifa.mawsul_licensed", "lean:Slge.Marifa.mawsul_nodup",
       "lean:Slge.Marifa.mawsul_al",
       "lean:Slge.Marifa.mawsul_dual_case", "lean:Slge.Marifa.deposited_no_tanwin",
       "lean:Slge.Marifa.man_looks_like_tanwin",
       "test:tests/test_conformance.py::test_marifa_matches_lean"),
    _c("MARIFA-tanwin",
       "على 6,544 صورةً من MASAQ: أل مع تنوين 1 (وسم خاطئ)؛ مضافٌ مع تنوين 12 (تنوينُ العوض "
       "وخلافُ وسم)؛ العلمُ منوَّن 35/157 فالتنوينُ ليس علامةَ تنكير", _S,
       "test:tests/test_marifa.py::test_masaq_measurement_and_index",
       note="القوّةُ ترتيبٌ معلَن؛ العلمُ والنكرة من المعجم؛ المستترُ بلا خانة."),
    # — الممنوعُ من الصرف —
    _c("SARF-law", "الممنوعُ: صورةُ جرّه هي صورةُ نصبه؛ والمنصرفُ يفرّقهما الكسرُ والتنوين؛ وشرطا الصرف "
       "يردّان الكسرة", _P,
       "lean:Slge.Sarf.jarr_eq_nasb", "lean:Slge.Sarf.sarf_jarr_ne_nasb",
       "lean:Slge.Sarf.al_jarr_kasra", "lean:Slge.Sarf.idafa_jarr_kasra",
       "test:tests/test_sarf.py::test_decisive_law_jarr_is_nasb"),
    _c("SARF-illa",
       "عللُ الصيغة تُقرأ من الخانة: منتهى الجموع (قراءةُ القالب سليمةٌ لكلّ أصل)، ألفا التأنيث، "
       "وزنُ أَفْعَل/فَعْلَان، الألفُ والنون", _P,
       "lean:Slge.Sarf.onTemplate_fill", "lean:Slge.Sarf.muntaha_wf",
       "lean:Slge.Sarf.witnesses_illa",
       "test:tests/test_conformance.py::test_sarf_matches_lean"),
    _c("SARF-masaq",
       "بعد الجارّ على 754 اسمًا: بأل ⇒ كسر 255؛ مضاف ⇒ كسر 120؛ المجرّدُ منوَّنُ كسرٍ 251 أو "
       "مفتوحٌ بلا تنوين 44 (الممنوع: 17 بعلّة صيغةٍ مقروءة، 27 معجم)", _S,
       "test:tests/test_sarf.py::test_masaq_measurement_and_index",
       note="العلميّةُ بعجمتها وتأنيثها وتركيبها وعدلها معجم؛ والهمزةُ الأصليّةُ في الممدود دَين."),
    # — التوابع —
    _c("TAWABI-case", "الحالةُ لا العلامة: قارئٌ يردّ الضمّةَ والواوَ والألفَ رفعًا؛ "
       "رفعُ الخمسة والعقود بالواو رفعٌ لكلّ جذع؛ والتبعيّةُ متماثلةٌ انعكاسيّة", _P,
       "lean:Slge.Tawabi.four_markers_one_case", "lean:Slge.Tawabi.follows_khamsa",
       "lean:Slge.Tawabi.caseClass_khamsa_raf", "lean:Slge.Tawabi.caseClass_uqud_raf",
       "lean:Slge.Tawabi.caseClass_jam_muannath", "lean:Slge.Tawabi.follows_symm",
       "lean:Slge.Tawabi.follows_refl",
       "test:tests/test_tawabi.py::test_four_markers_one_case"),
    _c("TAWABI-unread", "نصبُ الخمسة بالألف لا يقرؤه القارئُ العامّ: الألفُ مشتركةٌ مع المقصور — "
       "المعجمُ يفصل",
       _P, "lean:Slge.Tawabi.khamsa_nasb_unread",
       "test:tests/test_tawabi.py::test_khamsa_raf_read_nasb_unread"),
    _c("TAWABI-nasaq", "حروفُ النسق التسعة في جدول أدوات الربط؛ والتوكيدُ المعنويّ ستّةُ ألفاظٍ "
       "مرخَّصة تُضاف إلى ضمير (وعَامَّة خارج الثنائيّ)", _P,
       "lean:Slge.Tawabi.nasaq_in_rawabit", "lean:Slge.Tawabi.tawkid_words_licensed",
       "lean:Slge.Tawabi.tawkid_case", "test:tests/test_tawabi.py::test_nasaq_and_tawkid"),
    _c("TAWABI-masaq", "على 3,179 زوجًا من MASAQ: النعتُ يوافق 873/1,079 فيما تقرؤه الخانة؛ "
       "المخالفُ من اختيار المتبوع ومن جرّ الممنوع بالفتحة", _S,
       "test:tests/test_tawabi.py::test_masaq_measurement_and_index",
       note="المتبوعُ قانونُ تيار؛ المطابقةُ الأربع للنعت تُقاس في النظم؛ "
            "البدلُ وعطفُ البيان لا تفرّقهما الخانة."),
    # — النواسخ —
    _c("NAWASIKH-ops", "أربعةُ أبوابٍ عمليّتان: كان = (رفع، نصب)، إنّ عكسُها، كاد عملُ كان، ظنّ نصبان، "
       "لا للجنس عملُ إنّ؛ والعمليّتان تحفظان الترخيص", _P,
       "lean:Slge.Nawasikh.inna_eq_swap_kana", "lean:Slge.Nawasikh.kada_eq_kana",
       "lean:Slge.Nawasikh.zanna_both_nasb", "lean:Slge.Nawasikh.laJins_eq_inna",
       "lean:Slge.Nawasikh.raf_licensed", "lean:Slge.Nawasikh.nasb_licensed",
       "test:tests/test_nawasikh.py::test_two_operations_four_babs"),
    _c("NAWASIKH-read", "ما رُفع يُقرأ رفعًا لكلّ جذع (ومع التنوين وأل)؛ وما نُصب نصبًا إن لم يكن آخرُه "
       "نونًا، ومع التنوين لكلّ جذع؛ والحركةُ وحدَها لا تنوينَ معها", _P,
       "lean:Slge.Nawasikh.caseClass_raf", "lean:Slge.Nawasikh.caseClass_nasb",
       "lean:Slge.Nawasikh.caseClass_nasb_tanwin", "lean:Slge.Nawasikh.caseClass_raf_tanwin",
       "lean:Slge.Nawasikh.caseClass_al_raf", "lean:Slge.Nawasikh.uqud_nasb_compatible",
       "lean:Slge.Nawasikh.raf_no_tanwin", "lean:Slge.Nawasikh.nasb_no_tanwin",
       "test:tests/test_nawasikh.py::test_two_operations_four_babs"),
    _c("NAWASIKH-la", "اسمُ لا النافية للجنس: فتحٌ بلا تنوينٍ ولا أداة، يُقرأ نصبًا", _P,
       "lean:Slge.Nawasikh.laJins_ism_no_tanwin", "lean:Slge.Nawasikh.la_rayb_witness",
       "test:tests/test_nawasikh.py::test_la_jins_ism_is_bare_nakira"),
    _c("NAWASIKH-kaffa", "المودَعاتُ الأربع مرخَّصة؛ والكفُّ إلحاقُ «مَا» يحفظ الترخيص والصورُ الستّ هي "
       "العمليّة؛ وجدولُ الأدوات يسجّل إِنَّ ناصبةً وإِنَّمَا بلا عمل؛ وخبرُ كاد مضارعٌ مرفوع", _P,
       "lean:Slge.Nawasikh.kana_licensed", "lean:Slge.Nawasikh.kada_licensed",
       "lean:Slge.Nawasikh.inna_licensed", "lean:Slge.Nawasikh.zanna_licensed",
       "lean:Slge.Nawasikh.kaffa_licensed", "lean:Slge.Nawasikh.kaffa_forms",
       "lean:Slge.Nawasikh.innama_kaffa_in_rawabit", "lean:Slge.Nawasikh.kada_khabar_raf",
       "test:tests/test_nawasikh.py::test_deposits_licensed_and_kaffa",
       note="أَنْ في جدول أدوات الربط ناصبةً (an_in_rawabit): دَينٌ سُدِّد؛ وجَعَلَ في بابين: المعنى يفصل."),
    _c("NAWASIKH-masaq", "على 2,599 اسمٍ وخبرٍ من MASAQ: خبرُ كان نصبٌ 99%، خبرُ إنّ رفعٌ 98%، "
       "اسمُ كان رفعٌ 92%، اسمُ إنّ نصبٌ 95%، اسمُ لا 73/73 نكرةٌ مفتوحة؛ عسى بأَنْ 21/24 "
       "وكاد 0/23 وطفق 0/3؛ وإنّما لا اسمَ ناسخٍ بعدها 27/27", _S,
       "test:tests/test_nawasikh.py::test_masaq_measurement_and_index",
       note="المخالفُ: ياءُ المتكلّم والمنقوص — دُيونٌ على القارئ؛ "
            "والتمامُ والجمودُ والتعليقُ تيارٌ ومعجم."),
    # — الجزم والشرط —
    _c("JAZM-ops", "العلاماتُ الثلاث عمليّات: السكونُ مرخَّصٌ بعد متحرّكٍ وغيرُ مرخَّصٍ بعد مدٍّ فيُلزِم حذفَ "
       "عين الأجوف؛ حذفُ حرف العلّة يحفظ الترخيصَ ويترك حركةَ الأصل؛ حذفُ النون صورةُ النصب", _P,
       "lean:Slge.Jazm.sukun_licensed", "lean:Slge.Jazm.hollow_forced",
       "lean:Slge.Jazm.yaqulu_sukun_unlicensed", "lean:Slge.Jazm.dropWeak_licensed",
       "lean:Slge.Jazm.dropWeak_last", "lean:Slge.Jazm.afal_jazm_eq_nasb",
       "lean:Slge.Jazm.marker_afal_jazm", "lean:Slge.Jazm.waw_shared",
       "test:tests/test_jazm.py::test_three_markers_three_operations"),
    _c("JAZM-tools", "الأدواتُ 4 + 12 + 7 مرخَّصة؛ لامُ الأمر حرفٌ متّصل؛ لَا الناهيةُ ولَمَّا الجازمةُ وسبعةُ "
       "أسماءِ شرطٍ خاناتُها خاناتُ غيرها (النافية، الحينيّة، الاستفهام)؛ وأَيّ وحدَها معربة", _P,
       "lean:Slge.Jazm.tools_licensed", "lean:Slge.Jazm.counts", "lean:Slge.Jazm.amr_licensed",
       "lean:Slge.Jazm.shared_la_lamma", "lean:Slge.Jazm.shared_istifham",
       "lean:Slge.Jazm.ayy_declines", "lean:Slge.Jazm.rawabit_jazm",
       "test:tests/test_jazm.py::test_tools_counted_and_shared",
       note="إِنْ وإِذْمَا ومَتَى وأَيَّانَ وأَيْنَ وإِذَا وحِينَ ولَوْ ولَوْمَا ليست في جدول أدوات الربط: دَين."),
    _c("JAZM-masaq", "على 1,365 مضارعًا مجزومًا من MASAQ: حذفُ النون يقرؤه القارئ 520/537، والسكونُ "
       "514/634 (والباقي كسرةُ الوصل ويَكُ)، وحذفُ حرف العلّة لا تقرؤه الخانة 192/194 كما بُرهن", _S,
       "test:tests/test_jazm.py::test_masaq_measurement_and_index",
       note="كسرةُ التقاء الساكنين قانونُ Context في الغانم؛ الجزمُ بفعلين والفاءُ الرابطة تيار."),
    # — بقيّة المنصوبات —
    _c("MANSUBAT-ops", "الحالُ المفردةُ والتمييزُ عمليّةٌ واحدة (نكرةٌ منصوبة = فتحٌ فتنوين): تُقرأ نصبًا "
       "وتحمل التنوينَ وتحفظ الترخيص لكلّ جذع؛ والفرزُ (مشتقّ/جامد) يقرؤه القالبُ بعد إسقاط اللاحقة "
       "وفكّ الإدغام؛ والمحوَّلُ عمليّات", _P,
       "lean:Slge.Mansubat.tamyiz_eq_hal", "lean:Slge.Mansubat.nakira_reads_nasb",
       "lean:Slge.Mansubat.nakira_has_tanwin", "lean:Slge.Mansubat.nakira_licensed",
       "lean:Slge.Mansubat.sorting_by_template", "lean:Slge.Mansubat.derived_witnesses",
       "lean:Slge.Mansubat.derived_of_bare", "lean:Slge.Mansubat.adad_tamyiz_is_nakira",
       "lean:Slge.Mansubat.tahwil_witness", "lean:Slge.Mansubat.sukara_hal",
       "test:tests/test_mansubat.py::test_hal_and_tamyiz_one_operation"),
    _c("MANSUBAT-istithna", "الاستثناءُ ثلاثُ حالاتٍ ثلاثُ عمليّات: التامُّ المثبت نصبٌ، والتامُّ المنفيّ "
       "نصبٌ أو بدلٌ (تبعيّةٌ في الحالة)، والمفرَّغُ عمليّةُ الموقع (إِلَّا بلا أثر)؛ غَيْر مضافةٌ تأخذ "
       "الحكم؛ خَلَا/عَدَا بـ«ما» نصب", _P,
       "lean:Slge.Mansubat.tamm_muthbat_reads_nasb", "lean:Slge.Mansubat.badal_follows",
       "lean:Slge.Mansubat.mufarragh_eq_role", "lean:Slge.Mansubat.tools_licensed",
       "lean:Slge.Mansubat.ghayr_idafa_jarr", "lean:Slge.Mansubat.ghayr_takes_hukm",
       "lean:Slge.Mansubat.ma_khala_nasb",
       "test:tests/test_mansubat.py::test_istithna_three_operations"),
    _c("MANSUBAT-masaq", "على 508 حالٍ وتمييزٍ ومستثنًى من MASAQ: الحالُ نصبٌ 275/290، التمييزُ 38/52 "
       "(والباقي تمييزُ كم مجرور)، المستثنى 38/41؛ والمثبتُ بعد إِلَّا مستثنًى 83، والمنفيُّ بدلٌ أو "
       "حسب الموقع 318/475", _S,
       "test:tests/test_mansubat.py::test_masaq_measurement_and_index",
       note="516 صورةً رُفضت بالاسم (REJECT: التنوينُ بعد الألف في طبعة MASAQ)؛ النفيُ والتمامُ تيار."),
    # — المجرورات —
    _c("MAJRURAT-ops", "الجرُّ عمليّةٌ واحدة (كسرٌ، وللنكرة تنوين) تُقرأ جرًّا لكلّ جذعٍ وتحفظ الترخيصَ "
       "ويحكم عليها جدولُ الأدوات؛ الياءُ (جمعٌ ومثنًّى) نصبٌ أو جرّ، والخمسةُ بالياء لا يقرؤها القارئ؛ "
       "والفتحةُ في الممنوع تُقرأ نصبًا والجرُّ من جدول العلل", _P,
       "lean:Slge.Majrurat.jarr_licensed", "lean:Slge.Majrurat.caseClass_jarr",
       "lean:Slge.Majrurat.caseClass_jarr_tanwin", "lean:Slge.Majrurat.govern_jarr",
       "lean:Slge.Majrurat.uqud_jarr_compatible", "lean:Slge.Majrurat.dual_jarr_compatible",
       "lean:Slge.Majrurat.khamsa_jarr_unread", "lean:Slge.Majrurat.mamnu_jarr_reads_nasb",
       "lean:Slge.Majrurat.an_kasra_shared",
       "test:tests/test_majrurat.py::test_one_operation_three_markers"),
    _c("MAJRURAT-sabab", "سببُ الجرّ في الحدّ: 17 حرفًا مرخَّصًا والمتّصلةُ الخمسةُ لا تُفسد ما بعدها؛ "
       "الإضافةُ تُسقط التنوينَ ونونَ الجمع والمثنّى، واللفظيّةُ يقرؤها القالب؛ والتبعيّةُ توافقٌ", _P,
       "lean:Slge.Majrurat.harfs_licensed", "lean:Slge.Majrurat.proclitic_jarr_licensed",
       "lean:Slge.Majrurat.harfs_in_rawabit", "lean:Slge.Majrurat.rubba_nakira",
       "lean:Slge.Majrurat.mudaf_no_tanwin", "lean:Slge.Majrurat.mudaf_drops_nun",
       "lean:Slge.Majrurat.lafziyya_by_template", "lean:Slge.Majrurat.tabi_jarr_follows",
       "test:tests/test_majrurat.py::test_sabab_in_boundary",
       note="تَاللَّهِ خارج الترخيص الثنائيّ (مدٌّ فلامٌ مشدّدة) كحَاجَّ: الثلاثيُّ في الغانم."),
    _c("MAJRURAT-masaq", "على 18,184 مجرورٍ ومضافٍ من MASAQ: الكسرةُ جرٌّ 9,790/9,930، الياءُ نصبٌ/جرّ "
       "أو غيرُ مقروءة 988/1,000، الفتحةُ نصبٌ 290/308؛ والمضافُ بلا تنوين 8,058/8,137", _S,
       "test:tests/test_majrurat.py::test_masaq_measurement_and_index",
       note="إِيمَانِ وشَيْطَانِ تُقرأ رفعًا كالمثنّى: خانةٌ واحدة؛ تنوينُ العوض في المضاف مسمًّى."),
    # — همزتا الوصل والقطع —
    _c("WASL-boundary", "لا ابتداءَ بساكن وهمزةُ الوصل تُرخِّصه؛ في الوصل تسقط فيتّصل الساكنُ بمتحرّكٍ قبله "
       "ولا تُقبل بعد ساكن؛ والقطعُ يبقى بعد أيّ آخر؛ والخانةُ لا تفرّقهما في الابتداء", _P,
       "lean:Slge.Wasl.no_initial_sukun", "lean:Slge.Wasl.wasl_licenses",
       "lean:Slge.Wasl.wasl_drops",
       "lean:Slge.Wasl.wasl_after_sukun", "lean:Slge.Wasl.qat_stays", "lean:Slge.Wasl.quick_test",
       "lean:Slge.Wasl.wasl_qat_cells_shared", "lean:Slge.Wasl.istifhamVerb_licensed",
       "test:tests/test_wasl.py::test_boundary_laws",
       note="الحدُّ نفسُه مبرهَنٌ في الغانم (A116.Boundary) وبقيّةُ الرسم WASL/WASL_SILENT في شهادته."),
    _c("WASL-templates", "الحصرُ الصرفيُّ تقسيمٌ لقوالب awzan المبدوءة بهمزة (14 وصلًا، 10 قطعًا، "
       "متباينان يغطّيان الأربعةَ والعشرين)؛ القارئُ يقرأ من القالب والجذر والعشرة السماعيّة؛ "
       "والألفُ لا تكون أصلًا", _P,
       "lean:Slge.Wasl.templates_partition", "lean:Slge.Wasl.templates_wf",
       "lean:Slge.Wasl.kind_witnesses", "lean:Slge.Wasl.template_reads_what_cells_cannot",
       "lean:Slge.Wasl.illa_not_wasl", "lean:Slge.Wasl.ten_licensed", "lean:Slge.Wasl.ten_shape",
       "lean:Slge.Wasl.plural_qat", "test:tests/test_wasl.py::test_templates_partition_and_reader",
       note="أمرُ الخماسيّ والسداسيّ وصلٌ (118–120) وأمرُ الرباعيّ قطعٌ (113): دَينٌ سُدِّد."),
    _c("WASL-masaq", "على 16,072 صورةً مبدوءةً بهمزة من MASAQ بشهادات البوّابة: فيما يقرؤه القالبُ "
       "(4,318) يوافق الشهادةَ 4,259؛ وبعد السابقة لا وصلَ قائمًا: 943 ساقطٌ و119 محذوفٌ رسمًا", _S,
       "test:tests/test_wasl.py::test_masaq_measurement_and_index",
       note="555 صورةً مرفوضةٌ بالاسم؛ المهموزُ المعتلّ والمدغم والحروفُ لا يقرؤها القالب."),
    # — الاسم —
    _c("ISM-thulathi", "المجرّدُ الثلاثيُّ عشرةٌ = 3 × 4 − 2: اثنا عشرَ قالبًا يسقط فُعُل وفِعُل، كلُّها "
       "سليمةٌ مرخَّصةٌ لكلّ جذر وتُقرأ من الخانتين الأُوليين؛ والرباعيُّ خمسةُ أشكالٍ (الحصرُ يسمّي فَعْلَل "
       "مرّتين) والخماسيُّ أربعة", _P,
       "lean:Slge.Ism.thulathi_ten", "lean:Slge.Ism.thulathi_wf", "lean:Slge.Ism.thulathi_licensed",
       "lean:Slge.Ism.thulathi_read", "lean:Slge.Ism.witnesses_read", "lean:Slge.Ism.rubai_shapes",
       "lean:Slge.Ism.khumasi_shapes", "test:tests/test_ism.py::test_thulathi_ten_and_shapes",
       note="الحصرُ يسمّي «فُعِل» ساقطةً ثمّ يعدّها بدُئِل: الجدولُ يفصل — الساقطان فُعُل وفِعُل."),
    _c("ISM-tahwil", "التصغيرُ ثلاثُ عمليّاتٍ تحفظ الترخيصَ لكلّ جذر ويقرؤها القارئ؛ والنسبُ عمليّةٌ واحدة "
       "بعد تهيئةٍ مسمّاة تحفظ الترخيصَ وتُقرأ", _P,
       "lean:Slge.Ism.tasghir_licensed", "lean:Slge.Ism.tasghir_read",
       "lean:Slge.Ism.tasghir_witnesses",
       "lean:Slge.Ism.nisba_licensed", "lean:Slge.Ism.nisba_read", "lean:Slge.Ism.nisba_witnesses",
       "test:tests/test_ism.py::test_tasghir_and_nisba_operations"),
    _c("ISM-bina", "البناءُ العارضُ حالةٌ ثابتةٌ في الآخر بعمليّةٍ في بابها (المنادى، اسمُ لا، المقطوع، "
       "المركّب)؛ واللازمُ 71 صورةً مودَعة", _P,
       "lean:Slge.Ism.arid_bina", "lean:Slge.Ism.lazim_deposited",
       "test:tests/test_ism.py::test_arid_bina_in_its_babs"),
    _c("ISM-masaq", "على 19,216 اسمًا معربًا من MASAQ: الثلاثيُّ 4,447 منه على العشرة 4,101 وفِعُل "
       "معدومة وفُعُل 185 كلُّها جموع؛ الرباعيُّ 1,580 أكثرُه فَعْلَل وفُعْلَل وفِعْلَل؛ تصغيرٌ 23 "
       "ونسبٌ 139 بالقارئ", _S,
       "test:tests/test_ism.py::test_masaq_measurement_and_index",
       note="1,824 صورةً مرفوضةٌ بالاسم؛ فَعَلَل وفَعِلَل أشكالُ المزيد بالتاء لا المجرّد."),
    # — الفعل —
    _c("FIL-abwab", "الأبوابُ الستّة أزواجُ (عينِ الماضي، عينِ المضارع) من تسعة؛ قوالبُها سليمةٌ وصورُها "
       "مرخَّصةٌ لكلّ جذر وتُقرأ من الخانتين؛ وشرطُ باب فَتَحَ حلقيّةٌ مقروءة", _P,
       "lean:Slge.Fil.abwab_six", "lean:Slge.Fil.bab_wf", "lean:Slge.Fil.bab_licensed",
       "lean:Slge.Fil.bab_read", "lean:Slge.Fil.bab_witnesses",
       "test:tests/test_fil.py::test_abwab_six_of_nine",
       note="الثلاثةُ الساقطة (كسر–ضم، ضم–فتح، ضم–كسر) ثقلٌ معلَن؛ واختيارُ الباب للجذر معجم."),
    _c("FIL-mazid", "أحرفُ الزيادة = طولُ القالب − 3؛ التسعةُ في awzan ثلاثةٌ بحرف وخمسةٌ بحرفين وواحدٌ "
       "بثلاثة؛ لا خماسيَّ الأصول (الجذرُ ثلاثيٌّ بالبناء) والرباعيُّ أشكالٌ مرخَّصة", _P,
       "lean:Slge.Fil.mazid_counts", "lean:Slge.Fil.root_is_ternary", "lean:Slge.Fil.rubai_shapes",
       "test:tests/test_fil.py::test_mazid_and_rubai"),
    _c("FIL-amr", "أمرُ المزيد من مضارعه بقاعدة أمر المجرّد (حذفُ المضارعة، تسكينُ الآخر، همزةُ وصلٍ "
       "لما بدأ بساكن): سبعةٌ بالقاعدة، وأَفْعِلْ يفرّقه القطعُ المفتوح؛ وأمرُ اِفْعَلَّ بالقاعدة غيرُ "
       "مرخَّصٍ ثنائيًّا", _P,
       "lean:Slge.Fil.amr_of_pres", "lean:Slge.Fil.amr_ifalla_unlicensed",
       "test:tests/test_fil.py::test_mazid_imperative_and_post_template_readers",
       note="دَينٌ سُدِّد: قوالبُ 113–120 في awzan وحوافُّها في الشبكة؛ فكُّ إدغام أمرِ اِفْعَلَّ بقيّةٌ مسمّاة."),
    _c("FIL-ilal", "الإعلالُ ثلاثُ عمليّات (قلبٌ ونقلٌ يحفظان الترخيص، وحذفٌ ملزَم) والإبدالُ ثلاثُ "
       "قواعد على اِفْتَعَلَ لا تغيّر نمطَ السكون (والهمزةُ فاءً كالواو والياء: اِتَّخَذَ)", _P,
       "lean:Slge.Fil.qalb_licensed", "lean:Slge.Fil.naql_licensed", "lean:Slge.Fil.hadhf_witness",
       "lean:Slge.Fil.qalb_witness", "lean:Slge.Fil.naql_witness", "lean:Slge.Fil.ibdal_licensed",
       "lean:Slge.Fil.ibdal_witnesses", "test:tests/test_fil.py::test_ilal_and_ibdal_operations",
       note="الردُّ مبرهَنٌ في الغانم (A116.Ilal)."),
    _c("FIL-readers", "ما بعد القالب: الأجوفُ على فَعَلَ بعد القلب [ف، ا، ل] لكلّ جذرٍ عينُه واوٌ أو ياء، "
       "والمضعَّفُ بعد الإدغام [ف، عْ، ع] لكلّ جذرٍ عينُه لامُه؛ الإدغامُ يحفظ الترخيص؛ والقارئان يردّان "
       "قَالَ وجَاءَ ورَدَّ", _P,
       "lean:Slge.Fil.qalb_pastT", "lean:Slge.Fil.idgham_pastT", "lean:Slge.Fil.idgham_licensed",
       "lean:Slge.Fil.readers_witnesses",
       "test:tests/test_fil.py::test_mazid_imperative_and_post_template_readers",
       note="عينُ الأجوف بين الواو والياء: المعجمُ يفصل (قَالَ: ق‑و‑ل، بَاعَ: ب‑ي‑ع)."),
    _c("FIL-masaq", "على 18,765 فعلًا من MASAQ: عينُ الماضي المجرّد السالم فتحٌ 489 كسرٌ 119 ضمٌّ 9، وعينُ "
       "المضارع فتحٌ 1,226 كسرٌ 1,036 ضمٌّ 657؛ الماضي على القوالب 831، وبعد القالب بالعمليّة 1,160 "
       "(أجوف 1,082، مضعَّف 78)؛ الباقي 1,233 ناقصٌ ومثالٌ ومزيدٌ معتلّ", _S,
       "test:tests/test_fil.py::test_masaq_measurement_and_index",
       note="الزوجُ (البابُ) قانونُ معجمٍ يجمع الصورتين؛ الخانةُ تقرأ كلَّ صورةٍ وحدَها."),
    # — الحروف والأدوات —
    _c("HURUF-table", "جدولٌ واحدٌ لـ68 حرفًا في ثلاث مجموعات (31 للأسماء، 18 للأفعال، 19 مشتركة) "
       "على 53 صورةً مرخَّصة؛ لا تنوينَ فيها (وما نونُه أصلٌ يشابه التنوين مسمًّى، وأَنَّ تُقرأ أداةَ "
       "تعريفٍ شمسيّة)؛ والمتّصلةُ لا تُفسد ما بعدها", _P,
       "lean:Slge.Huruf.counts", "lean:Slge.Huruf.table_licensed", "lean:Slge.Huruf.no_tanwin",
       "lean:Slge.Huruf.proclitics_keep_licence", "lean:Slge.Huruf.shared_cells",
       "test:tests/test_huruf.py::test_table_deposited_and_licensed",
       note="الخانةُ الواحدةُ في أبوابٍ عدّة (لَا أربعًا، وَ أربعًا، حَتَّى ثلاثًا): العملُ من التيار."),
    _c("HURUF-amal", "عملُ الحرف عمليّةٌ على ما بعده بُرهنت في بابها: جرٌّ، نصبُ اسمٍ ورفعُ خبر، نصبُ "
       "المضارع وجزمُه، والتبعيّة؛ وجدولُ أدوات الربط يشهد لما فيه؛ والتنفيسُ بلا أثر", _P,
       "lean:Slge.Huruf.amal_is_operation", "lean:Slge.Huruf.rawabit_agrees",
       "lean:Slge.Huruf.sawfa_witness", "test:tests/test_huruf.py::test_amal_is_operation"),
    _c("HURUF-masaq", "على 41,830 موضعًا من MASAQ: لَنْ ينصب المضارعَ بعده 104/106، وأَنْ 446 نصبًا مقابل "
       "25 رفعًا، وحَتَّى ناصبةٌ للفعل 74 وجارّةٌ للاسم؛ ولَا في خمسة أدوار وإِنْ في أربعة", _S,
       "test:tests/test_huruf.py::test_masaq_measurement_and_index",
       note="عدُّ أوصافٍ مجمَّد؛ صورُ الحروف بشهادات البوّابة؛ أَنْ المضمرةُ تيار."),
    # — الجملةُ الاسميّة —
    _c("JUMLA-cells", "المبتدأُ والخبرُ طرفان مرفوعان بعمليّةٍ واحدة تُقرأ رفعًا وتحفظ الترخيص لكلّ جذع؛ "
       "وصورُهما تُقرأ: الضميرُ من جدوله، والمبنيُّ من جداوله، والمعربُ من رفعه؛ وشبهُ الجملة من صدرها، "
       "والجملةُ الفعليّةُ من قالب الفعل، والمفردُ من رفعه", _P,
       "lean:Slge.Jumla.nominal_reads_raf", "lean:Slge.Jumla.nominal_licensed",
       "lean:Slge.Jumla.pronoun_is_damir", "lean:Slge.Jumla.raf_is_ism",
       "lean:Slge.Jumla.kinds_witnesses",
       "test:tests/test_jumla.py::test_both_sides_raf_and_kinds",
       note="المصدرُ المؤوّل مبتدأً تيار؛ والمتّصلُ الجارُّ على نكرةٍ لا تفرّقه الخانةُ من حرف الأصل."),
    _c("JUMLA-order", "الرتبةُ دالّةٌ في الخانات لا في الموضع (التقديمُ عمليّةٌ على الزوج): لامُ الابتداء "
       "تمسك المبتدأ لكلّ مبتدأ وخبر، والصدارةُ والنكرةُ مع شبه الجملة والضميرُ العائدُ تقدّم الخبر، "
       "والخبرُ الفعليُّ وتساوي الرتبة يؤخّرانه، وما سواه جواز؛ والموضعُ المخالفُ يُرفض", _P,
       "lean:Slge.Jumla.swap_swap", "lean:Slge.Jumla.order_swap", "lean:Slge.Jumla.order_lam",
       "lean:Slge.Jumla.lam_licensed", "lean:Slge.Jumla.lam_refuses_khabar_first",
       "lean:Slge.Jumla.order_witnesses",
       "test:tests/test_jumla.py::test_order_is_read_from_cells_not_position",
       note="الحصرُ بإلّا وإنّما تيارٌ (كلمتان) خارج القارئ باسمه."),
    _c("JUMLA-agree", "المطابقةُ عمليّاتٌ على الخبر (تأنيثٌ، تثنيةٌ، جمعان) تحفظ الترخيص، ويقرؤها الجنسُ "
       "والعددُ من اللاحقة بعد إسقاطها؛ فالعمليّةُ الواحدةُ على الطرفين تُطابق؛ والرابطُ في الخبر الجملة "
       "ضميرٌ أو إشارةٌ أو إعادةُ لفظ", _P,
       "lean:Slge.Jumla.ops_licensed", "lean:Slge.Jumla.suffix_licensed",
       "lean:Slge.Jumla.gender_taNith",
       "lean:Slge.Jumla.number_taNith", "lean:Slge.Jumla.number_ops", "lean:Slge.Jumla.gender_jamF",
       "lean:Slge.Jumla.agree_ops", "lean:Slge.Jumla.agree_witnesses",
       "lean:Slge.Jumla.rabit_repeat",
       "lean:Slge.Jumla.rabit_witnesses", "lean:Slge.Jumla.lawla_witness",
       "test:tests/test_jumla.py::test_agreement_is_an_operation_and_an_exception",
       "test:tests/test_jumla.py::test_rabit_four_kinds_three_read",
       note="استثناءُ جمع غير العاقل يقرؤه القالبُ احتمالًا والعقلُ معجم؛ العمومُ والتلاؤمُ الأنطولوجيُّ "
            "والتقديرُ في حذف الخبر معلَنة؛ الفاعلُ المستتر لا خانةَ له."),
    _c("JUMLA-masaq", "على 3,146 زوجًا (مبتدأ، خبر) من MASAQ بشهادات البوّابة: رتبةُ القارئ تقبل موضعَ "
       "المصحف في 2,822 (89.7%)؛ والخبرُ المفردُ المشتقُّ يطابق مبتدأه المعرب في 269/312؛ والرابطُ "
       "ضميرٌ في 329 من 519 جملةً فعليّة", _S,
       "test:tests/test_jumla.py::test_masaq_measurement_and_index",
       note="الأزواجُ بنافذة الآية (المؤخّرُ يأخذ ما قبله)؛ 192 كلمةً مستبعَدةً بالاسم."),
    # — الجملةُ الفعليّة —
    _c("FILIYYA-fil", "الفعلُ ثلاثُ حالات: الماضي مبنيٌّ وآخرُه تقرؤه لاحقتُه (على جدول الضمائر) ومرخَّصٌ "
       "بها لكلّ جذعٍ سالم، والمضارعُ معربٌ بعلاماتٍ عمليّات (Jazm/Afal)، والأمرُ مبنيٌّ على ما يُجزم به "
       "مضارعُه (آخرُ كلّ قالب أمرٍ ساكن)", _P,
       "lean:Slge.Filiyya.past_endings", "lean:Slge.Filiyya.past_licensed",
       "lean:Slge.Filiyya.amr_ends_like_jazm",
       "test:tests/test_filiyya.py::test_verb_three_states_and_subject_three_forms"),
    _c("FILIYYA-fail", "الفاعلُ رفعٌ يُقرأ لكلّ جذع؛ البارزُ المتّصلُ لاحقةٌ من الجدول بحالة ما قبلها "
       "تُقرأ لكلّ فعل، والمفعولُ المتّصلُ كذلك؛ والمستترُ لا خانةَ له", _P,
       "lean:Slge.Filiyya.fail_reads_raf", "lean:Slge.Filiyya.subjectSuffixes_from_table",
       "lean:Slge.Filiyya.attached_subject", "lean:Slge.Filiyya.attached_object",
       "test:tests/test_filiyya.py::test_verb_three_states_and_subject_three_forms",
       note="المصدرُ المؤوّل فاعلًا تيار؛ نونُ النسوة/الأصل وكافُ الخطاب/الأصل بحالة ما قبلها وما بقي "
            "معجم."),
    _c("FILIYYA-order", "رتبُ التباديل (ف × س₁ × س₂) من الخانات لا من الموضع: الفاعلُ المتّصل يقدّم "
       "الفاعلَ "
       "لكلّ فعلٍ ومفعول، والمفعولُ المتّصل يقدّم المفعولَ لكلّ فعلٍ وفاعل؛ والعائدُ وخفاءُ العلامة والصدارةُ "
       "شواهد؛ والموضعُ المخالفُ يُرفض", _P,
       "lean:Slge.Filiyya.order_swap", "lean:Slge.Filiyya.attached_subject_first",
       "lean:Slge.Filiyya.attached_object_first", "lean:Slge.Filiyya.order_witnesses",
       "test:tests/test_filiyya.py::test_order_from_cells_and_mutation_refused",
       note="الحصرُ بإلّا وإنّما تيار؛ ومَا/مَنْ صورةٌ واحدةٌ للاستفهام والموصول والشرط."),
    _c("FILIYYA-naib", "المبنيُّ للمجهول عمليّتان على الحالات (ضمُّ الأوّل وكسرُ ما قبل الآخر؛ وفتحُه في "
       "المضارع): فَعَلَ ← فُعِلَ ويَفْعَلُ ← يُفْعَلُ لكلّ جذر بقالبي الشبكة؛ نائبُ الفاعل بالرفع نفسِه، "
       "وصورُه الأربع يقرؤها الجدولُ والصدر", _P,
       "lean:Slge.Filiyya.majhul_fill", "lean:Slge.Filiyya.majhul_witnesses",
       "lean:Slge.Filiyya.naib_eq_fail",
       "lean:Slge.Filiyya.naib_witnesses",
       "test:tests/test_filiyya.py::test_passive_two_state_operations_and_naib",
       note="ترتيبُ النائب معلَن؛ اسمُ المصدر والمصدرُ على قالبٍ واحد (الدَّرْس): معجم."),
    _c("FILIYYA-mafail", "المفاعيلُ نصبٌ فتنوين يُقرأ لكلّ جذع؛ الظرفُ من جداوله منصوبًا؛ قانونُ الفرز: "
       "مشتقٌّ ⇒ حال، مصدرٌ بجذر الفعل ⇒ مطلق، مصدرٌ بغيره ⇒ لأجله؛ المعيّةُ واوٌ متّصلةٌ تحفظ الترخيص "
       "والمشاركةُ على تَفَاعَلَ عطف؛ والمطلقُ يردّ جذرَ فعله لكلّ جذر", _P,
       "lean:Slge.Filiyya.maful_reads_nasb", "lean:Slge.Filiyya.zarf_reads_nasb",
       "lean:Slge.Filiyya.sorting_masdar_hal", "lean:Slge.Filiyya.maiyya_licensed",
       "lean:Slge.Filiyya.tafaala_is_ataf", "lean:Slge.Filiyya.mutlaq_shares_root",
       "test:tests/test_filiyya.py::test_four_objects",
       note="المختصُّ من الظروف (المسجد) وفعلُ المشاركة خارج تَفَاعَلَ: معجم."),
    _c("FILIYYA-masaq", "على 26,196 كلمةً من MASAQ بشهادات البوّابة: آخرُ الماضي من لاحقته يوافق "
       "علامةَ "
       "MASAQ 6,119/6,979؛ الفاعلُ المتّصلُ يوافق وسمَه 14,252/16,727؛ ورتبةُ القارئ تقبل موضعَ "
       "المصحف في "
       "15,621 من 16,727 (93.4%)", _S,
       "test:tests/test_filiyya.py::test_masaq_measurement_and_index",
       note="الثلاثيّاتُ بنافذة الفعل؛ 2,644 كلمةً مستبعَدةً بالاسم."),
    # — شبهُ الجملة —
    _c("SHIBH-forms", "شبهُ الجملة صورتان: حرفٌ من الجدول ثمّ جرٌّ على الآخر (المجرورُ بعد الحرف بعينه "
       "ويُقرأ جرًّا لكلّ اسم، والتركيبُ مرخَّصٌ لكلّ حرفٍ واسم)، وظرفٌ من الجداول منصوبًا؛ والقارئُ يفرزهما؛ "
       "وردُّ الزائد رفعٌ يُعيد الاسمَ بعينه لكلّ اسم؛ والمختصُّ خارج الجدول الحاصر فيُجرّ", _P,
       "lean:Slge.Shibh.jarr_majrur_reads_jarr", "lean:Slge.Shibh.jarr_majrur_licensed",
       "lean:Slge.Shibh.kind_witnesses", "lean:Slge.Shibh.setLast_setLast",
       "lean:Slge.Shibh.zaid_restores",
       "lean:Slge.Shibh.zaid_witness", "lean:Slge.Shibh.masjid_not_zarf",
       "test:tests/test_shibh.py::test_two_forms_and_the_table_is_exhaustive",
       "test:tests/test_shibh.py::test_zaid_is_restored_by_raf",
       note="الأصليُّ والزائدُ خانةٌ واحدة: الزيادةُ معنًى؛ مَعَ ليست في الجدول المودَع — باسمها."),
    _c("SHIBH-anchor", "المرتكزُ ممّا قبل شبه الجملة: فعلٌ على قالبه أو مشتقٌّ على قالب الوصف أو الكونُ "
       "المحذوف (ثلاثةٌ حاصرة)؛ والمحلُّ من خانة ما قبلها: صلةٌ بعد كلّ موصول، نعتٌ بعد النكرة لكلّ جذع، "
       "خبرٌ بعد المعرفة المرفوعة لكلّ جذع، حالٌ بعد المنصوبة؛ والكونُ المحذوفُ بحالة المحلّ", _P,
       "lean:Slge.Shibh.anchor_witnesses", "lean:Slge.Shibh.mahall_after_mawsul",
       "lean:Slge.Shibh.mahall_after_nakira", "lean:Slge.Shibh.mahall_after_al_raf",
       "lean:Slge.Shibh.mahall_witnesses", "lean:Slge.Shibh.kawn_reads",
       "test:tests/test_shibh.py::test_anchor_and_mahall_from_the_preceding_cells",
       note="تقديرُ الكون معلَنٌ وحالتُه مقروءة؛ المرتكزُ البعيدُ تيار؛ برهانُ الحصر المُرسَل تحصيلُ حاصل."),
    _c("SHIBH-masaq", "على 40,731 كلمةً من MASAQ بشهادات البوّابة: الجارُّ والمجرور بالقارئ "
       "8,075/12,402 "
       "(والباقي متّصلٌ على غير أل)، الظرفُ 1,375/2,033، المجرورُ يُقرأ جرًّا 5,392 ويُردّ زائدُه بعينه "
       "4,752؛ وشبهُ الجملة الخبرُ مرتكزُها كونٌ محذوف 616/739", _S,
       "test:tests/test_shibh.py::test_masaq_measurement_and_index",
       note="المرتكزُ والمحلُّ من الكلمة السابقة مباشرة؛ 3,370 كلمةً مستبعَدةً بالاسم."),
    # — النِّسَبُ الثلاث —
    _c("NISAB-isnad", "الإسنادُ عمليّةٌ واحدة: مبتدأُ الاسميّة وفاعلُ الفعليّة ونائبُه هي الرفعُ بعينه، "
       "فيُقرأ المسندُ إليه رفعًا لكلّ جذع", _P,
       "lean:Slge.Nisab.isnad_one_operation", "lean:Slge.Nisab.isnad_reads_raf",
       "test:tests/test_nisab.py::test_isnad_is_one_operation"),
    _c("NISAB-taqyid", "التقييدُ لا يُنشئ رفعًا: الحالُ والتمييزُ والمفعولُ نصبٌ لكلّ جذع، والإضافةُ والجارُّ "
       "جرٌّ لكلّ اسم، والنعتُ تبعٌ تناظريٌّ انعكاسيّ؛ والرفعُ في التقييد تبعٌ لا أصل", _P,
       "lean:Slge.Nisab.taqyid_nasb", "lean:Slge.Nisab.taqyid_jarr", "lean:Slge.Nisab.naat_follows",
       "lean:Slge.Nisab.taqyid_raf_only_by_following",
       "test:tests/test_nisab.py::test_taqyid_never_creates_raf"),
    _c("NISAB-tadmin", "التضمينُ على الخانات ترتيبٌ جزئيٌّ (انعكاسيٌّ متعدٍّ متضادُّ التباين) من نواة Lean؛ "
       "الصورةُ تتضمّن جذرَها لكلّ قالبٍ ولكلّ جذر؛ والفصلُ: ما اختلف قالبُه اختلفت صورتُه على 121 قالبًا؛ "
       "وسلاسلُ الأوزان تنتهي بالجذر", _P,
       "lean:Slge.Nisab.contains_refl", "lean:Slge.Nisab.contains_trans",
       "lean:Slge.Nisab.contains_antisymm",
       "lean:Slge.Nisab.form_contains_root", "lean:Slge.Nisab.slots_ordered",
       "lean:Slge.Nisab.species_distinct", "lean:Slge.Nisab.chains_end_at_root",
       "test:tests/test_nisab.py::test_containment_is_a_partial_order_and_forms_contain_roots",
       "test:tests/test_nisab.py::test_chains_end_at_root",
       note="التضمينُ بين الكلمات (الجنسُ والنوع) معجم؛ القالبُ المودَعُ بمعنيين صورةٌ واحدة: الفصلُ هناك "
            "معنًى."),
    _c("NISAB-masaq", "القارئُ nisba على 10,149 زوجًا من الشرائح المودَعة بشهادات البوّابة: يوافق وسمَ "
       "MASAQ "
       "في 6,332 (62%)؛ الإسنادُ مبتدأً وخبرًا 1,416/1,643، والتقييدُ مفعولًا به 1,955/3,471", _S,
       "lean:Slge.Nisab.nisba_witnesses", "test:tests/test_nisab.py::test_reader_and_masaq",
       note="المبنيُّ فاعلًا ومفعولًا صورةٌ واحدة؛ العلمُ المنوَّن نكرةٌ بالخانة؛ المعتلُّ على غير قالب."),
    # — التعليلُ والسببيّة —
    _c("TALIL-fadla", "العلّةُ فضلةٌ لا تُرفَع: المفعولُ لأجله مصدرٌ منصوبٌ لكلّ جذع، وصورتا التعليل "
       "(نصبُ المصدر، جرُّه بالحرف) كلمةٌ بعينها إلّا خانةَ الآخر؛ وأدواتُ التعليل الستُّ مرخَّصةٌ من جدول "
       "الربط، ولِأَنَّ عملُ إِنَّ، وليس فيها ما يرفع معمولَه", _P,
       "lean:Slge.Talil.liajlih_reads_nasb", "lean:Slge.Talil.fadla_witnesses",
       "lean:Slge.Talil.two_forms_same_word", "lean:Slge.Talil.tools_licensed",
       "lean:Slge.Talil.tools_in_rawabit", "lean:Slge.Talil.li_anna_eq_inna",
       "lean:Slge.Talil.talil_never_raf", "lean:Slge.Talil.min_ajli_jarr",
       "test:tests/test_talil.py::test_cause_is_never_raf_and_two_forms_are_one_word",
       note="شرطُ المفعول لأجله (القلبيّةُ واتّحادُ الفاعل والزمان) معنًى؛ اللامُ والباءُ لغير التعليل "
            "احتمالٌ لا قطع."),
    _c("TALIL-sababiyya", "السببيّةُ الاشتقاقيّة على الأوزان الـ121 ترتيبٌ جزئيٌّ صارم: لا شيءَ علّةُ "
       "نفسه، وعلّةُ العلّة علّة، ولا دور، والبعدُ عن الجذر يتناقص على كلّ سبب؛ والجذرُ علّةُ الكلّ ولا "
       "علّةَ له", _P,
       "lean:Slge.Talil.derives_irrefl", "lean:Slge.Talil.derives_trans",
       "lean:Slge.Talil.derives_asymm", "lean:Slge.Talil.derives_dist",
       "lean:Slge.Talil.root_causes_all",
       "test:tests/test_talil.py::test_derivational_causality_is_a_strict_partial_order",
       note="السببيّةُ بين الأحداث (التعليمُ علّةُ العلم) معنًى لا خانة."),
    _c("TALIL-tanazu", "التنازع: إعمالُ الثاني لقربه — المتنازَعُ فيه معمولُ الأقرب وخانتُه مستقلّةٌ عن "
       "الأوّل، والأوّلُ بضميره متّصلًا حافظًا للترخيص؛ والمفعولُ لأجله حرٌّ في الموضع بنصبٍ واحد", _P,
       "lean:Slge.Talil.nearer_works", "lean:Slge.Talil.first_takes_pronoun",
       "lean:Slge.Talil.tanazu_witness", "lean:Slge.Talil.fronting_keeps_nasb",
       "test:tests/test_talil.py::test_tanazu_nearer_works_and_first_keeps_pronoun",
       note="إعمالُ الأوّل (الكوفيّون) معلَن لا مودَع."),
    _c("TALIL-masaq", "القارئُ talil على 5,593 كلمةً من الشريحتين المودَعتين بشهادات البوّابة: المفعولُ "
       "لأجله يُقرأ لأجله 27/38، والمفعولُ به يُقرأ لأجله خطأً 161/2,618، والمجرورُ بـلِ/بِ يُقرأ تعليلًا "
       "بالحرف 359/2,887 (إحصاءٌ بلا مرجع)؛ وكلُّ مفعولٍ لأجله في MASAQ منصوب 38/38", _S,
       "lean:Slge.Talil.talil_witnesses", "test:tests/test_talil.py::test_reader_and_masaq",
       note="فَعَالٌ ومَفْعِلَةٌ وتَفْعِلَةٌ غيرُ مودَعة (جَزَاءً، مَوْعِظَةً)؛ الأجوفُ والمقصورُ على غير قالب."),
    # — المقام —
    _c("MAQAM-shakhs", "الشخصُ من الخانة: صدرُ المضارع يقرؤه لكلّ قالبٍ (13) ولكلّ جذرٍ لا ألفَ فيه — "
       "همزةٌ ونونٌ متكلّم، تاءٌ مخاطبٌ أو غائبة (لا تفصل)، ياءٌ غائب؛ ولاحقةُ الفاعل بشخصٍ لكلّ لاحقة، "
       "والماضي بلا لاحقةٍ غائب، والأمرُ مخاطب", _P,
       "lean:Slge.Maqam.present_prefix_reads_person", "lean:Slge.Maqam.withPrefix_fill",
       "lean:Slge.Maqam.present_heads_ya", "lean:Slge.Maqam.suffixShakhs_covers",
       "lean:Slge.Maqam.shakhs_witnesses",
       "test:tests/test_maqam.py::test_prefix_reads_person_for_every_present_template_and_root",
       note="القارئُ المركَّب (لاحقةٌ فصدرٌ فقالب) مشهودٌ لا عامّ؛ العامُّ قارئُ الصدر على الأجذار بلا ألف."),
    _c("MAQAM-istitar", "المستترُ لا خانةَ له: غيابُ لاحقةٍ وشخصٌ مقروء؛ وجوبًا للحاضر وجوازًا للغائب؛ "
       "والاسمُ الظاهرُ فاعلًا للغائب وحده لا بعد متكلّمٍ أو مخاطب، والمتّصلُ والمستترُ لكلّ شخص", _P,
       "lean:Slge.Maqam.mustatir_has_no_cell", "lean:Slge.Maqam.hadir_wujub",
       "lean:Slge.Maqam.ghaib_jawaz",
       "lean:Slge.Maqam.zahir_only_ghaib", "lean:Slge.Maqam.zahir_not_hadir",
       "lean:Slge.Maqam.zuhur_witnesses",
       "test:tests/test_maqam.py::test_concealed_has_no_cell_and_explicit_only_for_ghaib",
       note="ما في الحصر المُرسَل من حظر استتار الغائب خلافُ النحو ولم يُدخَل: الغائبُ مستترٌ جوازًا."),
    _c("MAQAM-tawkid", "التوكيدُ اللفظيّ للضمير مطابقةُ شخص: لكلّ منفصلٍ في الجدول شخصٌ، ولا توكيدَ إلّا "
       "بمنفصلٍ من الجدول وفعلٍ قُرئ شخصُه؛ والضميرُ العائدُ في الفاعل يفرض تقديمَ المفعول", _P,
       "lean:Slge.Maqam.detached_all_read", "lean:Slge.Maqam.detached_mem",
       "lean:Slge.Maqam.tawkid_needs_both", "lean:Slge.Maqam.tawkid_witnesses",
       "lean:Slge.Maqam.aid_forces_maful_first",
       "test:tests/test_maqam.py::test_emphasis_requires_same_person",
       note="الحضورُ والشهودُ وعودُ الغائب على سابقٍ: معنًى ومقام."),
    _c("MAQAM-masaq", "على 16,727 فعلًا من MASAQ بشهادات البوّابة: الشخصُ حيث وُسم يوافق 596 ويخالف 32 "
       "(ولم يُقرأ 560)، ولاحقةُ الفاعل توافق 14,256/16,727، والفاعلُ الظاهرُ بعد الفعل 560 بعد غائبٍ "
       "أو تاءٍ و10 بعد حاضر (طفرةُ zahir_only_ghaib المقيسة)", _S,
       "test:tests/test_maqam.py::test_masaq_measurement_and_index",
       note="المبدَلُ همزتُه ألفًا والناقصُ والمثالُ المنصوب: الخانةُ لا تفصل؛ وسومُ MASAQ للشخص قليلةٌ "
            "وبعضُها مخالف."),
    # — الجهةُ والزمن —
    _c("JIHA-sigha", "الصيغةُ دالّةٌ في الحالات: ما على قالبٍ فحالاتُه حالاتُ قالبه، وأصنافُ الماضي "
       "والمضارع والأمر متباينةُ الحالات قالبًا قالبًا؛ فقارئُ الصيغة يقرأ كلَّ ماضٍ ماضيًا وكلَّ أمرٍ أمرًا "
       "وكلَّ مضارعٍ بصدوره الأربعة مضارعًا لكلّ جذرٍ لا ألفَ فيه", _P,
       "lean:Slge.Jiha.states_of_onTemplate", "lean:Slge.Jiha.sigha_states_disjoint",
       "lean:Slge.Jiha.sigha_of_fill", "lean:Slge.Jiha.not_on_other_class",
       "test:tests/test_jiha.py::test_sigha_is_a_function_of_states_for_every_root"),
    _c("JIHA-amr", "الأمرُ للمخاطب وحده: صيغةُ الأمر مخاطبٌ عند قارئ المقام لكلّ قالبٍ ولكلّ جذرٍ (بلا "
       "ألفٍ ولا تاءٍ آخرًا ولا لاحقة)، وأمرُ الغائب والمتكلّم باللام على المضارع لا بقالب", _P,
       "lean:Slge.Jiha.amr_is_mukhatab", "lean:Slge.Jiha.amr_fill_last",
       "lean:Slge.Jiha.ghaib_amr_by_lam",
       "test:tests/test_jiha.py::test_amr_is_mukhatab_and_ghaib_by_lam"),
    _c("JIHA-shift", "أدواتُ الإزاحة (السين، سَوْفَ، لَمْ، لَنْ، كَانَ) عمليّاتٌ لا تقبل إلّا المضارع، "
       "والماضي والأمرُ لا يُزاحان بأداة؛ السينُ تحفظ الترخيص وتُردّ بعينها، والأدواتُ من جدول الربط "
       "بعملها", _P,
       "lean:Slge.Jiha.shift_only_present", "lean:Slge.Jiha.past_not_shifted",
       "lean:Slge.Jiha.sa_licensed", "lean:Slge.Jiha.sa_restores", "lean:Slge.Jiha.lam_restores",
       "lean:Slge.Jiha.shifts_in_rawabit",
       "lean:Slge.Jiha.jiha_witnesses", "test:tests/test_jiha.py::test_shift_only_on_present",
       note="نقاطُ رايشنباخ (E، S، R) والزمنُ المعنويّ: معنًى لا خانة."),
    _c("JIHA-masaq", "على 16,642 فعلًا من MASAQ بشهادات البوّابة: الصيغةُ على 8,799 فعلًا بلا لاحقة "
       "توافق الوسمَ في 4,586 وتخالفه في 202 (والباقي معتلٌّ أو على غير قالب)؛ والسينُ على 117 فعلًا: "
       "116 مضارعًا "
       "وواحدٌ ماضٍ (طفرةُ shift_only_present المقيسة)", _S,
       "test:tests/test_jiha.py::test_masaq_measurement_and_index",
       note="المبنيُّ للمجهول من المزيد (أُنْزِلَ) وأمرُ أَفْعَلَ غيرُ مودَعَين، والمعتلُّ على غير قالب."),
    # — النعتُ والمطابقة الرباعيّة —
    _c("NAAT-vec", "النعتُ الحقيقيّ مطابقةٌ في أربعةٍ تُقرأ من الخانة (الإعراب، التعريف، الجنس، العدد): "
       "انعكاسيّةٌ على المقروء وتناظريّة؛ والمخالفُ إعرابًا أو تعريفًا ممنوعٌ لكلّ جذعين؛ والمنوَّنُ المرفوعُ "
       "بلا أل على مثله مطابقٌ في الإعراب والتعريف لكلّ جذعين", _P,
       "lean:Slge.Naat.naatOk_refl", "lean:Slge.Naat.naatOk_symm", "lean:Slge.Naat.naatOk_case",
       "lean:Slge.Naat.naatOk_definite", "lean:Slge.Naat.naatOk_agree",
       "lean:Slge.Naat.non_matching_case_blocked", "lean:Slge.Naat.non_matching_definite_blocked",
       "lean:Slge.Naat.nakira_pair_two_coordinates", "lean:Slge.Naat.hasAl_setLast_tanwin",
       "lean:Slge.Naat.naat_witnesses",
       "test:tests/test_naat.py::test_four_coordinates_match_for_every_stem",
       note="الجنسُ والعددُ من اللاحقة والقالب: المؤنّثُ بلا تاء والجمعُ غيرُ المقيس لا تفصلهما الخانة."),
    _c("NAAT-haml", "الحملُ واحدٌ والفرقُ التعريف: النعتُ والخبرُ على معرفةٍ مرفوعةٍ يتّفقان في ثلاثةٍ "
       "ويفترقان في التعريف؛ والجملةُ بعد النكرة نعتٌ وبعد المعرفة حال — الحالُ تشترط صاحبًا معرفةً لكلّ "
       "كلمة، والجملةُ بعد النكرة المنوَّنة المنصوبة نعتٌ لكلّ جذعٍ لا تشابه صورتُه فعلًا", _P,
       "lean:Slge.Naat.khabar_not_naat", "lean:Slge.Naat.hal_requires_marifa",
       "lean:Slge.Naat.naat_after_nakira",
       "test:tests/test_naat.py::test_clause_after_nakira_is_naat_and_hal_needs_marifa",
       note="النعتُ السببيّ خارج الحصر؛ المعطوفُ والبدلُ يُقرآن نعتًا متى طابقا: الفرقُ أداةٌ ومعنًى."),
    _c("NAAT-masaq", "على 1,388 زوجَ نعتٍ من MASAQ بشهادات البوّابة: قارئُ المطابقة الرباعيّة يقرؤها "
       "نعتًا في 677؛ والإعرابُ من الخانة على طرفَي النعت يوافق الوسمَ 2,188/2,776، وأل توافق det "
       "2,609/2,776", _S,
       "test:tests/test_naat.py::test_masaq_measurement_and_index",
       note="أوّلُ مخالفة فيما لم يُقرأ: إعرابٌ لا يُقرأ 309 (موصولٌ ومبنيّ)، تعريفٌ 162 (مضافٌ وعلم)، "
            "إعرابٌ 108، عددٌ 76، جنسٌ 56."),
    # — الأسلوب: الخبرُ والإنشاء —
    _c("USLUB-khabar", "الصدقُ والكذبُ للخبر وحده، والإنشاءُ يُقرأ من الخانة: الأمرُ إنشاءٌ لكلّ قالبِ أمرٍ "
       "ولكلّ جذرٍ مهما كان ما قبله وما بعده؛ ولَا تفصل النهيَ (إنشاء) عن النفي (خبر) بخانة آخر الفعل "
       "وحدها لكلّ قالبِ مضارعٍ وصدرٍ وجذر؛ ومَا أَفْعَلَ تعجّبٌ إن نُصب ما بعده وخبرٌ إن رُفع لكلّ جذر", _P,
       "lean:Slge.Uslub.truth_iff_khabar", "lean:Slge.Uslub.amr_is_insha",
       "lean:Slge.Uslub.la_splits_by_last_state", "lean:Slge.Uslub.sukun_present_not_past",
       "lean:Slge.Uslub.nahy_only_present", "lean:Slge.Uslub.ma_afala_splits_by_next_case",
       "lean:Slge.Uslub.tools_licensed", "lean:Slge.Uslub.tools_in_rawabit",
       "lean:Slge.Uslub.uslub_witnesses",
       "test:tests/test_uslub.py::test_truth_only_for_khabar_and_insha_read_from_cells",
       "test:tests/test_uslub.py::test_witnesses_and_mutations",
       note="يَلْلِمْ من ل‑ل‑م يشابه لَلِّمْ بالخانة فقُيّد برهانُ لَا بذلك؛ القسمُ وصيغُ العقود والخبرُ "
            "المرادُ به الإنشاء معنًى."),
    _c("USLUB-masaq", "على شريحة شبه الجملة بشهادات البوّابة: لَا + مضارعٍ بلا لاحقة 34 سياقًا بوسم "
       "MASAQ (جزم = نهي، غير عامل = نفي): القارئُ يوافقه بخانة الآخر في 21 ويخالفه في 7 (معتلٌّ "
       "وأجوف)؛ فعلُ الأمر 268: يُقرأ أمرًا في 123؛ ما بعد حرف الاستفهام 24: استفهامٌ في 23", _S,
       "test:tests/test_uslub.py::test_masaq_measurement_and_index",
       note="الأجوفُ والناقصُ على غير قالب: 132 أمرًا لا يُقرأ و13 يُقرأ خبرًا — باسمها."),
    # — الطلب —
    _c("TALAB-suwar", "صورُ الأمر الأربع تُقرأ من الخانة (الصيغة، اللام، المصدر النائب، اسم الفعل من "
       "جدولٍ حاصر)؛ لامُ الأمر على المضارع تصل كلَّ شخصٍ لكلّ قالبٍ ولكلّ جذر، وتجزم أبدًا، وتحفظ "
       "الترخيص", _P,
       "lean:Slge.Talab.four_forms_witnesses", "lean:Slge.Talab.ismFil_licensed",
       "lean:Slge.Talab.lam_reaches_every_person", "lean:Slge.Talab.lam_amr_jazm",
       "lean:Slge.Talab.lam_amr_licensed",
       "test:tests/test_talab.py::test_four_forms_and_lam_for_every_person",
       note="المضعّفُ يُجزَم بالفتح (التقاءُ الساكنين) والمعتلُّ بالحذف: دَينُ الإعلال؛ المصدرُ النائبُ عن "
            "المفعول المطلق لا يفرّقه إلّا الصدر."),
    _c("TALAB-amr-nahy", "الأمرُ بالشيء ليس نهيًا عن ضدّه على الخانة: لَا قبل صيغة الأمر لا تقلبها "
       "نهيًا لكلّ قالبٍ ولكلّ جذر، والنهيُ لا يُقرأ إلّا بلَا قبل مضارع، وصيغةُ الأمر لا تُقرأ نهيًا "
       "مهما كان ما قبلها وما بعدها — التحويلُ عمليّتان", _P,
       "lean:Slge.Talab.la_before_amr_stays_amr", "lean:Slge.Talab.nahy_requires_la",
       "lean:Slge.Talab.amr_never_reads_nahy",
       "test:tests/test_talab.py::test_four_forms_and_lam_for_every_person",
       note="الضدُّ معنًى؛ والإلزامُ (وجوبٌ/ندب) ليس في الخانة: معلَن لا مبرهَن."),
    _c("TALAB-masaq", "على MASAQ بشهادات البوّابة: فعلُ الأمر بلا لاحقة 268 يُقرأ صيغةً في 123، واسمُ "
       "فعل الأمر 1/1؛ لامُ الأمر 71 موضعًا كلُّها مجزومة عند MASAQ (سكونٌ 38، حذفُ نون 21، حذفُ حرف "
       "علّة 12) و69 منها بعد الواو أو الفاء", _S,
       "test:tests/test_talab.py::test_masaq_measurement_and_index",
       note="الأجوفُ والناقصُ على غير قالب: 145 أمرًا لا يُقرأ — باسمها؛ أَفْعِلْ (113) أُدخل في قوالب "
            "الأمر."),
    # — الكليُّ والجزئيّ —
    _c("KULLI-ayan", "الكليُّ في الخارج وجودُه في أفراده: ما على قالبٍ فهو القالبُ مملوءًا بجذر وكلُّ "
       "ملءٍ على قالبه لكلّ قالبٍ ولكلّ كلمة؛ الجزئيّاتُ المجدوَلة ليست على قالبٍ إلّا أربعًا تشابه قالبًا "
       "بالخانة والجدولُ يفصلها؛ والعرضيُّ والحدثُ لا يشتركان في قالب", _P,
       "lean:Slge.Kulli.universal_in_particulars", "lean:Slge.Kulli.particulars_off_templates",
       "lean:Slge.Kulli.juzi_by_table", "lean:Slge.Kulli.aradi_hadath_disjoint",
       "lean:Slge.Kulli.kulli_witnesses",
       "test:tests/test_kulli.py::test_universal_lives_in_its_particulars_and_particulars_are_tabled",
       note="نَحْنُ وأَيُّ على فَعْلٌ، ذَلِكَ على فَعِلَ، ثَمَّتَ على فَعَّلَ بالخانة؛ والعلمُ جزئيٌّ بالمعجم."),
    _c("KULLI-masdar", "المصدرُ مجرّدٌ من الزمن: لكلّ قالبِ مصدرٍ ولكلّ جذرٍ لا ألفَ فيه لا يُقرأ ماضيًا ولا "
       "مضارعًا ولا أمرًا، ولا تدخله أدواتُ الإزاحة؛ والفعلُ مهيّأٌ بالزمن لكلّ قالب", _P,
       "lean:Slge.Kulli.masdar_no_sigha", "lean:Slge.Kulli.masdar_states_disjoint",
       "lean:Slge.Kulli.masdar_not_shifted", "lean:Slge.Jiha.sigha_of_fill",
       "test:tests/test_kulli.py::test_masdar_has_no_tense_and_verb_has",
       note="فَعْلَةُ بشرط ألّا تكون فاؤها صدرَ مضارع (نَصْرَةٌ/نَفْعَلُ)؛ ومُفَاعَلَةٌ = مُفَاعَلٌ + ة بالخانة."),
    _c("KULLI-masaq", "على 15,260 كلمةً موسومةً من MASAQ بشهادات البوّابة: القارئُ يوافق صنفَ MASAQ في "
       "7,327 من 13,657؛ الجزئيُّ 2,389، الفعلُ 1,868، العرضيُّ 622، الماهويُّ 1,899، المصدرُ 517", _S,
       "test:tests/test_kulli.py::test_masaq_measurement_and_index",
       note="أكبرُ البقايا: الجامدُ على قالب المصدر (بَحْرٌ على فَعْلٌ) يُقرأ حدثًا 1,976 — الفرقُ معنًى."),
    # — الوضعُ والمشتركُ والترادف —
    _c("WAD-fill", "الوضعُ ملءُ قالبٍ بجذر: متباينٌ في الجذر لكلّ قالبٍ سليم، والقالبُ يُستردّ من ملئه لكلّ "
       "جذرٍ لا ألفَ فيه؛ والميزانُ لا يُشترَك: كلُّ ميزانٍ من الـ121 على صورةٍ واحدة ومعانيه بابُ قالبه", _P,
       "lean:Slge.Wad.wad_injective", "lean:Slge.Wad.sense_of_fill", "lean:Slge.Wad.mizan_unaided",
       "lean:Slge.Wad.mizan_senses",
       "test:tests/test_wad.py::test_wad_is_injective_in_root_and_recovered_from_the_word",
       note="الموضوعُ له على الخانات زوجٌ (قالب، جذر)؛ و«الوضعُ موضوعُه الذهن» رأيٌ لا خانةَ له."),
    _c("WAD-mushtarak", "المشتركُ اللفظيُّ محصورٌ ومجدوَل: اشتراكُ الوضع ستّةُ أزواجٍ متطابقة في المعجم "
       "المودَع، واشتراكُ الصورة لا يقع لجذرين لا ألفَ فيهما إلّا بين قالبين متساويي الطول والحالات "
       "والزوائد المتقابلة لا تقابل ألفٌ زائدةٌ موضعَ أصلٍ فيهما — وأزواجُها 42 بعينها (36 مختلفةُ "
       "القالب)", _P,
       "lean:Slge.Wad.duplicate_templates", "lean:Slge.Wad.mayCollide_sound",
       "lean:Slge.Wad.homonymy_is_tabled", "lean:Slge.Wad.collision_pairs_eq",
       "lean:Slge.Wad.collision_pairs_split", "lean:Slge.Wad.intishar_two_roots",
       "lean:Slge.Wad.wad_witnesses", "test:tests/test_wad.py::test_homonymy_is_bounded_and_tabled",
       note="اِنْتِشَارٌ: اِنْفِعَالٌ من ت‑ش‑ر وافْتِعَالٌ من ن‑ش‑ر؛ ومَنْحَةٌ: مَفْعَلٌ/فَعْلَةٌ. اشتراكُ المعنى "
            "(عَيْنٌ) ليس في الخانة."),
    _c("WAD-taraduf", "المترادفان الصرفيّان يشتركان في الجذر لكلّ قالبين سليمين ولكلّ جذر، ومصادرُ "
       "الجذر الواحد صورٌ متباينة إلّا ما تطابق قالبُه", _P,
       "lean:Slge.Wad.taraduf_same_root", "lean:Slge.Wad.masdar_forms_distinct",
       "test:tests/test_wad.py::test_synonyms_share_root_and_differ_in_form",
       note="ترادفُ الجذرين (قَمَرٌ/هِلَالٌ) معنًى لا صورة: معلَن."),
    _c("WAD-masaq", "على 15,260 كلمةً موسومةً من MASAQ بشهادات البوّابة: ممّا تقرؤه القوالب (2,911) "
       "يُفهم بلا قرينة 2,748 (94.4%)؛ مشتركُ الوضع 48 ومشتركُ الصورة 115، ووسمُ المرجع قرينةً "
       "يفصلهما", _S,
       "test:tests/test_wad.py::test_masaq_measurement_and_index",
       note="أكبرُ المشترك المقيس: اللَّهُ بسابقة أل على أَفْعَلَ/فَعَّلَ (87) — العلَمُ بالمعجم؛ وآمَنَ تُقرأ "
            "فَاعَلَ بالخانة."),
    # — المتباين —
    _c("TABAYUN-rel", "التباينُ على الخانات (كلمتان لا مادّةَ بينهما) متماثلٌ لكلّ كلمتين وغيرُ انعكاسيّ "
       "(كلُّ ذي مادّةٍ يشارك نفسَه)؛ والحصرُ السباعيُّ باعتبار الدالّ والمدلول يُقرأ بعدد الكلمات وعدد "
       "الموادّ وله قسمٌ ثامن تقرؤه الخانة: المتداخلان", _P,
       "lean:Slge.Tabayun.tabayun_symm", "lean:Slge.Tabayun.shareMadda_self",
       "lean:Slge.Tabayun.tabayun_irrefl", "lean:Slge.Tabayun.rel_witnesses",
       "lean:Slge.Tabayun.seven_not_exhaustive",
       "test:tests/test_tabayun.py::test_tabayun_is_symmetric_and_irreflexive",
       "test:tests/test_tabayun.py::test_seven_fold_division_and_its_eighth",
       note="اِنْتِشَارٌ/نَشْرٌ متداخلان (ن‑ش‑ر مشتركة وت‑ش‑ر منفردة)؛ المنقولُ والحقيقةُ والمجازُ لا "
            "خانةَ لها."),
    _c("TABAYUN-asl", "الأصلُ في الوضع التباين: على القالب المعزول (77 من الـ121) جذران مختلفان لا "
       "ألفَ فيهما كلمتان متباينتان على قالبٍ واحد — لكلّ قالبٍ معزول ولكلّ جذرين؛ والترادفُ التامُّ "
       "مستحيل (الملءُ دالّة)", _P,
       "lean:Slge.Tabayun.tabayun_of_isolated", "lean:Slge.Tabayun.mawadd_fill_isolated",
       "lean:Slge.Tabayun.isolated_count", "lean:Slge.Tabayun.fill_functional",
       "test:tests/test_tabayun.py::test_default_is_divergence_on_isolated_templates",
       note="على غير المعزول يقع التداخل (اِنْفِعَالٌ/اِفْتِعَالٌ)؛ وfill_functional بديهيّ."),
    _c("TABAYUN-masaq", "على 936 صورةً مقروءةً من MASAQ بشهادات البوّابة: بين كلّ صورتين (437,580 "
       "زوجًا) متباينان 99.82%، متّحدا المادّة 760، متداخلان 13؛ عائلاتُ المادّة 565 أكبرُها ن‑ز‑ل "
       "وك‑ف‑ر (10 صور)", _S,
       "test:tests/test_tabayun.py::test_masaq_measurement_and_index",
       note="متّحدا المادّة ترادفُ صورةٍ لا معنًى؛ وفَعَالٌ (سَوَادٌ/بَيَاضٌ) ليست في المعجم المودَع."),
    # — البتّاتُ على السُّلَّم —
    _c("BITS-ladder", "شهاداتُ المدوّنة المختومة (18,179 صورة / 78,207 كلمة، مودَعةً خاناتٍ وأعدادًا لا "
       "نصًّا) تمرّ بالدرجات بلا ضياع: الخاناتُ ذرّاتٌ بعينها 18,179/18,179؛ fold < U(n) "
       "وunfold∘fold = id على 18,114/18,114؛ مجموعُ بتّات الطيّ 658,873 ≤ Σ width(n) 672,465؛ "
       "المصحفُ تيارًا واحدًا 78,100 "
       "كلمةً = 2,792,533 بتًّا = Σ cost(k)، وكلُّ كلمةٍ تعود؛ المنحُ = الترخيصُ 18,114", _S,
       "lean:Slge.slgeFold_lt", "lean:Slge.Sequence.slgeUnfold_slgeFold",
       "lean:Slge.Sequence.decodeWord_encodeWord", "lean:Slge.Sequence.decode_encode",
       "lean:Slge.Grant.mursam_sound",
       "test:tests/test_bits.py::test_fold_under_its_proven_bound_and_back",
       "test:tests/test_bits.py::test_whole_mushaf_as_one_stream",
       note="عددُ الشهادة في الغانم Σ 1,276,753 بتًّا = 1.96 × عددِ الذرّات قبل اقتران كانتور (651,981) "
            "ليحمل 38 بتًّا من الرتبة — مقيس؛ تغييرُه قرارُ برهانٍ في A116.Numbering."),
    # — المدود —
    _c("MADD-letter", "حرفُ المدّ خانةٌ ساكنةٌ بعد حركتها (الصنفُ v في التقطيع الثلاثيّ): لا مدَّ في صدر "
       "كلمةٍ ولا مدّان متجاوران لكلّ كلمة؛ والترخيصُ الثنائيُّ هو binOK على الأصناف لكلّ كلمة", _P,
       "lean:Slge.Madd.kinds_head_not_v", "lean:Slge.Madd.no_adjacent_madd",
       "lean:Slge.Madd.licensed_eq_binOK", "lean:Slge.Madd.kindOf_cv",
       "test:tests/test_madd.py::test_madd_letter_is_sukun_after_its_vowel_and_never_initial_or_adjacent",
       note="kinds مرآةُ gate.licence.kind_of على الخانات؛ مطابَقةٌ بجدول madd.csv على الـ121."),
    _c("MADD-lazim", "المدُّ اللازم (مدٌّ ثمّ ساكنٌ أصليّ) هو فاصلُ الترخيص الثلاثيّ عن الثنائيّ: في كلمةٍ "
       "مرخَّصةٍ وصلًا مدٌّ لازمٌ ⇔ غيرُ مرخَّصةٍ ثنائيًّا — لكلّ كلمة؛ وعلى المصحف 65 صورةً "
       "ثلاثيّةً فقط "
       "= 65 صورةَ لازم", _P,
       "lean:Slge.Madd.lazim_iff_not_binary", "lean:Slge.Madd.hasVC_iff_not_binOK",
       "lean:Slge.Madd.addallin_ternary_only",
       "test:tests/test_madd.py::test_lazim_separates_ternary_from_binary",
       "test:tests/test_madd.py::test_corpus_measurement_and_index",
       note="الضَّالِّينَ وحَاجَّ: مثقَّلٌ (مضعَّف)؛ ءَالْءَانَ مخفَّف. اللازمُ الحرفيّ (الٓمٓ) غيرُ مشكولٍ فلا يدخل."),
    _c("MADD-rules", "أحكامُ المدّ من الخانة التالية والحدّ: همزةٌ في الكلمة ⇒ متّصل، ساكنٌ ⇒ لازم، همزةٌ "
       "صدرَ التالية ⇒ منفصلٌ وصلًا (لكلّ كلمة)، قبل الأخيرة وقفًا ⇒ عارضٌ والكلمةُ نفسُها "
       "طبيعيٌّ وصلًا "
       "(لكلّ كلمة)؛ "
       "واللينُ والصلةُ ملحقان، والواوُ الساقطةُ محجوبةٌ بالجدول", _P,
       "lean:Slge.Madd.arid_iff_pause", "lean:Slge.Madd.munfasil_iff_next_hamza",
       "lean:Slge.Madd.silent_waw_tabled", "lean:Slge.Madd.madd_witnesses",
       "test:tests/test_madd.py::test_rules_read_from_next_cell_and_boundary",
       note="المقاديرُ معلَنة؛ الألفُ الخنجريّة ليست في المدوّنة المختومة؛ مدُّ العوض بقيّةُ رسمٍ في "
            "الغانم."),
    _c("MADD-masaq", "على المصحف المشهود (78,207 كلمة، 47,865 حرفَ مدّ): طبيعيّ 40,230، منفصل 5,619، "
       "متّصل "
       "1,744، لازم 108، صلة 4,591، محجوب 164؛ وقفًا سقفُ العارض 16,627 واللين 3,031؛ وعلى "
       "MASAQ الهاءُ "
       "بين متحرّكين هاءُ كنايةٍ في 55.2%", _S,
       "test:tests/test_madd.py::test_corpus_measurement_and_index",
       note="الخانةُ لا تفصل هاءَ الكناية من هاء الكلمة (اللَّه): الصلةُ قراءةٌ بشرط القرينة."),
    # — البوّاباتُ المتتابعة والسجلّ —
    _c("GATES-ladder", "شهادةُ الغانم تصعد SLGE سبعَ بوّاباتٍ متتابعة (الخانة، الترخيص، العدد حاكمةً؛ "
       "الجداول، الصرف، الإعراب، الجواب قارئةً)، ولا بوّابةَ فوق مرفوضة، والمخرجُ ذرّاتٌ بعينها؛ على "
       "المصحف 18,114 صورةً تصعد كلَّه و65 تقف عند العدد باسمها", _S,
       "lean:Slge.Grant.ladder_implies_base", "lean:Slge.Grant.no_grant_of_refused",
       "test:tests/test_gates.py::test_ladder_order_and_named_refusals",
       "test:tests/test_gates.py::test_whole_mushaf_climbs_consistently",
       note="قانونُ السُّلَّم مبرهَنٌ على المجرّد؛ البوّاباتُ تركّب الدوالَّ القائمة (مفحوص) ولا تبني قراءة."),
    _c("GATES-manifest", "السجلُّ مصدرٌ واحدٌ لمواضع كلّ وحدة (65 وحدة، 53 جدولًا، 43 فهرسًا): كلُّ وحدةٍ "
       "موصولةٌ في Lean والتدقيق والتصدير والفهرس والاختبار وبالعكس، وCI يأخذ قوائمَه منه", _X,
       "test:tests/test_gates.py::test_manifest_covers_the_tree",
       note="ما نُسي من المواضع العشرة يسقط الفحص بدل أن يُكتشف باليد."),
    # — الجذع: تسويةُ الآخر وفصلُ الزوائد —
    _c("JIDH-case", "الإعرابُ والمزاجُ حالةُ الخانة الأخيرة لا جزءٌ من القالب: استخراجُ الجذر لا يرى "
       "الحالات لكلّ قالبٍ وكلمةٍ وحالة، وملءُ قالبٍ سليم بأيّ حالةٍ في آخره يُقرأ على قالبه ويُستردّ جذرُه "
       "بعينه", _P,
       "lean:Slge.Jidh.rootOf_setLast", "lean:Slge.Jidh.onTemplateMod_setLast",
       "lean:Slge.Jidh.setLast_fill",
       "test:tests/test_jidh.py::test_case_is_the_last_cell_not_the_template",
       note="القوالبُ أُودعت بآخرٍ واحد (wazn.py: parse(«فَعْلُ»))؛ التسويةُ تسبق المطابقة في كلّ قارئٍ "
            "جديد."),
    _c("JIDH-peel", "الجبرُ مغلقٌ صعودًا ونزولًا: سابقةٌ متحرّكة على مرخَّصٍ مرخَّصٌ (لكلّ سابقةٍ وكلمة)، "
       "والقطعُ عكسُ الإلصاق بعينه (لكلّ كلمة)، والقارئُ لا يعيد قراءةً إلّا وردُّها الكلمةُ بعينها "
       "وجذعُها مرخَّصٌ في ذاته؛ وما صعد بالجبر ينزل بالقارئ: لكلّ سابقةٍ ولاحقةٍ من الجداول وقالبٍ سليم "
       "وجذرٍ وحالةِ آخر", _P,
       "lean:Slge.Jidh.prefix_licensed", "lean:Slge.Jidh.peelPrefix_append",
       "lean:Slge.Jidh.peelSuffix_append", "lean:Slge.Jidh.dropAl_al",
       "lean:Slge.Jidh.jidh_complete",
       "lean:Slge.Jidh.peelPrefix_sound", "lean:Slge.Jidh.peelSuffix_sound",
       "lean:Slge.Jidh.dropAl_sound", "lean:Slge.Jidh.jidh_restores",
       "lean:Slge.Jidh.jidh_witnesses_al", "lean:Slge.Jidh.jidh_witnesses_case",
       "lean:Slge.Jidh.jidh_witnesses_affix",
       "test:tests/test_jidh.py::test_peeling_restores_the_word_exactly",
       note="التعدّدُ يُقرأ كما هو (كَذَّبُوا: فَعَّلَ+وا أو كَ+الذَّبُو) والقرينةُ تفصله."),
    _c("JIDH-masaq", "على مودَع المصحف نفسِه (18,179 صورةً بزوائدها): القوالبُ تقرأ 1,743 كما هي، "
       "و4,815 بعد تسوية الآخر وحدَها (والنونُ الساكنةُ لامٌ قبل أن تكون تنوينًا)، و14,912 (82.0%) بعد "
       "فصل الزوائد والنزول بالإعلال؛ وعلى قسمة MASAQ المحجوبة (40,731): قراءةٌ واحدةٌ توافقها "
       "35.5%، "
       "وبين قراءاتٍ متعدّدة 33.2%، وعلى غيرها 15.3%، ولا قراءة 15.9%", _S,
       "test:tests/test_jidh.py::test_numbers_before_and_after_on_the_same_deposit",
       note="ما بقي باسمه: قالبا فِعْلٍ وفَعَالٍ غيرُ مودَعين، والجداولُ تقرأ أدواتِها، والأصلُ الواويُّ "
            "واليائيُّ قراءتان تفصلهما القرينةُ المعجميّة."),
    # — الإعلالُ والإبدال: جبرٌ مغلقٌ صعودًا ونزولًا —
    _c("ILAL-inverse", "القواعدُ الثلاثَ عشرةَ صعودٌ من الأصل إلى الصورة في نافذة، والنزولُ عكسُه بعينه: "
       "كلُّ أصلٍ ينزل إليه القارئُ يصعد إلى الصورة بعينها، وكلُّ أصلٍ يصعد ينزل إليه — لكلّ قاعدةٍ وكلمةٍ "
       "وموضع", _P,
       "lean:Slge.Ilal.down_sound", "lean:Slge.Ilal.down_complete", "lean:Slge.Ilal.undo_sound",
       "lean:Slge.Ilal.undo_complete", "lean:Slge.Ilal.up_length",
       "test:tests/test_ilal.py::test_every_rule_ascends_and_descends_exactly",
       note="هندسةٌ عكسيّةٌ لـA116.Ilal: هناك سجلُّ تعديلٍ يردّ الأصلَ (edit_roundtrip)، وهنا النزولُ دالّةٌ "
            "من الصورة إلى أصولها كلِّها."),
    _c("ILAL-closed", "القلبُ بين متحرّكين، والنقلُ، وحذفُ واو المثال، وقلبُ اللام، وحذفُ اللام، "
       "والإبدالُ تحفظ الترخيصَ — عبر الجسر إلى أدوات الغانم بعينها؛ وأصلُ حذف العين (ألفٌ ساكنةٌ قبل "
       "ساكن) غيرُ مرخَّصٍ فالحذفُ ملزَم", _P,
       "lean:Slge.Ilal.qalbAyn_closed", "lean:Slge.Ilal.naql_closed",
       "lean:Slge.Ilal.hadhfWaw_closed", "lean:Slge.Ilal.qalbLam_closed",
       "lean:Slge.Ilal.hadhfLam_closed", "lean:Slge.Ilal.ibdal_closed",
       "lean:Slge.Ilal.hadhfAyn_forced", "lean:Slge.Ilal.closure_witnesses",
       "test:tests/test_ilal.py::test_closure_and_forcing_on_licensing",
       note="الشروطُ اللغويّة (حرفُ المضارعة، ضمُّ اللام قبل واو الجماعة، مواضعُ النوافذ) معلَنةٌ "
            "لا مبرهَنة — كما في الغانم."),
    _c("ILAL-descent", "القارئُ ينزل حتى خطوتين وكلُّ ما ينزل إليه يصعد بسلسلته إلى الكلمة بعينها، "
       "وما صعد بخطوةٍ في موضعه ينزل؛ وفي الجذع: أصلُ كلّ قراءةٍ يصعد بسلسلتها إلى جذعها، وما صعد من "
       "قالبٍ وجذرٍ بقاعدةٍ ينزل بالقارئ", _P,
       "lean:Slge.Ilal.descend_ascends", "lean:Slge.Ilal.descend_complete",
       "lean:Slge.Ilal.step1_sound", "lean:Slge.Ilal.step1_complete",
       "lean:Slge.Jidh.readingsAt_ascends", "lean:Slge.Jidh.jidh_ascends",
       "lean:Slge.Jidh.jidh_complete_ilal", "lean:Slge.Ilal.up_witnesses",
       "lean:Slge.Ilal.down_qala", "lean:Slge.Ilal.down_qul", "lean:Slge.Ilal.down_yaqulu",
       "lean:Slge.Ilal.down_daa", "lean:Slge.Ilal.down_yaidu", "lean:Slge.Ilal.down_amana",
       "lean:Slge.Ilal.down_mizan", "lean:Slge.Ilal.down_istabara",
       "lean:Slge.Jidh.jidh_witnesses_ilal_qalb", "lean:Slge.Jidh.jidh_witnesses_ilal_hadhf",
       "test:tests/test_ilal.py::test_descent_is_bounded_and_every_descent_ascends",
       "test:tests/test_ilal.py::test_jidh_reads_by_descent_with_named_origins",
       note="قُلْ وكُنْتُمْ بخطوتين (قلبٌ ثمّ حذفٌ ملزَم)؛ والنزولُ لا يُجرى إلّا إن لم يُقرأ الجذعُ مباشرةً "
            "(أولويّةٌ معلَنة)."),
    _c("ILAL-roundtrip", "الردُّ بسجلّ الغانم بعينه: لكلّ قاعدةٍ وأصلٍ وموضع، ردُّ الصورة بسجلّ "
       "التعديل (البداية، طولُ المدرَج، المحذوف) هو الأصلُ بعينه — مثولُ edit_roundtrip — وعلى خانات "
       "الغانم عبر الجسر بالسجلّ نفسِه؛ وإبدالُ حاملٍ غيرِ حرف مدٍّ بمثله (تاءُ الافتعال طاءً أو دالًا، "
       "فاؤُه تاءً) لا يغيّر الأصنافَ الثلاثة فلا الترخيصَ الثلاثيَّ وصلًا ووقفًا", _P,
       "lean:Slge.Ilal.apply_roundtrip", "lean:Slge.Ilal.apply_roundtrip_a116",
       "lean:Slge.Ilal.restoreEdit_map", "lean:Slge.Ilal.ibdal_kinds",
       "lean:Slge.Ilal.ibdal_ternary", "lean:Slge.Ilal.kindOf_carrier",
       "lean:Slge.Ilal.kindsAux_state",
       "lean:Slge.Ilal.roundtrip_witnesses",
       "test:tests/test_ilal.py::test_roundtrip_by_the_alghanem_record",
       note="سجلُّ SLGE هو سجلُّ الغانم: النزولُ دالّةً (down) والردُّ سجلًّا (record) وجهان لبرهانٍ واحد."),
    _c("ILAL-law", "قانونُ الإبدال على المودَع عدًّا لا حكمًا: بعد حرف الإطباق الساكن تاءٌ 17 وطاءٌ 108، "
       "وبعد د/ذ/ز الساكنة تاءٌ 20 ودالٌ 297؛ والتاءُ الباقيةُ (32 رسمًا: بَسَطتَ، حَرَصتُم، أَخَذتُ…) تاءُ "
       "فاعلٍ أو خطابٍ لا تاءُ افتعال", _S,
       "test:tests/test_ilal.py::test_numbers_on_the_deposit",
       note="«لا تبقى التاءُ بعد الإطباق» بلا شرط الافتعال منقوضٌ في المودَع 17 مرّة؛ وبشرطه المعلَن "
            "لا نقضَ له. لا بديهيّةَ هنا."),
    _c("ILAL-masaq", "على مودَع المصحف نفسِه: 2,138 صورةً لها قراءةٌ بالإعلال (11.8%)، منها 1,000 لا "
       "تُقرأ إلّا به (5.5%)؛ وكلُّ قراءةٍ (6,516) صعد أصلُها بسلسلتها على المودَع؛ وعلى قسمة MASAQ "
       "المحجوبة: 9,249 كلمةً لا تُقرأ إلّا بالإعلال لاحقةُ المرجع بين قراءاتها في 92.4%", _S,
       "test:tests/test_ilal.py::test_numbers_on_the_deposit",
       note="باسمه: المبنيُّ للمجهول والمجزومُ من الأجوف ليسا من القواعد؛ والإعلالُ بثلاث خطوات."),
    # — القرينةُ المعجميّة: عضويّةُ الجذر في مقاييس اللغة —
    _c("MAQAYIS-member", "العضويّةُ في مقاييس اللغة (4,561 جذرًا ثلاثيًّا حواملَ، جدولٌ مولَّدٌ من مودَعٍ "
       "مختوم) دالّةٌ على الخانات لا بحثَ خارج الجدول، والمعتلّةُ في الطبعة تطابق الواوَ أو الياءَ لا "
       "غير، وقراءةٌ أصلُها على قالبٍ سليم بجذرٍ مشهود مشهودةٌ", _P,
       "lean:Slge.Maqayis.member_sound", "lean:Slge.Maqayis.matchesL_weak",
       "lean:Slge.Maqayis.matchesL_exact", "lean:Slge.Maqayis.attested_of_member",
       "lean:Slge.Maqayis.member_witnesses",
       "test:tests/test_maqayis.py::test_membership_is_on_cells_and_weak_matches_waw_or_ya_only",
       note="الجدولُ عضويّةٌ لا معنًى: محاورُ المعاني لم تُودَع؛ والرباعيُّ الثلاثةُ أُسقط باسمه."),
    _c("MAQAYIS-rank", "الترتيبُ بالقرينة — المشهودُ أوّلًا — لا يُسقط قراءةً ولا يزيدها لكلّ قائمة؛ وعلى "
       "الشاهد: كَذَّبُوا تفصلها (كذب مشهودٌ وذبو لا)، وقَالَ لا تفصلها (قول وقيل كلاهما مشهود)", _P,
       "lean:Slge.Maqayis.mem_rank", "lean:Slge.Maqayis.length_rank",
       "lean:Slge.Maqayis.rank_kadhdhabu", "lean:Slge.Maqayis.rank_qala",
       "lean:Slge.Maqayis.rank_fariqun",
       "lean:Slge.Jidh.stemSenses_eq_stemForm",
       "test:tests/test_maqayis.py::test_rank_keeps_every_reading_and_puts_attested_first",
       note="بوّابةُ الجذع تعيد القراءاتِ مرتّبةً بالقرينة (`gates._g5`) والتعدّدُ باقٍ كما هو."),
    _c("MAQAYIS-masaq", "على مودَع المصحف نفسِه: الصورُ متعدّدةُ القراءات 3,896 ← 2,895 (فصلت القرينةُ "
       "1,001، 25.7% من المتعدّد)، و2,178 صورةً لا قراءةَ مشهودةً لها؛ وعلى قسمة MASAQ المحجوبة "
       "(40,731): "
       "قراءةٌ واحدةٌ موافقة 35.5% ← 40.0%، وبين متعدّدة 33.2% ← 27.6%، والقرينةُ تُسقط قسمةً "
       "ذهبيّةً في 1.1% (458: قراءةٌ على قالبٍ بجذرٍ غيرِ مشهود لما تقرؤه الجداول أو للمضارع الأجوف)", _S,
       "test:tests/test_maqayis.py::test_numbers_before_and_after_on_the_same_deposit",
       note="الخسارةُ تُذكر كما يُذكر الربح؛ والقرينةُ ترتّب ولا تُسقط. الجذرُ من صورة الجذع "
            "(`stemSenses_eq_stemForm`) لا من الجذع كما هو — كان التنوينُ يمنع الجذرَ فتبقى 4,347 "
            "بلا قراءةٍ مشهودة (أُصلح في اليوم نفسه)."),
    # — قوالبُ الاسم على أبنية سيبويه (أ2) —
    _c("ABNIYA-ism", "قوالبُ الاسم الأربعةُ المضافة (فِعْل، فَعَال، فُعَيْل، فَاعُول) هياكلُها عند سيبويه، "
       "وحوافُّها من آبائها في الشبكة بعمليّاتٍ مفحوصة، وسليمةٌ مرخَّصةٌ لكلّ أصل", _P,
       "lean:Slge.Abniya.ism_in_abniya", "lean:Slge.Shabaka.edges_apply", "lean:Slge.Wazn.awzan_wf",
       "lean:Slge.Wazn.awzan_licensed",
       "test:tests/test_abniya.py::test_added_noun_templates_satisfy_the_three_conditions",
       note="المعلَّقُ باسمه (ABNIYA_INDEX.md): فَعِل (يتساوى مع فَعِلَ)، فَيْعِل، فُعْلَة، فَعِيلَة، مَفْعِلَة، "
            "النسبةُ، فُعَالَة — لم ترفع الموافقةَ على MASAQ أو أنزلتها."),
    _c("ABNIYA-disjoint", "التمايز: قالبان مفصولان (يختلفان في زائدٍ، أو زائدٌ قبالةَ أصل، أو أصلان "
       "بحالتين، أو في الآخر بالحامل) لا يقرآن ملءً واحدًا بعد تسوية الآخر على أصلين نظيفين — لكلّ "
       "قالبين من الجدول "
       "وأصلين وحالتين؛ وكلُّ زوجين من الـ125 مفصولان إلّا 11 مسمّاة", _P,
       "lean:Slge.Abniya.separated_sound", "lean:Slge.Abniya.awzan_disjoint",
       "lean:Slge.Abniya.awzan_separated", "lean:Slge.Abniya.ambiguous_sound",
       "lean:Slge.Abniya.awzan_lits",
       "test:tests/test_abniya.py::test_separation_refuses_one_fill_for_two_templates_on_clean_roots",
       note="الأزواجُ غيرُ المفصولة هي بعينها ما يعيده الجذعُ قراءاتٍ متعدّدةً على جذرٍ واحد (الماضي "
            "ومصدرُه، الماضي والأمر، القالبُ المكرَّر)."),
    _c("ABNIYA-masaq", "على مودَع المصحف نفسِه: الجذعُ 14,912 ← 15,510 من 18,179 (82.0% ← 85.3%)؛ فِعْلٌ "
       "وحدَه يقرأ 406 صورةً لا تُقرأ إلّا عليه وفَعَالٌ 265؛ وعلى قسمة MASAQ المحجوبة: لا قراءة 15.9% ← "
       "12.2%، وقراءةٌ واحدةٌ موافقة 35.5% ← 38.0%، وبعد القرينة المعجميّة 40.0% ← 43.0%", _S,
       "test:tests/test_abniya.py::test_numbers_before_and_after_on_the_same_deposit",
       note="ما نقص يُذكر: صورٌ تُقرأ بالإعلال 2,138 ← 1,960 (صارت تُقرأ مباشرةً على فِعْل/فَعَال)، "
            "وما تقرؤه الجداول (إِنَّ، مِنْ) صار يُقرأ على فِعْل أيضًا — الجداولُ قبل القوالب (أ4)."),
    # — الأدواتُ علاقاتٍ تشغيليّة —
    _c("ADAWAT-structure", "كلُّ أداةٍ من الجدول الموحَّد (68) على بنيةٍ واحدة: الصورةُ خاناتٍ، الرتبةُ، "
       "أصنافُ المعمولات بعدد الرتبة، والعاملُ في الاسم معمولُه الأوّل اسمٌ وفي الفعل فعلٌ والعاطفُ "
       "ثنائيّ؛ والعملُ دالّةٌ على خانة آخر المعمول تعيد مرخَّصًا على المعرب (لكلّ أداةٍ وكلمة)، "
       "والجزمُ بتسكينٍ مرخَّصٍ ما لم يسبقه مدّ", _P,
       "lean:Slge.Adawat.table_length", "lean:Slge.Adawat.args_arity",
       "lean:Slge.Adawat.args_of_amal", "lean:Slge.Adawat.apply_licensed",
       "lean:Slge.Adawat.apply_jazm_licensed",
       "test:tests/test_adawat.py::test_amal_is_a_licensed_function_on_the_last_cell",
       note="نوعُ العلاقة (تعدية، توكيد، نفي، شرط، جمع، ترتيب، تخيير…) عمودٌ معلَنٌ من كتب حروف "
            "المعاني لا مبرهَن: الخاناتُ لا تحمل معنى، ولا جداولَ صدقٍ هنا."),
    _c("ADAWAT-composition", "التركيبُ بعينه والكفّ: كَأَنَّ = كَ ++ أَنَّ، أَلَا = أَ ++ لَا، أَمَا = أَ ++ مَا، "
       "لِكَيْ = لِ ++ كَيْ وكَيْلَا = كَيْ ++ لَا بعملِ كَيْ، وإِنَّمَا = إِنَّ ++ مَا بلا عمل", _P,
       "lean:Slge.Adawat.compositions", "lean:Slge.Nawasikh.kaffa_forms",
       "test:tests/test_adawat.py::test_compositions_and_kaff_are_exact"),
    _c("ADAWAT-rank", "الأداةُ المجاورة تقدّم قراءاتِ جارتها التي صنفُها صنفُ معمولها الأوّل ولا تُسقط "
       "قراءةً ولا تزيدها (لكلّ أداةٍ وقائمة)؛ وعلى الشاهد: لَمْ تجزم يَكْتُبُ وإِنَّ تنصب كِتَابٌ وتُبقي "
       "قراءتَي فَرِيقٌ", _P,
       "lean:Slge.Adawat.mem_rank", "lean:Slge.Adawat.length_rank", "lean:Slge.Adawat.witnesses",
       "test:tests/test_adawat.py::test_rank_puts_the_fitting_category_first_and_drops_nothing",
       note="بوّابةُ «الأدوات» في السُّلَّم بعد الجذع تقرأ الأداةَ السابقة من السياق "
            "(`climb(prev=…)`)."),
    _c("ADAWAT-masaq", "على قسمة MASAQ المحجوبة (40,731؛ 29,866 لها تالية): بعد الجارّ القائم بنفسه "
       "التاليةُ مجرورةٌ 89.8% (3,701)، وبعد ناصب الفعل منصوبةٌ 80.0% بلا مخالف، وبعد الجازم مجزومةٌ "
       "بلا مخالف؛ والجارُّ المتّصل 81.5%؛ وللتالية ذات القراءات من الصنفين (593): القراءةُ الأولى "
       "بصنف المرجع 49.9% ← 96.5% بترتيب الأداة", _S,
       "test:tests/test_adawat.py::test_numbers_before_and_after_on_masaq",
       note="المخالفُ باسمه: معمولُ الأداة ليس التاليةَ دائمًا، والصورةُ المشتركة (لَا ×4) تُؤخذ بأوّل "
            "مدخل فضعف «نصب الاسم» (21.4%) — فصلُ المشترك شأنُ الجملة."),
    # — الجهةُ الوجوديّة: المصدرُ والمشتقُّ والجامدُ تقسيمًا مغلقًا —
    _c("WUJUD-partition", "كلُّ قالبٍ من الـ125 على صنفٍ واحد من ستّة (فعل 37، مصدر 22، وصفٌ مشتقّ 25، "
       "ظرفٌ وآلة 7، صيغةُ جمع 30، اسمٌ 4)؛ الفعلُ هو قوائمُ الماضي والمضارع والأمر بعينها، والمصدرُ "
       "قوالبُ المصدر بعينها، والوصفُ داخل قوالب الوصف إلّا فُعَلَاءُ جمعًا", _P,
       "lean:Slge.Wujud.table_length", "lean:Slge.Wujud.table_length_N",
       "lean:Slge.Wujud.class_counts", "lean:Slge.Wujud.fil_eq",
       "lean:Slge.Wujud.masdar_eq", "lean:Slge.Wujud.wasf_derived",
       "test:tests/test_wujud.py::test_partition_is_total_and_six_fold",
       note="الأصنافُ من أبواب الأوزان المودَعة (معلَن)؛ الجمودُ قيدٌ معجميٌّ لا تفصله الخانة: فِعْلٌ "
            "عِلْمًا مصدرٌ ورِجْلًا جامد."),
    _c("WUJUD-closure", "الإغلاقُ المنطقيّ والأنطولوجيّ: كلُّ فعلٍ له صيغةٌ على ميزانه ولا صيغةَ لمصدر، "
       "وكلُّ وصفٍ مشتقٌّ على ميزانه إلّا المقصورَين؛ أصلُ الشبكة مصدرٌ، ولا شيءَ ينحدر من اسمٍ ولا من "
       "صيغة جمع، والمشتقُّ أبوه فعلٌ أو مشتقّ", _P,
       "lean:Slge.Wujud.fil_sigha_mizan", "lean:Slge.Wujud.masdar_no_sigha_mizan",
       "lean:Slge.Wujud.wasf_derived_mizan", "lean:Slge.Wujud.root_masdar",
       "lean:Slge.Wujud.ism_jam_leaves", "lean:Slge.Wujud.mushtaqq_from_fil_or_mushtaqq",
       "lean:Slge.Jiha.sigha_of_fill", "lean:Slge.Kulli.masdar_no_sigha",
       "test:tests/test_wujud.py::test_closure_against_existing_lists_and_network",
       note="هذا معنى «المصدرُ أصلُ المشتقّ» و«الجامدُ لا يُشتقّ منه» على الجدول لا في الكلام."),
    _c("WUJUD-reader", "الكليُّ يقرأ الجهةَ المودَعة على الميزان في 111 من 125، والمخالفُ 14 بأرقامها: "
       "اشتراكُ الصورة (أَفْعَلُ/أَفْعُلُ مضارعُ المتكلّم، فِعْلَة جمعًا وهيئة، فِعَال وفُعُول جمعًا ومصدرًا، "
       "مُفَاعَلَة ومِفْعَال وفَعَّالَة بصورة المشتقّ، فُعَلَاء) أو ما لا يقرؤه (المقصور)؛ وجهةُ القراءة من "
       "قوالبها، والترتيبُ بجهةٍ لا يُسقط قراءةً", _P,
       "lean:Slge.Wujud.kulli_agreement", "lean:Slge.Wujud.mem_rank", "lean:Slge.Wujud.length_rank",
       "lean:Slge.Wujud.witnesses",
       "test:tests/test_wujud.py::test_reader_agreement_names_its_exceptions"),
    _c("WUJUD-masaq", "على مودَع المصحف (18,179): جهةُ القراءة الأولى فعلٌ 7,250، مصدرٌ 2,959، وصفٌ "
       "2,436، ظرفٌ وآلة 155، جمعٌ 1,813، اسمٌ 897، لا قراءة 2,669؛ وعلى وسوم MASAQ المحجوبة (23,847 "
       "مقروءة): الموافقةُ 52.2% (الفعلُ 83.4%، المصدرُ 49.9%، الوصفُ 53.6%، الاسمُ 30.2%)، وبعد ترتيب "
       "الأداة 52.4%", _S,
       "test:tests/test_wujud.py::test_numbers_on_the_deposit_and_masaq",
       note="الاسمُ عند المرجع يُقرأ هنا مصدرًا في 4,044 لأنّ القالبَ لا يفصل الاسمَ من المصدر (فَعْل، "
            "فِعَال)؛ والفعلُ يُقرأ وصفًا/اسمًا في 1,090 — القوالبُ المشتركة؛ كلٌّ باسمه."),
    _c("MAANI-table", "معاني الحروف منقولةٌ من مبحث «الحرف» في الشخصيّة ج3 بترتيب المصدر "
       "(مودَعٌ مختوم؛ 25 مدخلًا، 29 حرفًا من الجدول الموحَّد)، كلُّ فهرسٍ فيها فهرسٌ في "
       "`Huruf.table`؛ المتعدّدُ تسعةٌ بأرقامها "
       "(الباء 7، من 4، أو 4، في 3، لا النافية 3، اللام/إلى/حتّى/حتّى العاطفة 2)؛ وحروفُ "
       "الجرّ بلا معنًى في "
       "المصدر خلا وعدا وحاشا بأرقامها", _P,
       "lean:Slge.Maani.table_length", "lean:Slge.Maani.indices_in_table",
       "lean:Slge.Maani.multi_eq", "lean:Slge.Maani.jarr_uncovered",
       "test:tests/test_maani.py::test_table_follows_the_source_order",
       "test:tests/test_maani.py::test_deposit_is_sealed_and_tables_are_generated_from_it",
       note="المعاني أسماءٌ من النصّ بالمطابقة الحرفيّة (`tools/deposit_maani.py`)؛ لا معنى يُختار "
            "ولا يُستنتج: ما لم يذكره المصدرُ فارغٌ باسمه."),
    _c("MAANI-rank", "الأصلُ أوّلًا: حيث ذكر المصدرُ معنى غايةٍ أو ظرفيّةٍ لحرفٍ ذكره أوّلَ معانيه؛ والترتيبُ "
       "بالقرينتين (ظرفٌ بعده، نفيٌ قبله) يحفظ العضويّةَ والعدد ولا يُسقط معنًى، وبلا "
       "قرينةٍ يعيد ترتيبَ "
       "المصدر بعينه", _P,
       "lean:Slge.Maani.ghaya_first_in_source", "lean:Slge.Maani.mem_rank",
       "lean:Slge.Maani.length_rank", "lean:Slge.Maani.rank_none", "lean:Slge.Maani.witnesses",
       "test:tests/test_maani.py::test_rank_by_clue_keeps_every_sense",
       note="القرينتان معلَنتان: الظرفُ من جدولَي `Zuruf`/`Zaman`، والنفيُ قبله يقدّم «زائدة» "
            "تعميمًا لشاهد "
            "المصدر الوحيد («ما جاءني من أحد»)."),
    _c("MAANI-masaq", "على MASAQ: 7,369 وقوعًا لحرفٍ له معانٍ؛ القرينتان غيّرتا ترتيبَ المصدر في 8 "
       "فقط (من 2، "
       "الباء 6)؛ وشواهدُ المصدر القرآنيّة على المعاني غير الأولى: يقدّمها الترتيبُ في 1 "
       "من 5 وُجدت — المعنى "
       "حاضرٌ في القائمة لا محذوف", _S,
       "test:tests/test_maani.py::test_numbers_on_masaq",
       note="«بمعنى مع» و«بمعنى على» و«من أجل» تلزمها قرينةُ المتعلَّق (الفعلُ العامل وجنسُ "
            "المجرور) — دينٌ "
            "باسمه؛ و«أو» بالمقام تحتاج `Uslub` على الجملة."),
    _c("MUKHASSAS-tree", "شجرةُ المخصّص كما هي من المختوم (1,600 عقدة: 73/337/1,190) بلا إعادة "
       "تصنيف: "
       "المعرّفاتُ مواضع، الأبُ أسبقُ وأدنى مستوًى وكتابُ الابن كتابُ أبيه، المستوى الأوّل وحدَه بلا أب، "
       "وكتابُ كلّ عقدةٍ من المستوى الأوّل", _P,
       "lean:Slge.Mukhassas.nodes_length", "lean:Slge.Mukhassas.ids_are_positions",
       "lean:Slge.Mukhassas.parent_lt", "lean:Slge.Mukhassas.parent_level_lt",
       "lean:Slge.Mukhassas.level_one_iff_no_parent", "lean:Slge.Mukhassas.book_is_level_one",
       "lean:Slge.Mukhassas.level_counts",
       "test:tests/test_mukhassas.py::test_tree_is_the_source_tree",
       note="الاستقراءُ العامّ (الكتابُ ما تبلغه مطاردةُ الأب) غيرُ مكتوبٍ في Lean؛ محليًّا مبرهَن وشاملًا "
            "مفحوص."),
    _c("MUKHASSAS-rasm", "ربطُ عناوين الشجرة بجذور المقاييس بالرسم (قاعدةٌ معلَنة: سوابقُ ولواحق، "
       "ثلاثةُ "
       "حروف أو أربعةٌ بألف، ألفاظُ الهيكل لا تُربط): 1,080 من 1,600 عقدة، 608 جذرًا متمايزًا؛ قابليّةُ "
       "الكتاب اتّحادُ جذور ما تحته بالتعريف", _S,
       "lean:Slge.Mukhassas.caps_length",
       "test:tests/test_mukhassas.py::test_rasm_linking_is_declared_and_measured",
       note="النصُّ غيرُ مشكول: الرابطُ «مطابَقٌ بالرسم» لا «مرخَّص»."),
    _c("MUKHASSAS-hukm", "الحكمُ على (كتاب، جذر) مرتبتان: «مفهوم» بشاهدٍ عقدةٍ في الكتاب يحمل عنوانُها "
       "الجذر، أو «معلومة» بلا شاهد؛ لا «مفهوم» بلا شاهد، والشاهدُ في القابليّات "
       "الموروثة، ولا رفضَ ولا "
       "امتناع؛ شواهد: مشي مفهومٌ تحت أبواب المشي ومعلومةٌ تحت الإنسان، وجري معلومةٌ تحت النخل", _P,
       "lean:Slge.Mukhassas.mafhum_has_witness", "lean:Slge.Mukhassas.mafhum_in_capsUnder",
       "lean:Slge.Mukhassas.judge_total", "lean:Slge.Mukhassas.witnesses",
       "test:tests/test_mukhassas.py::test_judgement_is_two_graded_with_witness",
       note="أوّلُ وحدات طبقة الحكم فوق السُّلَّم (المادّة ١٠)؛ الغيابُ ليس امتناعًا (المادّة ١٦)؛ الحكمُ "
            "لـ(كتاب، جذر) لا لـ(مسنَد إليه، مسنَد) بعد."),
    _c("MUKHASSAS-masaq", "على مودَع المصحف: القراءاتُ الفعليّة الأولى 6,329 صورةً على 1,115 جذرًا (921 "
       "بلا جذرٍ في المقاييس)؛ يشهد لجذرها كتابٌ في المخصّص: 324 من 1,115 جذرًا (29.1%)، "
       "2,794 من 6,329 "
       "صورة (44.1%)", _S,
       "test:tests/test_mukhassas.py::test_numbers_on_the_deposit",
       note="قابليّةٌ لجنسٍ ما، لا للمسنَد إليه بعينه؛ والربطُ بالرسم يُسقط ما لم يُربط."),
    # — المنح: لا اسمَ قبل قبضته —
    _c("GRANT-check", "المنحُ برهانُ فحصٍ جرى؛ ما رفضه الفحصُ لا يُمنح، ولا درجةَ فوق مرفوضة", _P,
       "lean:Slge.Grant.grant_iff_check", "lean:Slge.Grant.no_grant_of_refused",
       "lean:Slge.Grant.ladder_implies_base", "lean:Slge.Grant.empty_ladder_grants_nothing",
       note="قانونُ tarkib/bridge.py بفحصٍ دالّةً لا نصًّا؛ الحكمُ المزوَّر الذي قبله الأصلُ لا يُصاغ هنا."),
    _c("GRANT-mursam", "لا يُمنح «مرسوم» إلّا لمرخَّصٍ، وهو Admissible في الـ116", _P,
       "lean:Slge.Grant.mursam_sound", "lean:Slge.Grant.mursam_refuses_initial_sukun",
       "test:tests/test_grant.py::test_mursam_grants_licensed_only"),
    _c("GRANT-forge", "لا حقلَ حكمٍ يُملأ: الفحصُ يجري كلَّ منح", _X,
       "test:tests/test_grant.py::test_verdict_cannot_be_forged",
       "test:tests/test_grant.py::test_grant_requires_check_to_run"),
    _c("GRANT-declared", "ستّةُ جسورٍ وصلت بلا فحصٍ يعمل: أسماءٌ معلَنة بدَينها لا جسور", _D,
       "test:tests/test_grant.py::test_only_one_rung_has_a_working_check"),
    # — التسلسل: النصّ تيارُ شهاداتٍ ذاتيُّ الحدّ —
    _c("SEQ-recover", "فكُّ طيِّ المرخَّصة يعيدها بعينها", _P,
       "lean:Slge.Sequence.slgeUnfold_slgeFold"),
    _c("SEQ-delim", "ترميزُ الكلمة ذاتيُّ الحدّ: تُقرأ من رأس أيّ تيارٍ ويبقى ما بعدها بعينه", _P,
       "lean:Slge.Sequence.decodeWord_encodeWord", "lean:Slge.Sequence.encodeWord_prefix_free",
       "test:tests/test_conformance.py::test_sequence_matches_lean",
       "test:tests/test_cells.py::test_stream_refuses_unlicensed_and_is_prefix_free"),
    _c("SEQ-stream", "تيارُ كلماتٍ مرخَّصةٍ يُفكّ كلُّه بترتيبه بلا فاصلٍ ولا حاملٍ زائد", _P,
       "lean:Slge.Sequence.decode_encode", "lean:Slge.Sequence.U_lt_two_pow_width",
       note="الكلفةُ معلنة: cost(k) = (k+1) + ⌊log₂U(k)⌋+1 بتًّا؛ k=1: 9، k=2: 17 (من جدول Lean)."),
    # — الاتّساق والأقانيم —
    _c("NUM-agree", "عددُ الشهادة (ترقيم الذرّات) وعددُ الطيّ متكافئان على المرخَّصات بطولٍ واحد", _P,
       "lean:Slge.Consistency.numbers_agree", "lean:Slge.Consistency.atomNumber_determines_fold",
       "lean:Slge.Consistency.fold_determines_atomNumber"),
    _c("AQ-pronoun", "الضمائرُ المنفصلة أقنومٌ سليم (كلُّها مرخَّصة) بأعدادٍ متباينة، وشكلُها ليس بصمة", _P,
       "lean:Slge.Categories.pronoun_sound", "lean:Slge.Categories.pronoun_numbers_nodup",
       "test:tests/test_conformance.py::test_categories_match_lean",
       note="خاناتُها من جسر الغانم (ستّةٌ في المجال المختوم، وستّةٌ خارجه تُذرَّر بالجسر "
            "وتُرفض من البوّابة بالاسم)؛ اكتمالُها على MASAQ قياسٌ لم يُطبع بعد."),
    _c("AQ-lattice", "الاحتواءُ بين الأقانيم انعكاسيٌّ متعدٍّ، والسلامةُ تنزل من الأعلى إلى الأدنى", _P,
       "lean:Slge.Categories.sub_trans"),
    # — المدخل الوحيد —
    _c("ENTRY", "لا يدخل العمودَ إلّا شهادةُ بوّابة الغانم ذرّاتٍ، وتعود ذرّاتٍ بعينها", _X,
       "test:tests/test_entry.py::test_kitabun_enters_as_five_cells_and_exits_byte_for_byte",
       "test:tests/test_entry.py::test_every_cell_round_trips",
       "test:tests/test_entry.py::test_non_atoms_are_refused_by_name",
       note="الجسرُ ذرّة ← خانة هو `Slge.ofCell/toCell` المبرهَن؛ والذرّاتُ نفسُها من `gate.enter` "
            "في الغانم (A116-CANONICAL-TXT-1.1) لا من قارئٍ هنا."),
    _c("GUARD", "لا قارئَ للنصّ ولا كاتبَ له في الشجرة خارج `suspended/`", _X,
       "test:tests/test_guard.py::test_no_breach_in_the_tree",
       "test:tests/test_guard.py::test_a_planted_reader_is_caught",
       "test:tests/test_guard.py::test_suspended_is_not_importable"),
    # — الخانة والترخيص والعدّ —
    _c("Q1", "الخاناتُ ‎116 = 29 × 4‎، تامّةٌ بلا تكرار", _P,
       "lean:Slge.scells_length", "test:tests/test_cells.py::test_cells_are_116"),
    _c("Q2", "الترخيصُ قيدُ مسار، وهو `Admissible` في الـ116 بعينه لكلّ طول", _P,
       "lean:Slge.licensed_iff", "test:tests/test_conformance.py::test_folds_match_lean"),
    _c("BRIDGE", "الجسرُ بين ترميز SLGE وترميز الـ116 تقابلٌ يحفظ السكون", _P,
       "lean:Slge.ofCell_toCell", "lean:Slge.toCell_ofCell", "lean:Slge.toCell_isSukun",
       "test:tests/test_conformance.py::test_bridge_matches_lean"),
    _c("COUNT", "عدّادُ SLGE هو ‎U(n)‎ لكلّ n", _P,
       "lean:Slge.count_eq_U", "test:tests/test_conformance.py::test_counts_match_lean"),
    _c("FOLD", "الطيُّ تقابلٌ بين المرخَّصات بطول n و‎{0…U(n)−1}‎", _P,
       "lean:Slge.slgeFold_injective", "lean:Slge.slgeFold_surjective",
       "test:tests/test_conformance.py::test_folds_match_lean",
       note="يحلّ محلّ Q23/Q23b في الأصل: كان الفحصُ هناك طيًّا موضعيًّا بأساس 116، "
            "وصحّتُه بالبناء لا بالعدّ؛ وهنا طيٌّ كثيفٌ مبرهَنٌ لكلّ طول."),
    _c("Q22", "الاستنتاجُ المعكوس: ‎U(1) = 87‎ و29 حاملًا ⇒ 3 متحرّكات ⇒ ‎116‎", _X,
       "test:tests/test_cells.py::test_inventory_is_derived_from_U1"),
    _c("Q24", "الظلُّ M/S يعجز والطيُّ يفرّق (ذَيْن/ذِين)", _X,
       "test:tests/test_cells.py::test_shadow_fails_fold_separates"),
    _c("Q3", "استواءُ البدال: تبديلُ حاملين في الجذر يتبدّل في المولَّد", _X,
       "suspended:tests/test_morphology.py::test_equivariance_all_transpositions",
       note="الأصلُ فحص 40 تبديلًا بعيّنة؛ هنا كلُّ تبديلٍ داخل كلّ صنفٍ على كلّ قالب."),
    _c("Q4", "الإعرابُ إسقاطٌ على الخانة الأخيرة يحفظ الترخيص", _X,
       "suspended:tests/test_morphology.py::test_iirab_touches_only_last_cell"),
    _c("Q5", "المثاليُّ المحظور (ألفٌ متحرّكة) لا يقع في أيّ ثابتٍ أو زائد", _X,
       "suspended:tests/test_morphology.py::test_no_forbidden_cell_in_any_table",
       note="كان الأصلُ يفحص PREFIX/SUFFIX ولا يفحص OPS، ففي OPS أربعةُ صفوفٍ تنقضه؛ صُحّحت."),
    _c("Q6", "إغلاقُ العمليّات في الـ116", _X,
       "suspended:tests/test_morphology.py::test_tables_are_closed_in_116"),
    _c("Q11", "الإملاء: ما كُتب يُقرأ بعينه، ‎read (write w) = w‎، لكلّ سلسلة", _P,
       "lean:Slge.Rasm.read_write", "lean:Slge.Rasm.write_injective",
       "suspended:tests/test_rasm_conformance.py::test_rasm_matches_lean",
       "suspended:tests/test_orthography.py::test_roundtrip_exhaustive_upto_2",
       "suspended:tests/test_orthography.py::test_roundtrip_exhaustive_3",
       note="الأصلُ فحص 7 عيّنات؛ وعلى المرخَّصات بطول ≤ 2 كان يخطئ في 31 ويسقط في 87 "
            "(«فِي» تعود ألفًا؛ والهمزةُ الساكنة KeyError). والمبرهَنُ قواعدُ الكاتب الخمسُ "
            "المعلنة على رموزٍ مجرّدة؛ ومطابقتُها بيونيكود البايثون على كلّ سلسلةٍ بطول ≤ 2."),
    _c("Q12", "الابتداء: المطلعُ متحرّك، وهمزةُ الوصل همزةٌ لا ألف", _X,
       "suspended:tests/test_orthography.py::test_begin_respects_rho"),
    _c("Q12-wasl", "حركةُ همزة الوصل في غير «ال» (كسرٌ أو ضمّ)", _O,
       note="الأصلُ يفتحها دائمًا؛ تُرك كما هو حتى يشهد نصٌّ مودَع."),
    _c("Q13", "الوصل: همزةُ الوصل تسقط، والشمسيُّ يُدغم، والوصلةُ ليست ساكنين", _S,
       "suspended:tests/test_orthography.py::test_join_bismillah"),
    _c("Q14", "الوقف: الختامُ ساكن، والتنوينُ يُحذف", _S,
       "suspended:tests/test_orthography.py::test_pause_tanwin"),
    _c("Q14-nun", "الوقفُ على «يَفْعَلُونَ» يحذف الواوَ والنونَ معًا", _O,
       note="هذا سلوكُ الأصل وتفحصه Q14 هناك؛ ولم يُشهد له بنصّ. يحتاج شاهدًا من قراءةٍ مودَعة."),
    _c("Q15", "التطبيعُ متساوي الأثر", _X,
       "suspended:tests/test_encoding.py::test_normalize_idempotent_on_every_char"),
    _c("Q16", "كاشفُ التعارض يلتقط كلَّ بديلٍ معلن", _X,
       "suspended:tests/test_encoding.py::test_conflicts_catch_every_substitution"),
    _c("Q17", "ملفّاتُ المحرّك خاليةٌ من محارفَ خارج الجدول", _X,
       "suspended:tests/test_encoding.py::test_sources_are_clean"),
    _c("Q18", "كلُّ حرفٍ متّجهُ صفاتٍ تامّ", _X,
       "test:tests/test_phonology.py::test_every_letter_has_a_full_vector"),
    _c("Q19", "كلُّ زوجٍ من الأزواج يقسم الـ29", _D,
       "test:tests/test_phonology.py::test_pairs_partition",
       note="صادقٌ بالبناء (السالبُ متمّمُ الموجب)؛ فهو تعريفٌ لا اكتشاف."),
    _c("Q20", "الجوفُ للمدّ الثلاث", _D, "test:tests/test_phonology.py::test_jawf_is_madd"),
    _c("PHON-open", "«ذ، ث» على «اللسان/عام»، و«ي» في الجوف وحده", _O,
       note="بياناتٌ تراثيّةٌ ناقصة كما أُعلنت؛ لم تُكمَّل من الذاكرة."),
    _c("Q21", "عمودُ الطبقات بلا دورة، ولا تُبنى طبقةٌ قبل شرطها", _X,
       "test:tests/test_order.py::test_spine_is_acyclic",
       "test:tests/test_order.py::test_no_leap"),
    _c("Q21-code", "الشيفرةُ نفسُها لا تقفز: لا تستورد وحدةٌ وحدةَ طبقةٍ ليست من شروطها", _X,
       "test:tests/test_order.py::test_modules_import_only_their_prerequisites"),
    _c("L3-L4", "الأدواتُ والمبنيّات: ذرّاتُها مشتقّةٌ من رسمها، ومرخَّصة", _X,
       "suspended:tests/test_lexicon.py::test_every_entry_is_licensed",
       note="في الأصل اختلف الرسمُ والذرّاتُ في عشرة مداخل؛ والمصدرُ الآن واحد."),
    _c("L1-rho", "سلّمُ الحروف: الألفُ وحدها لا تتحرّك", _X,
       "suspended:tests/test_morphology.py::test_every_used_cell_respects_rho",
       note="الأصلُ (`LADDER`) منع الحركةَ على الواو والياء أيضًا، فناقض «وَ» و«يَ» في جداوله."),
    # — الدلالة —
    _c("DL1-DL6", "أقسامُ الوضع والدلالة والحقيقة والمجاز والمنطوق والمفهوم مغلقة", _D,
       "test:tests/test_semantics.py::test_partitions_are_closed"),
    _c("DL4", "كشفُ النسب بالكلمات المفتاحيّة", _O,
       note="حُذف `nisba_ok`: البحثُ عن «فاعل» في نصٍّ ليس كشفًا للإسناد. يُبنى في طبقة النظم."),
    # — المعرفة —
    _c("GHAZALI", "جدولُ الصور المنتجة هو جدولُ الغزالي بعينه، محسوبًا بالبتّات", _P,
       "lean:Slge.Ghazali.ghazali_table",
       "test:tests/test_conformance.py::test_ghazali_matches_lean"),
    _c("BARREN", "عقمُ نقيض المقدَّم وعين التالي في الأخصّ مشهودٌ بنموذجين", _P,
       "lean:Slge.Ghazali.barren_witnessed"),
    _c("CHAIN", "الأخصُّ متعدٍّ (مفهومُ الموافقة سلسلة)", _P, "lean:Slge.Ghazali.akhass_chain"),
    _c("LICENCE", "الرافعُ إلى المساواة يُنتج مفهومَ المخالفة", _P,
       "lean:Slge.Ghazali.licence_makes_mafhum"),
    _c("INFER", "`infer` لا يُنتج إلّا بمقبولٍ وبصورةٍ منتجة", _X,
       "test:tests/test_knowledge.py::test_candidates_never_produce",
       "test:tests/test_knowledge.py::test_every_produced_step_is_productive"),
    _c("MAFHUM-open", "طريقُ مخالفة الغاية ومخالفة العدد إلى صورة", _O,
       note="`knowledge.MAFHUM_ROUTE` يكتب الموافقةَ ومخالفتي الصفة والشرط وحدها."),
    # — رتبة الجواب —
    _c("RANK-MEET", "رتبةُ النتيجة رتبةُ أضعف مقدّماتها؛ لا ترقية", _P,
       "lean:Slge.Rank.pathGrade_qati_iff", "lean:Slge.Rank.no_promotion",
       "test:tests/test_rank.py::test_rank_never_promotes_on_random_worlds",
       note="الغزالي، محكّ النظر: «يقينية ضرورية بحسب ذوق المقدمات»."),
    _c("RANK-WEIGH", "القطعيُّ يردّ الظنّيّ، ولا يُردّ قطعيّ، والراجحُ مرجوحٌ من الجهة الأخرى، "
       "والتعادلُ ظنّيّان متساويان، وتعارضُ قطعيّين تناقض", _P,
       "lean:Slge.Rank.weigh_swap", "lean:Slge.Rank.qati_never_loses",
       "lean:Slge.Rank.mardud_iff", "lean:Slge.Rank.tanaqud_iff", "lean:Slge.Rank.taadul_iff",
       "test:tests/test_rank.py::test_rank_table_matches_lean",
       note="التفكير: «يؤخذ القطعي ويرد الظني»؛ ج٣ ¶1060، ¶1062."),
    _c("RANK-KHASS", "الخاصُّ يُعمل به أيًّا كان ثبوتُه، والعامُّ مخصوصٌ لا مردود", _P,
       "lean:Slge.Rank.specific_wins", "lean:Slge.Rank.general_is_makhsus",
       "lean:Slge.Rank.qati_general_yields_to_zanni_specific",
       "lean:Slge.Rank.same_scope_is_weigh",
       "test:tests/test_rank.py::test_specific_wins_and_general_is_makhsus",
       note="ج٣ ¶1065. والخصوصُ محسوبٌ من لزوم المقدَّمين بالقواعد المقبولة."),
    _c("RANK-THUBUT", "تصنيفُ الدليل قطعيًّا أو ظنّيًّا", Status.معلن,
       "test:tests/test_rank.py::test_evidence_grades",
       note="المتواترُ والتعريفُ قطعيّان؛ الآحادُ والمشهورُ والمعجمُ والمشاهدةُ (حكمٌ على صفة) "
            "ظنّيّة — ج٣ ¶275، ¶277، ¶713؛ التفكير. قاعدةٌ معلنةٌ لا مبرهنة."),
    _c("RANK-open", "مرجّحاتُ الحكم (التحريمُ على الإباحة …) والجمعُ «من وجه دون وجه»", _O,
       note="ج٣ ¶1063، ¶1066–1074: يحتاجان نوعَ الحكم ونطاقَه في القاعدة؛ وتعارضُ ظنّيّين "
            "في نطاقٍ واحدٍ يوزن الآن بعدد الشواهد المستقلّة وحده."),
    # — التعلّم —
    _c("LEARN", "حلقةُ التعلّم: المرشَّحُ لا يُنتج، والمحجوبُ لا يراه المولِّد، "
       "والخاطئُ يُسحب، والسجلُّ تامّ", _X,
       "test:tests/test_learning.py::test_held_out_is_never_shown",
       "test:tests/test_learning.py::test_wrong_admission_is_retracted",
       "test:tests/test_learning.py::test_every_proposal_has_one_verdict"),
    # — الجواب —
    _c("ANSWER", "كلُّ جملةٍ في الجواب لها وسمٌ وسند، والمُعيدُ لا يُسقطهما", _X,
       "test:tests/test_answer.py::test_every_sentence_is_tagged",
       "test:tests/test_answer.py::test_verbalizer_cannot_drop_tags"),
    # — ما بقي مفتوحًا من الصرف —
    _c("GRID-wasl", "همزةُ الأوزان VII–X مكتوبةٌ ‎(ء، فتح)‎ في الشبكة", _O,
       note="يُفحص على `sibawayh-abniya.tsv` في الغانم قبل أيّ تغيير."),
    _c("GRID-NOM-labels", "قالبا MS-7 وNS-1 يخالفان رسمَ اسميهما", _O,
       "suspended:tests/test_morphology.py::test_nominal_templates_against_their_own_labels",
       note="MS-7: لامٌ ثابتٌ ساكن والرسمُ «لَ» جذريّ؛ NS-1: فاءٌ مفتوحةٌ والرسمُ «فْ». "
            "كشفهما الفحصُ الآليّ للقالب برسم اسمه؛ والحسمُ لصاحب الجرد."),
    _c("WAZUN", "استخراجُ الأوزان من نشرةٍ مشكولةٍ لأبواب سيبويه", _O,
       note="الأصلُ (`slge_wazun`) يستدعي `slge_laws.normalize` غيرَ الموجودة؛ والنشرةُ "
            "المجرّدةُ مودعةٌ في الغانم (`corpora/sibawayh-abniya.tsv`) بلا تشكيل."),
)


def _suspend(claims: tuple[Claim, ...]) -> tuple[Claim, ...]:
    """دعوى سندُها في `suspended/` تُوسَم معلَّقةً مهما كان وسمُها المعلَن: لا يُشهَد بما لا يجري.

    البرهانُ في Lean (إن وُجد) باقٍ بعينه، لكنّ المرآةَ البايثونيّةَ التي كانت تُفحَص معلَّقةٌ
    حتى تعود عبر بوّابة الغانم؛ فالوسمُ وسمُ الطريق كلِّه لا أقوى حلقةٍ فيه.
    """

    out: list[Claim] = []
    for c in claims:
        if any(s.startswith("suspended:") for s in c.support):
            note = ("معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ "
                    f"الوسمُ المعلَن قبل التعليق: {c.status.name}")
            full = (c.note + " " if c.note else "") + note
            out.append(Claim(c.claim_id, c.statement, Status.معلق, c.support, full))
        else:
            out.append(c)
    return tuple(out)


LEDGER: Final[tuple[Claim, ...]] = _suspend(_DECLARED)
"""السجلّ."""
