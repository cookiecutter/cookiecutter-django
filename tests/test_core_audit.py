"""Tests for the core audit module."""

import json
from pathlib import Path

import pytest

from hooks.core.actions import DeleteFileAction, ModifyFileAction
from hooks.core.audit import AuditEntry, AuditLogger, AuditReport, AuditStatus


class TestAuditEntry:
    def test_audit_entry_creation(self, tmp_path):
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        entry = AuditEntry(action=action, sequence_number=1)

        assert entry.action == action
        assert entry.status == AuditStatus.PENDING
        assert entry.sequence_number == 1

    def test_audit_entry_to_dict(self, tmp_path):
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        entry = AuditEntry(action=action, sequence_number=1)

        d = entry.to_dict()

        assert d["sequence_number"] == 1
        assert d["status"] == "pending"
        assert d["action"]["type"] == "delete_file"


class TestAuditReport:
    def test_empty_report(self):
        report = AuditReport()

        assert report.total_actions == 0
        assert report.successful_actions == 0
        assert report.failed_actions == 0

    def test_report_counts(self, tmp_path):
        report = AuditReport()

        action1 = DeleteFileAction(file_path=tmp_path / "test1.txt")
        action2 = DeleteFileAction(file_path=tmp_path / "test2.txt")
        action3 = ModifyFileAction(file_path=tmp_path / "test3.txt", modifications={})

        entry1 = AuditEntry(action=action1, status=AuditStatus.SUCCESS)
        entry2 = AuditEntry(action=action2, status=AuditStatus.FAILED)
        entry3 = AuditEntry(action=action3, status=AuditStatus.SUCCESS)

        report.entries = [entry1, entry2, entry3]

        assert report.total_actions == 3
        assert report.successful_actions == 2
        assert report.failed_actions == 1

    def test_report_to_dict(self, tmp_path):
        report = AuditReport(project_name="test_project")

        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        entry = AuditEntry(action=action, status=AuditStatus.SUCCESS, sequence_number=1)
        report.entries = [entry]

        d = report.to_dict()

        assert d["project_name"] == "test_project"
        assert d["summary"]["total_actions"] == 1
        assert d["summary"]["successful"] == 1

    def test_report_to_markdown(self, tmp_path):
        report = AuditReport(project_name="test_project")

        action = DeleteFileAction(
            file_path=tmp_path / "test.txt",
            description="Delete test file",
        )
        entry = AuditEntry(action=action, status=AuditStatus.SUCCESS, sequence_number=1)
        report.entries = [entry]
        report.end_time = report.start_time

        md = report.to_markdown()

        assert "# Project Generation Report" in md
        assert "test_project" in md
        assert "Delete test file" in md
        assert "✅" in md


class TestAuditLogger:
    def test_log_action(self, tmp_path):
        logger = AuditLogger(project_name="test")
        action = DeleteFileAction(file_path=tmp_path / "test.txt")

        entry = logger.log_action(action)

        assert len(logger.report.entries) == 1
        assert entry.action == action
        assert entry.sequence_number == 1

    def test_log_result(self, tmp_path):
        logger = AuditLogger(project_name="test")
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        entry = logger.log_action(action)

        from hooks.core.actions import ActionResult

        result = ActionResult(success=True, message="Done")
        logger.log_result(entry, result)

        assert entry.result == result
        assert entry.status == AuditStatus.SUCCESS

    def test_log_rollback(self, tmp_path):
        logger = AuditLogger(project_name="test")
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        entry = logger.log_action(action)

        from hooks.core.actions import ActionResult

        rollback_result = ActionResult(success=True, message="Rolled back")
        logger.log_rollback(entry, rollback_result)

        assert entry.rollback_result == rollback_result
        assert entry.status == AuditStatus.ROLLED_BACK

    def test_finalize(self, tmp_path):
        logger = AuditLogger(project_name="test")
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        logger.log_action(action)

        report = logger.finalize()

        assert report.end_time is not None
        assert report.project_name == "test"

    def test_get_successful_entries(self, tmp_path):
        logger = AuditLogger(project_name="test")

        action1 = DeleteFileAction(file_path=tmp_path / "test1.txt")
        action2 = DeleteFileAction(file_path=tmp_path / "test2.txt")

        entry1 = logger.log_action(action1)
        entry2 = logger.log_action(action2)

        from hooks.core.actions import ActionResult

        logger.log_result(entry1, ActionResult(success=True))
        logger.log_result(entry2, ActionResult(success=False))

        successful = logger.get_successful_entries()
        assert len(successful) == 1
        assert successful[0] == entry1

    def test_get_failed_entries(self, tmp_path):
        logger = AuditLogger(project_name="test")

        action1 = DeleteFileAction(file_path=tmp_path / "test1.txt")
        action2 = DeleteFileAction(file_path=tmp_path / "test2.txt")

        entry1 = logger.log_action(action1)
        entry2 = logger.log_action(action2)

        from hooks.core.actions import ActionResult

        logger.log_result(entry1, ActionResult(success=True))
        logger.log_result(entry2, ActionResult(success=False, error="Failed"))

        failed = logger.get_failed_entries()
        assert len(failed) == 1
        assert failed[0] == entry2
