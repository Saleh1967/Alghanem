import pytest

from alghanem.encyclopedia.self_observation import (
    AuthenticatedRepositoryArtifact,
    AuthenticatedRepositoryFragment,
    AuthenticatedRepositorySnapshot,
    AuthenticatedRepositoryTransition,
    RepositoryArtifactChangeRef,
    RepositoryArtifactRef,
    RepositoryFragmentRef,
    RepositoryObservationAuthority,
    RepositoryObservationRequest,
    RepositorySnapshotRef,
    RepositoryTransitionRef,
    SelfObservationContractError,
)


def snapshot(
    commit_sha: str = "c1",
    tree_sha: str = "t1",
    repository_identity: str = "Alghanem",
) -> RepositorySnapshotRef:
    return RepositorySnapshotRef(
        repository_identity=repository_identity,
        commit_sha=commit_sha,
        tree_sha=tree_sha,
    )


def artifact(
    snap: RepositorySnapshotRef | None = None,
    path: str = "src/alghanem/encyclopedia/inquiry.py",
    blob_sha: str = "blob-1",
) -> RepositoryArtifactRef:
    return RepositoryArtifactRef(
        snapshot=snap if snap is not None else snapshot(),
        artifact_path=path,
        blob_sha=blob_sha,
    )


class TestRepositorySnapshotRef:
    @pytest.mark.parametrize(
        "field_name", ["repository_identity", "commit_sha", "tree_sha"]
    )
    def test_rejects_blank_fields(self, field_name: str) -> None:
        kwargs = {
            "repository_identity": "Alghanem",
            "commit_sha": "c1",
            "tree_sha": "t1",
        }
        kwargs[field_name] = ""

        with pytest.raises(SelfObservationContractError):
            RepositorySnapshotRef(**kwargs)

    @pytest.mark.parametrize(
        "field_name", ["repository_identity", "commit_sha", "tree_sha"]
    )
    def test_rejects_whitespace_only_fields(self, field_name: str) -> None:
        kwargs = {
            "repository_identity": "Alghanem",
            "commit_sha": "c1",
            "tree_sha": "t1",
        }
        kwargs[field_name] = "   "

        with pytest.raises(SelfObservationContractError):
            RepositorySnapshotRef(**kwargs)

    def test_distinct_commits_are_distinct_snapshots(self) -> None:
        assert snapshot("c1") != snapshot("c2")


class TestRepositoryArtifactRef:
    def test_requires_repository_snapshot_ref(self) -> None:
        with pytest.raises(SelfObservationContractError):
            RepositoryArtifactRef(
                snapshot="not-a-snapshot",  # type: ignore[arg-type]
                artifact_path="src/alghanem/encyclopedia/inquiry.py",
                blob_sha="blob-1",
            )

    @pytest.mark.parametrize("field_name", ["artifact_path", "blob_sha"])
    def test_rejects_blank_fields(self, field_name: str) -> None:
        kwargs = {
            "snapshot": snapshot(),
            "artifact_path": "src/alghanem/encyclopedia/inquiry.py",
            "blob_sha": "blob-1",
        }
        kwargs[field_name] = ""

        with pytest.raises(SelfObservationContractError):
            RepositoryArtifactRef(**kwargs)

    def test_same_path_at_different_commit_is_a_different_occurrence(self) -> None:
        first = artifact(snapshot("c1"))
        second = artifact(snapshot("c2"))

        assert first != second


class TestRepositoryFragmentRef:
    def test_accepts_a_well_formed_fragment_ref(self) -> None:
        fragment = RepositoryFragmentRef(
            artifact=artifact(),
            fragment_locator="RootInquiry",
            fragment_content_id="fragment-1",
        )

        assert fragment.artifact == artifact()
        assert fragment.fragment_locator == "RootInquiry"
        assert fragment.fragment_content_id == "fragment-1"

    def test_requires_repository_artifact_ref(self) -> None:
        with pytest.raises(SelfObservationContractError):
            RepositoryFragmentRef(
                artifact="not-an-artifact",  # type: ignore[arg-type]
                fragment_locator="RootInquiry",
                fragment_content_id="fragment-1",
            )

    @pytest.mark.parametrize("field_name", ["fragment_locator", "fragment_content_id"])
    def test_rejects_blank_fields(self, field_name: str) -> None:
        kwargs = {
            "artifact": artifact(),
            "fragment_locator": "RootInquiry",
            "fragment_content_id": "fragment-1",
        }
        kwargs[field_name] = ""

        with pytest.raises(SelfObservationContractError):
            RepositoryFragmentRef(**kwargs)


class TestRepositoryArtifactChangeRef:
    def test_requires_repository_artifact_refs(self) -> None:
        with pytest.raises(SelfObservationContractError):
            RepositoryArtifactChangeRef(
                before="not-an-artifact",  # type: ignore[arg-type]
                after=artifact(),
            )
        with pytest.raises(SelfObservationContractError):
            RepositoryArtifactChangeRef(
                before=artifact(),
                after="not-an-artifact",  # type: ignore[arg-type]
            )

    def test_requires_the_same_artifact_path_on_both_sides(self) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        with pytest.raises(SelfObservationContractError):
            RepositoryArtifactChangeRef(
                before=artifact(from_snap, path="a.py", blob_sha="blob-a"),
                after=artifact(to_snap, path="b.py", blob_sha="blob-b"),
            )

    def test_requires_distinct_blob_shas(self) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        with pytest.raises(SelfObservationContractError):
            RepositoryArtifactChangeRef(
                before=artifact(from_snap, path="a.py", blob_sha="blob-a"),
                after=artifact(to_snap, path="a.py", blob_sha="blob-a"),
            )

    def test_requires_the_same_repository_identity_on_both_sides(self) -> None:
        from_snap = snapshot("c1", repository_identity="Alghanem")
        to_snap = snapshot("c2", repository_identity="OtherRepository")

        with pytest.raises(SelfObservationContractError):
            RepositoryArtifactChangeRef(
                before=artifact(from_snap, path="a.py", blob_sha="blob-a"),
                after=artifact(to_snap, path="a.py", blob_sha="blob-b"),
            )

    def test_requires_distinct_snapshot_commit_shas(self) -> None:
        same_snap = snapshot("c1")

        with pytest.raises(SelfObservationContractError):
            RepositoryArtifactChangeRef(
                before=artifact(same_snap, path="a.py", blob_sha="blob-a"),
                after=artifact(same_snap, path="a.py", blob_sha="blob-b"),
            )

    def test_accepts_a_well_formed_change(self) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        change = RepositoryArtifactChangeRef(
            before=artifact(from_snap, path="a.py", blob_sha="blob-a"),
            after=artifact(to_snap, path="a.py", blob_sha="blob-b"),
        )

        assert change.artifact_path == "a.py"


class TestRepositoryTransitionRef:
    def test_requires_distinct_from_and_to_snapshots(self) -> None:
        same = snapshot("c1")

        with pytest.raises(SelfObservationContractError):
            RepositoryTransitionRef(
                from_snapshot=same,
                to_snapshot=same,
                changed_artifacts=(),
                added_artifacts=(),
                removed_artifacts=(),
            )

    def test_requires_the_same_repository_identity(self) -> None:
        from_snap = snapshot("c1", repository_identity="Alghanem")
        to_snap = snapshot("c2", repository_identity="OtherRepository")

        with pytest.raises(SelfObservationContractError):
            RepositoryTransitionRef(
                from_snapshot=from_snap,
                to_snapshot=to_snap,
                changed_artifacts=(),
                added_artifacts=(),
                removed_artifacts=(),
            )

    def test_added_artifacts_must_be_anchored_to_to_snapshot(self) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        with pytest.raises(SelfObservationContractError):
            RepositoryTransitionRef(
                from_snapshot=from_snap,
                to_snapshot=to_snap,
                changed_artifacts=(),
                added_artifacts=(artifact(from_snap),),
                removed_artifacts=(),
            )

    def test_removed_artifacts_must_be_anchored_to_from_snapshot(self) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        with pytest.raises(SelfObservationContractError):
            RepositoryTransitionRef(
                from_snapshot=from_snap,
                to_snapshot=to_snap,
                changed_artifacts=(),
                added_artifacts=(),
                removed_artifacts=(artifact(to_snap),),
            )

    def test_changed_artifacts_before_side_must_be_anchored_to_from_snapshot(
        self,
    ) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        with pytest.raises(SelfObservationContractError):
            RepositoryTransitionRef(
                from_snapshot=from_snap,
                to_snapshot=to_snap,
                changed_artifacts=(
                    RepositoryArtifactChangeRef(
                        before=artifact(to_snap, path="a.py", blob_sha="blob-a"),
                        after=artifact(to_snap, path="a.py", blob_sha="blob-b"),
                    ),
                ),
                added_artifacts=(),
                removed_artifacts=(),
            )

    def test_changed_artifacts_after_side_must_be_anchored_to_to_snapshot(
        self,
    ) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        with pytest.raises(SelfObservationContractError):
            RepositoryTransitionRef(
                from_snapshot=from_snap,
                to_snapshot=to_snap,
                changed_artifacts=(
                    RepositoryArtifactChangeRef(
                        before=artifact(from_snap, path="a.py", blob_sha="blob-a"),
                        after=artifact(from_snap, path="a.py", blob_sha="blob-b"),
                    ),
                ),
                added_artifacts=(),
                removed_artifacts=(),
            )

    def test_rejects_duplicate_artifact_paths_within_one_bucket(self) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        with pytest.raises(SelfObservationContractError):
            RepositoryTransitionRef(
                from_snapshot=from_snap,
                to_snapshot=to_snap,
                changed_artifacts=(),
                added_artifacts=(
                    artifact(to_snap, path="a.py"),
                    artifact(to_snap, path="a.py"),
                ),
                removed_artifacts=(),
            )

    def test_rejects_duplicate_artifact_paths_across_buckets(self) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        with pytest.raises(SelfObservationContractError):
            RepositoryTransitionRef(
                from_snapshot=from_snap,
                to_snapshot=to_snap,
                changed_artifacts=(),
                added_artifacts=(artifact(to_snap, path="same.py"),),
                removed_artifacts=(artifact(from_snap, path="same.py"),),
            )

    def test_accepts_a_well_formed_transition(self) -> None:
        from_snap = snapshot("c1")
        to_snap = snapshot("c2")

        transition = RepositoryTransitionRef(
            from_snapshot=from_snap,
            to_snapshot=to_snap,
            changed_artifacts=(
                RepositoryArtifactChangeRef(
                    before=artifact(from_snap, path="changed.py", blob_sha="blob-a"),
                    after=artifact(to_snap, path="changed.py", blob_sha="blob-b"),
                ),
            ),
            added_artifacts=(artifact(to_snap, path="added.py"),),
            removed_artifacts=(artifact(from_snap, path="removed.py"),),
        )

        assert transition.from_snapshot == from_snap
        assert transition.to_snapshot == to_snap


class FakeProvider:
    provider_identity = "fixture"
    implementation_identity = "fixture-v1"
    protocol_version = "1"

    def resolve_repository(self, identity: str) -> str | None:
        return identity if identity == "Alghanem" else None

    def resolve_commit(self, repository: str, commit_sha: str) -> str | None:
        return commit_sha if commit_sha in {"c1", "c2", "c3"} else None

    def tree_for_commit(self, commit: str) -> str:
        return {"c1": "t1", "c2": "t2", "c3": "t3"}[commit]

    def blob_at_path(self, tree_sha: str, path: str) -> str | None:
        return {"t1": "b1", "t2": "b2", "t3": "b3"}.get(tree_sha)

    def fragment_from_blob(self, blob_sha: str, locator: str) -> str | None:
        return f"{blob_sha}:{locator}" if locator else None

    def is_ancestor(self, repository: str, from_sha: str, to_sha: str) -> bool:
        return (from_sha, to_sha) == ("c1", "c2")


def authenticated_run():
    return RepositoryObservationAuthority(FakeProvider()).open_run()


def test_authenticated_types_have_no_public_issue_helpers() -> None:
    assert not hasattr(AuthenticatedRepositorySnapshot, "_issue")
    assert not hasattr(AuthenticatedRepositoryArtifact, "_issue")
    assert not hasattr(AuthenticatedRepositoryFragment, "_issue")
    assert not hasattr(AuthenticatedRepositoryTransition, "_issue")


def test_one_run_can_authenticate_and_transition_two_snapshots() -> None:
    run = authenticated_run()
    first = run.observe_snapshot(snapshot("c1", "t1"))
    second = run.observe_snapshot(snapshot("c2", "t2"))

    transition = run.observe_transition(first, second)

    assert transition.from_snapshot is first
    assert transition.to_snapshot is second


def test_cross_run_transition_is_rejected() -> None:
    first = authenticated_run().observe_snapshot(snapshot("c1", "t1"))
    second = authenticated_run().observe_snapshot(snapshot("c2", "t2"))

    with pytest.raises(SelfObservationContractError):
        authenticated_run().observe_transition(first, second)


def test_non_ancestral_transition_is_rejected() -> None:
    run = authenticated_run()
    first = run.observe_snapshot(snapshot("c2", "t2"))
    second = run.observe_snapshot(snapshot("c3", "t3"))

    with pytest.raises(SelfObservationContractError):
        run.observe_transition(first, second)


def test_request_remains_an_address_and_observation_authenticates_it() -> None:
    request = RepositoryObservationRequest(snapshot("c1", "t1"))
    observed = RepositoryObservationAuthority(FakeProvider()).observe(request)

    assert observed.snapshot == request.requested_snapshot


def test_fake_snapshot_tree_is_rejected() -> None:
    with pytest.raises(SelfObservationContractError):
        authenticated_run().observe_snapshot(snapshot("c1", "fake-tree"))


def test_fake_artifact_blob_is_rejected() -> None:
    run = authenticated_run()
    observed = run.observe_snapshot(snapshot("c1", "t1"))

    with pytest.raises(SelfObservationContractError):
        run.observe_artifact(observed, artifact(snapshot("c1", "t1"), blob_sha="fake"))


def test_missing_fragment_is_rejected() -> None:
    run = authenticated_run()
    observed = run.observe_snapshot(snapshot("c1", "t1"))
    observed_artifact = run.observe_artifact(
        observed, artifact(snapshot("c1", "t1"), blob_sha="b1")
    )

    with pytest.raises(SelfObservationContractError):
        run.observe_fragment(observed_artifact, "")


def test_authenticated_objects_and_runs_reject_direct_construction() -> None:
    with pytest.raises(SelfObservationContractError):
        AuthenticatedRepositorySnapshot(snapshot(), None)  # type: ignore[arg-type]
    with pytest.raises(SelfObservationContractError):
        AuthenticatedRepositoryArtifact(None, "", "", None)  # type: ignore[arg-type]
    with pytest.raises(SelfObservationContractError):
        AuthenticatedRepositoryFragment(None, "", "", None)  # type: ignore[arg-type]
    with pytest.raises(SelfObservationContractError):
        AuthenticatedRepositoryTransition(None, None, None)  # type: ignore[arg-type]
    with pytest.raises(SelfObservationContractError):
        RepositoryObservationAuthority(FakeProvider()).open_run().__class__(
            "run", "provider", "implementation", "1", FakeProvider()
        )
