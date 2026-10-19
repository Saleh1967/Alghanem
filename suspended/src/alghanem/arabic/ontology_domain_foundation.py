"""أساسٌ واحدٌ يُؤسَّس عليه كلُّ مجالٍ أنطولوجيّ: `PK_0` ثمّ `O_0` ثمّ الرصيد.

لا تُنشئ هذه الوحدةُ أنواعًا ولا وقائع؛ تُقيم الأرضيّةَ التي **يُشترَط** على
كلّ بندٍ في الرصيد أن يقع داخلها: قاعدةُ المعلومات السابقة بشروطها التسعة، ثمّ
مرشَّحو الأنواع العامّة. ومن أراد مجالًا ثانيًا — بابًا أو كتابًا — أخذ هذه
الأرضيّةَ نفسَها، فيظهر هل العملياتُ عامّةٌ أم مكتوبةٌ لكلمةٍ واحدة.

**ومرشَّحُ نوعٍ ليس نوعًا مُودَعًا** (`A_FOUNDED_KIND_IS_NOT_A_DOMAIN_TYPE`):
`O_0` يقول إنّ «الحدث» جنسٌ لا يُستغنى عنه، ولا يقول إنّ «فتحَ البابِ» نوعُ
حدثٍ موجود؛ الثاني يُودَع في الرصيد بمصدره ومنزلة اعتماده.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from typing import Final

from ..ontology import GeneralOntology, OntologicalCandidate, OntologicalKind
from ..prior import PriorCondition, PriorConditionKind, PriorInformationBase
from ..prior.conditions import PriorLicenseGenus

__all__ = [
    "A_FOUNDED_KIND_IS_NOT_A_DOMAIN_TYPE",
    "THE_FOUNDED_KINDS",
    "domain_ontology",
    "domain_prior_base",
]

A_FOUNDED_KIND_IS_NOT_A_DOMAIN_TYPE: Final[str] = (
    "تأسيسُ جنسٍ ليس إيداعَ نوع: `O_0` يُرخِّص أن يكون في المجال أحداثٌ "
    "وحالاتٌ وأدوار، ولا يقول إنّ في العالَم بابًا ولا فتحًا؛ وإيداعُ النوع "
    "وتعريفِه وشروطِه يقع في الرصيد بمصدره"
)

THE_FOUNDED_KINDS: Final[tuple[OntologicalKind, ...]] = (
    OntologicalKind.THING,
    OntologicalKind.IDENTITY,
    OntologicalKind.ATTRIBUTE,
    OntologicalKind.STATE,
    OntologicalKind.EVENT,
    OntologicalKind.RELATION,
    OntologicalKind.ROLE,
    OntologicalKind.REFERENCE,
    OntologicalKind.TRANSFORMATION,
    OntologicalKind.CONDITION,
    OntologicalKind.PREVENTER,
)
"""الأجناسُ المؤسَّسةُ في هذه الأرضيّة؛ وما خرج عنها لا يُودَع بندًا."""

_LICENSING: Final[dict[OntologicalKind, PriorConditionKind]] = {
    OntologicalKind.THING: PriorConditionKind.DOMAIN,
    OntologicalKind.IDENTITY: PriorConditionKind.IDENTITY_CRITERION,
    OntologicalKind.ATTRIBUTE: PriorConditionKind.ATTRIBUTE_POSSIBILITY,
    OntologicalKind.STATE: PriorConditionKind.ATTRIBUTE_POSSIBILITY,
    OntologicalKind.EVENT: PriorConditionKind.TRANSFORMATION_CONDITIONS,
    OntologicalKind.RELATION: PriorConditionKind.RELATION_POSSIBILITY,
    OntologicalKind.ROLE: PriorConditionKind.RELATION_POSSIBILITY,
    OntologicalKind.REFERENCE: PriorConditionKind.UNIT_CRITERION,
    OntologicalKind.TRANSFORMATION: PriorConditionKind.TRANSFORMATION_CONDITIONS,
    OntologicalKind.CONDITION: PriorConditionKind.CONDITIONS_AND_PREVENTERS,
    OntologicalKind.PREVENTER: PriorConditionKind.CONDITIONS_AND_PREVENTERS,
}
"""الشرطُ المُرخِّصُ لكلّ جنس؛ مُعلَنٌ بجدولٍ لا مُستنتَجٌ من اسم الجنس."""


def domain_prior_base(base_id: str, domain_note: str) -> PriorInformationBase:
    """أقِم قاعدةَ المعلومات السابقة بشروطها التسعة لمجالٍ مُسمًّى.

    المدخل: مُعرِّفٌ وبيانُ مجال.
    الشرط: الشروطُ التسعةُ حاضرةٌ مرّةً واحدةً كلُّ واحدٍ منها.
    المخرج: قاعدةٌ صالحةٌ لتأسيس `O_0` عليها.
    حدُّها: الشروطُ **مُصطلَحٌ عليها للمجال**، لا مُثبَتةٌ عن العالَم.
    """

    return PriorInformationBase(
        base_id=base_id,
        domain_note=domain_note,
        conditions=tuple(
            PriorCondition(
                condition_id=f"{base_id}-{kind.value}",
                kind=kind,
                statement=f"شرطُ {kind.value} في مجال: {domain_note}",
                what_it_forbids=f"ما يُخِلّ بشرط {kind.value} في هذا المجال",
                licensed_by=PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
            )
            for kind in PriorConditionKind
        ),
    )


def domain_ontology(ontology_id: str, base: PriorInformationBase) -> GeneralOntology:
    """أسِّس `O_0` على قاعدةٍ قائمة، بمرشَّحٍ لكلّ جنسٍ في `THE_FOUNDED_KINDS`.

    المدخل: مُعرِّفٌ وقاعدةٌ سابقة.
    الشرط: لكلّ مرشَّحٍ دعوى ضرورةٍ ودعوى عدمِ اختزالٍ وشرطٌ مُرخِّصٌ في القاعدة.
    المخرج: أنطولوجيا عامّةٌ تُقيَّد بها بنودُ الرصيد.
    حدُّها: الترخيصُ لجنسٍ لا يُثبِت فردًا ولا نوعًا ولا وقوعَ حدث.
    """

    candidates = tuple(
        OntologicalCandidate(
            candidate_id=f"{ontology_id}-{kind.value}",
            kind=kind,
            necessity_claim=f"لا يُستغنى عن جنس {kind.value} في وصف هذا المجال",
            irreducibility_claim=f"لا يُرَدّ {kind.value} إلى غيره من المرشَّحين",
            licensing_condition=_LICENSING[kind],
        )
        for kind in THE_FOUNDED_KINDS
    )
    return GeneralOntology.founded_on(ontology_id, base, candidates)
