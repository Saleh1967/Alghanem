"""شاهدُ حفظ الدلالة التاريخيّة: الطبقةُ المجمَّدة بايتاتُها ومغلقُ تبعيّتها معًا."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "src" / "alghanem"

_FROZEN_LAYER_DIGESTS: dict[str, str] = {
    "canonical_content.py": (
        "a12f95ff33fd5e3b3364c1a6612f9e254243648335ffafe43fb8ad6d7aa9ac23"
    ),
    "linguistic/anchored.py": (
        "7debab99fd13ff87ca26f4ef5d2c57f250668419b5c9fbd669152068c4781098"
    ),
    "linguistic/closure.py": (
        "e3b23b05c28004ed1c27fb7ec7eaef32b15fe63758a5a110e9ae28a85a61dc0c"
    ),
    "linguistic/hypothesis.py": (
        "c4c0bf475533a8efc2186f795cb80d2b1796abfa9d94fd8405ef92685cae8500"
    ),
    "linguistic/nisbah.py": (
        "00f7d209c03c36f9e8e5ff75b796abe6f53c2e5008096527f2bc36b50591cff0"
    ),
    "linguistic/role.py": (
        "b73a823f68b1717279ea8993b2a278bcd6b5dac35c83edf6319364cb0136c192"
    ),
    "linguistic/schema.py": (
        "1bce9ba2a0871b16db3292dc2151f2211c68c37a96553d56aee33e619a141d4a"
    ),
    "metaalgebra/composition.py": (
        "e8fd382c338fe1ff933775adb04f2356b8b8051d7cdda62f2b3d823ab37a2d72"
    ),
    "metaalgebra/layer.py": (
        "6db692fdd11b3a9405101dd99b071a8b26e14de23c267eaeb1305091f4d06d09"
    ),
    "metaalgebra/schema.py": (
        "a45d0aaad190c0de84bc767e3d79dfc89f604a909f27d4112e41ff3afab5da10"
    ),
    "metaalgebra/specification.py": (
        "8ed5cf4db056c7836aab573402b80ec6f613e4db2843f159510a60ed718869b7"
    ),
    "metaalgebra/standing.py": (
        "49358b7aab008ae86c91aba1244a30bdcbce6e815abae33ea7f32cf792c60934"
    ),
    "metaalgebra/transition.py": (
        "357aaaf0f92b6151ace835880c12b125a3cbe928e1738c2bf4a55de2b101dfb1"
    ),
    "ontology/general.py": (
        "f804a7edc765e27f7144ba622b49e6fae7e8769cdc4708a5c9f4c58e198ab155"
    ),
    "ontology/linguistic.py": (
        "7fbd4afbaabe33f948e50dc4db07e8926f5870643ff917f5a50f913f6f6ec99c"
    ),
    "prior/conditions.py": (
        "2ebe65dbed646311f6156a2cefe0c11ad065cbed110cd367adfd1f115da464ee"
    ),
}
"""مغلقُ تبعيّة `v2`: بايتاتُ كلِّ وحدةٍ تدخل في معناها، لا بايتاتُها وحدَها."""

_FROZEN_SCHEMA_DIGESTS: dict[str, str] = {
    "linguistic-nisbah.schema.v2": (
        "e6542de0eb08384f3501f2874e191fd58eed214724c77f8b52302fc8bc29eccb"
    ),
}


def _file_digest(relative: str) -> str:
    return hashlib.sha256((_PACKAGE_ROOT / relative).read_bytes()).hexdigest()


def _module_path(module: str) -> str:
    return module.replace(".", "/") + ".py"


def _internal_imports(relative: str) -> set[str]:
    """اقرأ ما تستورده الوحدةُ من داخل الحزمة، نسبيًّا كان أو مُسمًّى."""

    package_parts = relative.split("/")[:-1]
    tree = ast.parse((_PACKAGE_ROOT / relative).read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level:
                base = package_parts[: len(package_parts) - (node.level - 1)]
                target = base + (node.module.split(".") if node.module else [])
            elif node.module and node.module.startswith("alghanem."):
                target = node.module.split(".")[1:]
            else:
                continue
            candidate = "/".join(target) + ".py"
            if (_PACKAGE_ROOT / candidate).is_file():
                found.add(candidate)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("alghanem."):
                    candidate = _module_path(alias.name[len("alghanem.") :])
                    if (_PACKAGE_ROOT / candidate).is_file():
                        found.add(candidate)
    return found


def _closure(root: str) -> set[str]:
    seen: set[str] = set()
    pending = [root]
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        pending.extend(sorted(_internal_imports(current)))
    return seen


def test_the_second_version_keeps_its_own_bytes() -> None:
    assert (
        _file_digest("linguistic/anchored.py")
        == _FROZEN_LAYER_DIGESTS["linguistic/anchored.py"]
    )


def test_the_second_version_keeps_the_bytes_of_everything_it_depends_on() -> None:
    """حفظُ البايتات وحدَه ليس حفظًا: المعنى يتغيّر إذا تغيّرت وحدةٌ يعتمد عليها."""

    for relative, expected in _FROZEN_LAYER_DIGESTS.items():
        assert _file_digest(relative) == expected, relative


def test_the_dependency_closure_gained_no_new_member() -> None:
    assert _closure("linguistic/anchored.py") == set(_FROZEN_LAYER_DIGESTS)


def test_the_new_layer_is_outside_the_frozen_closure() -> None:
    frozen = _closure("linguistic/anchored.py")
    for newcomer in (
        "linguistic/anchored_v3.py",
        "ontology/linguistic_v2.py",
        "ontology/lineage.py",
        "prior/references.py",
    ):
        assert (_PACKAGE_ROOT / newcomer).is_file(), newcomer
        assert newcomer not in frozen, newcomer


def test_the_new_layer_reads_the_parent_identity_and_nothing_else_of_it() -> None:
    """`v3` يستورد من `v2` مرجعَ الهويّة فقط، ولا يبني بأدوات `v2`."""

    tree = ast.parse(
        (_PACKAGE_ROOT / "linguistic/anchored_v3.py").read_text(encoding="utf-8")
    )
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "anchored":
            imported.update(alias.name for alias in node.names)
    assert imported == {"ANCHORED_NISBAH_SCHEMA"}


def test_the_frozen_schema_identities_did_not_move() -> None:
    from alghanem.linguistic.anchored import ANCHORED_NISBAH_SCHEMA

    assert (
        ANCHORED_NISBAH_SCHEMA.content_id
        == _FROZEN_SCHEMA_DIGESTS["linguistic-nisbah.schema.v2"]
    )


def test_the_third_schema_is_another_identity_beside_the_second() -> None:
    from alghanem.linguistic.anchored_v3 import ANCHORED_V3_NISBAH_SCHEMA

    assert ANCHORED_V3_NISBAH_SCHEMA.content_id not in set(
        _FROZEN_SCHEMA_DIGESTS.values()
    )
