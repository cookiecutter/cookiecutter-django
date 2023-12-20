import json
import os
import re
from datetime import datetime
from pathlib import Path

import yaml
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

    # Generate cff file from JSON file
    cff_writer = CitationCFFFile()
    cff_writer.save_cff(contrib_file.content)


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


class CitationCFFFile:
    """Helper to interact with the CITATION.cff file."""

    cff_dict: dict

    def __init__(self, output_path: Path = ROOT / "CITATION.cff") -> None:
        """Read initial content."""
        self.output_path = output_path

    @staticmethod
    def read_version_from_setup(root_path: Path) -> str:
        """Read the version string from setup.py, or return today's date if not found."""
        setup_path = root_path / "setup.py"
        version_pattern = re.compile(r"version\s*=\s*['\"]([^'\"]+)['\"]")
        with open(setup_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = version_pattern.search(line)
                if match:
                    return match.group(1)
        # Return today's date in the format YYYY-MM-DD if no version is found
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def parse_contributor_dict(contributor: dict) -> dict:
        """extract the `name` field and split on the first space. return a dict
        where the first value is the `family-names` and the rest is the `given-names`
        if there is no split, the whole string is the `family-names` and the given-names is empty
        """
        name = contributor.get("name", "")
        name_parts = name.split(" ", 1)
        if len(name_parts) == 1:
            return {"family-names": name_parts[0], "given-names": ""}
        else:
            return {"family-names": name_parts[1], "given-names": name_parts[0]}

    def save_cff(self, contributors: list) -> dict:
        """Provide default content for CITATION.cff."""
        version_date = self.read_version_from_setup(ROOT)

        core_contribs = [self.parse_contributor_dict(c) for c in contributors if c.get("is_core", False)]
        core_contribs.append({"name": "Community Contributors"})

        cff_content = {
            "cff-version": "1.2.0",
            "message": "If you use this software, please cite it as below.",
            "title": "cookiecutter-django",
            "version": version_date,
            "date-released": version_date,
            "authors": core_contribs,
            "abstract": "Cookiecutter Django is a framework for jumpstarting "
            "production-ready Django projects quickly.",
            "notes": "This project has received contributions from many individuals, "
            "for which we are grateful. For a full list of contributors, see the CONTRIBUTORS.md in the repository",
            "repository-code": "https://github.com/cookiecutter/cookiecutter-django"
        }

        with open(self.output_path, 'w', encoding='utf-8') as file:
            yaml.dump(cff_content, file, default_flow_style=False)


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
