from __future__ import annotations

import dataclasses
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hooks.core.actions import Action
from hooks.core.actions import ActionResult
from hooks.core.audit import AuditEntry
from hooks.core.context import Checkpoint
from hooks.core.context import ExecutionContext
from hooks.core.context import FailurePolicy


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
SUCCESS = "\x1b[1;32m [SUCCESS]: "
ERROR = "\x1b[1;31m [ERROR]: "


@dataclass
class ExecutionResult:
    success: bool
    message: str
    rolled_back_count: int = 0
    failed_actions: list[str] = dataclasses.field(default_factory=list)

    def __bool__(self) -> bool:
        return self.success


class ActionExecutor:
    def __init__(self, context: ExecutionContext):
        self.context = context

    def execute(self, actions: list[Action]) -> ExecutionResult:
        if not actions:
            return ExecutionResult(success=True, message="No actions to execute")

        print(f"{INFO}Planning {len(actions)} actions...{TERMINATOR}")

        if self.context.dry_run:
            return self._dry_run(actions)

        return self._execute_with_policy(actions)

    def _dry_run(self, actions: list[Action]) -> ExecutionResult:
        print(f"{INFO}Dry-run mode: simulating {len(actions)} actions{TERMINATOR}")

        for i, action in enumerate(actions, 1):
            print(f"  [{i}/{len(actions)}] {action.describe()}")

        return ExecutionResult(
            success=True,
            message=f"Dry-run complete: {len(actions)} actions would be executed",
        )

    def _execute_with_policy(self, actions: list[Action]) -> ExecutionResult:
        failed_actions: list[str] = []
        last_successful_idx = -1

        for i, action in enumerate(actions):
            result = self._execute_single(action)

            if not result.success:
                failed_actions.append(action.describe())

                if self.context.failure_policy == FailurePolicy.STOP_IMMEDIATELY:
                    print(f"{ERROR}Action failed: {action.describe()}{TERMINATOR}")
                    print(f"{ERROR}{result.error}{TERMINATOR}")
                    return ExecutionResult(
                        success=False,
                        message=f"Execution stopped at action {i + 1}/{len(actions)}",
                        failed_actions=failed_actions,
                    )

                if self.context.failure_policy == FailurePolicy.ROLLBACK_ALL:
                    print(f"{ERROR}Action failed, rolling back all changes...{TERMINATOR}")
                    rolled_back = self._rollback_all()
                    return ExecutionResult(
                        success=False,
                        message=f"Execution failed, rolled back {rolled_back} actions",
                        rolled_back_count=rolled_back,
                        failed_actions=failed_actions,
                    )

                if self.context.failure_policy == FailurePolicy.ROLLBACK_FAILED:
                    print(f"{WARNING}Action failed, continuing...{TERMINATOR}")
            else:
                last_successful_idx = i

        if failed_actions:
            if self.context.failure_policy == FailurePolicy.CONTINUE_ON_ERROR:
                print(f"{WARNING}{len(failed_actions)} actions failed but execution continued{TERMINATOR}")
                return ExecutionResult(
                    success=True,
                    message=f"Completed with {len(failed_actions)} failures",
                    failed_actions=failed_actions,
                )

        return ExecutionResult(
            success=True,
            message=f"All {len(actions)} actions executed successfully",
        )

    def _execute_single(self, action: Action) -> ActionResult:
        entry = self.context.audit_logger.log_action(action)

        print(f"{INFO}Executing: {action.describe()}{TERMINATOR}")
        result = action.execute(dry_run=False)

        self.context.audit_logger.log_result(entry, result)

        if result.success and result.backup_data is not None:
            self.context.create_checkpoint(entry, result.backup_data)
            self.context.mark_success(entry.sequence_number)

        return result

    def _rollback_all(self) -> int:
        checkpoints = self.context.get_checkpoints_for_rollback()
        rolled_back = 0

        print(f"{INFO}Rolling back {len(checkpoints)} actions...{TERMINATOR}")

        for checkpoint in checkpoints:
            rollback_result = checkpoint.entry.action.rollback(checkpoint.backup_data)

            if rollback_result.success:
                self.context.audit_logger.log_rollback(checkpoint.entry, rollback_result)
                rolled_back += 1
                print(f"  ↩️ Rolled back: {checkpoint.entry.action.describe()}")
            else:
                print(f"{WARNING}Failed to rollback: {checkpoint.entry.action.describe()}{TERMINATOR}")

        return rolled_back

    def rollback_from(self, sequence_number: int) -> int:
        checkpoints = [
            cp
            for cp in self.context.checkpoints
            if cp.sequence_number >= sequence_number
        ]
        rolled_back = 0

        for checkpoint in reversed(checkpoints):
            if checkpoint.backup_data is not None:
                rollback_result = checkpoint.entry.action.rollback(checkpoint.backup_data)
                if rollback_result.success:
                    self.context.audit_logger.log_rollback(checkpoint.entry, rollback_result)
                    rolled_back += 1

        return rolled_back


class ResumableExecutor(ActionExecutor):
    def __init__(self, context: ExecutionContext, state_file: str = ".generation_state.json"):
        super().__init__(context)
        self.state_file = state_file

    def save_state(self, last_sequence: int) -> None:
        import json

        state = {
            "last_successful_checkpoint": last_sequence,
            "project_slug": self.context.project_slug,
            "checkpoints": [
                {
                    "sequence_number": cp.sequence_number,
                    "action": cp.entry.action.to_dict(),
                }
                for cp in self.context.checkpoints
            ],
        }
        Path(self.state_file).write_text(json.dumps(state, indent=2))

    def load_state(self) -> dict[str, Any] | None:
        import json

        state_path = Path(self.state_file)
        if state_path.exists():
            return json.loads(state_path.read_text())
        return None

    def can_resume(self) -> bool:
        state = self.load_state()
        return state is not None and state.get("last_successful_checkpoint", 0) > 0

    def resume(self, actions: list[Action]) -> ExecutionResult:
        state = self.load_state()
        if not state:
            return self.execute(actions)

        last_checkpoint = state.get("last_successful_checkpoint", 0)
        remaining_actions = actions[last_checkpoint:]

        if not remaining_actions:
            print(f"{SUCCESS}Generation already complete, nothing to resume{TERMINATOR}")
            return ExecutionResult(success=True, message="Generation already complete")

        print(f"{INFO}Resuming from checkpoint {last_checkpoint}, {len(remaining_actions)} actions remaining{TERMINATOR}")
        return self._execute_with_policy(remaining_actions)
