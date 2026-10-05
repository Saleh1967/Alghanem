"""البوّابةُ الرسميّة: المدخلُ الوحيدُ من البايتات، والمخرجُ الوحيدُ إليها.

لا يدخل نصٌّ إلى أيّ طبقةٍ في هذه الشجرة ولا يخرج منها إلّا من هنا، بأربع دوالّ:

* `enter(data, context)` — بايتاتُ كلمةٍ واحدةٍ (UTF-8) ← `Certificate` أو `Refusal`.
  الشهادةُ تحمل ذرّاتِ الـ116، ورتبةَ الكلمة في ليفها، والعددَ الذي يطويهما (اقترانُ
  كانتور على ترقيم الذرّات)، وبصمةَ القاموس. والرفضُ يحمل سببَه مسمًّى ولا يُخمَّن شيء.
* `exit(cert)` — الشهادةُ ← بايتاتُ الكلمة بعينها (`Fiber.decode_encode`).
* `derive(root, template)` — جذرٌ وقالبٌ ← صورُ الفعل المولَّدة، كلٌّ منها شهادةً.
* `recover(cert)` — شهادةٌ ← الجذورُ والأوزانُ التي تولِّدها، إن كانت مولَّدةً.

البرهان: `formal/a116` (الترقيمُ `Numbering`، الليفُ `Fiber`، التقطيعُ `Stages`،
الاشتقاقُ `Ishtiqaq`، التمدّداتُ `Recovery`)، ومطابقتُه بهذه الشيفرة في
`tests/test_conformance.py`. وما ليس له برهانٌ موسومٌ في `Certificate.standing`.

المجالُ مجالُ القاموس المختوم: كلمةٌ خارجَه تُرفض بـ`OUTSIDE_DECLARED_DOMAIN` ولا تُخمَّن.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

from .contextual import Certificate as _Cert
from .contextual import Codebook, Context, project

__all__ = [
    "CORPUS_SHA256",
    "Certificate",
    "Context",
    "Refusal",
    "derive",
    "enter",
    "exit",
    "gate",
    "recover",
]

_ROOT: Final[Path] = Path(__file__).resolve().parents[1]
CORPUS: Final[Path] = _ROOT / "corpora" / "quran-simple-enhanced.txt"
CORPUS_SHA256: Final[str] = (
    "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
)

Certificate = _Cert


@dataclass(frozen=True)
class Refusal:
    """رفضٌ مسمًّى: الحالة (DEFER أو REJECT أو OUTSIDE_DECLARED_DOMAIN) وأسبابها."""

    status: str
    reasons: tuple[str, ...]


class Gate:
    """قاموسٌ مختومٌ على مدوّنةٍ ببصمتها، في سياقٍ واحد. يُبنى مرّةً ويُسأل كثيرًا."""

    def __init__(self, context: Context | None = None, corpus: Path = CORPUS) -> None:
        raw = corpus.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != CORPUS_SHA256:
            raise ValueError(f"WRONG_SEALED_CORPUS:{digest}")
        self.context = context or Context()
        text = raw.decode("utf-8")
        forms = {w for w in text.split() if w != "<sel>" and _arabic(w)}
        self.book = Codebook(forms, self.context)  # type: ignore[no-untyped-call]

    def enter(self, data: bytes) -> Certificate | Refusal:
        surface = data.decode("utf-8")
        if surface not in self.book.decisions:
            decision = project(surface, self.context)
            if decision["status"] != "READY":
                return Refusal(decision["status"], _reasons(decision))
            return Refusal("OUTSIDE_DECLARED_DOMAIN", ())
        decision = self.book.decisions[surface]
        if decision["status"] != "READY":
            return Refusal(decision["status"], _reasons(decision))
        return cast(Certificate, self.book.encode(surface))  # type: ignore[no-untyped-call]

    def exit(self, cert: Certificate) -> bytes:
        return cast(str, self.book.decode(cert)).encode("utf-8")  # type: ignore[no-untyped-call]


def _arabic(w: str) -> bool:
    return any("ء" <= c <= "ي" for c in w)


def _reasons(decision: dict[str, Any]) -> tuple[str, ...]:
    out: list[str] = []
    for r in decision.get("reasons") or ():
        if isinstance(r, dict):
            out.append(str(r.get("reason")))
        else:
            out.append(str(r))
    return tuple(out)


_GATE: Gate | None = None


def gate() -> Gate:
    """البوّابةُ على المدوّنة المختومة في سياق الابتداء والاستمرار؛ تُبنى عند أوّل نداء."""

    global _GATE
    if _GATE is None:
        _GATE = Gate()
    return _GATE


def enter(data: bytes, context: Context | None = None) -> Certificate | Refusal:
    """بايتاتُ كلمةٍ ← شهادةٌ أو رفضٌ مسمًّى."""

    if context is None:
        return gate().enter(data)
    return Gate(context).enter(data)


def exit(cert: Certificate) -> bytes:  # noqa: A001 - الاسمُ مقصود: مخرجُ البوّابة
    """شهادةٌ ← بايتاتُ الكلمة بعينها."""

    return gate().exit(cert)


def derive(root: str, before_object: bool = False) -> dict[str, list[tuple[str, str, str]]]:
    """جذرٌ ← صورُ الفعل المولَّدةُ بالقواعد المعلنة: الصورةُ ← قراءاتُها (الصيغة، الوزن، الضمير)."""

    from .mabni_verbs import verb_forms

    return dict(verb_forms(root, before_object))


Reading = tuple[str, str, str, str]


def recover(surface_or_cert: Certificate | str) -> tuple[str, tuple[Reading, ...]]:
    """صورةٌ (أو شهادتُها) ← (المآل، التحليلات: جذر، صنف، وزن، ضمير)."""

    from .mabni_bridge import recover_verb

    surface = (
        gate().exit(surface_or_cert).decode("utf-8")
        if isinstance(surface_or_cert, _Cert)
        else surface_or_cert
    )
    outcome, found = recover_verb(surface)
    return outcome.name, tuple((a.root, a.kind, a.form, a.person) for a in found)


def forms(data: Iterable[bytes]) -> list[Certificate | Refusal]:
    """عدّةُ كلماتٍ دفعةً واحدة."""

    g = gate()
    return [g.enter(d) for d in data]
