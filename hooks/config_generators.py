"""
配置生成器模块 - 处理 Django 配置和密钥生成

将配置生成逻辑与文件操作分离，实现纯函数式的配置生成。
"""

from __future__ import annotations

import random
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hooks.operations import Operation
from hooks.operations import SetFlagOperation

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


def generate_random_user() -> str:
    """生成随机用户名"""
    result = generate_random_string(length=32, using_ascii_letters=True)
    return result or "django_user"


@dataclass
class SecretConfig:
    """密钥配置"""

    django_secret_key: str
    django_admin_url: str
    postgres_user: str
    postgres_password: str
    celery_flower_user: str
    celery_flower_password: str

    @classmethod
    def generate(cls, debug: bool = False) -> SecretConfig:
        """生成新的密钥配置"""
        if debug:
            return cls(
                django_secret_key="debug-secret-key-not-for-production",
                django_admin_url="admin/",
                postgres_user="debug",
                postgres_password="debug",
                celery_flower_user="debug",
                celery_flower_password="debug",
            )

        return cls(
            django_secret_key=generate_random_string(
                length=64,
                using_digits=True,
                using_ascii_letters=True,
            )
            or "fallback-secret-key",
            django_admin_url=(
                generate_random_string(
                    length=32,
                    using_digits=True,
                    using_ascii_letters=True,
                )
                or "admin"
            )
            + "/",
            postgres_user=generate_random_user(),
            postgres_password=generate_random_string(
                length=64,
                using_digits=True,
                using_ascii_letters=True,
            )
            or "fallback-password",
            celery_flower_user=generate_random_user(),
            celery_flower_password=generate_random_string(
                length=64,
                using_digits=True,
                using_ascii_letters=True,
            )
            or "fallback-password",
        )


def create_flag_operations(config: SecretConfig) -> list[Operation]:
    """
    创建所有设置标志位的操作

    Args:
        config: 密钥配置

    Returns:
        操作列表
    """
    operations: list[Operation] = []

    # 环境文件路径
    local_django_envs = Path(".envs", ".local", ".django")
    production_django_envs = Path(".envs", ".production", ".django")
    local_postgres_envs = Path(".envs", ".local", ".postgres")
    production_postgres_envs = Path(".envs", ".production", ".postgres")

    # 生产环境 Django 配置
    operations.extend(
        [
            SetFlagOperation(
                file_path=production_django_envs,
                flag="!!!SET DJANGO_SECRET_KEY!!!",
                value=config.django_secret_key,
            ),
            SetFlagOperation(
                file_path=production_django_envs,
                flag="!!!SET DJANGO_ADMIN_URL!!!",
                value=config.django_admin_url,
            ),
        ]
    )

    # PostgreSQL 配置
    for env_file in [local_postgres_envs, production_postgres_envs]:
        operations.extend(
            [
                SetFlagOperation(
                    file_path=env_file,
                    flag="!!!SET POSTGRES_USER!!!",
                    value=config.postgres_user,
                ),
                SetFlagOperation(
                    file_path=env_file,
                    flag="!!!SET POSTGRES_PASSWORD!!!",
                    value=config.postgres_password,
                ),
            ]
        )

    # Celery Flower 配置
    for env_file in [local_django_envs, production_django_envs]:
        operations.extend(
            [
                SetFlagOperation(
                    file_path=env_file,
                    flag="!!!SET CELERY_FLOWER_USER!!!",
                    value=config.celery_flower_user,
                ),
                SetFlagOperation(
                    file_path=env_file,
                    flag="!!!SET CELERY_FLOWER_PASSWORD!!!",
                    value=config.celery_flower_password,
                ),
            ]
        )

    # 设置文件中的密钥
    operations.extend(
        [
            SetFlagOperation(
                file_path=Path("config", "settings", "local.py"),
                flag="!!!SET DJANGO_SECRET_KEY!!!",
                value=config.django_secret_key,
            ),
            SetFlagOperation(
                file_path=Path("config", "settings", "test.py"),
                flag="!!!SET DJANGO_SECRET_KEY!!!",
                value=config.django_secret_key,
            ),
        ]
    )

    return operations


def create_dependency_operations(use_docker: bool) -> list[Operation]:
    """
    创建依赖安装相关的操作

    Args:
        use_docker: 是否使用 Docker

    Returns:
        操作列表
    """
    from hooks.operations import DeleteDirectoryOperation
    from hooks.operations import RunCommandOperation

    operations: list[Operation] = []

    # 依赖安装命令
    if use_docker:
        # Docker 模式：先构建镜像，然后在容器中运行
        uv_dockerfile = Path("compose/local/uv/Dockerfile")
        uv_image_tag = "cookiecutter-django-uv-runner:latest"

        operations.append(
            RunCommandOperation(
                command=[
                    "docker",
                    "build",
                    "--load",
                    "-t",
                    uv_image_tag,
                    "-f",
                    str(uv_dockerfile),
                    "-q",
                    ".",
                ],
                env={"DOCKER_BUILDKIT": "1"},
            ),
        )

        # 安装生产依赖
        operations.append(
            RunCommandOperation(
                command=[
                    "docker",
                    "run",
                    "--rm",
                    "-v",
                    f"{Path.cwd()}:/app",
                    uv_image_tag,
                    "uv",
                    "add",
                    "--no-sync",
                    "-r",
                    "requirements/production.txt",
                ],
            ),
        )

        # 安装开发依赖
        operations.append(
            RunCommandOperation(
                command=[
                    "docker",
                    "run",
                    "--rm",
                    "-v",
                    f"{Path.cwd()}:/app",
                    uv_image_tag,
                    "uv",
                    "add",
                    "--no-sync",
                    "--dev",
                    "-r",
                    "requirements/local.txt",
                ],
            ),
        )
    else:
        # 本地模式：直接使用 uv
        operations.extend(
            [
                RunCommandOperation(
                    command=["uv", "add", "--no-sync", "-r", "requirements/production.txt"],
                ),
                RunCommandOperation(
                    command=["uv", "add", "--no-sync", "--dev", "-r", "requirements/local.txt"],
                ),
            ]
        )

    # 删除 requirements 目录
    operations.append(DeleteDirectoryOperation(dir_path=Path("requirements")))

    # 删除 uv Dockerfile 目录
    operations.append(DeleteDirectoryOperation(dir_path=Path("compose/local/uv")))

    return operations


def get_warning_messages(context: dict[str, Any]) -> list[str]:
    """
    获取需要显示的警告消息

    Args:
        context: 项目上下文字典

    Returns:
        警告消息列表
    """
    warnings: list[str] = []

    use_docker = context.get("use_docker", "").lower() == "y"
    use_heroku = context.get("use_heroku", "").lower() == "y"
    cloud_provider = context.get("cloud_provider", "None")
    keep_local_envs = context.get("keep_local_envs_in_vcs", "").lower() == "y"

    # 环境变量警告
    if not use_docker and not use_heroku and keep_local_envs:
        warnings.append(
            ".env(s) are only utilized when Docker Compose and/or "
            "Heroku support is enabled. Keeping them as requested, but they may not be useful "
            "in your current setup.",
        )

    # 云提供商警告
    if cloud_provider == "None" and not use_docker:
        warnings.append(
            "You chose to not use any cloud providers nor Docker, media files won't be served in production.",
        )

    return warnings
