"""فحصُ مصدرٍ نحويٍّ مقترَح قبل بنائه: أيُتاح أصلًا، وبأيّ إذن، وبأيّ بنية؟

اقتُرح كتابُ **النحو الواضح في قواعد اللغة العربية** لعليّ الجارم ومصطفى أمين
مصدرًا لعملٍ لاحقٍ في الشجرة النحوية: ٤٢١ قاعدةً مرقّمةً في ثلاثة أجزاء، مع
أمثلةٍ وتمريناتٍ لكلّ قاعدة. وهذه الوحدةُ **الخطوةُ صفر وحدَها** على المنوال
الذي جرى عليه شاهدُ المدوَّنة الإعرابية وإيداعُ الحامل/الحالة: يُتحقَّق قبل
البناء، وتُسمّى القيودُ المعلومةُ سلفًا لا بعد أن يُبنى عليها::

    ProbedSource     != LicensedSource
    ARuleStatement   != ADecisionProcedure

**والإذنُ يسبق البنية.** فإن لم يُبلَغ مصدرٌ ذو رخصةٍ صريحةٍ مفتوحة، لم تُقرَأ
بنيةُ الكتاب أصلًا، ولم تُسجَّل عنها دعوى؛ لأنّ قولَ «بنيتُه مستخرَجة» عن نصٍّ
لم يُحسَم إذنُه يُقدِّم الطُّعمَ على الحكم. وقاعدةُ `WitnessBytesAreNotVendored`
في `irab_corpus_witness` قائمةٌ هنا بأشدّ: تلك المدوَّنةُ كانت ذاتَ رخصةٍ
منصوصة، وهذا الكتابُ يدور في مواضعَ تقول «الملكية الفكرية محفوظة لأصحابها» أو
تسكت، **وسكوتُ الرخصة ليس إذنًا**.

**وما جرى فعلًا في هذه البيئة**: طُلبت مواضعُ المصدر الخمسةُ المُسمّاة أدناه
واحدًا واحدًا، فلم يُفتَح منها شيء؛ حُجب اسمُ المضيف نفسُه (`DNS`) فلم تصل
الطلبات. فرتبةُ كلِّ مُرشَّحٍ هنا **لم تُبلَغ من هذه البيئة**، لا «غيرُ
موجود»، على منوال ما صُرِّح به في `REQUESTED_EDITION_WAS_NOT_REACHED`. وما وصل
عن رخصِ تلك الصفحات وصل خبرًا من محرّك بحثٍ لا من صفحةٍ فُتِحت، فلا يُكتَب
نصًّا مقروءًا (`SECOND_HAND_LICENCE_REPORT_IS_NOT_A_READ_PAGE`).

**ولم تُنسَخ بايتةٌ واحدة**، ولا بصمةٌ لملفٍّ لم يُفتَح، ولا سطرُ قاعدةٍ من
الكتاب؛ فاستخراجُ «العناوين وحدَها» من نصٍّ محفوظِ الحقوق مُشتَقٌّ منه لا بصمةٌ
عنه (`A_DIGEST_IS_NOT_A_PERMISSION`).

**ولا سلطةَ لهذه الوحدة**: لا تسجيلَ مسبقًا، ولا استخراج، ولا عقدةَ قرارٍ
واحدة، ولا صفَّ خطوةٍ في `DirectCertaintyStep`، ولا ولادة، ولا تجميد، ولا
تستورد من `kernel/` شيئًا (`THIS_PROBE_IS_NOT_A_GATE`).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "A_DIGEST_IS_NOT_A_PERMISSION",
    "A_RULE_STATEMENT_IS_NOT_A_DECISION_PROCEDURE",
    "MAANI_AL_NAHW_IS_NOT_NAHW_WADIH",
    "MAANI_AL_NAHW_REJECTED_WORK",
    "NAHW_WADIH_PROBE_NAMED_RESIDUALS",
    "NAHW_WADIH_WORK",
    "OCR_OVER_SCAN_IS_NEITHER_EDITION_NOR_TRANSCRIPTION",
    "PROBED_CANDIDATES",
    "PUBLIC_DOMAIN_BY_AGE_IS_A_JURISDICTIONAL_QUESTION",
    "RIGHTS_RESERVED_IS_A_STRONGER_BAR_THAN_SILENCE",
    "SECOND_HAND_LICENCE_REPORT_IS_NOT_A_READ_PAGE",
    "THIS_PROBE_IS_NOT_A_GATE",
    "GrammarSourceCandidate",
    "GrammarSourceProbeError",
    "GrammarSourceProbeOutcome",
    "GrammarSourceProbeReport",
    "LicenceStanding",
    "ProposedWork",
    "SourceReachability",
    "StructureStanding",
    "TextLayerStanding",
    "run_nahw_wadih_source_probe",
    "derive_probe_outcome",
]


class GrammarSourceProbeError(ValueError):
    """تُرفَع حين يُوصَف مُرشَّحٌ وصفًا يدّعي قراءةَ ما لم يُفتَح."""


def _require_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GrammarSourceProbeError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
    return value


# --- الكتابُ المقصود، وغيرُه المرفوضُ بعلّته -----------------------------------


@dataclass(frozen=True, slots=True)
class ProposedWork:
    """كتابٌ مقترَحٌ مُسمًّى بمؤلّفيه؛ ومعه علّةُ ردِّه إن كان مردودًا."""

    title: str
    authors: tuple[str, ...]
    rejection_ground: str | None

    def __post_init__(self) -> None:
        _require_text(self.title, "عنوانُ الكتاب")
        if not self.authors:
            raise GrammarSourceProbeError(
                "كتابٌ بلا مؤلّفٍ مُسمًّى لا يُميَّز عن كتابٍ آخر بعنوانٍ قريب."
            )
        for author in self.authors:
            _require_text(author, "اسمُ مؤلّف")
        if self.rejection_ground is not None:
            _require_text(self.rejection_ground, "علّةُ الردّ")

    @property
    def is_rejected(self) -> bool:
        """أرُدَّ هذا الكتابُ بعلّةٍ مكتوبة؟"""
        return self.rejection_ground is not None


NAHW_WADIH_WORK: Final[ProposedWork] = ProposedWork(
    title="النحو الواضح في قواعد اللغة العربية",
    authors=("علي الجارم", "مصطفى أمين"),
    rejection_ground=None,
)
"""الكتابُ المقصودُ بهذا الفحص، لا غيرُه."""


MAANI_AL_NAHW_REJECTED_WORK: Final[ProposedWork] = ProposedWork(
    title="معاني النحو",
    authors=("فاضل صالح السامرائي",),
    rejection_ground=(
        "نُظر فيه لهذا الغرض فرُدَّ: نثرٌ في تعليل المعنى، لا عمودُ قواعدَ "
        "مرقّمةٍ يُقابَل بعقدِ قرار؛ فلا يقوم مقامَ النحو الواضح ولا يُبدَّل به"
    ),
)
"""كتابٌ مغايرٌ نُظر فيه ورُدَّ؛ ويُحفَظ ردُّه بعلّته لئلّا يُبدَّل بالمقصود."""


# --- رتبُ ما جرى في الفحص: بلوغٌ، وإذنٌ، وطبقةُ نصّ، وبنية ---------------------


class SourceReachability(Enum):
    """أفُتِح الموضعُ من هذه البيئة أم لم يُبلَغ؟ ولا ثالثَ يُقرأ نفيًا."""

    OPENED_IN_THIS_SANDBOX = "opened_in_this_sandbox"
    UNREACHABLE_FROM_THIS_SANDBOX = "unreachable_from_this_sandbox"

    @property
    def was_opened(self) -> bool:
        """أقُرِئت صفحتُه فعلًا في هذا التشغيل؟"""
        return self is SourceReachability.OPENED_IN_THIS_SANDBOX


class LicenceStanding(Enum):
    """رتبةُ الإذن؛ وواحدةٌ منها وحدَها تفكّ الحجر، ولا عضوَ فيها بمعنى «غالبًا مباح»."""

    EXPLICIT_OPEN_LICENCE_NAMED = "explicit_open_licence_named"
    RIGHTS_RESERVED_STATED = "rights_reserved_stated"
    NO_STATEMENT_FOUND = "no_statement_found"
    NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED = "not_read_because_page_was_not_opened"

    @property
    def unblocks(self) -> bool:
        """أتكفي هذه الرتبةُ وحدَها لتجاوز سؤال الإذن؟"""
        return self is LicenceStanding.EXPLICIT_OPEN_LICENCE_NAMED


class TextLayerStanding(Enum):
    """جنسُ ما وُجد من نصّ: مقروءٌ آليًّا، أم ناتجُ تعرّفٍ ضوئيّ، أم لا نصّ."""

    MACHINE_READABLE_TEXT_LAYER_FOUND = "machine_readable_text_layer_found"
    OCR_OVER_SCAN = "ocr_over_scan"
    NO_TEXT_LAYER_FOUND = "no_text_layer_found"
    NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED = (
        "not_inspected_because_page_was_not_opened"
    )

    @property
    def is_machine_readable(self) -> bool:
        """أهو نصٌّ مقروءٌ آليًّا لا ناتجَ تعرّفٍ ضوئيٍّ على صورة؟"""
        return self is TextLayerStanding.MACHINE_READABLE_TEXT_LAYER_FOUND


class StructureStanding(Enum):
    """رتبةُ البنية؛ وثالثتُها امتناعٌ عن النظر لا حكمٌ على المنظور فيه."""

    NUMBERED_RULE_STRUCTURE_EXTRACTABLE = "numbered_rule_structure_extractable"
    PROSE_OR_SCAN_ONLY = "prose_or_scan_only"
    NOT_INSPECTED_LICENCE_BLOCKED_FIRST = "not_inspected_licence_blocked_first"


class GrammarSourceProbeOutcome(Enum):
    """القيمةُ المُسمّاةُ التي ينتهي إليها الفحص؛ ثلاثةٌ لا رابعَ لها.

    ولا عضوَ فيها بمعنى «صالحٌ جزئيًّا»: المنزلةُ الوسطى المريحةُ غيرُ قابلةٍ
    للقول هنا لا مكروهةً فحسب، على منوال `GapClosureOutcome`.
    """

    SOURCE_AVAILABLE_STRUCTURE_EXTRACTABLE = "source_available_structure_extractable"
    SOURCE_AVAILABLE_STRUCTURE_NOT_EXTRACTABLE = (
        "source_available_structure_not_extractable"
    )
    SOURCE_LICENCE_UNRESOLVED = "source_licence_unresolved"


# --- المُرشَّح: ما فُتِح، لا ما كان يُرجى أن يُفتَح -----------------------------


@dataclass(frozen=True, slots=True)
class GrammarSourceCandidate:
    """موضعٌ طُلب فيه الكتاب، مُسجَّلٌ بما جرى عليه لا بما يُظَنّ به."""

    work: ProposedWork
    mirror: str
    requested_url: str
    declared_print_edition: str | None
    reachability: SourceReachability
    licence_standing: LicenceStanding
    verbatim_licence_text: str | None
    text_layer: TextLayerStanding
    numbered_rule_headings_found: bool | None
    note: str
    sha256: str | None = None
    byte_length: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.work, ProposedWork):
            raise GrammarSourceProbeError("المُرشَّحُ يُسمّي كتابَه عضوًا في `ProposedWork`.")
        if self.work.is_rejected:
            raise GrammarSourceProbeError(
                "كتابٌ مردودٌ بعلّته لا يُفحَص مكانَ المقصود؛ "
                + MAANI_AL_NAHW_IS_NOT_NAHW_WADIH
            )
        _require_text(self.mirror, "الموضعُ المقصود")
        _require_text(self.requested_url, "الرابطُ المطلوب")
        _require_text(self.note, "بيانُ ما جرى")
        if self.declared_print_edition is not None:
            _require_text(self.declared_print_edition, "الطبعةُ المُصرَّح بها")
        for value, label in (
            (self.reachability, SourceReachability),
            (self.licence_standing, LicenceStanding),
            (self.text_layer, TextLayerStanding),
        ):
            if not isinstance(value, label):
                raise GrammarSourceProbeError(f"رتبةُ المُرشَّح عضوٌ في `{label.__name__}`.")
        if not self.reachability.was_opened:
            if (
                self.licence_standing
                is not LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED
            ):
                raise GrammarSourceProbeError(
                    "صفحةٌ لم تُفتَح لا تُقرأ رخصتُها ولا يُقرأ سكوتُها؛ "
                    "فرتبةُ إذنها `NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED`."
                )
            if (
                self.text_layer
                is not TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED
            ):
                raise GrammarSourceProbeError("صفحةٌ لم تُفتَح لا يُوصَف ما فيها من نصّ.")
            if self.numbered_rule_headings_found is not None:
                raise GrammarSourceProbeError(
                    "عناوينُ قواعدَ مُثبَتةٌ أو منفيّةٌ في صفحةٍ لم تُفتَح دعوى بلا نظر."
                )
            if self.sha256 is not None or self.byte_length is not None:
                raise GrammarSourceProbeError(
                    "بصمةٌ لملفٍّ لم يُفتَح إسنادٌ إلى ما لم يُقرأ؛ "
                    "ولا تُكتَب بصمةٌ إلّا عن بايتاتٍ فُتِحت."
                )
        else:
            if (
                self.licence_standing
                is LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED
            ):
                raise GrammarSourceProbeError(
                    "صفحةٌ فُتِحت يُصرَّح بما قُرئ فيها من إذنٍ أو بخلوّها منه."
                )
            if (
                self.text_layer
                is TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED
            ):
                raise GrammarSourceProbeError("صفحةٌ فُتِحت يُصرَّح بجنس ما فيها من نصّ.")
        if self.licence_standing in (
            LicenceStanding.EXPLICIT_OPEN_LICENCE_NAMED,
            LicenceStanding.RIGHTS_RESERVED_STATED,
        ):
            if self.verbatim_licence_text is None:
                raise GrammarSourceProbeError(
                    "رتبةُ إذنٍ مبنيّةٌ على نصٍّ مقروءٍ تُودِع نصَّه بحروفه."
                )
            _require_text(self.verbatim_licence_text, "نصُّ الرخصة بحروفه")
        elif self.verbatim_licence_text is not None:
            raise GrammarSourceProbeError(
                "نصُّ رخصةٍ مكتوبٌ مع رتبةٍ تقول إنّه لم يُقرَأ تناقضٌ في السجلّ."
            )
        if (self.sha256 is None) != (self.byte_length is None):
            raise GrammarSourceProbeError(
                "البصمةُ والطولُ يقومان معًا؛ وبصمةٌ بلا طولٍ نصفُ تعريف."
            )
        if self.sha256 is not None:
            if len(self.sha256) != 64 or any(
                character not in "0123456789abcdef" for character in self.sha256
            ):
                raise GrammarSourceProbeError(
                    "البصمةُ `sha256` بأربعةٍ وستين محرفًا سُدَاسيَّ العشر."
                )
        if self.byte_length is not None and self.byte_length < 1:
            raise GrammarSourceProbeError("طولُ ملفٍّ فُتِح عددٌ صحيحٌ موجب.")
        if (
            self.numbered_rule_headings_found is not None
            and self.text_layer is TextLayerStanding.NO_TEXT_LAYER_FOUND
        ):
            raise GrammarSourceProbeError(
                "بنيةٌ مُثبَتةٌ أو منفيّةٌ حيث لا نصّ أصلًا دعوى بلا موضوع."
            )

    @property
    def structure_is_mechanically_extractable(self) -> bool:
        """أتُستخرَج بنيةُ القواعد آليًّا من هذا الموضع كما قُرئ؟

        وناتجُ التعرّف الضوئيّ لا يُعَدّ بنيةً مهما بدا نصًّا: تقطيعُه أثرُ
        تعرّفٍ على صفحةٍ مصوّرة لا أثرُ بنيةِ الكتاب
        (`OCR_OVER_SCAN_IS_NEITHER_EDITION_NOR_TRANSCRIPTION`).
        """
        return (
            self.text_layer.is_machine_readable
            and self.numbered_rule_headings_found is True
        )


# --- الحصيلة: مُشتقّةٌ من الصفوف، لا مكتوبةٌ ثابتًا ------------------------------


@dataclass(frozen=True, slots=True)
class GrammarSourceProbeReport:
    """حصيلةُ الفحص: قيمتُها المُسمّاة، ورتبةُ البنية، وعلّةُ الحكم.

    ولا حقلَ فيها بمعنى نجاحٍ أو رسوب: الحكمُ على قابلية المصدر لا على أحد.
    """

    outcome: GrammarSourceProbeOutcome
    structure_standing: StructureStanding
    licence_unblocked_candidates: tuple[GrammarSourceCandidate, ...]
    reason: str

    def __post_init__(self) -> None:
        _require_text(self.reason, "علّةُ الحكم")
        if not isinstance(self.outcome, GrammarSourceProbeOutcome):
            raise GrammarSourceProbeError("الحصيلةُ عضوٌ في `GrammarSourceProbeOutcome`.")
        licence_unresolved = (
            self.outcome is GrammarSourceProbeOutcome.SOURCE_LICENCE_UNRESOLVED
        )
        blocked_structure = (
            self.structure_standing
            is StructureStanding.NOT_INSPECTED_LICENCE_BLOCKED_FIRST
        )
        if licence_unresolved != blocked_structure:
            raise GrammarSourceProbeError(
                "الإذنُ يسبق البنية: إن لم يُحسَم الإذنُ لم تُقرَأ البنية، "
                "وإن حُسم لم تبقَ البنيةُ ممتنعةً عن النظر."
            )
        if licence_unresolved and self.licence_unblocked_candidates:
            raise GrammarSourceProbeError(
                "لا يجتمع إذنٌ غيرُ محسومٍ مع مُرشَّحٍ فُكَّ عنه الحجر."
            )


def derive_probe_outcome(
    candidates: tuple[GrammarSourceCandidate, ...],
) -> GrammarSourceProbeReport:
    """اشتقّ الحصيلةَ من الصفوف المُسجَّلة: الإذنُ أوّلًا، ثمّ البنية.

    ولا تُقرأ البنيةُ ما لم يُفَكَّ الحجر: مُرشَّحٌ لم يبلغ رخصةً صريحةً مفتوحة
    لا يُنظَر في بنيته، فلا تُروى بنيةٌ مستخرَجةٌ فوق نصٍّ مجهولِ الإذن.
    """
    if not candidates:
        raise GrammarSourceProbeError("فحصٌ بلا موضعٍ مطلوبٍ واحدٍ ليس فحصًا.")
    for candidate in candidates:
        if candidate.work != NAHW_WADIH_WORK:
            raise GrammarSourceProbeError(
                "هذا الفحصُ للنحو الواضح وحدَه؛ " + MAANI_AL_NAHW_IS_NOT_NAHW_WADIH
            )
    unblocked = tuple(
        candidate for candidate in candidates if candidate.licence_standing.unblocks
    )
    if not unblocked:
        unopened = sum(
            1 for candidate in candidates if not candidate.reachability.was_opened
        )
        return GrammarSourceProbeReport(
            outcome=GrammarSourceProbeOutcome.SOURCE_LICENCE_UNRESOLVED,
            structure_standing=StructureStanding.NOT_INSPECTED_LICENCE_BLOCKED_FIRST,
            licence_unblocked_candidates=(),
            reason=(
                f"طُلب {len(candidates)} موضعًا، ولم يبلغ واحدٌ منها رخصةً صريحةً "
                f"مفتوحة؛ ومنها {unopened} لم تُفتَح من هذه البيئة أصلًا. "
                "وسكوتُ الرخصة ليس إذنًا، فلم تُقرَأ بنيةُ الكتاب ولم تُنسَخ بايتة."
            ),
        )
    extractable = tuple(
        candidate
        for candidate in unblocked
        if candidate.structure_is_mechanically_extractable
    )
    if extractable:
        return GrammarSourceProbeReport(
            outcome=(GrammarSourceProbeOutcome.SOURCE_AVAILABLE_STRUCTURE_EXTRACTABLE),
            structure_standing=StructureStanding.NUMBERED_RULE_STRUCTURE_EXTRACTABLE,
            licence_unblocked_candidates=unblocked,
            reason=(
                f"بلغ {len(unblocked)} موضعًا رخصةً صريحةً مفتوحة، ووُجدت في "
                f"{len(extractable)} منها عناوينُ قواعدَ مرقّمةٌ في نصٍّ مقروءٍ "
                "آليًّا. والاستخراجُ بعد ذلك عملٌ آخرُ لم يُبدَأ هنا."
            ),
        )
    return GrammarSourceProbeReport(
        outcome=(GrammarSourceProbeOutcome.SOURCE_AVAILABLE_STRUCTURE_NOT_EXTRACTABLE),
        structure_standing=StructureStanding.PROSE_OR_SCAN_ONLY,
        licence_unblocked_candidates=unblocked,
        reason=(
            f"بلغ {len(unblocked)} موضعًا رخصةً صريحةً مفتوحة، ولم توجد فيها "
            "بنيةُ قواعدَ مرقّمةٌ مستخرَجة: نثرٌ متّصلٌ أو صفحاتٌ مصوّرةٌ وما "
            "يُشتقّ منها بالتعرّف الضوئيّ. فالتقطيعُ عملُ يدٍ لا عملُ آلة."
        ),
    )


# --- ما جرى فعلًا: خمسةُ مواضعَ طُلبت، ولم يُفتَح منها شيء -----------------------


_NOT_OPENED_NOTE: Final[str] = (
    "طُلب الرابطُ من هذه البيئة فلم يُبلَغ المضيفُ أصلًا (تعذّر حلُّ اسم "
    "النطاق)، فلم تُقرَأ صفحةٌ ولا رخصةٌ ولا نصّ"
)


PROBED_CANDIDATES: Final[tuple[GrammarSourceCandidate, ...]] = (
    GrammarSourceCandidate(
        work=NAHW_WADIH_WORK,
        mirror="shamela.ws",
        requested_url="https://shamela.ws/book/10018",
        declared_print_edition=None,
        reachability=SourceReachability.UNREACHABLE_FROM_THIS_SANDBOX,
        licence_standing=LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED,
        verbatim_licence_text=None,
        text_layer=TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED,
        numbered_rule_headings_found=None,
        note="صفحةُ الكتاب في المكتبة الشاملة. " + _NOT_OPENED_NOTE,
    ),
    GrammarSourceCandidate(
        work=NAHW_WADIH_WORK,
        mirror="shamela.org",
        requested_url="https://shamela.org/book/10018",
        declared_print_edition=None,
        reachability=SourceReachability.UNREACHABLE_FROM_THIS_SANDBOX,
        licence_standing=LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED,
        verbatim_licence_text=None,
        text_layer=TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED,
        numbered_rule_headings_found=None,
        note="الموضعُ الثاني للشاملة. " + _NOT_OPENED_NOTE,
    ),
    GrammarSourceCandidate(
        work=NAHW_WADIH_WORK,
        mirror="ketabonline.com",
        requested_url="https://ketabonline.com/ar/books/253",
        declared_print_edition=None,
        reachability=SourceReachability.UNREACHABLE_FROM_THIS_SANDBOX,
        licence_standing=LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED,
        verbatim_licence_text=None,
        text_layer=TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED,
        numbered_rule_headings_found=None,
        note="جامعُ الكتب الإسلامية، نصٌّ مُصفَّح. " + _NOT_OPENED_NOTE,
    ),
    GrammarSourceCandidate(
        work=NAHW_WADIH_WORK,
        mirror="archive.org",
        requested_url="https://archive.org/metadata/20200227_20200227_0737",
        declared_print_edition=None,
        reachability=SourceReachability.UNREACHABLE_FROM_THIS_SANDBOX,
        licence_standing=LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED,
        verbatim_licence_text=None,
        text_layer=TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED,
        numbered_rule_headings_found=None,
        note=(
            "بياناتُ نسخةٍ مصوّرةٍ في الأرشيف، وطُلبت لأجل رتبة رخصتها لا "
            "لأجل بايتاتها. " + _NOT_OPENED_NOTE
        ),
    ),
    GrammarSourceCandidate(
        work=NAHW_WADIH_WORK,
        mirror="hindawi.org",
        requested_url="https://www.hindawi.org/books/",
        declared_print_edition=None,
        reachability=SourceReachability.UNREACHABLE_FROM_THIS_SANDBOX,
        licence_standing=LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED,
        verbatim_licence_text=None,
        text_layer=TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED,
        numbered_rule_headings_found=None,
        note=(
            "ناشرٌ يصرّح برخصةٍ مفتوحةٍ في كتبه، طُلب ليكون خلوُّه من الكتاب "
            "نفيًا مُسجَّلًا لا بابًا مسكوتًا عنه. " + _NOT_OPENED_NOTE
        ),
    ),
)
"""المواضعُ الخمسةُ المطلوبةُ بترتيب طلبها، وكلٌّ منها بما جرى عليه."""


def run_nahw_wadih_source_probe() -> GrammarSourceProbeReport:
    """أعِد اشتقاقَ حصيلة الفحص من الصفوف المُودَعة؛ مدخلٌ بلا وُسطاء."""
    return derive_probe_outcome(PROBED_CANDIDATES)


# --- ما لا يحسمه هذا الفحص، مُسمًّى ------------------------------------------


A_RULE_STATEMENT_IS_NOT_A_DECISION_PROCEDURE: Final[str] = (
    "A_RULE_STATEMENT_IS_NOT_A_DECISION_PROCEDURE: القاعدةُ المرقّمةُ في هذا "
    "الكتاب تقرير عمومٍ نحويٍّ بالنثر («الفاعل مرفوعٌ دائمًا»)، ولا تحمل "
    "الاختبارَ الخوارزميَّ الذي يُعرَف به أنّها تنطبق على تسلسلٍ من الرموز؛ "
    "فتحويلُ ٤٢١ تقريرًا إلى شجرة قرارٍ عملٌ من جنسٍ آخرَ وأكبرَ من إيداع بنية "
    "الكتاب، والخطوةُ صفر هنا تفحص صلاحيةَ المصدر لا قابليةَ بناء الشجرة منه"
)

A_DIGEST_IS_NOT_A_PERMISSION: Final[str] = (
    "A_DIGEST_IS_NOT_A_PERMISSION: بصمةُ ملفٍّ محفوظِ الحقوق إحالةٌ إليه لا "
    "إذنٌ فيه، وهي مع ذلك مقبولةٌ تثبيتًا كما في شاهد المدوَّنة الإعرابية؛ "
    "أمّا استخراجُ بنيته — ولو «العناوينَ وحدَها» — فمُشتَقٌّ من النصّ لا بصمةٌ "
    "عنه، ولا يُودَع بغير إذنٍ مُسمًّى"
)

OCR_OVER_SCAN_IS_NEITHER_EDITION_NOR_TRANSCRIPTION: Final[str] = (
    "OCR_OVER_SCAN_IS_NEITHER_EDITION_NOR_TRANSCRIPTION: ناتجُ التعرّف "
    "الضوئيِّ على صفحاتٍ مصوّرةٍ جنسٌ ثالثٌ دون الطبعة ودون النقل المكتوب في "
    "الشجرة؛ وتقطيعُه أثرُ تعرّفٍ على صورةٍ لا أثرُ بنيةِ الكتاب، فلا يُقرأ "
    "بنيةً مستخرَجةً مهما بدا نصًّا"
)

RIGHTS_RESERVED_IS_A_STRONGER_BAR_THAN_SILENCE: Final[str] = (
    "RIGHTS_RESERVED_IS_A_STRONGER_BAR_THAN_SILENCE: «الملكية الفكرية محفوظة "
    "لأصحابها» نصٌّ مانعٌ مقروء، وسكوتُ الصفحة عن الرخصة منعٌ أيضًا لأنّ "
    "السكوتَ ليس إذنًا؛ فكلاهما يحجب، والأوّلُ أوكدُ لا أهون"
)

SECOND_HAND_LICENCE_REPORT_IS_NOT_A_READ_PAGE: Final[str] = (
    "SECOND_HAND_LICENCE_REPORT_IS_NOT_A_READ_PAGE: ما وصل عن رخص هذه "
    "المواضع وصل خبرًا من محرّك بحثٍ لا من صفحةٍ فُتِحت؛ فلا يُكتَب نصًّا "
    "مقروءًا بحروفه، ورتبةُ كلِّ موضعٍ لم يُفتَح `NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED`"
)

MAANI_AL_NAHW_IS_NOT_NAHW_WADIH: Final[str] = (
    "MAANI_AL_NAHW_IS_NOT_NAHW_WADIH: «معاني النحو» للسامرّائي كتابٌ آخرُ "
    "نُظر فيه لهذا الغرض فرُدَّ لأنّه نثرٌ في تعليل المعنى لا عمودُ قواعدَ "
    "مرقّمة؛ ورُدُّه محفوظٌ بعلّته هنا ليُمنَع إبدالُه بالمقصود آليًّا لا ذكرًا"
)

PUBLIC_DOMAIN_BY_AGE_IS_A_JURISDICTIONAL_QUESTION: Final[str] = (
    "PUBLIC_DOMAIN_BY_AGE_IS_A_JURISDICTIONAL_QUESTION: قد يكون متنُ الكتاب "
    "قد آل إلى المِلك العامّ بمُضيّ المدّة في بعض الولايات دون بعض، ويبقى "
    "لطبعةٍ حديثةٍ بعينها جهدُها المحميّ؛ وهذا سؤالٌ قانونيٌّ لا يُحسَم في هذه "
    "الشجرة ولا يُقرأ إذنًا، وهو مُسجَّلٌ مفتوحًا لا مطويًّا"
)

THIS_PROBE_IS_NOT_A_GATE: Final[str] = (
    "THIS_PROBE_IS_NOT_A_GATE: هذه الوحدةُ تسجيلٌ لفحصٍ جرى، لا سلطة: لا "
    "تسجيلَ مسبقًا، ولا استخراجَ قاعدةٍ واحدة، ولا عقدةَ قرار، ولا صفَّ خطوةٍ "
    "في `DirectCertaintyStep`، ولا ولادةَ ولا تجميد، ولا تستورد من `kernel/` "
    "شيئًا ولا تقرؤها وحدةٌ فيه"
)

NAHW_WADIH_PROBE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_RULE_STATEMENT_IS_NOT_A_DECISION_PROCEDURE": (
        A_RULE_STATEMENT_IS_NOT_A_DECISION_PROCEDURE
    ),
    "A_DIGEST_IS_NOT_A_PERMISSION": A_DIGEST_IS_NOT_A_PERMISSION,
    "OCR_OVER_SCAN_IS_NEITHER_EDITION_NOR_TRANSCRIPTION": (
        OCR_OVER_SCAN_IS_NEITHER_EDITION_NOR_TRANSCRIPTION
    ),
    "RIGHTS_RESERVED_IS_A_STRONGER_BAR_THAN_SILENCE": (
        RIGHTS_RESERVED_IS_A_STRONGER_BAR_THAN_SILENCE
    ),
    "SECOND_HAND_LICENCE_REPORT_IS_NOT_A_READ_PAGE": (
        SECOND_HAND_LICENCE_REPORT_IS_NOT_A_READ_PAGE
    ),
    "MAANI_AL_NAHW_IS_NOT_NAHW_WADIH": MAANI_AL_NAHW_IS_NOT_NAHW_WADIH,
    "PUBLIC_DOMAIN_BY_AGE_IS_A_JURISDICTIONAL_QUESTION": (
        PUBLIC_DOMAIN_BY_AGE_IS_A_JURISDICTIONAL_QUESTION
    ),
    "THIS_PROBE_IS_NOT_A_GATE": THIS_PROBE_IS_NOT_A_GATE,
}
"""ما لا يحسمه هذا الفحص، مُسمًّى هنا لا متروكًا ليُفترَض."""
