"""سجلُّ الوحدات: لكلّ وحدةٍ موضعُها في الشجرة كلِّها — ملفُّ Lean، وجدولُ المطابقة، وأداةُ الفهرس، واختبارُها.

كان إدخالُ وحدةٍ يمسّ عشرةَ ملفّاتٍ باليد (`Slge.lean`، `Audit.lean`، `Main.lean`، `guard.py`، `order.py`،
`status.py`، `gen_lean_index.py`، `ci.yml`، `CLAUDE.md`، `test_conformance.py`). هذا السجلُّ مصدرٌ واحدٌ
لتلك المواضع: `tools/check_manifest.py` يفحص أنّ كلَّ وحدةٍ موصولةٌ في كلّ موضع، وCI يأخذ قوائمَه من هنا
لا من سطرٍ مكتوبٍ باليد. وصفيٌّ لا يبني (كـ`order` و`status`).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = ["CERTIFICATES_DIGEST", "DEPOSITS", "DEPOSIT_KINDS", "GATE_REV", "MODULES", "Deposit",
           "Module", "index_tools", "lean_files", "readers_under_law", "tables"]


@dataclass(frozen=True, slots=True)
class Module:
    """وحدةٌ بايثونيّة وما يقابلها: ملفّاتُ Lean (بلا `.lean`)، جداولُ `slge-table`، أداةُ الفهرس،
    والاختبار."""

    name: str
    lean: tuple[str, ...] = ()
    tables: tuple[str, ...] = ()
    index: str | None = None
    test: str | None = None
    law: bool = False
    """قارئٌ تحت قانون القارئ (CLAUDE.md): بوّابةٌ في `gates.LADDER`، مقيسٌ على مودَع المصحف قبل أيّ
    شريحة، ولا يطابق قالبًا إلّا عبر `jidh.on_template_mod`."""


def _m(name: str, index: bool = True) -> Module:
    """بابٌ قياسيّ: `Name.lean`، جدولُ `name`، `gen_name_index.py`، `test_name.py`."""

    return Module(name, (name.capitalize(),), (name,), f"gen_{name}_index.py" if index else None,
                  f"test_{name}.py")


MODULES: Final[tuple[Module, ...]] = (
    # الأساس: البتّات والمدخل والتسلسل — Lean باسمٍ غيرِ اسم الوحدة
    Module("cells", ("Bridge", "Consistency"), ("bridge", "counts", "folds"), None,
           "test_cells.py"),
    Module("entry", (), (), None, "test_entry.py"),
    Module("stream", ("Sequence",), ("sequence",), None, None),
    Module("phonology", (), (), None, "test_phonology.py"),
    Module("semantics", ("Rasm",), ("rasm",), None, "test_semantics.py"),
    Module("categories", ("Categories",), ("categories",), None, None),
    Module("nazm", (), (), None, "test_nazm.py"),
    Module("grant", ("Grant",), (), None, "test_grant.py"),
    Module("knowledge", ("Ghazali",), ("ghazali",), None, "test_knowledge.py"),
    Module("rank", ("Rank",), ("rank",), None, "test_rank.py"),
    Module("learning", (), (), None, "test_learning.py"),
    Module("answer", (), (), None, "test_answer.py"),
    # الأبواب: Lean باسم الوحدة، جدولٌ باسمها، فهرسٌ واختبار
    _m("wazn", index=False), _m("shabaka", index=False), _m("khamsa", index=False),
    _m("afal", index=False), _m("rawabit"), _m("damair"), _m("ishara"), _m("istifham"), _m("nida"),
    _m("zuruf"), _m("zaman"), _m("adad"), _m("marifa"), _m("sarf"), _m("tawabi"), _m("nawasikh"),
    _m("jazm"), _m("mansubat"), _m("majrurat"), _m("wasl"), _m("ism"), _m("fil"), _m("huruf"),
    _m("jumla"), _m("filiyya"), _m("shibh"), _m("nisab"), _m("talil"), _m("maqam"), _m("jiha"),
    _m("naat"), _m("uslub"), _m("talab"), _m("kulli"), _m("wad"), _m("tabayun"),
    Module("madd", ("Madd",), ("madd",), "gen_madd_index.py", "test_madd.py", law=True),
    Module("ilal", ("Ilal",), ("ilal",), "gen_ilal_index.py", "test_ilal.py", law=True),
    Module("jidh", ("Jidh",), ("jidh",), "gen_jidh_index.py", "test_jidh.py", law=True),
    Module("maqayis", ("Maqayis", "MaqayisTable"), ("maqayis",), "gen_maqayis_index.py",
           "test_maqayis.py", law=True),
    Module("maqayis_table", (), (), None, "test_maqayis.py"),  # مولَّدٌ من المودَع
    Module("abniya", ("Abniya", "AbniyaTable"), ("abniya",), "gen_abniya_index.py",
           "test_abniya.py"),
    Module("abniya_table", (), (), None, "test_abniya.py"),  # مولَّدٌ من المودَع
    Module("adawat", ("Adawat",), ("adawat",), "gen_adawat_index.py", "test_adawat.py", law=True),
    Module("wujud", ("Wujud", "WujudTable"), ("wujud",), "gen_wujud_index.py", "test_wujud.py",
           law=True),
    Module("wujud_table", (), (), None, "test_wujud.py"),  # مولَّدٌ من أبواب الأوزان
    Module("maani", ("Maani", "MaaniTable"), ("maani",), "gen_maani_index.py", "test_maani.py"),
    Module("maani_table", (), (), None, "test_maani.py"),  # مولَّدٌ من مودَع معاني الحروف
    Module("mukhassas", ("Mukhassas", "MukhassasTable"), ("mukhassas",), "gen_mukhassas_index.py",
           "test_mukhassas.py"),
    Module("mukhassas_table", (), (), None, "test_mukhassas.py"),  # مولَّدٌ من المخصّص المختوم
    Module("zawaid", ("Zawaid", "ZawaidTable"), ("zawaid",), "gen_zawaid_index.py",
           "test_zawaid.py"),
    Module("zawaid_table", (), (), None, "test_zawaid.py"),  # مولَّدٌ من الكتاب المختوم
    Module("makharij", ("Makharij", "MakharijTable"), ("makharij",), "gen_makharij_index.py",
           "test_makharij.py"),
    Module("makharij_table", (), (), None, "test_makharij.py"),  # مولَّدٌ من الكتاب المختوم
    Module("ilal_bab", ("IlalBab", "IlalBabTable"), ("ilal_bab",), "gen_ilal_bab_index.py",
           "test_ilal_bab.py"),
    Module("ilal_bab_table", (), (), None, "test_ilal_bab.py"),  # مولَّدٌ من الكتاب المختوم والمصحف
    Module("tawzi", ("Tawzi",), ("tawzi",), "gen_tawzi_index.py", "test_tawzi.py", law=True),
    Module("alam", ("Alam", "AlamTable"), ("alam",), "gen_alam_index.py", "test_alam.py",
           law=True),
    Module("alam_table", (), (), None, "test_alam.py"),  # مولَّدٌ من المودَع الموقَّع
    Module("sawabiq", ("Sawabiq", "SawabiqTable"), ("sawabiq",), "gen_sawabiq_index.py",
           "test_sawabiq.py", law=True),
    Module("sawabiq_table", (), (), None, "test_sawabiq.py"),  # مولَّدٌ من الكتاب المختوم والمصحف
    Module("hasm", ("Hasm", "HasmTable"), ("hasm",), "gen_hasm_index.py", "test_hasm.py"),
    Module("hasm_table", (), (), None, "test_hasm.py"),  # تكرارُ الجذور، مولَّدٌ من مودَع المصحف
    Module("pipeline", ("Pipeline", "PipelineTable"), ("pipeline",), "gen_pipeline_index.py",
           "test_pipeline.py"),
    Module("pipeline_table", (), (), None, "test_pipeline.py"),  # القمعُ أعدادًا، مولَّدٌ على MASAQ
    # الفهارسُ الجامعة (بلا وحدة)
    Module("bits", (), (), "gen_bits_index.py", "test_bits.py"),
    Module("nabhani", (), (), "gen_nabhani_index.py", "test_nabhani_index.py"),  # فهرسُ المطابقة
    Module("gates", (), (), None, "test_gates.py"),
)
"""كلُّ وحدةٍ حيّة (وصفيّةُ `order`/`status`/`guard`/`manifest` خارجَها) وما يقابلها."""


DEPOSIT_KINDS: Final[frozenset[str]] = frozenset(
    {"واقع مختوم", "وضع", "معلومات سابقة", "مرجع محجوب"})
"""أنواعُ المودَع الأربعة (دستورُ الوكيل، المادّة ١٢): **واقعٌ مختوم** (شهاداتُ النصّ كما نقلتها
البوّابة بلا تخمين)؛ **وضع** (اصطلاحُ العرب: لفظٌ ↔ معنًى ذهنيّ — المقاييس، الأبنية، الأوزان)؛
**معلومات سابقة** (حقائقُ الأشياء وخواصُّها — الأجناسُ والقابليّات؛ لا يُقاس بها ترخيصٌ ولا تُقاس
هي على مرجع ترخيص)؛ **مرجعٌ محجوب** (وسومٌ بشريّة يُقاس عليها ولا يُقرأ منها)."""


@dataclass(frozen=True, slots=True)
class Deposit:
    """ملفٌّ في `tests/data/` ونوعُه؛ لا مودَعَ بلا نوع (`tests/test_deposits.py`). المختومُ بإذن
    المالك يحمل بصمةَ محتواه (بعد فكّ الضغط) ورخصتَه (`tests/test_seals.py`)."""

    path: str
    kind: str
    note: str = ""
    sha256: str = ""
    licence: str = ""


GATE_REV: Final[str] = "072ef77d1f9945ec2fde100f9d32c9b56d0e609e"
"""إيداعُ بوّابة الغانم (`Saleh1967/Alghanem`، فرع `claude/official-gate`) الذي يُعاد منه توليدُ مودَع
الشهادات في CI (`tools/gen_certificates.py --check`): ما يقيسه SLGE هو ما تطبعه البوّابةُ على المدوّنة
المختومة بهذا الإيداع؛ أيُّ فرقٍ `DEPOSIT_DRIFTED_FROM_GATE`. يُرفع مع المودَع معًا لا أحدُهما وحدَه."""

CERTIFICATES_DIGEST: Final[str] = "4329fb9c3acaf5235c00da1e2373d9706c9739e488c05ab7d3cb377e69545144"
"""بصمةُ المودَع بصورته القانونيّة (JSON مرتّبَ المفاتيح بلا فراغ) كما طبعتها البوّابةُ على `GATE_REV`؛
يفحصها `tests/test_deposits.py` محلّيًّا بلا بوّابة، وCI يعيد التوليدَ من البوّابة نفسها."""

DEPOSITS: Final[tuple[Deposit, ...]] = (
    Deposit("corpus-certificates.json.gz", "واقع مختوم",
            "شهاداتُ المصحف كلِّه خاناتٍ وأعدادًا؛ بصمةُ المدوّنة فيه؛ يُعاد توليدُه من البوّابة على "
            "GATE_REV"),
    Deposit("maqayis-roots.json.gz", "وضع", "جذورُ مقاييس اللغة حواملَ (4,561)"),
    Deposit("sibawayh-abniya.tsv", "وضع", "أبنيةُ الأسماء عند سيبويه (158 هيكلًا)"),
    Deposit("nabhani-huruf.json", "وضع",
            "معاني الحروف من مبحث «الحرف» في الشخصيّة ج3 بترتيب المصدر (25 مدخلًا، 29 حرفًا)"),
    # — مختومةٌ بإذن مالك المشروع («اختم ورخّص — موافق بتوقيع مالك المشروع»، 2026-10-08)؛ نصوصُ
    #   OpenITI (الإصدار 2025.1.9، Zenodo 17767721) برخصة CC BY-NC-SA 4.0؛ بايتاتٌ مودَعة لا تقرؤها
    #   شيفرةٌ هنا إلّا أدواتُ الإيداع المعفاة، وما يُقرأ منها يدخل جدولًا مولَّدًا بـ--check (المادّة ١٢). —
    Deposit("openiti-mukhassas.txt.gz", "وضع",
            "المخصّص لابن سيده (JK000849): 1,600 عقدةً 73/337/1,190 كما هي؛ روايةُ الوضع الأوّل "
            "مسنَدةً",
            "8d8134c2bce16b70b07bddf974fa5e9c0f7cd80129d8452baf55cd87006b80ac",
            "CC BY-NC-SA 4.0 (OpenITI)"),
    Deposit("openiti-maqayis.txt.gz", "وضع",
            "معجم مقاييس اللغة لابن فارس كاملًا (JK008008) ومنه الرباعيّ وما فوقه",
            "da8853fc941d4016a533fd9c7a1f794a2ccfa92f1c74e68d4acbd6d910e72a67",
            "CC BY-NC-SA 4.0 (OpenITI)"),
    Deposit("openiti-sibawayh-kitab.txt.gz", "وضع",
            "الكتاب لسيبويه كاملًا (JK006989؛ 0200AH @599f22f، مطابقٌ لنسخة hamil): حروفُ الزوائد "
            "العشرة بمواضعها، وأبوابُ النون الثقيلة والخفيفة بشواهدها",
            "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625",
            "CC BY-NC-SA 4.0 (OpenITI)"),
    # — بتوقيع المالك (صالح الغانم، 2026-10-09): لفظُ الجلالة منفردًا لا شبيهَ له، واللهمّ، والأعلامُ
    #   موسومةً لفظًا منفردًا بلا قياس (ممنوعٌ/منصرف/مقصور/غيرُ مشهود الجرّ، عربيٌّ/أعجميّ). —
    Deposit("owner-alam.json", "وضع",
            "لفظُ الجلالة (10 صور) و57 علمًا موسومةً بعينها؛ وضعُ العلميّة لا القياس — تُولَّد منه "
            "جداولُ `Alam` بـ--check (ADR ٢٤)",
            "09290ebbc0203a407531a74dd528581108f7403931c7bd4dd80a9b0d5fb59a86",
            "بتوقيع المالك"),
    Deposit("openiti-majaz-quran.txt.gz", "مرجع محجوب",
            "مجاز القرآن لأبي عبيدة (JK010146): مرجعُ الأحكام المحجوب للمجاز — يُقاس عليه ولا يُقرأ "
            "منه",
            "432dae05748f2f972b3238e56dd0c56e72b10f0c3900ee8da1a8cca812b2fc88",
            "CC BY-NC-SA 4.0 (OpenITI)"),
    *(Deposit(f"masaq-{x}", "مرجع محجوب", "شريحةُ MASAQ") for x in (
        "adad.json", "fil.json.gz", "filiyya.json.gz", "hamza.json", "huruf.json",
        "interrog.json", "ism.json.gz", "jazm.json", "jumla.json", "majrurat.json.gz",
        "mansubat.json", "marifa.json", "munada.json", "nawasikh.json", "sarf.json",
        "shibh.json.gz", "tawabi.json", "zaman.json", "zawaid.json", "zuruf.json")),
)
"""كلُّ مودَعٍ بنوعه. «معلومات سابقة» لا مودَعَ لها بعد: المخصّصُ مختومٌ «وضعًا» (روايةُ الوضع)،
وتُشتقّ منه المعلوماتُ السابقة (الأجناسُ والقابليّات) جدولًا مولَّدًا بنوعها حين يُؤذن بأداتها."""


def tables() -> tuple[str, ...]:
    """أسماءُ جداول `lake exe slge-table` بترتيب السجلّ — قائمةُ CI."""

    return tuple(t for m in MODULES for t in m.tables)


def lean_files() -> tuple[str, ...]:
    return tuple(x for m in MODULES for x in m.lean)


def readers_under_law() -> tuple[Module, ...]:
    """القرّاءُ الخاضعون لقانون القارئ — كلُّ قارئٍ جديدٍ يُسجَّل هنا بـ`law=True`."""

    return tuple(m for m in MODULES if m.law)


def index_tools() -> tuple[str, ...]:
    """أدواتُ الفهارس التي يفحصها CI بـ`--check`."""

    return tuple(m.index for m in MODULES if m.index)
