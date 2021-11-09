"""
Creates an issue that generates a table for dependency checking whether
all packages support the latest Django version. "Latest" does not include
patches, only comparing major and minor version numbers.

This script handles when there are multiple Django versions that need
to keep up to date.
"""
from __future__ import annotations

import os
from typing import NamedTuple, Sequence, TYPE_CHECKING

import requests
import sys
from pathlib import Path

from github import Github


if TYPE_CHECKING:
    from github.Issue import Issue

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
REQUIREMENTS_DIR = ROOT / "{{cookiecutter.project_slug}}" / "requirements"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY", None)
ISSUE_AUTHOR = os.getenv("GITHUB_ISSUE_AUTHOR", "actions-user")


class Version(NamedTuple):
    major: str
    minor: str

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    @classmethod
    def parse(cls, version_str: str) -> Version:
        major, minor, *_ = version_str.split(".")
        return cls(major=major, minor=minor)


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
        releases = [r for r in releases if r.replace(".", "").isdigit()]
    return sorted(releases, reverse=reverse)


def get_name_and_version(requirements_line: str) -> tuple[str, ...]:
    full_name, version = requirements_line.split(" ", 1)[0].split("==")
    name_without_extras = full_name.split("[", 1)[0]
    return name_without_extras, version


def get_all_latest_django_versions() -> tuple[Version, list[Version]]:
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
    current_minor_version = Version.parse(current_version_str)
    all_django_versions = get_package_versions(get_package_info("django"))
    newer_versions: set[Version] = set()
    for version_str in all_django_versions:
        released_minor_version = Version.parse(version_str)
        if released_minor_version > current_minor_version:
            newer_versions.add(released_minor_version)

    return current_minor_version, sorted(newer_versions, reverse=True)


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
    def __init__(self, base_dj_version: Version, needed_dj_versions: list[Version]):
        self.github = Github(GITHUB_TOKEN)
        self.repo = self.github.get_repo(GITHUB_REPO)

        self.base_dj_version = base_dj_version
        self.needed_dj_versions = needed_dj_versions
        # (major+minor) Version and description
        self.existing_issues: dict[Version, Issue] = {}

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
                    if "==" in line and not line.startswith("{%"):
                        name, version = get_name_and_version(line)
                        self.requirements[requirements_file][name] = (
                            version,
                            get_package_info(name),
                        )

    def load_existing_issues(self):
        """Closes the issue if the base Django version is greater than the needed"""
        qualifiers = {
            "repo": GITHUB_REPO,
            "author": ISSUE_AUTHOR,
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
            issue_version_str = issue.title.split(" ")[-1]
            issue_version = Version.parse(issue_version_str)
            if self.base_dj_version > issue_version:
                issue.edit(state="closed")
                print(f"Closed issue {issue.title} (ID: [{issue.id}]({issue.url}))")
            else:
                self.existing_issues[issue_version] = issue

    def get_compatibility(
        self, package_name: str, package_info: dict, needed_dj_version: Version
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
        supported_dj_versions: list[Version] = []
        for classifier in package_info["info"]["classifiers"]:
            # Usually in the form of "Framework :: Django :: 3.2"
            tokens = classifier.split(" ")
            if len(tokens) >= 5 and tokens[2].lower() == "django":
                version = Version.parse(tokens[4])
                if len(version) == 2:
                    supported_dj_versions.append(version)

        if supported_dj_versions:
            if any(v >= needed_dj_version for v in supported_dj_versions):
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
        urls = [
            package_info["info"].get(url_key) for url_key in self.HOME_PAGE_URL_KEYS
        ]
        try:
            return f"[{{}}]({next(item for item in urls if item)})"
        except StopIteration:
            return "{}"

    def generate_markdown(self, needed_dj_version: Version):
        requirements = f"{needed_dj_version} requirements tables\n\n"
        for _file in self.requirements_files:
            requirements += _TABLE_HEADER.format_map(
                {"file": _file, "dj_version": needed_dj_version}
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

    def create_or_edit_issue(self, needed_dj_version: Version, description: str):
        if issue := self.existing_issues.get(needed_dj_version):
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
    if GITHUB_REPO is None:
        raise RuntimeError(
            "No github repo, please set the environment variable GITHUB_REPOSITORY"
        )
    main()
