# سجلُّ الدعاوى

مولَّدٌ من `src/slge/status.py` بـ`python tools/gen_status.py`؛ لا يُحرَّر باليد.

| الوسم | العدد |
|---|---|
| مبرهن | 18 |
| مفحوص_استقصاء | 11 |
| مفحوص_بعينة | 0 |
| دليل | 0 |
| معلن | 5 |
| رأي | 0 |
| مفتوح | 8 |
| معلق | 14 |

| المعرّف | الدعوى | الوسم | السند | ملاحظة |
|---|---|---|---|---|
| AQ-lattice | الاحتواءُ بين الأقانيم انعكاسيٌّ متعدٍّ، والسلامةُ تنزل من الأعلى إلى الأدنى | مبرهن | `lean:Slge.Categories.sub_trans` |  |
| AQ-pronoun | الضمائرُ المنفصلة أقنومٌ سليم (كلُّها مرخَّصة) بأعدادٍ متباينة، وشكلُها ليس بصمة | مبرهن | `lean:Slge.Categories.pronoun_sound`<br>`lean:Slge.Categories.pronoun_numbers_nodup`<br>`test:tests/test_conformance.py::test_categories_match_lean` | خاناتُها من شهادات بوّابة الغانم؛ اكتمالُها على MASAQ قياسٌ لم يُطبع بعد. |
| BARREN | عقمُ نقيض المقدَّم وعين التالي في الأخصّ مشهودٌ بنموذجين | مبرهن | `lean:Slge.Ghazali.barren_witnessed` |  |
| BRIDGE | الجسرُ بين ترميز SLGE وترميز الـ116 تقابلٌ يحفظ السكون | مبرهن | `lean:Slge.ofCell_toCell`<br>`lean:Slge.toCell_ofCell`<br>`lean:Slge.toCell_isSukun`<br>`test:tests/test_conformance.py::test_bridge_matches_lean` |  |
| CHAIN | الأخصُّ متعدٍّ (مفهومُ الموافقة سلسلة) | مبرهن | `lean:Slge.Ghazali.akhass_chain` |  |
| COUNT | عدّادُ SLGE هو ‎U(n)‎ لكلّ n | مبرهن | `lean:Slge.count_eq_U`<br>`test:tests/test_conformance.py::test_counts_match_lean` |  |
| FOLD | الطيُّ تقابلٌ بين المرخَّصات بطول n و‎{0…U(n)−1}‎ | مبرهن | `lean:Slge.slgeFold_injective`<br>`lean:Slge.slgeFold_surjective`<br>`test:tests/test_conformance.py::test_folds_match_lean` | يحلّ محلّ Q23/Q23b في الأصل: كان الفحصُ هناك طيًّا موضعيًّا بأساس 116، وصحّتُه بالبناء لا بالعدّ؛ وهنا طيٌّ كثيفٌ مبرهَنٌ لكلّ طول. |
| GHAZALI | جدولُ الصور المنتجة هو جدولُ الغزالي بعينه، محسوبًا بالبتّات | مبرهن | `lean:Slge.Ghazali.ghazali_table`<br>`test:tests/test_conformance.py::test_ghazali_matches_lean` |  |
| LICENCE | الرافعُ إلى المساواة يُنتج مفهومَ المخالفة | مبرهن | `lean:Slge.Ghazali.licence_makes_mafhum` |  |
| NUM-agree | عددُ الشهادة (ترقيم الذرّات) وعددُ الطيّ متكافئان على المرخَّصات بطولٍ واحد | مبرهن | `lean:Slge.Consistency.numbers_agree`<br>`lean:Slge.Consistency.atomNumber_determines_fold`<br>`lean:Slge.Consistency.fold_determines_atomNumber` |  |
| Q1 | الخاناتُ ‎116 = 29 × 4‎، تامّةٌ بلا تكرار | مبرهن | `lean:Slge.scells_length`<br>`test:tests/test_cells.py::test_cells_are_116` |  |
| Q2 | الترخيصُ قيدُ مسار، وهو `Admissible` في الـ116 بعينه لكلّ طول | مبرهن | `lean:Slge.licensed_iff`<br>`test:tests/test_conformance.py::test_folds_match_lean` |  |
| RANK-KHASS | الخاصُّ يُعمل به أيًّا كان ثبوتُه، والعامُّ مخصوصٌ لا مردود | مبرهن | `lean:Slge.Rank.specific_wins`<br>`lean:Slge.Rank.general_is_makhsus`<br>`lean:Slge.Rank.qati_general_yields_to_zanni_specific`<br>`lean:Slge.Rank.same_scope_is_weigh`<br>`test:tests/test_rank.py::test_specific_wins_and_general_is_makhsus` | ج٣ ¶1065. والخصوصُ محسوبٌ من لزوم المقدَّمين بالقواعد المقبولة. |
| RANK-MEET | رتبةُ النتيجة رتبةُ أضعف مقدّماتها؛ لا ترقية | مبرهن | `lean:Slge.Rank.pathGrade_qati_iff`<br>`lean:Slge.Rank.no_promotion`<br>`test:tests/test_rank.py::test_rank_never_promotes_on_random_worlds` | الغزالي، محكّ النظر: «يقينية ضرورية بحسب ذوق المقدمات». |
| RANK-WEIGH | القطعيُّ يردّ الظنّيّ، ولا يُردّ قطعيّ، والراجحُ مرجوحٌ من الجهة الأخرى، والتعادلُ ظنّيّان متساويان، وتعارضُ قطعيّين تناقض | مبرهن | `lean:Slge.Rank.weigh_swap`<br>`lean:Slge.Rank.qati_never_loses`<br>`lean:Slge.Rank.mardud_iff`<br>`lean:Slge.Rank.tanaqud_iff`<br>`lean:Slge.Rank.taadul_iff`<br>`test:tests/test_rank.py::test_rank_table_matches_lean` | التفكير: «يؤخذ القطعي ويرد الظني»؛ ج٣ ¶1060، ¶1062. |
| SEQ-delim | ترميزُ الكلمة ذاتيُّ الحدّ: تُقرأ من رأس أيّ تيارٍ ويبقى ما بعدها بعينه | مبرهن | `lean:Slge.Sequence.decodeWord_encodeWord`<br>`lean:Slge.Sequence.encodeWord_prefix_free`<br>`test:tests/test_conformance.py::test_sequence_matches_lean`<br>`test:tests/test_cells.py::test_stream_refuses_unlicensed_and_is_prefix_free` |  |
| SEQ-recover | فكُّ طيِّ المرخَّصة يعيدها بعينها | مبرهن | `lean:Slge.Sequence.slgeUnfold_slgeFold` |  |
| SEQ-stream | تيارُ كلماتٍ مرخَّصةٍ يُفكّ كلُّه بترتيبه بلا فاصلٍ ولا حاملٍ زائد | مبرهن | `lean:Slge.Sequence.decode_encode`<br>`lean:Slge.Sequence.U_lt_two_pow_width` | الكلفةُ معلنة: cost(k) = (k+1) + ⌊log₂U(k)⌋+1 بتًّا؛ k=1: 9، k=2: 17 (من جدول Lean). |
| ANSWER | كلُّ جملةٍ في الجواب لها وسمٌ وسند، والمُعيدُ لا يُسقطهما | مفحوص_استقصاء | `test:tests/test_answer.py::test_every_sentence_is_tagged`<br>`test:tests/test_answer.py::test_verbalizer_cannot_drop_tags` |  |
| ENTRY | لا يدخل العمودَ إلّا شهادةُ بوّابة الغانم ذرّاتٍ، وتعود ذرّاتٍ بعينها | مفحوص_استقصاء | `test:tests/test_entry.py::test_kitabun_enters_as_five_cells_and_exits_byte_for_byte`<br>`test:tests/test_entry.py::test_every_cell_round_trips`<br>`test:tests/test_entry.py::test_non_atoms_are_refused_by_name` | الجسرُ ذرّة ← خانة هو `Slge.ofCell/toCell` المبرهَن؛ والذرّاتُ نفسُها من `gate.enter` في الغانم (A116-CANONICAL-TXT-1.1) لا من قارئٍ هنا. |
| GUARD | لا قارئَ للنصّ ولا كاتبَ له في الشجرة خارج `suspended/` | مفحوص_استقصاء | `test:tests/test_guard.py::test_no_breach_in_the_tree`<br>`test:tests/test_guard.py::test_a_planted_reader_is_caught`<br>`test:tests/test_guard.py::test_suspended_is_not_importable` |  |
| INFER | `infer` لا يُنتج إلّا بمقبولٍ وبصورةٍ منتجة | مفحوص_استقصاء | `test:tests/test_knowledge.py::test_candidates_never_produce`<br>`test:tests/test_knowledge.py::test_every_produced_step_is_productive` |  |
| LEARN | حلقةُ التعلّم: المرشَّحُ لا يُنتج، والمحجوبُ لا يراه المولِّد، والخاطئُ يُسحب، والسجلُّ تامّ | مفحوص_استقصاء | `test:tests/test_learning.py::test_held_out_is_never_shown`<br>`test:tests/test_learning.py::test_wrong_admission_is_retracted`<br>`test:tests/test_learning.py::test_every_proposal_has_one_verdict` |  |
| NAZM-case | توافقُ الإعراب بين كلمتين هو تساوي حالة الخانة الأخيرة | مفحوص_استقصاء | `test:tests/test_nazm.py::test_case_agreement_is_last_cell_state` |  |
| Q18 | كلُّ حرفٍ متّجهُ صفاتٍ تامّ | مفحوص_استقصاء | `test:tests/test_phonology.py::test_every_letter_has_a_full_vector` |  |
| Q21 | عمودُ الطبقات بلا دورة، ولا تُبنى طبقةٌ قبل شرطها | مفحوص_استقصاء | `test:tests/test_order.py::test_spine_is_acyclic`<br>`test:tests/test_order.py::test_no_leap` |  |
| Q21-code | الشيفرةُ نفسُها لا تقفز: لا تستورد وحدةٌ وحدةَ طبقةٍ ليست من شروطها | مفحوص_استقصاء | `test:tests/test_order.py::test_modules_import_only_their_prerequisites` |  |
| Q22 | الاستنتاجُ المعكوس: ‎U(1) = 87‎ و29 حاملًا ⇒ 3 متحرّكات ⇒ ‎116‎ | مفحوص_استقصاء | `test:tests/test_cells.py::test_inventory_is_derived_from_U1` |  |
| Q24 | الظلُّ M/S يعجز والطيُّ يفرّق (ذَيْن/ذِين) | مفحوص_استقصاء | `test:tests/test_cells.py::test_shadow_fails_fold_separates` |  |
| DL1-DL6 | أقسامُ الوضع والدلالة والحقيقة والمجاز والمنطوق والمفهوم مغلقة | معلن | `test:tests/test_semantics.py::test_partitions_are_closed` |  |
| NAZM | ستّةُ أنماط تركيبٍ وثلاثُ علاقاتٍ منقولةٌ من تعقّل جداولَ معلَنة؛ لا قاعدةَ تعمل | معلن | `test:tests/test_nazm.py::test_six_patterns_three_relations_as_in_taaqol` | المصدر sonaiso/taaqol-gpt@91dad10 (formal_shape_composition.py، رتبته هناك مرشَّح). ما له بتٌّ هنا شرطٌ واحد: توافقُ الإعراب (حالةُ الخانة الأخيرة). |
| Q19 | كلُّ زوجٍ من الأزواج يقسم الـ29 | معلن | `test:tests/test_phonology.py::test_pairs_partition` | صادقٌ بالبناء (السالبُ متمّمُ الموجب)؛ فهو تعريفٌ لا اكتشاف. |
| Q20 | الجوفُ للمدّ الثلاث | معلن | `test:tests/test_phonology.py::test_jawf_is_madd` |  |
| RANK-THUBUT | تصنيفُ الدليل قطعيًّا أو ظنّيًّا | معلن | `test:tests/test_rank.py::test_evidence_grades` | المتواترُ والتعريفُ قطعيّان؛ الآحادُ والمشهورُ والمعجمُ والمشاهدةُ (حكمٌ على صفة) ظنّيّة — ج٣ ¶275، ¶277، ¶713؛ التفكير. قاعدةٌ معلنةٌ لا مبرهنة. |
| DL4 | كشفُ النسب بالكلمات المفتاحيّة | مفتوح | — | حُذف `nisba_ok`: البحثُ عن «فاعل» في نصٍّ ليس كشفًا للإسناد. يُبنى في طبقة النظم. |
| GRID-wasl | همزةُ الأوزان VII–X مكتوبةٌ ‎(ء، فتح)‎ في الشبكة | مفتوح | — | يُفحص على `sibawayh-abniya.tsv` في الغانم قبل أيّ تغيير. |
| MAFHUM-open | طريقُ مخالفة الغاية ومخالفة العدد إلى صورة | مفتوح | — | `knowledge.MAFHUM_ROUTE` يكتب الموافقةَ ومخالفتي الصفة والشرط وحدها. |
| PHON-open | «ذ، ث» على «اللسان/عام»، و«ي» في الجوف وحده | مفتوح | — | بياناتٌ تراثيّةٌ ناقصة كما أُعلنت؛ لم تُكمَّل من الذاكرة. |
| Q12-wasl | حركةُ همزة الوصل في غير «ال» (كسرٌ أو ضمّ) | مفتوح | — | الأصلُ يفتحها دائمًا؛ تُرك كما هو حتى يشهد نصٌّ مودَع. |
| Q14-nun | الوقفُ على «يَفْعَلُونَ» يحذف الواوَ والنونَ معًا | مفتوح | — | هذا سلوكُ الأصل وتفحصه Q14 هناك؛ ولم يُشهد له بنصّ. يحتاج شاهدًا من قراءةٍ مودَعة. |
| RANK-open | مرجّحاتُ الحكم (التحريمُ على الإباحة …) والجمعُ «من وجه دون وجه» | مفتوح | — | ج٣ ¶1063، ¶1066–1074: يحتاجان نوعَ الحكم ونطاقَه في القاعدة؛ وتعارضُ ظنّيّين في نطاقٍ واحدٍ يوزن الآن بعدد الشواهد المستقلّة وحده. |
| WAZUN | استخراجُ الأوزان من نشرةٍ مشكولةٍ لأبواب سيبويه | مفتوح | — | الأصلُ (`slge_wazun`) يستدعي `slge_laws.normalize` غيرَ الموجودة؛ والنشرةُ المجرّدةُ مودعةٌ في الغانم (`corpora/sibawayh-abniya.tsv`) بلا تشكيل. |
| GRID-NOM-labels | قالبا MS-7 وNS-1 يخالفان رسمَ اسميهما | معلق | `suspended:tests/test_morphology.py::test_nominal_templates_against_their_own_labels` | MS-7: لامٌ ثابتٌ ساكن والرسمُ «لَ» جذريّ؛ NS-1: فاءٌ مفتوحةٌ والرسمُ «فْ». كشفهما الفحصُ الآليّ للقالب برسم اسمه؛ والحسمُ لصاحب الجرد. معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفتوح |
| L1-rho | سلّمُ الحروف: الألفُ وحدها لا تتحرّك | معلق | `suspended:tests/test_morphology.py::test_every_used_cell_respects_rho` | الأصلُ (`LADDER`) منع الحركةَ على الواو والياء أيضًا، فناقض «وَ» و«يَ» في جداوله. معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| L3-L4 | الأدواتُ والمبنيّات: ذرّاتُها مشتقّةٌ من رسمها، ومرخَّصة | معلق | `suspended:tests/test_lexicon.py::test_every_entry_is_licensed` | في الأصل اختلف الرسمُ والذرّاتُ في عشرة مداخل؛ والمصدرُ الآن واحد. معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| Q11 | الإملاء: ما كُتب يُقرأ بعينه، ‎read (write w) = w‎، لكلّ سلسلة | معلق | `lean:Slge.Rasm.read_write`<br>`lean:Slge.Rasm.write_injective`<br>`suspended:tests/test_rasm_conformance.py::test_rasm_matches_lean`<br>`suspended:tests/test_orthography.py::test_roundtrip_exhaustive_upto_2`<br>`suspended:tests/test_orthography.py::test_roundtrip_exhaustive_3` | الأصلُ فحص 7 عيّنات؛ وعلى المرخَّصات بطول ≤ 2 كان يخطئ في 31 ويسقط في 87 («فِي» تعود ألفًا؛ والهمزةُ الساكنة KeyError). والمبرهَنُ قواعدُ الكاتب الخمسُ المعلنة على رموزٍ مجرّدة؛ ومطابقتُها بيونيكود البايثون على كلّ سلسلةٍ بطول ≤ 2. معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مبرهن |
| Q12 | الابتداء: المطلعُ متحرّك، وهمزةُ الوصل همزةٌ لا ألف | معلق | `suspended:tests/test_orthography.py::test_begin_respects_rho` | معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| Q13 | الوصل: همزةُ الوصل تسقط، والشمسيُّ يُدغم، والوصلةُ ليست ساكنين | معلق | `suspended:tests/test_orthography.py::test_join_bismillah` | معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_بعينة |
| Q14 | الوقف: الختامُ ساكن، والتنوينُ يُحذف | معلق | `suspended:tests/test_orthography.py::test_pause_tanwin` | معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_بعينة |
| Q15 | التطبيعُ متساوي الأثر | معلق | `suspended:tests/test_encoding.py::test_normalize_idempotent_on_every_char` | معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| Q16 | كاشفُ التعارض يلتقط كلَّ بديلٍ معلن | معلق | `suspended:tests/test_encoding.py::test_conflicts_catch_every_substitution` | معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| Q17 | ملفّاتُ المحرّك خاليةٌ من محارفَ خارج الجدول | معلق | `suspended:tests/test_encoding.py::test_sources_are_clean` | معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| Q3 | استواءُ البدال: تبديلُ حاملين في الجذر يتبدّل في المولَّد | معلق | `suspended:tests/test_morphology.py::test_equivariance_all_transpositions` | الأصلُ فحص 40 تبديلًا بعيّنة؛ هنا كلُّ تبديلٍ داخل كلّ صنفٍ على كلّ قالب. معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| Q4 | الإعرابُ إسقاطٌ على الخانة الأخيرة يحفظ الترخيص | معلق | `suspended:tests/test_morphology.py::test_iirab_touches_only_last_cell` | معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| Q5 | المثاليُّ المحظور (ألفٌ متحرّكة) لا يقع في أيّ ثابتٍ أو زائد | معلق | `suspended:tests/test_morphology.py::test_no_forbidden_cell_in_any_table` | كان الأصلُ يفحص PREFIX/SUFFIX ولا يفحص OPS، ففي OPS أربعةُ صفوفٍ تنقضه؛ صُحّحت. معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
| Q6 | إغلاقُ العمليّات في الـ116 | معلق | `suspended:tests/test_morphology.py::test_tables_are_closed_in_116` | معلَّقٌ مع وحدته (انظر SUSPENDED_REGISTRY.json)؛ الوسمُ المعلَن قبل التعليق: مفحوص_استقصاء |
