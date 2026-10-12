# ADR ٤٢ — الميزان: حكمُ الموصول آلةٌ منتهيةٌ جدولُها من البرهان (قرارُ المالك، 2026-10-12)

**السبب.** سدّ ADR ٣٨ دَينَ `GATE_JOINED_VS_STRICTJOINB_UNPROVEN` **بالمطابقة** على جدول `hadd-join`
(293,904 زوجًا)، لا بالبرهان. وطلبُ المالك: «رفعُ المطابقة إلى برهان يحتاج نموذجًا صوريًّا لبايثون، وهو
خارج هذه الشجرة. نبني.»

**الفكرة.** لا نُنمذج بايثون كلَّها. حكمُ الموصول في آلة Algebra (`Harf`، ADR ٣–٤ هناك) طيٌّ على
انتقالٍ **مجالُه منتهٍ**: 42 حالًا × 116 خانة. فالجدولُ الذي تطبعه النواةُ لهذا الانتقال ليس عيّنةً بل
**الدالّةُ كلُّها**. ويبقى خارج البرهان مفسِّرٌ بايثونيٌّ من أسطرٍ قليلة يطوي الجدول.

**القرار.**

1. **نقلُ الآلة إلى الشجرة.**
   * نُسخت `Harf.{Khana,Maqta,Satr,Thunai}` و`HarfBridge.{Takafu,Satr}` من Algebra إلى
     `formal/a116/A116/Harf/` و`A116/HarfBridge/`.
   * الاستيرادُ وحدَه أُعيدت كتابتُه (`A116.Harf.*`)، وتُبنى على A116 الحاليّة.
2. **`A116.Mizan`** (مبرهن، مدقَّق في `Audit.lean`):
   * `machineJoin pause L W`: الطيُّ بـ`Harf.wasl`/`waqf` من `bad'` على `L`، ثمّ `Harf.hadd`، ثمّ الطيُّ
     على `W`، ثمّ `qabilWasl`/`qabilWaqf`.
   * `machineJoin_eq`: ‎`machineJoin false L W = strictJoinB L W`‎ لكلّ كلمتين غيرِ فارغتين، **بلا حدٍّ
     على الطول**.
   * `machineJoin_pause_eq`: ‎`machineJoin true L W = strictJoinPauseB L W`‎ كذلك.
   * المجالُ منتهٍ ومعدودٌ بلا تكرار: `hal_nodup`، `khana_nodup`، `hal_count` (42)، `bad_first`، `cells_map`.
   * كلاهما من `HarfBridge.join_eq_strictJoinB`/`joinWaqf_eq_strictJoinPauseB` بعد `projW_toH`.
3. **الجدول `formal/a116/mizan.csv`**: `lake exe a116-table mizan`، 9,902 سطرًا.
   * 116 سطرَ `cell` (الذرّةُ ← رقمُ الخانة).
   * 42 سطرَ `state` (القبولُ وصلًا ووقفًا، وصورةُ الحدّ).
   * 2 × 42 × 116 سطرَ انتقال.
   * يُودَع ويُطابَق في CI (`git diff --exit-code`).
4. **المفسِّر `gate/mizan.py`**:
   * `run` يطوي الذرّات بالجدول.
   * `machine_join` يقرأ الجدول ويطويه كما في `machineJoin`.
   * `Gate.enter` بسياق `joined` يحكم به حين لا يفرغ الطرفان.
   * `joined_failure` باقٍ لتسمية الشرط الساقط وحدَها، فأسماءُ الرفض لم تتغيّر.
5. **الفحص** (`tests/test_mizan.py`):
   * الجدولُ دالّةٌ كلّيّة على مجالها.
   * المفسِّرُ على جدول `hadd-join` كلِّه هو عمودا `strictJoinB`/`strictJoinPauseB` من النواة.
   * ثلاثُ طفراتٍ في المفسِّر يلتقطها الجدول: `MUTANT_NO_HADD_STEP`، `MUTANT_WASL_FOR_PAUSE`،
     `MUTANT_WRONG_START`.
   * ويُفحص حكمُ الميزان على كلّ موقعٍ داخليٍّ جاهزٍ في مودَعَي المصحف والصحيحين
     (`test_context_deposit_shapes.py`، علامة `MIZAN`).

**الوسم.**

* **مبرهن**: الآلةُ هي `strictJoinB`/`strictJoinPauseB` لكلّ طول.
* **مولَّد ومطابَق**: الجدول هو انتقالُ الآلة.
* **مفحوص**: المفسِّر.

**ما بقي باسمه.**

* `MIZAN_INTERPRETER_UNPROVEN`: المفسِّرُ (`run`، `machine_join`، وقارئُ الجدول) بايثونُ غيرُ مبرهَنة. هو
  أسطرٌ معدودة، ومفحوصٌ على مجال `hadd-join` بطفراته، لكن لا برهانَ أنّه يطوي كما يطوي `List.foldl`.
* `MIZAN_TABLE_PRINTED_BY_COMPILED_LEAN`: الجدولُ تطبعه شيفرةُ Lean المترجَمة (`lake exe`)، لا النواة.
  فالثقةُ فيه ثقةٌ بالمترجِم ووقت التشغيل، لا بالنواة.
* فالدَّينُ `GATE_JOINED_VS_STRICTJOINB_UNPROVEN` صار **مبرهَنًا إلّا المفسِّرَ والطابع**، ولم يصر مبرهَنًا كلَّه.
