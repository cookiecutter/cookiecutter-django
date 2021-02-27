import json
import os
from pathlib import Path
from github import Github

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)


def main() -> None:
    """
    Script entry point.
    """
    repo = Github(login_or_token=GITHUB_TOKEN).get_repo("github/choosealicense.com")
    license_dir = ROOT / "{{cookiecutter.project_slug}}" / "licenses"
    titles = []
    for file in repo.get_contents("_licenses", "gh-pages"):
        content = file.decoded_content.decode(file.encoding)
        titles.append(content.split("\n", maxsplit=2)[1].replace("title: ", ""))
        (license_dir / file.name).write_text(content)
    # Put "Not open source" at front so people know it's an option
    update_cookiecutter(["Not open source"] + sorted(titles))


def update_cookiecutter(titles: list):
    with open("cookiecutter.json") as f:
        data = json.load(f)
    data["open_source_license"] = titles
    with open("cookiecutter.json", "wt") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
