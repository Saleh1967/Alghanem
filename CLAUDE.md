# تعليماتٌ لكلّ وكيلٍ قبل الدخول — مستودع SLGE

اقرأ هذا كلَّه قبل أيّ أمر. ما خالفه يُرفض بالاسم.

## القانون الواحد

**لا يدخل هذه الشجرةَ نصٌّ، ولا يخرج منها نصّ. المدخلُ الوحيد شهادةُ بوّابة الغانم، والمخرجُ الوحيد ذرّاتُها بعينها.**

- النصُّ يدخل في مستودع الغانم وحدَه: `gate.enter(bytes) → Certificate | Refusal` (`Saleh1967/Alghanem`، فرع `claude/official-gate`، حزمة `gate/`، برهانُها `formal/a116`).
- هنا: `slge.entry.from_atoms(cert.atoms) → خانات`، و`slge.entry.to_atoms(خانات) → ذرّات` تعود إلى `gate.exit`. والطيُّ `to_integer/from_integer` مبرهَنٌ (`Slge.slgeFold_*`) على المرخَّص ثنائيًّا؛ وما رخّصه الثلاثيُّ وحدَه (كـ«حَاجَّ») يحمل عددَه في شهادته.
- الطبقاتُ الحيّة: `entry`، `cells`، `stream`، `categories`، `phonology`، `semantics`، `nazm`، `grant`، `wazn`، `shabaka`، `khamsa`، `afal`، `knowledge`، `rank`، `learning`، `answer` (و`order`، `status`، `guard` وصفًا). ما سواها **معلَّق** في `suspended/` بسجلٍّ (`SUSPENDED_REGISTRY.json`): `encoding`، `orthography`، `lexicon`، `morphology` — كانت تقرأ النصّ وتطبّعه خارج البوّابة.

## ما لا تفعله

1. لا تكتب `open`، `print`، `read_text`، `encode`، `decode`، `unicodedata.normalize`، `argv`… في `src/slge/` أو `tools/` (إلّا القائمة البيضاء في `slge.guard.EXEMPT_FILES`). الحارسُ `slge.guard.breaches()` يُسقط البناء.
2. لا تستورد `slge.encoding` ولا `slge.orthography` ولا `slge.lexicon` ولا `slge.morphology` ولا شيئًا من `suspended/`.
3. لا تستورد بوّابةَ الغانم هنا: الشهادةُ تصل بتّاتٍ (ذرّاتٍ وعددًا)؛ المستودعان منفصلان والبرهانُ مشترَكٌ بإيداعٍ مثبَّت (`formal/lake-manifest.json`).
4. لا تُعِد وحدةً من `suspended/` إلّا بثلاثة: (١) مدخلُها `slge.entry` على شهادةٍ لا نصّ، (٢) اختباراتٌ مستقلّةٌ عن شيفرتها مطعَّمةٌ بالطفرة (20/20)، (٣) ADR في `ARCHITECTURE.md`. ثمّ `python tools/gen_registry.py`.
5. لا تحرِّر `STATUS.md` ولا `LEAN_INDEX.md` ولا `SUSPENDED_REGISTRY.json` ولا `formal/out/*` بيدك؛ تُولَّد وتُطابَق.
6. لا تكتب في `status.py` وسمًا أقوى من سنده: «مبرهن» لما في Lean باسمه مدقَّقًا في `Audit.lean`؛ «مفحوص» لما له اختبارٌ باسمه؛ وما سندُه في `suspended/` يُوسَم «معلق» آليًّا (`status._suspend`). (الدعاوى المعروفةُ المبالغُ فيها سابقًا: Q22 دوريّ، Q3 بالبناء — لا تُعِدها.)
7. لا تدمج بلا إذن صاحب المستودع.

## قبل أن تقول «تمّ»

```sh
pip install -r requirements-dev.txt && pip install -e . --no-deps
ruff check . && mypy && pytest -q                     # 142 اختبارًا
python tools/gen_status.py --check
python tools/gen_registry.py --check
python tools/gen_lean_index.py --check               # فهرسُ المبرهنات على درجات الترخيص (LEAN_INDEX.md)
python -c "from slge.guard import breaches; print(breaches() or 'لا خرق')"
cd formal && lake build && lake env lean Audit.lean   # 67 مبرهنة؛ propext/Quot.sound فقط
```

وافصل في جوابك ما فحصته الآلة عمّا استنتجتَه، وأثبت وجودَ كلّ ملفٍّ تذكره قبل الكلام عنه.

**المستودعاتُ المشمولة بهذا القانون:** الغانم (البوّابة)، SLGE (هذا)، hamil، Algebra، والدساتير الثلاثة. **Taaqol-GPT ليس منها.**
