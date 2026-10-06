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
    _c("WAZN-table", "113 وزنًا مودَعًا سليمةٌ ومرخَّصةٌ لكلّ أصل؛ بايثونُها مطابقٌ لجدول Lean", _P,
       "lean:Slge.Wazn.awzan_wf", "lean:Slge.Wazn.awzan_licensed",
       "test:tests/test_conformance.py::test_wazn_matches_lean"),
    _c("WAZN-sibawayh",
       "هياكلُ الأوزان مقابل أبنية سيبويه المجمَّدة: 95/113 عنده؛ 18 مسمّاة؛ 122 من هياكله خارج الجدول",
       _S,
       "test:tests/test_wazn.py::test_skeletons_measured_against_sibawayh",
       note="الحركاتُ معلَنةٌ من كتب الصرف لا مقيسة؛ الرباعيُّ والإعلالُ والمفعولُ المطلق والجامدُ "
            "خارج الجدول باسمها (DEBTS)."),
    _c("WAZN-awzan", "أوزانُ الفعل والمصدر والمشتقّات والتأنيث والجموع كما في كتب الصرف", _D,
       "test:tests/test_wazn.py::test_masdar_of_mazid_is_a_declared_pair_of_deposited_awzan"),
    # — شبكةُ الأوزان: الترخيصُ الجبريُّ التدريجيُّ من المصدر —
    _c("SHABAKA-wf", "إدخالٌ وحذفٌ (بشرط بقاء الأصل) وتغييرُ حالة: كلُّ تتابعٍ يحفظ استردادَ الأصل", _P,
       "lean:Slge.Shabaka.wf_step", "lean:Slge.Shabaka.wf_run",
       "test:tests/test_shabaka.py::test_every_edit_keeps_the_root_recoverable"),
    _c("SHABAKA-edges",
       "112 حافّةً من المصدر المجرّد: الابنُ = الأبُ بعد عمليّاته، وكلُّ وزنٍ يبلغ الجذر", _P,
       "lean:Slge.Shabaka.edges_apply", "lean:Slge.Shabaka.network_rooted",
       "lean:Slge.Shabaka.run_edge_wf",
       "test:tests/test_conformance.py::test_shabaka_matches_lean"),
    _c("SHABAKA-classical",
       "ترتيبُ البصريّين: المصدرُ أصلُ المشتقّات؛ الماضي فالمضارع فالأمر؛ المزيدُ من المجرّد", _D,
       "test:tests/test_shabaka.py::test_classical_edges_are_machine_checked_and_rooted"),
    _c("SHABAKA-minimal",
       "ترتيبُ البصريّين ليس أقلَّ الأشجار كلفةً: 341 عمليّةً مقابل 155؛ يتّفقان في 21 أبًا من 112",
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
    _c("RAWABIT-cells", "70 أداةً مفردة خاناتُها مرخَّصة؛ 36 منها من شهادات البوّابة بعينها", _P,
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
