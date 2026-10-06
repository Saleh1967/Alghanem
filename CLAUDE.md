# تعليماتٌ لكلّ وكيلٍ قبل الدخول — مستودع الغانم

اقرأ هذا كلَّه قبل أيّ أمر. ما خالفه يُرفض بالاسم، لا يُناقَش.

## القانون الواحد

**لا يدخل إلى هذه الشجرة إلّا بتٌّ ولا يخرج منها إلّا بتّ، ومدخلُه ومخرجُه الوحيدان: البرهانُ في `formal/a116` ومرآتُه `gate/`.**

- المدخل: `gate.enter(bytes) → Certificate | Refusal`. الشهادةُ ذرّاتٌ من الـ116 وعددٌ يطويها؛ والرفضُ مسمًّى (`DEFER`، `REJECT`، `OUTSIDE_DECLARED_DOMAIN`) ولا يُخمَّن شيء.
- المخرج: `gate.exit(cert) → bytes` — الكلمةُ بعينها (`Fiber.decode_encode`).
- الاشتقاق: `gate.derive(root)`، والاسترجاع: `gate.recover(cert)`؛ كلاهما يُقاس على مرجعٍ بشريٍّ محجوب (MASAQ) لا على شيفرته.
- الترخيص: `gate.licence` — الثلاثيّ (`cv | v | c`) لا الثنائيّ؛ فالثنائيُّ أعمى عن المدّ (`Ternary.binary_is_blind_to_madd`).
- الحدّ: `Context(entry, exit)` — في الوصل تُرخَّص الكلمةُ مع ما قبلها (`JUNCTION_NOT_LICENSED` رفضٌ مسمًّى)، لا تُحشر كسرةُ التقاء الساكنين تخمينًا.
- البقيّة: `gate.residue` — الرسمُ = صورةٌ قانونيّة + بقيّةُ قواعدِ طبعةٍ مسمّاة؛ الشهادةُ تحملها ويُردّ الرسمُ بعينه (`A116.Residue.chain_restore`). ما لا قاعدةَ له يُرفض باسمه، لا يُخمَّن.

كلُّ ما سوى ذلك **معلَّق** في `suspended/` بسجلٍّ (`SUSPENDED_REGISTRY.json`) يذكر سببَ كلّ وحدةٍ وشرطَ عودتها. التعليقُ نقلٌ لا حذف؛ التاريخُ في git.

## ما لا تفعله

1. لا تكتب `open`، `print`، `read_text`، `encode`، `decode`، `normalize`، `argv`، `stdin`… في أيّ ملفٍ خارج `gate/` (و`tests/`، `formal/`، `tools/gen_registry.py`). الحارسُ `gate.guard.breaches()` يمشي على الشجرة كلَّها ويُسقط البناء.
2. لا تستورد من `suspended/` ولا من `canonical116` ولا من داخليّات البوّابة (`gate.contextual`، `gate.bridge`، `gate.mabni_*`…). الواجهةُ `gate` وحدَها (`enter`، `exit`، `derive`، `recover`، `licence`).
3. لا تُعِد وحدةً من `suspended/` إلّا بثلاثة معًا: (١) مدخلُها ومخرجُها عبر `gate.api`، (٢) اختباراتٌ توقعاتُها مستقلّةٌ عن شيفرتها ومطعَّمةٌ بالطفرة (منهج 20/20)، (٣) ADR مسجَّل. ثمّ `python tools/gen_registry.py` لتحديث السجلّ.
4. لا تحرِّر الجداول المولَّدة (`formal/a116/*.csv`) ولا `SUSPENDED_REGISTRY.json` ولا `gate/audit_results.json` بيدك؛ تُولَّد وتُطابَق (`git diff --exit-code`).
5. لا تمسّ `gate/bridge_v1_0.py` (مجمَّدٌ ببصمته) ولا `corpora/quran-simple-enhanced.txt` (مختومٌ بـ`CORPUS_SHA256`).
6. لا تدمج في `main` بلا إذن صاحب المستودع. فرعُ العمل: `claude/official-gate`.
7. لا تكتب «مبرهن» إلّا لما في Lean باسمه، ولا «مفحوص» إلّا لما له اختبارٌ باسمه، ولا «مقيس» إلّا لما له رقمٌ على مرجعٍ محجوب. وما سوى ذلك «معلن» أو «رأي». ولا تُثبت ادّعاءً في ملفٍّ قبل أن يوجد ما يثبته (لا CI قبل CI).
8. لا تحلّل بنصٍّ لم يمرّ بالبوّابة ولو كان الفحصُ عابرًا؛ وإن احتجت فحصًا خارجها فاكتبه في `tests/` أو مؤقّتًا خارج الشجرة.

## ما تفعله قبل أن تقول «تمّ»

```sh
export PATH=$HOME/.elan/bin:$PATH
(cd formal/a116 && lake build && lake env lean Audit.lean)   # صفرُ تحذير؛ المسلّماتُ propext/Classical.choice/Quot.sound فقط
(cd formal/a116 && lake exe a116-table syllables > syllables.csv)   # 13 MB، يُولَّد لا يُودَع؛ يلزم test_conformance
ruff check gate tests tools && mypy
python tools/gen_registry.py --check
python -c "from gate.guard import breaches; print(breaches() or 'لا خرق')"
pytest -q -m "not slow"        # 69 اختبارًا؛ و`pytest -q -m slow` للقياس على MASAQ (≥ 97%)
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
| `formal/a116/A116/Unicode.lean`, `Boundary.lean` | UTF-8 تقابلٌ ذاتيُّ الحدّ على مجال يونيكود؛ قانون الابتداء/الوصل/الوقف (لا ابتداء بساكن، الوقف يُسكِّن، الوصل بشرط الحدّ، همزة الوصل تسقط ولا تُقبل بعد ساكن) | مبرهن؛ مطابَق (`utf8.csv`، `test_boundary.py`) |
| `gate/residue.py` | بقيّةُ الرسم: 8 قواعد طبعةٍ مسمّاة (`A116.Residue`)؛ READY 8,532 → 18,179 من 18,200، ردٌّ بعينه | مبرهن (الردّ) + مقيس (التغطية) |
| `gate/mabni_verbs.py`, `gate/mabni_bridge.py` | 770 جذرًا ← 315,874 صورة؛ الاسترجاع | مقيس (MASAQ 97.23%) |
| `gate/guard.py` | الحارس | مفحوص (خرقٌ مزروعٌ يُلتقط) |
| `suspended/` | 984 وحدة معلَّقة | لا يُستورد |

**المستودعاتُ المشمولة بهذا القانون:** الغانم (هذا)، SLGE، hamil، Algebra، والدساتير الثلاثة. **Taaqol-GPT ليس منها.** البوّابةُ لها جميعًا هي بوّابةُ الغانم هذه؛ ما في غيرها من بوّاباتٍ يُعلَّق بالطريقة نفسها حتى يعود عبرها.
