"""Tests for bug fixes in hooks."""

import os
import sys
from pathlib import Path
from typing import NamedTuple

import pytest

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))


class TestBug1JinjaVariableSpacing:
    """Bug 1: Jinja template variable name spacing errors.

    Some Jinja variables had inconsistent spacing like:
    - "{{ cookiecutter.open_source_license}}" (missing space before }})
    - "{{ cookiecutter.cloud_provider}}" (missing space before }})

    They should be:
    - "{{ cookiecutter.open_source_license }}"
    - "{{ cookiecutter.cloud_provider }}"
    """

    def test_specific_jinja_spacing_bugs_fixed(self):
        """Test that specific known spacing bugs are fixed."""
        post_gen_path = Path(__file__).parent.parent / "hooks" / "post_gen_project.py"
        content = post_gen_path.read_text()

        # These specific patterns should NOT exist (missing space before }})
        bad_patterns = [
            '"{{ cookiecutter.open_source_license}}"',
            '"{{ cookiecutter.cloud_provider}}"',
        ]

        for pattern in bad_patterns:
            assert pattern not in content, f"Found bad Jinja spacing pattern: {pattern}"


class TestBug2NamedTupleLen:
    """Bug 2: NamedTuple len() usage should use _fields for clarity.

    In scripts/create_django_issue.py line 222:
    if len(version) == 2:

    While len() works on NamedTuple in Python 3, using len(version._fields)
    is more explicit and clearer about intent. It also works consistently
    across all Python versions.
    """

    def test_namedtuple_fields_is_preferred(self):
        """Test that using _fields is the preferred approach for clarity."""

        class TestVersion(NamedTuple):
            major: int
            minor: int

        version = TestVersion(major=4, minor=2)

        # Both work in Python 3, but _fields is more explicit
        assert len(version) == 2
        assert len(version._fields) == 2

    def test_fix_uses_fields_not_len(self):
        """Test that the fix uses version._fields instead of version."""
        script_path = Path(__file__).parent.parent / "scripts" / "create_django_issue.py"
        content = script_path.read_text(encoding="utf-8")

        # Should use len(version._fields) not len(version)
        assert "len(version._fields)" in content, "Should use len(version._fields) for clarity"


class TestBug3FileExistenceCheck:
    """Bug 3: Missing existence check before file/directory deletion.

    Functions like remove_open_source_files(), remove_gplv3_files(), etc.
    called unlink() or rmtree() without checking if files/directories exist first.
    """

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for testing."""
        prev_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            yield tmp_path
        finally:
            os.chdir(prev_cwd)

    def test_remove_open_source_files_no_error_when_missing(self, temp_dir):
        """Test that removing non-existent files doesn't raise error after fix."""
        from hooks.post_gen_project import remove_open_source_files

        # Files don't exist, but should NOT raise FileNotFoundError after fix
        remove_open_source_files()  # Should complete without error

    def test_remove_gplv3_files_no_error_when_missing(self, temp_dir):
        """Test that removing non-existent COPYING file doesn't raise error after fix."""
        from hooks.post_gen_project import remove_gplv3_files

        # COPYING file doesn't exist, but should NOT raise FileNotFoundError after fix
        remove_gplv3_files()  # Should complete without error

    def test_remove_custom_user_manager_files_no_error_when_missing(self, temp_dir):
        """Test that removing non-existent manager files doesn't raise error after fix."""
        from hooks.post_gen_project import remove_custom_user_manager_files

        # Create the directory structure but not the files
        users_path = Path("{{cookiecutter.project_slug}}", "users")
        users_path.mkdir(parents=True)
        (users_path / "tests").mkdir()

        # Files don't exist, but should NOT raise FileNotFoundError after fix
        remove_custom_user_manager_files()  # Should complete without error


class TestBug4CaseComparison:
    """Bug 4: Inconsistent case comparison.

    Line 523: if "{{ cookiecutter.use_docker }}".lower() == "y" and "{{ cookiecutter.cloud_provider }}" != "AWS":

    The cloud_provider comparison didn't use .lower() but compared with "AWS" (uppercase).
    This was inconsistent with other comparisons that use .lower().
    """

    def test_cloud_provider_case_comparison_fixed(self):
        """Test that cloud_provider comparison is now case-consistent."""
        post_gen_path = Path(__file__).parent.parent / "hooks" / "post_gen_project.py"
        content = post_gen_path.read_text()

        # Find the line comparing cloud_provider with AWS
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if "cloud_provider" in line and "!=" in line and "aws" in line.lower():
                # This comparison should now use .lower()
                assert ".lower()" in line, f"Line {i} should use .lower() for case consistency: {line.strip()}"


class TestBug5DeadCode:
    """Bug 5: Dead code - condition branch that never executes.

    Lines 304-305 in post_gen_project.py (before fix):
    if not using_sysrandom:
        return None

    using_sysrandom was set to True at module import time on modern systems.
    So 'if not using_sysrandom' would never be True on modern systems.

    This dead code has been removed.
    """

    def test_using_sysrandom_removed(self):
        """Test that using_sysrandom variable has been removed."""
        post_gen_path = Path(__file__).parent.parent / "hooks" / "post_gen_project.py"
        content = post_gen_path.read_text(encoding="utf-8")

        # using_sysrandom should no longer exist in the file
        assert "using_sysrandom" not in content, "using_sysrandom should be removed"

    def test_no_dead_code_check(self):
        """Test that the dead code check 'if not using_sysrandom' is removed."""
        post_gen_path = Path(__file__).parent.parent / "hooks" / "post_gen_project.py"
        content = post_gen_path.read_text(encoding="utf-8")

        # The dead code check should no longer exist
        assert "if not using_sysrandom" not in content, "Dead code check should be removed"


class TestBug6BroadException:
    """Bug 6: Overly broad exception catching.

    Line 654: except Exception as e:

    This caught all exceptions, which could mask unexpected errors.
    Should catch specific exceptions like OSError instead.
    """

    def test_no_bare_except_exception(self):
        """Test that no bare 'except Exception' is used (except for noqa lines)."""
        post_gen_path = Path(__file__).parent.parent / "hooks" / "post_gen_project.py"
        content = post_gen_path.read_text()

        # Check for bare 'except Exception' pattern (excluding noqa lines)
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if "except Exception" in line and "noqa" not in line:
                pytest.fail(f"Line {i} uses overly broad 'except Exception': {line.strip()}")

    def test_specific_oserror_used_for_shutil_rmtree(self):
        """Test that OSError is used for shutil.rmtree error handling."""
        post_gen_path = Path(__file__).parent.parent / "hooks" / "post_gen_project.py"
        content = post_gen_path.read_text()

        # After fix, should use OSError instead of Exception
        assert "except OSError as e:" in content, "Should use 'except OSError as e:' for shutil.rmtree"
