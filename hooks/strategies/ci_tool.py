from pathlib import Path

from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("ci_tool", "Handle CI tool configuration files")
class CIToolStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list:
        actions = []
        ci_tool = context.get_config("ci_tool", "None")

        if ci_tool != "Travis":
            actions.append(
                DeleteFileAction(
                    file_path=Path(".travis.yml"),
                    description="Remove Travis CI config",
                )
            )

        if ci_tool != "Gitlab":
            actions.append(
                DeleteFileAction(
                    file_path=Path(".gitlab-ci.yml"),
                    description="Remove GitLab CI config",
                )
            )

        if ci_tool != "Github":
            actions.append(
                DeleteDirectoryAction(
                    dir_path=Path(".github"),
                    description="Remove GitHub Actions config",
                )
            )

        if ci_tool != "Drone":
            actions.append(
                DeleteFileAction(
                    file_path=Path(".drone.yml"),
                    description="Remove Drone CI config",
                )
            )

        return actions
