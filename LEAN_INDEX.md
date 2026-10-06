# فهرسُ مبرهنات Lean على درجات الترخيص التدريجيّ

مولَّدٌ بـ`python tools/gen_lean_index.py` من ملفّات `.lean` و`Audit.lean` و`out/axioms.txt`؛ لا يُحرَّر باليد. الـ116 من الغانم بإيداعه المثبَّت في `formal/lakefile.toml`.

**647 مبرهنة، منها 476 مدقَّقةُ المسلّمات.**

كلُّ درجةٍ تستهلك ما قبلها: لا تدخل الكلمةُ درجةً قبل أن تُرخَّص في التي تحتها. «مدقَّق» = في `Audit.lean` وطُبعت مسلّماتُه؛ وما ليس مدقَّقًا مبرهَنٌ في Lean لكن لم يُطبع سندُه بعدُ فلا يُستشهد به في `status.py`.

## الدرجة ١ — البايتُ والنقطة: UTF-8 تقابلٌ ذاتيُّ الحدّ

### `A116/Unicode.lean` — 7 مبرهنة (`A116.Unicode`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `cont_of_mod` | — | — | — |
| `decode_encode` | **القراءةُ تعيد الكتابةَ وما بعدها بعينه** لكلّ نقطةٍ في مجال يونيكود. | مدقَّق | propext, Classical.choice, Quot.sound |
| `encode_prefix_free` | **التفكيكُ وحيد:** ترميزان بذيلين متساويان ⟹ النقطتان واحدةٌ والذيلان واحد. | مدقَّق | propext, Classical.choice, Quot.sound |
| `encode_ne_nil` | — | — | — |
| `decodeAll_encodeAll` | **التيارُ يعود كلُّه.** | مدقَّق | propext, Classical.choice, Quot.sound |
| `arabic_is_two_bytes` | كلُّ ما في المدى العربيّ ‎U+0600–U+06FF‎ بايتان. | مدقَّق | propext, Quot.sound |
| `markOrder_restore` | حرفٌ لحقته شدّةٌ ثمّ حركة (رسمُ المصحف) أو حركةٌ ثمّ شدّة (NFC): الترتيبُ الأصليّ يُردّ بالسجلّ. | مدقَّق | propext, Quot.sound |

## الدرجة ٢ — الحدّ: ابتداءٌ ووصلٌ ووقف

### `A116/Boundary.lean` — 5 مبرهنة (`A116.Boundary`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `no_start_with_sukun` | **الابتداء:** المرخَّصُ لا يبدأ بساكن. | مدقَّق | propext |
| `pause_ends_with_sukun` | **الوقف:** مشغّلُ الوقف يُسكِّن الآخر، والناتجُ مرخَّصٌ وقفًا. | مدقَّق | propext, Quot.sound |
| `join_iff` | **الوصل:** وصلُ ‎a‎ (المنتهية بـ‎c‎) بـ‎b‎ مرخَّصٌ ⇔ حدُّهما جائز. | مدقَّق | propext, Quot.sound |
| `wasl_dropped_needs_moving_left` | **همزةُ الوصل:** إن سقطت وبقيت الكلمةُ مبدوءةً بساكنٍ (لْحَمْدُ) فلا ترخيصَ لها إلّا موصولةً بما | مدقَّق | propext, Quot.sound |
| `pause_then_join_is_not_join` | **الوقفُ ثمّ الوصلُ ليس وصلًا:** ما وُقف عليه (ساكنُ الآخر) لا يُوصل بما سقطت وصلُه. | مدقَّق | propext, Quot.sound |

## الدرجة ٣ — الخانة: 29 حاملًا × 4 حالات = 116

### `A116/Cells.lean` — 8 مبرهنة (`A116`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `mem_all` | — | — | — |
| `mem_cells` | **التمام:** كلُّ خانةٍ ممكنةٍ واقعةٌ في التعداد. | مدقَّق | propext, Quot.sound |
| `cells_nodup` | **المنع:** لا خانةَ تُعَدّ مرّتين. | مدقَّق | لا مسلّمات |
| `cells_length` | **العدد:** طولُ تعدادٍ تامٍّ بلا تكرار هو `116 = 29 × 4`. | مدقَّق | لا مسلّمات |
| `cells_length_eq_product` | **العدد:** طولُ تعدادٍ تامٍّ بلا تكرار هو `116 = 29 × 4`. | — | — |
| `cells112_length` | — | — | — |
| `hamzaRow_length` | — | — | — |
| `cells_split` | الفرقُ صفُّ الهمزة وحدَه: `116 = 112 + 4`، مُشتقًّا لا مكتوبًا. | مدقَّق | لا مسلّمات |

## الدرجة ٤ — الترخيصُ الثنائيّ: لا ابتداءَ بساكن ولا تجاورَ ساكنين

### `A116/Model.lean` — 11 مبرهنة (`A116`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `mem_all` | — | — | — |
| `step_depends_only_on_sukun` | — | مدقَّق | propext |
| `saturation_rungs` | درجاتُ الإشباع كما في `fixpoint_reading().rungs`: ‎(1, 3)‎، ثمّ لا زيادة. | مدقَّق | propext |
| `Sstar_closed_on_cells` | **الإغلاقُ مفحوصٌ استقصاءً:** ‎|Sstar| × 116 = 348‎ انتقالًا، كلُّها داخلَ `Sstar`. | — | — |
| `Sstar_closed` | والإغلاقُ على كلّ خانةٍ ممكنة، لا على المعدودة فحسب، بتمام التعداد. | مدقَّق | propext, Quot.sound |
| `awaiting_mem_Sstar` | والإغلاقُ على كلّ خانةٍ ممكنة، لا على المعدودة فحسب، بتمام التعداد. | — | — |
| `run_mem_Sstar` | **المبرهنة ١:** أثرُ كلّ سلسلةٍ بأيّ طولٍ واقعٌ في `Sstar`. والبرهانُ استقراءٌ | مدقَّق | propext, Quot.sound |
| `Sstar_complete` | **خواءُ المبرهنة ١ مُعلَنًا:** `Sstar` هي الحالاتُ كلُّها. | مدقَّق | propext |
| `run_ne_fellOut_aux` | اللمّةُ الجامعة: توصيفُ الحالتين غيرِ الساقطتين معًا، بالاستقراء على السلسلة. | — | — |
| `run_ne_fellOut_iff` | **المبرهنة ٢:** سلسلةٌ لا تسقط من النموذج **إذا وفقط إذا** كانت مقبولةً | مدقَّق | propext |
| `run_eq_fellOut_iff` | صيغةُ النقض: تسقط السلسلةُ إذا وفقط إذا بدأت بساكنٍ أو تجاور فيها ساكنان. | مدقَّق | propext, Classical.choice, Quot.sound |

## الدرجة ٥ — العدّ: ‎U(n+2) = 87U(n+1) + 87·29·U(n)‎

### `A116/Count.lean` — 19 مبرهنة (`A116`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `decode_code_on_cells` | — | — | — |
| `decode_code` | — | — | — |
| `code_decode` | — | — | — |
| `code_lt` | — | — | — |
| `code_lt_87_iff` | — | — | — |
| `decide_code_lt` | — | — | — |
| `admissible_iff_valid_aux` | اللمّةُ الجامعة، على منوال `run_ne_fellOut_aux`. | — | — |
| `admissible_iff_valid` | **السلسلةُ مقبولةٌ في النموذج ⟺ صورتُها جائزةٌ لا تبدأ بمحجور.** | مدقَّق | propext, Quot.sound |
| `run_ne_fellOut_iff_valid` | والآلةُ نفسُها: لا تسقط السلسلةُ ⟺ صورتُها جائزة. | مدقَّق | propext, Quot.sound |
| `cellFold_lt` | — | مدقَّق | propext, Quot.sound |
| `map_code_injective` | — | — | — |
| `cellFold_injective` | **متباين:** مقبولتان بطولٍ واحدٍ وطيٍّ واحدٍ هما واحدة. | مدقَّق | propext, Quot.sound |
| `map_code_decode` | **متباين:** مقبولتان بطولٍ واحدٍ وطيٍّ واحدٍ هما واحدة. | — | — |
| `cellFold_surjective` | **شامل:** كلُّ عددٍ دون ‎U(n)‎ طيُّ سلسلةٍ مقبولةٍ بطول `n`. | مدقَّق | propext, Quot.sound |
| `U_zero` | — | — | — |
| `U_one` | — | — | — |
| `U_succ_succ` | **‎U(n+2) = 87·U(n+1) + 87·29·U(n)‎ لكلّ ‎n‎.** | مدقَّق | propext, Quot.sound |
| `U_values` | أوّلُ الأعداد؛ ويقابلها CI بالعدّ المباشر في البايثون حتى الطول 2. | مدقَّق | لا مسلّمات |
| `hamil_ladder` | **سلّمُ hamil** (`burhan/THE-PROOF.md`): ‎T(n)‎ على حقل الـ112 بـ‎f = 84، b = 28‎. | مدقَّق | لا مسلّمات |

## الدرجة ٦ — الطيُّ والعدد: المرخَّصةُ ↔ عددُها

### `A116/Fold.lean` — 16 مبرهنة (`A116.Fold`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `T_succ_succ` | **المبرهنة ١:** ‎T(n+2) = f·T(n+1) + f·b·T(n)‎. | مدقَّق | propext |
| `S_false_le_S_true` | **المبرهنة ١:** ‎T(n+2) = f·T(n+1) + f·b·T(n)‎. | — | — |
| `fold_cons_free` | الطيُّ على رمزٍ حرٍّ في الصدر. | — | — |
| `fold_cons_blocked` | الطيُّ على رمزٍ محجورٍ في الصدر (ولا يقع إلّا حيث يجوز). | — | — |
| `fold_lt` | **الطيُّ داخلَ مداه:** صورةُ كلّ جائزةٍ أصغرُ من عدد الجائزات. | مدقَّق | propext, Quot.sound |
| `unfold_lo` | الفكُّ حين يقع العددُ في كتلة الأحرار. | — | — |
| `unfold_hi` | الفكُّ حين يقع العددُ فوق كتلة الأحرار. | — | — |
| `unfold_fold` | **الفكُّ معكوسُ الطيّ من اليسار:** كلُّ جائزةٍ تعود بعينها. | مدقَّق | propext, Quot.sound |
| `unfold_spec` | **الفكُّ معكوسُ الطيّ من اليمين:** كلُّ عددٍ في المدى صورةُ جائزةٍ بالطول المطلوب. | مدقَّق | propext, Quot.sound |
| `fold_injective` | **التقابلُ مجموعًا:** جائزتان بطولٍ واحدٍ لهما طيٌّ واحدٌ فهما واحدة. | مدقَّق | propext, Quot.sound |
| `T_pos` | — | — | — |
| `le_off` | — | — | — |
| `exists_interval` | كلُّ عددٍ يقع في فترة طولٍ واحدة. | — | — |
| `off_mono` | كلُّ عددٍ يقع في فترة طولٍ واحدة. | — | — |
| `foldAny_injective` | **الطيُّ بلا طول متباين:** لا يُستعار الطولُ من خارج. | مدقَّق | propext, Quot.sound |
| `foldAny_surjective` | **الطيُّ بلا طول شامل:** كلُّ عددٍ طبيعيٍّ صورةُ جائزة. | مدقَّق | propext, Quot.sound |

### `A116/Numbering.lean` — 21 مبرهنة (`A116.Numbering`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `valid_zero_iff` | — | مدقَّق | propext, Quot.sound |
| `S_zero_pow` | — | — | — |
| `off_zero_geo` | — | — | — |
| `digits_cons` | — | — | — |
| `fold_zero_eq_digits` | — | مدقَّق | propext |
| `foldAny_zero_closed` | ‎F(a) = O(n) + v(a)‎ بصيغته الصريحة. | مدقَّق | propext |
| `bridgeCell_bridgeIndex_on_cells` | — | — | — |
| `bridgeCell_bridgeIndex` | — | مدقَّق | propext, Quot.sound |
| `bridgeIndex_bridgeCell` | — | مدقَّق | لا مسلّمات |
| `bridgeIndex_lt_on_cells` | — | — | — |
| `bridgeIndex_lt` | — | — | — |
| `orders_differ_only_in_two_rows` | ترتيبُ الجسر وترتيبُ `Cells` يختلفان في ثمانيةِ مواضعَ لا غير: صفّا الألف والهمزة. | مدقَّق | لا مسلّمات |
| `bridgeIndex_injective` | ترتيبُ الجسر وترتيبُ `Cells` يختلفان في ثمانيةِ مواضعَ لا غير: صفّا الألف والهمزة. | — | — |
| `atomNumber_closed` | — | مدقَّق | propext, Quot.sound |
| `atomNumber_injective` | **التباين:** سلسلتان بعددٍ واحدٍ هما واحدة، بأيّ طول. | مدقَّق | propext, Quot.sound |
| `atomNumber_surjective` | **الشمول:** كلُّ عددٍ طبيعيٍّ رقمُ سلسلةٍ واحدة. | مدقَّق | propext, Quot.sound |
| `tri_mono` | — | — | — |
| `tri_closed` | — | — | — |
| `pair_injective` | **التباين.** | مدقَّق | propext, Classical.choice, Quot.sound |
| `pair_surjective` | **الشمول.** | مدقَّق | propext, Quot.sound |
| `pair_closed` | الصيغةُ المغلقةُ في `contextual.pair`: ‎(u+r)(u+r+1)/2 + r‎. | مدقَّق | propext, Quot.sound |

## الدرجة ٧ — الليفُ والبقيّة: الرسمُ ↔ الذرّات، وقواعدُ الطبعة تُردّ بعينها

### `A116/Fiber.lean` — 13 مبرهنة (`A116.Fiber`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `mem_fiber` | — | — | — |
| `rank_lt` | — | مدقَّق | propext |
| `decode_encode` | **الاستعادة.** | مدقَّق | propext, Quot.sound |
| `encode_injective` | **التباين**: من الاستعادة. | مدقَّق | propext, Quot.sound |
| `decode_sound` | الفكُّ لا يُخرج إلا عنصرًا من `D` صورتُه المطلوبة؛ ورتبةٌ خارج الليف تُرفض. | مدقَّق | propext |
| `decode_none_of_rank_ge` | الفكُّ لا يُخرج إلا عنصرًا من `D` صورتُه المطلوبة؛ ورتبةٌ خارج الليف تُرفض. | — | — |
| `fiber_nodup` | الفكُّ لا يُخرج إلا عنصرًا من `D` صورتُه المطلوبة؛ ورتبةٌ خارج الليف تُرفض. | — | — |
| `register_injective_on_fiber` | سجلٌّ يُستعاد منه كلُّ عنصرٍ من ليفه مع الصورة متباينُ القيم على الليف. | — | — |
| `nodup_nat_length_le` | قائمةُ أعدادٍ بلا تكرارٍ كلُّها أصغرُ من ‎n‎ طولُها لا يزيد على ‎n‎. | — | — |
| `nodup_fin_length_le` | قائمةٌ بلا تكرارٍ من ‎Fin k‎ طولُها لا يزيد على ‎k‎ (مبدأ الحمام). | مدقَّق | propext, Classical.choice, Quot.sound |
| `fiber_length_le` | **الحدّ الأدنى.** كلُّ سجلٍّ بقيمٍ في ‎Fin k‎ يُستعاد منه الليفُ كلُّه يحقّق ‎m ≤ k‎. | مدقَّق | propext, Classical.choice, Quot.sound |
| `rank_register_fits` | وسجلُّ الرتبة يبلغ هذا الحدّ: ‎m‎ حالةً بالضبط تكفي. | — | — |
| `fiber_length_le_two_pow` | **البتّات.** سجلٌّ ثابتُ الطول بـ‎b‎ بتّاتٍ يستعيد الليفَ ⇒ ‎m ≤ 2^b‎. | مدقَّق | propext, Classical.choice, Quot.sound |

### `A116/Residue.lean` — 6 مبرهنة (`A116.Residue`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `sukun_restore` | `sukun`: الطبعةُ حذفت سكونًا بعد حرفٍ؛ الإصلاحُ يدخله؛ السجلُّ يحذفه. | مدقَّق | propext, Quot.sound |
| `fariqa_restore` | `fariqa`: الطبعةُ كتبت ألفًا بعد واوٍ ساكنةٍ في الآخر؛ الإصلاحُ يحذفها؛ السجلُّ يعيدها. | مدقَّق | propext, Quot.sound |
| `tanwinAlif_restore` | `tanwinAlif`: الطبعةُ كتبت الألفَ قبل التنوين؛ الإصلاحُ يقدّم التنوين؛ السجلُّ يعيد الترتيب. | مدقَّق | propext, Quot.sound |
| `idgham_restore` | `idgham`: الطبعةُ وضعت شدّةً أوّلَ الكلمة؛ الإصلاحُ يحذفها؛ السجلُّ يعيدها. | مدقَّق | propext, Quot.sound |
| `chain_restore` | **سلسلةُ التعديلات تُردّ**: مهما كان عددُ القواعد المطبَّقة على الكلمة، `restoreAll` يعيد الرسم. | مدقَّق | propext |
| `residue_separates` | **الرسمُ يحدّد الصورةَ والبقيّةَ معًا**: صورتان وبقيّتان تردّان إلى رسمٍ واحد هما واحدةٌ وواحدة. | مدقَّق | لا مسلّمات |

## الدرجة ٨ — التقطيعُ الثلاثيّ: cv/v/c، المدّ، الوقف، الوصل

### `A116/Stages.lean` — 15 مبرهنة (`A116.Stages`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `sylOf_coda` | — | — | — |
| `leadOf_atoms` | — | — | — |
| `coda_of_sylOf` | — | — | — |
| `atoms_of_leadOf` | — | — | — |
| `run_append` | — | — | — |
| `run_length` | — | — | — |
| `run_of_noCV` | — | — | — |
| `cv_not_mem_coda` | — | — | — |
| `cv_not_mem_lead` | — | — | — |
| `startsCV_flatMap` | — | — | — |
| `syls_flatMap` | — | — | — |
| `parse_flat` | — | مدقَّق | propext, Quot.sound |
| `flatMap_of_syls` | — | — | — |
| `flat_parse` | — | مدقَّق | propext, Quot.sound |
| `flat_injective` | — | مدقَّق | propext, Quot.sound |

### `A116/Ternary.lean` — 14 مبرهنة (`A116.Ternary`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `greedy_spec` | — | — | — |
| `binary_is_continue` | — | مدقَّق | propext, Quot.sound |
| `parse_eq_of_flat` | كلُّ تقطيعٍ لسلسلةٍ هو تقطيعُها الوحيد. | — | — |
| `continue_strictly_extends_binary` | — | مدقَّق | propext, Quot.sound |
| `continue_is_pause` | — | مدقَّق | propext, Quot.sound |
| `pause_strictly_extends_continue` | — | مدقَّق | propext, Quot.sound |
| `tamm_is_pause_only` | — | مدقَّق | propext, Quot.sound |
| `binary_is_blind_to_madd` | — | مدقَّق | propext, Quot.sound |
| `continueB_iff` | — | مدقَّق | propext, Quot.sound |
| `pauseB_iff` | — | مدقَّق | propext, Quot.sound |
| `noAdjacent_iff_noSS` | — | — | — |
| `admissible_iff_admissibleB` | — | مدقَّق | propext |
| `noPair_eq_noSS` | — | — | — |
| `binOK_eq_admissibleB` | — | مدقَّق | propext |

### `A116/Pause.lean` — 8 مبرهنة (`A116.Pause`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `mem_pats` | — | — | — |
| `admissibleB_eq_okB` | — | — | — |
| `mem_pats_iff` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `weights_eq_S` | — | — | — |
| `U_by_patterns` | — | مدقَّق | propext |
| `pause_snoc` | — | — | — |
| `pause_admissible` | — | مدقَّق | propext, Quot.sound |
| `pause_strictly_extends` | — | مدقَّق | propext, Classical.choice, Quot.sound |

### `A116/Junction.lean` — 10 مبرهنة (`A116.Junction`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `pat_mapCarriers` | — | — | — |
| `admissible_map_carriers` | — | مدقَّق | propext |
| `run_append` | — | — | — |
| `admissible_prefix` | — | مدقَّق | propext, Quot.sound |
| `run_snoc_of_ne` | بعد سلسلةٍ لم تسقط وآخرُها ‎c‎: الحالةُ تُعيِّنها ‎c‎ وحدَها. | — | — |
| `admissible_append` | بعد سلسلةٍ لم تسقط وآخرُها ‎c‎: الحالةُ تُعيِّنها ‎c‎ وحدَها. | مدقَّق | propext, Quot.sound |
| `U_by_patterns_upto_6` | — | مدقَّق | propext |
| `licensed_upto_4` | — | مدقَّق | لا مسلّمات |
| `burnside_3` | — | مدقَّق | لا مسلّمات |
| `burnside_4` | — | مدقَّق | لا مسلّمات |

## الدرجة ٩ — الإعلالُ والهمزة: تعديلاتٌ على الخانات تُردّ، والكرسيُّ دالّةٌ في السياق

### `A116/Ilal.lean` — 23 مبرهنة (`A116.Ilal`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `admissible_of_pat_eq` | — | — | — |
| `admissible_replace_carrier` | إبدالُ حاملٍ مع بقاء الحالة: الترخيصُ واحد. | مدقَّق | propext |
| `step_vowelled` | إبدالُ حاملٍ مع بقاء الحالة: الترخيصُ واحد. | — | — |
| `step_sukun_afterSeed` | إبدالُ حاملٍ مع بقاء الحالة: الترخيصُ واحد. | — | — |
| `step_sukun_awaiting` | إبدالُ حاملٍ مع بقاء الحالة: الترخيصُ واحد. | — | — |
| `run3` | إبدالُ حاملٍ مع بقاء الحالة: الترخيصُ واحد. | — | — |
| `run2` | إبدالُ حاملٍ مع بقاء الحالة: الترخيصُ واحد. | — | — |
| `run_three` | إبدالُ حاملٍ مع بقاء الحالة: الترخيصُ واحد. | — | — |
| `vowelled_to_sukun_between_vowelled` | قلبُ متحرّكٍ ساكنًا بين متحرّكين (قَوَلَ ← قَالَ) يحفظ الترخيص. | مدقَّق | propext, Quot.sound |
| `swap_sukun_vowel` | نقلُ الحركة (يَقْوُلُ ← يَقُولُ): ساكنٌ ثمّ متحرّكٌ ثمّ متحرّك ← متحرّكٌ ثمّ ساكنٌ ثمّ متحرّك. | مدقَّق | propext, Quot.sound |
| `delete_sukun_after_vowelled` | حذفُ ساكنٍ بعد متحرّك (يَوْعِدُ ← يَعِدُ) يحفظ الترخيص إن تلاه متحرّك. | مدقَّق | propext, Quot.sound |
| `two_sukun_not_admissible` | ساكنان متجاوران: لا ترخيص. | مدقَّق | propext, Quot.sound |
| `qalb_ayn_restore` | 1. قلبُ العين ألفًا: الأصلُ ‎(و/ي، فتحة)‎ يُردّ من السجلّ. | مدقَّق | propext, Classical.choice, Quot.sound |
| `hadhf_ayn_restore` | 2. حذفُ العين لالتقاء الساكنين، مع نقل حركة الفاء: يُردّ الأصل. | — | — |
| `hadhf_ayn_forced` | 2′. **الإلزام**: الأصلُ (عينٌ ساكنةٌ ثمّ ساكن) غيرُ مرخَّصٍ أصلًا، فالحذفُ واجب. | مدقَّق | propext, Quot.sound |
| `naql_restore` | 3. النقل: يُردّ الأصل. | مدقَّق | propext, Quot.sound |
| `qalb_lam_restore` | 4. قلبُ لام الناقص ألفًا: يُردّ الأصل. | — | — |
| `hadhf_lam_restore` | 5. حذفُ لام الناقص قبل واو الجماعة (دَعَوُوْا ← دَعَوْا): يُردّ الأصل. | — | — |
| `hadhf_waw_restore` | 6. حذفُ واو المثال: يُردّ الأصل. | — | — |
| `ibdal_restore` | 7–12. الإبدالُ (حاملٌ بحامل): يُردّ الأصل. | مدقَّق | propext, Quot.sound |
| `qala_witness` | قَوَلَ ← قَالَ: الأصلُ والصورةُ كلاهما مرخَّص (القلبُ حافظ). | مدقَّق | propext, Classical.choice, Quot.sound |
| `qultu_witness` | قَالْتُ ← قُلْتُ: الأصلُ غيرُ مرخَّصٍ والصورةُ مرخَّصة (الحذفُ ملزَم). | مدقَّق | propext, Classical.choice, Quot.sound |
| `yaqulu_witness` | يَقْوُلُ ← يَقُولُ: كلاهما مرخَّص (النقلُ حافظ). | مدقَّق | propext, Classical.choice, Quot.sound |

### `A116/Hamza.lean` — 7 مبرهنة (`A116.Hamza`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `seat_initial_by_own` | — | مدقَّق | propext |
| `seat_final_by_prev` | — | مدقَّق | propext |
| `seat_after_madd_final_is_line` | — | مدقَّق | propext |
| `seat_medial_strongest` | — | مدقَّق | propext |
| `seat_depends_on_context` | الكرسيُّ يتبع السياق لا الهمزة: سياقان لهمزةٍ واحدةٍ يختلفان كرسيًّا. | مدقَّق | لا مسلّمات |
| `qat_stays_when_joined` | همزةُ القطع المتحرّكةُ أوّلَ الكلمة تبقى في الوصل، والوصلُ بها مرخَّصٌ مهما كان آخرُ ما قبلها. | مدقَّق | propext, Classical.choice, Quot.sound |
| `prefix_hamza_admissible` | إسباقُ همزةٍ متحرّكةٍ (استفهام، متكلّم، تعدية) لمرخَّصةٍ يُبقيها مرخَّصة. | مدقَّق | propext, Classical.choice, Quot.sound |

## الدرجة ١٠ — الاشتقاقُ والاسترجاع: الأصلُ يُستردّ بالقالب، والصيغةُ وحدَها لا تعيّنه

### `A116/Ishtiqaq.lean` — 8 مبرهنة (`A116.Ishtiqaq`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `extract_fill` | — | — | — |
| `extract_fill_wf` | — | مدقَّق | propext |
| `root_sublist_fill` | — | — | — |
| `root_sublist_fill_wf` | — | مدقَّق | propext |
| `fill_injective` | — | مدقَّق | propext, Quot.sound |
| `soundTemplates_length` | — | — | — |
| `soundTemplates_wf` | — | مدقَّق | propext |
| `form_alone_does_not_determine_root` | انْتَبَرَ: انفعل من (ت ب ر) وافتعل من (ن ب ر) صيغةٌ واحدة. | مدقَّق | propext |

### `A116/Derivation.lean` — 7 مبرهنة (`A116.Derivation`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `edges_length` | — | — | — |
| `branching_nodes` | — | مدقَّق | لا مسلّمات |
| `rows_stochastic` | — | مدقَّق | لا مسلّمات |
| `stationary_unique` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `share_of_I` | حصّةُ المجرّد: `π(I) = v I / Σ v = 2/5` لكلّ متّجهٍ مستقرّ. | مدقَّق | propext, Classical.choice, Quot.sound |
| `stationary_w` | — | مدقَّق | propext |
| `w_total` | — | — | — |

### `A116/Recovery.lean` — 8 مبرهنة (`A116.Recovery`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `edit_roundtrip` | — | مدقَّق | propext, Quot.sound |
| `shadda_restore` | — | مدقَّق | propext, Quot.sound |
| `tanwin_restore` | — | مدقَّق | propext, Quot.sound |
| `hamza_restore` | — | مدقَّق | propext, Quot.sound |
| `ilal_edit_restore` | — | مدقَّق | propext, Quot.sound |
| `no_seat_recovery_from_hamza_alone` | — | مدقَّق | propext |
| `restoration_forces_fiber_separation` | — | مدقَّق | لا مسلّمات |
| `compose_restoration` | — | مدقَّق | لا مسلّمات |

### `A116/Field112.lean` — 7 مبرهنة (`A116.Field112`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `letters28_length` | — | — | — |
| `letters28_nodup` | — | — | — |
| `carriers29_length` | — | — | — |
| `hamilField112_length` | — | — | — |
| `field112_eq_cells112` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `hamzaRow_named` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `cells_eq_field112_append_hamza` | — | مدقَّق | propext, Classical.choice, Quot.sound |

### `A116/Ladder.lean` — 10 مبرهنة (`A116.Ladder`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `run_depends_only_on_pattern` | — | مدقَّق | propext |
| `U_eq_pow_mul_g` | — | مدقَّق | propext, Quot.sound |
| `g_values` | — | — | — |
| `pattern_count_fib` | عددُ الأنماط الجائزة بطول n — وهو بالتقابل `Fold.fold 1 1 false` عددُ الكلمات | مدقَّق | propext |
| `admissible_patterns_3` | — | مدقَّق | propext |
| `U3_by_pattern` | — | مدقَّق | لا مسلّمات |
| `cited_letters_are_carriers` | كلُّ حرفٍ مستعمَلٍ أدناه حاملٌ معلَن، فلا يسقط `idxOf` إلى الصفر صامتًا. | — | — |
| `patterns_of_the_cited_words` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `kana_and_inna_are_indistinguishable` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `kana_is_not_kataba` | — | مدقَّق | propext, Classical.choice, Quot.sound |

## الدرجة ١١ — الجسرُ إلى SLGE: ترميزان، برهانٌ واحد

### `Slge/Bridge.lean` — 15 مبرهنة (`Slge`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `mem_scells` | — | — | — |
| `scells_length` | — | مدقَّق | لا مسلّمات |
| `ofCell_toCell_on` | — | — | — |
| `toCell_ofCell_on` | — | — | — |
| `toCell_isSukun_on` | — | — | — |
| `toCell_injective` | — | — | — |
| `map_toCell_injective` | — | — | — |
| `map_toCell_ofCell` | — | — | — |
| `noAdj_iff` | — | — | — |
| `licensed_iff` | **الترخيصُ هو القبولُ في الـ116 بعينه**، لكلّ سلسلةٍ بأيّ طول. | مدقَّق | propext, Quot.sound |
| `slgeFold_lt` | — | — | — |
| `slgeFold_injective` | **متباين:** مرخَّصتان بطولٍ واحدٍ وطيٍّ واحدٍ هما واحدة. | مدقَّق | propext, Quot.sound |
| `slgeFold_surjective` | **شامل:** كلُّ عددٍ دون ‎U(n)‎ طيُّ مرخَّصةٍ بطول n، وهي `slgeUnfold n k`. | مدقَّق | propext, Quot.sound |
| `countPair_eq` | — | — | — |
| `count_eq_U` | **عدّادُ SLGE هو ‎U(n)‎ لكلّ n.** | مدقَّق | propext, Quot.sound |

### `Slge/Consistency.lean` — 4 مبرهنة (`Slge.Consistency`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `atomNumberS_injective` | — | — | — |
| `atomNumber_determines_fold` | — | مدقَّق | propext, Quot.sound |
| `fold_determines_atomNumber` | — | مدقَّق | propext, Quot.sound |
| `numbers_agree` | **العددان متكافئان** على مرخَّصتين بطولٍ واحد. | مدقَّق | propext, Quot.sound |

### `Slge/Rasm.lean` — 7 مبرهنة (`Slge.Rasm`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `headOK_single` | — | — | — |
| `headOK_withTanwin` | — | — | — |
| `headOK_write` | — | مدقَّق | propext |
| `read_single_append` | — | — | — |
| `read_withTanwin` | — | — | — |
| `read_write` | **ما كُتب يُقرأ بعينه**، لكلّ سلسلةٍ ولأيّ سابق. | مدقَّق | propext, Quot.sound |
| `write_injective` | **ما كُتب يُقرأ بعينه**، لكلّ سلسلةٍ ولأيّ سابق. | مدقَّق | propext, Quot.sound |

## الدرجة ١٢ — التسلسل: النصُّ تيارُ شهاداتٍ ذاتيُّ الحدّ

### `Slge/Sequence.lean` — 8 مبرهنة (`Slge.Sequence`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `cellUnfold_cellFold` | — | — | — |
| `slgeUnfold_slgeFold` | **الاسترجاع:** `slgeUnfold` بعد `slgeFold` هو الكلمةُ بعينها. | مدقَّق | propext, Quot.sound |
| `bitsToNat_natToBits` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `U_lt_two_pow_width` | — | مدقَّق | propext |
| `readLen_lenBits` | — | — | — |
| `decodeWord_encodeWord` | **ذاتيّةُ الحدّ:** كلمةٌ مرخَّصةٌ مرمَّزةٌ في رأس أيّ تيارٍ تُقرأ بعينها ويبقى ما بعدها بعينه. | مدقَّق | propext, Classical.choice, Quot.sound |
| `encodeWord_prefix_free` | **التفكيكُ وحيد:** إن تساوى ترميزا كلمتين مرخَّصتين مع ذيليهما فالكلمتان واحدةٌ والذيلان واحد. | مدقَّق | propext, Classical.choice, Quot.sound |
| `decode_encode` | **التيار يعود كلُّه:** فكُّ ترميزِ كلماتٍ مرخَّصةٍ يعيدها بترتيبها. | مدقَّق | propext, Classical.choice, Quot.sound |

## الدرجة ١٣ — المنح: لا اسمَ قبل قبضته

### `Slge/Grant.lean` — 7 مبرهنة (`Slge.Grant`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `grant_iff_check` | — | مدقَّق | لا مسلّمات |
| `no_grant_of_refused` | ما رفضه الفحصُ لا يُمنح، مهما قيل. | مدقَّق | لا مسلّمات |
| `ladder_implies_lower` | — | — | — |
| `ladder_implies_base` | — | مدقَّق | propext |
| `empty_ladder_grants_nothing` | لا درجةَ فوق سُلَّمٍ فارغ. | مدقَّق | propext |
| `mursam_sound` | لا يُمنح «مرسوم» إلّا لمرخَّص — وهو بالجسر `Admissible` في الـ116. | مدقَّق | propext, Quot.sound |
| `mursam_refuses_initial_sukun` | شاهدُ رفض: ساكنٌ في الصدر لا يُمنح. | مدقَّق | propext |

## الدرجة ١٤ — الأقانيم: الصنفُ عضويّةٌ قابلةٌ للفصل؛ وأسماءُ الإشارة نواةٌ بثلاث عمليّات

### `Slge/Categories.lean` — 9 مبرهنة (`Slge.Categories`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `sub_refl` | — | — | — |
| `sub_trans` | — | مدقَّق | لا مسلّمات |
| `sound_of_sub` | — | — | — |
| `ofList_sound` | — | — | — |
| `pronouns_licensed` | — | — | — |
| `pronoun_sound` | — | مدقَّق | propext |
| `pronoun_sub_licensed` | — | — | — |
| `pronoun_numbers_nodup` | أعدادُ الضمائر بطيّها متباينة: لكلٍّ بصمتُه. | مدقَّق | لا مسلّمات |
| `pronoun_shape_not_fingerprint` | وأشكالُها ليست بصمة: هُوَ وهِيَ تتابعُ سكونٍ واحدٌ وكلمتان مختلفتان. | — | — |

### `Slge/Ishara.lean` — 16 مبرهنة (`Slge.Ishara`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `tanbih_licensed` | — | مدقَّق | propext, Quot.sound |
| `bud_licensed` | — | مدقَّق | propext |
| `v22` | — | — | — |
| `v25` | — | — | — |
| `v28` | — | — | — |
| `s3` | — | — | — |
| `caseOf_dual` | — | مدقَّق | propext |
| `caseOf_dual_bud` | — | مدقَّق | propext |
| `nasb_eq_jarr_dual` | الياءُ لا تفرّق بين النصب والجرّ: صورةٌ واحدة. | مدقَّق | propext |
| `forms_count` | — | — | — |
| `forms_licensed` | — | مدقَّق | propext |
| `forms_nodup` | — | مدقَّق | propext |
| `duals_have_case` | — | مدقَّق | propext |
| `mabni_no_case` | — | مدقَّق | propext |
| `witnessed_count` | — | — | — |
| `witnessed_subset` | — | مدقَّق | propext |

### `Slge/Marifa.lean` — 17 مبرهنة (`Slge.Marifa`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `shamsi_map_isSukun` | — | — | — |
| `shamsi_licensed` | — | مدقَّق | propext |
| `al_licensed` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `hasAl_al` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `licensed_initOf` | — | — | — |
| `dropTanwin_licensed` | — | مدقَّق | propext |
| `v24` | — | — | — |
| `v26` | — | — | — |
| `idafa_no_tanwin` | المضافُ إلى ضميرٍ لا تنوينَ له: آخرُه الضميرُ لا النون. | مدقَّق | propext, Classical.choice, Quot.sound |
| `mawsul_licensed` | — | مدقَّق | propext |
| `mawsul_nodup` | — | مدقَّق | propext |
| `mawsul_al` | الموصولُ المبدوءُ بأل تقرأ الأداةَ في صدره. | مدقَّق | propext |
| `mawsul_dual_case` | مثنّى الموصول يُقرأ إعرابُه كالإشارة: من المدّ قبل النون. | مدقَّق | propext |
| `al_is_marifa` | — | — | — |
| `mudaf_is_marifa` | — | مدقَّق | propext |
| `deposited_no_tanwin` | المودَعُ بالذات لا تنوينَ فيه — إلّا مَنْ: نونُها أصلٌ ساكنٌ بعد فتحٍ، فالخانةُ تقرؤها كتنوين | مدقَّق | propext |
| `man_looks_like_tanwin` | المودَعُ بالذات لا تنوينَ فيه — إلّا مَنْ: نونُها أصلٌ ساكنٌ بعد فتحٍ، فالخانةُ تقرؤها كتنوين | مدقَّق | propext |

## الدرجة ١٥ — الوزنُ وشبكتُه: القالبُ يُرخَّص مرّةً لكلّ الأصول، والجبرُ يحفظ الأصل

### `Slge/Wazn.lean` — 13 مبرهنة (`Slge.Wazn`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `extract_fill` | — | — | — |
| `lookup_map` | — | — | — |
| `rootOf_fill` | الأصلُ يُستردّ من الصيغة، لكلّ قالبٍ سليمٍ ولكلّ أصل. | مدقَّق | propext |
| `states_fill` | حالاتُ الصيغة حالاتُ القالب. | مدقَّق | propext, Quot.sound |
| `noAdj_states` | — | — | — |
| `licensed_states` | — | — | — |
| `licensed_fill_indep` | **الترخيصُ لا يتوقّف على الأصل.** | مدقَّق | propext, Quot.sound |
| `licensed_of_mizan` | مرخَّصٌ بميزانه ⇒ مرخَّصٌ بكلّ أصل. | — | — |
| `awzan_count` | — | — | — |
| `awzan_wf` | — | مدقَّق | propext |
| `awzan_mizan_licensed` | — | — | — |
| `awzan_licensed` | كلُّ وزنٍ مودَعٍ مرخَّصٌ لكلّ أصلٍ ثلاثيّ. | مدقَّق | propext, Quot.sound |
| `awzan_root` | وكلُّ وزنٍ مودَعٍ يردّ الأصل. | مدقَّق | propext |

### `Slge/Shabaka.lean` — 9 مبرهنة (`Slge.Shabaka`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `mem_slots_ins` | — | — | — |
| `slots_setSt` | — | — | — |
| `wf_of_sub` | — | — | — |
| `wf_step` | كلُّ عمليّةٍ تحفظ السلامة. | مدقَّق | propext, Quot.sound |
| `wf_run` | وكلُّ تتابعٍ. | مدقَّق | propext, Quot.sound |
| `edges_apply` | الابنُ هو الأبُ بعد عمليّاته، لكلّ حافّة. | مدقَّق | propext |
| `edges_count` | — | — | — |
| `network_rooted` | كلُّ وزنٍ يبلغ الجذر. | مدقَّق | propext |
| `run_edge_wf` | كلُّ وزنٍ يبلغ الجذر. | مدقَّق | propext, Quot.sound |

## الدرجة ١٦ — الإعرابُ بالحروف وبالنون والضمائرُ: الأسماءُ الخمسة والأفعالُ الخمسة ونا والتاء

### `Slge/Khamsa.lean` — 13 مبرهنة (`Slge.Khamsa`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `madd_injective` | — | — | — |
| `madd_matches_short` | — | مدقَّق | propext |
| `getLast_form` | — | — | — |
| `caseOf_form` | — | مدقَّق | propext |
| `form_injective_stem` | — | مدقَّق | propext |
| `ya_neutralizes_case` | — | — | — |
| `tanwin_when_not_mudaf` | — | — | — |
| `letters_when_mudaf` | — | — | — |
| `no_guess_for_plural` | — | مدقَّق | propext |
| `khamsa_licensed` | — | مدقَّق | propext |
| `khamsa_numbers_nodup` | — | مدقَّق | propext |
| `forms_count` | — | — | — |
| `khamsa_tanwin_licensed` | وبالتنوين كذلك مرخَّصة. | — | — |

### `Slge/Afal.lean` — 12 مبرهنة (`Slge.Afal`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `glide_matches_before` | — | مدقَّق | propext |
| `five_pairs` | — | — | — |
| `nasb_eq_jazm` | — | مدقَّق | propext |
| `lastOf_cons_append` | — | — | — |
| `initOf_cons_append` | — | — | — |
| `form_raf` | — | — | — |
| `form_nasb` | — | — | — |
| `moodOf_raf` | — | مدقَّق | propext |
| `moodOf_nasb` | — | مدقَّق | propext |
| `pronounOf_form` | — | مدقَّق | propext |
| `five_licensed` | — | مدقَّق | propext |
| `forms_count` | عددُها: جذعان بالغيبة (٢ ضميرين × ٣) + جذعان بالخطاب (٣ × ٣) = ٣٠. | — | — |

### `Slge/Damair.lean` — 16 مبرهنة (`Slge.Damair`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `iyya_is_carrier_plus_suffix` | — | مدقَّق | propext, Quot.sound |
| `nasbDetached_count` | — | — | — |
| `na_raf_reads_sukun` | نا الفاعلين: يلحق ما آخرُه ساكنٌ صحيح (لا حرفَ مدّ). | مدقَّق | propext |
| `na_after_madd_not_raf` | وبعد حرف المدّ (إِيَّانَا، فِينَا) ليس رفعًا: المدُّ حركةٌ طويلة. | مدقَّق | propext, Classical.choice, Quot.sound |
| `na_nasb_reads_vowel` | نا المتكلّمين: يلحق ما آخرُه متحرّك. | مدقَّق | propext, Classical.choice, Quot.sound |
| `ta_person` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `ta_after_vowel_not_subject` | والتاءُ بعد متحرّكٍ ليست تاءَ الفاعل. | مدقَّق | propext |
| `ya_ambiguous` | الياءُ الساكنة بعد كسرٍ: مخاطبةٌ أو متكلّمٌ — الخانةُ لا تفصل. | — | — |
| `noAdj_append` | الإلحاقُ يحفظ الترخيص إن كان الموصولُ مرخَّصًا والملحَقُ لا يبدأ بساكنٍ بعد ساكن. | — | — |
| `attach_licensed` | الإلحاقُ يحفظ الترخيص إن كان الموصولُ مرخَّصًا والملحَقُ لا يبدأ بساكنٍ بعد ساكن. | مدقَّق | propext |
| `witness_na_roles` | — | مدقَّق | propext |
| `witness_ta_persons` | — | مدقَّق | propext |
| `witness_iyya` | — | مدقَّق | propext |
| `damair_licensed` | — | مدقَّق | propext |
| `damair_nodup` | — | مدقَّق | لا مسلّمات |
| `allForms_count` | — | — | — |

### `Slge/Nida.lean` — 9 مبرهنة (`Slge.Nida`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `tanwin_never_bina` | التنوينُ لا يجامع البناء. | مدقَّق | propext |
| `damm_is_bina` | الضمُّ في الآخر بلا تنوينٍ بناءٌ أبدًا (ما لم يكن قبله واوٌ ساكنةٌ فنون: جمعٌ سالم). | مدقَّق | propext |
| `ya_junction` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `noAdj_two_sukun` | — | — | — |
| `nudba_not_binary_licensed` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `particles_licensed` | — | مدقَّق | propext |
| `particles_nodup` | — | مدقَّق | لا مسلّمات |
| `particles_count` | — | — | — |
| `witnesses_hukm` | — | مدقَّق | propext |

### `Slge/Zuruf.lean` — 12 مبرهنة (`Slge.Zuruf`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `lastOf_setLast` | — | — | — |
| `hukm_qat` | — | مدقَّق | propext |
| `hukm_mudaf` | — | مدقَّق | propext |
| `hukm_jarr` | — | مدقَّق | propext |
| `map_isSukun_setLast` | حالاتُ السكون لا تتغيّر بتبديل حركةٍ بحركة، فالترخيصُ محفوظ. | — | — |
| `licensed_of_map_isSukun` | حالاتُ السكون لا تتغيّر بتبديل حركةٍ بحركة، فالترخيصُ محفوظ. | — | — |
| `setLast_licensed` | حالاتُ السكون لا تتغيّر بتبديل حركةٍ بحركة، فالترخيصُ محفوظ. | مدقَّق | propext, Quot.sound |
| `forms_licensed` | — | مدقَّق | propext |
| `forms_count` | — | — | — |
| `forms_hukm` | — | مدقَّق | propext |
| `constants_single` | — | مدقَّق | propext |
| `haythu_always_cut` | حَيْثُ مقطوعةٌ أبدًا: حكمُها الضمّ. | مدقَّق | propext |

### `Slge/Zaman.lean` — 12 مبرهنة (`Slge.Zaman`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `tanwin_vs_qat` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `lastOf_append_singleton` | — | — | — |
| `initOf_append_singleton` | — | — | — |
| `hukm_rafTanwin` | — | مدقَّق | propext |
| `hukm_nasbTanwin` | — | مدقَّق | propext |
| `forms_count` | — | — | — |
| `forms_licensed` | — | مدقَّق | propext |
| `forms_nodup` | — | مدقَّق | propext |
| `forms_hukm` | — | مدقَّق | propext |
| `constants_licensed` | — | مدقَّق | propext |
| `constants_states` | — | مدقَّق | propext |
| `al_amsu` | — | مدقَّق | propext |

### `Slge/Adad.lean` — 15 مبرهنة (`Slge.Adad`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `setLast_setLast` | — | — | — |
| `fem_is_masc_without_ta` | — | مدقَّق | propext |
| `genderOf_masc` | — | مدقَّق | propext |
| `genderOf_fem_forms` | صورُ المؤنّث المودَعة كلُّها تُقرأ مؤنّثةً — ومنها سِتُّ بتائها الأصليّة. | مدقَّق | propext |
| `shin_law` | — | مدقَّق | propext |
| `compound_both_fatha` | — | مدقَّق | propext |
| `twelve_case` | — | مدقَّق | propext |
| `v27` | — | — | — |
| `uqud_case` | — | مدقَّق | propext |
| `tamyiz_ranges` | — | مدقَّق | propext |
| `forms_count` | — | — | — |
| `forms_licensed` | — | مدقَّق | propext |
| `forms_nodup` | — | مدقَّق | propext |
| `ten_single_opposes` | — | مدقَّق | propext |
| `six_ta_is_radical` | — | مدقَّق | propext |

### `Slge/Sarf.lean` — 7 مبرهنة (`Slge.Sarf`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `jarr_eq_nasb` | — | مدقَّق | propext |
| `sarf_jarr_ne_nasb` | — | مدقَّق | propext |
| `al_jarr_kasra` | — | مدقَّق | propext, Quot.sound |
| `idafa_jarr_kasra` | — | مدقَّق | propext |
| `onTemplate_fill` | — | مدقَّق | propext, Quot.sound |
| `witnesses_illa` | — | مدقَّق | propext |
| `muntaha_wf` | — | مدقَّق | propext |

## الدرجة ١٧ — أدواتُ الربط والاستفهام: الخانةُ فالحدُّ فالعمل، والمعنى معلَن

### `Slge/Rawabit.lean` — 7 مبرهنة (`Slge.Rawabit`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `govern_jazm_afal` | الجزمُ على الأفعال الخمسة: حذفُ النون. | مدقَّق | propext |
| `govern_nasb_afal` | الجزمُ على الأفعال الخمسة: حذفُ النون. | مدقَّق | propext |
| `raf_not_governed_jazm` | والرفعُ لا يحمل أثرَ الجزم: النونُ باقية. | مدقَّق | propext |
| `proclitic_keeps_licence` | الحرفُ المتحرّك المتّصل لا يُفسد ترخيصَ ما بعده. | مدقَّق | propext, Quot.sound |
| `particles_count` | — | — | — |
| `particles_licensed` | — | مدقَّق | propext |
| `proclitics_one_vowelled_cell` | كلُّ حرفٍ متّصلٍ خانةٌ واحدةٌ متحرّكة. | مدقَّق | propext |

### `Slge/Istifham.lean` — 15 مبرهنة (`Slge.Istifham`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `caseOf_ayy` | — | مدقَّق | propext |
| `ayy_differs_only_in_state` | — | مدقَّق | propext |
| `madha_is_ma_dha` | — | مدقَّق | لا مسلّمات |
| `man_dha_junction` | — | مدقَّق | propext |
| `amman_is_am_man` | — | مدقَّق | لا مسلّمات |
| `ma_after_jarr` | — | مدقَّق | لا مسلّمات |
| `amma_is_an_ma_idgham` | — | مدقَّق | propext |
| `mimma_is_min_ma_idgham` | — | مدقَّق | propext |
| `idghamNM_length` | الإدغامُ لا يغيّر الطول. | مدقَّق | propext |
| `hamza_prefix_licensed` | الإدغامُ لا يغيّر الطول. | مدقَّق | propext, Quot.sound |
| `forms_count` | — | — | — |
| `forms_licensed` | — | مدقَّق | propext |
| `forms_nodup` | — | مدقَّق | propext |
| `mabni_single_form` | — | مدقَّق | propext |
| `ayy_three_forms` | والمعربُ أَيّ له ثلاث. | مدقَّق | propext |

## الدرجة ١٨ — التوابعُ والنواسخُ والجزم: الحالةُ لا العلامة، وأبوابٌ عمليّتان، وعلاماتٌ ثلاثٌ عمليّاتٌ ثلاث

### `Slge/Tawabi.lean` — 14 مبرهنة (`Slge.Tawabi`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `compatible_symm` | — | مدقَّق | propext |
| `follows_symm` | — | مدقَّق | propext |
| `compatible_refl` | — | — | — |
| `follows_refl` | — | مدقَّق | propext |
| `four_markers_one_case` | — | مدقَّق | لا مسلّمات |
| `follows_khamsa` | — | مدقَّق | propext |
| `v3` | جمعُ المؤنّث السالم: الكسرةُ بعد ألفٍ وتاء نصبٌ أو جرّ لكلّ جذع (مُؤْمِنَاتٍ، الْمُؤْمِنَاتِ). | — | — |
| `caseClass_jam_muannath` | جمعُ المؤنّث السالم: الكسرةُ بعد ألفٍ وتاء نصبٌ أو جرّ لكلّ جذع (مُؤْمِنَاتٍ، الْمُؤْمِنَاتِ). | مدقَّق | propext |
| `nasaq_in_rawabit` | — | مدقَّق | لا مسلّمات |
| `tawkid_words_licensed` | — | مدقَّق | propext |
| `tawkid_case` | كُلُّهُمْ: الحالةُ من الجذع قبل الضمير. | مدقَّق | propext |
| `caseClass_khamsa_raf` | قانونُ الحالة على العمليّات: رفعُ الأسماء الخمسة بالواو رفعٌ عند القارئ، لكلّ جذع. | مدقَّق | propext |
| `khamsa_nasb_unread` | ونصبُها بالألف لا يقرؤه القارئُ العامّ: الألفُ بعد فتحٍ مشتركةٌ مع المقصور (مُوسَى) — المعجمُ يفصل. | مدقَّق | propext |
| `caseClass_uqud_raf` | العقودُ بالواو رفعٌ لكلّ جذعٍ غيرِ فارغ. | مدقَّق | propext |

### `Slge/Nawasikh.lean` — 41 مبرهنة (`Slge.Nawasikh`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `inna_eq_swap_kana` | — | مدقَّق | propext |
| `kada_eq_kana` | — | مدقَّق | propext |
| `laJins_eq_inna` | — | مدقَّق | propext |
| `zanna_both_nasb` | — | مدقَّق | propext |
| `raf_licensed` | — | مدقَّق | propext, Quot.sound |
| `nasb_licensed` | — | مدقَّق | propext, Quot.sound |
| `setLast_eq_append` | تغييرُ الآخر تفكيكٌ: ما قبلَ الآخر ثمّ الآخرُ بحالته الجديدة. | مدقَّق | propext |
| `caseClass_of_last_damm` | ما آخرُه مضمومٌ يُقرأ رفعًا، كائنًا ما كان ما قبله. | مدقَّق | propext |
| `caseClass_raf` | ما آخرُه مضمومٌ يُقرأ رفعًا، كائنًا ما كان ما قبله. | مدقَّق | propext |
| `lastOf_setLast_carrier` | ما آخرُه مضمومٌ يُقرأ رفعًا، كائنًا ما كان ما قبله. | مدقَّق | propext |
| `exists_lastOf` | ما آخرُه مضمومٌ يُقرأ رفعًا، كائنًا ما كان ما قبله. | — | — |
| `caseClass_nasb` | ما آخرُه مضمومٌ يُقرأ رفعًا، كائنًا ما كان ما قبله. | مدقَّق | propext |
| `caseClass_nasb_tanwin` | النكرةُ المنصوبة: فتحٌ فتنوين — تُقرأ نصبًا لكلّ جذع. | مدقَّق | propext |
| `caseClass_raf_tanwin` | النكرةُ المنصوبة: فتحٌ فتنوين — تُقرأ نصبًا لكلّ جذع. | مدقَّق | propext |
| `caseClass_al_raf` | المعرَّفُ بأل مرفوعًا يُقرأ رفعًا: الأداةُ في الصدر لا تمسّ الآخر. | مدقَّق | propext |
| `caseClass_of_last_yin` | ما آخرُه كسرٌ فياءٌ ساكنةٌ فنونٌ مفتوحة: نصبٌ أو جرّ. | مدقَّق | propext |
| `uqud_nasb_compatible` | ُونَ/ِينَ: خبرُ كان جمعًا سالمًا يوافق النصبَ (قانونُ العقود). | مدقَّق | propext |
| `no_tanwin_setLast` | — | مدقَّق | propext, Quot.sound |
| `raf_no_tanwin` | — | مدقَّق | propext, Quot.sound |
| `nasb_no_tanwin` | — | مدقَّق | propext, Quot.sound |
| `hasAl_setLast` | الحركةُ في الآخر لا تُدخل الأداةَ في الصدر. | مدقَّق | propext, Quot.sound |
| `laJins_ism_no_tanwin` | اسمُ لا النافية للجنس: فتحٌ بلا تنوينٍ ولا أداة (نكرةٌ)؛ والفتحُ يُقرأ نصبًا. | مدقَّق | propext, Quot.sound |
| `kana_licensed` | — | مدقَّق | propext |
| `kada_licensed` | — | مدقَّق | propext |
| `inna_licensed` | — | مدقَّق | propext |
| `zanna_licensed` | — | مدقَّق | propext |
| `counts` | — | مدقَّق | لا مسلّمات |
| `jaala_shared` | جَعَلَ في بابين: الخانةُ واحدةٌ والمعنى (الشروع/التحويل) يفصل. | مدقَّق | لا مسلّمات |
| `inna_in_rawabit` | الستّةُ كلُّها في جدول أدوات الربط بعملها `nasbIsm` — سُدِّد الدَين (كَأَنَّ ولَيْتَ). | مدقَّق | لا مسلّمات |
| `laysa_la_ma_in_rawabit` | لَيْسَ ولَا ومَا في جدول أدوات الربط بلا عملٍ مسجَّل: عملُها عملُ كان قانونُ تيار. | مدقَّق | لا مسلّمات |
| `kaffa_licensed` | — | مدقَّق | propext |
| `kaffa_forms` | — | مدقَّق | لا مسلّمات |
| `kaffa_forms_licensed` | — | مدقَّق | propext |
| `innama_kaffa_in_rawabit` | جدولُ أدوات الربط: إِنَّ تنصب الاسم، وإِنَّمَا بلا عمل — الكفُّ مسجَّلٌ في الجدول. | مدقَّق | لا مسلّمات |
| `laytama_cells` | لَيْتَمَا يجوز فيها الإعمال: الكفُّ قرارُ تيارٍ لا خانة (الخانةُ واحدة). | — | — |
| `kada_khabar_raf` | — | مدقَّق | propext |
| `an_licensed` | — | مدقَّق | propext |
| `an_in_rawabit` | — | مدقَّق | لا مسلّمات |
| `an_khabar_nasb` | — | مدقَّق | propext |
| `kana_inna_witness` | — | مدقَّق | propext |
| `la_rayb_witness` | — | مدقَّق | propext |

### `Slge/Jazm.lean` — 21 مبرهنة (`Slge.Jazm`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `noAdj_append_two_sukun` | — | مدقَّق | propext |
| `sukun_licensed` | السكونُ بعد متحرّكٍ مرخَّص. | مدقَّق | propext |
| `hollow_forced` | السكونُ بعد مدٍّ غيرُ مرخَّص: حذفُ عين الأجوف ملزَم. | مدقَّق | propext, Classical.choice, Quot.sound |
| `dropWeak_licensed` | السكونُ بعد مدٍّ غيرُ مرخَّص: حذفُ عين الأجوف ملزَم. | مدقَّق | propext |
| `dropWeak_last` | بعد الحذف يبقى الآخرُ بحركة الأصل — لا سكونَ يُقرأ. | مدقَّق | propext |
| `weak_witnesses` | — | مدقَّق | propext |
| `yaqulu_sukun_unlicensed` | — | مدقَّق | propext |
| `yaqul_licensed` | — | مدقَّق | propext |
| `waw_shared` | — | مدقَّق | لا مسلّمات |
| `marker_afal_jazm` | — | مدقَّق | propext |
| `afal_jazm_eq_nasb` | الجزمُ والنصبُ في الخمسة صورةٌ واحدة: الأداةُ تفصل. | مدقَّق | propext |
| `marker_witnesses` | — | مدقَّق | لا مسلّمات |
| `tools_licensed` | — | مدقَّق | propext |
| `counts` | — | مدقَّق | propext |
| `amr_licensed` | — | مدقَّق | propext, Quot.sound |
| `yunfiq_witness` | — | مدقَّق | propext |
| `shared_la_lamma` | لَا الناهيةُ ولَا النافية، ولَمَّا الجازمةُ والحينيّة: خانةٌ واحدة — الحكمُ من الفعل بعدها. | مدقَّق | propext |
| `shared_istifham` | سبعةٌ من أسماء الشرط خاناتُها خاناتُ الاستفهام. | مدقَّق | propext |
| `ayy_declines` | أَيّ وحدَها معربة: ثلاثُ صورٍ بثلاث حركات. | مدقَّق | propext |
| `rawabit_jazm` | جدولُ أدوات الربط: الجوازمُ كلُّها فيه بعملها (لَمْ لَمَّا وأدواتُ الشرط الجازمة الاثنتا عشرة)، وغيرُ | مدقَّق | propext |
| `two_verbs` | الجزمُ بفعلين: حكمُ كلٍّ منهما حكمُ الواحد. | مدقَّق | propext |

### `Slge/Mansubat.lean` — 20 مبرهنة (`Slge.Mansubat`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `tamyiz_eq_hal` | — | مدقَّق | propext |
| `nakira_reads_nasb` | — | مدقَّق | propext |
| `nakira_has_tanwin` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `nakira_licensed` | — | مدقَّق | propext, Quot.sound |
| `derived_of_bare` | — | مدقَّق | propext |
| `derived_witnesses` | شواهدُ البوّابة: صَافَّاتٍ (فكٌّ فإسقاط)، مُبْصِرَةً (ـَة)، خَالِدِينَ (ـِين)، بَيْضَاءَ (فَعْلَاء)، | مدقَّق | propext |
| `sorting_by_template` | — | مدقَّق | propext |
| `derived_templates_wf` | — | مدقَّق | propext |
| `adad_tamyiz_is_nakira` | تمييزُ العدد 11–99: الحالةُ نفسُها (فتحٌ منوَّنٌ مفرد). | مدقَّق | propext, Quot.sound |
| `tahwil_witness` | — | مدقَّق | propext |
| `tamm_muthbat_reads_nasb` | — | مدقَّق | propext |
| `badal_follows` | البدلُ تبعيّةٌ في الحالة: مرفوعٌ بعد مرفوع (المستثنى منه فاعلٌ). | مدقَّق | propext |
| `mufarragh_eq_role` | المفرَّغ: إِلَّا بلا أثرٍ على الخانة؛ العمليّةُ عمليّةُ الموقع. | مدقَّق | propext |
| `tools_licensed` | — | مدقَّق | propext |
| `illa_ghayr_in_rawabit` | — | مدقَّق | لا مسلّمات |
| `ghayr_idafa_jarr` | — | مدقَّق | propext |
| `ghayr_takes_hukm` | — | مدقَّق | propext |
| `ma_khala_nasb` | — | مدقَّق | propext |
| `witnesses` | شواهدُ البوّابة: سُجَّدًا (حال)، شَيْبًا وعُيُونًا وكَوْكَبًا (تمييز) = العمليّةُ على الجذع. | مدقَّق | propext |
| `sukara_hal` | — | مدقَّق | propext |

### `Slge/Majrurat.lean` — 24 مبرهنة (`Slge.Majrurat`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `jarr_licensed` | — | مدقَّق | propext, Quot.sound |
| `caseClass_jarr` | الكسرةُ تُقرأ جرًّا إن لم يكن الآخرُ نونًا (ِينَ قانونُها قانونُ العقود) ولم يكن تاءً بعد ألف | مدقَّق | propext |
| `caseClass_jarr_tanwin` | النكرةُ المجرورة: كسرٌ فتنوين — جرٌّ (أو نصبٌ/جرٌّ في جمع المؤنّث) لكلّ جذع. | مدقَّق | propext |
| `govern_jarr` | النكرةُ المجرورة: كسرٌ فتنوين — جرٌّ (أو نصبٌ/جرٌّ في جمع المؤنّث) لكلّ جذع. | مدقَّق | propext |
| `uqud_jarr_compatible` | — | مدقَّق | propext |
| `caseClass_of_last_ayn` | — | مدقَّق | propext |
| `dual_jarr_compatible` | — | مدقَّق | propext |
| `khamsa_jarr_unread` | الأسماءُ الخمسة بالياء: الياءُ بعد كسرٍ مشتركةٌ مع المنقوص — المعجمُ يفصل. | مدقَّق | propext |
| `mamnu_jarr_reads_nasb` | الممنوعُ من الصرف: فتحٌ يُقرأ نصبًا؛ الجرُّ من جدول العلل. | مدقَّق | propext |
| `masajid_witness` | الممنوعُ من الصرف: فتحٌ يُقرأ نصبًا؛ الجرُّ من جدول العلل. | مدقَّق | propext |
| `harfs_licensed` | — | مدقَّق | propext |
| `harfs_count` | — | مدقَّق | لا مسلّمات |
| `proclitic_jarr_licensed` | المتّصلةُ الخمسةُ لا تُفسد ما بعدها. | مدقَّق | propext, Quot.sound |
| `harfs_in_rawabit` | السبعةَ عشرَ كلُّها في جدول أدوات الربط: ستّةَ عشرَ جارّةً، وواوُ القسم خانةُ واو العطف (بلا عمل في | مدقَّق | لا مسلّمات |
| `qasam_witness` | تَاللَّهِ ووَاللَّهِ: شاهدا بوّابة؛ التاءُ مختصّةٌ بلفظ الجلالة (معلَن). وتَاللَّهِ (مدٌّ قبل لامٍ | مدقَّق | propext |
| `rubba_nakira` | رُبَّ تجرّ النكرات: النكرةُ المجرورةُ تحمل التنوين لكلّ جذع. | مدقَّق | propext, Classical.choice, Quot.sound |
| `mudaf_no_tanwin` | المضافُ لا تنوينَ له (قانونُ حسم المضاف): إسقاطُ التنوين عمليّةٌ قبل الإلحاق. | مدقَّق | propext, Quot.sound |
| `mudaf_drops_nun` | — | مدقَّق | propext |
| `muhandisu_witness` | مُهَنْدِسُو الشَّرِكَةِ: شاهدُ الحصر عمليّةً. | مدقَّق | propext |
| `lafziyya_by_template` | الإضافةُ اللفظيّة: المضافُ مشتقٌّ على قالبٍ (صَانِعُ الْمَعْرُوفِ)؛ والمعنويّة: المضافُ جامد | مدقَّق | propext |
| `mudaf_marifa` | المضافُ إلى معرفةٍ معرفةٌ (الإضافةُ المحضة): المضافُ إلى ضميرٍ في `Marifa`. | مدقَّق | propext |
| `tabi_jarr_follows` | — | مدقَّق | propext |
| `an_kasra_shared` | المفردُ المختومُ بألفٍ ونونٍ مجرورًا (إِيمَانِ، شَيْطَانِ) والمثنّى المرفوعُ (رَجُلَانِ): خانةٌ واحدة — القارئُ | مدقَّق | لا مسلّمات |
| `rajul_salih` | بِرَجُلٍ صَالِحٍ: نكرتان مجرورتان منوَّنتان تتبع إحداهما الأخرى. | مدقَّق | propext |

### `Slge/Wasl.lean` — 19 مبرهنة (`Slge.Wasl`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `no_initial_sukun` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `wasl_licenses` | همزةُ الوصل تُرخِّص الابتداءَ بالساكن. | مدقَّق | propext, Quot.sound |
| `wasl_drops` | في الوصل تسقط الهمزةُ ويتّصل الساكنُ بما قبله متحرّكًا. | مدقَّق | propext |
| `wasl_after_sukun` | وبعد ساكنٍ لا تُقبل: ساكنان — كسرةُ التقاء الساكنين قانونُ الحدّ في الغانم. | مدقَّق | propext, Classical.choice, Quot.sound |
| `qat_stays` | القطعُ يبقى: همزةٌ متحرّكةٌ بعد أيّ آخر. | مدقَّق | propext, Quot.sound |
| `quick_test` | — | مدقَّق | propext |
| `wasl_qat_cells_shared` | — | مدقَّق | propext |
| `templates_partition` | — | مدقَّق | propext, Quot.sound |
| `templates_wf` | — | مدقَّق | propext |
| `ten_licensed` | — | مدقَّق | propext |
| `ten_count` | — | مدقَّق | لا مسلّمات |
| `ten_shape` | كلُّها همزةٌ متحرّكةٌ فساكن: شكلُ الوصل. | مدقَّق | propext |
| `illa_not_wasl` | إِلَّا على اِفْعَلْ بجذر ل‑ل‑ا: القالبُ يقبلها والألفُ الأصلُ تردّها — فلا تُقرأ وصلًا. | مدقَّق | propext |
| `kind_witnesses` | شواهد: اِقْرَأْ (بوّابة)، اِنْطَلَقَ، اِسْتَخْرَجَ، اِنْطِلَاق وصلٌ؛ أَكْرَمَ، إِكْرَام، أَبْنَاءَ (بوّابة) قطعٌ؛ أَخَذَ | مدقَّق | propext |
| `template_reads_what_cells_cannot` | القالبُ يقرأ الوصلَ من القطع حيث الخانةُ لا تقرؤه: اِنْطِلَاق وإِكْرَام. | مدقَّق | propext |
| `plural_qat` | جمعُهما قطعٌ: أَسْمَاء وأَبْنَاء على أَفْعَال؛ والمفردان وصلٌ بالسماع (الجدول قبل القالب). | مدقَّق | propext |
| `bism_witness` | بِسْمِ: الحرفُ المتّصل + الجذعُ بعد إسقاط الهمزة، مجرورًا — بشهادة البوّابة بلا بقيّة. | مدقَّق | propext |
| `istifham_al_witness` | — | مدقَّق | propext |
| `istifhamVerb_licensed` | — | مدقَّق | propext |

### `Slge/Ism.lean` — 15 مبرهنة (`Slge.Ism`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `thulathi_ten` | — | مدقَّق | propext |
| `thulathi_wf` | — | مدقَّق | propext |
| `thulathi_licensed` | العشرةُ مرخَّصةٌ لكلّ جذر: الحالاتُ ثابتةٌ لا ساكنَ في الأوّل ولا ساكنان. | مدقَّق | propext, Quot.sound |
| `thulathi_read` | — | مدقَّق | propext |
| `witnesses_read` | — | مدقَّق | propext |
| `rubai_shapes` | الحصرُ يعدّ ستّةً ويسمّي فَعْلَل مرّتين: الأشكالُ خمسة. | مدقَّق | propext |
| `khumasi_shapes` | الحصرُ يعدّ ستّةً ويسمّي فَعْلَل مرّتين: الأشكالُ خمسة. | مدقَّق | propext |
| `tasghir_licensed` | — | مدقَّق | propext, Quot.sound |
| `tasghir_read` | — | مدقَّق | propext |
| `tasghir_witnesses` | رُجَيْل من رَجُل، دُرَيْهِم من دِرْهَم، عُصَيْفِير من عُصْفُور؛ وبُنَيَّ (بوّابة) بياءٍ مشدّدة: ياءُ التصغير | مدقَّق | propext |
| `nisba_licensed` | النسبُ بعد التهيئة يحفظ الترخيص إذا كان المهيَّأُ مرخَّصًا وآخرُه متحرّكًا. | مدقَّق | propext, Quot.sound |
| `nisba_read` | — | مدقَّق | propext, Classical.choice, Quot.sound |
| `nisba_witnesses` | شواهد: مِصْرِيّ (مِصْرَ بوّابة)، مَكِّيّ، عَصَوِيّ، مُصْطَفِيّ، عَمَوِيّ، قَاضِيّ؛ وعَرَبِيٌّ بشهادة البوّابة. | مدقَّق | propext |
| `arid_bina` | الأربعةُ عمليّاتٌ على الآخر بحالةٍ ثابتة: ضمُّ المنادى، فتحُ اسم لا، ضمُّ المقطوع، فتحُ المركّب. | مدقَّق | propext |
| `lazim_deposited` | اللازمُ: جداولُ صورٍ مودَعةٍ (الضمائر، الإشارة، الاستفهام، الشرط) لا عمليّةَ على آخرها. | مدقَّق | propext |

### `Slge/Fil.lean` — 24 مبرهنة (`Slge.Fil`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `abwab_six` | — | مدقَّق | propext |
| `bab_wf` | — | مدقَّق | propext |
| `bab_licensed` | — | مدقَّق | propext, Quot.sound |
| `bab_read` | — | مدقَّق | propext |
| `bab_witnesses` | شواهدُ البوّابة: ضَرَبَ–يَضْرِبُ، فَتَحَ–يَفْتَحُ (ح حلقيّة)، فَرِحَ–يَفْرَحُ؛ ويَنْصُرُ وحَسِبَ. | مدقَّق | propext |
| `bab3_condition_witness` | شواهدُ البوّابة: ضَرَبَ–يَضْرِبُ، فَتَحَ–يَفْتَحُ (ح حلقيّة)، فَرِحَ–يَفْرَحُ؛ ويَنْصُرُ وحَسِبَ. | مدقَّق | propext |
| `mazid_counts` | — | مدقَّق | propext |
| `amr_of_pres` | أمرُ المزيد من مضارعه بالقاعدة نفسِها التي تُخرج أمرَ المجرّد (`Shabaka.edges` 8–10): سبعةٌ بالقاعدة وحدَها؛ ويُفْعِلُ ب | مدقَّق | propext, Quot.sound |
| `amr_ifalla_unlicensed` | أمرُ اِفْعَلَّ بالقاعدة اِفْعَلْلْ: ساكنان، غيرُ مرخَّصٍ ثنائيًّا (كجزمه) — فكُّ الإدغام أو الفتحُ | مدقَّق | propext |
| `rubai_shapes` | — | مدقَّق | propext |
| `root_is_ternary` | جذرُ `Wazn` ثلاثيٌّ بالبناء: لا خماسيَّ الأصول. | مدقَّق | لا مسلّمات |
| `qalb_witness` | — | مدقَّق | propext |
| `naql_witness` | — | مدقَّق | propext |
| `qalb_licensed` | القلبُ يحفظ الترخيص إذا كان ما بعد الألف متحرّكًا. | مدقَّق | propext, Classical.choice, Quot.sound |
| `naql_licensed` | النقلُ يحفظ الترخيص بعد حرفٍ متحرّك: المعتلُّ كان متحرّكًا فلا يجتمع ساكنان. | مدقَّق | propext, Classical.choice, Quot.sound |
| `hadhf_witness` | الحذفُ ملزَم: يَقُولُ مجزومًا — السكونُ بعد المدّ غيرُ مرخَّصٍ (`Jazm.hollow_forced`) فيُحذف. | مدقَّق | propext |
| `ibdal_map_isSukun` | — | مدقَّق | propext |
| `ibdal_licensed` | — | مدقَّق | propext |
| `ibdal_witnesses` | اِصْطَبَرَ، اِزْدَهَرَ، اِتَّصَلَ، اِتَّخَذَ (الهمزةُ فاءً كالواو والياء — دَينٌ سُدِّد)؛ وبشهادة البوّابة اصْطَفَى | مدقَّق | propext |
| `idgham_licensed` | الإدغامُ يحفظ الترخيصَ إذا كان الأوّلُ متحرّكًا (ما قبل العين لا يكون ساكنًا في الماضي). | مدقَّق | propext, Classical.choice, Quot.sound |
| `qalb_pastT` | الأجوفُ على فَعَلَ بعد القلب: [ف، ا، ل] لكلّ جذرٍ عينُه واوٌ أو ياء. | مدقَّق | propext |
| `idgham_pastT` | المضعَّفُ على فَعَلَ بعد الإدغام: [ف، عْ، ع] لكلّ جذرٍ عينُه لامُه. | مدقَّق | propext |
| `readers_witnesses` | قَالَ وجَاءَ يُقرآن أجوفين (ق‑؟‑ل، ج‑؟‑ء)؛ رَدَّ ومَدَّ مضعَّفين، وما قُرئ يُردّ بالعمليّة بعينه. | مدقَّق | propext |
| `kada_eleven` | هذا الحصرُ يعدّ كاد أحدَ عشرَ (بلا هَبَّ): العشرةُ المشتركةُ في `Nawasikh.kadaSisters`. | مدقَّق | لا مسلّمات |

### `Slge/Huruf.lean` — 8 مبرهنة (`Slge.Huruf`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `counts` | — | مدقَّق | لا مسلّمات |
| `table_licensed` | — | مدقَّق | propext |
| `no_tanwin` | لا تنوينَ في حرف؛ وما نونُه أصلٌ ساكنٌ بعد حركةٍ يقرؤه `Nida.hasTanwin` تنوينًا — بالاسم. | مدقَّق | propext |
| `proclitics_keep_licence` | المتّصلةُ (خانةٌ واحدةٌ متحرّكة) لا تُفسد ما بعدها. | مدقَّق | propext, Classical.choice, Quot.sound |
| `shared_cells` | 68 مدخلًا على 53 صورة؛ لَا ووَ أربعًا، حَتَّى ولِ ثلاثًا، إِنْ وفَ اثنين. | مدقَّق | لا مسلّمات |
| `amal_is_operation` | العملُ عمليّةٌ على ما بعد الحرف: مجرورٌ بعد الجارّ، منصوبُ الاسم بعد المشبّهة، منصوبُ المضارع | مدقَّق | propext |
| `rawabit_agrees` | كلُّ عاملٍ في جدول أدوات الربط اسمُه في هذا الجدول له مدخلٌ بعملِه نفسِه — إلّا مَا: شرطيّةً اسمٌ | مدقَّق | propext |
| `sawfa_witness` | التنفيسُ بلا أثر: سَيَقُولُ (بوّابة) = سَ + يَقُولُ، وسَوْفَ مودَعة. | مدقَّق | propext |

## الدرجة ١٩ — المعرفةُ والترجيح: الإنتاجُ والتعارضُ وقطعيُّ الدلالة

### `Slge/Ghazali.lean` — 4 مبرهنة (`Slge.Ghazali`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `ghazali_table` | **الجدولُ نتيجة:** المنتِجُ بالبتات هو المنتِجُ عند الغزالي، خانةً خانة. | مدقَّق | propext |
| `barren_witnessed` | **العقمُ مشهود:** في الصورتين العقيمتين من الأخصّ نموذجان مقبولان تختلف فيهما | مدقَّق | لا مسلّمات |
| `akhass_chain` | **الموافقةُ سلسلة:** الأخصُّ متعدٍّ، فـ«أفّ ⇒ أذى ⇒ محرَّم» تنتج «أفّ ⇒ محرَّم». | مدقَّق | لا مسلّمات |
| `licence_makes_mafhum` | **الرافعُ إلى المساواة يُنتج:** إذا قام دليلٌ على أنّ العلّةَ واحدة (الأخصُّ صار | مدقَّق | لا مسلّمات |

### `Slge/Rank.lean` — 11 مبرهنة (`Slge.Rank`)

| المبرهنة | ما تقول | التدقيق | المسلّمات |
|---|---|---|---|
| `pathGrade_qati_iff` | — | مدقَّق | propext, Quot.sound |
| `no_promotion` | **لا ترقية:** ظنّيٌّ واحدٌ في الطريق يجعله ظنّيًّا. | مدقَّق | propext, Quot.sound |
| `weigh_swap` | — | مدقَّق | propext, Quot.sound |
| `qati_never_loses` | — | مدقَّق | propext |
| `mardud_iff` | — | مدقَّق | propext |
| `tanaqud_iff` | — | مدقَّق | propext |
| `taadul_iff` | — | مدقَّق | propext, Quot.sound |
| `specific_wins` | — | مدقَّق | propext |
| `general_is_makhsus` | — | مدقَّق | propext |
| `qati_general_yields_to_zanni_specific` | **الخصوصُ مقدَّمٌ على الثبوت:** عامٌّ قطعيٌّ يعارضه خاصٌّ ظنّيٌّ فيُعمل بالظنّيّ. | مدقَّق | propext |
| `same_scope_is_weigh` | وبلا خصوصٍ يرجع الوزنُ إلى `weigh` بعينه. | مدقَّق | propext |

