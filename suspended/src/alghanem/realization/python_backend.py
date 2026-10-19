"""`G_py`: خلفيّةُ توليدِ Python من `Σ_A` وحدها، بعرضٍ قانونيٍّ حتميّ.

    PythonCode = G_py^g(Σ_A)     لا     Σ_A ≈ ما كتبه المبرمج يدويًّا

**ولا دلالةَ من نثر:** شروطُ `Σ_A` اليومَ نصوصٌ بشريّةٌ لا تعابيرُ صوريّة، فلا
يخترع المولِّد لها معنًى تنفيذيًّا. يُولِّد لكلِّ شرطٍ نثريٍّ **عقدَ رفضٍ
صريحًا** يرفع `UnimplementedSemantics` حاملًا نصَّ الشرط؛ فالنقصُ يَظهر عند
النداء لا يُموَّه بقيمةٍ افتراضيّةٍ صادقة.

    prose  ⟼  raise UnimplementedSemantics(prose)
    ExecutableClause.expression  ⟼  Python expression

**والمُصرِّف `compile_expression` موجودٌ ومُختبَر**، وهو الطريقُ الوحيدُ إلى
دلالةٍ مولَّدة؛ لكنّ `Σ_A` لا تحمل بعدُ بندًا تنفيذيًّا، فكلُّ محمولٍ مولَّدٍ
اليومَ رفضٌ مُعلَن. وهذا وصفٌ للحال لا اعتذارٌ عنه.

**والحتميّةُ من التوليد:** ترتيبٌ ثابتٌ بأسماء المعرّفات، وقوالبُ ثابتة، وبلا
طوابعَ زمنيّةٍ ولا مساراتٍ مطلقة.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from ..metaalgebra.clause import (
    And,
    Clause,
    Constant,
    DeclarativeClause,
    Eq,
    ExecutableClause,
    Expression,
    FieldRef,
    MemberOf,
    Not,
    Or,
    PartialApply,
)
from ..metaalgebra.layer import LayerSignature
from ..metaalgebra.realization import ResidualDisposition
from ..metaalgebra.specification import AbstractSystemSpecification
from ..metaalgebra.transition import TransitionOutcome, TransitionSignature
from .artifact import GENERATED_FILE_BANNER, GeneratedArtifact, GeneratedArtifactSet
from .generator_identity import generator_digest
from .manifest import GeneratedArtifactManifest

__all__ = [
    "NO_SEMANTICS_FROM_PROSE_IN_GENERATION",
    "PYTHON_BACKEND_ID",
    "PYTHON_TARGET_LANGUAGE",
    "PythonBackend",
    "PythonBackendError",
    "compile_expression",
    "render_clause_contract",
    "python_identifier",
    "python_type_name",
]

PYTHON_BACKEND_ID: Final = "g_py"
PYTHON_TARGET_LANGUAGE: Final = "python"

NO_SEMANTICS_FROM_PROSE_IN_GENERATION: Final = (
    "لا يُولَّد محمولٌ تنفيذيٌّ من شرطٍ نثريّ؛ والنثرُ يُولِّد عقدَ رفضٍ " "صريحًا يَظهر عند النداء"
)


class PythonBackendError(ValueError):
    """خطأُ توليد: معرّفٌ لا يُحوَّل إلى اسمِ Python، أو تصادمُ أسماء."""


def python_identifier(value: str) -> str:
    """اسمُ Python صغيرُ الحروف من معرّفِ مواصفة، بتحويلٍ حتميّ."""

    if type(value) is not str or not value.strip():
        raise PythonBackendError("المعرّفُ المُحوَّل نصٌّ غيرُ فارغ")
    characters = [
        character if character.isalnum() and character.isascii() else "_"
        for character in value
    ]
    name = "".join(characters).strip("_").lower()
    while "__" in name:
        name = name.replace("__", "_")
    if not name:
        raise PythonBackendError(f"المعرّفُ «{value}» لا يُحوَّل إلى اسمِ Python")
    if name[0].isdigit():
        name = f"n_{name}"
    return name


def python_type_name(value: str, suffix: str) -> str:
    """اسمُ نوعٍ بصيغة PascalCase من معرّفِ مواصفةٍ ولاحقةٍ ثابتة."""

    parts = [part for part in python_identifier(value).split("_") if part]
    return "".join(part.capitalize() for part in parts) + suffix


def compile_expression(expression: Expression) -> str:
    """تعبيرُ Python من عقدةِ بندٍ تنفيذيّ؛ وهو الطريقُ الوحيدُ إلى دلالةٍ مولَّدة."""

    if isinstance(expression, Constant):
        return repr(expression.value)
    if isinstance(expression, FieldRef):
        return "subject" + "".join(f"[{part!r}]" for part in expression.path)
    if isinstance(expression, Eq):
        left = compile_expression(expression.left)
        right = compile_expression(expression.right)
        return f"({left} == {right})"
    if isinstance(expression, MemberOf):
        element = compile_expression(expression.element)
        members = ", ".join(compile_expression(member) for member in expression.members)
        return f"({element} in ({members},))"
    if isinstance(expression, Not):
        return f"(not {compile_expression(expression.operand)})"
    if isinstance(expression, And):
        operands = " and ".join(
            compile_expression(operand) for operand in expression.operands
        )
        return f"({operands})"
    if isinstance(expression, Or):
        operands = " or ".join(
            compile_expression(operand) for operand in expression.operands
        )
        return f"({operands})"
    if isinstance(expression, PartialApply):
        arguments = ", ".join(
            compile_expression(argument) for argument in expression.arguments
        )
        name = python_identifier(expression.operation_id)
        return f"operations[{name!r}]({arguments})"
    raise PythonBackendError("عقدةٌ غيرُ معروفةٍ لا تُصرَّف إلى Python")


def _text_literal(value: str) -> str:
    return repr(value)


def _prose_contract(name: str, prose: str, origin: str) -> list[str]:
    return [
        f"def {name}(subject: object) -> bool:",
        f'    """{origin}"""',
        "",
        f"    raise UnimplementedSemantics({_text_literal(prose)})",
        "",
        "",
    ]


def render_clause_contract(name: str, clause: Clause, origin: str) -> str:
    """مصدرُ محمولٍ من بندٍ: تصريفٌ للتنفيذيّ، ورفضٌ مُعلَنٌ للتقريريّ."""

    if isinstance(clause, ExecutableClause):
        body = f"    return bool({compile_expression(clause.expression)})"
        return "\n".join(
            [
                f"def {name}(subject: object) -> bool:",
                f'    """{origin}"""',
                "",
                body,
                "",
            ]
        )
    if isinstance(clause, DeclarativeClause):
        return "\n".join(_prose_contract(name, clause.clause_text, origin)[:-2] + [""])
    raise PythonBackendError(NO_SEMANTICS_FROM_PROSE_IN_GENERATION)


def _module_header(
    *,
    sigma_digest: str,
    schema_digest: str,
    backend_generator_digest: str,
) -> list[str]:
    return [
        GENERATED_FILE_BANNER,
        f"# backend_id: {PYTHON_BACKEND_ID}",
        f"# target_language: {PYTHON_TARGET_LANGUAGE}",
        f"# schema_digest: {schema_digest}",
        f"# sigma_digest: {sigma_digest}",
        f"# generator_digest: {backend_generator_digest}",
        '"""Executable trace generated from an abstract specification.',
        "",
        "This module is derived, not authored. Every prose condition of the",
        "specification is rendered as an explicit refusal rather than an invented",
        "semantics, so an unimplemented predicate fails loudly when called.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "from enum import Enum",
        "",
        "",
        "class UnimplementedSemantics(NotImplementedError):",
        '    """A prose condition carries no executable meaning."""',
        "",
        "",
        "class GeneratedOutcome(Enum):",
        '    """Outcomes declared by the specification language."""',
        "",
    ]


def _outcome_block() -> list[str]:
    lines: list[str] = []
    for outcome in sorted(TransitionOutcome, key=lambda member: member.value):
        lines.append(f'    {outcome.value} = "{outcome.value}"')
    lines.extend(
        [
            "",
            "",
            "class GeneratedResidualDisposition(Enum):",
            '    """Dispositions a residual may receive."""',
            "",
        ]
    )
    for disposition in sorted(ResidualDisposition, key=lambda member: member.value):
        lines.append(f'    {disposition.value} = "{disposition.value}"')
    lines.extend(["", ""])
    return lines


def _trace_block() -> list[str]:
    return [
        "@dataclass(frozen=True, slots=True)",
        "class GeneratedTrace:",
        '    """The minimal recoverable record of one attempted transition."""',
        "",
        "    transition_id: str",
        "    source_carrier_id: str",
        "    target_carrier_id: str",
        "    outcome: GeneratedOutcome",
        "    recovered_facts: tuple[str, ...]",
        "",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class GeneratedResidual:",
        '    """One residual row with its declared disposition."""',
        "",
        "    residual_id: str",
        "    disposition: GeneratedResidualDisposition",
        "    reason: str",
        "",
        "",
    ]


def _layer_block(layer: LayerSignature) -> list[str]:
    carrier_type = python_type_name(layer.layer_id, "Carrier")
    state_type = python_type_name(layer.layer_id, "State")
    prefix = python_identifier(layer.layer_id)
    lines: list[str] = [
        "@dataclass(frozen=True, slots=True)",
        f"class {carrier_type}:",
        f'    """Carrier of layer {layer.layer_id}: {layer.carrier.carrier_id}."""',
        "",
        "    carrier_id: str",
        "    borne: object",
        "",
        "",
        "@dataclass(frozen=True, slots=True)",
        f"class {state_type}:",
        f'    """State of layer {layer.layer_id}: '
        f'{layer.state_space.state_space_id}."""',
        "",
        f"    carrier: {carrier_type}",
        "    state_id: str",
        "    assignment: tuple[tuple[str, str], ...]",
        "",
        "",
    ]
    lines.extend(
        _prose_contract(
            f"{prefix}_is_member",
            layer.carrier.membership_condition,
            f"Membership condition of carrier {layer.carrier.carrier_id}.",
        )
    )
    lines.extend(
        _prose_contract(
            f"{prefix}_is_state",
            layer.state_space.state_condition,
            f"State condition of {layer.state_space.state_space_id}.",
        )
    )
    lines.extend(
        _prose_contract(
            f"{prefix}_is_closed",
            layer.closure.quotient_condition,
            f"Closure law {layer.closure.law_id}.",
        )
    )
    for operation in sorted(layer.operations, key=lambda item: item.operation_id):
        name = f"{prefix}_op_{python_identifier(operation.operation_id)}"
        result_literal = _text_literal(operation.result_condition)
        undefined = ", ".join(_text_literal(item) for item in operation.undefined_when)
        lines.extend(
            [
                f"def {name}(subject: object) -> object:",
                f'    """Partial operation {operation.operation_id}; '
                f'undefined in declared cases."""',
                "",
                f"    undefined_when = ({undefined},)",
                "    del undefined_when",
                f"    raise UnimplementedSemantics({result_literal})",
                "",
                "",
            ]
        )
    for relation in sorted(layer.license_relations, key=lambda item: item.relation_id):
        lines.extend(
            _prose_contract(
                f"{prefix}_licenses_{python_identifier(relation.relation_id)}",
                relation.holds_when,
                f"Licence relation {relation.relation_id}.",
            )
        )
    for invariant in sorted(layer.invariants, key=lambda item: item.component_name):
        lines.extend(
            _prose_contract(
                f"{prefix}_preserves_{python_identifier(invariant.component_name)}",
                invariant.extracted_question,
                f"Invariant component {invariant.component_name}.",
            )
        )
    return lines


def _transition_block(transition: TransitionSignature) -> list[str]:
    prefix = python_identifier(transition.transition_id)
    lines: list[str] = []
    lines.extend(
        _prose_contract(
            f"{prefix}_in_domain",
            transition.domain.holds_when,
            f"Domain condition {transition.domain.condition_id} of "
            f"{transition.transition_id}.",
        )
    )
    lines.extend(
        _prose_contract(
            f"{prefix}_is_licensed",
            transition.gate.licensed_when,
            f"Licence gate {transition.gate.gate_id}; unlicensed yields "
            + " or ".join(
                outcome.value for outcome in transition.gate.unlicensed_outcomes
            )
            + ".",
        )
    )
    lines.extend(
        _prose_contract(
            f"{prefix}_may_hand_off",
            transition.handoff.holds_when,
            f"Handoff condition {transition.handoff.condition_id}; failure yields "
            f"{transition.handoff.failure_outcome.value}.",
        )
    )
    steps = ", ".join(_text_literal(step) for step in transition.transformation.steps)
    preserved = ", ".join(
        _text_literal(name) for name in transition.preservation.preserved_components
    )
    facts = ", ".join(
        _text_literal(fact) for fact in transition.trace.certificate_facts
    )
    lines.extend(
        [
            f"def {prefix}_apply(subject: object) -> object:",
            f'    """Transformation {transition.transformation.transformation_id} '
            f'from {transition.source_layer_id} to {transition.target_layer_id}."""',
            "",
            f"    declared_steps = ({steps},)",
            f"    preserved_components = ({preserved},)",
            f"    certificate_facts = ({facts},)",
            "    del declared_steps, preserved_components, certificate_facts",
            f"    raise UnimplementedSemantics("
            f"{_text_literal(transition.transformation.undefined_when[0])})",
            "",
            "",
        ]
    )
    return lines


def _render_module(specification: AbstractSystemSpecification, digest: str) -> str:
    lines = _module_header(
        sigma_digest=specification.content_id,
        schema_digest=specification.schema_ref.content_id,
        backend_generator_digest=digest,
    )
    lines.extend(_outcome_block())
    lines.extend(_trace_block())
    for layer in sorted(specification.layers, key=lambda item: item.layer_id):
        lines.extend(_layer_block(layer))
    for transition in sorted(
        specification.transitions, key=lambda item: item.transition_id
    ):
        lines.extend(_transition_block(transition))
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


@dataclass(frozen=True, slots=True)
class PythonBackend:
    """`G_py`: مولِّدُ Python الحتميّ، هُويّتُه بصمةُ مصدره."""

    @property
    def backend_id(self) -> str:
        """اسمُ الخلفيّة."""

        return PYTHON_BACKEND_ID

    @property
    def target_language(self) -> str:
        """لغةُ الهدف."""

        return PYTHON_TARGET_LANGUAGE

    @property
    def generator_digest(self) -> str:
        """بصمةُ المولِّد من بايتات مصدره."""

        return generator_digest()

    def module_path(self, specification: AbstractSystemSpecification) -> str:
        """مسارُ الوحدةِ المولَّدة، مُشتَقٌّ من اسم المواصفة لا من بيئةِ التشغيل."""

        return f"{python_identifier(specification.spec_id)}.py"

    def generate(
        self, specification: AbstractSystemSpecification
    ) -> GeneratedArtifactSet:
        """آثارُ التوليد من المواصفة وحدها."""

        if not isinstance(specification, AbstractSystemSpecification):
            raise PythonBackendError("المولَّدُ منه مواصفةُ نظامٍ مجرّدة")
        text = _render_module(specification, self.generator_digest)
        return GeneratedArtifactSet(
            artifacts=(
                GeneratedArtifact(
                    relative_path=self.module_path(specification), text=text
                ),
            )
        )

    def manifest(
        self, specification: AbstractSystemSpecification
    ) -> GeneratedArtifactManifest:
        """بيانُ التوليد بالبصمتين واسم الخلفيّة."""

        return GeneratedArtifactManifest(
            backend_id=self.backend_id,
            target_language=self.target_language,
            schema_digest=specification.schema_ref.content_id,
            sigma_digest=specification.content_id,
            generator_digest=self.generator_digest,
            artifacts=self.generate(specification),
        )
