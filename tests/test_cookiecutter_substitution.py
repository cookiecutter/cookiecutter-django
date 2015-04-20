import re

import sh

from .base import DjangoCookieTestCase


class TestCookiecutterSubstitution(DjangoCookieTestCase):
    """Test that all cookiecutter instances are substituted"""

    def test_all_cookiecutter_instances_are_substituted(self):
        # Build a list containing absolute paths to the generated files
        paths = self.generate_project()

        # Construct the cookiecutter search pattern
        pattern = "{{(\s?cookiecutter)[.](.*?)}}"
        re_obj = re.compile(pattern)

        # Assert that no match is found in any of the files
        for path in paths:
            for line in open(path, 'r'):
                match = re_obj.search(line)
                self.assertIsNone(
                    match,
                    "cookiecutter variable not replaced in {}".format(path))

    def test_flake8_complaince(self):
        """generated project should pass flake8"""
        self.generate_project()
        try:
            sh.flake8(self.destpath)
        except sh.ErrorReturnCode as e:
            raise AssertionError(e)
