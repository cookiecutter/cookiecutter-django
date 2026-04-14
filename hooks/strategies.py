"""
策略模块 - 将每个特性选项转换为独立的策略对象

每个策略类自己声明：
- 要删除什么文件
- 要修改什么配置
- 要添加什么依赖

主流程只负责按用户选择组装要执行的策略列表，没有 if/else 分支。
"""

from __future__ import annotations

import json
import random
import string
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path

from hooks.operations import AppendToFileOperation
from hooks.operations import DeleteDirectoryOperation
from hooks.operations import DeleteFileOperation
from hooks.operations import ModifyFileOperation
from hooks.operations import Operation

# 全局随机数生成器
try:
    _random = random.SystemRandom()
    _using_sysrandom = True
except NotImplementedError:
    _using_sysrandom = False


def generate_random_string(
    length: int,
    using_digits: bool = False,
    using_ascii_letters: bool = False,
    using_punctuation: bool = False,
) -> str | None:
    """生成随机字符串"""
    if not _using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)

    return "".join([_random.choice(symbols) for _ in range(length)])


@dataclass
class ProjectContext:
    """
    项目上下文 - 包含所有 cookiecutter 变量

    策略类通过此对象访问用户选择。
    """

    project_slug: str
    open_source_license: str
    username_type: str
    editor: str
    use_docker: str
    cloud_provider: str
    use_heroku: str
    frontend_pipeline: str
    use_celery: str
    use_async: str
    ci_tool: str
    rest_api: str
    keep_local_envs_in_vcs: str
    debug: str

    @classmethod
    def from_cookiecutter(cls) -> ProjectContext:
        """从 cookiecutter 上下文创建"""
        return cls(
            project_slug="{{ cookiecutter.project_slug }}",
            open_source_license="{{ cookiecutter.open_source_license }}",
            username_type="{{ cookiecutter.username_type }}",
            editor="{{ cookiecutter.editor }}",
            use_docker="{{ cookiecutter.use_docker }}",
            cloud_provider="{{ cookiecutter.cloud_provider }}",
            use_heroku="{{ cookiecutter.use_heroku }}",
            frontend_pipeline="{{ cookiecutter.frontend_pipeline }}",
            use_celery="{{ cookiecutter.use_celery }}",
            use_async="{{ cookiecutter.use_async }}",
            ci_tool="{{ cookiecutter.ci_tool }}",
            rest_api="{{ cookiecutter.rest_api }}",
            keep_local_envs_in_vcs="{{ cookiecutter.keep_local_envs_in_vcs }}",
            debug="{{ cookiecutter.debug }}",
        )

    def is_yes(self, value: str) -> bool:
        """检查值是否为 'y'"""
        return value.lower() == "y"


class ProjectStrategy(ABC):
    """
    项目策略基类

    每个特性选项对应一个策略类，策略类决定：
    - 是否适用于当前上下文
    - 要执行哪些操作
    """

    @abstractmethod
    def applies_to(self, context: ProjectContext) -> bool:
        """
        判断此策略是否适用于当前上下文

        Returns:
            True 如果策略应该被应用
        """

    @abstractmethod
    def get_operations(self, context: ProjectContext) -> list[Operation]:
        """
        获取此策略要执行的所有操作

        Returns:
            操作列表
        """

    def get_name(self) -> str:
        """获取策略名称"""
        return self.__class__.__name__


# =============================================================================
# 开源许可证策略
# =============================================================================


class NotOpenSourceStrategy(ProjectStrategy):
    """非开源项目策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.open_source_license == "Not open source"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path("CONTRIBUTORS.txt")),
            DeleteFileOperation(file_path=Path("LICENSE")),
        ]


class NotGPLv3Strategy(ProjectStrategy):
    """非 GPLv3 许可证策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.open_source_license != "GPLv3"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path("COPYING")),
        ]


# =============================================================================
# 用户认证策略
# =============================================================================


class UsernameAuthStrategy(ProjectStrategy):
    """用户名认证策略（使用 Django 内置）"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.username_type == "username"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        users_path = Path(context.project_slug, "users")
        return [
            DeleteFileOperation(file_path=users_path / "managers.py"),
            DeleteFileOperation(file_path=users_path / "tests" / "test_managers.py"),
        ]


# =============================================================================
# 编辑器策略
# =============================================================================


class NonPyCharmStrategy(ProjectStrategy):
    """非 PyCharm 编辑器策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.editor != "PyCharm"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        ops: list[Operation] = [
            DeleteDirectoryOperation(dir_path=Path(".idea")),
            DeleteDirectoryOperation(dir_path=Path("docs", "pycharm")),
        ]
        return ops


class PyCharmDockerStrategy(ProjectStrategy):
    """PyCharm + Docker 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.editor == "PyCharm" and context.is_yes(context.use_docker)

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        # 这个策略实际上不需要删除文件，但保留作为示例
        return []


class PyCharmNonDockerStrategy(ProjectStrategy):
    """PyCharm 但不用 Docker 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.editor == "PyCharm" and not context.is_yes(context.use_docker)

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        run_configs = Path(".idea", "runConfigurations")
        return [
            DeleteFileOperation(file_path=run_configs / "docker_compose_up_django.xml"),
            DeleteFileOperation(file_path=run_configs / "docker_compose_up_docs.xml"),
        ]


# =============================================================================
# Docker 策略
# =============================================================================


class DockerStrategy(ProjectStrategy):
    """使用 Docker 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.is_yes(context.use_docker)

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        ops: list[Operation] = [
            DeleteDirectoryOperation(dir_path=Path("utility")),
        ]

        # 如果使用云提供商，删除 nginx
        if context.cloud_provider.lower() != "none":
            ops.append(
                DeleteDirectoryOperation(dir_path=Path("compose", "production", "nginx")),
            )

        # 如果不是 AWS，删除 AWS Dockerfile
        if context.cloud_provider != "AWS":
            ops.append(
                DeleteDirectoryOperation(dir_path=Path("compose", "production", "aws")),
            )

        return ops


class NonDockerStrategy(ProjectStrategy):
    """不使用 Docker 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return not context.is_yes(context.use_docker)

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteDirectoryOperation(dir_path=Path(".devcontainer")),
            DeleteDirectoryOperation(dir_path=Path("compose")),
            DeleteFileOperation(file_path=Path("docker-compose.local.yml")),
            DeleteFileOperation(file_path=Path("docker-compose.production.yml")),
            DeleteFileOperation(file_path=Path(".dockerignore")),
            DeleteFileOperation(file_path=Path("justfile")),
        ]


# =============================================================================
# Heroku 策略
# =============================================================================


class NonHerokuStrategy(ProjectStrategy):
    """不使用 Heroku 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return not context.is_yes(context.use_heroku)

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        ops: list[Operation] = [
            DeleteFileOperation(file_path=Path("Procfile")),
            DeleteDirectoryOperation(dir_path=Path("bin")),
        ]
        return ops


# =============================================================================
# 环境变量策略
# =============================================================================


class EnvsInVCSWithoutDockerHerokuStrategy(ProjectStrategy):
    """保留环境变量在 VCS 中，但不使用 Docker 或 Heroku"""

    def applies_to(self, context: ProjectContext) -> bool:
        return (
            not context.is_yes(context.use_docker)
            and not context.is_yes(context.use_heroku)
            and context.is_yes(context.keep_local_envs_in_vcs)
        )

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        # 这个策略只打印警告，不执行操作
        # 警告在策略执行后单独处理
        return []


class RemoveEnvsStrategy(ProjectStrategy):
    """删除环境变量相关文件策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return (
            not context.is_yes(context.use_docker)
            and not context.is_yes(context.use_heroku)
            and not context.is_yes(context.keep_local_envs_in_vcs)
        )

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteDirectoryOperation(dir_path=Path(".envs")),
            DeleteFileOperation(file_path=Path("merge_production_dotenvs_in_dotenv.py")),
            DeleteDirectoryOperation(dir_path=Path("tests")),
        ]


class GitignoreEnvsStrategy(ProjectStrategy):
    """添加环境变量到 gitignore 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.is_yes(context.use_docker) or context.is_yes(context.use_heroku)

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        ops: list[Operation] = [
            AppendToFileOperation(file_path=Path(".gitignore"), content=".env"),
            AppendToFileOperation(file_path=Path(".gitignore"), content=".envs/*"),
        ]

        if context.is_yes(context.keep_local_envs_in_vcs):
            ops.append(
                AppendToFileOperation(file_path=Path(".gitignore"), content="!.envs/.local/"),
            )

        return ops


# =============================================================================
# 前端构建策略
# =============================================================================


class NoFrontendPipelineStrategy(ProjectStrategy):
    """无前端构建工具策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.frontend_pipeline in ["None", "Django Compressor"]

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        ops: list[Operation] = [
            DeleteFileOperation(file_path=Path("gulpfile.mjs")),
            DeleteDirectoryOperation(dir_path=Path("webpack")),
            DeleteDirectoryOperation(dir_path=Path(context.project_slug, "static", "sass")),
            DeleteFileOperation(file_path=Path("package.json")),
        ]

        # 删除 vendors.js
        vendors_js = Path(context.project_slug, "static", "js", "vendors.js")
        ops.append(DeleteFileOperation(file_path=vendors_js))

        # 如果使用 Docker，删除 node Dockerfile
        if context.is_yes(context.use_docker):
            ops.append(
                DeleteDirectoryOperation(dir_path=Path("compose", "local", "node")),
            )

        return ops


class GulpStrategy(ProjectStrategy):
    """使用 Gulp 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.frontend_pipeline == "Gulp"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        ops: list[Operation] = [
            DeleteDirectoryOperation(dir_path=Path("webpack")),
            DeleteFileOperation(file_path=Path(context.project_slug, "static", "js", "vendors.js")),
            DeleteFileOperation(file_path=Path(context.project_slug, "static", "css", "project.css")),
        ]

        # 修改 package.json
        def modify_package_json(content: str) -> str:
            data = json.loads(content)
            # 删除 webpack 相关依赖
            webpack_deps = [
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
            ]
            for dep in webpack_deps:
                data["devDependencies"].pop(dep, None)
            # 删除 babel 配置
            data.pop("babel", None)
            # 更新 scripts
            data["scripts"]["dev"] = "gulp"
            data["scripts"]["build"] = "gulp build"
            return json.dumps(data, ensure_ascii=False, indent=2) + "\n"

        ops.append(
            ModifyFileOperation(file_path=Path("package.json"), modifier=modify_package_json),
        )

        return ops


class WebpackStrategy(ProjectStrategy):
    """使用 Webpack 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.frontend_pipeline == "Webpack"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        ops: list[Operation] = [
            DeleteFileOperation(file_path=Path("gulpfile.mjs")),
            DeleteFileOperation(file_path=Path(context.project_slug, "static", "css", "project.css")),
        ]

        # 修改 package.json
        def modify_package_json(content: str) -> str:
            data = json.loads(content)
            # 删除 gulp 相关依赖
            gulp_deps = [
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
            for dep in gulp_deps:
                data["devDependencies"].pop(dep, None)

            # 设置 scripts
            use_docker = context.is_yes(context.use_docker)
            use_async = context.is_yes(context.use_async)

            if use_docker:
                data["devDependencies"].pop("concurrently", None)
                data["scripts"]["dev"] = "webpack serve --config webpack/dev.config.js"
                data["scripts"]["build"] = "webpack --config webpack/prod.config.js"
            else:
                dev_django_cmd = (
                    "uvicorn config.asgi:application --reload" if use_async else "python manage.py runserver_plus"
                )
                data["scripts"]["dev"] = "concurrently npm:dev:*"
                data["scripts"]["dev:webpack"] = "webpack serve --config webpack/dev.config.js"
                data["scripts"]["dev:django"] = dev_django_cmd
                data["scripts"]["build"] = "webpack --config webpack/prod.config.js"

            return json.dumps(data, ensure_ascii=False, indent=2) + "\n"

        ops.append(
            ModifyFileOperation(file_path=Path("package.json"), modifier=modify_package_json),
        )

        return ops


# =============================================================================
# Celery 策略
# =============================================================================


class NonCeleryStrategy(ProjectStrategy):
    """不使用 Celery 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return not context.is_yes(context.use_celery)

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        ops: list[Operation] = [
            DeleteFileOperation(file_path=Path("config", "celery_app.py")),
            DeleteFileOperation(file_path=Path(context.project_slug, "users", "tasks.py")),
            DeleteFileOperation(file_path=Path(context.project_slug, "users", "tests", "test_tasks.py")),
        ]

        # 如果使用 Docker，删除 celery compose 目录
        if context.is_yes(context.use_docker):
            ops.extend(
                [
                    DeleteDirectoryOperation(dir_path=Path("compose", "local", "django", "celery")),
                    DeleteDirectoryOperation(dir_path=Path("compose", "production", "django", "celery")),
                ]
            )

        return ops


# =============================================================================
# CI 工具策略
# =============================================================================


class NonTravisStrategy(ProjectStrategy):
    """不使用 Travis CI 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.ci_tool != "Travis"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path(".travis.yml")),
        ]


class NonGitlabStrategy(ProjectStrategy):
    """不使用 GitLab CI 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.ci_tool != "Gitlab"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path(".gitlab-ci.yml")),
        ]


class NonGithubStrategy(ProjectStrategy):
    """不使用 GitHub Actions 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.ci_tool != "Github"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteDirectoryOperation(dir_path=Path(".github")),
        ]


class NonDroneStrategy(ProjectStrategy):
    """不使用 Drone CI 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.ci_tool != "Drone"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path(".drone.yml")),
        ]


# =============================================================================
# REST API 策略
# =============================================================================


class DRFStrategy(ProjectStrategy):
    """使用 Django REST Framework 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.rest_api == "DRF"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path("config", "api.py")),
            DeleteFileOperation(file_path=Path(context.project_slug, "users", "api", "schema.py")),
        ]


class NinjaStrategy(ProjectStrategy):
    """使用 Django Ninja 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.rest_api == "Django Ninja"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path("config", "api_router.py")),
            DeleteFileOperation(file_path=Path(context.project_slug, "users", "api", "serializers.py")),
        ]


class NoRestAPIStrategy(ProjectStrategy):
    """不使用 REST API 策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return context.rest_api == "None"

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path("config", "api_router.py")),
            DeleteFileOperation(file_path=Path("config", "api.py")),
            DeleteFileOperation(file_path=Path(context.project_slug, "users", "api", "serializers.py")),
            DeleteFileOperation(file_path=Path(context.project_slug, "users", "api", "schema.py")),
            DeleteDirectoryOperation(dir_path=Path(context.project_slug, "users", "api")),
            DeleteDirectoryOperation(dir_path=Path(context.project_slug, "users", "tests", "api")),
        ]


# =============================================================================
# 异步策略
# =============================================================================


class NonAsyncStrategy(ProjectStrategy):
    """不使用异步策略"""

    def applies_to(self, context: ProjectContext) -> bool:
        return not context.is_yes(context.use_async)

    def get_operations(self, context: ProjectContext) -> list[Operation]:
        return [
            DeleteFileOperation(file_path=Path("config", "asgi.py")),
            DeleteFileOperation(file_path=Path("config", "websocket.py")),
        ]


# =============================================================================
# 策略注册表
# =============================================================================


class StrategyRegistry:
    """
    策略注册表 - 管理所有策略

    负责：
    - 注册策略
    - 根据上下文选择适用的策略
    - 收集所有操作
    """

    def __init__(self) -> None:
        self._strategies: list[type[ProjectStrategy]] = []

    def register(self, strategy_class: type[ProjectStrategy]) -> type[ProjectStrategy]:
        """注册策略类"""
        self._strategies.append(strategy_class)
        return strategy_class

    def get_applicable_strategies(
        self,
        context: ProjectContext,
    ) -> list[ProjectStrategy]:
        """获取适用于当前上下文的所有策略实例"""
        instances = []
        for strategy_class in self._strategies:
            instance = strategy_class()
            if instance.applies_to(context):
                instances.append(instance)
        return instances

    def collect_operations(self, context: ProjectContext) -> list[Operation]:
        """
        收集所有适用策略的操作

        Args:
            context: 项目上下文

        Returns:
            所有操作的列表
        """
        operations: list[Operation] = []
        strategies = self.get_applicable_strategies(context)

        for strategy in strategies:
            ops = strategy.get_operations(context)
            operations.extend(ops)

        return operations


# 创建全局策略注册表
registry = StrategyRegistry()

# 注册所有策略
registry.register(NotOpenSourceStrategy)
registry.register(NotGPLv3Strategy)
registry.register(UsernameAuthStrategy)
registry.register(NonPyCharmStrategy)
registry.register(PyCharmDockerStrategy)
registry.register(PyCharmNonDockerStrategy)
registry.register(DockerStrategy)
registry.register(NonDockerStrategy)
registry.register(NonHerokuStrategy)
registry.register(EnvsInVCSWithoutDockerHerokuStrategy)
registry.register(RemoveEnvsStrategy)
registry.register(GitignoreEnvsStrategy)
registry.register(NoFrontendPipelineStrategy)
registry.register(GulpStrategy)
registry.register(WebpackStrategy)
registry.register(NonCeleryStrategy)
registry.register(NonTravisStrategy)
registry.register(NonGitlabStrategy)
registry.register(NonGithubStrategy)
registry.register(NonDroneStrategy)
registry.register(DRFStrategy)
registry.register(NinjaStrategy)
registry.register(NoRestAPIStrategy)
registry.register(NonAsyncStrategy)
