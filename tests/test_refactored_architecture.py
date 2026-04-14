"""Tests for the refactored architecture: audit, operations, strategies, rollback"""

import os
from pathlib import Path

import pytest

from hooks.core import AppendFileOperation
from hooks.core import AuditLog
from hooks.core import DeleteDirOperation
from hooks.core import DeleteFileOperation
from hooks.core import ExecutionContext
from hooks.core import FailureStrategy
from hooks.core import ModifyFileOperation
from hooks.core import RealExecutor
from hooks.core import SetFlagOperation
from hooks.strategies import ALL_STRATEGIES
from hooks.strategies import AsyncStrategy
from hooks.strategies import CeleryStrategy
from hooks.strategies import CiToolStrategy
from hooks.strategies import DockerStrategy
from hooks.strategies import FrontendPipelineStrategy
from hooks.strategies import LicenseStrategy
from hooks.strategies import RestApiStrategy
from hooks.strategies import UsernameTypeStrategy


class TestAuditLog:
    def test_audit_log_records_operations(self):
        audit = AuditLog()
        assert len(audit.entries) == 0

        from hooks.core import AuditEntry
        from hooks.core import OperationType

        entry = AuditEntry(
            operation_type=OperationType.DELETE_FILE,
            target="test.txt",
            success=True,
        )
        audit.record(entry)
        assert len(audit.entries) == 1
        assert audit.entries[0].target == "test.txt"

    def test_generate_report_summary(self):
        audit = AuditLog()
        from hooks.core import AuditEntry
        from hooks.core import OperationType

        audit.record(AuditEntry(OperationType.DELETE_FILE, "f1.txt", success=True))
        audit.record(AuditEntry(OperationType.DELETE_FILE, "f2.txt", success=True))
        audit.record(AuditEntry(OperationType.MODIFY_FILE, "f3.txt", success=False, error="test error"))

        report = audit.generate_report()
        assert report["summary"]["total_operations"] == 3
        assert report["summary"]["successful"] == 2
        assert report["summary"]["failed"] == 1
        assert report["operations_by_type"]["delete_file"] == 2
        assert report["operations_by_type"]["modify_file"] == 1


class TestOperations:
    def test_delete_file_operation(self, working_directory):
        test_file = Path("test_delete.txt")
        test_file.write_text("content")

        op = DeleteFileOperation(test_file)
        audit = AuditLog()

        op.execute(audit)
        assert not test_file.exists()
        assert op.executed
        assert audit.entries[0].success

    def test_delete_file_rollback(self, working_directory):
        test_file = Path("test_rollback.txt")
        original_content = "important content"
        test_file.write_text(original_content)

        op = DeleteFileOperation(test_file)
        audit = AuditLog()
        op.execute(audit)
        assert not test_file.exists()

        op.rollback(audit)
        assert test_file.exists()
        assert test_file.read_text() == original_content

    def test_modify_file_operation_and_rollback(self, working_directory):
        test_file = Path("test_modify.txt")
        test_file.write_text("Hello World")

        def modifier(content):
            return content.replace("World", "Django")

        op = ModifyFileOperation(test_file, modifier)
        audit = AuditLog()
        op.execute(audit)

        assert test_file.read_text() == "Hello Django"

        op.rollback(audit)
        assert test_file.read_text() == "Hello World"

    def test_append_file_operation_and_rollback(self, working_directory):
        test_file = Path("test_append.txt")
        test_file.write_text("line1\n")

        op = AppendFileOperation(test_file, "line2")
        audit = AuditLog()
        op.execute(audit)

        lines = test_file.read_text().splitlines()
        assert len(lines) == 2
        assert lines[1] == "line2"

        op.rollback(audit)
        assert test_file.read_text() == "line1\n"

    def test_set_flag_operation(self, working_directory):
        test_file = Path("test_flag.txt")
        test_file.write_text("SECRET_KEY = '!!!SET MY_KEY!!!'")

        op = SetFlagOperation(test_file, "!!!SET MY_KEY!!!", "super-secret-123")
        audit = AuditLog()
        op.execute(audit)

        assert "super-secret-123" in test_file.read_text()
        assert "!!!SET MY_KEY!!!" not in test_file.read_text()

    def test_delete_dir_operation_and_rollback(self, working_directory):
        test_dir = Path("test_dir")
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content1")
        (test_dir / "file2.txt").write_text("content2")

        op = DeleteDirOperation(test_dir)
        audit = AuditLog()
        op.execute(audit)

        assert not test_dir.exists()

        op.rollback(audit)
        assert test_dir.exists()
        assert (test_dir / "file1.txt").read_text() == "content1"
        assert (test_dir / "file2.txt").read_text() == "content2"


class TestExecutors:
    def test_dry_run_executor(self, working_directory):
        test_file = Path("test_dryrun.txt")
        test_file.write_text("content")

        ctx = ExecutionContext(dry_run=True)
        ctx.add_operation(DeleteFileOperation(test_file))
        ctx.execute_all()

        assert test_file.exists()
        report = ctx.get_report()
        assert report["entries"][0]["details"]["dry_run"] is True

    def test_real_executor(self, working_directory):
        test_file = Path("test_real.txt")
        test_file.write_text("content")

        ctx = ExecutionContext(executor=RealExecutor())
        ctx.add_operation(DeleteFileOperation(test_file))
        ctx.execute_all()

        assert not test_file.exists()


class TestRollbackManager:
    def test_rollback_all_on_failure(self, working_directory):
        f1 = Path("f1.txt")
        f2 = Path("f2.txt")
        f1.write_text("content1")
        f2.write_text("content2")

        class FailingOperation(DeleteFileOperation):
            def _execute(self):
                super()._execute()
                raise RuntimeError("Simulated failure")

        ctx = ExecutionContext(failure_strategy=FailureStrategy.ROLLBACK)
        ctx.add_operation(DeleteFileOperation(f1))
        ctx.add_operation(FailingOperation(f2))

        with pytest.raises(RuntimeError):
            ctx.execute_all()

        assert f1.exists()

    def test_checkpoint_and_resume(self, working_directory):
        ctx = ExecutionContext()
        f1 = Path("f1.txt")
        f2 = Path("f2.txt")
        f3 = Path("f3.txt")
        for f in [f1, f2, f3]:
            f.write_text("content")

        ctx.add_operation(DeleteFileOperation(f1))
        ctx.checkpoint()
        ctx.add_operation(DeleteFileOperation(f2))
        ctx.add_operation(DeleteFileOperation(f3))

        assert ctx.checkpoint_index == 1

        ctx.operations[1]._execute = lambda: (_ for _ in ()).throw(RuntimeError("Oops"))
        ctx.failure_strategy = FailureStrategy.ABORT

        with pytest.raises(RuntimeError):
            ctx.execute_all()

        assert not f1.exists()


class TestStrategies:
    def test_all_strategies_have_should_apply(self):
        for strategy_class in ALL_STRATEGIES:
            strategy = strategy_class()
            assert callable(strategy.should_apply)
            assert callable(strategy.collect_operations)

    def test_license_strategy(self):
        strategy = LicenseStrategy()
        closed_ops = strategy.collect_operations({"open_source_license": "Not open source"})
        mit_ops = strategy.collect_operations({"open_source_license": "MIT"})
        assert len(closed_ops) >= len(mit_ops)

    def test_username_type_strategy(self):
        strategy = UsernameTypeStrategy()
        ops = strategy.collect_operations({"username_type": "username"})
        assert len(ops) == 2

        ops_email = strategy.collect_operations({"username_type": "email"})
        assert len(ops_email) == 0

    def test_docker_strategy(self):
        strategy = DockerStrategy()
        ops_with_docker = strategy.collect_operations(
            {
                "use_docker": "y",
                "cloud_provider": "AWS",
            }
        )
        ops_no_docker = strategy.collect_operations(
            {
                "use_docker": "n",
                "cloud_provider": "None",
            }
        )
        assert len(ops_no_docker) > len(ops_with_docker)

    def test_celery_strategy(self):
        strategy = CeleryStrategy()
        ops_no_celery = strategy.collect_operations(
            {
                "use_celery": "n",
                "use_docker": "y",
            }
        )
        ops_with_celery = strategy.collect_operations(
            {
                "use_celery": "y",
                "use_docker": "y",
            }
        )
        assert len(ops_no_celery) > len(ops_with_celery)

    def test_ci_tool_strategy(self):
        strategy = CiToolStrategy()
        ops_none = strategy.collect_operations({"ci_tool": "None"})
        ops_github = strategy.collect_operations({"ci_tool": "Github"})
        assert len(ops_none) > len(ops_github)

    def test_rest_api_strategy(self):
        strategy = RestApiStrategy()
        ops_none = strategy.collect_operations({"rest_api": "None"})
        ops_drf = strategy.collect_operations({"rest_api": "DRF"})
        ops_ninja = strategy.collect_operations({"rest_api": "Django Ninja"})
        assert len(ops_none) > len(ops_drf)
        assert len(ops_none) > len(ops_ninja)

    def test_async_strategy(self):
        strategy = AsyncStrategy()
        ops_no_async = strategy.collect_operations({"use_async": "n"})
        ops_async = strategy.collect_operations({"use_async": "y"})
        assert len(ops_no_async) == 2
        assert len(ops_async) == 0

    def test_frontend_pipeline_strategy(self):
        strategy = FrontendPipelineStrategy()
        ops_none = strategy.collect_operations(
            {
                "frontend_pipeline": "None",
                "use_docker": "y",
                "use_async": "n",
            }
        )
        assert len(ops_none) > 0

    def test_all_strategies_produce_operations(self):
        default_context = {
            "open_source_license": "MIT",
            "username_type": "email",
            "editor": "None",
            "use_docker": "n",
            "cloud_provider": "None",
            "use_heroku": "n",
            "ci_tool": "None",
            "keep_local_envs_in_vcs": "y",
            "frontend_pipeline": "None",
            "use_celery": "n",
            "rest_api": "None",
            "use_async": "n",
            "debug": "y",
        }

        all_ops = []
        for strategy_class in ALL_STRATEGIES:
            strategy = strategy_class()
            if strategy.should_apply(default_context):
                ops = strategy.collect_operations(default_context)
                all_ops.extend(ops)

        assert len(all_ops) > 0


class TestExecutionContext:
    def test_two_phase_execution(self, working_directory):
        f1 = Path("f1.txt")
        f2 = Path("f2.txt")
        f1.write_text("c1")
        f2.write_text("c2")

        ctx = ExecutionContext()

        assert len(ctx.operations) == 0

        ctx.add_operation(DeleteFileOperation(f1))
        ctx.add_operation(DeleteFileOperation(f2))

        assert len(ctx.operations) == 2
        assert f1.exists()
        assert f2.exists()

        ctx.execute_all()

        assert not f1.exists()
        assert not f2.exists()

    def test_report_generation_after_execution(self, working_directory):
        f1 = Path("report_test.txt")
        f1.write_text("test")

        ctx = ExecutionContext()
        ctx.add_operation(DeleteFileOperation(f1))
        ctx.execute_all()

        report = ctx.get_report()
        assert report["summary"]["total_operations"] == 1
        assert report["summary"]["successful"] == 1
        assert "delete_file" in report["operations_by_type"]


@pytest.fixture
def working_directory(tmp_path):
    prev_cwd = Path.cwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(prev_cwd)
