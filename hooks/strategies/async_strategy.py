from pathlib import Path

from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("async", "Handle async configuration files")
class AsyncStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return not context.is_enabled("use_async")

    def plan(self, context: ExecutionContext) -> list:
        return [
            DeleteFileAction(
                file_path=Path("config", "asgi.py"),
                description="Remove ASGI config (sync mode)",
            ),
            DeleteFileAction(
                file_path=Path("config", "websocket.py"),
                description="Remove websocket config (sync mode)",
            ),
        ]
