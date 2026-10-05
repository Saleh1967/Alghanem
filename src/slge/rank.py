"""رتبةُ الجواب: يقينٌ، ظنّ، راجح، مرجوح، مردود، تعادل — محسوبةً من الطريق لا مُعلنةً باليد.

## النصوص

* **اليقين والظنّ** — الغزالي، «محكّ النظر» (OpenITI `0505Ghazali.MihakkNazar`، مراتب
  الإدراك): الحالةُ الأولى «أن تتيقن وتقطع به، وينضاف إليه قطع ثانٍ … ولا يجوز الغلط»؛
  والثالثة «أن يكون له سكون نفس إلى الشيء والتصديق به وهو يشعر بنقيضه … وهذا يسمى ظنا،
  وله درجات في الميل إلى الزيادة والنقصان لا تحصى. فمن سمع من عدل شيئا سكنت إليه نفسه، فإن
  انضاف إليه ثانٍ زاد السكون وقوي الظن». فقوّةُ الظنّ **عددُ الشواهد المستقلّة**.
* **رتبةُ النتيجة رتبةُ أضعف مقدّماتها** — الموضع نفسه: «كانت النتيجة الحاصلة يقينية ضرورية
  بحسب ذوق المقدمات». (وهو مبدأ «أضعف حلقة» في ASPIC+ عند Modgil وPrakken.)
* **ثبوتُ الخبر** — النبهاني، الشخصية ج٣ ¶275، ¶277: المشهورُ «لا يفيد اليقين، وإنما يفيد
  الظن»، وخبرُ الآحاد «يفيد الظن ولا يفيد اليقين»؛ ¶713: «جميع آيات القرآن ثبتت بالدليل
  القطعي».
* **الحكمُ على الصفة ظنّيّ** — النبهاني، «التفكير»: «فإن كانت هذه النتيجة هي الحكم على وجود
  الشيء فهي قطعية … أما إن كانت النتيجة هي الحكم على حقيقة الشيء أو صفته فإنها تكون نتيجة
  ظنية». وقاعدةُ اللزوم «كلّما كان أ كان ب» حكمٌ على صفة، فالمشاهدةُ والقياسُ يثبتانها ظنًّا.
* **التعارض** — «التفكير»: «إذا تعارض القطعي والظني يؤخذ القطعي ويرد الظني»؛ والشخصية ج٣
  ¶1060: «والتعادل لا يقع بين الدليلين القطعيين مطلقاً، وكذلك لا يقع بين الدليل القطعي والدليل
  الظني»؛ ¶1062: «والترجيح يختص بالأدلة الظنية».

## ما هو مبرهَن وما هو معلن

جدولُ الوزن (`weigh`) والجمعُ بأضعف حلقة (`path_grade`) مبرهَنان في `formal/Slge/Rank.lean`
(لا ترقية، والتناظر، والقطعيُّ لا يُردّ، ولا يُردّ إلّا ظنّيٌّ عارضه قطعيّ)، ويطابقهما
`tests/test_conformance.py`. أمّا **تصنيفُ الدليل** قطعيًّا أو ظنّيًّا (`evidence_grade`) فقاعدةٌ
معلنةٌ من النصوص أعلاه، وكلُّ تصنيفٍ يحمل سببه.

* **الخاصُّ قبل الثبوت** — ج٣ ¶1065: «فإن كان المقطوع به عاماً والمظنون خاصاً عمل بالمظنون …
  فحينئذ يرجح الخاص على العام، ويعمل به جمعاً بين الدليلين». والخصوصُ هنا محسوب: قاعدةُ
  الإثبات أخصُّ من قاعدة النفي إذا لزم مقدَّمَها مقدَّمُ الأخرى بالقواعد المقبولة ولم ينعكس.
  والعامُّ حينئذ **مخصوص** لا مردود (`Slge.Rank.general_is_makhsus`).

وما لم يُبنَ بعد: مرجّحاتُ الحكم (التحريمُ على الإباحة … ¶1066–1074) تحتاج نوعَ الحكم؛
وصورُ الجمع غيرُ التخصيص (¶1063: «ولو من وجه دون وجه»). فإذا تعارض ظنّيّان في نطاقٍ واحد
وُزنا بعدد الشواهد المستقلّة وحده.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .knowledge import (
    Admission,
    Evidence,
    Genus,
    Licence,
    Literal,
    Naql,
    Standing,
    Step,
    WorldRule,
    moves,
    productive,
)

__all__ = [
    "Grade",
    "Rank",
    "Ranked",
    "Side",
    "alone",
    "evidence_grade",
    "path_grade",
    "rank",
    "weigh",
    "weigh_scoped",
]


class Grade(Enum):
    """ثبوتُ مقدّمةٍ أو دلالةُ خطوة."""

    ظني = "zanni"
    قطعي = "qati"


class Rank(Enum):
    """رتبةُ الجواب."""

    يقين = "yaqin"
    ظن = "zann"
    راجح = "rajih"
    مرجوح = "marjuh"
    مردود = "mardud"
    تعادل = "taadul"
    تناقض = "tanaqud"
    مخصوص = "makhsus"
    لا_علم = "none"


def evidence_grade(ev: Evidence) -> tuple[Grade, str]:
    """ثبوتُ الدليل وسببُه."""

    if ev.genus is Genus.تعريف_مشترط:
        return Grade.قطعي, "تعريفٌ مشترط: قطعيٌّ داخل النموذج المعلن"
    if ev.genus is Genus.خبر_مقبول:
        if ev.naql is Naql.متواتر:
            return Grade.قطعي, "خبرٌ متواتر يفيد اليقين (ج٣ ¶713، ¶268)"
        if ev.naql is None:
            return Grade.ظني, "خبرٌ لم يُعلن طريقُ نقله: يُعامَل آحادًا"
        return Grade.ظني, f"خبرُ {ev.naql.name} يفيد الظنّ (ج٣ ¶275، ¶277)"
    if ev.genus is Genus.شاهد_معجمي:
        if ev.naql is Naql.متواتر:
            return Grade.قطعي, "وضعٌ لغويٌّ منقولٌ تواترًا"
        return Grade.ظني, "اللغةُ طريقُها الرواية، والشاهدُ الواحدُ آحاد"
    if ev.genus in (Genus.مشاهدة, Genus.قياس_كمي):
        return Grade.ظني, "حكمٌ على صفة الشيء لا على وجوده: ظنّيّ («التفكير»)"
    return Grade.ظني, "فرضيّة"


def _meet(a: Grade, b: Grade) -> Grade:
    return Grade.قطعي if a is b is Grade.قطعي else Grade.ظني


def path_grade(
    path: tuple[Step, ...], rules: dict[str, WorldRule], licences: dict[str, Licence]
) -> tuple[Grade, tuple[str, ...]]:
    """رتبةُ الطريق: أدنى ثبوتِ دليلٍ فيه وأدنى دلالةِ خطوة (`Slge.Rank.pathGrade`)."""

    grade, reasons = Grade.قطعي, []
    for step in path:
        rule = rules[step.rule_id]
        assert rule.evidence is not None
        g, why = evidence_grade(rule.evidence)
        grade = _meet(grade, g)
        reasons.append(f"{rule.rule_id}: {why}")
        if rule.standing is Standing.عادي:
            grade = Grade.ظني
            reasons.append(f"{rule.rule_id}: عادةٌ لا ضرورة (التهافت)")
        if step.licence is not None:
            grade = Grade.ظني
            reasons.append(f"{rule.rule_id}: رُفعت إلى المساواة بـ{step.licence.name}، والرفعُ ظنّ")
            g2, why2 = evidence_grade(licences[step.rule_id].evidence)
            grade = _meet(grade, g2)
            reasons.append(f"رافع {rule.rule_id}: {why2}")
    return grade, tuple(reasons)


@dataclass(frozen=True, slots=True)
class Side:
    """جانبٌ من التعارض: رتبتُه، وعددُ شواهده المستقلّة."""

    grade: Grade
    strength: int


def alone(g: Grade) -> Rank:
    """بلا معارض."""

    return Rank.يقين if g is Grade.قطعي else Rank.ظن


def weigh(a: Side, b: Side) -> Rank:
    """حكمُ الجانب الأوّل إذا عارضه الثاني (`Slge.Rank.weigh` حرفًا)."""

    if a.grade is Grade.قطعي:
        return Rank.تناقض if b.grade is Grade.قطعي else Rank.يقين
    if b.grade is Grade.قطعي:
        return Rank.مردود
    if a.strength > b.strength:
        return Rank.راجح
    if a.strength < b.strength:
        return Rank.مرجوح
    return Rank.تعادل


def weigh_scoped(a: Side, b: Side, a_specific: bool, b_specific: bool) -> Rank:
    """الوزنُ مع الخصوص (`Slge.Rank.weighS` حرفًا)."""

    if a_specific and not b_specific:
        return alone(a.grade)
    if b_specific and not a_specific:
        return Rank.مخصوص
    return weigh(a, b)


@dataclass(frozen=True, slots=True)
class Ranked:
    """الجوابُ برتبته: النتيجة، والرتبة، والطرقُ المؤيّدة والمعارضة، والأسباب."""

    conclusion: Literal | None
    rank: Rank
    support: tuple[tuple[Step, ...], ...]
    opposition: tuple[tuple[Step, ...], ...]
    side: Side | None
    opposing: Side | None
    reasons: tuple[str, ...]
    blocked_by: tuple[str, ...]
    specialised: bool = False


def _paths(
    givens: tuple[Literal, ...],
    target: str,
    rules: tuple[WorldRule, ...],
    licences: dict[str, Licence],
    blocked: set[str],
    max_depth: int,
) -> list[tuple[Literal, tuple[Step, ...]]]:
    """كلُّ طريقٍ بسيطٍ منتجٍ بالمقبول وحده إلى الهدف، بطول ‎≤ max_depth‎."""

    out: list[tuple[Literal, tuple[Step, ...]]] = []

    def walk(at: Literal, path: tuple[Step, ...], seen: frozenset[Literal]) -> None:
        if at.concept == target and path:
            out.append((at, path))
            return
        if len(path) >= max_depth:
            return
        for rule in rules:
            if rule.admission is not Admission.مقبول or rule.rule_id in blocked:
                continue
            lic = licences.get(rule.rule_id)
            for nxt, form, ok in moves(rule, at, lic is not None):
                if not ok or nxt in seen:
                    continue
                used = lic.ground if lic is not None and not productive(rule.degree, form) else None
                walk(nxt, (*path, Step(rule.rule_id, form, used)), seen | {nxt})

    for given in givens:
        walk(given, (), frozenset(givens))
    return out


def _evidence_ids(path: tuple[Step, ...], rules: dict[str, WorldRule],
                  licences: dict[str, Licence]) -> frozenset[str]:
    ids: set[str] = set()
    for s in path:
        ev = rules[s.rule_id].evidence
        assert ev is not None
        ids.add(ev.evidence_id)
        if s.licence is not None:
            ids.add(licences[s.rule_id].evidence.evidence_id)
    return frozenset(ids)


def _side(
    paths: list[tuple[Step, ...]], rules: dict[str, WorldRule], licences: dict[str, Licence]
) -> tuple[Side, tuple[tuple[Step, ...], ...], tuple[str, ...]]:
    """أقوى رتبةٍ في الجانب، وعددُ طرقها المستقلّة (لا يشترك اثنان منها في دليل)."""

    graded = [(path_grade(p, rules, licences), p) for p in paths]
    best = Grade.قطعي if any(g is Grade.قطعي for (g, _), _ in graded) else Grade.ظني
    chosen: list[tuple[Step, ...]] = []
    used: set[str] = set()
    reasons: list[str] = []
    for (g, why), p in sorted(graded, key=lambda x: len(x[1])):
        if g is not best:
            continue
        ids = _evidence_ids(p, rules, licences)
        if ids & used:
            continue
        chosen.append(p)
        used |= ids
        reasons.extend(why)
    return Side(best, len(chosen)), tuple(chosen), tuple(dict.fromkeys(reasons))


def _antecedent(path: tuple[Step, ...], rules: dict[str, WorldRule]) -> str:
    """مقدَّمُ القاعدة الأخيرة في الطريق: ما عُلّق عليه الحكمُ في الهدف."""

    return rules[path[-1].rule_id].antecedent


def _entails(a: str, b: str, rules: tuple[WorldRule, ...], blocked: set[str]) -> bool:
    """أيلزم «ب» من «أ» بالقواعد المقبولة المثبِتة وحدها؟"""

    if a == b:
        return True
    usable = tuple(r for r in rules if r.admission is Admission.مقبول and r.positive
                   and r.rule_id not in blocked)
    return any(c.affirmed for c, _ in _paths((Literal(a, True),), b, usable, {}, set(), 8))


def rank(
    given: Literal | tuple[Literal, ...],
    target: str,
    rules: tuple[WorldRule, ...],
    licences: tuple[Licence, ...] = (),
    present_blockers: frozenset[str] = frozenset(),
    max_depth: int = 8,
) -> Ranked:
    """رتّب الجوابَ في الهدف: اجمع الطرقَ المنتجةَ للإثبات وللنفي من المعطيات كلّها، ثمّ زِن."""

    givens = given if isinstance(given, tuple) else (given,)
    by_id = {r.rule_id: r for r in rules}
    lic = {x.rule_id: x for x in licences if not x.is_candidate}
    blocked = {r.rule_id for r in rules if set(r.blocker_ids) & present_blockers}
    blockers = tuple(sorted({b for r in rules for b in r.blocker_ids if b in present_blockers}))
    found = _paths(givens, target, rules, lic, blocked, max_depth)
    pro = [p for c, p in found if c.affirmed]
    con = [p for c, p in found if not c.affirmed]
    if not pro and not con:
        return Ranked(None, Rank.لا_علم, (), (), None, None, (), blockers)
    if not con or not pro:
        affirmed = bool(pro)
        side, chosen, why = _side(pro or con, by_id, lic)
        return Ranked(Literal(target, affirmed), alone(side.grade), chosen, (), side, None,
                      why, blockers)
    sp, cp, wp = _side(pro, by_id, lic)
    sc, cc, wc = _side(con, by_id, lic)
    ap, ac = _antecedent(cp[0], by_id), _antecedent(cc[0], by_id)
    p_in_c, c_in_p = _entails(ap, ac, rules, blocked), _entails(ac, ap, rules, blocked)
    p_spec, c_spec = p_in_c and not c_in_p, c_in_p and not p_in_c
    verdict = weigh_scoped(sp, sc, p_spec, c_spec)
    specialised = p_spec or c_spec
    if verdict in (Rank.مرجوح, Rank.مردود, Rank.مخصوص):  # الجوابُ هو الغالب، والمغلوبُ يُذكر
        return Ranked(Literal(target, False), weigh_scoped(sc, sp, c_spec, p_spec), cc, cp,
                      sc, sp, wc + wp, blockers, specialised)
    conclusion = None if verdict in (Rank.تعادل, Rank.تناقض) else Literal(target, True)
    return Ranked(conclusion, verdict, cp, cc, sp, sc, wp + wc, blockers, specialised)
