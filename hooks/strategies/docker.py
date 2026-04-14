from pathlib import Path

from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("docker", "Handle Docker configuration files")
class DockerStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list:
        actions = []
        use_docker = context.is_enabled("use_docker")

        if use_docker:
            actions.extend(self._plan_docker_enabled(context))
        else:
            actions.extend(self._plan_docker_disabled(context))

        return actions

    def _plan_docker_enabled(self, context: ExecutionContext) -> list:
        actions = []

        actions.append(
            DeleteDirectoryAction(
                dir_path=Path("utility"),
                description="Remove utility directory (Docker mode)",
            )
        )

        cloud_provider = context.get_config("cloud_provider", "")
        if cloud_provider.lower() != "none":
            actions.append(
                DeleteDirectoryAction(
                    dir_path=Path("compose", "production", "nginx"),
                    description="Remove nginx Docker files (cloud provider selected)",
                )
            )

        if cloud_provider != "AWS":
            actions.append(
                DeleteDirectoryAction(
                    dir_path=Path("compose", "production", "aws"),
                    description="Remove AWS Docker files (non-AWS provider)",
                )
            )

        return actions

    def _plan_docker_disabled(self, context: ExecutionContext) -> list:
        actions = []

        actions.append(
            DeleteDirectoryAction(
                dir_path=Path(".devcontainer"),
                description="Remove devcontainer directory",
            )
        )
        actions.append(
            DeleteDirectoryAction(
                dir_path=Path("compose"),
                description="Remove compose directory",
            )
        )

        for file_name in [
            "docker-compose.local.yml",
            "docker-compose.production.yml",
            ".dockerignore",
            "justfile",
        ]:
            actions.append(
                DeleteFileAction(
                    file_path=Path(file_name),
                    description=f"Remove Docker file: {file_name}",
                )
            )

        if context.equals("editor", "PyCharm"):
            for file_name in ["docker_compose_up_django.xml", "docker_compose_up_docs.xml"]:
                actions.append(
                    DeleteFileAction(
                        file_path=Path(".idea", "runConfigurations", file_name),
                        description=f"Remove PyCharm Docker run config: {file_name}",
                    )
                )

        return actions
