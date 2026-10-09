# سجلُّ الأرقام — لا رقمَ بلا مولِّد

مولَّدٌ بـ`python tools/gen_claims.py` من `measure()` في كلّ أداةِ فهرس؛ لا يُحرَّر باليد، و`--check` يعيد الحسابَ كلَّه في CI ويُسقط البناءَ على أيّ فرق. السطرُ أربعةٌ لا خامسَ لها: الرقم، المولِّد، المودَعاتُ المقروءة (ببصمتها أدناه)، بصمةُ المخرَج كاملًا. مراجعةُ هذا المستودع هي الإيداعُ الحاملُ لهذا الملفّ وشاهدُها تشغيلُ CI؛ وبرهانُ الـ116 مثبَّتٌ على الإيداع `a3341231703542f68c3909d93f289ccbd8faf5e6` (`formal/lakefile.toml`).

## المودَعات ببصماتها

| المودَع | النوع | sha256 |
|---|---|---|
| `corpus-certificates.json.gz` | واقع مختوم | `89d4bb9f5d354e1bece473ff8a058625d82b13b848994f77edd8f9d26c3e844b` |
| `context-certificates.json.gz` | واقع مختوم | `0c2d2fac65716259eeb6189ae03134b5672665460e43ae0a2830710afa5ac4de` |
| `maqayis-roots.json.gz` | وضع | `90312a5adb4bc32043d1e57cc0bc8438c4ac19d6b3d57e90defe2d9c77c1542e` |
| `sibawayh-abniya.tsv` | وضع | `678ca5144698b571a42804b19b8d1680766df7f2339cf6c9c53d84994051fdd9` |
| `nabhani-huruf.json` | وضع | `5f6f3d64736e981a867524d7478ab1773670033d2a229f8aefcbbaf4905f4766` |
| `openiti-mukhassas.txt.gz` | وضع | `8d8134c2bce16b70b07bddf974fa5e9c0f7cd80129d8452baf55cd87006b80ac` |
| `openiti-maqayis.txt.gz` | وضع | `da8853fc941d4016a533fd9c7a1f794a2ccfa92f1c74e68d4acbd6d910e72a67` |
| `openiti-sibawayh-kitab.txt.gz` | وضع | `a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625` |
| `nabhani-shakhsiyya-3.txt.gz` | وضع | `359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4` |
| `nabhani-tafkir.txt.gz` | وضع | `b9b08eabec468aa0f93b80c01879e3812c57f4bd677e68e448967e3575bfaae4` |
| `owner-alam.json` | وضع | `561fa752b4c97d356786009ba0e5017b15089bf615bc2939eafc794edce6993f` |
| `openiti-majaz-quran.txt.gz` | مرجع محجوب | `432dae05748f2f972b3238e56dd0c56e72b10f0c3900ee8da1a8cca812b2fc88` |
| `masaq-adad.json` | مرجع محجوب | `9018b3f445f65bc23799f0bee3cda1ab1fe3a1a0a0ab7e67e6d85406e77cd822` |
| `masaq-fil.json.gz` | مرجع محجوب | `61ed093595d72dc3b144b1ce1baf5f9c358f17ceeda765378a5198e86546060c` |
| `masaq-filiyya.json.gz` | مرجع محجوب | `830834cedf1069f581c6e7c5028a3874e610b48568205031140657624548ad08` |
| `masaq-hamza.json` | مرجع محجوب | `31e9021b84ffae48f25e3cd1d5a7e9b1af5a51907580e902aeafe23329452203` |
| `masaq-huruf.json` | مرجع محجوب | `928482e7b86ff2c1717cb48ec510a8aa6f8c07fafdf155a879d38f789bdedc2e` |
| `masaq-interrog.json` | مرجع محجوب | `d3cd64abc1e20de1b1f3c5d5d5ef3af90583733efa078e8b38c874ebd39e91c4` |
| `masaq-ism.json.gz` | مرجع محجوب | `034bfbab4be475ea129b5687e3a02a59ac781b1e55235aa40cf02d8e90479039` |
| `masaq-jazm.json` | مرجع محجوب | `d0c3f09993751be1145ff94a88241a278e4cafbad60139523f5d112f4a33366c` |
| `masaq-jumla.json` | مرجع محجوب | `e0f0ac0dd12ee087924cc96caf793e8e291a8fcf6aea390f9b7e39ee2f751a05` |
| `masaq-majrurat.json.gz` | مرجع محجوب | `3edc1175fde2d577dfaaaa671da594a578f22614c37e48e75baf4b580b4c9d78` |
| `masaq-mansubat.json` | مرجع محجوب | `3e646c835770b388e0a7a9142d9f30237ac73e2e3343b59b3cf70890aa0957ab` |
| `masaq-marifa.json` | مرجع محجوب | `c54122187501fd2f49af6d9c8622cdaf12f6e45322202578000815c8b6b6b3ae` |
| `masaq-munada.json` | مرجع محجوب | `2189dd4d7dc752fd25786e16cea156ef23679841e7c36f763e6f0f3f11643a42` |
| `masaq-nawasikh.json` | مرجع محجوب | `27dbe6e838439327f1ba46e9e563383791a4cd04996032c650b9de74f5b4c9c8` |
| `masaq-sarf.json` | مرجع محجوب | `5884bd5f77fe622752ebfbbb3368ee5f888c8fd716a80f82a94d777442ed7f03` |
| `masaq-shibh.json.gz` | مرجع محجوب | `a312d1646c713f01545b710e0dc7b5b429fc728ffe8e7f8c0ff2abbd16b5f760` |
| `masaq-tawabi.json` | مرجع محجوب | `2917e3bf75bf919e3daddfa667e94342490ef20fc4cdee5680a4e52832632c26` |
| `masaq-zaman.json` | مرجع محجوب | `b67ccb039a2c24a1e3809104994fbb5fbd68d9796b034e85d654683c19db011b` |
| `masaq-zawaid.json` | مرجع محجوب | `15ab1c4691c88ebb99b4f37c5f1c062c83a20a988fdd6099cc835eaea4097478` |
| `masaq-zuruf.json` | مرجع محجوب | `ef2e77119120a8f5109e28e63c0835468ce85442806c44b0e4f4a70635416dd3` |

## الأرقام (1,123 رقمًا من 47 مولِّدًا)

### `tools/gen_abniya_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `cfd3af676a5c13aa`.

| المسار في المخرَج | الرقم |
|---|---|
| `forms` | 18,179 |
| `gold.121` | 1,197 |
| `gold.122` | 763 |
| `gold.123` | 4 |
| `gold.124` | 29 |
| `in_abniya` | 111 |
| `masaq` | 40,731 |
| `match` | 15,583 |
| `n` | 125 |
| `none` | 4,844 |
| `only.121` | 396 |
| `only.122` | 265 |
| `only.123` | 7 |
| `only.124` | 28 |
| `read` | 15,673 |
| `separated_pairs` | 7,739 |
| `step2` | 15,673 |
| `with.121` | 770 |
| `with.122` | 660 |
| `with.123` | 15 |
| `with.124` | 45 |

### `tools/gen_adad_index.py::measure`

يقرأ: `masaq-adad.json`. بصمةُ المخرَج: `3574aca0c8175050`.

| المسار في المخرَج | الرقم |
|---|---|
| `[0].('100', 'تنوين كسر', True)` | 5 |
| `[0].('1000', 'تنوين كسر', True)` | 6 |
| `[0].('20-90', 'تنوين فتح', True)` | 8 |
| `[0].('20-90', 'فتح', True)` | 1 |
| `[0].('3-10', 'تنوين كسر', True)` | 45 |
| `[0].('3-10', 'سكون', False)` | 1 |
| `[0].('3-10', 'فتح', True)` | 6 |
| `[1]` | 72 |
| `[2]` | 112 |

### `tools/gen_adawat_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `d21b95c6d178c1da`.

| المسار في المخرَج | الرقم |
|---|---|
| `after.مخالف` | 23 |
| `after.موافق` | 572 |
| `amal.جرّ.مبنيّ` | 47 |
| `amal.جرّ.مخالف` | 375 |
| `amal.جرّ.موافق` | 3,701 |
| `amal.جزم.مبنيّ` | 23 |
| `amal.جزم.موافق` | 14 |
| `amal.جزم فعلين.مبنيّ` | 12 |
| `amal.جزم فعلين.مخالف` | 2 |
| `amal.جزم فعلين.موافق` | 3 |
| `amal.نصب الاسم.مبنيّ` | 35 |
| `amal.نصب الاسم.مخالف` | 53 |
| `amal.نصب الاسم.موافق` | 24 |
| `amal.نصب الفعل.مبنيّ` | 9 |
| `amal.نصب الفعل.موافق` | 36 |
| `attached.مبنيّ` | 242 |
| `attached.مخالف` | 459 |
| `attached.موافق` | 3,093 |
| `before.مخالف` | 297 |
| `before.موافق` | 298 |
| `forms` | 18,179 |
| `per_tool[0][1]` | 1,655 |
| `per_tool[1][1]` | 1,121 |
| `per_tool[2][1]` | 660 |
| `per_tool[3][1]` | 397 |
| `per_tool[4][1]` | 279 |
| `per_tool[5][1]` | 150 |
| `per_tool[6][1]` | 138 |
| `per_tool[7][1]` | 56 |
| `per_tool[8][1]` | 55 |
| `per_tool[9][1]` | 45 |
| `per_tool[10][1]` | 34 |
| `per_tool[11][1]` | 33 |
| `rows` | 40,731 |
| `table` | 68 |
| `tool_forms` | 50 |
| `with_next` | 29,866 |

### `tools/gen_alam_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `e7ef8a0a45ac5cbb`.

| المسار في المخرَج | الرقم |
|---|---|
| `case_asked` | 1,714 |
| `case_ok` | 1,631 |
| `det_jalala` | 1,255 |
| `forms` | 18,179 |
| `gold` | 460 |
| `jalala_forms` | 10 |
| `jforms.AFTER_PREFIX` | 10 |
| `jforms.INITIAL` | 3 |
| `jforms.LAHUMMA` | 1 |
| `jforms.MADD` | 3 |
| `kinds.أعجمي` | 86 |
| `kinds.جلالة` | 17 |
| `kinds.عربي` | 75 |
| `multi` | 0 |
| `none` | 218 |
| `props` | 1,935 |
| `read` | 178 |
| `sarfs.غير مشهود الجرّ` | 23 |
| `sarfs.مقصور` | 13 |
| `sarfs.ممنوع` | 76 |
| `sarfs.منصرف` | 49 |
| `sarfs.منفرد` | 17 |
| `table` | 57 |
| `table_kinds.أعجمي` | 30 |
| `table_kinds.عربي` | 27 |
| `table_sarfs.غير مشهود الجرّ` | 8 |
| `table_sarfs.مقصور` | 4 |
| `table_sarfs.ممنوع` | 27 |
| `table_sarfs.منصرف` | 18 |
| `unread_top.len` | 15 |
| `with_pre` | 81 |
| `wrong` | 2 |

### `tools/gen_bits_index.py::measure`

يقرأ: `corpus-certificates.json.gz`. بصمةُ المخرَج: `5a7cb1f462d440e9`.

| المسار في المخرَج | الرقم |
|---|---|
| `atoms_number_bits` | 651,981 |
| `atoms_ok` | 18,179 |
| `binary` | 18,114 |
| `cells` | 99,130 |
| `cert_bits` | 1,276,753 |
| `certified_tokens` | 78,207 |
| `codebook_bytes` | 2,245,161 |
| `cost_sum` | 2,792,533 |
| `fibers_gt1` | 38 |
| `fold_bits` | 658,873 |
| `fold_bound` | 672,465 |
| `fold_lt` | 18,114 |
| `fold_roundtrip` | 18,114 |
| `forms` | 18,179 |
| `granted` | 18,114 |
| `log116` | 679,832 |
| `per_word` | 78,100 |
| `refusals.DEFER:UNVOCALIZED_WORD_IS_NEVER_GUESSED` | 30 |
| `refusals.REJECT:INITIAL_SUKUN_WITHOUT_REPAIR` | 3 |
| `refusals.REJECT:NOT_CONTINUE_LICENSED_AFTER_REPAIR` | 1 |
| `refusals.REJECT:TANWIN_WITH_ANOTHER_HARAKA` | 4 |
| `residual_bits` | 38 |
| `residue_edits` | 19,889 |
| `sample_ok` | 1 |
| `stream_bits` | 2,792,533 |
| `stream_words` | 78,100 |
| `ternary_only` | 65 |
| `tokens` | 78,245 |
| `widths.10` | 94 |
| `widths.11` | 8 |
| `widths.2` | 10,277 |
| `widths.3` | 13,089 |
| `widths.4` | 18,199 |
| `widths.5` | 16,614 |
| `widths.6` | 12,300 |
| `widths.7` | 4,468 |
| `widths.8` | 2,710 |
| `widths.9` | 341 |

### `tools/gen_coverage_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `context-certificates.json.gz`. بصمةُ المخرَج: `db1e48d05d29b7c6`.

| المسار في المخرَج | الرقم |
|---|---|
| `attested_cells.len` | 113 |
| `cells.attested` | 113 |
| `cells.licensable` | 113 |
| `cells.vowelled_alif_seen` | 0 |
| `context_forms` | 17,937 |
| `forms` | 18,179 |
| `maqayis.forms_with_root` | 13,450 |
| `maqayis.muhtamal_only` | 276 |
| `maqayis.none` | 2,666 |
| `maqayis.qati` | 1,619 |
| `maqayis.roots` | 4,561 |
| `maqayis.top_qati[0][1]` | 131 |
| `maqayis.top_qati[1][1]` | 115 |
| `maqayis.top_qati[2][1]` | 106 |
| `maqayis.top_qati[3][1]` | 91 |
| `maqayis.top_qati[4][1]` | 86 |
| `maqayis.top_qati[5][1]` | 83 |
| `maqayis.top_qati[6][1]` | 82 |
| `maqayis.top_qati[7][1]` | 74 |
| `maqayis.top_qati[8][1]` | 74 |
| `maqayis.top_qati[9][1]` | 67 |
| `mukhassas.muhtamal_only` | 19 |
| `mukhassas.no_roots` | 520 |
| `mukhassas.nodes` | 1,600 |
| `mukhassas.none` | 89 |
| `mukhassas.qati` | 972 |
| `mukhassas.with_roots` | 1,080 |
| `readers.الإعراب.forms` | 18,114 |
| `readers.الإعراب.tokens` | 78,100 |
| `readers.الجداول.forms` | 1,029 |
| `readers.الجداول.tokens` | 30,548 |
| `readers.الجذع.forms` | 15,667 |
| `readers.الجذع.tokens` | 67,999 |
| `readers.الجواب.forms` | 18,114 |
| `readers.الجواب.tokens` | 78,100 |
| `readers.السوابق.forms` | 4,928 |
| `readers.السوابق.tokens` | 20,138 |
| `readers.الصرف.forms` | 1,221 |
| `readers.الصرف.tokens` | 6,874 |
| `tables.alam.attested` | 57 |
| `tables.alam.rows` | 57 |
| `tables.sawabiq.attested` | 11 |
| `tables.sawabiq.rows` | 11 |
| `tables.tawzi.attested` | 160 |
| `tables.tawzi.rows` | 246 |
| `tables.tawzi.unattested.len` | 86 |
| `tokens` | 78,245 |

### `tools/gen_fil_index.py::measure`

يقرأ: `masaq-fil.json.gz`. بصمةُ المخرَج: `0dfed518411bde12`.

| المسار في المخرَج | الرقم |
|---|---|
| `ibdal.تاءٌ ⇒ دال (د)` | 1 |
| `ibdal.تاءٌ ⇒ طاء (ص)` | 3 |
| `ibdal.تاءٌ ⇒ طاء (ط)` | 1 |
| `ibdal.فاءٌ ⇒ تاء مدغمة` | 32 |
| `n` | 18,765 |
| `n_iv` | 2,919 |
| `n_pv` | 617 |
| `past.ضم` | 9 |
| `past.فتح` | 489 |
| `past.كسر` | 119 |
| `pres.ضم` | 657 |
| `pres.فتح` | 1,226 |
| `pres.كسر` | 1,036 |
| `templ.len` | 15 |
| `templ.sum` | 3,224 |

### `tools/gen_filiyya_index.py::measure`

يقرأ: `masaq-filiyya.json.gz`. بصمةُ المخرَج: `3bcc5cfcd3f4a7af`.

| المسار في المخرَج | الرقم |
|---|---|
| `endings.len` | 16 |
| `endings.sum` | 6,979 |
| `fadla.('مفعول لأجله', 'مفعول لأجله')` | 23 |
| `fadla.('مفعول لأجله', '—')` | 15 |
| `fadla.('مفعول مطلق', 'حال')` | 9 |
| `fadla.('مفعول مطلق', 'مفعول لأجله')` | 57 |
| `fadla.('مفعول مطلق', 'مفعول مطلق')` | 11 |
| `fadla.('مفعول مطلق', '—')` | 84 |
| `n` | 26,196 |
| `naib.مجرور` | 1 |
| `naib.مصدر` | 145 |
| `naib.مفعول به` | 185 |
| `obj.('فعل أمر', False)` | 179 |
| `obj.('فعل أمر', True)` | 1,111 |
| `obj.('فعل ماضٍ مبني للمجهول', False)` | 69 |
| `obj.('فعل ماضٍ مبني للمجهول', True)` | 539 |
| `obj.('فعل ماضٍ', False)` | 933 |
| `obj.('فعل ماضٍ', True)` | 6,046 |
| `obj.('فعل مضارع مبني للمجهول', False)` | 9 |
| `obj.('فعل مضارع مبني للمجهول', True)` | 464 |
| `obj.('فعل مضارع', False)` | 634 |
| `obj.('فعل مضارع', True)` | 6,743 |
| `rutba.len` | 20 |
| `rutba.sum` | 16,727 |
| `subj.('فعل أمر', False)` | 131 |
| `subj.('فعل أمر', True)` | 1,159 |
| `subj.('فعل ماضٍ مبني للمجهول', False)` | 22 |
| `subj.('فعل ماضٍ مبني للمجهول', True)` | 586 |
| `subj.('فعل ماضٍ', False)` | 1,193 |
| `subj.('فعل ماضٍ', True)` | 5,786 |
| `subj.('فعل مضارع مبني للمجهول', False)` | 96 |
| `subj.('فعل مضارع مبني للمجهول', True)` | 377 |
| `subj.('فعل مضارع', False)` | 1,033 |
| `subj.('فعل مضارع', True)` | 6,344 |
| `triples` | 16,727 |
| `zarf.('ظرف زمان', 'جرّ')` | 19 |
| `zarf.('ظرف زمان', 'رفع')` | 70 |
| `zarf.('ظرف زمان', 'لا تقرؤه الخانة')` | 749 |
| `zarf.('ظرف زمان', 'نصب')` | 455 |
| `zarf.('ظرف زمان', 'نصب/جرّ')` | 16 |
| `zarf.('ظرف مكان', 'جرّ')` | 18 |
| `zarf.('ظرف مكان', 'رفع')` | 29 |
| `zarf.('ظرف مكان', 'لا تقرؤه الخانة')` | 26 |
| `zarf.('ظرف مكان', 'نصب')` | 641 |
| `zarf.('ظرف مكان', 'نصب/جرّ')` | 10 |

### `tools/gen_hasm_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `a39740feb48cf7e2`.

| المسار في المخرَج | الرقم |
|---|---|
| `bound` | 129 |
| `forms` | 18,179 |
| `masaq.DECIDED_GOLD` | 5,516 |
| `masaq.DECIDED_WRONG` | 3,385 |
| `masaq.NO_READING` | 4,844 |
| `masaq.TIE` | 415 |
| `masaq.TIE_GOLD_IN` | 1,572 |
| `masaq.UNIQUE_GOLD` | 21,242 |
| `masaq.UNIQUE_WRONG` | 3,757 |
| `masaq.masaq` | 40,731 |
| `roots` | 2,380 |
| `unique_forms` | 12,157 |

### `tools/gen_huruf_index.py::measure`

يقرأ: `masaq-huruf.json`. بصمةُ المخرَج: `80b599ba62ca055d`.

| المسار في المخرَج | الرقم |
|---|---|
| `after.أن.اسم مبني` | 97 |
| `after.أن.اسم مجرور` | 23 |
| `after.أن.اسم مرفوع` | 61 |
| `after.أن.اسم منصوب` | 557 |
| `after.أن.غيره` | 270 |
| `after.أن.فعل مضارع مبني` | 7 |
| `after.أن.فعل مضارع مجزوم` | 5 |
| `after.أن.فعل مضارع مرفوع` | 25 |
| `after.أن.فعل مضارع منصوب` | 446 |
| `after.إذن.اسم مبني` | 2 |
| `after.إذن.اسم مجرور` | 25 |
| `after.إذن.اسم مرفوع` | 2 |
| `after.إذن.اسم منصوب` | 4 |
| `after.إذن.غيره` | 1 |
| `after.إذن.فعل مضارع مرفوع` | 5 |
| `after.حتى.اسم مجرور` | 7 |
| `after.حتى.اسم منصوب` | 42 |
| `after.حتى.غيره` | 17 |
| `after.حتى.فعل مضارع مبني` | 1 |
| `after.حتى.فعل مضارع مرفوع` | 1 |
| `after.حتى.فعل مضارع منصوب` | 74 |
| `after.كي.غيره` | 3 |
| `after.كي.فعل مضارع منصوب` | 7 |
| `after.لا.اسم مبني` | 32 |
| `after.لا.اسم مجرور` | 43 |
| `after.لا.اسم مرفوع` | 101 |
| `after.لا.اسم منصوب` | 115 |
| `after.لا.غيره` | 109 |
| `after.لا.فعل مضارع مبني` | 8 |
| `after.لا.فعل مضارع مجرور` | 1 |
| `after.لا.فعل مضارع مجزوم` | 408 |
| `after.لا.فعل مضارع مرفوع` | 832 |
| `after.لا.فعل مضارع منصوب` | 38 |
| `after.لم.اسم مجزوم` | 5 |
| `after.لم.غيره` | 6 |
| `after.لم.فعل مضارع مجزوم` | 342 |
| `after.لم.فعل مضارع مرفوع` | 14 |
| `after.لن.غيره` | 1 |
| `after.لن.فعل مضارع مجرور` | 1 |
| `after.لن.فعل مضارع منصوب` | 104 |
| `roles.len` | 40 |

### `tools/gen_ilal_bab_index.py::measure`

يقرأ: `corpus-certificates.json.gz`. بصمةُ المخرَج: `150dc7fc0c6f9fa2`.

| المسار في المخرَج | الرقم |
|---|---|
| `all_read` | 1 |
| `chapters` | 9 |
| `debts` | 7 |
| `forms` | 18,179 |
| `read.len` | 13 |
| `read.sum` | 37,799 |
| `rows` | 13 |
| `witnessed` | 8 |

### `tools/gen_ilal_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `c331f264cbc40892`.

| المسار في المخرَج | الرقم |
|---|---|
| `checked` | 6,201 |
| `forms` | 18,179 |
| `law.dzz_dal` | 297 |
| `law.dzz_other` | 693 |
| `law.dzz_ta` | 20 |
| `law.itbaq_other` | 613 |
| `law.itbaq_ta` | 17 |
| `law.itbaq_tta` | 108 |
| `law.kept.len` | 32 |
| `law.wy_other` | 5,496 |
| `law.wy_ta` | 224 |
| `lengths.1` | 3,145 |
| `lengths.2` | 3,056 |
| `m_hit` | 7,163 |
| `m_total` | 7,749 |
| `only` | 648 |
| `rules.len` | 13 |
| `rules.sum` | 9,257 |
| `with` | 2,040 |

### `tools/gen_ism_index.py::measure`

يقرأ: `masaq-ism.json.gz`. بصمةُ المخرَج: `de8d160e7f77cf0d`.

| المسار في المخرَج | الرقم |
|---|---|
| `n` | 19,216 |
| `n3` | 4,447 |
| `n4` | 1,580 |
| `nis.len` | 22 |
| `nis.sum` | 139 |
| `rub.len` | 21 |
| `rub.sum` | 1,580 |
| `tas.حنين` | 1 |
| `tas.سليمان` | 17 |
| `tas.شعيب` | 1 |
| `tas.عزير` | 1 |
| `tas.قريش` | 1 |
| `tas.مهيمن` | 1 |
| `tas.نقيض` | 1 |
| `thul.('ضم', 'سكون')` | 514 |
| `thul.('ضم', 'ضم')` | 185 |
| `thul.('ضم', 'فتح')` | 57 |
| `thul.('فتح', 'سكون')` | 2,669 |
| `thul.('فتح', 'ضم')` | 25 |
| `thul.('فتح', 'فتح')` | 426 |
| `thul.('فتح', 'كسر')` | 62 |
| `thul.('كسر', 'سكون')` | 261 |
| `thul.('كسر', 'فتح')` | 85 |
| `thul.('كسر', 'كسر')` | 2 |

### `tools/gen_jazm_index.py::measure`

يقرأ: `masaq-jazm.json`. بصمةُ المخرَج: `cdcaa62dd041e26b`.

| المسار في المخرَج | الرقم |
|---|---|
| `[0].('السكون', 'حذف النون')` | 6 |
| `[0].('السكون', 'سكون')` | 514 |
| `[0].('السكون', 'لا تقرؤه الخانة')` | 114 |
| `[0].('حذف النون', 'حذف النون')` | 520 |
| `[0].('حذف النون', 'لا تقرؤه الخانة')` | 17 |
| `[0].('حذف حرف العلة', 'حذف النون')` | 1 |
| `[0].('حذف حرف العلة', 'سكون')` | 1 |
| `[0].('حذف حرف العلة', 'لا تقرؤه الخانة')` | 192 |
| `[1].len` | 15 |
| `[1].sum` | 1,365 |
| `[2].('السكون', 'ضم')` | 24 |
| `[2].('السكون', 'فتح')` | 10 |
| `[2].('السكون', 'كسر')` | 80 |
| `[2].('حذف حرف العلة', 'ضم')` | 17 |
| `[2].('حذف حرف العلة', 'فتح')` | 70 |
| `[2].('حذف حرف العلة', 'كسر')` | 105 |
| `[3]` | 1,365 |

### `tools/gen_jidh_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `6b492435201268ef`.

| المسار في المخرَج | الرقم |
|---|---|
| `before` | 1,848 |
| `forms` | 18,179 |
| `gold_among` | 14,329 |
| `gold_match` | 15,583 |
| `masaq` | 40,731 |
| `none` | 4,844 |
| `only_wrong` | 5,975 |
| `readings.0` | 2,506 |
| `readings.1` | 11,366 |
| `readings.2` | 2,659 |
| `readings.3+` | 1,648 |
| `step1` | 5,196 |
| `step2` | 15,673 |

### `tools/gen_jiha_index.py::measure`

يقرأ: `masaq-filiyya.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `e1894dceb8e9ad69`.

| المسار في المخرَج | الرقم |
|---|---|
| `after.('كَانَ', 'ADV')` | 3 |
| `after.('كَانَ', 'NOUN_ABSTRACT')` | 5 |
| `after.('كَانَ', 'NOUN_ACTIVE_PART')` | 2 |
| `after.('كَانَ', 'NOUN_CONCRETE')` | 11 |
| `after.('كَانَ', 'NOUN_PROP')` | 2 |
| `after.('كَانَ', 'PREP')` | 73 |
| `after.('كَانَ', 'PRON')` | 10 |
| `after.('كَانَ', 'REL_PRON')` | 4 |
| `after.('كَانَ', 'ماضٍ')` | 1 |
| `after.('كَانَ', 'مضارع')` | 1 |
| `after.('لَمْ', 'مضارع')` | 13 |
| `bare.('أمر', 'أمر')` | 214 |
| `bare.('أمر', 'ماضٍ')` | 2 |
| `bare.('أمر', 'مضارع')` | 2 |
| `bare.('أمر', '—')` | 488 |
| `bare.('ماضٍ', 'أمر')` | 5 |
| `bare.('ماضٍ', 'ماضٍ')` | 1,611 |
| `bare.('ماضٍ', 'مضارع')` | 129 |
| `bare.('ماضٍ', '—')` | 1,975 |
| `bare.('مضارع', 'أمر')` | 12 |
| `bare.('مضارع', 'ماضٍ')` | 52 |
| `bare.('مضارع', 'مضارع')` | 2,761 |
| `bare.('مضارع', '—')` | 1,548 |
| `fut.ماضٍ` | 1 |
| `fut.مضارع` | 116 |
| `n` | 16,642 |
| `read_fut.مستقبل` | 53 |
| `read_fut.—` | 64 |

### `tools/gen_jumla_index.py::measure`

يقرأ: `masaq-jumla.json`. بصمةُ المخرَج: `aef4b1092195f085`.

| المسار في المخرَج | الرقم |
|---|---|
| `agree.('مؤنث جمع', 'غيره')` | 4 |
| `agree.('مؤنث مفرد', 'غيره')` | 9 |
| `agree.('مذكر جمع', 'غيره')` | 1 |
| `agree.('مذكر جمع', 'مطابق')` | 4 |
| `agree.('مذكر مفرد (تكسيرٌ محتمل)', 'بالاستثناء')` | 3 |
| `agree.('مذكر مفرد (تكسيرٌ محتمل)', 'غيره')` | 5 |
| `agree.('مذكر مفرد (تكسيرٌ محتمل)', 'مطابق')` | 11 |
| `agree.('مذكر مفرد', 'غيره')` | 21 |
| `agree.('مذكر مفرد', 'مطابق')` | 254 |
| `kk.len` | 13 |
| `kk.sum` | 3,146 |
| `mk.len` | 18 |
| `mk.sum` | 3,146 |
| `n` | 7,418 |
| `nakira` | 548 |
| `pairs` | 3,146 |
| `rabit.ضمير` | 329 |
| `rabit.—` | 190 |
| `rutba.('تقديم الخبر', 'الخبرُ أوّلًا', True)` | 161 |
| `rutba.('تقديم الخبر', 'المبتدأُ أوّلًا', False)` | 71 |
| `rutba.('تقديم المبتدأ', 'الخبرُ أوّلًا', False)` | 253 |
| `rutba.('تقديم المبتدأ', 'المبتدأُ أوّلًا', True)` | 1,622 |
| `rutba.('جواز', 'الخبرُ أوّلًا', True)` | 269 |
| `rutba.('جواز', 'المبتدأُ أوّلًا', True)` | 770 |

### `tools/gen_kulli_index.py::measure`

يقرأ: `masaq-shibh.json.gz`. بصمةُ المخرَج: `e8abfbb271d08dd3`.

| المسار في المخرَج | الرقم |
|---|---|
| `mizan.حدث مجرّد` | 24 |
| `mizan.حدث مهيّأ` | 39 |
| `mizan.كليّ عرضيّ` | 26 |
| `mizan.كليّ ماهويّ` | 31 |
| `mizan.—` | 5 |
| `n` | 15,260 |
| `read.len` | 29 |
| `read.sum` | 15,260 |

### `tools/gen_maani_index.py::measure`

يقرأ: `masaq-shibh.json.gz`. بصمةُ المخرَج: `e5228dcb45a13186`.

| المسار في المخرَج | الرقم |
|---|---|
| `occ` | 7,369 |
| `per.0.changed` | 6 |
| `per.0.either` | 26 |
| `per.0.n` | 2,041 |
| `per.0.nafy` | 6 |
| `per.0.zarf` | 20 |
| `per.1.changed` | 0 |
| `per.1.either` | 4 |
| `per.1.n` | 866 |
| `per.1.nafy` | 0 |
| `per.1.zarf` | 4 |
| `per.10.changed` | 0 |
| `per.10.either` | 0 |
| `per.10.n` | 142 |
| `per.10.nafy` | 0 |
| `per.10.zarf` | 0 |
| `per.2.changed` | 0 |
| `per.2.either` | 0 |
| `per.2.n` | 284 |
| `per.2.nafy` | 0 |
| `per.2.zarf` | 0 |
| `per.3.changed` | 0 |
| `per.3.either` | 3 |
| `per.3.n` | 8 |
| `per.3.nafy` | 0 |
| `per.3.zarf` | 3 |
| `per.5.changed` | 2 |
| `per.5.either` | 300 |
| `per.5.n` | 1,670 |
| `per.5.nafy` | 2 |
| `per.5.zarf` | 298 |
| `per.6.changed` | 0 |
| `per.6.either` | 24 |
| `per.6.n` | 405 |
| `per.6.nafy` | 1 |
| `per.6.zarf` | 23 |
| `per.7.changed` | 0 |
| `per.7.either` | 0 |
| `per.7.n` | 153 |
| `per.7.nafy` | 0 |
| `per.7.zarf` | 0 |
| `per.8.changed` | 0 |
| `per.8.either` | 4 |
| `per.8.n` | 669 |
| `per.8.nafy` | 4 |
| `per.8.zarf` | 0 |
| `per.9.changed` | 0 |
| `per.9.either` | 65 |
| `per.9.n` | 1,131 |
| `per.9.nafy` | 64 |
| `per.9.zarf` | 1 |
| `tops.0.الإلصاق` | 2,035 |
| `tops.0.زائدة` | 6 |
| `tops.1.الاختصاص` | 866 |
| `tops.10.انتهاء الغاية` | 142 |
| `tops.2.التشبيه` | 284 |
| `tops.3.القسم` | 8 |
| `tops.5.ابتداء الغاية` | 1,668 |
| `tops.5.زائدة` | 2 |
| `tops.6.انتهاء الغاية` | 405 |
| `tops.7.المباعدة` | 153 |
| `tops.8.الاستعلاء` | 669 |
| `tops.9.الظرفية` | 1,131 |
| `witnesses[0][4]` | 1 |
| `witnesses[1][4]` | 1 |
| `witnesses[2][4]` | 1 |
| `witnesses[4][4]` | 1 |
| `witnesses[5][4]` | 1 |

### `tools/gen_madd_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `37e3d1c24ce1aee7`.

| المسار في المخرَج | الرقم |
|---|---|
| `continue_licensed` | 18,179 |
| `forms` | 18,179 |
| `lazim_all_ternary_only` | 1 |
| `lazim_forms` | 65 |
| `letters` | 47,865 |
| `sila_pron` | 1,648 |
| `sila_total` | 2,984 |
| `ternary_only` | 65 |
| `ternary_only_all_lazim` | 1 |
| `tokens` | 78,207 |
| `waqf.عارض` | 16,627 |
| `waqf.لين` | 3,031 |
| `wasl.صلة صغرى` | 3,547 |
| `wasl.صلة كبرى` | 1,044 |
| `wasl.طبيعيّ` | 40,230 |
| `wasl.لازم مثقَّل` | 106 |
| `wasl.لازم مخفَّف` | 2 |
| `wasl.متّصل` | 1,744 |
| `wasl.محجوب` | 164 |
| `wasl.منفصل` | 5,619 |

### `tools/gen_majrurat_index.py::measure`

يقرأ: `masaq-majrurat.json.gz`. بصمةُ المخرَج: `aa3944a74f414823`.

| المسار في المخرَج | الرقم |
|---|---|
| `harf.إلى` | 385 |
| `harf.ب` | 1,396 |
| `harf.ت` | 8 |
| `harf.على` | 637 |
| `harf.عن` | 202 |
| `harf.في` | 1,067 |
| `harf.ك` | 72 |
| `harf.ل` | 767 |
| `harf.من` | 1,907 |
| `harf.و` | 149 |
| `harf.—` | 137 |
| `lafzi.('غيره', True)` | 7,104 |
| `lafzi.('مشتقّ', True)` | 1,033 |
| `mabni` | 1,947 |
| `marker.len` | 21 |
| `marker.sum` | 11,669 |
| `mudaf_tanwin.('جمعٌ أو مثنًّى', False)` | 79 |
| `mudaf_tanwin.('مفرد', False)` | 7,979 |
| `mudaf_tanwin.('مفرد', True)` | 79 |
| `n` | 18,184 |
| `nun.True` | 174 |
| `sabab.len` | 15 |
| `sabab.sum` | 11,669 |

### `tools/gen_makharij_index.py::measure`

يقرأ: `corpus-certificates.json.gz`. بصمةُ المخرَج: `688459656128b669`.

| المسار في المخرَج | الرقم |
|---|---|
| `atoms` | 99,130 |
| `by_makhraj.len` | 15 |
| `furu` | 14 |
| `jahr_agree` | 28 |
| `lam_atoms` | 7,319 |
| `lips_agree` | 0 |
| `makharij` | 15 |
| `sifat_atoms.len` | 13 |
| `sifat_atoms.sum` | 351,111 |
| `stated` | 16 |

### `tools/gen_mansubat_index.py::measure`

يقرأ: `masaq-mansubat.json`. بصمةُ المخرَج: `88b5de544f470f4b`.

| المسار في المخرَج | الرقم |
|---|---|
| `case.('تمييز', 'جرّ')` | 14 |
| `case.('تمييز', 'موافق')` | 38 |
| `case.('حال', 'لا تقرؤه الخانة')` | 15 |
| `case.('حال', 'موافق')` | 275 |
| `case.('مستثنى', 'رفع')` | 2 |
| `case.('مستثنى', 'لا تقرؤه الخانة')` | 1 |
| `case.('مستثنى', 'موافق')` | 38 |
| `illa.('مثبت', 'بدل')` | 4 |
| `illa.('مثبت', 'حسب موقعه')` | 74 |
| `illa.('مثبت', 'غير اسم')` | 25 |
| `illa.('مثبت', 'مستثنى')` | 83 |
| `illa.('منفيّ', 'بدل')` | 47 |
| `illa.('منفيّ', 'حسب موقعه')` | 271 |
| `illa.('منفيّ', 'غير اسم')` | 127 |
| `illa.('منفيّ', 'مستثنى')` | 30 |
| `mabni` | 125 |
| `n` | 508 |
| `n_illa` | 661 |
| `nakira.('تمييز', False)` | 2 |
| `nakira.('تمييز', True)` | 50 |
| `nakira.('حال', False)` | 53 |
| `nakira.('حال', True)` | 237 |
| `sort.('تمييز', 'جامد')` | 50 |
| `sort.('تمييز', 'غيره')` | 1 |
| `sort.('تمييز', 'مشتق')` | 1 |
| `sort.('حال', 'جامد')` | 77 |
| `sort.('حال', 'غيره')` | 5 |
| `sort.('حال', 'مشتق')` | 208 |
| `templ.('تمييز', False)` | 45 |
| `templ.('تمييز', True)` | 7 |
| `templ.('حال', False)` | 90 |
| `templ.('حال', True)` | 200 |

### `tools/gen_maqam_index.py::measure`

يقرأ: `masaq-filiyya.json.gz`. بصمةُ المخرَج: `7830c4f605575193`.

| المسار في المخرَج | الرقم |
|---|---|
| `attach.خالف` | 2,471 |
| `attach.وافق` | 14,256 |
| `n` | 16,727 |
| `person.خالف` | 32 |
| `person.لم يُقرأ` | 560 |
| `person.وافق` | 596 |
| `read.غائب` | 4,768 |
| `read.متكلم` | 716 |
| `read.مخاطب` | 1,531 |
| `read.مخاطب/غائبة` | 119 |
| `read.—` | 9,593 |
| `zahir.حاضر` | 10 |
| `zahir.غائب` | 560 |
| `zahir.لم يُقرأ` | 1,334 |

### `tools/gen_maqayis_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `fbc34b1d380acbfb`.

| المسار في المخرَج | الرقم |
|---|---|
| `a.among` | 11,540 |
| `a.dropped` | 715 |
| `a.match` | 17,657 |
| `a.none` | 4,844 |
| `a.wrong` | 5,975 |
| `after.1` | 12,476 |
| `after.2` | 2,282 |
| `after.3+` | 915 |
| `attested_readings` | 17,752 |
| `b.among` | 14,329 |
| `b.match` | 15,583 |
| `b.none` | 4,844 |
| `b.wrong` | 5,975 |
| `before.1` | 11,366 |
| `before.2` | 2,659 |
| `before.3+` | 1,648 |
| `dropped[0][1]` | 217 |
| `dropped[1][1]` | 33 |
| `dropped[2][1]` | 20 |
| `dropped[3][1]` | 13 |
| `dropped[4][1]` | 10 |
| `dropped[5][1]` | 10 |
| `dropped[6][1]` | 9 |
| `dropped[7][1]` | 8 |
| `forms` | 18,179 |
| `masaq` | 40,731 |
| `none_attested` | 2,223 |
| `roots` | 4,561 |
| `total_readings` | 24,531 |

### `tools/gen_marifa_index.py::measure`

يقرأ: `masaq-marifa.json`. بصمةُ المخرَج: `407de8606a03d893`.

| المسار في المخرَج | الرقم |
|---|---|
| `[0].('علم', False)` | 122 |
| `[0].('علم', True)` | 35 |
| `[0].('غير ذلك (نكرةٌ غالبًا)', False)` | 681 |
| `[0].('غير ذلك (نكرةٌ غالبًا)', True)` | 1,559 |
| `[0].('مضاف إلى ضمير', False)` | 1,248 |
| `[0].('مضاف إلى ضمير', True)` | 3 |
| `[0].('مضاف', False)` | 1,002 |
| `[0].('مضاف', True)` | 9 |
| `[0].('معرَّف بأل', False)` | 1,884 |
| `[0].('معرَّف بأل', True)` | 1 |
| `[1]` | 6,544 |

### `tools/gen_mukhassas_index.py::measure`

يقرأ: `corpus-certificates.json.gz`. بصمةُ المخرَج: `7aeb2e2923000384`.

| المسار في المخرَج | الرقم |
|---|---|
| `attested.len` | 328 |
| `books.len` | 73 |
| `by_level.1` | 73 |
| `by_level.2` | 337 |
| `by_level.3` | 1,190 |
| `distinct` | 608 |
| `linked` | 1,080 |
| `unlinked` | 926 |
| `verb_roots.len` | 1,128 |
| `verb_roots.sum` | 6,519 |

### `tools/gen_naat_index.py::measure`

يقرأ: `masaq-tawabi.json`. بصمةُ المخرَج: `f100e721bbf6092b`.

| المسار في المخرَج | الرقم |
|---|---|
| `case.خالف` | 255 |
| `case.لم يُقرأ` | 333 |
| `case.وافق` | 2,188 |
| `coords.الإعراب` | 108 |
| `coords.الإعرابُ لا يُقرأ` | 309 |
| `coords.التعريف` | 162 |
| `coords.الجنس` | 56 |
| `coords.العدد` | 76 |
| `def.خالف` | 167 |
| `def.وافق` | 2,609 |
| `n` | 3,179 |
| `read.('اسم معطوف', False)` | 836 |
| `read.('اسم معطوف', True)` | 656 |
| `read.('بدل', False)` | 144 |
| `read.('بدل', True)` | 117 |
| `read.('توكيد', False)` | 18 |
| `read.('توكيد', True)` | 20 |
| `read.('نعت', False)` | 711 |
| `read.('نعت', True)` | 677 |

### `tools/gen_nawasikh_index.py::measure`

يقرأ: `masaq-nawasikh.json`. بصمةُ المخرَج: `2480c701e34d4fdd`.

| المسار في المخرَج | الرقم |
|---|---|
| `ba` | 84 |
| `detail.('اسم حرف ناسخ', 'جرّ')` | 26 |
| `detail.('اسم حرف ناسخ', 'رفع')` | 3 |
| `detail.('اسم فعل ناسخ', 'جرّ')` | 15 |
| `detail.('اسم فعل ناسخ', 'نصب')` | 3 |
| `detail.('اسم فعل ناسخ', 'نصب/جرّ')` | 4 |
| `detail.('خبر حرف ناسخ', 'جرّ')` | 9 |
| `detail.('خبر حرف ناسخ', 'نصب')` | 2 |
| `detail.('خبر حرف ناسخ', 'نصب/جرّ')` | 2 |
| `detail.('خبر فعل ناسخ', 'جرّ')` | 1 |
| `detail.('خبر فعل ناسخ', 'رفع')` | 1 |
| `innama.('أنما', 'حرف جر')` | 1 |
| `innama.('أنما', 'فعل مضارع')` | 3 |
| `innama.('إنما', 'حرف جر')` | 1 |
| `innama.('إنما', 'فعل ماضٍ')` | 3 |
| `innama.('إنما', 'فعل مضارع مبني للمجهول')` | 3 |
| `innama.('إنما', 'فعل مضارع')` | 5 |
| `innama.('إنما', 'مبتدأ')` | 11 |
| `kada.('طفق', False)` | 3 |
| `kada.('عسى', False)` | 3 |
| `kada.('عسى', True)` | 21 |
| `kada.('كاد', False)` | 23 |
| `la_ok` | 73 |
| `lemmas.len` | 40 |
| `lemmas.sum` | 3,578 |
| `mabni` | 273 |
| `n` | 2,599 |
| `n_la` | 73 |
| `table.len` | 14 |
| `table.sum` | 2,242 |

### `tools/gen_nida_index.py::measure`

يقرأ: `masaq-munada.json`. بصمةُ المخرَج: `282d9f9689ee6afa`.

| المسار في المخرَج | الرقم |
|---|---|
| `[0].('لا تقرؤه الخانة', 'مبني', 'غير مضاف')` | 38 |
| `[0].('لا تقرؤه الخانة', 'معرب', 'مضاف')` | 25 |
| `[0].('مبني على الضم', 'مبني', 'غير مضاف')` | 188 |
| `[0].('مضاف إلى ياء محذوفة', 'مبني', 'غير مضاف')` | 17 |
| `[0].('مضاف إلى ياء محذوفة', 'مبني', 'مضاف')` | 1 |
| `[0].('مضاف إلى ياء محذوفة', 'معرب', 'مضاف')` | 104 |
| `[0].('معرب منصوب', 'مبني', 'غير مضاف')` | 25 |
| `[0].('معرب منصوب', 'معرب', 'غير مضاف')` | 2 |
| `[0].('معرب منصوب', 'معرب', 'مضاف')` | 88 |
| `[0].('نكرة غير مقصودة (منصوب)', 'مبني', 'غير مضاف')` | 1 |
| `[1]` | 489 |

### `tools/gen_nisab_index.py::measure`

يقرأ: `masaq-filiyya.json.gz`، `masaq-jumla.json`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `65eda71af5c5ea54`.

| المسار في المخرَج | الرقم |
|---|---|
| `depths.0` | 1 |
| `depths.1` | 25 |
| `depths.2` | 20 |
| `depths.3` | 45 |
| `depths.4` | 25 |
| `depths.5` | 9 |
| `pairs` | 10,149 |
| `read.('إسناد: فعل وفاعل', 'إسناد')` | 1,226 |
| `read.('إسناد: فعل وفاعل', 'تقييد')` | 271 |
| `read.('إسناد: فعل وفاعل', '—')` | 804 |
| `read.('إسناد: مبتدأ وخبر', 'إسناد')` | 1,416 |
| `read.('إسناد: مبتدأ وخبر', 'تقييد')` | 143 |
| `read.('إسناد: مبتدأ وخبر', '—')` | 84 |
| `read.('تقييد: مضاف إليه أو مجرور', 'إسناد')` | 460 |
| `read.('تقييد: مضاف إليه أو مجرور', 'تقييد')` | 1,735 |
| `read.('تقييد: مضاف إليه أو مجرور', '—')` | 539 |
| `read.('تقييد: مفعول به', 'إسناد')` | 712 |
| `read.('تقييد: مفعول به', 'تقييد')` | 1,955 |
| `read.('تقييد: مفعول به', '—')` | 804 |

### `tools/gen_pipeline_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `7d8757a3f0117525`.

| المسار في المخرَج | الرقم |
|---|---|
| `asked` | 10,445 |
| `content` | 26,418 |
| `masaq` | 40,731 |
| `ranked.content_passed` | 3,023 |
| `ranked.funnel[0]` | 40,731 |
| `ranked.funnel[1]` | 40,731 |
| `ranked.funnel[2]` | 34,237 |
| `ranked.funnel[3]` | 13,087 |
| `ranked.funnel[4]` | 8,104 |
| `ranked.funnel[5]` | 3,023 |
| `ranked.stops.CASE_MISMATCH` | 1,080 |
| `ranked.stops.CASE_NOT_READ` | 3,903 |
| `ranked.stops.JIHA_MISMATCH` | 7,953 |
| `ranked.stops.NISBA_MISMATCH` | 908 |
| `ranked.stops.NOT_IN_CERTIFICATES` | 0 |
| `ranked.stops.NO_JIHA_IN_REFERENCE` | 13,197 |
| `ranked.stops.NO_NISBA_IN_REFERENCE` | 4,173 |
| `ranked.stops.NO_READING` | 1,803 |
| `ranked.stops.PARTICLE_NOT_IN_TABLE` | 151 |
| `ranked.stops.PASSED` | 3,023 |
| `ranked.stops.READING_NOT_GOLD` | 4,540 |
| `ranked.stops.SEGMENTS_TIE` | 0 |
| `strict.content_passed` | 3,070 |
| `strict.funnel[0]` | 40,731 |
| `strict.funnel[1]` | 40,731 |
| `strict.funnel[2]` | 34,206 |
| `strict.funnel[3]` | 13,260 |
| `strict.funnel[4]` | 8,165 |
| `strict.funnel[5]` | 3,070 |
| `strict.stops.CASE_MISMATCH` | 963 |
| `strict.stops.CASE_NOT_READ` | 4,132 |
| `strict.stops.JIHA_MISMATCH` | 7,854 |
| `strict.stops.NISBA_MISMATCH` | 911 |
| `strict.stops.NOT_IN_CERTIFICATES` | 0 |
| `strict.stops.NO_JIHA_IN_REFERENCE` | 13,092 |
| `strict.stops.NO_NISBA_IN_REFERENCE` | 4,184 |
| `strict.stops.NO_READING` | 1,803 |
| `strict.stops.PARTICLE_NOT_IN_TABLE` | 151 |
| `strict.stops.PASSED` | 3,070 |
| `strict.stops.READING_NOT_GOLD` | 2,891 |
| `strict.stops.SEGMENTS_TIE` | 1,680 |

### `tools/gen_sarf_index.py::measure`

يقرأ: `masaq-sarf.json`. بصمةُ المخرَج: `0a3136c06bb018de`.

| المسار في المخرَج | الرقم |
|---|---|
| `[0].len` | 14 |
| `[0].sum` | 754 |
| `[1].ألف التأنيث الممدودة` | 3 |
| `[1].ألف ونون زائدتان` | 3 |
| `[1].صيغة منتهى الجموع` | 6 |
| `[1].معجم` | 27 |
| `[1].وزن أَفْعَل/فَعْلَان (صفةٌ أو علم)` | 5 |
| `[3]` | 754 |

### `tools/gen_sawabiq_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `6a1a4d26b7267a13`.

| المسار في المخرَج | الرقم |
|---|---|
| `agree` | 7,438 |
| `asked` | 7,654 |
| `by_kind.AL[0]` | 5,711 |
| `by_kind.AL[1]` | 5,707 |
| `by_kind.BA_JARR[0]` | 1,543 |
| `by_kind.BA_JARR[1]` | 1,436 |
| `by_kind.LAM_AMR[0]` | 40 |
| `by_kind.LAM_AMR[1]` | 26 |
| `by_kind.LAM_JARR[0]` | 527 |
| `by_kind.LAM_JARR[1]` | 465 |
| `by_kind.LAM_KAY[0]` | 302 |
| `by_kind.LAM_KAY[1]` | 295 |
| `by_kind.WASL_FIL[0]` | 138 |
| `by_kind.WASL_FIL[1]` | 114 |
| `forms` | 18,179 |
| `joined` | 2,289 |
| `kinds.AL` | 2,607 |
| `kinds.BA_JARR` | 526 |
| `kinds.LAM_AMR` | 211 |
| `kinds.LAM_JARR` | 287 |
| `kinds.LAM_KAY` | 255 |
| `kinds.WASL_FIL` | 1,591 |
| `kinds.WASL_ISM` | 13 |
| `lines[0]` | 8,658 |
| `lines[1]` | 8,686 |
| `lines[2]` | 17,502 |
| `lines[3]` | 17,564 |
| `lines[4]` | 18,330 |
| `mabni` | 575 |
| `multi` | 511 |
| `none` | 138 |
| `other` | 78 |
| `read` | 4,947 |
| `table` | 11 |
| `unread_top[0][1]` | 6 |
| `unread_top[1][1]` | 5 |
| `unread_top[2][1]` | 5 |
| `unread_top[3][1]` | 4 |
| `unread_top[4][1]` | 4 |
| `unread_top[5][1]` | 4 |
| `unread_top[6][1]` | 3 |
| `unread_top[7][1]` | 3 |
| `unread_top[8][1]` | 3 |
| `unread_top[9][1]` | 3 |
| `unread_top[10][1]` | 2 |
| `unread_top[11][1]` | 2 |

### `tools/gen_shibh_index.py::measure`

يقرأ: `masaq-shibh.json.gz`. بصمةُ المخرَج: `494f1b72c4c98eff`.

| المسار في المخرَج | الرقم |
|---|---|
| `anchor.len` | 16 |
| `anchor.sum` | 1,231 |
| `kinds.('جار ومجرور', 'جار ومجرور')` | 8,075 |
| `kinds.('جار ومجرور', '—')` | 4,327 |
| `kinds.('ظرف', 'جار ومجرور')` | 18 |
| `kinds.('ظرف', 'ظرف')` | 1,375 |
| `kinds.('ظرف', '—')` | 640 |
| `mahall.len` | 24 |
| `mahall.sum` | 1,231 |
| `majrur.جرّ` | 5,392 |
| `majrur.رفع` | 163 |
| `majrur.لا تقرؤه الخانة` | 1,015 |
| `majrur.نصب` | 1,191 |
| `majrur.نصب/جرّ` | 148 |
| `n` | 40,731 |
| `restored` | 4,752 |
| `zarf.('ظرف زمان', 'جار ومجرور')` | 1 |
| `zarf.('ظرف زمان', 'ظرف')` | 916 |
| `zarf.('ظرف زمان', '—')` | 392 |
| `zarf.('ظرف مكان', 'جار ومجرور')` | 17 |
| `zarf.('ظرف مكان', 'ظرف')` | 459 |
| `zarf.('ظرف مكان', '—')` | 248 |

### `tools/gen_siyaq_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `context-certificates.json.gz`. بصمةُ المخرَج: `1b6242193332c886`.

| المسار في المخرَج | الرقم |
|---|---|
| `both_ready` | 78,188 |
| `hidden_by_pause.تنوين ضم` | 619 |
| `hidden_by_pause.تنوين فتح` | 921 |
| `hidden_by_pause.تنوين كسر` | 469 |
| `hidden_by_pause.ضم` | 355 |
| `hidden_by_pause.فتح` | 2,850 |
| `hidden_by_pause.كسر` | 601 |
| `junctions.FARQ_ALIF_DROPPED` | 28 |
| `junctions.MADD_DROPPED` | 2,683 |
| `junctions.SAKIN_KASRA` | 46 |
| `lift_bad` | 127 |
| `lift_bad_top[0][1]` | 18 |
| `lift_bad_top[1][1]` | 15 |
| `lift_bad_top[2][1]` | 15 |
| `lift_bad_top[3][1]` | 14 |
| `lift_bad_top[4][1]` | 8 |
| `lift_bad_top[5][1]` | 5 |
| `lift_bad_top[6][1]` | 5 |
| `lift_bad_top[7][1]` | 4 |
| `lift_bad_top[8][1]` | 4 |
| `lift_bad_top[9][1]` | 3 |
| `lift_ok` | 10,761 |
| `lift_pairs.فتح ← ضم` | 14 |
| `lift_pairs.فتح ← كسر` | 113 |
| `named` | 78,188 |
| `refusals.DEFER:UNVOCALIZED_WORD_IS_NEVER_GUESSED` | 30 |
| `refusals.REJECT:INITIAL_SUKUN_WITHOUT_REPAIR` | 7 |
| `refusals.REJECT:JUNCTION_NOT_LICENSED` | 7 |
| `refusals.REJECT:JUNCTION_NOT_LICENSED,CVVC_NOT_GEMINATE` | 1 |
| `refusals.REJECT:JUNCTION_NOT_LICENSED,NOT_PAUSE_LICENSED` | 1 |
| `refusals.REJECT:NOT_CONTINUE_LICENSED_AFTER_REPAIR` | 1 |
| `refusals.REJECT:TANWIN_WITH_ANOTHER_HARAKA` | 8 |
| `relation.ساقطة الوصل` | 9,395 |
| `relation.ساقطة الوصل، وقف ألف` | 1 |
| `relation.ساقطة الوصل، وقف حذف` | 5 |
| `relation.ساقطة الوصل، وقف سكون` | 1,445 |
| `relation.ساقطة الوصل، وقف هاء` | 42 |
| `relation.هي` | 62,978 |
| `relation.وقف ألف` | 911 |
| `relation.وقف حذف` | 1,018 |
| `relation.وقف سكون` | 2,313 |
| `relation.وقف هاء` | 80 |
| `restored` | 78,061 |
| `status.ابتداءً جاهز، سياقًا جاهز` | 78,188 |
| `status.ابتداءً جاهز، سياقًا مرفوض` | 19 |
| `status.ابتداءً مرفوض، سياقًا جاهز` | 2 |
| `status.ابتداءً مرفوض، سياقًا مرفوض` | 36 |
| `tokens` | 78,245 |

### `tools/gen_tabayun_index.py::measure`

يقرأ: `masaq-shibh.json.gz`. بصمةُ المخرَج: `6d974b6ba552e2af`.

| المسار في المخرَج | الرقم |
|---|---|
| `families.len` | 589 |
| `families.sum` | 975 |
| `forms` | 988 |
| `isolated` | 81 |
| `pairs.متباينان` | 486,737 |
| `pairs.متداخلان` | 14 |
| `pairs.متّحدا المادّة` | 827 |
| `sizes.1` | 408 |
| `sizes.10` | 2 |
| `sizes.2` | 88 |
| `sizes.3` | 41 |
| `sizes.4` | 24 |
| `sizes.5` | 12 |
| `sizes.6` | 9 |
| `sizes.7` | 3 |
| `sizes.8` | 1 |
| `sizes.9` | 1 |

### `tools/gen_talab_index.py::measure`

يقرأ: `masaq-jazm.json`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `060993d67355ac1a`.

| المسار في المخرَج | الرقم |
|---|---|
| `before.بعد الواو أو الفاء` | 69 |
| `before.في الصدر` | 2 |
| `lam_n` | 71 |
| `markers.السكون` | 38 |
| `markers.حذف النون` | 21 |
| `markers.حذف حرف العلة` | 12 |
| `read.('اسم فعل أمر', 'اسم فعل')` | 1 |
| `read.('فعل أمر', 'صيغة')` | 123 |
| `read.('فعل أمر', '—')` | 145 |

### `tools/gen_talil_index.py::measure`

يقرأ: `masaq-filiyya.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `5bfcb4daeaea5ad3`.

| المسار في المخرَج | الرقم |
|---|---|
| `cases.منصوب` | 38 |
| `derives` | 345 |
| `pairs` | 5,593 |
| `read.('اسم مجرور بـ لِ/بِ', 'تعليل بالحرف')` | 359 |
| `read.('اسم مجرور بـ لِ/بِ', '—')` | 2,528 |
| `read.('مفعول به', 'مفعول لأجله')` | 161 |
| `read.('مفعول به', '—')` | 2,457 |
| `read.('مفعول لأجله', 'مفعول لأجله')` | 27 |
| `read.('مفعول لأجله', '—')` | 11 |
| `read.('مفعول مطلق', 'مفعول لأجله')` | 10 |
| `read.('مفعول مطلق', '—')` | 40 |

### `tools/gen_tawabi_index.py::measure`

يقرأ: `masaq-tawabi.json`. بصمةُ المخرَج: `d29a2c29d5bbd7b9`.

| المسار في المخرَج | الرقم |
|---|---|
| `[0].('اسم معطوف', 'لا تقرؤه الخانة')` | 315 |
| `[0].('اسم معطوف', 'مخالف')` | 404 |
| `[0].('اسم معطوف', 'موافق')` | 773 |
| `[0].('بدل', 'لا تقرؤه الخانة')` | 81 |
| `[0].('بدل', 'مخالف')` | 46 |
| `[0].('بدل', 'موافق')` | 134 |
| `[0].('توكيد', 'لا تقرؤه الخانة')` | 6 |
| `[0].('توكيد', 'مخالف')` | 12 |
| `[0].('توكيد', 'موافق')` | 20 |
| `[0].('نعت', 'لا تقرؤه الخانة')` | 309 |
| `[0].('نعت', 'مخالف')` | 206 |
| `[0].('نعت', 'موافق')` | 873 |
| `[1].len` | 24 |
| `[1].sum` | 668 |
| `[2]` | 3,179 |

### `tools/gen_tawzi_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `b3f82e98b1ce45ad`.

| المسار في المخرَج | الرقم |
|---|---|
| `forms` | 18,179 |
| `gold` | 13,151 |
| `kinds.إشارة` | 45 |
| `kinds.استفهام` | 27 |
| `kinds.حرف` | 587 |
| `kinds.ضمير` | 44 |
| `kinds.ظرف` | 141 |
| `kinds.موصول` | 10 |
| `kinds_table.إشارة` | 23 |
| `kinds_table.استفهام` | 14 |
| `kinds_table.حرف` | 82 |
| `kinds_table.ضمير` | 24 |
| `kinds_table.ظرف` | 92 |
| `kinds_table.موصول` | 11 |
| `masaq_particles` | 14,313 |
| `multi` | 45 |
| `none` | 507 |
| `read` | 854 |
| `table` | 246 |
| `unread_by_tag[0][1]` | 195 |
| `unread_by_tag[1][1]` | 82 |
| `unread_by_tag[2][1]` | 65 |
| `unread_by_tag[3][1]` | 48 |
| `unread_by_tag[4][1]` | 32 |
| `unread_by_tag[5][1]` | 22 |
| `unread_by_tag[6][1]` | 11 |
| `unread_by_tag[7][1]` | 10 |
| `unread_top[0][1]` | 59 |
| `unread_top[1][1]` | 46 |
| `unread_top[2][1]` | 43 |
| `unread_top[3][1]` | 36 |
| `unread_top[4][1]` | 33 |
| `unread_top[5][1]` | 31 |
| `unread_top[6][1]` | 24 |
| `unread_top[7][1]` | 18 |
| `unread_top[8][1]` | 11 |
| `unread_top[9][1]` | 10 |
| `unread_top[10][1]` | 8 |
| `unread_top[11][1]` | 8 |
| `with_pre` | 386 |
| `with_suf` | 389 |
| `wrong` | 655 |

### `tools/gen_uslub_index.py::measure`

يقرأ: `masaq-shibh.json.gz`. بصمةُ المخرَج: `4b9ab1671fd49cbd`.

| المسار في المخرَج | الرقم |
|---|---|
| `n` | 326 |
| `read.('أمر', 'إنشاء', 'أمر')` | 123 |
| `read.('أمر', 'إنشاء', 'خبر')` | 13 |
| `read.('أمر', 'إنشاء', '—')` | 132 |
| `read.('استفهام', 'إنشاء', 'استفهام')` | 23 |
| `read.('استفهام', 'إنشاء', '—')` | 1 |
| `read.('لَا', 'نفي (خبر)', 'خبر')` | 14 |
| `read.('لَا', 'نفي (خبر)', '—')` | 3 |
| `read.('لَا', 'نهي (إنشاء)', 'خبر')` | 7 |
| `read.('لَا', 'نهي (إنشاء)', 'نهي')` | 7 |
| `read.('لَا', 'نهي (إنشاء)', '—')` | 3 |
| `truth.('إنشاء', False)` | 279 |
| `truth.('إنشاء', True)` | 13 |
| `truth.('نفي (خبر)', False)` | 3 |
| `truth.('نفي (خبر)', True)` | 14 |
| `truth.('نهي (إنشاء)', False)` | 10 |
| `truth.('نهي (إنشاء)', True)` | 7 |

### `tools/gen_wad_index.py::measure`

يقرأ: `masaq-shibh.json.gz`. بصمةُ المخرَج: `f7832698b4f56a1b`.

| المسار في المخرَج | الرقم |
|---|---|
| `dist.مجدوَل` | 2,389 |
| `dist.مشترك الصورة` | 115 |
| `dist.مشترك الوضع` | 48 |
| `dist.مفرد الوضع` | 3,019 |
| `dist.—` | 9,689 |
| `n` | 15,260 |
| `sura.((11, 12), 'علَم')` | 87 |
| `sura.((11, 12), 'فعل')` | 3 |
| `sura.((16, 17), 'فعل')` | 3 |
| `sura.((50, 84), 'جامد/جمع')` | 16 |
| `sura.((55, 84), 'جامد/جمع')` | 2 |
| `sura.((80, 84), 'جامد/جمع')` | 2 |
| `sura.((80, 84), 'مشتقّ')` | 1 |
| `sura.((95, 98), 'جامد/جمع')` | 1 |
| `wad.((30, 94), 'جامد/جمع')` | 11 |
| `wad.((30, 94), 'مشتقّ')` | 2 |
| `wad.((30, 94), 'مصدر')` | 2 |
| `wad.((35, 41, 93), 'جامد/جمع')` | 22 |
| `wad.((35, 41, 93), 'مشتقّ')` | 1 |
| `wad.((35, 41, 93), 'مصدر')` | 3 |
| `wad.((51, 60), 'جامد/جمع')` | 7 |

### `tools/gen_wasl_index.py::measure`

يقرأ: `masaq-hamza.json`. بصمةُ المخرَج: `c2f97d35281c6442`.

| المسار في المخرَج | الرقم |
|---|---|
| `agree` | 5,811 |
| `kinds.قطع` | 12,319 |
| `kinds.قطع بعد ال` | 980 |
| `kinds.محذوفة رسمًا` | 8 |
| `kinds.محذوفة رسمًا (ال)` | 111 |
| `kinds.وصل` | 1,711 |
| `kinds.وصل ساقط` | 381 |
| `kinds.وصل ساقط (ال)` | 562 |
| `n` | 16,072 |
| `read` | 5,915 |
| `reader.len` | 35 |
| `reader.sum` | 14,010 |
| `ten.('ابن', 'وصل')` | 32 |
| `ten.('اثنان', 'وصل')` | 1 |
| `ten.('اسم', 'وصل')` | 14 |
| `ten.('امرؤ', 'وصل')` | 1 |

### `tools/gen_wujud_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-shibh.json.gz`. بصمةُ المخرَج: `24114f2cd471586a`.

| المسار في المخرَج | الرقم |
|---|---|
| `after.len` | 16 |
| `after.sum` | 23,977 |
| `before.len` | 16 |
| `before.sum` | 23,977 |
| `classes.اسم` | 4 |
| `classes.جمع` | 30 |
| `classes.ظرف وآلة` | 7 |
| `classes.فعل` | 37 |
| `classes.مصدر` | 22 |
| `classes.وصف` | 25 |
| `dist.اسم` | 881 |
| `dist.جمع` | 1,813 |
| `dist.ظرف وآلة` | 155 |
| `dist.فعل` | 7,445 |
| `dist.مصدر` | 2,944 |
| `dist.وصف` | 2,435 |
| `dist.—` | 2,506 |
| `forms` | 18,179 |
| `masaq` | 25,799 |
| `none` | 1,822 |

### `tools/gen_zawaid_index.py::measure`

يقرأ: `corpus-certificates.json.gz`، `masaq-zawaid.json`. بصمةُ المخرَج: `54df0fb6bb5f5171`.

| المسار في المخرَج | الرقم |
|---|---|
| `cells` | 40 |
| `end_ta` | 224 |
| `end_thaqila` | 267 |
| `masaq.EMPHATIC_NUN.agree` | 160 |
| `masaq.EMPHATIC_NUN.cells` | 239 |
| `masaq.EMPHATIC_NUN.n` | 240 |
| `masaq.PROTECT_NUN.agree` | 109 |
| `masaq.PROTECT_NUN.cells` | 219 |
| `masaq.PROTECT_NUN.n` | 220 |
| `masaq.SUFF_FEM_TA.agree` | 348 |
| `masaq.SUFF_FEM_TA.cells` | 643 |
| `masaq.SUFF_FEM_TA.n` | 646 |
| `ta_verb` | 156 |
| `table[0][2][0]` | 1 |
| `table[0][2][1]` | 4 |
| `table[0][3]` | 5 |
| `table[1][2][0]` | 2 |
| `table[1][2][1]` | 3 |
| `table[1][2][2]` | 4 |
| `table[1][2][3]` | 5 |
| `table[1][3]` | 7 |
| `table[2][3]` | 1 |
| `table[3][2][0]` | 1 |
| `table[3][2][1]` | 4 |
| `table[3][2][2]` | 2 |
| `table[3][2][3]` | 3 |
| `table[3][2][4]` | 5 |
| `table[3][3]` | 7 |
| `table[4][2][0]` | 5 |
| `table[4][2][1]` | 6 |
| `table[4][2][2]` | 4 |
| `table[4][2][3]` | 1 |
| `table[4][2][4]` | 2 |
| `table[4][2][5]` | 3 |
| `table[4][3]` | 8 |
| `table[5][2][0]` | 4 |
| `table[5][2][1]` | 5 |
| `table[5][2][2]` | 6 |
| `table[5][2][3]` | 1 |
| `table[5][3]` | 5 |
| `table[6][3]` | 1 |
| `table[7][2][0]` | 1 |
| `table[7][3]` | 3 |
| `table[8][2][0]` | 2 |
| `table[8][2][1]` | 3 |
| `table[8][2][2]` | 4 |
| `table[8][2][3]` | 5 |
| `table[8][3]` | 5 |
| `table[9][3]` | 1 |
| `thaqila_verb` | 96 |
| `witness_linked` | 36 |
| `witness_read` | 4 |
| `witness_words` | 48 |

### `tools/gen_zuruf_index.py::measure`

يقرأ: `masaq-zuruf.json`. بصمةُ المخرَج: `0735d182399bde88`.

| المسار في المخرَج | الرقم |
|---|---|
| `[0].len` | 21 |
| `[0].sum` | 1,493 |
| `[1]` | 1,493 |
