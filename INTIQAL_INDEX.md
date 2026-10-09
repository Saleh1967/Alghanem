# فهرسُ الانتقالات — لا انتقالَ على الـ116 إلّا مسجَّلًا باسمه ومبرهنته

مولَّدٌ بـ`python tools/gen_intiqal_index.py` من `slge.intiqal.REGISTRY`؛ لا يُحرَّر باليد. الحارسُ يمشي على `src/slge` فيرفض دالّةَ انتقالٍ عامّةً (‎Word → Word‎) غيرَ مسجَّلة، وصفًّا بلا دالّة، ومبرهنةً غيرَ مدقَّقة في `Audit.lean`، ودَينًا بلا ملاحظة. السجلُّ **مفحوصٌ** لا مبرهَن: Lean (`IntiqalTable`) يحمل الأسماءَ لا الدوالَّ، والإغلاقُ حيث ذُكر مبرهنةٌ باسمها.

87 انتقالًا: إغلاقٌ 32، خاصّةٌ 35، دَينٌ باسمه 20.

| الوحدة | الدالّة | المبرهنة | النوع | ملاحظة |
|---|---|---|---|---|
| `adad` | `masc` | `Slge.Adad.genderOf_masc` | خاصّة |  |
| `adad` | `fem` | `Slge.Adad.genderOf_fem_forms` | خاصّة |  |
| `adad` | `compound` | `Slge.Adad.compound_both_fatha` | خاصّة |  |
| `adad` | `uqud` | `Slge.Adad.uqud_case` | خاصّة |  |
| `adawat` | `apply` | `Slge.Adawat.apply_licensed` | إغلاق |  |
| `damair` | `attach` | `Slge.Damair.attach_licensed` | إغلاق |  |
| `fil` | `qalb` | `Slge.Fil.qalb_licensed` | إغلاق |  |
| `fil` | `naql` | `Slge.Fil.naql_licensed` | إغلاق |  |
| `fil` | `ibdal` | `Slge.Fil.ibdal_licensed` | إغلاق |  |
| `fil` | `idgham` | `Slge.Fil.idgham_licensed` | إغلاق |  |
| `filiyya` | `past` | `Slge.Filiyya.past_licensed` | إغلاق |  |
| `filiyya` | `fail` | `Slge.Filiyya.fail_reads_raf` | خاصّة |  |
| `filiyya` | `majhul` | `Slge.Filiyya.majhul_fill` | خاصّة |  |
| `filiyya` | `majhul_pres` | — | — | مضارعُ المجهول بلا مبرهنة؛ يُبرهَن مع المبنيّ للمجهول قارئًا |
| `filiyya` | `naib` | `Slge.Filiyya.naib_eq_fail` | خاصّة |  |
| `filiyya` | `maful` | `Slge.Filiyya.maful_reads_nasb` | خاصّة |  |
| `filiyya` | `maiyya` | `Slge.Filiyya.maiyya_licensed` | إغلاق |  |
| `ilal` | `restore` | `Slge.Ilal.apply_roundtrip` | إغلاق |  |
| `ishara` | `tanbih` | `Slge.Ishara.tanbih_licensed` | إغلاق |  |
| `ishara` | `bud` | `Slge.Ishara.bud_licensed` | إغلاق |  |
| `ishara` | `dual` | `Slge.Ishara.caseOf_dual` | خاصّة |  |
| `ism` | `nisba` | `Slge.Ism.nisba_licensed` | إغلاق |  |
| `ism` | `prepare` | — | — | تهيئةُ الاسم للنسبة (حذفُ التاء والألف) بلا مبرهنة |
| `istifham` | `idgham_nm` | `Slge.Istifham.idghamNM_length` | خاصّة |  |
| `istifham` | `ma_after_jarr` | `Slge.Istifham.ma_after_jarr` | خاصّة |  |
| `jazm` | `sukun` | `Slge.Jazm.sukun_licensed` | إغلاق |  |
| `jazm` | `drop_weak` | `Slge.Jazm.dropWeak_licensed` | إغلاق |  |
| `jazm` | `amr` | `Slge.Jazm.amr_licensed` | إغلاق |  |
| `jidh` | `stem_form` | `Slge.Jidh.stemSenses_eq_stemForm` | خاصّة |  |
| `jumla` | `lam` | `Slge.Jumla.lam_licensed` | إغلاق |  |
| `jumla` | `ta_nith` | `Slge.Jumla.gender_taNith` | خاصّة |  |
| `jumla` | `dual` | — | — | المثنّى في الجملة الاسميّة بلا مبرهنةٍ باسمه (الحالةُ في `Tawabi`) |
| `jumla` | `jam_m` | — | — | جمعُ المذكّر السالم بلا مبرهنةٍ باسمه (الحالةُ في `Tawabi`) |
| `jumla` | `jam_f` | `Slge.Jumla.gender_jamF` | خاصّة |  |
| `jumla` | `bare` | — | — | تجريدُ الكلمة من أل والتنوين بلا مبرهنة |
| `majrurat` | `jarr` | `Slge.Majrurat.jarr_licensed` | إغلاق |  |
| `majrurat` | `jarr_nakira` | — | — | جرُّ النكرة بالتنوين بلا مبرهنةٍ باسمه |
| `majrurat` | `dual` | `Slge.Majrurat.dual_jarr_compatible` | خاصّة |  |
| `majrurat` | `mudaf` | `Slge.Majrurat.mudaf_no_tanwin` | خاصّة |  |
| `majrurat` | `mudaf_uqud` | — | — | إضافةُ العقود بلا مبرهنة |
| `majrurat` | `mudaf_dual` | — | — | إضافةُ المثنّى (حذفُ النون) بلا مبرهنةٍ باسمه |
| `mansubat` | `raf` | — | — | رفعُ الاسم في بقيّة المنصوبات بلا مبرهنةٍ باسمه (`Nawasikh.raf_licensed` نظيرُه) |
| `mansubat` | `nasb` | `Slge.Mansubat.nakira_reads_nasb` | خاصّة |  |
| `mansubat` | `nakira_mansuba` | — | — | النكرةُ المنصوبة بالتنوين بلا مبرهنةٍ باسمه |
| `mansubat` | `strip_suffix` | — | — | نزعُ لاحقة الضمير بلا مبرهنة (`Jidh.peelSuffix_sound` نظيرُه) |
| `mansubat` | `fakk` | — | — | فكُّ الإدغام في التوكيد بلا مبرهنة |
| `mansubat` | `mustathna` | — | — | المستثنى بلا مبرهنةٍ باسمه |
| `mansubat` | `ghayr_of` | — | — | غيرُ وسوى بلا مبرهنة |
| `mansubat` | `after_khala` | `Slge.Mansubat.ma_khala_nasb` | خاصّة |  |
| `maqam` | `with_prefix` | `Slge.Maqam.withPrefix_fill` | خاصّة |  |
| `marifa` | `shamsi` | `Slge.Marifa.shamsi_licensed` | إغلاق |  |
| `marifa` | `al` | `Slge.Marifa.al_licensed` | إغلاق |  |
| `marifa` | `drop_tanwin` | `Slge.Marifa.dropTanwin_licensed` | إغلاق |  |
| `marifa` | `idafa` | `Slge.Marifa.idafa_no_tanwin` | خاصّة |  |
| `naat` | `naat` | `Slge.Naat.naatOk_agree` | خاصّة |  |
| `nawasikh` | `raf` | `Slge.Nawasikh.raf_licensed` | إغلاق |  |
| `nawasikh` | `nasb` | `Slge.Nawasikh.nasb_licensed` | إغلاق |  |
| `nawasikh` | `tanwin` | `Slge.Nawasikh.no_tanwin_setLast` | خاصّة |  |
| `nawasikh` | `kaffa` | `Slge.Nawasikh.kaffa_licensed` | إغلاق |  |
| `nida` | `ya_junction` | `Slge.Nida.ya_junction` | خاصّة |  |
| `nida` | `nudba` | `Slge.Nida.nudba_not_binary_licensed` | إغلاق |  |
| `nisab` | `isnad` | `Slge.Nisab.isnad_one_operation` | خاصّة |  |
| `sarf` | `sarf_jarr` | `Slge.Sarf.sarf_jarr_ne_nasb` | خاصّة |  |
| `sarf` | `sarf_nasb` | — | — | نصبُ المنصرف بلا مبرهنةٍ باسمه |
| `sarf` | `mamnu_jarr` | `Slge.Alam.mamnu_jarr_is_fatha` | خاصّة |  |
| `sarf` | `al_jarr` | `Slge.Sarf.al_jarr_kasra` | خاصّة |  |
| `sarf` | `idafa_jarr` | `Slge.Sarf.idafa_jarr_kasra` | خاصّة |  |
| `sawabiq` | `lift` | `Slge.Sawabiq.joined_is_initial` | خاصّة |  |
| `shibh` | `jarr_majrur` | `Slge.Shibh.jarr_majrur_licensed` | إغلاق |  |
| `shibh` | `zarf` | — | — | الظرفُ شبهَ جملة بلا مبرهنةٍ باسمه |
| `talab` | `lam_amr` | `Slge.Talab.lam_amr_licensed` | إغلاق |  |
| `talab` | `lam_amr_after_waw` | `Slge.Sawabiq.sakin_is_kasra` | خاصّة |  |
| `talab` | `masdar_amr` | — | — | المصدرُ النائبُ عن الأمر بلا مبرهنة |
| `talil` | `maful_li_ajlih` | — | — | المفعولُ لأجله بلا مبرهنةٍ باسمه |
| `talil` | `apply` | — | — | تطبيقُ التعليل بلا مبرهنة |
| `tawabi` | `tawkid` | `Slge.Tawabi.tawkid_words_licensed` | إغلاق |  |
| `tawzi` | `alif_to_ya` | — | — | الألفُ ياءً قبل الضمير بلا مبرهنةٍ باسمه (`tawzi_restores` يردّه) |
| `wasl` | `drop_wasl` | `Slge.Wasl.wasl_drops` | إغلاق |  |
| `wasl` | `istifham_verb` | `Slge.Wasl.istifhamVerb_licensed` | إغلاق |  |
| `zaman` | `raf_tanwin` | `Slge.Zaman.hukm_rafTanwin` | خاصّة |  |
| `zaman` | `nasb_tanwin` | `Slge.Zaman.hukm_nasbTanwin` | خاصّة |  |
| `zawaid` | `tawkid` | `Slge.Zawaid.tawkid_licensed` | إغلاق |  |
| `zawaid` | `anith` | `Slge.Zawaid.anith_licensed` | إغلاق |  |
| `zuruf` | `set_last` | `Slge.Zuruf.setLast_licensed` | إغلاق |  |
| `zuruf` | `mudaf` | `Slge.Zuruf.hukm_mudaf` | خاصّة |  |
| `zuruf` | `jarr` | `Slge.Zuruf.hukm_jarr` | خاصّة |  |
| `zuruf` | `qat` | `Slge.Zuruf.hukm_qat` | خاصّة |  |

## ما ليس هنا — باسمه

- الديونُ أعلاه انتقالاتٌ بلا مبرهنةٍ باسمها؛ لا تُحذف الدالّةُ ولا تُزاد مبرهنةٌ من الذاكرة؛ تُبرهَن واحدةً واحدة أو تُعلَّق.
- «خاصّة» ليست إغلاقًا: تُثبت حالةً أو علامةً لا حفظَ الترخيص؛ ترقيتُها إلى إغلاقٍ مبرهنةٌ جديدة.
- الدوالُّ التي تنقل خاناتٍ عبر أنواعٍ وسيطة (قراءاتٌ، سجلّاتٌ) خارج هذا الحصر؛ حصرُها بالنوع الوسيط خطوةٌ لاحقة.
