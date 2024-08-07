from typing import Any

from cookiecutter.environment import StrictEnvironment
from jinja2.ext import Extension


class PackageManager:
    managers: dict[str, "PackageManager"] = {}

    def __init_subclass__(cls, **kwargs):
        cls.managers[cls.__name__.lower()] = cls()

    def install(self, obj: str, context: dict[str, Any]) -> str:
        raise NotImplementedError("Subclasses must implement the install method")


class PIP(PackageManager):
    """PIP package manager"""

    def install(self, obj: str, context: dict[str, Any]) -> str:
        if obj == "development":
            return "pip install -r requirements/local.txt"

        return f"pip install {obj}"


class Poetry(PackageManager):
    """Poetry package manager"""

    def install(self, obj: str, context: dict[str, Any]) -> str:
        if obj == "development":
            return "poetry install --with dev"

        return f"poetry add {obj}"


class UV(PackageManager):
    """Poetry package manager"""


class InstallExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment: StrictEnvironment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def install(obj, context):
            # TODO we need to retrieve the package manager from the context or in another way
            # manager_name = context.package_manager
            manager_name = "pip"
            package_manager = PackageManager.managers[manager_name]
            return package_manager.install(obj, context)

        environment.filters["install"] = install
