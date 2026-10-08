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
    """الأوزانُ المودَعة (125) بميزانها خاناتٍ، ترخيصُها، وردُّها الأصلَ = جدولُ `Wazn.awzan`."""

    from slge.wazn import AWZAN, FAL, mizan, root_of

    rows = _rows("wazn.csv")
    assert len(rows) == len(AWZAN) == 125
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
    assert len(rows) == len(CLASSICAL) == 124 and names[29] == ROOT
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


def test_shibh_matches_lean() -> None:
    """الصورتان والزائدُ والمرتكزُ والمحلُّ والكونُ المحذوف على الشواهد = جدولُ `Shibh`."""

    from slge.shibh import anchor, kawn, kind, mahall
    from slge.tawabi import case_class

    rows = _rows("shibh.csv")
    kk = {"jarrMajrur": "جار ومجرور", "zarf": "ظرف", "none": "—"}
    an = {"verb": "فعل", "derived": "مشتق", "kawn": "كون محذوف"}
    mh = {"khabar": "خبر", "naat": "نعت", "hal": "حال", "sila": "صلة", "unread": "—"}

    def cells(s: str) -> tuple[Cell, ...]:
        return tuple(_cell(int(i)) for i in s.split("-")) if s else ()

    assert len(rows) == 5 + 1 + 3 + 4 + 4
    for r in rows:
        if r[0] == "kind":
            assert kind(cells(r[1])) == kk[r[2]], r
        elif r[0] == "zaid":
            assert r[1] == r[2] and case_class(cells(r[1])) == "رفع"
        elif r[0] == "anchor":
            assert anchor(cells(r[1])) == an[r[2]], r
        elif r[0] == "mahall":
            assert mahall(cells(r[1])) == mh[r[2]], r
        elif r[0] == "kawn":
            assert kawn(mh[r[1]]) == cells(r[2]), r


def test_nisab_matches_lean() -> None:
    """سلاسلُ الأوزان وأبعادُها، والنسبةُ المقروءةُ على الشواهد = جدولُ `Nisab`."""

    from slge.nisab import chain, dist, nisba

    rows = _rows("nisab.csv")
    nn = {"isnad": "إسناد", "taqyid": "تقييد", "unread": "—"}
    chains = [r for r in rows if r[0] == "chain"]
    assert len(chains) == 125
    for r in chains:
        k = int(r[1])
        assert chain(k) == [int(x) for x in r[2].split("-")] and dist(k) == int(r[3]), r
    for r in rows:
        if r[0] == "nisba":
            a = tuple(_cell(int(i)) for i in r[1].split("-"))
            b = tuple(_cell(int(i)) for i in r[2].split("-"))
            assert nisba(a, b) == nn[r[3]], r


def test_talil_matches_lean() -> None:
    """أزواجُ السببيّة الاشتقاقيّة، وأدواتُ التعليل، والتعليلُ المقروء، والتنازعُ = جدولُ `Talil`."""

    from slge.nisab import dist
    from slge.talil import TOOLS, derives, talil, tanazu
    from slge.wazn import AWZAN

    rows = _rows("talil.csv")
    tn = {"liAnna": "لأنّ", "liajlih": "مفعول لأجله", "biHarf": "تعليل بالحرف", "unread": "—"}
    an = {"jarr": "جرّ", "inna": "إنّ", "nasbFil": "نصب الفعل"}
    got = {(int(r[1]), int(r[2])) for r in rows if r[0] == "derives"}
    n = len(AWZAN)
    assert got == {(a, b) for a in range(n) for b in range(n) if derives(a, b)}
    assert len(got) == 345  # 339 قبل قوالب الاسم الأربعة
    for r in rows:
        if r[0] == "derives":
            assert dist(int(r[2])) == int(r[3]) < dist(int(r[1])), r
        elif r[0] == "tool":
            name, cells, amal = r[1], tuple(_cell(int(i)) for i in r[2].split("-")), an[r[3]]
            assert (name, cells, amal) in TOOLS, r
        elif r[0] == "talil":
            a = tuple(_cell(int(i)) for i in r[1].split("-"))
            b = tuple(_cell(int(i)) for i in r[2].split("-"))
            assert talil(a, b) == tn[r[3]], r
        elif r[0] == "tanazu":
            v1, v2, w = (tuple(_cell(int(i)) for i in x.split("-")) for x in r[1:4])
            assert tanazu(v1[:-1], v2, (*w[:-1], ("ر", "ضم")), v1[-1:]) == (v1, v2, w), r
    assert sum(r[0] == "tool" for r in rows) == len(TOOLS) == 6


def test_maqam_matches_lean() -> None:
    """الشخصُ من الصدر على الميزان لكلّ قالب، والشواهدُ (الشخصُ والظهورُ والتوكيد) = جدولُ `Maqam`."""

    from slge.maqam import PRESENT_TEMPLATES, shakhs, tawkid, with_prefix, zuhur
    from slge.wazn import AWZAN, mizan

    rows = _rows("maqam.csv")
    sn = {"mutakallim": "متكلم", "mukhatab": "مخاطب", "ghaib": "غائب", "ta": "مخاطب/غائبة",
          "none": None}
    zn = {"zahir": "ظاهر", "mustatir": "مستتر", "muttasil": "متصل"}
    pre = {"0": "ء", "25": "ن", "3": "ت", "28": "ي"}
    presents = [r for r in rows if r[0] == "present"]
    assert len(presents) == 4 * len(PRESENT_TEMPLATES)
    for r in presents:
        v = with_prefix(pre[r[2]], mizan(AWZAN[int(r[1])].template))
        assert v == tuple(_cell(int(i)) for i in r[3].split("-")) and shakhs(v) == sn[r[4]], r
    for r in rows:
        if r[0] == "shakhs":
            assert shakhs(tuple(_cell(int(i)) for i in r[1].split("-"))) == sn[r[2]], r
        elif r[0] == "zuhur":
            v = tuple(_cell(int(i)) for i in r[1].split("-"))
            n = tuple(_cell(int(i)) for i in r[2].split("-")) if r[2] else None
            assert zuhur(v, n) == zn[r[3]], r
        elif r[0] == "tawkid":
            v = tuple(_cell(int(i)) for i in r[1].split("-"))
            d = tuple(_cell(int(i)) for i in r[2].split("-"))
            assert tawkid(v, d) == (r[3] == "true"), r
    assert sum(r[0] == "tawkid" for r in rows) == 8 and sum(r[0] == "zuhur" for r in rows) == 4


def test_jiha_matches_lean() -> None:
    """الصيغةُ على الميزان لكلّ قالب (الماضي والأمر والمضارع بصدوره)، والجهةُ على الشواهد = `Jiha`."""

    from slge.jiha import jiha, sigha

    rows = _rows("jiha.csv")
    gn = {"madi": "ماضٍ", "mudari": "مضارع", "amr": "أمر", "none": None}
    jn = {"madi": "ماضٍ", "mudari": "مضارع", "mustaqbal": "مستقبل", "madiManfi": "ماضٍ منفيّ",
          "mustaqbalManfi": "مستقبل منفيّ", "madiMustamirr": "ماضٍ مستمرّ", "amr": "أمر",
          "unread": "—"}
    assert sum(r[0] == "sigha" for r in rows) == 13 + 11 + 4 * 13
    for r in rows:
        if r[0] == "sigha":
            assert sigha(tuple(_cell(int(i)) for i in r[2].split("-"))) == gn[r[3]], r
        elif r[0] == "jiha":
            a = tuple(_cell(int(i)) for i in r[1].split("-")) if r[1] else ()
            b = tuple(_cell(int(i)) for i in r[2].split("-"))
            assert jiha(a, b) == jn[r[3]], r
    assert sum(r[0] == "jiha" for r in rows) == 11


def test_naat_matches_lean() -> None:
    """المتّجهُ الرباعيّ والنعتُ والحملُ والمحلُّ على الشواهد = جدولُ `Naat`."""

    from slge.naat import haml_kind, jumla_mahall, naat, naat_ok, vec

    rows = _rows("naat.csv")
    cn = {"raf": "رفع", "nasb": "نصب", "jarr": "جرّ", "nasbJarr": "نصب/جرّ",
          "unread": "لا تقرؤه الخانة"}
    gn, nn = {"masc": "مذكر", "fem": "مؤنث"}, {"single": "مفرد", "dual": "مثنى", "plural": "جمع"}
    hn = {"naat": "نعت", "khabar": "خبر", "unread": "—"}
    mn = {"naat": "نعت", "hal": "حال", "unread": "—"}

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-"))

    for r in rows:
        if r[0] == "vec":
            assert vec(cells(r[1])) == (cn[r[2]], r[3] == "true", gn[r[4]], nn[r[5]]), r
        elif r[0] == "naat":
            m, k = cells(r[1]), cells(r[2])
            assert naat(m, k) == cells(r[3]) and naat_ok(m, naat(m, k)) == (r[4] == "true"), r
        elif r[0] == "haml":
            m, n = cells(r[1]), cells(r[2])
            assert naat_ok(m, n) == (r[3] == "true") and haml_kind(m, n) == hn[r[4]], r
        elif r[0] == "mahall":
            assert jumla_mahall(cells(r[1])) == mn[r[2]], r
    assert sum(r[0] == "vec" for r in rows) == 12 and sum(r[0] == "haml" for r in rows) == 5


def test_uslub_matches_lean() -> None:
    """الأدواتُ، ولَا على كلّ قالبِ مضارعٍ بصدوره مجزومًا ومرفوعًا، والأسلوبُ على الشواهد = جدولُ `Uslub`."""

    from slge.uslub import LA, TOOLS, truth_apt, uslub

    rows = _rows("uslub.csv")
    un = {"khabar": "خبر", "amr": "أمر", "nahy": "نهي", "istifham": "استفهام", "nida": "نداء",
          "tamanni": "تمنّ", "tarajji": "ترجّ", "taajjub": "تعجّب", "madhDhamm": "مدح وذمّ",
          "unread": "—"}

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-")) if x else ()

    assert sum(r[0] == "la" for r in rows) == 104 and sum(r[0] == "tool" for r in rows) == 14
    for r in rows:
        if r[0] == "tool":
            assert (r[1], cells(r[2]), un[r[3]]) in TOOLS, r
        elif r[0] == "la":
            assert uslub(LA, cells(r[1])) == un[r[2]], r
        elif r[0] == "uslub":
            u = uslub(cells(r[1]), cells(r[2]), cells(r[3]) if r[3] else None)
            assert u == un[r[4]] and truth_apt(u) == (r[5] == "true"), r


def test_talab_matches_lean() -> None:
    """أسماءُ الفعل، ولامُ الأمر على كلّ قالبِ مضارعٍ بصدوره (مكسورةً وساكنة)، والشواهد = `Talab`."""

    from slge.talab import ISM_FIL, WAW, talab

    rows = _rows("talab.csv")
    sn = {"sigha": "صيغة", "lam": "لام", "masdar": "مصدر", "ismFil": "اسم فعل", "none": None}

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-")) if x else ()

    assert sum(r[0] == "lam" for r in rows) == 52 == sum(r[0] == "lamWaw" for r in rows)
    for r in rows:
        if r[0] == "ismFil":
            assert (r[1], cells(r[2])) in ISM_FIL and talab((), cells(r[2])) == sn[r[3]], r
        elif r[0] == "lam":
            assert talab((), cells(r[1])) == sn[r[2]], r
        elif r[0] == "lamWaw":
            assert talab(WAW, cells(r[1])) == sn[r[2]], r
        elif r[0] == "talab":
            assert talab(cells(r[1]), cells(r[2])) == sn[r[3]], r
    assert sum(r[0] == "talab" for r in rows) == 10 and sum(r[0] == "ismFil" for r in rows) == 8


def test_kulli_matches_lean() -> None:
    """الجهةُ الوجوديّة على الميزان لكلّ قالب، وعلى الجزئيّات المجدوَلة، وعلى الشواهد = جدولُ `Kulli`."""

    from slge.kulli import kulli

    rows = _rows("kulli.csv")
    kn = {"juzi": "جزئيّ", "aradi": "كليّ عرضيّ", "hadath": "حدث مجرّد", "fil": "حدث مهيّأ",
          "jamid": "كليّ ماهويّ", "unread": "—"}

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-"))

    assert sum(r[0] == "mizan" for r in rows) == 125 and sum(r[0] == "table" for r in rows) == 51
    for r in rows:
        if r[0] == "mizan":
            assert kulli(cells(r[2])) == kn[r[3]], r
        elif r[0] in ("table", "kulli"):
            assert kulli(cells(r[1])) == kn[r[2]], r



def test_wad_matches_lean() -> None:
    """معاني الميزان وصورُه وقراءتُه لكلّ قالب، وأزواجُ الالتقاء، والمتطابقات، والشواهد = جدولُ `Wad`."""

    from slge.marifa import drop_tanwin
    from slge.wad import classes, collision_pairs, duplicates, senses, wad

    rows = _rows("wad.csv")
    kn = {"majdul": "مجدوَل", "mufrad": "مفرد الوضع", "wadMushtarak": "مشترك الوضع",
          "suraMushtarak": "مشترك الصورة", "unread": "—"}

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-"))

    def ks(x: str) -> tuple[int, ...]:
        return tuple(int(i) for i in x.split("+")) if x else ()

    assert sum(r[0] == "mizan" for r in rows) == 125 and sum(r[0] == "wad" for r in rows) == 12
    assert tuple((int(r[1]), int(r[2])) for r in rows if r[0] == "pair") == collision_pairs()
    assert tuple((int(r[1]), int(r[2])) for r in rows if r[0] == "dup") == duplicates()
    for r in rows:
        if r[0] == "mizan":
            m = cells(r[2])
            assert senses(m) == ks(r[3]) and classes(m) == ks(r[4]) and wad(m) == kn[r[5]], r
        elif r[0] == "wad":
            w = cells(r[1])
            assert senses(drop_tanwin(w)) == ks(r[2]) and wad(w) == kn[r[3]], r


def test_tabayun_matches_lean() -> None:
    """موادُّ الميزان وعزلةُ القالب لكلّ قالب، وعلاقاتُ الشواهد = جدولُ `Tabayun`."""

    from slge.tabayun import isolated, mawadd, rel

    rows = _rows("tabayun.csv")
    rn = {"munfarid": "منفرد", "mushtarak": "مشترك", "ittihad": "متّحدا المادّة",
          "mutabayin": "متباينان", "mutadakhil": "متداخلان", "unread": "—"}

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-"))

    assert sum(r[0] == "mizan" for r in rows) == 125 and sum(r[0] == "rel" for r in rows) == 9
    for r in rows:
        if r[0] == "mizan":
            m = cells(r[2])
            assert isolated(int(r[1])) == (r[3] == "true"), r
            assert mawadd(m) == (("ف", "ع", "ل"),) * int(r[4]), r
        elif r[0] == "rel":
            assert rel(cells(r[1]), cells(r[2])) == rn[r[3]], r


def test_madd_matches_lean() -> None:
    """الأصنافُ والترخيصُ الثلاثيّ والثنائيّ ومدودُ الميزان لكلّ قالب، والشواهدُ بسياقها = جدولُ `Madd`."""

    from slge.madd import binary_ok, continue_licensed, has_vc, kinds, madd, pause_licensed

    rows = _rows("madd.csv")
    mn = {"tabii": "طبيعيّ", "muttasil": "متّصل", "munfasil": "منفصل", "lazimThaqil": "لازم مثقَّل",
          "lazimKhafif": "لازم مخفَّف", "arid": "عارض", "lin": "لين", "silaSughra": "صلة صغرى",
          "silaKubra": "صلة كبرى", "silent": "محجوب"}

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-")) if x else ()

    def hits(x: str) -> list[tuple[int, str]]:
        return [(int(h.split(":")[0]), mn[h.split(":")[1]]) for h in x.split("+")] if x else []

    assert sum(r[0] == "mizan" for r in rows) == 125 and sum(r[0] == "madd" for r in rows) == 15
    for r in rows:
        if r[0] == "mizan":
            m = cells(r[2])
            assert "".join(kinds(m)) == r[3], r
            flags = (continue_licensed(m), pause_licensed(m), binary_ok(m))
            assert flags == tuple(x == "true" for x in r[4:7]), r
            assert madd(m, (), False) == hits(r[7]) and madd(m, (), True) == hits(r[8]), r
        elif r[0] == "madd":
            w, n, p = cells(r[1]), cells(r[2]), r[3] == "true"
            assert madd(w, n, p) == hits(r[4]), r
            assert (binary_ok(w), has_vc(w)) == (r[5] == "true", r[6] == "true"), r


def test_jidh_matches_lean() -> None:
    """تسويةُ الآخر على الميزان لكلّ قالبٍ وحالة، وقراءاتُ الشواهد (السوابق، أل، الجذع، اللاحقة،
    القوالب) = جدولُ `Jidh`."""

    from slge.jidh import jidh, last_state, on_template_mod, stem_senses
    from slge.wazn import AWZAN
    from slge.zuruf import set_last

    rows = _rows("jidh.csv")
    st_of = {"0": "فتح", "1": "كسر", "2": "ضم", "3": "سكون"}

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-")) if x else ()

    assert sum(r[0] == "mizan" for r in rows) == 125 and sum(r[0] == "jidh" for r in rows) == 10
    readings: dict[str, list[list[str]]] = {}
    for r in rows:
        if r[0] == "mizan":
            k, m = int(r[1]), cells(r[2])
            assert st_of[r[3]] == last_state(AWZAN[k].template), r
            hits = "".join("1" if on_template_mod(k, set_last(m, st)) else "0"
                           for st in st_of.values())
            assert hits == r[4], r
            want_ts = tuple(int(x) for x in r[5].split("+") if x)
            assert stem_senses(set_last(m, "كسر")) == want_ts, r
        elif r[0] == "reading":
            readings.setdefault(r[1], []).append(r[2:])
    for r in rows:
        if r[0] == "jidh":
            got = jidh(cells(r[1]))
            assert len(got) == int(r[2]), r
            want = readings.get(r[1], [])
            def key(cs: tuple[tuple[str, str], ...]) -> str:
                return "-".join(str(index(c)) for c in cs)

            mine = [[key(tuple(c for p in x.pre for c in p)), str(x.al), key(x.stem), key(x.suf),
                     "+".join(str(t) for t in x.templates), key(x.restore()), key(x.asl),
                     _chain(x.ilal)] for x in got]
            assert mine == want, (r, mine, want)


def _chain(ch: tuple[tuple[str, int], ...]) -> str:
    from slge.ilal import RULES

    return "+".join(f"{RULES.index(rule)}:{i}" for rule, i in ch)


def test_ilal_matches_lean() -> None:
    """الصعودُ والنزولُ لكلّ قاعدةٍ وموضعٍ على كلمات الشواهد، والنزولُ حتى خطوتين بسلاسله = جدولُ "
    "`Ilal`."""

    from slge.ilal import RULES, apply, descend, record, restore, undo

    rows = _rows("ilal.csv")

    def cells(x: str) -> tuple[tuple[str, str], ...]:
        return tuple(_cell(int(i)) for i in x.split("-")) if x else ()

    def key(cs: tuple[tuple[str, str], ...]) -> str:
        return "-".join(str(index(c)) for c in cs)

    n_apply = n_undo = n_record = 0
    descents: dict[str, list[tuple[str, str]]] = {}
    for r in rows:
        if r[0] == "apply":
            got = apply(RULES[int(r[1])], cells(r[2]), int(r[3]))
            assert ("-" if got is None else key(got)) == r[4], r
            n_apply += 1
        elif r[0] == "undo":
            us = undo(RULES[int(r[1])], cells(r[2]), int(r[3]))
            assert "|".join(key(u) for u in us) == r[4], r
            n_undo += 1
        elif r[0] == "record":
            rule, u, i = RULES[int(r[1])], cells(r[2]), int(r[3])
            rc = record(rule, u, i)
            assert (str(rc[0]), str(rc[1]), key(rc[2])) == (r[4], r[5], r[6]), r
            v = apply(rule, u, i)
            assert v is not None and key(restore(v, rc)) == r[7] == key(u), r  # roundtrip
            n_record += 1
        elif r[0] == "descend":
            descents.setdefault(r[1], []).append((r[2], r[3]))
    assert n_apply == n_undo > 1000 and len(descents) >= 15 and n_record == 12
    for w, want in descents.items():
        mine = [(_chain(ch), key(u)) for ch, u in descend(cells(w), len(cells(w)))]
        assert mine == want, (w, mine, want)


def test_maqayis_matches_lean() -> None:
    """جدولُ المقاييس مفكوكًا، والعضويّةُ على شبكة 125 جذرًا وعلى الشواهد، وترتيبُ قراءات الشواهد بالقرينة
    وجذورُها = جدولُ `Maqayis`."""

    from slge.jidh import jidh
    from slge.maqayis import ROOTS, attested, decode, member, rank, roots_of

    rows = _rows("maqayis.csv")

    def cells(x: str) -> tuple[Cell, ...]:
        return tuple(_cell(int(i)) for i in x.split("-")) if x else ()

    def key(cs: tuple[Cell, ...]) -> str:
        return "-".join(str(index(c)) for c in cs)

    codes = [r for r in rows if r[0] == "code"]
    assert rows[0][0] == "size" and int(rows[0][1]) == len(codes) == len(ROOTS) == 4561
    assert [int(r[1]) for r in codes] == list(ROOTS)
    for r in codes:
        assert decode(int(r[1])) == (int(r[2]), int(r[3]), int(r[4])), r
    members = [r for r in rows if r[0] == "member"]
    assert len(members) == 137 and {r[4] for r in members} == {"true", "false"}
    for r in members:
        root = tuple(ALPHABET[int(x)] for x in r[1:4])
        assert member(root) == (r[4] == "true"), r  # type: ignore[arg-type]
    readings: dict[str, list[list[str]]] = {}
    for r in rows:
        if r[0] == "reading":
            readings.setdefault(r[1], []).append(r[2:])
    n_rank = 0
    for r in rows:
        if r[0] == "rank":
            n_rank += 1
            got = rank(jidh(cells(r[1])))
            assert len(got) == int(r[2]), r
            mine = [[str(attested(x)).lower(), key(x.asl), "+".join(str(t) for t in x.templates),
                     "+".join(".".join(str(ALPHABET.index(c)) for c in ro) for ro in roots_of(x))]
                    for x in got]
            assert mine == readings.get(r[1], []), (r, mine)
    assert n_rank == 12


def test_abniya_matches_lean() -> None:
    """هيكلُ كلّ قالبٍ وعضويّتُه في أبنية سيبويه، وتمايزُ كلّ زوجين، والأزواجُ المسمّاة = جدولُ `Abniya`."""

    from slge.abniya import AMBIGUOUS, SKELETONS, in_abniya, separated, skeleton_of
    from slge.wazn import AWZAN

    rows = _rows("abniya.csv")
    assert rows[0] == ["size", str(len(SKELETONS))] and len(SKELETONS) == 158
    skel = [r for r in rows if r[0] == "skel"]
    assert len(skel) == len(AWZAN) == 125
    for r in skel:
        t = AWZAN[int(r[1])].template
        assert "-".join(str(x) for x in skeleton_of(t)) == r[2], r
        assert in_abniya(t) == (r[3] == "true"), r
    seps = [r for r in rows if r[0] == "sep"]
    assert len(seps) == 125 * 124 // 2
    for r in seps:
        k, q = int(r[1]), int(r[2])
        assert separated(AWZAN[k].template, AWZAN[q].template) == (r[3] == "true"), r
    assert [(int(r[1]), int(r[2])) for r in rows if r[0] == "amb"] == list(AMBIGUOUS)


def test_adawat_matches_lean() -> None:
    """لكلّ أداة: الصورةُ والرتبةُ والأصنافُ والعملُ على شاهدين ونوعُ العلاقة، والترتيبُ على الشواهد = جدولُ
    `Adawat`."""

    from slge.adawat import TABLE_ADAWAT, apply, cat_of, fits, of_cells, rank
    from slge.jidh import jidh
    from slge.maqayis import rank as rank_maqayis

    rows = _rows("adawat.csv")
    cat = {"اسم": "ism", "فعل": "fil", "جملة": "jumla", "أيّ": "ay"}
    rel = {"تعدية": "taadiya", "استثناء": "istithna", "تقليل": "taqlil", "توكيد": "tawkid",
           "تشبيه": "tashbih", "استدراك": "istidrak", "تمنٍّ": "tamanni", "ترجٍّ": "tarajji",
           "نداء": "nida", "نفي": "nafy", "معيّة": "maiyya", "مصدريّة": "masdariyya", "جزاء": "jaza",
           "أمر": "amr", "نهي": "nahy", "شرط": "shart", "تنفيس": "tanfis", "ردع": "rad",
           "تحقيق": "tahqiq", "جمع": "jam", "ترتيب وتعقيب": "tartibTaqib",
           "ترتيب وتراخٍ": "tartibTarakhi", "غاية": "ghaya", "تخيير": "takhyir", "إضراب": "idrab",
           "استفهام": "istifham", "استفتاح": "istiftah"}

    def cells(x: str) -> tuple[Cell, ...]:
        return tuple(_cell(int(i)) for i in x.split("-")) if x else ()

    def key(cs: tuple[Cell, ...]) -> str:
        return "-".join(str(index(c)) for c in cs)

    kitabu, yaktubu = cells("89-12-7-10"), cells("112-91-14-10")  # كِتَابُ، يَكْتُبُ
    adat = [r for r in rows if r[0] == "adat"]
    assert len(adat) == len(TABLE_ADAWAT) == 68
    for r in adat:
        a = TABLE_ADAWAT[int(r[1])]
        assert key(a.harf.cells) == r[2] and a.arity == int(r[3]), r
        assert "+".join(cat[x] for x in a.args) == r[4], r
        assert r[5] == f"Slge.Adawat.Rel.{rel[a.rel]}", r
        assert key(apply(a, kitabu)) == r[6] and key(apply(a, yaktubu)) == r[7], r
    ranks = [r for r in rows if r[0] == "rank"]
    assert len(ranks) == 6
    for r in ranks:
        found = of_cells(cells(r[2]))
        if r[3] == "none":
            assert found is None, r
            continue
        assert found is not None
        a = found
        rs = rank(a, rank_maqayis(jidh(cells(r[1]))))
        assert len(rs) == int(r[3]), r
        mine = "+".join(("1" if fits(a, x) else "0") + "." + cat[cat_of(x)] for x in rs)
        assert mine == r[4], (r, mine)


def test_wujud_matches_lean() -> None:
    """جهةُ كلّ قالبٍ وقراءةُ الكليّ لميزانه وأبوه في الشبكة، وجهةُ قراءات الشواهد = جدولُ `Wujud`."""

    from slge.jidh import jidh
    from slge.kulli import kulli
    from slge.shabaka import CLASSICAL
    from slge.wazn import AWZAN, mizan
    from slge.wujud import ONT, ont_of, ont_of_reading

    rows = _rows("wujud.csv")
    on = {"فعل": "fil", "مصدر": "masdar", "وصف": "wasf", "ظرف وآلة": "zarfAla", "جمع": "jam",
          "اسم": "ism"}
    kn = {"جزئيّ": "juzi", "كليّ عرضيّ": "aradi", "حدث مجرّد": "hadath", "حدث مهيّأ": "fil",
          "كليّ ماهويّ": "jamid", "—": "unread"}
    names = [w.name for w in AWZAN]
    ont = [r for r in rows if r[0] == "ont"]
    assert len(ont) == len(ONT) == 125
    for r in ont:
        k = int(r[1])
        assert on[ont_of(k)] == r[2] and kn[kulli(mizan(AWZAN[k].template))] == r[3], r
        parent = CLASSICAL.get(names[k])
        assert (str(names.index(parent)) if parent else "-") == r[4], r
    readings = [r for r in rows if r[0] == "reading"]
    assert len(readings) == 7
    for r in readings:
        w = tuple(_cell(int(i)) for i in r[1].split("-"))
        assert "+".join(on[ont_of_reading(x)] for x in jidh(w)) == r[2], r


def test_maani_matches_lean() -> None:
    """معاني كلّ حرفٍ بترتيب المصدر، والترتيبُ بالقرينتين على شواهد، وظرفيّةُ صورٍ = جدولُ `Maani`."""

    from slge.maani import is_zarf, rank, senses_of
    from slge.maani_table import SENSES, TABLE

    lean = {"ابتداء الغاية في الزمان": "ibtidaGhayaZaman", "ابتداء الغاية": "ibtidaGhaya",
            "انتهاء الغاية": "intihaGhaya", "التبعيض": "tabid", "بيان الجنس": "bayanJins",
            "زائدة": "zaida", "بمعنى مع": "maa", "الظرفية": "zarfiyya", "بمعنى على": "ala",
            "التجوّز": "tajawwuz", "الإلصاق": "ilsaq", "الاستعانة": "istiana",
            "المصاحبة": "musahaba",
            "بمعنى من أجل": "minAjl", "بمعنى في": "fi", "الاختصاص": "ikhtisas", "التقليل": "taqlil",
            "القسم": "qasam", "الاستعلاء": "istila", "المباعدة": "mubaada", "التشبيه": "tashbih",
            "مطلق الجمع": "mutlaqJam", "الترتيب والتعقيب": "tartibTaqib",
            "الترتيب والتراخي": "tartibTarakhi", "المعطوف جزء من المعطوف عليه": "juzMinMatuf",
            "الترتيب": "tartib", "تعليق الحكم بأحد المذكورين": "taliqBiAhad", "الشك": "shakk",
            "التخيير": "takhyir", "الإباحة": "ibaha", "مخالفة المعطوف عليه في حكمه": "mukhalafa",
            "نفي الحال": "nafyHal", "نفي المستقبل": "nafyMustaqbal", "النهي": "nahy",
            "الدعاء": "dua",
            "قلب المضارع إلى الماضي": "qalbMadi", "تأكيد المستقبل": "takidMustaqbal"}
    assert set(lean) == set(SENSES)
    rows = _rows("maani.csv")
    senses = [r for r in rows if r[0] == "senses"]
    assert len(senses) == len(TABLE) == 29
    for r in senses:
        assert "+".join(lean[s] for s in senses_of(int(r[1]))) == r[2], r
    ranks = [r for r in rows if r[0] == "rank"]
    assert len(ranks) == 20
    for r in ranks:
        mine = rank(senses_of(int(r[1])), nafy_before=r[2] == "true", zarf_after=r[3] == "true")
        assert "+".join(lean[s] for s in mine) == r[4], r
    zarf = [r for r in rows if r[0] == "zarf"]
    assert len(zarf) == 4 and [r[2] for r in zarf] == ["true", "true", "false", "false"]
    for r in zarf:
        assert str(is_zarf(tuple(_cell(int(i)) for i in r[1].split("-")))).lower() == r[2], r


def test_mukhassas_matches_lean() -> None:
    """الشجرةُ (معرّف، مستوى، أب، كتاب، جذور)، والقابليّاتُ الموروثة لكلّ كتاب، والحكمُ على شواهد = جدولُ
    `Mukhassas`."""

    from slge.mukhassas import BOOKS, NODES, judge_in

    rows = _rows("mukhassas.csv")
    nodes = [r for r in rows if r[0] == "node"]
    assert len(nodes) == len(NODES) == 1600
    for r in nodes:
        n = NODES[int(r[1])]
        assert (n[1], n[2], n[5]) == (int(r[2]), int(r[3]), int(r[4])), r
        assert [str(c) for c in n[4]] == ([] if r[5] == "" else r[5].split("+")), r
    under = [r for r in rows if r[0] == "under"]
    assert len(under) == len(BOOKS) == 73
    for r in under:
        mine = BOOKS[int(r[1])]
        lean = [] if r[2] == "" else [int(x) for x in r[2].split("+")]
        assert sorted(set(lean)) == sorted(mine) and len(lean) >= len(mine), r
    judged = [r for r in rows if r[0] == "judge"]
    assert len(judged) == 5
    for r in judged:
        g, w = judge_in(int(r[1]), int(r[2]))
        assert (f"mafhum:{w}" if g == "مفهوم" else "malumah") == r[3], r


def test_zawaid_matches_lean() -> None:
    """حروفُ الزوائد العشرة وخاناتُها الأربعون واللواحقُ الثلاث، وإلصاقُ النون والتاء على شواهد = جدولُ
    `Zawaid`؛ والجدولُ المنقول وشواهدُ القرآن حواملَ = `zawaid_table`."""

    from slge.zawaid import (
        CELLS,
        KHAFIFA,
        LETTERS,
        MUDARAA,
        TA_TANITH,
        THAQILA,
        WITNESSES,
        anith,
        has_tanwin_shape,
        tawkid,
    )
    from slge.zawaid_table import TABLE

    def cells(x: str) -> tuple[Cell, ...]:
        return tuple(_cell(int(i)) for i in x.split("-")) if x else ()

    def key(cs: tuple[Cell, ...]) -> str:
        return "-".join(str(index(c)) for c in cs)

    heads = ("letters", "mudaraa", "cells", "thaqila", "khafifa", "taTanith")
    rows = {r[0]: r for r in _rows("zawaid.csv") if r[0] in heads}
    assert [ALPHABET[int(i)] for i in rows["letters"][1].split("+")] == list(LETTERS)
    assert [ALPHABET[int(i)] for i in rows["mudaraa"][1].split("+")] == list(MUDARAA)
    assert cells(rows["cells"][1]) == CELLS and len(CELLS) == 40
    assert (cells(rows["thaqila"][1]), cells(rows["khafifa"][1]), cells(rows["taTanith"][1])) == (
        THAQILA, KHAFIFA, TA_TANITH)
    table = [r for r in _rows("zawaid.csv") if r[0] == "table"]
    assert len(table) == len(TABLE) == 10
    for r, (_, letter, pos, exs, _) in zip(table, TABLE, strict=True):
        assert ALPHABET[int(r[1])] == letter
        assert ([] if r[2] == "" else [int(p) for p in r[2].split("+")]) == list(pos)
        assert len([] if r[3] == "" else r[3].split("|")) == len(exs)
    wit = [r for r in _rows("zawaid.csv") if r[0] == "witness"]
    assert len(wit) == sum(len(ws) for _, ws in WITNESSES) == 48
    ops = [r for r in _rows("zawaid.csv") if r[0] in ("tawkid", "anith", "tanwin")]
    assert len(ops) == 6 * 4
    for r in ops:
        w = cells(r[1])
        if r[0] == "tawkid":
            got = tawkid(w, r[2] == "1")
            assert key(got) == r[3] and str(licensed(got)).lower() == r[4], r
        elif r[0] == "anith":
            got = anith(w)
            assert key(got) == r[2] and str(licensed(got)).lower() == r[3], r
        else:
            assert str(has_tanwin_shape(tawkid(w, False))).lower() == r[2], r


def test_makharij_matches_lean() -> None:
    """ترتيبُ سيبويه والمخارجُ والصفاتُ والساقطُ = جدولُ `Makharij`."""

    from slge.makharij import BAYN, MAKHARIJ, MISSING, ORDER, SIFAT, STATED_COUNT

    rows = _rows("makharij.csv")
    by = {r[0]: r for r in rows if r[0] in ("order", "stated", "missing")}
    assert [ALPHABET[int(i)] for i in by["order"][1].split("+")] == list(ORDER)
    assert int(by["stated"][1]) == STATED_COUNT
    assert [ALPHABET[int(i)] for i in by["missing"][1].split("+")] == list(MISSING)
    mk = [r for r in rows if r[0] == "makhraj"]
    assert len(mk) == len(MAKHARIJ) == 15
    for r in mk:
        assert tuple(ALPHABET[int(i)] for i in r[2].split("+")) == MAKHARIJ[int(r[1])][1], r
    for r in (r for r in rows if r[0] == "sifa"):
        mine = BAYN if r[1] == "bayn" else SIFAT[r[1]][1]
        assert tuple(ALPHABET[int(i)] for i in r[2].split("+")) == mine, r


def test_ilal_bab_matches_lean() -> None:
    """أبوابُ الإعلال: القاعدةُ وسطرُها وشاهدُها وصورةُ المصحف وموضعُها وقراءتُها = جدولُ `IlalBab`."""

    from slge.ilal import RULES
    from slge.ilal_bab import DEBTS, TABLE, reads

    rows = _rows("ilal_bab.csv")
    got = [r for r in rows if r[0] == "row"]
    # رسمُ الشاهد خشنًا كما أودعته الأداة: الهمزةُ بصورها ألفٌ، ة→ت، ى→ا.
    coarse = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "آ": "ءا", "ة": "ت", "ى": "ا"}
    assert len(got) == len(TABLE) == 13
    for r, mine in zip(got, TABLE, strict=True):
        rule, _, line, word, cells, at, _ = mine
        assert RULES[int(r[1])] == rule and int(r[2]) == line, r
        rasm = "".join(coarse.get(ch, ch) for ch in word).replace("ء", "ا")
        assert [ALPHABET[int(i)] for i in r[3].split("+")] == [c for c in rasm if c in ALPHABET], r
        key = "-".join(str(index(c)) for c in (cells or ()))
        assert r[4] == key and int(r[5]) == (at or 0), r
        assert (r[6] == "true") == reads(mine), r
    assert [int(r[1]) for r in rows if r[0] == "debt"] == [n for _, n in DEBTS]


def test_pipeline_matches_lean() -> None:
    """قمعُ السُّلَّم صارمًا ومرتَّبًا = جدولُ `PipelineTable`، والمراحلُ خمس."""

    from slge.pipeline import STAGES
    from slge.pipeline_table import RANKED, STRICT

    by = {r[0]: r[1] for r in _rows("pipeline.csv")}
    assert tuple(int(x) for x in by["strict"].split("+")) == STRICT
    assert tuple(int(x) for x in by["ranked"].split("+")) == RANKED
    assert int(by["stages"]) == len(STAGES) == len(STRICT) - 1 == 5


def test_hasm_matches_lean() -> None:
    """حدُّ التكرار وعددُ الجذور وثلاثُ كلماتٍ (قراءات، قسمات، القسمةُ المحسومة) = `Hasm` في Lean."""

    from slge.hasm import BOUND, hasm, segments
    from slge.hasm_table import ROOT_FREQ
    from slge.jidh import jidh

    rows = _rows("hasm.csv")
    by = {r[0]: r for r in rows if r[0] in ("bound", "roots")}
    assert int(by["bound"][1]) == BOUND and int(by["roots"][1]) == len(ROOT_FREQ)
    for r in (r for r in rows if r[0] == "word"):
        w = tuple(CELLS[int(i)] for i in r[2].split("-"))
        rs = jidh(w)
        assert len(rs) == int(r[3]) and len(segments(rs)) == int(r[4]), r
        h = hasm(None, rs)
        if r[5] == "TIE":
            assert h.seg is None
        else:
            assert h.seg is not None
            pre, al, stem, suf = h.seg
            k = "-".join(str(index(c)) for c in stem)
            key = ("+".join("-".join(str(index(c)) for c in p) for p in pre) + f"|{al}|{k}|"
                   + "-".join(str(index(c)) for c in suf))
            assert key == r[5], (key, r)
