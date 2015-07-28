import re

import sh

from .base import DjangoCookieTestCase


class TestCookiecutterSubstitution(DjangoCookieTestCase):
    """Test that all cookiecutter instances are substituted"""

    def test_all_cookiecutter_instances_are_substituted(self):
        # Build a list containing absolute paths to the generated files
        paths = self.generate_project()
        self.check_paths(paths)

    def test_flake8_complaince(self):
        """generated project should pass flake8"""
        self.generate_project()
        try:
            sh.flake8(self.destpath)
        except sh.ErrorReturnCode as e:
            raise AssertionError(e)
