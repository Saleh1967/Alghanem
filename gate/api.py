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

import functools
import gzip
import hashlib
from collections.abc import Iterable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Final, cast

from .contextual import Certificate as _Cert
from .contextual import Codebook, Context, project
from .licence import (
    continue_licensed,
    hadd_ok,
    hadd_pause_ok,
    kind_of,
    pause_licensed,
    repair_junction,
    straddles,
)
from .residue import Edit, has_marks, repair, unrepair

__all__ = [
    "CORPUS_SHA256",
    "HADITH_CORPUS",
    "HADITH_LINES_SHA256",
    "SEALED_CORPORA",
    "Certificate",
    "Context",
    "Refusal",
    "derive",
    "enter",
    "exit",
    "gate",
    "recover",
    "sealed_forms",
]

_ROOT: Final[Path] = Path(__file__).resolve().parents[1]
CORPUS: Final[Path] = _ROOT / "corpora" / "quran-simple-enhanced.txt"
CORPUS_SHA256: Final[str] = (
    "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
)
HADITH_CORPUS: Final[Path] = Path(__file__).resolve().parent.parent / "corpora" / "hadith" / (
    "sahihain-lines.txt.gz")
HADITH_LINES_SHA256: Final[str] = (
    "14b1a4b7a6d67449b23f016f351d12da9a934ce76116e3c283042705c6d71e3b"
)
SEALED_CORPORA: Final[dict[str, str]] = {
    CORPUS.name: CORPUS_SHA256,
    HADITH_CORPUS.name: HADITH_LINES_SHA256,
}
"""المدوّناتُ المختومة ببصمة محتواها (بعد فكّ الضغط إن كانت مضغوطة): المصحفُ، والصحيحان سطورًا
(`tools/gen_hadith_lines.py`، من ملفّي Open-Hadith-Data المختومين، ODbL 1.0). الرموزُ `<…>` فيها
رموزُ طبعةٍ مسمّاة لا كلمات."""

@dataclass(frozen=True)
class Certificate:
    """شهادةُ الكلمة: شهادةُ الصورة القانونيّة (ذرّاتٌ وعدد) + بقيّةُ الرسم (قواعدُ الطبعة بمواضعها).

    `A116.Residue`: الرسمُ = الصورةُ + البقيّة، ويُردّ بعينه (`chain_restore`)، والرسمُ يحدّدهما معًا
    (`residue_separates`). فالبصمةُ الكاملة (العدد، البقيّة)، لا العددُ وحدَه.
    `junction`: ما فعله الوصلُ بآخر الكلمة **اليساريّة** عند التقاء الساكنين على الحدّ (`A116.Iltiqa`:
    `FARQ_ALIF_DROPPED` | `MADD_DROPPED` | `SAKIN_KASRA`) — وجهٌ مسمًّى لا تخمين؛ ذرّاتُ هذه الكلمة لا
    تُمسّ.
    """

    core: _Cert
    residue: tuple[Edit, ...]
    junction: str | None = None

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


@functools.lru_cache(maxsize=4)
def sealed_forms(corpus: Path = CORPUS) -> frozenset[str]:
    """الصورُ القانونيّةُ للمدوّنة المختومة (بعد إصلاح الرسم بقواعد الطبعة المسمّاة `residue`)؛
    تُقرأ مرّةً وتُفحص بصمتُها، فلا تُعاد قراءتُها لكلّ سياق."""

    raw = corpus.read_bytes()
    if corpus.name.endswith(".gz"):
        raw = gzip.decompress(raw)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SEALED_CORPORA.get(corpus.name):
        raise ValueError(f"WRONG_SEALED_CORPUS:{digest}")
    text = raw.decode("utf-8")
    surfaces = {w for w in text.split() if not is_marker(w) and _arabic(w)}
    return frozenset(repair(w)[0] for w in surfaces)


class Gate:
    """قاموسٌ مختومٌ على مدوّنةٍ ببصمتها، في سياقٍ واحد. يُبنى مرّةً ويُسأل كثيرًا.

    المجالُ المعلَن `domain` (إن أُعطي) صورٌ قانونيّة **من المدوّنة المختومة** يُبنى القاموسُ عليها وحدَها
    في هذا السياق — كما يفعل `gate.audit` لكلّ كلمةٍ يساريّة؛ وما خرج عن المختوم يُرفض باسمه
    `DOMAIN_OUTSIDE_SEALED_CORPUS`. الشهادةُ تسمّي قاموسَها ببصمته، فالمجالُ المقيَّد قاموسٌ مسمًّى لا
    مجالٌ مخمَّن؛ وبلا `domain` القاموسُ على المدوّنة كلِّها.
    """

    def __init__(
        self,
        context: Context | None = None,
        corpus: Path = CORPUS,
        domain: Iterable[str] | None = None,
    ) -> None:
        context = context or Context()
        if context.entry == "joined":
            # الكلمةُ اليساريّة تدخل بصورتها القانونيّة (إصلاحُ الرسم ثابتٌ عليها: `repair` لا يغيّرها)،
            # فالسياقُ المسمّى في الشهادة هو الصورةُ لا رسمُها.
            context = replace(context, left=repair(context.left)[0])
        self.context = context
        sealed = sealed_forms(corpus)
        forms: frozenset[str] = sealed if domain is None else frozenset(domain)
        if not forms <= sealed:
            # القاموسُ على الصور القانونيّة: الرسمُ يدخل بعد إصلاحه بقواعد الطبعة المسمّاة (`residue`).
            raise ValueError("DOMAIN_OUTSIDE_SEALED_CORPUS")
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
        # الترخيصُ بالحدّ: وصلًا `Hadd.strictB` (`continueB ∧ haddB`)، ووقفًا `Hadd.strictPauseB`
        # (`pauseB ∧ haddPauseB`: المدُّ العارض للسكون — `v c` في الطرف وحدَه يُقبل؛ `strictB_pause`).
        pause = self.context.exit == "pause"
        licensed = pause_licensed if pause else continue_licensed
        hadd = hadd_pause_ok if pause else hadd_ok
        if self.context.entry == "joined":
            # قانونُ الحدّ (`Boundary.join_iff`): الموصولُ يُرخَّص مع ما قبله، لا وحدَه؛ وما سقطت وصلُه
            # لا يُقبل بعد ساكن (`pause_then_join_is_not_join`). لا تُحشَر كسرةٌ: رفضٌ مسمًّى.
            left = project(repair(self.context.left)[0], Context())
            if left["status"] != "READY":
                return Refusal("DEFER", ("LEFT_CONTEXT_HAS_NO_CERTIFICATE",))
            # التقاءُ الساكنين على الحدّ (`Iltiqa.repair`): الألفُ الفارقة تسقط، أو المدُّ يُحذف، أو
            # الساكنُ يُكسَر — في آخر اليساريّة وحدَها، وجهًا مسمًّى يحمله الشهادة؛ وإلّا لا شيء.
            left_atoms, junction = repair_junction(tuple(left["atoms"]), atoms)
            joined = left_atoms + atoms
            if not licensed(kind_of(joined)):
                return Refusal("REJECT", ("JUNCTION_NOT_LICENSED",)
                               + (("NOT_PAUSE_LICENSED",) if pause else ()))
            if not hadd(joined):
                # `Hadd.strictB`/`strictPauseB`: مدٌّ قبل ساكنٍ غيرِ مدغمٍ داخلَ الكلمة (يَا + لْأَرْضِ)
                # — لا يُقصَّر تخمينًا؛ وقفًا الطرفُ وحدَه مُعفًى (`geminatePauseB_vc_carrier`).
                return Refusal("REJECT", ("JUNCTION_NOT_LICENSED", "CVVC_NOT_GEMINATE"))
            if straddles(left_atoms, atoms):
                # `Hadd.strictJoinB`/`strictJoinPauseB`: المدُّ في كلمةٍ والمدغمُ في الأخرى
                # (يَا + شْشَافِعِينَ) — الاستثناءُ داخلَ الكلمة الواحدة وحدَها؛ والمدُّ يُقصَّر نطقًا، فلا
                # يُرخَّص ولا يُقصَّر تخمينًا.
                return Refusal("REJECT", ("JUNCTION_NOT_LICENSED", "CVVC_ACROSS_WORD_BOUNDARY"))
            return Certificate(core, residue, junction)
        elif not licensed(kind_of(atoms)):
            # الترخيصُ الثلاثيّ (`Ternary.ContinueLicensed`/`PauseLicensed`) هو الحكمُ الأخير.
            return Refusal("REJECT", ("NOT_PAUSE_LICENSED",) if pause
                           else ("NOT_CONTINUE_LICENSED_AFTER_REPAIR",))
        elif not hadd(atoms):
            # قيدُ الحدّ (`Hadd.strictB`/`strictPauseB`): قافيةُ مدٍّ داخليّة لا يُغلقها أوّلُ مثلين (قَالْتُ).
            return Refusal("REJECT", ("CVVC_NOT_GEMINATE",))
        return Certificate(core, residue)

    def exit(self, cert: Certificate) -> bytes:
        canonical = cast(str, self.book.decode(cert.core))  # type: ignore[no-untyped-call]
        return unrepair(canonical, cert.residue).encode("utf-8")


def _arabic(w: str) -> bool:
    return any("ء" <= c <= "ي" for c in w)


def is_marker(w: str) -> bool:
    """رمزُ طبعةٍ في المدوّنة المختومة (`<sel>` في المصحف؛ `<rlm>`، `<q>`، `<ltr:ح>`… في الصحيحين): ليس
    كلمةً فلا يدخل البوّابة ولا يُعدّ موقعًا."""

    return len(w) > 2 and w[0] == "<" and w[-1] == ">"


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


def derive(
    root: str, before_object: bool = False, ilhaq: bool = False
) -> dict[str, list[tuple[str, str, str]]]:
    """جذرٌ ← صورُ الفعل المولَّدةُ بالقواعد المعلنة: الصورةُ ← قراءاتُها (الصيغة، الوزن، الضمير).
    وبـ`ilhaq=True` الملحَقُ بالرباعيّ من الثلاثيّ الصحيح وحدَه (باب الكتاب س19135–19138؛ سماعيٌّ
    معجمًا فلا يدخل الفهرسَ المقيس)."""

    from .mabni_verbs import ilhaq_forms, verb_forms

    return dict(ilhaq_forms(root, before_object) if ilhaq else verb_forms(root, before_object))


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
