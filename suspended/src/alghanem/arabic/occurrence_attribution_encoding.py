"""ترميزٌ ثنائيٌّ للوقعات المقيسة، وتجربةُ فصلٍ تُظهِر ضرورةَ علاقة التعيين.

**السؤالان المُجابُ عنهما ههنا بحرفهما**: أيُسترجَع الوقوعُ الكتابيُّ المقيسُ
من ترميزٍ ثنائيٍّ ذي سجلّاتٍ مشتركةٍ مرتّبة؟ وهل يحتاج الاسترجاعُ حقلَ إسنادٍ
ثالثًا مستقلًّا؟ والجوابان يخرجان بالتشغيل::

    RetrievalInTheMeasuredScope      → قائم
    TheAttributionRelationUnderSeparation → ضروريّ
    AnExtraAttributionField          → لا يضيف معلومةً للهدف المحدَّد
    ALinguisticOrPhoneticBirth       → مُرجأ

وحدودُ ذلك مُسمّاةٌ لا مطويّة:

* **الاسترجاعُ صحّةُ ترميزٍ لا شهادةُ ولادة.** أن تُسترجَع الوقعاتُ من
  بايتاتها شيءٌ، وأن يُقال إنّ اللغةَ وُلِد ليفُها شيءٌ آخر لا يدّعى ههنا
  (`A_ROUND_TRIP_IS_A_CODING_PROPERTY_NOT_A_LINGUISTIC_LAW`).
* **النطاقُ هو المقيسُ وحدَه.** ما لم يُعيَّن في الطبقة المرجعيّة يُرمَّز
  **بوصفه ممتنعًا عن التعيين**، فيُسترجَع امتناعُه لا حالٌ اختُرعت له
  (`AN_UNRESOLVED_OCCURRENCE_IS_ENCODED_AS_UNRESOLVED_NOT_GUESSED`).
* **الضرورةُ مُثبَتةٌ بشاهدٍ قادحٍ لا بدعوى.** مثالُ الميمين — ميمٌ ساكنةٌ
  وميمٌ متحرّكة — يُشغَّل، ويُعَدُّ عددُ التركيبات المتّسقة مع البيانات
  المفصولة؛ فإن زاد على واحدٍ فالموضعُ ضائع.
* **«لا حاجة» ليست «لا معنى».** نفيُ الحاجة مقصورٌ على **الهدف المُعلَن**:
  استرجاعُ الوقعة. وحقلٌ لا يضيف بتًّا لهذا الهدف قد يضيف لهدفٍ آخرَ لم يُختبَر
  هنا (`NOT_NECESSARY_IS_RELATIVE_TO_THE_DECLARED_TARGET_ONLY`).
* **الإرجاءُ بمانعٍ مُسمًّى لا بسكوت.** لا هدفَ لغويٌّ مستقلٌّ اختُبر، ولا
  قارئَ مؤهّلٌ للإغلاق على شرط `minimal_complete_fiber`، ولا قياسَ أداءٍ
  صوتيٍّ للوصل والوقف.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا تقرؤها
بوّابةٌ في `kernel/`. وكلُّ عددٍ تُخرجه يُشتقّ عند القراءة لا يُكتَب في حقل.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from itertools import permutations
from typing import Final

from alghanem.arabic.reference_articulation_layer import (
    ReferenceReading,
    read_the_deposited_ayah,
)

__all__ = [
    "AN_EXTRA_FIELD_COSTS_BITS_AND_RETURNS_NONE",
    "AN_UNRESOLVED_OCCURRENCE_IS_ENCODED_AS_UNRESOLVED_NOT_GUESSED",
    "A_ROUND_TRIP_IS_A_CODING_PROPERTY_NOT_A_LINGUISTIC_LAW",
    "A_SWAP_THAT_SURVIVES_IS_A_LOST_POSITION_NOT_A_TIE",
    "AttributionFieldNecessity",
    "BirthBlocker",
    "EncodedCorpus",
    "LinguisticAndPhoneticBirth",
    "NO_INDEPENDENT_THREE_FIELD_TRIPLE_IS_BORN_HERE",
    "NO_LINGUISTIC_FIBER_LAW_IS_BORN_HERE",
    "NOT_NECESSARY_IS_RELATIVE_TO_THE_DECLARED_TARGET_ONLY",
    "OCCURRENCE_ATTRIBUTION_NAMED_RESIDUALS",
    "OccurrenceAttributionError",
    "OccurrenceRecord",
    "THE_MEASURED_SCOPE_IS_THIS_DEPOSIT_NOT_THE_LANGUAGE",
    "THE_TWO_MIMS",
    "SeparatedData",
    "SharedRegisters",
    "UNRESOLVED_STATE",
    "assess_attribution_field",
    "assess_linguistic_and_phonetic_birth",
    "decode_corpus",
    "encode_corpus",
    "occurrences_of",
    "separate",
]


class OccurrenceAttributionError(ValueError):
    """خطأٌ في الترميز أو فكّه؛ يُرفَع ولا يُصحَّح المُدخَلُ ضمنًا."""


UNRESOLVED_STATE: Final[str] = "غير_مُعيَّن"
"""حالُ الوقعة التي امتنعت عن التعيين؛ تُرمَّز امتناعًا لا تُخمَّن."""


@dataclass(frozen=True, slots=True)
class OccurrenceRecord:
    """وقعةٌ مقيسة: حاملُها المرسوم، وحالُها، وموضعُها من الكلمات.

    والعلاقةُ بين الحامل والحال **داخل السجلّ نفسِه**، لا في جدولٍ ثالثٍ
    بجانبه؛ وهذا هو محلُّ النزاع الذي تفصل فيه هذه الوحدة.
    """

    word_index: int
    carrier: str
    state: str

    def __post_init__(self) -> None:
        if self.word_index < 0:
            raise OccurrenceAttributionError("موضعُ الكلمة عددٌ غيرُ سالب")
        if not self.carrier:
            raise OccurrenceAttributionError("وقعةٌ بلا حاملٍ مرسومٍ لا تُرمَّز")
        if not self.state:
            raise OccurrenceAttributionError("وقعةٌ بلا حالٍ مكتوبٍ لا تُرمَّز")

    @property
    def pair(self) -> tuple[str, str]:
        """زوجُ الحامل والحال؛ وهو ما يُطلَب استرجاعُه موضوعًا في محلّه."""

        return (self.carrier, self.state)


def occurrences_of(reading: ReferenceReading) -> tuple[OccurrenceRecord, ...]:
    """اقرأ وقعاتِ الطبقة المرجعيّة سجلّاتٍ قابلةً للترميز؛ ولا يُطرَح ممتنع."""

    return tuple(
        OccurrenceRecord(
            word_index=one.word_index,
            carrier=one.graphic,
            state=UNRESOLVED_STATE if one.pattern is None else one.pattern.letter,
        )
        for one in reading.occurrences
    )


def _width(count: int) -> int:
    """عرضُ الخانة بالبتّات لسجلٍّ بهذا العدد، مُشتقًّا لا مكتوبًا."""

    if count <= 0:
        raise OccurrenceAttributionError("سجلٌّ خالٍ لا يُرمَّز منه رمزٌ واحد")
    width = 1
    while (1 << width) < count:
        width += 1
    return width


@dataclass(frozen=True, slots=True)
class SharedRegisters:
    """سجلّاتٌ مشتركةٌ مرتّبة: الحواملُ والحالاتُ وأطوالُ الكلمات.

    و**الترتيبُ هو المفتاح**: الرمزُ ليس إلّا رتبةً في سجلٍّ مُتَّفَقٍ عليه،
    فمن بدّل ترتيبَ السجلّ بدّل معنى كلّ رمزٍ في البايتات.
    """

    carriers: tuple[str, ...]
    states: tuple[str, ...]
    longest_word: int

    def __post_init__(self) -> None:
        if len(set(self.carriers)) != len(self.carriers):
            raise OccurrenceAttributionError("سجلُّ الحوامل لا يقبل تكرارَ مدخل")
        if len(set(self.states)) != len(self.states):
            raise OccurrenceAttributionError("سجلُّ الحالات لا يقبل تكرارَ مدخل")
        if self.longest_word <= 0:
            raise OccurrenceAttributionError("أطولُ كلمةٍ وقعةٌ واحدةٌ على الأقلّ")

    @property
    def carrier_width(self) -> int:
        """عرضُ خانة الحامل، مُشتقًّا من عدد مدخلات سجلّه."""

        return _width(len(self.carriers))

    @property
    def state_width(self) -> int:
        """عرضُ خانة الحال، مُشتقًّا من عدد مدخلات سجلّه."""

        return _width(len(self.states))

    @property
    def length_width(self) -> int:
        """عرضُ خانة طول الكلمة، مُشتقًّا من أطول كلمةٍ في المقيس."""

        return _width(self.longest_word + 1)

    @property
    def record_width(self) -> int:
        """عرضُ سجلّ الوقعة الواحدة؛ حاملٌ وحالٌ لا ثالثَ لهما."""

        return self.carrier_width + self.state_width

    def carrier_code(self, carrier: str) -> int:
        """رتبةُ الحامل في سجلّه؛ ويُرفَض ما ليس فيه."""

        try:
            return self.carriers.index(carrier)
        except ValueError as error:
            raise OccurrenceAttributionError(
                "حاملٌ خارجَ السجلّ المشترك لا يُرمَّز؛ والسجلُّ لا يُوسَّع ضمنًا"
            ) from error

    def state_code(self, state: str) -> int:
        """رتبةُ الحال في سجلّه؛ ويُرفَض ما ليس فيه."""

        try:
            return self.states.index(state)
        except ValueError as error:
            raise OccurrenceAttributionError(
                "حالٌ خارجَ السجلّ المشترك لا يُرمَّز؛ والسجلُّ لا يُوسَّع ضمنًا"
            ) from error


def _registers_for(records: Sequence[OccurrenceRecord]) -> SharedRegisters:
    carriers: list[str] = []
    states: list[str] = []
    lengths: dict[int, int] = {}
    for record in records:
        if record.carrier not in carriers:
            carriers.append(record.carrier)
        if record.state not in states:
            states.append(record.state)
        lengths[record.word_index] = lengths.get(record.word_index, 0) + 1
    return SharedRegisters(
        carriers=tuple(carriers),
        states=tuple(states),
        longest_word=max(lengths.values()) if lengths else 1,
    )


def _bits(value: int, width: int) -> str:
    if value < 0 or value >= (1 << width):
        raise OccurrenceAttributionError("قيمةٌ لا تسع خانتَها لا تُقتطَع؛ تُرَدّ")
    return format(value, f"0{width}b")


@dataclass(frozen=True, slots=True)
class EncodedCorpus:
    """بايتاتٌ ثنائيّةٌ وسجلّاتُها؛ وكلُّ عددٍ عنها مُشتقٌّ عند القراءة."""

    registers: SharedRegisters
    bits: str
    word_count: int

    def __post_init__(self) -> None:
        if set(self.bits) - {"0", "1"}:
            raise OccurrenceAttributionError("الترميزُ ثنائيٌّ، ولا رمزَ ثالثَ فيه")

    @property
    def bit_length(self) -> int:
        """طولُ الترميز بالبتّات، مُشتقًّا لا مُعلَنًا."""

        return len(self.bits)


def encode_corpus(records: Sequence[OccurrenceRecord]) -> EncodedCorpus:
    """رمِّز الوقعاتِ ترميزًا ثنائيًّا بسجلّاتٍ مشتركةٍ مرتّبةٍ مُشتقّةٍ منها.

    وحدودُ الكلمات **محفوظةٌ بطولٍ مُصرَّحٍ به قبل كلّ كلمة**، لا برمزٍ فاصلٍ:
    فالرمزُ الفاصلُ يحتلّ قيمةً في فضاء الرموز فيلتبس بحاملٍ، والطولُ لا يلتبس.
    """

    if not records:
        raise OccurrenceAttributionError("مُدوّنةٌ خاليةٌ لا تُرمَّز ولا تُسترجَع")
    registers = _registers_for(records)
    words: list[list[OccurrenceRecord]] = []
    for record in records:
        if not words or words[-1][0].word_index != record.word_index:
            words.append([record])
        else:
            words[-1].append(record)
    pieces: list[str] = [_bits(len(words), 32)]
    for word in words:
        pieces.append(_bits(len(word), registers.length_width))
        for record in word:
            pieces.append(
                _bits(registers.carrier_code(record.carrier), registers.carrier_width)
            )
            pieces.append(
                _bits(registers.state_code(record.state), registers.state_width)
            )
    return EncodedCorpus(
        registers=registers, bits="".join(pieces), word_count=len(words)
    )


def decode_corpus(encoded: EncodedCorpus) -> tuple[OccurrenceRecord, ...]:
    """فُكَّ الترميزَ إلى وقعاتٍ؛ ويُرفَض كلُّ رمزٍ غيرِ مخصَّصٍ في سجلّه.

    فرمزٌ يقع في فضاء الخانة ولا مدخلَ له في السجلّ **يُرَدّ**، ولا يُردّ عنه
    أقربُ مدخلٍ ولا مدخلٌ افتراضيّ؛ فالتساهلُ ههنا يُخرِج وقعاتٍ لم تُقَس.
    """

    registers = encoded.registers
    cursor = 0

    def take(width: int) -> int:
        nonlocal cursor
        chunk = encoded.bits[cursor : cursor + width]
        if len(chunk) != width:
            raise OccurrenceAttributionError("بايتاتٌ ناقصةٌ لا تُكمَّل بأصفارٍ مفترضة")
        cursor += width
        return int(chunk, 2)

    word_count = take(32)
    records: list[OccurrenceRecord] = []
    for word_index in range(word_count):
        length = take(registers.length_width)
        if length == 0:
            raise OccurrenceAttributionError("كلمةٌ بلا وقعةٍ ليست حدًّا محفوظًا")
        for _ in range(length):
            carrier_code = take(registers.carrier_width)
            state_code = take(registers.state_width)
            if carrier_code >= len(registers.carriers):
                raise OccurrenceAttributionError(
                    "رمزُ حاملٍ غيرُ مخصَّصٍ في السجلّ؛ ولا يُردّ عنه أقربُ مدخل"
                )
            if state_code >= len(registers.states):
                raise OccurrenceAttributionError(
                    "رمزُ حالٍ غيرُ مخصَّصٍ في السجلّ؛ ولا يُردّ عنه أقربُ مدخل"
                )
            records.append(
                OccurrenceRecord(
                    word_index=word_index,
                    carrier=registers.carriers[carrier_code],
                    state=registers.states[state_code],
                )
            )
    if cursor != len(encoded.bits):
        raise OccurrenceAttributionError("بايتاتٌ زائدةٌ بعد آخر كلمةٍ لا تُهمَل")
    return tuple(records)


# --- تجربةُ الفصل: مثالُ الميمين -----------------------------------------------


THE_TWO_MIMS: Final[tuple[OccurrenceRecord, ...]] = (
    OccurrenceRecord(word_index=0, carrier="م", state="ساكنة"),
    OccurrenceRecord(word_index=0, carrier="م", state="متحرّكة"),
)
"""ميمان في كلمةٍ واحدة، حاملُهما واحدٌ وحالُهما مختلف؛ وهو الشاهدُ القادح.

فلو كان الحاملان مختلفَي الرسم لَفرّقهما الرسمُ وحدَه، ولَما احتيج إلى علاقة؛
فالشاهدُ يُختار **قادحًا بالبناء** لا مُيسِّرًا للنتيجة المطلوبة.
"""


@dataclass(frozen=True, slots=True)
class SeparatedData:
    """بياناتٌ مفصولة: مجموعةُ الحوامل ومجموعةُ الحالات، بلا رابطٍ بينهما.

    وهي صورةُ «ثلاثةِ حقولٍ مستقلّةٍ» التي تُدَّعى: حواملُ في جدولٍ، وحالاتٌ في
    جدولٍ، والموضعُ يُتوقَّع أن يُستنتَج. وهذه الوحدةُ تُشغِّل هذا التوقّع.
    """

    carriers: tuple[str, ...]
    states: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.carriers) != len(self.states):
            raise OccurrenceAttributionError(
                "الفصلُ لا يُنقِص عددًا؛ فمجموعتان مختلفتا الكثرة ليستا فصلًا لهذه"
            )

    @property
    def consistent_reassemblies(self) -> frozenset[tuple[tuple[str, str], ...]]:
        """كلُّ تركيبٍ متّسقٍ مع المفصول؛ ويُعَدُّ بالتشغيل لا بالتقدير.

        والاتّساقُ ههنا: أيُّ إقرانٍ للحوامل بالحالات يحفظ ترتيبَ الحوامل
        ويستوفي الحالاتِ كلَّها. فإن زاد المتّسقُ على واحدٍ فالبياناتُ المفصولة
        لا تُعيّن الأصلَ، وإن كان واحدًا فالفصلُ لم يُضِع شيئًا ههنا.
        """

        return frozenset(
            tuple(zip(self.carriers, order, strict=True))
            for order in permutations(self.states)
        )

    @property
    def attribution_is_lost(self) -> bool:
        """أضاع الفصلُ موضعَ الإسناد؟ يُقرَأ من تعدّد التركيبات المتّسقة."""

        return len(self.consistent_reassemblies) > 1


def separate(records: Sequence[OccurrenceRecord]) -> SeparatedData:
    """افصِل السجلّاتِ إلى مجموعتين بلا رابط؛ وهي عمليةٌ تُجرى لا تُفترَض."""

    return SeparatedData(
        carriers=tuple(one.carrier for one in records),
        states=tuple(one.state for one in records),
    )


# --- الحقلُ الثالث: أيضيف بتًّا للهدف المُعلَن؟ -----------------------------------


class AttributionFieldNecessity(Enum):
    """حالُ حقل الإسناد الثالث بالنسبة إلى هدفٍ مُعلَن؛ ثلاثةٌ مغلقة."""

    NECESSARY_FOR_THE_DECLARED_TARGET = "ضروريٌّ_للهدف_المُعلَن"
    NOT_NECESSARY_FOR_THE_DECLARED_TARGET = "غيرُ_ضروريٍّ_للهدف_المُعلَن"
    UNTESTED_AGAINST_ANY_TARGET = "لم_يُختبَر_على_هدف"


@dataclass(frozen=True, slots=True)
class AttributionFieldDecision:
    """قرارٌ مُشتقٌّ: أيزيد الحقلُ الثالثُ استرجاعًا، أم يزيد بتّاتٍ فحسب؟"""

    necessity: AttributionFieldNecessity
    plain_bits: int
    augmented_bits: int
    both_retrieve_the_same: bool

    @property
    def added_bits(self) -> int:
        """ما كلّفه الحقلُ الثالثُ من بتّات، مُشتقًّا بالطرح."""

        return self.augmented_bits - self.plain_bits


def assess_attribution_field(
    records: Sequence[OccurrenceRecord],
) -> AttributionFieldDecision:
    """قايِس ترميزين: سجلٌّ يحفظ العلاقةَ بترتيبه، وسجلٌّ يُكرّرها حقلًا ثالثًا.

    والحقلُ الثالثُ ههنا **دالّةٌ في السجلّ نفسِه**: رتبةُ زوج (حامل، حال) في
    سجلٍّ ثالث. فهو مُشتقٌّ ممّا رُمِّز أصلًا، ولا يفصل حالَين لم يفصلهما
    السجلّ. ولذلك يُقاس أثرُه على **الهدف المُعلَن وحدَه**: استرجاعُ الوقعة في
    محلّها (`NOT_NECESSARY_IS_RELATIVE_TO_THE_DECLARED_TARGET_ONLY`).
    """

    plain = encode_corpus(records)
    decoded = decode_corpus(plain)
    pairs: list[tuple[str, str]] = []
    for record in records:
        if record.pair not in pairs:
            pairs.append(record.pair)
    pair_width = _width(len(pairs))
    augmented_bits = plain.bit_length + pair_width * len(records)
    both_same = decoded == tuple(records)
    if augmented_bits > plain.bit_length and both_same:
        necessity = AttributionFieldNecessity.NOT_NECESSARY_FOR_THE_DECLARED_TARGET
    elif not both_same:
        necessity = AttributionFieldNecessity.NECESSARY_FOR_THE_DECLARED_TARGET
    else:
        necessity = AttributionFieldNecessity.UNTESTED_AGAINST_ANY_TARGET
    return AttributionFieldDecision(
        necessity=necessity,
        plain_bits=plain.bit_length,
        augmented_bits=augmented_bits,
        both_retrieve_the_same=both_same,
    )


# --- الشهادةُ اللغويّةُ والصوتيّة: إرجاءٌ بموانعَ مُسمّاة --------------------------


class BirthBlocker(Enum):
    """موانعُ الشهادة اللغويّة والصوتيّة، كلٌّ منها مُسمًّى بموضعه."""

    NO_INDEPENDENT_LINGUISTIC_TARGET_WAS_TESTED = "لا_هدفَ_لغويًّا_مستقلًّا_اختُبر"
    NO_READER_QUALIFIED_TO_CLOSE_THE_REQUIREMENT = "لا_قارئَ_مؤهّلًا_للإغلاق"
    NO_PERFORMANCE_MEASUREMENT_OF_WASL_AND_WAQF = "لا_قياسَ_أداءٍ_للوصل_والوقف"


class LinguisticAndPhoneticBirth(Enum):
    """حالُ الشهادة اللغويّة والصوتيّة؛ مُخرَجٌ واحدٌ لا ثالثَ له اليوم."""

    DEFER = "مُرجأةٌ_بموانعَ_مُسمّاة"


@dataclass(frozen=True, slots=True)
class BirthVerdict:
    """حكمُ هذه التجربة مفصولَ الأجزاء؛ فلا يُقرَأ اجتيازُ جزءٍ اجتيازًا للكلّ."""

    retrieval_holds_in_the_measured_scope: bool
    attribution_relation_is_necessary: bool
    attribution_field: AttributionFieldNecessity
    linguistic_and_phonetic: LinguisticAndPhoneticBirth
    blockers: tuple[BirthBlocker, ...]

    @property
    def a_three_field_triple_is_born(self) -> bool:
        """لا. فثلاثةُ حقولٍ مستقلّةٍ لم تثبت ولادتُها ههنا، والنفيُ مكتوب."""

        return False

    @property
    def a_complete_linguistic_fiber_law_is_born(self) -> bool:
        """لا. والإرجاءُ قائمٌ بموانعه الثلاثة، لا يرفعه اجتيازُ الترميز."""

        return False


def assess_linguistic_and_phonetic_birth(
    records: Sequence[OccurrenceRecord] = (),
) -> BirthVerdict:
    """اقرأ الحكمَ من التشغيل: استرجاعٌ قائم، وعلاقةٌ ضروريّة، وشهادةٌ مُرجأة.

    وقيامُ الاسترجاع **لا يرفع** الإرجاءَ ولا يمسّه: موانعُه الثلاثةُ في جنسٍ
    آخرَ من الأدلّة، وترقيةُ حكمٍ بدليلٍ من غير جنسه هي عينُ ما تمنعه هذه
    الشجرة (`A_ROUND_TRIP_IS_A_CODING_PROPERTY_NOT_A_LINGUISTIC_LAW`).
    """

    measured = tuple(records) if records else occurrences_of(read_the_deposited_ayah())
    retrieval = decode_corpus(encode_corpus(measured)) == measured
    return BirthVerdict(
        retrieval_holds_in_the_measured_scope=retrieval,
        attribution_relation_is_necessary=separate(THE_TWO_MIMS).attribution_is_lost,
        attribution_field=assess_attribution_field(measured).necessity,
        linguistic_and_phonetic=LinguisticAndPhoneticBirth.DEFER,
        blockers=tuple(BirthBlocker),
    )


# --- ما لا تحسمه هذه التجربة، مُسمًّى ------------------------------------------


A_ROUND_TRIP_IS_A_CODING_PROPERTY_NOT_A_LINGUISTIC_LAW: Final[str] = (
    "A_ROUND_TRIP_IS_A_CODING_PROPERTY_NOT_A_LINGUISTIC_LAW: قيامُ الاسترجاع "
    "خاصّيّةٌ في الترميز الذي كُتب ههنا، لا قانونٌ في العربية؛ ولا يُرفَع به "
    "إرجاءُ الشهادة اللغويّة ولا الصوتيّة، إذ الدليلُ من غير جنس الدعوى"
)

THE_MEASURED_SCOPE_IS_THIS_DEPOSIT_NOT_THE_LANGUAGE: Final[str] = (
    "THE_MEASURED_SCOPE_IS_THIS_DEPOSIT_NOT_THE_LANGUAGE: النطاقُ المقيسُ "
    "وقعاتُ نصٍّ مُودَعٍ بعينه؛ وقيامُ الاسترجاع عليه لا يُعمَّم على ما لم "
    "يُقَس، ولا على رسمٍ لم يُعرَض على السجلّات"
)

AN_UNRESOLVED_OCCURRENCE_IS_ENCODED_AS_UNRESOLVED_NOT_GUESSED: Final[str] = (
    "AN_UNRESOLVED_OCCURRENCE_IS_ENCODED_AS_UNRESOLVED_NOT_GUESSED: الوقعةُ "
    "الممتنعةُ عن التعيين تُرمَّز بحالِ امتناعها فيُسترجَع الامتناعُ نفسُه؛ "
    "وترميزُها بحالٍ مُخمَّنةٍ يرفع نسبةَ الاسترجاع باختراع ما لم يُقَس"
)

A_SWAP_THAT_SURVIVES_IS_A_LOST_POSITION_NOT_A_TIE: Final[str] = (
    "A_SWAP_THAT_SURVIVES_IS_A_LOST_POSITION_NOT_A_TIE: تبديلُ حالَي الميمين "
    "إذا بقي متّسقًا مع البيانات المفصولة فالموضعُ ضائعٌ لا متكافئ؛ فالتركيبان "
    "يصفان وقوعين مختلفين ولا يفصل بينهما المفصول"
)

NOT_NECESSARY_IS_RELATIVE_TO_THE_DECLARED_TARGET_ONLY: Final[str] = (
    "NOT_NECESSARY_IS_RELATIVE_TO_THE_DECLARED_TARGET_ONLY: نفيُ الحاجة إلى "
    "حقل الإسناد مقصورٌ على هدف استرجاع الوقعة في محلّها؛ وحقلٌ لا يضيف بتًّا "
    "لهذا الهدف قد يضيف لهدفٍ آخرَ لم يُعرَض ههنا، فلا يُقرَأ النفيُ عامًّا"
)

AN_EXTRA_FIELD_COSTS_BITS_AND_RETURNS_NONE: Final[str] = (
    "AN_EXTRA_FIELD_COSTS_BITS_AND_RETURNS_NONE: الحقلُ الثالثُ دالّةٌ في "
    "السجلّ المرمَّز أصلًا، فلا يفصل حالَين لم يفصلهما السجلّ؛ وزيادتُه زيادةُ "
    "بتّاتٍ مقيسةٌ بالطرح لا زيادةُ معلومة"
)

NO_INDEPENDENT_THREE_FIELD_TRIPLE_IS_BORN_HERE: Final[str] = (
    "NO_INDEPENDENT_THREE_FIELD_TRIPLE_IS_BORN_HERE: لم تثبت ولادةُ ثلاثيّةٍ "
    "مستقلّةٍ من ثلاثة حقول؛ والذي وُلِد ضرورةُ حفظ علاقة التعيين عند فصل "
    "البيانات، وهو أضيقُ منها"
)

NO_LINGUISTIC_FIBER_LAW_IS_BORN_HERE: Final[str] = (
    "NO_LINGUISTIC_FIBER_LAW_IS_BORN_HERE: لم يُولَد قانونُ ليفٍ لغويٍّ مكتمل؛ "
    "والنفيُ مكتوبٌ لئلّا يُقرَأ سكوتُ الشفرة عنه احتمالًا مفتوحًا"
)

OCCURRENCE_ATTRIBUTION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_ROUND_TRIP_IS_A_CODING_PROPERTY_NOT_A_LINGUISTIC_LAW": (
        A_ROUND_TRIP_IS_A_CODING_PROPERTY_NOT_A_LINGUISTIC_LAW
    ),
    "THE_MEASURED_SCOPE_IS_THIS_DEPOSIT_NOT_THE_LANGUAGE": (
        THE_MEASURED_SCOPE_IS_THIS_DEPOSIT_NOT_THE_LANGUAGE
    ),
    "AN_UNRESOLVED_OCCURRENCE_IS_ENCODED_AS_UNRESOLVED_NOT_GUESSED": (
        AN_UNRESOLVED_OCCURRENCE_IS_ENCODED_AS_UNRESOLVED_NOT_GUESSED
    ),
    "A_SWAP_THAT_SURVIVES_IS_A_LOST_POSITION_NOT_A_TIE": (
        A_SWAP_THAT_SURVIVES_IS_A_LOST_POSITION_NOT_A_TIE
    ),
    "NOT_NECESSARY_IS_RELATIVE_TO_THE_DECLARED_TARGET_ONLY": (
        NOT_NECESSARY_IS_RELATIVE_TO_THE_DECLARED_TARGET_ONLY
    ),
    "AN_EXTRA_FIELD_COSTS_BITS_AND_RETURNS_NONE": (
        AN_EXTRA_FIELD_COSTS_BITS_AND_RETURNS_NONE
    ),
    "NO_INDEPENDENT_THREE_FIELD_TRIPLE_IS_BORN_HERE": (
        NO_INDEPENDENT_THREE_FIELD_TRIPLE_IS_BORN_HERE
    ),
    "NO_LINGUISTIC_FIBER_LAW_IS_BORN_HERE": NO_LINGUISTIC_FIBER_LAW_IS_BORN_HERE,
}
"""ما لا تحسمه هذه التجربة، مُسمًّى هنا لا متروكًا ليُفترَض."""
