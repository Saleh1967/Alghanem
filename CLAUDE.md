# تعليماتٌ لكلّ وكيلٍ قبل الدخول — مستودع SLGE

اقرأ هذا كلَّه قبل أيّ أمر. ما خالفه يُرفض بالاسم.

**دستورُ الوكيل** (ملزِمٌ لي قبل القانون الواحد وبعده): `AGENT_CONSTITUTION.md` في مستودع الغانم — سبعَ عشرةَ مادّةً في ثلاثة أبواب: تسعٌ ضدّ الهلوسة والغشّ الدستوريّ وفبركة الاختبارات وترك Lean؛ وخمسٌ تفصل الوضعَ عن المعلومات السابقة عن الحكم (الحكمُ فوق الترخيص لا فيه؛ الشهادةُ لا تأخذ العالمَ معاملًا؛ لا مودَعَ بلا نوع؛ الحكمُ ثلاثيٌّ لا يُسقط ترخيصًا؛ أركانُ العقل الأربعة شرطُ كلّ اقتراح)؛ وثلاثٌ لمراتب المخرج (من حيث هي / معلومة / مفهوم؛ لا «مفهوم» بلا شاهدِ واقعٍ مودَع؛ الدلالةُ من حيث هي بلا لافظٍ ولا سامع، وLean يُبرهن المرويَّ لا اللغة)، كلٌّ بفحصها الآليّ واسم مخالفتها.

## القانون الواحد

**لا يدخل هذه الشجرةَ نصٌّ، ولا يخرج منها نصّ. المدخلُ الوحيد شهادةُ بوّابة الغانم، والمخرجُ الوحيد ذرّاتُها بعينها.**

- النصُّ يدخل في مستودع الغانم وحدَه: `gate.enter(bytes) → Certificate | Refusal` (`Saleh1967/Alghanem`، فرع `claude/official-gate`، حزمة `gate/`، برهانُها `formal/a116`).
- السُّلَّمُ الفعليّ: `slge.gates.climb(cert.atoms)` تسعُ بوّاباتٍ متتابعة (الخانة، الترخيص، العدد حاكمةً؛ الجداول، الجذع، الأدوات، الصرف، الإعراب، الجواب قارئةً) — ولا بوّابةَ فوق مرفوضة (`Grant.ladder_implies_base`). وكلُّ وحدةٍ مسجَّلةٌ في `slge.manifest` بمواضعها، و`python tools/check_manifest.py` يشهد أنّها موصولةٌ في كلّ موضع (ADR ٦ في `ARCHITECTURE.md`).
- شهاداتُ المصحف كلِّه مودَعةٌ خاناتٍ وأعدادًا (`tests/data/corpus-certificates.json.gz`، بصمةُ المدوّنة فيه) وتُقاس على السُّلَّم في `BITS_INDEX.md`.
- هنا: `slge.entry.from_atoms(cert.atoms) → خانات`، و`slge.entry.to_atoms(خانات) → ذرّات` تعود إلى `gate.exit`. والطيُّ `to_integer/from_integer` مبرهَنٌ (`Slge.slgeFold_*`) على المرخَّص ثنائيًّا؛ وما رخّصه الثلاثيُّ وحدَه (كـ«حَاجَّ») يحمل عددَه في شهادته.
- الطبقاتُ الحيّة: `entry`، `cells`، `stream`، `categories`، `phonology`، `semantics`، `nazm`، `grant`، `wazn`، `shabaka`، `khamsa`، `afal`، `rawabit`، `damair`، `ishara`، `istifham`، `nida`، `zuruf`، `zaman`، `adad`، `marifa`، `sarf`، `tawabi`، `nawasikh`، `jazm`، `mansubat`، `majrurat`، `wasl`، `ism`، `fil`، `huruf`، `jumla`، `filiyya`، `shibh`، `nisab`، `talil`، `maqam`، `jiha`، `naat`، `uslub`، `talab`، `kulli`، `wad`، `tabayun`، `madd`، `ilal`، `jidh`، `maqayis_table`، `maqayis`، `abniya_table`، `abniya`، `adawat`، `wujud_table`، `wujud`، `maani_table`، `maani`، `mukhassas_table`، `mukhassas`، `knowledge`، `rank`، `learning`، `answer`، و`gates` (البوّاباتُ المتتابعة فوقها كلِّها) (و`order`، `status`، `guard`، `manifest` وصفًا). وفوق البوّابات طبقةُ **الحكم** (`order.LAYERS["الحكم"]`): ما يحكم على مطابقة النسبة للواقع المودَع لا يدخل سُلَّم الترخيص (دستور الوكيل، المادّتان ١٠ و١٣)؛ أوّلُ وحداتها `mukhassas` (بإذن المالك 2026-10-08، ADR ١٥): شجرةُ المخصّص كما هي وقابليّاتُ عناوينها بالرسم، والحكمُ على (كتاب، جذر) مرتبتين «مفهوم» بشاهدٍ أو «معلومة» بلا شاهد — لا رفضَ ولا امتناع (`Mukhassas.mafhum_has_witness`، `judge_total`)؛ وكلُّ مودَعٍ في `tests/data/` مسجَّلٌ بنوعه في `manifest.DEPOSITS` (المادّة ١٢)؛ والمختومُ بإذن المالك (المخصّص، مقاييس اللغة كاملًا، مجاز القرآن — OpenITI، CC BY-NC-SA 4.0) يحمل بصمتَه ورخصتَه ويفحصه `tests/test_seals.py`، وهو بايتاتٌ لا تقرؤها شيفرةٌ هنا إلّا أداةُ إيداعٍ معفاة تولّد جدولًا بـ`--check`. ما سواها **معلَّق** في `suspended/` بسجلٍّ (`SUSPENDED_REGISTRY.json`): `encoding`، `orthography`، `lexicon`، `morphology` — كانت تقرأ النصّ وتطبّعه خارج البوّابة.

## قانونُ القارئ (ملزِمٌ لكلّ وكيل؛ يفحصه `tests/test_gates.py::test_readers_under_the_law`)

لا يدخل قارئٌ جديدٌ هذه الشجرةَ إلّا بثلاثة معًا، وكلُّ قارئٍ يُسجَّل في `slge.manifest` بـ`law=True`:

1. **بوّابةٌ في `gates.LADDER` لا دالّةٌ منفردة**: يُستدعى من `slge/gates.py` في موضعه من السُّلَّم، فتمرّ عليه شهادةُ المصحف كاملةً في كلّ اختبار.
2. **مقيسٌ على شهادات المصحف الكاملة قبل أيّ شريحةٍ مقسومة**: فهرسُه يقرأ `tests/data/corpus-certificates.json.gz` (الصورُ بسوابقها ولواحقها) ويُثبت الرقمَ عليه؛ وشرائحُ MASAQ المقسومة قرينةٌ تالية لا مقياسٌ أوّل — فما يُقاس على الجذع لا يشهد على الكلمة.
3. **لا يطابق قالبًا إلّا بعد تسوية الآخر المبرهَنة** (`jidh.on_template_mod` ← `Jidh.onTemplateMod_setLast`): الإعرابُ والمزاجُ حالةُ الخانة الأخيرة لا جزءٌ من القالب؛ والزوائدُ عمليّاتٌ جبريّة مغلقةٌ صعودًا (الإلصاقُ يحفظ الترخيص: `prefix_licensed`، `Jumla.suffix_licensed`) ونزولًا (القطعُ عكسُها بعينه: `peelPrefix_append`، `peelSuffix_append`، `dropAl_al`)، والنزولُ يستوفي الصعود (`jidh_complete`): ما صعد بالجبر ينزل بالقارئ — لا بحثًا في جدولٍ يُفحص ردُّه. والإعلالُ والإبدالُ كذلك (`Slge.Ilal`، هندسةٌ عكسيّةٌ لـ`A116.Ilal`): القاعدةُ صعودٌ `up` ونزولٌ `down` عكسُه بعينه (`undo_sound`) لا يفوته أصلٌ (`undo_complete`)، مغلقٌ على الترخيص عبر الجسر إلى أدوات الغانم (`qalbAyn_closed`، `naql_closed`، `hadhfWaw_closed`، `ibdal_closed`، `hadhfAyn_forced`…)، والجذعُ ينزل به حتى خطوتين وكلُّ ما ينزل إليه يصعد بسلسلته (`jidh_ascends`، `jidh_complete_ilal`)، والردُّ بسجلّ الغانم بعينه مبرهَنٌ على خانات SLGE وخانات الغانم معًا (`apply_roundtrip`، `apply_roundtrip_a116`). الشروطُ اللغويّة (حرفُ المضارعة، ضمُّ اللام، مواضعُ النوافذ) معلَنةٌ لا مبرهَنة. والتعدّدُ الباقي ترتّبه **القرينةُ المعجميّة** (`Slge.Maqayis`): عضويّةُ جذر القراءة في مقاييس اللغة (4,561 جذرًا حواملَ، جدولٌ مولَّدٌ من مودَعٍ مختوم) دالّةٌ على الخانات (`member_sound`)، والترتيبُ المشهودُ أوّلًا لا يُسقط قراءةً ولا يزيدها (`mem_rank`، `length_rank`)؛ الجدولُ يفصل ما لم يُشهَد ولا يختار بين مشهودَين (قول/قيل). و**معاني الحرف الواحد** (`Slge.Maani`) منقولةٌ من مبحث الحرف في الشخصيّة ج3 بترتيب المصدر (مودَعٌ مختوم) وتُرتَّب بالقرينة (ظرفٌ بعده، نفيٌ قبله) لا تُختار: الأصلُ أوّلًا (`ghaya_first_in_source`) والترتيبُ لا يُسقط معنًى (`Maani.mem_rank`).

سببُ القانون مسجَّلٌ بالعدد في `ARCHITECTURE.md` (ADR ٧): القرّاءُ الذين بُنوا على الحصور المُرسَلة وقِيسوا على جذوعٍ مقسومة قرؤوا 1,743 صورةً من 18,179؛ وبعد التسوية والفصل 13,706.

## ما لا تفعله

1. لا تكتب `open`، `print`، `read_text`، `encode`، `decode`، `unicodedata.normalize`، `argv`… في `src/slge/` أو `tools/` (إلّا القائمة البيضاء في `slge.guard.EXEMPT_FILES`). الحارسُ `slge.guard.breaches()` يُسقط البناء.
2. لا تستورد `slge.encoding` ولا `slge.orthography` ولا `slge.lexicon` ولا `slge.morphology` ولا شيئًا من `suspended/`.
3. لا تستورد بوّابةَ الغانم هنا: الشهادةُ تصل بتّاتٍ (ذرّاتٍ وعددًا)؛ المستودعان منفصلان والبرهانُ مشترَكٌ بإيداعٍ مثبَّت (`formal/lake-manifest.json`).
4. لا تُعِد وحدةً من `suspended/` إلّا بثلاثة: (١) مدخلُها `slge.entry` على شهادةٍ لا نصّ، (٢) اختباراتٌ مستقلّةٌ عن شيفرتها مطعَّمةٌ بالطفرة (20/20)، (٣) ADR في `ARCHITECTURE.md`. ثمّ `python tools/gen_registry.py`.
5. لا تحرِّر `STATUS.md` ولا `LEAN_INDEX.md` ولا `RAWABIT_INDEX.md` ولا `DAMAIR_INDEX.md` ولا `ISHARA_INDEX.md` ولا `ISTIFHAM_INDEX.md` ولا `NIDA_INDEX.md` ولا `ZURUF_INDEX.md` ولا `ZAMAN_INDEX.md` ولا `ADAD_INDEX.md` ولا `MARIFA_INDEX.md` ولا `SARF_INDEX.md` ولا `TAWABI_INDEX.md` ولا `NAWASIKH_INDEX.md` ولا `JAZM_INDEX.md` ولا `MANSUBAT_INDEX.md` ولا `MAJRURAT_INDEX.md` ولا `WASL_INDEX.md` ولا `ISM_INDEX.md` ولا `FIL_INDEX.md` ولا `HURUF_INDEX.md` ولا `JUMLA_INDEX.md` ولا `FILIYYA_INDEX.md` ولا `SHIBH_INDEX.md` ولا `NISAB_INDEX.md` ولا `TALIL_INDEX.md` ولا `MAQAM_INDEX.md` ولا `JIHA_INDEX.md` ولا `NAAT_INDEX.md` ولا `USLUB_INDEX.md` ولا `TALAB_INDEX.md` ولا `KULLI_INDEX.md` ولا `WAD_INDEX.md` ولا `TABAYUN_INDEX.md` ولا `BITS_INDEX.md` ولا `MADD_INDEX.md` ولا `ILAL_INDEX.md` ولا `JIDH_INDEX.md` ولا `MAQAYIS_INDEX.md` ولا `ABNIYA_INDEX.md` ولا `ADAWAT_INDEX.md` ولا `WUJUD_INDEX.md` ولا `MAANI_INDEX.md` ولا `NABHANI_INDEX.md` ولا `MUKHASSAS_INDEX.md` ولا `SUSPENDED_REGISTRY.json` ولا `formal/out/*` بيدك؛ تُولَّد وتُطابَق.
6. لا تكتب في `status.py` وسمًا أقوى من سنده: «مبرهن» لما في Lean باسمه مدقَّقًا في `Audit.lean`؛ «مفحوص» لما له اختبارٌ باسمه؛ وما سندُه في `suspended/` يُوسَم «معلق» آليًّا (`status._suspend`). (الدعاوى المعروفةُ المبالغُ فيها سابقًا: Q22 دوريّ، Q3 بالبناء — لا تُعِدها.)
7. لا تدمج بلا إذن صاحب المستودع.

## قبل أن تقول «تمّ»

```sh
pip install -r requirements-dev.txt && pip install -e . --no-deps
ruff check . && mypy && pytest -q                     # 372 اختبارًا
python tools/gen_status.py --check
python tools/gen_registry.py --check
python tools/check_manifest.py && python tools/check_manifest.py --indexes   # السجلُّ وكلُّ الفهارس (بدل السطور أدناه واحدًا واحدًا)
python tools/gen_lean_index.py --check               # فهرسُ المبرهنات على درجات الترخيص (LEAN_INDEX.md)
python tools/gen_rawabit_index.py --check            # فهرسةُ أدوات الربط على الدرجات (RAWABIT_INDEX.md)
python tools/gen_damair_index.py --check             # فهرسُ الضمائر على الدرجات (DAMAIR_INDEX.md)
python tools/gen_ishara_index.py --check             # فهرسُ أسماء الإشارة على الدرجات (ISHARA_INDEX.md)
python tools/gen_istifham_index.py --check           # فهرسُ أسماء الاستفهام على الدرجات (ISTIFHAM_INDEX.md)
python tools/gen_nida_index.py --check               # فهرسُ النداء على الدرجات (NIDA_INDEX.md)
python tools/gen_zuruf_index.py --check              # فهرسُ ظروف المكان على الدرجات (ZURUF_INDEX.md)
python tools/gen_zaman_index.py --check              # فهرسُ ظروف الزمان على الدرجات (ZAMAN_INDEX.md)
python tools/gen_adad_index.py --check               # فهرسُ العدد على الدرجات (ADAD_INDEX.md)
python tools/gen_marifa_index.py --check             # فهرسُ المعارف على الدرجات (MARIFA_INDEX.md)
python tools/gen_sarf_index.py --check               # فهرسُ الممنوع من الصرف على الدرجات (SARF_INDEX.md)
python tools/gen_tawabi_index.py --check             # فهرسُ التوابع على الدرجات (TAWABI_INDEX.md)
python tools/gen_nawasikh_index.py --check           # فهرسُ النواسخ على الدرجات (NAWASIKH_INDEX.md)
python tools/gen_jazm_index.py --check               # فهرسُ الجزم والشرط على الدرجات (JAZM_INDEX.md)
python tools/gen_mansubat_index.py --check           # فهرسُ بقيّة المنصوبات على الدرجات (MANSUBAT_INDEX.md)
python tools/gen_majrurat_index.py --check           # فهرسُ المجرورات على الدرجات (MAJRURAT_INDEX.md)
python tools/gen_wasl_index.py --check               # فهرسُ همزتي الوصل والقطع على الدرجات (WASL_INDEX.md)
python tools/gen_ism_index.py --check                # فهرسُ الاسم على الدرجات (ISM_INDEX.md)
python tools/gen_fil_index.py --check                # فهرسُ الفعل على الدرجات (FIL_INDEX.md)
python tools/gen_huruf_index.py --check              # فهرسُ الحروف والأدوات على الدرجات (HURUF_INDEX.md)
python tools/gen_jumla_index.py --check              # فهرسُ الجملة الاسميّة على الدرجات (JUMLA_INDEX.md)
python tools/gen_filiyya_index.py --check            # فهرسُ الجملة الفعليّة على الدرجات (FILIYYA_INDEX.md)
python tools/gen_shibh_index.py --check              # فهرسُ شبه الجملة على الدرجات (SHIBH_INDEX.md)
python tools/gen_nisab_index.py --check              # فهرسُ النِّسَب الثلاث على الدرجات (NISAB_INDEX.md)
python tools/gen_talil_index.py --check              # فهرسُ التعليل والسببيّة على الدرجات (TALIL_INDEX.md)
python tools/gen_maqam_index.py --check              # فهرسُ المقام على الدرجات (MAQAM_INDEX.md)
python tools/gen_jiha_index.py --check               # فهرسُ الجهة والزمن على الدرجات (JIHA_INDEX.md)
python tools/gen_naat_index.py --check               # فهرسُ النعت والمطابقة الرباعيّة على الدرجات (NAAT_INDEX.md)
python tools/gen_uslub_index.py --check              # فهرسُ الأسلوب (الخبر والإنشاء) على الدرجات (USLUB_INDEX.md)
python tools/gen_talab_index.py --check              # فهرسُ الطلب (صور الأمر) على الدرجات (TALAB_INDEX.md)
python tools/gen_kulli_index.py --check              # فهرسُ الكليّ والجزئيّ على الدرجات (KULLI_INDEX.md)
python tools/gen_wad_index.py --check                # فهرسُ الوضع والمشترك والترادف على الدرجات (WAD_INDEX.md)
python tools/gen_tabayun_index.py --check            # فهرسُ المتباين على الدرجات (TABAYUN_INDEX.md)
python tools/gen_bits_index.py --check               # فهرسُ البتّات: شهاداتُ المصحف على الدرجات (BITS_INDEX.md)
python tools/gen_madd_index.py --check               # فهرسُ المدود على الدرجات (MADD_INDEX.md)
python tools/gen_jidh_index.py --check               # فهرسُ الجذع: الرقمُ قبل التسوية والفصل وبعدهما (JIDH_INDEX.md)
python tools/gen_ilal_index.py --check               # فهرسُ الإعلال: ما لا يُقرأ إلّا بالنزول، بقواعده (ILAL_INDEX.md)
python tools/gen_maqayis_index.py --check            # فهرسُ القرينة المعجميّة: المتعدّدُ قبل عضويّة المقاييس وبعدها (MAQAYIS_INDEX.md)
python tools/deposit_maqayis.py --check              # جدولا المقاييس (Lean وبايثون) مولَّدان من المودَع المختوم tests/data/maqayis-roots.json.gz
python tools/gen_abniya_index.py --check             # فهرسُ قوالب الاسم على أبنية سيبويه: أثرُ كلّ قالبٍ مضاف على المودَع (ABNIYA_INDEX.md)
python tools/deposit_abniya.py --check               # جدولا الأبنية (Lean وبايثون) مولَّدان من المودَع المختوم tests/data/sibawayh-abniya.tsv
python tools/gen_adawat_index.py --check             # فهرسُ الأدوات علاقاتٍ تشغيليّة: العملُ والترتيبُ على MASAQ (ADAWAT_INDEX.md)
python tools/gen_wujud_index.py --check              # فهرسُ الجهة الوجوديّة: المصدرُ والمشتقُّ والجامدُ على المودَع ووسوم MASAQ (WUJUD_INDEX.md)
python tools/deposit_wujud.py --check                # جدولا الوجود (Lean وبايثون) مولَّدان من أبواب الأوزان
python tools/gen_maani_index.py --check              # فهرسُ معاني الحروف: تعدّدُ معاني الحرف مرتَّبًا بالقرينة على MASAQ (MAANI_INDEX.md)
python tools/deposit_maani.py --check                # جدولا معاني الحروف (Lean وبايثون) مولَّدان من المودَع المختوم tests/data/nabhani-huruf.json
python tools/gen_nabhani_index.py --check            # فهرسُ المطابقة النبهانيّ ↔ الوحدات: لا إشارةَ إلى وحدةٍ أو مبرهنةٍ أو اختبارٍ لا وجودَ له (NABHANI_INDEX.md)
python tools/gen_mukhassas_index.py --check          # فهرسُ المخصّص: الشجرةُ كما هي، الربطُ بالرسم، القابليّاتُ الموروثة، الحكمُ بشاهد على المودَع (MUKHASSAS_INDEX.md)
python tools/deposit_mukhassas.py --check            # جدولا المخصّص (Lean وبايثون) مولَّدان من المختوم tests/data/openiti-mukhassas.txt.gz
python -c "from slge.guard import breaches; print(breaches() or 'لا خرق')"
cd formal && lake build && lake env lean Audit.lean   # 822 مدقَّقة (الـ116 وSLGE)؛ propext/Classical.choice/Quot.sound فقط
```

وافصل في جوابك ما فحصته الآلة عمّا استنتجتَه، وأثبت وجودَ كلّ ملفٍّ تذكره قبل الكلام عنه.

**المستودعاتُ المشمولة بهذا القانون:** الغانم (البوّابة)، SLGE (هذا)، hamil، Algebra، والدساتير الثلاثة. **Taaqol-GPT ليس منها.**
