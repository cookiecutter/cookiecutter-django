from __future__ import annotations

import json
import random
import shutil
import string
import subprocess
import sys
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Callable

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

DEBUG_VALUE = "debug"


class OperationType(Enum):
    DELETE_FILE = "delete_file"
    DELETE_DIR = "delete_dir"
    MODIFY_FILE = "modify_file"
    APPEND_FILE = "append_file"
    RUN_COMMAND = "run_command"
    SET_FLAG = "set_flag"


class FailureStrategy(Enum):
    ABORT = "abort"
    CONTINUE = "continue"
    ROLLBACK = "rollback"


@dataclass
class AuditEntry:
    operation_type: OperationType
    target: str
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = False
    error: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


class AuditLog:
    def __init__(self) -> None:
        self.entries: list[AuditEntry] = []

    def record(self, entry: AuditEntry) -> None:
        self.entries.append(entry)

    def generate_report(self) -> dict[str, Any]:
        total = len(self.entries)
        successful = sum(1 for e in self.entries if e.success)
        failed = sum(1 for e in self.entries if not e.success)
        by_type = {op_type: sum(1 for e in self.entries if e.operation_type == op_type) for op_type in OperationType}
        return {
            "summary": {
                "total_operations": total,
                "successful": successful,
                "failed": failed,
            },
            "operations_by_type": {k.value: v for k, v in by_type.items() if v > 0},
            "entries": [
                {
                    "type": e.operation_type.value,
                    "target": e.target,
                    "timestamp": e.timestamp.isoformat(),
                    "success": e.success,
                    "error": e.error,
                    "details": e.details,
                }
                for e in self.entries
            ],
        }

    def print_report(self) -> None:
        report = self.generate_report()
        print("\n" + "=" * 60)
        print("GENERATION AUDIT REPORT")
        print("=" * 60)
        print(f"Total operations: {report['summary']['total_operations']}")
        print(f"Successful: {report['summary']['successful']}")
        print(f"Failed: {report['summary']['failed']}")
        print("\nOperations by type:")
        for op_type, count in report["operations_by_type"].items():
            print(f"  - {op_type}: {count}")
        print("=" * 60 + "\n")


class Operation(ABC):
    def __init__(self, operation_type: OperationType, target: str) -> None:
        self.operation_type = operation_type
        self.target = target
        self.executed = False
        self.backup_data: Any = None

    @abstractmethod
    def _execute(self) -> None: ...

    @abstractmethod
    def _rollback(self) -> None: ...

    def execute(self, audit_log: AuditLog) -> None:
        entry = AuditEntry(operation_type=self.operation_type, target=self.target)
        try:
            self._execute()
            self.executed = True
            entry.success = True
        except Exception as e:
            entry.success = False
            entry.error = str(e)
            raise
        finally:
            audit_log.record(entry)

    def rollback(self, audit_log: AuditLog) -> None:
        if not self.executed:
            return
        entry = AuditEntry(
            operation_type=self.operation_type,
            target=f"ROLLBACK: {self.target}",
            details={"original_operation": self.target},
        )
        try:
            self._rollback()
            entry.success = True
        except Exception as e:
            entry.success = False
            entry.error = str(e)
            raise
        finally:
            audit_log.record(entry)


class DeleteFileOperation(Operation):
    def __init__(self, file_path: Path | str) -> None:
        super().__init__(OperationType.DELETE_FILE, str(file_path))
        self.file_path = Path(file_path)
        self.backup_content: bytes | None = None

    def _execute(self) -> None:
        if self.file_path.exists():
            self.backup_content = self.file_path.read_bytes()
            self.file_path.unlink()

    def _rollback(self) -> None:
        if self.backup_content is not None:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_bytes(self.backup_content)


class DeleteDirOperation(Operation):
    def __init__(self, dir_path: Path | str) -> None:
        super().__init__(OperationType.DELETE_DIR, str(dir_path))
        self.dir_path = Path(dir_path)
        self.backup_archive: Path | None = None

    def _execute(self) -> None:
        if self.dir_path.exists():
            backup_base = self.dir_path.parent / f".backup_{self.dir_path.name}"
            self.backup_archive = Path(shutil.make_archive(str(backup_base), "zip", self.dir_path))
            shutil.rmtree(self.dir_path)

    def _rollback(self) -> None:
        if self.backup_archive and self.backup_archive.exists():
            self.dir_path.mkdir(parents=True, exist_ok=True)
            shutil.unpack_archive(str(self.backup_archive), self.dir_path)
            self.backup_archive.unlink()


class ModifyFileOperation(Operation):
    def __init__(
        self,
        file_path: Path | str,
        modifier: Callable[[str], str],
    ) -> None:
        super().__init__(OperationType.MODIFY_FILE, str(file_path))
        self.file_path = Path(file_path)
        self.modifier = modifier
        self.backup_content: bytes | None = None

    def _execute(self) -> None:
        self.backup_content = self.file_path.read_bytes()
        content = self.file_path.read_text()
        new_content = self.modifier(content)
        self.file_path.write_text(new_content)

    def _rollback(self) -> None:
        if self.backup_content is not None:
            self.file_path.write_bytes(self.backup_content)


class AppendFileOperation(Operation):
    def __init__(self, file_path: Path | str, content: str) -> None:
        super().__init__(OperationType.APPEND_FILE, str(file_path))
        self.file_path = Path(file_path)
        self.content = content
        self.original_size: int = 0

    def _execute(self) -> None:
        self.original_size = self.file_path.stat().st_size if self.file_path.exists() else 0
        with self.file_path.open("a") as f:
            f.write(self.content + "\n")

    def _rollback(self) -> None:
        if self.file_path.exists():
            with self.file_path.open("r+b") as f:
                f.truncate(self.original_size)


class RunCommandOperation(Operation):
    def __init__(self, cmd: list[str], **kwargs: Any) -> None:
        super().__init__(OperationType.RUN_COMMAND, " ".join(cmd))
        self.cmd = cmd
        self.kwargs = kwargs
        self.details: dict[str, Any] = {}

    def _execute(self) -> None:
        result = subprocess.run(
            self.cmd,
            capture_output=True,
            check=True,
            **self.kwargs,
        )
        self.details = {
            "returncode": result.returncode,
            "stdout": result.stdout.decode()[:500],
            "stderr": result.stderr.decode()[:500],
        }

    def _rollback(self) -> None:
        pass


class SetFlagOperation(Operation):
    def __init__(self, file_path: Path | str, flag: str, value: str) -> None:
        super().__init__(OperationType.SET_FLAG, str(file_path))
        self.file_path = Path(file_path)
        self.flag = flag
        self.value = value
        self.backup_content: bytes | None = None

    def _execute(self) -> None:
        self.backup_content = self.file_path.read_bytes()
        content = self.file_path.read_text()
        content = content.replace(self.flag, self.value)
        self.file_path.write_text(content)

    def _rollback(self) -> None:
        if self.backup_content is not None:
            self.file_path.write_bytes(self.backup_content)


class Executor(ABC):
    @abstractmethod
    def execute(self, operation: Operation, audit_log: AuditLog) -> None: ...


class RealExecutor(Executor):
    def execute(self, operation: Operation, audit_log: AuditLog) -> None:
        operation.execute(audit_log)


class DryRunExecutor(Executor):
    def execute(self, operation: Operation, audit_log: AuditLog) -> None:
        entry = AuditEntry(
            operation_type=operation.operation_type,
            target=operation.target,
            details={"dry_run": True},
        )
        entry.success = True
        audit_log.record(entry)
        print(f"[DRY RUN] Would {operation.operation_type.value}: {operation.target}")


class LogOnlyExecutor(Executor):
    def execute(self, operation: Operation, audit_log: AuditLog) -> None:
        entry = AuditEntry(
            operation_type=operation.operation_type,
            target=operation.target,
            details={"log_only": True},
        )
        entry.success = True
        audit_log.record(entry)


class RollbackManager:
    def __init__(self, audit_log: AuditLog) -> None:
        self.audit_log = audit_log
        self.executed_operations: list[Operation] = []

    def register_executed(self, operation: Operation) -> None:
        if operation.executed:
            self.executed_operations.append(operation)

    def rollback_all(self) -> None:
        print("\n" + "!" * 60)
        print("ROLLING BACK ALL OPERATIONS")
        print("!" * 60)
        for operation in reversed(self.executed_operations):
            try:
                operation.rollback(self.audit_log)
                print(f"  Rolled back: {operation.target}")
            except Exception as e:
                print(f"  Failed to rollback {operation.target}: {e}")
        print("Rollback complete\n")


class ExecutionContext:
    def __init__(
        self,
        executor: Executor | None = None,
        failure_strategy: FailureStrategy = FailureStrategy.ROLLBACK,
        dry_run: bool = False,
    ) -> None:
        self.audit_log = AuditLog()
        self.rollback_manager = RollbackManager(self.audit_log)
        self.executor = executor or (DryRunExecutor() if dry_run else RealExecutor())
        self.failure_strategy = failure_strategy
        self.operations: list[Operation] = []
        self.checkpoint_index = 0

    def add_operation(self, operation: Operation) -> None:
        self.operations.append(operation)

    def checkpoint(self) -> None:
        self.checkpoint_index = len(self.operations)

    def execute_all(self) -> None:
        for i, operation in enumerate(self.operations):
            try:
                self.executor.execute(operation, self.audit_log)
                self.rollback_manager.register_executed(operation)
            except Exception as e:
                print(f"Error executing operation {operation.target}: {e}", file=sys.stderr)
                match self.failure_strategy:
                    case FailureStrategy.ABORT:
                        print("Aborting execution due to failure", file=sys.stderr)
                        raise
                    case FailureStrategy.CONTINUE:
                        print("Continuing despite failure...", file=sys.stderr)
                        continue
                    case FailureStrategy.ROLLBACK:
                        self.rollback_manager.rollback_all()
                        raise
        self.checkpoint()

    def resume_from_checkpoint(self) -> None:
        for operation in self.operations[self.checkpoint_index :]:
            try:
                self.executor.execute(operation, self.audit_log)
                self.rollback_manager.register_executed(operation)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                match self.failure_strategy:
                    case FailureStrategy.ROLLBACK:
                        self.rollback_manager.rollback_all()
                        raise
                    case FailureStrategy.ABORT:
                        raise
                    case FailureStrategy.CONTINUE:
                        continue

    def get_report(self) -> dict[str, Any]:
        return self.audit_log.generate_report()

    def print_report(self) -> None:
        self.audit_log.print_report()


class Strategy(ABC):
    @abstractmethod
    def should_apply(self, context: dict[str, Any]) -> bool: ...

    @abstractmethod
    def collect_operations(self, context: dict[str, Any]) -> list[Operation]: ...


def update_package_json_modifier(
    remove_dev_deps: list[str] | None = None,
    remove_keys: list[str] | None = None,
    scripts: dict[str, str] | None = None,
) -> Callable[[str], str]:
    remove_dev_deps = remove_dev_deps or []
    remove_keys = remove_keys or []
    scripts = scripts or {}

    def modifier(content: str) -> str:
        data = json.loads(content)
        for package_name in remove_dev_deps:
            data["devDependencies"].pop(package_name, None)
        for key in remove_keys:
            data.pop(key, None)
        data["scripts"].update(scripts)
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"

    return modifier


def remove_repo_from_pre_commit_modifier(repo_to_remove: str) -> Callable[[str], str]:
    def modifier(content: str) -> str:
        lines = content.splitlines(keepends=True)
        removing = False
        new_lines = []
        for line in lines:
            if removing and "- repo:" in line:
                removing = False
            if repo_to_remove in line:
                removing = True
            if not removing:
                new_lines.append(line)
        return "".join(new_lines)

    return modifier


def generate_random_string(
    length: int,
    using_digits: bool = False,
    using_ascii_letters: bool = False,
    using_punctuation: bool = False,
) -> str | None:
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def generate_random_user() -> str:
    result = generate_random_string(length=32, using_ascii_letters=True)
    assert result is not None
    return result


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
SUCCESS = "\x1b[1;32m [SUCCESS]: "
