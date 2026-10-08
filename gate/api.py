"""البوّابةُ الرسميّة: المدخلُ الوحيدُ من البايتات، والمخرجُ الوحيدُ إليها.

لا يدخل نصٌّ إلى أيّ طبقةٍ في هذه الشجرة ولا يخرج منها إلّا من هنا، بأربع دوالّ:

* `enter(data, context)` — بايتاتُ كلمةٍ واحدةٍ (UTF-8) ← `Certificate` أو `Refusal`.
  الشهادةُ تحمل ذرّاتِ الـ116، ورتبةَ الكلمة في ليفها، والعددَ الذي يطويهما (اقترانُ
  كانتور على ترقيم الذرّات)، وبصمةَ القاموس. والرفضُ يحمل سببَه مسمًّى ولا يُخمَّن شيء.
* `exit(cert)` — الشهادةُ ← بايتاتُ الكلمة بعينها (`Fiber.decode_encode` + ردُّ البقيّة
  `Residue.chain_restore`).
* البقيّة: الرسمُ يدخل بعد إصلاحه بقواعد الطبعة الثماني المسمّاة (`residue.repair`)، وتحمل الشهادةُ
  السجلَّ ليُردّ الرسمُ بعينه عند الخروج.
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
from .licence import continue_licensed, hadd_ok, kind_of, straddles
from .residue import Edit, has_marks, repair, unrepair

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

@dataclass(frozen=True)
class Certificate:
    """شهادةُ الكلمة: شهادةُ الصورة القانونيّة (ذرّاتٌ وعدد) + بقيّةُ الرسم (قواعدُ الطبعة بمواضعها).

    `A116.Residue`: الرسمُ = الصورةُ + البقيّة، ويُردّ بعينه (`chain_restore`)، والرسمُ يحدّدهما معًا
    (`residue_separates`). فالبصمةُ الكاملة (العدد، البقيّة)، لا العددُ وحدَه.
    """

    core: _Cert
    residue: tuple[Edit, ...]

    @property
    def atoms(self) -> tuple[str, ...]:
        return self.core.atoms

    @property
    def integer(self) -> int:
        return self.core.integer


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
        surfaces = {w for w in text.split() if w != "<sel>" and _arabic(w)}
        # القاموسُ على الصور القانونيّة: الرسمُ يدخل بعد إصلاحه بقواعد الطبعة المسمّاة (`residue`).
        forms = {repair(w)[0] for w in surfaces}
        self.book = Codebook(forms, self.context)  # type: ignore[no-untyped-call]

    def enter(self, data: bytes) -> Certificate | Refusal:
        try:
            surface = data.decode("utf-8")
        except UnicodeDecodeError:
            return Refusal("REJECT", ("NOT_UTF8",))
        if not surface or any(c.isspace() for c in surface):
            # المدخلُ كلمةٌ واحدة: لا فراغَ فيها ولا تكون فارغة — رفضٌ مسمًّى لا استثناء.
            return Refusal("REJECT", ("NOT_ONE_TOKEN",))
        if not has_marks(surface):
            # كلمةٌ بلا أيّ علامة (الحروفُ المقطّعة، نصٌّ غيرُ مشكول): لا تُصلَح ولا تُخمَّن.
            return Refusal("DEFER", ("UNVOCALIZED_WORD_IS_NEVER_GUESSED",))
        canonical, residue = repair(surface)
        if canonical not in self.book.decisions:
            decision = project(canonical, self.context)
            if decision["status"] != "READY":
                return Refusal(decision["status"], _reasons(decision))
            return Refusal("OUTSIDE_DECLARED_DOMAIN", ())
        decision = self.book.decisions[canonical]
        if decision["status"] != "READY":
            return Refusal(decision["status"], _reasons(decision))
        core = self.book.encode(canonical)  # type: ignore[no-untyped-call]
        atoms = tuple(core.atoms)
        if self.context.entry == "joined":
            # قانونُ الحدّ (`Boundary.join_iff`): الموصولُ يُرخَّص مع ما قبله، لا وحدَه؛ وما سقطت وصلُه
            # لا يُقبل بعد ساكن (`pause_then_join_is_not_join`). لا تُحشَر كسرةٌ: رفضٌ مسمًّى.
            left = project(repair(self.context.left)[0], Context())
            if left["status"] != "READY":
                return Refusal("DEFER", ("LEFT_CONTEXT_HAS_NO_CERTIFICATE",))
            joined = tuple(left["atoms"]) + atoms
            if not continue_licensed(kind_of(joined)):
                return Refusal("REJECT", ("JUNCTION_NOT_LICENSED",))
            if not hadd_ok(joined):
                # `Hadd.strictB`: مدٌّ قبل ساكنٍ غيرِ مدغمٍ عند الحدّ (يَا + لْأَرْضِ) — لا يُقصَّر تخمينًا.
                return Refusal("REJECT", ("JUNCTION_NOT_LICENSED", "CVVC_NOT_GEMINATE"))
            if straddles(tuple(left["atoms"]), atoms):
                # `Hadd.strictJoinB`: المدُّ في كلمةٍ والمدغمُ في الأخرى (يَا + شْشَافِعِينَ) — الاستثناءُ
                # داخلَ الكلمة الواحدة وحدَها؛ والمدُّ يُقصَّر نطقًا، فلا يُرخَّص ولا يُقصَّر تخمينًا.
                return Refusal("REJECT", ("JUNCTION_NOT_LICENSED", "CVVC_ACROSS_WORD_BOUNDARY"))
        elif not continue_licensed(kind_of(atoms)):
            # الترخيصُ الثلاثيّ (`Ternary.ContinueLicensed`) هو الحكمُ الأخير: لا شهادةَ لغير المرخَّص.
            return Refusal("REJECT", ("NOT_CONTINUE_LICENSED_AFTER_REPAIR",))
        elif not hadd_ok(atoms):
            # قيدُ الحدّ (`Hadd.strictB`): قافيةُ مدٍّ لا يُغلقها أوّلُ مثلين (قَالْتُ) — رفضٌ مسمًّى.
            return Refusal("REJECT", ("CVVC_NOT_GEMINATE",))
        return Certificate(core, residue)

    def exit(self, cert: Certificate) -> bytes:
        canonical = cast(str, self.book.decode(cert.core))  # type: ignore[no-untyped-call]
        return unrepair(canonical, cert.residue).encode("utf-8")


def _arabic(w: str) -> bool:
    return any("ء" <= c <= "ي" for c in w)


def _reasons(decision: dict[str, Any]) -> tuple[str, ...]:
    """أسبابُ الرفض بأسمائها؛ وما غلّفه الجسرُ في `upstream_error` يُفكّ فلا يخرج رفضٌ بلا اسم."""

    out: list[str] = []
    for r in decision.get("reasons") or ():
        if isinstance(r, dict):
            inner = r.get("upstream_error")
            if isinstance(inner, dict) and r.get("reason") is None:
                out.append(str(inner.get("reason")))
            else:
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
        if isinstance(surface_or_cert, Certificate)
        else surface_or_cert
    )
    outcome, found = recover_verb(surface)
    return outcome.name, tuple((a.root, a.kind, a.form, a.person) for a in found)


def forms(data: Iterable[bytes]) -> list[Certificate | Refusal]:
    """عدّةُ كلماتٍ دفعةً واحدة."""

    g = gate()
    return [g.enter(d) for d in data]
