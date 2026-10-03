"""سجلُّ القضايا المقبولة عن الواقع، وسياسةُ أدلّته، والأفرادُ وهويّاتُهم.

هذا **المستوى الثالث**. وما يدخله يحتاج دليلًا من جنسٍ يُثبِت
(`EvidenceGenus.is_fact_establishing`): مشاهدةً أو قياسًا أو خبرًا معتمدًا أو
استنتاجًا مُرخَّصًا. والتعريفُ الاصطلاحيُّ والفرضيّةُ المُعلَنةُ يُحفَظان
بصفتهما في الرصيد ولا يدخلان ههنا.

**والانتقالُ من المضمون إلى الواقعة منفَّذٌ ومشروط** (`deposit_from_discourse`):

* مضمونٌ شرطيٌّ أو استفهاميٌّ لا يُودَع البتّة؛ فكُّ المضمون من شرطه بلا
  ترخيصٍ هو عينُ الممنوع (`A_CONDITIONAL_IS_NOT_UNBOUND_BY_DEPOSIT`).
* مضمونٌ منفيٌّ يُودَع **منفيًّا بدليله**، ولا ينقلب موجبًا
  (`A_NEGATED_CONTENT_NEVER_BECOMES_AN_AFFIRMED_FACT`).
* ذِكرُ اسمٍ لا يُنشئ فردًا: الأفرادُ يُودَعون بأدلّتهم، ومضمونٌ يُحيل إلى
  فردٍ غيرِ مودَعٍ يُرفَض (`A_MENTION_IS_NOT_AN_EXISTENCE_CLAIM`).

**وحالُ الوجود منزلةٌ مُسمّاة**: فردٌ قد يكون مُثبَتًا، أو مُفترَضًا للخطاب،
أو مرشَّحَ إحالةٍ لا غير. ومعرفةُ نوعِه لا تُثبِت وجودَه، ووجودُه لا يُثبِت
وقوعَ حدثٍ له (`A_KIND_IS_NOT_AN_OCCURRENCE`).

**وإبطالُ دليلٍ يُسقِط ما استند إليه وحدَه** (`retract`): القضايا المرتبطةُ
بدليلٍ أُبطِل تُعلَّق، وغيرُها لا يُمَسّ.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .content import (
    A_MENTION_IS_NOT_AN_EXISTENCE_CLAIM,
    DesignationMethod,
    DiscourseContent,
    FillerStanding,
    Modality,
    NegationScope,
    Polarity,
)
from .epistemics import Evidence, EvidenceRef, Scope

__all__ = [
    "A_CONDITIONAL_IS_NOT_UNBOUND_BY_DEPOSIT",
    "A_KIND_IS_NOT_AN_OCCURRENCE",
    "A_NEGATED_CONTENT_NEVER_BECOMES_AN_AFFIRMED_FACT",
    "ONLY_A_FACT_ESTABLISHING_GENUS_DEPOSITS",
    "ExistenceStanding",
    "FactError",
    "FactRegister",
    "Individual",
    "Proposition",
    "PropositionForm",
]


class FactError(ValueError):
    """رفضٌ بنيويٌّ في سجلّ الوقائع؛ لا حملَ على أقرب حالة."""


ONLY_A_FACT_ESTABLISHING_GENUS_DEPOSITS: Final[str] = (
    "لا تُودَع واقعةٌ إلّا بدليلٍ من جنسٍ يُثبِت: التعريفُ الاصطلاحيُّ "
    "والفرضيّةُ المُعلَنةُ والشهادةُ المعجميّةُ تُؤسِّس رصيدًا ولا تُثبِت وقوعًا"
)

A_NEGATED_CONTENT_NEVER_BECOMES_AN_AFFIRMED_FACT: Final[str] = (
    "المنفيُّ لا ينقلب موجبًا بالإيداع: يُسجَّل منفيًّا بدليله ونطاقِه، ومن "
    "أودعه موجبًا أنشأ عن الواقع خبرًا لم يقله أحد"
)

A_CONDITIONAL_IS_NOT_UNBOUND_BY_DEPOSIT: Final[str] = (
    "الشرطيُّ لا يُفَكّ من شرطه بالإيداع: مضمونٌ لا يلتزم قائلُه بوقوعه لا "
    "يصير واقعةً لأنّه مفهوم"
)

A_KIND_IS_NOT_AN_OCCURRENCE: Final[str] = (
    "معرفةُ النوع ليست إثباتًا لوقوع حدثٍ لفرده: أن تعرف أنّ البابَ يُفتَح "
    "ويُغلَق شيءٌ، وأن تُثبِت أنّ هذا البابَ فُتِح شيءٌ آخر"
)


class ExistenceStanding(Enum):
    """حالُ إثبات وجود الفرد؛ مفردةٌ مغلقةٌ لا تُقرَأ إحداها مكان الأخرى."""

    ESTABLISHED = "established"
    ASSUMED_FOR_THE_DISCOURSE = "assumed_for_the_discourse"
    CANDIDATE_ONLY = "candidate_only"

    @property
    def is_established(self) -> bool:
        """أمُثبَتٌ وجودُه؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self is ExistenceStanding.ESTABLISHED


class PropositionForm(Enum):
    """صورةُ القضيّة؛ خمسٌ مغلقةٌ لكلٍّ أطرافُها المعلومة."""

    TYPE_MEMBERSHIP = "type_membership"
    ATTRIBUTE_VALUE = "attribute_value"
    STATE_HOLDS = "state_holds"
    RELATION_HOLDS = "relation_holds"
    EVENT_OCCURRED = "event_occurred"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FactError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class Individual:
    """فردٌ واحد: هويّتُه، وطريقةُ تعيينه، ونوعُه المرشَّح، وحالُ إثبات وجوده."""

    individual_id: str
    designation_method: DesignationMethod
    candidate_type_ids: tuple[str, ...]
    existence: ExistenceStanding
    evidence_ref: EvidenceRef | None = None

    def __post_init__(self) -> None:
        _require_text(self.individual_id, "مُعرِّفُ الفرد")
        if not isinstance(self.designation_method, DesignationMethod):
            raise FactError("طريقةُ تعيين الفرد عضوٌ في مفردتها المغلقة")
        if not isinstance(self.candidate_type_ids, tuple):
            raise FactError("أنواعُ الفرد المرشَّحة صفٌّ مجمَّد")
        if not isinstance(self.existence, ExistenceStanding):
            raise FactError("حالُ وجود الفرد عضوٌ في مفردتها المغلقة")
        if self.existence.is_established and not isinstance(
            self.evidence_ref, EvidenceRef
        ):
            raise FactError(
                "فردٌ مُثبَتُ الوجود بلا دليلٍ مُشارٍ إليه؛ و"
                + A_MENTION_IS_NOT_AN_EXISTENCE_CLAIM
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفرد للبصمة."""

        return {
            "individual_id": self.individual_id,
            "designation_method": self.designation_method.value,
            "candidate_type_ids": list(self.candidate_type_ids),
            "existence": self.existence.value,
            "evidence_ref": (
                None
                if self.evidence_ref is None
                else self.evidence_ref.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class Proposition:
    """قضيّةٌ مقبولة: صورتُها، وأطرافُها، وقطبيّتُها، ونطاقُها، ودليلُها.

    و`derived_from` تُسمّي ما استُنتِجت منه إن كانت مُستنتَجة: مُعرِّفاتُ
    قضايا ومُعرِّفُ قاعدةٍ بإصدارها؛ فالحكمُ يحمل سندَه ولا يُفصَل عنه.
    """

    proposition_id: str
    form: PropositionForm
    subject_id: str
    predicate_id: str
    value: str | None
    polarity: Polarity
    scope: Scope
    evidence_ref: EvidenceRef
    derived_from_proposition_ids: tuple[str, ...] = ()
    derived_by_rule: str | None = None
    suspended: bool = False

    def __post_init__(self) -> None:
        _require_text(self.proposition_id, "مُعرِّفُ القضيّة")
        if not isinstance(self.form, PropositionForm):
            raise FactError("صورةُ القضيّة عضوٌ في مفردتها المغلقة")
        _require_text(self.subject_id, "موضوعُ القضيّة")
        _require_text(self.predicate_id, "محمولُ القضيّة")
        if self.form in (
            PropositionForm.ATTRIBUTE_VALUE,
            PropositionForm.STATE_HOLDS,
        ):
            _require_text(self.value, "قيمةُ المحمول في هذه الصورة")
        if not isinstance(self.polarity, Polarity):
            raise FactError("قطبيّةُ القضيّة عضوٌ في مفردتها المغلقة")
        if not isinstance(self.scope, Scope):
            raise FactError("نطاقُ القضيّة نطاقٌ قائم")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise FactError("دليلُ القضيّة إشارةٌ مبصومة")
        if bool(self.derived_from_proposition_ids) != bool(self.derived_by_rule):
            raise FactError(
                "القضيّةُ المُستنتَجةُ تُسمّي مقدّماتِها وقاعدتَها معًا؛ ونصفُ " "سندٍ سندٌ لا يُراجَع"
            )
        if not isinstance(self.suspended, bool):
            raise FactError("تعليقُ القضيّة قيمةٌ ثنائيّة")

    @property
    def is_derived(self) -> bool:
        """أمُستنتَجةٌ هي؟ خاصّيّةٌ تُشتَقّ من حاملها لا حقلٌ يُكتَب."""

        return self.derived_by_rule is not None

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القضيّة للبصمة."""

        return {
            "proposition_id": self.proposition_id,
            "form": self.form.value,
            "subject_id": self.subject_id,
            "predicate_id": self.predicate_id,
            "value": self.value,
            "polarity": self.polarity.value,
            "scope": self.scope.as_canonical_content(),
            "evidence_ref": self.evidence_ref.as_canonical_content(),
            "derived_from_proposition_ids": list(self.derived_from_proposition_ids),
            "derived_by_rule": self.derived_by_rule,
            "suspended": self.suspended,
        }


@dataclass(frozen=True, slots=True)
class FactRegister:
    """سجلُّ الوقائع: أفرادٌ وقضايا وأدلّة، وعمليّاتُه تُخرِج سجلًّا جديدًا.

    السجلُّ مجمَّدٌ والعمليّاتُ **لا تُعدِّله موضعيًّا**: كلُّ إيداعٍ أو إبطالٍ
    يُخرِج سجلًّا جديدًا ببصمةٍ جديدة، فتبقى الحالُ السابقةُ قابلةً للمقابلة.
    """

    register_id: str
    evidence: tuple[Evidence, ...] = ()
    individuals: tuple[Individual, ...] = ()
    propositions: tuple[Proposition, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.register_id, "مُعرِّفُ السجلّ")
        for group, label, attribute in (
            (self.evidence, "الأدلّة", "evidence_id"),
            (self.individuals, "الأفراد", "individual_id"),
            (self.propositions, "القضايا", "proposition_id"),
        ):
            ids = tuple(getattr(item, attribute) for item in group)
            if len(set(ids)) != len(ids):
                raise FactError(f"مُعرِّفٌ مكرَّرٌ في {label} يُرفَض لا يُطوى")

    # ----- قراءةٌ -----

    def evidence_of(self, evidence_id: str) -> Evidence:
        """الدليلُ بمُعرِّفه؛ والغيابُ رفضٌ مُسمًّى."""

        for item in self.evidence:
            if item.evidence_id == evidence_id:
                return item
        raise FactError(f"لا دليلَ في السجلّ مُعرِّفُه `{evidence_id}`")

    def individual_of(self, individual_id: str) -> Individual:
        """الفردُ بمُعرِّفه؛ والغيابُ رفضٌ مُسمًّى."""

        for item in self.individuals:
            if item.individual_id == individual_id:
                return item
        raise FactError(f"لا فردَ في السجلّ مُعرِّفُه `{individual_id}`")

    def proposition_of(self, proposition_id: str) -> Proposition:
        """القضيّةُ بمُعرِّفها؛ والغيابُ رفضٌ مُسمًّى."""

        for item in self.propositions:
            if item.proposition_id == proposition_id:
                return item
        raise FactError(f"لا قضيّةَ في السجلّ مُعرِّفُها `{proposition_id}`")

    @property
    def active_propositions(self) -> tuple[Proposition, ...]:
        """القضايا غيرُ المعلَّقة؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(item for item in self.propositions if not item.suspended)

    # ----- إيداعٌ -----

    def with_evidence(self, evidence: Evidence) -> FactRegister:
        """أودِع دليلًا؛ ومُعرِّفٌ مكرَّرٌ بمضمونٍ مختلفٍ يُرفَض لا يُستبدَل صمتًا."""

        if not isinstance(evidence, Evidence):
            raise FactError("المُودَعُ دليلٌ قائم")
        for item in self.evidence:
            if item.evidence_id == evidence.evidence_id:
                raise FactError(
                    "دليلٌ بمُعرِّفٍ قائم؛ وتبديلُ مضمونه يكون بـ`amend_evidence` "
                    "لا بإيداعٍ ثانٍ صامت"
                )
        return replace(self, evidence=(*self.evidence, evidence))

    def with_individual(self, individual: Individual) -> FactRegister:
        """أودِع فردًا؛ ومُثبَتُ الوجود يلزمه دليلٌ قائمٌ في السجلّ."""

        if not isinstance(individual, Individual):
            raise FactError("المُودَعُ فردٌ قائم")
        if individual.evidence_ref is not None:
            self._require_live_evidence(individual.evidence_ref)
        return replace(self, individuals=(*self.individuals, individual))

    def with_proposition(self, proposition: Proposition) -> FactRegister:
        """أودِع قضيّةً بدليلٍ يُثبِت؛ والأطرافُ تُفحَص ولا تُقبَل أسماءً حرّة."""

        if not isinstance(proposition, Proposition):
            raise FactError("المُودَعُ قضيّةٌ قائمة")
        evidence = self._require_live_evidence(proposition.evidence_ref)
        if not evidence.establishes_facts:
            raise FactError(
                ONLY_A_FACT_ESTABLISHING_GENUS_DEPOSITS
                + f"؛ والجنسُ المُقدَّم: `{evidence.genus.value}`"
            )
        self.individual_of(proposition.subject_id)
        for premise_id in proposition.derived_from_proposition_ids:
            self.proposition_of(premise_id)
        return replace(self, propositions=(*self.propositions, proposition))

    def _require_live_evidence(self, ref: EvidenceRef) -> Evidence:
        evidence = self.evidence_of(ref.evidence_id)
        if not ref.matches(evidence):
            raise FactError(
                "الإشارةُ تُشير إلى مضمونٍ لم يعد قائمًا: بصمةُ الدليل تغيّرت "
                f"بعد الإشارة إليه (`{ref.evidence_id}`)"
            )
        return evidence

    # ----- الانتقالُ من المضمون إلى الواقعة -----

    def deposit_from_discourse(
        self,
        content: DiscourseContent,
        evidence: Evidence,
        proposition_id: str,
    ) -> FactRegister:
        """انقل مضمونَ عبارةٍ إلى السجلّ **بدليلٍ**، محفوظَ القطبيّة والنطاق.

        المضمونُ وحدَه لا ينقل شيئًا؛ والدليلُ هو ما يُدخِل القضيّةَ السجلَّ،
        وجنسُه هو ما يُحدِّد أتُقبَل أصلًا. والشرطيُّ والاستفهاميُّ يُرفَضان.
        """

        if not isinstance(content, DiscourseContent):
            raise FactError("المنقولُ مضمونُ عبارةٍ قائم")
        event = content.event
        if event.modality in (Modality.CONDITIONAL, Modality.INTERROGATED):
            raise FactError(
                A_CONDITIONAL_IS_NOT_UNBOUND_BY_DEPOSIT
                + f"؛ والجهةُ المقروءة: `{event.modality.value}`"
            )
        if event.modality is Modality.UNREAD:
            raise FactError("جهةُ القول غيرُ مقروءة، وغيرُ المقروءِ لا يُقرَأ إخبارًا")
        if event.negation_scope is NegationScope.ONE_ROLE_FILLING:
            raise FactError(
                "نفيُ شَغْلِ دورٍ ليس نفيًا لوقوع الحدث؛ فلا يُودَع قضيّةً عن "
                "الوقوع، وهو عينُ ما يمنع انتقالَ النطاق"
            )
        subject_id = self._subject_of(content)
        register = self.with_evidence(evidence)
        return register.with_proposition(
            Proposition(
                proposition_id=proposition_id,
                form=PropositionForm.EVENT_OCCURRED,
                subject_id=subject_id,
                predicate_id=event.event_type_id,
                value=None,
                polarity=event.polarity,
                scope=event.time_scope,
                evidence_ref=evidence.ref,
            )
        )

    def _subject_of(self, content: DiscourseContent) -> str:
        designated = tuple(
            filling
            for filling in content.event.role_fillings
            if filling.standing is FillerStanding.DESIGNATED
        )
        for filling in designated:
            assert filling.designation is not None
            if not filling.designation.is_resolved:
                raise FactError(
                    "تعيينٌ لم ينحصر في فردٍ واحد؛ ومجموعةُ المرشَّحين لا تُودَع "
                    f"موضوعًا لقضيّة (الدور `{filling.role_id}`)"
                )
            individual_id = filling.designation.candidate_individual_ids[0]
            self.individual_of(individual_id)
        if not designated:
            raise FactError(
                "مضمونٌ لا طرفَ مُعيَّنًا فيه لا يُودَع قضيّةً عن فردٍ؛ و"
                + A_MENTION_IS_NOT_AN_EXISTENCE_CLAIM
            )
        first = designated[0]
        assert first.designation is not None
        return first.designation.candidate_individual_ids[0]

    # ----- الإبطالُ وتحديثُ التابع -----

    def amend_evidence(self, evidence: Evidence) -> FactRegister:
        """بدِّل مضمونَ دليلٍ قائم، ثمّ علِّق ما استند إليه وحدَه.

        وتبديلُ المضمون يُغيِّر البصمة؛ فالقضايا المشيرةُ إلى البصمة القديمة
        تُعلَّق، وما لا يُشير إليها لا يُمَسّ.
        """

        if not isinstance(evidence, Evidence):
            raise FactError("البديلُ دليلٌ قائم")
        previous = self.evidence_of(evidence.evidence_id)
        if previous.content_id == evidence.content_id:
            raise FactError("تبديلٌ لا يُغيِّر المضمون؛ ولا هويّةَ جديدةً بلا مضمونٍ جديد")
        replaced = tuple(
            evidence if item.evidence_id == evidence.evidence_id else item
            for item in self.evidence
        )
        return replace(self, evidence=replaced)._suspend_dependents_of(
            previous.ref.content_id, evidence.evidence_id
        )

    def retract(self, evidence_id: str) -> FactRegister:
        """أبطِل دليلًا: تُعلَّق القضايا المستندةُ إليه وتوابعُها، ولا يُمَسّ غيرُها."""

        evidence = self.evidence_of(evidence_id)
        return self._suspend_dependents_of(evidence.content_id, evidence_id)

    def _suspend_dependents_of(self, content_id: str, evidence_id: str) -> FactRegister:
        suspended_ids: set[str] = set()
        updated = list(self.propositions)
        for index, item in enumerate(updated):
            if (
                item.evidence_ref.evidence_id == evidence_id
                and item.evidence_ref.content_id == content_id
                and not item.suspended
            ):
                updated[index] = replace(item, suspended=True)
                suspended_ids.add(item.proposition_id)
        changed = True
        while changed:
            changed = False
            for index, item in enumerate(updated):
                if item.suspended:
                    continue
                if suspended_ids & set(item.derived_from_proposition_ids):
                    updated[index] = replace(item, suspended=True)
                    suspended_ids.add(item.proposition_id)
                    changed = True
        return replace(self, propositions=tuple(updated))

    def reinstate(self, proposition_id: str, evidence: Evidence) -> FactRegister:
        """أعِد تقييمَ قضيّةٍ معلَّقةٍ ببرهانٍ مستقلٍّ بديل، لا بإسقاطٍ آليّ.

        والإعادةُ لا تقع إلّا بدليلٍ **آخَر** يُثبِت؛ وإلّا بقيت معلَّقةً كما هي.
        """

        item = self.proposition_of(proposition_id)
        if not item.suspended:
            raise FactError("القضيّةُ غيرُ معلَّقة؛ ولا إعادةَ تقييمٍ لما لم يُعلَّق")
        if evidence.evidence_id == item.evidence_ref.evidence_id:
            raise FactError("الإعادةُ ببرهانٍ مستقلٍّ: دليلٌ بمُعرِّفِ الدليل المُبطَل ليس بديلًا")
        if not evidence.establishes_facts:
            raise FactError(ONLY_A_FACT_ESTABLISHING_GENUS_DEPOSITS)
        register = (
            self
            if any(one.evidence_id == evidence.evidence_id for one in self.evidence)
            else self.with_evidence(evidence)
        )
        updated = tuple(
            replace(one, suspended=False, evidence_ref=evidence.ref)
            if one.proposition_id == proposition_id
            else one
            for one in register.propositions
        )
        return replace(register, propositions=updated)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السجلّ للبصمة."""

        return {
            "register_id": self.register_id,
            "evidence": [
                {"evidence_id": item.evidence_id, **item.as_canonical_content()}
                for item in sorted(self.evidence, key=lambda item: item.evidence_id)
            ],
            "individuals": [
                item.as_canonical_content()
                for item in sorted(
                    self.individuals, key=lambda item: item.individual_id
                )
            ],
            "propositions": [
                item.as_canonical_content()
                for item in sorted(
                    self.propositions, key=lambda item: item.proposition_id
                )
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ السجلّ؛ وكلُّ إيداعٍ أو إبطالٍ يُخرِج بصمةً أخرى."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
