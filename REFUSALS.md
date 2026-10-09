# سجلُّ الرفض — لا اسمَ رفضٍ بلا مرساةٍ أو إعلان

مولَّدٌ بـ`python tools/gen_refusals.py` بشجرة تركيب `gate/*.py`؛ لا يُحرَّر باليد. كلُّ اسمٍ تُطلقه البوّابةُ رفضًا إمّا **مرسًى** (مبرهنةٌ أو تعريفٌ في Lean باسمه، أو مدخلٌ في GLOSSARY؛ وما في ADR سردٌ لا مرساة) وإمّا **معلَنٌ** دَينًا بصنفه وشرطه في `DECLARED`؛ و`--check` يُسقط البناءَ على اسمٍ بلا هذا ولا ذاك (`REFUSAL_WITHOUT_ANCHOR`) وعلى إعلانٍ بَطَل (`STALE_DECLARED_REFUSAL`).

30 اسمًا: 5 مرسًى، 25 معلَنًا.

| الاسم | يُطلَق في | المرساة أو الإعلان |
|---|---|---|
| `ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL` | `bridge.py` | **معلَن** (همزة): ألفٌ بعد سابقةٍ محتملة قد تكون وصلًا — تحتاج الحدّ |
| `ANNOTATION_CONTRADICTS_AN_EXPLICIT_MARK` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (واجهة): الحاشيةُ لا تُبطل علامةً مكتوبة |
| `ATOM_OUTSIDE_A116` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (واجهة): ذرّةٌ ليست من الـ116 — `A116.cells_length` يحصر الشبكة |
| `A_MULTI_WORD_TEXT_NEEDS_A_BOUNDARY_INTERFACE` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (واجهة): عدّةُ كلماتٍ تدخل بحدودها لا دفعةً واحدة |
| `BARE_ALIF_OWN_MARK_NOT_LICENSED` | `contextual.py` | مرسًى: `formal/a116/A116/Alif.lean` |
| `CONFLICTING_MARKS` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (رسم): علامتان متعارضتان على حرفٍ واحد — لا تُرجَّح إحداهما |
| `CVVC_ACROSS_WORD_BOUNDARY` | `api.py` | مرسًى: `formal/a116/A116/Iltiqa.lean` |
| `CVVC_NOT_GEMINATE` | `api.py` | مرسًى: `formal/a116/A116/Hadd.lean` |
| `FINAL_HARAKA_IS_ABSENT` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (رسم): آخرُ الكلمة بلا حركة؛ الوقفُ يُعلَن بالحدّ لا يُخمَّن من الرسم |
| `HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (رسم): حرفٌ بلا حركةٍ في غير مواضع الإسقاط المسمّاة (`residue`) |
| `INITIAL_SUKUN_WITHOUT_REPAIR` | `contextual.py` | **معلَن** (حدّ): ساكنٌ في الابتداء بلا إصلاح — `A116.Boundary` «لا ابتداء بساكن»؛ الاسمُ نفسُه ليس في Lean بعدُ |
| `JUNCTION_NOT_LICENSED` | `api.py` | مرسًى: `formal/a116/A116/Iltiqa.lean` |
| `LEFT_CONTEXT_HAS_NO_CERTIFICATE` | `api.py` | **معلَن** (واجهة): الجارُ الأيسر لا شهادةَ له فلا وصلَ يُحكم |
| `NOT_CONTINUE_LICENSED_AFTER_REPAIR` | `api.py` | **معلَن** (ترخيص): الترخيصُ الثلاثيّ وصلًا هو `Ternary.continueB` بعينه؛ الاسمُ وحدَه لم يدخل Lean |
| `NOT_ONE_EXACT_WORD_SPAN` | `contextual.py` | **معلَن** (واجهة): النصُّ أكثرُ من كلمةٍ أو لا كلمةَ فيه — قيدُ الواجهة |
| `NOT_ONE_TOKEN` | `api.py` | **معلَن** (واجهة): المدخلُ كلمةٌ واحدة بلا فراغ — قيدُ الواجهة لا اللغة |
| `NOT_PAUSE_LICENSED` | `api.py` | مرسًى: `formal/a116/A116/Iltiqa.lean` |
| `NOT_UTF8` | `api.py` | **معلَن** (واجهة): بايتاتٌ ليست UTF-8؛ `A116.Unicode` يبرهن التقابلَ على المجال لا على ما خارجه |
| `NO_ARABIC_WORD_IN_SOURCE` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (واجهة): لا حرفَ عربيًّا في المدخل |
| `SHADDA_WITH_SUKUN` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (رسم): شدّةٌ مع سكون — تركيبٌ لا خانةَ له |
| `START_VOWEL_OF_WASL_IS_UNKNOWN` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (همزة): همزةُ وصلٍ بلا حركةٍ مكتوبة؛ قاعدةُ الثالث في SLGE (`Sawabiq.wasl_state_damm_iff`) لم تُرفَع إلى بوّابة الغانم |
| `TANWIN_ATTACHMENT_IS_AMBIGUOUS` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (همزة): موضعُ التنوين على الألف أو ما قبلها غيرُ محسوم |
| `TANWIN_WITH_ANOTHER_HARAKA` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (رسم): تنوينٌ مع حركةٍ أخرى |
| `TA_MARBUTA_IS_NOT_FINAL` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (رسم): تاءٌ مربوطة في غير الآخر |
| `THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (همزة): ألفٌ لا يُعرف أهي مدٌّ أم كرسيٌّ أم فارقة |
| `UNSUPPORTED_LETTER` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (واجهة): حرفٌ خارج الحوامل الـ29 المعلَنة في الجسر |
| `UNSUPPORTED_MARK` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (واجهة): علامةٌ خارج علامات البروتوكول |
| `UNVOCALIZED_WORD_IS_NEVER_GUESSED` | `api.py` | **معلَن** (رسم): كلمةٌ بلا أيّ علامة (الحروفُ المقطّعة) لا تُشكَّل تخمينًا |
| `VOWEL_WITH_SUKUN` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (رسم): حركةٌ مع سكونٍ على حرفٍ واحد |
| `WASL_IS_DECLARED_OUTSIDE_A_WORD_START` | `bridge.py`، `bridge_v1_0.py` | **معلَن** (همزة): وصلٌ معلَنٌ في غير أوّل الكلمة |
