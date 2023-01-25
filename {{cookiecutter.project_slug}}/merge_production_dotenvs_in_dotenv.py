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
    merged_files: Sequence[Path],
    append_linesep: bool = True,
) -> None:
    merged_content = ""
    for merged_file_path in merged_files:
        merged_content += merged_file_path.read_text()
        if append_linesep:
            merged_content += os.linesep
    output_file.write_text(merged_content)


def main():
    merge(DOTENV_FILE, PRODUCTION_DOTENV_FILES)


@pytest.mark.parametrize("merged_file_count", range(3))
@pytest.mark.parametrize("append_linesep", [True, False])
def test_merge(tmpdir_factory, merged_file_count: int, append_linesep: bool):
    tmp_dir = Path(str(tmpdir_factory.getbasetemp()))

    output_file = tmp_dir / ".env"

    expected_output_file_content = ""
    merged_files = []
    for i in range(merged_file_count):
        merged_file_ord = i + 1

        merged_filename = f".service{merged_file_ord}"
        merged_file = tmp_dir / merged_filename

        merged_file_content = merged_filename * merged_file_ord

        with open(merged_file, "w+") as file:
            file.write(merged_file_content)

        expected_output_file_content += merged_file_content
        if append_linesep:
            expected_output_file_content += os.linesep

        merged_files.append(merged_file)

    merge(output_file, merged_files, append_linesep)

    with open(output_file) as output_file:
        actual_output_file_content = output_file.read()

    assert actual_output_file_content == expected_output_file_content


if __name__ == "__main__":
    main()
