"""Git provenance for eval runs.

Every agent run records which repo snapshot produced it, so a run can be tied back
to the exact recipe, tool-description prompts, and loop code that were live. The git
commit SHA is a content fingerprint of every tracked file at that commit, so unlike
the human-maintained recipe_version string it cannot be edited without changing
(the v0.4.0-edited-in-place problem).

Resolved once at import: the commit does not change while a process runs. In the
production image the `.git` directory may be absent, so the SHA falls back to a
build-time env var (GIT_SHA) and finally to "unknown"; a request never fails over
missing provenance.
"""
import os
import subprocess

from pydantic import BaseModel

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Provenance(BaseModel):
    """Repo fingerprint stamped on every run."""

    git_sha: str        # commit SHA, or a build-time env / "unknown" fallback
    git_dirty: bool     # True if the working tree had uncommitted changes to tracked files


def _run_git(*args: str) -> str | None:
    """Return the trimmed stdout of a git command, or None if git can't answer here
    (not installed, no repo, or a non-zero exit)."""
    try:
        out = subprocess.run(
            ["git", *args],
            capture_output=True, text=True, timeout=5, cwd=_REPO_ROOT,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def _resolve() -> Provenance:
    # `git rev-parse HEAD` resolves the ref HEAD (the current branch tip) to its full
    # 40-char commit SHA. That SHA is a content hash over the whole committed tree, so
    # it fingerprints every tracked file (recipe, tool prompts, loop code) at once.
    sha = _run_git("rev-parse", "HEAD")
    if sha is not None:
        # `git status --porcelain` lists working-tree changes in a stable, script-friendly
        # format: one line per modified/added/deleted tracked path, and nothing at all when
        # the tree is clean. So a non-empty result means uncommitted edits exist, i.e. the
        # SHA above does not fully describe what ran; empty means the SHA is exact.
        dirty = _run_git("status", "--porcelain")
        return Provenance(git_sha=sha, git_dirty=bool(dirty))
    # No git available (e.g. the prod image without .git): use the build-stamped SHA.
    return Provenance(git_sha=os.environ.get("GIT_SHA", "unknown"), git_dirty=False)


PROVENANCE = _resolve()
