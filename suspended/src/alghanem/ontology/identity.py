"""شبكةُ التسمية والهويّة: اللفظُ يُسمّي، والمعيارُ يُوحِّد، والرابطُ يُسحَب.

النواةُ القائمةُ فيها `Designation` من الخطاب و`resolve_reference` تُحاصِر
مرشَّحيها بشرط النوع. لكنّ `Designation` **تحمل قائمةَ مرشَّحيها معها**: فمن
كتبها كتب جوابَ التعيين فيها. وهذه الوحدةُ تسدّ ذلك: المرشَّحون يُشتقّون من
**تسمياتٍ مودَعةٍ بأدلّتها**، فإضافةُ شخصٍ أو مدينةٍ توسعةٌ في البيانات لا
تعديلٌ في المحرّك.

**أوّلًا: التسميةُ علاقةٌ لا هويّة.**
اسمٌ واحدٌ قد يُسمّي أفرادًا كُثُرًا، والفردُ قد يحمل أسماءً كُثُرًا. فتطابقُ
النصّ دليلُ ترشيحٍ لا إثباتُ تطابق؛ وعليه `candidates_for_surface` تُخرِج كلَّ
من سُمّي باللفظ ولا تختار منهم واحدًا بحال.

**ثانيًا: اسمُ العَلَم لا يُشتَقّ منه وصف.**
تسميةُ شخصٍ «صالحًا» تُودَع تسميةً، ولا تُولِّد قضيّةَ صفةٍ عن صلاحه. وليس
في هذه الوحدةِ طريقٌ من `Naming` إلى `Proposition`؛ وغيابُ الطريق هو المنع.

**ثالثًا: الرابطُ يحتاج مفتاحَين ومعيارًا مُعلَنًا.**
`IdentityLink` يُرفَض بناؤه ما لم تُوافق مفاتيحُه **كلَّ** مفاتيح المعيار
المُعلَن، وما لم يكن المعيارُ ذا مفتاحَين فأكثر. فكتابةُ «same» لا تُنشئ
رابطًا، ومفتاحٌ واحدٌ متوافقٌ ليس برهانًا.

**رابعًا: التعليقُ عند التعارض سياسةٌ تحفّظيّةٌ مُعلَنة.**
`ConflictPolicy` مفردةٌ مغلقةٌ فيها `SUSPEND_THE_COMPONENT` و
`SUSPEND_THE_CONTESTED_LINKS`؛ والأولى أوسعُ من اللزوم المنطقيّ، فتُسمّى
سياسةً ويُختبَر حدُّها. والدمجُ لا يمحو شيئًا: السجلّاتُ الأصليّةُ باقيةٌ
وكلُّ عمليّةٍ تُخرِج شبكةً جديدة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .epistemics import EvidenceRef, Scope
from .facts import FactRegister


class IdentityError(ValueError):
    """خطأٌ في شبكة التسمية والهويّة؛ صنفٌ مستقلٌّ لا يُلتبَس بغيره."""


A_NAME_IS_A_RELATION_NOT_AN_IDENTITY: Final[str] = (
    "التسميةُ تربط لفظًا بفرد؛ وتطابقُ اللفظين دليلُ ترشيحٍ لا إثباتُ تطابق، "
    "فاسمٌ واحدٌ يُسمّي أفرادًا واسمانِ يُسمّيان فردًا"
)

A_PROPER_NAME_CARRIES_NO_ATTRIBUTE: Final[str] = (
    "تسميةُ شخصٍ «صالحًا» تُودَع تسميةً ولا تُولِّد قضيّةَ صفةٍ عن صلاحه؛ "
    "ولا طريقَ ههنا من التسمية إلى الإسناد، وغيابُ الطريق هو المنع"
)

WRITING_SAME_IS_NOT_AN_IDENTITY_PROOF: Final[str] = (
    "رابطُ الهويّة يلزمه معيارٌ مُعلَنٌ ذو مفتاحَين فأكثر، وموافقةُ كلِّ "
    "مفاتيحه؛ فمفتاحٌ واحدٌ متوافقٌ ليس برهانًا عامًّا، وكتابةُ «same» ليست شيئًا"
)

A_MERGE_ERASES_NOTHING: Final[str] = (
    "الدمجُ لا يمحو السجلّات الأصليّة: الفردانِ باقيانِ بمُعرِّفيهما، والرابطُ "
    "طبقةٌ فوقهما تُسحَب فتعود القراءةُ إلى ما كانت"
)

SUSPENDING_A_COMPONENT_IS_A_POLICY: Final[str] = (
    "تعليقُ مكوّنِ هويّةٍ كاملٍ عند التعارض سياسةٌ تحفّظيّةٌ مُعلَنةٌ لا أثرٌ "
    "منطقيٌّ وحيد؛ ويُختبَر حدُّها بأنّها تُعلّق روابطَ لا تعارضَ فيها"
)

A_CRITERION_NAMES_ITS_AUTHORITY: Final[str] = (
    "معيارُ الهويّة يُسمّي مفاتيحَه ومجالَه وزمنَه وسلطةَ مصدره؛ ومعيارٌ بلا "
    "سلطةٍ مُسمّاةٍ لا يُبنى"
)


class NamingGenus(Enum):
    """جنسُ التسمية؛ مفردةٌ مغلقةٌ فيها عضوُ جهلٍ مُصرَّحٌ به."""

    PROPER_NAME = "proper_name"
    BYNAME = "byname"
    TOPONYM = "toponym"
    FORMER_NAME = "former_name"
    TRANSLITERATION = "transliteration"
    UNREAD = "unread"


class NamedKind(Enum):
    """المُسمّى: أفردٌ هو أم مفهوم؟ فصلٌ يمنع قراءةَ النوع فردًا."""

    INDIVIDUAL = "individual"
    CONCEPT = "concept"


class ConflictPolicy(Enum):
    """سياسةُ التعارض؛ مفردةٌ مغلقةٌ لا تُقرَأ إحداها لزومًا منطقيًّا."""

    SUSPEND_THE_CONTESTED_LINKS = "suspend_the_contested_links"
    SUSPEND_THE_COMPONENT = "suspend_the_component"


class KeyAgreementStanding(Enum):
    """منزلةُ مفتاحٍ في المقابلة؛ والسكوتُ منزلةٌ ثالثةٌ لا تُقرَأ خلافًا."""

    AGREES = "agrees"
    DIFFERS = "differs"
    NOT_RECORDED = "not_recorded"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise IdentityError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class Naming:
    """تسميةٌ واحدة: لفظٌ، ومُسمًّى، ولغةٌ، وجنسٌ، ونطاقٌ، ودليل.

    والمُسمّى مُعرِّفٌ ومنزلةٌ (فردٌ أو مفهوم) معًا؛ فلا يُقرَأ اسمُ نوعٍ فردًا
    ولا عكسُه. والنطاقُ يحمل زمنَ التسمية إن كانت مؤقّتةً (كاسمٍ سابقٍ لمدينة).
    """

    naming_id: str
    surface: str
    named_id: str
    named_kind: NamedKind
    genus: NamingGenus
    language_id: str
    scope: Scope
    evidence_ref: EvidenceRef
    context_note: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.naming_id, "مُعرِّفُ التسمية")
        _require_text(self.surface, "لفظُ التسمية")
        _require_text(self.named_id, "مُعرِّفُ المُسمّى")
        if not isinstance(self.named_kind, NamedKind):
            raise IdentityError("منزلةُ المُسمّى عضوٌ في مفردتها المغلقة")
        if not isinstance(self.genus, NamingGenus):
            raise IdentityError("جنسُ التسمية عضوٌ في مفردته المغلقة")
        _require_text(self.language_id, "لغةُ التسمية")
        if not isinstance(self.scope, Scope):
            raise IdentityError("نطاقُ التسمية نطاقٌ قائم")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise IdentityError(
                "التسميةُ بدليلٍ مُشارٍ إليه؛ و" + A_NAME_IS_A_RELATION_NOT_AN_IDENTITY
            )
        if self.context_note is not None:
            _require_text(self.context_note, "سياقُ التسمية إن ذُكر")

    @property
    def names_an_individual(self) -> bool:
        """أتُسمّي فردًا؟ خاصّيّةٌ تُشتَقّ من منزلة المُسمّى لا حقلٌ يُكتَب."""

        return self.named_kind is NamedKind.INDIVIDUAL

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التسمية للبصمة."""

        return {
            "naming_id": self.naming_id,
            "surface": self.surface,
            "named_id": self.named_id,
            "named_kind": self.named_kind.value,
            "genus": self.genus.value,
            "language_id": self.language_id,
            "scope": self.scope.as_canonical_content(),
            "evidence_ref": self.evidence_ref.as_canonical_content(),
            "context_note": self.context_note,
        }


@dataclass(frozen=True, slots=True)
class IdentityCriterion:
    """معيارُ هويّةٍ مُعلَن: مفاتيحُه، ومجالُه، وزمنُه، وسلطةُ مصدره.

    ويُرفَض معيارٌ بمفتاحٍ واحد: فالتوافقُ في مفتاحٍ وحدَه لا يُوحِّد فردَين،
    وهو عينُ ما يُفرِّق بين الترشيح والبرهان.
    """

    criterion_id: str
    key_names: tuple[str, ...]
    scope: Scope
    authority: str

    def __post_init__(self) -> None:
        _require_text(self.criterion_id, "مُعرِّفُ المعيار")
        if not isinstance(self.key_names, tuple) or len(self.key_names) < 2:
            raise IdentityError(
                "مفاتيحُ المعيار صفٌّ مجمَّدٌ فيه مفتاحانِ فأكثر؛ و"
                + WRITING_SAME_IS_NOT_AN_IDENTITY_PROOF
            )
        if len(set(self.key_names)) != len(self.key_names):
            raise IdentityError("مفتاحٌ مكرَّرٌ في المعيار يُرفَض لا يُطوى")
        for key in self.key_names:
            _require_text(key, "اسمُ المفتاح")
        if not isinstance(self.scope, Scope):
            raise IdentityError("نطاقُ المعيار نطاقٌ قائم")
        _require_text(
            self.authority, "سلطةُ المعيار؛ و" + A_CRITERION_NAMES_ITS_AUTHORITY
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المعيار للبصمة."""

        return {
            "criterion_id": self.criterion_id,
            "key_names": list(self.key_names),
            "scope": self.scope.as_canonical_content(),
            "authority": self.authority,
        }


@dataclass(frozen=True, slots=True)
class KeyReading:
    """قراءةُ مفتاحٍ على طرفَي الرابط: منزلتُها مُشتقّةٌ من القيمتين لا مكتوبة."""

    key_name: str
    left_value: str | None
    right_value: str | None

    def __post_init__(self) -> None:
        _require_text(self.key_name, "اسمُ المفتاح المقروء")
        for value, label in (
            (self.left_value, "الطرف الأوّل"),
            (self.right_value, "الطرف الثاني"),
        ):
            if value is not None:
                _require_text(value, f"قيمةُ المفتاح عند {label} إن ذُكرت")

    @property
    def standing(self) -> KeyAgreementStanding:
        """أتوافقا؟ والسكوتُ منزلةٌ ثالثةٌ لا تُقرَأ خلافًا ولا وفاقًا."""

        if self.left_value is None or self.right_value is None:
            return KeyAgreementStanding.NOT_RECORDED
        if self.left_value == self.right_value:
            return KeyAgreementStanding.AGREES
        return KeyAgreementStanding.DIFFERS

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القراءة للبصمة."""

        return {
            "key_name": self.key_name,
            "left_value": self.left_value,
            "right_value": self.right_value,
            "standing": self.standing.value,
        }


@dataclass(frozen=True, slots=True)
class IdentityLink:
    """رابطُ هويّةٍ بين فردَين: معيارُه، وقراءاتُ مفاتيحه، ودليلُه.

    ويُرفَض بناؤه ما لم تُقرأ **كلُّ** مفاتيح المعيار وتوافق جميعُها؛ فلا رابطَ
    بمفتاحٍ ناقصٍ ولا بمفتاحٍ ساكت. والسحبُ `retracted` لا يحذف الرابط بل
    يُعطِّله، فيبقى أثرُه في السجلّ كما كان.
    """

    link_id: str
    left_individual_id: str
    right_individual_id: str
    criterion_id: str
    key_readings: tuple[KeyReading, ...]
    evidence_ref: EvidenceRef
    retracted: bool = False

    def __post_init__(self) -> None:
        _require_text(self.link_id, "مُعرِّفُ الرابط")
        _require_text(self.left_individual_id, "الطرفُ الأوّل")
        _require_text(self.right_individual_id, "الطرفُ الثاني")
        if self.left_individual_id == self.right_individual_id:
            raise IdentityError("رابطُ هويّةٍ بين فردٍ ونفسِه لا يُفيد شيئًا")
        _require_text(self.criterion_id, "مُعرِّفُ معيار الرابط")
        if not isinstance(self.key_readings, tuple) or not self.key_readings:
            raise IdentityError(
                "قراءاتُ المفاتيح صفٌّ مجمَّدٌ غيرُ فارغ؛ و"
                + WRITING_SAME_IS_NOT_AN_IDENTITY_PROOF
            )
        names = tuple(reading.key_name for reading in self.key_readings)
        if len(set(names)) != len(names):
            raise IdentityError("مفتاحٌ مقروءٌ مرّتين في رابطٍ واحدٍ يُرفَض لا يُطوى")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise IdentityError("رابطُ الهويّة بدليلٍ مُشارٍ إليه")
        if not isinstance(self.retracted, bool):
            raise IdentityError("سحبُ الرابط قيمةٌ ثنائيّة")

    @property
    def agreeing_key_names(self) -> tuple[str, ...]:
        """المفاتيحُ الموافقةُ وحدَها؛ والساكتُ ليس منها."""

        return tuple(
            reading.key_name
            for reading in self.key_readings
            if reading.standing is KeyAgreementStanding.AGREES
        )

    @property
    def differing_key_names(self) -> tuple[str, ...]:
        """المفاتيحُ المختلفةُ؛ وواحدٌ منها يكفي لنقض الرابط."""

        return tuple(
            reading.key_name
            for reading in self.key_readings
            if reading.standing is KeyAgreementStanding.DIFFERS
        )

    @property
    def is_live(self) -> bool:
        """أما زال نافذًا؟ خاصّيّةٌ تُشتَقّ من السحب لا حقلٌ ثانٍ يُكتَب."""

        return not self.retracted

    def endpoints(self) -> frozenset[str]:
        """طرفا الرابط مجموعةً؛ الاتّجاهُ لا يُفيد ههنا."""

        return frozenset((self.left_individual_id, self.right_individual_id))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الرابط للبصمة."""

        return {
            "link_id": self.link_id,
            "left_individual_id": self.left_individual_id,
            "right_individual_id": self.right_individual_id,
            "criterion_id": self.criterion_id,
            "key_readings": [
                reading.as_canonical_content() for reading in self.key_readings
            ],
            "evidence_ref": self.evidence_ref.as_canonical_content(),
            "retracted": self.retracted,
        }


@dataclass(frozen=True, slots=True)
class NamingCandidate:
    """مرشَّحٌ مُشتَقٌّ من تسمية: الفردُ، والتسميةُ التي رشّحته، وسببُ الترشيح."""

    individual_id: str
    naming_id: str
    reason: str

    def __post_init__(self) -> None:
        _require_text(self.individual_id, "مُعرِّفُ الفرد المرشَّح")
        _require_text(self.naming_id, "مُعرِّفُ التسمية المُرشِّحة")
        _require_text(self.reason, "سببُ الترشيح")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرشَّح للبصمة."""

        return {
            "individual_id": self.individual_id,
            "naming_id": self.naming_id,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class IdentityNetwork:
    """شبكةُ التسمية والهويّة فوق سجلّ الوقائع؛ مجمَّدةٌ وكلُّ عمليّةٍ تُخرِج أخرى.

    وهي **لا تملك** الأفراد ولا الأدلّة: تلك في `FactRegister`. ومهمّتُها
    ثلاثٌ: اشتقاقُ المرشَّحين من التسميات، وحفظُ المعايير والروابط، وسحبُ
    الرابط دون محوِ شيء.
    """

    network_id: str
    namings: tuple[Naming, ...] = ()
    criteria: tuple[IdentityCriterion, ...] = ()
    links: tuple[IdentityLink, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.network_id, "مُعرِّفُ الشبكة")
        for group, label, attribute in (
            (self.namings, "التسميات", "naming_id"),
            (self.criteria, "المعايير", "criterion_id"),
            (self.links, "الروابط", "link_id"),
        ):
            ids = tuple(getattr(item, attribute) for item in group)
            if len(set(ids)) != len(ids):
                raise IdentityError(f"مُعرِّفٌ مكرَّرٌ في {label} يُرفَض لا يُطوى")

    # ----- قراءةٌ -----

    def naming_of(self, naming_id: str) -> Naming:
        """التسميةُ بمُعرِّفها؛ والغيابُ رفضٌ مُسمًّى."""

        for item in self.namings:
            if item.naming_id == naming_id:
                return item
        raise IdentityError(f"لا تسميةَ في الشبكة مُعرِّفُها `{naming_id}`")

    def criterion_of(self, criterion_id: str) -> IdentityCriterion:
        """المعيارُ بمُعرِّفه؛ والغيابُ رفضٌ مُسمًّى."""

        for item in self.criteria:
            if item.criterion_id == criterion_id:
                return item
        raise IdentityError(f"لا معيارَ في الشبكة مُعرِّفُه `{criterion_id}`")

    def link_of(self, link_id: str) -> IdentityLink:
        """الرابطُ بمُعرِّفه؛ والغيابُ رفضٌ مُسمًّى."""

        for item in self.links:
            if item.link_id == link_id:
                return item
        raise IdentityError(f"لا رابطَ في الشبكة مُعرِّفُه `{link_id}`")

    @property
    def live_links(self) -> tuple[IdentityLink, ...]:
        """الروابطُ النافذة؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(item for item in self.links if item.is_live)

    def namings_of_individual(self, individual_id: str) -> tuple[Naming, ...]:
        """كلُّ أسماء فردٍ واحد؛ فالفردُ يحمل أسماءً، وهذا وجهُ العلاقة الثاني."""

        return tuple(
            item
            for item in self.namings
            if item.names_an_individual and item.named_id == individual_id
        )

    # ----- إيداعٌ -----

    def with_naming(self, naming: Naming, register: FactRegister) -> IdentityNetwork:
        """أودِع تسميةً؛ ومُسمّاها الفردُ يلزمه أن يكون مودَعًا في السجلّ.

        وإيداعُ التسميةِ **لا** يُثبِت وجودَ المُسمّى ولا يُولِّد عنه قضيّة:
        فتسميةُ شخصٍ «صالحًا» تُودَع تسميةً ولا تُنشئ صفةً عن صلاحه.
        """

        if not isinstance(naming, Naming):
            raise IdentityError("المُودَعُ تسميةٌ قائمة")
        if not isinstance(register, FactRegister):
            raise IdentityError("التسميةُ تُقابَل بسجلّ وقائعَ قائم")
        if naming.names_an_individual:
            register.individual_of(naming.named_id)
        for item in self.namings:
            if item.naming_id == naming.naming_id:
                raise IdentityError("تسميةٌ بمُعرِّفٍ قائم؛ ولا استبدالَ صامت")
        return replace(self, namings=(*self.namings, naming))

    def with_criterion(self, criterion: IdentityCriterion) -> IdentityNetwork:
        """أودِع معيارَ هويّةٍ مُعلَنًا."""

        if not isinstance(criterion, IdentityCriterion):
            raise IdentityError("المُودَعُ معيارٌ قائم")
        for item in self.criteria:
            if item.criterion_id == criterion.criterion_id:
                raise IdentityError("معيارٌ بمُعرِّفٍ قائم؛ ولا استبدالَ صامت")
        return replace(self, criteria=(*self.criteria, criterion))

    def with_link(self, link: IdentityLink, register: FactRegister) -> IdentityNetwork:
        """أودِع رابطَ هويّةٍ بعد فحص معياره ومفاتيحه وطرفَيه.

        ثلاثةُ شروطٍ تُفحَص ههنا ولا يُقبَل الرابطُ بأقلّ منها: الطرفانِ
        مودَعانِ في السجلّ، والمعيارُ مودَعٌ في الشبكة، وكلُّ مفتاحٍ من مفاتيح
        المعيار **مقروءٌ وموافق**. فمفتاحٌ ساكتٌ أو ناقصٌ يردّ الرابط.
        """

        if not isinstance(link, IdentityLink):
            raise IdentityError("المُودَعُ رابطٌ قائم")
        if not isinstance(register, FactRegister):
            raise IdentityError("الرابطُ يُقابَل بسجلّ وقائعَ قائم")
        register.individual_of(link.left_individual_id)
        register.individual_of(link.right_individual_id)
        criterion = self.criterion_of(link.criterion_id)
        agreeing = set(link.agreeing_key_names)
        missing = tuple(key for key in criterion.key_names if key not in agreeing)
        if missing:
            raise IdentityError(
                "رابطٌ لا تُوافق مفاتيحُه كلَّ مفاتيح معياره؛ والناقصُ: "
                + "، ".join(missing)
                + "؛ و"
                + WRITING_SAME_IS_NOT_AN_IDENTITY_PROOF
            )
        for item in self.links:
            if item.link_id == link.link_id:
                raise IdentityError("رابطٌ بمُعرِّفٍ قائم؛ ولا استبدالَ صامت")
        return replace(self, links=(*self.links, link))

    # ----- السحبُ والتعارض -----

    def amend_link_readings(
        self,
        link_id: str,
        key_readings: tuple[KeyReading, ...],
        evidence_ref: EvidenceRef,
    ) -> IdentityNetwork:
        """أعِد قراءةَ مفاتيح رابطٍ قائمٍ بدليلٍ جديد؛ وقد تصير مختلفة.

        وهذا هو الطريقُ الوحيدُ إلى التعارض: الرابطُ **لا يُودَع** مختلفَ
        المفاتيح، وإنّما يُودَع موافقًا ثمّ يأتي خبرٌ معارضٌ فيُعاد قراءةُ
        مفاتيحه. فالتعارضُ حادثٌ في الأدلّة لا حالٌ تُكتَب ابتداءً.
        """

        link = self.link_of(link_id)
        if not isinstance(evidence_ref, EvidenceRef):
            raise IdentityError("إعادةُ القراءة بدليلٍ مُشارٍ إليه")
        if evidence_ref == link.evidence_ref:
            raise IdentityError("إعادةُ قراءةٍ بالدليل نفسِه ليست قراءةً ثانية")
        amended = replace(link, key_readings=key_readings, evidence_ref=evidence_ref)
        updated = tuple(
            amended if item.link_id == link_id else item for item in self.links
        )
        return replace(self, links=updated)

    def retract_link(self, link_id: str) -> IdentityNetwork:
        """اسحب رابطًا: يُعطَّل ولا يُحذَف، والسجلّاتُ الأصليّةُ لا تُمَسّ.

        والفردانِ باقيانِ بمُعرِّفيهما، والرابطُ طبقةٌ فوقهما تُسحَب فتعود
        القراءةُ إلى ما كانت.
        """

        link = self.link_of(link_id)
        if link.retracted:
            raise IdentityError("رابطٌ مسحوبٌ لا يُسحَب مرّتين")
        updated = tuple(
            replace(item, retracted=True) if item.link_id == link_id else item
            for item in self.links
        )
        return replace(self, links=updated)

    def apply_conflict_policy(
        self, policy: ConflictPolicy
    ) -> tuple[IdentityNetwork, tuple[str, ...]]:
        """طبِّق سياسةَ التعارض وأخرِج الشبكةَ الجديدةَ وأسماءَ ما عُلِّق.

        و`SUSPEND_THE_CONTESTED_LINKS` تُعلّق الروابطَ التي فيها مفتاحٌ مختلفٌ
        وحدَها؛ و`SUSPEND_THE_COMPONENT` تُعلّق كلَّ روابط المكوّن المتّصل الذي
        وقع فيه التعارض — وهي أوسعُ من اللزوم المنطقيّ، فتُسمّى سياسةً ولا
        تُقدَّم أثرًا وحيدًا.
        """

        if not isinstance(policy, ConflictPolicy):
            raise IdentityError("سياسةُ التعارض عضوٌ في مفردتها المغلقة")
        contested = tuple(item for item in self.live_links if item.differing_key_names)
        if not contested:
            return self, ()
        if policy is ConflictPolicy.SUSPEND_THE_CONTESTED_LINKS:
            targets = {item.link_id for item in contested}
        else:
            component = set[str]()
            for item in contested:
                component |= item.endpoints()
            changed = True
            while changed:
                changed = False
                for item in self.live_links:
                    if item.endpoints() & component and not (
                        item.endpoints() <= component
                    ):
                        component |= item.endpoints()
                        changed = True
            targets = {
                item.link_id for item in self.live_links if item.endpoints() & component
            }
        updated = tuple(
            replace(item, retracted=True) if item.link_id in targets else item
            for item in self.links
        )
        return replace(self, links=updated), tuple(sorted(targets))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشبكة للبصمة."""

        return {
            "network_id": self.network_id,
            "namings": [
                item.as_canonical_content()
                for item in sorted(self.namings, key=lambda item: item.naming_id)
            ],
            "criteria": [
                item.as_canonical_content()
                for item in sorted(self.criteria, key=lambda item: item.criterion_id)
            ],
            "links": [
                item.as_canonical_content()
                for item in sorted(self.links, key=lambda item: item.link_id)
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الشبكة؛ وكلُّ إيداعٍ أو سحبٍ يُخرِج بصمةً أخرى."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def candidates_for_surface(
    surface: str,
    network: IdentityNetwork,
    register: FactRegister,
    language_id: str | None = None,
) -> tuple[NamingCandidate, ...]:
    """اشتقّ مرشَّحي الإحالة من التسميات المودَعة، لا من قائمةٍ مُمرَّرةٍ معك.

    المدخل: لفظٌ، وشبكةُ تسمياتٍ، وسجلُّ أفراد.
    الشرط: كلُّ مرشَّحٍ مُسمًّى بتسميةٍ مودَعةٍ ومودَعٌ فردًا في السجلّ.
    المخرج: مرشَّحون بأسباب ترشيحهم مرتّبين بمُعرِّفاتهم.
    ما تحفظه: لا تختار واحدًا من متعدّد، ولا تُنشئ فردًا، ولا تُثبِت وجودًا.
    """

    _require_text(surface, "اللفظُ المطلوب")
    if not isinstance(network, IdentityNetwork):
        raise IdentityError("المرشَّحون يُشتقّون من شبكةٍ قائمة")
    if not isinstance(register, FactRegister):
        raise IdentityError("المرشَّحون يُقابَلون بسجلّ وقائعَ قائم")
    found: list[NamingCandidate] = []
    for naming in network.namings:
        if naming.surface != surface or not naming.names_an_individual:
            continue
        if language_id is not None and naming.language_id != language_id:
            continue
        register.individual_of(naming.named_id)
        found.append(
            NamingCandidate(
                individual_id=naming.named_id,
                naming_id=naming.naming_id,
                reason=(
                    f"تسميةٌ مودَعةٌ من جنس `{naming.genus.value}` تربط اللفظَ "
                    f"`{surface}` بهذا الفرد؛ و" + A_NAME_IS_A_RELATION_NOT_AN_IDENTITY
                ),
            )
        )
    return tuple(sorted(found, key=lambda item: (item.individual_id, item.naming_id)))


def linked_individual_ids(
    individual_id: str, network: IdentityNetwork
) -> tuple[str, ...]:
    """المُعرِّفاتُ الموحَّدةُ مع هذا الفرد **بروابطَ نافذةٍ وحدَها**.

    والسحبُ يُخرِج الطرفَ من هذه القائمةِ فورًا؛ فهي مُشتقّةٌ لا مخزونة.
    """

    _require_text(individual_id, "مُعرِّفُ الفرد")
    if not isinstance(network, IdentityNetwork):
        raise IdentityError("التوحيدُ يُقرَأ من شبكةٍ قائمة")
    reached = {individual_id}
    changed = True
    while changed:
        changed = False
        for link in network.live_links:
            endpoints = link.endpoints()
            if endpoints & reached and not endpoints <= reached:
                reached |= endpoints
                changed = True
    return tuple(sorted(reached - {individual_id}))
