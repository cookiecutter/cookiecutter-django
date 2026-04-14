from pathlib import Path

from hooks.core.actions import AppendFileAction
from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("heroku", "Handle Heroku deployment files")
class HerokuStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list:
        actions = []
        use_heroku = context.is_enabled("use_heroku")
        use_docker = context.is_enabled("use_docker")

        if not use_heroku:
            actions.extend(self._plan_heroku_disabled(context))

        if use_docker or use_heroku:
            actions.extend(self._plan_env_gitignore(context))

        return actions

    def _plan_heroku_disabled(self, context: ExecutionContext) -> list:
        actions = []
        ci_tool = context.get_config("ci_tool", "")

        for file_name in ["Procfile"]:
            if file_name == "requirements.txt" and ci_tool.lower() == "travis":
                continue
            actions.append(
                DeleteFileAction(
                    file_path=Path(file_name),
                    description=f"Remove Heroku file: {file_name}",
                )
            )

        actions.append(
            DeleteDirectoryAction(
                dir_path=Path("bin"),
                description="Remove Heroku bin directory",
            )
        )

        return actions

    def _plan_env_gitignore(self, context: ExecutionContext) -> list:
        actions = []
        keep_local_envs = context.is_enabled("keep_local_envs_in_vcs")

        actions.append(
            AppendFileAction(
                file_path=Path(".gitignore"),
                content=".env",
                description="Add .env to gitignore",
            )
        )
        actions.append(
            AppendFileAction(
                file_path=Path(".gitignore"),
                content=".envs/*",
                description="Add .envs/* to gitignore",
            )
        )

        if keep_local_envs:
            actions.append(
                AppendFileAction(
                    file_path=Path(".gitignore"),
                    content="!.envs/.local/",
                    description="Keep local envs in VCS",
                )
            )

        return actions
