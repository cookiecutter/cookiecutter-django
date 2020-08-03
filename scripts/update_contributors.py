import json
from pathlib import Path

import requests
from jinja2 import Template

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
BOT_LOGINS = ["pyup-bot"]
OUTPUT_FILE_PATH = ROOT / "CONTRIBUTORS.rst"

CONTRIBUTORS_TABLE_TEMPLATE = """
<table>
  <tr>
    <th>Name</th>
    <th>Github</th>
    <th>Twitter</th>
  </tr>
  {%- for contributor in contributors %}
  <tr>
    <td>{{ contributor.name }}</td>
    <td>
      <a href="https://github.com/{{ contributor.github_login }}">{{ contributor.github_login }}</a>
    </td>
    <td>{{ contributor.twitter_username }}</td>
  </tr>
  {%- endfor %}
</table>
"""


def main() -> None:
    gh = GitHub()
    recent_authors = set(gh.iter_recent_authors())
    contrib_file = ContributorsJSONFile()
    for username in recent_authors:
        if username not in contrib_file:
            user_data = gh.fetch_user_info(username)
            contrib_file.add_contributor(user_data)
    contrib_file.save()

    rst_file = ContributorsRSTFile()
    rst_file.generate_table(contrib_file.content)
    rst_file.save()


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
        with self.file_path.open() as fd:
            self.content = json.load(fd)

    def __contains__(self, github_login: str):
        return any(github_login == contrib["github_login"] for contrib in self.content)

    def add_contributor(self, user_data):
        contributor_data = {
            "name": user_data["name"],
            "github_login": user_data["login"],
            "twitter_username": user_data["twitter_username"],
        }
        new_content = self.content + [contributor_data]
        self.content = sorted(new_content, key=lambda user: user["name"])

    def save(self):
        with self.file_path.open("w") as fd:
            json.dump(self.content, fd, indent=2)


class ContributorsRSTFile:
    file_path = ROOT / "CONTRIBUTORS.md"
    content = None
    marker_start = "<!-- BEGIN-GENERATED-CONTENT -->"
    marker_end = "<!-- END-GENERATED-CONTENT -->"

    def __init__(self) -> None:
        with self.file_path.open() as fd:
            content = fd.read()
        self.before, rest_initial = content.split(f"{self.marker_start}")
        self.middle, self.after = rest_initial.split(f"{self.marker_end}")

    def generate_table(self, profiles_list):
        template = Template(CONTRIBUTORS_TABLE_TEMPLATE, autoescape=True)
        contributors = [profile for profile in profiles_list if not profile.get("is_core", False)]
        self.middle = template.render(contributors=contributors)

    def save(self):
        with self.file_path.open("w") as fd:
            new_content = "\n".join(
                [
                    self.before,
                    self.marker_start,
                    self.middle,
                    self.marker_end,
                    self.after,
                ]
            )

            fd.write(new_content)


if __name__ == "__main__":
    template = Template(CONTRIBUTORS_TABLE_TEMPLATE, autoescape=True)
    contrib_file = ContributorsJSONFile()
    contributors = [profile for profile in contrib_file.content if profile.get("is_core", False)]
    print(template.render(contributors=contributors))
