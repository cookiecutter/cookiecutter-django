import json
import os
from pathlib import Path

from github import Github
from github.NamedUser import NamedUser
from jinja2 import Template

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
BOT_LOGINS = ["pyup-bot"]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY", None)


def main() -> None:
    """
    Script entry point.

    1. Fetch recent contributors from the Github API
    2. Add missing ones to the JSON file
    3. Generate Markdown from JSON file
    """
    recent_authors = set(iter_recent_authors())

    # Add missing users to the JSON file
    contrib_file = ContributorsJSONFile()
    for author in recent_authors:
        print(f"Checking if {author.login} should be added")
        if author.login not in contrib_file:
            contrib_file.add_contributor(author)
            print(f"Added {author.login} to contributors")
    contrib_file.save()

    # Generate MD file from JSON file
    write_md_file(contrib_file.content)


def iter_recent_authors():
    """
    Fetch users who opened recently merged pull requests.

    Use Github API to fetch recent authors rather than
    git CLI to work with Github usernames.
    """
    repo = Github(login_or_token=GITHUB_TOKEN, per_page=5).get_repo(GITHUB_REPO)
    recent_pulls = repo.get_pulls(state="closed", sort="updated", direction="desc").get_page(0)
    for pull in recent_pulls:
        if pull.merged and pull.user.type == "User" and pull.user.login not in BOT_LOGINS:
            yield pull.user


class ContributorsJSONFile:
    """Helper to interact with the JSON file."""

    file_path = ROOT / ".github" / "contributors.json"
    content = None

    def __init__(self) -> None:
        """Read initial content."""
        self.content = json.loads(self.file_path.read_text())

    def __contains__(self, github_login: str):
        """Provide a nice API to do: `username in file`."""
        return any(
            # Github usernames are case insensitive
            github_login.lower() == contrib["github_login"].lower()
            for contrib in self.content
        )

    def add_contributor(self, user: NamedUser):
        """Append the contributor data we care about at the end."""
        contributor_data = {
            "name": user.name or user.login,
            "github_login": user.login,
            "twitter_username": user.twitter_username or "",
        }
        self.content.append(contributor_data)

    def save(self):
        """Write the file to disk with indentation."""
        text_content = json.dumps(self.content, indent=2, ensure_ascii=False)
        self.file_path.write_text(text_content)


def write_md_file(contributors):
    """Generate markdown file from Jinja template."""
    contributors_template = ROOT / ".github" / "CONTRIBUTORS-template.md"
    template = Template(contributors_template.read_text(), autoescape=True)
    core_contributors = [c for c in contributors if c.get("is_core", False)]
    other_contributors = (c for c in contributors if not c.get("is_core", False))
    other_contributors = sorted(other_contributors, key=lambda c: c["name"].lower())
    content = template.render(core_contributors=core_contributors, other_contributors=other_contributors)

    file_path = ROOT / "CONTRIBUTORS.md"
    file_path.write_text(content)


if __name__ == "__main__":
    if GITHUB_REPO is None:
        raise RuntimeError("No github repo, please set the environment variable GITHUB_REPOSITORY")
    main()
