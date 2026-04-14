from pathlib import Path

from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("editor", "Handle editor-specific files")
class EditorStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return not context.equals("editor", "PyCharm")

    def plan(self, context: ExecutionContext) -> list:
        actions = []

        idea_dir_path = Path(".idea")
        if idea_dir_path.exists():
            actions.append(
                DeleteDirectoryAction(
                    dir_path=idea_dir_path,
                    description="Remove PyCharm .idea directory",
                )
            )

        docs_dir_path = Path("docs", "pycharm")
        if docs_dir_path.exists():
            actions.append(
                DeleteDirectoryAction(
                    dir_path=docs_dir_path,
                    description="Remove PyCharm documentation",
                )
            )

        return actions
