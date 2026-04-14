from __future__ import annotations

import os
from pathlib import Path

from hooks.core import (
    AppendFileOperation,
    DeleteDirOperation,
    DeleteFileOperation,
    ModifyFileOperation,
    Operation,
    RunCommandOperation,
    SetFlagOperation,
    Strategy,
    remove_repo_from_pre_commit_modifier,
    update_package_json_modifier,
)


PROJECT_SLUG = "{{ cookiecutter.project_slug }}"


class LicenseStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        license_type = context["open_source_license"]
        if license_type == "Not open source":
            operations.append(DeleteFileOperation("CONTRIBUTORS.txt"))
            operations.append(DeleteFileOperation("LICENSE"))
        if license_type != "GPLv3":
            operations.append(DeleteFileOperation("COPYING"))
        return operations


class UsernameTypeStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        if context["username_type"] == "username":
            users_path = Path(PROJECT_SLUG, "users")
            operations.append(DeleteFileOperation(users_path / "managers.py"))
            operations.append(DeleteFileOperation(users_path / "tests" / "test_managers.py"))
        return operations


class EditorStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        if context["editor"] != "PyCharm":
            operations.append(DeleteDirOperation(".idea"))
            operations.append(DeleteDirOperation(Path("docs", "pycharm")))
        return operations


class DockerStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        use_docker = context["use_docker"].lower() == "y"
        cloud_provider = context["cloud_provider"]

        if use_docker:
            operations.append(DeleteDirOperation("utility"))
            if cloud_provider.lower() != "none":
                operations.append(DeleteDirOperation(Path("compose", "production", "nginx")))
        else:
            operations.append(DeleteDirOperation(".devcontainer"))
            operations.append(DeleteDirOperation("compose"))
            docker_files = [
                "docker-compose.local.yml",
                "docker-compose.production.yml",
                ".dockerignore",
                "justfile",
            ]
            for fname in docker_files:
                operations.append(DeleteFileOperation(fname))

        if use_docker and cloud_provider != "AWS":
            operations.append(DeleteDirOperation(Path("compose", "production", "aws")))

        return operations


class HerokuStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        if context["use_heroku"].lower() == "n":
            operations.append(DeleteFileOperation("Procfile"))
            operations.append(DeleteDirOperation("bin"))
        return operations


class EnvsStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        use_docker = context["use_docker"].lower() == "y"
        use_heroku = context["use_heroku"].lower() == "y"
        keep_envs = context["keep_local_envs_in_vcs"].lower() == "y"

        if not use_docker and not use_heroku:
            if not keep_envs:
                operations.append(DeleteDirOperation(".envs"))
                operations.append(DeleteFileOperation("merge_production_dotenvs_in_dotenv.py"))
                operations.append(DeleteDirOperation("tests"))
        else:
            operations.append(AppendFileOperation(".gitignore", ".env"))
            operations.append(AppendFileOperation(".gitignore", ".envs/*"))
            if keep_envs:
                operations.append(AppendFileOperation(".gitignore", "!.envs/.local/"))
        return operations


class FrontendPipelineStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        pipeline = context["frontend_pipeline"]
        use_docker = context["use_docker"].lower() == "y"
        use_async = context["use_async"].lower() == "y"

        static_path = Path(PROJECT_SLUG, "static")

        if pipeline in ["None", "Django Compressor"]:
            operations.append(DeleteFileOperation("gulpfile.mjs"))
            operations.append(DeleteDirOperation("webpack"))
            operations.append(DeleteDirOperation(static_path / "sass"))
            operations.append(DeleteFileOperation("package.json"))
            operations.append(
                ModifyFileOperation(
                    ".pre-commit-config.yaml",
                    remove_repo_from_pre_commit_modifier("mirrors-prettier"),
                ),
            )
            if use_docker:
                operations.append(DeleteDirOperation(Path("compose", "local", "node")))
        else:
            operations.append(DeleteFileOperation(static_path / "css" / "project.css"))
            if pipeline == "Gulp":
                operations.append(
                    ModifyFileOperation(
                        "package.json",
                        update_package_json_modifier(
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
                            scripts={
                                "dev": "gulp",
                                "build": "gulp build",
                            },
                        ),
                    ),
                )
                operations.append(DeleteDirOperation("webpack"))
            elif pipeline == "Webpack":
                scripts = {
                    "dev": "webpack serve --config webpack/dev.config.js",
                    "build": "webpack --config webpack/prod.config.js",
                }
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
                if not use_docker:
                    dev_django_cmd = (
                        "uvicorn config.asgi:application --reload"
                        if use_async
                        else "python manage.py runserver_plus"
                    )
                    scripts.update({
                        "dev": "concurrently npm:dev:*",
                        "dev:webpack": "webpack serve --config webpack/dev.config.js",
                        "dev:django": dev_django_cmd,
                    })
                else:
                    remove_dev_deps.append("concurrently")
                operations.append(
                    ModifyFileOperation(
                        "package.json",
                        update_package_json_modifier(
                            remove_dev_deps=remove_dev_deps,
                            scripts=scripts,
                        ),
                    ),
                )
                operations.append(DeleteFileOperation("gulpfile.mjs"))

        return operations


class CeleryStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        if context["use_celery"].lower() == "n":
            operations.append(DeleteFileOperation(Path("config", "celery_app.py")))
            operations.append(
                DeleteFileOperation(Path(PROJECT_SLUG, "users", "tasks.py")),
            )
            operations.append(
                DeleteFileOperation(Path(PROJECT_SLUG, "users", "tests", "test_tasks.py")),
            )
            if context["use_docker"].lower() == "y":
                operations.append(
                    DeleteDirOperation(Path("compose", "local", "django", "celery")),
                )
                operations.append(
                    DeleteDirOperation(Path("compose", "production", "django", "celery")),
                )
        return operations


class CiToolStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        ci_tool = context["ci_tool"]
        if ci_tool != "Travis":
            operations.append(DeleteFileOperation(".travis.yml"))
        if ci_tool != "Gitlab":
            operations.append(DeleteFileOperation(".gitlab-ci.yml"))
        if ci_tool != "Github":
            operations.append(DeleteDirOperation(".github"))
        if ci_tool != "Drone":
            operations.append(DeleteFileOperation(".drone.yml"))
        return operations


class RestApiStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        rest_api = context["rest_api"]
        users_path = Path(PROJECT_SLUG, "users")
        if rest_api == "DRF":
            operations.append(DeleteFileOperation(Path("config", "api.py")))
            operations.append(DeleteFileOperation(users_path / "api" / "schema.py"))
        elif rest_api == "Django Ninja":
            operations.append(DeleteFileOperation(Path("config", "api_router.py")))
            operations.append(DeleteFileOperation(users_path / "api" / "serializers.py"))
        else:
            operations.append(DeleteFileOperation(Path("config", "api_router.py")))
            operations.append(DeleteFileOperation(Path("config", "api.py")))
            operations.append(DeleteFileOperation(users_path / "api" / "serializers.py"))
            operations.append(DeleteFileOperation(users_path / "api" / "schema.py"))
            operations.append(DeleteDirOperation(users_path / "api"))
            operations.append(DeleteDirOperation(users_path / "tests" / "api"))
        return operations


class AsyncStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        if context["use_async"].lower() == "n":
            operations.append(DeleteFileOperation(Path("config", "asgi.py")))
            operations.append(DeleteFileOperation(Path("config", "websocket.py")))
        return operations


class SecretGenerationStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        from hooks.core import (
            DEBUG_VALUE,
            generate_random_string,
            generate_random_user,
        )

        operations = []
        debug = context["debug"].lower() == "y"
        postgres_user = DEBUG_VALUE if debug else generate_random_user()
        celery_user = DEBUG_VALUE if debug else generate_random_user()

        envs = [
            (Path(".envs", ".local", ".django"), False),
            (Path(".envs", ".production", ".django"), True),
        ]
        for env_path, is_production in envs:
            if env_path.exists():
                if is_production:
                    secret_key = generate_random_string(
                        length=64, using_digits=True, using_ascii_letters=True,
                    )
                    admin_url = generate_random_string(
                        length=32, using_digits=True, using_ascii_letters=True,
                    )
                    operations.append(
                        SetFlagOperation(env_path, "!!!SET DJANGO_SECRET_KEY!!!", secret_key),
                    )
                    operations.append(
                        SetFlagOperation(env_path, "!!!SET DJANGO_ADMIN_URL!!!", f"{admin_url}/"),
                    )

                pg_pwd = DEBUG_VALUE if debug else generate_random_string(
                    length=64, using_digits=True, using_ascii_letters=True,
                )
                flower_pwd = DEBUG_VALUE if debug else generate_random_string(
                    length=64, using_digits=True, using_ascii_letters=True,
                )
                operations.append(
                    SetFlagOperation(env_path, "!!!SET POSTGRES_USER!!!", postgres_user),
                )
                operations.append(
                    SetFlagOperation(env_path, "!!!SET POSTGRES_PASSWORD!!!", pg_pwd),
                )
                operations.append(
                    SetFlagOperation(env_path, "!!!SET CELERY_FLOWER_USER!!!", celery_user),
                )
                operations.append(
                    SetFlagOperation(env_path, "!!!SET CELERY_FLOWER_PASSWORD!!!", flower_pwd),
                )

        for settings_file in ["local.py", "test.py"]:
            settings_path = Path("config", "settings", settings_file)
            if settings_path.exists():
                secret_key = generate_random_string(
                    length=64, using_digits=True, using_ascii_letters=True,
                )
                operations.append(
                    SetFlagOperation(settings_path, "!!!SET DJANGO_SECRET_KEY!!!", secret_key),
                )

        return operations


class SetupDependenciesStrategy(Strategy):
    def should_apply(self, context: dict) -> bool:
        return True

    def collect_operations(self, context: dict) -> list[Operation]:
        operations = []
        use_docker = context["use_docker"].lower() == "y"

        if use_docker:
            uv_docker_image_path = Path("compose/local/uv/Dockerfile")
            uv_image_tag = "cookiecutter-django-uv-runner:latest"
            operations.append(
                RunCommandOperation([
                    "docker", "build", "--load", "-t", uv_image_tag,
                    "-f", str(uv_docker_image_path), "-q", ".",
                ], env={**os.environ, "DOCKER_BUILDKIT": "1"}),
            )
            current_path = Path.cwd().absolute()
            uv_cmd = ["docker", "run", "--rm", "-v", f"{current_path}:/app", uv_image_tag, "uv"]
        else:
            uv_cmd = ["uv"]

        operations.append(
            RunCommandOperation([*uv_cmd, "add", "--no-sync", "-r", "requirements/production.txt"]),
        )
        operations.append(
            RunCommandOperation([*uv_cmd, "add", "--no-sync", "--dev", "-r", "requirements/local.txt"]),
        )

        operations.append(DeleteDirOperation("requirements"))
        operations.append(DeleteDirOperation(Path("compose/local/uv")))

        return operations


ALL_STRATEGIES: list[type[Strategy]] = [
    LicenseStrategy,
    UsernameTypeStrategy,
    EditorStrategy,
    DockerStrategy,
    HerokuStrategy,
    EnvsStrategy,
    FrontendPipelineStrategy,
    CeleryStrategy,
    CiToolStrategy,
    RestApiStrategy,
    AsyncStrategy,
    SecretGenerationStrategy,
    SetupDependenciesStrategy,
]
