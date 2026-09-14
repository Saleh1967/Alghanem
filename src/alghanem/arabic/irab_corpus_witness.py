"""شاهدٌ إعرابيٌّ خارجيّ: مدوَّنةٌ مُوسَّمةٌ بأيدي غيرنا، لا نصٌّ من تأليفنا.

كلُّ ما سبق في هذه الشجرة من قياسٍ عربيٍّ كان إمّا على نصٍّ مُفرَّغٍ فيها
(`fatiha_source_text`)، وإمّا على أرقامٍ مُودَعةٍ بلا أنبوبٍ يُعيد اشتقاقها
(`distributional_probe_report`). وكلاهما يترك البابَ الذي أُغلِق هنا مفتوحًا:
**من صنع شواهدَه صنع جوابَه**. فالحكمُ الإعرابيُّ الذي نُقاس عليه هنا مُوسَّمٌ
كلمةً كلمةً في مدوَّنةٍ خارجيةٍ مُسمّاةٍ بمؤلّفها ورخصتها وبصمتها، وُسِم قبل أن
يُطرَح سؤالُنا هذا ولا يعلم به.

`WITNESS_BYTES_ARE_NOT_VENDORED`: لا تُنسَخ بايتاتُ المدوَّنة إلى هذه الشجرة.
ورخصتُها تُجيز النسخ الحرفيَّ وحده وتمنع التغيير، ورخصةُ النصِّ العثمانيِّ
المُضمَّن فيها `CC BY-ND`؛ وهاتان رخصتان غيرُ رخصةِ هذا المستودع. فالمُودَعُ هنا
**بصمةٌ وطولُ بايتاتٍ ومسارٌ مُصرَّح**، وبهما يُعيد حائزُ البايتات نفسِها اشتقاقَ
كلِّ رقمٍ في `irab_case_readout` حرفًا بحرف، ولا يُعيد اشتقاقَه من لا يحوزها.

`ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY`: تشترط المدوَّنةُ التصريحَ بمصدرها
والإحالةَ إلى موضعها، فالإسنادُ هنا شرطُ استعمالٍ منصوصٌ عليه لا لطفَ عبارة.

`A_MIRROR_IS_NOT_THE_UPSTREAM`: البايتاتُ المقيسةُ أُخِذت من مرآةٍ في مستودعٍ
عامّ، والمنبعُ المُعلَنُ موضعٌ آخر. فالمُصرَّحُ به هنا **ما قِيس**، لا ما كان
يُرجى أن يُقاس؛ ومن بدّل المرآةَ بالمنبع أسنَد بصمةً إلى ملفٍّ لم يفتحه.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = [
    "ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE",
    "A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE",
    "IRAB_CORPUS_WITNESS_NAMED_RESIDUALS",
    "QURANIC_ARABIC_CORPUS_WITNESS",
    "WITNESS_BYTES_ARE_NOT_VENDORED_NOTE",
    "IrabCorpusWitness",
    "IrabCorpusWitnessError",
]


class IrabCorpusWitnessError(ValueError):
    """تُرفَع حين يُوصَف شاهدٌ خارجيٌّ وصفًا لا يُعاد به اشتقاقُ قياسه."""


WITNESS_BYTES_ARE_NOT_VENDORED_NOTE: Final[str] = (
    "WitnessBytesAreNotVendored: بايتاتُ المدوَّنة لا تُنسَخ إلى هذه الشجرة؛ "
    "رخصتُها ورخصةُ النصِّ المُضمَّن فيها غيرُ رخصةِ هذا المستودع، والمُودَعُ "
    "بصمةٌ وطولٌ ومسارٌ يُعيد بها حائزُ البايتات نفسِها اشتقاقَ كلِّ رقم"
)

ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE: Final[str] = (
    "AttributionIsAConditionNotACourtesy: تشترط المدوَّنةُ التصريحَ بمصدرها "
    "والإحالةَ إلى موضعها؛ فالإسنادُ شرطُ استعمالٍ منصوصٌ عليه لا لطفَ عبارة"
)

A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE: Final[str] = (
    "AMirrorIsNotTheUpstream: البايتاتُ المقيسةُ أُخِذت من مرآةٍ عامّةٍ لا من "
    "المنبع المُعلَن؛ فالبصمةُ بصمةُ ما فُتِح، ومن أسنَدها إلى المنبع أسنَد "
    "بصمةً إلى ملفٍّ لم يقرأه"
)

IRAB_CORPUS_WITNESS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "WitnessBytesAreNotVendored": WITNESS_BYTES_ARE_NOT_VENDORED_NOTE,
    "AttributionIsAConditionNotACourtesy": (
        ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE
    ),
    "AMirrorIsNotTheUpstream": A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE,
}


def _require_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise IrabCorpusWitnessError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
    return value


@dataclass(frozen=True, slots=True)
class IrabCorpusWitness:
    """مدوَّنةٌ إعرابيةٌ خارجيةٌ مُسمّاةٌ ببصمتها وطولها ورخصتها وشرط إسنادها."""

    corpus: str
    version: str
    upstream: str
    measured_mirror: str
    measured_path: str
    sha256: str
    byte_length: int
    licenses: tuple[str, ...]
    required_attribution_links: tuple[str, ...]
    attribution_requirement: str
    annotation_note: str

    def __post_init__(self) -> None:
        _require_text(self.corpus, "اسمُ المدوَّنة")
        _require_text(self.version, "إصدارُ المدوَّنة")
        _require_text(self.upstream, "منبعُ المدوَّنة")
        _require_text(self.measured_mirror, "المرآةُ المقيسة")
        _require_text(self.measured_path, "مسارُ الملفّ المقيس")
        _require_text(self.sha256, "بصمةُ الملفّ المقيس")
        if len(self.sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.sha256
        ):
            raise IrabCorpusWitnessError(
                "بصمةُ الملفّ المقيس `sha256` بأربعةٍ وستين محرفًا سُدَاسيَّ "
                "العشر؛ وبصمةٌ ناقصةٌ لا يُعاد بها اشتقاقُ قياس."
            )
        if not isinstance(self.byte_length, int) or self.byte_length < 1:
            raise IrabCorpusWitnessError(
                "طولُ الملفّ المقيس عددٌ صحيحٌ موجب؛ وبصمةٌ بلا طولٍ نصفُ تعريف."
            )
        if not self.licenses:
            raise IrabCorpusWitnessError(
                "مدوَّنةٌ خارجيةٌ بلا رخصةٍ مُسمّاةٍ لا تُستعمَل؛ وسكوتُ الرخصة " "ليس إذنًا."
            )
        seen: set[str] = set()
        for license_name in self.licenses:
            _require_text(license_name, "رخصةٌ مُسمّاة")
            if license_name in seen:
                raise IrabCorpusWitnessError(
                    f"رخصةٌ مكرّرة: {license_name}؛ والتكرارُ يُوهِم تعدُّدَ أذون."
                )
            seen.add(license_name)
        if not self.required_attribution_links:
            raise IrabCorpusWitnessError(
                "شرطُ الإسناد يُسمّي مواضعَ الإحالة بأعيانها؛ وشرطٌ بلا موضعٍ "
                "مُعلَنٍ لا يُتحقَّق من الوفاء به."
            )
        links: set[str] = set()
        for link in self.required_attribution_links:
            _require_text(link, "موضعُ إحالةٍ مشروط")
            if link in links:
                raise IrabCorpusWitnessError(
                    f"موضعُ إحالةٍ مكرّر: {link}؛ والتكرارُ يُوهِم تعدُّدَ شروط."
                )
            links.add(link)
        _require_text(self.attribution_requirement, "شرطُ الإسناد")
        _require_text(self.annotation_note, "بيانُ التوسيم")


QURANIC_ARABIC_CORPUS_WITNESS: Final[IrabCorpusWitness] = IrabCorpusWitness(
    corpus="Quranic Arabic Corpus (morphology)",
    version="0.4",
    upstream="http://corpus.quran.com/download",
    measured_mirror="raw.githubusercontent.com/alstat/QuranTree.jl",
    measured_path="data/quranic-corpus-morphology-0.4.txt",
    sha256="a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46",
    byte_length=6_309_503,
    licenses=(
        "GNU General Public License (Quranic Arabic Corpus, © 2011 Kais Dukes)",
        "Creative Commons BY-ND 3.0 Unported (Tanzil Quran Text, Uthmani 1.0.2)",
    ),
    required_attribution_links=(
        "http://corpus.quran.com",
        "http://tanzil.info",
    ),
    attribution_requirement=(
        "تشترط ترويسةُ الملفّ التصريحَ بالمصدر (Quranic Arabic Corpus) "
        "والإحالةَ إلى http://corpus.quran.com، وكذلك التصريحَ بمصدر النصِّ "
        "(Tanzil.info) والإحالةَ إلى http://tanzil.info؛ وتمنع الرخصتان "
        "تغييرَ الملفّ، فلم يُغيَّر ولم يُنسَخ إلى هذه الشجرة. "
        + ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE
    ),
    annotation_note=(
        "الملفُّ سطرٌ لكلِّ مقطعٍ صرفيّ: موضعُه `(سورة:آية:كلمة:مقطع)`، وصورتُه "
        "بترميز Buckwalter، ووَسْمُه، وسماتُه. والحالةُ الإعرابيةُ `NOM` و`ACC` "
        "و`GEN` مُوسَّمةٌ في السمات بأيدي واضعي المدوَّنة قبل سؤالِ هذه الشجرة "
        "ولا علمَ لهم به. وليس في هذا الملفّ وظائفُ نحويةٌ (فاعل/مفعول به)؛ "
        "تلك في شجرة الإعراب النحويّ لا في ملفّ الصرف، ولم تُقَس هنا. "
        + A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE
    ),
)
