from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Any

from hooks.core.actions import Action
from hooks.core.actions import ActionResult


class AuditStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class AuditEntry:
    action: Action
    result: ActionResult | None = None
    status: AuditStatus = AuditStatus.PENDING
    timestamp: datetime = field(default_factory=datetime.now)
    rollback_result: ActionResult | None = None
    sequence_number: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence_number": self.sequence_number,
            "action": self.action.to_dict(),
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "result": {
                "success": self.result.success,
                "message": self.result.message,
                "error": self.result.error,
            }
            if self.result
            else None,
            "rollback_result": {
                "success": self.rollback_result.success,
                "message": self.rollback_result.message,
                "error": self.rollback_result.error,
            }
            if self.rollback_result
            else None,
        }


@dataclass
class AuditReport:
    entries: list[AuditEntry] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    project_name: str = ""

    @property
    def total_actions(self) -> int:
        return len(self.entries)

    @property
    def successful_actions(self) -> int:
        return sum(1 for e in self.entries if e.status == AuditStatus.SUCCESS)

    @property
    def failed_actions(self) -> int:
        return sum(1 for e in self.entries if e.status == AuditStatus.FAILED)

    @property
    def rolled_back_actions(self) -> int:
        return sum(1 for e in self.entries if e.status == AuditStatus.ROLLED_BACK)

    @property
    def files_deleted(self) -> int:
        from hooks.core.actions import ActionType

        return sum(
            1
            for e in self.entries
            if e.action.action_type == ActionType.DELETE_FILE and e.status == AuditStatus.SUCCESS
        )

    @property
    def directories_deleted(self) -> int:
        from hooks.core.actions import ActionType

        return sum(
            1
            for e in self.entries
            if e.action.action_type == ActionType.DELETE_DIRECTORY and e.status == AuditStatus.SUCCESS
        )

    @property
    def files_modified(self) -> int:
        from hooks.core.actions import ActionType

        return sum(
            1
            for e in self.entries
            if e.action.action_type in (ActionType.MODIFY_FILE, ActionType.APPEND_FILE)
            and e.status == AuditStatus.SUCCESS
        )

    @property
    def commands_executed(self) -> int:
        from hooks.core.actions import ActionType

        return sum(
            1
            for e in self.entries
            if e.action.action_type == ActionType.RUN_COMMAND and e.status == AuditStatus.SUCCESS
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_name": self.project_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "summary": {
                "total_actions": self.total_actions,
                "successful": self.successful_actions,
                "failed": self.failed_actions,
                "rolled_back": self.rolled_back_actions,
                "files_deleted": self.files_deleted,
                "directories_deleted": self.directories_deleted,
                "files_modified": self.files_modified,
                "commands_executed": self.commands_executed,
            },
            "entries": [e.to_dict() for e in self.entries],
        }

    def to_markdown(self) -> str:
        lines = [
            "# Project Generation Report",
            "",
            f"**Project:** {self.project_name}",
            f"**Started:** {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
        ]

        if self.end_time:
            lines.append(f"**Finished:** {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            duration = (self.end_time - self.start_time).total_seconds()
            lines.append(f"**Duration:** {duration:.2f} seconds")

        lines.extend(
            [
                "",
                "## Summary",
                "",
                "| Metric | Count |",
                "|--------|-------|",
                f"| Total Actions | {self.total_actions} |",
                f"| Successful | {self.successful_actions} |",
                f"| Failed | {self.failed_actions} |",
                f"| Rolled Back | {self.rolled_back_actions} |",
                f"| Files Deleted | {self.files_deleted} |",
                f"| Directories Deleted | {self.directories_deleted} |",
                f"| Files Modified | {self.files_modified} |",
                f"| Commands Executed | {self.commands_executed} |",
                "",
                "## Detailed Actions",
                "",
            ],
        )

        for entry in self.entries:
            status_icon = {
                AuditStatus.SUCCESS: "✅",
                AuditStatus.FAILED: "❌",
                AuditStatus.ROLLED_BACK: "↩️",
                AuditStatus.PENDING: "⏳",
            }.get(entry.status, "❓")

            lines.append(f"### {status_icon} {entry.action.describe()}")
            lines.append(f"- **Type:** `{entry.action.action_type.value}`")
            lines.append(f"- **Status:** {entry.status.value}")

            if entry.result:
                lines.append(f"- **Message:** {entry.result.message}")
                if entry.result.error:
                    lines.append(f"- **Error:** {entry.result.error}")

            if entry.rollback_result:
                lines.append(f"- **Rollback:** {entry.rollback_result.message}")

            lines.append("")

        return "\n".join(lines)


class AuditLogger:
    def __init__(self, project_name: str = ""):
        self.report = AuditReport(project_name=project_name)
        self._sequence = 0

    def log_action(self, action: Action) -> AuditEntry:
        self._sequence += 1
        entry = AuditEntry(action=action, sequence_number=self._sequence)
        self.report.entries.append(entry)
        return entry

    def log_result(self, entry: AuditEntry, result: ActionResult) -> None:
        entry.result = result
        entry.status = AuditStatus.SUCCESS if result.success else AuditStatus.FAILED

    def log_rollback(self, entry: AuditEntry, result: ActionResult) -> None:
        entry.rollback_result = result
        if result.success:
            entry.status = AuditStatus.ROLLED_BACK

    def finalize(self) -> AuditReport:
        self.report.end_time = datetime.now()
        return self.report

    def get_successful_entries(self) -> list[AuditEntry]:
        return [e for e in self.report.entries if e.status == AuditStatus.SUCCESS]

    def get_failed_entries(self) -> list[AuditEntry]:
        return [e for e in self.report.entries if e.status == AuditStatus.FAILED]
