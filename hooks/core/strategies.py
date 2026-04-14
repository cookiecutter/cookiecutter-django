from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from hooks.core.actions import Action
from hooks.core.context import ExecutionContext


class FeatureStrategy(ABC):
    name: str
    description: str = ""

    @abstractmethod
    def should_apply(self, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def plan(self, context: ExecutionContext) -> list[Action]:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"


class CompositeStrategy(FeatureStrategy):
    def __init__(self, strategies: list[FeatureStrategy]):
        self.strategies = strategies
        self.name = "composite"
        self.description = "Composite strategy combining multiple strategies"

    def should_apply(self, context: ExecutionContext) -> bool:
        return any(s.should_apply(context) for s in self.strategies)

    def plan(self, context: ExecutionContext) -> list[Action]:
        actions = []
        for strategy in self.strategies:
            if strategy.should_apply(context):
                actions.extend(strategy.plan(context))
        return actions


class ConditionalStrategy(FeatureStrategy):
    def __init__(
        self,
        condition: callable[[ExecutionContext], bool],
        true_strategy: FeatureStrategy,
        false_strategy: FeatureStrategy | None = None,
    ):
        self.condition = condition
        self.true_strategy = true_strategy
        self.false_strategy = false_strategy
        self.name = f"conditional_{true_strategy.name}"

    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list[Action]:
        if self.condition(context):
            return self.true_strategy.plan(context)
        if self.false_strategy:
            return self.false_strategy.plan(context)
        return []


class StrategyRegistry:
    _strategies: dict[str, type[FeatureStrategy]] = {}

    @classmethod
    def register(cls, strategy_class: type[FeatureStrategy]) -> type[FeatureStrategy]:
        instance = strategy_class()
        cls._strategies[instance.name] = strategy_class
        return strategy_class

    @classmethod
    def get(cls, name: str) -> type[FeatureStrategy] | None:
        return cls._strategies.get(name)

    @classmethod
    def get_all(cls) -> list[type[FeatureStrategy]]:
        return list(cls._strategies.values())

    @classmethod
    def create_all(cls) -> list[FeatureStrategy]:
        return [strategy_class() for strategy_class in cls._strategies.values()]


def strategy(name: str, description: str = ""):
    def decorator(cls: type[FeatureStrategy]) -> type[FeatureStrategy]:
        cls.name = name
        cls.description = description
        return StrategyRegistry.register(cls)

    return decorator
