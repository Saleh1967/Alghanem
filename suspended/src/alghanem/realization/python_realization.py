"""`R_python`: تحقيقُ `Σ_A^ref` في ميدان Python، بالتوازي مع التحقيق العربيّ.

    Σ_A  ⟶  R_python(Σ_A)        و        Σ_A  ⟶  R_arabic(Σ_A)

لا:

    Arabic ⟶ Python

فليست Python تعريفًا للنظريّة، ولا العربيّةُ تفرض بنيةَ البرنامج؛ كلاهما
تحقيقٌ لأصلٍ واحدٍ تحت القوانين نفسِها. وهذا هو محلُّ الدعوى:

    ∃ Σ : Realizes(R_arabic, Σ) ∧ Realizes(R_python, Σ)

**وهذا التحقيقُ اليومَ بنيويٌّ لا دلاليّ:** كلُّ شرطٍ فيه `DeclarativeClause`
حاملٌ سببَ عدمِ كونِه تنفيذيًّا، لا تعبيرٌ صوريّ. فهو يُظهر أنّ مكوّنات `Σ_A`
الثمانيةَ والسبعةَ لها مقابلاتٌ مُسمّاةٌ في الميدان، ولا يُظهر أنّها صادقةٌ فيه.

**وميدانان لا يُثبتان استقلالَ التمثيل:** غايتُهما أن يُظهرا أنّ القانون لا
يلزم تسميةَ أحدهما. والاستقلالُ دَينٌ في `commutation` لا نتيجةٌ هنا.
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
from .reference_specification import REFERENCE_SPECIFICATION

__all__ = [
    "PYTHON_DOMAIN",
    "PYTHON_REALIZATION_IS_STRUCTURAL_NOT_SEMANTIC",
    "python_realization",
]

PYTHON_REALIZATION_IS_STRUCTURAL_NOT_SEMANTIC: Final = (
    "تحقيقُ Python اليومَ ربطُ مكوّناتٍ مُسمّاةٍ لا إعطاءُ دلالةٍ تنفيذيّة؛ "
    "وكلُّ شرطٍ فيه تقريريٌّ يحمل سببَ عدمِ كونِه تنفيذيًّا"
)

PYTHON_DOMAIN: Final = RealizationDomainRef(
    domain_id="python",
    description=(
        "ميدانُ الكائنات المُنمَّطة وحالاتِ البرنامج والدوالِّ الجزئيّة "
        "والاستثناءاتِ وسجلّاتِ الأثر"
    ),
    what_is_not_this_domain=(
        "ما يقع خارجَ نموذجِ التنفيذ: النصُّ البشريُّ والعُرفُ اللغويُّ " "وكلُّ ما لا يُنفَّذ"
    ),
)

_LAYER_COMPONENT_BINDINGS: Final[dict[str, tuple[str, str, str]]] = {
    "carrier": (
        "Typed Object / AST Carrier",
        "الحاملُ في Python كائنٌ مُنمَّطٌ مجمَّدٌ تبقى هُويّتُه مع تغيّر الإسناد",
        "كائنٌ قابلٌ للتحوير تتغيّر هُويّتُه بتغيّر حقله",
    ),
    "state_space": (
        "Program State / Type State",
        "الحالُ إسنادٌ على الكائن يُقرأ ويُستبدَل بلا استبدال الكائن",
        "حالٌ لا يمكن تغييرُه إلّا بإنشاء حاملٍ جديد",
    ),
    "operations": (
        "partial functions",
        "العمليّةُ دالّةٌ جزئيّةٌ ترفع استثناءً معلومًا خارجَ مجالها",
        "دالّةٌ تُرجِع قيمةً افتراضيّةً خارجَ مجالها بدل أن ترفع",
    ),
    "license_relations": (
        "typing / licensing predicates",
        "الترخيصُ محمولٌ يُفحَص قبل التشغيل ويُرفَض عند تخلّفه",
        "محمولٌ يُحسَب بعد التشغيل فيبرّر ما وقع",
    ),
    "invariants": (
        "invariant assertions",
        "الثابتُ مقولةٌ تُفحَص على الطرفين لا على الطرف الواحد",
        "مقولةٌ تُفحَص على المخرَج وحدَه فلا تكشف تغيُّرَ المصدر",
    ),
    "closure": (
        "valid closed object",
        "المغلَقُ كائنٌ اجتاز كلَّ فحوصِ بنائه فلا يُعاد فحصُه",
        "كائنٌ يُبنى ناقصًا ثمّ يُكمَّل بعد الإنشاء",
    ),
    "trace": (
        "audit / provenance record",
        "الأثرُ سجلٌّ مجمَّدٌ يُستعاد منه سببُ الترخيص",
        "سجلٌّ يُعاد كتابتُه بعد الواقعة",
    ),
    "residuals": (
        "exceptions / residuals / deferred obligations",
        "البقيّةُ صفٌّ مُسجَّلٌ لما لم يُنقَل، لا استثناءٌ مبتلَع",
        "استثناءٌ يُلتقَط ويُهمَل بلا صفٍّ مُسجَّل",
    ),
}

_TRANSITION_COMPONENT_BINDINGS: Final[dict[str, tuple[str, str, str]]] = {
    "domain": (
        "domain guard",
        "شرطُ المجال فحصٌ سابقٌ على التحويل يرفض المُدخَل غيرَ المؤهَّل",
        "تحويلٌ يبدأ ثمّ يفشل في منتصفه",
    ),
    "gate": (
        "licensing gate",
        "البوّابةُ محمولُ ترخيصٍ يمنع أو يؤجّل عند تخلّفه",
        "بوّابةٌ تُسجِّل التحذيرَ وتمضي",
    ),
    "transformation": (
        "partial transformation function",
        "التحويلُ دالّةٌ جزئيّةٌ من نوعٍ إلى نوعٍ آخرَ معلومَين",
        "دالّةٌ تُعيد النوعَ نفسَه فلا تكون انتقالًا بين طبقتين",
    ),
    "preservation": (
        "invariant preservation check",
        "الحفظُ مقارنةُ ثابتٍ مُسمًّى على المصدر والهدف",
        "مقارنةُ تمثيلين بايتًا ببايت بدل مقارنةِ الثابت المُسمّى",
    ),
    "trace": (
        "transition audit certificate",
        "شهادةُ الانتقال سجلٌّ مجمَّدٌ بوقائعِ التدقيق المطلوبة",
        "شهادةٌ تنقص واقعةً من وقائع التدقيق",
    ),
    "residual_policy": (
        "residual rank policy",
        "سياسةُ البقايا تمنع نقصَ الرتبة بلا تصريحٍ بسببه",
        "سياسةٌ تسمح بإسقاطِ بقيّةٍ صامتًا",
    ),
    "handoff": (
        "hand-off precondition",
        "شرطُ التسليم فحصٌ يزيد على صحّةِ بناء الكائن",
        "شرطٌ يعيد نصَّ فحصِ البناء فيكون الإغلاقَ باسمٍ ثانٍ",
    ),
}

_RESIDUAL_DISPOSITION_BINDINGS: Final[dict[ResidualDisposition, str]] = {
    ResidualDisposition.CLOSE: "حين تُستوعَب البقيّةُ في الميدان بلا تعديلِ عقد",
    ResidualDisposition.REFINE: "حين تلزم البقيّةُ توسيعَ العقدِ المُنفَّذ لا نقضَه",
    ResidualDisposition.REVISE_DOMAIN: (
        "حين تدلّ البقيّةُ على أنّ ربطَ الميدان نفسِه خاطئٌ فيُعاد"
    ),
    ResidualDisposition.DEFER: "حين لا يكفي المُنفَّذُ للحكم فتبقى البقيّةُ دَينًا",
}


def _component(
    component_name: str, binding: tuple[str, str, str]
) -> ComponentRealization:
    realized_as, condition_text, falsifier = binding
    return ComponentRealization(
        component_name=component_name,
        realized_as=realized_as,
        realization_condition=DeclarativeClause(
            clause_id=f"python.{component_name}",
            clause_text=condition_text,
            why_not_executable=(
                "الشرطُ وصفٌ لعقدِ الميدان لا تعبيرٌ صوريّ؛ " "ولا دلالةَ تنفيذيّةً تُولَّد من نثر"
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
            (TransitionOutcome.BLOCK, "استثناءُ منعٍ مُسمًّى يوقف التحويل"),
            (TransitionOutcome.DEFER, "عقدُ `UnimplementedSemantics` المُعلَن"),
        ),
    )


def python_realization(
    specification: AbstractSystemSpecification = REFERENCE_SPECIFICATION,
) -> Realization:
    """تحقيقُ مواصفةٍ في ميدان Python: ربطٌ بنيويٌّ تامُّ التغطية."""

    return Realization(
        realization_id="R.python",
        domain=PYTHON_DOMAIN,
        specification=specification,
        layer_realizations=tuple(
            _layer_realization(layer_id) for layer_id in specification.layer_ids
        ),
        transition_realizations=tuple(
            _transition_realization(transition_id)
            for transition_id in specification.transition_ids
        ),
    )
