"""
执行器模块 - 支持多种执行模式

提供真实执行、模拟执行、仅记录日志等多种执行模式，
业务逻辑只声明"要做什么"，不关心具体如何执行。
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from enum import Enum
from enum import auto
from pathlib import Path
from typing import Any

from hooks.audit import AuditEntry
from hooks.audit import AuditLog
from hooks.audit import OperationStatus
from hooks.operations import FailureStrategy
from hooks.operations import Operation


class ExecutionMode(Enum):
    """执行模式"""

    REAL = auto()  # 真实执行
    DRY_RUN = auto()  # 模拟执行（只打印，不实际执行）
    LOG_ONLY = auto()  # 仅记录日志


class Executor(ABC):
    """
    执行器抽象基类

    定义执行器的接口，所有具体执行器都继承此类。
    """

    def __init__(self, audit_log: AuditLog | None = None) -> None:
        self.audit_log = audit_log or AuditLog()
        self.errors: list[tuple[Operation, Exception]] = []

    @abstractmethod
    def execute(self, operation: Operation) -> dict[str, Any]:
        """执行单个操作"""

    def execute_all(self, operations: list[Operation]) -> list[AuditEntry]:
        """
        执行所有操作

        Args:
            operations: 要执行的操作列表

        Returns:
            所有审计条目
        """
        entries = []
        for op in operations:
            entry = self.execute(op)
            entries.append(entry)
        return entries


class RealExecutor(Executor):
    """
    真实执行器 - 实际执行所有操作

    支持失败处理和回滚机制。
    """

    def __init__(
        self,
        audit_log: AuditLog | None = None,
        auto_rollback: bool = True,
    ) -> None:
        super().__init__(audit_log)
        self.auto_rollback = auto_rollback
        self.executed_entries: list[AuditEntry] = []

    def execute(self, operation: Operation) -> AuditEntry:
        """
        执行单个操作，支持失败处理和回滚

        Args:
            operation: 要执行的操作

        Returns:
            审计条目
        """
        entry = self.audit_log.record_operation(operation)
        entry.mark_started()

        try:
            result = operation.execute()
            entry.mark_success(result)
            self.executed_entries.append(entry)

            # 如果操作被跳过，也记录下来
            if result.get("skipped"):
                entry.mark_skipped(result.get("reason", ""))

        except Exception as e:
            entry.mark_failed(e)
            self.errors.append((operation, e))

            # 根据失败策略处理
            if operation.failure_strategy == FailureStrategy.STOP:
                if self.auto_rollback:
                    self._rollback_all()
                raise ExecutionError(f"Operation failed: {operation.describe()}", e, entry)
            if operation.failure_strategy == FailureStrategy.SKIP:
                # 继续执行后续操作
                pass
            elif operation.failure_strategy == FailureStrategy.RETRY:
                # 可以实现重试逻辑
                pass

        return entry

    def _rollback_all(self) -> None:
        """回滚所有已执行的操作"""
        print("\n发生错误，开始回滚...")
        for entry in self.audit_log.get_entries_for_rollback():
            try:
                entry.operation.rollback(entry.rollback_data)
                entry.mark_rolled_back()
                print(f"  ↺ 已回滚: {entry.operation.describe()}")
            except Exception as e:
                print(f"  ✗ 回滚失败: {entry.operation.describe()} - {e}")


class DryRunExecutor(Executor):
    """
    模拟执行器 - 只打印操作，不实际执行

    用于预览将要执行的操作。
    """

    def execute(self, operation: Operation) -> AuditEntry:
        """模拟执行操作"""
        entry = self.audit_log.record_operation(operation)
        entry.mark_started()

        # 模拟执行结果
        result = {
            "success": True,
            "dry_run": True,
            "would_execute": True,
        }
        entry.mark_success(result)

        print(f"[DRY-RUN] {operation.describe()}")
        return entry


class LogOnlyExecutor(Executor):
    """
    仅记录执行器 - 只记录到审计日志，不执行也不打印

    用于收集操作列表，后续统一处理。
    """

    def execute(self, operation: Operation) -> AuditEntry:
        """仅记录操作"""
        entry = self.audit_log.record_operation(operation)
        entry.mark_skipped("Log only mode")
        return entry


class TwoPhaseExecutor:
    """
    两阶段执行器 - 实现副作用隔离

    第一阶段：决策阶段，在内存中构建操作列表
    第二阶段：执行阶段，统一执行所有副作用

    两阶段之间可以插入：预览、人工确认、dry-run 等能力
    """

    def __init__(self) -> None:
        self.pending_operations: list[Operation] = []
        self.audit_log = AuditLog()
        self._phase: str = "decision"  # 'decision' 或 'execution'

    def add_operation(self, operation: Operation) -> None:
        """
        添加操作到待执行列表（决策阶段）

        此阶段纯在内存中操作，无副作用。
        """
        if self._phase != "decision":
            raise RuntimeError("Cannot add operations in execution phase")
        self.pending_operations.append(operation)

    def add_operations(self, operations: list[Operation]) -> None:
        """批量添加操作"""
        for op in operations:
            self.add_operation(op)

    def preview(self) -> list[str]:
        """
        预览将要执行的操作

        Returns:
            操作描述列表
        """
        return [op.describe() for op in self.pending_operations]

    def print_preview(self) -> None:
        """打印预览"""
        print("\n" + "=" * 60)
        print("操作预览")
        print("=" * 60)
        for i, desc in enumerate(self.preview(), 1):
            print(f"  {i:3d}. {desc}")
        print(f"\n总计: {len(self.pending_operations)} 个操作")
        print("=" * 60)

    def execute(
        self,
        mode: ExecutionMode = ExecutionMode.REAL,
        auto_rollback: bool = True,
        confirm: bool = False,
    ) -> AuditLog:
        """
        执行所有待执行操作（执行阶段）

        Args:
            mode: 执行模式
            auto_rollback: 失败时是否自动回滚
            confirm: 执行前是否需要确认

        Returns:
            审计日志
        """
        self._phase = "execution"

        # 如果需要确认
        if confirm:
            self.print_preview()
            response = input("\n确认执行以上操作? [y/N]: ")
            if response.lower() != "y":
                print("操作已取消")
                return self.audit_log

        # 选择执行器
        if mode == ExecutionMode.REAL:
            executor: Executor = RealExecutor(self.audit_log, auto_rollback)
        elif mode == ExecutionMode.DRY_RUN:
            executor = DryRunExecutor(self.audit_log)
        elif mode == ExecutionMode.LOG_ONLY:
            executor = LogOnlyExecutor(self.audit_log)
        else:
            raise ValueError(f"Unknown execution mode: {mode}")

        # 执行所有操作
        executor.execute_all(self.pending_operations)

        return self.audit_log

    def get_audit_log(self) -> AuditLog:
        """获取审计日志"""
        return self.audit_log


class ExecutionError(Exception):
    """执行错误"""

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
        entry: AuditEntry | None = None,
    ) -> None:
        super().__init__(message)
        self.original_error = original_error
        self.entry = entry


class ResumableExecutor:
    """
    可恢复执行器 - 支持从中断处继续执行

    通过保存和加载审计日志，实现断点续执行。
    """

    def __init__(self, state_file: Path | str | None = None) -> None:
        self.state_file = Path(state_file) if state_file else None
        self.audit_log = AuditLog()
        self.completed_operations: set[int] = set()

    def save_state(self) -> None:
        """保存当前状态"""
        if self.state_file:
            self.audit_log.save_to_file(self.state_file)

    def load_state(self) -> None:
        """加载之前的状态"""
        if self.state_file and self.state_file.exists():
            self.audit_log.load_from_file(self.state_file)
            # 标记已完成的操作
            for entry in self.audit_log.entries:
                if entry.status == OperationStatus.SUCCESS:
                    self.completed_operations.add(entry.sequence_number)

    def is_completed(self, operation_id: int) -> bool:
        """检查操作是否已完成"""
        return operation_id in self.completed_operations

    def execute_with_resume(
        self,
        operations: list[Operation],
        mode: ExecutionMode = ExecutionMode.REAL,
    ) -> AuditLog:
        """
        执行操作，支持从中断处恢复

        Args:
            operations: 所有操作
            mode: 执行模式

        Returns:
            审计日志
        """
        # 加载之前的状态
        self.load_state()

        executor = TwoPhaseExecutor()

        # 只添加未完成的操作
        for i, op in enumerate(operations, 1):
            if not self.is_completed(i):
                executor.add_operation(op)

        # 执行
        audit_log = executor.execute(mode)

        # 保存状态
        self.save_state()

        return audit_log
