from __future__ import annotations

import json
import shutil
import subprocess
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ActionType(Enum):
    DELETE_FILE = "delete_file"
    DELETE_DIRECTORY = "delete_directory"
    CREATE_DIRECTORY = "create_directory"
    MODIFY_FILE = "modify_file"
    APPEND_FILE = "append_file"
    RUN_COMMAND = "run_command"


@dataclass
class ActionResult:
    success: bool
    message: str = ""
    error: str | None = None
    backup_data: Any = None
    timestamp: datetime = field(default_factory=datetime.now)


class Action(ABC):
    action_type: ActionType
    description: str = ""

    @abstractmethod
    def execute(self, dry_run: bool = False) -> ActionResult:
        pass

    @abstractmethod
    def rollback(self, backup_data: Any = None) -> ActionResult:
        pass

    def describe(self) -> str:
        return self.description or f"{self.action_type.value}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.action_type.value,
            "description": self.description,
        }


@dataclass
class DeleteFileAction(Action):
    file_path: Path
    description: str = ""
    action_type: ActionType = field(default=ActionType.DELETE_FILE, init=False)

    def __post_init__(self):
        if not self.description:
            self.description = f"Delete file: {self.file_path}"

    def execute(self, dry_run: bool = False) -> ActionResult:
        if not self.file_path.exists():
            return ActionResult(
                success=True,
                message=f"File {self.file_path} does not exist, skipping",
            )

        backup_data = None
        if not dry_run:
            backup_data = self.file_path.read_bytes()
            self.file_path.unlink()

        return ActionResult(
            success=True,
            message=f"{'[DRY-RUN] ' if dry_run else ''}Deleted file: {self.file_path}",
            backup_data=backup_data,
        )

    def rollback(self, backup_data: bytes | None = None) -> ActionResult:
        if backup_data is None:
            return ActionResult(
                success=True,
                message=f"No backup data for {self.file_path}, skipping rollback",
            )

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_bytes(backup_data)
            return ActionResult(
                success=True,
                message=f"Restored file: {self.file_path}",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                error=str(e),
                message=f"Failed to restore file: {self.file_path}",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "file_path": str(self.file_path),
        }


@dataclass
class DeleteDirectoryAction(Action):
    dir_path: Path
    description: str = ""
    action_type: ActionType = field(default=ActionType.DELETE_DIRECTORY, init=False)

    def __post_init__(self):
        if not self.description:
            self.description = f"Delete directory: {self.dir_path}"

    def execute(self, dry_run: bool = False) -> ActionResult:
        if not self.dir_path.exists():
            return ActionResult(
                success=True,
                message=f"Directory {self.dir_path} does not exist, skipping",
            )

        backup_data = None
        if not dry_run:
            import tempfile

            with tempfile.NamedTemporaryFile(delete=False, suffix=".tar") as tmp:
                backup_path = Path(tmp.name)
            shutil.make_archive(str(backup_path.with_suffix("")), "tar", self.dir_path)
            backup_data = backup_path.with_suffix(".tar").read_bytes()
            backup_path.with_suffix(".tar").unlink()
            shutil.rmtree(self.dir_path)

        return ActionResult(
            success=True,
            message=f"{'[DRY-RUN] ' if dry_run else ''}Deleted directory: {self.dir_path}",
            backup_data=backup_data,
        )

    def rollback(self, backup_data: bytes | None = None) -> ActionResult:
        if backup_data is None:
            return ActionResult(
                success=True,
                message=f"No backup data for {self.dir_path}, skipping rollback",
            )

        try:
            import tempfile

            with tempfile.NamedTemporaryFile(delete=False, suffix=".tar") as tmp:
                tmp.write(backup_data)
                backup_path = Path(tmp.name)

            shutil.unpack_archive(str(backup_path), self.dir_path.parent)
            backup_path.unlink()
            return ActionResult(
                success=True,
                message=f"Restored directory: {self.dir_path}",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                error=str(e),
                message=f"Failed to restore directory: {self.dir_path}",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "dir_path": str(self.dir_path),
        }


@dataclass
class CreateDirectoryAction(Action):
    dir_path: Path
    description: str = ""
    action_type: ActionType = field(default=ActionType.CREATE_DIRECTORY, init=False)

    def __post_init__(self):
        if not self.description:
            self.description = f"Create directory: {self.dir_path}"

    def execute(self, dry_run: bool = False) -> ActionResult:
        if self.dir_path.exists():
            return ActionResult(
                success=True,
                message=f"Directory {self.dir_path} already exists, skipping",
            )

        if not dry_run:
            self.dir_path.mkdir(parents=True, exist_ok=True)

        return ActionResult(
            success=True,
            message=f"{'[DRY-RUN] ' if dry_run else ''}Created directory: {self.dir_path}",
        )

    def rollback(self, backup_data: Any = None) -> ActionResult:
        try:
            if self.dir_path.exists():
                shutil.rmtree(self.dir_path)
            return ActionResult(
                success=True,
                message=f"Removed directory: {self.dir_path}",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                error=str(e),
                message=f"Failed to remove directory: {self.dir_path}",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "dir_path": str(self.dir_path),
        }


@dataclass
class ModifyFileAction(Action):
    file_path: Path
    modifications: dict[str, str]
    description: str = ""
    action_type: ActionType = field(default=ActionType.MODIFY_FILE, init=False)

    def __post_init__(self):
        if not self.description:
            self.description = f"Modify file: {self.file_path}"

    def execute(self, dry_run: bool = False) -> ActionResult:
        if not self.file_path.exists():
            return ActionResult(
                success=False,
                error=f"File {self.file_path} does not exist",
            )

        backup_data = None
        if not dry_run:
            backup_data = self.file_path.read_text()
            content = backup_data
            for old_str, new_str in self.modifications.items():
                content = content.replace(old_str, new_str)
            self.file_path.write_text(content)

        return ActionResult(
            success=True,
            message=f"{'[DRY-RUN] ' if dry_run else ''}Modified file: {self.file_path}",
            backup_data=backup_data,
        )

    def rollback(self, backup_data: str | None = None) -> ActionResult:
        if backup_data is None:
            return ActionResult(
                success=True,
                message=f"No backup data for {self.file_path}, skipping rollback",
            )

        try:
            self.file_path.write_text(backup_data)
            return ActionResult(
                success=True,
                message=f"Restored file content: {self.file_path}",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                error=str(e),
                message=f"Failed to restore file: {self.file_path}",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "file_path": str(self.file_path),
            "modifications": self.modifications,
        }


@dataclass
class AppendFileAction(Action):
    file_path: Path
    content: str
    description: str = ""
    action_type: ActionType = field(default=ActionType.APPEND_FILE, init=False)

    def __post_init__(self):
        if not self.description:
            self.description = f"Append to file: {self.file_path}"

    def execute(self, dry_run: bool = False) -> ActionResult:
        backup_data = None
        if self.file_path.exists():
            backup_data = self.file_path.read_text()

        if not dry_run:
            with self.file_path.open("a") as f:
                f.write(self.content)
                if not self.content.endswith("\n"):
                    f.write("\n")

        return ActionResult(
            success=True,
            message=f"{'[DRY-RUN] ' if dry_run else ''}Appended to file: {self.file_path}",
            backup_data=backup_data,
        )

    def rollback(self, backup_data: str | None = None) -> ActionResult:
        try:
            if backup_data is None:
                if self.file_path.exists():
                    self.file_path.unlink()
            else:
                self.file_path.write_text(backup_data)
            return ActionResult(
                success=True,
                message=f"Restored file: {self.file_path}",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                error=str(e),
                message=f"Failed to restore file: {self.file_path}",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "file_path": str(self.file_path),
            "content": self.content,
        }


@dataclass
class RunCommandAction(Action):
    command: list[str]
    cwd: Path | None = None
    env: dict[str, str] | None = None
    description: str = ""
    action_type: ActionType = field(default=ActionType.RUN_COMMAND, init=False)

    def __post_init__(self):
        if not self.description:
            self.description = f"Run command: {' '.join(self.command)}"

    def execute(self, dry_run: bool = False) -> ActionResult:
        if dry_run:
            return ActionResult(
                success=True,
                message=f"[DRY-RUN] Would run: {' '.join(self.command)}",
            )

        try:
            result = subprocess.run(
                self.command,
                capture_output=True,
                text=True,
                cwd=str(self.cwd) if self.cwd else None,
                env={**dict(__import__("os").environ), **(self.env or {})},
                check=True,
            )
            return ActionResult(
                success=True,
                message=f"Command executed: {' '.join(self.command)}",
                backup_data={"stdout": result.stdout, "stderr": result.stderr},
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                error=f"Command failed with code {e.returncode}: {e.stderr}",
                message=f"Failed to run: {' '.join(self.command)}",
            )

    def rollback(self, backup_data: Any = None) -> ActionResult:
        return ActionResult(
            success=True,
            message="Command actions cannot be rolled back automatically",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "command": self.command,
            "cwd": str(self.cwd) if self.cwd else None,
        }


@dataclass
class ModifyJsonFileAction(Action):
    file_path: Path
    remove_dev_deps: list[str] = field(default_factory=list)
    remove_keys: list[str] = field(default_factory=list)
    update_scripts: dict[str, str] = field(default_factory=dict)
    description: str = ""
    action_type: ActionType = field(default=ActionType.MODIFY_FILE, init=False)

    def __post_init__(self):
        if not self.description:
            self.description = f"Modify JSON file: {self.file_path}"

    def execute(self, dry_run: bool = False) -> ActionResult:
        if not self.file_path.exists():
            return ActionResult(
                success=False,
                error=f"File {self.file_path} does not exist",
            )

        backup_data = None
        if not dry_run:
            backup_data = self.file_path.read_text()
            content = json.loads(backup_data)

            for package_name in self.remove_dev_deps:
                content.get("devDependencies", {}).pop(package_name, None)

            for key in self.remove_keys:
                content.pop(key, None)

            content.get("scripts", {}).update(self.update_scripts)

            updated_content = json.dumps(content, ensure_ascii=False, indent=2) + "\n"
            self.file_path.write_text(updated_content)

        return ActionResult(
            success=True,
            message=f"{'[DRY-RUN] ' if dry_run else ''}Modified JSON file: {self.file_path}",
            backup_data=backup_data,
        )

    def rollback(self, backup_data: str | None = None) -> ActionResult:
        if backup_data is None:
            return ActionResult(
                success=True,
                message=f"No backup data for {self.file_path}, skipping rollback",
            )

        try:
            self.file_path.write_text(backup_data)
            return ActionResult(
                success=True,
                message=f"Restored JSON file: {self.file_path}",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                error=str(e),
                message=f"Failed to restore JSON file: {self.file_path}",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "file_path": str(self.file_path),
            "remove_dev_deps": self.remove_dev_deps,
            "remove_keys": self.remove_keys,
            "update_scripts": self.update_scripts,
        }
