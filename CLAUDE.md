# تعليماتٌ لكلّ وكيلٍ قبل الدخول — مستودع الغانم

اقرأ هذا كلَّه قبل أيّ أمر. ما خالفه يُرفض بالاسم، لا يُناقَش.

**دستورُ الوكيل** (ملزِمٌ لي قبل القانون الواحد وبعده): `AGENT_CONSTITUTION.md` في مستودع الغانم — سبعَ عشرةَ مادّةً في ثلاثة أبواب: تسعٌ ضدّ الهلوسة والغشّ الدستوريّ وفبركة الاختبارات وترك Lean؛ وخمسٌ تفصل الوضعَ عن المعلومات السابقة عن الحكم (الحكمُ فوق الترخيص لا فيه؛ الشهادةُ لا تأخذ العالمَ معاملًا؛ لا مودَعَ بلا نوع؛ الحكمُ ثلاثيٌّ لا يُسقط ترخيصًا؛ أركانُ العقل الأربعة شرطُ كلّ اقتراح)؛ وثلاثٌ لمراتب المخرج (من حيث هي / معلومة / مفهوم؛ لا «مفهوم» بلا شاهدِ واقعٍ مودَع؛ الدلالةُ من حيث هي بلا لافظٍ ولا سامع، وLean يُبرهن المرويَّ لا اللغة)، كلٌّ بفحصها الآليّ واسم مخالفتها.

## القانون الواحد

**لا يدخل إلى هذه الشجرة إلّا بتٌّ ولا يخرج منها إلّا بتّ، ومدخلُه ومخرجُه الوحيدان: البرهانُ في `formal/a116` ومرآتُه `gate/`.**

- المدخل: `gate.enter(bytes) → Certificate | Refusal`. الشهادةُ ذرّاتٌ من الـ116 وعددٌ يطويها؛ والرفضُ مسمًّى (`DEFER`، `REJECT`، `OUTSIDE_DECLARED_DOMAIN`) ولا يُخمَّن شيء.
- المخرج: `gate.exit(cert) → bytes` — الكلمةُ بعينها (`Fiber.decode_encode`).
- الاشتقاق: `gate.derive(root)`، والاسترجاع: `gate.recover(cert)`؛ كلاهما يُقاس على مرجعٍ بشريٍّ محجوب (MASAQ) لا على شيفرته.
- الترخيص: `gate.licence` — الثلاثيّ (`cv | v | c`) لا الثنائيّ؛ فالثنائيُّ أعمى عن المدّ (`Ternary.binary_is_blind_to_madd`).
- قيدُ الحدّ: قافيةُ المدّ (CVVC) لا تُرخَّص وصلًا إلّا والمُغلِقُ أوّلُ مثلين (حَاجَّ)، أو مدَّ الفرق (آلْآنَ) — `A116.Hadd.strictB` ومرآتُه `gate.licence.strict_licensed`؛ وما سواه رفضٌ مسمًّى `CVVC_NOT_GEMINATE` (قَالْتُ)، لا تقصيرَ تخمينًا. والاستثناءُ **داخلَ الكلمة الواحدة** وحدَها: في الوصل `A116.Hadd.strictJoinB` (مرآتُه `strict_joined`) يرفض مدًّا في كلمةٍ قبل مدغمٍ في الأخرى (يَا + الشَّافِعِينَ) باسم `CVVC_ACROSS_WORD_BOUNDARY`. و**وقفًا** (`exit = pause`) المدُّ العارض للسكون: قافيةُ مدٍّ يُغلقها ساكنُ الوقف في الطرف وحدَه تُرخَّص (الرَّحِيمْ، الْعَصْرْ) — `A116.Hadd.strictPauseB`/`strictJoinPauseB` ومرآتُهما `gate.licence.strict_pause_licensed`/`strict_joined_pause`؛ الوصلُ يستلزم الوقف (`strictB_pause`)، وكلُّ `v c` داخليٍّ مدغمٌ وقفًا أيضًا (`geminatePauseB_vc_carrier`)، ووقفُ المرخَّص وصلًا مرخَّصٌ وقفًا إذا صار آخرُه مُغلِقًا (`strictPauseB_pause`)؛ وما يرفضه الوقف `NOT_PAUSE_LICENSED`. والسكونُ في الخانة **موضعيّ**: «موضعٌ لا تتبعه حركةٌ قصيرة» لا «عدمُ الحركة نطقًا»؛ فحرفُ المدّ خانةٌ ساكنةٌ دورُها `v` (`Hadd.kindOf`)، و«الحركةُ الصفر» هي حالةُ `sukun` وظيفيًّا (ADR ٣).
- الحدّ: `Context(entry, exit)` — في الوصل تُرخَّص الكلمةُ مع ما قبلها (`JUNCTION_NOT_LICENSED` رفضٌ مسمًّى). و**التقاءُ الساكنين على الحدّ** (`A116.Iltiqa`، مرآتُه `gate.licence.repair_junction`): ثلاثةُ أوجهٍ لا رابعَ لها في آخر الكلمة اليساريّة وحدَها، بترتيبٍ لا يُبدَّل — الألفُ الفارقة تسقط (`FARQ_ALIF_DROPPED`)، حرفُ المدّ يُحذف (`MADD_DROPPED`: فِي الْأَرْضِ ← فِلْأَرْضِ)، الساكنُ يُكسَر (`SAKIN_KASRA`: لُوطٍ الْمُرْسَلُونَ — «أن يكون الساكن الأول مكسورا»، الكتاب) — وجهًا مسمًّى تحمله الشهادة (`Certificate.junction`) لا تخمينًا، وذرّاتُ الكلمة الثانية لا تُمسّ؛ مبرهَن: لا إصلاحَ بلا التقاء (`repair_noop_of_right_vowel`)، وبعد الإصلاح آخرُ الأولى متحرّك (`repaired_endsVowel`) والوصلُ ثابتٌ عليه (`repair_fixed`) ولا قافيةَ مدٍّ يقطعها الحدّ (`straddles_repaired_false`)؛ مطابَق بجدول `iltiqa` (360,000 زوجًا). والمدوّنةُ كلُّها تدخل **بسياقها** موقعًا موقعًا (`tools/gen_context_certificates.py`: الآيةُ سطرٌ، أوّلُها ابتداءٌ وآخرُها وقف، وما بينهما موصولٌ بما قبله على قاموسٍ مسمًّى `Gate(context, domain)` — مجالٌ من المدوّنة المختومة لا مخمَّن `DOMAIN_OUTSIDE_SEALED_CORPUS`)؛ مودَعُها في SLGE (`context-certificates.json.gz`) بمواقع `corpus-certificates` نفسِها.
- البقيّة: `gate.residue` — الرسمُ = صورةٌ قانونيّة + بقيّةُ قواعدِ طبعةٍ مسمّاة؛ الشهادةُ تحملها ويُردّ الرسمُ بعينه (`A116.Residue.chain_restore`). ما لا قاعدةَ له يُرفض باسمه، لا يُخمَّن.

كلُّ ما سوى ذلك **معلَّق** في `suspended/` بسجلٍّ (`SUSPENDED_REGISTRY.json`) يذكر سببَ كلّ وحدةٍ وشرطَ عودتها. التعليقُ نقلٌ لا حذف؛ التاريخُ في git.

## ما لا تفعله

1. لا تكتب `open`، `print`، `read_text`، `encode`، `decode`، `normalize`، `argv`، `stdin`… في أيّ ملفٍ خارج `gate/` (و`tests/`، `formal/`، `tools/gen_registry.py`، `tools/gen_glossary.py`، `tools/gen_claims.py`، `tools/gen_certificates.py`، `tools/gen_context_certificates.py`، `tools/gen_refusals.py`). الحارسُ `gate.guard.breaches()` يمشي على الشجرة كلَّها ويُسقط البناء.
2. لا تستورد من `suspended/` ولا من `canonical116` ولا من داخليّات البوّابة (`gate.contextual`، `gate.bridge`، `gate.mabni_*`…). الواجهةُ `gate` وحدَها (`enter`، `exit`، `derive`، `recover`، `licence`).
3. لا تُعِد وحدةً من `suspended/` إلّا بثلاثة معًا: (١) مدخلُها ومخرجُها عبر `gate.api`، (٢) اختباراتٌ توقعاتُها مستقلّةٌ عن شيفرتها ومطعَّمةٌ بالطفرة (منهج 20/20)، (٣) ADR مسجَّل. ثمّ `python tools/gen_registry.py` لتحديث السجلّ.
4. لا تحرِّر الجداول المولَّدة (`formal/a116/*.csv`) ولا `SUSPENDED_REGISTRY.json` ولا `gate/audit_results.json` ولا `GLOSSARY.md` ولا `REFUSALS.md` ولا `CLAIMS.md` بيدك؛ تُولَّد وتُطابَق (`git diff --exit-code`).
5. لا تمسّ `gate/bridge_v1_0.py` (مجمَّدٌ ببصمته) ولا `corpora/quran-simple-enhanced.txt` (مختومٌ بـ`CORPUS_SHA256`).
6. لا تدمج في `main` بلا إذن صاحب المستودع. فرعُ العمل: `claude/official-gate`.
7. لا تكتب «مبرهن» إلّا لما في Lean باسمه، ولا «مفحوص» إلّا لما له اختبارٌ باسمه، ولا «مقيس» إلّا لما له رقمٌ على مرجعٍ محجوب. وما سوى ذلك «معلن» أو «رأي». ولا تُثبت ادّعاءً في ملفٍّ قبل أن يوجد ما يثبته (لا CI قبل CI).
8. لا تحلّل بنصٍّ لم يمرّ بالبوّابة ولو كان الفحصُ عابرًا؛ وإن احتجت فحصًا خارجها فاكتبه في `tests/` أو مؤقّتًا خارج الشجرة.

## ما تفعله قبل أن تقول «تمّ»

```sh
export PATH=$HOME/.elan/bin:$PATH
(cd formal/a116 && lake build && lake env lean Audit.lean)   # صفرُ تحذير؛ المسلّماتُ propext/Classical.choice/Quot.sound فقط
(cd formal/a116 && lake exe a116-table syllables > syllables.csv)   # 13 MB، يُولَّد لا يُودَع؛ يلزم test_conformance
(cd formal/a116 && lake exe a116-table hadd > hadd.csv)             # 14 MB، يُولَّد لا يُودَع؛ يلزم test_hadd وgen_claims
(cd formal/a116 && lake exe a116-table hadd-join > hadd-join.csv)   # الحدُّ بين كلمتين؛ يُولَّد لا يُودَع؛ يلزم test_hadd وgen_claims
(cd formal/a116 && lake exe a116-table iltiqa > iltiqa.csv)         # التقاءُ الساكنين على الحدّ؛ يُولَّد لا يُودَع؛ يلزم test_iltiqa وgen_claims
(cd formal/a116 && lake exe a116-table licensable > licensable.csv) # المرخَّصُ من الشبكة (113 خانة، بلا ألفٍ متحرّكة)؛ يُودَع ويُطابَق (`git diff --exit-code`)؛ يلزم test_alif
ruff check gate tests tools && mypy
python tools/gen_registry.py --check
python tools/gen_glossary.py --check          # معجمُ الاصطلاح (GLOSSARY.md): كلُّ مصطلحٍ بموضع تعريفه، مرساةٌ لا توجد تُسقط البناء
python tools/gen_refusals.py --check          # سجلُّ الرفض (REFUSALS.md): كلُّ اسمِ رفضٍ تُطلقه البوّابة مرسًى في Lean/GLOSSARY أو معلَنٌ بصنفه وشرطه؛ اسمٌ بلا هذا ولا ذاك يُسقط البناء (REFUSAL_WITHOUT_ANCHOR)، وإعلانٌ بَطَل كذلك
python -m gate.audit corpora/quran-simple-enhanced.txt /tmp/audit_out && git diff --exit-code -- gate/audit_results.json   # الملفُّ ما تحسبه البوّابة الآن، لا كتلةَ فيه بيد
python tools/gen_certificates.py --check ../slge/tests/data/corpus-certificates.json.gz   # مودَعُ SLGE هو ما تطبعه هذه البوّابة الآن (DEPOSIT_DRIFTED_FROM_GATE)؛ CI الخاصّ بـSLGE يشغّله على الإيداع المثبَّت
python tools/gen_context_certificates.py --check ../slge/tests/data/context-certificates.json.gz   # مودَعُ SLGE الثاني: كلُّ موقعٍ في سياقه (ابتداء/وصل، استمرار/وقف) على قاموسٍ مسمًّى `Gate(context, domain)`؛ همزةُ الوصل ساقطةٌ في الوصل والوقفُ يُسكِّن ويُرخَّص بقيده، والرفضُ باسمه (~25 ثانية)
python tools/gen_claims.py --check            # سجلُّ الأرقام (CLAIMS.md): كلُّ رقمٍ منشور يُعاد حسابُه من مولِّده المسمّى ببصمة مودَعاته ومخرَجه؛ ولا عددَ في CLAUDE.md بلا مولِّد (~4 دقائق)
python -c "from gate.guard import breaches; print(breaches() or 'لا خرق')"
pytest -q -m "not slow"        # 148 اختبارًا؛ و`pytest -q -m slow` للقياس على MASAQ (≥ 97%)
```

وقبل الطبعة: أثبت أنّ الملف الذي تتكلّم عنه موجودٌ («لا ثقة بلا طبعة»)، وافصل في جوابك ما فحصته الآلة عمّا استنتجتَه أنت.

## الخريطة

| الموضع | ما هو | وسمُه |
|---|---|---|
| `formal/a116/A116/*.lean` | الـ116، الترخيص، العدّ، الليف، الترقيم، التقطيع الثلاثيّ، الاشتقاق، التمدّدات (`Recovery`) | مبرهن (نواة Lean، بلا Mathlib) |
| `formal/a116/*.csv` | جداولُ Lean المولَّدة: الترتيب، الأعداد، أزواج كانتور، 265,719 تقطيعًا | مولَّد |
| `gate/api.py` | الواجهة الوحيدة | مفحوص (`tests/test_gate.py`) |
| `gate/bridge.py`, `gate/contextual.py` | النصّ ← الذرّات، الترقيم، الشهادة (بروتوكول A116-CANONICAL-TXT-1.1) | مطابَق للجداول (`tests/test_conformance.py`) |
| `gate/licence.py` | التقطيع الثلاثيّ بايثونًا؛ الحكمُ الأخير قبل الشهادة | مطابَق لـ265,719 سطرًا من Lean |
| `formal/a116/A116/Hadd.lean` + `gate/licence.py` (`strict_licensed`) | قيدُ الحدّ: قافيةُ المدّ مدغمةٌ أو مدُّ فرق؛ إسقاطُ الخانة على `cv \| v \| c` تعريفٌ في Lean (`kindOf`) | مبرهن؛ مطابَق لـ346,200 سطرًا ولـ293,904 زوجًا موصولًا (`strictJoinB`) وصلًا ووقفًا (`strictPauseB`، `strictJoinPauseB` في العمود الأخير) (`test_hadd.py`، بسبع طفراتٍ مرفوضة) |
| `formal/a116/A116/Iltiqa.lean` + `gate/licence.py` (`repair_junction`) | التقاءُ الساكنين على الحدّ: الألفُ الفارقة تسقط / المدُّ يُحذف / الساكنُ يُكسَر، في آخر الأولى وحدَها، وجهًا مسمًّى في الشهادة | مبرهن (لا تصرّفَ بلا التقاء، الآخرُ متحرّكٌ بعده، ثابتٌ عليه، لا قافيةَ تقطع الحدّ)؛ مطابَق لـ360,000 زوجٍ (`test_iltiqa.py`، بثلاث طفراتٍ مرفوضة) |
| `formal/a116/A116/Hadd.lean` (`ilhaqPair`، `idghamPair`) + `gate/mabni_verbs.py` (`ilhaq_forms`) | الإلحاقُ بالرباعيّ (الكتاب س19135–19138): لامُ الإلحاق مثلان أوّلُهما متحرّك فصنفُها `cv` لا `c` — ليست إدغامًا (س21122)؛ والإدغامُ أوّلُ مثليه `c`؛ قوالبُه فَعْلَلَ/فَوْعَلَ/فَيْعَلَ/فَعْوَلَ وتَفَعْلَلَ من الثلاثيّ الصحيح بـ`derive(root, ilhaq=True)`، خارج الفهرس المقيس | مبرهن (`ilhaq_not_geminate`، `idgham_closer`، `jalbaba_vs_aadda`)؛ مفحوص ردًّا (`test_ilhaq.py`: derive → الجسر READY → مرخَّص وصلًا ووقفًا، بطفراتٍ مرفوضة) — لا مقيس: لا مرجعَ محجوبًا فيه |
| `formal/a116/A116/Alif.lean` + `gate/licence.py` (`licensable_atom`) | الألفُ لا تكون أبدًا إلّا ساكنة (الكتاب س18101): من الشبكة ثلاثٌ لا تُرخَّص — (ا،فتح) (ا،ضم) (ا،كسر) — والمرخَّصُ 113 خانةً قسمةً تامّة؛ ما كُتب ألفًا بحركةِ نفسها رفضٌ مسمًّى `BARE_ALIF_OWN_MARK_NOT_LICENSED` | مبرهن (`licensable_length`، `cells_partition`، `licensable_no_vowelled_alif`)؛ مطابَق لجدول `licensable.csv` المودَع (`test_alif.py`، بطفرةٍ مرفوضة)؛ مقيس: كلُّ شهادةٍ جاهزة على المدوّنة ذرّاتُها من المرخَّص |
| `formal/a116/A116/Unicode.lean`, `Boundary.lean` | UTF-8 تقابلٌ ذاتيُّ الحدّ على مجال يونيكود؛ قانون الابتداء/الوصل/الوقف (لا ابتداء بساكن، الوقف يُسكِّن، الوصل بشرط الحدّ، همزة الوصل تسقط ولا تُقبل بعد ساكن) | مبرهن؛ مطابَق (`utf8.csv`، `test_boundary.py`) |
| `formal/a116/A116/Ilal.lean` + `gate/ilal.py` | الإعلال والإبدال: 12 قاعدةً تعديلاتٍ على الخانات؛ الردّ مبرهَن، الإغلاق مبرهَن (قلب/نقل/حذف/إبدال)، حذف عين الأجوف ملزَم (الأصل غير مرخَّص) | مبرهن + شواهد مفحوصة |
| `formal/a116/A116/Hamza.lean` + `gate/hamza.py` | الهمزة: حاملٌ كسائر الحوامل؛ كرسيُّها دالّة في السياق (384 سياقًا، جدول Lean)؛ القطع يبقى في الوصل، والأدوار الزائدة (استفهام/متكلّم/تعدية) تحفظ الترخيص | مبرهن؛ مقيس (97.6% من كراسي المصحف، الباقي بقيّة مسمّاة) |
| `gate/residue.py` | بقيّةُ الرسم: 9 قواعد طبعةٍ مسمّاة (`A116.Residue`؛ التاسعةُ `DAGGER_ALIF` لطبعة globalquran/hamil)؛ READY 8,532 → 18,179 من 18,200، ردٌّ بعينه | مبرهن (الردّ) + مقيس (التغطية) |
| `gate/mabni_verbs.py`, `gate/mabni_bridge.py` | 770 جذرًا ← 315,874 صورة؛ الاسترجاع | مقيس (MASAQ 97.23%) |
| `gate/guard.py` | الحارس | مفحوص (خرقٌ مزروعٌ يُلتقط) |
| `tools/gen_refusals.py` → `REFUSALS.md` | سجلُّ الرفض: 30 اسمًا تُطلقها البوّابة — 5 مرسًى في Lean، 25 معلَنًا بصنفه (واجهة/رسم/همزة/ترخيص/حدّ) وشرطِ سداده | مفحوص (`test_refusals.py`: اسمٌ مزروعٌ وإعلانان باطلان يُلتقطون) |
| `suspended/` | 984 وحدة معلَّقة | لا يُستورد |

**المستودعاتُ المشمولة بهذا القانون:** الغانم (هذا)، SLGE، hamil، Algebra، والدساتير الثلاثة. **Taaqol-GPT ليس منها.** البوّابةُ لها جميعًا هي بوّابةُ الغانم هذه؛ ما في غيرها من بوّاباتٍ يُعلَّق بالطريقة نفسها حتى يعود عبرها.
