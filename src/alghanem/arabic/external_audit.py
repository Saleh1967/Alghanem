"""External Arabic-card auditor that uses current Alghanem G0 contracts.

This module intentionally does not issue kernel verdict authority.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final
from unicodedata import category, normalize

from alghanem.kernel.birth import (
    BirthExperimentSpecification,
    BirthQuery,
    EvidenceMode,
    ProjectionPoset,
    StructureHypothesis,
)


class ExternalAuditError(ValueError):
    """Raised when the external audit card is malformed."""


_TATWEEL: Final = "\u0640"
_LETTER_FOLDING: Final = {
    "\u0622": "\u0627",
    "\u0623": "\u0627",
    "\u0625": "\u0627",
    "\u0671": "\u0627",
    "\u0649": "\u064a",
    "\u0629": "\u0647",
}
_UNDETERMINED_RELATION: Final = "غير_متعينة"
_WEAKER_RELATION: Final = "أضعف_صوريًّا"
_EQUIVALENT_RELATION: Final = "مكافئ_صوريًّا"
_INCOMPARABLE_RELATION: Final = "غير_قابل_للمقارنة"
_ALLOWED_RELATIONS: Final = (
    _UNDETERMINED_RELATION,
    _WEAKER_RELATION,
    _EQUIVALENT_RELATION,
    _INCOMPARABLE_RELATION,
)
_CLOSED_STATUS: Final = "مغلق"


def comparison_key(value: str) -> str:
    """Return the orthography-insensitive key used to compare card text.

    The key applies the repository's `NFC` normalization form, drops every
    combining mark, invisible formatting character, and `TATWEEL`, and folds
    equivalent `ALEF`, `ALEF MAQSURA`, and `TEH MARBUTA` surface forms. It
    exists only so that comparisons do not silently depend on optional
    diacritics or invisible characters; it asserts no linguistic identity and
    never replaces the card's own text in any reported field.
    """
    unmarked = "".join(
        character
        for character in normalize("NFC", value)
        if category(character) not in {"Mn", "Cf"} and character != _TATWEEL
    )
    return "".join(_LETTER_FOLDING.get(character, character) for character in unmarked)


_RELATION_BY_KEY: Final = {
    comparison_key(relation): relation for relation in _ALLOWED_RELATIONS
}
if len(_RELATION_BY_KEY) != len(_ALLOWED_RELATIONS):  # pragma: no cover - guard
    raise RuntimeError("two allowed relations collapse onto one comparison key")


def canonical_relation(value: str) -> str:
    """Return the closed-vocabulary relation named by ``value``.

    Only `غير_متعينة` and the explicitly resolved relations
    `أضعف_صوريًّا`, `مكافئ_صوريًّا`, and `غير_قابل_للمقارنة` are accepted. Any
    other text — a misspelling or an invented term — is rejected instead of
    being silently counted as a resolved relation.
    """
    relation = _RELATION_BY_KEY.get(comparison_key(value))
    if relation is None:
        allowed = "، ".join(_ALLOWED_RELATIONS)
        raise ExternalAuditError(
            "القراءات_المنافسة[].علاقة_بالنموذج_المختبر must be one of: " + allowed
        )
    return relation


@dataclass(frozen=True, slots=True)
class ExternalAuditResult:
    """External audit outcome; this is not a kernel birth verdict."""

    الجهة: str
    نتيجة_التدقيق_الخارجي: str
    سبب: str
    النموذج_المختبر: str
    مخروط_الأضعف_المشتق: tuple[str, ...]
    الإسقاطات_المنافسة_المشتقة: tuple[str, ...]
    عدد_القراءات_المنافسة: int
    عدد_العلاقات_غير_المتعينة: int
    عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة: int
    تفاصيل_القراءات_المنافسة: tuple[tuple[str, str], ...]
    حالة_إغلاق_Down_E: str
    سبب_حالة_إغلاق_Down_E: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "الجهة": self.الجهة,
            "نتيجة_التدقيق_الخارجي": self.نتيجة_التدقيق_الخارجي,
            "سبب": self.سبب,
            "النموذج_المختبر": self.النموذج_المختبر,
            "مخروط_الأضعف_المشتق": list(self.مخروط_الأضعف_المشتق),
            "الإسقاطات_المنافسة_المشتقة": list(self.الإسقاطات_المنافسة_المشتقة),
            "عدد_القراءات_المنافسة": self.عدد_القراءات_المنافسة,
            "عدد_العلاقات_غير_المتعينة": self.عدد_العلاقات_غير_المتعينة,
            "عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة": (
                self.عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة
            ),
            "تفاصيل_القراءات_المنافسة": [
                {"قراءة": name, "علاقة_بالنموذج_المختبر": relation}
                for name, relation in self.تفاصيل_القراءات_المنافسة
            ],
            "حالة_إغلاق_Down_E": self.حالة_إغلاق_Down_E,
            "سبب_حالة_إغلاق_Down_E": self.سبب_حالة_إغلاق_Down_E,
        }


def _assess_down_e_closure(
    card: dict[str, Any], *, weaker_cone: tuple[str, ...], blocking_relations: int
) -> tuple[str, str]:
    if blocking_relations:
        return (
            "غير_متعينة",
            "علاقة المنافسة مع قراءة منافسة ما زالت حاجبة قبل فحص إغلاق Down_E",
        )
    if not weaker_cone:
        return ("مغلق", "مخروط السوابق الأضعف فارغ في التصور الحالي")
    raw_entries = card.get("اغلاق_سوابق_Down_E")
    if not isinstance(raw_entries, list):
        return (
            "غير_متعينة",
            "لا يوجد توثيق لإغلاق سوابق Down_E المطلوبة",
        )
    closure_by_model: dict[str, tuple[str, str]] = {}
    for entry in raw_entries:
        if not isinstance(entry, dict):
            raise ExternalAuditError("اغلاق_سوابق_Down_E entries must be mappings")
        model = _require_text(entry.get("نموذج"), "اغلاق_سوابق_Down_E[].نموذج")
        status = _require_text(entry.get("حالة"), "اغلاق_سوابق_Down_E[].حالة")
        closure_by_model[comparison_key(model)] = (model, status)
    cone_keys = {comparison_key(model) for model in weaker_cone}
    if (
        set(closure_by_model) != cone_keys
        or len(cone_keys) != len(weaker_cone)
        or len(closure_by_model) != len(raw_entries)
    ):
        return (
            "غير_متعينة",
            "توثيق إغلاق Down_E لا يطابق مخروط السوابق الأضعف المشتق بدقة",
        )
    closed_key = comparison_key(_CLOSED_STATUS)
    non_closed = sorted(
        model
        for model, status in closure_by_model.values()
        if comparison_key(status) != closed_key
    )
    if non_closed:
        return (
            "غير_مغلق",
            f"سوابق Down_E غير مغلقة: {', '.join(non_closed)}",
        )
    return ("مغلق", "كل سوابق Down_E المشتقة موثقة كمغلقة")


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExternalAuditError(f"{field_name} must be non-blank text")
    return value


def _read_json_yaml(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ExternalAuditError("audit card must be YAML-compatible JSON") from exc
    if not isinstance(payload, dict):
        raise ExternalAuditError("audit card root must be a mapping")
    return payload


def _parse_mode(value: Any) -> EvidenceMode:
    mode_text = _require_text(value, "تعريف_التجربة.evidence_mode")
    by_name = {
        "FORMAL": EvidenceMode.FORMAL,
        "EMPIRICAL": EvidenceMode.EMPIRICAL,
        "MIXED": EvidenceMode.MIXED,
    }
    if mode_text not in by_name:
        raise ExternalAuditError(
            "تعريف_التجربة.evidence_mode must be FORMAL/EMPIRICAL/MIXED"
        )
    return by_name[mode_text]


def build_birth_spec_from_card(card: dict[str, Any]) -> BirthExperimentSpecification:
    if "نماذج_أضعف_معلنة" in card:
        raise ExternalAuditError("WeakerCone must be derived, not caller-declared")
    trial = card.get("تعريف_التجربة")
    if not isinstance(trial, dict):
        raise ExternalAuditError("تعريف_التجربة must be a mapping")

    hypothesis = StructureHypothesis(
        hypothesis_id=_require_text(card.get("معرف_الفرضية"), "معرف_الفرضية"),
        statement=_require_text(card.get("الفرضية"), "الفرضية"),
    )
    test_model = _require_text(card.get("النموذج_المختبر"), "النموذج_المختبر")
    query = BirthQuery(
        query_id=_require_text(card.get("معرف_السؤال"), "معرف_السؤال"),
        hypothesis=hypothesis,
        test_model=test_model,
    )

    projections = trial.get("projections")
    relations = trial.get("strict_relations")
    if not isinstance(projections, list) or not all(
        isinstance(item, str) and item.strip() for item in projections
    ):
        raise ExternalAuditError(
            "تعريف_التجربة.projections must be a list of non-blank text"
        )
    if not isinstance(relations, list) or not all(
        isinstance(item, list)
        and len(item) == 2
        and isinstance(item[0], str)
        and item[0].strip()
        and isinstance(item[1], str)
        and item[1].strip()
        for item in relations
    ):
        raise ExternalAuditError(
            "تعريف_التجربة.strict_relations must be a list of [lower, richer] pairs"
        )

    return BirthExperimentSpecification(
        experiment_id=_require_text(
            trial.get("experiment_id"), "تعريف_التجربة.experiment_id"
        ),
        revision_id=_require_text(
            trial.get("revision_id"), "تعريف_التجربة.revision_id"
        ),
        revision_sequence=1,
        evidence_mode=_parse_mode(trial.get("evidence_mode")),
        domain=_require_text(trial.get("domain"), "تعريف_التجربة.domain"),
        projection_poset=ProjectionPoset(
            tuple(projections), tuple((item[0], item[1]) for item in relations)
        ),
        birth_query=query,
        residual_definition_id=_require_text(
            trial.get("residual_definition_id"), "تعريف_التجربة.residual_definition_id"
        ),
        residual_definition=_require_text(
            trial.get("residual_definition"), "تعريف_التجربة.residual_definition"
        ),
        closure_criterion_id=_require_text(
            trial.get("closure_criterion_id"), "تعريف_التجربة.closure_criterion_id"
        ),
        closure_criterion=_require_text(
            trial.get("closure_criterion"), "تعريف_التجربة.closure_criterion"
        ),
        evidence_requirements=_require_text(
            trial.get("evidence_requirements"), "تعريف_التجربة.evidence_requirements"
        ),
    )


def audit_card(path: str | Path) -> ExternalAuditResult:
    card_path = Path(path)
    card = _read_json_yaml(card_path)
    specification = build_birth_spec_from_card(card)

    alternatives = card.get("القراءات_المنافسة")
    if not isinstance(alternatives, list):
        raise ExternalAuditError("القراءات_المنافسة must be a list")
    parsed_alternatives: list[tuple[str, str]] = []
    unresolved: list[tuple[str, str]] = []
    blocking_incomparable: list[tuple[str, str]] = []
    for item in alternatives:
        if not isinstance(item, dict):
            raise ExternalAuditError("كل قراءة منافسة يجب أن تكون كائنًا")
        reading = _require_text(item.get("قراءة"), "القراءات_المنافسة[].قراءة")
        declared_relation = _require_text(
            item.get("علاقة_بالنموذج_المختبر"),
            "القراءات_المنافسة[].علاقة_بالنموذج_المختبر",
        )
        relation = canonical_relation(declared_relation)
        complete_rival = item.get("تفسير_منافس_كامل")
        if complete_rival is not None and not isinstance(complete_rival, bool):
            raise ExternalAuditError(
                "القراءات_المنافسة[].تفسير_منافس_كامل must be true or false"
            )
        if relation != _INCOMPARABLE_RELATION and complete_rival is not None:
            raise ExternalAuditError(
                "القراءات_المنافسة[].تفسير_منافس_كامل is meaningful only for "
                + _INCOMPARABLE_RELATION
            )
        parsed_alternatives.append((reading, declared_relation))
        if relation == _UNDETERMINED_RELATION:
            unresolved.append((reading, declared_relation))
        elif relation == _INCOMPARABLE_RELATION and complete_rival is not False:
            blocking_incomparable.append((reading, declared_relation))
    blocking = len(unresolved) + len(blocking_incomparable)
    down_e_status, down_e_reason = _assess_down_e_closure(
        card,
        weaker_cone=specification.frozen_weaker_models,
        blocking_relations=blocking,
    )

    if blocking or down_e_status != "مغلق":
        return ExternalAuditResult(
            الجهة="مدقق_خارجي",
            نتيجة_التدقيق_الخارجي="DEFER_التدقيق",
            سبب=("تعذر الحسم الخارجي: علاقة المنافسة/الأضعف أو إغلاق Down_E غير مكتمل"),
            النموذج_المختبر=specification.birth_query.test_model,
            مخروط_الأضعف_المشتق=specification.frozen_weaker_models,
            الإسقاطات_المنافسة_المشتقة=specification.competing_projections,
            عدد_القراءات_المنافسة=len(parsed_alternatives),
            عدد_العلاقات_غير_المتعينة=len(unresolved),
            عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة=len(blocking_incomparable),
            تفاصيل_القراءات_المنافسة=tuple(parsed_alternatives),
            حالة_إغلاق_Down_E=down_e_status,
            سبب_حالة_إغلاق_Down_E=down_e_reason,
        )

    return ExternalAuditResult(
        الجهة="مدقق_خارجي",
        نتيجة_التدقيق_الخارجي="PASS_التدقيق",
        سبب="لا توجد علاقة منافسة حاجبة في البطاقة الخارجية",
        النموذج_المختبر=specification.birth_query.test_model,
        مخروط_الأضعف_المشتق=specification.frozen_weaker_models,
        الإسقاطات_المنافسة_المشتقة=specification.competing_projections,
        عدد_القراءات_المنافسة=len(parsed_alternatives),
        عدد_العلاقات_غير_المتعينة=0,
        عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة=0,
        تفاصيل_القراءات_المنافسة=tuple(parsed_alternatives),
        حالة_إغلاق_Down_E=down_e_status,
        سبب_حالة_إغلاق_Down_E=down_e_reason,
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run external Arabic audit card")
    parser.add_argument("card", help="Path to YAML-compatible JSON audit card")
    args = parser.parse_args()

    result = audit_card(args.card)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
