from pathlib import Path

from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.actions import ModifyJsonFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("frontend_pipeline", "Handle frontend pipeline configuration")
class FrontendPipelineStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list:
        pipeline = context.get_config("frontend_pipeline", "None")
        use_docker = context.is_enabled("use_docker")
        use_async = context.is_enabled("use_async")

        if pipeline in ["None", "Django Compressor"]:
            return self._plan_no_frontend(use_docker)
        return self._plan_frontend_pipeline(pipeline, use_docker, use_async)

    def _plan_no_frontend(self, use_docker: bool) -> list:
        actions = []

        actions.append(
            DeleteFileAction(
                file_path=Path("gulpfile.mjs"),
                description="Remove Gulp file",
            ),
        )

        actions.append(
            DeleteDirectoryAction(
                dir_path=Path("webpack"),
                description="Remove webpack directory",
            ),
        )

        vendors_js_path = Path("{{ cookiecutter.project_slug }}", "static", "js", "vendors.js")
        if vendors_js_path.exists():
            actions.append(
                DeleteFileAction(
                    file_path=vendors_js_path,
                    description="Remove vendors.js",
                ),
            )

        actions.append(
            DeleteDirectoryAction(
                dir_path=Path("{{cookiecutter.project_slug}}", "static", "sass"),
                description="Remove Sass directory",
            ),
        )

        actions.append(
            DeleteFileAction(
                file_path=Path("package.json"),
                description="Remove package.json",
            ),
        )

        actions.append(
            DeleteFileAction(
                file_path=Path(".pre-commit-config.yaml"),
                description="Remove prettier pre-commit (placeholder)",
            ),
        )

        if use_docker:
            actions.append(
                DeleteDirectoryAction(
                    dir_path=Path("compose", "local", "node"),
                    description="Remove Node Dockerfile",
                ),
            )

        return actions

    def _plan_frontend_pipeline(self, pipeline: str, use_docker: bool, use_async: bool) -> list:
        actions = []

        project_css_path = Path("{{ cookiecutter.project_slug }}", "static", "css", "project.css")
        if project_css_path.exists():
            actions.append(
                DeleteFileAction(
                    file_path=project_css_path,
                    description="Remove project.css",
                ),
            )

        if pipeline == "Gulp":
            actions.extend(self._plan_gulp(use_docker, use_async))
        elif pipeline == "Webpack":
            actions.extend(self._plan_webpack(use_docker, use_async))

        return actions

    def _plan_gulp(self, use_docker: bool, use_async: bool) -> list:
        actions = []

        actions.append(
            DeleteDirectoryAction(
                dir_path=Path("webpack"),
                description="Remove webpack directory (Gulp mode)",
            ),
        )

        actions.append(
            ModifyJsonFileAction(
                file_path=Path("package.json"),
                remove_dev_deps=[
                    "@babel/core",
                    "@babel/preset-env",
                    "babel-loader",
                    "concurrently",
                    "css-loader",
                    "mini-css-extract-plugin",
                    "postcss-loader",
                    "postcss-preset-env",
                    "sass-loader",
                    "webpack",
                    "webpack-bundle-tracker",
                    "webpack-cli",
                    "webpack-dev-server",
                    "webpack-merge",
                ],
                remove_keys=["babel"],
                update_scripts={
                    "dev": "gulp",
                    "build": "gulp build",
                },
                description="Update package.json for Gulp",
            ),
        )

        return actions

    def _plan_webpack(self, use_docker: bool, use_async: bool) -> list:
        actions = []

        actions.append(
            DeleteFileAction(
                file_path=Path("gulpfile.mjs"),
                description="Remove Gulp file (Webpack mode)",
            ),
        )

        remove_dev_deps = [
            "browser-sync",
            "cssnano",
            "gulp",
            "gulp-concat",
            "gulp-imagemin",
            "gulp-plumber",
            "gulp-postcss",
            "gulp-rename",
            "gulp-sass",
            "gulp-uglify-es",
        ]

        scripts = {
            "dev": "webpack serve --config webpack/dev.config.js",
            "build": "webpack --config webpack/prod.config.js",
        }

        if not use_docker:
            dev_django_cmd = (
                "uvicorn config.asgi:application --reload" if use_async else "python manage.py runserver_plus"
            )
            scripts.update(
                {
                    "dev": "concurrently npm:dev:*",
                    "dev:webpack": "webpack serve --config webpack/dev.config.js",
                    "dev:django": dev_django_cmd,
                },
            )
        else:
            remove_dev_deps.append("concurrently")

        actions.append(
            ModifyJsonFileAction(
                file_path=Path("package.json"),
                remove_dev_deps=remove_dev_deps,
                update_scripts=scripts,
                description="Update package.json for Webpack",
            ),
        )

        return actions
