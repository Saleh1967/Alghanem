"""مودَعُ معاني الحروف (ADR ١١٥): `corpora/huruf/maani.tsv`.

بندُ خطّة البنّاء (جوابُه 2026-10-19، نقله المالكُ في رسالته 02:06 ثمّ قال «اصلح كل المطلوب وقم
بايداع كل ما يلزم»):
«مودَعُ معاني الحروف: صفوفٌ من ج3 س468–507 بأعيانها. في كلّ صفٍّ: الحرف، ومعانيه بلفظها،
وسطرُه. ويُضاف شاهدُ «الكتاب» حيث يوجد، ويُفحص كلُّ اقتباسٍ في سطره آليًّا» — بترقيم الغانم:
سطورُ `shakhsiyya_j3.txt.gz` المختوم من 1، وسطورُ «الكتاب» JK006989 المختوم في `corpora/kitab/` من 1.

* كلُّ لفظٍ ومعنًى في سطره من ج3 بعينه، والسطرُ في 468–507؛ وكلُّ شاهدٍ من «الكتاب» في سطره بعينه.
* المفتاحُ من اللفظ بقاعدةٍ مكتوبةٍ هنا مستقلّة: أسماءُ الحروف بجدولٍ باليد، وغيرُها بطيّ الهمزة
  والألف المقصورة وحذف الشدّة.
* المودَعُ بلا صفٍّ مكرّر (لفظًا ومعنًى وسطرًا؛ و«حاشا» و«خلا» و«عدا» للاستثناء في س483 وس506
  صفّان)، وكلُّ سطرٍ من 468 إلى 507 فيه معنى حرفٍ له صفّ (ما عدا عناوين الأبواب والشاهدَ الشعريّ،
  بأسمائها).
* معيارُ العنوان والمعنى (تعيينُ البنّاء، `HARF_CLASS_FUNCTION_NOT_MEANING`): سطرٌ يعرّف وظيفةَ
  صنفٍ كلِّه (س468 «ما يفضي بمعاني الأفعال إلى الأسماء») لا يُعطى معنًى لكلّ حرف؛ وسطرٌ يسمّي الصنفَ
  بمعناه ولا يذكر لحرفه معنًى غيرَه (س499 «حروف التنبيه»، س506 «حروف الاستثناء»…)
  يُعطي حروفَه ذلك المعنى.
* حدُّ الفحص (`LAFZ_MAANA_PAIRING_BY_READING`): الاختبارُ يجد اللفظَ والمعنى في السطر، ولا يفحص أنّ
  المعنى لذلك اللفظ حيث تجتمع حروفٌ في سطرٍ واحد (س484، 492، 500، 506)؛ فالإسنادُ قراءةُ البنّاء،
  ومعانٍ بأعيانها مكتوبةٌ باليد أدناه. وصورُ المعنى الواحد لا تُفرد (`HARF_SUBFORMS_NOT_ROWS`):
  س495 «لنفي المستقبل، إما خبراً … أو نهياً … أو دعاء» معنًى واحد بصوره. والشاهدُ من «الكتاب» سطرٌ
  واحد (`KITAB_SHAHID_ONE_LINE`): ما انقطع على سطرين («وأما عن فلما» / «عدا الشيء»، «لكن …
  فتوجب» / «بها بعد نفي») يُقتبس منه سطرُ المعنى وحدَه.
* الطفرات: إزاحةُ سطرٍ، ومعنًى محرَّف، ومفتاحٌ محرَّف — كلٌّ يُسقط فحصه.
"""

from __future__ import annotations

import gzip
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DEPOSIT = ROOT / "corpora" / "huruf" / "maani.tsv"
J3 = ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz"
KITAB = ROOT / "corpora" / "kitab" / "0180Sibawayhi.KitabSibawayhi.JK006989-ara1.gz"

# أسماءُ الحروف كما سمّاها ج3 ← الحرف، باليد.
LETTER_NAMES = {
    "الباء": "ب", "اللام": "ل", "الكاف": "ك", "الواو": "و", "الفاء": "ف", "الهمزة": "ء",
    "الهـمـزة": "ء",
    "السين": "س", "واو القسم": "و", "تاء القسم": "ت", "لام التعريف": "ل", "لام جواب القسم": "ل",
    "الموطئة للقسم": "ل", "لام جواب لو": "ل", "لام الأمر": "ل", "لام الابتداء": "ل",
}
# سطورٌ في 468–507 لا صفَّ لها، بأسمائها: عناوينُ الأبواب التي تعدّ الحروف ولا تذكر معنى،
# والشاهدُ الشعريّ.
NO_ROW = {468: "TITLE_IDAFA", 477: "TITLE_HARF_ISM", 479: "SHIR", 485: "TITLE_ATF",
          493: "TITLE_NAFY", 501: "TITLE_JAWAB"}


def lines(path: Path) -> list[str]:
    return gzip.open(path, "rt", encoding="utf-8").read().split("\n")


def rows(text: str | None = None) -> list[list[str]]:
    t = DEPOSIT.read_text(encoding="utf-8") if text is None else text
    return [ln.split("\t") for ln in t.splitlines()[1:]]


def key_of(lafz: str) -> str:
    if lafz in LETTER_NAMES:
        return LETTER_NAMES[lafz]
    out = lafz.replace("ّ", "")
    for a, b in (("أ", "ء"), ("إ", "ء"), ("آ", "ء"), ("ى", "ا")):
        out = out.replace(a, b)
    return out


def quote_failures(rs: list[list[str]]) -> list[str]:
    j3, kit = lines(J3), lines(KITAB)
    bad = []
    for lafz, _h, maana, js, ks, kn in rs:
        s = int(js)
        if not 468 <= s <= 507:
            bad.append(f"OUT_OF_RANGE {lafz} {s}")
        line = j3[s - 1]
        if lafz not in line or maana not in line:
            bad.append(f"J3 {lafz} {maana} {s}")
        if ks != "0" and kn not in kit[int(ks) - 1]:
            bad.append(f"KITAB {lafz} {ks}")
        if (ks == "0") != (kn == ""):
            bad.append(f"KITAB_PAIR {lafz} {ks}")
    return bad


def key_failures(rs: list[list[str]]) -> list[str]:
    return [f"{r[0]} {r[1]}" for r in rs if key_of(r[0]) != r[1]]


def test_header() -> None:
    assert DEPOSIT.read_text(encoding="utf-8").splitlines()[0] == (
        "lafz\tharf\tmaana\tj3_satr\tkitab_satr\tkitab_nass")


def test_quotes_in_their_lines() -> None:
    assert quote_failures(rows()) == []


def test_keys_by_independent_rule() -> None:
    assert key_failures(rows()) == []


def test_no_duplicate_rows() -> None:
    rs = [tuple(r[:4]) for r in rows()]
    assert len(rs) == len(set(rs))


def test_every_meaning_line_has_a_row() -> None:
    have = {int(r[3]) for r in rows()}
    assert set(range(468, 508)) == have | set(NO_ROW)
    assert not have & set(NO_ROW)


def test_examples_by_hand() -> None:
    by: dict[str, list[str]] = {}
    for r in rows():
        by.setdefault(r[1], []).append(r[2])
    assert by["من"] == ["لابتداء الغاية", "للتبعيض", "لبيان الجنس", "زائدة"]
    assert by["رب"] == ["للتقليل"]
    assert "لمطـلق الجـمـع لا تفيد ترتيباً ولا معية" in by["و"]
    # س473 وس490 كاملتين، باليد (ضبطه المراجع).
    assert by["ب"] == ["للإلصاق", "للاستعانة", "المصاحبة", "بمعنى على", "بمعنى من أجل", "زائدة",
                       "بمعنى «في»", "تجـعـل الفعل اللازم متعدياً",
                       "تجعل الفعل المتعدي متجزئاً متبعضاً"]
    assert by["ءو"] == ["للشك", "للتخيير", "للإباحة", "تعليق الحكم بأحد المذكورين",
                        "مع الشك في وجود الأمرين"]
    assert by["ءم"] == ["تعليق الحكم بأحد المذكورين", "مع العلم بأحدهما والشك في تعيينه"]
    assert by["ما"] == ["لنفي الحـال، أو الماضي القريب من الحال", "مؤولة بمصدر"]


def test_kitab_witnesses_by_hand() -> None:
    """شواهدُ «الكتاب» من باب «عدة ما يكون عليه الكلم» (س18330–18539) بأسطرها، باليد."""
    got = {(r[0], r[4]) for r in rows() if r[4] != "0"}
    for want in [("الباء", "18341"), ("الكاف", "18337"), ("من", "18417"), ("لكنّ", "18509"),
                 ("سوف", "18510"), ("إنّ", "18516"), ("ليت", "18518"), ("بلى", "18525"),
                 ("نعم", "18526"), ("ألا", "18532"), ("كلا", "18533"), ("يا", "18414")]:
        assert want in got, want
    assert all(18330 <= int(k) <= 18539 for _l, k in got)


@pytest.mark.parametrize("name", ["MUTANT_SATR_SHIFT", "MUTANT_MAANA_EDIT", "MUTANT_KEY_EDIT"])
def test_mutants_killed(name: str) -> None:
    rs = rows()
    if name == "MUTANT_SATR_SHIFT":
        rs[0] = rs[0][:3] + [str(int(rs[0][3]) + 1)] + rs[0][4:]
        assert quote_failures(rs) != []
    elif name == "MUTANT_MAANA_EDIT":
        rs[0] = rs[0][:2] + [rs[0][2] + "ة"] + rs[0][3:]
        assert quote_failures(rs) != []
    else:
        rs[0] = [rs[0][0], rs[0][1] + "ا"] + rs[0][2:]
        assert key_failures(rs) != []
