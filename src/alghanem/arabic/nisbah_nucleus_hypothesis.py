"""G0.NSB-0: إيداعُ نصّ «نواة النسبة» مُجمَّدًا، وفاحصُ أمانةٍ يسبق كلَّ قراءة.

النصُّ المُودَع هنا **نقدٌ لمنزلة قانونٍ قائم لا نقضٌ له**: يقول إنّ
`Representation(x)=(Carrier,State)` يصف *كيف يوجد* الشيءُ في النظام، ولا يفسّر
وحدَه *لماذا هو لغويّ*؛ وإنّ الأعلى لغويًّا هو الطرفُ والمحمولُ والنسبة. وهذه
الوحدةُ **تُجمّد النصَّ وتقف**.

**والنقدُ ليس نسخًا** (`CritiqueIsNotRepeal`): `CARRIER_IS_NOT_STATE` في
`metaalgebra/layer.py` يبقى بنصّه وبصمته، وبصمةُ `META_ALGEBRA_SCHEMA` لا
تتغيّر بشيءٍ ممّا هنا. ومَن قرأ إيداعَ نصٍّ ناقدٍ إلغاءً لقانونٍ نافذٍ قرأ ما
لم يجرِ.

**وإعادةُ التفسير بعد رؤية النتيجة ليست نسخًا مُرخَّصًا**
(`ReinterpretationAfterAResultIsNotSupersession`): `G0.FLT-1.Q` قُرِئت منه
نتيجةٌ أولى (تسعُ فروعٍ استمرارًا وتسعٌ مرشَّحةً لفرعٍ مستقلّ، وخمسةُ أسطحٍ
`UNDERPOWERED`)، و`SupersessionIsNotEditing` يرخّص الاستبدالَ **ما لم تُقرأ
نتيجة**. فلا `SupersessionRecord` هنا البتّة؛ بل `CompetingStatementRecord`
يُسمّي النصَّ المُنافَس، ويُصرّح بأنّ بصمتَه ولفظَه باقيان، ويُسمّي ما يُبطِل
هذا النصَّ الجديدَ نفسَه.

**والأمانةُ تُشتَقّ ولا تُوعَد بها** (`VerbatimFidelityIsCheckedNotPromised`):
تُسمّى مواضعُ التدوين الحاسمة واحدًا واحدًا، ويُشتَقّ حضورُها من النصّ المُودَع
عند الاستيراد، وموضعٌ غائبٌ يُسقِط الوحدةَ ولا يمرّ تنسيقًا. وهذا بعينه ما لم
يكن موجودًا حين جُمِّد نصُّ `G0.FLT-0`.

**ولا قارئَ في هذا الإيداع** (`NoReadoutExistsForNSB0Yet`): لا مفردةَ أدوارٍ،
ولا سجلَّ نسبةٍ، ولا ضابطَ سلبيًّا، ولا حقلَ نتيجةٍ البتّة — وحارسٌ عند
الاستيراد يمنع تسلّلَ حقلٍ كهذا لاحقًا. ودفعةٌ تجمع النصَّ وقارئَه لا تستطيع أن
تشهد لترتيب نفسها، وهو بعينه ما أسقط `G0.FLT-0`.

**وإدخالُ «النسبة» صنفًا نحويًّا في `Σ_M` ممنوعٌ هنا**
(`ANucleusProposalIsNotASchemaAmendment`): `A_SCHEMA_IS_NOT_A_SPECIFICATION`
يمنع أن تُكتَب نظريّةٌ بعينها في لغة الجبر؛ فالدعوى تُسجَّل سؤالًا مفتوحًا ولا
تُنفَّذ.

**والدورُ النسبيُّ لا يُدفَن في التمثيل** (`RelationIsNotRepresentation`):
نظيرُ `CARRIER_IS_NOT_STATE` في الطبقة الأعلى؛ ويُفحَص منعُ دفنِه على أسماء
حقول كلّ صنفٍ هنا عند الاستيراد.

**وما أجّلته وحداتٌ قائمةٌ يبقى مؤجَّلًا** (`ArgumentRoleIsDeferredAtItsOwnStage`):
الفاعليةُ والمفعوليةُ والمسببيةُ مُسجَّلةٌ أصلًا مرحلةً في
`compound_layer_preregistration`، مؤجَّلةً لانتفاء نصٍّ مصدريّ؛ ورفعُها هنا
تخطٍّ لتأجيلٍ قائم.

**ولا مفردةَ إفادةٍ ثانية** (`IfadaVocabularyIsNotDuplicated`): `IfadaStanding`
قائمةٌ في `mantuq_mafhum_ifada`، وهذه الوحدةُ لا تستورد منها ولا تُنشئ لها
نظيرًا؛ فنسختان من مفردةٍ واحدةٍ تنحرفان بلا أن تُخفق إحداهما.

تسجيلٌ لا سلطة: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا تستورد هذه
الوحدةُ من `kernel/` حرفًا، ولا تقرؤها وحدةٌ فيه، ولا تدخل
`BirthExperimentSpecification`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .flt1_qiyas_law import FLT1_QIYAS_TEXT_DIGEST

__all__ = [
    "AN_UNCHECKED_FROZEN_TEXT_IS_WHAT_FAILED_BEFORE_NOTE",
    "A_NUCLEUS_PROPOSAL_IS_NOT_A_SCHEMA_AMENDMENT_NOTE",
    "ARGUMENT_ROLE_IS_DEFERRED_AT_ITS_OWN_STAGE_NOTE",
    "COMPETING_STATEMENT_RECORD",
    "CRITIQUE_IS_NOT_REPEAL_NOTE",
    "IFADA_VOCABULARY_IS_NOT_DUPLICATED_NOTE",
    "NISBAH_NUCLEUS_NAMED_RESIDUALS",
    "NISBAH_NUCLEUS_TEXT",
    "NISBAH_NUCLEUS_TEXT_DIGEST",
    "NO_READOUT_EXISTS_FOR_NSB0_YET_NOTE",
    "REINTERPRETATION_AFTER_A_RESULT_IS_NOT_SUPERSESSION_NOTE",
    "RELATION_IS_NOT_REPRESENTATION_NOTE",
    "REQUIRED_NOTATION_SITES",
    "VERBATIM_FIDELITY_IS_CHECKED_NOT_PROMISED_NOTE",
    "CompetingStatementRecord",
    "FidelityReport",
    "FidelitySiteReading",
    "FidelityStanding",
    "NisbahNucleusHypothesisError",
    "NotationSite",
    "derive_fidelity_report",
    "nisbah_nucleus_text_digest",
]


class NisbahNucleusHypothesisError(ValueError):
    """رفضٌ مُسمّى في وحدة نصّ G0.NSB-0؛ لا تصحيحَ صامتًا ولا تخطّي."""


NISBAH_NUCLEUS_TEXT: Final[
    str
] = r"""نعم. إذا جعلنا الأصل:

\[
\boxed{\text{اللغةُ نظامٌ لإنشاء النِّسَب بين الأجناس والصفات}}
\]

فإن فرضية:

\[
\forall X,\quad X=(Carrier,State)
\]

لا تصلح أن تكون النواة العليا للغة. تصلح كنواة تمثيل وتنفيذ، لكنها لا تفسر وحدها لماذا وُجدت اللغة ولا ما الذي تنتجه.

المشكلة أن Carrier/State يصف كيفية وجود الوحدة في النظام، بينما اللغة في الأصل تحتاج أن تفسر:

\[
\boxed{\text{من يُنسب إليه ماذا؟ وبأي نسبة؟}}
\]

وهذا يقتضي إعادة بناء «بنية البنية» حول المحمول عليه، والمحمول، والنسبة.

1. النقد الأول: الحامل والحالة لا ينتجان نسبة

لنفرض:

\[
زيد=(Carrier,State)
\]

و:

\[
قائم=(Carrier,State).
\]

هذا لا ينتج:

\[
زيد\ قائم.
\]

فالمفقود كيان ثالث:

\[
\boxed{Relation / Nisbah}
\]

أي:

\[
\operatorname{Isnad}(زيد,قائم).
\]

إذن الحد الأدنى اللغوي ليس:

\[
(C,S)
\]

بل أقرب إلى:

\[
\boxed{(Term,\ Predicate,\ Relation)}
\]

أو بلغتك:

\[
\boxed{(جنس/محل,\ صفة/محمول,\ نسبة)}
\]

فالحامل والحالة يقعان داخل كل طرف، ولا يغنيان عن النسبة.

2. النقد الثاني: «الجنس» إن أُخذ بالمعنى المنطقي الضيق لا يكفي

إذا قلنا إن الطرف الأول دائمًا «جنس»، فسنصطدم بـ:

زيد؛

هذا؛

أنا؛

خمسة رجال؛

قيام زيد؛

إن قام زيد؛

فوق البيت.

هذه ليست أجناسًا بالمعنى المنطقي الصارم.

لذلك ينبغي أن يكون الأصل الأعم:

\[
\boxed{TermAnchor}
\]

أي «ما يصح أن يكون طرفًا محفوظ الهوية في نسبة».

ثم يكون الجنس أحد أنواعه:

\[
Genus\subseteq TermAnchor.
\]

وكذلك:

\[
Individual,\ Reference,\ EventAnchor,\ QuantityAnchor
\subseteq TermAnchor.
\]

فتصبح عبارتك الدقيقة:

> اللغة للنِّسَب بين المتعينات أو الأجناس من جهة، والمحمولات أو الصفات من جهة أخرى.

3. النقد الثالث: ليست كل صفة أحادية

«أبيض» يمكن تمثيلها:

\[
White(x).
\]

لكن:

\[
أكبر\ من
\]

تحتاج:

\[
GreaterThan(x,y).
\]

و«أعطى»:

\[
Give(x,y,z).
\]

إذن الصفة في الجبر لا ينبغي أن تكون مجرد State، بل:

\[
\boxed{Predicate_n}
\]

أي محمول ذو رتبة:

\[
n=1,2,3,\ldots
\]

وهذا مهم جدًا للنحو؛ لأنه يجعل الفاعل والمفعول والمفعول الثاني ليست أسماءً محفوظة في قوائم، بل مواقع حجج داخل المحمول.

مثلًا:

\[
ضرب(زيد,عمراً)
\]

تُبنى جبريًا:

\[
P_{\text{ضرب}}(Agent=زيد,\ Patient=عمرو).
\]

هنا الفاعلية والمفعولية ليستا «حالتين» فقط، بل:

\[
\boxed{ArgumentRoles}
\]

داخل نسبة الحدث.

4. النواة الجديدة لبنية البنية

أقترح أن تصبح النواة العليا:

\[
\boxed{
\mathfrak L=
(T,P,O,N,\Gamma,R)
}
\]

حيث:

\[
T=\text{Terms / محال النسبة}
\]

\[
P=\text{Predicates / المحمولات والصفات والأحداث}
\]

\[
O=\text{Operators / الأدوات والعوامل}
\]

\[
N=\text{Licensed Nisab / النسب المرخصة}
\]

\[
\Gamma=\text{شروط الترخيص والأنواع والمقام}
\]

\[
R=\text{البقايا}.
\]

ثم تكون الوحدة اللغوية المكتملة:

\[
\boxed{
N_i=
P_i(t_1,\ldots,t_n\mid \Theta)
}
\]

حيث \(\Theta\) تحمل القيود مثل:

\[
الزمن,\ الكم,\ التعريف,\ المقام,\ الشرط,\ النفي,\ الجهة,\ldots
\]

وهنا تصبح اللغة فعلًا جبر نسب.

5. أين يذهب Carrier/State إذن؟

لا نحذفه.

بل ننزله درجة واحدة:

\[
\boxed{
Carrier/State
=
\text{قانون تحقق أي كيان داخل طبقة}
}
\]

أما:

\[
\boxed{
Term/Predicate/Relation
=
\text{القانون اللغوي الأعلى}
}
\]

فمثلًا «زيد»:

\[
Carrier=\text{داله}
\]

\[
State=\text{حالته الصرفية/النحوية الحالية}
\]

لكن وظيفته في النسبة:

\[
Role=Term.
\]

و«ضرب»:

\[
Carrier=\text{الصيغة الفعلية}
\]

\[
State=\text{ماضٍ معلوم مفرد...}
\]

أما دوره الأعلى:

\[
Role=Predicate/Event.
\]

و«في»:

\[
Carrier=\text{لفظ في}
\]

\[
State=\text{بناء ثابت}
\]

لكن دوره:

\[
Role=RelationalOperator.
\]

إذن:

\[
\boxed{
Representation(x)=(Carrier,State)
}
\]

ولا بد بالإضافة إلى ذلك من:

\[
\boxed{
LinguisticRole(x)
\in
\{Term,Predicate,Operator,\ldots\}.
}
\]

6. إعادة بناء الطبقات كلها

الطبقة	ماذا تبني حقيقةً؟

الصوت/الرسم	حوامل قابلة للتمييز والتركيب
المقطع	وحدات مغلقة تصلح لبناء الدال
الجذر	مادة تصورية/حدثية مرشحة، لا نسبة مكتملة
الوزن	مشغل يحدد نوع تفعيل المادة
الجامد	TermCandidate في الأصل
المصدر	Predicate/EventCore مجرد من الزمن
المشتق	Predicate مربوط بدور: فاعل/مفعول/صفة...
الفعل	محمول حدثي مؤطّر بالزمن والجهة وبنية الحجج
الاسم	طرف صالح للإحالة أو الحمل عليه
الحرف	Operator أو رابط أو قيد للنسبة
المعجم	مخزون Term / Predicate / Operator candidates
النحو	جبر ربط الحجج بالمحمولات وبناء النِّسَب
الإعراب	ترميز سطحي لأثر العلاقة المرخصة
التركيب	شبكة نسب مرخصة
الإفادة	إغلاق كافٍ لشبكة النسبة
الحكم	مرحلة أعلى من الإفادة، لا يساويها

وهذه إعادة بناء جوهرية: الصرف لا ينتج كلمات فقط؛ بل يهيئ أطراف النسبة ومحمولاتها ومشغلاتها. والنحو لا يرتب الكلمات؛ بل يربط هذه الأشياء في نسب.

7. الجامد والمصدر والمشتق يظهر معناهما الحقيقي الآن

هذا يعيد تثبيت فكرتك السابقة ولكن بصورة أقوى.

الجامد

ليس فقط:

\[
Carrier/State.
\]

بل غالبًا:

\[
\boxed{
Jāmid\to TermAnchor
}
\]

أي مرساة كيان/جنس/مفهوم يقبل أن يُحمل عليه.

المصدر

ليس «اسم حدث» فقط، بل:

\[
\boxed{
Masdar\to PredicateCore
}
\]

أي أصل الحدث قبل إسناده إلى:

فاعل؛

مفعول؛

زمن؛

عدد؛

شخص.

مثل:

\[
ضرب
\]

كحدث مجرد.

المشتق

هو الجسر العظيم بين الصرف والنسبة:

\[
\boxed{
Derivative
=
PredicateCore+ArgumentRole
}
\]

فـ:

\[
ضارب
\]

يعيد الحدث إلى:

\[
AgentRole.
\]

و:

\[
مضروب
\]

إلى:

\[
PatientRole.
\]

إذن المشتقات ليست مجرد «حالات» للمصدر، بل إسقاطات للمحمول على أحد أطراف نسبته.

وهذا تفسير جبري أقوى بكثير.

8. الفعل

هنا أيضًا Carrier/State وحدها ضعيفة.

الأدق:

\[
\boxed{
Verb=
PredicateCore
+
TemporalFrame
+
ArgumentStructure
+
AssertionReadiness
}
\]

أي أن:

\[
كتب
\]

يحمل قابلية:

\[
Write(Agent,Patient)
\]

مع:

\[
Time=Past.
\]

ولذلك لا تتم الإفادة بمجرد الفعل؛ يبقى أحد أطراف النسبة مطلوبًا أو مقدرًا.

وهذا يفسر لماذا قلت سابقًا إن الماضي المجرد مكتمل صرفيًا لكنه مفتوح تركيبيًا للفاعل.

9. الاسم والفعل والحرف

بدل أن نجعلها حالات من حامل واحد فقط، يمكن تفسيرها وظيفيًا:

\[
\boxed{
اسم\Rightarrow Term/Predicate\ Candidate
}
\]

لأن الاسم قد يكون:

\[
زيد
\]

طرفًا، أو:

\[
قائم
\]

محمولًا.

والفعل:

\[
\boxed{
فعل\Rightarrow EventPredicate
}
\]

والحرف:

\[
\boxed{
حرف\Rightarrow Operator/RelationModifier
}
\]

مثل:

\[
في,\ من,\ إلى,\ لم,\ إن,\ هل.
\]

وهذا أقرب إلى سبب وجود هذه الأقسام أصلًا.

10. المبني والمعرب

هما ليسا حاملين مستقلين في المستوى الأعلى.

إنهما خاصيتان في واجهة الدال مع النسبة:

\[
\boxed{
Mu'rab=
Carrier\ whose\ surface\ state\ may\ encode\ relational\ role
}
\]

بينما:

\[
\boxed{
Mabni=
Carrier\ whose\ surface\ form\ does\ not\ vary\ along\ that\ axis
}
\]

إذن الإعراب هو:

\[
Relation\to SurfaceEffect.
\]

لا:

\[
SurfaceEffect\to Relation
\]

بالضرورة.

وهذا مهم جدًا.

11. الفاعلية والمفعولية والسببية

هذه من أوضح المواضع التي يكسر فيها Carrier/State وحده المعنى.

الأدق:

\[
\boxed{
Agent,\ Patient,\ Cause,\ Result
=
Roles\ inside\ predicates/relations
}
\]

فليست «أشياء» أولًا.

مثلًا:

\[
سبب(النار,الدخان)
\]

نسبة بين طرفين.

والسببية نوع علاقة:

\[
R_{\text{causal}}(x,y).
\]

12. المطابقة والتضمن والالتزام

هذه بالتحديد ليست Carrier/State في أصلها.

بل:

\[
\boxed{
Relations(Signifier,Meaning)
}
\]

أي إذا كان:

\[
D=\text{دال}
\]

و:

\[
M=\text{مدلول}
\]

فالمطابقة مثلًا علاقة:

\[
R_{\text{mutabaqa}}(D,M).
\]

والتضمن:

\[
R_{\text{tadammun}}(D,M_{part}).
\]

والالتزام:

\[
R_{\text{iltizam}}(M,M').
\]

إذن هذه أكبر شاهد على أن النسبة أسبق من Carrier/State في المستوى الدلالي.

13. الدال والمدلول

نحتاج أيضًا إعادة صياغتهما.

الدال:

\[
\boxed{
Signifier=
Encoded\ Term/Predicate/Operator
}
\]

والمدلول:

\[
\boxed{
Meaning=
Conceptual\ Term/Predicate/Relation
}
\]

والوضع:

\[
\boxed{
Wad'=
LicensedCorrespondence(SignifierRole,MeaningRole)
}
\]

وبهذا تتحول «الدلالة» كلها إلى جبر علاقات بين بنيتين:

\[
\mathfrak D_{\text{signifier}}
\]

و:

\[
\mathfrak M_{\text{meaning}}.
\]

14. الكلي والجزئي

هما ليسا حاملين مستقلين أولًا.

بل وصفان لمدى طرف أو مفهوم:

\[
\boxed{
Kulli(x)\iff x\text{ صالح للحمل على كثيرين}
}
\]

والجزئي:

\[
\boxed{
Juz'i(x)\iff reference(x)\text{ متعين}
}
\]

أي أنهما أقرب إلى:

\[
Quantificational/Referential\ properties.
\]

ثم إذا دخل الكلي في قياس يصبح طرفًا في نسبة أعلى.

15. العدد والمعدود والعد

هذه تصبح واضحة جدًا بهذا الأصل.

المعدود:

\[
t\in T.
\]

العدد:

\[
q\in P
\]

باعتباره محمول كمية:

\[
Cardinality(t)=q.
\]

والعد عملية:

\[
\boxed{
Count:T\to QuantityState
}
\]

أو:

\[
Count(S)=n.
\]

إذن قولك:

> العد حالة/محمول

قريب، لكن الأدق أنه عملية تنتج محمولًا كميًا.

16. المتواطئ والمتباين والمشكك والمترادف والمنقول

هذه أيضًا ليست «حامل/حالة» أصلًا، وإنما أنماط علاقات.

المترادف:

\[
R_{\text{synonym}}(D_1,D_2\mid M)
\]

أي دالان بالنسبة إلى مدلول.

المتواطئ:

\[
R_{\text{univocal}}(Concept,Instances).
\]

المشكك:

\[
R_{\text{graded}}(Concept,Instances,Order).
\]

المتباين:

\[
R_{\text{disjoint}}(Concept_1,Concept_2).
\]

المنقول:

\[
R_{\text{transfer}}(Wad'_1,Wad'_2).
\]

لاحظ: الأصل في كل هذه الأبواب هو العلاقة.

وهذا يؤيد فرضيتك الجديدة أكثر من Carrier/State.

17. الحقيقة والمجاز

كذلك:

\[
\boxed{
TruthOfUsage
=
Relation(Usage,Wad',Context)
}
\]

فالحقيقة اللغوية:

\[
Usage\sim OriginalWad'.
\]

والعرفية:

\[
Usage\sim ConventionalWad'.
\]

والمجاز:

\[
Usage\not\sim PrimaryWad'
\]

مع:

\[
LicensedTransfer+Qarina.
\]

إذن المجاز لا ينبغي أن يصبح «حالة» فقط، بل نتيجة فحص علاقة الاستعمال بالوضع والمقام.

18. الجملة الاسمية والفعلية وشبه الجملة

هذه ليست أنواع حوامل في الأصل، بل هندسات مختلفة لبناء النسبة.

الجملة الاسمية:

\[
Term\to Predicate.
\]

الجملة الفعلية:

\[
EventPredicate\to Arguments.
\]

شبه الجملة:

\[
RelationalOperator\to Term
\]

ثم تتصل بنسبة أعلى.

أي أن:

\[
\boxed{
SentenceType=
RelationConstructionSchema.
}
\]

19. الإخبار والإنشاء

بعد بناء النسبة نحتاج طبقة «قوة النسبة»:

\[
\boxed{
Force(Nisbah)
}
\]

مثل:

\[
Assert(N)
\]

أو:

\[
Question(N)
\]

أو:

\[
Command(N)
\]

أو:

\[
Wish(N).
\]

إذن الخبر والإنشاء لا يغيران بالضرورة طرفي النسبة، بل يغيران جهة تشغيل النسبة.

20. الزمن والمقام

الزمن ليس طرفًا عاديًا في كل مرة.

بل parameter:

\[
N=P(x\mid Time=t).
\]

والمقام:

\[
N=P(x\mid Context=c).
\]

أي:

\[
\boxed{
ContextualParameters
}
\]

تقيّد النسبة وتغير تفسيرها.

21. الإفادة

هنا يظهر القانون الجديد بوضوح.

الإفادة ليست Carrier/State فقط.

إنها:

\[
\boxed{
Ifadah=
Closure\ of\ Licensed\ Nisbah.
}
\]

أي عندما نملك:

\[
Predicate
+
RequiredArguments
+
Relation
+
NecessaryConstraints
\]

نصل إلى:

\[
\boxed{
CompleteNisbah.
}
\]

وهذه هي الإفادة قبل الحكم.

إذن:

\[
\boxed{
لا إفادة بلا نسبة
}
\]

تصبح أقوى من:

\[
\text{كل إفادة Carrier/State}.
\]

22. المنطوق والمفهوم

المنطوق:

\[
\boxed{
N_{explicit}
}
\]

أي نسبة يدل عليها البناء مباشرة.

والمفهوم:

\[
\boxed{
N_{derived}
}
\]

تُشتق من الأولى عبر بوابة:

\[
N_{explicit}
\xrightarrow{Gateway}
N_{derived}.
\]

وهذا يحقق تمامًا قاعدتك:

\[
\boxed{
لا مفهوم بلا بوابة.
}
\]

إذن المنطوق والمفهوم نسبتان مختلفتا جهة الاستخراج، لا مجرد حاملين/حالتين.

البنية الكلية الجديدة

بعد هذا النقد أرى أن القانون الأعلى لا ينبغي أن يكون:

\[
Carrier\to State\to Carrier\to State.
\]

بل:

\[
\boxed{
Representation
\to
Term/Predicate/Operator
\to
LicensedRelation
\to
RelationClosure
\to
Ifadah
}
\]

وتحت Representation يعمل قانون:

\[
Carrier/State.
\]

فتصبح الصورة:

\[
\boxed{
\begin{aligned}
&Carrier/State\\
&\downarrow\\
&Role\ Extraction\\
&\downarrow\\
&Term\quad Predicate\quad Operator\\
&\downarrow\\
&Argument\ Binding\\
&\downarrow\\
&Licensed\ Nisbah\\
&\downarrow\\
&Restriction/Reference/Time/Context\\
&\downarrow\\
&Closure\\
&\downarrow\\
&Ifadah\\
&\downarrow\\
&Manṭūq/Mafhūm\\
&\downarrow\\
&Hukm
\end{aligned}}
\]

وهذه، في رأيي، أقرب كثيرًا إلى «بنية بنية اللغة».

وما يبقى من Carrier/State؟

يبقى قانونًا عامًا مهمًا جدًا، لكن منزلته تتغير.

بدل:

\[
\boxed{
UniversalCarrierStateLaw
}
\]

كقانون لغوي أعلى، يصبح:

\[
\boxed{
UniversalRepresentationLaw
}
\]

أي:

> كل كيان يدخل النظام يحتاج حاملًا يحفظ هويته وحالةً تحدد تحققه.

لكن كل كيان لغوي لا يكتمل بوصفه لغويًا إلا إذا عُرفت وظيفته في النسبة.

فتكون القاعدة الكاملة:

\[
\boxed{
LinguisticObject(x)
=
Representation(x)
+
RelationalRole(x)
}
\]

حيث:

\[
Representation(x)=(Carrier,State)
\]

و:

\[
RelationalRole(x)\in
\{
Term,\ Predicate,\ Operator,\ Argument,\ Relation,\ Constraint
\}.
\]

وهذا هو التصحيح الأساسي.

وأرى أن النواة الجديدة التي ينبغي أن تدخل Σ_M لاحقًا ليست فقط:

\[
Layer,\ Transition,\ Realization
\]

بل تحت الاختبار تصبح:

\[
\boxed{
Term,\ Predicate,\ Operator,\ ArgumentRole,\ Nisbah,\ Constraint,\ Closure
}
\]

أما Carrier/State فيبقى الواجهة العامة لتحقيق هذه الأشياء.

في صياغة واحدة:

\[
\boxed{
\text{الحامل والحالة يفسران كيف يوجد الشيء؛
والجنس والصفة والنسبة تفسر لماذا هو لغوي.}
}
\]

وهذه نقطة الفصل التي أرى أنها تعيد بناء المشروع كله من أساس أصلب.
"""  # noqa: E501


@dataclass(frozen=True, slots=True)
class NotationSite:
    """موضعُ تدوينٍ حاسمٌ في النصّ الوارد، بما يقرّره وبما يسقط بسقوطه."""

    site_id: str
    literal: str
    what_it_decides: str
    what_its_absence_invalidates: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.site_id, "مُعرِّفُ الموضع"),
            (self.literal, "حرفيّةُ الموضع"),
            (self.what_it_decides, "ما يقرّره الموضع"),
            (self.what_its_absence_invalidates, "ما يُبطله غيابُه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise NisbahNucleusHypothesisError(
                    f"{label} نصٌّ غيرُ فارغ؛ وموضعٌ بلا حرفيّةٍ لا يُفحَص"
                )


REQUIRED_NOTATION_SITES: Final[tuple[NotationSite, ...]] = (
    NotationSite(
        site_id="the-minimal-linguistic-triple",
        literal=r"\boxed{(Term,\ Predicate,\ Relation)}",
        what_it_decides="أنّ الحدَّ الأدنى اللغويَّ ثلاثيٌّ لا ثنائيّ",
        what_its_absence_invalidates="دعوى النصّ كلَّها، فلا نواةَ بديلةً تُختبَر",
    ),
    NotationSite(
        site_id="the-missing-third-entity",
        literal=r"\operatorname{Isnad}(زيد,قائم)",
        what_it_decides="أنّ النسبةَ كيانٌ ثالثٌ لا يُنتجه طرفان",
        what_its_absence_invalidates="النقدَ الأوّل، فيبقى `(C,S)` كافيًا بالصمت",
    ),
    NotationSite(
        site_id="the-term-anchor",
        literal=r"\boxed{TermAnchor}",
        what_it_decides="أنّ الأصلَ الأعمَّ مرساةُ طرفٍ لا جنسٌ منطقيّ",
        what_its_absence_invalidates="النقدَ الثاني، فتُردّ الأطرافُ كلُّها أجناسًا",
    ),
    NotationSite(
        site_id="the-term-anchor-subkinds",
        literal=(
            r"Individual,\ Reference,\ EventAnchor,\ QuantityAnchor"
            "\n"
            r"\subseteq TermAnchor."
        ),
        what_it_decides="أنّ الجنسَ أحدُ أنواع المرساة لا الأصلَ فيها",
        what_its_absence_invalidates="حصرَ الأنواع، فتصير المرساةُ اسمًا بلا قسمة",
    ),
    NotationSite(
        site_id="the-predicate-arity",
        literal=r"\boxed{Predicate_n}",
        what_it_decides="أنّ للمحمول رتبةً، فليست كلُّ صفةٍ أحاديّة",
        what_its_absence_invalidates="النقدَ الثالث، وهو مِلاكُ بنية الحجج",
    ),
    NotationSite(
        site_id="the-argument-roles",
        literal=r"\boxed{ArgumentRoles}",
        what_it_decides="أنّ الفاعليةَ والمفعوليةَ مواقعُ حججٍ داخل المحمول",
        what_its_absence_invalidates="دعوى أنّ الأدوارَ ليست قوائمَ أسماءٍ محفوظة",
    ),
    NotationSite(
        site_id="the-proposed-nucleus",
        literal="\\mathfrak L=\n(T,P,O,N,\\Gamma,R)",
        what_it_decides="النواةَ العليا المُقترَحة بمواضعها الستّة",
        what_its_absence_invalidates="القسمَ الرابع، وهو موضعُ الاقتراح نفسِه",
    ),
    NotationSite(
        site_id="the-complete-unit",
        literal="N_i=\nP_i(t_1,\\ldots,t_n\\mid \\Theta)",
        what_it_decides="أنّ الوحدةَ اللغويةَ المكتملةَ محمولٌ بحججٍ وقيود",
        what_its_absence_invalidates="ربطَ النواة بالوحدة، فيبقى الاقتراحُ معلَّقًا",
    ),
    NotationSite(
        site_id="representation-stays",
        literal="Representation(x)=(Carrier,State)",
        what_it_decides="أنّ `Carrier/State` يبقى قانونًا ولا يُحذَف",
        what_its_absence_invalidates="`CritiqueIsNotRepeal`، فيُقرأ النقدُ نسخًا",
    ),
    NotationSite(
        site_id="the-relational-role",
        literal=(
            "LinguisticRole(x)\n"
            "\\in\n"
            "\\{Term,Predicate,Operator,\\ldots\\}."
        ),
        what_it_decides="أنّ الدورَ النسبيَّ مكوّنٌ زائدٌ على التمثيل",
        what_its_absence_invalidates="`RelationIsNotRepresentation` من أصله",
    ),
    NotationSite(
        site_id="the-derivative-bridge",
        literal="Derivative\n=\nPredicateCore+ArgumentRole",
        what_it_decides="أنّ المشتقَّ إسقاطُ محمولٍ على أحد أطراف نسبته",
        what_its_absence_invalidates="الجسرَ المُدَّعى بين الصرف والنسبة",
    ),
    NotationSite(
        site_id="irab-direction",
        literal="Relation\\to SurfaceEffect.",
        what_it_decides="اتّجاهَ الإعراب: من النسبة إلى الأثر السطحيّ لا عكسَه",
        what_its_absence_invalidates="دعوى اتّجاهٍ قابلةً للقياس على مدوّنة",
    ),
    NotationSite(
        site_id="ifada-as-closure",
        literal="Ifadah=\nClosure\\ of\\ Licensed\\ Nisbah.",
        what_it_decides="أنّ الإفادةَ إغلاقُ نسبةٍ مُرخَّصةٍ لا حالُ حاملٍ",
        what_its_absence_invalidates="وصلَ النصِّ بمفردة الإفادة القائمة",
    ),
    NotationSite(
        site_id="mantuq-mafhum-gateway",
        literal="N_{explicit}\n\\xrightarrow{Gateway}\nN_{derived}.",
        what_it_decides="أنّ المفهومَ نسبةٌ مُشتَقّةٌ عبر بوّابةٍ مُسمّاة",
        what_its_absence_invalidates="قاعدةَ «لا مفهومَ بلا بوّابة» في هذا النصّ",
    ),
    NotationSite(
        site_id="the-complete-rule",
        literal=(
            "LinguisticObject(x)\n"
            "=\n"
            "Representation(x)\n"
            "+\n"
            "RelationalRole(x)"
        ),
        what_it_decides="القاعدةَ الكاملة: تمثيلٌ ودورٌ معًا لا أحدُهما",
        what_its_absence_invalidates="خلاصةَ النصّ، وهي موضعُ التصحيح المُدَّعى",
    ),
    NotationSite(
        site_id="the-deferred-schema-proposal",
        literal=(
            r"Term,\ Predicate,\ Operator,\ ArgumentRole,\ Nisbah,"
            r"\ Constraint,\ Closure"
        ),
        what_it_decides="ما يقترح النصُّ إدخالَه `Σ_M` **تحت الاختبار** لاحقًا",
        what_its_absence_invalidates="موضعَ التأجيل، فيُقرأ الاقتراحُ تنفيذًا",
    ),
)


class FidelityStanding(Enum):
    """منزلةُ النصّ المُودَع؛ ثنائيّةٌ لأنّ الموضعَ إمّا حضر أو غاب."""

    EVERY_DECISIVE_SITE_IS_PRESENT = "كلُّ_موضعٍ_حاسمٍ_حاضرٌ_في_النصّ_المُودَع"
    A_DECISIVE_SITE_IS_ABSENT = "موضعٌ_حاسمٌ_غائبٌ_فالإيداعُ_باطلٌ_قبل_قراءته"


@dataclass(frozen=True, slots=True)
class FidelitySiteReading:
    """قراءةُ موضعٍ واحد: حاضرٌ في النصّ المُودَع أم غائب."""

    site_id: str
    is_present: bool
    what_it_decides: str
    what_its_absence_invalidates: str


@dataclass(frozen=True, slots=True)
class FidelityReport:
    """تقريرُ الأمانة كاملًا؛ يُعرَض قبل وجود أيّ قراءة."""

    standing: FidelityStanding
    sites: tuple[FidelitySiteReading, ...]
    absent_site_ids: tuple[str, ...]
    text_digest: str

    @property
    def is_fit_to_be_read(self) -> bool:
        """الإيداعُ صالحٌ لأن يُقرَأ متى حضرت المواضعُ الحاسمة كلُّها."""

        return self.standing is FidelityStanding.EVERY_DECISIVE_SITE_IS_PRESENT


@dataclass(frozen=True, slots=True)
class CompetingStatementRecord:
    """نصٌّ منافسٌ مُعلَن، لا ناسخٌ: المُنافَسُ يبقى بلفظه وبصمته.

    وهذا الصنفُ **ليس** `SupersessionRecord` ولا بديلًا عنه: ذاك يرخّص
    الاستبدالَ ما لم تُقرأ نتيجة، وقد قُرِئت؛ فالمشروعُ الوحيد أن يُعلَن النصُّ
    منافسًا ويبقى الأوّلُ قائمًا يُقاس عليه.
    """

    competed_text_digest: str
    competing_text_digest: str
    what_the_competed_text_keeps: str
    why_supersession_is_refused_here: str
    what_would_invalidate_this_statement: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.competed_text_digest, "بصمةُ النصّ المُنافَس"),
            (self.competing_text_digest, "بصمةُ النصّ المنافِس"),
            (self.what_the_competed_text_keeps, "ما يبقى للنصّ المُنافَس"),
            (self.why_supersession_is_refused_here, "سببُ رفض النسخ هنا"),
            (
                self.what_would_invalidate_this_statement,
                "ما يُبطِل هذا النصَّ نفسَه",
            ),
        ):
            if not isinstance(value, str) or not value.strip():
                raise NisbahNucleusHypothesisError(f"{label} نصٌّ غيرُ فارغ")
        if self.competed_text_digest == self.competing_text_digest:
            raise NisbahNucleusHypothesisError(
                "نصٌّ ينافس نفسَه ليس منافسًا؛ وبصمتاهما تفترقان"
            )


def nisbah_nucleus_text_digest(text: str | None = None) -> str:
    """اشتقّ بصمةَ النصّ من بايتاته المعياريّة؛ ولا تُكتَب بجانبه ثابتًا."""

    text = NISBAH_NUCLEUS_TEXT if text is None else text
    if not isinstance(text, str) or not text.strip():
        raise NisbahNucleusHypothesisError("النصُّ المُجمَّد نصٌّ غيرُ فارغ")
    return canonical_digest(canonical_bytes(text))


NISBAH_NUCLEUS_TEXT_DIGEST: Final[str] = nisbah_nucleus_text_digest()


def derive_fidelity_report(text: str | None = None) -> FidelityReport:
    """اشتقّ حضورَ كلّ موضعٍ حاسمٍ من النصّ المُودَع؛ ولا تُصرِّح بأمانةٍ منقولة."""

    text = NISBAH_NUCLEUS_TEXT if text is None else text
    readings: list[FidelitySiteReading] = []
    absent: list[str] = []
    for site in REQUIRED_NOTATION_SITES:
        present = site.literal in text
        if not present:
            absent.append(site.site_id)
        readings.append(
            FidelitySiteReading(
                site_id=site.site_id,
                is_present=present,
                what_it_decides=site.what_it_decides,
                what_its_absence_invalidates=site.what_its_absence_invalidates,
            )
        )
    standing = (
        FidelityStanding.EVERY_DECISIVE_SITE_IS_PRESENT
        if not absent
        else FidelityStanding.A_DECISIVE_SITE_IS_ABSENT
    )
    return FidelityReport(
        standing=standing,
        sites=tuple(readings),
        absent_site_ids=tuple(absent),
        text_digest=nisbah_nucleus_text_digest(text),
    )


COMPETING_STATEMENT_RECORD: Final[CompetingStatementRecord] = (
    CompetingStatementRecord(
        competed_text_digest=FLT1_QIYAS_TEXT_DIGEST,
        competing_text_digest=NISBAH_NUCLEUS_TEXT_DIGEST,
        what_the_competed_text_keeps=(
            "نصُّ `G0.FLT-1.Q` يبقى بلفظه وبصمته ومواضعِه الحاسمة، وقراءتُه "
            "الأولى تبقى مقروءةً كما خرجت؛ ولا حرفَ فيه يُعدَّل بهذا الإيداع"
        ),
        why_supersession_is_refused_here=(
            "`SupersessionIsNotEditing` يرخّص النسخَ ما لم تُقرأ نتيجةٌ من "
            "المنسوخ، وقد قُرِئت من `G0.FLT-1.Q` نتيجةٌ أولى مُسجَّلة؛ فإعادةُ "
            "الصياغة بعد الرؤية هي بعينها العلّةُ التي أسقطت `G0.FLT-0`. "
            "فالمشروعُ إعلانُ نصٍّ منافسٍ مستقلٍّ ببصمته، لا استبدالُ نصٍّ قُرِئ"
        ),
        what_would_invalidate_this_statement=(
            "يسقط هذا النصُّ إن أعاد نموذجٌ أضعفُ — الحاملُ وحدَه، أو "
            "(الحامل، الحالة) وحدَهما، أو الزوجُ غيرُ المرتَّب من طرفين بلا "
            "محمول — الهدفَ المُجمَّدَ نفسَه بكفاءةٍ مساوية؛ فالتعادلُ يُسقِط "
            "دعوى أنّ النسبةَ نواةٌ أعلى، ولا يُشترَط تفوُّقُ الأضعف. ويسقط "
            "كذلك إن كانت كلُّ بوّابةٍ تُثبِته صادقةً ببنية القارئ لا بالمدوّنة"
        ),
    )
)


CRITIQUE_IS_NOT_REPEAL_NOTE: Final[str] = (
    "CritiqueIsNotRepeal: نقدُ منزلةِ قانونٍ ليس نقضًا له؛ `CARRIER_IS_NOT_STATE` "
    "يبقى بنصّه في `Σ_M`، وبصمةُ `META_ALGEBRA_SCHEMA` لا تتغيّر بهذا الإيداع"
)

REINTERPRETATION_AFTER_A_RESULT_IS_NOT_SUPERSESSION_NOTE: Final[str] = (
    "ReinterpretationAfterAResultIsNotSupersession: النسخُ مُرخَّصٌ ما لم تُقرأ "
    "نتيجة، وقد قُرِئت من `G0.FLT-1.Q`؛ فلا `SupersessionRecord` هنا، بل إعلانُ "
    "منافسةٍ يبقى معه النصُّ الأوّلُ بلفظه وبصمته"
)

A_NUCLEUS_PROPOSAL_IS_NOT_A_SCHEMA_AMENDMENT_NOTE: Final[str] = (
    "ANucleusProposalIsNotASchemaAmendment: `A_SCHEMA_IS_NOT_A_SPECIFICATION` "
    "يمنع كتابةَ نظريّةٍ بعينها في لغة الجبر؛ فدعوى إدخال `Nisbah` صنفًا نحويًّا "
    "في `Σ_M` تُسجَّل سؤالًا مفتوحًا ولا تُنفَّذ في هذا الإيداع"
)

RELATION_IS_NOT_REPRESENTATION_NOTE: Final[str] = (
    "RelationIsNotRepresentation: الدورُ النسبيُّ مكوّنٌ مستقلٌّ لا حقلٌ يُدفَن "
    "داخل الحامل ولا داخل الحالة؛ ودفنُه يُلغي التمييزَ الذي عليه مدارُ النصّ، "
    "كما يُلغي دفنُ `S` في `C` تمييزَ الحامل والحالة"
)

ARGUMENT_ROLE_IS_DEFERRED_AT_ITS_OWN_STAGE_NOTE: Final[str] = (
    "ArgumentRoleIsDeferredAtItsOwnStage: الفاعليةُ والمفعوليةُ والمسببيةُ "
    "مرحلةٌ مُسجَّلةٌ في `compound_layer_preregistration` مؤجَّلةٌ لانتفاء نصٍّ "
    "مصدريّ؛ ورفعُها هنا عضوًا في مفردةٍ تخطٍّ لتأجيلٍ قائمٍ لا توسيعُ نطاق"
)

IFADA_VOCABULARY_IS_NOT_DUPLICATED_NOTE: Final[str] = (
    "IfadaVocabularyIsNotDuplicated: `IfadaStanding` قائمةٌ في "
    "`mantuq_mafhum_ifada`؛ ولا تُنشَأ لها هنا نظيرةٌ ثانية، فنسختان من مفردةٍ "
    "واحدةٍ تنحرفان بلا أن تُخفق إحداهما"
)

VERBATIM_FIDELITY_IS_CHECKED_NOT_PROMISED_NOTE: Final[str] = (
    "VerbatimFidelityIsCheckedNotPromised: مواضعُ التدوين الحاسمة مُعدَّدةٌ "
    "واحدًا واحدًا، وحضورُها مُشتَقٌّ من النصّ المُودَع عند الاستيراد؛ وموضعٌ "
    "غائبٌ يُسقِط الإيداعَ ولا يمرّ تنسيقًا"
)

NO_READOUT_EXISTS_FOR_NSB0_YET_NOTE: Final[str] = (
    "NoReadoutExistsForNSB0Yet: هذا الإيداعُ نصٌّ وإعلانُ منافسةٍ فقط؛ لا مفردةَ "
    "أدوارٍ، ولا سجلَّ نسبةٍ، ولا ضابطَ سلبيًّا، ولا حقلَ نتيجة. ودفعةٌ تجمع "
    "النصَّ وقارئَه لا تشهد لترتيب نفسها"
)

AN_UNCHECKED_FROZEN_TEXT_IS_WHAT_FAILED_BEFORE_NOTE: Final[str] = (
    "AnUncheckedFrozenTextIsWhatFailedBefore: سقط `G0.FLT-0` لأنّ نصَّه بُصِّم "
    "ولم يُقابَل بالوارد قبل تشغيله؛ فالمقابلةُ الآليّةُ القبليّة شرطُ دخولٍ "
    "لا حاشيةُ جودة"
)

NISBAH_NUCLEUS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    CRITIQUE_IS_NOT_REPEAL_NOTE,
    REINTERPRETATION_AFTER_A_RESULT_IS_NOT_SUPERSESSION_NOTE,
    A_NUCLEUS_PROPOSAL_IS_NOT_A_SCHEMA_AMENDMENT_NOTE,
    RELATION_IS_NOT_REPRESENTATION_NOTE,
    ARGUMENT_ROLE_IS_DEFERRED_AT_ITS_OWN_STAGE_NOTE,
    IFADA_VOCABULARY_IS_NOT_DUPLICATED_NOTE,
    VERBATIM_FIDELITY_IS_CHECKED_NOT_PROMISED_NOTE,
    NO_READOUT_EXISTS_FOR_NSB0_YET_NOTE,
    AN_UNCHECKED_FROZEN_TEXT_IS_WHAT_FAILED_BEFORE_NOTE,
)


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "outcome",
    "result",
    "verdict",
    "reading",
    "score",
    "rank",
    "birth",
    "freeze",
    "role",
)

_DECLARED_TYPES: Final[tuple[type, ...]] = (
    CompetingStatementRecord,
    FidelityReport,
    FidelitySiteReading,
    NotationSite,
)


def _refuse_a_duplicated_site() -> None:
    ids = tuple(site.site_id for site in REQUIRED_NOTATION_SITES)
    if len(ids) != len(set(ids)):
        raise NisbahNucleusHypothesisError(
            "موضعٌ مكرَّرٌ يُنقص العدَّ ويُقرأ تمامًا؛ والمكرَّرُ يُرفَض لا يُطوى"
        )


def _refuse_a_text_that_lost_a_decisive_site() -> None:
    report = derive_fidelity_report()
    if not report.is_fit_to_be_read:
        raise NisbahNucleusHypothesisError(
            "مواضعُ حاسمةٌ غائبةٌ من النصّ المُودَع: "
            f"{'، '.join(report.absent_site_ids)}؛ وموضعٌ غائبٌ يُسقِط الإيداعَ "
            "قبل قراءته ولا يمرّ تنسيقًا"
        )


def _refuse_a_result_or_role_field() -> None:
    for declaring_type in _DECLARED_TYPES:
        for field in fields(declaring_type):
            lowered = field.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise NisbahNucleusHypothesisError(
                        f"`{declaring_type.__name__}.{field.name}` يحمل "
                        f"«{token}»: هذا إيداعُ نصٍّ لا قارئ، ولا دورَ نسبيًّا "
                        "يُكتَب فيه ولا نتيجةَ تُسجَّل"
                    )


def _refuse_a_statement_that_competes_with_itself() -> None:
    if COMPETING_STATEMENT_RECORD.competing_text_digest != NISBAH_NUCLEUS_TEXT_DIGEST:
        raise NisbahNucleusHypothesisError(
            "بصمةُ النصّ المنافِس في السجلّ تفارق بصمةَ النصّ المُودَع هنا"
        )
    if COMPETING_STATEMENT_RECORD.competed_text_digest != FLT1_QIYAS_TEXT_DIGEST:
        raise NisbahNucleusHypothesisError(
            "بصمةُ النصّ المُنافَس في السجلّ تفارق بصمةَ نصّ `G0.FLT-1.Q`"
        )


_refuse_a_duplicated_site()
_refuse_a_text_that_lost_a_decisive_site()
_refuse_a_result_or_role_field()
_refuse_a_statement_that_competes_with_itself()
