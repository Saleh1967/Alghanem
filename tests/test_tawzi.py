"""الموزِّع: توقّعاتٌ مستقلّةٌ عن الشيفرة (المبنيُّ من جدوله بسوابقه ولاحقته ويُردّ بعينه؛ الحاملُ
لا يُقرأ
وحدَه؛ التعديلاتُ مسمّاة؛ ما ليس في الجدول لا يُقرأ)، والإغلاقُ (ADR ٥٣): اللاحقةُ لا يحملها إلّا
حاملُها، والمركَّبُ
بمَا/مَنْ، وميمُ الجمع وياءُ الإضافة وكافُ الخطاب وهمزةُ الوصل — وطفراتٌ مرفوضة بأسمائها."""

from __future__ import annotations

import re
import sys
import types
from pathlib import Path
from typing import Any

from slge.cells import licensed
from slge.rawabit import cells_of
from slge.tawzi import (
    COMPOUNDS,
    HOSTS,
    KINDS,
    SUF_TABLE,
    SUFFIXES,
    TABLE,
    UNSOURCED,
    VARIANTS,
    VERBS,
    alif_to_ya,
    junction,
    restore,
    tawzi,
)

SRC = Path(__file__).resolve().parent.parent / "src" / "slge" / "tawzi.py"


def test_table_is_the_union_of_deposited_tables_without_duplicates() -> None:
    # 246 صورةً قبل الإغلاق، والفعلان ظَنَّ وحَسِبَ خرجا (VERB_NOT_MABNI)؛ الحاملان بِ ولِ وحدَهما
    # 246 قبل ADR ٥٣؛ ظَنَّ وحَسِبَ فعلان (ADR ٥٣)، وذُو الطائيّةُ بلا سندٍ في الكتاب (ADR ٥٤)
    assert VERBS == ("ظَنَّ", "حَسِبَ") and UNSOURCED == ("ذُو",)
    assert len(TABLE) == 243 and len(HOSTS) == 2
    assert not {cells_of(v) for v in VERBS} & {w for _, _, w in TABLE}
    assert len({w for _, _, w in TABLE}) == len(TABLE) and all(licensed(w) for _, _, w in TABLE)
    assert {k for k, _, _ in TABLE} == set(KINDS) and all(k == "حرف" for k, _, _ in HOSTS)
    assert {n for _, n, _ in HOSTS} == {"بِ", "لِ"}
    assert not {w for _, _, w in HOSTS} & {w for _, _, w in TABLE}  # الحاملُ ليس مبنيًّا قائمًا بنفسه
    assert set(SUF_TABLE) <= {w for _, _, w in TABLE}
    # المركَّباتُ: 24 جارًّا وناسخًا قائمًا بنفسه × (مَا، مَنْ)، وأَنْ وإِنْ بلَا (ADR ٥٤)؛ كلُّها مرخَّصة
    assert len(COMPOUNDS) == 24 * 2 + 2 and all(licensed(w) for _, _, w in COMPOUNDS)
    # اللواحق: 17 ضميرًا متّصلًا، وياءُ الإضافة ساكنة، وثلاثُ لواحقَ بميمٍ ساكنة (كُمْ هُمْ هِمْ) × (ضمّ، كسر)
    assert len(SUFFIXES) == 17 + 1 + 3 * 2


def test_reads_particles_pronouns_and_adverbs_with_clitics_and_restores() -> None:
    for word, pre, name, suf, variant in (
        ("عَلَيْهِمْ", "", "عَلَى", "هم", "ALIF_TO_YA"),
        ("وَإِذَا", "و", "إِذَا", "", ""),
        ("بِمَا", "ب", "مَا", "", ""),
        ("مِنْهُمْ", "", "مِنْ", "هم", ""),
        ("إِنَّهُ", "", "إِنَّ", "ه", ""),
        ("فَلَمَّا", "ف", "لَمَّا", "", ""),
        ("بِهِ", "", "بِ", "ه", ""),
        ("لَكُمْ", "", "لِ", "كم", "LAM_FATHA"),
        ("مِنَ", "", "مِنْ", "", "JUNCTION_FATHA"),
        ("عَنِ", "", "عَنْ", "", "JUNCTION_KASRA"),
        # الإغلاق (ADR ٥٣)
        ("لَهُمُ", "", "لِ", "هم", "LAM_FATHA"),          # ميمُ الجمع موصولةً مضمومة
        ("عَلَيْهِمِ", "", "عَلَى", "هم", "ALIF_TO_YA"),   # ومكسورة
        ("لِي", "", "لِ", "ي", ""),                        # ياءُ الإضافة ساكنة
        ("إِنِّي", "", "إِنَّ", "ي", "KASR_BEFORE_YA"),
        ("وَلِلَّذِينَ", "ول", "الَّذِينَ", "", "WASL_DROP"),
        ("ذَلِكُمْ", "", "ذَلِكَ", "", "KAF_KHITAB"),
        ("كَذَلِكِ", "ك", "ذَلِكَ", "", "KAF_KHITAB"),
        ("هُمُ", "", "", "", "JUNCTION_DAMMA"),
        ("وَمِنْكُمْ", "و", "مِنْ", "كم", ""),
        ("فِيمَا", "", "فِي+مَا", "", ""),
        ("مِمَّا", "", "مِنْ+مَا", "", ""),
        ("عَمَّنْ", "", "عَنْ+مَنْ", "", ""),
        ("كَأَنَّمَا", "", "كَأَنَّ+مَا", "", ""),
    ):
        w = cells_of(word)
        ms = tawzi(w)
        assert ms and all(restore(m) == w for m in ms), word
        assert any(m.name == name and "".join(k for p in m.pre for k, _ in p) == pre
                   and "".join(k for k, _ in m.suf) == suf and m.variant == variant
                   for m in ms), (word, ms)


def test_suffix_needs_its_host() -> None:
    # وَهُمْ: الواوُ ليست حاملًا — واوٌ وضميرٌ منفصل وحدَه
    ms = tawzi(cells_of("وَهُمْ"))
    assert ms and all(not m.suf for m in ms) and {m.kind for m in ms} == {"ضمير"}
    # إِنِّي: إِنَّ قبل ياء الإضافة، لا «إِنْ» الشرطيّةُ بنون الوقاية
    assert [(m.name, m.variant) for m in tawzi(cells_of("إِنِّي"))] == [("إِنَّ", "KASR_BEFORE_YA")]
    # الكافُ والتاءُ لا تحملان: كَهُ وتَهُ لا تُقرآن
    assert not tawzi(cells_of("كَهُ")) and not tawzi(cells_of("تَهُ"))
    # والموصولُ والاستفهامُ لا يحملان لاحقة
    assert not any(m.suf for m in tawzi(cells_of("مَاهُ")))


def test_template_words_and_bare_hosts_are_not_read_here() -> None:
    assert not tawzi(cells_of("كَتَبَ")) and not tawzi(cells_of("ذَهَبَ"))
    assert not tawzi(cells_of("بِ")) and not tawzi(cells_of("لِ"))  # الحاملُ يحتاج لاحقة
    assert not tawzi(cells_of("مَعَ"))  # ليس في جداولنا — باسمه، لا من الذاكرة
    assert not tawzi(cells_of("ظَنَّ")) and not tawzi(cells_of("حَسِبَ"))  # فعلان لهما قالب


def test_variants_are_named_and_minimal_and_mutants() -> None:
    assert VARIANTS == ("", "ALIF_TO_YA", "LAM_FATHA", "KASR_BEFORE_YA", "JUNCTION_KASRA",
                        "JUNCTION_FATHA", "JUNCTION_DAMMA", "KAF_KHITAB", "WASL_DROP",
                        "NUN_NA_IDGHAM")
    assert alif_to_ya(cells_of("إِلَى")) == cells_of("إِلَيْ")
    assert alif_to_ya(cells_of("عَنْ")) == cells_of("عَنْ")
    k, f = junction(cells_of("عَنْ"))
    assert k == cells_of("عَنِ") and f == cells_of("عَنَ")
    assert junction(cells_of("إِذَا")) == (cells_of("إِذَا"), cells_of("إِذَا"))  # لا ساكنَ في الآخر
    # طفرة: الألفُ لا تصير ياءً بلا لاحقة (عَلَيْ وحدَها لا تُقرأ عَلَى)
    assert not any(m.name == "عَلَى" for m in tawzi(cells_of("عَلَيْ")))
    # طفرة: لاحقةٌ ليست من جدول الضمائر لا تُقطع
    assert not tawzi(cells_of("مِنْزَ"))
    # همزةُ الوصل لا تسقط بلا سابقة: لَّذِينَ وحدَها لا تُقرأ
    assert not tawzi(cells_of("الَّذِينَ")[1:])


def _mutant(old: str, new: str) -> dict[str, Any]:
    src = SRC.read_text(encoding="utf-8")
    assert old in src, old
    mod = types.ModuleType("tawzi_mutant")
    sys.modules["tawzi_mutant"] = mod  # الصنفُ البيانيّ يطلب وحدتَه
    # الطفرةُ يلتقطها الاختبارُ لا الفحصُ الداخليّ
    src = src.replace(old, new, 1).replace("\n_check()\n", "\n")
    exec(compile(src, "tawzi_mutant", "exec"), mod.__dict__)
    return mod.__dict__


def test_named_closure_mutants_are_caught() -> None:
    # MUTANT_ANY_PROCLITIC_HOSTS: الحواملُ كلُّ المتّصلة كما كانت ← وَهُمْ تُقرأ واوًا حاملًا
    m = _mutant('if p.proclitic and p.name in ("بِ", "لِ"))', "if p.proclitic)")
    assert any(x.suf for x in m["tawzi"](cells_of("وَهُمْ")))
    # MUTANT_ANY_CORE_TAKES_SUFFIX: كلُّ مبنيٍّ يحمل ← إِنْ + نِي قراءةٌ ثانية لإِنِّي
    m = _mutant("cores = _SUF_CORES if suf else _PLAIN",
                "cores = {**_CORES, **_SUF_CORES} if suf else _PLAIN")
    assert len(m["tawzi"](cells_of("إِنِّي"))) == 2
    # MUTANT_NO_IDGHAM: مِنْ + مَا بلا إدغام ← مِمَّا لا تُقرأ
    m = _mutant('return (*a[:-1], ("م", SUKUN), *b)', "return (*a, *b)")
    assert not m["tawzi"](cells_of("مِمَّا"))
    # MUTANT_WASL_WITHOUT_PREFIX: همزةُ الوصل تسقط بلا سابقة
    m = _mutant("if has_pre and core not in _COMPOUND_CORES and core[:2]", "if core[:2]")
    assert m["tawzi"](cells_of("الَّذِينَ")[1:])


def test_rules_are_anchored_in_the_sealed_kitab() -> None:
    # كلُّ قاعدةٍ تستشهد بالكتاب لها في `Tawzi.lean` سطرُها وعبارتُها، والعبارةُ في السطر المختوم بعينه
    import gzip

    lines = gzip.decompress((SRC.parents[2] / "tests" / "data" / "openiti-sibawayh-kitab.txt.gz")
                            .read_bytes()).decode("utf-8").splitlines()
    for line, phrase in ((8106, "ياء الإضافة إلا كان متحركا مكسورا"), (8128, "الكاف التي تجر بها"),
                         (8130, "قلما تكلموا بذا"), (14027, "ولا تدخل إلا في واحد"),
                         (18109, "لا يكسرها إذا كانت بعدها ألف وصل"),
                         (21468, "وتدغم النون مع الميم")):
        assert phrase in lines[line - 1] + " " + lines[line], (line, phrase)
    lean = (SRC.parents[2] / "formal" / "Slge" / "Tawzi.lean").read_text(encoding="utf-8")
    for anchor in ("س8106", "س8128", "س14027", "س18109", "س21468"):
        assert anchor in lean
    assert re.search(r"س18117", lean)


def test_debts_paid_by_hand() -> None:
    """ADR ٥٤: كلُّ دَينٍ بقراءته المتوقَّعة باليد، أو بلا قراءة حيث المصدرُ يمنع."""

    def reads(word: str) -> list[tuple[str, str, str, str]]:
        return [("".join(k for p in m.pre for k, _ in p), m.name, m.variant,
                 "".join(k for k, _ in m.suf)) for m in tawzi(cells_of(word))]

    assert reads("إِنَّا") == [("", "إِنَّ", "NUN_NA_IDGHAM", "نا")]
    assert reads("وَلَكِنَّا") == [("و", "لَكِنَّ", "NUN_NA_IDGHAM", "نا")]
    assert reads("أَلَّا") == [("", "أَنْ+لَا", "", "")]
    assert reads("أَيُّهُمْ") == [("", "أَيُّ", "", "هم")]
    assert reads("أَيُّهَا") == []        # يا أَيُّها: الهاءُ للتنبيه (س5503–5505)
    assert reads("أَكَلَهُ") == []        # لا جارَّ بعد الكاف (س4192)
    assert reads("أَبِي") == []           # اسمٌ من الخمسة لا يُقطع
    assert reads("ذُو") == []             # ذُو الطائيّةُ بلا سند
    assert reads("أَلَهُمْ")[0][:2] == ("ء", "لِ")  # والاستفهامُ قبل الحامل باقٍ


def test_debt_mutants_are_caught() -> None:
    # MUTANT_NO_NUN_NA: بلا حذف النون ← إِنَّا لا تُقرأ
    m = _mutant('out.append(("NUN_NA_IDGHAM", core[:-1]))', "pass")
    assert not m["tawzi"](cells_of("إِنَّا"))
    # MUTANT_AYYUHA_PRONOUN: هاءُ أيّها ضميرًا
    m = _mutant("if core in _AYY and suf == _HA:", "if False:")
    assert m["tawzi"](cells_of("أَيُّهَا"))
    # MUTANT_JARR_ON_JARR: الكافُ قبل اللام الحاملة
    m = _mutant("if pre and pre[-1] in _JARR_PRE and core in _JARR_CORES:", "if False:")
    assert m["tawzi"](cells_of("أَكَلَهُ"))
    # MUTANT_KHAMSA_CUT: الاسمُ من الخمسة يُقطع حروفًا
    m = _mutant("frozenset(khamsa_form(s, c) for s in KHAMSA for c in CASES)", "frozenset()")
    assert m["tawzi"](cells_of("أَبِي"))
