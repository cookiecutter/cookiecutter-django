import datetime as dt
import os
import re
from collections.abc import Iterable
from pathlib import Path
import git
import github.PullRequest
import github.Repository
from github import Github
from jinja2 import Template

CONFIG = {
    "CURRENT_FILE": Path(__file__),
    "ROOT": Path(__file__).parents[1],
    "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
    "GITHUB_REPO": os.getenv("GITHUB_REPOSITORY"),
    "GIT_BRANCH": os.getenv("GITHUB_REF_NAME"),
}


def iter_pulls(repo: github.Repository.Repository, merged_date: dt.date) -> Iterable[github.PullRequest.PullRequest]:
    """Fetch merged pull requests at the date we're interested in."""
    recent_pulls = repo.get_pulls(
        state="closed",
        sort="updated",
        direction="desc",
    ).get_page(0)
    for pull in recent_pulls:
        if pull.merged and pull.merged_at.date() == merged_date:
            yield pull


def group_pulls_by_change_type(pull_requests_list: list[github.PullRequest.PullRequest]) -> dict[str, list[github.PullRequest.PullRequest]]:
    """Group pull requests by change type."""
    grouped_pulls = {
        "Changed": [],
        "Fixed": [],
        "Documentation": [],
        "Updated": [],
    }
    for pull in pull_requests_list:
        label_names = {label.name for label in pull.labels}
        if "project infrastructure" in label_names:
            # Don't mention it in the changelog
            continue
        if "update" in label_names:
            group_name = "Updated"
        elif "bug" in label_names:
            group_name = "Fixed"
        elif "docs" in label_names:
            group_name = "Documentation"
        else:
            group_name = "Changed"
        grouped_pulls[group_name].append(pull)
    return grouped_pulls


def generate_md(grouped_pulls: dict[str, list[github.PullRequest.PullRequest]]) -> str:
    """Generate markdown file from Jinja template."""
    changelog_template = CONFIG["ROOT"] / ".github" / "changelog-template.md"
    template = Template(changelog_template.read_text(), autoescape=True)
    return template.render(grouped_pulls=grouped_pulls)


def write_changelog(file_path: Path, release: str, content: str) -> None:
    """Write Release details to the changelog file."""
    content = f"## {release}\n{content}"
    old_content = file_path.read_text()
    updated_content = old_content.replace(
        "<!-- GENERATOR_PLACEHOLDER -->",
        f"<!-- GENERATOR_PLACEHOLDER -->\n\n{content}",
    )
    file_path.write_text(updated_content)


def update_version(file_path: Path, release: str) -> None:
    """Update template version in setup.py."""
    old_content = file_path.read_text()
    updated_content = re.sub(
        r'\nversion = "\d+\.\d+\.\d+"\n',
        f'\nversion = "{release}"\n',
        old_content,
    )
    file_path.write_text(updated_content)


def update_git_repo(paths: list[Path], release: str) -> None:
    """Commit, tag changes in git repo and push to origin."""
    repo = git.Repo(CONFIG["ROOT"])
    for path in paths:
        repo.git.add(path)
    message = f"Release {release}"

    user = repo.git.config("--get", "user.name")
    email = repo.git.config("--get", "user.email")

    repo.git.commit(
        m=message,
        author=f"{user} <{email}>",
    )
    repo.git.tag("-a", release, m=message)
    server = f"https://{CONFIG['GITHUB_TOKEN']}@github.com/{CONFIG['GITHUB_REPO']}.git"
    print(f"Pushing changes to {CONFIG['GIT_BRANCH']} branch of {CONFIG['GITHUB_REPO']}")
    repo.git.push(server, CONFIG["GIT_BRANCH"])
    repo.git.push("--tags", server, CONFIG["GIT_BRANCH"])


def main() -> None:
    # ... (existing code)


if __name__ == "__main__":
    if CONFIG["GITHUB_REPO"] is None:
        raise RuntimeError("No github repo, please set the environment variable GITHUB_REPOSITORY")
    if CONFIG["GIT_BRANCH"] is None:
        raise RuntimeError("No git branch set, please set the GITHUB_REF_NAME environment variable")
    main()
