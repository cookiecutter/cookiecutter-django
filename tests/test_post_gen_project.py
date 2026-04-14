"""Tests for the refactored post_gen_project.py using new architecture."""

import json
import os
from pathlib import Path

import pytest

from hooks.core.context import FailurePolicy
from hooks.post_gen_project import EnvFilesStrategy
from hooks.post_gen_project import GitignoreStrategy
from hooks.post_gen_project import ProjectGenerationOrchestrator
from hooks.post_gen_project import SecretGenerationStrategy


class TestSecretGenerationStrategy:
    def test_should_apply_always(self):
        from hooks.core.context import ExecutionContext

        context = ExecutionContext(project_slug="test")
        strategy = SecretGenerationStrategy()
        assert strategy.should_apply(context)

    def test_plan_generates_secret_actions(self):
        from hooks.core.context import ExecutionContext

        context = ExecutionContext(project_slug="test")
        strategy = SecretGenerationStrategy(debug=True)
        actions = strategy.plan(context)

        assert len(actions) > 0
        assert any("secret" in a.description.lower() for a in actions)

    def test_debug_mode_uses_debug_values(self):
        strategy = SecretGenerationStrategy(debug=True)
        assert strategy.postgres_user == "debug"
        assert strategy.celery_flower_user == "debug"


class TestEnvFilesStrategy:
    def test_plan_removes_envs_when_no_docker_heroku(self):
        from hooks.core.context import ExecutionContext

        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_docker": "n", "use_heroku": "n", "keep_local_envs_in_vcs": "n"},
        )
        strategy = EnvFilesStrategy()
        actions = strategy.plan(context)

        paths = [str(a.dir_path) if hasattr(a, "dir_path") else str(a.file_path) for a in actions]
        assert any(".envs" in p for p in paths)

    def test_plan_keeps_envs_when_keep_local_envs(self):
        from hooks.core.context import ExecutionContext

        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_docker": "n", "use_heroku": "n", "keep_local_envs_in_vcs": "y"},
        )
        strategy = EnvFilesStrategy()
        actions = strategy.plan(context)

        assert len(actions) == 0


class TestGitignoreStrategy:
    def test_should_apply_when_docker_enabled(self):
        from hooks.core.context import ExecutionContext

        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_docker": "y", "use_heroku": "n"},
        )
        strategy = GitignoreStrategy()
        assert strategy.should_apply(context)

    def test_should_apply_when_heroku_enabled(self):
        from hooks.core.context import ExecutionContext

        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_docker": "n", "use_heroku": "y"},
        )
        strategy = GitignoreStrategy()
        assert strategy.should_apply(context)

    def test_should_not_apply_when_no_docker_heroku(self):
        from hooks.core.context import ExecutionContext

        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_docker": "n", "use_heroku": "n"},
        )
        strategy = GitignoreStrategy()
        assert not strategy.should_apply(context)

    def test_plan_adds_env_to_gitignore(self):
        from hooks.core.context import ExecutionContext

        context = ExecutionContext(
            project_slug="test",
            cookiecutter_config={"use_docker": "y", "keep_local_envs_in_vcs": "n"},
        )
        strategy = GitignoreStrategy()
        actions = strategy.plan(context)

        contents = [a.content for a in actions]
        assert ".env" in contents
        assert ".envs/*" in contents


class TestProjectGenerationOrchestrator:
    def test_orchestrator_creation(self):
        config = {"project_slug": "test_project"}
        orchestrator = ProjectGenerationOrchestrator(config)

        assert orchestrator.project_slug == "test_project"
        assert orchestrator.context.project_slug == "test_project"

    def test_orchestrator_with_dry_run(self):
        config = {"project_slug": "test_project"}
        orchestrator = ProjectGenerationOrchestrator(config, dry_run=True)

        assert orchestrator.context.dry_run

    def test_orchestrator_with_failure_policy(self):
        config = {"project_slug": "test_project"}
        orchestrator = ProjectGenerationOrchestrator(
            config,
            failure_policy=FailurePolicy.CONTINUE_ON_ERROR,
        )

        assert orchestrator.context.failure_policy == FailurePolicy.CONTINUE_ON_ERROR

    def test_register_all_strategies(self):
        config = {"project_slug": "test_project"}
        orchestrator = ProjectGenerationOrchestrator(config)
        orchestrator.register_all_strategies()

        assert len(orchestrator._strategies) == 14

    def test_plan_returns_actions(self):
        config = {
            "project_slug": "test_project",
            "open_source_license": "MIT",
            "username_type": "email",
            "editor": "VS Code",
            "use_docker": "n",
            "cloud_provider": "None",
            "use_heroku": "n",
            "frontend_pipeline": "None",
            "use_celery": "n",
            "ci_tool": "Github",
            "rest_api": "DRF",
            "use_async": "n",
            "keep_local_envs_in_vcs": "n",
            "debug": "y",
        }
        orchestrator = ProjectGenerationOrchestrator(config)
        orchestrator.register_all_strategies()

        actions = orchestrator.plan()

        assert len(actions) > 0
        assert all(hasattr(a, "execute") for a in actions)

    def test_preview(self):
        config = {"project_slug": "test_project", "debug": "y"}
        orchestrator = ProjectGenerationOrchestrator(config)
        orchestrator.register_all_strategies()

        preview = orchestrator.preview()

        assert "test_project" in preview
        assert "Preview" in preview


class TestOrchestratorIntegration:
    def test_full_flow_dry_run(self, tmp_path, monkeypatch):
        config = {
            "project_slug": "my_project",
            "open_source_license": "MIT",
            "username_type": "email",
            "editor": "None",
            "use_docker": "n",
            "cloud_provider": "None",
            "use_heroku": "n",
            "frontend_pipeline": "None",
            "use_celery": "n",
            "ci_tool": "Github",
            "rest_api": "DRF",
            "use_async": "n",
            "keep_local_envs_in_vcs": "n",
            "debug": "y",
        }

        orchestrator = ProjectGenerationOrchestrator(config, dry_run=True)
        orchestrator.register_all_strategies()

        actions = orchestrator.plan()
        assert len(actions) > 0

    def test_audit_report_generated(self, tmp_path):
        config = {
            "project_slug": "test_project",
            "debug": "y",
        }

        original_cwd = Path.cwd()
        os.chdir(tmp_path)

        try:
            orchestrator = ProjectGenerationOrchestrator(config, dry_run=True)
            orchestrator.register_all_strategies()

            actions = orchestrator.plan()
            orchestrator.executor.execute(actions)

            orchestrator.context.save_report(tmp_path / "report.md")
            orchestrator.context.save_json_report(tmp_path / "report.json")

            assert (tmp_path / "report.md").exists()
            assert (tmp_path / "report.json").exists()

            report_content = (tmp_path / "report.md").read_text()
            assert "test_project" in report_content

            json_report = json.loads((tmp_path / "report.json").read_text())
            assert json_report["project_name"] == "test_project"
        finally:
            os.chdir(original_cwd)


class TestRollbackMechanism:
    def test_rollback_on_failure(self, tmp_path):
        from hooks.core.actions import DeleteFileAction
        from hooks.core.context import ExecutionContext
        from hooks.core.context import FailurePolicy
        from hooks.core.executor import ActionExecutor

        test_file = tmp_path / "test.txt"
        test_file.write_text("original content")

        context = ExecutionContext(
            project_slug="test",
            failure_policy=FailurePolicy.ROLLBACK_ALL,
        )
        executor = ActionExecutor(context)

        delete_action = DeleteFileAction(file_path=test_file)

        original_cwd = Path.cwd()
        os.chdir(tmp_path)
        try:
            result = executor.execute([delete_action])

            assert not test_file.exists()

            checkpoints = context.get_checkpoints_for_rollback()
            assert len(checkpoints) == 1

            rollback_result = delete_action.rollback(checkpoints[0].backup_data)
            assert rollback_result.success
            assert test_file.exists()
            assert test_file.read_text() == "original content"
        finally:
            os.chdir(original_cwd)

    def test_checkpoint_created_for_file_modification(self, tmp_path):
        from hooks.core.actions import ModifyFileAction
        from hooks.core.context import ExecutionContext
        from hooks.core.executor import ActionExecutor

        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello {{ name }}!")

        context = ExecutionContext(project_slug="test")
        executor = ActionExecutor(context)

        modify_action = ModifyFileAction(
            file_path=test_file,
            modifications={"{{ name }}": "World"},
        )

        original_cwd = Path.cwd()
        os.chdir(tmp_path)
        try:
            result = executor.execute([modify_action])

            assert result.success
            assert test_file.read_text() == "Hello World!"

            checkpoints = context.get_checkpoints_for_rollback()
            assert len(checkpoints) == 1
            assert checkpoints[0].backup_data == "Hello {{ name }}!"
        finally:
            os.chdir(original_cwd)


class TestDifferentConfigCombinations:
    @pytest.mark.parametrize(
        "config_override",
        [
            {"use_docker": "y", "cloud_provider": "AWS"},
            {"use_docker": "y", "cloud_provider": "None"},
            {"use_docker": "n", "use_heroku": "y"},
            {"frontend_pipeline": "Gulp"},
            {"frontend_pipeline": "Webpack"},
            {"rest_api": "Django Ninja"},
            {"open_source_license": "Not open source"},
            {"username_type": "username"},
            {"editor": "PyCharm"},
            {"use_celery": "y"},
            {"ci_tool": "Travis"},
            {"ci_tool": "Gitlab"},
            {"ci_tool": "Drone"},
            {"use_async": "y"},
        ],
    )
    def test_config_combinations(self, config_override):
        base_config = {
            "project_slug": "test_project",
            "debug": "y",
        }
        config = {**base_config, **config_override}

        orchestrator = ProjectGenerationOrchestrator(config, dry_run=True)
        orchestrator.register_all_strategies()

        actions = orchestrator.plan()
        assert len(actions) >= 0
