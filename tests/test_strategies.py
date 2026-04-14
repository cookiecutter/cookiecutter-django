"""Tests for the strategies module."""

from pathlib import Path

import pytest

from hooks.core.actions import DeleteDirectoryAction, DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.strategies.async_strategy import AsyncStrategy
from hooks.strategies.celery import CeleryStrategy
from hooks.strategies.ci_tool import CIToolStrategy
from hooks.strategies.docker import DockerStrategy
from hooks.strategies.editor import EditorStrategy
from hooks.strategies.frontend_pipeline import FrontendPipelineStrategy
from hooks.strategies.heroku import HerokuStrategy
from hooks.strategies.license import OpenSourceLicenseStrategy
from hooks.strategies.rest_api import RestApiStrategy
from hooks.strategies.username_type import UsernameTypeStrategy


def get_path_from_action(action):
    if isinstance(action, DeleteFileAction):
        return str(action.file_path)
    elif isinstance(action, DeleteDirectoryAction):
        return str(action.dir_path)
    return ""


class TestOpenSourceLicenseStrategy:
    def test_should_apply_not_open_source(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"open_source_license": "Not open source"},
        )
        strategy = OpenSourceLicenseStrategy()

        assert strategy.should_apply(context)

    def test_should_apply_gplv3(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"open_source_license": "MIT"},
        )
        strategy = OpenSourceLicenseStrategy()

        assert strategy.should_apply(context)

    def test_plan_not_open_source(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"open_source_license": "Not open source"},
        )
        strategy = OpenSourceLicenseStrategy()
        actions = strategy.plan(context)

        assert len(actions) == 3
        paths = [get_path_from_action(a) for a in actions]
        assert any("CONTRIBUTORS.txt" in p for p in paths)
        assert any("LICENSE" in p for p in paths)
        assert any("COPYING" in p for p in paths)


class TestUsernameTypeStrategy:
    def test_should_apply_username_mode(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"username_type": "username"},
        )
        strategy = UsernameTypeStrategy()

        assert strategy.should_apply(context)

    def test_should_not_apply_email_mode(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"username_type": "email"},
        )
        strategy = UsernameTypeStrategy()

        assert not strategy.should_apply(context)

    def test_plan_username_mode(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"username_type": "username"},
        )
        strategy = UsernameTypeStrategy()
        actions = strategy.plan(context)

        assert len(actions) == 2
        paths = [get_path_from_action(a) for a in actions]
        assert any("managers.py" in p for p in paths)


class TestEditorStrategy:
    def test_should_apply_non_pycharm(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"editor": "VS Code"},
        )
        strategy = EditorStrategy()

        assert strategy.should_apply(context)

    def test_should_not_apply_pycharm(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"editor": "PyCharm"},
        )
        strategy = EditorStrategy()

        assert not strategy.should_apply(context)


class TestDockerStrategy:
    def test_should_apply_always(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={},
        )
        strategy = DockerStrategy()

        assert strategy.should_apply(context)

    def test_plan_docker_enabled(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_docker": "y", "cloud_provider": "None"},
        )
        strategy = DockerStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("utility" in p for p in paths)

    def test_plan_docker_disabled(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_docker": "n"},
        )
        strategy = DockerStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("compose" in p for p in paths)
        assert any("docker-compose" in p for p in paths)


class TestHerokuStrategy:
    def test_should_apply_always(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={},
        )
        strategy = HerokuStrategy()

        assert strategy.should_apply(context)

    def test_plan_heroku_disabled(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_heroku": "n", "ci_tool": "None"},
        )
        strategy = HerokuStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("Procfile" in p for p in paths)
        assert any("bin" in p for p in paths)


class TestFrontendPipelineStrategy:
    def test_should_apply_always(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={},
        )
        strategy = FrontendPipelineStrategy()

        assert strategy.should_apply(context)

    def test_plan_no_frontend(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"frontend_pipeline": "None", "use_docker": "n"},
        )
        strategy = FrontendPipelineStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("package.json" in p for p in paths)

    def test_plan_gulp(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"frontend_pipeline": "Gulp", "use_docker": "n", "use_async": "n"},
        )
        strategy = FrontendPipelineStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("webpack" in p for p in paths)

    def test_plan_webpack(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"frontend_pipeline": "Webpack", "use_docker": "n", "use_async": "n"},
        )
        strategy = FrontendPipelineStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("gulpfile" in p for p in paths)


class TestCeleryStrategy:
    def test_should_apply_celery_disabled(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"use_celery": "n"},
        )
        strategy = CeleryStrategy()

        assert strategy.should_apply(context)

    def test_should_not_apply_celery_enabled(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"use_celery": "y"},
        )
        strategy = CeleryStrategy()

        assert not strategy.should_apply(context)

    def test_plan_celery_disabled(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"use_celery": "n", "use_docker": "n"},
        )
        strategy = CeleryStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("celery_app.py" in p for p in paths)


class TestCIToolStrategy:
    def test_should_apply_always(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={},
        )
        strategy = CIToolStrategy()

        assert strategy.should_apply(context)

    def test_plan_github_ci(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"ci_tool": "Github"},
        )
        strategy = CIToolStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert not any(".github" in p for p in paths)
        assert any(".travis.yml" in p for p in paths)

    def test_plan_no_ci(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"ci_tool": "None"},
        )
        strategy = CIToolStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any(".github" in p for p in paths)
        assert any(".travis.yml" in p for p in paths)


class TestRestApiStrategy:
    def test_should_apply_always(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={},
        )
        strategy = RestApiStrategy()

        assert strategy.should_apply(context)

    def test_plan_drf(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"rest_api": "DRF"},
        )
        strategy = RestApiStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("schema.py" in p for p in paths)

    def test_plan_ninja(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"rest_api": "Django Ninja"},
        )
        strategy = RestApiStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("serializers.py" in p for p in paths)

    def test_plan_no_api(self):
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config={"rest_api": "None"},
        )
        strategy = RestApiStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("api" in p for p in paths)


class TestAsyncStrategy:
    def test_should_apply_async_disabled(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_async": "n"},
        )
        strategy = AsyncStrategy()

        assert strategy.should_apply(context)

    def test_should_not_apply_async_enabled(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_async": "y"},
        )
        strategy = AsyncStrategy()

        assert not strategy.should_apply(context)

    def test_plan_async_disabled(self):
        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_async": "n"},
        )
        strategy = AsyncStrategy()
        actions = strategy.plan(context)

        paths = [get_path_from_action(a) for a in actions]
        assert any("asgi.py" in p for p in paths)
        assert any("websocket.py" in p for p in paths)
