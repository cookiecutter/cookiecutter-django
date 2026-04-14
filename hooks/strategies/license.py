from pathlib import Path

from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("open_source_license", "Handle open source license file removal")
class OpenSourceLicenseStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        license_value = context.get_config("open_source_license", "")
        return license_value == "Not open source" or license_value != "GPLv3"

    def plan(self, context: ExecutionContext) -> list[DeleteFileAction]:
        actions = []
        license_value = context.get_config("open_source_license", "")

        if license_value == "Not open source":
            for file_name in ["CONTRIBUTORS.txt", "LICENSE"]:
                actions.append(
                    DeleteFileAction(
                        file_path=Path(file_name),
                        description=f"Remove open source file: {file_name}",
                    ),
                )

        if license_value != "GPLv3":
            actions.append(
                DeleteFileAction(
                    file_path=Path("COPYING"),
                    description="Remove GPLv3 license file",
                ),
            )

        return actions
