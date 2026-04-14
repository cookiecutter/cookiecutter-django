from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from pathlib import Path
from typing import Any

from hooks.core.audit import AuditEntry
from hooks.core.audit import AuditLogger


class FailurePolicy(Enum):
    STOP_IMMEDIATELY = "stop_immediately"
    CONTINUE_ON_ERROR = "continue_on_error"
    ROLLBACK_ALL = "rollback_all"
    ROLLBACK_FAILED = "rollback_failed"


@dataclass
class Checkpoint:
    sequence_number: int
    entry: AuditEntry
    backup_data: Any


@dataclass
class ExecutionContext:
    project_slug: str
    cookiecutter_config: dict[str, Any] = field(default_factory=dict)
    failure_policy: FailurePolicy = FailurePolicy.STOP_IMMEDIATELY
    dry_run: bool = False
    audit_logger: AuditLogger = field(default_factory=AuditLogger)
    checkpoints: list[Checkpoint] = field(default_factory=list)
    last_successful_checkpoint: int = 0
    _backup_store: dict[int, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.audit_logger.report.project_name = self.project_slug

    def get_config(self, key: str, default: Any = None) -> Any:
        return self.cookiecutter_config.get(key, default)

    def is_enabled(self, key: str) -> bool:
        value = self.get_config(key, "n")
        return str(value).lower() in ("y", "yes", "true", "1")

    def equals(self, key: str, value: str) -> bool:
        return str(self.get_config(key, "")).lower() == value.lower()

    def create_checkpoint(self, entry: AuditEntry, backup_data: Any) -> Checkpoint:
        checkpoint = Checkpoint(
            sequence_number=entry.sequence_number,
            entry=entry,
            backup_data=backup_data,
        )
        self.checkpoints.append(checkpoint)
        self._backup_store[entry.sequence_number] = backup_data
        return checkpoint

    def get_backup(self, sequence_number: int) -> Any:
        return self._backup_store.get(sequence_number)

    def get_checkpoints_for_rollback(self) -> list[Checkpoint]:
        return [cp for cp in reversed(self.checkpoints) if cp.backup_data is not None]

    def mark_success(self, sequence_number: int) -> None:
        self.last_successful_checkpoint = sequence_number

    def get_report(self) -> str:
        report = self.audit_logger.finalize()
        return report.to_markdown()

    def get_json_report(self) -> dict[str, Any]:
        report = self.audit_logger.finalize()
        return report.to_dict()

    def save_report(self, output_path: Path) -> None:
        report = self.audit_logger.finalize()
        output_path.write_text(report.to_markdown(), encoding="utf-8")

    def save_json_report(self, output_path: Path) -> None:
        import json

        report = self.audit_logger.finalize()
        output_path.write_text(
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
