"""شرطٌ ومانعٌ ومتعذِّر، وسببٌ بمعناه الضيّق: ما يُختبَر قبل توليد حاملِ حالة.

ما تفعله هذه الوحدة
-------------------
`alghanem.arabic.encoding.carrier_state_candidate` يرفض عند البناء في ثلاثين
موضعًا، وكلُّ رفضٍ منها له جنسٌ أصوليٌّ مختلف، ولم يكن لواحدٍ منها اسمُ جنسه.
هذه الوحدة **تقرؤها وتُصنِّفها ولا تمسّها**: لا تُعدَّل رسالةُ رفضٍ واحدة، ولا
يُضاف رفضٌ، ولا يُحذَف. والمواضع تُشتقّ من شجرة النحو المجرّدة للوحدة نفسها
(`derive_refusal_sites`) لا من قائمةٍ مكتوبةٍ يدًا، فإضافةُ رفضٍ جديدٍ بلا جنسٍ
تُسقِط استيرادَ هذه الوحدة عند الاستيراد لا تمرّ بتحذير
(`derive_unclassified_refusal_sites`).

والأجناس ثلاثة، مغلقة:

* **شرطٌ**: قيدٌ موجَبٌ على جنس المُدخَل، إن تخلّف لم يُمكن الحكمُ أصلًا
  («الحاملُ نقطةُ ترميزٍ واحدة»، «الحالةُ عضوٌ في `CarrierState`»).
* **مانعٌ**: بنيةٌ حاضرةٌ تمنع الحكمَ مع قيام شرطه («مَقعدٌ على غير مضيفه»،
  «تنوينٌ على حالةٍ لا تحمله»).
* **متعذِّرٌ**: موضعٌ لا تحسمه العلاماتُ المكتوبة، فالرفضُ فيه امتناعٌ عن
  الترجيح لا حكمٌ بالفساد. وهما موضعان اثنان بعينهما: الكتابةُ الثانية في
  خانةٍ اشتُقّت قيمتُها مرّة. والوحدةُ المُصنَّفة تقول عن نفسها إنها «ترفض ولا
  تُصلِح» في هذين الموضعين، فالتصنيفُ قراءةٌ لما فعلته لا إضافةٌ عليه.

**والسببُ — بمعناه الضيّق — هو الجديدُ الوحيد هنا**: علامةٌ كاشفةٌ تُختبَر قبل
التوليد، لا علّةٌ فاعلة. والعلّةُ غائبةٌ عن هذه الثلاثيّة **بقرارٍ مُعلَن** لا
بسكوت (`EFFICIENT_CAUSE_IS_OMITTED_BY_DECISION_NOT_BY_SILENCE`).

الفراغُ الذي تسدّه
------------------
المولِّد اليوم يُخرِج «الحمد» خمسَ حالاتٍ كلُّها `SUKUN_IMPLICIT`، وليس في
السطح علامةٌ واحدةٌ تُثبت شيئًا منها. فالحالةُ هناك **مفترَضةٌ عند غياب
العلامة**، وهي في النوع نفسِه الذي تُكتب فيه فتحةُ «بَ» المقروءةُ من السطح.
و`StateEvidence` يفصل الجنسين، فيصير الفرقُ مقروءًا في النوع لا مطويًّا في
قيمةٍ واحدة. والجنسُ الثاني سُمّي بما يفعله الكودُ فعلًا — «افتراضٌ عند
الغياب» — لا «سكونًا أصليًّا»، لأنّ الثاني دعوى لغويّةٌ تحتاج دليلًا ليس في
السطح (`ABSENCE_ASSUMPTION_IS_NAMED_FOR_THE_CODE_NOT_FOR_A_LINGUISTIC_CLAIM`).

والجنسُ الثالث يرفع تناقضًا قائمًا بين وحدتين في هذه الشجرة:
`alghanem.arabic.ibtida_wasl_waqf_registration` سجّلت أنّ ألف «الْحَمْدُ» لا
تحمل علامةً أصلًا، فمنزلتُها **متعذّرةُ القياس** لا ساكنةٌ ولا متحرّكة
(`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`)، بينما يجزم المولِّدُ
فيها بالسكون. فالقارئُ هنا يُصنِّف ذلك الموضعَ `UNDECIDABLE`، ولا يُعدِّل
المولِّدَ ولا يكذّبه: وحدةُ `CarrierStateUnit` تبقى كما أخرجها بايتًا بايتًا،
ويُضاف إليها جنسُ سببها من خارجها.

**وألفُ الوصل المكتوبة (ٱ) ليست من هذا الجنس**: هي علامةٌ مكتوبةٌ تحسم ما لا
تحسمه الألفُ المجرّدة، فمَن كتبها فقد أزال التعذُّر. فالتعذُّر مشتقٌّ من خلوّ
السطح من العلامة، لا مُعلَنٌ للألف بما هي ألف
(`UNDECIDABILITY_IS_DERIVED_FROM_THE_SURFACE_NOT_DECLARED_FOR_THE_ALEF`).

العلامةُ المرصودةُ ليست الحالةَ المشتقّة
-----------------------------------------
`MarkObservation` تُسجِّل نقطةَ ترميزٍ مرصودةً بموضعها في السطح المُوحَّد، ولا
تحمل حالةً ولا تدّعي أنّ حالةً اشتُقّت منها. وأنّ الجنسين متمايزان يُشتقّ ولا
يُقال: سطح «بَُ» يُخرِج علامتين مرصودتين ويُخرِج **صفرَ** حالات، لأنّ المولِّد
يرفضه بالكتابة الثانية. فالرصدُ قائمٌ حيث لا حالةَ أصلًا
(`AN_OBSERVED_MARK_IS_NOT_A_DERIVED_STATE`).

القابليّةُ مرصودةٌ لا مُعلَنة
-----------------------------
`derive_observed_capacities` لا تقرأ جدولًا مكتوبًا يدًا: تُرجع ما وقع فعلًا من
العلامات على الحوامل في النصوص المُمرَّرة إليها. وما لم يُرصَد يُسجَّل
**غيرَ مرصودٍ** لا ممتنعًا، لأنّ عدمَ الشاهد ليس شاهدَ العدم
(`ABSENCE_OF_A_WITNESS_IS_NOT_A_WITNESS_OF_ABSENCE`). وهي مقيَّدةٌ بالنصوص
التي مرّت عليها وحدها، فلا تُقرأ وصفًا للعربية
(`OBSERVED_CAPACITY_IS_BOUNDED_BY_THE_SURFACES_IT_READ`).

ما لا يُبنى هنا، وسببُه
-----------------------
* **لا «حقيقة وجودٍ» للحرف**: الهويّةُ مؤجَّلةٌ في هذه الشجرة إلى بوّابة
  ولادةٍ لم تُبنَ، والمتاحُ وجودٌ مرصودٌ في سطحٍ مُمرَّر لا وجودٌ ماهويّ
  (`LETTER_EXISTENCE_HERE_IS_OBSERVED_NOT_ESSENTIAL`).
* **لا «علاقاتٌ» مُعلَنة**: العلاقةُ المشتقّةُ من الرصد مقبولة، والمُعلَنةُ
  سلفًا جدولٌ مستورَدٌ يجب فصلُه كما فُصل جدولا الذلاقة والأدوار في
  `alghanem.arabic.letter_fingerprint` (`NO_RELATION_TABLE_IS_DECLARED_HERE`).

سلطةُ الوحدة
------------
تسجيلٌ واشتقاق، لا سلطة: لا ولادة، ولا حكمَ ولادة، ولا تجميد، ولا `E0`، ولا
تستورد من `kernel/`، ولا تقرؤها بوّابةٌ فيه.
"""

from __future__ import annotations

import ast
import inspect
import unicodedata
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Final, Literal

from . import carrier_state_candidate as _deposited
from .carrier_state_candidate import (
    DECLARED_CARRIERS,
    CarrierState,
    CarrierStateCodec,
    CarrierStateEncodingError,
    CarrierStateUnit,
)

__all__ = [
    "ABSENCE_ASSUMPTION_IS_NAMED_FOR_THE_CODE_NOT_FOR_A_LINGUISTIC_CLAIM",
    "ABSENCE_OF_A_WITNESS_IS_NOT_A_WITNESS_OF_ABSENCE",
    "AN_OBSERVED_MARK_IS_NOT_A_DERIVED_STATE",
    "A_WORD_BOUNDARY_HERE_IS_A_PASSTHROUGH_AND_NOT_A_LEXICAL_BOUNDARY",
    "CLASSIFICATION_READS_THE_DEPOSITED_MODULE_AND_DOES_NOT_AMEND_IT",
    "DECLARED_JOINERS",
    "DECLARED_STATE_MARKS",
    "EFFICIENT_CAUSE_IS_OMITTED_BY_DECISION_NOT_BY_SILENCE",
    "EvidencedUnit",
    "EvidencingReader",
    "LETTER_EXISTENCE_HERE_IS_OBSERVED_NOT_ESSENTIAL",
    "MarkObservation",
    "NORMALIZATION_FORM",
    "NO_RELATION_TABLE_IS_DECLARED_HERE",
    "OBSERVED_CAPACITY_IS_BOUNDED_BY_THE_SURFACES_IT_READ",
    "ORPHAN_MARKS_ARE_CARRIED_AND_EVIDENCE_NOTHING",
    "ObservedCapacityCensus",
    "REFUSAL_GENUS_REGISTRY",
    "RefusalGenus",
    "RefusalSite",
    "STATE_EVIDENCE_NAMED_RESIDUALS",
    "StateEvidence",
    "StateEvidenceError",
    "UNDECIDABILITY_IS_DERIVED_FROM_THE_SURFACE_NOT_DECLARED_FOR_THE_ALEF",
    "derive_mark_observations",
    "derive_observed_capacities",
    "derive_refusal_sites",
    "derive_unclassified_refusal_sites",
]


class StateEvidenceError(ValueError):
    """يُرفَع حين يُبنى شاهدٌ لا يحمل جنسَ سببه، أو يحمل ما لا يُقرأ منه."""


NORMALIZATION_FORM: Final[Literal["NFC"]] = "NFC"
"""صورةُ التوحيد المقروءة هنا، وهي صورةُ المولِّد المُودَع نفسُها."""


# --- المُخلَّفات المُسمّاة ---------------------------------------------------

CLASSIFICATION_READS_THE_DEPOSITED_MODULE_AND_DOES_NOT_AMEND_IT: Final = (
    "every refusal classified here is read out of carrier_state_candidate by "
    "its own abstract syntax tree; no refusal message is reworded, none is "
    "added, and none is removed, so the classification is a reading of what "
    "that module already does and never an amendment to it"
)

EFFICIENT_CAUSE_IS_OMITTED_BY_DECISION_NOT_BY_SILENCE: Final = (
    "the classical fourth term, the efficient cause, is deliberately outside "
    "this triad: sabab is used here in its narrow sense only, as a detectable "
    "sign tested before generation. the omission is recorded as a decision "
    "that stays open to challenge, not absorbed into the existence of the "
    "letter and then passed over in silence"
)

ABSENCE_ASSUMPTION_IS_NAMED_FOR_THE_CODE_NOT_FOR_A_LINGUISTIC_CLAIM: Final = (
    "the second evidence genus is named for what the deposited codec actually "
    "does when no mark is written, and not 'an underlying sukun', which is a "
    "linguistic claim needing evidence that the surface does not carry"
)

UNDECIDABILITY_IS_DERIVED_FROM_THE_SURFACE_NOT_DECLARED_FOR_THE_ALEF: Final = (
    "UNDECIDABLE is derived from a surface that writes no mark at all, so the "
    "written wasla (U+0671) is not undecidable: whoever wrote it removed the "
    "undecidability. nothing is declared undecidable for the alef as such"
)

AN_OBSERVED_MARK_IS_NOT_A_DERIVED_STATE: Final = (
    "MarkObservation records a codepoint seen at an offset and carries no "
    "state; the two genera are kept apart by derivation and not by wording, "
    "since a surface that writes two marks into one slot yields two "
    "observations and zero units, being refused by the deposited codec"
)

A_WORD_BOUNDARY_HERE_IS_A_PASSTHROUGH_AND_NOT_A_LEXICAL_BOUNDARY: Final = (
    "UNDECIDABLE is reported for an alef that opens a run of carriers, and "
    "such a run opens at the start of the surface or after any passthrough "
    "unit that is not a declared joiner. this is a surface rule and never a "
    "lexical one: it does not know what a word is, it knows where the "
    "carriers stop. probing it found its own defect, since a tatweel is a "
    "passthrough that joins rather than separates and opened a word until "
    "DECLARED_JOINERS was named; the set is declared in this module and "
    "derived from no property of Arabic, so another joiner nobody named "
    "would reopen the same defect"
)

ORPHAN_MARKS_ARE_CARRIED_AND_EVIDENCE_NOTHING: Final = (
    "a mark written with no carrier before it is generated as a passthrough "
    "unit by the deposited codec; it is carried here so that no observed mark "
    "is dropped, and it evidences no state, since there is no carrier whose "
    "state it could be"
)

ABSENCE_OF_A_WITNESS_IS_NOT_A_WITNESS_OF_ABSENCE: Final = (
    "a (carrier, mark) pair that no supplied surface exhibits is recorded as "
    "unobserved and never as impossible; no capacity table is written by hand "
    "here and no pair is ruled out"
)

OBSERVED_CAPACITY_IS_BOUNDED_BY_THE_SURFACES_IT_READ: Final = (
    "a derived capacity census is established over the surfaces passed to it "
    "and over no others; it is not a description of Arabic and it does not "
    "become one by being run over more text"
)

LETTER_EXISTENCE_HERE_IS_OBSERVED_NOT_ESSENTIAL: Final = (
    "this module records that a carrier was observed in a supplied surface; "
    "it establishes no identity for that letter, since identity in this tree "
    "is deferred to a birth gate that is not built"
)

NO_RELATION_TABLE_IS_DECLARED_HERE: Final = (
    "no table of relations between letters or between marks is written in "
    "this module; a relation derived from observation is admitted, and a "
    "pre-declared one would be an imported table owing the separation that "
    "letter_fingerprint applies to its ithlaq and role tables"
)

STATE_EVIDENCE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "CLASSIFICATION_READS_THE_DEPOSITED_MODULE_AND_DOES_NOT_AMEND_IT": (
        CLASSIFICATION_READS_THE_DEPOSITED_MODULE_AND_DOES_NOT_AMEND_IT
    ),
    "EFFICIENT_CAUSE_IS_OMITTED_BY_DECISION_NOT_BY_SILENCE": (
        EFFICIENT_CAUSE_IS_OMITTED_BY_DECISION_NOT_BY_SILENCE
    ),
    "ABSENCE_ASSUMPTION_IS_NAMED_FOR_THE_CODE_NOT_FOR_A_LINGUISTIC_CLAIM": (
        ABSENCE_ASSUMPTION_IS_NAMED_FOR_THE_CODE_NOT_FOR_A_LINGUISTIC_CLAIM
    ),
    "UNDECIDABILITY_IS_DERIVED_FROM_THE_SURFACE_NOT_DECLARED_FOR_THE_ALEF": (
        UNDECIDABILITY_IS_DERIVED_FROM_THE_SURFACE_NOT_DECLARED_FOR_THE_ALEF
    ),
    "AN_OBSERVED_MARK_IS_NOT_A_DERIVED_STATE": AN_OBSERVED_MARK_IS_NOT_A_DERIVED_STATE,
    "A_WORD_BOUNDARY_HERE_IS_A_PASSTHROUGH_AND_NOT_A_LEXICAL_BOUNDARY": (
        A_WORD_BOUNDARY_HERE_IS_A_PASSTHROUGH_AND_NOT_A_LEXICAL_BOUNDARY
    ),
    "ORPHAN_MARKS_ARE_CARRIED_AND_EVIDENCE_NOTHING": (
        ORPHAN_MARKS_ARE_CARRIED_AND_EVIDENCE_NOTHING
    ),
    "ABSENCE_OF_A_WITNESS_IS_NOT_A_WITNESS_OF_ABSENCE": (
        ABSENCE_OF_A_WITNESS_IS_NOT_A_WITNESS_OF_ABSENCE
    ),
    "OBSERVED_CAPACITY_IS_BOUNDED_BY_THE_SURFACES_IT_READ": (
        OBSERVED_CAPACITY_IS_BOUNDED_BY_THE_SURFACES_IT_READ
    ),
    "LETTER_EXISTENCE_HERE_IS_OBSERVED_NOT_ESSENTIAL": (
        LETTER_EXISTENCE_HERE_IS_OBSERVED_NOT_ESSENTIAL
    ),
    "NO_RELATION_TABLE_IS_DECLARED_HERE": NO_RELATION_TABLE_IS_DECLARED_HERE,
}


# --- الثلاثيّة: شرطٌ ومانعٌ ومتعذِّر ------------------------------------------


class RefusalGenus(Enum):
    """جنسُ الرفض. مفردةٌ مغلقة، ولكلّ عضوٍ منها موضعٌ قائمٌ في المولِّد."""

    CONDITION = "condition"
    PREVENTER = "preventer"
    UNDECIDABLE = "undecidable"

    @property
    def arabic_name(self) -> str:
        """اسمُ الجنس بالعربية، كما يُسمّى في أصول الفقه."""
        return _GENUS_ARABIC_NAMES[self]


_GENUS_ARABIC_NAMES: Final[dict[RefusalGenus, str]] = {
    RefusalGenus.CONDITION: "شرط",
    RefusalGenus.PREVENTER: "مانع",
    RefusalGenus.UNDECIDABLE: "متعذِّر",
}

if len(_GENUS_ARABIC_NAMES) != len(RefusalGenus):  # pragma: no cover - guard
    raise RuntimeError("every RefusalGenus member carries an Arabic name")


@dataclass(frozen=True, order=True)
class RefusalSite:
    """موضعُ رفضٍ واحدٍ في المولِّد المُودَع، مُشتقٌّ من شجرة نحوه لا مكتوبٌ يدًا.

    المفتاحُ هو اسمُ الدالّة الحاضنة ونصُّ الرسالة الثابت بعد توحيد الفراغ،
    ولا يُستعمَل رقمُ السطر مفتاحًا لأنّ تحريرًا في أوّل الملفّ يُزيحه فيُبطِل
    تصنيفًا صحيحًا، وتغييرُ رسالةٍ تغييرٌ في الرفض نفسه يستحقّ إعادةَ تصنيف.
    """

    function: str
    message: str

    def __post_init__(self) -> None:
        for field_name in ("function", "message"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise StateEvidenceError(f"{field_name} must be a non-empty string")


def _literal_message(node: ast.expr) -> str:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return " ".join(node.value.split())
    if isinstance(node, ast.JoinedStr):
        parts = [
            piece.value
            for piece in node.values
            if isinstance(piece, ast.Constant) and isinstance(piece.value, str)
        ]
        return " ".join("".join(parts).split())
    return " ".join(ast.unparse(node).split())


def derive_refusal_sites() -> tuple[RefusalSite, ...]:
    """اقرأ مواضعَ الرفض من شجرة نحو المولِّد المُودَع، ولا تكتبها يدًا."""
    tree = ast.parse(inspect.getsource(_deposited))
    enclosing: dict[ast.AST, str] = {}
    stack: list[tuple[ast.AST, str]] = [(tree, "<module>")]
    while stack:
        node, name = stack.pop()
        for child in ast.iter_child_nodes(node):
            child_name = (
                child.name
                if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
                else name
            )
            enclosing[child] = child_name
            stack.append((child, child_name))
    sites: set[RefusalSite] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Raise) or not isinstance(node.exc, ast.Call):
            continue
        called = node.exc.func
        raised = called.id if isinstance(called, ast.Name) else None
        if raised != CarrierStateEncodingError.__name__ or not node.exc.args:
            continue
        sites.add(
            RefusalSite(
                enclosing.get(node, "<module>"), _literal_message(node.exc.args[0])
            )
        )
    return tuple(sorted(sites))


_CONDITION_MESSAGES: Final[tuple[tuple[str, str], ...]] = (
    ("__post_init__", "a carrier is exactly one codepoint"),
    ("__post_init__", "a layer names itself and its claim"),
    ("__post_init__", "a layer order is a positive integer"),
    ("__post_init__", "a measurement over no token at all is not a measurement"),
    (
        "__post_init__",
        "a measurement that accepted no token at all is not a measurement; "
        "see REFUSAL_IS_NOT_A_ROUND_TRIP",
    ),
    ("__post_init__", "a mismatch total is a non-negative integer"),
    ("__post_init__", "a refusal total is a non-negative integer"),
    ("__post_init__", "a source byte length is a positive integer"),
    (
        "__post_init__",
        "a source sha256 is 64 characters; a partial digest re-derives no "
        "measurement",
    ),
    ("__post_init__", "a unit state is a CarrierState member"),
    (
        "__post_init__",
        "is outside DECLARED_CARRIERS, so it may only be carried as a "
        "passthrough unit",
    ),
    ("__post_init__", "must be a non-empty string"),
    ("_refuse_mismatched_seat", "a unit seat is a CarrierSeat member"),
    ("_refuse_unheld_flags", "a gemination role is a GeminationRole member"),
    ("generate", "a surface is a string"),
    ("retrieve", "every retrieved element is a CarrierStateUnit"),
)

_PREVENTER_MESSAGES: Final[tuple[tuple[str, str], ...]] = (
    ("__post_init__", "a dagger unit carries no structure"),
    (
        "__post_init__",
        "more mismatches than tokens is two contradictory claims in one " "measurement",
    ),
    (
        "__post_init__",
        "more refused and mismatched tokens than tokens is two contradictory "
        "claims in one measurement",
    ),
    ("_refuse_mismatched_seat", "seat is written on , not on"),
    ("_refuse_structure_on_a_bare_state", "a dagger unit is written on the alef"),
    (
        "_refuse_structure_on_a_bare_state",
        "a unit carries no seat, tanwin, gemination, or mark: a field written "
        "here would never be read back",
    ),
    ("_refuse_unheld_flags", "a tanwin holds fatha, damma, or kasra"),
    ("_refuse_unheld_flags", "an alef seat is consumed only by a fatha tanwin"),
    ("_refuse_unheld_flags", "an explicit madda is read on the waw only"),
    (
        "_refuse_unheld_flags",
        "the first half of a gemination pair carries no tanwin or mark",
    ),
    (
        "_refuse_unheld_flags",
        "the first half of a gemination pair holds sukun_implicit",
    ),
    (
        "retrieve",
        "a gemination pair start is not followed by its own carrier, so the "
        "pair cannot be written back",
    ),
)

_UNDECIDABLE_MESSAGES: Final[tuple[tuple[str, str], ...]] = (
    ("_read_marks", "a second shadda writes over a gemination already read in"),
    ("_read_marks", "a second vowel mark writes over a state already read in"),
)

REFUSAL_GENUS_REGISTRY: Final[Mapping[RefusalSite, RefusalGenus]] = {
    RefusalSite(function, message): genus
    for genus, group in (
        (RefusalGenus.CONDITION, _CONDITION_MESSAGES),
        (RefusalGenus.PREVENTER, _PREVENTER_MESSAGES),
        (RefusalGenus.UNDECIDABLE, _UNDECIDABLE_MESSAGES),
    )
    for function, message in group
}
"""جنسُ كلّ موضعِ رفضٍ قائمٍ في المولِّد المُودَع. تصنيفٌ لا تعديل."""


def derive_unclassified_refusal_sites() -> tuple[RefusalSite, ...]:
    """أيُّ مواضعِ الرفضِ القائمةِ بلا جنسٍ مُسمًّى؟ يُشتقّ ولا يُقال."""
    return tuple(
        site for site in derive_refusal_sites() if site not in REFUSAL_GENUS_REGISTRY
    )


def _derive_absent_classifications() -> tuple[RefusalSite, ...]:
    """أيُّ المُصنَّفاتِ لم يبقَ لها موضعٌ في المولِّد؟ تصنيفٌ لِما لا وجودَ له."""
    present = set(derive_refusal_sites())
    return tuple(sorted(site for site in REFUSAL_GENUS_REGISTRY if site not in present))


_UNCLASSIFIED: Final = derive_unclassified_refusal_sites()
if _UNCLASSIFIED:  # pragma: no cover - guard
    raise RuntimeError(
        "a refusal in carrier_state_candidate carries no named genus: "
        f"{[(site.function, site.message) for site in _UNCLASSIFIED]}"
    )

_ABSENT: Final = _derive_absent_classifications()
if _ABSENT:  # pragma: no cover - guard
    raise RuntimeError(
        "a classified refusal no longer exists in carrier_state_candidate: "
        f"{[(site.function, site.message) for site in _ABSENT]}"
    )


# --- العلامةُ المرصودة، مفصولةً عن الحالةِ المشتقّة ----------------------------

DECLARED_STATE_MARKS: Final[frozenset[str]] = frozenset(
    "\u064b\u064c\u064d"  # التنوين
    "\u064e\u064f\u0650"  # الحركات
    "\u0652"  # السكون
    "\u0670"  # الألف الخنجريّة
)
"""نقاطُ الترميزِ التي تحسم حالةَ الحامل، مُعلَنةٌ في هذه الوحدة لا مشتقّة.

الشدّةُ والمدّةُ والصفرُ المستدير خارجَ هذه المجموعة عمدًا: كلٌّ منها يكتب
بنيةً أخرى (تضعيفًا، أو مدًّا، أو سكوتًا)، ولا يحسم أيُّها حالةَ الحامل. فلو
عُدَّت علاماتِ حالةٍ لصارت الشدّةُ في «بّ» دليلًا على سكونٍ لم يكتبه أحد.
"""


@dataclass(frozen=True, order=True)
class MarkObservation:
    """علامةٌ رُصدت في سطحٍ بموضعها. لا تحمل حالةً ولا تدّعي اشتقاقَ واحدة."""

    offset: int
    codepoint: str

    def __post_init__(self) -> None:
        if not isinstance(self.offset, int) or isinstance(self.offset, bool):
            raise StateEvidenceError("an observation offset is an integer")
        if self.offset < 0:
            raise StateEvidenceError("an observation offset is not negative")
        if not isinstance(self.codepoint, str) or len(self.codepoint) != 1:
            raise StateEvidenceError("an observed mark is exactly one codepoint")
        if self.codepoint not in DECLARED_STATE_MARKS:
            raise StateEvidenceError(
                f"{self.codepoint!r} is outside DECLARED_STATE_MARKS, so it is "
                "not observed as a mark here"
            )

    @property
    def unicode_name(self) -> str:
        """اسمُ نقطة الترميز في قاعدة يونيكود، مقروءًا لا محفوظًا."""
        return unicodedata.name(self.codepoint, "")


def derive_mark_observations(surface: str) -> tuple[MarkObservation, ...]:
    """ارصد كلّ علامةٍ مكتوبةٍ في السطح بموضعها، بلا اشتقاقِ حالةٍ ولا رفض."""
    if not isinstance(surface, str):
        raise StateEvidenceError("a surface is a string")
    text = unicodedata.normalize(NORMALIZATION_FORM, surface)
    return tuple(
        MarkObservation(offset, char)
        for offset, char in enumerate(text)
        if char in DECLARED_STATE_MARKS
    )


# --- السببُ بمعناه الضيّق ------------------------------------------------------


class StateEvidence(Enum):
    """جنسُ ما تستند إليه حالةُ الحامل. مفردةٌ مغلقة، ثلاثةُ أعضاء."""

    WRITTEN_MARK = "written_mark"
    ABSENCE_ASSUMPTION = "absence_assumption"
    UNDECIDABLE = "undecidable"

    @property
    def arabic_name(self) -> str:
        """اسمُ الجنس بالعربية."""
        return _EVIDENCE_ARABIC_NAMES[self]

    @property
    def is_read_from_the_surface(self) -> bool:
        """أهذا جنسٌ قرأه السطحُ فعلًا، أم أنتجه المولِّدُ من غير علامة؟"""
        return self is StateEvidence.WRITTEN_MARK


_EVIDENCE_ARABIC_NAMES: Final[dict[StateEvidence, str]] = {
    StateEvidence.WRITTEN_MARK: "علامةٌ مكتوبة",
    StateEvidence.ABSENCE_ASSUMPTION: "افتراضٌ عند الغياب",
    StateEvidence.UNDECIDABLE: "متعذِّر",
}

if len(_EVIDENCE_ARABIC_NAMES) != len(StateEvidence):  # pragma: no cover - guard
    raise RuntimeError("every StateEvidence member carries an Arabic name")


@dataclass(frozen=True)
class EvidencedUnit:
    """وحدةُ حاملٍ وحالةٍ، ومعها جنسُ سببها والعلاماتُ التي قامت عليها.

    الوحدةُ المحمولة تبقى كما أخرجها المولِّدُ المُودَع، لا يُمسّ منها شيء؛
    وجنسُ السبب يُضاف من خارجها. ووحدةُ العبور (`PASSTHROUGH`) لا حالةَ حاملٍ
    لها أصلًا، فلا يُعلَّق بها سبب: `evidence is None` مقصورةٌ عليها. وقد تحمل
    علامةً يتيمةً كُتبت بلا حاملٍ قبلها، فتُحمَل ولا تشهد بشيء
    (`ORPHAN_MARKS_ARE_CARRIED_AND_EVIDENCE_NOTHING`).
    """

    unit: CarrierStateUnit
    evidence: StateEvidence | None
    marks: tuple[MarkObservation, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.unit, CarrierStateUnit):
            raise StateEvidenceError("an evidenced unit wraps a CarrierStateUnit")
        if not isinstance(self.marks, tuple) or any(
            not isinstance(mark, MarkObservation) for mark in self.marks
        ):
            raise StateEvidenceError("marks is a tuple of MarkObservation")
        if self.unit.state is CarrierState.PASSTHROUGH:
            if self.evidence is not None:
                raise StateEvidenceError(
                    "a passthrough unit holds no carrier state, so no state "
                    "evidence attaches to it"
                )
            return
        if not isinstance(self.evidence, StateEvidence):
            raise StateEvidenceError(
                "a carrier state is not generated without the genus of its "
                "sabab: evidence is a StateEvidence member"
            )
        self._refuse_marks_that_do_not_match_the_genus()

    def _refuse_marks_that_do_not_match_the_genus(self) -> None:
        if self.evidence is StateEvidence.WRITTEN_MARK and not self.marks:
            raise StateEvidenceError(
                "a written_mark evidence names no mark, which is the claim it "
                "exists to carry"
            )
        if self.evidence is not StateEvidence.WRITTEN_MARK and self.marks:
            raise StateEvidenceError(
                f"a {self.evidence.value if self.evidence else None} unit rests "
                "on no written mark, so it carries none"
            )


# --- القارئ: يشتقّ جنسَ السبب ولا يُعدِّل المولِّد ------------------------------

_WORD_INITIAL_UNDECIDABLE_CARRIERS: Final[frozenset[str]] = frozenset("\u0627")
"""الحاملُ الذي لا تحسم العلاماتُ حالتَه في أوّل الكلمة: الألفُ المجرّدة وحدها."""

DECLARED_JOINERS: Final[frozenset[str]] = frozenset(
    "\u0640"  # التطويل
    "\u200c"  # فاصلُ الوصل
    "\u200d"  # واصلُ الوصل
)
"""نقاطُ ترميزٍ تمرّ بين الحوامل ولا تفتح كلمةً جديدة، مُعلَنةٌ لا مشتقّة."""


@dataclass(frozen=True)
class EvidencingReader:
    """يُشغِّل المولِّدَ المُودَع كما هو، ثمّ يُلحِق بكلّ وحدةٍ جنسَ سببها."""

    codec: CarrierStateCodec = CarrierStateCodec()

    def read(self, surface: str) -> tuple[EvidencedUnit, ...]:
        """اقرأ سطحًا وحدات، مع جنسِ سببِ كلّ حالةٍ فيها.

        موضعُ كلّ علامةٍ يُشتقّ من المولِّد المُودَع نفسِه: يُكتب كلُّ سابقٍ
        مرّةً ومعه اللاحق، فيكون الفرقُ بين الكتابتين هو نصيبُ اللاحقِ من
        السطح بالضبط. ولا يُعاد هنا بناءُ قارئِ العلامات، فلا يفترق قارئان.

        والمكتوبُ يُوحَّد قبل الفرق: `retrieve` يكتب الشدّةَ قبل الحركة، وNFC
        يُقدِّم الحركةَ عليها، فلو قِيس الموضعُ على غير المُوحَّد لأشار إلى
        نقطةِ ترميزٍ غيرِ التي رُصدت. وأنّ المكتوبَ بادئةٌ من السطح يُختبَر لا
        يُفترَض، فإن تخلّف رُفِض ولم يُبلَّغ موضعٌ مظنون.
        """
        if not isinstance(surface, str):
            raise StateEvidenceError("a surface is a string")
        text = unicodedata.normalize(NORMALIZATION_FORM, surface)
        units = self.codec.generate(text)
        observations = derive_mark_observations(text)
        evidenced: list[EvidencedUnit] = []
        word_initial = True
        written_so_far = ""
        index = 0
        total = len(units)
        while index < total:
            # نصفا المشدَّد يُكتبان معًا، فلا يُفصَل أوّلُهما عن ثانيه.
            span = 2 if units[index].gemination is not None else 1
            written = unicodedata.normalize(
                NORMALIZATION_FORM, self.codec.retrieve(units[: index + span])
            )
            if not text.startswith(written):
                raise StateEvidenceError(
                    "the units written back so far are not a prefix of the "
                    f"surface they were read from ({text!r}), so no offset in "
                    "it can be reported"
                )
            segment = written[len(written_so_far) :]
            marks = tuple(
                MarkObservation(len(written_so_far) + offset, char)
                for offset, char in enumerate(segment)
                if char in DECLARED_STATE_MARKS
            )
            written_so_far = written
            for position, unit in enumerate(units[index : index + span]):
                # في المشدَّد لا يحمل النصفُ الأوّل علامةَ حالةٍ البتّة، لأنّ
                # بناءَ الوحدة يُلزمه السكونَ الضمنيَّ ويمنع عنه التنوين.
                held = marks if position == span - 1 else ()
                evidenced.append(
                    EvidencedUnit(
                        unit, self._evidence_for(unit, held, word_initial), held
                    )
                )
                word_initial = (
                    unit.state is CarrierState.PASSTHROUGH
                    and unit.carrier not in DECLARED_JOINERS
                )
            index += span
        self._refuse_a_lost_observation(observations, evidenced)
        return tuple(evidenced)

    @staticmethod
    def _evidence_for(
        unit: CarrierStateUnit,
        marks: tuple[MarkObservation, ...],
        word_initial: bool,
    ) -> StateEvidence | None:
        if unit.state is CarrierState.PASSTHROUGH:
            return None
        if marks:
            return StateEvidence.WRITTEN_MARK
        if word_initial and unit.carrier in _WORD_INITIAL_UNDECIDABLE_CARRIERS:
            return StateEvidence.UNDECIDABLE
        return StateEvidence.ABSENCE_ASSUMPTION

    @staticmethod
    def _refuse_a_lost_observation(
        observations: tuple[MarkObservation, ...],
        evidenced: list[EvidencedUnit],
    ) -> None:
        carried = sum(len(item.marks) for item in evidenced)
        if carried != len(observations):
            raise StateEvidenceError(
                f"{len(observations)} state marks were observed in the surface "
                f"and {carried} were carried by the units read from it, so a "
                "mark was observed and never attached"
            )


# --- القابليّةُ المرصودة -------------------------------------------------------


@dataclass(frozen=True)
class ObservedCapacityCensus:
    """أيُّ العلاماتِ وقعت فعلًا على أيّ الحوامل، في السطوح المقروءة وحدها."""

    surfaces_read: int
    observed: Mapping[str, frozenset[str]]

    def __post_init__(self) -> None:
        if not isinstance(self.surfaces_read, int) or isinstance(
            self.surfaces_read, bool
        ):
            raise StateEvidenceError("surfaces_read is an integer")
        if self.surfaces_read < 0:
            raise StateEvidenceError("surfaces_read is not negative")

    def unobserved_pairs(self) -> tuple[tuple[str, str], ...]:
        """الأزواجُ التي لم تُرصَد. غيرُ مرصودةٍ لا ممتنعة."""
        return tuple(
            sorted(
                (carrier, mark)
                for carrier in sorted(DECLARED_CARRIERS)
                for mark in sorted(DECLARED_STATE_MARKS)
                if mark not in self.observed.get(carrier, frozenset())
            )
        )


def derive_observed_capacities(surfaces: Iterable[str]) -> ObservedCapacityCensus:
    """اشتقّ القابليّةَ من الرصد وحده؛ لا يُقرأ هنا جدولٌ مكتوبٌ يدًا."""
    reader = EvidencingReader()
    observed: dict[str, set[str]] = {}
    count = 0
    for surface in surfaces:
        count += 1
        for item in reader.read(surface):
            for mark in item.marks:
                observed.setdefault(item.unit.carrier, set()).add(mark.codepoint)
    return ObservedCapacityCensus(
        count,
        {carrier: frozenset(marks) for carrier, marks in sorted(observed.items())},
    )
