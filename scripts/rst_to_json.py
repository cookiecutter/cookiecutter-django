import json
from pathlib import Path

CURRENT_FILE = Path(__file__)
ROOT = CURRENT_FILE.parents[1]


def main():
    input_file_path = ROOT / "CONTRIBUTORS.rst"
    content = input_file_path.read_text()

    table_separator = (
        "========================== ============================ =============="
    )
    table_content = content.split(table_separator)[2]

    profiles_list = [
        {
            "name": "Daniel Roy Greenfeld",
            "github_login": "pydanny",
            "twitter_username": "pydanny",
            "is_core": True,
        },
        {
            "name": "Audrey Roy Greenfeld",
            "github_login": "audreyr",
            "twitter_username": "audreyr",
            "is_core": True,
        },
        {
            "name": "Fábio C. Barrionuevo da Luz",
            "github_login": "luzfcb",
            "twitter_username": "luzfcb",
            "is_core": True,
        },
        {
            "name": "Saurabh Kumar",
            "github_login": "theskumar",
            "twitter_username": "_theskumar",
            "is_core": True,
        },
        {
            "name": "Jannis Gebauer",
            "github_login": "jayfk",
            "twitter_username": "",
            "is_core": True,
        },
        {
            "name": "Burhan Khalid",
            "github_login": "burhan",
            "twitter_username": "burhan",
            "is_core": True,
        },
        {
            "name": "Shupeyko Nikita",
            "github_login": "webyneter",
            "twitter_username": "webyneter",
            "is_core": True,
        },
        {
            "name": "Bruno Alla",
            "github_login": "browniebroke",
            "twitter_username": "_BrunoAlla",
            "is_core": True,
        },
        {
            "name": "Wan Liuyang",
            "github_login": "sfdye",
            "twitter_username": "sfdye",
            "is_core": True,
        },
    ]
    core_members = [member["github_login"] for member in profiles_list]

    for contrib in table_content.split("\n"):
        if not contrib:
            continue
        line_parts = contrib.split("`")
        name = line_parts[0].strip()
        github_login = line_parts[1].lstrip("@") if len(line_parts) > 1 else ""
        if github_login in core_members:
            continue
        twitter_username = (
            line_parts[2].lstrip("_").strip().lstrip("@")
            if len(line_parts) == 3
            else ""
        )
        profile = {
            "name": name,
            "github_login": github_login,
            "twitter_username": twitter_username,
        }
        profiles_list.append(profile)

    output_file_path = ROOT / ".github" / "contributors.json"
    output_file_path.write_text(
        json.dumps(profiles_list, indent=2, ensure_ascii=False)
    )



if __name__ == "__main__":
    main()
