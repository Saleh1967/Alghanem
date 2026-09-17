"""G0.EX.1e: binding one experimental run to one frozen experiment, before it runs.

This module closes exactly one question: which frozen experiment is a run a run
*of*? Before it, the answer was read from the domain alone, which is not an
answer at all:

`SameDomainIsNotSameExperiment`. Two experiments may be frozen in one domain,
and a record produced under the first could be carried to a gate holding the
second's binding: the domain matched, so the offer passed, and the offer's own
trace then named an experiment the run had never been bound to. That is a
cross-experiment provenance leak and not a naming inconvenience.

`SameExperimentNameIsNotSameFrozenContent`. Neither is an experiment id an
answer. A revision of one experiment shares its id and freezes different
content -- a different query, a different residual definition, different
evidence requirements -- so identity here is the frozen manifest's own content
id and never the name written on it.

The binding happens *before* the run, not after it:

    ExperimentalRunBindingAuthority.bind(binding, request)
        -> BoundExperimentalRunRequest
        -> ExperimentalAuthority.run(bound_request=..., ...)
        -> ExperimentalRunRecord carrying the bound request's content digest

`NoRunWithoutPriorFrozenExperimentBinding`: `ExperimentalAuthority.run` accepts
no bare request, so a run that was never bound cannot be produced, cannot be
replayed, and therefore cannot be offered. The laboratory still tries what the
constitution has not admitted -- nothing here asks whether the candidate is
born, true, or necessary -- but it does so against a question frozen before the
answer was seen.

`BindingIsNotEvidenceAndNotBirth`. This authority issues a bound request and
nothing else. It imports no acquisition type, issues no snapshot, no verdict,
and no certificate, and the bound request confers nothing: it makes a run
*attributable*, never admissible.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field

from .experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    BirthExperimentSpecificationContentIdentity,
)
from .experimental import (
    BoundExperimentalRunRequest as _BoundExperimentalRunRequestSeam,
)
from .experimental import (
    ExperimentalAuthorityError,
    ExperimentalRunRequest,
    _require_text,
    sweep_forbidden_fields,
)
from .experimental_request_content_identity import (
    CanonicalExperimentalRunRequestEncoder,
    ExperimentalRunRequestContentIdentity,
)
from .trace import Trace

_BINDING_TOKEN = object()

EXPERIMENTAL_BINDING_NAMED_LAWS: dict[str, str] = {
    "SameDomainIsNotSameExperiment": (
        "SameDomainIsNotSameExperiment: a run is bound to one frozen "
        "experiment's own content id, never to the domain it happens to share "
        "with every other experiment frozen in that domain. Equal domains are "
        "a necessary condition of binding and never a sufficient one"
    ),
    "SameExperimentNameIsNotSameFrozenContent": (
        "SameExperimentNameIsNotSameFrozenContent: an experiment id names a "
        "line of revisions, and two revisions freeze two different questions. "
        "Identity here is the frozen manifest's content id, so a binding to "
        "one revision never authorises an offer against another"
    ),
    "NoRunWithoutPriorFrozenExperimentBinding": (
        "NoRunWithoutPriorFrozenExperimentBinding: the binding is derived "
        "before the run, from a request frozen before the run, so no result "
        "can choose the experiment it will later be attributed to. An unbound "
        "request is not an admissible argument to the run authority at all"
    ),
    "BindingIsNotEvidenceAndNotBirth": (
        "BindingIsNotEvidenceAndNotBirth: a bound request makes a run "
        "attributable and nothing more. This authority issues no snapshot, no "
        "verdict, and no certificate, and holding a bound request confers "
        "neither evidence nor birth"
    ),
    "OneRequestIsBoundOnce": (
        "OneRequestIsBoundOnce: within one binding authority, one request "
        "content identity is bound to one frozen experiment content id. A "
        "second binding of the same request to a different experiment is "
        "refused rather than recorded, so a single run cannot be attributed "
        "two provenances"
    ),
}
"""The named limits this module freezes; each text opens with its own law name."""


@dataclass(frozen=True, slots=True)
class BoundExperimentalRunRequest(_BoundExperimentalRunRequestSeam):
    """Authority-issued binding of one frozen request to one frozen experiment.

    Constructible only by `ExperimentalRunBindingAuthority.bind`. Neither the
    request's content identity nor the experiment's is accepted from a caller:
    the first is derived by the canonical encoder and the second is read from
    the verified binding.
    """

    binding_id: str
    issuing_authority_id: str
    bound_request: ExperimentalRunRequest
    request_content_id: ExperimentalRunRequestContentIdentity
    binding: BirthExperimentSpecificationContentBinding
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _BINDING_TOKEN:
            raise ExperimentalAuthorityError(
                "bound experimental run requests must be issued by "
                "ExperimentalRunBindingAuthority"
            )
        _require_text(self.binding_id, "experimental run binding id")
        _require_text(self.issuing_authority_id, "experimental binding authority id")
        if type(self.trace) is not Trace:
            raise ExperimentalAuthorityError(
                "a bound experimental run request requires a trace"
            )

    @property
    def request(self) -> ExperimentalRunRequest:
        """The request this binding closed over; the run authority's seam."""

        return self.bound_request

    @property
    def request_content_digest(self) -> str:
        """The canonical content digest of that request; derived, never given."""

        return self.request_content_id.digest

    @property
    def experiment_content_id(self) -> BirthExperimentSpecificationContentIdentity:
        """The frozen experiment's own content id; read from the binding."""

        return self.binding.content_id

    @property
    def domain(self) -> str:
        """The frozen experiment's own domain; read from the binding."""

        return self.binding.specification.domain

    @property
    def confers_authorized_evidence(self) -> bool:
        """`BindingIsNotEvidenceAndNotBirth`; structurally false."""

        return False

    @property
    def confers_birth(self) -> bool:
        """`BindingIsNotEvidenceAndNotBirth`; structurally false."""

        return False

    @property
    def confers_necessity(self) -> bool:
        """Binding a run to a question does not oblige any answer."""

        return False


class ExperimentalRunBindingAuthority:
    """The sole issuer of a `BoundExperimentalRunRequest`; it runs nothing.

    This class exposes `bind` and its own id, and no method that runs an
    experiment, offers evidence, certifies a birth, or admits an entity.

    Binding ids are unique within this authority's own registry, and one
    request content identity is bound to at most one frozen experiment content
    id here. As elsewhere in the kernel, `LocalInjectivity != PortableIdentity`:
    two binding authorities are two uncoordinated issuance scopes.
    """

    def __init__(self, *, authority_id: str) -> None:
        _require_text(authority_id, "experimental binding authority id")
        self._authority_id = authority_id
        self._issued_binding_ids: set[str] = set()
        self._bound_requests: dict[str, str] = {}
        self._lock = threading.Lock()

    @property
    def authority_id(self) -> str:
        return self._authority_id

    def bind(
        self,
        *,
        binding_id: str,
        request: ExperimentalRunRequest,
        binding: BirthExperimentSpecificationContentBinding,
    ) -> BoundExperimentalRunRequest:
        """Bind one request to one frozen experiment, before anything is run."""

        _require_text(binding_id, "experimental run binding id")
        if type(request) is not ExperimentalRunRequest:
            raise ExperimentalAuthorityError(
                "binding requires an experimental run request"
            )
        if type(binding) is not BirthExperimentSpecificationContentBinding:
            raise ExperimentalAuthorityError(
                "binding requires a genuine frozen experiment content binding"
            )
        domain = binding.specification.domain
        if request.declared_scope != domain:
            raise ExperimentalAuthorityError(
                "the request's declared scope must equal the frozen experiment's "
                "domain"
            )

        content_id = CanonicalExperimentalRunRequestEncoder.encode(request).content_id
        experiment_digest = binding.content_id.digest
        specification = binding.specification
        trace = Trace(
            (
                f"binding:{binding_id}",
                f"authority:{self._authority_id}",
                f"candidate:{request.candidate.candidate_id}",
                f"request_content:{content_id.digest}",
                f"domain:{domain}",
                f"experiment:{specification.experiment_id}"
                f"@{specification.revision_id}",
                f"experiment_content:{experiment_digest}",
                "reading:SameDomainIsNotSameExperiment",
                "reading:SameExperimentNameIsNotSameFrozenContent",
                "reading:BindingIsNotEvidenceAndNotBirth",
            )
        )

        with self._lock:
            if binding_id in self._issued_binding_ids:
                raise ExperimentalAuthorityError(
                    "experimental run binding id already issued by this authority"
                )
            already_bound = self._bound_requests.get(content_id.digest)
            if already_bound is not None and already_bound != experiment_digest:
                raise ExperimentalAuthorityError(
                    "this request is already bound to a different frozen "
                    "experiment within this authority"
                )
            self._issued_binding_ids.add(binding_id)
            self._bound_requests[content_id.digest] = experiment_digest

        return BoundExperimentalRunRequest(
            binding_id=binding_id,
            issuing_authority_id=self._authority_id,
            bound_request=request,
            request_content_id=content_id,
            binding=binding,
            trace=trace,
            _token=_BINDING_TOKEN,
        )


_BINDING_AUTHORITY_SURFACE = frozenset({"authority_id", "bind"})


def _public_surface(owner: type) -> frozenset[str]:
    return frozenset(name for name in vars(owner) if not name.startswith("_"))


sweep_forbidden_fields(BoundExperimentalRunRequest)

if _public_surface(ExperimentalRunBindingAuthority) != _BINDING_AUTHORITY_SURFACE:
    raise RuntimeError(
        "ExperimentalRunBindingAuthority must expose no method beyond binding "
        "a request to a frozen experiment"
    )
for _law_name, _law_text in EXPERIMENTAL_BINDING_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("each named law text must open with its own law name")


__all__ = [
    "EXPERIMENTAL_BINDING_NAMED_LAWS",
    "BoundExperimentalRunRequest",
    "ExperimentalRunBindingAuthority",
]
