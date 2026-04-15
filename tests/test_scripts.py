"""Unit tests for the scripts"""

import ast
from pathlib import Path


class TestBug2NamedTupleLen:
    """Test cases for Bug 2: NamedTuple doesn't support len() operation"""

    def test_dj_version_no_len_check(self):
        """Verify DjVersion code doesn't use len() on the NamedTuple"""
        script_path = Path(__file__).parent.parent / "scripts" / "create_django_issue.py"
        source = script_path.read_text(encoding="utf-8")

        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "len":
                    for arg in node.args:
                        if isinstance(arg, ast.Name) and arg.id == "version":
                            raise AssertionError("len(version) found - NamedTuple doesn't support len()")

    def test_dj_version_class_definition(self):
        """Verify DjVersion is properly defined as NamedTuple"""
        script_path = Path(__file__).parent.parent / "scripts" / "create_django_issue.py"
        source = script_path.read_text(encoding="utf-8")

        assert "class DjVersion(NamedTuple):" in source
        assert "major: int" in source
        assert "minor: int" in source
