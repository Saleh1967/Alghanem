# ADR ٦٢ — قفلُ الدالّ وحده: `Qufl.dal_locked`، والواجهةُ مجمَّدةٌ باسم `dal-v1` (أمرُ المالك «اقفل الدالّ ووثّق»، 2026-10-14)

**الحال:** مقبول. **ينفّذ** البندين ١ و٤ من ADR ٦٠، ويسدّ `DAL_LOCK_NOT_PROVEN`.

## ١. ما القفل

القفلُ ثلاثةُ أشياء، لا إعلان:

1. **مبرهنةٌ** في `formal/a116/A116/Qufl.lean` تجمع دفترَ الدالّ بوظائفه الستّ على حدّه الممدود.
2. **واجهةٌ مجمَّدة** باسم `gate.DAL_LOCK = "dal-v1"`، مرآتُها المكتوبةُ باليد في `tests/test_qufl.py::FROZEN`.
3. **فرزُ الديون** بالمراحل الثلاث (§٤)، فلا يبقى في الغانم دَينٌ مفتوحٌ من غير مرحلته إلّا مسمًّى بمقرّه.

## ٢. المبرهنة

الدفترُ `Qufl.locked d` لكلّ درجة d:

| الوظيفة | السند | حدُّه |
|---|---|---|
| ترميز، إملاء، صوت | `Exhaust.tarmizAt`، `imlaAt`، `sawtAt` | كما في `Exhaust.current` |
| اشتقاق | `Qufl.ishtiqaqLocked`: `Ledger.ishtiqaqAt` **و** `Tasrif.madi_exhausted`، `mudari_exhausted`، `amr_exhausted` **و** `Rubai.rubai_licensed` **و** `Neutral.weak_licensed` | القوالبُ الصحيحة؛ **وكلُّ جذرٍ ثلاثيٍّ بلا ألف** (صحيحٌ، معتلٌّ، مهموز، مضعّف) في الماضي بأبوابه والمضارع بحروفه وإعرابه والأمر؛ **وكلُّ جذرٍ رباعيٍّ بلا ألف** بأبنيته الستّ؛ والمعتلُّ بالمحايد على الجذور المرجعيّة |
| صرف | `Qufl.sarfLocked`: `Ledger.sarfAt` **و** `Tasrif.madd_drop_forced` **و** `haa_forced` | حالةُ الآخر بقالبه؛ وما يُلزمه القانونُ في المعتلّ: حذفُ المدّ في مجزوم الأجوف، وهاءُ السكت |
| نحو | `Ledger.mahallAt` | موضعُ العلامة الأخير، والوقفُ يمحوها |
| دلالة | `.muallaq "DALALA_AT_DAL_MADLUL_BRIDGE"` | **منفذُ جسر** إلى المرحلة الثالثة، لا دَينٌ على الغانم |

**المبرهن** (ثلاثَ عشرةَ مبرهنةً في `Audit.lean`؛ المدقَّق 787 ← **800**؛ المسلّماتُ propext وClassical.choice وQuot.sound):

* `locked_six_qaim`، `locked_qaim_count`: الستُّ قائمةٌ في كلّ درجة، ستٌّ من سبع.
* `locked_extends_filled`: لا شيءَ نُقص عن `Ledger.filled`.
* `locked_stops_at_one`، `dalala_alone_opens`: بقانون الاستنفاد يقف الدفترُ عند الدرجة الأولى، والدلالةُ وحدَها تفتح.
* `locked_beyond_sahih`: على شواهد الصفات الستّ (كتب، وعد، قول، رمي، ءخذ، مدد) الماضي فَعَلَ مرخَّصٌ وصلًا ووقفًا؛
  و`shawahid_not_all_sahih`: خمسةٌ منها لا يبلغها `Tasrif.every_position` المشروطُ بالصحيح. هذا هو الامتداد.
* `locked_quad`: دَحْرَجَ على فَعْلَلَ مرخَّص، والبوّابةُ بعدد الأصول مفتوحةٌ للرباعيّ (`Rubai.quad_open_by_maqayis`).
* `dal_locked`: الجامع.
* `sijill_outside_lock`: سجلُّ الملفّات يقف عند الصفر بدليله، ودفترُ الدالّ مرخَّصٌ في الدرجة الأولى — فالسجلُّ خارج الحدّ.

**المطابَق:** `qufl.csv` يطبعه Lean (28 صفًّا للدفتر و7 شواهد) ويُودَع ويُطابَق في CI؛ و`tests/test_qufl.py` يكتب صفوفَه باليد،
ويمرّر كلماتِ المصحف (كَتَبَ، وَعَدَ، قَالَ، رَمَى، أَخَذَ) على `gate.enter` فتُقارن ذرّاتُها بالجدول، ويحكم في ما ليس في
المجال (مَدَّ، دَحْرَجَ) بمرآة الترخيص المستقلّة `gate.licence` لا بـLean؛ طفراتُه `MUTANT_DALALA_QAIM`، `MUTANT_SAHIH_ONLY`،
`MUTANT_SIGNATURE_DRIFT`.

## ٣. الواجهةُ المجمَّدة (`dal-v1`)

`gate.DAL_LOCK = "dal-v1"`، و`test_interface_frozen` يطابق توقيعاتِ `enter`، `exit`، `derive`، `recover`، `licence`
وحقولَ `Certificate` و`Refusal` و`Context` بما كُتب باليد في `FROZEN`. تغييرُ أيٍّ منها بعد اليوم ADR موسومٌ بكسر
الواجهة، يرفع `DAL_LOCK` ويرفع التثبيتَ في المستودعات المستهلِكة (SLGE `GATE_REV`، Algebra `lakefile`) معًا.
والبروتوكولُ `A116-CANONICAL-TXT-1.1` كما هو. والوسمُ `dal-v1` على إيداع هذا الـADR في `claude/official-gate`، بلا دمج.

## ٤. فرزُ الديون المفتوحة بالمراحل

تُفرز الديونُ المسمّاة في CLAUDE.md وأقسامِ «ما بقي باسمه» في ADR ١–٦١. أسماءُ الرفض والثوابتُ والطفراتُ ليست ديونًا.

**(أ) من الدالّ وحده — داخل القفل، تبقى هنا:**

| الدَّين | حالُه بعد القفل |
|---|---|
| `IFANLALA_WITHOUT_SEALED_VOWELS` | رفضٌ مسمًّى لا دَين: افْعَنْلَلَ بلا شاهدٍ مشكول، والبوّابةُ لا تخمّن |
| `VI_TA_IDGHAM_NOT_IN_TABLE`، `WASL_LAM_ARTICLE_VS_ROOT` | فجوتا جدولٍ في الأوزان؛ علاجُ الثانية في الفعل قائم (`Mudari.waslVerb_ne_fatha`) وفي الاسم مفتوح |
| `MIZAN_INTERPRETER_UNPROVEN` | المفسِّرُ على جدول الميزان مطابَقٌ على `hadd-join` كلِّه، غيرُ مبرهَن |
| `MADD_AL_FARQ_OUTSIDE_NIZAM`، `ILTIQA_AS_INTIQAL_UNPROVEN`، `JOIN_AS_NIZAM_UNPROVEN`، `LIFT_WAQF_UNPROVEN`، `NAHW_GROUPING_NOT_WRITTEN`، `DEPTH_CONDITION_NOT_WRITTEN` | ديونُ نظام الأنظمة؛ لا تمسّ الوظائف الستّ |
| `CASE_NEEDS_AMIL`، `AMIL_BEYOND_ATTACHED`، `MAMNU_UNDETECTED`، `QISM_ORACLE`، `ALAM_SECOND_BY_LENGTH` | العاملُ خارج الكلمة المتّصلة: مرجعُه النحّاسُ والعكبري بالختم التجريبيّ (ADR ٦١) بتسجيلٍ مسبق |
| `HAA_SAKT_PAUSE`، `MA_ZAIDA`، `ZAIDA_BA_MIN`، `NOMINAL_NUMBER_SUFFIXES`، `TANITH_ALIFS`، `PEEL_TAKES_RADICAL`، `SAWABIQ_BEFORE_IMPERFECT`، `SAWABIQ_BEFORE_NOUNS`، `RECOVER_IS_VERB_ONLY`، `QUAD_ROOT_NOT_RECOVERED` | الاسترجاعُ: مقيسٌ على مراجعَ محجوبة، وتحسينُه لا يغيّر الواجهة |
| `SIJILL_IN_LOCK_SCOPE_UNDECIDED` | **حُسم مؤقّتًا بـ`sijill_outside_lock`**: سجلُّ الملفّات خارج الحدّ، لأنّه سجلُّ شجرةٍ لا قانونُ الدالّ؛ ويبقى لك ردُّه |
| `KEYS_DISTINCT_CHECKED_NOT_PROVEN`، `CVVC_PAUSE_UNCHANGED`، `JUNCTION_SHORTENING_NOT_MODELLED`، `MADD_AL_FARQ_SOURCE_LOCUS_UNVERIFIED` | قائمة، لا تمسّ القفل |

**(ب) من المدلول وحده — مقرُّها Algebra (ADR ٩ هناك):**

`HUKM_MEASUREMENT_IN_SLGE`، `BOOK_HEADING_MISSING`، `MUKHASSAS_MEMBERSHIP_RULE_NOT_REGISTERED`، `MENTIONED_NOT_POSITED`،
`POSITED_MEMBERSHIP_NOT_WRITTEN` — كلُّها عن «المخصَّص» مرجعًا للجنس والقابليّة، وهو مودَعُ المعنى (`MAANA_DEPOSIT_NOT_NAMED` هناك).

**(ج) من الدالّ والمدلول معًا — مقرُّها `dal-madlul-constitution` (ADR ٧ هناك):**

`WAD_QARINA_NOT_TRANSFERRED`، `WAD_QARINA_NOT_DEPOSITED`، `SENSE_LEVEL_NOT_DEPOSITED`، `NARRATOR_INDEPENDENCE_DECLARED`،
`DALLA_MADLUL_PARTITION_UNPROVEN`، `QARINA_NOT_INFORMATIVE`، `CONTEXT_IS_VERSE`، `QARAR_SEAT`، `MANHAJ_REGISTRY_NOT_WRITTEN`،
`JUDGE1_VS_JUDGET`، `TAYY_STEPS_UNLISTED`، `TASLIM_ENCODING_DECLARED`.

**(د) مراجعُ وقياسات — ليست من قانون الدالّ، وتبقى حيث هي:** ديونُ لين (`LANE_*`، `FUULA_*`، `A_OVER_TOO_WIDE`،
`TRANSITIVITY_*`، `WEAK_*`، `HARAKA_SHARE_NOT_MEASURED`، `CITATION_FORM_HOMOGRAPH`)، وديونُ QAC والصحيحين
(`HADITH_ROOT_GOLD_ABSENT`، `SAME_TEXT_AS_MASAQ_DEV`، `PROCLITIC_NOT_STRIPPED`، `MASAQ_SLICES_PRE_ULA_WAW`)، والختمُ التجريبيّ
(`TRIAL_*`).

## ٥. ما بقي باسمه

* `DAL_LOCK_SCOPE_FORMS`: القفلُ على **الصيغ** المبرهنة (الماضي والمضارع والأمر، والأوزان الإحدى والثلاثون على الصحيح،
  وأبنية الرباعيّ الستّ)، لا على كلّ صيغةٍ ممكنة: المزيدُ على المعتلّ خارج `Tasrif` ما زال بالمحايد على الجذور المرجعيّة
  وحدَها (`Neutral.weak_licensed`)، لا على كلّ جذر.
* `SIJILL_IN_LOCK_SCOPE_UNDECIDED`: حُسم مؤقّتًا خارج الحدّ؛ ينتظر لفظَ المالك.
* `TRIAL_ORDER_UNDECIDED`: نُفّذ الختمُ التجريبيّ أوّلًا (ADR ٦١) على الترتيب المقترح؛ الصفحةُ التجريبيّة بعد هذا القفل.
* `DAL_V1_TAG`: الوسمُ يُدفع مع هذا الإيداع؛ إن تعذّر دفعُه قيل ذلك.
