"""`G_py` دالّةٌ حتميّةٌ من `(Σ_A, g)`، ولا تُولِّد دلالةً من نثر."""

from __future__ import annotations

import pytest

from alghanem.metaalgebra.clause import (
    And,
    Constant,
    DeclarativeClause,
    Eq,
    ExecutableClause,
    FieldRef,
    MemberOf,
    Not,
    Or,
    PartialApply,
)
from alghanem.metaalgebra.specification import AbstractSystemSpecification, SchemaRef
from alghanem.realization.artifact import GENERATED_FILE_BANNER, GeneratedArtifactError
from alghanem.realization.manifest import GeneratedArtifactManifestError
from alghanem.realization.python_backend import (
    PYTHON_BACKEND_ID,
    PythonBackend,
    PythonBackendError,
    compile_expression,
    python_identifier,
    python_type_name,
    render_clause_contract,
)
from alghanem.realization.reference_specification import REFERENCE_SPECIFICATION


def _backend() -> PythonBackend:
    return PythonBackend()


def test_generation_is_a_function_of_the_specification_alone() -> None:
    first = _backend().generate(REFERENCE_SPECIFICATION)
    second = _backend().generate(REFERENCE_SPECIFICATION)
    assert first.content_id == second.content_id
    assert first.artifacts[0].text == second.artifacts[0].text


def test_a_manifest_carries_both_digests_and_the_backend_name() -> None:
    manifest = _backend().manifest(REFERENCE_SPECIFICATION)
    assert manifest.backend_id == PYTHON_BACKEND_ID
    assert manifest.sigma_digest == REFERENCE_SPECIFICATION.content_id
    assert manifest.generator_digest != manifest.sigma_digest
    assert manifest.determinism_key == (
        PYTHON_BACKEND_ID,
        manifest.sigma_digest,
        manifest.generator_digest,
    )
    assert manifest.describes(REFERENCE_SPECIFICATION)


def test_a_different_specification_yields_a_different_artifact() -> None:
    other = AbstractSystemSpecification(
        spec_id=f"{REFERENCE_SPECIFICATION.spec_id}.variant",
        schema_ref=SchemaRef.of(),
        layers=REFERENCE_SPECIFICATION.layers,
        transitions=REFERENCE_SPECIFICATION.transitions,
    )
    assert other.content_id != REFERENCE_SPECIFICATION.content_id
    first = _backend().generate(REFERENCE_SPECIFICATION)
    second = _backend().generate(other)
    assert first.content_id != second.content_id


def test_every_prose_condition_becomes_an_explicit_refusal() -> None:
    text = _backend().generate(REFERENCE_SPECIFICATION).artifacts[0].text
    assert "class UnimplementedSemantics(NotImplementedError):" in text
    assert text.count("raise UnimplementedSemantics(") >= len(
        REFERENCE_SPECIFICATION.layers
    )
    assert "return True" not in text


def test_the_generated_module_declares_its_origin_in_its_header() -> None:
    text = _backend().generate(REFERENCE_SPECIFICATION).artifacts[0].text
    assert text.startswith(GENERATED_FILE_BANNER)
    assert f"# sigma_digest: {REFERENCE_SPECIFICATION.content_id}" in text
    assert "# generator_digest: " in text


def test_the_generated_module_is_importable_python() -> None:
    text = _backend().generate(REFERENCE_SPECIFICATION).artifacts[0].text
    namespace: dict[str, object] = {}
    exec(compile(text, "<generated>", "exec"), namespace)
    assert "GeneratedTrace" in namespace
    assert "GeneratedResidualDisposition" in namespace


def test_a_generated_predicate_refuses_rather_than_answers() -> None:
    text = _backend().generate(REFERENCE_SPECIFICATION).artifacts[0].text
    namespace: dict[str, object] = {}
    exec(compile(text, "<generated>", "exec"), namespace)
    predicate = namespace["l0_is_member"]
    assert callable(predicate)
    with pytest.raises(NotImplementedError):
        predicate(object())


def test_an_executable_clause_is_the_only_road_to_generated_semantics() -> None:
    clause = ExecutableClause(
        clause_id="c.executable",
        clause_text="عضوٌ في قائمةٍ مُصرَّحٍ بها",
        expression=MemberOf(
            element=FieldRef(path=("kind",)),
            members=(Constant(value="a"), Constant(value="b")),
        ),
    )
    source = render_clause_contract("is_admissible", clause, "Executable clause.")
    namespace: dict[str, object] = {}
    exec(compile(source, "<clause>", "exec"), namespace)
    predicate = namespace["is_admissible"]
    assert callable(predicate)
    assert predicate({"kind": "a"}) is True
    assert predicate({"kind": "z"}) is False


def test_a_declarative_clause_yields_a_refusal_not_a_default_answer() -> None:
    clause = DeclarativeClause(
        clause_id="c.prose",
        clause_text="شرطٌ نثريٌّ بلا صورة",
        why_not_executable="لم تُعطَ له دلالةٌ صوريّةٌ بعدُ",
    )
    source = render_clause_contract("is_admissible", clause, "Prose clause.")
    namespace: dict[str, object] = {"UnimplementedSemantics": NotImplementedError}
    exec(compile(source, "<clause>", "exec"), namespace)
    predicate = namespace["is_admissible"]
    assert callable(predicate)
    with pytest.raises(NotImplementedError):
        predicate({"kind": "a"})


def test_every_executable_node_compiles() -> None:
    expression = And(
        operands=(
            Or(
                operands=(
                    Eq(left=FieldRef(path=("a",)), right=Constant(value=1)),
                    Not(
                        operand=Eq(left=FieldRef(path=("a",)), right=Constant(value=2))
                    ),
                )
            ),
            MemberOf(element=FieldRef(path=("b",)), members=(Constant(value=True),)),
        )
    )
    compiled = compile_expression(expression)
    assert "subject['a']" in compiled
    assert " and " in compiled and " or " in compiled


def test_a_partial_application_compiles_to_an_operation_lookup() -> None:
    compiled = compile_expression(
        PartialApply(operation_id="L0.op", arguments=(FieldRef(path=("x",)),))
    )
    assert compiled.startswith("operations['l0_op'](")


def test_an_unknown_node_is_refused_rather_than_guessed() -> None:
    with pytest.raises(PythonBackendError):
        compile_expression("not a node")  # type: ignore[arg-type]


def test_an_identifier_transformation_is_deterministic_and_refuses_the_empty() -> None:
    assert python_identifier("L0.op") == "l0_op"
    assert python_identifier("L0.op") == python_identifier("L0.op")
    assert python_type_name("L0", "Carrier") == "L0Carrier"
    with pytest.raises(PythonBackendError):
        python_identifier("...")


def test_a_manifest_refuses_a_non_specification_comparison() -> None:
    manifest = _backend().manifest(REFERENCE_SPECIFICATION)
    with pytest.raises(GeneratedArtifactManifestError):
        manifest.describes("not a specification")  # type: ignore[arg-type]


def test_an_artifact_refuses_an_absolute_path() -> None:
    from alghanem.realization.artifact import GeneratedArtifact

    with pytest.raises(GeneratedArtifactError):
        GeneratedArtifact(relative_path="/tmp/x.py", text=f"{GENERATED_FILE_BANNER}\n")


def test_an_artifact_refuses_text_without_the_generated_banner() -> None:
    from alghanem.realization.artifact import GeneratedArtifact

    with pytest.raises(GeneratedArtifactError):
        GeneratedArtifact(relative_path="x.py", text="x = 1\n")


def test_the_backend_refuses_a_non_specification() -> None:
    with pytest.raises(PythonBackendError):
        _backend().generate("not a specification")  # type: ignore[arg-type]
