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


@pytest.mark.parametrize(
    ("input_contents", "append_linesep", "expected_output"),
    [
        # No line separator
        ([], False, ""),
        ([""], False, ""),
        (["\n"], False, "\n"),
        (["TEST=1"], False, "TEST=1"),
        (["THIS=2", "THAT='example'"], False, "THIS=2THAT='example'"),
        (["ONE=1\n", "TWO=2"], False, "ONE=1\nTWO=2"),
        (["A=0", "B=1", "C=2"], False, "A=0B=1C=2"),
        # With line separator
        (
            [],
            True,
            "",
        ),
        (
            [""],
            True,
            "\n",
        ),
        (
            ["JANE=doe"],
            True,
            "JANE=doe\n",
        ),
        (["SEP=true", "AR=ator"], True, "SEP=true\nAR=ator\n"),
        (["X=x\n", "Y=y", "Z=z\n"], True, "X=x\n\nY=y\nZ=z\n\n"),
    ],
)
def test_merge(
    tmp_path: Path,
    input_contents: list[str],
    append_linesep: bool,
    expected_output: str,
):
    output_file = tmp_path / ".env"

    files_to_merge = []
    for num, input_content in enumerate(input_contents, start=1):
        merge_file = tmp_path / f".service{num}"
        merge_file.write_text(input_content)
        files_to_merge.append(merge_file)

    merge(output_file, files_to_merge, append_linesep)

    assert output_file.read_text() == expected_output


if __name__ == "__main__":
    main()
