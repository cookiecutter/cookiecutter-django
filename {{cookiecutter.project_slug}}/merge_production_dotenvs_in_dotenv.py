import os
from collections.abc import Sequence
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
PRODUCTION_DOTENVS_DIR = BASE_DIR / ".envs" / ".production"
PRODUCTION_DOTENV_FILES = [
    PRODUCTION_DOTENVS_DIR / ".django",
    PRODUCTION_DOTENVS_DIR / ".postgres",
]
DOTENV_FILE = BASE_DIR / ".env"


def merge(
    output_file: Path,
    files_to_merge: Sequence[Path],
    append_linesep: bool = True,
) -> None:
    merged_content = ""
    for merge_file in files_to_merge:
        merged_content += merge_file.read_text()
        if append_linesep:
            merged_content += os.linesep
    output_file.write_text(merged_content)


def main():
    merge(DOTENV_FILE, PRODUCTION_DOTENV_FILES)


if __name__ == "__main__":
    main()
