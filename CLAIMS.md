# سجلُّ الأرقام — لا رقمَ بلا مولِّد

مولَّدٌ بـ`python tools/gen_claims.py` باستدعاء كلّ مولِّدٍ مسمًّى في الشجرة؛ لا يُحرَّر باليد، و`--check` يعيد الحسابَ كلَّه في CI ويُسقط البناءَ على أيّ فرق. السطرُ أربعةٌ لا خامسَ لها: الرقم، المولِّد، المودَعاتُ المقروءة (ببصمتها أدناه)، بصمةُ المخرَج كاملًا. مراجعةُ هذا المستودع هي الإيداعُ الحاملُ لهذا الملفّ وشاهدُها تشغيلُ CI. جداولُ Lean يولّدها `lake exe a116-table` في CI وتُطابَق بايتًا بايتًا بالإيداع المسجَّل هنا.

## المودَعات ببصماتها

| المودَع | النوع | sha256 |
|---|---|---|
| `corpora/quran-simple-enhanced.txt` | واقع مختوم (`CORPUS_SHA256`) | `37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a` |
| `corpora/MASAQ.csv` | مرجع محجوب | `d43d2a813afbe0490254bb26623d6041ed352a273d333e731ddbcda3bd0b6f3a` |

## الأرقام (170 رقمًا من 15 مولِّدًا)

### `gate.audit.main`

يقرأ: `corpora/quran-simple-enhanced.txt`. بصمةُ المخرَج: `bc66953c7346f13e`.

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
| `edition_residue.rules_fired.SUKUN` | 13,074 |
| `edition_residue.rules_fired.TANWIN_ALIF` | 1,119 |
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

### `gate.hamza.seat_census`

يقرأ: `corpora/quran-simple-enhanced.txt`. بصمةُ المخرَج: `1bb1d9fdc3838bd7`.

| المسار في المخرَج | الرقم |
|---|---|
| `by_rule` | 4,112 |
| `miss.ء` | 2 |
| `miss.أ` | 16 |
| `miss.ؤ` | 7 |
| `miss.إ` | 30 |
| `miss.ئ` | 46 |
| `seats` | 4,213 |

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

### `lake exe a116-table counts`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `57afd4b22641c974`.

| المسار في المخرَج | الرقم |
|---|---|
| `counts.csv.rows` | 7 |

### `lake exe a116-table hadd`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `2f2ab2c4532e4433`.

| المسار في المخرَج | الرقم |
|---|---|
| `hadd.csv.rows` | 346,200 |

### `lake exe a116-table hamza`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `5028db66c4fbdd50`.

| المسار في المخرَج | الرقم |
|---|---|
| `hamza.csv.rows` | 384 |

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

### `lake exe a116-table pairs`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `9cefda5e3998e4d5`.

| المسار في المخرَج | الرقم |
|---|---|
| `pairs.csv.rows` | 4,096 |

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

### `lake exe a116-table utf8`

يقرأ: — (نواةُ Lean؛ لا مودَع). بصمةُ المخرَج: `a08302aea8bd3b70`.

| المسار في المخرَج | الرقم |
|---|---|
| `utf8.csv.rows` | 53 |
