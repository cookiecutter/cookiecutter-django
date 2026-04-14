from pathlib import Path

from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("username_type", "Handle username type configuration")
class UsernameTypeStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return context.equals("username_type", "username")

    def plan(self, context: ExecutionContext) -> list[DeleteFileAction]:
        project_slug = context.project_slug
        users_path = Path(project_slug) / "users"

        return [
            DeleteFileAction(
                file_path=users_path / "managers.py",
                description="Remove custom user manager (username mode)",
            ),
            DeleteFileAction(
                file_path=users_path / "tests" / "test_managers.py",
                description="Remove user manager tests (username mode)",
            ),
        ]
