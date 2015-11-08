# -*- coding: utf-8 -*-

import pytest

@pytest.fixture
def context():
    return {
        "project_name": "My Test Project",
        "repo_name": "my_test_project",
        "author_name": "Test Author",
        "email": "test@example.com",
        "description": "A short description of the project.",
        "domain_name": "example.com",
        "version": "0.1.0",
        "timezone": "UTC",
        "now": "2015/01/13",
        "year": "2015"
    }


def test_default_configuration(cookies, context):
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
