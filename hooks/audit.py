"""
审计日志模块 - 记录所有操作并提供变更报告

支持操作追踪、变更清单生成、以及回滚能力。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any

from hooks.operations import Operation, OperationType


class OperationStatus(Enum):
    """操作执行状态"""
    PENDING = auto()      # 待执行
    EXECUTING = auto()    # 执行中
    SUCCESS = auto()      # 成功
    FAILED = auto()       # 失败
    ROLLED_BACK = auto()  # 已回滚
    SKIPPED = auto()      # 已跳过


@dataclass
class AuditEntry:
    """
    审计条目 - 记录单个操作的完整生命周期
    """
    operation: Operation
    sequence_number: int
    timestamp_start: datetime | None = None
    timestamp_end: datetime | None = None
    status: OperationStatus = OperationStatus.PENDING
    result: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None
    rollback_data: dict[str, Any] | None = None
    
    def mark_started(self) -> None:
        """标记操作开始"""
        self.timestamp_start = datetime.now()
        self.status = OperationStatus.EXECUTING
    
    def mark_success(self, result: dict[str, Any]) -> None:
        """标记操作成功"""
        self.timestamp_end = datetime.now()
        self.status = OperationStatus.SUCCESS
        self.result = result
        # 保存回滚所需数据
        self.rollback_data = result.get("backup_data") or result
    
    def mark_failed(self, error: Exception) -> None:
        """标记操作失败"""
        self.timestamp_end = datetime.now()
        self.status = OperationStatus.FAILED
        self.error_message = str(error)
    
    def mark_rolled_back(self) -> None:
        """标记已回滚"""
        self.status = OperationStatus.ROLLED_BACK
    
    def mark_skipped(self, reason: str = "") -> None:
        """标记已跳过"""
        self.timestamp_end = datetime.now()
        self.status = OperationStatus.SKIPPED
        self.error_message = reason
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            "sequence_number": self.sequence_number,
            "operation": self.operation.to_dict(),
            "status": self.status.name,
            "timestamp_start": self.timestamp_start.isoformat() if self.timestamp_start else None,
            "timestamp_end": self.timestamp_end.isoformat() if self.timestamp_end else None,
            "duration_ms": self._get_duration_ms(),
            "result": self.result,
            "error_message": self.error_message,
        }
    
    def _get_duration_ms(self) -> int | None:
        """获取执行耗时（毫秒）"""
        if self.timestamp_start and self.timestamp_end:
            delta = self.timestamp_end - self.timestamp_start
            return int(delta.total_seconds() * 1000)
        return None


class AuditLog:
    """
    审计日志 - 管理所有操作的审计记录
    
    提供：
    - 操作记录
    - 变更清单报告
    - 回滚支持
    """
    
    def __init__(self) -> None:
        self.entries: list[AuditEntry] = []
        self._sequence_counter = 0
        self.session_start = datetime.now()
    
    def record_operation(self, operation: Operation) -> AuditEntry:
        """
        记录一个新操作
        
        Args:
            operation: 要记录的操作
            
        Returns:
            创建的审计条目
        """
        self._sequence_counter += 1
        entry = AuditEntry(
            operation=operation,
            sequence_number=self._sequence_counter,
        )
        self.entries.append(entry)
        return entry
    
    def get_entries_by_status(self, status: OperationStatus) -> list[AuditEntry]:
        """按状态获取条目"""
        return [e for e in self.entries if e.status == status]
    
    def get_entries_by_type(self, op_type: OperationType) -> list[AuditEntry]:
        """按操作类型获取条目"""
        return [e for e in self.entries if e.operation.operation_type == op_type]
    
    def get_successful_entries(self) -> list[AuditEntry]:
        """获取所有成功执行的条目（可用于回滚）"""
        return [e for e in self.entries if e.status == OperationStatus.SUCCESS]
    
    def get_entries_for_rollback(self) -> list[AuditEntry]:
        """
        获取需要回滚的条目（按逆序）
        
        返回成功执行的条目，按执行顺序的逆序排列，
        以便按正确顺序回滚。
        """
        successful = self.get_successful_entries()
        return list(reversed(successful))
    
    def generate_report(self) -> dict[str, Any]:
        """
        生成变更清单报告
        
        Returns:
            包含统计信息和详细变更列表的字典
        """
        total = len(self.entries)
        successful = len(self.get_entries_by_status(OperationStatus.SUCCESS))
        failed = len(self.get_entries_by_status(OperationStatus.FAILED))
        skipped = len(self.get_entries_by_status(OperationStatus.SKIPPED))
        rolled_back = len(self.get_entries_by_status(OperationStatus.ROLLED_BACK))
        
        # 按类型统计
        by_type = {}
        for op_type in OperationType:
            count = len(self.get_entries_by_type(op_type))
            if count > 0:
                by_type[op_type.name] = count
        
        # 详细变更列表
        changes = []
        for entry in self.entries:
            changes.append({
                "sequence": entry.sequence_number,
                "description": entry.operation.describe(),
                "status": entry.status.name,
                "type": entry.operation.operation_type.name,
            })
        
        return {
            "summary": {
                "total_operations": total,
                "successful": successful,
                "failed": failed,
                "skipped": skipped,
                "rolled_back": rolled_back,
                "by_type": by_type,
            },
            "session": {
                "start_time": self.session_start.isoformat(),
                "end_time": datetime.now().isoformat(),
            },
            "changes": changes,
        }
    
    def print_report(self) -> None:
        """打印变更报告到控制台"""
        report = self.generate_report()
        summary = report["summary"]
        
        print("\n" + "=" * 60)
        print("变更清单报告")
        print("=" * 60)
        print(f"总操作数: {summary['total_operations']}")
        print(f"  - 成功: {summary['successful']}")
        print(f"  - 失败: {summary['failed']}")
        print(f"  - 跳过: {summary['skipped']}")
        print(f"  - 已回滚: {summary['rolled_back']}")
        print("\n按类型统计:")
        for op_type, count in summary["by_type"].items():
            print(f"  - {op_type}: {count}")
        
        print("\n详细变更列表:")
        for change in report["changes"]:
            status_icon = {
                "SUCCESS": "✓",
                "FAILED": "✗",
                "SKIPPED": "○",
                "ROLLED_BACK": "↺",
                "PENDING": "…",
                "EXECUTING": "►",
            }.get(change["status"], "?")
            print(f"  {status_icon} [{change['sequence']:3d}] {change['description']}")
        
        print("=" * 60)
    
    def save_to_file(self, path: Path | str) -> None:
        """保存审计日志到文件"""
        path = Path(path)
        report = self.generate_report()
        
        # 添加完整的条目详情
        full_data = {
            "report": report,
            "entries": [e.to_dict() for e in self.entries],
        }
        
        path.write_text(json.dumps(full_data, indent=2, ensure_ascii=False))
    
    def load_from_file(self, path: Path | str) -> None:
        """从文件加载审计日志（用于恢复会话）"""
        import json
        from datetime import datetime
        
        path = Path(path)
        if not path.exists():
            return
            
        data = json.loads(path.read_text())
        
        # 从加载的数据中重建条目
        if "entries" in data:
            for entry_data in data["entries"]:
                # 创建简化的审计条目，只包含状态和序列号
                # 注意：这里不重建完整的 Operation 对象，只记录状态信息
                self._sequence_counter = max(
                    self._sequence_counter,
                    entry_data.get("sequence_number", 0)
                )
                
                # 存储条目数据供后续查询
                self.entries.append(
                    _LoadedAuditEntry(
                        sequence_number=entry_data.get("sequence_number", 0),
                        status=OperationStatus[entry_data.get("status", "PENDING")],
                        operation_type=entry_data.get("operation", {}).get("type", "UNKNOWN"),
                        description=entry_data.get("operation", {}).get("description", ""),
                    )
                )


class _LoadedAuditEntry:
    """用于从文件加载的简化审计条目"""
    
    def __init__(
        self,
        sequence_number: int,
        status: OperationStatus,
        operation_type: str,
        description: str,
    ) -> None:
        self.sequence_number = sequence_number
        self.status = status
        self.operation_type = operation_type
        self.description = description
        self.operation = _LoadedOperation(operation_type, description)


class _LoadedOperation:
    """用于从文件加载的简化操作"""
    
    def __init__(self, operation_type: str, description: str) -> None:
        self._operation_type = operation_type
        self._description = description
    
    @property
    def operation_type(self):
        return self._operation_type
    
    def describe(self) -> str:
        return self._description
