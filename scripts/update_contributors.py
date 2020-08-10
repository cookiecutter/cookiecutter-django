import json
from pathlib import Path

import requests
from jinja2 import Template

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
BOT_LOGINS = ["pyup-bot"]

CONTRIBUTORS_TEMPLATE = """
# Contributors

## Core Developers

These contributors have commit flags for the repository, and are able to
accept and merge pull requests.

<table>
  <tr>
    <th>Name</th>
    <th>Github</th>
    <th>Twitter</th>
  </tr>
  {%- for contributor in core_contributors %}
  <tr>
    <td>{{ contributor.name }}</td>
    <td>
      <a href="https://github.com/{{ contributor.github_login }}">{{ contributor.github_login }}</a>
    </td>
    <td>{{ contributor.twitter_username }}</td>
  </tr>
  {%- endfor %}
</table>

*Audrey is also the creator of Cookiecutter. Audrey and Daniel are on
the Cookiecutter core team.*

## Other Contributors

Listed in alphabetical order.

<table>
  <tr>
    <th>Name</th>
    <th>Github</th>
    <th>Twitter</th>
  </tr>
  {%- for contributor in other_contributors %}
  <tr>
    <td>{{ contributor.name }}</td>
    <td>
      <a href="https://github.com/{{ contributor.github_login }}">{{ contributor.github_login }}</a>
    </td>
    <td>{{ contributor.twitter_username }}</td>
  </tr>
  {%- endfor %}
</table>

### Special Thanks

The following haven't provided code directly, but have provided
guidance and advice.

-   Jannis Leidel
-   Nate Aune
-   Barry Morrison
"""


def main() -> None:
    gh = GitHub()
    recent_authors = set(gh.iter_recent_authors())
    contrib_file = ContributorsJSONFile()
    for username in recent_authors:
        if username not in contrib_file and username not in BOT_LOGINS:
            user_data = gh.fetch_user_info(username)
            contrib_file.add_contributor(user_data)
    contrib_file.save()

    write_md_file(contrib_file.content)


class GitHub:
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
    file_path = ROOT / ".github" / "contributors.json"
    content = None

    def __init__(self) -> None:
        self.content = json.loads(self.file_path.read_text())

    def __contains__(self, github_login: str):
        return any(github_login == contrib["github_login"] for contrib in self.content)

    def add_contributor(self, user_data):
        contributor_data = {
            "name": user_data["name"],
            "github_login": user_data["login"],
            "twitter_username": user_data["twitter_username"],
        }
        self.content.extend(contributor_data)

    def save(self):
        text_content = json.dumps(self.content, indent=2, ensure_ascii=False)
        self.file_path.write_text(text_content)


def write_md_file(contributors):
    template = Template(CONTRIBUTORS_TEMPLATE, autoescape=True)
    core_contributors = [c for c in contributors if c.get("is_core", False)]
    other_contributors = (c for c in contributors if not c.get("is_core", False))
    other_contributors = sorted(other_contributors, key=lambda c: c["name"])
    content = template.render(
        core_contributors=core_contributors, other_contributors=other_contributors
    )

    file_path = ROOT / "CONTRIBUTORS.md"
    file_path.write_text(content)


if __name__ == "__main__":
    main()
