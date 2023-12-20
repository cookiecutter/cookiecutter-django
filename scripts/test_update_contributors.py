from pathlib import Path

from .update_contributors import CitationCFFFile, ContributorsJSONFile


def test_CitationCFFFile(tmp_path):
    """Test the CitationCFFFile class."""
    contrib_file = ContributorsJSONFile()
    citation_output_path = Path(tmp_path / "CITATION.cff")
    cff_writer = CitationCFFFile(output_path=citation_output_path)

    cff_writer.save_cff(contrib_file.content)

    # Verify
    assert citation_output_path.exists()
