"""البوّابة: كلُّ جاهزٍ يعود بايتًا ببايت، ويقبله النموذجُ المبرهَن، وذرّاتُه مشتقّةٌ من رسمه."""

from __future__ import annotations

import pytest

from gate import Refusal, enter, exit, gate, recover
from gate.licence import binary_ok, continue_licensed, kind_of, pause_licensed
from gate.rasm_consistency import consistent


def test_licence_matches_lean_witnesses() -> None:
    """الشواهدُ المسمّاةُ في `Ternary.lean`: hajja، bahr، tamm."""

    hajja, bahr, tamm = ["cv", "v", "c", "cv"], ["cv", "c", "c"], ["cv", "v", "c", "c"]
    assert continue_licensed(hajja) and not binary_ok(hajja)
    assert pause_licensed(bahr) and not continue_licensed(bahr)
    assert pause_licensed(tamm) and not continue_licensed(tamm)
    assert kind_of(("حَ", "اْ", "جْ", "جَ")) == hajja
    assert kind_of(("مَ", "اْ")) == ["cv", "v"] and kind_of(("مِ", "نْ")) == ["cv", "c"]


def test_corpus_is_the_sealed_one() -> None:
    """18,200 رسمًا في المدوّنة المختومة تصير 17,572 صورةً قانونيّة (رسومٌ تتّحد صورتُها وتختلف بقيّتُها)."""

    assert gate().book.payload["bridge_protocol"] == "A116-CANONICAL-TXT-1.1"
    assert len(gate().book.domain) == 17572


def test_every_ready_word_round_trips_and_is_admissible() -> None:
    g = gate()
    ready = madd = 0
    for surface in g.book.domain:
        cert = g.enter(surface.encode("utf-8"))
        if isinstance(cert, Refusal):
            assert cert.status in ("DEFER", "REJECT") and cert.reasons
            continue
        ready += 1
        assert g.exit(cert) == surface.encode("utf-8")
        k = kind_of(cert.atoms)
        assert continue_licensed(k), surface
        if not binary_ok(k):
            madd += 1
        assert consistent(surface, cert.atoms), surface
        assert g.book.decode_integer(cert.integer) == surface
    assert ready == 17551
    assert madd == 65  # ما يراه الثلاثيُّ ويعمى عنه الثنائيّ: مدٌّ ثمّ مشدَّد (حَاجَّ)


def test_refusals_are_named_and_never_guessed() -> None:
    assert enter("حاسوب".encode()).reasons == ("UNVOCALIZED_WORD_IS_NEVER_GUESSED",)
    assert enter("حم".encode()).reasons == ("UNVOCALIZED_WORD_IS_NEVER_GUESSED",)
    assert not isinstance(enter("يَعْلَمُونَ".encode()), Refusal)  # المدُّ بلا سكون: قاعدةُ طبعةٍ مسمّاة
    # رمزٌ ليس حرفًا (واوٌ صغيرة، ترقيم): ليس كلمةً واحدة — DEFER باسمه، لا حالةَ رابعة ولا None
    for w in ("حَوْلَهُۥ", "عَلَيْهِۦ", "كَتَبَ،", "«كَتَبَ»"):
        r = enter(w.encode())
        assert isinstance(r, Refusal) and r.status == "DEFER", w
        assert r.reasons == ("NOT_ONE_EXACT_WORD_SPAN",), w
    # المدخلُ بايتاتٌ: ما ليس UTF-8 وما ليس كلمةً واحدة يُرفض باسمه ولا يُرمى استثناء
    assert enter(b"\xff\xfe") == Refusal("REJECT", ("NOT_UTF8",))
    assert enter(b"") == Refusal("REJECT", ("NOT_ONE_TOKEN",))
    assert enter("كَتَبَ ضَرَبَ".encode()) == Refusal("REJECT", ("NOT_ONE_TOKEN",))


def test_enter_has_three_statuses_only() -> None:
    """القانون: الرفضُ DEFER أو REJECT أو OUTSIDE_DECLARED_DOMAIN لا غير — على رسوم المدوّنة المختومة
    وعلى رسومٍ عثمانيّةٍ ومرقّمة؛ وكلُّ تأجيلٍ أو ردٍّ له سببٌ مسمًّى (والخارجُ عن المجال اسمُه حالتُه)."""

    g = gate()
    sample = [*g.book.domain[:2000], "حَوْلَهُۥ", "رَبِّهِۦ", "بِهِۦٓ", "ٱلنَّبِيِّۦنَ", "ٱللَّهِ", "هُدًۭى", "مَٰلِكِ",
              "كَتَبَ،", "الٓمٓ"]
    for s in sample:
        r = g.enter(s.encode())
        if isinstance(r, Refusal):
            assert r.status in ("DEFER", "REJECT", "OUTSIDE_DECLARED_DOMAIN"), (s, r)
            if r.status != "OUTSIDE_DECLARED_DOMAIN":
                assert r.reasons and all(x and x != "None" for x in r.reasons), (s, r)
    with pytest.raises(ValueError):
        exit(enter("كَتَبَ".encode())._replace(ordinal=5) if False else _tampered())


def _tampered():
    from dataclasses import replace

    cert = enter("كَتَبَ".encode())
    assert not isinstance(cert, Refusal)
    return replace(cert, core=replace(cert.core, ordinal=5))


def test_generation_and_recovery_agree() -> None:
    cert = enter("كَتَبَ".encode())
    assert not isinstance(cert, Refusal)
    outcome, found = recover(cert)
    assert outcome == "RECOVERED" and ("كتب", "PAST", "I-a", "3MS") in found


@pytest.mark.slow
def test_recovery_on_masaq_verbs_is_at_least_97_percent() -> None:
    from gate.mabni_bridge import verb_readings

    r = verb_readings()
    total = sum(r["outcomes"].values()) if "outcomes" in r else None
    assert total, r.keys()
    assert r["outcomes"]["RECOVERED"] / total >= 0.97


def test_pronoun_atoms_match_slge_categories_lean() -> None:
    """الضمائرُ المنفصلة الاثنا عشر: ذرّاتُ البوّابة هي خاناتُ `Slge.Categories.pronouns` (مواضعُ SLGE:
    الهمزةُ 0 ثمّ الأبجديّة؛ الحالاتُ فتح 0 كسر 1 ضم 2 سكون 3)."""

    alphabet = "ءابتثجحخدذرزسشصضطظعغفقكلمنهوي"
    marks = {"َ": 0, "ِ": 1, "ُ": 2, "ْ": 3}
    expected = {
        "أَنَا": [(0, 0), (25, 0), (1, 3)], "نَحْنُ": [(25, 0), (6, 3), (25, 2)],
        "أَنْتَ": [(0, 0), (25, 3), (3, 0)], "أَنْتِ": [(0, 0), (25, 3), (3, 1)],
        "أَنْتُمَا": [(0, 0), (25, 3), (3, 2), (24, 0), (1, 3)],
        "أَنْتُمْ": [(0, 0), (25, 3), (3, 2), (24, 3)],
        "أَنْتُنَّ": [(0, 0), (25, 3), (3, 2), (25, 3), (25, 0)],
        "هُوَ": [(26, 2), (27, 0)], "هِيَ": [(26, 1), (28, 0)],
        "هُمَا": [(26, 2), (24, 0), (1, 3)], "هُمْ": [(26, 2), (24, 3)],
        "هُنَّ": [(26, 2), (25, 3), (25, 0)],
    }
    from gate.contextual import Context, project

    for surface, cells in expected.items():
        cert = enter(surface.encode("utf-8"))
        if isinstance(cert, Refusal):  # خارج المجال المختوم: رفضٌ بالاسم، والجسرُ وحدَه يُذرّر
            assert cert.status == "OUTSIDE_DECLARED_DOMAIN", surface
            decision = project(surface, Context())
            assert decision["status"] == "READY", surface
            atoms = decision["atoms"]
        else:
            atoms = cert.atoms
        assert [(alphabet.index(a[0]), marks[a[1]]) for a in atoms] == cells, surface


# — المادّة ١١ من دستور الوكيل: الشهادةُ لا تأخذ العالمَ معاملًا —

LAFZ_CONTEXT = frozenset({"entry", "exit", "left", "profile"})
"""ما يجوز أن يدخل البوّابةَ مع البايتات: حدُّ الوصل والوقف، والجارُ الأيسر، وطبعةٌ مسمّاة — كلُّه من اللفظ،
لا شيءَ منه من الواقع الخارجيّ («زيدٌ قائم» لا يبطل إذا قعد زيد)."""


def _world_free(params: tuple[str, ...], context_fields: frozenset[str]) -> list[str]:
    bad = [p for p in params if p not in ("data", "context")]
    bad += [f"context.{f}" for f in sorted(context_fields - LAFZ_CONTEXT)]
    return [f"WORLD_IN_CERTIFICATE:{x}" for x in bad]


def test_certificate_takes_no_world() -> None:
    import dataclasses
    import inspect

    from gate.contextual import Context

    params = tuple(inspect.signature(enter).parameters)
    fields = frozenset(f.name for f in dataclasses.fields(Context))
    assert params == ("data", "context") and _world_free(params, fields) == []
    assert _world_free(("data", "world"), fields) == ["WORLD_IN_CERTIFICATE:world"]
    assert _world_free(params, fields | {"time"}) == ["WORLD_IN_CERTIFICATE:context.time"]
