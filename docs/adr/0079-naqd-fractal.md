# ADR ٧٩ — نقدُ مرفق «برهان الاتّساق الفراكتاليّ» صوريًّا (طلبُ المالك «حلّل وبرهن»، 2026-10-16)

**الحال:** مقبول. **يبني على** ADR ٦٤ (`Sigha.Naqd`)، ٦٣ (`Tawafiq.not_3364`)، ٧١ (`Awamil`)، ٧٧ (`Fractal`)؛ لا يغيّر الواجهة `dal-v1`.

## السبب

أرفق المالك نصًّا (sha256 أوّل 16: `eb6508948ba05e18`) من وكيلٍ آخر: شفرةُ Lean 4 تدّعي «إثباتَ الاتّساق الكامل لنظامك الجبريّ الفركتليّ»، و«إثباتَ اتّصال النصّ التامّ وقيدِ الحدّ»، و«استقرارَ النظام وتشغيلَه الفركتليّ دون الحاجة لسجلّ الأرقام». وطلب: «حلّل وبرهن».

## ما طُبع في الجلسة (قبل أيّ كلام)

* المرفقُ **لا يُترجَم** بـ`lean` v4.34.1 (توليفةُ `formal/a116`): `Application type mismatch` في `proof_text_continuity` — `rcases ih2 with ⟨s2, e2⟩` يجعل `e2 : ∃ end_state, s2 = s2` (قضيّةً) ثمّ `exists s1, e2` يضعه حيث يُنتظر `PhoneticLink`؛ وتحذيرُ متغيّرٍ غيرِ مستعمل `op` في `proof_algebraic_closure`. فدعوى «الشفرة البرهانيّة الكاملة» كاذبةٌ بالترجمة.
* عبارتا مبرهنتيه: `∃ s e : PhoneticLink, s = s` و`∃ r : SyntacticClass, r = r`.

## القرار: `formal/a116/A116/NaqdFractal.lean`

أنواعُ المرفق بأعيانها (`Movement`، `PhoneticLink`، `LicensingGate`/`isLicensed`، `SyntacticClass`، `Phrase`)، ثمّ:

| المبرهنة | ما تقوله |
|---|---|
| `continuity_without_hypothesis` | عبارةُ المرفق الأولى بعينها تُبرهَن بلا الفرض `isLicensed g = true` وبلا استقراء؛ وLean يحذّر من إهمال الشاهد الثاني |
| `closure_without_hypothesis` | عبارتُه الثانية بعينها بلا «العامل» |
| `continuity_is_about_nothing` | العبارةُ صادقةٌ لأيّ نوعٍ مسكونٍ أيًّا كان: لا شيءَ فيها عن الخانات ولا العربيّة |
| `continuity_even_when_gate_closed` | النتيجةُ نفسُها حين البوّابةُ **مغلقة** — الفرضُ لا يُستعمل |
| `gate_ignores_cells` | `isLicensed` دالّةٌ في ثلاثة بتّات، أيُّ خاناتٍ تُلحق لا تغيّرها (نظيرُ `Sigha.Naqd.verify_ignores_structure`) |
| `open_gate_accepts_empty` | البوّابةُ المفتوحة تقبل بلا محتوًى |
| `real_gate_reads_cells` | المقابلُ القائم: `Hadd.strictB` يقبل كَتَبَ ويرفض كَاْاْ — حكمان على محتويين |
| `phonetic_link_is_blind_product` | فضاؤه 29 × 4 × 29 = 3,364 ليس عددَ طول (`Tawafiq.not_3364`) |
| `no_xor_in_awamil` | لا «Xor» في أصناف الأثر الثلاثةَ عشر، والعطفُ تابعٌ بلا أثر (`Awamil.tabi_no_effect`) |
| `fractal_says_something` | الفراكتالُ القائم ليس `x = x`: الصفرُ هويّةٌ في كلّ طبقة (`Fractal.zero_element_identity`) |

**الحكمُ على المرفق** (الدستور م١٤): بحثٌ منطقيٌّ بلا واقع — لا مودَعَ مختومًا، ولا مدخلَ ينقله، ولا جدولَ قبل القراءة؛ مبرهناتُه بعد إصلاحها صحيحةٌ رياضيًّا وفارغةٌ لغويًّا. لا يدخل منه شيءٌ إلى الشجرة: `ATTACHMENT_FRACTAL_REJECTED`. و«بلا سجلّ الأرقام» مردود: Lean يُبرهن المرويَّ المودَع (م١٧) والقياسُ شيءٌ آخر (م٦).

**ما يقابل دعاواه في الشجرة** (قائمٌ قبل هذا ADR): اتّصالُ النصّ وقيدُ الحدّ `FractalHadd.line_for_strict`/`text_append` (ADR ٧٨)، إصلاحُ الوصل `Iltiqa`، الفراكتالُ `Fractal.fractal_succ`/`fractal_append`/`sitta_kull_tabaqa` (ADR ٧٧)، العاملُ والمعمول `Amil`/`Awamil` (ADR ٧٠–٧١)، الإحالةُ والضمائر **لم تُكتب** (`PRONOUNS_NOT_WRITTEN`، ADR ٦٤).

## الطفرات (في الجلسة، خارج CI)

ثلاثٌ مرفوضة: (١) كَاْاْ مرخَّصة وصلًا؛ (٢) `Tawafiq.wasl 2 = 3364`؛ (٣) `Awamil.first .tabi = some .raf`.

## ما بقي باسمه

`ATTACHMENT_FRACTAL_REJECTED` (لا يدخل)، `PRONOUNS_NOT_WRITTEN` (الإحالة)، وكلُّ ديون ADR ٧٧–٧٨.
