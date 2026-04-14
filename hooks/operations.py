"""
操作抽象模块 - 定义所有可能的操作类型

此模块将"要做什么"与"怎么做"分离，所有操作都是纯数据对象，
可以在内存中构建和组合，最后统一执行。
"""

from __future__ import annotations

import shutil
import subprocess
from abc import ABC
from abc import abstractmethod
from enum import Enum
from enum import auto
from pathlib import Path
from typing import Any


class OperationType(Enum):
    """操作类型枚举"""

    DELETE_FILE = auto()
    DELETE_DIRECTORY = auto()
    MODIFY_FILE = auto()
    APPEND_TO_FILE = auto()
    RUN_COMMAND = auto()
    SET_FLAG = auto()


class FailureStrategy(Enum):
    """失败处理策略"""

    STOP = auto()  # 立即停止，回滚已执行的操作
    SKIP = auto()  # 跳过当前操作，继续执行后续操作
    RETRY = auto()  # 重试当前操作


class Operation(ABC):
    """
    操作基类 - 所有具体操作都继承此类

    不使用 dataclass 继承，而是使用普通类，
    避免 dataclass 字段顺序的限制。
    """

    def __init__(
        self,
        failure_strategy: FailureStrategy = FailureStrategy.STOP,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.failure_strategy = failure_strategy
        self.metadata = metadata or {}

    @property
    @abstractmethod
    def operation_type(self) -> OperationType:
        """操作类型属性"""

    @abstractmethod
    def execute(self) -> Any:
        """执行操作，返回执行结果"""

    @abstractmethod
    def rollback(self, backup_data: dict[str, Any] | None = None) -> None:
        """回滚操作，恢复到执行前状态"""

    @abstractmethod
    def describe(self) -> str:
        """返回人类可读的操作描述"""

    def to_dict(self) -> dict[str, Any]:
        """序列化为字典，用于审计日志"""
        return {
            "type": self.operation_type.name,
            "failure_strategy": self.failure_strategy.name,
            "metadata": self.metadata,
            "description": self.describe(),
        }


class DeleteFileOperation(Operation):
    """删除文件操作"""

    def __init__(
        self,
        file_path: Path,
        failure_strategy: FailureStrategy = FailureStrategy.STOP,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(failure_strategy, metadata)
        self.file_path = file_path

    @property
    def operation_type(self) -> OperationType:
        return OperationType.DELETE_FILE

    def execute(self) -> dict[str, Any]:
        path = Path(self.file_path)
        if not path.exists():
            return {"success": True, "skipped": True, "reason": "File does not exist"}

        # 保存文件内容以便回滚
        content = path.read_bytes()
        path.unlink()
        return {"success": True, "skipped": False, "backed_up_content": content}

    def rollback(self, backup_data: dict[str, Any] | None = None) -> None:
        if backup_data and "backed_up_content" in backup_data:
            path = Path(self.file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(backup_data["backed_up_content"])

    def describe(self) -> str:
        return f"删除文件: {self.file_path}"


class DeleteDirectoryOperation(Operation):
    """删除目录操作"""

    def __init__(
        self,
        dir_path: Path,
        failure_strategy: FailureStrategy = FailureStrategy.STOP,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(failure_strategy, metadata)
        self.dir_path = dir_path

    @property
    def operation_type(self) -> OperationType:
        return OperationType.DELETE_DIRECTORY

    def execute(self) -> dict[str, Any]:
        path = Path(self.dir_path)
        if not path.exists():
            return {"success": True, "skipped": True, "reason": "Directory does not exist"}

        # 创建临时备份目录
        backup_path = path.parent / f"{path.name}.backup"
        if backup_path.exists():
            shutil.rmtree(backup_path)
        shutil.copytree(path, backup_path)
        shutil.rmtree(path)
        return {"success": True, "skipped": False, "backup_path": backup_path}

    def rollback(self, backup_data: dict[str, Any] | None = None) -> None:
        if backup_data and "backup_path" in backup_data:
            backup_path = backup_data["backup_path"]
            target_path = Path(self.dir_path)
            if backup_path.exists():
                if target_path.exists():
                    shutil.rmtree(target_path)
                shutil.copytree(backup_path, target_path)
                shutil.rmtree(backup_path)

    def describe(self) -> str:
        return f"删除目录: {self.dir_path}"


class ModifyFileOperation(Operation):
    """修改文件内容操作"""

    def __init__(
        self,
        file_path: Path,
        modifier: callable,
        failure_strategy: FailureStrategy = FailureStrategy.STOP,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(failure_strategy, metadata)
        self.file_path = file_path
        self.modifier = modifier

    @property
    def operation_type(self) -> OperationType:
        return OperationType.MODIFY_FILE

    def execute(self) -> dict[str, Any]:
        path = Path(self.file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        original_content = path.read_text()
        new_content = self.modifier(original_content)
        path.write_text(new_content)
        return {"success": True, "original_content": original_content}

    def rollback(self, backup_data: dict[str, Any] | None = None) -> None:
        if backup_data and "original_content" in backup_data:
            path = Path(self.file_path)
            path.write_text(backup_data["original_content"])

    def describe(self) -> str:
        return f"修改文件: {self.file_path}"


class AppendToFileOperation(Operation):
    """追加内容到文件操作"""

    def __init__(
        self,
        file_path: Path,
        content: str,
        failure_strategy: FailureStrategy = FailureStrategy.STOP,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(failure_strategy, metadata)
        self.file_path = file_path
        self.content = content

    @property
    def operation_type(self) -> OperationType:
        return OperationType.APPEND_TO_FILE

    def execute(self) -> dict[str, Any]:
        path = Path(self.file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        original_size = path.stat().st_size if path.exists() else 0
        with path.open("a") as f:
            f.write(self.content)
            f.write("\n")

        return {"success": True, "original_size": original_size, "appended": self.content}

    def rollback(self, backup_data: dict[str, Any] | None = None) -> None:
        if backup_data and "original_size" in backup_data:
            path = Path(self.file_path)
            if path.exists():
                content = path.read_text()
                # 移除追加的内容
                appended = backup_data["appended"]
                if content.endswith(appended + "\n"):
                    new_content = content[: -(len(appended) + 1)]
                    path.write_text(new_content)

    def describe(self) -> str:
        return f"追加到文件: {self.file_path}"


class RunCommandOperation(Operation):
    """执行命令操作"""

    def __init__(
        self,
        command: list[str],
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
        failure_strategy: FailureStrategy = FailureStrategy.STOP,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(failure_strategy, metadata)
        self.command = command
        self.cwd = cwd
        self.env = env

    @property
    def operation_type(self) -> OperationType:
        return OperationType.RUN_COMMAND

    def execute(self) -> dict[str, Any]:
        import os

        env_vars = {**os.environ}
        if self.env:
            env_vars.update(self.env)

        result = subprocess.run(
            self.command,
            cwd=self.cwd,
            env=env_vars,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode,
                self.command,
                output=result.stdout,
                stderr=result.stderr,
            )

        return {
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    def rollback(self, backup_data: dict[str, Any] | None = None) -> None:
        # 命令操作通常不可回滚，但可以记录日志
        pass

    def describe(self) -> str:
        cmd_str = " ".join(self.command)
        return f"执行命令: {cmd_str}"


class SetFlagOperation(Operation):
    """设置标志位操作（用于替换文件中的占位符）"""

    def __init__(
        self,
        file_path: Path,
        flag: str,
        value: str | None = None,
        generator: callable | None = None,
        failure_strategy: FailureStrategy = FailureStrategy.STOP,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(failure_strategy, metadata)
        self.file_path = file_path
        self.flag = flag
        self.value = value
        self.generator = generator

    @property
    def operation_type(self) -> OperationType:
        return OperationType.SET_FLAG

    def execute(self) -> dict[str, Any]:
        path = Path(self.file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # 确定要设置的值
        value = self.value
        if value is None and self.generator:
            value = self.generator()

        if value is None:
            raise ValueError(f"No value provided for flag {self.flag}")

        original_content = path.read_text()
        new_content = original_content.replace(self.flag, value)
        path.write_text(new_content)

        return {
            "success": True,
            "original_content": original_content,
            "flag": self.flag,
            "value": value,
        }

    def rollback(self, backup_data: dict[str, Any] | None = None) -> None:
        if backup_data and "original_content" in backup_data:
            path = Path(self.file_path)
            path.write_text(backup_data["original_content"])

    def describe(self) -> str:
        return f"设置标志 {self.flag} 在文件 {self.file_path}"


# 向后兼容的函数
def append_to_gitignore_file(ignored_line: str) -> None:
    """
    向后兼容函数：追加内容到 .gitignore 文件

    这是为了兼容旧的测试代码。
    """
    op = AppendToFileOperation(file_path=Path(".gitignore"), content=ignored_line)
    op.execute()
