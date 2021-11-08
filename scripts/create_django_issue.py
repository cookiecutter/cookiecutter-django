"""
Creates an issue that generates a table for dependency checking whether
all packages support the latest Django version. "Latest" does not include
patches, only comparing major and minor version numbers.

This script handles when there are multiple Django versions that need
to keep up to date.
"""

import os
from typing import Sequence, TYPE_CHECKING

import requests
import sys
from pathlib import Path

from github import Github


if TYPE_CHECKING:
    from github.Issue import Issue

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
REQUIREMENTS_DIR = ROOT / "{{cookiecutter.project_slug}}" / "requirements"
GITHUB_REPO = "cookiecutter/cookiecutter-django"


def get_package_info(package: str) -> dict:
    # "django" converts to "Django" on redirect
    r = requests.get(f"https://pypi.org/pypi/{package}/json", allow_redirects=True)
    if not r.ok:
        print(f"Couldn't find package: {package}")
        sys.exit(1)
    return r.json()


def get_package_versions(package_info: dict, reverse=True, *, include_pre=False):
    # Mostly used for the Django check really... to get the latest
    # package version, you could simple do get_package_info()["info"]["version"]
    releases: Sequence[str] = package_info["releases"].keys()
    if not include_pre:
        releases = [x for x in releases if x.replace(".", "").isdigit()]
    return sorted(releases, reverse=reverse)


def get_name_and_version(requirements_line: str) -> tuple[str, str]:
    full_name, version = requirements_line.split(" ", 1)[0].split("==")
    name_without_extras = full_name.split("[", 1)[0]
    return name_without_extras, version


def get_all_latest_django_versions() -> tuple[str, list[str]]:
    """
    Grabs all Django versions that are worthy of a GitHub issue. Depends on
    if Django versions has higher major version or minor version
    """
    base_txt = REQUIREMENTS_DIR / "base.txt"
    with base_txt.open() as f:
        for line in f.readlines():
            if "django==" in line:
                break
        else:
            print(f"django not found in {base_txt}")  # Huh...?
            sys.exit(1)

    # Begin parsing and verification
    _, current_version_str = get_name_and_version(line)
    # Get a tuple of (major, minor) - ignoring patch version
    current_minor_version = tuple(current_version_str.split(".")[:2])
    all_django_versions = get_package_versions(get_package_info("django"))
    newer_versions: set[tuple] = set()
    for version_str in all_django_versions:
        released_minor_version = tuple(version_str.split(".")[:2])
        if released_minor_version > current_minor_version:
            newer_versions.add(released_minor_version)

    needed_versions_str = ['.'.join(v) for v in sorted(newer_versions)]
    return line, needed_versions_str


def get_first_digit(tokens) -> str:
    return next(item for item in tokens if item.isdigit())


_TABLE_HEADER = """

## {file}.txt

| Name | Version in Master | {dj_version} Compatible Version | OK |
| ---- | :---------------: | :-----------------------------: | :-: |
"""
VITAL_BUT_UNKNOWN = [
    "django-environ",  # not updated often
    "pylint-django",  # classifier not included in setup.py
]


class GitHubManager:
    def __init__(self, base_dj_version: str, needed_dj_versions: list[str]):
        self.github = Github(os.getenv("GITHUB_TOKEN", None))
        self.repo = self.github.get_repo(GITHUB_REPO)

        self.base_dj_version = base_dj_version
        self.needed_dj_versions = needed_dj_versions
        # (major+minor) Version and description
        self.existing_issues: dict[str, "Issue"] = {}

        # Load all requirements from our requirements files and preload their
        # package information like a cache:
        self.requirements_files = ["base", "local", "production"]
        # Format:
        # requirement file name: {package name: (master_version, package_info)}
        self.requirements: dict[str, dict[str, tuple[str, dict]]] = {
            x: {} for x in self.requirements_files
        }

    def setup(self) -> None:
        self.load_requirements()
        self.load_existing_issues()

    def load_requirements(self):
        for requirements_file in self.requirements_files:
            with (REQUIREMENTS_DIR / f"{requirements_file}.txt").open() as f:
                for line in f.readlines():
                    if "==" in line and not line.startswith('{%'):
                        name, version = get_name_and_version(line)
                        self.requirements[requirements_file][name] = (
                            version, get_package_info(name)
                        )

    def load_existing_issues(self):
        """Closes the issue if the base Django version is greater than the needed"""
        qualifiers = {
            "repo": GITHUB_REPO,
            "author": "actions-user",
            "state": "open",
            "is": "issue",
            "in": "title",
        }
        issues = list(
            self.github.search_issues(
                "[Django Update]", "created", "desc", **qualifiers
            )
        )
        for issue in issues:
            try:
                dj_version = get_first_digit(issue.title.split(" "))
            except StopIteration:
                try:
                    # Some padding; randomly chose 4 to make sure we don't get a random
                    # version number from a package that's not Django
                    dj_version = get_first_digit(issue.body.split(" ", 4))
                except StopIteration:
                    print(
                        f"Found issue {issue.title} that had an invalid syntax",
                        "(Did not have a Django version number in the title or body's"
                        f" first word. Issue number: [{issue.id}]({issue.url}))"
                    )
                    continue
            if self.base_dj_version > dj_version:
                issue.edit(state="closed")
                print(f"Closed issue {issue.title} (ID: [{issue.id}]({issue.url}))")
                try:
                    self.needed_dj_versions.remove(dj_version)
                except ValueError:
                    print("Something weird happened. Continuing anyway (Warning ID: 1)")
            else:
                self.existing_issues[dj_version] = issue

    def get_compatibility(
        self, package_name: str, package_info: dict, needed_dj_version
    ):
        """
        Verify compatibility via setup.py classifiers. If Django is not in the
        classifiers, then default compatibility is n/a and OK is ✅.

        If it's a package that's vital but known to not be updated often, we give it
        a ❓. If a package has ❓ or 🕒, then we allow manual update. Automatic updates
         only include ❌ and ✅.
        """
        # If issue previously existed, find package and skip any gtg, manually
        # updated packages, or known releases that will happen but haven't yet
        if issue := self.existing_issues.get(needed_dj_version):
            if index := issue.body.find(package_name):
                name, _current, prev_compat, ok = issue.body[index:].split("|", 4)[:4]
                if ok in ("✅", "❓", "🕒"):
                    return prev_compat, ok

        if package_name in VITAL_BUT_UNKNOWN:
            return "", "❓"

        # Check classifiers if it includes Django
        supported_dj_versions = []
        for classifier in package_info["info"]["classifiers"]:
            # Usually in the form of "Framework :: Django :: 3.2"
            tokens = classifier.split(" ")
            for token in tokens:
                if token.lower() == "django":
                    try:
                        _version = get_first_digit(reversed(tokens))
                    except StopIteration:
                        pass
                    else:
                        supported_dj_versions.append(
                            float(".".join(_version.split(".", 2)[:2]))
                        )

        if supported_dj_versions:
            needed_dj_version = float(needed_dj_version)
            if any(x >= needed_dj_version for x in supported_dj_versions):
                return package_info["info"]["version"], "✅"
            else:
                return "", "❌"

        # Django classifier DNE; assume it just isn't a Django lib
        # Great exceptions include pylint-django, where we need to do this manually...
        return "n/a", "✅"

    HOME_PAGE_URL_KEYS = [
        "home_page",
        "project_url",
        "docs_url",
        "package_url",
        "release_url",
        "bugtrack_url",
    ]

    def _get_md_home_page_url(self, package_info: dict):
        urls = [package_info["info"].get(x) for x in self.HOME_PAGE_URL_KEYS]
        try:
            return f"[{{}}]({next(item for item in urls if item)})"
        except StopIteration:
            return "{}"

    def generate_markdown(self, needed_dj_version: str):
        requirements = f"{needed_dj_version} requirements tables\n\n"
        for _file in self.requirements_files:
            requirements += (
                _TABLE_HEADER.format_map(
                    {"file": _file, "dj_version": needed_dj_version}
                )
            )
            for package_name, (version, info) in self.requirements[_file].items():
                compat_version, icon = self.get_compatibility(
                    package_name, info, needed_dj_version
                )
                requirements += (
                    f"|{self._get_md_home_page_url(info).format(package_name)}"
                    f"|{version}|{compat_version}|{icon}|\n"
                )
        return requirements

    def create_or_edit_issue(self, needed_dj_version, description):
        if issue := self.existing_issues.get(str(needed_dj_version)):
            issue.edit(body=description)
        else:
            self.repo.create_issue(
                f"[Update Django] Django {needed_dj_version}", description
            )

    def generate(self):
        for version in self.needed_dj_versions:
            md_content = self.generate_markdown(version)
            self.create_or_edit_issue(version, md_content)


def main() -> None:
    # Check if there are any djs
    current_dj, latest_djs = get_all_latest_django_versions()
    if not latest_djs:
        sys.exit(0)
    manager = GitHubManager(current_dj, latest_djs)
    manager.setup()
    manager.generate()


if __name__ == "__main__":
    main()
