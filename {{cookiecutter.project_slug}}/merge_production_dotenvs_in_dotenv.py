import os
from collections.abc import Sequence
from pathlib import Path

import pytest

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


@pytest.mark.parametrize("files_count", range(3))
@pytest.mark.parametrize("append_linesep", [True, False])
def test_merge(tmp_path: Path, files_count: int, append_linesep: bool):
    output_file = tmp_path / ".env"

    expected_output_file_content = ""
    files_to_merge = []
    for num in range(1, files_count + 1):
        merge_filename = f".service{num}"
        merge_file = tmp_path / merge_filename

        merge_file_content = merge_filename * num
        merge_file.write_text(merge_file_content)

        expected_output_file_content += merge_file_content
        if append_linesep:
            expected_output_file_content += os.linesep

        files_to_merge.append(merge_file)

    merge(output_file, files_to_merge, append_linesep)

    actual_output_file_content = output_file.read_text()
    assert actual_output_file_content == expected_output_file_content


if __name__ == "__main__":
    main()
