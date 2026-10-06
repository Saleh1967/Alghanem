"""مطابقةُ البايثون لتعريفات Lean، على مخرجات `lake exe slge-table` المودَعة في `formal/out/`.

ويفحص CI أنّ هذه المخرجاتِ هي ما يُخرجه Lean الآن (يعيد توليدها ثمّ `git diff --exit-code`)،
فتنتقل مبرهناتُ `formal/Slge/` إلى الدوالّ البايثونيّة بهذا التطابق.
"""

from __future__ import annotations

import csv
from pathlib import Path

from conftest import ROOT, licensed_words
from slge.cells import ALPHABET, CELLS, STATES, Cell, a116_code, count, fold, index, licensed
from slge.knowledge import Degree, Form, productive

OUT = ROOT / "formal" / "out"


def _rows(name: str) -> list[list[str]]:
    with Path(OUT / name).open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def _cell(i: int) -> Cell:
    return (ALPHABET[i // 4], STATES[i % 4])


def test_bridge_matches_lean() -> None:
    rows = _rows("bridge.csv")
    assert len(rows) == 116
    for (carrier, state, code), cell in zip(rows, CELLS, strict=True):
        assert (ALPHABET[int(carrier)], STATES[int(state)]) == cell
        assert int(code) == a116_code(cell)


def test_counts_match_lean() -> None:
    rows = _rows("counts.csv")
    assert [int(n) for n, _ in rows] == list(range(13))
    assert all(int(u) == count(int(n)) for n, u in rows)


def test_folds_match_lean() -> None:
    lean = {r[0]: int(r[1]) for r in _rows("folds.csv")}
    ours = {"-".join(str(index(c)) for c in w): fold(w)
            for n in (0, 1, 2) for w in licensed_words(n)}
    assert lean == ours  # المجموعتان واحدة: فالترخيصُ واحدٌ أيضًا على الطول ≤ 2
    assert all(_cell(int(i)) in CELLS for k in lean if k for i in k.split("-"))


def test_ghazali_matches_lean() -> None:
    names = {"akhass": Degree.اخص, "musawi": Degree.مساو}
    forms = {f.value: f for f in Form}
    rows = _rows("ghazali.csv")
    assert len(rows) == 8
    for d, f, p in rows:
        assert productive(names[d], forms[f]) == (p == "true")


def test_sequence_matches_lean() -> None:
    """`stream.encode_word` = `Sequence.encodeWord` على كلّ مرخَّصةٍ بطول ‎≤ 2‎،
    والعرضُ والكلفةُ كما في Lean،
    وكلُّ تيارٍ مرمَّزٍ يُفكّ بعينه (مرآةُ `decode_encode`)."""

    from slge.stream import cost, decode, encode, encode_word, width

    rows = _rows("sequence.csv")
    widths = {int(r[1]): (int(r[2]), int(r[3])) for r in rows if r[0] == "width"}
    assert widths == {k: (width(k), cost(k)) for k in (0, 1, 2)}
    lean = {r[0]: r[1] for r in rows if r[0] != "width"}
    ours = {"-".join(str(index(c)) for c in w): "".join("1" if b else "0" for b in encode_word(w))
            for n in (0, 1, 2) for w in licensed_words(n)}
    assert lean == ours
    words = [w for n in (1, 2) for w in licensed_words(n)][:500]
    assert decode(encode(words)) == [tuple(w) for w in words]


def test_categories_match_lean() -> None:
    """الضمائرُ الاثنا عشر خاناتٍ وأعدادًا = جدولُ `Categories.pronouns` في Lean."""

    from slge.categories import PRONOUNS, fingerprints, pronoun

    rows = [r for r in _rows("categories.csv") if r[0] == "pronoun"]
    assert [r[1] for r in rows] == ["-".join(str(index(c)) for c in w) for w in PRONOUNS]
    assert [int(r[2]) for r in rows] == list(fingerprints())
    assert len(set(fingerprints())) == 12 and all(pronoun(w) for w in PRONOUNS)


def test_wazn_matches_lean() -> None:
    """الأوزانُ المودَعة (104) بميزانها خاناتٍ، ترخيصُها، وردُّها الأصلَ = جدولُ `Wazn.awzan`."""

    from slge.wazn import AWZAN, FAL, mizan, root_of

    rows = _rows("wazn.csv")
    assert len(rows) == len(AWZAN) == 121
    for r, w in zip(rows, AWZAN, strict=True):
        m = mizan(w.template)
        assert r[1] == "-".join(str(index(c)) for c in m), w.name
        assert r[2] == "true" and licensed(m), w.name
        assert r[3] == "-".join(str(ALPHABET.index(c)) for c in FAL)
        assert root_of(w.template, m) == FAL


def test_shabaka_matches_lean() -> None:
    """حوافُّ البصريّين: (ابن، أب، عددُ العمليّات، يبلغ الجذر) = جدولُ `Shabaka.edges`."""

    from slge.shabaka import CLASSICAL, ROOT, diff
    from slge.wazn import AWZAN

    names = [w.name for w in AWZAN]
    by = {w.name: w.template for w in AWZAN}
    rows = _rows("shabaka.csv")
    assert len(rows) == len(CLASSICAL) == 120 and names[29] == ROOT
    for r, (child, parent) in zip(rows, CLASSICAL.items(), strict=True):
        assert (int(r[0]), int(r[1])) == (names.index(child), names.index(parent))
        assert int(r[2]) == len(diff(by[parent], by[child])) and r[3] == "true"


def test_khamsa_matches_lean() -> None:
    """الصورُ الخمسَ عشرة خاناتٍ وأعدادًا = جدولُ `Khamsa.forms`."""

    from slge.khamsa import CASES, KHAMSA, form

    rows = _rows("khamsa.csv")
    forms = [form(s, c) for s in KHAMSA for c in CASES]
    assert [r[0] for r in rows] == ["-".join(str(index(c)) for c in w) for w in forms]
    assert [int(r[1]) for r in rows] == [fold(w) for w in forms]


def test_afal_matches_lean() -> None:
    """الصورُ الثلاثون (4 جذوع × ضمائرُها × 3 حالات) = جدولُ `Afal.forms`."""

    from slge.afal import MOODS, PRONOUNS, STEMS, agree, form

    rows = _rows("afal.csv")
    forms = [form(s, p, m) for s in STEMS for p in PRONOUNS if agree(s.prefix, p) for m in MOODS]
    assert len(rows) == len(forms) == 30
    assert [r[0] for r in rows] == ["-".join(str(index(c)) for c in w) for w in forms]
    assert [r[1] for r in rows] == ["true"] * 30


def test_rawabit_matches_lean() -> None:
    """الأدواتُ السبعون خاناتٍ وعملًا واتّصالًا = جدولُ `Rawabit.particles`."""

    from slge.rawabit import PARTICLES

    rows = _rows("rawabit.csv")
    amal = {"": "none", "جزم": "jazm", "نصب": "nasb", "جرّ": "jarr",
            "نصب الاسم ورفع الخبر": "nasbIsm"}
    assert len(rows) == len(PARTICLES) == 90
    for r, p in zip(rows, PARTICLES, strict=True):
        assert r[0] == p.name and r[1] == "-".join(str(index(c)) for c in p.cells)
        assert r[2] == amal[p.amal] and r[3] == str(p.proclitic).lower() and r[4] == "true"


def test_damair_matches_lean() -> None:
    """الصورُ الثلاثُ والثلاثون (12 رفع + 12 نصب + 9 شواهد) = جدولُ `Damair.allForms`."""

    from slge.damair import DETACHED_NASB, DETACHED_RAF, WITNESS

    rows = _rows("damair.csv")
    forms = [p.cells for p in DETACHED_RAF + DETACHED_NASB] + list(WITNESS.values())[:9]
    assert len(rows) == len(forms) == 33
    assert [r[0] for r in rows] == ["-".join(str(index(c)) for c in w) for w in forms]


def test_ishara_matches_lean() -> None:
    """الصورُ الخمسُ والعشرون بأسمائها وخاناتها = جدولُ `Ishara.forms`."""

    from slge.ishara import FORMS

    rows = _rows("ishara.csv")
    assert len(rows) == len(FORMS) == 25
    for r, f in zip(rows, FORMS, strict=True):
        assert r[0] == f.name and r[1] == "-".join(str(index(c)) for c in f.cells)


def test_istifham_matches_lean() -> None:
    """الصورُ الاثنتان والعشرون بأسمائها وخاناتها = جدولُ `Istifham.forms`."""

    from slge.istifham import FORMS

    rows = _rows("istifham.csv")
    assert len(rows) == len(FORMS) == 22
    for r, f in zip(rows, FORMS, strict=True):
        assert r[0] == f.name and r[1] == "-".join(str(index(c)) for c in f.cells)


def test_nida_matches_lean() -> None:
    """الأدواتُ الستّ وشواهدُ الحكم = جدولا `Nida.particles` و`Nida.witnesses`."""

    from slge.nida import PARTICLES, hukm

    rows = _rows("nida.csv")
    parts = [r for r in rows if r[0] == "particle"]
    assert [r[1] for r in parts] == [p.name for p in PARTICLES]
    assert [r[2] for r in parts] == ["-".join(str(index(c)) for c in p.cells) for p in PARTICLES]
    lean_hukm = {"mabniDamm": "مبني على الضم", "mansub": "معرب منصوب",
                 "mudafIlaYa": "مضاف إلى ياء محذوفة", "unread": "لا تقرؤه الخانة"}
    for r in rows:
        if r[0] == "witness":
            cells = tuple(_cell(int(i)) for i in r[2].split("-"))
            assert hukm(cells) == lean_hukm[r[3]], r[1]


def test_zuruf_matches_lean() -> None:
    """الصورُ الإحدى والخمسون (17 جذعًا × مضاف/مجرور/مقطوع) = جدولُ `Zuruf.forms`."""

    from slge.zuruf import STEMS, jarr, mudaf, qat

    rows = _rows("zuruf.csv")
    forms = [op(z.stem) for z in STEMS for op in (mudaf, jarr, qat)]
    assert len(rows) == len(forms) == 51
    assert [r[0] for r in rows] == ["-".join(str(index(c)) for c in w) for w in forms]


def test_zaman_matches_lean() -> None:
    """الصورُ الأربعون (8 × 5) والثوابتُ الثمانية = جدولا `Zaman.forms` و`Zaman.constants`."""

    from slge.zaman import CONSTANTS, STEMS, forms_of

    rows = _rows("zaman.csv")
    forms = [f for stem in STEMS.values() for f in forms_of(stem)]
    frows = [r for r in rows if r[0] == "form"]
    assert [r[1] for r in frows] == ["-".join(str(index(c)) for c in w) for w in forms]
    crows = [r for r in rows if r[0] == "constant"]
    assert [r[1] for r in crows] == list(CONSTANTS)
    assert [r[2] for r in crows] == ["-".join(str(index(c)) for c in w)
                                     for w, _ in CONSTANTS.values()]
    assert [STATES[int(r[3])] for r in crows] == [st for _, st in CONSTANTS.values()]


def test_adad_matches_lean() -> None:
    """الصورُ الاثنتان والثمانون = جدولُ `Adad.forms` بترتيبه."""

    from slge.adad import STEMS, UQUD, compound, fem, masc, twelve, uqud

    rows = _rows("adad.csv")
    forms: list[tuple[Cell, ...]] = []
    for s in STEMS.values():
        forms += [masc(s, STATES[2]), masc(s, STATES[0]), masc(s, STATES[1]),
                  fem(s, STATES[2]), fem(s, STATES[0]), fem(s, STATES[1])]
    for s in UQUD.values():
        forms += [uqud(s, True), uqud(s, False)]
    forms += [twelve(True, True), twelve(False, True), twelve(True, False), twelve(False, False)]
    for n, s in STEMS.items():
        if n <= 9:
            forms += [compound(s, True), compound(s, False)]
    assert len(rows) == len(forms) == 82
    assert [r[0] for r in rows] == ["-".join(str(index(c)) for c in w) for w in forms]


def test_marifa_matches_lean() -> None:
    """الموصولةُ الأربعَ عشرةَ بأسمائها وخاناتها = جدولُ `Marifa.mawsul`."""

    from slge.marifa import MAWSUL

    rows = _rows("marifa.csv")
    assert [r[0] for r in rows] == list(MAWSUL)
    assert [r[1] for r in rows] == ["-".join(str(index(c)) for c in w) for w in MAWSUL.values()]


def test_sarf_matches_lean() -> None:
    """شواهدُ العلل بأحكامها = جدولُ `Sarf.witnesses`."""

    from slge.sarf import illa

    lean = {"muntahaJumu": "صيغة منتهى الجموع", "maqsura": "ألف التأنيث المقصورة",
            "mamduda": "ألف التأنيث الممدودة", "sifa": "وزن أَفْعَل/فَعْلَان (صفةٌ أو علم)",
            "alifNun": "ألف ونون زائدتان", "unread": "معجم"}
    rows = _rows("sarf.csv")
    assert len(rows) == 9
    for r in rows:
        cells = tuple(_cell(int(i)) for i in r[1].split("-"))
        assert illa(cells) == lean[r[2]], r[0]


def test_tawabi_matches_lean() -> None:
    """شواهدُ العلامات الأربع = جدولُ `Tawabi` بحالاتها المقروءة."""

    from slge.tawabi import case_class

    rows = _rows("tawabi.csv")
    lean = {"raf": "رفع", "nasb": "نصب", "jarr": "جرّ", "nasbJarr": "نصب/جرّ",
            "unread": "لا تقرؤه الخانة"}
    assert len(rows) == 5
    for r in rows:
        cells = tuple(_cell(int(i)) for i in r[1].split("-"))
        assert case_class(cells) == lean[r[2]], r[0]


def test_nawasikh_matches_lean() -> None:
    """المودَعاتُ الأربع وصورُ الكفّ وشاهدا كان/إنّ = جدولُ `Nawasikh`."""

    from slge.nawasikh import INNA, KADA, KANA, ZANNA, kaffa, nasb, raf, tanwin
    from slge.rawabit import cells_of

    rows = _rows("nawasikh.csv")
    assert len(rows) == 13 + 12 + 6 + 15 + 6 + 2
    babs = {"kana": KANA, "kada": KADA, "inna": INNA, "zanna": ZANNA}
    for r in rows:
        cells = tuple(_cell(int(i)) for i in r[2].split("-"))
        if r[0] in babs:
            word = next(w for w in babs[r[0]] if w.replace("اِ", "ا") == r[1])
            assert cells_of(word) == cells, r
        elif r[0] == "kaffa":
            assert kaffa(cells_of(r[1])) == cells, r
        else:
            op = nasb if r[0] == "kana_khabar" else raf
            assert tanwin(op(cells_of("غَفُورُ"))) == cells == cells_of(r[1]), r


def test_jazm_matches_lean() -> None:
    """أدواتُ الجزم والشرط وشواهدُ القارئ = جدولُ `Jazm`."""

    from slge.jazm import JAZIM_ONE, SHART_GHAYR, SHART_JAZIM, marker
    from slge.rawabit import cells_of

    rows = _rows("jazm.csv")
    assert len(rows) == 4 + 12 + 7 + 8
    babs = {"one": JAZIM_ONE, "jazim": SHART_JAZIM, "ghayr": SHART_GHAYR}
    lean = {"sukun": "سكون", "dropNun": "حذف النون", "unread": "لا تقرؤه الخانة"}
    for r in rows:
        cells = tuple(_cell(int(i)) for i in r[2].split("-"))
        if r[0] in babs:
            assert r[1] in babs[r[0]] and cells_of(r[1]) == cells, r
        else:
            assert marker(cells) == lean[r[3]], r


def test_mansubat_matches_lean() -> None:
    """قانونُ الفرز والعمليّاتُ والأدوات = جدولُ `Mansubat`."""

    from slge.mansubat import TOOLS, derived, ghayr_of, nakira_mansuba, raf, tahwil
    from slge.marifa import idafa
    from slge.rawabit import cells_of
    from slge.zuruf import jarr

    rows = _rows("mansubat.csv")
    assert len(rows) == 5 + 4 + 6
    names = {"dahik": "ضَاحِكُ", "rakid": "رَاكِضُ", "nafs": "نَفْسُ", "shayb": "شَيْبُ", "sukara": "سُكَارَى"}
    tools = dict(zip(("illa", "ghayr", "siwa", "khala", "ada", "hasha"), TOOLS, strict=True))
    shayb, ras = cells_of("شَيْبُ"), cells_of("رَأْسُ")
    ops = {"shayb": nakira_mansuba(shayb), "ras": tahwil(shayb, ras)[0],
           "original": idafa(raf(shayb), cells_of("اَرَّأْسِ")),
           "ghayr_raf": ghayr_of(raf, cells_of("رَجُلُ"))}
    for r in rows:
        cells = tuple(_cell(int(i)) for i in r[2].split("-"))
        if r[0] == "derived":
            assert cells_of(names[r[1]]) == cells and derived(cells) == (r[3] == "true"), r
        elif r[0] == "op":
            assert ops[r[1]] == cells, r
        else:
            assert cells_of(tools[r[1]]) == cells, r
    assert jarr(ras)[-1] == ("س", "كسر")


def test_majrurat_matches_lean() -> None:
    """حروفُ الجرّ وعمليّاتُ الإضافة والمثنّى = جدولُ `Majrurat`."""

    from slge.majrurat import HARFS, dual, jarr_nakira, mudaf_dual, mudaf_uqud
    from slge.rawabit import cells_of

    rows = _rows("majrurat.csv")
    assert len(rows) == len(HARFS) + 4
    rajul = cells_of("رَجُلُ")
    ops = {"jarr_nakira": jarr_nakira(rajul), "dual": dual(rajul), "mudaf_dual": mudaf_dual(rajul),
           "mudaf_uqud": mudaf_uqud(cells_of("مُهَنْدِسُ"), True)}
    for r in rows:
        cells = tuple(_cell(int(i)) for i in r[2].split("-"))
        if r[0] == "harf":
            assert r[1] in HARFS and cells_of(r[1]) == cells, r
        else:
            assert ops[r[1]] == cells, r


def test_wasl_matches_lean() -> None:
    """الأسماءُ العشرة وشواهدُ القارئ وتقسيمُ القوالب = جدولُ `Wasl`."""

    from slge.rawabit import cells_of
    from slge.wasl import QAT_TEMPLATES, TEN, WASL_TEMPLATES, kind

    rows = _rows("wasl.csv")
    assert len(rows) == 10 + 7 + 2
    lean = {"wasl": "وصل", "qat": "قطع", "qatRadical": "قطع أصلي", "unread": "لا يُقرأ"}
    ten = {w[:-1]: cells_of(w)[:-1] for w in TEN}
    for r in rows:
        if r[0] == "templates":
            assert tuple(int(i) for i in r[2].split("-")) == (WASL_TEMPLATES if r[1] == "wasl"
                                                               else QAT_TEMPLATES)
            continue
        cells = tuple(_cell(int(i)) for i in r[2].split("-"))
        if r[0] == "ten":
            assert ten[r[1]] == cells[:-1] and kind(cells) == lean[r[3]], r
        else:
            assert kind(cells) == lean[r[3]], r


def test_ism_matches_lean() -> None:
    """شواهدُ الثلاثيّ وأشكالُ الرباعيّ والخماسيّ وعمليّاتُ التصغير والنسب = جدولُ `Ism`."""

    from slge.cells import STATES
    from slge.ism import nisba, prepare, read_thulathi, saghir3, saghir4, saghir5, shape
    from slge.rawabit import cells_of

    rows = _rows("ism.csv")
    assert len(rows) == 11 + 10 + 7
    st = dict(zip("0123", STATES, strict=True))
    u = STATES[2]
    ops = {"rujayl": saghir3("ر", "ج", "ل", u), "durayhim": saghir4("د", "ر", "ه", "م", u),
           "usayfir": saghir5("ع", "ص", "ف", "ر", u), "misri": nisba(cells_of("مِصْرَ"), u),
           "makki": nisba(prepare("حذف التاء", cells_of("مَكَّةُ")), STATES[2]),
           "asawi": nisba(prepare("مقصور ثالث", cells_of("عَصَا")), STATES[2]),
           "amawi": nisba(prepare("منقوص ثالث", cells_of("عَمِي")), STATES[2])}
    for r in rows:
        cells = tuple(_cell(int(i)) for i in r[2].split("-"))
        if r[0] == "thulathi":
            f, a = r[3].split("-")
            assert read_thulathi(cells) == (st[f], st[a]), r
        elif r[0] == "shape":
            assert shape(cells) == tuple(st[x] for x in r[3].split("-")), r
        else:
            assert ops[r[1]] == cells, r


def test_fil_matches_lean() -> None:
    """الأبوابُ وأحرفُ الزيادة وعمليّاتُ الإعلال والإبدال والرباعيُّ = جدولُ `Fil`."""

    from slge.cells import STATES
    from slge.fil import (
        ABWAB,
        MAZID,
        MAZID_AMR,
        MAZID_PRES,
        added,
        amr_of,
        ibdal,
        idgham,
        iftaal,
        naql,
        qalb,
    )
    from slge.rawabit import cells_of
    from slge.wazn import AWZAN

    rows = _rows("fil.csv")
    assert len(rows) == 6 + 9 + 7 + 7 + 4
    st = dict(zip("0123", STATES, strict=True))
    ops = {"istabara": ibdal(iftaal(("ص", "ب", "ر"))), "izdahara": ibdal(iftaal(("ز", "ه", "ر"))),
           "ittasala": ibdal(iftaal(("و", "ص", "ل"))), "ittakhadha": ibdal(iftaal(("ء", "خ", "ذ"))),
           "radda": idgham(cells_of("رَدَدَ")), "qala": qalb(cells_of("قَوَلَ")),
           "qulu": naql(cells_of("قْوُلُ"))}
    amr = [r for r in rows if r[0] == "amr"]
    assert [(int(r[1]), int(r[2])) for r in amr] == list(zip(MAZID_PRES, MAZID_AMR, strict=True))
    for r in amr:
        assert r[3] == "true" and amr_of(AWZAN[int(r[1])].template) == AWZAN[int(r[2])].template
    babs = [r for r in rows if r[0] == "bab"]
    assert [(st[r[1][0]], st[r[1][2]]) for r in babs] == list(ABWAB)
    for r in rows:
        if r[0] == "mazid":
            assert int(r[1]) in MAZID and added(int(r[1])) == int(r[2]), r
        elif r[0] == "op":
            assert ops[r[1]] == tuple(_cell(int(i)) for i in r[2].split("-")), r
        elif r[0] == "rubai":
            assert cells_of(r[1]) == tuple(_cell(int(i)) for i in r[2].split("-")), r


def test_huruf_matches_lean() -> None:
    """جدولُ الحروف الموحَّد = جدولُ `Huruf` بأصنافه وأعماله."""

    from slge.huruf import TABLE

    rows = _rows("huruf.csv")
    assert len(rows) == len(TABLE) == 68
    cls = {"ism": "اسم", "fil": "فعل", "mushtarak": "مشترك"}
    amal = {"jarr": "جرّ", "nasbIsm": "نصب الاسم", "nida": "نداء", "maiyya": "معيّة",
            "nasbFil": "نصب الفعل", "jazm": "جزم", "jazm2": "جزم فعلين", "tabi": "تبعيّة",
            "none": ""}
    for r, x in zip(rows, TABLE, strict=True):
        cells = tuple(_cell(int(i)) for i in r[2].split("-"))
        assert (cls[r[0]], r[1], cells, amal[r[3]]) == (x.cls, x.name, x.cells, x.amal), r


def test_jumla_matches_lean() -> None:
    """الرتبةُ والقبولُ وصنفُ الخبر على الشواهد، والجنسُ والعددُ بعد العمليّات = جدولُ `Jumla`."""

    from slge.jumla import (
        WITNESSES,
        admissible,
        broken_plural,
        dual,
        gender,
        jam_f,
        jam_m,
        khabar_kind,
        number,
        order,
        ta_nith,
    )
    from slge.rawabit import cells_of

    rows = _rows("jumla.csv")
    ru = {"khabarFirst": "تقديم الخبر", "mubtadaFirst": "تقديم المبتدأ", "free": "جواز"}
    kk = {"mufrad": "مفرد", "shibhJumla": "شبه جملة", "jumla": "جملة فعلية", "unread": "—"}
    orders = [r for r in rows if r[0] == "order"]
    assert len(orders) == len(WITNESSES) == 7
    for r, j in zip(orders, WITNESSES.values(), strict=True):
        assert j.mubtada == tuple(_cell(int(i)) for i in r[2].split("-")), r[1]
        assert j.khabar == tuple(_cell(int(i)) for i in r[3].split("-")), r[1]
        assert order(j) == ru[r[4]] and admissible(j) == (r[5] == "true")
        assert khabar_kind(j.khabar) == kk[r[6]]
    talib = cells_of("طَالِبُ")
    forms = {"talib": talib, "taNith": ta_nith(talib), "dual": dual(talib), "jamM": jam_m(talib),
             "jamF": jam_f(talib), "dualTaNith": dual(ta_nith(talib)), "jibal": cells_of("اَلْجِبَالُ"),
             "shahiqa": cells_of("شَاهِقَةُ")}
    g = {"masc": "مذكر", "fem": "مؤنث"}
    n = {"single": "مفرد", "dual": "مثنى", "plural": "جمع"}
    for r in rows:
        if r[0] == "agree":
            w = forms[r[1]]
            assert w == tuple(_cell(int(i)) for i in r[2].split("-")), r[1]
            assert (gender(w), number(w)) == (g[r[3]], n[r[4]]), r[1]
            assert broken_plural(w) == (r[5] == "true"), r[1]


def test_filiyya_matches_lean() -> None:
    """رتبةُ الثلاثيّ وقبولُه على الشواهد، والمجهولُ، والنائبُ، والفرزُ = جدولُ `Filiyya`."""

    from slge.filiyya import (
        WITNESSES,
        admissible,
        majhul,
        majhul_pres,
        naib_kind,
        order,
        sort_fadla,
    )
    from slge.rawabit import cells_of

    rows = _rows("filiyya.csv")
    ru = {"failFirst": "الفاعل أولًا", "mafulFirst": "المفعول أولًا",
          "mafulBeforeFil": "المفعول قبل الفعل", "free": "جواز"}
    nk = {"maful": "مفعول به", "majrur": "مجرور", "zarf": "ظرف", "masdar": "مصدر"}
    fd = {"liajlih": "مفعول لأجله", "mutlaq": "مفعول مطلق", "hal": "حال", "unread": "—"}

    def cells(s: str) -> tuple[Cell, ...]:
        return tuple(_cell(int(i)) for i in s.split("-")) if s else ()

    orders = [r for r in rows if r[0] == "order"]
    assert len(orders) == len(WITNESSES) == 6
    for r, j in zip(orders, WITNESSES.values(), strict=True):
        assert (j.fil, j.fail, j.maful) == (cells(r[2]), cells(r[3]), cells(r[4])), r[1]
        assert order(j) == ru[r[5]] and admissible(j) == (r[6] == "true"), r[1]
    for r in rows:
        if r[0] == "majhul":
            op = majhul(cells_of("كَتَبَ")) if r[1] == "kataba" else majhul_pres(cells_of("يَكْتُبُ"))
            assert op == cells(r[2]), r[1]
        elif r[0] == "naib":
            assert naib_kind(cells(r[1])) == nk[r[2]], r[1]
        elif r[0] == "fadla":
            assert sort_fadla(cells(r[1]), cells(r[2])) == fd[r[3]], r[1]
