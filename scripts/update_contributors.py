import json
from pathlib import Path

import requests
from jinja2 import Template

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
BOT_LOGINS = ["pyup-bot"]


def main() -> None:
    """
    Script entry point.

    1. Fetch recent contribtors from the Github API
    2. Add missing ones to the JSON file
    3. Generate Markdown from JSON file
    """
    # Use Github API to fetch recent authors rather than
    # git CLI because we need to know their GH username
    gh = GitHub()
    recent_authors = set(gh.iter_recent_authors())

    # Add missing users to the JSON file
    contrib_file = ContributorsJSONFile()
    for username in recent_authors:
        print(f"Checking if {username} should be added")
        if username not in contrib_file:
            user_data = gh.fetch_user_info(username)
            contrib_file.add_contributor(user_data)
            print(f"Added {username} to contributors")
    contrib_file.save()

    # Generate MD file from JSON file
    write_md_file(contrib_file.content)


class GitHub:
    """Small wrapper around Github REST API."""

    base_url = "https://api.github.com"

    def __init__(self) -> None:
        self.session = requests.Session()

    def request(self, endpoint):
        response = self.session.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()

    def iter_recent_authors(self):
        commits = self.request("/repos/pydanny/cookiecutter-django/commits")
        for commit in commits:
            login = commit["author"]["login"]
            if login not in BOT_LOGINS:
                yield login

    def fetch_user_info(self, username):
        return self.request(f"/users/{username}")


class ContributorsJSONFile:
    """Helper to interact with the JSON file."""

    file_path = ROOT / ".github" / "contributors.json"
    content = None

    def __init__(self) -> None:
        """Read initial content."""
        self.content = json.loads(self.file_path.read_text())

    def __contains__(self, github_login: str):
        """Provide a nice API to do: `username in file`."""
        return any(github_login == contrib["github_login"] for contrib in self.content)

    def add_contributor(self, user_data):
        """Append the contributor data we care about at the end."""
        contributor_data = {
            "name": user_data["name"],
            "github_login": user_data["login"],
            "twitter_username": user_data["twitter_username"],
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
    content = template.render(
        core_contributors=core_contributors, other_contributors=other_contributors
    )

    file_path = ROOT / "CONTRIBUTORS.md"
    file_path.write_text(content)


if __name__ == "__main__":
    main()
