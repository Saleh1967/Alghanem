"""`R_arabic`: تحقيقُ `Σ_A^ref` في الميدان العربيّ، بالتوازي مع تحقيق Python.

    Σ_M  →  Σ_A  →  { R_arabic(Σ_A) , R_python(Σ_A) }

**لا** `Arabic → Python` **ولا** `Python → Arabic`.

فالعربيّةُ تحقّقٌ لغويٌّ للجبر، وPython تحقّقٌ تنفيذيٌّ له؛ ولا يُشتَقّ أحدُهما
من الآخر. والعلاقةُ بينهما ليست تطابقَ مفردات، بل:

    Same Algebraic Law  +  Different Realization

**وهذا التحقيقُ بنيويٌّ لا دلاليّ، بالتصريح:** لا يربط `CarrierState` بمقطعٍ
ولا بحركةٍ ولا بوزن. ذلك الربطُ دعوى لغويّةٌ تلزمها شواهدُ وقياسٌ ومعيارُ
تكذيب، ولا تُستحَقّ بمجرّد أنّ الجبر يسمح بها. فما هنا: أنّ مكوّنات `Σ_A` لها
مقابلاتٌ **مُسمّاةٌ ومُفنَّدةٌ** في الميدان العربيّ، لا أنّها صادقةٌ فيه.

**وميدانان تغطيةٌ لا استقلالُ تمثيل:** كونُ `Σ_A` قابلًا للتحقيق في ميدانين
يُظهر أنّ القانون لا يلزم تسميةَ أحدهما؛ والاستقلالُ يلزمه مربّعٌ تبادليٌّ
مُبرَّأ، وهو دَينٌ مُسجَّلٌ في `metaalgebra.commutation` لا نتيجةٌ هنا.
"""

from __future__ import annotations

from typing import Final

from ..metaalgebra.clause import DeclarativeClause
from ..metaalgebra.layer import LAYER_COMPONENT_NAMES
from ..metaalgebra.realization import (
    REALIZED_TRANSITION_COMPONENT_NAMES,
    ComponentRealization,
    LayerRealization,
    Realization,
    RealizationDomainRef,
    ResidualDisposition,
    ResidualDispositionRealization,
    TransitionRealization,
)
from ..metaalgebra.specification import AbstractSystemSpecification
from ..metaalgebra.transition import TransitionOutcome

__all__ = [
    "ARABIC_DOMAIN",
    "ARABIC_REALIZATION_IS_STRUCTURAL_NOT_LINGUISTIC",
    "NO_CARRIER_STATE_TO_SYLLABLE_BINDING_YET",
    "arabic_realization",
]

ARABIC_REALIZATION_IS_STRUCTURAL_NOT_LINGUISTIC: Final = (
    "التحقيقُ العربيُّ اليومَ ربطُ مكوّناتٍ مُسمّاةٍ بمواضعِ الميدان، "
    "لا دعوى صدقٍ لغويّ؛ وكلُّ شرطٍ فيه تقريريٌّ بتصريحه"
)

NO_CARRIER_STATE_TO_SYLLABLE_BINDING_YET: Final = (
    "لا يُربَط `CarrierState` بمقطعٍ ولا بحركةٍ ولا بوزنٍ في هذا المعلَم؛ "
    "فذلك دعوى لغويّةٌ تلزمها شواهدُ وقياسٌ ومعيارُ تكذيب، "
    "ولا تُستحَقّ بمجرّد أنّ الجبر يسمح بها"
)

ARABIC_DOMAIN: Final = RealizationDomainRef(
    domain_id="arabic",
    description=(
        "ميدانُ المادّة العربيّة المرخَّصة: حواملُ صوتيّةٌ وكتابيّة، "
        "وأحوالٌ عليها، وعمليّاتُ وصلٍ واشتقاقٍ وتركيب"
    ),
    what_is_not_this_domain=(
        "ما لا يقع في المادّة العربيّة المرخَّصة: نموذجُ التنفيذ البرمجيّ، "
        "وكلُّ لسانٍ آخر، وكلُّ ما لم يُرخَّص شاهدًا"
    ),
)

_LAYER_COMPONENT_BINDINGS: Final[dict[str, tuple[str, str, str]]] = {
    "carrier": (
        "حاملٌ صوتيٌّ/كتابيّ",
        "الحاملُ في الميدان العربيّ ما يبقى هو هو مع تبدّل ما يعتوره",
        "موضعٌ يتبدّل بتبدّل حالِه فلا يصحّ عدُّه حاملًا",
    ),
    "state_space": (
        "حالٌ على الحامل",
        "الحالُ ما يعتوِر الحاملَ ويتبدّل عليه بلا إبطالِ هُويّته",
        "ما لا يتبدّل أصلًا، فيكون من الحامل لا من الحال",
    ),
    "operations": (
        "عمليّاتٌ جزئيّة: وصلٌ وامتدادٌ واشتقاقٌ وتركيب",
        "العمليّةُ جزئيّةٌ: لها مواضعُ تمتنع فيها لا تُنتِج فيها بالتكلّف",
        "عمليّةٌ يُدّعى عمومُها فتُنتِج في كلّ موضعٍ بلا امتناع",
    ),
    "license_relations": (
        "علاقاتُ ترخيصٍ مُصرَّحٌ بشواهدها",
        "العلاقةُ ترخيصٌ سابقٌ على التشغيل تُفحَص شواهدُه",
        "علاقةٌ تُستنبَط من وقوع الاستعمال فتبرّر ما وقع",
    ),
    "invariants": (
        "ثوابتُ هُويّةٍ مُسمّاة",
        "الثابتُ سؤالٌ مُنتزَعٌ يُفحَص على الطرفين لا اسمٌ يُطمأنّ إليه",
        "ثباتُ الاسم يُتّخذ دليلًا على ثبات المُسمّى",
    ),
    "closure": (
        "إغلاقٌ بملاحظاتٍ مُصرَّحٍ بها",
        "المغلَقُ ما لا تميّزه الملاحظاتُ المُصرَّحُ بها عن نظيره",
        "إغلاقٌ يُدّعى بملاحظاتٍ تعجز عن التمييز بين موضعين مختلفين",
    ),
    "trace": (
        "سندٌ وأثرُ ترخيص",
        "الأثرُ يكفي لتفسير الترخيص ولا يحمل الجوابَ كاملًا",
        "أثرٌ يُستعاد منه الجوابُ فيغني عن الفحص",
    ),
    "residuals": (
        "بقايا مُسجَّلةٌ لا مُهمَلة",
        "البقيّةُ صفٌّ لكلّ واقعةٍ بما لم يُستوعَب",
        "بقيّةٌ تُطوى بالسكوت فلا يظهر نقصُ الاستيعاب",
    ),
}

_TRANSITION_COMPONENT_BINDINGS: Final[dict[str, tuple[str, str, str]]] = {
    "domain": (
        "شرطُ المحلِّ القابل",
        "المحلُّ القابلُ ما استوفى شرطَ الطبقة المصدر مغلَقًا",
        "محلٌّ يُدخَل عليه الانتقالُ قبل إغلاقه",
    ),
    "gate": (
        "بابُ الترخيص",
        "البابُ يمنع أو يؤجّل عند تخلّف الشرط، ولا يمضي بالتحذير",
        "بابٌ يُسجِّل التخلّفَ ثمّ يمضي",
    ),
    "transformation": (
        "تحويلٌ بين طبقتين مُسمّاتين",
        "التحويلُ ينقل من طبقةٍ إلى أخرى مغايرةٍ لها",
        "تحويلٌ يُعيد الطبقةَ نفسَها فلا يكون انتقالًا",
    ),
    "preservation": (
        "حفظُ ثابتٍ مُسمًّى",
        "الحفظُ مقايسةُ الثابت على المصدر والهدف في المُسمّى وحدَه",
        "مقايسةُ الصورتين ظاهرًا بدل مقايسة الثابت المُسمّى",
    ),
    "trace": (
        "شهادةُ انتقالٍ بوقائعِ تدقيقٍ تامّة",
        "الشهادةُ تحمل وقائعَ التدقيق المطلوبةَ كلَّها",
        "شهادةٌ تنقص واقعةً فلا يُستعاد منها سببُ الترخيص",
    ),
    "residual_policy": (
        "سياسةُ رتبةِ البقايا",
        "لا تنقص الرتبةُ بلا تصريحٍ بسبب النقص",
        "نقصانُ رتبةٍ يمرّ صامتًا",
    ),
    "handoff": (
        "شرطُ تسليمٍ زائدٌ على الإغلاق",
        "التسليمُ يزيد على الإغلاق تأهّلَ الخروج إلى الطبقة الأعلى",
        "شرطُ تسليمٍ يعيد نصَّ الإغلاق فيكون الإغلاقَ باسمٍ ثانٍ",
    ),
}

_RESIDUAL_DISPOSITION_BINDINGS: Final[dict[ResidualDisposition, str]] = {
    ResidualDisposition.CLOSE: "حين تُستوعَب البقيّةُ بشواهدِ الميدان بلا تعديلِ ربط",
    ResidualDisposition.REFINE: "حين تلزم البقيّةُ توسيعَ الربط اللغويّ لا نقضَه",
    ResidualDisposition.REVISE_DOMAIN: (
        "حين تدلّ البقيّةُ على أنّ ربطَ المكوّن بالمادّة العربيّة خاطئٌ فيُعاد"
    ),
    ResidualDisposition.DEFER: "حين لا تكفي الشواهدُ للحكم فتبقى البقيّةُ دَينًا",
}


def _component(
    component_name: str, binding: tuple[str, str, str]
) -> ComponentRealization:
    realized_as, condition_text, falsifier = binding
    return ComponentRealization(
        component_name=component_name,
        realized_as=realized_as,
        realization_condition=DeclarativeClause(
            clause_id=f"arabic.{component_name}",
            clause_text=condition_text,
            why_not_executable=(
                "الشرطُ وصفٌ لموضعِ المكوّن في الميدان لا تعبيرٌ صوريّ؛ "
                "ولا دلالةَ تنفيذيّةً تُولَّد من نثر"
            ),
        ),
        what_would_falsify_this_realization=falsifier,
    )


def _layer_realization(layer_id: str) -> LayerRealization:
    return LayerRealization(
        layer_id=layer_id,
        components=tuple(
            _component(name, _LAYER_COMPONENT_BINDINGS[name])
            for name in LAYER_COMPONENT_NAMES
        ),
        residual_dispositions=tuple(
            ResidualDispositionRealization(
                disposition=disposition,
                holds_when=_RESIDUAL_DISPOSITION_BINDINGS[disposition],
            )
            for disposition in ResidualDisposition
        ),
    )


def _transition_realization(transition_id: str) -> TransitionRealization:
    return TransitionRealization(
        transition_id=transition_id,
        components=tuple(
            _component(name, _TRANSITION_COMPONENT_BINDINGS[name])
            for name in REALIZED_TRANSITION_COMPONENT_NAMES
        ),
        unlicensed_outcome_realizations=(
            (TransitionOutcome.BLOCK, "منعٌ مُصرَّحٌ بسببه في الميدان"),
            (TransitionOutcome.DEFER, "توقّفٌ لعدم كفاية الشواهد"),
        ),
    )


def arabic_realization(specification: AbstractSystemSpecification) -> Realization:
    """تحقيقُ مواصفةٍ في الميدان العربيّ: ربطٌ بنيويٌّ تامُّ التغطية.

    والانتقالاتُ مُحقَّقةٌ بنيويًّا: مقابلاتٌ مُسمّاةٌ لمكوّناتها، لا دعوى أنّ
    انتقالًا عربيًّا بعينه صادقٌ تحت هذا الانتقال المجرّد.
    """

    return Realization(
        realization_id="R.arabic",
        domain=ARABIC_DOMAIN,
        specification=specification,
        layer_realizations=tuple(
            _layer_realization(layer_id) for layer_id in specification.layer_ids
        ),
        transition_realizations=tuple(
            _transition_realization(transition_id)
            for transition_id in specification.transition_ids
        ),
    )
