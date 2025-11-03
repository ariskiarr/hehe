"""
Simple auto commit & push bot.

Usage:
  python commit_bot.py --repo "C:/path/to/repo" --branch main

The script will create/update a timestamped file under .auto_contrib/, git add, commit and push.

Notes:
- Make sure the machine has git installed and accessible in PATH.
- Use SSH auth or cached credentials so git push won't prompt for interactive credentials.
- Ensure the repo's local git user.email matches your GitHub account email to count as contribution.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto commit and push to a git repo (for contribution automation).")
    parser.add_argument("--repo", type=str, default=".", help="Path to the local git repo")
    parser.add_argument("--branch", type=str, default=None, help="Branch to push to (defaults to current)")
    parser.add_argument("--message", type=str, default="Auto contribution {ts}", help="Commit message template. Use {ts} for timestamp")
    parser.add_argument("--file", type=str, default=None, help="File path to write/update relative to repo root")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.exists():
        print(f"ERROR: repo path does not exist: {repo}")
        return 2
    if not is_git_repo(repo):
        print(f"ERROR: Not a git repository: {repo}")
        return 3

    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    # Decide file to touch
    if args.file:
        target = repo / args.file
    else:
        folder = repo / ".auto_contrib"
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / f"contrib-{datetime.utcnow().strftime('%Y%m%d')}.txt"

    # Write or append a line so the file changes
    try:
        with target.open("a", encoding="utf-8") as f:
            f.write(f"Auto commit at {ts}\n")
    except Exception as e:
        print(f"ERROR: Could not write to file {target}: {e}")
        return 4

    # Git add
    r = run(["git", "add", str(target)], cwd=repo)
    if r.returncode != 0:
        print("git add failed:\n", r.stdout, r.stderr)
        return 5

    commit_msg = args.message.format(ts=ts)
    # Commit. If there's nothing to commit (rare because we appended), handle gracefully.
    r = run(["git", "commit", "-m", commit_msg], cwd=repo)
    if r.returncode != 0:
        # If it's because there are no changes, treat as success (no-op)
        combined = (r.stdout or "") + (r.stderr or "")
        if "nothing to commit" in combined.lower() or "no changes added to commit" in combined.lower():
            print("No changes to commit. Exiting OK.")
            return 0
        print("git commit failed:\n", r.stdout, r.stderr)
        return 6

    # Push
    push_cmd = ["git", "push"]
    if args.branch:
        push_cmd = ["git", "push", "origin", args.branch]

    r = run(push_cmd, cwd=repo)
    if r.returncode != 0:
        print("git push failed:\n", r.stdout, r.stderr)
        return 7

    print("Committed and pushed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
