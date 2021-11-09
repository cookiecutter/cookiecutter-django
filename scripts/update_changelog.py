import os
from pathlib import Path
from github import Github
from jinja2 import Template
import datetime as dt

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)

# Generate changelog for PRs merged yesterday
MERGED_DATE = dt.date.today() - dt.timedelta(days=1)


def main() -> None:
    """
    Script entry point.
    """
    merged_pulls = list(iter_pulls())
    if not merged_pulls:
        print("Nothing was merged, existing.")
        return

    # Group pull requests by type of change
    grouped_pulls = group_pulls_by_change_type(merged_pulls)

    # Generate portion of markdown
    rendered_content = generate_md(grouped_pulls)

    # Update CHANGELOG.md file
    file_path = ROOT / "CHANGELOG.md"
    old_content = file_path.read_text()
    updated_content = old_content.replace(
        "<!-- GENERATOR_PLACEHOLDER -->",
        f"<!-- GENERATOR_PLACEHOLDER -->\n\n{rendered_content}",
    )
    file_path.write_text(updated_content)


def iter_pulls():
    """Fetch merged pull requests at the date we're interested in."""
    repo = Github(login_or_token=GITHUB_TOKEN).get_repo(
        "cookiecutter/cookiecutter-django"
    )
    recent_pulls = repo.get_pulls(
        state="closed", sort="updated", direction="desc"
    ).get_page(0)
    for pull in recent_pulls:
        if pull.merged and pull.merged_at.date() == MERGED_DATE:
            yield pull


def group_pulls_by_change_type(pull_requests_list):
    """Group pull request by change type."""
    grouped_pulls = {
        "Changed": [],
        "Fixed": [],
        "Updated": [],
    }
    for pull in pull_requests_list:
        label_names = {l.name for l in pull.labels}
        if "update" in label_names:
            group_name = "Updated"
        elif "bug" in label_names:
            group_name = "Fixed"
        else:
            group_name = "Changed"
        grouped_pulls[group_name].append(pull)
    return grouped_pulls


def generate_md(grouped_pulls):
    """Generate markdown file from Jinja template."""
    changelog_template = ROOT / ".github" / "changelog-template.md"
    template = Template(changelog_template.read_text(), autoescape=True)
    return template.render(merge_date=MERGED_DATE, grouped_pulls=grouped_pulls)


if __name__ == "__main__":
    main()
