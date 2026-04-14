"""
Tests for the audit module.

Tests cover:
- Audit entry lifecycle
- Audit log management
- Report generation
- Rollback tracking
"""

from pathlib import Path

from hooks.audit import AuditEntry
from hooks.audit import AuditLog
from hooks.audit import OperationStatus
from hooks.operations import DeleteDirectoryOperation
from hooks.operations import DeleteFileOperation
from hooks.operations import OperationType


class TestAuditEntry:
    """Tests for AuditEntry."""

    def test_initial_state(self):
        """Test initial state of audit entry."""
        op = DeleteFileOperation(file_path=Path("test.txt"))
        entry = AuditEntry(operation=op, sequence_number=1)

        assert entry.status == OperationStatus.PENDING
        assert entry.timestamp_start is None
        assert entry.timestamp_end is None
        assert entry.error_message is None

    def test_mark_started(self):
        """Test marking entry as started."""
        op = DeleteFileOperation(file_path=Path("test.txt"))
        entry = AuditEntry(operation=op, sequence_number=1)

        entry.mark_started()

        assert entry.status == OperationStatus.EXECUTING
        assert entry.timestamp_start is not None

    def test_mark_success(self):
        """Test marking entry as successful."""
        op = DeleteFileOperation(file_path=Path("test.txt"))
        entry = AuditEntry(operation=op, sequence_number=1)

        entry.mark_started()
        entry.mark_success({"success": True})

        assert entry.status == OperationStatus.SUCCESS
        assert entry.timestamp_end is not None
        assert entry.result == {"success": True}

    def test_mark_failed(self):
        """Test marking entry as failed."""
        op = DeleteFileOperation(file_path=Path("test.txt"))
        entry = AuditEntry(operation=op, sequence_number=1)

        entry.mark_started()
        entry.mark_failed(ValueError("Test error"))

        assert entry.status == OperationStatus.FAILED
        assert entry.error_message == "Test error"

    def test_mark_rolled_back(self):
        """Test marking entry as rolled back."""
        op = DeleteFileOperation(file_path=Path("test.txt"))
        entry = AuditEntry(operation=op, sequence_number=1)

        entry.mark_started()
        entry.mark_success({"success": True})
        entry.mark_rolled_back()

        assert entry.status == OperationStatus.ROLLED_BACK

    def test_mark_skipped(self):
        """Test marking entry as skipped."""
        op = DeleteFileOperation(file_path=Path("test.txt"))
        entry = AuditEntry(operation=op, sequence_number=1)

        entry.mark_skipped("File does not exist")

        assert entry.status == OperationStatus.SKIPPED
        assert entry.error_message == "File does not exist"

    def test_to_dict(self):
        """Test serialization to dict."""
        op = DeleteFileOperation(file_path=Path("test.txt"))
        entry = AuditEntry(operation=op, sequence_number=1)

        entry.mark_started()
        entry.mark_success({"success": True})

        data = entry.to_dict()

        assert data["sequence_number"] == 1
        assert data["status"] == "SUCCESS"
        assert "operation" in data
        assert "duration_ms" in data


class TestAuditLog:
    """Tests for AuditLog."""

    def test_record_operation(self):
        """Test recording an operation."""
        log = AuditLog()
        op = DeleteFileOperation(file_path=Path("test.txt"))

        entry = log.record_operation(op)

        assert len(log.entries) == 1
        assert entry.sequence_number == 1
        assert entry.operation == op

    def test_multiple_operations_sequence(self):
        """Test sequence numbers for multiple operations."""
        log = AuditLog()

        entry1 = log.record_operation(DeleteFileOperation(file_path=Path("test1.txt")))
        entry2 = log.record_operation(DeleteFileOperation(file_path=Path("test2.txt")))
        entry3 = log.record_operation(DeleteFileOperation(file_path=Path("test3.txt")))

        assert entry1.sequence_number == 1
        assert entry2.sequence_number == 2
        assert entry3.sequence_number == 3

    def test_get_entries_by_status(self):
        """Test filtering entries by status."""
        log = AuditLog()

        op1 = DeleteFileOperation(file_path=Path("test1.txt"))
        entry1 = log.record_operation(op1)
        entry1.mark_success({})

        op2 = DeleteFileOperation(file_path=Path("test2.txt"))
        entry2 = log.record_operation(op2)
        entry2.mark_failed(ValueError("Error"))

        op3 = DeleteFileOperation(file_path=Path("test3.txt"))
        entry3 = log.record_operation(op3)
        entry3.mark_skipped("")

        successful = log.get_entries_by_status(OperationStatus.SUCCESS)
        failed = log.get_entries_by_status(OperationStatus.FAILED)

        assert len(successful) == 1
        assert len(failed) == 1
        assert successful[0] == entry1
        assert failed[0] == entry2

    def test_get_entries_by_type(self):
        """Test filtering entries by operation type."""
        log = AuditLog()

        file_op = DeleteFileOperation(file_path=Path("test.txt"))
        dir_op = DeleteDirectoryOperation(dir_path=Path("test_dir"))

        log.record_operation(file_op)
        log.record_operation(dir_op)

        file_entries = log.get_entries_by_type(OperationType.DELETE_FILE)
        dir_entries = log.get_entries_by_type(OperationType.DELETE_DIRECTORY)

        assert len(file_entries) == 1
        assert len(dir_entries) == 1

    def test_get_successful_entries(self):
        """Test getting successful entries for rollback."""
        log = AuditLog()

        op1 = DeleteFileOperation(file_path=Path("test1.txt"))
        entry1 = log.record_operation(op1)
        entry1.mark_success({})

        op2 = DeleteFileOperation(file_path=Path("test2.txt"))
        entry2 = log.record_operation(op2)
        entry2.mark_failed(ValueError("Error"))

        successful = log.get_successful_entries()

        assert len(successful) == 1
        assert successful[0] == entry1

    def test_get_entries_for_rollback(self):
        """Test getting entries in rollback order."""
        log = AuditLog()

        op1 = DeleteFileOperation(file_path=Path("test1.txt"))
        entry1 = log.record_operation(op1)
        entry1.mark_success({})

        op2 = DeleteFileOperation(file_path=Path("test2.txt"))
        entry2 = log.record_operation(op2)
        entry2.mark_success({})

        rollback_entries = log.get_entries_for_rollback()

        # Should be in reverse order
        assert len(rollback_entries) == 2
        assert rollback_entries[0] == entry2
        assert rollback_entries[1] == entry1

    def test_generate_report(self, tmp_path, monkeypatch):
        """Test report generation."""
        monkeypatch.chdir(tmp_path)
        log = AuditLog()

        op1 = DeleteFileOperation(file_path=Path("test1.txt"))
        entry1 = log.record_operation(op1)
        entry1.mark_success({})

        op2 = DeleteFileOperation(file_path=Path("test2.txt"))
        entry2 = log.record_operation(op2)
        entry2.mark_failed(ValueError("Error"))

        report = log.generate_report()

        assert report["summary"]["total_operations"] == 2
        assert report["summary"]["successful"] == 1
        assert report["summary"]["failed"] == 1
        assert len(report["changes"]) == 2

    def test_save_and_load(self, tmp_path, monkeypatch):
        """Test saving and loading audit log."""
        monkeypatch.chdir(tmp_path)
        log = AuditLog()

        op = DeleteFileOperation(file_path=Path("test.txt"))
        entry = log.record_operation(op)
        entry.mark_success({})

        save_path = tmp_path / "audit.json"
        log.save_to_file(save_path)

        assert save_path.exists()

        # Verify file contains valid JSON
        import json

        data = json.loads(save_path.read_text())
        assert "report" in data
        assert "entries" in data


class TestAuditLogEdgeCases:
    """Tests for edge cases."""

    def test_empty_log_report(self):
        """Test report generation with empty log."""
        log = AuditLog()

        report = log.generate_report()

        assert report["summary"]["total_operations"] == 0
        assert report["summary"]["successful"] == 0
        assert report["changes"] == []

    def test_all_failed_entries(self):
        """Test with all failed entries."""
        log = AuditLog()

        for i in range(3):
            op = DeleteFileOperation(file_path=Path(f"test{i}.txt"))
            entry = log.record_operation(op)
            entry.mark_failed(ValueError(f"Error {i}"))

        successful = log.get_successful_entries()
        rollback = log.get_entries_for_rollback()

        assert len(successful) == 0
        assert len(rollback) == 0
