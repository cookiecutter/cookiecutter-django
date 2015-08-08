from __future__ import absolute_import
import sh

from .base import DjangoCookieTestCase


class TestCookiecutterSubstitution(DjangoCookieTestCase):
    """Test that all cookiecutter instances are substituted"""

    def test_default_configuration(self):
        # Build a list containing absolute paths to the generated files
        paths = self.generate_project()
        self.check_paths(paths)

    def test_maildump_enabled(self):
        paths = self.generate_project(extra_context={'use_maildump': 'y'})
        self.check_paths(paths)

    def test_celery_enabled(self):
        paths = self.generate_project(extra_context={'use_celery': 'y'})
        self.check_paths(paths)

    def test_windows_enabled(self):
        paths = self.generate_project(extra_context={'windows': 'y'})
        self.check_paths(paths)

    def test_flake8_compliance(self):
        """generated project should pass flake8"""
        self.generate_project()
        try:
            sh.flake8(self.destpath)
        except sh.ErrorReturnCode as e:
            raise AssertionError(e)
