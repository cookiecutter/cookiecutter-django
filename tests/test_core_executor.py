"""Tests for the core executor module."""

from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.context import FailurePolicy
from hooks.core.executor import ActionExecutor
from hooks.core.executor import ExecutionResult


class TestActionExecutor:
    def test_execute_empty_actions(self):
        context = ExecutionContext(project_slug="test_project")
        executor = ActionExecutor(context)

        result = executor.execute([])

        assert result.success
        assert "No actions" in result.message

    def test_execute_single_action_success(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        context = ExecutionContext(project_slug="test_project")
        executor = ActionExecutor(context)

        action = DeleteFileAction(file_path=test_file)
        result = executor.execute([action])

        assert result.success
        assert not test_file.exists()

    def test_execute_multiple_actions(self, tmp_path):
        file1 = tmp_path / "test1.txt"
        file2 = tmp_path / "test2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        context = ExecutionContext(project_slug="test_project")
        executor = ActionExecutor(context)

        actions = [
            DeleteFileAction(file_path=file1),
            DeleteFileAction(file_path=file2),
        ]
        result = executor.execute(actions)

        assert result.success
        assert not file1.exists()
        assert not file2.exists()

    def test_execute_with_stop_immediately_policy(self, tmp_path):
        file1 = tmp_path / "test1.txt"
        file2 = tmp_path / "test2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        context = ExecutionContext(
            project_slug="test_project",
            failure_policy=FailurePolicy.STOP_IMMEDIATELY,
        )
        executor = ActionExecutor(context)

        actions = [
            DeleteFileAction(file_path=file1),
            DeleteFileAction(file_path=tmp_path / "nonexistent"),
        ]
        result = executor.execute(actions)

        assert result.success

    def test_dry_run_mode(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        context = ExecutionContext(
            project_slug="test_project",
            dry_run=True,
        )
        executor = ActionExecutor(context)

        action = DeleteFileAction(file_path=test_file)
        result = executor.execute([action])

        assert result.success
        assert test_file.exists()

    def test_rollback_all(self, tmp_path):
        file1 = tmp_path / "test1.txt"
        file2 = tmp_path / "test2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        context = ExecutionContext(
            project_slug="test_project",
            failure_policy=FailurePolicy.ROLLBACK_ALL,
        )
        executor = ActionExecutor(context)

        actions = [
            DeleteFileAction(file_path=file1),
            DeleteFileAction(file_path=file2),
        ]
        result = executor.execute(actions)

        assert result.success
        assert not file1.exists()
        assert not file2.exists()

    def test_audit_logger_records_actions(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        context = ExecutionContext(project_slug="test_project")
        executor = ActionExecutor(context)

        action = DeleteFileAction(file_path=test_file)
        executor.execute([action])

        assert len(context.audit_logger.report.entries) == 1


class TestExecutionResult:
    def test_success_result(self):
        result = ExecutionResult(success=True, message="Done")

        assert result.success
        assert result.message == "Done"
        assert bool(result)

    def test_failure_result(self):
        result = ExecutionResult(
            success=False,
            message="Failed",
            failed_actions=["action1"],
        )

        assert not result.success
        assert len(result.failed_actions) == 1
        assert not bool(result)

    def test_result_with_rollback(self):
        result = ExecutionResult(
            success=False,
            message="Rolled back",
            rolled_back_count=3,
        )

        assert result.rolled_back_count == 3
