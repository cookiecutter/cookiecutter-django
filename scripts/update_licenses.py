import codecs
import json
import os
import re
from pathlib import Path

from github import Github

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def main() -> None:
    """
    Script entry point.
    """
    titles_dict = {}
    repo = Github(login_or_token=GITHUB_TOKEN).get_repo("github/choosealicense.com")
    license_dir = ROOT / "{{cookiecutter.project_slug}}" / "licenses"
    license_dir.mkdir(exist_ok=True)
    for file in repo.get_contents("_licenses", "gh-pages"):
        content = codecs.decode(file.decoded_content)
        # make below line into a dictionary mapping to filename
        titles_dict[content.split("\n", maxsplit=2)[1].replace("title: ", "")] = file.name
        path = license_dir / file.name
        if not path.is_file():
            path.touch()
            (license_dir / file.name).write_text(replace_content_options(content))

    # write the titles dictionary to a json file so it can be accessed by other files
    with open("{{cookiecutter.project_slug}}/licenses/licenses.json", "w") as licenses_dict:
        json.dump(titles_dict, licenses_dict, indent=2)
    # Put "Not open source" at front so people know it's an option
    front_options = [
        "Not open source",
        "MIT License",
        'BSD 3-Clause "New" or "Revised" License',
        "GNU General Public License v3.0",
        "Apache License 2.0",
    ]
    # update to iterate through dictionary
    titles = [x for x in sorted(titles_dict.keys()) if x not in front_options]
    update_cookiecutter(front_options + titles)


year = (re.compile(r"\[year]"), "{% now 'utc', '%Y' %}")
email = (re.compile(r"\[email]"), "{{ cookiecutter.email }}")
fullname = (re.compile(r"\[fullname]"), "{{ cookiecutter.author_name }}")
project = (re.compile(r"\[project]"), "{{ cookiecutter.project_name }}")
projecturl = (re.compile(r"\[projecturl]"), "{{ cookiecutter.domain_name }}")


def replace_content_options(content) -> str:
    for compiled, replace in (year, email, fullname, project, projecturl):
        content = compiled.sub(replace, content)
    return content


def update_cookiecutter(titles: list):
    with open("cookiecutter.json") as f:
        data = json.load(f)
    data["open_source_license"] = titles
    with open("cookiecutter.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
