"""Tests for the core context module."""

import json

from hooks.core.actions import DeleteFileAction
from hooks.core.context import Checkpoint
from hooks.core.context import ExecutionContext
from hooks.core.context import FailurePolicy


class TestExecutionContext:
    def test_context_creation(self):
        context = ExecutionContext(project_slug="test_project")

        assert context.project_slug == "test_project"
        assert context.failure_policy == FailurePolicy.STOP_IMMEDIATELY
        assert not context.dry_run

    def test_context_with_config(self):
        config = {"use_docker": "y", "use_celery": "n"}
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config=config,
        )

        assert context.get_config("use_docker") == "y"
        assert context.get_config("use_celery") == "n"
        assert context.get_config("missing", "default") == "default"

    def test_is_enabled(self):
        config = {"use_docker": "y", "use_celery": "n", "debug": "true"}
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config=config,
        )

        assert context.is_enabled("use_docker")
        assert not context.is_enabled("use_celery")
        assert context.is_enabled("debug")

    def test_equals(self):
        config = {"editor": "PyCharm", "cloud_provider": "AWS"}
        context = ExecutionContext(
            project_slug="test_project",
            cookiecutter_config=config,
        )

        assert context.equals("editor", "PyCharm")
        assert context.equals("editor", "pycharm")
        assert not context.equals("editor", "VS Code")

    def test_create_checkpoint(self, tmp_path):
        context = ExecutionContext(project_slug="test_project")
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        from hooks.core.audit import AuditEntry

        entry = AuditEntry(action=action, sequence_number=1)
        checkpoint = context.create_checkpoint(entry, b"backup_data")

        assert len(context.checkpoints) == 1
        assert checkpoint.sequence_number == 1
        assert checkpoint.backup_data == b"backup_data"

    def test_get_backup(self, tmp_path):
        context = ExecutionContext(project_slug="test_project")
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        from hooks.core.audit import AuditEntry

        entry = AuditEntry(action=action, sequence_number=1)
        context.create_checkpoint(entry, b"backup_data")

        backup = context.get_backup(1)
        assert backup == b"backup_data"

    def test_get_checkpoints_for_rollback(self, tmp_path):
        context = ExecutionContext(project_slug="test_project")
        from hooks.core.audit import AuditEntry

        action1 = DeleteFileAction(file_path=tmp_path / "test1.txt")
        entry1 = AuditEntry(action=action1, sequence_number=1)
        context.create_checkpoint(entry1, b"backup1")

        action2 = DeleteFileAction(file_path=tmp_path / "test2.txt")
        entry2 = AuditEntry(action=action2, sequence_number=2)
        context.create_checkpoint(entry2, None)

        action3 = DeleteFileAction(file_path=tmp_path / "test3.txt")
        entry3 = AuditEntry(action=action3, sequence_number=3)
        context.create_checkpoint(entry3, b"backup3")

        checkpoints = context.get_checkpoints_for_rollback()

        assert len(checkpoints) == 2
        assert checkpoints[0].sequence_number == 3
        assert checkpoints[1].sequence_number == 1

    def test_get_report(self, tmp_path):
        context = ExecutionContext(project_slug="test_project")

        report = context.get_report()

        assert "test_project" in report
        assert "Project Generation Report" in report

    def test_get_json_report(self, tmp_path):
        context = ExecutionContext(project_slug="test_project")

        report = context.get_json_report()

        assert report["project_name"] == "test_project"
        assert "summary" in report

    def test_save_report(self, tmp_path):
        context = ExecutionContext(project_slug="test_project")
        report_path = tmp_path / "report.md"

        context.save_report(report_path)

        assert report_path.exists()
        content = report_path.read_text()
        assert "test_project" in content

    def test_save_json_report(self, tmp_path):
        context = ExecutionContext(project_slug="test_project")
        report_path = tmp_path / "report.json"

        context.save_json_report(report_path)

        assert report_path.exists()
        content = json.loads(report_path.read_text())
        assert content["project_name"] == "test_project"


class TestFailurePolicy:
    def test_failure_policy_values(self):
        assert FailurePolicy.STOP_IMMEDIATELY.value == "stop_immediately"
        assert FailurePolicy.CONTINUE_ON_ERROR.value == "continue_on_error"
        assert FailurePolicy.ROLLBACK_ALL.value == "rollback_all"
        assert FailurePolicy.ROLLBACK_FAILED.value == "rollback_failed"


class TestCheckpoint:
    def test_checkpoint_creation(self, tmp_path):
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        from hooks.core.audit import AuditEntry

        entry = AuditEntry(action=action, sequence_number=1)
        checkpoint = Checkpoint(
            sequence_number=1,
            entry=entry,
            backup_data=b"backup",
        )

        assert checkpoint.sequence_number == 1
        assert checkpoint.entry == entry
        assert checkpoint.backup_data == b"backup"
