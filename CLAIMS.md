# سجلُّ الأرقام — لا رقمَ بلا مولِّد

مولَّدٌ بـ`python tools/gen_claims.py` باستدعاء كلّ مولِّدٍ مسمًّى في الشجرة؛ لا يُحرَّر باليد، و`--check` يعيد الحسابَ كلَّه في CI ويُسقط البناءَ على أيّ فرق. السطرُ أربعةٌ لا خامسَ لها: الرقم، المولِّد، المودَعاتُ المقروءة (ببصمتها أدناه)، بصمةُ المخرَج كاملًا. مراجعةُ هذا المستودع هي الإيداعُ الحاملُ لهذا الملفّ وشاهدُها تشغيلُ CI. جداولُ Lean يولّدها `lake exe a116-table` في CI وتُطابَق بايتًا بايتًا بالإيداع المسجَّل هنا.

## المودَعات ببصماتها

| المودَع | النوع | sha256 |
|---|---|---|
| `corpora/quran-simple-enhanced.txt` | واقع مختوم (`CORPUS_SHA256`) | `37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a` |
| `corpora/MASAQ.csv` | مرجع محجوب | `d43d2a813afbe0490254bb26623d6041ed352a273d333e731ddbcda3bd0b6f3a` |
| `corpora/hadith/sahih_al-bukhari_ahadith_mushakkala_mufassala.utf8.csv.gz` | واقع مختوم (ODbL 1.0؛ بايتاتُه بعد فكّ الضغط) | `b03f661876fc4089520800b9231b57a1564baff734344ea8914494b86e2eb708` |
| `corpora/hadith/sahih_muslim_ahadith_mushakkala_mufassala.utf8.csv.gz` | واقع مختوم (ODbL 1.0؛ بايتاتُه بعد فكّ الضغط) | `79232c8d7c27fef161d8f33ca169f9754741cfe14957dde2ac76893374998943` |
| `corpora/abniya-intiqa-lines.txt` | مجالٌ مختومٌ ثالث: انتقاءُ الأبنية بيد المالك (`ABNIYA_INTIQA_SHA256`، ADR ١٣) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## الأرقام (241 رقمًا من 35 مولِّدًا)

### `gate.audit.main`

يقرأ: `corpora/quran-simple-enhanced.txt`. بصمةُ المخرَج: `1b890308af74daa9`.

| المسار في المخرَج | الرقم |
|---|---|
| `context_transitions.destination_context_unavailable` | 489 |
| `context_transitions.destination_nonready_no_promotion` | 3,560 |
| `context_transitions.successful_reversible_context_transports` | 35,740 |
| `corpus_bytes` | 1,319,901 |
| `distinct_forms` | 18,200 |
| `edition_residue.canonical_forms` | 17,572 |
| `edition_residue.ready_after` | 18,179 |
| `edition_residue.refused_named.INITIAL_SUKUN_WITHOUT_REPAIR` | 3 |
| `edition_residue.refused_named.NOT_CONTINUE_LICENSED_AFTER_REPAIR` | 1 |
| `edition_residue.refused_named.TANWIN_WITH_ANOTHER_HARAKA` | 3 |
| `edition_residue.refused_named.UNVOCALIZED_WORD_IS_NEVER_GUESSED` | 14 |
| `edition_residue.round_trip_failures` | 0 |
| `edition_residue.rules_fired.ASSIM` | 38 |
| `edition_residue.rules_fired.FARIQA` | 1,080 |
| `edition_residue.rules_fired.IDGHAM` | 910 |
| `edition_residue.rules_fired.SHAMSI` | 734 |
| `edition_residue.rules_fired.SUKUN` | 13,060 |
| `edition_residue.rules_fired.TANWIN_ALIF` | 1,119 |
| `edition_residue.rules_fired.ULA_WAW` | 14 |
| `edition_residue.rules_fired.WASL` | 1,945 |
| `edition_residue.rules_fired.WASL_SILENT` | 989 |
| `edition_residue.sealed_surfaces` | 18,200 |
| `exact_recovery_cases` | 26,526 |
| `fiber_size_histograms.joined_continue.1` | 4,725 |
| `fiber_size_histograms.joined_continue.2` | 3 |
| `fiber_size_histograms.joined_pause.1` | 4,683 |
| `fiber_size_histograms.joined_pause.2` | 24 |
| `fiber_size_histograms.start_continue.1` | 8,496 |
| `fiber_size_histograms.start_continue.2` | 18 |
| `fiber_size_histograms.start_pause.1` | 6,912 |
| `fiber_size_histograms.start_pause.2` | 547 |
| `fiber_size_histograms.start_pause.3` | 98 |
| `fiber_size_histograms.start_pause.4` | 40 |
| `fiber_size_histograms.start_pause.5` | 12 |
| `fiber_size_histograms.start_pause.6` | 2 |
| `general_language_closure` | 0 |
| `joined_forms_with_real_left` | 17,343 |
| `largest_fibers.joined_continue.bits` | 1 |
| `largest_fibers.joined_pause.bits` | 1 |
| `largest_fibers.start_continue.bits` | 1 |
| `largest_fibers.start_pause.bits` | 3 |
| `occurrences` | 78,245 |
| `reason_counts.joined_continue.ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL` | 1,231 |
| `reason_counts.joined_continue.HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED` | 10,504 |
| `reason_counts.joined_continue.INITIAL_SUKUN_WITHOUT_REPAIR` | 279 |
| `reason_counts.joined_continue.TANWIN_ATTACHMENT_IS_AMBIGUOUS` | 5 |
| `reason_counts.joined_continue.THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED` | 4,486 |
| `reason_counts.joined_pause.ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL` | 1,231 |
| `reason_counts.joined_pause.FINAL_HARAKA_IS_ABSENT` | 833 |
| `reason_counts.joined_pause.HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED` | 9,671 |
| `reason_counts.joined_pause.INITIAL_SUKUN_WITHOUT_REPAIR` | 279 |
| `reason_counts.joined_pause.TANWIN_ATTACHMENT_IS_AMBIGUOUS` | 5 |
| `reason_counts.joined_pause.THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED` | 4,486 |
| `reason_counts.start_continue.ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL` | 844 |
| `reason_counts.start_continue.HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED` | 6,156 |
| `reason_counts.start_continue.INITIAL_SUKUN_WITHOUT_REPAIR` | 480 |
| `reason_counts.start_continue.TANWIN_ATTACHMENT_IS_AMBIGUOUS` | 3 |
| `reason_counts.start_continue.THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED` | 2,185 |
| `reason_counts.start_pause.ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL` | 844 |
| `reason_counts.start_pause.FINAL_HARAKA_IS_ABSENT` | 866 |
| `reason_counts.start_pause.HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED` | 5,290 |
| `reason_counts.start_pause.INITIAL_SUKUN_WITHOUT_REPAIR` | 480 |
| `reason_counts.start_pause.TANWIN_ATTACHMENT_IS_AMBIGUOUS` | 3 |
| `reason_counts.start_pause.THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED` | 2,185 |
| `short_numbering_cases` | 13,573 |
| `stats.joined_continue.DEFER` | 12,333 |
| `stats.joined_continue.READY` | 4,731 |
| `stats.joined_continue.REJECT` | 279 |
| `stats.joined_continue.codebook_bytes` | 4,092,377 |
| `stats.joined_continue.domain` | 17,343 |
| `stats.joined_continue.exact_roundtrips` | 4,731 |
| `stats.joined_continue.sum_residual_bits_per_ready_form` | 6 |
| `stats.joined_pause.DEFER` | 12,333 |
| `stats.joined_pause.READY` | 4,731 |
| `stats.joined_pause.REJECT` | 279 |
| `stats.joined_pause.codebook_bytes` | 4,054,771 |
| `stats.joined_pause.domain` | 17,343 |
| `stats.joined_pause.exact_roundtrips` | 4,731 |
| `stats.joined_pause.sum_residual_bits_per_ready_form` | 48 |
| `stats.start_continue.DEFER` | 9,188 |
| `stats.start_continue.READY` | 8,532 |
| `stats.start_continue.REJECT` | 480 |
| `stats.start_continue.codebook_bytes` | 2,606,377 |
| `stats.start_continue.domain` | 18,200 |
| `stats.start_continue.exact_roundtrips` | 8,532 |
| `stats.start_continue.sum_residual_bits_per_ready_form` | 36 |
| `stats.start_pause.DEFER` | 9,188 |
| `stats.start_pause.READY` | 8,532 |
| `stats.start_pause.REJECT` | 480 |
| `stats.start_pause.codebook_bytes` | 2,583,556 |
| `stats.start_pause.domain` | 18,200 |
| `stats.start_pause.exact_roundtrips` | 8,532 |
| `stats.start_pause.sum_residual_bits_per_ready_form` | 2,218 |

### `tools/gen_hadith_lines.py::stats`

يقرأ: `corpora/hadith/sahih_al-bukhari_ahadith_mushakkala_mufassala.utf8.csv.gz`، `corpora/hadith/sahih_muslim_ahadith_mushakkala_mufassala.utf8.csv.gz`. بصمةُ المخرَج: `976c5dcfe339dc6e`.

| المسار في المخرَج | الرقم |
|---|---|
| `lines` | 12,370 |
| `markers` | 725,280 |
| `per_book.sahih_al-bukhari_ahadith_mushakkala_mufassala.utf8.csv` | 7,008 |
| `per_book.sahih_muslim_ahadith_mushakkala_mufassala.utf8.csv` | 5,362 |
| `words` | 995,413 |

### `gate.hamza.seat_census`

يقرأ: `corpora/quran-simple-enhanced.txt`. بصمةُ المخرَج: `8810d2fd59bacbe8`.

| المسار في المخرَج | الرقم |
|---|---|
| `by_rule` | 4,107 |
| `miss.ء` | 2 |
| `miss.أ` | 16 |
| `miss.ؤ` | 7 |
| `miss.إ` | 30 |
| `miss.ئ` | 51 |
| `seats` | 4,213 |

### `gate.degrees.attestation`

يقرأ: `corpora/quran-simple-enhanced.txt`. بصمةُ المخرَج: `fce2ff86346c07b7`.

| المسار في المخرَج | الرقم |
|---|---|
| `degrees.1.attested` | 2 |
| `degrees.1.forms` | 64 |
| `degrees.1.table` | 3 |
| `degrees.2.attested` | 12 |
| `degrees.2.forms` | 1,835 |
| `degrees.2.table` | 12 |
| `degrees.3.attested` | 35 |
| `degrees.3.forms` | 6,840 |
| `degrees.3.table` | 48 |
| `degrees.3.unattested.len` | 13 |
| `degrees.4.attested` | 79 |
| `degrees.4.forms` | 6,320 |
| `degrees.4.table` | 192 |
| `degrees.5.attested` | 122 |
| `degrees.5.forms` | 2,531 |
| `degrees.5.table` | 768 |
| `degrees.6.attested` | 111 |
| `degrees.6.forms` | 488 |
| `degrees.6.table` | 3,072 |
| `degrees.7.attested` | 36 |
| `degrees.7.forms` | 95 |
| `degrees.7.table` | 12,288 |
| `degrees.8.attested` | 4 |
| `degrees.8.forms` | 6 |
| `degrees.8.table` | 49,152 |
| `refused_by_gate` | 21 |

### `tests/test_neutral.py::corpus_comparison`

يقرأ: `corpora/quran-simple-enhanced.txt`. بصمةُ المخرَج: `17e229430787a150`.

| المسار في المخرَج | الرقم |
|---|---|
| `gaps.IFTAAL_IBDAL` | 5 |
| `gaps.IMPERATIVE_WEAK_DELETION` | 47 |
| `gaps.ISTAHWADHA_NOT_NEUTRALIZED` | 1 |
| `gaps.LAM_YA_AFTER_KASRA` | 2 |
| `gaps.PASSIVE_WEAK_NOT_NEUTRAL` | 21 |
| `matched` | 295 |
| `matched_by_wazn.len` | 22 |
| `matched_by_wazn.sum` | 295 |

### `tests/test_mudari.py::corpus_comparison`

يقرأ: `corpora/quran-simple-enhanced.txt`. بصمةُ المخرَج: `1c3147f9911e8547`.

| المسار في المخرَج | الرقم |
|---|---|
| `gaps.ALIF_IN_ROOT` | 8 |
| `gaps.HAMZA_DOUBLED_ROOT` | 27 |
| `gaps.RAA_TAKHFIF_OWNER_OVER_GATE` | 1 |
| `gaps.YA_FA_IFTAAL_HOLLOW` | 1 |
| `matched` | 7,621 |
| `matched_by_form.I` | 2,022 |
| `matched_by_form.II` | 703 |
| `matched_by_form.III` | 700 |
| `matched_by_form.IV` | 699 |
| `matched_by_form.V` | 702 |
| `matched_by_form.VI` | 699 |
| `matched_by_form.VII` | 699 |
| `matched_by_form.VIII` | 698 |
| `matched_by_form.X` | 699 |
| `roots` | 703 |

### `gate.mabni_bridge.verb_readings`

يقرأ: `corpora/MASAQ.csv`. بصمةُ المخرَج: `ac473b098cf1934f`.

| المسار في المخرَج | الرقم |
|---|---|
| `by_tag.CV:NOT_GENERATED` | 44 |
| `by_tag.CV:RECOVERED` | 1,783 |
| `by_tag.PV:NOT_GENERATED` | 230 |
| `by_tag.PV:RECOVERED` | 7,894 |
| `by_tag.PV_PASS:NOT_GENERATED` | 17 |
| `by_tag.PV_PASS:RECOVERED` | 532 |
| `most_frequent_not_generated.len` | 40 |
| `not_generated_and_unexplained[0][1]` | 3 |
| `not_generated_and_unexplained[1][1]` | 2 |
| `not_generated_and_unexplained[2][1]` | 1 |
| `not_generated_and_unexplained[3][1]` | 1 |
| `not_generated_and_unexplained[4][1]` | 1 |
| `not_generated_and_unexplained[5][1]` | 1 |
| `not_generated_and_unexplained[6][1]` | 1 |
| `not_generated_by_stem_letters.HAMZATED` | 99 |
| `not_generated_by_stem_letters.SOUND_LETTERS` | 132 |
| `not_generated_by_stem_letters.WEAK` | 60 |
| `not_generated_diagnosis.OBJECT_PRONOUN_TAGGED_AS_SUBJECT_IN_THE_REFERENCE` | 31 |
| `not_generated_diagnosis.ROOT_ABSENT_FROM_THE_DEPOSITED_LEXICON` | 232 |
| `not_generated_diagnosis.SUBJECT_SUFFIX_SPLIT_OFF_BY_THE_REFERENCE` | 18 |
| `not_generated_diagnosis.UNEXPLAINED` | 10 |
| `outcomes.NOT_GENERATED` | 291 |
| `outcomes.RECOVERED` | 10,209 |
| `recovered_by_root_class.DEFECTIVE` | 2,205 |
| `recovered_by_root_class.DOUBLED` | 421 |
| `recovered_by_root_class.HOLLOW` | 2,608 |
| `recovered_by_root_class.SOUND` | 4,975 |
| `roots_absent_from_the_lexicon.len` | 70 |
| `roots_per_recovered_token.1` | 7,974 |
| `roots_per_recovered_token.2` | 1,499 |
| `roots_per_recovered_token.3` | 724 |
| `roots_per_recovered_token.4` | 12 |

### `gate.mabni_bridge.verb_generation_reading`

يقرأ: `corpora/MASAQ.csv`. بصمةُ المخرَج: `30118432cf73d28c`.

| المسار في المخرَج | الرقم |
|---|---|
| `corpus_vs_generated_atoms.before_object_not_compared` | 1,733 |
| `corpus_vs_generated_atoms.same_atoms` | 5,024 |
| `corpus_vs_generated_atoms.surface_DEFER` | 3,452 |
| `fiber_sizes.1` | 248,052 |
| `fiber_sizes.2` | 4,085 |
| `fiber_sizes.3` | 19,526 |
| `fiber_sizes.6` | 164 |
| `generated_forms` | 315,874 |
| `projection.DEFER:ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL` | 90 |
| `projection.READY` | 315,784 |
| `roots` | 770 |

### `gate.mabni_bridge.lexical_generation_reading`

يقرأ: `corpora/MASAQ.csv`. بصمةُ المخرَج: `8fbf58eb31339cd5`.

| المسار في المخرَج | الرقم |
|---|---|
| `fiber_sizes.1` | 169 |
| `fiber_sizes.2` | 5 |
| `forms` | 206 |
| `lemmas` | 142 |
| `projection.DEFER:HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED` | 18 |
| `projection.DEFER:TANWIN_ATTACHMENT_IS_AMBIGUOUS` | 1 |
| `projection.DEFER:THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED` | 8 |
| `projection.READY` | 179 |

### `gate.mabni_bridge.lexical_recognition_reading`

يقرأ: `corpora/MASAQ.csv`. بصمةُ المخرَج: `0563d230c2e77506`.

| المسار في المخرَج | الرقم |
|---|---|
| `Prefix:correct` | 12,267 |
| `Prefix:gold` | 12,276 |
| `Prefix:predicted` | 22,725 |
| `Stem:correct` | 11,229 |
| `Stem:gold` | 11,807 |
| `Stem:predicted` | 11,953 |
| `Suffix:correct` | 9,926 |
| `Suffix:gold` | 10,480 |
| `Suffix:predicted` | 18,976 |
| `words` | 35,048 |
| `words_not_aligned` | 1,165 |

### `lake exe a116-table amr`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `8c2b1db31fae9e20`.

| المسار في المخرَج | الرقم |
|---|---|
| `amr.csv.rows` | 118 |

### `lake exe a116-table counts`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `57afd4b22641c974`.

| المسار في المخرَج | الرقم |
|---|---|
| `counts.csv.rows` | 7 |

### `lake exe a116-table degrees`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `0217e1252456df8d`.

| المسار في المخرَج | الرقم |
|---|---|
| `degrees.csv.rows` | 255 |

### `lake exe a116-table degrees-pause`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `f2aa82b5a52df13a`.

| المسار في المخرَج | الرقم |
|---|---|
| `degrees-pause.csv.rows` | 510 |

### `lake exe a116-table hadd`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `b0d2c362048bc8ff`.

| المسار في المخرَج | الرقم |
|---|---|
| `hadd.csv.rows` | 346,200 |

### `lake exe a116-table hadd-join`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `7332971e50628ff1`.

| المسار في المخرَج | الرقم |
|---|---|
| `hadd-join.csv.rows` | 293,904 |

### `lake exe a116-table hamza`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `5028db66c4fbdd50`.

| المسار في المخرَج | الرقم |
|---|---|
| `hamza.csv.rows` | 384 |

### `lake exe a116-table iltiqa`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `e3ca5a80cfc7cb80`.

| المسار في المخرَج | الرقم |
|---|---|
| `iltiqa.csv.rows` | 360,000 |

### `lake exe a116-table ledger`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `ae0aefbdfd942fd3`.

| المسار في المخرَج | الرقم |
|---|---|
| `ledger.csv.rows` | 31 |

### `lake exe a116-table licensable`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `2a84446370e21995`.

| المسار في المخرَج | الرقم |
|---|---|
| `licensable.csv.rows` | 113 |

### `lake exe a116-table maqayis`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `c33179f6f7f07c4b`.

| المسار في المخرَج | الرقم |
|---|---|
| `maqayis.csv.rows` | 4,506 |

### `lake exe a116-table need`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `fa515db73b9357f0`.

| المسار في المخرَج | الرقم |
|---|---|
| `need.csv.rows` | 9,840 |

### `lake exe a116-table nizam`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `4b5deaa674ec0a13`.

| المسار في المخرَج | الرقم |
|---|---|
| `nizam.csv.rows` | 9 |

### `lake exe a116-table numbers`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `43edb37f96c5b4fd`.

| المسار في المخرَج | الرقم |
|---|---|
| `numbers.csv.rows` | 13,573 |

### `lake exe a116-table order`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `24fc85605adf6265`.

| المسار في المخرَج | الرقم |
|---|---|
| `order.csv.rows` | 116 |

### `lake exe a116-table neutral`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `1992d0a2feaabfe7`.

| المسار في المخرَج | الرقم |
|---|---|
| `neutral.csv.rows` | 341 |

### `lake exe a116-table pairs`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `9cefda5e3998e4d5`.

| المسار في المخرَج | الرقم |
|---|---|
| `pairs.csv.rows` | 4,096 |

### `lake exe a116-table roles`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `70a2ba0ac98eb465`.

| المسار في المخرَج | الرقم |
|---|---|
| `roles.csv.rows` | 116 |

### `lake exe a116-table rubai`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `23ae2687adcc61b5`.

| المسار في المخرَج | الرقم |
|---|---|
| `rubai.csv.rows` | 79 |

### `lake exe a116-table syllables`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `c4e6bcb99802b9d9`.

| المسار في المخرَج | الرقم |
|---|---|
| `syllables.csv.rows` | 265,719 |

### `lake exe a116-table table`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `e5d35172c85daaf0`.

| المسار في المخرَج | الرقم |
|---|---|
| `table.csv.rows` | 348 |

### `lake exe a116-table tasrif`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `5be548fea273540d`.

| المسار في المخرَج | الرقم |
|---|---|
| `tasrif.csv.rows` | 1,281 |

### `lake exe a116-table utf8`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `a08302aea8bd3b70`.

| المسار في المخرَج | الرقم |
|---|---|
| `utf8.csv.rows` | 53 |

### `lake exe a116-table wazn`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `f658fd7949a27714`.

| المسار في المخرَج | الرقم |
|---|---|
| `wazn.csv.rows` | 31 |

### `lake exe a116-table wazn-body`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `b03a4c22cdc02e69`.

| المسار في المخرَج | الرقم |
|---|---|
| `wazn-body.csv.rows` | 31 |


## أعدادُ المبرهنات بوحداتها (85 مبرهنة)

مستخرَجةٌ من نصوص Lean (`formal/a116/A116/*.lean`): كلُّ مبرهنةٍ مدقَّقة ينتهي نصُّها بـ‎= عدد‎؛ والوحدةُ من القائمة المغلقة أدناه (ADR ١٢). العددُ هو الثابتُ الأخير في نصّ المبرهنة.

| الرقم | الوحدة | المبرهنة |
|---|---|---|
| 3 | خانة | `A116.Alif.alifVowelled_length` |
| 113 | خانة | `A116.Alif.licensable_length` |
| 4 | علامة إعراب | `A116.Amil.asliyya_count` |
| 7 | علامة إعراب | `A116.Amil.harfiyya_count` |
| 32 | زوج صنف وحالة | `A116.Amil.naib_count` |
| 13 | صنف أثر | `A116.Awamil.all_length` |
| 100 | عامل | `A116.AwamilCount.rows_length` |
| 14 | عامل | `A116.AwamilCount.class_counts` |
| 4 | عامل | `A116.AwamilCount.names_repeat` |
| 116 | خانة | `A116.Cells.cells_length` |
| 112 | خانة | `A116.Cells.cells112_length` |
| 4 | خانة | `A116.Cells.hamzaRow_length` |
| 304 | متتالية أصناف بالوزن | `A116.ContinueCount.continue_count_304` |
| 87 | سلسلة خانات مرخصة بالطول | `A116.Count.U_one` |
| 9 | ضلع اشتقاق | `A116.Derivation.edges_length` |
| 6 | ضلع اشتقاق | `A116.Derivation.branching_nodes` |
| 6 | احتمال×6 | `A116.Derivation.rows_stochastic` |
| 15 | وزن التوزيع المستقر | `A116.Derivation.w_total` |
| 375 | سلسلة غلاف بالطول | `A116.Envelope.envelope_375` |
| 75 | سلسلة غلاف بالطول | `A116.Envelope.envelope_licensed_75` |
| 59 | سلسلة غلاف بالطول | `A116.Envelope.envelope_licensed_continue_59` |
| 116 | دور خانة | `A116.Exhaust.role_count` |
| 3 | حقل وظيفة | `A116.Exhaust.current_qaim_count` |
| 40 | زوج مانع | `A116.Fasl.makhraj_mani_count` |
| 28 | حامل | `A116.Field112.letters28_length` |
| 112 | خانة | `A116.Field112.hamilField112_length` |
| 6,236 | آية | `A116.FractalMushaf.ayat_count` |
| 38 | كلمة مصحف | `A116.FractalMushaf.kalimat_count` |
| 6,198 | آية | `A116.FractalMushaf.ayat_ctx_count` |
| 16,188 | حد بين كلمتين | `A116.FractalMushaf.hadd_counts` |
| 6,006 | آية | `A116.FractalTarkib.isnad_mushaf` |
| 7 | حالة آلة | `A116.Hajah.states_length` |
| 31 | قالب | `A116.Ishtiqaq.soundTemplates_length` |
| 29 | حامل | `A116.Jadwal.khalil_partition` |
| 29 | خانة | `A116.Jadwal.ibtida_wasl_waqf_counts` |
| 8 | زوج متجاور | `A116.Jadwal.obs_counts` |
| 122,052,735 | سلسلة خانات مرخصة بالطول | `A116.Junction.licensed_upto_4` |
| 177,045 | قلادة حوامل | `A116.Junction.burnside_4` |
| 5 | نمط متحرك/ساكن | `A116.Ladder.admissible_patterns_3` |
| 1,097,505 | سلسلة خانات مرخصة بالطول | `A116.Ladder.U3_by_pattern` |
| 6 | حقل وظيفة | `A116.Ledger.filled_qaim_count` |
| 29 | حامل | `A116.Makharij.huruf_length` |
| 10 | حامل | `A116.Makharij.jahr_partition` |
| 93 | زوج إدغام | `A116.MakharijIdgham.pos_count` |
| 44 | زوج إدغام | `A116.MakharijIdgham.neg_count` |
| 120 | زوج إدغام | `A116.MakharijIdgham.R_count` |
| 44 | زوج إدغام | `A116.MakharijIdgham.far_count` |
| 3 | حالة آلة | `A116.Model.saturation_rungs` |
| 6 | زوج جوار | `A116.Nizam.waslK_count` |
| 8 | خانة | `A116.Numbering.orders_differ_only_in_two_rows` |
| 375 | متتالية أصناف بالوزن | `A116.PauseCount.pause_count_375` |
| 782 | زوج وضع مشترك | `A116.Qarina.pair_count` |
| 566 | زوج وضع مشترك | `A116.Qarina.covered_count` |
| 558 | زوج وضع مشترك | `A116.Qarina.separable_count` |
| 207 | لفظ مشترك | `A116.Qarina.lafz_covered_count` |
| 199 | لفظ مشترك | `A116.Qarina.lafz_separable_count` |
| 45 | زوج صنف وحالة | `A116.Qism.pairs_length` |
| 24 | زوج صنف وحالة | `A116.Qism.coverage_counts` |
| 5 | زوج صنف وحالة | `A116.Qism.naive_wrong_count` |
| 6 | حقل وظيفة | `A116.Qufl.locked_qaim_count` |
| 625 | صفة جذر | `A116.Rubai.allSifa4_length` |
| 1,094 | مدخل سجل | `A116.Sijill.rows_length` |
| 4 | مدخل سجل | `A116.Sijill.mana_count` |
| 7 | مدخل سجل | `A116.Sijill.qaim_count` |
| 250 | صفة جذر | `A116.Tasrif.allSifa_length` |
| 84 | سلسلة خانات | `A116.Tawafiq.wasl_one` |
| 84 | سلسلة خانات | `A116.Tawafiq.waqf_one` |
| 9,492 | سلسلة خانات | `A116.Tawafiq.wasl_two` |
| 9,492 | سلسلة خانات | `A116.Tawafiq.waqf_two` |
| 56 | سلسلة خانات | `A116.Tawafiq.alif_closers_two` |
| 64 | بناء ثلاثي | `A116.Tawafiq.shapes64_length` |
| 45 | بناء ثلاثي | `A116.Tawafiq.shapes64_wasl` |
| 48 | بناء ثلاثي | `A116.Tawafiq.shapes64_waqf` |
| 12 | بناء ثلاثي | `A116.Tawafiq.law_ism_twelve` |
| 10 | بناء ثلاثي | `A116.Tawafiq.naql_ism_ten` |
| 12 | بناء ثلاثي | `A116.Tawafiq.law_fil_twelve` |
| 4 | بناء ثلاثي | `A116.Tawafiq.naql_fil_four` |
| 48 | بناء رباعي | `A116.Tawafiq.shapes48_length` |
| 45 | بناء رباعي | `A116.Tawafiq.law_rubai` |
| 31 | قالب | `A116.Tawafiq.zawaid_row` |
| 2 | بايت | `A116.Unicode.arabic_is_two_bytes` |
| 382 | لفظ مشترك | `A116.Wad.mushtarak_count` |
| 12 | قالب | `A116.Wazn.wasl_joined_waits` |
| 10 | حامل | `A116.Zawaid.zawaid_length` |
| 37 | خانة | `A116.Zawaid.zawaid_cells_licensable` |

### رقمٌ واحدٌ بوحداتٍ مختلفة — لا يُقرأ بلا وحدته

- 3: حالة آلة؛ حقل وظيفة؛ خانة
- 4: بناء ثلاثي؛ خانة؛ عامل؛ علامة إعراب؛ مدخل سجل
- 5: زوج صنف وحالة؛ نمط متحرك/ساكن
- 6: احتمال×6؛ حقل وظيفة؛ زوج جوار؛ ضلع اشتقاق
- 7: حالة آلة؛ علامة إعراب؛ مدخل سجل
- 8: خانة؛ زوج متجاور
- 10: بناء ثلاثي؛ حامل
- 12: بناء ثلاثي؛ قالب
- 29: حامل؛ خانة
- 45: بناء ثلاثي؛ بناء رباعي؛ زوج صنف وحالة
- 48: بناء ثلاثي؛ بناء رباعي
- 116: خانة؛ دور خانة
- 375: سلسلة غلاف بالطول؛ متتالية أصناف بالوزن

### القائمةُ المغلقة للوحدات

| الوحدة | معناها |
|---|---|
| خانة | خانةٌ من شبكة الحوامل × الحالات |
| حامل | حرفٌ حاملٌ بلا حالة |
| بايت | بايتٌ في ترميز UTF-8 |
| سلسلة خانات مرخصة بالطول | سلسلةُ خاناتٍ مرخَّصةٌ ثنائيًّا (‎U(n)‎) بطولها |
| سلسلة خانات | سلسلةُ خاناتٍ من الشبكة المرخَّصة (113) بطولٍ معلوم، مرخَّصةٌ ثلاثيًّا |
| بناء ثلاثي | بناءٌ من حركاتٍ على الأصول الثلاثة لجذرٍ صحيحٍ شاهد (ك ت ب) |
| صنف أثر | صنفُ أثرِ العامل على معموليه (`Awamil.Athar`) — ADR ٧١ |
| عامل | عاملٌ من جدول العوامل المودَع (`corpora/awamil/awamil.tsv`) — ADR ٧١ |
| بناء رباعي | بناءٌ من حركاتٍ على الأصول الأربعة لجذرٍ صحيحٍ شاهد (د ح ر ج)، آخرُه فتحة |
| علامة إعراب | آخرٌ من آخِر المعرب في جدول الألفيّة (`Qism.Ending`): حركةٌ أصليّة أو حرفٌ نائب — ADR ٧٠ |
| قلادة حوامل | مدارُ سلاسل الحوامل تحت الدوران (عدُّ بيرنسايد) |
| نمط متحرك/ساكن | نمطُ M/S بطولٍ معيّن |
| حالة آلة | حالةٌ في آلة الترخيص المشبَّعة |
| ضلع اشتقاق | ضلعٌ بين أبواب الفعل في رسم الاشتقاق |
| احتمال×6 | احتمالُ انتقالٍ مضروبًا في 6 |
| وزن التوزيع المستقر | وزنٌ غيرُ مسوًّى في التوزيع المستقرّ على الأبواب |
| قالب | قالبُ صيغةٍ صرفيّة |
| متتالية أصناف بالوزن | متتاليةُ أصنافٍ (cv=2، v=c=1) بوزنها الصوتيّ |
| سلسلة غلاف بالطول | سلسلةُ C/V من الغلاف المقترَح بطولها |
| دور خانة | زوجُ (خانةٍ مرخَّصة، دورٍ تقبله: cv أو v أو c) — ADR ١٥ |
| حقل وظيفة | حقلٌ من الوظائف السبع في صفّ درجة (ترميز … دلالة) — ADR ١٥ |
| زوج جوار | زوجُ صنفين متجاورين (قبل، بعد) مأذونٌ وصلًا في نظام الجوار — ADR ٢٣ |
| صفة جذر | صفةُ جذر: أصنافُ أصوله (و ي ء ل صحيح)، ومماثلةُ العين واللام في الثلاثيّ — ADR ٢٦ |
| مدخل سجل | مدخلٌ في سجلّ التراخيص المودَع (`docs/sijill/ledger.json`): ملفٌّ ببصمته — ADR ٢٩ |
| زوج صنف وحالة | زوجُ (صنفِ معربٍ، حالةِ إعراب) له آخرٌ في جدول الألفيّة (`Qism.ending`) — ADR ٥٤ |
| لفظ مشترك | لفظٌ (مفتاحُ خاناتٍ من لين) له في علاقة الوضع المودَعة جذران فأكثر (`corpora/wad/wad.tsv`) — ADR ٥٦ |
| زوج وضع مشترك | زوجُ (لفظٍ مشترك، جذرٍ من جذوره) في علاقة الوضع المودَعة، وحقلُه عُقَدُ «المخصَّص» (`corpora/wad/qarina.tsv`) — ADR ٥٩ |
| زوج إدغام | زوجُ (حرفٍ مدغَم، حرفٍ مدغَمٍ فيه) من صفوف أبواب الإدغام في «الكتاب» المختوم (`A116.MakharijIdgham`) — ADR ٦٨ |
| زوج متجاور | زوجُ أصلين متجاورين في جذرٍ ثلاثيٍّ من «مقاييس اللغة» المختومة (`A116.Jadwal.obsD`) — ADR ٧٣ |
| زوج مانع | زوجٌ مرتّبٌ من حرفين مختلفين سببُ فصلهما واحد في مجاله (`A116.Fasl.mani`) — ADR ٧٤ |
| آية | آيةٌ من المصحف المختوم سطرًا (`A116.FractalMushaf.ayat`) — ADR ٧٨ |
| كلمة مصحف | موقعُ كلمةٍ في المصحف المختوم داخلٌ `gate.enter` (`A116.FractalMushaf.Aya`) — ADR ٧٨ |
| حد بين كلمتين | حدٌّ بين كلمتين متجاورتين في آيةٍ من المصحف المختوم (`A116.FractalMushaf.Aya`) — ADR ٧٨ |
